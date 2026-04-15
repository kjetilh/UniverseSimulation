#!/usr/bin/env python3
"""v0.15bb local_swap growth202 mode map.

This round does not run new simulations. It maps the four placement cases
inside the target-96, growth_seed-202 local_swap family to see whether the
current diffuse/mixed outcomes actually form a small internal mode atlas.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v15_defect_lifetime_lab as v15


RUNS_CSV = Path("Documentation/v15aw_local_swap_core_shell_runs.csv")
TARGET = 96
GROWTH_SEED = 202


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


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def classify_mode(
    *,
    coarse_return: float,
    core_share: float,
    shell_plus_rare_share: float,
    core_to_shell: float,
    tail_density: float,
    rare_share: float,
    tail_union_nodes: float,
) -> str:
    if core_share >= 0.45 and core_to_shell >= 1.20 and tail_density >= 0.60:
        return "high_core_mixed_mode"
    if coarse_return >= 0.80 and shell_plus_rare_share >= 0.60 and tail_union_nodes >= 60.0:
        return "wide_diffuse_retention_mode"
    if rare_share >= 0.40 and shell_plus_rare_share >= 0.85 and tail_density <= 0.36:
        return "dissipative_rare_shell_mode"
    if coarse_return >= 0.55 and shell_plus_rare_share >= 0.75 and tail_density <= 0.50 and tail_union_nodes <= 40.0:
        return "compressed_shell_return_mode"
    return "residual_mode"


def mode_rows(run_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in run_rows:
        if int(row["target_nodes"]) != TARGET or int(row["growth_seed"]) != GROWTH_SEED:
            continue
        core_share = safe_float(row["core_share_of_union"])
        shell_share = safe_float(row["shell_share_of_union"])
        rare_share = safe_float(row["rare_share_of_union"])
        core_nodes = safe_float(row["core_nodes"])
        shell_nodes = safe_float(row["shell_nodes"])
        tail_union_nodes = safe_float(row["tail_union_nodes"])
        mean_tail_damage_nodes = safe_float(row["mean_tail_damage_nodes"])
        shell_plus_rare_share = shell_share + rare_share
        core_to_shell = core_nodes / max(1.0, shell_nodes)
        tail_density = mean_tail_damage_nodes / max(1.0, tail_union_nodes)
        coarse_return = safe_float(row["full_coarse_return_rate"])
        out.append(
            {
                "placement": int(row["placement"]),
                "support_signature": str(row["support_signature"]),
                "core_shell_label": str(row["core_shell_label"]),
                "full_label": str(row["full_label"]),
                "full_coarse_return_rate": coarse_return,
                "core_share_of_union": core_share,
                "shell_share_of_union": shell_share,
                "rare_share_of_union": rare_share,
                "shell_plus_rare_share": shell_plus_rare_share,
                "core_to_shell_ratio": core_to_shell,
                "tail_density": tail_density,
                "tail_union_nodes": tail_union_nodes,
                "mode_label": classify_mode(
                    coarse_return=coarse_return,
                    core_share=core_share,
                    shell_plus_rare_share=shell_plus_rare_share,
                    core_to_shell=core_to_shell,
                    tail_density=tail_density,
                    rare_share=rare_share,
                    tail_union_nodes=tail_union_nodes,
                ),
            }
        )
    return out


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        out.append(
            {
                "placement": int(row["placement"]),
                "mode_label": str(row["mode_label"]),
                "full_coarse_return_rate": safe_float(row["full_coarse_return_rate"]),
                "shell_plus_rare_share": safe_float(row["shell_plus_rare_share"]),
                "core_to_shell_ratio": safe_float(row["core_to_shell_ratio"]),
                "tail_density": safe_float(row["tail_density"]),
                "tail_union_nodes": safe_float(row["tail_union_nodes"]),
            }
        )
    return out


def diagnosis_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    labels = {str(row["mode_label"]) for row in rows}
    if len(labels) == len(rows):
        status = "growth202_mode_map_supported"
        note = "De fire growth_seed-202-plasseringene fyller fire ulike lokale modi i stedet for a kollapse til én diffus restkategori."
        next_step = "compare_p3_to_other_202_modes"
        next_note = "Neste steg bør forklare hvorfor p3 velger komprimert shell-retur mens p1 og p2 velger andre diffuse modi."
    else:
        status = "growth202_mode_map_partly_split"
        note = "Growth_seed-202-familien ser strukturert ut, men minst to plasseringer havner fortsatt i samme lokale modus."
        next_step = "refine_growth202_boundary"
        next_note = "Neste steg bør splitte den gjenværende overlappen inne i growth_seed 202."
    return [
        {
            "diagnostic_family": "growth202_mode_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, rows: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bb: local_swap growth202 mode map")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden sjekker om de fire plasseringene inne i `target 96`, `growth_seed 202` faktisk fyller forskjellige lokale modi, i stedet for bare ulike grader av samme diffuse restkategori.")
    lines.append("")
    lines.append("## Placement map")
    lines.append("")
    lines.append("| placement | support | core-shell label | coarse return | shell+rare | core/shell | tail density | tail union | mode |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {int(row['placement'])} | {row['support_signature']} | {row['core_shell_label']} | {fmt(row['full_coarse_return_rate'])} | {fmt(row['shell_plus_rare_share'])} | {fmt(row['core_to_shell_ratio'])} | {fmt(row['tail_density'])} | {fmt(row['tail_union_nodes'],1)} | {row['mode_label']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren forklaringsrunde inne i growth_seed 202, ikke en ny simulering.")
    lines.append("- Les dette som et lite moduskart for én lokal familie, ikke som en bred lov for local_swap.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bb local_swap growth202 mode map.")
    p.add_argument("--in-runs-csv", type=str, default=str(RUNS_CSV))
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15bb_local_swap_growth202_mode_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15bb_local_swap_growth202_mode_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bb_local_swap_growth202_mode_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bb_local_swap_growth202_mode_map.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bb_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bb.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_rows = read_csv(Path(args.in_runs_csv))
    rows = mode_rows(run_rows)
    aggregate = aggregate_rows(rows)
    diagnosis = diagnosis_rows(rows)
    report_md = build_report(rows=rows, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bb operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som et lite moduskart inne i growth_seed 202, ikke som en ny bred scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bb",
            "",
            "Denne runden ser bare på én liten familie av tilfeller og sjekker om de fire plasseringene faktisk oppfører seg som fire forskjellige lokale modi.",
            "",
            "Det er nyttig fordi det kan gjøre det lettere å forklare hvorfor ett tilfelle holder shell-retur, et annet blir mer dissipativt, og et tredje holder mer kjerne.",
        ]
    ) + "\n"
    write_csv(args.out_rows_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
