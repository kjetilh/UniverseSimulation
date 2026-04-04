#!/usr/bin/env python3
"""v0.15u add_chord p1 microcenter validation.

This round is intentionally narrower than v15t. It stays on the same base and
tests whether p1 is a real local maximum against both immediate flanks p0 and
p2 under a fresh set of holdout seeds.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 48
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2)
SEED_DELTAS = (151, 179, 211, 239, 271, 307)
FULL_STEPS = 2560
LOG_EVERY = 8


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def quantile(values: Sequence[float], q: float) -> float:
    return v15.quantile(values, q)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def run_rows(*, base_state: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
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
            full_label = v15q.classify_recurrence_label(int(res["log_rows"][-1]["alive"]), metrics)
            info = dict(res["perturbation_info"])
            rows.append(
                {
                    "target_nodes": TARGET,
                    "growth_seed": GROWTH_SEED,
                    "placement": int(placement),
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
                    "support_signature": ",".join(str(x) for x in info.get("support", [])),
                    "full_label": full_label,
                    "full_exact_return_rate": safe_float(metrics["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(metrics["coarse_return_rate"]),
                    "full_max_exact_return_jaccard": safe_float(metrics["max_exact_return_jaccard"]),
                }
            )
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        group = [row for row in rows if int(row["placement"]) == int(placement)]
        exacts = [safe_float(row["full_exact_return_rate"]) for row in group]
        coarses = [safe_float(row["full_coarse_return_rate"]) for row in group]
        out.append(
            {
                "placement": int(placement),
                "n_runs": len(group),
                "cyclic_rate": mean_defined(1.0 if str(row["full_label"]) == "cyclic_return" else 0.0 for row in group),
                "mean_full_exact_return_rate": mean_defined(exacts),
                "q10_full_exact_return_rate": quantile(exacts, 0.10),
                "mean_full_coarse_return_rate": mean_defined(coarses),
                "q10_full_coarse_return_rate": quantile(coarses, 0.10),
                "mean_full_max_exact_return_jaccard": mean_defined(
                    safe_float(row["full_max_exact_return_jaccard"]) for row in group
                ),
            }
        )
    return out


def pair_duel_counts(rows: Sequence[Dict[str, Any]], left: int, right: int) -> str:
    left_wins = 0
    right_wins = 0
    ties = 0
    for seed_delta in SEED_DELTAS:
        pair = [row for row in rows if int(row["seed_delta"]) == int(seed_delta) and int(row["placement"]) in {left, right}]
        pair_by_place = {int(row["placement"]): row for row in pair}
        if len(pair_by_place) != 2:
            continue
        delta = safe_float(pair_by_place[left]["full_exact_return_rate"]) - safe_float(pair_by_place[right]["full_exact_return_rate"])
        if delta > 0.01:
            left_wins += 1
        elif delta < -0.01:
            right_wins += 1
        else:
            ties += 1
    return f"p{left}_wins={left_wins};p{right}_wins={right_wins};ties={ties}"


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    by_place = {int(row["placement"]): row for row in aggregate}
    p0 = by_place[0]
    p1 = by_place[1]
    p2 = by_place[2]
    p0_exact = safe_float(p0["mean_full_exact_return_rate"])
    p1_exact = safe_float(p1["mean_full_exact_return_rate"])
    p2_exact = safe_float(p2["mean_full_exact_return_rate"])
    p0_cyclic = safe_float(p0["cyclic_rate"])
    p1_cyclic = safe_float(p1["cyclic_rate"])
    p2_cyclic = safe_float(p2["cyclic_rate"])
    duel_10 = pair_duel_counts(rows, 1, 0)
    duel_12 = pair_duel_counts(rows, 1, 2)

    def wins_from(text: str, tag: str) -> int:
        for chunk in text.split(";"):
            if chunk.startswith(tag + "="):
                return int(chunk.split("=", 1)[1])
        return 0

    p1_vs_p0 = wins_from(duel_10, "p1_wins")
    p1_vs_p2 = wins_from(duel_12, "p1_wins")
    p0_vs_p1 = wins_from(duel_10, "p0_wins")
    p2_vs_p1 = wins_from(duel_12, "p2_wins")

    if p1_cyclic >= 0.80 and p1_exact - p0_exact >= 0.05 and p1_exact - p2_exact >= 0.05 and p1_vs_p0 >= 4 and p1_vs_p2 >= 4:
        status = "confirmed_p1_microcenter"
        note = "Plassering 1 holder høyere cycle-rate og exact-return enn begge umiddelbare flanker under nye holdout-seeds."
        next_step = "explain_p1_support"
        next_note = "Neste steg bør forklare hva i p1-støtten som gjør den mer stabil enn p0 og p2."
    elif p0_cyclic >= p1_cyclic and p0_exact > p1_exact and p0_vs_p1 >= 4:
        status = "left_flank_competes"
        note = "Venstre flanke holder minst like godt som p1 under de nye holdout-seedene, så mikrocenteret er ikke rent løst."
        next_step = "compare_p0_p1_mechanism"
        next_note = "Neste steg bør sammenligne p0 og p1 mekanistisk, ikke anta at sentrum er avklart."
    elif p1_cyclic >= 0.80 and p0_cyclic >= 0.80 and p2_cyclic >= 0.80 and max(abs(p1_exact - p0_exact), abs(p1_exact - p2_exact)) < 0.05:
        status = "flat_microband"
        note = "Alle tre plasseringene holder cycle-signalet omtrent like godt, så det ser mer ut som et lite flatt mikroband enn et sentrum."
        next_step = "treat_as_microband"
        next_note = "Neste steg bør forklare hvorfor hele mikrobandet holder, ikke presse fram ett enkelt sentrum."
    elif p2_cyclic > p1_cyclic and p2_vs_p1 >= 4:
        status = "right_flank_recovers"
        note = "Høyre flanke henter inn eller passerer p1 under friske holdout-seeds."
        next_step = "compare_p1_p2_mechanism"
        next_note = "Neste steg bør forklare hvorfor p2 noen ganger kollapser og andre ganger nesten matcher p1."
    else:
        status = "microcenter_still_mixed"
        note = "P1 ser fortsatt lovende ut, men mikrocenteret er ikke rent nok skilt fra flankene til å kalles fullt avklart."
        next_step = "stay_micro"
        next_note = "Neste steg bør være en liten mekanistisk forklaringsrunde inne i p0-p1-p2-triplet."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er rent separert og alle smale microcenter-profiler matcher ønsket add_chord-perturbasjon."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "microcenter_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "p1_vs_p0_seed_duels",
            "status": duel_10,
            "note": "Smale head-to-head-dueller pa samme seed_delta mellom p1 og p0.",
        },
        {
            "diagnostic_family": "p1_vs_p2_seed_duels",
            "status": duel_12,
            "note": "Smale head-to-head-dueller pa samme seed_delta mellom p1 og p2.",
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, target_summary: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15u: add_chord p1 microcenter")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester bare om `p1` faktisk er et lokalt maksimum mot begge nærmeste flanker `p0` og `p2` under friske holdout-seeds."
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
    lines.append("## Microcenter summary")
    lines.append("")
    lines.append("| placement | n | cyclic rate | mean full exact | q10 full exact | mean full coarse |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['placement'])} | {int(row['n_runs'])} | {fmt(row['cyclic_rate'])} | {fmt(row['mean_full_exact_return_rate'])} | {fmt(row['q10_full_exact_return_rate'])} | {fmt(row['mean_full_coarse_return_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en mikrotest inne i samme lokale add_chord-band, ikke en ny family-scan.")
    lines.append("- Les resultatet som lokal robusthet eller flathet i et lite band, ikke som generell defect-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15u add_chord p1 microcenter validation.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15u_add_chord_p1_microcenter_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15u_add_chord_p1_microcenter_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15u_add_chord_p1_microcenter_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15u_add_chord_p1_microcenter_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15u_add_chord_p1_microcenter.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15u_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15u.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    rows = run_rows(base_state=base_state)
    aggregate = aggregate_rows(rows)
    diagnosis = diagnosis_rows(target_summary, rows, aggregate)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15u operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in diagnosis
            ],
            "",
            "- Les denne runden som en mikrotest inne i det lokale add_chord-bandet, ikke som bred syklusbekreftelse.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15u",
            "",
            "Denne runden sjekker om plassering 1 virkelig er sentrum i det lille lokale cycle-bandet, eller om nabopunktene holder nesten like godt.",
            "",
            "Vi gjør det med noen få helt nye seed-varianter, men fortsatt på samme base og samme smale område.",
        ]
    ) + "\n"
    write_csv(args.out_runs_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
