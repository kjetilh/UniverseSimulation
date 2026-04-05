#!/usr/bin/env python3
"""v0.15y p0-vs-p1 case duel lab.

This round follows v15x. It does not add more seeds. It takes only the three
most informative seed cases from the existing p0/p1 local duel family:

- 151: p1 clean edge
- 239: apparent speed/stability tradeoff
- 271: p0 clean edge

The goal is to see whether these are actually repeatable local case types once
we inspect the first tail segment snapshot-by-snapshot.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 48
GROWTH_SEED = 202
PLACEMENTS = (0, 1)
SEED_DELTAS = (151, 239, 271)
FULL_STEPS = 2560
LOG_EVERY = 8


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


def segment_bounds(log_rows: Sequence[Dict[str, Any]], first_exact_step: float) -> Tuple[int, int]:
    tail_start_idx = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(log_rows))))
    if not math.isfinite(first_exact_step) or first_exact_step < 0:
        return tail_start_idx, len(log_rows) - 1
    end_idx = len(log_rows) - 1
    for idx in range(tail_start_idx, len(log_rows)):
        if safe_float(log_rows[idx]["step"]) >= first_exact_step:
            end_idx = idx
            break
    return tail_start_idx, end_idx


def run_rows(*, base_state: Any) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    run_rows_out: List[Dict[str, Any]] = []
    segment_rows_out: List[Dict[str, Any]] = []
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    for placement in PLACEMENTS:
        base_run_seed = TARGET * 100000 + GROWTH_SEED * 1000 + int(placement)
        for seed_delta in SEED_DELTAS:
            run_seed = int(base_run_seed + seed_delta)
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
            metrics = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
            first_exact = safe_float(metrics["first_exact_return_step"])
            start_idx, end_idx = segment_bounds(res["log_rows"], first_exact)
            seg_rows = res["log_rows"][start_idx : end_idx + 1]
            seg_sets = res["damaged_sets"][start_idx : end_idx + 1]
            prev_set = None
            for local_idx, (row, damaged) in enumerate(zip(seg_rows, seg_sets)):
                adj = v15.jaccard(prev_set, damaged) if prev_set is not None else float("nan")
                prev_set = damaged
                segment_rows_out.append(
                    {
                        "seed_delta": int(seed_delta),
                        "placement": int(placement),
                        "run_seed": int(run_seed),
                        "segment_local_index": int(local_idx),
                        "step": int(row["step"]),
                        "damage_component_count": int(row["damage_component_count"]),
                        "largest_component_fraction": safe_float(row["largest_component_fraction"]),
                        "boundary_to_volume": safe_float(row["boundary_to_volume"]),
                        "radius_control": safe_float(row["radius_control"]),
                        "damaged_nodes_count": int(row["damaged_nodes_count"]),
                        "adjacent_jaccard": adj,
                    }
                )
            info = dict(res["perturbation_info"])
            run_rows_out.append(
                {
                    "seed_delta": int(seed_delta),
                    "placement": int(placement),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
                    "support_signature": ",".join(str(x) for x in info.get("support", [])),
                    "full_label": v15q.classify_recurrence_label(int(res["log_rows"][-1]["alive"]), metrics),
                    "full_exact_return_rate": safe_float(metrics["exact_return_rate"]),
                    "first_exact_return_step": first_exact,
                    "segment_snapshot_count": len(seg_rows),
                    "mean_prelock_component_count": mean_defined(safe_float(r["damage_component_count"]) for r in seg_rows),
                    "mean_prelock_largest_fraction": mean_defined(safe_float(r["largest_component_fraction"]) for r in seg_rows),
                    "mean_prelock_boundary_to_volume": mean_defined(safe_float(r["boundary_to_volume"]) for r in seg_rows),
                    "mean_prelock_radius": mean_defined(safe_float(r["radius_control"]) for r in seg_rows if safe_float(r["radius_control"]) >= 0),
                    "mean_prelock_damage_nodes": mean_defined(safe_float(r["damaged_nodes_count"]) for r in seg_rows),
                    "mean_prelock_adjacent_jaccard": mean_defined(
                        safe_float(r["adjacent_jaccard"]) for r in segment_rows_out
                        if int(r["seed_delta"]) == int(seed_delta) and int(r["placement"]) == int(placement) and math.isfinite(safe_float(r["adjacent_jaccard"]))
                    ),
                    "post_exact_hit_rate": safe_float(metrics["exact_return_rate"]),
                }
            )
    return run_rows_out, segment_rows_out


def case_label(
    *,
    exact_gap: float,
    first_gap: float,
    component_gap: float,
    largest_gap: float,
    switch_proxy_gap: float,
) -> str:
    if exact_gap >= 0.08 and first_gap <= -24 and largest_gap >= 0.0 and switch_proxy_gap >= 0.02:
        return "p1_clean_case"
    if exact_gap <= -0.12 and first_gap >= 16 and component_gap >= 0.20:
        return "p0_clean_case"
    if exact_gap <= -0.08 and first_gap <= -8:
        return "tradeoff_case"
    return "mixed_case"


def duel_rows(run_rows_out: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    by_delta: Dict[int, Dict[int, Dict[str, Any]]] = {}
    for row in run_rows_out:
        by_delta.setdefault(int(row["seed_delta"]), {})[int(row["placement"])] = row
    for seed_delta in sorted(by_delta):
        pair = by_delta[seed_delta]
        if set(pair) != {0, 1}:
            continue
        p0 = pair[0]
        p1 = pair[1]
        exact_gap = safe_float(p1["full_exact_return_rate"]) - safe_float(p0["full_exact_return_rate"])
        first_gap = safe_float(p1["first_exact_return_step"]) - safe_float(p0["first_exact_return_step"])
        component_gap = safe_float(p1["mean_prelock_component_count"]) - safe_float(p0["mean_prelock_component_count"])
        largest_gap = safe_float(p1["mean_prelock_largest_fraction"]) - safe_float(p0["mean_prelock_largest_fraction"])
        switch_proxy_gap = safe_float(p1["mean_prelock_adjacent_jaccard"]) - safe_float(p0["mean_prelock_adjacent_jaccard"])
        out.append(
            {
                "seed_delta": int(seed_delta),
                "p0_full_exact_return_rate": safe_float(p0["full_exact_return_rate"]),
                "p1_full_exact_return_rate": safe_float(p1["full_exact_return_rate"]),
                "p1_minus_p0_exact_gap": exact_gap,
                "p0_first_exact_return_step": safe_float(p0["first_exact_return_step"]),
                "p1_first_exact_return_step": safe_float(p1["first_exact_return_step"]),
                "p1_minus_p0_first_gap": first_gap,
                "p1_minus_p0_component_gap": component_gap,
                "p1_minus_p0_largest_gap": largest_gap,
                "p1_minus_p0_adjacent_jaccard_gap": switch_proxy_gap,
                "case_label": case_label(
                    exact_gap=exact_gap,
                    first_gap=first_gap,
                    component_gap=component_gap,
                    largest_gap=largest_gap,
                    switch_proxy_gap=switch_proxy_gap,
                ),
            }
        )
    return out


def aggregate_rows(duels: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    labels = sorted({str(row["case_label"]) for row in duels})
    total = max(1, len(duels))
    out: List[Dict[str, Any]] = []
    for label in labels:
        grp = [row for row in duels if str(row["case_label"]) == label]
        out.append(
            {
                "case_label": label,
                "n_cases": len(grp),
                "rate": len(grp) / total,
                "mean_p1_minus_p0_exact_gap": mean_defined(safe_float(row["p1_minus_p0_exact_gap"]) for row in grp),
                "mean_p1_minus_p0_first_gap": mean_defined(safe_float(row["p1_minus_p0_first_gap"]) for row in grp),
                "mean_p1_minus_p0_component_gap": mean_defined(safe_float(row["p1_minus_p0_component_gap"]) for row in grp),
                "mean_p1_minus_p0_largest_gap": mean_defined(safe_float(row["p1_minus_p0_largest_gap"]) for row in grp),
                "mean_p1_minus_p0_adjacent_jaccard_gap": mean_defined(safe_float(row["p1_minus_p0_adjacent_jaccard_gap"]) for row in grp),
            }
        )
    return out


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], duels: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    counts = {str(row["case_label"]): 0 for row in duels}
    for row in duels:
        counts[str(row["case_label"])] = counts.get(str(row["case_label"]), 0) + 1
    p1_clean = counts.get("p1_clean_case", 0)
    p0_clean = counts.get("p0_clean_case", 0)
    tradeoff = counts.get("tradeoff_case", 0)
    mixed = counts.get("mixed_case", 0)
    if p1_clean >= 1 and p0_clean >= 1 and tradeoff >= 1:
        status = "three_case_family_supported"
        note = "De tre valgte seed-casene holder faktisk som tre ulike lokale case-typer: p1-clean, tradeoff og p0-clean."
        next_step = "explain_case_triggers"
        next_note = "Neste steg bør forklare hva som utløser hvert case, ikke samle flere aggregate-runder."
    elif p1_clean + p0_clean + tradeoff >= 2 and mixed == 0:
        status = "case_family_partly_supported"
        note = "Case-runden skiller minst to lokale case-typer, men ikke alle tre helt rent."
        next_step = "focus_on_missing_case"
        next_note = "Neste steg bør forklare hva som skiller det manglende caset fra de to som holder."
    else:
        status = "case_family_not_yet"
        note = "Selv de mest informative seed-casene kollapser ikke rent til et lite sett lokale case-typer."
        next_step = "stop_splitting_cases"
        next_note = "Neste steg bør være et nytt defect-spørsmål eller en annen observabel, ikke flere case-splitt."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": "Startstørrelsene er rent separert i denne case-runden." if size_clean else "Størrelsesseparasjonen er uklar i denne runden.",
        },
        {
            "diagnostic_family": "case_snapshot",
            "status": f"p1_clean={p1_clean};tradeoff={tradeoff};p0_clean={p0_clean};mixed={mixed}",
            "note": "Dette oppsummerer de tre utvalgte seed-casene etter onset-metrikkene.",
        },
        {
            "diagnostic_family": "case_family_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, target_summary: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15y: p0-vs-p1 case duel lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester om de tre mest informative p0/p1-seedene faktisk holder som tre ulike lokale case-typer."
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
    lines.append("## Case aggregate")
    lines.append("")
    lines.append("| case | n | rate | exact gap | first gap | component gap | largest gap | adjacent-jaccard gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['case_label']} | {int(row['n_cases'])} | {fmt(row['rate'])} | {fmt(row['mean_p1_minus_p0_exact_gap'])} | {fmt(row['mean_p1_minus_p0_first_gap'],1)} | {fmt(row['mean_p1_minus_p0_component_gap'])} | {fmt(row['mean_p1_minus_p0_largest_gap'])} | {fmt(row['mean_p1_minus_p0_adjacent_jaccard_gap'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren case-duel-runde på tre utvalgte seeds, ikke en ny sweep.")
    lines.append("- Les dette som lokal case-typologi, ikke som generell defect-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15y p0-vs-p1 case duel lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15y_p0_p1_case_duel_runs.csv")
    p.add_argument("--out-segment-csv", type=str, default="Documentation/v15y_p0_p1_case_duel_segments.csv")
    p.add_argument("--out-duel-csv", type=str, default="Documentation/v15y_p0_p1_case_duel_duels.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15y_p0_p1_case_duel_aggregate.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15y_p0_p1_case_duel_target_summary.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15y_p0_p1_case_duel_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15y_p0_p1_case_duel_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15y_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15y.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    run_rows_out, segment_rows_out = run_rows(base_state=base_state)
    duel_rows_out = duel_rows(run_rows_out)
    aggregate = aggregate_rows(duel_rows_out)
    diagnosis = diagnosis_rows(target_summary, duel_rows_out)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15y operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in diagnosis
            ],
            "",
            "- Les denne runden som en case-duel-runde på tre seed-caser, ikke som bredere lokal scanning.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15y",
            "",
            "Denne runden sjekker om de tre mest informative små p0/p1-tilfellene faktisk er tre ulike lokale mønstre, eller bare tilfeldige variasjoner.",
            "",
            "Vi ser derfor bare på akkurat disse tre seedene og måler hvordan de skiller lag i den første delen av senfasen.",
        ]
    ) + "\n"
    write_csv(args.out_runs_csv, run_rows_out)
    write_csv(args.out_segment_csv, segment_rows_out)
    write_csv(args.out_duel_csv, duel_rows_out)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
