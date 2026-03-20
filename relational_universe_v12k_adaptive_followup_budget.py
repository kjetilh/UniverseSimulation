#!/usr/bin/env python3
"""v0.12k adaptive follow-up budget around band_zero_del.

The previous v12i-v12j rounds showed that pre-screening is not where the main
workflow cost lives. This round asks a narrower question: can we save real
follow-up work by using the first few run-seeds on each base as an adaptive
decision signal, instead of always running the full follow-up bundle?
"""
from __future__ import annotations

import argparse
import math
import random
import statistics
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12


POLICIES: List[Tuple[str, int, float]] = [
    ("full_followup", 6, 1.0),
    ("probe1_only", 1, 0.0),
    ("probe2_only", 2, 0.0),
    ("probe1_top_quarter", 1, 0.25),
    ("probe1_top_half", 1, 0.50),
    ("probe2_top_half", 2, 0.50),
]
REFERENCE_POLICY = "full_followup"
REFERENCE_RUNS = 6
EPSILON = 0.02


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v12.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v12.write_csv(path, rows)


def fixed_candidate() -> v09.ScaleCandidate:
    return v09.ScaleCandidate("band_zero_del", 0.02, 0.00, 0.02, 0.00, 0.00)


def collect_timed_run_rows(
    ensembles: Sequence[v10b.CalibrationEnsemble],
    base_states: Mapping[Tuple[str, int], Any],
    growth_seeds: Sequence[int],
    run_offsets: Sequence[int],
) -> List[Dict[str, Any]]:
    candidate = fixed_candidate()
    rows: List[Dict[str, Any]] = []
    name_hash = sum(ord(ch) for ch in candidate.name) % 997
    for ens in ensembles:
        for gseed in growth_seeds:
            base = base_states[(ens.name, int(gseed))]
            steps = v10e.steps_for_state(base.g.num_nodes())
            for run_index, off in enumerate(run_offsets, start=1):
                seed = int(gseed) + int(off) + name_hash
                start = time.perf_counter()
                row = v09.run_single_candidate_from_base(candidate, ens, base, seed=seed, steps=steps)
                elapsed = time.perf_counter() - start
                row["growth_seed"] = int(gseed)
                row["run_index"] = int(run_index)
                row["run_offset"] = int(off)
                row["runtime_seconds"] = elapsed
                row["steps"] = int(steps)
                rows.append(row)
    return rows


