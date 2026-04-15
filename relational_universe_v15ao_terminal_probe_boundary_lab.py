#!/usr/bin/env python3
"""v0.15ao terminal-probe boundary lab for add_chord delayed high outcomes.

This round follows v15an. v15an showed that the overlap zone becomes clearer if
we ask whether high-band actually holds:

- one case becomes a real delayed high-hold crossover
- one case stays a no-high plateau
- one residual case becomes only a terminal high probe

The next narrow question is:

can we sharpen the boundary further by comparing terminal high-probe not only
to real delayed high-hold, but also to a nearby case where high appears early
and then dies out?

This round runs no new simulations. It reuses v15ai snapshots together with
the focused v15am/v15an run set and one nearby delayed-structured control.
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
IN_V15AN = DOC / "v15an_boundary_high_hold_runs.csv"
IN_V15AJ = DOC / "v15aj_early_lock_band_onset_runs.csv"
IN_SNAPSHOTS = DOC / "v15ai_early_lock_band_snapshots.csv"
IN_TARGET = DOC / "v15an_boundary_high_hold_target_summary.csv"

TARGET = 48
WINDOW = 72
LAST12 = 12
EXTRA_RUN_SEEDS = {5002221}


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


def classify_outcome(
    *,
    high_start_index: int,
    runway_snapshots: int,
    high_hold_rate: float,
    first_high_block: int,
    last12_high_rate: float,
    post_start_low_rate: float,
) -> str:
    if high_start_index >= WINDOW:
        return "no_high_hold_plateau"
    if runway_snapshots <= 6 and first_high_block >= 3 and last12_high_rate <= 0.30:
        return "terminal_high_probe"
    if high_start_index <= 16 and high_hold_rate <= 0.35 and last12_high_rate == 0.0 and post_start_low_rate >= 0.25:
        return "failed_early_high_probe"
    if runway_snapshots >= 24 and high_hold_rate >= 0.65 and last12_high_rate >= 0.50:
        return "established_high_hold"
    return "ambiguous_high_boundary"


def outcome_note(label: str) -> str:
    if label == "established_high_hold":
        return "High-band kommer inn tidlig nok og holder lenge nok til at dette leses som et ekte high-hold-lop."
    if label == "terminal_high_probe":
        return "High-band dukker opp helt mot slutten og rekker ikke a etablere noen reell hold-fase."
    if label == "failed_early_high_probe":
        return "High-band dukker opp tidlig, men glipper og kollapser tilbake i lavere band i stedet for a holde."
    if label == "no_high_hold_plateau":
        return "Runet far aldri noen faktisk high-hold-fase og blir liggende i platåformen."
    return "Runet er fortsatt ikke skarpt lest av denne grenseobservabelen."


def build_focus_rows(
    *,
    v15an_rows_in: Sequence[Mapping[str, str]],
    v15aj_rows_in: Sequence[Mapping[str, str]],
    snapshot_rows_in: Sequence[Mapping[str, str]],
) -> List[Dict[str, Any]]:
    v15aj_lookup = {int(row["run_seed"]): dict(row) for row in v15aj_rows_in}
    snapshot_lookup: Dict[int, List[Dict[str, str]]] = defaultdict(list)
    for row in snapshot_rows_in:
        snapshot_lookup[int(row["run_seed"])].append(dict(row))

    base_rows = [dict(row) for row in v15an_rows_in]
    for seed in EXTRA_RUN_SEEDS:
        aj = v15aj_lookup[seed]
        base_rows.append(
            {
                "row_role": "nearby_probe_control",
                "run_seed": str(seed),
                "source_group": str(aj["source_group"]),
                "placement": str(aj["placement"]),
                "anchor_seed_delta": str(aj["anchor_seed_delta"]),
                "holdout_seed_delta": str(aj["holdout_seed_delta"]),
                "support_signature": str(aj["support_signature"]),
                "onset_family": "delayed_probe_control",
                "boundary_split_label": "outside_boundary_focus",
                "prior_overlap_explanation": "nearby_failed_probe_control",
            }
        )

    out: List[Dict[str, Any]] = []
    for row in base_rows:
        run_seed = int(row["run_seed"])
        snapshots = sorted(snapshot_lookup[run_seed], key=lambda r: int(r["step"]))[:WINDOW]
        bands = [str(r["shell_count_band"]) for r in snapshots]
        component_counts = [safe_float(r["shell_component_count"]) for r in snapshots]
        active_nodes = [safe_float(r["shell_active_nodes"]) for r in snapshots]
        high_start_raw = first_run_ge(bands, "high", 3)
        high_start = WINDOW if high_start_raw is None else high_start_raw
        suffix = bands[high_start:] if high_start_raw is not None else []

        first_high_block = 0
        if high_start_raw is not None:
            idx = high_start_raw
            while idx < len(bands) and bands[idx] == "high":
                first_high_block += 1
                idx += 1

        high_hold_rate = sum(1 for band in suffix if band == "high") / max(1, len(suffix)) if suffix else 0.0
        post_start_low_rate = sum(1 for band in suffix if band == "low") / max(1, len(suffix)) if suffix else 0.0
        post_start_mid_rate = sum(1 for band in suffix if band == "mid") / max(1, len(suffix)) if suffix else 0.0
        label = classify_outcome(
            high_start_index=high_start,
            runway_snapshots=len(suffix),
            high_hold_rate=high_hold_rate,
            first_high_block=first_high_block,
            last12_high_rate=sum(1 for band in bands[-LAST12:] if band == "high") / max(1, LAST12),
            post_start_low_rate=post_start_low_rate,
        )
        out.append(
            {
                "row_role": str(row["row_role"]),
                "run_seed": run_seed,
                "source_group": str(row["source_group"]),
                "placement": int(row["placement"]),
                "anchor_seed_delta": int(row["anchor_seed_delta"]),
                "holdout_seed_delta": int(row["holdout_seed_delta"]),
                "support_signature": str(row["support_signature"]),
                "onset_family": str(row["onset_family"]),
                "boundary_split_label": str(row["boundary_split_label"]),
                "prior_overlap_explanation": str(row["prior_overlap_explanation"]),
                "high_start_index": high_start,
                "high_start_step": int(snapshots[high_start]["step"]) if high_start_raw is not None else -1,
                "runway_snapshots": len(suffix),
                "runway_steps": len(suffix) * 8,
                "high_hold_rate": high_hold_rate,
                "post_start_mid_rate": post_start_mid_rate,
                "post_start_low_rate": post_start_low_rate,
                "first_high_block": int(first_high_block),
                "longest_high_run_after_start": int(longest_run(suffix, "high")) if suffix else 0,
                "longest_mid_run_after_start": int(longest_run(suffix, "mid")) if suffix else 0,
                "last12_high_rate": sum(1 for band in bands[-LAST12:] if band == "high") / max(1, LAST12),
                "last12_mid_rate": sum(1 for band in bands[-LAST12:] if band == "mid") / max(1, LAST12),
                "last12_low_rate": sum(1 for band in bands[-LAST12:] if band == "low") / max(1, LAST12),
                "peak_component_count": max(component_counts),
                "last12_component_mean": mean_defined(component_counts[-LAST12:]),
                "last12_active_mean": mean_defined(active_nodes[-LAST12:]),
                "high_boundary_label": label,
                "high_boundary_note": outcome_note(label),
            }
        )
    return out


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for label in sorted({str(row["high_boundary_label"]) for row in rows}):
        grp = [row for row in rows if str(row["high_boundary_label"]) == label]
        out.append(
            {
                "group_type": "high_boundary_label",
                "group_value": label,
                "n_runs": len(grp),
                "rate": len(grp) / max(1, len(rows)),
                "mean_high_start_index": mean_defined(safe_float(row["high_start_index"]) for row in grp),
                "mean_runway_snapshots": mean_defined(safe_float(row["runway_snapshots"]) for row in grp),
                "mean_high_hold_rate": mean_defined(safe_float(row["high_hold_rate"]) for row in grp),
                "mean_post_start_mid_rate": mean_defined(safe_float(row["post_start_mid_rate"]) for row in grp),
                "mean_post_start_low_rate": mean_defined(safe_float(row["post_start_low_rate"]) for row in grp),
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
    labels = {str(row["high_boundary_label"]) for row in rows}
    if labels >= {"established_high_hold", "terminal_high_probe", "failed_early_high_probe", "no_high_hold_plateau"}:
        status = "terminal_probe_boundary_is_structured"
        note = "Den smale high-grensen deler seg na i fire lesbare utfall: ekte high-hold, terminal high-probe, mislykket tidlig high-probe og ingen high-hold."
        next_step = "probe_terminal_vs_hold_trigger"
        next_note = "Neste steg bor forklare hva som bestemmer om sen high starter tidlig nok til a bli hold, i stedet for a ende som terminal probe."
    else:
        status = "terminal_probe_boundary_still_mixed"
        note = "High-grensen er litt tydeligere, men kollapser fortsatt ikke til et lite nok utfallssett."
        next_step = "change_high_boundary_observable"
        next_note = "Neste steg bor bytte observabel igjen i stedet for a presse denne grensen hardere."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": (
                "Startstorrelsene er fortsatt rent separert; denne runden bruker bare ekte v15ai-, v15aj- og v15an-data."
                if size_clean
                else "Storrelsesseparasjonen er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "terminal_probe_boundary_status",
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
    lines.append("# Relasjonell universgraf v0.15ao: terminal probe boundary lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden kjorer ingen nye simuleringer. Den bruker ekte `v15ai`-snapshotter, det fokuserte `v15an`-settet og ett naerliggende delayed-probe-kontrollop for a splitte high-grensen videre.")
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
    lines.append("| seed | role | start idx | runway | high hold | post mid | post low | last12 high | label |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(rows, key=lambda r: int(r["run_seed"])):
        lines.append(
            f"| {int(row['run_seed'])} | {row['row_role']} | {int(row['high_start_index'])} | {int(row['runway_snapshots'])} | {fmt(row['high_hold_rate'])} | {fmt(row['post_start_mid_rate'])} | {fmt(row['post_start_low_rate'])} | {fmt(row['last12_high_rate'])} | {row['high_boundary_label']} |"
        )
    lines.append("")
    lines.append("## Aggregate")
    lines.append("")
    lines.append("| label | n | rate | mean start idx | mean runway | mean hold | mean post mid | mean post low |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['group_value']} | {int(row['n_runs'])} | {fmt(row['rate'])} | {fmt(row['mean_high_start_index'], 1)} | {fmt(row['mean_runway_snapshots'], 1)} | {fmt(row['mean_high_hold_rate'])} | {fmt(row['mean_post_start_mid_rate'])} | {fmt(row['mean_post_start_low_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en liten grenseanalyse, ikke en ny scan.")
    lines.append("- Les utfallene som haleutfall, ikke som nye defect-arter.")
    lines.append("- Hvis denne runden virker, betyr det at residual- og probe-sporene er bedre forklart som en liten high-grensefamilie enn som generell boundary-mix.")
    return "\n".join(lines) + "\n"


def build_recommendation(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    status = next(row for row in diagnosis if str(row["diagnostic_family"]) == "terminal_probe_boundary_status")
    next_step = next(row for row in diagnosis if str(row["diagnostic_family"]) == "next_step")
    return "\n".join(
        [
            "# v0.15ao operativ anbefaling",
            "",
            f"- boundary-status: `{status['status']}`",
            f"- lesning: {status['note']}",
            f"- neste steg: `{next_step['status']}`",
            f"- begrunnelse: {next_step['note']}",
        ]
    ) + "\n"


def build_non_specialist_note(rows: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    by_seed = {int(row["run_seed"]): str(row["high_boundary_label"]) for row in rows}
    status = next(row for row in diagnosis if str(row["diagnostic_family"]) == "terminal_probe_boundary_status")
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15ao",
        "",
        "Denne runden sa pa en veldig liten grense inne i haleatferden: nar high-band dukker opp, blir det da vaerende, dør det ut igjen, eller kommer det bare for sent?",
        "",
        "Det viktigste vi fant er:",
        "",
        f"- seed `5002161`: `{by_seed.get(5002161, 'uklar')}`",
        f"- seed `5002220`: `{by_seed.get(5002220, 'uklar')}`",
        f"- seed `5002240`: `{by_seed.get(5002240, 'uklar')}`",
        f"- seed `5002221`: `{by_seed.get(5002221, 'uklar')}`",
        "",
        f"Den operative dommen er `{status['status']}`: {status['note']}",
        "",
        "Det nye her er at vi na kan skille mellom sen ekte high-hold, sen terminal probe og tidlig mislykket probe i stedet for a lese alt som samme slags boundary-uklarhet.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    v15an_rows_in = read_csv(IN_V15AN)
    v15aj_rows_in = read_csv(IN_V15AJ)
    snapshot_rows_in = read_csv(IN_SNAPSHOTS)
    target_rows = read_csv(IN_TARGET)

    rows = build_focus_rows(v15an_rows_in=v15an_rows_in, v15aj_rows_in=v15aj_rows_in, snapshot_rows_in=snapshot_rows_in)
    aggregate = aggregate_rows(rows)
    diagnosis = diagnosis_rows(target_rows=target_rows, rows=rows)
    report = build_report(target_rows=target_rows, rows=rows, aggregate=aggregate, diagnosis=diagnosis)
    recommendation = build_recommendation(diagnosis)
    non_specialist = build_non_specialist_note(rows, diagnosis)

    write_csv(DOC / "v15ao_terminal_probe_boundary_runs.csv", rows)
    write_csv(DOC / "v15ao_terminal_probe_boundary_aggregate.csv", aggregate)
    write_csv(DOC / "v15ao_terminal_probe_boundary_diagnosis.csv", diagnosis)
    write_csv(DOC / "v15ao_terminal_probe_boundary_target_summary.csv", list(target_rows))
    (DOC / "v15ao_terminal_probe_boundary_lab.md").write_text(report, encoding="utf-8")
    (DOC / "v0_15ao_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15ao.md").write_text(non_specialist, encoding="utf-8")


if __name__ == "__main__":
    main()
