#!/usr/bin/env python3
"""v0.15dd direct route-entry / retention instrumentation.

v15db showed that downstream routing explains p0 high-score/no-horizon false
positives. v15dc showed that existing censored component proxies are too weak
as pre-horizon selectors. This round stops squeezing those proxies and logs the
route process directly per snapshot.

Scope is intentionally narrow:
- target 1024
- add_chord only
- placements p0, p1, p2
- same fresh seed deltas as v15da

This is instrumentation, not a new physics claim and not a selector refit.
"""
from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15cg_target768_far_shell_horizon_lab as v15cg
import relational_universe_v15cs_add_chord_p0_scale_response_holdout as v15cs
import relational_universe_v15cv_add_chord_winning_placement_mechanism_probe as v15cv
import relational_universe_v15da_frozen_intensity_placement_contrast as v15da
import relational_universe_v15q_single_defect_recurrence_lab as v15q


DOC = Path("Documentation")

TARGET_NODES = v15da.TARGET_NODES
GROWTH_SEED = v15da.GROWTH_SEED
PERTURBATION = v15da.PERTURBATION
PLACEMENTS = v15da.PLACEMENTS
FRESH_SEED_DELTAS = v15da.FRESH_SEED_DELTAS
LOG_EVERY = v15da.LOG_EVERY
PRIMARY_SCORE = v15da.PRIMARY_SCORE
FALSE_POSITIVE_SCORE_FLOOR = 0.60


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def median_defined(values: Iterable[float]) -> float:
    vals = sorted(x for x in values if math.isfinite(x))
    if not vals:
        return float("nan")
    mid = len(vals) // 2
    if len(vals) % 2:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2.0


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def clamp01(x: float) -> float:
    if not math.isfinite(x):
        return 0.0
    return max(0.0, min(1.0, x))


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    v15.write_csv(path, list(rows))


def profile_label(placement: int) -> str:
    return f"{PERTURBATION}_p{int(placement)}"


def route_phase(row: Mapping[str, Any]) -> str:
    band = str(row["horizon_band"])
    if band == "high":
        return "high_route"
    if band == "mid":
        return "mid_route"
    if int(row["outer_nodes"]) > 0:
        return "outer_probe"
    return "near_field"


def contiguous_runs(values: Sequence[str], target: str) -> List[Tuple[int, int]]:
    runs: List[Tuple[int, int]] = []
    start = -1
    for idx, value in enumerate(values):
        if value == target and start < 0:
            start = idx
        elif value != target and start >= 0:
            runs.append((start, idx - 1))
            start = -1
    if start >= 0:
        runs.append((start, len(values) - 1))
    return runs


