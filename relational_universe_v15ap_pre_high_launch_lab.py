#!/usr/bin/env python3
"""v0.15ap pre-high launch lab for add_chord delayed high boundary.

This round follows v15ao. v15ao split the narrow high boundary into four late
tail outcomes:

- established high hold
- terminal high probe
- failed early high probe
- no high-hold plateau

The next narrow question is:

can those outcomes be read more mechanistically from the pre-high launch window
just before high appears or fails to appear?

This round runs no new simulations. It reuses the focused v15ao run set and
the real v15ai snapshots.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v15_defect_lifetime_lab as v15


DOC = Path("Documentation")
IN_RUNS = DOC / "v15ao_terminal_probe_boundary_runs.csv"
IN_SNAPSHOTS = DOC / "v15ai_early_lock_band_snapshots.csv"
IN_TARGET = DOC / "v15ao_terminal_probe_boundary_target_summary.csv"

TARGET = 48
WINDOW = 72
PRE_WINDOW = 8


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


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def classify_launch(
    *,
    high_boundary_label: str,
    pre_high_count: int,
    pre_low_count: int,
    pre_mid_count: int,
    pre_mean_largest_fraction: float,
    pre_mean_active_nodes: float,
    pre_mean_component_count: float,
) -> str:
    if high_boundary_label == "no_high_hold_plateau":
        return "no_launch_plateau"
    if high_boundary_label == "established_high_hold":
        if pre_high_count >= 1 and pre_mean_largest_fraction <= 0.25:
            return "mixed_threshold_launch"
        return "soft_threshold_launch"
    if high_boundary_label == "terminal_high_probe":
        if pre_high_count == 0 and pre_mid_count == PRE_WINDOW and pre_mean_largest_fraction >= 0.28:
            return "compact_terminal_launch"
        return "soft_terminal_launch"
    if high_boundary_label == "failed_early_high_probe":
        if pre_high_count == 0 and pre_mid_count == PRE_WINDOW and pre_mean_active_nodes - pre_mean_component_count <= 0.25:
            return "premature_probe_launch"
        return "soft_failed_probe_launch"
    return "unclassified_launch"


def note_for(label: str) -> str:
    if label == "mixed_threshold_launch":
        return "Launch-vinduet er fortsatt litt blandet, med minst ett tidlig high-glimt og lav shell-kompakthet, før ekte high-hold tar over."
    if label == "soft_threshold_launch":
        return "Launch-vinduet peker mot threshold-passering, men ikke like rent som de sterkeste hold-lopene."
    if label == "compact_terminal_launch":
        return "Launch-vinduet er helt mid-dominert og mer kompakt, og high kommer for sent til a bli et ekte hold."
    if label == "soft_terminal_launch":
        return "Runet ender som terminal probe, men launch-vinduet er ikke helt rent kompakt."
    if label == "premature_probe_launch":
        return "Launch-vinduet er helt mid-dominert, men mindre kompakt enn terminal-proben; high dukker opp tidlig og glipper igjen."
    if label == "soft_failed_probe_launch":
        return "Runet feiler som probe, men launch-vinduet er ikke helt rent lest."
    if label == "no_launch_plateau":
        return "Runet bygger aldri opp noe launch-vindu mot high og blir i platåformen."
    return "Launch-vinduet er fortsatt ikke skarpt lest."


def build_rows(
    *,
    run_rows_in: Sequence[Mapping[str, str]],
    snapshot_rows_in: Sequence[Mapping[str, str]],
) -> List[Dict[str, Any]]:
    snapshot_lookup: Dict[int, List[Dict[str, str]]] = defaultdict(list)
    for row in snapshot_rows_in:
        snapshot_lookup[int(row["run_seed"])].append(dict(row))

    out: List[Dict[str, Any]] = []
    for run_row in run_rows_in:
        run_seed = int(run_row["run_seed"])
        snapshots = sorted(snapshot_lookup[run_seed], key=lambda r: int(r["step"]))[:WINDOW]
        high_start_index = int(run_row["high_start_index"])
        pre_end = min(high_start_index, WINDOW)
        pre_start = max(0, pre_end - PRE_WINDOW)
        pre_rows = snapshots[pre_start:pre_end]

        pre_bands = [str(r["shell_count_band"]) for r in pre_rows]
        pre_high = sum(1 for band in pre_bands if band == "high")
        pre_mid = sum(1 for band in pre_bands if band == "mid")
        pre_low = sum(1 for band in pre_bands if band == "low")
        pre_largest = mean_defined(safe_float(r["largest_shell_component_fraction"]) for r in pre_rows) if pre_rows else float("nan")
        pre_components = mean_defined(safe_float(r["shell_component_count"]) for r in pre_rows) if pre_rows else float("nan")
        pre_active = mean_defined(safe_float(r["shell_active_nodes"]) for r in pre_rows) if pre_rows else float("nan")
        pre_boundary = mean_defined(safe_float(r["shell_boundary_to_volume"]) for r in pre_rows) if pre_rows else float("nan")

        launch_label = classify_launch(
            high_boundary_label=str(run_row["high_boundary_label"]),
            pre_high_count=pre_high,
            pre_low_count=pre_low,
            pre_mid_count=pre_mid,
            pre_mean_largest_fraction=pre_largest,
            pre_mean_active_nodes=pre_active,
            pre_mean_component_count=pre_components,
        )

        out.append(
            {
                "row_role": str(run_row["row_role"]),
                "run_seed": run_seed,
                "source_group": str(run_row["source_group"]),
                "placement": int(run_row["placement"]),
                "anchor_seed_delta": int(run_row["anchor_seed_delta"]),
                "holdout_seed_delta": int(run_row["holdout_seed_delta"]),
                "support_signature": str(run_row["support_signature"]),
                "high_boundary_label": str(run_row["high_boundary_label"]),
                "high_start_index": high_start_index,
                "pre_window_start_index": int(pre_start),
                "pre_window_len": int(len(pre_rows)),
                "pre_high_count": int(pre_high),
                "pre_mid_count": int(pre_mid),
                "pre_low_count": int(pre_low),
                "pre_mean_largest_fraction": pre_largest,
                "pre_mean_component_count": pre_components,
                "pre_mean_active_nodes": pre_active,
                "pre_active_minus_components": pre_active - pre_components if math.isfinite(pre_active) and math.isfinite(pre_components) else float("nan"),
                "pre_mean_boundary_to_volume": pre_boundary,
                "pre_band_signature": "".join(band[0] for band in pre_bands),
                "launch_label": launch_label,
                "launch_note": note_for(launch_label),
            }
        )
    return out


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for label in sorted({str(row["launch_label"]) for row in rows}):
        grp = [row for row in rows if str(row["launch_label"]) == label]
        out.append(
            {
                "group_type": "launch_label",
                "group_value": label,
                "n_runs": len(grp),
                "rate": len(grp) / max(1, len(rows)),
                "mean_pre_high_count": mean_defined(safe_float(row["pre_high_count"]) for row in grp),
                "mean_pre_mid_count": mean_defined(safe_float(row["pre_mid_count"]) for row in grp),
                "mean_pre_low_count": mean_defined(safe_float(row["pre_low_count"]) for row in grp),
                "mean_pre_largest_fraction": mean_defined(safe_float(row["pre_mean_largest_fraction"]) for row in grp),
                "mean_pre_component_count": mean_defined(safe_float(row["pre_mean_component_count"]) for row in grp),
                "mean_pre_active_minus_components": mean_defined(safe_float(row["pre_active_minus_components"]) for row in grp),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_rows: Sequence[Mapping[str, str]],
    rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_rows if int(row["target_nodes"]) == TARGET)
    labels = {str(row["launch_label"]) for row in rows}
    if labels >= {"mixed_threshold_launch", "compact_terminal_launch", "premature_probe_launch", "no_launch_plateau"}:
        status = "pre_high_launch_map_supported"
        note = "Pre-high-vinduet deler de fire haleutfallene i et lite launch-kart: blandet threshold-launch, kompakt terminal launch, prematur probe-launch og ingen launch."
        next_step = "holdout_launch_map"
        next_note = "Neste steg bor teste om dette launch-kartet holder pa noen fa naerliggende seeds, ikke a scanne bredere."
    else:
        status = "pre_high_launch_map_still_mixed"
        note = "Pre-high-vinduet gir litt mer struktur, men ikke et rent nok launch-kart ennå."
        next_step = "change_launch_observable"
        next_note = "Neste steg bor bytte launch-observabel i stedet for a presse denne hardere."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": (
                "Startstorrelsene er fortsatt rent separert; denne runden bruker bare ekte v15ai- og v15ao-data."
                if size_clean
                else "Storrelsesseparasjonen er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "launch_map_status",
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
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15ap: pre-high launch lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden kjorer ingen nye simuleringer. Den bruker ekte `v15ai`-snapshotter og `v15ao`-runsettet for a lese high-grensen gjennom launch-vinduet rett for high enten holder, feiler eller uteblir.")
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
    lines.append("## Focus runs")
    lines.append("")
    lines.append("| seed | high boundary | pre bands | pre high | pre mid | pre low | pre largest | pre active-comp | launch label |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(rows, key=lambda r: int(r["run_seed"])):
        lines.append(
            f"| {int(row['run_seed'])} | {row['high_boundary_label']} | {row['pre_band_signature']} | {int(row['pre_high_count'])} | {int(row['pre_mid_count'])} | {int(row['pre_low_count'])} | {fmt(row['pre_mean_largest_fraction'])} | {fmt(row['pre_active_minus_components'])} | {row['launch_label']} |"
        )
    lines.append("")
    lines.append("## Aggregate")
    lines.append("")
    lines.append("| launch label | n | rate | mean pre high | mean pre mid | mean pre low | mean pre largest |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['group_value']} | {int(row['n_runs'])} | {fmt(row['rate'])} | {fmt(row['mean_pre_high_count'])} | {fmt(row['mean_pre_mid_count'])} | {fmt(row['mean_pre_low_count'])} | {fmt(row['mean_pre_largest_fraction'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en liten launch-runde, ikke en ny scan.")
    lines.append("- Les launch-labelene som lokale pre-high forklaringer, ikke som nye defect-arter.")
    lines.append("- Hvis denne runden virker, betyr det at forskjellen mellom hold, terminal probe og failed probe faktisk er synlig allerede rett for high-forsoket.")
    return "\n".join(lines) + "\n"


def build_recommendation(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    status = next(row for row in diagnosis if str(row["diagnostic_family"]) == "launch_map_status")
    next_step = next(row for row in diagnosis if str(row["diagnostic_family"]) == "next_step")
    return "\n".join(
        [
            "# v0.15ap operativ anbefaling",
            "",
            f"- launch-status: `{status['status']}`",
            f"- lesning: {status['note']}",
            f"- neste steg: `{next_step['status']}`",
            f"- begrunnelse: {next_step['note']}",
        ]
    ) + "\n"


def build_non_specialist_note(rows: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    by_seed = {int(row["run_seed"]): str(row["launch_label"]) for row in rows}
    status = next(row for row in diagnosis if str(row["diagnostic_family"]) == "launch_map_status")
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15ap",
        "",
        "Denne runden sa pa de siste fa stegene for high-band for a se om ulike haleutfall faktisk starter forskjellig allerede like for selve high-forsoket.",
        "",
        "Det viktigste vi fant er:",
        "",
        f"- seed `5002161`: `{by_seed.get(5002161, 'uklar')}`",
        f"- seed `5002220`: `{by_seed.get(5002220, 'uklar')}`",
        f"- seed `5002221`: `{by_seed.get(5002221, 'uklar')}`",
        f"- seed `5002240`: `{by_seed.get(5002240, 'uklar')}`",
        "",
        f"Den operative dommen er `{status['status']}`: {status['note']}",
        "",
        "Det nye her er at forskjellen mellom ekte hold, terminal probe og mislykket probe ser ut til a finnes allerede i launch-vinduet, ikke bare i halen etterpa.",
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

    write_csv(DOC / "v15ap_pre_high_launch_runs.csv", rows)
    write_csv(DOC / "v15ap_pre_high_launch_aggregate.csv", aggregate)
    write_csv(DOC / "v15ap_pre_high_launch_diagnosis.csv", diagnosis)
    write_csv(DOC / "v15ap_pre_high_launch_target_summary.csv", list(target_rows))
    (DOC / "v15ap_pre_high_launch_lab.md").write_text(report, encoding="utf-8")
    (DOC / "v0_15ap_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15ap.md").write_text(non_specialist, encoding="utf-8")


if __name__ == "__main__":
    main()
