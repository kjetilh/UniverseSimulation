"""Feature extraction and algebraic identities for the feature lab."""

from __future__ import annotations

import math
from typing import Dict, Iterable, List, Mapping, Optional, Sequence

from .graph_core import State, UGraph, beta1_cycle_rank, count_components


FULL_FEATURE_ORDER = [
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

REDUCED_FEATURE_ORDER = [
    "tokens",
    "nodes",
    "edges",
    "components",
    "wedges",
    "triangles",
    "star3",
    "c4",
    "spectral_radius",
    "clustering",
    "dim_proxy",
]

ALGEBRAIC_IDENTITY_NOTES = [
    "`beta1 = edges - nodes + components`",
    "`deg_sq_sum = 2*wedges + 2*edges`",
]


def comb2(k: int) -> int:
    """Return k choose 2."""
    return 0 if k < 2 else k * (k - 1) // 2


def comb3(k: int) -> int:
    """Return k choose 3."""
    return 0 if k < 3 else k * (k - 1) * (k - 2) // 6


def wedge_count(g: UGraph) -> int:
    """Count wedges centred on all nodes."""
    return sum(comb2(g.degree(node)) for node in g.nodes())


def star3_count(g: UGraph) -> int:
    """Count 3-stars."""
    return sum(comb3(g.degree(node)) for node in g.nodes())


def degree_sq_sum(g: UGraph) -> int:
    """Return the sum of squared degrees."""
    return sum(g.degree(node) ** 2 for node in g.nodes())


def triangle_count(g: UGraph) -> int:
    """Count triangles exactly via node ordering."""
    count = 0
    for node in g.nodes():
        forward = [neighbor for neighbor in g.neighbors(node) if neighbor > node]
        forward_set = set(forward)
        for neighbor in forward:
            for target in g.neighbors(neighbor):
                if target > neighbor and target in forward_set:
                    count += 1
    return count


def four_cycle_count(g: UGraph) -> int:
    """Count 4-cycles exactly."""
    total = 0
    nodes = sorted(g.nodes())
    for idx, u in enumerate(nodes):
        neighbors_u = g.neighbors(u)
        for v in nodes[idx + 1 :]:
            common = len(neighbors_u.intersection(g.neighbors(v)))
            total += comb2(common)
    return total // 2


def adjacency_spectral_radius(g: UGraph, iters: int = 25) -> float:
    """Approximate the adjacency spectral radius with power iteration."""
    nodes = g.nodes()
    n = len(nodes)
    if n == 0:
        return 0.0

    index = {node: idx for idx, node in enumerate(nodes)}
    x = [1.0 / math.sqrt(n)] * n
    rayleigh = 0.0
    for _ in range(iters):
        y = [0.0] * n
        for node in nodes:
            idx = index[node]
            y[idx] = sum(x[index[neighbor]] for neighbor in g.neighbors(node))
        norm = math.sqrt(sum(value * value for value in y))
        if norm == 0.0:
            return 0.0
        x = [value / norm for value in y]
        numerator = 0.0
        denominator = sum(value * value for value in x)
        for node in nodes:
            idx = index[node]
            numerator += x[idx] * sum(x[index[neighbor]] for neighbor in g.neighbors(node))
        rayleigh = numerator / denominator if denominator else 0.0
    return float(rayleigh)


def _deterministic_sample(nodes: Sequence[int], limit: int) -> List[int]:
    ordered = sorted(nodes)
    if len(ordered) <= limit:
        return ordered
    if limit <= 1:
        return [ordered[len(ordered) // 2]]
    span = len(ordered) - 1
    indices = [round(pos * span / (limit - 1)) for pos in range(limit)]
    return [ordered[index] for index in indices]


def approx_clustering(g: UGraph, sample: int = 200) -> float:
    """Approximate clustering using a deterministic node sample."""
    nodes = g.nodes()
    if not nodes:
        return 0.0
    sample_nodes = _deterministic_sample(nodes, sample)
    coefficients: List[float] = []
    for node in sample_nodes:
        neighbors = list(g.neighbors(node))
        degree = len(neighbors)
        if degree < 2:
            coefficients.append(0.0)
            continue
        links = 0
        for idx, a in enumerate(neighbors):
            neighbors_a = g.neighbors(a)
            for b in neighbors[idx + 1 :]:
                if b in neighbors_a:
                    links += 1
        coefficients.append(2.0 * links / (degree * (degree - 1)))
    return sum(coefficients) / len(coefficients)


def bfs_ball_volumes(g: UGraph, root: int, r_max: int) -> List[int]:
    """Return ball volumes around root up to radius r_max."""
    if root not in g.adj:
        return [0] * (r_max + 1)
    visited = {root}
    frontier = {root}
    volumes = [1]
    for _ in range(r_max):
        next_frontier = set()
        for node in frontier:
            for neighbor in g.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_frontier.add(neighbor)
        frontier = next_frontier
        volumes.append(len(visited))
        if not frontier:
            volumes.extend([len(visited)] * (r_max - len(volumes) + 1))
            break
    return volumes[: r_max + 1]


def volume_dimension_proxy(g: UGraph, samples: int = 8, r_max: int = 4) -> float:
    """Return a coarse dimension proxy from local volume growth."""
    nodes = g.nodes()
    if len(nodes) < 2:
        return 0.0

    roots = _deterministic_sample(nodes, samples)
    slopes: List[float] = []
    for root in roots:
        volumes = bfs_ball_volumes(g, root, r_max)
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


def full_feature_row(state: State) -> Dict[str, float]:
    """Extract the full feature row for the current state."""
    g = state.g
    return {
        "t": state.t,
        "tokens": float(len(state.tokens)),
        "nodes": float(g.num_nodes()),
        "edges": float(g.num_edges()),
        "components": float(count_components(g)),
        "beta1": float(beta1_cycle_rank(g)),
        "wedges": float(wedge_count(g)),
        "triangles": float(triangle_count(g)),
        "star3": float(star3_count(g)),
        "c4": float(four_cycle_count(g)),
        "deg_sq_sum": float(degree_sq_sum(g)),
        "spectral_radius": float(adjacency_spectral_radius(g)),
        "clustering": float(approx_clustering(g)),
        "dim_proxy": float(volume_dimension_proxy(g)),
    }


def feature_row(state: State, feature_names: Optional[Sequence[str]] = None) -> Dict[str, float]:
    """Extract either the full feature row or a named subset."""
    row = full_feature_row(state)
    if feature_names is None:
        return row
    return {"t": row["t"], **{name: row[name] for name in feature_names}}


def feature_delta(before: State, after: State, feature_names: Sequence[str]) -> Dict[str, float]:
    """Return exact feature deltas by differencing before/after states."""
    before_row = full_feature_row(before)
    after_row = full_feature_row(after)
    return {name: after_row[name] - before_row[name] for name in feature_names}


def resolve_feature_names(feature_basis: str, feature_csv: Optional[str]) -> List[str]:
    """Resolve analysis features for full or reduced feature bases."""
    basis = FULL_FEATURE_ORDER if feature_basis == "full" else REDUCED_FEATURE_ORDER
    if feature_csv is None:
        return list(basis)

    requested = [name.strip() for name in feature_csv.split(",") if name.strip()]
    if not requested:
        raise ValueError("No feature names were provided")

    available = set(FULL_FEATURE_ORDER)
    unknown = [name for name in requested if name not in available]
    if unknown:
        raise ValueError(f"Unknown features requested: {', '.join(unknown)}")

    if feature_basis == "reduced":
        disallowed = [name for name in requested if name not in REDUCED_FEATURE_ORDER]
        if disallowed:
            raise ValueError(
                "Reduced basis removes algebraically redundant coordinates; "
                f"remove: {', '.join(disallowed)}"
            )
    return requested


def identity_residuals(row: Mapping[str, float]) -> Dict[str, float]:
    """Return residuals for the built-in algebraic identities."""
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


def max_abs_identity_residuals(rows: Iterable[Mapping[str, float]]) -> Dict[str, float]:
    """Return the largest absolute identity residual observed in a set of rows."""
    maxima: Dict[str, float] = {}
    for row in rows:
        for name, residual in identity_residuals(row).items():
            maxima[name] = max(maxima.get(name, 0.0), abs(residual))
    return maxima