def annotate_route_snapshots(
    *,
    rows: Sequence[Mapping[str, Any]],
    run_ids: Mapping[str, Any],
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    bands = [str(row["horizon_band"]) for row in rows]
    high_runs = contiguous_runs(bands, "high")
    high_run_by_index: Dict[int, Tuple[int, int, int]] = {}
    for run_id, (start, end) in enumerate(high_runs, start=1):
        length = end - start + 1
        for idx in range(start, end + 1):
            high_run_by_index[idx] = (run_id, length, idx - start)

    sustained_runs = [(start, end) for start, end in high_runs if end - start + 1 >= 3]
    first_sustained_start = sustained_runs[0][0] if sustained_runs else -1
    last_high_index = max((end for _, end in high_runs), default=-1)
    retention_indices = (
        set(range(first_sustained_start, last_high_index + 1))
        if first_sustained_start >= 0 and last_high_index >= first_sustained_start
        else set()
    )

    snapshot_rows: List[Dict[str, Any]] = []
    dropout_count = 0
    reentry_count = 0
    mid_to_high_count = 0
    for idx, row in enumerate(rows):
        band = str(row["horizon_band"])
        prev_band = bands[idx - 1] if idx > 0 else ""
        high_run_id, high_run_length, high_run_position = high_run_by_index.get(idx, (0, 0, -1))
        sustained = int(high_run_length >= 3)
        sustained_start = int(sustained and high_run_position == 0)
        in_retention_window = int(idx in retention_indices)
        dropout = int(in_retention_window and idx > first_sustained_start and prev_band == "high" and band != "high")
        reentry = int(in_retention_window and idx > first_sustained_start and prev_band != "high" and band == "high")
        mid_to_high = int(idx > 0 and prev_band == "mid" and band == "high")
        dropout_count += dropout
        reentry_count += reentry
        mid_to_high_count += mid_to_high

        outer_share = safe_float(row["outer_share"])
        weighted_distance = safe_float(row["weighted_mean_distance"])
        high_share_margin = outer_share - v15cg.HIGH_SHARE_THRESHOLD
        high_distance_margin = weighted_distance - v15cg.HIGH_DISTANCE_THRESHOLD
        outer_pressure_without_high = int(
            band != "high"
            and (
                outer_share >= v15cg.MID_SHARE_THRESHOLD
                or int(row["outer_nodes"]) > 0
            )
        )

        snapshot_rows.append(
            {
                **run_ids,
                "snapshot_index": int(row["snapshot_index"]),
                "step": int(row["step"]),
                "horizon_band": band,
                "route_phase": route_phase(row),
                "high_flag": int(band == "high"),
                "mid_flag": int(band == "mid"),
                "mid_or_high_flag": int(band in {"mid", "high"}),
                "outer_present_flag": int(int(row["outer_nodes"]) > 0),
                "outer_pressure_without_high": outer_pressure_without_high,
                "outer_share": outer_share,
                "weighted_mean_distance": weighted_distance,
                "high_share_margin": high_share_margin,
                "high_distance_margin": high_distance_margin,
                "damaged_nodes": int(row["damaged_nodes"]),
                "component_count": int(row["component_count"]),
                "largest_component_fraction": safe_float(row["largest_component_fraction"]),
                "high_run_id": int(high_run_id),
                "high_run_length": int(high_run_length),
                "high_run_position": int(high_run_position),
                "sustained_high3_flag": sustained,
                "sustained_high3_start_flag": sustained_start,
                "retention_window_flag": in_retention_window,
                "dropout_after_entry_flag": dropout,
                "reentry_after_dropout_flag": reentry,
                "mid_to_high_transition_flag": mid_to_high,
            }
        )

    total = max(1, len(snapshot_rows))
    high_count = sum(int(row["high_flag"]) for row in snapshot_rows)
    mid_count = sum(int(row["mid_flag"]) for row in snapshot_rows)
    outer_pressure_count = sum(int(row["outer_pressure_without_high"]) for row in snapshot_rows)
    sustained_count = sum(int(row["sustained_high3_flag"]) for row in snapshot_rows)
    retention_high_count = sum(
        int(row["high_flag"]) for row in snapshot_rows if int(row["retention_window_flag"]) == 1
    )
    retention_window_count = sum(int(row["retention_window_flag"]) for row in snapshot_rows)
    last12 = snapshot_rows[-12:]
    last12_high_rate = mean_defined(float(row["high_flag"]) for row in last12)

    first_high_step = next((int(row["step"]) for row in snapshot_rows if int(row["high_flag"]) == 1), -1)
    first_sustained_step = next(
        (int(row["step"]) for row in snapshot_rows if int(row["sustained_high3_start_flag"]) == 1),
        -1,
    )
    first_outer_pressure_step = next(
        (int(row["step"]) for row in snapshot_rows if int(row["outer_pressure_without_high"]) == 1),
        -1,
    )

    if first_sustained_start < 0:
        pre_entry_rows = snapshot_rows
    else:
        pre_entry_rows = [row for row in snapshot_rows if int(row["snapshot_index"]) < first_sustained_start]
    pre_entry_outer_pressure_rate = mean_defined(float(row["outer_pressure_without_high"]) for row in pre_entry_rows)
    pre_entry_mid_or_high_rate = mean_defined(float(row["mid_or_high_flag"]) for row in pre_entry_rows)
    pre_entry_mean_distance = mean_defined(safe_float(row["weighted_mean_distance"]) for row in pre_entry_rows)

    retention_rate = (
        retention_high_count / retention_window_count
        if retention_window_count
        else 0.0
    )
    longest_high_run = max((end - start + 1 for start, end in high_runs), default=0)
    if first_sustained_start >= 0 and retention_rate >= 0.60 and last12_high_rate >= 0.50:
        direct_label = "sustained_high_retention"
    elif first_sustained_start >= 0 and last12_high_rate < 0.50:
        direct_label = "entry_then_dropout"
    elif high_count > 0:
        direct_label = "transient_high_probe"
    elif outer_pressure_count / total >= 0.25:
        direct_label = "outer_pressure_no_high_entry"
    else:
        direct_label = "no_route_entry"

    summary = {
        **run_ids,
        "snapshot_count": int(total),
        "first_high_step_direct": int(first_high_step),
        "first_sustained_high3_step": int(first_sustained_step),
        "first_outer_pressure_step": int(first_outer_pressure_step),
        "high_snapshot_count": int(high_count),
        "mid_snapshot_count": int(mid_count),
        "outer_pressure_without_high_count": int(outer_pressure_count),
        "sustained_high3_snapshot_count": int(sustained_count),
        "high_run_count": int(len(high_runs)),
        "sustained_high_run_count": int(len(sustained_runs)),
        "longest_high_run_direct": int(longest_high_run),
        "direct_retention_window_count": int(retention_window_count),
        "direct_retention_rate_after_entry": float(retention_rate),
        "direct_dropout_count_after_entry": int(dropout_count),
        "direct_reentry_count_after_dropout": int(reentry_count),
        "mid_to_high_transition_count": int(mid_to_high_count),
        "direct_high_rate": high_count / total,
        "direct_mid_or_high_rate": (mid_count + high_count) / total,
        "outer_pressure_without_high_rate": outer_pressure_count / total,
        "sustained_high3_rate": sustained_count / total,
        "last12_high_rate_direct": float(last12_high_rate),
        "pre_entry_outer_pressure_rate": float(pre_entry_outer_pressure_rate),
        "pre_entry_mid_or_high_rate": float(pre_entry_mid_or_high_rate),
        "pre_entry_mean_distance": float(pre_entry_mean_distance),
        "direct_route_entry_label": direct_label,
        "first_sustained_high3_earliness": (
            clamp01(1.0 - first_sustained_step / max(1, safe_float(rows[-1]["step"])))
            if first_sustained_step >= 0
            else 0.0
        ),
    }
    return snapshot_rows, summary


def run_single(
    *,
    base_state: Any,
    base_row: Mapping[str, Any],
    params: Any,
    placement: int,
    seed_delta: int,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    run_seed = v15da.v15cn.run_seed_for(
        target=TARGET_NODES,
        perturbation=PERTURBATION,
        placement=placement,
        seed_delta=seed_delta,
    )
    res = v15ae.run_defect_with_control_graphs(
        base_state,
        params=params,
        seed=run_seed,
        steps=v15cs.scaled_steps_for_target(TARGET_NODES),
        perturbation=PERTURBATION,
        center_token_index=placement,
        local_coupling="maximal",
        log_every=LOG_EVERY,
    )
    info = dict(res["perturbation_info"])
    support = [int(x) for x in info.get("support", [])]
    support_signature = ",".join(str(x) for x in support)
    base_dist = v7.bfs_distances(base_state.g, support)
    fallback = (max(base_dist.values()) + 1) if base_dist else 1
    snapshot_rows = v15cv.snapshot_rows_for_run(
        target=TARGET_NODES,
        placement=placement,
        seed_delta=seed_delta,
        run_seed=run_seed,
        support_signature=support_signature,
        log_rows=res["log_rows"],
        damaged_sets=res["damaged_sets"],
        control_graphs=res["control_graphs"],
        base_dist=base_dist,
        fallback=fallback,
    )
    recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
    final_drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
    support_features = v15cv.support_mechanism_features(
        target=TARGET_NODES,
        base_state=base_state,
        placement=placement,
        seed_delta=seed_delta,
        run_seed=run_seed,
        support=support,
    )
    mechanism_row = v15cv.run_summary_row(
        target=TARGET_NODES,
        placement=placement,
        seed_delta=seed_delta,
        run_seed=run_seed,
        requested_match=int(v15.v14.perturbation_requested_match(PERTURBATION, str(info.get("type", "unknown")))),
        support_signature=support_signature,
        support_features=support_features,
        recurrence=recurrence,
        final_drift=final_drift,
        snapshot_rows=snapshot_rows,
    )
    run_ids = {
        "target_nodes": TARGET_NODES,
        "growth_seed": GROWTH_SEED,
        "profile_label": profile_label(placement),
        "perturbation": PERTURBATION,
        "placement": int(placement),
        "seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "support_signature": support_signature,
    }
    route_snapshots, route_summary = annotate_route_snapshots(rows=snapshot_rows, run_ids=run_ids)
    run_row = {
        **mechanism_row,
        **route_summary,
        "requested_match": int(v15.v14.perturbation_requested_match(PERTURBATION, str(info.get("type", "unknown")))),
        "source_scope": f"v15dd_fresh_p{placement}",
    }
    return route_snapshots, run_row


def add_frozen_scores(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    prior_rows = v15da.read_csv(DOC / "v15da_frozen_intensity_placement_contrast_runs.csv")
    prior_by_key = {
        (int(safe_float(row["placement"])), int(safe_float(row["seed_delta"]))): row
        for row in prior_rows
    }
    scored_rows: List[Dict[str, Any]] = []
    for row in run_rows:
        key = (int(safe_float(row["placement"])), int(safe_float(row["seed_delta"])))
        prior = prior_by_key[key]
        label = str(row["far_shell_horizon_label"])
        scored = {
            **dict(row),
            PRIMARY_SCORE: safe_float(prior[PRIMARY_SCORE]),
            "decisive_label": v15da.decisive_label(label),
            "prior_v15da_horizon_label": str(prior["far_shell_horizon_label"]),
            "prior_v15da_genealogy_pattern": str(prior["genealogy_pattern"]),
            "score_source": "v15da_frozen_score_reused_no_refit",
        }
        for key_name, value in prior.items():
            if key_name.startswith("frozen_component_"):
                scored[key_name] = value
        scored_rows.append(scored)
    return scored_rows


def analysis_group(row: Mapping[str, Any]) -> str:
    placement = int(safe_float(row["placement"]))
    label = str(row["far_shell_horizon_label"])
    score = safe_float(row[PRIMARY_SCORE])
    if placement == 1 and label == "established_far_shell_horizon":
        return "p1_established"
    if placement == 0 and label == "no_far_shell_horizon" and score >= FALSE_POSITIVE_SCORE_FLOOR:
        return "p0_high_score_no_horizon"
    if placement == 0 and label == "no_far_shell_horizon":
        return "p0_no_horizon_other"
    if placement == 2 and label == "no_far_shell_horizon":
        return "p2_no_horizon"
    if label == "established_far_shell_horizon":
        return "other_established"
    if label == "no_far_shell_horizon":
        return "other_no_horizon"
    return "non_decisive"


def pairwise_auc(pos_values: Sequence[float], neg_values: Sequence[float]) -> float:
    pos = [x for x in pos_values if math.isfinite(x)]
    neg = [x for x in neg_values if math.isfinite(x)]
    if not pos or not neg:
        return float("nan")
    wins = 0.0
    total = 0
    for p in pos:
        for n in neg:
            total += 1
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return wins / total if total else float("nan")


METRICS: Tuple[Tuple[str, str, str], ...] = (
    ("first_sustained_high3_earliness", "higher_is_established", "direct_entry"),
    ("direct_retention_rate_after_entry", "higher_is_established", "direct_retention"),
    ("last12_high_rate_direct", "higher_is_established", "direct_retention"),
    ("sustained_high3_rate", "higher_is_established", "direct_retention"),
    ("direct_high_rate", "higher_is_established", "direct_entry"),
    ("longest_high_run_direct", "higher_is_established", "direct_entry"),
    ("outer_pressure_without_high_rate", "lower_is_established", "failed_route_pressure"),
    ("direct_dropout_count_after_entry", "lower_is_established", "failed_retention"),
    ("genealogy_intensity_index", "higher_is_established", "baseline_failed_selector"),
)


def oriented(row: Mapping[str, Any], metric: str, direction: str) -> float:
    value = safe_float(row[metric])
    return -value if direction == "lower_is_established" else value


def metric_score_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    decisive = [row for row in run_rows if int(row["decisive_label"]) in (0, 1)]
    established = [row for row in decisive if int(row["decisive_label"]) == 1]
    no_horizon = [row for row in decisive if int(row["decisive_label"]) == 0]
    p1_est = [row for row in run_rows if row["analysis_group"] == "p1_established"]
    p0_false = [row for row in run_rows if row["analysis_group"] == "p0_high_score_no_horizon"]
    out: List[Dict[str, Any]] = []
    for metric, direction, family in METRICS:
        est_values = [oriented(row, metric, direction) for row in established]
        no_values = [oriented(row, metric, direction) for row in no_horizon]
        p1_values = [oriented(row, metric, direction) for row in p1_est]
        p0_values = [oriented(row, metric, direction) for row in p0_false]
        raw_est = [safe_float(row[metric]) for row in established]
        raw_no = [safe_float(row[metric]) for row in no_horizon]
        raw_p1 = [safe_float(row[metric]) for row in p1_est]
        raw_p0 = [safe_float(row[metric]) for row in p0_false]
        out.append(
            {
                "metric": metric,
                "direction": direction,
                "metric_family": family,
                "n_established": len(established),
                "n_no_horizon": len(no_horizon),
                "n_p1_established": len(p1_est),
                "n_p0_high_score_no_horizon": len(p0_false),
                "auc_established_vs_no": pairwise_auc(est_values, no_values),
                "auc_p1_established_vs_p0_false_positive": pairwise_auc(p1_values, p0_values),
                "median_established_raw": median_defined(raw_est),
                "median_no_horizon_raw": median_defined(raw_no),
                "median_p1_established_raw": median_defined(raw_p1),
                "median_p0_false_positive_raw": median_defined(raw_p0),
                "median_p1_minus_p0_false_raw": median_defined(raw_p1) - median_defined(raw_p0),
            }
        )
    return sorted(
        out,
        key=lambda row: (
            -safe_float(row["auc_p1_established_vs_p0_false_positive"], -1.0),
            -safe_float(row["auc_established_vs_no"], -1.0),
        ),
    )


def group_summary_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in run_rows:
        grouped[str(row["analysis_group"])].append(row)
    out: List[Dict[str, Any]] = []
    for group, rows in sorted(grouped.items()):
        labels = Counter(str(row["far_shell_horizon_label"]) for row in rows)
        route_labels = Counter(str(row["direct_route_entry_label"]) for row in rows)
        placements = Counter(f"p{int(row['placement'])}" for row in rows)
        out.append(
            {
                "analysis_group": group,
                "n_runs": len(rows),
                "placements": ";".join(f"{k}:{v}" for k, v in sorted(placements.items())),
                "horizon_labels": ";".join(f"{k}:{v}" for k, v in sorted(labels.items())),
                "direct_route_labels": ";".join(f"{k}:{v}" for k, v in sorted(route_labels.items())),
                "median_genealogy_intensity": median_defined(safe_float(row[PRIMARY_SCORE]) for row in rows),
                "median_first_sustained_high3_step": median_defined(safe_float(row["first_sustained_high3_step"]) for row in rows if int(row["first_sustained_high3_step"]) >= 0),
                "median_retention_rate": median_defined(safe_float(row["direct_retention_rate_after_entry"]) for row in rows),
                "median_last12_high_rate": median_defined(safe_float(row["last12_high_rate_direct"]) for row in rows),
                "median_outer_pressure_without_high_rate": median_defined(safe_float(row["outer_pressure_without_high_rate"]) for row in rows),
                "median_dropout_count": median_defined(safe_float(row["direct_dropout_count_after_entry"]) for row in rows),
            }
        )
    return out


def label_cross_tab_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[str, str], List[Mapping[str, Any]]] = defaultdict(list)
    for row in run_rows:
        grouped[(str(row["far_shell_horizon_label"]), str(row["direct_route_entry_label"]))].append(row)
    out: List[Dict[str, Any]] = []
    for (horizon, route), rows in sorted(grouped.items()):
        out.append(
            {
                "far_shell_horizon_label": horizon,
                "direct_route_entry_label": route,
                "n_runs": len(rows),
                "placements": ";".join(sorted({f"p{int(row['placement'])}" for row in rows})),
                "median_genealogy_intensity": median_defined(safe_float(row[PRIMARY_SCORE]) for row in rows),
                "median_outer_pressure_without_high_rate": median_defined(safe_float(row["outer_pressure_without_high_rate"]) for row in rows),
                "median_retention_rate": median_defined(safe_float(row["direct_retention_rate_after_entry"]) for row in rows),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    group_rows: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(safe_float(row["requested_match"])) for row in run_rows), default=0) == 1
    p1 = next((row for row in group_rows if row["analysis_group"] == "p1_established"), None)
    p0 = next((row for row in group_rows if row["analysis_group"] == "p0_high_score_no_horizon"), None)
    best = max(
        (row for row in metric_rows if row["metric_family"] != "baseline_failed_selector"),
        key=lambda row: safe_float(row["auc_p1_established_vs_p0_false_positive"], -1.0),
    )
    baseline = next(row for row in metric_rows if row["metric"] == "genealogy_intensity_index")

    if p1 and p0:
        p1_routes = str(p1["direct_route_labels"])
        p0_routes = str(p0["direct_route_labels"])
        group_note = (
            f"p1 established route labels `{p1_routes}`; p0 high-score/no-horizon route labels `{p0_routes}`. "
            f"Median retention p1={fmt(p1['median_retention_rate'])}, p0={fmt(p0['median_retention_rate'])}; "
            f"outer-pressure-without-high p1={fmt(p1['median_outer_pressure_without_high_rate'])}, p0={fmt(p0['median_outer_pressure_without_high_rate'])}."
        )
    else:
        group_note = "Mangler p1 established eller p0 high-score/no-horizon gruppe."

    best_auc = safe_float(best["auc_p1_established_vs_p0_false_positive"])
    if best_auc >= 0.95:
        primary_status = "direct_route_entry_retention_separates_false_positives"
        primary_note = (
            f"`{best['metric']}` skiller p1 established fra p0 false positives med AUC={fmt(best_auc)}. "
            "Dette er mekanistisk instrumentering, ikke en pre-entry selector."
        )
        next_status = "derive_pre_entry_features_from_direct_route_log"
        next_note = "Bruk snapshot-loggen til aa lage eksplisitte pre-entry kandidater; ikke bruk direct route outcome som predictor."
    elif best_auc >= 0.75:
        primary_status = "direct_route_entry_retention_partly_separates"
        primary_note = (
            f"`{best['metric']}` er beste direct-route observabel med AUC={fmt(best_auc)} mot p0 false positives."
        )
        next_status = "inspect_route_timeline_cases"
        next_note = "Se paa case-timelines for aa finne en tidligere og mindre tautologisk feature."
    else:
        primary_status = "direct_route_entry_retention_not_clean"
        primary_note = f"Beste direct-route observabel `{best['metric']}` har bare AUC={fmt(best_auc)}."
        next_status = "retire_route_entry_as_selector_axis"
        next_note = "Route-entry er da mer beskrivelse enn nyttig selector-akse."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelse er ren og alle requested add_chord-perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Enten startstorrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        },
        {
            "diagnostic_family": "instrumentation_scope",
            "status": "direct_snapshot_route_logging",
            "note": "v15dd rerunner v15da-scope og logger route_phase, sustained high3, retention, dropout og outer-pressure-without-high per snapshot.",
        },
        {"diagnostic_family": "primary_result", "status": primary_status, "note": primary_note},
        {"diagnostic_family": "group_reading", "status": "p1_vs_p0_false_positive_direct_route", "note": group_note},
        {
            "diagnostic_family": "baseline_check",
            "status": "genealogy_intensity_still_not_selector",
            "note": f"Baseline genealogy-intensity AUC mot p0 false positives er {fmt(baseline['auc_p1_established_vs_p0_false_positive'])}.",
        },
        {"diagnostic_family": "next_step", "status": next_status, "note": next_note},
    ]


