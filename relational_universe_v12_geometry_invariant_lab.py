#!/usr/bin/env python3
"""v0.12 geometry / invariant lab around the frozen band_zero_del regime.

This script is the first step after the v11 frontier work. It treats the
frontier as temporarily frozen at `band_zero_del` and asks three narrower
questions:

1. Do a few normalized geometric observables stay stable across scale?
2. Which observables drift slowest under the dynamics, i.e. look most like
   quasi-invariants inside this regime?
3. Can a small geometric basis predict important dynamical outcomes nearly as
   well as a larger descriptive bundle?

The point is not to prove new mathematics outright. The point is to test
whether the regime exposes structure that could later support simpler or more
efficient algorithms on the states it generates.
"""
from __future__ import annotations

import argparse
import itertools
import math
import statistics
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v11c_binary_bridge_vs_band as v11c


BASIS_FEATURES = [
    "initial_beta1_per_node",
    "initial_triangles_per_node",
    "initial_spectral_per_sqrtN",
    "initial_dim_proxy",
    "initial_clustering",
]

TARGET_METRICS = [
    "avg_local_overlap",
    "final_radius_control",
    "abs_delta_beta1_rel",
]


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v11c.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v11c.mean_defined(values)


def quantile(values: Sequence[float], q: float) -> float:
    return v10b.quantile(values, q)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v11c.write_csv(path, rows)


def fixed_candidate() -> v09.ScaleCandidate:
    return v09.ScaleCandidate("band_zero_del", 0.02, 0.00, 0.02, 0.00, 0.00)


def enrich_run_row(row: Dict[str, Any], base_lookup: Mapping[Tuple[str, int], Dict[str, Any]]) -> Dict[str, Any]:
    base = base_lookup[(str(row["ensemble"]), int(row["growth_seed"]))]
    initial_nodes = max(1.0, safe_float(row["initial_nodes"], 1.0))
    initial_tokens = max(1.0, safe_float(row["initial_tokens"], 1.0))
    initial_beta1 = max(1.0, safe_float(row["initial_beta1"], 1.0))
    initial_triangles = max(1.0, safe_float(row["initial_triangles"], 1.0))
    initial_spectral = max(1e-9, safe_float(row["initial_spectral_radius"], 1.0))
    initial_dim = max(1e-9, safe_float(row["initial_dim_proxy"], 1.0))
    initial_clustering = max(1e-9, safe_float(base["initial_clustering"], 1e-9))

    enriched = dict(row)
    for key in [
        "initial_avg_degree",
        "initial_beta1_per_node",
        "initial_triangles_per_node",
        "initial_spectral_per_sqrtN",
        "initial_clustering",
    ]:
        enriched[key] = safe_float(base[key], float("nan"))

    enriched["abs_delta_tokens_rel"] = safe_float(row["abs_delta_tokens"]) / initial_tokens
    enriched["abs_delta_nodes_rel"] = safe_float(row["abs_delta_nodes"]) / initial_nodes
    enriched["abs_delta_beta1_rel"] = safe_float(row["abs_delta_beta1"]) / initial_beta1
    enriched["abs_delta_triangles_rel"] = safe_float(row["abs_delta_triangles"]) / initial_triangles
    enriched["abs_delta_spectral_radius_rel"] = safe_float(row["abs_delta_spectral_radius"]) / initial_spectral
    enriched["abs_delta_dim_proxy_rel"] = safe_float(row["abs_delta_dim_proxy"]) / initial_dim
    enriched["abs_delta_clustering_rel"] = safe_float(row["abs_delta_clustering"]) / initial_clustering
    return enriched


