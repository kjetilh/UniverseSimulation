#!/usr/bin/env python3
"""v0.15bn add_chord scale-jump family map.

This round follows the v15bl/v15bm conclusion: stay inside the strongest
family rather than pushing a cross-family claim.

Question:
does the strongest add_chord spectral pocket at target 48, placement 2, have a
recognizable small scale-jump counterpart at target 96 under the same coarse
geometry and quasi-invariant observables?
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


TARGETS = (48, 96)
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2, 3)
SEED_DELTAS = (151, 179, 211, 239, 271, 307)
ANCHOR_TARGET = 48
ANCHOR_PLACEMENT = 2
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
NONTRIVIAL_METRICS = v15bl.NONTRIVIAL_REL_METRICS
COARSE_KEYS = [
    "mean_full_exact_return_rate",
    "mean_full_coarse_return_rate",
    "mean_core_share_of_union",
    "mean_shell_share_of_union",
    "mean_rare_share_of_union",
    "mean_core_cover",
]


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    return v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def aggregate_group(rows: Sequence[Mapping[str, Any]], *, target_nodes: int, placement: int) -> Dict[str, Any]:
    nontrivial_pairs = [
        (metric, mean_defined(safe_float(row[metric]) for row in rows))
        for metric in NONTRIVIAL_METRICS
    ]
    nontrivial_pairs.sort(key=lambda item: item[1])
    rank_map = {metric: idx for idx, (metric, _) in enumerate(nontrivial_pairs, start=1)}
    best_metric, best_mean = nontrivial_pairs[0]
    return {
        "target_nodes": int(target_nodes),
        "placement": int(placement),
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


def scale_match_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    agg_map = {(int(row["target_nodes"]), int(row["placement"])): dict(row) for row in aggregate}
    anchor = agg_map[(ANCHOR_TARGET, ANCHOR_PLACEMENT)]
    out: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        candidate = agg_map[(96, placement)]
        coarse_distance = sum(abs(safe_float(candidate[key]) - safe_float(anchor[key])) for key in COARSE_KEYS)
        spectral_margin_gap = abs(
            safe_float(candidate["mean_dim_minus_spectral"]) - safe_float(anchor["mean_dim_minus_spectral"])
        )
        combined_distance = coarse_distance + spectral_margin_gap
        out.append(
            {
                "anchor_target": ANCHOR_TARGET,
                "anchor_placement": ANCHOR_PLACEMENT,
                "candidate_target": 96,
                "candidate_placement": int(placement),
                "candidate_best_nontrivial_metric": str(candidate["best_nontrivial_metric"]),
                "candidate_spectral_rank_nontrivial": int(candidate["spectral_rank_nontrivial"]),
                "coarse_distance": coarse_distance,
                "spectral_margin_gap": spectral_margin_gap,
                "combined_distance": combined_distance,
                "candidate_dim_minus_spectral": safe_float(candidate["mean_dim_minus_spectral"]),
                "candidate_structured_core_shell_rate": safe_float(candidate["structured_core_shell_rate"]),
            }
        )
    out.sort(key=lambda row: safe_float(row["combined_distance"]))
    for idx, row in enumerate(out, start=1):
        row["match_rank"] = idx
    return out


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], match_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    best = dict(match_rows[0])
    runner_up = dict(match_rows[1]) if len(match_rows) > 1 else None
    gap_to_next = (
        safe_float(runner_up["combined_distance"]) - safe_float(best["combined_distance"])
        if runner_up is not None
        else float("nan")
    )
    if int(best["candidate_spectral_rank_nontrivial"]) == 1 and safe_float(best["combined_distance"]) <= 0.35 and gap_to_next >= 0.05:
        status = "small_scale_jump_match_supported"
        note = (
            f"Beste 96-match er p{int(best['candidate_placement'])} med combined distance {fmt(best['combined_distance'])} "
            f"og et tydelig gap til neste kandidat ({fmt(gap_to_next)})."
        )
        next_step = "holdout_best_scale_pair"
        next_note = "Neste steg bor vaere en liten holdout bare pa ankerparet 48/p2 vs den beste 96-matchen."
    elif int(best["candidate_spectral_rank_nontrivial"]) == 1:
        status = "small_scale_jump_match_weak"
        note = (
            f"Beste 96-match er p{int(best['candidate_placement'])}, men combined distance-gapet til neste kandidat er bare {fmt(gap_to_next)}."
        )
        next_step = "holdout_with_one_control"
        next_note = "Neste steg bor teste ankerparet mot en enkel 96-kontroll for a se om dette er ekte eller bare svak lokal konkurranse."
    else:
        status = "small_scale_jump_match_not_yet"
        note = "Ingen 96-kandidat holder samtidig ren spectral-rank og lav nok coarse-geometriavstand til ankeret."
        next_step = "explain_scale_break"
        next_note = "Neste steg bor forklare hvor skalasprekken sitter, ikke late som familien allerede skalerer."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsene er rent separert og alle add_chord-runs matcher onsket perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "anchor_profile",
            "status": "cycle_band_p2",
            "note": "Ankeret er target 48, placement 2, siden det var den sterkeste spektrale lommen i v15bl innen add_chord-bandet.",
        },
        {
            "diagnostic_family": "scale_jump_match",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, target_summary: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], match_rows: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bn: add_chord scale-jump family map")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om den sterkeste add_chord-lommen fra 48/p2 har en liten gjenkjennelig motpart ved target 96 pa samme coarse-geometri- og spectral-akse.")
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
    lines.append("## Aggregate per target/placement")
    lines.append("")
    lines.append("| target | placement | exact | coarse | core | shell | rare | spectral | dim | best non-trivial | spectral rank |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['target_nodes'])} | {int(row['placement'])} | {fmt(row['mean_full_exact_return_rate'])} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_core_share_of_union'])} | {fmt(row['mean_shell_share_of_union'])} | {fmt(row['mean_rare_share_of_union'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} | {fmt(row['mean_abs_delta_dim_proxy_rel'])} | {row['best_nontrivial_metric']} | {int(row['spectral_rank_nontrivial'])} |"
        )
    lines.append("")
    lines.append("## 48/p2 mot 96-kandidater")
    lines.append("")
    lines.append("| 96 placement | combined distance | coarse distance | spectral gap | best metric | spectral rank | match rank |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in match_rows:
        lines.append(
            f"| {int(row['candidate_placement'])} | {fmt(row['combined_distance'])} | {fmt(row['coarse_distance'])} | {fmt(row['spectral_margin_gap'])} | {row['candidate_best_nontrivial_metric']} | {int(row['candidate_spectral_rank_nontrivial'])} | {int(row['match_rank'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en liten add_chord-skalaovergang, ikke en bred ny scan.")
    lines.append("- Positivt signal her betyr bare at vi har en kandidat til samme familie over ett lite skalahopp.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bn add_chord scale-jump family map.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15bn_add_chord_scale_jump_target_summary.csv")
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15bn_add_chord_scale_jump_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15bn_add_chord_scale_jump_aggregate.csv")
    p.add_argument("--out-match-csv", type=str, default="Documentation/v15bn_add_chord_scale_jump_match_rows.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bn_add_chord_scale_jump_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bn_add_chord_scale_jump_family_map.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bn_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bn.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles(list(TARGETS))
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    ensemble_by_target = {int(ens.target_nodes): ens for ens in ensembles}
    base_lookup = {(str(row["ensemble"]), int(row["growth_seed"])): dict(row) for row in base_rows}
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    rows: List[Dict[str, Any]] = []

    for target in TARGETS:
        ens = ensemble_by_target[int(target)]
        base = base_states[(ens.name, GROWTH_SEED)]
        base_row = base_lookup[(ens.name, GROWTH_SEED)]
        for placement in PLACEMENTS:
            for seed_delta in SEED_DELTAS:
                run_seed = int(target) * 100000 + GROWTH_SEED * 1000 + int(placement) + int(seed_delta)
                res = v15q.run_defect_with_sets(
                    base,
                    params=params,
                    seed=run_seed,
                    steps=FULL_STEPS,
                    perturbation="add_chord",
                    center_token_index=int(placement),
                    local_coupling="maximal",
                    log_every=LOG_EVERY,
                )
                recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
                full_label = v15q.classify_recurrence_label(int(res["summary"]["final_alive"]), recurrence)
                info = dict(res["perturbation_info"])
                support = list(info.get("support", []))
                core_shell = v15ac.core_shell_metrics(res["damaged_sets"], support)
                drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                rows.append(
                    {
                        "target_nodes": int(target),
                        "growth_seed": GROWTH_SEED,
                        "placement": int(placement),
                        "seed_delta": int(seed_delta),
                        "run_seed": int(run_seed),
                        "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
                        "support_signature": ",".join(str(x) for x in support),
                        "full_label": full_label,
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
    for target in TARGETS:
        for placement in PLACEMENTS:
            group = [row for row in rows if int(row["target_nodes"]) == int(target) and int(row["placement"]) == int(placement)]
            aggregate.append(aggregate_group(group, target_nodes=int(target), placement=int(placement)))
    aggregate.sort(key=lambda row: (int(row["target_nodes"]), int(row["placement"])))

    match_rows = scale_match_rows(aggregate)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) in TARGETS]
    diagnosis = diagnosis_rows(target_summary, rows, aggregate, match_rows)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, match_rows=match_rows, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bn operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en liten add_chord-skalaovergang, ikke som en ny generell geometri-lov.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bn",
            "",
            "Denne runden sjekker om den sterkeste lille add_chord-familien ved storrelse 48 har en gjenkjennelig slektning ved storrelse 96.",
            "",
            "Poenget er ikke a bevise univers-lignende geometri, men a se om samme type lokale struktur faktisk overlever ett lite skalahopp.",
        ]
    ) + "\n"
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_rows_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_match_csv, match_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
