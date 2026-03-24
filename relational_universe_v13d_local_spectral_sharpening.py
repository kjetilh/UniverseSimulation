#!/usr/bin/env python3
"""v0.13d local sharpening of the spectral quasi-invariant signal.

This is the next narrow step after v13c. Instead of widening the family or
jumping to a larger validation set, it spends more budget on a tighter local
family where the spectral-vs-dim story was still mixed.
"""
from __future__ import annotations

import argparse
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
FOCUS_METRICS = list(v13c.FOCUS_METRICS)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v12.safe_float(x, default)


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
            "candidate": v09.ScaleCandidate("band_death_0005", 0.02, 0.005, 0.02, 0.00, 0.00),
            "axis_group": "death",
        },
    ]


def candidate_meta() -> Dict[str, Dict[str, Any]]:
    return {spec["candidate"].name: spec for spec in candidate_specs()}


def select_candidate_specs(candidate_names: Sequence[str] | None) -> List[Dict[str, Any]]:
    specs = candidate_specs()
    if not candidate_names:
        return specs
    wanted = {name.strip() for name in candidate_names if name.strip()}
    return [spec for spec in specs if spec["candidate"].name in wanted]


def local_sharpening_summary(
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
        if p_spectral >= 0.80 and mean_margin >= 0.008 and mean_delta <= 0.006:
            local_status = "strong_local"
        elif p_spectral >= 0.65 and mean_margin >= 0.005 and mean_delta <= 0.010:
            local_status = "good_but_local"
        else:
            local_status = "mixed"
        rows.append(
            {
                "candidate_name": candidate_name,
                "axis_group": meta[candidate_name]["axis_group"],
                "spectral_mean_rel_drift": safe_float(spectral["bootstrap_mean_relative_drift"]),
                "spectral_q90_rel_drift": safe_float(spectral["bootstrap_q90_relative_drift"]),
                "dim_mean_rel_drift": safe_float(dim["bootstrap_mean_relative_drift"]),
                "dim_q90_rel_drift": safe_float(dim["bootstrap_q90_relative_drift"]),
                "p_spectral_lt_dim": p_spectral,
                "mean_dim_minus_spectral": mean_margin,
                "spectral_delta_vs_anchor": mean_delta,
                "local_status": local_status,
            }
        )
    return rows


def recommendation_rows(
    local_rows: Sequence[Dict[str, Any]],
    delta_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    zero_rows = [r for r in delta_rows if str(r["metric"]) in ZERO_SANITY_METRICS]
    zero_breaks = any(
        abs(safe_float(r["mean_delta_vs_anchor"])) > 1e-12 or safe_float(r["same_value_rate"]) < 0.999
        for r in zero_rows
    )
    out.append(
        {
            "signal_family": "zero_drift_sanity",
            "status": "breaks_off_anchor" if zero_breaks else "still_exact",
            "best_candidate": "mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel",
            "note": (
                "Null-driftene bryter fortsatt off-anchor og skal behandles som artefakter, ikke lover."
                if zero_breaks
                else "Null-driftene holder fortsatt eksakt i denne lokale skjerpingsrunden."
            ),
        }
    )

    worst_pairwise = min(safe_float(r["p_spectral_lt_dim"]) for r in local_rows) if local_rows else float("nan")
    worst_margin = min(safe_float(r["mean_dim_minus_spectral"]) for r in local_rows) if local_rows else float("nan")
    max_delta = max(abs(safe_float(r["spectral_delta_vs_anchor"])) for r in local_rows) if local_rows else float("nan")
    strong_count = sum(1 for r in local_rows if str(r["local_status"]) == "strong_local")
    mixed_count = sum(1 for r in local_rows if str(r["local_status"]) == "mixed")

    if mixed_count == 0 and worst_pairwise >= 0.75 and worst_margin >= 0.006 and max_delta <= 0.008:
        status = "good_but_local"
        note = "Spektraldriften er nå skarp nok i den lokale familien til å fortjene en større, målrettet valideringsrunde."
        validation_status = "yes_targeted"
        validation_note = "Bruk neste større valideringssett på spektral quasi-invariant-testing med `dim_proxy` som sekundær kontroll."
    elif strong_count >= 2 and worst_pairwise >= 0.65 and max_delta <= 0.010:
        status = "mixed_but_improving"
        note = "Spektraldriften skjerpes lokalt, men det finnes fortsatt minst ett knife-edge-regime som holder signalet blandet."
        validation_status = "not_yet"
        validation_note = "Vent med større valideringssett til knife-edge-regimet er bedre avklart."
    else:
        status = "mixed"
        note = "Spektraldriften er fortsatt interessant, men ikke skarp nok lokalt til å rettferdiggjøre større valideringssett."
        validation_status = "not_yet"
        validation_note = "Vent med større valideringssett til det lokale spektralsporet er skarpere."

    out.append(
        {
            "signal_family": "spectral_quasi_invariant",
            "status": status,
            "best_candidate": SPECTRAL_METRIC,
            "note": note,
        }
    )
    out.append(
        {
            "signal_family": "larger_validation_set",
            "status": validation_status,
            "best_candidate": "spectral_vs_dim_local_sharpening",
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
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.13d: lokal skjerping av spektral quasi-invariant")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden gjør ikke familien bredere. Den bruker mer budsjett på et stramt lokalt regime-sett for å se om spektraldriften blir skarpere enn `dim_proxy` akkurat der `v13c` fortsatt var blandet."
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
    lines.append("## Lokal spektral-vs-dim-summering")
    lines.append("")
    lines.append("| regime | axis | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | local_status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in local_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['axis_group']} | {safe_float(row['spectral_mean_rel_drift']):.4f} | "
            f"{safe_float(row['dim_mean_rel_drift']):.4f} | {safe_float(row['p_spectral_lt_dim']):.3f} | "
            f"{safe_float(row['mean_dim_minus_spectral']):.4f} | {safe_float(row['spectral_delta_vs_anchor']):.4f} | {row['local_status']} |"
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
    lines.append("- Denne runden bruker mer diskrimineringsbudsjett per regime i stedet for å gjøre familien bredere.")
    lines.append("- Hvis spektraldriften fortsatt ikke skiller seg tydelig fra `dim_proxy` her, bør vi være forsiktige med større valideringssett.")
    lines.append("- Hvis den derimot skjerpes i knife-edge-regimene, er det et bedre grunnlag for målrettet oppskalering enn `v13c` ga alene.")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    spectral = next((r for r in recommendation if str(r["signal_family"]) == "spectral_quasi_invariant"), None)
    validation = next((r for r in recommendation if str(r["signal_family"]) == "larger_validation_set"), None)
    lines = [
        "# v0.13d for ikke-spesialister",
        "",
        "Denne runden gjør ikke testen bredere. Den prøver bare å avgjøre om spektralsporet blir tydeligere når vi bruker mer budsjett på de nærmeste og vanskeligste regimene.",
        "",
    ]
    if spectral is not None:
        lines.append(f"- Spektralsporet: `{spectral['status']}`.")
    if validation is not None:
        lines.append(f"- Større valideringssett: `{validation['status']}`.")
    lines.extend(["", "Poenget er å gjøre signalet skarpere før vi bruker mer budsjett bredt.", ""])
    return "\n".join(lines)


def build_recommendation(recommendation: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.13d operativ anbefaling", ""]
    for row in recommendation:
        lines.append(f"- {row['signal_family']}: {row['note']}")
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.13d local spectral sharpening")
    ap.add_argument("--growth-regime", default="fast_balanced")
    ap.add_argument("--targets", default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=7)
    ap.add_argument("--run-seeds", type=int, default=7)
    ap.add_argument("--bootstrap-reps", type=int, default=300)
    ap.add_argument("--candidate-names", default="")
    ap.add_argument("--output-prefix", default="Documentation/v13d")
    ap.add_argument("--report-md", default="Documentation/v13d_local_spectral_sharpening.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_13d.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_13d_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    regime = v10e.recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]
    candidate_names = [x for x in args.candidate_names.split(",") if x.strip()]
    specs = select_candidate_specs(candidate_names)
    candidates = [spec["candidate"] for spec in specs]
    meta = {spec["candidate"].name: spec for spec in specs}
    growth_seeds = [61001 + 23 * i for i in range(args.growth_seeds)]
    run_offsets = [35001 + 31 * i for i in range(args.run_seeds)]

    print(
        f"[v13d] regime={regime.name} targets={targets} candidates={[c.name for c in candidates]} "
        f"growth={len(growth_seeds)} runs={len(run_offsets)} boot={args.bootstrap_reps}"
    )
    print("[v13d] building bases...")
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    base_lookup = {(str(r['ensemble']), int(r['growth_seed'])): dict(r) for r in base_rows}
    print("[v13d] bases done")

    print("[v13d] collecting run rows...")
    raw_run_rows = v10e.collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    run_rows = [v12.enrich_run_row(row, base_lookup) for row in raw_run_rows]
    print(f"[v13d] runs done: {len(run_rows)} rows")

    print("[v13d] aggregating candidate/base rows...")
    candidate_base_rows = v13b.grouped_candidate_base_rows(base_rows, run_rows)
    stable_rows = v13.stable_control_summary(base_rows, args.bootstrap_reps, seed=31001) if hasattr(v13, "stable_control_summary") else v13.feature_stability_bootstrap_summary(base_rows, args.bootstrap_reps, 31001)[1]
    run_summary_rows = v13b.regime_run_summary(candidate_base_rows, meta)
    print("[v13d] bootstrap: focus drift summary...")
    focus_boot_rows, focus_summary_rows = v13c.focus_bootstrap_summary(candidate_base_rows, meta, args.bootstrap_reps, seed=31041)
    print("[v13d] paired spectral-vs-dim comparison...")
    pairwise_rows = v13c.spectral_dim_pairwise_summary(candidate_base_rows, meta)
    print("[v13d] off-anchor deltas vs anchor...")
    delta_rows = v13c.anchor_focus_delta_summary(candidate_base_rows, meta)
    local_rows = local_sharpening_summary(focus_summary_rows, pairwise_rows, delta_rows, meta)
    recommendation = recommendation_rows(local_rows, delta_rows)

    print("[v13d] writing outputs...")
    prefix = args.output_prefix
    write_csv(f"{prefix}_spectral_validation_base_rows.csv", candidate_base_rows)
    write_csv(f"{prefix}_spectral_validation_target_summary.csv", list(target_summary))
    write_csv(f"{prefix}_spectral_validation_run_summary.csv", run_summary_rows)
    write_csv(f"{prefix}_spectral_validation_focus_bootstrap_rows.csv", focus_boot_rows)
    write_csv(f"{prefix}_spectral_validation_focus_summary.csv", focus_summary_rows)
    write_csv(f"{prefix}_spectral_validation_pairwise_summary.csv", pairwise_rows)
    write_csv(f"{prefix}_spectral_validation_anchor_delta_summary.csv", delta_rows)
    write_csv(f"{prefix}_spectral_validation_local_summary.csv", local_rows)
    write_csv(f"{prefix}_spectral_validation_recommendations.csv", recommendation)

    for path, content in [
        (args.report_md, build_report(target_summary, stable_rows, run_summary_rows, focus_summary_rows, pairwise_rows, delta_rows, local_rows, recommendation)),
        (args.lay_md, build_lay_summary(recommendation)),
        (args.recommendation_md, build_recommendation(recommendation)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
    print("[v13d] done")


if __name__ == "__main__":
    main()
