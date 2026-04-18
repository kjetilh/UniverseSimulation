#!/usr/bin/env python3
"""v0.15bo add_chord scale-jump holdout.

Follow-up to v15bn:
test the weak 48/p2 -> 96/p3 match against the nearest 96 rival (p1) on fresh
holdout seeds, using the same coarse-geometry and relative-drift observables.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15q_single_defect_recurrence_lab as v15q


GROWTH_SEED = 202
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
SEED_DELTAS = (331, 359, 389, 419, 449, 479)
NONTRIVIAL_METRICS = v15bl.NONTRIVIAL_REL_METRICS
COARSE_KEYS = [
    "mean_full_exact_return_rate",
    "mean_full_coarse_return_rate",
    "mean_core_share_of_union",
    "mean_shell_share_of_union",
    "mean_rare_share_of_union",
    "mean_core_cover",
]
PROFILES = (
    {"profile_label": "anchor_48_p2", "target_nodes": 48, "placement": 2, "role": "anchor"},
    {"profile_label": "candidate_96_p3", "target_nodes": 96, "placement": 3, "role": "candidate"},
    {"profile_label": "control_96_p1", "target_nodes": 96, "placement": 1, "role": "control"},
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def aggregate_profile(rows: Sequence[Mapping[str, Any]], profile: Mapping[str, Any]) -> Dict[str, Any]:
    nontrivial_pairs = [
        (metric, mean_defined(safe_float(row[metric]) for row in rows))
        for metric in NONTRIVIAL_METRICS
    ]
    nontrivial_pairs.sort(key=lambda item: item[1])
    rank_map = {metric: idx for idx, (metric, _) in enumerate(nontrivial_pairs, start=1)}
    best_metric, best_mean = nontrivial_pairs[0]
    return {
        "profile_label": str(profile["profile_label"]),
        "role": str(profile["role"]),
        "target_nodes": int(profile["target_nodes"]),
        "placement": int(profile["placement"]),
        "n_runs": len(rows),
        "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in rows),
        "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in rows),
        "structured_core_shell_rate": mean_defined(
            1.0 if str(row["core_shell_label"]) in ("stable_core_variable_shell", "dominant_static_core") else 0.0
            for row in rows
        ),
        "mean_core_share_of_union": mean_defined(safe_float(row["core_share_of_union"]) for row in rows),
        "mean_shell_share_of_union": mean_defined(safe_float(row["shell_share_of_union"]) for row in rows),
        "mean_rare_share_of_union": mean_defined(safe_float(row["rare_share_of_union"]) for row in rows),
        "mean_core_cover": mean_defined(safe_float(row["mean_core_cover"]) for row in rows),
        "mean_abs_delta_spectral_radius_rel": mean_defined(safe_float(row["abs_delta_spectral_radius_rel"]) for row in rows),
        "mean_abs_delta_dim_proxy_rel": mean_defined(safe_float(row["abs_delta_dim_proxy_rel"]) for row in rows),
        "mean_abs_delta_clustering_rel": mean_defined(safe_float(row["abs_delta_clustering_rel"]) for row in rows),
        "mean_abs_delta_triangles_rel": mean_defined(safe_float(row["abs_delta_triangles_rel"]) for row in rows),
        "best_nontrivial_metric": best_metric,
        "best_nontrivial_mean_relative_drift": best_mean,
        "spectral_rank_nontrivial": rank_map["abs_delta_spectral_radius_rel"],
        "dim_rank_nontrivial": rank_map["abs_delta_dim_proxy_rel"],
        "mean_dim_minus_spectral": mean_defined(
            safe_float(row["abs_delta_dim_proxy_rel"]) - safe_float(row["abs_delta_spectral_radius_rel"]) for row in rows
        ),
    }


def comparison_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    agg_map = {str(row["profile_label"]): dict(row) for row in aggregate}
    anchor = agg_map["anchor_48_p2"]
    out: List[Dict[str, Any]] = []
    for key in ("candidate_96_p3", "control_96_p1"):
        other = agg_map[key]
        coarse_distance = sum(abs(safe_float(other[name]) - safe_float(anchor[name])) for name in COARSE_KEYS)
        spectral_margin_gap = abs(
            safe_float(other["mean_dim_minus_spectral"]) - safe_float(anchor["mean_dim_minus_spectral"])
        )
        out.append(
            {
                "anchor_profile": "anchor_48_p2",
                "other_profile": key,
                "other_role": str(other["role"]),
                "other_best_nontrivial_metric": str(other["best_nontrivial_metric"]),
                "other_spectral_rank_nontrivial": int(other["spectral_rank_nontrivial"]),
                "coarse_distance": coarse_distance,
                "spectral_margin_gap": spectral_margin_gap,
                "combined_distance": coarse_distance + spectral_margin_gap,
                "other_dim_minus_spectral": safe_float(other["mean_dim_minus_spectral"]),
                "other_structured_core_shell_rate": safe_float(other["structured_core_shell_rate"]),
            }
        )
    out.sort(key=lambda row: safe_float(row["combined_distance"]))
    for idx, row in enumerate(out, start=1):
        row["comparison_rank"] = idx
    return out


def diagnosis_rows(
    target_summary: Sequence[Mapping[str, Any]],
    rows: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    candidate = next(row for row in comparisons if str(row["other_profile"]) == "candidate_96_p3")
    control = next(row for row in comparisons if str(row["other_profile"]) == "control_96_p1")
    combined_gap = safe_float(control["combined_distance"]) - safe_float(candidate["combined_distance"])
    spectral_gap = safe_float(control["spectral_margin_gap"]) - safe_float(candidate["spectral_margin_gap"])
    coarse_gap = safe_float(control["coarse_distance"]) - safe_float(candidate["coarse_distance"])

    if (
        int(candidate["other_spectral_rank_nontrivial"]) == 1
        and combined_gap >= 0.05
        and safe_float(candidate["combined_distance"]) < safe_float(control["combined_distance"])
    ):
        status = "scale_jump_pair_supported"
        note = (
            f"96/p3 holder spectral rank 1 og slar 96/p1 pa holdout med combined gap {fmt(combined_gap)} "
            f"(coarse gap {fmt(coarse_gap)}, spectral-margin gap {fmt(spectral_gap)})."
        )
        next_step = "update_context_and_probe_coarse_geometry"
        next_note = "Neste steg kan bruke dette som en ekte liten skalapair og teste en eksplisitt coarse-geometry-beskrivelse."
    elif (
        int(candidate["other_spectral_rank_nontrivial"]) == 1
        and safe_float(candidate["combined_distance"]) < safe_float(control["combined_distance"])
    ):
        status = "scale_jump_pair_weak"
        note = (
            f"96/p3 holder seg foran 96/p1 pa holdout, men bare med combined gap {fmt(combined_gap)}."
        )
        next_step = "one_more_geometry_tiebreak"
        next_note = "Neste steg bor vaere en veldig liten geometry tie-break, ikke en bred ny runde."
    else:
        status = "scale_jump_pair_not_yet"
        note = "96/p3 holder ikke klart nok foran 96/p1 pa holdout til at vi kan lese dette som en ekte liten skalafamilie."
        next_step = "explain_scale_break"
        next_note = "Neste steg bor forklare hvor 48->96-likheten bryter, ikke late som scale-transfer allerede holder."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsene er rent separert og alle holdout-runs matcher onsket add_chord-perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "holdout_scale_pair",
            "status": status,
            "note": note,
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
    comparisons: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bo: add_chord scale-jump holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester 48/p2 mot den svakeste men beste 96-kandidaten fra v15bn (p3), med 96/p1 som naermeste kontrollrival.")
    lines.append("")
    lines.append("## Startstorrelser")
    lines.append("")
    lines.append("| target | mean initial | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Aggregate profiler")
    lines.append("")
    lines.append("| profile | role | exact | coarse | core | shell | rare | spectral | dim | best metric | spectral rank |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {row['role']} | {fmt(row['mean_full_exact_return_rate'])} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_core_share_of_union'])} | {fmt(row['mean_shell_share_of_union'])} | {fmt(row['mean_rare_share_of_union'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} | {fmt(row['mean_abs_delta_dim_proxy_rel'])} | {row['best_nontrivial_metric']} | {int(row['spectral_rank_nontrivial'])} |"
        )
    lines.append("")
    lines.append("## Holdout-sammenlikning mot anker")
    lines.append("")
    lines.append("| other profile | role | combined | coarse | spectral gap | best metric | spectral rank | rank |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in comparisons:
        lines.append(
            f"| {row['other_profile']} | {row['other_role']} | {fmt(row['combined_distance'])} | {fmt(row['coarse_distance'])} | {fmt(row['spectral_margin_gap'])} | {row['other_best_nontrivial_metric']} | {int(row['other_spectral_rank_nontrivial'])} | {int(row['comparison_rank'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren holdout-tie-break for en liten add_chord-skalaovergang.")
    lines.append("- Positivt signal her betyr bare at vi har et bedre grunnlag for a snakke om en smal familiespesifikk skalaovergang.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bo add_chord scale-jump holdout.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15bo_add_chord_scale_jump_holdout_target_summary.csv")
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15bo_add_chord_scale_jump_holdout_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15bo_add_chord_scale_jump_holdout_aggregate.csv")
    p.add_argument("--out-comparison-csv", type=str, default="Documentation/v15bo_add_chord_scale_jump_holdout_comparison.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bo_add_chord_scale_jump_holdout_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bo_add_chord_scale_jump_holdout.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bo_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bo.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    targets = sorted({int(profile["target_nodes"]) for profile in PROFILES})
    ensembles = v15.deep_ensembles(targets)
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    ensemble_by_target = {int(ens.target_nodes): ens for ens in ensembles}
    base_lookup = {(str(row["ensemble"]), int(row["growth_seed"])): dict(row) for row in base_rows}
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    rows: List[Dict[str, Any]] = []

    for profile in PROFILES:
        target = int(profile["target_nodes"])
        placement = int(profile["placement"])
        ens = ensemble_by_target[target]
        base = base_states[(ens.name, GROWTH_SEED)]
        base_row = base_lookup[(ens.name, GROWTH_SEED)]
        for seed_delta in SEED_DELTAS:
            run_seed = target * 100000 + GROWTH_SEED * 1000 + placement * 100 + int(seed_delta)
            res = v15q.run_defect_with_sets(
                base,
                params=params,
                seed=run_seed,
                steps=FULL_STEPS,
                perturbation="add_chord",
                center_token_index=placement,
                local_coupling="maximal",
                log_every=LOG_EVERY,
            )
            recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
            info = dict(res["perturbation_info"])
            support = list(info.get("support", []))
            core_shell = v15ac.core_shell_metrics(res["damaged_sets"], support)
            drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
            rows.append(
                {
                    "profile_label": str(profile["profile_label"]),
                    "role": str(profile["role"]),
                    "target_nodes": target,
                    "growth_seed": GROWTH_SEED,
                    "placement": placement,
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
                    "support_signature": ",".join(str(x) for x in support),
                    "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                    "core_shell_label": str(core_shell["label"]),
                    "core_share_of_union": safe_float(core_shell["core_share_of_union"]),
                    "shell_share_of_union": safe_float(core_shell["shell_share_of_union"]),
                    "rare_share_of_union": safe_float(core_shell["rare_share_of_union"]),
                    "mean_core_cover": safe_float(core_shell["mean_core_cover"]),
                    **drift,
                }
            )

    aggregate: List[Dict[str, Any]] = []
    for profile in PROFILES:
        group = [row for row in rows if str(row["profile_label"]) == str(profile["profile_label"])]
        aggregate.append(aggregate_profile(group, profile))

    aggregate.sort(key=lambda row: ("anchor" not in str(row["role"]), int(row["target_nodes"]), int(row["placement"])))
    comparisons = comparison_rows(aggregate)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) in targets]
    diagnosis = diagnosis_rows(target_summary, rows, comparisons)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, comparisons=comparisons, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bo operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en smal tie-break for en liten add_chord-skalaovergang, ikke som en generell skala-lov.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bo",
            "",
            "Denne runden sjekker om den beste 96-kandidaten virkelig ligner den sterke 48-familien, eller om den bare sa vidt vant over en naer nabo.",
            "",
            "Hvis 96/p3 fortsatt holder foran kontrollen pa nye seeds, er det et lite men ekte tegn pa at samme familie kan overleve ett lite skalahopp.",
        ]
    ) + "\n"

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_rows_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_comparison_csv, comparisons)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
