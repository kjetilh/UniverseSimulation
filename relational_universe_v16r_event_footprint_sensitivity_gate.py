#!/usr/bin/env python3
"""v16r: posthoc v16m sensitivity under the qualified event-footprint null."""
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
import relational_universe_v16m_qualified_sampler_fresh_holdout as v16m
import relational_universe_v16n_coarse_event_resource_null_calibration as v16n
import relational_universe_v16o_event_resource_reachability_audit as v16o
import relational_universe_v16q_event_footprint_null_calibration as v16q


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"
QUALIFIED_MAX_ATTEMPTS_PER_EDGE = 60
PRIMARY_REPLICATES = v16j.NULL_REPLICATES
PRIMARY_SWAP_MULTIPLIER = v16j.TARGET_ACCEPTED_SWAPS_PER_EDGE
LONGER_REPLICATES = v16k.LONGER_NULL_REPLICATES
LONGER_SWAP_MULTIPLIER = v16k.LONGER_TARGET_SWAP_MULTIPLIER

SOURCE_CHAIN = DOC / "v16r_source_chain.csv"
PRE_REGISTRATION = DOC / "v16r_pre_registration.csv"
PRIMARY_RUNS = DOC / "v16r_event_footprint_run_summary.csv"
PRIMARY_NULLS = DOC / "v16r_event_footprint_null_distribution.csv"
PRIMARY_AUDIT = DOC / "v16r_event_footprint_perturbation_integrity.csv"
EFFECT_GATE = DOC / "v16r_effect_existence_gate.csv"
LONGER_RUNS = DOC / "v16r_longer_footprint_run_summary.csv"
LONGER_NULLS = DOC / "v16r_longer_footprint_null_distribution.csv"
LONGER_AUDIT = DOC / "v16r_longer_footprint_perturbation_integrity.csv"
LONGER_GATE = DOC / "v16r_longer_footprint_gate.csv"
COMPARISON = DOC / "v16r_v16m_sensitivity_comparison.csv"
GATE_EVALUATION = DOC / "v16r_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16r_claim_ledger.csv"
REPORT = DOC / "v16r_event_footprint_sensitivity_gate.md"
RECOMMENDATION = DOC / "v0_16r_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16r.md"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = [
        ("v16m", "holdout_events", v16m.EVENT_LOG),
        ("v16m", "holdout_edges", v16m.EDGE_LOG),
        ("v16m", "strict_null_run_summary", v16m.PRIMARY_RUNS),
        ("v16m", "effect_gate", v16m.EFFECT_GATE),
        ("v16q", "footprint_sampler_implementation", Path(v16q.__file__)),
        ("v16q", "sampler_qualification", v16q.QUALIFICATION),
        ("v16q", "sampler_gate", v16q.GATE_EVALUATION),
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
        "gate": "v16r_event_footprint_sensitivity_gate",
        "purpose_ref": PURPOSE_REF,
        "scope": "posthoc_sensitivity_on_six_v16m_primary_histories",
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
        "no_early_stop": True,
        "not_an_independent_replication": True,
    }


