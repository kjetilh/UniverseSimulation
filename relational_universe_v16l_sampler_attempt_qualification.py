#!/usr/bin/env python3
"""v16l: qualify a larger strict-null attempt ceiling on saved v16k DAGs.

The scientific observable, swap targets, stopping conditions, null counts, and
seeds are unchanged.  Only the safety ceiling increases from 60 to 240
attempts per direct edge.  Qualification depends exclusively on perturbation
completion, preservation, and uniqueness.  Recomputed interval statistics are
post-hoc sensitivity diagnostics and cannot rehabilitate frozen v16k.
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
import relational_universe_v16k_fresh_strict_null_replication as v16k


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"
QUALIFIED_MAX_ATTEMPTS_PER_EDGE = 240
SOURCE_MAX_ATTEMPTS_PER_EDGE = v16j.MAX_ATTEMPTS_PER_EDGE

SOURCE_CHAIN = DOC / "v16l_source_chain.csv"
PRE_REGISTRATION = DOC / "v16l_pre_registration.csv"
PRIMARY_RUNS = DOC / "v16l_posthoc_primary_run_summary.csv"
PRIMARY_NULLS = DOC / "v16l_posthoc_primary_null_distribution.csv"
PRIMARY_AUDIT = DOC / "v16l_primary_qualification_integrity.csv"
LONGER_RUNS = DOC / "v16l_posthoc_longer_run_summary.csv"
LONGER_NULLS = DOC / "v16l_posthoc_longer_null_distribution.csv"
LONGER_AUDIT = DOC / "v16l_longer_qualification_integrity.csv"
QUALIFICATION = DOC / "v16l_sampler_qualification.csv"
SENSITIVITY = DOC / "v16l_posthoc_spectrum_sensitivity.csv"
GATE_EVALUATION = DOC / "v16l_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16l_claim_ledger.csv"
REPORT = DOC / "v16l_sampler_attempt_qualification.md"
RECOMMENDATION = DOC / "v0_16l_operativ_anbefaling.md"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_key(row: Mapping[str, Any]) -> Tuple[int, int, str, int]:
    return (
        int(row["growth_seed"]),
        int(row["run_offset"]),
        str(row["arm"]),
        int(row["run_seed"]),
    )


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = [
        ("v16j", "strict_null_implementation", Path(v16j.__file__)),
        ("v16k", "fresh_replication_implementation", Path(v16k.__file__)),
        ("v16k", "frozen_gate", DOC / "v16k_gate_evaluation.csv"),
        ("v16k", "interpretation_audit", DOC / "v16k_interpretation_audit.csv"),
        ("v16k", "event_log", DOC / "v16k_event_log.csv"),
        ("v16k", "dependency_edges", DOC / "v16k_fine_dependency_edges.csv"),
        ("v16k", "run_summary", DOC / "v16k_run_summary.csv"),
        ("v16k", "primary_results", DOC / "v16k_strict_null_run_summary.csv"),
        ("v16k", "longer_results", DOC / "v16k_longer_perturbation_run_summary.csv"),
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
        "gate": "v16l_sampler_attempt_qualification",
        "purpose_ref": PURPOSE_REF,
        "source_stage": "v16k",
        "source_max_attempts_per_edge": SOURCE_MAX_ATTEMPTS_PER_EDGE,
        "qualified_max_attempts_per_edge": QUALIFIED_MAX_ATTEMPTS_PER_EDGE,
        "primary_target_swap_multiplier": v16j.TARGET_ACCEPTED_SWAPS_PER_EDGE,
        "primary_null_replicates": v16j.NULL_REPLICATES,
        "longer_target_swap_multiplier": v16k.LONGER_TARGET_SWAP_MULTIPLIER,
        "longer_null_replicates": v16k.LONGER_NULL_REPLICATES,
        "same_null_seeds_as_v16k": True,
        "qualification_uses_effect_values": False,
        "posthoc_spectrum_is_confirmatory": False,
        "future_holdout_required": True,
    }


def spec_digest() -> str:
    raw = json.dumps(spec_payload(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_v16k_dags() -> List[v16i.RunDAG]:
    event_rows = v16i.read_csv(DOC / "v16k_event_log.csv")
    edge_rows = v16i.read_csv(DOC / "v16k_fine_dependency_edges.csv")
    run_rows = v16i.read_csv(DOC / "v16k_run_summary.csv")
    events_by_key: Dict[Tuple[int, int, str, int], List[Dict[str, str]]] = defaultdict(list)
    edges_by_key: Dict[Tuple[int, int, str, int], List[Dict[str, str]]] = defaultdict(list)
    for row in event_rows:
        events_by_key[run_key(row)].append(row)
    for row in edge_rows:
        edges_by_key[run_key(row)].append(row)
    expected = {run_key(row) for row in run_rows}
    if set(events_by_key) != expected or set(edges_by_key) != expected or len(expected) != 12:
        raise ValueError("v16l source history keys are incomplete")
    dags: List[v16i.RunDAG] = []
    for key in sorted(expected):
        events = sorted(events_by_key[key], key=lambda row: int(row["event_id"]))
        if len(events) != v16k.STEPS:
            raise ValueError("v16l source history event count failed")
        predecessors: List[List[int]] = [[] for _ in events]
        for edge in edges_by_key[key]:
            predecessors[int(edge["child_event_id"])].append(int(edge["parent_event_id"]))
        frozen_predecessors = tuple(tuple(sorted(set(parents))) for parents in predecessors)
        depths = tuple(v16i.recompute_depths(frozen_predecessors))
        observed_depths = tuple(int(row["causal_depth"]) for row in events)
        if depths != observed_depths:
            raise ValueError("v16l source history depth reconstruction failed")
        dags.append(v16i.RunDAG(
            stage="v16k",
            target_nodes=v16k.TARGET_NODES,
            growth_seed=key[0],
            run_offset=key[1],
            arm=key[2],
            run_seed=key[3],
            predecessors=frozen_predecessors,
            depths=depths,
            indegrees=tuple(len(parents) for parents in frozen_predecessors),
        ))
    return dags


def preregistration_rows() -> List[Dict[str, Any]]:
    if not SOURCE_CHAIN.exists():
        raise ValueError("missing v16l source chain")
    rows: List[Dict[str, Any]] = []
    for dag in load_v16k_dags():
        for family, replicates, multiplier in (
            (v16j.NULL_FAMILY, v16j.NULL_REPLICATES, v16j.TARGET_ACCEPTED_SWAPS_PER_EDGE),
            ("degree_depth_global_age_bin_double_edge_swap_longer_010", v16k.LONGER_NULL_REPLICATES, v16k.LONGER_TARGET_SWAP_MULTIPLIER),
        ):
            rows.append({
                "purpose_ref": PURPOSE_REF,
                "spec_digest": spec_digest(),
                "script_sha256": file_sha256(SCRIPT),
                "v16j_sha256": file_sha256(Path(v16j.__file__)),
                "v16k_sha256": file_sha256(Path(v16k.__file__)),
                "source_chain_sha256": file_sha256(SOURCE_CHAIN),
                **dag.prefix,
                "null_family": family,
                "null_replicates": replicates,
                "target_swap_multiplier": multiplier,
                "source_max_attempts_per_edge": SOURCE_MAX_ATTEMPTS_PER_EDGE,
                "qualified_max_attempts_per_edge": QUALIFIED_MAX_ATTEMPTS_PER_EDGE,
                "qualification_uses_effect_values": 0,
                "posthoc_spectrum_confirmatory": 0,
            })
    return rows


def prepare() -> None:
    gates = v16i.read_csv(DOC / "v16k_gate_evaluation.csv")
    overall = next(row["status"] for row in gates if row["gate"] == "v16k_overall")
    if overall != "v16k_instrumentation_failed":
        raise ValueError("v16l requires the frozen v16k instrumentation failure")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    rows = preregistration_rows()
    v16i.write_csv(PRE_REGISTRATION, rows)
    print(f"[v16l] prepared rows={len(rows)} digest={spec_digest()}")


def load_and_verify_preregistration() -> List[v16i.RunDAG]:
    observed = v16i.read_csv(PRE_REGISTRATION)
    expected = [{key: str(value) for key, value in row.items()} for row in preregistration_rows()]
    if observed != expected:
        raise ValueError("v16l preregistration changed")
    frozen_sources = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current_sources = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen_sources != current_sources:
        raise ValueError("v16l source chain changed")
    return load_v16k_dags()


def with_qualified_ceiling(function: Any, *args: Any, **kwargs: Any) -> Any:
    original = v16j.MAX_ATTEMPTS_PER_EDGE
    if original != SOURCE_MAX_ATTEMPTS_PER_EDGE:
        raise RuntimeError("v16j attempt ceiling changed unexpectedly")
    v16j.MAX_ATTEMPTS_PER_EDGE = QUALIFIED_MAX_ATTEMPTS_PER_EDGE
    try:
        return function(*args, **kwargs)
    finally:
        v16j.MAX_ATTEMPTS_PER_EDGE = original


def qualification_rows(
    primary_audits: Sequence[Mapping[str, Any]],
    longer_audits: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for family, audits, integrity_field, expected in (
        (v16j.NULL_FAMILY, primary_audits, "null_integrity_pass", 12 * v16j.NULL_REPLICATES),
        ("degree_depth_global_age_bin_double_edge_swap_longer_010", longer_audits, "perturbation_integrity_pass", 12 * v16k.LONGER_NULL_REPLICATES),
    ):
        passes = sum(int(row[integrity_field]) for row in audits)
        maximum_attempts_per_edge = max(
            float(row["attempted_swaps"]) / float(row["edge_count"])
            for row in audits
        )
        rows.append({
            "null_family": family,
            "n_perturbations": len(audits),
            "completion_and_integrity_passes": passes,
            "required_passes": expected,
            "max_observed_attempts_per_edge": maximum_attempts_per_edge,
            "qualified_ceiling_attempts_per_edge": QUALIFIED_MAX_ATTEMPTS_PER_EDGE,
            "min_changed_edge_fraction": min(float(row["changed_edge_fraction"]) for row in audits),
            "all_unique_within_run": int(all(float(row["run_unique_null_fraction"]) == 1.0 for row in audits)),
            "qualification_pass": int(len(audits) == expected and passes == expected),
            "effect_values_used_for_decision": 0,
        })
    return rows


def sensitivity_rows(
    qualified_primary: Sequence[Mapping[str, Any]],
    qualified_longer: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    old_primary = {run_key(row): row for row in v16i.read_csv(DOC / "v16k_strict_null_run_summary.csv")}
    old_longer = {run_key(row): row for row in v16i.read_csv(DOC / "v16k_longer_perturbation_run_summary.csv")}
    rows: List[Dict[str, Any]] = []
    for family, fresh_rows, old_rows in (
        (v16j.NULL_FAMILY, qualified_primary, old_primary),
        ("degree_depth_global_age_bin_double_edge_swap_longer_010", qualified_longer, old_longer),
    ):
        for row in fresh_rows:
            old = old_rows[run_key(row)]
            before = float(old["js_effect_ratio"])
            after = float(row["js_effect_ratio"])
            rows.append({
                **{field: row[field] for field in ("stage", "target_nodes", "growth_seed", "run_offset", "arm", "run_seed")},
                "null_family": family,
                "source_attempt_ceiling": SOURCE_MAX_ATTEMPTS_PER_EDGE,
                "qualified_attempt_ceiling": QUALIFIED_MAX_ATTEMPTS_PER_EDGE,
                "source_js_effect_ratio": before,
                "qualified_js_effect_ratio": after,
                "qualified_over_source_ratio": after / before,
                "same_effect_direction": int((before > 1.0) == (after > 1.0)),
                "confirmatory": 0,
            })
    return rows


def gate_rows(qualification: Sequence[Mapping[str, Any]]) -> Tuple[List[Dict[str, Any]], str]:
    source_pass = len(v16i.read_csv(PRE_REGISTRATION)) == 24
    primary = next(row for row in qualification if row["null_family"] == v16j.NULL_FAMILY)
    longer = next(row for row in qualification if row["null_family"] != v16j.NULL_FAMILY)
    primary_pass = int(primary["qualification_pass"]) == 1
    longer_pass = int(longer["qualification_pass"]) == 1
    if source_pass and primary_pass and longer_pass:
        overall = "sampler_attempt_budget_qualified_for_new_holdout"
    else:
        overall = "sampler_attempt_budget_not_qualified"
    rows = [
        {"gate": "v16k_source_contract", "status": "pass" if source_pass else "fail", "observed": int(source_pass), "required": 1, "decision": "continue" if source_pass else "stop"},
        {"gate": "primary_completion_integrity", "status": "pass" if primary_pass else "fail", "observed": f"{primary['completion_and_integrity_passes']}/{primary['n_perturbations']}", "required": "384/384", "decision": "continue" if primary_pass else "do_not_use_sampler"},
        {"gate": "longer_completion_integrity", "status": "pass" if longer_pass else "fail", "observed": f"{longer['completion_and_integrity_passes']}/{longer['n_perturbations']}", "required": "192/192", "decision": "continue" if longer_pass else "do_not_use_sampler"},
        {"gate": "effect_blind_qualification", "status": "pass", "observed": 0, "required": "effect_values_used=0", "decision": "continue"},
        {"gate": "v16l_overall", "status": overall, "observed": f"source={int(source_pass)};primary={int(primary_pass)};longer={int(longer_pass)}", "required": "1;1;1", "decision": overall},
    ]
    return rows, overall


def claim_rows(overall: str) -> List[Dict[str, Any]]:
    qualified = overall == "sampler_attempt_budget_qualified_for_new_holdout"
    return [
        {"claim_id": "C1", "claim": "A 240-attempts-per-edge ceiling completes all frozen primary and longer perturbation targets on the v16k DAGs while preserving declared structure and uniqueness.", "status": "supported" if qualified else "unsupported", "evidence": "v16l_sampler_qualification.csv", "scope_limit": "attempt-budget qualification on saved v16k DAGs"},
        {"claim_id": "C2", "claim": "The qualified sampler has validated the v16k scientific effect confirmatorily.", "status": "unsupported", "evidence": "none", "scope_limit": "v16l posthoc spectra cannot rehabilitate frozen v16k"},
        {"claim_id": "C3", "claim": "The qualified sampler is uniform, stationary, converged, independent, or representative over the constrained DAG space.", "status": "unsupported", "evidence": "none", "scope_limit": "completion and perturbation integrity do not prove those properties"},
        {"claim_id": "C4", "claim": "The qualified sampler is ready for a new fresh-history holdout under the declared completion contract.", "status": "supported" if qualified else "unsupported", "evidence": "v16l_gate_evaluation.csv", "scope_limit": "requires new seeds and unchanged scientific gates"},
    ]


def build_report(
    qualification: Sequence[Mapping[str, Any]],
    sensitivity: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16l sampler attempt-budget qualification",
        "",
        f"Status: `{overall}`.",
        "",
        "v16l keeps frozen v16k failed. It changes only the operational safety ceiling from 60 to 240 attempts per direct edge and reruns the exact same perturbation seeds, targets, stopping conditions, and null counts on the saved v16k DAGs.",
        "",
        f"Specification digest: `{spec_digest()}`.",
        "",
        "## Effect-blind qualification",
        "",
    ]
    lines.extend(v16i.table(qualification, ("null_family", "n_perturbations", "completion_and_integrity_passes", "max_observed_attempts_per_edge", "min_changed_edge_fraction", "all_unique_within_run", "qualification_pass")))
    lines.extend(["", "## Post-hoc spectrum sensitivity", ""])
    lines.append("These rows are nonconfirmatory and did not enter the qualification decision.")
    lines.append("")
    lines.extend(v16i.table(sensitivity, ("growth_seed", "run_offset", "arm", "null_family", "source_js_effect_ratio", "qualified_js_effect_ratio", "qualified_over_source_ratio", "same_effect_direction", "confirmatory")))
    lines.extend(["", "## Gates", ""])
    lines.extend(v16i.table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "A pass means only that the larger safety ceiling completes the declared perturbation contracts on these saved DAGs and can be frozen for a new holdout. It does not prove convergence, stationarity, independence, representativeness, or uniform sampling. It does not make v16k a completed replication.",
        "",
        "No result here establishes dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum behavior, particles, entanglement, or a physical causal law.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    dags = load_and_verify_preregistration()
    primary_runs: List[Dict[str, Any]] = []
    primary_nulls: List[Dict[str, Any]] = []
    primary_audits: List[Dict[str, Any]] = []
    longer_runs: List[Dict[str, Any]] = []
    longer_nulls: List[Dict[str, Any]] = []
    longer_audits: List[Dict[str, Any]] = []
    for index, dag in enumerate(dags, start=1):
        primary, p_nulls, p_audits = with_qualified_ceiling(v16j.analyze_run, dag)
        longer, l_nulls, l_audits = with_qualified_ceiling(
            v16k.analyze_perturbation_family,
            dag,
            label="degree_depth_global_age_bin_double_edge_swap_longer_010",
            replicates=v16k.LONGER_NULL_REPLICATES,
            target_swap_multiplier=v16k.LONGER_TARGET_SWAP_MULTIPLIER,
        )
        primary_runs.append(primary)
        primary_nulls.extend(p_nulls)
        primary_audits.extend(p_audits)
        longer_runs.append(longer)
        longer_nulls.extend(l_nulls)
        longer_audits.extend(l_audits)
        print(f"[v16l] runs={index}/{len(dags)} primary={int(primary['all_null_integrity_pass'])} longer={int(longer['all_perturbation_integrity_pass'])}")

    qualification = qualification_rows(primary_audits, longer_audits)
    sensitivity = sensitivity_rows(primary_runs, longer_runs)
    gates, overall = gate_rows(qualification)
    v16i.write_csv(PRIMARY_RUNS, primary_runs)
    v16i.write_csv(PRIMARY_NULLS, primary_nulls)
    v16i.write_csv(PRIMARY_AUDIT, primary_audits)
    v16i.write_csv(LONGER_RUNS, longer_runs)
    v16i.write_csv(LONGER_NULLS, longer_nulls)
    v16i.write_csv(LONGER_AUDIT, longer_audits)
    v16i.write_csv(QUALIFICATION, qualification)
    v16i.write_csv(SENSITIVITY, sensitivity)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claim_rows(overall))
    REPORT.write_text(build_report(qualification, sensitivity, gates, overall), encoding="utf-8")
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.16l\n\n"
        f"Status: `{overall}`.\n\n"
        "Keep v16k failed. If v16l qualifies, freeze the 240-attempt ceiling for one new 12-run fresh-history holdout with new seeds and unchanged existence/magnitude semantics. Do not proceed to a resource-aware null before that holdout.\n",
        encoding="utf-8",
    )
    print(f"[v16l] complete overall={overall}")


def verify_outputs() -> None:
    load_and_verify_preregistration()
    qualification = v16i.read_csv(QUALIFICATION)
    gates = v16i.read_csv(GATE_EVALUATION)
    if len(qualification) != 2 or not all(int(row["qualification_pass"]) for row in qualification):
        raise ValueError("v16l sampler qualification failed")
    if len(v16i.read_csv(PRIMARY_AUDIT)) != 384 or len(v16i.read_csv(LONGER_AUDIT)) != 192:
        raise ValueError("v16l audit row counts failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16l_overall")
    if overall != "sampler_attempt_budget_qualified_for_new_holdout":
        raise ValueError(f"v16l not qualified: {overall}")
    if v16j.MAX_ATTEMPTS_PER_EDGE != SOURCE_MAX_ATTEMPTS_PER_EDGE:
        raise ValueError("v16l leaked its qualified ceiling into v16j")
    print(f"[v16l] output verification pass overall={overall}")


def self_test() -> None:
    dags = load_v16k_dags()
    if len(dags) != 12 or SOURCE_MAX_ATTEMPTS_PER_EDGE != 60 or QUALIFIED_MAX_ATTEMPTS_PER_EDGE != 240:
        raise AssertionError("v16l frozen design failed")
    before = v16j.MAX_ATTEMPTS_PER_EDGE
    with_qualified_ceiling(lambda: None)
    if v16j.MAX_ATTEMPTS_PER_EDGE != before:
        raise AssertionError("v16l ceiling restoration failed")
    print("[v16l] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16l sampler attempt-budget qualification")
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
