#!/usr/bin/env python3
"""v0.10f frontier test around band_zero_del and band_small_triad.

Two-phase design to stay computationally tractable while still increasing
strictness relative to v0.10e:
1. Broad frontier scan with more growth seeds than v0.10e and a compact local
   candidate set around the current frontier.
2. Extra run-seed replication for the anchor pair and the best broad-scan
   candidate, yielding a sharper final comparison without reopening generator
   uncertainty.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e


# ---------------------------------------------------------------------------
# Candidate design
# ---------------------------------------------------------------------------

def rate_tag(x: float) -> str:
    return f"{int(round(1000.0 * x)):03d}"


def named_candidate(name: str, p_swap: float, p_triad: float, p_del: float) -> v09.ScaleCandidate:
    return v09.ScaleCandidate(name, 0.02, 0.00, p_swap, p_triad, p_del)


def frontier_candidates() -> List[v09.ScaleCandidate]:
    return [
        named_candidate("band_zero_del", 0.02, 0.00, 0.00),
        named_candidate("frontier_diag_mid", 0.02, 0.005, 0.005),
        named_candidate("band_small_triad", 0.02, 0.010, 0.010),
        named_candidate("band_best", 0.02, 0.000, 0.010),
        named_candidate("frontier_triad_only", 0.02, 0.010, 0.000),
        named_candidate("frontier_zero_del_swap025", 0.025, 0.000, 0.000),
        named_candidate("frontier_small_triad_swap015", 0.015, 0.010, 0.010),
    ]


def classify_candidate(name: str) -> Tuple[str, str]:
    if name.startswith("band_zero_del") or name.startswith("frontier_zero_del"):
        return ("zero_del_family", "swap_probe" if "swap" in name else "core")
    if name.startswith("band_small_triad") or name.startswith("frontier_small_triad"):
        return ("small_triad_family", "swap_probe" if "swap" in name else "core")
    if name == "band_best":
        return ("reference_axis", "core")
    if name == "frontier_diag_mid":
        return ("diagonal_bridge", "core")
    if name == "frontier_triad_only":
        return ("triad_axis", "core")
    return ("other", "core")


# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------

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
        fam, stage = classify_candidate(cand.name)
        row["frontier_family"] = fam
        row["frontier_stage"] = stage
        rows.append(row)
    v10e.add_focused_score(rows)
    rows.sort(key=lambda r: v10e.safe_float(r.get("focused_score"), -1.0), reverse=True)
    return rows


def finalists_from_broad(candidate_rows: Sequence[Dict[str, Any]]) -> List[str]:
    names = ["band_zero_del", "band_small_triad"]
    ordered = [str(r["candidate_name"]) for r in candidate_rows]
    for name in ordered:
        if name not in names:
            names.append(name)
            break
    return names


def build_markdown(
    regime_name: str,
    base_summary: Sequence[Dict[str, Any]],
    broad_candidate_rows: Sequence[Dict[str, Any]],
    final_candidate_rows: Sequence[Dict[str, Any]],
    final_pair_rows: Sequence[Dict[str, Any]],
    final_names: Sequence[str],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.10f: frontier-runde rundt band_zero_del og band_small_triad")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden gjør det neste naturlige metodiske steget etter v0.10e: vi holder generatoren fast på `fast_balanced / deep`, "
        "øker growth-seed-variasjonen i en smal lokal scan, og bruker deretter ekstra run-seed-replikasjon på den ankerbaserte fronten. "
        "Målet er å avgjøre om fronten fortsatt er todelt, om den smelter sammen til én kandidat, eller om en tredje lokal nabo begynner å dominere."
    )
    lines.append("")
    lines.append("## Realiserte startstørrelser")
    lines.append("")
    lines.append("| target | mean_initial | q10 | q90 | separated_from_prev | mean_tokens | mean_beta1 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in base_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {v10e.safe_float(row['mean_initial_nodes']):.1f} | {v10e.safe_float(row['q10_initial_nodes']):.1f} | {v10e.safe_float(row['q90_initial_nodes']):.1f} | {int(row['separated_from_prev'])} | {v10e.safe_float(row['mean_initial_tokens']):.1f} | {v10e.safe_float(row['mean_initial_beta1']):.1f} |"
        )
    lines.append("")
    lines.append("## Bred frontier-scan")
    lines.append("")
    lines.append("| candidate | family | focused_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin | quasi_large |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in broad_candidate_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['frontier_family']} | {v10e.safe_float(row['focused_score']):.3f} | {v10e.safe_float(row['mean_composite']):.3f} | {v10e.safe_float(row['ci_low_mean_composite']):.3f} | {v10e.safe_float(row['top_prob_mean_composite']):.3f} | {v10e.safe_float(row['alpha_large']):.3f} | {v10e.safe_float(row['alpha_jump']):.3f} | {v10e.safe_float(row['linear_margin']):.3f} | {v10e.safe_float(row['quasi_large']):.3f} |"
        )
    lines.append("")
    lines.append("## Finalister med ekstra run-seeds")
    lines.append("")
    lines.append("| candidate | focused_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin | quasi_large |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in final_candidate_rows:
        lines.append(
            f"| {row['candidate_name']} | {v10e.safe_float(row['focused_score']):.3f} | {v10e.safe_float(row['mean_composite']):.3f} | {v10e.safe_float(row['ci_low_mean_composite']):.3f} | {v10e.safe_float(row['top_prob_mean_composite']):.3f} | {v10e.safe_float(row['alpha_large']):.3f} | {v10e.safe_float(row['alpha_jump']):.3f} | {v10e.safe_float(row['linear_margin']):.3f} | {v10e.safe_float(row['quasi_large']):.3f} |"
        )
    lines.append("")
    lines.append("## Pairwise sannsynligheter i finalefeltet")
    lines.append("")
    lines.append("| a | b | P(a > b) |")
    lines.append("| --- | --- | --- |")
    for row in sorted(final_pair_rows, key=lambda r: (str(r['candidate_a']), str(r['candidate_b']))):
        if str(row['candidate_a']) in final_names and str(row['candidate_b']) in final_names:
            lines.append(f"| {row['candidate_a']} | {row['candidate_b']} | {v10e.safe_float(row['prob_a_gt_b_mean_composite']):.3f} |")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append(
        "Hvis `band_zero_del` og `band_small_triad` fortsatt begge ligger i toppen etter ekstra run-seeds, bør prosjektet foreløpig holde to kandidater åpne. "
        "Hvis én av dem begynner å dominere også i det utvidede finalefeltet, er det grunnlag for å gjøre den til operativ standard i neste runde. "
        "Hvis en tredje lokal nabo tar over, er det et tegn på at fronten fortsatt må kartlegges litt finere før vi låser oss til én etikett."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.10f frontier test")
    ap.add_argument("--growth-regime", type=str, default="fast_balanced")
    ap.add_argument("--targets", type=str, default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=4)
    ap.add_argument("--run-seeds-broad", type=int, default=3)
    ap.add_argument("--run-seeds-final", type=int, default=4)
    ap.add_argument("--bootstrap-reps", type=int, default=350)
    ap.add_argument("--output-prefix", type=str, default="/mnt/data/v10f")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [e for e in v10b.build_ensembles(targets) if e.burnin_label == "deep"]
    candidates = frontier_candidates()

    growth_seeds = [10101 + 29 * i for i in range(args.growth_seeds)]
    broad_run_offsets = [2101 + 37 * i for i in range(args.run_seeds_broad)]
    final_run_offsets = [2101 + 37 * i for i in range(args.run_seeds_final)]

    print("[v10f] building bases...", flush=True)
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    print("[v10f] bases done", flush=True)
    base_summary = v10e.summarize_bases(base_rows)

    print("[v10f] broad scan runs...", flush=True)
    broad_run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, broad_run_offsets, regime.name)
    print(f"[v10f] broad runs done: {len(broad_run_rows)} rows", flush=True)
    broad_group_rows = v10e.summarize_groups(candidates, ensembles, broad_run_rows)
    print("[v10f] broad bootstrap...", flush=True)
    broad_ci_rows, broad_pair_rows, broad_top_rows = v10e.bootstrap_joint(
        candidates,
        ensembles,
        broad_run_rows,
        reps=int(args.bootstrap_reps),
        rng_seed=28031,
    )
    broad_candidate_rows = candidate_rows_from_group_rows(candidates, broad_group_rows, broad_ci_rows, broad_top_rows)

    final_names = finalists_from_broad(broad_candidate_rows)
    final_candidates = [cand for cand in candidates if cand.name in final_names]
    print(f"[v10f] finalists: {final_names}", flush=True)
    final_run_rows = [r for r in broad_run_rows if str(r["candidate_name"]) in final_names]
    extra_offsets = [off for off in final_run_offsets if off not in broad_run_offsets]
    if extra_offsets:
        print("[v10f] finalist extra runs...", flush=True)
        final_run_rows.extend(v10e.collect_run_rows(final_candidates, ensembles, base_states, growth_seeds, extra_offsets, regime.name))
        print(f"[v10f] finalist rows now: {len(final_run_rows)}", flush=True)
    final_group_rows = v10e.summarize_groups(final_candidates, ensembles, final_run_rows)
    print("[v10f] finalist bootstrap...", flush=True)
    final_ci_rows, final_pair_rows, final_top_rows = v10e.bootstrap_joint(
        final_candidates,
        ensembles,
        final_run_rows,
        reps=int(args.bootstrap_reps),
        rng_seed=29041,
    )
    final_candidate_rows = candidate_rows_from_group_rows(final_candidates, final_group_rows, final_ci_rows, final_top_rows)
    final_profile_rows = v10e.size_profiles(final_names, final_group_rows)

    prefix = args.output_prefix
    v10e.write_csv(f"{prefix}_frontier_base_rows.csv", base_rows)
    v10e.write_csv(f"{prefix}_frontier_base_summary.csv", base_summary)
    v10e.write_csv(f"{prefix}_frontier_broad_run_rows.csv", broad_run_rows)
    v10e.write_csv(f"{prefix}_frontier_broad_group_rows.csv", broad_group_rows)
    v10e.write_csv(f"{prefix}_frontier_broad_candidate_summary.csv", broad_candidate_rows)
    v10e.write_csv(f"{prefix}_frontier_broad_pairwise.csv", broad_pair_rows)
    v10e.write_csv(f"{prefix}_frontier_finalists.csv", [{"candidate_name": n} for n in final_names])
    v10e.write_csv(f"{prefix}_frontier_final_run_rows.csv", final_run_rows)
    v10e.write_csv(f"{prefix}_frontier_final_group_rows.csv", final_group_rows)
    v10e.write_csv(f"{prefix}_frontier_final_candidate_summary.csv", final_candidate_rows)
    v10e.write_csv(f"{prefix}_frontier_final_pairwise.csv", final_pair_rows)
    v10e.write_csv(f"{prefix}_frontier_final_size_profiles.csv", final_profile_rows)
    print("[v10f] writing outputs...", flush=True)
    Path(f"{prefix}_frontier_validation.md").write_text(
        build_markdown(regime.name, base_summary, broad_candidate_rows, final_candidate_rows, final_pair_rows, final_names),
        encoding="utf-8",
    )
    print("[v10f] done", flush=True)


if __name__ == "__main__":
    main()
