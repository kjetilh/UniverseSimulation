#!/usr/bin/env python3
"""v0.15ad add_chord boundary-shell dynamics lab.

This round follows v15ac. Since the local add_chord recurrence band looks like
a stable core with a variable shell, it asks a tighter question:

is the shell turnover calm and incremental, or bursty and reset-like?
"""
from __future__ import annotations

import argparse
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Set

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 48
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2)
SEED_DELTAS = (151, 179, 211, 239, 271, 307)
FULL_STEPS = 2560
LOG_EVERY = 8
CORE_THRESHOLD = 0.80
SHELL_THRESHOLD = 0.20


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def quantile(values: Sequence[float], q: float) -> float:
    return v15.quantile(values, q)


def sd_or_zero(values: Sequence[float]) -> float:
    vals = [safe_float(v) for v in values if math.isfinite(safe_float(v))]
    if len(vals) <= 1:
        return 0.0
    return float((sum((x - (sum(vals) / len(vals))) ** 2 for x in vals) / (len(vals) - 1)) ** 0.5)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def classify_shell_dynamics(*, refresh_mean: float, burst_rate: float, boundary_sd: float, shell_cover_mean: float) -> str:
    if refresh_mean <= 0.25 and burst_rate <= 0.15 and boundary_sd <= 0.05:
        return "calm_shell_cycle"
    if refresh_mean >= 0.40 or burst_rate >= 0.30:
        return "bursty_shell_cycle"
    if shell_cover_mean < 0.40:
        return "thin_shell_cycle"
    return "mixed_shell_cycle"


def shell_sets(damaged_sets: Sequence[Set[int]]) -> Dict[str, Any]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(damaged_sets))))
    tail_sets = damaged_sets[tail_start:]
    denom = max(1, len(tail_sets))
    occ: Counter[int] = Counter()
    for damaged in tail_sets:
        occ.update(damaged)
    occupancies = {node: count / denom for node, count in occ.items()}
    core_nodes = {node for node, frac in occupancies.items() if frac >= CORE_THRESHOLD}
    shell_nodes = {node for node, frac in occupancies.items() if SHELL_THRESHOLD <= frac < CORE_THRESHOLD}
    return {
        "tail_start": tail_start,
        "tail_sets": tail_sets,
        "core_nodes": core_nodes,
        "shell_nodes": shell_nodes,
    }


