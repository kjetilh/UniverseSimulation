#!/usr/bin/env python3
"""v0.15cf target-768 support-locus mechanism lab.

After v15cd/v15ce, the broad target-768 family map is still too unstable for a
full mechanism story. The stable remainder is narrower:

- add_chord_p0 held as the spectral outlier
- add_chord_p2 / local_swap_p2 held as the strongest cross-carrier near-symmetry

This round asks a smaller question:

is target-768 better read as an asymmetric support-locus split between
placement 0 and placement 2 than as a broad carrier family map?

The hypothesis is intentionally narrow:

- placement 2 may be a carrier-robust rare/diffuse locus
- placement 0 may be a more carrier-sensitive support locus
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
import relational_universe_v15aw_local_swap_core_shell_lab as v15aw
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15bu_same_locus_carrier_occupancy_spectrum_lab as v15bu
import relational_universe_v15ca_target192_radial_occupancy_mechanism_lab as v15ca
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 768
GROWTH_SEED = 202
PLACEMENTS = (0, 2)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (3209, 3251, 3299, 3343)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY


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
    perturbation_offset = {"add_chord": 1009, "local_swap": 1063}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def aggregate_profile(rows: Sequence[Mapping[str, Any]], *, perturbation: str, placement: int) -> Dict[str, Any]:
    return {
        "profile_label": f"{perturbation}_p{int(placement)}",
        "perturbation": perturbation,
        "placement": int(placement),
        "target_nodes": TARGET,
        "growth_seed": GROWTH_SEED,
        "n_runs": len(rows),
        "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in rows),
        "mean_core_share": mean_defined(safe_float(row["core_share_of_union"]) for row in rows),
        "mean_shell_share": mean_defined(safe_float(row["shell_share_of_union"]) for row in rows),
        "mean_rare_share": mean_defined(safe_float(row["rare_share_of_union"]) for row in rows),
        "mean_core_cover": mean_defined(safe_float(row["mean_core_cover"]) for row in rows),
        "mean_support_core_frac": mean_defined(safe_float(row["support_core_frac"]) for row in rows),
        "mean_tail_union_nodes": mean_defined(safe_float(row["tail_union_nodes"]) for row in rows),
        "mean_occupancy_entropy": mean_defined(safe_float(row["occupancy_entropy"]) for row in rows),
        "mean_top1_mass_share": mean_defined(safe_float(row["top1_mass_share"]) for row in rows),
        "mean_top3_mass_share": mean_defined(safe_float(row["top3_mass_share"]) for row in rows),
        "mean_top5_mass_share": mean_defined(safe_float(row["top5_mass_share"]) for row in rows),
        "mean_occ_sd": mean_defined(safe_float(row["occ_sd"]) for row in rows),
        "mean_weighted_mean_distance": mean_defined(safe_float(row["weighted_mean_distance"]) for row in rows),
        "mean_weighted_distance_sd": mean_defined(safe_float(row["weighted_distance_sd"]) for row in rows),
        "mean_shell4plus_mass_share": mean_defined(safe_float(row["shell4plus_mass_share"]) for row in rows),
        "mean_shell_entropy": mean_defined(safe_float(row["shell_entropy"]) for row in rows),
        "mean_rare_mass_share": mean_defined(safe_float(row["rare_mass_share"]) for row in rows),
        "mean_abs_delta_spectral_radius_rel": mean_defined(safe_float(row["abs_delta_spectral_radius_rel"]) for row in rows),
        "mean_abs_delta_dim_proxy_rel": mean_defined(safe_float(row["abs_delta_dim_proxy_rel"]) for row in rows),
    }


def locus_summary_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        group = [row for row in aggregate if int(row["placement"]) == int(placement)]
        out.append(
            {
                "placement": int(placement),
                "n_profiles": len(group),
                "profiles": ";".join(str(row["profile_label"]) for row in group),
                "mean_full_coarse_return_rate": mean_defined(safe_float(row["mean_full_coarse_return_rate"]) for row in group),
                "mean_core_share": mean_defined(safe_float(row["mean_core_share"]) for row in group),
                "mean_rare_share": mean_defined(safe_float(row["mean_rare_share"]) for row in group),
                "mean_support_core_frac": mean_defined(safe_float(row["mean_support_core_frac"]) for row in group),
                "mean_occupancy_entropy": mean_defined(safe_float(row["mean_occupancy_entropy"]) for row in group),
                "mean_top3_mass_share": mean_defined(safe_float(row["mean_top3_mass_share"]) for row in group),
                "mean_weighted_mean_distance": mean_defined(safe_float(row["mean_weighted_mean_distance"]) for row in group),
                "mean_shell4plus_mass_share": mean_defined(safe_float(row["mean_shell4plus_mass_share"]) for row in group),
                "mean_rare_mass_share": mean_defined(safe_float(row["mean_rare_mass_share"]) for row in group),
                "mean_abs_delta_spectral_radius_rel": mean_defined(safe_float(row["mean_abs_delta_spectral_radius_rel"]) for row in group),
            }
        )
    out.sort(key=lambda row: int(row["placement"]))
    return out


def support_compare_row(a: Mapping[str, Any], b: Mapping[str, Any], *, compare_label: str) -> Dict[str, Any]:
    return {
        "compare_label": compare_label,
        "rare_share_gap_b_minus_a": safe_float(b["mean_rare_share"]) - safe_float(a["mean_rare_share"]),
        "support_core_gap_a_minus_b": safe_float(a["mean_support_core_frac"]) - safe_float(b["mean_support_core_frac"]),
        "weighted_distance_gap_b_minus_a": safe_float(b["mean_weighted_mean_distance"]) - safe_float(a["mean_weighted_mean_distance"]),
        "shell4plus_gap_b_minus_a": safe_float(b["mean_shell4plus_mass_share"]) - safe_float(a["mean_shell4plus_mass_share"]),
        "rare_mass_gap_b_minus_a": safe_float(b["mean_rare_mass_share"]) - safe_float(a["mean_rare_mass_share"]),
        "occupancy_entropy_gap_b_minus_a": safe_float(b["mean_occupancy_entropy"]) - safe_float(a["mean_occupancy_entropy"]),
        "top3_gap_a_minus_b": safe_float(a["mean_top3_mass_share"]) - safe_float(b["mean_top3_mass_share"]),
        "coarse_return_gap_a_minus_b": safe_float(a["mean_full_coarse_return_rate"]) - safe_float(b["mean_full_coarse_return_rate"]),
        "spectral_rel_gap_b_minus_a": safe_float(b["mean_abs_delta_spectral_radius_rel"]) - safe_float(a["mean_abs_delta_spectral_radius_rel"]),
    }


def carrier_gap_row(a: Mapping[str, Any], b: Mapping[str, Any], *, compare_label: str) -> Dict[str, Any]:
    return {
        "compare_label": compare_label,
        "abs_core_share_gap": abs(safe_float(a["mean_core_share"]) - safe_float(b["mean_core_share"])),
        "abs_rare_share_gap": abs(safe_float(a["mean_rare_share"]) - safe_float(b["mean_rare_share"])),
        "abs_support_core_gap": abs(safe_float(a["mean_support_core_frac"]) - safe_float(b["mean_support_core_frac"])),
        "abs_weighted_distance_gap": abs(safe_float(a["mean_weighted_mean_distance"]) - safe_float(b["mean_weighted_mean_distance"])),
        "abs_shell4plus_gap": abs(safe_float(a["mean_shell4plus_mass_share"]) - safe_float(b["mean_shell4plus_mass_share"])),
        "abs_rare_mass_gap": abs(safe_float(a["mean_rare_mass_share"]) - safe_float(b["mean_rare_mass_share"])),
        "abs_occupancy_entropy_gap": abs(safe_float(a["mean_occupancy_entropy"]) - safe_float(b["mean_occupancy_entropy"])),
        "abs_top3_gap": abs(safe_float(a["mean_top3_mass_share"]) - safe_float(b["mean_top3_mass_share"])),
        "abs_spectral_rel_gap": abs(safe_float(a["mean_abs_delta_spectral_radius_rel"]) - safe_float(b["mean_abs_delta_spectral_radius_rel"])),
    }


def comparison_rows(aggregate: Sequence[Mapping[str, Any]], locus_summary: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_profile = {str(row["profile_label"]): row for row in aggregate}
    by_locus = {int(row["placement"]): row for row in locus_summary}
    out = [
        support_compare_row(by_profile["add_chord_p0"], by_profile["add_chord_p2"], compare_label="add_chord_p2_minus_p0"),
        support_compare_row(by_profile["local_swap_p0"], by_profile["local_swap_p2"], compare_label="local_swap_p2_minus_p0"),
        support_compare_row(by_locus[0], by_locus[2], compare_label="pooled_p2_minus_p0"),
        carrier_gap_row(by_profile["add_chord_p0"], by_profile["local_swap_p0"], compare_label="carrier_gap_at_p0"),
        carrier_gap_row(by_profile["add_chord_p2"], by_profile["local_swap_p2"], compare_label="carrier_gap_at_p2"),
    ]
    return out


def support_split_score(row: Mapping[str, Any]) -> int:
    score = 0
    if safe_float(row["rare_share_gap_b_minus_a"]) >= 0.05:
        score += 1
    if safe_float(row["weighted_distance_gap_b_minus_a"]) >= 0.08:
        score += 1
    if safe_float(row["shell4plus_gap_b_minus_a"]) >= 0.03:
        score += 1
    if safe_float(row["rare_mass_gap_b_minus_a"]) >= 0.05:
        score += 1
    if safe_float(row["occupancy_entropy_gap_b_minus_a"]) >= 0.02:
        score += 1
    if safe_float(row["top3_gap_a_minus_b"]) >= 0.02:
        score += 1
    if safe_float(row["support_core_gap_a_minus_b"]) >= 0.05:
        score += 1
    return score


def carrier_gap_score(row: Mapping[str, Any]) -> float:
    keys = (
        "abs_core_share_gap",
        "abs_rare_share_gap",
        "abs_support_core_gap",
        "abs_weighted_distance_gap",
        "abs_shell4plus_gap",
        "abs_rare_mass_gap",
        "abs_occupancy_entropy_gap",
        "abs_top3_gap",
        "abs_spectral_rel_gap",
    )
    return mean_defined(safe_float(row[key]) for key in keys)


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    by_label = {str(row["compare_label"]): row for row in comparisons}
    add_split = support_split_score(by_label["add_chord_p2_minus_p0"])
    swap_split = support_split_score(by_label["local_swap_p2_minus_p0"])
    pooled_split = support_split_score(by_label["pooled_p2_minus_p0"])
    p0_gap = carrier_gap_score(by_label["carrier_gap_at_p0"])
    p2_gap = carrier_gap_score(by_label["carrier_gap_at_p2"])

    if add_split >= 5 and swap_split >= 5 and pooled_split >= 6 and p2_gap + 0.03 <= p0_gap:
        status = "support_locus_asymmetry_supported"
        note = (
            f"Begge carrierne leser p2 som mer rare/diffus enn p0 (scores {add_split}/7 og {swap_split}/7), "
            f"og carrier-gapet er mindre ved p2 enn ved p0 ({fmt(p2_gap)} < {fmt(p0_gap)})."
        )
        next_step = "probe_stable_p2_locus_mechanism"
        next_note = "Neste steg bor forklare hvorfor p2-locuset er carrier-robust, ikke utvide hele target-768-kartet."
    elif pooled_split >= 5 and p2_gap <= p0_gap:
        status = "support_locus_split_supported_carrier_gap_weak"
        note = (
            f"Pooled p0->p2-splittelsen er tydelig (score {pooled_split}/7), "
            f"men carrier-gap-asymmetrien er bare svak ({fmt(p2_gap)} vs {fmt(p0_gap)})."
        )
        next_step = "narrow_p2_holdout_or_second_mechanism"
        next_note = "Neste steg bor vaere en enda smalere p2-fokusert holdout eller en ny mekanismeobservabel."
    elif add_split >= 4 or swap_split >= 4 or pooled_split >= 4:
        status = "support_locus_split_weak"
        note = (
            f"Det finnes en svak p0/p2-locus-splittelse (scores add={add_split}, swap={swap_split}, pooled={pooled_split}), "
            f"men den er ikke ren nok ennå."
        )
        next_step = "stay_narrow_at_target768"
        next_note = "Neste steg bor fortsatt holde seg smalt ved target 768, ikke gjenapne bred family-label-tuning."
    else:
        status = "support_locus_split_not_yet"
        note = "Heller ikke denne smale p0/p2-observabelen skiller target-768-resten rent."
        next_step = "new_target768_observable"
        next_note = "Neste steg bor vaere en ny target-768-observabel, ikke mer av samme support-locus-lesning."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsen er ren og alle target-768 support-locus-runs matcher onsket perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "support_locus_mechanism",
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
    locus_summary: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cf: target-768 support-locus mechanism lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden ser bare pa den stabile resten etter `v15ce`: placement `0` og `2` ved target `768`.")
    lines.append("Sporsmalet er om target-768 ser bedre ut som en support-locus-splitt enn som en bred carrier family-map.")
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
    lines.append("## Profile summary")
    lines.append("")
    lines.append("| profile | coarse | core | rare | support core | occ entropy | top3 | mean dist | shell4+ | rare mass | spectral rel |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_core_share'])} | {fmt(row['mean_rare_share'])} | {fmt(row['mean_support_core_frac'])} | {fmt(row['mean_occupancy_entropy'])} | {fmt(row['mean_top3_mass_share'])} | {fmt(row['mean_weighted_mean_distance'])} | {fmt(row['mean_shell4plus_mass_share'])} | {fmt(row['mean_rare_mass_share'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} |"
        )
    lines.append("")
    lines.append("## Locus summary")
    lines.append("")
    lines.append("| placement | profiles | coarse | core | rare | support core | occ entropy | top3 | mean dist | shell4+ | rare mass | spectral rel |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in locus_summary:
        lines.append(
            f"| {int(row['placement'])} | {row['profiles']} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_core_share'])} | {fmt(row['mean_rare_share'])} | {fmt(row['mean_support_core_frac'])} | {fmt(row['mean_occupancy_entropy'])} | {fmt(row['mean_top3_mass_share'])} | {fmt(row['mean_weighted_mean_distance'])} | {fmt(row['mean_shell4plus_mass_share'])} | {fmt(row['mean_rare_mass_share'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} |"
        )
    lines.append("")
    lines.append("## Comparison summary")
    lines.append("")
    lines.append("| compare | rare gap | support-core gap | distance gap | shell4+ gap | rare-mass gap | entropy gap | top3 gap | coarse gap | spectral gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in comparisons[:3]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['rare_share_gap_b_minus_a'])} | {fmt(row['support_core_gap_a_minus_b'])} | {fmt(row['weighted_distance_gap_b_minus_a'])} | {fmt(row['shell4plus_gap_b_minus_a'])} | {fmt(row['rare_mass_gap_b_minus_a'])} | {fmt(row['occupancy_entropy_gap_b_minus_a'])} | {fmt(row['top3_gap_a_minus_b'])} | {fmt(row['coarse_return_gap_a_minus_b'])} | {fmt(row['spectral_rel_gap_b_minus_a'])} |"
        )
    lines.append("")
    lines.append("## Carrier gap")
    lines.append("")
    lines.append("| compare | core gap | rare gap | support-core gap | distance gap | shell4+ gap | rare-mass gap | entropy gap | top3 gap | spectral gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in comparisons[3:]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['abs_core_share_gap'])} | {fmt(row['abs_rare_share_gap'])} | {fmt(row['abs_support_core_gap'])} | {fmt(row['abs_weighted_distance_gap'])} | {fmt(row['abs_shell4plus_gap'])} | {fmt(row['abs_rare_mass_gap'])} | {fmt(row['abs_occupancy_entropy_gap'])} | {fmt(row['abs_top3_gap'])} | {fmt(row['abs_spectral_rel_gap'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en smal target-768-runde rundt den stabile resten, ikke et nytt family-sok.")
    lines.append("- Positivt signal her betyr at p0/p2-splittelsen leses bedre som locus-mekanisme enn som full carrier-fysikk.")
    lines.append("- Near-symmetry skal fortsatt leses som feature-level naerhet, ikke sterkere.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cf target-768 support-locus mechanism lab.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cf_target768_support_locus_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cf_target768_support_locus_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cf_target768_support_locus_aggregate.csv")
    p.add_argument("--out-locus-csv", type=str, default="Documentation/v15cf_target768_support_locus_locus_summary.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15cf_target768_support_locus_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cf_target768_support_locus_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cf_target768_support_locus_mechanism_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cf_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cf.md")
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
                radial = v15ca.radial_occupancy_metrics(base_state, support, res["damaged_sets"])
                spectrum = v15bu.occupancy_spectrum_metrics(res["damaged_sets"])
                support_features = v14c.support_geometry_features(base_state, support)
                drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                run_rows.append(
                    {
                        "profile_label": f"{perturbation}_p{int(placement)}",
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
                        "support_core_frac": safe_float(core_shell["support_core_frac"]),
                        **radial,
                        **spectrum,
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
    locus_summary = locus_summary_rows(aggregate)
    comparisons = comparison_rows(aggregate, locus_summary)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        comparisons=comparisons,
    )
    report_md = build_report(
        target_summary=target_summary,
        aggregate=aggregate,
        locus_summary=locus_summary,
        comparisons=comparisons,
        diagnosis=diagnosis,
    )
    op_md = "\n".join(
        [
            "# v0.15cf operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les dette som en smal target-768-locus-runde, ikke som ny bred family-label-tuning.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15cf",
            "",
            "Denne runden ser bare pa to lokale startsteder ved storrelse 768 for a sjekke om det er selve stedet i grafen som betyr mest, mer enn hvilken perturbasjon som brukes.",
            "",
            "Hvis det stemmer, skal placement 2 se lik ut pa tvers av carrier, mens placement 0 er mer blandet og sensitiv.",
        ]
    ) + "\n"

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_locus_csv, locus_summary)
    write_csv(args.out_compare_csv, comparisons)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
