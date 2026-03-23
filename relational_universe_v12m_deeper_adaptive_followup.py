#!/usr/bin/env python3
"""v0.12m deeper adaptive follow-up under fixed full_basis screening.

This round follows v0.12l. The screening side is frozen at the current
reference workflow: `full_basis@0.50`. The only thing that changes is the
adaptive follow-up policy used on the screened bases.

The question is narrow and practical:
can a slightly deeper adaptive policy recover enough quality to become a better
time/quality challenger than `probe2_top_half`?
"""
from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12
import relational_universe_v12e_start_state_screening as v12e
import relational_universe_v12f_budget_screening as v12f
import relational_universe_v12i_measured_runtime_pipeline as v12i
import relational_universe_v12l_hybrid_screening_followup as v12l
import relational_universe_v12k_adaptive_followup_budget as v12k


REFERENCE_POLICY = "full_followup"
SCREEN_POLICY_NAME = "full_basis"
SCREEN_FEATURES = tuple(v12.BASIS_FEATURES)
SCREEN_BUDGET = 0.50
EPSILON = 0.02
FOLLOWUP_POLICIES: List[Tuple[str, int, float]] = [
    ("full_followup", 6, 1.0),
    ("probe2_top_half", 2, 0.50),
    ("probe3_top_half", 3, 0.50),
    ("probe4_top_half", 4, 0.50),
    ("probe2_top_two_thirds", 2, 0.6666667),
    ("probe3_top_two_thirds", 3, 0.6666667),
]


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v12.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v12.write_csv(path, rows)


