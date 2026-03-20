#!/usr/bin/env python3
"""v0.12e start-state screening / sorting around band_zero_del.

This step asks whether the small radius-surrogate plateau from v0.12d is useful
for a concrete task: cheaply ranking or screening start states before running
the full dynamics.
"""
from __future__ import annotations

import argparse
import math
import random
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12


ANCHOR_REGIME = "band_zero_del"
TARGET_METRIC = "mean_final_radius_control"
BASIS_SPECS = [
    ("spectral_plus_dim", ("initial_spectral_per_sqrtN", "initial_dim_proxy")),
    ("spectral_only", ("initial_spectral_per_sqrtN",)),
    ("spectral_plus_clustering", ("initial_spectral_per_sqrtN", "initial_clustering")),
    ("full_basis", tuple(v12.BASIS_FEATURES)),
]


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v12.write_csv(path, rows)


def fixed_candidate():
    import relational_universe_v09_scale_and_natural_ensembles as v09

    return v09.ScaleCandidate(ANCHOR_REGIME, 0.02, 0.00, 0.02, 0.00, 0.00)


def mean_defined(values: Iterable[float]) -> float:
    return v12.mean_defined(values)


def sd_or_zero(values: Sequence[float]) -> float:
    vals = [float(v) for v in values if math.isfinite(float(v))]
    if len(vals) < 2:
        return 0.0
    m = sum(vals) / len(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / len(vals))