def spec_digest() -> str:
    raw = json.dumps(spec_payload(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def prepare() -> None:
    v16m.verify_outputs()
    v16q.verify_outputs()
    qualification = v16i.read_csv(v16q.QUALIFICATION)
    if len(qualification) != 1 or qualification[0]["status"] != "v16q_event_footprint_sampler_qualified":
        raise ValueError("v16r requires qualified v16q sampler")
    if int(qualification[0]["selected_attempt_ceiling"]) != QUALIFIED_MAX_ATTEMPTS_PER_EDGE:
        raise ValueError("v16r qualified attempt ceiling mismatch")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [{
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "script_sha256": file_sha256(SCRIPT),
        "source_chain_sha256": file_sha256(SOURCE_CHAIN),
        "source_history_count": 6,
        "source_arm": v16m.PRIMARY_ARM,
        "primary_replicates": PRIMARY_REPLICATES,
        "primary_swap_multiplier": PRIMARY_SWAP_MULTIPLIER,
        "longer_replicates": LONGER_REPLICATES,
        "longer_swap_multiplier": LONGER_SWAP_MULTIPLIER,
        "qualified_max_attempts_per_edge": QUALIFIED_MAX_ATTEMPTS_PER_EDGE,
        "not_an_independent_replication": 1,
    }])
    print(f"[v16r] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    rows = v16i.read_csv(PRE_REGISTRATION)
    expected = {
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "script_sha256": file_sha256(SCRIPT),
        "source_chain_sha256": file_sha256(SOURCE_CHAIN),
        "source_history_count": "6",
        "source_arm": v16m.PRIMARY_ARM,
        "primary_replicates": str(PRIMARY_REPLICATES),
        "primary_swap_multiplier": str(PRIMARY_SWAP_MULTIPLIER),
        "longer_replicates": str(LONGER_REPLICATES),
        "longer_swap_multiplier": str(LONGER_SWAP_MULTIPLIER),
        "qualified_max_attempts_per_edge": str(QUALIFIED_MAX_ATTEMPTS_PER_EDGE),
        "not_an_independent_replication": "1",
    }
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v16r preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v16r source chain changed")


def load_primary_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    grouped: Dict[Tuple[int, int, str, int], List[Dict[str, str]]] = defaultdict(list)
    for row in v16i.read_csv(v16m.EVENT_LOG):
        if row["arm"] == v16m.PRIMARY_ARM:
            grouped[v16o.run_key(row)].append(row)
    runs: List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]] = []
    for key in sorted(grouped):
        rows = sorted(grouped[key], key=lambda row: int(row["event_id"]))
        metadata, audit = v16n.event_metadata(rows)
        if not int(audit["event_id_mapping_total_pass"]):
            raise ValueError("v16r metadata mapping failed")
        predecessors = tuple(
            tuple(int(value) for value in row["direct_predecessors"].split(";") if value)
            for row in rows
        )
        depths = tuple(int(row["causal_depth"]) for row in rows)
        if tuple(v16i.recompute_depths(predecessors)) != depths:
            raise ValueError("v16r source depth mismatch")
        growth_seed, run_offset, arm, run_seed = key
        dag = v16i.RunDAG(
            stage="v16r",
            target_nodes=v16m.TARGET_NODES,
            growth_seed=growth_seed,
            run_offset=run_offset,
            arm=arm,
            run_seed=run_seed,
            predecessors=predecessors,
            depths=depths,
            indegrees=tuple(len(parents) for parents in predecessors),
        )
        runs.append((dag, metadata))
    if len(runs) != 6:
        raise ValueError("v16r requires six v16m primary histories")
    return runs


