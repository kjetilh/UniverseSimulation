#!/usr/bin/env python3
"""v0.15ab add_chord cycle lag lab.

This round asks a new observability question inside the strongest local
add_chord recurrence band:

when we see strong exact-return rates, do they come from a stable return lag,
or from broad multi-lag recurrence without a sharp local period?
"""
from __future__ import annotations

import argparse
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Set, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 48
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2)
SEED_DELTAS = (151, 179, 211, 239, 271, 307)
FULL_STEPS = 2560
LOG_EVERY = 8
MIN_HIT_SCORE = 0.95


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


def lag_metrics(log_rows: Sequence[Dict[str, Any]], damaged_sets: Sequence[Set[int]]) -> Dict[str, Any]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(log_rows))))
    hit_lags_snapshots: List[int] = []
    hit_lags_steps: List[float] = []
    hit_scores: List[float] = []
    best_lag_steps: List[float] = []

    for idx in range(tail_start, len(log_rows)):
        cur_set = damaged_sets[idx]
        best_score = -1.0
        best_prev = -1
        for prev in range(0, max(0, idx - v15q.MIN_GAP_SNAPSHOTS)):
            score = v15q.exact_jaccard(cur_set, damaged_sets[prev])
            if score > best_score:
                best_score = score
                best_prev = prev
        if best_prev >= 0 and math.isfinite(best_score):
            lag_snap = idx - best_prev
            lag_steps = safe_float(log_rows[idx]["step"]) - safe_float(log_rows[best_prev]["step"])
            best_lag_steps.append(lag_steps)
            if best_score >= MIN_HIT_SCORE:
                hit_lags_snapshots.append(lag_snap)
                hit_lags_steps.append(lag_steps)
                hit_scores.append(best_score)

    if hit_lags_steps:
        counts = Counter(hit_lags_steps)
        dominant_lag_step, dominant_count = counts.most_common(1)[0]
        second_count = counts.most_common(2)[1][1] if len(counts) >= 2 else 0
        dominant_share = dominant_count / max(1, len(hit_lags_steps))
        top2_share = (dominant_count + second_count) / max(1, len(hit_lags_steps))
        unique_lag_count = len(counts)
    else:
        dominant_lag_step = float("nan")
        dominant_share = 0.0
        top2_share = 0.0
        unique_lag_count = 0

    return {
        "hit_count": len(hit_lags_steps),
        "hit_rate": len(hit_lags_steps) / max(1, len(log_rows) - tail_start),
        "dominant_lag_steps": dominant_lag_step,
        "dominant_lag_share": dominant_share,
        "top2_lag_share": top2_share,
        "unique_hit_lag_count": unique_lag_count,
        "mean_hit_lag_steps": mean_defined(hit_lags_steps),
        "q10_hit_lag_steps": quantile(hit_lags_steps, 0.10) if hit_lags_steps else float("nan"),
        "q90_hit_lag_steps": quantile(hit_lags_steps, 0.90) if hit_lags_steps else float("nan"),
        "mean_hit_score": mean_defined(hit_scores),
        "mean_best_lag_steps": mean_defined(best_lag_steps),
    }


