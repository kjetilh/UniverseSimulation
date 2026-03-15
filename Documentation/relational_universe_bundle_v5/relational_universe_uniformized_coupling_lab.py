
#!/usr/bin/env python3
"""relational_universe_uniformized_coupling_lab.py

v0.6 adaptive familywise uniformization / coupling laboratory for the
relational-universe toy model.

Purpose
-------
Extend v0.5 perturbation analysis to *open* regimes where token birth/death
changes the total event rate. We do this with a shared dominating event clock
("familywise uniformization") so that two nearby replicas can still be driven
by the same potential-event stream.

Core construction
-----------------
For each branch X in {A,B}, define family rates lambda_f^X for event families
f in {seed, token, birth, death}. At each step, use the dominating family rates

    mu_f = max(lambda_f^A, lambda_f^B)

and total dominating rate

    M = sum_f mu_f.

Sample a potential event time dt ~ Exp(M), choose family f with probability
mu_f / M, then thin independently *conditional on the shared family* using a
common uniform U:

    accept_X iff U < lambda_f^X / mu_f.

Within the accepted family we use common random numbers / rank coupling for
local choices. This preserves exact branch marginals while maximizing agreement
at the family-acceptance level for Bernoulli accept/reject.

This lab is still a toy model, but it is a cleaner way to discuss causal spread
in open sectors than the fixed-rate shared-SSA coupling used in v0.5.
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


# ----------------------------
# Features / combinatorics
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

def approx_clustering(g: UGraph, sample: int = 200, rng: Optional[random.Random] = None) -> float:
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
    rng = rng or random.Random(0)
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
    token_pos: Dict[int, int]
    t: float = 0.0

    def clone(self) -> "State":
        return State(g=self.g.clone(), token_pos=dict(self.token_pos), t=self.t)

    def sorted_token_ids(self) -> List[int]:
        return sorted(self.token_pos.keys())

    def token_count(self) -> int:
        return len(self.token_pos)


def feature_row(state: State, rng: Optional[random.Random] = None) -> Dict[str, float]:
    g = state.g
    return {
        "tokens": float(state.token_count()),
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


# ----------------------------
# Initialization / perturbations
# ----------------------------

def bootstrap(initial_cycle: int, initial_tokens: int, rng: random.Random) -> Tuple[State, int, int]:
    g = UGraph()
    initial_cycle = max(4, initial_cycle)
    for v in range(initial_cycle):
        g.add_edge(v, (v + 1) % initial_cycle)
    token_pos = {tid: rng.randrange(initial_cycle) for tid in range(max(1, initial_tokens))}
    state = State(g=g, token_pos=token_pos, t=0.0)
    next_node_id = initial_cycle
    next_token_id = max(1, initial_tokens)
    return state, next_node_id, next_token_id

def choose_center_token(state: State, center_token_index: int) -> Tuple[int, int, int]:
    tids = state.sorted_token_ids()
    tid = tids[center_token_index % len(tids)]
    v = state.token_pos[tid]
    ns = sorted(state.g.neighbors(v))
    if not ns:
        raise ValueError("Center token sits on isolated node; bootstrap impossible.")
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
    support = sorted({v, u, w})
    return {
        "type": "local_swap",
        "support": support,
        "delta_core": {"tokens": 0, "nodes": 0, "components": 0, "beta1": 0},
    }

def apply_chord_perturbation(state: State, center_token_index: int = 0) -> Dict[str, Any]:
    v, u, w = choose_center_token(state, center_token_index)
    state.g.add_edge(v, w)
    support = sorted({v, u, w})
    return {
        "type": "add_chord",
        "support": support,
        "delta_core": {"tokens": 0, "nodes": 0, "components": 0, "beta1": +1},
    }

def apply_perturbation(state: State, perturbation: str, center_token_index: int) -> Dict[str, Any]:
    if perturbation == "local_swap":
        return apply_local_swap_perturbation(state, center_token_index)
    if perturbation == "add_chord":
        return apply_chord_perturbation(state, center_token_index)
    raise ValueError(f"Unknown perturbation: {perturbation}")


# ----------------------------
# Dynamics
# ----------------------------

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

def choose_by_rank(seq: Sequence[int], u: float) -> Optional[int]:
    if not seq:
        return None
    idx = min(int(u * len(seq)), len(seq) - 1)
    return seq[idx]

def relocate_tokens_from_dead_node(token_pos: Dict[int, int], dead_node: int, destination: int) -> None:
    for tid, node in list(token_pos.items()):
        if node == dead_node:
            token_pos[tid] = destination


def choose_weighted_by_u(items: Sequence[int], weights: Sequence[float], u: float) -> Optional[int]:
    if not items:
        return None
    total = float(sum(max(0.0, w) for w in weights))
    if total <= 0.0:
        return choose_by_rank(items, u)
    target = u * total
    acc = 0.0
    last_item = items[-1]
    for item, w in zip(items, weights):
        acc += max(0.0, float(w))
        if target <= acc:
            return item
    return last_item

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

def seed_anchor(state: State, u_anchor: float) -> Optional[int]:
    tids = state.sorted_token_ids()
    if tids:
        tid = choose_by_rank(tids, u_anchor)
        assert tid is not None
        return state.token_pos[tid]
    nodes = sorted(state.g.nodes())
    return choose_by_rank(nodes, u_anchor)

def apply_seed(state: State, new_node_id: int, u_anchor: float) -> Dict[str, Any]:
    host = seed_anchor(state, u_anchor)
    if host is None:
        return {"event": "seed_reject", "reason": "no_host"}
    state.g.add_edge(new_node_id, host)
    return {"event": "seed", "host": host, "new_node": new_node_id}

def apply_token_move(
    state: State,
    params: Params,
    u_token: float,
    u_neighbor: float,
    u_rule: float,
    u_candidate: float,
) -> Dict[str, Any]:
    tids = state.sorted_token_ids()
    if not tids:
        return {"event": "token_reject", "reason": "no_tokens"}
    tid = choose_by_rank(tids, u_token)
    assert tid is not None
    v = state.token_pos[tid]
    neigh = sorted(state.g.neighbors(v))
    if not neigh:
        return {"event": "stuck", "token_id": tid, "node_before": v}
    u = choose_by_rank(neigh, u_neighbor)
    assert u is not None
    deg_v_before = state.g.degree(v)
    deg_u_before = state.g.degree(u)

    state.token_pos[tid] = u
    ctx: Dict[str, Any] = {
        "event": "move",
        "token_id": tid,
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
        if params.forbid_pruning_current_token_node and deg_u_before <= 1:
            return ctx
        state.g.remove_edge(v, u)
        if state.g.degree(v) == 0:
            relocate_tokens_from_dead_node(state.token_pos, v, u)
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
        ctx.update({"event": "triad", "w_before": w})
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
            relocate_tokens_from_dead_node(state.token_pos, u, v)
            state.g.remove_node(u)
            ctx["pruned_u"] = u
        ctx.update({"event": "swap", "w_before": w})
        return ctx

    return ctx

def apply_birth(state: State, params: Params, new_token_id: int, u_host: float) -> Dict[str, Any]:
    tids = state.sorted_token_ids()
    if tids:
        bw = birth_weights(state, params)
        items = tids
        weights = [bw[tid] for tid in items]
        host_tid = choose_weighted_by_u(items, weights, u_host)
        assert host_tid is not None
        host_node = state.token_pos[host_tid]
        state.token_pos[new_token_id] = host_node
        return {"event": "birth", "host_token": host_tid, "new_token_id": new_token_id, "node": host_node}
    nodes = sorted(state.g.nodes())
    node = choose_by_rank(nodes, u_host)
    if node is None:
        return {"event": "birth_reject", "reason": "no_host"}
    state.token_pos[new_token_id] = node
    return {"event": "birth", "host_token": None, "new_token_id": new_token_id, "node": node}

def apply_death(state: State, params: Params, u_token: float) -> Dict[str, Any]:
    tids = state.sorted_token_ids()
    if len(tids) <= params.min_tokens - 1:
        return {"event": "death_reject", "reason": "below_min"}
    if len(tids) <= params.min_tokens:
        return {"event": "death_reject", "reason": "at_min"}
    dw = death_weights(state, params)
    items = tids
    weights = [dw[tid] for tid in items]
    tid = choose_weighted_by_u(items, weights, u_token)
    assert tid is not None
    node = state.token_pos.pop(tid)
    return {"event": "death", "token_id": tid, "node": node}


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


def coupled_step(
    control: State,
    perturbed: State,
    manager: PairManager,
    rng: random.Random,
    params: Params,
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

    # common random numbers for local arguments
    u_anchor = rng.random()
    u_token = rng.random()
    u_neighbor = rng.random()
    u_rule = rng.random()
    u_candidate = rng.random()

    ctx_c: Dict[str, Any] = {"event": "null"}
    ctx_p: Dict[str, Any] = {"event": "null"}

    if family == "seed":
        new_node_id = manager.alloc_node_id()
        if accept_c:
            ctx_c = apply_seed(control, new_node_id, u_anchor)
        if accept_p:
            ctx_p = apply_seed(perturbed, new_node_id, u_anchor)

    elif family == "token":
        if accept_c:
            ctx_c = apply_token_move(control, params, u_token, u_neighbor, u_rule, u_candidate)
        if accept_p:
            ctx_p = apply_token_move(perturbed, params, u_token, u_neighbor, u_rule, u_candidate)

    elif family == "birth":
        new_token_id = manager.alloc_token_id()
        if accept_c:
            ctx_c = apply_birth(control, params, new_token_id, u_anchor)
        if accept_p:
            ctx_p = apply_birth(perturbed, params, new_token_id, u_anchor)

    elif family == "death":
        if accept_c:
            ctx_c = apply_death(control, params, u_token)
        if accept_p:
            ctx_p = apply_death(perturbed, params, u_token)

    return {
        "family": family,
        "dt": dt,
        "rates_control": rates_c,
        "rates_perturbed": rates_p,
        "mu": mu,
        "M": M,
        "accept_control": accept_c,
        "accept_perturbed": accept_p,
        "control": ctx_c,
        "perturbed": ctx_p,
    }


# ----------------------------
# Damage / divergence metrics
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
        out.add(a); out.add(b)
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

def l1_feature_difference(control: State, perturbed: State, keys: Sequence[str]) -> float:
    fc = feature_row(control)
    fp = feature_row(perturbed)
    return float(sum(abs(fp[k] - fc[k]) for k in keys))

def core_feature_difference(control: State, perturbed: State) -> Dict[str, float]:
    fc = feature_row(control)
    fp = feature_row(perturbed)
    return {k: fp[k] - fc[k] for k in FEATURE_NAMES}

def damage_snapshot(control: State, perturbed: State, support: Sequence[int]) -> Dict[str, Any]:
    d_edges = edge_symmetric_difference(control, perturbed)
    d_nodes = damaged_nodes(control, perturbed)
    r_ctrl = radius_from_support(control.g, support, d_nodes)
    r_pert = radius_from_support(perturbed.g, support, d_nodes)
    nearest_ctrl = nearest_damage_distance(control.g, support, d_nodes)
    nearest_pert = nearest_damage_distance(perturbed.g, support, d_nodes)
    diff = core_feature_difference(control, perturbed)
    shared_tokens = set(control.token_pos.keys()).intersection(perturbed.token_pos.keys())
    token_hamming = sum(1 for tid in shared_tokens if control.token_pos[tid] != perturbed.token_pos[tid])
    token_sym = len(set(control.token_pos.keys()).symmetric_difference(perturbed.token_pos.keys()))
    return {
        "edge_diff_count": len(d_edges),
        "node_diff_count": len(node_symmetric_difference(control, perturbed)),
        "damaged_nodes_count": len(d_nodes),
        "token_hamming_shared": token_hamming,
        "token_id_symdiff": token_sym,
        "radius_control": -1 if r_ctrl is None else int(r_ctrl),
        "radius_perturbed": -1 if r_pert is None else int(r_pert),
        "nearest_control": -1 if nearest_ctrl is None else int(nearest_ctrl),
        "nearest_perturbed": -1 if nearest_pert is None else int(nearest_pert),
        "core_l1": sum(abs(diff[k]) for k in ("tokens", "nodes", "components", "beta1")),
        "regime_l1": l1_feature_difference(control, perturbed, ["wedges", "triangles", "star3", "c4", "spectral_radius", "clustering", "dim_proxy"]),
        "delta_tokens": diff["tokens"],
        "delta_nodes": diff["nodes"],
        "delta_components": diff["components"],
        "delta_beta1": diff["beta1"],
        "delta_triangles": diff["triangles"],
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
            if out[r] is None:
                out[r] = t
    return out

def summarize_coupling(event_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    fams = ["seed", "token", "birth", "death"]
    out: Dict[str, Any] = {
        "total_potential_events": len(event_rows),
        "both_accept_total": 0,
        "one_sided_total": 0,
        "null_total": 0,
        "family": {},
    }
    for f in fams:
        sub = [r for r in event_rows if r["family"] == f]
        both = sum(1 for r in sub if r["accept_control"] and r["accept_perturbed"])
        one = sum(1 for r in sub if (r["accept_control"] != r["accept_perturbed"]))
        null = sum(1 for r in sub if (not r["accept_control"] and not r["accept_perturbed"]))
        out["both_accept_total"] += both
        out["one_sided_total"] += one
        out["null_total"] += null
        out["family"][f] = {
            "potential": len(sub),
            "both_accept": both,
            "one_sided": one,
            "null": null,
        }
    return out

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
    coupling = summarize_coupling(event_rows)

    rows = [["metric", "value"]]
    for k, v in report_json["headline_metrics"].items():
        rows.append([k, f"{v}"])
    headline_table = markdown_table(rows)

    fam_rows = [["family", "potential", "both_accept", "one_sided", "null"]]
    for fam, sub in coupling["family"].items():
        fam_rows.append([fam, str(sub["potential"]), str(sub["both_accept"]), str(sub["one_sided"]), str(sub["null"])])
    fam_table = markdown_table(fam_rows)

    hit_rows = [["radius", "first_hit_time_control"]]
    for r in range(args.first_hit_rmax + 1):
        t = hit_ctrl[r]
        hit_rows.append([str(r), "NA" if t is None else f"{t:.6g}"])
    hit_table = markdown_table(hit_rows)

    sections = [
        f"# Uniformized coupling lab: {args.label}",
        "",
        "## Formål",
        "",
        "Dette v0.6-steget utvider kausalitetslaben til åpne regimer der token-antallet kan endre seg.",
        "I v0.5 var en eksakt felles Gillespie-klokke bare ren når token-antallet var identisk og konstant i begge grener.",
        "I v0.6 bruker vi i stedet en dominerende felles potensial-hendelsesprosess og familywise thinning.",
        "",
        "## Kjøringsparametre",
        "",
        f"- steps: {args.steps}",
        f"- seed: {args.seed}",
        f"- initial_cycle: {args.initial_cycle}",
        f"- initial_tokens: {args.initial_tokens}",
        f"- r_seed: {args.r_seed}",
        f"- r_token: {args.r_token}",
        f"- r_birth: {args.r_birth}",
        f"- r_death: {args.r_death}",
        f"- p_triad: {args.p_triad}",
        f"- p_del: {args.p_del}",
        f"- p_swap: {args.p_swap}",
        f"- min_tokens: {args.min_tokens}",
        f"- perturbation: {args.perturbation}",
        f"- center_token_index: {args.center_token_index}",
        "",
        "## Startperturbasjon",
        "",
        "```json",
        json.dumps(perturbation_info, indent=2, sort_keys=True),
        "```",
        "",
        "## Hovedfunn fra kjøringen",
        "",
        headline_table,
        "",
        "## Kvalitet på koblingen",
        "",
        f"- totale potensial-hendelser: {coupling['total_potential_events']}",
        f"- begge aksepterte: {coupling['both_accept_total']}",
        f"- ensidige aksepter: {coupling['one_sided_total']}",
        f"- dobbelt-null: {coupling['null_total']}",
        "",
        fam_table,
        "",
        "## Front-hastigheter",
        "",
        f"- control: max(r/t) = {speed_ctrl['max_ratio']:.6g}, lineær fit-slope = {speed_ctrl['fit_slope']:.6g}",
        f"- perturbed: max(r/t) = {speed_pert['max_ratio']:.6g}, lineær fit-slope = {speed_pert['fit_slope']:.6g}",
        "",
        "## Første treff per radius",
        "",
        hit_table,
        "",
        "## Tolkning",
        "",
        "Familywise uniformization gjør det mulig å beholde én delt potensial-klokke selv når totalratene i de to grenene er ulike.",
        "Dermed kan vi skille mellom virkelig kausal spredning og ren klokke-deskronisering.",
        "",
        "I åpne regimer er det fortsatt mulig at forskjeller i tokens, noder eller topologi vokser raskt.",
        "Poenget i v0.6 er ikke å bevise universell causal cone én gang for alle, men å gjøre testen metodisk legitim i de regimene der v0.5 ikke lenger var tilstrekkelig.",
        "",
        "## Hva som er nytt i dette steget",
        "",
        "1. Token birth/death er nå eksplisitt inne i perturbasjonslaben.",
        "2. Eventtid er koblet via en dominerende felles potensial-hendelsesstrøm.",
        "3. Familywise thinning og felles uniforms gir maksimal samsvar på aksept-beslutningen for hver valgt familie.",
        "4. Node- og token-id-er bevares over grenene når hendelser deles, slik at divergens kan måles meningsfullt.",
        "",
        "## Begrensninger",
        "",
        "- Koblingen er eksakt på familywise-rate-nivå, men ikke nødvendigvis maksimal for hele den lokale overgangskjernen.",
        "- Rank-kobling for lokale valg er enkel og robust, men ikke den eneste mulige eller nødvendigvis optimale koblingen.",
        "- Vi må senere undersøke om front-hastighet blir robust under andre lokale koblingsvalg.",
        "",
        "## Neste naturlige steg",
        "",
        "- Bygg en mer finmasket maksimal kobling for lokale overganger innen hver familie.",
        "- Studer om det finnes en stabil overgrense for front-hastighet over et større parameterrom.",
        "- Koble v0.6-laben til dimensjons- og energidiskusjonen: er det de samme regimene som gir quasi-invariants, stabil geometri og begrenset spredning?",
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
        "# Hvor vi er nå – forklart enkelt",
        "",
        "## Hva problemet var",
        "",
        "I forrige steg kunne vi sammenligne to nesten like universgrener bare så lenge de hadde like mange action-bærere (tokens).",
        "Men så snart en gren fikk flere eller færre tokens enn den andre, begynte de å 'gå på ulike klokker'.",
        "Da ble det uklart om forskjeller spredte seg fordi modellen hadde ekte kausalitet, eller bare fordi vi sammenlignet to systemer som ikke lenger fikk hendelser samtidig.",
        "",
        "## Hva vi har gjort nå",
        "",
        "Vi bygde derfor en ny metode med en felles overordnet klokke.",
        "Ved hver mulig hendelse trekker vi først hvilken type hendelse som kunne skje, og så avgjør vi om den faktisk skjer i den ene grenen, den andre, begge eller ingen.",
        "",
        "Det gjør at begge universgrenene fortsatt lever under samme overordnede 'vær', selv når de lokalt utvikler seg litt forskjellig.",
        "",
        "## Hvorfor dette er viktig",
        "",
        "Nå kan vi teste om en liten lokal forskjell sprer seg utover gradvis, også i mer realistiske og åpne regimer der antall action-bærere kan vokse og krympe.",
        "",
        "## Hva en representativ kjøring viste",
        "",
        f"- skadefronten endte på radius {hm['final_radius_control']} i kontrollgeometrien",
        f"- forskjellen i kantstruktur endte på {hm['final_edge_diff_count']} kanter",
        f"- antall tokens mellom grenene skilte seg til slutt med {hm['final_delta_tokens']}",
        f"- den estimerte effektive front-hastigheten i kontrollgrenen var omtrent {hm['fit_speed_control']:.4g}",
        "",
        "Dette er fortsatt ikke en fysisk lov. Det er en laboratoriemåling inne i modellen.",
        "Men det er et viktig steg fordi testen nå er mye renere enn før.",
        "",
        "## Hva dette betyr i praksis",
        "",
        "Vi er nå kommet til et punkt der prosjektet ikke bare spør om modellen kan lage stabile mønstre, men også om den kan lage en innebygd grense for hvor fort påvirkning sprer seg.",
        "",
        "Hvis det holder seg gjennom flere tester, er det et signal om at noe relativitet-lignende kan vokse frem av modellen i stedet for å bli lagt inn utenfra.",
        "",
        "## Hva som kommer etterpå",
        "",
        "- forbedre selve koblingen slik at den blir enda skarpere",
        "- kartlegge hvilke parameterregimer som gir best tegn til lyskjegle-lignende oppførsel",
        "- koble dette til energidiskusjonen og til spørsmålet om hvordan romdimensjoner kan dukke opp",
        "",
    ])


# ----------------------------
# Main
# ----------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Uniformized coupling lab for open relational-universe regimes.")
    p.add_argument("--label", type=str, default="v0_6_run")
    p.add_argument("--steps", type=int, default=20000)
    p.add_argument("--seed", type=int, default=123)
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

    p.add_argument("--token-open-topologically-closed", action="store_true",
                   help="Preset: seed + swap + birth + death.")
    p.add_argument("--full-open", action="store_true",
                   help="Preset: seed + triad + delete + swap + birth + death.")

    p.add_argument("--perturbation", type=str, default="local_swap", choices=["local_swap", "add_chord"])
    p.add_argument("--center-token-index", type=int, default=0)
    p.add_argument("--log-every", type=int, default=50)
    p.add_argument("--first-hit-rmax", type=int, default=8)

    p.add_argument("--out-log-csv", type=str, default="uniformized_coupling_log.csv")
    p.add_argument("--out-events-csv", type=str, default="uniformized_coupling_events.csv")
    p.add_argument("--out-summary-md", type=str, default="uniformized_coupling_summary.md")
    p.add_argument("--out-lay-md", type=str, default="uniformized_coupling_lay_summary.md")
    p.add_argument("--out-json", type=str, default="uniformized_coupling_report.json")
    return p

def apply_presets(args: argparse.Namespace) -> None:
    if args.token_open_topologically_closed:
        args.p_triad = 0.0
        args.p_del = 0.0
        args.p_swap = max(args.p_swap, 0.08)
        args.r_birth = max(args.r_birth, 0.05)
        args.r_death = max(args.r_death, 0.05)
        args.birth_degree_bias = max(args.birth_degree_bias, 0.75)
        args.death_inverse_degree_scale = max(args.death_inverse_degree_scale, 1.0)
    if args.full_open:
        args.p_triad = max(args.p_triad, 0.10)
        args.p_del = max(args.p_del, 0.06)
        args.p_swap = max(args.p_swap, 0.08)
        args.r_birth = max(args.r_birth, 0.08)
        args.r_death = max(args.r_death, 0.06)
        args.birth_degree_bias = max(args.birth_degree_bias, 0.75)
        args.death_inverse_degree_scale = max(args.death_inverse_degree_scale, 1.0)

def main() -> None:
    args = build_parser().parse_args()
    apply_presets(args)

    rng = random.Random(args.seed)
    base, next_node_id, next_token_id = bootstrap(args.initial_cycle, args.initial_tokens, rng)
    control = base.clone()
    perturbed = base.clone()
    perturbation_info = apply_perturbation(perturbed, args.perturbation, args.center_token_index)
    support = perturbation_info["support"]
    manager = PairManager(next_node_id=next_node_id, next_token_id=next_token_id)

    params = Params(
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
    )

    log_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []

    snap0 = damage_snapshot(control, perturbed, support)
    log_rows.append({"step": 0, "t": 0.0, **snap0})

    max_radius_control = max(-1, snap0["radius_control"])
    max_radius_perturbed = max(-1, snap0["radius_perturbed"])

    for step in range(1, args.steps + 1):
        shared = coupled_step(control, perturbed, manager, rng, params)

        event_rows.append({
            "step": step,
            "t": control.t,
            "family": shared["family"],
            "dt": shared["dt"],
            "M": shared.get("M", 0.0),
            "accept_control": int(bool(shared.get("accept_control", False))),
            "accept_perturbed": int(bool(shared.get("accept_perturbed", False))),
            "control_event": shared.get("control", {}).get("event", "null"),
            "perturbed_event": shared.get("perturbed", {}).get("event", "null"),
            "control_tokens": control.token_count(),
            "perturbed_tokens": perturbed.token_count(),
            "control_nodes": control.g.num_nodes(),
            "perturbed_nodes": perturbed.g.num_nodes(),
        })

        if step % args.log_every == 0 or step == args.steps:
            snap = damage_snapshot(control, perturbed, support)
            max_radius_control = max(max_radius_control, snap["radius_control"])
            max_radius_perturbed = max(max_radius_perturbed, snap["radius_perturbed"])
            log_rows.append({"step": step, "t": control.t, **snap})

    final = log_rows[-1]
    speed = estimate_front_speed(log_rows, "t", "radius_control")
    coupling = summarize_coupling(event_rows)

    headline_metrics = {
        "final_t": float(final["t"]),
        "final_radius_control": int(final["radius_control"]),
        "final_radius_perturbed": int(final["radius_perturbed"]),
        "max_radius_control": int(max_radius_control),
        "max_radius_perturbed": int(max_radius_perturbed),
        "final_edge_diff_count": int(final["edge_diff_count"]),
        "final_damaged_nodes_count": int(final["damaged_nodes_count"]),
        "final_delta_tokens": float(final["delta_tokens"]),
        "final_delta_beta1": float(final["delta_beta1"]),
        "final_core_l1": float(final["core_l1"]),
        "final_regime_l1": float(final["regime_l1"]),
        "fit_speed_control": float(speed["fit_slope"]),
        "both_accept_total": int(coupling["both_accept_total"]),
        "one_sided_total": int(coupling["one_sided_total"]),
        "null_total": int(coupling["null_total"]),
    }

    report = {
        "label": args.label,
        "params": vars(args),
        "perturbation_info": perturbation_info,
        "headline_metrics": headline_metrics,
        "coupling_summary": coupling,
        "first_row": log_rows[0],
        "last_row": final,
    }

    with open(args.out_log_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(log_rows[0].keys()))
        writer.writeheader()
        writer.writerows(log_rows)

    with open(args.out_events_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(event_rows[0].keys()) if event_rows else ["step"])
        writer.writeheader()
        if event_rows:
            writer.writerows(event_rows)

    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, sort_keys=True)

    with open(args.out_summary_md, "w", encoding="utf-8") as f:
        f.write(make_summary_md(args, log_rows, event_rows, perturbation_info, report, args.out_log_csv, args.out_events_csv))

    with open(args.out_lay_md, "w", encoding="utf-8") as f:
        f.write(make_lay_summary_md(report, args))

    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
