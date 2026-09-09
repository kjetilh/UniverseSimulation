"""UC1: bounded baseline counterexamples and circulation instrumentation.

This does not implement a new universe model. Calibration uses engineered
histories; it must never be reported as spontaneous formation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import random
from statistics import median
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import relational_universe_sim as baseline

SPEC = ROOT / "Documentation/Program/UC1_preregistration.json"


def circulation_coverage(path: list[int]) -> float:
    """Fraction of hops covered by >=3 same-direction simple-cycle laps.

    Sliding windows and set union avoid counting overlapping detections twice.
    This is an observer over histories, with no effect on the simulated graph.
    """
    covered: set[int] = set()
    for length in range(3, 7):
        width = 3 * length
        for start in range(len(path) - width):
            cycle = path[start : start + length]
            if len(set(cycle)) != length:
                continue
            if all(path[start + offset] == cycle[offset % length]
                   for offset in range(length, width + 1)):
                covered.update(range(start, start + width))
    return len(covered) / (len(path) - 1) if len(path) > 1 else 0.0


def sign_probability(positive: int, negative: int) -> float:
    """One-sided exact sign probability, excluding ties."""
    n = positive + negative
    return sum(math.comb(n, k) for k in range(positive, n + 1)) / 2**n if n else 1.0


def graph_state(edges: list[tuple[int, int]], tokens: list[int]) -> baseline.SimState:
    graph = baseline.UGraph()
    for a, b in edges:
        graph.add_edge(a, b)
    for vertex in tokens:
        graph.add_node(vertex)
    return baseline.SimState(graph, list(tokens), max(graph.nodes()) + 1)


def baseline_probes() -> list[dict]:
    params = baseline.Params(r_seed=0, r_token_birth=0, r_token_death=0,
                             p_delete_traversed_edge=1,
                             p_triadic_closure=0, p_local_rewire=0)
    rows = []
    for relocation in (False, True):
        random.seed(20260909)
        edges = [(0, 1), (2, 3)] if relocation else [(0, 1)]
        state = graph_state(edges, [0])
        params.relocate_tokens_on_prune = relocation
        before = list(state.tokens)
        baseline.gillespie_step(state, params)
        rows.append({
            "probe": "cross_component_relocation" if relocation else "unit_loss",
            "initial_edges": edges, "tokens_before": before,
            "tokens_after": list(state.tokens), "nodes_after": sorted(state.g.nodes()),
            "violation_observed": bool(set(state.tokens) & {2, 3}) if relocation
                                  else len(state.tokens) < len(before),
            "scope": "root baseline under specified boundary input; not all v-series runs",
        })
    random.seed(20260909)
    state = graph_state([(2, 3)], [0])
    baseline.token_event(state, params)
    rows.append({
        "probe": "isolated_global_reconnection", "initial_edges": [(2, 3)],
        "tokens_before": [0], "tokens_after": list(state.tokens),
        "neighbors_of_isolated_host_after": sorted(state.g.neighbors(0)),
        "violation_observed": bool(set(state.g.neighbors(0)) & {2, 3}),
        "scope": "root baseline fallback on an isolated host",
    })
    return rows


def run(out: Path) -> None:
    spec_bytes = SPEC.read_bytes()
    spec = json.loads(spec_bytes)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    with (out / "UC1_reference_paths.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["cycle_length", "replicate", "seed", "reference", "hop", "node"])
        for length in (3, 4):
            for replicate in range(spec["references"]["replicates_per_graph"]):
                seed = 2026090900 + 100 * length + replicate
                rng = random.Random(seed)
                hops = spec["references"]["hops_per_history"]
                positive = [step % length for step in range(hops + 1)]
                null = [0]
                for _ in range(hops):
                    null.append((null[-1] + rng.choice((-1, 1))) % length)
                for role, path in (("positive", positive), ("null", null)):
                    assert all((b - a) % length in {1, length - 1}
                               for a, b in zip(path, path[1:]))
                    writer.writerows((length, replicate, seed, role, i, node)
                                     for i, node in enumerate(path))
                p, n = circulation_coverage(positive), circulation_coverage(null)
                rows.append({"cycle_length": length, "replicate": replicate, "seed": seed,
                             "hops": hops, "positive": p, "null": n,
                             "sign": (p > n) - (p < n),
                             "squared_sign": (p*p > n*n) - (p*p < n*n)})
    with (out / "UC1_reference_summary.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    wins = sum(row["sign"] > 0 for row in rows)
    losses = sum(row["sign"] < 0 for row in rows)
    probability = sign_probability(wins, losses)
    summary = {
        "round": "UC1", "stage": "instrumentation_only",
        "preregistration_sha256": hashlib.sha256(spec_bytes).hexdigest(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "baseline_source_sha256": hashlib.sha256((ROOT / "relational_universe_sim.py").read_bytes()).hexdigest(),
        "baseline_probes": baseline_probes(),
        "reference_pairs": len(rows), "positive_signs": wins, "negative_signs": losses,
        "one_sided_sign_p": probability,
        "positive_median": median(row["positive"] for row in rows),
        "null_median": median(row["null"] for row in rows),
        "squared_signs_identical": all(row["sign"] == row["squared_sign"] for row in rows),
        "reference_separation_pass": probability <= .05 and
            median(row["positive"] for row in rows) > median(row["null"] for row in rows),
        "candidate_runs": 0,
        "claim_limit": "Engineered circulation controls and baseline counterexamples only. No spontaneous metastability, invariant, dimension or physics result.",
    }
    summary["evidence_sha256"] = {
        name: hashlib.sha256((out / name).read_bytes()).hexdigest()
        for name in ("UC1_reference_paths.csv", "UC1_reference_summary.csv")
    }
    (out / "UC1_measurements.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    run(parser.parse_args().out)
