#!/usr/bin/env python3
"""v0.15dc censored pre-horizon routing precursor lab.

v15db showed that downstream routing cleanly separates p0 false positives
from p1 established far-shell horizons, but that is not a legitimate early
selector. This no-new-dynamics round reuses v15da component trajectories and
censors component observables at first high entry when first_high_step exists.

Goal:
- test whether a stricter pre-high / pre-horizon routing precursor exists
- keep downstream horizon fields as evaluation only
- do not refit the v15cz genealogy-intensity score
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15db_routing_phase_observable_synthesis as v15db


DOC = Path("Documentation")
RUNS_CSV = DOC / "v15da_frozen_intensity_placement_contrast_runs.csv"
COMPONENTS_CSV = DOC / "v15da_frozen_intensity_placement_contrast_component_trajectories.csv"

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


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    v15.write_csv(path, list(rows))


def median_defined(values: Iterable[float]) -> float:
    vals = sorted(x for x in values if math.isfinite(x))
    if not vals:
        return float("nan")
    mid = len(vals) // 2
    if len(vals) % 2:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2.0


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def run_key(row: Mapping[str, Any]) -> Tuple[int, int]:
    return int(safe_float(row["placement"])), int(safe_float(row["seed_delta"]))


def decisiveness(label: str) -> int:
    if label == "established_far_shell_horizon":
        return 1
    if label == "no_far_shell_horizon":
        return 0
    return -1


def pairwise_auc(pos_values: Sequence[float], neg_values: Sequence[float]) -> float:
    return v15db.pairwise_auc(pos_values, neg_values)


def linear_slope(points: Sequence[Tuple[float, float]]) -> float:
    xs: List[float] = []
    ys: List[float] = []
    for x, y in points:
        if math.isfinite(x) and math.isfinite(y):
            xs.append(x)
            ys.append(y)
    if len(xs) < 2:
        return float("nan")
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    denom = sum((x - xbar) ** 2 for x in xs)
    if denom <= 0:
        return float("nan")
    return sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / denom


def snapshot_rows(rows: Sequence[Mapping[str, str]]) -> Dict[int, List[Mapping[str, str]]]:
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


def mass_fraction(rows: Sequence[Mapping[str, str]], field: str, threshold: float) -> float:
    total = 0.0
    selected = 0.0
    for row in rows:
        weight = safe_float(row["size_nodes"])
        value = safe_float(row[field])
        if not math.isfinite(weight) or weight <= 0:
            continue
        total += weight
        if math.isfinite(value) and value >= threshold:
            selected += weight
    return selected / total if total else float("nan")


def active_run_length(flags: Sequence[bool]) -> int:
    best = 0
    cur = 0
    for flag in flags:
        if flag:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


def summarize_snapshots(rows: Sequence[Mapping[str, str]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for idx, snap in sorted(snapshot_rows(rows).items()):
        step = safe_float(snap[0]["step"])
        total_mass = safe_float(snap[0]["total_defect_mass"])
        component_count = safe_float(snap[0]["component_count"])
        largest_fraction = safe_float(snap[0]["largest_component_fraction"])
        mean_distance = mass_weighted(snap, "mean_support_distance")
        max_distance = max((safe_float(row["max_support_distance"]) for row in snap), default=float("nan"))
        far6 = mass_fraction(snap, "max_support_distance", 6.0)
        far8 = mass_fraction(snap, "max_support_distance", 8.0)
        far10 = mass_fraction(snap, "max_support_distance", 10.0)
        route_active = (
            (math.isfinite(far8) and far8 >= 0.20)
            or (math.isfinite(mean_distance) and mean_distance >= 4.0)
        )
        out.append(
            {
                "snapshot_index": idx,
                "step": step,
                "total_mass": total_mass,
                "component_count": component_count,
                "largest_fraction": largest_fraction,
                "mean_distance": mean_distance,
                "max_distance": max_distance,
                "far6_mass_fraction": far6,
                "far8_mass_fraction": far8,
                "far10_mass_fraction": far10,
                "route_active": route_active,
            }
        )
    return out


def censor_snapshots(snapshots: Sequence[Mapping[str, Any]], run: Mapping[str, str]) -> Tuple[List[Mapping[str, Any]], str, float]:
    early_limit = safe_float(run["early_step_limit"])
    first_high = safe_float(run["first_high_step"])
    if math.isfinite(first_high):
        cutoff = min(early_limit, max(0.0, first_high - safe_float(run["log_every"], 8.0)))
        reason = "censored_before_first_high"
    else:
        cutoff = early_limit
        reason = "early_limit_no_first_high"
    return [snap for snap in snapshots if safe_float(snap["step"]) <= cutoff], reason, cutoff


def window_features(snapshots: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    if not snapshots:
        return {
            "pre_snapshot_count": 0,
            "pre_last_step": float("nan"),
            "pre_mean_distance": float("nan"),
            "pre_max_distance": float("nan"),
            "pre_last_mean_distance": float("nan"),
            "pre_last_far8_fraction": float("nan"),
            "pre_mean_far6_fraction": float("nan"),
            "pre_mean_far8_fraction": float("nan"),
            "pre_mean_far10_fraction": float("nan"),
            "pre_peak_far8_fraction": float("nan"),
            "pre_peak_far10_fraction": float("nan"),
            "pre_route_active_rate": float("nan"),
            "pre_longest_route_active_run": 0,
            "pre_distance_slope_per_100": float("nan"),
            "pre_far8_slope_per_100": float("nan"),
            "pre_route_coherence_index": float("nan"),
            "pre_mass_distance_flux": float("nan"),
            "pre_late_route_gain": float("nan"),
        }
    mean_dist = [safe_float(snap["mean_distance"]) for snap in snapshots]
    far6 = [safe_float(snap["far6_mass_fraction"]) for snap in snapshots]
    far8 = [safe_float(snap["far8_mass_fraction"]) for snap in snapshots]
    far10 = [safe_float(snap["far10_mass_fraction"]) for snap in snapshots]
    masses = [safe_float(snap["total_mass"]) for snap in snapshots]
    steps = [safe_float(snap["step"]) for snap in snapshots]
    flags = [bool(snap["route_active"]) for snap in snapshots]
    half = max(1, len(snapshots) // 2)
    early_far8 = mean_defined(far8[:half])
    late_far8 = mean_defined(far8[half:])
    distance_slope = linear_slope(list(zip(steps, mean_dist))) * 100.0
    far8_slope = linear_slope(list(zip(steps, far8))) * 100.0
    route_active_rate = sum(1 for flag in flags if flag) / len(flags)
    longest_active = active_run_length(flags)
    coherence = (
        0.35 * clamp01(mean_defined(far8))
        + 0.25 * clamp01(max((x for x in far8 if math.isfinite(x)), default=0.0))
        + 0.20 * clamp01(route_active_rate)
        + 0.10 * clamp01(longest_active / max(1, len(flags)))
        + 0.10 * clamp01(mean_defined(mean_dist) / 8.0)
    )
    flux = mean_defined(
        m * d
        for m, d in zip(masses, mean_dist)
        if math.isfinite(m) and math.isfinite(d)
    )
    return {
        "pre_snapshot_count": len(snapshots),
        "pre_last_step": max(steps),
        "pre_mean_distance": mean_defined(mean_dist),
        "pre_max_distance": max((safe_float(snap["max_distance"]) for snap in snapshots), default=float("nan")),
        "pre_last_mean_distance": mean_dist[-1],
        "pre_last_far8_fraction": far8[-1],
        "pre_mean_far6_fraction": mean_defined(far6),
        "pre_mean_far8_fraction": mean_defined(far8),
        "pre_mean_far10_fraction": mean_defined(far10),
        "pre_peak_far8_fraction": max((x for x in far8 if math.isfinite(x)), default=float("nan")),
        "pre_peak_far10_fraction": max((x for x in far10 if math.isfinite(x)), default=float("nan")),
        "pre_route_active_rate": route_active_rate,
        "pre_longest_route_active_run": longest_active,
        "pre_distance_slope_per_100": distance_slope,
        "pre_far8_slope_per_100": far8_slope,
        "pre_route_coherence_index": coherence,
        "pre_mass_distance_flux": flux,
        "pre_late_route_gain": late_far8 - early_far8,
    }


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


def build_run_features() -> List[Dict[str, Any]]:
    run_rows = read_csv(RUNS_CSV)
    components = read_csv(COMPONENTS_CSV)
    grouped_components: Dict[Tuple[int, int], List[Mapping[str, str]]] = defaultdict(list)
    for row in components:
        grouped_components[run_key(row)].append(row)

    out: List[Dict[str, Any]] = []
    for run in run_rows:
        key = run_key(run)
        snapshots = summarize_snapshots(grouped_components[key])
        censored, censor_reason, censor_cutoff_step = censor_snapshots(snapshots, run)
        features = window_features(censored)
        placement = int(safe_float(run["placement"]))
        label = str(run["far_shell_horizon_label"])
        score = safe_float(run[PRIMARY_SCORE])
        out.append(
            {
                "target_nodes": run["target_nodes"],
                "growth_seed": run["growth_seed"],
                "profile_label": run["profile_label"],
                "placement": placement,
                "seed_delta": int(safe_float(run["seed_delta"])),
                "run_seed": run["run_seed"],
                "support_signature": run["support_signature"],
                "far_shell_horizon_label": label,
                "decisive_label": decisiveness(label),
                "genealogy_intensity_index": score,
                "first_high_step": run["first_high_step"],
                "early_step_limit": run["early_step_limit"],
                "censor_reason": censor_reason,
                "censor_cutoff_step": censor_cutoff_step,
                "tail_mean_far_shell_share": run["tail_mean_far_shell_share"],
                "high_retention_rate": run["high_retention_rate"],
                "last12_high_rate": run["last12_high_rate"],
                "high_horizon_span": run["high_horizon_span"],
                "analysis_group": analysis_group(placement, label, score),
                "is_high_score_no_horizon": int(label == "no_far_shell_horizon" and score >= FALSE_POSITIVE_SCORE_FLOOR),
                "is_p0_high_score_no_horizon": int(
                    placement == 0 and label == "no_far_shell_horizon" and score >= FALSE_POSITIVE_SCORE_FLOOR
                ),
                **features,
            }
        )
    return out


METRICS: Tuple[Tuple[str, str], ...] = (
    ("pre_route_coherence_index", "higher_is_established"),
    ("pre_mean_far8_fraction", "higher_is_established"),
    ("pre_peak_far8_fraction", "higher_is_established"),
    ("pre_mean_far10_fraction", "higher_is_established"),
    ("pre_peak_far10_fraction", "higher_is_established"),
    ("pre_route_active_rate", "higher_is_established"),
    ("pre_longest_route_active_run", "higher_is_established"),
    ("pre_mean_distance", "higher_is_established"),
    ("pre_last_mean_distance", "higher_is_established"),
    ("pre_distance_slope_per_100", "higher_is_established"),
    ("pre_far8_slope_per_100", "higher_is_established"),
    ("pre_mass_distance_flux", "higher_is_established"),
    ("pre_late_route_gain", "higher_is_established"),
    ("genealogy_intensity_index", "higher_is_established"),
)


def oriented(row: Mapping[str, Any], metric: str, direction: str) -> float:
    value = safe_float(row[metric])
    if direction == "lower_is_established":
        return -value
    return value


def metric_score_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    decisive = [row for row in rows if int(row["decisive_label"]) in (0, 1)]
    established = [row for row in decisive if int(row["decisive_label"]) == 1]
    no_horizon = [row for row in decisive if int(row["decisive_label"]) == 0]
    p1_established = [row for row in rows if row["analysis_group"] == "p1_established"]
    p0_false = [row for row in rows if row["analysis_group"] == "p0_high_score_no_horizon"]
    out: List[Dict[str, Any]] = []
    for metric, direction in METRICS:
        est_values = [oriented(row, metric, direction) for row in established]
        no_values = [oriented(row, metric, direction) for row in no_horizon]
        p1_values = [oriented(row, metric, direction) for row in p1_established]
        p0_values = [oriented(row, metric, direction) for row in p0_false]
        raw_p1 = [safe_float(row[metric]) for row in p1_established]
        raw_p0 = [safe_float(row[metric]) for row in p0_false]
        raw_est = [safe_float(row[metric]) for row in established]
        raw_no = [safe_float(row[metric]) for row in no_horizon]
        out.append(
            {
                "metric": metric,
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
                "median_pre_route_coherence": median_defined(safe_float(row["pre_route_coherence_index"]) for row in group_rows),
                "median_pre_mean_far8": median_defined(safe_float(row["pre_mean_far8_fraction"]) for row in group_rows),
                "median_pre_peak_far8": median_defined(safe_float(row["pre_peak_far8_fraction"]) for row in group_rows),
                "median_pre_route_active_rate": median_defined(safe_float(row["pre_route_active_rate"]) for row in group_rows),
                "median_pre_mean_distance": median_defined(safe_float(row["pre_mean_distance"]) for row in group_rows),
                "median_pre_snapshot_count": median_defined(safe_float(row["pre_snapshot_count"]) for row in group_rows),
            }
        )
    return out


def false_positive_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        if int(row["is_high_score_no_horizon"]) != 1:
            continue
        out.append(
            {
                "placement": f"p{int(safe_float(row['placement']))}",
                "seed_delta": int(safe_float(row["seed_delta"])),
                "genealogy_intensity_index": row["genealogy_intensity_index"],
                "pre_route_coherence_index": row["pre_route_coherence_index"],
                "pre_mean_far8_fraction": row["pre_mean_far8_fraction"],
                "pre_peak_far8_fraction": row["pre_peak_far8_fraction"],
                "pre_route_active_rate": row["pre_route_active_rate"],
                "pre_mean_distance": row["pre_mean_distance"],
                "censor_reason": row["censor_reason"],
                "censor_cutoff_step": row["censor_cutoff_step"],
                "first_high_step": row["first_high_step"],
                "high_horizon_span": row["high_horizon_span"],
            }
        )
    return sorted(out, key=lambda row: (-safe_float(row["genealogy_intensity_index"]), row["placement"], row["seed_delta"]))


def diagnosis_rows(metric_rows: Sequence[Mapping[str, Any]], group_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    best = max(
        metric_rows,
        key=lambda row: safe_float(row["auc_p1_established_vs_p0_false_positive"], -1.0),
    )
    best_auc_p1_p0 = safe_float(best["auc_p1_established_vs_p0_false_positive"])
    best_auc_est_no = safe_float(best["auc_established_vs_no"])
    coherence = next(row for row in metric_rows if row["metric"] == "pre_route_coherence_index")
    intensity = next(row for row in metric_rows if row["metric"] == "genealogy_intensity_index")
    p1 = next((row for row in group_rows if row["analysis_group"] == "p1_established"), None)
    p0 = next((row for row in group_rows if row["analysis_group"] == "p0_high_score_no_horizon"), None)

    if best["metric"] != "genealogy_intensity_index" and best_auc_p1_p0 >= 0.80 and best_auc_est_no >= 0.75:
        status = "pre_horizon_route_precursor_promising"
        note = (
            f"Beste censored pre-horizon observabel `{best['metric']}` har AUC={fmt(best_auc_p1_p0)} "
            f"for p1 established vs p0 false positives og AUC={fmt(best_auc_est_no)} for established vs no-horizon."
        )
        next_status = "pre_register_censored_route_precursor"
        next_note = "Kan testes paa friske seeds hvis cutoff-regelen fryses foer kjøring."
    elif best_auc_p1_p0 >= 0.70:
        status = "pre_horizon_route_precursor_weak"
        note = (
            f"Beste censored pre-horizon observabel `{best['metric']}` er bare delvis separerende "
            f"(p1-vs-p0-false AUC={fmt(best_auc_p1_p0)}, established-vs-no AUC={fmt(best_auc_est_no)})."
        )
        next_status = "instrument_snapshot_route_entry_directly"
        next_note = "Treng mer direkte per-snapshot route-entry/retention logging; eksisterende sensurerte komponentfelt er ikke nok."
    else:
        status = "pre_horizon_route_precursor_not_found"
        note = (
            f"Ingen sensurert pre-horizon observabel skiller godt nok; best `{best['metric']}` har "
            f"p1-vs-p0-false AUC={fmt(best_auc_p1_p0)}."
        )
        next_status = "stop_using_pre_horizon_component_proxy"
        next_note = "Ikke press eksisterende komponentproxyer videre; ny instrumentering maa logge route-entry direkte."

    group_note = "Mangler p1/p0 grupper for direkte medianlesning."
    if p1 and p0:
        group_note = (
            f"p1 established median coherence={fmt(p1['median_pre_route_coherence'])} og pre_far8={fmt(p1['median_pre_mean_far8'])}; "
            f"p0 false positives median coherence={fmt(p0['median_pre_route_coherence'])} og pre_far8={fmt(p0['median_pre_mean_far8'])}."
        )

    return [
        {
            "diagnostic_family": "data_scope",
            "status": "no_new_dynamics_v15da_only",
            "note": "Analysen leser bare v15da runs og component trajectories.",
        },
        {
            "diagnostic_family": "censoring_rule",
            "status": "pre_first_high_or_early_limit",
            "note": "Established-runs sensureres foer first_high_step; no-high-runs bruker early_step_limit.",
        },
        {
            "diagnostic_family": "primary_result",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "group_reading",
            "status": "p1_vs_p0_false_positive_pre_horizon",
            "note": group_note,
        },
        {
            "diagnostic_family": "baseline_check",
            "status": "genealogy_intensity_still_not_selector",
            "note": (
                f"Baseline genealogy-intensity har p1-vs-p0-false AUC={fmt(intensity['auc_p1_established_vs_p0_false_positive'])}; "
                f"pre_route_coherence har AUC={fmt(coherence['auc_p1_established_vs_p0_false_positive'])}."
            ),
        },
        {
            "diagnostic_family": "next_step",
            "status": next_status,
            "note": next_note,
        },
    ]


def build_report(
    group_rows: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
    false_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dc: censored pre-horizon routing precursor")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden bruker ingen ny dynamikk. Den leser v15da-komponentbaner og sensurerer pre-horizon observabler foer `first_high_step` der high-entry finnes.")
    lines.append("Maalet er aa teste om routing-forskjellen som v15db fant downstream allerede finnes i strengere pre-high komponentdata.")
    lines.append("")
    lines.append("## Group summary")
    lines.append("")
    lines.append("| group | n | placements | labels | intensity | coherence | mean far8 | peak far8 | active | distance | snapshots |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in group_rows:
        lines.append(
            f"| {row['analysis_group']} | {int(row['n_runs'])} | {row['placements']} | {row['labels']} | {fmt(row['median_genealogy_intensity'])} | {fmt(row['median_pre_route_coherence'])} | {fmt(row['median_pre_mean_far8'])} | {fmt(row['median_pre_peak_far8'])} | {fmt(row['median_pre_route_active_rate'])} | {fmt(row['median_pre_mean_distance'])} | {fmt(row['median_pre_snapshot_count'], 1)} |"
        )
    lines.append("")
    lines.append("## Metric ranking")
    lines.append("")
    lines.append("| metric | AUC est/no | AUC p1/p0 false | median p1 | median p0 false | p1-p0 false |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in metric_rows:
        lines.append(
            f"| {row['metric']} | {fmt(row['auc_established_vs_no'])} | {fmt(row['auc_p1_established_vs_p0_false_positive'])} | {fmt(row['median_p1_established_raw'])} | {fmt(row['median_p0_false_positive_raw'])} | {fmt(row['median_p1_minus_p0_false_raw'])} |"
        )
    lines.append("")
    lines.append("## High-score no-horizon cases")
    lines.append("")
    lines.append("| placement | seed | intensity | coherence | mean far8 | peak far8 | active | distance | cutoff | first high | horizon |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in false_rows:
        lines.append(
            f"| {row['placement']} | {int(row['seed_delta'])} | {fmt(row['genealogy_intensity_index'])} | {fmt(row['pre_route_coherence_index'])} | {fmt(row['pre_mean_far8_fraction'])} | {fmt(row['pre_peak_far8_fraction'])} | {fmt(row['pre_route_active_rate'])} | {fmt(row['pre_mean_distance'])} | {fmt(row['censor_cutoff_step'], 1)} | {row['first_high_step']} | {fmt(row['high_horizon_span'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en observabelsyntese paa eksisterende v15da-data, ikke en ny dynamisk validering.")
    lines.append("- Sensureringen gjor testen strengere enn v15db: downstream tail/retention er bare evaluering, ikke feature.")
    lines.append("- Et svakt eller negativt resultat betyr at eksisterende komponentproxyer ikke er nok som pre-horizon selector.")
    lines.append("- Ikke oppgrader til partikler, Lorentz-likhet, invariant, entanglement eller universell geometri.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15dc", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke bruk v15db downstream route-score som selector.")
    lines.append("- Hvis v15dc bare gir svakt signal, neste steg er direkte snapshot-instrumentering av route-entry/retention.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15dc",
            "",
            "Denne runden testet om vi kan se tegn til en langvarig fjernhale foer selve fjernhale-oppfoerselen er i gang.",
            "",
            f"- Hovedlesning: `{diag['primary_result']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Kort sagt: dette skiller mellom en ekte tidlig pekepinn og en forklaring vi bare ser etterpaa.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15dc censored pre-horizon routing precursor lab.")
    p.add_argument("--out-run-features-csv", default=str(DOC / "v15dc_pre_horizon_run_features.csv"))
    p.add_argument("--out-group-csv", default=str(DOC / "v15dc_pre_horizon_group_summary.csv"))
    p.add_argument("--out-metrics-csv", default=str(DOC / "v15dc_pre_horizon_metric_scores.csv"))
    p.add_argument("--out-false-csv", default=str(DOC / "v15dc_pre_horizon_false_positive_cases.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15dc_pre_horizon_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15dc_pre_horizon_routing_precursor.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15dc_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15dc.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_features = build_run_features()
    group_rows = group_summary_rows(run_features)
    metric_rows = metric_score_rows(run_features)
    false_rows = false_positive_rows(run_features)
    diagnosis = diagnosis_rows(metric_rows, group_rows)

    write_csv(args.out_run_features_csv, run_features)
    write_csv(args.out_group_csv, group_rows)
    write_csv(args.out_metrics_csv, metric_rows)
    write_csv(args.out_false_csv, false_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(build_report(group_rows, metric_rows, false_rows, diagnosis), encoding="utf-8")
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
