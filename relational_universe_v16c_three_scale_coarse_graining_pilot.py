#!/usr/bin/env python3
"""v16c preregistered three-scale event-DAG coarse-graining pilot.

The frozen map bins fine events by causal depth and contracts direct-edge
connected components inside each depth window. Quotient edges retain concrete
fine-edge witnesses. The map uses neither graph node labels nor scheduler order.

This is an architecture experiment. It does not test continuum limits, Lorentz
symmetry, spacetime, particles, entanglement, or universal causal structure.
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
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v16a_disjoint_event_commutation_gate as v16a
import relational_universe_v16ac_local_seed_adapter_gate as v16ac
import relational_universe_v16b_intrinsic_event_dag_gate as v16b


DOC = Path("Documentation")
PURPOSE_REF = "purpose://prompt.unknown"
SOURCE_GATE = DOC / "v16b_gate_evaluation.csv"
SOURCE_TARGET = DOC / "v16b_target_summary.csv"
SOURCE_EVENTS = DOC / "v16b_event_log.csv"
SOURCE_EDGES = DOC / "v16b_dependency_edges.csv"
DESIGN_CALIBRATION = DOC / "v16c_design_calibration.csv"
PREREG = DOC / "v16c_pre_registration.csv"

TARGET_NODES = 1024
GROWTH_SEEDS = (3109, 3203)
RUN_OFFSETS = (51017, 51059, 51091)
ARMS = ("current_global", "exposure_matched_local")
STEPS = 2048
TOPOLOGICAL_REPLAYS = 2
SCALE_WINDOWS = (1, 4, 16)
TRANSITIONS = ((1, 4), (4, 16))
PRIMARY_METRICS = (
    "causal_depth_retention",
    "antichain_width_retention",
    "dependency_density_retention",
)
EVENT_TYPES = v16b.EVENT_TYPES
TOLERANCE = 1.0e-12

MAX_LOCAL_TRANSITION_CV = 0.40
GROWTH_MEDIAN_RATIO_RANGE = (0.60, 1.67)
SCHEDULER_MEDIAN_RATIO_RANGE = (0.60, 1.67)
MAX_NONSEED_EVENT_TV = 0.05
MIN_REORDERED_POSITION_FRACTION = 0.10
MIN_SCALE16_COARSE_NODES = 16
MIN_SCALE16_NODE_RETENTION = 0.01
MAX_SCALE16_NODE_RETENTION = 0.90


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


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, item: int) -> int:
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != item:
            parent = self.parent[item]
            self.parent[item] = root
            item = parent
        return root

    def union(self, left: int, right: int) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1


def analyze_edges(node_count: int, edges: Set[Tuple[int, int]]) -> Dict[str, Any]:
    predecessors: List[Set[int]] = [set() for _ in range(node_count)]
    successors: List[Set[int]] = [set() for _ in range(node_count)]
    invalid_edges = 0
    for parent, child in edges:
        if parent == child or not (0 <= parent < node_count and 0 <= child < node_count):
            invalid_edges += 1
            continue
        predecessors[child].add(parent)
        successors[parent].add(child)
    indegrees = [len(row) for row in predecessors]
    ready = sorted(index for index, degree in enumerate(indegrees) if degree == 0)
    order: List[int] = []
    while ready:
        node = ready.pop(0)
        order.append(node)
        for child in sorted(successors[node]):
            indegrees[child] -= 1
            if indegrees[child] == 0:
                ready.append(child)
                ready.sort()
    acyclic = len(order) == node_count and invalid_edges == 0
    depths = [0] * node_count
    ancestor_bits = [0] * node_count
    if acyclic:
        for node in order:
            bits = 0
            depth = 0
            for parent in predecessors[node]:
                bits |= ancestor_bits[parent] | (1 << parent)
                depth = max(depth, depths[parent] + 1)
            ancestor_bits[node] = bits
            depths[node] = depth
    layer_counts = Counter(depths)
    comparable_pairs = sum(bits.bit_count() for bits in ancestor_bits)
    possible_pairs = node_count * (node_count - 1) // 2
    edge_count = len(edges)
    causal_depth = max(depths, default=-1) + 1 if acyclic else 0
    return {
        "node_count": node_count,
        "edge_count": edge_count,
        "dependency_density": edge_count / node_count if node_count else 0.0,
        "causal_depth": causal_depth,
        "max_layer_width": max(layer_counts.values(), default=0) if acyclic else 0,
        "comparable_pair_fraction": comparable_pairs / possible_pairs if possible_pairs else 0.0,
        "acyclic": int(acyclic),
        "invalid_edges": invalid_edges,
    }


def coarse_grain(
    dag: v16b.DependencyDAG,
    window: int,
    prefix: Mapping[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any], Dict[str, Any]]:
    fine = dag.analyze()
    depths = list(fine["depths"])
    n_events = len(depths)
    union_find = UnionFind(n_events)
    fine_edges: List[Tuple[int, int, Set[str]]] = []
    for child, predecessor_map in enumerate(dag.predecessors):
        for parent, reasons in predecessor_map.items():
            fine_edges.append((parent, child, set(reasons)))
            if depths[parent] // window == depths[child] // window:
                union_find.union(parent, child)

    grouped: Dict[int, List[int]] = defaultdict(list)
    for event_id in range(n_events):
        grouped[union_find.find(event_id)].append(event_id)
    if window == 1:
        groups = sorted(grouped.values(), key=min)
    else:
        groups = sorted(grouped.values(), key=lambda members: (depths[members[0]] // window, min(members)))
    event_to_coarse: Dict[int, int] = {}
    for coarse_id, members in enumerate(groups):
        for event_id in members:
            event_to_coarse[event_id] = coarse_id

    membership_rows: List[Dict[str, Any]] = []
    depth_bin_errors = 0
    for coarse_id, members in enumerate(groups):
        bins = {depths[event_id] // window for event_id in members}
        depth_bin_errors += int(len(bins) != 1)
        for event_id in members:
            membership_rows.append({
                **prefix,
                "scale_window": window,
                "event_id": event_id,
                "fine_causal_depth": depths[event_id],
                "depth_bin": depths[event_id] // window,
                "coarse_event_id": coarse_id,
                "coarse_group_size": len(members),
                "group_min_event_id": min(members),
                "group_max_event_id": max(members),
            })

    edge_witnesses: Dict[Tuple[int, int], List[Tuple[int, int, Set[str]]]] = defaultdict(list)
    internalized_edges = 0
    for parent, child, reasons in fine_edges:
        coarse_parent = event_to_coarse[parent]
        coarse_child = event_to_coarse[child]
        if coarse_parent == coarse_child:
            internalized_edges += 1
        else:
            edge_witnesses[(coarse_parent, coarse_child)].append((parent, child, reasons))
    quotient_edges = set(edge_witnesses)
    edge_rows: List[Dict[str, Any]] = []
    for (parent, child), witnesses in sorted(edge_witnesses.items()):
        conflict_types: Set[str] = set()
        resources: Set[str] = set()
        for _, _, reasons in witnesses:
            for reason in reasons:
                conflict_type, resource = reason.split(":", 1)
                conflict_types.add(conflict_type)
                resources.add(resource)
        first = min((fine_parent, fine_child) for fine_parent, fine_child, _ in witnesses)
        edge_rows.append({
            **prefix,
            "scale_window": window,
            "parent_coarse_event_id": parent,
            "child_coarse_event_id": child,
            "fine_edge_witness_count": len(witnesses),
            "first_parent_event_id": first[0],
            "first_child_event_id": first[1],
            "conflict_types": ";".join(sorted(conflict_types)),
            "witness_resources": ";".join(sorted(resources)),
        })

    coarse = analyze_edges(len(groups), quotient_edges)
    event_coverage_errors = n_events - len(event_to_coarse)
    duplicate_membership_errors = len(membership_rows) - len({int(row["event_id"]) for row in membership_rows})
    quotient_witness_errors = sum(not witnesses for witnesses in edge_witnesses.values())
    self_edges = sum(parent == child for parent, child in quotient_edges)
    fine_edge_set = {(parent, child) for parent, child, _ in fine_edges}
    identity_membership = int(window != 1 or all(len(members) == 1 for members in groups))
    identity_edges = int(window != 1 or quotient_edges == fine_edge_set)
    summary = {
        **prefix,
        "scale_window": window,
        "fine_events": n_events,
        "fine_edges": len(fine_edges),
        "coarse_nodes": len(groups),
        "coarse_edges": len(quotient_edges),
        "internalized_fine_edges": internalized_edges,
        "node_retention": len(groups) / n_events if n_events else 0.0,
        "edge_retention": len(quotient_edges) / len(fine_edges) if fine_edges else 0.0,
        "causal_depth": coarse["causal_depth"],
        "max_layer_width": coarse["max_layer_width"],
        "comparable_pair_fraction": coarse["comparable_pair_fraction"],
        "dependency_density": coarse["dependency_density"],
    }
    audit = {
        **prefix,
        "scale_window": window,
        "membership_rows": len(membership_rows),
        "unique_fine_events": len({int(row["event_id"]) for row in membership_rows}),
        "coarse_nodes": len(groups),
        "event_coverage_errors": event_coverage_errors,
        "duplicate_membership_errors": duplicate_membership_errors,
        "depth_bin_errors": depth_bin_errors,
        "quotient_edges": len(quotient_edges),
        "quotient_witness_errors": quotient_witness_errors,
        "self_edges": self_edges,
        "quotient_invalid_edges": coarse["invalid_edges"],
        "quotient_acyclic": coarse["acyclic"],
        "identity_membership_pass": identity_membership,
        "identity_edge_pass": identity_edges,
        "map_integrity_pass": int(
            event_coverage_errors == 0
            and duplicate_membership_errors == 0
            and depth_bin_errors == 0
            and quotient_witness_errors == 0
            and self_edges == 0
            and coarse["invalid_edges"] == 0
            and coarse["acyclic"] == 1
            and identity_membership == 1
            and identity_edges == 1
        ),
    }
    return membership_rows, edge_rows, summary, audit


def transition_rows(scale_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    lookup = {int(row["scale_window"]): row for row in scale_rows}
    rows: List[Dict[str, Any]] = []
    metric_sources = {
        "causal_depth_retention": "causal_depth",
        "antichain_width_retention": "max_layer_width",
        "dependency_density_retention": "dependency_density",
    }
    prefix = {key: scale_rows[0][key] for key in ("growth_seed", "run_offset", "arm", "run_seed")}
    for source_window, target_window in TRANSITIONS:
        for metric, source_field in metric_sources.items():
            source_value = float(lookup[source_window][source_field])
            target_value = float(lookup[target_window][source_field])
            rows.append({
                **prefix,
                "source_window": source_window,
                "target_window": target_window,
                "transition": f"{source_window}_to_{target_window}",
                "metric": metric,
                "source_value": source_value,
                "target_value": target_value,
                "retention_ratio": ratio(target_value, source_value),
            })
    return rows


def dag_from_rows(event_count: int, edge_rows: Sequence[Mapping[str, str]]) -> v16b.DependencyDAG:
    dag = v16b.DependencyDAG()
    dag.predecessors = [{} for _ in range(event_count)]
    for row in edge_rows:
        parent = int(row["parent_event_id"])
        child = int(row["child_event_id"])
        dag.predecessors[child][parent] = {"CALIBRATION:dependency"}
    return dag


def design_audit() -> None:
    events = read_csv(SOURCE_EVENTS)
    edges = read_csv(SOURCE_EDGES)
    key_fields = ("growth_seed", "run_offset", "arm", "run_seed")
    event_groups: Dict[Tuple[str, ...], List[Dict[str, str]]] = defaultdict(list)
    edge_groups: Dict[Tuple[str, ...], List[Dict[str, str]]] = defaultdict(list)
    for row in events:
        event_groups[tuple(row[field] for field in key_fields)].append(row)
    for row in edges:
        edge_groups[tuple(row[field] for field in key_fields)].append(row)
    calibration_rows: List[Dict[str, Any]] = []
    for key, event_group in sorted(event_groups.items()):
        prefix = dict(zip(key_fields, key))
        dag = dag_from_rows(len(event_group), edge_groups[key])
        scale_rows: List[Dict[str, Any]] = []
        audit_rows: List[Dict[str, Any]] = []
        for window in SCALE_WINDOWS:
            _, _, summary, audit = coarse_grain(dag, window, prefix)
            scale_rows.append(summary)
            audit_rows.append(audit)
        transitions = transition_rows(scale_rows)
        calibration_rows.extend({
            "artifact_role": "design_calibration_from_v16b_not_fresh_evidence",
            **row,
            "all_map_integrity_pass": int(all(int(audit["map_integrity_pass"]) for audit in audit_rows)),
        } for row in scale_rows)
        calibration_rows.extend({
            "artifact_role": "design_calibration_transition_from_v16b_not_fresh_evidence",
            **row,
            "scale_window": "",
            "all_map_integrity_pass": int(all(int(audit["map_integrity_pass"]) for audit in audit_rows)),
        } for row in transitions)
    write_csv(DESIGN_CALIBRATION, calibration_rows)
    scale16 = [row for row in calibration_rows if str(row.get("scale_window")) == "16"]
    transition_values = [float(row["retention_ratio"]) for row in calibration_rows if row.get("metric")]
    print(
        "[v16c] design calibration "
        f"runs={len(event_groups)} rows={len(calibration_rows)} "
        f"scale16_nodes={min(int(row['coarse_nodes']) for row in scale16)}-"
        f"{max(int(row['coarse_nodes']) for row in scale16)} "
        f"transition_retention={min(transition_values):.6f}-{max(transition_values):.6f}"
    )


def source_contract_rows() -> Tuple[List[Dict[str, Any]], bool, float]:
    gate_rows = read_csv(SOURCE_GATE)
    target_rows = read_csv(SOURCE_TARGET)
    overall = [row for row in gate_rows if row["gate"] == "v16b_overall"]
    if not DESIGN_CALIBRATION.exists():
        raise ValueError("missing v16c design calibration; run --design-audit first")
    local_rate = v16ac.FROZEN_LOCAL_RATE
    rows = [
        {
            "check": "v16b_overall",
            "observed": overall[0]["status"] if len(overall) == 1 else f"rows={len(overall)}",
            "required": "pass_to_v16c_coarse_graining_pilot",
            "status": "pass" if len(overall) == 1 and overall[0]["status"] == "pass_to_v16c_coarse_graining_pilot" else "fail",
        },
        {
            "check": "v16b_target_hygiene",
            "observed": target_rows[0]["separated_from_prev"] if len(target_rows) == 1 else f"rows={len(target_rows)}",
            "required": 1,
            "status": "pass" if len(target_rows) == 1 and int(target_rows[0]["separated_from_prev"]) == 1 else "fail",
        },
        {
            "check": "design_calibration_present",
            "observed": file_sha256(DESIGN_CALIBRATION),
            "required": "nonempty calibration artifact from v16b",
            "status": "pass" if DESIGN_CALIBRATION.stat().st_size > 0 else "fail",
        },
        {
            "check": "local_adapter_rate_frozen",
            "observed": local_rate,
            "required": v16ac.FROZEN_LOCAL_RATE,
            "status": "pass",
        },
    ]
    return rows, all(row["status"] == "pass" for row in rows), local_rate


def frozen_spec(local_rate: float) -> Dict[str, Any]:
    return {
        "purpose_ref": PURPOSE_REF,
        "source_gate_sha256": file_sha256(SOURCE_GATE),
        "source_target_sha256": file_sha256(SOURCE_TARGET),
        "design_calibration_sha256": file_sha256(DESIGN_CALIBRATION),
        "target_nodes": TARGET_NODES,
        "growth_seeds": list(GROWTH_SEEDS),
        "run_offsets": list(RUN_OFFSETS),
        "arms": list(ARMS),
        "steps": STEPS,
        "topological_replays": TOPOLOGICAL_REPLAYS,
        "local_rate": local_rate,
        "coarse_map": {
            "scale_windows": list(SCALE_WINDOWS),
            "depth_bin": "floor(fine_causal_depth / scale_window)",
            "contraction": "weak_components_of_direct_fine_edges_inside_each_depth_bin",
            "quotient_edge": "at_least_one_direct_fine_edge_between_components",
            "uses_graph_node_labels": False,
            "uses_scheduler_order_beyond_dependency_dag": False,
        },
        "primary_metrics": list(PRIMARY_METRICS),
        "transitions": [list(pair) for pair in TRANSITIONS],
        "thresholds": {
            "max_local_transition_cv": MAX_LOCAL_TRANSITION_CV,
            "growth_median_ratio_range": list(GROWTH_MEDIAN_RATIO_RANGE),
            "scheduler_median_ratio_range": list(SCHEDULER_MEDIAN_RATIO_RANGE),
            "max_nonseed_event_tv": MAX_NONSEED_EVENT_TV,
            "min_reordered_position_fraction": MIN_REORDERED_POSITION_FRACTION,
            "min_scale16_coarse_nodes": MIN_SCALE16_COARSE_NODES,
            "min_scale16_node_retention": MIN_SCALE16_NODE_RETENTION,
            "max_scale16_node_retention": MAX_SCALE16_NODE_RETENTION,
        },
    }


def spec_digest(spec: Mapping[str, Any]) -> str:
    payload = json.dumps(spec, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def run_seed(growth_seed: int, run_offset: int, arm: str) -> int:
    arm_code = {"current_global": 0, "exposure_matched_local": 1}[arm]
    return TARGET_NODES * 1_000_000 + growth_seed * 10_000 + run_offset + arm_code * 100_000_000 + 16_003


def preregistration_rows(local_rate: float) -> List[Dict[str, Any]]:
    digest = spec_digest(frozen_spec(local_rate))
    rows: List[Dict[str, Any]] = []
    for growth_seed in GROWTH_SEEDS:
        for run_offset in RUN_OFFSETS:
            for arm in ARMS:
                rows.append({
                    "purpose_ref": PURPOSE_REF,
                    "spec_digest": digest,
                    "source_gate_sha256": file_sha256(SOURCE_GATE),
                    "design_calibration_sha256": file_sha256(DESIGN_CALIBRATION),
                    "target_nodes": TARGET_NODES,
                    "growth_seed": growth_seed,
                    "run_offset": run_offset,
                    "arm": arm,
                    "run_seed": run_seed(growth_seed, run_offset, arm),
                    "steps": STEPS,
                    "topological_replays": TOPOLOGICAL_REPLAYS,
                    "scale_windows": ";".join(map(str, SCALE_WINDOWS)),
                    "primary_metrics": ";".join(PRIMARY_METRICS),
                    "frozen_local_rate": local_rate,
                    "max_local_transition_cv": MAX_LOCAL_TRANSITION_CV,
                    "growth_ratio_low": GROWTH_MEDIAN_RATIO_RANGE[0],
                    "growth_ratio_high": GROWTH_MEDIAN_RATIO_RANGE[1],
                    "scheduler_ratio_low": SCHEDULER_MEDIAN_RATIO_RANGE[0],
                    "scheduler_ratio_high": SCHEDULER_MEDIAN_RATIO_RANGE[1],
                    "prepared_before_fresh_dynamics": 1,
                })
    return rows


def prepare() -> None:
    source_rows, source_pass, local_rate = source_contract_rows()
    if not source_pass:
        raise RuntimeError(f"v16b source contract failed: {source_rows}")
    rows = preregistration_rows(local_rate)
    write_csv(PREREG, rows)
    print(f"[v16c] prepared rows={len(rows)} digest={rows[0]['spec_digest']}")


def load_and_verify_preregistration() -> Tuple[List[Dict[str, str]], float, List[Dict[str, Any]]]:
    if not PREREG.exists():
        raise ValueError("missing v16c preregistration; run --prepare-only first")
    source_rows, source_pass, local_rate = source_contract_rows()
    if not source_pass:
        raise RuntimeError("v16b source contract no longer passes")
    observed = read_csv(PREREG)
    expected = preregistration_rows(local_rate)
    expected_digest = spec_digest(frozen_spec(local_rate))
    if len(observed) != len(expected):
        raise ValueError("v16c preregistration row count changed")
    if {row["spec_digest"] for row in observed} != {expected_digest}:
        raise ValueError("v16c preregistration digest changed")
    fields = ("growth_seed", "run_offset", "arm", "run_seed")
    observed_keys = {tuple(row[field] for field in fields) for row in observed}
    expected_keys = {tuple(str(row[field]) for field in fields) for row in expected}
    if observed_keys != expected_keys:
        raise ValueError("v16c preregistration assignments changed")
    return observed, local_rate, source_rows


def replay_audit(
    initial_state: v7.State,
    final_state: v7.State,
    trace: Sequence[v16b.TraceEvent],
    dag: v16b.DependencyDAG,
    params: v7.Params,
    prefix: Mapping[str, Any],
    run_seed_value: int,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    original = list(range(len(trace)))
    for replay_index in range(TOPOLOGICAL_REPLAYS):
        replay_seed = run_seed_value + 73_000_037 + replay_index * 104_729
        order = v16b.random_topological_order(dag, random.Random(replay_seed))
        positions = {event_id: position for position, event_id in enumerate(order)}
        valid = all(positions[parent] < positions[child] for child, preds in enumerate(dag.predecessors) for parent in preds)
        state = initial_state.clone()
        context_failures = 0
        for event_id in order:
            item = trace[event_id]
            context = v16a.apply_event(state, item.event, params)
            context_failures += int(str(context.get("event", "")) != item.event_type)
        changed = sum(left != right for left, right in zip(order, original))
        rows.append({
            **prefix,
            "replay_index": replay_index,
            "replay_seed": replay_seed,
            "topological_order_valid": int(valid),
            "changed_positions": changed,
            "changed_position_fraction": changed / len(order) if order else 0.0,
            "context_failures": context_failures,
            "final_structure_equal": int(v7.states_equal(state, final_state)),
        })
    return rows


def run_assignment(
    base: v7.State,
    assignment: Mapping[str, str],
    params: v7.Params,
    adapter: v16ac.LocalSeedClockAdapter,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any], List[Dict[str, Any]], Dict[str, Any], v16b.DependencyDAG]:
    initial_state = base.clone()
    state = base.clone()
    rng = random.Random(int(assignment["run_seed"]))
    next_node_id, next_token_id = v08b.next_ids_from_state(state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)
    dag = v16b.DependencyDAG()
    trace: List[v16b.TraceEvent] = []
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
        family, total_rate = v16b.choose_family(rates, rng)
        if total_rate <= 0.0:
            raise RuntimeError("non-positive total rate")
        dt = rng.expovariate(total_rate)
        total_time += dt
        state.t += dt
        kernel = adapter.family_kernel(state, family, params)
        if not kernel:
            raise RuntimeError(f"empty kernel for positive family {family}")
        descriptor = tuple(v7.sample_from_dist(kernel, rng))
        concrete = v16b.materialize_event(family, descriptor, manager)
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
        trace.append(v16b.TraceEvent(step - 1, family, event_type, concrete, tuple(sorted(reads)), tuple(sorted(writes)), dt, total_time))

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
            "direct_predecessors": ";".join(str(parent) for parent in sorted(predecessors)),
            "indegree": len(predecessors),
            "causal_depth": analysis["depths"][item.event_id],
        })
    dependency_rows = v16b.edge_rows(prefix, dag)
    replay_rows = replay_audit(initial_state, final_state, trace, dag, params, prefix, int(assignment["run_seed"]))
    relabel_row = v16b.relabel_replay(initial_state, final_state, trace, dag, params, prefix)
    relabel_row["coarse_map_transport_pass"] = int(
        int(relabel_row["edge_set_equal"]) == 1 and int(relabel_row["depth_sequence_equal"]) == 1
    )
    run_row: Dict[str, Any] = {
        **prefix,
        "steps": STEPS,
        "initial_nodes": initial_state.g.num_nodes(),
        "final_nodes": final_state.g.num_nodes(),
        "initial_tokens": initial_state.token_count(),
        "final_tokens": final_state.token_count(),
        "total_time": total_time,
        "invalid_events": invalid_events,
        "n_events": analysis["n_events"],
        "fine_edges": analysis["edge_count"],
        "fine_causal_depth": analysis["causal_depth"],
        "fine_max_layer_width": analysis["max_layer_width"],
        "fine_comparable_pair_fraction": analysis["comparable_pair_fraction"],
        "fine_acyclic": analysis["acyclic"],
        "fine_edge_witness_errors": analysis["edge_witness_errors"],
        "topological_replay_failures": sum(
            not (int(row["topological_order_valid"]) and int(row["context_failures"]) == 0 and int(row["final_structure_equal"]))
            for row in replay_rows
        ),
        "min_reordered_position_fraction": min(float(row["changed_position_fraction"]) for row in replay_rows),
        "relabel_pass": relabel_row["relabel_pass"],
        "coarse_map_transport_pass": relabel_row["coarse_map_transport_pass"],
    }
    for event_type in EVENT_TYPES:
        run_row[f"{event_type}_events"] = event_counts[event_type]
    return event_rows, dependency_rows, run_row, replay_rows, relabel_row, dag


def local_stability_rows(transition_data: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    local = [row for row in transition_data if row["arm"] == "exposure_matched_local"]
    for source, target in TRANSITIONS:
        transition = f"{source}_to_{target}"
        for metric in PRIMARY_METRICS:
            values = [float(row["retention_ratio"]) for row in local if row["transition"] == transition and row["metric"] == metric]
            cv = coefficient_of_variation(values)
            rows.append({
                "transition": transition,
                "metric": metric,
                "n_runs": len(values),
                "mean_retention": mean(values),
                "median_retention": median(values),
                "retention_cv": cv,
                "max_cv": MAX_LOCAL_TRANSITION_CV,
                "local_stability_pass": int(cv <= MAX_LOCAL_TRANSITION_CV),
            })
    return rows


def growth_transfer_rows(transition_data: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    local = [row for row in transition_data if row["arm"] == "exposure_matched_local"]
    for source, target in TRANSITIONS:
        transition = f"{source}_to_{target}"
        for metric in PRIMARY_METRICS:
            medians = {
                seed: median(
                    float(row["retention_ratio"])
                    for row in local
                    if row["transition"] == transition and row["metric"] == metric and int(row["growth_seed"]) == seed
                )
                for seed in GROWTH_SEEDS
            }
            value_ratio = ratio(medians[GROWTH_SEEDS[1]], medians[GROWTH_SEEDS[0]])
            rows.append({
                "transition": transition,
                "metric": metric,
                f"growth_{GROWTH_SEEDS[0]}_median": medians[GROWTH_SEEDS[0]],
                f"growth_{GROWTH_SEEDS[1]}_median": medians[GROWTH_SEEDS[1]],
                "second_over_first_ratio": value_ratio,
                "ratio_low": GROWTH_MEDIAN_RATIO_RANGE[0],
                "ratio_high": GROWTH_MEDIAN_RATIO_RANGE[1],
                "growth_transfer_pass": int(GROWTH_MEDIAN_RATIO_RANGE[0] <= value_ratio <= GROWTH_MEDIAN_RATIO_RANGE[1]),
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


def scheduler_transfer_rows(
    transition_data: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    tv = nonseed_event_tv(run_rows)
    for source, target in TRANSITIONS:
        transition = f"{source}_to_{target}"
        for metric in PRIMARY_METRICS:
            arm_medians = {
                arm: median(
                    float(row["retention_ratio"])
                    for row in transition_data
                    if row["transition"] == transition and row["metric"] == metric and row["arm"] == arm
                )
                for arm in ARMS
            }
            value_ratio = ratio(arm_medians["exposure_matched_local"], arm_medians["current_global"])
            rows.append({
                "transition": transition,
                "metric": metric,
                "current_global_median": arm_medians["current_global"],
                "local_median": arm_medians["exposure_matched_local"],
                "local_over_global_ratio": value_ratio,
                "ratio_low": SCHEDULER_MEDIAN_RATIO_RANGE[0],
                "ratio_high": SCHEDULER_MEDIAN_RATIO_RANGE[1],
                "scheduler_transfer_pass": int(SCHEDULER_MEDIAN_RATIO_RANGE[0] <= value_ratio <= SCHEDULER_MEDIAN_RATIO_RANGE[1]),
                "nonseed_event_tv": tv,
                "nonseed_tv_pass": int(tv <= MAX_NONSEED_EVENT_TV),
            })
    return rows


def gate_evaluation(
    source_pass: bool,
    target_rows: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    replay_rows: Sequence[Mapping[str, Any]],
    relabel_rows: Sequence[Mapping[str, Any]],
    scale_rows: Sequence[Mapping[str, Any]],
    map_rows: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], str]:
    expected_runs = len(GROWTH_SEEDS) * len(RUN_OFFSETS) * len(ARMS)
    target_pass = len(target_rows) == 1 and int(target_rows[0]["separated_from_prev"]) == 1
    run_integrity = len(run_rows) == expected_runs and all(int(row["n_events"]) == STEPS and int(row["invalid_events"]) == 0 for row in run_rows)
    fine_dag_integrity = all(int(row["fine_acyclic"]) and int(row["fine_edge_witness_errors"]) == 0 and int(row["fine_edges"]) > 0 for row in run_rows)
    replay_pass = (
        len(replay_rows) == expected_runs * TOPOLOGICAL_REPLAYS
        and all(int(row["topological_order_valid"]) and int(row["context_failures"]) == 0 and int(row["final_structure_equal"]) for row in replay_rows)
        and all(float(row["changed_position_fraction"]) >= MIN_REORDERED_POSITION_FRACTION for row in replay_rows)
    )
    relabel_pass = len(relabel_rows) == expected_runs and all(int(row["relabel_pass"]) and int(row["coarse_map_transport_pass"]) for row in relabel_rows)
    map_integrity = len(map_rows) == expected_runs * len(SCALE_WINDOWS) and all(int(row["map_integrity_pass"]) for row in map_rows)
    identity_pass = all(
        int(row["identity_membership_pass"]) and int(row["identity_edge_pass"])
        for row in map_rows if int(row["scale_window"]) == 1
    )
    by_run: Dict[Tuple[int, int, str], Dict[int, Mapping[str, Any]]] = defaultdict(dict)
    for row in scale_rows:
        by_run[(int(row["growth_seed"]), int(row["run_offset"]), str(row["arm"]))][int(row["scale_window"])] = row
    strict_compression = len(by_run) == expected_runs and all(
        int(scales[1]["coarse_nodes"]) > int(scales[4]["coarse_nodes"]) > int(scales[16]["coarse_nodes"])
        for scales in by_run.values()
    )
    scale16_rows = [row for row in scale_rows if int(row["scale_window"]) == 16]
    nondegenerate = len(scale16_rows) == expected_runs and all(
        int(row["coarse_nodes"]) >= MIN_SCALE16_COARSE_NODES
        and MIN_SCALE16_NODE_RETENTION <= float(row["node_retention"]) <= MAX_SCALE16_NODE_RETENTION
        for row in scale16_rows
    )
    local_stability = all(int(row["local_stability_pass"]) for row in local_rows)
    growth_transfer = all(int(row["growth_transfer_pass"]) for row in growth_rows)
    scheduler_transfer = all(int(row["scheduler_transfer_pass"]) and int(row["nonseed_tv_pass"]) for row in scheduler_rows)
    exact_map_pass = all((source_pass, target_pass, run_integrity, fine_dag_integrity, replay_pass, relabel_pass, map_integrity, identity_pass, strict_compression, nondegenerate))
    all_pass = exact_map_pass and local_stability and growth_transfer and scheduler_transfer
    if all_pass:
        overall = "pass_to_v16d_scale_holdout"
    elif exact_map_pass:
        overall = "coarse_map_valid_but_transfer_not_yet"
    else:
        overall = "coarse_map_instrumentation_failed"
    gates = [
        {"gate": "v16b_source_contract", "status": "pass" if source_pass else "fail", "observed": int(source_pass), "required": 1, "decision": "continue"},
        {"gate": "target_hygiene", "status": "pass" if target_pass else "fail", "observed": target_rows[0]["separated_from_prev"] if len(target_rows) == 1 else len(target_rows), "required": 1, "decision": "continue"},
        {"gate": "fresh_run_integrity", "status": "pass" if run_integrity else "fail", "observed": f"runs={len(run_rows)};invalid={sum(int(row['invalid_events']) for row in run_rows)}", "required": f"runs={expected_runs};invalid=0", "decision": "continue"},
        {"gate": "fine_dag_integrity", "status": "pass" if fine_dag_integrity else "fail", "observed": f"acyclic={sum(int(row['fine_acyclic']) for row in run_rows)};witness_errors={sum(int(row['fine_edge_witness_errors']) for row in run_rows)}", "required": f"acyclic={expected_runs};witness_errors=0", "decision": "continue"},
        {"gate": "fresh_topological_replay", "status": "pass" if replay_pass else "fail", "observed": f"replays={len(replay_rows)};min_reorder={min(float(row['changed_position_fraction']) for row in replay_rows):.6f};failures={sum(not int(row['final_structure_equal']) or int(row['context_failures']) for row in replay_rows)}", "required": f"replays={expected_runs * TOPOLOGICAL_REPLAYS};failures=0", "decision": "continue" if replay_pass else "repair_support"},
        {"gate": "relabel_and_map_transport", "status": "pass" if relabel_pass else "fail", "observed": sum(int(row["relabel_pass"]) and int(row["coarse_map_transport_pass"]) for row in relabel_rows), "required": expected_runs, "decision": "continue" if relabel_pass else "repair_map"},
        {"gate": "quotient_map_integrity", "status": "pass" if map_integrity else "fail", "observed": f"passes={sum(int(row['map_integrity_pass']) for row in map_rows)}/{len(map_rows)}", "required": expected_runs * len(SCALE_WINDOWS), "decision": "continue" if map_integrity else "repair_map"},
        {"gate": "scale1_identity", "status": "pass" if identity_pass else "fail", "observed": int(identity_pass), "required": 1, "decision": "continue" if identity_pass else "repair_map"},
        {"gate": "strict_three_scale_compression", "status": "pass" if strict_compression else "fail", "observed": int(strict_compression), "required": 1, "decision": "continue" if strict_compression else "revise_scale_windows"},
        {"gate": "scale16_nondegenerate", "status": "pass" if nondegenerate else "fail", "observed": f"nodes={min(int(row['coarse_nodes']) for row in scale16_rows)}-{max(int(row['coarse_nodes']) for row in scale16_rows)};retention={min(float(row['node_retention']) for row in scale16_rows):.6f}-{max(float(row['node_retention']) for row in scale16_rows):.6f}", "required": f"nodes>={MIN_SCALE16_COARSE_NODES};retention in [{MIN_SCALE16_NODE_RETENTION},{MAX_SCALE16_NODE_RETENTION}]", "decision": "continue" if nondegenerate else "revise_scale_windows"},
        {"gate": "local_transition_cv", "status": "pass" if local_stability else "fail", "observed": ";".join(f"{row['transition']}:{row['metric']}={float(row['retention_cv']):.6f}" for row in local_rows), "required": f"each<={MAX_LOCAL_TRANSITION_CV}", "decision": "continue" if local_stability else "hold_scale_claim"},
        {"gate": "growth_seed_transfer", "status": "pass" if growth_transfer else "fail", "observed": ";".join(f"{row['transition']}:{row['metric']}={float(row['second_over_first_ratio']):.6f}" for row in growth_rows), "required": f"each in [{GROWTH_MEDIAN_RATIO_RANGE[0]},{GROWTH_MEDIAN_RATIO_RANGE[1]}]", "decision": "continue" if growth_transfer else "hold_scale_claim"},
        {"gate": "scheduler_transfer", "status": "pass" if scheduler_transfer else "fail", "observed": ";".join(f"{row['transition']}:{row['metric']}={float(row['local_over_global_ratio']):.6f}" for row in scheduler_rows) + f";tv={float(scheduler_rows[0]['nonseed_event_tv']):.6f}", "required": f"ratios in [{SCHEDULER_MEDIAN_RATIO_RANGE[0]},{SCHEDULER_MEDIAN_RATIO_RANGE[1]}];tv<={MAX_NONSEED_EVENT_TV}", "decision": "continue" if scheduler_transfer else "hold_scale_claim"},
        {"gate": "v16c_overall", "status": overall, "observed": int(all_pass), "required": 1, "decision": "design_fresh_scale_holdout" if all_pass else ("retain_map_without_transfer_claim" if exact_map_pass else "repair_instrumentation")},
    ]
    return gates, overall


def claim_rows(status: str) -> List[Dict[str, Any]]:
    exact = status in {"pass_to_v16d_scale_holdout", "coarse_map_valid_but_transfer_not_yet"}
    transfer = status == "pass_to_v16d_scale_holdout"
    return [
        {"claim_id": "C1", "statement": "The frozen depth-window map produces witnessed acyclic quotient DAGs at all three scales.", "status": "supported" if exact else "not_supported", "evidence": "v16c_map_audit.csv;v16c_coarse_dependency_edges.csv", "scope_limit": "fresh finite event histories under the declared v16a support schema"},
        {"claim_id": "C2", "statement": "The scale-1 map is the exact fine DAG and the 1/4/16 sequence compresses strictly without collapse.", "status": "supported" if exact else "not_supported", "evidence": "v16c_scale_summary.csv;v16c_gate_evaluation.csv", "scope_limit": "three selected depth windows at target 1024"},
        {"claim_id": "C3", "statement": "Primary transition ratios are stable enough across fresh bases and scheduler arms for a separate scale holdout.", "status": "supported" if transfer else "not_supported", "evidence": "v16c_local_stability.csv;v16c_growth_transfer.csv;v16c_scheduler_transfer.csv", "scope_limit": "broad pilot thresholds, two growth seeds and six runs per arm"},
        {"claim_id": "C4", "statement": "The quotient map is invariant under concrete node relabeling.", "status": "supported" if exact else "not_supported", "evidence": "v16c_relabel_replay_audit.csv", "scope_limit": "follows from preserved event edge set and depth sequence"},
        {"claim_id": "C5", "statement": "The three quotients establish a continuum limit, emergent spacetime, or Lorentz symmetry.", "status": "unsupported", "evidence": "none", "scope_limit": "not tested by v16c"},
        {"claim_id": "C6", "statement": "The event DAG is a universal physical causal order.", "status": "unsupported", "evidence": "none", "scope_limit": "implementation-level conflict order under a declared event vocabulary"},
    ]


def build_report(
    source_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    scale_rows: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# UniverseSimulation v16c: preregistered three-scale coarse-graining pilot",
        "",
        "## Research question",
        "",
        "Can one frozen, node-label-free map turn fresh event-DAG histories into nondegenerate witnessed quotient DAGs at three scales, and do the resulting transition ratios transfer across fresh bases and the local/global scheduler contrast?",
        "",
        "## Evidential separation",
        "",
        "- Architecture definition: causal-depth windows and within-window direct-edge connected components define the quotient map.",
        "- Design calibration: v16b histories were used only to reject degenerate scale choices before preregistration; they are not v16c holdout evidence.",
        "- Generated artifacts: memberships, quotient edges, and ratio summaries are deterministic functions of each fresh event DAG.",
        "- Actual dynamics: twelve new histories were generated only after the calibration artifact and preregistration were written.",
        "- Negative boundary: continuum, Lorentz, spacetime, particle, entanglement, and universal-causality claims were not tested.",
        "",
        "## Frozen source contract",
        "",
    ]
    lines.extend(table(source_rows, ("check", "observed", "required", "status")))
    lines.extend([
        "",
        "## Frozen map",
        "",
        "For each scale window `w in {1,4,16}`, each event receives `floor(causal_depth / w)`. Direct dependency edges whose endpoints are in the same bin are treated as undirected for component contraction. Every remaining quotient edge stores one or more concrete fine-edge witnesses. The map does not inspect graph node labels or original scheduler positions beyond the dependency DAG.",
        "",
        f"Fresh target `{TARGET_NODES}`, growth seeds `{GROWTH_SEEDS[0]}/{GROWTH_SEEDS[1]}`, run offsets `{RUN_OFFSETS[0]}/{RUN_OFFSETS[1]}/{RUN_OFFSETS[2]}`, `{STEPS}` events, and scheduler arms `current_global` / frozen `exposure_matched_local`.",
        "",
        "Target hygiene:",
        "",
    ])
    lines.extend(table(target_rows, ("target_nodes", "growth_replicates", "mean_initial_nodes", "mean_initial_tokens", "mean_initial_beta1", "separated_from_prev")))
    lines.extend(["", "## Fine histories", ""])
    lines.extend(table(run_rows, ("growth_seed", "run_offset", "arm", "n_events", "fine_edges", "fine_causal_depth", "fine_max_layer_width", "topological_replay_failures", "relabel_pass", "coarse_map_transport_pass")))
    lines.extend(["", "## Three-scale quotients", ""])
    lines.extend(table(scale_rows, ("growth_seed", "run_offset", "arm", "scale_window", "coarse_nodes", "coarse_edges", "node_retention", "causal_depth", "max_layer_width", "comparable_pair_fraction", "dependency_density")))
    lines.extend(["", "## Local transition stability", ""])
    lines.extend(table(local_rows, ("transition", "metric", "mean_retention", "median_retention", "retention_cv", "local_stability_pass")))
    lines.extend(["", "## Fresh-base transfer", ""])
    lines.extend(table(growth_rows, ("transition", "metric", f"growth_{GROWTH_SEEDS[0]}_median", f"growth_{GROWTH_SEEDS[1]}_median", "second_over_first_ratio", "growth_transfer_pass")))
    lines.extend(["", "## Scheduler transfer", ""])
    lines.extend(table(scheduler_rows, ("transition", "metric", "current_global_median", "local_median", "local_over_global_ratio", "scheduler_transfer_pass", "nonseed_event_tv", "nonseed_tv_pass")))
    lines.extend(["", "## Gate evaluation", ""])
    lines.extend(table(gate_rows, ("gate", "status", "observed", "required", "decision")))
    lines.extend(["", f"Overall status: `{overall}`.", "", "## Interpretation", ""])
    if overall == "pass_to_v16d_scale_holdout":
        lines.append("The frozen map is exact at scale 1, yields strictly smaller witnessed DAGs at scales 4 and 16, and its three preregistered transition ratios remain inside broad pilot bounds across fresh bases and scheduler arms. This supports one independent scale holdout, not a continuum or spacetime claim.")
    elif overall == "coarse_map_valid_but_transfer_not_yet":
        lines.append("The quotient construction is technically valid, but at least one transition ratio is not stable across bases or schedulers. Retain the map as instrumentation; do not promote a scale-family claim or tune thresholds on these runs.")
    else:
        lines.append("At least one exact structural, replay, relabel, identity, compression, or non-collapse condition failed. Treat this as an instrumentation failure and repair only the smallest map defect before new dynamics.")
    lines.extend([
        "",
        "Causal-depth retention is partly construction-adjacent: depth windows mechanically constrain that ratio toward the inverse window factor. Antichain-width and dependency-density retention are therefore the less direct transfer checks. Passing all three is a consistency result for this map, not three independent physical signals.",
        "",
        "## Evidential boundary",
        "",
        "A stable finite three-scale quotient would show that the event-history representation supports a repeatable hierarchy under one explicit map. It would not show an observer-independent continuum, metric geometry, Lorentz covariance, quantum entanglement, particles, or laws of our universe.",
        "",
        "## Next decision",
        "",
    ])
    if overall == "pass_to_v16d_scale_holdout":
        lines.append("Run one preregistered v16d holdout with a fresh target or event budget. Freeze the same map and ratios unchanged; use the local adapter as primary and current-global only as a diagnostic control.")
    elif overall == "coarse_map_valid_but_transfer_not_yet":
        lines.append("Stop new scale dynamics. Identify the single unstable ratio and decide whether it is a bad observable or genuine scheduler/base dependence without refitting this pilot.")
    else:
        lines.append("Do not run a scale holdout. Repair the exact map or witness accounting first and repeat the self-test/calibration sequence.")
    lines.append("")
    return "\n".join(lines)


def verify_outputs() -> None:
    assignments, _, _ = load_and_verify_preregistration()
    expected_runs = len(assignments)
    run_rows = read_csv(DOC / "v16c_run_summary.csv")
    event_rows = read_csv(DOC / "v16c_event_log.csv")
    fine_edges = read_csv(DOC / "v16c_fine_dependency_edges.csv")
    memberships = read_csv(DOC / "v16c_coarse_membership.csv")
    coarse_edges = read_csv(DOC / "v16c_coarse_dependency_edges.csv")
    scale_rows = read_csv(DOC / "v16c_scale_summary.csv")
    map_rows = read_csv(DOC / "v16c_map_audit.csv")
    replay_rows = read_csv(DOC / "v16c_topological_replay_audit.csv")
    relabel_rows = read_csv(DOC / "v16c_relabel_replay_audit.csv")
    gate_rows = read_csv(DOC / "v16c_gate_evaluation.csv")
    key_fields = ("growth_seed", "run_offset", "arm", "run_seed")

    def key(row: Mapping[str, str]) -> Tuple[str, ...]:
        return tuple(row[field] for field in key_fields)

    assignment_keys = {key(row) for row in assignments}
    assert len(run_rows) == expected_runs
    assert {key(row) for row in run_rows} == assignment_keys
    assert len(event_rows) == expected_runs * STEPS
    assert len(memberships) == expected_runs * STEPS * len(SCALE_WINDOWS)
    assert len(scale_rows) == expected_runs * len(SCALE_WINDOWS)
    assert len(map_rows) == expected_runs * len(SCALE_WINDOWS)
    assert len(replay_rows) == expected_runs * TOPOLOGICAL_REPLAYS
    assert len(relabel_rows) == expected_runs
    assert all(int(row["map_integrity_pass"]) == 1 for row in map_rows)
    assert all(int(row["relabel_pass"]) == 1 and int(row["coarse_map_transport_pass"]) == 1 for row in relabel_rows)
    assert all(
        int(row["topological_order_valid"]) == 1
        and int(row["context_failures"]) == 0
        and int(row["final_structure_equal"]) == 1
        for row in replay_rows
    )

    events_by_run: Dict[Tuple[str, ...], Set[int]] = defaultdict(set)
    fine_edge_count: Counter[Tuple[str, ...]] = Counter()
    memberships_by_run_scale: Dict[Tuple[Tuple[str, ...], int], List[Dict[str, str]]] = defaultdict(list)
    coarse_edges_by_run_scale: Dict[Tuple[Tuple[str, ...], int], List[Dict[str, str]]] = defaultdict(list)
    scale_by_run: Dict[Tuple[Tuple[str, ...], int], Dict[str, str]] = {}
    for row in event_rows:
        events_by_run[key(row)].add(int(row["event_id"]))
    for row in fine_edges:
        fine_edge_count[key(row)] += 1
    for row in memberships:
        memberships_by_run_scale[(key(row), int(row["scale_window"]))].append(row)
    for row in coarse_edges:
        assert int(row["fine_edge_witness_count"]) >= 1
        coarse_edges_by_run_scale[(key(row), int(row["scale_window"]))].append(row)
    for row in scale_rows:
        scale_by_run[(key(row), int(row["scale_window"]))] = row

    for run_key in assignment_keys:
        assert events_by_run[run_key] == set(range(STEPS))
        for window in SCALE_WINDOWS:
            member_rows = memberships_by_run_scale[(run_key, window)]
            assert {int(row["event_id"]) for row in member_rows} == set(range(STEPS))
            coarse_ids = {int(row["coarse_event_id"]) for row in member_rows}
            scale = scale_by_run[(run_key, window)]
            assert len(coarse_ids) == int(scale["coarse_nodes"])
            assert len(coarse_edges_by_run_scale[(run_key, window)]) == int(scale["coarse_edges"])
            if window == 1:
                assert all(int(row["event_id"]) == int(row["coarse_event_id"]) for row in member_rows)
                assert len(coarse_edges_by_run_scale[(run_key, window)]) == fine_edge_count[run_key]

    overall = [row for row in gate_rows if row["gate"] == "v16c_overall"]
    assert len(overall) == 1 and overall[0]["status"] in {
        "pass_to_v16d_scale_holdout",
        "coarse_map_valid_but_transfer_not_yet",
        "coarse_map_instrumentation_failed",
    }
    for path in (
        DOC / "v16c_three_scale_coarse_graining_pilot.md",
        DOC / "v0_16c_operativ_anbefaling.md",
        DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16c.md",
    ):
        assert path.exists() and path.stat().st_size > 0
    print(
        f"[v16c] output verification pass runs={expected_runs} events={len(event_rows)} "
        f"memberships={len(memberships)} coarse_edges={len(coarse_edges)} overall={overall[0]['status']}"
    )


def self_test() -> None:
    dag = v16b.DependencyDAG()
    dag.predecessors = [
        {},
        {},
        {0: {"RAW:node:0"}},
        {1: {"RAW:node:1"}},
        {2: {"RAW:node:2"}, 3: {"RAW:node:3"}},
    ]
    prefix = {"growth_seed": -1, "run_offset": -1, "arm": "self_test", "run_seed": 1}
    scale_rows: List[Dict[str, Any]] = []
    for window in SCALE_WINDOWS:
        membership, edges, summary, audit = coarse_grain(dag, window, prefix)
        assert len(membership) == 5
        assert int(audit["map_integrity_pass"]) == 1
        assert int(summary["coarse_nodes"]) >= 1
        assert all(int(row["fine_edge_witness_count"]) >= 1 for row in edges)
        scale_rows.append(summary)
    assert int(scale_rows[0]["coarse_nodes"]) == 5
    assert int(scale_rows[0]["coarse_edges"]) == 4
    rows = transition_rows(scale_rows)
    assert len(rows) == len(TRANSITIONS) * len(PRIMARY_METRICS)
    print("[v16c] self-test pass")


def run() -> None:
    assignments, local_rate, source_rows = load_and_verify_preregistration()
    adapter = v16ac.LocalSeedClockAdapter(local_rate)
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    target_rows = v10e.summarize_bases(base_rows)
    if len(target_rows) != 1 or int(target_rows[0]["separated_from_prev"]) != 1:
        raise RuntimeError("v16c target hygiene failed")
    ensemble_name = ensembles[0].name
    params = v16a.anchor_params()
    event_rows: List[Dict[str, Any]] = []
    fine_edge_rows: List[Dict[str, Any]] = []
    run_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    relabel_rows: List[Dict[str, Any]] = []
    membership_rows: List[Dict[str, Any]] = []
    coarse_edge_rows: List[Dict[str, Any]] = []
    scale_rows: List[Dict[str, Any]] = []
    map_rows: List[Dict[str, Any]] = []
    transitions: List[Dict[str, Any]] = []
    for index, assignment in enumerate(assignments, start=1):
        base = base_states[(ensemble_name, int(assignment["growth_seed"]))]
        events, fine_edges, run_row, replays, relabel, dag = run_assignment(base, assignment, params, adapter)
        prefix = {key: run_row[key] for key in ("growth_seed", "run_offset", "arm", "run_seed")}
        run_scales: List[Dict[str, Any]] = []
        for window in SCALE_WINDOWS:
            memberships, coarse_edges, summary, audit = coarse_grain(dag, window, prefix)
            membership_rows.extend(memberships)
            coarse_edge_rows.extend(coarse_edges)
            scale_rows.append(summary)
            run_scales.append(summary)
            map_rows.append(audit)
        run_transitions = transition_rows(run_scales)
        transitions.extend(run_transitions)
        event_rows.extend(events)
        fine_edge_rows.extend(fine_edges)
        run_rows.append(run_row)
        replay_rows.extend(replays)
        relabel_rows.append(relabel)
        print(
            f"[v16c] runs={index}/{len(assignments)} arm={assignment['arm']} "
            f"nodes={run_scales[0]['coarse_nodes']}/{run_scales[1]['coarse_nodes']}/{run_scales[2]['coarse_nodes']}"
        )

    local_rows = local_stability_rows(transitions)
    growth_rows = growth_transfer_rows(transitions)
    scheduler_rows = scheduler_transfer_rows(transitions, run_rows)
    gate_rows, overall = gate_evaluation(
        True, target_rows, run_rows, replay_rows, relabel_rows, scale_rows, map_rows, local_rows, growth_rows, scheduler_rows
    )
    write_csv(DOC / "v16c_source_chain.csv", source_rows)
    write_csv(DOC / "v16c_target_summary.csv", target_rows)
    write_csv(DOC / "v16c_event_log.csv", event_rows)
    write_csv(DOC / "v16c_fine_dependency_edges.csv", fine_edge_rows)
    write_csv(DOC / "v16c_run_summary.csv", run_rows)
    write_csv(DOC / "v16c_coarse_membership.csv", membership_rows)
    write_csv(DOC / "v16c_coarse_dependency_edges.csv", coarse_edge_rows)
    write_csv(DOC / "v16c_scale_summary.csv", scale_rows)
    write_csv(DOC / "v16c_transition_ratios.csv", transitions)
    write_csv(DOC / "v16c_map_audit.csv", map_rows)
    write_csv(DOC / "v16c_topological_replay_audit.csv", replay_rows)
    write_csv(DOC / "v16c_relabel_replay_audit.csv", relabel_rows)
    write_csv(DOC / "v16c_local_stability.csv", local_rows)
    write_csv(DOC / "v16c_growth_transfer.csv", growth_rows)
    write_csv(DOC / "v16c_scheduler_transfer.csv", scheduler_rows)
    write_csv(DOC / "v16c_gate_evaluation.csv", gate_rows)
    write_csv(DOC / "v16c_claim_ledger.csv", claim_rows(overall))
    report = build_report(source_rows, target_rows, run_rows, scale_rows, local_rows, growth_rows, scheduler_rows, gate_rows, overall)
    (DOC / "v16c_three_scale_coarse_graining_pilot.md").write_text(report, encoding="utf-8")
    recommendation = "\n".join([
        "# Operativ anbefaling v0.16c",
        "",
        f"Status: `{overall}`.",
        "",
        "- Behold coarse-map-resultatet avgrenset til den frosne depth-window-konstruksjonen og ferske endelige historikker.",
        "- Ved full pass: kjoer ett separat scale-holdout uten aa endre kart, ratioer eller terskler.",
        "- Ved map-pass men transfer-fail: behold instrumenteringen, men stopp skala-claim og ikke refit denne piloten.",
        "- Ved strukturell fail: reparer bare minste kart-/witness-feil foer ny dynamikk.",
        "- Ikke promoter tre endelige skalaer til continuum, spacetime, Lorentz-symmetri eller universell kausalitet.",
        "",
    ])
    (DOC / "v0_16c_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    lay = "\n".join([
        "# v0.16c for ikke-spesialister",
        "",
        "Vi tok hendelsesgrafen fra v16b og lagde tre opplosninger. Hendelser som ligger naer hverandre i kausal dybde og er koblet med en direkte avhengighet, blir samlet til ett grovere punkt. Hver grov pil maa fortsatt kunne spores til minst en konkret fin pil.",
        "",
        f"Statusen i denne runden er `{overall}`. En full pass betyr bare at dette bestemte kartet gir en repeterbar endelig skalahierarki og fortjener en ny holdout. Det er ikke et bevis for kontinuerlig romtid eller relativitet.",
        "",
    ])
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16c.md").write_text(lay, encoding="utf-8")
    print(
        f"[v16c] overall={overall} runs={len(run_rows)} events={len(event_rows)} "
        f"fine_edges={len(fine_edge_rows)} coarse_memberships={len(membership_rows)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="v16c three-scale event-DAG coarse-graining pilot")
    parser.add_argument("--design-audit", action="store_true")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    selected = sum((args.design_audit, args.prepare_only, args.self_test, args.verify_only))
    if selected > 1:
        raise ValueError("choose only one mode")
    if args.self_test:
        self_test()
    elif args.design_audit:
        design_audit()
    elif args.prepare_only:
        prepare()
    elif args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
