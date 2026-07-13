#!/usr/bin/env python3
"""v16b history-intrinsic event-DAG and scheduler robustness gate.

The primary object is a dependency DAG over executed concrete events. Edges
are induced only by declared read/write conflicts. The strongest check replays
several different topological orders of each DAG and requires the exact same
final graph and token placement.

This is an architecture experiment. It does not test Lorentz symmetry,
spacetime, particles, entanglement, or universal causal structure.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v16a_disjoint_event_commutation_gate as v16a
import relational_universe_v16ac_local_seed_adapter_gate as v16ac


DOC = Path("Documentation")
PURPOSE_REF = "purpose://prompt.unknown"
SOURCE_TARGET = DOC / "v16ac_target_summary.csv"
SOURCE_GATES = DOC / "v16ac_gate_evaluation.csv"
PREREG = DOC / "v16b_pre_registration.csv"
TARGET_NODES = 1024
GROWTH_SEEDS = (2801, 2903)
RUN_OFFSETS = (41011, 41047, 41081)
ARMS = ("current_global", "exposure_matched_local")
STEPS = 2048
TOPOLOGICAL_REPLAYS = 4
COMMUTATION_CANDIDATES = 512
MAX_COMMUTATION_TESTS = 128
MIN_COMMUTATION_TESTS_PER_RUN = 64
TOLERANCE = 1.0e-12

MAX_LOCAL_METRIC_CV = 0.35
GROWTH_MEDIAN_RATIO_RANGE = (0.60, 1.67)
SCHEDULER_MEDIAN_RATIO_RANGE = (0.60, 1.67)
MAX_NONSEED_EVENT_TV = 0.05
MIN_REORDERED_POSITION_FRACTION = 0.10
MIN_LAYER_WIDTH_FRACTION = 0.01
MAX_COMPARABLE_PAIR_FRACTION = 0.95

DAG_METRICS = (
    "causal_depth_fraction",
    "max_layer_width_fraction",
    "comparable_pair_fraction",
)
EVENT_TYPES = ("seed", "birth", "move", "swap", "stuck", "death", "delete", "triad")


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    records = list(rows)
    if not records:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: List[str] = []
    for row in records:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def safe_float(value: Any, default: float = float("nan")) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def fmt(value: Any, digits: int = 6) -> str:
    number = safe_float(value)
    return str(value) if not math.isfinite(number) else f"{number:.{digits}f}"


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row.get(field, "")) for field in fields) + " |")
    return lines


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mean(values: Iterable[float]) -> float:
    data = list(values)
    return sum(data) / len(data) if data else float("nan")


def median(values: Iterable[float]) -> float:
    data = list(values)
    return statistics.median(data) if data else float("nan")


def coefficient_of_variation(values: Iterable[float]) -> float:
    data = list(values)
    center = mean(data)
    if len(data) < 2 or abs(center) <= TOLERANCE:
        return 0.0 if data and all(abs(value) <= TOLERANCE for value in data) else float("inf")
    return statistics.stdev(data) / abs(center)


def ratio(numerator: float, denominator: float) -> float:
    if abs(denominator) <= TOLERANCE:
        return 1.0 if abs(numerator) <= TOLERANCE else float("inf")
    return numerator / denominator


def source_contract_rows() -> Tuple[List[Dict[str, Any]], bool, float]:
    target_rows = read_csv(SOURCE_TARGET)
    gate_rows = read_csv(SOURCE_GATES)
    if len(target_rows) != 1:
        raise ValueError("v16ac target summary must have exactly one row")
    target = target_rows[0]
    overall = [row for row in gate_rows if row["gate"] == "v16ac_overall"]
    local_rate = float(target["frozen_local_rate"])
    rows = [
        {
            "check": "v16ac_overall",
            "observed": overall[0]["status"] if len(overall) == 1 else f"rows={len(overall)}",
            "required": "pass_adapter_to_v16b",
            "status": "pass" if len(overall) == 1 and overall[0]["status"] == "pass_adapter_to_v16b" else "fail",
        },
        {
            "check": "v16ac_target_status",
            "observed": target["status"],
            "required": "pass_adapter_to_v16b",
            "status": "pass" if target["status"] == "pass_adapter_to_v16b" else "fail",
        },
        {
            "check": "v16ac_frozen_rate",
            "observed": local_rate,
            "required": v16ac.FROZEN_LOCAL_RATE,
            "status": "pass" if abs(local_rate - v16ac.FROZEN_LOCAL_RATE) <= TOLERANCE else "fail",
        },
        {
            "check": "core_anchor_not_promoted",
            "observed": target["core_anchor_promoted"],
            "required": 0,
            "status": "pass" if int(target["core_anchor_promoted"]) == 0 else "fail",
        },
        {
            "check": "v16ac_all_subgates",
            "observed": sum(row["status"] != "pass" for row in gate_rows if row["gate"] != "v16ac_overall"),
            "required": 0,
            "status": "pass" if all(row["status"] == "pass" for row in gate_rows if row["gate"] != "v16ac_overall") else "fail",
        },
    ]
    return rows, all(row["status"] == "pass" for row in rows), local_rate


def frozen_spec(local_rate: float) -> Dict[str, Any]:
    return {
        "purpose_ref": PURPOSE_REF,
        "source_target_sha256": file_sha256(SOURCE_TARGET),
        "target_nodes": TARGET_NODES,
        "growth_seeds": list(GROWTH_SEEDS),
        "run_offsets": list(RUN_OFFSETS),
        "arms": list(ARMS),
        "steps": STEPS,
        "topological_replays": TOPOLOGICAL_REPLAYS,
        "local_rate": local_rate,
        "thresholds": {
            "commutation_candidates": COMMUTATION_CANDIDATES,
            "max_commutation_tests": MAX_COMMUTATION_TESTS,
            "min_commutation_tests_per_run": MIN_COMMUTATION_TESTS_PER_RUN,
            "max_local_metric_cv": MAX_LOCAL_METRIC_CV,
            "growth_median_ratio_range": list(GROWTH_MEDIAN_RATIO_RANGE),
            "scheduler_median_ratio_range": list(SCHEDULER_MEDIAN_RATIO_RANGE),
            "max_nonseed_event_tv": MAX_NONSEED_EVENT_TV,
            "min_reordered_position_fraction": MIN_REORDERED_POSITION_FRACTION,
            "min_layer_width_fraction": MIN_LAYER_WIDTH_FRACTION,
            "max_comparable_pair_fraction": MAX_COMPARABLE_PAIR_FRACTION,
        },
    }


def spec_digest(spec: Mapping[str, Any]) -> str:
    payload = json.dumps(spec, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def run_seed(growth_seed: int, run_offset: int, arm: str) -> int:
    arm_code = {"current_global": 0, "exposure_matched_local": 1}[arm]
    return TARGET_NODES * 1_000_000 + growth_seed * 10_000 + run_offset + arm_code * 100_000_000 + 16_002


def preregistration_rows(local_rate: float) -> List[Dict[str, Any]]:
    digest = spec_digest(frozen_spec(local_rate))
    rows: List[Dict[str, Any]] = []
    for growth_seed in GROWTH_SEEDS:
        for run_offset in RUN_OFFSETS:
            for arm in ARMS:
                rows.append({
                    "purpose_ref": PURPOSE_REF,
                    "spec_digest": digest,
                    "source_target_sha256": file_sha256(SOURCE_TARGET),
                    "target_nodes": TARGET_NODES,
                    "growth_seed": growth_seed,
                    "run_offset": run_offset,
                    "arm": arm,
                    "run_seed": run_seed(growth_seed, run_offset, arm),
                    "steps": STEPS,
                    "topological_replays": TOPOLOGICAL_REPLAYS,
                    "frozen_local_rate": local_rate,
                    "independent_arm_rng": 1,
                    "independent_arm_id_allocator": 1,
                    "max_local_metric_cv": MAX_LOCAL_METRIC_CV,
                    "growth_ratio_low": GROWTH_MEDIAN_RATIO_RANGE[0],
                    "growth_ratio_high": GROWTH_MEDIAN_RATIO_RANGE[1],
                    "scheduler_ratio_low": SCHEDULER_MEDIAN_RATIO_RANGE[0],
                    "scheduler_ratio_high": SCHEDULER_MEDIAN_RATIO_RANGE[1],
                    "max_nonseed_event_tv": MAX_NONSEED_EVENT_TV,
                    "prepared_before_fresh_dynamics": 1,
                })
    return rows


def prepare() -> None:
    source_rows, source_pass, local_rate = source_contract_rows()
    if not source_pass:
        raise RuntimeError(f"v16ac source contract failed: {source_rows}")
    rows = preregistration_rows(local_rate)
    write_csv(PREREG, rows)
    print(f"[v16b] prepared rows={len(rows)} digest={rows[0]['spec_digest']}")


def load_and_verify_preregistration() -> Tuple[List[Dict[str, str]], float, List[Dict[str, Any]]]:
    if not PREREG.exists():
        raise ValueError("missing v16b preregistration; run --prepare-only first")
    source_rows, source_pass, local_rate = source_contract_rows()
    if not source_pass:
        raise RuntimeError("v16ac source contract no longer passes")
    observed = read_csv(PREREG)
    expected = preregistration_rows(local_rate)
    if len(observed) != len(expected):
        raise ValueError("v16b preregistration row count changed")
    expected_digest = spec_digest(frozen_spec(local_rate))
    if {row["spec_digest"] for row in observed} != {expected_digest}:
        raise ValueError("v16b preregistration digest changed")
    observed_keys = {(int(row["growth_seed"]), int(row["run_offset"]), row["arm"], int(row["run_seed"])) for row in observed}
    expected_keys = {(int(row["growth_seed"]), int(row["run_offset"]), row["arm"], int(row["run_seed"])) for row in expected}
    if observed_keys != expected_keys:
        raise ValueError("v16b preregistration assignments changed")
    return observed, local_rate, source_rows


@dataclass(frozen=True)
class TraceEvent:
    event_id: int
    family: str
    event_type: str
    event: v16a.Event
    reads: Tuple[str, ...]
    writes: Tuple[str, ...]
    dt: float
    time: float


class DependencyDAG:
    """Online conflict DAG using last-writer and readers-since-write frontiers."""

    def __init__(self) -> None:
        self.predecessors: List[Dict[int, Set[str]]] = []
        self.last_writer: Dict[str, int] = {}
        self.readers_since_write: Dict[str, Set[int]] = defaultdict(set)

    def add(self, reads: Iterable[str], writes: Iterable[str]) -> Dict[int, Set[str]]:
        event_id = len(self.predecessors)
        read_set = set(reads)
        write_set = set(writes)
        reasons: Dict[int, Set[str]] = defaultdict(set)
        for resource in read_set:
            writer = self.last_writer.get(resource)
            if writer is not None:
                reasons[writer].add(f"RAW:{resource}")
        for resource in write_set:
            writer = self.last_writer.get(resource)
            if writer is not None:
                reasons[writer].add(f"WAW:{resource}")
            for reader in self.readers_since_write.get(resource, set()):
                reasons[reader].add(f"WAR:{resource}")
        self.predecessors.append({pred: set(values) for pred, values in reasons.items()})
        for resource in read_set.difference(write_set):
            self.readers_since_write[resource].add(event_id)
        for resource in write_set:
            self.last_writer[resource] = event_id
            self.readers_since_write[resource].clear()
        return self.predecessors[-1]

    def analyze(self) -> Dict[str, Any]:
        n_events = len(self.predecessors)
        successors: List[Set[int]] = [set() for _ in range(n_events)]
        depths: List[int] = []
        ancestor_bits: List[int] = []
        witness_errors = 0
        for child, predecessor_map in enumerate(self.predecessors):
            bits = 0
            depth = 0
            for pred, reasons in predecessor_map.items():
                witness_errors += int(pred >= child or not reasons)
                successors[pred].add(child)
                bits |= ancestor_bits[pred] | (1 << pred)
                depth = max(depth, depths[pred] + 1)
            ancestor_bits.append(bits)
            depths.append(depth)
        edge_count = sum(len(row) for row in self.predecessors)
        layer_counts = Counter(depths)
        causal_depth = max(depths, default=-1) + 1
        comparable_pairs = sum(bits.bit_count() for bits in ancestor_bits)
        possible_pairs = n_events * (n_events - 1) // 2
        return {
            "n_events": n_events,
            "edge_count": edge_count,
            "direct_edges_per_event": edge_count / n_events if n_events else 0.0,
            "root_count": sum(not row for row in self.predecessors),
            "sink_count": sum(not row for row in successors),
            "causal_depth": causal_depth,
            "causal_depth_fraction": causal_depth / n_events if n_events else 0.0,
            "max_layer_width": max(layer_counts.values(), default=0),
            "max_layer_width_fraction": max(layer_counts.values(), default=0) / n_events if n_events else 0.0,
            "mean_layer_width": n_events / causal_depth if causal_depth else 0.0,
            "comparable_pairs": comparable_pairs,
            "comparable_pair_fraction": comparable_pairs / possible_pairs if possible_pairs else 0.0,
            "max_indegree": max((len(row) for row in self.predecessors), default=0),
            "max_outdegree": max((len(row) for row in successors), default=0),
            "acyclic": int(witness_errors == 0),
            "edge_witness_errors": witness_errors,
            "depths": depths,
            "ancestor_bits": ancestor_bits,
            "successors": successors,
        }


def choose_family(rates: Mapping[str, float], rng: random.Random) -> Tuple[str, float]:
    total = sum(max(0.0, float(rates[family])) for family in ("seed", "token", "birth", "death"))
    if total <= 0.0:
        return "noop", 0.0
    draw = rng.random() * total
    cumulative = 0.0
    for family in ("seed", "token", "birth", "death"):
        cumulative += max(0.0, float(rates[family]))
        if draw <= cumulative:
            return family, total
    return "death", total


def materialize_event(family: str, descriptor: Tuple[Any, ...], manager: v7.PairManager) -> v16a.Event:
    event = v16a.Event(family, tuple(descriptor))
    if event.kind == "seed":
        return v16a.Event(family, tuple(descriptor), new_node_id=manager.next_node_id)
    if event.kind == "birth":
        return v16a.Event(family, tuple(descriptor), new_token_id=manager.next_token_id)
    return event


def edge_rows(prefix: Mapping[str, Any], dag: DependencyDAG) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for child, predecessor_map in enumerate(dag.predecessors):
        for pred, reason_values in sorted(predecessor_map.items()):
            reasons = sorted(reason_values)
            rows.append({
                **prefix,
                "parent_event_id": pred,
                "parent_step": pred + 1,
                "child_event_id": child,
                "child_step": child + 1,
                "conflict_types": ";".join(sorted({reason.split(":", 1)[0] for reason in reasons})),
                "witness_resources": ";".join(sorted({reason.split(":", 1)[1] for reason in reasons})),
                "witness_count": len(reasons),
            })
    return rows


def random_topological_order(dag: DependencyDAG, rng: random.Random) -> List[int]:
    n_events = len(dag.predecessors)
    successors: List[List[int]] = [[] for _ in range(n_events)]
    indegrees = [len(row) for row in dag.predecessors]
    for child, predecessors in enumerate(dag.predecessors):
        for pred in predecessors:
            successors[pred].append(child)
    ready = [index for index, degree in enumerate(indegrees) if degree == 0]
    order: List[int] = []
    while ready:
        selected = rng.randrange(len(ready))
        event_id = ready.pop(selected)
        order.append(event_id)
        for child in successors[event_id]:
            indegrees[child] -= 1
            if indegrees[child] == 0:
                ready.append(child)
    if len(order) != n_events:
        raise RuntimeError("dependency graph is cyclic")
    return order


def replay_order(
    initial_state: v7.State,
    final_state: v7.State,
    trace: Sequence[TraceEvent],
    dag: DependencyDAG,
    params: v7.Params,
    prefix: Mapping[str, Any],
    run_seed_value: int,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    original = list(range(len(trace)))
    for replay_index in range(TOPOLOGICAL_REPLAYS):
        replay_seed = run_seed_value + 70_000_019 + replay_index * 104_729
        order = random_topological_order(dag, random.Random(replay_seed))
        positions = {event_id: position for position, event_id in enumerate(order)}
        order_valid = all(positions[pred] < positions[child] for child, predecessors in enumerate(dag.predecessors) for pred in predecessors)
        state = initial_state.clone()
        context_failures = 0
        for event_id in order:
            item = trace[event_id]
            context = v16a.apply_event(state, item.event, params)
            context_failures += int(str(context.get("event", "")) != item.event_type)
        changed_positions = sum(left != right for left, right in zip(order, original))
        rows.append({
            **prefix,
            "replay_index": replay_index,
            "replay_seed": replay_seed,
            "order_sha256": hashlib.sha256(",".join(map(str, order)).encode("utf-8")).hexdigest(),
            "topological_order_valid": int(order_valid),
            "changed_positions": changed_positions,
            "changed_position_fraction": changed_positions / len(order) if order else 0.0,
            "context_failures": context_failures,
            "final_structure_equal": int(v7.states_equal(state, final_state)),
        })
    return rows


def map_resource(resource: str, mapping: Mapping[int, int]) -> str:
    parts = resource.split(":")
    if parts[0] in {"node", "adj"}:
        return f"{parts[0]}:{mapping[int(parts[1])]}"
    if parts[0] == "edge":
        left, right = sorted((mapping[int(parts[1])], mapping[int(parts[2])]))
        return f"edge:{left}:{right}"
    return resource


def relabel_replay(
    initial_state: v7.State,
    final_state: v7.State,
    trace: Sequence[TraceEvent],
    dag: DependencyDAG,
    params: v7.Params,
    prefix: Mapping[str, Any],
) -> Dict[str, Any]:
    initial_nodes = sorted(int(node) for node in initial_state.g.nodes())
    targets = list(reversed([500_000 + index for index in range(len(initial_nodes))]))
    mapping: Dict[int, int] = dict(zip(initial_nodes, targets))
    relabelled_state = v16a.relabel_state(initial_state, mapping)
    relabelled_dag = DependencyDAG()
    support_mismatches = 0
    context_failures = 0
    for item in trace:
        if item.event.new_node_id is not None:
            mapping[int(item.event.new_node_id)] = 1_000_000 + int(item.event.new_node_id)
        mapped_event = v16a.map_event(item.event, mapping)
        relabelled_reads, relabelled_writes = v16a.action_access(relabelled_state, mapped_event)
        expected_reads = {map_resource(resource, mapping) for resource in item.reads}
        expected_writes = {map_resource(resource, mapping) for resource in item.writes}
        support_mismatches += int(expected_reads != relabelled_reads or expected_writes != relabelled_writes)
        relabelled_dag.add(relabelled_reads, relabelled_writes)
        context = v16a.apply_event(relabelled_state, mapped_event, params)
        context_failures += int(str(context.get("event", "")) != item.event_type)
    transported_final = v16a.relabel_state(final_state, mapping)
    original_edges = {(pred, child) for child, predecessors in enumerate(dag.predecessors) for pred in predecessors}
    relabelled_edges = {(pred, child) for child, predecessors in enumerate(relabelled_dag.predecessors) for pred in predecessors}
    original_analysis = dag.analyze()
    relabelled_analysis = relabelled_dag.analyze()
    return {
        **prefix,
        "events": len(trace),
        "support_mismatch_events": support_mismatches,
        "context_failures": context_failures,
        "edge_set_equal": int(original_edges == relabelled_edges),
        "depth_sequence_equal": int(original_analysis["depths"] == relabelled_analysis["depths"]),
        "final_structure_equal": int(v7.states_equal(relabelled_state, transported_final)),
        "relabel_pass": int(
            support_mismatches == 0
            and context_failures == 0
            and original_edges == relabelled_edges
            and original_analysis["depths"] == relabelled_analysis["depths"]
            and v7.states_equal(relabelled_state, transported_final)
        ),
    }


def adjacent_commutation_audit(
    initial_state: v7.State,
    final_state: v7.State,
    trace: Sequence[TraceEvent],
    params: v7.Params,
    prefix: Mapping[str, Any],
    run_seed_value: int,
) -> Dict[str, Any]:
    candidate_count = min(COMMUTATION_CANDIDATES, max(0, len(trace) - 1))
    candidate_indices = set(random.Random(run_seed_value + 90_000_011).sample(range(len(trace) - 1), candidate_count))
    state = initial_state.clone()
    tested = 0
    failures = 0
    invalid_candidates = 0
    max_tests = MAX_COMMUTATION_TESTS
    for index, item in enumerate(trace):
        if index < len(trace) - 1 and index in candidate_indices and tested < max_tests:
            right = trace[index + 1]
            try:
                disjoint, _ = v16a.are_disjoint(state, item.event, right.event)
            except (KeyError, AssertionError):
                invalid_candidates += 1
                disjoint = False
            if disjoint:
                ab, ab_context = v16a.run_order(state, item.event, right.event, params)
                ba, ba_context = v16a.run_order(state, right.event, item.event, params)
                valid = (
                    ab_context == (item.event_type, right.event_type)
                    and ba_context == (right.event_type, item.event_type)
                )
                exact = v7.states_equal(ab, ba)
                tested += 1
                failures += int(not (valid and exact))
        context = v16a.apply_event(state, item.event, params)
        invalid_candidates += int(str(context.get("event", "")) != item.event_type)
    return {
        **prefix,
        "candidate_indices": candidate_count,
        "declared_disjoint_tested": tested,
        "commutation_failures": failures,
        "invalid_or_unavailable_candidates": invalid_candidates,
        "sequential_replay_final_equal": int(v7.states_equal(state, final_state)),
        "commutation_pass": int(tested >= MIN_COMMUTATION_TESTS_PER_RUN and failures == 0 and v7.states_equal(state, final_state)),
    }


def run_assignment(
    base: v7.State,
    assignment: Mapping[str, str],
    params: v7.Params,
    adapter: v16ac.LocalSeedClockAdapter,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any], List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    initial_state = base.clone()
    state = base.clone()
    rng = random.Random(int(assignment["run_seed"]))
    next_node_id, next_token_id = v08b.next_ids_from_state(state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)
    dag = DependencyDAG()
    trace: List[TraceEvent] = []
    event_counts: Counter[str] = Counter()
    invalid_events = 0
    total_time = 0.0
    prefix = {
        "growth_seed": int(assignment["growth_seed"]),
        "run_offset": int(assignment["run_offset"]),
        "arm": assignment["arm"],
        "run_seed": int(assignment["run_seed"]),
    }
    for step in range(1, STEPS + 1):
        rates = v7.family_rates(state, params) if assignment["arm"] == "current_global" else adapter.family_rates(state, params)
        family, total_rate = choose_family(rates, rng)
        if total_rate <= 0.0:
            raise RuntimeError("non-positive total rate")
        dt = rng.expovariate(total_rate)
        total_time += dt
        state.t += dt
        kernel = adapter.family_kernel(state, family, params)
        if not kernel:
            raise RuntimeError(f"empty kernel for positive family {family}")
        descriptor = tuple(v7.sample_from_dist(kernel, rng))
        concrete = materialize_event(family, descriptor, manager)
        reads, writes = v16a.action_access(state, concrete)
        dag.add(reads, writes)
        context = adapter.apply_descriptor(state, family, descriptor, params, manager)
        event_type = str(context.get("event", "unknown"))
        invalid_events += int(event_type != concrete.kind)
        if concrete.new_node_id is not None:
            invalid_events += int(int(context.get("new_node", -1)) != concrete.new_node_id)
        if concrete.new_token_id is not None:
            invalid_events += int(int(context.get("new_token_id", -1)) != concrete.new_token_id)
        event_counts[event_type] += 1
        trace.append(TraceEvent(step - 1, family, event_type, concrete, tuple(sorted(reads)), tuple(sorted(writes)), dt, total_time))

    final_state = state.clone()
    analysis = dag.analyze()
    event_rows: List[Dict[str, Any]] = []
    for item in trace:
        predecessors = dag.predecessors[item.event_id]
        event_rows.append({
            **prefix,
            "event_id": item.event_id,
            "step": item.event_id + 1,
            "family": item.family,
            "event_type": item.event_type,
            "descriptor": repr(item.event.descriptor),
            "new_node_id": "" if item.event.new_node_id is None else item.event.new_node_id,
            "new_token_id": "" if item.event.new_token_id is None else item.event.new_token_id,
            "dt": item.dt,
            "time": item.time,
            "read_resources": ";".join(item.reads),
            "write_resources": ";".join(item.writes),
            "direct_predecessors": ";".join(str(pred) for pred in sorted(predecessors)),
            "indegree": len(predecessors),
            "causal_depth": analysis["depths"][item.event_id],
            "ancestor_count": analysis["ancestor_bits"][item.event_id].bit_count(),
        })
    dependency_rows = edge_rows(prefix, dag)
    replay_rows = replay_order(initial_state, final_state, trace, dag, params, prefix, int(assignment["run_seed"]))
    relabel_row = relabel_replay(initial_state, final_state, trace, dag, params, prefix)
    commutation_row = adjacent_commutation_audit(initial_state, final_state, trace, params, prefix, int(assignment["run_seed"]))
    run_row: Dict[str, Any] = {
        **prefix,
        "steps": STEPS,
        "initial_nodes": initial_state.g.num_nodes(),
        "final_nodes": final_state.g.num_nodes(),
        "initial_tokens": initial_state.token_count(),
        "final_tokens": final_state.token_count(),
        "total_time": total_time,
        "invalid_events": invalid_events,
        "topological_replays": len(replay_rows),
        "topological_replay_failures": sum(
            not (
                int(row["topological_order_valid"])
                and int(row["context_failures"]) == 0
                and int(row["final_structure_equal"])
            )
            for row in replay_rows
        ),
        "min_reordered_position_fraction": min(float(row["changed_position_fraction"]) for row in replay_rows),
        "relabel_pass": relabel_row["relabel_pass"],
        "commutation_tests": commutation_row["declared_disjoint_tested"],
        "commutation_failures": commutation_row["commutation_failures"],
        **{key: value for key, value in analysis.items() if key not in {"depths", "ancestor_bits", "successors"}},
    }
    for event_type in EVENT_TYPES:
        run_row[f"{event_type}_events"] = event_counts[event_type]
    return event_rows, dependency_rows, run_row, replay_rows, relabel_row, commutation_row


def arm_summary_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for arm in ARMS:
        subset = [row for row in run_rows if row["arm"] == arm]
        row: Dict[str, Any] = {
            "arm": arm,
            "n_runs": len(subset),
            "total_events": sum(int(item["n_events"]) for item in subset),
            "total_dependency_edges": sum(int(item["edge_count"]) for item in subset),
            "total_topological_replay_failures": sum(int(item["topological_replay_failures"]) for item in subset),
            "total_commutation_failures": sum(int(item["commutation_failures"]) for item in subset),
        }
        for metric in DAG_METRICS:
            values = [float(item[metric]) for item in subset]
            row[f"median_{metric}"] = median(values)
            row[f"mean_{metric}"] = mean(values)
            row[f"cv_{metric}"] = coefficient_of_variation(values)
        for event_type in EVENT_TYPES:
            row[f"total_{event_type}_events"] = sum(int(item[f"{event_type}_events"]) for item in subset)
        rows.append(row)
    return rows


def growth_stability_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    local = [row for row in run_rows if row["arm"] == "exposure_matched_local"]
    rows: List[Dict[str, Any]] = []
    for metric in DAG_METRICS:
        medians = {
            seed: median(float(row[metric]) for row in local if int(row["growth_seed"]) == seed)
            for seed in GROWTH_SEEDS
        }
        value_ratio = ratio(medians[GROWTH_SEEDS[1]], medians[GROWTH_SEEDS[0]])
        rows.append({
            "metric": metric,
            f"growth_{GROWTH_SEEDS[0]}_median": medians[GROWTH_SEEDS[0]],
            f"growth_{GROWTH_SEEDS[1]}_median": medians[GROWTH_SEEDS[1]],
            "second_over_first_ratio": value_ratio,
            "ratio_low": GROWTH_MEDIAN_RATIO_RANGE[0],
            "ratio_high": GROWTH_MEDIAN_RATIO_RANGE[1],
            "growth_stability_pass": int(GROWTH_MEDIAN_RATIO_RANGE[0] <= value_ratio <= GROWTH_MEDIAN_RATIO_RANGE[1]),
        })
    return rows


def nonseed_event_tv(run_rows: Sequence[Mapping[str, Any]]) -> float:
    event_types = ("birth", "move", "swap", "stuck", "death", "delete", "triad")
    distributions: Dict[str, Dict[str, float]] = {}
    for arm in ARMS:
        counts = {event_type: sum(int(row[f"{event_type}_events"]) for row in run_rows if row["arm"] == arm) for event_type in event_types}
        total = sum(counts.values())
        distributions[arm] = {event_type: counts[event_type] / total if total else 0.0 for event_type in event_types}
    return 0.5 * sum(abs(distributions[ARMS[0]][event_type] - distributions[ARMS[1]][event_type]) for event_type in event_types)


def scheduler_fingerprint_rows(
    run_rows: Sequence[Mapping[str, Any]],
    arm_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    lookup = {row["arm"]: row for row in arm_rows}
    tv = nonseed_event_tv(run_rows)
    rows: List[Dict[str, Any]] = []
    for metric in DAG_METRICS:
        global_value = float(lookup["current_global"][f"median_{metric}"])
        local_value = float(lookup["exposure_matched_local"][f"median_{metric}"])
        value_ratio = ratio(local_value, global_value)
        rows.append({
            "metric": metric,
            "current_global_median": global_value,
            "local_median": local_value,
            "local_over_global_ratio": value_ratio,
            "ratio_low": SCHEDULER_MEDIAN_RATIO_RANGE[0],
            "ratio_high": SCHEDULER_MEDIAN_RATIO_RANGE[1],
            "scheduler_metric_pass": int(SCHEDULER_MEDIAN_RATIO_RANGE[0] <= value_ratio <= SCHEDULER_MEDIAN_RATIO_RANGE[1]),
            "nonseed_event_tv": tv,
            "nonseed_tv_pass": int(tv <= MAX_NONSEED_EVENT_TV),
        })
    return rows


def matched_scheduler_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_key: Dict[Tuple[int, int], Dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for row in run_rows:
        by_key[(int(row["growth_seed"]), int(row["run_offset"]))][str(row["arm"])] = row
    rows: List[Dict[str, Any]] = []
    for (growth_seed, run_offset), arms in sorted(by_key.items()):
        if set(arms) != set(ARMS):
            raise ValueError(f"incomplete matched pair {(growth_seed, run_offset)}")
        global_row = arms["current_global"]
        local_row = arms["exposure_matched_local"]
        row: Dict[str, Any] = {"growth_seed": growth_seed, "run_offset": run_offset}
        for metric in DAG_METRICS:
            row[f"global_{metric}"] = global_row[metric]
            row[f"local_{metric}"] = local_row[metric]
            row[f"local_over_global_{metric}"] = ratio(float(local_row[metric]), float(global_row[metric]))
        rows.append(row)
    return rows


def gate_evaluation(
    source_pass: bool,
    target_rows: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    replay_rows: Sequence[Mapping[str, Any]],
    relabel_rows: Sequence[Mapping[str, Any]],
    commutation_rows: Sequence[Mapping[str, Any]],
    arm_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], str]:
    expected_runs = len(GROWTH_SEEDS) * len(RUN_OFFSETS) * len(ARMS)
    target_pass = len(target_rows) == 1 and int(target_rows[0]["separated_from_prev"]) == 1
    run_integrity = len(run_rows) == expected_runs and all(int(row["n_events"]) == STEPS and int(row["invalid_events"]) == 0 for row in run_rows)
    dag_integrity = all(int(row["acyclic"]) and int(row["edge_witness_errors"]) == 0 and int(row["edge_count"]) > 0 for row in run_rows)
    replay_pass = (
        len(replay_rows) == expected_runs * TOPOLOGICAL_REPLAYS
        and all(int(row["topological_order_valid"]) and int(row["context_failures"]) == 0 and int(row["final_structure_equal"]) for row in replay_rows)
        and all(float(row["changed_position_fraction"]) >= MIN_REORDERED_POSITION_FRACTION for row in replay_rows)
    )
    relabel_pass = len(relabel_rows) == expected_runs and all(int(row["relabel_pass"]) for row in relabel_rows)
    commutation_pass = (
        len(commutation_rows) == expected_runs
        and all(int(row["declared_disjoint_tested"]) >= MIN_COMMUTATION_TESTS_PER_RUN for row in commutation_rows)
        and all(int(row["commutation_failures"]) == 0 and int(row["sequential_replay_final_equal"]) for row in commutation_rows)
    )
    nontrivial = all(
        1 < int(row["causal_depth"]) < STEPS
        and float(row["max_layer_width_fraction"]) >= MIN_LAYER_WIDTH_FRACTION
        and 0.0 < float(row["comparable_pair_fraction"]) <= MAX_COMPARABLE_PAIR_FRACTION
        for row in run_rows
    )
    local_arm = next(row for row in arm_rows if row["arm"] == "exposure_matched_local")
    local_cv_values = [float(local_arm[f"cv_{metric}"]) for metric in DAG_METRICS]
    local_stability = all(value <= MAX_LOCAL_METRIC_CV for value in local_cv_values)
    growth_stability = all(int(row["growth_stability_pass"]) for row in growth_rows)
    scheduler_stability = all(int(row["scheduler_metric_pass"]) and int(row["nonseed_tv_pass"]) for row in scheduler_rows)
    exact_architecture_pass = all((source_pass, target_pass, run_integrity, dag_integrity, replay_pass, relabel_pass, commutation_pass, nontrivial))
    all_pass = exact_architecture_pass and local_stability and growth_stability and scheduler_stability
    if all_pass:
        overall = "pass_to_v16c_coarse_graining_pilot"
    elif exact_architecture_pass:
        overall = "event_dag_valid_but_coarse_stability_not_yet"
    else:
        overall = "event_dag_support_incomplete"
    gates = [
        {"gate": "v16ac_source_contract", "status": "pass" if source_pass else "fail", "observed": int(source_pass), "required": 1, "decision": "continue"},
        {"gate": "target_hygiene", "status": "pass" if target_pass else "fail", "observed": target_rows[0]["separated_from_prev"] if len(target_rows) == 1 else len(target_rows), "required": 1, "decision": "continue"},
        {"gate": "run_integrity", "status": "pass" if run_integrity else "fail", "observed": f"runs={len(run_rows)};invalid={sum(int(row['invalid_events']) for row in run_rows)}", "required": f"runs={expected_runs};invalid=0", "decision": "continue"},
        {"gate": "dag_acyclic_witnessed", "status": "pass" if dag_integrity else "fail", "observed": f"runs={sum(int(row['acyclic']) for row in run_rows)};witness_errors={sum(int(row['edge_witness_errors']) for row in run_rows)}", "required": f"runs={expected_runs};witness_errors=0", "decision": "continue"},
        {"gate": "topological_replay_invariance", "status": "pass" if replay_pass else "fail", "observed": f"replays={len(replay_rows)};failures={sum(not int(row['final_structure_equal']) or int(row['context_failures']) for row in replay_rows)};min_reorder={min(float(row['changed_position_fraction']) for row in replay_rows):.6f}", "required": f"replays={expected_runs * TOPOLOGICAL_REPLAYS};failures=0;min_reorder>={MIN_REORDERED_POSITION_FRACTION}", "decision": "continue" if replay_pass else "revise_support_schema"},
        {"gate": "concrete_relabel_replay", "status": "pass" if relabel_pass else "fail", "observed": sum(int(row["relabel_pass"]) for row in relabel_rows), "required": expected_runs, "decision": "continue" if relabel_pass else "revise_support_schema"},
        {"gate": "adjacent_disjoint_commutation", "status": "pass" if commutation_pass else "fail", "observed": f"min_tests={min(int(row['declared_disjoint_tested']) for row in commutation_rows)};failures={sum(int(row['commutation_failures']) for row in commutation_rows)}", "required": f"min_tests>={MIN_COMMUTATION_TESTS_PER_RUN};failures=0", "decision": "continue" if commutation_pass else "revise_support_schema"},
        {"gate": "nontrivial_partial_order", "status": "pass" if nontrivial else "fail", "observed": f"depth={min(int(row['causal_depth']) for row in run_rows)}-{max(int(row['causal_depth']) for row in run_rows)};width_fraction={min(float(row['max_layer_width_fraction']) for row in run_rows):.6f}-{max(float(row['max_layer_width_fraction']) for row in run_rows):.6f}", "required": "1<depth<steps;nonzero antichain and comparability", "decision": "continue"},
        {"gate": "local_dag_metric_cv", "status": "pass" if local_stability else "fail", "observed": ";".join(f"{metric}={value:.6f}" for metric, value in zip(DAG_METRICS, local_cv_values)), "required": f"each<={MAX_LOCAL_METRIC_CV}", "decision": "continue" if local_stability else "hold_v16c"},
        {"gate": "growth_seed_transfer", "status": "pass" if growth_stability else "fail", "observed": ";".join(f"{row['metric']}={float(row['second_over_first_ratio']):.6f}" for row in growth_rows), "required": f"each in [{GROWTH_MEDIAN_RATIO_RANGE[0]},{GROWTH_MEDIAN_RATIO_RANGE[1]}]", "decision": "continue" if growth_stability else "hold_v16c"},
        {"gate": "scheduler_coarse_fingerprint", "status": "pass" if scheduler_stability else "fail", "observed": ";".join(f"{row['metric']}={float(row['local_over_global_ratio']):.6f}" for row in scheduler_rows) + f";tv={float(scheduler_rows[0]['nonseed_event_tv']):.6f}", "required": f"ratios in [{SCHEDULER_MEDIAN_RATIO_RANGE[0]},{SCHEDULER_MEDIAN_RATIO_RANGE[1]}];tv<={MAX_NONSEED_EVENT_TV}", "decision": "continue" if scheduler_stability else "hold_v16c"},
        {"gate": "v16b_overall", "status": overall, "observed": int(all_pass), "required": 1, "decision": "design_v16c_three_scale_pilot" if all_pass else ("refine_coarse_observables" if exact_architecture_pass else "repair_event_support")},
    ]
    return gates, overall


def claim_rows(status: str) -> List[Dict[str, Any]]:
    exact_valid = status in {"pass_to_v16c_coarse_graining_pilot", "event_dag_valid_but_coarse_stability_not_yet"}
    stable = status == "pass_to_v16c_coarse_graining_pilot"
    return [
        {"claim_id": "C1", "statement": "Declared read/write conflicts define an acyclic dependency DAG for every fresh trace.", "status": "supported" if exact_valid else "not_supported", "evidence": "v16b_dependency_edges.csv;v16b_run_summary.csv", "scope_limit": "fresh finite histories under the declared support schema"},
        {"claim_id": "C2", "statement": "Different topological orders of each event DAG reproduce the exact final graph and token placement.", "status": "supported" if exact_valid else "not_supported", "evidence": "v16b_topological_replay_audit.csv", "scope_limit": f"{TOPOLOGICAL_REPLAYS} sampled orders per run, not every linear extension"},
        {"claim_id": "C3", "statement": "Concrete trace support and DAG structure transport under deterministic node relabeling.", "status": "supported" if exact_valid else "not_supported", "evidence": "v16b_relabel_replay_audit.csv", "scope_limit": "same event histories replayed after a deterministic bijection"},
        {"claim_id": "C4", "statement": "Coarse DAG fingerprints are stable enough across fresh bases and scheduler variants to justify a small v16c pilot.", "status": "supported" if stable else "not_supported", "evidence": "v16b_growth_stability.csv;v16b_scheduler_fingerprint.csv;v16b_gate_evaluation.csv", "scope_limit": "broad preregistered bounds, two growth seeds and six runs per arm"},
        {"claim_id": "C5", "statement": "The event DAG is a universal causal order or emergent spacetime.", "status": "unsupported", "evidence": "none", "scope_limit": "history-intrinsic implementation structure is not a universal physics result"},
        {"claim_id": "C6", "statement": "Lorentz symmetry, particles, or entanglement follow from the event-DAG pass.", "status": "unsupported", "evidence": "none", "scope_limit": "not tested by v16b"},
    ]


def build_report(
    source_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    arm_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# UniverseSimulation v16b: history-intrinsic event-DAG gate",
        "",
        "## Research question",
        "",
        "Can executed local events be represented by a nontrivial dependency DAG whose independent linearizations, concrete relabel replay, and adjacent disjoint swaps preserve the same dynamics, and are coarse DAG fingerprints stable across fresh bases and the local/global scheduler contrast?",
        "",
        "## Evidential separation",
        "",
        "- Architecture definition: a directed edge records a declared RAW, WAR, or WAW conflict on a concrete node, token, edge, or adjacency resource.",
        "- Generated artifact: the DAG, causal depths, antichain layers, and comparability counts are computed from each executed event history.",
        "- Actual dynamics: twelve fresh runs were executed after a separate preregistration step, six per scheduler arm.",
        "- Negative boundary: no Lorentz, spacetime, particle, entanglement, or universal-causality claim is tested.",
        "",
        "## Frozen source contract",
        "",
    ]
    lines.extend(table(source_rows, ("check", "observed", "required", "status")))
    lines.extend([
        "",
        "## Design",
        "",
        f"Target `{TARGET_NODES}`, fresh growth seeds `{GROWTH_SEEDS[0]}/{GROWTH_SEEDS[1]}`, three run offsets, `{STEPS}` events, and two independent arms: `current_global` and frozen `exposure_matched_local`. Each trace receives `{TOPOLOGICAL_REPLAYS}` random topological replays.",
        "",
        "The DAG frontier connects a read to the most recent writer, and a write to the most recent writer plus readers since that write. Read/read pairs remain unordered. This is a conflict-dependency DAG for the declared support schema, not a claim that the schema is fundamental physics.",
        "",
        "Target hygiene:",
        "",
    ])
    lines.extend(table(target_rows, ("target_nodes", "growth_replicates", "mean_initial_nodes", "mean_initial_tokens", "mean_initial_beta1", "separated_from_prev")))
    lines.extend(["", "## Run-level DAG results", ""])
    lines.extend(table(run_rows, ("growth_seed", "run_offset", "arm", "n_events", "edge_count", "causal_depth", "causal_depth_fraction", "max_layer_width_fraction", "comparable_pair_fraction", "topological_replay_failures", "relabel_pass", "commutation_tests", "commutation_failures")))
    lines.extend(["", "## Scheduler summaries", ""])
    lines.extend(table(arm_rows, ("arm", "n_runs", "total_events", "total_dependency_edges", "median_causal_depth_fraction", "cv_causal_depth_fraction", "median_max_layer_width_fraction", "cv_max_layer_width_fraction", "median_comparable_pair_fraction", "cv_comparable_pair_fraction")))
    lines.extend(["", "## Fresh-base stability", ""])
    lines.extend(table(growth_rows, ("metric", f"growth_{GROWTH_SEEDS[0]}_median", f"growth_{GROWTH_SEEDS[1]}_median", "second_over_first_ratio", "growth_stability_pass")))
    lines.extend(["", "## Scheduler coarse fingerprint", ""])
    lines.extend(table(scheduler_rows, ("metric", "current_global_median", "local_median", "local_over_global_ratio", "scheduler_metric_pass", "nonseed_event_tv", "nonseed_tv_pass")))
    lines.extend(["", "## Gate evaluation", ""])
    lines.extend(table(gate_rows, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        f"Overall status: `{overall}`.",
        "",
        "## Interpretation",
        "",
        "A topological replay pass would show that the declared dependency structure is operationally sufficient for the sampled histories: many sequential orders are representational choices rather than different outcomes. Relabel replay would show that this structure does not depend on node names.",
        "",
        "Even a full pass remains modest. The DAG is history-intrinsic under the current event vocabulary and support declaration. It is not yet an observer-independent continuum causal order, and stable normalized DAG summaries are not Lorentz symmetry.",
        "",
        "## Next decision",
        "",
    ])
    if overall == "pass_to_v16c_coarse_graining_pilot":
        lines.append("Proceed to one small three-scale v16c pilot. Freeze a coarse-graining map before dynamics and test whether causal-depth, antichain-width, and dependency-density ratios transfer across scales. Keep the local adapter isolated and retain current-global as a diagnostic control.")
    elif overall == "event_dag_valid_but_coarse_stability_not_yet":
        lines.append("Keep the exact event-DAG result, but do not start v16c. Diagnose which coarse observable failed across bases or schedulers, then make one narrow observable refinement without changing event support.")
    else:
        lines.append("Do not start coarse-graining. Inspect replay or relabel counterevidence to find the smallest missing read/write dependency and rerun v16b after repairing the support schema.")
    lines.append("")
    return "\n".join(lines)


def self_test() -> None:
    import networkx as nx

    state = v16a.nx_to_state(nx.path_graph(4), (0, 3))
    params = v16a.anchor_params()
    first = v16a.Event("token", ("move", 0, 0, 1))
    disjoint = v16a.Event("token", ("move", 1, 3, 2))
    reads_a, writes_a = v16a.action_access(state, first)
    reads_b, writes_b = v16a.action_access(state, disjoint)
    dag = DependencyDAG()
    dag.add(reads_a, writes_a)
    dag.add(reads_b, writes_b)
    assert not dag.predecessors[1]
    ab, _ = v16a.run_order(state, first, disjoint, params)
    ba, _ = v16a.run_order(state, disjoint, first, params)
    assert v7.states_equal(ab, ba)
    trace = [
        TraceEvent(0, "token", "move", first, tuple(sorted(reads_a)), tuple(sorted(writes_a)), 0.1, 0.1),
        TraceEvent(1, "token", "move", disjoint, tuple(sorted(reads_b)), tuple(sorted(writes_b)), 0.1, 0.2),
    ]
    prefix = {"growth_seed": -1, "run_offset": -1, "arm": "self_test", "run_seed": 1}
    replays = replay_order(state, ab, trace, dag, params, prefix, 1)
    assert all(int(row["topological_order_valid"]) and int(row["context_failures"]) == 0 and int(row["final_structure_equal"]) for row in replays)
    relabel = relabel_replay(state, ab, trace, dag, params, prefix)
    assert int(relabel["relabel_pass"]) == 1

    dependent_state = state.clone()
    v16a.apply_event(dependent_state, first, params)
    second = v16a.Event("token", ("move", 0, 1, 2))
    reads_c, writes_c = v16a.action_access(dependent_state, second)
    dependent = DependencyDAG()
    dependent.add(reads_a, writes_a)
    dependent.add(reads_c, writes_c)
    assert 0 in dependent.predecessors[1]
    assert dependent.analyze()["acyclic"] == 1
    print("[v16b] self-test pass")


def run() -> None:
    assignments, local_rate, source_rows = load_and_verify_preregistration()
    adapter = v16ac.LocalSeedClockAdapter(local_rate)
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    target_rows = v10e.summarize_bases(base_rows)
    if len(target_rows) != 1 or int(target_rows[0]["separated_from_prev"]) != 1:
        raise RuntimeError("v16b target hygiene failed")
    ensemble_name = ensembles[0].name
    params = v16a.anchor_params()
    event_rows: List[Dict[str, Any]] = []
    dependency_rows: List[Dict[str, Any]] = []
    run_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    relabel_rows: List[Dict[str, Any]] = []
    commutation_rows: List[Dict[str, Any]] = []
    for index, assignment in enumerate(assignments, start=1):
        base = base_states[(ensemble_name, int(assignment["growth_seed"]))]
        events, dependencies, run_row, replays, relabel, commutation = run_assignment(base, assignment, params, adapter)
        event_rows.extend(events)
        dependency_rows.extend(dependencies)
        run_rows.append(run_row)
        replay_rows.extend(replays)
        relabel_rows.append(relabel)
        commutation_rows.append(commutation)
        print(f"[v16b] runs={index}/{len(assignments)} arm={assignment['arm']} edges={run_row['edge_count']} depth={run_row['causal_depth']}")

    arm_rows = arm_summary_rows(run_rows)
    growth_rows = growth_stability_rows(run_rows)
    scheduler_rows = scheduler_fingerprint_rows(run_rows, arm_rows)
    matched_rows = matched_scheduler_rows(run_rows)
    gate_rows, overall = gate_evaluation(source_pass=True, target_rows=target_rows, run_rows=run_rows, replay_rows=replay_rows, relabel_rows=relabel_rows, commutation_rows=commutation_rows, arm_rows=arm_rows, growth_rows=growth_rows, scheduler_rows=scheduler_rows)

    write_csv(DOC / "v16b_source_chain.csv", source_rows)
    write_csv(DOC / "v16b_target_summary.csv", target_rows)
    write_csv(DOC / "v16b_event_log.csv", event_rows)
    write_csv(DOC / "v16b_dependency_edges.csv", dependency_rows)
    write_csv(DOC / "v16b_run_summary.csv", run_rows)
    write_csv(DOC / "v16b_arm_summary.csv", arm_rows)
    write_csv(DOC / "v16b_topological_replay_audit.csv", replay_rows)
    write_csv(DOC / "v16b_relabel_replay_audit.csv", relabel_rows)
    write_csv(DOC / "v16b_adjacent_commutation_audit.csv", commutation_rows)
    write_csv(DOC / "v16b_growth_stability.csv", growth_rows)
    write_csv(DOC / "v16b_scheduler_fingerprint.csv", scheduler_rows)
    write_csv(DOC / "v16b_matched_scheduler_comparison.csv", matched_rows)
    write_csv(DOC / "v16b_gate_evaluation.csv", gate_rows)
    write_csv(DOC / "v16b_claim_ledger.csv", claim_rows(overall))
    report = build_report(source_rows, target_rows, run_rows, arm_rows, growth_rows, scheduler_rows, gate_rows, overall)
    (DOC / "v16b_intrinsic_event_dag_gate.md").write_text(report, encoding="utf-8")
    recommendation = "\n".join([
        "# Operativ anbefaling v0.16b",
        "",
        f"Status: `{overall}`.",
        "",
        "- Behold event-DAG-resultatet avgrenset til deklarert read/write-support og samplede historikker.",
        "- Ved full pass: gaa til en liten, preregistrert tre-skala v16c coarse-graining-pilot.",
        "- Ved eksakt DAG-pass men stabilitetsfail: raffiner bare den svake coarse-observabelen; ikke endre event-support.",
        "- Ved replay/relabel-fail: reparer minste manglende supportavhengighet og rerun v16b.",
        "- Ikke promoter event-DAG til spacetime, Lorentz-symmetri eller universell kausal orden.",
        "",
    ])
    (DOC / "v0_16b_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    lay = "\n".join([
        "# v0.16b for ikke-spesialister",
        "",
        "Vi gjorde hver faktisk hendelse til et punkt i en avhengighetsgraf. En pil betyr at en senere hendelse leser eller endrer noe en tidligere hendelse brukte eller endret.",
        "",
        "Den viktigste proeven stokker om hendelser som grafen sier er uavhengige, men respekterer alle pilene. Dersom mange slike rekkefolger ender i eksakt samme graf og tokenplassering, er mye av den opprinnelige sekvensen bare en representasjonsrekkefolge, ikke en fysisk avhengighet.",
        "",
        f"Statusen i denne runden er `{overall}`. Selv ved pass er dette en kontrollert kausal arkitektur i modellen, ikke et bevis for romtid eller relativitet.",
        "",
    ])
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16b.md").write_text(lay, encoding="utf-8")
    print(f"[v16b] overall={overall} runs={len(run_rows)} events={len(event_rows)} edges={len(dependency_rows)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16b intrinsic event-DAG gate")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif args.prepare_only:
        prepare()
    else:
        run()


if __name__ == "__main__":
    main()
