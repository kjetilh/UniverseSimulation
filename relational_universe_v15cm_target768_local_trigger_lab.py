#!/usr/bin/env python3
"""v0.15cm target-768 local trigger lab.

v15cl rejected the first shell2/3 gate / global-budget coupling observable,
but the p2 far-shell horizon itself remained alive on the same target-768
pocket. This round asks a more local question:

does p2 differ from p0 already in the early launch dynamics near support?

The observables are deliberately early and local:

- first hit step for shell1/shell2/shell3/outer
- early radius growth
- early near-support and shell3 load
- static support geometry
- downstream far-shell-horizon label for alignment only
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15cg_target768_far_shell_horizon_lab as v15cg
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 768
GROWTH_SEED = 202
PLACEMENTS = (0, 2)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (4703, 4751, 4801, 4861)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
EARLY_STEP_LIMIT = 640
OUTER_DISTANCE_FLOOR = 4


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
    perturbation_offset = {"add_chord": 1811, "local_swap": 1877}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def shell_counts(damaged: Set[int], base_dist: Mapping[int, int], fallback: int) -> Dict[str, int]:
    counts = {"shell0": 0, "shell1": 0, "shell2": 0, "shell3": 0, "outer": 0}
    for node in damaged:
        dist = int(base_dist.get(node, fallback))
        if dist <= 0:
            counts["shell0"] += 1
        elif dist == 1:
            counts["shell1"] += 1
        elif dist == 2:
            counts["shell2"] += 1
        elif dist == 3:
            counts["shell3"] += 1
        else:
            counts["outer"] += 1
    return counts


def mean_distance(damaged: Set[int], base_dist: Mapping[int, int], fallback: int) -> float:
    if not damaged:
        return 0.0
    return sum(int(base_dist.get(node, fallback)) for node in damaged) / max(1, len(damaged))


def snapshot_rows_for_run(
    *,
    perturbation: str,
    placement: int,
    seed_delta: int,
    run_seed: int,
    support_signature: str,
    log_rows: Sequence[Mapping[str, Any]],
    damaged_sets: Sequence[Set[int]],
    base_dist: Mapping[int, int],
    fallback: int,
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for idx, row in enumerate(log_rows):
        damaged = set(damaged_sets[idx])
        counts = shell_counts(damaged, base_dist, fallback)
        total = max(1, len(damaged))
        outer = counts["outer"]
        weighted_distance = mean_distance(damaged, base_dist, fallback)
        if outer / total >= v15cg.HIGH_SHARE_THRESHOLD and weighted_distance >= v15cg.HIGH_DISTANCE_THRESHOLD:
            horizon_band = "high"
        elif outer / total >= v15cg.MID_SHARE_THRESHOLD and weighted_distance >= v15cg.MID_DISTANCE_THRESHOLD:
            horizon_band = "mid"
        else:
            horizon_band = "low"
        out.append(
            {
                "profile_label": f"{perturbation}_p{int(placement)}",
                "perturbation": perturbation,
                "placement": int(placement),
                "seed_delta": int(seed_delta),
                "run_seed": int(run_seed),
                "support_signature": support_signature,
                "snapshot_index": int(idx),
                "step": int(row["step"]),
                "damaged_nodes": int(len(damaged)),
                "shell0_nodes": int(counts["shell0"]),
                "shell1_nodes": int(counts["shell1"]),
                "shell2_nodes": int(counts["shell2"]),
                "shell3_nodes": int(counts["shell3"]),
                "outer_nodes": int(outer),
                "near_support_nodes": int(counts["shell0"] + counts["shell1"]),
                "shell3_share": counts["shell3"] / total,
                "outer_share": outer / total,
                "near_support_share": (counts["shell0"] + counts["shell1"]) / total,
                "radius_control": int(row["radius_control"]),
                "boundary_to_volume": safe_float(row["boundary_to_volume"]),
                "component_count": int(row["damage_component_count"]),
                "largest_component_fraction": safe_float(row["largest_component_fraction"]),
                "weighted_mean_distance": weighted_distance,
                "horizon_band": horizon_band,
            }
        )
    return out


def first_step_where(rows: Sequence[Mapping[str, Any]], predicate: Any) -> float:
    for row in rows:
        if predicate(row):
            return safe_float(row["step"])
    return float("nan")


def horizon_summary(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(rows))))
    tail_rows = list(rows[tail_start:])
    bands = [str(row["horizon_band"]) for row in tail_rows]
    high_start_raw = v15cg.first_run_ge(bands, "high", 3)
    window = len(bands)
    high_start = window if high_start_raw is None else int(high_start_raw)
    if high_start_raw is None:
        last_high = -1
        high_horizon = 0
        retention = 0.0
    else:
        high_positions = [idx for idx, band in enumerate(bands) if band == "high" and idx >= high_start_raw]
        last_high = max(high_positions)
        horizon_slice = bands[high_start_raw:last_high + 1]
        high_horizon = len(horizon_slice)
        retention = sum(1 for band in horizon_slice if band == "high") / max(1, len(horizon_slice))
    last12 = bands[-12:]
    last12_high_rate = sum(1 for band in last12 if band == "high") / max(1, len(last12)) if last12 else 0.0
    total_high_count = sum(1 for band in bands if band == "high")
    label = v15cg.classify_far_shell_horizon(
        high_start_index=high_start,
        last_high_index=last_high,
        high_horizon_span=high_horizon,
        high_retention_rate=retention,
        last12_high_rate=last12_high_rate,
        total_high_count=total_high_count,
        window=window,
    )
    return {
        "far_shell_horizon_label": label,
        "high_retention_rate": retention,
        "last12_high_rate": last12_high_rate,
        "tail_total_high_count": total_high_count,
    }


def early_radius_slope(rows: Sequence[Mapping[str, Any]]) -> float:
    early = [row for row in rows if safe_float(row["step"]) <= EARLY_STEP_LIMIT and int(row["radius_control"]) >= 0]
    if len(early) < 2:
        return float("nan")
    x0 = safe_float(early[0]["step"])
    y0 = safe_float(early[0]["radius_control"])
    x1 = safe_float(early[-1]["step"])
    y1 = safe_float(early[-1]["radius_control"])
    if x1 <= x0:
        return float("nan")
    return (y1 - y0) / (x1 - x0)


def run_summary(
    *,
    perturbation: str,
    placement: int,
    seed_delta: int,
    run_seed: int,
    requested_match: int,
    support_signature: str,
    support_geom: Mapping[str, Any],
    recurrence: Mapping[str, Any],
    final_drift: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    early = [row for row in rows if safe_float(row["step"]) <= EARLY_STEP_LIMIT]
    if not early:
        early = list(rows[:1])
    horizon = horizon_summary(rows)
    first_outer = first_step_where(rows, lambda row: int(row["outer_nodes"]) > 0)
    first_shell3 = first_step_where(rows, lambda row: int(row["shell3_nodes"]) > 0)
    first_shell2 = first_step_where(rows, lambda row: int(row["shell2_nodes"]) > 0)
    first_shell1 = first_step_where(rows, lambda row: int(row["shell1_nodes"]) > 0)
    early_peak_damage = max((int(row["damaged_nodes"]) for row in early), default=0)
    early_peak_near = max((int(row["near_support_nodes"]) for row in early), default=0)
    early_peak_shell3_share = max((safe_float(row["shell3_share"]) for row in early), default=float("nan"))
    early_peak_outer_share = max((safe_float(row["outer_share"]) for row in early), default=float("nan"))
    first_outer_is_early = int(math.isfinite(first_outer) and first_outer <= EARLY_STEP_LIMIT)

    if first_outer_is_early and early_peak_near >= 8 and early_peak_shell3_share >= 0.10:
        trigger_label = "loaded_fast_outer_launch"
    elif first_outer_is_early:
        trigger_label = "fast_outer_launch"
    elif math.isfinite(first_shell3) and first_shell3 <= EARLY_STEP_LIMIT:
        trigger_label = "shell3_probe_without_outer_launch"
    elif early_peak_near >= 8:
        trigger_label = "near_support_load_without_launch"
    else:
        trigger_label = "quiet_or_delayed_trigger"

    return {
        "profile_label": f"{perturbation}_p{int(placement)}",
        "perturbation": perturbation,
        "placement": int(placement),
        "seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "requested_match": int(requested_match),
        "support_signature": support_signature,
        "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
        "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
        "first_shell1_step": first_shell1,
        "first_shell2_step": first_shell2,
        "first_shell3_step": first_shell3,
        "first_outer_step": first_outer,
        "first_outer_is_early": first_outer_is_early,
        "early_radius_slope": early_radius_slope(rows),
        "early_peak_damage_nodes": int(early_peak_damage),
        "early_peak_near_support_nodes": int(early_peak_near),
        "early_peak_shell3_share": early_peak_shell3_share,
        "early_peak_outer_share": early_peak_outer_share,
        "mean_early_boundary_to_volume": mean_defined(safe_float(row["boundary_to_volume"]) for row in early),
        "mean_early_component_count": mean_defined(safe_float(row["component_count"]) for row in early),
        "trigger_label": trigger_label,
        "support_size": safe_float(support_geom["support_size"]),
        "mean_support_degree": safe_float(support_geom["mean_support_degree"]),
        "support_ball_1": safe_float(support_geom["support_ball_1"]),
        "support_ball_2": safe_float(support_geom["support_ball_2"]),
        "support_ball_3": safe_float(support_geom["support_ball_3"]),
        "shell2_over_shell1": safe_float(support_geom["shell2_over_shell1"]),
        "ball3_over_ball1": safe_float(support_geom["ball3_over_ball1"]),
        **horizon,
        "final_abs_delta_spectral_radius_rel": safe_float(final_drift["abs_delta_spectral_radius_rel"]),
        "final_abs_delta_beta1_rel": safe_float(final_drift["abs_delta_beta1_rel"]),
        "final_abs_delta_dim_proxy_rel": safe_float(final_drift["abs_delta_dim_proxy_rel"]),
    }


def finite_mean(values: Iterable[float]) -> float:
    return mean_defined(value for value in values if math.isfinite(value))


def aggregate_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        for placement in PLACEMENTS:
            group = [
                row for row in run_rows
                if str(row["perturbation"]) == perturbation and int(row["placement"]) == int(placement)
            ]
            out.append(
                {
                    "profile_label": f"{perturbation}_p{int(placement)}",
                    "perturbation": perturbation,
                    "placement": int(placement),
                    "n_runs": len(group),
                    "established_far_shell_rate": mean_defined(
                        1.0 if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon" else 0.0 for row in group
                    ),
                    "loaded_fast_outer_launch_rate": mean_defined(
                        1.0 if str(row["trigger_label"]) == "loaded_fast_outer_launch" else 0.0 for row in group
                    ),
                    "fast_outer_launch_rate": mean_defined(
                        1.0 if str(row["trigger_label"]) in {"loaded_fast_outer_launch", "fast_outer_launch"} else 0.0 for row in group
                    ),
                    "mean_first_outer_step": finite_mean(safe_float(row["first_outer_step"]) for row in group),
                    "mean_first_shell3_step": finite_mean(safe_float(row["first_shell3_step"]) for row in group),
                    "mean_early_radius_slope": finite_mean(safe_float(row["early_radius_slope"]) for row in group),
                    "mean_early_peak_damage_nodes": mean_defined(safe_float(row["early_peak_damage_nodes"]) for row in group),
                    "mean_early_peak_near_support_nodes": mean_defined(safe_float(row["early_peak_near_support_nodes"]) for row in group),
                    "mean_early_peak_shell3_share": mean_defined(safe_float(row["early_peak_shell3_share"]) for row in group),
                    "mean_early_peak_outer_share": mean_defined(safe_float(row["early_peak_outer_share"]) for row in group),
                    "mean_early_boundary_to_volume": mean_defined(safe_float(row["mean_early_boundary_to_volume"]) for row in group),
                    "mean_support_degree": mean_defined(safe_float(row["mean_support_degree"]) for row in group),
                    "support_ball_2": mean_defined(safe_float(row["support_ball_2"]) for row in group),
                    "support_ball_3": mean_defined(safe_float(row["support_ball_3"]) for row in group),
                    "shell2_over_shell1": mean_defined(safe_float(row["shell2_over_shell1"]) for row in group),
                    "ball3_over_ball1": mean_defined(safe_float(row["ball3_over_ball1"]) for row in group),
                    "mean_final_abs_delta_spectral_radius_rel": mean_defined(safe_float(row["final_abs_delta_spectral_radius_rel"]) for row in group),
                }
            )
    return out


def compare_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by = {str(row["profile_label"]): dict(row) for row in aggregate}
    keys = [
        "established_far_shell_rate",
        "loaded_fast_outer_launch_rate",
        "fast_outer_launch_rate",
        "mean_first_outer_step",
        "mean_first_shell3_step",
        "mean_early_radius_slope",
        "mean_early_peak_damage_nodes",
        "mean_early_peak_near_support_nodes",
        "mean_early_peak_shell3_share",
        "mean_early_boundary_to_volume",
        "mean_support_degree",
        "support_ball_2",
        "support_ball_3",
        "shell2_over_shell1",
        "ball3_over_ball1",
        "mean_final_abs_delta_spectral_radius_rel",
    ]
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        p0 = by[f"{perturbation}_p0"]
        p2 = by[f"{perturbation}_p2"]
        row: Dict[str, Any] = {"compare_label": f"{perturbation}_p2_minus_p0"}
        for key in keys:
            row[f"{key}_gap"] = safe_float(p2[key]) - safe_float(p0[key])
        out.append(row)
    add2 = by["add_chord_p2"]
    swap2 = by["local_swap_p2"]
    row = {"compare_label": "local_swap_p2_minus_add_chord_p2"}
    for key in keys:
        row[f"{key}_gap"] = safe_float(swap2[key]) - safe_float(add2[key])
    out.append(row)
    return out


def trigger_score(row: Mapping[str, Any]) -> int:
    score = 0
    if safe_float(row["established_far_shell_rate_gap"]) >= 0.25:
        score += 1
    if safe_float(row["fast_outer_launch_rate_gap"]) >= 0.25:
        score += 1
    if safe_float(row["mean_first_outer_step_gap"]) <= -128.0:
        score += 1
    if safe_float(row["mean_early_radius_slope_gap"]) >= 0.002:
        score += 1
    if safe_float(row["mean_early_peak_shell3_share_gap"]) >= 0.05:
        score += 1
    if safe_float(row["mean_early_peak_damage_nodes_gap"]) >= 8.0:
        score += 1
    return score


def geometry_score(row: Mapping[str, Any]) -> int:
    score = 0
    if safe_float(row["mean_support_degree_gap"]) >= 0.5:
        score += 1
    if safe_float(row["support_ball_2_gap"]) >= 2.0:
        score += 1
    if safe_float(row["support_ball_3_gap"]) >= 4.0:
        score += 1
    if safe_float(row["shell2_over_shell1_gap"]) >= 0.10:
        score += 1
    return score


def diagnosis_rows(
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    compares: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    by_compare = {str(row["compare_label"]): row for row in compares}
    add_trigger = trigger_score(by_compare["add_chord_p2_minus_p0"])
    swap_trigger = trigger_score(by_compare["local_swap_p2_minus_p0"])
    add_geom = geometry_score(by_compare["add_chord_p2_minus_p0"])
    swap_geom = geometry_score(by_compare["local_swap_p2_minus_p0"])

    if add_trigger >= 4 and swap_trigger >= 4:
        trigger_status = "shared_p2_local_trigger_candidate"
        trigger_note = f"Begge carrierne viser tidlig p2-launch-fordel (scores add={add_trigger}/6, swap={swap_trigger}/6)."
        next_step = "holdout_local_trigger"
        next_note = "Neste steg bor holde ut triggerobservabelen paa friske seeds."
    elif add_trigger >= 3 or swap_trigger >= 3:
        trigger_status = "local_trigger_weak_or_carrier_split"
        trigger_note = f"Tidlig trigger peker delvis mot p2, men ikke rent (scores add={add_trigger}/6, swap={swap_trigger}/6)."
        next_step = "compare_trigger_vs_scale"
        next_note = "Neste steg bor enten skjerpe triggerobservabelen eller teste om p2-horisonten skalerer."
    else:
        trigger_status = "local_trigger_not_yet"
        trigger_note = f"Tidlig supportnaer trigger skiller ikke p2 rent fra p0 (scores add={add_trigger}/6, swap={swap_trigger}/6)."
        next_step = "p2_horizon_scale_holdout"
        next_note = "Neste steg bor teste om p2-horisonten er target-768-spesifikk eller holder paa ny skala."

    if add_geom >= 3 and swap_geom >= 3:
        geometry_status = "support_geometry_aligned"
        geometry_note = f"Static support geometry peker samme vei for p2 i begge carrierne (scores add={add_geom}/4, swap={swap_geom}/4)."
    elif add_geom >= 2 or swap_geom >= 2:
        geometry_status = "support_geometry_weak_or_carrier_split"
        geometry_note = f"Static support geometry er delvis, men ikke ren (scores add={add_geom}/4, swap={swap_geom}/4)."
    else:
        geometry_status = "support_geometry_not_explanatory"
        geometry_note = f"Static support geometry forklarer ikke p2-trigger rent (scores add={add_geom}/4, swap={swap_geom}/4)."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {"diagnostic_family": "shared_p2_local_trigger", "status": trigger_status, "note": trigger_note},
        {"diagnostic_family": "support_geometry_alignment", "status": geometry_status, "note": geometry_note},
        {"diagnostic_family": "next_step", "status": next_step, "note": next_note},
    ]


def build_report(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    compares: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cm: target-768 local trigger lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om p2-horisonten ved target 768 kan forklares av tidlig supportnaer launch-dynamikk.")
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
    lines.append("## Aggregate local trigger")
    lines.append("")
    lines.append("| profile | horizon | fast launch | first outer | first shell3 | early slope | early damage | shell3 peak | support degree | ball3/ball1 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {fmt(row['established_far_shell_rate'])} | {fmt(row['fast_outer_launch_rate'])} | {fmt(row['mean_first_outer_step'],1)} | {fmt(row['mean_first_shell3_step'],1)} | {fmt(row['mean_early_radius_slope'],4)} | {fmt(row['mean_early_peak_damage_nodes'],1)} | {fmt(row['mean_early_peak_shell3_share'])} | {fmt(row['mean_support_degree'])} | {fmt(row['ball3_over_ball1'])} |"
        )
    lines.append("")
    lines.append("## P2 versus P0")
    lines.append("")
    lines.append("| compare | horizon gap | fast launch gap | first outer gap | early slope gap | early damage gap | shell3 peak gap | support degree gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares[:2]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['established_far_shell_rate_gap'])} | {fmt(row['fast_outer_launch_rate_gap'])} | {fmt(row['mean_first_outer_step_gap'],1)} | {fmt(row['mean_early_radius_slope_gap'],4)} | {fmt(row['mean_early_peak_damage_nodes_gap'],1)} | {fmt(row['mean_early_peak_shell3_share_gap'])} | {fmt(row['mean_support_degree_gap'])} |"
        )
    lines.append("")
    lines.append("## Cross-carrier P2 contrast")
    lines.append("")
    lines.append("| compare | horizon gap | fast launch gap | first outer gap | early slope gap | early damage gap | shell3 peak gap | support degree gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares[2:]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['established_far_shell_rate_gap'])} | {fmt(row['fast_outer_launch_rate_gap'])} | {fmt(row['mean_first_outer_step_gap'],1)} | {fmt(row['mean_early_radius_slope_gap'],4)} | {fmt(row['mean_early_peak_damage_nodes_gap'],1)} | {fmt(row['mean_early_peak_shell3_share_gap'])} | {fmt(row['mean_support_degree_gap'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en lokal tidligfase-observabel, ikke en ny global invariant-test.")
    lines.append("- Positivt signal betyr bare at p2-horisonten kan ha en supportnaer launch-forklaring.")
    lines.append("- Negativt signal betyr at neste steg bor teste skala/holdout heller enn enda mer trigger-tuning.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15cm", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Les dette som en tidlig lokal trigger-test, ikke som bevis for partikler eller universell geometri.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15cm",
        "",
        "Denne runden tester om p2-halen ved target 768 starter som en spesiell tidlig lokal launch naer perturbasjonen.",
        "",
        f"- Lokal trigger: `{diag['shared_p2_local_trigger']['status']}`.",
        f"- Supportgeometri: `{diag['support_geometry_alignment']['status']}`.",
        "",
        "Dette er fortsatt bare en mekanismetest. Det viser ikke partikler, romtid eller en global bevaringslov.",
        "",
        f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cm target-768 local trigger lab.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cm_target768_local_trigger_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cm_target768_local_trigger_runs.csv")
    p.add_argument("--out-snapshot-csv", type=str, default="Documentation/v15cm_target768_local_trigger_snapshot_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cm_target768_local_trigger_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15cm_target768_local_trigger_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cm_target768_local_trigger_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cm_target768_local_trigger_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cm_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cm.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    base_row = next(
        row for row in base_rows
        if int(row["target_nodes"]) == TARGET and int(row["growth_seed"]) == GROWTH_SEED
    )
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    run_rows: List[Dict[str, Any]] = []
    snapshot_rows: List[Dict[str, Any]] = []

    for perturbation in PERTURBATIONS:
        for placement in PLACEMENTS:
            for seed_delta in SEED_DELTAS:
                run_seed = run_seed_for(perturbation=perturbation, placement=placement, seed_delta=seed_delta)
                res = v15ae.run_defect_with_control_graphs(
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
                final_drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                info = dict(res["perturbation_info"])
                support = [int(x) for x in info.get("support", [])]
                support_signature = ",".join(str(x) for x in support)
                support_geom = v14c.support_geometry_features(base_state, support)
                base_dist = v7.bfs_distances(base_state.g, support)
                fallback = (max(base_dist.values()) + 1) if base_dist else 1
                rows = snapshot_rows_for_run(
                    perturbation=perturbation,
                    placement=placement,
                    seed_delta=seed_delta,
                    run_seed=run_seed,
                    support_signature=support_signature,
                    log_rows=res["log_rows"],
                    damaged_sets=res["damaged_sets"],
                    base_dist=base_dist,
                    fallback=fallback,
                )
                snapshot_rows.extend(rows)
                run_rows.append(
                    run_summary(
                        perturbation=perturbation,
                        placement=placement,
                        seed_delta=seed_delta,
                        run_seed=run_seed,
                        requested_match=int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
                        support_signature=support_signature,
                        support_geom=support_geom,
                        recurrence=recurrence,
                        final_drift=final_drift,
                        rows=rows,
                    )
                )

    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    aggregate = aggregate_rows(run_rows)
    compares = compare_rows(aggregate)
    diagnosis = diagnosis_rows(target_summary, run_rows, compares)

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_snapshot_csv, snapshot_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_compare_csv, compares)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            target_summary=target_summary,
            aggregate=aggregate,
            compares=compares,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
