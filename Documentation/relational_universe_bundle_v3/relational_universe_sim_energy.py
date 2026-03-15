#!/usr/bin/env python3
"""relational_universe_sim_energy.py

Extension of relational_universe_sim.py with explicit candidate "energy" functionals
and diagnostics for exact / local / emergent (quasi-)conservation.

This is a *toy* sandbox aligned with your ontology:
  - One node type
  - One relation type (undirected edge)
  - Units of action are local rewrite events (here implemented via mobile "tokens")
  - Randomness selects events (continuous-time SSA / Gillespie)

The point is not to reproduce real cosmology, but to keep us honest:
given a small local rewrite rule-set, we can test what kinds of invariants exist
and whether something energy-like emerges as a robust macrovariable.

Pure Python 3.10+.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from dataclasses import dataclass
from typing import Dict, Set, List, Optional, Tuple


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


def count_components(g: UGraph) -> int:
    """Number of connected components."""
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


def is_bridge(g: UGraph, a: int, b: int, bfs_cap: Optional[int] = None) -> bool:
    """Heuristic bridge test by reachability when ignoring edge (a,b)."""
    if not g.has_edge(a, b):
        return False
    q = [a]
    seen = {a}
    explored = 0
    while q:
        v = q.pop()
        explored += 1
        if bfs_cap is not None and explored > bfs_cap:
            # if we abort early, treat as non-bridge to avoid freezing dynamics
            return False
        for u in g.neighbors(v):
            if (v == a and u == b) or (v == b and u == a):
                continue
            if u == b:
                return False
            if u not in seen:
                seen.add(u)
                q.append(u)
    return True


def beta1_cycle_rank(g: UGraph) -> int:
    """β1 = |E| - |V| + C (cycle rank / first Betti number of a graph)."""
    return g.num_edges() - g.num_nodes() + count_components(g)


def stress_energy(g: UGraph, d0: float) -> float:
    """E_stress = Σ_v (deg(v) - d0)^2."""
    return float(sum((g.degree(v) - d0) ** 2 for v in g.nodes()))


def approx_clustering(g: UGraph, sample: int = 200) -> float:
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


def bfs_ball_set(g: UGraph, root: int, r_max: int) -> Set[int]:
    """Return the node set B(root,r_max)."""
    visited = {root}
    frontier = {root}
    for _ in range(r_max):
        nxt = set()
        for v in frontier:
            for u in g.neighbors(v):
                if u not in visited:
                    visited.add(u)
                    nxt.add(u)
        frontier = nxt
        if not frontier:
            break
    return visited


def approx_effective_dimension(g: UGraph, sample_roots: int = 20, r_max: int = 6) -> float:
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


@dataclass
class Params:
    # event rates
    r_token: float = 1.0
    r_seed: float = 0.05

    # local rewrites per token step
    p_delete_traversed_edge: float = 0.02
    p_triadic_closure: float = 0.10
    p_local_rewire: float = 0.05

    # optional token birth/death
    r_token_birth: float = 0.0
    r_token_death: float = 0.0

    relocate_tokens_on_prune: bool = False

    # connectivity preservation
    avoid_disconnect: bool = False
    bridge_bfs_cap: Optional[int] = 50_000

    max_nodes: int = 50_000
    max_edges: int = 200_000

    log_every_events: int = 500
    sample_for_metrics: int = 200
    max_radius_for_dim: int = 6

    # energy
    d0_for_stress: float = 4.0
    w_tokens: float = 1.0
    w_beta1: float = 1.0
    w_stress: float = 0.0
    check_exact_energy: bool = False
    check_energy_eps: float = 1e-9

    # local conservation test (tokens only, on a *fixed* initial region)
    local_region_radius: int = 0


@dataclass
class SimState:
    g: UGraph
    tokens: List[int]
    next_node_id: int
    t: float = 0.0
    event_count: int = 0

    # Optional fixed region A ⊂ V for local conservation bookkeeping.
    region_A: Optional[Set[int]] = None
    region_E0: int = 0
    region_flux_in: int = 0
    region_flux_out: int = 0
    region_births_in: int = 0
    region_deaths_in: int = 0
    region_prune_drops_in: int = 0
    region_reloc_in: int = 0
    region_reloc_out: int = 0


def init_state(n0: int = 30, m0: int = 60, tokens0: int = 10) -> SimState:
    g = UGraph()
    for i in range(n0):
        g.add_node(i)
    for i in range(n0):
        g.add_edge(i, (i + 1) % n0)
    attempts = 0
    while g.num_edges() < m0 and attempts < 20 * m0:
        a = random.randrange(n0)
        b = random.randrange(n0)
        g.add_edge(a, b)
        attempts += 1
    nodes = g.nodes()
    tokens = [random.choice(nodes) for _ in range(tokens0)]
    return SimState(g=g, tokens=tokens, next_node_id=n0)


def energy_functionals(s: SimState, p: Params) -> Tuple[float, int, float, float]:
    """Return (E_total, beta1, E_stress, E_tokens)."""
    g = s.g
    e_tok = float(len(s.tokens))
    b1 = beta1_cycle_rank(g)
    e_st = stress_energy(g, p.d0_for_stress) if p.w_stress != 0.0 else 0.0
    e_tot = p.w_tokens * e_tok + p.w_beta1 * float(b1) + p.w_stress * e_st
    return e_tot, b1, e_st, e_tok


def gillespie_step(s: SimState, p: Params) -> None:
    g = s.g
    n_tok = len(s.tokens)

    R_token = p.r_token * n_tok
    R_seed = p.r_seed if (g.num_nodes() > 0 and g.num_nodes() < p.max_nodes and g.num_edges() < p.max_edges) else 0.0
    R_birth = p.r_token_birth if g.num_nodes() > 0 else 0.0
    R_death = p.r_token_death * n_tok
    R = R_token + R_seed + R_birth + R_death
    if R <= 0.0:
        return

    if p.check_exact_energy:
        e_before, _, _, _ = energy_functionals(s, p)
    else:
        e_before = 0.0

    u = random.random()
    s.t += -math.log(max(u, 1e-12)) / R

    x = random.random() * R
    if x < R_token:
        token_event(s, p)
    elif x < R_token + R_seed:
        seed_event(s)
    elif x < R_token + R_seed + R_birth:
        token_birth_event(s)
    else:
        token_death_event(s)

    removed = g.prune_isolated()
    if removed:
        # We need per-token handling to keep correct local-conservation bookkeeping.
        region = s.region_A
        survivors = g.nodes()
        new_tokens: List[int] = []
        for v in s.tokens:
            if v in g.adj:
                new_tokens.append(v)
                continue

            # token sat on a node that was pruned
            in_region = (region is not None and v in region)
            if p.relocate_tokens_on_prune and survivors:
                nv = random.choice(survivors)
                new_tokens.append(nv)
                if region is not None:
                    in_after = nv in region
                    if in_region and not in_after:
                        s.region_reloc_out += 1
                    elif (not in_region) and in_after:
                        s.region_reloc_in += 1
                # if both in/out same, no net local effect
            else:
                # drop token (open system)
                if in_region:
                    s.region_prune_drops_in += 1
        s.tokens = new_tokens

    s.event_count += 1

    if p.check_exact_energy:
        e_after, _, _, _ = energy_functionals(s, p)
        if abs(e_after - e_before) > p.check_energy_eps:
            raise RuntimeError(
                f"Energy not conserved at event {s.event_count}: {e_before} -> {e_after} (Δ={e_after-e_before})."
            )


def token_event(s: SimState, p: Params) -> None:
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
        w = g.random_node()
        if w is not None and w != v:
            g.add_edge(v, w)
        return

    # traverse v -> u
    region = s.region_A
    if region is not None:
        in_before = v in region
        in_after = u in region
        if in_before and not in_after:
            s.region_flux_out += 1
        elif (not in_before) and in_after:
            s.region_flux_in += 1

    s.tokens[i] = u

    # delete traversed edge
    if random.random() < p.p_delete_traversed_edge:
        if (not p.avoid_disconnect) or (not is_bridge(g, v, u, bfs_cap=p.bridge_bfs_cap)):
            g.remove_edge(v, u)
        return

    # triadic closure
    if random.random() < p.p_triadic_closure:
        candidates = [w for w in g.neighbors(u) if w != v]
        if candidates:
            w = random.choice(candidates)
            g.add_edge(v, w)

    # local rewire
    if random.random() < p.p_local_rewire:
        # IMPORTANT: to make this a true "edge swap" (|E| preserved), we must
        # avoid choosing w such that edge (v,w) already exists. Otherwise we
        # can remove (v,u) and fail to add a *new* edge, decreasing |E|.
        candidates = [w for w in g.neighbors(u) if w != v and not g.has_edge(v, w)]
        if candidates:
            w = random.choice(candidates)
            if (not p.avoid_disconnect) or (not is_bridge(g, v, u, bfs_cap=p.bridge_bfs_cap)):
                g.remove_edge(v, u)
                g.add_edge(v, w)


def seed_event(s: SimState) -> None:
    g = s.g
    if g.num_nodes() == 0:
        return
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
    v = s.g.random_node()
    if v is not None:
        s.tokens.append(v)
        if s.region_A is not None and v in s.region_A:
            s.region_births_in += 1


def token_death_event(s: SimState) -> None:
    if not s.tokens:
        return
    i = random.randrange(len(s.tokens))
    v = s.tokens[i]
    if s.region_A is not None and v in s.region_A:
        s.region_deaths_in += 1
    s.tokens.pop(i)


def linear_regression_slope(xs: List[float], ys: List[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        return float("nan")
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    num = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    den = sum((x - xbar) ** 2 for x in xs)
    return float("nan") if den == 0 else num / den


def run(steps: int, seed: int, params: Params, out_csv: Optional[str]) -> None:
    random.seed(seed)
    s = init_state()

    # Fixed local region for token conservation bookkeeping.
    if params.local_region_radius > 0 and s.g.num_nodes() > 0:
        anchor = s.tokens[0] if s.tokens else s.g.random_node()
        if anchor is not None:
            s.region_A = bfs_ball_set(s.g, anchor, params.local_region_radius)
            s.region_E0 = sum(1 for v in s.tokens if v in s.region_A)

    fieldnames = [
        "event",
        "time",
        "nodes",
        "edges",
        "components",
        "tokens",
        "beta1",
        "E_tokens",
        "E_stress",
        "E_total",
        "avg_degree",
        "clustering",
        "eff_dim",
        # local token conservation diagnostics
        "region_tokens",
        "region_tokens_pred",
        "region_residual",
    ]
    writer = None
    f = None
    if out_csv:
        f = open(out_csv, "w", newline="", encoding="utf-8")
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

    ts: List[float] = []
    Es: List[float] = []

    for _ in range(steps):
        gillespie_step(s, params)

        if s.event_count % params.log_every_events == 0:
            g = s.g
            n = g.num_nodes()
            m = g.num_edges()
            c = count_components(g)
            avg_deg = 2.0 * m / n if n else 0.0
            cl = approx_clustering(g, sample=params.sample_for_metrics)
            dim = approx_effective_dimension(g, sample_roots=20, r_max=params.max_radius_for_dim)
            e_total, b1, e_stress, e_tok = energy_functionals(s, params)

            # local token conservation (fixed region A)
            if s.region_A is None:
                region_tokens = float("nan")
                region_pred = float("nan")
                region_resid = float("nan")
            else:
                region_tokens = sum(1 for v in s.tokens if v in s.region_A)
                region_pred = (
                    s.region_E0
                    + (s.region_flux_in - s.region_flux_out)
                    + (s.region_births_in - s.region_deaths_in)
                    + (s.region_reloc_in - s.region_reloc_out)
                    - s.region_prune_drops_in
                )
                region_resid = region_tokens - region_pred

            row = dict(
                event=s.event_count,
                time=s.t,
                nodes=n,
                edges=m,
                components=c,
                tokens=len(s.tokens),
                beta1=b1,
                E_tokens=e_tok,
                E_stress=e_stress,
                E_total=e_total,
                avg_degree=avg_deg,
                clustering=cl,
                eff_dim=dim,
                region_tokens=region_tokens,
                region_tokens_pred=region_pred,
                region_residual=region_resid,
            )
            print(row)
            if writer:
                writer.writerow(row)
            ts.append(s.t)
            Es.append(e_total)

        if s.g.num_edges() >= params.max_edges:
            print("Reached max_edges; stopping.")
            break

    if f:
        f.close()

    if len(ts) >= 5:
        slope = linear_regression_slope(ts, Es)
        ebar = sum(Es) / len(Es)
        print("\nQuasi-conservation diagnostic (logged samples):")
        print(f"  slope dE/dt ≈ {slope:.6g}")
        print(f"  mean(E)     ≈ {ebar:.6g}")
        print(f"  relative drift per unit time ≈ {slope / (abs(ebar) + 1e-12):.6g}")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Relational universe simulator with energy diagnostics (toy model).")
    ap.add_argument("--steps", type=int, default=80_000)
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--out", type=str, default="trajectory_energy.csv")

    ap.add_argument("--r-token", type=float, default=1.0)
    ap.add_argument("--r-seed", type=float, default=0.05)
    ap.add_argument("--r-birth", type=float, default=0.0)
    ap.add_argument("--r-death", type=float, default=0.0)

    ap.add_argument("--p-del", type=float, default=0.02)
    ap.add_argument("--p-triad", type=float, default=0.10)
    ap.add_argument("--p-rewire", type=float, default=0.05)

    ap.add_argument("--relocate-tokens", action="store_true")
    ap.add_argument("--avoid-disconnect", action="store_true")
    ap.add_argument("--bridge-cap", type=int, default=50_000)

    ap.add_argument("--log-every", type=int, default=500)
    ap.add_argument("--sample", type=int, default=200)
    ap.add_argument("--rmax", type=int, default=6)
    ap.add_argument("--max-nodes", type=int, default=50_000)
    ap.add_argument("--max-edges", type=int, default=200_000)

    ap.add_argument("--d0", type=float, default=4.0)
    ap.add_argument("--w-tokens", type=float, default=1.0)
    ap.add_argument("--w-beta1", type=float, default=1.0)
    ap.add_argument("--w-stress", type=float, default=0.0)
    ap.add_argument("--check-exact", action="store_true")
    ap.add_argument("--check-eps", type=float, default=1e-9)

    ap.add_argument(
        "--local-radius",
        type=int,
        default=0,
        help=(
            "If >0, define a fixed initial region A as the BFS ball of this radius "
            "around the first token, and log exact token-count continuity in that region."
        ),
    )

    ap.add_argument(
        "--closed",
        action="store_true",
        help=(
            "Preset: closed-ish dynamics (no edge add/delete, no token birth/death), "
            "avoid disconnect on, relocate tokens. Useful for studying exact invariants like β1."
        ),
    )
    return ap.parse_args()


def main() -> None:
    args = parse_args()

    if args.closed:
        args.p_del = 0.0
        args.p_triad = 0.0
        args.r_birth = 0.0
        args.r_death = 0.0
        args.avoid_disconnect = True
        args.relocate_tokens = True

    p = Params(
        r_token=args.r_token,
        r_seed=args.r_seed,
        p_delete_traversed_edge=args.p_del,
        p_triadic_closure=args.p_triad,
        p_local_rewire=args.p_rewire,
        r_token_birth=args.r_birth,
        r_token_death=args.r_death,
        relocate_tokens_on_prune=args.relocate_tokens,
        avoid_disconnect=args.avoid_disconnect,
        bridge_bfs_cap=args.bridge_cap,
        log_every_events=args.log_every,
        sample_for_metrics=args.sample,
        max_radius_for_dim=args.rmax,
        max_nodes=args.max_nodes,
        max_edges=args.max_edges,
        d0_for_stress=args.d0,
        w_tokens=args.w_tokens,
        w_beta1=args.w_beta1,
        w_stress=args.w_stress,
        check_exact_energy=args.check_exact,
        check_energy_eps=args.check_eps,
        local_region_radius=args.local_radius,
    )

    out_csv = args.out if args.out.strip() else None
    run(steps=args.steps, seed=args.seed, params=p, out_csv=out_csv)


if __name__ == "__main__":
    main()
