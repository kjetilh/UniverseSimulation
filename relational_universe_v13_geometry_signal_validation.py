#!/usr/bin/env python3
"""v0.13 geometry signal validation around the frozen band_zero_del regime.

This round follows the v0.12-v0.12n structure and workflow phase. The goal is
not to tune another screening policy. The goal is to answer a narrower question:

Which geometry / quasi-invariant signals are strong enough to justify a larger
validation set, and which are still too weak, too local, or too artifact-like
to scale up yet?
"""
from __future__ import annotations

import argparse
import itertools
import math
import random
import statistics
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12
import relational_universe_v12e_start_state_screening as v12e


STABILITY_FEATURES = [
    "initial_avg_degree",
    "initial_beta1_per_node",
    "initial_triangles_per_node",
    "initial_spectral_per_sqrtN",
    "initial_dim_proxy",
    "initial_clustering",
]

DRIFT_METRICS = [
    "mean_abs_delta_tokens_rel",
    "mean_abs_delta_nodes_rel",
    "mean_abs_delta_beta1_rel",
    "mean_abs_delta_triangles_rel",
    "mean_abs_delta_spectral_radius_rel",
    "mean_abs_delta_dim_proxy_rel",
    "mean_abs_delta_clustering_rel",
]

PREDICTION_TARGETS = [
    "mean_final_radius_control",
    "mean_avg_local_overlap",
]

BASIS_SPECS = [
    ("avg_degree_only", ("initial_avg_degree",)),
    ("spectral_only", ("initial_spectral_per_sqrtN",)),
    ("dim_only", ("initial_dim_proxy",)),
    ("spectral_plus_dim", ("initial_spectral_per_sqrtN", "initial_dim_proxy")),
    ("spectral_plus_clustering", ("initial_spectral_per_sqrtN", "initial_clustering")),
    ("full_basis", tuple(v12.BASIS_FEATURES)),
]


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v12.mean_defined(values)


def quantile(values: Sequence[float], q: float) -> float:
    return v10b.quantile(values, q)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v12.write_csv(path, rows)


def fixed_candidate() -> v09.ScaleCandidate:
    return v09.ScaleCandidate("band_zero_del", 0.02, 0.00, 0.02, 0.00, 0.00)


