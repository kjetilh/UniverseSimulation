#!/usr/bin/env python3
"""v0.13j refinement of the clean upper-triad band.

This follows v13i. The apparent recovery point around `bridge_00084375_0000`
did not hold, but two lower upper-side points remained sharp. This round tests
whether there is a genuinely cleaner local sub-band between
`bridge_0008125_0000` and `bridge_000828125_0000`, or whether that was also a
local fluctuation.
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
LOWER_MID = "bridge_0008203125_0000"
UPPER_MID = "bridge_000828125_0000"
UPPER_INNER_CONTROL = "bridge_0008359375_0000"
UPPER_OUTER_CONTROL = "bridge_00084375_0000"


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v12.write_csv(path, rows)


def candidate_specs() -> List[Dict[str, Any]]:
    return [
        {
            "candidate": v09.ScaleCandidate(ANCHOR_REGIME, 0.02, 0.00, 0.02, 0.00, 0.00),
            "axis_group": "anchor",
        },
        {
            "candidate": v09.ScaleCandidate(LOWER_ANCHOR, 0.02, 0.00, 0.02, 0.0008125, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate(LOWER_MID, 0.02, 0.00, 0.02, 0.0008203125, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate(UPPER_MID, 0.02, 0.00, 0.02, 0.000828125, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate(UPPER_INNER_CONTROL, 0.02, 0.00, 0.02, 0.0008359375, 0.00),
            "axis_group": "triad",
        },
        {
            "candidate": v09.ScaleCandidate(UPPER_OUTER_CONTROL, 0.02, 0.00, 0.02, 0.00084375, 0.00),
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


def band_diagnosis(summary_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_name = {str(row["candidate_name"]): dict(row) for row in summary_rows}
    band_rows = [by_name[LOWER_ANCHOR], by_name[LOWER_MID], by_name[UPPER_MID]]
    control_rows = [by_name[UPPER_INNER_CONTROL], by_name[UPPER_OUTER_CONTROL]]

    band_mean_p = statistics.mean(safe_float(r["p_spectral_lt_dim"]) for r in band_rows)
    band_mean_margin = statistics.mean(safe_float(r["mean_dim_minus_spectral"]) for r in band_rows)
    band_mean_delta = statistics.mean(safe_float(r["spectral_delta_vs_anchor"]) for r in band_rows)
    band_mean_spectral = statistics.mean(safe_float(r["spectral_mean_rel_drift"]) for r in band_rows)

    control_mean_p = statistics.mean(safe_float(r["p_spectral_lt_dim"]) for r in control_rows)
    control_mean_margin = statistics.mean(safe_float(r["mean_dim_minus_spectral"]) for r in control_rows)
    control_mean_delta = statistics.mean(safe_float(r["spectral_delta_vs_anchor"]) for r in control_rows)
    control_mean_spectral = statistics.mean(safe_float(r["spectral_mean_rel_drift"]) for r in control_rows)

    p_gain_vs_controls = band_mean_p - control_mean_p
    margin_gain_vs_controls = band_mean_margin - control_mean_margin
    delta_improvement_vs_controls = control_mean_delta - band_mean_delta
    spectral_improvement_vs_controls = control_mean_spectral - band_mean_spectral

    sharp_count = sum(1 for r in band_rows if str(r["local_status"]) == "sharp_local")
    mixed_count = sum(1 for r in band_rows if str(r["local_status"]) == "mixed")

    if (
        sharp_count == len(band_rows)
        and p_gain_vs_controls >= 0.08
        and margin_gain_vs_controls >= 0.0015
        and delta_improvement_vs_controls >= 0.0004
        and spectral_improvement_vs_controls >= 0.0004
    ):
        band_status = "clean_band_supported"
    elif (
        mixed_count == 0
        and abs(p_gain_vs_controls) <= 0.04
        and abs(delta_improvement_vs_controls) <= 0.0008
        and abs(spectral_improvement_vs_controls) <= 0.0008
    ):
        band_status = "clean_band_plateau"
    elif (
        band_mean_p <= control_mean_p
        and band_mean_delta >= control_mean_delta
        and band_mean_spectral >= control_mean_spectral
    ):
        band_status = "clean_band_not_supported"
    else:
        band_status = "sampling_ambiguous"

    return [
        {
            "lower_anchor_candidate": LOWER_ANCHOR,
            "lower_mid_candidate": LOWER_MID,
            "upper_mid_candidate": UPPER_MID,
            "upper_inner_control_candidate": UPPER_INNER_CONTROL,
            "upper_outer_control_candidate": UPPER_OUTER_CONTROL,
            "band_mean_p_spectral_lt_dim": band_mean_p,
            "control_mean_p_spectral_lt_dim": control_mean_p,
            "band_mean_dim_minus_spectral": band_mean_margin,
            "control_mean_dim_minus_spectral": control_mean_margin,
            "band_mean_spectral_delta_vs_anchor": band_mean_delta,
            "control_mean_spectral_delta_vs_anchor": control_mean_delta,
            "band_mean_spectral_mean_rel_drift": band_mean_spectral,
            "control_mean_spectral_mean_rel_drift": control_mean_spectral,
            "band_sharp_count": sharp_count,
            "band_mixed_count": mixed_count,
            "p_gain_vs_controls": p_gain_vs_controls,
            "margin_gain_vs_controls": margin_gain_vs_controls,
            "delta_improvement_vs_controls": delta_improvement_vs_controls,
            "spectral_improvement_vs_controls": spectral_improvement_vs_controls,
            "band_status": band_status,
        }
    ]


def recommendation_rows(
    summary_rows: Sequence[Dict[str, Any]],
    band_rows: Sequence[Dict[str, Any]],
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
                "Den smale upper-band-runden bryter fortsatt `beta1` off-anchor; null-drift skal fortsatt ikke leses som lov."
                if beta1_breaks
                else "Null-driftene holder fortsatt eksakt i denne smale upper-band-runden."
            ),
        }
    )

    diagnosis = band_rows[0]
    status = str(diagnosis["band_status"])
    good_count = sum(1 for r in summary_rows if str(r["local_status"]) in {"sharp_local", "good_but_local"})
    mixed_count = sum(1 for r in summary_rows if str(r["local_status"]) == "mixed")

    if status == "clean_band_supported" and good_count >= 4:
        spectral_status = "good_but_local"
        spectral_note = "Det smale bandet mellom `bridge_0008125_0000` og `bridge_000828125_0000` holder som den reneste lokale triad-sonen, men sporet er fortsatt lokalt."
        validation_status = "yes_targeted"
        validation_note = "Et lite målrettet valideringssett rundt dette bandet er nå rimelig."
    elif status == "clean_band_plateau" and mixed_count <= 1:
        spectral_status = "good_but_local"
        spectral_note = "Det smale upper-bandet ser mer ut som et lite lokalt plateau enn en enkelt skarp topp."
        validation_status = "yes_targeted"
        validation_note = "Et lite målrettet valideringssett kan brukes på hele dette smale bandet før bredere oppskalering."
    elif status == "clean_band_not_supported":
        spectral_status = "mixed"
        spectral_note = "Det tilsynelatende rene upper-bandet holder ikke bedre enn kontrollpunktene over det; spektralsporet er fortsatt blandet her."
        validation_status = "not_yet"
        validation_note = "Vent med bredere validering til upper-bandet er bedre forstått."
    else:
        spectral_status = "mixed"
        spectral_note = "Upper-bandet er fortsatt ikke rent nok til å kalle spektralsporet målrettet validert."
        validation_status = "not_yet"
        validation_note = "Vent med bredere validering til det smale bandet er bedre avklart."

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
            "best_candidate": "spectral_vs_dim_upper_clean_band",
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
    band_rows: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.13j: raffinering av rent oversideband")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden følger etter `v13i` og tester om den reneste delen av oversiden faktisk er et lite sammenhengende band mellom `bridge_0008125_0000` og `bridge_000828125_0000`, eller om også dette bare var en lokal fluktuasjon."
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
    lines.append("## Band-sammendrag")
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
    lines.append("## Band-diagnose")
    lines.append("")
    lines.append("| band_mean_p | control_mean_p | p_gain_vs_controls | margin_gain_vs_controls | delta_improvement_vs_controls | spectral_improvement_vs_controls | band_status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in band_rows:
        lines.append(
            f"| {safe_float(row['band_mean_p_spectral_lt_dim']):.3f} | {safe_float(row['control_mean_p_spectral_lt_dim']):.3f} | "
            f"{safe_float(row['p_gain_vs_controls']):.4f} | {safe_float(row['margin_gain_vs_controls']):.4f} | "
            f"{safe_float(row['delta_improvement_vs_controls']):.4f} | {safe_float(row['spectral_improvement_vs_controls']):.4f} | {row['band_status']} |"
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
    lines.append("- Denne runden spør bare om de reneste oversidepunktene faktisk danner et lite sammenhengende band.")
    lines.append("- Hvis de gjør det, vet vi at upper-bandet er en ekte lokal struktur og ikke bare ett enkelt godt punkt.")
    lines.append("- Hvis de ikke gjør det, skal også dette bandet leses som midlertidig lokal variasjon.")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    spectral = next((r for r in recommendation if str(r["signal_family"]) == "spectral_quasi_invariant"), None)
    validation = next((r for r in recommendation if str(r["signal_family"]) == "larger_validation_set"), None)
    lines = [
        "# v0.13j for ikke-spesialister",
        "",
        "Denne runden ser bare på om den reneste delen av den øvre triad-sonen faktisk holder som et lite sammenhengende område, eller om den også bryter opp når vi ser nærmere på den.",
        "",
    ]
    if spectral is not None:
        lines.append(f"- Spektralsporet: `{spectral['status']}`.")
    if validation is not None:
        lines.append(f"- Neste valideringsnivå: `{validation['status']}`.")
    lines.extend(["", "Poenget er å vite om vi virkelig har funnet et lite stabilt bånd, eller bare nye lokale gode målinger.", ""])
    return "\n".join(lines)


def build_recommendation(recommendation: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.13j operativ anbefaling", ""]
    for row in recommendation:
        lines.append(f"- {row['signal_family']}: {row['note']}")
    lines.append("")
    return "\n".join(lines)


def build_status_note(band_rows: Sequence[Dict[str, Any]], recommendation: Sequence[Dict[str, Any]]) -> str:
    diagnosis = band_rows[0]
    spectral = next((r for r in recommendation if str(r["signal_family"]) == "spectral_quasi_invariant"), None)
    validation = next((r for r in recommendation if str(r["signal_family"]) == "larger_validation_set"), None)
    lines = [
        "# Relasjonell universgraf status v0.13j",
        "",
        "## Kort status",
        "",
        "- Dette er neste smale steg etter `v13i`.",
        f"- Band-status mellom `{LOWER_ANCHOR}` og `{UPPER_MID}`: `{diagnosis['band_status']}`.",
        f"- P-gain mot øvre kontrollpunkt: `{safe_float(diagnosis['p_gain_vs_controls']):.4f}`.",
        f"- Delta-forbedring mot øvre kontrollpunkt: `{safe_float(diagnosis['delta_improvement_vs_controls']):.4f}`.",
    ]
    if spectral is not None:
        lines.append(f"- Spektralsporet: `{spectral['status']}`.")
    if validation is not None:
        lines.append(f"- Neste valideringsnivå: `{validation['status']}`.")
    lines.extend(["", "## Lesning", ""])
    lines.append("- `v13j` sier mer presist om den reneste delen av oversiden er et lite bånd eller bare en lokal serie gode punkt.")
    lines.append("- `beta1` skal fortsatt ikke leses som lov hvis den fortsatt bryter off-anchor.")
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.13j upper clean band refinement")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=5)
    ap.add_argument("--run-seeds", type=int, default=5)
    ap.add_argument("--bootstrap-reps", type=int, default=260)
    ap.add_argument("--output-prefix", default="Documentation/v13j")
    ap.add_argument("--report-md", default="Documentation/v13j_upper_clean_band_refinement.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_13j.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_13j_operativ_anbefaling.md")
    ap.add_argument("--status-md", default="Documentation/relasjonell_universgraf_status_v0_13j.md")
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
        f"[v13j] regime={regime.name} targets={targets} candidates={[c.name for c in candidates]} "
        f"growth={len(growth_seeds)} runs={len(run_offsets)} boot={args.bootstrap_reps}"
    )
    print("[v13j] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    base_lookup = {(str(r['ensemble']), int(r['growth_seed'])): dict(r) for r in base_rows}
    print("[v13j] bases done")

    print("[v13j] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    run_rows = [v12.enrich_run_row(row, base_lookup) for row in raw_run_rows]
    print(f"[v13j] runs done: {len(run_rows)} rows")

    print("[v13j] aggregating candidate/base rows...")
    candidate_base_rows = v13b.grouped_candidate_base_rows(base_rows, run_rows)
    stable_rows = (
        v13.stable_control_summary(base_rows, args.bootstrap_reps, seed=77001)
        if hasattr(v13, "stable_control_summary")
        else v13.feature_stability_bootstrap_summary(base_rows, args.bootstrap_reps, 77001)[1]
    )
    run_summary_rows = v13b.regime_run_summary(candidate_base_rows, meta)
    print("[v13j] bootstrap: focus drift summary...")
    focus_boot_rows, focus_summary_rows = v13c.focus_bootstrap_summary(candidate_base_rows, meta, args.bootstrap_reps, seed=77041)
    print("[v13j] paired spectral-vs-dim comparison...")
    pairwise_rows = v13c.spectral_dim_pairwise_summary(candidate_base_rows, meta)
    print("[v13j] off-anchor deltas vs anchor...")
    delta_rows = v13c.anchor_focus_delta_summary(candidate_base_rows, meta)
    summary_rows = refinement_summary(focus_summary_rows, pairwise_rows, delta_rows, meta)
    band_rows = band_diagnosis(summary_rows)
    recommendation = recommendation_rows(summary_rows, band_rows, delta_rows)

    print("[v13j] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_spectral_validation_base_rows.csv", candidate_base_rows)
    write_csv(f"{prefix}_spectral_validation_target_summary.csv", list(target_summary))
    write_csv(f"{prefix}_spectral_validation_run_summary.csv", run_summary_rows)
    write_csv(f"{prefix}_spectral_validation_focus_bootstrap_rows.csv", focus_boot_rows)
    write_csv(f"{prefix}_spectral_validation_focus_summary.csv", focus_summary_rows)
    write_csv(f"{prefix}_spectral_validation_pairwise_summary.csv", pairwise_rows)
    write_csv(f"{prefix}_spectral_validation_anchor_delta_summary.csv", delta_rows)
    write_csv(f"{prefix}_spectral_validation_refinement_summary.csv", summary_rows)
    write_csv(f"{prefix}_spectral_validation_band_diagnosis.csv", band_rows)
    write_csv(f"{prefix}_spectral_validation_recommendations.csv", recommendation)

    for path, content in [
        (args.report_md, build_report(target_summary, stable_rows, run_summary_rows, focus_summary_rows, pairwise_rows, delta_rows, summary_rows, band_rows, recommendation)),
        (args.lay_md, build_lay_summary(recommendation)),
        (args.recommendation_md, build_recommendation(recommendation)),
        (args.status_md, build_status_note(band_rows, recommendation)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v13j] done")


if __name__ == "__main__":
    main()
