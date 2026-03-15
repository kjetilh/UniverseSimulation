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
import os
import random
import statistics
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

try:
    import numpy as np
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"numpy is required: {exc}")

_TEMP_CACHE_ROOT = Path(tempfile.gettempdir()) / "relational_universe_cache"
_TEMP_CACHE_ROOT.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_TEMP_CACHE_ROOT / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(_TEMP_CACHE_ROOT / "xdg"))
Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
Path(os.environ["XDG_CACHE_HOME"]).mkdir(parents=True, exist_ok=True)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception:
    plt = None


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
    union_edges = control.g.edge_set().union(perturbed.g.edge_set())
    d_nodes = damaged_nodes(control, perturbed)
    r_ctrl = radius_from_support(control.g, support, d_nodes)
    r_pert = radius_from_support(perturbed.g, support, d_nodes)
    nearest_ctrl = nearest_damage_distance(control.g, support, d_nodes)
    nearest_pert = nearest_damage_distance(perturbed.g, support, d_nodes)
    diff = core_feature_difference(control, perturbed)
    return {
        "edge_diff_count": len(d_edges),
        "edge_jaccard_distance": 0.0 if not union_edges else len(d_edges) / len(union_edges),
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

def finite_or_none(x: float) -> Optional[float]:
    return None if not math.isfinite(x) else float(x)

def fmt_float(x: Optional[float], digits: int = 6) -> str:
    if x is None:
        return "NA"
    x_val = float(x)
    if not math.isfinite(x_val):
        return "NA"
    return f"{x_val:.{digits}g}"

def mean_std(values: Sequence[float]) -> Tuple[float, float]:
    vals = [float(v) for v in values]
    if not vals:
        return float("nan"), float("nan")
    if len(vals) == 1:
        return vals[0], 0.0
    return statistics.mean(vals), statistics.stdev(vals)

def parse_int_list(text: str) -> List[int]:
    return [int(chunk.strip()) for chunk in text.split(",") if chunk.strip()]

def parse_str_list(text: str) -> List[str]:
    return [chunk.strip() for chunk in text.split(",") if chunk.strip()]

def ensure_parent_dir(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)

def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)

def plot_mean_band(
    xs: Sequence[float],
    mean: Sequence[float],
    std: Sequence[float],
    title: str,
    xlabel: str,
    ylabel: str,
    out_path: str,
    label: str,
) -> Optional[str]:
    if plt is None or not xs:
        return None
    ensure_parent_dir(out_path)
    x_arr = np.array(xs, dtype=float)
    mean_arr = np.array(mean, dtype=float)
    std_arr = np.array(std, dtype=float)
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    ax.plot(x_arr, mean_arr, linewidth=2.0, label=label)
    ax.fill_between(x_arr, mean_arr - std_arr, mean_arr + std_arr, alpha=0.2)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    return out_path

def plot_comparison_bands(
    series_by_label: Dict[str, Dict[str, List[float]]],
    title: str,
    xlabel: str,
    ylabel: str,
    out_path: str,
) -> Optional[str]:
    if plt is None or not series_by_label:
        return None
    ensure_parent_dir(out_path)
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    for label, payload in sorted(series_by_label.items()):
        xs = np.array(payload["x"], dtype=float)
        mean = np.array(payload["mean"], dtype=float)
        std = np.array(payload["std"], dtype=float)
        ax.plot(xs, mean, linewidth=2.0, label=label)
        ax.fill_between(xs, mean - std, mean + std, alpha=0.18)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    return out_path

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
        f"- regime: {getattr(args, 'regime', 'custom')}",
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
        "- `edge_jaccard_distance` måler hvor ulik kantmengden er relativt til samlet støtte, ikke bare absolutte tellinger.",
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
        f"_Rå logg: `{csv_log_path}`_",
        "",
        f"_Rå eventdata: `{csv_events_path}`_",
        "",
    ]
    return "\n".join(sections)

def make_lay_summary_md(report_json: Dict[str, Any], args: argparse.Namespace) -> str:
    hm = report_json["headline_metrics"]
    fit_speed = hm.get("fit_speed_control")
    fit_speed_txt = "NA" if fit_speed is None else f"{float(fit_speed):.4g}"
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
        "## Hva dette nye steget gjør",
        "",
        "Nå har vi laget en test for kausalitet og signalhastighet.",
        "Vi gjør det ved å starte med to nesten identiske universer, gi bare det ene en liten lokal endring, og så la begge få akkurat samme støy videre.",
        "",
        "## Hva kjøringen viser",
        "",
        f"- Forskjellsmengden endte med {hm['final_edge_diff_count']} forskjellige kanter mellom de to grenene.",
        f"- Den målte skadefronten nådde radius {hm['final_radius_control']} i kontrollgeometrien.",
        f"- En enkel laboratoriemåling ga effektiv front-hastighet omtrent {fit_speed_txt} radiusenheter per tidsenhet.",
        "",
        "Dette er ikke lyshastigheten til universet. Det er bare et første tegn på at modellen kan ha en øvre hastighet for hvordan forskjeller sprer seg.",
        "",
        "## Hva som gjenstår",
        "",
        "- teste mange kjøringer, ikke bare representative eksempler",
        "- teste flere typer lokale forstyrrelser",
        "- bygge en mer avansert kobling når antallet action-bærere ikke lenger holdes fast",
        "- undersøke om den målte front-hastigheten blir en universell størrelse eller bare en regimedetalj",
        "",
    ])

