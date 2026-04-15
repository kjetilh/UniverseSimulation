#!/usr/bin/env python3
"""v0.15ay local_swap 96-pocket explainer.

This round does not run new simulations. It uses the v15aw local_swap
core-shell rows plus local support geometry to explain why one 96-case still
looks core+shell-like while the rest mostly drift into diffuse shell behavior.
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
    label = str(row["core_shell_label"])
    if growth_seed == 101 and placement == 3 and label == "stable_core_variable_shell":
        return "pocket_anchor"
    if placement == 3 and growth_seed == 202:
        return "same_placement_diffuse_control"
    if growth_seed == 101 and placement == 1:
        return "compact_nonpocket_control"
    if growth_seed == 202 and placement == 0:
        return "high_core_nonpocket_control"
    return "background_nonpocket"


def explainer_rows(run_rows: Sequence[Mapping[str, str]], base_states: Mapping[Tuple[str, int], Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    ens_name = v15.deep_ensembles([TARGET])[0].name
    for row in run_rows:
        if int(row["target_nodes"]) != TARGET:
            continue
        growth_seed = int(row["growth_seed"])
        base_state = base_states[(ens_name, growth_seed)]
        support = [int(x) for x in str(row["support_signature"]).split(",") if x]
        geom = v14c.support_geometry_features(base_state, support)
        out.append(
            {
                "growth_seed": growth_seed,
                "placement": int(row["placement"]),
                "role": role_for(row),
                "support_signature": str(row["support_signature"]),
                "core_shell_label": str(row["core_shell_label"]),
                "mean_support_degree": safe_float(geom["mean_support_degree"]),
                "support_ball_1": safe_float(geom["support_ball_1"]),
                "support_ball_2": safe_float(geom["support_ball_2"]),
                "support_ball_3": safe_float(geom["support_ball_3"]),
                "shell2_over_shell1": safe_float(geom["shell2_over_shell1"]),
                "ball3_over_ball1": safe_float(geom["ball3_over_ball1"]),
                "core_share_of_union": safe_float(row["core_share_of_union"]),
                "shell_share_of_union": safe_float(row["shell_share_of_union"]),
                "rare_share_of_union": safe_float(row["rare_share_of_union"]),
                "mean_core_cover": safe_float(row["mean_core_cover"]),
                "mean_shell_cover": safe_float(row["mean_shell_cover"]),
                "mean_tail_damage_nodes": safe_float(row["mean_tail_damage_nodes"]),
                "tail_union_nodes": int(row["tail_union_nodes"]),
                "full_exact_return_rate": safe_float(row["full_exact_return_rate"]),
                "full_coarse_return_rate": safe_float(row["full_coarse_return_rate"]),
            }
        )
    return out


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for role in (
        "pocket_anchor",
        "same_placement_diffuse_control",
        "compact_nonpocket_control",
        "high_core_nonpocket_control",
        "background_nonpocket",
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
                "mean_support_degree": mean_defined(safe_float(row["mean_support_degree"]) for row in group),
                "mean_ball3_over_ball1": mean_defined(safe_float(row["ball3_over_ball1"]) for row in group),
                "mean_core_share_of_union": mean_defined(safe_float(row["core_share_of_union"]) for row in group),
                "mean_shell_share_of_union": mean_defined(safe_float(row["shell_share_of_union"]) for row in group),
                "mean_rare_share_of_union": mean_defined(safe_float(row["rare_share_of_union"]) for row in group),
                "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in group),
            }
        )
    return out


def diagnosis_rows(rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    def one(role: str) -> Dict[str, Any]:
        return next(row for row in aggregate if str(row["role"]) == role)

    pocket = one("pocket_anchor")
    same_place = one("same_placement_diffuse_control")
    compact = one("compact_nonpocket_control")
    background = one("background_nonpocket")

    pocket_compact = safe_float(pocket["mean_ball3_over_ball1"]) < min(
        safe_float(same_place["mean_ball3_over_ball1"]),
        safe_float(compact["mean_ball3_over_ball1"]),
        safe_float(background["mean_ball3_over_ball1"]),
    )
    pocket_low_rare = safe_float(pocket["mean_rare_share_of_union"]) <= min(
        safe_float(same_place["mean_rare_share_of_union"]),
        safe_float(background["mean_rare_share_of_union"]),
    )
    same_place_flip = safe_float(pocket["stable_core_shell_rate"]) > safe_float(same_place["stable_core_shell_rate"])

    if pocket_compact and pocket_low_rare and same_place_flip:
        status = "compact_low_rare_pocket_supported"
        note = "96-lommen ser best ut som et kompakt støttecase med dempet rare-turnover. Samme placement ved growth_seed 202 holder ikke, så placement alene er ikke forklaringen."
        next_step = "explain_seed_flip_within_p3"
        next_note = "Neste steg bør sammenligne growth_seed 101 og 202 direkte innen placement 3, siden det er der pocketen faktisk lever eller dør."
    else:
        status = "pocket_still_partly_mixed"
        note = "96-lommen er reell, men forklaringen gjennom kompakt støtte og rare-share er ikke ren nok ennå."
        next_step = "stay_local_on_96_pocket"
        next_note = "Neste steg bør holde seg på denne ene lommen, ikke åpne en bred size-scan igjen."

    return [
        {
            "diagnostic_family": "pocket_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "placement_sufficiency",
            "status": "placement_not_sufficient" if same_place_flip else "placement_maybe_sufficient",
            "note": (
                "Placement 3 gir ikke pocket automatisk; growth_seed 202 faller tilbake til diffuse_shell_recurrence."
                if same_place_flip
                else "Samme placement holder omtrent samme regime på tvers av growth-seeds."
            ),
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15ay: local_swap 96-pocket explainer")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden forklarer den ene `96`-lommen i v15aw som fortsatt holder `stable_core_variable_shell`, og sammenligner den med noen få nære ikke-lommer.")
    lines.append("")
    lines.append("## Case rows")
    lines.append("")
    lines.append("| role | growth_seed | placement | label | support | mean degree | ball3/ball1 | core share | shell share | rare share | coarse return |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {row['role']} | {int(row['growth_seed'])} | {int(row['placement'])} | {row['core_shell_label']} | {row['support_signature']} | {fmt(row['mean_support_degree'])} | {fmt(row['ball3_over_ball1'])} | {fmt(row['core_share_of_union'])} | {fmt(row['shell_share_of_union'])} | {fmt(row['rare_share_of_union'])} | {fmt(row['full_coarse_return_rate'])} |"
        )
    lines.append("")
    lines.append("## Role summary")
    lines.append("")
    lines.append("| role | n | stable core+shell | diffuse shell | mean degree | mean ball3/ball1 | mean core share | mean rare share | mean coarse return |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['role']} | {int(row['n_runs'])} | {fmt(row['stable_core_shell_rate'])} | {fmt(row['diffuse_shell_rate'])} | {fmt(row['mean_support_degree'])} | {fmt(row['mean_ball3_over_ball1'])} | {fmt(row['mean_core_share_of_union'])} | {fmt(row['mean_rare_share_of_union'])} | {fmt(row['mean_full_coarse_return_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren forklaringsrunde pa toppen av v15aw og v15ax, ikke en ny simulering.")
    lines.append("- Les dette som en forklaring av den ene `96`-lommen, ikke som en ny stor law for local_swap.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ay local_swap 96-pocket explainer.")
    p.add_argument("--in-runs-csv", type=str, default=str(RUNS_CSV))
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15ay_local_swap_96_pocket_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ay_local_swap_96_pocket_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ay_local_swap_96_pocket_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ay_local_swap_96_pocket_explainer.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ay_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ay.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_rows = read_csv(Path(args.in_runs_csv))
    base_states = load_base_states()
    rows = explainer_rows(run_rows, base_states)
    aggregate = aggregate_rows(rows)
    diagnosis = diagnosis_rows(rows, aggregate)
    report_md = build_report(rows=rows, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15ay operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en liten forklaring av `96`-lommen, ikke som en ny size-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15ay",
            "",
            "Denne runden forklarer hvorfor ett lite `96`-tilfelle fortsatt ser ryddig ut i local_swap-sporet, mens de fleste andre `96`-tilfellene blir mer diffuse.",
            "",
            "Målet er å finne ut om dette lille unntaket ser ut som ren tilfeldighet, eller om det har en lesbar lokal forklaring.",
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
