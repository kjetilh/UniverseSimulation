#!/usr/bin/env python3
"""v0.15bi local_swap load-stabilizer flip.

This round does not run new simulations. It explains the p2-vs-p1 boundary
inside growth_seed 202 by testing whether p2 is the highest-load direction
while p1 is the strongest stabilizer direction.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
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


def load_base_state() -> Any:
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, _ = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    return base_states[(ensembles[0].name, GROWTH_SEED)]


def placement_rows(run_rows: Sequence[Mapping[str, str]], base_state: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in run_rows:
        if int(row["target_nodes"]) != TARGET or int(row["growth_seed"]) != GROWTH_SEED:
            continue
        placement = int(row["placement"])
        if placement not in (1, 2, 3):
            continue
        support = [int(x) for x in str(row["support_signature"]).split(",") if x]
        geom = v14c.support_geometry_features(base_state, support)
        out.append(
            {
                "placement": placement,
                "label": str(row["core_shell_label"]),
                "coarse_return": safe_float(row["full_coarse_return_rate"]),
                "core_share": safe_float(row["core_share_of_union"]),
                "rare_share": safe_float(row["rare_share_of_union"]),
                "shell_share": safe_float(row["shell_share_of_union"]),
                "mean_support_degree": safe_float(geom["mean_support_degree"]),
                "support_ball_1": safe_float(geom["support_ball_1"]),
                "support_ball_2": safe_float(geom["support_ball_2"]),
                "support_ball_3": safe_float(geom["support_ball_3"]),
                "shell2_over_shell1": safe_float(geom["shell2_over_shell1"]),
            }
        )
    return sorted(out, key=lambda r: int(r["placement"]))


def load_axes() -> Dict[str, Callable[[Mapping[str, Any]], float]]:
    return {
        "ball1_load": lambda v: safe_float(v["support_ball_1"]),
        "ball2_load": lambda v: safe_float(v["support_ball_2"]),
        "ball3_load": lambda v: safe_float(v["support_ball_3"]),
        "degree_ball1_load": lambda v: safe_float(v["mean_support_degree"]) + safe_float(v["support_ball_1"]) / 10.0,
        "degree_ball2_load": lambda v: safe_float(v["mean_support_degree"]) + safe_float(v["support_ball_2"]) / 20.0,
    }


def stabilizer_axes() -> Dict[str, Callable[[Mapping[str, Any]], float]]:
    return {
        "retention_shell_stabilizer": lambda v: safe_float(v["coarse_return"]) + safe_float(v["shell2_over_shell1"]),
        "retention_core_stabilizer": lambda v: safe_float(v["coarse_return"]) + safe_float(v["core_share"]),
        "full_stabilizer": lambda v: safe_float(v["coarse_return"]) + safe_float(v["core_share"]) + safe_float(v["shell2_over_shell1"]),
    }


def axis_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by = {int(row["placement"]): row for row in rows}
    out: List[Dict[str, Any]] = []
    for family, axes in [("load", load_axes()), ("stabilizer", stabilizer_axes())]:
        for name, fn in axes.items():
            p1 = fn(by[1])
            p2 = fn(by[2])
            p3 = fn(by[3])
            top = 1 if ((family == "load" and p2 > p1 and p2 > p3) or (family == "stabilizer" and p1 > p2 and p1 > p3)) else 0
            margin = (
                min(p2 - p1, p2 - p3)
                if family == "load" and top
                else min(p1 - p2, p1 - p3)
                if family == "stabilizer" and top
                else float("nan")
            )
            out.append(
                {
                    "axis_name": name,
                    "axis_family": family,
                    "p1_value": p1,
                    "p2_value": p2,
                    "p3_value": p3,
                    "family_top_supported": top,
                    "top_margin": margin,
                }
            )
    return sorted(out, key=lambda r: (str(r["axis_family"]), -int(r["family_top_supported"]), -safe_float(r["top_margin"], -1.0)))


def diagnosis_rows(axis_rows_out: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    load_rows = [row for row in axis_rows_out if str(row["axis_family"]) == "load"]
    stab_rows = [row for row in axis_rows_out if str(row["axis_family"]) == "stabilizer"]
    load_supported = all(int(row["family_top_supported"]) == 1 for row in load_rows)
    stab_supported = all(int(row["family_top_supported"]) == 1 for row in stab_rows)
    best_load = max(load_rows, key=lambda r: safe_float(r["top_margin"], -1.0))
    best_stab = max(stab_rows, key=lambda r: safe_float(r["top_margin"], -1.0))
    if load_supported and stab_supported:
        status = "load_without_stabilization_supported"
        note = "p2 topper alle små last-akser, mens p1 topper alle små stabiliseringsakser. Det støtter at rare-load-flippen ligger i høy last uten tilsvarende stabilisering."
        next_step = "explain_missing_stabilizer"
    else:
        status = "load_stabilizer_flip_not_yet"
        note = "Last- og stabiliseringssidene lot seg ikke splitte rent nok i denne runden."
        next_step = "change_boundary_observable"
    return [
        {
            "diagnostic_family": "load_stabilizer_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "best_load_axis",
            "status": str(best_load["axis_name"]),
            "note": f"Beste lastakse gir margin {fmt(best_load['top_margin'])}.",
        },
        {
            "diagnostic_family": "best_stabilizer_axis",
            "status": str(best_stab["axis_name"]),
            "note": f"Beste stabiliseringsakse gir margin {fmt(best_stab['top_margin'])}.",
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": "Neste steg bør forklare hva p2 mangler av stabilisering relativt til p1.",
        },
    ]


def build_report(*, placements: Sequence[Mapping[str, Any]], axes: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bi: local_swap load-stabilizer flip")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden tester om `p2` og `p1` skilles best av en last-vs-stabilisering-flip: `p2` som tyngst lokal last, `p1` som sterkest stabilisering.")
    lines.append("")
    lines.append("## Placement snapshot")
    lines.append("")
    lines.append("| placement | coarse return | core share | rare share | mean degree | ball1 | ball2 | shell2/shell1 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in placements:
        lines.append(
            f"| {int(row['placement'])} | {fmt(row['coarse_return'])} | {fmt(row['core_share'])} | {fmt(row['rare_share'])} | {fmt(row['mean_support_degree'])} | {fmt(row['support_ball_1'])} | {fmt(row['support_ball_2'])} | {fmt(row['shell2_over_shell1'])} |"
        )
    lines.append("")
    lines.append("## Load and stabilizer axes")
    lines.append("")
    lines.append("| axis | family | p1 | p2 | p3 | supported | margin |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in axes:
        lines.append(
            f"| {row['axis_name']} | {row['axis_family']} | {fmt(row['p1_value'])} | {fmt(row['p2_value'])} | {fmt(row['p3_value'])} | {int(row['family_top_supported'])} | {fmt(row['top_margin'])} |"
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
    lines.append("- Les dette som en lokal p2-vs-p1-grenseforklaring, ikke som en global law for `local_swap`.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bi local_swap load-stabilizer flip.")
    p.add_argument("--in-runs-csv", type=str, default=str(RUNS_CSV))
    p.add_argument("--out-placements-csv", type=str, default="Documentation/v15bi_local_swap_load_stabilizer_placements.csv")
    p.add_argument("--out-axes-csv", type=str, default="Documentation/v15bi_local_swap_load_stabilizer_axes.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bi_local_swap_load_stabilizer_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bi_local_swap_load_stabilizer_flip.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bi_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bi.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    base_state = load_base_state()
    placements = placement_rows(read_csv(Path(args.in_runs_csv)), base_state)
    axes = axis_rows(placements)
    diagnosis = diagnosis_rows(axes)
    report_md = build_report(placements=placements, axes=axes, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bi operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en smal p2-vs-p1-grenseforklaring, ikke som en ny bred scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bi",
            "",
            "Denne runden tester om de to lokale retningene `p1` og `p2` skiller lag fordi de er tunge på forskjellige måter.",
            "",
            "Tanken er at `p2` kan være tyngst på lokal last, mens `p1` er bedre til å holde strukturen samlet når lasten først er der.",
        ]
    ) + "\n"
    write_csv(args.out_placements_csv, placements)
    write_csv(args.out_axes_csv, axes)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
