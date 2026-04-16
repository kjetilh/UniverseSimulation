#!/usr/bin/env python3
"""v0.15bk local_swap load-stabilizer mode map.

This round does not run new simulations. It combines the best load axis and
the best stabilizer axis from v15bi/v15bj to map p1, p2, p3 into a small local
mode chart.
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


def placement_rows(rows: Sequence[Mapping[str, str]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        load_axis = safe_float(row["support_ball_2"])
        stabilizer_axis = (
            safe_float(row["coarse_return"])
            + safe_float(row["core_share"])
            + safe_float(row["shell2_over_shell1"])
        )
        out.append(
            {
                "placement": int(row["placement"]),
                "coarse_return": safe_float(row["coarse_return"]),
                "core_share": safe_float(row["core_share"]),
                "rare_share": safe_float(row["rare_share"]),
                "ball2_load": load_axis,
                "full_stabilizer": stabilizer_axis,
            }
        )
    mean_load = sum(safe_float(row["ball2_load"]) for row in out) / max(1, len(out))
    mean_stab = sum(safe_float(row["full_stabilizer"]) for row in out) / max(1, len(out))
    for row in out:
        load_delta = safe_float(row["ball2_load"]) - mean_load
        stab_delta = safe_float(row["full_stabilizer"]) - mean_stab
        if load_delta >= 0 and stab_delta >= 0:
            mode = "buffered_heavy_load"
        elif load_delta >= 0 and stab_delta < 0:
            mode = "rare_load_risk"
        elif load_delta < 0 and stab_delta < 0:
            mode = "low_load_diffuse"
        else:
            mode = "light_but_buffered"
        row["load_delta_vs_mean"] = load_delta
        row["stabilizer_delta_vs_mean"] = stab_delta
        row["mode"] = mode
    return sorted(out, key=lambda r: int(r["placement"]))


def diagnosis_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by = {int(row["placement"]): row for row in rows}
    p1 = by[1]
    p2 = by[2]
    p3 = by[3]
    if (
        str(p1["mode"]) == "buffered_heavy_load"
        and str(p2["mode"]) == "rare_load_risk"
        and str(p3["mode"]) == "low_load_diffuse"
    ):
        status = "load_stabilizer_mode_map_supported"
        note = "p1, p2 og p3 fyller tre ulike lokale modi: tung last med buffer, tung last uten nok buffer, og lavere last med diffus retur."
        next_step = "explain_risk_side_only"
    else:
        status = "mode_map_not_yet"
        note = "Load-stabilizer-kartet ble ikke rent nok i denne enkle sentreringen."
        next_step = "change_mode_map_centering"
    return [
        {
            "diagnostic_family": "load_stabilizer_mode_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": "Neste steg bør gå på risiko-siden av kartet, ikke åpne en bredere scan.",
        },
    ]


def build_report(*, rows: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bk: local_swap load-stabilizer mode map")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden samler de beste lokale last- og stabiliseringsaksene i ett lite moduskart for `p1`, `p2` og `p3`.")
    lines.append("")
    lines.append("## Mode map")
    lines.append("")
    lines.append("| placement | ball2 load | full stabilizer | load delta | stabilizer delta | mode |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {int(row['placement'])} | {fmt(row['ball2_load'])} | {fmt(row['full_stabilizer'])} | {fmt(row['load_delta_vs_mean'])} | {fmt(row['stabilizer_delta_vs_mean'])} | {row['mode']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en ren synteserunde på eksisterende data, ikke en ny simulering.")
    lines.append("- Les dette som et lite lokalt moduskart for growth_seed 202, ikke som en global law for `local_swap`.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bk local_swap load-stabilizer mode map.")
    p.add_argument("--in-placements-csv", type=str, default=str(PLACEMENTS_CSV))
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15bk_local_swap_load_stabilizer_mode_rows.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bk_local_swap_load_stabilizer_mode_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bk_local_swap_load_stabilizer_mode_map.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bk_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bk.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    rows = placement_rows(read_csv(Path(args.in_placements_csv)))
    diagnosis = diagnosis_rows(rows)
    report_md = build_report(rows=rows, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bk operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som et lite load-stabilizer-moduskart, ikke som en ny bred scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bk",
            "",
            "Denne runden samler de forrige små funnene til et enkelt lokalt kart.",
            "",
            "Poenget er å se om de tre nærliggende retningene egentlig fyller tre ulike roller: tung last med buffer, tung last uten nok buffer, og lavere last med diffus oppførsel.",
        ]
    ) + "\n"
    write_csv(args.out_rows_csv, rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
