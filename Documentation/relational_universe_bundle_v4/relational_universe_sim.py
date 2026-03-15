#!/usr/bin/env python3
"""
relational_universe_sim.py

Minimal stochastic simulation of a "relational universe" as a dynamic undirected graph.

Core primitives (matching your ontology):
  - Nodes (information-bearing units)
  - One relation type (edges)
  - Units of action (events) that are local rewrites
  - Randomness (stochastic choice of which event occurs)

Implementation choice:
  - We represent "units of action" as mobile agents ("tokens") that:
        (i) traverse an existing relation
       (ii) optionally perform a *local* rewrite near the traversed relation
    This is an implementation device: the *ontology* still has only nodes+relations+events.

Scheduling:
  - Continuous-time stochastic simulation (Gillespie-style SSA) to avoid a privileged global tick.
    This is the same family of ideas used in rule-based stochastic simulators such as KaSim for Kappa models.  (See docs.)

What you can test with this sandbox:
  - Does a large connected component persist under local stochastic rewrites?
  - Do loops/triangles/metastable "particles" appear?
  - Under what rules do you see approximate invariants (conservation-like quantities)?
  - Coarse geometry proxies: clustering, volume growth, effective dimension proxy.

No external dependencies (pure Python 3.10+).
"""
from __future__ import annotations

import argparse
import math
import random
import csv
from dataclasses import dataclass
from typing import Dict, Set, List, Optional


# ---------------------------
# Graph data structure
# ---------------------------

class UGraph:
    """Simple undirected graph with integer node ids and adjacency sets."""
    def __init__(self) -> None:
        self.adj: Dict[int, Set[int]] = {}

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
        return len(self.neighbors(v))

    def nodes(self) -> List[int]:
        return list(self.adj.keys())

    def num_nodes(self) -> int:
        return len(self.adj)

    def num_edges(self) -> int:
        return sum(len(ns) for ns in self.adj.values()) // 2

    def random_node(self) -> Optional[int]:
        if not self.adj:
            return None
        return random.choice(self.nodes())

    def random_neighbor(self, v: int) -> Optional[int]:
        ns = list(self.neighbors(v))
        if not ns:
            return None
        return random.choice(ns)

    def prune_isolated(self) -> List[int]:
        """Remove nodes with degree 0. Return removed node ids."""
        removed: List[int] = []
        for v in list(self.adj.keys()):
            if len(self.adj[v]) == 0:
                self.remove_node(v)
                removed.append(v)
        return removed


# ---------------------------
# Parameters
# ---------------------------

@dataclass
class Params:
    # Event rates (continuous time)
    r_token: float = 1.0            # per-token action rate
    r_seed: float = 0.05            # global seed attachment rate

    # Local rewrite probabilities conditioned on a token step
    p_delete_traversed_edge: float = 0.02
    p_triadic_closure: float = 0.10
    p_local_rewire: float = 0.05

    # Optional token birth/death (set to 0.0 for token-count conservation)
    r_token_birth: float = 0.0
    r_token_death: float = 0.0

    # "Operational existence": if True, tokens on pruned nodes are relocated (keeps token count);
    # if False, they are removed (open-system energy-like quantity).
    relocate_tokens_on_prune: bool = False

    # Safety caps (avoid explosive densification in toy runs)
    max_nodes: int = 50_000
    max_edges: int = 200_000

    # Logging / metrics
    log_every_events: int = 500
    sample_for_metrics: int = 200
    max_radius_for_dim: int = 6


# ---------------------------
# Coarse metrics (cheap-ish)
# ---------------------------

def approx_clustering(g: UGraph, sample: int = 200) -> float:
    """Approximate average local clustering coefficient by sampling nodes."""
    vs = g.nodes()
    if not vs:
        return 0.0
    if len(vs) > sample:
        vs = random.sample(vs, sample)
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


def bfs_ball_volumes(g: UGraph, root: int, r_max: int) -> List[int]:
    """Return |B(root,r)| for r=0..r_max using BFS layers."""
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


