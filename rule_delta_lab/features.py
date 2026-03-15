"""Feature extraction, identities, and reduced bases for the rule-delta lab."""

from __future__ import annotations

import math
from typing import Dict, List, Mapping, Optional, Sequence

from .graph_core import State, UGraph, beta1_cycle_rank, count_components


FULL_FEATURES = [
    "tokens",
    "nodes",
    "edges",
    "components",
    "beta1",
    "wedges",
    "triangles",
    "star3",
    "c4",
    "deg_sq_sum",
    "spectral_radius",
    "clustering",
    "dim_proxy",
]

REDUCED_FEATURES = [
    "tokens",
    "nodes",
    "components",
    "beta1",
    "wedges",
    "triangles",
    "star3",
    "c4",
    "spectral_radius",
    "clustering",
    "dim_proxy",
]

CORE_FEATURES = ["tokens", "nodes", "components", "beta1"]
MOTIF_FEATURES = ["wedges", "triangles", "star3"]
REGIME_FEATURES = ["c4", "spectral_radius", "clustering", "dim_proxy"]


def comb2(k: int) -> int:
    """Return k choose 2."""

    return 0 if k < 2 else k * (k - 1) // 2


def comb3(k: int) -> int:
    """Return k choose 3."""

    return 0 if k < 3 else k * (k - 1) * (k - 2) // 6


def wedge_count(graph: UGraph) -> int:
    return sum(comb2(graph.degree(node)) for node in graph.nodes())


def star3_count(graph: UGraph) -> int:
    return sum(comb3(graph.degree(node)) for node in graph.nodes())


def degree_sq_sum(graph: UGraph) -> int:
    return sum(graph.degree(node) ** 2 for node in graph.nodes())


def triangle_count(graph: UGraph) -> int:
    count = 0
    for node in graph.nodes():
        forward = [neighbor for neighbor in graph.neighbors(node) if neighbor > node]
        forward_set = set(forward)
        for neighbor in forward:
            for target in graph.neighbors(neighbor):
                if target > neighbor and target in forward_set:
                    count += 1
    return count


def four_cycle_count(graph: UGraph) -> int:
    total = 0
    nodes = sorted(graph.nodes())
    for index, u in enumerate(nodes):
        neighbors_u = graph.neighbors(u)
        for v in nodes[index + 1 :]:
            total += comb2(len(neighbors_u.intersection(graph.neighbors(v))))
    return total // 2


def adjacency_spectral_radius(graph: UGraph, iters: int = 25) -> float:
    nodes = graph.nodes()
    n_nodes = len(nodes)
    if n_nodes == 0:
        return 0.0

    index = {node: idx for idx, node in enumerate(nodes)}
    vector = [1.0 / math.sqrt(n_nodes)] * n_nodes
    rayleigh = 0.0
    for _ in range(iters):
        next_vector = [0.0] * n_nodes
        for node in nodes:
            idx = index[node]
            next_vector[idx] = sum(vector[index[neighbor]] for neighbor in graph.neighbors(node))
        norm = math.sqrt(sum(value * value for value in next_vector))
        if norm == 0.0:
            return 0.0
        vector = [value / norm for value in next_vector]
        denominator = sum(value * value for value in vector)
        numerator = 0.0
        for node in nodes:
            idx = index[node]
            numerator += vector[idx] * sum(vector[index[neighbor]] for neighbor in graph.neighbors(node))
        rayleigh = numerator / denominator if denominator else 0.0
    return float(rayleigh)


