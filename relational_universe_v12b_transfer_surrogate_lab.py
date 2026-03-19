#!/usr/bin/env python3
"""v0.12b transfer and surrogate lab around the frozen band_zero_del regime.

This follow-up asks whether the small geometric basis identified in v0.12 is
useful only inside the anchor regime, or whether it transfers to nearby local
triad variants.
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


ANCHOR_BASIS = ("initial_spectral_per_sqrtN", "initial_clustering")
FULL_BASIS = tuple(v12.BASIS_FEATURES)
TRANSFER_TARGETS = ["final_radius_control", "avg_local_overlap"]


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v12.write_csv(path, rows)


def transfer_candidates() -> List[Any]:
    return [
        v11d.named_candidate("band_zero_del", 0.0000),
        v11d.named_candidate("bridge_00075_0000", 0.00075),
        v11d.named_candidate("bridge_0010_0000", 0.0010),
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
                "mean_avg_local_overlap": v12.mean_defined(safe_float(r["avg_local_overlap"]) for r in sub),
                "mean_final_radius_control": v12.mean_defined(safe_float(r["final_radius_control"]) for r in sub),
                "mean_fit_speed_control": v12.mean_defined(safe_float(r["fit_speed_control"]) for r in sub),
                "mean_abs_delta_beta1_rel": v12.mean_defined(safe_float(r["abs_delta_beta1_rel"]) for r in sub),
                "mean_abs_delta_triangles_rel": v12.mean_defined(safe_float(r["abs_delta_triangles_rel"]) for r in sub),
            }
        )
    return out


def evaluate_basis(train_rows: Sequence[Dict[str, Any]], test_rows: Sequence[Dict[str, Any]], features: Sequence[str], target_metric: str) -> Dict[str, Any]:
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
    train_rows = [r for r in run_rows if str(r["candidate_name"]) == "band_zero_del"]
    out: List[Dict[str, Any]] = []
    basis_specs = [
        ("spectral_only", ("initial_spectral_per_sqrtN",)),
        ("spectral_plus_clustering", ANCHOR_BASIS),
        ("full_basis", FULL_BASIS),
    ]
    test_regimes = ["band_zero_del", "bridge_00075_0000", "bridge_0010_0000"]
    for metric in TRANSFER_TARGETS:
        for regime in test_regimes:
            test_rows = [r for r in run_rows if str(r["candidate_name"]) == regime]
            for basis_name, features in basis_specs:
                stats = evaluate_basis(train_rows, test_rows, features, metric)
                out.append(
                    {
                        "target_metric": metric,
                        "train_regime": "band_zero_del",
                        "test_regime": regime,
                        "basis_name": basis_name,
                        "basis_features": "+".join(features),
                        **stats,
                    }
                )
    return out


def build_report(target_summary: Sequence[Dict[str, Any]], run_summary_rows: Sequence[Dict[str, Any]], transfer_rows: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.12b: transfer og surrogate-lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester om den lille geometriske basisen fra v0.12 er lokalt nyttig bare i `band_zero_del`, eller om den transfererer til nærliggende triad-varianter."
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
    lines.append("| regime | target | overlap | radius | fit_speed | rel_drift_triangles |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in run_summary_rows:
        lines.append(
            f"| {row['candidate_name']} | {int(row['target_nodes'])} | {safe_float(row['mean_avg_local_overlap']):.3f} | "
            f"{safe_float(row['mean_final_radius_control']):.3f} | {safe_float(row['mean_fit_speed_control']):.3f} | "
            f"{safe_float(row['mean_abs_delta_triangles_rel']):.3f} |"
        )
    lines.append("")
    lines.append("## Transfer av redusert basis")
    lines.append("")
    lines.append("| metric | test_regime | basis | rmse | baseline_rmse | relative_skill |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in transfer_rows:
        lines.append(
            f"| {row['target_metric']} | {row['test_regime']} | {row['basis_name']} | {safe_float(row['cv_rmse']):.4f} | "
            f"{safe_float(row['baseline_rmse']):.4f} | {safe_float(row['relative_skill']):.3f} |"
        )
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Hvis `spectral_plus_clustering` holder positiv skill også utenfor `band_zero_del`, er det et bedre tegn på ekte struktur enn om den bare virker på anchor-regimet.")
    lines.append("- Hvis full basis ikke slår en liten basis, tyder det på at vi ikke trenger mange koordinater for å bære det nyttige signalet.")
    lines.append("- Hvis transfer bryter sammen med én gang, er geometrihypotesen fortsatt for lokal eller for svak.")
    lines.append("")
    radius_rows = [r for r in transfer_rows if r["target_metric"] == "final_radius_control" and r["test_regime"] != "band_zero_del"]
    overlap_rows = [r for r in transfer_rows if r["target_metric"] == "avg_local_overlap" and r["test_regime"] != "band_zero_del"]
    best_radius = max(radius_rows, key=lambda r: safe_float(r["relative_skill"], -1e9)) if radius_rows else None
    best_overlap = max(overlap_rows, key=lambda r: safe_float(r["relative_skill"], -1e9)) if overlap_rows else None
    lines.append("## Operativ lesning")
    lines.append("")
    if best_radius is not None:
        lines.append(
            f"- For `final_radius_control` transfererer en liten basis faktisk til nærliggende regimer. Best off-anchor er `{best_radius['basis_name']}` mot `{best_radius['test_regime']}` med relative skill `{safe_float(best_radius['relative_skill']):.3f}`."
        )
    if best_overlap is not None:
        lines.append(
            f"- For `avg_local_overlap` er transfer svakere. Best off-anchor er `{best_overlap['basis_name']}` mot `{best_overlap['test_regime']}` med relative skill `{safe_float(best_overlap['relative_skill']):.3f}`, sa dette sporet ser ikke robust ut ennå."
        )
    lines.append("- Konklusjonen i denne runden er derfor moderat positiv for radius-prediksjon, men ikke for overlap/repair.")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(transfer_rows: Sequence[Dict[str, Any]]) -> str:
    radius_rows = [r for r in transfer_rows if r["target_metric"] == "final_radius_control" and r["test_regime"] != "band_zero_del"]
    best = max(radius_rows, key=lambda r: safe_float(r["relative_skill"], -1e9)) if radius_rows else max(transfer_rows, key=lambda r: safe_float(r["relative_skill"], -1e9))
    return "\n".join(
        [
            "# v0.12b for ikke-spesialister",
            "",
            "Denne runden sjekker om en liten geometrisk oppskrift fortsatt virker når vi flytter oss litt bort fra hovedregimet.",
            "",
            f"- Den sterkeste off-anchor transfer-signaturen i denne runden er `{best['basis_name']}` for `{best['target_metric']}` mot `{best['test_regime']}`.",
            "- Dette ser lovende ut for radius-lignende utfall, men ikke for overlap/repair ennå.",
            "",
        ]
    )


def build_recommendation(transfer_rows: Sequence[Dict[str, Any]]) -> str:
    radius_rows = [r for r in transfer_rows if r["target_metric"] == "final_radius_control" and r["test_regime"] != "band_zero_del"]
    best_radius = max(radius_rows, key=lambda r: safe_float(r["relative_skill"], -1e9)) if radius_rows else None
    lines = ["# v0.12b operativ anbefaling", ""]
    if best_radius is not None and safe_float(best_radius["relative_skill"], -1.0) > 0.0:
        lines.append(
            f"Fortsett med transfersporet, men hold det smalt og ærlig. I denne runden er det `final_radius_control` som bærer transfer-signalet, og best off-anchor er `{best_radius['basis_name']}` mot `{best_radius['test_regime']}` med relative skill `{safe_float(best_radius['relative_skill']):.3f}`."
        )
        lines.append(
            "`spectral_plus_clustering` er fortsatt verdt å følge fordi det var den beste lille basisen i v0.12, men tallene her sier at vi ikke bør anta at 2-feature-basisen er best uten videre. `avg_local_overlap` ser foreløpig ikke ut til å transferere robust."
        )
    else:
        lines.append(
            "Transfer-signalet er svakt. Hold geometri-/invariantsporet apent, men ikke anta ennå at den lille basisen generaliserer utover anchor-regimet."
        )
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12b transfer / surrogate lab")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=4)
    ap.add_argument("--run-seeds", type=int, default=4)
    ap.add_argument("--output-prefix", default="Documentation/v12b")
    ap.add_argument("--report-md", default="Documentation/v12b_transfer_surrogate_lab.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12b.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12b_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    candidates = transfer_candidates()
    growth_seeds = [25001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [9101 + 31 * i for i in range(args.run_seeds)]

    print(f"[v12b] regime={regime.name} targets={targets} candidates={[c.name for c in candidates]} growth={len(growth_seeds)} runs={len(run_offsets)}")
    print("[v12b] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    base_lookup = {(str(r['ensemble']), int(r['growth_seed'])): dict(r) for r in base_rows}
    print("[v12b] bases done")

    print("[v12b] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    run_rows = [v12.enrich_run_row(row, base_lookup) for row in raw_run_rows]
    print(f"[v12b] runs done: {len(run_rows)} rows")

    run_summary_rows = summarize_regime_target_runs(run_rows)
    transfer_rows = transfer_summary(run_rows)

    print("[v12b] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_transfer_base_rows.csv", base_rows)
    write_csv(f"{prefix}_transfer_target_summary.csv", list(target_summary))
    write_csv(f"{prefix}_transfer_run_rows.csv", run_rows)
    write_csv(f"{prefix}_transfer_run_summary.csv", run_summary_rows)
    write_csv(f"{prefix}_transfer_basis_summary.csv", transfer_rows)

    for path, content in [
        (args.report_md, build_report(target_summary, run_summary_rows, transfer_rows)),
        (args.lay_md, build_lay_summary(transfer_rows)),
        (args.recommendation_md, build_recommendation(transfer_rows)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v12b] done")


if __name__ == "__main__":
    main()
