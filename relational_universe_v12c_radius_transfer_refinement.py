#!/usr/bin/env python3
"""v0.12c radius-transfer refinement around the frozen band_zero_del regime.

This is a narrow follow-up to v0.12b. It keeps the model, generator, and
feature machinery fixed, and asks one sharper question:

Which small geometric basis carries the most robust off-anchor signal for
`final_radius_control` across nearby local triad variants?
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v11d_local_triad_refinement as v11d
import relational_universe_v12_geometry_invariant_lab as v12


ANCHOR_REGIME = "band_zero_del"
TARGET_METRIC = "final_radius_control"
BASIS_SPECS = [
    ("spectral_only", ("initial_spectral_per_sqrtN",)),
    ("clustering_only", ("initial_clustering",)),
    ("dim_only", ("initial_dim_proxy",)),
    ("spectral_plus_clustering", ("initial_spectral_per_sqrtN", "initial_clustering")),
    ("spectral_plus_dim", ("initial_spectral_per_sqrtN", "initial_dim_proxy")),
    ("clustering_plus_dim", ("initial_clustering", "initial_dim_proxy")),
    ("full_basis", tuple(v12.BASIS_FEATURES)),
]


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v12.write_csv(path, rows)


def transfer_candidates() -> List[Any]:
    return [
        v11d.named_candidate("band_zero_del", 0.0000),
        v11d.named_candidate("bridge_0005_0000", 0.0005),
        v11d.named_candidate("bridge_00075_0000", 0.00075),
        v11d.named_candidate("bridge_0010_0000", 0.0010),
        v11d.named_candidate("bridge_00125_0000", 0.00125),
        v11d.named_candidate("bridge_0015_0000", 0.0015),
    ]


def summarize_regime_target_runs(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_key: Dict[tuple[str, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        by_key.setdefault((str(row["candidate_name"]), int(row["target_nodes"])), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for (name, target), sub in sorted(by_key.items()):
        out.append(
            {
                "candidate_name": name,
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


def transfer_summary(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    train_rows = [r for r in run_rows if str(r["candidate_name"]) == ANCHOR_REGIME]
    test_regimes = sorted({str(r["candidate_name"]) for r in run_rows})
    out: List[Dict[str, Any]] = []
    for regime in test_regimes:
        test_rows = [r for r in run_rows if str(r["candidate_name"]) == regime]
        for basis_name, features in BASIS_SPECS:
            stats = evaluate_basis(train_rows, test_rows, features, TARGET_METRIC)
            out.append(
                {
                    "target_metric": TARGET_METRIC,
                    "train_regime": ANCHOR_REGIME,
                    "test_regime": regime,
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
        best_row = max(rows, key=lambda r: safe_float(r["relative_skill"], -1e9))
        worst_row = min(rows, key=lambda r: safe_float(r["relative_skill"], 1e9))
        out.append(
            {
                "basis_name": name,
                "basis_features": rows[0]["basis_features"] if rows else "",
                "feature_count": int(rows[0]["feature_count"]) if rows else 0,
                "anchor_skill": safe_float(anchor_row["relative_skill"]) if anchor_row else float("nan"),
                "mean_off_anchor_skill": v12.mean_defined(skills),
                "min_off_anchor_skill": min(skills) if skills else float("nan"),
                "max_off_anchor_skill": max(skills) if skills else float("nan"),
                "positive_off_anchor_regimes": sum(1 for v in skills if math.isfinite(v) and v > 0.0),
                "off_anchor_regimes": len(skills),
                "best_test_regime": str(best_row["test_regime"]),
                "best_test_skill": safe_float(best_row["relative_skill"]),
                "worst_test_regime": str(worst_row["test_regime"]),
                "worst_test_skill": safe_float(worst_row["relative_skill"]),
            }
        )
    out.sort(
        key=lambda row: (
            safe_float(row["mean_off_anchor_skill"], -1e9),
            safe_float(row["min_off_anchor_skill"], -1e9),
            -int(row["feature_count"]),
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
    lines.append("# Relasjonell universgraf v0.12c: radius-transfer-raffinement")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden holder `band_zero_del` fast og tester bare hvor robust radius-transferen er til nærliggende triad-varianter, og hvilken liten basis som bærer mest av signalet."
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
    lines.append("| regime | target | radius | fit_speed | overlap | rel_drift_triangles |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in run_summary_rows:
        lines.append(
            f"| {row['candidate_name']} | {int(row['target_nodes'])} | {safe_float(row['mean_final_radius_control']):.3f} | "
            f"{safe_float(row['mean_fit_speed_control']):.3f} | {safe_float(row['mean_avg_local_overlap']):.3f} | "
            f"{safe_float(row['mean_abs_delta_triangles_rel']):.3f} |"
        )
    lines.append("")
    lines.append("## Radius-transfer per basis")
    lines.append("")
    lines.append("| test_regime | basis | rmse | baseline_rmse | relative_skill |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in transfer_rows:
        lines.append(
            f"| {row['test_regime']} | {row['basis_name']} | {safe_float(row['cv_rmse']):.4f} | "
            f"{safe_float(row['baseline_rmse']):.4f} | {safe_float(row['relative_skill']):.3f} |"
        )
    lines.append("")
    lines.append("## Off-anchor basis-ranking")
    lines.append("")
    lines.append("| rank | basis | mean_off_anchor_skill | min_off_anchor_skill | positive_regimes | best_test | worst_test |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in ranking_rows:
        lines.append(
            f"| {int(row['rank'])} | {row['basis_name']} | {safe_float(row['mean_off_anchor_skill']):.3f} | "
            f"{safe_float(row['min_off_anchor_skill']):.3f} | {int(row['positive_off_anchor_regimes'])}/{int(row['off_anchor_regimes'])} | "
            f"{row['best_test_regime']} ({safe_float(row['best_test_skill']):.3f}) | {row['worst_test_regime']} ({safe_float(row['worst_test_skill']):.3f}) |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    best = ranking_rows[0] if ranking_rows else None
    worst_regime = ""
    negative_everywhere = False
    off_anchor_by_regime: Dict[str, List[float]] = {}
    for row in transfer_rows:
        regime = str(row["test_regime"])
        if regime == ANCHOR_REGIME:
            continue
        off_anchor_by_regime.setdefault(regime, []).append(safe_float(row["relative_skill"]))
    if off_anchor_by_regime:
        shared_worst = min(
            off_anchor_by_regime,
            key=lambda regime: v12.mean_defined(off_anchor_by_regime[regime]),
        )
        worst_regime = shared_worst
        negative_everywhere = all(v < 0.0 for v in off_anchor_by_regime[shared_worst] if math.isfinite(v))
    if best is not None:
        lines.append(
            f"- Den sterkeste off-anchor radius-basen i denne runden er `{best['basis_name']}` med mean off-anchor skill `{safe_float(best['mean_off_anchor_skill']):.3f}` og worst-case `{safe_float(best['min_off_anchor_skill']):.3f}`."
        )
    if worst_regime:
        if negative_everywhere:
            lines.append(
                f"- Alle de testede basisene blir svakt negative ved `{worst_regime}`. Det tyder mer pa en lokal gyldighetsgrense for radius-surrogatet enn pa en ren rangeringsstoy."
            )
        else:
            lines.append(
                f"- Det svakeste off-anchor-punktet i denne runden er `{worst_regime}`. Det er naturlig a behandle det som ytterkant for den lokale transfer-sonen."
            )
    lines.append("- Hvis en liten basis topper både mean og worst-case off-anchor, er det et bedre tegn på ekte struktur enn om bare anchor-fitten ser god ut.")
    lines.append("- Hvis signalet holder for radius men ikke for overlap, peker det mot en smal geometrisk surrogate heller enn en bred dynamisk erstatning.")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(ranking_rows: Sequence[Dict[str, Any]]) -> str:
    best = ranking_rows[0] if ranking_rows else None
    best_name = best["basis_name"] if best is not None else "ingen klar basis"
    return "\n".join(
        [
            "# v0.12c for ikke-spesialister",
            "",
            "Denne runden sammenligner noen få enkle geometriske oppskrifter for å se hvilken som best forutsier hvor langt en forstyrrelse sprer seg.",
            "",
            f"- Den beste lille oppskriften i denne runden er `{best_name}`.",
            "- Vi bryr oss mest om hvordan den virker utenfor hovedregimet, ikke bare der den ble lært opp.",
            "",
        ]
    )


def build_recommendation(ranking_rows: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.12c operativ anbefaling", ""]
    if not ranking_rows:
        lines.append("Radius-transferen er for svak eller ufullstendig til å gi en operativ anbefaling.")
        lines.append("")
        return "\n".join(lines)
    best = ranking_rows[0]
    second = ranking_rows[1] if len(ranking_rows) > 1 else None
    lines.append(
        f"Fortsett radius-/surrogatesporet med `{best['basis_name']}` som første arbeidsbasis. Den topper off-anchor transfer med mean skill `{safe_float(best['mean_off_anchor_skill']):.3f}` og worst-case `{safe_float(best['min_off_anchor_skill']):.3f}`."
    )
    if second is not None:
        lines.append(
            f"Behold `{second['basis_name']}` som nær kontroll. Hvis disse to holder seg tette i senere runder, har vi trolig et lite plateau av enkle surrogate-baser heller enn én unik vinner."
        )
    if safe_float(best["min_off_anchor_skill"], 0.0) < 0.0:
        lines.append(
            f"Behandle samtidig `bridge_0015_0000`-enden som en lokal grensekontroll: når alle basisene blir svakt negative der, er det et tegn på at radius-transferen fortsatt er lokal og ikke bør overselges."
        )
    lines.append(
        "Hold analysen smal: bruk `final_radius_control` som hovedmål og ikke anta at overlap/repair følger med før repoet faktisk viser det."
    )
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12c radius-transfer refinement")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=4)
    ap.add_argument("--run-seeds", type=int, default=4)
    ap.add_argument("--output-prefix", default="Documentation/v12c_radius")
    ap.add_argument("--report-md", default="Documentation/v12c_radius_transfer_refinement.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12c.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12c_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    candidates = transfer_candidates()
    growth_seeds = [27001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [10101 + 31 * i for i in range(args.run_seeds)]

    print(f"[v12c] regime={regime.name} targets={targets} candidates={[c.name for c in candidates]} growth={len(growth_seeds)} runs={len(run_offsets)}")
    print("[v12c] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    base_lookup = {(str(r['ensemble']), int(r['growth_seed'])): dict(r) for r in base_rows}
    print("[v12c] bases done")

    print("[v12c] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    run_rows = [v12.enrich_run_row(row, base_lookup) for row in raw_run_rows]
    print(f"[v12c] runs done: {len(run_rows)} rows")

    run_summary_rows = summarize_regime_target_runs(run_rows)
    transfer_rows = transfer_summary(run_rows)
    ranking_rows = basis_ranking(transfer_rows)

    print("[v12c] writing outputs...")
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
    print("[v12c] done")


if __name__ == "__main__":
    main()
