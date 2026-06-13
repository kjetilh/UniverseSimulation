#!/usr/bin/env python3
"""v0.15db routing/phase observable synthesis.

v15da showed that the frozen genealogy-intensity score is not a selector:
p0 can score high while failing to establish far-shell horizon. This no-new-
dynamics round tests whether existing timing/routing observables separate
those p0 false positives from p1 established runs.

Discipline:
- reads v15da only
- does not refit v15cz score
- separates early/pre-entry features from downstream routing/retention fields
- does not upgrade to particle, invariant, Lorentz, or spacetime claims
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
RUNS_CSV = DOC / "v15da_frozen_intensity_placement_contrast_runs.csv"
COMPONENTS_CSV = DOC / "v15da_frozen_intensity_placement_contrast_component_trajectories.csv"

PRIMARY_SCORE = "genealogy_intensity_index"
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


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    v15.write_csv(path, list(rows))


def decisive_label(label: str) -> int:
    if label == "established_far_shell_horizon":
        return 1
    if label == "no_far_shell_horizon":
        return 0
    return -1


def run_key(row: Mapping[str, Any]) -> Tuple[int, int]:
    return int(safe_float(row["placement"])), int(safe_float(row["seed_delta"]))


def weighted_mean(pairs: Iterable[Tuple[float, float]]) -> float:
    total_weight = 0.0
    total = 0.0
    for value, weight in pairs:
        if not math.isfinite(value) or not math.isfinite(weight) or weight <= 0:
            continue
        total += value * weight
        total_weight += weight
    return total / total_weight if total_weight else float("nan")


def mass_fraction(rows: Sequence[Mapping[str, str]], *, distance_field: str, threshold: float) -> float:
    total = 0.0
    selected = 0.0
    for row in rows:
        size = safe_float(row["size_nodes"])
        dist = safe_float(row[distance_field])
        if not math.isfinite(size) or size <= 0:
            continue
        total += size
        if math.isfinite(dist) and dist >= threshold:
            selected += size
    return selected / total if total else float("nan")


def component_feature_rows(component_rows: Sequence[Mapping[str, str]], runs_by_key: Mapping[Tuple[int, int], Mapping[str, Any]]) -> Dict[Tuple[int, int], Dict[str, Any]]:
    grouped: Dict[Tuple[int, int], List[Mapping[str, str]]] = defaultdict(list)
    for row in component_rows:
        grouped[run_key(row)].append(row)

    out: Dict[Tuple[int, int], Dict[str, Any]] = {}
    for key, rows in grouped.items():
        run = runs_by_key[key]
        early_limit = safe_float(run["early_step_limit"])
        max_step = max(safe_float(row["step"]) for row in rows)
        tail_start = max_step * 0.75
        early = [row for row in rows if safe_float(row["step"]) <= early_limit]
        tail = [row for row in rows if safe_float(row["step"]) >= tail_start]
        all_rows = rows
        out[key] = {
            "component_early_weighted_mean_distance": weighted_mean(
                (safe_float(row["mean_support_distance"]), safe_float(row["size_nodes"])) for row in early
            ),
            "component_early_max_distance": max((safe_float(row["max_support_distance"]) for row in early), default=float("nan")),
            "component_early_far8_mass_fraction": mass_fraction(early, distance_field="max_support_distance", threshold=8.0),
            "component_early_far10_mass_fraction": mass_fraction(early, distance_field="max_support_distance", threshold=10.0),
            "component_tail_weighted_mean_distance": weighted_mean(
                (safe_float(row["mean_support_distance"]), safe_float(row["size_nodes"])) for row in tail
            ),
            "component_tail_max_distance": max((safe_float(row["max_support_distance"]) for row in tail), default=float("nan")),
            "component_tail_far8_mass_fraction": mass_fraction(tail, distance_field="max_support_distance", threshold=8.0),
            "component_tail_far10_mass_fraction": mass_fraction(tail, distance_field="max_support_distance", threshold=10.0),
            "component_all_weighted_mean_distance": weighted_mean(
                (safe_float(row["mean_support_distance"]), safe_float(row["size_nodes"])) for row in all_rows
            ),
            "component_all_far8_mass_fraction": mass_fraction(all_rows, distance_field="max_support_distance", threshold=8.0),
        }
        out[key]["component_distance_gain_tail_minus_early"] = (
            safe_float(out[key]["component_tail_weighted_mean_distance"])
            - safe_float(out[key]["component_early_weighted_mean_distance"])
        )
    return out


def enriched_run_rows() -> List[Dict[str, Any]]:
    run_rows = read_csv(RUNS_CSV)
    runs_by_key = {run_key(row): row for row in run_rows}
    comp_features = component_feature_rows(read_csv(COMPONENTS_CSV), runs_by_key)
    rows: List[Dict[str, Any]] = []
    for row in run_rows:
        key = run_key(row)
        placement = int(safe_float(row["placement"]))
        label = str(row["far_shell_horizon_label"])
        score = safe_float(row[PRIMARY_SCORE])
        first_high = safe_float(row["first_high_step"])
        step_budget = safe_float(row["step_budget"])
        phase_entry_index = (
            0.35 * clamp01(safe_float(row["early_high_band_rate"]))
            + 0.25 * clamp01(safe_float(row["early_mid_or_high_rate"]))
            + 0.25 * clamp01(safe_float(row["max_early_outer_share"]))
            + 0.15 * clamp01(safe_float(row["mean_early_weighted_distance"]) / 8.0)
        )
        tail_route_index = (
            0.50 * clamp01(safe_float(row["tail_mean_far_shell_share"]))
            + 0.25 * clamp01(safe_float(row["high_retention_rate"]))
            + 0.25 * clamp01(safe_float(row["last12_high_rate"]))
        )
        entry_timing_index = 0.0
        if math.isfinite(first_high) and math.isfinite(step_budget) and step_budget > 0:
            entry_timing_index = clamp01(1.0 - first_high / step_budget)
        component_tail_route_index = (
            0.50 * clamp01(safe_float(comp_features[key]["component_tail_far8_mass_fraction"]))
            + 0.25 * clamp01(safe_float(comp_features[key]["component_tail_far10_mass_fraction"]))
            + 0.25 * clamp01(safe_float(comp_features[key]["component_tail_weighted_mean_distance"]) / 12.0)
        )
        route_efficiency_per_intensity = safe_float(row["tail_mean_far_shell_share"]) / (score + 1e-9)
        horizon_efficiency_per_churn = safe_float(row["high_horizon_span"]) / (safe_float(row["churn_event_count"]) + 1.0)
        intensity_without_route_pressure = score - tail_route_index
        phase_intensity_gap = score - phase_entry_index
        is_false_positive = (
            label == "no_far_shell_horizon"
            and score >= FALSE_POSITIVE_SCORE_FLOOR
        )
        is_p0_false_positive = is_false_positive and placement == 0
        rows.append(
            {
                **dict(row),
                **comp_features[key],
                "decisive_label": decisive_label(label),
                "phase_entry_index": phase_entry_index,
                "tail_route_index": tail_route_index,
                "entry_timing_index": entry_timing_index,
                "component_tail_route_index": component_tail_route_index,
                "route_efficiency_per_intensity": route_efficiency_per_intensity,
                "horizon_efficiency_per_churn": horizon_efficiency_per_churn,
                "intensity_without_route_pressure": intensity_without_route_pressure,
                "phase_intensity_gap": phase_intensity_gap,
                "is_high_score_no_horizon": int(is_false_positive),
                "is_p0_high_score_no_horizon": int(is_p0_false_positive),
                "analysis_group": analysis_group(placement, label, score),
            }
        )
    return rows


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
    ("genealogy_intensity_index", "higher_is_established", "baseline_failed_selector"),
    ("phase_entry_index", "higher_is_established", "early_pre_entry"),
    ("component_early_weighted_mean_distance", "higher_is_established", "early_pre_entry"),
    ("component_early_far8_mass_fraction", "higher_is_established", "early_pre_entry"),
    ("component_early_far10_mass_fraction", "higher_is_established", "early_pre_entry"),
    ("tail_route_index", "higher_is_established", "downstream_routing"),
    ("entry_timing_index", "higher_is_established", "downstream_routing"),
    ("component_tail_route_index", "higher_is_established", "downstream_routing"),
    ("component_tail_far8_mass_fraction", "higher_is_established", "downstream_routing"),
    ("route_efficiency_per_intensity", "higher_is_established", "downstream_routing"),
    ("horizon_efficiency_per_churn", "higher_is_established", "downstream_outcome"),
    ("intensity_without_route_pressure", "lower_is_established", "false_positive_pressure"),
    ("phase_intensity_gap", "lower_is_established", "false_positive_pressure"),
)


def oriented_value(row: Mapping[str, Any], metric: str, direction: str) -> float:
    value = safe_float(row[metric])
    if direction == "lower_is_established":
        return -value
    return value


def metric_score_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    decisive = [row for row in rows if int(row["decisive_label"]) in (0, 1)]
    established = [row for row in decisive if int(row["decisive_label"]) == 1]
    no_horizon = [row for row in decisive if int(row["decisive_label"]) == 0]
    p1_est = [row for row in rows if row["analysis_group"] == "p1_established"]
    p0_false = [row for row in rows if row["analysis_group"] == "p0_high_score_no_horizon"]
    out: List[Dict[str, Any]] = []
    for metric, direction, family in METRICS:
        est_values = [oriented_value(row, metric, direction) for row in established]
        no_values = [oriented_value(row, metric, direction) for row in no_horizon]
        p1_values = [oriented_value(row, metric, direction) for row in p1_est]
        p0_values = [oriented_value(row, metric, direction) for row in p0_false]
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
                "median_established_minus_no_raw": median_defined(raw_est) - median_defined(raw_no),
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
                "median_genealogy_intensity": median_defined(safe_float(row[PRIMARY_SCORE]) for row in group_rows),
                "median_phase_entry_index": median_defined(safe_float(row["phase_entry_index"]) for row in group_rows),
                "median_tail_route_index": median_defined(safe_float(row["tail_route_index"]) for row in group_rows),
                "median_entry_timing_index": median_defined(safe_float(row["entry_timing_index"]) for row in group_rows),
                "median_component_tail_route_index": median_defined(safe_float(row["component_tail_route_index"]) for row in group_rows),
                "median_intensity_without_route_pressure": median_defined(safe_float(row["intensity_without_route_pressure"]) for row in group_rows),
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
                "label": row["far_shell_horizon_label"],
                "genealogy_intensity_index": safe_float(row[PRIMARY_SCORE]),
                "phase_entry_index": safe_float(row["phase_entry_index"]),
                "tail_route_index": safe_float(row["tail_route_index"]),
                "entry_timing_index": safe_float(row["entry_timing_index"]),
                "component_tail_route_index": safe_float(row["component_tail_route_index"]),
                "intensity_without_route_pressure": safe_float(row["intensity_without_route_pressure"]),
                "first_high_step": row["first_high_step"],
                "tail_mean_far_shell_share": safe_float(row["tail_mean_far_shell_share"]),
                "high_horizon_span": safe_float(row["high_horizon_span"]),
            }
        )
    return sorted(out, key=lambda row: (-safe_float(row["genealogy_intensity_index"]), row["placement"], row["seed_delta"]))


def diagnosis_rows(metric_rows: Sequence[Mapping[str, Any]], group_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    best_pre = max(
        (row for row in metric_rows if row["metric_family"] == "early_pre_entry"),
        key=lambda row: safe_float(row["auc_p1_established_vs_p0_false_positive"], -1.0),
    )
    best_downstream = max(
        (row for row in metric_rows if row["metric_family"] == "downstream_routing"),
        key=lambda row: safe_float(row["auc_p1_established_vs_p0_false_positive"], -1.0),
    )
    pressure = next(row for row in metric_rows if row["metric"] == "intensity_without_route_pressure")
    p0_group = next((row for row in group_rows if row["analysis_group"] == "p0_high_score_no_horizon"), None)
    p1_group = next((row for row in group_rows if row["analysis_group"] == "p1_established"), None)

    pre_auc = safe_float(best_pre["auc_p1_established_vs_p0_false_positive"])
    down_auc = safe_float(best_downstream["auc_p1_established_vs_p0_false_positive"])
    pressure_auc = safe_float(pressure["auc_p1_established_vs_p0_false_positive"])

    if pre_auc >= 0.80 and safe_float(best_pre["auc_established_vs_no"]) >= 0.75:
        status = "early_route_observable_promising"
        note = (
            f"Beste early/pre-entry observabel `{best_pre['metric']}` skiller p1 established fra p0 false positives "
            f"med AUC={fmt(pre_auc)}."
        )
        next_status = "pre_register_early_route_holdout"
        next_note = "Kan pre-registreres paa friske seeds uten aa bruke downstream horizon-felter."
    elif down_auc >= 0.90 and pre_auc < 0.80:
        status = "downstream_routing_separates_but_not_pre_entry"
        note = (
            f"Downstream routing `{best_downstream['metric']}` skiller rent nok (AUC={fmt(down_auc)}), "
            f"men beste early/pre-entry `{best_pre['metric']}` er svakere (AUC={fmt(pre_auc)})."
        )
        next_status = "instrument_pre_horizon_routing"
        next_note = "Neste steg bor instrumentere en tidligere route-entry/retention precursor, ikke bruke downstream route som selector."
    elif pressure_auc >= 0.80:
        status = "false_positive_pressure_promising"
        note = (
            f"Pressure-metrikken `{pressure['metric']}` skiller p0 false positives fra p1 established med AUC={fmt(pressure_auc)}."
        )
        next_status = "turn_pressure_into_pre_registered_observable"
        next_note = "Ma testes paa friske seeds og holdes adskilt fra horizon-output."
    else:
        status = "routing_observable_not_yet"
        note = (
            f"Ingen candidate observabel skiller p0 false positives rent nok: best early AUC={fmt(pre_auc)}, "
            f"best downstream AUC={fmt(down_auc)}, pressure AUC={fmt(pressure_auc)}."
        )
        next_status = "design_new_instrumentation"
        next_note = "Treng ny instrumentering av phase/band-entry eller support-to-far-shell routing."

    p0_note = "p0 false-positive group absent"
    if p0_group and p1_group:
        p0_note = (
            f"p0 false positives har median intensity {fmt(p0_group['median_genealogy_intensity'])} "
            f"mot p1 established {fmt(p1_group['median_genealogy_intensity'])}, men tail_route "
            f"{fmt(p0_group['median_tail_route_index'])} mot {fmt(p1_group['median_tail_route_index'])}."
        )

    return [
        {
            "diagnostic_family": "data_scope",
            "status": "no_new_dynamics_v15da_only",
            "note": "Analysen leser bare v15da runs og component trajectories.",
        },
        {"diagnostic_family": "primary_result", "status": status, "note": note},
        {"diagnostic_family": "false_positive_reading", "status": "p0_intensity_without_route", "note": p0_note},
        {"diagnostic_family": "next_step", "status": next_status, "note": next_note},
    ]


def build_report(
    *,
    group_rows: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
    false_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15db: routing/phase observable synthesis")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden bruker ingen ny dynamikk. Den analyserer v15da for aa finne hvorfor p0 kan ha hoy genealogy-intensity uten far-shell-horizon.")
    lines.append("Observabler deles i early/pre-entry, downstream routing og false-positive pressure.")
    lines.append("")
    lines.append("## Group summary")
    lines.append("")
    lines.append("| group | n | placements | labels | intensity | phase | tail route | entry timing | pressure |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in group_rows:
        lines.append(
            f"| {row['analysis_group']} | {int(row['n_runs'])} | {row['placements']} | {row['labels']} | {fmt(row['median_genealogy_intensity'])} | {fmt(row['median_phase_entry_index'])} | {fmt(row['median_tail_route_index'])} | {fmt(row['median_entry_timing_index'])} | {fmt(row['median_intensity_without_route_pressure'])} |"
        )
    lines.append("")
    lines.append("## Metric ranking")
    lines.append("")
    lines.append("| metric | family | direction | AUC est/no | AUC p1/p0 false | median p1-p0 false |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in metric_rows:
        lines.append(
            f"| {row['metric']} | {row['metric_family']} | {row['direction']} | {fmt(row['auc_established_vs_no'])} | {fmt(row['auc_p1_established_vs_p0_false_positive'])} | {fmt(row['median_p1_minus_p0_false_raw'])} |"
        )
    lines.append("")
    lines.append("## High-score no-horizon cases")
    lines.append("")
    lines.append("| placement | seed | score | phase | tail route | entry timing | pressure | first high | tail share | horizon |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in false_rows:
        lines.append(
            f"| {row['placement']} | {int(row['seed_delta'])} | {fmt(row['genealogy_intensity_index'])} | {fmt(row['phase_entry_index'])} | {fmt(row['tail_route_index'])} | {fmt(row['entry_timing_index'])} | {fmt(row['intensity_without_route_pressure'])} | {row['first_high_step']} | {fmt(row['tail_mean_far_shell_share'])} | {fmt(row['high_horizon_span'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en observabelsyntese, ikke en ny dynamisk validering.")
    lines.append("- Downstream route/retention kan forklare p0 false positives, men er ikke automatisk en gyldig pre-horizon selector.")
    lines.append("- Ikke oppgrader til partikler, Lorentz-likhet, invariant, entanglement eller universell geometri.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15db", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke refit v15cz-score eller v15da-resultater til en selector-claim.")
    lines.append("- Bruk funnet til aa designe en pre-horizon routing/phase observabel hvis mulig.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15db",
            "",
            "Denne runden brukte ingen nye simuleringer. Den spurte hvorfor noen p0-runs ser kraftige ut lokalt, men likevel ikke faar lang hale.",
            "",
            f"- Hovedlesning: `{diag['primary_result']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Kort sagt: vi ser forskjell paa lokal uro og faktisk rute/retensjon ut i far-shell. Men vi maa finne en tidligere observabel foer dette kan bli en predictor.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15db routing/phase observable synthesis.")
    p.add_argument("--out-run-features-csv", default=str(DOC / "v15db_routing_phase_run_features.csv"))
    p.add_argument("--out-group-csv", default=str(DOC / "v15db_routing_phase_group_summary.csv"))
    p.add_argument("--out-metrics-csv", default=str(DOC / "v15db_routing_phase_metric_scores.csv"))
    p.add_argument("--out-false-csv", default=str(DOC / "v15db_routing_phase_false_positive_cases.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15db_routing_phase_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15db_routing_phase_observable_synthesis.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15db_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15db.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_features = enriched_run_rows()
    group_rows = group_summary_rows(run_features)
    metric_rows = metric_score_rows(run_features)
    false_rows = false_positive_rows(run_features)
    diagnosis = diagnosis_rows(metric_rows, group_rows)

    write_csv(args.out_run_features_csv, run_features)
    write_csv(args.out_group_csv, group_rows)
    write_csv(args.out_metrics_csv, metric_rows)
    write_csv(args.out_false_csv, false_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            group_rows=group_rows,
            metric_rows=metric_rows,
            false_rows=false_rows,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
