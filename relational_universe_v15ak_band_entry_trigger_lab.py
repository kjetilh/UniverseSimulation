#!/usr/bin/env python3
"""v0.15ak band entry trigger lab for add_chord recurrence band.

This round follows v15aj. v15aj showed that the robust `early_fragment_lock`
main family has structured onset:

- many runs enter an immediate `low-mid` ladder
- some runs settle later into `mid-high`
- a minority remain in broader three-band churn

The next narrow question is:

can simple early-tail trigger features explain those onset types better than
the onset labels alone?

This round runs no new simulations. It analyzes the real `v15ai` snapshots and
`v15aj` onset labels.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v15_defect_lifetime_lab as v15


DOC = Path("Documentation")
IN_RUNS = DOC / "v15aj_early_lock_band_onset_runs.csv"
IN_SNAPSHOTS = DOC / "v15ai_early_lock_band_snapshots.csv"
IN_TARGET = DOC / "v15aj_early_lock_band_onset_target_summary.csv"

TARGET = 48
EARLY_WINDOW = 24
SOURCE_ORDER = {"anchor_main_family": 0, "holdout_revert": 1, "combined": 2}


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


def trigger_label(
    *,
    early_low_rate: float,
    early_mid_rate: float,
    early_high_rate: float,
    early_mean_component_count: float,
    early_mean_largest_fraction: float,
    early_switch_count: int,
) -> str:
    if early_high_rate >= 0.20 or early_mean_component_count >= 5.5:
        return "heavy_high_pressure_trigger"
    if (
        early_low_rate >= 0.75
        and early_mean_component_count <= 3.0
        and early_mean_largest_fraction >= 0.40
        and early_switch_count <= 3
    ):
        return "compact_low_entry_trigger"
    if early_mid_rate >= 0.70 and early_high_rate == 0.0 and early_switch_count <= 2:
        return "mid_loaded_low_mid_trigger"
    return "boundary_mixed_trigger"


def onset_family(onset_label: str) -> str:
    if onset_label in {"immediate_low-mid_ladder", "immediate_low_lock"}:
        return "immediate_low_family"
    if onset_label in {"mid_tail_mid-high_ladder", "late_tail_mid-high_ladder", "immediate_mid-high_ladder"}:
        return "mid_high_entry_family"
    if onset_label == "persistent_three_band_churn":
        return "persistent_churn_family"
    return "other"


def analyze_runs(
    *,
    run_rows_in: Sequence[Mapping[str, str]],
    snapshot_rows_in: Sequence[Mapping[str, str]],
) -> List[Dict[str, Any]]:
    snapshot_lookup: Dict[int, List[Dict[str, str]]] = defaultdict(list)
    for row in snapshot_rows_in:
        snapshot_lookup[int(row["run_seed"])].append(dict(row))

    out: List[Dict[str, Any]] = []
    for run_row in sorted(run_rows_in, key=lambda r: (SOURCE_ORDER.get(str(r["source_group"]), 99), int(r["run_seed"]))):
        run_seed = int(run_row["run_seed"])
        snapshots = sorted(snapshot_lookup[run_seed], key=lambda row: int(row["step"]))
        early_rows = snapshots[:EARLY_WINDOW]
        bands = [str(row["shell_count_band"]) for row in early_rows]
        early_low_rate = sum(1 for band in bands if band == "low") / max(1, len(bands))
        early_mid_rate = sum(1 for band in bands if band == "mid") / max(1, len(bands))
        early_high_rate = sum(1 for band in bands if band == "high") / max(1, len(bands))
        early_switch_count = sum(1 for a, b in zip(bands, bands[1:]) if a != b)
        early_mean_component_count = mean_defined(float(row["shell_component_count"]) for row in early_rows)
        early_mean_active_nodes = mean_defined(float(row["shell_active_nodes"]) for row in early_rows)
        early_mean_largest_fraction = mean_defined(float(row["largest_shell_component_fraction"]) for row in early_rows)
        early_mean_attachment_frac = mean_defined(float(row["shell_attachment_node_frac"]) for row in early_rows)
        early_mean_boundary_to_volume = mean_defined(float(row["shell_boundary_to_volume"]) for row in early_rows)
        label = trigger_label(
            early_low_rate=early_low_rate,
            early_mid_rate=early_mid_rate,
            early_high_rate=early_high_rate,
            early_mean_component_count=early_mean_component_count,
            early_mean_largest_fraction=early_mean_largest_fraction,
            early_switch_count=early_switch_count,
        )
        out.append(
            {
                "source_group": str(run_row["source_group"]),
                "placement": int(run_row["placement"]),
                "anchor_seed_delta": int(run_row["anchor_seed_delta"]),
                "holdout_seed_delta": int(run_row["holdout_seed_delta"]),
                "run_seed": run_seed,
                "support_signature": str(run_row["support_signature"]),
                "onset_label": str(run_row["onset_label"]),
                "onset_family": onset_family(str(run_row["onset_label"])),
                "band_lock_label": str(run_row["band_lock_label"]),
                "early_low_rate": early_low_rate,
                "early_mid_rate": early_mid_rate,
                "early_high_rate": early_high_rate,
                "early_mean_component_count": early_mean_component_count,
                "early_mean_active_nodes": early_mean_active_nodes,
                "early_mean_largest_fraction": early_mean_largest_fraction,
                "early_mean_attachment_frac": early_mean_attachment_frac,
                "early_mean_boundary_to_volume": early_mean_boundary_to_volume,
                "early_switch_count": int(early_switch_count),
                "trigger_label": label,
            }
        )
    return out


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    def add_group(group_type: str, group_value: str, group_rows: Sequence[Mapping[str, Any]]) -> None:
        if not group_rows:
            return
        out.append(
            {
                "group_type": group_type,
                "group_value": group_value,
                "n_runs": len(group_rows),
                "compact_low_entry_rate": mean_defined(1.0 if str(row["trigger_label"]) == "compact_low_entry_trigger" else 0.0 for row in group_rows),
                "mid_loaded_low_mid_rate": mean_defined(1.0 if str(row["trigger_label"]) == "mid_loaded_low_mid_trigger" else 0.0 for row in group_rows),
                "boundary_mixed_rate": mean_defined(1.0 if str(row["trigger_label"]) == "boundary_mixed_trigger" else 0.0 for row in group_rows),
                "heavy_high_pressure_rate": mean_defined(1.0 if str(row["trigger_label"]) == "heavy_high_pressure_trigger" else 0.0 for row in group_rows),
                "mean_early_low_rate": mean_defined(safe_float(row["early_low_rate"]) for row in group_rows),
                "mean_early_mid_rate": mean_defined(safe_float(row["early_mid_rate"]) for row in group_rows),
                "mean_early_high_rate": mean_defined(safe_float(row["early_high_rate"]) for row in group_rows),
                "mean_early_component_count": mean_defined(safe_float(row["early_mean_component_count"]) for row in group_rows),
                "mean_early_largest_fraction": mean_defined(safe_float(row["early_mean_largest_fraction"]) for row in group_rows),
                "mean_early_switch_count": mean_defined(safe_float(row["early_switch_count"]) for row in group_rows),
            }
        )

    add_group("source_group", "combined", rows)
    for source_group in ("anchor_main_family", "holdout_revert"):
        add_group("source_group", source_group, [row for row in rows if str(row["source_group"]) == source_group])
    for onset in ("immediate_low_family", "mid_high_entry_family", "persistent_churn_family"):
        add_group("onset_family", onset, [row for row in rows if str(row["onset_family"]) == onset])
    return out


def diagnosis_rows(
    *,
    target_rows: Sequence[Mapping[str, str]],
    aggregate_rows_in: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_rows if int(row["target_nodes"]) == TARGET)
    low_family = next(row for row in aggregate_rows_in if str(row["group_type"]) == "onset_family" and str(row["group_value"]) == "immediate_low_family")
    mid_high_family = next(row for row in aggregate_rows_in if str(row["group_type"]) == "onset_family" and str(row["group_value"]) == "mid_high_entry_family")
    churn_family = next(row for row in aggregate_rows_in if str(row["group_type"]) == "onset_family" and str(row["group_value"]) == "persistent_churn_family")

    if (
        safe_float(low_family["compact_low_entry_rate"]) >= 0.80
        and (safe_float(mid_high_family["boundary_mixed_rate"]) + safe_float(mid_high_family["heavy_high_pressure_rate"])) >= 0.80
        and safe_float(churn_family["boundary_mixed_rate"]) >= 0.75
    ):
        status = "entry_trigger_map_partly_supported"
        note = "Tidlig hale skiller immediate `low-mid` ganske rent fra resten: disse runene er nesten alltid kompakte low-entry-caser, mens `mid-high` og vedvarende churn for det meste lever i en boundary/heavy-trigger-sone."
        next_step = "split_boundary_zone"
        next_note = "Neste steg bor forklare hva som deler boundary-zonen i faktisk `mid-high`-entry mot vedvarende tre-band-churn."
    elif safe_float(low_family["compact_low_entry_rate"]) >= 0.70:
        status = "low_entry_trigger_supported"
        note = "Vi kan forklare immediate `low-mid` ganske godt som kompakt low-entry, men resten av onset-familiene er fortsatt for blandet."
        next_step = "probe_non_low_zone"
        next_note = "Neste steg bor fokusere bare pa run uten kompakt low-entry."
    else:
        status = "entry_trigger_map_still_mixed"
        note = "Tidlig hale gir ikke et rent triggerkart for onset-familiene ennå."
        next_step = "pivot_trigger_observable"
        next_note = "Neste steg bor bytte triggerobservabel, ikke presse disse tersklene hardere."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": (
                "Startstorrelsen er rent separert, og denne runden bygger bare pa ekte `v15ai`- og `v15aj`-data."
                if size_clean
                else "Storrelsesseparasjonen er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "entry_trigger_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "family_split_note",
            "status": "descriptive",
            "note": (
                f"Immediate low-family har compact-low-rate {fmt(low_family['compact_low_entry_rate'])}, "
                f"mid-high-family har boundary/heavy-rate {fmt(safe_float(mid_high_family['boundary_mixed_rate']) + safe_float(mid_high_family['heavy_high_pressure_rate']))}, "
                f"og churn-family har boundary-rate {fmt(churn_family['boundary_mixed_rate'])}."
            ),
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
    aggregate_rows_in: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    source_rows = [row for row in aggregate_rows_in if str(row["group_type"]) == "source_group"]
    onset_rows = [row for row in aggregate_rows_in if str(row["group_type"]) == "onset_family"]
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15ak: band entry trigger lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om enkle tidlige hale-features kan forklare onset-typene fra `v15aj`, spesielt skillet mellom immediate `low-mid`, senere `mid-high`, og vedvarende tre-band-churn.")
    lines.append("")
    lines.append("## Startstorrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_rows:
        if int(row["target_nodes"]) != TARGET:
            continue
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Source groups")
    lines.append("")
    lines.append("| group | n | compact low | mid-loaded low-mid | boundary mixed | heavy high | early low | early mid | early high | switches |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(source_rows, key=lambda r: SOURCE_ORDER.get(str(r["group_value"]), 99)):
        lines.append(
            f"| {row['group_value']} | {int(row['n_runs'])} | {fmt(row['compact_low_entry_rate'])} | {fmt(row['mid_loaded_low_mid_rate'])} | {fmt(row['boundary_mixed_rate'])} | {fmt(row['heavy_high_pressure_rate'])} | {fmt(row['mean_early_low_rate'])} | {fmt(row['mean_early_mid_rate'])} | {fmt(row['mean_early_high_rate'])} | {fmt(row['mean_early_switch_count'])} |"
        )
    lines.append("")
    lines.append("## Per onset family")
    lines.append("")
    lines.append("| onset family | n | compact low | mid-loaded low-mid | boundary mixed | heavy high | mean comp | largest frac | switches |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in onset_rows:
        lines.append(
            f"| {row['group_value']} | {int(row['n_runs'])} | {fmt(row['compact_low_entry_rate'])} | {fmt(row['mid_loaded_low_mid_rate'])} | {fmt(row['boundary_mixed_rate'])} | {fmt(row['heavy_high_pressure_rate'])} | {fmt(row['mean_early_component_count'])} | {fmt(row['mean_early_largest_fraction'])} | {fmt(row['mean_early_switch_count'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en smal forklaringsrunde inne i samme hovedfamilie og samme halevindu.")
    lines.append("- `compact_low_entry_trigger` betyr tidlig lav last, lavt komponentnivaa og rolig switching.")
    lines.append("- `boundary_mixed_trigger` betyr at runet starter i en blandet grensesone der tidlig hale ikke ennå skiller rent mellom `mid-high`-entry og vedvarende churn.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ak band entry trigger lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15ak_band_entry_trigger_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ak_band_entry_trigger_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ak_band_entry_trigger_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15ak_band_entry_trigger_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ak_band_entry_trigger_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ak_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ak.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_rows_in = read_csv(IN_RUNS)
    snapshot_rows_in = read_csv(IN_SNAPSHOTS)
    target_rows = read_csv(IN_TARGET)

    analyzed_rows = analyze_runs(
        run_rows_in=run_rows_in,
        snapshot_rows_in=snapshot_rows_in,
    )
    aggregate = aggregate_rows(analyzed_rows)
    diagnosis = diagnosis_rows(
        target_rows=target_rows,
        aggregate_rows_in=aggregate,
    )
    report_md = build_report(
        target_rows=target_rows,
        aggregate_rows_in=aggregate,
        diagnosis=diagnosis,
    )
    op_md = "\n".join(
        [
            "# v0.15ak operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en triggertest for onset-typene fra `v15aj`, ikke som nye defect-arter.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15ak",
            "",
            "Forrige runde viste at hale-onseten har struktur. Denne runden ser pa de aller tidligste snapshottene i halen for a se om de peker mot ulike inngangstyper.",
            "",
            "Målet er a finne ut om run som gaar rett inn i et rolig `low-mid`-monster allerede ser annerledes ut tidlig, sammenlignet med run som senere sklir opp i tyngre `mid-high`-monster eller blir igjen i mer blandet churn.",
        ]
    ) + "\n"

    write_csv(args.out_runs_csv, analyzed_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_target_csv, target_rows)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