def per_split_rows(
    base_level_rows: Sequence[Dict[str, Any]],
    grouped_runs: Dict[Tuple[int, str, int], List[Dict[str, Any]]],
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
        for policy_name, probe_runs, extend_frac in FOLLOWUP_POLICIES:
            evaluated = v12l.apply_followup_policy(selected, grouped_runs, probe_runs, extend_frac)
            metrics = v12l.hybrid_metrics(test_rows, evaluated)
            total_seconds = screening_seconds + safe_float(metrics["used_seconds"])
            per_policy.append(
                {
                    "split_id": split_id,
                    "followup_policy_name": policy_name,
                    "screen_policy_name": SCREEN_POLICY_NAME,
                    "budget_frac": SCREEN_BUDGET,
                    "feature_count": len(SCREEN_FEATURES),
                    "probe_runs": probe_runs,
                    "extend_frac": extend_frac,
                    "train_rows": len(train_rows),
                    "test_rows": len(test_rows),
                    "screening_seconds": screening_seconds,
                    "followup_seconds": safe_float(metrics["used_seconds"]),
                    "total_seconds": total_seconds,
                    **metrics,
                }
            )

        ref = next(r for r in per_policy if str(r["followup_policy_name"]) == REFERENCE_POLICY)
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
    keys = [name for name, _, _ in FOLLOWUP_POLICIES]
    out: List[Dict[str, Any]] = []
    for policy_name in keys:
        sub = [r for r in rows if str(r["followup_policy_name"]) == policy_name]
        exemplar = sub[0]
        out.append(
            {
                "followup_policy_name": policy_name,
                "screen_policy_name": exemplar["screen_policy_name"],
                "budget_frac": safe_float(exemplar["budget_frac"]),
                "feature_count": int(exemplar["feature_count"]),
                "probe_runs": int(exemplar["probe_runs"]),
                "extend_frac": safe_float(exemplar["extend_frac"]),
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
                "screen_share_of_total": mean_defined(
                    safe_float(r["screening_seconds"]) / safe_float(r["total_seconds"])
                    if safe_float(r["total_seconds"]) > 1e-12
                    else float("nan")
                    for r in sub
                ),
            }
        )
    out.sort(
        key=lambda row: (
            safe_float(row["faster_and_near_match_rate"], -1e9),
            safe_float(row["near_match_rate_eps_02"], -1e9),
            safe_float(row["mean_speedup_vs_ref"], -1e9),
            safe_float(row["mean_best_hit"], -1e9),
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
    lines.append("# Relasjonell universgraf v0.12m: dypere adaptiv oppfølging under fast screening")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden holder screeningdelen fast ved `full_basis@0.50` og tester bare en dypere familie av adaptive oppfolgingspolicyer. Maalet er a se om vi kan komme naermere referansen uten a gi fra oss hele tidsgevinsten."
    )
    lines.append("")
    lines.append("## Metode")
    lines.append("")
    lines.append("- Regime holdes fast ved `band_zero_del`.")
    lines.append("- Screening holdes fast ved `full_basis@0.50`.")
    lines.append("- Bare adaptive follow-up-policyer varieres.")
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
    lines.append("## Adaptive policy-sammendrag under fast screening")
    lines.append("")
    lines.append("| rank | policy | probe_runs | extend_frac | best_hit | recall | pairwise | total_s | speedup | d_best_hit | d_recall | near_match | faster_and_match |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in summary_rows:
        lines.append(
            f"| {int(row['rank'])} | {row['followup_policy_name']} | {int(row['probe_runs'])} | {safe_float(row['extend_frac']):.3f} | "
            f"{safe_float(row['mean_best_hit']):.3f} | {safe_float(row['mean_recall']):.3f} | {safe_float(row['mean_pairwise_within_target']):.3f} | "
            f"{safe_float(row['mean_total_seconds']):.3f} | {safe_float(row['mean_speedup_vs_ref']):.3f} | {safe_float(row['mean_delta_best_hit_vs_ref']):.3f} | "
            f"{safe_float(row['mean_delta_recall_vs_ref']):.3f} | {safe_float(row['near_match_rate_eps_02']):.3f} | {safe_float(row['faster_and_near_match_rate']):.3f} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    ref = next((r for r in summary_rows if str(r["followup_policy_name"]) == REFERENCE_POLICY), None)
    p2h = next((r for r in summary_rows if str(r["followup_policy_name"]) == "probe2_top_half"), None)
    p3h = next((r for r in summary_rows if str(r["followup_policy_name"]) == "probe3_top_half"), None)
    p2t = next((r for r in summary_rows if str(r["followup_policy_name"]) == "probe2_top_two_thirds"), None)
    p3t = next((r for r in summary_rows if str(r["followup_policy_name"]) == "probe3_top_two_thirds"), None)
    if ref is not None:
        lines.append(
            f"- Referansen `full_followup` bruker `{safe_float(ref['mean_total_seconds']):.3f}` sekunder og setter nullpunktet for hit/recall."
        )
    if p2h is not None:
        lines.append(
            f"- `probe2_top_half` er arven fra `v12k`/`v12l`: `speedup={safe_float(p2h['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(p2h['mean_best_hit']):.3f}`, `recall={safe_float(p2h['mean_recall']):.3f}`."
        )
    if p3h is not None:
        lines.append(
            f"- `probe3_top_half` tester mer informasjon per base uten a utvide feltet: `speedup={safe_float(p3h['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(p3h['mean_best_hit']):.3f}`, `recall={safe_float(p3h['mean_recall']):.3f}`."
        )
    if p2t is not None:
        lines.append(
            f"- `probe2_top_two_thirds` tester bredere adaptiv oppfolging: `speedup={safe_float(p2t['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(p2t['mean_best_hit']):.3f}`, `recall={safe_float(p2t['mean_recall']):.3f}`."
        )
    if p3t is not None:
        lines.append(
            f"- `probe3_top_two_thirds` er den mest informative adaptive utfordreren i denne familien: `speedup={safe_float(p3t['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(p3t['mean_best_hit']):.3f}`, `recall={safe_float(p3t['mean_recall']):.3f}`."
        )
    lines.append(
        "- `probe2_top_two_thirds` og `probe3_top_two_thirds` kollapser i praksis til `full_followup` i denne settingen, fordi `0.667` med bare to screenede baser per størrelse betyr at begge blir forlenget. De er derfor nyttige som metodisk kontroll, ikke som ekte adaptive vinnere."
    )
    lines.append(
        "- Den viktigste nye lesningen er at `probe3_top_half` faktisk matcher referansen på mean `best_hit` og `recall`, samtidig som den er klart raskere. Pairwise er fortsatt litt svakere, så dette er den første sterke adaptive utfordreren, ikke en endelig ny standard."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(summary_rows: Sequence[Dict[str, Any]]) -> str:
    best = summary_rows[0] if summary_rows else None
    lines = [
        "# v0.12m for ikke-spesialister",
        "",
        "Denne runden spør om vi kan gjøre den smarte oppfølgingen litt mer informert, uten å gå helt tilbake til full kostnad.",
        "",
    ]
    if best is not None:
        lines.append(
            f"- Den beste adaptive kandidaten i denne runden er `{best['followup_policy_name']}`, med `speedup={safe_float(best['mean_speedup_vs_ref']):.3f}` og `near_match={safe_float(best['near_match_rate_eps_02']):.3f}`."
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_recommendation(summary_rows: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.12m operativ anbefaling", ""]
    ref = next((r for r in summary_rows if str(r["followup_policy_name"]) == REFERENCE_POLICY), None)
    p2h = next((r for r in summary_rows if str(r["followup_policy_name"]) == "probe2_top_half"), None)
    best_nonref = next((r for r in summary_rows if str(r["followup_policy_name"]) != REFERENCE_POLICY), None)
    if ref is None or p2h is None or best_nonref is None:
        lines.append("v12m ga ikke nok signal til en ny operativ anbefaling.")
        lines.append("")
        return "\n".join(lines)
    lines.append("Behold `full_followup` som referanse under fast `full_basis@0.50` screening.")
    lines.append(
        f"Bruk `probe2_top_half` som baseline for adaptiv kvalitet/tid fra v12k-v12l: `speedup={safe_float(p2h['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(p2h['mean_best_hit']):.3f}`, `recall={safe_float(p2h['mean_recall']):.3f}`."
    )
    lines.append(
        f"Beste dypere utfordrer i denne runden er `{best_nonref['followup_policy_name']}`, med `speedup={safe_float(best_nonref['mean_speedup_vs_ref']):.3f}`, `best_hit={safe_float(best_nonref['mean_best_hit']):.3f}` og `recall={safe_float(best_nonref['mean_recall']):.3f}`."
    )
    lines.append(
        "Les `probe3_top_half` som den første seriøse adaptive utfordreren: den matcher referansen på mean hit/recall og er fortsatt raskere. Det som gjenstår å avklare er om den lille pairwise-svikten er akseptabel eller kan rettes med en smartere beslutningsregel."
    )
    lines.append(
        "Neste smale steg bør derfor være en valideringsrunde som bare sammenligner `full_followup` mot `probe3_top_half`, og eventuelt en liten variant med bedre tie-break eller forlengelsesregel."
    )
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12m deeper adaptive follow-up")
    ap.add_argument("--timed-run-csv", default="Documentation/v12k_adaptive_followup_budget_timed_run_rows.csv")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=6)
    ap.add_argument("--test-frac", type=float, default=0.50)
    ap.add_argument("--screening-repeats", type=int, default=40)
    ap.add_argument("--screening-seed", type=int, default=12101)
    ap.add_argument("--screen-timing-loops", type=int, default=300)
    ap.add_argument("--output-prefix", default="Documentation/v12m_deeper_adaptive_followup")
    ap.add_argument("--report-md", default="Documentation/v12m_deeper_adaptive_followup.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12m.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12m_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    run_rows = v12l.read_timed_run_rows(args.timed_run_csv)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    growth_seeds = [61001 + 23 * i for i in range(args.growth_seeds)]
    regime = v10e.recommended_regime(args.growth_regime)
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]

    print(f"[v12m] regime={regime.name} targets={targets} growth={len(growth_seeds)} rows={len(run_rows)}")
    print("[v12m] rebuilding base features for the same measured bases...")
    _, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    base_level_rows = v12l.parse_base_rows(base_rows, run_rows)
    grouped_runs = v12l.group_runs_by_base(run_rows)
    target_rows = v12k.target_summary(base_rows, run_rows)

    print("[v12m] evaluating deeper adaptive policies...")
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
    print("[v12m] writing outputs...")
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
    print("[v12m] done")


if __name__ == "__main__":
    main()
