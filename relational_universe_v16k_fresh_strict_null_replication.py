#!/usr/bin/env python3
"""v16k: fresh-history replication of the v16j interval-spectrum contrast.

The v16j observable and primary strict perturbation null are unchanged.  The
primary question is effect existence on fresh histories.  Magnitude is a
separate descriptive compatibility classification and cannot rescue or fail
the existence result.

This is a finite event-DAG test.  It does not establish dimension,
manifoldlikeness, Lorentz symmetry, spacetime, continuum behavior, particles,
entanglement, or a physical causal law.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import shutil
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v16a_disjoint_event_commutation_gate as v16a
import relational_universe_v16ac_local_seed_adapter_gate as v16ac
import relational_universe_v16h_fresh_rate_logged_mechanism_holdout as v16h
import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16j_interval_strict_null_gate as v16j


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

TARGET_NODES = v16h.TARGET_NODES
STEPS = v16h.STEPS
GROWTH_SEEDS = tuple(
    5000 + v16i.stable_seed("v16k", "fresh-growth", index) % 4000
    for index in range(2)
)
RUN_OFFSETS = tuple(
    90000 + v16i.stable_seed("v16k", "fresh-offset", index) % 9000
    for index in range(3)
)
ARMS = v16h.ARMS
PRIMARY_ARM = v16j.PRIMARY_ARM
EXCLUDED_TRANSIENT_GROWTH_SEEDS = (5203, 5389)

PRIMARY_NULL_REPLICATES = v16j.NULL_REPLICATES
LONGER_NULL_REPLICATES = 16
LONGER_TARGET_SWAP_MULTIPLIER = 0.10
LONGER_MIN_MEDIAN_EFFECT_RATIO = 1.0
LONGER_MIN_POSITIVE_FRACTION = 5.0 / 6.0
MIN_FREE_BYTES = 250 * 1024 * 1024
BOOTSTRAP_REPLICATES = 10_000
FACTOR_TWO_LOW = 0.5
FACTOR_TWO_HIGH = 2.0

SOURCE_CHAIN = DOC / "v16k_source_chain.csv"
FROZEN_BASELINES = DOC / "v16k_frozen_magnitude_baselines.csv"
PRE_REGISTRATION = DOC / "v16k_pre_registration.csv"
TARGET_SUMMARY = DOC / "v16k_target_summary.csv"
EVENT_LOG = DOC / "v16k_event_log.csv"
EDGE_LOG = DOC / "v16k_fine_dependency_edges.csv"
RUN_SUMMARY = DOC / "v16k_run_summary.csv"
REPLAY_AUDIT = DOC / "v16k_topological_replay_audit.csv"
RELABEL_AUDIT = DOC / "v16k_relabel_replay_audit.csv"
DIRECT_RATE_AUDIT = DOC / "v16k_direct_rate_audit.csv"
STRICT_RUNS = DOC / "v16k_strict_null_run_summary.csv"
STRICT_NULLS = DOC / "v16k_strict_null_distribution.csv"
STRICT_AUDIT = DOC / "v16k_strict_null_perturbation_integrity.csv"
EFFECT_GATE = DOC / "v16k_effect_existence_gate.csv"
GROWTH_ROBUSTNESS = DOC / "v16k_growth_robustness.csv"
SCHEDULER_ROBUSTNESS = DOC / "v16k_scheduler_robustness.csv"
LONGER_RUNS = DOC / "v16k_longer_perturbation_run_summary.csv"
LONGER_NULLS = DOC / "v16k_longer_perturbation_distribution.csv"
LONGER_AUDIT = DOC / "v16k_longer_perturbation_integrity.csv"
LONGER_GATE = DOC / "v16k_longer_perturbation_gate.csv"
MAGNITUDE = DOC / "v16k_magnitude_compatibility.csv"
GATE_EVALUATION = DOC / "v16k_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16k_claim_ledger.csv"
EXECUTION_AUDIT = DOC / "v16k_execution_audit.csv"
REPORT = DOC / "v16k_fresh_strict_null_replication.md"
RECOMMENDATION = DOC / "v0_16k_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16k.md"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def median(values: Iterable[float]) -> float:
    return v16i.median(values)


def mean(values: Iterable[float]) -> float:
    return v16i.mean(values)


def run_seed(growth_seed: int, run_offset: int, arm: str) -> int:
    return v16h.run_seed(growth_seed, run_offset, arm)


def assignments() -> List[Dict[str, Any]]:
    return [
        {
            "growth_seed": growth_seed,
            "run_offset": run_offset,
            "arm": arm,
            "run_seed": run_seed(growth_seed, run_offset, arm),
        }
        for growth_seed in GROWTH_SEEDS
        for run_offset in RUN_OFFSETS
        for arm in ARMS
    ]


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = [
        ("v16h", "fresh_dynamics_implementation", Path(v16h.__file__)),
        ("v16h", "source_gate", DOC / "v16h_gate_evaluation.csv"),
        ("v16i", "observable_implementation", Path(v16i.__file__)),
        ("v16j", "strict_null_implementation", Path(v16j.__file__)),
        ("v16j", "interpretation_audit", DOC / "v16j_interpretation_audit.csv"),
        ("v16j", "calibration_runs", DOC / "v16j_design_calibration_strict_null_runs.csv"),
        ("v16j", "holdout_runs", DOC / "v16j_strict_null_run_summary.csv"),
        ("v16j", "gate", DOC / "v16j_gate_evaluation.csv"),
    ]
    return [
        {
            "stage": stage,
            "role": role,
            "artifact": path.name,
            "sha256": file_sha256(path),
            "source_status": "present",
            "source_pass": 1,
        }
        for stage, role, path in paths
    ]


def frozen_baseline_rows() -> List[Dict[str, Any]]:
    calibration = v16i.read_csv(DOC / "v16j_design_calibration_strict_null_runs.csv")
    holdout = v16i.read_csv(DOC / "v16j_strict_null_run_summary.csv")
    v16d_values = [
        float(row["js_effect_ratio"])
        for row in calibration
        if row["stage"] == "v16d" and row["arm"] == PRIMARY_ARM
    ]
    v16h_values = [
        float(row["js_effect_ratio"])
        for row in holdout
        if row["stage"] == "v16h" and row["arm"] == PRIMARY_ARM
    ]
    if len(v16d_values) != 6 or len(v16h_values) != 6:
        raise ValueError("v16k requires six primary runs in each historical anchor")
    medians = {"v16d": median(v16d_values), "v16h": median(v16h_values)}
    return [
        {
            "source_stage": stage,
            "source_n_primary_runs": 6,
            "source_median_js_effect_ratio": value,
            "factor_two_low": value * FACTOR_TWO_LOW,
            "factor_two_high": value * FACTOR_TWO_HIGH,
            "source_artifact": (
                "v16j_design_calibration_strict_null_runs.csv"
                if stage == "v16d"
                else "v16j_strict_null_run_summary.csv"
            ),
            "frozen_before_formal_v16k_histories": 1,
        }
        for stage, value in medians.items()
    ]


def spec_payload() -> Dict[str, Any]:
    return {
        "gate": "v16k_fresh_strict_null_replication",
        "purpose_ref": PURPOSE_REF,
        "target_nodes": TARGET_NODES,
        "steps": STEPS,
        "growth_seeds": list(GROWTH_SEEDS),
        "run_offsets": list(RUN_OFFSETS),
        "arms": list(ARMS),
        "primary_arm": PRIMARY_ARM,
        "excluded_transient_growth_seeds": list(EXCLUDED_TRANSIENT_GROWTH_SEEDS),
        "observable": "v16i_dyadic_open_causal_interval_spectrum",
        "primary_metric": "full_spectrum_jensen_shannon_effect_ratio",
        "primary_null_family": v16j.NULL_FAMILY,
        "primary_null_replicates": PRIMARY_NULL_REPLICATES,
        "primary_target_swap_multiplier": v16j.TARGET_ACCEPTED_SWAPS_PER_EDGE,
        "longer_null_replicates": LONGER_NULL_REPLICATES,
        "longer_target_swap_multiplier": LONGER_TARGET_SWAP_MULTIPLIER,
        "effect_thresholds": {
            "min_local_median_effect_ratio": v16j.MIN_LOCAL_MEDIAN_EFFECT_RATIO,
            "min_local_positive_fraction": v16j.MIN_LOCAL_POSITIVE_FRACTION,
            "max_empirical_p": v16j.MAX_EMPIRICAL_P,
            "min_local_p_le_010_fraction": v16j.MIN_LOCAL_P_LE_010_FRACTION,
        },
        "longer_sensitivity_thresholds": {
            "min_median_effect_ratio": LONGER_MIN_MEDIAN_EFFECT_RATIO,
            "min_positive_fraction": LONGER_MIN_POSITIVE_FRACTION,
        },
        "magnitude_model": "four_way_descriptive_factor_two_anchor_compatibility",
        "bootstrap_replicates": BOOTSTRAP_REPLICATES,
        "no_early_success_stop": True,
        "scope": "fresh_finite_event_dag_replication",
    }


def spec_digest() -> str:
    raw = json.dumps(spec_payload(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def preregistration_rows() -> List[Dict[str, Any]]:
    if not SOURCE_CHAIN.exists() or not FROZEN_BASELINES.exists():
        raise ValueError("missing v16k frozen source products")
    return [
        {
            "purpose_ref": PURPOSE_REF,
            "spec_digest": spec_digest(),
            "script_sha256": file_sha256(SCRIPT),
            "v16h_sha256": file_sha256(Path(v16h.__file__)),
            "v16i_sha256": file_sha256(Path(v16i.__file__)),
            "v16j_sha256": file_sha256(Path(v16j.__file__)),
            "source_chain_sha256": file_sha256(SOURCE_CHAIN),
            "frozen_baselines_sha256": file_sha256(FROZEN_BASELINES),
            "target_nodes": TARGET_NODES,
            "steps": STEPS,
            **assignment,
            "primary_null_replicates": PRIMARY_NULL_REPLICATES,
            "primary_target_swap_multiplier": v16j.TARGET_ACCEPTED_SWAPS_PER_EDGE,
            "longer_null_replicates": LONGER_NULL_REPLICATES,
            "longer_target_swap_multiplier": LONGER_TARGET_SWAP_MULTIPLIER,
            "min_local_median_effect_ratio": v16j.MIN_LOCAL_MEDIAN_EFFECT_RATIO,
            "min_local_positive_fraction": v16j.MIN_LOCAL_POSITIVE_FRACTION,
            "min_local_p_le_010_fraction": v16j.MIN_LOCAL_P_LE_010_FRACTION,
            "formal_history_generated_after_freeze": 1,
        }
        for assignment in assignments()
    ]


def prepare() -> None:
    if set(GROWTH_SEEDS) & set(EXCLUDED_TRANSIENT_GROWTH_SEEDS):
        raise ValueError("formal seeds overlap quarantined transient adviser seeds")
    if shutil.disk_usage(ROOT).free < MIN_FREE_BYTES:
        raise RuntimeError("v16k preflight requires at least 250 MiB free")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(FROZEN_BASELINES, frozen_baseline_rows())
    rows = preregistration_rows()
    v16i.write_csv(PRE_REGISTRATION, rows)
    print(f"[v16k] prepared runs={len(rows)} digest={spec_digest()}")


def load_and_verify_preregistration() -> List[Dict[str, str]]:
    observed = v16i.read_csv(PRE_REGISTRATION)
    expected = [{key: str(value) for key, value in row.items()} for row in preregistration_rows()]
    if observed != expected:
        raise ValueError("v16k preregistration changed after freeze")
    frozen_sources = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current_sources = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen_sources != current_sources:
        raise ValueError("v16k source chain changed after freeze")
    if set(int(row["growth_seed"]) for row in observed) & set(EXCLUDED_TRANSIENT_GROWTH_SEEDS):
        raise ValueError("v16k preregistration contains quarantined transient seeds")
    return observed


def run_dag_from_history(
    assignment: Mapping[str, Any], event_rows: Sequence[Mapping[str, Any]], dependency_dag: Any,
) -> v16i.RunDAG:
    predecessors = tuple(
        tuple(sorted(dependency_dag.predecessors[event_id]))
        for event_id in range(STEPS)
    )
    depths = tuple(int(row["causal_depth"]) for row in event_rows)
    indegrees = tuple(len(parents) for parents in predecessors)
    if tuple(v16i.recompute_depths(predecessors)) != depths:
        raise RuntimeError("v16k in-memory depth reconstruction failed")
    return v16i.RunDAG(
        stage="v16k",
        target_nodes=TARGET_NODES,
        growth_seed=int(assignment["growth_seed"]),
        run_offset=int(assignment["run_offset"]),
        arm=str(assignment["arm"]),
        run_seed=int(assignment["run_seed"]),
        predecessors=predecessors,
        depths=depths,
        indegrees=indegrees,
    )


def analyze_perturbation_family(
    dag: v16i.RunDAG,
    *,
    label: str,
    replicates: int,
    target_swap_multiplier: float,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    observed = v16i.interval_spectrum(dag.predecessors)
    products: List[Dict[str, Any]] = []
    audits: List[Dict[str, Any]] = []
    for replicate in range(replicates):
        seed = v16i.stable_seed("v16k", label, *dag.key, replicate)
        rewired, audit = v16j.strict_rewire(
            dag, seed, target_swap_multiplier=target_swap_multiplier
        )
        products.append(v16i.interval_spectrum(rewired))
        audits.append({
            **dag.prefix,
            "null_family": label,
            "target_swap_multiplier": target_swap_multiplier,
            "null_replicate": replicate,
            "null_seed": seed,
            **audit,
        })
    unique_count = len({str(row["null_edge_sha256"]) for row in audits})
    unique_fraction = unique_count / replicates
    for row in audits:
        row["run_unique_null_count"] = unique_count
        row["run_unique_null_fraction"] = unique_fraction
        row["perturbation_integrity_pass"] = int(
            int(row["structure_pass"]) == 1
            and int(row["mixing_pass"]) == 1
            and unique_count == replicates
        )
    null_spectra = [row["probabilities"] for row in products]
    center = v16i.mean_spectrum(null_spectra)
    observed_js = v16i.jensen_shannon(observed["probabilities"], center)
    null_self = [
        v16i.jensen_shannon(row, v16i.mean_spectrum(null_spectra, skip=index))
        for index, row in enumerate(null_spectra)
    ]
    null_median = median(null_self)
    ratio = observed_js / max(null_median, v16j.EPSILON)
    summary = {
        **dag.prefix,
        "null_family": label,
        "target_swap_multiplier": target_swap_multiplier,
        "null_replicates": replicates,
        "n_events": len(dag.predecessors),
        "observed_js_to_null_center": observed_js,
        "null_median_leave_one_out_js": null_median,
        "js_effect_ratio": ratio,
        "effect_positive": int(ratio > 1.0),
        "observed_tail_mass_ge_8": observed["tail_mass_ge_8"],
        "null_mean_tail_mass_ge_8": mean(row["tail_mass_ge_8"] for row in products),
        "tail_mass_ge_8_delta": observed["tail_mass_ge_8"] - mean(row["tail_mass_ge_8"] for row in products),
        "mean_acceptance_rate": mean(float(row["acceptance_rate"]) for row in audits),
        "min_changed_edge_fraction": min(float(row["changed_edge_fraction"]) for row in audits),
        "unique_null_fraction": unique_fraction,
        "all_perturbation_integrity_pass": int(all(int(row["perturbation_integrity_pass"]) for row in audits)),
    }
    null_rows = [
        {
            **dag.prefix,
            "null_family": label,
            "target_swap_multiplier": target_swap_multiplier,
            "null_replicate": replicate,
            "null_seed": audits[replicate]["null_seed"],
            "null_edge_sha256": audits[replicate]["null_edge_sha256"],
            "leave_one_out_js": null_self[replicate],
            "tail_mass_ge_8": product["tail_mass_ge_8"],
            **{
                f"prob_{bin_label}": product["probabilities"][index]
                for index, (bin_label, _, _) in enumerate(v16i.INTERVAL_BINS)
            },
        }
        for replicate, product in enumerate(products)
    ]
    return summary, null_rows, audits


def longer_gate_row(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    primary = [row for row in rows if row["arm"] == PRIMARY_ARM]
    ratio = median(float(row["js_effect_ratio"]) for row in primary)
    positive = mean(float(row["effect_positive"]) for row in primary)
    integrity = len(primary) == 6 and all(int(row["all_perturbation_integrity_pass"]) for row in primary)
    passed = integrity and ratio >= LONGER_MIN_MEDIAN_EFFECT_RATIO and positive >= LONGER_MIN_POSITIVE_FRACTION
    return {
        "stage": "v16k",
        "primary_arm": PRIMARY_ARM,
        "n_runs": len(primary),
        "target_swap_multiplier": LONGER_TARGET_SWAP_MULTIPLIER,
        "null_replicates_per_run": LONGER_NULL_REPLICATES,
        "median_js_effect_ratio": ratio,
        "positive_fraction": positive,
        "perturbation_integrity_pass": int(integrity),
        "min_median_effect_ratio": LONGER_MIN_MEDIAN_EFFECT_RATIO,
        "min_positive_fraction": LONGER_MIN_POSITIVE_FRACTION,
        "longer_perturbation_consistency_pass": int(passed),
    }


def quantile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return ordered[low]
    fraction = position - low
    return ordered[low] * (1.0 - fraction) + ordered[high] * fraction


def bootstrap_median_interval(values: Sequence[float]) -> Tuple[float, float]:
    rng = random.Random(v16i.stable_seed("v16k", "magnitude-bootstrap"))
    draws = [
        median(values[rng.randrange(len(values))] for _ in values)
        for _ in range(BOOTSTRAP_REPLICATES)
    ]
    return quantile(draws, 0.025), quantile(draws, 0.975)


def magnitude_row(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    primary = [float(row["js_effect_ratio"]) for row in rows if row["arm"] == PRIMARY_ARM]
    if len(primary) != 6:
        raise ValueError("magnitude classification requires six primary runs")
    baselines = {
        row["source_stage"]: float(row["source_median_js_effect_ratio"])
        for row in v16i.read_csv(FROZEN_BASELINES)
    }
    fresh = median(primary)
    v16h_low, v16h_high = baselines["v16h"] * 0.5, baselines["v16h"] * 2.0
    v16d_low, v16d_high = baselines["v16d"] * 0.5, baselines["v16d"] * 2.0
    in_h = v16h_low <= fresh <= v16h_high
    in_d = v16d_low <= fresh <= v16d_high
    if in_h and in_d:
        classification = "compatible_with_both_prior_anchors"
    elif in_h:
        classification = "compatible_with_v16h_only"
    elif in_d:
        classification = "compatible_with_v16d_only"
    else:
        classification = "outside_factor_two_compatibility_envelope"
    ci_low, ci_high = bootstrap_median_interval(primary)
    return {
        "stage": "v16k",
        "primary_arm": PRIMARY_ARM,
        "n_runs": len(primary),
        "fresh_median_js_effect_ratio": fresh,
        "bootstrap_median_ci_low": ci_low,
        "bootstrap_median_ci_high": ci_high,
        "bootstrap_replicates": BOOTSTRAP_REPLICATES,
        "v16d_anchor_median": baselines["v16d"],
        "v16h_anchor_median": baselines["v16h"],
        "fresh_over_v16d": fresh / baselines["v16d"],
        "fresh_over_v16h": fresh / baselines["v16h"],
        "v16h_band_low": v16h_low,
        "both_band_low": max(v16h_low, v16d_low),
        "both_band_high": min(v16h_high, v16d_high),
        "v16d_band_high": v16d_high,
        "magnitude_compatibility_class": classification,
        "confirmatory_gate": 0,
    }


def gate_rows(
    target_rows: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    replay_rows: Sequence[Mapping[str, Any]],
    relabel_rows: Sequence[Mapping[str, Any]],
    direct_rows: Sequence[Mapping[str, Any]],
    strict_audits: Sequence[Mapping[str, Any]],
    local: Mapping[str, Any],
    longer_audits: Sequence[Mapping[str, Any]],
    longer: Mapping[str, Any],
    magnitude: Mapping[str, Any],
) -> Tuple[List[Dict[str, Any]], str]:
    expected_runs = 12
    target_pass = len(target_rows) == 1 and int(target_rows[0]["mean_initial_nodes"]) == TARGET_NODES
    history_pass = len(run_rows) == expected_runs and all(
        int(row["n_events"]) == STEPS
        and int(row["invalid_events"]) == 0
        and int(row["fine_acyclic"]) == 1
        and int(row["fine_edge_witness_errors"]) == 0
        for row in run_rows
    )
    replay_pass = len(replay_rows) == expected_runs * v16h.TOPOLOGICAL_REPLAYS and all(
        int(row["topological_order_valid"]) == 1
        and int(row["context_failures"]) == 0
        and int(row["final_structure_equal"]) == 1
        for row in replay_rows
    )
    relabel_pass = len(relabel_rows) == expected_runs and all(int(row["relabel_pass"]) for row in relabel_rows)
    direct_pass = len(direct_rows) == expected_runs and all(int(row["direct_log_parity_pass"]) for row in direct_rows)
    primary_null_pass = len(strict_audits) == expected_runs * PRIMARY_NULL_REPLICATES and all(
        int(row["null_integrity_pass"]) for row in strict_audits
    )
    longer_null_pass = len(longer_audits) == expected_runs * LONGER_NULL_REPLICATES and all(
        int(row["perturbation_integrity_pass"]) for row in longer_audits
    )
    instrumentation = all((target_pass, history_pass, replay_pass, relabel_pass, direct_pass, primary_null_pass, longer_null_pass))
    existence = int(local["local_gate_pass"]) == 1
    longer_consistency = int(longer["longer_perturbation_consistency_pass"]) == 1
    if not instrumentation:
        overall = "v16k_instrumentation_failed"
    elif not existence:
        overall = "fresh_strict_null_spectrum_contrast_not_replicated"
    elif not longer_consistency:
        overall = "fresh_spectrum_contrast_inconclusive_under_longer_perturbation"
    else:
        overall = "fresh_strict_null_spectrum_contrast_replicated"
    rows = [
        {"gate": "target_hygiene", "status": "pass" if target_pass else "fail", "observed": target_rows[0]["mean_initial_nodes"] if len(target_rows) == 1 else len(target_rows), "required": TARGET_NODES, "decision": "continue" if target_pass else "repair"},
        {"gate": "fresh_history_integrity", "status": "pass" if history_pass else "fail", "observed": f"runs={len(run_rows)};events={sum(int(row['n_events']) for row in run_rows)}", "required": "runs=12;events=36864", "decision": "continue" if history_pass else "repair"},
        {"gate": "replay_relabel_rate_parity", "status": "pass" if replay_pass and relabel_pass and direct_pass else "fail", "observed": f"replay={int(replay_pass)};relabel={int(relabel_pass)};rate={int(direct_pass)}", "required": "1;1;1", "decision": "continue" if replay_pass and relabel_pass and direct_pass else "repair"},
        {"gate": "primary_perturbation_integrity", "status": "pass" if primary_null_pass else "fail", "observed": f"passes={sum(int(row['null_integrity_pass']) for row in strict_audits)}/{len(strict_audits)}", "required": "384/384", "decision": "continue" if primary_null_pass else "inconclusive"},
        {"gate": "fresh_effect_existence", "status": "pass" if existence else "fail", "observed": f"median={float(local['median_js_effect_ratio']):.6f};positive={float(local['positive_fraction']):.6f};p_le_010={float(local['p_le_010_fraction']):.6f}", "required": "median>=2;positive>=5/6;p_le_010>=1/2", "decision": "replicated_primary" if existence else "not_replicated"},
        {"gate": "longer_perturbation_integrity", "status": "pass" if longer_null_pass else "fail", "observed": f"passes={sum(int(row['perturbation_integrity_pass']) for row in longer_audits)}/{len(longer_audits)}", "required": "192/192", "decision": "continue" if longer_null_pass else "inconclusive"},
        {"gate": "longer_perturbation_consistency", "status": "pass" if longer_consistency else "fail", "observed": f"median={float(longer['median_js_effect_ratio']):.6f};positive={float(longer['positive_fraction']):.6f}", "required": "median>=1;positive>=5/6", "decision": "consistent" if longer_consistency else "inconclusive"},
        {"gate": "magnitude_compatibility", "status": "descriptive", "observed": magnitude["magnitude_compatibility_class"], "required": "not_a_confirmatory_gate", "decision": magnitude["magnitude_compatibility_class"]},
        {"gate": "v16k_overall", "status": overall, "observed": f"instrumentation={int(instrumentation)};existence={int(existence)};longer={int(longer_consistency)}", "required": "1;1;1", "decision": overall},
    ]
    return rows, overall


def claim_rows(overall: str, magnitude: Mapping[str, Any]) -> List[Dict[str, Any]]:
    replicated = overall == "fresh_strict_null_spectrum_contrast_replicated"
    return [
        {"claim_id": "C1", "root_claim": 1, "claim": "The formal v16k histories were generated after the v16k design and new seeds were frozen.", "status": "supported", "evidence": "v16k_pre_registration.csv;v16k_execution_audit.csv", "undercutter": "An adviser transient used different quarantined seeds before freeze.", "scope_limit": "same simulator implementation and target as v16h"},
        {"claim_id": "C2", "root_claim": 1, "claim": "The finite event-DAG interval-spectrum contrast replicated on fresh histories under the unchanged v16j strict perturbation family.", "status": "supported" if replicated else "unsupported", "evidence": "v16k_effect_existence_gate.csv;v16k_longer_perturbation_gate.csv", "undercutter": "Perturbation integrity does not prove uniform or stationary null sampling.", "scope_limit": "conditional on this strict-null sampler"},
        {"claim_id": "C3", "root_claim": 0, "claim": "The fresh effect magnitude is descriptively compatible with one or both prior strict-null anchors.", "status": "supported" if magnitude["magnitude_compatibility_class"] != "outside_factor_two_compatibility_envelope" else "unsupported", "evidence": "v16k_magnitude_compatibility.csv", "undercutter": "Six primary runs give imprecise magnitude estimation.", "scope_limit": "descriptive factor-two bands; not a confirmatory stability gate"},
        {"claim_id": "C4", "root_claim": 1, "claim": "The v16j/v16k perturbations are approximately uniform independent samples from the constrained DAG space.", "status": "unsupported", "evidence": "none", "undercutter": "Short independently seeded swaps from the observed DAG have no convergence proof here.", "scope_limit": "only preservation, perturbation size, and uniqueness are audited"},
        {"claim_id": "C5", "root_claim": 1, "claim": "The contrast is independent of event-family and read/write-resource wiring.", "status": "unsupported", "evidence": "none", "undercutter": "The current null does not preserve those strata.", "scope_limit": "requires a separately calibrated resource-aware null"},
        {"claim_id": "C6", "root_claim": 1, "claim": "The interval spectrum establishes dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particles, or entanglement.", "status": "unsupported", "evidence": "none", "undercutter": "No analytic sprinkling comparison, continuum scaling, or relevant dynamics test was performed.", "scope_limit": "finite simulator event DAG only"},
    ]


def build_report(
    summaries: Sequence[Mapping[str, Any]],
    local: Mapping[str, Any],
    growth: Sequence[Mapping[str, Any]],
    scheduler: Sequence[Mapping[str, Any]],
    longer: Mapping[str, Any],
    magnitude: Mapping[str, Any],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16k fresh strict-null replication",
        "",
        f"Status: `{overall}`.",
        "",
        "## Frozen question",
        "",
        "Does the v16j finite event-DAG interval-spectrum contrast replicate on twelve fresh arm-specific runs when the observable, primary strict perturbation family, and existence thresholds are unchanged? Magnitude compatibility is reported separately and cannot change the existence result.",
        "",
        f"Specification digest: `{spec_digest()}`.",
        "",
        "The formal growth seeds were deterministically derived as " + ", ".join(str(value) for value in GROWTH_SEEDS) + ". Adviser-transient seeds 5203 and 5389 were quarantined and were not used.",
        "",
        "## Primary results",
        "",
    ]
    lines.extend(v16i.table(summaries, ("growth_seed", "run_offset", "arm", "observed_js_to_null_center", "null_median_leave_one_out_js", "js_effect_ratio", "empirical_p_upper", "tail_mass_ge_8_delta")))
    lines.extend(["", "## Separate outcomes", ""])
    lines.extend(v16i.table([local], ("n_runs", "median_js_effect_ratio", "positive_fraction", "p_le_010_fraction", "local_gate_pass")))
    lines.append("")
    lines.extend(v16i.table([longer], ("n_runs", "target_swap_multiplier", "median_js_effect_ratio", "positive_fraction", "perturbation_integrity_pass", "longer_perturbation_consistency_pass")))
    lines.append("")
    lines.extend(v16i.table([magnitude], ("fresh_median_js_effect_ratio", "bootstrap_median_ci_low", "bootstrap_median_ci_high", "fresh_over_v16d", "fresh_over_v16h", "magnitude_compatibility_class")))
    lines.extend(["", "Growth and scheduler rows are diagnostics, not additional primary endpoints.", ""])
    lines.extend(v16i.table(growth, ("group_field", "group_value", "n_runs", "median_js_effect_ratio", "positive_fraction", "group_pass")))
    lines.append("")
    lines.extend(v16i.table(scheduler, ("group_field", "group_value", "n_runs", "median_js_effect_ratio", "positive_fraction", "group_pass")))
    lines.extend(["", "## Gates", ""])
    lines.extend(v16i.table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "The primary null preserves scheduler order, exact direct in/out-degree, exact causal-depth sequence/profile, and the global dyadic parent-age-bin histogram. Its independently seeded short swap perturbations are audited for preservation, minimum perturbation, and uniqueness. These checks do not establish convergence, stationarity, independence, representativeness, or approximate uniform sampling over the constrained DAG space.",
        "",
        "All v16j strict-null tail-mass deltas, and the v16k values reported above, must be read by sign. The primary finding is a full-spectrum contrast; it is not automatically an increase in large intervals.",
        "",
        "Causal-set interval-abundance work derives dimension relevance by comparison with analytic expectations for Poisson-sprinkled Alexandrov intervals. v16k performs no such comparison. It therefore does not establish dimension, manifoldlikeness, Lorentz invariance, spacetime, continuum behavior, particles, entanglement, or a physical causal law.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    prereg = load_and_verify_preregistration()
    if shutil.disk_usage(ROOT).free < MIN_FREE_BYTES:
        raise RuntimeError("v16k run preflight requires at least 250 MiB free")
    adapter = v16ac.LocalSeedClockAdapter(v16h.frozen_local_rate())
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(
        ensembles, v10e.recommended_regime("fast_balanced"), list(GROWTH_SEEDS)
    )
    target_rows = v10e.summarize_bases(base_rows)
    ensemble_name = ensembles[0].name
    params = v16a.anchor_params()

    all_events: List[Dict[str, Any]] = []
    all_edges: List[Dict[str, Any]] = []
    run_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    relabel_rows: List[Dict[str, Any]] = []
    direct_rows: List[Dict[str, Any]] = []
    strict_summaries: List[Dict[str, Any]] = []
    strict_nulls: List[Dict[str, Any]] = []
    strict_audits: List[Dict[str, Any]] = []
    longer_summaries: List[Dict[str, Any]] = []
    longer_nulls: List[Dict[str, Any]] = []
    longer_audits: List[Dict[str, Any]] = []

    for index, assignment in enumerate(prereg, start=1):
        base = base_states[(ensemble_name, int(assignment["growth_seed"]))]
        events, edges, rates, run_row, replays, relabel, dependency_dag = v16h.run_assignment(
            base, assignment, params, adapter
        )
        direct = v16h.direct_rate_audit(base, events, rates, run_row, v16h.frozen_local_rate())
        if not int(direct["direct_log_parity_pass"]):
            raise RuntimeError(f"v16k direct-rate parity failed: {direct}")
        dag = run_dag_from_history(assignment, events, dependency_dag)
        strict_summary, run_strict_nulls, run_strict_audits = v16j.analyze_run(dag)
        longer_summary, run_longer_nulls, run_longer_audits = analyze_perturbation_family(
            dag,
            label="degree_depth_global_age_bin_double_edge_swap_longer_010",
            replicates=LONGER_NULL_REPLICATES,
            target_swap_multiplier=LONGER_TARGET_SWAP_MULTIPLIER,
        )
        all_events.extend(events)
        all_edges.extend(edges)
        run_rows.append(run_row)
        replay_rows.extend(replays)
        relabel_rows.append(relabel)
        direct_rows.append(direct)
        strict_summaries.append(strict_summary)
        strict_nulls.extend(run_strict_nulls)
        strict_audits.extend(run_strict_audits)
        longer_summaries.append(longer_summary)
        longer_nulls.extend(run_longer_nulls)
        longer_audits.extend(run_longer_audits)
        print(
            f"[v16k] runs={index}/{len(prereg)} arm={assignment['arm']} "
            f"primary_ratio={float(strict_summary['js_effect_ratio']):.6f} "
            f"longer_ratio={float(longer_summary['js_effect_ratio']):.6f}"
        )

    local = v16j.local_gate_row(strict_summaries, "v16k")
    growth = v16i.aggregate_rows(
        strict_summaries, "growth_seed", v16j.GROUP_MIN_MEDIAN_EFFECT_RATIO, v16j.GROUP_MIN_POSITIVE_FRACTION
    )
    scheduler = v16i.aggregate_rows(
        strict_summaries, "arm", v16j.GROUP_MIN_MEDIAN_EFFECT_RATIO, v16j.GROUP_MIN_POSITIVE_FRACTION
    )
    longer = longer_gate_row(longer_summaries)
    magnitude = magnitude_row(strict_summaries)
    gates, overall = gate_rows(
        target_rows, run_rows, replay_rows, relabel_rows, direct_rows,
        strict_audits, local, longer_audits, longer, magnitude,
    )

    v16i.write_csv(TARGET_SUMMARY, target_rows)
    v16i.write_csv(EVENT_LOG, all_events)
    v16i.write_csv(EDGE_LOG, all_edges)
    v16i.write_csv(RUN_SUMMARY, run_rows)
    v16i.write_csv(REPLAY_AUDIT, replay_rows)
    v16i.write_csv(RELABEL_AUDIT, relabel_rows)
    v16i.write_csv(DIRECT_RATE_AUDIT, direct_rows)
    v16i.write_csv(STRICT_RUNS, strict_summaries)
    v16i.write_csv(STRICT_NULLS, strict_nulls)
    v16i.write_csv(STRICT_AUDIT, strict_audits)
    v16i.write_csv(EFFECT_GATE, [local])
    v16i.write_csv(GROWTH_ROBUSTNESS, growth)
    v16i.write_csv(SCHEDULER_ROBUSTNESS, scheduler)
    v16i.write_csv(LONGER_RUNS, longer_summaries)
    v16i.write_csv(LONGER_NULLS, longer_nulls)
    v16i.write_csv(LONGER_AUDIT, longer_audits)
    v16i.write_csv(LONGER_GATE, [longer])
    v16i.write_csv(MAGNITUDE, [magnitude])
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claim_rows(overall, magnitude))
    v16i.write_csv(EXECUTION_AUDIT, [{
        "event": "adviser_transient_seed_quarantine",
        "observed": "in_memory_results_on_growth_seeds_5203_5389_were_seen_before_formal_freeze",
        "formal_growth_seeds": ";".join(str(value) for value in GROWTH_SEEDS),
        "excluded_growth_seeds": ";".join(str(value) for value in EXCLUDED_TRANSIENT_GROWTH_SEEDS),
        "thresholds_changed_after_transient": 0,
        "formal_seed_overlap": 0,
        "primary_gate_affected": 0,
    }])
    REPORT.write_text(build_report(strict_summaries, local, growth, scheduler, longer, magnitude, gates, overall), encoding="utf-8")
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.16k\n\n"
        f"Status: `{overall}`.\n\n"
        f"Primary median effect ratio: `{float(local['median_js_effect_ratio']):.6f}`.\n\n"
        f"Longer-perturbation median ratio: `{float(longer['median_js_effect_ratio']):.6f}`.\n\n"
        f"Magnitude class: `{magnitude['magnitude_compatibility_class']}`.\n\n"
        "If the fresh existence result replicated, calibrate a coarse event-family/resource-stratified null on calibration histories before applying it to a new holdout. Do not fit dimension or claim geometry.\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.16k\n\n"
        f"Statusen er `{overall}`. Testen kjoerte helt nye simuleringer og sammenlignet hendelsesgrafene med strukturbevarende tilfeldige perturbasjoner. "
        "Den avgjor om et avgrenset grafmonster gjentar seg, ikke om romtid eller partikler er funnet.\n",
        encoding="utf-8",
    )
    print(f"[v16k] complete overall={overall} magnitude={magnitude['magnitude_compatibility_class']}")


def verify_outputs() -> None:
    load_and_verify_preregistration()
    events = v16i.read_csv(EVENT_LOG)
    runs = v16i.read_csv(RUN_SUMMARY)
    strict_runs = v16i.read_csv(STRICT_RUNS)
    strict_audits = v16i.read_csv(STRICT_AUDIT)
    longer_runs = v16i.read_csv(LONGER_RUNS)
    longer_audits = v16i.read_csv(LONGER_AUDIT)
    gates = v16i.read_csv(GATE_EVALUATION)
    claims = v16i.read_csv(CLAIM_LEDGER)
    if len(events) != 12 * STEPS or len(runs) != 12 or len(strict_runs) != 12 or len(longer_runs) != 12:
        raise ValueError("v16k history/result row counts failed")
    if len(strict_audits) != 12 * PRIMARY_NULL_REPLICATES or not all(int(row["null_integrity_pass"]) for row in strict_audits):
        raise ValueError("v16k primary perturbation integrity failed")
    if len(longer_audits) != 12 * LONGER_NULL_REPLICATES or not all(int(row["perturbation_integrity_pass"]) for row in longer_audits):
        raise ValueError("v16k longer perturbation integrity failed")
    if len({row["gate"] for row in gates}) != len(gates) or len({row["claim_id"] for row in claims}) != len(claims):
        raise ValueError("v16k duplicate gate or claim ids")
    for path in (EVENT_LOG, EDGE_LOG, RUN_SUMMARY, STRICT_RUNS, STRICT_NULLS, STRICT_AUDIT, LONGER_RUNS, LONGER_NULLS, LONGER_AUDIT, MAGNITUDE, GATE_EVALUATION):
        for row in v16i.read_csv(path):
            if any(str(value).lower() in {"nan", "inf", "-inf"} for value in row.values()):
                raise ValueError(f"v16k non-finite value in {path.name}")
    overall = next(row["status"] for row in gates if row["gate"] == "v16k_overall")
    allowed = {
        "v16k_instrumentation_failed",
        "fresh_strict_null_spectrum_contrast_not_replicated",
        "fresh_spectrum_contrast_inconclusive_under_longer_perturbation",
        "fresh_strict_null_spectrum_contrast_replicated",
    }
    if overall not in allowed:
        raise ValueError("v16k unknown overall status")
    print(f"[v16k] output verification pass overall={overall}")


def self_test() -> None:
    if len(assignments()) != 12 or len({row["run_seed"] for row in assignments()}) != 12:
        raise AssertionError("v16k assignments are not unique")
    if set(GROWTH_SEEDS) & set(EXCLUDED_TRANSIENT_GROWTH_SEEDS):
        raise AssertionError("v16k formal seeds overlap transient seeds")
    if PRIMARY_NULL_REPLICATES != 32 or LONGER_TARGET_SWAP_MULTIPLIER <= v16j.TARGET_ACCEPTED_SWAPS_PER_EDGE:
        raise AssertionError("v16k perturbation design changed")
    fake = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    low, high = bootstrap_median_interval(fake)
    if not (low <= median(fake) <= high):
        raise AssertionError("v16k bootstrap interval failed")
    print(f"[v16k] self-test pass seeds={GROWTH_SEEDS} offsets={RUN_OFFSETS}")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16k fresh strict-null replication")
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
