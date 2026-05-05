#!/usr/bin/env python3
"""v0.15cn p2 horizon scale holdout.

v15cm kept the target-768 p2 far-shell horizon alive but rejected a simple
early local-trigger explanation. This round asks the next narrower question:

does the p2 far-shell horizon survive a scale jump, or is it target-768 local?

Design:
- keep band_zero_del / deep ensemble infrastructure
- keep add_chord and local_swap
- compare only placement p0 and p2
- include a fresh target-768 anchor and one modest target-1024 holdout
- keep the old far-shell horizon label as the primary observable

This is not a broad target search and not a new invariant claim.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15cg_target768_far_shell_horizon_lab as v15cg
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGETS = (768, 1024)
GROWTH_SEED = 202
PLACEMENTS = (0, 2)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (5101, 5153)
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


def run_seed_for(*, target: int, perturbation: str, placement: int, seed_delta: int) -> int:
    perturbation_offset = {"add_chord": 1913, "local_swap": 1979}[perturbation]
    return int(target) * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def raw_far_shell_tail_series(base_state: v7.State, support: Sequence[int], damaged_sets: Sequence[Set[int]]) -> List[Dict[str, float]]:
    dist = v7.bfs_distances(base_state.g, support)
    fallback = (max(dist.values()) + 1) if dist else 1
    out: List[Dict[str, float]] = []
    for damaged in damaged_sets:
        nodes = list(damaged)
        total = max(1, len(nodes))
        dists = [int(dist.get(node, fallback)) for node in nodes]
        far_count = sum(1 for value in dists if value >= 4)
        out.append(
            {
                "far_shell_share": far_count / total,
                "weighted_mean_distance": (sum(dists) / total) if dists else 0.0,
            }
        )
    return out


def band_for_snapshot(snapshot: Mapping[str, Any]) -> str:
    far_share = safe_float(snapshot["far_shell_share"])
    mean_distance = safe_float(snapshot["weighted_mean_distance"])
    if far_share >= v15cg.HIGH_SHARE_THRESHOLD and mean_distance >= v15cg.HIGH_DISTANCE_THRESHOLD:
        return "high"
    if far_share >= v15cg.MID_SHARE_THRESHOLD and mean_distance >= v15cg.MID_DISTANCE_THRESHOLD:
        return "mid"
    return "low"


def horizon_fields(tail_series: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    bands = [band_for_snapshot(row) for row in tail_series]
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
    total_mid_count = sum(1 for band in bands if band == "mid")
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
        "tail_snapshot_count": int(window),
        "high_start_index": int(high_start),
        "last_high_index": int(last_high),
        "high_horizon_span": int(high_horizon),
        "high_retention_rate": float(retention),
        "last12_high_rate": float(last12_high_rate),
        "total_high_count": int(total_high_count),
        "total_mid_count": int(total_mid_count),
        "longest_high_run": int(v15cg.longest_run(bands, "high")),
        "far_shell_horizon_label": label,
        "far_shell_horizon_note": v15cg.horizon_note(label),
    }


def analyze_run(
    *,
    target: int,
    base_state: v7.State,
    base_row: Mapping[str, Any],
    perturbation: str,
    placement: int,
    seed_delta: int,
) -> Dict[str, Any]:
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    run_seed = run_seed_for(target=target, perturbation=perturbation, placement=placement, seed_delta=seed_delta)
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
    tail_series = raw_far_shell_tail_series(base_state, support, res["damaged_sets"][tail_start:])
    horizon = horizon_fields(tail_series)
    drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
    return {
        "profile_label": f"{perturbation}_p{int(placement)}",
        "perturbation": perturbation,
        "target_nodes": int(target),
        "growth_seed": GROWTH_SEED,
        "placement": int(placement),
        "seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "step_budget": int(FULL_STEPS),
        "log_every": int(LOG_EVERY),
        "requested_match": int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
        "support_signature": ",".join(str(x) for x in support),
        "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
        "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
        "mean_far_shell_share": mean_defined(safe_float(row["far_shell_share"]) for row in tail_series),
        "q90_far_shell_share": v15.quantile([safe_float(row["far_shell_share"]) for row in tail_series], 0.90)
        if tail_series
        else float("nan"),
        "mean_weighted_mean_distance": mean_defined(safe_float(row["weighted_mean_distance"]) for row in tail_series),
        "max_weighted_mean_distance": max((safe_float(row["weighted_mean_distance"]) for row in tail_series), default=float("nan")),
        **horizon,
        **drift,
    }


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for target in TARGETS:
        for perturbation in PERTURBATIONS:
            for placement in PLACEMENTS:
                group = [
                    row
                    for row in rows
                    if int(row["target_nodes"]) == int(target)
                    and str(row["perturbation"]) == perturbation
                    and int(row["placement"]) == int(placement)
                ]
                out.append(
                    {
                        "target_nodes": int(target),
                        "profile_label": f"{perturbation}_p{int(placement)}",
                        "perturbation": perturbation,
                        "placement": int(placement),
                        "n_runs": len(group),
                        "established_far_shell_rate": mean_defined(
                            1.0 if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon" else 0.0
                            for row in group
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
                        "mean_abs_delta_spectral_radius_rel": mean_defined(
                            safe_float(row["abs_delta_spectral_radius_rel"]) for row in group
                        ),
                    }
                )
    return out


def p2_support_score(row: Mapping[str, Any]) -> int:
    score = 0
    if safe_float(row["established_rate_gap"]) >= 0.33:
        score += 1
    if safe_float(row["no_horizon_control_gap"]) >= 0.33:
        score += 1
    if safe_float(row["high_retention_gap"]) >= 0.25:
        score += 1
    if safe_float(row["last12_high_gap"]) >= 0.25:
        score += 1
    if safe_float(row["high_horizon_gap"]) >= 16.0:
        score += 1
    if safe_float(row["distance_gap"]) >= 1.0:
        score += 1
    return score


def compare_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_key = {
        (int(row["target_nodes"]), str(row["perturbation"]), int(row["placement"])): row
        for row in aggregate
    }
    out: List[Dict[str, Any]] = []
    for target in TARGETS:
        for perturbation in PERTURBATIONS:
            p0 = by_key[(int(target), perturbation, 0)]
            p2 = by_key[(int(target), perturbation, 2)]
            row: Dict[str, Any] = {
                "target_nodes": int(target),
                "compare_label": f"{perturbation}_p2_minus_p0",
                "perturbation": perturbation,
                "established_rate_gap": safe_float(p2["established_far_shell_rate"]) - safe_float(p0["established_far_shell_rate"]),
                "no_horizon_control_gap": safe_float(p0["no_far_shell_rate"]) - safe_float(p2["no_far_shell_rate"]),
                "high_retention_gap": safe_float(p2["mean_high_retention_rate"]) - safe_float(p0["mean_high_retention_rate"]),
                "last12_high_gap": safe_float(p2["mean_last12_high_rate"]) - safe_float(p0["mean_last12_high_rate"]),
                "high_horizon_gap": safe_float(p2["mean_high_horizon_span"]) - safe_float(p0["mean_high_horizon_span"]),
                "total_high_gap": safe_float(p2["mean_total_high_count"]) - safe_float(p0["mean_total_high_count"]),
                "far_share_gap": safe_float(p2["mean_far_shell_share"]) - safe_float(p0["mean_far_shell_share"]),
                "q90_far_share_gap": safe_float(p2["mean_q90_far_shell_share"]) - safe_float(p0["mean_q90_far_shell_share"]),
                "distance_gap": safe_float(p2["mean_weighted_mean_distance"]) - safe_float(p0["mean_weighted_mean_distance"]),
                "spectral_gap": safe_float(p2["mean_abs_delta_spectral_radius_rel"]) - safe_float(p0["mean_abs_delta_spectral_radius_rel"]),
                "p2_established_rate": safe_float(p2["established_far_shell_rate"]),
                "p0_no_horizon_rate": safe_float(p0["no_far_shell_rate"]),
            }
            row["support_score"] = int(p2_support_score(row))
            row["candidate_supported"] = int(
                int(row["support_score"]) >= 4
                and safe_float(row["p2_established_rate"]) >= 0.50
                and safe_float(row["p0_no_horizon_rate"]) >= 0.50
            )
            out.append(row)
    return out


def scale_summary_rows(aggregate: Sequence[Mapping[str, Any]], compares: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_key = {
        (int(row["target_nodes"]), str(row["perturbation"]), int(row["placement"])): row
        for row in aggregate
    }
    by_compare = {(int(row["target_nodes"]), str(row["perturbation"])): row for row in compares}
    out: List[Dict[str, Any]] = []
    for target in TARGETS:
        supported = [row for row in compares if int(row["target_nodes"]) == int(target) and int(row["candidate_supported"]) == 1]
        add2 = by_key[(int(target), "add_chord", 2)]
        swap2 = by_key[(int(target), "local_swap", 2)]
        add0 = by_key[(int(target), "add_chord", 0)]
        swap0 = by_key[(int(target), "local_swap", 0)]
        add_cmp = by_compare[(int(target), "add_chord")]
        swap_cmp = by_compare[(int(target), "local_swap")]
        out.append(
            {
                "target_nodes": int(target),
                "supported_carrier_count": len(supported),
                "supported_carriers": ";".join(str(row["perturbation"]) for row in supported) if supported else "none",
                "shared_p2_supported": int(len(supported) == len(PERTURBATIONS)),
                "any_p2_supported": int(len(supported) >= 1),
                "add_chord_p2_established_rate": safe_float(add2["established_far_shell_rate"]),
                "local_swap_p2_established_rate": safe_float(swap2["established_far_shell_rate"]),
                "add_chord_p0_no_horizon_rate": safe_float(add0["no_far_shell_rate"]),
                "local_swap_p0_no_horizon_rate": safe_float(swap0["no_far_shell_rate"]),
                "add_chord_support_score": int(add_cmp["support_score"]),
                "local_swap_support_score": int(swap_cmp["support_score"]),
                "mean_p2_established_rate": mean_defined(
                    [safe_float(add2["established_far_shell_rate"]), safe_float(swap2["established_far_shell_rate"])]
                ),
                "mean_p0_no_horizon_rate": mean_defined(
                    [safe_float(add0["no_far_shell_rate"]), safe_float(swap0["no_far_shell_rate"])]
                ),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    scale_summary: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    by_target = {int(row["target_nodes"]): row for row in scale_summary}
    anchor = by_target[768]
    jump = by_target[1024]
    anchor_any = int(anchor["any_p2_supported"]) == 1
    jump_any = int(jump["any_p2_supported"]) == 1
    jump_shared = int(jump["shared_p2_supported"]) == 1

    if anchor_any and jump_shared:
        scale_status = "p2_horizon_scale_holdout_supported"
        scale_note = (
            "Fresh target-768 anchor reproduces at least one p2 carrier, and target-1024 supports both p2 carriers "
            f"(add={fmt(jump['add_chord_p2_established_rate'])}, swap={fmt(jump['local_swap_p2_established_rate'])})."
        )
        next_step = "probe_scale_normal_p2_horizon_mechanism"
        next_note = "Neste steg bor teste en skalanormal mekanisme for p2-horisonten, ikke flere target-768 trigger-observabler."
    elif anchor_any and jump_any:
        scale_status = "p2_horizon_scale_holdout_carrier_specific"
        scale_note = (
            "Fresh target-768 anchor reproduces, and target-1024 retains a p2 signal in at least one carrier "
            f"({jump['supported_carriers']}), but not both."
        )
        next_step = "carrier_scope_scale_holdout"
        next_note = "Neste steg bor skille carrier-scope fra skala-scope med ett smalt ekstra carrier/target-holdout."
    elif anchor_any and not jump_any:
        scale_status = "target768_specific_under_current_budget"
        scale_note = (
            "Fresh target-768 anchor reproduces at least partly, but target-1024 does not support p2 under the same absolute step budget. "
            "Dette kan bety target-768-spesifisitet eller at 1024 trenger lengre dynamisk budsjett."
        )
        next_step = "target1024_budget_extension_or_intermediate_scale"
        next_note = "Neste steg bor teste om 1024 trenger lengre budsjett, eller om et mellomtarget bryter overgangen."
    elif (not anchor_any) and jump_any:
        scale_status = "scale_signal_unanchored"
        scale_note = (
            "Target-1024 viser p2-signal, men fresh target-768 anchor replikerer ikke i denne seedpakken. "
            "Det er interessant, men ikke en ren holdout."
        )
        next_step = "repeat_anchor_or_expand_seed_budget"
        next_note = "Neste steg bor sikre anchor-replikasjon foer sterk skala-tolkning."
    else:
        scale_status = "p2_horizon_scale_holdout_not_supported"
        scale_note = "Verken fresh target-768 anchor eller target-1024 gir p2-horisontstotte i denne smale holdouten."
        next_step = "retire_p2_horizon_or_extend_budget_once"
        next_note = "Neste steg bor enten pensjonere p2-horizon-sporet eller gi det ett eksplisitt lengre budsjett foer avslag."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelser er separerte og alle requested perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Enten startstorrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        },
        {
            "diagnostic_family": "p2_horizon_scale_holdout",
            "status": scale_status,
            "note": scale_note,
        },
        {
            "diagnostic_family": "budget_scope",
            "status": "same_absolute_budget",
            "note": f"Alle targets bruker step_budget={FULL_STEPS}; fravaer ved 1024 er derfor ikke alene bevis for skala-fravaer.",
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
    scale_summary: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cn: p2 horizon scale holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om p2 far-shell-horisonten er target-768-spesifikk eller overlever ett moderat skalahopp til target `1024`.")
    lines.append("Den inkluderer en fresh target-768 anchor og holder oppsettet smalt: `p0` mot `p2`, `add_chord` og `local_swap`, samme absolute step budget.")
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
    lines.append("| target | profile | established | none | horizon | retention | last12 high | total high | far share | distance | spectral rel |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['target_nodes'])} | {row['profile_label']} | {fmt(row['established_far_shell_rate'])} | {fmt(row['no_far_shell_rate'])} | {fmt(row['mean_high_horizon_span'])} | {fmt(row['mean_high_retention_rate'])} | {fmt(row['mean_last12_high_rate'])} | {fmt(row['mean_total_high_count'])} | {fmt(row['mean_far_shell_share'])} | {fmt(row['mean_weighted_mean_distance'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} |"
        )
    lines.append("")
    lines.append("## P2 versus P0")
    lines.append("")
    lines.append("| target | compare | est gap | control none gap | retention gap | last12 gap | horizon gap | distance gap | support score | supported |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares:
        lines.append(
            f"| {int(row['target_nodes'])} | {row['compare_label']} | {fmt(row['established_rate_gap'])} | {fmt(row['no_horizon_control_gap'])} | {fmt(row['high_retention_gap'])} | {fmt(row['last12_high_gap'])} | {fmt(row['high_horizon_gap'])} | {fmt(row['distance_gap'])} | {int(row['support_score'])} | {int(row['candidate_supported'])} |"
        )
    lines.append("")
    lines.append("## Scale summary")
    lines.append("")
    lines.append("| target | supported carriers | shared | add p2 est | swap p2 est | add score | swap score | p0 none |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in scale_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {row['supported_carriers']} | {int(row['shared_p2_supported'])} | {fmt(row['add_chord_p2_established_rate'])} | {fmt(row['local_swap_p2_established_rate'])} | {int(row['add_chord_support_score'])} | {int(row['local_swap_support_score'])} | {fmt(row['mean_p0_no_horizon_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en smal skala-holdout av p2-horisonten, ikke et bredt nytt target-search.")
    lines.append("- Positivt signal betyr bare at samme observabel overlever ett skalahopp under samme absolute budsjett.")
    lines.append("- Negativt signal ved target 1024 er ikke alene bevis mot skalaeffekt, fordi tidsbudsjettet ikke er skalanormalisert.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15cn", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke les dette som global invariant-evidens. Dette er en smal holdout av en p2 far-shell-observabel.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    by_family = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15cn",
        "",
        "Denne runden sjekker om det lille p2-monsteret ved storrelse 768 ogsaa finnes naar vi oker storrelsen til 1024.",
        "",
        f"- Hovedresultat: `{by_family['p2_horizon_scale_holdout']['status']}`.",
        f"- Kontrollstatus: `{by_family['artifact_control']['status']}`.",
        f"- Budsjett-scope: `{by_family['budget_scope']['status']}`.",
        "",
        "Hvis signalet holder, er det mer interessant enn et rent target-768-uhell.",
        "Hvis det ikke holder, kan det enten vaere ekte skala-brudd eller bare at den storre grafen trenger mer tid.",
        "",
        f"- Neste steg: `{by_family['next_step']['status']}` fordi {by_family['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cn p2 horizon scale holdout.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cn_p2_horizon_scale_holdout_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cn_p2_horizon_scale_holdout_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cn_p2_horizon_scale_holdout_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15cn_p2_horizon_scale_holdout_compare.csv")
    p.add_argument("--out-scale-summary-csv", type=str, default="Documentation/v15cn_p2_horizon_scale_holdout_scale_summary.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cn_p2_horizon_scale_holdout_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cn_p2_horizon_scale_holdout_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cn_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cn.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles(list(TARGETS))
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    by_target_state = {ens.target_nodes: base_states[(ens.name, GROWTH_SEED)] for ens in ensembles}
    by_target_row = {
        int(row["target_nodes"]): row
        for row in base_rows
        if int(row["growth_seed"]) == GROWTH_SEED and int(row["target_nodes"]) in TARGETS
    }

    run_rows = [
        analyze_run(
            target=target,
            base_state=by_target_state[int(target)],
            base_row=by_target_row[int(target)],
            perturbation=perturbation,
            placement=placement,
            seed_delta=seed_delta,
        )
        for target in TARGETS
        for perturbation in PERTURBATIONS
        for placement in PLACEMENTS
        for seed_delta in SEED_DELTAS
    ]
    aggregate = aggregate_rows(run_rows)
    compares = compare_rows(aggregate)
    scale_summary = scale_summary_rows(aggregate, compares)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) in TARGETS]
    diagnosis = diagnosis_rows(target_summary=target_summary, run_rows=run_rows, scale_summary=scale_summary)

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_compare_csv, compares)
    write_csv(args.out_scale_summary_csv, scale_summary)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            target_summary=target_summary,
            aggregate=aggregate,
            compares=compares,
            scale_summary=scale_summary,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
