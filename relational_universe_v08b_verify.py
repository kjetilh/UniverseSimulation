#!/usr/bin/env python3
"""Verification and regression helpers for the v0.8b natural-ensemble scan."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import relational_universe_v08b_natural_ensemble_robustness as v08b


RUN_REQUIRED_COLUMNS = {
    "ensemble",
    "seed",
    "r_birth",
    "r_death",
    "p_swap",
    "p_triad",
    "p_del",
    "final_radius_control",
    "avg_local_overlap",
    "final_edge_diff_count",
    "abs_delta_beta1",
    "abs_delta_spectral_radius",
    "initial_nodes",
}

ENSEMBLE_REQUIRED_COLUMNS = {
    "ensemble",
    "r_birth",
    "r_death",
    "p_swap",
    "p_triad",
    "p_del",
    "mean_initial_nodes",
    "mean_initial_tokens",
    "composite_score",
    "ci_low_composite",
    "ci_high_composite",
    "ci_low_mean_radius",
    "ci_high_mean_radius",
    "ci_low_mean_overlap",
    "ci_high_mean_overlap",
}

OVERALL_REQUIRED_COLUMNS = {
    "r_birth",
    "r_death",
    "p_swap",
    "p_triad",
    "p_del",
    "mean_composite_natural",
    "ci_low_mean_composite_natural",
    "ci_high_mean_composite_natural",
    "mean_radius_natural",
    "mean_overlap_natural",
}


def safe_float(value: Any, default: float = float("nan")) -> float:
    try:
        out = float(value)
    except Exception:
        return default
    if math.isnan(out) or math.isinf(out):
        return default
    return out


def load_rows(path: str | Path) -> List[Dict[str, Any]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def candidate_key(row: Dict[str, Any]) -> Tuple[float, float, float, float, float]:
    return (
        round(safe_float(row.get("r_birth"), 0.0), 6),
        round(safe_float(row.get("r_death"), 0.0), 6),
        round(safe_float(row.get("p_swap"), 0.0), 6),
        round(safe_float(row.get("p_triad"), 0.0), 6),
        round(safe_float(row.get("p_del"), 0.0), 6),
    )


def column_check(rows: Sequence[Dict[str, Any]], required: Sequence[str]) -> Dict[str, Any]:
    if not rows:
        return {"ok": False, "missing": list(required), "present": []}
    present = set(rows[0].keys())
    missing = sorted(set(required) - present)
    return {"ok": not missing, "missing": missing, "present": sorted(present)}


def mean_initial_nodes_by_ensemble(run_rows: Sequence[Dict[str, Any]]) -> Dict[str, float]:
    values: Dict[str, List[float]] = {}
    for row in run_rows:
        values.setdefault(str(row["ensemble"]), []).append(safe_float(row.get("initial_nodes"), float("nan")))
    return {name: sum(vals) / len(vals) for name, vals in values.items() if vals}


def verify_ensemble_growth(run_rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    means = mean_initial_nodes_by_ensemble(run_rows)
    toy = means.get("toy_cycle8", float("nan"))
    natural = {k: v for k, v in means.items() if k != "toy_cycle8"}
    ok = math.isfinite(toy) and all(v > toy for v in natural.values())
    return {"ok": ok, "toy_cycle8_mean_nodes": toy, "natural_mean_nodes": natural}


def verify_bootstrap_intervals(
    ensemble_rows: Sequence[Dict[str, Any]],
    overall_rows: Sequence[Dict[str, Any]],
) -> Dict[str, Any]:
    ensemble_failures: List[str] = []
    overall_failures: List[str] = []
    for row in ensemble_rows:
        comp = safe_float(row.get("composite_score"))
        lo = safe_float(row.get("ci_low_composite"))
        hi = safe_float(row.get("ci_high_composite"))
        radius = safe_float(row.get("mean_final_radius_control"))
        radius_lo = safe_float(row.get("ci_low_mean_radius"))
        radius_hi = safe_float(row.get("ci_high_mean_radius"))
        overlap = safe_float(row.get("mean_avg_local_overlap"))
        overlap_lo = safe_float(row.get("ci_low_mean_overlap"))
        overlap_hi = safe_float(row.get("ci_high_mean_overlap"))
        if not (lo <= comp <= hi):
            ensemble_failures.append(f"{row['ensemble']}:{candidate_key(row)} composite")
        if not (radius_lo <= radius <= radius_hi):
            ensemble_failures.append(f"{row['ensemble']}:{candidate_key(row)} radius")
        if not (overlap_lo <= overlap <= overlap_hi):
            ensemble_failures.append(f"{row['ensemble']}:{candidate_key(row)} overlap")
    for row in overall_rows:
        comp = safe_float(row.get("mean_composite_natural"))
        lo = safe_float(row.get("ci_low_mean_composite_natural"))
        hi = safe_float(row.get("ci_high_mean_composite_natural"))
        if not (lo <= comp <= hi):
            overall_failures.append(str(candidate_key(row)))
    return {
        "ok": not ensemble_failures and not overall_failures,
        "ensemble_failures": ensemble_failures,
        "overall_failures": overall_failures,
    }


def ranking_stability(
    ensemble_rows: Sequence[Dict[str, Any]],
    *,
    bootstrap_seeds: Sequence[int],
    bootstrap_reps: int,
) -> Dict[str, Any]:
    ensembles = v08b.default_ensembles()
    rankings: List[List[Tuple[float, float, float, float, float]]] = []
    for seed in bootstrap_seeds:
        ranked = v08b.aggregate_overall(list(ensemble_rows), ensembles, bootstrap_reps=bootstrap_reps, rng_seed=seed)
        rankings.append([candidate_key(row) for row in ranked])

    baseline = rankings[0]
    baseline_top = baseline[0]
    positions: List[int] = []
    top3_sets: List[set[Tuple[float, float, float, float, float]]] = []
    for ranking in rankings:
        positions.append(ranking.index(baseline_top) + 1)
        top3_sets.append(set(ranking[:3]))
    stable_band = max(positions) <= 2
    common_top3 = set.intersection(*top3_sets) if top3_sets else set()
    return {
        "ok": stable_band and len(common_top3) >= 2,
        "baseline_top_candidate": baseline_top,
        "top_candidate_positions": positions,
        "common_top3_count": len(common_top3),
        "bootstrap_seeds": list(bootstrap_seeds),
    }


def build_summary(
    run_rows: Sequence[Dict[str, Any]],
    ensemble_rows: Sequence[Dict[str, Any]],
    overall_rows: Sequence[Dict[str, Any]],
    *,
    bootstrap_seeds: Sequence[int],
    bootstrap_reps: int,
) -> Dict[str, Any]:
    return {
        "run_columns": column_check(run_rows, RUN_REQUIRED_COLUMNS),
        "ensemble_columns": column_check(ensemble_rows, ENSEMBLE_REQUIRED_COLUMNS),
        "overall_columns": column_check(overall_rows, OVERALL_REQUIRED_COLUMNS),
        "ensemble_growth": verify_ensemble_growth(run_rows),
        "bootstrap_intervals": verify_bootstrap_intervals(ensemble_rows, overall_rows),
        "ranking_stability": ranking_stability(ensemble_rows, bootstrap_seeds=bootstrap_seeds, bootstrap_reps=bootstrap_reps),
    }


def make_report(summary: Dict[str, Any]) -> str:
    lines = [
        "# v0.8b verifikasjon og regresjon",
        "",
        "## Hva som ble sjekket",
        "",
        "- at de naturlige ensemblefamiliene faktisk ble større enn `toy_cycle8`,",
        "- at bootstrap-intervallene omslutter de tilhørende punktestimatene,",
        "- at rangeringen etter `ci_low_mean_composite_natural` ikke hopper rundt når bootstrap-seed endres litt,",
        "- og at CSV-strukturen fortsatt inneholder de viktigste bakoverkompatible kolonnene.",
        "",
        "## Resultat",
        "",
        f"- Kolonnesjekk run CSV: {'pass' if summary['run_columns']['ok'] else 'FAIL'}",
        f"- Kolonnesjekk ensemble CSV: {'pass' if summary['ensemble_columns']['ok'] else 'FAIL'}",
        f"- Kolonnesjekk overall CSV: {'pass' if summary['overall_columns']['ok'] else 'FAIL'}",
        f"- Naturlige ensembler større enn `toy_cycle8`: {'pass' if summary['ensemble_growth']['ok'] else 'FAIL'}",
        f"- Bootstrap-konsistens: {'pass' if summary['bootstrap_intervals']['ok'] else 'FAIL'}",
        f"- Ranking-stabilitet: {'pass' if summary['ranking_stability']['ok'] else 'FAIL'}",
        "",
        "## Detaljer",
        "",
        f"- `toy_cycle8` mean initial nodes: {summary['ensemble_growth']['toy_cycle8_mean_nodes']:.3f}",
    ]
    for name, value in sorted(summary["ensemble_growth"]["natural_mean_nodes"].items()):
        lines.append(f"- `{name}` mean initial nodes: {value:.3f}")
    lines.extend(
        [
            "- Ranking-kriteriet her er pragmatisk: baseline-topkandidaten skal holde seg innen topp-2 over små bootstrap-seed-endringer.",
            f"- Topkandidaten fra baseline-bootstrap holdt posisjonene {summary['ranking_stability']['top_candidate_positions']} over seed-varianten.",
            f"- Felles kandidater i top-3 over alle bootstrap-seeds: {summary['ranking_stability']['common_top3_count']}",
            "",
        ]
    )
    if summary["bootstrap_intervals"]["ensemble_failures"] or summary["bootstrap_intervals"]["overall_failures"]:
        lines.append("## Feil")
        lines.append("")
        for failure in summary["bootstrap_intervals"]["ensemble_failures"]:
            lines.append(f"- Ensemble-intervalfeil: `{failure}`")
        for failure in summary["bootstrap_intervals"]["overall_failures"]:
            lines.append(f"- Overall-intervalfeil: `{failure}`")
        lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify v0.8b outputs and summarize regression health.")
    parser.add_argument("--run-csv", type=str, default="Documentation/v08b_natural_ensemble_runs.csv")
    parser.add_argument("--ensemble-csv", type=str, default="Documentation/v08b_natural_ensemble_aggregate.csv")
    parser.add_argument("--overall-csv", type=str, default="Documentation/v08b_candidate_robustness.csv")
    parser.add_argument("--bootstrap-seeds", type=str, default="314159,314160,314170,314180,314190")
    parser.add_argument("--bootstrap-reps", type=int, default=200)
    parser.add_argument("--report-md", type=str, default="Documentation/v08b_verification_report.md")
    parser.add_argument("--json-out", type=str, default="Documentation/v08b_verification_report.json")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_rows = load_rows(args.run_csv)
    ensemble_rows = load_rows(args.ensemble_csv)
    overall_rows = load_rows(args.overall_csv)
    bootstrap_seeds = [int(piece.strip()) for piece in args.bootstrap_seeds.split(",") if piece.strip()]
    summary = build_summary(
        run_rows,
        ensemble_rows,
        overall_rows,
        bootstrap_seeds=bootstrap_seeds,
        bootstrap_reps=args.bootstrap_reps,
    )
    Path(args.report_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_md).write_text(make_report(summary), encoding="utf-8")
    Path(args.json_out).write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    main()
