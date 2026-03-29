#!/usr/bin/env python3
"""v0.13i refinement around the recovered upper-triad point.

This follows v13h. The upper side no longer looks like a simple monotone
degradation; instead, `bridge_00084375_0000` appeared as a locally recovered
point. This round tests whether that recovery is real under finer bracketing.
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

LOWER_ANCHOR = "bridge_0008125_0000"
LOWER_FINE = "bridge_000828125_0000"
CENTER = "bridge_00084375_0000"
UPPER_FINE = "bridge_000859375_0000"
UPPER_ANCHOR = "bridge_000875_0000"


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
            "candidate": v09.ScaleCandidate(LOWER_ANCHOR, 0.02, 0.00, 0.02, 0.0008125, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate(LOWER_FINE, 0.02, 0.00, 0.02, 0.000828125, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate(CENTER, 0.02, 0.00, 0.02, 0.00084375, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate(UPPER_FINE, 0.02, 0.00, 0.02, 0.000859375, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate(UPPER_ANCHOR, 0.02, 0.00, 0.02, 0.0008750, 0.00),
            "axis_group": "triad",
        },
    ]


def candidate_meta() -> Dict[str, Dict[str, Any]]:
    return {spec["candidate"].name: spec for spec in candidate_specs()}


def refinement_summary(
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
        top3_prob = safe_float(spectral["top3_prob"])
        spectral_mean = safe_float(spectral["bootstrap_mean_relative_drift"])
        dim_mean = safe_float(dim["bootstrap_mean_relative_drift"])
        if p_spectral >= 0.80 and mean_margin >= 0.015 and mean_delta <= 0.003 and top3_prob >= 0.99:
            local_status = "sharp_local"
        elif p_spectral >= 0.72 and mean_margin >= 0.011 and mean_delta <= 0.006:
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
                "spectral_top3_prob": top3_prob,
                "local_status": local_status,
            }
        )
    return rows


def recovery_diagnosis(summary_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_name = {str(row["candidate_name"]): dict(row) for row in summary_rows}
    lower_anchor = by_name[LOWER_ANCHOR]
    lower_fine = by_name[LOWER_FINE]
    center = by_name[CENTER]
    upper_fine = by_name[UPPER_FINE]
    upper_anchor = by_name[UPPER_ANCHOR]

    immediate_neighbors = [lower_fine, upper_fine]
    flank_anchors = [lower_anchor, upper_anchor]

    center_p = safe_float(center["p_spectral_lt_dim"])
    center_margin = safe_float(center["mean_dim_minus_spectral"])
    center_delta = safe_float(center["spectral_delta_vs_anchor"])
    center_spectral = safe_float(center["spectral_mean_rel_drift"])

    immediate_mean_p = statistics.mean(safe_float(r["p_spectral_lt_dim"]) for r in immediate_neighbors)
    immediate_mean_margin = statistics.mean(safe_float(r["mean_dim_minus_spectral"]) for r in immediate_neighbors)
    immediate_mean_delta = statistics.mean(safe_float(r["spectral_delta_vs_anchor"]) for r in immediate_neighbors)
    immediate_mean_spectral = statistics.mean(safe_float(r["spectral_mean_rel_drift"]) for r in immediate_neighbors)

    flank_mean_p = statistics.mean(safe_float(r["p_spectral_lt_dim"]) for r in flank_anchors)
    flank_mean_delta = statistics.mean(safe_float(r["spectral_delta_vs_anchor"]) for r in flank_anchors)

    p_gain_vs_immediate = center_p - immediate_mean_p
    margin_gain_vs_immediate = center_margin - immediate_mean_margin
    delta_improvement_vs_immediate = immediate_mean_delta - center_delta
    spectral_improvement_vs_immediate = immediate_mean_spectral - center_spectral

    if (
        center_p >= max(safe_float(r["p_spectral_lt_dim"]) for r in immediate_neighbors) + 0.08
        and margin_gain_vs_immediate >= 0.0020
        and delta_improvement_vs_immediate >= 0.0006
        and spectral_improvement_vs_immediate >= 0.0006
    ):
        recovery_status = "local_recovery_supported"
    elif (
        abs(p_gain_vs_immediate) <= 0.04
        and abs(delta_improvement_vs_immediate) <= 0.0008
        and abs(spectral_improvement_vs_immediate) <= 0.0008
    ):
        recovery_status = "local_plateau"
    elif (
        center_p <= immediate_mean_p
        and center_delta >= immediate_mean_delta
        and center_spectral >= immediate_mean_spectral
    ):
        recovery_status = "recovery_not_supported"
    else:
        recovery_status = "sampling_ambiguous"

    return [
        {
            "lower_anchor_candidate": LOWER_ANCHOR,
            "lower_fine_candidate": LOWER_FINE,
            "center_candidate": CENTER,
            "upper_fine_candidate": UPPER_FINE,
            "upper_anchor_candidate": UPPER_ANCHOR,
            "center_p_spectral_lt_dim": center_p,
            "immediate_mean_p_spectral_lt_dim": immediate_mean_p,
            "flank_mean_p_spectral_lt_dim": flank_mean_p,
            "center_mean_dim_minus_spectral": center_margin,
            "immediate_mean_dim_minus_spectral": immediate_mean_margin,
            "center_spectral_delta_vs_anchor": center_delta,
            "immediate_mean_spectral_delta_vs_anchor": immediate_mean_delta,
            "flank_mean_spectral_delta_vs_anchor": flank_mean_delta,
            "center_spectral_mean_rel_drift": center_spectral,
            "immediate_mean_spectral_mean_rel_drift": immediate_mean_spectral,
            "p_gain_vs_immediate": p_gain_vs_immediate,
            "margin_gain_vs_immediate": margin_gain_vs_immediate,
            "delta_improvement_vs_immediate": delta_improvement_vs_immediate,
            "spectral_improvement_vs_immediate": spectral_improvement_vs_immediate,
            "recovery_status": recovery_status,
        }
    ]


def recommendation_rows(
    summary_rows: Sequence[Dict[str, Any]],
    recovery_rows: Sequence[Dict[str, Any]],
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
                "Upper-recovery-runden bryter fortsatt `beta1` off-anchor; null-drift skal fortsatt ikke leses som lov."
                if beta1_breaks
                else "Null-driftene holder fortsatt eksakt i denne upper-recovery-runden."
            ),
        }
    )

    recovery = recovery_rows[0]
    status = str(recovery["recovery_status"])
    good_count = sum(1 for r in summary_rows if str(r["local_status"]) in {"sharp_local", "good_but_local"})
    mixed_count = sum(1 for r in summary_rows if str(r["local_status"]) == "mixed")

    if status == "local_recovery_supported" and good_count >= 4:
        spectral_status = "good_but_local"
        spectral_note = "Det gjenopprettede oversidepunktet holder under finere bracketing, men sporet er fortsatt lokalt og ikke bredt validert."
        validation_status = "yes_targeted"
        validation_note = "Neste steg kan bruke et svært smalt, målrettet sett rundt dette oversidepunktet."
    elif status == "local_plateau" and mixed_count <= 1:
        spectral_status = "good_but_local"
        spectral_note = "Oversiden ser mer ut som et lite lokalt plateau rundt recovery-punktet enn en skarp topp."
        validation_status = "yes_targeted"
        validation_note = "Et nytt lite kontrollsett kan brukes på dette recovery-plateauet før bredere oppskalering."
    elif status == "recovery_not_supported":
        spectral_status = "mixed"
        spectral_note = "Det gjenopprettede oversidepunktet holder ikke under finere bracketing; spektralsporet er fortsatt blandet her."
        validation_status = "not_yet"
        validation_note = "Vent med bredere validering til recovery-området er bedre forstått."
    else:
        spectral_status = "mixed"
        spectral_note = "Recovery-området er fortsatt ikke rent nok til å kalle spektralsporet målrettet validert."
        validation_status = "not_yet"
        validation_note = "Vent med bredere validering til recovery-området er bedre avklart."

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
            "best_candidate": "spectral_vs_dim_upper_recovery_refinement",
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
    summary_rows: Sequence[Dict[str, Any]],
    recovery_rows: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.13i: raffinering av gjenopprettet oversidepunkt")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden følger etter `v13h` og tester bare om det gjenopprettede oversidepunktet ved `bridge_00084375_0000` holder under finere bracketing, eller om det bare var en lokal fluktuasjon."
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
    lines.append("## Recovery-sammendrag")
    lines.append("")
    lines.append("| regime | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | spectral_top3_prob | local_status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in summary_rows:
        lines.append(
            f"| {row['candidate_name']} | {safe_float(row['spectral_mean_rel_drift']):.4f} | {safe_float(row['dim_mean_rel_drift']):.4f} | "
            f"{safe_float(row['p_spectral_lt_dim']):.3f} | {safe_float(row['mean_dim_minus_spectral']):.4f} | "
            f"{safe_float(row['spectral_delta_vs_anchor']):.4f} | {safe_float(row['spectral_top3_prob']):.3f} | {row['local_status']} |"
        )
    lines.append("")
    lines.append("## Recovery-diagnose")
    lines.append("")
    lines.append("| center | immediate_mean_p | p_gain_vs_immediate | margin_gain_vs_immediate | delta_improvement_vs_immediate | spectral_improvement_vs_immediate | recovery_status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in recovery_rows:
        lines.append(
            f"| {row['center_candidate']} | {safe_float(row['immediate_mean_p_spectral_lt_dim']):.3f} | "
            f"{safe_float(row['p_gain_vs_immediate']):.4f} | {safe_float(row['margin_gain_vs_immediate']):.4f} | "
            f"{safe_float(row['delta_improvement_vs_immediate']):.4f} | {safe_float(row['spectral_improvement_vs_immediate']):.4f} | {row['recovery_status']} |"
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
    lines.append("- Denne runden spør bare om det gjenopprettede punktet holder når vi ser enda nærmere på det.")
    lines.append("- Hvis det holder, vet vi at oversiden har ekte lokal struktur, ikke bare støy.")
    lines.append("- Hvis det ikke holder, skal recovery-punktet leses som en midlertidig lokal fluktuasjon.")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    spectral = next((r for r in recommendation if str(r["signal_family"]) == "spectral_quasi_invariant"), None)
    validation = next((r for r in recommendation if str(r["signal_family"]) == "larger_validation_set"), None)
    lines = [
        "# v0.13i for ikke-spesialister",
        "",
        "Denne runden zoomer enda mer inn på det ene oversidepunktet som så lovende ut i `v13h`, for å finne ut om det virkelig er spesielt eller bare var en tilfeldig god måling.",
        "",
    ]
    if spectral is not None:
        lines.append(f"- Spektralsporet: `{spectral['status']}`.")
    if validation is not None:
        lines.append(f"- Neste valideringsnivå: `{validation['status']}`.")
    lines.extend(["", "Poenget er å vite om vi har funnet et ekte lite toppunkt, eller om oversiden fortsatt bare er blandet.", ""])
    return "\n".join(lines)


def build_recommendation(recommendation: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.13i operativ anbefaling", ""]
    for row in recommendation:
        lines.append(f"- {row['signal_family']}: {row['note']}")
    lines.append("")
    return "\n".join(lines)


def build_status_note(recovery_rows: Sequence[Dict[str, Any]], recommendation: Sequence[Dict[str, Any]]) -> str:
    recovery = recovery_rows[0]
    spectral = next((r for r in recommendation if str(r["signal_family"]) == "spectral_quasi_invariant"), None)
    validation = next((r for r in recommendation if str(r["signal_family"]) == "larger_validation_set"), None)
    lines = [
        "# Relasjonell universgraf status v0.13i",
        "",
        "## Kort status",
        "",
        "- Dette er neste smale steg etter `v13h`.",
        f"- Recovery-status rundt `{CENTER}`: `{recovery['recovery_status']}`.",
        f"- P-gain mot nærmeste naboer: `{safe_float(recovery['p_gain_vs_immediate']):.4f}`.",
        f"- Delta-forbedring mot nærmeste naboer: `{safe_float(recovery['delta_improvement_vs_immediate']):.4f}`.",
    ]
    if spectral is not None:
        lines.append(f"- Spektralsporet: `{spectral['status']}`.")
    if validation is not None:
        lines.append(f"- Neste valideringsnivå: `{validation['status']}`.")
    lines.extend(["", "## Lesning", ""])
    lines.append("- `v13i` sier mer presist om det lovende oversidepunktet er ekte eller bare midlertidig.")
    lines.append("- `beta1` skal fortsatt ikke leses som lov hvis den fortsatt bryter off-anchor.")
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.13i upper recovery refinement")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=5)
    ap.add_argument("--run-seeds", type=int, default=5)
    ap.add_argument("--bootstrap-reps", type=int, default=260)
    ap.add_argument("--output-prefix", default="Documentation/v13i")
    ap.add_argument("--report-md", default="Documentation/v13i_upper_recovery_refinement.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_13i.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_13i_operativ_anbefaling.md")
    ap.add_argument("--status-md", default="Documentation/relasjonell_universgraf_status_v0_13i.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    specs = candidate_specs()
    candidates = [spec["candidate"] for spec in specs]
    meta = candidate_meta()
    growth_seeds = [103001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [71001 + 31 * i for i in range(args.run_seeds)]

    print(
        f"[v13i] regime={regime.name} targets={targets} candidates={[c.name for c in candidates]} "
        f"growth={len(growth_seeds)} runs={len(run_offsets)} boot={args.bootstrap_reps}"
    )
    print("[v13i] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    base_lookup = {(str(r['ensemble']), int(r['growth_seed'])): dict(r) for r in base_rows}
    print("[v13i] bases done")

    print("[v13i] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    run_rows = [v12.enrich_run_row(row, base_lookup) for row in raw_run_rows]
    print(f"[v13i] runs done: {len(run_rows)} rows")

    print("[v13i] aggregating candidate/base rows...")
    candidate_base_rows = v13b.grouped_candidate_base_rows(base_rows, run_rows)
    stable_rows = (
        v13.stable_control_summary(base_rows, args.bootstrap_reps, seed=77001)
        if hasattr(v13, "stable_control_summary")
        else v13.feature_stability_bootstrap_summary(base_rows, args.bootstrap_reps, 77001)[1]
    )
    run_summary_rows = v13b.regime_run_summary(candidate_base_rows, meta)
    print("[v13i] bootstrap: focus drift summary...")
    focus_boot_rows, focus_summary_rows = v13c.focus_bootstrap_summary(candidate_base_rows, meta, args.bootstrap_reps, seed=77041)
    print("[v13i] paired spectral-vs-dim comparison...")
    pairwise_rows = v13c.spectral_dim_pairwise_summary(candidate_base_rows, meta)
    print("[v13i] off-anchor deltas vs anchor...")
    delta_rows = v13c.anchor_focus_delta_summary(candidate_base_rows, meta)
    summary_rows = refinement_summary(focus_summary_rows, pairwise_rows, delta_rows, meta)
    recovery_rows = recovery_diagnosis(summary_rows)
    recommendation = recommendation_rows(summary_rows, recovery_rows, delta_rows)

    print("[v13i] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_spectral_validation_base_rows.csv", candidate_base_rows)
    write_csv(f"{prefix}_spectral_validation_target_summary.csv", list(target_summary))
    write_csv(f"{prefix}_spectral_validation_run_summary.csv", run_summary_rows)
    write_csv(f"{prefix}_spectral_validation_focus_bootstrap_rows.csv", focus_boot_rows)
    write_csv(f"{prefix}_spectral_validation_focus_summary.csv", focus_summary_rows)
    write_csv(f"{prefix}_spectral_validation_pairwise_summary.csv", pairwise_rows)
    write_csv(f"{prefix}_spectral_validation_anchor_delta_summary.csv", delta_rows)
    write_csv(f"{prefix}_spectral_validation_refinement_summary.csv", summary_rows)
    write_csv(f"{prefix}_spectral_validation_recovery_diagnosis.csv", recovery_rows)
    write_csv(f"{prefix}_spectral_validation_recommendations.csv", recommendation)

    for path, content in [
        (args.report_md, build_report(target_summary, stable_rows, run_summary_rows, focus_summary_rows, pairwise_rows, delta_rows, summary_rows, recovery_rows, recommendation)),
        (args.lay_md, build_lay_summary(recommendation)),
        (args.recommendation_md, build_recommendation(recommendation)),
        (args.status_md, build_status_note(recovery_rows, recommendation)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v13i] done")


if __name__ == "__main__":
    main()
