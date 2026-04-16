#!/usr/bin/env python3
"""v0.15bg local_swap shell-drag decomposition.

This round does not run new simulations. It decomposes the `p3 > p2`
shell-drag side from v15bf to test whether that drag is driven mainly by
ordinary shell width or by rare-load inflation.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

import relational_universe_v15_defect_lifetime_lab as v15


RUNS_CSV = Path("Documentation/v15aw_local_swap_core_shell_runs.csv")
TARGET = 96
GROWTH_SEED = 202


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def placement_rows(run_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in run_rows:
        if int(row["target_nodes"]) != TARGET or int(row["growth_seed"]) != GROWTH_SEED:
            continue
        out.append(
            {
                "placement": int(row["placement"]),
                "label": str(row["core_shell_label"]),
                "coarse_return": safe_float(row["full_coarse_return_rate"]),
                "core_share": safe_float(row["core_share_of_union"]),
                "shell_share": safe_float(row["shell_share_of_union"]),
                "rare_share": safe_float(row["rare_share_of_union"]),
                "shell_plus_rare_share": safe_float(row["shell_share_of_union"]) + safe_float(row["rare_share_of_union"]),
                "tail_union_nodes": int(row["tail_union_nodes"]),
                "mean_tail_damage_nodes": safe_float(row["mean_tail_damage_nodes"]),
                "tail_density": safe_float(row["mean_tail_damage_nodes"]) / max(1.0, safe_float(row["tail_union_nodes"])),
            }
        )
    return sorted(out, key=lambda r: int(r["placement"]))


def decomposition_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by = {int(row["placement"]): row for row in rows}
    p2 = by[2]
    p3 = by[3]
    shell_gap = safe_float(p2["shell_share"]) - safe_float(p3["shell_share"])
    rare_gap = safe_float(p2["rare_share"]) - safe_float(p3["rare_share"])
    shell_burden_gap = safe_float(p2["shell_plus_rare_share"]) - safe_float(p3["shell_plus_rare_share"])
    rare_fraction = rare_gap / shell_burden_gap if shell_burden_gap > 0 else float("nan")
    shell_fraction = shell_gap / shell_burden_gap if shell_burden_gap > 0 else float("nan")
    if rare_fraction >= 0.75 and shell_gap <= 0.01:
        drag_mode = "rare_loaded_shell_drag"
        note = "Shell-draget skyldes nesten helt oppblåst rare-andel, ikke bredere ordinær shell."
    elif shell_fraction >= 0.50:
        drag_mode = "broad_shell_drag"
        note = "Shell-draget bæres i stor grad av bredere ordinær shell."
    else:
        drag_mode = "mixed_shell_drag"
        note = "Shell-draget er fortsatt for blandet til å kalles rent rare-drevet eller shell-drevet."
    return [
        {
            "pair_label": "p3_vs_p2",
            "winner": 3,
            "loser": 2,
            "winner_label": str(p3["label"]),
            "loser_label": str(p2["label"]),
            "shell_gap_loser_minus_winner": shell_gap,
            "rare_gap_loser_minus_winner": rare_gap,
            "shell_burden_gap_loser_minus_winner": shell_burden_gap,
            "rare_fraction_of_shell_drag": rare_fraction,
            "shell_fraction_of_shell_drag": shell_fraction,
            "tail_union_gap_loser_minus_winner": int(p2["tail_union_nodes"]) - int(p3["tail_union_nodes"]),
            "tail_density_gap_winner_minus_loser": safe_float(p3["tail_density"]) - safe_float(p2["tail_density"]),
            "coarse_return_gap_winner_minus_loser": safe_float(p3["coarse_return"]) - safe_float(p2["coarse_return"]),
            "drag_mode": drag_mode,
            "note": note,
        }
    ]


def diagnosis_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    row = rows[0]
    if str(row["drag_mode"]) == "rare_loaded_shell_drag":
        status = "rare_loaded_shell_drag_supported"
        note = "Den balanserte p3 > p2-overgangen ser ikke ut som bredere shell i seg selv; taperen bærer nesten hele shell-draget som oppblåst rare-last."
        next_step = "explain_rare_load_trigger"
    else:
        status = "shell_drag_not_yet_split"
        note = "Shell-drag-siden lot seg ikke deles rent i rare-vs-shell i denne observabelen."
        next_step = "change_shell_observable"
    return [
        {
            "diagnostic_family": "shell_drag_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": "Neste steg bør forklare hva som avgjør om rare-last blåses opp i den dissipative p2-retningen.",
        },
    ]


def build_report(*, placements: Sequence[Mapping[str, Any]], rows: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bg: local_swap shell-drag decomposition")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden åpner `retention_plus_shell_drag` fra `v15bf` for å se om shell-draget faktisk bæres av ordinær shell-bredde eller av rare-last.")
    lines.append("")
    lines.append("## Relevant placements")
    lines.append("")
    lines.append("| placement | label | coarse return | shell share | rare share | shell+rare | tail union | tail density |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in placements:
        if int(row["placement"]) not in (2, 3):
            continue
        lines.append(
            f"| {int(row['placement'])} | {row['label']} | {fmt(row['coarse_return'])} | {fmt(row['shell_share'])} | {fmt(row['rare_share'])} | {fmt(row['shell_plus_rare_share'])} | {int(row['tail_union_nodes'])} | {fmt(row['tail_density'])} |"
        )
    lines.append("")
    lines.append("## Shell-drag decomposition")
    lines.append("")
    lines.append("| pair | shell gap | rare gap | shell-burden gap | rare fraction | shell fraction | tail-union gap | density gap | mode |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {row['pair_label']} | {fmt(row['shell_gap_loser_minus_winner'])} | {fmt(row['rare_gap_loser_minus_winner'])} | {fmt(row['shell_burden_gap_loser_minus_winner'])} | {fmt(row['rare_fraction_of_shell_drag'])} | {fmt(row['shell_fraction_of_shell_drag'])} | {int(row['tail_union_gap_loser_minus_winner'])} | {fmt(row['tail_density_gap_winner_minus_loser'])} | {row['drag_mode']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en ren forklaringsrunde på eksisterende data, ikke en ny simulering.")
    lines.append("- Les dette som en lokal dekomponering av `p3 > p2`-overgangen, ikke som en generell lov for alle local_swap-tilfeller.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bg local_swap shell-drag decomposition.")
    p.add_argument("--in-runs-csv", type=str, default=str(RUNS_CSV))
    p.add_argument("--out-placements-csv", type=str, default="Documentation/v15bg_local_swap_shell_drag_placements.csv")
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15bg_local_swap_shell_drag_rows.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bg_local_swap_shell_drag_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bg_local_swap_shell_drag_decomposition.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bg_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bg.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    placements = placement_rows(read_csv(Path(args.in_runs_csv)))
    rows = decomposition_rows(placements)
    diagnosis = diagnosis_rows(rows)
    report_md = build_report(placements=placements, rows=rows, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bg operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en dekomponering av shell-drag-siden fra `v15bf`, ikke som en ny bred scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bg",
            "",
            "Denne runden prøver å skille to ting som ellers lett flyter sammen: vanlig randbredde og mer uregelmessig rare-last.",
            "",
            "Poenget er å se om den svakere lokale modusen taper fordi den har mer rand generelt, eller fordi den fylles opp av den mer ustabile rare-delen av halen.",
        ]
    ) + "\n"
    write_csv(args.out_placements_csv, placements)
    write_csv(args.out_rows_csv, rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
