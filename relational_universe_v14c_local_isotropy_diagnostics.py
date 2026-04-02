#!/usr/bin/env python3
"""v0.14c local isotropy diagnostics around the active anchor regime.

This is the next narrow step after v14b. It fixes:
- one regime: band_zero_del
- one perturbation type: local_swap
- matched deep natural bases

and asks whether local support geometry can explain a meaningful part of the
placement-to-placement variation in front measurements.

This is still not a proof of Lorentz symmetry or its absence. It is a local
microframe / anisotropy probe.
"""
from __future__ import annotations

import argparse
import math
import statistics
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14_lorentz_diagnostics as v14


ANCHOR_NAME = v14.ANCHOR_CANDIDATE
PERTURBATION = "local_swap"
FEATURE_CANDIDATES = (
    "support_ball_2",
    "support_ball_3",
    "support_shell_2",
    "mean_support_degree",
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v14.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v14.mean_defined(values)


def sd_or_zero(values: Iterable[float]) -> float:
    return v14.sd_or_zero(values)


def quantile(values: Sequence[float], q: float) -> float:
    return v14.quantile(values, q)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v10b.write_csv(path, rows)


def anchor_spec() -> Dict[str, Any]:
    return {
        "candidate": v09.ScaleCandidate(ANCHOR_NAME, 0.02, 0.00, 0.02, 0.00, 0.00),
        "candidate_role": "anchor",
    }


def deep_ensembles(targets: Sequence[int]) -> List[v10b.CalibrationEnsemble]:
    return [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]


def ball_and_shell_counts(g: v7.UGraph, support: Sequence[int], r_max: int = 3) -> Dict[str, float]:
    dist = v7.bfs_distances(g, support)
    balls: Dict[int, int] = {}
    shells: Dict[int, int] = {}
    for r in range(r_max + 1):
        balls[r] = sum(1 for d in dist.values() if d <= r)
        shells[r] = sum(1 for d in dist.values() if d == r)
    out: Dict[str, float] = {}
    for r in range(1, r_max + 1):
        out[f"support_ball_{r}"] = float(balls[r])
        out[f"support_shell_{r}"] = float(shells[r])
    return out


def support_geometry_features(base_state: v7.State, support: Sequence[int]) -> Dict[str, float]:
    degs = [base_state.g.degree(v) for v in support if v in base_state.g.adj]
    mean_deg = float(sum(degs) / len(degs)) if degs else 0.0
    min_deg = float(min(degs)) if degs else 0.0
    max_deg = float(max(degs)) if degs else 0.0
    ball_shell = ball_and_shell_counts(base_state.g, support, r_max=3)
    shell1 = max(1.0, ball_shell.get("support_shell_1", 0.0))
    shell2 = ball_shell.get("support_shell_2", 0.0)
    ball1 = max(1.0, ball_shell.get("support_ball_1", 0.0))
    ball3 = ball_shell.get("support_ball_3", 0.0)
    return {
        "support_size": float(len(support)),
        "mean_support_degree": mean_deg,
        "min_support_degree": min_deg,
        "max_support_degree": max_deg,
        **ball_shell,
        "shell2_over_shell1": float(shell2 / shell1),
        "ball3_over_ball1": float(ball3 / ball1),
    }


def pearson_corr(xs: Sequence[float], ys: Sequence[float]) -> float:
    pts = [
        (float(x), float(y))
        for x, y in zip(xs, ys)
        if math.isfinite(float(x)) and math.isfinite(float(y))
    ]
    if len(pts) < 2:
        return float("nan")
    xbar = statistics.mean(x for x, _ in pts)
    ybar = statistics.mean(y for _, y in pts)
    sxx = sum((x - xbar) ** 2 for x, _ in pts)
    syy = sum((y - ybar) ** 2 for _, y in pts)
    if sxx <= 0.0 or syy <= 0.0:
        return float("nan")
    sxy = sum((x - xbar) * (y - ybar) for x, y in pts)
    return float(sxy / math.sqrt(sxx * syy))


def rank_values(values: Sequence[float]) -> List[float]:
    vals = [float(v) for v in values]
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    ranks = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg_rank = 0.5 * (i + j) + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    return ranks


def spearman_corr(xs: Sequence[float], ys: Sequence[float]) -> float:
    pts = [
        (float(x), float(y))
        for x, y in zip(xs, ys)
        if math.isfinite(float(x)) and math.isfinite(float(y))
    ]
    if len(pts) < 2:
        return float("nan")
    rx = rank_values([x for x, _ in pts])
    ry = rank_values([y for _, y in pts])
    return pearson_corr(rx, ry)


def collect_run_rows(
    spec: Mapping[str, Any],
    ensembles: Sequence[v10b.CalibrationEnsemble],
    base_states: Mapping[Tuple[str, int], Any],
    growth_seeds: Sequence[int],
    run_offsets: Sequence[int],
    placement_count: int,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    cand = spec["candidate"]
    params = v09.candidate_to_params(cand)
    for ens in ensembles:
        for gseed in growth_seeds:
            base = base_states[(ens.name, int(gseed))]
            token_count = max(1, len(base.sorted_token_ids()))
            placements = list(range(min(int(placement_count), token_count)))
            steps = v10e.steps_for_state(base.g.num_nodes())
            log_every = max(12, min(80, steps // 10))
            for run_offset in run_offsets:
                run_seed = int(ens.target_nodes) * 100000 + int(gseed) * 1000 + int(run_offset)
                for placement in placements:
                    res = v14.run_coupled_from_base_with_info(
                        base,
                        params=params,
                        seed=run_seed,
                        steps=steps,
                        perturbation=PERTURBATION,
                        center_token_index=placement,
                        local_coupling="maximal",
                        log_every=log_every,
                    )
                    perturb_info = res["perturbation_info"]
                    actual = str(perturb_info.get("type", "unknown"))
                    requested_match = v14.perturbation_requested_match(PERTURBATION, actual)
                    support = list(perturb_info.get("support", []))
                    geom = support_geometry_features(base, support)
                    hm = res["headline_metrics"]
                    rows.append(
                        {
                            "candidate_name": cand.name,
                            "ensemble": ens.name,
                            "target_nodes": ens.target_nodes,
                            "growth_seed": int(gseed),
                            "run_offset": int(run_offset),
                            "run_seed": int(run_seed),
                            "placement_index": int(placement),
                            "requested_match": 1 if requested_match else 0,
                            "actual_perturbation": actual,
                            "support_signature": ",".join(str(x) for x in support),
                            "fit_speed_control": safe_float(hm.get("fit_speed_control")),
                            "hit_t_control_r2": safe_float(hm.get("hit_t_control_r2")),
                            "hit_t_control_r3": safe_float(hm.get("hit_t_control_r3")),
                            "radius_drop_rate_control": safe_float(hm.get("radius_drop_rate_control"), 0.0),
                            "max_ratio_control": safe_float(hm.get("max_ratio_control")),
                            "max_radius_control": safe_float(hm.get("max_radius_control")),
                            "shared_node_fraction_final": safe_float(hm.get("shared_node_fraction_final")),
                            **geom,
                        }
                    )
    return rows


def placement_summary(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: MutableMapping[int, List[Dict[str, Any]]] = {}
    for row in run_rows:
        grouped.setdefault(int(row["placement_index"]), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for placement, rows in sorted(grouped.items()):
        out.append(
            {
                "placement_index": placement,
                "n_runs": len(rows),
                "strict_match_rate": mean_defined(float(r["requested_match"]) for r in rows),
                "unique_support_signatures": len({str(r["support_signature"]) for r in rows}),
                "mean_fit_speed_control": mean_defined(safe_float(r["fit_speed_control"]) for r in rows),
                "mean_hit_t_control_r2": mean_defined(safe_float(r["hit_t_control_r2"]) for r in rows),
                "mean_support_ball_2": mean_defined(safe_float(r["support_ball_2"]) for r in rows),
                "mean_support_ball_3": mean_defined(safe_float(r["support_ball_3"]) for r in rows),
                "mean_support_degree": mean_defined(safe_float(r["mean_support_degree"]) for r in rows),
            }
        )
    return out


def feature_signal_summary(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = [r for r in run_rows if int(r["requested_match"]) == 1]
    out: List[Dict[str, Any]] = []
    fit_speed = [safe_float(r["fit_speed_control"]) for r in rows]
    hit_r2_neg = [-safe_float(r["hit_t_control_r2"]) for r in rows]
    for feature in FEATURE_CANDIDATES:
        feat_vals = [safe_float(r[feature]) for r in rows]
        out.append(
            {
                "feature_name": feature,
                "pearson_vs_fit_speed": pearson_corr(feat_vals, fit_speed),
                "spearman_vs_fit_speed": spearman_corr(feat_vals, fit_speed),
                "pearson_vs_neg_hit_r2": pearson_corr(feat_vals, hit_r2_neg),
                "spearman_vs_neg_hit_r2": spearman_corr(feat_vals, hit_r2_neg),
                "q10_feature": quantile(feat_vals, 0.10),
                "q90_feature": quantile(feat_vals, 0.90),
            }
        )
    return out


def within_base_alignment_summary(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: MutableMapping[Tuple[str, int, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        if int(row["requested_match"]) != 1:
            continue
        key = (str(row["ensemble"]), int(row["growth_seed"]), int(row["run_offset"]))
        grouped.setdefault(key, []).append(dict(row))

    feature_records: MutableMapping[str, List[Dict[str, Any]]] = {feature: [] for feature in FEATURE_CANDIDATES}
    for rows in grouped.values():
        if len(rows) < 2:
            continue
        best_speed = max(rows, key=lambda r: safe_float(r["fit_speed_control"]))
        best_hit = min(rows, key=lambda r: safe_float(r["hit_t_control_r2"]))
        for feature in FEATURE_CANDIDATES:
            best_feature = max(rows, key=lambda r: safe_float(r[feature]))
            feature_records[feature].append(
                {
                    "align_speed": 1 if int(best_feature["placement_index"]) == int(best_speed["placement_index"]) else 0,
                    "align_hit": 1 if int(best_feature["placement_index"]) == int(best_hit["placement_index"]) else 0,
                    "feature_gap": safe_float(best_feature[feature]) - min(safe_float(r[feature]) for r in rows),
                    "speed_gap": safe_float(best_speed["fit_speed_control"]) - min(safe_float(r["fit_speed_control"]) for r in rows),
                    "hit_gap": max(safe_float(r["hit_t_control_r2"]) for r in rows) - safe_float(best_hit["hit_t_control_r2"]),
                }
            )

    out: List[Dict[str, Any]] = []
    for feature, rows in feature_records.items():
        out.append(
            {
                "feature_name": feature,
                "n_matched_bases": len(rows),
                "align_speed_rate": mean_defined(float(r["align_speed"]) for r in rows),
                "align_hit_rate": mean_defined(float(r["align_hit"]) for r in rows),
                "mean_feature_gap": mean_defined(safe_float(r["feature_gap"]) for r in rows),
                "mean_speed_gap": mean_defined(safe_float(r["speed_gap"]) for r in rows),
                "mean_hit_gap": mean_defined(safe_float(r["hit_gap"]) for r in rows),
            }
        )
    return out


def recommendation_rows(
    target_summary: Sequence[Dict[str, Any]],
    placement_rows: Sequence[Dict[str, Any]],
    feature_rows: Sequence[Dict[str, Any]],
    align_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    match_clean = min((safe_float(row["strict_match_rate"], 0.0) for row in placement_rows), default=0.0) >= 0.999
    out.append(
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and match_clean) else "unclear",
            "note": (
                "Startstørrelsene er separert og alle local_swap-placement-rader bruker ønsket perturbasjon."
                if (size_clean and match_clean)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        }
    )

    feature_lookup = {str(r["feature_name"]): dict(r) for r in feature_rows}
    align_lookup = {str(r["feature_name"]): dict(r) for r in align_rows}
    scored: List[Tuple[float, str]] = []
    for feature in FEATURE_CANDIDATES:
        sig = feature_lookup[feature]
        ali = align_lookup[feature]
        signal = mean_defined(
            [
                abs(safe_float(sig["spearman_vs_fit_speed"])),
                abs(safe_float(sig["spearman_vs_neg_hit_r2"])),
                safe_float(ali["align_speed_rate"]),
                safe_float(ali["align_hit_rate"]),
            ]
        )
        scored.append((signal, feature))
    scored.sort(reverse=True)
    best_feature = scored[0][1]
    best_sig = feature_lookup[best_feature]
    best_align = align_lookup[best_feature]
    corr_strength = max(
        abs(safe_float(best_sig["spearman_vs_fit_speed"])),
        abs(safe_float(best_sig["spearman_vs_neg_hit_r2"])),
    )
    align_strength = max(
        safe_float(best_align["align_speed_rate"]),
        safe_float(best_align["align_hit_rate"]),
    )

    if corr_strength >= 0.35 and align_strength >= 0.55:
        status = "anisotropy_supported"
        note = f"Lokal støttegeometri rundt `{best_feature}` ser ut til å forklare en meningsfull del av hastighetsvariasjonen."
    elif corr_strength >= 0.20 and align_strength >= 0.40:
        status = "mixed"
        note = f"`{best_feature}` bærer noe signal, men ikke sterkt nok til å si at lokal mikroframe nå er tydelig støttet."
    else:
        status = "weak"
        note = f"Ingen av de testede støttegeometriene, inkludert `{best_feature}`, forklarer hastighetsvariasjonen særlig godt."

    out.append(
        {
            "diagnostic_family": "local_isotropy_probe",
            "status": status,
            "note": note,
        }
    )
    out.append(
        {
            "diagnostic_family": "next_step",
            "status": (
                "microframe_followup"
                if status == "anisotropy_supported"
                else "pause_lorentz_expansion"
            ),
            "note": (
                "Neste steg kan være en eksplisitt mikroframe-/isotropirunde rundt den beste støttegeometrien."
                if status == "anisotropy_supported"
                else "Ikke utvid Lorentz-sporet bredt ennå; bruk heller dette til å vurdere om videre isotropitesting er verdt kostnaden."
            ),
        }
    )
    return out


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def build_report(
    target_summary: Sequence[Dict[str, Any]],
    placement_rows: Sequence[Dict[str, Any]],
    feature_rows: Sequence[Dict[str, Any]],
    align_rows: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.14c: lokal isotropi-diagnostikk")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden fryser ett regime og én perturbasjonstype (`band_zero_del` + `local_swap`) og tester om lokal støttegeometri kan forklare plasseringsover variasjon i frontmålingene."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Placement-sammendrag")
    lines.append("")
    lines.append("| placement | strict_match | unique_supports | mean fit_speed | mean hit t(r=2) | mean ball2 | mean degree |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in placement_rows:
        lines.append(
            f"| {int(row['placement_index'])} | {fmt(row['strict_match_rate'])} | {int(row['unique_support_signatures'])} | {fmt(row['mean_fit_speed_control'])} | {fmt(row['mean_hit_t_control_r2'])} | {fmt(row['mean_support_ball_2'],1)} | {fmt(row['mean_support_degree'])} |"
        )
    lines.append("")
    lines.append("## Geometrisignal")
    lines.append("")
    lines.append("| feature | spearman vs speed | spearman vs -hit(r2) | q10 | q90 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in feature_rows:
        lines.append(
            f"| {row['feature_name']} | {fmt(row['spearman_vs_fit_speed'])} | {fmt(row['spearman_vs_neg_hit_r2'])} | {fmt(row['q10_feature'])} | {fmt(row['q90_feature'])} |"
        )
    lines.append("")
    lines.append("## Within-base alignment")
    lines.append("")
    lines.append("| feature | align speed | align hit | mean feature gap | mean speed gap | mean hit gap |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in align_rows:
        lines.append(
            f"| {row['feature_name']} | {fmt(row['align_speed_rate'])} | {fmt(row['align_hit_rate'])} | {fmt(row['mean_feature_gap'])} | {fmt(row['mean_speed_gap'])} | {fmt(row['mean_hit_gap'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Hvis støttegeometri predikerer hvilken plassering som får raskest spredning, styrker det at lokal anisotropi / mikroframe er en reell forklaring.")
    lines.append("- Hvis signalet er svakt selv her, er placement-støy fortsatt der, men ikke godt forklart av disse enkle lokale geometrifeaturene.")
    lines.append("- Ingen av delene gir Lorentz-likhet; dette er bare en diagnose av lokal retning-/støttefølsomhet.")
    lines.append("")
    return "\n".join(lines)


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    probe = next((row for row in recommendation if row["diagnostic_family"] == "local_isotropy_probe"), None)
    nxt = next((row for row in recommendation if row["diagnostic_family"] == "next_step"), None)
    return "\n".join(
        [
            "# Relasjonell universgraf v0.14c for ikke-spesialister",
            "",
            "Denne runden testet om forskjeller mellom ulike steder i grafen kan forklares av enkel lokal geometri rundt inngrepet.",
            "",
            f"Hoveddommen er `{probe['status'] if probe else 'ukjent'}`.",
            "",
            f"Det betyr: {probe['note'] if probe else 'ingen oppsummering tilgjengelig.'}",
            "",
            f"Neste anbefaling er: {nxt['note'] if nxt else 'ingen ny anbefaling registrert.'}",
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.14c local isotropy diagnostics.")
    p.add_argument("--targets", type=str, default="48,96,192,256")
    p.add_argument("--growth-seeds", type=str, default="101,202,303")
    p.add_argument("--run-offsets", type=str, default="0,17")
    p.add_argument("--placement-count", type=int, default=6)
    p.add_argument("--out-run-csv", type=str, default="Documentation/v14c_local_isotropy_run_rows.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v14c_local_isotropy_target_summary.csv")
    p.add_argument("--out-placement-csv", type=str, default="Documentation/v14c_local_isotropy_placement_summary.csv")
    p.add_argument("--out-feature-csv", type=str, default="Documentation/v14c_local_isotropy_feature_signal_summary.csv")
    p.add_argument("--out-align-csv", type=str, default="Documentation/v14c_local_isotropy_alignment_summary.csv")
    p.add_argument("--out-recommendation-csv", type=str, default="Documentation/v14c_local_isotropy_recommendations.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v14c_local_isotropy_diagnostics.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_14c.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_14c_operativ_anbefaling.md")
    return p.parse_args()


def parse_int_list(spec: str) -> List[int]:
    return [int(part.strip()) for part in spec.split(",") if part.strip()]


def main() -> None:
    args = parse_args()
    targets = parse_int_list(args.targets)
    growth_seeds = parse_int_list(args.growth_seeds)
    run_offsets = parse_int_list(args.run_offsets)

    spec = anchor_spec()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = deep_ensembles(targets)
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)

    run_rows = collect_run_rows(spec, ensembles, base_states, growth_seeds, run_offsets, args.placement_count)
    placement_rows = placement_summary(run_rows)
    feature_rows = feature_signal_summary(run_rows)
    align_rows = within_base_alignment_summary(run_rows)
    recommendation = recommendation_rows(target_summary, placement_rows, feature_rows, align_rows)

    report_md = build_report(target_summary, placement_rows, feature_rows, align_rows, recommendation)
    lay_md = build_lay_summary(recommendation)
    op_md = "\n".join(
        [
            "# v0.14c operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Ikke les denne runden som et bevis på isotropi eller skjult mikroframe.",
            "- Les den som en lokal test av om enkel støttegeometri faktisk forklarer placement-varians.",
        ]
    )

    write_csv(args.out_run_csv, run_rows)
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_placement_csv, placement_rows)
    write_csv(args.out_feature_csv, feature_rows)
    write_csv(args.out_align_csv, align_rows)
    write_csv(args.out_recommendation_csv, recommendation)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")

    print(f"Wrote {args.out_summary_md}")
    print(f"Wrote {args.out_feature_csv}")
    print(f"Wrote {args.out_align_csv}")


if __name__ == "__main__":
    main()
