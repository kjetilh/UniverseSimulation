#!/usr/bin/env python3
"""v0.15au post-peak fade explainer for the late high boundary.

This round follows v15at. v15at sharpened the delayed high boundary into a
useful burst reading:

- a real sustained hold burst,
- a no-high burst family,
- and one small fading-late-burst remainder.

The next narrow question is:

can that fading remainder be explained by what happens *after* the peak burst,
rather than by launch failure alone?
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15ai_early_lock_band_lab as v15ai
import relational_universe_v15ar_high_retention_horizon_lab as v15ar
import relational_universe_v15at_high_burst_window_lab as v15at


TARGET = 48
GROWTH_SEED = 202
FULL_STEPS = 2560
LOG_EVERY = 8
WINDOW = v15ar.WINDOW
BURST_WINDOW = v15at.BURST_WINDOW

CASE_SPECS = (
    {
        "case_label": "anchor_hold",
        "placement": 2,
        "seed_delta": 239,
        "expected_burst_label": "sustained_hold_burst",
    },
    {
        "case_label": "fading_holdout",
        "placement": 2,
        "seed_delta": 231,
        "expected_burst_label": "fading_late_burst",
    },
    {
        "case_label": "no_high_holdout",
        "placement": 2,
        "seed_delta": 247,
        "expected_burst_label": "no_high_burst",
    },
)


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


def base_run_seed_for(placement: int) -> int:
    return TARGET * 100000 + GROWTH_SEED * 1000 + int(placement)


def first_value(values: Sequence[str], target: str) -> int:
    for idx, value in enumerate(values):
        if value == target:
            return idx
    return -1


def classify_post_peak(
    *,
    first_high_index: int,
    peak_high_window_rate: float,
    post_peak_high_rate: float,
    post_peak_mid_rate: float,
    last12_high_rate: float,
    first_low_after_peak: int,
) -> str:
    if first_high_index >= WINDOW:
        return "no_launch_tail"
    if peak_high_window_rate >= 0.75 and post_peak_high_rate >= 0.60 and last12_high_rate >= 0.50:
        return "post_peak_hold"
    if peak_high_window_rate >= 0.75 and post_peak_high_rate <= 0.25 and post_peak_mid_rate >= 0.50 and 0 <= first_low_after_peak <= 12:
        return "post_peak_fade"
    return "mixed_post_peak"


def mechanism_note(label: str) -> str:
    if label == "post_peak_hold":
        return "Etter peak holder high-segmentet seg stabilt helt inn i tail-slutten."
    if label == "post_peak_fade":
        return "Runet far en ekte peak, men taper high raskt etterpa og glir tilbake i mid/lav tail."
    if label == "no_launch_tail":
        return "Runet far aldri noe reelt high-lop a forklare etter peak."
    return "Post-peak-vinduet leser fortsatt ikke dette caset helt rent."


def analyze_case(*, base_state: Any, case_label: str, placement: int, seed_delta: int, expected_burst_label: str) -> Dict[str, Any]:
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    run_seed = int(base_run_seed_for(placement) + seed_delta)
    res = v15ae.run_defect_with_control_graphs(
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
    support_signature = ",".join(str(x) for x in info.get("support", []))
    recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
    full_label = v15q.classify_recurrence_label(int(res["log_rows"][-1]["alive"]), recurrence)
    partition = v15ae.occupancy_partition(res["damaged_sets"])
    snap_rows = v15ae.shell_snapshot_rows(
        placement=placement,
        seed_delta=seed_delta,
        run_seed=run_seed,
        support_signature=support_signature,
        core_nodes=set(partition["core_nodes"]),
        shell_nodes=set(partition["shell_nodes"]),
        log_rows=res["log_rows"],
        damaged_sets=res["damaged_sets"],
        control_graphs=res["control_graphs"],
    )
    normalized = [
        v15ai.normalize_snapshot_row(
            row,
            source_group="post_peak_case",
            anchor_seed_delta=seed_delta,
            holdout_seed_delta=-1,
            family_tag="post_peak_boundary",
        )
        for row in snap_rows
        if int(row["shell_active_nodes"]) > 0
    ]
    bands = [str(row["shell_count_band"]) for row in normalized[:WINDOW]]
    first_high_raw = v15ar.first_run_ge(bands, "high", 3)
    first_high_index = WINDOW if first_high_raw is None else int(first_high_raw)
    peak_start, peak_rate = v15at.rolling_high_peak(bands, BURST_WINDOW)
    peak_end = min(len(bands), peak_start + BURST_WINDOW)
    post_peak = bands[peak_end:]
    post_peak_high_rate = sum(1 for band in post_peak if band == "high") / max(1, len(post_peak)) if post_peak else 0.0
    post_peak_mid_rate = sum(1 for band in post_peak if band == "mid") / max(1, len(post_peak)) if post_peak else 0.0
    post_peak_low_rate = sum(1 for band in post_peak if band == "low") / max(1, len(post_peak)) if post_peak else 0.0
    last12 = bands[-12:]
    last12_high_rate = sum(1 for band in last12 if band == "high") / max(1, len(last12)) if last12 else 0.0
    first_low_after_peak = first_value(post_peak, "low")
    mechanism_label = classify_post_peak(
        first_high_index=first_high_index,
        peak_high_window_rate=peak_rate,
        post_peak_high_rate=post_peak_high_rate,
        post_peak_mid_rate=post_peak_mid_rate,
        last12_high_rate=last12_high_rate,
        first_low_after_peak=first_low_after_peak,
    )
    return {
        "case_label": case_label,
        "placement": int(placement),
        "seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "expected_burst_label": expected_burst_label,
        "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
        "support_signature": support_signature,
        "full_label": full_label,
        "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
        "first_high_index": int(first_high_index),
        "peak_high_window_start": int(peak_start),
        "peak_high_window_rate": float(peak_rate),
        "post_peak_high_rate": float(post_peak_high_rate),
        "post_peak_mid_rate": float(post_peak_mid_rate),
        "post_peak_low_rate": float(post_peak_low_rate),
        "first_low_after_peak": int(first_low_after_peak),
        "last12_high_rate": float(last12_high_rate),
        "post_peak_label": mechanism_label,
        "post_peak_note": mechanism_note(mechanism_label),
    }


def run_rows(*, base_state: Any) -> List[Dict[str, Any]]:
    return [
        analyze_case(
            base_state=base_state,
            case_label=str(spec["case_label"]),
            placement=int(spec["placement"]),
            seed_delta=int(spec["seed_delta"]),
            expected_burst_label=str(spec["expected_burst_label"]),
        )
        for spec in CASE_SPECS
    ]


def diagnosis_rows(*, target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary if int(row["target_nodes"]) == TARGET)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    labels = {str(row["post_peak_label"]) for row in rows}
    if labels >= {"post_peak_hold", "post_peak_fade", "no_launch_tail"}:
        status = "post_peak_map_supported"
        note = "Det lille triplet-caset deler seg rent i post-peak hold, post-peak fade og ingen launch-tail."
        next_step = "holdout_post_peak_fade"
        next_note = "Neste steg bor teste om `post_peak_fade` holder pa noen fa naerliggende seeds rundt fading-caset."
    else:
        status = "post_peak_map_still_mixed"
        note = "Post-peak-vinduet gir noe struktur, men triplet-en kollapser ikke rent nok ennå."
        next_step = "change_fade_observable"
        next_note = "Neste steg bor bytte observabel igjen rundt fading-caset."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsene er rent separert og alle run i denne runden matcher onsket add_chord-perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "post_peak_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15au: post-peak fade explainer")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden forklarer bare den lille `anchor_hold` / `fading_holdout` / `no_high_holdout`-triplet-en etter at burst-peaken faktisk er etablert.")
    lines.append("")
    lines.append("## Startstorrelser")
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
    lines.append("## Cases")
    lines.append("")
    lines.append("| case | run seed | expected burst | peak start | peak rate | post high | post mid | first low after peak | post-peak label |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {row['case_label']} | {int(row['run_seed'])} | {row['expected_burst_label']} | {int(row['peak_high_window_start'])} | {fmt(row['peak_high_window_rate'])} | {fmt(row['post_peak_high_rate'])} | {fmt(row['post_peak_mid_rate'])} | {int(row['first_low_after_peak'])} | {row['post_peak_label']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren forklaringsrunde for fading-sporet, ikke en ny bred seed-scan.")
    lines.append("- Les dette som lokal mekanikk etter peak, ikke som nye defect-arter.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15au post-peak fade explainer.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15au_post_peak_fade_runs.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15au_post_peak_fade_target_summary.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15au_post_peak_fade_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15au_post_peak_fade_explainer.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15au_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15au.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    rows = run_rows(base_state=base_state)
    diagnosis = diagnosis_rows(target_summary=target_summary, rows=rows)
    report_md = build_report(target_summary=target_summary, rows=rows, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15au operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en liten post-peak-forklaring, ikke som en ny bred defect-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15au",
            "",
            "Etter at vi fant ett lite fading-spor, ser denne runden bare pa hva som skjer etter at high-peaken allerede er etablert.",
            "",
            "Målet er a skille et ekte hold fra et lop som fader ut igjen, og fra et lop som aldri virkelig starter.",
        ]
    ) + "\n"
    write_csv(args.out_runs_csv, rows)
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
