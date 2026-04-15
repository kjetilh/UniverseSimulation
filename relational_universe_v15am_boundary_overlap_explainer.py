#!/usr/bin/env python3
"""v0.15am boundary overlap explainer for add_chord early-lock band.

This round follows v15al. v15al partly split the non-low boundary zone into:

- late_high_rise_boundary
- mid_plateau_boundary
- residual_boundary

But three overlap cases remained:

- one persistent churn run that still looked like late high-rise
- one mid-high entry run that still looked like mid plateau
- one mid-high entry run that stayed residual

This script runs no new simulations. It uses the real v15ai snapshots and the
real v15al boundary split rows to ask whether those overlap cases are at least
locally explainable against nearby typical reference runs.
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v15_defect_lifetime_lab as v15


DOC = Path("Documentation")
IN_RUNS = DOC / "v15al_boundary_zone_split_runs.csv"
IN_SNAPSHOTS = DOC / "v15ai_early_lock_band_snapshots.csv"
IN_TARGET = DOC / "v15al_boundary_zone_split_target_summary.csv"

TARGET = 48
WINDOW = 72
LAST12 = 12
OVERLAP_SEEDS = {5002161, 5002240, 5002220}
DISTANCE_FEATURES = (
    "first_high_ge3_index",
    "longest_high_run",
    "longest_mid_run",
    "collapse_low_index",
    "last12_high_rate",
    "last12_mid_rate",
    "peak_component_count",
    "last48_switch_count",
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def median_defined(values: Iterable[float]) -> float:
    finite = [safe_float(v) for v in values if math.isfinite(safe_float(v))]
    if not finite:
        return float("nan")
    return float(statistics.median(finite))


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def longest_run(bands: Sequence[str], target: str) -> int:
    best = 0
    current = 0
    for band in bands:
        if band == target:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def first_run_ge(bands: Sequence[str], target: str, length: int) -> int | None:
    current = 0
    for idx, band in enumerate(bands):
        current = current + 1 if band == target else 0
        if current >= length:
            return idx - length + 1
    return None


def collapse_index(bands: Sequence[str], target: str) -> int | None:
    for idx in range(len(bands)):
        if target not in bands[idx:]:
            return idx
    return None


def row_role(row: Mapping[str, str]) -> str | None:
    run_seed = int(row["run_seed"])
    onset_family = str(row["onset_family"])
    boundary = str(row["boundary_split_label"])
    if run_seed in OVERLAP_SEEDS:
        return "overlap_case"
    if onset_family == "mid_high_entry_family" and boundary == "late_high_rise_boundary":
        return "typical_late_high_rise"
    if onset_family == "persistent_churn_family" and boundary == "mid_plateau_boundary":
        return "typical_mid_plateau"
    return None


def compute_run_row(
    *,
    run_row: Mapping[str, str],
    snapshots: Sequence[Mapping[str, str]],
) -> Dict[str, Any]:
    ordered = sorted(snapshots, key=lambda row: int(row["step"]))[:WINDOW]
    bands = [str(row["shell_count_band"]) for row in ordered]
    component_counts = [safe_float(row["shell_component_count"]) for row in ordered]
    largest = [safe_float(row["largest_shell_component_fraction"]) for row in ordered]
    boundaries = [safe_float(row["shell_boundary_to_volume"]) for row in ordered]
    active = [safe_float(row["shell_active_nodes"]) for row in ordered]
    role = row_role(run_row)
    first_high_ge3 = first_run_ge(bands, "high", 3)
    collapse_low = collapse_index(bands, "low")
    collapse_mid = collapse_index(bands, "mid")
    last12 = bands[-LAST12:]
    return {
        "row_role": role,
        "run_seed": int(run_row["run_seed"]),
        "source_group": str(run_row["source_group"]),
        "placement": int(run_row["placement"]),
        "anchor_seed_delta": int(run_row["anchor_seed_delta"]),
        "holdout_seed_delta": int(run_row["holdout_seed_delta"]),
        "support_signature": str(run_row["support_signature"]),
        "onset_family": str(run_row["onset_family"]),
        "boundary_split_label": str(run_row["boundary_split_label"]),
        "first_high_ge3_index": float(WINDOW if first_high_ge3 is None else first_high_ge3),
        "longest_high_run": float(longest_run(bands, "high")),
        "longest_mid_run": float(longest_run(bands, "mid")),
        "longest_low_run": float(longest_run(bands, "low")),
        "collapse_low_index": float(WINDOW if collapse_low is None else collapse_low),
        "collapse_mid_index": float(WINDOW if collapse_mid is None else collapse_mid),
        "last12_high_rate": sum(1 for band in last12 if band == "high") / max(1, len(last12)),
        "last12_mid_rate": sum(1 for band in last12 if band == "mid") / max(1, len(last12)),
        "last12_low_rate": sum(1 for band in last12 if band == "low") / max(1, len(last12)),
        "first24_switch_count": float(sum(1 for a, b in zip(bands[:24], bands[1:24]) if a != b)),
        "last48_switch_count": float(sum(1 for a, b in zip(bands[24:], bands[25:]) if a != b)),
        "peak_component_count": max(component_counts),
        "last12_component_mean": mean_defined(component_counts[-LAST12:]),
        "last12_largest_fraction": mean_defined(largest[-LAST12:]),
        "last12_boundary_to_volume": mean_defined(boundaries[-LAST12:]),
        "last12_active_nodes": mean_defined(active[-LAST12:]),
        "peak_high_rate_72": safe_float(run_row["peak_high_rate_72"]),
        "high_last24_rate_72": safe_float(run_row["high_last24_rate_72"]),
        "mid_last24_rate_72": safe_float(run_row["mid_last24_rate_72"]),
        "low_last24_rate_72": safe_float(run_row["low_last24_rate_72"]),
        "mean_component_count_72": safe_float(run_row["mean_component_count_72"]),
        "mean_active_nodes_72": safe_float(run_row["mean_active_nodes_72"]),
        "mean_largest_fraction_72": safe_float(run_row["mean_largest_fraction_72"]),
        "mean_attachment_frac_72": safe_float(run_row["mean_attachment_frac_72"]),
        "mean_boundary_to_volume_72": safe_float(run_row["mean_boundary_to_volume_72"]),
        "switch_count_72": safe_float(run_row["switch_count_72"]),
    }


def build_profiles(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Dict[str, float]]:
    profiles: Dict[str, Dict[str, float]] = {}
    for role in ("typical_late_high_rise", "typical_mid_plateau"):
        grp = [row for row in rows if str(row["row_role"]) == role]
        profiles[role] = {
            feature: median_defined(safe_float(row[feature]) for row in grp)
            for feature in DISTANCE_FEATURES
        }
    return profiles


def feature_ranges(rows: Sequence[Mapping[str, Any]]) -> Dict[str, float]:
    out: Dict[str, float] = {}
    for feature in DISTANCE_FEATURES:
        values = [safe_float(row[feature]) for row in rows]
        finite = [value for value in values if math.isfinite(value)]
        out[feature] = max(finite) - min(finite) if finite else 1.0
        if out[feature] <= 0.0:
            out[feature] = 1.0
    return out


def distance_to_profile(
    *,
    row: Mapping[str, Any],
    profile: Mapping[str, float],
    ranges: Mapping[str, float],
) -> float:
    return sum(
        abs(safe_float(row[feature]) - safe_float(profile[feature])) / safe_float(ranges[feature], 1.0)
        for feature in DISTANCE_FEATURES
    ) / len(DISTANCE_FEATURES)


def classify_overlap(
    *,
    row: Mapping[str, Any],
    dist_high: float,
    dist_plateau: float,
) -> str:
    onset_family = str(row["onset_family"])
    boundary = str(row["boundary_split_label"])
    first_high = safe_float(row["first_high_ge3_index"])
    longest_mid = safe_float(row["longest_mid_run"])
    last12_high = safe_float(row["last12_high_rate"])
    last12_mid = safe_float(row["last12_mid_rate"])
    gap = abs(dist_high - dist_plateau)

    if onset_family == "persistent_churn_family" and boundary == "late_high_rise_boundary":
        return "churn_to_high_rise_crossover"
    if onset_family == "mid_high_entry_family" and boundary == "mid_plateau_boundary":
        if first_high >= WINDOW and longest_mid >= 18.0 and last12_mid >= 0.80:
            return "suppressed_high_rise_plateau"
        return "mid_high_plateau_crossover"
    if boundary == "residual_boundary":
        if gap <= 0.14 and last12_mid >= 0.60 and last12_high <= 0.30:
            return "residual_boundary_blend"
        if dist_high < dist_plateau:
            return "residual_tilt_to_high_rise"
        return "residual_tilt_to_mid_plateau"
    return "unclassified_overlap"


def explanation_note(label: str) -> str:
    if label == "churn_to_high_rise_crossover":
        return "Runet starter som et churn-nart boundary-spor, men glir sent over i en ekte high-rise hale."
    if label == "suppressed_high_rise_plateau":
        return "Runet kommer fra mid-high-entry-siden, men hoy-rise blir undertrykt og runet blir liggende pa et roligere mid-platå."
    if label == "residual_boundary_blend":
        return "Runet blir verken et rent high-rise-spor eller et rent mid-platå; det blir liggende i et blandet grenselag."
    if label == "residual_tilt_to_high_rise":
        return "Runet er residualt, men ligger metrisk naermere high-rise-profilen enn mid-platået."
    if label == "residual_tilt_to_mid_plateau":
        return "Runet er residualt, men ligger metrisk naermere mid-platå-profilen enn high-rise-profilen."
    if label == "typical_late_high_rise":
        return "Typisk referanserun for late high-rise."
    if label == "typical_mid_plateau":
        return "Typisk referanserun for mid-platå."
    return "Runet er ikke forklart av denne smale overlap-runden."


def build_rows(
    *,
    run_rows_in: Sequence[Mapping[str, str]],
    snapshot_rows_in: Sequence[Mapping[str, str]],
) -> List[Dict[str, Any]]:
    snapshot_lookup: Dict[int, List[Dict[str, str]]] = defaultdict(list)
    for row in snapshot_rows_in:
        snapshot_lookup[int(row["run_seed"])].append(dict(row))

    rows: List[Dict[str, Any]] = []
    for run_row in run_rows_in:
        role = row_role(run_row)
        if role is None:
            continue
        run_seed = int(run_row["run_seed"])
        rows.append(compute_run_row(run_row=run_row, snapshots=snapshot_lookup[run_seed]))

    profiles = build_profiles(rows)
    ranges = feature_ranges(rows)
    out: List[Dict[str, Any]] = []
    for row in rows:
        dist_high = distance_to_profile(row=row, profile=profiles["typical_late_high_rise"], ranges=ranges)
        dist_plateau = distance_to_profile(row=row, profile=profiles["typical_mid_plateau"], ranges=ranges)
        role = str(row["row_role"])
        if role == "overlap_case":
            explanation = classify_overlap(row=row, dist_high=dist_high, dist_plateau=dist_plateau)
        else:
            explanation = role
        margin = abs(dist_high - dist_plateau)
        nearest = "typical_late_high_rise" if dist_high < dist_plateau else "typical_mid_plateau"
        out.append(
            {
                **row,
                "distance_to_late_high_rise": dist_high,
                "distance_to_mid_plateau": dist_plateau,
                "distance_margin": margin,
                "nearest_reference_family": nearest,
                "overlap_explanation_label": explanation,
                "explanation_note": explanation_note(explanation),
            }
        )
    return out


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    overlap_rows = [row for row in rows if str(row["row_role"]) == "overlap_case"]
    for label in sorted({str(row["overlap_explanation_label"]) for row in overlap_rows}):
        grp = [row for row in overlap_rows if str(row["overlap_explanation_label"]) == label]
        out.append(
            {
                "group_type": "overlap_explanation",
                "group_value": label,
                "n_runs": len(grp),
                "rate": len(grp) / max(1, len(overlap_rows)),
                "mean_distance_to_late_high_rise": mean_defined(safe_float(row["distance_to_late_high_rise"]) for row in grp),
                "mean_distance_to_mid_plateau": mean_defined(safe_float(row["distance_to_mid_plateau"]) for row in grp),
                "mean_distance_margin": mean_defined(safe_float(row["distance_margin"]) for row in grp),
                "mean_first_high_ge3_index": mean_defined(safe_float(row["first_high_ge3_index"]) for row in grp),
                "mean_last12_high_rate": mean_defined(safe_float(row["last12_high_rate"]) for row in grp),
                "mean_last12_mid_rate": mean_defined(safe_float(row["last12_mid_rate"]) for row in grp),
                "mean_peak_component_count": mean_defined(safe_float(row["peak_component_count"]) for row in grp),
            }
        )
    for role in ("typical_late_high_rise", "typical_mid_plateau"):
        grp = [row for row in rows if str(row["row_role"]) == role]
        out.append(
            {
                "group_type": "reference_family",
                "group_value": role,
                "n_runs": len(grp),
                "rate": 1.0,
                "mean_distance_to_late_high_rise": mean_defined(safe_float(row["distance_to_late_high_rise"]) for row in grp),
                "mean_distance_to_mid_plateau": mean_defined(safe_float(row["distance_to_mid_plateau"]) for row in grp),
                "mean_distance_margin": mean_defined(safe_float(row["distance_margin"]) for row in grp),
                "mean_first_high_ge3_index": mean_defined(safe_float(row["first_high_ge3_index"]) for row in grp),
                "mean_last12_high_rate": mean_defined(safe_float(row["last12_high_rate"]) for row in grp),
                "mean_last12_mid_rate": mean_defined(safe_float(row["last12_mid_rate"]) for row in grp),
                "mean_peak_component_count": mean_defined(safe_float(row["peak_component_count"]) for row in grp),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_rows: Sequence[Mapping[str, str]],
    rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_rows if int(row["target_nodes"]) == TARGET)
    overlap_rows = [row for row in rows if str(row["row_role"]) == "overlap_case"]
    labels = {str(row["overlap_explanation_label"]) for row in overlap_rows}
    if labels == {
        "churn_to_high_rise_crossover",
        "suppressed_high_rise_plateau",
        "residual_boundary_blend",
    }:
        status = "overlap_cases_are_locally_explainable"
        note = "De tre overlap-caseene kollapser til tre forskjellige lokale forklaringer: en churn-til-high-rise crossover, en undertrykt high-rise som blir mid-platå, og ett residualt grenselag."
        next_step = "holdout_overlap_explanations"
        next_note = "Neste steg bor teste om akkurat disse overlap-forklaringene holder pa noen fa naerliggende seeds, ikke a scanne bredere."
    else:
        status = "overlap_cases_still_partly_mixed"
        note = "Overlap-caseene er mer lesbare enn i v15al, men kollapser ikke til et lite lokalt forklaringssett ennå."
        next_step = "change_overlap_observable"
        next_note = "Neste steg bor bytte observabel inne i overlap-sonen, ikke presse denne forklaringen hardere."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": (
                "Startstorrelsene er fortsatt rent separert; denne runden bruker bare ekte v15ai- og v15al-data."
                if size_clean
                else "Storrelsesseparasjonen er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "overlap_explainer_status",
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
    target_rows: Sequence[Mapping[str, str]],
    rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    reference_rows = [row for row in rows if str(row["row_role"]) != "overlap_case"]
    overlap_rows = [row for row in rows if str(row["row_role"]) == "overlap_case"]
    overlap_aggregate = [row for row in aggregate if str(row["group_type"]) == "overlap_explanation"]
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15am: boundary overlap explainer")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden kjorer ingen nye simuleringer. Den bruker ekte `v15ai`-snapshotter og ekte `v15al`-boundary-labels for a forklare de tre overlap-caseene som ble igjen mellom late high-rise og mid-platå.")
    lines.append("")
    lines.append("## Startstorrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_rows:
        if int(row["target_nodes"]) != TARGET:
            continue
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Reference profiles")
    lines.append("")
    lines.append("| role | seed | placement | first high>=3 | last12 high | last12 mid | longest high | longest mid | peak comp |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(reference_rows, key=lambda row: (str(row["row_role"]), int(row["run_seed"]))):
        lines.append(
            f"| {row['row_role']} | {int(row['run_seed'])} | {int(row['placement'])} | {fmt(row['first_high_ge3_index'], 1)} | {fmt(row['last12_high_rate'])} | {fmt(row['last12_mid_rate'])} | {fmt(row['longest_high_run'], 1)} | {fmt(row['longest_mid_run'], 1)} | {fmt(row['peak_component_count'], 1)} |"
        )
    lines.append("")
    lines.append("## Overlap cases")
    lines.append("")
    lines.append("| seed | onset family | boundary label | nearest | d high | d plateau | margin | explanation |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(overlap_rows, key=lambda row: int(row["run_seed"])):
        lines.append(
            f"| {int(row['run_seed'])} | {row['onset_family']} | {row['boundary_split_label']} | {row['nearest_reference_family']} | {fmt(row['distance_to_late_high_rise'])} | {fmt(row['distance_to_mid_plateau'])} | {fmt(row['distance_margin'])} | {row['overlap_explanation_label']} |"
        )
    lines.append("")
    lines.append("## Overlap aggregate")
    lines.append("")
    lines.append("| explanation | n | rate | mean first high>=3 | mean last12 high | mean last12 mid | mean margin |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in overlap_aggregate:
        lines.append(
            f"| {row['group_value']} | {int(row['n_runs'])} | {fmt(row['rate'])} | {fmt(row['mean_first_high_ge3_index'], 1)} | {fmt(row['mean_last12_high_rate'])} | {fmt(row['mean_last12_mid_rate'])} | {fmt(row['mean_distance_margin'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en liten forklaringsrunde inne i boundary-sonen, ikke en ny scan.")
    lines.append("- Les forklaringene som lokale overgangstyper, ikke som nye defect-arter eller lokale lover.")
    lines.append("- Hvis overlap-caseene er lokalt forklarbare, betyr det at `v15al` sin rest-ambiguitet er mer strukturert enn bare blandet stoy.")
    return "\n".join(lines) + "\n"


def build_recommendation(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    overlap_status = next(row for row in diagnosis if str(row["diagnostic_family"]) == "overlap_explainer_status")
    next_step = next(row for row in diagnosis if str(row["diagnostic_family"]) == "next_step")
    lines = [
        "# v0.15am operativ anbefaling",
        "",
        f"- overlap-status: `{overlap_status['status']}`",
        f"- lesning: {overlap_status['note']}",
        f"- neste steg: `{next_step['status']}`",
        f"- begrunnelse: {next_step['note']}",
    ]
    return "\n".join(lines) + "\n"


def build_non_specialist_note(rows: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    overlap_rows = [row for row in rows if str(row["row_role"]) == "overlap_case"]
    by_seed = {int(row["run_seed"]): str(row["overlap_explanation_label"]) for row in overlap_rows}
    status = next(row for row in diagnosis if str(row["diagnostic_family"]) == "overlap_explainer_status")
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15am",
        "",
        "Vi hadde fortsatt tre sma lop i boundary-sonen som ikke passet helt inn i hovedbildet fra `v15al`.",
        "",
        "Denne runden laget ingen nye simuleringer. Vi gikk bare tilbake til de ekte snapshottene og sammenlignet disse tre lopene med typiske high-rise- og mid-platå-lop.",
        "",
        "Det viktigste vi fant er:",
        "",
        f"- seed `5002161`: `{by_seed.get(5002161, 'uklar')}`",
        f"- seed `5002240`: `{by_seed.get(5002240, 'uklar')}`",
        f"- seed `5002220`: `{by_seed.get(5002220, 'uklar')}`",
        "",
        f"Den operative dommen er `{status['status']}`: {status['note']}",
        "",
        "Det betyr ikke at vi har en ny lov. Det betyr bare at de siste overlap-runene ser mer lokalt forklarbare ut enn de gjorde i `v15al`.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    run_rows_in = read_csv(IN_RUNS)
    snapshot_rows_in = read_csv(IN_SNAPSHOTS)
    target_rows = read_csv(IN_TARGET)

    rows = build_rows(run_rows_in=run_rows_in, snapshot_rows_in=snapshot_rows_in)
    aggregate = aggregate_rows(rows)
    diagnosis = diagnosis_rows(target_rows=target_rows, rows=rows)
    report = build_report(target_rows=target_rows, rows=rows, aggregate=aggregate, diagnosis=diagnosis)
    recommendation = build_recommendation(diagnosis)
    non_specialist = build_non_specialist_note(rows, diagnosis)

    write_csv(DOC / "v15am_boundary_overlap_explainer_runs.csv", rows)
    write_csv(DOC / "v15am_boundary_overlap_explainer_aggregate.csv", aggregate)
    write_csv(DOC / "v15am_boundary_overlap_explainer_diagnosis.csv", diagnosis)
    write_csv(DOC / "v15am_boundary_overlap_explainer_target_summary.csv", list(target_rows))
    (DOC / "v15am_boundary_overlap_explainer.md").write_text(report, encoding="utf-8")
    (DOC / "v0_15am_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15am.md").write_text(non_specialist, encoding="utf-8")


if __name__ == "__main__":
    main()
