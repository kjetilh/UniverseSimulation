#!/usr/bin/env python3
"""v0.13b cross-regime quasi-invariant test around the frozen band_zero_del regime.

This follows v0.13. The point is not to widen the frontier again. The point is
to test whether the most interesting slow-drift signals survive small local
regime changes, or whether they were only anchor-regime artifacts.
"""
from __future__ import annotations

import argparse
import math
import random
import statistics
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12
import relational_universe_v13_geometry_signal_validation as v13


ANCHOR_REGIME = "band_zero_del"
DRIFT_METRICS = [
    "mean_abs_delta_nodes_rel",
    "mean_abs_delta_beta1_rel",
    "mean_abs_delta_spectral_radius_rel",
    "mean_abs_delta_dim_proxy_rel",
    "mean_abs_delta_triangles_rel",
    "mean_abs_delta_clustering_rel",
    "mean_abs_delta_tokens_rel",
]


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v12.mean_defined(values)


def quantile(values: Sequence[float], q: float) -> float:
    return v10b.quantile(values, q)


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
            "candidate": v09.ScaleCandidate("band_death_0005", 0.02, 0.005, 0.02, 0.00, 0.00),
            "axis_group": "death",
        },
    ]


def candidate_meta() -> Dict[str, Dict[str, Any]]:
    return {spec["candidate"].name: spec for spec in candidate_specs()}


