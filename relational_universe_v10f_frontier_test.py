#!/usr/bin/env python3
"""v0.10f frontier test around band_zero_del and band_small_triad."""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, List, Sequence

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10c_growth_regime_search as v10c
import relational_universe_v10e_focused_band_validation as v10e


def safe_float(x: Any, default: float = float("nan")) -> float:
    try:
        y = float(x)
    except Exception:
        return default
    if math.isnan(y) or math.isinf(y):
        return default
    return y


def mean_defined(values):
    vals = [float(v) for v in values if math.isfinite(float(v))]
    return sum(vals) / len(vals) if vals else float("nan")


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys: List[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def frontier_candidates(mode: str = "full") -> List[v09.ScaleCandidate]:
    full = [
        v09.ScaleCandidate("band_zero_del", 0.02, 0.00, 0.02, 0.00, 0.00),
        v09.ScaleCandidate("band_small_triad", 0.02, 0.00, 0.02, 0.01, 0.01),
        v09.ScaleCandidate("band_triad_zero_del", 0.02, 0.00, 0.02, 0.01, 0.00),
        v09.ScaleCandidate("band_tiny_triad_zero_del", 0.02, 0.00, 0.02, 0.005, 0.00),
        v09.ScaleCandidate("band_tiny_triad_tiny_del", 0.02, 0.00, 0.02, 0.005, 0.005),
        v09.ScaleCandidate("band_mid_triad_tiny_del", 0.02, 0.00, 0.02, 0.015, 0.005),
        v09.ScaleCandidate("band_best", 0.02, 0.00, 0.02, 0.00, 0.01),
        v09.ScaleCandidate("band_small_death", 0.02, 0.01, 0.02, 0.00, 0.01),
    ]
    if mode == "full":
        return full
    if mode == "compact":
        keep = {
            "band_zero_del",
            "band_small_triad",
            "band_triad_zero_del",
            "band_mid_triad_tiny_del",
            "band_best",
            "band_small_death",
        }
        return [cand for cand in full if cand.name in keep]
    if mode == "minimal":
        keep = {
            "band_zero_del",
            "band_small_triad",
            "band_best",
            "band_small_death",
        }
        return [cand for cand in full if cand.name in keep]
    raise ValueError(f"Unknown candidate grid mode: {mode}")


def add_frontier_score(rows: List[Dict[str, Any]]) -> None:
    metrics = {
        "ci_low_mean_composite": True,
        "top_prob_mean_composite": True,
        "abs_alpha_jump": False,
        "linear_margin": True,
        "quasi_large": True,
    }
    for row in rows:
        row["abs_alpha_jump"] = abs(safe_float(row.get("alpha_jump"), float("nan")))
    for key, higher in metrics.items():
        vals = [safe_float(r.get(key), float("nan")) for r in rows]
        vals = [v for v in vals if math.isfinite(v)]
        if not vals:
            continue
        lo, hi = min(vals), max(vals)
        for row in rows:
            row[f"score_{key}"] = v09.objective_score(safe_float(row.get(key), float("nan")), lo, hi, higher_better=higher)
    score_keys = [f"score_{key}" for key in metrics]
    for row in rows:
        row["frontier_score"] = mean_defined(safe_float(row.get(key), float("nan")) for key in score_keys)


def frontier_interpretation(candidate_rows: Sequence[Dict[str, Any]], pair_rows: Sequence[Dict[str, Any]]) -> Dict[str, str]:
    ordered = sorted(candidate_rows, key=lambda r: safe_float(r["frontier_score"]), reverse=True)
    top_names = [str(r["candidate_name"]) for r in ordered[:2]]
    lookup = {(str(r["candidate_a"]), str(r["candidate_b"])): safe_float(r["prob_a_gt_b_mean_composite"]) for r in pair_rows}
    pair = float("nan")
    if len(top_names) == 2:
        pair = lookup.get((top_names[0], top_names[1]), float("nan"))
    if len(top_names) < 2:
        frontier = "For få kandidater til å si noe om en frontier."
    elif 0.40 <= pair <= 0.60:
        frontier = "Fronten holder seg todelt; toppkandidatene ligger fortsatt tett mot hverandre."
    else:
        frontier = f"Fronten smalner inn; `{top_names[0]}` ser ut til å ha et tydeligere overtak over `{top_names[1]}`."
    if len(top_names) < 2:
        recommendation = "Hold flere kandidater åpne til neste runde."
    elif 0.35 <= pair <= 0.65:
        recommendation = f"Hold både `{top_names[0]}` og `{top_names[1]}` åpne videre."
    else:
        recommendation = f"Bruk `{top_names[0]}` som operativ standardkandidat og `{top_names[1]}` som nær kontroll."
    return {
        "frontier_statement": frontier,
        "recommendation": recommendation,
    }


def technical_markdown(candidate_rows: Sequence[Dict[str, Any]], pair_rows: Sequence[Dict[str, Any]], profile_rows: Sequence[Dict[str, Any]], interpretation: Dict[str, str]) -> str:
    lines = [
        "# v0.10f frontier-test",
        "",
        "Denne runden holder `fast_balanced / deep` fast og tester et lite lokalt grid rundt `band_zero_del` og `band_small_triad` med høyere replikasjon enn v0.10e.",
        "",
        "## Kandidatsammendrag",
        "",
        "| candidate | frontier_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in sorted(candidate_rows, key=lambda r: safe_float(r["frontier_score"]), reverse=True):
        lines.append(
            f"| {row['candidate_name']} | {safe_float(row['frontier_score']):.3f} | {safe_float(row['mean_composite']):.3f} | "
            f"{safe_float(row['ci_low_mean_composite']):.3f} | {safe_float(row['top_prob_mean_composite']):.3f} | "
            f"{safe_float(row['alpha_large']):.3f} | {safe_float(row['alpha_jump']):.3f} | {safe_float(row['linear_margin']):.3f} |"
        )
    lines.extend([
        "",
        "## Pairwise-sannsynligheter",
        "",
        "| a | b | P(a > b) |",
        "| --- | --- | --- |",
    ])
    for row in sorted(pair_rows, key=lambda r: (str(r["candidate_a"]), str(r["candidate_b"]))):
        lines.append(f"| {row['candidate_a']} | {row['candidate_b']} | {safe_float(row['prob_a_gt_b_mean_composite']):.3f} |")
    lines.extend([
        "",
        "## Størrelsesprofiler",
        "",
        "| candidate | target | realized_initial | radius | overlap | quasi | composite |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for row in sorted(profile_rows, key=lambda r: (str(r["candidate_name"]), int(r["target_nodes"]))):
        lines.append(
            f"| {row['candidate_name']} | {int(row['target_nodes'])} | {safe_float(row['mean_initial_nodes']):.1f} | "
            f"{safe_float(row['mean_radius']):.2f} | {safe_float(row['mean_overlap']):.3f} | {safe_float(row['mean_quasi']):.3f} | "
            f"{safe_float(row['mean_composite']):.3f} |"
        )
    lines.extend([
        "",
        "## Operativ lesning",
        "",
        f"- {interpretation['frontier_statement']}",
        f"- {interpretation['recommendation']}",
        "",
    ])
    return "\n".join(lines)


def lay_markdown(interpretation: Dict[str, str]) -> str:
    return "\n".join([
        "# v0.10f frontier-test for ikke-spesialister",
        "",
        "I denne runden sjekker vi om prosjektet egentlig har én ny favorittkandidat, eller om to nesten-like kandidater fortsatt bør holdes åpne.",
        "",
        interpretation["frontier_statement"],
        "",
        interpretation["recommendation"],
        "",
    ])


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Run a focused frontier test around band_zero_del and band_small_triad")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=4)
    ap.add_argument("--run-seeds", type=int, default=4)
    ap.add_argument("--bootstrap-reps", type=int, default=300)
    ap.add_argument("--grid-mode", default="full", choices=["full", "compact", "minimal"])
    ap.add_argument("--output-prefix", default="Documentation/v10f")
    ap.add_argument("--report-md", default="Documentation/v10f_frontier_test.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_10f.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_10f_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [e for e in v10b.build_ensembles(targets) if e.burnin_label == "deep"]
    candidates = frontier_candidates(args.grid_mode)
    growth_seeds = [9001 + 18 * i for i in range(args.growth_seeds)]
    run_offsets = [1501 + 26 * i for i in range(args.run_seeds)]

    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    group_rows = v10e.summarize_groups(candidates, ensembles, run_rows)
    ci_rows, pair_rows, top_rows = v10e.bootstrap_joint(candidates, ensembles, run_rows, reps=int(args.bootstrap_reps), rng_seed=25017)
    top_lookup = {str(r["candidate_name"]): r for r in top_rows}

    candidate_rows: List[Dict[str, Any]] = []
    for cand in candidates:
        row = v10e.point_candidate_summary(cand.name, group_rows)
        row.update(ci_rows[cand.name])
        row["top_prob_mean_composite"] = top_lookup[cand.name]["top_prob_mean_composite"]
        candidate_rows.append(row)
    add_frontier_score(candidate_rows)
    candidate_rows.sort(key=lambda r: safe_float(r["frontier_score"]), reverse=True)

    profile_rows = v10e.size_profiles([c.name for c in candidates], group_rows)
    interpretation = frontier_interpretation(candidate_rows, pair_rows)

    prefix = args.output_prefix
    write_csv(f"{prefix}_frontier_base_rows.csv", base_rows)
    write_csv(f"{prefix}_frontier_run_rows.csv", run_rows)
    write_csv(f"{prefix}_frontier_group_rows.csv", group_rows)
    write_csv(f"{prefix}_frontier_candidate_summary.csv", candidate_rows)
    write_csv(f"{prefix}_frontier_pairwise.csv", pair_rows)
    write_csv(f"{prefix}_frontier_top_probs.csv", top_rows)
    write_csv(f"{prefix}_frontier_size_profiles.csv", profile_rows)

    for path, content in [
        (args.report_md, technical_markdown(candidate_rows, pair_rows, profile_rows, interpretation)),
        (args.lay_md, lay_markdown(interpretation)),
        (args.recommendation_md, "\n".join(["# v0.10f operativ anbefaling", "", interpretation["recommendation"], ""])),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
