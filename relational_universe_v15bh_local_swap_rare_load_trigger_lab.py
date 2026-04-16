#!/usr/bin/env python3
"""v0.15bh local_swap rare-load trigger lab.

This round does not run new simulations. It tests whether the dissipative p2
direction inside growth_seed 202 can be read as a small support/load trigger
for rare-load inflation, rather than just as another diffuse shell variant.
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
                "rare_share": safe_float(row["rare_share_of_union"]),
                "shell_share": safe_float(row["shell_share_of_union"]),
                "coarse_return": safe_float(row["full_coarse_return_rate"]),
                "mean_support_degree": safe_float(geom["mean_support_degree"]),
                "support_ball_1": safe_float(geom["support_ball_1"]),
                "support_ball_2": safe_float(geom["support_ball_2"]),
                "support_ball_3": safe_float(geom["support_ball_3"]),
                "ball3_over_ball1": safe_float(geom["ball3_over_ball1"]),
                "shell2_over_shell1": safe_float(geom["shell2_over_shell1"]),
            }
        )
    return sorted(out, key=lambda r: int(r["placement"]))


def candidate_axes() -> Dict[str, Callable[[Mapping[str, Any]], float]]:
    return {
        "support_degree": lambda v: safe_float(v["mean_support_degree"]),
        "ball1_load": lambda v: safe_float(v["support_ball_1"]),
        "ball2_load": lambda v: safe_float(v["support_ball_2"]),
        "ball3_load": lambda v: safe_float(v["support_ball_3"]),
        "degree_minus_shell2": lambda v: safe_float(v["mean_support_degree"]) - safe_float(v["shell2_over_shell1"]),
        "dense_local_load": lambda v: safe_float(v["mean_support_degree"]) + safe_float(v["support_ball_1"]) / 10.0 - safe_float(v["shell2_over_shell1"]),
        "compact_dense_load": lambda v: safe_float(v["mean_support_degree"]) + safe_float(v["support_ball_1"]) / 10.0 - safe_float(v["ball3_over_ball1"]),
    }


def axis_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by = {int(row["placement"]): row for row in rows}
    out: List[Dict[str, Any]] = []
    for name, fn in candidate_axes().items():
        p1 = fn(by[1])
        p2 = fn(by[2])
        p3 = fn(by[3])
        p2_top = p2 > p1 and p2 > p3
        full_rare_order = p2 > p3 > p1
        margin = min(p2 - p1, p2 - p3) if p2_top else float("nan")
        out.append(
            {
                "axis_name": name,
                "p1_value": p1,
                "p2_value": p2,
                "p3_value": p3,
                "p2_top": 1 if p2_top else 0,
                "full_rare_order": 1 if full_rare_order else 0,
                "p2_margin": margin,
            }
        )
    return sorted(out, key=lambda r: (int(r["p2_top"]), safe_float(r["p2_margin"], -1.0)), reverse=True)


def diagnosis_rows(axis_rows_out: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    p2_top_axes = [row for row in axis_rows_out if int(row["p2_top"]) == 1]
    full_order_axes = [row for row in axis_rows_out if int(row["full_rare_order"]) == 1]
    best = axis_rows_out[0]
    if len(p2_top_axes) >= 3 and len(full_order_axes) == 0:
        status = "p2_rare_load_trigger_supported"
        note = "Flere små støtte-/last-akser setter p2 tydelig øverst, men ingen av dem løser samtidig p3 > p1. Det støtter en lokal p2-trigger uten å late som hele rare-rangeringen er løst."
        next_step = "explain_p2_trigger_without_overclaim"
    elif len(full_order_axes) >= 1:
        status = "full_rare_load_axis_supported"
        note = "Minst én liten akse gjenskaper hele rare-rangeringen p2 > p3 > p1."
        next_step = "stress_full_rare_axis"
    else:
        status = "rare_load_trigger_not_yet"
        note = "Ingen liten støtte-/last-akse setter p2 tydelig nok øverst."
        next_step = "change_trigger_family"
    return [
        {
            "diagnostic_family": "rare_load_trigger_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "best_axis",
            "status": str(best["axis_name"]),
            "note": f"Beste kandidatakse gir p2-margin {fmt(best['p2_margin'])}.",
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": "Neste steg bør forklare p2-triggeren lokalt, ikke åpne en bredere scan.",
        },
    ]


def build_report(*, placements: Sequence[Mapping[str, Any]], axes: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bh: local_swap rare-load trigger lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden tester om `p2` kan leses som en egen rare-load-retning ut fra en liten støtte-/last-akse.")
    lines.append("")
    lines.append("## Placement snapshot")
    lines.append("")
    lines.append("| placement | rare share | shell share | coarse return | mean degree | ball1 | ball2 | ball3 | shell2/shell1 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in placements:
        lines.append(
            f"| {int(row['placement'])} | {fmt(row['rare_share'])} | {fmt(row['shell_share'])} | {fmt(row['coarse_return'])} | {fmt(row['mean_support_degree'])} | {fmt(row['support_ball_1'])} | {fmt(row['support_ball_2'])} | {fmt(row['support_ball_3'])} | {fmt(row['shell2_over_shell1'])} |"
        )
    lines.append("")
    lines.append("## Candidate trigger axes")
    lines.append("")
    lines.append("| axis | p1 | p2 | p3 | p2 top | full rare order | margin |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in axes:
        lines.append(
            f"| {row['axis_name']} | {fmt(row['p1_value'])} | {fmt(row['p2_value'])} | {fmt(row['p3_value'])} | {int(row['p2_top'])} | {int(row['full_rare_order'])} | {fmt(row['p2_margin'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en ren akse-/triggerlab på eksisterende data, ikke en ny simulering.")
    lines.append("- Les dette som en smal test av p2-retningen, ikke som en full forklaring av hele p1/p2/p3-kartet.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bh local_swap rare-load trigger lab.")
    p.add_argument("--in-runs-csv", type=str, default=str(RUNS_CSV))
    p.add_argument("--out-placements-csv", type=str, default="Documentation/v15bh_local_swap_rare_load_trigger_placements.csv")
    p.add_argument("--out-axes-csv", type=str, default="Documentation/v15bh_local_swap_rare_load_trigger_axes.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bh_local_swap_rare_load_trigger_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bh_local_swap_rare_load_trigger_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bh_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bh.md")
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
            "# v0.15bh operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en smal rare-load-triggerlab, ikke som en ny bred scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bh",
            "",
            "Denne runden spør om den mest dissipative lokale modusen kan gjenkjennes tidlig gjennom hvor tett og tungt støtteområdet er lokalt.",
            "",
            "Poenget er ikke å forklare alt på én gang, men å se om akkurat p2-retningen ser ut til å ha en liten lokal trigger som peker mot høy rare-last.",
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
