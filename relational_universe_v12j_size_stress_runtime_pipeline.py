#!/usr/bin/env python3
"""v0.12j modest size-stress test for the measured runtime pipeline.

This step asks whether the v0.12i workflow reading is just a small-graph fact,
or whether it still holds when we move to somewhat larger natural start
ensembles under the same active regime and same compact-policy comparison.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12
import relational_universe_v12e_start_state_screening as v12e
import relational_universe_v12f_budget_screening as v12f
import relational_universe_v12i_measured_runtime_pipeline as v12i


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v12.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v12.write_csv(path, rows)


def build_target_summary(base_rows: Sequence[Dict[str, Any]], base_level_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return v12f.target_summary(base_rows, base_level_rows)


def build_report(
    target_rows: Sequence[Dict[str, Any]],
    followup_summary_rows: Sequence[Dict[str, Any]],
    aggregate_rows: Sequence[Dict[str, Any]],
    *,
    base_count: int,
    run_count: int,
    repeats: int,
    timing_loops: int,
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.12j: moderat størrelses-stresstest av målt runtime-pipeline")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester om v12i-lesningen holder nar vi flytter den samme arbeidsflyten opp til noe storre naturlige ensembler. Maalet er ikke ny frontier eller ny modell, men a se om screeningdelen blir mer relevant eller om oppfolging fortsatt dominerer."
    )
    lines.append("")
    lines.append("## Metode")
    lines.append("")
    lines.append("- Samme arbeidsregime: `band_zero_del`.")
    lines.append("- Samme policyfamilie: `full_basis@0.50`, `spectral_only@0.50`, `spectral_plus_dim@0.667`, pluss `random_baseline@0.50`.")
    lines.append("- Samme type måling som v12i: virkelig screeningtid og virkelig oppfolgingstid på lokal kodebane.")
    lines.append(f"- Datasett: `{base_count}` baser og `{run_count}` underliggende runs i denne storrelsesrunden.")
    lines.append(f"- Screening-splitt: `{repeats}`. Timing-lokker per screeningpass: `{timing_loops}`.")
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
    lines.append("## Målt oppfølgingstid per størrelse")
    lines.append("")
    lines.append("| target | samples | mean_bundle_seconds | mean_seconds_per_run | mean_steps_per_run | q10_bundle | q90_bundle |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in followup_summary_rows:
        lines.append(
            f"| {int(row['target_nodes'])} | {int(row['samples'])} | {safe_float(row['mean_bundle_seconds']):.4f} | "
            f"{safe_float(row['mean_seconds_per_run']):.4f} | {safe_float(row['mean_steps_per_run']):.1f} | "
            f"{safe_float(row['q10_bundle_seconds']):.4f} | {safe_float(row['q90_bundle_seconds']):.4f} |"
        )
    lines.append("")
    lines.append("## Målt pipeline-sammendrag")
    lines.append("")
    lines.append("| rank | policy | budget | total_s | speedup_vs_ref | best_hit | recall | d_best_hit | d_recall | near_match | faster | faster_and_match | screen_share |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate_rows:
        lines.append(
            f"| {int(row['rank'])} | {row['policy_name']} | {safe_float(row['budget_frac']):.3f} | {safe_float(row['mean_total_seconds']):.4f} | "
            f"{safe_float(row['mean_speedup_vs_ref']):.3f} | {safe_float(row['mean_best_hit']):.3f} | {safe_float(row['mean_recall']):.3f} | "
            f"{safe_float(row['mean_delta_best_hit_vs_ref']):.3f} | {safe_float(row['mean_delta_recall_vs_ref']):.3f} | "
            f"{safe_float(row['near_match_rate_eps_02']):.3f} | {safe_float(row['faster_than_ref_rate']):.3f} | "
            f"{safe_float(row['faster_and_near_match_rate']):.3f} | {safe_float(row['screen_share_of_total']):.6f} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    ref = next(
        (r for r in aggregate_rows if str(r["policy_name"]) == "full_basis" and abs(safe_float(r["budget_frac"]) - 0.50) <= 1e-9),
        None,
    )
    same_budget = next(
        (r for r in aggregate_rows if str(r["policy_name"]) == "spectral_only" and abs(safe_float(r["budget_frac"]) - 0.50) <= 1e-9),
        None,
    )
    cost_sens = next(
        (r for r in aggregate_rows if str(r["policy_name"]) == "spectral_plus_dim" and abs(safe_float(r["budget_frac"]) - 0.667) <= 1e-6),
        None,
    )
    if ref is not None:
        lines.append(
            f"- Referansen `full_basis@0.50` bruker `{safe_float(ref['mean_total_seconds']):.4f}` sekunder per split, og screeningdelen utgjor bare `{safe_float(ref['screen_share_of_total']):.6f}` av totalen."
        )
    if same_budget is not None:
        lines.append(
            f"- `spectral_only@0.50` gir `speedup_vs_ref={safe_float(same_budget['mean_speedup_vs_ref']):.3f}` og `near_match={safe_float(same_budget['near_match_rate_eps_02']):.3f}`."
        )
    if cost_sens is not None:
        lines.append(
            f"- `spectral_plus_dim@0.667` gir `speedup_vs_ref={safe_float(cost_sens['mean_speedup_vs_ref']):.3f}` og `near_match={safe_float(cost_sens['near_match_rate_eps_02']):.3f}`."
        )
    lines.append(
        "- Denne runden skal leses som en størrelses-stresstest av v12i. Hvis screeningandelen fortsatt er naer null, betyr det at den praktiske flaskehalsen fortsatt ligger i oppfolgingen, ikke i valg av enkel screeningbasis."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(aggregate_rows: Sequence[Dict[str, Any]]) -> str:
    ref = next(
        (r for r in aggregate_rows if str(r["policy_name"]) == "full_basis" and abs(safe_float(r["budget_frac"]) - 0.50) <= 1e-9),
        None,
    )
    same_budget = next(
        (r for r in aggregate_rows if str(r["policy_name"]) == "spectral_only" and abs(safe_float(r["budget_frac"]) - 0.50) <= 1e-9),
        None,
    )
    lines = [
        "# v0.12j for ikke-spesialister",
        "",
        "Denne runden sjekker om den samme praktiske dommen fortsatt holder nar vi flytter arbeidsflyten til noe storre grafer.",
        "",
    ]
    if ref is not None:
        lines.append(
            f"- Referansen `full_basis@0.50` bruker omtrent `{safe_float(ref['mean_total_seconds']):.4f}` sekunder per split i denne storrelsesrunden."
        )
    if same_budget is not None:
        lines.append(
            f"- `spectral_only@0.50` er fortsatt den enkleste kandidaten, men i denne større runden er `near_match={safe_float(same_budget['near_match_rate_eps_02']):.3f}` og kvaliteten er svakere enn referansen."
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_recommendation(aggregate_rows: Sequence[Dict[str, Any]]) -> str:
    ref = next(
        (r for r in aggregate_rows if str(r["policy_name"]) == "full_basis" and abs(safe_float(r["budget_frac"]) - 0.50) <= 1e-9),
        None,
    )
    same_budget = next(
        (r for r in aggregate_rows if str(r["policy_name"]) == "spectral_only" and abs(safe_float(r["budget_frac"]) - 0.50) <= 1e-9),
        None,
    )
    lines = ["# v0.12j operativ anbefaling", ""]
    if ref is None:
        lines.append("v12j ga ikke nok signal til en ny operativ anbefaling.")
        lines.append("")
        return "\n".join(lines)
    lines.append(
        "Behold `full_basis@0.50` som arbeidsbenchmark til en kompakt policy viser maelt bedre eller lik kvalitet med raskere total arbeidsflyt ogsa under litt storre grafer."
    )
    if same_budget is not None:
        lines.append(
            f"Ikke behandle `spectral_only@0.50` som ny arbeidsvinner i denne større runden. Den er fortsatt nyttig som enkel kontroll, men her taper den kvalitetsmessig mot referansen med `near_match={safe_float(same_budget['near_match_rate_eps_02']):.3f}`."
        )
    lines.append(
        "Neste naturlige steg etter v12j er ikke frontier-tuning, men enten en litt storre workflow-runde eller en direkte analyse av om oppfolgingsbudsjettet kan kortes ned smartere enn ved ren pre-screening."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12j modest size-stress runtime pipeline")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="96,192,320,384")
    ap.add_argument("--growth-seeds", type=int, default=6)
    ap.add_argument("--run-seeds", type=int, default=4)
    ap.add_argument("--screening-repeats", type=int, default=30)
    ap.add_argument("--test-frac", type=float, default=0.50)
    ap.add_argument("--screening-seed", type=int, default=12191)
    ap.add_argument("--screen-timing-loops", type=int, default=150)
    ap.add_argument("--timing-growth-samples", type=int, default=2)
    ap.add_argument("--timing-repeats", type=int, default=2)
    ap.add_argument("--output-prefix", default="Documentation/v12j_size_stress_runtime_pipeline")
    ap.add_argument("--report-md", default="Documentation/v12j_size_stress_runtime_pipeline.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12j.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12j_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    candidate = v12f.fixed_candidate()
    growth_seeds = [51001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [32101 + 31 * i for i in range(args.run_seeds)]

    print(f"[v12j] regime={regime.name} targets={targets} growth={len(growth_seeds)} runs={len(run_offsets)}")
    print("[v12j] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    print("[v12j] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows([candidate], ensembles, base_states, growth_seeds, run_offsets, regime.name)
    base_level_rows = v12e.build_base_level_rows(base_rows, raw_run_rows)
    target_rows = build_target_summary(base_rows, base_level_rows)

    print("[v12j] measuring follow-up bundles...")
    followup_rows = v12i.followup_timing_rows(
        ensembles,
        regime,
        growth_seeds,
        run_offsets,
        timing_growth_samples=args.timing_growth_samples,
        timing_repeats=args.timing_repeats,
    )
    followup_summary_rows, followup_lookup = v12i.summarize_followup_timing(followup_rows)

    print("[v12j] evaluating pipeline...")
    split_rows = v12i.pipeline_split_rows(
        base_level_rows,
        repeats=args.screening_repeats,
        test_frac=args.test_frac,
        screening_seed=args.screening_seed,
        timing_loops=args.screen_timing_loops,
        followup_bundle_seconds_by_target=followup_lookup,
    )
    aggregate_rows = v12i.aggregate_pipeline_rows(split_rows)

    prefix = args.output_prefix
    print("[v12j] writing outputs...")
    write_csv(f"{prefix}_target_summary.csv", target_rows)
    write_csv(f"{prefix}_followup_timing_rows.csv", followup_rows)
    write_csv(f"{prefix}_followup_timing_summary.csv", followup_summary_rows)
    write_csv(f"{prefix}_split_rows.csv", split_rows)
    write_csv(f"{prefix}_summary.csv", aggregate_rows)

    for path, content in [
        (
            args.report_md,
            build_report(
                target_rows,
                followup_summary_rows,
                aggregate_rows,
                base_count=len(base_level_rows),
                run_count=len(raw_run_rows),
                repeats=args.screening_repeats,
                timing_loops=args.screen_timing_loops,
            ),
        ),
        (args.lay_md, build_lay_summary(aggregate_rows)),
        (args.recommendation_md, build_recommendation(aggregate_rows)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v12j] done")


if __name__ == "__main__":
    main()