def _deterministic_sample(nodes: Sequence[int], limit: int) -> List[int]:
    ordered = sorted(nodes)
    if len(ordered) <= limit:
        return ordered
    if limit <= 1:
        return [ordered[len(ordered) // 2]]
    span = len(ordered) - 1
    indices = [round(position * span / (limit - 1)) for position in range(limit)]
    return [ordered[index] for index in indices]


def approx_clustering(graph: UGraph, sample: int = 200) -> float:
    nodes = graph.nodes()
    if not nodes:
        return 0.0
    sample_nodes = _deterministic_sample(nodes, sample)
    coefficients: List[float] = []
    for node in sample_nodes:
        neighbors = list(graph.neighbors(node))
        degree = len(neighbors)
        if degree < 2:
            coefficients.append(0.0)
            continue
        links = 0
        for index, a in enumerate(neighbors):
            neighbors_a = graph.neighbors(a)
            for b in neighbors[index + 1 :]:
                if b in neighbors_a:
                    links += 1
        coefficients.append(2.0 * links / (degree * (degree - 1)))
    return sum(coefficients) / len(coefficients)


def bfs_ball_volumes(graph: UGraph, root: int, r_max: int) -> List[int]:
    if root not in graph.adj:
        return [0] * (r_max + 1)
    visited = {root}
    frontier = {root}
    volumes = [1]
    for _ in range(r_max):
        next_frontier = set()
        for node in frontier:
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_frontier.add(neighbor)
        frontier = next_frontier
        volumes.append(len(visited))
        if not frontier:
            volumes.extend([len(visited)] * (r_max - len(volumes) + 1))
            break
    return volumes[: r_max + 1]


def volume_dimension_proxy(graph: UGraph, samples: int = 8, r_max: int = 4) -> float:
    nodes = graph.nodes()
    if len(nodes) < 2:
        return 0.0

    roots = _deterministic_sample(nodes, samples)
    slopes: List[float] = []
    for root in roots:
        volumes = bfs_ball_volumes(graph, root, r_max)
        xs: List[float] = []
        ys: List[float] = []
        for radius in range(1, len(volumes)):
            if volumes[radius] > 1:
                xs.append(math.log(radius))
                ys.append(math.log(volumes[radius]))
        if len(xs) < 2:
            continue
        mean_x = sum(xs) / len(xs)
        mean_y = sum(ys) / len(ys)
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        denominator = sum((x - mean_x) ** 2 for x in xs)
        if denominator > 0:
            slopes.append(numerator / denominator)
    return float(sum(slopes) / len(slopes)) if slopes else 0.0


def feature_row(state: State) -> Dict[str, float]:
    graph = state.g
    edges = graph.num_edges()
    wedges = wedge_count(graph)
    return {
        "t": state.t,
        "tokens": float(len(state.tokens)),
        "nodes": float(graph.num_nodes()),
        "edges": float(edges),
        "components": float(count_components(graph)),
        "beta1": float(beta1_cycle_rank(graph)),
        "wedges": float(wedges),
        "triangles": float(triangle_count(graph)),
        "star3": float(star3_count(graph)),
        "c4": float(four_cycle_count(graph)),
        "deg_sq_sum": float(degree_sq_sum(graph)),
        "spectral_radius": float(adjacency_spectral_radius(graph)),
        "clustering": float(approx_clustering(graph)),
        "dim_proxy": float(volume_dimension_proxy(graph)),
    }


def feature_delta(before: State, after: State, feature_names: Sequence[str]) -> Dict[str, float]:
    before_row = feature_row(before)
    after_row = feature_row(after)
    return {name: after_row[name] - before_row[name] for name in feature_names}


def identity_residuals(row: Mapping[str, float]) -> Dict[str, float]:
    residuals: Dict[str, float] = {}
    if {"beta1", "edges", "nodes", "components"}.issubset(row):
        residuals["beta1_identity"] = float(row["beta1"]) - (
            float(row["edges"]) - float(row["nodes"]) + float(row["components"])
        )
    if {"deg_sq_sum", "wedges", "edges"}.issubset(row):
        residuals["deg_sq_identity"] = float(row["deg_sq_sum"]) - (
            2.0 * float(row["wedges"]) + 2.0 * float(row["edges"])
        )
    return residuals


def resolve_feature_names(feature_basis: str, feature_csv: Optional[str]) -> List[str]:
    basis = FULL_FEATURES if feature_basis == "full" else REDUCED_FEATURES
    if feature_csv is None:
        return list(basis)

    requested = [name.strip() for name in feature_csv.split(",") if name.strip()]
    if not requested:
        raise ValueError("Ingen feature-navn ble oppgitt")

    available = set(FULL_FEATURES)
    unknown = [name for name in requested if name not in available]
    if unknown:
        raise ValueError(f"Ukjente features: {', '.join(unknown)}")

    if feature_basis == "reduced":
        disallowed = [name for name in requested if name not in REDUCED_FEATURES]
        if disallowed:
            raise ValueError(
                "Redusert basis fjerner algebraisk redundante koordinater; "
                f"fjern: {', '.join(disallowed)}"
            )
    return requested