def shell_metrics(log_rows: Sequence[Dict[str, Any]], damaged_sets: Sequence[Set[int]]) -> Dict[str, Any]:
    data = shell_sets(damaged_sets)
    tail_start = int(data["tail_start"])
    tail_sets = list(data["tail_sets"])
    shell_nodes = set(data["shell_nodes"])
    shell_active_sets = [damaged.intersection(shell_nodes) for damaged in tail_sets]
    adj = [v15.jaccard(shell_active_sets[i], shell_active_sets[i + 1]) for i in range(len(shell_active_sets) - 1)]
    refresh = [1.0 - x for x in adj]
    burst_rate = mean_defined(1.0 if x >= 0.50 else 0.0 for x in refresh)
    shell_sizes = [len(s) for s in shell_active_sets]
    shell_cover = [(len(s) / max(1, len(shell_nodes))) if shell_nodes else float("nan") for s in shell_active_sets]
    tail_rows = log_rows[tail_start:]
    boundary_vals = [safe_float(row["boundary_to_volume"]) for row in tail_rows]

    return {
        "tail_snapshot_count": len(tail_sets),
        "shell_nodes": len(shell_nodes),
        "mean_shell_active_nodes": mean_defined(shell_sizes),
        "q10_shell_active_nodes": quantile(shell_sizes, 0.10) if shell_sizes else float("nan"),
        "q90_shell_active_nodes": quantile(shell_sizes, 0.90) if shell_sizes else float("nan"),
        "mean_shell_cover": mean_defined(x for x in shell_cover if math.isfinite(x)),
        "q10_shell_cover": quantile([x for x in shell_cover if math.isfinite(x)], 0.10) if any(math.isfinite(x) for x in shell_cover) else float("nan"),
        "mean_shell_adjacent_jaccard": mean_defined(adj),
        "q10_shell_adjacent_jaccard": quantile(adj, 0.10) if adj else float("nan"),
        "mean_shell_refresh": mean_defined(refresh),
        "burst_rate": burst_rate,
        "mean_boundary_to_volume": mean_defined(boundary_vals),
        "sd_boundary_to_volume": sd_or_zero(boundary_vals),
    }


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
            metrics = shell_metrics(res["log_rows"], res["damaged_sets"])
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
                    "full_label": v15q.classify_recurrence_label(int(res["log_rows"][-1]["alive"]), recurrence),
                    "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                    "shell_nodes": int(metrics["shell_nodes"]),
                    "mean_shell_active_nodes": safe_float(metrics["mean_shell_active_nodes"]),
                    "q10_shell_active_nodes": safe_float(metrics["q10_shell_active_nodes"]),
                    "q90_shell_active_nodes": safe_float(metrics["q90_shell_active_nodes"]),
                    "mean_shell_cover": safe_float(metrics["mean_shell_cover"]),
                    "q10_shell_cover": safe_float(metrics["q10_shell_cover"]),
                    "mean_shell_adjacent_jaccard": safe_float(metrics["mean_shell_adjacent_jaccard"]),
                    "q10_shell_adjacent_jaccard": safe_float(metrics["q10_shell_adjacent_jaccard"]),
                    "mean_shell_refresh": safe_float(metrics["mean_shell_refresh"]),
                    "burst_rate": safe_float(metrics["burst_rate"]),
                    "mean_boundary_to_volume": safe_float(metrics["mean_boundary_to_volume"]),
                    "sd_boundary_to_volume": safe_float(metrics["sd_boundary_to_volume"]),
                    "shell_label": classify_shell_dynamics(
                        refresh_mean=safe_float(metrics["mean_shell_refresh"]),
                        burst_rate=safe_float(metrics["burst_rate"]),
                        boundary_sd=safe_float(metrics["sd_boundary_to_volume"]),
                        shell_cover_mean=safe_float(metrics["mean_shell_cover"]),
                    ),
                }
            )
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        group = [row for row in rows if int(row["placement"]) == int(placement)]
        out.append(
            {
                "placement": int(placement),
                "n_runs": len(group),
                "cyclic_rate": mean_defined(1.0 if str(row["full_label"]) == "cyclic_return" else 0.0 for row in group),
                "calm_shell_rate": mean_defined(1.0 if str(row["shell_label"]) == "calm_shell_cycle" else 0.0 for row in group),
                "bursty_shell_rate": mean_defined(1.0 if str(row["shell_label"]) == "bursty_shell_cycle" else 0.0 for row in group),
                "mixed_shell_rate": mean_defined(1.0 if str(row["shell_label"]) == "mixed_shell_cycle" else 0.0 for row in group),
                "thin_shell_rate": mean_defined(1.0 if str(row["shell_label"]) == "thin_shell_cycle" else 0.0 for row in group),
                "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in group),
                "mean_shell_refresh": mean_defined(safe_float(row["mean_shell_refresh"]) for row in group),
                "q10_shell_refresh": quantile([safe_float(row["mean_shell_refresh"]) for row in group], 0.10),
                "mean_burst_rate": mean_defined(safe_float(row["burst_rate"]) for row in group),
                "mean_shell_cover": mean_defined(safe_float(row["mean_shell_cover"]) for row in group),
                "mean_boundary_sd": mean_defined(safe_float(row["sd_boundary_to_volume"]) for row in group),
            }
        )
    return out


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    p0 = next(row for row in aggregate if int(row["placement"]) == 0)
    p1 = next(row for row in aggregate if int(row["placement"]) == 1)
    p2 = next(row for row in aggregate if int(row["placement"]) == 2)

    if max(safe_float(p0["calm_shell_rate"]), safe_float(p1["calm_shell_rate"]), safe_float(p2["calm_shell_rate"])) >= 0.50:
        status = "core_shell_variation_is_calm"
        note = "Randen ser ut til å flimre ganske rolig og inkrementelt, ikke i store resets eller bursts."
        next_step = "probe_shell_topology"
        next_note = "Neste steg bør måle randtopologien mer direkte, siden variasjonen ser reell men rolig ut."
    elif max(safe_float(p0["bursty_shell_rate"]), safe_float(p1["bursty_shell_rate"]), safe_float(p2["bursty_shell_rate"])) >= 0.50:
        status = "core_shell_variation_is_bursty"
        note = "Randen ser ut til å skifte i bursts, ikke bare som rolig lokal churn."
        next_step = "probe_burst_events"
        next_note = "Neste steg bør se direkte på burst-overganger i randen."
    else:
        status = "boundary_shell_still_mixed"
        note = "Randdynamikken er tydelig nok til å måles, men ikke ren nok til én enkel calm/bursty-lesning ennå."
        next_step = "stay_boundary_local"
        next_note = "Neste steg bør være en enda mindre rand-observabel i samme band."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er rent separert og alle smale boundary-shell-profiler matcher ønsket add_chord-perturbasjon."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "boundary_shell_status",
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
    lines.append("# Relasjonell universgraf v0.15ad: add_chord boundary-shell dynamics lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden spør om den variable randen i det lokale add_chord-båndet skifter rolig og inkrementelt, eller i mer bursty hopp.")
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
    lines.append("## Boundary-shell summary")
    lines.append("")
    lines.append("| placement | n | cyclic | calm shell | bursty shell | mixed shell | mean refresh | mean burst | mean shell cover |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['placement'])} | {int(row['n_runs'])} | {fmt(row['cyclic_rate'])} | {fmt(row['calm_shell_rate'])} | {fmt(row['bursty_shell_rate'])} | {fmt(row['mixed_shell_rate'])} | {fmt(row['mean_shell_refresh'])} | {fmt(row['mean_burst_rate'])} | {fmt(row['mean_shell_cover'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en rand-observabel inne i det samme lokale add_chord-båndet, ikke en ny placement-scan.")
    lines.append("- Les dette som dynamikk i den variable randen, ikke som bevis for en generell defect-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ad add_chord boundary-shell dynamics lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15ad_add_chord_boundary_shell_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ad_add_chord_boundary_shell_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ad_add_chord_boundary_shell_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15ad_add_chord_boundary_shell_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ad_add_chord_boundary_shell_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ad_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ad.md")
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
            "# v0.15ad operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en rand-dynamikk-observabel inne i det lokale add_chord-båndet, ikke som en ny scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15ad",
            "",
            "Etter at vi fant en stabil kjerne med en mer variabel rand, spør denne runden om randen endrer seg rolig litt etter litt, eller om den hopper i mer dramatiske burst-lignende skift.",
            "",
            "Vi måler derfor hvor mye randnodene overlapper fra ett sent steg til det neste.",
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
