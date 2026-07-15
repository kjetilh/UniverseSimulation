#!/usr/bin/env python3
"""v16s: fresh-history holdout under the qualified event-footprint null."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any, Dict, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v16a_disjoint_event_commutation_gate as v16a
import relational_universe_v16ac_local_seed_adapter_gate as v16ac
import relational_universe_v16h_fresh_rate_logged_mechanism_holdout as v16h
import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16j_interval_strict_null_gate as v16j
import relational_universe_v16k_fresh_strict_null_replication as v16k
import relational_universe_v16m_qualified_sampler_fresh_holdout as v16m
import relational_universe_v16n_coarse_event_resource_null_calibration as v16n
import relational_universe_v16q_event_footprint_null_calibration as v16q
import relational_universe_v16r_event_footprint_sensitivity_gate as v16r


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

TARGET_NODES = v16m.TARGET_NODES
STEPS = v16m.STEPS
PRIMARY_ARM = v16m.PRIMARY_ARM
GROWTH_SEEDS = tuple(
    9000 + v16i.stable_seed("v16s", "fresh-growth", index) % 3000
    for index in range(2)
)
RUN_OFFSETS = tuple(
    120000 + v16i.stable_seed("v16s", "fresh-offset", index) % 9000
    for index in range(3)
)
EXCLUDED_GROWTH_SEEDS = tuple(sorted({
    5203,
    5389,
    *v16k.GROWTH_SEEDS,
    *v16m.GROWTH_SEEDS,
    *v16n.GROWTH_SEEDS,
}))
QUALIFIED_MAX_ATTEMPTS_PER_EDGE = v16r.QUALIFIED_MAX_ATTEMPTS_PER_EDGE
PRIMARY_REPLICATES = v16r.PRIMARY_REPLICATES
PRIMARY_SWAP_MULTIPLIER = v16r.PRIMARY_SWAP_MULTIPLIER
LONGER_REPLICATES = v16r.LONGER_REPLICATES
LONGER_SWAP_MULTIPLIER = v16r.LONGER_SWAP_MULTIPLIER

SOURCE_CHAIN = DOC / "v16s_source_chain.csv"
PRE_REGISTRATION = DOC / "v16s_pre_registration.csv"
TARGET_SUMMARY = DOC / "v16s_target_summary.csv"
EVENT_LOG = DOC / "v16s_event_log.csv"
EDGE_LOG = DOC / "v16s_fine_dependency_edges.csv"
RUN_SUMMARY = DOC / "v16s_run_summary.csv"
REPLAY_AUDIT = DOC / "v16s_topological_replay_audit.csv"
RELABEL_AUDIT = DOC / "v16s_relabel_replay_audit.csv"
DIRECT_RATE_AUDIT = DOC / "v16s_direct_rate_audit.csv"
PRIMARY_RUNS = DOC / "v16s_event_footprint_run_summary.csv"
PRIMARY_NULLS = DOC / "v16s_event_footprint_null_distribution.csv"
PRIMARY_AUDIT = DOC / "v16s_event_footprint_perturbation_integrity.csv"
EFFECT_GATE = DOC / "v16s_effect_existence_gate.csv"
LONGER_RUNS = DOC / "v16s_longer_footprint_run_summary.csv"
LONGER_NULLS = DOC / "v16s_longer_footprint_null_distribution.csv"
LONGER_AUDIT = DOC / "v16s_longer_footprint_perturbation_integrity.csv"
LONGER_GATE = DOC / "v16s_longer_footprint_gate.csv"
ANCHOR_COMPARISON = DOC / "v16s_anchor_comparison.csv"
GATE_EVALUATION = DOC / "v16s_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16s_claim_ledger.csv"
REPORT = DOC / "v16s_fresh_event_footprint_holdout.md"
RECOMMENDATION = DOC / "v0_16s_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16s.md"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assignments() -> List[Dict[str, Any]]:
    return [
        {
            "growth_seed": growth_seed,
            "run_offset": run_offset,
            "arm": PRIMARY_ARM,
            "run_seed": v16h.run_seed(growth_seed, run_offset, PRIMARY_ARM),
        }
        for growth_seed in GROWTH_SEEDS
        for run_offset in RUN_OFFSETS
    ]


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = [
        ("v16h", "fresh_dynamics_implementation", Path(v16h.__file__)),
        ("v16i", "observable_implementation", Path(v16i.__file__)),
        ("v16q", "qualified_footprint_sampler", Path(v16q.__file__)),
        ("v16q", "sampler_qualification", v16q.QUALIFICATION),
        ("v16r", "posthoc_sensitivity_implementation", Path(v16r.__file__)),
        ("v16r", "posthoc_gate", v16r.GATE_EVALUATION),
        ("v16r", "posthoc_effect", v16r.EFFECT_GATE),
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
        "gate": "v16s_fresh_event_footprint_holdout",
        "purpose_ref": PURPOSE_REF,
        "scope": "new_fresh_histories_with_preselected_footprint_null",
        "target_nodes": TARGET_NODES,
        "steps": STEPS,
        "growth_seeds": list(GROWTH_SEEDS),
        "run_offsets": list(RUN_OFFSETS),
        "arm": PRIMARY_ARM,
        "excluded_growth_seeds": list(EXCLUDED_GROWTH_SEEDS),
        "observable": "v16i_dyadic_open_causal_interval_spectrum",
        "primary_metric": "full_spectrum_jensen_shannon_effect_ratio",
        "null_family": v16q.NULL_FAMILY,
        "qualified_max_attempts_per_edge": QUALIFIED_MAX_ATTEMPTS_PER_EDGE,
        "primary_replicates": PRIMARY_REPLICATES,
        "primary_swap_multiplier": PRIMARY_SWAP_MULTIPLIER,
        "longer_replicates": LONGER_REPLICATES,
        "longer_swap_multiplier": LONGER_SWAP_MULTIPLIER,
        "effect_thresholds": {
            "min_median_effect_ratio": v16j.MIN_LOCAL_MEDIAN_EFFECT_RATIO,
            "min_positive_fraction": v16j.MIN_LOCAL_POSITIVE_FRACTION,
            "max_empirical_p": v16j.MAX_EMPIRICAL_P,
            "min_p_le_010_fraction": v16j.MIN_LOCAL_P_LE_010_FRACTION,
        },
        "longer_thresholds": {
            "min_median_effect_ratio": v16k.LONGER_MIN_MEDIAN_EFFECT_RATIO,
            "min_positive_fraction": v16k.LONGER_MIN_POSITIVE_FRACTION,
        },
        "anchor_comparison": "descriptive_only",
        "no_early_stop": True,
    }


def spec_digest() -> str:
    raw = json.dumps(spec_payload(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def preregistration_rows() -> List[Dict[str, Any]]:
    return [{
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "script_sha256": file_sha256(SCRIPT),
        "source_chain_sha256": file_sha256(SOURCE_CHAIN),
        "target_nodes": TARGET_NODES,
        "steps": STEPS,
        **assignment,
        "primary_replicates": PRIMARY_REPLICATES,
        "primary_swap_multiplier": PRIMARY_SWAP_MULTIPLIER,
        "longer_replicates": LONGER_REPLICATES,
        "longer_swap_multiplier": LONGER_SWAP_MULTIPLIER,
        "qualified_max_attempts_per_edge": QUALIFIED_MAX_ATTEMPTS_PER_EDGE,
        "formal_history_generated_after_freeze": 1,
    } for assignment in assignments()]


def prepare() -> None:
    v16r.verify_outputs()
    if set(GROWTH_SEEDS) & set(EXCLUDED_GROWTH_SEEDS):
        raise ValueError("v16s fresh seeds overlap prior or quarantined seeds")
    if len(set(GROWTH_SEEDS)) != len(GROWTH_SEEDS) or len(set(RUN_OFFSETS)) != len(RUN_OFFSETS):
        raise ValueError("v16s assignments are not unique")
    if shutil.disk_usage(ROOT).free < v16k.MIN_FREE_BYTES:
        raise RuntimeError("v16s preflight requires at least 250 MiB free")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, preregistration_rows())
    print(f"[v16s] prepared runs={len(assignments())} digest={spec_digest()}")


def verify_frozen_sources() -> List[Dict[str, str]]:
    rows = v16i.read_csv(PRE_REGISTRATION)
    expected = [{key: str(value) for key, value in row.items()} for row in preregistration_rows()]
    if rows != expected:
        raise ValueError("v16s preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v16s source chain changed")
    return rows


def fresh_dag(
    assignment: Mapping[str, Any],
    events: Sequence[Mapping[str, Any]],
    dependency_dag: Any,
) -> v16i.RunDAG:
    source = v16k.run_dag_from_history(assignment, events, dependency_dag)
    return v16i.RunDAG(
        stage="v16s",
        target_nodes=source.target_nodes,
        growth_seed=source.growth_seed,
        run_offset=source.run_offset,
        arm=source.arm,
        run_seed=source.run_seed,
        predecessors=source.predecessors,
        depths=source.depths,
        indegrees=source.indegrees,
    )


def anchor_rows(fresh_median: float) -> List[Dict[str, Any]]:
    anchors = [
        ("v16m_strict_null_fresh_holdout", float(v16i.read_csv(v16m.EFFECT_GATE)[0]["median_js_effect_ratio"])),
        ("v16r_footprint_null_posthoc", float(v16i.read_csv(v16r.EFFECT_GATE)[0]["median_js_effect_ratio"])),
        ("v16s_footprint_null_fresh_holdout", fresh_median),
    ]
    return [{
        "anchor": label,
        "median_js_effect_ratio": value,
        "fresh_v16s_over_anchor": fresh_median / max(value, v16j.EPSILON),
        "confirmatory_gate": 0,
        "interpretation": "descriptive_only",
    } for label, value in anchors]


def build_report(
    primary: Sequence[Mapping[str, Any]],
    local: Mapping[str, Any],
    longer: Mapping[str, Any],
    anchors: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16s fresh event-footprint holdout",
        "",
        f"Status: `{overall}`.",
        "",
        "V16s generated six new exposure-matched histories after freezing the v16q-qualified event-footprint null, assignments, null counts, thresholds, and source hashes. It is the first fresh-history confirmatory use of this null family.",
        "",
        f"Specification digest: `{spec_digest()}`.",
        "",
        "## Per-run primary results",
        "",
    ]
    lines.extend(v16i.table(primary, (
        "growth_seed", "run_offset", "js_effect_ratio", "empirical_p_upper",
        "tail_mass_ge_8_delta", "min_actual_resource_conflict_edge_fraction",
        "all_perturbation_integrity_pass",
    )))
    lines.extend(["", "## Confirmatory aggregates", ""])
    lines.extend(v16i.table([local], (
        "n_runs", "median_js_effect_ratio", "positive_fraction", "p_le_010_fraction", "local_gate_pass",
    )))
    lines.append("")
    lines.extend(v16i.table([longer], (
        "n_runs", "median_js_effect_ratio", "positive_fraction",
        "perturbation_integrity_pass", "longer_perturbation_consistency_pass",
    )))
    lines.extend(["", "## Descriptive anchors", ""])
    lines.extend(v16i.table(anchors, (
        "anchor", "median_js_effect_ratio", "fresh_v16s_over_anchor", "interpretation",
    )))
    lines.extend(["", "## Gates", ""])
    lines.extend(v16i.table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "Replication supports a fresh finite event-DAG interval-spectrum contrast conditional on the qualified coarse footprint sampler. It does not establish sampler irreducibility, convergence, stationarity, representativeness, or uniformity, and the null does not preserve concrete resource identity.",
        "",
        "The primary endpoint is full-spectrum contrast. Tail-mass deltas must be read by sign and are not assumed positive.",
        "",
        "No dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particle, entanglement, or physical-law claim is authorized.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    prereg = verify_frozen_sources()
    if shutil.disk_usage(ROOT).free < v16k.MIN_FREE_BYTES:
        raise RuntimeError("v16s run preflight requires at least 250 MiB free")
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
    primary: List[Dict[str, Any]] = []
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
            raise RuntimeError("v16s direct-rate parity failed")
        dag = fresh_dag(assignment, events, dependency_dag)
        metadata, metadata_audit = v16n.event_metadata(events)
        if not int(metadata_audit["event_id_mapping_total_pass"]):
            raise RuntimeError("v16s event metadata mapping failed")
        summary, nulls, audits = v16r.analyze_family(
            dag,
            metadata,
            label=f"{v16q.NULL_FAMILY}_primary_0075",
            replicates=PRIMARY_REPLICATES,
            target_swap_multiplier=PRIMARY_SWAP_MULTIPLIER,
        )
        longer, l_nulls, l_audits = v16r.analyze_family(
            dag,
            metadata,
            label=f"{v16q.NULL_FAMILY}_longer_0100",
            replicates=LONGER_REPLICATES,
            target_swap_multiplier=LONGER_SWAP_MULTIPLIER,
        )
        events_all.extend(events)
        edges_all.extend(edges)
        run_rows.append(run_row)
        replay_rows.extend(replays)
        relabel_rows.append(relabel)
        direct_rows.append(direct)
        primary.append(summary)
        primary_nulls.extend(nulls)
        primary_audits.extend(audits)
        longer_runs.append(longer)
        longer_nulls.extend(l_nulls)
        longer_audits.extend(l_audits)
        print(
            f"[v16s] runs={index}/{len(prereg)} primary={summary['js_effect_ratio']:.6f} "
            f"longer={longer['js_effect_ratio']:.6f}"
        )

    local = v16j.local_gate_row(primary, "v16s")
    longer_gate = dict(v16k.longer_gate_row(longer_runs))
    longer_gate["stage"] = "v16s"
    anchors = anchor_rows(float(local["median_js_effect_ratio"]))
    target_pass = (
        len(target_rows) == 1
        and int(float(target_rows[0]["mean_initial_nodes"])) == TARGET_NODES
        and int(target_rows[0]["separated_from_prev"]) == 1
    )
    history_pass = (
        target_pass
        and len(run_rows) == 6
        and all(
            int(row["n_events"]) == STEPS
            and int(row["invalid_events"]) == 0
            and int(row["fine_acyclic"]) == 1
            and int(row["fine_edge_witness_errors"]) == 0
            and int(row["topological_replay_failures"]) == 0
            and int(row["relabel_pass"]) == 1
            for row in run_rows
        )
        and len(replay_rows) == 12
        and all(int(row["direct_log_parity_pass"]) for row in direct_rows)
    )
    primary_integrity = len(primary_audits) == 192 and all(
        int(row["perturbation_integrity_pass"]) for row in primary_audits
    )
    longer_integrity = len(longer_audits) == 96 and all(
        int(row["perturbation_integrity_pass"]) for row in longer_audits
    )
    existence = int(local["local_gate_pass"]) == 1
    longer_consistency = int(longer_gate["longer_perturbation_consistency_pass"]) == 1
    if not all((history_pass, primary_integrity, longer_integrity)):
        overall = "v16s_fresh_event_footprint_instrumentation_failed"
    elif not existence:
        overall = "v16s_fresh_event_footprint_spectrum_contrast_not_replicated"
    elif not longer_consistency:
        overall = "v16s_fresh_event_footprint_spectrum_inconclusive_under_longer_perturbation"
    else:
        overall = "v16s_fresh_event_footprint_spectrum_contrast_replicated"
    gates = [
        {
            "gate": "fresh_history_integrity",
            "status": "pass" if history_pass else "fail",
            "observed": f"runs={len(run_rows)};events={len(events_all)};replays={len(replay_rows)}",
            "required": "runs=6;events=18432;replays=12",
            "decision": "continue" if history_pass else "repair",
        },
        {
            "gate": "qualified_primary_footprint_perturbation_integrity",
            "status": "pass" if primary_integrity else "fail",
            "observed": f"{sum(int(row['perturbation_integrity_pass']) for row in primary_audits)}/{len(primary_audits)}",
            "required": "192/192",
            "decision": "continue" if primary_integrity else "inconclusive",
        },
        {
            "gate": "fresh_footprint_effect_existence",
            "status": "pass" if existence else "fail",
            "observed": f"median={float(local['median_js_effect_ratio']):.6f};positive={float(local['positive_fraction']):.6f};p_le_010={float(local['p_le_010_fraction']):.6f}",
            "required": "median>=2;positive>=5/6;p_le_010>=1/2",
            "decision": "replicated" if existence else "not_replicated",
        },
        {
            "gate": "qualified_longer_footprint_perturbation_integrity",
            "status": "pass" if longer_integrity else "fail",
            "observed": f"{sum(int(row['perturbation_integrity_pass']) for row in longer_audits)}/{len(longer_audits)}",
            "required": "96/96",
            "decision": "continue" if longer_integrity else "inconclusive",
        },
        {
            "gate": "longer_footprint_consistency",
            "status": "pass" if longer_consistency else "fail",
            "observed": f"median={float(longer_gate['median_js_effect_ratio']):.6f};positive={float(longer_gate['positive_fraction']):.6f}",
            "required": "median>=1;positive>=5/6",
            "decision": "consistent" if longer_consistency else "inconclusive",
        },
        {
            "gate": "v16s_overall",
            "status": overall,
            "observed": f"history={int(history_pass)};existence={int(existence)};longer={int(longer_consistency)}",
            "required": "1;1;1",
            "decision": overall,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "The finite event-DAG interval-spectrum contrast replicated on fresh histories under the preselected qualified event-footprint null.",
            "status": "supported" if overall == "v16s_fresh_event_footprint_spectrum_contrast_replicated" else "unsupported",
            "evidence": "v16s_effect_existence_gate.csv;v16s_longer_footprint_gate.csv",
            "scope_limit": "six finite fresh histories conditional on a coarse qualified sampler",
        },
        {
            "claim_id": "C2",
            "claim": "The contrast is independent of concrete resource identity or establishes a causal event mechanism.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "the footprint does not preserve concrete resource identity",
        },
        {
            "claim_id": "C3",
            "claim": "The sampler is uniform, converged, stationary, independent, or representative.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "procedural qualification only",
        },
        {
            "claim_id": "C4",
            "claim": "Dimension, Lorentz symmetry, spacetime, continuum physics, particles, or entanglement were established.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "finite event-DAG structural diagnostic only",
        },
    ]

    v16i.write_csv(TARGET_SUMMARY, target_rows)
    v16i.write_csv(EVENT_LOG, events_all)
    v16i.write_csv(EDGE_LOG, edges_all)
    v16i.write_csv(RUN_SUMMARY, run_rows)
    v16i.write_csv(REPLAY_AUDIT, replay_rows)
    v16i.write_csv(RELABEL_AUDIT, relabel_rows)
    v16i.write_csv(DIRECT_RATE_AUDIT, direct_rows)
    v16i.write_csv(PRIMARY_RUNS, primary)
    v16i.write_csv(PRIMARY_NULLS, primary_nulls)
    v16i.write_csv(PRIMARY_AUDIT, primary_audits)
    v16i.write_csv(EFFECT_GATE, [local])
    v16i.write_csv(LONGER_RUNS, longer_runs)
    v16i.write_csv(LONGER_NULLS, longer_nulls)
    v16i.write_csv(LONGER_AUDIT, longer_audits)
    v16i.write_csv(LONGER_GATE, [longer_gate])
    v16i.write_csv(ANCHOR_COMPARISON, anchors)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    REPORT.write_text(build_report(primary, local, longer_gate, anchors, gates, overall), encoding="utf-8")
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.16s\n\n"
        f"Status: `{overall}`.\n\n"
        f"Primary median ratio: `{float(local['median_js_effect_ratio']):.6f}`.\n\n"
        f"Longer median ratio: `{float(longer_gate['median_js_effect_ratio']):.6f}`.\n\n"
        "This fresh finite-DAG result remains conditional on a coarse sampler and does not authorize a physical geometry claim.\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.16s\n\n"
        f"Statusen er `{overall}`. Denne runden lager helt nye simuleringer og tester dem mot kontrollgrafer som bevarer grove hendelses- og ressursroller. En positiv status er en ny strukturell replikasjon, ikke et funn av romtid eller naturlover.\n",
        encoding="utf-8",
    )
    print(f"[v16s] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    runs = v16i.read_csv(RUN_SUMMARY)
    events = v16i.read_csv(EVENT_LOG)
    primary = v16i.read_csv(PRIMARY_AUDIT)
    longer = v16i.read_csv(LONGER_AUDIT)
    gates = v16i.read_csv(GATE_EVALUATION)
    if len(runs) != 6 or len(events) != 6 * STEPS:
        raise ValueError("v16s fresh history row counts failed")
    if len(primary) != 192 or not all(int(row["perturbation_integrity_pass"]) for row in primary):
        raise ValueError("v16s primary integrity failed")
    if len(longer) != 96 or not all(int(row["perturbation_integrity_pass"]) for row in longer):
        raise ValueError("v16s longer integrity failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16s_overall")
    allowed = {
        "v16s_fresh_event_footprint_instrumentation_failed",
        "v16s_fresh_event_footprint_spectrum_contrast_not_replicated",
        "v16s_fresh_event_footprint_spectrum_inconclusive_under_longer_perturbation",
        "v16s_fresh_event_footprint_spectrum_contrast_replicated",
    }
    if overall not in allowed:
        raise ValueError("v16s unknown status")
    print(f"[v16s] output verification pass overall={overall}")


def self_test() -> None:
    rows = assignments()
    if len(rows) != 6 or len({row["run_seed"] for row in rows}) != 6:
        raise AssertionError("v16s assignments failed")
    if set(GROWTH_SEEDS) & set(EXCLUDED_GROWTH_SEEDS):
        raise AssertionError("v16s seeds overlap excluded histories")
    if QUALIFIED_MAX_ATTEMPTS_PER_EDGE != 60:
        raise AssertionError("v16s qualified ceiling changed")
    print(f"[v16s] self-test pass seeds={GROWTH_SEEDS} offsets={RUN_OFFSETS}")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16s fresh event-footprint holdout")
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
