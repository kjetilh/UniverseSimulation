#!/usr/bin/env python3
"""v0.12i measured runtime pipeline on top of v0.12f-v0.12h.

This round replaces the abstract screen-cost knob from v0.12h with a direct
local timing model:

1. measure the actual screening-model wall-clock for each active policy on the
   same holdout task as v0.12f/v0.12g,
2. measure the actual wall-clock for a full follow-up bundle on the active
   band_zero_del dynamics at each target size,
3. combine them into a practical pipeline comparison.

This is still not "new physics". It is a workflow test that asks whether the
compact surrogates save real work on this machine and codepath.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12
import relational_universe_v12e_start_state_screening as v12e
import relational_universe_v12f_budget_screening as v12f


ANCHOR_REGIME = "band_zero_del"
REFERENCE_POLICY = "full_basis"
REFERENCE_BUDGET = 0.50
EPSILON = 0.02
PIPELINES: List[Tuple[str, float, Sequence[str]]] = [
    ("full_basis", 0.50, tuple(v12.BASIS_FEATURES)),
    ("spectral_only", 0.50, ("initial_spectral_per_sqrtN",)),
    ("spectral_plus_dim", 0.667, ("initial_spectral_per_sqrtN", "initial_dim_proxy")),
    ("random_baseline", 0.50, ()),
]


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v12.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v12.write_csv(path, rows)


def read_csv(path: str | Path) -> List[Dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fixed_candidate() -> v09.ScaleCandidate:
    return v09.ScaleCandidate(ANCHOR_REGIME, 0.02, 0.00, 0.02, 0.00, 0.00)


def parse_base_rows(path: str | Path) -> List[Dict[str, Any]]:
    rows = read_csv(path)
    out: List[Dict[str, Any]] = []
    int_keys = {"target_nodes", "growth_seed", "runs"}
    for row in rows:
        enriched: Dict[str, Any] = {}
        for key, value in row.items():
            if key in int_keys:
                enriched[key] = int(value)
            else:
                enriched[key] = safe_float(value, default=value)
        out.append(enriched)
    return out


def count_selected_by_target(rows: Sequence[Dict[str, Any]]) -> Dict[int, int]:
    out: Dict[int, int] = {}
    for row in rows:
        out[int(row["target_nodes"])] = out.get(int(row["target_nodes"]), 0) + 1
    return out


def measure_screening_seconds(
    train_rows: Sequence[Dict[str, Any]],
    test_rows: Sequence[Dict[str, Any]],
    policy_name: str,
    features: Sequence[str],
    budget_frac: float,
    *,
    seed: int,
    loops: int,
) -> float:
    # Warm-up once to avoid timing import/cache effects in the measured loop.
    warm_rng = random.Random(seed)
    scored = v12f.score_rows(train_rows, test_rows, policy_name, features, warm_rng)
    _ = v12f.select_within_target(scored, budget_frac)

    start = time.perf_counter()
    for _ in range(loops):
        loop_rng = random.Random(seed)
        scored = v12f.score_rows(train_rows, test_rows, policy_name, features, loop_rng)
        _ = v12f.select_within_target(scored, budget_frac)
    elapsed = time.perf_counter() - start
    return elapsed / max(1, loops)


def followup_timing_rows(
    ensembles: Sequence[v10b.CalibrationEnsemble],
    regime: Any,
    growth_seeds: Sequence[int],
    run_offsets: Sequence[int],
    *,
    timing_growth_samples: int,
    timing_repeats: int,
) -> List[Dict[str, Any]]:
    candidate = fixed_candidate()
    base_states, _ = v10e.build_bases(ensembles, regime, growth_seeds)
    name_hash = sum(ord(ch) for ch in candidate.name) % 997
    rows: List[Dict[str, Any]] = []
    for ens in ensembles:
        chosen_growth = list(growth_seeds[: max(1, timing_growth_samples)])
        for gseed in chosen_growth:
            base = base_states[(ens.name, int(gseed))]
            steps = v10e.steps_for_state(base.g.num_nodes())
            for rep in range(1, timing_repeats + 1):
                start = time.perf_counter()
                for off in run_offsets:
                    seed = int(gseed) + int(off) + name_hash
                    _ = v09.run_single_candidate_from_base(candidate, ens, base, seed=seed, steps=steps)
                elapsed = time.perf_counter() - start
                rows.append(
                    {
                        "target_nodes": int(ens.target_nodes),
                        "ensemble": ens.name,
                        "growth_seed": int(gseed),
                        "timing_repeat": rep,
                        "steps_per_run": int(steps),
                        "runs_in_bundle": len(run_offsets),
                        "bundle_seconds": elapsed,
                        "seconds_per_run": elapsed / max(1, len(run_offsets)),
                    }
                )
    return rows


def summarize_followup_timing(rows: Sequence[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[int, float]]:
    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in rows:
        by_target.setdefault(int(row["target_nodes"]), []).append(dict(row))

    out: List[Dict[str, Any]] = []
    bundle_lookup: Dict[int, float] = {}
    for target in sorted(by_target):
        sub = by_target[target]
        bundle_mean = mean_defined(safe_float(r["bundle_seconds"]) for r in sub)
        run_mean = mean_defined(safe_float(r["seconds_per_run"]) for r in sub)
        out.append(
            {
                "target_nodes": target,
                "samples": len(sub),
                "mean_bundle_seconds": bundle_mean,
                "mean_seconds_per_run": run_mean,
                "mean_steps_per_run": mean_defined(safe_float(r["steps_per_run"]) for r in sub),
                "q10_bundle_seconds": v10b.quantile([safe_float(r["bundle_seconds"]) for r in sub], 0.10),
                "q90_bundle_seconds": v10b.quantile([safe_float(r["bundle_seconds"]) for r in sub], 0.90),
            }
        )
        bundle_lookup[target] = bundle_mean
    return out, bundle_lookup


def pipeline_split_rows(
    base_level_rows: Sequence[Dict[str, Any]],
    *,
    repeats: int,
    test_frac: float,
    screening_seed: int,
    timing_loops: int,
    followup_bundle_seconds_by_target: Mapping[int, float],
) -> List[Dict[str, Any]]:
    master_rng = random.Random(screening_seed)
    rows: List[Dict[str, Any]] = []
    for split_id in range(1, repeats + 1):
        split_rng = random.Random(master_rng.randint(1, 10**9))
        train_idx, test_idx = v12e.stratified_holdout_indices(base_level_rows, split_rng, test_frac)
        train_rows = [dict(base_level_rows[i]) for i in train_idx]
        test_rows = [dict(base_level_rows[i]) for i in test_idx]

        per_policy: List[Dict[str, Any]] = []
        for policy_name, budget_frac, features in PIPELINES:
            policy_seed = split_rng.randint(1, 10**9)
            policy_rng = random.Random(policy_seed)
            scored = v12f.score_rows(train_rows, test_rows, policy_name, features, policy_rng)
            selected = v12f.select_within_target(scored, budget_frac)
            metrics = v12f.selection_metrics(selected, scored)
            by_target = count_selected_by_target(selected)
            followup_seconds = sum(
                count * safe_float(followup_bundle_seconds_by_target.get(target, float("nan")))
                for target, count in by_target.items()
            )
            screening_seconds = measure_screening_seconds(
                train_rows,
                test_rows,
                policy_name,
                features,
                budget_frac,
                seed=policy_seed,
                loops=timing_loops,
            )
            total_seconds = screening_seconds + followup_seconds
            per_policy.append(
                {
                    "split_id": split_id,
                    "policy_name": policy_name,
                    "budget_frac": budget_frac,
                    "feature_count": len(features),
                    "train_rows": len(train_rows),
                    "test_rows": len(test_rows),
                    "selected_rows": len(selected),
                    "screening_seconds": screening_seconds,
                    "followup_seconds": followup_seconds,
                    "total_seconds": total_seconds,
                    "selected_target_48": by_target.get(48, 0),
                    "selected_target_96": by_target.get(96, 0),
                    "selected_target_192": by_target.get(192, 0),
                    "selected_target_256": by_target.get(256, 0),
                    **metrics,
                }
            )

        ref = next(
            row
            for row in per_policy
            if str(row["policy_name"]) == REFERENCE_POLICY and abs(safe_float(row["budget_frac"]) - REFERENCE_BUDGET) <= 1e-9
        )
        ref_total = safe_float(ref["total_seconds"])
        ref_hit = safe_float(ref["within_target_best_hit"])
        ref_recall = safe_float(ref["within_target_top_quartile_recall"])

        for row in per_policy:
            row["delta_best_hit_vs_ref"] = safe_float(row["within_target_best_hit"]) - ref_hit
            row["delta_recall_vs_ref"] = safe_float(row["within_target_top_quartile_recall"]) - ref_recall
            row["time_delta_vs_ref"] = safe_float(row["total_seconds"]) - ref_total
            row["time_ratio_vs_ref"] = safe_float(row["total_seconds"]) / ref_total if ref_total > 1e-12 else float("nan")
            row["speedup_vs_ref"] = ref_total / safe_float(row["total_seconds"]) if safe_float(row["total_seconds"]) > 1e-12 else float("nan")
            near_match = (
                safe_float(row["within_target_best_hit"]) >= ref_hit - EPSILON
                and safe_float(row["within_target_top_quartile_recall"]) >= ref_recall - EPSILON
            )
            row["near_match_eps_02"] = 1 if near_match else 0
            row["faster_than_ref"] = 1 if safe_float(row["total_seconds"]) <= ref_total + 1e-12 else 0
            row["faster_and_near_match"] = 1 if near_match and row["faster_than_ref"] == 1 else 0
            rows.append(row)
    return rows


def aggregate_pipeline_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    keys = sorted({(str(r["policy_name"]), safe_float(r["budget_frac"])) for r in rows})
    out: List[Dict[str, Any]] = []
    for policy_name, budget_frac in keys:
        sub = [
            r
            for r in rows
            if str(r["policy_name"]) == policy_name and abs(safe_float(r["budget_frac"]) - budget_frac) <= 1e-9
        ]
        out.append(
            {
                "policy_name": policy_name,
                "budget_frac": budget_frac,
                "feature_count": int(sub[0]["feature_count"]) if sub else 0,
                "mean_screening_seconds": mean_defined(safe_float(r["screening_seconds"]) for r in sub),
                "mean_followup_seconds": mean_defined(safe_float(r["followup_seconds"]) for r in sub),
                "mean_total_seconds": mean_defined(safe_float(r["total_seconds"]) for r in sub),
                "mean_time_ratio_vs_ref": mean_defined(safe_float(r["time_ratio_vs_ref"]) for r in sub),
                "mean_speedup_vs_ref": mean_defined(safe_float(r["speedup_vs_ref"]) for r in sub),
                "mean_best_hit": mean_defined(safe_float(r["within_target_best_hit"]) for r in sub),
                "mean_recall": mean_defined(safe_float(r["within_target_top_quartile_recall"]) for r in sub),
                "mean_selected_lift": mean_defined(safe_float(r["within_target_selected_lift"]) for r in sub),
                "mean_delta_best_hit_vs_ref": mean_defined(safe_float(r["delta_best_hit_vs_ref"]) for r in sub),
                "mean_delta_recall_vs_ref": mean_defined(safe_float(r["delta_recall_vs_ref"]) for r in sub),
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
        ),
        reverse=True,
    )
    for idx, row in enumerate(out, start=1):
        row["rank"] = idx
    return out


def build_report(
    followup_summary_rows: Sequence[Dict[str, Any]],
    aggregate_rows: Sequence[Dict[str, Any]],
    *,
    repeats: int,
    timing_loops: int,
    timing_growth_samples: int,
    timing_repeats: int,
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.12i: målt arbeidsflyt-tid for screening og oppfølging")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden erstatter den abstrakte skjermkostnaden i v12h med direkte lokal måling. Sporsmalet er ikke lenger bare hvilken policy som ser billig ut i en modell, men hvilken som faktisk gir en raskere arbeidsflyt pa denne maskinen og denne kodebanen."
    )
    lines.append("")
    lines.append("## Metode")
    lines.append("")
    lines.append("- Samme arbeidsregime som v12f-v12h: `band_zero_del`.")
    lines.append("- Samme policyfamilie som aktiv arbeidslesning: `full_basis@0.50`, `spectral_only@0.50`, `spectral_plus_dim@0.667`, pluss `random_baseline@0.50` som diagnostisk kontroll.")
    lines.append("- Screeningtiden maales som virkelig veggklokketid for score+seleksjon pa de samme stratified holdout-splitt som v12f brukte.")
    lines.append("- Oppfolgingstiden maales som virkelig veggklokketid for en full dynamikk-bundle per valgt base, altsa alle run-seeds for den basen.")
    lines.append(
        "- Dette er fortsatt en arbeidsflyttest, ikke ny fysikk. Hvis en policy vinner her, betyr det at den ser ut til a gi en raskere praksis under dagens benchmarkoppsett."
    )
    lines.append(f"- Screening-splitt: `{repeats}`. Timing-lokker per screeningpass: `{timing_loops}`.")
    lines.append(
        f"- Oppfolgingstid kalibrert med `{timing_growth_samples}` growth-baser per størrelse og `{timing_repeats}` repeats per bundle."
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
            f"{safe_float(row['faster_and_near_match_rate']):.3f} | {safe_float(row['screen_share_of_total']):.3f} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    ref = next(
        (r for r in aggregate_rows if str(r["policy_name"]) == REFERENCE_POLICY and abs(safe_float(r["budget_frac"]) - REFERENCE_BUDGET) <= 1e-9),
        None,
    )
    spectral_same = next(
        (r for r in aggregate_rows if str(r["policy_name"]) == "spectral_only" and abs(safe_float(r["budget_frac"]) - 0.50) <= 1e-9),
        None,
    )
    spectral_dim = next(
        (r for r in aggregate_rows if str(r["policy_name"]) == "spectral_plus_dim" and abs(safe_float(r["budget_frac"]) - 0.667) <= 1e-6),
        None,
    )
    if ref is not None:
        lines.append(
            f"- Referansen `full_basis@0.50` bruker i snitt `{safe_float(ref['mean_total_seconds']):.4f}` sekunder per split i denne lokale modellen."
        )
        lines.append(
            f"- Screeningdelen utgjor bare `{safe_float(ref['screen_share_of_total']):.3f}` av totalen for referansen. Det forteller hvor mye av arbeidsflyten som faktisk styres av oppfolgingsdynamikken."
        )
    if spectral_same is not None:
        lines.append(
            f"- `spectral_only@0.50` er same-budget-kandidaten: `speedup_vs_ref={safe_float(spectral_same['mean_speedup_vs_ref']):.3f}`, `near_match={safe_float(spectral_same['near_match_rate_eps_02']):.3f}` og `faster_and_match={safe_float(spectral_same['faster_and_near_match_rate']):.3f}`."
        )
    if spectral_dim is not None:
        lines.append(
            f"- `spectral_plus_dim@0.667` er den dyrere kompakte utfordreren: `speedup_vs_ref={safe_float(spectral_dim['mean_speedup_vs_ref']):.3f}`, `near_match={safe_float(spectral_dim['near_match_rate_eps_02']):.3f}` og `faster_and_match={safe_float(spectral_dim['faster_and_near_match_rate']):.3f}`."
        )
    lines.append(
        "- Dette skal leses som en praktisk arbeidsdom. Hvis de kompakte policyene ikke blir raskere her, er det et tegn pa at de forelopig gir en ryddigere beskrivelse mer enn en faktisk spart arbeidsflyt."
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
        "# v0.12i for ikke-spesialister",
        "",
        "Denne runden spør om den enklere geometriregelen faktisk sparer tid i praksis, ikke bare ser pen ut i tabeller.",
        "",
    ]
    if ref is not None:
        lines.append(f"- Referansen er fortsatt `full_basis@0.50`, med omtrent `{safe_float(ref['mean_total_seconds']):.4f}` sekunder per split i denne lokale målingen.")
    if same_budget is not None:
        lines.append(
            f"- Den enkleste kandidaten er `spectral_only@0.50`, med `speedup_vs_ref={safe_float(same_budget['mean_speedup_vs_ref']):.3f}` og `near_match={safe_float(same_budget['near_match_rate_eps_02']):.3f}`."
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_recommendation(aggregate_rows: Sequence[Dict[str, Any]]) -> str:
    ref = next(
        (r for r in aggregate_rows if str(r["policy_name"]) == "full_basis" and abs(safe_float(r["budget_frac"]) - 0.50) <= 1e-9),
        None,
    )
    spectral_same = next(
        (r for r in aggregate_rows if str(r["policy_name"]) == "spectral_only" and abs(safe_float(r["budget_frac"]) - 0.50) <= 1e-9),
        None,
    )
    spectral_dim = next(
        (r for r in aggregate_rows if str(r["policy_name"]) == "spectral_plus_dim" and abs(safe_float(r["budget_frac"]) - 0.667) <= 1e-6),
        None,
    )
    lines = ["# v0.12i operativ anbefaling", ""]
    if ref is None:
        lines.append("v12i ga ikke nok signal til en ny operativ anbefaling.")
        lines.append("")
        return "\n".join(lines)
    lines.append(
        "Behold `full_basis@0.50` som operativ arbeidsbenchmark til en kompakt policy faktisk viser bedre eller lik kvalitet med maelt raskere total arbeidsflyt."
    )
    if spectral_same is not None:
        lines.append(
            f"Behold `spectral_only@0.50` som den viktigste enkle kandidaten. Den er fortsatt den naturlige same-budget-sammenlikningen, med `speedup_vs_ref={safe_float(spectral_same['mean_speedup_vs_ref']):.3f}` og `near_match={safe_float(spectral_same['near_match_rate_eps_02']):.3f}`."
        )
    if spectral_dim is not None:
        lines.append(
            f"Behold `spectral_plus_dim@0.667` som kostnadssensitiv utfordrer bare hvis den maelte workflow-raten faktisk er konkurransedyktig. I denne runden er `speedup_vs_ref={safe_float(spectral_dim['mean_speedup_vs_ref']):.3f}` og `near_match={safe_float(spectral_dim['near_match_rate_eps_02']):.3f}`."
        )
    lines.append(
        "Neste naturlige steg etter v12i er en liten størrelses-stresstest: sjekk om denne arbeidsdommen holder når vi flytter samme pipeline litt opp i startstørrelse, ikke ved ny frontier-tuning."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12i measured runtime pipeline")
    ap.add_argument("--base-level-csv", default="Documentation/v12f_budget_base_rows.csv")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=12)
    ap.add_argument("--run-seeds", type=int, default=6)
    ap.add_argument("--screening-repeats", type=int, default=60)
    ap.add_argument("--test-frac", type=float, default=0.50)
    ap.add_argument("--screening-seed", type=int, default=12061)
    ap.add_argument("--screen-timing-loops", type=int, default=300)
    ap.add_argument("--timing-growth-samples", type=int, default=3)
    ap.add_argument("--timing-repeats", type=int, default=2)
    ap.add_argument("--output-prefix", default="Documentation/v12i_measured_runtime_pipeline")
    ap.add_argument("--report-md", default="Documentation/v12i_measured_runtime_pipeline.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12i.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12i_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    base_level_rows = parse_base_rows(args.base_level_csv)

    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    growth_seeds = [41001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [22101 + 31 * i for i in range(args.run_seeds)]

    print(
        f"[v12i] targets={targets} base_rows={len(base_level_rows)} "
        f"screen_splits={args.screening_repeats} timing_growth_samples={args.timing_growth_samples}"
    )
    print("[v12i] measuring follow-up bundles...")
    followup_rows = followup_timing_rows(
        ensembles,
        regime,
        growth_seeds,
        run_offsets,
        timing_growth_samples=args.timing_growth_samples,
        timing_repeats=args.timing_repeats,
    )
    followup_summary_rows, followup_lookup = summarize_followup_timing(followup_rows)
    print("[v12i] follow-up timing done")

    print("[v12i] evaluating measured pipeline...")
    split_rows = pipeline_split_rows(
        base_level_rows,
        repeats=args.screening_repeats,
        test_frac=args.test_frac,
        screening_seed=args.screening_seed,
        timing_loops=args.screen_timing_loops,
        followup_bundle_seconds_by_target=followup_lookup,
    )
    aggregate_rows = aggregate_pipeline_rows(split_rows)
    print("[v12i] writing outputs...")

    prefix = args.output_prefix
    write_csv(f"{prefix}_followup_timing_rows.csv", followup_rows)
    write_csv(f"{prefix}_followup_timing_summary.csv", followup_summary_rows)
    write_csv(f"{prefix}_split_rows.csv", split_rows)
    write_csv(f"{prefix}_summary.csv", aggregate_rows)

    for path, content in [
        (
            args.report_md,
            build_report(
                followup_summary_rows,
                aggregate_rows,
                repeats=args.screening_repeats,
                timing_loops=args.screen_timing_loops,
                timing_growth_samples=args.timing_growth_samples,
                timing_repeats=args.timing_repeats,
            ),
        ),
        (args.lay_md, build_lay_summary(aggregate_rows)),
        (args.recommendation_md, build_recommendation(aggregate_rows)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v12i] done")


if __name__ == "__main__":
    main()
