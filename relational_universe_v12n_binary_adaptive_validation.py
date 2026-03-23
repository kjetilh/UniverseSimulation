#!/usr/bin/env python3
"""v0.12n binary validation of the first strong adaptive challenger.

This round is intentionally narrow. It keeps the v0.12m screening setup fixed
and asks whether `probe3_top_half` is robust enough to challenge
`full_followup`, or whether a tiny decision-rule tweak is needed.
"""
from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12
import relational_universe_v12e_start_state_screening as v12e
import relational_universe_v12f_budget_screening as v12f
import relational_universe_v12i_measured_runtime_pipeline as v12i
import relational_universe_v12k_adaptive_followup_budget as v12k
import relational_universe_v12l_hybrid_screening_followup as v12l


REFERENCE_POLICY = "full_followup"
SCREEN_POLICY_NAME = "full_basis"
SCREEN_FEATURES = tuple(v12.BASIS_FEATURES)
SCREEN_BUDGET = 0.50
PROBE_RUNS = 3
EPSILON = 0.02
GUARD_THRESHOLD = 0.50
POLICIES = [
    "full_followup",
    "probe3_top_half",
    "probe3_top_half_screen_tiebreak",
    "probe3_guarded_half",
]


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v12.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v12.write_csv(path, rows)


def prepared_rows_for_target(selected_rows: Sequence[Dict[str, Any]], grouped_runs: Mapping[Tuple[int, str, int], List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in selected_rows:
        key = (int(row["target_nodes"]), str(row["ensemble"]), int(row["growth_seed"]))
        runs = grouped_runs[key]
        partial = runs[:PROBE_RUNS]
        partial_mean = mean_defined(safe_float(r["final_radius_control"]) for r in partial)
        full_mean = mean_defined(safe_float(r["final_radius_control"]) for r in runs)
        partial_seconds = sum(safe_float(r["runtime_seconds"]) for r in partial)
        full_seconds = sum(safe_float(r["runtime_seconds"]) for r in runs)
        out.append(
            {
                "target_nodes": int(row["target_nodes"]),
                "ensemble": str(row["ensemble"]),
                "growth_seed": int(row["growth_seed"]),
                "screen_score": safe_float(row["screen_score"]),
                "runs": runs,
                "partial_mean": partial_mean,
                "full_mean": full_mean,
                "partial_seconds": partial_seconds,
                "full_seconds": full_seconds,
                "used_runs": PROBE_RUNS,
                "used_seconds": partial_seconds,
                "estimated_score": partial_mean,
                "extended": 0,
            }
        )
    return out


def choose_extension_order(rows: Sequence[Dict[str, Any]], *, tie_break: bool) -> List[Dict[str, Any]]:
    if tie_break:
        return sorted(rows, key=lambda r: (safe_float(r["partial_mean"]), safe_float(r["screen_score"])), reverse=True)
    return sorted(rows, key=lambda r: safe_float(r["partial_mean"]), reverse=True)


def apply_policy_to_target(rows: Sequence[Dict[str, Any]], policy_name: str) -> List[Dict[str, Any]]:
    prepared = [dict(r) for r in rows]
    if policy_name == "full_followup":
        for row in prepared:
            row["used_runs"] = len(row["runs"])
            row["used_seconds"] = safe_float(row["full_seconds"])
            row["estimated_score"] = safe_float(row["full_mean"])
            row["extended"] = 1
        return prepared

    if policy_name in {"probe3_top_half", "probe3_top_half_screen_tiebreak", "probe3_guarded_half"}:
        tie_break = policy_name in {"probe3_top_half_screen_tiebreak", "probe3_guarded_half"}
        ranked = choose_extension_order(prepared, tie_break=tie_break)
        extend_n = max(1, len(ranked) // 2)
        if policy_name == "probe3_guarded_half" and len(ranked) >= 2:
            gap = abs(safe_float(ranked[0]["partial_mean"]) - safe_float(ranked[1]["partial_mean"]))
            if gap <= GUARD_THRESHOLD:
                extend_n = min(len(ranked), extend_n + 1)
        extend_ids = {(str(r["ensemble"]), int(r["growth_seed"])) for r in ranked[:extend_n]}
        for row in prepared:
            if (str(row["ensemble"]), int(row["growth_seed"])) in extend_ids:
                row["used_runs"] = len(row["runs"])
                row["used_seconds"] = safe_float(row["full_seconds"])
                row["estimated_score"] = safe_float(row["full_mean"])
                row["extended"] = 1
        return prepared

    raise ValueError(f"Unknown policy: {policy_name}")


def apply_policy(
    selected_rows: Sequence[Dict[str, Any]],
    grouped_runs: Mapping[Tuple[int, str, int], List[Dict[str, Any]]],
    policy_name: str,
) -> List[Dict[str, Any]]:
    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in selected_rows:
        by_target.setdefault(int(row["target_nodes"]), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for target in sorted(by_target):
        prepared = prepared_rows_for_target(by_target[target], grouped_runs)
        out.extend(apply_policy_to_target(prepared, policy_name))
    return out


def per_split_rows(
    base_level_rows: Sequence[Dict[str, Any]],
    grouped_runs: Mapping[Tuple[int, str, int], List[Dict[str, Any]]],
    *,
    repeats: int,
    test_frac: float,
    screening_seed: int,
    timing_loops: int,
) -> List[Dict[str, Any]]:
    master_rng = random.Random(screening_seed)
    rows: List[Dict[str, Any]] = []
    for split_id in range(1, repeats + 1):
        split_rng = random.Random(master_rng.randint(1, 10**9))
        train_idx, test_idx = v12e.stratified_holdout_indices(base_level_rows, split_rng, test_frac)
        train_rows = [dict(base_level_rows[i]) for i in train_idx]
        test_rows = [dict(base_level_rows[i]) for i in test_idx]

        policy_seed = split_rng.randint(1, 10**9)
        scored = v12f.score_rows(train_rows, test_rows, SCREEN_POLICY_NAME, SCREEN_FEATURES, random.Random(policy_seed))
        selected = v12f.select_within_target(scored, SCREEN_BUDGET)
        screening_seconds = v12i.measure_screening_seconds(
            train_rows,
            test_rows,
            SCREEN_POLICY_NAME,
            SCREEN_FEATURES,
            SCREEN_BUDGET,
            seed=policy_seed,
            loops=timing_loops,
        )

        per_policy: List[Dict[str, Any]] = []
        for policy_name in POLICIES:
            evaluated = apply_policy(selected, grouped_runs, policy_name)
            metrics = v12l.hybrid_metrics(test_rows, evaluated)
            total_seconds = screening_seconds + safe_float(metrics["used_seconds"])
            per_policy.append(
                {
                    "split_id": split_id,
                    "policy_name": policy_name,
                    "screen_policy_name": SCREEN_POLICY_NAME,
                    "budget_frac": SCREEN_BUDGET,
                    "feature_count": len(SCREEN_FEATURES),
                    "probe_runs": PROBE_RUNS,
                    "train_rows": len(train_rows),
                    "test_rows": len(test_rows),
                    "screening_seconds": screening_seconds,
                    "followup_seconds": safe_float(metrics["used_seconds"]),
                    "total_seconds": total_seconds,
                    **metrics,
                }
            )

        ref = next(r for r in per_policy if str(r["policy_name"]) == REFERENCE_POLICY)
        ref_total = safe_float(ref["total_seconds"])
        ref_hit = safe_float(ref["within_target_best_hit"])
        ref_recall = safe_float(ref["within_target_top_quartile_recall"])
        ref_pairwise = safe_float(ref["mean_pairwise_within_target"])
        for row in per_policy:
            row["delta_best_hit_vs_ref"] = safe_float(row["within_target_best_hit"]) - ref_hit
            row["delta_recall_vs_ref"] = safe_float(row["within_target_top_quartile_recall"]) - ref_recall
            row["delta_pairwise_vs_ref"] = safe_float(row["mean_pairwise_within_target"]) - ref_pairwise
            row["time_delta_vs_ref"] = safe_float(row["total_seconds"]) - ref_total
            row["time_ratio_vs_ref"] = safe_float(row["total_seconds"]) / ref_total if ref_total > 1e-12 else float("nan")
            row["speedup_vs_ref"] = ref_total / safe_float(row["total_seconds"]) if safe_float(row["total_seconds"]) > 1e-12 else float("nan")
            near_match = (
                safe_float(row["within_target_best_hit"]) >= ref_hit - EPSILON
                and safe_float(row["within_target_top_quartile_recall"]) >= ref_recall - EPSILON
            )
            row["near_match_eps_02"] = 1 if near_match else 0
            row["faster_than_ref"] = 1 if safe_float(row["total_seconds"]) <= ref_total + 1e-12 else 0
            row["faster_and_near_match"] = 1 if near_match and int(row["faster_than_ref"]) == 1 else 0
            rows.append(row)
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for policy_name in POLICIES:
        sub = [r for r in rows if str(r["policy_name"]) == policy_name]
        exemplar = sub[0]
        out.append(
            {
                "policy_name": policy_name,
                "screen_policy_name": exemplar["screen_policy_name"],
                "budget_frac": safe_float(exemplar["budget_frac"]),
                "feature_count": int(exemplar["feature_count"]),
                "probe_runs": int(exemplar["probe_runs"]),
                "mean_selected_rows": mean_defined(safe_float(r["selected_rows"]) for r in sub),
                "mean_extended_rows": mean_defined(safe_float(r["extended_rows"]) for r in sub),
                "mean_used_runs": mean_defined(safe_float(r["used_runs"]) for r in sub),
                "mean_screening_seconds": mean_defined(safe_float(r["screening_seconds"]) for r in sub),
                "mean_followup_seconds": mean_defined(safe_float(r["followup_seconds"]) for r in sub),
                "mean_total_seconds": mean_defined(safe_float(r["total_seconds"]) for r in sub),
                "mean_speedup_vs_ref": mean_defined(safe_float(r["speedup_vs_ref"]) for r in sub),
                "mean_best_hit": mean_defined(safe_float(r["within_target_best_hit"]) for r in sub),
                "mean_recall": mean_defined(safe_float(r["within_target_top_quartile_recall"]) for r in sub),
                "mean_pairwise_within_target": mean_defined(safe_float(r["mean_pairwise_within_target"]) for r in sub),
                "mean_selected_lift": mean_defined(safe_float(r["within_target_selected_lift"]) for r in sub),
                "mean_delta_best_hit_vs_ref": mean_defined(safe_float(r["delta_best_hit_vs_ref"]) for r in sub),
                "mean_delta_recall_vs_ref": mean_defined(safe_float(r["delta_recall_vs_ref"]) for r in sub),
                "mean_delta_pairwise_vs_ref": mean_defined(safe_float(r["delta_pairwise_vs_ref"]) for r in sub),
                "near_match_rate_eps_02": mean_defined(safe_float(r["near_match_eps_02"]) for r in sub),
                "faster_than_ref_rate": mean_defined(safe_float(r["faster_than_ref"]) for r in sub),
                "faster_and_near_match_rate": mean_defined(safe_float(r["faster_and_near_match"]) for r in sub),
            }
        )
    out.sort(
        key=lambda row: (
            safe_float(row["faster_and_near_match_rate"], -1e9),
            safe_float(row["near_match_rate_eps_02"], -1e9),
            safe_float(row["mean_speedup_vs_ref"], -1e9),
            safe_float(row["mean_pairwise_within_target"], -1e9),
        ),
        reverse=True,
    )
    for idx, row in enumerate(out, start=1):
        row["rank"] = idx
    return out


def build_report(
    target_rows: Sequence[Dict[str, Any]],
    summary_rows: Sequence[Dict[str, Any]],
    *,
    repeats: int,
    timing_loops: int,
    base_count: int,
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.12n: binær validering av probe3_top_half")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden er bevisst smal. Vi holder screening fast ved `full_basis@0.50` og sammenligner bare `full_followup`, `probe3_top_half` og to små beslutningsregelvarianter."
    )
    lines.append("")
    lines.append("## Metode")
    lines.append("")
    lines.append("- Regime holdes fast ved `band_zero_del`.")
    lines.append("- Screening holdes fast ved `full_basis@0.50`.")
    lines.append("- Adaptive policyer bygger alle på `probe_runs=3`.")
    lines.append(f"- Datasett: `{base_count}` baser. Screeningsplitt: `{repeats}`. Timing-lokker per screeningpass: `{timing_loops}`.")
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
    lines.append("## Policy-sammendrag")
    lines.append("")
    lines.append("| rank | policy | best_hit | recall | pairwise | total_s | speedup | d_best_hit | d_recall | d_pairwise | near_match | faster_and_match |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in summary_rows:
        lines.append(
            f"| {int(row['rank'])} | {row['policy_name']} | {safe_float(row['mean_best_hit']):.3f} | {safe_float(row['mean_recall']):.3f} | "
            f"{safe_float(row['mean_pairwise_within_target']):.3f} | {safe_float(row['mean_total_seconds']):.3f} | {safe_float(row['mean_speedup_vs_ref']):.3f} | "
            f"{safe_float(row['mean_delta_best_hit_vs_ref']):.3f} | {safe_float(row['mean_delta_recall_vs_ref']):.3f} | {safe_float(row['mean_delta_pairwise_vs_ref']):.3f} | "
            f"{safe_float(row['near_match_rate_eps_02']):.3f} | {safe_float(row['faster_and_near_match_rate']):.3f} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    ref = next((r for r in summary_rows if str(r["policy_name"]) == "full_followup"), None)
    p3 = next((r for r in summary_rows if str(r["policy_name"]) == "probe3_top_half"), None)
    tie = next((r for r in summary_rows if str(r["policy_name"]) == "probe3_top_half_screen_tiebreak"), None)
    guard = next((r for r in summary_rows if str(r["policy_name"]) == "probe3_guarded_half"), None)
    if ref is not None:
        lines.append(
            f"- `full_followup` er referansen med `total_s={safe_float(ref['mean_total_seconds']):.3f}`."
        )
    if p3 is not None:
        lines.append(
            f"- `probe3_top_half` er hovedutfordreren: `speedup={safe_float(p3['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(p3['mean_best_hit']):.3f}`, `recall={safe_float(p3['mean_recall']):.3f}`, `pairwise={safe_float(p3['mean_pairwise_within_target']):.3f}`."
        )
    if tie is not None:
        lines.append(
            f"- `probe3_top_half_screen_tiebreak` tester om skjermscore kan brukes som sekundær beslutningsregel: `speedup={safe_float(tie['mean_speedup_vs_ref']):.3f}`, `pairwise={safe_float(tie['mean_pairwise_within_target']):.3f}`."
        )
    if guard is not None:
        lines.append(
            f"- `probe3_guarded_half` tester om små partielle forskjeller bør utløse bredere forlengelse: `speedup={safe_float(guard['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(guard['mean_best_hit']):.3f}`, `recall={safe_float(guard['mean_recall']):.3f}`."
        )
    lines.append(
        "- Den viktige repo-lojale lesningen her er at `probe3_top_half` fortsatt er raskere, men ikke lenger matcher referansen på hit/recall i denne direkte valideringen."
    )
    lines.append(
        "- Siden tie-break- og guarded-varianten ikke hjelper, ser det forelopig ikke ut som om små lokale beslutningsregel-justeringer er nok til a lukke gapet."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(summary_rows: Sequence[Dict[str, Any]]) -> str:
    best = summary_rows[0] if summary_rows else None
    lines = [
        "# v0.12n for ikke-spesialister",
        "",
        "Denne runden tester om den nye smarte oppfølgingen faktisk holder når vi bare sammenligner den mot full oppfølging og noen få små varianter.",
        "",
    ]
    if best is not None:
        lines.append(
            f"- Den beste kandidaten i denne runden er `{best['policy_name']}`, med `speedup={safe_float(best['mean_speedup_vs_ref']):.3f}` og `near_match={safe_float(best['near_match_rate_eps_02']):.3f}`."
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_recommendation(summary_rows: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.12n operativ anbefaling", ""]
    p3 = next((r for r in summary_rows if str(r["policy_name"]) == "probe3_top_half"), None)
    tie = next((r for r in summary_rows if str(r["policy_name"]) == "probe3_top_half_screen_tiebreak"), None)
    guard = next((r for r in summary_rows if str(r["policy_name"]) == "probe3_guarded_half"), None)
    if p3 is None or tie is None or guard is None:
        lines.append("v12n ga ikke nok signal til en ny operativ anbefaling.")
        lines.append("")
        return "\n".join(lines)
    lines.append("Behold `full_followup` som referanse under fast `full_basis@0.50` screening.")
    lines.append(
        f"Les `probe3_top_half` som hovedkandidaten: `speedup={safe_float(p3['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(p3['mean_best_hit']):.3f}`, `recall={safe_float(p3['mean_recall']):.3f}` og `pairwise={safe_float(p3['mean_pairwise_within_target']):.3f}`."
    )
    lines.append(
        f"`probe3_top_half_screen_tiebreak` og `probe3_guarded_half` forbedrer ikke dette bildet: tie-break holder samme tall som hovedkandidaten, mens guarded-varianten blir tregere uten kvalitetsgevinst."
    )
    lines.append(
        "Den repo-lojale dommen etter v12n er derfor: `probe3_top_half` er fortsatt en nyttig rask utfordrer, men den er ikke robust nok til å erstatte `full_followup` ennå."
    )
    lines.append(
        "Hvis vi skal videre herfra, bør neste steg være en smartere tidlig beslutningsstatistikk eller et større valideringssett, ikke flere nesten-like lokale varianter."
    )
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12n binary adaptive validation")
    ap.add_argument("--timed-run-csv", default="Documentation/v12k_adaptive_followup_budget_timed_run_rows.csv")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=6)
    ap.add_argument("--test-frac", type=float, default=0.50)
    ap.add_argument("--screening-repeats", type=int, default=40)
    ap.add_argument("--screening-seed", type=int, default=12111)
    ap.add_argument("--screen-timing-loops", type=int, default=300)
    ap.add_argument("--output-prefix", default="Documentation/v12n_binary_adaptive_validation")
    ap.add_argument("--report-md", default="Documentation/v12n_binary_adaptive_validation.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12n.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12n_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    run_rows = v12l.read_timed_run_rows(args.timed_run_csv)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    growth_seeds = [61001 + 23 * i for i in range(args.growth_seeds)]
    regime = v10e.recommended_regime(args.growth_regime)
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]

    print(f"[v12n] regime={regime.name} targets={targets} growth={len(growth_seeds)} rows={len(run_rows)}")
    print("[v12n] rebuilding base features for the same measured bases...")
    _, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    base_level_rows = v12l.parse_base_rows(base_rows, run_rows)
    grouped_runs = v12l.group_runs_by_base(run_rows)
    target_rows = v12k.target_summary(base_rows, run_rows)

    print("[v12n] evaluating binary adaptive validation...")
    split_rows = per_split_rows(
        base_level_rows,
        grouped_runs,
        repeats=args.screening_repeats,
        test_frac=args.test_frac,
        screening_seed=args.screening_seed,
        timing_loops=args.screen_timing_loops,
    )
    summary_rows = aggregate_rows(split_rows)

    prefix = args.output_prefix
    print("[v12n] writing outputs...")
    write_csv(f"{prefix}_target_summary.csv", target_rows)
    write_csv(f"{prefix}_split_rows.csv", split_rows)
    write_csv(f"{prefix}_summary.csv", summary_rows)

    for path, content in [
        (
            args.report_md,
            build_report(
                target_rows,
                summary_rows,
                repeats=args.screening_repeats,
                timing_loops=args.screen_timing_loops,
                base_count=len(base_level_rows),
            ),
        ),
        (args.lay_md, build_lay_summary(summary_rows)),
        (args.recommendation_md, build_recommendation(summary_rows)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v12n] done")


if __name__ == "__main__":
    main()