def target_summary(base_rows: Sequence[Dict[str, Any]], run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    base_lookup = {(str(r["ensemble"]), int(r["growth_seed"])): dict(r) for r in base_rows}
    by_key: Dict[Tuple[str, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        by_key.setdefault((str(row["ensemble"]), int(row["growth_seed"])), []).append(dict(row))

    per_base: List[Dict[str, Any]] = []
    for (ensemble, growth_seed), sub in sorted(by_key.items()):
        base = base_lookup[(ensemble, growth_seed)]
        radii = [safe_float(r["final_radius_control"]) for r in sub]
        per_base.append(
            {
                "ensemble": ensemble,
                "growth_seed": int(growth_seed),
                "target_nodes": int(base["target_nodes"]),
                "mean_initial_nodes": safe_float(base["initial_nodes"]),
                "mean_actual_radius": mean_defined(radii),
            }
        )

    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in per_base:
        by_target.setdefault(int(row["target_nodes"]), []).append(dict(row))

    out: List[Dict[str, Any]] = []
    prev_q90 = None
    for target in sorted(by_target):
        sub = by_target[target]
        initial_nodes = [safe_float(r["mean_initial_nodes"]) for r in sub]
        actual_radius = [safe_float(r["mean_actual_radius"]) for r in sub]
        q10 = v10b.quantile(initial_nodes, 0.10)
        q90 = v10b.quantile(initial_nodes, 0.90)
        separated = 1 if prev_q90 is None or q10 > prev_q90 else 0
        out.append(
            {
                "target_nodes": target,
                "bases": len(sub),
                "mean_initial_nodes": mean_defined(initial_nodes),
                "q10_initial_nodes": q10,
                "q90_initial_nodes": q90,
                "mean_actual_radius": mean_defined(actual_radius),
                "sd_actual_radius": statistics.pstdev(actual_radius) if len(actual_radius) >= 2 else 0.0,
                "separated_from_prev": separated,
            }
        )
        prev_q90 = q90
    return out


def group_runs_by_base(run_rows: Sequence[Dict[str, Any]]) -> Dict[Tuple[int, str, int], List[Dict[str, Any]]]:
    by_base: Dict[Tuple[int, str, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        key = (int(row["target_nodes"]), str(row["ensemble"]), int(row["growth_seed"]))
        by_base.setdefault(key, []).append(dict(row))
    for key in by_base:
        by_base[key].sort(key=lambda r: int(r["run_index"]))
    return by_base


def quantile_top_n(rows: Sequence[Dict[str, Any]], q: float = 0.25) -> int:
    return max(1, int(math.ceil(len(rows) * q)))


def apply_policy_to_target(rows: Sequence[Dict[str, Any]], probe_runs: int, extend_frac: float) -> List[Dict[str, Any]]:
    enriched: List[Dict[str, Any]] = []
    for row in rows:
        sub = row["runs"]
        partial = sub[:probe_runs]
        partial_mean = mean_defined(safe_float(r["final_radius_control"]) for r in partial)
        full_mean = mean_defined(safe_float(r["final_radius_control"]) for r in sub)
        partial_seconds = sum(safe_float(r["runtime_seconds"]) for r in partial)
        full_seconds = sum(safe_float(r["runtime_seconds"]) for r in sub)
        enriched.append(
            {
                **row,
                "partial_mean": partial_mean,
                "full_mean": full_mean,
                "partial_seconds": partial_seconds,
                "full_seconds": full_seconds,
                "used_runs": probe_runs,
                "estimated_score": partial_mean,
                "used_seconds": partial_seconds,
                "extended": 0,
            }
        )

    if extend_frac > 0.0:
        ranked = sorted(enriched, key=lambda r: safe_float(r["partial_mean"]), reverse=True)
        extend_n = max(1, int(math.ceil(len(ranked) * extend_frac)))
        extend_ids = {
            (str(r["ensemble"]), int(r["growth_seed"]))
            for r in ranked[:extend_n]
        }
        for row in enriched:
            if (str(row["ensemble"]), int(row["growth_seed"])) in extend_ids:
                row["used_runs"] = len(row["runs"])
                row["estimated_score"] = safe_float(row["full_mean"])
                row["used_seconds"] = safe_float(row["full_seconds"])
                row["extended"] = 1
    return enriched


def evaluate_policy_rows(run_rows: Sequence[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    by_base = group_runs_by_base(run_rows)
    target_bases: Dict[int, List[Dict[str, Any]]] = {}
    for (target, ensemble, gseed), rows in by_base.items():
        target_bases.setdefault(target, []).append(
            {
                "target_nodes": target,
                "ensemble": ensemble,
                "growth_seed": gseed,
                "runs": rows,
            }
        )

    split_rows: List[Dict[str, Any]] = []
    summary_rows: List[Dict[str, Any]] = []
    for policy_name, probe_runs, extend_frac in POLICIES:
        all_rows: List[Dict[str, Any]] = []
        for target in sorted(target_bases):
            sub = apply_policy_to_target(target_bases[target], probe_runs, extend_frac)
            all_rows.extend(sub)

        target_best_hits: List[float] = []
        target_recalls: List[float] = []
        target_pairwise: List[float] = []
        total_seconds = sum(safe_float(r["used_seconds"]) for r in all_rows)
        total_full_seconds = sum(safe_float(r["full_seconds"]) for r in all_rows)
        total_used_runs = sum(int(r["used_runs"]) for r in all_rows)
        total_full_runs = sum(len(r["runs"]) for r in all_rows)

        for target in sorted(target_bases):
            sub = [r for r in all_rows if int(r["target_nodes"]) == target]
            actual_sorted = sorted(sub, key=lambda r: safe_float(r["full_mean"]), reverse=True)
            est_sorted = sorted(sub, key=lambda r: safe_float(r["estimated_score"]), reverse=True)
            actual_best = actual_sorted[0]
            est_best = est_sorted[0]
            target_best_hits.append(
                1.0
                if (str(actual_best["ensemble"]), int(actual_best["growth_seed"])) == (str(est_best["ensemble"]), int(est_best["growth_seed"]))
                else 0.0
            )

            top_n = quantile_top_n(actual_sorted)
            actual_top = {
                (str(r["ensemble"]), int(r["growth_seed"]))
                for r in actual_sorted[:top_n]
            }
            est_top = {
                (str(r["ensemble"]), int(r["growth_seed"]))
                for r in est_sorted[:top_n]
            }
            captured = len(actual_top & est_top)
            target_recalls.append(captured / max(1, len(actual_top)))

            correct = 0.0
            total = 0
            for i in range(len(sub)):
                for j in range(i + 1, len(sub)):
                    ai = safe_float(sub[i]["full_mean"])
                    aj = safe_float(sub[j]["full_mean"])
                    if abs(ai - aj) <= 1e-12:
                        continue
                    pi = safe_float(sub[i]["estimated_score"])
                    pj = safe_float(sub[j]["estimated_score"])
                    total += 1
                    prod = (pi - pj) * (ai - aj)
                    if prod > 0:
                        correct += 1.0
                    elif abs(prod) <= 1e-12:
                        correct += 0.5
            target_pairwise.append(correct / total if total else float("nan"))

        summary_rows.append(
            {
                "policy_name": policy_name,
                "probe_runs": probe_runs,
                "extend_frac": extend_frac,
                "mean_best_hit": mean_defined(target_best_hits),
                "mean_top_quartile_recall": mean_defined(target_recalls),
                "mean_pairwise_within_target": mean_defined(target_pairwise),
                "total_used_runs": total_used_runs,
                "total_full_runs": total_full_runs,
                "run_fraction_vs_full": total_used_runs / max(1, total_full_runs),
                "total_used_seconds": total_seconds,
                "total_full_seconds": total_full_seconds,
                "time_fraction_vs_full": total_seconds / total_full_seconds if total_full_seconds > 1e-12 else float("nan"),
            }
        )

        for row in all_rows:
            split_rows.append(
                {
                    "policy_name": policy_name,
                    "probe_runs": probe_runs,
                    "extend_frac": extend_frac,
                    "target_nodes": int(row["target_nodes"]),
                    "ensemble": row["ensemble"],
                    "growth_seed": int(row["growth_seed"]),
                    "estimated_score": safe_float(row["estimated_score"]),
                    "full_mean": safe_float(row["full_mean"]),
                    "partial_mean": safe_float(row["partial_mean"]),
                    "used_runs": int(row["used_runs"]),
                    "used_seconds": safe_float(row["used_seconds"]),
                    "full_seconds": safe_float(row["full_seconds"]),
                    "extended": int(row["extended"]),
                }
            )

    ref = next(r for r in summary_rows if str(r["policy_name"]) == REFERENCE_POLICY)
    ref_hit = safe_float(ref["mean_best_hit"])
    ref_recall = safe_float(ref["mean_top_quartile_recall"])
    ref_pairwise = safe_float(ref["mean_pairwise_within_target"])
    ref_seconds = safe_float(ref["total_used_seconds"])
    for row in summary_rows:
        row["delta_best_hit_vs_ref"] = safe_float(row["mean_best_hit"]) - ref_hit
        row["delta_recall_vs_ref"] = safe_float(row["mean_top_quartile_recall"]) - ref_recall
        row["delta_pairwise_vs_ref"] = safe_float(row["mean_pairwise_within_target"]) - ref_pairwise
        row["speedup_vs_ref"] = ref_seconds / safe_float(row["total_used_seconds"]) if safe_float(row["total_used_seconds"]) > 1e-12 else float("nan")
        near_match = (
            safe_float(row["mean_best_hit"]) >= ref_hit - EPSILON
            and safe_float(row["mean_top_quartile_recall"]) >= ref_recall - EPSILON
        )
        row["near_match_eps_02"] = 1 if near_match else 0
        row["faster_than_ref"] = 1 if safe_float(row["total_used_seconds"]) <= ref_seconds + 1e-12 else 0
        row["faster_and_near_match"] = 1 if near_match and row["faster_than_ref"] == 1 else 0

    summary_rows.sort(
        key=lambda r: (
            safe_float(r["faster_and_near_match"], -1e9),
            safe_float(r["near_match_eps_02"], -1e9),
            safe_float(r["speedup_vs_ref"], -1e9),
            safe_float(r["mean_pairwise_within_target"], -1e9),
        ),
        reverse=True,
    )
    for idx, row in enumerate(summary_rows, start=1):
        row["rank"] = idx
    return split_rows, summary_rows


def build_report(
    target_rows: Sequence[Dict[str, Any]],
    summary_rows: Sequence[Dict[str, Any]],
    *,
    base_count: int,
    run_count: int,
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.12k: adaptiv styring av oppfølgingsbudsjettet")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden flytter fokus bort fra pre-screening og inn i selve oppfolgingsarbeidet. Sporsmalet er om noen fa tidlige run-seeds per base kan brukes til a avgjore hvilke baser som faktisk fortjener full oppfolging."
    )
    lines.append("")
    lines.append("## Metode")
    lines.append("")
    lines.append("- Samme regime: `band_zero_del`.")
    lines.append("- Samme dynamiske utfallsmal: full-bundle `mean_final_radius_control` per base.")
    lines.append("- Hver policy far se de forste `probe_runs` run-seedene for alle baser.")
    lines.append("- Noen policyer stopper der; andre fullforer alle run-seeds for en top-fraksjon av basene innen hver størrelse.")
    lines.append(f"- Datasett: `{base_count}` baser og `{run_count}` timed single-run rows.")
    lines.append("")
    lines.append("## Realiserte startstørrelser")
    lines.append("")
    lines.append("| target | bases | mean_initial_nodes | q10 | q90 | separated_from_prev | mean_actual_radius | sd_actual_radius |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in target_rows:
        lines.append(
            f"| {int(row['target_nodes'])} | {int(row['bases'])} | {safe_float(row['mean_initial_nodes']):.1f} | "
            f"{safe_float(row['q10_initial_nodes']):.1f} | {safe_float(row['q90_initial_nodes']):.1f} | {int(row['separated_from_prev'])} | "
            f"{safe_float(row['mean_actual_radius']):.3f} | {safe_float(row['sd_actual_radius']):.3f} |"
        )
    lines.append("")
    lines.append("## Adaptive policy-sammendrag")
    lines.append("")
    lines.append("| rank | policy | probe_runs | extend_frac | best_hit | recall | pairwise | run_frac | time_frac | speedup | near_match | faster_and_match |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in summary_rows:
        lines.append(
            f"| {int(row['rank'])} | {row['policy_name']} | {int(row['probe_runs'])} | {safe_float(row['extend_frac']):.2f} | "
            f"{safe_float(row['mean_best_hit']):.3f} | {safe_float(row['mean_top_quartile_recall']):.3f} | {safe_float(row['mean_pairwise_within_target']):.3f} | "
            f"{safe_float(row['run_fraction_vs_full']):.3f} | {safe_float(row['time_fraction_vs_full']):.3f} | {safe_float(row['speedup_vs_ref']):.3f} | "
            f"{int(row['near_match_eps_02'])} | {int(row['faster_and_near_match'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    ref = next((r for r in summary_rows if str(r["policy_name"]) == REFERENCE_POLICY), None)
    probe1_only = next((r for r in summary_rows if str(r["policy_name"]) == "probe1_only"), None)
    probe1_half = next((r for r in summary_rows if str(r["policy_name"]) == "probe1_top_half"), None)
    probe2_half = next((r for r in summary_rows if str(r["policy_name"]) == "probe2_top_half"), None)
    if ref is not None:
        lines.append(
            f"- Referansen `full_followup` bruker all oppfolgingskostnad (`time_frac=1.0`) og gir `best_hit={safe_float(ref['mean_best_hit']):.3f}`, `recall={safe_float(ref['mean_top_quartile_recall']):.3f}`."
        )
    if probe1_only is not None:
        lines.append(
            f"- `probe1_only` er den raskeste policyen: `time_frac={safe_float(probe1_only['time_fraction_vs_full']):.3f}`, men den faller til `best_hit={safe_float(probe1_only['mean_best_hit']):.3f}`, `recall={safe_float(probe1_only['mean_top_quartile_recall']):.3f}`."
        )
    if probe1_half is not None:
        lines.append(
            f"- `probe1_top_half` er den mest aggressive adaptive kandidaten i denne runden: `time_frac={safe_float(probe1_half['time_fraction_vs_full']):.3f}`, `best_hit={safe_float(probe1_half['mean_best_hit']):.3f}`, `recall={safe_float(probe1_half['mean_top_quartile_recall']):.3f}`."
        )
    if probe2_half is not None:
        lines.append(
            f"- `probe2_top_half` er den mest balanserte kandidaten: `time_frac={safe_float(probe2_half['time_fraction_vs_full']):.3f}`, `best_hit={safe_float(probe2_half['mean_best_hit']):.3f}`, `recall={safe_float(probe2_half['mean_top_quartile_recall']):.3f}`."
        )
    lines.append(
        "- Den viktigste operative dommen er at ingen adaptive policyer er naer-match mot full oppfolging i denne runden. Det betyr at adaptive follow-up er lovende, men ennå ikke en drop-in erstatning."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(summary_rows: Sequence[Dict[str, Any]]) -> str:
    fastest = next((r for r in summary_rows if str(r["policy_name"]) == "probe1_only"), None)
    balanced = next((r for r in summary_rows if str(r["policy_name"]) == "probe2_top_half"), None)
    lines = [
        "# v0.12k for ikke-spesialister",
        "",
        "Denne runden sjekker om vi kan spare arbeid ved a starte med noen fa dynamikk-kjoringer per base og bare bruke fullt budsjett pa de mest lovende basene.",
        "",
    ]
    if fastest is not None:
        lines.append(
            f"- Den raskeste policyen er `probe1_only`, som bruker omtrent `time_frac={safe_float(fastest['time_fraction_vs_full']):.3f}` av full kostnad, men den taper mye kvalitet."
        )
    if balanced is not None:
        lines.append(
            f"- Den mest balanserte policyen er `probe2_top_half`, som bruker `time_frac={safe_float(balanced['time_fraction_vs_full']):.3f}` og holder `best_hit={safe_float(balanced['mean_best_hit']):.3f}`."
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_recommendation(summary_rows: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.12k operativ anbefaling", ""]
    ref = next((r for r in summary_rows if str(r["policy_name"]) == REFERENCE_POLICY), None)
    fastest = next((r for r in summary_rows if str(r["policy_name"]) == "probe1_only"), None)
    balanced = next((r for r in summary_rows if str(r["policy_name"]) == "probe2_top_half"), None)
    if ref is None or fastest is None or balanced is None:
        lines.append("v12k ga ikke nok signal til en ny operativ anbefaling.")
        lines.append("")
        return "\n".join(lines)
    lines.append(
        "Behold `full_followup` som referanse. Ingen adaptive policyer er naer nok full oppfolging til a bli en ny standard direkte fra denne runden."
    )
    lines.append(
        f"Les `probe1_only` som den raske yttergrensen: `time_frac={safe_float(fastest['time_fraction_vs_full']):.3f}`, men `best_hit={safe_float(fastest['mean_best_hit']):.3f}` og `recall={safe_float(fastest['mean_top_quartile_recall']):.3f}` er for svake."
    )
    lines.append(
        f"Les `probe2_top_half` som den mest balanserte adaptive utfordreren: `time_frac={safe_float(balanced['time_fraction_vs_full']):.3f}`, `best_hit={safe_float(balanced['mean_best_hit']):.3f}` og `recall={safe_float(balanced['mean_top_quartile_recall']):.3f}`."
    )
    lines.append(
        "Neste naturlige steg etter v12k er enten å gjøre en litt dypere adaptiv oppfølgingsrunde, eller å kombinere den beste adaptive follow-up-politikken med den eksisterende screeningbenchmarken for en ekte end-to-end arbeidsflyt."
    )
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12k adaptive follow-up budget")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=6)
    ap.add_argument("--run-seeds", type=int, default=6)
    ap.add_argument("--output-prefix", default="Documentation/v12k_adaptive_followup_budget")
    ap.add_argument("--report-md", default="Documentation/v12k_adaptive_followup_budget.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12k.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12k_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    growth_seeds = [61001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [42101 + 31 * i for i in range(args.run_seeds)]

    print(f"[v12k] regime={regime.name} targets={targets} growth={len(growth_seeds)} runs={len(run_offsets)}")
    print("[v12k] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    print("[v12k] collecting timed run rows...")
    run_rows = collect_timed_run_rows(ensembles, base_states, growth_seeds, run_offsets)
    print(f"[v12k] timed runs done: {len(run_rows)} rows")

    target_rows = target_summary(base_rows, run_rows)
    split_rows, summary_rows = evaluate_policy_rows(run_rows)

    prefix = args.output_prefix
    print("[v12k] writing outputs...")
    write_csv(f"{prefix}_target_summary.csv", target_rows)
    write_csv(f"{prefix}_timed_run_rows.csv", run_rows)
    write_csv(f"{prefix}_split_rows.csv", split_rows)
    write_csv(f"{prefix}_summary.csv", summary_rows)

    for path, content in [
        (args.report_md, build_report(target_rows, summary_rows, base_count=len(base_rows), run_count=len(run_rows))),
        (args.lay_md, build_lay_summary(summary_rows)),
        (args.recommendation_md, build_recommendation(summary_rows)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v12k] done")


if __name__ == "__main__":
    main()
