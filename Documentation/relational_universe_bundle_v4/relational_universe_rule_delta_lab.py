
#!/usr/bin/env python3
"""relational_universe_rule_delta_lab.py

Next-step analysis for the relational-universe toy model:
- reduced feature basis
- standardized increments
- rule-conditioned delta-F matrices
- symbolic core invariant classification
- empirical validation of context-dependent delta formulas

This script extends the feature-lab stage with per-event instrumentation.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from dataclasses import dataclass
from typing import Dict, Set, List, Optional, Tuple, Any

try:
    import numpy as np
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"numpy is required for this lab: {exc}")


# ----------------------------
# Basic graph
# ----------------------------

class UGraph:
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
        vs = self.nodes()
        return random.choice(vs) if vs else None

    def random_neighbor(self, v: int) -> Optional[int]:
        ns = list(self.neighbors(v))
        return random.choice(ns) if ns else None

    def prune_isolated(self) -> List[int]:
        removed = []
        for v in list(self.adj.keys()):
            if not self.adj[v]:
                self.remove_node(v)
                removed.append(v)
        return removed


# ----------------------------
# Helpers
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

def is_bridge(g: UGraph, a: int, b: int, bfs_cap: Optional[int] = None) -> bool:
    if not g.has_edge(a, b):
        return False
    q = [a]
    seen = {a}
    explored = 0
    while q:
        v = q.pop()
        explored += 1
        if bfs_cap is not None and explored > bfs_cap:
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

def common_neighbors_count(g: UGraph, a: int, b: int) -> int:
    if a not in g.adj or b not in g.adj:
        return 0
    if len(g.adj[a]) < len(g.adj[b]):
        return sum((u in g.adj[b]) for u in g.adj[a])
    return sum((u in g.adj[a]) for u in g.adj[b])

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

def volume_dimension_proxy(g: UGraph, samples: int = 8, r_max: int = 4) -> float:
    vs = g.nodes()
    if len(vs) < 2:
        return 0.0
    roots = vs if len(vs) <= samples else random.sample(vs, samples)
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


# ----------------------------
# State and features
# ----------------------------

@dataclass
class State:
    g: UGraph
    tokens: List[int]
    t: float
    next_node_id: int

def bootstrap(initial_cycle: int, initial_tokens: int) -> State:
    g = UGraph()
    if initial_cycle < 2:
        initial_cycle = 2
    for v in range(initial_cycle):
        g.add_edge(v, (v + 1) % initial_cycle)
    tokens = [random.randrange(initial_cycle) for _ in range(max(1, initial_tokens))]
    return State(g=g, tokens=tokens, t=0.0, next_node_id=initial_cycle)

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

def feature_row(state: State) -> Dict[str, float]:
    g = state.g
    edges = g.num_edges()
    wedges = wedge_count(g)
    row = {
        "t": state.t,
        "tokens": float(len(state.tokens)),
        "nodes": float(g.num_nodes()),
        "edges": float(edges),
        "components": float(count_components(g)),
        "beta1": float(beta1_cycle_rank(g)),
        "wedges": float(wedges),
        "triangles": float(triangle_count(g)),
        "star3": float(star3_count(g)),
        "c4": float(four_cycle_count(g)),
        "deg_sq_sum": float(sum(g.degree(v) ** 2 for v in g.nodes())),
        "spectral_radius": float(adjacency_spectral_radius(g)),
        "clustering": float(approx_clustering(g)),
        "dim_proxy": float(volume_dimension_proxy(g)),
    }
    return row

def reduced_feature_vector(row: Dict[str, float]) -> np.ndarray:
    return np.array([float(row[name]) for name in REDUCED_FEATURES], dtype=float)

def core_feature_vector(row: Dict[str, float]) -> np.ndarray:
    return np.array([float(row[name]) for name in CORE_FEATURES], dtype=float)


# ----------------------------
# Dynamics with instrumentation
# ----------------------------

def remove_or_relocate_tokens(state: State, removed_nodes: List[int], relocate: bool) -> Tuple[int, int]:
    if not removed_nodes:
        return (0, 0)
    removed = set(removed_nodes)
    survivors = state.g.nodes()
    births = 0
    deaths = 0
    new_tokens = []
    for tok in state.tokens:
        if tok in removed:
            if relocate and survivors:
                new_tokens.append(random.choice(survivors))
                births += 1
            else:
                deaths += 1
        else:
            new_tokens.append(tok)
    state.tokens = new_tokens
    return (births, deaths)

def seed_attach(state: State, choose_token_host: bool = True) -> Dict[str, Any]:
    g = state.g
    ctx: Dict[str, Any] = {"event": "seed", "host": None, "host_deg_before": None}
    if g.num_nodes() == 0:
        g.add_node(state.next_node_id)
        state.next_node_id += 1
        return ctx
    if choose_token_host and state.tokens:
        host = random.choice(state.tokens)
    else:
        host = g.random_node()
    if host is None:
        return ctx
    ctx["host"] = host
    ctx["host_deg_before"] = g.degree(host)
    x = state.next_node_id
    state.next_node_id += 1
    g.add_edge(x, host)
    ctx["new_node"] = x
    return ctx

def token_birth(state: State) -> Dict[str, Any]:
    ctx = {"event": "birth"}
    if state.g.num_nodes() == 0:
        return ctx
    state.tokens.append(state.g.random_node())  # type: ignore[arg-type]
    return ctx

def token_death(state: State) -> Dict[str, Any]:
    ctx = {"event": "death"}
    if state.tokens:
        idx = random.randrange(len(state.tokens))
        ctx["dead_token_node"] = state.tokens[idx]
        state.tokens.pop(idx)
    return ctx

def token_event(
    state: State,
    p_triad: float,
    p_del: float,
    p_swap: float,
    avoid_disconnect: bool,
    relocate_tokens: bool,
) -> Dict[str, Any]:
    if not state.tokens:
        return {"event": "noop"}
    tidx = random.randrange(len(state.tokens))
    v = state.tokens[tidx]
    u = state.g.random_neighbor(v)
    if u is None:
        return {"event": "stuck", "token_index": tidx, "v": v}

    g = state.g
    ctx: Dict[str, Any] = {
        "event": "move",
        "token_index": tidx,
        "v_before": v,
        "u_before": u,
        "deg_v_before": g.degree(v),
        "deg_u_before": g.degree(u),
        "bridge_vu_before": bool(is_bridge(g, v, u, bfs_cap=5000)),
        "common_vu_before": common_neighbors_count(g, v, u),
    }

    state.tokens[tidx] = u  # traverse first, then rewrite

    roll = random.random()
    total = p_triad + p_del + p_swap
    if total <= 0:
        return ctx

    if roll < p_del:
        if not avoid_disconnect or not ctx["bridge_vu_before"]:
            g.remove_edge(v, u)
            removed = g.prune_isolated()
            births_from_reloc, deaths_from_prune = remove_or_relocate_tokens(state, removed, relocate_tokens)
            ctx.update({
                "event": "delete",
                "removed_isolated_nodes": len(removed),
                "token_relocations_from_prune": births_from_reloc,
                "token_deaths_from_prune": deaths_from_prune,
            })
            return ctx
        return ctx

    roll -= p_del
    if roll < p_triad:
        cands = [w for w in g.neighbors(u) if w != v and not g.has_edge(v, w)]
        if cands:
            w = random.choice(cands)
            ctx.update({
                "w_before": w,
                "deg_w_before": g.degree(w),
                "common_vw_before": common_neighbors_count(g, v, w),
            })
            g.add_edge(v, w)
            ctx["event"] = "triad"
            return ctx
        return ctx

    roll -= p_triad
    if roll < p_swap:
        cands = [w for w in g.neighbors(u) if w != v and not g.has_edge(v, w)]
        if cands and (not avoid_disconnect or not ctx["bridge_vu_before"]):
            w = random.choice(cands)
            ctx.update({
                "w_before": w,
                "deg_w_before": g.degree(w),
                "common_vw_before": common_neighbors_count(g, v, w),
            })
            g.remove_edge(v, u)
            g.add_edge(v, w)
            removed = g.prune_isolated()
            births_from_reloc, deaths_from_prune = remove_or_relocate_tokens(state, removed, relocate_tokens)
            ctx.update({
                "event": "swap",
                "removed_isolated_nodes": len(removed),
                "token_relocations_from_prune": births_from_reloc,
                "token_deaths_from_prune": deaths_from_prune,
            })
            return ctx
        return ctx

    return ctx

def step(
    state: State,
    r_seed: float,
    r_token: float,
    r_birth: float,
    r_death: float,
    p_triad: float,
    p_del: float,
    p_swap: float,
    avoid_disconnect: bool,
    relocate_tokens: bool,
) -> Dict[str, Any]:
    n_tokens = len(state.tokens)
    channels: List[Tuple[str, float]] = [
        ("seed", max(0.0, r_seed)),
        ("token", max(0.0, r_token) * n_tokens),
        ("birth", max(0.0, r_birth)),
        ("death", max(0.0, r_death)),
    ]
    total = sum(r for _, r in channels)
    if total <= 0:
        return {"event": "noop"}
    dt = random.expovariate(total)
    state.t += dt
    x = random.random() * total
    acc = 0.0
    event = "noop"
    for name, rate in channels:
        acc += rate
        if x <= acc:
            event = name
            break
    if event == "seed":
        return seed_attach(state, choose_token_host=True)
    if event == "birth":
        return token_birth(state)
    if event == "death":
        return token_death(state)
    if event == "token":
        return token_event(
            state,
            p_triad=p_triad,
            p_del=p_del,
            p_swap=p_swap,
            avoid_disconnect=avoid_disconnect,
            relocate_tokens=relocate_tokens,
        )
    return {"event": "noop"}


# ----------------------------
# Symbolic / theoretical core matrices
# ----------------------------

RULESET_LIBRARY: Dict[str, List[str]] = {
    "closed_topological": ["seed", "swap"],
    "open_topological": ["seed", "triad", "delete", "swap"],
    "fully_open_linear": ["seed", "triad", "delete", "swap", "birth", "death"],
}

def core_delta_vector_for_rule(rule: str) -> np.ndarray:
    # Features: [tokens, nodes, components, beta1]
    mapping = {
        "move": np.array([0., 0., 0., 0.]),
        "stuck": np.array([0., 0., 0., 0.]),
        "noop": np.array([0., 0., 0., 0.]),
        "seed": np.array([0., 1., 0., 0.]),
        "birth": np.array([1., 0., 0., 0.]),
        "death": np.array([-1., 0., 0., 0.]),
        "triad": np.array([0., 0., 0., 1.]),
        "delete": np.array([0., 0., 0., -1.]),
        "swap": np.array([0., 0., 0., 0.]),
    }
    return mapping.get(rule, np.zeros(4))

def nullspace_basis(A: np.ndarray, atol: float = 1e-10) -> np.ndarray:
    if A.size == 0:
        return np.eye(0)
    u, s, vh = np.linalg.svd(A, full_matrices=True)
    rank = int((s > atol).sum())
    return vh[rank:].T

def invariant_classification_markdown() -> str:
    lines = [
        "# Symbolsk invariantklassifikasjon i kjernebasis",
        "",
        "Kjernebasis er `F_core = (tokens, nodes, components, beta1)`.",
        "Her betyr `beta1 = edges - nodes + components` grafens første Betti-tall (uavhengige sykluser).",
        "",
        "## Primitive regler og eksakte lineære inkrementer",
        "",
        "| regel | Δtokens | Δnodes | Δcomponents | Δbeta1 | merknad |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    notes = {
        "seed": "Ny bladnode festes til eksisterende komponent.",
        "birth": "Token fødes på eksisterende node.",
        "death": "Token dør.",
        "triad": "Ny kant legges inn mellom to tidligere ikke-adjiserte noder i samme komponent.",
        "delete": "Ikke-bro-kant fjernes i samme komponent.",
        "swap": "En kant fjernes og en annen legges inn; lineært ingen endring i kjernebasis.",
        "move": "Ren traversering uten topologisk omskriving.",
    }
    for rule in ["seed", "birth", "death", "triad", "delete", "swap", "move"]:
        d = core_delta_vector_for_rule(rule)
        lines.append(
            f"| {rule} | {int(d[0])} | {int(d[1])} | {int(d[2])} | {int(d[3])} | {notes[rule]} |"
        )

    lines.extend([
        "",
        "## Nullrom og eksakte lineære invariants",
        "",
        "En lineær kombinasjon `I = c·F_core` er eksakt invariant dersom `ΔF_rule · c = 0` for alle regler i den valgte regelklassen.",
        "",
    ])
    for label, rules in RULESET_LIBRARY.items():
        A = np.vstack([core_delta_vector_for_rule(r) for r in rules])
        basis = nullspace_basis(A)
        pretty = []
        names = CORE_FEATURES
        for j in range(basis.shape[1]):
            col = basis[:, j]
            nz = [f"{col[i]:+.1f}·{names[i]}" for i in range(len(names)) if abs(col[i]) > 1e-9]
            pretty.append(" ".join(nz) if nz else "0")
        lines.append(f"### Regelsett: `{label}`")
        lines.append("")
        lines.append(f"Regler: {', '.join(rules)}")
        lines.append("")
        lines.append(f"Invariantrommets dimensjon: {basis.shape[1]}")
        lines.append("")
        if pretty:
            for p in pretty:
                lines.append(f"- {p}")
        else:
            lines.append("- ingen ikke-trivielle lineære invariants")
        lines.append("")
    lines.extend([
        "## Tolkning",
        "",
        "- I `closed_topological` er `tokens`, `components` og `beta1` eksakte lineære invariants i kjernebasis.",
        "- Hvis man i tillegg arbeider i én fast sammenhengende komponent (`components = 1`), reduseres de ikke-trivielle invariantene til `tokens` og `beta1`.",
        "- I `open_topological` bryter `triad/delete` den eksakte bevaringen av `beta1`, men `tokens` består som invariant så lenge token-birth/death er slått av.",
        "- I `fully_open_linear` er det i praksis bare `components` som gjenstår; i en fast sammenhengende komponent forsvinner dermed alle ikke-trivielle lineære invariants i kjernebasis.",
        "",
        "Dette er den presise lineære klassifikasjonen som tidligere lå implisitt i diskusjonen.",
        "",
    ])
    return "\n".join(lines)


# ----------------------------
# Context-dependent formulas
# ----------------------------

def predict_contextual_delta(ctx: Dict[str, Any], after_minus_before: Dict[str, float]) -> Dict[str, Optional[float]]:
    event = ctx.get("event")
    pred: Dict[str, Optional[float]] = {
        "wedges": None,
        "triangles": None,
        "star3": None,
    }
    if event == "seed":
        h = ctx.get("host_deg_before")
        if h is not None:
            h = int(h)
            pred["wedges"] = float(h)
            pred["triangles"] = 0.0
            pred["star3"] = float(comb2(h))
    elif event == "triad":
        dv = ctx.get("deg_v_before")
        dw = ctx.get("deg_w_before")
        c = ctx.get("common_vw_before")
        if dv is not None and dw is not None and c is not None:
            dv = int(dv); dw = int(dw); c = int(c)
            pred["wedges"] = float(dv + dw)
            pred["triangles"] = float(c)
            pred["star3"] = float(comb2(dv) + comb2(dw))
    elif event == "delete":
        dv = ctx.get("deg_v_before")
        du = ctx.get("deg_u_before")
        c = ctx.get("common_vu_before")
        if dv is not None and du is not None and c is not None:
            dv = int(dv); du = int(du); c = int(c)
            pred["wedges"] = float(-((dv - 1) + (du - 1)))
            pred["triangles"] = float(-c)
            pred["star3"] = float(-(comb2(dv - 1) + comb2(du - 1)))
    elif event == "swap":
        du = ctx.get("deg_u_before")
        dw = ctx.get("deg_w_before")
        c_del = ctx.get("common_vu_before")
        c_add = ctx.get("common_vw_before")
        if du is not None and dw is not None and c_del is not None and c_add is not None:
            du = int(du); dw = int(dw); c_del = int(c_del); c_add = int(c_add)
            pred["wedges"] = float(-(du - 1) + dw)
            pred["triangles"] = float(-c_del + (c_add - 1))
            pred["star3"] = float(-comb2(du - 1) + comb2(dw))
    return pred


# ----------------------------
# Analysis
# ----------------------------

def markdown_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows[1:])
    return "\n".join([header, sep, body])

def summarise_events(event_rows: List[Dict[str, Any]]) -> str:
    rows = [["event", "count"]]
    counts: Dict[str, int] = {}
    for r in event_rows:
        e = str(r["event"])
        counts[e] = counts.get(e, 0) + 1
    for e in sorted(counts):
        rows.append([e, str(counts[e])])
    return markdown_table(rows)

def mean_delta_tables(event_rows: List[Dict[str, Any]]) -> Tuple[str, str]:
    if not event_rows:
        return "", ""
    deltas = np.array([[float(r[f"d_{name}"]) for name in REDUCED_FEATURES] for r in event_rows], dtype=float)
    std = deltas.std(axis=0)
    std[std == 0.0] = 1.0
    groups: Dict[str, List[int]] = {}
    for i, r in enumerate(event_rows):
        groups.setdefault(str(r["event"]), []).append(i)

    raw_rows = [["event"] + REDUCED_FEATURES]
    z_rows = [["event"] + REDUCED_FEATURES]
    for ev in sorted(groups):
        idx = groups[ev]
        m = deltas[idx].mean(axis=0)
        mz = (deltas[idx] / std).mean(axis=0)
        raw_rows.append([ev] + [f"{x:.4g}" for x in m])
        z_rows.append([ev] + [f"{x:.4g}" for x in mz])
    return markdown_table(raw_rows), markdown_table(z_rows)

def empirical_rule_matrix(event_rows: List[Dict[str, Any]], event_filter: List[str]) -> np.ndarray:
    groups = []
    for ev in event_filter:
        subset = [r for r in event_rows if r["event"] == ev]
        if subset:
            arr = np.array([[float(r[f"d_{name}"]) for name in CORE_FEATURES] for r in subset], dtype=float)
            groups.append(arr.mean(axis=0))
        else:
            groups.append(np.zeros(len(CORE_FEATURES)))
    return np.array(groups, dtype=float)

def format_nullspace_basis(basis: np.ndarray, feature_names: List[str], tol: float = 1e-9) -> List[str]:
    out = []
    if basis.size == 0 or basis.shape[1] == 0:
        return ["ingen"]
    for j in range(basis.shape[1]):
        col = basis[:, j]
        nz = [f"{col[i]:+.3f}·{feature_names[i]}" for i in range(len(feature_names)) if abs(col[i]) > tol]
        out.append(" ".join(nz) if nz else "0")
    return out

def contextual_formula_residuals(event_rows: List[Dict[str, Any]]) -> str:
    rows = [["event", "feature", "n", "mean_abs_residual", "max_abs_residual"]]
    tracked_events = ["seed", "triad", "delete", "swap"]
    tracked_features = ["wedges", "triangles", "star3"]
    for ev in tracked_events:
        for feat in tracked_features:
            residuals = []
            for r in event_rows:
                if r["event"] != ev:
                    continue
                p = r.get(f"pred_{feat}")
                if p is None or p == "":
                    continue
                residuals.append(abs(float(r[f"d_{feat}"]) - float(p)))
            if residuals:
                rows.append([ev, feat, str(len(residuals)), f"{float(np.mean(residuals)):.6g}", f"{float(np.max(residuals)):.6g}"])
            else:
                rows.append([ev, feat, "0", "nan", "nan"])
    return markdown_table(rows)

def theoretical_context_formulas_md() -> str:
    rows = [
        ["regel", "lokal kontekst", "Δwedges", "Δtriangles", "Δstar3"],
        ["seed", "hostgrad h", "h", "0", "C(h,2)"],
        ["triad", "grader d_v,d_w og felles naboer c", "d_v + d_w", "c", "C(d_v,2)+C(d_w,2)"],
        ["delete", "grader d_v,d_u og felles naboer c", "-[(d_v-1)+(d_u-1)]", "-c", "-[C(d_v-1,2)+C(d_u-1,2)]"],
        ["swap", "d_u,d_w,c_del,c_add", "-(d_u-1)+d_w", "-c_del + c_add", "-C(d_u-1,2)+C(d_w,2)"],
    ]
    text = [
        "## Kontekstbetingede eksakte formler i den reduserte motivsektoren",
        "",
        "Disse formlene gjelder for features som kan uttrykkes rent kombinatorisk ved lokale grad- og nabostrukturer.",
        "De er ikke antagelser; de er identiteter for de primitive reglene slik de er implementert i simulatoren.",
        "",
        markdown_table(rows),
        "",
        "Merk at `c4`, `spectral_radius`, `clustering` og `dim_proxy` ikke har like enkle lokale lukkede formler i denne implementasjonen.",
        "De må derfor analyseres empirisk som regimevariabler eller quasi-invariant-kandidater.",
        "",
    ]
    return "\n".join(text)

def build_markdown_report(
    args: argparse.Namespace,
    event_rows: List[Dict[str, Any]],
    csv_path: str,
) -> str:
    raw_table, z_table = mean_delta_tables(event_rows)

    sections = [
        "# Redusert basis og regelbetingede ΔF-matriser",
        "",
        "Dette dokumentet er v0.4-steget i prosjektet. Målet er å erstatte diffuse quasi-invariant-utsagn med en presis analyse av:",
        "",
        "1. hvilken feature-basis som er algebraisk uavhengig,",
        "2. hvilke lineære invariants som følger av den valgte regelklassen,",
        "3. hvilke kontekstbetingede motivendringer som kan beregnes eksakt, og",
        "4. hvilke resterende features som må behandles som empiriske makrovariabler.",
        "",
        "## Kjøringsparametre",
        "",
        f"- steps: {args.steps}",
        f"- seed: {args.seed}",
        f"- r_seed: {args.r_seed}",
        f"- r_token: {args.r_token}",
        f"- r_birth: {args.r_birth}",
        f"- r_death: {args.r_death}",
        f"- p_triad: {args.p_triad}",
        f"- p_del: {args.p_del}",
        f"- p_swap: {args.p_swap}",
        f"- avoid_disconnect: {args.avoid_disconnect}",
        f"- relocate_tokens: {args.relocate_tokens}",
        "",
        "## Redusert feature-basis",
        "",
        "Vi bruker følgende reduserte basis:",
        "",
        "`tokens, nodes, components, beta1, wedges, triangles, star3, c4, spectral_radius, clustering, dim_proxy`",
        "",
        "Følgende størrelser er eksplisitt tatt ut av basisen fordi de er algebraisk avledbare:",
        "",
        "- `edges = beta1 + nodes - components`",
        "- `deg_sq_sum = 2*edges + 2*wedges = 2*(beta1 + nodes - components) + 2*wedges`",
        "",
        invariant_classification_markdown(),
        theoretical_context_formulas_md(),
        "## Hendelsesfordeling",
        "",
        summarise_events(event_rows),
        "",
        "## Empirisk regelbetinget middelmatrise i redusert basis",
        "",
        "Tabellen under viser middelverdien av `ΔF` per hendelsestype i den reduserte basisen.",
        "",
        raw_table,
        "",
        "## Standardisert middelmatrise",
        "",
        "Her er de samme radene etter standardisering per feature med global standardavviksskala over hendelsesmatrisen.",
        "Dette gjør det mulig å sammenlikne hvilke regler som dominerer hvilke features uavhengig av enhetsstørrelse.",
        "",
        z_table,
        "",
    ]

    # Theoretical nullspaces
    sections.extend([
        "## Nullrom fra teoretiske kjernematriser",
        "",
    ])
    for label, rules in RULESET_LIBRARY.items():
        A = np.vstack([core_delta_vector_for_rule(r) for r in rules])
        basis = nullspace_basis(A)
        sections.append(f"### {label}")
        sections.append("")
        sections.append("Regler: " + ", ".join(rules))
        sections.append("")
        sections.append("Invariantbasis:")
        sections.append("")
        for b in format_nullspace_basis(basis, CORE_FEATURES):
            sections.append(f"- {b}")
        sections.append("")

    # Empirical nullspace for active events in this run
    active_rules = [ev for ev in ["seed", "birth", "death", "triad", "delete", "swap"] if any(r["event"] == ev for r in event_rows)]
    if active_rules:
        A_emp = empirical_rule_matrix(event_rows, active_rules)
        basis_emp = nullspace_basis(A_emp)
        rows = [["regel"] + CORE_FEATURES]
        for ev, row in zip(active_rules, A_emp):
            rows.append([ev] + [f"{x:.4g}" for x in row])
        sections.extend([
            "## Empirisk kjernematrise for aktive regler i denne kjøringen",
            "",
            markdown_table(rows),
            "",
            "Empirisk nullromsbasis i kjernebasis:",
            "",
        ])
        for b in format_nullspace_basis(basis_emp, CORE_FEATURES):
            sections.append(f"- {b}")
        sections.append("")

    sections.extend([
        "## Residualtest for kontekstbetingede motivformler",
        "",
        "Hvis residualene her er null (opp til flyttallsavrunding), bekrefter simulatoren de eksakte lokale formlene for `wedges`, `triangles` og `star3`.",
        "",
        contextual_formula_residuals(event_rows),
        "",
        "## Metodologisk status",
        "",
        "Dette steget etablerer et presist skille mellom tre nivåer:",
        "",
        "1. **Grafidentiteter**: størrelser som ikke bør behandles som uavhengige observabler.",
        "2. **Regelstyrte invariants**: nullrom til de primitive `ΔF`-radene i valgt regelklasse.",
        "3. **Regimevariabler**: `c4`, `spectral_radius`, `clustering`, `dim_proxy` og lignende, som må analyseres empirisk og eventuelt som quasi-invarianter.",
        "",
        "Denne sondringen er nødvendig før man kan gå videre til mer modne spørsmål om emergent geometri, effektiv energi og dimensjon.",
        "",
        "## Videre arbeid",
        "",
        "- Legg til flere lokale motivfeatures og sjekk om de er uavhengige etter identitetsreduksjon.",
        "- Bygg en eksplisitt `Rule`-abstraksjon med analytiske `delta_core`- og `delta_motif`-metoder.",
        "- Koble dette til perturbasjonstester for maksimal propagasjonshastighet og senere til spektral/volumetrisk dimensjon.",
        "",
        f"_CSV med rå hendelsesdata: `{csv_path}`_",
        "",
    ])
    return "\n".join(sections)


# ----------------------------
# Main runner
# ----------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Reduced-basis and rule-conditioned delta-F lab.")
    p.add_argument("--steps", type=int, default=12000)
    p.add_argument("--seed", type=int, default=11)
    p.add_argument("--initial-cycle", type=int, default=6)
    p.add_argument("--initial-tokens", type=int, default=4)
    p.add_argument("--r-seed", type=float, default=0.05)
    p.add_argument("--r-token", type=float, default=1.0)
    p.add_argument("--r-birth", type=float, default=0.0)
    p.add_argument("--r-death", type=float, default=0.0)
    p.add_argument("--p-triad", type=float, default=0.0)
    p.add_argument("--p-del", type=float, default=0.0)
    p.add_argument("--p-swap", type=float, default=0.06)
    p.add_argument("--avoid-disconnect", action="store_true")
    p.add_argument("--relocate-tokens", action="store_true")
    p.add_argument("--closed-topological", action="store_true", help="Convenience preset: seed+swap, no triad/delete/birth/death, avoid_disconnect on.")
    p.add_argument("--open-topological", action="store_true", help="Convenience preset: seed+triad+delete+swap, no birth/death, avoid_disconnect on.")
    p.add_argument("--out-csv", type=str, default="rule_delta_events.csv")
    p.add_argument("--out-md", type=str, default="rule_delta_summary.md")
    return p

def apply_presets(args: argparse.Namespace) -> None:
    if args.closed_topological:
        args.p_triad = 0.0
        args.p_del = 0.0
        args.p_swap = max(args.p_swap, 0.06)
        args.r_birth = 0.0
        args.r_death = 0.0
        args.avoid_disconnect = True
        args.relocate_tokens = True
    if args.open_topological:
        args.p_triad = max(args.p_triad, 0.10)
        args.p_del = max(args.p_del, 0.10)
        args.p_swap = max(args.p_swap, 0.06)
        args.r_birth = 0.0
        args.r_death = 0.0
        args.avoid_disconnect = True
        args.relocate_tokens = True

def main() -> None:
    args = build_parser().parse_args()
    apply_presets(args)
    random.seed(args.seed)
    np.random.seed(args.seed)

    state = bootstrap(args.initial_cycle, args.initial_tokens)
    event_rows: List[Dict[str, Any]] = []

    for i in range(args.steps):
        before = feature_row(state)
        ctx = step(
            state,
            r_seed=args.r_seed,
            r_token=args.r_token,
            r_birth=args.r_birth,
            r_death=args.r_death,
            p_triad=args.p_triad,
            p_del=args.p_del,
            p_swap=args.p_swap,
            avoid_disconnect=args.avoid_disconnect,
            relocate_tokens=args.relocate_tokens,
        )
        after = feature_row(state)

        row: Dict[str, Any] = {"i": i, "t_before": before["t"], "t_after": after["t"], "event": ctx.get("event", "unknown")}
        for name, val in ctx.items():
            if name == "event":
                continue
            row[name] = val
        for name in REDUCED_FEATURES:
            row[f"before_{name}"] = before[name]
            row[f"after_{name}"] = after[name]
            row[f"d_{name}"] = after[name] - before[name]

        pred = predict_contextual_delta(ctx, {name: row[f"d_{name}"] for name in REDUCED_FEATURES})
        for feat in ["wedges", "triangles", "star3"]:
            row[f"pred_{feat}"] = "" if pred[feat] is None else float(pred[feat])

        event_rows.append(row)

    fieldnames = sorted({k for row in event_rows for k in row.keys()})
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(event_rows)

    md = build_markdown_report(args, event_rows, args.out_csv)
    with open(args.out_md, "w", encoding="utf-8") as f:
        f.write(md)

if __name__ == "__main__":
    main()
