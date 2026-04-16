#!/usr/bin/env python3
"""v0.15bj local_swap stabilizer component lab.

This round does not run new simulations. It decomposes the p1-vs-p2
stabilizer gap from v15bi to determine whether the missing stabilizer on the
p2 side is driven mainly by retention, by core support, or by shell layering.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

import relational_universe_v15_defect_lifetime_lab as v15


PLACEMENTS_CSV = Path("Documentation/v15bi_local_swap_load_stabilizer_placements.csv")


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
            "coarse_return": safe_float(row["coarse_return"]),
            "core_share": safe_float(row["core_share"]),
            "shell2_over_shell1": safe_float(row["shell2_over_shell1"]),
        }
    return out


def component_rows(placements: Mapping[int, Mapping[str, Any]]) -> List[Dict[str, Any]]:
    p1 = placements[1]
    p2 = placements[2]
    coarse_gap = safe_float(p1["coarse_return"]) - safe_float(p2["coarse_return"])
    core_gap = safe_float(p1["core_share"]) - safe_float(p2["core_share"])
    shell_gap = safe_float(p1["shell2_over_shell1"]) - safe_float(p2["shell2_over_shell1"])
    total_gap = coarse_gap + core_gap + shell_gap
    rows = [
        {
            "component": "coarse_return",
            "gap": coarse_gap,
            "share_of_total_gap": coarse_gap / total_gap if total_gap > 0 else float("nan"),
        },
        {
            "component": "core_share",
            "gap": core_gap,
            "share_of_total_gap": core_gap / total_gap if total_gap > 0 else float("nan"),
        },
        {
            "component": "shell2_over_shell1",
            "gap": shell_gap,
            "share_of_total_gap": shell_gap / total_gap if total_gap > 0 else float("nan"),
        },
        {
            "component": "full_stabilizer_gap",
            "gap": total_gap,
            "share_of_total_gap": 1.0,
        },
    ]
    return rows


def diagnosis_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    comp = {str(row["component"]): row for row in rows}
    coarse_share = safe_float(comp["coarse_return"]["share_of_total_gap"])
    core_share = safe_float(comp["core_share"]["share_of_total_gap"])
    shell_share = safe_float(comp["shell2_over_shell1"]["share_of_total_gap"])
    if coarse_share >= 0.50 and core_share >= 0.25 and shell_share < 0.20:
        status = "retention_led_stabilizer_deficit_supported"
        note = "p2 mangler ikke stabilisering pa alle fronter like mye. Underskuddet er retention-led, med core-share som tydelig sekundarkomponent og shell-lagdeling som liten tredjekomponent."
        next_step = "compare_missing_retention_vs_missing_core"
    elif core_share >= coarse_share:
        status = "core_led_stabilizer_deficit_supported"
        note = "Stabiliseringsunderskuddet ser mest ut til a være et kjerneunderskudd."
        next_step = "explain_core_deficit"
    else:
        status = "stabilizer_component_mix_not_yet"
        note = "Stabiliseringsgapet lot seg ikke dele rent nok i denne komponentlesningen."
        next_step = "change_stabilizer_observable"
    return [
        {
            "diagnostic_family": "stabilizer_component_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "component_shares",
            "status": "retention_core_shell_shares",
            "note": f"Retention {fmt(coarse_share)}, core {fmt(core_share)}, shell-lagdeling {fmt(shell_share)} av total stabiliseringsgap.",
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": "Neste steg bør forklare hvorfor retention-led underskudd og høy last møtes akkurat i p2.",
        },
    ]


def build_report(*, rows: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bj: local_swap stabilizer component lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden åpner `full_stabilizer` fra `v15bi` for å se hva `p2` faktisk mangler relativt til `p1`.")
    lines.append("")
    lines.append("## Component decomposition")
    lines.append("")
    lines.append("| component | gap | share of total |")
    lines.append("| --- | --- | --- |")
    for row in rows:
        lines.append(f"| {row['component']} | {fmt(row['gap'])} | {fmt(row['share_of_total_gap'])} |")
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en forklaringsrunde på eksisterende data, ikke en ny simulering.")
    lines.append("- Les dette som en lokal p1-vs-p2-komponentdeling, ikke som en global local_swap-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bj local_swap stabilizer component lab.")
    p.add_argument("--in-placements-csv", type=str, default=str(PLACEMENTS_CSV))
    p.add_argument("--out-components-csv", type=str, default="Documentation/v15bj_local_swap_stabilizer_components.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bj_local_swap_stabilizer_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bj_local_swap_stabilizer_component_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bj_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bj.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    placements = placement_map(read_csv(Path(args.in_placements_csv)))
    rows = component_rows(placements)
    diagnosis = diagnosis_rows(rows)
    report_md = build_report(rows=rows, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bj operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en stabiliserings-komponentdeling, ikke som en ny bred scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bj",
            "",
            "Denne runden spør hvilken del av stabiliseringen som faktisk mangler når systemet går fra den tryggere `p1`-retningen til den mer rare-lastede `p2`-retningen.",
            "",
            "Poenget er å se om problemet først og fremst er svakere tilbakevending, svakere kjerne, eller svakere lokal lagdeling rundt kjernen.",
        ]
    ) + "\n"
    write_csv(args.out_components_csv, rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
