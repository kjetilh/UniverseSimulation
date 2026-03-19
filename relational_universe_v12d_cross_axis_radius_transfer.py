#!/usr/bin/env python3
"""v0.12d cross-axis radius-transfer test around band_zero_del.

This follows v0.12c. The goal is no longer to refine the triad axis further,
but to test whether the radius-surrogate signal survives small local
perturbations along nearby non-triad directions.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, List, Sequence

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12


ANCHOR_REGIME = "band_zero_del"
TARGET_METRIC = "final_radius_control"
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


def candidate_specs() -> List[Dict[str, Any]]:
    return [
        {
            "candidate": v09.ScaleCandidate("band_zero_del", 0.02, 0.00, 0.02, 0.00, 0.00),
            "axis_group": "anchor",
        },
        {
            "candidate": v09.ScaleCandidate("bridge_00075_0000", 0.02, 0.00, 0.02, 0.00075, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate("bridge_0010_0000", 0.02, 0.00, 0.02, 0.00100, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate("band_pdel_0005", 0.02, 0.00, 0.02, 0.00, 0.005),
            "axis_group": "delete",
        },
        {
            "candidate": v09.ScaleCandidate("band_pdel_0010", 0.02, 0.00, 0.02, 0.00, 0.010),
            "axis_group": "delete",
        },
        {
            "candidate": v09.ScaleCandidate("band_death_0005", 0.02, 0.005, 0.02, 0.00, 0.00),
            "axis_group": "death",
        },
    ]


def candidate_lookup() -> Dict[str, Dict[str, Any]]:
    return {spec["candidate"].name: spec for spec in candidate_specs()}


def summarize_regime_target_runs(run_rows: Sequence[Dict[str, Any]], meta: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_key: Dict[tuple[str, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        by_key.setdefault((str(row["candidate_name"]), int(row["target_nodes"])), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for (name, target), sub in sorted(by_key.items()):
        out.append(
            {
                "candidate_name": name,
                "axis_group": meta[name]["axis_group"],
                "target_nodes": target,
                "runs": len(sub),
                "mean_final_radius_control": v12.mean_defined(safe_float(r["final_radius_control"]) for r in sub),
                "mean_fit_speed_control": v12.mean_defined(safe_float(r["fit_speed_control"]) for r in sub),
                "mean_avg_local_overlap": v12.mean_defined(safe_float(r["avg_local_overlap"]) for r in sub),
                "mean_abs_delta_triangles_rel": v12.mean_defined(safe_float(r["abs_delta_triangles_rel"]) for r in sub),
            }
        )
    return out


def evaluate_basis(
    train_rows: Sequence[Dict[str, Any]],
    test_rows: Sequence[Dict[str, Any]],
    features: Sequence[str],
    target_metric: str,
) -> Dict[str, Any]:
    intercept, weights = v12.fit_linear_regression(train_rows, features, target_metric)
    preds = [v12.predict_row(r, features, intercept, weights) for r in test_rows]
    actual = [safe_float(r[target_metric], 0.0) for r in test_rows]
    train_mean = v12.mean_defined(safe_float(r[target_metric], 0.0) for r in train_rows)
    baseline_preds = [train_mean] * len(test_rows)
    rmse_model = v12.rmse(actual, preds)
    rmse_baseline = v12.rmse(actual, baseline_preds)
    skill = 1.0 - (rmse_model / rmse_baseline) if math.isfinite(rmse_baseline) and rmse_baseline > 1e-12 else float("nan")
    return {
        "cv_rmse": rmse_model,
        "baseline_rmse": rmse_baseline,
        "relative_skill": skill,
        "intercept": intercept,
        "weights": ",".join(f"{w:.6f}" for w in weights),
    }


def transfer_summary(run_rows: Sequence[Dict[str, Any]], meta: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    train_rows = [r for r in run_rows if str(r["candidate_name"]) == ANCHOR_REGIME]
    test_regimes = sorted({str(r["candidate_name"]) for r in run_rows})
    out: List[Dict[str, Any]] = []
    for regime in test_regimes:
        test_rows = [r for r in run_rows if str(r["candidate_name"]) == regime]
        axis_group = meta[regime]["axis_group"]
        for basis_name, features in BASIS_SPECS:
            stats = evaluate_basis(train_rows, test_rows, features, TARGET_METRIC)
            out.append(
                {
                    "target_metric": TARGET_METRIC,
                    "train_regime": ANCHOR_REGIME,
                    "test_regime": regime,
                    "axis_group": axis_group,
                    "basis_name": basis_name,
                    "basis_features": "+".join(features),
                    "feature_count": len(features),
                    **stats,
                }
            )
    return out


def basis_ranking(transfer_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    off_anchor = [r for r in transfer_rows if str(r["test_regime"]) != ANCHOR_REGIME]
    names = sorted({str(r["basis_name"]) for r in transfer_rows})
    out: List[Dict[str, Any]] = []
    for name in names:
        rows = [r for r in off_anchor if str(r["basis_name"]) == name]
        anchor_row = next((r for r in transfer_rows if str(r["basis_name"]) == name and str(r["test_regime"]) == ANCHOR_REGIME), None)
        skills = [safe_float(r["relative_skill"]) for r in rows]
        triad_rows = [r for r in rows if str(r["axis_group"]) == "triad"]
        cross_rows = [r for r in rows if str(r["axis_group"]) != "triad"]
        triad_skills = [safe_float(r["relative_skill"]) for r in triad_rows]
        cross_skills = [safe_float(r["relative_skill"]) for r in cross_rows]
        best_row = max(rows, key=lambda r: safe_float(r["relative_skill"], -1e9))
        worst_row = min(rows, key=lambda r: safe_float(r["relative_skill"], 1e9))
        out.append(
            {
                "basis_name": name,
                "basis_features": rows[0]["basis_features"] if rows else "",
                "feature_count": int(rows[0]["feature_count"]) if rows else 0,
                "anchor_skill": safe_float(anchor_row["relative_skill"]) if anchor_row else float("nan"),
                "mean_off_anchor_skill": v12.mean_defined(skills),
                "mean_triad_skill": v12.mean_defined(triad_skills),
                "mean_cross_axis_skill": v12.mean_defined(cross_skills),
                "min_off_anchor_skill": min(skills) if skills else float("nan"),
                "positive_off_anchor_regimes": sum(1 for v in skills if math.isfinite(v) and v > 0.0),
                "positive_cross_axis_regimes": sum(1 for v in cross_skills if math.isfinite(v) and v > 0.0),
                "cross_axis_regimes": len(cross_skills),
                "best_test_regime": str(best_row["test_regime"]),
                "best_test_skill": safe_float(best_row["relative_skill"]),
                "worst_test_regime": str(worst_row["test_regime"]),
                "worst_test_skill": safe_float(worst_row["relative_skill"]),
            }
        )
    out.sort(
        key=lambda row: (
            safe_float(row["mean_cross_axis_skill"], -1e9),
            safe_float(row["mean_off_anchor_skill"], -1e9),
            safe_float(row["min_off_anchor_skill"], -1e9),
        ),
        reverse=True,
    )
    for idx, row in enumerate(out, start=1):
        row["rank"] = idx
    return out


def build_report(
    target_summary: Sequence[Dict[str, Any]],
    run_summary_rows: Sequence[Dict[str, Any]],
    transfer_rows: Sequence[Dict[str, Any]],
    ranking_rows: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.12d: kryssakse radius-transfer")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester om radius-surrogatet holder utover ren triad-akse ved a sammenligne sma basisvalg mot triad-, delete- og death-naerregimer rundt `band_zero_del`."
    )
    lines.append("")
    lines.append("## Startstorrelser")
    lines.append("")
    lines.append("| target | mean_initial | q10 | q90 | separated_from_prev |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {safe_float(row['mean_initial_nodes']):.1f} | {safe_float(row['q10_initial_nodes']):.1f} | {safe_float(row['q90_initial_nodes']):.1f} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Regimeutfall per størrelse")
    lines.append("")
    lines.append("| regime | axis | target | radius | fit_speed | overlap | rel_drift_triangles |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in run_summary_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['axis_group']} | {int(row['target_nodes'])} | {safe_float(row['mean_final_radius_control']):.3f} | "
            f"{safe_float(row['mean_fit_speed_control']):.3f} | {safe_float(row['mean_avg_local_overlap']):.3f} | {safe_float(row['mean_abs_delta_triangles_rel']):.3f} |"
        )
    lines.append("")
    lines.append("## Radius-transfer per basis")
    lines.append("")
    lines.append("| regime | axis | basis | relative_skill |")
    lines.append("| --- | --- | --- | --- |")
    for row in transfer_rows:
        lines.append(
            f"| {row['test_regime']} | {row['axis_group']} | {row['basis_name']} | {safe_float(row['relative_skill']):.3f} |"
        )
    lines.append("")
    lines.append("## Basis-ranking")
    lines.append("")
    lines.append("| rank | basis | mean_cross_axis_skill | mean_off_anchor_skill | min_off_anchor_skill | cross_axis_positive |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in ranking_rows:
        lines.append(
            f"| {int(row['rank'])} | {row['basis_name']} | {safe_float(row['mean_cross_axis_skill']):.3f} | "
            f"{safe_float(row['mean_off_anchor_skill']):.3f} | {safe_float(row['min_off_anchor_skill']):.3f} | "
            f"{int(row['positive_cross_axis_regimes'])}/{int(row['cross_axis_regimes'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    if ranking_rows:
        best = ranking_rows[0]
        simple_control = next((row for row in ranking_rows[1:] if int(row["feature_count"]) <= int(best["feature_count"])), None)
        full_basis = next((row for row in ranking_rows if str(row["basis_name"]) == "full_basis"), None)
        lines.append(
            f"- Best kryssakse-basis er `{best['basis_name']}` med mean cross-axis skill `{safe_float(best['mean_cross_axis_skill']):.3f}` og total off-anchor skill `{safe_float(best['mean_off_anchor_skill']):.3f}`."
        )
        if simple_control is not None:
            lines.append(
                f"- Narmeste enkle kontroll er `{simple_control['basis_name']}`. Det er den riktige sammenligningen hvis vi bryr oss om enkel surrogate-geometri heller enn bare score alene."
            )
        if full_basis is not None:
            lines.append(
                f"- `full_basis` er fortsatt nyttig som sanity check, men den taper her pa samlet off-anchor-robusthet (`{safe_float(full_basis['mean_off_anchor_skill']):.3f}`) mot `{best['basis_name']}` (`{safe_float(best['mean_off_anchor_skill']):.3f}`)."
            )
    lines.append("- Dette er en strukturtest, ikke en ny frontier-runde. Negative tall her ma leses som grenser for surrogate-gyldighet, ikke som ny kandidatkonkurranse.")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(ranking_rows: Sequence[Dict[str, Any]]) -> str:
    best = ranking_rows[0] if ranking_rows else None
    best_name = best["basis_name"] if best is not None else "ingen klar basis"
    return "\n".join(
        [
            "# v0.12d for ikke-spesialister",
            "",
            "Denne runden tester om den enkle radius-oppskriften fortsatt virker når vi vrir litt pa andre lokale knapper enn bare triader.",
            "",
            f"- Den mest robuste lille oppskriften pa tvers av disse lokale variasjonene er `{best_name}`.",
            "",
        ]
    )


def build_recommendation(ranking_rows: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.12d operativ anbefaling", ""]
    if not ranking_rows:
        lines.append("Kryssakse-transferen er for svak eller ufullstendig til å gi en operativ anbefaling.")
        lines.append("")
        return "\n".join(lines)
    best = ranking_rows[0]
    simple_control = next((row for row in ranking_rows[1:] if int(row["feature_count"]) <= int(best["feature_count"])), None)
    close_plateau = False
    if simple_control is not None:
        close_plateau = abs(safe_float(best["mean_cross_axis_skill"]) - safe_float(simple_control["mean_cross_axis_skill"])) <= 0.01
    if close_plateau and simple_control is not None:
        lines.append(
            f"Fortsett med et lite arbeidsplateau av `{best['basis_name']}` og `{simple_control['basis_name']}`. De er for tette pa kryssakse-skill til at repoet stotter en hard enkeltrangering mellom de enkle basisene ennå."
        )
    else:
        lines.append(
            f"Fortsett radius-/surrogatesporet med `{best['basis_name']}` som første kryssakse-arbeidsbasis. Den topper mean cross-axis skill med `{safe_float(best['mean_cross_axis_skill']):.3f}`."
        )
        if simple_control is not None:
            lines.append(f"Behold `{simple_control['basis_name']}` som naer enkel kontroll.")
    lines.append(
        "Hold analysen smal og repo-lojal: les dette som en test av lokal surrogate-gyldighet, ikke som en ny frontier-konkurranse."
    )
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12d cross-axis radius-transfer")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=4)
    ap.add_argument("--run-seeds", type=int, default=4)
    ap.add_argument("--output-prefix", default="Documentation/v12d_cross_axis")
    ap.add_argument("--report-md", default="Documentation/v12d_cross_axis_radius_transfer.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12d.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12d_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    specs = candidate_specs()
    meta = candidate_lookup()
    candidates = [spec["candidate"] for spec in specs]
    growth_seeds = [29001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [11101 + 31 * i for i in range(args.run_seeds)]

    print(f"[v12d] regime={regime.name} targets={targets} candidates={[c.name for c in candidates]} growth={len(growth_seeds)} runs={len(run_offsets)}")
    print("[v12d] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    base_lookup = {(str(r['ensemble']), int(r['growth_seed'])): dict(r) for r in base_rows}
    print("[v12d] bases done")

    print("[v12d] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    run_rows = [v12.enrich_run_row(row, base_lookup) for row in raw_run_rows]
    print(f"[v12d] runs done: {len(run_rows)} rows")

    run_summary_rows = summarize_regime_target_runs(run_rows, meta)
    transfer_rows = transfer_summary(run_rows, meta)
    ranking_rows = basis_ranking(transfer_rows)

    print("[v12d] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_base_rows.csv", base_rows)
    write_csv(f"{prefix}_target_summary.csv", list(target_summary))
    write_csv(f"{prefix}_run_rows.csv", run_rows)
    write_csv(f"{prefix}_run_summary.csv", run_summary_rows)
    write_csv(f"{prefix}_basis_summary.csv", transfer_rows)
    write_csv(f"{prefix}_basis_ranking.csv", ranking_rows)

    for path, content in [
        (args.report_md, build_report(target_summary, run_summary_rows, transfer_rows, ranking_rows)),
        (args.lay_md, build_lay_summary(ranking_rows)),
        (args.recommendation_md, build_recommendation(ranking_rows)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v12d] done")


if __name__ == "__main__":
    main()
