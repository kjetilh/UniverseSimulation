"""UC2 preregistered dynamic calibration and descriptive candidate histories.

No candidate effect/null significance is computed. Calibration must precede
candidate execution with identical protocol and source hashes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import heapq
import json
from pathlib import Path
import random
from statistics import median
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from Tools.local_change_candidate import (
    make_state, apply_move, attempt_step, edge_set, component_partition,
)
from Tools.units_of_change_conformance import circulation_coverage, sign_probability

SPEC = ROOT / "Documentation/Program/UC2_preregistration.json"
EVENT_FIELDS = ["run_id", "attempt", "tick", "unit_index", "source", "target", "carried"]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes() -> dict[str, str]:
    return {p: digest(ROOT / p) for p in (
        "Documentation/Program/UC2_preregistration.json",
        "Tools/local_change_candidate.py",
        "Tools/run_local_change_candidate.py",
        "Tools/units_of_change_conformance.py",
    )}


def uniform_tree(n: int, rng: random.Random) -> list[tuple[int, int]]:
    """Uniform labeled tree via uniform Pruefer word; labels are bookkeeping."""
    if n < 2:
        raise ValueError("Tree requires at least two nodes")
    word = [rng.randrange(n) for _ in range(n - 2)]
    degrees = [1] * n
    for v in word:
        degrees[v] += 1
    leaves = [v for v in range(n) if degrees[v] == 1]
    heapq.heapify(leaves)
    edges = []
    for v in word:
        leaf = heapq.heappop(leaves)
        edges.append((leaf, v))
        degrees[leaf] -= 1
        degrees[v] -= 1
        if degrees[v] == 1:
            heapq.heappush(leaves, v)
    edges.append(tuple(leaves))
    return sorted(tuple(sorted(edge)) for edge in edges)


def signature(state) -> tuple:
    # Deliberately exclude observer counters and scheduling PRNG state.
    return tuple(sorted(edge_set(state))), tuple(state.units)


def jobs_for(stage: str, spec: dict) -> list[tuple]:
    if stage == "calibration":
        c = spec[stage]
        return [(f"{role}-{rep}", 3, c["seed_start"] + rep, c["steps"], role)
                for rep in range(c["replicates"]) for role in ("positive", "null")]
    c = spec["candidate"]
    return [(f"n{n}-{rep}", n, 20260910000 + 100 * n + rep, c["steps"], "candidate")
            for n in c["node_counts"] for rep in range(c["replicates_per_size"])]


def initialize(run_id: str, n: int, seed: int, steps: int, role: str):
    rng = random.Random(seed)
    edges = [(0, 1), (0, 2)] if role != "candidate" else uniform_tree(n, rng)
    degrees = [sum(v in e for e in edges) for v in range(n)]
    host = 0 if role != "candidate" else rng.choice([v for v in range(n) if degrees[v] >= 2])
    state = make_state(range(n), edges, [host])
    initial = {"run_id": run_id, "node_count": n, "seed": seed,
               "role": role, "edges": edges, "units": [host], "steps": steps}
    return state, rng, initial


def run_case(run_id: str, n: int, seed: int, steps: int,
             role: str, writer) -> tuple[dict, dict]:
    state, rng, initial = initialize(run_id, n, seed, steps, role)
    host = state.units[0]
    path, states = [host], [signature(state)]
    original_components = component_partition(state)
    for i in range(steps):
        if role == "positive":
            target = (i + 1) % 3
            carried = 3 - state.units[0] - target
            result = apply_move(state, 0, target, carried)
        else:
            result = attempt_step(state, rng)
        if not result.changed:
            raise RuntimeError("Initially eligible tree unit unexpectedly blocked")
        if (len(state.units) != 1 or len(edge_set(state)) != n - 1 or
                component_partition(state) != original_components):
            raise RuntimeError("UC2 candidate invariant failure")
        writer.writerow({"run_id": run_id, "attempt": state.attempts,
                         "tick": state.ticks, "unit_index": result.unit_index,
                         "source": result.source, "target": result.target,
                         "carried": result.carried})
        path.append(state.units[0])
        states.append(signature(state))
    return initial, {"run_id": run_id, "node_count": n, "seed": seed,
                     "role": role, "steps": steps, "attempts": state.attempts,
                     "ticks": state.ticks, "node_itinerary_coverage": circulation_coverage(path),
                     "exact_state_orbit_coverage": circulation_coverage(states),
                     "distinct_observed_states": len(set(states)),
                     "final_nodes": n, "final_edges": len(edge_set(state)),
                     "final_units": len(state.units), "cycle_rank": 0,
                     "trace_final_state_sha256": hashlib.sha256(repr(states[-1]).encode()).hexdigest()}


def calibration_metrics(rows: list[dict]) -> dict:
    p = [float(r["node_itinerary_coverage"]) for r in rows if r["role"] == "positive"]
    n = [float(r["node_itinerary_coverage"]) for r in rows if r["role"] == "null"]
    signs = [(a > b) - (a < b) for a, b in zip(p, n)]
    transformed = [(a*a > b*b) - (a*a < b*b) for a, b in zip(p, n)]
    prob = sign_probability(signs.count(1), signs.count(-1))
    return dict(positive_median=median(p), null_median=median(n), paired_signs=signs,
                one_sided_sign_score=prob, squared_signs_identical=signs == transformed,
                reference_gate_pass=median(p) > median(n) and prob <= .05 and signs == transformed)


def measure(stage: str, out: Path) -> dict:
    spec = json.loads(SPEC.read_text())
    hashes = source_hashes()
    if stage == "candidate":
        calibration_path = out / "UC2_calibration.json"
        calibration = json.loads(calibration_path.read_text())
        if calibration["source_sha256"] != hashes or not calibration["reference_gate_pass"]:
            raise RuntimeError("Candidate refused: stale or unqualified references")
        verify("calibration", out)
    out.mkdir(parents=True, exist_ok=True)
    initial, rows = [], []
    prefix = "UC2_" + stage
    with (out / (prefix + "_events.csv")).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EVENT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for job in jobs_for(stage, spec):
            start, summary = run_case(*job, writer)
            initial.append(start)
            rows.append(summary)
    (out / (prefix + "_initial.json")).write_text(json.dumps(initial, indent=2) + "\n")
    with (out / (prefix + "_summary.csv")).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    result = {"round": "UC2", "stage": stage, "source_sha256": hashes,
              "runs": len(rows), "total_successful_changes": sum(r["ticks"] for r in rows),
              "evidence_sha256": {prefix + suffix: digest(out / (prefix + suffix))
                                  for suffix in ("_initial.json", "_events.csv", "_summary.csv")}}
    if stage == "calibration":
        result.update(calibration_metrics(rows))
        result["claim_limit"] = "Dynamic engineered orbit instrument qualification, not spontaneous structure."
    else:
        result.update(calibration_sha256=digest(out / "UC2_calibration.json"),
                      node_itinerary_median=median(r["node_itinerary_coverage"] for r in rows),
                      exact_state_orbit_median=median(r["exact_state_orbit_coverage"] for r in rows),
                      claim_limit=spec["claim_limit"], candidate_effect_gate="not_defined_descriptive_only")
    (out / (prefix + ".json")).write_text(json.dumps(result, indent=2) + "\n")
    return result


def verify(stage: str, out: Path) -> dict:
    prefix = "UC2_" + stage
    record = json.loads((out / (prefix + ".json")).read_text())
    spec = json.loads(SPEC.read_text())
    if record["stage"] != stage or record["round"] != "UC2":
        raise RuntimeError("Wrong evidence identity")
    if record["source_sha256"] != source_hashes():
        raise RuntimeError("Source/protocol hash mismatch")
    expected_files = {prefix + suffix for suffix in ("_initial.json", "_events.csv", "_summary.csv")}
    if set(record["evidence_sha256"]) != expected_files:
        raise RuntimeError("Incomplete or unexpected evidence manifest")
    for name, expected in record["evidence_sha256"].items():
        if digest(out / name) != expected:
            raise RuntimeError("Evidence hash mismatch: " + name)
    initial = json.loads((out / (prefix + "_initial.json")).read_text())
    scheduled = [initialize(*job) for job in jobs_for(stage, spec)]
    expected_initial = json.loads(json.dumps([item[2] for item in scheduled]))
    if initial != expected_initial or record["runs"] != len(scheduled):
        raise RuntimeError("Initial states or run schedule differ from preregistration")
    generated = {item[2]["run_id"]: item for item in scheduled}
    states = {r["run_id"]: make_state(range(r["node_count"]), r["edges"], r["units"]) for r in initial}
    paths = {key: [s.units[0]] for key, s in states.items()}
    snapshots = {key: [signature(s)] for key, s in states.items()}
    count = 0
    with (out / (prefix + "_events.csv")).open() as handle:
        for row in csv.DictReader(handle):
            state = states[row["run_id"]]
            seeded, rng, start = generated[row["run_id"]]
            if start["role"] == "positive":
                target = (seeded.ticks + 1) % 3
                expected = apply_move(seeded, 0, target, 3 - seeded.units[0] - target)
            else:
                expected = attempt_step(seeded, rng)
            if (int(row["unit_index"]), int(row["source"]), int(row["target"]), int(row["carried"])) != (
                    expected.unit_index, expected.source, expected.target, expected.carried):
                raise RuntimeError("Trace differs from seeded preregistered dynamics")
            if state.units[int(row["unit_index"])] != int(row["source"]):
                raise RuntimeError("Trace source mismatch")
            apply_move(state, int(row["unit_index"]), int(row["target"]), int(row["carried"]))
            if state.ticks != int(row["tick"]) or state.attempts != int(row["attempt"]):
                raise RuntimeError("Trace clock mismatch")
            paths[row["run_id"]].append(state.units[0])
            snapshots[row["run_id"]].append(signature(state))
            count += 1
    with (out / (prefix + "_summary.csv")).open() as handle:
        rows = list(csv.DictReader(handle))
        if [r["run_id"] for r in rows] != [r["run_id"] for r in initial]:
            raise RuntimeError("Summary run IDs differ from schedule")
        for row, start in zip(rows, initial):
            key = row["run_id"]
            state = states[key]
            if (state.ticks != start["steps"] or state.ticks != int(row["steps"]) or
                    int(row["node_count"]) != start["node_count"] or int(row["seed"]) != start["seed"] or
                    row["role"] != start["role"] or int(row["attempts"]) != state.attempts or
                    int(row["ticks"]) != state.ticks or int(row["final_units"]) != len(state.units) or
                    int(row["final_nodes"]) != len(state.adjacency) or
                    int(row["final_edges"]) != len(edge_set(state)) or
                    int(row["cycle_rank"]) != len(edge_set(state))-len(state.adjacency)+len(component_partition(state)) or
                    int(row["distinct_observed_states"]) != len(set(snapshots[key])) or
                    circulation_coverage(paths[key]) != float(row["node_itinerary_coverage"]) or
                    circulation_coverage(snapshots[key]) != float(row["exact_state_orbit_coverage"]) or
                    hashlib.sha256(repr(signature(state)).encode()).hexdigest() != row["trace_final_state_sha256"]):
                raise RuntimeError("Trace/summary mismatch")
    if count != record["total_successful_changes"]:
        raise RuntimeError("Event count mismatch")
    if stage == "calibration":
        if any(record[k] != v for k, v in calibration_metrics(rows).items()):
            raise RuntimeError("Reference gate/metrics differ from replayed data")
    else:
        if digest(out / "UC2_calibration.json") != record["calibration_sha256"]:
            raise RuntimeError("Changed calibration record")
        verify("calibration", out)
        if not json.loads((out / "UC2_calibration.json").read_text())["reference_gate_pass"]:
            raise RuntimeError("Candidate lacks a qualified calibration")
        for column, field in (("node_itinerary_coverage", "node_itinerary_median"),
                              ("exact_state_orbit_coverage", "exact_state_orbit_median")):
            if median(float(r[column]) for r in rows) != record[field]:
                raise RuntimeError("Candidate aggregate differs from replayed data")
    return {"stage": stage, "replayed_runs": len(states), "replayed_changes": count,
            "all_hashes_and_endpoints_match": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("calibration", "candidate"))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify(args.stage, args.out) if args.verify else measure(args.stage, args.out), indent=2))