def approx_effective_dimension(g: UGraph, sample_roots: int = 20, r_max: int = 6) -> float:
    """
    Rough effective dimension proxy via volume growth:
      V(r) ~ r^d  => d ~ slope of log V vs log r  (for r>=2)
    """
    if g.num_nodes() < 50:
        return float("nan")
    roots = g.nodes()
    if len(roots) > sample_roots:
        roots = random.sample(roots, sample_roots)
    vols = [0.0] * (r_max + 1)
    for rt in roots:
        br = bfs_ball_volumes(g, rt, r_max)
        for r, v in enumerate(br):
            vols[r] += v
    vols = [v / len(roots) for v in vols]

    xs: List[float] = []
    ys: List[float] = []
    for r in range(2, r_max + 1):
        if vols[r] <= 0:
            continue
        xs.append(math.log(r))
        ys.append(math.log(vols[r]))
    if len(xs) < 2:
        return float("nan")

    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    num = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    den = sum((x - xbar) ** 2 for x in xs)
    return float("nan") if den == 0 else num / den


# ---------------------------
# Simulation engine (SSA / Gillespie-style)
# ---------------------------

@dataclass
class SimState:
    g: UGraph
    tokens: List[int]
    next_node_id: int
    t: float = 0.0
    event_count: int = 0


def init_state(n0: int = 30, m0: int = 60, tokens0: int = 10) -> SimState:
    g = UGraph()
    for i in range(n0):
        g.add_node(i)
    # base ring ensures connected start
    for i in range(n0):
        g.add_edge(i, (i + 1) % n0)
    # random chords
    attempts = 0
    while g.num_edges() < m0 and attempts < 20 * m0:
        a = random.randrange(n0)
        b = random.randrange(n0)
        g.add_edge(a, b)
        attempts += 1

    nodes = g.nodes()
    tokens = [random.choice(nodes) for _ in range(tokens0)]
    return SimState(g=g, tokens=tokens, next_node_id=n0)


def gillespie_step(s: SimState, p: Params) -> None:
    """
    One stochastic event:
      - token action (move + local rewrite)
      - seed attachment (add node connected to a local site)
      - optional token birth/death
    """
    g = s.g
    n_tok = len(s.tokens)

    R_token = p.r_token * n_tok
    R_seed = p.r_seed if (g.num_nodes() > 0 and g.num_nodes() < p.max_nodes and g.num_edges() < p.max_edges) else 0.0
    R_birth = p.r_token_birth if (g.num_nodes() > 0) else 0.0
    R_death = p.r_token_death * n_tok
    R = R_token + R_seed + R_birth + R_death
    if R <= 0.0:
        return

    # time increment
    u = random.random()
    s.t += -math.log(max(u, 1e-12)) / R

    # choose event
    x = random.random() * R
    if x < R_token:
        token_event(s, p)
    elif x < R_token + R_seed:
        seed_event(s, p)
    elif x < R_token + R_seed + R_birth:
        token_birth_event(s)
    else:
        token_death_event(s)

    removed = g.prune_isolated()
    if removed:
        if p.relocate_tokens_on_prune:
            # relocate tokens that sat on removed nodes to random surviving nodes
            survivors = g.nodes()
            if survivors:
                s.tokens = [v if v in g.adj else random.choice(survivors) for v in s.tokens]
            else:
                s.tokens = []
        else:
            # drop tokens that sat on removed nodes (open-system behaviour)
            s.tokens = [v for v in s.tokens if v in g.adj]

    s.event_count += 1


def token_event(s: SimState, p: Params) -> None:
    """A token traverses one edge and locally rewrites near that edge."""
    g = s.g
    if not s.tokens or g.num_nodes() == 0:
        return

    i = random.randrange(len(s.tokens))
    v = s.tokens[i]
    if v not in g.adj:
        rv = g.random_node()
        if rv is not None:
            s.tokens[i] = rv
        return

    u = g.random_neighbor(v)
    if u is None:
        # attempt to reattach once; otherwise it will be pruned
        w = g.random_node()
        if w is not None and w != v:
            g.add_edge(v, w)
        return

    # traverse v -> u
    s.tokens[i] = u

    # (1) delete traversed edge
    if random.random() < p.p_delete_traversed_edge:
        g.remove_edge(v, u)
        return

    # (2) triadic closure: connect v to a neighbor of u
    if random.random() < p.p_triadic_closure:
        candidates = [w for w in g.neighbors(u) if w != v]
        if candidates:
            w = random.choice(candidates)
            g.add_edge(v, w)

    # (3) local rewire: replace edge (v,u) by (v,w), w near u
    if random.random() < p.p_local_rewire:
        candidates = [w for w in g.neighbors(u) if w != v]
        if candidates:
            w = random.choice(candidates)
            g.remove_edge(v, u)
            g.add_edge(v, w)


