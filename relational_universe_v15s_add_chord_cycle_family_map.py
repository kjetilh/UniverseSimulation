#!/usr/bin/env python3
"""v0.15s add_chord cycle-family mapping around the surviving long-horizon trace.

This is a deliberately narrow follow-up to v15r. It keeps the same regime and
the same base family, but maps the local placement corridor around the one
profile that held full-horizon cyclic return: target 48, growth seed 202.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 48
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2, 3)
PREFIX_STEPS = 1280
FULL_STEPS = 2560
LOG_EVERY = 8


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def subset_trace(
    log_rows: Sequence[Dict[str, Any]],
    damaged_sets: Sequence[set[int]],
    max_step: int,
) -> Tuple[List[Dict[str, Any]], List[set[int]]]:
    sub_rows: List[Dict[str, Any]] = []
    sub_sets: List[set[int]] = []
    for row, damaged in zip(log_rows, damaged_sets):
        if int(row["step"]) <= max_step:
            sub_rows.append(dict(row))
            sub_sets.append(set(damaged))
    return sub_rows, sub_sets


def transition_label(prefix_label: str, full_label: str) -> str:
    if prefix_label == "cyclic_return" and full_label == "cyclic_return":
        return "sustained_cyclic_return"
    if prefix_label == "cyclic_return" and full_label == "morphology_return":
        return "cyclic_softens_to_morphology_return"
    if prefix_label == "morphology_return" and full_label == "cyclic_return":
        return "morphology_tips_to_cycle"
    if prefix_label == "morphology_return" and full_label == "morphology_return":
        return "sustained_morphology_return"
    if full_label == "extinct_after_return":
        return "return_then_extinction"
    if full_label == "drifting_tail":
        return "return_decay"
    return "mixed_transition"


def run_rows(*, base_state: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    for placement in PLACEMENTS:
        run_seed = TARGET * 100000 + GROWTH_SEED * 1000 + int(placement)
        res = v15q.run_defect_with_sets(
            base_state,
            params=params,
            seed=run_seed,
            steps=FULL_STEPS,
            perturbation="add_chord",
            center_token_index=placement,
            local_coupling="maximal",
            log_every=LOG_EVERY,
        )
        info = dict(res["perturbation_info"])
        actual = str(info.get("type", "unknown"))
        support = list(info.get("support", []))
        requested_match = 1 if v15.v14.perturbation_requested_match("add_chord", actual) else 0

        prefix_rows, prefix_sets = subset_trace(res["log_rows"], res["damaged_sets"], PREFIX_STEPS)
        prefix_metrics = v15q.recurrence_metrics(prefix_rows, prefix_sets)
        full_metrics = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
        prefix_label = v15q.classify_recurrence_label(int(prefix_rows[-1]["alive"]), prefix_metrics)
        full_label = v15q.classify_recurrence_label(int(res["log_rows"][-1]["alive"]), full_metrics)

        rows.append(
            {
                "target_nodes": TARGET,
                "growth_seed": GROWTH_SEED,
                "placement": int(placement),
                "run_seed": int(run_seed),
                "requested_match": int(requested_match),
                "support_signature": ",".join(str(x) for x in support),
                "prefix_label": prefix_label,
                "full_label": full_label,
                "transition_label": transition_label(prefix_label, full_label),
                "prefix_exact_return_rate": safe_float(prefix_metrics["exact_return_rate"]),
                "prefix_coarse_return_rate": safe_float(prefix_metrics["coarse_return_rate"]),
                "prefix_max_exact_return_jaccard": safe_float(prefix_metrics["max_exact_return_jaccard"]),
                "full_exact_return_rate": safe_float(full_metrics["exact_return_rate"]),
                "full_coarse_return_rate": safe_float(full_metrics["coarse_return_rate"]),
                "full_max_exact_return_jaccard": safe_float(full_metrics["max_exact_return_jaccard"]),
                "full_first_exact_return_step": safe_float(full_metrics["first_exact_return_step"]),
                "full_first_coarse_return_step": safe_float(full_metrics["first_coarse_return_step"]),
            }
        )
    return rows


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    by_place = {int(row["placement"]): row for row in rows}
    cyclic_places = sorted(int(row["placement"]) for row in rows if str(row["full_label"]) == "cyclic_return")
    strongest = max(rows, key=lambda row: (safe_float(row["full_exact_return_rate"]), safe_float(row["full_coarse_return_rate"])))
    strongest_place = int(strongest["placement"])
    strongest_exact = safe_float(strongest["full_exact_return_rate"])
    p2_is_cyclic = 2 in cyclic_places
    immediate_neighbor_cycles = sum(1 for p in (1, 3) if p in cyclic_places)
    if p2_is_cyclic and immediate_neighbor_cycles >= 1:
        status = "local_cycle_band"
        note = "Det overlevende cycle-signalet sprer seg til minst én umiddelbar naboprofil på samme base."
        next_step = "probe_cycle_band"
        next_note = "Neste steg bør være en enda smalere kartlegging bare rundt det lokale cycle-båndet."
    elif p2_is_cyclic and strongest_place == 2:
        status = "single_cycle_center"
        note = "Plassering 2 er fortsatt den sterkeste lokale cycle-kandidaten, mens flankene holder lavere eller bare morfologisk retur."
        next_step = "probe_single_center"
        next_note = "Neste steg bør være en finere lokal test rundt plassering 2 alene."
    elif cyclic_places:
        status = "shifted_cycle_hint"
        note = "Cycle-signalet finnes fortsatt, men ser ut til å ligge forskjøvet i den lokale familien heller enn rent sentrert på plassering 2."
        next_step = "follow_shifted_cycle"
        next_note = "Neste steg bør følge den faktisk sterkeste lokale cycle-plasseringen, ikke låse seg til p2."
    else:
        status = "cycle_not_supported"
        note = "Den lokale family-mapen støtter ikke et robust cycle-spor på full horisont i denne smale korridoren."
        next_step = "pivot_again"
        next_note = "Neste steg bør være et annet smalt defect-spørsmål enn videre cycle-mapping langs denne aksen."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er rent separert og alle lokale add_chord-profiler matcher ønsket perturbasjonstype."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "cycle_family_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "strongest_profile",
            "status": f"p{strongest_place}",
            "note": f"Sterkeste full-horisontprofil er plassering {strongest_place} med full_exact_return_rate={fmt(strongest_exact)}.",
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(
    *,
    target_summary: Sequence[Dict[str, Any]],
    rows: Sequence[Dict[str, Any]],
    diagnosis: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15s: add_chord cycle-family map")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden kartlegger bare den lokale `add_chord`-familien rundt den ene profilen som holdt ekte `cyclic_return` i `v15r`."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        if int(row["target_nodes"]) != TARGET:
            continue
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Local family map")
    lines.append("")
    lines.append("| placement | support | prefix | full | transition | prefix exact | full exact | full coarse |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {int(row['placement'])} | {row['support_signature']} | {row['prefix_label']} | {row['full_label']} | {row['transition_label']} | {fmt(row['prefix_exact_return_rate'])} | {fmt(row['full_exact_return_rate'])} | {fmt(row['full_coarse_return_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren local family-map på samme base, ikke en ny sweep.")
    lines.append("- Les dette som recurrence i ett smalt add_chord-område, ikke som generell cycle-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15s add_chord cycle-family map.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15s_add_chord_cycle_family_runs.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15s_add_chord_cycle_family_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15s_add_chord_cycle_family_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15s_add_chord_cycle_family_map.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15s_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15s.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    rows = run_rows(base_state=base_state)
    diagnosis = diagnosis_rows(target_summary, rows)
    report_md = build_report(target_summary=target_summary, rows=rows, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15s operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in diagnosis
            ],
            "",
            "- Les denne runden som en smal add_chord cycle-family map, ikke som bevis for en generell sykluslov.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15s",
            "",
            "Denne runden sjekker om den ene lovende add_chord-skaden fra forrige runde er et helt isolert tilfelle eller del av en liten lokal familie.",
            "",
            "Poenget er å finne ut om cycle-signalet bare finnes på ett punkt, eller om det holder i et lite nabolag rundt det.",
        ]
    ) + "\n"
    write_csv(args.out_runs_csv, rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
