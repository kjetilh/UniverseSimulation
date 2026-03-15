
#!/usr/bin/env python3
"""relational_universe_perturbation_lab.py

v0.5 perturbation / causal-cone laboratory for the relational-universe toy model.

Main ideas
----------
1. Evolve two replicas with a shared stochastic instruction stream ("common noise").
2. Introduce one local perturbation in replica B only.
3. Measure how fast the induced difference set spreads through graph space and feature space.

Important methodological point
------------------------------
This lab defaults to a *strictly local* rule sector. It intentionally avoids the
global bridge test used in earlier "avoid_disconnect" modes, because that test
is nonlocal and obscures any claim about emergent causal cones.

The lab therefore studies locality in the cleaner sector:
- seed attachment (local)
- token traversal + local delete / triad / swap
- optional leaf pruning and token relocation implemented by local endpoint data only

This makes the perturbation experiment a better proxy for "bounded information propagation".
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

try:
    import numpy as np
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"numpy is required: {exc}")


# ----------------------------
# Basic graph
# ----------------------------

class UGraph:
    def __init__(self) -> None:
        self.adj: Dict[int, Set[int]] = {}

    def clone(self) -> "UGraph":
        g = UGraph()
        g.adj = {v: set(ns) for v, ns in self.adj.items()}
        return g

    def add_node(self, v: int) -> None:
        if v not in self.adj:
            self.adj[v] = set()

    def add_edge(self, a: int, b: int) -> None:
        if a == b:
            return
        self.add_node(a)
        self.add_node(b)
        self.adj[a].add(b)
        self.adj[b].add(a)

    def has_edge(self, a: int, b: int) -> bool:
        return a in self.adj and b in self.adj[a]

    def remove_edge(self, a: int, b: int) -> None:
        if a in self.adj:
            self.adj[a].discard(b)
        if b in self.adj:
            self.adj[b].discard(a)

    def remove_node(self, v: int) -> None:
        if v not in self.adj:
            return
        for u in list(self.adj[v]):
            self.adj[u].discard(v)
        del self.adj[v]

    def neighbors(self, v: int) -> Set[int]:
        return self.adj.get(v, set())

    def degree(self, v: int) -> int:
        return len(self.adj.get(v, ()))

    def nodes(self) -> List[int]:
        return list(self.adj.keys())

    def num_nodes(self) -> int:
        return len(self.adj)

    def num_edges(self) -> int:
        return sum(len(ns) for ns in self.adj.values()) // 2

    def edge_set(self) -> Set[Tuple[int, int]]:
        out: Set[Tuple[int, int]] = set()
        for a, ns in self.adj.items():
            for b in ns:
                if a < b:
                    out.add((a, b))
        return out

    def random_node(self, rng: random.Random) -> Optional[int]:
        vs = self.nodes()
        return rng.choice(vs) if vs else None


# ----------------------------
# Combinatorics / features
# ----------------------------

def comb2(k: int) -> int:
    return 0 if k < 2 else k * (k - 1) // 2

def comb3(k: int) -> int:
    return 0 if k < 3 else k * (k - 1) * (k - 2) // 6

def count_components(g: UGraph) -> int:
    vs = g.nodes()
    if not vs:
        return 0
    seen: Set[int] = set()
    c = 0
    for start in vs:
        if start in seen:
            continue
        c += 1
        stack = [start]
        seen.add(start)
        while stack:
            v = stack.pop()
            for u in g.neighbors(v):
                if u not in seen:
                    seen.add(u)
                    stack.append(u)
    return c

def beta1_cycle_rank(g: UGraph) -> int:
    return g.num_edges() - g.num_nodes() + count_components(g)

def wedge_count(g: UGraph) -> int:
    return sum(comb2(g.degree(v)) for v in g.nodes())

def star3_count(g: UGraph) -> int:
    return sum(comb3(g.degree(v)) for v in g.nodes())

def triangle_count(g: UGraph) -> int:
    count = 0
    for v in g.nodes():
        nv = [u for u in g.neighbors(v) if u > v]
        nset = set(nv)
        for u in nv:
            for w in g.neighbors(u):
                if w > u and w in nset:
                    count += 1
    return count

def four_cycle_count(g: UGraph) -> int:
    vs = sorted(g.nodes())
    total = 0
    for i, u in enumerate(vs):
        nu = g.neighbors(u)
        for v in vs[i + 1 :]:
            c = len(nu.intersection(g.neighbors(v)))
            total += comb2(c)
    return total // 2

def adjacency_spectral_radius(g: UGraph, iters: int = 30) -> float:
    vs = g.nodes()
    n = len(vs)
    if n == 0:
        return 0.0
    idx = {v: i for i, v in enumerate(vs)}
    x = [1.0 / math.sqrt(n)] * n
    lam = 0.0
    for _ in range(iters):
        y = [0.0] * n
        for v in vs:
            i = idx[v]
            s = 0.0
            for u in g.neighbors(v):
                s += x[idx[u]]
            y[i] = s
        norm = math.sqrt(sum(z * z for z in y))
        if norm == 0.0:
            return 0.0
        x = [z / norm for z in y]
        num = 0.0
        den = sum(z * z for z in x)
        for v in vs:
            i = idx[v]
            s = 0.0
            for u in g.neighbors(v):
                s += x[idx[u]]
            num += x[i] * s
        lam = num / den if den else 0.0
    return float(lam)

def approx_clustering(g: UGraph, sample: int = 200, rng: Optional[random.Random] = None) -> float:
    vs = g.nodes()
    if not vs:
        return 0.0
    if len(vs) > sample:
        if rng is None:
            rng = random.Random(0)
        vs = rng.sample(vs, sample)
    coeffs: List[float] = []
    for v in vs:
        ns = list(g.neighbors(v))
        k = len(ns)
        if k < 2:
            coeffs.append(0.0)
            continue
        links = 0
        for i in range(k):
            a = ns[i]
            na = g.neighbors(a)
            for j in range(i + 1, k):
                b = ns[j]
                if b in na:
                    links += 1
        coeffs.append(2.0 * links / (k * (k - 1)))
    return sum(coeffs) / len(coeffs)

def bfs_distances(g: UGraph, sources: Iterable[int], max_radius: Optional[int] = None) -> Dict[int, int]:
    src = [s for s in sources if s in g.adj]
    if not src:
        return {}
    dist: Dict[int, int] = {}
    frontier = list(src)
    for s in src:
        dist[s] = 0
    head = 0
    while head < len(frontier):
        v = frontier[head]
        head += 1
        dv = dist[v]
        if max_radius is not None and dv >= max_radius:
            continue
        for u in g.neighbors(v):
            if u not in dist:
                dist[u] = dv + 1
                frontier.append(u)
    return dist

def bfs_ball_volumes(g: UGraph, root: int, r_max: int) -> List[int]:
    if root not in g.adj:
        return [0] * (r_max + 1)
    visited = {root}
    frontier = {root}
    volumes = [1]
    for _ in range(r_max):
        nxt = set()
        for v in frontier:
            for u in g.neighbors(v):
                if u not in visited:
                    visited.add(u)
                    nxt.add(u)
        frontier = nxt
        volumes.append(len(visited))
        if not frontier:
            volumes.extend([len(visited)] * (r_max - len(volumes) + 1))
            break
    return volumes[: r_max + 1]

def volume_dimension_proxy(g: UGraph, samples: int = 8, r_max: int = 4, rng: Optional[random.Random] = None) -> float:
    vs = g.nodes()
    if len(vs) < 2:
        return 0.0
    if rng is None:
        rng = random.Random(0)
    roots = vs if len(vs) <= samples else rng.sample(vs, samples)
    ds = []
    for r in roots:
        vols = bfs_ball_volumes(g, r, r_max)
        xs, ys = [], []
        for rad in range(1, len(vols)):
            if vols[rad] > 1:
                xs.append(math.log(rad))
                ys.append(math.log(vols[rad]))
        if len(xs) >= 2:
            mx = sum(xs) / len(xs)
            my = sum(ys) / len(ys)
            num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            den = sum((x - mx) ** 2 for x in xs)
            if den > 0:
                ds.append(num / den)
    return float(sum(ds) / len(ds)) if ds else 0.0


FEATURE_NAMES = [
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


@dataclass
class State:
    g: UGraph
    tokens: List[int]
    t: float
    next_node_id: int

    def clone(self) -> "State":
        return State(g=self.g.clone(), tokens=list(self.tokens), t=self.t, next_node_id=self.next_node_id)


def feature_row(state: State, rng: Optional[random.Random] = None) -> Dict[str, float]:
    g = state.g
    return {
        "tokens": float(len(state.tokens)),
        "nodes": float(g.num_nodes()),
        "components": float(count_components(g)),
        "beta1": float(beta1_cycle_rank(g)),
        "wedges": float(wedge_count(g)),
        "triangles": float(triangle_count(g)),
        "star3": float(star3_count(g)),
        "c4": float(four_cycle_count(g)),
        "spectral_radius": float(adjacency_spectral_radius(g)),
        "clustering": float(approx_clustering(g, rng=rng)),
        "dim_proxy": float(volume_dimension_proxy(g, rng=rng)),
    }

def feature_vector(state: State, rng: Optional[random.Random] = None) -> np.ndarray:
    row = feature_row(state, rng=rng)
    return np.array([row[k] for k in FEATURE_NAMES], dtype=float)


# ----------------------------
# Initialization and perturbations
# ----------------------------

def bootstrap(initial_cycle: int, initial_tokens: int, rng: random.Random) -> State:
    g = UGraph()
    initial_cycle = max(4, initial_cycle)
    for v in range(initial_cycle):
        g.add_edge(v, (v + 1) % initial_cycle)
    tokens = [rng.randrange(initial_cycle) for _ in range(max(1, initial_tokens))]
    return State(g=g, tokens=tokens, t=0.0, next_node_id=initial_cycle)

def choose_center_token(state: State, center_token_index: int) -> Tuple[int, int, int]:
    tidx = center_token_index % len(state.tokens)
    v = state.tokens[tidx]
    ns = sorted(state.g.neighbors(v))
    if not ns:
        raise ValueError("Center token sits on isolated node; bootstrap impossible.")
    u = ns[0]
    nu = sorted(w for w in state.g.neighbors(u) if w != v and not state.g.has_edge(v, w))
    if not nu:
        # fallback: use next neighbor on cycle-like graph
        nu = sorted(w for w in state.g.neighbors(u) if w != v)
    if not nu:
        raise ValueError("Could not construct local perturbation candidate.")
    w = nu[0]
    return v, u, w

def apply_local_swap_perturbation(state: State, center_token_index: int = 0) -> Dict[str, Any]:
    v, u, w = choose_center_token(state, center_token_index)
    if state.g.has_edge(v, u):
        state.g.remove_edge(v, u)
    state.g.add_edge(v, w)
    support = sorted({v, u, w})
    return {
        "type": "local_swap",
        "v": v,
        "u": u,
        "w": w,
        "support": support,
        "delta_core": {"tokens": 0, "nodes": 0, "components": 0, "beta1": 0},
    }

def apply_chord_perturbation(state: State, center_token_index: int = 0) -> Dict[str, Any]:
    v, u, w = choose_center_token(state, center_token_index)
    state.g.add_edge(v, w)
    support = sorted({v, u, w})
    return {
        "type": "add_chord",
        "v": v,
        "u": u,
        "w": w,
        "support": support,
        "delta_core": {"tokens": 0, "nodes": 0, "components": 0, "beta1": +1},
    }

def apply_perturbation(state: State, perturbation: str, center_token_index: int) -> Dict[str, Any]:
    if perturbation == "local_swap":
        return apply_local_swap_perturbation(state, center_token_index=center_token_index)
    if perturbation == "add_chord":
        return apply_chord_perturbation(state, center_token_index=center_token_index)
    raise ValueError(f"Unknown perturbation: {perturbation}")


# ----------------------------
# Shared-instruction local dynamics
# ----------------------------

@dataclass
class Params:
    r_seed: float
    r_token: float
    p_triad: float
    p_del: float
    p_swap: float
    strict_local: bool = True
    forbid_pruning_current_token_node: bool = True

def choose_by_rank(seq: Sequence[int], u: float) -> Optional[int]:
    if not seq:
        return None
    idx = min(int(u * len(seq)), len(seq) - 1)
    return seq[idx]

def relocate_tokens_from_dead_node(tokens: List[int], dead_node: int, destination: int) -> None:
    for i, tok in enumerate(tokens):
        if tok == dead_node:
            tokens[i] = destination

def apply_seed_instruction(state: State, host_token_index: int) -> Dict[str, Any]:
    if not state.tokens:
        return {"event": "noop"}
    tidx = host_token_index % len(state.tokens)
    host = state.tokens[tidx]
    x = state.next_node_id
    state.next_node_id += 1
    state.g.add_edge(x, host)
    return {"event": "seed", "token_index": tidx, "host": host, "new_node": x}

def apply_token_instruction(
    state: State,
    token_index: int,
    u_neighbor: float,
    u_rule: float,
    u_candidate: float,
    params: Params,
) -> Dict[str, Any]:
    if not state.tokens:
        return {"event": "noop"}

    tidx = token_index % len(state.tokens)
    v = state.tokens[tidx]
    neigh = sorted(state.g.neighbors(v))
    if not neigh:
        return {"event": "stuck", "token_index": tidx, "v_before": v}

    u = choose_by_rank(neigh, u_neighbor)
    assert u is not None
    deg_v_before = state.g.degree(v)
    deg_u_before = state.g.degree(u)

    # traverse first
    state.tokens[tidx] = u
    ctx: Dict[str, Any] = {
        "event": "move",
        "token_index": tidx,
        "v_before": v,
        "u_before": u,
        "deg_v_before": deg_v_before,
        "deg_u_before": deg_u_before,
    }

    total = params.p_triad + params.p_del + params.p_swap
    if total <= 0.0:
        return ctx

    roll = u_rule
    if roll < params.p_del:
        # strict-local admissibility: do not prune the occupied target node u
        # local relocation handles dead leaf at v if needed.
        if params.forbid_pruning_current_token_node and deg_u_before <= 1:
            return ctx
        state.g.remove_edge(v, u)
        if state.g.degree(v) == 0:
            relocate_tokens_from_dead_node(state.tokens, v, u)
            state.g.remove_node(v)
            ctx["pruned_v"] = v
        ctx["event"] = "delete"
        return ctx

    roll -= params.p_del
    if roll < params.p_triad:
        cands = sorted(w for w in state.g.neighbors(u) if w != v and not state.g.has_edge(v, w))
        w = choose_by_rank(cands, u_candidate)
        if w is None:
            return ctx
        state.g.add_edge(v, w)
        ctx.update({"event": "triad", "w_before": w, "deg_w_before": state.g.degree(w)})
        return ctx

    roll -= params.p_triad
    if roll < params.p_swap:
        cands = sorted(w for w in state.g.neighbors(u) if w != v and not state.g.has_edge(v, w))
        w = choose_by_rank(cands, u_candidate)
        if w is None:
            return ctx
        if params.forbid_pruning_current_token_node and deg_u_before <= 1:
            return ctx
        state.g.remove_edge(v, u)
        state.g.add_edge(v, w)
        if state.g.degree(u) == 0:
            # If u ever prunes due to a deg-1 case slipping through, relocate locally to v.
            relocate_tokens_from_dead_node(state.tokens, u, v)
            state.g.remove_node(u)
            ctx["pruned_u"] = u
        ctx.update({"event": "swap", "w_before": w, "deg_w_before": state.g.degree(w)})
        return ctx

    return ctx

def shared_step_pair(
    control: State,
    perturbed: State,
    rng: random.Random,
    params: Params,
) -> Dict[str, Any]:
    if len(control.tokens) != len(perturbed.tokens):
        raise RuntimeError("Perturbation lab assumes matched token counts across replicas.")
    K = len(control.tokens)
    total_rate = max(0.0, params.r_seed) + max(0.0, params.r_token) * K
    if total_rate <= 0.0:
        return {"event": "noop", "dt": 0.0}

    dt = rng.expovariate(total_rate)
    control.t += dt
    perturbed.t += dt

    x = rng.random() * total_rate
    if x < max(0.0, params.r_seed):
        tidx = rng.randrange(K)
        ctx_c = apply_seed_instruction(control, tidx)
        ctx_p = apply_seed_instruction(perturbed, tidx)
        return {"event": "seed", "dt": dt, "shared_token_index": tidx, "control": ctx_c, "perturbed": ctx_p}

    tidx = rng.randrange(K)
    u_neighbor = rng.random()
    u_rule = rng.random()
    u_candidate = rng.random()
    ctx_c = apply_token_instruction(control, tidx, u_neighbor, u_rule, u_candidate, params)
    ctx_p = apply_token_instruction(perturbed, tidx, u_neighbor, u_rule, u_candidate, params)
    return {
        "event": "token",
        "dt": dt,
        "shared_token_index": tidx,
        "u_neighbor": u_neighbor,
        "u_rule": u_rule,
        "u_candidate": u_candidate,
        "control": ctx_c,
        "perturbed": ctx_p,
    }


# ----------------------------
# Damage / causal metrics
# ----------------------------

def token_hamming(control: State, perturbed: State) -> int:
    return sum(1 for a, b in zip(control.tokens, perturbed.tokens) if a != b)

def edge_symmetric_difference(control: State, perturbed: State) -> Set[Tuple[int, int]]:
    return control.g.edge_set().symmetric_difference(perturbed.g.edge_set())

def node_symmetric_difference(control: State, perturbed: State) -> Set[int]:
    return set(control.g.nodes()).symmetric_difference(set(perturbed.g.nodes()))

def damaged_nodes(control: State, perturbed: State) -> Set[int]:
    nodes: Set[int] = set()
    for a, b in edge_symmetric_difference(control, perturbed):
        nodes.add(a); nodes.add(b)
    nodes.update(node_symmetric_difference(control, perturbed))
    for a, b in zip(control.tokens, perturbed.tokens):
        if a != b:
            nodes.add(a); nodes.add(b)
    return nodes

def radius_from_support(g: UGraph, support: Sequence[int], targets: Set[int]) -> Optional[int]:
    relevant = [v for v in targets if v in g.adj]
    if not support or not relevant:
        return None
    dist = bfs_distances(g, support)
    vals = [dist[v] for v in relevant if v in dist]
    return max(vals) if vals else None

def nearest_damage_distance(g: UGraph, support: Sequence[int], targets: Set[int]) -> Optional[int]:
    relevant = [v for v in targets if v in g.adj]
    if not support or not relevant:
        return None
    dist = bfs_distances(g, support)
    vals = [dist[v] for v in relevant if v in dist]
    return min(vals) if vals else None

def core_feature_difference(control: State, perturbed: State) -> Dict[str, float]:
    fc = feature_row(control)
    fp = feature_row(perturbed)
    return {k: fp[k] - fc[k] for k in FEATURE_NAMES}

def l1_feature_difference(control: State, perturbed: State, keys: Sequence[str]) -> float:
    fc = feature_row(control)
    fp = feature_row(perturbed)
    return float(sum(abs(fp[k] - fc[k]) for k in keys))

def damage_snapshot(
    control: State,
    perturbed: State,
    support: Sequence[int],
) -> Dict[str, Any]:
    d_edges = edge_symmetric_difference(control, perturbed)
    d_nodes = damaged_nodes(control, perturbed)
    r_ctrl = radius_from_support(control.g, support, d_nodes)
    r_pert = radius_from_support(perturbed.g, support, d_nodes)
    nearest_ctrl = nearest_damage_distance(control.g, support, d_nodes)
    nearest_pert = nearest_damage_distance(perturbed.g, support, d_nodes)
    diff = core_feature_difference(control, perturbed)
    return {
        "edge_diff_count": len(d_edges),
        "node_diff_count": len(node_symmetric_difference(control, perturbed)),
        "damaged_nodes_count": len(d_nodes),
        "token_hamming": token_hamming(control, perturbed),
        "radius_control": -1 if r_ctrl is None else int(r_ctrl),
        "radius_perturbed": -1 if r_pert is None else int(r_pert),
        "nearest_control": -1 if nearest_ctrl is None else int(nearest_ctrl),
        "nearest_perturbed": -1 if nearest_pert is None else int(nearest_pert),
        "core_l1": sum(abs(diff[k]) for k in ("tokens", "nodes", "components", "beta1")),
        "regime_l1": l1_feature_difference(control, perturbed, ["wedges", "triangles", "star3", "c4", "spectral_radius", "clustering", "dim_proxy"]),
        "delta_beta1": diff["beta1"],
        "delta_wedges": diff["wedges"],
        "delta_triangles": diff["triangles"],
        "delta_c4": diff["c4"],
        "delta_spectral_radius": diff["spectral_radius"],
        "delta_clustering": diff["clustering"],
        "delta_dim_proxy": diff["dim_proxy"],
    }


# ----------------------------
# Reporting helpers
# ----------------------------

def markdown_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    head = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows[1:])
    return "\n".join([head, sep, body])

def estimate_front_speed(log_rows: List[Dict[str, Any]], key_t: str, key_r: str) -> Dict[str, float]:
    pairs = [(float(r[key_t]), float(r[key_r])) for r in log_rows if float(r[key_t]) > 0.0 and float(r[key_r]) >= 0.0]
    if len(pairs) < 2:
        return {"max_ratio": float("nan"), "fit_slope": float("nan"), "fit_intercept": float("nan")}
    ratios = [rad / t for t, rad in pairs if t > 0]
    xs = np.array([p[0] for p in pairs], dtype=float)
    ys = np.array([p[1] for p in pairs], dtype=float)
    A = np.vstack([xs, np.ones(len(xs))]).T
    slope, intercept = np.linalg.lstsq(A, ys, rcond=None)[0]
    return {"max_ratio": float(max(ratios)), "fit_slope": float(slope), "fit_intercept": float(intercept)}

def first_hit_times(log_rows: List[Dict[str, Any]], key_r: str, key_t: str, r_max: int) -> Dict[int, Optional[float]]:
    out: Dict[int, Optional[float]] = {r: None for r in range(r_max + 1)}
    for row in log_rows:
        rad = int(row[key_r])
        if rad < 0:
            continue
        t = float(row[key_t])
        for r in range(rad + 1):
            if r in out and out[r] is None:
                out[r] = t
    return out

def first_hit_steps(log_rows: List[Dict[str, Any]], key_r: str, r_max: int) -> Dict[int, Optional[int]]:
    out: Dict[int, Optional[int]] = {r: None for r in range(r_max + 1)}
    for row in log_rows:
        rad = int(row[key_r])
        if rad < 0:
            continue
        step = int(row["step"])
        for r in range(rad + 1):
            if r in out and out[r] is None:
                out[r] = step
    return out

def event_consistency_counts(event_rows: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {
        "same_micro_event": 0,
        "different_micro_event": 0,
        "same_token_index": 0,
        "different_token_index": 0,
    }
    for row in event_rows:
        if row["control_event"] == row["perturbed_event"]:
            counts["same_micro_event"] += 1
        else:
            counts["different_micro_event"] += 1
        if row.get("control_token_after") == row.get("perturbed_token_after"):
            counts["same_token_index"] += 1
        else:
            counts["different_token_index"] += 1
    return counts

def make_summary_md(
    args: argparse.Namespace,
    log_rows: List[Dict[str, Any]],
    event_rows: List[Dict[str, Any]],
    perturbation_info: Dict[str, Any],
    report_json: Dict[str, Any],
    csv_log_path: str,
    csv_events_path: str,
) -> str:
    speed_ctrl = estimate_front_speed(log_rows, "t", "radius_control")
    speed_pert = estimate_front_speed(log_rows, "t", "radius_perturbed")
    hit_ctrl = first_hit_times(log_rows, "radius_control", "t", args.first_hit_rmax)
    hit_step_ctrl = first_hit_steps(log_rows, "radius_control", args.first_hit_rmax)
    consistency = event_consistency_counts(event_rows)

    rows = [["metric", "value"]]
    for k, v in report_json["headline_metrics"].items():
        rows.append([k, f"{v}"])
    headline_table = markdown_table(rows)

    event_rows_md = [["metric", "value"]]
    for k, v in consistency.items():
        event_rows_md.append([k, str(v)])
    event_table = markdown_table(event_rows_md)

    hit_rows = [["radius", "first_hit_time_control", "first_hit_step_control"]]
    for r in range(args.first_hit_rmax + 1):
        t = hit_ctrl[r]
        s = hit_step_ctrl[r]
        hit_rows.append([str(r), "NA" if t is None else f"{t:.6g}", "NA" if s is None else str(s)])
    hit_table = markdown_table(hit_rows)

    sections = [
        f"# Perturbasjonslab: {args.label}",
        "",
        "## Formål",
        "",
        "Dette v0.5-steget undersøker om den lokale relasjonsdynamikken faktisk gir en operasjonell causal cone.",
        "Metoden er å kjøre to kopla replikater med samme stokastiske instruksjonsstrøm og én lokal forskjell i bare den ene.",
        "",
        "## Viktig metodisk oppgradering",
        "",
        "Tidligere laboratorier brukte et globalt bro-kriterium (`avoid_disconnect`) for å hindre frakobling.",
        "Det kriteriet er ikke strengt lokalt. Denne perturbasjonslaben bruker derfor som standard en renere, lokal regelklasse.",
        "",
        "## Kjøringsparametre",
        "",
        f"- label: {args.label}",
        f"- steps: {args.steps}",
        f"- seed: {args.seed}",
        f"- initial_cycle: {args.initial_cycle}",
        f"- initial_tokens: {args.initial_tokens}",
        f"- r_seed: {args.r_seed}",
        f"- r_token: {args.r_token}",
        f"- p_triad: {args.p_triad}",
        f"- p_del: {args.p_del}",
        f"- p_swap: {args.p_swap}",
        f"- perturbation: {args.perturbation}",
        f"- center_token_index: {args.center_token_index}",
        f"- log_every: {args.log_every}",
        "",
        "## Startperturbasjon",
        "",
        "```json",
        json.dumps(perturbation_info, indent=2, sort_keys=True),
        "```",
        "",
        "## Hovedfunn fra denne kjøringen",
        "",
        headline_table,
        "",
        "## Tolking",
        "",
        "- `radius_control` og `radius_perturbed` måler hvor langt den observerbare forskjellsmengden strekker seg fra perturbasjonens støtte i de to grenene.",
        "- Hvis disse radiusene vokser langsomt og omtrent lineært i eventtid, har vi en praktisk kandidat til en emergent causal cone.",
        "- Hvis de derimot hopper momentant til store verdier uten lokal mekanisme, er lokaliteten brutt eller målingen dårlig definert.",
        "",
        "## Front-hastigheter",
        "",
        f"- control: max(r/t) = {speed_ctrl['max_ratio']:.6g}, lineær fit-slope = {speed_ctrl['fit_slope']:.6g}",
        f"- perturbed: max(r/t) = {speed_pert['max_ratio']:.6g}, lineær fit-slope = {speed_pert['fit_slope']:.6g}",
        "",
        "Disse tallene er ikke fundamentale konstanter. De er laboratorie-estimater for effektiv spredningshastighet i denne regelklassen og dette parameterregimet.",
        "",
        "## Første treff per radius (control-geometri)",
        "",
        hit_table,
        "",
        "## Event-konsistens mellom grenene",
        "",
        event_table,
        "",
        "## Hva som er etablert i dette steget",
        "",
        "1. Prosjektet har nå en eksplisitt perturbasjonsmetodikk basert på shared noise / kopla replikater.",
        "2. Lokalitet er renset metodisk ved å flytte analysen til en strengt lokal regelklasse.",
        "3. Causal-cone-spørsmålet er nå flyttet fra metafor til målbart objekt: radius som funksjon av eventtid og makrofeature-drift.",
        "",
        "## Begrensninger",
        "",
        "- Denne laben holder token-antallet fast. Dermed er shared-SSA-koblingen eksakt fordi den totale raten er den samme i begge grener.",
        "- Hvis token birth/death skal inn igjen, må vi bygge maksimal kobling eller uniformisering for å beholde metodisk kontroll.",
        "- `radius_control` er definert relativt til kontrollgrenenes øyeblikksgeometri; det er operasjonelt nyttig, men ikke eneste mulige definisjon.",
        "",
        "## Neste naturlige steg etter denne laben",
        "",
        "- Utvid koblingen til birth/death-regimer med uniformisering eller maksimal Poisson-kobling.",
        "- Legg til multikjøringsstatistikk og konfidensintervaller for front-hastighet.",
        "- Knytt causal-cone-estimatet til relativitetsdiskusjonen: når blir denne hastigheten universell over eksitasjoner og regimer?",
        "",
        "## Referanser",
        "",
        "- D. T. Gillespie, *Exact stochastic simulation of coupled chemical reactions* (1977).",
        "- P. Arrighi og G. Dowek, *Causal graph dynamics* (2013).",
        "- P. Arrighi og S. Martiel, *Quantum causal graph dynamics* (2017).",
        "- B. Martin, *Damage spreading and μ-sensitivity on cellular automata* (2007).",
        "- E. H. Lieb og D. W. Robinson, *The finite group velocity of quantum spin systems* (1972).",
        "",
        f"_Rå logg: `{csv_log_path}`_",
        "",
        f"_Rå eventdata: `{csv_events_path}`_",
        "",
    ]
    return "\n".join(sections)

def make_lay_summary_md(report_json: Dict[str, Any], args: argparse.Namespace) -> str:
    hm = report_json["headline_metrics"]
    return "\n".join([
        "# Hvor vi er i prosjektet – forklart uten fagjargon",
        "",
        "## Kort fortalt",
        "",
        "Vi prøver å se om et univers kan bygges fra bare tre ting:",
        "",
        "- noder",
        "- relasjoner mellom noder",
        "- små lokale hendelser som endrer relasjoner",
        "",
        "Tanken er at rom, tid, partikler og kanskje energi ikke er grunnleggende ting, men mønstre som dukker opp når denne grafen utvikler seg.",
        "",
        "## Hva vi hadde funnet før dette steget",
        "",
        "Tidligere fant vi at noen størrelser i modellen er helt presist bevarte i bestemte regelklasser.",
        "Det ga oss et første matematisk grep om hva som kan ligne på ladninger eller energi-lignende størrelser.",
        "",
        "## Hva dette nye steget gjør",
        "",
        "Nå har vi laget en test for kausalitet og 'signalhastighet'.",
        "Vi gjør det ved å starte med to nesten identiske universer.",
        "Det ene får én liten lokal endring. Deretter lar vi begge utvikle seg med akkurat samme tilfeldige 'støy'.",
        "",
        "Hvis forskjellen sprer seg sakte og lokalt, tyder det på at modellen har en slags innebygget lyskjegle:",
        "altså at påvirkning ikke kan hoppe vilkårlig langt med én gang.",
        "",
        "## Den viktigste metodiske oppdagelsen",
        "",
        "Vi oppdaget også noe viktig om selve modellen:",
        "En gammel sikkerhetsmekanisme vi brukte for å unngå at grafen falt fra hverandre, var faktisk ikke helt lokal.",
        "Det betyr at den ikke er god nok hvis målet er å undersøke om relativitet-lignende kausalitet kan oppstå.",
        "",
        "Derfor laget vi en ny, renere test der reglene virkelig er lokale.",
        "",
        "## Hva kjøringen viser",
        "",
        f"- Forskjellsmengden endte med {hm['final_edge_diff_count']} forskjellige kanter mellom de to grenene.",
        f"- Den målte skadefronten nådde radius {hm['final_radius_control']} i kontrollgeometrien.",
        f"- En enkel laboratoriemåling ga effektiv front-hastighet omtrent {hm['fit_speed_control']:.4g} radiusenheter per tidsenhet.",
        "",
        "Dette er ikke 'lyshastigheten til universet'.",
        "Det er bare første tegn på at modellen kan ha en øvre hastighet for hvordan forskjeller sprer seg.",
        "",
        "## Hva dette innebærer",
        "",
        "Hvis denne typen begrenset spredning holder seg når vi gjør modellen mer avansert, er det et sterkt tegn på at relativitet-lignende struktur kan komme ut av modellen i stedet for å legges inn på forhånd.",
        "",
        "## Hva som gjenstår",
        "",
        "- teste mange kjøringer, ikke bare representative eksempler",
        "- teste flere typer lokale forstyrrelser",
        "- bygge en mer avansert kobling når antallet action-bærere ikke lenger holdes fast",
        "- undersøke om den målte front-hastigheten blir en universell størrelse eller bare en regimedetalj",
        "",
        "## En enkel analogi",
        "",
        "Tenk deg to identiske snøhauger. Du trykker inn en liten bulk i den ene. Deretter blåser samme vind over begge.",
        "Hvis bulken bare påvirker området rundt seg og sprer seg gradvis, har systemet lokal kausalitet.",
        "Hvis hele haugen plutselig endrer seg overalt, er modellen ikke lokal nok.",
        "",
        "Denne laben er vår versjon av det eksperimentet.",
        "",
    ])


# ----------------------------
# Main
# ----------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Perturbation / causal-cone lab for the relational universe model.")
    p.add_argument("--label", type=str, default="v0_5_run")
    p.add_argument("--steps", type=int, default=20000)
    p.add_argument("--seed", type=int, default=101)
    p.add_argument("--initial-cycle", type=int, default=8)
    p.add_argument("--initial-tokens", type=int, default=4)
    p.add_argument("--r-seed", type=float, default=0.04)
    p.add_argument("--r-token", type=float, default=1.0)
    p.add_argument("--p-triad", type=float, default=0.0)
    p.add_argument("--p-del", type=float, default=0.0)
    p.add_argument("--p-swap", type=float, default=0.08)
    p.add_argument("--closed-topological", action="store_true", help="Convenience preset: seed+swap only.")
    p.add_argument("--open-topological", action="store_true", help="Convenience preset: seed+triad+delete+swap.")
    p.add_argument("--perturbation", type=str, default="local_swap", choices=["local_swap", "add_chord"])
    p.add_argument("--center-token-index", type=int, default=0)
    p.add_argument("--log-every", type=int, default=50)
    p.add_argument("--first-hit-rmax", type=int, default=8)
    p.add_argument("--out-log-csv", type=str, default="perturbation_log.csv")
    p.add_argument("--out-events-csv", type=str, default="perturbation_events.csv")
    p.add_argument("--out-summary-md", type=str, default="perturbation_summary.md")
    p.add_argument("--out-lay-md", type=str, default="perturbation_lay_summary.md")
    p.add_argument("--out-json", type=str, default="perturbation_report.json")
    return p

def apply_presets(args: argparse.Namespace) -> None:
    if args.closed_topological:
        args.p_triad = 0.0
        args.p_del = 0.0
        args.p_swap = max(args.p_swap, 0.08)
    if args.open_topological:
        args.p_triad = max(args.p_triad, 0.10)
        args.p_del = max(args.p_del, 0.06)
        args.p_swap = max(args.p_swap, 0.08)

def main() -> None:
    args = build_parser().parse_args()
    apply_presets(args)
    rng = random.Random(args.seed)

    base = bootstrap(args.initial_cycle, args.initial_tokens, rng)
    control = base.clone()
    perturbed = base.clone()

    perturbation_info = apply_perturbation(perturbed, args.perturbation, args.center_token_index)
    support = perturbation_info["support"]

    params = Params(
        r_seed=args.r_seed,
        r_token=args.r_token,
        p_triad=args.p_triad,
        p_del=args.p_del,
        p_swap=args.p_swap,
        strict_local=True,
        forbid_pruning_current_token_node=True,
    )

    log_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []

    first_snap = damage_snapshot(control, perturbed, support)
    log_rows.append({
        "step": 0,
        "t": 0.0,
        **first_snap,
    })

    max_radius_ctrl = max(-1, first_snap["radius_control"])
    max_radius_pert = max(-1, first_snap["radius_perturbed"])

    for step in range(1, args.steps + 1):
        shared = shared_step_pair(control, perturbed, rng, params)

        event_row = {
            "step": step,
            "t": control.t,
            "shared_event_family": shared["event"],
            "shared_token_index": shared.get("shared_token_index", ""),
            "control_event": shared.get("control", {}).get("event", ""),
            "perturbed_event": shared.get("perturbed", {}).get("event", ""),
            "control_token_after": control.tokens[shared["shared_token_index"]] if shared.get("event") == "token" and control.tokens else "",
            "perturbed_token_after": perturbed.tokens[shared["shared_token_index"]] if shared.get("event") == "token" and perturbed.tokens else "",
        }
        event_rows.append(event_row)

        if step % args.log_every == 0 or step == args.steps:
            snap = damage_snapshot(control, perturbed, support)
            max_radius_ctrl = max(max_radius_ctrl, snap["radius_control"])
            max_radius_pert = max(max_radius_pert, snap["radius_perturbed"])
            log_rows.append({
                "step": step,
                "t": control.t,
                **snap,
            })

    speed_ctrl = estimate_front_speed(log_rows, "t", "radius_control")
    speed_pert = estimate_front_speed(log_rows, "t", "radius_perturbed")
    final = log_rows[-1]

    report = {
        "label": args.label,
        "params": {
            "steps": args.steps,
            "seed": args.seed,
            "initial_cycle": args.initial_cycle,
            "initial_tokens": args.initial_tokens,
            "r_seed": args.r_seed,
            "r_token": args.r_token,
            "p_triad": args.p_triad,
            "p_del": args.p_del,
            "p_swap": args.p_swap,
            "perturbation": args.perturbation,
            "center_token_index": args.center_token_index,
            "log_every": args.log_every,
        },
        "perturbation": perturbation_info,
        "headline_metrics": {
            "final_time": round(float(final["t"]), 6),
            "final_edge_diff_count": int(final["edge_diff_count"]),
            "final_damaged_nodes_count": int(final["damaged_nodes_count"]),
            "final_token_hamming": int(final["token_hamming"]),
            "final_radius_control": int(final["radius_control"]),
            "final_radius_perturbed": int(final["radius_perturbed"]),
            "max_radius_control": int(max_radius_ctrl),
            "max_radius_perturbed": int(max_radius_pert),
            "final_core_l1": round(float(final["core_l1"]), 6),
            "final_regime_l1": round(float(final["regime_l1"]), 6),
            "final_delta_beta1": round(float(final["delta_beta1"]), 6),
            "fit_speed_control": round(float(speed_ctrl["fit_slope"]), 6) if math.isfinite(speed_ctrl["fit_slope"]) else None,
            "fit_speed_perturbed": round(float(speed_pert["fit_slope"]), 6) if math.isfinite(speed_pert["fit_slope"]) else None,
            "max_ratio_speed_control": round(float(speed_ctrl["max_ratio"]), 6) if math.isfinite(speed_ctrl["max_ratio"]) else None,
            "max_ratio_speed_perturbed": round(float(speed_pert["max_ratio"]), 6) if math.isfinite(speed_pert["max_ratio"]) else None,
        },
    }

    with open(args.out_log_csv, "w", newline="", encoding="utf-8") as f:
        if log_rows:
            writer = csv.DictWriter(f, fieldnames=list(log_rows[0].keys()))
            writer.writeheader()
            writer.writerows(log_rows)

    with open(args.out_events_csv, "w", newline="", encoding="utf-8") as f:
        if event_rows:
            writer = csv.DictWriter(f, fieldnames=list(event_rows[0].keys()))
            writer.writeheader()
            writer.writerows(event_rows)

    summary_md = make_summary_md(args, log_rows, event_rows, perturbation_info, report, args.out_log_csv, args.out_events_csv)
    with open(args.out_summary_md, "w", encoding="utf-8") as f:
        f.write(summary_md)

    lay_md = make_lay_summary_md(report, args)
    with open(args.out_lay_md, "w", encoding="utf-8") as f:
        f.write(lay_md)

    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, sort_keys=True)

    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
