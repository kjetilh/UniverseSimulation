#!/usr/bin/env python3
"""v16f preregistered clock/depth cross-map relation gate.

The primary statistic compares the depth-window-16 event partition with the
frozen v16e simulation-clock partitions using normalized mutual information.
Equal-event-count slabs, shuffled waiting times, and monotone slabs preserving
the exact clock-bin size multiset are explicit controls.

v16e histories already exist, so this is a frozen-data analysis holdout, not a
new dynamical holdout. It does not test Lorentz symmetry, physical time,
spacetime, continuum limits, particles, entanglement, or universal causality.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v16c_three_scale_coarse_graining_pilot as v16c
import relational_universe_v16e_clock_slab_map_gate as v16e


DOC = Path("Documentation")
SCRIPT = Path("relational_universe_v16f_cross_map_relation_gate.py")
CALIBRATION_RUNS = DOC / "v16f_design_calibration_relation_runs.csv"
CALIBRATION_NULLS = DOC / "v16f_design_calibration_null_distribution.csv"
DESIGN_SELECTION = DOC / "v16f_design_selection.csv"
PREREG = DOC / "v16f_pre_registration.csv"
CALIBRATION_STAGES = ("v16c", "v16d")
SELECTED_CLOCK_BINS = (128, 64, 32)
DEPTH_WINDOW = 16
CALIBRATION_NULL_REPLICATES = 64
HOLDOUT_NULL_REPLICATES = 64
ARMS = ("current_global", "exposure_matched_local")
PRIMARY_ARM = "exposure_matched_local"

MAX_MEDIAN_NMI_DELTA = -0.005
MAX_MEDIAN_NULL_Z = -2.0
MIN_NEGATIVE_RUN_FRACTION = 5.0 / 6.0
CALIBRATION_TRANSFER_RANGE = (0.50, 2.00)
HOLDOUT_CALIBRATION_RANGE = (0.50, 2.00)
GROWTH_TRANSFER_RANGE = (0.60, 1.67)
SCHEDULER_TRANSFER_RANGE = (0.60, 1.67)
TOLERANCE = 1.0e-12

read_csv = v16c.read_csv
write_csv = v16c.write_csv
mean = v16c.mean
median = v16c.median
sample_sd = v16e.sample_sd
stable_seed = v16e.stable_seed

RUN_FIELDS = ("growth_seed", "run_offset", "arm", "run_seed")


def run_key(row: Mapping[str, Any]) -> Tuple[str, ...]:
    return tuple(str(row[field]) for field in RUN_FIELDS)


def numeric_prefix(key: Sequence[str]) -> Dict[str, Any]:
    return {
        "growth_seed": int(key[0]),
        "run_offset": int(key[1]),
        "arm": key[2],
        "run_seed": int(key[3]),
    }


def group_rows(path: Path) -> Dict[Tuple[str, ...], List[Dict[str, str]]]:
    grouped: Dict[Tuple[str, ...], List[Dict[str, str]]] = defaultdict(list)
    for row in read_csv(path):
        grouped[run_key(row)].append(row)
    return grouped


def partition_information(
    left: Sequence[int],
    right: Sequence[int],
) -> Dict[str, float]:
    if len(left) != len(right) or not left:
        raise ValueError("partition labels must have equal nonzero length")
    n = len(left)
    left_counts = Counter(left)
    right_counts = Counter(right)
    joint_counts = Counter(zip(left, right))
    left_entropy = -sum((count / n) * math.log(count / n) for count in left_counts.values())
    right_entropy = -sum((count / n) * math.log(count / n) for count in right_counts.values())
    mutual_information = sum(
        (count / n) * math.log((count * n) / (left_counts[left_id] * right_counts[right_id]))
        for (left_id, right_id), count in joint_counts.items()
    )
    denominator = math.sqrt(left_entropy * right_entropy)
    normalized = mutual_information / denominator if denominator > 0.0 else 0.0
    return {
        "left_entropy": left_entropy,
        "right_entropy": right_entropy,
        "mutual_information": mutual_information,
        "normalized_mutual_information": normalized,
        "joint_cells": len(joint_counts),
    }


def run_lengths(assignments: Sequence[int]) -> List[int]:
    lengths: List[int] = []
    previous: int | None = None
    for assignment in assignments:
        if assignment != previous:
            lengths.append(1)
            previous = assignment
        else:
            lengths[-1] += 1
    return lengths


def contiguous_assignments(lengths: Sequence[int]) -> List[int]:
    return [bin_id for bin_id, length in enumerate(lengths) for _ in range(length)]


def size_order_null(
    clock_assignments: Sequence[int],
    seed: int,
) -> List[int]:
    lengths = run_lengths(clock_assignments)
    random.Random(seed).shuffle(lengths)
    assignments = contiguous_assignments(lengths)
    if len(assignments) != len(clock_assignments):
        raise AssertionError("size/order null changed event coverage")
    return assignments


def edge_phi(
    clock_assignments: Sequence[int],
    depth_assignments: Sequence[int],
    edges: Sequence[Tuple[int, int]],
) -> float:
    n11 = n10 = n01 = n00 = 0
    for parent, child in edges:
        clock_internal = clock_assignments[parent] == clock_assignments[child]
        depth_internal = depth_assignments[parent] == depth_assignments[child]
        if clock_internal and depth_internal:
            n11 += 1
        elif clock_internal:
            n10 += 1
        elif depth_internal:
            n01 += 1
        else:
            n00 += 1
    denominator = math.sqrt((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00))
    return (n11 * n00 - n10 * n01) / denominator if denominator else 0.0


def edge_internal_fraction(
    assignments: Sequence[int],
    edges: Sequence[Tuple[int, int]],
) -> float:
    return mean(assignments[parent] == assignments[child] for parent, child in edges) if edges else 0.0


def assignments_from_membership(
    rows: Sequence[Mapping[str, str]],
    event_count: int,
    assignment_field: str,
) -> List[int]:
    assignments: Dict[int, int] = {}
    for row in rows:
        event_id = int(row["event_id"])
        if event_id in assignments:
            raise ValueError("duplicate membership event")
        assignments[event_id] = int(row[assignment_field])
    if set(assignments) != set(range(event_count)):
        raise ValueError("membership does not cover every event")
    return [assignments[event_id] for event_id in range(event_count)]


def edge_pairs(rows: Sequence[Mapping[str, str]]) -> List[Tuple[int, int]]:
    return [(int(row["parent_event_id"]), int(row["child_event_id"])) for row in rows]


def relation_products(
    dts: Sequence[float],
    depth_assignments: Sequence[int],
    edges: Sequence[Tuple[int, int]],
    prefix: Mapping[str, Any],
    null_replicates: int,
    seed_tag: str,
    frozen_clock_assignments: Sequence[int] | None = None,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]]:
    bin_count = int(prefix["clock_bins"])
    clock = v16e.normalized_clock_bins(dts, bin_count)
    if frozen_clock_assignments is not None and list(frozen_clock_assignments) != clock:
        raise ValueError("frozen v16e clock membership does not match regenerated clock map")
    event_count = v16e.event_count_bins(len(dts), bin_count)
    observed = partition_information(clock, depth_assignments)
    count_relation = partition_information(event_count, depth_assignments)
    observed_phi = edge_phi(clock, depth_assignments, edges)
    count_phi = edge_phi(event_count, depth_assignments, edges)
    null_rows: List[Dict[str, Any]] = []
    waiting_nmi: List[float] = []
    waiting_phi: List[float] = []
    size_nmi: List[float] = []
    size_phi: List[float] = []
    seed_parts = tuple(prefix[field] for field in ("stage", "growth_seed", "run_offset", "arm", "run_seed", "clock_bins"))
    for null_index in range(null_replicates):
        waiting_seed = stable_seed(seed_tag, "waiting_time", *seed_parts, null_index)
        waiting = v16e.shuffled_clock_bins(dts, bin_count, waiting_seed)
        waiting_relation = partition_information(waiting, depth_assignments)
        waiting_edge_phi = edge_phi(waiting, depth_assignments, edges)
        waiting_nmi.append(waiting_relation["normalized_mutual_information"])
        waiting_phi.append(waiting_edge_phi)
        null_rows.append({
            **prefix,
            "null_family": "shuffled_waiting_time",
            "null_index": null_index,
            "null_seed": waiting_seed,
            "normalized_mutual_information": waiting_relation["normalized_mutual_information"],
            "edge_internalization_phi": waiting_edge_phi,
            "occupied_clock_bins": len(set(waiting)),
        })

        size_seed = stable_seed(seed_tag, "size_order", *seed_parts, null_index)
        size_order = size_order_null(clock, size_seed)
        size_relation = partition_information(size_order, depth_assignments)
        size_edge_phi = edge_phi(size_order, depth_assignments, edges)
        size_nmi.append(size_relation["normalized_mutual_information"])
        size_phi.append(size_edge_phi)
        null_rows.append({
            **prefix,
            "null_family": "size_order_matched",
            "null_index": null_index,
            "null_seed": size_seed,
            "normalized_mutual_information": size_relation["normalized_mutual_information"],
            "edge_internalization_phi": size_edge_phi,
            "occupied_clock_bins": len(set(size_order)),
        })

    waiting_sd = sample_sd(waiting_nmi)
    size_sd = sample_sd(size_nmi)
    summary = {
        **prefix,
        "event_count": len(dts),
        "fine_edges": len(edges),
        "occupied_clock_bins": len(set(clock)),
        "depth_components": len(set(depth_assignments)),
        "clock_entropy": observed["left_entropy"],
        "depth_entropy": observed["right_entropy"],
        "joint_cells": int(observed["joint_cells"]),
        "observed_nmi": observed["normalized_mutual_information"],
        "event_count_nmi": count_relation["normalized_mutual_information"],
        "waiting_null_mean_nmi": mean(waiting_nmi),
        "waiting_null_sd_nmi": waiting_sd,
        "size_order_null_mean_nmi": mean(size_nmi),
        "size_order_null_sd_nmi": size_sd,
        "nmi_minus_event_count": observed["normalized_mutual_information"] - count_relation["normalized_mutual_information"],
        "nmi_minus_waiting_null": observed["normalized_mutual_information"] - mean(waiting_nmi),
        "nmi_minus_size_order_null": observed["normalized_mutual_information"] - mean(size_nmi),
        "waiting_null_z": (observed["normalized_mutual_information"] - mean(waiting_nmi)) / waiting_sd if waiting_sd else 0.0,
        "size_order_null_z": (observed["normalized_mutual_information"] - mean(size_nmi)) / size_sd if size_sd else 0.0,
        "all_relative_deltas_negative": int(
            observed["normalized_mutual_information"] < count_relation["normalized_mutual_information"]
            and observed["normalized_mutual_information"] < mean(waiting_nmi)
            and observed["normalized_mutual_information"] < mean(size_nmi)
        ),
    }
    edge_diagnostic = {
        **prefix,
        "depth_internal_edge_fraction": edge_internal_fraction(depth_assignments, edges),
        "clock_internal_edge_fraction": edge_internal_fraction(clock, edges),
        "observed_edge_phi": observed_phi,
        "event_count_edge_phi": count_phi,
        "waiting_null_mean_edge_phi": mean(waiting_phi),
        "size_order_null_mean_edge_phi": mean(size_phi),
        "edge_phi_minus_event_count": observed_phi - count_phi,
        "edge_phi_minus_waiting_null": observed_phi - mean(waiting_phi),
        "edge_phi_minus_size_order_null": observed_phi - mean(size_phi),
        "diagnostic_only": 1,
    }
    return summary, null_rows, edge_diagnostic


def calibration_inputs(stage: str) -> Tuple[
    Dict[Tuple[str, ...], List[Dict[str, str]]],
    Dict[Tuple[str, ...], List[Dict[str, str]]],
    Dict[Tuple[str, ...], List[Dict[str, str]]],
]:
    return (
        group_rows(DOC / f"{stage}_event_log.csv"),
        group_rows(DOC / f"{stage}_fine_dependency_edges.csv"),
        group_rows(DOC / f"{stage}_coarse_membership.csv"),
    )


def design_audit() -> None:
    relation_rows: List[Dict[str, Any]] = []
    null_rows: List[Dict[str, Any]] = []
    for stage in CALIBRATION_STAGES:
        events_by_run, edges_by_run, memberships_by_run = calibration_inputs(stage)
        for key in sorted(events_by_run):
            events = sorted(events_by_run[key], key=lambda row: int(row["event_id"]))
            depth_rows = [row for row in memberships_by_run[key] if int(row["scale_window"]) == DEPTH_WINDOW]
            depth = assignments_from_membership(depth_rows, len(events), "coarse_event_id")
            edges = edge_pairs(edges_by_run[key])
            dts = [float(row["dt"]) for row in events]
            for clock_bins in SELECTED_CLOCK_BINS:
                prefix = {
                    "artifact_role": "v16f_old_data_design_calibration_not_analysis_holdout_evidence",
                    "stage": stage,
                    **numeric_prefix(key),
                    "depth_window": DEPTH_WINDOW,
                    "clock_bins": clock_bins,
                }
                relation, nulls, _ = relation_products(
                    dts, depth, edges, prefix, CALIBRATION_NULL_REPLICATES, "v16f-calibration"
                )
                relation_rows.append(relation)
                null_rows.extend(nulls)
    write_csv(CALIBRATION_RUNS, relation_rows)
    write_csv(CALIBRATION_NULLS, null_rows)
    for stage in CALIBRATION_STAGES:
        local = [row for row in relation_rows if row["stage"] == stage and row["arm"] == PRIMARY_ARM]
        for clock_bins in SELECTED_CLOCK_BINS:
            rows = [row for row in local if int(row["clock_bins"]) == clock_bins]
            print(
                f"[v16f-design] stage={stage} bins={clock_bins} runs={len(rows)} "
                f"d_wait={median(float(row['nmi_minus_waiting_null']) for row in rows):.6f} "
                f"d_size={median(float(row['nmi_minus_size_order_null']) for row in rows):.6f} "
                f"d_count={median(float(row['nmi_minus_event_count']) for row in rows):.6f}"
            )


def magnitude_ratio(numerator: float, denominator: float) -> float:
    return abs(numerator) / abs(denominator) if abs(denominator) > TOLERANCE else math.inf


def expected_selection_rows() -> List[Dict[str, Any]]:
    if not CALIBRATION_RUNS.exists() or not CALIBRATION_NULLS.exists():
        raise ValueError("missing v16f design calibration; run --design-audit first")
    calibration = read_csv(CALIBRATION_RUNS)
    rows: List[Dict[str, Any]] = []
    for clock_bins in SELECTED_CLOCK_BINS:
        by_stage: Dict[str, List[Dict[str, str]]] = {
            stage: [
                row for row in calibration
                if row["stage"] == stage
                and row["arm"] == PRIMARY_ARM
                and int(row["clock_bins"]) == clock_bins
            ]
            for stage in CALIBRATION_STAGES
        }
        if any(len(stage_rows) != 6 for stage_rows in by_stage.values()):
            raise ValueError(f"unexpected calibration coverage for bins={clock_bins}")
        aggregate: Dict[str, float] = {}
        for stage, stage_rows in by_stage.items():
            for field in (
                "nmi_minus_waiting_null",
                "nmi_minus_size_order_null",
                "nmi_minus_event_count",
                "waiting_null_z",
                "size_order_null_z",
            ):
                aggregate[f"{stage}_{field}"] = median(float(row[field]) for row in stage_rows)
            aggregate[f"{stage}_negative_fraction"] = mean(
                int(row["all_relative_deltas_negative"]) for row in stage_rows
            )
        rows.append({
            "artifact_role": "v16f_frozen_cross_map_design_not_analysis_holdout_evidence",
            "clock_bins": clock_bins,
            "depth_window": DEPTH_WINDOW,
            "primary_statistic": "normalized_mutual_information",
            "expected_direction": "clock_depth_nmi_lower_than_all_chronological_controls",
            **aggregate,
            "v16d_over_v16c_waiting_magnitude_ratio": magnitude_ratio(
                aggregate["v16d_nmi_minus_waiting_null"], aggregate["v16c_nmi_minus_waiting_null"]
            ),
            "v16d_over_v16c_size_magnitude_ratio": magnitude_ratio(
                aggregate["v16d_nmi_minus_size_order_null"], aggregate["v16c_nmi_minus_size_order_null"]
            ),
            "v16d_over_v16c_count_magnitude_ratio": magnitude_ratio(
                aggregate["v16d_nmi_minus_event_count"], aggregate["v16c_nmi_minus_event_count"]
            ),
            "max_median_nmi_delta": MAX_MEDIAN_NMI_DELTA,
            "max_median_null_z": MAX_MEDIAN_NULL_Z,
            "min_negative_run_fraction": MIN_NEGATIVE_RUN_FRACTION,
            "calibration_transfer_low": CALIBRATION_TRANSFER_RANGE[0],
            "calibration_transfer_high": CALIBRATION_TRANSFER_RANGE[1],
            "calibration_runs_sha256": v16c.file_sha256(CALIBRATION_RUNS),
            "calibration_nulls_sha256": v16c.file_sha256(CALIBRATION_NULLS),
        })
    return rows


def selection_row_passes(row: Mapping[str, Any]) -> bool:
    delta_fields = (
        "v16c_nmi_minus_waiting_null",
        "v16c_nmi_minus_size_order_null",
        "v16c_nmi_minus_event_count",
        "v16d_nmi_minus_waiting_null",
        "v16d_nmi_minus_size_order_null",
        "v16d_nmi_minus_event_count",
    )
    z_fields = (
        "v16c_waiting_null_z",
        "v16c_size_order_null_z",
        "v16d_waiting_null_z",
        "v16d_size_order_null_z",
    )
    fraction_fields = ("v16c_negative_fraction", "v16d_negative_fraction")
    ratio_fields = (
        "v16d_over_v16c_waiting_magnitude_ratio",
        "v16d_over_v16c_size_magnitude_ratio",
        "v16d_over_v16c_count_magnitude_ratio",
    )
    return (
        all(float(row[field]) <= MAX_MEDIAN_NMI_DELTA for field in delta_fields)
        and all(float(row[field]) <= MAX_MEDIAN_NULL_Z for field in z_fields)
        and all(float(row[field]) >= MIN_NEGATIVE_RUN_FRACTION for field in fraction_fields)
        and all(CALIBRATION_TRANSFER_RANGE[0] <= float(row[field]) <= CALIBRATION_TRANSFER_RANGE[1] for field in ratio_fields)
    )


def freeze_design() -> None:
    rows = expected_selection_rows()
    if not all(selection_row_passes(row) for row in rows):
        raise RuntimeError("v16f old-data calibration does not support the proposed frozen direction")
    write_csv(DESIGN_SELECTION, rows)
    print(
        f"[v16f] froze depth_window={DEPTH_WINDOW} clock_bins={SELECTED_CLOCK_BINS} "
        f"selection_sha256={v16c.file_sha256(DESIGN_SELECTION)}"
    )


def selection_verified() -> bool:
    if not DESIGN_SELECTION.exists():
        return False
    observed = read_csv(DESIGN_SELECTION)
    expected = expected_selection_rows()
    if len(observed) != len(expected):
        return False
    observed_by_bin = {int(row["clock_bins"]): row for row in observed}
    for expected_row in expected:
        observed_row = observed_by_bin.get(int(expected_row["clock_bins"]))
        if observed_row is None:
            return False
        for field, expected_value in expected_row.items():
            if field in {"artifact_role", "primary_statistic", "expected_direction", "calibration_runs_sha256", "calibration_nulls_sha256"}:
                if observed_row[field] != str(expected_value):
                    return False
            elif abs(float(observed_row[field]) - float(expected_value)) > TOLERANCE:
                return False
    return True


def source_contract_rows() -> Tuple[List[Dict[str, Any]], bool]:
    gate_rows = read_csv(DOC / "v16e_gate_evaluation.csv")
    overall = [row for row in gate_rows if row["gate"] == "v16e_overall"]
    subgates = [row for row in gate_rows if row["gate"] != "v16e_overall"]
    prereg_verified = True
    prereg_error = "verified"
    try:
        v16e.load_and_verify_preregistration()
    except (AssertionError, KeyError, RuntimeError, ValueError) as error:
        prereg_verified = False
        prereg_error = f"{type(error).__name__}:{error}"
    checks = [
        {
            "check": "v16e_overall",
            "observed": overall[0]["status"] if len(overall) == 1 else f"rows={len(overall)}",
            "required": "pass_to_v16f_cross_map_relation_gate",
            "status": "pass" if len(overall) == 1 and overall[0]["status"] == "pass_to_v16f_cross_map_relation_gate" else "fail",
        },
        {
            "check": "v16e_all_subgates",
            "observed": sum(row["status"] != "pass" for row in subgates),
            "required": 0,
            "status": "pass" if subgates and all(row["status"] == "pass" for row in subgates) else "fail",
        },
        {
            "check": "v16e_preregistration_reverified",
            "observed": prereg_error,
            "required": "verified",
            "status": "pass" if prereg_verified else "fail",
        },
        {
            "check": "v16f_design_selection",
            "observed": v16c.file_sha256(DESIGN_SELECTION) if DESIGN_SELECTION.exists() else "missing",
            "required": "verified old-data-only design",
            "status": "pass" if selection_verified() else "fail",
        },
    ]
    for name in (
        "v16e_event_log.csv",
        "v16e_fine_dependency_edges.csv",
        "v16e_primary_control_membership.csv",
        "v16e_run_summary.csv",
        "v16e_scheduler_effect_transfer.csv",
    ):
        path = DOC / name
        checks.append({
            "check": f"source_hash_{name}",
            "observed": v16c.file_sha256(path),
            "required": "frozen into v16f preregistration",
            "status": "pass",
        })
    return checks, all(row["status"] == "pass" for row in checks)


def source_hashes() -> Dict[str, str]:
    names = (
        "v16e_event_log.csv",
        "v16e_fine_dependency_edges.csv",
        "v16e_primary_control_membership.csv",
        "v16e_run_summary.csv",
        "v16e_scheduler_effect_transfer.csv",
        "v16e_gate_evaluation.csv",
        "v16e_pre_registration.csv",
    )
    return {name: v16c.file_sha256(DOC / name) for name in names}


def frozen_spec() -> Dict[str, Any]:
    return {
        "purpose_ref": "purpose://prompt.unknown",
        "analysis_role": "existing_v16e_histories_frozen_before_v16f_observable_computation",
        "source_hashes": source_hashes(),
        "source_script_sha256": v16c.file_sha256(Path("relational_universe_v16e_clock_slab_map_gate.py")),
        "design_selection_sha256": v16c.file_sha256(DESIGN_SELECTION),
        "depth_window": DEPTH_WINDOW,
        "clock_bins": list(SELECTED_CLOCK_BINS),
        "null_replicates": HOLDOUT_NULL_REPLICATES,
        "primary_arm": PRIMARY_ARM,
        "primary_statistic": "sqrt_entropy_normalized_mutual_information",
        "controls": [
            "equal_event_count_slabs",
            "shuffled_waiting_time_slabs",
            "monotone_slabs_preserving_exact_clock_bin_size_multiset",
        ],
        "expected_direction": "clock_depth_nmi_lower_than_all_chronological_controls",
        "secondary_diagnostic": "fine_dependency_edge_internalization_phi_not_gated",
        "thresholds": {
            "max_median_nmi_delta": MAX_MEDIAN_NMI_DELTA,
            "max_median_null_z": MAX_MEDIAN_NULL_Z,
            "min_negative_run_fraction": MIN_NEGATIVE_RUN_FRACTION,
            "holdout_calibration_range": list(HOLDOUT_CALIBRATION_RANGE),
            "growth_transfer_range": list(GROWTH_TRANSFER_RANGE),
            "scheduler_transfer_range": list(SCHEDULER_TRANSFER_RANGE),
        },
    }


def spec_digest() -> str:
    payload = json.dumps(frozen_spec(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def preregistration_rows() -> List[Dict[str, Any]]:
    source_rows = read_csv(DOC / "v16e_pre_registration.csv")
    digest = spec_digest()
    rows: List[Dict[str, Any]] = []
    for source in source_rows:
        rows.append({
            "purpose_ref": "purpose://prompt.unknown",
            "spec_digest": digest,
            "analysis_role": "frozen_existing_data_analysis_holdout_not_new_dynamics",
            "source_event_log_sha256": source_hashes()["v16e_event_log.csv"],
            "source_membership_sha256": source_hashes()["v16e_primary_control_membership.csv"],
            "design_selection_sha256": v16c.file_sha256(DESIGN_SELECTION),
            "growth_seed": int(source["growth_seed"]),
            "run_offset": int(source["run_offset"]),
            "arm": source["arm"],
            "run_seed": int(source["run_seed"]),
            "steps": int(source["steps"]),
            "depth_window": DEPTH_WINDOW,
            "clock_bins": ";".join(map(str, SELECTED_CLOCK_BINS)),
            "null_replicates_per_family": HOLDOUT_NULL_REPLICATES,
            "max_median_nmi_delta": MAX_MEDIAN_NMI_DELTA,
            "max_median_null_z": MAX_MEDIAN_NULL_Z,
            "min_negative_run_fraction": MIN_NEGATIVE_RUN_FRACTION,
            "prepared_before_v16e_cross_map_relation_computation": 1,
        })
    return rows


def prepare() -> None:
    source_rows, source_pass = source_contract_rows()
    if not source_pass:
        raise RuntimeError(f"v16f source contract failed: {source_rows}")
    rows = preregistration_rows()
    write_csv(PREREG, rows)
    print(f"[v16f] prepared rows={len(rows)} digest={rows[0]['spec_digest']}")


def load_and_verify_preregistration() -> Tuple[List[Dict[str, str]], List[Dict[str, Any]]]:
    if not PREREG.exists():
        raise ValueError("missing v16f preregistration; run --prepare-only first")
    source_rows, source_pass = source_contract_rows()
    if not source_pass:
        raise RuntimeError("v16f source contract no longer passes")
    observed = read_csv(PREREG)
    expected = preregistration_rows()
    if len(observed) != len(expected):
        raise ValueError("v16f preregistration row count changed")
    fields = tuple(expected[0])
    for observed_row, expected_row in zip(observed, expected):
        for field in fields:
            if observed_row[field] != str(expected_row[field]):
                raise ValueError(f"v16f preregistration changed field={field}")
    return observed, source_rows


def calibration_lookup() -> Dict[int, Dict[str, str]]:
    return {int(row["clock_bins"]): row for row in read_csv(DESIGN_SELECTION)}


def local_relation_rows(relation_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    calibration = calibration_lookup()
    rows: List[Dict[str, Any]] = []
    for clock_bins in SELECTED_CLOCK_BINS:
        subset = [
            row for row in relation_rows
            if row["arm"] == PRIMARY_ARM and int(row["clock_bins"]) == clock_bins
        ]
        if len(subset) != 6:
            raise ValueError("unexpected local holdout coverage")
        medians = {
            field: median(float(row[field]) for row in subset)
            for field in (
                "nmi_minus_waiting_null",
                "nmi_minus_size_order_null",
                "nmi_minus_event_count",
                "waiting_null_z",
                "size_order_null_z",
            )
        }
        baseline = calibration[clock_bins]
        ratios = {
            "waiting": magnitude_ratio(medians["nmi_minus_waiting_null"], float(baseline["v16d_nmi_minus_waiting_null"])),
            "size": magnitude_ratio(medians["nmi_minus_size_order_null"], float(baseline["v16d_nmi_minus_size_order_null"])),
            "count": magnitude_ratio(medians["nmi_minus_event_count"], float(baseline["v16d_nmi_minus_event_count"])),
        }
        negative_fraction = mean(int(row["all_relative_deltas_negative"]) for row in subset)
        passed = (
            all(medians[field] <= MAX_MEDIAN_NMI_DELTA for field in (
                "nmi_minus_waiting_null", "nmi_minus_size_order_null", "nmi_minus_event_count"
            ))
            and medians["waiting_null_z"] <= MAX_MEDIAN_NULL_Z
            and medians["size_order_null_z"] <= MAX_MEDIAN_NULL_Z
            and negative_fraction >= MIN_NEGATIVE_RUN_FRACTION
            and all(HOLDOUT_CALIBRATION_RANGE[0] <= ratio <= HOLDOUT_CALIBRATION_RANGE[1] for ratio in ratios.values())
        )
        rows.append({
            "clock_bins": clock_bins,
            "depth_window": DEPTH_WINDOW,
            "n_local_runs": len(subset),
            "median_nmi_minus_waiting_null": medians["nmi_minus_waiting_null"],
            "median_nmi_minus_size_order_null": medians["nmi_minus_size_order_null"],
            "median_nmi_minus_event_count": medians["nmi_minus_event_count"],
            "median_waiting_null_z": medians["waiting_null_z"],
            "median_size_order_null_z": medians["size_order_null_z"],
            "negative_run_fraction": negative_fraction,
            "holdout_over_v16d_waiting_magnitude_ratio": ratios["waiting"],
            "holdout_over_v16d_size_magnitude_ratio": ratios["size"],
            "holdout_over_v16d_count_magnitude_ratio": ratios["count"],
            "local_relation_pass": int(passed),
        })
    return rows


def transfer_rows(
    relation_rows: Sequence[Mapping[str, Any]],
    dimension: str,
    values: Sequence[str],
    ratio_range: Tuple[float, float],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    expected_coverage = 3 if dimension == "growth_seed" else 6
    for clock_bins in SELECTED_CLOCK_BINS:
        magnitudes: Dict[str, Dict[str, float]] = {}
        for value in values:
            subset = [
                row for row in relation_rows
                if int(row["clock_bins"]) == clock_bins
                and str(row[dimension]) == value
                and (dimension == "arm" or row["arm"] == PRIMARY_ARM)
            ]
            if len(subset) != expected_coverage:
                raise ValueError(f"unexpected {dimension} transfer coverage value={value}")
            magnitudes[value] = {
                control: abs(median(float(row[field]) for row in subset))
                for control, field in (
                    ("waiting", "nmi_minus_waiting_null"),
                    ("size", "nmi_minus_size_order_null"),
                    ("count", "nmi_minus_event_count"),
                )
            }
        ratios = {
            control: magnitudes[values[1]][control] / magnitudes[values[0]][control]
            if magnitudes[values[0]][control] > TOLERANCE else math.inf
            for control in ("waiting", "size", "count")
        }
        passed = all(ratio_range[0] <= ratio <= ratio_range[1] for ratio in ratios.values())
        rows.append({
            "clock_bins": clock_bins,
            "depth_window": DEPTH_WINDOW,
            "dimension": dimension,
            "first_value": values[0],
            "second_value": values[1],
            "first_waiting_abs_effect": magnitudes[values[0]]["waiting"],
            "second_waiting_abs_effect": magnitudes[values[1]]["waiting"],
            "waiting_magnitude_ratio": ratios["waiting"],
            "first_size_abs_effect": magnitudes[values[0]]["size"],
            "second_size_abs_effect": magnitudes[values[1]]["size"],
            "size_magnitude_ratio": ratios["size"],
            "first_count_abs_effect": magnitudes[values[0]]["count"],
            "second_count_abs_effect": magnitudes[values[1]]["count"],
            "count_magnitude_ratio": ratios["count"],
            "ratio_low": ratio_range[0],
            "ratio_high": ratio_range[1],
            "transfer_pass": int(passed),
        })
    return rows


def gate_evaluation(
    source_pass: bool,
    prereg_pass: bool,
    depth_audits: Sequence[Mapping[str, Any]],
    relation_rows: Sequence[Mapping[str, Any]],
    null_rows: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], str]:
    expected_runs = 12
    depth_pass = len(depth_audits) == expected_runs and all(int(row["map_integrity_pass"]) for row in depth_audits)
    relation_pass = len(relation_rows) == expected_runs * len(SELECTED_CLOCK_BINS)
    null_pass = len(null_rows) == expected_runs * len(SELECTED_CLOCK_BINS) * HOLDOUT_NULL_REPLICATES * 2
    local_pass = len(local_rows) == len(SELECTED_CLOCK_BINS) and all(int(row["local_relation_pass"]) for row in local_rows)
    growth_pass = len(growth_rows) == len(SELECTED_CLOCK_BINS) and all(int(row["transfer_pass"]) for row in growth_rows)
    scheduler_pass = len(scheduler_rows) == len(SELECTED_CLOCK_BINS) and all(int(row["transfer_pass"]) for row in scheduler_rows)
    exact = source_pass and prereg_pass and depth_pass and relation_pass and null_pass
    if exact and local_pass and growth_pass and scheduler_pass:
        overall = "pass_to_v16g_clock_depth_boundary_mechanism_gate"
    elif exact:
        positive = all(
            float(row["median_nmi_minus_waiting_null"]) > 0.0
            and float(row["median_nmi_minus_size_order_null"]) > 0.0
            and float(row["median_nmi_minus_event_count"]) > 0.0
            for row in local_rows
        )
        overall = "cross_map_direction_changed_requires_new_design" if positive else "cross_map_relation_not_supported_stop_scale_synthesis"
    else:
        overall = "v16f_instrumentation_failed"
    gates = [
        {"gate": "v16e_source_contract", "status": "pass" if source_pass else "fail", "observed": int(source_pass), "required": 1, "decision": "continue" if source_pass else "repair_source"},
        {"gate": "v16f_preregistration", "status": "pass" if prereg_pass else "fail", "observed": int(prereg_pass), "required": 1, "decision": "continue" if prereg_pass else "repair_preregistration"},
        {"gate": "depth16_map_integrity", "status": "pass" if depth_pass else "fail", "observed": f"passes={sum(int(row['map_integrity_pass']) for row in depth_audits)}/{len(depth_audits)}", "required": expected_runs, "decision": "continue" if depth_pass else "repair_depth_map"},
        {"gate": "relation_row_integrity", "status": "pass" if relation_pass else "fail", "observed": len(relation_rows), "required": expected_runs * len(SELECTED_CLOCK_BINS), "decision": "continue" if relation_pass else "repair_relation"},
        {"gate": "null_row_integrity", "status": "pass" if null_pass else "fail", "observed": len(null_rows), "required": expected_runs * len(SELECTED_CLOCK_BINS) * HOLDOUT_NULL_REPLICATES * 2, "decision": "continue" if null_pass else "repair_nulls"},
        {"gate": "local_relative_anti_alignment", "status": "pass" if local_pass else "fail", "observed": ";".join(f"{row['clock_bins']}:{float(row['median_nmi_minus_waiting_null']):.6f}/{float(row['median_nmi_minus_size_order_null']):.6f}/{float(row['median_nmi_minus_event_count']):.6f}" for row in local_rows), "required": f"all medians<={MAX_MEDIAN_NMI_DELTA};null_z<={MAX_MEDIAN_NULL_Z};negative>={MIN_NEGATIVE_RUN_FRACTION:.3f}", "decision": "continue" if local_pass else "do_not_merge_maps"},
        {"gate": "growth_relation_transfer", "status": "pass" if growth_pass else "fail", "observed": ";".join(f"{row['clock_bins']}:{float(row['waiting_magnitude_ratio']):.3f}/{float(row['size_magnitude_ratio']):.3f}/{float(row['count_magnitude_ratio']):.3f}" for row in growth_rows), "required": f"each in {GROWTH_TRANSFER_RANGE}", "decision": "continue" if growth_pass else "condition_on_base"},
        {"gate": "scheduler_relation_diagnostic", "status": "pass" if scheduler_pass else "fail", "observed": ";".join(f"{row['clock_bins']}:{float(row['waiting_magnitude_ratio']):.3f}/{float(row['size_magnitude_ratio']):.3f}/{float(row['count_magnitude_ratio']):.3f}" for row in scheduler_rows), "required": f"each in {SCHEDULER_TRANSFER_RANGE}", "decision": "continue" if scheduler_pass else "scheduler_conditioned"},
        {"gate": "v16f_overall", "status": overall, "observed": int(overall == "pass_to_v16g_clock_depth_boundary_mechanism_gate"), "required": 1, "decision": "test_boundary_mechanism" if overall == "pass_to_v16g_clock_depth_boundary_mechanism_gate" else "stop_or_redesign"},
    ]
    return gates, overall


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = []
        for field in fields:
            value = row[field]
            values.append(f"{value:.6f}" if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return lines


def claim_rows(overall: str) -> List[Dict[str, Any]]:
    exact = overall != "v16f_instrumentation_failed"
    signal = overall == "pass_to_v16g_clock_depth_boundary_mechanism_gate"
    return [
        {"claim_id": "C1", "statement": "The validated depth-window-16 map can be reconstructed on all frozen v16e histories with complete memberships and witnessed quotient edges.", "status": "supported" if exact else "not_supported", "evidence": "v16f_depth_map_audit.csv;v16f_depth_coarse_edges.csv", "scope_limit": "existing finite v16e histories under the declared support schema"},
        {"claim_id": "C2", "statement": "Clock/depth partition NMI is lower than equal-count, shuffled-waiting-time, and exact-size/order controls at all three frozen clock resolutions.", "status": "supported" if signal else "not_supported", "evidence": "v16f_local_relation_gate.csv;v16f_relation_run_summary.csv;v16f_relation_null_distribution.csv", "scope_limit": "analysis holdout on existing v16e histories, expected direction calibrated on v16c/v16d"},
        {"claim_id": "C3", "statement": "The relative anti-alignment transfers across two v16e growth seeds and the scheduler diagnostic within frozen broad bounds.", "status": "supported" if signal else "not_supported", "evidence": "v16f_growth_relation_transfer.csv;v16f_scheduler_relation_transfer.csv", "scope_limit": "two growth seeds, two scheduler arms, broad magnitude-ratio gates"},
        {"claim_id": "C4", "statement": "Clock slabs and causal-depth quotients are validated as two views of one common emergent geometry.", "status": "unsupported", "evidence": "none", "scope_limit": "v16f expected and tests relative anti-alignment rather than common-map equivalence"},
        {"claim_id": "C5", "statement": "The cross-map result establishes physical time, Lorentz symmetry, spacetime, or a continuum limit.", "status": "unsupported", "evidence": "none", "scope_limit": "simulation clock remains scheduler-order-dependent and no observer transformation or metric is tested"},
        {"claim_id": "C6", "statement": "The finite partition relation establishes particles, entanglement, or universal causal laws.", "status": "unsupported", "evidence": "none", "scope_limit": "not tested by v16f"},
    ]


def build_report(
    source_rows: Sequence[Mapping[str, Any]],
    relation_rows: Sequence[Mapping[str, Any]],
    edge_rows: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# UniverseSimulation v16f: clock/depth cross-map relation gate",
        "",
        "## Research question",
        "",
        "Are the independently validated simulation-clock and causal-depth partitions related beyond chronological, waiting-time, and exact-size/order controls?",
        "",
        "## Evidential separation",
        "",
        "- Design calibration: only old v16c/v16d histories determined the statistic, direction, controls, and thresholds.",
        "- Frozen-data analysis holdout: v16e histories existed before v16f, but their clock/depth NMI relation was not used to choose the v16f design.",
        "- Primary statistic: normalized mutual information between depth-window-16 components and clock bins 128/64/32.",
        "- Controls: equal event counts, shuffled waiting times, and monotone slabs preserving the exact clock-bin size multiset.",
        "- Secondary diagnostic: dependency-edge internalization phi; it is reported but does not gate the result.",
        "- Negative boundary: lower relative NMI is not negative mutual information and is not proof of incompatible physical geometries.",
        "",
        "## Execution hygiene",
        "",
        "The first holdout invocation completed all 36 relation calculations but stopped before artifact writing because the transfer helper incorrectly expected six primary runs per growth seed instead of the preregistered three offsets. Only that coverage assertion was made dimension-aware (three per growth seed, six per scheduler arm); source data, statistics, controls, seeds, thresholds, and expected direction were unchanged. The complete frozen analysis was then rerun.",
        "",
        "## Source contract",
        "",
    ]
    lines.extend(table(source_rows, ("check", "observed", "required", "status")))
    lines.extend(["", "## Run-level primary relation", ""])
    lines.extend(table(relation_rows, (
        "growth_seed", "run_offset", "arm", "clock_bins", "depth_components", "observed_nmi",
        "nmi_minus_waiting_null", "nmi_minus_size_order_null", "nmi_minus_event_count",
        "waiting_null_z", "size_order_null_z",
    )))
    lines.extend(["", "## Local primary gate", ""])
    lines.extend(table(local_rows, (
        "clock_bins", "median_nmi_minus_waiting_null", "median_nmi_minus_size_order_null",
        "median_nmi_minus_event_count", "median_waiting_null_z", "median_size_order_null_z",
        "negative_run_fraction", "local_relation_pass",
    )))
    lines.extend(["", "## Growth transfer", ""])
    lines.extend(table(growth_rows, (
        "clock_bins", "first_value", "second_value", "waiting_magnitude_ratio",
        "size_magnitude_ratio", "count_magnitude_ratio", "transfer_pass",
    )))
    lines.extend(["", "## Scheduler diagnostic", ""])
    lines.extend(table(scheduler_rows, (
        "clock_bins", "first_value", "second_value", "waiting_magnitude_ratio",
        "size_magnitude_ratio", "count_magnitude_ratio", "transfer_pass",
    )))
    lines.extend(["", "## Edge internalization diagnostic", ""])
    diagnostic_local = [row for row in edge_rows if row["arm"] == PRIMARY_ARM]
    lines.extend(table(diagnostic_local, (
        "growth_seed", "run_offset", "clock_bins", "depth_internal_edge_fraction",
        "clock_internal_edge_fraction", "observed_edge_phi", "edge_phi_minus_waiting_null",
        "edge_phi_minus_size_order_null", "diagnostic_only",
    )))
    lines.extend(["", "## Gate evaluation", ""])
    lines.extend(table(gate_rows, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        f"Overall status: `{overall}`.",
        "",
        "## Interpretation",
        "",
    ])
    if overall == "pass_to_v16g_clock_depth_boundary_mechanism_gate":
        lines.extend([
            "The actual simulation-clock partition is systematically less similar to the depth-window-16 partition than all three chronological controls. The direction survives the frozen v16c-to-v16d calibration transfer, the v16e analysis holdout, both v16e growth seeds, and the scheduler diagnostic.",
            "",
            "This is evidence for a repeatable relative cross-map relation, but it is evidence against immediately treating the two maps as interchangeable views of one common geometry. A scheduler/rate mechanism can produce the same pattern.",
        ])
    elif overall == "cross_map_relation_not_supported_stop_scale_synthesis":
        lines.append("The frozen relative relation did not survive the analysis holdout. Do not merge the maps or spend a larger scale budget on this synthesis.")
    elif overall == "cross_map_direction_changed_requires_new_design":
        lines.append("The frozen direction reversed. Treat that as a failed preregistered direction, not as post hoc evidence for common geometry.")
    else:
        lines.append("Instrumentation or source integrity failed; no cross-map interpretation is licensed.")
    lines.extend([
        "",
        "The NMI delta is not a Lorentz diagnostic and does not define a metric, observer transformation, light cone, proper time, or continuum.",
        "",
        "## Next decision",
        "",
        "If the frozen anti-alignment passes, preregister one v16g mechanism test asking whether event-family and local-rate conditioning explains where clock boundaries cut depth components. Do not add a third map or increase target size first.",
        "",
    ])
    return "\n".join(lines)


def verify_outputs() -> None:
    prereg_rows, _ = load_and_verify_preregistration()
    memberships = read_csv(DOC / "v16f_depth_membership.csv")
    coarse_edges = read_csv(DOC / "v16f_depth_coarse_edges.csv")
    audits = read_csv(DOC / "v16f_depth_map_audit.csv")
    relations = read_csv(DOC / "v16f_relation_run_summary.csv")
    nulls = read_csv(DOC / "v16f_relation_null_distribution.csv")
    edge_diagnostics = read_csv(DOC / "v16f_edge_agreement_diagnostic.csv")
    execution_audit = read_csv(DOC / "v16f_execution_audit.csv")
    gates = read_csv(DOC / "v16f_gate_evaluation.csv")
    expected_runs = len(prereg_rows)
    assert expected_runs == 12
    assert len(memberships) == expected_runs * 3072
    assert len(audits) == expected_runs and all(int(row["map_integrity_pass"]) == 1 for row in audits)
    assert len(relations) == expected_runs * len(SELECTED_CLOCK_BINS)
    assert len(edge_diagnostics) == len(relations)
    assert len(execution_audit) == 1
    assert int(execution_audit[0]["design_changed"]) == 0
    assert int(execution_audit[0]["source_data_changed"]) == 0
    assert len(nulls) == len(relations) * HOLDOUT_NULL_REPLICATES * 2
    assert {row["null_family"] for row in nulls} == {"shuffled_waiting_time", "size_order_matched"}
    members_by_run: Dict[Tuple[str, ...], List[Dict[str, str]]] = defaultdict(list)
    edges_by_run: Dict[Tuple[str, ...], List[Dict[str, str]]] = defaultdict(list)
    for row in memberships:
        members_by_run[run_key(row)].append(row)
    for row in coarse_edges:
        edges_by_run[run_key(row)].append(row)
    for row in audits:
        key = run_key(row)
        members = members_by_run[key]
        assert len(members) == 3072
        assert {int(item["event_id"]) for item in members} == set(range(3072))
        assert len(edges_by_run[key]) == int(row["quotient_edges"])
    overall = [row for row in gates if row["gate"] == "v16f_overall"]
    assert len(overall) == 1 and overall[0]["status"] in {
        "pass_to_v16g_clock_depth_boundary_mechanism_gate",
        "cross_map_relation_not_supported_stop_scale_synthesis",
        "cross_map_direction_changed_requires_new_design",
        "v16f_instrumentation_failed",
    }
    print(
        f"[v16f] output verification pass runs={expected_runs} memberships={len(memberships)} "
        f"coarse_edges={len(coarse_edges)} relations={len(relations)} nulls={len(nulls)} "
        f"overall={overall[0]['status']}"
    )


def run() -> None:
    prereg_rows, source_rows = load_and_verify_preregistration()
    events_by_run = group_rows(DOC / "v16e_event_log.csv")
    edges_by_run = group_rows(DOC / "v16e_fine_dependency_edges.csv")
    clock_by_run = group_rows(DOC / "v16e_primary_control_membership.csv")
    expected_keys = {run_key(row) for row in prereg_rows}
    if set(events_by_run) != expected_keys or set(edges_by_run) != expected_keys or set(clock_by_run) != expected_keys:
        raise ValueError("v16e source run keys do not match v16f preregistration")
    depth_memberships: List[Dict[str, Any]] = []
    depth_edges: List[Dict[str, Any]] = []
    depth_summaries: List[Dict[str, Any]] = []
    depth_audits: List[Dict[str, Any]] = []
    relation_rows: List[Dict[str, Any]] = []
    null_rows: List[Dict[str, Any]] = []
    edge_diagnostics: List[Dict[str, Any]] = []
    for index, prereg in enumerate(prereg_rows, start=1):
        key = run_key(prereg)
        prefix = numeric_prefix(key)
        events = sorted(events_by_run[key], key=lambda row: int(row["event_id"]))
        edge_source = edges_by_run[key]
        dag = v16e.dag_from_edge_rows(len(events), edge_source)
        memberships, coarse_edges, depth_summary, depth_audit = v16c.coarse_grain(
            dag, DEPTH_WINDOW, prefix
        )
        depth = assignments_from_membership(memberships, len(events), "coarse_event_id")
        edges = edge_pairs(edge_source)
        dts = [float(row["dt"]) for row in events]
        depth_memberships.extend(memberships)
        depth_edges.extend(coarse_edges)
        depth_summaries.append(depth_summary)
        depth_audits.append(depth_audit)
        clock_rows = clock_by_run[key]
        for clock_bins in SELECTED_CLOCK_BINS:
            frozen_rows = [
                row for row in clock_rows
                if row["map_kind"] == "clock" and int(row["requested_bins"]) == clock_bins
            ]
            frozen_clock = assignments_from_membership(frozen_rows, len(events), "source_bin")
            relation_prefix = {
                "stage": "v16e_analysis_holdout",
                **prefix,
                "depth_window": DEPTH_WINDOW,
                "clock_bins": clock_bins,
            }
            relation, nulls, edge_diagnostic = relation_products(
                dts,
                depth,
                edges,
                relation_prefix,
                HOLDOUT_NULL_REPLICATES,
                "v16f-analysis-holdout",
                frozen_clock,
            )
            relation_rows.append(relation)
            null_rows.extend(nulls)
            edge_diagnostics.append(edge_diagnostic)
        print(
            f"[v16f] runs={index}/{len(prereg_rows)} arm={prefix['arm']} "
            + " ".join(
                f"b{row['clock_bins']}={float(row['nmi_minus_waiting_null']):.6f}"
                for row in relation_rows[-len(SELECTED_CLOCK_BINS):]
            )
        )
    local_rows = local_relation_rows(relation_rows)
    growth_values = tuple(str(seed) for seed in sorted({int(row["growth_seed"]) for row in relation_rows}))
    growth_rows = transfer_rows(relation_rows, "growth_seed", growth_values, GROWTH_TRANSFER_RANGE)
    scheduler_rows = transfer_rows(relation_rows, "arm", ARMS, SCHEDULER_TRANSFER_RANGE)
    gates, overall = gate_evaluation(
        True, True, depth_audits, relation_rows, null_rows, local_rows, growth_rows, scheduler_rows
    )
    write_csv(DOC / "v16f_source_chain.csv", source_rows)
    write_csv(DOC / "v16f_depth_membership.csv", depth_memberships)
    write_csv(DOC / "v16f_depth_coarse_edges.csv", depth_edges)
    write_csv(DOC / "v16f_depth_map_summary.csv", depth_summaries)
    write_csv(DOC / "v16f_depth_map_audit.csv", depth_audits)
    write_csv(DOC / "v16f_relation_run_summary.csv", relation_rows)
    write_csv(DOC / "v16f_relation_null_distribution.csv", null_rows)
    write_csv(DOC / "v16f_edge_agreement_diagnostic.csv", edge_diagnostics)
    write_csv(DOC / "v16f_execution_audit.csv", [{
        "event": "pre_output_transfer_coverage_assertion_repair",
        "observed": "growth_seed_transfer_expected_6_primary_runs_but_preregistered_design_has_3_offsets_per_seed",
        "change": "dimension_aware_expected_coverage_growth_seed_3_scheduler_arm_6",
        "design_changed": 0,
        "source_data_changed": 0,
        "statistics_or_thresholds_changed": 0,
        "holdout_recomputed_after_repair": 1,
    }])
    write_csv(DOC / "v16f_local_relation_gate.csv", local_rows)
    write_csv(DOC / "v16f_growth_relation_transfer.csv", growth_rows)
    write_csv(DOC / "v16f_scheduler_relation_transfer.csv", scheduler_rows)
    write_csv(DOC / "v16f_gate_evaluation.csv", gates)
    write_csv(DOC / "v16f_claim_ledger.csv", claim_rows(overall))
    report = build_report(source_rows, relation_rows, edge_diagnostics, local_rows, growth_rows, scheduler_rows, gates, overall)
    (DOC / "v16f_cross_map_relation_gate.md").write_text(report, encoding="utf-8")
    recommendation = "\n".join([
        "# Operativ anbefaling v0.16f",
        "",
        f"Status: `{overall}`.",
        "",
        "- Ikke slaa sammen clock- og depth-kartene til en felles geometri paa grunnlag av v16f.",
        "- Ved full pass: test om event-family og lokal rate forklarer hvor clock-grenser kutter depth-komponenter.",
        "- Ikke legg til et tredje kart eller oek target foer mekanismen er testet.",
        "- Behold edge-internaliserings-phi som diagnostikk; den var ikke primary og skal ikke oppgraderes post hoc.",
        "- Ikke presenter simulation clock som proper time eller resultatet som Lorentz-, spacetime- eller continuum-evidens.",
        "",
    ])
    (DOC / "v0_16f_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    lay = "\n".join([
        "# v0.16f for ikke-spesialister",
        "",
        "Vi sammenlignet to maater aa gruppere de samme hendelsene paa: etter simulert klokketid og etter kausal avhengighetsdybde. Deretter sammenlignet vi med kontroller som beholdt rekkefolge, ventetider eller gruppestorrelser.",
        "",
        f"Statusen er `{overall}`. En stabil forskjell betyr at kartene har en repeterbar relasjon, men ikke at de er to koordinatsystemer for den samme fysiske romtiden.",
        "",
    ])
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16f.md").write_text(lay, encoding="utf-8")
    print(
        f"[v16f] overall={overall} runs={len(prereg_rows)} depth_memberships={len(depth_memberships)} "
        f"relations={len(relation_rows)} nulls={len(null_rows)}"
    )


def self_test() -> None:
    left = [0, 0, 1, 1]
    identical = partition_information(left, left)
    assert abs(identical["normalized_mutual_information"] - 1.0) < TOLERANCE
    assert run_lengths([0, 0, 1, 2, 2]) == [2, 1, 2]
    null = size_order_null([0, 0, 1, 2, 2], 7)
    assert sorted(run_lengths(null)) == [1, 2, 2]
    edges = [(0, 1), (1, 2), (2, 3)]
    assert -1.0 <= edge_phi(left, left, edges) <= 1.0
    print("[v16f] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16f clock/depth cross-map relation gate")
    parser.add_argument("--design-audit", action="store_true")
    parser.add_argument("--freeze-design", action="store_true")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    modes = sum((args.design_audit, args.freeze_design, args.prepare_only, args.self_test, args.verify_only))
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