def seed_event(s: SimState, p: Params) -> None:
    """Add a new node with a single relation to an existing local site."""
    g = s.g
    if g.num_nodes() == 0 or g.num_nodes() >= p.max_nodes:
        return

    # attach locally: pick a token site if possible
    attach = None
    if s.tokens:
        attach = random.choice(s.tokens)
        if attach not in g.adj:
            attach = None
    if attach is None:
        attach = g.random_node()
    if attach is None:
        return

    new_id = s.next_node_id
    s.next_node_id += 1
    g.add_edge(new_id, attach)


def token_birth_event(s: SimState) -> None:
    g = s.g
    v = g.random_node()
    if v is not None:
        s.tokens.append(v)


def token_death_event(s: SimState) -> None:
    if s.tokens:
        s.tokens.pop(random.randrange(len(s.tokens)))


# ---------------------------
# Run / log
# ---------------------------

def run(
    steps: int,
    seed: int,
    params: Params,
    out_csv: Optional[str],
) -> None:
    random.seed(seed)
    s = init_state()

    fieldnames = [
        "event",
        "time",
        "nodes",
        "edges",
        "tokens",
        "avg_degree",
        "clustering",
        "eff_dim",
    ]
    writer = None
    f = None
    if out_csv:
        f = open(out_csv, "w", newline="", encoding="utf-8")
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

    for _ in range(steps):
        gillespie_step(s, params)

        if s.event_count % params.log_every_events == 0:
            g = s.g
            n = g.num_nodes()
            m = g.num_edges()
            avg_deg = 2.0 * m / n if n else 0.0
            cl = approx_clustering(g, sample=params.sample_for_metrics)
            dim = approx_effective_dimension(g, sample_roots=20, r_max=params.max_radius_for_dim)

            row = dict(
                event=s.event_count,
                time=s.t,
                nodes=n,
                edges=m,
                tokens=len(s.tokens),
                avg_degree=avg_deg,
                clustering=cl,
                eff_dim=dim,
            )
            print(row)
            if writer:
                writer.writerow(row)

        if s.g.num_edges() >= params.max_edges:
            print("Reached max_edges; stopping.")
            break

    if f:
        f.close()


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Relational universe graph-rewrite simulator (toy model).")
    ap.add_argument("--steps", type=int, default=80_000)
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--out", type=str, default="trajectory.csv", help="CSV output path (use empty string to disable).")

    # expose key params
    ap.add_argument("--r-token", type=float, default=1.0)
    ap.add_argument("--r-seed", type=float, default=0.05)
    ap.add_argument("--p-del", type=float, default=0.02, help="P(delete traversed edge | token event)")
    ap.add_argument("--p-triad", type=float, default=0.10, help="P(triadic closure | token event)")
    ap.add_argument("--p-rewire", type=float, default=0.05, help="P(local rewire | token event)")

    ap.add_argument("--r-birth", type=float, default=0.0)
    ap.add_argument("--r-death", type=float, default=0.0)
    ap.add_argument("--relocate-tokens", action="store_true", help="Relocate tokens on pruned nodes (keeps token count).")

    ap.add_argument("--log-every", type=int, default=500)
    ap.add_argument("--sample", type=int, default=200)
    ap.add_argument("--rmax", type=int, default=6)

    ap.add_argument("--max-nodes", type=int, default=50_000)
    ap.add_argument("--max-edges", type=int, default=200_000)
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    p = Params(
        r_token=args.r_token,
        r_seed=args.r_seed,
        p_delete_traversed_edge=args.p_del,
        p_triadic_closure=args.p_triad,
        p_local_rewire=args.p_rewire,
        r_token_birth=args.r_birth,
        r_token_death=args.r_death,
        relocate_tokens_on_prune=args.relocate_tokens,
        log_every_events=args.log_every,
        sample_for_metrics=args.sample,
        max_radius_for_dim=args.rmax,
        max_nodes=args.max_nodes,
        max_edges=args.max_edges,
    )
    out_csv = args.out if args.out.strip() else None
    run(steps=args.steps, seed=args.seed, params=p, out_csv=out_csv)


if __name__ == "__main__":
    main()