def build_report(
    *,
    group_rows: Sequence[Mapping[str, Any]],
    label_rows: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dd: direct route-entry / retention lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden rerunner v15da-scope og logger route-state direkte per snapshot.")
    lines.append("Maalet er aa skille faktisk high-route entry/retention fra outer pressure uten high-entry.")
    lines.append("Dette er instrumentering, ikke en ny pre-horizon selector og ikke en fysikk-claim.")
    lines.append("")
    lines.append("## Design")
    lines.append("")
    lines.append("| field | value |")
    lines.append("| --- | --- |")
    lines.append(f"| target | {TARGET_NODES} |")
    lines.append(f"| growth seed | {GROWTH_SEED} |")
    lines.append(f"| perturbation | {PERTURBATION} |")
    lines.append(f"| placements | {';'.join('p' + str(x) for x in PLACEMENTS)} |")
    lines.append(f"| seed deltas | {';'.join(str(x) for x in FRESH_SEED_DELTAS)} |")
    lines.append("")
    lines.append("## Group summary")
    lines.append("")
    lines.append("| group | n | placements | horizon labels | route labels | intensity | first sustained | retention | last12 | outer pressure | dropout |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in group_rows:
        lines.append(
            f"| {row['analysis_group']} | {int(row['n_runs'])} | {row['placements']} | {row['horizon_labels']} | {row['direct_route_labels']} | {fmt(row['median_genealogy_intensity'])} | {fmt(row['median_first_sustained_high3_step'], 1)} | {fmt(row['median_retention_rate'])} | {fmt(row['median_last12_high_rate'])} | {fmt(row['median_outer_pressure_without_high_rate'])} | {fmt(row['median_dropout_count'], 1)} |"
        )
    lines.append("")
    lines.append("## Route label cross-tab")
    lines.append("")
    lines.append("| horizon label | direct route label | n | placements | intensity | outer pressure | retention |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in label_rows:
        lines.append(
            f"| {row['far_shell_horizon_label']} | {row['direct_route_entry_label']} | {int(row['n_runs'])} | {row['placements']} | {fmt(row['median_genealogy_intensity'])} | {fmt(row['median_outer_pressure_without_high_rate'])} | {fmt(row['median_retention_rate'])} |"
        )
    lines.append("")
    lines.append("## Metric ranking")
    lines.append("")
    lines.append("| metric | family | direction | AUC est/no | AUC p1/p0 false | median p1 | median p0 false | p1-p0 false |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in metric_rows:
        lines.append(
            f"| {row['metric']} | {row['metric_family']} | {row['direction']} | {fmt(row['auc_established_vs_no'])} | {fmt(row['auc_p1_established_vs_p0_false_positive'])} | {fmt(row['median_p1_established_raw'])} | {fmt(row['median_p0_false_positive_raw'])} | {fmt(row['median_p1_minus_p0_false_raw'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Direct route logging kan forklare false positives, men maa ikke behandles som en pre-entry predictor.")
    lines.append("- Hvis separasjonen er sterk, er neste steg aa avlede en tidligere feature fra snapshot-loggen og teste den separat.")
    lines.append("- Ikke oppgrader til partikler, Lorentz-likhet, entanglement, invariant eller universell geometri.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15dd", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Bruk direct-route-loggen som mekanistisk instrumentering, ikke som selector direkte.")
    lines.append("- Neste selector-kandidat maa vaere tidligere enn sustained high-entry og pre-registreres separat.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15dd",
            "",
            "Denne runden logger ikke bare om en fjernhale finnes til slutt, men naar et run faktisk gaar inn i en fjern rute og om det holder seg der.",
            "",
            f"- Hovedlesning: `{diag['primary_result']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Kort sagt: vi prover aa skille ekte rute/retensjon fra lokal uro som bare ser kraftig ut.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15dd direct route-entry / retention lab.")
    p.add_argument("--out-target-csv", default=str(DOC / "v15dd_direct_route_target_summary.csv"))
    p.add_argument("--out-snapshots-csv", default=str(DOC / "v15dd_direct_route_snapshot_log.csv"))
    p.add_argument("--out-runs-csv", default=str(DOC / "v15dd_direct_route_run_summary.csv"))
    p.add_argument("--out-groups-csv", default=str(DOC / "v15dd_direct_route_group_summary.csv"))
    p.add_argument("--out-labels-csv", default=str(DOC / "v15dd_direct_route_label_crosstab.csv"))
    p.add_argument("--out-metrics-csv", default=str(DOC / "v15dd_direct_route_metric_scores.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15dd_direct_route_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15dd_direct_route_entry_retention.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15dd_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15dd.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    base_row = next(
        row for row in base_rows
        if int(row["growth_seed"]) == GROWTH_SEED and int(row["target_nodes"]) == TARGET_NODES
    )
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])

    snapshot_rows: List[Dict[str, Any]] = []
    raw_run_rows: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        for seed_delta in FRESH_SEED_DELTAS:
            route_snapshots, run_row = run_single(
                base_state=base_state,
                base_row=base_row,
                params=params,
                placement=int(placement),
                seed_delta=int(seed_delta),
            )
            snapshot_rows.extend(route_snapshots)
            raw_run_rows.append(run_row)

    run_rows = add_frozen_scores(raw_run_rows)
    for row in run_rows:
        row["analysis_group"] = analysis_group(row)
    group_rows = group_summary_rows(run_rows)
    label_rows = label_cross_tab_rows(run_rows)
    metric_rows = metric_score_rows(run_rows)
    target_summary = [
        row for row in v10e.summarize_bases(base_rows)
        if int(row["target_nodes"]) == TARGET_NODES
    ]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        group_rows=group_rows,
        metric_rows=metric_rows,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_snapshots_csv, snapshot_rows)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_groups_csv, group_rows)
    write_csv(args.out_labels_csv, label_rows)
    write_csv(args.out_metrics_csv, metric_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            group_rows=group_rows,
            label_rows=label_rows,
            metric_rows=metric_rows,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
