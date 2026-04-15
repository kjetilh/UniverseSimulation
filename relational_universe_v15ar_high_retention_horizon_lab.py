#!/usr/bin/env python3
"""v0.15ar high retention horizon lab for add_chord high boundary.

This round follows v15aq. v15aq made the immediate post-launch impulse more
readable, but the failed-probe track still did not become sharp enough.

The next narrow question is:

can the high boundary be read more cleanly through a simple horizon observable:
when high starts, how long does it remain present before the last high event?

This round runs no new simulations. It reuses the focused v15ao/v15ap run set
and the real v15ai snapshots.
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
IN_RUNS = DOC / "v15ap_pre_high_launch_runs.csv"
IN_SNAPSHOTS = DOC / "v15ai_early_lock_band_snapshots.csv"
IN_TARGET = DOC / "v15ap_pre_high_launch_target_summary.csv"

TARGET = 48
WINDOW = 72


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


def first_run_ge(bands: Sequence[str], target: str, length: int) -> int | None:
    current = 0
    for idx, band in enumerate(bands):
        current = current + 1 if band == target else 0
        if current >= length:
            return idx - length + 1
    return None


def classify_horizon(
    *,
    high_start_index: int,
    last_high_index: int,
    high_horizon_span: int,
    high_retention_rate: float,
    last12_high_rate: float,
) -> str:
    if high_start_index >= WINDOW:
        return "no_high_presence"
    if high_horizon_span <= 6 and last_high_index >= WINDOW - 3 and last12_high_rate <= 0.30:
        return "terminal_probe_horizon"
    if last_high_index <= 24 and high_horizon_span >= 12 and last12_high_rate == 0.0:
        return "failed_probe_horizon"
    if last_high_index == WINDOW - 1 and high_horizon_span >= 24 and high_retention_rate >= 0.65 and last12_high_rate >= 0.50:
        return "established_hold_horizon"
    return "mixed_horizon"


def note_for(label: str) -> str:
    if label == "established_hold_horizon":
        return "High starter og blir vaerende helt ut i halen med lang og reell horisont."
    if label == "terminal_probe_horizon":
        return "High dukker opp helt mot slutten og får bare en kort terminal horisont."
    if label == "failed_probe_horizon":
        return "High dukker opp tidlig nok, men forsvinner igjen lenge for sluttvinduet."
    if label == "no_high_presence":
        return "High blir aldri tilstede i noen faktisk horisont."
    return "Runet er fortsatt ikke helt skarpt lest av horisont-observabelen."


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
        bands = [str(r["shell_count_band"]) for r in snapshots]

        high_start_raw = first_run_ge(bands, "high", 3)
        high_start = WINDOW if high_start_raw is None else high_start_raw
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
        label = classify_horizon(
            high_start_index=high_start,
            last_high_index=last_high,
            high_horizon_span=high_horizon,
            high_retention_rate=retention,
            last12_high_rate=sum(1 for band in last12 if band == "high") / max(1, len(last12)),
        )
        out.append(
            {
                "row_role": str(run_row["row_role"]),
                "run_seed": run_seed,
                "source_group": str(run_row["source_group"]),
                "placement": int(run_row["placement"]),
                "support_signature": str(run_row["support_signature"]),
                "launch_label": str(run_row["launch_label"]),
                "high_start_index": high_start,
                "last_high_index": int(last_high),
                "high_horizon_span": int(high_horizon),
                "high_retention_rate": retention,
                "last12_high_rate": sum(1 for band in last12 if band == "high") / max(1, len(last12)),
                "last12_mid_rate": sum(1 for band in last12 if band == "mid") / max(1, len(last12)),
                "last12_low_rate": sum(1 for band in last12 if band == "low") / max(1, len(last12)),
                "horizon_label": label,
                "horizon_note": note_for(label),
            }
        )
    return out


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for label in sorted({str(row["horizon_label"]) for row in rows}):
        grp = [row for row in rows if str(row["horizon_label"]) == label]
        out.append(
            {
                "group_type": "horizon_label",
                "group_value": label,
                "n_runs": len(grp),
                "rate": len(grp) / max(1, len(rows)),
                "mean_high_start_index": mean_defined(safe_float(row["high_start_index"]) for row in grp),
                "mean_last_high_index": mean_defined(safe_float(row["last_high_index"]) for row in grp),
                "mean_high_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in grp),
                "mean_high_retention_rate": mean_defined(safe_float(row["high_retention_rate"]) for row in grp),
                "mean_last12_high_rate": mean_defined(safe_float(row["last12_high_rate"]) for row in grp),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_rows: Sequence[Mapping[str, str]],
    rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_rows if int(row["target_nodes"]) == TARGET)
    labels = {str(row["horizon_label"]) for row in rows}
    if labels >= {"established_hold_horizon", "terminal_probe_horizon", "failed_probe_horizon", "no_high_presence"}:
        status = "horizon_map_supported"
        note = "High-grensen blir na rent lest som et lite horisont-kart: ekte hold-horisont, terminal probe-horisont, failed probe-horisont og ingen high-presens."
        next_step = "holdout_horizon_map"
        next_note = "Neste steg bor teste dette horisont-kartet pa noen fa naerliggende seeds, ikke a scanne bredere."
    else:
        status = "horizon_map_still_mixed"
        note = "Horisont-observabelen gir noe struktur, men ikke et rent nok kart ennå."
        next_step = "change_failed_probe_observable"
        next_note = "Neste steg bor bytte observabel rundt failed-probe-sporet i stedet for a presse horisonten hardere."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": (
                "Startstorrelsene er fortsatt rent separert; denne runden bruker bare ekte v15ai- og v15ap-data."
                if size_clean
                else "Storrelsesseparasjonen er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "horizon_map_status",
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
    lines.append("# Relasjonell universgraf v0.15ar: high retention horizon lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden kjorer ingen nye simuleringer. Den bruker ekte `v15ai`-snapshotter og `v15ap`-runsettet for a lese high-grensen gjennom hvor lenge high faktisk blir vaerende etter start.")
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
    lines.append("| seed | launch label | start | last high | horizon | retention | last12 high | horizon label |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(rows, key=lambda r: int(r["run_seed"])):
        lines.append(
            f"| {int(row['run_seed'])} | {row['launch_label']} | {int(row['high_start_index'])} | {int(row['last_high_index'])} | {int(row['high_horizon_span'])} | {fmt(row['high_retention_rate'])} | {fmt(row['last12_high_rate'])} | {row['horizon_label']} |"
        )
    lines.append("")
    lines.append("## Aggregate")
    lines.append("")
    lines.append("| horizon label | n | rate | mean start | mean last high | mean horizon | mean retention |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['group_value']} | {int(row['n_runs'])} | {fmt(row['rate'])} | {fmt(row['mean_high_start_index'])} | {fmt(row['mean_last_high_index'])} | {fmt(row['mean_high_horizon_span'])} | {fmt(row['mean_high_retention_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en liten horisont-runde, ikke en ny scan.")
    lines.append("- Les horisont-labelene som lokale high-forlop, ikke som nye defect-arter.")
    lines.append("- Hvis denne runden virker, betyr det at forskjellen mellom hold, terminal probe og failed probe er lesbar i hvor langt high faktisk rekker a leve.")
    return "\n".join(lines) + "\n"


def build_recommendation(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    status = next(row for row in diagnosis if str(row["diagnostic_family"]) == "horizon_map_status")
    next_step = next(row for row in diagnosis if str(row["diagnostic_family"]) == "next_step")
    return "\n".join(
        [
            "# v0.15ar operativ anbefaling",
            "",
            f"- horizon-status: `{status['status']}`",
            f"- lesning: {status['note']}",
            f"- neste steg: `{next_step['status']}`",
            f"- begrunnelse: {next_step['note']}",
        ]
    ) + "\n"


def build_non_specialist_note(rows: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    by_seed = {int(row["run_seed"]): str(row["horizon_label"]) for row in rows}
    status = next(row for row in diagnosis if str(row["diagnostic_family"]) == "horizon_map_status")
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15ar",
        "",
        "Denne runden sa pa hvor langt high faktisk lever etter at det begynner, i stedet for bare hvordan starten eller impulsen ser ut.",
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
        "Det nye her er at high-grensen kan leses gjennom hvor langt high faktisk lever: holder helt ut, bare blinker til på slutten, glipper tidlig, eller dukker aldri opp.",
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

    write_csv(DOC / "v15ar_high_retention_horizon_runs.csv", rows)
    write_csv(DOC / "v15ar_high_retention_horizon_aggregate.csv", aggregate)
    write_csv(DOC / "v15ar_high_retention_horizon_diagnosis.csv", diagnosis)
    write_csv(DOC / "v15ar_high_retention_horizon_target_summary.csv", list(target_rows))
    (DOC / "v15ar_high_retention_horizon_lab.md").write_text(report, encoding="utf-8")
    (DOC / "v0_15ar_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15ar.md").write_text(non_specialist, encoding="utf-8")


if __name__ == "__main__":
    main()
