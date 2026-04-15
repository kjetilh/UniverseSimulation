#!/usr/bin/env python3
"""v0.15bc local_swap p3-vs-p1-p2 contrast.

This round does not run new simulations. It takes the growth_seed-202 mode map
from v15bb and makes the two most informative contrasts explicit:

- why p3 is not just a weaker p1
- why p3 is not just a slightly cleaner p2
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v15_defect_lifetime_lab as v15


RUNS_CSV = Path("Documentation/v15aw_local_swap_core_shell_runs.csv")
TARGET = 96
GROWTH_SEED = 202
PLACEMENTS = (1, 2, 3)


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


def placement_rows(run_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in run_rows:
        if int(row["target_nodes"]) != TARGET or int(row["growth_seed"]) != GROWTH_SEED:
            continue
        placement = int(row["placement"])
        if placement not in PLACEMENTS:
            continue
        core_share = safe_float(row["core_share_of_union"])
        shell_share = safe_float(row["shell_share_of_union"])
        rare_share = safe_float(row["rare_share_of_union"])
        core_nodes = safe_float(row["core_nodes"])
        shell_nodes = safe_float(row["shell_nodes"])
        tail_union = max(1.0, safe_float(row["tail_union_nodes"]))
        mean_tail = safe_float(row["mean_tail_damage_nodes"])
        out.append(
            {
                "placement": placement,
                "support_signature": str(row["support_signature"]),
                "core_shell_label": str(row["core_shell_label"]),
                "full_coarse_return_rate": safe_float(row["full_coarse_return_rate"]),
                "core_share_of_union": core_share,
                "shell_share_of_union": shell_share,
                "rare_share_of_union": rare_share,
                "shell_plus_rare_share": shell_share + rare_share,
                "core_to_shell_ratio": core_nodes / max(1.0, shell_nodes),
                "tail_density": mean_tail / tail_union,
                "tail_union_nodes": tail_union,
            }
        )
    return sorted(out, key=lambda r: int(r["placement"]))


def classify_pair(*, base: Mapping[str, Any], other: Mapping[str, Any]) -> str:
    coarse_gap = safe_float(base["full_coarse_return_rate"]) - safe_float(other["full_coarse_return_rate"])
    shell_gap = safe_float(base["shell_plus_rare_share"]) - safe_float(other["shell_plus_rare_share"])
    density_gap = safe_float(base["tail_density"]) - safe_float(other["tail_density"])
    rare_gap = safe_float(base["rare_share_of_union"]) - safe_float(other["rare_share_of_union"])
    union_gap = safe_float(base["tail_union_nodes"]) - safe_float(other["tail_union_nodes"])

    if coarse_gap > -0.30 and coarse_gap < 0.0 and shell_gap >= 0.10 and density_gap <= -0.06 and union_gap <= -20.0:
        return "compressed_vs_wide_retention"
    if coarse_gap >= 0.15 and rare_gap <= -0.08 and density_gap >= 0.08:
        return "retained_vs_dissipative_shell"
    return "mixed_pair_contrast"


def pair_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_placement = {int(row["placement"]): row for row in rows}
    p3 = by_placement[3]
    out: List[Dict[str, Any]] = []
    for other_placement in (1, 2):
        other = by_placement[other_placement]
        out.append(
            {
                "base_placement": 3,
                "other_placement": other_placement,
                "pair_label": f"p3_vs_p{other_placement}",
                "contrast_label": classify_pair(base=p3, other=other),
                "coarse_return_gap": safe_float(p3["full_coarse_return_rate"]) - safe_float(other["full_coarse_return_rate"]),
                "shell_plus_rare_gap": safe_float(p3["shell_plus_rare_share"]) - safe_float(other["shell_plus_rare_share"]),
                "core_to_shell_gap": safe_float(p3["core_to_shell_ratio"]) - safe_float(other["core_to_shell_ratio"]),
                "tail_density_gap": safe_float(p3["tail_density"]) - safe_float(other["tail_density"]),
                "tail_union_gap": safe_float(p3["tail_union_nodes"]) - safe_float(other["tail_union_nodes"]),
                "rare_share_gap": safe_float(p3["rare_share_of_union"]) - safe_float(other["rare_share_of_union"]),
            }
        )
    return out


def diagnosis_rows(pair_rows_out: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    labels = {str(row["contrast_label"]) for row in pair_rows_out}
    if labels == {"compressed_vs_wide_retention", "retained_vs_dissipative_shell"}:
        status = "p3_boundary_contrast_supported"
        note = "P3 skiller seg fra p1 og p2 langs to forskjellige akser: kompresjon mot bred retention, og retention mot dissipativ rare-shell."
        next_step = "look_for_shared_trigger_axis"
        next_note = "Neste steg bør lete etter én liten triggerakse som avgjør om samme diffuse regime blir bred retention, komprimert shell-retur eller dissipativ rare-shell."
    else:
        status = "p3_boundary_contrast_partly_mixed"
        note = "P3 ser informativ ut, men minst én av kontrastene mot p1/p2 er fortsatt for uklar."
        next_step = "refine_pairwise_contrast"
        next_note = "Neste steg bør holde seg på denne p3-vs-p1/p2-aksen og forbedre observabelen."
    return [
        {
            "diagnostic_family": "p3_boundary_contrast",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, rows: Sequence[Dict[str, Any]], pair_rows_out: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bc: local_swap p3-vs-p1-p2 contrast")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden forklarer hva som faktisk skiller `p3` fra de to mest informative nabomodusene i `growth_seed 202`: `p1` og `p2`.")
    lines.append("")
    lines.append("## Placement snapshot")
    lines.append("")
    lines.append("| placement | label | coarse return | shell+rare | core/shell | tail density | tail union |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {int(row['placement'])} | {row['core_shell_label']} | {fmt(row['full_coarse_return_rate'])} | {fmt(row['shell_plus_rare_share'])} | {fmt(row['core_to_shell_ratio'])} | {fmt(row['tail_density'])} | {fmt(row['tail_union_nodes'],1)} |"
        )
    lines.append("")
    lines.append("## Pairwise contrasts")
    lines.append("")
    lines.append("| pair | contrast | coarse gap | shell+rare gap | core/shell gap | tail density gap | tail union gap | rare gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in pair_rows_out:
        lines.append(
            f"| {row['pair_label']} | {row['contrast_label']} | {fmt(row['coarse_return_gap'])} | {fmt(row['shell_plus_rare_gap'])} | {fmt(row['core_to_shell_gap'])} | {fmt(row['tail_density_gap'])} | {fmt(row['tail_union_gap'],1)} | {fmt(row['rare_share_gap'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren kontrastanalyse inne i `growth_seed 202`, ikke en ny simulering.")
    lines.append("- Les dette som en forklaring av p3-grensen mot to naere modi, ikke som en bred ny local_swap-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bc local_swap p3-vs-p1-p2 contrast.")
    p.add_argument("--in-runs-csv", type=str, default=str(RUNS_CSV))
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15bc_local_swap_p3_vs_p1_p2_rows.csv")
    p.add_argument("--out-pairs-csv", type=str, default="Documentation/v15bc_local_swap_p3_vs_p1_p2_pairs.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bc_local_swap_p3_vs_p1_p2_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bc_local_swap_p3_vs_p1_p2_contrast.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bc_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bc.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_rows = read_csv(Path(args.in_runs_csv))
    rows = placement_rows(run_rows)
    pair_rows_out = pair_rows(rows)
    diagnosis = diagnosis_rows(pair_rows_out)
    report_md = build_report(rows=rows, pair_rows_out=pair_rows_out, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bc operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en p3-vs-p1/p2-kontrast, ikke som en ny bred defect-kjøring.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bc",
            "",
            "Denne runden sammenligner den ene shell-returmodusen direkte med to andre nærliggende modi for å se hva som faktisk skiller dem.",
            "",
            "Målet er å finne ut om forskjellen handler om bredde, hvor mye som bevares, eller hvor mye systemet glir over i mer dissipativ randstøy.",
        ]
    ) + "\n"
    write_csv(args.out_rows_csv, rows)
    write_csv(args.out_pairs_csv, pair_rows_out)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
