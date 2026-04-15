#!/usr/bin/env python3
"""v0.15ba local_swap compressed-shell explainer.

This round does not run new simulations. It follows v15az and asks:

is the `202/p3` local_swap flip best read as a compressed shell-return mode
rather than just a weak or failed pocket?
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

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


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def role_for(row: Mapping[str, str]) -> str:
    growth_seed = int(row["growth_seed"])
    placement = int(row["placement"])
    if growth_seed == 101 and placement == 3:
        return "pocket_anchor"
    if growth_seed == 202 and placement == 3:
        return "compressed_flip_candidate"
    if growth_seed == 202 and placement == 1:
        return "high_coarse_diffuse_control"
    if growth_seed == 202 and placement == 0:
        return "high_amplification_nonpocket"
    return "background_control"


def explainer_rows(run_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in run_rows:
        if int(row["target_nodes"]) != 96:
            continue
        core_nodes = safe_float(row["core_nodes"])
        shell_nodes = safe_float(row["shell_nodes"])
        rare_nodes = safe_float(row["rare_nodes"])
        tail_union_nodes = max(1.0, safe_float(row["tail_union_nodes"]))
        mean_tail_damage_nodes = safe_float(row["mean_tail_damage_nodes"])
        shell_plus_rare = shell_nodes + rare_nodes
        out.append(
            {
                "growth_seed": int(row["growth_seed"]),
                "placement": int(row["placement"]),
                "role": role_for(row),
                "support_signature": str(row["support_signature"]),
                "core_shell_label": str(row["core_shell_label"]),
                "full_label": str(row["full_label"]),
                "full_coarse_return_rate": safe_float(row["full_coarse_return_rate"]),
                "full_exact_return_rate": safe_float(row["full_exact_return_rate"]),
                "core_share_of_union": safe_float(row["core_share_of_union"]),
                "shell_share_of_union": safe_float(row["shell_share_of_union"]),
                "rare_share_of_union": safe_float(row["rare_share_of_union"]),
                "shell_plus_rare_share": shell_plus_rare / tail_union_nodes,
                "core_to_shell_ratio": core_nodes / max(1.0, shell_nodes),
                "tail_density": mean_tail_damage_nodes / tail_union_nodes,
                "tail_union_nodes": tail_union_nodes,
                "mean_tail_damage_nodes": mean_tail_damage_nodes,
                "mean_core_cover": safe_float(row["mean_core_cover"]),
                "mean_shell_cover": safe_float(row["mean_shell_cover"]),
            }
        )
    return out


def summary_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for role in (
        "compressed_flip_candidate",
        "pocket_anchor",
        "high_coarse_diffuse_control",
        "high_amplification_nonpocket",
        "background_control",
    ):
        group = [row for row in rows if str(row["role"]) == role]
        if not group:
            continue
        out.append(
            {
                "role": role,
                "n_runs": len(group),
                "stable_core_shell_rate": mean_defined(
                    1.0 if str(row["core_shell_label"]) == "stable_core_variable_shell" else 0.0 for row in group
                ),
                "diffuse_shell_rate": mean_defined(
                    1.0 if str(row["core_shell_label"]) == "diffuse_shell_recurrence" else 0.0 for row in group
                ),
                "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in group),
                "mean_shell_plus_rare_share": mean_defined(safe_float(row["shell_plus_rare_share"]) for row in group),
                "mean_core_to_shell_ratio": mean_defined(safe_float(row["core_to_shell_ratio"]) for row in group),
                "mean_tail_density": mean_defined(safe_float(row["tail_density"]) for row in group),
                "mean_tail_union_nodes": mean_defined(safe_float(row["tail_union_nodes"]) for row in group),
                "mean_core_cover": mean_defined(safe_float(row["mean_core_cover"]) for row in group),
            }
        )
    return out


def diagnosis_rows(summary: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_role = {str(row["role"]): row for row in summary}
    candidate = by_role["compressed_flip_candidate"]
    pocket = by_role["pocket_anchor"]
    high_coarse = by_role["high_coarse_diffuse_control"]

    shell_heavy = safe_float(candidate["mean_shell_plus_rare_share"]) >= 0.75
    low_density = safe_float(candidate["mean_tail_density"]) <= 0.50
    low_core_shell = safe_float(candidate["mean_core_to_shell_ratio"]) <= 0.60
    still_recurrent = safe_float(candidate["mean_full_coarse_return_rate"]) >= 0.60
    more_shell_heavy_than_high_coarse = safe_float(candidate["mean_shell_plus_rare_share"]) > safe_float(high_coarse["mean_shell_plus_rare_share"])
    denser_than_pocket = safe_float(pocket["mean_tail_density"]) > safe_float(candidate["mean_tail_density"])

    if shell_heavy and low_density and low_core_shell and still_recurrent and denser_than_pocket:
        status = "compressed_shell_return_supported"
        note = "`202/p3` ser ikke best ut som svak pocket. Den holder fortsatt recurrence, men i en komprimert shell-dominert modus med hoy shell+rare-andel og lav tail-density."
        next_step = "explain_shell_retention_inside_growth202"
        next_note = "Neste steg bør sammenligne `202/p3` mot andre `growth_seed 202`-caser for a forklare hvorfor akkurat denne plasseringen holder pa shell-retur."
    else:
        status = "compressed_shell_return_not_yet"
        note = "Det finnes tegn til komprimert shell-retur, men ikke rent nok til at det slar svak-pocket-lesningen."
        next_step = "stay_on_flip"
        next_note = "Neste steg bør fortsatt holde seg pa `202/p3`-flippen."

    return [
        {
            "diagnostic_family": "compressed_shell_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "relative_scope",
            "status": "shell_heavier_than_pocket" if denser_than_pocket and more_shell_heavy_than_high_coarse else "scope_mixed",
            "note": (
                "`202/p3` er mer shell-dominert enn pocket-caset og samtidig mer komprimert i tailen."
                if denser_than_pocket and more_shell_heavy_than_high_coarse
                else "`202/p3` skiller seg noe ut, men ikke rent nok i forhold til de naere kontrollene."
            ),
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, rows: Sequence[Dict[str, Any]], summary: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15ba: local_swap compressed-shell explainer")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden sjekker om `202/p3` best leses som en komprimert shell-retur, i stedet for bare som en svak eller mislykket pocket.")
    lines.append("")
    lines.append("## Case rows")
    lines.append("")
    lines.append("| role | growth_seed | placement | label | coarse return | core share | shell share | rare share | shell+rare | core/shell | tail density |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {row['role']} | {int(row['growth_seed'])} | {int(row['placement'])} | {row['core_shell_label']} | {fmt(row['full_coarse_return_rate'])} | {fmt(row['core_share_of_union'])} | {fmt(row['shell_share_of_union'])} | {fmt(row['rare_share_of_union'])} | {fmt(row['shell_plus_rare_share'])} | {fmt(row['core_to_shell_ratio'])} | {fmt(row['tail_density'])} |"
        )
    lines.append("")
    lines.append("## Role summary")
    lines.append("")
    lines.append("| role | n | stable core+shell | diffuse shell | coarse return | shell+rare | core/shell | tail density | tail union nodes |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in summary:
        lines.append(
            f"| {row['role']} | {int(row['n_runs'])} | {fmt(row['stable_core_shell_rate'])} | {fmt(row['diffuse_shell_rate'])} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_shell_plus_rare_share'])} | {fmt(row['mean_core_to_shell_ratio'])} | {fmt(row['mean_tail_density'])} | {fmt(row['mean_tail_union_nodes'],1)} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren forklaringsrunde pa toppen av v15aw-v15az, ikke en ny simulering.")
    lines.append("- Les dette som en liten modusforklaring for `202/p3`, ikke som en ny generell local_swap-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ba local_swap compressed-shell explainer.")
    p.add_argument("--in-runs-csv", type=str, default=str(RUNS_CSV))
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15ba_local_swap_compressed_shell_rows.csv")
    p.add_argument("--out-summary-csv", type=str, default="Documentation/v15ba_local_swap_compressed_shell_summary.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ba_local_swap_compressed_shell_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ba_local_swap_compressed_shell_explainer.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ba_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ba.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_rows = read_csv(Path(args.in_runs_csv))
    rows = explainer_rows(run_rows)
    summary = summary_rows(rows)
    diagnosis = diagnosis_rows(summary)
    report_md = build_report(rows=rows, summary=summary, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15ba operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en liten modusforklaring for `202/p3`, ikke som en ny broad defect-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15ba",
            "",
            "Denne runden spør om ett av de diffuse `96`-tilfellene egentlig holder en liten, komprimert randform i live, i stedet for å bygge en stor stabil kjerne.",
            "",
            "Det er nyttig fordi det kan forklare hvorfor samme type lokale skade noen ganger blir ryddig og andre ganger holder seg i en mer shell-dominert form.",
        ]
    ) + "\n"
    write_csv(args.out_rows_csv, rows)
    write_csv(args.out_summary_csv, summary)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