def grouped_base_level_rows(
    base_rows: Sequence[Dict[str, Any]],
    run_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    base_lookup = {(str(r["ensemble"]), int(r["growth_seed"])): dict(r) for r in base_rows}
    by_key: Dict[Tuple[str, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        by_key.setdefault((str(row["ensemble"]), int(row["growth_seed"])), []).append(dict(row))

    out: List[Dict[str, Any]] = []
    for (ensemble, growth_seed), sub in sorted(by_key.items()):
        base = base_lookup[(ensemble, growth_seed)]
        row: Dict[str, Any] = {
            "ensemble": ensemble,
            "target_nodes": int(base["target_nodes"]),
            "growth_seed": int(growth_seed),
            "runs": len(sub),
            "mean_final_radius_control": mean_defined(safe_float(r["final_radius_control"]) for r in sub),
            "mean_avg_local_overlap": mean_defined(safe_float(r["avg_local_overlap"]) for r in sub),
            "mean_fit_speed_control": mean_defined(safe_float(r["fit_speed_control"]) for r in sub),
            "mean_avg_same_descriptor": mean_defined(safe_float(r["avg_same_descriptor"]) for r in sub),
            "mean_abs_delta_tokens_rel": mean_defined(safe_float(r["abs_delta_tokens_rel"]) for r in sub),
            "mean_abs_delta_nodes_rel": mean_defined(safe_float(r["abs_delta_nodes_rel"]) for r in sub),
            "mean_abs_delta_beta1_rel": mean_defined(safe_float(r["abs_delta_beta1_rel"]) for r in sub),
            "mean_abs_delta_triangles_rel": mean_defined(safe_float(r["abs_delta_triangles_rel"]) for r in sub),
            "mean_abs_delta_spectral_radius_rel": mean_defined(safe_float(r["abs_delta_spectral_radius_rel"]) for r in sub),
            "mean_abs_delta_dim_proxy_rel": mean_defined(safe_float(r["abs_delta_dim_proxy_rel"]) for r in sub),
            "mean_abs_delta_clustering_rel": mean_defined(safe_float(r["abs_delta_clustering_rel"]) for r in sub),
        }
        for feature in STABILITY_FEATURES:
            row[feature] = safe_float(base[feature])
        out.append(row)
    return out


def resample_by_target(rows: Sequence[Dict[str, Any]], rng: random.Random) -> List[Dict[str, Any]]:
    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in rows:
        by_target.setdefault(int(row["target_nodes"]), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for target in sorted(by_target):
        sub = by_target[target]
        out.extend(dict(rng.choice(sub)) for _ in range(len(sub)))
    return out


def feature_stability_bootstrap_summary(
    base_rows: Sequence[Dict[str, Any]],
    bootstrap_reps: int,
    seed: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    original_rows = [r for r in v12.feature_stability_rows(base_rows) if r["row_type"] == "summary"]
    original_map = {str(r["feature"]): dict(r) for r in original_rows}
    rng = random.Random(seed)
    boot_rows: List[Dict[str, Any]] = []
    for rep in range(1, bootstrap_reps + 1):
        sample = resample_by_target(base_rows, rng)
        summary_rows = [r for r in v12.feature_stability_rows(sample) if r["row_type"] == "summary"]
        for row in summary_rows:
            boot_rows.append(
                {
                    "bootstrap_rep": rep,
                    "feature": row["feature"],
                    "mean_cv": safe_float(row["mean_cv"]),
                    "max_cv": safe_float(row["max_cv"]),
                    "value_range": safe_float(row["value_range"]),
                    "mean_vs_logN_slope": safe_float(row["mean_vs_logN_slope"]),
                }
            )

    summary: List[Dict[str, Any]] = []
    for feature in STABILITY_FEATURES:
        sub = [r for r in boot_rows if str(r["feature"]) == feature]
        mean_cvs = [safe_float(r["mean_cv"]) for r in sub]
        max_cvs = [safe_float(r["max_cv"]) for r in sub]
        slopes = [safe_float(r["mean_vs_logN_slope"]) for r in sub]
        ranges = [safe_float(r["value_range"]) for r in sub]
        base = original_map[feature]
        summary.append(
            {
                "feature": feature,
                "original_mean_cv": safe_float(base["mean_cv"]),
                "original_max_cv": safe_float(base["max_cv"]),
                "original_value_range": safe_float(base["value_range"]),
                "original_mean_vs_logN_slope": safe_float(base["mean_vs_logN_slope"]),
                "bootstrap_mean_cv": statistics.mean(mean_cvs) if mean_cvs else float("nan"),
                "bootstrap_q10_mean_cv": quantile(mean_cvs, 0.10),
                "bootstrap_q90_mean_cv": quantile(mean_cvs, 0.90),
                "bootstrap_mean_max_cv": statistics.mean(max_cvs) if max_cvs else float("nan"),
                "bootstrap_q90_max_cv": quantile(max_cvs, 0.90),
                "bootstrap_mean_range": statistics.mean(ranges) if ranges else float("nan"),
                "bootstrap_q10_slope": quantile(slopes, 0.10),
                "bootstrap_q90_slope": quantile(slopes, 0.90),
                "abs_slope_ci_max": max(abs(quantile(slopes, 0.10)), abs(quantile(slopes, 0.90))),
            }
        )
    summary.sort(
        key=lambda row: (
            safe_float(row["bootstrap_mean_cv"], float("inf")),
            safe_float(row["abs_slope_ci_max"], float("inf")),
            safe_float(row["bootstrap_q90_max_cv"], float("inf")),
        )
    )
    for idx, row in enumerate(summary, start=1):
        row["rank"] = idx
    return boot_rows, summary


def drift_bootstrap_summary(
    base_level_rows: Sequence[Dict[str, Any]],
    bootstrap_reps: int,
    seed: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    rng = random.Random(seed)
    boot_rows: List[Dict[str, Any]] = []
    for rep in range(1, bootstrap_reps + 1):
        sample = resample_by_target(base_level_rows, rng)
        ranked: List[Tuple[str, float]] = []
        for metric in DRIFT_METRICS:
            vals = [safe_float(r[metric]) for r in sample]
            mean_v = statistics.mean(vals) if vals else float("nan")
            ranked.append((metric, mean_v))
        ranked.sort(key=lambda item: item[1])
        rank_map = {metric: idx for idx, (metric, _) in enumerate(ranked, start=1)}
        for metric, mean_v in ranked:
            boot_rows.append(
                {
                    "bootstrap_rep": rep,
                    "metric": metric,
                    "mean_relative_drift": mean_v,
                    "rank": rank_map[metric],
                    "is_top1": int(rank_map[metric] == 1),
                    "is_top3": int(rank_map[metric] <= 3),
                }
            )

    summary: List[Dict[str, Any]] = []
    for metric in DRIFT_METRICS:
        sub = [r for r in boot_rows if str(r["metric"]) == metric]
        drifts = [safe_float(r["mean_relative_drift"]) for r in sub]
        ranks = [int(r["rank"]) for r in sub]
        summary.append(
            {
                "metric": metric,
                "bootstrap_mean_relative_drift": statistics.mean(drifts) if drifts else float("nan"),
                "bootstrap_q10_relative_drift": quantile(drifts, 0.10),
                "bootstrap_q90_relative_drift": quantile(drifts, 0.90),
                "bootstrap_mean_rank": statistics.mean(ranks) if ranks else float("nan"),
                "top1_prob": mean_defined(int(r["is_top1"]) for r in sub),
                "top3_prob": mean_defined(int(r["is_top3"]) for r in sub),
            }
        )
    summary.sort(
        key=lambda row: (
            safe_float(row["bootstrap_mean_relative_drift"], float("inf")),
            safe_float(row["bootstrap_mean_rank"], float("inf")),
        )
    )
    for idx, row in enumerate(summary, start=1):
        row["rank"] = idx
    return boot_rows, summary


def evaluate_basis_on_split(
    train_rows: Sequence[Dict[str, Any]],
    test_rows: Sequence[Dict[str, Any]],
    basis_name: str,
    features: Sequence[str],
    target_metric: str,
) -> Dict[str, Any]:
    intercept, weights = v12.fit_linear_regression(train_rows, features, target_metric)
    enriched_test: List[Dict[str, Any]] = []
    actual = []
    predicted = []
    for row in test_rows:
        pred = v12.predict_row(row, features, intercept, weights)
        actual_val = safe_float(row[target_metric])
        actual.append(actual_val)
        predicted.append(pred)
        enriched = dict(row)
        enriched["prediction"] = pred
        enriched_test.append(enriched)
    baseline_pred = mean_defined(safe_float(r[target_metric]) for r in train_rows)
    baseline_rmse = v12.rmse(actual, [baseline_pred] * len(actual))
    model_rmse = v12.rmse(actual, predicted)
    relative_skill = 1.0 - (model_rmse / baseline_rmse) if math.isfinite(baseline_rmse) and baseline_rmse > 1e-12 else float("nan")
    return {
        "basis_name": basis_name,
        "basis_features": "+".join(features),
        "feature_count": len(features),
        "rmse": model_rmse,
        "baseline_rmse": baseline_rmse,
        "relative_skill": relative_skill,
        "spearman_all": v12e.spearman(predicted, actual),
        "pairwise_all": v12e.pairwise_accuracy(enriched_test, "prediction", target_metric),
        "pairwise_within_target": v12e.within_target_pairwise_accuracy(enriched_test, "prediction", target_metric),
        "intercept": intercept,
        "weights": ",".join(f"{w:.6f}" for w in weights),
    }


def prediction_split_validation(
    base_level_rows: Sequence[Dict[str, Any]],
    repeats: int,
    test_frac: float,
    seed: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    rng = random.Random(seed)
    split_rows: List[Dict[str, Any]] = []
    for split_id in range(1, repeats + 1):
        train_idx, test_idx = v12e.stratified_holdout_indices(base_level_rows, rng, test_frac)
        train_rows = [dict(base_level_rows[i]) for i in train_idx]
        test_rows = [dict(base_level_rows[i]) for i in test_idx]
        for target_metric in PREDICTION_TARGETS:
            split_scores: List[Tuple[str, float]] = []
            for basis_name, features in BASIS_SPECS:
                stats = evaluate_basis_on_split(train_rows, test_rows, basis_name, features, target_metric)
                split_rows.append(
                    {
                        "split_id": split_id,
                        "target_metric": target_metric,
                        "train_rows": len(train_rows),
                        "test_rows": len(test_rows),
                        **stats,
                    }
                )
                split_scores.append((basis_name, safe_float(stats["relative_skill"], -1e9)))
            split_scores.sort(key=lambda item: item[1], reverse=True)
            for rank, (basis_name, _) in enumerate(split_scores, start=1):
                for row in split_rows[-len(BASIS_SPECS):]:
                    if row["split_id"] == split_id and row["target_metric"] == target_metric and row["basis_name"] == basis_name:
                        row["split_rank"] = rank
                        break

    summary: List[Dict[str, Any]] = []
    for target_metric in PREDICTION_TARGETS:
        target_rows = [r for r in split_rows if str(r["target_metric"]) == target_metric]
        for basis_name, features in BASIS_SPECS:
            sub = [r for r in target_rows if str(r["basis_name"]) == basis_name]
            skills = [safe_float(r["relative_skill"]) for r in sub]
            pairwise_all = [safe_float(r["pairwise_all"]) for r in sub]
            pairwise_within = [safe_float(r["pairwise_within_target"]) for r in sub]
            spearmans = [safe_float(r["spearman_all"]) for r in sub]
            ranks = [safe_float(r["split_rank"]) for r in sub]
            summary.append(
                {
                    "target_metric": target_metric,
                    "basis_name": basis_name,
                    "basis_features": "+".join(features),
                    "feature_count": len(features),
                    "mean_relative_skill": statistics.mean(skills) if skills else float("nan"),
                    "q10_relative_skill": quantile(skills, 0.10),
                    "q90_relative_skill": quantile(skills, 0.90),
                    "positive_skill_rate": mean_defined(float(v > 0.0) for v in skills),
                    "mean_pairwise_all": statistics.mean(pairwise_all) if pairwise_all else float("nan"),
                    "mean_pairwise_within_target": statistics.mean(pairwise_within) if pairwise_within else float("nan"),
                    "mean_spearman_all": statistics.mean(spearmans) if spearmans else float("nan"),
                    "mean_split_rank": statistics.mean(ranks) if ranks else float("nan"),
                    "top_rank_rate": mean_defined(float(r == 1) for r in ranks),
                }
            )
    summary.sort(
        key=lambda row: (
            str(row["target_metric"]),
            -safe_float(row["mean_relative_skill"], -1e9),
            -safe_float(row["mean_pairwise_within_target"], -1e9),
        )
    )

    pairwise_rows: List[Dict[str, Any]] = []
    for target_metric in PREDICTION_TARGETS:
        target_rows = [r for r in split_rows if str(r["target_metric"]) == target_metric]
        by_basis = {basis_name: [r for r in target_rows if str(r["basis_name"]) == basis_name] for basis_name, _ in BASIS_SPECS}
        for (basis_a, _), (basis_b, _) in itertools.combinations(BASIS_SPECS, 2):
            rows_a = by_basis[basis_a]
            rows_b = by_basis[basis_b]
            better_skill = 0.0
            better_pairwise = 0.0
            total = 0
            margins: List[float] = []
            for row_a, row_b in zip(rows_a, rows_b):
                sa = safe_float(row_a["relative_skill"])
                sb = safe_float(row_b["relative_skill"])
                pa = safe_float(row_a["pairwise_within_target"])
                pb = safe_float(row_b["pairwise_within_target"])
                total += 1
                if sa > sb:
                    better_skill += 1.0
                elif abs(sa - sb) <= 1e-12:
                    better_skill += 0.5
                if pa > pb:
                    better_pairwise += 1.0
                elif abs(pa - pb) <= 1e-12:
                    better_pairwise += 0.5
                margins.append(sa - sb)
            pairwise_rows.append(
                {
                    "target_metric": target_metric,
                    "basis_a": basis_a,
                    "basis_b": basis_b,
                    "p_a_beats_b_by_skill": (better_skill / total) if total else float("nan"),
                    "p_a_beats_b_by_pairwise_within_target": (better_pairwise / total) if total else float("nan"),
                    "mean_skill_margin_a_minus_b": statistics.mean(margins) if margins else float("nan"),
                }
            )
    return split_rows, summary, pairwise_rows


def validation_priority(
    stability_rows: Sequence[Dict[str, Any]],
    drift_rows: Sequence[Dict[str, Any]],
    prediction_rows: Sequence[Dict[str, Any]],
    pairwise_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    radius_rows = [r for r in prediction_rows if str(r["target_metric"]) == "mean_final_radius_control" and str(r["basis_name"]) != "full_basis"]
    radius_rows.sort(key=lambda r: safe_float(r["mean_relative_skill"], -1e9), reverse=True)
    if radius_rows:
        best = radius_rows[0]
        runner = radius_rows[1] if len(radius_rows) >= 2 else None
        pair = None
        if runner is not None:
            pair = next(
                (
                    r for r in pairwise_rows
                    if str(r["target_metric"]) == "mean_final_radius_control"
                    and {
                        str(r["basis_a"]),
                        str(r["basis_b"]),
                    } == {str(best["basis_name"]), str(runner["basis_name"])}
                ),
                None,
            )
        if safe_float(best["q10_relative_skill"]) > 0.0 and safe_float(best["positive_skill_rate"]) >= 0.85:
            status = "yes_targeted"
            note = "Radius-signalet er ekte nok til å fortjene større validering."
            if pair is not None:
                p = safe_float(pair["p_a_beats_b_by_skill"])
                p = p if str(pair["basis_a"]) == str(best["basis_name"]) else 1.0 - p
                if 0.35 <= p <= 0.65:
                    status = "yes_to_resolve_compact_ranking"
                    note = "Radius-signalet er positivt, men de beste små basisene er fortsatt for tette til å rangere hardt."
        else:
            status = "not_yet"
            note = "Radius-signalet er for svakt eller for ustabilt til at større validering er førsteprioritet."
        out.append(
            {
                "signal_family": "radius_basis",
                "status": status,
                "best_candidate": best["basis_name"],
                "note": note,
            }
        )

    overlap_rows = [r for r in prediction_rows if str(r["target_metric"]) == "mean_avg_local_overlap" and str(r["basis_name"]) != "full_basis"]
    overlap_rows.sort(key=lambda r: safe_float(r["mean_relative_skill"], -1e9), reverse=True)
    if overlap_rows:
        best = overlap_rows[0]
        status = "not_yet"
        note = "Overlap-signalet er fortsatt for svakt til å forsvare større validering."
        if safe_float(best["q10_relative_skill"]) > 0.0 and safe_float(best["positive_skill_rate"]) >= 0.85:
            status = "maybe"
            note = "Overlap-signalet ser bedre ut enn før, men trenger fortsatt forsiktig lesning."
        out.append(
            {
                "signal_family": "overlap_basis",
                "status": status,
                "best_candidate": best["basis_name"],
                "note": note,
            }
        )

    stable = stability_rows[:2]
    if stable:
        out.append(
            {
                "signal_family": "stable_geometry_features",
                "status": "yes_targeted",
                "best_candidate": "+".join(str(r["feature"]) for r in stable),
                "note": "De mest stabile normaliserte geometriaksene er sterke nok til å brukes som faste kontroller i større validering.",
            }
        )

    drift_best = drift_rows[:3]
    if drift_best:
        artifact_like = {"mean_abs_delta_nodes_rel", "mean_abs_delta_beta1_rel"}
        best_name = str(drift_best[0]["metric"])
        status = "cross_regime_first" if best_name in artifact_like else "yes_targeted"
        note = (
            "Null- eller nesten-null-drift ser interessant ut, men bør testes på tvers av nærliggende regimer før større validering."
            if best_name in artifact_like
            else "De tregeste driftstørrelsene er lovende quasi-invariant-kandidater for videre validering."
        )
        out.append(
            {
                "signal_family": "quasi_invariants",
                "status": status,
                "best_candidate": "+".join(str(r["metric"]) for r in drift_best),
                "note": note,
            }
        )
    return out


def build_report(
    target_summary: Sequence[Dict[str, Any]],
    stability_rows: Sequence[Dict[str, Any]],
    drift_rows: Sequence[Dict[str, Any]],
    prediction_rows: Sequence[Dict[str, Any]],
    pairwise_rows: Sequence[Dict[str, Any]],
    recommendation_rows: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.13: validering av geometri- og invariantsignaler")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tar et steg tilbake fra workflow-policyene og spør hvor robuste de underliggende geometri- og quasi-invariantsignalene faktisk er. "
        "Målet er å avgjøre om et større valideringssett sannsynligvis vil gi ny informasjon, eller bare mer støy rundt svake effekter."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean_initial | q10 | q90 | separated_from_prev | mean_dim_proxy |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {safe_float(row['mean_initial_nodes']):.1f} | {safe_float(row['q10_initial_nodes']):.1f} | "
            f"{safe_float(row['q90_initial_nodes']):.1f} | {int(row['separated_from_prev'])} | {safe_float(row['mean_initial_dim_proxy']):.3f} |"
        )
    lines.append("")
    lines.append("## 1. Geometrisk stabilitet")
    lines.append("")
    lines.append("| rank | feature | mean_cv | q10_cv | q90_cv | slope_q10 | slope_q90 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in stability_rows:
        lines.append(
            f"| {int(row['rank'])} | {row['feature']} | {safe_float(row['bootstrap_mean_cv']):.3f} | "
            f"{safe_float(row['bootstrap_q10_mean_cv']):.3f} | {safe_float(row['bootstrap_q90_mean_cv']):.3f} | "
            f"{safe_float(row['bootstrap_q10_slope']):.3f} | {safe_float(row['bootstrap_q90_slope']):.3f} |"
        )
    lines.append("")
    lines.append("## 2. Quasi-invariant-kandidater")
    lines.append("")
    lines.append("| rank | metric | mean_rel_drift | q10 | q90 | top1_prob | top3_prob |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in drift_rows:
        lines.append(
            f"| {int(row['rank'])} | {row['metric']} | {safe_float(row['bootstrap_mean_relative_drift']):.4f} | "
            f"{safe_float(row['bootstrap_q10_relative_drift']):.4f} | {safe_float(row['bootstrap_q90_relative_drift']):.4f} | "
            f"{safe_float(row['top1_prob']):.3f} | {safe_float(row['top3_prob']):.3f} |"
        )
    lines.append("")
    lines.append("## 3. Redusert basis: split-validering")
    lines.append("")
    lines.append("| target_metric | basis | mean_skill | q10_skill | q90_skill | positive_rate | pairwise_within | spearman | top_rank_rate |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in prediction_rows:
        lines.append(
            f"| {row['target_metric']} | {row['basis_name']} | {safe_float(row['mean_relative_skill']):.3f} | "
            f"{safe_float(row['q10_relative_skill']):.3f} | {safe_float(row['q90_relative_skill']):.3f} | "
            f"{safe_float(row['positive_skill_rate']):.3f} | {safe_float(row['mean_pairwise_within_target']):.3f} | "
            f"{safe_float(row['mean_spearman_all']):.3f} | {safe_float(row['top_rank_rate']):.3f} |"
        )
    lines.append("")
    lines.append("## 4. Pairwise basis-sammenligning")
    lines.append("")
    lines.append("| target_metric | basis_a | basis_b | p_a_beats_b_by_skill | p_a_beats_b_by_pairwise | mean_skill_margin |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in pairwise_rows:
        lines.append(
            f"| {row['target_metric']} | {row['basis_a']} | {row['basis_b']} | "
            f"{safe_float(row['p_a_beats_b_by_skill']):.3f} | {safe_float(row['p_a_beats_b_by_pairwise_within_target']):.3f} | "
            f"{safe_float(row['mean_skill_margin_a_minus_b']):.3f} |"
        )
    lines.append("")
    lines.append("## 5. Repo-lojal tolkning")
    lines.append("")
    lines.append(
        "- Algebraiske identiteter er fortsatt ikke hovedpoenget her. Denne runden handler om normalisert geometri, langsom drift og prediktiv kompresjon."
    )
    lines.append(
        "- Generatorsporet holdes separat via target summary. Dersom startstørrelsene ikke hadde vært rent separert, ville tolkningen under vært mye svakere."
    )
    lines.append(
        "- `mean_abs_delta_nodes_rel` og `mean_abs_delta_beta1_rel` kan se svært sterke ut, men bør fortsatt behandles som mulige regime-/koblingsartefakter til de er testet bedre på tvers av nærliggende regimer."
    )
    lines.append(
        "- Den viktige beslutningen i denne runden er ikke om én liten basis 'vinner alt', men om radius-/geometrisignalet er ekte nok til å fortjene et større valideringssett."
    )
    lines.append("")
    lines.append("## 6. Anbefaling om større valideringssett")
    lines.append("")
    lines.append("| signal_family | status | best_candidate | note |")
    lines.append("| --- | --- | --- | --- |")
    for row in recommendation_rows:
        lines.append(
            f"| {row['signal_family']} | {row['status']} | {row['best_candidate']} | {row['note']} |"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(recommendation_rows: Sequence[Dict[str, Any]]) -> str:
    radius = next((r for r in recommendation_rows if str(r["signal_family"]) == "radius_basis"), None)
    drift = next((r for r in recommendation_rows if str(r["signal_family"]) == "quasi_invariants"), None)
    lines = [
        "# v0.13 for ikke-spesialister",
        "",
        "Denne runden spør ikke om en ny frontier-vinner. Den spør om de geometriske mønstrene vi ser er sterke nok til at det er verdt å samle mye mer data.",
        "",
    ]
    if radius is not None:
        lines.append(f"- Radius-signalet: `{radius['status']}` via `{radius['best_candidate']}`.")
    if drift is not None:
        lines.append(f"- Quasi-invariant-sporet: `{drift['status']}` via `{drift['best_candidate']}`.")
    lines.extend(
        [
            "",
            "Kort sagt: vi prøver å skille ekte struktur fra ting som bare ser pene ut i små datasett.",
            "",
        ]
    )
    return "\n".join(lines)


def build_recommendation(recommendation_rows: Sequence[Dict[str, Any]], prediction_rows: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.13 operativ anbefaling", ""]
    radius = next((r for r in recommendation_rows if str(r["signal_family"]) == "radius_basis"), None)
    overlap = next((r for r in recommendation_rows if str(r["signal_family"]) == "overlap_basis"), None)
    stable = next((r for r in recommendation_rows if str(r["signal_family"]) == "stable_geometry_features"), None)
    drift = next((r for r in recommendation_rows if str(r["signal_family"]) == "quasi_invariants"), None)
    if radius is not None:
        lines.append(f"- Radius/geometri: {radius['note']}")
    if overlap is not None:
        lines.append(f"- Overlap/repair: {overlap['note']}")
    if stable is not None:
        lines.append(f"- Stabile startfeatures: {stable['note']}")
    if drift is not None:
        lines.append(f"- Quasi-invarianter: {drift['note']}")
    radius_rows = [
        r for r in prediction_rows
        if str(r["target_metric"]) == "mean_final_radius_control" and str(r["basis_name"]) != "full_basis"
    ]
    radius_rows.sort(key=lambda r: safe_float(r["mean_relative_skill"], -1e9), reverse=True)
    if len(radius_rows) >= 2:
        best_radius = radius_rows[0]
        second_radius = radius_rows[1]
        lines.append(
            f"- Hold `{best_radius['basis_name']}` og `{second_radius['basis_name']}` som hovedduo i neste større strukturvalidering. "
            f"I denne runden ligger de på mean radius-skill {safe_float(best_radius['mean_relative_skill']):.3f} og "
            f"{safe_float(second_radius['mean_relative_skill']):.3f}."
        )
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.13 geometry signal validation")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=5)
    ap.add_argument("--run-seeds", type=int, default=5)
    ap.add_argument("--bootstrap-reps", type=int, default=200)
    ap.add_argument("--split-repeats", type=int, default=140)
    ap.add_argument("--test-frac", type=float, default=0.35)
    ap.add_argument("--output-prefix", default="Documentation/v13")
    ap.add_argument("--report-md", default="Documentation/v13_geometry_signal_validation.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_13.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_13_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    candidate = fixed_candidate()
    growth_seeds = [43001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [17101 + 31 * i for i in range(args.run_seeds)]

    print(
        f"[v13] regime={regime.name} targets={targets} candidate={candidate.name} "
        f"growth={len(growth_seeds)} runs={len(run_offsets)} boot={args.bootstrap_reps} splits={args.split_repeats}"
    )
    print("[v13] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    base_lookup = {(str(r["ensemble"]), int(r["growth_seed"])): dict(r) for r in base_rows}
    print("[v13] bases done")

    print("[v13] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows([candidate], ensembles, base_states, growth_seeds, run_offsets, regime.name)
    run_rows = [v12.enrich_run_row(row, base_lookup) for row in raw_run_rows]
    print(f"[v13] runs done: {len(run_rows)} rows")

    print("[v13] aggregating base-level rows...")
    base_level_rows = grouped_base_level_rows(base_rows, run_rows)

    print("[v13] bootstrap: feature stability...")
    stability_boot_rows, stability_summary_rows = feature_stability_bootstrap_summary(
        base_rows, args.bootstrap_reps, seed=19001
    )

    print("[v13] bootstrap: quasi-invariant drift...")
    drift_boot_rows, drift_summary_rows = drift_bootstrap_summary(
        base_level_rows, args.bootstrap_reps, seed=19037
    )

    print("[v13] repeated split validation...")
    prediction_split_rows, prediction_summary_rows, prediction_pairwise_rows = prediction_split_validation(
        base_level_rows,
        repeats=args.split_repeats,
        test_frac=args.test_frac,
        seed=19111,
    )

    recommendation_rows = validation_priority(
        stability_summary_rows,
        drift_summary_rows,
        prediction_summary_rows,
        prediction_pairwise_rows,
    )

    print("[v13] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_geometry_signal_validation_base_rows.csv", base_level_rows)
    write_csv(f"{prefix}_geometry_signal_validation_target_summary.csv", list(target_summary))
    write_csv(f"{prefix}_geometry_signal_stability_bootstrap_rows.csv", stability_boot_rows)
    write_csv(f"{prefix}_geometry_signal_stability_summary.csv", stability_summary_rows)
    write_csv(f"{prefix}_quasi_invariant_bootstrap_rows.csv", drift_boot_rows)
    write_csv(f"{prefix}_quasi_invariant_bootstrap_summary.csv", drift_summary_rows)
    write_csv(f"{prefix}_geometry_signal_validation_split_rows.csv", prediction_split_rows)
    write_csv(f"{prefix}_geometry_signal_validation_summary.csv", prediction_summary_rows)
    write_csv(f"{prefix}_geometry_signal_validation_pairwise.csv", prediction_pairwise_rows)
    write_csv(f"{prefix}_geometry_signal_validation_recommendations.csv", recommendation_rows)

    for path, content in [
        (
            args.report_md,
            build_report(
                target_summary,
                stability_summary_rows,
                drift_summary_rows,
                prediction_summary_rows,
                prediction_pairwise_rows,
                recommendation_rows,
            ),
        ),
        (args.lay_md, build_lay_summary(recommendation_rows)),
        (args.recommendation_md, build_recommendation(recommendation_rows, prediction_summary_rows)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v13] done")


if __name__ == "__main__":
    main()
