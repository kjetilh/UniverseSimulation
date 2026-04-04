#!/usr/bin/env python3
"""v0.15t add_chord cycle-center holdout validation.

This round stays inside the local v15s cycle band and asks a narrower question:
is placement 1 really a stronger local cycle center than placement 2, or did
v15s mostly reveal a flat little band on one reference seed family?
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
PLACEMENTS = (1, 2)
SEED_DELTAS = (0, 17, 43, 71, 101, 137)
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
            actual = str(info.get("type", "unknown"))
            rows.append(
                {
                    "target_nodes": TARGET,
                    "growth_seed": GROWTH_SEED,
                    "placement": int(placement),
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match("add_chord", actual)),
                    "support_signature": ",".join(str(x) for x in info.get("support", [])),
                    "full_label": full_label,
                    "full_exact_return_rate": safe_float(metrics["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(metrics["coarse_return_rate"]),
                    "full_max_exact_return_jaccard": safe_float(metrics["max_exact_return_jaccard"]),
                    "full_first_exact_return_step": safe_float(metrics["first_exact_return_step"]),
                    "full_first_coarse_return_step": safe_float(metrics["first_coarse_return_step"]),
                }
            )
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        group = [row for row in rows if int(row["placement"]) == int(placement)]
        exacts = [safe_float(row["full_exact_return_rate"]) for row in group]
        coarses = [safe_float(row["full_coarse_return_rate"]) for row in group]
        cyclic_rate = mean_defined(1.0 if str(row["full_label"]) == "cyclic_return" else 0.0 for row in group)
        out.append(
            {
                "placement": int(placement),
                "n_runs": len(group),
                "cyclic_rate": cyclic_rate,
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


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    by_place = {int(row["placement"]): row for row in aggregate}
    p1 = by_place[1]
    p2 = by_place[2]
    p1_exact = safe_float(p1["mean_full_exact_return_rate"])
    p2_exact = safe_float(p2["mean_full_exact_return_rate"])
    p1_cyclic = safe_float(p1["cyclic_rate"])
    p2_cyclic = safe_float(p2["cyclic_rate"])
    p1_pair_wins = 0
    p2_pair_wins = 0
    ties = 0
    for seed_delta in SEED_DELTAS:
        pair = [row for row in rows if int(row["seed_delta"]) == int(seed_delta)]
        if len(pair) != 2:
            continue
        pair_by_place = {int(row["placement"]): row for row in pair}
        delta = safe_float(pair_by_place[1]["full_exact_return_rate"]) - safe_float(pair_by_place[2]["full_exact_return_rate"])
        if delta > 0.01:
            p1_pair_wins += 1
        elif delta < -0.01:
            p2_pair_wins += 1
        else:
            ties += 1
    if p1_cyclic >= 0.80 and p1_exact - p2_exact >= 0.05 and p1_pair_wins >= 4:
        status = "shifted_center_p1"
        note = "Plassering 1 holder høyere cycle-rate og høyere exact-return over de smale holdout-seedene enn plassering 2."
        next_step = "probe_p1_microcenter"
        next_note = "Neste steg bør være en enda smalere mikrotest rundt p1 som lokalt cycle-sentrum."
    elif p1_cyclic >= 0.60 and p2_cyclic >= 0.60 and abs(p1_exact - p2_exact) < 0.05:
        status = "flat_local_band"
        note = "Plassering 1 og 2 holder begge cycle-signalet godt nok til at båndet ser flatt ut under denne smale holdout-testen."
        next_step = "treat_as_flat_band"
        next_note = "Neste steg bør forklare hvorfor flere nærliggende profiler faller inn i samme cycle-regime, ikke presse frem ett sentrum."
    elif p2_cyclic > p1_cyclic and p2_pair_wins >= 4:
        status = "center_returns_to_p2"
        note = "Den opprinnelige p2-profilen holder seg best når vi går bort fra referanseseedene."
        next_step = "probe_p2_microcenter"
        next_note = "Neste steg bør kartlegge p2 som mulig lokalt cycle-sentrum med enda smalere seed-kontroll."
    else:
        status = "band_remains_ambiguous"
        note = "Holdout-seedene holder cycle-signalet levende, men skiller ikke rent nok mellom p1 og p2 til å gi et sikkert sentrum."
        next_step = "stay_narrow"
        next_note = "Neste steg bør være en liten mekanistisk forklaringsrunde inne i båndet, ikke bredere scanning."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er rent separert og alle smale holdout-profiler matcher ønsket add_chord-perturbasjon."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "cycle_center_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "pairwise_seed_duels",
            "status": f"p1_wins={p1_pair_wins};p2_wins={p2_pair_wins};ties={ties}",
            "note": "Dette teller bare smale head-to-head-dueller på samme seed_delta, med 0.01 som liten likevektsterskel.",
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, target_summary: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15t: add_chord cycle-center holdout")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden holder seg inne i `v15s`-båndet og tester bare om `p1` faktisk er et sterkere lokalt cycle-sentrum enn `p2` under noen få nye dynamikk-seeds."
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
    lines.append("## Holdout summary")
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
    lines.append("- Dette er en smal holdout-test inne i samme lokale cycle-band, ikke en ny placement-scan.")
    lines.append("- Les resultatet som lokal robusthet for cycle-bandet, ikke som bevis for en universell defect-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15t add_chord cycle-center holdout validation.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15t_add_chord_cycle_center_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15t_add_chord_cycle_center_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15t_add_chord_cycle_center_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15t_add_chord_cycle_center_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15t_add_chord_cycle_center_holdout.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15t_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15t.md")
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
            "# v0.15t operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in diagnosis
            ],
            "",
            "- Les denne runden som en smal holdout-test inne i det lokale add_chord-båndet, ikke som en ny bred cycle-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15t",
            "",
            "Denne runden sjekker om plassering 1 faktisk er den sterkeste versjonen av det lokale add_chord-cycle-signalet, eller om plassering 1 og 2 egentlig oppfører seg nesten likt.",
            "",
            "Vi gjør det med noen få nye dynamikk-seeds på samme base, ikke ved å åpne et bredt nytt søk.",
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
