#!/usr/bin/env python3
"""v0.15bd local_swap trigger-axis lab.

This round does not run new simulations. It tests a small curated set of
candidate scalar axes to see whether one of them orders the three diffuse
growth_seed-202 local_swap modes (p1 > p3 > p2) more cleanly than the others.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15


RUNS_CSV = Path("Documentation/v15aw_local_swap_core_shell_runs.csv")
TARGET = 96
GROWTH_SEED = 202


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


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
        support = [int(x) for x in str(row["support_signature"]).split(",") if x]
        geom = v14c.support_geometry_features(base_state, support)
        out.append(
            {
                "placement": int(row["placement"]),
                "core_shell_label": str(row["core_shell_label"]),
                "full_coarse_return_rate": safe_float(row["full_coarse_return_rate"]),
                "core_share_of_union": safe_float(row["core_share_of_union"]),
                "shell_plus_rare_share": safe_float(row["shell_share_of_union"]) + safe_float(row["rare_share_of_union"]),
                "tail_density": safe_float(row["mean_tail_damage_nodes"]) / max(1.0, safe_float(row["tail_union_nodes"])),
                "core_to_shell_ratio": safe_float(row["core_nodes"]) / max(1.0, safe_float(row["shell_nodes"])),
                "mean_support_degree": safe_float(geom["mean_support_degree"]),
                "ball3_over_ball1": safe_float(geom["ball3_over_ball1"]),
                "shell2_over_shell1": safe_float(geom["shell2_over_shell1"]),
            }
        )
    return sorted(out, key=lambda r: int(r["placement"]))


def candidate_axes() -> Dict[str, Callable[[Mapping[str, Any]], float]]:
    return {
        "coarse_return": lambda v: safe_float(v["full_coarse_return_rate"]),
        "core_share": lambda v: safe_float(v["core_share_of_union"]),
        "tail_density": lambda v: safe_float(v["tail_density"]),
        "core_to_shell": lambda v: safe_float(v["core_to_shell_ratio"]),
        "retention_core_axis": lambda v: safe_float(v["full_coarse_return_rate"]) + safe_float(v["core_to_shell_ratio"]),
        "retention_density_axis": lambda v: safe_float(v["full_coarse_return_rate"]) + safe_float(v["tail_density"]),
        "retention_minus_shell_axis": lambda v: safe_float(v["full_coarse_return_rate"]) - safe_float(v["shell_plus_rare_share"]),
        "core_minus_shell_axis": lambda v: safe_float(v["core_share_of_union"]) - safe_float(v["shell_plus_rare_share"]),
        "support_compactness_axis": lambda v: -safe_float(v["ball3_over_ball1"]),
        "support_density_axis": lambda v: safe_float(v["mean_support_degree"]),
    }


def axis_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_placement = {int(row["placement"]): row for row in rows}
    out: List[Dict[str, Any]] = []
    for name, fn in candidate_axes().items():
        p1 = fn(by_placement[1])
        p3 = fn(by_placement[3])
        p2 = fn(by_placement[2])
        p0 = fn(by_placement[0])
        ordered = p1 > p3 > p2
        margin = min(p1 - p3, p3 - p2) if ordered else float("nan")
        out.append(
            {
                "axis_name": name,
                "p1_value": p1,
                "p3_value": p3,
                "p2_value": p2,
                "p0_value": p0,
                "orders_p1_gt_p3_gt_p2": 1 if ordered else 0,
                "ordered_margin": margin,
                "axis_family": "support" if "support" in name else "dynamic",
            }
        )
    return sorted(
        out,
        key=lambda r: (int(r["orders_p1_gt_p3_gt_p2"]), safe_float(r["ordered_margin"], -1.0)),
        reverse=True,
    )


def diagnosis_rows(axis_rows_out: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    best = axis_rows_out[0]
    best_dynamic = next(row for row in axis_rows_out if str(row["axis_family"]) == "dynamic")
    support_candidates = [row for row in axis_rows_out if str(row["axis_family"]) == "support"]
    support_best = max(support_candidates, key=lambda r: safe_float(r["ordered_margin"], -1.0))

    if str(best_dynamic["axis_name"]) == "retention_core_axis" and int(best_dynamic["orders_p1_gt_p3_gt_p2"]) == 1:
        status = "retention_core_axis_supported"
        note = "En enkel dynamisk akse, `coarse_return + core_to_shell`, ordner p1 > p3 > p2 renere enn de andre tolkbare kandidatene."
        next_step = "explain_axis_from_components"
        next_note = "Neste steg bør forklare hva som faktisk driver denne aksen lokalt, ikke bare bruke den som score."
    else:
        status = "trigger_axis_not_yet"
        note = "Ingen liten, tolkbar kandidatakse skiller p1, p3 og p2 rent nok ennå."
        next_step = "change_axis_family"
        next_note = "Neste steg bør prøve en annen observabelfamilie enn disse enkle aksene."

    support_note = (
        f"Beste støtteakse er `{support_best['axis_name']}`, men den holder ikke ren ordering."
        if int(support_best["orders_p1_gt_p3_gt_p2"]) == 0
        else f"Støtteakse `{support_best['axis_name']}` ordner også casene, men svakere enn den dynamiske aksen."
    )

    return [
        {
            "diagnostic_family": "trigger_axis_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "support_axis_status",
            "status": "support_weaker_than_dynamic",
            "note": support_note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, placements: Sequence[Dict[str, Any]], axes: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bd: local_swap trigger-axis lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden tester et lite sett tolkbare kandidat-akser for a se om en av dem ordner de tre diffuse growth_seed-202-modiene som `p1 > p3 > p2`.")
    lines.append("")
    lines.append("## Placement snapshot")
    lines.append("")
    lines.append("| placement | label | coarse return | core share | shell+rare | tail density | core/shell | mean degree | ball3/ball1 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in placements:
        lines.append(
            f"| {int(row['placement'])} | {row['core_shell_label']} | {fmt(row['full_coarse_return_rate'])} | {fmt(row['core_share_of_union'])} | {fmt(row['shell_plus_rare_share'])} | {fmt(row['tail_density'])} | {fmt(row['core_to_shell_ratio'])} | {fmt(row['mean_support_degree'])} | {fmt(row['ball3_over_ball1'])} |"
        )
    lines.append("")
    lines.append("## Candidate axes")
    lines.append("")
    lines.append("| axis | family | p1 | p3 | p2 | p0 | ordered | margin |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in axes:
        lines.append(
            f"| {row['axis_name']} | {row['axis_family']} | {fmt(row['p1_value'])} | {fmt(row['p3_value'])} | {fmt(row['p2_value'])} | {fmt(row['p0_value'])} | {int(row['orders_p1_gt_p3_gt_p2'])} | {fmt(row['ordered_margin'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren akselab pa eksisterende data, ikke en ny simulering.")
    lines.append("- Les dette som en liten triggerakse for den diffuse modussplittelsen, ikke som en ny global lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bd local_swap trigger-axis lab.")
    p.add_argument("--in-runs-csv", type=str, default=str(RUNS_CSV))
    p.add_argument("--out-placements-csv", type=str, default="Documentation/v15bd_local_swap_trigger_axis_placements.csv")
    p.add_argument("--out-axes-csv", type=str, default="Documentation/v15bd_local_swap_trigger_axis_candidates.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bd_local_swap_trigger_axis_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bd_local_swap_trigger_axis_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bd_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bd.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    base_state = load_base_state()
    run_rows = read_csv(Path(args.in_runs_csv))
    placements = placement_rows(run_rows, base_state)
    axes = axis_rows(placements)
    diagnosis = diagnosis_rows(axes)
    report_md = build_report(placements=placements, axes=axes, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bd operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en triggerakse-lab pa eksisterende data, ikke som en ny bred scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bd",
            "",
            "Denne runden tester om det finnes én enkel måleakse som forklarer hvorfor tre nærliggende diffuse modi likevel skiller lag.",
            "",
            "Målet er å finne en liten, lesbar regel som sier noe om når systemet holder bedre på struktur, og når det sklir mer over i rand- og rare-støy.",
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
