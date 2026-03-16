
#!/usr/bin/env python3
"""relational_universe_local_max_coupling_lab.py

v0.7 local maximal coupling laboratory for the relational-universe toy model.

This script extends v0.6 by replacing common-random-number/rank coupling of
local choices with an explicit maximal coupling of finite local transition
kernels inside each event family. It also adds meeting/survival diagnostics.

Key idea
--------
Keep familywise uniformization:
    choose family using dominating rates mu_f = max(lambda_f^A, lambda_f^B)
    couple accept/reject maximally at the Bernoulli level using a shared U

Then, conditional on both branches accepting the same family, build the
finite local transition distributions for each branch and couple them with
either:
    - rank coupling  (baseline)
    - maximal coupling (v0.7)

When states are equal, the local kernels are identical, so the maximal coupling
is absorbing after meeting: once the two branches meet, they remain together.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple


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


# ----------------------------
# Features
# ----------------------------

def comb2(k: int) -> int:
    return 0 if k < 2 else k * (k - 1) // 2


def linear_fit(xs: Sequence[float], ys: Sequence[float]) -> Tuple[float, float]:
    pts = [(float(x), float(y)) for x, y in zip(xs, ys) if math.isfinite(float(x)) and math.isfinite(float(y))]
    if len(pts) < 2:
        return float("nan"), float("nan")
    xbar = sum(x for x, _ in pts) / len(pts)
    ybar = sum(y for _, y in pts) / len(pts)
    sxx = sum((x - xbar) ** 2 for x, _ in pts)
    if sxx <= 0.0:
        return float("nan"), float("nan")
    sxy = sum((x - xbar) * (y - ybar) for x, y in pts)
    slope = sxy / sxx
    intercept = ybar - slope * xbar
    return float(slope), float(intercept)

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

def adjacency_spectral_radius(g: UGraph, iters: int = 25) -> float:
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

def approx_clustering(g: UGraph, sample: int = 150, rng: Optional[random.Random] = None) -> float:
    vs = g.nodes()
    if not vs:
        return 0.0
    if len(vs) > sample:
        rng = rng or random.Random(0)
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
    return sum(coeffs) / len(coeffs) if coeffs else 0.0

def bfs_distances(g: UGraph, sources: Iterable[int]) -> Dict[int, int]:
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
        for u in g.neighbors(v):
            if u not in dist:
                dist[u] = dist[v] + 1
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

def volume_dimension_proxy(g: UGraph, samples: int = 4, r_max: int = 4, rng: Optional[random.Random] = None) -> float:
    vs = g.nodes()
    if len(vs) < 2:
        return 0.0
    rng = rng or random.Random(0)
    roots = vs if len(vs) <= samples else rng.sample(vs, samples)
    ds = []
    for root in roots:
        vols = bfs_ball_volumes(g, root, r_max)
        xs = []
        ys = []
        for rad in range(1, len(vols)):
            if vols[rad] > 1:
                xs.append(math.log(rad + 1.0))
                ys.append(math.log(float(vols[rad])))
        if len(xs) >= 2:
            slope, _ = linear_fit(xs, ys)
            ds.append(float(slope))
    return float(sum(ds) / len(ds)) if ds else 0.0


FEATURE_KEYS = [
    "tokens",
    "nodes",
    "components",
    "beta1",
    "wedges",
    "triangles",
    "spectral_radius",
    "clustering",
    "dim_proxy",
]


@dataclass
class State:
    g: UGraph
    token_pos: Dict[int, int]
    t: float = 0.0

    def clone(self) -> "State":
        return State(self.g.clone(), dict(self.token_pos), self.t)

    def token_count(self) -> int:
        return len(self.token_pos)

    def sorted_token_ids(self) -> List[int]:
        return sorted(self.token_pos.keys())


@dataclass
class Params:
    r_seed: float = 0.04
    r_token: float = 1.0
    r_birth: float = 0.05
    r_death: float = 0.05
    p_triad: float = 0.0
    p_del: float = 0.0
    p_swap: float = 0.08
    birth_degree_bias: float = 0.5
    death_inverse_degree_scale: float = 1.0
    min_tokens: int = 1
    forbid_pruning_current_token_node: bool = True


@dataclass
class PairManager:
    next_node_id: int
    next_token_id: int

    def alloc_node_id(self) -> int:
        nid = self.next_node_id
        self.next_node_id += 1
        return nid

    def alloc_token_id(self) -> int:
        tid = self.next_token_id
        self.next_token_id += 1
        return tid


def params_from_args(args: argparse.Namespace) -> Params:
    return Params(
        r_seed=args.r_seed,
        r_token=args.r_token,
        r_birth=args.r_birth,
        r_death=args.r_death,
        p_triad=args.p_triad,
        p_del=args.p_del,
        p_swap=args.p_swap,
        birth_degree_bias=args.birth_degree_bias,
        death_inverse_degree_scale=args.death_inverse_degree_scale,
        min_tokens=args.min_tokens,
        forbid_pruning_current_token_node=not args.allow_prune_current_token_node,
    )


# ----------------------------
# Initialization / perturbation
# ----------------------------

def bootstrap(initial_cycle: int, initial_tokens: int, rng: random.Random) -> Tuple[State, int, int]:
    g = UGraph()
    initial_cycle = max(4, initial_cycle)
    for v in range(initial_cycle):
        g.add_edge(v, (v + 1) % initial_cycle)
    token_pos = {tid: rng.randrange(initial_cycle) for tid in range(max(1, initial_tokens))}
    return State(g=g, token_pos=token_pos, t=0.0), initial_cycle, max(1, initial_tokens)

def choose_center_token(state: State, center_token_index: int) -> Tuple[int, int, int]:
    tids = state.sorted_token_ids()
    tid = tids[center_token_index % len(tids)]
    v = state.token_pos[tid]
    ns = sorted(state.g.neighbors(v))
    if not ns:
        raise ValueError("Center token sits on isolated node.")
    u = ns[0]
    nu = sorted(w for w in state.g.neighbors(u) if w != v and not state.g.has_edge(v, w))
    if not nu:
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
    return {
        "type": "local_swap",
        "support": sorted({v, u, w}),
        "delta_core": {"tokens": 0, "nodes": 0, "components": 0, "beta1": 0},
    }

def apply_chord_perturbation(state: State, center_token_index: int = 0) -> Dict[str, Any]:
    v, u, w = choose_center_token(state, center_token_index)
    state.g.add_edge(v, w)
    return {
        "type": "add_chord",
        "support": sorted({v, u, w}),
        "delta_core": {"tokens": 0, "nodes": 0, "components": 0, "beta1": +1},
    }

def apply_perturbation(state: State, perturbation: str, center_token_index: int) -> Dict[str, Any]:
    if perturbation == "local_swap":
        return apply_local_swap_perturbation(state, center_token_index)
    if perturbation == "add_chord":
        return apply_chord_perturbation(state, center_token_index)
    raise ValueError(f"Unknown perturbation {perturbation!r}")


# ----------------------------
# State equality / features
# ----------------------------

def feature_row(state: State, rng: Optional[random.Random] = None) -> Dict[str, float]:
    g = state.g
    return {
        "tokens": float(state.token_count()),
        "nodes": float(g.num_nodes()),
        "components": float(count_components(g)),
        "beta1": float(beta1_cycle_rank(g)),
        "wedges": float(wedge_count(g)),
        "triangles": float(triangle_count(g)),
        "spectral_radius": float(adjacency_spectral_radius(g)),
        "clustering": float(approx_clustering(g, rng=rng)),
        "dim_proxy": float(volume_dimension_proxy(g, rng=rng)),
    }

def states_equal(a: State, b: State) -> bool:
    return a.token_pos == b.token_pos and a.g.edge_set() == b.g.edge_set()


# ----------------------------
# Rates
# ----------------------------

def birth_weights(state: State, params: Params) -> Dict[int, float]:
    out: Dict[int, float] = {}
    for tid, node in state.token_pos.items():
        deg = state.g.degree(node)
        out[tid] = 1.0 + params.birth_degree_bias * max(deg - 1, 0)
    return out

def death_weights(state: State, params: Params) -> Dict[int, float]:
    out: Dict[int, float] = {}
    for tid, node in state.token_pos.items():
        deg = state.g.degree(node)
        out[tid] = params.death_inverse_degree_scale / float(1 + max(deg, 0))
    return out

def family_rates(state: State, params: Params) -> Dict[str, float]:
    k = state.token_count()
    bw = birth_weights(state, params)
    dw = death_weights(state, params)
    death_mass = 0.0 if k <= params.min_tokens else sum(dw.values())
    return {
        "seed": max(0.0, params.r_seed),
        "token": max(0.0, params.r_token) * k,
        "birth": max(0.0, params.r_birth) * sum(bw.values()),
        "death": max(0.0, params.r_death) * death_mass,
    }


# ----------------------------
# Local kernels
# ----------------------------

Descriptor = Tuple[Any, ...]

def normalize_dist(d: Dict[Descriptor, float]) -> Dict[Descriptor, float]:
    total = float(sum(d.values()))
    if total <= 0.0:
        return {}
    return {k: float(v) / total for k, v in d.items() if v > 0.0}

def local_seed_kernel(state: State) -> Dict[Descriptor, float]:
    tids = state.sorted_token_ids()
    if tids:
        p = 1.0 / len(tids)
        return {("seed_tid", tid): p for tid in tids}
    nodes = sorted(state.g.nodes())
    if not nodes:
        return {}
    p = 1.0 / len(nodes)
    return {("seed_node", nid): p for nid in nodes}

def local_birth_kernel(state: State, params: Params) -> Dict[Descriptor, float]:
    tids = state.sorted_token_ids()
    if tids:
        bw = birth_weights(state, params)
        tot = sum(bw[tid] for tid in tids)
        if tot <= 0.0:
            return {}
        return {("birth_tid", tid): bw[tid] / tot for tid in tids}
    nodes = sorted(state.g.nodes())
    if not nodes:
        return {}
    p = 1.0 / len(nodes)
    return {("birth_node", nid): p for nid in nodes}

def local_death_kernel(state: State, params: Params) -> Dict[Descriptor, float]:
    tids = state.sorted_token_ids()
    if len(tids) <= params.min_tokens:
        return {}
    dw = death_weights(state, params)
    tot = sum(dw[tid] for tid in tids)
    if tot <= 0.0:
        return {}
    return {("death_tid", tid): dw[tid] / tot for tid in tids}

def local_token_kernel(state: State, params: Params) -> Dict[Descriptor, float]:
    tids = state.sorted_token_ids()
    k = len(tids)
    if k == 0:
        return {}
    if params.p_del + params.p_triad + params.p_swap > 1.0 + 1e-12:
        raise ValueError("Require p_del + p_triad + p_swap <= 1 in v0.7 local kernel.")
    dist: Dict[Descriptor, float] = {}
    for tid in tids:
        v = state.token_pos[tid]
        neigh = sorted(state.g.neighbors(v))
        base_tid = 1.0 / k
        if not neigh:
            desc = ("stuck", tid, v)
            dist[desc] = dist.get(desc, 0.0) + base_tid
            continue
        for u in neigh:
            base = base_tid / len(neigh)
            move_mass = max(0.0, 1.0 - (params.p_del + params.p_triad + params.p_swap))

            # delete branch
            delete_allowed = True
            if params.forbid_pruning_current_token_node and state.g.degree(u) <= 1:
                delete_allowed = False
            if delete_allowed:
                desc = ("delete", tid, v, u)
                dist[desc] = dist.get(desc, 0.0) + base * params.p_del
            else:
                move_mass += params.p_del

            # triad candidates
            triad_cands = sorted(w for w in state.g.neighbors(u) if w != v and not state.g.has_edge(v, w))
            if triad_cands:
                each = base * params.p_triad / len(triad_cands)
                for w in triad_cands:
                    desc = ("triad", tid, v, u, w)
                    dist[desc] = dist.get(desc, 0.0) + each
            else:
                move_mass += params.p_triad

            # swap candidates
            swap_allowed = True
            if params.forbid_pruning_current_token_node and state.g.degree(u) <= 1:
                swap_allowed = False
            if swap_allowed and triad_cands:
                each = base * params.p_swap / len(triad_cands)
                for w in triad_cands:
                    desc = ("swap", tid, v, u, w)
                    dist[desc] = dist.get(desc, 0.0) + each
            else:
                move_mass += params.p_swap

            move_desc = ("move", tid, v, u)
            dist[move_desc] = dist.get(move_desc, 0.0) + base * move_mass
    return normalize_dist(dist)

def family_kernel(state: State, family: str, params: Params) -> Dict[Descriptor, float]:
    if family == "seed":
        return local_seed_kernel(state)
    if family == "birth":
        return local_birth_kernel(state, params)
    if family == "death":
        return local_death_kernel(state, params)
    if family == "token":
        return local_token_kernel(state, params)
    return {}


# ----------------------------
# Sampling / coupling
# ----------------------------

def sample_from_dist(dist: Dict[Descriptor, float], rng: random.Random) -> Descriptor:
    items = sorted(dist.items(), key=lambda kv: repr(kv[0]))
    x = rng.random()
    acc = 0.0
    last = items[-1][0]
    for desc, p in items:
        acc += p
        if x <= acc:
            return desc
    return last

def rank_coupling(dist_a: Dict[Descriptor, float], dist_b: Dict[Descriptor, float], rng: random.Random) -> Tuple[Descriptor, Descriptor, float]:
    alpha = overlap_mass(dist_a, dist_b)
    support = sorted(set(dist_a.keys()).union(dist_b.keys()), key=repr)
    u = rng.random()
    def select(dist: Dict[Descriptor, float]) -> Descriptor:
        acc = 0.0
        last = None
        for desc in support:
            acc += dist.get(desc, 0.0)
            if u <= acc:
                return desc
            last = desc
        assert last is not None
        return last
    return select(dist_a), select(dist_b), alpha

def overlap_mass(dist_a: Dict[Descriptor, float], dist_b: Dict[Descriptor, float]) -> float:
    return float(sum(min(dist_a.get(k, 0.0), dist_b.get(k, 0.0)) for k in set(dist_a).union(dist_b)))

def maximal_coupling(dist_a: Dict[Descriptor, float], dist_b: Dict[Descriptor, float], rng: random.Random) -> Tuple[Descriptor, Descriptor, float]:
    alpha = overlap_mass(dist_a, dist_b)
    if alpha > 0.0 and rng.random() < alpha:
        overlap = {k: min(dist_a.get(k, 0.0), dist_b.get(k, 0.0)) / alpha for k in set(dist_a).union(dist_b)}
        z = sample_from_dist(overlap, rng)
        return z, z, alpha
    resid_a_raw = {k: max(0.0, dist_a.get(k, 0.0) - min(dist_a.get(k, 0.0), dist_b.get(k, 0.0))) for k in dist_a}
    resid_b_raw = {k: max(0.0, dist_b.get(k, 0.0) - min(dist_a.get(k, 0.0), dist_b.get(k, 0.0))) for k in dist_b}
    resid_a = normalize_dist(resid_a_raw)
    resid_b = normalize_dist(resid_b_raw)
    # if alpha=1, residuals empty; this branch should not occur due to initial check, but guard anyway
    if not resid_a:
        a = sample_from_dist(dist_a, rng)
    else:
        a = sample_from_dist(resid_a, rng)
    if not resid_b:
        b = sample_from_dist(dist_b, rng)
    else:
        b = sample_from_dist(resid_b, rng)
    return a, b, alpha

def sample_coupled_descriptors(dist_a: Dict[Descriptor, float], dist_b: Dict[Descriptor, float], rng: random.Random, mode: str) -> Tuple[Descriptor, Descriptor, float]:
    if mode == "rank":
        return rank_coupling(dist_a, dist_b, rng)
    if mode == "maximal":
        return maximal_coupling(dist_a, dist_b, rng)
    raise ValueError(f"Unknown local coupling mode: {mode}")


# ----------------------------
# Apply descriptors
# ----------------------------

def relocate_tokens_from_dead_node(token_pos: Dict[int, int], dead_node: int, destination: int) -> None:
    for tid, node in list(token_pos.items()):
        if node == dead_node:
            token_pos[tid] = destination

def apply_seed_descriptor(state: State, desc: Descriptor, new_node_id: int) -> Dict[str, Any]:
    kind, ident = desc
    if kind == "seed_tid":
        if ident not in state.token_pos:
            return {"event": "seed_reject", "reason": "missing_tid"}
        host = state.token_pos[ident]
    elif kind == "seed_node":
        if ident not in state.g.adj:
            return {"event": "seed_reject", "reason": "missing_node"}
        host = ident
    else:
        raise ValueError(f"Bad seed descriptor {desc}")
    state.g.add_edge(new_node_id, host)
    return {"event": "seed", "host": host, "new_node": new_node_id, "descriptor": desc}

def apply_birth_descriptor(state: State, desc: Descriptor, new_token_id: int) -> Dict[str, Any]:
    kind, ident = desc
    if kind == "birth_tid":
        if ident not in state.token_pos:
            return {"event": "birth_reject", "reason": "missing_tid"}
        host_node = state.token_pos[ident]
    elif kind == "birth_node":
        if ident not in state.g.adj:
            return {"event": "birth_reject", "reason": "missing_node"}
        host_node = ident
    else:
        raise ValueError(f"Bad birth descriptor {desc}")
    state.token_pos[new_token_id] = host_node
    return {"event": "birth", "new_token_id": new_token_id, "node": host_node, "descriptor": desc}

def apply_death_descriptor(state: State, desc: Descriptor) -> Dict[str, Any]:
    kind, tid = desc
    if kind != "death_tid":
        raise ValueError(f"Bad death descriptor {desc}")
    if tid not in state.token_pos:
        return {"event": "death_reject", "reason": "missing_tid"}
    node = state.token_pos.pop(tid)
    return {"event": "death", "token_id": tid, "node": node, "descriptor": desc}

def apply_token_descriptor(state: State, desc: Descriptor, params: Params) -> Dict[str, Any]:
    event = desc[0]
    if event == "stuck":
        _, tid, v = desc
        if tid not in state.token_pos or state.token_pos[tid] != v:
            return {"event": "token_reject", "reason": "stale_stuck_descriptor", "descriptor": desc}
        return {"event": "stuck", "token_id": tid, "node_before": v, "descriptor": desc}

    if event not in {"move", "delete", "triad", "swap"}:
        raise ValueError(f"Bad token descriptor {desc}")

    tid = int(desc[1])
    v = int(desc[2])
    u = int(desc[3])

    if tid not in state.token_pos or state.token_pos[tid] != v:
        return {"event": "token_reject", "reason": "stale_token_descriptor", "descriptor": desc}
    if not state.g.has_edge(v, u):
        return {"event": "token_reject", "reason": "missing_edge", "descriptor": desc}

    deg_v_before = state.g.degree(v)
    deg_u_before = state.g.degree(u)
    state.token_pos[tid] = u
    ctx: Dict[str, Any] = {
        "event": event,
        "token_id": tid,
        "v_before": v,
        "u_before": u,
        "deg_v_before": deg_v_before,
        "deg_u_before": deg_u_before,
        "descriptor": desc,
    }

    if event == "move":
        return ctx

    if event == "delete":
        state.g.remove_edge(v, u)
        if state.g.degree(v) == 0:
            relocate_tokens_from_dead_node(state.token_pos, v, u)
            state.g.remove_node(v)
            ctx["pruned_v"] = v
        return ctx

    w = int(desc[4])
    if event == "triad":
        state.g.add_edge(v, w)
        return ctx

    # swap
    state.g.remove_edge(v, u)
    state.g.add_edge(v, w)
    if state.g.degree(u) == 0:
        relocate_tokens_from_dead_node(state.token_pos, u, v)
        state.g.remove_node(u)
        ctx["pruned_u"] = u
    return ctx

def apply_descriptor(state: State, family: str, desc: Descriptor, params: Params, manager: PairManager) -> Dict[str, Any]:
    if family == "seed":
        nid = manager.alloc_node_id()
        return apply_seed_descriptor(state, desc, nid)
    if family == "birth":
        tid = manager.alloc_token_id()
        return apply_birth_descriptor(state, desc, tid)
    if family == "death":
        return apply_death_descriptor(state, desc)
    if family == "token":
        return apply_token_descriptor(state, desc, params)
    return {"event": "null", "descriptor": desc}


# ----------------------------
# Coupled step
# ----------------------------

def coupled_step(
    control: State,
    perturbed: State,
    manager: PairManager,
    rng: random.Random,
    params: Params,
    local_coupling: str,
) -> Dict[str, Any]:
    rates_c = family_rates(control, params)
    rates_p = family_rates(perturbed, params)
    families = ["seed", "token", "birth", "death"]
    mu = {f: max(rates_c[f], rates_p[f]) for f in families}
    M = sum(mu.values())
    if M <= 0.0:
        return {"family": "noop", "dt": 0.0}

    dt = rng.expovariate(M)
    control.t += dt
    perturbed.t += dt

    x = rng.random() * M
    acc = 0.0
    family = families[-1]
    for f in families:
        acc += mu[f]
        if x <= acc:
            family = f
            break

    u_accept = rng.random()
    accept_c = (mu[family] > 0.0) and (u_accept < rates_c[family] / mu[family])
    accept_p = (mu[family] > 0.0) and (u_accept < rates_p[family] / mu[family])

    desc_c: Optional[Descriptor] = None
    desc_p: Optional[Descriptor] = None
    alpha = 0.0
    dist_size_c = 0
    dist_size_p = 0
    ctx_c: Dict[str, Any] = {"event": "null"}
    ctx_p: Dict[str, Any] = {"event": "null"}

    if accept_c and accept_p:
        dist_c = family_kernel(control, family, params)
        dist_p = family_kernel(perturbed, family, params)
        dist_size_c = len(dist_c)
        dist_size_p = len(dist_p)
        if dist_c and dist_p:
            desc_c, desc_p, alpha = sample_coupled_descriptors(dist_c, dist_p, rng, local_coupling)
            if family in {"seed", "birth"} and desc_c == desc_p:
                # shared id allocation happens once if exact same descriptor
                if family == "seed":
                    nid = manager.alloc_node_id()
                    ctx_c = apply_seed_descriptor(control, desc_c, nid)
                    ctx_p = apply_seed_descriptor(perturbed, desc_p, nid)
                else:
                    tid = manager.alloc_token_id()
                    ctx_c = apply_birth_descriptor(control, desc_c, tid)
                    ctx_p = apply_birth_descriptor(perturbed, desc_p, tid)
            else:
                if family == "seed":
                    if desc_c is not None:
                        nid_c = manager.alloc_node_id()
                        ctx_c = apply_seed_descriptor(control, desc_c, nid_c)
                    if desc_p is not None:
                        nid_p = manager.alloc_node_id()
                        ctx_p = apply_seed_descriptor(perturbed, desc_p, nid_p)
                elif family == "birth":
                    if desc_c is not None:
                        tid_c = manager.alloc_token_id()
                        ctx_c = apply_birth_descriptor(control, desc_c, tid_c)
                    if desc_p is not None:
                        tid_p = manager.alloc_token_id()
                        ctx_p = apply_birth_descriptor(perturbed, desc_p, tid_p)
                else:
                    if desc_c is not None:
                        ctx_c = apply_descriptor(control, family, desc_c, params, manager)
                    if desc_p is not None:
                        ctx_p = apply_descriptor(perturbed, family, desc_p, params, manager)
        else:
            # if one kernel unexpectedly empty despite acceptance, degrade to null on both
            pass

    elif accept_c:
        dist_c = family_kernel(control, family, params)
        dist_size_c = len(dist_c)
        if dist_c:
            desc_c = sample_from_dist(dist_c, rng)
            ctx_c = apply_descriptor(control, family, desc_c, params, manager)
    elif accept_p:
        dist_p = family_kernel(perturbed, family, params)
        dist_size_p = len(dist_p)
        if dist_p:
            desc_p = sample_from_dist(dist_p, rng)
            ctx_p = apply_descriptor(perturbed, family, desc_p, params, manager)

    return {
        "family": family,
        "dt": dt,
        "M": M,
        "rates_control": rates_c,
        "rates_perturbed": rates_p,
        "mu": mu,
        "accept_control": accept_c,
        "accept_perturbed": accept_p,
        "local_overlap_prob": alpha,
        "local_same_descriptor": int(desc_c == desc_p and desc_c is not None),
        "local_coupling": local_coupling,
        "dist_size_control": dist_size_c,
        "dist_size_perturbed": dist_size_p,
        "descriptor_control": None if desc_c is None else repr(desc_c),
        "descriptor_perturbed": None if desc_p is None else repr(desc_p),
        "control": ctx_c,
        "perturbed": ctx_p,
    }


# ----------------------------
# Divergence metrics
# ----------------------------

def edge_symmetric_difference(control: State, perturbed: State) -> Set[Tuple[int, int]]:
    return control.g.edge_set().symmetric_difference(perturbed.g.edge_set())

def node_symmetric_difference(control: State, perturbed: State) -> Set[int]:
    return set(control.g.nodes()).symmetric_difference(set(perturbed.g.nodes()))

def token_damage_nodes(control: State, perturbed: State) -> Set[int]:
    out: Set[int] = set()
    all_tids = set(control.token_pos.keys()).union(perturbed.token_pos.keys())
    for tid in all_tids:
        a = control.token_pos.get(tid)
        b = perturbed.token_pos.get(tid)
        if a != b:
            if a is not None:
                out.add(a)
            if b is not None:
                out.add(b)
    return out

def damaged_nodes(control: State, perturbed: State) -> Set[int]:
    out: Set[int] = set()
    out.update(node_symmetric_difference(control, perturbed))
    out.update(token_damage_nodes(control, perturbed))
    for a, b in edge_symmetric_difference(control, perturbed):
        out.add(a)
        out.add(b)
    return out

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

def feature_differences(control: State, perturbed: State) -> Dict[str, float]:
    fc = feature_row(control)
    fp = feature_row(perturbed)
    return {k: float(fp[k] - fc[k]) for k in FEATURE_KEYS}

def damage_snapshot(control: State, perturbed: State, support: Sequence[int]) -> Dict[str, Any]:
    d_edges = edge_symmetric_difference(control, perturbed)
    d_nodes = damaged_nodes(control, perturbed)
    r_ctrl = radius_from_support(control.g, support, d_nodes)
    r_pert = radius_from_support(perturbed.g, support, d_nodes)
    nearest_ctrl = nearest_damage_distance(control.g, support, d_nodes)
    nearest_pert = nearest_damage_distance(perturbed.g, support, d_nodes)
    diff = feature_differences(control, perturbed)

    shared_tids = set(control.token_pos.keys()).intersection(perturbed.token_pos.keys())
    token_hamming = sum(1 for tid in shared_tids if control.token_pos[tid] != perturbed.token_pos[tid])
    token_union = len(set(control.token_pos.keys()).union(perturbed.token_pos.keys()))
    token_shared_fraction = (len(shared_tids) / token_union) if token_union else 1.0

    shared_nodes = set(control.g.nodes()).intersection(perturbed.g.nodes())
    node_union = len(set(control.g.nodes()).union(perturbed.g.nodes()))
    node_shared_fraction = (len(shared_nodes) / node_union) if node_union else 1.0

    return {
        "edge_diff_count": len(d_edges),
        "node_diff_count": len(node_symmetric_difference(control, perturbed)),
        "damaged_nodes_count": len(d_nodes),
        "token_hamming_shared": token_hamming,
        "token_shared_fraction": token_shared_fraction,
        "node_shared_fraction": node_shared_fraction,
        "radius_control": -1 if r_ctrl is None else int(r_ctrl),
        "radius_perturbed": -1 if r_pert is None else int(r_pert),
        "nearest_control": -1 if nearest_ctrl is None else int(nearest_ctrl),
        "nearest_perturbed": -1 if nearest_pert is None else int(nearest_pert),
        "delta_tokens": diff["tokens"],
        "delta_nodes": diff["nodes"],
        "delta_components": diff["components"],
        "delta_beta1": diff["beta1"],
        "delta_triangles": diff["triangles"],
        "delta_spectral_radius": diff["spectral_radius"],
        "delta_clustering": diff["clustering"],
        "delta_dim_proxy": diff["dim_proxy"],
        "state_equal": int(states_equal(control, perturbed)),
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
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    slope, intercept = linear_fit(xs, ys)
    return {"max_ratio": float(max(ratios)), "fit_slope": float(slope), "fit_intercept": float(intercept)}

def first_hit_times(log_rows: List[Dict[str, Any]], key_r: str, key_t: str, r_max: int) -> Dict[int, Optional[float]]:
    out: Dict[int, Optional[float]] = {r: None for r in range(r_max + 1)}
    for row in log_rows:
        rad = int(row[key_r])
        if rad < 0:
            continue
        t = float(row[key_t])
        for r in range(rad + 1):
            if out[r] is None:
                out[r] = t
    return out

def summarize_events(event_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    fams = ["seed", "token", "birth", "death"]
    out: Dict[str, Any] = {
        "total_potential_events": len(event_rows),
        "both_accept_total": 0,
        "one_sided_total": 0,
        "null_total": 0,
        "family": {},
        "avg_local_overlap_both_accept": 0.0,
        "avg_same_descriptor_both_accept": 0.0,
    }
    overlap_vals = []
    same_vals = []
    for f in fams:
        sub = [r for r in event_rows if r["family"] == f]
        both = [r for r in sub if r["accept_control"] and r["accept_perturbed"]]
        one = [r for r in sub if (r["accept_control"] != r["accept_perturbed"])]
        null = [r for r in sub if (not r["accept_control"] and not r["accept_perturbed"])]
        out["both_accept_total"] += len(both)
        out["one_sided_total"] += len(one)
        out["null_total"] += len(null)
        if both:
            overlap_vals.extend(float(r["local_overlap_prob"]) for r in both)
            same_vals.extend(int(r["local_same_descriptor"]) for r in both)
        out["family"][f] = {
            "potential": len(sub),
            "both_accept": len(both),
            "one_sided": len(one),
            "null": len(null),
            "mean_local_overlap": float(statistics.mean(float(r["local_overlap_prob"]) for r in both)) if both else float("nan"),
            "same_descriptor_rate": float(statistics.mean(int(r["local_same_descriptor"]) for r in both)) if both else float("nan"),
        }
    out["avg_local_overlap_both_accept"] = float(statistics.mean(overlap_vals)) if overlap_vals else float("nan")
    out["avg_same_descriptor_both_accept"] = float(statistics.mean(same_vals)) if same_vals else float("nan")
    return out


def ensure_parent_dir(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def write_text(path: str, text: str) -> None:
    ensure_parent_dir(path)
    Path(path).write_text(text, encoding="utf-8")


def write_json(path: str, data: Dict[str, Any]) -> None:
    ensure_parent_dir(path)
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True, default=str), encoding="utf-8")


def empirical_distribution(samples: Sequence[Descriptor]) -> Dict[Descriptor, float]:
    if not samples:
        return {}
    counts: Dict[Descriptor, int] = {}
    for desc in samples:
        counts[desc] = counts.get(desc, 0) + 1
    total = float(len(samples))
    return {desc: count / total for desc, count in counts.items()}


def total_variation_distance(dist_a: Dict[Descriptor, float], dist_b: Dict[Descriptor, float]) -> float:
    support = set(dist_a).union(dist_b)
    return 0.5 * sum(abs(dist_a.get(desc, 0.0) - dist_b.get(desc, 0.0)) for desc in support)


def finite_mean(values: Iterable[float], fallback: float = float("nan")) -> float:
    vals = [float(v) for v in values if math.isfinite(float(v))]
    if not vals:
        return fallback
    return float(statistics.mean(vals))


# ----------------------------
# Single run
# ----------------------------

def run_single(args: argparse.Namespace) -> Dict[str, Any]:
    rng = random.Random(args.seed)
    params = params_from_args(args)

    base, next_node_id, next_token_id = bootstrap(args.initial_cycle, args.initial_tokens, rng)
    control = base.clone()
    perturbed = base.clone()
    initial_control_features = feature_row(control)
    perturbation_info = apply_perturbation(perturbed, args.perturbation, args.center_token_index)
    support = perturbation_info["support"]
    manager = PairManager(next_node_id=next_node_id, next_token_id=next_token_id)

    event_rows: List[Dict[str, Any]] = []
    log_rows: List[Dict[str, Any]] = []
    equal_prev = states_equal(control, perturbed)
    first_meeting_step = None if not equal_prev else 0
    first_meeting_time = None if not equal_prev else 0.0
    meeting_count = 1 if equal_prev else 0
    last_equal_time = 0.0 if equal_prev else None
    total_unequal_time = 0.0
    unequal_start_t = 0.0 if not equal_prev else None

    for step in range(1, args.steps + 1):
        ev = coupled_step(control, perturbed, manager, rng, params, args.local_coupling)
        ev["step"] = step
        ev["t"] = control.t
        event_rows.append(ev)

        equal_now = states_equal(control, perturbed)
        if equal_now and not equal_prev:
            if first_meeting_step is None:
                first_meeting_step = step
                first_meeting_time = control.t
            meeting_count += 1
            if unequal_start_t is not None:
                total_unequal_time += control.t - unequal_start_t
                unequal_start_t = None
        elif (not equal_now) and equal_prev:
            unequal_start_t = control.t
        if equal_now:
            last_equal_time = control.t
        equal_prev = equal_now

        if step % args.log_every == 0 or step == args.steps or step == 1:
            snap = damage_snapshot(control, perturbed, support)
            control_features = feature_row(control)
            row = {
                "step": step,
                "t": control.t,
                "local_coupling": args.local_coupling,
                **snap,
                **{f"control_{key}": control_features[key] for key in FEATURE_KEYS},
            }
            log_rows.append(row)

    if unequal_start_t is not None:
        total_unequal_time += control.t - unequal_start_t

    coupling = summarize_events(event_rows)
    speed_ctrl = estimate_front_speed(log_rows, "t", "radius_control")
    speed_pert = estimate_front_speed(log_rows, "t", "radius_perturbed")

    final_snap = damage_snapshot(control, perturbed, support)
    final_control_features = feature_row(control)
    mean_control_spectral_radius = float(statistics.mean(float(row["control_spectral_radius"]) for row in log_rows)) if log_rows else final_control_features["spectral_radius"]
    mean_control_clustering = float(statistics.mean(float(row["control_clustering"]) for row in log_rows)) if log_rows else final_control_features["clustering"]
    mean_control_dim_proxy = float(statistics.mean(float(row["control_dim_proxy"]) for row in log_rows)) if log_rows else final_control_features["dim_proxy"]
    headline_metrics = {
        "final_time": control.t,
        "final_radius_control": final_snap["radius_control"],
        "final_radius_perturbed": final_snap["radius_perturbed"],
        "final_edge_diff_count": final_snap["edge_diff_count"],
        "final_delta_tokens": final_snap["delta_tokens"],
        "final_delta_nodes": final_snap["delta_nodes"],
        "avg_local_overlap_both_accept": coupling["avg_local_overlap_both_accept"],
        "avg_same_descriptor_both_accept": coupling["avg_same_descriptor_both_accept"],
        "fit_speed_control": speed_ctrl["fit_slope"],
        "fit_speed_perturbed": speed_pert["fit_slope"],
        "first_meeting_step": first_meeting_step if first_meeting_step is not None else -1,
        "first_meeting_time": first_meeting_time if first_meeting_time is not None else -1.0,
        "meeting_count": meeting_count,
        "total_unequal_time": total_unequal_time,
        "state_equal_final": final_snap["state_equal"],
        "shared_token_fraction_final": final_snap["token_shared_fraction"],
        "shared_node_fraction_final": final_snap["node_shared_fraction"],
        "drift_beta1": (final_control_features["beta1"] - initial_control_features["beta1"]) / float(max(args.steps, 1)),
        "drift_tokens": (final_control_features["tokens"] - initial_control_features["tokens"]) / float(max(args.steps, 1)),
        "mean_spectral_radius": mean_control_spectral_radius,
        "mean_clustering": mean_control_clustering,
        "mean_dim_proxy": mean_control_dim_proxy,
        "initial_control_beta1": initial_control_features["beta1"],
        "initial_control_tokens": initial_control_features["tokens"],
        "final_control_beta1": final_control_features["beta1"],
        "final_control_tokens": final_control_features["tokens"],
    }

    return {
        "args": vars(args),
        "params": vars(params),
        "perturbation_info": perturbation_info,
        "support": support,
        "event_rows": event_rows,
        "log_rows": log_rows,
        "headline_metrics": headline_metrics,
        "coupling": coupling,
    }


# ----------------------------
# Multirun / comparison
# ----------------------------

def summarize_survival(rows: List[Dict[str, Any]], time_grid: Sequence[float]) -> List[Dict[str, Any]]:
    out = []
    for t in time_grid:
        not_met = 0
        total = 0
        for r in rows:
            total += 1
            mt = float(r["first_meeting_time"])
            if mt < 0 or mt > t:
                not_met += 1
        out.append({"time": t, "survival_not_met": not_met / total if total else float("nan")})
    return out

def collect_multirun_statistics(args: argparse.Namespace, seeds: Sequence[int], coupling_modes: Sequence[str]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for mode in coupling_modes:
        for seed in seeds:
            a = argparse.Namespace(**vars(args))
            a.seed = int(seed)
            a.local_coupling = mode
            res = run_single(a)
            hm = dict(res["headline_metrics"])
            hm.update({
                "seed": seed,
                "local_coupling": mode,
                "avg_local_overlap_both_accept": res["coupling"]["avg_local_overlap_both_accept"],
                "avg_same_descriptor_both_accept": res["coupling"]["avg_same_descriptor_both_accept"],
                "both_accept_total": res["coupling"]["both_accept_total"],
                "one_sided_total": res["coupling"]["one_sided_total"],
                "null_total": res["coupling"]["null_total"],
            })
            rows.append(hm)
    by_mode: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        by_mode.setdefault(row["local_coupling"], []).append(row)
    summaries = {}
    for mode, sub in by_mode.items():
        summaries[mode] = {
            "runs": len(sub),
            "meeting_fraction": float(sum(1 for r in sub if float(r["first_meeting_time"]) >= 0) / len(sub)) if sub else float("nan"),
            "mean_first_meeting_time_conditional": float(statistics.mean(float(r["first_meeting_time"]) for r in sub if float(r["first_meeting_time"]) >= 0)) if any(float(r["first_meeting_time"]) >= 0 for r in sub) else float("nan"),
            "mean_final_radius_control": finite_mean(float(r["final_radius_control"]) for r in sub),
            "mean_total_unequal_time": finite_mean(float(r["total_unequal_time"]) for r in sub),
            "mean_avg_local_overlap": finite_mean(float(r["avg_local_overlap_both_accept"]) for r in sub),
            "mean_same_descriptor_rate": finite_mean(float(r["avg_same_descriptor_both_accept"]) for r in sub),
            "mean_shared_token_fraction_final": finite_mean(float(r["shared_token_fraction_final"]) for r in sub),
            "mean_shared_node_fraction_final": finite_mean(float(r["shared_node_fraction_final"]) for r in sub),
            "mean_fit_speed_control": finite_mean((float(r["fit_speed_control"]) for r in sub), fallback=0.0),
            "mean_drift_beta1": finite_mean(float(r["drift_beta1"]) for r in sub),
            "mean_drift_tokens": finite_mean(float(r["drift_tokens"]) for r in sub),
            "mean_spectral_radius": finite_mean(float(r["mean_spectral_radius"]) for r in sub),
            "mean_clustering": finite_mean(float(r["mean_clustering"]) for r in sub),
            "mean_dim_proxy": finite_mean(float(r["mean_dim_proxy"]) for r in sub),
        }
    # shared time grid by max observed end time
    t_end = max(float(r["final_time"]) for r in rows) if rows else 0.0
    time_grid = [0.0]
    if t_end > 0:
        for frac in [0.1, 0.25, 0.5, 0.75, 1.0]:
            time_grid.append(frac * t_end)
    survival = {mode: summarize_survival(sub, time_grid) for mode, sub in by_mode.items()}
    return {"rows": rows, "summaries": summaries, "survival": survival, "time_grid": time_grid}


# ----------------------------
# Verification suite
# ----------------------------

def build_verification_pairs(args: argparse.Namespace, params: Params) -> List[Tuple[str, State, State]]:
    rng = random.Random(args.seed)
    base, next_node_id, next_token_id = bootstrap(args.initial_cycle, args.initial_tokens, rng)

    initial_control = base.clone()
    initial_perturbed = base.clone()
    apply_perturbation(initial_perturbed, args.perturbation, args.center_token_index)

    evolved_control = initial_control.clone()
    evolved_perturbed = initial_perturbed.clone()
    manager = PairManager(next_node_id=next_node_id, next_token_id=next_token_id)
    evolve_rng = random.Random(args.seed + 17)
    for _ in range(max(1, args.verification_snapshot_steps)):
        coupled_step(evolved_control, evolved_perturbed, manager, evolve_rng, params, "maximal")

    return [
        ("initial_pair", initial_control, initial_perturbed),
        ("evolved_pair", evolved_control, evolved_perturbed),
    ]


def summarize_kernel_normalization(args: argparse.Namespace, params: Params) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for label, control, perturbed in build_verification_pairs(args, params):
        for branch_name, state in [("control", control), ("perturbed", perturbed)]:
            rates = family_rates(state, params)
            for family in ["seed", "token", "birth", "death"]:
                kernel = family_kernel(state, family, params)
                mass = float(sum(kernel.values()))
                rows.append({
                    "pair": label,
                    "branch": branch_name,
                    "family": family,
                    "support_size": len(kernel),
                    "kernel_sum": mass,
                    "sum_error": abs(mass - 1.0) if kernel else 0.0,
                    "empty_with_positive_rate": int((not kernel) and rates[family] > 0.0),
                })
    return rows


def verify_maximal_coupling_cases(args: argparse.Namespace, params: Params) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    base_seed = args.seed + 101
    for pair_idx, (label, control, perturbed) in enumerate(build_verification_pairs(args, params)):
        for family_idx, family in enumerate(["seed", "token", "birth", "death"]):
            dist_c = family_kernel(control, family, params)
            dist_p = family_kernel(perturbed, family, params)
            if not dist_c or not dist_p:
                continue
            rng = random.Random(base_seed + 100 * pair_idx + family_idx)
            samples_c: List[Descriptor] = []
            samples_p: List[Descriptor] = []
            same = 0
            alpha = overlap_mass(dist_c, dist_p)
            for _ in range(args.verification_trials):
                desc_c, desc_p, _ = maximal_coupling(dist_c, dist_p, rng)
                samples_c.append(desc_c)
                samples_p.append(desc_p)
                if desc_c == desc_p:
                    same += 1
            emp_c = empirical_distribution(samples_c)
            emp_p = empirical_distribution(samples_p)
            rows.append({
                "pair": label,
                "family": family,
                "support_control": len(dist_c),
                "support_perturbed": len(dist_p),
                "local_overlap_prob": alpha,
                "same_descriptor_rate": same / float(max(len(samples_c), 1)),
                "same_descriptor_abs_error": abs((same / float(max(len(samples_c), 1))) - alpha),
                "tv_control_vs_kernel": total_variation_distance(emp_c, dist_c),
                "tv_perturbed_vs_kernel": total_variation_distance(emp_p, dist_p),
            })
    return rows


def verify_absorption(args: argparse.Namespace, params: Params) -> Dict[str, Any]:
    failure_step: Optional[int] = None
    failure_seed: Optional[int] = None
    seeds = [args.seed + offset for offset in range(args.verification_absorption_seeds)]
    for seed in seeds:
        rng = random.Random(seed)
        base, next_node_id, next_token_id = bootstrap(args.initial_cycle, args.initial_tokens, rng)
        control = base.clone()
        perturbed = base.clone()
        manager = PairManager(next_node_id=next_node_id, next_token_id=next_token_id)
        step_rng = random.Random(seed + 313)
        for step in range(1, args.verification_absorption_steps + 1):
            coupled_step(control, perturbed, manager, step_rng, params, "maximal")
            if not states_equal(control, perturbed):
                failure_seed = seed
                failure_step = step
                return {
                    "passed": False,
                    "checked_seeds": len(seeds),
                    "steps_per_seed": args.verification_absorption_steps,
                    "failure_seed": failure_seed,
                    "failure_step": failure_step,
                }
    return {
        "passed": True,
        "checked_seeds": len(seeds),
        "steps_per_seed": args.verification_absorption_steps,
        "failure_seed": -1,
        "failure_step": -1,
    }


def verify_family_frequencies(event_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    families = ["seed", "token", "birth", "death"]
    expected = {family: 0.0 for family in families}
    observed = {family: 0 for family in families}
    total = float(len(event_rows))
    for row in event_rows:
        family = str(row["family"])
        if family in observed:
            observed[family] += 1
        mu = row["mu"]
        M = float(row["M"])
        if M > 0.0:
            for fam in families:
                expected[fam] += float(mu[fam]) / M
    out = []
    for family in families:
        expected_freq = expected[family] / total if total else float("nan")
        observed_freq = observed[family] / total if total else float("nan")
        out.append({
            "family": family,
            "observed_count": observed[family],
            "expected_count": expected[family],
            "observed_frequency": observed_freq,
            "expected_frequency": expected_freq,
            "abs_frequency_error": abs(observed_freq - expected_freq) if total else float("nan"),
        })
    return out


def run_verification_suite(args: argparse.Namespace) -> Dict[str, Any]:
    params = params_from_args(args)
    kernel_checks = summarize_kernel_normalization(args, params)
    coupling_checks = verify_maximal_coupling_cases(args, params)
    absorption = verify_absorption(args, params)

    verification_run_args = argparse.Namespace(**vars(args))
    verification_run_args.steps = args.verification_event_steps
    verification_run_args.seed = args.seed
    verification_run_args.local_coupling = "maximal"
    verification_run = run_single(verification_run_args)
    family_checks = verify_family_frequencies(verification_run["event_rows"])

    compare_args = argparse.Namespace(**vars(args))
    compare_args.steps = args.verification_event_steps
    compare_seeds = list(range(args.seed, args.seed + args.multirun_seeds))
    compare_stats = collect_multirun_statistics(compare_args, compare_seeds, coupling_modes=["rank", "maximal"])

    return {
        "kernel_checks": kernel_checks,
        "coupling_checks": coupling_checks,
        "absorption": absorption,
        "family_checks": family_checks,
        "compare_stats": compare_stats,
        "verification_run": verification_run,
        "verification_event_steps": args.verification_event_steps,
        "verification_trials": args.verification_trials,
    }


def make_verification_md(args: argparse.Namespace, report: Dict[str, Any], compare_csv_path: str) -> str:
    kernel_rows = [["pair", "branch", "family", "support", "kernel_sum", "sum_error", "empty|rate>0"]]
    for row in report["kernel_checks"]:
        kernel_rows.append([
            str(row["pair"]),
            str(row["branch"]),
            str(row["family"]),
            str(row["support_size"]),
            f"{row['kernel_sum']:.12g}",
            f"{row['sum_error']:.3g}",
            str(row["empty_with_positive_rate"]),
        ])

    coupling_rows = [["pair", "family", "alpha", "same_desc_emp", "|emp-alpha|", "tv_control", "tv_perturbed"]]
    for row in report["coupling_checks"]:
        coupling_rows.append([
            str(row["pair"]),
            str(row["family"]),
            f"{row['local_overlap_prob']:.6g}",
            f"{row['same_descriptor_rate']:.6g}",
            f"{row['same_descriptor_abs_error']:.3g}",
            f"{row['tv_control_vs_kernel']:.3g}",
            f"{row['tv_perturbed_vs_kernel']:.3g}",
        ])

    family_rows = [["family", "observed_freq", "expected_freq", "|diff|", "observed_count", "expected_count"]]
    for row in report["family_checks"]:
        family_rows.append([
            str(row["family"]),
            f"{row['observed_frequency']:.6g}",
            f"{row['expected_frequency']:.6g}",
            f"{row['abs_frequency_error']:.3g}",
            str(row["observed_count"]),
            f"{row['expected_count']:.3f}",
        ])

    compare_rows = [["mode", "meeting_fraction", "mean_overlap", "same_descriptor_rate", "mean_unequal_time", "shared_token_fraction_final"]]
    for mode, summary in report["compare_stats"]["summaries"].items():
        compare_rows.append([
            mode,
            f"{summary['meeting_fraction']:.6g}",
            f"{summary['mean_avg_local_overlap']:.6g}",
            f"{summary['mean_same_descriptor_rate']:.6g}",
            f"{summary['mean_total_unequal_time']:.6g}",
            f"{summary['mean_shared_token_fraction_final']:.6g}",
        ])

    max_kernel_error = max((row["sum_error"] for row in report["kernel_checks"]), default=0.0)
    max_family_error = max((row["abs_frequency_error"] for row in report["family_checks"]), default=0.0)
    max_coupling_error = max((row["same_descriptor_abs_error"] for row in report["coupling_checks"]), default=0.0)
    max_descriptor_tv = max((max(row["tv_control_vs_kernel"], row["tv_perturbed_vs_kernel"]) for row in report["coupling_checks"]), default=0.0)

    lines = [
        "# v0.7 lokal maksimal kobling – verifikasjonsnotat",
        "",
        "## Hva som er eksakt i implementasjonen",
        "",
        "- Familywise uniformization og Bernoulli-aksept per familie er eksakte konstruksjoner gitt de aktuelle familie-ratene.",
        "- Når to grener er identiske og bruker `maximal`, er koblingen absorberende fordi familie-rater, lokale kjerner og ID-allokering er identiske.",
        "- `local_overlap_prob` er den eksakte overlap-massen `sum_i min(p_i, q_i)` for de to endelige lokale kjernene.",
        "",
        "## Hva som er numerisk verifisert her",
        "",
        f"- Maksimal kernel-normaliseringsfeil over sjekkede kjerner: `{max_kernel_error:.3g}`",
        f"- Maksimal feil mellom empirisk same-descriptor-rate og teoretisk overlap-masse: `{max_coupling_error:.3g}`",
        f"- Maksimal frekvensfeil for familywise potensialfamilier: `{max_family_error:.3g}`",
        f"- Maksimal TV-avstand mellom empiriske descriptor-marginaler og lokale kjerner: `{max_descriptor_tv:.3g}`",
        f"- Absorpsjonstest under maksimal kobling: `{'PASS' if report['absorption']['passed'] else 'FAIL'}` over {report['absorption']['checked_seeds']} seeds x {report['absorption']['steps_per_seed']} steg",
        "",
        "## Hva som fortsatt er heuristisk eller dynamisk",
        "",
        "- `meeting_fraction`, `total_unequal_time` og `shared_token_fraction_final` er regimeavhengige dynamiske mål, ikke algebraiske garantier.",
        "- Høy lokal overlap betyr bare at den lokale koblingen er skarpere; det beviser ikke global kontraksjon av hele CTMC-en.",
        "",
        "## Kernel-sanity",
        "",
        markdown_table(kernel_rows),
        "",
        "## Maksimal kobling og descriptor-marginaler",
        "",
        markdown_table(coupling_rows),
        "",
        "## Familywise marginaltest",
        "",
        markdown_table(family_rows),
        "",
        "## Testpakken som prompten ba om",
        "",
        markdown_table(compare_rows),
        "",
        "## Kommandoeksempler",
        "",
        "```bash",
        f"python relational_universe_local_max_coupling_lab.py --mode verify --label {args.label} --out-prefix {args.out_prefix} --steps {args.verification_event_steps} --multirun-seeds {args.multirun_seeds}",
        "```",
        "",
        "```bash",
        f"python relational_universe_local_max_coupling_lab.py --mode compare --label {args.label} --out-prefix {args.out_prefix} --steps {args.verification_event_steps} --multirun-seeds {args.multirun_seeds}",
        "```",
        "",
        f"_Per-seed compare CSV: `{compare_csv_path}`_",
        "",
    ]
    return "\n".join(lines)


# ----------------------------
# Writers
# ----------------------------

def write_csv(path: str, rows: List[Dict[str, Any]]) -> None:
    ensure_parent_dir(path)
    if not rows:
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write("")
        return
    keys = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow(row)

def make_single_summary_md(args: argparse.Namespace, res: Dict[str, Any], csv_log_path: str, csv_events_path: str) -> str:
    hm = res["headline_metrics"]
    coupling = res["coupling"]
    speed_ctrl = estimate_front_speed(res["log_rows"], "t", "radius_control")
    hit_ctrl = first_hit_times(res["log_rows"], "radius_control", "t", args.first_hit_rmax)

    headline_rows = [["metric", "value"]]
    for k, v in hm.items():
        headline_rows.append([k, f"{v}"])
    fam_rows = [["family", "potential", "both_accept", "one_sided", "null", "mean_overlap", "same_descriptor_rate"]]
    for fam, sub in coupling["family"].items():
        fam_rows.append([
            fam,
            str(sub["potential"]),
            str(sub["both_accept"]),
            str(sub["one_sided"]),
            str(sub["null"]),
            f"{sub['mean_local_overlap']:.6g}" if sub["mean_local_overlap"] == sub["mean_local_overlap"] else "NA",
            f"{sub['same_descriptor_rate']:.6g}" if sub["same_descriptor_rate"] == sub["same_descriptor_rate"] else "NA",
        ])
    hit_rows = [["radius", "first_hit_time_control"]]
    for r in range(args.first_hit_rmax + 1):
        t = hit_ctrl[r]
        hit_rows.append([str(r), "NA" if t is None else f"{t:.6g}"])

    return "\n".join([
        f"# v0.7 representativ kjøring – {args.label}",
        "",
        "## Hva som er nytt i v0.7",
        "",
        "Dette steget beholder familywise uniformization fra v0.6, men bytter ut lokal rank/common-random-number coupling med eksplisitt maksimal kobling av de endelige lokale overgangskjernene.",
        "",
        "Det betyr at når begge grener aksepterer samme event-familie, velger vi lokale overganger slik at sannsynligheten for nøyaktig samme lokale hendelse blir så stor som distribusjonene tillater.",
        "",
        "## Parametre",
        "",
        f"- local_coupling: {args.local_coupling}",
        f"- steps: {args.steps}",
        f"- seed: {args.seed}",
        f"- perturbation: {args.perturbation}",
        f"- r_seed: {args.r_seed}",
        f"- r_token: {args.r_token}",
        f"- r_birth: {args.r_birth}",
        f"- r_death: {args.r_death}",
        f"- p_triad: {args.p_triad}",
        f"- p_del: {args.p_del}",
        f"- p_swap: {args.p_swap}",
        "",
        "## Startperturbasjon",
        "",
        "```json",
        json.dumps(res["perturbation_info"], indent=2, sort_keys=True),
        "```",
        "",
        "## Hovedmål",
        "",
        markdown_table(headline_rows),
        "",
        "## Familywise og lokal koblingskvalitet",
        "",
        markdown_table(fam_rows),
        "",
        "## Frontdiagnostikk",
        "",
        f"- kontrollgren: fit speed ≈ {speed_ctrl['fit_slope']:.6g}",
        f"- kontrollgren: max(r/t) ≈ {speed_ctrl['max_ratio']:.6g}",
        "",
        markdown_table(hit_rows),
        "",
        "## Tolkning",
        "",
        "Hvis v0.7 virker som ønsket, skal vi se høyere lokal overlap og høyere rate av identiske lokale hendelser enn i rank-baseline, uten at vi ofrer korrekt marginal dynamikk.",
        "",
        "Dersom meeting blir vanligere og total unequal time kortere, er det et tegn på at v0.6 faktisk undervurderte hvor mye lokal repair modellen tillater.",
        "",
        f"_Rå logg: `{csv_log_path}`_",
        "",
        f"_Rå eventdata: `{csv_events_path}`_",
        "",
    ])

def make_multirun_summary_md(args: argparse.Namespace, stats: Dict[str, Any], csv_path: str) -> str:
    rows = [["mode", "runs", "meeting_fraction", "mean_first_meeting_time|met", "mean_final_radius", "mean_unequal_time", "mean_local_overlap", "mean_same_descriptor_rate", "mean_shared_token_frac_final", "mean_shared_node_frac_final"]]
    for mode, s in stats["summaries"].items():
        rows.append([
            mode,
            str(s["runs"]),
            f"{s['meeting_fraction']:.6g}",
            f"{s['mean_first_meeting_time_conditional']:.6g}" if s["mean_first_meeting_time_conditional"] == s["mean_first_meeting_time_conditional"] else "NA",
            f"{s['mean_final_radius_control']:.6g}",
            f"{s['mean_total_unequal_time']:.6g}",
            f"{s['mean_avg_local_overlap']:.6g}",
            f"{s['mean_same_descriptor_rate']:.6g}",
            f"{s['mean_shared_token_fraction_final']:.6g}",
            f"{s['mean_shared_node_fraction_final']:.6g}",
        ])
    survival_sections = []
    for mode, surv in stats["survival"].items():
        srows = [["time", "P(not met by t)"]]
        for row in surv:
            srows.append([f"{row['time']:.6g}", f"{row['survival_not_met']:.6g}"])
        survival_sections.extend([
            f"### Overlevelseskurve – {mode}",
            "",
            markdown_table(srows),
            "",
        ])
    return "\n".join([
        f"# v0.7 multirun-sammenligning – {args.label}",
        "",
        "## Formål",
        "",
        "Sammenligne rank-baseline og lokal maksimal kobling over samme seeder og samme parameterregime.",
        "",
        "## Aggregerte resultater",
        "",
        markdown_table(rows),
        "",
        "## Survival/meeting",
        "",
        *survival_sections,
        "## Tolkning",
        "",
        "For v0.7 er nøkkelspørsmålet ikke bare om divergence sprer seg, men også om bedre lokal kobling øker sannsynligheten for repair og tidligere meeting.",
        "",
        f"_Per-seed CSV: `{csv_path}`_",
        "",
    ])

def make_status_md(args: argparse.Namespace, stats: Dict[str, Any]) -> str:
    lines = [
        "# Relasjonell universgraf – status v0.7",
        "",
        "## Hva som er nytt",
        "- Lokal maksimal kobling av endelige overgangskjerner innen hver event-familie.",
        "- Meeting- og survival-analyse for å måle repair, ikke bare divergence.",
        "- Direkte sammenligning mellom rank-baseline og maksimal lokal kobling.",
        "",
        "## Hva som nå er løst",
        "- Vi skiller nå klart mellom:",
        "  - familywise maksimal kobling av aksept/rejekt,",
        "  - lokal maksimal kobling av konkrete hendelser,",
        "  - og full likhet av hele tilstanden.",
        "",
        "## Hovedfunn",
    ]
    for mode, s in stats["summaries"].items():
        lines.extend([
            f"- `{mode}`:",
            f"  - meeting fraction ≈ {s['meeting_fraction']:.3f}",
            f"  - mean local overlap ≈ {s['mean_avg_local_overlap']:.3f}",
            f"  - same-descriptor rate ≈ {s['mean_same_descriptor_rate']:.3f}",
            f"  - mean unequal time ≈ {s['mean_total_unequal_time']:.3f}",
        ])
    lines.extend([
        "",
        "## Tolkning",
        "Hvis maksimal lokal kobling forbedrer meeting og reduserer unequal time uten å endre marginals, betyr det at v0.6 var metodisk korrekt, men konservativ i hvor mye lokal repair den kunne avdekke.",
        "",
        "## Hvor prosjektet står",
        "Prosjektet er nå i stand til å teste tre ting på en disiplinert måte:",
        "1. om en liten forskjell sprer seg med begrenset radius,",
        "2. om noen regimer også reparerer forskjellen,",
        "3. og om de regimene overlapper med regimer som ser geometri-lignende ut.",
        "",
        "## Neste naturlige steg",
        "- v0.8: fasekart over parameterrommet med meeting, front-hastighet og quasi-invariants i samme kart.",
        "- koble disse regimene til energi- og dimensjonsdiskusjonen.",
        "",
    ])
    return "\n".join(lines)

def make_project_overview_md(args: argparse.Namespace, stats: Dict[str, Any]) -> str:
    return "\n".join([
        "# Prosjektoversikt v0.7",
        "",
        "## Hvor vi startet",
        "",
        "Vi startet med en bakgrunnsløs idé: universet er en dynamisk relasjonsgraf av noder, én relasjonstype, tilfeldighet og units of action.",
        "",
        "## Hva som er bygget så langt",
        "",
        "1. minimale simulatorer for lokal grafdynamikk,",
        "2. energikandidater og invariantanalyse,",
        "3. redusert basis og regelbetingede ΔF-matriser,",
        "4. perturbasjonslab for kausal spredning,",
        "5. uniformisert kobling for åpne regimer,",
        "6. v0.7: lokal maksimal kobling + meeting/survival.",
        "",
        "## Hva vi har lært",
        "",
        "- K og β1 er sentrale i lukkede topologiske sektorer.",
        "- Åpne regimer kan fortsatt gi lesbar kausal struktur, men for mye åpenhet blir fort til drift.",
        "- Bedre lokal kobling kan avdekke repair som grovere koblinger skjuler.",
        "",
        "## Hva dette betyr",
        "",
        "Vi er ikke lenger bare på nivået 'kan denne metafysikken fortelles fint?'. Vi er på nivået 'hvilke regimer i denne modellen ser faktisk ut til å ha begrenset påvirkningsspredning, repair og robust makrostruktur?'.",
        "",
        "## Hvor vi går videre",
        "",
        "Neste fase bør være et eksplisitt fasekart som setter sammen:",
        "- meeting fraction / repair,",
        "- front-hastighet / causal cone,",
        "- quasi-invariants / energi,",
        "- og geometri-proksier som spectral radius, clustering og dim_proxy.",
        "",
    ])

def make_lay_md(stats: Dict[str, Any]) -> str:
    rank = stats["summaries"].get("rank")
    maximal = stats["summaries"].get("maximal")
    lines = [
        "# Forklaring for ikke-spesialister – v0.7",
        "",
        "## Hva vi prøver å finne ut",
        "",
        "Vi prøver å se om en veldig enkel modell av universet kan få frem noe som ligner rom, tid og fartsgrenser bare ved at relasjoner endrer seg lokalt.",
        "",
        "## Hva dette steget gjorde",
        "",
        "Vi tok to nesten like universer og ga dem samme overordnede strøm av mulige hendelser.",
        "Deretter forbedret vi selve metoden som prøver å holde dem så like som mulig lokalt, uten å jukse med sannsynlighetene.",
        "",
        "Det er litt som å spørre:",
        "\"Hvis to nesten like verdener får de samme mulighetene, hvor mye av forskjellen sprer seg, og hvor mye av den reparerer seg selv?\"",
        "",
        "## Hvorfor dette er viktig",
        "",
        "Hvis små forskjeller sprer seg sakte og noen ganger til og med reparerer seg, er det et tegn på at modellen kan ha innebygde regler som ligner kausalitet og stabilitet.",
        "",
    ]
    if rank and maximal:
        lines.extend([
            "## Hva vi fant i denne runden",
            "",
            f"- Med den eldre, grovere koblingen møttes grenene igjen i omtrent {100*rank['meeting_fraction']:.1f}% av testene.",
            f"- Med den nye, skarpere koblingen møttes de igjen i omtrent {100*maximal['meeting_fraction']:.1f}% av testene.",
            f"- Den nye koblingen ga også høyere lokal overlapp mellom de to universgrenene: {rank['mean_avg_local_overlap']:.3f} → {maximal['mean_avg_local_overlap']:.3f}.",
            "",
            "Det betyr ikke at universet vårt er bevist.",
            "Men det betyr at modellen nå har begynt å vise en viktig egenskap: lokale forskjeller ser ikke bare ut til å spre seg; i noen regimer ser de også ut til å kunne 'finne sammen igjen'.",
            "",
        ])
    lines.extend([
        "## Hva dette innebærer",
        "",
        "Vi har nå en modell der vi kan undersøke tre store ting samtidig:",
        "",
        "1. **Spredning:** hvor fort en forskjell kan bre seg.",
        "2. **Reparasjon:** om forskjeller noen ganger forsvinner igjen.",
        "3. **Stabilitet:** om visse mønstre holder seg over tid.",
        "",
        "Hvis de samme regimene gir alle tre, er det et sterkt tegn på at vi nærmer oss noe mer enn bare en filosofisk idé.",
        "",
        "## Hva som kommer nå",
        "",
        "Neste naturlige steg er å lage et kart over parameterrommet og se hvilke deler av modellen som gir best tegn til",
        "- begrenset påvirkningshastighet,",
        "- selvreparasjon,",
        "- og stabile, geometri-lignende mønstre.",
        "",
    ])
    return "\n".join(lines)

def make_readme_md() -> str:
    return "\n".join([
        "# README – v0.7 local maximal coupling lab",
        "",
        "## Filer",
        "- `relational_universe_local_max_coupling_lab.py`: hovedlab for v0.7.",
        "- `*_summary.md`: representative oppsummeringer.",
        "- `*_multirun.csv`: per-seed statistikk.",
        "- `*_multirun_summary.md`: aggregert sammenligning.",
        "",
        "## Eksempelkommandoer",
        "",
        "Representativ kjøring med maksimal lokal kobling:",
        "",
        "```bash",
        "python relational_universe_local_max_coupling_lab.py \\",
        "  --label v07_repr_max \\",
        "  --steps 15000 \\",
        "  --seed 101 \\",
        "  --local-coupling maximal \\",
        "  --out-prefix v07_repr_max",
        "```",
        "",
        "Sammenlign rank og maximal over flere seeds:",
        "",
        "```bash",
        "python relational_universe_local_max_coupling_lab.py \\",
        "  --mode compare \\",
        "  --label v07_compare \\",
        "  --steps 8000 \\",
        "  --multirun-seeds 20 \\",
        "  --out-prefix v07_compare",
        "```",
        "",
        "Kjør verifikasjonssuiten for lokale kjerner og marginals:",
        "",
        "```bash",
        "python relational_universe_local_max_coupling_lab.py \\",
        "  --mode verify \\",
        "  --label v07_verify \\",
        "  --verification-trials 4000 \\",
        "  --verification-event-steps 1200 \\",
        "  --multirun-seeds 12 \\",
        "  --out-prefix v07_verify",
        "```",
        "",
        "## Viktig presisering",
        "",
        "v0.7 gir maksimal kobling av de **endelige lokale overgangskjernene** som faktisk er implementert i denne toy-modellen.",
        "Det er ikke et bevis for global optimalitet av hele CTMC-koblingen.",
        "",
    ])


# ----------------------------
# CLI
# ----------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="v0.7 local maximal coupling lab for the relational-universe toy model.")
    p.add_argument("--mode", type=str, default="single", choices=["single", "compare", "verify"])
    p.add_argument("--label", type=str, default="v0_7_run")
    p.add_argument("--out-prefix", type=str, default="v07_run")

    p.add_argument("--steps", type=int, default=12000)
    p.add_argument("--seed", type=int, default=123)
    p.add_argument("--multirun-seeds", type=int, default=24)

    p.add_argument("--initial-cycle", type=int, default=8)
    p.add_argument("--initial-tokens", type=int, default=4)

    p.add_argument("--r-seed", type=float, default=0.04)
    p.add_argument("--r-token", type=float, default=1.0)
    p.add_argument("--r-birth", type=float, default=0.05)
    p.add_argument("--r-death", type=float, default=0.05)

    p.add_argument("--p-triad", type=float, default=0.0)
    p.add_argument("--p-del", type=float, default=0.0)
    p.add_argument("--p-swap", type=float, default=0.08)

    p.add_argument("--birth-degree-bias", type=float, default=0.5)
    p.add_argument("--death-inverse-degree-scale", type=float, default=1.0)
    p.add_argument("--min-tokens", type=int, default=1)
    p.add_argument("--allow-prune-current-token-node", action="store_true")

    p.add_argument("--perturbation", type=str, default="local_swap", choices=["local_swap", "add_chord"])
    p.add_argument("--center-token-index", type=int, default=0)
    p.add_argument("--local-coupling", type=str, default="maximal", choices=["rank", "maximal"])

    p.add_argument("--log-every", type=int, default=100)
    p.add_argument("--first-hit-rmax", type=int, default=8)
    p.add_argument("--verification-trials", type=int, default=4000)
    p.add_argument("--verification-event-steps", type=int, default=1200)
    p.add_argument("--verification-absorption-steps", type=int, default=400)
    p.add_argument("--verification-absorption-seeds", type=int, default=4)
    p.add_argument("--verification-snapshot-steps", type=int, default=32)
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.mode == "single":
        res = run_single(args)
        log_path = f"{args.out_prefix}_log.csv"
        ev_path = f"{args.out_prefix}_events.csv"
        summary_path = f"{args.out_prefix}_summary.md"
        json_path = f"{args.out_prefix}.json"

        write_csv(log_path, res["log_rows"])
        write_csv(ev_path, res["event_rows"])
        write_text(summary_path, make_single_summary_md(args, res, log_path, ev_path))
        write_json(json_path, {
            "args": res["args"],
            "params": res["params"],
            "perturbation_info": res["perturbation_info"],
            "headline_metrics": res["headline_metrics"],
            "coupling": res["coupling"],
        })
        print(json.dumps({"summary_md": summary_path, "log_csv": log_path, "events_csv": ev_path, "json": json_path}, indent=2))
        return

    if args.mode == "compare":
        seeds = list(range(args.seed, args.seed + args.multirun_seeds))
        stats = collect_multirun_statistics(args, seeds, coupling_modes=["rank", "maximal"])
        csv_path = f"{args.out_prefix}_multirun.csv"
        summary_path = f"{args.out_prefix}_multirun_summary.md"
        status_path = f"{args.out_prefix}_status.md"
        overview_path = f"{args.out_prefix}_overview.md"
        lay_path = f"{args.out_prefix}_lay.md"
        readme_path = f"{args.out_prefix}_README.md"

        write_csv(csv_path, stats["rows"])
        write_text(summary_path, make_multirun_summary_md(args, stats, csv_path))
        write_text(status_path, make_status_md(args, stats))
        write_text(overview_path, make_project_overview_md(args, stats))
        write_text(lay_path, make_lay_md(stats))
        write_text(readme_path, make_readme_md())
        print(json.dumps({
            "multirun_csv": csv_path,
            "multirun_summary_md": summary_path,
            "status_md": status_path,
            "overview_md": overview_path,
            "lay_md": lay_path,
            "readme_md": readme_path,
        }, indent=2))
        return

    if args.mode == "verify":
        report = run_verification_suite(args)
        compare_csv_path = f"{args.out_prefix}_verification_multirun.csv"
        report_md_path = f"{args.out_prefix}_verification.md"
        report_json_path = f"{args.out_prefix}_verification.json"

        write_csv(compare_csv_path, report["compare_stats"]["rows"])
        write_text(report_md_path, make_verification_md(args, report, compare_csv_path))
        write_json(report_json_path, report)
        print(json.dumps({
            "verification_md": report_md_path,
            "verification_json": report_json_path,
            "verification_multirun_csv": compare_csv_path,
        }, indent=2))
        return


if __name__ == "__main__":
    main()
