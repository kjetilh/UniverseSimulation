#!/usr/bin/env python3
"""v0.15bp add_chord scale-break explainer.

Explains the negative v15bo result:
why 48/p2 does not cleanly transfer to 96 even though v15bn found a weak
candidate and v15bo tested that candidate against a nearby control.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

import relational_universe_v15_defect_lifetime_lab as v15


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def classify_break(anchor: Mapping[str, str], other: Mapping[str, str]) -> Dict[str, Any]:
    exact_gap = safe_float(other["mean_full_exact_return_rate"]) - safe_float(anchor["mean_full_exact_return_rate"])
    coarse_gap = safe_float(other["mean_full_coarse_return_rate"]) - safe_float(anchor["mean_full_coarse_return_rate"])
    core_gap = safe_float(other["mean_core_share_of_union"]) - safe_float(anchor["mean_core_share_of_union"])
    shell_gap = safe_float(other["mean_shell_share_of_union"]) - safe_float(anchor["mean_shell_share_of_union"])
    rare_gap = safe_float(other["mean_rare_share_of_union"]) - safe_float(anchor["mean_rare_share_of_union"])
    spectral_rank = int(other["spectral_rank_nontrivial"])
    best_metric = str(other["best_nontrivial_metric"])

    if spectral_rank == 1 and shell_gap > 0.15 and rare_gap > 0.08:
        break_label = "spectral_without_geometry_hold"
    elif spectral_rank != 1 and coarse_gap > -0.08 and core_gap > -0.30:
        break_label = "geometry_without_spectral_hold"
    elif coarse_gap <= -0.10 and shell_gap > 0.15:
        break_label = "broad_geometry_break"
    else:
        break_label = "mixed_scale_break"

    return {
        "other_profile": str(other["profile_label"]),
        "other_role": str(other["role"]),
        "other_best_nontrivial_metric": best_metric,
        "other_spectral_rank_nontrivial": spectral_rank,
        "exact_gap_vs_anchor": exact_gap,
        "coarse_gap_vs_anchor": coarse_gap,
        "core_gap_vs_anchor": core_gap,
        "shell_gap_vs_anchor": shell_gap,
        "rare_gap_vs_anchor": rare_gap,
        "break_label": break_label,
    }


def diagnosis_rows(class_rows: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows = list(class_rows)
    candidate = next(row for row in rows if str(row["other_profile"]) == "candidate_96_p3")
    control = next(row for row in rows if str(row["other_profile"]) == "control_96_p1")

    if (
        str(candidate["break_label"]) == "spectral_without_geometry_hold"
        and str(control["break_label"]) == "geometry_without_spectral_hold"
    ):
        status = "split_scale_break_supported"
        note = (
            "96/p3 holder spectral rang, men glipper geometrisk; 96/p1 holder bedre coarse-geometri, men glipper spectralt. "
            "Skalabruddet ser derfor ut som en delt breaking av samme familiekrav."
        )
        next_step = "pause_scale_transfer_claim"
        next_note = "Neste steg bor ikke presse mer pa samme scale-transfer-claim uten en ny coarse observabel eller et annet carrier-spor."
    else:
        status = "scale_break_still_mixed"
        note = "Skalabruddet er ikke helt delt i en ren spectral-vs-geometry-splitt, sa forklaringen er fortsatt delvis blandet."
        next_step = "one_more_break_observable"
        next_note = "Neste steg bor vaere en ny observabel for skalabrudd, ikke mer av samme tie-break."

    return [
        {
            "diagnostic_family": "scale_break",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(class_rows: List[Mapping[str, Any]], diagnosis: List[Mapping[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bp: add_chord scale-break explainer")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden forklarer hvorfor 48/p2 ikke holder som en ren liten skalafamilie ved 96 etter v15bo.")
    lines.append("")
    lines.append("## Bruddtyper mot ankeret")
    lines.append("")
    lines.append("| profile | role | break label | exact gap | coarse gap | core gap | shell gap | rare gap | spectral rank | best metric |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in class_rows:
        lines.append(
            f"| {row['other_profile']} | {row['other_role']} | {row['break_label']} | {fmt(row['exact_gap_vs_anchor'])} | {fmt(row['coarse_gap_vs_anchor'])} | {fmt(row['core_gap_vs_anchor'])} | {fmt(row['shell_gap_vs_anchor'])} | {fmt(row['rare_gap_vs_anchor'])} | {int(row['other_spectral_rank_nontrivial'])} | {row['other_best_nontrivial_metric']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en forklaringsrunde, ikke en ny simulering.")
    lines.append("- Poenget er a lokalisere om 48->96-bruddet sitter i spectral rang, coarse geometri eller begge.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bp add_chord scale-break explainer.")
    p.add_argument("--in-aggregate", type=str, default="Documentation/v15bo_add_chord_scale_jump_holdout_aggregate.csv")
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15bp_add_chord_scale_break_rows.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bp_add_chord_scale_break_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bp_add_chord_scale_break_explainer.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bp_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bp.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    aggregate = read_csv(args.in_aggregate)
    anchor = next(row for row in aggregate if str(row["profile_label"]) == "anchor_48_p2")
    others = [row for row in aggregate if str(row["profile_label"]) != "anchor_48_p2"]
    class_rows = [classify_break(anchor, row) for row in others]
    diagnosis = diagnosis_rows(class_rows)
    report_md = build_report(class_rows, diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bp operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en presisering av hvorfor scale-transfer ikke holdt, ikke som en ny negativ totaldom over add_chord-sporet.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bp",
            "",
            "Denne runden forklarer hvorfor den lille 48-familien ikke ble en ren 96-familie.",
            "",
            "Kort sagt: den ene 96-kandidaten holder den spektrale siden bedre, mens den andre holder den grove formen bedre. Ingen av dem holder begge deler samtidig.",
        ]
    ) + "\n"

    write_csv(args.out_rows_csv, class_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