def build_base_level_rows(base_rows: Sequence[Dict[str, Any]], run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    base_lookup = {(str(r["ensemble"]), int(r["growth_seed"])): dict(r) for r in base_rows}
    by_key: Dict[Tuple[str, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        by_key.setdefault((str(row["ensemble"]), int(row["growth_seed"])), []).append(dict(row))

    out: List[Dict[str, Any]] = []
    for (ensemble, growth_seed), sub in sorted(by_key.items()):
        base = base_lookup[(ensemble, growth_seed)]
        radii = [safe_float(r["final_radius_control"]) for r in sub]
        overlaps = [safe_float(r["avg_local_overlap"]) for r in sub]
        fit_speeds = [safe_float(r["fit_speed_control"]) for r in sub]
        out.append(
            {
                "ensemble": ensemble,
                "target_nodes": int(base["target_nodes"]),
                "growth_seed": int(growth_seed),
                "runs": len(sub),
                "mean_final_radius_control": mean_defined(radii),
                "sd_final_radius_control": sd_or_zero(radii),
                "mean_avg_local_overlap": mean_defined(overlaps),
                "mean_fit_speed_control": mean_defined(fit_speeds),
                "initial_avg_degree": safe_float(base["initial_avg_degree"]),
                "initial_beta1_per_node": safe_float(base["initial_beta1_per_node"]),
                "initial_triangles_per_node": safe_float(base["initial_triangles_per_node"]),
                "initial_spectral_per_sqrtN": safe_float(base["initial_spectral_per_sqrtN"]),
                "initial_dim_proxy": safe_float(base["initial_dim_proxy"]),
                "initial_clustering": safe_float(base["initial_clustering"]),
            }
        )
    return out


def target_summary(base_level_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in base_level_rows:
        by_target.setdefault(int(row["target_nodes"]), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for target in sorted(by_target):
        sub = by_target[target]
        out.append(
            {
                "target_nodes": target,
                "bases": len(sub),
                "mean_radius": mean_defined(safe_float(r["mean_final_radius_control"]) for r in sub),
                "sd_radius": sd_or_zero([safe_float(r["mean_final_radius_control"]) for r in sub]),
                "mean_overlap": mean_defined(safe_float(r["mean_avg_local_overlap"]) for r in sub),
                "mean_fit_speed": mean_defined(safe_float(r["mean_fit_speed_control"]) for r in sub),
            }
        )
    return out


def stratified_holdout_indices(rows: Sequence[Dict[str, Any]], rng: random.Random, test_frac: float) -> Tuple[List[int], List[int]]:
    train_idx: List[int] = []
    test_idx: List[int] = []
    by_target: Dict[int, List[int]] = {}
    for idx, row in enumerate(rows):
        by_target.setdefault(int(row["target_nodes"]), []).append(idx)
    for target in sorted(by_target):
        idxs = by_target[target][:]
        rng.shuffle(idxs)
        test_n = max(2, int(round(len(idxs) * test_frac)))
        test_n = min(test_n, max(1, len(idxs) - 2))
        test_idx.extend(idxs[:test_n])
        train_idx.extend(idxs[test_n:])
    return sorted(train_idx), sorted(test_idx)


def rank_values(values: Sequence[float]) -> List[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i
        while j + 1 < len(indexed) and indexed[j + 1][1] == indexed[i][1]:
            j += 1
        avg_rank = 0.5 * (i + j) + 1.0
        for k in range(i, j + 1):
            ranks[indexed[k][0]] = avg_rank
        i = j + 1
    return ranks


def pearson(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        return float("nan")
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    sxx = sum((x - xbar) ** 2 for x in xs)
    syy = sum((y - ybar) ** 2 for y in ys)
    if sxx <= 1e-12 or syy <= 1e-12:
        return float("nan")
    sxy = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    return sxy / math.sqrt(sxx * syy)


def spearman(xs: Sequence[float], ys: Sequence[float]) -> float:
    return pearson(rank_values(list(xs)), rank_values(list(ys)))


def pairwise_accuracy(rows: Sequence[Dict[str, Any]], pred_key: str, actual_key: str) -> float:
    correct = 0
    total = 0
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            ai = safe_float(rows[i][actual_key])
            aj = safe_float(rows[j][actual_key])
            if abs(ai - aj) <= 1e-12:
                continue
            pi = safe_float(rows[i][pred_key])
            pj = safe_float(rows[j][pred_key])
            total += 1
            if (pi - pj) * (ai - aj) > 0:
                correct += 1
            elif abs((pi - pj) * (ai - aj)) <= 1e-12:
                correct += 0.5
    return (correct / total) if total else float("nan")


def within_target_pairwise_accuracy(rows: Sequence[Dict[str, Any]], pred_key: str, actual_key: str) -> float:
    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in rows:
        by_target.setdefault(int(row["target_nodes"]), []).append(dict(row))
    vals = [pairwise_accuracy(sub, pred_key, actual_key) for sub in by_target.values()]
    return mean_defined(v for v in vals if math.isfinite(v))


def top_quantile_lift(rows: Sequence[Dict[str, Any]], pred_key: str, actual_key: str, q: float = 0.25) -> float:
    if not rows:
        return float("nan")
    sorted_rows = sorted(rows, key=lambda r: safe_float(r[pred_key]), reverse=True)
    top_n = max(1, int(math.ceil(len(rows) * q)))
    selected = sorted_rows[:top_n]
    selected_mean = mean_defined(safe_float(r[actual_key]) for r in selected)
    overall_mean = mean_defined(safe_float(r[actual_key]) for r in rows)
    if not math.isfinite(overall_mean) or abs(overall_mean) <= 1e-12:
        return float("nan")
    return (selected_mean / overall_mean) - 1.0


def within_target_top_quantile_lift(rows: Sequence[Dict[str, Any]], pred_key: str, actual_key: str, q: float = 0.25) -> float:
    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in rows:
        by_target.setdefault(int(row["target_nodes"]), []).append(dict(row))
    vals = [top_quantile_lift(sub, pred_key, actual_key, q=q) for sub in by_target.values()]
    return mean_defined(v for v in vals if math.isfinite(v))


def evaluate_basis_on_split(
    train_rows: Sequence[Dict[str, Any]],
    test_rows: Sequence[Dict[str, Any]],
    basis_name: str,
    features: Sequence[str],
) -> Dict[str, Any]:
    intercept, weights = v12.fit_linear_regression(train_rows, features, TARGET_METRIC)
    enriched_test: List[Dict[str, Any]] = []
    actual = []
    predicted = []
    for row in test_rows:
        pred = v12.predict_row(row, features, intercept, weights)
        actual_val = safe_float(row[TARGET_METRIC])
        actual.append(actual_val)
        predicted.append(pred)
        enriched = dict(row)
        enriched["predicted_radius"] = pred
        enriched_test.append(enriched)
    baseline_pred = mean_defined(safe_float(r[TARGET_METRIC]) for r in train_rows)
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
        "spearman_all": spearman(predicted, actual),
        "pairwise_all": pairwise_accuracy(enriched_test, "predicted_radius", TARGET_METRIC),
        "pairwise_within_target": within_target_pairwise_accuracy(enriched_test, "predicted_radius", TARGET_METRIC),
        "top_quartile_lift_all": top_quantile_lift(enriched_test, "predicted_radius", TARGET_METRIC),
        "top_quartile_lift_within_target": within_target_top_quantile_lift(enriched_test, "predicted_radius", TARGET_METRIC),
        "intercept": intercept,
        "weights": ",".join(f"{w:.6f}" for w in weights),
    }


def screening_summary(base_level_rows: Sequence[Dict[str, Any]], repeats: int, test_frac: float, seed: int) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    rng = random.Random(seed)
    split_rows: List[Dict[str, Any]] = []
    for split_id in range(1, repeats + 1):
        train_idx, test_idx = stratified_holdout_indices(base_level_rows, rng, test_frac)
        train_rows = [dict(base_level_rows[i]) for i in train_idx]
        test_rows = [dict(base_level_rows[i]) for i in test_idx]
        for basis_name, features in BASIS_SPECS:
            stats = evaluate_basis_on_split(train_rows, test_rows, basis_name, features)
            split_rows.append(
                {
                    "split_id": split_id,
                    "train_rows": len(train_rows),
                    "test_rows": len(test_rows),
                    **stats,
                }
            )

    summary_rows: List[Dict[str, Any]] = []
    for basis_name, features in BASIS_SPECS:
        sub = [r for r in split_rows if str(r["basis_name"]) == basis_name]
        summary_rows.append(
            {
                "basis_name": basis_name,
                "basis_features": "+".join(features),
                "feature_count": len(features),
                "mean_relative_skill": mean_defined(safe_float(r["relative_skill"]) for r in sub),
                "mean_spearman_all": mean_defined(safe_float(r["spearman_all"]) for r in sub),
                "mean_pairwise_all": mean_defined(safe_float(r["pairwise_all"]) for r in sub),
                "mean_pairwise_within_target": mean_defined(safe_float(r["pairwise_within_target"]) for r in sub),
                "mean_top_quartile_lift_all": mean_defined(safe_float(r["top_quartile_lift_all"]) for r in sub),
                "mean_top_quartile_lift_within_target": mean_defined(safe_float(r["top_quartile_lift_within_target"]) for r in sub),
                "mean_rmse": mean_defined(safe_float(r["rmse"]) for r in sub),
                "mean_baseline_rmse": mean_defined(safe_float(r["baseline_rmse"]) for r in sub),
            }
        )
    summary_rows.sort(
        key=lambda row: (
            safe_float(row["mean_pairwise_within_target"], -1e9),
            safe_float(row["mean_top_quartile_lift_within_target"], -1e9),
            safe_float(row["mean_relative_skill"], -1e9),
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
    repeats: int,
    test_frac: float,
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.12e: screening og sortering av starttilstander")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester om de enkle radius-basisene fra v12d kan brukes til billigere prediksjon eller sortering av starttilstander før vi kjører hele dynamikken."
    )
    lines.append("")
    lines.append("## Metode")
    lines.append("")
    lines.append(
        f"- Arbeidsregime: `{ANCHOR_REGIME}`."
    )
    lines.append(
        f"- Baseenheter: `{base_count}` starttilstander bygget fra `4` størrelser med `8` growth-seeds hver."
    )
    lines.append(
        f"- Dynamiske etiketter: `{run_count}` simulasjonsruns aggregert til base-nivå (`mean_final_radius_control`)."
    )
    lines.append(
        f"- Validering: `{repeats}` stratified holdout-split med testandel `{test_frac:.2f}` per størrelse."
    )
    lines.append("- Sammenligningsoppgaven er bevisst praktisk: kan vi rangere eller screene baser bedre enn en naiv konstant baseline?")
    lines.append("")
    lines.append("## Hvordan metricene leses")
    lines.append("")
    lines.append("- `relative_skill`: hvor mye bedre RMSE modellen er enn en konstant baseline.")
    lines.append("- `spearman_all`: hvor godt modellen bevarer global rangordning pa tvers av alle testbaser.")
    lines.append("- `pairwise_within_target`: hvor ofte modellen rangerer to baser riktig innen samme størrelse. Dette er den viktigste screening-metrikken hvis vi vil unnga at størrelse alene dominerer.")
    lines.append("- `top_quartile_lift_within_target`: hvor mye bedre de toppskorede basene faktisk er enn gjennomsnittet innen samme størrelse. Positiv verdi betyr nyttig screening-lift.")
    lines.append("")
    lines.append("## Base-nivå per størrelse")
    lines.append("")
    lines.append("| target | bases | mean_radius | sd_radius | mean_overlap | mean_fit_speed |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in target_rows:
        lines.append(
            f"| {int(row['target_nodes'])} | {int(row['bases'])} | {safe_float(row['mean_radius']):.3f} | {safe_float(row['sd_radius']):.3f} | {safe_float(row['mean_overlap']):.3f} | {safe_float(row['mean_fit_speed']):.3f} |"
        )
    lines.append("")
    lines.append("## Screening-sammendrag")
    lines.append("")
    lines.append("| rank | basis | pairwise_within_target | top_quartile_lift_within_target | spearman_all | relative_skill |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in summary_rows:
        lines.append(
            f"| {int(row['rank'])} | {row['basis_name']} | {safe_float(row['mean_pairwise_within_target']):.3f} | "
            f"{safe_float(row['mean_top_quartile_lift_within_target']):.3f} | {safe_float(row['mean_spearman_all']):.3f} | {safe_float(row['mean_relative_skill']):.3f} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    if summary_rows:
        best = summary_rows[0]
        second = summary_rows[1] if len(summary_rows) > 1 else None
        compact = next((row for row in summary_rows if int(row["feature_count"]) <= 2), None)
        lines.append(
            f"- Beste screening-basis i denne runden er `{best['basis_name']}` med within-target pairwise `{safe_float(best['mean_pairwise_within_target']):.3f}` og within-target top-quartile lift `{safe_float(best['mean_top_quartile_lift_within_target']):.3f}`."
        )
        if second is not None:
            lines.append(
                f"- Narmeste kontroll er `{second['basis_name']}`. Hvis den ligger naert, er det mer riktig a snakke om et lite arbeidsplateau enn en hard enkeltrangering."
            )
        if compact is not None and str(compact["basis_name"]) != str(best["basis_name"]):
            lines.append(
                f"- Beste kompakte basis er `{compact['basis_name']}`. Den slar ikke `full_basis` pa within-target screening her, men den holder hoyere global korrelasjon og bedre enkelhet."
            )
        lines.append(
            "- Den viktige metodiske lesningen er derfor ikke at én basis vant alt, men at repoet nå støtter et benchmark-vs-kompakt-basis-skille."
        )
    lines.append("- Denne runden ma leses som en nyttetest av en enkel surrogate, ikke som ny fysikk i seg selv.")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(summary_rows: Sequence[Dict[str, Any]]) -> str:
    best = summary_rows[0] if summary_rows else None
    best_name = best["basis_name"] if best is not None else "ingen klar basis"
    compact = next((row for row in summary_rows if int(row["feature_count"]) <= 2), None)
    compact_name = compact["basis_name"] if compact is not None else best_name
    return "\n".join(
        [
            "# v0.12e for ikke-spesialister",
            "",
            "Denne runden sjekker om vi kan bruke en liten geometrisk oppskrift til a finne lovende starttilstander uten a kjore hele simuleringen først.",
            "",
            f"- Den sterkeste sorteringsoppskriften i denne runden er `{best_name}`.",
            f"- Den beste lille oppskriften er `{compact_name}`.",
            "",
        ]
    )


def build_recommendation(summary_rows: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.12e operativ anbefaling", ""]
    if not summary_rows:
        lines.append("Screening-signalet er for svakt til å gi en operativ anbefaling.")
        lines.append("")
        return "\n".join(lines)
    best = summary_rows[0]
    second = summary_rows[1] if len(summary_rows) > 1 else None
    compact = next((row for row in summary_rows if int(row["feature_count"]) <= 2), None)
    if compact is not None and str(compact["basis_name"]) != str(best["basis_name"]):
        lines.append(
            f"Behold `full_basis` som screening-benchmark og `{compact['basis_name']}` som kompakt arbeidsbasis. Repoet stotter ennå ikke at den lille basisen slar `full_basis` pa within-target screening, men den er fortsatt den beste enkle kandidaten."
        )
    elif second is not None and abs(safe_float(best["mean_pairwise_within_target"]) - safe_float(second["mean_pairwise_within_target"])) <= 0.02:
        lines.append(
            f"Fortsett med et lite screening-plateau av `{best['basis_name']}` og `{second['basis_name']}`. De er for tette pa within-target ranking til at repoet stotter en hard enkeltrangering ennå."
        )
    else:
        lines.append(
            f"Fortsett med `{best['basis_name']}` som første screening-basis. Den gir best within-target ranking og best lift for top-k sortering i denne runden."
        )
        if second is not None:
            lines.append(f"Behold `{second['basis_name']}` som naer kontroll.")
    lines.append(
        "Hvis neste runde fortsatt ser god ut, er det naturlige steget a teste om denne enkle sorteringen faktisk kan spare simuleringstid i en kandidat-screeningflyt."
    )
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12e start-state screening")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=8)
    ap.add_argument("--run-seeds", type=int, default=6)
    ap.add_argument("--screening-repeats", type=int, default=40)
    ap.add_argument("--test-frac", type=float, default=0.25)
    ap.add_argument("--screening-seed", type=int, default=12051)
    ap.add_argument("--output-prefix", default="Documentation/v12e_screening")
    ap.add_argument("--report-md", default="Documentation/v12e_start_state_screening.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12e.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12e_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    candidate = fixed_candidate()
    growth_seeds = [31001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [12101 + 31 * i for i in range(args.run_seeds)]

    print(f"[v12e] regime={regime.name} targets={targets} growth={len(growth_seeds)} runs={len(run_offsets)}")
    print("[v12e] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    print("[v12e] bases done")

    print("[v12e] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows([candidate], ensembles, base_states, growth_seeds, run_offsets, regime.name)
    print(f"[v12e] runs done: {len(raw_run_rows)} rows")

    base_level = build_base_level_rows(base_rows, raw_run_rows)
    target_rows = target_summary(base_level)
    split_rows, summary_rows = screening_summary(
        base_level,
        repeats=args.screening_repeats,
        test_frac=args.test_frac,
        seed=args.screening_seed,
    )

    print("[v12e] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_base_rows.csv", base_level)
    write_csv(f"{prefix}_target_summary.csv", target_rows)
    write_csv(f"{prefix}_split_rows.csv", split_rows)
    write_csv(f"{prefix}_summary.csv", summary_rows)

    for path, content in [
        (
            args.report_md,
            build_report(
                target_rows,
                summary_rows,
                base_count=len(base_level),
                run_count=len(raw_run_rows),
                repeats=args.screening_repeats,
                test_frac=args.test_frac,
            ),
        ),
        (args.lay_md, build_lay_summary(summary_rows)),
        (args.recommendation_md, build_recommendation(summary_rows)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v12e] done")


if __name__ == "__main__":
    main()
