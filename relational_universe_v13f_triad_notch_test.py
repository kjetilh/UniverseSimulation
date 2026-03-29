#!/usr/bin/env python3
"""v0.13f notch test for the spectral quasi-invariant in the triad corridor.

This follows v13e. The corridor is no longer broadly mixed; the ambiguity is
localized near `bridge_00075_0000`. This round keeps the model fixed and only
adds finer triad points immediately around that regime.
"""
from __future__ import annotations

import argparse
import statistics
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v12_geometry_invariant_lab as v12
import relational_universe_v13_geometry_signal_validation as v13
import relational_universe_v13b_cross_regime_quasiinvariant_test as v13b
import relational_universe_v13c_spectral_quasiinvariant_validation as v13c


ANCHOR_REGIME = "band_zero_del"
SPECTRAL_METRIC = v13c.SPECTRAL_METRIC
DIM_METRIC = v13c.DIM_METRIC
ZERO_SANITY_METRICS = list(v13c.ZERO_SANITY_METRICS)

LOWER_EDGE = "bridge_000625_0000"
LOWER_FINE = "bridge_0006875_0000"
CENTER = "bridge_00075_0000"
UPPER_FINE = "bridge_0008125_0000"
UPPER_EDGE = "bridge_000875_0000"


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
            "candidate": v09.ScaleCandidate(LOWER_EDGE, 0.02, 0.00, 0.02, 0.000625, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate(LOWER_FINE, 0.02, 0.00, 0.02, 0.0006875, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate(CENTER, 0.02, 0.00, 0.02, 0.0007500, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate(UPPER_FINE, 0.02, 0.00, 0.02, 0.0008125, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate(UPPER_EDGE, 0.02, 0.00, 0.02, 0.0008750, 0.00),
            "axis_group": "triad",
        },
    ]


def candidate_meta() -> Dict[str, Dict[str, Any]]:
    return {spec["candidate"].name: spec for spec in candidate_specs()}


def candidate_local_summary(
    focus_summary_rows: Sequence[Dict[str, Any]],
    pairwise_rows: Sequence[Dict[str, Any]],
    delta_rows: Sequence[Dict[str, Any]],
    meta: Mapping[str, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    focus_lookup = {
        (str(row["candidate_name"]), str(row["metric"])): dict(row)
        for row in focus_summary_rows
    }
    pairwise_lookup = {str(row["candidate_name"]): dict(row) for row in pairwise_rows}
    delta_lookup = {
        (str(row["candidate_name"]), str(row["metric"])): dict(row)
        for row in delta_rows
    }
    rows: List[Dict[str, Any]] = []
    for candidate_name in sorted(name for name in meta if name != ANCHOR_REGIME):
        spectral = focus_lookup[(candidate_name, SPECTRAL_METRIC)]
        dim = focus_lookup[(candidate_name, DIM_METRIC)]
        pairwise = pairwise_lookup[candidate_name]
        delta = delta_lookup[(candidate_name, SPECTRAL_METRIC)]
        p_spectral = safe_float(pairwise["p_spectral_lt_dim"])
        mean_margin = safe_float(pairwise["mean_dim_minus_spectral"])
        mean_delta = safe_float(delta["mean_delta_vs_anchor"])
        spectral_mean = safe_float(spectral["bootstrap_mean_relative_drift"])
        dim_mean = safe_float(dim["bootstrap_mean_relative_drift"])
        if p_spectral >= 0.80 and mean_margin >= 0.012 and mean_delta <= 0.0045:
            local_status = "sharp_local"
        elif p_spectral >= 0.70 and mean_margin >= 0.009 and mean_delta <= 0.0065:
            local_status = "good_but_local"
        else:
            local_status = "mixed"
        rows.append(
            {
                "candidate_name": candidate_name,
                "axis_group": meta[candidate_name]["axis_group"],
                "spectral_mean_rel_drift": spectral_mean,
                "dim_mean_rel_drift": dim_mean,
                "p_spectral_lt_dim": p_spectral,
                "mean_dim_minus_spectral": mean_margin,
                "spectral_delta_vs_anchor": mean_delta,
                "local_status": local_status,
            }
        )
    return rows


def notch_summary(local_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_name = {str(row["candidate_name"]): dict(row) for row in local_rows}
    lower_edge = by_name[LOWER_EDGE]
    lower_fine = by_name[LOWER_FINE]
    center = by_name[CENTER]
    upper_fine = by_name[UPPER_FINE]
    upper_edge = by_name[UPPER_EDGE]

    fine_neighbors = [lower_fine, upper_fine]
    edge_neighbors = [lower_edge, upper_edge]

    fine_mean_p = statistics.mean(safe_float(r["p_spectral_lt_dim"]) for r in fine_neighbors)
    fine_mean_margin = statistics.mean(safe_float(r["mean_dim_minus_spectral"]) for r in fine_neighbors)
    fine_mean_delta = statistics.mean(safe_float(r["spectral_delta_vs_anchor"]) for r in fine_neighbors)
    fine_mean_spectral = statistics.mean(safe_float(r["spectral_mean_rel_drift"]) for r in fine_neighbors)

    edge_mean_p = statistics.mean(safe_float(r["p_spectral_lt_dim"]) for r in edge_neighbors)
    edge_mean_delta = statistics.mean(safe_float(r["spectral_delta_vs_anchor"]) for r in edge_neighbors)

    notch_depth_pairwise = fine_mean_p - safe_float(center["p_spectral_lt_dim"])
    notch_depth_margin = fine_mean_margin - safe_float(center["mean_dim_minus_spectral"])
    notch_depth_delta = safe_float(center["spectral_delta_vs_anchor"]) - fine_mean_delta
    notch_depth_spectral = safe_float(center["spectral_mean_rel_drift"]) - fine_mean_spectral

    if (
        safe_float(center["p_spectral_lt_dim"]) <= min(safe_float(r["p_spectral_lt_dim"]) for r in fine_neighbors) - 0.12
        and notch_depth_margin >= 0.0020
        and notch_depth_delta >= 0.0008
        and notch_depth_spectral >= 0.0008
    ):
        notch_status = "likely_local_notch"
    elif notch_depth_pairwise <= 0.05 and abs(notch_depth_delta) <= 0.0007 and abs(notch_depth_spectral) <= 0.0007:
        notch_status = "local_plateau"
    elif (
        safe_float(center["p_spectral_lt_dim"]) >= fine_mean_p
        and safe_float(center["spectral_delta_vs_anchor"]) <= fine_mean_delta
        and safe_float(center["spectral_mean_rel_drift"]) <= fine_mean_spectral
    ):
        notch_status = "notch_not_supported"
    else:
        notch_status = "sampling_ambiguous"

    return [
        {
            "center_candidate": CENTER,
            "lower_fine_candidate": LOWER_FINE,
            "upper_fine_candidate": UPPER_FINE,
            "lower_edge_candidate": LOWER_EDGE,
            "upper_edge_candidate": UPPER_EDGE,
            "center_p_spectral_lt_dim": safe_float(center["p_spectral_lt_dim"]),
            "fine_neighbor_mean_p_spectral_lt_dim": fine_mean_p,
            "edge_neighbor_mean_p_spectral_lt_dim": edge_mean_p,
            "center_mean_dim_minus_spectral": safe_float(center["mean_dim_minus_spectral"]),
            "fine_neighbor_mean_dim_minus_spectral": fine_mean_margin,
            "center_spectral_delta_vs_anchor": safe_float(center["spectral_delta_vs_anchor"]),
            "fine_neighbor_mean_spectral_delta_vs_anchor": fine_mean_delta,
            "edge_neighbor_mean_spectral_delta_vs_anchor": edge_mean_delta,
            "center_spectral_mean_rel_drift": safe_float(center["spectral_mean_rel_drift"]),
            "fine_neighbor_mean_spectral_mean_rel_drift": fine_mean_spectral,
            "notch_depth_pairwise": notch_depth_pairwise,
            "notch_depth_margin": notch_depth_margin,
            "notch_depth_delta": notch_depth_delta,
            "notch_depth_spectral": notch_depth_spectral,
            "notch_status": notch_status,
        }
    ]


def recommendation_rows(
    local_rows: Sequence[Dict[str, Any]],
    notch_rows: Sequence[Dict[str, Any]],
    delta_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    beta1_rows = [r for r in delta_rows if str(r["metric"]) == "mean_abs_delta_beta1_rel"]
    beta1_breaks = any(abs(safe_float(r["mean_delta_vs_anchor"])) > 1e-12 for r in beta1_rows)
    out.append(
        {
            "signal_family": "zero_drift_sanity",
            "status": "breaks_off_anchor" if beta1_breaks else "still_exact",
            "best_candidate": "mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel",
            "note": (
                "Triad-notch-runden bryter fortsatt `beta1` off-anchor; null-drift skal fortsatt ikke leses som lov."
                if beta1_breaks
                else "Null-driftene holder fortsatt eksakt i denne notch-runden."
            ),
        }
    )

    notch = notch_rows[0]
    notch_status = str(notch["notch_status"])
    fine_rows = [r for r in local_rows if str(r["candidate_name"]) in {LOWER_FINE, UPPER_FINE}]
    fine_sharp_count = sum(1 for r in fine_rows if str(r["local_status"]) == "sharp_local")
    fine_good_count = sum(1 for r in fine_rows if str(r["local_status"]) in {"sharp_local", "good_but_local"})

    if notch_status == "local_plateau" and fine_good_count == 2:
        spectral_status = "good_but_local"
        spectral_note = "Det blandede triadpunktet flater ut til et lite lokalt plateau; spektralsporet er renere enn i v13e."
        validation_status = "yes_targeted"
        validation_note = "Et neste større valideringssett kan brukes målrettet på spektralsporet med `dim_proxy` som sekundær kontroll."
    elif notch_status == "likely_local_notch" and fine_sharp_count == 2:
        spectral_status = "mixed_but_structured"
        spectral_note = "Triad-korridoren ser ut til å ha et ekte lokalt hakk rundt `bridge_00075_0000`; spektralsporet overlever, men er lokalt ikke-uniformt."
        validation_status = "not_yet"
        validation_note = "Forklar eller stabiliser notch-området før større valideringssett."
    elif notch_status == "notch_not_supported" and fine_good_count == 2:
        spectral_status = "good_but_local"
        spectral_note = "Det tidligere blandede punktet ser ikke lenger ut som et eget hakk; den smale triad-korridoren er lokalt renere."
        validation_status = "yes_targeted"
        validation_note = "Den smale triad-korridoren er ren nok til en målrettet neste valideringsrunde."
    else:
        spectral_status = "mixed"
        spectral_note = "Notch-området er fortsatt ikke rent nok til å si om `bridge_00075_0000` er et ekte lokalt hakk eller bare restusikkerhet."
        validation_status = "not_yet"
        validation_note = "Vent med større valideringssett til notch-området er bedre forklart."

    out.append(
        {
            "signal_family": "spectral_quasi_invariant",
            "status": spectral_status,
            "best_candidate": SPECTRAL_METRIC,
            "note": spectral_note,
        }
    )
    out.append(
        {
            "signal_family": "larger_validation_set",
            "status": validation_status,
            "best_candidate": "spectral_vs_dim_triad_notch",
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
    local_rows: Sequence[Dict[str, Any]],
    notch_rows: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.13f: notch-test i triad-korridoren")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden holder modellen fast og gjør bare én ting: den tester om det blandede triadpunktet i `v13e` er et ekte lokalt hakk eller bare restusikkerhet etter for grov bracketing."
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
    lines.append("## Lokal triad-notch-summering")
    lines.append("")
    lines.append("| regime | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | local_status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in local_rows:
        lines.append(
            f"| {row['candidate_name']} | {safe_float(row['spectral_mean_rel_drift']):.4f} | {safe_float(row['dim_mean_rel_drift']):.4f} | "
            f"{safe_float(row['p_spectral_lt_dim']):.3f} | {safe_float(row['mean_dim_minus_spectral']):.4f} | "
            f"{safe_float(row['spectral_delta_vs_anchor']):.4f} | {row['local_status']} |"
        )
    lines.append("")
    lines.append("## Notch-diagnose")
    lines.append("")
    lines.append("| center | fine_neighbor_mean_p | edge_neighbor_mean_p | notch_depth_pairwise | notch_depth_margin | notch_depth_delta | notch_depth_spectral | notch_status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in notch_rows:
        lines.append(
            f"| {row['center_candidate']} | {safe_float(row['fine_neighbor_mean_p_spectral_lt_dim']):.3f} | "
            f"{safe_float(row['edge_neighbor_mean_p_spectral_lt_dim']):.3f} | {safe_float(row['notch_depth_pairwise']):.4f} | "
            f"{safe_float(row['notch_depth_margin']):.4f} | {safe_float(row['notch_depth_delta']):.4f} | "
            f"{safe_float(row['notch_depth_spectral']):.4f} | {row['notch_status']} |"
        )
    lines.append("")
    lines.append("## Fokusdrift per regime")
    lines.append("")
    lines.append("| regime | metric | mean_rel_drift | q10 | q90 | top2_prob |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in focus_summary_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['metric']} | {safe_float(row['bootstrap_mean_relative_drift']):.4f} | "
            f"{safe_float(row['bootstrap_q10_relative_drift']):.4f} | {safe_float(row['bootstrap_q90_relative_drift']):.4f} | {safe_float(row['top2_prob']):.3f} |"
        )
    lines.append("")
    lines.append("## Spektral mot dim")
    lines.append("")
    lines.append("| regime | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in pairwise_rows:
        lines.append(
            f"| {row['candidate_name']} | {safe_float(row['p_spectral_lt_dim']):.3f} | "
            f"{safe_float(row['mean_dim_minus_spectral']):.4f} | {safe_float(row['q10_dim_minus_spectral']):.4f} | {safe_float(row['q90_dim_minus_spectral']):.4f} |"
        )
    lines.append("")
    lines.append("## Off-anchor mot anker")
    lines.append("")
    lines.append("| regime | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in delta_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['metric']} | {safe_float(row['mean_delta_vs_anchor']):.4f} | "
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
    lines.append("- Denne runden prøver ikke å gjøre spektralsporet bredere, bare å avgjøre om hakket rundt `bridge_00075_0000` er reelt.")
    lines.append("- Hvis hakket er reelt, betyr det at spektralsporet har mer lokal struktur enn `v13e` alene kunne vise.")
    lines.append("- Hvis hakket flater ut, er triad-korridoren renere enn før og et bedre grunnlag for neste målrettede validering.")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    spectral = next((r for r in recommendation if str(r["signal_family"]) == "spectral_quasi_invariant"), None)
    validation = next((r for r in recommendation if str(r["signal_family"]) == "larger_validation_set"), None)
    lines = [
        "# v0.13f for ikke-spesialister",
        "",
        "Denne runden zoomer helt inn på ett lite punkt i triad-korridoren for å finne ut om det virkelig er et lokalt hakk i signalet, eller bare usikkerhet fra for grov inndeling.",
        "",
    ]
    if spectral is not None:
        lines.append(f"- Spektralsporet: `{spectral['status']}`.")
    if validation is not None:
        lines.append(f"- Større valideringssett: `{validation['status']}`.")
    lines.extend(["", "Poenget er å vite om vi bør forklare et lokalt hakk, eller om korridoren nå er ren nok til neste målrettede test.", ""])
    return "\n".join(lines)


def build_recommendation(recommendation: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.13f operativ anbefaling", ""]
    for row in recommendation:
        lines.append(f"- {row['signal_family']}: {row['note']}")
    lines.append("")
    return "\n".join(lines)


def build_status_note(notch_rows: Sequence[Dict[str, Any]], recommendation: Sequence[Dict[str, Any]]) -> str:
    notch = notch_rows[0]
    spectral = next((r for r in recommendation if str(r["signal_family"]) == "spectral_quasi_invariant"), None)
    validation = next((r for r in recommendation if str(r["signal_family"]) == "larger_validation_set"), None)
    lines = [
        "# Relasjonell universgraf status v0.13f",
        "",
        "## Kort status",
        "",
        "- Dette er neste smale steg etter `v13e`.",
        f"- Notch-status rundt `{CENTER}`: `{notch['notch_status']}`.",
        f"- Pairwise-dybde mot fine naboer: `{safe_float(notch['notch_depth_pairwise']):.4f}`.",
        f"- Drift-dybde mot fine naboer: `{safe_float(notch['notch_depth_spectral']):.4f}`.",
    ]
    if spectral is not None:
        lines.append(f"- Spektralsporet: `{spectral['status']}`.")
    if validation is not None:
        lines.append(f"- Større valideringssett: `{validation['status']}`.")
    lines.extend(["", "## Lesning", ""])
    lines.append("- `v13f` avgjør ikke hele geometri-sporet alene, men den gjør triad-usikkerheten mer lokal og mer tolkbar.")
    lines.append("- Null-driften for `beta1` skal fortsatt ikke leses som lov hvis den fortsatt bryter off-anchor.")
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.13f triad notch test")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=5)
    ap.add_argument("--run-seeds", type=int, default=5)
    ap.add_argument("--bootstrap-reps", type=int, default=220)
    ap.add_argument("--output-prefix", default="Documentation/v13f")
    ap.add_argument("--report-md", default="Documentation/v13f_triad_notch_test.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_13f.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_13f_operativ_anbefaling.md")
    ap.add_argument("--status-md", default="Documentation/relasjonell_universgraf_status_v0_13f.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    specs = candidate_specs()
    candidates = [spec["candidate"] for spec in specs]
    meta = candidate_meta()
    growth_seeds = [87001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [53001 + 31 * i for i in range(args.run_seeds)]

    print(
        f"[v13f] regime={regime.name} targets={targets} candidates={[c.name for c in candidates]} "
        f"growth={len(growth_seeds)} runs={len(run_offsets)} boot={args.bootstrap_reps}"
    )
    print("[v13f] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    base_lookup = {(str(r['ensemble']), int(r['growth_seed'])): dict(r) for r in base_rows}
    print("[v13f] bases done")

    print("[v13f] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    run_rows = [v12.enrich_run_row(row, base_lookup) for row in raw_run_rows]
    print(f"[v13f] runs done: {len(run_rows)} rows")

    print("[v13f] aggregating candidate/base rows...")
    candidate_base_rows = v13b.grouped_candidate_base_rows(base_rows, run_rows)
    stable_rows = (
        v13.stable_control_summary(base_rows, args.bootstrap_reps, seed=51001)
        if hasattr(v13, "stable_control_summary")
        else v13.feature_stability_bootstrap_summary(base_rows, args.bootstrap_reps, 51001)[1]
    )
    run_summary_rows = v13b.regime_run_summary(candidate_base_rows, meta)
    print("[v13f] bootstrap: focus drift summary...")
    focus_boot_rows, focus_summary_rows = v13c.focus_bootstrap_summary(candidate_base_rows, meta, args.bootstrap_reps, seed=51041)
    print("[v13f] paired spectral-vs-dim comparison...")
    pairwise_rows = v13c.spectral_dim_pairwise_summary(candidate_base_rows, meta)
    print("[v13f] off-anchor deltas vs anchor...")
    delta_rows = v13c.anchor_focus_delta_summary(candidate_base_rows, meta)
    local_rows = candidate_local_summary(focus_summary_rows, pairwise_rows, delta_rows, meta)
    notch_rows = notch_summary(local_rows)
    recommendation = recommendation_rows(local_rows, notch_rows, delta_rows)

    print("[v13f] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_spectral_validation_base_rows.csv", candidate_base_rows)
    write_csv(f"{prefix}_spectral_validation_target_summary.csv", list(target_summary))
    write_csv(f"{prefix}_spectral_validation_run_summary.csv", run_summary_rows)
    write_csv(f"{prefix}_spectral_validation_focus_bootstrap_rows.csv", focus_boot_rows)
    write_csv(f"{prefix}_spectral_validation_focus_summary.csv", focus_summary_rows)
    write_csv(f"{prefix}_spectral_validation_pairwise_summary.csv", pairwise_rows)
    write_csv(f"{prefix}_spectral_validation_anchor_delta_summary.csv", delta_rows)
    write_csv(f"{prefix}_spectral_validation_local_summary.csv", local_rows)
    write_csv(f"{prefix}_spectral_validation_notch_summary.csv", notch_rows)
    write_csv(f"{prefix}_spectral_validation_recommendations.csv", recommendation)

    for path, content in [
        (args.report_md, build_report(target_summary, stable_rows, run_summary_rows, focus_summary_rows, pairwise_rows, delta_rows, local_rows, notch_rows, recommendation)),
        (args.lay_md, build_lay_summary(recommendation)),
        (args.recommendation_md, build_recommendation(recommendation)),
        (args.status_md, build_status_note(notch_rows, recommendation)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v13f] done")


if __name__ == "__main__":
    main()
