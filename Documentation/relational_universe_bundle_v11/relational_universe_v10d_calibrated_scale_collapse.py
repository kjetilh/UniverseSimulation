#!/usr/bin/env python3
"""v0.10d calibrated scale rerun on improved growth ensembles."""
from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v09b_asymptotic_refinement as v09b
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10c_growth_regime_search as v10c


def safe_float(x: Any, default: float = float("nan")) -> float:
    try:
        y = float(x)
    except Exception:
        return default
    if math.isnan(y) or math.isinf(y):
        return default
    return y


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    path = Path(path)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys: List[str] = []
    seen = set()
    for row in rows:
        for k in row:
            if k not in seen:
                seen.add(k)
                keys.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def recommended_regime(name: str) -> v10c.FastRegime:
    for reg in v10c.default_regimes():
        if reg.name == name:
            return reg
    raise ValueError(f"Unknown growth regime {name!r}")


def build_fast_bases(
    ensembles: Sequence[v10b.CalibrationEnsemble],
    regime: v10c.FastRegime,
    growth_seeds: Sequence[int],
) -> Dict[Tuple[str, int], Any]:
    out = {}
    for ens in ensembles:
        for seed in growth_seeds:
            out[(ens.name, int(seed))] = v10c.grow_fast(ens, int(seed), regime)[0]
    return out


def default_candidates() -> List[v09.ScaleCandidate]:
    wanted = {"band_best", "macro_stable", "balanced_pdel"}
    return [c for c in v09.default_candidates() if c.name in wanted]


def steps_for_state(nodes: int) -> int:
    return max(220, min(800, int(round(5.0 * nodes))))


def summarize_candidate(point: v09.ScaleCandidate, group_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    sub = [r for r in group_rows if r["candidate_name"] == point.name]
    metrics = v09b.asymptotic_metrics_from_group_rows(sub)
    return {
        "candidate_name": point.name,
        "mean_composite": statistics.mean(float(r["composite_score"]) for r in sub),
        "mean_repair": statistics.mean(float(r["repair_score"]) for r in sub),
        "mean_causal": statistics.mean(float(r["causal_score"]) for r in sub),
        "mean_quasi": statistics.mean(float(r["quasi_score"]) for r in sub),
        "mean_geom": statistics.mean(float(r["geom_score"]) for r in sub),
        **metrics,
    }


def build_markdown(regime_name: str, candidate_rows: List[Dict[str, Any]], profile_rows: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# v0.10d calibrated scale rerun")
    lines.append("")
    lines.append(f"Denne rerunden bruker growth-regimet `{regime_name}` og bare ensembles som faktisk realiserer reelt separerte startstørrelser.")
    lines.append("")
    lines.append("## Kandidatsammendrag")
    lines.append("")
    lines.append("| candidate | mean_composite | mean_repair | mean_causal | mean_quasi | mean_geom | alpha_all | alpha_large | alpha_jump | linear_margin |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(candidate_rows, key=lambda r: safe_float(r["mean_composite"]), reverse=True):
        lines.append(
            f"| {row['candidate_name']} | {safe_float(row['mean_composite']):.3f} | {safe_float(row['mean_repair']):.3f} | "
            f"{safe_float(row['mean_causal']):.3f} | {safe_float(row['mean_quasi']):.3f} | {safe_float(row['mean_geom']):.3f} | "
            f"{safe_float(row['alpha_all']):.3f} | {safe_float(row['alpha_large']):.3f} | {safe_float(row['alpha_jump']):.3f} | {safe_float(row['linear_margin']):.3f} |"
        )
    lines.append("")
    lines.append("## Størrelsesprofiler")
    lines.append("")
    lines.append("| candidate | target | realized_initial | radius | overlap | quasi | composite | beta1_drift |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(profile_rows, key=lambda r: (str(r["candidate_name"]), int(r["target_nodes"]))):
        lines.append(
            f"| {row['candidate_name']} | {int(row['target_nodes'])} | {safe_float(row['mean_initial_nodes']):.1f} | "
            f"{safe_float(row['mean_radius']):.2f} | {safe_float(row['mean_overlap']):.3f} | {safe_float(row['mean_quasi']):.3f} | "
            f"{safe_float(row['mean_composite']):.3f} | {safe_float(row['mean_beta1_drift']):.2f} |"
        )
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("Hvis ekstreme eller negative eksponenter forsvinner når startstørrelsene faktisk separerer, er det et tegn på at tidligere funn var generatorartefakter.")
    lines.append("Hvis en kandidat fortsatt ser dårlig ut etter kalibrering, er det mer rimelig å tolke det som en dynamisk svakhet ved selve kandidaten.")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.10d calibrated scale rerun")
    ap.add_argument("--growth-regime", type=str, default="fast_balanced")
    ap.add_argument("--targets", type=str, default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=2)
    ap.add_argument("--run-seeds", type=int, default=2)
    ap.add_argument("--output-prefix", type=str, default="/mnt/data/v10d")
    return ap


def main() -> None:
    ap = build_argparser()
    args = ap.parse_args()

    regime = recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [e for e in v10b.build_ensembles(targets) if e.burnin_label == "deep"]
    growth_seeds = [3000 + 17 * i for i in range(args.growth_seeds)]
    run_seed_offsets = [1101 + 18 * i for i in range(args.run_seeds)]
    candidates = default_candidates()

    base_states = build_fast_bases(ensembles, regime, growth_seeds)

    run_rows: List[Dict[str, Any]] = []
    for point in candidates:
        for ens in ensembles:
            for gseed in growth_seeds:
                base = base_states[(ens.name, int(gseed))]
                steps = steps_for_state(base.g.num_nodes())
                for off in run_seed_offsets:
                    row = v09.run_single_candidate_from_base(point, ens, base, seed=int(gseed + off), steps=steps)
                    row["growth_regime"] = regime.name
                    row["growth_seed"] = gseed
                    row["run_seed"] = int(gseed + off)
                    row["steps"] = steps
                    run_rows.append(row)

    group_rows: List[Dict[str, Any]] = []
    for point in candidates:
        for ens in ensembles:
            sub = [r for r in run_rows if r["candidate_name"] == point.name and r["ensemble"] == ens.name]
            agg = v09.summarize_group(point, ens, sub)
            group_rows.append(agg)
    v09.add_scores_to_group_rows(group_rows)

    candidate_rows = [summarize_candidate(point, group_rows) for point in candidates]
    candidate_rows.sort(key=lambda r: safe_float(r["mean_composite"]), reverse=True)

    profile_rows: List[Dict[str, Any]] = []
    for point in candidates:
        sub = [r for r in group_rows if r["candidate_name"] == point.name]
        profile_rows.extend([{**row, "candidate_name": point.name} for row in v09b.size_profile(sub)])

    prefix = args.output_prefix
    write_csv(f"{prefix}_calibrated_scale_run_rows.csv", run_rows)
    write_csv(f"{prefix}_calibrated_scale_group_rows.csv", group_rows)
    write_csv(f"{prefix}_calibrated_scale_candidate_summary.csv", candidate_rows)
    write_csv(f"{prefix}_calibrated_scale_size_profiles.csv", profile_rows)
    Path(f"{prefix}_calibrated_scale.md").write_text(build_markdown(regime.name, candidate_rows, profile_rows), encoding="utf-8")


if __name__ == "__main__":
    main()
