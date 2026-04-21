#!/usr/bin/env python3
"""v0.15bw family-structure holdout.

v15bv found weak family structure at target 96 / growth seed 202:

- six profiles formed a broad geometry_core_family
- add_chord_p1 looked like an expanded_shell_family outlier
- local_swap_p3 looked like a spectral_core_family outlier
- no pair was near-symmetric in both support and carrier feature space

This script is the narrow holdout before any scale jump. It reuses the same
observables and labels, but runs fresh seeds and treats the v15bv family map as
a falsifiable expectation.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15ad_add_chord_boundary_shell_lab as v15ad
import relational_universe_v15aw_local_swap_core_shell_lab as v15aw
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15bv_family_structure_symmetry_lab as v15bv
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 96
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2, 3)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (1061, 1091, 1123, 1151, 1181, 1213)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY

EXPECTED_FAMILY = {
    "add_chord_p0": "geometry_core_family",
    "add_chord_p1": "expanded_shell_family",
    "add_chord_p2": "geometry_core_family",
    "add_chord_p3": "geometry_core_family",
    "local_swap_p0": "geometry_core_family",
    "local_swap_p1": "geometry_core_family",
    "local_swap_p2": "geometry_core_family",
    "local_swap_p3": "spectral_core_family",
}


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


def run_seed_for(*, perturbation: str, placement: int, seed_delta: int) -> int:
    perturbation_offset = {"add_chord": 113, "local_swap": 157}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def with_holdout_columns(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for row in aggregate:
        out = dict(row)
        profile = str(out["profile_label"])
        expected = EXPECTED_FAMILY[profile]
        observed = str(out["family_label"])
        out["expected_family_label"] = expected
        out["family_match_expected"] = int(observed == expected)
        out["expected_geometry_core_member"] = int(expected == "geometry_core_family")
        out["geometry_core_retained"] = int(expected == "geometry_core_family" and observed == "geometry_core_family")
        out["outlier_retained"] = int(expected != "geometry_core_family" and observed == expected)
        return_gap = safe_float(out["mean_full_coarse_return_rate"]) - 0.72
        core_gap = safe_float(out["mean_core_share"]) - 0.50
        rare_gap = 0.15 - safe_float(out["mean_rare_share"])
        out["geometry_core_min_margin"] = min(return_gap, core_gap, rare_gap)
        rows.append(out)
    return rows


def holdout_summary_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    geometry_expected = [row for row in aggregate if int(row["expected_geometry_core_member"]) == 1]
    outliers = [row for row in aggregate if int(row["expected_geometry_core_member"]) == 0]
    all_rows = list(aggregate)
    full_near = [
        row
        for row in v15bv.pairwise_rows(aggregate)
        if str(row["symmetry_label"]) == "support_and_carrier_near_symmetry"
    ]
    return [
        {
            "summary_family": "all_profiles",
            "n_profiles": len(all_rows),
            "match_rate": mean_defined(float(row["family_match_expected"]) for row in all_rows),
            "geometry_core_retention_rate": mean_defined(float(row["geometry_core_retained"]) for row in geometry_expected),
            "outlier_retention_rate": mean_defined(float(row["outlier_retained"]) for row in outliers),
            "mean_geometry_core_min_margin": mean_defined(safe_float(row["geometry_core_min_margin"]) for row in geometry_expected),
            "full_near_symmetry_count": len(full_near),
        },
        {
            "summary_family": "expected_geometry_core",
            "n_profiles": len(geometry_expected),
            "match_rate": mean_defined(float(row["family_match_expected"]) for row in geometry_expected),
            "geometry_core_retention_rate": mean_defined(float(row["geometry_core_retained"]) for row in geometry_expected),
            "outlier_retention_rate": float("nan"),
            "mean_geometry_core_min_margin": mean_defined(safe_float(row["geometry_core_min_margin"]) for row in geometry_expected),
            "full_near_symmetry_count": len(full_near),
        },
        {
            "summary_family": "expected_outliers",
            "n_profiles": len(outliers),
            "match_rate": mean_defined(float(row["family_match_expected"]) for row in outliers),
            "geometry_core_retention_rate": float("nan"),
            "outlier_retention_rate": mean_defined(float(row["outlier_retained"]) for row in outliers),
            "mean_geometry_core_min_margin": float("nan"),
            "full_near_symmetry_count": len(full_near),
        },
    ]


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    summary: Sequence[Mapping[str, Any]],
    pairwise: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    all_summary = next(row for row in summary if str(row["summary_family"]) == "all_profiles")
    out_summary = next(row for row in summary if str(row["summary_family"]) == "expected_outliers")
    geom_summary = next(row for row in summary if str(row["summary_family"]) == "expected_geometry_core")
    match_rate = safe_float(all_summary["match_rate"], 0.0)
    geom_rate = safe_float(geom_summary["geometry_core_retention_rate"], 0.0)
    outlier_rate = safe_float(out_summary["outlier_retention_rate"], 0.0)
    full_near = [row for row in pairwise if str(row["symmetry_label"]) == "support_and_carrier_near_symmetry"]
    geometry_members = [
        str(row["profile_label"])
        for row in aggregate
        if str(row["family_label"]) == "geometry_core_family"
    ]

    if match_rate >= 0.875 and geom_rate >= 0.90 and outlier_rate >= 0.50:
        status = "family_structure_holdout_supported"
        note = (
            f"Holdouten matcher {fmt(match_rate)} av v15bv family-map; geometry-core-retention er {fmt(geom_rate)} "
            f"og outlier-retention er {fmt(outlier_rate)}."
        )
        next_step = "scale_jump_with_family_controls"
        next_note = "Neste steg bor bruke family-map som kontroll ved et nytt skalahopp, ikke flere target-96 label-runder."
    elif geom_rate >= 0.90:
        status = "geometry_core_plateau_supported_outliers_unstable"
        note = (
            f"Geometry-core-plateauet holder ({fmt(geom_rate)}), men outlier-rollene holder svakere ({fmt(outlier_rate)})."
        )
        next_step = "scale_jump_geometry_core_only"
        next_note = "Neste steg bor bare ta med geometry-core-plateauet som kontroll inn i et skalahopp."
    elif match_rate >= 0.625:
        status = "family_structure_weak_holdout"
        note = f"Family-map holder delvis ({fmt(match_rate)}), men ikke sterkt nok til mer lokal target-96 raffinering."
        next_step = "new_scale_jump"
        next_note = "Neste steg bor vaere skalahopp; behold v15bv/v15bw som svake kontroller, ikke som fast familieinndeling."
    else:
        status = "family_structure_not_replicated"
        note = f"Family-map replikerer ikke rent i holdout ({fmt(match_rate)})."
        next_step = "new_scale_jump"
        next_note = "Neste steg bor vaere nytt skalahopp heller enn mer family-threshold-tuning ved target 96."

    symmetry_status = "no_full_near_symmetry" if not full_near else "full_near_symmetry_candidate"
    symmetry_note = (
        "Ingen profilpar er naere i bade support- og carrier-feature-rom i holdouten."
        if not full_near
        else f"{len(full_near)} profilpar er full feature-level near-symmetry-kandidater i holdouten."
    )

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Enten startstorrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        },
        {
            "diagnostic_family": "family_holdout",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "geometry_core_members",
            "status": "observed",
            "note": ";".join(geometry_members),
        },
        {
            "diagnostic_family": "symmetry_holdout",
            "status": symmetry_status,
            "note": symmetry_note,
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
    summary: Sequence[Mapping[str, Any]],
    pairwise: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bw: family-structure holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om family-map fra `v15bv` holder pa friske seeds for samme target/base.")
    lines.append("Dette er en holdout, ikke et nytt placement-sok og ikke et skalahopp.")
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
    lines.append("## Holdout family map")
    lines.append("")
    lines.append("| profile | expected | observed | match | coarse | core | shell | rare | spectral rel | geom margin |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {row['expected_family_label']} | {row['family_label']} | {int(row['family_match_expected'])} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_core_share'])} | {fmt(row['mean_shell_share'])} | {fmt(row['mean_rare_share'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} | {fmt(row['geometry_core_min_margin'])} |"
        )
    lines.append("")
    lines.append("## Holdout summary")
    lines.append("")
    lines.append("| group | n | match rate | geometry retention | outlier retention | mean geom margin | full near symmetries |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in summary:
        lines.append(
            f"| {row['summary_family']} | {int(row['n_profiles'])} | {fmt(row['match_rate'])} | {fmt(row['geometry_core_retention_rate'])} | {fmt(row['outlier_retention_rate'])} | {fmt(row['mean_geometry_core_min_margin'])} | {int(row['full_near_symmetry_count'])} |"
        )
    lines.append("")
    lines.append("## Beste pairwise feature-avstander")
    lines.append("")
    lines.append("| rank | profile A | profile B | family match | support dist | carrier dist | combined | symmetry label |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in pairwise[:8]:
        lines.append(
            f"| {int(row['combined_rank'])} | {row['profile_a']} | {row['profile_b']} | {int(row['family_match'])} | {fmt(row['support_distance'])} | {fmt(row['carrier_distance'])} | {fmt(row['combined_distance'])} | {row['symmetry_label']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette tester replikerbarhet av en heuristisk family-map, ikke eksakte arter.")
    lines.append("- Hvis plateauet holder bedre enn outlier-rollene, skal bare plateauet brukes som kontroll i neste skalahopp.")
    lines.append("- Full feature-level near-symmetry ville krevd lav avstand i bade support- og carrier-rom; support-only likhet er ikke nok.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bw family-structure holdout.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15bw_family_structure_holdout_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15bw_family_structure_holdout_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15bw_family_structure_holdout_aggregate.csv")
    p.add_argument("--out-summary-csv", type=str, default="Documentation/v15bw_family_structure_holdout_summary.csv")
    p.add_argument("--out-pairwise-csv", type=str, default="Documentation/v15bw_family_structure_holdout_pairwise.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bw_family_structure_holdout_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bw_family_structure_holdout_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bw_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bw.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    base_row = next(row for row in base_rows if int(row["target_nodes"]) == TARGET and int(row["growth_seed"]) == GROWTH_SEED)
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    run_rows: List[Dict[str, Any]] = []

    for perturbation in PERTURBATIONS:
        for placement in PLACEMENTS:
            for seed_delta in SEED_DELTAS:
                run_seed = run_seed_for(perturbation=perturbation, placement=placement, seed_delta=seed_delta)
                res = v15q.run_defect_with_sets(
                    base_state,
                    params=params,
                    seed=run_seed,
                    steps=FULL_STEPS,
                    perturbation=perturbation,
                    center_token_index=placement,
                    local_coupling="maximal",
                    log_every=LOG_EVERY,
                )
                recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
                info = dict(res["perturbation_info"])
                support = [int(x) for x in info.get("support", [])]
                core_shell = (
                    v15ac.core_shell_metrics(res["damaged_sets"], support)
                    if perturbation == "add_chord"
                    else v15aw.core_shell_metrics(res["damaged_sets"], support)
                )
                shell = v15ad.shell_metrics(res["log_rows"], res["damaged_sets"])
                support_features = v14c.support_geometry_features(base_state, support)
                drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                run_rows.append(
                    {
                        "profile_label": v15bv.profile_label(perturbation, placement),
                        "perturbation": perturbation,
                        "target_nodes": TARGET,
                        "growth_seed": GROWTH_SEED,
                        "placement": int(placement),
                        "seed_delta": int(seed_delta),
                        "run_seed": int(run_seed),
                        "requested_match": int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
                        "support_signature": ",".join(str(x) for x in support),
                        "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                        "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                        "core_share_of_union": safe_float(core_shell["core_share_of_union"]),
                        "shell_share_of_union": safe_float(core_shell["shell_share_of_union"]),
                        "rare_share_of_union": safe_float(core_shell["rare_share_of_union"]),
                        "mean_core_cover": safe_float(core_shell["mean_core_cover"]),
                        "core_shell_label": str(core_shell["label"]),
                        "mean_shell_refresh": safe_float(shell["mean_shell_refresh"]),
                        "burst_rate": safe_float(shell["burst_rate"]),
                        "mean_shell_cover": safe_float(shell["mean_shell_cover"]),
                        "sd_boundary_to_volume": safe_float(shell["sd_boundary_to_volume"]),
                        **support_features,
                        **drift,
                    }
                )

    aggregate = [
        v15bv.aggregate_profile(
            [row for row in run_rows if str(row["perturbation"]) == perturbation and int(row["placement"]) == int(placement)],
            perturbation=perturbation,
            placement=placement,
        )
        for perturbation in PERTURBATIONS
        for placement in PLACEMENTS
    ]
    aggregate = with_holdout_columns(sorted(aggregate, key=lambda row: (str(row["perturbation"]), int(row["placement"]))))
    summary = holdout_summary_rows(aggregate)
    pairwise = v15bv.pairwise_rows(aggregate)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        aggregate=aggregate,
        summary=summary,
        pairwise=pairwise,
    )
    report_md = build_report(
        target_summary=target_summary,
        aggregate=aggregate,
        summary=summary,
        pairwise=pairwise,
        diagnosis=diagnosis,
    )
    op_md = "\n".join(
        [
            "# v0.15bw operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Bruk denne runden som holdout av v15bv family-map. Hvis den peker mot skalahopp, ikke press flere target-96 terskler.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bw",
            "",
            "Forrige runde antydet at de fleste lokale forstyrrelsene pa samme storrelse ligger pa et felles grovt plateau, mens to profiler skiller seg ut.",
            "",
            "Denne runden sjekker om den historien gjentar seg med nye tilfeldige seeds. Hvis ikke, er det et tegn pa at vi bor hoppe til en ny storrelse i stedet for a finpusse samme kart.",
        ]
    ) + "\n"

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_summary_csv, summary)
    write_csv(args.out_pairwise_csv, pairwise)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
