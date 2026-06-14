#!/usr/bin/env python3
"""v0.15df strict pre-entry support/topology synthesis.

v15de showed that direct route-prefix fields do not provide a legitimate
strict pre-entry selector. This no-new-dynamics round deliberately stops
squeezing route logs and tests non-route observables from existing component
trajectories:

- static support geometry from v15dd run summaries
- component topology and support-distance structure from v15da component rows
- strict windows only: steps <= 32, <= 64, <= 96

Downstream horizon and direct-route labels are used only as evaluation labels.
No route-entry/retention fields are used as candidate features.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v15_defect_lifetime_lab as v15


DOC = Path("Documentation")
RUNS_CSV = DOC / "v15dd_direct_route_run_summary.csv"
COMPONENTS_CSV = DOC / "v15da_frozen_intensity_placement_contrast_component_trajectories.csv"

STRICT_WINDOWS = (32, 64, 96)
PRIMARY_SCORE = "genealogy_intensity_index"
FALSE_POSITIVE_SCORE_FLOOR = 0.60


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def clamp01(x: float) -> float:
    if not math.isfinite(x):
        return 0.0
    return max(0.0, min(1.0, x))


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


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def run_key(row: Mapping[str, Any]) -> Tuple[int, int]:
    return int(safe_float(row["placement"])), int(safe_float(row["seed_delta"]))


def decisive_label(label: str) -> int:
    if label == "established_far_shell_horizon":
        return 1
    if label == "no_far_shell_horizon":
        return 0
    return -1


def analysis_group(placement: int, label: str, score: float) -> str:
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


def linear_slope(points: Sequence[Tuple[float, float]]) -> float:
    pts = [(x, y) for x, y in points if math.isfinite(x) and math.isfinite(y)]
    if len(pts) < 2:
        return float("nan")
    xs = [x for x, _ in pts]
    ys = [y for _, y in pts]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    denom = sum((x - xbar) ** 2 for x in xs)
    if denom <= 0:
        return float("nan")
    return sum((x - xbar) * (y - ybar) for x, y in pts) / denom


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


def snapshot_groups(rows: Sequence[Mapping[str, str]]) -> Dict[int, List[Mapping[str, str]]]:
    grouped: Dict[int, List[Mapping[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[int(safe_float(row["snapshot_index"]))].append(row)
    return dict(grouped)


def mass_weighted(rows: Sequence[Mapping[str, str]], field: str) -> float:
    total_weight = 0.0
    total = 0.0
    for row in rows:
        weight = safe_float(row["size_nodes"])
        value = safe_float(row[field])
        if not math.isfinite(weight) or weight <= 0 or not math.isfinite(value):
            continue
        total += value * weight
        total_weight += weight
    return total / total_weight if total_weight else float("nan")


def mass_fraction(rows: Sequence[Mapping[str, str]], predicate: Any) -> float:
    total = 0.0
    selected = 0.0
    for row in rows:
        weight = safe_float(row["size_nodes"])
        if not math.isfinite(weight) or weight <= 0:
            continue
        total += weight
        if predicate(row):
            selected += weight
    return selected / total if total else float("nan")


def summarize_snapshot(rows: Sequence[Mapping[str, str]]) -> Dict[str, Any]:
    first = rows[0]
    total_mass = safe_float(first["total_defect_mass"])
    component_count = safe_float(first["component_count"])
    largest_fraction = safe_float(first["largest_component_fraction"])
    total_beta1 = sum(safe_float(row["beta1_local"], 0.0) for row in rows)
    total_boundary = sum(safe_float(row["boundary_edge_count"], 0.0) for row in rows)
    total_internal = sum(safe_float(row["internal_edge_count"], 0.0) for row in rows)
    mean_support_distance = mass_weighted(rows, "mean_support_distance")
    max_support_distance = max((safe_float(row["max_support_distance"]) for row in rows), default=float("nan"))
    min_support_distance = min((safe_float(row["min_support_distance"]) for row in rows), default=float("nan"))
    boundary_to_volume = mass_weighted(rows, "boundary_to_volume")
    support_touch = mass_fraction(rows, lambda row: safe_float(row["min_support_distance"]) <= 0.0)
    near_support = mass_fraction(rows, lambda row: safe_float(row["min_support_distance"]) <= 1.0)
    gate_bridge = mass_fraction(
        rows,
        lambda row: safe_float(row["min_support_distance"]) <= 1.0 and safe_float(row["max_support_distance"]) >= 2.0,
    )
    spanning = mass_fraction(
        rows,
        lambda row: safe_float(row["max_support_distance"]) - safe_float(row["min_support_distance"]) >= 2.0,
    )
    beta_component = mass_fraction(rows, lambda row: safe_float(row["beta1_local"]) > 0.0)
    boundary_heavy = mass_fraction(rows, lambda row: safe_float(row["boundary_to_volume"]) >= 4.0)
    beta1_per_mass = total_beta1 / max(1.0, total_mass)
    boundary_per_mass = total_boundary / max(1.0, total_mass)
    internal_per_mass = total_internal / max(1.0, total_mass)
    fragmentation_pressure = component_count * (1.0 - largest_fraction)
    gate_tension = (
        0.30 * clamp01(gate_bridge)
        + 0.20 * clamp01(spanning)
        + 0.20 * clamp01(boundary_to_volume / 12.0)
        + 0.15 * clamp01(beta1_per_mass)
        + 0.15 * clamp01(fragmentation_pressure / 12.0)
    )
    coherent_gate = gate_bridge * largest_fraction * clamp01(total_mass / 32.0)
    trapped_core = near_support * clamp01(boundary_to_volume / 12.0) * clamp01(1.0 - mean_support_distance / 4.0)
    return {
        "snapshot_index": int(safe_float(first["snapshot_index"])),
        "step": safe_float(first["step"]),
        "total_mass": total_mass,
        "component_count": component_count,
        "largest_fraction": largest_fraction,
        "total_beta1": total_beta1,
        "total_boundary_edges": total_boundary,
        "total_internal_edges": total_internal,
        "mean_support_distance": mean_support_distance,
        "max_support_distance": max_support_distance,
        "min_support_distance": min_support_distance,
        "boundary_to_volume": boundary_to_volume,
        "support_touch_fraction": support_touch,
        "near_support_fraction": near_support,
        "gate_bridge_fraction": gate_bridge,
        "spanning_fraction": spanning,
        "beta_component_fraction": beta_component,
        "boundary_heavy_fraction": boundary_heavy,
        "beta1_per_mass": beta1_per_mass,
        "boundary_per_mass": boundary_per_mass,
        "internal_per_mass": internal_per_mass,
        "fragmentation_pressure": fragmentation_pressure,
        "gate_tension_index": gate_tension,
        "coherent_gate_index": coherent_gate,
        "trapped_core_index": trapped_core,
    }


def summarize_run_snapshots(rows: Sequence[Mapping[str, str]]) -> List[Dict[str, Any]]:
    return [
        summarize_snapshot(snap)
        for _, snap in sorted(snapshot_groups(rows).items())
    ]


def window_summary(snapshots: Sequence[Mapping[str, Any]], window: int) -> Dict[str, Any]:
    selected = [row for row in snapshots if safe_float(row["step"]) <= window]
    prefix = f"w{int(window)}"
    if not selected:
        return {
            f"{prefix}_snapshot_count": 0,
            f"{prefix}_last_step": float("nan"),
        }

    def values(field: str) -> List[float]:
        return [safe_float(row[field]) for row in selected]

    steps = values("step")
    out: Dict[str, Any] = {
        f"{prefix}_snapshot_count": len(selected),
        f"{prefix}_last_step": max(steps),
    }
    scalar_specs = [
        "total_mass",
        "component_count",
        "largest_fraction",
        "total_beta1",
        "total_boundary_edges",
        "total_internal_edges",
        "mean_support_distance",
        "max_support_distance",
        "boundary_to_volume",
        "support_touch_fraction",
        "near_support_fraction",
        "gate_bridge_fraction",
        "spanning_fraction",
        "beta_component_fraction",
        "boundary_heavy_fraction",
        "beta1_per_mass",
        "boundary_per_mass",
        "internal_per_mass",
        "fragmentation_pressure",
        "gate_tension_index",
        "coherent_gate_index",
        "trapped_core_index",
    ]
    for field in scalar_specs:
        vals = values(field)
        out[f"{prefix}_mean_{field}"] = mean_defined(vals)
        out[f"{prefix}_max_{field}"] = max((x for x in vals if math.isfinite(x)), default=float("nan"))
    slope_fields = [
        "total_mass",
        "component_count",
        "largest_fraction",
        "total_beta1",
        "mean_support_distance",
        "boundary_to_volume",
        "gate_bridge_fraction",
        "fragmentation_pressure",
        "gate_tension_index",
        "coherent_gate_index",
        "trapped_core_index",
    ]
    for field in slope_fields:
        out[f"{prefix}_{field}_slope_per_100"] = linear_slope(list(zip(steps, values(field)))) * 100.0
    return out


def static_features(run: Mapping[str, str]) -> Dict[str, Any]:
    keys = [
        "support_size",
        "mean_support_degree",
        "min_support_degree",
        "max_support_degree",
        "support_ball_1",
        "support_ball_2",
        "support_ball_3",
        "shell2_over_shell1",
        "ball3_over_ball1",
        "support_internal_edge_count",
        "support_boundary_to_volume",
        "support_pairwise_mean_distance",
    ]
    return {f"static_{key}": safe_float(run[key]) for key in keys}


def build_run_features() -> List[Dict[str, Any]]:
    run_rows = read_csv(RUNS_CSV)
    comp_rows = read_csv(COMPONENTS_CSV)
    grouped_components: Dict[Tuple[int, int], List[Mapping[str, str]]] = defaultdict(list)
    for row in comp_rows:
        grouped_components[run_key(row)].append(row)

    out: List[Dict[str, Any]] = []
    for run in run_rows:
        key = run_key(run)
        placement = int(safe_float(run["placement"]))
        label = str(run["far_shell_horizon_label"])
        score = safe_float(run[PRIMARY_SCORE])
        snapshots = summarize_run_snapshots(grouped_components[key])
        row: Dict[str, Any] = {
            "target_nodes": int(safe_float(run["target_nodes"])),
            "growth_seed": int(safe_float(run["growth_seed"])),
            "profile_label": str(run["profile_label"]),
            "perturbation": str(run["perturbation"]),
            "placement": placement,
            "seed_delta": int(safe_float(run["seed_delta"])),
            "run_seed": int(safe_float(run["run_seed"])),
            "support_signature": str(run["support_signature"]),
            "far_shell_horizon_label": label,
            "direct_route_entry_label": str(run["direct_route_entry_label"]),
            "decisive_label": decisive_label(label),
            "genealogy_intensity_index": score,
            "analysis_group": str(run.get("analysis_group") or analysis_group(placement, label, score)),
            "first_sustained_high3_step": int(safe_float(run["first_sustained_high3_step"], -1)),
            "strict_pre_entry_max_step": max(STRICT_WINDOWS),
            "source_scope": "no_new_dynamics_v15da_components_v15dd_labels",
        }
        row.update(static_features(run))
        for window in STRICT_WINDOWS:
            row.update(window_summary(snapshots, window))
        out.append(row)
    return out


def metric_catalog() -> List[Tuple[str, str, str, int]]:
    metrics: List[Tuple[str, str, str, int]] = []
    static_specs = [
        ("static_support_ball_1", "higher_is_established"),
        ("static_support_ball_2", "higher_is_established"),
        ("static_support_ball_3", "higher_is_established"),
        ("static_shell2_over_shell1", "higher_is_established"),
        ("static_ball3_over_ball1", "higher_is_established"),
        ("static_mean_support_degree", "higher_is_established"),
        ("static_support_boundary_to_volume", "lower_is_established"),
        ("static_support_pairwise_mean_distance", "higher_is_established"),
        ("static_support_internal_edge_count", "higher_is_established"),
    ]
    for metric, direction in static_specs:
        metrics.append((metric, direction, "static_support_geometry", 0))

    dynamic_specs = [
        ("mean_total_mass", "higher_is_established"),
        ("max_total_mass", "higher_is_established"),
        ("total_mass_slope_per_100", "higher_is_established"),
        ("mean_component_count", "higher_is_established"),
        ("max_component_count", "higher_is_established"),
        ("component_count_slope_per_100", "higher_is_established"),
        ("mean_largest_fraction", "higher_is_established"),
        ("largest_fraction_slope_per_100", "higher_is_established"),
        ("mean_total_beta1", "higher_is_established"),
        ("max_total_beta1", "higher_is_established"),
        ("mean_beta1_per_mass", "higher_is_established"),
        ("mean_total_boundary_edges", "higher_is_established"),
        ("mean_boundary_per_mass", "higher_is_established"),
        ("mean_boundary_to_volume", "higher_is_established"),
        ("boundary_to_volume_slope_per_100", "higher_is_established"),
        ("mean_mean_support_distance", "higher_is_established"),
        ("mean_support_distance_slope_per_100", "higher_is_established"),
        ("max_max_support_distance", "higher_is_established"),
        ("mean_support_touch_fraction", "lower_is_established"),
        ("mean_near_support_fraction", "lower_is_established"),
        ("mean_gate_bridge_fraction", "higher_is_established"),
        ("max_gate_bridge_fraction", "higher_is_established"),
        ("gate_bridge_fraction_slope_per_100", "higher_is_established"),
        ("mean_spanning_fraction", "higher_is_established"),
        ("mean_beta_component_fraction", "higher_is_established"),
        ("mean_boundary_heavy_fraction", "higher_is_established"),
        ("mean_fragmentation_pressure", "lower_is_established"),
        ("fragmentation_pressure_slope_per_100", "lower_is_established"),
        ("mean_gate_tension_index", "higher_is_established"),
        ("gate_tension_index_slope_per_100", "higher_is_established"),
        ("mean_coherent_gate_index", "higher_is_established"),
        ("coherent_gate_index_slope_per_100", "higher_is_established"),
        ("mean_trapped_core_index", "lower_is_established"),
        ("trapped_core_index_slope_per_100", "lower_is_established"),
    ]
    for window in STRICT_WINDOWS:
        for suffix, direction in dynamic_specs:
            metrics.append((f"w{window}_{suffix}", direction, "strict_pre_entry_component_topology", window))

    metrics.append(("genealogy_intensity_index", "higher_is_established", "baseline_downstream_genealogy", -1))
    return metrics


def oriented(row: Mapping[str, Any], metric: str, direction: str) -> float:
    value = safe_float(row.get(metric))
    if direction == "lower_is_established":
        return -value
    return value


def metric_score_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    decisive = [row for row in rows if int(row["decisive_label"]) in (0, 1)]
    established = [row for row in decisive if int(row["decisive_label"]) == 1]
    no_horizon = [row for row in decisive if int(row["decisive_label"]) == 0]
    p1_established = [row for row in rows if str(row["analysis_group"]) == "p1_established"]
    p0_false = [row for row in rows if str(row["analysis_group"]) == "p0_high_score_no_horizon"]
    out: List[Dict[str, Any]] = []
    for metric, direction, family, window in metric_catalog():
        est_values = [oriented(row, metric, direction) for row in established]
        no_values = [oriented(row, metric, direction) for row in no_horizon]
        p1_values = [oriented(row, metric, direction) for row in p1_established]
        p0_values = [oriented(row, metric, direction) for row in p0_false]
        raw_est = [safe_float(row.get(metric)) for row in established]
        raw_no = [safe_float(row.get(metric)) for row in no_horizon]
        raw_p1 = [safe_float(row.get(metric)) for row in p1_established]
        raw_p0 = [safe_float(row.get(metric)) for row in p0_false]
        out.append(
            {
                "metric": metric,
                "metric_family": family,
                "window_step": int(window),
                "direction": direction,
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
            str(row["metric"]),
        ),
    )


def group_summary_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["analysis_group"])].append(row)
    out: List[Dict[str, Any]] = []
    for group, group_rows in sorted(grouped.items()):
        labels = Counter(str(row["far_shell_horizon_label"]) for row in group_rows)
        placements = Counter(f"p{int(safe_float(row['placement']))}" for row in group_rows)
        out.append(
            {
                "analysis_group": group,
                "n_runs": len(group_rows),
                "placements": ";".join(f"{k}:{v}" for k, v in sorted(placements.items())),
                "labels": ";".join(f"{k}:{v}" for k, v in sorted(labels.items())),
                "median_genealogy_intensity": median_defined(safe_float(row["genealogy_intensity_index"]) for row in group_rows),
                "median_static_ball3_over_ball1": median_defined(safe_float(row["static_ball3_over_ball1"]) for row in group_rows),
                "median_static_support_boundary_to_volume": median_defined(safe_float(row["static_support_boundary_to_volume"]) for row in group_rows),
                "median_w96_mass": median_defined(safe_float(row["w96_mean_total_mass"]) for row in group_rows),
                "median_w96_beta1": median_defined(safe_float(row["w96_mean_total_beta1"]) for row in group_rows),
                "median_w96_boundary_per_mass": median_defined(safe_float(row["w96_mean_boundary_per_mass"]) for row in group_rows),
                "median_w96_gate_bridge": median_defined(safe_float(row["w96_mean_gate_bridge_fraction"]) for row in group_rows),
                "median_w96_gate_tension": median_defined(safe_float(row["w96_mean_gate_tension_index"]) for row in group_rows),
                "median_w96_trapped_core": median_defined(safe_float(row["w96_mean_trapped_core_index"]) for row in group_rows),
            }
        )
    return out


def family_summary_rows(metric_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[str, int], List[Mapping[str, Any]]] = defaultdict(list)
    for row in metric_rows:
        if str(row["metric_family"]) == "baseline_downstream_genealogy":
            continue
        grouped[(str(row["metric_family"]), int(row["window_step"]))].append(row)
    out: List[Dict[str, Any]] = []
    for (family, window), rows in sorted(grouped.items()):
        best = max(
            rows,
            key=lambda row: (
                safe_float(row["auc_p1_established_vs_p0_false_positive"], -1.0),
                safe_float(row["auc_established_vs_no"], -1.0),
            ),
        )
        out.append(
            {
                "metric_family": family,
                "window_step": int(window),
                "n_metrics": len(rows),
                "best_metric": best["metric"],
                "best_direction": best["direction"],
                "best_auc_p1_vs_p0_false": best["auc_p1_established_vs_p0_false_positive"],
                "best_auc_established_vs_no": best["auc_established_vs_no"],
                "median_p1_raw": best["median_p1_established_raw"],
                "median_p0_false_raw": best["median_p0_false_positive_raw"],
            }
        )
    return out


def best_dynamic_metric(metric_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [
        row for row in metric_rows
        if str(row["metric_family"]) == "strict_pre_entry_component_topology"
    ]
    return max(
        candidates,
        key=lambda row: (
            safe_float(row["auc_p1_established_vs_p0_false_positive"], -1.0),
            safe_float(row["auc_established_vs_no"], -1.0),
        ),
    )


def diagnosis_rows(
    metric_rows: Sequence[Mapping[str, Any]],
    family_rows: Sequence[Mapping[str, Any]],
    group_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    best = best_dynamic_metric(metric_rows)
    best_auc_p1 = safe_float(best["auc_p1_established_vs_p0_false_positive"])
    best_auc_all = safe_float(best["auc_established_vs_no"])
    intensity = next(row for row in metric_rows if str(row["metric"]) == "genealogy_intensity_index")
    static_best = max(
        (row for row in metric_rows if str(row["metric_family"]) == "static_support_geometry"),
        key=lambda row: safe_float(row["auc_p1_established_vs_p0_false_positive"], -1.0),
    )
    dynamic_best = max(
        (row for row in metric_rows if str(row["metric_family"]) == "strict_pre_entry_component_topology"),
        key=lambda row: safe_float(row["auc_p1_established_vs_p0_false_positive"], -1.0),
    )
    p1 = next((row for row in group_rows if str(row["analysis_group"]) == "p1_established"), None)
    p0 = next((row for row in group_rows if str(row["analysis_group"]) == "p0_high_score_no_horizon"), None)

    if best_auc_p1 >= 0.80 and best_auc_all >= 0.70:
        primary_status = "pre_entry_support_topology_promising"
        next_status = "pre_register_boundary_mass_holdout_with_static_audit"
        next_note = "Frys beste strict dynamiske observabel og test paa friske seeds; statisk supportgeometri maa rapporteres som placement-confound/audit."
    elif best_auc_p1 >= 0.70:
        primary_status = "pre_entry_support_topology_weak"
        next_status = "inspect_cases_before_holdout"
        next_note = "Signalet er ikke sterkt nok til claim; inspiser om det er statisk placement-lekkasje eller en faktisk lokal gate."
    else:
        primary_status = "pre_entry_support_topology_not_found"
        next_status = "seek_different_pre_entry_observable_or_scale_decision"
        next_note = "Ikke press support/topologi-vinduene videre uten ny instrumentering eller et smalere mekanistisk sporsmaal."

    group_note = "Mangler p1/p0 false-positive grupper for direkte medianlesning."
    if p1 and p0:
        group_note = (
            f"p1 median w96 gate_tension={fmt(p1['median_w96_gate_tension'])}, "
            f"trapped_core={fmt(p1['median_w96_trapped_core'])}; "
            f"p0 false-positive median gate_tension={fmt(p0['median_w96_gate_tension'])}, "
            f"trapped_core={fmt(p0['median_w96_trapped_core'])}."
        )

    return [
        {
            "diagnostic_family": "data_scope",
            "status": "no_new_dynamics_v15da_components_v15dd_labels",
            "note": "Analysen leser v15da component trajectories og v15dd run-summary; ingen ny dynamikk.",
        },
        {
            "diagnostic_family": "leakage_guard",
            "status": "strict_windows_le_96_no_route_fields",
            "note": "Kandidatfeatures bruker bare statisk supportgeometri og komponent/topologi ved steps <=96; route-entry/retention brukes ikke som feature.",
        },
        {
            "diagnostic_family": "primary_result",
            "status": primary_status,
            "note": (
                f"Beste strict dynamiske ikke-route metric `{best['metric']}` har "
                f"AUC={fmt(best_auc_p1)} mot p0 false positives og AUC={fmt(best_auc_all)} established-vs-no."
            ),
        },
        {
            "diagnostic_family": "static_confound_check",
            "status": "static_support_geometry_separates_but_is_placement_level",
            "note": (
                f"Beste statiske metric `{static_best['metric']}` har AUC="
                f"{fmt(static_best['auc_p1_established_vs_p0_false_positive'])} mot p0 false positives, "
                "men dette er statisk support/placement-informasjon og maa ikke alene tolkes som dynamisk selector."
            ),
        },
        {
            "diagnostic_family": "dynamic_check",
            "status": "best_strict_component_topology",
            "note": (
                f"Beste strict dynamiske metric `{dynamic_best['metric']}` har AUC="
                f"{fmt(dynamic_best['auc_p1_established_vs_p0_false_positive'])} mot p0 false positives."
            ),
        },
        {
            "diagnostic_family": "group_reading",
            "status": "p1_vs_p0_false_positive_support_topology",
            "note": group_note,
        },
        {
            "diagnostic_family": "baseline_check",
            "status": "genealogy_intensity_not_primary_selector",
            "note": (
                f"Baseline genealogy-intensity har AUC="
                f"{fmt(intensity['auc_p1_established_vs_p0_false_positive'])} mot p0 false positives."
            ),
        },
        {
            "diagnostic_family": "next_step",
            "status": next_status,
            "note": next_note,
        },
    ]


def top_rows(rows: Sequence[Mapping[str, Any]], n: int = 20) -> List[Mapping[str, Any]]:
    return list(rows[:n])


def build_report(
    group_rows: Sequence[Mapping[str, Any]],
    family_rows: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15df: strict pre-entry support/topology synthesis")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden bruker ingen ny dynamikk.")
    lines.append("Den leser `v15da` component trajectories og `v15dd` run-summary, men bruker downstream horizon/route-labels bare som evalueringsfasit.")
    lines.append("Kandidatfeatures er ikke-route: statisk supportgeometri og komponent/topologi/support-distance i strict vinduer `<=32`, `<=64`, `<=96`.")
    lines.append("Primarresultatet bruker strict dynamisk komponent/topologi; statisk supportgeometri rapporteres som confound-/heuristikk-audit.")
    lines.append("")
    lines.append("## Family summary")
    lines.append("")
    lines.append("| family | window | n metrics | best metric | direction | AUC p1/p0 false | AUC est/no | median p1 | median p0 false |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in family_rows:
        lines.append(
            f"| {row['metric_family']} | {int(row['window_step'])} | {int(row['n_metrics'])} | {row['best_metric']} | {row['best_direction']} | {fmt(row['best_auc_p1_vs_p0_false'])} | {fmt(row['best_auc_established_vs_no'])} | {fmt(row['median_p1_raw'])} | {fmt(row['median_p0_false_raw'])} |"
        )
    lines.append("")
    lines.append("## Group summary")
    lines.append("")
    lines.append("| group | n | placements | labels | intensity | static b3/b1 | static b/v | w96 mass | w96 beta1 | w96 boundary/mass | w96 bridge | w96 tension | w96 trapped |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in group_rows:
        lines.append(
            f"| {row['analysis_group']} | {int(row['n_runs'])} | {row['placements']} | {row['labels']} | {fmt(row['median_genealogy_intensity'])} | {fmt(row['median_static_ball3_over_ball1'])} | {fmt(row['median_static_support_boundary_to_volume'])} | {fmt(row['median_w96_mass'])} | {fmt(row['median_w96_beta1'])} | {fmt(row['median_w96_boundary_per_mass'])} | {fmt(row['median_w96_gate_bridge'])} | {fmt(row['median_w96_gate_tension'])} | {fmt(row['median_w96_trapped_core'])} |"
        )
    lines.append("")
    lines.append("## Top metrics")
    lines.append("")
    lines.append("| metric | family | window | direction | AUC est/no | AUC p1/p0 false | median p1 | median p0 false | p1-p0 false |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in top_rows(metric_rows, 24):
        lines.append(
            f"| {row['metric']} | {row['metric_family']} | {int(row['window_step'])} | {row['direction']} | {fmt(row['auc_established_vs_no'])} | {fmt(row['auc_p1_established_vs_p0_false_positive'])} | {fmt(row['median_p1_established_raw'])} | {fmt(row['median_p0_false_positive_raw'])} | {fmt(row['median_p1_minus_p0_false_raw'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en observabelsyntese paa eksisterende data, ikke en ny dynamisk validering.")
    lines.append("- Route-entry/retention-felt er eksplisitt utelatt fra kandidatfeatures.")
    lines.append("- Et positivt funn her er bare en kandidat for pre-registrert holdout, ikke en invariant eller en universell geometri.")
    lines.append("- Et negativt funn betyr at strict pre-entry support/topologi ikke forklarer p1-vs-p0 false-positive-skillet i dagens data.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15df", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke bruk route-entry/retention som pre-entry selector.")
    lines.append("- Ikke refit genealogy-intensity til denne kontrasten.")
    lines.append("- Hvis beste ikke-route feature er sterk nok, frys den foer eventuell frisk holdout.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15df",
            "",
            "Denne runden spurte om vi kan se noe nyttig foer fjernhale-oppfoerselen starter.",
            "",
            "I stedet for aa se paa selve ruten utover, saa den paa lokal form: hvor skaden ligger rundt startpunktet, hvor oppstykket den er, og enkel lokal topologi.",
            "",
            f"- Hovedlesning: `{diag['primary_result']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Kort sagt: dette er en test av om formen paa de tidlige lokale sporene sier noe foer systemet faktisk begynner aa gaa langt utover.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15df strict pre-entry support/topology synthesis.")
    p.add_argument("--out-run-features-csv", default=str(DOC / "v15df_pre_entry_support_topology_run_features.csv"))
    p.add_argument("--out-family-csv", default=str(DOC / "v15df_pre_entry_support_topology_family_summary.csv"))
    p.add_argument("--out-group-csv", default=str(DOC / "v15df_pre_entry_support_topology_group_summary.csv"))
    p.add_argument("--out-metrics-csv", default=str(DOC / "v15df_pre_entry_support_topology_metric_scores.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15df_pre_entry_support_topology_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15df_pre_entry_support_topology_synthesis.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15df_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15df.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_rows = build_run_features()
    metric_rows = metric_score_rows(run_rows)
    group_rows = group_summary_rows(run_rows)
    family_rows = family_summary_rows(metric_rows)
    diagnosis = diagnosis_rows(metric_rows, family_rows, group_rows)

    write_csv(args.out_run_features_csv, run_rows)
    write_csv(args.out_family_csv, family_rows)
    write_csv(args.out_group_csv, group_rows)
    write_csv(args.out_metrics_csv, metric_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(group_rows, family_rows, metric_rows, diagnosis),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")
    print(f"wrote {args.out_summary_md}")
    print(f"wrote {args.out_diagnosis_csv}")


if __name__ == "__main__":
    main()