def feature_stability_rows(base_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    per_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in base_rows:
        per_target.setdefault(int(row["target_nodes"]), []).append(dict(row))

    detailed: List[Dict[str, Any]] = []
    features = [
        "initial_beta1_per_node",
        "initial_triangles_per_node",
        "initial_spectral_per_sqrtN",
        "initial_dim_proxy",
        "initial_clustering",
        "initial_avg_degree",
    ]
    target_means: Dict[str, List[Tuple[float, float]]] = {feat: [] for feat in features}
    for target in sorted(per_target):
        sub = per_target[target]
        for feat in features:
            vals = [safe_float(r[feat]) for r in sub]
            vals = [v for v in vals if math.isfinite(v)]
            mean_v = statistics.mean(vals) if vals else float("nan")
            sd_v = statistics.pstdev(vals) if len(vals) >= 2 else 0.0
            cv = (sd_v / abs(mean_v)) if vals and abs(mean_v) > 1e-12 else 0.0
            detailed.append(
                {
                    "row_type": "per_target",
                    "feature": feat,
                    "target_nodes": target,
                    "mean_value": mean_v,
                    "sd_value": sd_v,
                    "cv_value": cv,
                }
            )
            target_means[feat].append((math.log(float(target)), mean_v))

    summary: List[Dict[str, Any]] = []
    for feat in features:
        rows = [r for r in detailed if r["feature"] == feat]
        cvs = [safe_float(r["cv_value"]) for r in rows]
        means = [safe_float(r["mean_value"]) for r in rows]
        xs = [x for x, _ in target_means[feat]]
        ys = [y for _, y in target_means[feat]]
        slope, intercept = v09.linear_fit(xs, ys)
        summary.append(
            {
                "row_type": "summary",
                "feature": feat,
                "mean_cv": mean_defined(cvs),
                "max_cv": max(cvs) if cvs else float("nan"),
                "value_range": (max(means) - min(means)) if means else float("nan"),
                "mean_vs_logN_slope": slope,
                "mean_vs_logN_intercept": intercept,
            }
        )
    return detailed + summary


def summarize_runs_by_target(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in run_rows:
        by_target.setdefault(int(row["target_nodes"]), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    metrics = [
        "meeting",
        "avg_local_overlap",
        "avg_same_descriptor",
        "shared_token_fraction_final",
        "shared_node_fraction_final",
        "fit_speed_control",
        "final_radius_control",
        "final_edge_diff_count",
        "abs_delta_beta1_rel",
        "abs_delta_triangles_rel",
        "abs_delta_spectral_radius_rel",
        "abs_delta_dim_proxy_rel",
        "abs_delta_clustering_rel",
    ]
    for target in sorted(by_target):
        sub = by_target[target]
        row: Dict[str, Any] = {
            "target_nodes": target,
            "runs": len(sub),
        }
        for metric in metrics:
            vals = [safe_float(r.get(metric), float("nan")) for r in sub]
            vals = [v for v in vals if math.isfinite(v)]
            row[f"mean_{metric}"] = statistics.mean(vals) if vals else float("nan")
            row[f"sd_{metric}"] = statistics.pstdev(vals) if len(vals) >= 2 else 0.0
        out.append(row)
    return out


def relative_drift_ranking(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    drift_keys = [
        "abs_delta_tokens_rel",
        "abs_delta_nodes_rel",
        "abs_delta_beta1_rel",
        "abs_delta_triangles_rel",
        "abs_delta_spectral_radius_rel",
        "abs_delta_dim_proxy_rel",
        "abs_delta_clustering_rel",
    ]
    rows: List[Dict[str, Any]] = []
    for key in drift_keys:
        vals = [safe_float(r.get(key), float("nan")) for r in run_rows]
        vals = [v for v in vals if math.isfinite(v)]
        rows.append(
            {
                "metric": key,
                "mean_relative_drift": statistics.mean(vals) if vals else float("nan"),
                "median_relative_drift": statistics.median(vals) if vals else float("nan"),
                "q10_relative_drift": quantile(vals, 0.10),
                "q90_relative_drift": quantile(vals, 0.90),
            }
        )
    rows.sort(key=lambda row: safe_float(row["mean_relative_drift"], float("inf")))
    for i, row in enumerate(rows, start=1):
        row["rank"] = i
    return rows


def solve_linear_system(a: List[List[float]], b: List[float]) -> List[float]:
    n = len(a)
    aug = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-12:
            return [0.0] * n
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col]
            if factor == 0.0:
                continue
            aug[r] = [x - factor * y for x, y in zip(aug[r], aug[col])]
    return [aug[i][-1] for i in range(n)]


def fit_linear_regression(rows: Sequence[Dict[str, Any]], features: Sequence[str], target: str) -> Tuple[float, List[float]]:
    p = len(features) + 1
    xtx = [[0.0 for _ in range(p)] for _ in range(p)]
    xty = [0.0 for _ in range(p)]
    for row in rows:
        x = [1.0] + [safe_float(row[f], 0.0) for f in features]
        y = safe_float(row[target], 0.0)
        for i in range(p):
            xty[i] += x[i] * y
            for j in range(p):
                xtx[i][j] += x[i] * x[j]
    coeffs = solve_linear_system(xtx, xty)
    intercept = coeffs[0]
    weights = coeffs[1:]
    return intercept, weights


def predict_row(row: Mapping[str, Any], features: Sequence[str], intercept: float, weights: Sequence[float]) -> float:
    return intercept + sum(w * safe_float(row[f], 0.0) for f, w in zip(features, weights))


def rmse(actual: Sequence[float], predicted: Sequence[float]) -> float:
    if not actual:
        return float("nan")
    return math.sqrt(sum((a - p) ** 2 for a, p in zip(actual, predicted)) / len(actual))


def reduced_basis_summary(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    subsets: List[Tuple[str, ...]] = []
    for k in (1, 2):
        subsets.extend(itertools.combinations(BASIS_FEATURES, k))
    subsets.append(tuple(BASIS_FEATURES))

    targets = sorted({int(r["target_nodes"]) for r in run_rows})
    for target_metric in TARGET_METRICS:
        for subset in subsets:
            fold_rmses: List[float] = []
            baseline_rmses: List[float] = []
            for held_target in targets:
                train = [r for r in run_rows if int(r["target_nodes"]) != held_target]
                test = [r for r in run_rows if int(r["target_nodes"]) == held_target]
                intercept, weights = fit_linear_regression(train, subset, target_metric)
                preds = [predict_row(r, subset, intercept, weights) for r in test]
                actual = [safe_float(r[target_metric], 0.0) for r in test]
                fold_rmses.append(rmse(actual, preds))
                baseline = statistics.mean(safe_float(r[target_metric], 0.0) for r in train)
                baseline_rmses.append(rmse(actual, [baseline] * len(actual)))
            mean_rmse = mean_defined(fold_rmses)
            mean_base = mean_defined(baseline_rmses)
            skill = 1.0 - (mean_rmse / mean_base) if math.isfinite(mean_base) and mean_base > 1e-12 else float("nan")
            results.append(
                {
                    "target_metric": target_metric,
                    "subset_size": len(subset),
                    "subset_name": "+".join(subset),
                    "cv_rmse": mean_rmse,
                    "baseline_rmse": mean_base,
                    "relative_skill": skill,
                }
            )
    results.sort(key=lambda row: (str(row["target_metric"]), int(row["subset_size"]), -safe_float(row["relative_skill"], -1e9)))
    return results


def top_basis_rows(basis_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    selected: List[Dict[str, Any]] = []
    for metric in TARGET_METRICS:
        sub = [r for r in basis_rows if r["target_metric"] == metric]
        if not sub:
            continue
        best_one = max((r for r in sub if int(r["subset_size"]) == 1), key=lambda r: safe_float(r["relative_skill"], -1e9))
        best_two = max((r for r in sub if int(r["subset_size"]) == 2), key=lambda r: safe_float(r["relative_skill"], -1e9))
        full = max((r for r in sub if int(r["subset_size"]) == len(BASIS_FEATURES)), key=lambda r: safe_float(r["relative_skill"], -1e9))
        selected.extend([best_one, best_two, full])
    return selected


def build_report(
    target_summary: Sequence[Dict[str, Any]],
    feature_rows: Sequence[Dict[str, Any]],
    run_summary_rows: Sequence[Dict[str, Any]],
    drift_rows: Sequence[Dict[str, Any]],
    basis_rows: Sequence[Dict[str, Any]],
) -> str:
    feature_summary = [r for r in feature_rows if r["row_type"] == "summary"]
    top_basis = top_basis_rows(basis_rows)
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.12: geometri- og invariantlab rundt band_zero_del")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden fryser frontier midlertidig ved `band_zero_del` og tester om regimet eksponerer en liten geometrisk eller invariant-lignende basis "
        "som kan beskrive dynamikken enklere enn en bred frontier-scan."
    )
    lines.append("")
    lines.append("## Startstorrelser")
    lines.append("")
    lines.append("| target | mean_initial | q10 | q90 | separated_from_prev | mean_beta1 | mean_triangles | mean_dim_proxy |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {safe_float(row['mean_initial_nodes']):.1f} | {safe_float(row['q10_initial_nodes']):.1f} | "
            f"{safe_float(row['q90_initial_nodes']):.1f} | {int(row['separated_from_prev'])} | {safe_float(row['mean_initial_beta1']):.1f} | "
            f"{safe_float(row['mean_initial_triangles']):.1f} | {safe_float(row['mean_initial_dim_proxy']):.3f} |"
        )
    lines.append("")
    lines.append("## Geometrisk stabilitet")
    lines.append("")
    lines.append("| feature | mean_cv | max_cv | range | slope_vs_logN |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in feature_summary:
        lines.append(
            f"| {row['feature']} | {safe_float(row['mean_cv']):.3f} | {safe_float(row['max_cv']):.3f} | "
            f"{safe_float(row['value_range']):.3f} | {safe_float(row['mean_vs_logN_slope']):.3f} |"
        )
    lines.append("")
    lines.append("## Dynamiske utfall per størrelse")
    lines.append("")
    lines.append("| target | overlap | radius | fit_speed | rel_drift_beta1 | rel_drift_triangles | rel_drift_dim |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in run_summary_rows:
        lines.append(
            f"| {int(row['target_nodes'])} | {safe_float(row['mean_avg_local_overlap']):.3f} | {safe_float(row['mean_final_radius_control']):.3f} | "
            f"{safe_float(row['mean_fit_speed_control']):.3f} | {safe_float(row['mean_abs_delta_beta1_rel']):.3f} | "
            f"{safe_float(row['mean_abs_delta_triangles_rel']):.3f} | {safe_float(row['mean_abs_delta_dim_proxy_rel']):.3f} |"
        )
    lines.append("")
    lines.append("## Kandidater til quasi-invarianter")
    lines.append("")
    lines.append("| rank | metric | mean_rel_drift | median_rel_drift | q10 | q90 |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in drift_rows:
        lines.append(
            f"| {int(row['rank'])} | {row['metric']} | {safe_float(row['mean_relative_drift']):.3f} | {safe_float(row['median_relative_drift']):.3f} | "
            f"{safe_float(row['q10_relative_drift']):.3f} | {safe_float(row['q90_relative_drift']):.3f} |"
        )
    lines.append("")
    lines.append("## Redusert basis som prediksjonsoppgave")
    lines.append("")
    lines.append("| target_metric | subset_size | subset | cv_rmse | baseline_rmse | relative_skill |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in top_basis:
        lines.append(
            f"| {row['target_metric']} | {int(row['subset_size'])} | {row['subset_name']} | "
            f"{safe_float(row['cv_rmse']):.4f} | {safe_float(row['baseline_rmse']):.4f} | {safe_float(row['relative_skill']):.3f} |"
        )
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append(
        "- Algebraiske identiteter er ikke hovedpoenget i denne runden; vi ser etter langsom drift og prediktiv kompresjon."
    )
    lines.append(
        "- Generatorartefakter holdes separat via target summary; hvis størrelsene ikke separerer, kan ikke geometrilesningen tas seriøst."
    )
    lines.append(
        "- Hvis en liten basis av normaliserte geometrifeatures gir god skill på dynamiske mål, er det et første tegn på at regimet bærer en effektiv grov beskrivelse."
    )
    lines.append(
        "- Hvis quasi-invariant-kandidatene også er de samme størrelsene som er lettest å predikere, er det spesielt interessant for videre matematisk arbeid."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(drift_rows: Sequence[Dict[str, Any]], basis_rows: Sequence[Dict[str, Any]]) -> str:
    best_drift = drift_rows[0]["metric"] if drift_rows else "ukjent"
    top_basis = top_basis_rows(basis_rows)
    best_basis = top_basis[0]["subset_name"] if top_basis else "ukjent"
    return "\n".join(
        [
            "# v0.12 for ikke-spesialister",
            "",
            "I stedet for å lete etter enda en ny frontier-vinner, bruker denne runden én stabil kandidat og ser etter skjult struktur.",
            "",
            f"- Den tregeste relative driften i denne runden ligger i `{best_drift}`.",
            f"- Den enkleste lovende prediksjonsbasisen i denne runden er `{best_basis}`.",
            "",
            "Hvis få størrelser kan forklare mye av oppførselen, er det den typen spor som senere kan bli til enklere eller raskere metoder.",
            "",
        ]
    )


def build_recommendation(drift_rows: Sequence[Dict[str, Any]], basis_rows: Sequence[Dict[str, Any]]) -> str:
    best_drift = drift_rows[0]["metric"] if drift_rows else "ukjent"
    top_basis = top_basis_rows(basis_rows)
    strongest = max(top_basis, key=lambda r: safe_float(r["relative_skill"], -1e9)) if top_basis else None
    lines = ["# v0.12 operativ anbefaling", ""]
    if strongest is not None:
        lines.append(
            f"Fortsett med geometri-/invariantsporet rundt `band_zero_del`. Prioriter `{best_drift}` som quasi-invariant-kandidat og "
            f"`{strongest['subset_name']}` som forelopig redusert basis for videre tester."
        )
    else:
        lines.append("Fortsett med geometri-/invariantsporet rundt `band_zero_del`, men vi trenger flere data for a identifisere en klar redusert basis.")
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12 geometry / invariant lab")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=4)
    ap.add_argument("--run-seeds", type=int, default=5)
    ap.add_argument("--output-prefix", default="Documentation/v12")
    ap.add_argument("--report-md", default="Documentation/v12_geometry_invariant_lab.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    candidate = fixed_candidate()
    growth_seeds = [23001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [8101 + 31 * i for i in range(args.run_seeds)]

    print(f"[v12] regime={regime.name} targets={targets} candidate={candidate.name} growth={len(growth_seeds)} runs={len(run_offsets)}")
    print("[v12] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    base_lookup = {(str(r["ensemble"]), int(r["growth_seed"])): dict(r) for r in base_rows}
    print("[v12] bases done")

    print("[v12] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows([candidate], ensembles, base_states, growth_seeds, run_offsets, regime.name)
    run_rows = [enrich_run_row(row, base_lookup) for row in raw_run_rows]
    print(f"[v12] runs done: {len(run_rows)} rows")

    feature_rows = feature_stability_rows(base_rows)
    run_summary_rows = summarize_runs_by_target(run_rows)
    drift_rows = relative_drift_ranking(run_rows)
    basis_rows = reduced_basis_summary(run_rows)

    print("[v12] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_geometry_base_rows.csv", base_rows)
    write_csv(f"{prefix}_geometry_target_summary.csv", list(target_summary))
    write_csv(f"{prefix}_geometry_run_rows.csv", run_rows)
    write_csv(f"{prefix}_geometry_feature_stability.csv", feature_rows)
    write_csv(f"{prefix}_geometry_run_summary.csv", run_summary_rows)
    write_csv(f"{prefix}_geometry_relative_drift_ranking.csv", drift_rows)
    write_csv(f"{prefix}_geometry_reduced_basis_summary.csv", basis_rows)

    for path, content in [
        (args.report_md, build_report(target_summary, feature_rows, run_summary_rows, drift_rows, basis_rows)),
        (args.lay_md, build_lay_summary(drift_rows, basis_rows)),
        (args.recommendation_md, build_recommendation(drift_rows, basis_rows)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v12] done")


if __name__ == "__main__":
    main()
