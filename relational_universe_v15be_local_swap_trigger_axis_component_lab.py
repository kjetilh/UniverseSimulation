#!/usr/bin/env python3
"""v0.15be local_swap trigger-axis component lab.

This round does not run new simulations. It decomposes the supported
`retention_core_axis = coarse_return + core_to_shell` from v15bd to see
whether the diffuse p1 > p3 > p2 ordering is driven mostly by one component
or by a small two-component split.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

import relational_universe_v15_defect_lifetime_lab as v15


PLACEMENTS_CSV = Path("Documentation/v15bd_local_swap_trigger_axis_placements.csv")


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
        placement = int(row["placement"])
        out[placement] = {
            "placement": placement,
            "label": str(row["core_shell_label"]),
            "coarse_return": safe_float(row["full_coarse_return_rate"]),
            "core_to_shell": safe_float(row["core_to_shell_ratio"]),
            "tail_density": safe_float(row["tail_density"]),
            "retention_core_axis": safe_float(row["full_coarse_return_rate"]) + safe_float(row["core_to_shell_ratio"]),
        }
    return out


def pair_rows(rows: Mapping[int, Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for winner, loser in [(1, 3), (3, 2), (1, 2)]:
        win = rows[winner]
        lose = rows[loser]
        coarse_gap = safe_float(win["coarse_return"]) - safe_float(lose["coarse_return"])
        core_gap = safe_float(win["core_to_shell"]) - safe_float(lose["core_to_shell"])
        density_gap = safe_float(win["tail_density"]) - safe_float(lose["tail_density"])
        axis_gap = safe_float(win["retention_core_axis"]) - safe_float(lose["retention_core_axis"])
        dominant_component = "core_to_shell" if core_gap > coarse_gap else "coarse_return"
        core_share = core_gap / axis_gap if axis_gap > 0 else float("nan")
        coarse_share = coarse_gap / axis_gap if axis_gap > 0 else float("nan")
        if core_share >= 0.60:
            gap_family = "core_amplification_dominant"
        elif coarse_share >= 0.60:
            gap_family = "retention_dominant"
        else:
            gap_family = "balanced_two_component_gap"
        out.append(
            {
                "pair_label": f"p{winner}_vs_p{loser}",
                "winner": winner,
                "loser": loser,
                "winner_label": str(win["label"]),
                "loser_label": str(lose["label"]),
                "retention_core_axis_gap": axis_gap,
                "coarse_return_gap": coarse_gap,
                "core_to_shell_gap": core_gap,
                "tail_density_gap": density_gap,
                "coarse_share_of_axis_gap": coarse_share,
                "core_share_of_axis_gap": core_share,
                "dominant_component": dominant_component,
                "gap_family": gap_family,
            }
        )
    return out


def aggregate_rows(pair_rows_out: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    core_dom = sum(1 for row in pair_rows_out if str(row["gap_family"]) == "core_amplification_dominant")
    balanced = sum(1 for row in pair_rows_out if str(row["gap_family"]) == "balanced_two_component_gap")
    retention_dom = sum(1 for row in pair_rows_out if str(row["gap_family"]) == "retention_dominant")
    mean_core_share = sum(safe_float(row["core_share_of_axis_gap"]) for row in pair_rows_out) / max(1, len(pair_rows_out))
    mean_coarse_share = sum(safe_float(row["coarse_share_of_axis_gap"]) for row in pair_rows_out) / max(1, len(pair_rows_out))
    if core_dom >= 1 and balanced >= 1 and retention_dom == 0:
        status = "two_component_axis_supported"
        note = "Aksen ser ikke monolittisk ut: p1 > p3 drives mest av core/shell, mens p3 > p2 drives av en mer balansert blanding av return og core/shell."
        next_step = "explain_balanced_vs_core_cases"
    elif core_dom == len(pair_rows_out):
        status = "core_amplification_dominant_axis"
        note = "Hele aksen ser ut til å være dominert av core/shell-forsterkning."
        next_step = "stress_core_component"
    elif retention_dom >= 1:
        status = "retention_component_still_active"
        note = "Coarse return bærer fortsatt minst ett av gapene som en egen dominant komponent."
        next_step = "explain_retention_component"
    else:
        status = "component_split_not_yet"
        note = "Aksedrivern er fortsatt for diffus til å deles presist opp."
        next_step = "change_observable_family"

    return [
        {
            "diagnostic_family": "axis_component_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "component_balance",
            "status": "core_component_stronger",
            "note": f"Mean core-share av aksedelta er {fmt(mean_core_share)} mot coarse-share {fmt(mean_coarse_share)}.",
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": "Neste steg bør forklare hvorfor ett gap blir core-dominert mens det andre blir mer balansert.",
        },
    ]


def build_report(*, pair_rows_out: Sequence[Mapping[str, Any]], aggregate: Sequence[Mapping[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15be: local_swap trigger-axis component lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden åpner `retention_core_axis = coarse_return + core_to_shell` fra `v15bd` for å se hvilke komponenter som faktisk driver `p1 > p3 > p2`.")
    lines.append("")
    lines.append("## Pair decomposition")
    lines.append("")
    lines.append("| pair | axis gap | coarse gap | core/shell gap | tail density gap | coarse share | core share | family |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in pair_rows_out:
        lines.append(
            f"| {row['pair_label']} | {fmt(row['retention_core_axis_gap'])} | {fmt(row['coarse_return_gap'])} | {fmt(row['core_to_shell_gap'])} | {fmt(row['tail_density_gap'])} | {fmt(row['coarse_share_of_axis_gap'])} | {fmt(row['core_share_of_axis_gap'])} | {row['gap_family']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in aggregate:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en ren forklaringsrunde på eksisterende data, ikke en ny simulering.")
    lines.append("- Les dette som en lokal komponentforklaring for `growth_seed 202`, ikke som en global lov for `local_swap`.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15be local_swap trigger-axis component lab.")
    p.add_argument("--in-placements-csv", type=str, default=str(PLACEMENTS_CSV))
    p.add_argument("--out-pairs-csv", type=str, default="Documentation/v15be_local_swap_trigger_axis_pairs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15be_local_swap_trigger_axis_aggregate.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15be_local_swap_trigger_axis_component_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15be_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15be.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    placements = placement_map(read_csv(Path(args.in_placements_csv)))
    pair_rows_out = pair_rows(placements)
    aggregate = aggregate_rows(pair_rows_out)
    report_md = build_report(pair_rows_out=pair_rows_out, aggregate=aggregate)
    op_md = "\n".join(
        [
            "# v0.15be operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in aggregate],
            "",
            "- Les denne runden som en komponentforklaring av `v15bd`, ikke som en ny bred scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15be",
            "",
            "Denne runden spør hva som faktisk bærer den nye triggeraksen fra `v15bd`.",
            "",
            "Poenget er å se om forskjellen mellom de tre lokale modusene drives mest av hvor godt systemet holder på struktur, hvor stor kjernen blir i forhold til randen, eller en blanding av begge.",
        ]
    ) + "\n"
    write_csv(args.out_pairs_csv, pair_rows_out)
    write_csv(args.out_aggregate_csv, aggregate)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
