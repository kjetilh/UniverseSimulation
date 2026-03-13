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
import hashlib
import math
import random
import csv
from collections import Counter, deque
from dataclasses import dataclass
from typing import Dict, FrozenSet, List, Optional, Sequence, Set, Tuple


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

    def copy(self) -> "UGraph":
        cloned = UGraph()
        cloned.adj = {v: set(ns) for v, ns in self.adj.items()}
        return cloned

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

    def edge_list(self) -> List[Tuple[int, int]]:
        return sorted((min(a, b), max(a, b)) for a, ns in self.adj.items() for b in ns if a < b)


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


def triangle_count(g: UGraph) -> int:
    """Count undirected triangles exactly."""
    total = 0
    for v in sorted(g.nodes()):
        upper_neighbors = sorted(u for u in g.neighbors(v) if u > v)
        for i, a in enumerate(upper_neighbors):
            a_neighbors = g.neighbors(a)
            for b in upper_neighbors[i + 1:]:
                if b in a_neighbors:
                    total += 1
    return total


def build_alpha_grid(alpha_min: float, alpha_max: float, alpha_step: float, alpha_grid: Optional[str]) -> Tuple[float, ...]:
    if alpha_grid:
        values = [float(part.strip()) for part in alpha_grid.split(",") if part.strip()]
        if not values:
            raise ValueError("alpha_grid was provided but contained no numeric values")
        return tuple(values)
    if alpha_step <= 0:
        raise ValueError("alpha_step must be > 0")
    if alpha_max < alpha_min:
        raise ValueError("alpha_max must be >= alpha_min")

    values: List[float] = []
    current = alpha_min
    while current <= alpha_max + 1e-12:
        values.append(round(current, 10))
        current += alpha_step
    return tuple(values)


def alpha_label(alpha: float) -> str:
    label = f"{alpha:.6g}"
    label = label.replace("-", "m").replace(".", "p")
    return label


def alpha_column_name(alpha: float) -> str:
    return f"M_minus_alpha_{alpha_label(alpha)}_N"


@dataclass(frozen=True)
class ObservableSample:
    event: int
    time: float
    values: Dict[str, float]


def candidate_quantity_values(s: SimState, alpha_values: Sequence[float]) -> Dict[str, float]:
    n = float(s.g.num_nodes())
    m = float(s.g.num_edges())
    k = float(len(s.tokens))
    triangles = float(triangle_count(s.g))
    values: Dict[str, float] = {
        "K": k,
        "M": m,
        "N": n,
        "T": triangles,
    }
    for alpha in alpha_values:
        values[alpha_column_name(alpha)] = m - alpha * n
    return values


