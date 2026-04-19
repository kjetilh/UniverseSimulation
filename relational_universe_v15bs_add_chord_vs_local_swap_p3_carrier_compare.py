#!/usr/bin/env python3
"""v0.15bs add_chord vs local_swap carrier compare at 96/p3.

After v15bq-v15br, compare the two carrier candidates directly at the same
target/growth-seed/placement to see whether geometry and spectral cleanliness
split across perturbation type.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15ad_add_chord_boundary_shell_lab as v15ad
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15aw_local_swap_core_shell_lab as v15aw
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 96
GROWTH_SEED = 202
PLACEMENT = 3
SEED_DELTAS = (719, 751, 787, 823, 859, 887)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
NONTRIVIAL_METRICS = v15bl.NONTRIVIAL_REL_METRICS
PERTURBATIONS = ("add_chord", "local_swap")


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


def aggregate_perturbation(rows: Sequence[Mapping[str, Any]], perturbation: str) -> Dict[str, Any]:
    nontrivial_pairs = [
        (metric, mean_defined(safe_float(row[metric]) for row in rows))
        for metric in NONTRIVIAL_METRICS
    ]
    nontrivial_pairs.sort(key=lambda item: item[1])
    rank_map = {metric: idx for idx, (metric, _) in enumerate(nontrivial_pairs, start=1)}
    best_metric, best_mean = nontrivial_pairs[0]
    return {
        "perturbation": perturbation,
        "n_runs": len(rows),
        "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in rows),
        "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in rows),
        "mean_core_share": mean_defined(safe_float(row["core_share_of_union"]) for row in rows),
        "mean_shell_share": mean_defined(safe_float(row["shell_share_of_union"]) for row in rows),
        "mean_rare_share": mean_defined(safe_float(row["rare_share_of_union"]) for row in rows),
        "mean_shell_refresh": mean_defined(safe_float(row["mean_shell_refresh"]) for row in rows),
        "mean_burst_rate": mean_defined(safe_float(row["burst_rate"]) for row in rows),
        "mean_shell_cover": mean_defined(safe_float(row["mean_shell_cover"]) for row in rows),
        "mean_shell_connected_rate": mean_defined(safe_float(row["shell_connected_rate"]) for row in rows),
        "mean_shell_fragmented_rate": mean_defined(safe_float(row["shell_fragmented_rate"]) for row in rows),
        "mean_attachment_node_frac": mean_defined(safe_float(row["mean_attachment_node_frac"]) for row in rows),
        "mean_abs_delta_spectral_radius_rel": mean_defined(safe_float(row["abs_delta_spectral_radius_rel"]) for row in rows),
        "mean_abs_delta_dim_proxy_rel": mean_defined(safe_float(row["abs_delta_dim_proxy_rel"]) for row in rows),
        "best_nontrivial_metric": best_metric,
        "best_nontrivial_mean_relative_drift": best_mean,
        "spectral_rank_nontrivial": rank_map["abs_delta_spectral_radius_rel"],
        "dim_rank_nontrivial": rank_map["abs_delta_dim_proxy_rel"],
        "mean_dim_minus_spectral": mean_defined(
            safe_float(row["abs_delta_dim_proxy_rel"]) - safe_float(row["abs_delta_spectral_radius_rel"]) for row in rows
        ),
    }


def comparison_row(aggregate: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    by = {str(row["perturbation"]): dict(row) for row in aggregate}
    add = by["add_chord"]
    swap = by["local_swap"]
    return {
        "compare_label": "add_chord_vs_local_swap_at_96_p3",
        "coarse_return_gap_add_minus_swap": safe_float(add["mean_full_coarse_return_rate"]) - safe_float(swap["mean_full_coarse_return_rate"]),
        "core_share_gap_add_minus_swap": safe_float(add["mean_core_share"]) - safe_float(swap["mean_core_share"]),
        "rare_share_gap_add_minus_swap": safe_float(add["mean_rare_share"]) - safe_float(swap["mean_rare_share"]),
        "shell_refresh_gap_add_minus_swap": safe_float(add["mean_shell_refresh"]) - safe_float(swap["mean_shell_refresh"]),
        "attachment_gap_add_minus_swap": safe_float(add["mean_attachment_node_frac"]) - safe_float(swap["mean_attachment_node_frac"]),
        "spectral_gap_swap_minus_add": safe_float(add["mean_abs_delta_spectral_radius_rel"]) - safe_float(swap["mean_abs_delta_spectral_radius_rel"]),
        "dim_minus_spectral_gap_swap_minus_add": safe_float(swap["mean_dim_minus_spectral"]) - safe_float(add["mean_dim_minus_spectral"]),
        "add_spectral_rank": int(add["spectral_rank_nontrivial"]),
        "swap_spectral_rank": int(swap["spectral_rank_nontrivial"]),
    }


def diagnosis_rows(target_summary: Sequence[Mapping[str, Any]], rows: Sequence[Mapping[str, Any]], aggregate: Sequence[Mapping[str, Any]], compare: Mapping[str, Any]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    coarse_gap = safe_float(compare["coarse_return_gap_add_minus_swap"])
    core_gap = safe_float(compare["core_share_gap_add_minus_swap"])
    spectral_gap = safe_float(compare["spectral_gap_swap_minus_add"])
    dim_margin_gap = safe_float(compare["dim_minus_spectral_gap_swap_minus_add"])

    if coarse_gap > 0.10 and core_gap > 0.10 and spectral_gap > 0.02 and dim_margin_gap > 0.0:
        status = "split_carrier_advantage_supported"
        note = (
            "add_chord holder tydelig sterkere skadegeometri ved samme locus, mens local_swap holder tydelig renere spectral drift. "
            "Carrier-fordelen splitter derfor mellom geometri og quasi-invariant-renhet."
        )
        next_step = "design_dual_track"
        next_note = "Neste steg bor vaere en liten dual-track plan: add_chord for coarse geometry, local_swap for spectral conditional quasi-invariants."
    elif spectral_gap > 0.02:
        status = "local_swap_spectral_edge_supported"
        note = "local_swap holder renere spectral drift ved samme locus, men den geometriske fordelen hos add_chord er ikke sterk nok til en ren splittlesning."
        next_step = "stress_local_swap_geometry"
        next_note = "Neste steg bor stresse local_swap-geometrien litt hardere for a se om den kan baere begge sider."
    elif coarse_gap > 0.10:
        status = "add_chord_geometry_edge_supported"
        note = "add_chord holder tydelig bedre coarse carrier-geometri ved samme locus, men den spektrale gevinsten er ikke ren nok hos local_swap."
        next_step = "stress_add_chord_spectral"
        next_note = "Neste steg bor teste om add_chord kan fa en skarpere conditional spectral-lesning ved et annet lokalt locus."
    else:
        status = "carrier_compare_still_mixed"
        note = "Carrier-sammenlikningen ved samme locus er fortsatt for blandet til en ren delt arbeidsdeling."
        next_step = "new_carrier_observable"
        next_note = "Neste steg bor bruke en ny carrier-observabel, ikke mer av samme p3-sammenlikning."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsen er ren og alle p3-runs matcher onsket perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "carrier_compare",
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
    compare: Mapping[str, Any],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bs: add_chord vs local_swap carrier compare at 96/p3")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden sammenlikner add_chord og local_swap direkte pa samme base, samme placement og samme holdout-seeds for a se om carrier-fordelen splitter mellom geometri og spectral renhet.")
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
    lines.append("## Carrier summary")
    lines.append("")
    lines.append("| perturbation | exact | coarse | core | shell | rare | refresh | attach | spectral | dim | spectral rank |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['perturbation']} | {fmt(row['mean_full_exact_return_rate'])} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_core_share'])} | {fmt(row['mean_shell_share'])} | {fmt(row['mean_rare_share'])} | {fmt(row['mean_shell_refresh'])} | {fmt(row['mean_attachment_node_frac'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} | {fmt(row['mean_abs_delta_dim_proxy_rel'])} | {int(row['spectral_rank_nontrivial'])} |"
        )
    lines.append("")
    lines.append("## Comparison deltas")
    lines.append("")
    lines.append("| coarse gap add-swap | core gap add-swap | rare gap add-swap | spectral gap swap-add | dim-minus-spectral gap swap-add |")
    lines.append("| --- | --- | --- | --- | --- |")
    lines.append(
        f"| {fmt(compare['coarse_return_gap_add_minus_swap'])} | {fmt(compare['core_share_gap_add_minus_swap'])} | {fmt(compare['rare_share_gap_add_minus_swap'])} | {fmt(compare['spectral_gap_swap_minus_add'])} | {fmt(compare['dim_minus_spectral_gap_swap_minus_add'])} |"
    )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren carrier-sammenlikning ved samme lokale locus.")
    lines.append("- Positivt signal her betyr ikke at noen perturbasjon er universelt best, men at de kan egne seg til ulike deler av videre geometri-/quasi-invariant-arbeid.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bs add_chord vs local_swap carrier compare.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15bs_add_chord_vs_local_swap_p3_target_summary.csv")
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15bs_add_chord_vs_local_swap_p3_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15bs_add_chord_vs_local_swap_p3_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15bs_add_chord_vs_local_swap_p3_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bs_add_chord_vs_local_swap_p3_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bs_add_chord_vs_local_swap_p3_carrier_compare.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bs_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bs.md")
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

    for perturbation in PERTURBATIONS:
        for seed_delta in SEED_DELTAS:
            run_seed = TARGET * 100000 + GROWTH_SEED * 1000 + PLACEMENT * 100 + int(seed_delta)
            if perturbation == "local_swap":
                run_seed += 7
            res = v15ae.run_defect_with_control_graphs(
                base_state,
                params=params,
                seed=run_seed,
                steps=FULL_STEPS,
                perturbation=perturbation,
                center_token_index=PLACEMENT,
                local_coupling="maximal",
                log_every=LOG_EVERY,
            )
            recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
            info = dict(res["perturbation_info"])
            support = [int(x) for x in info.get("support", [])]
            if perturbation == "add_chord":
                core_shell = v15ac.core_shell_metrics(res["damaged_sets"], support)
            else:
                core_shell = v15aw.core_shell_metrics(res["damaged_sets"], support)
            shell = v15ad.shell_metrics(res["log_rows"], res["damaged_sets"])
            partition = v15ae.occupancy_partition(res["damaged_sets"])
            snap_rows = v15ae.shell_snapshot_rows(
                placement=PLACEMENT,
                seed_delta=seed_delta,
                run_seed=run_seed,
                support_signature=",".join(str(x) for x in support),
                core_nodes=set(partition["core_nodes"]),
                shell_nodes=set(partition["shell_nodes"]),
                log_rows=res["log_rows"],
                damaged_sets=res["damaged_sets"],
                control_graphs=res["control_graphs"],
            )
            active_rows = [row for row in snap_rows if int(row["shell_active_nodes"]) > 0]
            drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
            rows.append(
                {
                    "perturbation": perturbation,
                    "target_nodes": TARGET,
                    "growth_seed": GROWTH_SEED,
                    "placement": PLACEMENT,
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
                    "support_signature": ",".join(str(x) for x in support),
                    "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                    "core_share_of_union": safe_float(core_shell["core_share_of_union"]),
                    "shell_share_of_union": safe_float(core_shell["shell_share_of_union"]),
                    "rare_share_of_union": safe_float(core_shell["rare_share_of_union"]),
                    "mean_shell_refresh": safe_float(shell["mean_shell_refresh"]),
                    "burst_rate": safe_float(shell["burst_rate"]),
                    "mean_shell_cover": safe_float(shell["mean_shell_cover"]),
                    "shell_connected_rate": mean_defined(float(row["shell_connected_active"]) for row in active_rows) if active_rows else float("nan"),
                    "shell_fragmented_rate": mean_defined(float(row["shell_fragmented_active"]) for row in active_rows) if active_rows else float("nan"),
                    "mean_attachment_node_frac": mean_defined(
                        safe_float(row["shell_attachment_node_frac"])
                        for row in active_rows
                        if math.isfinite(safe_float(row["shell_attachment_node_frac"]))
                    ),
                    **drift,
                }
            )

    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    aggregate = [aggregate_perturbation([row for row in rows if str(row["perturbation"]) == perturbation], perturbation) for perturbation in PERTURBATIONS]
    compare = comparison_row(aggregate)
    diagnosis = diagnosis_rows(target_summary, rows, aggregate, compare)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, compare=compare, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bs operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en direkte carrier-sammenlikning ved samme locus, ikke som en bred ny scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bs",
            "",
            "Denne runden sammenlikner to ulike forstyrrelser pa nøyaktig samme sted i modellen for a se hva som holder best sammen.",
            "",
            "Tanken er at den ene kanskje lager en sterkere grov form, mens den andre holder en renere nesten-bevart struktur.",
        ]
    ) + "\n"
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_rows_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_compare_csv, [compare])
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
