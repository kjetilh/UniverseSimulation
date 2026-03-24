#!/usr/bin/env python3
"""v0.13c targeted validation of the spectral quasi-invariant signal.

This follows v0.13b. It scales up only the signal that survived the local
cross-regime test:

- mean_abs_delta_spectral_radius_rel

The goal is not a broad new scan. The goal is to test whether the spectral
quasi-invariant remains the best non-trivial low-drift signal when we use a
slightly larger local regime family and a slightly larger validation budget.
"""
from __future__ import annotations

import argparse
import random
import statistics
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12
import relational_universe_v13_geometry_signal_validation as v13
import relational_universe_v13b_cross_regime_quasiinvariant_test as v13b


ANCHOR_REGIME = "band_zero_del"
SPECTRAL_METRIC = "mean_abs_delta_spectral_radius_rel"
DIM_METRIC = "mean_abs_delta_dim_proxy_rel"
ZERO_SANITY_METRICS = [
    "mean_abs_delta_nodes_rel",
    "mean_abs_delta_beta1_rel",
]
FOCUS_METRICS = [
    SPECTRAL_METRIC,
    DIM_METRIC,
    *ZERO_SANITY_METRICS,
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
            "candidate": v09.ScaleCandidate("bridge_0005_0000", 0.02, 0.00, 0.02, 0.00050, 0.00),
            "axis_group": "triad",
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


def candidate_meta() -> Dict[str, Dict[str, Any]]:
    return {spec["candidate"].name: spec for spec in candidate_specs()}


def focus_bootstrap_summary(
    candidate_base_rows: Sequence[Dict[str, Any]],
    meta: Mapping[str, Dict[str, Any]],
    bootstrap_reps: int,
    seed: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    rng = random.Random(seed)
    boot_rows: List[Dict[str, Any]] = []
    candidates = sorted({str(r["candidate_name"]) for r in candidate_base_rows})
    for rep in range(1, bootstrap_reps + 1):
        sample = v13b.resample_regime_target_rows(candidate_base_rows, rng)
        for candidate_name in candidates:
            sub = [r for r in sample if str(r["candidate_name"]) == candidate_name]
            ranked = []
            for metric in FOCUS_METRICS:
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
                        "rank_within_focus": rank_map[metric],
                        "is_best_nontrivial": int(metric == SPECTRAL_METRIC and rank_map[metric] == 3),
                    }
                )

    summary: List[Dict[str, Any]] = []
    for candidate_name in candidates:
        for metric in FOCUS_METRICS:
            sub = [
                r for r in boot_rows
                if str(r["candidate_name"]) == candidate_name and str(r["metric"]) == metric
            ]
            drifts = [safe_float(r["mean_relative_drift"]) for r in sub]
            ranks = [int(r["rank_within_focus"]) for r in sub]
            summary.append(
                {
                    "candidate_name": candidate_name,
                    "axis_group": meta[candidate_name]["axis_group"],
                    "metric": metric,
                    "bootstrap_mean_relative_drift": statistics.mean(drifts) if drifts else float("nan"),
                    "bootstrap_q10_relative_drift": quantile(drifts, 0.10),
                    "bootstrap_q90_relative_drift": quantile(drifts, 0.90),
                    "bootstrap_mean_rank_within_focus": statistics.mean(ranks) if ranks else float("nan"),
                    "top2_prob": mean_defined(float(r <= 2) for r in ranks),
                    "top3_prob": mean_defined(float(r <= 3) for r in ranks),
                }
            )
    summary.sort(key=lambda row: (str(row["candidate_name"]), safe_float(row["bootstrap_mean_relative_drift"], float("inf"))))
    return boot_rows, summary


