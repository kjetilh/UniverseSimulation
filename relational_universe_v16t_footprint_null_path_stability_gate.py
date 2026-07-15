#!/usr/bin/env python3
"""v16t: effect-blind path and chain-length stability gate for the footprint null.

This gate computes interval spectra only for rewired null DAGs. It never computes
the source DAG spectrum and therefore cannot inspect or tune the v16s effect.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16j_interval_strict_null_gate as v16j
import relational_universe_v16n_coarse_event_resource_null_calibration as v16n
import relational_universe_v16o_event_resource_reachability_audit as v16o
import relational_universe_v16q_event_footprint_null_calibration as v16q
import relational_universe_v16s_fresh_event_footprint_holdout as v16s


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

REPLICATES = 16
MAX_ATTEMPTS_PER_EDGE = 240
MIN_CHANGED_EDGE_FRACTION = v16q.MIN_CHANGED_EDGE_FRACTION
MIN_UNIQUE_NULL_FRACTION = v16q.MIN_UNIQUE_NULL_FRACTION
MAX_CENTER_SHIFT_RATIO = 2.0

PROTOCOLS: Tuple[Tuple[str, Tuple[float, ...]], ...] = (
    ("direct_short_0075", (0.075,)),
    ("direct_reference_0100", (0.100,)),
    ("direct_long_0200", (0.200,)),
    ("staged_long_0100x2", (0.100, 0.100)),
)
COMPARISONS: Tuple[Tuple[str, str, str, str], ...] = (
    ("short_vs_reference", "direct_short_0075", "direct_reference_0100", "chain_length"),
    ("reference_vs_long", "direct_reference_0100", "direct_long_0200", "chain_length"),
    ("direct_long_vs_staged_long", "direct_long_0200", "staged_long_0100x2", "path_segmentation"),
)

SOURCE_CHAIN = DOC / "v16t_source_chain.csv"
PRE_REGISTRATION = DOC / "v16t_pre_registration.csv"
NULL_DISTRIBUTION = DOC / "v16t_null_spectrum_distribution.csv"
PERTURBATION_AUDIT = DOC / "v16t_footprint_perturbation_integrity.csv"
PROTOCOL_SUMMARY = DOC / "v16t_null_protocol_summary.csv"
CENTER_COMPARISON = DOC / "v16t_null_center_comparison.csv"
GATE_EVALUATION = DOC / "v16t_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16t_claim_ledger.csv"
REPORT = DOC / "v16t_footprint_null_path_stability_gate.md"
RECOMMENDATION = DOC / "v0_16t_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16t.md"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v16s", "fresh_event_histories", v16s.EVENT_LOG),
        ("v16s", "fresh_dependency_edges", v16s.EDGE_LOG),
        ("v16s", "fresh_history_gate", v16s.GATE_EVALUATION),
        ("v16q", "footprint_sampler_implementation", Path(v16q.__file__)),
        ("v16q", "sampler_qualification", v16q.QUALIFICATION),
    )
    return [{
        "stage": stage,
        "role": role,
        "artifact": path.name,
        "sha256": file_sha256(path),
        "source_pass": 1,
    } for stage, role, path in paths]


def spec_payload() -> Dict[str, Any]:
    return {
        "gate": "v16t_footprint_null_path_stability_gate",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_null_sampler_stability_on_six_frozen_v16s_histories",
        "source_history_count": 6,
        "source_arm": v16s.PRIMARY_ARM,
        "null_family": v16q.NULL_FAMILY,
        "protocols": [
            {"label": label, "stage_swap_multipliers": list(multipliers)}
            for label, multipliers in PROTOCOLS
        ],
        "comparisons": [
            {"label": label, "left": left, "right": right, "gate_family": family}
            for label, left, right, family in COMPARISONS
        ],
        "replicates_per_protocol_per_history": REPLICATES,
        "max_attempts_per_edge": MAX_ATTEMPTS_PER_EDGE,
        "min_changed_edge_fraction": MIN_CHANGED_EDGE_FRACTION,
        "min_unique_null_fraction": MIN_UNIQUE_NULL_FRACTION,
        "center_metric": "jensen_shannon_between_protocol_mean_spectra",
        "dispersion_metric": "median_pooled_leave_one_out_jensen_shannon",
        "center_shift_ratio": "center_js/max(pooled_leave_one_out_median,epsilon)",
        "max_center_shift_ratio": MAX_CENTER_SHIFT_RATIO,
        "all_source_dags_must_pass": True,
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "no_early_stop": True,
    }


def spec_digest() -> str:
    raw = json.dumps(spec_payload(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def preregistration_row() -> Dict[str, Any]:
    return {
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "script_sha256": file_sha256(SCRIPT),
        "source_chain_sha256": file_sha256(SOURCE_CHAIN),
        "source_history_count": 6,
        "source_arm": v16s.PRIMARY_ARM,
        "protocols": ";".join(label for label, _ in PROTOCOLS),
        "replicates_per_protocol_per_history": REPLICATES,
        "max_attempts_per_edge": MAX_ATTEMPTS_PER_EDGE,
        "min_changed_edge_fraction": MIN_CHANGED_EDGE_FRACTION,
        "min_unique_null_fraction": MIN_UNIQUE_NULL_FRACTION,
        "max_center_shift_ratio": MAX_CENTER_SHIFT_RATIO,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v16s.verify_outputs()
    overall = next(
        row["status"] for row in v16i.read_csv(v16s.GATE_EVALUATION)
        if row["gate"] == "v16s_overall"
    )
    if overall != "v16s_fresh_event_footprint_spectrum_contrast_replicated":
        raise ValueError("v16t requires the frozen successful v16s fresh-history gate")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v16t] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    rows = v16i.read_csv(PRE_REGISTRATION)
    expected = {key: str(value) for key, value in preregistration_row().items()}
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v16t preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v16t source chain changed")


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    grouped: Dict[Tuple[int, int, str, int], List[Dict[str, str]]] = defaultdict(list)
    for row in v16i.read_csv(v16s.EVENT_LOG):
        if row["arm"] == v16s.PRIMARY_ARM:
            grouped[v16o.run_key(row)].append(row)
    runs: List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]] = []
    for key in sorted(grouped):
        rows = sorted(grouped[key], key=lambda row: int(row["event_id"]))
        metadata, audit = v16n.event_metadata(rows)
        if not int(audit["event_id_mapping_total_pass"]):
            raise ValueError("v16t event metadata mapping failed")
        predecessors = tuple(
            tuple(int(value) for value in row["direct_predecessors"].split(";") if value)
            for row in rows
        )
        depths = tuple(int(row["causal_depth"]) for row in rows)
        if tuple(v16i.recompute_depths(predecessors)) != depths:
            raise ValueError("v16t source depth mismatch")
        growth_seed, run_offset, arm, run_seed = key
        runs.append((v16i.RunDAG(
            stage="v16t",
            target_nodes=v16s.TARGET_NODES,
            growth_seed=growth_seed,
            run_offset=run_offset,
            arm=arm,
            run_seed=run_seed,
            predecessors=predecessors,
            depths=depths,
            indegrees=tuple(len(parents) for parents in predecessors),
        ), metadata))
    if len(runs) != 6:
        raise ValueError("v16t requires six frozen v16s histories")
    return runs


def final_structure_audit(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    rewired: Sequence[Sequence[int]],
) -> Dict[str, Any]:
    original = dag.predecessors
    original_edges = {
        (parent, child) for child, parents in enumerate(original) for parent in parents
    }
    rewired_edges = {
        (parent, child) for child, parents in enumerate(rewired) for parent in parents
    }
    edge_count = len(original_edges)
    changed_edges = edge_count - len(original_edges & rewired_edges)
    checks = {
        "edge_count_pass": int(len(rewired_edges) == edge_count),
        "scheduler_order_pass": int(all(parent < child for parent, child in rewired_edges)),
        "indegree_sequence_pass": int(tuple(len(parents) for parents in rewired) == dag.indegrees),
        "outdegree_sequence_pass": int(v16j.outdegrees(rewired) == v16j.outdegrees(original)),
        "depth_sequence_pass": int(tuple(v16i.recompute_depths(rewired)) == dag.depths),
        "global_age_bin_histogram_pass": int(
            v16j.global_age_signature(rewired) == v16j.global_age_signature(original)
        ),
        "global_event_footprint_histogram_pass": int(
            v16q.footprint_signature(rewired, metadata)
            == v16q.footprint_signature(original, metadata)
        ),
    }
    actual_conflicts = sum(
        v16n.edge_color(parent, child, metadata) is not None
        for parent, child in rewired_edges
    )
    return {
        "edge_count": edge_count,
        "changed_edge_count": changed_edges,
        "changed_edge_fraction": changed_edges / edge_count,
        **checks,
        "actual_resource_conflict_edge_fraction": actual_conflicts / edge_count,
        "structure_pass": int(all(checks.values())),
        "null_edge_sha256": v16j.edge_digest(rewired),
    }


def run_protocol(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    protocol_label: str,
    stage_multipliers: Sequence[float],
    replicate: int,
) -> Tuple[Tuple[Tuple[int, ...], ...], Dict[str, Any]]:
    current = dag.predecessors
    stage_audits: List[Dict[str, Any]] = []
    stage_seeds: List[int] = []
    for stage_index, multiplier in enumerate(stage_multipliers, start=1):
        stage_seed = v16i.stable_seed(
            "v16t", protocol_label, *dag.key, replicate, stage_index,
            f"swap={multiplier:.6f}",
        )
        stage_dag = v16i.RunDAG(
            stage="v16t",
            target_nodes=dag.target_nodes,
            growth_seed=dag.growth_seed,
            run_offset=dag.run_offset,
            arm=dag.arm,
            run_seed=dag.run_seed,
            predecessors=tuple(tuple(parents) for parents in current),
            depths=dag.depths,
            indegrees=dag.indegrees,
        )
        current, stage_audit = v16q.footprint_rewire(
            stage_dag,
            metadata,
            stage_seed,
            target_swap_multiplier=multiplier,
            max_attempts_per_edge=MAX_ATTEMPTS_PER_EDGE,
        )
        stage_seeds.append(stage_seed)
        stage_audits.append(stage_audit)

    final = final_structure_audit(dag, metadata, current)
    completion_pass = all(int(row["completion_and_change_pass"]) for row in stage_audits)
    final_change_pass = float(final["changed_edge_fraction"]) >= MIN_CHANGED_EDGE_FRACTION
    total_attempts = sum(int(row["attempted_swaps"]) for row in stage_audits)
    total_accepted = sum(int(row["accepted_swaps"]) for row in stage_audits)
    audit = {
        **dag.prefix,
        "protocol": protocol_label,
        "stage_swap_multipliers": "+".join(f"{value:.3f}" for value in stage_multipliers),
        "stage_count": len(stage_multipliers),
        "null_replicate": replicate,
        "null_seed": ";".join(str(seed) for seed in stage_seeds),
        "max_attempts_per_edge": MAX_ATTEMPTS_PER_EDGE,
        "target_accepted_swaps": sum(int(row["target_accepted_swaps"]) for row in stage_audits),
        "accepted_swaps": total_accepted,
        "attempted_swaps": total_attempts,
        "attempts_per_edge": total_attempts / int(final["edge_count"]),
        "acceptance_rate": total_accepted / total_attempts if total_attempts else 0.0,
        "stage_1_target_accepted_swaps": stage_audits[0]["target_accepted_swaps"],
        "stage_1_accepted_swaps": stage_audits[0]["accepted_swaps"],
        "stage_1_attempted_swaps": stage_audits[0]["attempted_swaps"],
        "stage_1_changed_edge_fraction": stage_audits[0]["changed_edge_fraction"],
        "stage_1_completion_pass": stage_audits[0]["completion_and_change_pass"],
        "stage_2_target_accepted_swaps": stage_audits[1]["target_accepted_swaps"] if len(stage_audits) == 2 else "",
        "stage_2_accepted_swaps": stage_audits[1]["accepted_swaps"] if len(stage_audits) == 2 else "",
        "stage_2_attempted_swaps": stage_audits[1]["attempted_swaps"] if len(stage_audits) == 2 else "",
        "stage_2_changed_edge_fraction": stage_audits[1]["changed_edge_fraction"] if len(stage_audits) == 2 else "",
        "stage_2_completion_pass": stage_audits[1]["completion_and_change_pass"] if len(stage_audits) == 2 else "",
        **final,
        "all_stage_completion_pass": int(completion_pass),
        "final_change_pass": int(final_change_pass),
        "completion_and_change_pass": int(completion_pass and final_change_pass),
    }
    return tuple(tuple(parents) for parents in current), audit


def protocol_products(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    protocol_label: str,
    multipliers: Sequence[float],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    products: List[Dict[str, Any]] = []
    audits: List[Dict[str, Any]] = []
    for replicate in range(REPLICATES):
        rewired, audit = run_protocol(dag, metadata, protocol_label, multipliers, replicate)
        products.append(v16i.interval_spectrum(rewired))
        audits.append(audit)
    unique_count = len({row["null_edge_sha256"] for row in audits})
    unique_fraction = unique_count / REPLICATES
    spectra = [row["probabilities"] for row in products]
    center = v16i.mean_spectrum(spectra)
    leave_one_out = [
        v16i.jensen_shannon(spectrum, v16i.mean_spectrum(spectra, skip=index))
        for index, spectrum in enumerate(spectra)
    ]
    for row in audits:
        row["run_unique_null_count"] = unique_count
        row["run_unique_null_fraction"] = unique_fraction
        row["run_uniqueness_pass"] = int(unique_fraction >= MIN_UNIQUE_NULL_FRACTION)
        row["perturbation_integrity_pass"] = int(
            int(row["structure_pass"])
            and int(row["completion_and_change_pass"])
            and int(row["run_uniqueness_pass"])
        )
    null_rows = [{
        **dag.prefix,
        "protocol": protocol_label,
        "null_replicate": replicate,
        "null_seed": audits[replicate]["null_seed"],
        "null_edge_sha256": audits[replicate]["null_edge_sha256"],
        "comparable_pairs": product["comparable_pairs"],
        "leave_one_out_js": leave_one_out[replicate],
        "mean_open_volume": product["mean_open_volume"],
        "tail_mass_ge_8": product["tail_mass_ge_8"],
        "spectrum_entropy": product["spectrum_entropy"],
        **{
            f"prob_{label}": product["probabilities"][index]
            for index, (label, _, _) in enumerate(v16i.INTERVAL_BINS)
        },
    } for replicate, product in enumerate(products)]
    summary = {
        **dag.prefix,
        "protocol": protocol_label,
        "stage_swap_multipliers": "+".join(f"{value:.3f}" for value in multipliers),
        "null_replicates": REPLICATES,
        "median_leave_one_out_js": v16i.median(leave_one_out),
        "mean_open_volume": v16i.mean(row["mean_open_volume"] for row in products),
        "mean_tail_mass_ge_8": v16i.mean(row["tail_mass_ge_8"] for row in products),
        "mean_acceptance_rate": v16i.mean(float(row["acceptance_rate"]) for row in audits),
        "min_changed_edge_fraction": min(float(row["changed_edge_fraction"]) for row in audits),
        "min_actual_resource_conflict_edge_fraction": min(
            float(row["actual_resource_conflict_edge_fraction"]) for row in audits
        ),
        "unique_null_fraction": unique_fraction,
        "all_perturbation_integrity_pass": int(
            all(int(row["perturbation_integrity_pass"]) for row in audits)
        ),
        **{
            f"center_prob_{label}": center[index]
            for index, (label, _, _) in enumerate(v16i.INTERVAL_BINS)
        },
    }
    return null_rows, audits, summary


def comparison_rows(
    null_rows: Sequence[Mapping[str, Any]],
    runs: Sequence[v16i.RunDAG],
) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[Tuple[int, int, str, int], str], List[Mapping[str, Any]]] = defaultdict(list)
    for row in null_rows:
        grouped[(v16i.run_key(row), str(row["protocol"]))].append(row)
    rows: List[Dict[str, Any]] = []
    probability_fields = [f"prob_{label}" for label, _, _ in v16i.INTERVAL_BINS]
    for dag in runs:
        for comparison, left_label, right_label, gate_family in COMPARISONS:
            left = sorted(
                grouped[(dag.key, left_label)], key=lambda row: int(row["null_replicate"])
            )
            right = sorted(
                grouped[(dag.key, right_label)], key=lambda row: int(row["null_replicate"])
            )
            if len(left) != REPLICATES or len(right) != REPLICATES:
                raise ValueError("v16t incomplete null ensemble")
            left_spectra = [[float(row[field]) for field in probability_fields] for row in left]
            right_spectra = [[float(row[field]) for field in probability_fields] for row in right]
            left_center = v16i.mean_spectrum(left_spectra)
            right_center = v16i.mean_spectrum(right_spectra)
            center_js = v16i.jensen_shannon(left_center, right_center)
            pooled_dispersion = v16i.median([
                *(float(row["leave_one_out_js"]) for row in left),
                *(float(row["leave_one_out_js"]) for row in right),
            ])
            ratio = center_js / max(pooled_dispersion, v16j.EPSILON)
            rows.append({
                **dag.prefix,
                "comparison": comparison,
                "gate_family": gate_family,
                "left_protocol": left_label,
                "right_protocol": right_label,
                "center_jensen_shannon": center_js,
                "pooled_median_leave_one_out_js": pooled_dispersion,
                "center_shift_ratio": ratio,
                "max_absolute_bin_delta": max(
                    abs(left_value - right_value)
                    for left_value, right_value in zip(left_center, right_center)
                ),
                "threshold": MAX_CENTER_SHIFT_RATIO,
                "stability_pass": int(ratio <= MAX_CENTER_SHIFT_RATIO),
            })
    return rows


def build_report(
    summaries: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16t footprint-null path stability gate",
        "",
        f"Status: `{overall}`.",
        "",
        "V16t is an effect-blind stability test of the v16q event-footprint null on the six frozen fresh v16s histories. It compares null ensembles across direct chain lengths and a segmented two-stage path. The source DAG interval spectrum and every observed/null effect statistic are excluded by design.",
        "",
        f"Specification digest: `{spec_digest()}`.",
        "",
        "## Frozen design",
        "",
        f"Each source DAG has `{REPLICATES}` independent nulls under each of four protocols: direct multipliers `0.075`, `0.100`, `0.200`, and staged `0.100 + 0.100`. The attempt ceiling is `{MAX_ATTEMPTS_PER_EDGE}` per edge per stage.",
        "",
        f"A comparison passes only when its center Jensen-Shannon divergence is at most `{MAX_CENTER_SHIFT_RATIO}` times the pooled median leave-one-out divergence. Every source DAG must pass.",
        "",
        "## Protocol summaries",
        "",
    ]
    lines.extend(v16i.table(summaries, (
        "growth_seed", "run_offset", "protocol", "median_leave_one_out_js",
        "mean_tail_mass_ge_8", "min_changed_edge_fraction",
        "min_actual_resource_conflict_edge_fraction", "all_perturbation_integrity_pass",
    )))
    lines.extend(["", "## Null-center comparisons", ""])
    lines.extend(v16i.table(comparisons, (
        "growth_seed", "run_offset", "comparison", "center_jensen_shannon",
        "pooled_median_leave_one_out_js", "center_shift_ratio", "stability_pass",
    )))
    lines.extend(["", "## Gates", ""])
    lines.extend(v16i.table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Evidential boundary",
        "",
        "A pass supports only procedure-level stability of null centers across these tested finite paths, lengths, seeds, and six source DAGs. It does not establish Markov-chain irreducibility, mixing time, convergence, stationarity, independence, representativeness, or uniform sampling.",
        "",
        "Because no source spectrum is computed, v16t neither confirms nor weakens the observed v16s spectrum contrast. It only tests whether that contrast was referenced to a visibly path-sensitive null center.",
        "",
        "No dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particle, entanglement, invariant, or physical-law claim is evaluated.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    verify_frozen_sources()
    loaded = load_runs()
    null_rows: List[Dict[str, Any]] = []
    audits: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []
    for run_index, (dag, metadata) in enumerate(loaded, start=1):
        for protocol_label, multipliers in PROTOCOLS:
            products, protocol_audits, summary = protocol_products(
                dag, metadata, protocol_label, multipliers
            )
            null_rows.extend(products)
            audits.extend(protocol_audits)
            summaries.append(summary)
        print(f"[v16t] source_runs={run_index}/{len(loaded)} protocols={len(PROTOCOLS)}")

    comparisons = comparison_rows(null_rows, [dag for dag, _ in loaded])
    expected_perturbations = len(loaded) * len(PROTOCOLS) * REPLICATES
    source_pass = len(loaded) == 6
    integrity_pass = (
        len(audits) == expected_perturbations
        and all(int(row["perturbation_integrity_pass"]) for row in audits)
    )
    chain_rows = [row for row in comparisons if row["gate_family"] == "chain_length"]
    path_rows = [row for row in comparisons if row["gate_family"] == "path_segmentation"]
    chain_pass = len(chain_rows) == 12 and all(int(row["stability_pass"]) for row in chain_rows)
    path_pass = len(path_rows) == 6 and all(int(row["stability_pass"]) for row in path_rows)
    if not source_pass or not integrity_pass:
        overall = "v16t_footprint_null_stability_instrumentation_failed"
    elif not chain_pass:
        overall = "v16t_footprint_null_center_chain_length_unstable"
    elif not path_pass:
        overall = "v16t_footprint_null_center_path_dependent"
    else:
        overall = "v16t_footprint_null_centers_stable_across_tested_paths"
    gates = [
        {
            "gate": "frozen_source_integrity",
            "status": "pass" if source_pass else "fail",
            "observed": f"source_dags={len(loaded)}",
            "required": "source_dags=6",
            "decision": "continue" if source_pass else "repair",
        },
        {
            "gate": "all_protocol_perturbation_integrity",
            "status": "pass" if integrity_pass else "fail",
            "observed": f"{sum(int(row['perturbation_integrity_pass']) for row in audits)}/{len(audits)}",
            "required": f"{expected_perturbations}/{expected_perturbations}",
            "decision": "continue" if integrity_pass else "instrumentation_failed",
        },
        {
            "gate": "chain_length_null_center_stability",
            "status": "pass" if chain_pass else "fail",
            "observed": f"{sum(int(row['stability_pass']) for row in chain_rows)}/{len(chain_rows)};max_ratio={max(float(row['center_shift_ratio']) for row in chain_rows):.6f}",
            "required": f"12/12;ratio<={MAX_CENTER_SHIFT_RATIO}",
            "decision": "stable" if chain_pass else "sampler_length_sensitive",
        },
        {
            "gate": "path_segmentation_null_center_stability",
            "status": "pass" if path_pass else "fail",
            "observed": f"{sum(int(row['stability_pass']) for row in path_rows)}/{len(path_rows)};max_ratio={max(float(row['center_shift_ratio']) for row in path_rows):.6f}",
            "required": f"6/6;ratio<={MAX_CENTER_SHIFT_RATIO}",
            "decision": "stable" if path_pass else "sampler_path_dependent",
        },
        {
            "gate": "observed_spectrum_and_effect_exclusion",
            "status": "pass",
            "observed": "source_spectra=0;observed_effect_metrics=0",
            "required": "0;0",
            "decision": "effect_blind",
        },
        {
            "gate": "v16t_overall",
            "status": overall,
            "observed": f"integrity={int(integrity_pass)};chain={int(chain_pass)};path={int(path_pass)}",
            "required": "1;1;1",
            "decision": overall,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "The event-footprint null center is stable across the tested direct chain lengths and staged path on all six frozen v16s DAGs.",
            "status": "supported" if overall == "v16t_footprint_null_centers_stable_across_tested_paths" else "unsupported",
            "evidence": "v16t_null_center_comparison.csv;v16t_gate_evaluation.csv",
            "scope_limit": "four frozen protocols, sixteen nulls each, six finite source DAGs",
        },
        {
            "claim_id": "C2",
            "claim": "The sampler is irreducible, mixed, converged, stationary, independent, representative, or uniform.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "finite center stability is not a Markov-chain proof",
        },
        {
            "claim_id": "C3",
            "claim": "The v16s observed interval-spectrum contrast was replicated or re-evaluated in v16t.",
            "status": "not_evaluated",
            "evidence": "v16t_gate_evaluation.csv",
            "scope_limit": "source spectrum and observed-effect metrics were excluded",
        },
        {
            "claim_id": "C4",
            "claim": "Dimension, Lorentz symmetry, spacetime, continuum physics, particles, entanglement, invariants, or physical laws were established.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "null-sampler instrumentation only",
        },
    ]
    v16i.write_csv(NULL_DISTRIBUTION, null_rows)
    v16i.write_csv(PERTURBATION_AUDIT, audits)
    v16i.write_csv(PROTOCOL_SUMMARY, summaries)
    v16i.write_csv(CENTER_COMPARISON, comparisons)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    REPORT.write_text(build_report(summaries, comparisons, gates, overall), encoding="utf-8")
    next_step = (
        "freeze_an_independent_null_family_before_any_new_effect_claim"
        if overall == "v16t_footprint_null_centers_stable_across_tested_paths"
        else "repair_or_retire_the_path_sensitive_footprint_sampler_before_effect_work"
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.16t\n\n"
        f"Status: `{overall}`.\n\n"
        f"Next: `{next_step}`.\n\n"
        "V16t is effect-blind and does not recompute the v16s observed contrast. A pass is procedural stability evidence, not a proof of sampler mixing or physical geometry.\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.16t\n\n"
        f"Statusen er `{overall}`. Denne runden tester bare om kontrollgeneratoren gir omtrent samme kontrollfordeling naar den kjoeres kortere, lengre eller i to etapper. Den ser ikke paa originalsignalets styrke og kan derfor ikke finjusteres mot et positivt resultat. Selv et bestaa-resultat er ikke et bevis paa romtid eller fysikk.\n",
        encoding="utf-8",
    )
    print(f"[v16t] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    nulls = v16i.read_csv(NULL_DISTRIBUTION)
    audits = v16i.read_csv(PERTURBATION_AUDIT)
    summaries = v16i.read_csv(PROTOCOL_SUMMARY)
    comparisons = v16i.read_csv(CENTER_COMPARISON)
    gates = v16i.read_csv(GATE_EVALUATION)
    expected = 6 * len(PROTOCOLS) * REPLICATES
    if len(nulls) != expected or len(audits) != expected:
        raise ValueError("v16t null or audit row count failed")
    if len(summaries) != 6 * len(PROTOCOLS) or len(comparisons) != 6 * len(COMPARISONS):
        raise ValueError("v16t summary or comparison row count failed")
    null_keys = {
        (v16i.run_key(row), row["protocol"], int(row["null_replicate"])) for row in nulls
    }
    audit_keys = {
        (v16i.run_key(row), row["protocol"], int(row["null_replicate"])) for row in audits
    }
    if null_keys != audit_keys or len(null_keys) != expected:
        raise ValueError("v16t null/audit identity mismatch")
    exclusion = next(row for row in gates if row["gate"] == "observed_spectrum_and_effect_exclusion")
    if exclusion["status"] != "pass" or exclusion["observed"] != "source_spectra=0;observed_effect_metrics=0":
        raise ValueError("v16t effect-blind exclusion failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16t_overall")
    allowed = {
        "v16t_footprint_null_stability_instrumentation_failed",
        "v16t_footprint_null_center_chain_length_unstable",
        "v16t_footprint_null_center_path_dependent",
        "v16t_footprint_null_centers_stable_across_tested_paths",
    }
    if overall not in allowed:
        raise ValueError("v16t unknown overall status")
    print(f"[v16t] output verification pass overall={overall}")


def self_test() -> None:
    if len(PROTOCOLS) != 4 or len(COMPARISONS) != 3:
        raise AssertionError("v16t frozen protocol matrix changed")
    if REPLICATES != 16 or MAX_ATTEMPTS_PER_EDGE != 240:
        raise AssertionError("v16t frozen budget changed")
    if MAX_CENTER_SHIFT_RATIO != 2.0:
        raise AssertionError("v16t frozen threshold changed")
    payload = spec_payload()
    if payload["source_spectrum_computation_allowed"] or payload["observed_effect_computation_allowed"]:
        raise AssertionError("v16t effect-blind exclusion changed")
    print("[v16t] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16t footprint-null path stability gate")
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