REGIME_PRESETS: Dict[str, Dict[str, float]] = {
    "closed_topological": {"p_triad": 0.0, "p_del": 0.0, "p_swap": 0.08},
    "open_topological": {"p_triad": 0.10, "p_del": 0.06, "p_swap": 0.08},
    "aggressive_triad_delete": {"p_triad": 0.24, "p_del": 0.14, "p_swap": 0.12},
}

BATCH_METRIC_SPECS: List[Tuple[str, str]] = [
    ("final_radius_control", "final_radius_control"),
    ("max_radius_control", "max_radius_control"),
    ("fit_speed_control", "fit_speed_control"),
    ("final_core_l1", "final_core_l1"),
    ("final_regime_l1", "final_regime_l1"),
    ("final_delta_beta1", "final_delta_beta1"),
    ("final_edge_jaccard_distance", "final_edge_jaccard_distance"),
]

COMPARISON_PERTURBATIONS = ("local_swap", "add_chord")

def copy_namespace(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(**vars(args))

def apply_presets(args: argparse.Namespace) -> None:
    if args.closed_topological:
        args.p_triad = 0.0
        args.p_del = 0.0
        args.p_swap = max(args.p_swap, 0.08)
    if args.open_topological:
        args.p_triad = max(args.p_triad, 0.10)
        args.p_del = max(args.p_del, 0.06)
        args.p_swap = max(args.p_swap, 0.08)

def apply_named_regime(args: argparse.Namespace, regime: str) -> None:
    args.closed_topological = False
    args.open_topological = False
    if regime == "custom":
        apply_presets(args)
        return
    if regime not in REGIME_PRESETS:
        raise ValueError(f"Unknown regime preset: {regime}")
    params = REGIME_PRESETS[regime]
    args.p_triad = float(params["p_triad"])
    args.p_del = float(params["p_del"])
    args.p_swap = float(params["p_swap"])

def infer_regime_name(args: argparse.Namespace) -> str:
    for name, preset in REGIME_PRESETS.items():
        if (
            math.isclose(args.p_triad, preset["p_triad"], rel_tol=0.0, abs_tol=1e-12)
            and math.isclose(args.p_del, preset["p_del"], rel_tol=0.0, abs_tol=1e-12)
            and math.isclose(args.p_swap, preset["p_swap"], rel_tol=0.0, abs_tol=1e-12)
        ):
            return name
    if getattr(args, "closed_topological", False):
        return "closed_topological"
    if getattr(args, "open_topological", False):
        return "open_topological"
    return "custom"

def run_single_experiment(args: argparse.Namespace) -> Dict[str, Any]:
    run_args = copy_namespace(args)
    apply_presets(run_args)
    run_args.regime = getattr(run_args, "regime", infer_regime_name(run_args))

    rng = random.Random(run_args.seed)
    base = bootstrap(run_args.initial_cycle, run_args.initial_tokens, rng)
    control = base.clone()
    perturbed = base.clone()

    perturbation_info = apply_perturbation(perturbed, run_args.perturbation, run_args.center_token_index)
    support = perturbation_info["support"]

    params = Params(
        r_seed=run_args.r_seed,
        r_token=run_args.r_token,
        p_triad=run_args.p_triad,
        p_del=run_args.p_del,
        p_swap=run_args.p_swap,
        strict_local=True,
        forbid_pruning_current_token_node=True,
    )

    log_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []

    first_snap = damage_snapshot(control, perturbed, support)
    max_radius_ctrl = max(-1, first_snap["radius_control"])
    max_radius_pert = max(-1, first_snap["radius_perturbed"])
    first_snap["front_envelope_control"] = max_radius_ctrl
    first_snap["front_envelope_perturbed"] = max_radius_pert
    log_rows.append({"step": 0, "t": 0.0, **first_snap})

    for step in range(1, run_args.steps + 1):
        shared = shared_step_pair(control, perturbed, rng, params)
        event_rows.append({
            "step": step,
            "t": control.t,
            "shared_event_family": shared["event"],
            "shared_token_index": shared.get("shared_token_index", ""),
            "control_event": shared.get("control", {}).get("event", ""),
            "perturbed_event": shared.get("perturbed", {}).get("event", ""),
            "control_token_after": control.tokens[shared["shared_token_index"]] if shared.get("event") == "token" and control.tokens else "",
            "perturbed_token_after": perturbed.tokens[shared["shared_token_index"]] if shared.get("event") == "token" and perturbed.tokens else "",
        })

        if step % run_args.log_every == 0 or step == run_args.steps:
            snap = damage_snapshot(control, perturbed, support)
            max_radius_ctrl = max(max_radius_ctrl, snap["radius_control"])
            max_radius_pert = max(max_radius_pert, snap["radius_perturbed"])
            snap["front_envelope_control"] = max_radius_ctrl
            snap["front_envelope_perturbed"] = max_radius_pert
            log_rows.append({"step": step, "t": control.t, **snap})

    speed_ctrl = estimate_front_speed(log_rows, "t", "radius_control")
    speed_pert = estimate_front_speed(log_rows, "t", "radius_perturbed")
    final = log_rows[-1]

    report = {
        "label": run_args.label,
        "params": {
            "regime": run_args.regime,
            "steps": run_args.steps,
            "seed": run_args.seed,
            "initial_cycle": run_args.initial_cycle,
            "initial_tokens": run_args.initial_tokens,
            "r_seed": run_args.r_seed,
            "r_token": run_args.r_token,
            "p_triad": run_args.p_triad,
            "p_del": run_args.p_del,
            "p_swap": run_args.p_swap,
            "perturbation": run_args.perturbation,
            "center_token_index": run_args.center_token_index,
            "log_every": run_args.log_every,
        },
        "perturbation": perturbation_info,
        "headline_metrics": {
            "final_time": round(float(final["t"]), 6),
            "final_edge_diff_count": int(final["edge_diff_count"]),
            "final_edge_jaccard_distance": round(float(final["edge_jaccard_distance"]), 6),
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
    return {
        "args": run_args,
        "report": report,
        "log_rows": log_rows,
        "event_rows": event_rows,
        "perturbation_info": perturbation_info,
    }

def write_single_outputs(result: Dict[str, Any], args: argparse.Namespace) -> None:
    ensure_parent_dir(args.out_log_csv)
    with open(args.out_log_csv, "w", newline="", encoding="utf-8") as f:
        if result["log_rows"]:
            writer = csv.DictWriter(f, fieldnames=list(result["log_rows"][0].keys()))
            writer.writeheader()
            writer.writerows(result["log_rows"])

    ensure_parent_dir(args.out_events_csv)
    with open(args.out_events_csv, "w", newline="", encoding="utf-8") as f:
        if result["event_rows"]:
            writer = csv.DictWriter(f, fieldnames=list(result["event_rows"][0].keys()))
            writer.writeheader()
            writer.writerows(result["event_rows"])

    summary_md = make_summary_md(
        args,
        result["log_rows"],
        result["event_rows"],
        result["perturbation_info"],
        result["report"],
        args.out_log_csv,
        args.out_events_csv,
    )
    ensure_parent_dir(args.out_summary_md)
    with open(args.out_summary_md, "w", encoding="utf-8") as f:
        f.write(summary_md)

    lay_md = make_lay_summary_md(result["report"], args)
    ensure_parent_dir(args.out_lay_md)
    with open(args.out_lay_md, "w", encoding="utf-8") as f:
        f.write(lay_md)

    ensure_parent_dir(args.out_json)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(result["report"], f, indent=2, sort_keys=True)

def long_log_rows_for_run(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    meta = {
        "label": result["report"]["label"],
        "regime": result["report"]["params"]["regime"],
        "perturbation": result["report"]["params"]["perturbation"],
        "seed": result["report"]["params"]["seed"],
    }
    return [{**meta, **row} for row in result["log_rows"]]

def summary_row_for_run(result: Dict[str, Any]) -> Dict[str, Any]:
    hm = result["report"]["headline_metrics"]
    return {
        "label": result["report"]["label"],
        "regime": result["report"]["params"]["regime"],
        "perturbation": result["report"]["params"]["perturbation"],
        "seed": result["report"]["params"]["seed"],
        **hm,
    }

def first_hit_rows_for_run(result: Dict[str, Any], r_max: int) -> List[Dict[str, Any]]:
    hit_times = first_hit_times(result["log_rows"], "radius_control", "t", r_max)
    hit_steps = first_hit_steps(result["log_rows"], "radius_control", r_max)
    meta = {
        "label": result["report"]["label"],
        "regime": result["report"]["params"]["regime"],
        "perturbation": result["report"]["params"]["perturbation"],
        "seed": result["report"]["params"]["seed"],
    }
    rows: List[Dict[str, Any]] = []
    for radius in range(r_max + 1):
        rows.append({
            **meta,
            "radius": radius,
            "hit_observed": 0 if hit_times[radius] is None else 1,
            "hit_time": "" if hit_times[radius] is None else round(float(hit_times[radius]), 6),
            "hit_step": "" if hit_steps[radius] is None else int(hit_steps[radius]),
        })
    return rows

def aggregate_time_series(
    results: Sequence[Dict[str, Any]],
    y_key: str,
    grid_points: int,
) -> Optional[Dict[str, List[float]]]:
    if not results:
        return None
    final_times = [float(res["log_rows"][-1]["t"]) for res in results if res["log_rows"]]
    if not final_times:
        return None
    t_max = min(final_times)
    if t_max <= 0.0:
        return None
    grid = np.linspace(0.0, t_max, grid_points)
    stacked: List[np.ndarray] = []
    for res in results:
        xs = np.array([float(row["t"]) for row in res["log_rows"]], dtype=float)
        ys = np.array([float(row[y_key]) for row in res["log_rows"]], dtype=float)
        stacked.append(np.interp(grid, xs, ys))
    arr = np.vstack(stacked)
    return {
        "x": grid.tolist(),
        "mean": arr.mean(axis=0).tolist(),
        "std": arr.std(axis=0, ddof=0).tolist(),
    }

def aggregate_step_series(
    results: Sequence[Dict[str, Any]],
    y_key: str,
) -> Optional[Dict[str, List[float]]]:
    if not results:
        return None
    common_steps: Optional[Set[int]] = None
    run_maps: List[Dict[int, float]] = []
    for res in results:
        mapping = {int(row["step"]): float(row[y_key]) for row in res["log_rows"]}
        run_maps.append(mapping)
        step_keys = set(mapping)
        common_steps = step_keys if common_steps is None else common_steps.intersection(step_keys)
    if not common_steps:
        return None
    steps = sorted(common_steps)
    arr = np.vstack([[mapping[step] for step in steps] for mapping in run_maps])
    return {
        "x": [float(step) for step in steps],
        "mean": arr.mean(axis=0).tolist(),
        "std": arr.std(axis=0, ddof=0).tolist(),
    }

def aggregate_summary_rows(summary_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for row in summary_rows:
        groups[(str(row["regime"]), str(row["perturbation"]))].append(row)
    aggregated: List[Dict[str, Any]] = []
    for (regime, perturbation), rows in sorted(groups.items()):
        agg_row: Dict[str, Any] = {
            "regime": regime,
            "perturbation": perturbation,
            "num_runs": len(rows),
        }
        for src_key, dst_base in BATCH_METRIC_SPECS:
            values = [float(row[src_key]) for row in rows if row[src_key] is not None]
            mean_v, std_v = mean_std(values)
            agg_row[f"mean_{dst_base}"] = finite_or_none(mean_v)
            agg_row[f"std_{dst_base}"] = finite_or_none(std_v)
        aggregated.append(agg_row)
    return aggregated

def aggregate_first_hit_rows(first_hit_rows: Sequence[Dict[str, Any]], r_max: int) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[str, str, int], List[Dict[str, Any]]] = defaultdict(list)
    for row in first_hit_rows:
        grouped[(str(row["regime"]), str(row["perturbation"]), int(row["radius"]))].append(row)
    out: List[Dict[str, Any]] = []
    for regime, perturbation in sorted({(r, p) for r, p, _ in grouped}):
        for radius in range(r_max + 1):
            rows = grouped.get((regime, perturbation, radius), [])
            observed_times = [float(r["hit_time"]) for r in rows if r["hit_observed"]]
            observed_steps = [float(r["hit_step"]) for r in rows if r["hit_observed"]]
            mean_time, std_time = mean_std(observed_times) if observed_times else (float("nan"), float("nan"))
            mean_step, std_step = mean_std(observed_steps) if observed_steps else (float("nan"), float("nan"))
            hit_fraction = 0.0 if not rows else sum(int(r["hit_observed"]) for r in rows) / len(rows)
            out.append({
                "regime": regime,
                "perturbation": perturbation,
                "radius": radius,
                "hit_fraction": round(hit_fraction, 6),
                "mean_hit_time": finite_or_none(mean_time),
                "std_hit_time": finite_or_none(std_time),
                "mean_hit_step": finite_or_none(mean_step),
                "std_hit_step": finite_or_none(std_step),
            })
    return out

def perturbation_comparison_rows(aggregate_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    lookup = {(row["regime"], row["perturbation"]): row for row in aggregate_rows}
    out: List[Dict[str, Any]] = []
    for regime in sorted({str(row["regime"]) for row in aggregate_rows}):
        key_swap = (regime, "local_swap")
        key_chord = (regime, "add_chord")
        if key_swap not in lookup or key_chord not in lookup:
            continue
        swap = lookup[key_swap]
        chord = lookup[key_chord]
        out.append({
            "regime": regime,
            "delta_mean_final_radius_control": finite_or_none(float(chord["mean_final_radius_control"]) - float(swap["mean_final_radius_control"])),
            "delta_mean_fit_speed_control": finite_or_none(float(chord["mean_fit_speed_control"]) - float(swap["mean_fit_speed_control"])),
            "delta_mean_final_regime_l1": finite_or_none(float(chord["mean_final_regime_l1"]) - float(swap["mean_final_regime_l1"])),
            "delta_mean_final_delta_beta1": finite_or_none(float(chord["mean_final_delta_beta1"]) - float(swap["mean_final_delta_beta1"])),
        })
    return out

def interpret_spread_pattern(aggregate_row: Dict[str, Any]) -> Tuple[str, str]:
    speed = float(aggregate_row["mean_fit_speed_control"]) if aggregate_row["mean_fit_speed_control"] is not None else 0.0
    max_radius = float(aggregate_row["mean_max_radius_control"]) if aggregate_row["mean_max_radius_control"] is not None else 0.0
    final_radius = float(aggregate_row["mean_final_radius_control"]) if aggregate_row["mean_final_radius_control"] is not None else 0.0
    regime_l1 = float(aggregate_row["mean_final_regime_l1"]) if aggregate_row["mean_final_regime_l1"] is not None else 0.0
    jaccard = float(aggregate_row["mean_final_edge_jaccard_distance"]) if aggregate_row["mean_final_edge_jaccard_distance"] is not None else 0.0
    if max_radius >= 4.0 and speed >= 0.18 and final_radius >= 3.0:
        return "ballistisk", "fronten flytter seg over flere radiuslag med vedvarende og omtrent lineær spredning."
    if max_radius <= 2.0 or (speed < 0.08 and regime_l1 >= 1.0 and jaccard >= 0.1):
        return "lokal scrambling", "forskjellen blir mest liggende som lokal omorganisering og diffus makrodrift."
    return "blandet", "dataene viser både lokal omrøring og en gradvis utadgående skadefront."

def interpret_batch_questions(
    aggregate_rows: Sequence[Dict[str, Any]],
    first_hit_agg_rows: Sequence[Dict[str, Any]],
) -> Dict[str, str]:
    lookup_first_hits: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for row in first_hit_agg_rows:
        lookup_first_hits[(str(row["regime"]), str(row["perturbation"]))].append(row)

    cone_lines: List[str] = []
    speeds: List[float] = []
    for row in aggregate_rows:
        key = (str(row["regime"]), str(row["perturbation"]))
        hit_rows = sorted(lookup_first_hits.get(key, []), key=lambda r: int(r["radius"]))
        monotone = True
        last = -float("inf")
        for hit in hit_rows:
            t = hit["mean_hit_time"]
            if t is None:
                continue
            val = float(t)
            if val + 1e-9 < last:
                monotone = False
                break
            last = val
        speed = row["mean_fit_speed_control"]
        if speed is not None:
            speeds.append(float(speed))
        if monotone and row["mean_max_radius_control"] is not None and float(row["mean_max_radius_control"]) >= 2.0:
            cone_lines.append(f"{row['regime']}/{row['perturbation']} har monotone first-hit-kurver og endelig frontfart.")

    bounded_cone = (
        "Ja, tentativt. " + " ".join(cone_lines[:3])
        if cone_lines
        else "Ikke robust ennå. Batchen viser ikke en stabil kombinasjon av monotone first-hit-kurver og vedvarende radiusvekst."
    )

    positive_speeds = [s for s in speeds if s > 0.0]
    if len(positive_speeds) >= 2:
        s_min = min(positive_speeds)
        s_max = max(positive_speeds)
        spread = s_max / s_min
        if spread >= 1.5:
            speed_variation = f"Ja. Effektiv frontfart varierer tydelig mellom gruppene; max/min-forholdet er omtrent {spread:.3g}."
        else:
            speed_variation = f"Ikke dramatisk i denne batchen. Effektiv frontfart ligger innenfor et max/min-forhold på omtrent {spread:.3g}."
        mean_speed = statistics.mean(positive_speeds)
        std_speed = statistics.stdev(positive_speeds) if len(positive_speeds) > 1 else 0.0
        cv = 0.0 if mean_speed == 0 else std_speed / abs(mean_speed)
        universality = (
            "Dataene peker svakt mot en mer universell effektiv hastighet, men dette er foreløpig bare deskriptivt."
            if cv <= 0.15
            else "Dataene peker mot en ikke-universell effektiv hastighet; regimer og perturbasjonstype flytter frontfarten merkbart."
        )
    elif len(speeds) >= 2:
        speed_variation = "Effektiv frontfart er svært liten eller skifter tegn mellom gruppene, så max/min-sammenlikning er ikke informativ i denne batchen."
        universality = "Dataene peker ikke mot noen robust universell hastighet i denne batchen."
    else:
        speed_variation = "For få grupper til å si noe meningsfullt om variasjon i frontfart."
        universality = "For lite datagrunnlag til å vurdere universalitet."

    return {
        "bounded_cone": bounded_cone,
        "speed_variation": speed_variation,
        "universality": universality,
    }

def build_batch_markdown(
    args: argparse.Namespace,
    summary_rows: Sequence[Dict[str, Any]],
    aggregate_rows: Sequence[Dict[str, Any]],
    first_hit_agg_rows: Sequence[Dict[str, Any]],
    plot_paths: Sequence[str],
) -> str:
    question_answers = interpret_batch_questions(aggregate_rows, first_hit_agg_rows)

    summary_table = [["regime", "perturbation", "seed", "final_radius", "max_radius", "fit_speed", "final_regime_L1", "delta_beta1", "edge_jaccard"]]
    for row in summary_rows:
        summary_table.append([
            str(row["regime"]),
            str(row["perturbation"]),
            str(row["seed"]),
            str(row["final_radius_control"]),
            str(row["max_radius_control"]),
            fmt_float(row["fit_speed_control"]),
            fmt_float(row["final_regime_l1"]),
            fmt_float(row["final_delta_beta1"]),
            fmt_float(row["final_edge_jaccard_distance"]),
        ])

    aggregate_table = [["regime", "perturbation", "n", "mean final_radius", "std final_radius", "mean max_radius", "mean fit_speed", "mean regime_L1", "mean delta_beta1", "mean edge_jaccard"]]
    for row in aggregate_rows:
        aggregate_table.append([
            str(row["regime"]),
            str(row["perturbation"]),
            str(row["num_runs"]),
            fmt_float(row["mean_final_radius_control"]),
            fmt_float(row["std_final_radius_control"]),
            fmt_float(row["mean_max_radius_control"]),
            fmt_float(row["mean_fit_speed_control"]),
            fmt_float(row["mean_final_regime_l1"]),
            fmt_float(row["mean_final_delta_beta1"]),
            fmt_float(row["mean_final_edge_jaccard_distance"]),
        ])

    first_hit_table = [["regime", "perturbation", "radius", "hit_fraction", "mean_hit_time", "mean_hit_step"]]
    for row in first_hit_agg_rows:
        first_hit_table.append([
            str(row["regime"]),
            str(row["perturbation"]),
            str(row["radius"]),
            fmt_float(row["hit_fraction"]),
            fmt_float(row["mean_hit_time"]),
            fmt_float(row["mean_hit_step"]),
        ])

    comparison_rows = perturbation_comparison_rows(aggregate_rows)
    comparison_table = [["regime", "delta radius (chord-swap)", "delta fit_speed", "delta regime_L1", "delta delta_beta1"]]
    for row in comparison_rows:
        comparison_table.append([
            str(row["regime"]),
            fmt_float(row["delta_mean_final_radius_control"]),
            fmt_float(row["delta_mean_fit_speed_control"]),
            fmt_float(row["delta_mean_final_regime_l1"]),
            fmt_float(row["delta_mean_final_delta_beta1"]),
        ])

    interpretations = [
        f"- `{row['regime']}` / `{row['perturbation']}`: `{interpret_spread_pattern(row)[0]}` fordi {interpret_spread_pattern(row)[1]}"
        for row in aggregate_rows
    ]
    plot_lines = [f"- `{path}`" for path in plot_paths] if plot_paths else ["- Ingen plott ble skrevet."]

    return "\n".join([
        f"# Batch-rapport: {args.label}",
        "",
        "## Konfigurasjon",
        "",
        f"- mode: {args.mode}",
        f"- steps: {args.steps}",
        f"- log_every: {args.log_every}",
        f"- seeds: {args.seeds or f'{args.seed},{args.seed + 1},{args.seed + 2}'}",
        f"- regimes: {args.regimes or 'closed_topological,open_topological,aggressive_triad_delete'}",
        f"- perturbations: {args.perturbations or 'local_swap,add_chord'}",
        "",
        "## Deskriptiv statistikk",
        "",
        "Denne delen er ren observasjonsoppsummering. Den er ikke teoretisk tolkning.",
        "",
        markdown_table(aggregate_table),
        "",
        "## Per-run oversikt",
        "",
        markdown_table(summary_table),
        "",
        "## Første-treff-kurver per radius",
        "",
        markdown_table(first_hit_table),
        "",
        "## Sammenlikning mellom `local_swap` og `add_chord`",
        "",
        markdown_table(comparison_table) if len(comparison_table) > 1 else "Batchen inneholdt ikke begge perturbasjonstyper i samme regime.",
        "",
        "## Kort batchtolking",
        "",
        *interpretations,
        "",
        "## Svar på forskningsspørsmålene",
        "",
        f"- Robust tegn på begrenset causal cone: {question_answers['bounded_cone']}",
        f"- Varierer front-hastigheten sterkt mellom regimer: {question_answers['speed_variation']}",
        f"- Universell eller ikke-universell effektiv hastighet: {question_answers['universality']}",
        "",
        "## Plott",
        "",
        *plot_lines,
        "",
        "## Skille mellom deskriptiv statistikk og teori",
        "",
        "Tallene over er deskriptive. Tolkingene om causal cone og effektiv hastighet er heuristiske og må testes videre i større batcher og senere i birth/death-regimer med strengere kobling.",
        "",
    ])

def generate_group_plots(
    grouped_results: Dict[Tuple[str, str], List[Dict[str, Any]]],
    plots_dir: str,
    plot_points: int,
) -> List[str]:
    plot_paths: List[str] = []
    if plt is None:
        return plot_paths
    ensure_dir(plots_dir)
    time_metrics = [
        ("radius_control", "Radius control vs tid", "tid", "radius_control", "radius_time"),
        ("edge_diff_count", "Edge diff count vs tid", "tid", "edge_diff_count", "edge_diff_time"),
        ("regime_l1", "Regime L1 vs tid", "tid", "regime_L1", "regime_l1_time"),
    ]
    for (regime, perturbation), results in sorted(grouped_results.items()):
        slug = f"{regime}__{perturbation}"
        for y_key, title, xlabel, ylabel, suffix in time_metrics:
            payload = aggregate_time_series(results, y_key, plot_points)
            if payload is None:
                continue
            out_path = str(Path(plots_dir) / f"{slug}_{suffix}.png")
            created = plot_mean_band(
                payload["x"],
                payload["mean"],
                payload["std"],
                title=f"{title} [{regime} / {perturbation}]",
                xlabel=xlabel,
                ylabel=ylabel,
                out_path=out_path,
                label=f"{regime} / {perturbation}",
            )
            if created is not None:
                plot_paths.append(created)

        step_payload = aggregate_step_series(results, "radius_control")
        if step_payload is not None:
            out_path = str(Path(plots_dir) / f"{slug}_radius_step.png")
            created = plot_mean_band(
                step_payload["x"],
                step_payload["mean"],
                step_payload["std"],
                title=f"Radius control vs steg [{regime} / {perturbation}]",
                xlabel="steg",
                ylabel="radius_control",
                out_path=out_path,
                label=f"{regime} / {perturbation}",
            )
            if created is not None:
                plot_paths.append(created)

    by_regime: Dict[str, Dict[str, Dict[str, List[float]]]] = defaultdict(dict)
    for (regime, perturbation), results in sorted(grouped_results.items()):
        payload = aggregate_time_series(results, "radius_control", plot_points)
        if payload is not None:
            by_regime[regime][perturbation] = payload
    for regime, payload in sorted(by_regime.items()):
        if not all(name in payload for name in COMPARISON_PERTURBATIONS):
            continue
        out_path = str(Path(plots_dir) / f"{regime}_local_swap_vs_add_chord_radius_time.png")
        created = plot_comparison_bands(
            {name: payload[name] for name in COMPARISON_PERTURBATIONS},
            title=f"local_swap vs add_chord [{regime}]",
            xlabel="tid",
            ylabel="radius_control",
            out_path=out_path,
        )
        if created is not None:
            plot_paths.append(created)
    return plot_paths

def load_batch_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def resolve_batch_inputs(args: argparse.Namespace) -> Tuple[List[int], List[str], List[str]]:
    config: Dict[str, Any] = {}
    if args.batch_config_json:
        config = load_batch_config(args.batch_config_json)
        for key, value in config.items():
            if key in {"seeds", "regimes", "perturbations"}:
                continue
            if hasattr(args, key):
                setattr(args, key, value)

    seeds = parse_int_list(args.seeds) if args.seeds else [int(x) for x in config.get("seeds", [args.seed, args.seed + 1, args.seed + 2])]
    regimes = parse_str_list(args.regimes) if args.regimes else [str(x) for x in config.get("regimes", ["closed_topological", "open_topological", "aggressive_triad_delete"])]
    perturbations = parse_str_list(args.perturbations) if args.perturbations else [str(x) for x in config.get("perturbations", ["local_swap", "add_chord"])]

    invalid_regimes = [name for name in regimes if name not in REGIME_PRESETS and name != "custom"]
    if invalid_regimes:
        raise ValueError(f"Unknown regimes: {', '.join(invalid_regimes)}")
    invalid_perturbations = [name for name in perturbations if name not in {"local_swap", "add_chord"}]
    if invalid_perturbations:
        raise ValueError(f"Unknown perturbations: {', '.join(invalid_perturbations)}")
    return seeds, regimes, perturbations

def run_batch_experiments(args: argparse.Namespace) -> Dict[str, Any]:
    seeds, regimes, perturbations = resolve_batch_inputs(args)
    grouped_results: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    summary_rows: List[Dict[str, Any]] = []
    long_log_rows: List[Dict[str, Any]] = []
    first_hit_rows: List[Dict[str, Any]] = []

    for regime in regimes:
        for perturbation in perturbations:
            for seed in seeds:
                run_args = copy_namespace(args)
                run_args.seed = seed
                run_args.perturbation = perturbation
                run_args.regime = regime
                run_args.label = f"{args.label}_{regime}_{perturbation}_seed{seed}"
                apply_named_regime(run_args, regime)
                result = run_single_experiment(run_args)
                grouped_results[(regime, perturbation)].append(result)
                summary_rows.append(summary_row_for_run(result))
                long_log_rows.extend(long_log_rows_for_run(result))
                first_hit_rows.extend(first_hit_rows_for_run(result, args.first_hit_rmax))

    aggregate_rows = aggregate_summary_rows(summary_rows)
    first_hit_agg_rows = aggregate_first_hit_rows(first_hit_rows, args.first_hit_rmax)
    plot_paths = [] if args.skip_plots else generate_group_plots(grouped_results, args.plots_dir, args.plot_points)
    summary_md = build_batch_markdown(args, summary_rows, aggregate_rows, first_hit_agg_rows, plot_paths)

    return {
        "summary_rows": summary_rows,
        "aggregate_rows": aggregate_rows,
        "long_log_rows": long_log_rows,
        "first_hit_agg_rows": first_hit_agg_rows,
        "plot_paths": plot_paths,
        "summary_md": summary_md,
        "answers": interpret_batch_questions(aggregate_rows, first_hit_agg_rows),
    }

def write_batch_outputs(batch: Dict[str, Any], args: argparse.Namespace) -> None:
    ensure_parent_dir(args.batch_summary_csv)
    with open(args.batch_summary_csv, "w", newline="", encoding="utf-8") as f:
        if batch["summary_rows"]:
            writer = csv.DictWriter(f, fieldnames=list(batch["summary_rows"][0].keys()))
            writer.writeheader()
            writer.writerows(batch["summary_rows"])

    ensure_parent_dir(args.batch_aggregate_csv)
    with open(args.batch_aggregate_csv, "w", newline="", encoding="utf-8") as f:
        if batch["aggregate_rows"]:
            writer = csv.DictWriter(f, fieldnames=list(batch["aggregate_rows"][0].keys()))
            writer.writeheader()
            writer.writerows(batch["aggregate_rows"])

    ensure_parent_dir(args.batch_log_csv)
    with open(args.batch_log_csv, "w", newline="", encoding="utf-8") as f:
        if batch["long_log_rows"]:
            writer = csv.DictWriter(f, fieldnames=list(batch["long_log_rows"][0].keys()))
            writer.writeheader()
            writer.writerows(batch["long_log_rows"])

    ensure_parent_dir(args.batch_first_hit_csv)
    with open(args.batch_first_hit_csv, "w", newline="", encoding="utf-8") as f:
        if batch["first_hit_agg_rows"]:
            writer = csv.DictWriter(f, fieldnames=list(batch["first_hit_agg_rows"][0].keys()))
            writer.writeheader()
            writer.writerows(batch["first_hit_agg_rows"])

    ensure_parent_dir(args.batch_summary_md)
    with open(args.batch_summary_md, "w", encoding="utf-8") as f:
        f.write(batch["summary_md"])

    ensure_parent_dir(args.batch_report_json)
    with open(args.batch_report_json, "w", encoding="utf-8") as f:
        json.dump({
            "label": args.label,
            "answers": batch["answers"],
            "aggregate_rows": batch["aggregate_rows"],
            "plot_paths": batch["plot_paths"],
        }, f, indent=2, sort_keys=True)


# ----------------------------
# Main
# ----------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Perturbation / causal-cone lab for the relational universe model.")
    p.add_argument("--mode", type=str, default="single", choices=["single", "batch"])
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
    p.add_argument("--seeds", type=str, default="", help="Comma-separated seeds for batch mode.")
    p.add_argument("--regimes", type=str, default="", help="Comma-separated regimes for batch mode.")
    p.add_argument("--perturbations", type=str, default="", help="Comma-separated perturbations for batch mode.")
    p.add_argument("--batch-config-json", type=str, default="", help="Optional JSON config for batch mode.")
    p.add_argument("--batch-summary-csv", type=str, default="perturbation_batch_summary.csv")
    p.add_argument("--batch-aggregate-csv", type=str, default="perturbation_batch_aggregate.csv")
    p.add_argument("--batch-log-csv", type=str, default="perturbation_batch_log.csv")
    p.add_argument("--batch-first-hit-csv", type=str, default="perturbation_batch_first_hits.csv")
    p.add_argument("--batch-summary-md", type=str, default="perturbation_batch_summary.md")
    p.add_argument("--batch-report-json", type=str, default="perturbation_batch_report.json")
    p.add_argument("--plots-dir", type=str, default="perturbation_plots")
    p.add_argument("--plot-points", type=int, default=80)
    p.add_argument("--skip-plots", action="store_true")
    return p

def main() -> None:
    args = build_parser().parse_args()
    if args.mode == "batch":
        batch = run_batch_experiments(args)
        write_batch_outputs(batch, args)
        for row in batch["aggregate_rows"]:
            label, reason = interpret_spread_pattern(row)
            print(f"[{row['regime']} / {row['perturbation']}] {label}: {reason}")
        print(json.dumps({
            "answers": batch["answers"],
            "num_groups": len(batch["aggregate_rows"]),
            "num_runs": len(batch["summary_rows"]),
            "plots_written": len(batch["plot_paths"]),
        }, indent=2, sort_keys=True))
        return

    apply_presets(args)
    args.regime = infer_regime_name(args)
    result = run_single_experiment(args)
    write_single_outputs(result, args)
    print(json.dumps(result["report"]["headline_metrics"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
