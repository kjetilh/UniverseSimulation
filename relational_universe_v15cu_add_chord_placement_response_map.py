#!/usr/bin/env python3
"""v0.15cu add_chord placement response map.

v15ct showed that p0 and p2 are not stable scale-law labels. The live signal is
weaker but more interesting: add_chord appears carrier-live, while the responding
placement changes with target/seed. This lab therefore maps a narrow local
placement landscape instead of spending more budget on one label.

Design:
- regime: band_zero_del
- growth seed: 202
- targets: 896 and 1024
- perturbation: add_chord only
- placements: p0, p1, p2, p3
- fresh seed deltas: not reused from v15cn/v15cp/v15cq/v15cs
- budgets: scaled from the target-768 step budget
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ct_response_fingerprint_synthesis as v15ct
import relational_universe_v15cs_add_chord_p0_scale_response_holdout as v15cs


TARGETS = (896, 1024)
PLACEMENTS = (0, 1, 2, 3)
PERTURBATION = "add_chord"
FRESH_SEED_DELTAS = (7307, 7351)
GROWTH_SEED = v15cs.GROWTH_SEED
REFERENCE_TARGET = v15cs.REFERENCE_TARGET
REFERENCE_STEPS = v15cs.REFERENCE_STEPS
LOG_EVERY = v15cs.LOG_EVERY

RESPONSE_CLASS_RANK = {
    "strong_persistent_far_shell": 5,
    "moderate_persistent_far_shell": 4,
    "transient_or_partial_horizon": 3,
    "diffuse_far_mass_no_horizon": 2,
    "no_horizon": 1,
    "weak_or_unclassified": 0,
}


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def fmt(x: Any, digits: int = 3) -> str:
    return v15cs.fmt(x, digits)


def profile_label(placement: int) -> str:
    return f"{PERTURBATION}_p{int(placement)}"


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def is_persistent(row: Mapping[str, Any]) -> bool:
    return "persistent_far_shell" in str(row["response_class"])


def class_rank(row: Mapping[str, Any]) -> int:
    return int(RESPONSE_CLASS_RANK.get(str(row["response_class"]), 0))


def placement_sort_key(row: Mapping[str, Any]) -> Tuple[int, float, float, float, float]:
    return (
        class_rank(row),
        safe_float(row["response_strength_score"]),
        safe_float(row["mean_high_horizon_span"]),
        safe_float(row["mean_high_retention_rate"]),
        safe_float(row["mean_weighted_mean_distance"]),
    )


def analyze_runs() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles(list(TARGETS))
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    by_target_state = {ens.target_nodes: base_states[(ens.name, GROWTH_SEED)] for ens in ensembles}
    by_target_row = {
        int(row["target_nodes"]): row
        for row in base_rows
        if int(row["growth_seed"]) == GROWTH_SEED and int(row["target_nodes"]) in TARGETS
    }
    run_rows: List[Dict[str, Any]] = []
    for target in TARGETS:
        for placement in PLACEMENTS:
            for seed_delta in FRESH_SEED_DELTAS:
                row = v15cs.analyze_run(
                    target=target,
                    base_state=by_target_state[int(target)],
                    base_row=by_target_row[int(target)],
                    perturbation=PERTURBATION,
                    placement=placement,
                    seed_delta=seed_delta,
                )
                row["profile_role"] = "placement_map"
                row["seed_scope"] = "fresh_seed_deltas_v15cu"
                run_rows.append(row)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) in TARGETS]
    return target_summary, run_rows


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for target in TARGETS:
        for placement in PLACEMENTS:
            group = [
                row
                for row in rows
                if int(row["target_nodes"]) == int(target)
                and str(row["perturbation"]) == PERTURBATION
                and int(row["placement"]) == int(placement)
            ]
            row: Dict[str, Any] = {
                "target_nodes": int(target),
                "profile_label": profile_label(placement),
                "perturbation": PERTURBATION,
                "placement": int(placement),
                "n_runs": len(group),
                "seed_deltas": ";".join(str(int(row["seed_delta"])) for row in group),
                "growth_seed": GROWTH_SEED,
                "reference_target_nodes": REFERENCE_TARGET,
                "reference_step_budget": REFERENCE_STEPS,
                "step_budget": int(v15cs.scaled_steps_for_target(target)),
                "log_every": LOG_EVERY,
                "established_far_shell_rate": mean_defined(
                    1.0 if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon" else 0.0
                    for row in group
                ),
                "late_probe_rate": mean_defined(
                    1.0 if str(row["far_shell_horizon_label"]) == "late_far_shell_probe" else 0.0 for row in group
                ),
                "mixed_far_shell_rate": mean_defined(
                    1.0 if str(row["far_shell_horizon_label"]) == "mixed_far_shell_horizon" else 0.0 for row in group
                ),
                "failed_far_shell_rate": mean_defined(
                    1.0 if str(row["far_shell_horizon_label"]) == "failed_far_shell_horizon" else 0.0 for row in group
                ),
                "no_far_shell_rate": mean_defined(
                    1.0 if str(row["far_shell_horizon_label"]) == "no_far_shell_horizon" else 0.0 for row in group
                ),
                "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in group),
                "mean_high_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group),
                "mean_high_retention_rate": mean_defined(safe_float(row["high_retention_rate"]) for row in group),
                "mean_last12_high_rate": mean_defined(safe_float(row["last12_high_rate"]) for row in group),
                "mean_total_high_count": mean_defined(safe_float(row["total_high_count"]) for row in group),
                "mean_longest_high_run": mean_defined(safe_float(row["longest_high_run"]) for row in group),
                "mean_far_shell_share": mean_defined(safe_float(row["mean_far_shell_share"]) for row in group),
                "mean_q90_far_shell_share": mean_defined(safe_float(row["q90_far_shell_share"]) for row in group),
                "mean_weighted_mean_distance": mean_defined(safe_float(row["mean_weighted_mean_distance"]) for row in group),
                "mean_abs_delta_spectral_radius_rel": mean_defined(
                    safe_float(row["abs_delta_spectral_radius_rel"]) for row in group
                ),
                "support_signatures": ";".join(sorted({str(row["support_signature"]) for row in group})),
            }
            row["response_strength_score"] = v15ct.response_strength_score(row)
            row["response_class"] = v15ct.response_class(row)
            out.append(row)
    return out


def placement_compare_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for target in TARGETS:
        group = sorted(
            [dict(row) for row in aggregate if int(row["target_nodes"]) == int(target)],
            key=placement_sort_key,
            reverse=True,
        )
        if not group:
            continue
        best = group[0]
        for rank, row in enumerate(group, start=1):
            out.append(
                {
                    "target_nodes": int(target),
                    "rank": int(rank),
                    "winner_flag": int(rank == 1),
                    "profile_label": row["profile_label"],
                    "placement": int(row["placement"]),
                    "response_class": row["response_class"],
                    "response_strength_score": int(row["response_strength_score"]),
                    "established_far_shell_rate": safe_float(row["established_far_shell_rate"]),
                    "mean_high_horizon_span": safe_float(row["mean_high_horizon_span"]),
                    "mean_high_retention_rate": safe_float(row["mean_high_retention_rate"]),
                    "mean_last12_high_rate": safe_float(row["mean_last12_high_rate"]),
                    "mean_far_shell_share": safe_float(row["mean_far_shell_share"]),
                    "mean_weighted_mean_distance": safe_float(row["mean_weighted_mean_distance"]),
                    "score_gap_to_best": int(row["response_strength_score"]) - int(best["response_strength_score"]),
                    "horizon_gap_to_best": safe_float(row["mean_high_horizon_span"]) - safe_float(best["mean_high_horizon_span"]),
                    "class_rank_gap_to_best": class_rank(row) - class_rank(best),
                }
            )
    return out


def landscape_label(rows: Sequence[Mapping[str, Any]]) -> str:
    persistent = [row for row in rows if is_persistent(row)]
    if not persistent:
        diffuse = [row for row in rows if str(row["response_class"]) == "diffuse_far_mass_no_horizon"]
        return "diffuse_without_horizon" if diffuse else "no_supported_placement_response"
    ranked = sorted(rows, key=placement_sort_key, reverse=True)
    best = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None
    if len(persistent) == 1:
        return "single_placement_dominant"
    if second is not None:
        score_gap = int(best["response_strength_score"]) - int(second["response_strength_score"])
        horizon_gap = safe_float(best["mean_high_horizon_span"]) - safe_float(second["mean_high_horizon_span"])
        if score_gap >= 2 or horizon_gap >= 48.0:
            return "single_placement_dominant_with_persistent_neighbors"
    return "multi_placement_response"


def target_pattern_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    target_clean = {int(row["target_nodes"]): int(row["separated_from_prev"]) for row in target_summary}
    out: List[Dict[str, Any]] = []
    for target in TARGETS:
        rows = [dict(row) for row in aggregate if int(row["target_nodes"]) == int(target)]
        ranked = sorted(rows, key=placement_sort_key, reverse=True)
        best = ranked[0]
        persistent = [row for row in rows if is_persistent(row)]
        run_group = [row for row in run_rows if int(row["target_nodes"]) == int(target)]
        out.append(
            {
                "target_nodes": int(target),
                "growth_seed": GROWTH_SEED,
                "seed_scope": "fresh_seed_deltas_v15cu",
                "seed_deltas": ";".join(str(x) for x in FRESH_SEED_DELTAS),
                "step_budget": int(v15cs.scaled_steps_for_target(target)),
                "separated_from_prev": int(target_clean.get(int(target), 0)),
                "requested_match_all": int(min((int(row["requested_match"]) for row in run_group), default=0) == 1),
                "best_profile": best["profile_label"],
                "best_placement": int(best["placement"]),
                "best_response_class": best["response_class"],
                "best_response_strength_score": int(best["response_strength_score"]),
                "best_horizon_span": safe_float(best["mean_high_horizon_span"]),
                "best_established_rate": safe_float(best["established_far_shell_rate"]),
                "n_persistent_placements": len(persistent),
                "persistent_placements": ";".join(str(int(row["placement"])) for row in persistent),
                "classes_by_placement": ";".join(
                    f"p{int(row['placement'])}:{row['response_class']}" for row in sorted(rows, key=lambda r: int(r["placement"]))
                ),
                "landscape_label": landscape_label(rows),
            }
        )
    return out


def placement_stability_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_key = {(int(row["target_nodes"]), int(row["placement"])): dict(row) for row in aggregate}
    out: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        a = by_key[(896, int(placement))]
        b = by_key[(1024, int(placement))]
        out.append(
            {
                "placement": int(placement),
                "profile_label": profile_label(placement),
                "target896_class": a["response_class"],
                "target1024_class": b["response_class"],
                "class_changed": int(str(a["response_class"]) != str(b["response_class"])),
                "target896_score": int(a["response_strength_score"]),
                "target1024_score": int(b["response_strength_score"]),
                "score_delta_1024_minus_896": int(b["response_strength_score"]) - int(a["response_strength_score"]),
                "target896_established_rate": safe_float(a["established_far_shell_rate"]),
                "target1024_established_rate": safe_float(b["established_far_shell_rate"]),
                "established_delta_1024_minus_896": safe_float(b["established_far_shell_rate"])
                - safe_float(a["established_far_shell_rate"]),
                "target896_horizon_span": safe_float(a["mean_high_horizon_span"]),
                "target1024_horizon_span": safe_float(b["mean_high_horizon_span"]),
                "horizon_delta_1024_minus_896": safe_float(b["mean_high_horizon_span"])
                - safe_float(a["mean_high_horizon_span"]),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    target_patterns: Sequence[Mapping[str, Any]],
    placement_stability: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    persistent_rows = [row for row in aggregate if is_persistent(row)]
    changed = sum(int(row["class_changed"]) for row in placement_stability)
    best_placements = [int(row["best_placement"]) for row in target_patterns]
    landscape_labels = {str(row["landscape_label"]) for row in target_patterns}

    if len(set(best_placements)) > 1 and persistent_rows:
        placement_status = "target_specific_placement_switch"
        placement_note = (
            "Beste placement skifter mellom target 896 og 1024, og minst en placement har persistent far-shell response."
        )
        next_step = "mechanism_probe_for_winning_placements"
        next_note = "Neste steg bor sammenligne supportgeometri og tidlig launch for vinnerplasseringene, ikke oeke label-budget."
    elif len(set(best_placements)) == 1 and persistent_rows:
        placement_status = "candidate_stable_placement"
        placement_note = f"Samme beste placement p{best_placements[0]} vinner ved begge target, med persistent response i kartet."
        next_step = "fresh_holdout_for_stable_add_chord_placement"
        next_note = "Neste steg bor holde ut den stabile placement-kandidaten paa nye seed-deltaer."
    elif "multi_placement_response" in landscape_labels:
        placement_status = "broad_or_mixed_placement_response"
        placement_note = "Flere placements gir persistent response uten ren vinner."
        next_step = "seek_nonplacement_observable"
        next_note = "Neste steg bor finne en observabel som forklarer hvorfor flere placements svarer."
    else:
        placement_status = "placement_response_not_supported"
        placement_note = "Kartet finner ingen robust persistent add_chord placement-response."
        next_step = "retire_add_chord_placement_map"
        next_note = "Neste steg bor forlate placement-labelen og syntetisere andre observabler."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelser er rene og alle requested add_chord-perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Enten startstorrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        },
        {
            "diagnostic_family": "seed_scope",
            "status": "fresh_seed_deltas_v15cu",
            "note": f"Seed-deltaene {FRESH_SEED_DELTAS} er ikke brukt i v15cn/v15cp/v15cq/v15cs.",
        },
        {
            "diagnostic_family": "add_chord_carrier",
            "status": "add_chord_carrier_live" if persistent_rows else "add_chord_carrier_not_supported_here",
            "note": f"{len(persistent_rows)} target/placement-aggregater har persistent far-shell response.",
        },
        {
            "diagnostic_family": "placement_landscape",
            "status": placement_status,
            "note": placement_note,
        },
        {
            "diagnostic_family": "target_stability",
            "status": "placement_classes_shift_across_targets" if changed else "placement_classes_stable_across_targets",
            "note": f"{changed}/{len(placement_stability)} placements skifter response-class mellom target 896 og 1024.",
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    placement_compare: Sequence[Mapping[str, Any]],
    target_patterns: Sequence[Mapping[str, Any]],
    placement_stability: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cu: add_chord placement response map")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om add_chord-responsen fra v15ct er et lite placement-landskap.")
    lines.append("Den kjorer ny dynamikk, men bare for `add_chord`, target `896/1024`, placements `0..3` og friske seed-deltaer.")
    lines.append("Dette er ikke en Lorentz-, global invariant-, entanglement- eller partikkeltest.")
    lines.append("")
    lines.append("## Design")
    lines.append("")
    lines.append("| field | value |")
    lines.append("| --- | --- |")
    lines.append(f"| targets | {';'.join(str(x) for x in TARGETS)} |")
    lines.append(f"| perturbation | {PERTURBATION} |")
    lines.append(f"| placements | {';'.join('p' + str(x) for x in PLACEMENTS)} |")
    lines.append(f"| fresh seed deltas | {';'.join(str(x) for x in FRESH_SEED_DELTAS)} |")
    lines.append(f"| reference steps | {REFERENCE_STEPS} at target {REFERENCE_TARGET} |")
    lines.append("")
    lines.append("## Startstorrelse")
    lines.append("")
    lines.append("| target | mean initial | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Placement aggregate")
    lines.append("")
    lines.append("| target | placement | class | score | established | none | horizon | retention | last12 | far share | distance |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['target_nodes'])} | p{int(row['placement'])} | {row['response_class']} | {int(row['response_strength_score'])} | {fmt(row['established_far_shell_rate'])} | {fmt(row['no_far_shell_rate'])} | {fmt(row['mean_high_horizon_span'])} | {fmt(row['mean_high_retention_rate'])} | {fmt(row['mean_last12_high_rate'])} | {fmt(row['mean_far_shell_share'])} | {fmt(row['mean_weighted_mean_distance'])} |"
        )
    lines.append("")
    lines.append("## Placement ranks")
    lines.append("")
    lines.append("| target | rank | placement | class | score | horizon | horizon gap to best |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in placement_compare:
        lines.append(
            f"| {int(row['target_nodes'])} | {int(row['rank'])} | p{int(row['placement'])} | {row['response_class']} | {int(row['response_strength_score'])} | {fmt(row['mean_high_horizon_span'])} | {fmt(row['horizon_gap_to_best'])} |"
        )
    lines.append("")
    lines.append("## Target patterns")
    lines.append("")
    lines.append("| target | best | class | score | horizon | persistent placements | landscape |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in target_patterns:
        lines.append(
            f"| {int(row['target_nodes'])} | {row['best_profile']} | {row['best_response_class']} | {int(row['best_response_strength_score'])} | {fmt(row['best_horizon_span'])} | {row['persistent_placements']} | {row['landscape_label']} |"
        )
    lines.append("")
    lines.append("## Cross-target placement stability")
    lines.append("")
    lines.append("| placement | 896 class | 1024 class | changed | horizon delta 1024-896 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in placement_stability:
        lines.append(
            f"| p{int(row['placement'])} | {row['target896_class']} | {row['target1024_class']} | {int(row['class_changed'])} | {fmt(row['horizon_delta_1024_minus_896'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Hvis beste placement skifter mellom target, er p0/p2 best lest som lokale lommer, ikke som skala-labeler.")
    lines.append("- Hvis samme placement vinner begge target, fortjener den en fresh holdout som placement-kandidat.")
    lines.append("- Hvis flere placements er persistent, trenger vi en observabel som forklarer responslandskapet heller enn mer placement-budget.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15cu", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke les dette som global invariant-, Lorentz-, entanglement- eller partikkel-evidens.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    by_family = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15cu",
        "",
        "Denne runden sjekker om add_chord-signalet egentlig handler om hvor i den lokale strukturen vi legger inn feilen.",
        "",
        f"- Kontrollstatus: `{by_family['artifact_control']['status']}`.",
        f"- Carrier-status: `{by_family['add_chord_carrier']['status']}`.",
        f"- Placement-landskap: `{by_family['placement_landscape']['status']}`.",
        f"- Target-stabilitet: `{by_family['target_stability']['status']}`.",
        "",
        "Poenget er aa unngaa aa overtolke navn som p0 og p2. Hvis beste plassering skifter, er det et landskap vi maa forklare, ikke en enkel lov.",
        "",
        f"- Neste steg: `{by_family['next_step']['status']}` fordi {by_family['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cu add_chord placement response map.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cu_add_chord_placement_response_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cu_add_chord_placement_response_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cu_add_chord_placement_response_aggregate.csv")
    p.add_argument("--out-placement-compare-csv", type=str, default="Documentation/v15cu_add_chord_placement_response_compare.csv")
    p.add_argument("--out-target-pattern-csv", type=str, default="Documentation/v15cu_add_chord_placement_response_target_patterns.csv")
    p.add_argument("--out-placement-stability-csv", type=str, default="Documentation/v15cu_add_chord_placement_response_stability.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cu_add_chord_placement_response_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cu_add_chord_placement_response_map.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cu_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cu.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    target_summary, run_rows = analyze_runs()
    aggregate = aggregate_rows(run_rows)
    placement_compare = placement_compare_rows(aggregate)
    target_patterns = target_pattern_rows(target_summary=target_summary, run_rows=run_rows, aggregate=aggregate)
    placement_stability = placement_stability_rows(aggregate)
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        aggregate=aggregate,
        target_patterns=target_patterns,
        placement_stability=placement_stability,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_placement_compare_csv, placement_compare)
    write_csv(args.out_target_pattern_csv, target_patterns)
    write_csv(args.out_placement_stability_csv, placement_stability)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            target_summary=target_summary,
            aggregate=aggregate,
            placement_compare=placement_compare,
            target_patterns=target_patterns,
            placement_stability=placement_stability,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
