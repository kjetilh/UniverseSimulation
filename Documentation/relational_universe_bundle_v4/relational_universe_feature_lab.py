
#!/usr/bin/env python3
"""relational_universe_feature_lab.py

Feature-space extension for the relational-universe toy model.

Adds:
- richer feature vectors (triangles, wedges, 3-stars, 4-cycles, degree moments)
- optional spectral proxy (adjacency spectral radius via power iteration)
- empirical quasi-invariant discovery via SVD on feature increments
- Markdown summary export

No external dependencies except optional numpy for the quasi-invariant analysis.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from dataclasses import dataclass
from typing import Dict, Set, List, Optional, Tuple


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
# Graph helpers
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

def degree_sq_sum(g: UGraph) -> int:
    return sum(g.degree(v) ** 2 for v in g.nodes())

def triangle_count(g: UGraph) -> int:
    # node-ordering method
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
    # C4 = (1/2) * sum_{u<v} C(|N(u)∩N(v)|, 2)
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
        # Rayleigh quotient
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

FEATURE_ORDER = [
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

def feature_row(state: State) -> Dict[str, float]:
    g = state.g
    row = {
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
    return row


# ----------------------------
# Dynamics
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
                births += 1  # not literal birth, but bookkeeping for local continuity tests if desired
            else:
                deaths += 1
        else:
            new_tokens.append(tok)
    state.tokens = new_tokens
    return (births, deaths)

def seed_attach(state: State, choose_token_host: bool = True) -> None:
    g = state.g
    if g.num_nodes() == 0:
        g.add_node(state.next_node_id)
        state.next_node_id += 1
        return
    if choose_token_host and state.tokens:
        host = random.choice(state.tokens)
    else:
        host = g.random_node()
    if host is None:
        return
    x = state.next_node_id
    state.next_node_id += 1
    g.add_edge(x, host)

def token_birth(state: State) -> None:
    if state.g.num_nodes() == 0:
        return
    state.tokens.append(state.g.random_node())  # type: ignore[arg-type]

def token_death(state: State) -> None:
    if state.tokens:
        idx = random.randrange(len(state.tokens))
        state.tokens.pop(idx)

def token_event(
    state: State,
    p_triad: float,
    p_del: float,
    p_swap: float,
    avoid_disconnect: bool,
    relocate_tokens: bool,
) -> str:
    if not state.tokens:
        return "noop"
    tidx = random.randrange(len(state.tokens))
    v = state.tokens[tidx]
    u = state.g.random_neighbor(v)
    if u is None:
        return "stuck"
    state.tokens[tidx] = u  # traverse first, then rewrite

    g = state.g
    roll = random.random()
    total = p_triad + p_del + p_swap
    if total <= 0:
        return "move"

    if roll < p_del:
        if not avoid_disconnect or not is_bridge(g, v, u, bfs_cap=5000):
            g.remove_edge(v, u)
            removed = g.prune_isolated()
            remove_or_relocate_tokens(state, removed, relocate_tokens)
            return "delete"
        return "move"

    roll -= p_del
    if roll < p_triad:
        # close triangle: v-u-w with new edge v-w, require w not already adjacent to v
        cands = [w for w in g.neighbors(u) if w != v and not g.has_edge(v, w)]
        if cands:
            w = random.choice(cands)
            g.add_edge(v, w)
            return "triad"
        return "move"

    roll -= p_triad
    if roll < p_swap:
        # strict edge-swap: remove v-u, add v-w; require no pre-existing v-w
        cands = [w for w in g.neighbors(u) if w != v and not g.has_edge(v, w)]
        if cands and (not avoid_disconnect or not is_bridge(g, v, u, bfs_cap=5000)):
            w = random.choice(cands)
            g.remove_edge(v, u)
            g.add_edge(v, w)
            removed = g.prune_isolated()
            remove_or_relocate_tokens(state, removed, relocate_tokens)
            return "swap"
        return "move"

    return "move"

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
) -> str:
    n_tokens = len(state.tokens)
    channels: List[Tuple[str, float]] = [
        ("seed", max(0.0, r_seed)),
        ("token", max(0.0, r_token) * n_tokens),
        ("birth", max(0.0, r_birth)),
        ("death", max(0.0, r_death)),
    ]
    total = sum(r for _, r in channels)
    if total <= 0:
        return "noop"
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
        seed_attach(state, choose_token_host=True)
        return "seed"
    if event == "birth":
        token_birth(state)
        return "birth"
    if event == "death":
        token_death(state)
        return "death"
    if event == "token":
        return token_event(
            state,
            p_triad=p_triad,
            p_del=p_del,
            p_swap=p_swap,
            avoid_disconnect=avoid_disconnect,
            relocate_tokens=relocate_tokens,
        )
    return "noop"


# ----------------------------
# Quasi-invariant analysis
# ----------------------------

def markdown_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows[1:])
    return "\n".join([header, sep, body])

def analyze_quasi_invariants(csv_path: str, feature_names: List[str], top_k: int = 3) -> str:
    try:
        import numpy as np  # type: ignore
    except Exception as exc:  # pragma: no cover
        return (
            "# Quasi-invariant analysis unavailable\n\n"
            f"Numpy could not be imported: `{exc}`.\n"
        )

    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    if len(rows) < 3:
        return "# Quasi-invariant analysis unavailable\n\nToo few logged rows.\n"

    t = np.array([float(r["t"]) for r in rows], dtype=float)
    F = np.array([[float(r[name]) for name in feature_names] for r in rows], dtype=float)
    dF = F[1:] - F[:-1]
    dt = (t[1:] - t[:-1]).reshape(-1, 1)
    dt[dt == 0.0] = 1.0
    rates = dF / dt

    # raw candidate invariants: smallest singular directions of dF and rates
    _, s_raw, vt_raw = np.linalg.svd(dF, full_matrices=False)
    _, s_rate, vt_rate = np.linalg.svd(rates, full_matrices=False)

    def candidate_block(vt, label: str) -> Tuple[str, List[List[str]]]:
        entries: List[List[str]] = [["rank", "type", "combinasjon", "increment_var", "time_slope"]]
        qmd = [f"## {label}\n"]
        for rank in range(1, min(top_k, vt.shape[0]) + 1):
            c = vt[-rank]
            q = F @ c
            dq = q[1:] - q[:-1]
            # slope of q against time
            A = np.column_stack([t, np.ones_like(t)])
            sol, *_ = np.linalg.lstsq(A, q, rcond=None)
            slope = float(sol[0])
            terms = [f"{coef:+.4f}·{name}" for coef, name in zip(c, feature_names) if abs(coef) >= 0.08]
            comb = " ".join(terms) if terms else "(sparse near-zero)"
            entries.append([str(rank), label, comb, f"{float(np.var(dq)):.6g}", f"{slope:.6g}"])
        return markdown_table(entries), entries

    raw_table, _ = candidate_block(vt_raw, "Minste endring i rå inkrementer ΔF")
    rate_table, _ = candidate_block(vt_rate, "Minste endring i hastigheter ΔF/Δt")

    # one-feature drifts
    drift_rows = [["feature", "slope", "mean", "std", "rel_slope_per_mean"]]
    A = np.column_stack([t, np.ones_like(t)])
    for j, name in enumerate(feature_names):
        q = F[:, j]
        sol, *_ = np.linalg.lstsq(A, q, rcond=None)
        slope = float(sol[0])
        mean = float(np.mean(q))
        std = float(np.std(q))
        rel = slope / mean if abs(mean) > 1e-12 else float("nan")
        drift_rows.append([name, f"{slope:.6g}", f"{mean:.6g}", f"{std:.6g}", f"{rel:.6g}"])

    singular_rows = [["matrix", "singular_values"]]
    singular_rows.append(["ΔF", ", ".join(f"{x:.4g}" for x in s_raw)])
    singular_rows.append(["ΔF/Δt", ", ".join(f"{x:.4g}" for x in s_rate)])

    md = [
        "# Empirisk quasi-invariantanalyse",
        "",
        "Dette dokumentet identifiserer lineære kombinasjoner av features som endrer seg minst over de loggede intervallene.",
        "Matematisk er dette de høyre-singularvektorene til inkrementmatrisen med minst singularverdi.",
        "",
        "## Feature-set",
        "",
        ", ".join(feature_names),
        "",
        "## Singularverdier",
        "",
        markdown_table(singular_rows),
        "",
        raw_table,
        "",
        rate_table,
        "",
        "## Enkel drift per feature",
        "",
        markdown_table(drift_rows),
        "",
        "## Tolkning",
        "",
        "En kandidat med liten increment_var og liten time_slope er en plausibel quasi-invariant i det aktuelle regimet.",
        "Det er ikke et bevis på fundamental bevaring; det er en empirisk signatur av metastabilitet i valgt feature-rom.",
        "",
    ]
    return "\n".join(md)


# ----------------------------
# Main
# ----------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Relational-universe feature lab.")
    p.add_argument("--steps", type=int, default=100000)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--initial-cycle", type=int, default=6)
    p.add_argument("--initial-tokens", type=int, default=4)
    p.add_argument("--r-seed", type=float, default=0.05)
    p.add_argument("--r-token", type=float, default=1.0)
    p.add_argument("--r-birth", type=float, default=0.0)
    p.add_argument("--r-death", type=float, default=0.0)
    p.add_argument("--p-triad", type=float, default=0.08)
    p.add_argument("--p-del", type=float, default=0.04)
    p.add_argument("--p-swap", type=float, default=0.06)
    p.add_argument("--avoid-disconnect", action="store_true", default=False)
    p.add_argument("--relocate-tokens", action="store_true", default=False)
    p.add_argument("--log-every", type=int, default=1000)
    p.add_argument("--out", type=str, default="feature_trajectory.csv")
    p.add_argument("--summary-md", type=str, default="")
    p.add_argument("--analyze", action="store_true", default=False)
    p.add_argument("--analyze-features", type=str, default="tokens,nodes,edges,beta1,wedges,triangles,star3,c4,deg_sq_sum,spectral_radius")
    return p


def main() -> None:
    args = build_parser().parse_args()
    random.seed(args.seed)
    state = bootstrap(args.initial_cycle, args.initial_tokens)

    fieldnames = ["event", "step"] + ["t"] + FEATURE_ORDER
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        def emit(step_idx: int, event_name: str) -> None:
            row = feature_row(state)
            out = {"event": event_name, "step": step_idx}
            out.update(row)
            writer.writerow(out)

        emit(0, "init")
        for i in range(1, args.steps + 1):
            ev = step(
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
            if i % args.log_every == 0 or i == args.steps:
                emit(i, ev)

    if args.summary_md:
        features = [x.strip() for x in args.analyze_features.split(",") if x.strip()]
        md_lines = [
            "# Kjøringsoppsummering for feature lab",
            "",
            "## Parametre",
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
            f"- avoid_disconnect: {args.avoid_disconnect}",
            f"- relocate_tokens: {args.relocate_tokens}",
            f"- log_every: {args.log_every}",
            "",
            f"- trajectory_csv: `{args.out}`",
            "",
        ]
        if args.analyze:
            md_lines.append(analyze_quasi_invariants(args.out, features))
        else:
            md_lines.append("Ingen quasi-invariantanalyse ble kjørt (`--analyze` manglet).")
        with open(args.summary_md, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))


if __name__ == "__main__":
    main()
