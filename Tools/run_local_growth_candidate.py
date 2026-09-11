"""UC3 frozen lawful reference calibration and descriptive growth experiment.

All attempts are logged. Per-unit observers advance on edits in their current
pre-event component, never on unrelated descendant-universe events. Verification
regenerates every product from the registered jobs and RNG streams into a
temporary directory; it does not trust stored gates, summaries or hash manifests.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from dataclasses import asdict
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import random
from statistics import median
import sys
import tempfile
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from Tools import local_growth_candidate as kernel
from Tools.local_growth_observer import snapshot, evaluate
from Tools.run_local_change_candidate import uniform_tree
from Tools.units_of_change_conformance import sign_probability

SPEC = ROOT / "Documentation/Program/UC3_preregistration.json"
EVENT_FIELDS = ["run_id", "attempt", "tick", "changed", "kind", "unit_index",
                "source", "target", "carried", "born", "removed", "reason",
                "active_units_before", "collapsible_units_before", "component_split"]
FRAME_FIELDS = ["run_id", "unit_index", "local_tick", "global_tick", "attempt",
                "N", "E", "beta", "core_nodes", "core_edges", "core_fraction",
                "beta_per_edge", "seen_splits", "seen_buds", "seen_collapses", "seen_cuts"]
SUFFIXES = ("_initial.json", "_events.csv", "_frames.csv", "_summary.csv", "_observations.json")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes() -> dict[str, str]:
    files = ("Tools/local_change_candidate.py", "Tools/local_growth_candidate.py",
             "Tools/local_growth_observer.py", "Tools/run_local_growth_candidate.py",
             "Tools/run_local_change_candidate.py", "Tools/units_of_change_conformance.py",
             "Documentation/Program/UC3_plan.md")
    return {"preregistration": digest(SPEC), **{p: digest(ROOT / p) for p in files}}


def _json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


@lru_cache(maxsize=None)
def dyck_completions(up: int, down: int, reached: bool, n: int,
                     interval: int, minimum: int) -> int:
    """Exact count with nonnegative prefixes and an observed peak constraint."""
    if not 0 <= down <= up <= n:
        return 0
    if (up + down) % interval == 0 and up - down >= minimum:
        reached = True
    if up == down == n:
        return int(reached)
    return ((dyck_completions(up + 1, down, reached, n, interval, minimum) if up < n else 0)
            + (dyck_completions(up, down + 1, reached, n, interval, minimum) if down < up else 0))


def dyck_word(n: int, rng: random.Random, interval: int, minimum: int) -> list[str]:
    if (not isinstance(n, int) or isinstance(n, bool) or n < 1 or
            not isinstance(interval, int) or isinstance(interval, bool) or interval < 1 or
            not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 0):
        raise ValueError("Dyck parameters must be valid integers")
    up = down = 0
    reached = minimum == 0
    if not dyck_completions(0, 0, reached, n, interval, minimum):
        raise ValueError("No Dyck words satisfy the observed-peak constraint")
    word = []
    while up + down < 2 * n:
        if (up + down) % interval == 0 and up - down >= minimum:
            reached = True
        a = dyck_completions(up + 1, down, reached, n, interval, minimum) if up < n else 0
        b = dyck_completions(up, down + 1, reached, n, interval, minimum) if down < up else 0
        if rng.randrange(a + b) < a:
            word.append("bud")
            up += 1
        else:
            word.append("collapse")
            down += 1
    return word


def jobs_for(stage: str, spec: dict) -> list[dict]:
    if stage not in ("calibration", "candidate") or spec["round"] != "UC3":
        raise ValueError("Wrong stage or round")
    if spec["law"]["classes"] != list(kernel.CLASSES) or spec["law"]["weights"] != list(kernel.DEFAULT_WEIGHTS):
        raise ValueError("Protocol does not specify the qualified UC3 law")
    if spec["law"]["unit_birth"] or not spec["law"]["retain_all_components"] or spec["law"]["reuse_node_ids"]:
        raise ValueError("Unsupported ontology")
    c = spec[stage]
    if stage == "calibration":
        return [dict(run_id=f"{role}-{rep}", n=c["node_count"], seed=c["seed_start"] + rep,
                     role=role, units=2, interval=c["snapshot_interval"])
                for rep in range(c["replicates"]) for role in ("positive", "null")]
    return [dict(run_id=f"n{n}-{rep}", n=n, seed=c["seed_start"] + 100*n + rep,
                 role="candidate", units=n//c["units_divisor"], interval=n//c["snapshot_divisor"])
            for n in c["node_counts"] for rep in range(c["replicates_per_size"])]


def initialize(job: dict):
    rng = random.Random(job["seed"])
    n = job["n"]
    if job["role"] == "candidate":
        edges = uniform_tree(n, rng)
        units = [rng.randrange(n) for _ in range(job["units"])]
    else:
        if n < 3:
            raise ValueError("Fan reference needs at least three nodes")
        edges = [(0, v) for v in range(1, n)] + [(v, v+1) for v in range(1, n-1)]
        units = [1, n-1]
    state = kernel.make_state(range(n), edges, units)
    initial = {**job, "nodes": list(range(n)), "edges": sorted(map(list, edges)),
               "unit_hosts": list(units), "next_node_id": state.next_node_id}
    return state, rng, initial


def partition_map(state) -> dict[int, frozenset[int]]:
    return {node: component for component in kernel.component_partition(state) for node in component}


def check_transition(before, after, event) -> bool:
    """Independent edge-set reconstruction, plus component/no-merge checks."""
    kernel.validate_state(after)
    old_edges, new_edges = set(kernel.edge_set(before)), set(kernel.edge_set(after))
    old_nodes, new_nodes = set(before.adjacency), set(after.adjacency)
    units = list(before.units)
    expected_edges, expected_nodes = set(old_edges), set(old_nodes)
    edge = lambda a, b: tuple(sorted((a, b)))
    expected_counter = before.next_node_id
    if after.attempts != before.attempts + 1 or after.ticks != before.ticks + int(event.changed):
        raise RuntimeError("Clock invariant failure")
    if event.changed:
        i, v, u, a = event.unit_index, event.source, event.target, event.carried
        if units[i] != v:
            raise RuntimeError("Wrong source unit")
        if event.kind == "bud":
            if u != event.born or u != before.next_node_id or edge(v, a) not in old_edges:
                raise RuntimeError("Nonlocal or reused birth")
            expected_nodes.add(u)
            expected_edges.update((edge(v, u), edge(a, u)))
            expected_counter += 1
        else:
            if edge(v, u) not in old_edges:
                raise RuntimeError("Nonlocal pre-existing-edge hop")
            if event.kind == "slide":
                if edge(v, a) not in old_edges or edge(u, a) in old_edges or a == u:
                    raise RuntimeError("Illegal slide")
                expected_edges.remove(edge(v, a))
                expected_edges.add(edge(u, a))
            elif event.kind == "collapse":
                if (event.removed != v or before.adjacency[v] != {u, a} or
                        edge(u, a) not in old_edges or units.count(v) != 1):
                    raise RuntimeError("Illegal collapse")
                expected_nodes.remove(v)
                expected_edges.difference_update((edge(v, u), edge(v, a)))
            elif event.kind == "cut":
                expected_edges.remove(edge(v, u))
            else:
                raise RuntimeError("Unknown successful class")
        units[i] = u
    if (new_edges != expected_edges or new_nodes != expected_nodes or after.units != units
            or after.next_node_id != expected_counter):
        raise RuntimeError("Graph/unit rewrite mismatch")
    origins = partition_map(before)
    if event.born is not None:
        origins[event.born] = origins[event.source]
    components_after = kernel.component_partition(after)
    if any(len({origins[v] for v in comp}) != 1 for comp in components_after):
        raise RuntimeError("Disconnected components merged")
    delta = len(components_after) - len(kernel.component_partition(before))
    if delta not in (0, 1) or (delta and (not event.changed or event.kind != "cut")):
        raise RuntimeError("Invalid fragmentation accounting")
    return bool(delta)


class ExposureObserver:
    """Independent causal histories; cannot mutate state or consume RNG."""
    def __init__(self, state, interval: int, emit_frame=None):
        if not isinstance(interval, int) or isinstance(interval, bool) or interval < 1:
            raise ValueError("Positive integer observation interval required")
        self.interval, self.emit_frame = interval, emit_frame
        self.clocks = [0] * len(state.units)
        self.counts = [Counter() for _ in state.units]
        self.histories = [[] for _ in state.units]
        self.metadata = [[] for _ in state.units]
        self._capture(state, range(len(state.units)))

    def _capture(self, state, tags):
        parts, cache = partition_map(state), {}
        for tag in tags:
            component = parts[state.units[tag]]
            key = (component, self.clocks[tag])
            if key not in cache:
                view = SimpleNamespace(adjacency={v: state.adjacency[v] for v in component},
                                       units=[state.units[tag]], ticks=self.clocks[tag], attempts=state.attempts)
                cache[key] = snapshot(view)
            frame = cache[key]
            self.histories[tag].append(frame)
            region, counts = frame["regions"][0], self.counts[tag]
            meta = {"unit_index": tag, "local_tick": self.clocks[tag], "global_tick": state.ticks,
                    "attempt": state.attempts, "N": region["N"], "E": region["E"], "beta": region["beta"],
                    "core_nodes": len(region["core_nodes"]), "core_edges": len(region["core_edges"]),
                    "core_fraction": region["core_fraction"], "beta_per_edge": region["beta_per_edge"],
                    "seen_splits": counts["split"], "seen_buds": counts["bud"],
                    "seen_collapses": counts["collapse"], "seen_cuts": counts["cut"]}
            self.metadata[tag].append(meta)
            if self.emit_frame:
                self.emit_frame(meta)

    def advance(self, before, state, event, split: bool):
        if not event.changed:
            return
        component = partition_map(before)[event.source]
        affected = [i for i, host in enumerate(before.units) if host in component]
        for tag in affected:
            self.clocks[tag] += 1
            self.counts[tag][event.kind] += 1
            self.counts[tag]["split"] += int(split)
        self._capture(state, [i for i in affected if self.clocks[i] % self.interval == 0])

    def result(self, settings: dict) -> dict:
        rows, intervals = [], []
        for tag, history in enumerate(self.histories):
            result = evaluate(history, **settings)
            row = {**result["per_unit"][0], "unit_index": tag, "component_exposures": self.clocks[tag],
                   "insufficient_trace": result["insufficient_trace"]}
            rows.append(row)
            for interval in result["qualifying_intervals"]:
                first = self.metadata[tag][interval["start_frame"]]
                last = self.metadata[tag][interval["end_frame"]]
                intervals.append({**interval, "unit_index": tag,
                                  "start_global_tick": first["global_tick"], "end_global_tick": last["global_tick"],
                                  "start_attempt": first["attempt"], "end_attempt": last["attempt"],
                                  "component_splits_in_window": last["seen_splits"] - first["seen_splits"],
                                  "buds_in_window": last["seen_buds"] - first["seen_buds"],
                                  "collapses_in_window": last["seen_collapses"] - first["seen_collapses"],
                                  "cuts_in_window": last["seen_cuts"] - first["seen_cuts"]})
        return {"primary": sum(r["fraction"] for r in rows)/len(rows) if rows else 0.0,
                "per_unit": rows, "qualifying_intervals": intervals,
                "scope": "Per-tag component exposure; tags/windows are correlated, seed-world is the replicate."}


def run_case(job: dict, spec: dict, event_writer, frame_writer) -> tuple[dict, dict, dict]:
    state, rng, initial = initialize(job)
    counts, blocked, drift_n = Counter(), Counter(), 0.0
    observer = ExposureObserver(state, job["interval"],
        lambda row: frame_writer.writerow({"run_id": job["run_id"], **row}))
    initial_balance = len(kernel.edge_set(state)) - 2*len(state.adjacency)
    initial_units = len(state.units)
    max_nodes = len(state.adjacency)
    words = []
    if job["role"] != "candidate":
        c = spec["calibration"]
        for _ in range(c["periods"]):
            words += (["bud"]*c["buds_per_period"] + ["collapse"]*c["buds_per_period"]
                      if job["role"] == "positive" else
                      dyck_word(c["buds_per_period"], rng, c["snapshot_interval"], c["null_observed_height_min"]))
    while True:
        if job["role"] == "candidate":
            c = spec["candidate"]
            if all(not state.adjacency[v] for v in state.units):
                stop = "activity_absorbed"
                break
            if len(state.adjacency) >= c["node_cap"]:
                stop = "node_cap_censored"
                break
            if state.ticks >= c["max_changes"]:
                stop = "change_budget"
                break
            if state.attempts >= c["max_attempts"]:
                stop = "attempt_budget"
                break
        elif state.ticks == len(words):
            stop = "reference_complete"
            break
        before = kernel.clone_state(state)
        active = sum(bool(before.adjacency[v]) for v in before.units)
        collapsible = sum(len(before.adjacency[v]) == 2 and before.units.count(v) == 1 and
                          all(b in before.adjacency[a] for a in before.adjacency[v] for b in before.adjacency[v] if a != b)
                          for v in before.units)
        if job["role"] == "candidate":
            drift_n += (active - 2*collapsible)/(8*initial_units)
            event = kernel.attempt_step(state, rng, spec["law"]["weights"])
        elif words[state.ticks] == "bud":
            event = kernel.apply_event(state, 1, "bud", target=0)
        else:
            source = state.units[0]
            target = next(v for v in state.adjacency[source] if v != 0)
            event = kernel.apply_event(state, 0, "collapse", target=target)
        split = check_transition(before, state, event)
        if event.changed:
            counts[event.kind] += 1
        else:
            blocked[event.kind] += 1
        if len(state.units) != initial_units or len(kernel.edge_set(state)) - 2*len(state.adjacency) + counts["cut"] != initial_balance:
            raise RuntimeError("Persistent-unit or accounting invariant failure")
        counts["splits"] += int(split)
        max_nodes = max(max_nodes, len(state.adjacency))
        event_writer.writerow({"run_id": job["run_id"], "attempt": state.attempts, "tick": state.ticks,
                               **asdict(event), "active_units_before": active,
                               "collapsible_units_before": collapsible, "component_split": split})
        observer.advance(before, state, event, split)
    detail = {"run_id": job["run_id"], **observer.result(spec["observer"])}
    parts = kernel.component_partition(state)
    edges = len(kernel.edge_set(state))
    per_unit = detail["per_unit"]
    summary = {**job, "attempts": state.attempts, "ticks": state.ticks, "stop": stop,
               "primary": detail["primary"], "final_N": len(state.adjacency), "max_N": max_nodes,
               "final_E": edges, "final_C": len(parts), "final_beta": edges-len(state.adjacency)+len(parts),
               "final_units": len(state.units), "isolated_units": sum(not state.adjacency[v] for v in state.units),
               **{kind: counts[kind] for kind in kernel.CLASSES}, "component_splits": counts["splits"],
               **{"blocked_"+kind: blocked[kind] for kind in kernel.CLASSES},
               "insufficient_unit_traces": sum(row["insufficient_trace"] for row in per_unit),
               "possible_windows": sum(row["possible_windows"] for row in per_unit),
               "size_core_eligible_windows": sum(row["size_core_eligible_windows"] for row in per_unit),
               "qualifying_windows": len(detail["qualifying_intervals"]),
               "qualifying_windows_with_split": sum(r["component_splits_in_window"] > 0 for r in detail["qualifying_intervals"]),
               "min_component_exposures": min(observer.clocks), "max_component_exposures": max(observer.clocks),
               "integrated_expected_node_drift": drift_n if job["role"] == "candidate" else "controlled_reference",
               "final_state_sha256": hashlib.sha256(repr(kernel.state_snapshot(state)).encode()).hexdigest()}
    return initial, summary, detail


def calibration_metrics(rows: list[dict]) -> dict:
    positives = [float(row["primary"]) for row in rows if row["role"] == "positive"]
    nulls = [float(row["primary"]) for row in rows if row["role"] == "null"]
    signs = [(a > b)-(a < b) for a, b in zip(positives, nulls)]
    squared = [(a*a > b*b)-(a*a < b*b) for a, b in zip(positives, nulls)]
    p = sign_probability(signs.count(1), signs.count(-1))
    return {"positive_median": median(positives), "null_median": median(nulls),
            "paired_signs": signs, "one_sided_sign_score": p, "squared_signs_identical": signs == squared,
            "reference_gate_pass": median(positives) > median(nulls) and p <= .05 and signs == squared}


def _execute(stage: str, spec: dict, out: Path, calibration_hash: str | None = None) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    prefix = "UC3_" + stage
    starts, rows, details = [], [], []
    with (out/(prefix+"_events.csv")).open("w", newline="") as e, (out/(prefix+"_frames.csv")).open("w", newline="") as f:
        ew = csv.DictWriter(e, fieldnames=EVENT_FIELDS, lineterminator="\n")
        fw = csv.DictWriter(f, fieldnames=FRAME_FIELDS, lineterminator="\n")
        ew.writeheader()
        fw.writeheader()
        for job in jobs_for(stage, spec):
            start, summary, detail = run_case(job, spec, ew, fw)
            starts.append(start)
            rows.append(summary)
            details.append(detail)
    _json(out/(prefix+"_initial.json"), starts)
    _json(out/(prefix+"_observations.json"), details)
    with (out/(prefix+"_summary.csv")).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    record = {"round": "UC3", "stage": stage, "source_sha256": source_hashes(),
              "runs": len(rows), "total_attempts": sum(r["attempts"] for r in rows),
              "total_changes": sum(r["ticks"] for r in rows),
              "evidence_sha256": {prefix+s: digest(out/(prefix+s)) for s in SUFFIXES}}
    if stage == "calibration":
        record.update(calibration_metrics(rows))
        c = spec[stage]
        record["conditional_dyck_words"] = dyck_completions(0, 0, False, c["buds_per_period"], c["snapshot_interval"], c["null_observed_height_min"])
        record["claim_limit"] = "Measured composite observer references, not a matched full-law candidate null or a physics result."
    else:
        record.update(calibration_sha256=calibration_hash,
                      strata=[{"initial_nodes": n, "runs": sum(r["n"] == n for r in rows),
                               "primary_median": median(r["primary"] for r in rows if r["n"] == n),
                               "runs_with_qualifying_windows": sum(r["qualifying_windows"] > 0 for r in rows if r["n"] == n),
                               "runs_with_size_core_exposure": sum(r["size_core_eligible_windows"] > 0 for r in rows if r["n"] == n),
                               "stops": dict(Counter(r["stop"] for r in rows if r["n"] == n))}
                              for n in spec[stage]["node_counts"]],
                      claim_limit=spec["claim_limit"], candidate_effect_gate="not_defined_descriptive_only")
    _json(out/(prefix+".json"), record)
    return record


def verify(stage: str, out: Path) -> dict:
    prefix = "UC3_" + stage
    record = json.loads((out/(prefix+".json")).read_text())
    spec = json.loads(SPEC.read_text())
    if record.get("round") != "UC3" or record.get("stage") != stage or record.get("source_sha256") != source_hashes():
        raise RuntimeError("Wrong evidence identity or stale source/protocol")
    expected_files = {prefix+s for s in SUFFIXES}
    if set(record.get("evidence_sha256", {})) != expected_files:
        raise RuntimeError("Incomplete/unexpected evidence manifest")
    for name, value in record["evidence_sha256"].items():
        if digest(out/name) != value:
            raise RuntimeError("Evidence checksum mismatch: " + name)
    calibration_hash = None
    if stage == "candidate":
        verify("calibration", out)
        calpath = out/"UC3_calibration.json"
        if not json.loads(calpath.read_text())["reference_gate_pass"]:
            raise RuntimeError("Candidate lacks qualified references")
        calibration_hash = digest(calpath)
    with tempfile.TemporaryDirectory(prefix="uc3-replay-") as tmp:
        regenerated = _execute(stage, spec, Path(tmp), calibration_hash)
    if regenerated != record:
        raise RuntimeError("Seeded replay, schedule, summaries, observer or gate differ")
    return {"stage": stage, "replayed_runs": record["runs"], "replayed_attempts": record["total_attempts"],
            "replayed_changes": record["total_changes"], "all_products_match": True}


def measure(stage: str, out: Path) -> dict:
    prefix = "UC3_" + stage
    if any((out/(prefix+s)).exists() for s in (".json", *SUFFIXES)):
        raise FileExistsError("Refusing to overwrite UC3 evidence")
    spec = json.loads(SPEC.read_text())
    calibration_hash = None
    if stage == "candidate":
        verify("calibration", out)
        path = out/"UC3_calibration.json"
        if not json.loads(path.read_text())["reference_gate_pass"]:
            raise RuntimeError("Reference gate failed; stop before candidate")
        calibration_hash = digest(path)
    return _execute(stage, spec, out, calibration_hash)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("calibration", "candidate"))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify(args.stage, args.out) if args.verify else measure(args.stage, args.out), indent=2))
