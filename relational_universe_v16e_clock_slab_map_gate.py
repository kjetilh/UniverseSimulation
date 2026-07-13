#!/usr/bin/env python3
"""v16e independent clock-slab coarse-map gate.

The candidate map groups events into equal intervals of normalized simulation
time. It does not use causal depth. Ordered equal-event-count slabs and shuffled
waiting-time slabs are explicit controls.

This is an architecture experiment. It does not test Lorentz symmetry,
spacetime, continuum limits, particles, entanglement, or universal causality.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
from collections import Counter
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v16a_disjoint_event_commutation_gate as v16a
import relational_universe_v16ac_local_seed_adapter_gate as v16ac
import relational_universe_v16b_intrinsic_event_dag_gate as v16b
import relational_universe_v16c_three_scale_coarse_graining_pilot as v16c
import relational_universe_v16d_target_scale_holdout as v16d


DOC = Path("Documentation")
CALIBRATION_SUMMARY = DOC / "v16e_design_calibration_map_summary.csv"
CALIBRATION_EFFECTS = DOC / "v16e_design_calibration_null_effects.csv"
DESIGN_SELECTION = DOC / "v16e_design_selection.csv"
PREREG = DOC / "v16e_pre_registration.csv"
SOURCE_SCRIPT = Path("relational_universe_v16d_target_scale_holdout.py")
SOURCE_GATE = DOC / "v16d_gate_evaluation.csv"
SOURCE_PREREG = DOC / "v16d_pre_registration.csv"
SOURCE_STAGES = {
    "v16c": (DOC / "v16c_event_log.csv", DOC / "v16c_fine_dependency_edges.csv"),
    "v16d": (DOC / "v16d_event_log.csv", DOC / "v16d_fine_dependency_edges.csv"),
}
CANDIDATE_BIN_FAMILIES = {
    "wide_128_32_8": (128, 32, 8),
    "compact_64_16_4": (64, 16, 4),
}
CALIBRATION_SHUFFLES = 16
SELECTED_BINS = (128, 64, 32)
FRESH_SHUFFLES = 32
TARGET_NODES = 1536
STEPS = 3072
EVENTS_PER_INITIAL_NODE = 2
GROWTH_SEEDS = (3701, 3803)
RUN_OFFSETS = (71003, 71047, 71089)
ARMS = ("current_global", "exposure_matched_local")
TOPOLOGICAL_REPLAYS = 2
EVENT_TYPES = v16b.EVENT_TYPES

MAX_LOCAL_MEDIAN_CLOCK_MINUS_NULL = -0.005
MAX_LOCAL_MEDIAN_CLOCK_MINUS_COUNT = -0.005
MAX_LOCAL_MEDIAN_NULL_Z = -2.0
MIN_LOCAL_NEGATIVE_RUN_FRACTION = 5.0 / 6.0
DISCOVERY_HOLDOUT_MAGNITUDE_RATIO_RANGE = (0.50, 2.00)
GROWTH_MAGNITUDE_RATIO_RANGE = (0.60, 1.67)
SCHEDULER_MAGNITUDE_RATIO_RANGE = (0.60, 1.67)
MAX_NONSEED_EVENT_TV = 0.05
MIN_REORDERED_POSITION_FRACTION = 0.10
TOLERANCE = 1.0e-12

read_csv = v16c.read_csv
write_csv = v16c.write_csv
mean = v16c.mean
median = v16c.median
coefficient_of_variation = v16c.coefficient_of_variation


def sample_sd(values: Iterable[float]) -> float:
    data = list(values)
    return statistics.stdev(data) if len(data) >= 2 else 0.0


def stable_seed(*parts: Any) -> int:
    payload = "|".join(str(part) for part in parts).encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def dag_from_edge_rows(event_count: int, rows: Sequence[Mapping[str, str]]) -> v16b.DependencyDAG:
    dag = v16b.DependencyDAG()
    dag.predecessors = [{} for _ in range(event_count)]
    for row in rows:
        parent = int(row["parent_event_id"])
        child = int(row["child_event_id"])
        reasons: Set[str] = set()
        conflict_types = [value for value in row["conflict_types"].split(";") if value]
        resources = [value for value in row["witness_resources"].split(";") if value]
        for conflict_type in conflict_types:
            for resource in resources:
                reasons.add(f"{conflict_type}:{resource}")
        dag.predecessors[child][parent] = reasons or {"CALIBRATION:dependency"}
    return dag


def normalized_clock_bins(dts: Sequence[float], bin_count: int) -> List[int]:
    total = sum(dts)
    if total <= 0.0:
        raise ValueError("clock map requires positive total time")
    assignments: List[int] = []
    elapsed = 0.0
    for dt in dts:
        midpoint = elapsed + 0.5 * dt
        assignments.append(min(bin_count - 1, int((midpoint / total) * bin_count)))
        elapsed += dt
    if any(left > right for left, right in zip(assignments, assignments[1:])):
        raise AssertionError("clock assignments must be monotone")
    return assignments


def event_count_bins(event_count: int, bin_count: int) -> List[int]:
    if event_count <= 0:
        return []
    return [min(bin_count - 1, event_id * bin_count // event_count) for event_id in range(event_count)]


def shuffled_clock_bins(dts: Sequence[float], bin_count: int, seed: int) -> List[int]:
    shuffled = list(dts)
    random.Random(seed).shuffle(shuffled)
    return normalized_clock_bins(shuffled, bin_count)


def quotient_summary(
    dag: v16b.DependencyDAG,
    assignments: Sequence[int],
    prefix: Mapping[str, Any],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    n_events = len(dag.predecessors)
    if len(assignments) != n_events:
        raise ValueError("assignment length does not match event DAG")
    if any(left > right for left, right in zip(assignments, assignments[1:])):
        raise ValueError("slab assignments are not monotone")
    occupied_bins = sorted(set(assignments))
    requested_bins = int(prefix["requested_bins"])
    coarse_for_bin = {bin_id: coarse_id for coarse_id, bin_id in enumerate(occupied_bins)}
    event_to_coarse = [coarse_for_bin[bin_id] for bin_id in assignments]
    quotient_witnesses: Dict[Tuple[int, int], int] = defaultdict(int)
    internalized = 0
    fine_edges = 0
    backward_edges = 0
    for child, predecessor_map in enumerate(dag.predecessors):
        for parent in predecessor_map:
            fine_edges += 1
            coarse_parent = event_to_coarse[parent]
            coarse_child = event_to_coarse[child]
            backward_edges += int(coarse_parent > coarse_child)
            if coarse_parent == coarse_child:
                internalized += 1
            else:
                quotient_witnesses[(coarse_parent, coarse_child)] += 1
    quotient_edges = set(quotient_witnesses)
    analysis = v16c.analyze_edges(len(occupied_bins), quotient_edges)
    occupancy = [assignments.count(bin_id) for bin_id in occupied_bins]
    mean_occupancy = mean(occupancy)
    occupancy_cv = coefficient_of_variation(occupancy)
    summary = {
        **prefix,
        "fine_events": n_events,
        "fine_edges": fine_edges,
        "requested_bins": requested_bins,
        "occupied_bins": len(occupied_bins),
        "empty_bins": requested_bins - len(occupied_bins),
        "coarse_edges": len(quotient_edges),
        "internalized_fine_edges": internalized,
        "edge_retention": len(quotient_edges) / fine_edges if fine_edges else 0.0,
        "fine_edge_crossing_rate": (fine_edges - internalized) / fine_edges if fine_edges else 0.0,
        "mean_events_per_bin": mean_occupancy,
        "occupancy_cv": occupancy_cv,
        "max_bin_fraction": max(occupancy, default=0) / n_events if n_events else 0.0,
        "causal_depth": analysis["causal_depth"],
        "max_layer_width": analysis["max_layer_width"],
        "comparable_pair_fraction": analysis["comparable_pair_fraction"],
        "dependency_density": analysis["dependency_density"],
    }
    audit = {
        **prefix,
        "assignment_rows": len(assignments),
        "unique_events": n_events,
        "occupied_bins": len(occupied_bins),
        "backward_edges": backward_edges,
        "quotient_edges": len(quotient_edges),
        "quotient_witness_errors": sum(count < 1 for count in quotient_witnesses.values()),
        "quotient_invalid_edges": analysis["invalid_edges"],
        "quotient_acyclic": analysis["acyclic"],
        "map_integrity_pass": int(
            len(assignments) == n_events
            and backward_edges == 0
            and all(count >= 1 for count in quotient_witnesses.values())
            and analysis["invalid_edges"] == 0
            and analysis["acyclic"] == 1
        ),
    }
    return summary, audit


def quotient_artifact_rows(
    dag: v16b.DependencyDAG,
    assignments: Sequence[int],
    prefix: Mapping[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    occupied_bins = sorted(set(assignments))
    coarse_for_bin = {bin_id: coarse_id for coarse_id, bin_id in enumerate(occupied_bins)}
    event_to_coarse = [coarse_for_bin[bin_id] for bin_id in assignments]
    occupancy = Counter(assignments)
    membership_rows = [
        {
            **prefix,
            "event_id": event_id,
            "source_bin": assignments[event_id],
            "coarse_event_id": event_to_coarse[event_id],
            "coarse_group_size": occupancy[assignments[event_id]],
        }
        for event_id in range(len(assignments))
    ]
    witnesses: Dict[Tuple[int, int], List[Tuple[int, int, Set[str]]]] = defaultdict(list)
    for child, predecessor_map in enumerate(dag.predecessors):
        for parent, reasons in predecessor_map.items():
            coarse_parent = event_to_coarse[parent]
            coarse_child = event_to_coarse[child]
            if coarse_parent != coarse_child:
                witnesses[(coarse_parent, coarse_child)].append((parent, child, set(reasons)))
    edge_rows: List[Dict[str, Any]] = []
    for (coarse_parent, coarse_child), fine_witnesses in sorted(witnesses.items()):
        conflict_types: Set[str] = set()
        resources: Set[str] = set()
        for _, _, reasons in fine_witnesses:
            for reason in reasons:
                conflict_type, resource = reason.split(":", 1)
                conflict_types.add(conflict_type)
                resources.add(resource)
        first_parent, first_child = min((parent, child) for parent, child, _ in fine_witnesses)
        edge_rows.append({
            **prefix,
            "parent_coarse_event_id": coarse_parent,
            "child_coarse_event_id": coarse_child,
            "fine_edge_witness_count": len(fine_witnesses),
            "first_parent_event_id": first_parent,
            "first_child_event_id": first_child,
            "conflict_types": ";".join(sorted(conflict_types)),
            "witness_resources": ";".join(sorted(resources)),
        })
    return membership_rows, edge_rows


def grouped_source_rows(
    event_path: Path,
    edge_path: Path,
) -> Iterable[Tuple[Tuple[str, str, str, str], List[Dict[str, str]], List[Dict[str, str]]]]:
    key_fields = ("growth_seed", "run_offset", "arm", "run_seed")
    event_groups: Dict[Tuple[str, str, str, str], List[Dict[str, str]]] = defaultdict(list)
    edge_groups: Dict[Tuple[str, str, str, str], List[Dict[str, str]]] = defaultdict(list)
    for row in read_csv(event_path):
        event_groups[tuple(row[field] for field in key_fields)].append(row)
    for row in read_csv(edge_path):
        edge_groups[tuple(row[field] for field in key_fields)].append(row)
    for key in sorted(event_groups):
        events = sorted(event_groups[key], key=lambda row: int(row["event_id"]))
        yield key, events, edge_groups[key]


def design_audit() -> None:
    summary_rows: List[Dict[str, Any]] = []
    effect_rows: List[Dict[str, Any]] = []
    key_fields = ("growth_seed", "run_offset", "arm", "run_seed")
    for source_stage, (event_path, edge_path) in SOURCE_STAGES.items():
        for key, events, edges in grouped_source_rows(event_path, edge_path):
            prefix = {"artifact_role": "v16e_design_calibration_not_fresh_evidence", "source_stage": source_stage}
            prefix.update(dict(zip(key_fields, key)))
            dts = [float(row["dt"]) for row in events]
            dag = dag_from_edge_rows(len(events), edges)
            for family_label, bin_counts in CANDIDATE_BIN_FAMILIES.items():
                for bin_count in bin_counts:
                    common = {**prefix, "bin_family": family_label, "requested_bins": bin_count}
                    clock_summary, clock_audit = quotient_summary(
                        dag,
                        normalized_clock_bins(dts, bin_count),
                        {**common, "map_kind": "clock", "shuffle_index": -1},
                    )
                    count_summary, count_audit = quotient_summary(
                        dag,
                        event_count_bins(len(events), bin_count),
                        {**common, "map_kind": "event_count", "shuffle_index": -1},
                    )
                    summary_rows.extend([
                        {**clock_summary, **{f"audit_{field}": value for field, value in clock_audit.items() if field not in clock_summary}},
                        {**count_summary, **{f"audit_{field}": value for field, value in count_audit.items() if field not in count_summary}},
                    ])
                    shuffled_summaries: List[Dict[str, Any]] = []
                    for shuffle_index in range(CALIBRATION_SHUFFLES):
                        shuffle_seed = stable_seed(source_stage, *key, family_label, bin_count, shuffle_index, "v16e")
                        shuffled_summary, shuffled_audit = quotient_summary(
                            dag,
                            shuffled_clock_bins(dts, bin_count, shuffle_seed),
                            {
                                **common,
                                "map_kind": "shuffled_clock",
                                "shuffle_index": shuffle_index,
                                "shuffle_seed": shuffle_seed,
                            },
                        )
                        shuffled_summaries.append(shuffled_summary)
                        summary_rows.append({
                            **shuffled_summary,
                            **{f"audit_{field}": value for field, value in shuffled_audit.items() if field not in shuffled_summary},
                        })
                    null_values = [float(row["edge_retention"]) for row in shuffled_summaries]
                    null_mean = mean(null_values)
                    null_sd = sample_sd(null_values)
                    clock_value = float(clock_summary["edge_retention"])
                    z_score = (clock_value - null_mean) / null_sd if null_sd > TOLERANCE else 0.0
                    effect_rows.append({
                        **common,
                        "clock_edge_retention": clock_value,
                        "event_count_edge_retention": count_summary["edge_retention"],
                        "shuffle_mean_edge_retention": null_mean,
                        "shuffle_sd_edge_retention": null_sd,
                        "clock_minus_shuffle_mean": clock_value - null_mean,
                        "clock_null_z": z_score,
                        "clock_minus_event_count": clock_value - float(count_summary["edge_retention"]),
                        "clock_occupied_bins": clock_summary["occupied_bins"],
                        "clock_occupancy_cv": clock_summary["occupancy_cv"],
                        "all_map_integrity_pass": int(
                            int(clock_audit["map_integrity_pass"])
                            and int(count_audit["map_integrity_pass"])
                            and all(int(row.get("audit_map_integrity_pass", 0)) for row in summary_rows[-CALIBRATION_SHUFFLES:])
                        ),
                    })
    write_csv(CALIBRATION_SUMMARY, summary_rows)
    write_csv(CALIBRATION_EFFECTS, effect_rows)
    for family_label in CANDIDATE_BIN_FAMILIES:
        subset = [row for row in effect_rows if row["bin_family"] == family_label]
        print(
            f"[v16e] design family={family_label} effects={len(subset)} "
            f"map_pass={sum(int(row['all_map_integrity_pass']) for row in subset)}/{len(subset)} "
            f"median_z={median(float(row['clock_null_z']) for row in subset):.6f} "
            f"sign_positive={sum(float(row['clock_minus_shuffle_mean']) > 0.0 for row in subset)}/{len(subset)} "
            f"occupied={min(int(row['clock_occupied_bins']) for row in subset)}-"
            f"{max(int(row['clock_occupied_bins']) for row in subset)}"
        )


def expected_selection_rows() -> List[Dict[str, Any]]:
    if not CALIBRATION_EFFECTS.exists() or not CALIBRATION_SUMMARY.exists():
        raise ValueError("missing v16e calibration artifacts; run --design-audit first")
    effects = read_csv(CALIBRATION_EFFECTS)
    rows: List[Dict[str, Any]] = []
    for bin_count in SELECTED_BINS:
        subset = [row for row in effects if int(row["requested_bins"]) == bin_count]
        local = [row for row in subset if row["arm"] == "exposure_matched_local"]
        if len(subset) != 24 or len(local) != 12:
            raise ValueError(f"unexpected calibration coverage for bin {bin_count}")
        rows.append({
            "artifact_role": "v16e_frozen_design_selection_not_fresh_evidence",
            "requested_bins": bin_count,
            "selection_reason": "nonnull_clock_edge_retention_at_material_resolution",
            "expected_direction": "clock_edge_retention_lower_than_controls",
            "calibration_runs": len(subset),
            "calibration_local_runs": len(local),
            "calibration_all_map_pass": int(all(int(row["all_map_integrity_pass"]) for row in subset)),
            "calibration_local_median_clock_minus_shuffle": median(float(row["clock_minus_shuffle_mean"]) for row in local),
            "calibration_local_median_clock_minus_event_count": median(float(row["clock_minus_event_count"]) for row in local),
            "calibration_local_median_null_z": median(float(row["clock_null_z"]) for row in local),
            "calibration_local_negative_fraction": mean(float(row["clock_minus_shuffle_mean"]) < 0.0 for row in local),
            "max_local_median_clock_minus_null": MAX_LOCAL_MEDIAN_CLOCK_MINUS_NULL,
            "max_local_median_clock_minus_count": MAX_LOCAL_MEDIAN_CLOCK_MINUS_COUNT,
            "max_local_median_null_z": MAX_LOCAL_MEDIAN_NULL_Z,
            "min_local_negative_run_fraction": MIN_LOCAL_NEGATIVE_RUN_FRACTION,
            "calibration_effects_sha256": v16c.file_sha256(CALIBRATION_EFFECTS),
            "calibration_summary_sha256": v16c.file_sha256(CALIBRATION_SUMMARY),
        })
    return rows


def freeze_design() -> None:
    rows = expected_selection_rows()
    if not all(
        int(row["calibration_all_map_pass"])
        and float(row["calibration_local_median_clock_minus_shuffle"]) <= MAX_LOCAL_MEDIAN_CLOCK_MINUS_NULL
        and float(row["calibration_local_median_clock_minus_event_count"]) <= MAX_LOCAL_MEDIAN_CLOCK_MINUS_COUNT
        and float(row["calibration_local_median_null_z"]) <= MAX_LOCAL_MEDIAN_NULL_Z
        and float(row["calibration_local_negative_fraction"]) >= MIN_LOCAL_NEGATIVE_RUN_FRACTION
        for row in rows
    ):
        raise RuntimeError("selected v16e clock bins do not meet discovery criteria")
    write_csv(DESIGN_SELECTION, rows)
    print(f"[v16e] froze design bins={SELECTED_BINS} selection_sha256={v16c.file_sha256(DESIGN_SELECTION)}")


def selection_verified() -> bool:
    if not DESIGN_SELECTION.exists():
        return False
    observed = read_csv(DESIGN_SELECTION)
    expected = expected_selection_rows()
    if len(observed) != len(expected):
        return False
    observed_lookup = {int(row["requested_bins"]): row for row in observed}
    for row in expected:
        candidate = observed_lookup.get(int(row["requested_bins"]))
        if candidate is None:
            return False
        for field in (
            "artifact_role",
            "selection_reason",
            "expected_direction",
            "calibration_effects_sha256",
            "calibration_summary_sha256",
        ):
            if candidate[field] != str(row[field]):
                return False
        for field in (
            "calibration_local_median_clock_minus_shuffle",
            "calibration_local_median_clock_minus_event_count",
            "calibration_local_median_null_z",
            "calibration_local_negative_fraction",
            "max_local_median_clock_minus_null",
            "max_local_median_clock_minus_count",
            "max_local_median_null_z",
            "min_local_negative_run_fraction",
        ):
            if abs(float(candidate[field]) - float(row[field])) > TOLERANCE:
                return False
    return True


def source_contract_rows() -> Tuple[List[Dict[str, Any]], bool, float]:
    gate_rows = read_csv(SOURCE_GATE)
    overall = [row for row in gate_rows if row["gate"] == "v16d_overall"]
    subgates = [row for row in gate_rows if row["gate"] != "v16d_overall"]
    prereg_verified = True
    prereg_error = "verified"
    try:
        v16d.load_and_verify_preregistration()
    except (AssertionError, KeyError, RuntimeError, ValueError) as error:
        prereg_verified = False
        prereg_error = f"{type(error).__name__}:{error}"
    rows = [
        {
            "check": "v16d_overall",
            "observed": overall[0]["status"] if len(overall) == 1 else f"rows={len(overall)}",
            "required": "pass_to_v16e_independent_coarse_map_gate",
            "status": "pass" if len(overall) == 1 and overall[0]["status"] == "pass_to_v16e_independent_coarse_map_gate" else "fail",
        },
        {
            "check": "v16d_all_subgates",
            "observed": sum(row["status"] != "pass" for row in subgates),
            "required": 0,
            "status": "pass" if subgates and all(row["status"] == "pass" for row in subgates) else "fail",
        },
        {
            "check": "v16d_preregistration_reverified",
            "observed": prereg_error,
            "required": "verified",
            "status": "pass" if prereg_verified else "fail",
        },
        {
            "check": "v16d_source_script_sha256",
            "observed": v16c.file_sha256(SOURCE_SCRIPT),
            "required": "frozen into v16e preregistration",
            "status": "pass",
        },
        {
            "check": "clock_design_selection",
            "observed": v16c.file_sha256(DESIGN_SELECTION) if DESIGN_SELECTION.exists() else "missing",
            "required": "verified selected bins and direction",
            "status": "pass" if selection_verified() else "fail",
        },
    ]
    return rows, all(row["status"] == "pass" for row in rows), v16ac.FROZEN_LOCAL_RATE


def frozen_spec(local_rate: float) -> Dict[str, Any]:
    return {
        "purpose_ref": "purpose://prompt.unknown",
        "source_script_sha256": v16c.file_sha256(SOURCE_SCRIPT),
        "source_gate_sha256": v16c.file_sha256(SOURCE_GATE),
        "source_prereg_sha256": v16c.file_sha256(SOURCE_PREREG),
        "calibration_summary_sha256": v16c.file_sha256(CALIBRATION_SUMMARY),
        "calibration_effects_sha256": v16c.file_sha256(CALIBRATION_EFFECTS),
        "design_selection_sha256": v16c.file_sha256(DESIGN_SELECTION),
        "target_nodes": TARGET_NODES,
        "steps": STEPS,
        "events_per_initial_node": EVENTS_PER_INITIAL_NODE,
        "growth_seeds": list(GROWTH_SEEDS),
        "run_offsets": list(RUN_OFFSETS),
        "arms": list(ARMS),
        "topological_replays": TOPOLOGICAL_REPLAYS,
        "fresh_shuffles": FRESH_SHUFFLES,
        "local_rate": local_rate,
        "map": {
            "name": "normalized_simulation_clock_slabs",
            "selected_bins": list(SELECTED_BINS),
            "assignment": "floor(event_dt_midpoint / total_run_time * requested_bins)",
            "uses_causal_depth": False,
            "relabel_invariant": True,
            "scheduler_order_dependent": True,
        },
        "controls": ["equal_event_count_slabs", "shuffled_waiting_time_slabs"],
        "primary_observable": "clock_edge_retention_minus_control_edge_retention",
        "thresholds": {
            "max_local_median_clock_minus_null": MAX_LOCAL_MEDIAN_CLOCK_MINUS_NULL,
            "max_local_median_clock_minus_count": MAX_LOCAL_MEDIAN_CLOCK_MINUS_COUNT,
            "max_local_median_null_z": MAX_LOCAL_MEDIAN_NULL_Z,
            "min_local_negative_run_fraction": MIN_LOCAL_NEGATIVE_RUN_FRACTION,
            "discovery_holdout_magnitude_ratio_range": list(DISCOVERY_HOLDOUT_MAGNITUDE_RATIO_RANGE),
            "growth_magnitude_ratio_range": list(GROWTH_MAGNITUDE_RATIO_RANGE),
            "scheduler_magnitude_ratio_range": list(SCHEDULER_MAGNITUDE_RATIO_RANGE),
            "max_nonseed_event_tv": MAX_NONSEED_EVENT_TV,
            "min_reordered_position_fraction": MIN_REORDERED_POSITION_FRACTION,
        },
    }


def spec_digest(spec: Mapping[str, Any]) -> str:
    payload = json.dumps(spec, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def run_seed(growth_seed: int, run_offset: int, arm: str) -> int:
    arm_code = {"current_global": 0, "exposure_matched_local": 1}[arm]
    return TARGET_NODES * 1_000_000 + growth_seed * 10_000 + run_offset + arm_code * 100_000_000 + 16_005


def preregistration_rows(local_rate: float) -> List[Dict[str, Any]]:
    digest = spec_digest(frozen_spec(local_rate))
    rows: List[Dict[str, Any]] = []
    for growth_seed in GROWTH_SEEDS:
        for run_offset in RUN_OFFSETS:
            for arm in ARMS:
                rows.append({
                    "purpose_ref": "purpose://prompt.unknown",
                    "spec_digest": digest,
                    "source_script_sha256": v16c.file_sha256(SOURCE_SCRIPT),
                    "design_selection_sha256": v16c.file_sha256(DESIGN_SELECTION),
                    "target_nodes": TARGET_NODES,
                    "events_per_initial_node": EVENTS_PER_INITIAL_NODE,
                    "growth_seed": growth_seed,
                    "run_offset": run_offset,
                    "arm": arm,
                    "run_seed": run_seed(growth_seed, run_offset, arm),
                    "steps": STEPS,
                    "topological_replays": TOPOLOGICAL_REPLAYS,
                    "selected_bins": ";".join(map(str, SELECTED_BINS)),
                    "fresh_shuffles": FRESH_SHUFFLES,
                    "frozen_local_rate": local_rate,
                    "max_local_median_clock_minus_null": MAX_LOCAL_MEDIAN_CLOCK_MINUS_NULL,
                    "max_local_median_clock_minus_count": MAX_LOCAL_MEDIAN_CLOCK_MINUS_COUNT,
                    "max_local_median_null_z": MAX_LOCAL_MEDIAN_NULL_Z,
                    "min_local_negative_run_fraction": MIN_LOCAL_NEGATIVE_RUN_FRACTION,
                    "prepared_before_fresh_dynamics": 1,
                })
    return rows


def prepare() -> None:
    source_rows, source_pass, local_rate = source_contract_rows()
    if not source_pass:
        raise RuntimeError(f"v16d source contract failed: {source_rows}")
    rows = preregistration_rows(local_rate)
    write_csv(PREREG, rows)
    print(f"[v16e] prepared rows={len(rows)} digest={rows[0]['spec_digest']}")


def load_and_verify_preregistration() -> Tuple[List[Dict[str, str]], float, List[Dict[str, Any]]]:
    if not PREREG.exists():
        raise ValueError("missing v16e preregistration; run --prepare-only first")
    source_rows, source_pass, local_rate = source_contract_rows()
    if not source_pass:
        raise RuntimeError("v16d source contract no longer passes")
    observed = read_csv(PREREG)
    expected = preregistration_rows(local_rate)
    expected_digest = spec_digest(frozen_spec(local_rate))
    if len(observed) != len(expected):
        raise ValueError("v16e preregistration row count changed")
    if {row["spec_digest"] for row in observed} != {expected_digest}:
        raise ValueError("v16e preregistration digest changed")
    fields = ("growth_seed", "run_offset", "arm", "run_seed")
    observed_keys = {tuple(row[field] for field in fields) for row in observed}
    expected_keys = {tuple(str(row[field]) for field in fields) for row in expected}
    if observed_keys != expected_keys:
        raise ValueError("v16e preregistration assignments changed")
    return observed, local_rate, source_rows


def run_assignment(
    base: v7.State,
    assignment: Mapping[str, str],
    params: v7.Params,
    adapter: v16ac.LocalSeedClockAdapter,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any], List[Dict[str, Any]], Dict[str, Any], v16b.DependencyDAG, List[float]]:
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
    replay_rows = v16c.replay_audit(initial_state, final_state, trace, dag, params, prefix, int(assignment["run_seed"]))
    relabel_row = v16b.relabel_replay(initial_state, final_state, trace, dag, params, prefix)
    relabel_row["clock_map_transport_pass"] = int(
        int(relabel_row["edge_set_equal"]) == 1 and len(trace) == len(analysis["depths"])
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
        "clock_map_transport_pass": relabel_row["clock_map_transport_pass"],
    }
    for event_type in EVENT_TYPES:
        run_row[f"{event_type}_events"] = event_counts[event_type]
    return event_rows, dependency_rows, run_row, replay_rows, relabel_row, dag, [item.dt for item in trace]


def fresh_map_products(
    dag: v16b.DependencyDAG,
    dts: Sequence[float],
    prefix: Mapping[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    summaries: List[Dict[str, Any]] = []
    audits: List[Dict[str, Any]] = []
    effects: List[Dict[str, Any]] = []
    memberships: List[Dict[str, Any]] = []
    coarse_edges: List[Dict[str, Any]] = []
    for bin_count in SELECTED_BINS:
        common = {**prefix, "requested_bins": bin_count}
        clock_assignments = normalized_clock_bins(dts, bin_count)
        count_assignments = event_count_bins(len(dts), bin_count)
        clock_prefix = {**common, "map_kind": "clock", "shuffle_index": -1, "shuffle_seed": ""}
        count_prefix = {**common, "map_kind": "event_count", "shuffle_index": -1, "shuffle_seed": ""}
        clock_summary, clock_audit = quotient_summary(dag, clock_assignments, clock_prefix)
        count_summary, count_audit = quotient_summary(dag, count_assignments, count_prefix)
        summaries.extend((clock_summary, count_summary))
        audits.extend((clock_audit, count_audit))
        clock_memberships, clock_edges = quotient_artifact_rows(dag, clock_assignments, clock_prefix)
        count_memberships, count_edges = quotient_artifact_rows(dag, count_assignments, count_prefix)
        memberships.extend(clock_memberships)
        memberships.extend(count_memberships)
        coarse_edges.extend(clock_edges)
        coarse_edges.extend(count_edges)
        shuffled_summaries: List[Dict[str, Any]] = []
        for shuffle_index in range(FRESH_SHUFFLES):
            shuffle_seed = stable_seed(
                prefix["growth_seed"], prefix["run_offset"], prefix["arm"], prefix["run_seed"],
                bin_count, shuffle_index, "v16e_fresh",
            )
            shuffle_prefix = {
                **common,
                "map_kind": "shuffled_clock",
                "shuffle_index": shuffle_index,
                "shuffle_seed": shuffle_seed,
            }
            shuffled_summary, shuffled_audit = quotient_summary(
                dag,
                shuffled_clock_bins(dts, bin_count, shuffle_seed),
                shuffle_prefix,
            )
            shuffled_summaries.append(shuffled_summary)
            summaries.append(shuffled_summary)
            audits.append(shuffled_audit)
        null_values = [float(row["edge_retention"]) for row in shuffled_summaries]
        null_mean = mean(null_values)
        null_sd = sample_sd(null_values)
        clock_value = float(clock_summary["edge_retention"])
        effects.append({
            **common,
            "clock_edge_retention": clock_value,
            "event_count_edge_retention": count_summary["edge_retention"],
            "shuffle_mean_edge_retention": null_mean,
            "shuffle_sd_edge_retention": null_sd,
            "clock_minus_shuffle_mean": clock_value - null_mean,
            "clock_null_z": (clock_value - null_mean) / null_sd if null_sd > TOLERANCE else 0.0,
            "clock_minus_event_count": clock_value - float(count_summary["edge_retention"]),
            "clock_occupied_bins": clock_summary["occupied_bins"],
            "clock_occupancy_cv": clock_summary["occupancy_cv"],
            "all_map_integrity_pass": int(
                int(clock_audit["map_integrity_pass"])
                and int(count_audit["map_integrity_pass"])
                and all(int(row["map_integrity_pass"]) for row in audits[-FRESH_SHUFFLES:])
            ),
        })
    return summaries, audits, effects, memberships, coarse_edges


def selection_lookup() -> Dict[int, Dict[str, str]]:
    if not selection_verified():
        raise ValueError("v16e design selection failed verification")
    return {int(row["requested_bins"]): row for row in read_csv(DESIGN_SELECTION)}


def local_effect_rows(effect_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    discovery = selection_lookup()
    rows: List[Dict[str, Any]] = []
    local = [row for row in effect_rows if row["arm"] == "exposure_matched_local"]
    for bin_count in SELECTED_BINS:
        subset = [row for row in local if int(row["requested_bins"]) == bin_count]
        deltas = [float(row["clock_minus_shuffle_mean"]) for row in subset]
        count_deltas = [float(row["clock_minus_event_count"]) for row in subset]
        z_values = [float(row["clock_null_z"]) for row in subset]
        median_delta = median(deltas)
        discovery_delta = float(discovery[bin_count]["calibration_local_median_clock_minus_shuffle"])
        magnitude_ratio = abs(median_delta) / abs(discovery_delta) if abs(discovery_delta) > TOLERANCE else float("inf")
        negative_fraction = mean(value < 0.0 for value in deltas)
        effect_pass = (
            len(subset) == len(GROWTH_SEEDS) * len(RUN_OFFSETS)
            and median_delta <= MAX_LOCAL_MEDIAN_CLOCK_MINUS_NULL
            and median(count_deltas) <= MAX_LOCAL_MEDIAN_CLOCK_MINUS_COUNT
            and median(z_values) <= MAX_LOCAL_MEDIAN_NULL_Z
            and negative_fraction >= MIN_LOCAL_NEGATIVE_RUN_FRACTION
            and DISCOVERY_HOLDOUT_MAGNITUDE_RATIO_RANGE[0] <= magnitude_ratio <= DISCOVERY_HOLDOUT_MAGNITUDE_RATIO_RANGE[1]
        )
        rows.append({
            "requested_bins": bin_count,
            "n_local_runs": len(subset),
            "median_clock_minus_shuffle": median_delta,
            "median_clock_minus_event_count": median(count_deltas),
            "median_clock_null_z": median(z_values),
            "negative_run_fraction": negative_fraction,
            "discovery_median_clock_minus_shuffle": discovery_delta,
            "holdout_over_discovery_magnitude_ratio": magnitude_ratio,
            "magnitude_ratio_low": DISCOVERY_HOLDOUT_MAGNITUDE_RATIO_RANGE[0],
            "magnitude_ratio_high": DISCOVERY_HOLDOUT_MAGNITUDE_RATIO_RANGE[1],
            "local_effect_pass": int(effect_pass),
        })
    return rows


def growth_effect_rows(effect_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    local = [row for row in effect_rows if row["arm"] == "exposure_matched_local"]
    rows: List[Dict[str, Any]] = []
    for bin_count in SELECTED_BINS:
        medians = {
            seed: median(
                abs(float(row["clock_minus_shuffle_mean"]))
                for row in local
                if int(row["requested_bins"]) == bin_count and int(row["growth_seed"]) == seed
            )
            for seed in GROWTH_SEEDS
        }
        value_ratio = medians[GROWTH_SEEDS[1]] / medians[GROWTH_SEEDS[0]] if medians[GROWTH_SEEDS[0]] > TOLERANCE else float("inf")
        rows.append({
            "requested_bins": bin_count,
            f"growth_{GROWTH_SEEDS[0]}_median_abs_effect": medians[GROWTH_SEEDS[0]],
            f"growth_{GROWTH_SEEDS[1]}_median_abs_effect": medians[GROWTH_SEEDS[1]],
            "second_over_first_magnitude_ratio": value_ratio,
            "ratio_low": GROWTH_MAGNITUDE_RATIO_RANGE[0],
            "ratio_high": GROWTH_MAGNITUDE_RATIO_RANGE[1],
            "growth_effect_pass": int(GROWTH_MAGNITUDE_RATIO_RANGE[0] <= value_ratio <= GROWTH_MAGNITUDE_RATIO_RANGE[1]),
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


def scheduler_effect_rows(
    effect_rows: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    tv = nonseed_event_tv(run_rows)
    for bin_count in SELECTED_BINS:
        medians = {
            arm: median(
                abs(float(row["clock_minus_shuffle_mean"]))
                for row in effect_rows
                if int(row["requested_bins"]) == bin_count and row["arm"] == arm
            )
            for arm in ARMS
        }
        value_ratio = medians["exposure_matched_local"] / medians["current_global"] if medians["current_global"] > TOLERANCE else float("inf")
        rows.append({
            "requested_bins": bin_count,
            "current_global_median_abs_effect": medians["current_global"],
            "local_median_abs_effect": medians["exposure_matched_local"],
            "local_over_global_magnitude_ratio": value_ratio,
            "ratio_low": SCHEDULER_MAGNITUDE_RATIO_RANGE[0],
            "ratio_high": SCHEDULER_MAGNITUDE_RATIO_RANGE[1],
            "scheduler_effect_pass": int(SCHEDULER_MAGNITUDE_RATIO_RANGE[0] <= value_ratio <= SCHEDULER_MAGNITUDE_RATIO_RANGE[1]),
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
    map_rows: Sequence[Mapping[str, Any]],
    effect_rows: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], str]:
    expected_runs = len(GROWTH_SEEDS) * len(RUN_OFFSETS) * len(ARMS)
    expected_maps = expected_runs * len(SELECTED_BINS) * (2 + FRESH_SHUFFLES)
    target_pass = len(target_rows) == 1 and int(target_rows[0]["mean_initial_nodes"]) == TARGET_NODES
    run_integrity = len(run_rows) == expected_runs and all(int(row["n_events"]) == STEPS and int(row["invalid_events"]) == 0 for row in run_rows)
    fine_dag_integrity = all(int(row["fine_acyclic"]) and int(row["fine_edge_witness_errors"]) == 0 for row in run_rows)
    replay_pass = (
        len(replay_rows) == expected_runs * TOPOLOGICAL_REPLAYS
        and all(int(row["topological_order_valid"]) and int(row["context_failures"]) == 0 and int(row["final_structure_equal"]) for row in replay_rows)
        and all(float(row["changed_position_fraction"]) >= MIN_REORDERED_POSITION_FRACTION for row in replay_rows)
    )
    relabel_pass = len(relabel_rows) == expected_runs and all(int(row["relabel_pass"]) and int(row["clock_map_transport_pass"]) for row in relabel_rows)
    map_integrity = len(map_rows) == expected_maps and all(int(row["map_integrity_pass"]) for row in map_rows)
    map_coverage = all(
        int(row["occupied_bins"]) == int(row["requested_bins"])
        for row in map_rows
        if row["map_kind"] in {"clock", "event_count"}
    )
    effect_integrity = len(effect_rows) == expected_runs * len(SELECTED_BINS) and all(int(row["all_map_integrity_pass"]) for row in effect_rows)
    local_effect = len(local_rows) == len(SELECTED_BINS) and all(int(row["local_effect_pass"]) for row in local_rows)
    growth_effect = len(growth_rows) == len(SELECTED_BINS) and all(int(row["growth_effect_pass"]) for row in growth_rows)
    scheduler_effect = len(scheduler_rows) == len(SELECTED_BINS) and all(int(row["scheduler_effect_pass"]) and int(row["nonseed_tv_pass"]) for row in scheduler_rows)
    exact_pass = all((source_pass, target_pass, run_integrity, fine_dag_integrity, replay_pass, relabel_pass, map_integrity, map_coverage, effect_integrity))
    all_pass = exact_pass and local_effect and growth_effect and scheduler_effect
    if all_pass:
        overall = "pass_to_v16f_cross_map_relation_gate"
    elif exact_pass:
        overall = "clock_map_exact_but_null_equivalent"
    else:
        overall = "v16e_instrumentation_failed"
    gates = [
        {"gate": "v16d_source_contract", "status": "pass" if source_pass else "fail", "observed": int(source_pass), "required": 1, "decision": "continue"},
        {"gate": "fresh_target_hygiene", "status": "pass" if target_pass else "fail", "observed": target_rows[0]["mean_initial_nodes"] if target_rows else "missing", "required": TARGET_NODES, "decision": "continue" if target_pass else "stop"},
        {"gate": "fresh_run_integrity", "status": "pass" if run_integrity else "fail", "observed": f"runs={len(run_rows)};invalid={sum(int(row['invalid_events']) for row in run_rows)}", "required": f"runs={expected_runs};invalid=0", "decision": "continue"},
        {"gate": "fine_dag_integrity", "status": "pass" if fine_dag_integrity else "fail", "observed": f"acyclic={sum(int(row['fine_acyclic']) for row in run_rows)};witness_errors={sum(int(row['fine_edge_witness_errors']) for row in run_rows)}", "required": f"acyclic={expected_runs};witness_errors=0", "decision": "continue"},
        {"gate": "fresh_topological_replay", "status": "pass" if replay_pass else "fail", "observed": f"replays={len(replay_rows)};min_reorder={min(float(row['changed_position_fraction']) for row in replay_rows):.6f};failures={sum(not int(row['final_structure_equal']) or int(row['context_failures']) for row in replay_rows)}", "required": f"replays={expected_runs * TOPOLOGICAL_REPLAYS};failures=0", "decision": "continue"},
        {"gate": "relabel_and_clock_map_transport", "status": "pass" if relabel_pass else "fail", "observed": sum(int(row["relabel_pass"]) and int(row["clock_map_transport_pass"]) for row in relabel_rows), "required": expected_runs, "decision": "continue" if relabel_pass else "repair_map"},
        {"gate": "all_map_integrity", "status": "pass" if map_integrity else "fail", "observed": f"passes={sum(int(row['map_integrity_pass']) for row in map_rows)}/{len(map_rows)}", "required": expected_maps, "decision": "continue" if map_integrity else "repair_map"},
        {"gate": "primary_control_bin_coverage", "status": "pass" if map_coverage else "fail", "observed": int(map_coverage), "required": 1, "decision": "continue" if map_coverage else "reject_bins"},
        {"gate": "effect_row_integrity", "status": "pass" if effect_integrity else "fail", "observed": len(effect_rows), "required": expected_runs * len(SELECTED_BINS), "decision": "continue"},
        {"gate": "local_clock_null_effect", "status": "pass" if local_effect else "fail", "observed": ";".join(f"{row['requested_bins']}:{float(row['median_clock_minus_shuffle']):.6f}:z={float(row['median_clock_null_z']):.3f}:neg={float(row['negative_run_fraction']):.3f}:ratio={float(row['holdout_over_discovery_magnitude_ratio']):.3f}" for row in local_rows), "required": f"delta<={MAX_LOCAL_MEDIAN_CLOCK_MINUS_NULL};count_delta<={MAX_LOCAL_MEDIAN_CLOCK_MINUS_COUNT};z<={MAX_LOCAL_MEDIAN_NULL_Z};negative>={MIN_LOCAL_NEGATIVE_RUN_FRACTION:.3f};discovery_ratio in {DISCOVERY_HOLDOUT_MAGNITUDE_RATIO_RANGE}", "decision": "continue" if local_effect else "clock_map_null_equivalent"},
        {"gate": "growth_effect_transfer", "status": "pass" if growth_effect else "fail", "observed": ";".join(f"{row['requested_bins']}={float(row['second_over_first_magnitude_ratio']):.6f}" for row in growth_rows), "required": f"each in {GROWTH_MAGNITUDE_RATIO_RANGE}", "decision": "continue" if growth_effect else "hold"},
        {"gate": "scheduler_effect_diagnostic", "status": "pass" if scheduler_effect else "fail", "observed": ";".join(f"{row['requested_bins']}={float(row['local_over_global_magnitude_ratio']):.6f}" for row in scheduler_rows) + f";tv={float(scheduler_rows[0]['nonseed_event_tv']):.6f}", "required": f"ratios in {SCHEDULER_MAGNITUDE_RATIO_RANGE};tv<={MAX_NONSEED_EVENT_TV}", "decision": "continue" if scheduler_effect else "hold"},
        {"gate": "v16e_overall", "status": overall, "observed": int(all_pass), "required": 1, "decision": "design_cross_map_relation" if all_pass else ("retire_clock_map_signal" if exact_pass else "repair_instrumentation")},
    ]
    return gates, overall


def claim_rows(status: str) -> List[Dict[str, Any]]:
    exact = status in {"pass_to_v16f_cross_map_relation_gate", "clock_map_exact_but_null_equivalent"}
    signal = status == "pass_to_v16f_cross_map_relation_gate"
    return [
        {"claim_id": "C1", "statement": "Equal simulation-time slabs define relabel-invariant witnessed acyclic quotient DAGs on fresh histories.", "status": "supported" if exact else "not_supported", "evidence": "v16e_map_audit.csv;v16e_primary_control_coarse_edges.csv", "scope_limit": "clock map depends on executed event order and simulation time"},
        {"claim_id": "C2", "statement": "Actual clock slabs retain fewer dependency edges than shuffled-waiting-time and equal-event-count controls at all three frozen resolutions.", "status": "supported" if signal else "not_supported", "evidence": "v16e_local_effect_gate.csv;v16e_null_effects.csv", "scope_limit": "target 1536, six fresh local runs, preregistered effect bounds"},
        {"claim_id": "C3", "statement": "Clock-aligned dependency clustering transfers across fresh growth seeds and the scheduler diagnostic.", "status": "supported" if signal else "not_supported", "evidence": "v16e_growth_effect_transfer.csv;v16e_scheduler_effect_transfer.csv", "scope_limit": "two growth seeds and broad magnitude-ratio bounds"},
        {"claim_id": "C4", "statement": "The clock-slab result independently proves the same structure as the causal-depth map.", "status": "unsupported", "evidence": "none", "scope_limit": "v16e tests a different clock-alignment property; cross-map relation remains untested"},
        {"claim_id": "C5", "statement": "Clock-slab clustering establishes Lorentz symmetry, proper time, or emergent spacetime.", "status": "unsupported", "evidence": "none", "scope_limit": "simulation time is an implementation clock, not a validated physical metric"},
        {"claim_id": "C6", "statement": "The finite quotient results establish continuum, particles, entanglement, or universal causal laws.", "status": "unsupported", "evidence": "none", "scope_limit": "not tested by v16e"},
    ]


def build_report(
    source_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    effect_rows: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# UniverseSimulation v16e: independent clock-slab coarse-map gate",
        "",
        "## Research question",
        "",
        "Does an independently defined, relabel-invariant simulation-clock coarse map expose dependency clustering that survives fresh holdout and exceeds both equal-event-count and shuffled-waiting-time controls?",
        "",
        "## Evidential separation",
        "",
        "- Discovery artifact: old v16c/v16d histories selected nondegenerate resolutions and a negative edge-retention direction before fresh dynamics.",
        "- Frozen candidate: equal intervals of normalized simulation time at 128, 64, and 32 bins; no causal depth enters the assignment.",
        "- Controls: equal-event-count slabs and 32 deterministic shuffled-waiting-time maps per run and resolution.",
        "- Primary observable: clock quotient edge retention minus control edge retention. Lower values mean more direct dependencies are internalized by actual clock slabs.",
        "- Actual dynamics: twelve fresh target-1536 histories were generated after design selection and preregistration.",
        "- Negative boundary: the simulation clock is not assumed to be proper time or a physical metric.",
        "",
        "## Source contract",
        "",
    ]
    lines.extend(v16c.table(source_rows, ("check", "observed", "required", "status")))
    lines.extend([
        "",
        "## Fresh design",
        "",
        f"Target `{TARGET_NODES}`, growth seeds `{GROWTH_SEEDS[0]}/{GROWTH_SEEDS[1]}`, offsets `{RUN_OFFSETS[0]}/{RUN_OFFSETS[1]}/{RUN_OFFSETS[2]}`, `{STEPS}` events, two scheduler arms, selected bins `{SELECTED_BINS}`, and `{FRESH_SHUFFLES}` waiting-time shuffles per run and resolution.",
        "",
        "Target hygiene:",
        "",
    ])
    lines.extend(v16c.table(target_rows, ("target_nodes", "growth_replicates", "mean_initial_nodes", "mean_initial_tokens", "mean_initial_beta1")))
    lines.extend(["", "## Fine-history controls", ""])
    lines.extend(v16c.table(run_rows, ("growth_seed", "run_offset", "arm", "n_events", "fine_edges", "fine_causal_depth", "topological_replay_failures", "relabel_pass", "clock_map_transport_pass")))
    lines.extend(["", "## Fresh run-level null effects", ""])
    lines.extend(v16c.table(effect_rows, ("growth_seed", "run_offset", "arm", "requested_bins", "clock_edge_retention", "event_count_edge_retention", "shuffle_mean_edge_retention", "clock_minus_shuffle_mean", "clock_null_z", "clock_minus_event_count")))
    lines.extend(["", "## Local primary gate", ""])
    lines.extend(v16c.table(local_rows, ("requested_bins", "median_clock_minus_shuffle", "median_clock_minus_event_count", "median_clock_null_z", "negative_run_fraction", "holdout_over_discovery_magnitude_ratio", "local_effect_pass")))
    lines.extend(["", "## Growth-seed transfer", ""])
    lines.extend(v16c.table(growth_rows, ("requested_bins", f"growth_{GROWTH_SEEDS[0]}_median_abs_effect", f"growth_{GROWTH_SEEDS[1]}_median_abs_effect", "second_over_first_magnitude_ratio", "growth_effect_pass")))
    lines.extend(["", "## Scheduler diagnostic", ""])
    lines.extend(v16c.table(scheduler_rows, ("requested_bins", "current_global_median_abs_effect", "local_median_abs_effect", "local_over_global_magnitude_ratio", "scheduler_effect_pass", "nonseed_event_tv", "nonseed_tv_pass")))
    lines.extend(["", "## Gate evaluation", ""])
    lines.extend(v16c.table(gate_rows, ("gate", "status", "observed", "required", "decision")))
    lines.extend(["", f"Overall status: `{overall}`.", "", "## Interpretation", ""])
    if overall == "pass_to_v16f_cross_map_relation_gate":
        lines.append("The actual simulation clock groups direct dependencies more strongly than both chronological equal-count slabs and shuffled waiting-time clocks at all three frozen resolutions. The effect survives fresh seeds, discovery-to-holdout magnitude checks, and the scheduler diagnostic. This is a non-null independent coarse-map signal, but it is not yet evidence that the clock and causal-depth maps represent one common geometry.")
    elif overall == "clock_map_exact_but_null_equivalent":
        lines.append("The clock map is technically valid, but its edge-retention effect does not survive the preregistered null or transfer gates. Retain the implementation as a control and do not treat simulation time as an independent organizing observable.")
    else:
        lines.append("An exact source, target, replay, relabel, assignment, witness, acyclicity, or coverage condition failed. Treat the round as instrumentation failure, not a map result.")
    lines.extend([
        "",
        "The edge-retention statistic is not a Lorentz diagnostic. A waiting-time-aligned dependency cluster can arise from the stochastic scheduler and local rate structure without defining a metric, light cone, observer transformation, or continuum.",
        "",
        "## Next decision",
        "",
    ])
    if overall == "pass_to_v16f_cross_map_relation_gate":
        lines.append("Preregister one v16f cross-map relation test: quantify whether clock slabs and causal-depth quotients align more than matched size/order nulls on the same fresh histories. Do not add a third map or increase target size first.")
    elif overall == "clock_map_exact_but_null_equivalent":
        lines.append("Stop clock-map promotion. Reassess whether a support-space map can be made acyclic without causal-depth leakage before new dynamics.")
    else:
        lines.append("Repair only the smallest instrumentation defect before any new dynamics.")
    lines.append("")
    return "\n".join(lines)


def verify_outputs() -> None:
    assignments, _, _ = load_and_verify_preregistration()
    expected_runs = len(assignments)
    expected_maps = expected_runs * len(SELECTED_BINS) * (2 + FRESH_SHUFFLES)
    run_rows = read_csv(DOC / "v16e_run_summary.csv")
    event_rows = read_csv(DOC / "v16e_event_log.csv")
    fine_edges = read_csv(DOC / "v16e_fine_dependency_edges.csv")
    summaries = read_csv(DOC / "v16e_map_summary.csv")
    audits = read_csv(DOC / "v16e_map_audit.csv")
    effects = read_csv(DOC / "v16e_null_effects.csv")
    memberships = read_csv(DOC / "v16e_primary_control_membership.csv")
    coarse_edges = read_csv(DOC / "v16e_primary_control_coarse_edges.csv")
    replay_rows = read_csv(DOC / "v16e_topological_replay_audit.csv")
    relabel_rows = read_csv(DOC / "v16e_relabel_replay_audit.csv")
    gate_rows = read_csv(DOC / "v16e_gate_evaluation.csv")
    key_fields = ("growth_seed", "run_offset", "arm", "run_seed")

    def key(row: Mapping[str, str]) -> Tuple[str, ...]:
        return tuple(row[field] for field in key_fields)

    assignment_keys = {key(row) for row in assignments}
    assert len(run_rows) == expected_runs and {key(row) for row in run_rows} == assignment_keys
    assert len(event_rows) == expected_runs * STEPS
    assert len(summaries) == expected_maps and len(audits) == expected_maps
    assert len(effects) == expected_runs * len(SELECTED_BINS)
    assert len(memberships) == expected_runs * len(SELECTED_BINS) * 2 * STEPS
    assert len(replay_rows) == expected_runs * TOPOLOGICAL_REPLAYS
    assert len(relabel_rows) == expected_runs
    assert all(int(row["map_integrity_pass"]) == 1 for row in audits)
    assert all(int(row["relabel_pass"]) == 1 and int(row["clock_map_transport_pass"]) == 1 for row in relabel_rows)
    assert all(
        int(row["topological_order_valid"]) == 1
        and int(row["context_failures"]) == 0
        and int(row["final_structure_equal"]) == 1
        for row in replay_rows
    )
    events_by_run: Dict[Tuple[str, ...], Set[int]] = defaultdict(set)
    fine_edge_count: Counter[Tuple[str, ...]] = Counter()
    members_by_map: Dict[Tuple[Tuple[str, ...], int, str], List[Dict[str, str]]] = defaultdict(list)
    edges_by_map: Counter[Tuple[Tuple[str, ...], int, str]] = Counter()
    summary_by_map: Dict[Tuple[Tuple[str, ...], int, str], Dict[str, str]] = {}
    for row in event_rows:
        events_by_run[key(row)].add(int(row["event_id"]))
    for row in fine_edges:
        fine_edge_count[key(row)] += 1
    for row in memberships:
        members_by_map[(key(row), int(row["requested_bins"]), row["map_kind"])].append(row)
    for row in coarse_edges:
        assert int(row["fine_edge_witness_count"]) >= 1
        edges_by_map[(key(row), int(row["requested_bins"]), row["map_kind"])] += 1
    for row in summaries:
        if row["map_kind"] in {"clock", "event_count"}:
            summary_by_map[(key(row), int(row["requested_bins"]), row["map_kind"])] = row
    for run_key in assignment_keys:
        assert events_by_run[run_key] == set(range(STEPS))
        for bin_count in SELECTED_BINS:
            for map_kind in ("clock", "event_count"):
                map_key = (run_key, bin_count, map_kind)
                rows = members_by_map[map_key]
                assert {int(row["event_id"]) for row in rows} == set(range(STEPS))
                assert edges_by_map[map_key] == int(summary_by_map[map_key]["coarse_edges"])
    overall = [row for row in gate_rows if row["gate"] == "v16e_overall"]
    assert len(overall) == 1 and overall[0]["status"] in {
        "pass_to_v16f_cross_map_relation_gate",
        "clock_map_exact_but_null_equivalent",
        "v16e_instrumentation_failed",
    }
    print(
        f"[v16e] output verification pass runs={expected_runs} events={len(event_rows)} "
        f"maps={len(summaries)} memberships={len(memberships)} overall={overall[0]['status']}"
    )


def run() -> None:
    assignments, local_rate, source_rows = load_and_verify_preregistration()
    adapter = v16ac.LocalSeedClockAdapter(local_rate)
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    target_rows = v10e.summarize_bases(base_rows)
    if len(target_rows) != 1 or int(target_rows[0]["mean_initial_nodes"]) != TARGET_NODES:
        raise RuntimeError("v16e target hygiene failed")
    ensemble_name = ensembles[0].name
    params = v16a.anchor_params()
    event_rows: List[Dict[str, Any]] = []
    fine_edge_rows: List[Dict[str, Any]] = []
    run_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    relabel_rows: List[Dict[str, Any]] = []
    map_summary_rows: List[Dict[str, Any]] = []
    map_audit_rows: List[Dict[str, Any]] = []
    effect_rows: List[Dict[str, Any]] = []
    membership_rows: List[Dict[str, Any]] = []
    coarse_edge_rows: List[Dict[str, Any]] = []
    for index, assignment in enumerate(assignments, start=1):
        base = base_states[(ensemble_name, int(assignment["growth_seed"]))]
        events, fine_edges, run_row, replays, relabel, dag, dts = run_assignment(base, assignment, params, adapter)
        prefix = {field: run_row[field] for field in ("growth_seed", "run_offset", "arm", "run_seed")}
        summaries, audits, effects, memberships, coarse_edges = fresh_map_products(dag, dts, prefix)
        event_rows.extend(events)
        fine_edge_rows.extend(fine_edges)
        run_rows.append(run_row)
        replay_rows.extend(replays)
        relabel_rows.append(relabel)
        map_summary_rows.extend(summaries)
        map_audit_rows.extend(audits)
        effect_rows.extend(effects)
        membership_rows.extend(memberships)
        coarse_edge_rows.extend(coarse_edges)
        print(
            f"[v16e] runs={index}/{len(assignments)} arm={assignment['arm']} "
            + " ".join(
                f"b{row['requested_bins']}={float(row['clock_minus_shuffle_mean']):.6f}"
                for row in effects
            )
        )
    local_rows = local_effect_rows(effect_rows)
    growth_rows = growth_effect_rows(effect_rows)
    scheduler_rows = scheduler_effect_rows(effect_rows, run_rows)
    gate_rows, overall = gate_evaluation(
        True, target_rows, run_rows, replay_rows, relabel_rows, map_audit_rows,
        effect_rows, local_rows, growth_rows, scheduler_rows,
    )
    write_csv(DOC / "v16e_source_chain.csv", source_rows)
    write_csv(DOC / "v16e_target_summary.csv", target_rows)
    write_csv(DOC / "v16e_event_log.csv", event_rows)
    write_csv(DOC / "v16e_fine_dependency_edges.csv", fine_edge_rows)
    write_csv(DOC / "v16e_run_summary.csv", run_rows)
    write_csv(DOC / "v16e_map_summary.csv", map_summary_rows)
    write_csv(DOC / "v16e_map_audit.csv", map_audit_rows)
    write_csv(DOC / "v16e_null_effects.csv", effect_rows)
    write_csv(DOC / "v16e_primary_control_membership.csv", membership_rows)
    write_csv(DOC / "v16e_primary_control_coarse_edges.csv", coarse_edge_rows)
    write_csv(DOC / "v16e_topological_replay_audit.csv", replay_rows)
    write_csv(DOC / "v16e_relabel_replay_audit.csv", relabel_rows)
    write_csv(DOC / "v16e_local_effect_gate.csv", local_rows)
    write_csv(DOC / "v16e_growth_effect_transfer.csv", growth_rows)
    write_csv(DOC / "v16e_scheduler_effect_transfer.csv", scheduler_rows)
    write_csv(DOC / "v16e_gate_evaluation.csv", gate_rows)
    write_csv(DOC / "v16e_claim_ledger.csv", claim_rows(overall))
    report = build_report(source_rows, target_rows, run_rows, effect_rows, local_rows, growth_rows, scheduler_rows, gate_rows, overall)
    (DOC / "v16e_clock_slab_map_gate.md").write_text(report, encoding="utf-8")
    recommendation = "\n".join([
        "# Operativ anbefaling v0.16e",
        "",
        f"Status: `{overall}`.",
        "",
        "- Behold clock-map-resultatet avgrenset til faktisk simuleringstid, target 1536 og de frosne 128/64/32-opplosningene.",
        "- Ved full pass: test relasjonen mellom clock-map og causal-depth-map paa nye data; ikke kall dem samme geometri ennaa.",
        "- Ved null-ekvivalens: behold clock-map som kontroll og stopp denne observabelretningen uten refit.",
        "- Clock-map er scheduler-order-dependent selv om det er relabel-invariant; ikke presenter det som observer-uavhengig tid.",
        "- Ikke promoter signalet til Lorentz-symmetri, proper time, spacetime eller continuum.",
        "",
    ])
    (DOC / "v0_16e_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    lay = "\n".join([
        "# v0.16e for ikke-spesialister",
        "",
        "Vi delte hver simulering i like store biter av faktisk simulert tid og spurte om hendelser som er direkte avhengige av hverandre oftere havner i samme tidsbit enn de gjoer med tilfeldige ventetider eller bare like mange hendelser per bit.",
        "",
        f"Statusen er `{overall}`. Et positivt resultat betyr at simuleringsklokken baerer en repeterbar organisering av lokale avhengigheter. Det betyr ikke at klokken er fysisk tid, proper time eller romtid.",
        "",
    ])
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16e.md").write_text(lay, encoding="utf-8")
    print(
        f"[v16e] overall={overall} runs={len(run_rows)} events={len(event_rows)} "
        f"maps={len(map_summary_rows)} effects={len(effect_rows)}"
    )


def self_test() -> None:
    assert SELECTED_BINS == (128, 64, 32)
    assert STEPS == TARGET_NODES * EVENTS_PER_INITIAL_NODE
    dts = [1.0, 2.0, 1.0, 4.0]
    clock = normalized_clock_bins(dts, 4)
    assert all(left <= right for left, right in zip(clock, clock[1:]))
    assert event_count_bins(4, 4) == [0, 1, 2, 3]
    dag = v16b.DependencyDAG()
    dag.predecessors = [{}, {0: {"RAW:node:0"}}, {}, {1: {"RAW:node:1"}, 2: {"RAW:node:2"}}]
    summary, audit = quotient_summary(dag, [0, 0, 1, 1], {"map_kind": "self_test", "requested_bins": 2})
    assert int(audit["map_integrity_pass"]) == 1
    assert int(summary["occupied_bins"]) == 2
    assert int(summary["coarse_edges"]) == 1
    print("[v16e] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16e independent clock-slab map gate")
    parser.add_argument("--design-audit", action="store_true")
    parser.add_argument("--freeze-design", action="store_true")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    modes = sum((
        args.design_audit,
        args.freeze_design,
        args.prepare_only,
        args.self_test,
        args.verify_only,
    ))
    if modes > 1:
        parser.error("choose at most one mode")
    if args.self_test:
        self_test()
    elif args.design_audit:
        design_audit()
    elif args.freeze_design:
        freeze_design()
    elif args.prepare_only:
        prepare()
    elif args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
