#!/usr/bin/env python3
"""v0.15az local_swap p3 seed-flip explainer.

This round does not run new simulations. It focuses only on the target-96,
placement-3 local_swap flip identified by v15ay and asks a more precise
question:

is the 101-vs-202 flip best read as a support-geometry flip, or as a
core-amplification flip inside the same placement?
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15


TARGET = 96
PLACEMENT = 3
GROWTH_SEEDS = (101, 202)
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


def load_base_states() -> Mapping[Tuple[str, int], Any]:
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, _ = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    return base_states


def role_for(row: Mapping[str, str]) -> str:
    growth_seed = int(row["growth_seed"])
    placement = int(row["placement"])
    if growth_seed == 101 and placement == 3:
        return "p3_pocket_anchor"
    if growth_seed == 202 and placement == 3:
        return "p3_diffuse_flip"
    if growth_seed == 202 and placement == 0:
        return "high_amplification_nonpocket"
    return "context_control"


def explainer_rows(run_rows: Sequence[Mapping[str, str]], base_states: Mapping[Tuple[str, int], Any]) -> List[Dict[str, Any]]:
    ens_name = v15.deep_ensembles([TARGET])[0].name
    out: List[Dict[str, Any]] = []
    for row in run_rows:
        if int(row["target_nodes"]) != TARGET:
            continue
        growth_seed = int(row["growth_seed"])
        base_state = base_states[(ens_name, growth_seed)]
        support = [int(x) for x in str(row["support_signature"]).split(",") if x]
        geom = v14c.support_geometry_features(base_state, support)
        ball1 = max(1.0, safe_float(geom["support_ball_1"]))
        core_nodes = safe_float(row["core_nodes"])
        shell_nodes = safe_float(row["shell_nodes"])
        rare_nodes = safe_float(row["rare_nodes"])
        mean_tail_damage_nodes = safe_float(row["mean_tail_damage_nodes"])
        out.append(
            {
                "growth_seed": growth_seed,
                "placement": int(row["placement"]),
                "role": role_for(row),
                "support_signature": str(row["support_signature"]),
                "core_shell_label": str(row["core_shell_label"]),
                "mean_support_degree": safe_float(geom["mean_support_degree"]),
                "support_ball_1": ball1,
                "support_ball_2": safe_float(geom["support_ball_2"]),
                "support_ball_3": safe_float(geom["support_ball_3"]),
                "ball3_over_ball1": safe_float(geom["ball3_over_ball1"]),
                "core_nodes": core_nodes,
                "shell_nodes": shell_nodes,
                "rare_nodes": rare_nodes,
                "mean_tail_damage_nodes": mean_tail_damage_nodes,
                "core_share_of_union": safe_float(row["core_share_of_union"]),
                "shell_share_of_union": safe_float(row["shell_share_of_union"]),
                "rare_share_of_union": safe_float(row["rare_share_of_union"]),
                "full_coarse_return_rate": safe_float(row["full_coarse_return_rate"]),
                "core_nodes_per_ball1": core_nodes / ball1,
                "shell_nodes_per_ball1": shell_nodes / ball1,
                "rare_nodes_per_ball1": rare_nodes / ball1,
                "tail_nodes_per_ball1": mean_tail_damage_nodes / ball1,
                "core_to_shell_ratio": core_nodes / max(1.0, shell_nodes),
            }
        )
    return out


def summary_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for role in ("p3_pocket_anchor", "p3_diffuse_flip", "high_amplification_nonpocket", "context_control"):
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
                "mean_ball3_over_ball1": mean_defined(safe_float(row["ball3_over_ball1"]) for row in group),
                "mean_core_nodes_per_ball1": mean_defined(safe_float(row["core_nodes_per_ball1"]) for row in group),
                "mean_tail_nodes_per_ball1": mean_defined(safe_float(row["tail_nodes_per_ball1"]) for row in group),
                "mean_core_to_shell_ratio": mean_defined(safe_float(row["core_to_shell_ratio"]) for row in group),
                "mean_rare_share_of_union": mean_defined(safe_float(row["rare_share_of_union"]) for row in group),
                "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in group),
            }
        )
    return out


def diagnosis_rows(summary: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_role = {str(row["role"]): row for row in summary}
    pocket = by_role["p3_pocket_anchor"]
    flip = by_role["p3_diffuse_flip"]
    high_amp = by_role["high_amplification_nonpocket"]

    geometry_close = abs(safe_float(pocket["mean_ball3_over_ball1"]) - safe_float(flip["mean_ball3_over_ball1"])) <= 0.25
    amp_gap = safe_float(pocket["mean_core_nodes_per_ball1"]) - safe_float(flip["mean_core_nodes_per_ball1"])
    tail_gap = safe_float(pocket["mean_tail_nodes_per_ball1"]) - safe_float(flip["mean_tail_nodes_per_ball1"])
    rare_gap = safe_float(flip["mean_rare_share_of_union"]) - safe_float(pocket["mean_rare_share_of_union"])
    high_amp_nonpocket = safe_float(high_amp["mean_core_nodes_per_ball1"]) > safe_float(pocket["mean_core_nodes_per_ball1"])

    if geometry_close and amp_gap >= 2.0 and tail_gap >= 2.5 and rare_gap >= 0.15:
        status = "p3_seed_flip_is_core_amplification_flip"
        note = "De to p3-casene ligger relativt naert i kompakthetsgeometri, men skiller lag hardt i hvor mye støtteområdet faktisk blåses opp til stor, vedvarende kjerne og hale."
        next_step = "explain_why_202_p3_stays_compressed"
        next_note = "Neste steg bør forklare hva som holder `202/p3` komprimert, siden placement-geometrien alene ikke gjør jobben."
    else:
        status = "p3_seed_flip_still_partly_mixed"
        note = "P3-flippen ser reell ut, men geometrinærhet og amplifikasjonsgap er ikke rene nok ennå til én enkel mekanistisk lesning."
        next_step = "stay_inside_p3"
        next_note = "Neste steg bør fortsatt holde seg inne i placement 3, ikke åpne bredere size- eller placement-scan."

    high_amp_note = (
        "Det finnes minst ett ikke-pocket-case med enda høyere core-forsterkning, så forsterkning alene er ikke en full forklaring."
        if high_amp_nonpocket
        else "Ingen ikke-pocket-kontroller overgår pocketen på core-forsterkning."
    )

    return [
        {
            "diagnostic_family": "seed_flip_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "amplification_scope",
            "status": "amplification_not_sufficient_globally" if high_amp_nonpocket else "amplification_mostly_specific",
            "note": high_amp_note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, rows: Sequence[Dict[str, Any]], summary: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15az: local_swap p3 seed-flip explainer")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden forklarer hvorfor `placement 3` ved `target 96` holder som en liten core+shell-lomme ved `growth_seed 101`, men ikke ved `growth_seed 202`.")
    lines.append("")
    lines.append("## Case rows")
    lines.append("")
    lines.append("| role | growth_seed | placement | label | support | ball3/ball1 | core/ball1 | tail/ball1 | core/shell | rare share | coarse return |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {row['role']} | {int(row['growth_seed'])} | {int(row['placement'])} | {row['core_shell_label']} | {row['support_signature']} | {fmt(row['ball3_over_ball1'])} | {fmt(row['core_nodes_per_ball1'])} | {fmt(row['tail_nodes_per_ball1'])} | {fmt(row['core_to_shell_ratio'])} | {fmt(row['rare_share_of_union'])} | {fmt(row['full_coarse_return_rate'])} |"
        )
    lines.append("")
    lines.append("## Role summary")
    lines.append("")
    lines.append("| role | n | stable core+shell | diffuse shell | mean ball3/ball1 | mean core/ball1 | mean tail/ball1 | mean core/shell | mean rare share | mean coarse return |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in summary:
        lines.append(
            f"| {row['role']} | {int(row['n_runs'])} | {fmt(row['stable_core_shell_rate'])} | {fmt(row['diffuse_shell_rate'])} | {fmt(row['mean_ball3_over_ball1'])} | {fmt(row['mean_core_nodes_per_ball1'])} | {fmt(row['mean_tail_nodes_per_ball1'])} | {fmt(row['mean_core_to_shell_ratio'])} | {fmt(row['mean_rare_share_of_union'])} | {fmt(row['mean_full_coarse_return_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren forklaringsrunde pa toppen av v15aw-v15ay, ikke en ny simulering.")
    lines.append("- Les dette som en forklaring av seed-flippen inne i `p3`, ikke som en ny generell lov for local_swap.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15az local_swap p3 seed-flip explainer.")
    p.add_argument("--in-runs-csv", type=str, default=str(RUNS_CSV))
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15az_local_swap_p3_seed_flip_rows.csv")
    p.add_argument("--out-summary-csv", type=str, default="Documentation/v15az_local_swap_p3_seed_flip_summary.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15az_local_swap_p3_seed_flip_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15az_local_swap_p3_seed_flip_explainer.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15az_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15az.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_rows = read_csv(Path(args.in_runs_csv))
    base_states = load_base_states()
    rows = explainer_rows(run_rows, base_states)
    summary = summary_rows(rows)
    diagnosis = diagnosis_rows(summary)
    report_md = build_report(rows=rows, summary=summary, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15az operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en forklaring av `p3` seed-flippen, ikke som en ny bred local_swap-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15az",
            "",
            "Denne runden forklarer hvorfor akkurat samme lokale plassering i en litt større graf noen ganger holder en ryddig kjerne, og andre ganger glir over i en mer diffus randform.",
            "",
            "Målet er å skille mellom ren lokal geometri og hvor mye skaden faktisk vokser inn i en større vedvarende kjerne.",
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
