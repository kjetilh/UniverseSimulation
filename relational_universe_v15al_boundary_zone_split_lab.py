#!/usr/bin/env python3
"""v0.15al boundary zone split lab for add_chord recurrence band.

This round follows v15ak. v15ak showed that immediate `low-mid` is almost
always a compact low-entry case, but the non-low runs still lived in one shared
boundary/heavy zone.

The next narrow question is:

can that boundary zone itself be split into a small number of later early-tail
profiles, and does that give real new information about `mid-high` entry versus
persistent churn?

This round runs no new simulations. It analyzes the real `v15ai` snapshots and
the boundary-tagged runs from `v15ak`.
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
IN_RUNS = DOC / "v15ak_band_entry_trigger_runs.csv"
IN_SNAPSHOTS = DOC / "v15ai_early_lock_band_snapshots.csv"
IN_TARGET = DOC / "v15ak_band_entry_trigger_target_summary.csv"

TARGET = 48
BOUNDARY_WINDOW = 72
LAST_WINDOW = 24


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


def boundary_label(
    *,
    peak_high_rate_72: float,
    high_last24_rate_72: float,
    mid_last24_rate_72: float,
    low_last24_rate_72: float,
    mean_component_count_72: float,
) -> str:
    if high_last24_rate_72 >= 0.50 or peak_high_rate_72 >= 0.30 or mean_component_count_72 >= 5.50:
        return "late_high_rise_boundary"
    if high_last24_rate_72 <= 0.05 and mid_last24_rate_72 >= 0.75 and low_last24_rate_72 <= 0.25:
        return "mid_plateau_boundary"
    return "residual_boundary"


def analyze_runs(
    *,
    run_rows_in: Sequence[Mapping[str, str]],
    snapshot_rows_in: Sequence[Mapping[str, str]],
) -> List[Dict[str, Any]]:
    snapshot_lookup: Dict[int, List[Dict[str, str]]] = defaultdict(list)
    for row in snapshot_rows_in:
        snapshot_lookup[int(row["run_seed"])].append(dict(row))

    out: List[Dict[str, Any]] = []
    for run_row in run_rows_in:
        if str(run_row["trigger_label"]) != "boundary_mixed_trigger":
            continue
        run_seed = int(run_row["run_seed"])
        snapshots = sorted(snapshot_lookup[run_seed], key=lambda row: int(row["step"]))[:BOUNDARY_WINDOW]
        bands = [str(row["shell_count_band"]) for row in snapshots]
        last = bands[-LAST_WINDOW:]
        peak_high_rate_72 = max(
            (sum(1 for band in bands[:idx] if band == "high") / idx) for idx in range(1, len(bands) + 1)
        )
        high_last24_rate_72 = sum(1 for band in last if band == "high") / max(1, len(last))
        mid_last24_rate_72 = sum(1 for band in last if band == "mid") / max(1, len(last))
        low_last24_rate_72 = sum(1 for band in last if band == "low") / max(1, len(last))
        mean_component_count_72 = mean_defined(float(row["shell_component_count"]) for row in snapshots)
        mean_active_nodes_72 = mean_defined(float(row["shell_active_nodes"]) for row in snapshots)
        mean_largest_fraction_72 = mean_defined(float(row["largest_shell_component_fraction"]) for row in snapshots)
        mean_attachment_frac_72 = mean_defined(float(row["shell_attachment_node_frac"]) for row in snapshots)
        mean_boundary_to_volume_72 = mean_defined(float(row["shell_boundary_to_volume"]) for row in snapshots)
        switch_count_72 = sum(1 for a, b in zip(bands, bands[1:]) if a != b)
        label = boundary_label(
            peak_high_rate_72=peak_high_rate_72,
            high_last24_rate_72=high_last24_rate_72,
            mid_last24_rate_72=mid_last24_rate_72,
            low_last24_rate_72=low_last24_rate_72,
            mean_component_count_72=mean_component_count_72,
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
                "onset_family": str(run_row["onset_family"]),
                "trigger_label": str(run_row["trigger_label"]),
                "peak_high_rate_72": peak_high_rate_72,
                "high_last24_rate_72": high_last24_rate_72,
                "mid_last24_rate_72": mid_last24_rate_72,
                "low_last24_rate_72": low_last24_rate_72,
                "mean_component_count_72": mean_component_count_72,
                "mean_active_nodes_72": mean_active_nodes_72,
                "mean_largest_fraction_72": mean_largest_fraction_72,
                "mean_attachment_frac_72": mean_attachment_frac_72,
                "mean_boundary_to_volume_72": mean_boundary_to_volume_72,
                "switch_count_72": int(switch_count_72),
                "boundary_split_label": label,
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
                "late_high_rise_rate": mean_defined(1.0 if str(row["boundary_split_label"]) == "late_high_rise_boundary" else 0.0 for row in group_rows),
                "mid_plateau_rate": mean_defined(1.0 if str(row["boundary_split_label"]) == "mid_plateau_boundary" else 0.0 for row in group_rows),
                "residual_rate": mean_defined(1.0 if str(row["boundary_split_label"]) == "residual_boundary" else 0.0 for row in group_rows),
                "mean_peak_high_rate_72": mean_defined(safe_float(row["peak_high_rate_72"]) for row in group_rows),
                "mean_high_last24_rate_72": mean_defined(safe_float(row["high_last24_rate_72"]) for row in group_rows),
                "mean_mid_last24_rate_72": mean_defined(safe_float(row["mid_last24_rate_72"]) for row in group_rows),
                "mean_low_last24_rate_72": mean_defined(safe_float(row["low_last24_rate_72"]) for row in group_rows),
                "mean_component_count_72": mean_defined(safe_float(row["mean_component_count_72"]) for row in group_rows),
                "mean_largest_fraction_72": mean_defined(safe_float(row["mean_largest_fraction_72"]) for row in group_rows),
                "mean_switch_count_72": mean_defined(safe_float(row["switch_count_72"]) for row in group_rows),
            }
        )

    add_group("all_boundary", "combined", rows)
    for family in ("mid_high_entry_family", "persistent_churn_family"):
        add_group("onset_family", family, [row for row in rows if str(row["onset_family"]) == family])
    for label in ("late_high_rise_boundary", "mid_plateau_boundary", "residual_boundary"):
        add_group("boundary_label", label, [row for row in rows if str(row["boundary_split_label"]) == label])
    return out


def diagnosis_rows(
    *,
    target_rows: Sequence[Mapping[str, str]],
    aggregate_rows_in: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_rows if int(row["target_nodes"]) == TARGET)
    mid_high = next(row for row in aggregate_rows_in if str(row["group_type"]) == "onset_family" and str(row["group_value"]) == "mid_high_entry_family")
    churn = next(row for row in aggregate_rows_in if str(row["group_type"]) == "onset_family" and str(row["group_value"]) == "persistent_churn_family")

    if (
        safe_float(mid_high["late_high_rise_rate"]) >= 0.50
        and safe_float(churn["mid_plateau_rate"]) >= 0.50
    ):
        status = "boundary_zone_partly_split"
        note = "Boundary-sonen er ikke ren, men den deler seg i to nyttige grener: `mid-high` havner oftere i late high-rise, mens vedvarende churn oftere blir i en mid-plateau-gren."
        next_step = "explain_overlap_cases"
        next_note = "Neste steg bor forklare overlap-caseene: ett churn-run som ogsa blir high-rise, og ett mid-high-run som blir mid-plateau."
    else:
        status = "boundary_zone_still_mixed"
        note = "Boundary-sonen blir ikke ren nok av denne andre observabelen heller."
        next_step = "pivot_again"
        next_note = "Neste steg bor bytte observabel eller fokusere pa konkrete overlap-case i stedet for ny aggregering."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": (
                "Startstorrelsen er rent separert, og denne runden bygger bare pa ekte `v15ai`, `v15aj` og `v15ak`-data."
                if size_clean
                else "Storrelsesseparasjonen er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "boundary_split_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "family_split_note",
            "status": "descriptive",
            "note": (
                f"`mid_high_entry_family` har late-high-rise-rate {fmt(mid_high['late_high_rise_rate'])}, "
                f"mens `persistent_churn_family` har mid-plateau-rate {fmt(churn['mid_plateau_rate'])}."
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
    onset_rows = [row for row in aggregate_rows_in if str(row["group_type"]) == "onset_family"]
    label_rows = [row for row in aggregate_rows_in if str(row["group_type"]) == "boundary_label"]
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15al: boundary zone split lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden prover a dele boundary-sonen fra `v15ak` i noen fa senere tidlige-hale profiler, for a se om `mid-high`-entry og vedvarende churn skiller lag bedre der.")
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
    lines.append("## Per onset family")
    lines.append("")
    lines.append("| onset family | n | late high-rise | mid plateau | residual | peak high | high last24 | comp72 | switches72 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in onset_rows:
        lines.append(
            f"| {row['group_value']} | {int(row['n_runs'])} | {fmt(row['late_high_rise_rate'])} | {fmt(row['mid_plateau_rate'])} | {fmt(row['residual_rate'])} | {fmt(row['mean_peak_high_rate_72'])} | {fmt(row['mean_high_last24_rate_72'])} | {fmt(row['mean_component_count_72'])} | {fmt(row['mean_switch_count_72'])} |"
        )
    lines.append("")
    lines.append("## Per boundary label")
    lines.append("")
    lines.append("| boundary label | n | high last24 | mid last24 | low last24 | comp72 | largest72 | switches72 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in label_rows:
        lines.append(
            f"| {row['group_value']} | {int(row['n_runs'])} | {fmt(row['mean_high_last24_rate_72'])} | {fmt(row['mean_mid_last24_rate_72'])} | {fmt(row['mean_low_last24_rate_72'])} | {fmt(row['mean_component_count_72'])} | {fmt(row['mean_largest_fraction_72'])} | {fmt(row['mean_switch_count_72'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en smal oppfolging av boundary-sonen, ikke en ny bred familie-scan.")
    lines.append("- `late_high_rise_boundary` betyr at hoy-band-trykk bygger seg opp tydelig i de forste 72 hale-snapshottene.")
    lines.append("- `mid_plateau_boundary` betyr at runet holder seg mest pa et roligere mid-platå uten tydelig high-rise i denne fasen.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15al boundary zone split lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15al_boundary_zone_split_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15al_boundary_zone_split_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15al_boundary_zone_split_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15al_boundary_zone_split_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15al_boundary_zone_split_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15al_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15al.md")
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
            "# v0.15al operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en smal splitting av boundary-sonen fra `v15ak`, ikke som nye defect-arter.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15al",
            "",
            "Forrige runde viste at de ikke-lave runene fortsatt levde i en felles boundary-sone tidlig i halen.",
            "",
            "Denne runden ser litt lenger frem i den tidlige halen for a se om denne sonen faktisk deler seg i noen fa tydeligere utviklingsprofiler.",
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