def lag_label(*, full_label: str, exact_rate: float, dominant_share: float, top2_share: float, unique_lags: int) -> str:
    if full_label == "cyclic_return" and exact_rate >= 0.50 and dominant_share >= 0.70 and unique_lags <= 2:
        return "stable_single_lag_cycle"
    if full_label == "cyclic_return" and exact_rate >= 0.50 and top2_share >= 0.80 and unique_lags <= 4:
        return "few_lag_cycle_family"
    if full_label == "cyclic_return" and exact_rate >= 0.20:
        return "diffuse_cycle_family"
    if full_label == "morphology_return" and exact_rate >= 0.20:
        return "morphology_with_exact_hits"
    return "weak_or_aperiodic"


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
            recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
            lags = lag_metrics(res["log_rows"], res["damaged_sets"])
            full_label = v15q.classify_recurrence_label(int(res["log_rows"][-1]["alive"]), recurrence)
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
                    "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                    "dominant_lag_steps": safe_float(lags["dominant_lag_steps"]),
                    "dominant_lag_share": safe_float(lags["dominant_lag_share"]),
                    "top2_lag_share": safe_float(lags["top2_lag_share"]),
                    "unique_hit_lag_count": int(lags["unique_hit_lag_count"]),
                    "hit_count": int(lags["hit_count"]),
                    "hit_rate": safe_float(lags["hit_rate"]),
                    "mean_hit_lag_steps": safe_float(lags["mean_hit_lag_steps"]),
                    "q10_hit_lag_steps": safe_float(lags["q10_hit_lag_steps"]),
                    "q90_hit_lag_steps": safe_float(lags["q90_hit_lag_steps"]),
                    "mean_hit_score": safe_float(lags["mean_hit_score"]),
                    "lag_label": lag_label(
                        full_label=full_label,
                        exact_rate=safe_float(recurrence["exact_return_rate"]),
                        dominant_share=safe_float(lags["dominant_lag_share"]),
                        top2_share=safe_float(lags["top2_lag_share"]),
                        unique_lags=int(lags["unique_hit_lag_count"]),
                    ),
                }
            )
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        group = [row for row in rows if int(row["placement"]) == int(placement)]
        exacts = [safe_float(row["full_exact_return_rate"]) for row in group]
        dominant_shares = [safe_float(row["dominant_lag_share"]) for row in group]
        dominant_lags = [safe_float(row["dominant_lag_steps"]) for row in group if math.isfinite(safe_float(row["dominant_lag_steps"]))]
        unique_lags = [safe_float(row["unique_hit_lag_count"]) for row in group]
        stable_rate = mean_defined(1.0 if str(row["lag_label"]) == "stable_single_lag_cycle" else 0.0 for row in group)
        few_rate = mean_defined(1.0 if str(row["lag_label"]) == "few_lag_cycle_family" else 0.0 for row in group)
        diffuse_rate = mean_defined(1.0 if str(row["lag_label"]) == "diffuse_cycle_family" else 0.0 for row in group)
        out.append(
            {
                "placement": int(placement),
                "n_runs": len(group),
                "cyclic_rate": mean_defined(1.0 if str(row["full_label"]) == "cyclic_return" else 0.0 for row in group),
                "stable_single_lag_rate": stable_rate,
                "few_lag_cycle_rate": few_rate,
                "diffuse_cycle_rate": diffuse_rate,
                "mean_full_exact_return_rate": mean_defined(exacts),
                "mean_dominant_lag_share": mean_defined(dominant_shares),
                "q10_dominant_lag_share": quantile(dominant_shares, 0.10),
                "mean_dominant_lag_steps": mean_defined(dominant_lags),
                "q10_dominant_lag_steps": quantile(dominant_lags, 0.10) if dominant_lags else float("nan"),
                "q90_dominant_lag_steps": quantile(dominant_lags, 0.90) if dominant_lags else float("nan"),
                "mean_unique_hit_lag_count": mean_defined(unique_lags),
            }
        )
    return out


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    by_place = {int(row["placement"]): row for row in aggregate}
    p0 = by_place[0]
    p1 = by_place[1]
    p2 = by_place[2]

    if safe_float(p1["stable_single_lag_rate"]) >= 0.50 and safe_float(p1["mean_dominant_lag_share"]) >= 0.70:
        status = "p1_stable_cycle_lag"
        note = "Plassering 1 ser ut til å ha en relativt skarp dominerende return-lag, ikke bare høy exact-return-rate."
        next_step = "probe_p1_period_holdout"
        next_note = "Neste steg bør teste om denne dominerende lagstrukturen holder på noen få nye seeds rundt p1."
    elif max(safe_float(p0["few_lag_cycle_rate"]), safe_float(p1["few_lag_cycle_rate"]), safe_float(p2["few_lag_cycle_rate"])) >= 0.50:
        status = "cycle_band_is_few_lag_family"
        note = "Det lokale add_chord-båndet ser mer ut som en liten few-lag-familie enn som ett rent enkelt periodisk sentrum."
        next_step = "compare_lag_signatures"
        next_note = "Neste steg bør sammenligne lag-signaturene mellom p0, p1 og p2 mer direkte, ikke bare lete etter ett sentrum."
    elif max(safe_float(p0["diffuse_cycle_rate"]), safe_float(p1["diffuse_cycle_rate"]), safe_float(p2["diffuse_cycle_rate"])) >= 0.50:
        status = "cycle_band_is_diffuse"
        note = "Høy return-rate ser hovedsakelig ut til å komme fra bred multi-lag-retur, ikke en skarp lokal periode."
        next_step = "stop_period_story"
        next_note = "Neste steg bør være en annen observabel enn periodisitet."
    else:
        status = "lag_story_mixed"
        note = "Lag-observabelen gjør cycle-båndet mer konkret, men ikke rent nok til en enkel periodestory ennå."
        next_step = "stay_small"
        next_note = "Neste steg bør være en liten mekanistisk eller holdout-basert lag-runde, ikke en bred scan."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er rent separert og alle smale cycle-lag-profiler matcher ønsket add_chord-perturbasjon."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "lag_cycle_status",
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
    lines.append("# Relasjonell universgraf v0.15ab: add_chord cycle lag lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden spør om det lokale add_chord-cycle-båndet ser periodisk ut med en stabil return-lag, eller om høy retur-rate kommer fra bred multi-lag-retur.")
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
    lines.append("## Lag summary")
    lines.append("")
    lines.append("| placement | n | cyclic rate | stable single lag | few lag | diffuse lag | mean exact | mean dominant share | mean dominant lag |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['placement'])} | {int(row['n_runs'])} | {fmt(row['cyclic_rate'])} | {fmt(row['stable_single_lag_rate'])} | {fmt(row['few_lag_cycle_rate'])} | {fmt(row['diffuse_cycle_rate'])} | {fmt(row['mean_full_exact_return_rate'])} | {fmt(row['mean_dominant_lag_share'])} | {fmt(row['mean_dominant_lag_steps'],1)} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ny observabel inne i samme lokale add_chord-band, ikke en ny placement-scan.")
    lines.append("- Les dette som periodisitetsdiagnostikk for local recurrence, ikke som bevis for en generell defect-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ab add_chord cycle lag lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15ab_add_chord_cycle_lag_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ab_add_chord_cycle_lag_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ab_add_chord_cycle_lag_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15ab_add_chord_cycle_lag_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ab_add_chord_cycle_lag_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ab_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ab.md")
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
            "# v0.15ab operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en ny lag-/periodisitetsobservabel inne i det lokale add_chord-båndet, ikke som en ny scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15ab",
            "",
            "Denne runden spør ikke bare om skaden kommer tilbake ofte. Den spør om den kommer tilbake med en noenlunde fast rytme, eller om returen bare er løs og variabel.",
            "",
            "Vi ser derfor på de samme tre lokale add_chord-plasseringene som før, men måler hvilke tidsforskjeller som faktisk dukker opp når skaden ligner seg selv igjen.",
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