def analyze_family(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    *,
    label: str,
    replicates: int,
    target_swap_multiplier: float,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    observed = v16i.interval_spectrum(dag.predecessors)
    products: List[Dict[str, Any]] = []
    audits: List[Dict[str, Any]] = []
    for replicate in range(replicates):
        seed = v16i.stable_seed(
            "v16r", label, *dag.key, replicate, f"swap={target_swap_multiplier:.6f}"
        )
        rewired, audit = v16q.footprint_rewire(
            dag,
            metadata,
            seed,
            target_swap_multiplier=target_swap_multiplier,
            max_attempts_per_edge=QUALIFIED_MAX_ATTEMPTS_PER_EDGE,
        )
        products.append(v16i.interval_spectrum(rewired))
        audits.append({
            **dag.prefix,
            "null_family": label,
            "null_replicate": replicate,
            "null_seed": seed,
            **audit,
        })
    unique_count = len({row["null_edge_sha256"] for row in audits})
    unique_fraction = unique_count / replicates
    for row in audits:
        row["run_unique_null_count"] = unique_count
        row["run_unique_null_fraction"] = unique_fraction
        row["run_uniqueness_pass"] = int(unique_fraction >= v16q.MIN_UNIQUE_NULL_FRACTION)
        row["perturbation_integrity_pass"] = int(
            int(row["structure_pass"])
            and int(row["completion_and_change_pass"])
            and int(row["run_uniqueness_pass"])
        )

    spectra = [row["probabilities"] for row in products]
    center = v16i.mean_spectrum(spectra)
    observed_js = v16i.jensen_shannon(observed["probabilities"], center)
    null_self = [
        v16i.jensen_shannon(spectrum, v16i.mean_spectrum(spectra, skip=index))
        for index, spectrum in enumerate(spectra)
    ]
    null_median = v16i.median(null_self)
    ratio = observed_js / max(null_median, v16j.EPSILON)
    empirical_p = (1 + sum(value >= observed_js for value in null_self)) / (replicates + 1)
    all_integrity = all(int(row["perturbation_integrity_pass"]) for row in audits)
    summary = {
        **dag.prefix,
        "null_family": label,
        "null_replicates": replicates,
        "target_swap_multiplier": target_swap_multiplier,
        "n_events": len(dag.predecessors),
        "direct_edges": sum(dag.indegrees),
        "causal_depth": max(dag.depths) + 1,
        "comparable_pairs": observed["comparable_pairs"],
        "observed_js_to_null_center": observed_js,
        "null_median_leave_one_out_js": null_median,
        "js_effect_ratio": ratio,
        "empirical_p_upper": empirical_p,
        "effect_positive": int(ratio > 1.0),
        "p_le_010": int(empirical_p <= v16j.MAX_EMPIRICAL_P),
        "observed_mean_open_volume": observed["mean_open_volume"],
        "null_mean_open_volume": v16i.mean(row["mean_open_volume"] for row in products),
        "observed_tail_mass_ge_8": observed["tail_mass_ge_8"],
        "null_mean_tail_mass_ge_8": v16i.mean(row["tail_mass_ge_8"] for row in products),
        "tail_mass_ge_8_delta": observed["tail_mass_ge_8"] - v16i.mean(row["tail_mass_ge_8"] for row in products),
        "mean_acceptance_rate": v16i.mean(float(row["acceptance_rate"]) for row in audits),
        "min_changed_edge_fraction": min(float(row["changed_edge_fraction"]) for row in audits),
        "min_actual_resource_conflict_edge_fraction": min(float(row["actual_resource_conflict_edge_fraction"]) for row in audits),
        "unique_null_fraction": unique_fraction,
        "all_perturbation_integrity_pass": int(all_integrity),
    }
    null_rows = [{
        **dag.prefix,
        "null_family": label,
        "null_replicate": replicate,
        "null_seed": audits[replicate]["null_seed"],
        "null_edge_sha256": audits[replicate]["null_edge_sha256"],
        "comparable_pairs": product["comparable_pairs"],
        "leave_one_out_js": null_self[replicate],
        "mean_open_volume": product["mean_open_volume"],
        "tail_mass_ge_8": product["tail_mass_ge_8"],
        **{
            f"prob_{bin_label}": product["probabilities"][index]
            for index, (bin_label, _, _) in enumerate(v16i.INTERVAL_BINS)
        },
    } for replicate, product in enumerate(products)]
    return summary, null_rows, audits


def comparison_rows(primary: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    old = {
        v16o.run_key(row): row
        for row in v16i.read_csv(v16m.PRIMARY_RUNS)
        if row["arm"] == v16m.PRIMARY_ARM
    }
    rows: List[Dict[str, Any]] = []
    for row in primary:
        prior = old[v16o.run_key(row)]
        old_ratio = float(prior["js_effect_ratio"])
        new_ratio = float(row["js_effect_ratio"])
        rows.append({
            **{key: row[key] for key in ("growth_seed", "run_offset", "arm", "run_seed")},
            "v16m_strict_null_js_effect_ratio": old_ratio,
            "v16r_footprint_null_js_effect_ratio": new_ratio,
            "footprint_over_strict_ratio": new_ratio / max(old_ratio, v16j.EPSILON),
            "v16m_empirical_p_upper": prior["empirical_p_upper"],
            "v16r_empirical_p_upper": row["empirical_p_upper"],
            "observed_spectrum_reused": 1,
        })
    return rows


def build_report(
    primary: Sequence[Mapping[str, Any]],
    local: Mapping[str, Any],
    longer: Mapping[str, Any],
    comparison: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16r event-footprint sensitivity gate",
        "",
        f"Status: `{overall}`.",
        "",
        "V16r is a posthoc sensitivity analysis on the six v16m primary histories. It reuses the observed event DAGs and replaces the v16m strict null with the v16q-qualified event-footprint null. It is not an independent replication.",
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
    lines.extend(["", "## Aggregate gates", ""])
    lines.extend(v16i.table([local], (
        "n_runs", "median_js_effect_ratio", "positive_fraction", "p_le_010_fraction", "local_gate_pass",
    )))
    lines.append("")
    lines.extend(v16i.table([longer], (
        "n_runs", "median_js_effect_ratio", "positive_fraction",
        "perturbation_integrity_pass", "longer_perturbation_consistency_pass",
    )))
    lines.extend(["", "## Same-history null comparison", ""])
    lines.extend(v16i.table(comparison, (
        "growth_seed", "run_offset", "v16m_strict_null_js_effect_ratio",
        "v16r_footprint_null_js_effect_ratio", "footprint_over_strict_ratio",
    )))
    lines.extend(["", "## Gates", ""])
    lines.extend(v16i.table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "Persistence means the coarse event-family/write-read namespace footprint does not absorb the interval-spectrum contrast on these six reused histories, conditional on the qualified procedure. It does not establish independence from concrete resource identity, a causal mechanism, sampler uniformity, or a new replication.",
        "",
        "Failure would show sensitivity to this null family, not prove that the original contrast was spurious.",
        "",
        "No dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particle, entanglement, or physical-law claim is authorized.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    verify_frozen_sources()
    primary: List[Dict[str, Any]] = []
    primary_nulls: List[Dict[str, Any]] = []
    primary_audits: List[Dict[str, Any]] = []
    longer_runs: List[Dict[str, Any]] = []
    longer_nulls: List[Dict[str, Any]] = []
    longer_audits: List[Dict[str, Any]] = []
    runs = load_primary_runs()
    for index, (dag, metadata) in enumerate(runs, start=1):
        summary, nulls, audits = analyze_family(
            dag,
            metadata,
            label=f"{v16q.NULL_FAMILY}_primary_0075",
            replicates=PRIMARY_REPLICATES,
            target_swap_multiplier=PRIMARY_SWAP_MULTIPLIER,
        )
        longer, l_nulls, l_audits = analyze_family(
            dag,
            metadata,
            label=f"{v16q.NULL_FAMILY}_longer_0100",
            replicates=LONGER_REPLICATES,
            target_swap_multiplier=LONGER_SWAP_MULTIPLIER,
        )
        primary.append(summary)
        primary_nulls.extend(nulls)
        primary_audits.extend(audits)
        longer_runs.append(longer)
        longer_nulls.extend(l_nulls)
        longer_audits.extend(l_audits)
        print(
            f"[v16r] runs={index}/{len(runs)} primary={summary['js_effect_ratio']:.6f} "
            f"longer={longer['js_effect_ratio']:.6f}"
        )

    local = v16j.local_gate_row(primary, "v16r")
    longer = dict(v16k.longer_gate_row(longer_runs))
    longer["stage"] = "v16r"
    comparison = comparison_rows(primary)
    primary_integrity = len(primary_audits) == 6 * PRIMARY_REPLICATES and all(
        int(row["perturbation_integrity_pass"]) for row in primary_audits
    )
    longer_integrity = len(longer_audits) == 6 * LONGER_REPLICATES and all(
        int(row["perturbation_integrity_pass"]) for row in longer_audits
    )
    existence = int(local["local_gate_pass"]) == 1
    longer_consistency = int(longer["longer_perturbation_consistency_pass"]) == 1
    if not primary_integrity or not longer_integrity:
        overall = "v16r_event_footprint_instrumentation_failed"
    elif existence and longer_consistency:
        overall = "v16r_spectrum_contrast_persists_under_event_footprint_null"
    elif float(local["positive_fraction"]) > 0:
        overall = "v16r_spectrum_contrast_attenuated_or_inconclusive"
    else:
        overall = "v16r_spectrum_contrast_not_distinguished_from_event_footprint_null"
    gates = [
        {
            "gate": "qualified_primary_footprint_perturbation_integrity",
            "status": "pass" if primary_integrity else "fail",
            "observed": f"{sum(int(row['perturbation_integrity_pass']) for row in primary_audits)}/{len(primary_audits)}",
            "required": "192/192",
            "decision": "continue" if primary_integrity else "inconclusive",
        },
        {
            "gate": "posthoc_footprint_effect_existence",
            "status": "pass" if existence else "fail",
            "observed": f"median={float(local['median_js_effect_ratio']):.6f};positive={float(local['positive_fraction']):.6f};p_le_010={float(local['p_le_010_fraction']):.6f}",
            "required": "median>=2;positive>=5/6;p_le_010>=1/2",
            "decision": "persists" if existence else "attenuated_or_absorbed",
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
            "observed": f"median={float(longer['median_js_effect_ratio']):.6f};positive={float(longer['positive_fraction']):.6f}",
            "required": "median>=1;positive>=5/6",
            "decision": "consistent" if longer_consistency else "inconclusive",
        },
        {
            "gate": "independent_replication_exclusion",
            "status": "pass",
            "observed": "same_v16m_histories",
            "required": "posthoc_sensitivity_only",
            "decision": "do_not_count_as_new_replication",
        },
        {
            "gate": "v16r_overall",
            "status": overall,
            "observed": f"integrity={int(primary_integrity and longer_integrity)};existence={int(existence)};longer={int(longer_consistency)}",
            "required": "diagnostic_branch",
            "decision": overall,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "The v16m interval-spectrum contrast persists under the qualified coarse event-footprint null on the same six primary histories.",
            "status": "supported" if overall == "v16r_spectrum_contrast_persists_under_event_footprint_null" else "unsupported",
            "evidence": "v16r_effect_existence_gate.csv;v16r_longer_footprint_gate.csv",
            "scope_limit": "posthoc same-history sensitivity conditional on a coarse qualified sampler",
        },
        {
            "claim_id": "C2",
            "claim": "V16r is an independent replication on fresh histories.",
            "status": "unsupported",
            "evidence": "v16r_pre_registration.csv",
            "scope_limit": "observed v16m histories are reused",
        },
        {
            "claim_id": "C3",
            "claim": "The contrast is independent of concrete resource identity or event mechanism.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "footprint does not preserve concrete resource identity and is not a causal mechanism proof",
        },
        {
            "claim_id": "C4",
            "claim": "The sampler is uniform, converged, stationary, independent, or representative.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "procedural qualification only",
        },
        {
            "claim_id": "C5",
            "claim": "Dimension, Lorentz symmetry, spacetime, continuum physics, particles, or entanglement were established.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "finite event-DAG structural sensitivity only",
        },
    ]

    v16i.write_csv(PRIMARY_RUNS, primary)
    v16i.write_csv(PRIMARY_NULLS, primary_nulls)
    v16i.write_csv(PRIMARY_AUDIT, primary_audits)
    v16i.write_csv(EFFECT_GATE, [local])
    v16i.write_csv(LONGER_RUNS, longer_runs)
    v16i.write_csv(LONGER_NULLS, longer_nulls)
    v16i.write_csv(LONGER_AUDIT, longer_audits)
    v16i.write_csv(LONGER_GATE, [longer])
    v16i.write_csv(COMPARISON, comparison)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    REPORT.write_text(build_report(primary, local, longer, comparison, gates, overall), encoding="utf-8")
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.16r\n\n"
        f"Status: `{overall}`.\n\n"
        f"Primary median ratio: `{float(local['median_js_effect_ratio']):.6f}`.\n\n"
        f"Longer median ratio: `{float(longer['median_js_effect_ratio']):.6f}`.\n\n"
        "This is a posthoc same-history sensitivity gate, not a new replication or a physics claim.\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.16r\n\n"
        f"Statusen er `{overall}`. Runden spoer om det tidligere grafmonsteret fortsatt skiller seg ut naar kontrollgrafene ogsaa bevarer grove hendelses- og ressursroller. De samme simuleringene brukes om igjen, saa dette er en robusthetstest og ikke en ny bekreftelse.\n",
        encoding="utf-8",
    )
    print(f"[v16r] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    primary = v16i.read_csv(PRIMARY_RUNS)
    p_audits = v16i.read_csv(PRIMARY_AUDIT)
    longer = v16i.read_csv(LONGER_RUNS)
    l_audits = v16i.read_csv(LONGER_AUDIT)
    gates = v16i.read_csv(GATE_EVALUATION)
    if len(primary) != 6 or len(longer) != 6:
        raise ValueError("v16r run summary count failed")
    if len(p_audits) != 192 or not all(int(row["perturbation_integrity_pass"]) for row in p_audits):
        raise ValueError("v16r primary integrity failed")
    if len(l_audits) != 96 or not all(int(row["perturbation_integrity_pass"]) for row in l_audits):
        raise ValueError("v16r longer integrity failed")
    if len(v16i.read_csv(COMPARISON)) != 6:
        raise ValueError("v16r comparison count failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16r_overall")
    allowed = {
        "v16r_event_footprint_instrumentation_failed",
        "v16r_spectrum_contrast_persists_under_event_footprint_null",
        "v16r_spectrum_contrast_attenuated_or_inconclusive",
        "v16r_spectrum_contrast_not_distinguished_from_event_footprint_null",
    }
    if overall not in allowed:
        raise ValueError("v16r unknown status")
    print(f"[v16r] output verification pass overall={overall}")


def self_test() -> None:
    qualification = v16i.read_csv(v16q.QUALIFICATION)
    if len(qualification) != 1 or int(qualification[0]["selected_attempt_ceiling"]) != QUALIFIED_MAX_ATTEMPTS_PER_EDGE:
        raise AssertionError("v16r qualified ceiling changed")
    runs = load_primary_runs()
    if len(runs) != 6 or any(dag.arm != v16m.PRIMARY_ARM for dag, _ in runs):
        raise AssertionError("v16r primary history selection failed")
    print("[v16r] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16r event-footprint sensitivity gate")
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
