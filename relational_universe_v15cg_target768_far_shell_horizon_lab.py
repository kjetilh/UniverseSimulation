#!/usr/bin/env python3
"""v0.15cg target-768 far-shell horizon lab.

v15cf showed that a coarse p0/p2 support-locus story is too blunt. The clean
parts of the signal were narrower:

- p2 sits farther out than p0 in both carriers
- p2 also carries somewhat more shell4+ mass than p0

This round asks the smaller follow-up:

is target-768 better read through a carrier-robust far-shell horizon at p2?

Instead of tail averages alone, it measures whether shell4+-heavy, long-range
damage actually persists over time in the tail.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 768
GROWTH_SEED = 202
PLACEMENTS = (0, 2)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (3407, 3451, 3499, 3547)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
HIGH_SHARE_THRESHOLD = 0.68
HIGH_DISTANCE_THRESHOLD = 6.0
MID_SHARE_THRESHOLD = 0.62
MID_DISTANCE_THRESHOLD = 5.0


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
    perturbation_offset = {"add_chord": 1109, "local_swap": 1163}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def first_run_ge(values: Sequence[str], target: str, length: int) -> int | None:
    current = 0
    for idx, value in enumerate(values):
        current = current + 1 if value == target else 0
        if current >= length:
            return idx - length + 1
    return None


def longest_run(values: Sequence[str], target: str) -> int:
    best = 0
    current = 0
    for value in values:
        if value == target:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def far_shell_snapshot_series(base_state: v7.State, support: Sequence[int], damaged_sets: Sequence[Set[int]]) -> List[Dict[str, Any]]:
    dist = v7.bfs_distances(base_state.g, support)
    fallback = (max(dist.values()) + 1) if dist else 1
    out: List[Dict[str, Any]] = []
    for damaged in damaged_sets:
        damaged_list = [node for node in damaged]
        total = max(1, len(damaged_list))
        dists = [int(dist.get(node, fallback)) for node in damaged_list]
        far_count = sum(1 for d in dists if d >= 4)
        far_share = far_count / total
        mean_distance = sum(dists) / total if dists else 0.0
        if far_share >= HIGH_SHARE_THRESHOLD and mean_distance >= HIGH_DISTANCE_THRESHOLD:
            band = "high"
        elif far_share >= MID_SHARE_THRESHOLD and mean_distance >= MID_DISTANCE_THRESHOLD:
            band = "mid"
        else:
            band = "low"
        out.append(
            {
                "far_shell_share": far_share,
                "weighted_mean_distance": mean_distance,
                "far_shell_band": band,
            }
        )
    return out


def classify_far_shell_horizon(
    *,
    high_start_index: int,
    last_high_index: int,
    high_horizon_span: int,
    high_retention_rate: float,
    last12_high_rate: float,
    total_high_count: int,
    window: int,
) -> str:
    if high_start_index >= window or total_high_count == 0:
        return "no_far_shell_horizon"
    if last12_high_rate >= 0.50 and high_horizon_span >= max(8, window // 4) and high_retention_rate >= 0.60:
        return "established_far_shell_horizon"
    if high_start_index >= max(0, window - 16) and total_high_count <= 6:
        return "late_far_shell_probe"
    if high_start_index <= max(4, window // 6) and last12_high_rate == 0.0 and high_horizon_span >= 8:
        return "failed_far_shell_horizon"
    return "mixed_far_shell_horizon"


def horizon_note(label: str) -> str:
    if label == "established_far_shell_horizon":
        return "Far-shell-massen bygger en reell halehorisont som holder ut i tail-slutten."
    if label == "late_far_shell_probe":
        return "Far-shell dukker opp sent, men rekker bare en kort probe-horisont."
    if label == "failed_far_shell_horizon":
        return "Far-shell dukker opp, men mister hold lenge før tail-slutten."
    if label == "no_far_shell_horizon":
        return "Runet bygger ingen faktisk far-shell-horisont."
    return "Far-shell-horisonten er fortsatt blandet i denne observabelen."


def analyze_run(
    *,
    base_state: v7.State,
    base_row: Mapping[str, Any],
    perturbation: str,
    placement: int,
    seed_delta: int,
) -> Dict[str, Any]:
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
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
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(res["log_rows"]))))
    tail_log = res["log_rows"][tail_start:]
    tail_damaged = res["damaged_sets"][tail_start:]
    tail_series = far_shell_snapshot_series(base_state, support, tail_damaged)
    bands = [str(row["far_shell_band"]) for row in tail_series]
    high_start_raw = first_run_ge(bands, "high", 3)
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
    total_mid_count = sum(1 for band in bands if band == "mid")
    mean_far_share = mean_defined(safe_float(row["far_shell_share"]) for row in tail_series)
    mean_weighted_distance = mean_defined(safe_float(row["weighted_mean_distance"]) for row in tail_series)
    q90_far_share = v15.quantile([safe_float(row["far_shell_share"]) for row in tail_series], 0.90) if tail_series else float("nan")
    label = classify_far_shell_horizon(
        high_start_index=high_start,
        last_high_index=last_high,
        high_horizon_span=high_horizon,
        high_retention_rate=retention,
        last12_high_rate=last12_high_rate,
        total_high_count=total_high_count,
        window=window,
    )
    drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
    return {
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
        "tail_snapshot_count": int(window),
        "high_start_index": int(high_start),
        "last_high_index": int(last_high),
        "high_horizon_span": int(high_horizon),
        "high_retention_rate": float(retention),
        "last12_high_rate": float(last12_high_rate),
        "total_high_count": int(total_high_count),
        "total_mid_count": int(total_mid_count),
        "longest_high_run": int(longest_run(bands, "high")),
        "mean_far_shell_share": mean_far_share,
        "q90_far_shell_share": q90_far_share,
        "mean_weighted_mean_distance": mean_weighted_distance,
        "far_shell_horizon_label": label,
        "far_shell_horizon_note": horizon_note(label),
        **drift,
    }


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        for placement in PLACEMENTS:
            group = [row for row in rows if str(row["perturbation"]) == perturbation and int(row["placement"]) == int(placement)]
            out.append(
                {
                    "profile_label": f"{perturbation}_p{int(placement)}",
                    "perturbation": perturbation,
                    "placement": int(placement),
                    "n_runs": len(group),
                    "established_far_shell_rate": mean_defined(
                        1.0 if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon" else 0.0 for row in group
                    ),
                    "late_probe_rate": mean_defined(
                        1.0 if str(row["far_shell_horizon_label"]) == "late_far_shell_probe" else 0.0 for row in group
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
                    "mean_abs_delta_spectral_radius_rel": mean_defined(safe_float(row["abs_delta_spectral_radius_rel"]) for row in group),
                }
            )
    out.sort(key=lambda row: (str(row["perturbation"]), int(row["placement"])))
    return out


def compare_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_profile = {str(row["profile_label"]): row for row in aggregate}
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        p0 = by_profile[f"{perturbation}_p0"]
        p2 = by_profile[f"{perturbation}_p2"]
        out.append(
            {
                "compare_label": f"{perturbation}_p2_minus_p0",
                "perturbation": perturbation,
                "established_rate_gap": safe_float(p2["established_far_shell_rate"]) - safe_float(p0["established_far_shell_rate"]),
                "high_retention_gap": safe_float(p2["mean_high_retention_rate"]) - safe_float(p0["mean_high_retention_rate"]),
                "last12_high_gap": safe_float(p2["mean_last12_high_rate"]) - safe_float(p0["mean_last12_high_rate"]),
                "high_horizon_gap": safe_float(p2["mean_high_horizon_span"]) - safe_float(p0["mean_high_horizon_span"]),
                "total_high_gap": safe_float(p2["mean_total_high_count"]) - safe_float(p0["mean_total_high_count"]),
                "far_share_gap": safe_float(p2["mean_far_shell_share"]) - safe_float(p0["mean_far_shell_share"]),
                "q90_far_share_gap": safe_float(p2["mean_q90_far_shell_share"]) - safe_float(p0["mean_q90_far_shell_share"]),
                "distance_gap": safe_float(p2["mean_weighted_mean_distance"]) - safe_float(p0["mean_weighted_mean_distance"]),
                "spectral_gap": safe_float(p2["mean_abs_delta_spectral_radius_rel"]) - safe_float(p0["mean_abs_delta_spectral_radius_rel"]),
            }
        )
    add0 = by_profile["add_chord_p0"]
    swap0 = by_profile["local_swap_p0"]
    add2 = by_profile["add_chord_p2"]
    swap2 = by_profile["local_swap_p2"]
    out.extend(
        [
            {
                "compare_label": "carrier_gap_at_p0",
                "perturbation": "mixed",
                "abs_established_rate_gap": abs(safe_float(add0["established_far_shell_rate"]) - safe_float(swap0["established_far_shell_rate"])),
                "abs_high_retention_gap": abs(safe_float(add0["mean_high_retention_rate"]) - safe_float(swap0["mean_high_retention_rate"])),
                "abs_last12_high_gap": abs(safe_float(add0["mean_last12_high_rate"]) - safe_float(swap0["mean_last12_high_rate"])),
                "abs_high_horizon_gap": abs(safe_float(add0["mean_high_horizon_span"]) - safe_float(swap0["mean_high_horizon_span"])),
                "abs_total_high_gap": abs(safe_float(add0["mean_total_high_count"]) - safe_float(swap0["mean_total_high_count"])),
                "abs_far_share_gap": abs(safe_float(add0["mean_far_shell_share"]) - safe_float(swap0["mean_far_shell_share"])),
                "abs_distance_gap": abs(safe_float(add0["mean_weighted_mean_distance"]) - safe_float(swap0["mean_weighted_mean_distance"])),
                "abs_spectral_gap": abs(safe_float(add0["mean_abs_delta_spectral_radius_rel"]) - safe_float(swap0["mean_abs_delta_spectral_radius_rel"])),
            },
            {
                "compare_label": "carrier_gap_at_p2",
                "perturbation": "mixed",
                "abs_established_rate_gap": abs(safe_float(add2["established_far_shell_rate"]) - safe_float(swap2["established_far_shell_rate"])),
                "abs_high_retention_gap": abs(safe_float(add2["mean_high_retention_rate"]) - safe_float(swap2["mean_high_retention_rate"])),
                "abs_last12_high_gap": abs(safe_float(add2["mean_last12_high_rate"]) - safe_float(swap2["mean_last12_high_rate"])),
                "abs_high_horizon_gap": abs(safe_float(add2["mean_high_horizon_span"]) - safe_float(swap2["mean_high_horizon_span"])),
                "abs_total_high_gap": abs(safe_float(add2["mean_total_high_count"]) - safe_float(swap2["mean_total_high_count"])),
                "abs_far_share_gap": abs(safe_float(add2["mean_far_shell_share"]) - safe_float(swap2["mean_far_shell_share"])),
                "abs_distance_gap": abs(safe_float(add2["mean_weighted_mean_distance"]) - safe_float(swap2["mean_weighted_mean_distance"])),
                "abs_spectral_gap": abs(safe_float(add2["mean_abs_delta_spectral_radius_rel"]) - safe_float(swap2["mean_abs_delta_spectral_radius_rel"])),
            },
        ]
    )
    return out


def carrier_gap_score(row: Mapping[str, Any]) -> float:
    keys = (
        "abs_established_rate_gap",
        "abs_high_retention_gap",
        "abs_last12_high_gap",
        "abs_high_horizon_gap",
        "abs_total_high_gap",
        "abs_far_share_gap",
        "abs_distance_gap",
        "abs_spectral_gap",
    )
    return mean_defined(safe_float(row[key]) for key in keys)


def perturbation_support_score(row: Mapping[str, Any]) -> int:
    score = 0
    if safe_float(row["distance_gap"]) >= 1.0:
        score += 1
    if safe_float(row["far_share_gap"]) >= 0.02:
        score += 1
    if safe_float(row["q90_far_share_gap"]) >= 0.02:
        score += 1
    if safe_float(row["last12_high_gap"]) >= 0.10:
        score += 1
    if safe_float(row["high_horizon_gap"]) >= 8.0:
        score += 1
    if safe_float(row["total_high_gap"]) >= 2.0:
        score += 1
    return score


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    compares: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    by_label = {str(row["compare_label"]): row for row in compares}
    add_score = perturbation_support_score(by_label["add_chord_p2_minus_p0"])
    swap_score = perturbation_support_score(by_label["local_swap_p2_minus_p0"])
    p0_gap = carrier_gap_score(by_label["carrier_gap_at_p0"])
    p2_gap = carrier_gap_score(by_label["carrier_gap_at_p2"])

    if add_score >= 4 and swap_score >= 4 and p2_gap + 0.05 <= p0_gap:
        status = "far_shell_horizon_supported"
        note = (
            f"Begge carrierne gir sterkere p2-horisont enn p0 (scores {add_score}/6 og {swap_score}/6), "
            f"og carrier-gapet er mindre ved p2 enn ved p0 ({fmt(p2_gap)} < {fmt(p0_gap)})."
        )
        next_step = "probe_p2_horizon_mechanism"
        next_note = "Neste steg bor forklare selve p2-horisonten, ikke gjenapne target-768-kartet."
    elif add_score >= 3 or swap_score >= 3:
        status = "far_shell_horizon_weak"
        note = f"Far-shell-horisonten gir en svak p2->p0-splittelse (scores add={add_score}, swap={swap_score}), men ikke rent nok ennå."
        next_step = "narrow_p2_horizon_holdout_or_second_observable"
        next_note = "Neste steg bor vaere en enda smalere p2-holdout eller en komplementar target-768-observabel."
    else:
        status = "far_shell_horizon_not_yet"
        note = "Heller ikke far-shell-horisonten skiller target-768-resten rent."
        next_step = "new_target768_observable"
        next_note = "Neste steg bor vaere en ny target-768-observabel, ikke mer far-shell-horisont-tuning."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsen er ren og alle target-768 far-shell-runs matcher onsket perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "far_shell_horizon",
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
    compares: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cg: target-768 far-shell horizon lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om target `768` leses bedre gjennom en vedvarende far-shell-horisont ved placement `2` enn gjennom brede family-labels.")
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
    lines.append("| profile | established | late probe | failed | none | coarse | horizon | retention | last12 high | total high | far share | q90 far share | distance | spectral rel |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {fmt(row['established_far_shell_rate'])} | {fmt(row['late_probe_rate'])} | {fmt(row['failed_far_shell_rate'])} | {fmt(row['no_far_shell_rate'])} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_high_horizon_span'])} | {fmt(row['mean_high_retention_rate'])} | {fmt(row['mean_last12_high_rate'])} | {fmt(row['mean_total_high_count'])} | {fmt(row['mean_far_shell_share'])} | {fmt(row['mean_q90_far_shell_share'])} | {fmt(row['mean_weighted_mean_distance'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} |"
        )
    lines.append("")
    lines.append("## P2 versus P0")
    lines.append("")
    lines.append("| compare | established gap | retention gap | last12 high gap | horizon gap | total high gap | far share gap | q90 far share gap | distance gap | spectral gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares[:2]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['established_rate_gap'])} | {fmt(row['high_retention_gap'])} | {fmt(row['last12_high_gap'])} | {fmt(row['high_horizon_gap'])} | {fmt(row['total_high_gap'])} | {fmt(row['far_share_gap'])} | {fmt(row['q90_far_share_gap'])} | {fmt(row['distance_gap'])} | {fmt(row['spectral_gap'])} |"
        )
    lines.append("")
    lines.append("## Carrier gap")
    lines.append("")
    lines.append("| compare | established gap | retention gap | last12 high gap | horizon gap | total high gap | far share gap | distance gap | spectral gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares[2:]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['abs_established_rate_gap'])} | {fmt(row['abs_high_retention_gap'])} | {fmt(row['abs_last12_high_gap'])} | {fmt(row['abs_high_horizon_gap'])} | {fmt(row['abs_total_high_gap'])} | {fmt(row['abs_far_share_gap'])} | {fmt(row['abs_distance_gap'])} | {fmt(row['abs_spectral_gap'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en smal target-768-observabel rundt p2-lommen, ikke mer bred family-tuning.")
    lines.append("- Positivt signal her betyr at p2 holder far-shell-overvekt over tid, ikke bare i tail-gjennomsnitt.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cg target-768 far-shell horizon lab.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cg_target768_far_shell_horizon_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cg_target768_far_shell_horizon_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cg_target768_far_shell_horizon_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15cg_target768_far_shell_horizon_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cg_target768_far_shell_horizon_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cg_target768_far_shell_horizon_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cg_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cg.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    base_row = next(row for row in base_rows if int(row["target_nodes"]) == TARGET and int(row["growth_seed"]) == GROWTH_SEED)

    run_rows = [
        analyze_run(
            base_state=base_state,
            base_row=base_row,
            perturbation=perturbation,
            placement=placement,
            seed_delta=seed_delta,
        )
        for perturbation in PERTURBATIONS
        for placement in PLACEMENTS
        for seed_delta in SEED_DELTAS
    ]
    aggregate = aggregate_rows(run_rows)
    compares = compare_rows(aggregate)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        compares=compares,
    )
    report_md = build_report(
        target_summary=target_summary,
        aggregate=aggregate,
        compares=compares,
        diagnosis=diagnosis,
    )
    op_md = "\n".join(
        [
            "# v0.15cg operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les dette som en smal target-768 far-shell-runde, ikke som ny bred family-label-tuning.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15cg",
            "",
            "Denne runden sjekker om placement 2 ved storrelse 768 ikke bare ligger lenger ute enn placement 0, men faktisk holder en ytterrand aktiv over tid.",
            "",
            "Hvis det stemmer, er p2 mer enn et tail-snitt: det blir en liten varig ytterhorisont.",
        ]
    ) + "\n"

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_compare_csv, compares)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
