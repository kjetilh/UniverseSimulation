#!/usr/bin/env python3
"""v16m: new fresh-history holdout using the v16l-qualified sampler ceiling.

The v16j interval-spectrum observable, swap targets, null counts, stopping
conditions, and scientific thresholds remain unchanged.  The only sampler
change is the v16l-qualified safety ceiling of 240 attempts per direct edge.

This finite event-DAG test does not establish dimension, manifoldlikeness,
Lorentz symmetry, spacetime, continuum behavior, particles, entanglement, or a
physical causal law.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v16a_disjoint_event_commutation_gate as v16a
import relational_universe_v16ac_local_seed_adapter_gate as v16ac
import relational_universe_v16h_fresh_rate_logged_mechanism_holdout as v16h
import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16j_interval_strict_null_gate as v16j
import relational_universe_v16k_fresh_strict_null_replication as v16k
import relational_universe_v16l_sampler_attempt_qualification as v16l


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

TARGET_NODES = v16k.TARGET_NODES
STEPS = v16k.STEPS
GROWTH_SEEDS = tuple(
    5000 + v16i.stable_seed("v16m", "fresh-growth", index) % 4000
    for index in range(2)
)
RUN_OFFSETS = tuple(
    100000 + v16i.stable_seed("v16m", "fresh-offset", index) % 9000
    for index in range(3)
)
ARMS = v16k.ARMS
PRIMARY_ARM = v16k.PRIMARY_ARM
EXCLUDED_GROWTH_SEEDS = (5203, 5389, *v16k.GROWTH_SEEDS)
QUALIFIED_MAX_ATTEMPTS_PER_EDGE = v16l.QUALIFIED_MAX_ATTEMPTS_PER_EDGE

SOURCE_CHAIN = DOC / "v16m_source_chain.csv"
PRE_REGISTRATION = DOC / "v16m_pre_registration.csv"
TARGET_SUMMARY = DOC / "v16m_target_summary.csv"
EVENT_LOG = DOC / "v16m_event_log.csv"
EDGE_LOG = DOC / "v16m_fine_dependency_edges.csv"
RUN_SUMMARY = DOC / "v16m_run_summary.csv"
REPLAY_AUDIT = DOC / "v16m_topological_replay_audit.csv"
RELABEL_AUDIT = DOC / "v16m_relabel_replay_audit.csv"
DIRECT_RATE_AUDIT = DOC / "v16m_direct_rate_audit.csv"
PRIMARY_RUNS = DOC / "v16m_strict_null_run_summary.csv"
PRIMARY_NULLS = DOC / "v16m_strict_null_distribution.csv"
PRIMARY_AUDIT = DOC / "v16m_strict_null_perturbation_integrity.csv"
EFFECT_GATE = DOC / "v16m_effect_existence_gate.csv"
GROWTH_ROBUSTNESS = DOC / "v16m_growth_robustness.csv"
SCHEDULER_ROBUSTNESS = DOC / "v16m_scheduler_robustness.csv"
LONGER_RUNS = DOC / "v16m_longer_perturbation_run_summary.csv"
LONGER_NULLS = DOC / "v16m_longer_perturbation_distribution.csv"
LONGER_AUDIT = DOC / "v16m_longer_perturbation_integrity.csv"
LONGER_GATE = DOC / "v16m_longer_perturbation_gate.csv"
MAGNITUDE = DOC / "v16m_magnitude_compatibility.csv"
GATE_EVALUATION = DOC / "v16m_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16m_claim_ledger.csv"
REPORT = DOC / "v16m_qualified_sampler_fresh_holdout.md"
RECOMMENDATION = DOC / "v0_16m_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16m.md"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assignments() -> List[Dict[str, Any]]:
    return [
        {
            "growth_seed": growth_seed,
            "run_offset": run_offset,
            "arm": arm,
            "run_seed": v16h.run_seed(growth_seed, run_offset, arm),
        }
        for growth_seed in GROWTH_SEEDS
        for run_offset in RUN_OFFSETS
        for arm in ARMS
    ]


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = [
        ("v16h", "fresh_dynamics_implementation", Path(v16h.__file__)),
        ("v16i", "observable_implementation", Path(v16i.__file__)),
        ("v16j", "strict_null_implementation", Path(v16j.__file__)),
        ("v16k", "replication_semantics", Path(v16k.__file__)),
        ("v16k", "frozen_magnitude_baselines", DOC / "v16k_frozen_magnitude_baselines.csv"),
        ("v16l", "qualification_implementation", Path(v16l.__file__)),
        ("v16l", "qualification_gate", DOC / "v16l_gate_evaluation.csv"),
        ("v16l", "qualification_summary", DOC / "v16l_sampler_qualification.csv"),
    ]
    return [
        {
            "stage": stage,
            "role": role,
            "artifact": path.name,
            "sha256": file_sha256(path),
            "source_pass": 1,
        }
        for stage, role, path in paths
    ]


def spec_payload() -> Dict[str, Any]:
    return {
        "gate": "v16m_qualified_sampler_fresh_holdout",
        "purpose_ref": PURPOSE_REF,
        "target_nodes": TARGET_NODES,
        "steps": STEPS,
        "growth_seeds": list(GROWTH_SEEDS),
        "run_offsets": list(RUN_OFFSETS),
        "arms": list(ARMS),
        "primary_arm": PRIMARY_ARM,
        "excluded_growth_seeds": list(EXCLUDED_GROWTH_SEEDS),
        "observable": "v16i_dyadic_open_causal_interval_spectrum",
        "primary_metric": "full_spectrum_jensen_shannon_effect_ratio",
        "primary_null_family": v16j.NULL_FAMILY,
        "primary_null_replicates": v16j.NULL_REPLICATES,
        "primary_target_swap_multiplier": v16j.TARGET_ACCEPTED_SWAPS_PER_EDGE,
        "longer_null_replicates": v16k.LONGER_NULL_REPLICATES,
        "longer_target_swap_multiplier": v16k.LONGER_TARGET_SWAP_MULTIPLIER,
        "qualified_max_attempts_per_edge": QUALIFIED_MAX_ATTEMPTS_PER_EDGE,
        "effect_thresholds": {
            "min_local_median_effect_ratio": v16j.MIN_LOCAL_MEDIAN_EFFECT_RATIO,
            "min_local_positive_fraction": v16j.MIN_LOCAL_POSITIVE_FRACTION,
            "max_empirical_p": v16j.MAX_EMPIRICAL_P,
            "min_local_p_le_010_fraction": v16j.MIN_LOCAL_P_LE_010_FRACTION,
        },
        "longer_sensitivity_thresholds": {
            "min_median_effect_ratio": v16k.LONGER_MIN_MEDIAN_EFFECT_RATIO,
            "min_positive_fraction": v16k.LONGER_MIN_POSITIVE_FRACTION,
        },
        "magnitude_model": "four_way_descriptive_factor_two_anchor_compatibility",
        "no_early_stop": True,
        "scope": "new_fresh_finite_event_dag_holdout",
    }


def spec_digest() -> str:
    raw = json.dumps(spec_payload(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def preregistration_rows() -> List[Dict[str, Any]]:
    if not SOURCE_CHAIN.exists():
        raise ValueError("missing v16m source chain")
    return [
        {
            "purpose_ref": PURPOSE_REF,
            "spec_digest": spec_digest(),
            "script_sha256": file_sha256(SCRIPT),
            "v16h_sha256": file_sha256(Path(v16h.__file__)),
            "v16j_sha256": file_sha256(Path(v16j.__file__)),
            "v16k_sha256": file_sha256(Path(v16k.__file__)),
            "v16l_sha256": file_sha256(Path(v16l.__file__)),
            "source_chain_sha256": file_sha256(SOURCE_CHAIN),
            "target_nodes": TARGET_NODES,
            "steps": STEPS,
            **assignment,
            "primary_null_replicates": v16j.NULL_REPLICATES,
            "primary_target_swap_multiplier": v16j.TARGET_ACCEPTED_SWAPS_PER_EDGE,
            "longer_null_replicates": v16k.LONGER_NULL_REPLICATES,
            "longer_target_swap_multiplier": v16k.LONGER_TARGET_SWAP_MULTIPLIER,
            "qualified_max_attempts_per_edge": QUALIFIED_MAX_ATTEMPTS_PER_EDGE,
            "formal_history_generated_after_freeze": 1,
        }
        for assignment in assignments()
    ]


def prepare() -> None:
    qualification = v16i.read_csv(DOC / "v16l_gate_evaluation.csv")
    overall = next(row["status"] for row in qualification if row["gate"] == "v16l_overall")
    if overall != "sampler_attempt_budget_qualified_for_new_holdout":
        raise ValueError("v16m requires qualified v16l sampler")
    if set(GROWTH_SEEDS) & set(EXCLUDED_GROWTH_SEEDS):
        raise ValueError("v16m formal seeds overlap prior or quarantined seeds")
    if shutil.disk_usage(ROOT).free < v16k.MIN_FREE_BYTES:
        raise RuntimeError("v16m preflight requires at least 250 MiB free")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    rows = preregistration_rows()
    v16i.write_csv(PRE_REGISTRATION, rows)
    print(f"[v16m] prepared runs={len(rows)} digest={spec_digest()}")


def load_and_verify_preregistration() -> List[Dict[str, str]]:
    observed = v16i.read_csv(PRE_REGISTRATION)
    expected = [{key: str(value) for key, value in row.items()} for row in preregistration_rows()]
    if observed != expected:
        raise ValueError("v16m preregistration changed")
    frozen_sources = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current_sources = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen_sources != current_sources:
        raise ValueError("v16m source chain changed")
    return observed


def v16m_dag(assignment: Mapping[str, Any], events: Sequence[Mapping[str, Any]], dependency_dag: Any) -> v16i.RunDAG:
    source = v16k.run_dag_from_history(assignment, events, dependency_dag)
    return v16i.RunDAG(
        stage="v16m",
        target_nodes=source.target_nodes,
        growth_seed=source.growth_seed,
        run_offset=source.run_offset,
        arm=source.arm,
        run_seed=source.run_seed,
        predecessors=source.predecessors,
        depths=source.depths,
        indegrees=source.indegrees,
    )


def longer_gate_row(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    result = dict(v16k.longer_gate_row(rows))
    result["stage"] = "v16m"
    return result


def magnitude_row(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    result = dict(v16k.magnitude_row(rows))
    result["stage"] = "v16m"
    return result


def gate_rows(
    target_rows: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    replay_rows: Sequence[Mapping[str, Any]],
    relabel_rows: Sequence[Mapping[str, Any]],
    direct_rows: Sequence[Mapping[str, Any]],
    primary_audits: Sequence[Mapping[str, Any]],
    local: Mapping[str, Any],
    longer_audits: Sequence[Mapping[str, Any]],
    longer: Mapping[str, Any],
    magnitude: Mapping[str, Any],
) -> Tuple[List[Dict[str, Any]], str]:
    target_pass = len(target_rows) == 1 and int(float(target_rows[0]["mean_initial_nodes"])) == TARGET_NODES
    history_pass = len(run_rows) == 12 and all(
        int(row["n_events"]) == STEPS and int(row["invalid_events"]) == 0
        and int(row["fine_acyclic"]) == 1 and int(row["fine_edge_witness_errors"]) == 0
        for row in run_rows
    )
    replay_pass = len(replay_rows) == 24 and all(
        int(row["topological_order_valid"]) and int(row["context_failures"]) == 0 and int(row["final_structure_equal"])
        for row in replay_rows
    )
    relabel_pass = len(relabel_rows) == 12 and all(int(row["relabel_pass"]) for row in relabel_rows)
    direct_pass = len(direct_rows) == 12 and all(int(row["direct_log_parity_pass"]) for row in direct_rows)
    primary_integrity = len(primary_audits) == 384 and all(int(row["null_integrity_pass"]) for row in primary_audits)
    longer_integrity = len(longer_audits) == 192 and all(int(row["perturbation_integrity_pass"]) for row in longer_audits)
    instrumentation = all((target_pass, history_pass, replay_pass, relabel_pass, direct_pass, primary_integrity, longer_integrity))
    existence = int(local["local_gate_pass"]) == 1
    longer_consistency = int(longer["longer_perturbation_consistency_pass"]) == 1
    if not instrumentation:
        overall = "v16m_qualified_sampler_instrumentation_failed"
    elif not existence:
        overall = "fresh_strict_null_spectrum_contrast_not_replicated"
    elif not longer_consistency:
        overall = "fresh_spectrum_contrast_inconclusive_under_longer_perturbation"
    else:
        overall = "fresh_strict_null_spectrum_contrast_replicated_with_qualified_sampler"
    rows = [
        {"gate": "fresh_history_integrity", "status": "pass" if target_pass and history_pass and replay_pass and relabel_pass and direct_pass else "fail", "observed": f"runs={len(run_rows)};events={sum(int(row['n_events']) for row in run_rows)};replays={len(replay_rows)}", "required": "runs=12;events=36864;replays=24", "decision": "continue" if target_pass and history_pass and replay_pass and relabel_pass and direct_pass else "repair"},
        {"gate": "qualified_primary_perturbation_integrity", "status": "pass" if primary_integrity else "fail", "observed": f"{sum(int(row['null_integrity_pass']) for row in primary_audits)}/{len(primary_audits)}", "required": "384/384", "decision": "continue" if primary_integrity else "inconclusive"},
        {"gate": "fresh_effect_existence", "status": "pass" if existence else "fail", "observed": f"median={float(local['median_js_effect_ratio']):.6f};positive={float(local['positive_fraction']):.6f};p_le_010={float(local['p_le_010_fraction']):.6f}", "required": "median>=2;positive>=5/6;p_le_010>=1/2", "decision": "replicated" if existence else "not_replicated"},
        {"gate": "qualified_longer_perturbation_integrity", "status": "pass" if longer_integrity else "fail", "observed": f"{sum(int(row['perturbation_integrity_pass']) for row in longer_audits)}/{len(longer_audits)}", "required": "192/192", "decision": "continue" if longer_integrity else "inconclusive"},
        {"gate": "longer_perturbation_consistency", "status": "pass" if longer_consistency else "fail", "observed": f"median={float(longer['median_js_effect_ratio']):.6f};positive={float(longer['positive_fraction']):.6f}", "required": "median>=1;positive>=5/6", "decision": "consistent" if longer_consistency else "inconclusive"},
        {"gate": "magnitude_compatibility", "status": "descriptive", "observed": magnitude["magnitude_compatibility_class"], "required": "not_a_confirmatory_gate", "decision": magnitude["magnitude_compatibility_class"]},
        {"gate": "v16m_overall", "status": overall, "observed": f"instrumentation={int(instrumentation)};existence={int(existence)};longer={int(longer_consistency)}", "required": "1;1;1", "decision": overall},
    ]
    return rows, overall


def claim_rows(overall: str, magnitude: Mapping[str, Any]) -> List[Dict[str, Any]]:
    replicated = overall == "fresh_strict_null_spectrum_contrast_replicated_with_qualified_sampler"
    return [
        {"claim_id": "C1", "claim": "The v16j finite event-DAG interval-spectrum contrast replicated on a second formal fresh-history holdout with the v16l-qualified sampler.", "status": "supported" if replicated else "unsupported", "evidence": "v16m_effect_existence_gate.csv;v16m_longer_perturbation_gate.csv", "scope_limit": "conditional on this qualified perturbation sampler"},
        {"claim_id": "C2", "claim": "The fresh effect magnitude is descriptively compatible with one or both prior strict-null anchors.", "status": "supported" if magnitude["magnitude_compatibility_class"] != "outside_factor_two_compatibility_envelope" else "unsupported", "evidence": "v16m_magnitude_compatibility.csv", "scope_limit": "descriptive point-anchor bands, not universal stability"},
        {"claim_id": "C3", "claim": "The qualified sampler is uniform, converged, stationary, independent, or representative over the constrained DAG space.", "status": "unsupported", "evidence": "none", "scope_limit": "completion and integrity do not prove sampler distribution"},
        {"claim_id": "C4", "claim": "The contrast is independent of event-family and read/write-resource wiring.", "status": "unsupported", "evidence": "none", "scope_limit": "requires a separately calibrated coarse resource-aware null"},
        {"claim_id": "C5", "claim": "The interval spectrum establishes dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particles, or entanglement.", "status": "unsupported", "evidence": "none", "scope_limit": "finite event-DAG structural diagnostic only"},
    ]


def build_report(
    summaries: Sequence[Mapping[str, Any]],
    local: Mapping[str, Any],
    longer: Mapping[str, Any],
    magnitude: Mapping[str, Any],
    growth: Sequence[Mapping[str, Any]],
    scheduler: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16m qualified-sampler fresh holdout",
        "",
        f"Status: `{overall}`.",
        "",
        "v16m is a new 12-run holdout. It uses new histories and the v16l-qualified 240-attempt safety ceiling while retaining the v16j/v16k observable, null targets, null counts, stopping conditions, and scientific thresholds.",
        "",
        f"Specification digest: `{spec_digest()}`.",
        "",
        "## Per-run primary results",
        "",
    ]
    lines.extend(v16i.table(summaries, ("growth_seed", "run_offset", "arm", "observed_js_to_null_center", "null_median_leave_one_out_js", "js_effect_ratio", "empirical_p_upper", "tail_mass_ge_8_delta")))
    lines.extend(["", "## Separate outcomes", ""])
    lines.extend(v16i.table([local], ("n_runs", "median_js_effect_ratio", "positive_fraction", "p_le_010_fraction", "local_gate_pass")))
    lines.append("")
    lines.extend(v16i.table([longer], ("n_runs", "target_swap_multiplier", "median_js_effect_ratio", "positive_fraction", "perturbation_integrity_pass", "longer_perturbation_consistency_pass")))
    lines.append("")
    lines.extend(v16i.table([magnitude], ("fresh_median_js_effect_ratio", "bootstrap_median_ci_low", "bootstrap_median_ci_high", "fresh_over_v16d", "fresh_over_v16h", "magnitude_compatibility_class")))
    lines.extend(["", "Growth and scheduler rows remain diagnostics.", ""])
    lines.extend(v16i.table(growth, ("group_field", "group_value", "n_runs", "median_js_effect_ratio", "positive_fraction", "group_pass")))
    lines.append("")
    lines.extend(v16i.table(scheduler, ("group_field", "group_value", "n_runs", "median_js_effect_ratio", "positive_fraction", "group_pass")))
    lines.extend(["", "## Gates", ""])
    lines.extend(v16i.table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "A replication supports a repeatable finite event-DAG interval-spectrum contrast conditional on this perturbation sampler. The null preserves scheduler order, exact direct in/out-degree, exact causal depth/profile, and the global dyadic parent-age-bin histogram. The higher attempt ceiling establishes completion, not convergence or uniform sampling.",
        "",
        "Tail-mass deltas must be read by sign; the primary endpoint is the full-spectrum contrast, not an assumed increase in large intervals.",
        "",
        "This result does not establish dimension, manifoldlikeness, Lorentz invariance, spacetime, continuum behavior, particles, entanglement, or a physical causal law.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    prereg = load_and_verify_preregistration()
    if shutil.disk_usage(ROOT).free < v16k.MIN_FREE_BYTES:
        raise RuntimeError("v16m run preflight requires at least 250 MiB free")
    adapter = v16ac.LocalSeedClockAdapter(v16h.frozen_local_rate())
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(
        ensembles, v10e.recommended_regime("fast_balanced"), list(GROWTH_SEEDS)
    )
    target_rows = v10e.summarize_bases(base_rows)
    ensemble_name = ensembles[0].name
    params = v16a.anchor_params()

    events_all: List[Dict[str, Any]] = []
    edges_all: List[Dict[str, Any]] = []
    run_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    relabel_rows: List[Dict[str, Any]] = []
    direct_rows: List[Dict[str, Any]] = []
    primary_runs: List[Dict[str, Any]] = []
    primary_nulls: List[Dict[str, Any]] = []
    primary_audits: List[Dict[str, Any]] = []
    longer_runs: List[Dict[str, Any]] = []
    longer_nulls: List[Dict[str, Any]] = []
    longer_audits: List[Dict[str, Any]] = []

    for index, assignment in enumerate(prereg, start=1):
        base = base_states[(ensemble_name, int(assignment["growth_seed"]))]
        events, edges, rates, run_row, replays, relabel, dependency_dag = v16h.run_assignment(
            base, assignment, params, adapter
        )
        direct = v16h.direct_rate_audit(base, events, rates, run_row, v16h.frozen_local_rate())
        if not int(direct["direct_log_parity_pass"]):
            raise RuntimeError("v16m direct-rate parity failed")
        dag = v16m_dag(assignment, events, dependency_dag)
        primary, p_nulls, p_audits = v16l.with_qualified_ceiling(v16j.analyze_run, dag)
        longer, l_nulls, l_audits = v16l.with_qualified_ceiling(
            v16k.analyze_perturbation_family,
            dag,
            label="degree_depth_global_age_bin_double_edge_swap_longer_010",
            replicates=v16k.LONGER_NULL_REPLICATES,
            target_swap_multiplier=v16k.LONGER_TARGET_SWAP_MULTIPLIER,
        )
        events_all.extend(events)
        edges_all.extend(edges)
        run_rows.append(run_row)
        replay_rows.extend(replays)
        relabel_rows.append(relabel)
        direct_rows.append(direct)
        primary_runs.append(primary)
        primary_nulls.extend(p_nulls)
        primary_audits.extend(p_audits)
        longer_runs.append(longer)
        longer_nulls.extend(l_nulls)
        longer_audits.extend(l_audits)
        print(f"[v16m] runs={index}/{len(prereg)} arm={assignment['arm']} primary_ratio={float(primary['js_effect_ratio']):.6f} longer_ratio={float(longer['js_effect_ratio']):.6f}")

    local = v16j.local_gate_row(primary_runs, "v16m")
    growth = v16i.aggregate_rows(primary_runs, "growth_seed", v16j.GROUP_MIN_MEDIAN_EFFECT_RATIO, v16j.GROUP_MIN_POSITIVE_FRACTION)
    scheduler = v16i.aggregate_rows(primary_runs, "arm", v16j.GROUP_MIN_MEDIAN_EFFECT_RATIO, v16j.GROUP_MIN_POSITIVE_FRACTION)
    longer = longer_gate_row(longer_runs)
    magnitude = magnitude_row(primary_runs)
    gates, overall = gate_rows(
        target_rows, run_rows, replay_rows, relabel_rows, direct_rows,
        primary_audits, local, longer_audits, longer, magnitude,
    )

    v16i.write_csv(TARGET_SUMMARY, target_rows)
    v16i.write_csv(EVENT_LOG, events_all)
    v16i.write_csv(EDGE_LOG, edges_all)
    v16i.write_csv(RUN_SUMMARY, run_rows)
    v16i.write_csv(REPLAY_AUDIT, replay_rows)
    v16i.write_csv(RELABEL_AUDIT, relabel_rows)
    v16i.write_csv(DIRECT_RATE_AUDIT, direct_rows)
    v16i.write_csv(PRIMARY_RUNS, primary_runs)
    v16i.write_csv(PRIMARY_NULLS, primary_nulls)
    v16i.write_csv(PRIMARY_AUDIT, primary_audits)
    v16i.write_csv(EFFECT_GATE, [local])
    v16i.write_csv(GROWTH_ROBUSTNESS, growth)
    v16i.write_csv(SCHEDULER_ROBUSTNESS, scheduler)
    v16i.write_csv(LONGER_RUNS, longer_runs)
    v16i.write_csv(LONGER_NULLS, longer_nulls)
    v16i.write_csv(LONGER_AUDIT, longer_audits)
    v16i.write_csv(LONGER_GATE, [longer])
    v16i.write_csv(MAGNITUDE, [magnitude])
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claim_rows(overall, magnitude))
    REPORT.write_text(build_report(primary_runs, local, longer, magnitude, growth, scheduler, gates, overall), encoding="utf-8")
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.16m\n\n"
        f"Status: `{overall}`.\n\n"
        f"Primary median ratio: `{float(local['median_js_effect_ratio']):.6f}`.\n\n"
        f"Longer median ratio: `{float(longer['median_js_effect_ratio']):.6f}`.\n\n"
        f"Magnitude class: `{magnitude['magnitude_compatibility_class']}`.\n\n"
        "If replicated, the next mechanism gate is calibration of a coarse event-family/resource-stratified null. This still does not authorize a dimension or geometry claim.\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.16m\n\n"
        f"Statusen er `{overall}`. Dette er en ny test paa helt nye simuleringer med en teknisk kvalifisert kontrollsampler. En positiv status betyr at et avgrenset grafmonster gjentar seg; den betyr ikke at romtid, partikler eller naturlover er funnet.\n",
        encoding="utf-8",
    )
    print(f"[v16m] complete overall={overall} magnitude={magnitude['magnitude_compatibility_class']}")


def verify_outputs() -> None:
    load_and_verify_preregistration()
    runs = v16i.read_csv(RUN_SUMMARY)
    primary = v16i.read_csv(PRIMARY_AUDIT)
    longer = v16i.read_csv(LONGER_AUDIT)
    gates = v16i.read_csv(GATE_EVALUATION)
    if len(runs) != 12 or len(v16i.read_csv(EVENT_LOG)) != 12 * STEPS:
        raise ValueError("v16m history row counts failed")
    if len(primary) != 384 or not all(int(row["null_integrity_pass"]) for row in primary):
        raise ValueError("v16m primary integrity failed")
    if len(longer) != 192 or not all(int(row["perturbation_integrity_pass"]) for row in longer):
        raise ValueError("v16m longer integrity failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16m_overall")
    allowed = {
        "v16m_qualified_sampler_instrumentation_failed",
        "fresh_strict_null_spectrum_contrast_not_replicated",
        "fresh_spectrum_contrast_inconclusive_under_longer_perturbation",
        "fresh_strict_null_spectrum_contrast_replicated_with_qualified_sampler",
    }
    if overall not in allowed:
        raise ValueError("v16m unknown status")
    for path in (PRIMARY_RUNS, PRIMARY_NULLS, PRIMARY_AUDIT, LONGER_RUNS, LONGER_NULLS, LONGER_AUDIT, MAGNITUDE):
        for row in v16i.read_csv(path):
            if any(str(value).lower() in {"nan", "inf", "-inf"} for value in row.values()):
                raise ValueError(f"v16m non-finite value in {path.name}")
    print(f"[v16m] output verification pass overall={overall}")


def self_test() -> None:
    rows = assignments()
    if len(rows) != 12 or len({row["run_seed"] for row in rows}) != 12:
        raise AssertionError("v16m assignments failed")
    if set(GROWTH_SEEDS) & set(EXCLUDED_GROWTH_SEEDS):
        raise AssertionError("v16m seeds overlap excluded histories")
    if QUALIFIED_MAX_ATTEMPTS_PER_EDGE != 240:
        raise AssertionError("v16m sampler ceiling changed")
    print(f"[v16m] self-test pass seeds={GROWTH_SEEDS} offsets={RUN_OFFSETS}")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16m qualified-sampler fresh holdout")
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