def grouped_candidate_base_rows(
    base_rows: Sequence[Dict[str, Any]],
    run_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    base_lookup = {(str(r["ensemble"]), int(r["growth_seed"])): dict(r) for r in base_rows}
    by_key: Dict[Tuple[str, str, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        by_key.setdefault(
            (str(row["candidate_name"]), str(row["ensemble"]), int(row["growth_seed"])),
            [],
        ).append(dict(row))

    out: List[Dict[str, Any]] = []
    for (candidate_name, ensemble, growth_seed), sub in sorted(by_key.items()):
        base = base_lookup[(ensemble, growth_seed)]
        row: Dict[str, Any] = {
            "candidate_name": candidate_name,
            "ensemble": ensemble,
            "target_nodes": int(base["target_nodes"]),
            "growth_seed": int(growth_seed),
            "runs": len(sub),
            "mean_final_radius_control": mean_defined(safe_float(r["final_radius_control"]) for r in sub),
            "mean_avg_local_overlap": mean_defined(safe_float(r["avg_local_overlap"]) for r in sub),
            "mean_fit_speed_control": mean_defined(safe_float(r["fit_speed_control"]) for r in sub),
        }
        for feature in v13.STABILITY_FEATURES:
            row[feature] = safe_float(base[feature])
        for metric in DRIFT_METRICS:
            source = metric.replace("mean_", "")
            row[metric] = mean_defined(safe_float(r[source]) for r in sub)
        out.append(row)
    return out


def resample_regime_target_rows(rows: Sequence[Dict[str, Any]], rng: random.Random) -> List[Dict[str, Any]]:
    by_key: Dict[Tuple[str, int], List[Dict[str, Any]]] = {}
    for row in rows:
        by_key.setdefault((str(row["candidate_name"]), int(row["target_nodes"])), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for key in sorted(by_key):
        sub = by_key[key]
        out.extend(dict(rng.choice(sub)) for _ in range(len(sub)))
    return out


def stable_control_summary(base_rows: Sequence[Dict[str, Any]], bootstrap_reps: int, seed: int) -> List[Dict[str, Any]]:
    _, summary = v13.feature_stability_bootstrap_summary(base_rows, bootstrap_reps, seed)
    return summary


def regime_run_summary(
    candidate_base_rows: Sequence[Dict[str, Any]],
    meta: Mapping[str, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    by_key: Dict[Tuple[str, int], List[Dict[str, Any]]] = {}
    for row in candidate_base_rows:
        by_key.setdefault((str(row["candidate_name"]), int(row["target_nodes"])), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for (candidate_name, target_nodes), sub in sorted(by_key.items()):
        out.append(
            {
                "candidate_name": candidate_name,
                "axis_group": meta[candidate_name]["axis_group"],
                "target_nodes": target_nodes,
                "bases": len(sub),
                "mean_final_radius_control": mean_defined(safe_float(r["mean_final_radius_control"]) for r in sub),
                "mean_avg_local_overlap": mean_defined(safe_float(r["mean_avg_local_overlap"]) for r in sub),
                "mean_fit_speed_control": mean_defined(safe_float(r["mean_fit_speed_control"]) for r in sub),
            }
        )
    return out


def regime_drift_bootstrap_summary(
    candidate_base_rows: Sequence[Dict[str, Any]],
    meta: Mapping[str, Dict[str, Any]],
    bootstrap_reps: int,
    seed: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    rng = random.Random(seed)
    boot_rows: List[Dict[str, Any]] = []
    candidates = sorted({str(r["candidate_name"]) for r in candidate_base_rows})
    for rep in range(1, bootstrap_reps + 1):
        sample = resample_regime_target_rows(candidate_base_rows, rng)
        for candidate_name in candidates:
            sub = [r for r in sample if str(r["candidate_name"]) == candidate_name]
            ranked: List[Tuple[str, float]] = []
            for metric in DRIFT_METRICS:
                vals = [safe_float(r[metric]) for r in sub]
                ranked.append((metric, statistics.mean(vals) if vals else float("nan")))
            ranked.sort(key=lambda item: item[1])
            rank_map = {metric: idx for idx, (metric, _) in enumerate(ranked, start=1)}
            for metric, mean_v in ranked:
                boot_rows.append(
                    {
                        "bootstrap_rep": rep,
                        "candidate_name": candidate_name,
                        "axis_group": meta[candidate_name]["axis_group"],
                        "metric": metric,
                        "mean_relative_drift": mean_v,
                        "rank": rank_map[metric],
                        "is_top3": int(rank_map[metric] <= 3),
                    }
                )

    summary: List[Dict[str, Any]] = []
    for candidate_name in candidates:
        for metric in DRIFT_METRICS:
            sub = [
                r for r in boot_rows
                if str(r["candidate_name"]) == candidate_name and str(r["metric"]) == metric
            ]
            drifts = [safe_float(r["mean_relative_drift"]) for r in sub]
            ranks = [int(r["rank"]) for r in sub]
            summary.append(
                {
                    "candidate_name": candidate_name,
                    "axis_group": meta[candidate_name]["axis_group"],
                    "metric": metric,
                    "bootstrap_mean_relative_drift": statistics.mean(drifts) if drifts else float("nan"),
                    "bootstrap_q10_relative_drift": quantile(drifts, 0.10),
                    "bootstrap_q90_relative_drift": quantile(drifts, 0.90),
                    "bootstrap_mean_rank": statistics.mean(ranks) if ranks else float("nan"),
                    "top3_prob": mean_defined(int(r["is_top3"]) for r in sub),
                }
            )
    summary.sort(
        key=lambda row: (
            str(row["candidate_name"]),
            safe_float(row["bootstrap_mean_relative_drift"], float("inf")),
        )
    )
    return boot_rows, summary


def anchor_delta_summary(
    candidate_base_rows: Sequence[Dict[str, Any]],
    meta: Mapping[str, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    anchor_lookup = {
        (str(r["ensemble"]), int(r["growth_seed"])): dict(r)
        for r in candidate_base_rows
        if str(r["candidate_name"]) == ANCHOR_REGIME
    }
    out: List[Dict[str, Any]] = []
    candidates = sorted({str(r["candidate_name"]) for r in candidate_base_rows if str(r["candidate_name"]) != ANCHOR_REGIME})
    for candidate_name in candidates:
        sub = [r for r in candidate_base_rows if str(r["candidate_name"]) == candidate_name]
        for metric in DRIFT_METRICS:
            deltas: List[float] = []
            off_greater = 0.0
            anchor_greater = 0.0
            same = 0.0
            total = 0
            for row in sub:
                key = (str(row["ensemble"]), int(row["growth_seed"]))
                anchor = anchor_lookup[key]
                off_val = safe_float(row[metric])
                anchor_val = safe_float(anchor[metric])
                delta = off_val - anchor_val
                deltas.append(delta)
                total += 1
                if off_val > anchor_val:
                    off_greater += 1.0
                elif off_val < anchor_val:
                    anchor_greater += 1.0
                else:
                    same += 1.0
            out.append(
                {
                    "candidate_name": candidate_name,
                    "axis_group": meta[candidate_name]["axis_group"],
                    "metric": metric,
                    "mean_delta_vs_anchor": statistics.mean(deltas) if deltas else float("nan"),
                    "q10_delta_vs_anchor": quantile(deltas, 0.10),
                    "q90_delta_vs_anchor": quantile(deltas, 0.90),
                    "p_off_gt_anchor": (off_greater / total) if total else float("nan"),
                    "p_anchor_gt_off": (anchor_greater / total) if total else float("nan"),
                    "same_value_rate": (same / total) if total else float("nan"),
                }
            )
    out.sort(
        key=lambda row: (
            str(row["candidate_name"]),
            abs(safe_float(row["mean_delta_vs_anchor"])),
        )
    )
    return out


def recommendation_rows(
    drift_summary_rows: Sequence[Dict[str, Any]],
    delta_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    zero_metrics = ["mean_abs_delta_nodes_rel", "mean_abs_delta_beta1_rel"]
    zero_rows = [r for r in delta_rows if str(r["metric"]) in zero_metrics]
    exact_holds = all(abs(safe_float(r["mean_delta_vs_anchor"])) <= 1e-12 and safe_float(r["same_value_rate"]) >= 0.999 for r in zero_rows)
    out.append(
        {
            "signal_family": "exact_zero_drifts",
            "status": "holds_local_family" if exact_holds else "breaks_off_anchor",
            "best_candidate": "mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel",
            "note": (
                "De eksakte null-driftene holder også under små lokale regimeavvik. Det gjør dem mer interessante, men fortsatt ikke automatisk til dyp ny matematikk."
                if exact_holds
                else "De eksakte null-driftene bryter når vi forlater ankerregimet, og bør derfor leses som regime-/koblingsartefakter."
            ),
        }
    )

    spectral_rows = [r for r in drift_summary_rows if str(r["metric"]) == "mean_abs_delta_spectral_radius_rel"]
    spectral_top3_all = all(safe_float(r["top3_prob"]) >= 0.95 for r in spectral_rows)
    spectral_deltas = [r for r in delta_rows if str(r["metric"]) == "mean_abs_delta_spectral_radius_rel"]
    max_abs_delta = max(abs(safe_float(r["mean_delta_vs_anchor"])) for r in spectral_deltas) if spectral_deltas else float("inf")
    if spectral_top3_all and max_abs_delta <= 0.01:
        status = "promote"
        note = "Den relative spektraldriften holder seg lav og top-3 gjennom hele den lokale regimefamilien."
    elif spectral_top3_all and max_abs_delta <= 0.03:
        status = "watch"
        note = "Den relative spektraldriften overlever lokal regimeflytting, men med nok inflasjon til at større validering ikke er førsteprioritet ennå."
    else:
        status = "weak"
        note = "Den relative spektraldriften er ikke robust nok på tvers av regimer til å bære neste store valideringssteg alene."
    out.append(
        {
            "signal_family": "spectral_quasi_invariant",
            "status": status,
            "best_candidate": "mean_abs_delta_spectral_radius_rel",
            "note": note,
        }
    )

    if status == "promote":
        validation_status = "yes_targeted"
        validation_note = "Et større valideringssett er mest naturlig for spektral quasi-invariant-testing, ikke for nye basis/workflow-runder."
    else:
        validation_status = "not_yet"
        validation_note = "Ikke bruk større valideringssett som førsteprioritet ennå; kryssregimebildet er fortsatt for lokalt eller for uklart."
    out.append(
        {
            "signal_family": "larger_validation_set",
            "status": validation_status,
            "best_candidate": "spectral_quasi_invariant_cross_regime",
            "note": validation_note,
        }
    )
    return out


def build_report(
    target_summary: Sequence[Dict[str, Any]],
    stable_rows: Sequence[Dict[str, Any]],
    run_summary_rows: Sequence[Dict[str, Any]],
    drift_summary_rows: Sequence[Dict[str, Any]],
    delta_rows: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.13b: kryssregime-test av quasi-invarianter")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester om de viktigste langsomme driftssignalene fra v0.13 holder når vi åpner små lokale triad-, delete- og death-avvik rundt `band_zero_del`."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean_initial | q10 | q90 | separated_from_prev |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {safe_float(row['mean_initial_nodes']):.1f} | {safe_float(row['q10_initial_nodes']):.1f} | {safe_float(row['q90_initial_nodes']):.1f} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Stabile kontrollakser fra v0.13")
    lines.append("")
    lines.append("| rank | feature | mean_cv | q90_cv | slope_q10 | slope_q90 |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in stable_rows[:4]:
        lines.append(
            f"| {int(row['rank'])} | {row['feature']} | {safe_float(row['bootstrap_mean_cv']):.3f} | "
            f"{safe_float(row['bootstrap_q90_mean_cv']):.3f} | {safe_float(row['bootstrap_q10_slope']):.3f} | {safe_float(row['bootstrap_q90_slope']):.3f} |"
        )
    lines.append("")
    lines.append("## Regimeutfall per størrelse")
    lines.append("")
    lines.append("| regime | axis | target | radius | overlap | fit_speed |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in run_summary_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['axis_group']} | {int(row['target_nodes'])} | {safe_float(row['mean_final_radius_control']):.3f} | "
            f"{safe_float(row['mean_avg_local_overlap']):.3f} | {safe_float(row['mean_fit_speed_control']):.3f} |"
        )
    lines.append("")
    lines.append("## Drift-rangering per regime")
    lines.append("")
    lines.append("| regime | axis | metric | mean_rel_drift | q10 | q90 | top3_prob |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in drift_summary_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['axis_group']} | {row['metric']} | {safe_float(row['bootstrap_mean_relative_drift']):.4f} | "
            f"{safe_float(row['bootstrap_q10_relative_drift']):.4f} | {safe_float(row['bootstrap_q90_relative_drift']):.4f} | {safe_float(row['top3_prob']):.3f} |"
        )
    lines.append("")
    lines.append("## Off-anchor mot anker")
    lines.append("")
    lines.append("| regime | axis | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in delta_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['axis_group']} | {row['metric']} | {safe_float(row['mean_delta_vs_anchor']):.4f} | "
            f"{safe_float(row['q10_delta_vs_anchor']):.4f} | {safe_float(row['q90_delta_vs_anchor']):.4f} | "
            f"{safe_float(row['p_off_gt_anchor']):.3f} | {safe_float(row['same_value_rate']):.3f} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    lines.append("| signal_family | status | best_candidate | note |")
    lines.append("| --- | --- | --- | --- |")
    for row in recommendation:
        lines.append(
            f"| {row['signal_family']} | {row['status']} | {row['best_candidate']} | {row['note']} |"
        )
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en dynamikk-/robusthetrunde, ikke en ny frontier-konkurranse.")
    lines.append("- Hvis null-driftene holder også off-anchor, blir de mer interessante, men fortsatt ikke automatisk til ny matematikk uten forklaring.")
    lines.append("- Hvis den relative spektraldriften holder seg lav og top-3 off-anchor, er det vår sterkeste ikke-trivielle quasi-invariant-kandidat så langt.")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    spectral = next((r for r in recommendation if str(r["signal_family"]) == "spectral_quasi_invariant"), None)
    validation = next((r for r in recommendation if str(r["signal_family"]) == "larger_validation_set"), None)
    lines = [
        "# v0.13b for ikke-spesialister",
        "",
        "Denne runden sjekker om de mest lovende tregt-driftende størrelsene holder når vi beveger oss litt bort fra hovedregimet.",
        "",
    ]
    if spectral is not None:
        lines.append(f"- Spektraldriften: `{spectral['status']}`.")
    if validation is not None:
        lines.append(f"- Større valideringssett: `{validation['status']}`.")
    lines.extend(["", "Kort sagt: vi tester om den samme strukturen overlever små lokale regelendringer.", ""])
    return "\n".join(lines)


def build_recommendation(recommendation: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.13b operativ anbefaling", ""]
    for row in recommendation:
        lines.append(f"- {row['signal_family']}: {row['note']}")
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.13b cross-regime quasi-invariant test")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=4)
    ap.add_argument("--run-seeds", type=int, default=4)
    ap.add_argument("--bootstrap-reps", type=int, default=160)
    ap.add_argument("--output-prefix", default="Documentation/v13b")
    ap.add_argument("--report-md", default="Documentation/v13b_cross_regime_quasiinvariant_test.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_13b.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_13b_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    specs = candidate_specs()
    candidates = [spec["candidate"] for spec in specs]
    meta = candidate_meta()
    growth_seeds = [47001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [20101 + 31 * i for i in range(args.run_seeds)]

    print(
        f"[v13b] regime={regime.name} targets={targets} candidates={[c.name for c in candidates]} "
        f"growth={len(growth_seeds)} runs={len(run_offsets)} boot={args.bootstrap_reps}"
    )
    print("[v13b] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    base_lookup = {(str(r["ensemble"]), int(r["growth_seed"])): dict(r) for r in base_rows}
    print("[v13b] bases done")

    print("[v13b] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    run_rows = [v12.enrich_run_row(row, base_lookup) for row in raw_run_rows]
    print(f"[v13b] runs done: {len(run_rows)} rows")

    print("[v13b] aggregating candidate/base rows...")
    candidate_base_rows = grouped_candidate_base_rows(base_rows, run_rows)
    stable_rows = stable_control_summary(base_rows, args.bootstrap_reps, seed=23001)
    run_summary_rows = regime_run_summary(candidate_base_rows, meta)
    print("[v13b] bootstrap: drift stability per regime...")
    drift_boot_rows, drift_summary_rows = regime_drift_bootstrap_summary(candidate_base_rows, meta, args.bootstrap_reps, seed=23041)
    print("[v13b] comparing off-anchor regimes to anchor...")
    delta_rows = anchor_delta_summary(candidate_base_rows, meta)
    recommendation = recommendation_rows(drift_summary_rows, delta_rows)

    print("[v13b] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_cross_regime_base_rows.csv", candidate_base_rows)
    write_csv(f"{prefix}_cross_regime_target_summary.csv", list(target_summary))
    write_csv(f"{prefix}_cross_regime_run_summary.csv", run_summary_rows)
    write_csv(f"{prefix}_cross_regime_drift_bootstrap_rows.csv", drift_boot_rows)
    write_csv(f"{prefix}_cross_regime_drift_summary.csv", drift_summary_rows)
    write_csv(f"{prefix}_cross_regime_anchor_delta_summary.csv", delta_rows)
    write_csv(f"{prefix}_cross_regime_recommendations.csv", recommendation)

    for path, content in [
        (args.report_md, build_report(target_summary, stable_rows, run_summary_rows, drift_summary_rows, delta_rows, recommendation)),
        (args.lay_md, build_lay_summary(recommendation)),
        (args.recommendation_md, build_recommendation(recommendation)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v13b] done")


if __name__ == "__main__":
    main()