def spectral_dim_pairwise_summary(candidate_base_rows: Sequence[Dict[str, Any]], meta: Mapping[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_candidate: Dict[str, List[Dict[str, Any]]] = {}
    for row in candidate_base_rows:
        by_candidate.setdefault(str(row["candidate_name"]), []).append(dict(row))

    out: List[Dict[str, Any]] = []
    for candidate_name, sub in sorted(by_candidate.items()):
        spectral_better = 0.0
        dim_better = 0.0
        total = 0
        margins: List[float] = []
        for row in sub:
            spectral = safe_float(row[SPECTRAL_METRIC])
            dim = safe_float(row[DIM_METRIC])
            total += 1
            margins.append(dim - spectral)
            if spectral < dim:
                spectral_better += 1.0
            elif dim < spectral:
                dim_better += 1.0
            else:
                spectral_better += 0.5
                dim_better += 0.5
        out.append(
            {
                "candidate_name": candidate_name,
                "axis_group": meta[candidate_name]["axis_group"],
                "p_spectral_lt_dim": (spectral_better / total) if total else float("nan"),
                "p_dim_lt_spectral": (dim_better / total) if total else float("nan"),
                "mean_dim_minus_spectral": statistics.mean(margins) if margins else float("nan"),
                "q10_dim_minus_spectral": quantile(margins, 0.10),
                "q90_dim_minus_spectral": quantile(margins, 0.90),
            }
        )
    return out


def anchor_focus_delta_summary(
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
        for metric in FOCUS_METRICS:
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
                deltas.append(off_val - anchor_val)
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
    out.sort(key=lambda row: (str(row["metric"]), abs(safe_float(row["mean_delta_vs_anchor"]))))
    return out


def recommendation_rows(
    focus_summary_rows: Sequence[Dict[str, Any]],
    pairwise_rows: Sequence[Dict[str, Any]],
    delta_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    zero_rows = [r for r in delta_rows if str(r["metric"]) in ZERO_SANITY_METRICS]
    zero_breaks = any(abs(safe_float(r["mean_delta_vs_anchor"])) > 1e-12 or safe_float(r["same_value_rate"]) < 0.999 for r in zero_rows)
    out.append(
        {
            "signal_family": "zero_drift_sanity",
            "status": "breaks_off_anchor" if zero_breaks else "still_exact",
            "best_candidate": "mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel",
            "note": (
                "Null-driftene bryter fortsatt off-anchor og skal behandles som artefakter, ikke lover."
                if zero_breaks
                else "Null-driftene holder fortsatt eksakt i denne større runden."
            ),
        }
    )

    spectral_rows = [r for r in focus_summary_rows if str(r["metric"]) == SPECTRAL_METRIC]
    spectral_top3_all = all(safe_float(r["top3_prob"]) >= 0.95 for r in spectral_rows)
    spectral_anchor_deltas = [r for r in delta_rows if str(r["metric"]) == SPECTRAL_METRIC]
    max_abs_delta = max(abs(safe_float(r["mean_delta_vs_anchor"])) for r in spectral_anchor_deltas) if spectral_anchor_deltas else float("inf")
    pairwise_ok = all(safe_float(r["p_spectral_lt_dim"]) >= 0.70 for r in pairwise_rows)
    if spectral_top3_all and pairwise_ok and max_abs_delta <= 0.02:
        status = "strong"
        note = "Spektraldriften holder seg lav, slår `dim_proxy` i alle regimer, og inflasjonen off-anchor er fortsatt moderat."
    elif spectral_top3_all and pairwise_ok:
        status = "good_but_local"
        note = "Spektraldriften holder fortsatt, men off-anchor-inflasjonen er stor nok til at vi fortsatt bør kalle signalet lokalt."
    else:
        status = "mixed"
        note = "Spektraldriften er fortsatt interessant, men ikke sterk nok til å stå alene som neste store valideringsmål."
    out.append(
        {
            "signal_family": "spectral_quasi_invariant",
            "status": status,
            "best_candidate": SPECTRAL_METRIC,
            "note": note,
        }
    )

    if status in {"strong", "good_but_local"}:
        validation_status = "yes_targeted"
        validation_note = "Neste større valideringssett bør brukes på spektral quasi-invariant-testing med `dim_proxy` som sekundær kontroll."
    else:
        validation_status = "not_yet"
        validation_note = "Vent med større valideringssett til spektralsporet er skarpere eller bredere testet."
    out.append(
        {
            "signal_family": "larger_validation_set",
            "status": validation_status,
            "best_candidate": "spectral_vs_dim_cross_regime",
            "note": validation_note,
        }
    )
    return out


def build_report(
    target_summary: Sequence[Dict[str, Any]],
    stable_rows: Sequence[Dict[str, Any]],
    run_summary_rows: Sequence[Dict[str, Any]],
    focus_summary_rows: Sequence[Dict[str, Any]],
    pairwise_rows: Sequence[Dict[str, Any]],
    delta_rows: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.13c: målrettet validering av spektral quasi-invariant")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden skalerer bare opp ett spor: `mean_abs_delta_spectral_radius_rel`. `dim_proxy` holdes som sekundær kontroll, og de gamle null-driftene holdes bare som sanity check."
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
    lines.append("## Stabile kontrollakser")
    lines.append("")
    lines.append("| rank | feature | mean_cv | q90_cv |")
    lines.append("| --- | --- | --- | --- |")
    for row in stable_rows[:3]:
        lines.append(
            f"| {int(row['rank'])} | {row['feature']} | {safe_float(row['bootstrap_mean_cv']):.3f} | {safe_float(row['bootstrap_q90_mean_cv']):.3f} |"
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
    lines.append("## Fokusdrift per regime")
    lines.append("")
    lines.append("| regime | axis | metric | mean_rel_drift | q10 | q90 | top2_prob |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in focus_summary_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['axis_group']} | {row['metric']} | {safe_float(row['bootstrap_mean_relative_drift']):.4f} | "
            f"{safe_float(row['bootstrap_q10_relative_drift']):.4f} | {safe_float(row['bootstrap_q90_relative_drift']):.4f} | {safe_float(row['top2_prob']):.3f} |"
        )
    lines.append("")
    lines.append("## Spektral mot dim")
    lines.append("")
    lines.append("| regime | axis | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in pairwise_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['axis_group']} | {safe_float(row['p_spectral_lt_dim']):.3f} | "
            f"{safe_float(row['mean_dim_minus_spectral']):.4f} | {safe_float(row['q10_dim_minus_spectral']):.4f} | {safe_float(row['q90_dim_minus_spectral']):.4f} |"
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
        lines.append(f"| {row['signal_family']} | {row['status']} | {row['best_candidate']} | {row['note']} |")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Denne runden er en målrettet validering, ikke en ny bred struktur-scan.")
    lines.append("- Hvis `spectral_radius_rel` fortsatt holder under et litt større og bredere lokalt regime-sett, er det det sterkeste ikke-trivielle sporet vi har nå.")
    lines.append("- Hvis `dim_proxy` holder nesten like godt eller null-driftene plutselig blir eksakte igjen, må lesningen dempes igjen.")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    spectral = next((r for r in recommendation if str(r["signal_family"]) == "spectral_quasi_invariant"), None)
    validation = next((r for r in recommendation if str(r["signal_family"]) == "larger_validation_set"), None)
    lines = [
        "# v0.13c for ikke-spesialister",
        "",
        "Denne runden bruker litt mer budsjett på ett bestemt spor: om den spektrale driften virkelig er det mest robuste ikke-trivielle mønsteret vårt.",
        "",
    ]
    if spectral is not None:
        lines.append(f"- Spektralsporet: `{spectral['status']}`.")
    if validation is not None:
        lines.append(f"- Større valideringssett: `{validation['status']}`.")
    lines.extend(["", "Poenget er å bruke mer data bare der det faktisk ser ut til å være noe å hente.", ""])
    return "\n".join(lines)


def build_recommendation(recommendation: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.13c operativ anbefaling", ""]
    for row in recommendation:
        lines.append(f"- {row['signal_family']}: {row['note']}")
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.13c targeted spectral quasi-invariant validation")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=5)
    ap.add_argument("--run-seeds", type=int, default=5)
    ap.add_argument("--bootstrap-reps", type=int, default=200)
    ap.add_argument("--output-prefix", default="Documentation/v13c")
    ap.add_argument("--report-md", default="Documentation/v13c_spectral_quasiinvariant_validation.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_13c.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_13c_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    specs = candidate_specs()
    candidates = [spec["candidate"] for spec in specs]
    meta = candidate_meta()
    growth_seeds = [52001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [24001 + 31 * i for i in range(args.run_seeds)]

    print(
        f"[v13c] regime={regime.name} targets={targets} candidates={[c.name for c in candidates]} "
        f"growth={len(growth_seeds)} runs={len(run_offsets)} boot={args.bootstrap_reps}"
    )
    print("[v13c] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    base_lookup = {(str(r['ensemble']), int(r['growth_seed'])): dict(r) for r in base_rows}
    print("[v13c] bases done")

    print("[v13c] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    run_rows = [v12.enrich_run_row(row, base_lookup) for row in raw_run_rows]
    print(f"[v13c] runs done: {len(run_rows)} rows")

    print("[v13c] aggregating candidate/base rows...")
    candidate_base_rows = v13b.grouped_candidate_base_rows(base_rows, run_rows)
    stable_rows = v13.stable_control_summary(base_rows, args.bootstrap_reps, seed=27001) if hasattr(v13, "stable_control_summary") else v13.feature_stability_bootstrap_summary(base_rows, args.bootstrap_reps, 27001)[1]
    run_summary_rows = v13b.regime_run_summary(candidate_base_rows, meta)
    print("[v13c] bootstrap: focus drift summary...")
    focus_boot_rows, focus_summary_rows = focus_bootstrap_summary(candidate_base_rows, meta, args.bootstrap_reps, seed=27041)
    print("[v13c] paired spectral-vs-dim comparison...")
    pairwise_rows = spectral_dim_pairwise_summary(candidate_base_rows, meta)
    print("[v13c] off-anchor deltas vs anchor...")
    delta_rows = anchor_focus_delta_summary(candidate_base_rows, meta)
    recommendation = recommendation_rows(focus_summary_rows, pairwise_rows, delta_rows)

    print("[v13c] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_spectral_validation_base_rows.csv", candidate_base_rows)
    write_csv(f"{prefix}_spectral_validation_target_summary.csv", list(target_summary))
    write_csv(f"{prefix}_spectral_validation_run_summary.csv", run_summary_rows)
    write_csv(f"{prefix}_spectral_validation_focus_bootstrap_rows.csv", focus_boot_rows)
    write_csv(f"{prefix}_spectral_validation_focus_summary.csv", focus_summary_rows)
    write_csv(f"{prefix}_spectral_validation_pairwise_summary.csv", pairwise_rows)
    write_csv(f"{prefix}_spectral_validation_anchor_delta_summary.csv", delta_rows)
    write_csv(f"{prefix}_spectral_validation_recommendations.csv", recommendation)

    for path, content in [
        (args.report_md, build_report(target_summary, stable_rows, run_summary_rows, focus_summary_rows, pairwise_rows, delta_rows, recommendation)),
        (args.lay_md, build_lay_summary(recommendation)),
        (args.recommendation_md, build_recommendation(recommendation)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v13c] done")


if __name__ == "__main__":
    main()
