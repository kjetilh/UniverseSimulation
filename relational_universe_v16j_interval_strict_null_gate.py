#!/usr/bin/env python3
"""v16j: test v16i causal-interval abundance against a stricter structural null.

The observable is unchanged from v16i.  The new null uses directed double-edge
swaps and preserves scheduler order, the exact in/out-degree sequences, the
exact causal-depth sequence, and the global dyadic parent-age-bin histogram.
Calibration uses v16c/v16d only; v16h strict-null values are computed only after
the design and source hashes have been frozen by ``--prepare-only``.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import random
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
PURPOSE_REF = "purpose://universe-simulation/causal-interval-strict-null/v16j"
CALIBRATION_STAGES = ("v16c", "v16d")
HOLDOUT_STAGE = "v16h"
PRIMARY_ARM = v16i.PRIMARY_ARM
NULL_FAMILY = "degree_depth_global_age_bin_double_edge_swap"
NULL_REPLICATES = 32
TARGET_ACCEPTED_SWAPS_PER_EDGE = 0.075
MAX_ATTEMPTS_PER_EDGE = 60
MIN_CHANGED_EDGE_FRACTION = 0.10
MIN_UNIQUE_NULL_FRACTION = 1.0
EPSILON = v16i.EPSILON

MIN_LOCAL_MEDIAN_EFFECT_RATIO = 2.0
MIN_LOCAL_POSITIVE_FRACTION = 5.0 / 6.0
MAX_EMPIRICAL_P = 0.10
MIN_LOCAL_P_LE_010_FRACTION = 0.50
GROUP_MIN_MEDIAN_EFFECT_RATIO = 1.0
GROUP_MIN_POSITIVE_FRACTION = 5.0 / 6.0
CALIBRATION_TRANSFER_RANGE = (0.5, 2.0)

CALIBRATION_RUNS = DOC / "v16j_design_calibration_strict_null_runs.csv"
CALIBRATION_NULLS = DOC / "v16j_design_calibration_strict_null_distribution.csv"
CALIBRATION_AUDIT = DOC / "v16j_design_calibration_strict_null_integrity.csv"
DESIGN_SELECTION = DOC / "v16j_design_selection.csv"
FROZEN_BASELINE = DOC / "v16j_frozen_v16d_strict_null_baseline.csv"
PRE_REGISTRATION = DOC / "v16j_pre_registration.csv"
SOURCE_CHAIN = DOC / "v16j_source_chain.csv"

RUN_SUMMARY = DOC / "v16j_strict_null_run_summary.csv"
NULL_DISTRIBUTION = DOC / "v16j_strict_null_distribution.csv"
NULL_AUDIT = DOC / "v16j_strict_null_integrity_audit.csv"
LOCAL_GATE = DOC / "v16j_local_strict_null_gate.csv"
CALIBRATION_TRANSFER = DOC / "v16j_calibration_transfer.csv"
GROWTH_TRANSFER = DOC / "v16j_growth_transfer.csv"
SCHEDULER_TRANSFER = DOC / "v16j_scheduler_transfer.csv"
GATE_EVALUATION = DOC / "v16j_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16j_claim_ledger.csv"
REPORT = DOC / "v16j_interval_strict_null_gate.md"
RECOMMENDATION = DOC / "v0_16j_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16j.md"


def lag_bin(parent: int, child: int) -> int:
    lag = child - parent
    if lag <= 0:
        raise ValueError("parent age requires parent < child")
    return lag.bit_length() - 1


def outdegrees(predecessors: Sequence[Sequence[int]]) -> Tuple[int, ...]:
    values = [0] * len(predecessors)
    for parents in predecessors:
        for parent in parents:
            values[parent] += 1
    return tuple(values)


def global_age_signature(predecessors: Sequence[Sequence[int]]) -> Tuple[Tuple[int, int], ...]:
    counts = Counter(
        lag_bin(parent, child)
        for child, parents in enumerate(predecessors)
        for parent in parents
    )
    return tuple(sorted(counts.items()))


def edge_digest(predecessors: Sequence[Sequence[int]]) -> str:
    payload = ";".join(
        f"{parent}>{child}"
        for child, parents in enumerate(predecessors)
        for parent in parents
    )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def strict_rewire(
    dag: v16i.RunDAG,
    seed: int,
    *,
    target_swap_multiplier: float = TARGET_ACCEPTED_SWAPS_PER_EDGE,
) -> Tuple[Tuple[Tuple[int, ...], ...], Dict[str, Any]]:
    rng = random.Random(seed)
    original = tuple(tuple(parents) for parents in dag.predecessors)
    predecessors: List[Set[int]] = [set(parents) for parents in original]
    edges: List[Tuple[int, int]] = [
        (parent, child)
        for child, parents in enumerate(original)
        for parent in parents
    ]
    edge_set = set(edges)
    original_edges = set(edges)
    edge_count = len(edges)
    target_swaps = max(1, math.ceil(edge_count * target_swap_multiplier))
    max_attempts = max(target_swaps, edge_count * MAX_ATTEMPTS_PER_EDGE)
    attempts = 0
    accepted = 0

    while attempts < max_attempts:
        attempts += 1
        first_index = rng.randrange(edge_count)
        second_index = rng.randrange(edge_count - 1)
        if second_index >= first_index:
            second_index += 1
        parent_a, child_b = edges[first_index]
        parent_c, child_d = edges[second_index]
        if parent_a == parent_c or child_b == child_d:
            continue

        new_first = (parent_a, child_d)
        new_second = (parent_c, child_b)
        if parent_a >= child_d or parent_c >= child_b:
            continue
        if new_first in edge_set or new_second in edge_set or new_first == new_second:
            continue

        # The pair swap retains the exact global dyadic parent-age histogram.
        old_age_bins = sorted((lag_bin(parent_a, child_b), lag_bin(parent_c, child_d)))
        new_age_bins = sorted((lag_bin(parent_a, child_d), lag_bin(parent_c, child_b)))
        if new_age_bins != old_age_bins:
            continue

        # Keeping max(parent depth) == child depth - 1 for every changed child
        # is sufficient to keep the full recursively defined depth sequence.
        next_b = (predecessors[child_b] - {parent_a}) | {parent_c}
        next_d = (predecessors[child_d] - {parent_c}) | {parent_a}
        if not next_b or not next_d:
            continue
        if max(dag.depths[parent] for parent in next_b) != dag.depths[child_b] - 1:
            continue
        if max(dag.depths[parent] for parent in next_d) != dag.depths[child_d] - 1:
            continue

        edge_set.remove((parent_a, child_b))
        edge_set.remove((parent_c, child_d))
        edge_set.add(new_first)
        edge_set.add(new_second)
        edges[first_index] = new_first
        edges[second_index] = new_second
        predecessors[child_b] = next_b
        predecessors[child_d] = next_d
        accepted += 1

        if accepted >= target_swaps:
            changed_now = edge_count - len(original_edges & edge_set)
            if changed_now / edge_count >= MIN_CHANGED_EDGE_FRACTION:
                break

    rewired = tuple(tuple(sorted(parents)) for parents in predecessors)
    recomputed_depths = tuple(v16i.recompute_depths(rewired))
    changed_edges = edge_count - len(original_edges & edge_set)
    changed_fraction = changed_edges / edge_count
    indegree_pass = tuple(len(parents) for parents in rewired) == dag.indegrees
    outdegree_pass = outdegrees(rewired) == outdegrees(original)
    depth_pass = recomputed_depths == dag.depths
    order_pass = all(parent < child for child, parents in enumerate(rewired) for parent in parents)
    age_pass = global_age_signature(rewired) == global_age_signature(original)
    edge_count_pass = sum(len(parents) for parents in rewired) == edge_count
    mixing_pass = accepted >= target_swaps and changed_fraction >= MIN_CHANGED_EDGE_FRACTION
    structure_pass = all((indegree_pass, outdegree_pass, depth_pass, order_pass, age_pass, edge_count_pass))
    return rewired, {
        "edge_count": edge_count,
        "target_accepted_swaps": target_swaps,
        "accepted_swaps": accepted,
        "attempted_swaps": attempts,
        "acceptance_rate": accepted / attempts if attempts else 0.0,
        "changed_edge_count": changed_edges,
        "changed_edge_fraction": changed_fraction,
        "edge_count_pass": int(edge_count_pass),
        "scheduler_order_pass": int(order_pass),
        "indegree_sequence_pass": int(indegree_pass),
        "outdegree_sequence_pass": int(outdegree_pass),
        "depth_sequence_pass": int(depth_pass),
        "global_age_bin_histogram_pass": int(age_pass),
        "mixing_pass": int(mixing_pass),
        "structure_pass": int(structure_pass),
        "null_edge_sha256": edge_digest(rewired),
    }


def spec_payload() -> Dict[str, Any]:
    return {
        "purpose_ref": PURPOSE_REF,
        "calibration_stages": list(CALIBRATION_STAGES),
        "holdout_stage": HOLDOUT_STAGE,
        "primary_arm": PRIMARY_ARM,
        "observable": "v16i_dyadic_open_causal_interval_abundance_spectrum",
        "primary_metric": "full_spectrum_jensen_shannon_effect_ratio",
        "null_family": NULL_FAMILY,
        "null_preserves": [
            "event_count",
            "scheduler_order",
            "per_event_indegree",
            "per_event_outdegree",
            "per_event_causal_depth",
            "causal_depth_layer_profile",
            "global_dyadic_parent_age_bin_histogram",
        ],
        "null_does_not_preserve": [
            "exact_parent_age_per_edge",
            "per_child_parent_age_bin_multiset",
            "event_family",
            "read_write_resource_type",
        ],
        "null_replicates": NULL_REPLICATES,
        "target_accepted_swaps_per_edge": TARGET_ACCEPTED_SWAPS_PER_EDGE,
        "max_attempts_per_edge": MAX_ATTEMPTS_PER_EDGE,
        "min_changed_edge_fraction": MIN_CHANGED_EDGE_FRACTION,
        "min_unique_null_fraction": MIN_UNIQUE_NULL_FRACTION,
        "thresholds": {
            "min_local_median_effect_ratio": MIN_LOCAL_MEDIAN_EFFECT_RATIO,
            "min_local_positive_fraction": MIN_LOCAL_POSITIVE_FRACTION,
            "max_empirical_p": MAX_EMPIRICAL_P,
            "min_local_p_le_010_fraction": MIN_LOCAL_P_LE_010_FRACTION,
            "group_min_median_effect_ratio": GROUP_MIN_MEDIAN_EFFECT_RATIO,
            "group_min_positive_fraction": GROUP_MIN_POSITIVE_FRACTION,
            "calibration_transfer_range": list(CALIBRATION_TRANSFER_RANGE),
        },
    }


def spec_digest() -> str:
    payload = json.dumps(spec_payload(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def analyze_run(dag: v16i.RunDAG) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    observed = v16i.interval_spectrum(dag.predecessors)
    null_products: List[Dict[str, Any]] = []
    audits: List[Dict[str, Any]] = []
    for replicate in range(NULL_REPLICATES):
        seed = v16i.stable_seed("v16j", dag.stage, *dag.key, NULL_FAMILY, replicate)
        rewired, audit = strict_rewire(dag, seed)
        null_products.append(v16i.interval_spectrum(rewired))
        audits.append({
            **dag.prefix,
            "null_family": NULL_FAMILY,
            "null_replicate": replicate,
            "null_seed": seed,
            **audit,
        })

    unique_count = len({str(row["null_edge_sha256"]) for row in audits})
    unique_fraction = unique_count / NULL_REPLICATES
    uniqueness_pass = unique_fraction >= MIN_UNIQUE_NULL_FRACTION
    for row in audits:
        row["run_unique_null_count"] = unique_count
        row["run_unique_null_fraction"] = unique_fraction
        row["run_uniqueness_pass"] = int(uniqueness_pass)
        row["null_integrity_pass"] = int(
            int(row["structure_pass"]) == 1
            and int(row["mixing_pass"]) == 1
            and uniqueness_pass
        )

    null_spectra = [row["probabilities"] for row in null_products]
    null_center = v16i.mean_spectrum(null_spectra)
    observed_js = v16i.jensen_shannon(observed["probabilities"], null_center)
    null_self_js = [
        v16i.jensen_shannon(row, v16i.mean_spectrum(null_spectra, skip=index))
        for index, row in enumerate(null_spectra)
    ]
    null_median = v16i.median(null_self_js)
    ratio = observed_js / max(null_median, EPSILON)
    empirical_p = (1 + sum(value >= observed_js for value in null_self_js)) / (NULL_REPLICATES + 1)
    summary = {
        **dag.prefix,
        "n_events": len(dag.predecessors),
        "direct_edges": sum(dag.indegrees),
        "causal_depth": max(dag.depths) + 1,
        "comparable_pairs": observed["comparable_pairs"],
        "observed_js_to_null_center": observed_js,
        "null_median_leave_one_out_js": null_median,
        "js_effect_ratio": ratio,
        "empirical_p_upper": empirical_p,
        "effect_positive": int(ratio > 1.0),
        "p_le_010": int(empirical_p <= MAX_EMPIRICAL_P),
        "observed_mean_open_volume": observed["mean_open_volume"],
        "null_mean_open_volume": v16i.mean(row["mean_open_volume"] for row in null_products),
        "observed_tail_mass_ge_8": observed["tail_mass_ge_8"],
        "null_mean_tail_mass_ge_8": v16i.mean(row["tail_mass_ge_8"] for row in null_products),
        "tail_mass_ge_8_delta": observed["tail_mass_ge_8"] - v16i.mean(row["tail_mass_ge_8"] for row in null_products),
        "mean_acceptance_rate": v16i.mean(float(row["acceptance_rate"]) for row in audits),
        "min_changed_edge_fraction": min(float(row["changed_edge_fraction"]) for row in audits),
        "unique_null_fraction": unique_fraction,
        "all_null_integrity_pass": int(all(int(row["null_integrity_pass"]) for row in audits)),
    }
    null_rows = [{
        **dag.prefix,
        "null_family": NULL_FAMILY,
        "null_replicate": replicate,
        "null_seed": audits[replicate]["null_seed"],
        "null_edge_sha256": audits[replicate]["null_edge_sha256"],
        "comparable_pairs": product["comparable_pairs"],
        "leave_one_out_js": null_self_js[replicate],
        "mean_open_volume": product["mean_open_volume"],
        "tail_mass_ge_8": product["tail_mass_ge_8"],
        **{
            f"prob_{label}": product["probabilities"][index]
            for index, (label, _, _) in enumerate(v16i.INTERVAL_BINS)
        },
    } for replicate, product in enumerate(null_products)]
    return summary, null_rows, audits


def analyze_stage(stage: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    summaries: List[Dict[str, Any]] = []
    nulls: List[Dict[str, Any]] = []
    audits: List[Dict[str, Any]] = []
    dags = v16i.load_stage(stage)
    for index, dag in enumerate(dags, start=1):
        summary, run_nulls, run_audits = analyze_run(dag)
        summaries.append(summary)
        nulls.extend(run_nulls)
        audits.extend(run_audits)
        print(
            f"[v16j] stage={stage} runs={index}/{len(dags)} arm={dag.arm} "
            f"ratio={float(summary['js_effect_ratio']):.6f} "
            f"changed_min={float(summary['min_changed_edge_fraction']):.3f}"
        )
    return summaries, nulls, audits


def local_gate_row(rows: Sequence[Mapping[str, Any]], stage: str) -> Dict[str, Any]:
    subset = [row for row in rows if row["arm"] == PRIMARY_ARM]
    ratio = v16i.median(float(row["js_effect_ratio"]) for row in subset)
    positive = v16i.mean(float(row["effect_positive"]) for row in subset)
    significant = v16i.mean(float(row["p_le_010"]) for row in subset)
    passed = (
        len(subset) == 6
        and ratio >= MIN_LOCAL_MEDIAN_EFFECT_RATIO
        and positive >= MIN_LOCAL_POSITIVE_FRACTION
        and significant >= MIN_LOCAL_P_LE_010_FRACTION
    )
    return {
        "stage": stage,
        "target_nodes": subset[0]["target_nodes"],
        "primary_arm": PRIMARY_ARM,
        "n_runs": len(subset),
        "median_js_effect_ratio": ratio,
        "positive_fraction": positive,
        "p_le_010_fraction": significant,
        "min_median_effect_ratio": MIN_LOCAL_MEDIAN_EFFECT_RATIO,
        "min_positive_fraction": MIN_LOCAL_POSITIVE_FRACTION,
        "min_p_le_010_fraction": MIN_LOCAL_P_LE_010_FRACTION,
        "local_gate_pass": int(passed),
    }


def source_chain_rows() -> List[Dict[str, Any]]:
    rows = v16i.source_chain_rows()
    additions = [
        ("v16i", "implementation", Path(v16i.__file__)),
        ("v16i", "observable_audit", DOC / "v16i_event_poset_isomorphism_audit.csv"),
        ("v16i", "gate", DOC / "v16i_gate_evaluation.csv"),
    ]
    for stage, role, path in additions:
        rows.append({
            "stage": stage,
            "role": role,
            "artifact": path.name,
            "sha256": v16i.file_sha256(path),
            "source_status": "present",
            "expected_status": "present",
            "source_pass": 1,
        })
    return rows


def calibration_transfer_row(source_row: Mapping[str, Any], holdout_row: Mapping[str, Any]) -> Dict[str, Any]:
    source = float(source_row["median_js_effect_ratio"])
    holdout = float(holdout_row["median_js_effect_ratio"])
    ratio = holdout / max(source, EPSILON)
    return {
        "source_stage": "v16d",
        "holdout_stage": HOLDOUT_STAGE,
        "source_median_js_effect_ratio": source,
        "holdout_median_js_effect_ratio": holdout,
        "holdout_over_source_ratio": ratio,
        "ratio_low": CALIBRATION_TRANSFER_RANGE[0],
        "ratio_high": CALIBRATION_TRANSFER_RANGE[1],
        "calibration_transfer_pass": int(CALIBRATION_TRANSFER_RANGE[0] <= ratio <= CALIBRATION_TRANSFER_RANGE[1]),
    }


def prepare() -> None:
    summaries: List[Dict[str, Any]] = []
    nulls: List[Dict[str, Any]] = []
    audits: List[Dict[str, Any]] = []
    local_rows: List[Dict[str, Any]] = []
    for stage in CALIBRATION_STAGES:
        stage_summaries, stage_nulls, stage_audits = analyze_stage(stage)
        summaries.extend(stage_summaries)
        nulls.extend(stage_nulls)
        audits.extend(stage_audits)
        local_rows.append(local_gate_row(stage_summaries, stage))

    v16c_row = next(row for row in local_rows if row["stage"] == "v16c")
    v16d_row = next(row for row in local_rows if row["stage"] == "v16d")
    calibration_ratio = float(v16d_row["median_js_effect_ratio"]) / max(float(v16c_row["median_js_effect_ratio"]), EPSILON)
    instrumentation_pass = all(int(row["null_integrity_pass"]) for row in audits)
    calibration_signal_pass = all(int(row["local_gate_pass"]) for row in local_rows)
    v16i.write_csv(CALIBRATION_RUNS, summaries)
    v16i.write_csv(CALIBRATION_NULLS, nulls)
    v16i.write_csv(CALIBRATION_AUDIT, audits)
    v16i.write_csv(DESIGN_SELECTION, [{
        "candidate": "v16i_interval_abundance_under_degree_depth_child_age_bin_null",
        "primary_metric": "full_spectrum_jensen_shannon_effect_ratio",
        "null_family": NULL_FAMILY,
        "v16c_local_median_effect_ratio": v16c_row["median_js_effect_ratio"],
        "v16d_local_median_effect_ratio": v16d_row["median_js_effect_ratio"],
        "v16d_over_v16c_effect_ratio": calibration_ratio,
        "v16c_local_gate_pass": v16c_row["local_gate_pass"],
        "v16d_local_gate_pass": v16d_row["local_gate_pass"],
        "null_instrumentation_pass": int(instrumentation_pass),
        "calibration_signal_pass": int(calibration_signal_pass),
        "frozen_for_v16h_strict_null_holdout": int(instrumentation_pass),
    }])
    v16i.write_csv(FROZEN_BASELINE, [{
        "source_stage": "v16d",
        "source_target_nodes": v16d_row["target_nodes"],
        "source_primary_arm": PRIMARY_ARM,
        "source_n_runs": v16d_row["n_runs"],
        "source_median_js_effect_ratio": v16d_row["median_js_effect_ratio"],
        "source_positive_fraction": v16d_row["positive_fraction"],
        "source_p_le_010_fraction": v16d_row["p_le_010_fraction"],
        "holdout_ratio_low": CALIBRATION_TRANSFER_RANGE[0],
        "holdout_ratio_high": CALIBRATION_TRANSFER_RANGE[1],
    }])
    sources = source_chain_rows()
    v16i.write_csv(SOURCE_CHAIN, sources)
    if not instrumentation_pass:
        raise RuntimeError("v16j strict null did not mix or preserve its declared structure on calibration")

    holdout_dags = v16i.load_stage(HOLDOUT_STAGE)
    prereg = [{
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "holdout_script_sha256": v16i.file_sha256(Path(__file__)),
        "v16i_implementation_sha256": v16i.file_sha256(Path(v16i.__file__)),
        "source_chain_sha256": v16i.file_sha256(SOURCE_CHAIN),
        "design_selection_sha256": v16i.file_sha256(DESIGN_SELECTION),
        "frozen_baseline_sha256": v16i.file_sha256(FROZEN_BASELINE),
        "holdout_stage": HOLDOUT_STAGE,
        "target_nodes": dag.target_nodes,
        "growth_seed": dag.growth_seed,
        "run_offset": dag.run_offset,
        "arm": dag.arm,
        "run_seed": dag.run_seed,
        "n_events": len(dag.predecessors),
        "null_family": NULL_FAMILY,
        "null_replicates": NULL_REPLICATES,
        "min_changed_edge_fraction": MIN_CHANGED_EDGE_FRACTION,
        "min_local_median_effect_ratio": MIN_LOCAL_MEDIAN_EFFECT_RATIO,
        "min_local_positive_fraction": MIN_LOCAL_POSITIVE_FRACTION,
        "max_empirical_p": MAX_EMPIRICAL_P,
        "min_local_p_le_010_fraction": MIN_LOCAL_P_LE_010_FRACTION,
        "strict_null_values_computed_after_freeze": 1,
    } for dag in holdout_dags]
    v16i.write_csv(PRE_REGISTRATION, prereg)
    print(
        f"[v16j] prepared runs={len(prereg)} digest={spec_digest()} "
        f"calibration_signal={int(calibration_signal_pass)} ratio={calibration_ratio:.6f}"
    )


def load_and_verify_preregistration() -> List[v16i.RunDAG]:
    prereg = v16i.read_csv(PRE_REGISTRATION)
    if len(prereg) != 12:
        raise ValueError("v16j preregistration must contain 12 assignments")
    expected_sets = {
        "spec_digest": spec_digest(),
        "holdout_script_sha256": v16i.file_sha256(Path(__file__)),
        "v16i_implementation_sha256": v16i.file_sha256(Path(v16i.__file__)),
        "source_chain_sha256": v16i.file_sha256(SOURCE_CHAIN),
        "design_selection_sha256": v16i.file_sha256(DESIGN_SELECTION),
        "frozen_baseline_sha256": v16i.file_sha256(FROZEN_BASELINE),
    }
    for field, expected in expected_sets.items():
        if {row[field] for row in prereg} != {expected}:
            raise ValueError(f"v16j preregistration hash mismatch: {field}")
    observed_sources = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current_sources = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if observed_sources != current_sources:
        raise ValueError("v16j source chain changed after freeze")
    dags = v16i.load_stage(HOLDOUT_STAGE)
    expected_keys = {
        (int(row["growth_seed"]), int(row["run_offset"]), row["arm"], int(row["run_seed"]))
        for row in prereg
    }
    if {dag.key for dag in dags} != expected_keys:
        raise ValueError("v16j holdout assignments changed")
    return dags


def gate_rows(
    summaries: Sequence[Mapping[str, Any]],
    audits: Sequence[Mapping[str, Any]],
    local: Mapping[str, Any],
    transfer: Mapping[str, Any],
    growth: Sequence[Mapping[str, Any]],
    scheduler: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], str]:
    source_pass = v16i.source_status(HOLDOUT_STAGE) == v16i.STAGE_FILES[HOLDOUT_STAGE]["expected"]
    run_pass = len(summaries) == 12 and all(int(row["n_events"]) == 3072 for row in summaries)
    null_pass = len(audits) == 12 * NULL_REPLICATES and all(int(row["null_integrity_pass"]) for row in audits)
    local_pass = int(local["local_gate_pass"]) == 1
    transfer_pass = int(transfer["calibration_transfer_pass"]) == 1
    growth_pass = len(growth) == 2 and all(int(row["group_pass"]) for row in growth)
    scheduler_pass = len(scheduler) == 2 and all(int(row["group_pass"]) for row in scheduler)
    instrumentation = all((source_pass, run_pass, null_pass))
    evidence = all((local_pass, transfer_pass, growth_pass, scheduler_pass))
    if not instrumentation:
        overall = "v16j_strict_null_instrumentation_failed"
    elif evidence:
        overall = "causal_interval_abundance_supported_beyond_degree_age_null"
    else:
        overall = "causal_interval_abundance_not_supported_under_degree_age_null"
    rows = [
        {"gate": "v16h_source_contract", "status": "pass" if source_pass else "fail", "observed": int(source_pass), "required": 1, "decision": "continue" if source_pass else "stop"},
        {"gate": "holdout_run_integrity", "status": "pass" if run_pass else "fail", "observed": f"runs={len(summaries)};events={sum(int(row['n_events']) for row in summaries)}", "required": "runs=12;events=36864", "decision": "continue" if run_pass else "repair_input"},
        {"gate": "strict_null_integrity_and_mixing", "status": "pass" if null_pass else "fail", "observed": f"passes={sum(int(row['null_integrity_pass']) for row in audits)}/{len(audits)}", "required": f"{12 * NULL_REPLICATES}/{12 * NULL_REPLICATES}", "decision": "continue" if null_pass else "repair_null"},
        {"gate": "local_strict_null_interval_abundance", "status": "pass" if local_pass else "fail", "observed": f"median_ratio={float(local['median_js_effect_ratio']):.6f};positive={float(local['positive_fraction']):.6f};p_le_010={float(local['p_le_010_fraction']):.6f}", "required": f"median>={MIN_LOCAL_MEDIAN_EFFECT_RATIO};positive>={MIN_LOCAL_POSITIVE_FRACTION};p_le_010>={MIN_LOCAL_P_LE_010_FRACTION}", "decision": "continue" if local_pass else "retire_interval_mechanism_candidate"},
        {"gate": "v16d_to_v16h_strict_null_transfer", "status": "pass" if transfer_pass else "fail", "observed": transfer["holdout_over_source_ratio"], "required": f"in [{CALIBRATION_TRANSFER_RANGE[0]},{CALIBRATION_TRANSFER_RANGE[1]}]", "decision": "continue" if transfer_pass else "not_stable_across_seed_holdout"},
        {"gate": "growth_seed_transfer", "status": "pass" if growth_pass else "fail", "observed": f"passing_groups={sum(int(row['group_pass']) for row in growth)}/{len(growth)}", "required": "2/2", "decision": "continue" if growth_pass else "growth_sensitive"},
        {"gate": "scheduler_transfer", "status": "pass" if scheduler_pass else "fail", "observed": f"passing_groups={sum(int(row['group_pass']) for row in scheduler)}/{len(scheduler)}", "required": "2/2", "decision": "continue" if scheduler_pass else "scheduler_sensitive"},
        {"gate": "v16j_overall", "status": overall, "observed": f"instrumentation={int(instrumentation)};evidence={int(evidence)}", "required": "instrumentation=1;evidence=1", "decision": overall},
    ]
    return rows, overall


def claim_rows(overall: str) -> List[Dict[str, Any]]:
    supported = overall == "causal_interval_abundance_supported_beyond_degree_age_null"
    return [
        {"claim_id": "C1", "claim": "The v16j null preserves exact direct in/out-degree, exact causal depth, scheduler order, and the global dyadic parent-age-bin histogram.", "status": "supported", "evidence": "v16j_strict_null_integrity_audit.csv", "scope_limit": "finite event DAGs; parent ages are binned globally rather than fixed per child or edge"},
        {"claim_id": "C2", "claim": "The v16h causal-interval spectrum remains repeatably distinct under the stricter v16j null.", "status": "supported" if supported else "unsupported", "evidence": "v16j_strict_null_run_summary.csv;v16j_local_strict_null_gate.csv", "scope_limit": "one preregistered strict-null family on twelve existing histories"},
        {"claim_id": "C3", "claim": "The v16i interval signal cannot be explained by direct degree and coarse parent-age wiring.", "status": "supported" if supported else "unsupported", "evidence": "v16j_gate_evaluation.csv", "scope_limit": "does not control event family or read/write resource type"},
        {"claim_id": "C4", "claim": "The interval spectrum establishes dimension, manifoldlikeness, Lorentz symmetry, spacetime, or a continuum limit.", "status": "unsupported", "evidence": "none", "scope_limit": "this remains a finite-poset structural diagnostic"},
    ]


def build_report(
    summaries: Sequence[Mapping[str, Any]],
    local: Mapping[str, Any],
    transfer: Mapping[str, Any],
    growth: Sequence[Mapping[str, Any]],
    scheduler: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16j causal-interval strict-null gate",
        "",
        f"Status: `{overall}`.",
        "",
        "## Question and freeze discipline",
        "",
        "v16j asks whether the v16i causal-interval abundance signal survives a null that controls direct degree and coarse parent-age wiring. No new dynamics were generated. The null mechanics and unchanged v16i full-spectrum Jensen-Shannon statistic were calibrated on v16c/v16d, hash-frozen, and only then evaluated on v16h.",
        "",
        f"Specification digest: `{spec_digest()}`.",
        "",
        "## Strict null",
        "",
        "Directed double-edge swaps preserve event count, original scheduler order, every event's exact direct indegree and outdegree, every event's exact causal depth, the full depth-layer profile, and the global dyadic parent-age-bin histogram. Every replicate must accept swaps equal to at least 7.5% of the direct-edge count, change at least 10% of direct edges, and be unique within its run.",
        "",
        "The null does not preserve exact parent age per edge, each child's age-bin multiset, event family, or read/write resource type. It therefore tests a specific mechanism alternative rather than every generator artifact.",
        "",
        "## Holdout results",
        "",
    ]
    lines.extend(v16i.table(summaries, ("growth_seed", "run_offset", "arm", "observed_js_to_null_center", "null_median_leave_one_out_js", "js_effect_ratio", "empirical_p_upper", "min_changed_edge_fraction", "tail_mass_ge_8_delta")))
    lines.extend(["", "## Gates", ""])
    lines.extend(v16i.table([local], ("n_runs", "median_js_effect_ratio", "positive_fraction", "p_le_010_fraction", "local_gate_pass")))
    lines.append("")
    lines.extend(v16i.table([transfer], ("source_median_js_effect_ratio", "holdout_median_js_effect_ratio", "holdout_over_source_ratio", "calibration_transfer_pass")))
    lines.append("")
    lines.extend(v16i.table(growth, ("group_field", "group_value", "n_runs", "median_js_effect_ratio", "positive_fraction", "group_pass")))
    lines.append("")
    lines.extend(v16i.table(scheduler, ("group_field", "group_value", "n_runs", "median_js_effect_ratio", "positive_fraction", "group_pass")))
    lines.append("")
    lines.extend(v16i.table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "A pass would support finite-poset interval structure beyond this degree/depth/coarse-age null. A fail with valid mixing would show that the earlier v16i contrast is not robust to this stricter mechanism control and is consistent with degree/age wiring. Neither outcome proves or disproves that a universe can emerge from local rules.",
        "",
        "This gate does not establish dimension, manifoldlikeness, Lorentz invariance, physical time, particles, entanglement, continuum behavior, or universal geometry.",
        "",
    ])
    return "\n".join(lines)


def write_interpretation(overall: str, local: Mapping[str, Any]) -> None:
    if overall == "causal_interval_abundance_supported_beyond_degree_age_null":
        next_step = "Run one fresh-history replication of the strict-null interval gate before adding dimension-like estimators."
        plain = "Intervallstrukturen overlevde en streng kontroll av grad, dybde og grov foreldre-alder. Det er et robust strukturspor, men fortsatt ikke romtid."
    elif overall == "causal_interval_abundance_not_supported_under_degree_age_null":
        next_step = "Retire interval abundance as a geometry candidate; test event-family/resource-type mechanism attribution only if needed to explain the artifact."
        plain = "Intervallsignalet overlevde ikke den strengere kontrollen. Det betyr at det forelopig best forstas som grad-/alderskobling, ikke som ny geometri."
    else:
        next_step = "Repair null mixing or preservation before drawing any scientific conclusion."
        plain = "Kontrollmodellen blandet ikke grafene godt nok, sa runden kan ikke tolkes fysisk."
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.16j\n\n"
        f"Status: `{overall}`.\n\n"
        f"Primary-arm median effect ratio: `{float(local['median_js_effect_ratio']):.6f}`.\n\n"
        f"Next: {next_step}\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.16j\n\n"
        f"{plain}\n\n"
        "Testen bruker de samme hendelsesgrafene som forrige runde, men sammenligner med tilfeldige grafer som beholder langt mer av den lokale koblingsstrukturen. "
        "Resultatet gjelder bare denne avgrensede testen og sier ikke at partikler, romtid eller naturlover er funnet.\n",
        encoding="utf-8",
    )


def run() -> None:
    dags = load_and_verify_preregistration()
    summaries: List[Dict[str, Any]] = []
    nulls: List[Dict[str, Any]] = []
    audits: List[Dict[str, Any]] = []
    for index, dag in enumerate(dags, start=1):
        summary, run_nulls, run_audits = analyze_run(dag)
        summaries.append(summary)
        nulls.extend(run_nulls)
        audits.extend(run_audits)
        print(f"[v16j] holdout runs={index}/{len(dags)} arm={dag.arm} ratio={float(summary['js_effect_ratio']):.6f}")

    local = local_gate_row(summaries, HOLDOUT_STAGE)
    baseline = v16i.read_csv(FROZEN_BASELINE)
    if len(baseline) != 1:
        raise ValueError("v16j frozen baseline must contain one row")
    baseline_row = {
        "median_js_effect_ratio": baseline[0]["source_median_js_effect_ratio"],
    }
    transfer = calibration_transfer_row(baseline_row, local)
    growth = v16i.aggregate_rows(summaries, "growth_seed", GROUP_MIN_MEDIAN_EFFECT_RATIO, GROUP_MIN_POSITIVE_FRACTION)
    scheduler = v16i.aggregate_rows(summaries, "arm", GROUP_MIN_MEDIAN_EFFECT_RATIO, GROUP_MIN_POSITIVE_FRACTION)
    gates, overall = gate_rows(summaries, audits, local, transfer, growth, scheduler)
    v16i.write_csv(RUN_SUMMARY, summaries)
    v16i.write_csv(NULL_DISTRIBUTION, nulls)
    v16i.write_csv(NULL_AUDIT, audits)
    v16i.write_csv(LOCAL_GATE, [local])
    v16i.write_csv(CALIBRATION_TRANSFER, [transfer])
    v16i.write_csv(GROWTH_TRANSFER, growth)
    v16i.write_csv(SCHEDULER_TRANSFER, scheduler)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claim_rows(overall))
    REPORT.write_text(build_report(summaries, local, transfer, growth, scheduler, gates, overall), encoding="utf-8")
    write_interpretation(overall, local)
    print(f"[v16j] complete overall={overall}")


def verify_outputs() -> None:
    summaries = v16i.read_csv(RUN_SUMMARY)
    nulls = v16i.read_csv(NULL_DISTRIBUTION)
    audits = v16i.read_csv(NULL_AUDIT)
    gates = v16i.read_csv(GATE_EVALUATION)
    if len(summaries) != 12 or len(nulls) != 12 * NULL_REPLICATES or len(audits) != len(nulls):
        raise ValueError("v16j output row counts failed")
    if not all(int(row["null_integrity_pass"]) for row in audits):
        raise ValueError("v16j null integrity failed")
    if len({row["gate"] for row in gates}) != len(gates):
        raise ValueError("v16j duplicate gate rows")
    for row in (*summaries, *nulls, *audits):
        for value in row.values():
            if str(value).lower() in {"nan", "inf", "-inf"}:
                raise ValueError("v16j non-finite output")
    overall = next(row["status"] for row in gates if row["gate"] == "v16j_overall")
    if overall not in {
        "causal_interval_abundance_supported_beyond_degree_age_null",
        "causal_interval_abundance_not_supported_under_degree_age_null",
        "v16j_strict_null_instrumentation_failed",
    }:
        raise ValueError("v16j unknown overall status")
    print(f"[v16j] output verification pass overall={overall}")


def self_test() -> None:
    dag = v16i.load_stage("v16c")[0]
    rewired, audit = strict_rewire(dag, v16i.stable_seed("v16j", "self-test"), target_swap_multiplier=0.05)
    if not int(audit["structure_pass"]):
        raise AssertionError(audit)
    if tuple(v16i.recompute_depths(rewired)) != dag.depths:
        raise AssertionError("depth mismatch")
    if global_age_signature(rewired) != global_age_signature(dag.predecessors):
        raise AssertionError("global age-bin mismatch")
    if outdegrees(rewired) != outdegrees(dag.predecessors):
        raise AssertionError("outdegree mismatch")
    print("[v16j] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16j causal-interval strict-null gate")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if sum((args.prepare_only, args.self_test, args.verify_only)) > 1:
        parser.error("choose at most one mode")
    if args.prepare_only:
        prepare()
    elif args.self_test:
        self_test()
    elif args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