def variance(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    return sum((value - mean) ** 2 for value in values) / len(values)


def drift_per_event(samples: Sequence[ObservableSample], quantity: str) -> float:
    if len(samples) < 2:
        return 0.0
    xs = [float(sample.event) for sample in samples]
    ys = [sample.values[quantity] for sample in samples]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    num = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    den = sum((x - xbar) ** 2 for x in xs)
    return 0.0 if den == 0 else num / den


def metastable_summary_rows(
    samples: Sequence[ObservableSample],
    alpha_values: Sequence[float],
    metastable_start_event: int,
) -> List[Dict[str, float | int | str | None]]:
    alpha_by_quantity = {alpha_column_name(alpha): alpha for alpha in alpha_values}
    quantity_names = ["K", "M", "N", "T", *alpha_by_quantity.keys()]
    rows: List[Dict[str, float | int | str | None]] = []
    for quantity in quantity_names:
        values = [sample.values[quantity] for sample in samples]
        rows.append(
            {
                "quantity": quantity,
                "alpha": alpha_by_quantity.get(quantity),
                "metastable_start_event": metastable_start_event,
                "sample_count": len(samples),
                "mean": (sum(values) / len(values)) if values else 0.0,
                "variance": variance(values),
                "drift_per_event": drift_per_event(samples, quantity),
                "first_value": values[0] if values else 0.0,
                "last_value": values[-1] if values else 0.0,
            }
        )
    return rows


def write_metastable_summary_csv(
    path: str,
    rows: Sequence[Dict[str, float | int | str | None]],
) -> None:
    fieldnames = [
        "quantity",
        "alpha",
        "metastable_start_event",
        "sample_count",
        "mean",
        "variance",
        "drift_per_event",
        "first_value",
        "last_value",
    ]
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


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

    def copy(self) -> "SimState":
        return SimState(
            g=self.g.copy(),
            tokens=list(self.tokens),
            next_node_id=self.next_node_id,
            t=self.t,
            event_count=self.event_count,
        )


@dataclass(frozen=True)
class SharedRNGStream:
    """Stateless keyed RNG for common-random-number coupling across trajectories."""
    seed: int

    def uniform(self, event_index: int, label: str, slot: int = 0) -> float:
        payload = f"{self.seed}:{event_index}:{label}:{slot}".encode("utf-8")
        digest = hashlib.blake2b(payload, digest_size=16).digest()
        value = int.from_bytes(digest[:8], "big") >> 11
        return value / float(1 << 53)

    def choose_index(self, size: int, event_index: int, label: str, slot: int = 0) -> Optional[int]:
        if size <= 0:
            return None
        u = self.uniform(event_index, label, slot)
        return min(int(u * size), size - 1)


@dataclass(frozen=True)
class TokenLocalContext:
    """Snapshot of the radius-2 neighborhood around the traversed edge."""
    token_index: int
    source: int
    destination: int
    traversed_edge: Tuple[int, int]
    radius2_nodes: FrozenSet[int]
    source_neighbors: Tuple[int, ...]
    destination_neighbors: Tuple[int, ...]
    destination_step_candidates: Tuple[int, ...]


class TokenRule:
    name = "token_rule"
    terminal = False

    def probability(self, state: SimState, local_context: TokenLocalContext) -> float:
        raise NotImplementedError

    def apply(self, state: SimState, local_context: TokenLocalContext) -> bool:
        raise NotImplementedError

    def apply_shared(self, state: SimState, local_context: TokenLocalContext, choice_u: float) -> bool:
        return self.apply(state, local_context)


@dataclass(frozen=True)
class DeleteTraversedEdgeRule(TokenRule):
    probability_value: float
    name: str = "delete_traversed_edge"
    terminal: bool = True

    def probability(self, state: SimState, local_context: TokenLocalContext) -> float:
        return self.probability_value

    def apply(self, state: SimState, local_context: TokenLocalContext) -> bool:
        state.g.remove_edge(*local_context.traversed_edge)
        return True


@dataclass(frozen=True)
class TriadicClosureRule(TokenRule):
    probability_value: float
    name: str = "triadic_closure"
    terminal: bool = False

    def probability(self, state: SimState, local_context: TokenLocalContext) -> float:
        if not local_context.destination_step_candidates:
            return 0.0
        return self.probability_value

    def apply(self, state: SimState, local_context: TokenLocalContext) -> bool:
        if not local_context.destination_step_candidates:
            return False
        w = random.choice(local_context.destination_step_candidates)
        state.g.add_edge(local_context.source, w)
        return True

    def apply_shared(self, state: SimState, local_context: TokenLocalContext, choice_u: float) -> bool:
        w = _pick_from_ordered(local_context.destination_step_candidates, choice_u)
        if w is None:
            return False
        state.g.add_edge(local_context.source, w)
        return True


@dataclass(frozen=True)
class LocalRewireRule(TokenRule):
    probability_value: float
    name: str = "local_rewire"
    terminal: bool = False

    def probability(self, state: SimState, local_context: TokenLocalContext) -> float:
        if not local_context.destination_step_candidates:
            return 0.0
        return self.probability_value

    def apply(self, state: SimState, local_context: TokenLocalContext) -> bool:
        if not local_context.destination_step_candidates:
            return False
        w = random.choice(local_context.destination_step_candidates)
        state.g.remove_edge(*local_context.traversed_edge)
        state.g.add_edge(local_context.source, w)
        return True

    def apply_shared(self, state: SimState, local_context: TokenLocalContext, choice_u: float) -> bool:
        w = _pick_from_ordered(local_context.destination_step_candidates, choice_u)
        if w is None:
            return False
        state.g.remove_edge(*local_context.traversed_edge)
        state.g.add_edge(local_context.source, w)
        return True


@dataclass(frozen=True)
class TokenRuleEngine:
    rules: Tuple[TokenRule, ...]

    def execute(self, state: SimState, local_context: TokenLocalContext) -> None:
        for rule in self.rules:
            probability = max(0.0, min(1.0, rule.probability(state, local_context)))
            if probability == 0.0:
                continue
            if random.random() < probability:
                applied = rule.apply(state, local_context)
                if applied and rule.terminal:
                    return


def _edge_radius_nodes(g: UGraph, a: int, b: int, max_radius: int = 2) -> FrozenSet[int]:
    visited = {a, b}
    frontier = {a, b}
    for _ in range(max_radius):
        nxt = set()
        for v in frontier:
            for u in g.neighbors(v):
                if u not in visited:
                    visited.add(u)
                    nxt.add(u)
        if not nxt:
            break
        frontier = nxt
    return frozenset(visited)


def _pick_from_ordered(values: Sequence[int], u: float) -> Optional[int]:
    if not values:
        return None
    idx = min(int(u * len(values)), len(values) - 1)
    return values[idx]


def build_token_local_context(g: UGraph, token_index: int, source: int, destination: int) -> TokenLocalContext:
    radius2_nodes = _edge_radius_nodes(g, source, destination, max_radius=2)
    source_neighbors = tuple(sorted(w for w in g.neighbors(source) if w in radius2_nodes))
    destination_neighbors = tuple(sorted(w for w in g.neighbors(destination) if w in radius2_nodes))
    destination_step_candidates = tuple(w for w in destination_neighbors if w != source)
    return TokenLocalContext(
        token_index=token_index,
        source=source,
        destination=destination,
        traversed_edge=(source, destination),
        radius2_nodes=radius2_nodes,
        source_neighbors=source_neighbors,
        destination_neighbors=destination_neighbors,
        destination_step_candidates=destination_step_candidates,
    )


def build_token_rule_engine(p: Params) -> TokenRuleEngine:
    return TokenRuleEngine(
        rules=(
            DeleteTraversedEdgeRule(probability_value=p.p_delete_traversed_edge),
            TriadicClosureRule(probability_value=p.p_triadic_closure),
            LocalRewireRule(probability_value=p.p_local_rewire),
        )
    )


def execute_token_rules_shared(
    state: SimState,
    local_context: TokenLocalContext,
    token_rule_engine: TokenRuleEngine,
    shared_rng: SharedRNGStream,
    event_index: int,
) -> None:
    for rule_idx, rule in enumerate(token_rule_engine.rules):
        probability = max(0.0, min(1.0, rule.probability(state, local_context)))
        if probability == 0.0:
            continue
        gate_u = shared_rng.uniform(event_index, f"rule_gate:{rule.name}", slot=rule_idx)
        if gate_u >= probability:
            continue
        choice_u = shared_rng.uniform(event_index, f"rule_choice:{rule.name}", slot=rule_idx)
        applied = rule.apply_shared(state, local_context, choice_u)
        if applied and rule.terminal:
            return


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


def gillespie_step(s: SimState, p: Params, token_rule_engine: TokenRuleEngine) -> None:
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
        token_event(s, token_rule_engine)
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


def gillespie_step_shared(
    s: SimState,
    p: Params,
    token_rule_engine: TokenRuleEngine,
    shared_rng: SharedRNGStream,
    event_index: int,
) -> None:
    g = s.g
    n_tok = len(s.tokens)

    R_token = p.r_token * n_tok
    R_seed = p.r_seed if (g.num_nodes() > 0 and g.num_nodes() < p.max_nodes and g.num_edges() < p.max_edges) else 0.0
    R_birth = p.r_token_birth if (g.num_nodes() > 0) else 0.0
    R_death = p.r_token_death * n_tok
    R = R_token + R_seed + R_birth + R_death
    if R > 0.0:
        time_u = shared_rng.uniform(event_index, "gillespie_time")
        selector_u = shared_rng.uniform(event_index, "gillespie_selector")
        s.t += -math.log(max(time_u, 1e-12)) / R
        x = selector_u * R
        if x < R_token:
            token_event_shared(s, token_rule_engine, shared_rng, event_index)
        elif x < R_token + R_seed:
            seed_event_shared(s, p, shared_rng, event_index)
        elif x < R_token + R_seed + R_birth:
            token_birth_event_shared(s, shared_rng, event_index)
        else:
            token_death_event_shared(s, shared_rng, event_index)

    removed = g.prune_isolated()
    if removed:
        if p.relocate_tokens_on_prune:
            survivors = sorted(g.nodes())
            if survivors:
                relocated: List[int] = []
                for idx, v in enumerate(s.tokens):
                    if v in g.adj:
                        relocated.append(v)
                        continue
                    w = _pick_from_ordered(
                        survivors,
                        shared_rng.uniform(event_index, "prune_relocate", slot=idx),
                    )
                    if w is not None:
                        relocated.append(w)
                s.tokens = relocated
            else:
                s.tokens = []
        else:
            s.tokens = [v for v in s.tokens if v in g.adj]

    s.event_count += 1


def token_event(s: SimState, token_rule_engine: TokenRuleEngine) -> None:
    """A token traverses one edge and applies local rules from a radius-2 context."""
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

    local_context = build_token_local_context(g, token_index=i, source=v, destination=u)
    token_rule_engine.execute(s, local_context)


def token_event_shared(
    s: SimState,
    token_rule_engine: TokenRuleEngine,
    shared_rng: SharedRNGStream,
    event_index: int,
) -> None:
    g = s.g
    if not s.tokens or g.num_nodes() == 0:
        return

    token_idx = shared_rng.choose_index(len(s.tokens), event_index, "token_index")
    if token_idx is None:
        return
    v = s.tokens[token_idx]
    if v not in g.adj:
        rv = _pick_from_ordered(sorted(g.nodes()), shared_rng.uniform(event_index, "invalid_token_relocation"))
        if rv is not None:
            s.tokens[token_idx] = rv
        return

    u = _pick_from_ordered(sorted(g.neighbors(v)), shared_rng.uniform(event_index, "token_neighbor"))
    if u is None:
        w = _pick_from_ordered(sorted(g.nodes()), shared_rng.uniform(event_index, "isolated_reattach"))
        if w is not None and w != v:
            g.add_edge(v, w)
        return

    s.tokens[token_idx] = u
    local_context = build_token_local_context(g, token_index=token_idx, source=v, destination=u)
    execute_token_rules_shared(s, local_context, token_rule_engine, shared_rng, event_index)


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


def seed_event_shared(s: SimState, p: Params, shared_rng: SharedRNGStream, event_index: int) -> None:
    g = s.g
    if g.num_nodes() == 0 or g.num_nodes() >= p.max_nodes:
        return

    attach = None
    if s.tokens:
        token_idx = shared_rng.choose_index(len(s.tokens), event_index, "seed_attach_token")
        if token_idx is not None:
            attach = s.tokens[token_idx]
            if attach not in g.adj:
                attach = None
    if attach is None:
        attach = _pick_from_ordered(sorted(g.nodes()), shared_rng.uniform(event_index, "seed_attach_node"))
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


def token_birth_event_shared(s: SimState, shared_rng: SharedRNGStream, event_index: int) -> None:
    v = _pick_from_ordered(sorted(s.g.nodes()), shared_rng.uniform(event_index, "token_birth_node"))
    if v is not None:
        s.tokens.append(v)


def token_death_event(s: SimState) -> None:
    if s.tokens:
        s.tokens.pop(random.randrange(len(s.tokens)))


def token_death_event_shared(s: SimState, shared_rng: SharedRNGStream, event_index: int) -> None:
    token_idx = shared_rng.choose_index(len(s.tokens), event_index, "token_death_index")
    if token_idx is not None:
        s.tokens.pop(token_idx)


def graph_edge_set(g: UGraph) -> Set[Tuple[int, int]]:
    return set(g.edge_list())


def token_counts(tokens: Sequence[int]) -> Counter[int]:
    return Counter(tokens)


def diff_support_nodes(
    base_state: SimState,
    perturbed_state: SimState,
) -> Tuple[Set[int], int, int]:
    edges_a = graph_edge_set(base_state.g)
    edges_b = graph_edge_set(perturbed_state.g)
    edge_delta = edges_a.symmetric_difference(edges_b)

    affected_nodes: Set[int] = set()
    for a, b in edge_delta:
        affected_nodes.add(a)
        affected_nodes.add(b)

    node_delta = set(base_state.g.nodes()).symmetric_difference(perturbed_state.g.nodes())
    affected_nodes.update(node_delta)

    token_a = token_counts(base_state.tokens)
    token_b = token_counts(perturbed_state.tokens)
    token_delta_nodes = 0
    for node in set(token_a) | set(token_b):
        if token_a[node] != token_b[node]:
            affected_nodes.add(node)
            token_delta_nodes += 1

    return affected_nodes, len(edge_delta), token_delta_nodes


def union_graph_adjacency(g1: UGraph, g2: UGraph) -> Dict[int, Set[int]]:
    adj: Dict[int, Set[int]] = {}
    for g in (g1, g2):
        for v, ns in g.adj.items():
            adj.setdefault(v, set()).update(ns)
            for u in ns:
                adj.setdefault(u, set()).add(v)
    return adj


def bfs_distances(adj: Dict[int, Set[int]], sources: Sequence[int]) -> Dict[int, int]:
    dist: Dict[int, int] = {}
    q: deque[int] = deque()
    for src in sources:
        if src in dist:
            continue
        dist[src] = 0
        q.append(src)
        adj.setdefault(src, set())
    while q:
        v = q.popleft()
        for u in adj.get(v, ()):
            if u in dist:
                continue
            dist[u] = dist[v] + 1
            q.append(u)
    return dist


def spread_radius(
    source_nodes: Sequence[int],
    affected_nodes: Set[int],
    base_state: SimState,
    perturbed_state: SimState,
) -> int:
    if not affected_nodes:
        return 0
    adj = union_graph_adjacency(base_state.g, perturbed_state.g)
    dist = bfs_distances(adj, source_nodes)
    reachable = [dist[node] for node in affected_nodes if node in dist]
    return max(reachable) if reachable else 0


def apply_local_perturbation(
    state: SimState,
    perturbation: str,
    perturb_rng: SharedRNGStream,
) -> Tuple[Set[int], str]:
    g = state.g
    if perturbation == "move_token":
        if not state.tokens:
            return set(), "move_token:no_tokens"
        token_idx = perturb_rng.choose_index(len(state.tokens), 0, "perturb_token")
        if token_idx is None:
            return set(), "move_token:no_token_index"
        v = state.tokens[token_idx]
        if v not in g.adj:
            return set(), f"move_token:token_{token_idx}_invalid"
        u = _pick_from_ordered(sorted(g.neighbors(v)), perturb_rng.uniform(0, "perturb_token_neighbor"))
        if u is None:
            return set(), f"move_token:token_{token_idx}_isolated"
        state.tokens[token_idx] = u
        return {v, u}, f"move_token:index={token_idx},from={v},to={u}"

    # default: remove one local edge near a token if possible, else any edge
    if state.tokens:
        token_idx = perturb_rng.choose_index(len(state.tokens), 0, "perturb_token")
        if token_idx is not None:
            v = state.tokens[token_idx]
            if v in g.adj:
                u = _pick_from_ordered(sorted(g.neighbors(v)), perturb_rng.uniform(0, "perturb_edge_neighbor"))
                if u is not None:
                    g.remove_edge(v, u)
                    return {v, u}, f"remove_edge:token={token_idx},edge=({min(v, u)},{max(v, u)})"

    edges = g.edge_list()
    edge_idx = perturb_rng.choose_index(len(edges), 0, "perturb_edge_fallback")
    if edge_idx is None:
        return set(), "remove_edge:no_edges"
    a, b = edges[edge_idx]
    g.remove_edge(a, b)
    return {a, b}, f"remove_edge:fallback=({a},{b})"


def run_coupled(
    steps: int,
    warmup_steps: int,
    seed: int,
    params: Params,
    out_csv: Optional[str],
    perturbation: str,
) -> None:
    random.seed(seed)
    reference = init_state()
    token_rule_engine = build_token_rule_engine(params)
    for _ in range(warmup_steps):
        gillespie_step(reference, params, token_rule_engine)

    base_state = reference.copy()
    perturbed_state = reference.copy()
    shared_rng = SharedRNGStream(seed=seed)
    perturb_support, perturbation_desc = apply_local_perturbation(
        perturbed_state,
        perturbation=perturbation,
        perturb_rng=SharedRNGStream(seed=seed ^ 0x5DEECE66D),
    )
    if not perturb_support:
        raise RuntimeError(f"Failed to apply perturbation: {perturbation_desc}")

    fieldnames = [
        "event",
        "base_time",
        "perturbed_time",
        "base_nodes",
        "perturbed_nodes",
        "base_edges",
        "perturbed_edges",
        "base_tokens",
        "perturbed_tokens",
        "affected_nodes",
        "affected_edges",
        "affected_token_nodes",
        "spread_radius",
        "running_spread_radius",
        "instantaneous_speed",
        "avg_speed",
        "c_star_estimate",
    ]
    writer = None
    f = None
    if out_csv:
        f = open(out_csv, "w", newline="", encoding="utf-8")
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

    running_radius = spread_radius(perturb_support, perturb_support, base_state, perturbed_state)
    prev_running_radius = running_radius
    c_star_estimate = 0.0

    print(
        {
            "mode": "coupled",
            "warmup_steps": warmup_steps,
            "perturbation": perturbation_desc,
            "initial_support": sorted(perturb_support),
        }
    )

    for coupled_event in range(1, steps + 1):
        gillespie_step_shared(base_state, params, token_rule_engine, shared_rng, coupled_event)
        gillespie_step_shared(perturbed_state, params, token_rule_engine, shared_rng, coupled_event)

        affected_nodes, affected_edges, affected_token_nodes = diff_support_nodes(base_state, perturbed_state)
        radius_now = spread_radius(perturb_support, affected_nodes, base_state, perturbed_state)
        running_radius = max(running_radius, radius_now)
        instantaneous_speed = running_radius - prev_running_radius
        avg_speed = running_radius / coupled_event
        c_star_estimate = max(c_star_estimate, instantaneous_speed, avg_speed)

        row = dict(
            event=coupled_event,
            base_time=base_state.t,
            perturbed_time=perturbed_state.t,
            base_nodes=base_state.g.num_nodes(),
            perturbed_nodes=perturbed_state.g.num_nodes(),
            base_edges=base_state.g.num_edges(),
            perturbed_edges=perturbed_state.g.num_edges(),
            base_tokens=len(base_state.tokens),
            perturbed_tokens=len(perturbed_state.tokens),
            affected_nodes=len(affected_nodes),
            affected_edges=affected_edges,
            affected_token_nodes=affected_token_nodes,
            spread_radius=radius_now,
            running_spread_radius=running_radius,
            instantaneous_speed=instantaneous_speed,
            avg_speed=avg_speed,
            c_star_estimate=c_star_estimate,
        )
        if coupled_event % params.log_every_events == 0 or coupled_event == 1 or coupled_event == steps:
            print(row)
        if writer:
            writer.writerow(row)
        prev_running_radius = running_radius

    if f:
        f.close()

    print(
        {
            "mode": "coupled_summary",
            "perturbation": perturbation_desc,
            "max_radius": running_radius,
            "c_star_estimate": c_star_estimate,
            "base_time": base_state.t,
            "perturbed_time": perturbed_state.t,
        }
    )


# ---------------------------
# Run / log
# ---------------------------

def run(
    steps: int,
    seed: int,
    params: Params,
    out_csv: Optional[str],
    alpha_values: Sequence[float],
    metastable_start_event: int,
    metastable_summary_out: Optional[str],
) -> None:
    random.seed(seed)
    s = init_state()
    token_rule_engine = build_token_rule_engine(params)
    metastable_samples: List[ObservableSample] = []

    fieldnames = [
        "event",
        "time",
        "nodes",
        "edges",
        "tokens",
        "K",
        "M",
        "N",
        "T",
        "avg_degree",
        "clustering",
        "eff_dim",
        *(alpha_column_name(alpha) for alpha in alpha_values),
    ]
    writer = None
    f = None
    if out_csv:
        f = open(out_csv, "w", newline="", encoding="utf-8")
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

    for step_idx in range(steps):
        gillespie_step(s, params, token_rule_engine)

        should_log = (
            s.event_count % params.log_every_events == 0
            or step_idx == steps - 1
            or s.g.num_edges() >= params.max_edges
        )
        if should_log:
            g = s.g
            n = g.num_nodes()
            m = g.num_edges()
            avg_deg = 2.0 * m / n if n else 0.0
            cl = approx_clustering(g, sample=params.sample_for_metrics)
            dim = approx_effective_dimension(g, sample_roots=20, r_max=params.max_radius_for_dim)
            candidate_values = candidate_quantity_values(s, alpha_values)

            row = dict(
                event=s.event_count,
                time=s.t,
                nodes=n,
                edges=m,
                tokens=len(s.tokens),
                K=candidate_values["K"],
                M=candidate_values["M"],
                N=candidate_values["N"],
                T=candidate_values["T"],
                avg_degree=avg_deg,
                clustering=cl,
                eff_dim=dim,
            )
            row.update(candidate_values)
            print(row)
            if writer:
                writer.writerow(row)
            if s.event_count >= metastable_start_event:
                metastable_samples.append(
                    ObservableSample(
                        event=s.event_count,
                        time=s.t,
                        values=candidate_values,
                    )
                )

        if s.g.num_edges() >= params.max_edges:
            print("Reached max_edges; stopping.")
            break

    if f:
        f.close()

    summary_rows = metastable_summary_rows(
        metastable_samples,
        alpha_values=alpha_values,
        metastable_start_event=metastable_start_event,
    )
    print(
        {
            "mode": "metastable_summary",
            "metastable_start_event": metastable_start_event,
            "sample_count": len(metastable_samples),
            "quantities": summary_rows,
        }
    )
    if metastable_summary_out:
        write_metastable_summary_csv(metastable_summary_out, summary_rows)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Relational universe graph-rewrite simulator (toy model).")
    ap.add_argument("--mode", choices=("single", "coupled"), default="single")
    ap.add_argument("--steps", type=int, default=80_000)
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--out", type=str, default="trajectory.csv", help="CSV output path (use empty string to disable).")
    ap.add_argument("--metastable-summary-out", type=str, default="", help="Optional CSV path for metastable drift/variance summary.")
    ap.add_argument("--metastable-start-event", type=int, default=-1, help="First logged event to include in metastable drift/variance analysis; default is half the run.")
    ap.add_argument("--alpha-grid", type=str, default="", help="Comma-separated alpha grid for M-alpha*N candidates, e.g. '0.5,1.0,1.5'.")
    ap.add_argument("--alpha-min", type=float, default=0.0, help="Minimum alpha if --alpha-grid is not set.")
    ap.add_argument("--alpha-max", type=float, default=4.0, help="Maximum alpha if --alpha-grid is not set.")
    ap.add_argument("--alpha-step", type=float, default=0.5, help="Step size for auto-generated alpha grid.")
    ap.add_argument("--coupled-out", type=str, default="coupled_trajectory.csv", help="CSV output path for coupled-run diagnostics.")
    ap.add_argument("--warmup-steps", type=int, default=0, help="Run this many single-trajectory steps before cloning the coupled pair.")
    ap.add_argument("--perturbation", choices=("remove_edge", "move_token"), default="remove_edge")

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
    alpha_values = build_alpha_grid(
        alpha_min=args.alpha_min,
        alpha_max=args.alpha_max,
        alpha_step=args.alpha_step,
        alpha_grid=args.alpha_grid.strip() or None,
    )
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
    if args.mode == "coupled":
        coupled_out = args.coupled_out if args.coupled_out.strip() else None
        run_coupled(
            steps=args.steps,
            warmup_steps=args.warmup_steps,
            seed=args.seed,
            params=p,
            out_csv=coupled_out,
            perturbation=args.perturbation,
        )
        return

    out_csv = args.out if args.out.strip() else None
    metastable_start_event = args.metastable_start_event if args.metastable_start_event >= 0 else max(args.log_every, args.steps // 2)
    metastable_summary_out = args.metastable_summary_out if args.metastable_summary_out.strip() else None
    run(
        steps=args.steps,
        seed=args.seed,
        params=p,
        out_csv=out_csv,
        alpha_values=alpha_values,
        metastable_start_event=metastable_start_event,
        metastable_summary_out=metastable_summary_out,
    )


if __name__ == "__main__":
    main()
