#!/usr/bin/env python3
"""v0.15bf local_swap gap-asymmetry explainer.

This round does not run new simulations. It explains why the two neighboring
gaps inside the v15bd/v15be trigger-axis ordering are not of the same type:
`p1 > p3` versus `p3 > p2`.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

import relational_universe_v15_defect_lifetime_lab as v15


PLACEMENTS_CSV = Path("Documentation/v15bd_local_swap_trigger_axis_placements.csv")
PAIRS_CSV = Path("Documentation/v15be_local_swap_trigger_axis_pairs.csv")


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


def placement_map(rows: Sequence[Mapping[str, str]]) -> Dict[int, Dict[str, Any]]:
    out: Dict[int, Dict[str, Any]] = {}
    for row in rows:
        out[int(row["placement"])] = {
            "placement": int(row["placement"]),
            "shell_plus_rare_share": safe_float(row["shell_plus_rare_share"]),
            "tail_density": safe_float(row["tail_density"]),
            "core_share": safe_float(row["core_share_of_union"]),
            "coarse_return": safe_float(row["full_coarse_return_rate"]),
            "core_to_shell": safe_float(row["core_to_shell_ratio"]),
        }
    return out


def asymmetry_rows(
    pair_rows: Sequence[Mapping[str, str]],
    placements: Mapping[int, Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in pair_rows:
        winner = int(row["winner"])
        loser = int(row["loser"])
        win = placements[winner]
        lose = placements[loser]
        coarse_gap = safe_float(row["coarse_return_gap"])
        core_gap = safe_float(row["core_to_shell_gap"])
        density_gap = safe_float(row["tail_density_gap"])
        shell_burden_gap = safe_float(lose["shell_plus_rare_share"]) - safe_float(win["shell_plus_rare_share"])
        core_share_gap = safe_float(win["core_share"]) - safe_float(lose["core_share"])
        if safe_float(row["core_share_of_axis_gap"]) >= 0.60 and density_gap < 0.10:
            gap_mode = "core_shape_separation"
            note = "Gapet drives mest av sterkere kjerne-forhold, mens tail-densiteten skiller mindre."
        elif safe_float(row["coarse_share_of_axis_gap"]) >= 0.45 and density_gap >= 0.10 and shell_burden_gap >= 0.08:
            gap_mode = "retention_plus_shell_drag"
            note = "Gapet leses best som en blanding av svakere retention og tydelig større shell-byrde hos taperen."
        else:
            gap_mode = "mixed_gap_family"
            note = "Gapet er fortsatt for blandet til å få en skarp lokal mekanismelesning."
        out.append(
            {
                "pair_label": row["pair_label"],
                "winner": winner,
                "loser": loser,
                "coarse_return_gap": coarse_gap,
                "core_to_shell_gap": core_gap,
                "tail_density_gap": density_gap,
                "core_share_gap": core_share_gap,
                "shell_burden_gap": shell_burden_gap,
                "gap_mode": gap_mode,
                "note": note,
            }
        )
    return out


def diagnosis_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_pair = {str(row["pair_label"]): row for row in rows}
    if (
        str(by_pair["p1_vs_p3"]["gap_mode"]) == "core_shape_separation"
        and str(by_pair["p3_vs_p2"]["gap_mode"]) == "retention_plus_shell_drag"
    ):
        status = "neighbor_gap_asymmetry_supported"
        note = "De to nabogapene er ikke samme type: øvre gap er mer ren kjerneform-separasjon, nedre gap er mer en blandet retention+shell-drag-overgang."
        next_step = "explain_shell_drag_side"
    else:
        status = "neighbor_gap_asymmetry_not_yet"
        note = "Nabogapene lot seg ikke splitte rent nok i denne observabelen."
        next_step = "change_local_observable"
    return [
        {
            "diagnostic_family": "gap_asymmetry_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": "Neste steg bør gå på shell-drag-siden av den balanserte overgangen, ikke lete etter enda en ny totalakse.",
        },
    ]


def build_report(*, rows: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bf: local_swap gap asymmetry explainer")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden spør om `p1 > p3` og `p3 > p2` faktisk er to ulike typer lokale gap inne i den samme triggeraksen.")
    lines.append("")
    lines.append("## Pair asymmetry")
    lines.append("")
    lines.append("| pair | coarse gap | core/shell gap | tail density gap | core-share gap | shell burden gap | mode |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {row['pair_label']} | {fmt(row['coarse_return_gap'])} | {fmt(row['core_to_shell_gap'])} | {fmt(row['tail_density_gap'])} | {fmt(row['core_share_gap'])} | {fmt(row['shell_burden_gap'])} | {row['gap_mode']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en forklaringsrunde på eksisterende data, ikke en ny simulering.")
    lines.append("- Les dette som lokal struktur inne i growth_seed-202-splittelsen, ikke som en global local_swap-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bf local_swap gap-asymmetry explainer.")
    p.add_argument("--in-placements-csv", type=str, default=str(PLACEMENTS_CSV))
    p.add_argument("--in-pairs-csv", type=str, default=str(PAIRS_CSV))
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15bf_local_swap_gap_asymmetry_rows.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bf_local_swap_gap_asymmetry_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bf_local_swap_gap_asymmetry_explainer.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bf_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bf.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    placements = placement_map(read_csv(Path(args.in_placements_csv)))
    rows = asymmetry_rows(read_csv(Path(args.in_pairs_csv)), placements)
    diagnosis = diagnosis_rows(rows)
    report_md = build_report(rows=rows, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bf operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en lokal asymmetriforklaring inne i `v15bd`/`v15be`, ikke som en ny bred scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bf",
            "",
            "Denne runden tester om de to små stegene inne i den nye triggeraksen faktisk er ulike typer overganger.",
            "",
            "Poenget er å se om én overgang mest handler om at kjernen blir sterkere, mens den andre mer handler om at systemet samtidig mister struktur og får tyngre randbelastning.",
        ]
    ) + "\n"
    write_csv(args.out_rows_csv, rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
