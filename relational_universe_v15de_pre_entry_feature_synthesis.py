#!/usr/bin/env python3
"""v0.15de pre-entry feature synthesis from v15dd direct route logs.

v15dd logged direct route-entry and retention per snapshot. Those fields
separate p1 established from p0 false positives, but they are outcome-near.
This no-new-dynamics round asks whether the direct snapshot log contains
earlier fixed-window features that can become pre-registered selector
candidates.

Discipline:
- reads only v15dd outputs
- does not rerun dynamics
- marks windows <= 96 as strict pre-entry because earliest p1 established
  sustained high3 entry in v15dd is at step 104
- marks later windows as entry-risk, not selector-ready
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15cg_target768_far_shell_horizon_lab as v15cg


DOC = Path("Documentation")
SNAPSHOTS_CSV = DOC / "v15dd_direct_route_snapshot_log.csv"
RUNS_CSV = DOC / "v15dd_direct_route_run_summary.csv"

STRICT_PRE_ENTRY_MAX_STEP = 96
WINDOWS = (64, 96, 128, 256, 512, 640)


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
    v15.write_csv(path, list(rows))


def run_key(row: Mapping[str, Any]) -> Tuple[int, int]:
    return int(safe_float(row["placement"])), int(safe_float(row["seed_delta"]))


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


def decisive_label(label: str) -> int:
    if label == "established_far_shell_horizon":
        return 1
    if label == "no_far_shell_horizon":
        return 0
    return -1


def window_class(window: int) -> str:
    return "strict_pre_entry" if int(window) <= STRICT_PRE_ENTRY_MAX_STEP else "entry_risk_window"


def summarize_window(rows: Sequence[Mapping[str, str]], window: int) -> Dict[str, Any]:
    selected = [row for row in rows if safe_float(row["step"]) <= window]
    if not selected:
        return {}

    outer = [safe_float(row["outer_share"]) for row in selected]
    dist = [safe_float(row["weighted_mean_distance"]) for row in selected]
    share_margin = [safe_float(row["high_share_margin"]) for row in selected]
    distance_margin = [safe_float(row["high_distance_margin"]) for row in selected]
    pressure = [safe_float(row["outer_pressure_without_high"]) for row in selected]
    outer_present = [safe_float(row["outer_present_flag"]) for row in selected]
    mid_or_high = [safe_float(row["mid_or_high_flag"]) for row in selected]
    high = [safe_float(row["high_flag"]) for row in selected]
    components = [safe_float(row["component_count"]) for row in selected]
    largest = [safe_float(row["largest_component_fraction"]) for row in selected]
    steps = [safe_float(row["step"]) for row in selected]

    positive_share_margin_rate = mean_defined(1.0 if x >= 0 else 0.0 for x in share_margin)
    positive_distance_margin_rate = mean_defined(1.0 if x >= 0 else 0.0 for x in distance_margin)
    ready_both_rate = mean_defined(
        1.0 if safe_float(row["high_share_margin"]) >= -0.10 and safe_float(row["high_distance_margin"]) >= -1.0 else 0.0
        for row in selected
    )
    pressure_without_distance_gap = mean_defined(
        max(0.0, safe_float(row["outer_share"]) - v15cg.MID_SHARE_THRESHOLD)
        * max(0.0, v15cg.HIGH_DISTANCE_THRESHOLD - safe_float(row["weighted_mean_distance"]))
        for row in selected
    )
    route_readiness_index = (
        0.35 * clamp01(mean_defined(outer) / v15cg.HIGH_SHARE_THRESHOLD)
        + 0.35 * clamp01(mean_defined(dist) / v15cg.HIGH_DISTANCE_THRESHOLD)
        + 0.15 * clamp01(max(outer) / v15cg.HIGH_SHARE_THRESHOLD)
        + 0.15 * clamp01(max(dist) / v15cg.HIGH_DISTANCE_THRESHOLD)
    )
    pressure_trap_index = (
        0.45 * clamp01(mean_defined(pressure))
        + 0.25 * clamp01(mean_defined(outer) / v15cg.HIGH_SHARE_THRESHOLD)
        + 0.20 * clamp01(max(outer) / v15cg.HIGH_SHARE_THRESHOLD)
        + 0.10 * clamp01(max(0.0, -mean_defined(distance_margin)) / v15cg.HIGH_DISTANCE_THRESHOLD)
    )

    prefix = f"w{int(window)}"
    return {
        f"{prefix}_snapshot_count": len(selected),
        f"{prefix}_mean_outer_share": mean_defined(outer),
        f"{prefix}_max_outer_share": max(outer),
        f"{prefix}_mean_weighted_distance": mean_defined(dist),
        f"{prefix}_max_weighted_distance": max(dist),
        f"{prefix}_mean_high_share_margin": mean_defined(share_margin),
        f"{prefix}_max_high_share_margin": max(share_margin),
        f"{prefix}_mean_high_distance_margin": mean_defined(distance_margin),
        f"{prefix}_max_high_distance_margin": max(distance_margin),
        f"{prefix}_outer_pressure_without_high_rate": mean_defined(pressure),
        f"{prefix}_outer_present_rate": mean_defined(outer_present),
        f"{prefix}_mid_or_high_rate": mean_defined(mid_or_high),
        f"{prefix}_high_rate": mean_defined(high),
        f"{prefix}_positive_share_margin_rate": positive_share_margin_rate,
        f"{prefix}_positive_distance_margin_rate": positive_distance_margin_rate,
        f"{prefix}_ready_both_rate": ready_both_rate,
        f"{prefix}_outer_share_slope_per_100": linear_slope(list(zip(steps, outer))) * 100.0,
        f"{prefix}_distance_slope_per_100": linear_slope(list(zip(steps, dist))) * 100.0,
        f"{prefix}_component_count_slope_per_100": linear_slope(list(zip(steps, components))) * 100.0,
        f"{prefix}_largest_component_slope_per_100": linear_slope(list(zip(steps, largest))) * 100.0,
        f"{prefix}_pressure_without_distance_gap": pressure_without_distance_gap,
        f"{prefix}_route_readiness_index": route_readiness_index,
        f"{prefix}_pressure_trap_index": pressure_trap_index,
    }


def build_run_features() -> List[Dict[str, Any]]:
    run_rows = read_csv(RUNS_CSV)
    snap_rows = read_csv(SNAPSHOTS_CSV)
    grouped_snaps: Dict[Tuple[int, int], List[Mapping[str, str]]] = defaultdict(list)
    for row in snap_rows:
        grouped_snaps[run_key(row)].append(row)

    out: List[Dict[str, Any]] = []
    for run in run_rows:
        key = run_key(run)
        snaps = sorted(grouped_snaps[key], key=lambda row: int(safe_float(row["snapshot_index"])))
        row: Dict[str, Any] = {
            "target_nodes": int(safe_float(run["target_nodes"])),
            "growth_seed": int(safe_float(run["growth_seed"])),
            "profile_label": str(run["profile_label"]),
            "perturbation": str(run["perturbation"]),
            "placement": int(safe_float(run["placement"])),
            "seed_delta": int(safe_float(run["seed_delta"])),
            "run_seed": int(safe_float(run["run_seed"])),
            "support_signature": str(run["support_signature"]),
            "far_shell_horizon_label": str(run["far_shell_horizon_label"]),
            "direct_route_entry_label": str(run["direct_route_entry_label"]),
            "analysis_group": str(run["analysis_group"]),
            "decisive_label": decisive_label(str(run["far_shell_horizon_label"])),
            "genealogy_intensity_index": safe_float(run["genealogy_intensity_index"]),
            "first_sustained_high3_step": int(safe_float(run["first_sustained_high3_step"], -1)),
            "direct_retention_rate_after_entry": safe_float(run["direct_retention_rate_after_entry"]),
            "outer_pressure_without_high_rate_full": safe_float(run["outer_pressure_without_high_rate"]),
        }
        for window in WINDOWS:
            row.update(summarize_window(snaps, window))
        out.append(row)
    return out


def metric_catalog() -> List[Tuple[str, str, int, str]]:
    metrics: List[Tuple[str, str, int, str]] = []
    for window in WINDOWS:
        prefix = f"w{window}"
        cls = window_class(window)
        specs = [
            ("mean_outer_share", "higher_is_established"),
            ("max_outer_share", "higher_is_established"),
            ("mean_weighted_distance", "higher_is_established"),
            ("max_weighted_distance", "higher_is_established"),
            ("mean_high_share_margin", "higher_is_established"),
            ("max_high_share_margin", "higher_is_established"),
            ("mean_high_distance_margin", "higher_is_established"),
            ("max_high_distance_margin", "higher_is_established"),
            ("outer_pressure_without_high_rate", "lower_is_established"),
            ("outer_present_rate", "higher_is_established"),
            ("positive_share_margin_rate", "higher_is_established"),
            ("positive_distance_margin_rate", "higher_is_established"),
            ("ready_both_rate", "higher_is_established"),
            ("outer_share_slope_per_100", "higher_is_established"),
            ("distance_slope_per_100", "higher_is_established"),
            ("component_count_slope_per_100", "higher_is_established"),
            ("largest_component_slope_per_100", "higher_is_established"),
            ("pressure_without_distance_gap", "lower_is_established"),
            ("route_readiness_index", "higher_is_established"),
            ("pressure_trap_index", "lower_is_established"),
        ]
        if cls != "strict_pre_entry":
            specs.extend(
                [
                    ("mid_or_high_rate", "higher_is_established"),
                    ("high_rate", "higher_is_established"),
                ]
            )
        for suffix, direction in specs:
            metrics.append((f"{prefix}_{suffix}", direction, window, cls))
    metrics.append(("genealogy_intensity_index", "higher_is_established", -1, "baseline_failed_selector"))
    return metrics


def oriented(row: Mapping[str, Any], metric: str, direction: str) -> float:
    value = safe_float(row[metric])
    return -value if direction == "lower_is_established" else value


def metric_score_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    decisive = [row for row in rows if int(row["decisive_label"]) in (0, 1)]
    established = [row for row in decisive if int(row["decisive_label"]) == 1]
    no_horizon = [row for row in decisive if int(row["decisive_label"]) == 0]
    p1_est = [row for row in rows if row["analysis_group"] == "p1_established"]
    p0_false = [row for row in rows if row["analysis_group"] == "p0_high_score_no_horizon"]
    out: List[Dict[str, Any]] = []
    for metric, direction, window, cls in metric_catalog():
        est_values = [oriented(row, metric, direction) for row in established]
        no_values = [oriented(row, metric, direction) for row in no_horizon]
        p1_values = [oriented(row, metric, direction) for row in p1_est]
        p0_values = [oriented(row, metric, direction) for row in p0_false]
        raw_p1 = [safe_float(row[metric]) for row in p1_est]
        raw_p0 = [safe_float(row[metric]) for row in p0_false]
        raw_est = [safe_float(row[metric]) for row in established]
        raw_no = [safe_float(row[metric]) for row in no_horizon]
        out.append(
            {
                "metric": metric,
                "direction": direction,
                "window_step": window,
                "window_class": cls,
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
            str(row["window_class"]) != "strict_pre_entry",
            -safe_float(row["auc_p1_established_vs_p0_false_positive"], -1.0),
            -safe_float(row["auc_established_vs_no"], -1.0),
        ),
    )


def window_summary_rows(metric_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for window in WINDOWS:
        for cls in sorted({row["window_class"] for row in metric_rows if int(row["window_step"]) == window}):
            group = [row for row in metric_rows if int(row["window_step"]) == window and row["window_class"] == cls]
            if not group:
                continue
            best = max(group, key=lambda row: safe_float(row["auc_p1_established_vs_p0_false_positive"], -1.0))
            out.append(
                {
                    "window_step": int(window),
                    "window_class": cls,
                    "n_metrics": len(group),
                    "best_metric": best["metric"],
                    "best_auc_p1_vs_p0_false": safe_float(best["auc_p1_established_vs_p0_false_positive"]),
                    "best_auc_established_vs_no": safe_float(best["auc_established_vs_no"]),
                    "best_direction": best["direction"],
                }
            )
    return out


def diagnosis_rows(metric_rows: Sequence[Mapping[str, Any]], window_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    strict = [row for row in metric_rows if row["window_class"] == "strict_pre_entry"]
    risky = [row for row in metric_rows if row["window_class"] == "entry_risk_window"]
    baseline = next(row for row in metric_rows if row["metric"] == "genealogy_intensity_index")
    best_strict = max(strict, key=lambda row: safe_float(row["auc_p1_established_vs_p0_false_positive"], -1.0))
    best_risky = max(risky, key=lambda row: safe_float(row["auc_p1_established_vs_p0_false_positive"], -1.0))
    strict_auc = safe_float(best_strict["auc_p1_established_vs_p0_false_positive"])
    strict_auc_global = safe_float(best_strict["auc_established_vs_no"])
    risky_auc = safe_float(best_risky["auc_p1_established_vs_p0_false_positive"])

    if strict_auc >= 0.80 and strict_auc_global >= 0.75:
        status = "strict_pre_entry_candidate_promising"
        note = (
            f"Beste strict pre-entry feature `{best_strict['metric']}` har AUC={fmt(strict_auc)} "
            f"for p1-vs-p0-false og AUC={fmt(strict_auc_global)} established-vs-no."
        )
        next_status = "pre_register_strict_pre_entry_holdout"
        next_note = "Frys feature, vindu og retning foer ny seed-holdout."
    elif risky_auc >= 0.90 and strict_auc < 0.80:
        status = "entry_risk_features_strong_but_strict_pre_entry_weak"
        note = (
            f"Entry-risk feature `{best_risky['metric']}` er sterk (AUC={fmt(risky_auc)}), "
            f"men beste strict pre-entry `{best_strict['metric']}` er svakere (AUC={fmt(strict_auc)})."
        )
        next_status = "do_not_pre_register_risky_window_yet"
        next_note = "Treng enten kortere vindu, ny instrumentering eller eksplisitt online-rule som stopper foer entry."
    elif strict_auc >= 0.70:
        status = "strict_pre_entry_candidate_weak"
        note = (
            f"Beste strict pre-entry feature `{best_strict['metric']}` er bare moderat: AUC={fmt(strict_auc)} "
            f"mot p0 false positives."
        )
        next_status = "inspect_strict_pre_entry_cases"
        next_note = "Se case-timelines foer eventuell holdout; ikke oppgrader til selector."
    else:
        status = "pre_entry_feature_not_found"
        note = f"Beste strict pre-entry feature `{best_strict['metric']}` har AUC={fmt(strict_auc)}."
        next_status = "seek_non_route_pre_entry_observable"
        next_note = "Route-loggen forklarer outcome, men gir ikke tidlig selector under strict-vindu."

    return [
        {
            "diagnostic_family": "data_scope",
            "status": "no_new_dynamics_v15dd_only",
            "note": "Analysen leser bare v15dd snapshot-log og run-summary.",
        },
        {
            "diagnostic_family": "leakage_guard",
            "status": "strict_windows_le_96",
            "note": "Tidligste p1 established sustained high3 entry i v15dd er step 104; vinduer <=96 er strict pre-entry.",
        },
        {"diagnostic_family": "primary_result", "status": status, "note": note},
        {
            "diagnostic_family": "entry_risk_best",
            "status": str(best_risky["metric"]),
            "note": f"Beste senere vindu har AUC={fmt(risky_auc)} mot p0 false positives og skal behandles som entry-risk, ikke claim.",
        },
        {
            "diagnostic_family": "baseline_check",
            "status": "genealogy_intensity_still_not_selector",
            "note": f"Baseline genealogy-intensity har AUC={fmt(baseline['auc_p1_established_vs_p0_false_positive'])} mot p0 false positives.",
        },
        {"diagnostic_family": "next_step", "status": next_status, "note": next_note},
    ]


def build_report(
    metric_rows: Sequence[Mapping[str, Any]],
    window_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15de: pre-entry feature synthesis")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden bruker ingen ny dynamikk. Den leser v15dd snapshot-loggen og tester faste tidlige vinduer.")
    lines.append("Vinduer `<=96` er strict pre-entry fordi tidligste p1 established sustained high3-entry er step `104`.")
    lines.append("Senere vinduer rapporteres, men regnes som entry-risk og skal ikke brukes som selector-claim alene.")
    lines.append("")
    lines.append("## Window summary")
    lines.append("")
    lines.append("| window | class | best metric | AUC p1/p0 false | AUC est/no | direction |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in window_rows:
        lines.append(
            f"| {int(row['window_step'])} | {row['window_class']} | {row['best_metric']} | {fmt(row['best_auc_p1_vs_p0_false'])} | {fmt(row['best_auc_established_vs_no'])} | {row['best_direction']} |"
        )
    lines.append("")
    lines.append("## Top strict pre-entry metrics")
    lines.append("")
    lines.append("| metric | direction | AUC est/no | AUC p1/p0 false | median p1 | median p0 false | p1-p0 false |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    strict = [row for row in metric_rows if row["window_class"] == "strict_pre_entry"][:20]
    for row in strict:
        lines.append(
            f"| {row['metric']} | {row['direction']} | {fmt(row['auc_established_vs_no'])} | {fmt(row['auc_p1_established_vs_p0_false_positive'])} | {fmt(row['median_p1_established_raw'])} | {fmt(row['median_p0_false_positive_raw'])} | {fmt(row['median_p1_minus_p0_false_raw'])} |"
        )
    lines.append("")
    lines.append("## Top entry-risk metrics")
    lines.append("")
    lines.append("| metric | window | direction | AUC est/no | AUC p1/p0 false | median p1 | median p0 false |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    risky = [row for row in metric_rows if row["window_class"] == "entry_risk_window"][:15]
    for row in risky:
        lines.append(
            f"| {row['metric']} | {int(row['window_step'])} | {row['direction']} | {fmt(row['auc_established_vs_no'])} | {fmt(row['auc_p1_established_vs_p0_false_positive'])} | {fmt(row['median_p1_established_raw'])} | {fmt(row['median_p0_false_positive_raw'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Strict pre-entry-vinduer kan bli selector-kandidater hvis de er sterke nok.")
    lines.append("- Entry-risk-vinduer kan forklare mekanismen, men maa ikke behandles som pre-entry predictors.")
    lines.append("- Ikke oppgrader til partikler, Lorentz-likhet, entanglement, invariant eller universell geometri.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15de", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Bare strict pre-entry-vinduer kan vurderes for pre-registrert selector.")
    lines.append("- Entry-risk-vinduer er mekanistiske forklaringer, ikke selector-ready features.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15de",
            "",
            "Denne runden spurte om vi kan se et tegn foer den lange fjernhalen faktisk starter.",
            "",
            f"- Hovedlesning: `{diag['primary_result']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Kort sagt: vi skiller mellom ekte tidlige tegn og ting som bare ser smarte ut fordi de allerede ligger for naer utfallet.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15de pre-entry feature synthesis.")
    p.add_argument("--out-run-features-csv", default=str(DOC / "v15de_pre_entry_run_features.csv"))
    p.add_argument("--out-metrics-csv", default=str(DOC / "v15de_pre_entry_metric_scores.csv"))
    p.add_argument("--out-window-csv", default=str(DOC / "v15de_pre_entry_window_summary.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15de_pre_entry_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15de_pre_entry_feature_synthesis.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15de_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15de.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_features = build_run_features()
    metric_rows = metric_score_rows(run_features)
    window_rows = window_summary_rows(metric_rows)
    diagnosis = diagnosis_rows(metric_rows, window_rows)

    write_csv(args.out_run_features_csv, run_features)
    write_csv(args.out_metrics_csv, metric_rows)
    write_csv(args.out_window_csv, window_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(build_report(metric_rows, window_rows, diagnosis), encoding="utf-8")
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
