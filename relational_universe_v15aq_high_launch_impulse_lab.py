#!/usr/bin/env python3
"""v0.15aq high launch impulse lab for add_chord boundary launch map.

This round follows v15ap. v15ap showed that the four late-tail high outcomes
already look different in the small pre-high launch window.

The next narrow question is:

can we sharpen the difference between established high-hold and terminal probe
by measuring the immediate launch impulse right after the putative high start?

This round runs no new simulations. It reuses the focused v15ap run set and
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
IN_RUNS = DOC / "v15ap_pre_high_launch_runs.csv"
IN_SNAPSHOTS = DOC / "v15ai_early_lock_band_snapshots.csv"
IN_TARGET = DOC / "v15ap_pre_high_launch_target_summary.csv"

TARGET = 48
WINDOW = 72
POST_WINDOW = 8


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


def longest_run(values: Sequence[str], target: str) -> int:
    best = 0
    current = 0
    for value in values:
        if value == target:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def first_transition(values: Sequence[str], from_value: str, to_value: str) -> int | None:
    for idx, (a, b) in enumerate(zip(values, values[1:])):
        if a == from_value and b == to_value:
            return idx + 1
    return None


def classify_impulse(
    *,
    high_boundary_label: str,
    launch_label: str,
    first8_high_rate: float,
    longest_high_run_first8: int,
    first8_mid_rate: float,
    impulse_active_gain: float,
    first_high_to_mid_backslide: int | None,
) -> str:
    if high_boundary_label == "no_high_hold_plateau":
        return "inactive_mid_plateau"
    if high_boundary_label == "failed_early_high_probe":
        if first8_high_rate <= 0.50 and first8_mid_rate >= 0.25:
            return "premature_probe_impulse"
        return "soft_failed_impulse"
    if high_boundary_label == "terminal_high_probe":
        if longest_high_run_first8 <= 3 and impulse_active_gain >= 1.0:
            return "compact_late_spike"
        return "soft_terminal_spike"
    if high_boundary_label == "established_high_hold":
        if first8_high_rate >= 0.75 and longest_high_run_first8 >= 5 and first_high_to_mid_backslide not in (0, 1):
            return "sustained_hold_impulse"
        return "rebounding_hold_impulse"
    return "unclassified_impulse"


def note_for(label: str) -> str:
    if label == "sustained_hold_impulse":
        return "High-launch blir raskt dominert av high og holder lenge nok til at runet går inn i ekte hold."
    if label == "rebounding_hold_impulse":
        return "Launch-impulsen peker mot hold, men med tydelig tidlig tilbakefall før high stabiliserer seg."
    if label == "compact_late_spike":
        return "Runet far en kort og kompakt sen high-spike, men uten nok runway til et ekte hold."
    if label == "premature_probe_impulse":
        return "Runet far en tidlig high-impuls som raskt glipper tilbake i mid/lav band."
    if label == "inactive_mid_plateau":
        return "Runet bygger ingen reell high-impuls og blir liggende i mid-platået."
    return "Impulsen er fortsatt ikke skarpt lest."


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
        start = int(run_row["high_start_index"])
        post_rows = snapshots[start:min(WINDOW, start + POST_WINDOW)] if start < WINDOW else []
        post_bands = [str(r["shell_count_band"]) for r in post_rows]
        post_components = [safe_float(r["shell_component_count"]) for r in post_rows]
        post_active = [safe_float(r["shell_active_nodes"]) for r in post_rows]
        pre_active = safe_float(run_row["pre_mean_active_nodes"])
        pre_components = safe_float(run_row["pre_mean_component_count"])
        first8_high_rate = sum(1 for band in post_bands if band == "high") / max(1, len(post_bands)) if post_bands else 0.0
        first8_mid_rate = sum(1 for band in post_bands if band == "mid") / max(1, len(post_bands)) if post_bands else 0.0
        first8_low_rate = sum(1 for band in post_bands if band == "low") / max(1, len(post_bands)) if post_bands else 0.0
        mean_post_active = mean_defined(post_active) if post_active else 0.0
        mean_post_components = mean_defined(post_components) if post_components else 0.0
        label = classify_impulse(
            high_boundary_label=str(run_row["high_boundary_label"]),
            launch_label=str(run_row["launch_label"]),
            first8_high_rate=first8_high_rate,
            longest_high_run_first8=longest_run(post_bands, "high"),
            first8_mid_rate=first8_mid_rate,
            impulse_active_gain=mean_post_active - pre_active if math.isfinite(pre_active) else 0.0,
            first_high_to_mid_backslide=first_transition(post_bands, "high", "mid"),
        )
        out.append(
            {
                "row_role": str(run_row["row_role"]),
                "run_seed": run_seed,
                "source_group": str(run_row["source_group"]),
                "placement": int(run_row["placement"]),
                "support_signature": str(run_row["support_signature"]),
                "high_boundary_label": str(run_row["high_boundary_label"]),
                "launch_label": str(run_row["launch_label"]),
                "high_start_index": start,
                "post_window_len": len(post_rows),
                "post_band_signature": "".join(band[0] for band in post_bands),
                "first8_high_rate": first8_high_rate,
                "first8_mid_rate": first8_mid_rate,
                "first8_low_rate": first8_low_rate,
                "longest_high_run_first8": int(longest_run(post_bands, "high")) if post_bands else 0,
                "longest_mid_run_first8": int(longest_run(post_bands, "mid")) if post_bands else 0,
                "first_high_to_mid_backslide": -1 if first_transition(post_bands, "high", "mid") is None else int(first_transition(post_bands, "high", "mid")),
                "impulse_active_gain": mean_post_active - pre_active if math.isfinite(pre_active) else 0.0,
                "impulse_component_gain": mean_post_components - pre_components if math.isfinite(pre_components) else 0.0,
                "mean_post_active_nodes": mean_post_active,
                "mean_post_component_count": mean_post_components,
                "impulse_label": label,
                "impulse_note": note_for(label),
            }
        )
    return out


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for label in sorted({str(row["impulse_label"]) for row in rows}):
        grp = [row for row in rows if str(row["impulse_label"]) == label]
        out.append(
            {
                "group_type": "impulse_label",
                "group_value": label,
                "n_runs": len(grp),
                "rate": len(grp) / max(1, len(rows)),
                "mean_first8_high_rate": mean_defined(safe_float(row["first8_high_rate"]) for row in grp),
                "mean_first8_mid_rate": mean_defined(safe_float(row["first8_mid_rate"]) for row in grp),
                "mean_longest_high_run_first8": mean_defined(safe_float(row["longest_high_run_first8"]) for row in grp),
                "mean_impulse_active_gain": mean_defined(safe_float(row["impulse_active_gain"]) for row in grp),
                "mean_impulse_component_gain": mean_defined(safe_float(row["impulse_component_gain"]) for row in grp),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_rows: Sequence[Mapping[str, str]],
    rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_rows if int(row["target_nodes"]) == TARGET)
    labels = {str(row["impulse_label"]) for row in rows}
    if labels >= {"sustained_hold_impulse", "compact_late_spike", "premature_probe_impulse", "inactive_mid_plateau"}:
        status = "launch_impulse_map_supported"
        note = "Det første post-launch-vinduet deler high-grensen videre i et lite impulse-kart: ekte hold-impuls, kompakt sen spike, prematur probe-impuls og inaktivt mid-platå."
        next_step = "holdout_impulse_map"
        next_note = "Neste steg bor teste dette impulse-kartet pa noen fa naerliggende seeds, ikke a scanne bredere."
    else:
        status = "launch_impulse_map_still_mixed"
        note = "Impulsvinduet gir litt mer struktur, men ikke et rent nok kart ennå."
        next_step = "change_impulse_observable"
        next_note = "Neste steg bor bytte impulsobservabel i stedet for a presse dette kartet hardere."
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
            "diagnostic_family": "impulse_map_status",
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
    lines.append("# Relasjonell universgraf v0.15aq: high launch impulse lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden kjorer ingen nye simuleringer. Den bruker ekte `v15ai`-snapshotter og `v15ap`-runsettet for a lese high-grensen gjennom det aller forste post-launch-vinduet.")
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
    lines.append("| seed | launch label | post bands | high8 | mid8 | longest high | active gain | impulse label |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(rows, key=lambda r: int(r["run_seed"])):
        lines.append(
            f"| {int(row['run_seed'])} | {row['launch_label']} | {row['post_band_signature']} | {fmt(row['first8_high_rate'])} | {fmt(row['first8_mid_rate'])} | {int(row['longest_high_run_first8'])} | {fmt(row['impulse_active_gain'])} | {row['impulse_label']} |"
        )
    lines.append("")
    lines.append("## Aggregate")
    lines.append("")
    lines.append("| impulse label | n | rate | mean high8 | mean mid8 | mean longest high | mean active gain |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['group_value']} | {int(row['n_runs'])} | {fmt(row['rate'])} | {fmt(row['mean_first8_high_rate'])} | {fmt(row['mean_first8_mid_rate'])} | {fmt(row['mean_longest_high_run_first8'])} | {fmt(row['mean_impulse_active_gain'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en liten impulse-runde, ikke en ny scan.")
    lines.append("- Les impulslabelene som lokale onset-forklaringer, ikke som nye defect-arter.")
    lines.append("- Hvis denne runden virker, betyr det at forskjellen mellom hold og probe er lesbar allerede i det aller forste launch-stoetet.")
    return "\n".join(lines) + "\n"


def build_recommendation(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    status = next(row for row in diagnosis if str(row["diagnostic_family"]) == "impulse_map_status")
    next_step = next(row for row in diagnosis if str(row["diagnostic_family"]) == "next_step")
    return "\n".join(
        [
            "# v0.15aq operativ anbefaling",
            "",
            f"- impulse-status: `{status['status']}`",
            f"- lesning: {status['note']}",
            f"- neste steg: `{next_step['status']}`",
            f"- begrunnelse: {next_step['note']}",
        ]
    ) + "\n"


def build_non_specialist_note(rows: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    by_seed = {int(row["run_seed"]): str(row["impulse_label"]) for row in rows}
    status = next(row for row in diagnosis if str(row["diagnostic_family"]) == "impulse_map_status")
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15aq",
        "",
        "Denne runden sa ikke pa hele halen, men bare pa det aller forste launch-stoetet etter at high begynner eller nesten begynner.",
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
        "Det nye her er at forskjellen mellom ekte hold, sen probe og mislykket probe ser ut til a vaere synlig allerede i det forste launch-stoetet, ikke bare i resten av halen.",
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

    write_csv(DOC / "v15aq_high_launch_impulse_runs.csv", rows)
    write_csv(DOC / "v15aq_high_launch_impulse_aggregate.csv", aggregate)
    write_csv(DOC / "v15aq_high_launch_impulse_diagnosis.csv", diagnosis)
    write_csv(DOC / "v15aq_high_launch_impulse_target_summary.csv", list(target_rows))
    (DOC / "v15aq_high_launch_impulse_lab.md").write_text(report, encoding="utf-8")
    (DOC / "v0_15aq_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15aq.md").write_text(non_specialist, encoding="utf-8")


if __name__ == "__main__":
    main()
