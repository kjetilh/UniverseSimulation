#!/usr/bin/env python3
"""v0.15ch target-768 local_swap p2 horizon holdout.

v15cg found only a weak target-768 far-shell horizon story overall:

- local_swap_p2 looked strongest
- add_chord_p2 showed only partial support
- p0 controls stayed cleaner

The next narrow step is not another broad observable. It is a falsifiable
holdout of the strongest remaining pocket:

does local_swap_p2 keep a far-shell horizon on fresh seeds, and does that hold
under a small neighborhood of horizon thresholds?
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


TARGET = 768
GROWTH_SEED = 202
PROFILES: Tuple[Tuple[str, int], ...] = (
    ("local_swap", 0),
    ("local_swap", 2),
    ("add_chord", 2),
)
SEED_DELTAS = (3607, 3643, 3691, 3739, 3793, 3847)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
THRESHOLD_CONFIGS: Tuple[Dict[str, Any], ...] = (
    {
        "config_label": "loose",
        "high_share_threshold": 0.66,
        "high_distance_threshold": 5.5,
        "mid_share_threshold": 0.60,
        "mid_distance_threshold": 4.5,
    },
    {
        "config_label": "baseline",
        "high_share_threshold": 0.68,
        "high_distance_threshold": 6.0,
        "mid_share_threshold": 0.62,
        "mid_distance_threshold": 5.0,
    },
    {
        "config_label": "tight",
        "high_share_threshold": 0.70,
        "high_distance_threshold": 6.5,
        "mid_share_threshold": 0.64,
        "mid_distance_threshold": 5.5,
    },
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


def run_seed_for(*, perturbation: str, placement: int, seed_delta: int) -> int:
    perturbation_offset = {"add_chord": 1211, "local_swap": 1277}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


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


def band_for_snapshot(snapshot: Mapping[str, Any], config: Mapping[str, Any]) -> str:
    far_share = safe_float(snapshot["far_shell_share"])
    mean_distance = safe_float(snapshot["weighted_mean_distance"])
    if far_share >= safe_float(config["high_share_threshold"]) and mean_distance >= safe_float(config["high_distance_threshold"]):
        return "high"
    if far_share >= safe_float(config["mid_share_threshold"]) and mean_distance >= safe_float(config["mid_distance_threshold"]):
        return "mid"
    return "low"


def analyze_raw_run(
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
    tail_damaged = res["damaged_sets"][tail_start:]
    tail_series = raw_far_shell_tail_series(base_state, support, tail_damaged)
    drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
    row = {
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
        "tail_snapshot_count": int(len(tail_series)),
        "mean_far_shell_share": mean_defined(safe_float(item["far_shell_share"]) for item in tail_series),
        "q90_far_shell_share": v15.quantile([safe_float(item["far_shell_share"]) for item in tail_series], 0.90) if tail_series else float("nan"),
        "mean_weighted_mean_distance": mean_defined(safe_float(item["weighted_mean_distance"]) for item in tail_series),
        "max_weighted_mean_distance": max((safe_float(item["weighted_mean_distance"]) for item in tail_series), default=float("nan")),
        **drift,
        "_tail_series": tail_series,
    }
    return row


def threshold_row(raw_row: Mapping[str, Any], config: Mapping[str, Any]) -> Dict[str, Any]:
    tail_series = list(raw_row["_tail_series"])
    bands = [band_for_snapshot(snapshot, config) for snapshot in tail_series]
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
        "profile_label": str(raw_row["profile_label"]),
        "perturbation": str(raw_row["perturbation"]),
        "target_nodes": int(raw_row["target_nodes"]),
        "growth_seed": int(raw_row["growth_seed"]),
        "placement": int(raw_row["placement"]),
        "seed_delta": int(raw_row["seed_delta"]),
        "run_seed": int(raw_row["run_seed"]),
        "requested_match": int(raw_row["requested_match"]),
        "support_signature": str(raw_row["support_signature"]),
        "config_label": str(config["config_label"]),
        "high_share_threshold": safe_float(config["high_share_threshold"]),
        "high_distance_threshold": safe_float(config["high_distance_threshold"]),
        "mid_share_threshold": safe_float(config["mid_share_threshold"]),
        "mid_distance_threshold": safe_float(config["mid_distance_threshold"]),
        "full_exact_return_rate": safe_float(raw_row["full_exact_return_rate"]),
        "full_coarse_return_rate": safe_float(raw_row["full_coarse_return_rate"]),
        "tail_snapshot_count": int(raw_row["tail_snapshot_count"]),
        "high_start_index": int(high_start),
        "last_high_index": int(last_high),
        "high_horizon_span": int(high_horizon),
        "high_retention_rate": float(retention),
        "last12_high_rate": float(last12_high_rate),
        "total_high_count": int(total_high_count),
        "total_mid_count": int(total_mid_count),
        "longest_high_run": int(v15cg.longest_run(bands, "high")),
        "mean_far_shell_share": safe_float(raw_row["mean_far_shell_share"]),
        "q90_far_shell_share": safe_float(raw_row["q90_far_shell_share"]),
        "mean_weighted_mean_distance": safe_float(raw_row["mean_weighted_mean_distance"]),
        "max_weighted_mean_distance": safe_float(raw_row["max_weighted_mean_distance"]),
        "far_shell_horizon_label": label,
        "far_shell_horizon_note": v15cg.horizon_note(label),
        "abs_delta_spectral_radius_rel": safe_float(raw_row["abs_delta_spectral_radius_rel"]),
    }


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for config in THRESHOLD_CONFIGS:
        config_label = str(config["config_label"])
        for perturbation, placement in PROFILES:
            group = [
                row
                for row in rows
                if str(row["config_label"]) == config_label
                and str(row["perturbation"]) == perturbation
                and int(row["placement"]) == int(placement)
            ]
            out.append(
                {
                    "config_label": config_label,
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
    return out


def local_support_score(row: Mapping[str, Any]) -> int:
    score = 0
    if safe_float(row["established_rate_gap"]) >= 0.33:
        score += 1
    if safe_float(row["no_horizon_control_gap"]) >= 0.33:
        score += 1
    if safe_float(row["high_retention_gap"]) >= 0.33:
        score += 1
    if safe_float(row["last12_high_gap"]) >= 0.33:
        score += 1
    if safe_float(row["high_horizon_gap"]) >= 24.0:
        score += 1
    if safe_float(row["distance_gap"]) >= 1.0:
        score += 1
    return score


def compare_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_key = {(str(row["config_label"]), str(row["profile_label"])): row for row in aggregate}
    out: List[Dict[str, Any]] = []
    for config in THRESHOLD_CONFIGS:
        config_label = str(config["config_label"])
        swap0 = by_key[(config_label, "local_swap_p0")]
        swap2 = by_key[(config_label, "local_swap_p2")]
        add2 = by_key[(config_label, "add_chord_p2")]
        local_row = {
            "config_label": config_label,
            "compare_label": "local_swap_p2_minus_local_swap_p0",
            "established_rate_gap": safe_float(swap2["established_far_shell_rate"]) - safe_float(swap0["established_far_shell_rate"]),
            "no_horizon_control_gap": safe_float(swap0["no_far_shell_rate"]) - safe_float(swap2["no_far_shell_rate"]),
            "high_retention_gap": safe_float(swap2["mean_high_retention_rate"]) - safe_float(swap0["mean_high_retention_rate"]),
            "last12_high_gap": safe_float(swap2["mean_last12_high_rate"]) - safe_float(swap0["mean_last12_high_rate"]),
            "high_horizon_gap": safe_float(swap2["mean_high_horizon_span"]) - safe_float(swap0["mean_high_horizon_span"]),
            "total_high_gap": safe_float(swap2["mean_total_high_count"]) - safe_float(swap0["mean_total_high_count"]),
            "far_share_gap": safe_float(swap2["mean_far_shell_share"]) - safe_float(swap0["mean_far_shell_share"]),
            "q90_far_share_gap": safe_float(swap2["mean_q90_far_shell_share"]) - safe_float(swap0["mean_q90_far_shell_share"]),
            "distance_gap": safe_float(swap2["mean_weighted_mean_distance"]) - safe_float(swap0["mean_weighted_mean_distance"]),
            "spectral_gap": safe_float(swap2["mean_abs_delta_spectral_radius_rel"]) - safe_float(swap0["mean_abs_delta_spectral_radius_rel"]),
        }
        local_row["support_score"] = int(local_support_score(local_row))
        local_row["candidate_supported"] = int(
            local_row["support_score"] >= 4
            and safe_float(swap2["established_far_shell_rate"]) >= 0.50
            and safe_float(swap0["no_far_shell_rate"]) >= 0.50
        )
        out.append(local_row)
        out.append(
            {
                "config_label": config_label,
                "compare_label": "local_swap_p2_minus_add_chord_p2",
                "established_rate_gap": safe_float(swap2["established_far_shell_rate"]) - safe_float(add2["established_far_shell_rate"]),
                "high_retention_gap": safe_float(swap2["mean_high_retention_rate"]) - safe_float(add2["mean_high_retention_rate"]),
                "last12_high_gap": safe_float(swap2["mean_last12_high_rate"]) - safe_float(add2["mean_last12_high_rate"]),
                "high_horizon_gap": safe_float(swap2["mean_high_horizon_span"]) - safe_float(add2["mean_high_horizon_span"]),
                "total_high_gap": safe_float(swap2["mean_total_high_count"]) - safe_float(add2["mean_total_high_count"]),
                "far_share_gap": safe_float(swap2["mean_far_shell_share"]) - safe_float(add2["mean_far_shell_share"]),
                "q90_far_share_gap": safe_float(swap2["mean_q90_far_shell_share"]) - safe_float(add2["mean_q90_far_shell_share"]),
                "distance_gap": safe_float(swap2["mean_weighted_mean_distance"]) - safe_float(add2["mean_weighted_mean_distance"]),
                "spectral_gap": safe_float(swap2["mean_abs_delta_spectral_radius_rel"]) - safe_float(add2["mean_abs_delta_spectral_radius_rel"]),
                "candidate_supported": int(
                    safe_float(swap2["established_far_shell_rate"]) >= 0.50
                    and safe_float(add2["established_far_shell_rate"]) + 0.17 <= safe_float(swap2["established_far_shell_rate"])
                ),
            }
        )
    return out


def robustness_rows(aggregate: Sequence[Mapping[str, Any]], compares: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_key = {(str(row["config_label"]), str(row["profile_label"])): row for row in aggregate}
    local_rows = [row for row in compares if str(row["compare_label"]) == "local_swap_p2_minus_local_swap_p0"]
    cross_rows = [row for row in compares if str(row["compare_label"]) == "local_swap_p2_minus_add_chord_p2"]
    swap2_rows = [by_key[(str(config["config_label"]), "local_swap_p2")] for config in THRESHOLD_CONFIGS]
    add2_rows = [by_key[(str(config["config_label"]), "add_chord_p2")] for config in THRESHOLD_CONFIGS]
    supported_configs = [str(row["config_label"]) for row in local_rows if int(row["candidate_supported"]) == 1]
    carrier_specific_configs = [str(row["config_label"]) for row in cross_rows if int(row["candidate_supported"]) == 1]
    cross_carrier_configs = [
        str(config["config_label"])
        for config in THRESHOLD_CONFIGS
        if safe_float(by_key[(str(config["config_label"]), "local_swap_p2")]["established_far_shell_rate"]) >= 0.50
        and safe_float(by_key[(str(config["config_label"]), "add_chord_p2")]["established_far_shell_rate"]) >= 0.50
    ]
    return [
        {
            "subject": "local_swap_p2_far_shell_horizon",
            "n_threshold_configs": len(THRESHOLD_CONFIGS),
            "supported_config_count": len(supported_configs),
            "supported_config_labels": ";".join(supported_configs) if supported_configs else "none",
            "carrier_specific_config_count": len(carrier_specific_configs),
            "carrier_specific_config_labels": ";".join(carrier_specific_configs) if carrier_specific_configs else "none",
            "cross_carrier_p2_config_count": len(cross_carrier_configs),
            "cross_carrier_p2_config_labels": ";".join(cross_carrier_configs) if cross_carrier_configs else "none",
            "min_local_swap_p2_established_rate": min((safe_float(row["established_far_shell_rate"]) for row in swap2_rows), default=float("nan")),
            "max_local_swap_p2_established_rate": max((safe_float(row["established_far_shell_rate"]) for row in swap2_rows), default=float("nan")),
            "min_add_chord_p2_established_rate": min((safe_float(row["established_far_shell_rate"]) for row in add2_rows), default=float("nan")),
            "max_add_chord_p2_established_rate": max((safe_float(row["established_far_shell_rate"]) for row in add2_rows), default=float("nan")),
            "min_local_support_score": min((int(row["support_score"]) for row in local_rows), default=0),
            "max_local_support_score": max((int(row["support_score"]) for row in local_rows), default=0),
        }
    ]


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    raw_run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    compares: Sequence[Mapping[str, Any]],
    robustness: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in raw_run_rows), default=0) == 1
    by_key = {(str(row["config_label"]), str(row["profile_label"])): row for row in aggregate}
    by_compare = {(str(row["config_label"]), str(row["compare_label"])): row for row in compares}
    baseline_swap2 = by_key[("baseline", "local_swap_p2")]
    baseline_swap0 = by_key[("baseline", "local_swap_p0")]
    baseline_add2 = by_key[("baseline", "add_chord_p2")]
    baseline_local = by_compare[("baseline", "local_swap_p2_minus_local_swap_p0")]
    robustness_row = robustness[0]
    supported_count = int(robustness_row["supported_config_count"])
    carrier_specific_count = int(robustness_row["carrier_specific_config_count"])
    cross_carrier_count = int(robustness_row["cross_carrier_p2_config_count"])

    shared_p2 = cross_carrier_count >= 2

    if int(baseline_local["candidate_supported"]) == 1 and supported_count >= 2:
        horizon_status = "local_swap_p2_horizon_holdout_supported"
        if shared_p2:
            horizon_note = (
                f"local_swap_p2 holder pa holdout ved baseline og {supported_count} av {int(robustness_row['n_threshold_configs'])} terskelkonfigurasjoner; "
                f"baseline established-rate er {fmt(baseline_swap2['established_far_shell_rate'])} mot {fmt(baseline_swap0['established_far_shell_rate'])} for p0-kontrollen, "
                f"og add_chord_p2 holder samtidig {fmt(baseline_add2['established_far_shell_rate'])} ved baseline."
            )
            next_step = "probe_shared_p2_horizon_mechanism"
            next_note = "Neste steg bor forklare hvorfor p2 bygger halehorisont pa tvers av carrier, ikke gjenapne bred target-768 family-tuning."
        else:
            horizon_note = (
                f"local_swap_p2 holder pa holdout ved baseline og {supported_count} av {int(robustness_row['n_threshold_configs'])} terskelkonfigurasjoner; "
                f"baseline established-rate er {fmt(baseline_swap2['established_far_shell_rate'])} mot {fmt(baseline_swap0['established_far_shell_rate'])} for p0-kontrollen."
            )
            next_step = "probe_local_swap_p2_mechanism"
            next_note = "Neste steg bor forklare hvorfor local_swap_p2 bygger halehorisont, ikke gjenapne bred target-768 family-tuning."
    elif safe_float(baseline_swap2["established_far_shell_rate"]) >= 0.50 or supported_count >= 1:
        horizon_status = "local_swap_p2_horizon_holdout_weak"
        horizon_note = (
            f"local_swap_p2 viser fortsatt noe holdout-signal (baseline established-rate {fmt(baseline_swap2['established_far_shell_rate'])}, "
            f"stottet i {supported_count} av {int(robustness_row['n_threshold_configs'])} terskelkonfigurasjoner), men ikke rent nok ennå."
        )
        next_step = "second_target768_mechanism_observable"
        next_note = "Neste steg bor vaere en komplementar mekanismeobservabel rundt p2-lommen, ikke en sterkere fysikklesning."
    else:
        horizon_status = "local_swap_p2_horizon_not_replicated"
        horizon_note = (
            f"local_swap_p2-horisonten holder ikke pa holdout; baseline established-rate er {fmt(baseline_swap2['established_far_shell_rate'])} "
            f"og ingen terskelkonfigurasjon gir en ren kandidat."
        )
        next_step = "new_observable_axis_or_scale_decision"
        next_note = "Neste steg bor vaere en ny observabelakse eller ny skalaavgjorelse, ikke mer p2-horisont-tuning."

    if carrier_specific_count >= 2 and cross_carrier_count < 2:
        carrier_status = "local_swap_specific_candidate"
        carrier_note = (
            f"Holdout-signalet ser smalere ut enn en generell p2-lov: local_swap_p2 slar add_chord_p2 i {carrier_specific_count} av "
            f"{int(robustness_row['n_threshold_configs'])} terskelkonfigurasjoner."
        )
    elif cross_carrier_count >= 2:
        carrier_status = "shared_p2_candidate"
        carrier_note = (
            f"Begge carrierne viser minst noe p2-horisont i {cross_carrier_count} terskelkonfigurasjoner; dette er fortsatt feature-level evidens, ikke en arts-paastand."
        )
    else:
        carrier_status = "carrier_scope_unclear"
        carrier_note = (
            f"Carrier-scope er fortsatt uklar: baseline established-rates er local_swap_p2={fmt(baseline_swap2['established_far_shell_rate'])}, "
            f"add_chord_p2={fmt(baseline_add2['established_far_shell_rate'])}."
        )

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Enten startstorrelsesseparasjon eller perturbasjonsmatching er uklar i denne holdouten."
            ),
        },
        {
            "diagnostic_family": "local_swap_p2_horizon_holdout",
            "status": horizon_status,
            "note": horizon_note,
        },
        {
            "diagnostic_family": "carrier_scope",
            "status": carrier_status,
            "note": carrier_note,
        },
        {
            "diagnostic_family": "baseline_control",
            "status": "observed",
            "note": (
                f"baseline p0 no-horizon={fmt(baseline_swap0['no_far_shell_rate'])}; "
                f"baseline local support score={int(baseline_local['support_score'])}/6."
            ),
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
    robustness: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15ch: target-768 local_swap p2 horizon holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden holder bare ut den sterkeste resten fra `v15cg`: `local_swap_p2` ved target `768`.")
    lines.append("Den bruker friske run-seeds og et lite nabolag av horisont-terskler for aa teste om signalet er mer enn ett enkelt cutoff-treff.")
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
    lines.append("## Profile x threshold summary")
    lines.append("")
    lines.append("| config | profile | established | none | horizon | retention | last12 high | total high | far share | distance | spectral rel |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for config in THRESHOLD_CONFIGS:
        config_label = str(config["config_label"])
        group = [row for row in aggregate if str(row["config_label"]) == config_label]
        for row in group:
            lines.append(
                f"| {config_label} | {row['profile_label']} | {fmt(row['established_far_shell_rate'])} | {fmt(row['no_far_shell_rate'])} | {fmt(row['mean_high_horizon_span'])} | {fmt(row['mean_high_retention_rate'])} | {fmt(row['mean_last12_high_rate'])} | {fmt(row['mean_total_high_count'])} | {fmt(row['mean_far_shell_share'])} | {fmt(row['mean_weighted_mean_distance'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} |"
            )
    lines.append("")
    lines.append("## Candidate comparison")
    lines.append("")
    lines.append("| config | compare | est gap | control none gap | retention gap | last12 gap | horizon gap | distance gap | support score | supported |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares:
        if str(row["compare_label"]) != "local_swap_p2_minus_local_swap_p0":
            continue
        lines.append(
            f"| {row['config_label']} | {row['compare_label']} | {fmt(row['established_rate_gap'])} | {fmt(row['no_horizon_control_gap'])} | {fmt(row['high_retention_gap'])} | {fmt(row['last12_high_gap'])} | {fmt(row['high_horizon_gap'])} | {fmt(row['distance_gap'])} | {int(row['support_score'])} | {int(row['candidate_supported'])} |"
        )
    lines.append("")
    lines.append("## Cross-carrier contrast")
    lines.append("")
    lines.append("| config | compare | est gap | retention gap | last12 gap | horizon gap | far share gap | distance gap | candidate-specific |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares:
        if str(row["compare_label"]) != "local_swap_p2_minus_add_chord_p2":
            continue
        lines.append(
            f"| {row['config_label']} | {row['compare_label']} | {fmt(row['established_rate_gap'])} | {fmt(row['high_retention_gap'])} | {fmt(row['last12_high_gap'])} | {fmt(row['high_horizon_gap'])} | {fmt(row['far_share_gap'])} | {fmt(row['distance_gap'])} | {int(row['candidate_supported'])} |"
        )
    lines.append("")
    lines.append("## Robustness summary")
    lines.append("")
    lines.append("| subject | supported configs | carrier-specific configs | cross-carrier configs | swap2 est min/max | add2 est min/max | support score min/max |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in robustness:
        lines.append(
            f"| {row['subject']} | {row['supported_config_labels']} | {row['carrier_specific_config_labels']} | {row['cross_carrier_p2_config_labels']} | {fmt(row['min_local_swap_p2_established_rate'])}/{fmt(row['max_local_swap_p2_established_rate'])} | {fmt(row['min_add_chord_p2_established_rate'])}/{fmt(row['max_add_chord_p2_established_rate'])} | {int(row['min_local_support_score'])}/{int(row['max_local_support_score'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en holdout av en smal p2-lomme, ikke en ny bred target-768-runde.")
    lines.append("- Positivt signal her betyr bare at local_swap_p2 ser mer robust ut som feature-level halehorisont under sma terskelendringer.")
    lines.append("- Negativt signal her betyr at v15cg traff en svak lomme som ikke holder rent paa friske seeds eller nabo-cutoffs.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15ch", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Les dette som en smal holdout av `local_swap_p2`, ikke som bevis for partikler eller universell geometri.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    short = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15ch",
        "",
        "Denne runden sjekker om ett lite og lovende monster i simuleringen faktisk dukker opp igjen nar vi prover pa nytt.",
        "",
        f"- Hovedresultat: `{short['local_swap_p2_horizon_holdout']['status']}`.",
        f"- Kontrollstatus: `{short['artifact_control']['status']}`.",
        f"- Carrier-scope: `{short['carrier_scope']['status']}`.",
        "",
        "Dette betyr fortsatt ikke at vi har funnet noe som fortjener aa kalles en partikkel.",
        "Det betyr bare at vi er i ferd med aa finne ut om ett lite monster er repeterbart eller om det var et skjort lokalt treff.",
        "",
        f"- Neste steg: `{short['next_step']['status']}` fordi {short['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ch target-768 local_swap p2 horizon holdout.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15ch_target768_local_swap_p2_horizon_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15ch_target768_local_swap_p2_horizon_runs.csv")
    p.add_argument("--out-threshold-csv", type=str, default="Documentation/v15ch_target768_local_swap_p2_horizon_threshold_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ch_target768_local_swap_p2_horizon_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15ch_target768_local_swap_p2_horizon_compare.csv")
    p.add_argument("--out-robustness-csv", type=str, default="Documentation/v15ch_target768_local_swap_p2_horizon_robustness.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ch_target768_local_swap_p2_horizon_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ch_target768_local_swap_p2_horizon_holdout_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ch_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ch.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    base_row = next(row for row in base_rows if int(row["target_nodes"]) == TARGET and int(row["growth_seed"]) == GROWTH_SEED)

    raw_run_rows = [
        analyze_raw_run(
            base_state=base_state,
            base_row=base_row,
            perturbation=perturbation,
            placement=placement,
            seed_delta=seed_delta,
        )
        for perturbation, placement in PROFILES
        for seed_delta in SEED_DELTAS
    ]
    threshold_rows = [
        threshold_row(raw_row, config)
        for raw_row in raw_run_rows
        for config in THRESHOLD_CONFIGS
    ]
    aggregate = aggregate_rows(threshold_rows)
    compares = compare_rows(aggregate)
    robustness = robustness_rows(aggregate, compares)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        raw_run_rows=raw_run_rows,
        aggregate=aggregate,
        compares=compares,
        robustness=robustness,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, [{k: v for k, v in row.items() if not str(k).startswith("_")} for row in raw_run_rows])
    write_csv(args.out_threshold_csv, threshold_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_compare_csv, compares)
    write_csv(args.out_robustness_csv, robustness)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            target_summary=target_summary,
            aggregate=aggregate,
            compares=compares,
            robustness=robustness,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
