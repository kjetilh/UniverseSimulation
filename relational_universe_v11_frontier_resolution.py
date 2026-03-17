#!/usr/bin/env python3
"""v0.11 frontier resolution around band_zero_del and diagonal bridge points."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, List, Sequence

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e


def named_candidate(name: str, p_swap: float, p_triad: float, p_del: float) -> v09.ScaleCandidate:
    return v09.ScaleCandidate(name, 0.02, 0.00, p_swap, p_triad, p_del)


def resolution_candidates() -> List[v09.ScaleCandidate]:
    return [
        named_candidate("band_zero_del", 0.020, 0.0000, 0.0000),
        named_candidate("band_zero_del_swap025", 0.025, 0.0000, 0.0000),
        named_candidate("bridge_0025_0000", 0.020, 0.0025, 0.0000),
        named_candidate("bridge_0025_0025", 0.020, 0.0025, 0.0025),
        named_candidate("bridge_0050_0025", 0.020, 0.0050, 0.0025),
        named_candidate("frontier_diag_mid", 0.020, 0.0050, 0.0050),
        named_candidate("bridge_0025_0000_swap025", 0.025, 0.0025, 0.0000),
        named_candidate("frontier_triad_only", 0.020, 0.0100, 0.0000),
    ]


def candidate_rows_from_group_rows(
    candidates: Sequence[v09.ScaleCandidate],
    group_rows: Sequence[Dict[str, Any]],
    ci_rows: Dict[str, Dict[str, float]],
    top_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    top_lookup = {str(r["candidate_name"]): r for r in top_rows}
    rows: List[Dict[str, Any]] = []
    for cand in candidates:
        row = v10e.point_candidate_summary(cand.name, group_rows)
        row.update(ci_rows[cand.name])
        row["top_prob_mean_composite"] = top_lookup[cand.name]["top_prob_mean_composite"]
        rows.append(row)
    v10e.add_focused_score(rows)
    rows.sort(key=lambda r: v10e.safe_float(r["focused_score"], -1.0), reverse=True)
    return rows


def interpret(candidate_rows: Sequence[Dict[str, Any]], pair_rows: Sequence[Dict[str, Any]]) -> Dict[str, str]:
    raw = max(candidate_rows, key=lambda r: v10e.safe_float(r["mean_composite"], -1.0))
    focused = max(candidate_rows, key=lambda r: v10e.safe_float(r["focused_score"], -1.0))
    same = str(raw["candidate_name"]) == str(focused["candidate_name"])
    lookup = {(str(r["candidate_a"]), str(r["candidate_b"])): v10e.safe_float(r["prob_a_gt_b_mean_composite"]) for r in pair_rows}
    pair = lookup.get((str(raw["candidate_name"]), str(focused["candidate_name"])), float("nan"))
    if same:
        convergence = f"Råvinner og focused-vinner har konvergert til `{raw['candidate_name']}`."
    else:
        convergence = f"Råvinneren er `{raw['candidate_name']}`, mens focused-vinneren er `{focused['candidate_name']}`."
    if same or (pair >= 0.65):
        recommendation = f"Bruk `{raw['candidate_name']}` som operativ standardkandidat i neste runde."
    else:
        recommendation = f"Hold både `{raw['candidate_name']}` og `{focused['candidate_name']}` åpne videre; spenningen er ikke helt oppløst."
    return {"convergence": convergence, "recommendation": recommendation}


def build_markdown(candidate_rows: Sequence[Dict[str, Any]], pair_rows: Sequence[Dict[str, Any]], interpretation: Dict[str, str]) -> str:
    lines = [
        "# v0.11 frontier resolution",
        "",
        "Denne runden tester et finere lokalt grid rundt `band_zero_del` og diagonalbroen, med en liten `p_swap`-akse og `frontier_triad_only` som kontroll.",
        "",
        "## Kandidatsammendrag",
        "",
        "| candidate | focused_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in sorted(candidate_rows, key=lambda r: v10e.safe_float(r["focused_score"], -1.0), reverse=True):
        lines.append(
            f"| {row['candidate_name']} | {v10e.safe_float(row['focused_score']):.3f} | {v10e.safe_float(row['mean_composite']):.3f} | "
            f"{v10e.safe_float(row['ci_low_mean_composite']):.3f} | {v10e.safe_float(row['top_prob_mean_composite']):.3f} | "
            f"{v10e.safe_float(row['alpha_large']):.3f} | {v10e.safe_float(row['alpha_jump']):.3f} | {v10e.safe_float(row['linear_margin']):.3f} |"
        )
    lines.extend([
        "",
        "## Pairwise-sannsynligheter",
        "",
        "| a | b | P(a > b) |",
        "| --- | --- | --- |",
    ])
    for row in sorted(pair_rows, key=lambda r: (str(r["candidate_a"]), str(r["candidate_b"]))):
        lines.append(f"| {row['candidate_a']} | {row['candidate_b']} | {v10e.safe_float(row['prob_a_gt_b_mean_composite']):.3f} |")
    lines.extend([
        "",
        "## Tolkning",
        "",
        f"- {interpretation['convergence']}",
        f"- {interpretation['recommendation']}",
        "",
    ])
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.11 frontier resolution")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=5)
    ap.add_argument("--run-seeds-broad", type=int, default=3)
    ap.add_argument("--run-seeds-final", type=int, default=4)
    ap.add_argument("--bootstrap-reps", type=int, default=220)
    ap.add_argument("--output-prefix", default="Documentation/v11")
    ap.add_argument("--report-md", default="Documentation/v11_frontier_resolution.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_11.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_11_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [e for e in v10b.build_ensembles(targets) if e.burnin_label == "deep"]
    candidates = resolution_candidates()
    growth_seeds = [12001 + 23 * i for i in range(args.growth_seeds)]
    broad_run_offsets = [3101 + 31 * i for i in range(args.run_seeds_broad)]
    final_run_offsets = [3101 + 31 * i for i in range(args.run_seeds_final)]

    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    base_summary = v10e.summarize_bases(base_rows)

    broad_run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, broad_run_offsets, regime.name)
    broad_group_rows = v10e.summarize_groups(candidates, ensembles, broad_run_rows)
    broad_ci_rows, broad_pair_rows, broad_top_rows = v10e.bootstrap_joint(candidates, ensembles, broad_run_rows, reps=int(args.bootstrap_reps), rng_seed=33031)
    broad_candidate_rows = candidate_rows_from_group_rows(candidates, broad_group_rows, broad_ci_rows, broad_top_rows)

    raw_winner = max(broad_candidate_rows, key=lambda r: v10e.safe_float(r["mean_composite"], -1.0))["candidate_name"]
    focused_winner = max(broad_candidate_rows, key=lambda r: v10e.safe_float(r["focused_score"], -1.0))["candidate_name"]
    finalist_names: List[str] = ["band_zero_del", str(raw_winner), str(focused_winner)]
    seen = set()
    finalist_names = [name for name in finalist_names if not (name in seen or seen.add(name))]
    finalists = [cand for cand in candidates if cand.name in finalist_names]

    final_run_rows = [r for r in broad_run_rows if str(r["candidate_name"]) in finalist_names]
    extra_offsets = [off for off in final_run_offsets if off not in broad_run_offsets]
    if extra_offsets:
        final_run_rows.extend(v10e.collect_run_rows(finalists, ensembles, base_states, growth_seeds, extra_offsets, regime.name))
    final_group_rows = v10e.summarize_groups(finalists, ensembles, final_run_rows)
    final_ci_rows, final_pair_rows, final_top_rows = v10e.bootstrap_joint(finalists, ensembles, final_run_rows, reps=int(args.bootstrap_reps), rng_seed=34041)
    final_candidate_rows = candidate_rows_from_group_rows(finalists, final_group_rows, final_ci_rows, final_top_rows)

    interpretation = interpret(final_candidate_rows, final_pair_rows)

    prefix = args.output_prefix
    v10e.write_csv(f"{prefix}_frontier_resolution_base_rows.csv", base_rows)
    v10e.write_csv(f"{prefix}_frontier_resolution_broad_candidate_summary.csv", broad_candidate_rows)
    v10e.write_csv(f"{prefix}_frontier_resolution_broad_pairwise.csv", broad_pair_rows)
    v10e.write_csv(f"{prefix}_frontier_resolution_final_candidate_summary.csv", final_candidate_rows)
    v10e.write_csv(f"{prefix}_frontier_resolution_final_pairwise.csv", final_pair_rows)

    for path, content in [
        (args.report_md, build_markdown(final_candidate_rows, final_pair_rows, interpretation)),
        (args.lay_md, "\n".join(["# v0.11 for ikke-spesialister", "", interpretation["convergence"], "", interpretation["recommendation"], ""])),
        (args.recommendation_md, "\n".join(["# v0.11 operativ anbefaling", "", interpretation["recommendation"], ""])),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
