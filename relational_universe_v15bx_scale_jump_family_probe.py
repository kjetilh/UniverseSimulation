#!/usr/bin/env python3
"""v0.15bx scale-jump family probe.

v15bw showed that the target-96 family map from v15bv did not replicate cleanly.
This is the promised scale jump: keep the same observable stack, but move to
target 192 and treat the family labels only as exploratory controls.

This is not a broad placement search. It uses the same four placements and two
perturbation types as v15bv/v15bw.
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


TARGET = 192
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2, 3)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (1409, 1433, 1459, 1487)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
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


def run_seed_for(*, perturbation: str, placement: int, seed_delta: int) -> int:
    perturbation_offset = {"add_chord": 211, "local_swap": 257}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def aggregate_profile(rows: Sequence[Mapping[str, Any]], *, perturbation: str, placement: int) -> Dict[str, Any]:
    nontrivial_pairs = [
        (metric, mean_defined(safe_float(row[metric]) for row in rows))
        for metric in NONTRIVIAL_METRICS
    ]
    nontrivial_pairs.sort(key=lambda item: item[1])
    rank_map = {metric: idx for idx, (metric, _) in enumerate(nontrivial_pairs, start=1)}
    best_metric, best_mean = nontrivial_pairs[0]
    out: Dict[str, Any] = {
        "profile_label": v15bv.profile_label(perturbation, placement),
        "perturbation": perturbation,
        "target_nodes": TARGET,
        "growth_seed": GROWTH_SEED,
        "placement": int(placement),
        "n_runs": len(rows),
        "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in rows),
        "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in rows),
        "mean_core_share": mean_defined(safe_float(row["core_share_of_union"]) for row in rows),
        "mean_shell_share": mean_defined(safe_float(row["shell_share_of_union"]) for row in rows),
        "mean_rare_share": mean_defined(safe_float(row["rare_share_of_union"]) for row in rows),
        "mean_mean_core_cover": mean_defined(safe_float(row["mean_core_cover"]) for row in rows),
        "mean_shell_refresh": mean_defined(safe_float(row["mean_shell_refresh"]) for row in rows),
        "mean_burst_rate": mean_defined(safe_float(row["burst_rate"]) for row in rows),
        "mean_shell_cover": mean_defined(safe_float(row["mean_shell_cover"]) for row in rows),
        "mean_boundary_to_volume_sd": mean_defined(safe_float(row["sd_boundary_to_volume"]) for row in rows),
        "mean_abs_delta_spectral_radius_rel": mean_defined(safe_float(row["abs_delta_spectral_radius_rel"]) for row in rows),
        "mean_abs_delta_dim_proxy_rel": mean_defined(safe_float(row["abs_delta_dim_proxy_rel"]) for row in rows),
        "mean_dim_minus_spectral": mean_defined(
            safe_float(row["abs_delta_dim_proxy_rel"]) - safe_float(row["abs_delta_spectral_radius_rel"])
            for row in rows
        ),
        "best_nontrivial_metric": best_metric,
        "best_nontrivial_mean_relative_drift": best_mean,
        "spectral_rank_nontrivial": rank_map["abs_delta_spectral_radius_rel"],
        "dim_rank_nontrivial": rank_map["abs_delta_dim_proxy_rel"],
    }
    for key in v15bv.SUPPORT_DISTANCE_KEYS:
        out[key] = mean_defined(safe_float(row[key]) for row in rows)
    out["family_label"] = v15bv.family_label(out)
    return out


def family_summary_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    labels = sorted({str(row["family_label"]) for row in aggregate})
    out: List[Dict[str, Any]] = []
    for label in labels:
        group = [row for row in aggregate if str(row["family_label"]) == label]
        out.append(
            {
                "family_label": label,
                "n_profiles": len(group),
                "profiles": ";".join(str(row["profile_label"]) for row in group),
                "perturbations": ";".join(sorted({str(row["perturbation"]) for row in group})),
                "placements": ";".join(str(row["placement"]) for row in group),
                "mean_coarse_return": mean_defined(safe_float(row["mean_full_coarse_return_rate"]) for row in group),
                "mean_core_share": mean_defined(safe_float(row["mean_core_share"]) for row in group),
                "mean_rare_share": mean_defined(safe_float(row["mean_rare_share"]) for row in group),
                "mean_spectral_rel": mean_defined(safe_float(row["mean_abs_delta_spectral_radius_rel"]) for row in group),
            }
        )
    out.sort(key=lambda row: (-int(row["n_profiles"]), str(row["family_label"])))
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    family_summary: Sequence[Mapping[str, Any]],
    pairwise: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    largest_family = max((int(row["n_profiles"]) for row in family_summary), default=0)
    repeated_non_mixed = [
        row
        for row in family_summary
        if int(row["n_profiles"]) >= 2 and str(row["family_label"]) != "mixed_family"
    ]
    full_near = [row for row in pairwise if str(row["symmetry_label"]) == "support_and_carrier_near_symmetry"]
    support_only = [row for row in pairwise if str(row["symmetry_label"]) == "support_only_near_symmetry"]

    if largest_family >= 6 and repeated_non_mixed:
        status = "scale_jump_family_plateau_supported"
        note = (
            f"Target 192 viser en dominerende familie med {largest_family} av 8 profiler; "
            f"{len(full_near)} full near-symmetry-kandidater."
        )
        next_step = "holdout_target192_family_plateau"
        next_note = "Neste steg bor validere target-192 plateauet pa friske seeds for a se om skalahoppet faktisk stabiliserte familiestrukturen."
    elif repeated_non_mixed and full_near:
        status = "scale_jump_family_plus_symmetry_candidate"
        note = (
            f"Target 192 har {len(repeated_non_mixed)} repeterte ikke-mixed family-labels og {len(full_near)} full near-symmetry-kandidater."
        )
        next_step = "holdout_target192_candidates"
        next_note = "Neste steg bor holde ut de konkrete target-192 kandidatene, ikke utvide placement-soket."
    elif repeated_non_mixed:
        status = "scale_jump_weak_family_signal"
        note = f"Target 192 har repeterte family-labels, men ikke et klart dominant plateau og ingen full near-symmetry."
        next_step = "choose_between_holdout_and_larger_scale"
        next_note = "Neste steg bor enten holde ut de beste kandidatene kort, eller hoppe videre til target 384 hvis signalet er for svakt."
    elif full_near or support_only:
        status = "scale_jump_symmetry_without_family"
        note = (
            f"Family-labels repeterer ikke tydelig, men det finnes {len(full_near)} full og {len(support_only)} support-only near-symmetry-kandidater."
        )
        next_step = "inspect_symmetry_candidates_or_jump_again"
        next_note = "Neste steg bor bare holde ut symmetrikandidatene hvis de er substantive; ellers hopp videre i skala."
    else:
        status = "scale_jump_no_family_signal"
        note = "Target 192 gir verken repeterte family-labels eller near-symmetry-kandidater som rettferdiggjor lokal raffinering."
        next_step = "larger_scale_jump"
        next_note = "Neste steg bor vaere target 384 eller en annen observabel, ikke mer av samme target-192 kart."

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
            "diagnostic_family": "scale_jump_family_probe",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "symmetry_scope",
            "status": "feature_level_only",
            "note": "Near-symmetry betyr bare lav normalisert support/carrier-avstand, ikke automorfi eller fysisk symmetri.",
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
    family_summary: Sequence[Mapping[str, Any]],
    pairwise: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bx: scale-jump family probe")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tar skalahoppet som `v15bw` gjorde metodisk riktig: samme observabler, men target `192` i stedet for mer target-96-terskelfiksing.")
    lines.append("Family-labels brukes som sonder og kontroller, ikke som etablert familiestruktur.")
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
    lines.append("## Target-192 profiler")
    lines.append("")
    lines.append("| profile | family | coarse | core | shell | rare | spectral rel | dim rel | support b2 | shell2/shell1 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {row['family_label']} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_core_share'])} | {fmt(row['mean_shell_share'])} | {fmt(row['mean_rare_share'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} | {fmt(row['mean_abs_delta_dim_proxy_rel'])} | {fmt(row['support_ball_2'])} | {fmt(row['shell2_over_shell1'])} |"
        )
    lines.append("")
    lines.append("## Family summary")
    lines.append("")
    lines.append("| family | n | profiles | mean coarse | mean core | mean rare | mean spectral rel |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in family_summary:
        lines.append(
            f"| {row['family_label']} | {int(row['n_profiles'])} | {row['profiles']} | {fmt(row['mean_coarse_return'])} | {fmt(row['mean_core_share'])} | {fmt(row['mean_rare_share'])} | {fmt(row['mean_spectral_rel'])} |"
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
    lines.append("- Dette er et smalt skalahopp etter en negativ holdout, ikke en bred ny scan.")
    lines.append("- Positivt signal her betyr bare at target 192 kan ha et mer stabilt feature-plateau enn target 96.")
    lines.append("- Symmetrikandidater ma holdes pa friske seeds for de kan brukes som mer enn navigasjon.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bx scale-jump family probe.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15bx_scale_jump_family_probe_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15bx_scale_jump_family_probe_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15bx_scale_jump_family_probe_aggregate.csv")
    p.add_argument("--out-family-csv", type=str, default="Documentation/v15bx_scale_jump_family_probe_family_summary.csv")
    p.add_argument("--out-pairwise-csv", type=str, default="Documentation/v15bx_scale_jump_family_probe_pairwise.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bx_scale_jump_family_probe_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bx_scale_jump_family_probe_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bx_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bx.md")
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
        aggregate_profile(
            [row for row in run_rows if str(row["perturbation"]) == perturbation and int(row["placement"]) == int(placement)],
            perturbation=perturbation,
            placement=placement,
        )
        for perturbation in PERTURBATIONS
        for placement in PLACEMENTS
    ]
    aggregate.sort(key=lambda row: (str(row["perturbation"]), int(row["placement"])))
    family_summary = family_summary_rows(aggregate)
    pairwise = v15bv.pairwise_rows(aggregate)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        family_summary=family_summary,
        pairwise=pairwise,
    )
    report_md = build_report(
        target_summary=target_summary,
        aggregate=aggregate,
        family_summary=family_summary,
        pairwise=pairwise,
        diagnosis=diagnosis,
    )
    op_md = "\n".join(
        [
            "# v0.15bx operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les dette som et smalt skalahopp etter v15bw, ikke som en bred ny family-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bx",
            "",
            "Da familiekartet pa storrelse 96 ikke gjentok seg rent, hoppet denne runden til storrelse 192 med samme maleapparat.",
            "",
            "Sporsmalet er enkelt: blir de lokale forstyrrelsene mer ordnet pa en storre graf, eller var familiestrukturen ved 96 mest lokal stoy?",
        ]
    ) + "\n"

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_family_csv, family_summary)
    write_csv(args.out_pairwise_csv, pairwise)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
