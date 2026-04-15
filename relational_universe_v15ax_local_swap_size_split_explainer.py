#!/usr/bin/env python3
"""v0.15ax local_swap size split explainer.

This round does not run new simulations. It reads the v15aw local_swap
core-shell results and asks whether the 48-vs-96 split is strong enough to be
treated as real new knowledge rather than a generic "mixed" outcome.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import relational_universe_v15_defect_lifetime_lab as v15


RUNS_CSV = Path("Documentation/v15aw_local_swap_core_shell_runs.csv")


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


def load_rows(path: Path) -> List[Dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for target in (48, 96):
        group = [row for row in rows if int(row["target_nodes"]) == target]
        counts = Counter(str(row["core_shell_label"]) for row in group)
        dominant_label = max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0] if counts else "none"
        out.append(
            {
                "target_nodes": target,
                "n_runs": len(group),
                "stable_core_variable_shell_rate": mean_defined(
                    1.0 if str(row["core_shell_label"]) == "stable_core_variable_shell" else 0.0 for row in group
                ),
                "mixed_core_shell_rate": mean_defined(
                    1.0 if str(row["core_shell_label"]) == "mixed_core_shell" else 0.0 for row in group
                ),
                "diffuse_shell_rate": mean_defined(
                    1.0 if str(row["core_shell_label"]) == "diffuse_shell_recurrence" else 0.0 for row in group
                ),
                "mean_core_share_of_union": mean_defined(safe_float(row["core_share_of_union"]) for row in group),
                "mean_shell_share_of_union": mean_defined(safe_float(row["shell_share_of_union"]) for row in group),
                "mean_rare_share_of_union": mean_defined(safe_float(row["rare_share_of_union"]) for row in group),
                "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in group),
                "dominant_label": dominant_label,
            }
        )
    return out


def placement_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for target in (48, 96):
        for placement in (0, 1, 2, 3):
            group = [
                row
                for row in rows
                if int(row["target_nodes"]) == target and int(row["placement"]) == placement
            ]
            counts = Counter(str(row["core_shell_label"]) for row in group)
            dominant_label = max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0] if counts else "none"
            out.append(
                {
                    "target_nodes": target,
                    "placement": placement,
                    "n_runs": len(group),
                    "stable_core_variable_shell_rate": mean_defined(
                        1.0 if str(row["core_shell_label"]) == "stable_core_variable_shell" else 0.0 for row in group
                    ),
                    "diffuse_shell_rate": mean_defined(
                        1.0 if str(row["core_shell_label"]) == "diffuse_shell_recurrence" else 0.0 for row in group
                    ),
                    "mean_core_share_of_union": mean_defined(safe_float(row["core_share_of_union"]) for row in group),
                    "mean_shell_share_of_union": mean_defined(safe_float(row["shell_share_of_union"]) for row in group),
                    "dominant_label": dominant_label,
                }
            )
    return out


def diagnosis_rows(aggregate: Sequence[Dict[str, Any]], placements: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_target = {int(row["target_nodes"]): row for row in aggregate}
    low = by_target[48]
    high = by_target[96]

    low_clean = safe_float(low["stable_core_variable_shell_rate"]) >= 0.99
    high_diffuse = safe_float(high["diffuse_shell_rate"]) >= 0.50
    core_drop = safe_float(low["mean_core_share_of_union"]) - safe_float(high["mean_core_share_of_union"])
    shell_rise = safe_float(high["mean_shell_share_of_union"]) - safe_float(low["mean_shell_share_of_union"])
    high_pockets = [
        row for row in placements
        if int(row["target_nodes"]) == 96 and str(row["dominant_label"]) == "stable_core_variable_shell"
    ]

    if low_clean and high_diffuse and core_drop >= 0.20 and shell_rise >= 0.08:
        status = "local_swap_size_split_supported"
        note = "48-nivået holder rent som stable core+shell, mens 96-nivået går over i en mer diffus shell-regime med klart lavere kjerneandel og høyere randandel."
        next_step = "explain_diffuse_96_pockets"
        next_note = "Neste steg bør forklare hvorfor noen få 96-run fortsatt nærmer seg core+shell, i stedet for å scanne bredere."
    else:
        status = "size_split_not_yet"
        note = "48-vs-96-splittelsen ser lovende ut, men er ikke skarp nok ennå til å behandles som en egen lokal lov."
        next_step = "stay_descriptive"
        next_note = "Neste steg bør holde seg på observabelnivå og unngå store size-påstander."

    pocket_note = (
        f"Det finnes {len(high_pockets)} små 96-lommer som fortsatt holder stable core+shell lokalt."
        if high_pockets
        else "Ingen 96-lommer holder stable core+shell rent lokalt."
    )

    return [
        {
            "diagnostic_family": "size_split_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "96_pocket_status",
            "status": "small_core_shell_pockets_present" if high_pockets else "no_core_shell_pockets",
            "note": pocket_note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, aggregate: Sequence[Dict[str, Any]], placements: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15ax: local_swap size split explainer")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden bruker bare v15aw-data for å avgjøre om forskjellen mellom target 48 og 96 i local_swap-sporet er sterk nok til å behandles som ny viten.")
    lines.append("")
    lines.append("## Target summary")
    lines.append("")
    lines.append("| target | n | core+shell | mixed | diffuse shell | mean core share | mean shell share | mean rare share | dominant |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['target_nodes'])} | {int(row['n_runs'])} | {fmt(row['stable_core_variable_shell_rate'])} | {fmt(row['mixed_core_shell_rate'])} | {fmt(row['diffuse_shell_rate'])} | {fmt(row['mean_core_share_of_union'])} | {fmt(row['mean_shell_share_of_union'])} | {fmt(row['mean_rare_share_of_union'])} | {row['dominant_label']} |"
        )
    lines.append("")
    lines.append("## Placement pockets")
    lines.append("")
    lines.append("| target | placement | n | core+shell | diffuse shell | mean core share | mean shell share | dominant |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in placements:
        lines.append(
            f"| {int(row['target_nodes'])} | {int(row['placement'])} | {int(row['n_runs'])} | {fmt(row['stable_core_variable_shell_rate'])} | {fmt(row['diffuse_shell_rate'])} | {fmt(row['mean_core_share_of_union'])} | {fmt(row['mean_shell_share_of_union'])} | {row['dominant_label']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren forklaringsrunde på toppen av v15aw, ikke en ny simulering.")
    lines.append("- Les dette som en strukturert size-splitt i local_swap-observabelen, ikke som en stor asymptotisk lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ax local_swap size split explainer.")
    p.add_argument("--in-runs-csv", type=str, default=str(RUNS_CSV))
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ax_local_swap_size_split_aggregate.csv")
    p.add_argument("--out-placement-csv", type=str, default="Documentation/v15ax_local_swap_size_split_placements.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ax_local_swap_size_split_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ax_local_swap_size_split_explainer.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ax_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ax.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_rows(Path(args.in_runs_csv))
    aggregate = aggregate_rows(rows)
    placements = placement_rows(rows)
    diagnosis = diagnosis_rows(aggregate, placements)
    report_md = build_report(aggregate=aggregate, placements=placements, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15ax operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en size-forklaring av v15aw, ikke som en ny bred defect-kjøring.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15ax",
            "",
            "Denne runden sjekker om local_swap ser lik ut på små og litt større grafer, eller om den endrer karakter når vi går opp i størrelse.",
            "",
            "Resultatet er nyttig fordi det sier om samme type lokal retur holder seg ren, eller om randen tar mer over når grafen blir større.",
        ]
    ) + "\n"
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_placement_csv, placements)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
