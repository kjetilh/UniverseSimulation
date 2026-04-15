#!/usr/bin/env python3
"""v0.15an boundary high-hold lab for add_chord early-lock overlap zone.

This round follows v15am. v15am made the boundary overlap cases more readable,
but one case still stayed only partly explained.

The next narrow question is:

can the overlap zone be read more sharply by asking whether high-band, once it
appears, actually holds, rebounds, or only flashes very late?

This round runs no new simulations. It reuses the real v15ai snapshots and the
focused run set already selected in v15am.
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
IN_RUNS = DOC / "v15am_boundary_overlap_explainer_runs.csv"
IN_SNAPSHOTS = DOC / "v15ai_early_lock_band_snapshots.csv"
IN_TARGET = DOC / "v15am_boundary_overlap_explainer_target_summary.csv"

TARGET = 48
WINDOW = 72
LAST12 = 12


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


def classify_high_hold(
    *,
    row_role: str,
    high_hold_start_index: int,
    high_hold_span_snapshots: int,
    high_hold_rate: float,
    high_relapse_count: int,
    last12_high_rate: float,
) -> str:
    if row_role == "typical_mid_plateau":
        return "no_high_hold_reference"
    if row_role == "typical_late_high_rise":
        if high_hold_rate >= 0.90 and high_relapse_count <= 1:
            return "stable_high_hold_reference"
        return "rebounding_high_hold_reference"
    if high_hold_start_index >= WINDOW:
        return "no_high_hold_plateau"
    if high_hold_span_snapshots <= 6 and high_hold_start_index >= WINDOW - 6:
        return "late_terminal_high_probe"
    if high_hold_rate >= 0.70 and last12_high_rate >= 0.50:
        return "delayed_high_hold_crossover"
    return "ambiguous_high_hold"


def mechanism_note(label: str) -> str:
    if label == "stable_high_hold_reference":
        return "Typisk late high-rise der high-band etablerer seg og holder nesten kontinuerlig."
    if label == "rebounding_high_hold_reference":
        return "Typisk late high-rise der high-band holder, men med noen tydelige tilbakefall og gjenopptakelser."
    if label == "no_high_hold_reference":
        return "Typisk mid-platå der high-band aldri etablerer noen reell hold-fase."
    if label == "delayed_high_hold_crossover":
        return "Runet kommer sent inn i high-band, men holder seg deretter lenge nok til at det ligner et ekte high-hold-spor."
    if label == "no_high_hold_plateau":
        return "Runet får ikke noen faktisk high-hold-fase og blir liggende i platåformen."
    if label == "late_terminal_high_probe":
        return "Runet viser high-band helt mot slutten, men bare som en kort terminal probe, ikke som en etablert hold-fase."
    return "Runet er ikke skarpt lest av high-hold-observabelen ennå."


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
        snapshots = sorted(snapshot_lookup[run_seed], key=lambda row: int(row["step"]))[:WINDOW]
        bands = [str(row["shell_count_band"]) for row in snapshots]
        steps = [int(row["step"]) for row in snapshots]
        component_counts = [safe_float(row["shell_component_count"]) for row in snapshots]

        start_idx_raw = first_run_ge(bands, "high", 3)
        start_idx = WINDOW if start_idx_raw is None else start_idx_raw
        suffix = bands[start_idx:] if start_idx_raw is not None else []
        suffix_components = component_counts[start_idx:] if start_idx_raw is not None else []

        high_hold_rate = sum(1 for band in suffix if band == "high") / max(1, len(suffix)) if suffix else 0.0
        high_relapse_count = sum(1 for a, b in zip(suffix, suffix[1:]) if a == "high" and b != "high")
        high_regain_count = sum(1 for a, b in zip(suffix, suffix[1:]) if a != "high" and b == "high")
        last12 = bands[-LAST12:]
        label = classify_high_hold(
            row_role=str(run_row["row_role"]),
            high_hold_start_index=start_idx,
            high_hold_span_snapshots=len(suffix),
            high_hold_rate=high_hold_rate,
            high_relapse_count=high_relapse_count,
            last12_high_rate=sum(1 for band in last12 if band == "high") / max(1, len(last12)),
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
                "onset_family": str(run_row["onset_family"]),
                "boundary_split_label": str(run_row["boundary_split_label"]),
                "prior_overlap_explanation": str(run_row["overlap_explanation_label"]),
                "high_hold_start_index": start_idx,
                "high_hold_start_step": int(steps[start_idx]) if start_idx_raw is not None else -1,
                "high_hold_span_snapshots": len(suffix),
                "high_hold_span_steps": len(suffix) * 8,
                "high_hold_rate": high_hold_rate,
                "longest_high_run_after_start": longest_run(suffix, "high") if suffix else 0,
                "high_relapse_count": int(high_relapse_count),
                "high_regain_count": int(high_regain_count),
                "post_start_switch_count": int(sum(1 for a, b in zip(suffix, suffix[1:]) if a != b)),
                "last12_high_rate": sum(1 for band in last12 if band == "high") / max(1, len(last12)),
                "last12_mid_rate": sum(1 for band in last12 if band == "mid") / max(1, len(last12)),
                "last12_low_rate": sum(1 for band in last12 if band == "low") / max(1, len(last12)),
                "mean_post_start_component_count": mean_defined(suffix_components) if suffix_components else 0.0,
                "high_hold_label": label,
                "high_hold_note": mechanism_note(label),
            }
        )
    return out


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    overlap_rows = [row for row in rows if str(row["row_role"]) == "overlap_case"]
    for label in sorted({str(row["high_hold_label"]) for row in overlap_rows}):
        grp = [row for row in overlap_rows if str(row["high_hold_label"]) == label]
        out.append(
            {
                "group_type": "overlap_high_hold",
                "group_value": label,
                "n_runs": len(grp),
                "rate": len(grp) / max(1, len(overlap_rows)),
                "mean_high_hold_start_index": mean_defined(safe_float(row["high_hold_start_index"]) for row in grp),
                "mean_high_hold_span_snapshots": mean_defined(safe_float(row["high_hold_span_snapshots"]) for row in grp),
                "mean_high_hold_rate": mean_defined(safe_float(row["high_hold_rate"]) for row in grp),
                "mean_high_relapse_count": mean_defined(safe_float(row["high_relapse_count"]) for row in grp),
                "mean_high_regain_count": mean_defined(safe_float(row["high_regain_count"]) for row in grp),
                "mean_last12_high_rate": mean_defined(safe_float(row["last12_high_rate"]) for row in grp),
            }
        )
    for role in ("typical_late_high_rise", "typical_mid_plateau"):
        grp = [row for row in rows if str(row["row_role"]) == role]
        out.append(
            {
                "group_type": "reference_role",
                "group_value": role,
                "n_runs": len(grp),
                "rate": 1.0,
                "mean_high_hold_start_index": mean_defined(safe_float(row["high_hold_start_index"]) for row in grp),
                "mean_high_hold_span_snapshots": mean_defined(safe_float(row["high_hold_span_snapshots"]) for row in grp),
                "mean_high_hold_rate": mean_defined(safe_float(row["high_hold_rate"]) for row in grp),
                "mean_high_relapse_count": mean_defined(safe_float(row["high_relapse_count"]) for row in grp),
                "mean_high_regain_count": mean_defined(safe_float(row["high_regain_count"]) for row in grp),
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
    overlap_labels = {str(row["high_hold_label"]) for row in rows if str(row["row_role"]) == "overlap_case"}
    if overlap_labels == {
        "delayed_high_hold_crossover",
        "late_terminal_high_probe",
        "no_high_hold_plateau",
    }:
        status = "high_hold_observable_sharpens_overlap_zone"
        note = "Overlap-sonen blir skarpere lest av high-hold-observabelen: ett lop faar reell sen high-hold, ett blir igjen uten high-hold, og residual-caset reduseres til en sen terminal high-probe."
        next_step = "probe_terminal_probe_boundary"
        next_note = "Neste steg bor teste hva som skiller ekte sen high-hold fra bare terminal high-probe, ikke presse generell overlap-forklaring videre."
    else:
        status = "high_hold_observable_still_mixed"
        note = "High-hold-observabelen gir litt mer struktur, men overlap-sonen kollapser fortsatt ikke rent."
        next_step = "change_overlap_observable_again"
        next_note = "Neste steg bor bytte overlap-observabel igjen, ikke presse high-hold videre."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": (
                "Startstorrelsene er fortsatt rent separert; denne runden bruker bare ekte v15ai- og v15am-data."
                if size_clean
                else "Storrelsesseparasjonen er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "high_hold_status",
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
    overlap_rows = [row for row in rows if str(row["row_role"]) == "overlap_case"]
    reference_rows = [row for row in rows if str(row["row_role"]) != "overlap_case"]
    overlap_aggregate = [row for row in aggregate if str(row["group_type"]) == "overlap_high_hold"]
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15an: boundary high-hold lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden kjorer ingen nye simuleringer. Den bruker ekte `v15ai`-snapshotter og det fokuserte run-settet fra `v15am` for a lese overlap-sonen gjennom hvor stabilt high-band holder etter forste opptreden.")
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
    lines.append("## Reference high-hold profiles")
    lines.append("")
    lines.append("| role | seed | start idx | span | hold rate | relapses | regains | last12 high | label |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(reference_rows, key=lambda row: (str(row["row_role"]), int(row["run_seed"]))):
        lines.append(
            f"| {row['row_role']} | {int(row['run_seed'])} | {int(row['high_hold_start_index'])} | {int(row['high_hold_span_snapshots'])} | {fmt(row['high_hold_rate'])} | {int(row['high_relapse_count'])} | {int(row['high_regain_count'])} | {fmt(row['last12_high_rate'])} | {row['high_hold_label']} |"
        )
    lines.append("")
    lines.append("## Overlap high-hold cases")
    lines.append("")
    lines.append("| seed | prior explanation | start idx | span | hold rate | relapses | regains | last12 high | high-hold label |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(overlap_rows, key=lambda row: int(row["run_seed"])):
        lines.append(
            f"| {int(row['run_seed'])} | {row['prior_overlap_explanation']} | {int(row['high_hold_start_index'])} | {int(row['high_hold_span_snapshots'])} | {fmt(row['high_hold_rate'])} | {int(row['high_relapse_count'])} | {int(row['high_regain_count'])} | {fmt(row['last12_high_rate'])} | {row['high_hold_label']} |"
        )
    lines.append("")
    lines.append("## Overlap aggregate")
    lines.append("")
    lines.append("| label | n | rate | mean start idx | mean span | mean hold rate | mean relapses |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in overlap_aggregate:
        lines.append(
            f"| {row['group_value']} | {int(row['n_runs'])} | {fmt(row['rate'])} | {fmt(row['mean_high_hold_start_index'], 1)} | {fmt(row['mean_high_hold_span_snapshots'], 1)} | {fmt(row['mean_high_hold_rate'])} | {fmt(row['mean_high_relapse_count'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en liten overlap-runde, ikke en ny scan.")
    lines.append("- Les high-hold-labelene som en observabel for haleatferd, ikke som nye defect-arter.")
    lines.append("- Hvis denne observabelen virker, betyr det at overlap-sonen best forklares av forskjellen mellom ekte sen high-hold og sen, men bare terminal, high-opptreden.")
    return "\n".join(lines) + "\n"


def build_recommendation(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    status = next(row for row in diagnosis if str(row["diagnostic_family"]) == "high_hold_status")
    next_step = next(row for row in diagnosis if str(row["diagnostic_family"]) == "next_step")
    lines = [
        "# v0.15an operativ anbefaling",
        "",
        f"- high-hold-status: `{status['status']}`",
        f"- lesning: {status['note']}",
        f"- neste steg: `{next_step['status']}`",
        f"- begrunnelse: {next_step['note']}",
    ]
    return "\n".join(lines) + "\n"


def build_non_specialist_note(rows: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    overlap_rows = [row for row in rows if str(row["row_role"]) == "overlap_case"]
    by_seed = {int(row["run_seed"]): str(row["high_hold_label"]) for row in overlap_rows}
    status = next(row for row in diagnosis if str(row["diagnostic_family"]) == "high_hold_status")
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15an",
        "",
        "Denne runden spurte ikke bare om high-band dukker opp, men om det faktisk holder seg etter at det har dukket opp.",
        "",
        "Det viktigste vi fant er:",
        "",
        f"- seed `5002161`: `{by_seed.get(5002161, 'uklar')}`",
        f"- seed `5002240`: `{by_seed.get(5002240, 'uklar')}`",
        f"- seed `5002220`: `{by_seed.get(5002220, 'uklar')}`",
        "",
        f"Den operative dommen er `{status['status']}`: {status['note']}",
        "",
        "Dette gir mer nytte enn bare en ny etikett, fordi residual-caset na leses som en sen terminal high-probe i stedet for et nesten-high-rise lop.",
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

    write_csv(DOC / "v15an_boundary_high_hold_runs.csv", rows)
    write_csv(DOC / "v15an_boundary_high_hold_aggregate.csv", aggregate)
    write_csv(DOC / "v15an_boundary_high_hold_diagnosis.csv", diagnosis)
    write_csv(DOC / "v15an_boundary_high_hold_target_summary.csv", list(target_rows))
    (DOC / "v15an_boundary_high_hold_lab.md").write_text(report, encoding="utf-8")
    (DOC / "v0_15an_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15an.md").write_text(non_specialist, encoding="utf-8")


if __name__ == "__main__":
    main()
