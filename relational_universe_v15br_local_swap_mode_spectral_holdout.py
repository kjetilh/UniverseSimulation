#!/usr/bin/env python3
"""v0.15br local_swap mode + spectral holdout.

Pivot after the add_chord scale-transfer track:
test whether the local_swap low_load_diffuse pocket survives as both
a mode label and a spectral pocket on fresh holdout seeds.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15aw_local_swap_core_shell_lab as v15aw
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 96
GROWTH_SEED = 202
PLACEMENTS = (1, 2, 3)
SEED_DELTAS = (503, 541, 577, 613, 647, 683)
NONTRIVIAL_METRICS = v15bl.NONTRIVIAL_REL_METRICS


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


def classify_mode(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    mean_load = mean_defined(safe_float(row["ball2_load"]) for row in rows)
    mean_stab = mean_defined(safe_float(row["full_stabilizer"]) for row in rows)
    out: List[Dict[str, Any]] = []
    for row in rows:
        load_delta = safe_float(row["ball2_load"]) - mean_load
        stab_delta = safe_float(row["full_stabilizer"]) - mean_stab
        if load_delta >= 0 and stab_delta >= 0:
            mode = "buffered_heavy_load"
        elif load_delta >= 0 and stab_delta < 0:
            mode = "rare_load_risk"
        elif load_delta < 0 and stab_delta < 0:
            mode = "low_load_diffuse"
        else:
            mode = "light_but_buffered"
        row = dict(row)
        row["load_delta_vs_mean"] = load_delta
        row["stabilizer_delta_vs_mean"] = stab_delta
        row["mode_label"] = mode
        out.append(row)
    return sorted(out, key=lambda row: int(row["placement"]))


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    per_placement: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        group = [row for row in rows if int(row["placement"]) == int(placement)]
        nontrivial_pairs = [
            (metric, mean_defined(safe_float(row[metric]) for row in group))
            for metric in NONTRIVIAL_METRICS
        ]
        nontrivial_pairs.sort(key=lambda item: item[1])
        rank_map = {metric: idx for idx, (metric, _) in enumerate(nontrivial_pairs, start=1)}
        best_metric, best_mean = nontrivial_pairs[0]
        per_placement.append(
            {
                "placement": int(placement),
                "n_runs": len(group),
                "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in group),
                "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in group),
                "stable_core_variable_shell_rate": mean_defined(
                    1.0 if str(row["core_shell_label"]) == "stable_core_variable_shell" else 0.0 for row in group
                ),
                "diffuse_shell_rate": mean_defined(
                    1.0 if str(row["core_shell_label"]) == "diffuse_shell_recurrence" else 0.0 for row in group
                ),
                "mean_core_share": mean_defined(safe_float(row["core_share_of_union"]) for row in group),
                "mean_shell_share": mean_defined(safe_float(row["shell_share_of_union"]) for row in group),
                "mean_rare_share": mean_defined(safe_float(row["rare_share_of_union"]) for row in group),
                "mean_support_ball_2": mean_defined(safe_float(row["support_ball_2"]) for row in group),
                "mean_shell2_over_shell1": mean_defined(safe_float(row["shell2_over_shell1"]) for row in group),
                "mean_abs_delta_spectral_radius_rel": mean_defined(
                    safe_float(row["abs_delta_spectral_radius_rel"]) for row in group
                ),
                "mean_abs_delta_dim_proxy_rel": mean_defined(
                    safe_float(row["abs_delta_dim_proxy_rel"]) for row in group
                ),
                "best_nontrivial_metric": best_metric,
                "best_nontrivial_mean_relative_drift": best_mean,
                "spectral_rank_nontrivial": rank_map["abs_delta_spectral_radius_rel"],
                "dim_rank_nontrivial": rank_map["abs_delta_dim_proxy_rel"],
                "mean_dim_minus_spectral": mean_defined(
                    safe_float(row["abs_delta_dim_proxy_rel"]) - safe_float(row["abs_delta_spectral_radius_rel"])
                    for row in group
                ),
            }
        )

    classified_input: List[Dict[str, Any]] = []
    for row in per_placement:
        classified_input.append(
            {
                "placement": int(row["placement"]),
                "coarse_return": safe_float(row["mean_full_coarse_return_rate"]),
                "core_share": safe_float(row["mean_core_share"]),
                "rare_share": safe_float(row["mean_rare_share"]),
                "ball2_load": safe_float(row["mean_support_ball_2"]),
                "full_stabilizer": (
                    safe_float(row["mean_full_coarse_return_rate"])
                    + safe_float(row["mean_core_share"])
                    + safe_float(row["mean_shell2_over_shell1"])
                ),
                **row,
            }
        )
    return classify_mode(classified_input)


def diagnosis_rows(target_summary: Sequence[Mapping[str, Any]], rows: Sequence[Mapping[str, Any]], aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    by = {int(row["placement"]): row for row in aggregate}
    p1 = by[1]
    p2 = by[2]
    p3 = by[3]
    if (
        str(p1["mode_label"]) == "buffered_heavy_load"
        and str(p2["mode_label"]) == "rare_load_risk"
        and str(p3["mode_label"]) == "low_load_diffuse"
        and int(p3["spectral_rank_nontrivial"]) == 1
        and safe_float(p3["mean_dim_minus_spectral"]) > 0.0
    ):
        status = "mode_plus_spectral_pocket_supported"
        note = "Holdouten bevarer det lokale moduskartet, og p3 holder fortsatt spectral rank 1 som low_load_diffuse-lomme."
        next_step = "compare_carrier_geometries"
        next_note = "Neste steg bor sammenligne coarse carrier-geometri direkte mellom add_chord og local_swap, siden local_swap-lommen holder bedre lokalt."
    elif int(p3["spectral_rank_nontrivial"]) == 1:
        status = "spectral_pocket_without_clean_mode_hold"
        note = "p3 holder spectral rank 1, men moduskartet holder ikke rent nok pa holdout."
        next_step = "explain_mode_drift"
        next_note = "Neste steg bor forklare hvilken del av moduskartet som driver pa holdout."
    else:
        status = "mode_plus_spectral_pocket_not_yet"
        note = "Holdouten bevarer ikke low_load_diffuse som en ren spectral+mode-lomme."
        next_step = "pivot_again"
        next_note = "Neste steg bor bytte carrier-retning eller observabel, ikke presse videre pa denne local_swap-lommen."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsen er ren og alle local_swap-holdout-runs matcher onsket perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "local_swap_mode_spectral_holdout",
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
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15br: local_swap mode spectral holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om local_swap sin `low_load_diffuse`-lomme holder pa friske seeds som bade modus og spectral lomme.")
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
    lines.append("## Holdout mode map")
    lines.append("")
    lines.append("| placement | mode | exact | coarse | core | shell | rare | ball2 load | stabilizer | spectral | dim | spectral rank |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['placement'])} | {row['mode_label']} | {fmt(row['mean_full_exact_return_rate'])} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_core_share'])} | {fmt(row['mean_shell_share'])} | {fmt(row['mean_rare_share'])} | {fmt(row['mean_support_ball_2'])} | {fmt(row['full_stabilizer'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} | {fmt(row['mean_abs_delta_dim_proxy_rel'])} | {int(row['spectral_rank_nontrivial'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en smal holdout av local_swap-lommen, ikke en bred ny modescan.")
    lines.append("- Positivt signal her betyr bare at local_swap er et bedre neste carrier-spor for geometri/quasi-invariant-arbeid enn add_chord akkurat na.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15br local_swap mode + spectral holdout.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15br_local_swap_mode_spectral_holdout_target_summary.csv")
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15br_local_swap_mode_spectral_holdout_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15br_local_swap_mode_spectral_holdout_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15br_local_swap_mode_spectral_holdout_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15br_local_swap_mode_spectral_holdout.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15br_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15br.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    base_row = next(row for row in base_rows if int(row["target_nodes"]) == TARGET and int(row["growth_seed"]) == GROWTH_SEED)
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    rows: List[Dict[str, Any]] = []

    for placement in PLACEMENTS:
        for seed_delta in SEED_DELTAS:
            run_seed = TARGET * 100000 + GROWTH_SEED * 1000 + placement * 100 + int(seed_delta)
            res = v15q.run_defect_with_sets(
                base_state,
                params=params,
                seed=run_seed,
                steps=v15aw.FULL_STEPS,
                perturbation="local_swap",
                center_token_index=placement,
                local_coupling="maximal",
                log_every=v15aw.LOG_EVERY,
            )
            recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
            info = dict(res["perturbation_info"])
            support = [int(x) for x in info.get("support", [])]
            core_shell = v15aw.core_shell_metrics(res["damaged_sets"], support)
            geom = v14c.support_geometry_features(base_state, support)
            drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
            rows.append(
                {
                    "target_nodes": TARGET,
                    "growth_seed": GROWTH_SEED,
                    "placement": int(placement),
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match("local_swap", str(info.get("type", "unknown")))),
                    "support_signature": ",".join(str(x) for x in support),
                    "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                    "core_shell_label": str(core_shell["label"]),
                    "core_share_of_union": safe_float(core_shell["core_share_of_union"]),
                    "shell_share_of_union": safe_float(core_shell["shell_share_of_union"]),
                    "rare_share_of_union": safe_float(core_shell["rare_share_of_union"]),
                    "mean_support_degree": safe_float(geom["mean_support_degree"]),
                    "support_ball_2": safe_float(geom["support_ball_2"]),
                    "shell2_over_shell1": safe_float(geom["shell2_over_shell1"]),
                    **drift,
                }
            )

    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    aggregate = aggregate_rows(rows)
    diagnosis = diagnosis_rows(target_summary, rows, aggregate)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15br operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en smal local_swap-holdout, ikke som en ny bred modescale.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15br",
            "",
            "Denne runden sjekker om den mest lovende local_swap-retningen fortsatt ser spesiell ut pa nye tilfeldige startvalg.",
            "",
            "Poenget er a se om den ikke bare vinner i ettertid, men faktisk holder som et lite lokalt monster av samme type igjen og igjen.",
        ]
    ) + "\n"
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_rows_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
