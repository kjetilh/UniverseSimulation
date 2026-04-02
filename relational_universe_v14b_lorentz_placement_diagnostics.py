#!/usr/bin/env python3
"""v0.14b placement-aware Lorentz diagnostics.

This round narrows the follow-up to the cleanest remaining ambiguity after v0.14:
is the observed front-speed difference mainly a perturbation-mode effect, or can
it be explained by local placement anisotropy on the same base graphs?

Method:
- keep the same deep natural ensembles and same matched base states as v0.14
- keep the same two nearby regimes: band_zero_del and band_pdel_0005
- compare only the two structural perturbations: local_swap and add_chord
- rerun each perturbation from several local center-token placements on the same
  base state and same stochastic seed
- compare between-mode gaps against within-mode placement gaps

This is still not a Lorentz proof. It is an artifact-sensitive diagnostic.
"""
from __future__ import annotations

import argparse
import math
import statistics
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14_lorentz_diagnostics as v14


PLACEMENTS = (0, 1, 2, 3)
PERTURBATIONS = ("local_swap", "add_chord")


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


def candidate_specs() -> List[Dict[str, Any]]:
    return v14.candidate_specs()


def deep_ensembles(targets: Sequence[int]) -> List[v10b.CalibrationEnsemble]:
    return v14.deep_ensembles(targets)


def steps_for_state(nodes: int) -> int:
    return v10e.steps_for_state(nodes)


def collect_run_rows(
    specs: Sequence[Dict[str, Any]],
    ensembles: Sequence[v10b.CalibrationEnsemble],
    base_states: Mapping[Tuple[str, int], Any],
    growth_seeds: Sequence[int],
    run_offsets: Sequence[int],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for spec in specs:
        cand = spec["candidate"]
        params = v09.candidate_to_params(cand)
        for ens in ensembles:
            for gseed in growth_seeds:
                base = base_states[(ens.name, int(gseed))]
                steps = steps_for_state(base.g.num_nodes())
                log_every = max(12, min(80, steps // 10))
                for run_offset in run_offsets:
                    run_seed = int(ens.target_nodes) * 100000 + int(gseed) * 1000 + int(run_offset)
                    for placement in PLACEMENTS:
                        for requested in PERTURBATIONS:
                            res = v14.run_coupled_from_base_with_info(
                                base,
                                params=params,
                                seed=run_seed,
                                steps=steps,
                                perturbation=requested,
                                center_token_index=placement,
                                local_coupling="maximal",
                                log_every=log_every,
                            )
                            hm = res["headline_metrics"]
                            init = res["initial_control_features"]
                            perturb_info = res["perturbation_info"]
                            actual = str(perturb_info.get("type", "unknown"))
                            actual_category = v14.perturbation_category(actual)
                            requested_match = v14.perturbation_requested_match(requested, actual)
                            support = perturb_info.get("support", [])
                            rows.append(
                                {
                                    "candidate_name": cand.name,
                                    "candidate_role": spec["candidate_role"],
                                    "ensemble": ens.name,
                                    "burnin_label": ens.burnin_label,
                                    "target_nodes": ens.target_nodes,
                                    "growth_seed": int(gseed),
                                    "run_offset": int(run_offset),
                                    "run_seed": int(run_seed),
                                    "placement_index": int(placement),
                                    "steps": int(steps),
                                    "requested_perturbation": requested,
                                    "actual_perturbation": actual,
                                    "actual_perturbation_category": actual_category,
                                    "requested_match": 1 if requested_match else 0,
                                    "fallback_used": 0 if requested_match else 1,
                                    "support_signature": ",".join(str(x) for x in support),
                                    "support_size": len(support),
                                    "initial_nodes": safe_float(init.get("nodes")),
                                    "fit_speed_control": safe_float(hm.get("fit_speed_control")),
                                    "max_ratio_control": safe_float(hm.get("max_ratio_control")),
                                    "hit_t_control_r2": safe_float(hm.get("hit_t_control_r2")),
                                    "hit_t_control_r3": safe_float(hm.get("hit_t_control_r3")),
                                    "radius_drop_rate_control": safe_float(hm.get("radius_drop_rate_control"), 0.0),
                                    "final_radius_control": safe_float(hm.get("final_radius_control")),
                                    "max_radius_control": safe_float(hm.get("max_radius_control")),
                                    "shared_node_fraction_final": safe_float(hm.get("shared_node_fraction_final")),
                                }
                            )
    return rows


def aggregate_by_placement(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: MutableMapping[Tuple[str, str, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        key = (
            str(row["candidate_name"]),
            str(row["requested_perturbation"]),
            int(row["placement_index"]),
        )
        grouped.setdefault(key, []).append(dict(row))

    out: List[Dict[str, Any]] = []
    for (candidate_name, perturbation, placement), rows in sorted(grouped.items()):
        out.append(
            {
                "candidate_name": candidate_name,
                "requested_perturbation": perturbation,
                "placement_index": placement,
                "n_runs": len(rows),
                "strict_match_rate": mean_defined(float(r["requested_match"]) for r in rows),
                "unique_support_signatures": len({str(r["support_signature"]) for r in rows}),
                "mean_fit_speed_control": mean_defined(safe_float(r["fit_speed_control"]) for r in rows),
                "sd_fit_speed_control": sd_or_zero(safe_float(r["fit_speed_control"]) for r in rows),
                "mean_hit_t_control_r2": mean_defined(safe_float(r["hit_t_control_r2"]) for r in rows),
                "mean_hit_t_control_r3": mean_defined(safe_float(r["hit_t_control_r3"]) for r in rows),
                "mean_radius_drop_rate": mean_defined(safe_float(r["radius_drop_rate_control"]) for r in rows),
                "mean_shared_node_fraction_final": mean_defined(safe_float(r["shared_node_fraction_final"]) for r in rows),
            }
        )
    return out


def within_mode_placement_summary(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: MutableMapping[Tuple[str, str, str, int, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        key = (
            str(row["candidate_name"]),
            str(row["requested_perturbation"]),
            str(row["ensemble"]),
            int(row["growth_seed"]),
            int(row["run_offset"]),
        )
        grouped.setdefault(key, []).append(dict(row))

    records: MutableMapping[Tuple[str, str], List[Dict[str, Any]]] = {}
    for (candidate_name, perturbation, _, _, _), rows in grouped.items():
        by_place = {int(r["placement_index"]): r for r in rows if int(r["requested_match"]) == 1}
        for left, right in combinations(sorted(by_place), 2):
            lrow = by_place[left]
            rrow = by_place[right]
            mean_speed_mag = max(
                1e-9,
                0.5 * (abs(safe_float(lrow["fit_speed_control"])) + abs(safe_float(rrow["fit_speed_control"]))),
            )
            mean_hit_mag = max(
                1e-9,
                0.5 * (
                    abs(safe_float(lrow["hit_t_control_r2"], 0.0)) +
                    abs(safe_float(rrow["hit_t_control_r2"], 0.0))
                ),
            )
            records.setdefault((candidate_name, perturbation), []).append(
                {
                    "abs_delta_fit_speed": abs(safe_float(lrow["fit_speed_control"]) - safe_float(rrow["fit_speed_control"])),
                    "rel_delta_fit_speed": abs(safe_float(lrow["fit_speed_control"]) - safe_float(rrow["fit_speed_control"])) / mean_speed_mag,
                    "abs_delta_hit_t_r2": abs(safe_float(lrow["hit_t_control_r2"]) - safe_float(rrow["hit_t_control_r2"])),
                    "rel_delta_hit_t_r2": abs(safe_float(lrow["hit_t_control_r2"]) - safe_float(rrow["hit_t_control_r2"])) / mean_hit_mag,
                    "abs_delta_hit_t_r3": abs(safe_float(lrow["hit_t_control_r3"]) - safe_float(rrow["hit_t_control_r3"])),
                    "abs_delta_radius_drop": abs(safe_float(lrow["radius_drop_rate_control"]) - safe_float(rrow["radius_drop_rate_control"])),
                    "same_support": 1 if str(lrow["support_signature"]) == str(rrow["support_signature"]) else 0,
                }
            )

    out: List[Dict[str, Any]] = []
    for (candidate_name, perturbation), rows in sorted(records.items()):
        out.append(
            {
                "candidate_name": candidate_name,
                "requested_perturbation": perturbation,
                "n_pairs": len(rows),
                "mean_abs_delta_fit_speed": mean_defined(safe_float(r["abs_delta_fit_speed"]) for r in rows),
                "mean_rel_delta_fit_speed": mean_defined(safe_float(r["rel_delta_fit_speed"]) for r in rows),
                "mean_abs_delta_hit_t_r2": mean_defined(safe_float(r["abs_delta_hit_t_r2"]) for r in rows),
                "mean_rel_delta_hit_t_r2": mean_defined(safe_float(r["rel_delta_hit_t_r2"]) for r in rows),
                "mean_abs_delta_hit_t_r3": mean_defined(safe_float(r["abs_delta_hit_t_r3"]) for r in rows),
                "mean_abs_delta_radius_drop": mean_defined(safe_float(r["abs_delta_radius_drop"]) for r in rows),
                "same_support_rate": mean_defined(float(r["same_support"]) for r in rows),
            }
        )
    return out


def between_mode_same_placement_summary(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: MutableMapping[Tuple[str, str, int, int, int], Dict[str, Dict[str, Any]]] = {}
    for row in run_rows:
        if int(row["requested_match"]) != 1:
            continue
        key = (
            str(row["candidate_name"]),
            str(row["ensemble"]),
            int(row["growth_seed"]),
            int(row["run_offset"]),
            int(row["placement_index"]),
        )
        grouped.setdefault(key, {})[str(row["requested_perturbation"])] = dict(row)

    records: MutableMapping[str, List[Dict[str, Any]]] = {}
    for (candidate_name, _, _, _, _), lookup in grouped.items():
        if not all(name in lookup for name in PERTURBATIONS):
            continue
        left = lookup["local_swap"]
        right = lookup["add_chord"]
        mean_speed_mag = max(
            1e-9,
            0.5 * (abs(safe_float(left["fit_speed_control"])) + abs(safe_float(right["fit_speed_control"]))),
        )
        mean_hit_mag = max(
            1e-9,
            0.5 * (
                abs(safe_float(left["hit_t_control_r2"], 0.0)) +
                abs(safe_float(right["hit_t_control_r2"], 0.0))
            ),
        )
        records.setdefault(candidate_name, []).append(
            {
                "abs_delta_fit_speed": abs(safe_float(left["fit_speed_control"]) - safe_float(right["fit_speed_control"])),
                "rel_delta_fit_speed": abs(safe_float(left["fit_speed_control"]) - safe_float(right["fit_speed_control"])) / mean_speed_mag,
                "abs_delta_hit_t_r2": abs(safe_float(left["hit_t_control_r2"]) - safe_float(right["hit_t_control_r2"])),
                "rel_delta_hit_t_r2": abs(safe_float(left["hit_t_control_r2"]) - safe_float(right["hit_t_control_r2"])) / mean_hit_mag,
                "abs_delta_hit_t_r3": abs(safe_float(left["hit_t_control_r3"]) - safe_float(right["hit_t_control_r3"])),
                "abs_delta_radius_drop": abs(safe_float(left["radius_drop_rate_control"]) - safe_float(right["radius_drop_rate_control"])),
                "abs_delta_support": abs(safe_float(left["support_size"]) - safe_float(right["support_size"])),
            }
        )

    out: List[Dict[str, Any]] = []
    for candidate_name, rows in sorted(records.items()):
        out.append(
            {
                "candidate_name": candidate_name,
                "n_pairs": len(rows),
                "mean_abs_delta_fit_speed": mean_defined(safe_float(r["abs_delta_fit_speed"]) for r in rows),
                "mean_rel_delta_fit_speed": mean_defined(safe_float(r["rel_delta_fit_speed"]) for r in rows),
                "mean_abs_delta_hit_t_r2": mean_defined(safe_float(r["abs_delta_hit_t_r2"]) for r in rows),
                "mean_rel_delta_hit_t_r2": mean_defined(safe_float(r["rel_delta_hit_t_r2"]) for r in rows),
                "mean_abs_delta_hit_t_r3": mean_defined(safe_float(r["abs_delta_hit_t_r3"]) for r in rows),
                "mean_abs_delta_radius_drop": mean_defined(safe_float(r["abs_delta_radius_drop"]) for r in rows),
                "mean_abs_delta_support": mean_defined(safe_float(r["abs_delta_support"]) for r in rows),
            }
        )
    return out


def placement_vs_mode_diagnosis(
    within_rows: Sequence[Dict[str, Any]],
    between_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    within_lookup = {(str(r["candidate_name"]), str(r["requested_perturbation"])): dict(r) for r in within_rows}
    between_lookup = {str(r["candidate_name"]): dict(r) for r in between_rows}
    out: List[Dict[str, Any]] = []
    for candidate_name, mode_row in sorted(between_lookup.items()):
        swap = within_lookup[(candidate_name, "local_swap")]
        chord = within_lookup[(candidate_name, "add_chord")]
        within_rel_speed = mean_defined([
            safe_float(swap["mean_rel_delta_fit_speed"]),
            safe_float(chord["mean_rel_delta_fit_speed"]),
        ])
        within_rel_hit = mean_defined([
            safe_float(swap["mean_rel_delta_hit_t_r2"]),
            safe_float(chord["mean_rel_delta_hit_t_r2"]),
        ])
        mode_rel_speed = safe_float(mode_row["mean_rel_delta_fit_speed"])
        mode_rel_hit = safe_float(mode_row["mean_rel_delta_hit_t_r2"])
        speed_ratio = mode_rel_speed / max(1e-9, within_rel_speed)
        hit_ratio = mode_rel_hit / max(1e-9, within_rel_hit)
        if speed_ratio >= 1.25 and hit_ratio >= 1.05:
            status = "mode_gap_stronger_than_placement"
        elif speed_ratio <= 1.05:
            status = "placement_noise_competes"
        else:
            status = "still_mixed"
        out.append(
            {
                "candidate_name": candidate_name,
                "within_rel_speed_mean": within_rel_speed,
                "within_rel_hit_r2_mean": within_rel_hit,
                "mode_rel_speed_mean": mode_rel_speed,
                "mode_rel_hit_r2_mean": mode_rel_hit,
                "speed_ratio_mode_over_within": speed_ratio,
                "hit_ratio_mode_over_within": hit_ratio,
                "diagnosis": status,
            }
        )
    return out


def recommendation_rows(
    target_summary: Sequence[Dict[str, Any]],
    placement_rows: Sequence[Dict[str, Any]],
    within_rows: Sequence[Dict[str, Any]],
    between_rows: Sequence[Dict[str, Any]],
    diagnosis_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    support_clean = min((safe_float(r["strict_match_rate"], 0.0) for r in placement_rows), default=0.0) >= 0.999
    out.append(
        {
            "diagnostic_family": "generator_and_placement_artifacts",
            "status": "clean" if (size_clean and support_clean) else "unclear",
            "note": (
                "Startstørrelsene er separert og alle placement-rader bruker ønsket perturbasjonstype."
                if (size_clean and support_clean)
                else "Enten størrelsene eller placement-matchingen er uklare; les isotropi-resultatet forsiktig."
            ),
        }
    )
    anchor_diag = next((r for r in diagnosis_rows if str(r["candidate_name"]) == v14.ANCHOR_CANDIDATE), None)
    control_diag = next((r for r in diagnosis_rows if str(r["candidate_name"]) == v14.CONTROL_CANDIDATE), None)
    anchor_status = str(anchor_diag["diagnosis"]) if anchor_diag else "unknown"
    control_status = str(control_diag["diagnosis"]) if control_diag else "unknown"

    if anchor_status == "mode_gap_stronger_than_placement" and control_status in {"mode_gap_stronger_than_placement", "still_mixed"}:
        status = "mode_dependence_strengthened"
        note = "Mellom-modus-gapet er storre enn typisk plasseringsover variasjon, sa v14-signalet ser mindre ut som ren lokal anisotropi."
    elif anchor_status == "placement_noise_competes":
        status = "anisotropy_not_ruled_out"
        note = "Plasseringsover variasjon i ankerregimet er naer nok mellom-modus-gapet til at Lorentz-sporet fortsatt er uklart."
    else:
        status = "still_mixed"
        note = "Plasseringstestene skjerper bildet noe, men ikke nok til a avklare Lorentz-sporet rent."

    out.append(
        {
            "diagnostic_family": "mode_vs_placement",
            "status": status,
            "note": note,
        }
    )
    out.append(
        {
            "diagnostic_family": "next_step",
            "status": (
                "isotropy_followup"
                if status == "mode_dependence_strengthened"
                else "keep_narrow_same_family"
            ),
            "note": (
                "Neste steg bor vaere en smal isotropi-runde med samme perturbasjonstype pa flere lokale retninger eller stotter."
                if status == "mode_dependence_strengthened"
                else "Neste steg bor fortsatt vaere smalt i samme familie; ikke oppskaler til stort valideringssett ennå."
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
    within_rows: Sequence[Dict[str, Any]],
    between_rows: Sequence[Dict[str, Any]],
    diagnosis_rows: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.14b: placement-aware Lorentz-diagnostikk")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester om forskjellen mellom `local_swap` og `add_chord` i v0.14 hovedsakelig var en ekte modusforskjell, eller om samme type inngrep varierer nesten like mye bare fordi vi treffer ulike lokale plasseringer."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Placement-sammendrag")
    lines.append("")
    lines.append("| regime | perturbation | placement | strict_match | unique_supports | mean fit_speed | mean hit t(r=2) |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in placement_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['requested_perturbation']} | {int(row['placement_index'])} | {fmt(row['strict_match_rate'])} | {int(row['unique_support_signatures'])} | {fmt(row['mean_fit_speed_control'])} | {fmt(row['mean_hit_t_control_r2'])} |"
        )
    lines.append("")
    lines.append("## Variasjon innen samme modus over plasseringer")
    lines.append("")
    lines.append("| regime | perturbation | rel speed gap | rel hit gap r2 | same support rate |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in within_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['requested_perturbation']} | {fmt(row['mean_rel_delta_fit_speed'])} | {fmt(row['mean_rel_delta_hit_t_r2'])} | {fmt(row['same_support_rate'])} |"
        )
    lines.append("")
    lines.append("## Variasjon mellom modus ved samme plassering")
    lines.append("")
    lines.append("| regime | rel speed gap | rel hit gap r2 | support gap |")
    lines.append("| --- | --- | --- | --- |")
    for row in between_rows:
        lines.append(
            f"| {row['candidate_name']} | {fmt(row['mean_rel_delta_fit_speed'])} | {fmt(row['mean_rel_delta_hit_t_r2'])} | {fmt(row['mean_abs_delta_support'],1)} |"
        )
    lines.append("")
    lines.append("## Diagnose: modus vs plassering")
    lines.append("")
    lines.append("| regime | within rel speed | mode rel speed | speed ratio | diagnosis |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in diagnosis_rows:
        lines.append(
            f"| {row['candidate_name']} | {fmt(row['within_rel_speed_mean'])} | {fmt(row['mode_rel_speed_mean'])} | {fmt(row['speed_ratio_mode_over_within'])} | {row['diagnosis']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Hvis mellom-modus-gapet er storre enn typisk within-modus-gap, styrker det at v14 faktisk sa en reell modusavhengighet.")
    lines.append("- Hvis within-modus-gapet er nesten like stort, er lokal anisotropi fortsatt en sterk alternativ forklaring.")
    lines.append("- Ingen av delene er i seg selv Lorentz-likhet; dette er fortsatt bare en smal diagnostikk.")
    lines.append("")
    return "\n".join(lines)


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    mode_row = next((row for row in recommendation if row["diagnostic_family"] == "mode_vs_placement"), None)
    next_row = next((row for row in recommendation if row["diagnostic_family"] == "next_step"), None)
    lines = [
        "# Relasjonell universgraf v0.14b for ikke-spesialister",
        "",
        "Denne runden spurte om forskjellen mellom to typer små inngrep i grafen kanskje bare skyldes at vi traff ulike steder i grafen, ikke at inngrepstypene faktisk oppfører seg forskjellig.",
        "",
        f"Hoveddommen er `{mode_row['status'] if mode_row else 'ukjent'}`.",
        "",
        f"Det betyr: {mode_row['note'] if mode_row else 'ingen oppsummering tilgjengelig.'}",
        "",
        f"Neste anbefaling er: {next_row['note'] if next_row else 'ingen ny anbefaling registrert.'}",
        "",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.14b placement-aware Lorentz diagnostics.")
    p.add_argument("--targets", type=str, default="48,96,192,256")
    p.add_argument("--growth-seeds", type=str, default="101,202")
    p.add_argument("--run-offsets", type=str, default="0,17")
    p.add_argument("--out-run-csv", type=str, default="Documentation/v14b_lorentz_placement_run_rows.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v14b_lorentz_placement_target_summary.csv")
    p.add_argument("--out-placement-csv", type=str, default="Documentation/v14b_lorentz_placement_summary.csv")
    p.add_argument("--out-within-csv", type=str, default="Documentation/v14b_lorentz_within_mode_summary.csv")
    p.add_argument("--out-between-csv", type=str, default="Documentation/v14b_lorentz_between_mode_summary.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v14b_lorentz_mode_vs_placement_diagnosis.csv")
    p.add_argument("--out-recommendation-csv", type=str, default="Documentation/v14b_lorentz_recommendations.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v14b_lorentz_placement_diagnostics.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_14b.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_14b_operativ_anbefaling.md")
    return p.parse_args()


def parse_int_list(spec: str) -> List[int]:
    return [int(part.strip()) for part in spec.split(",") if part.strip()]


def main() -> None:
    args = parse_args()
    targets = parse_int_list(args.targets)
    growth_seeds = parse_int_list(args.growth_seeds)
    run_offsets = parse_int_list(args.run_offsets)

    specs = candidate_specs()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = deep_ensembles(targets)
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)

    run_rows = collect_run_rows(specs, ensembles, base_states, growth_seeds, run_offsets)
    placement_rows = aggregate_by_placement(run_rows)
    within_rows = within_mode_placement_summary(run_rows)
    between_rows = between_mode_same_placement_summary(run_rows)
    diagnosis_rows = placement_vs_mode_diagnosis(within_rows, between_rows)
    recommendation = recommendation_rows(target_summary, placement_rows, within_rows, between_rows, diagnosis_rows)

    report_md = build_report(target_summary, placement_rows, within_rows, between_rows, diagnosis_rows, recommendation)
    lay_md = build_lay_summary(recommendation)
    op_md = "\n".join(
        [
            "# v0.14b operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Ikke les denne runden som et bevis på isotropi eller Lorentz-likhet.",
            "- Les den som en diagnostikk av om v14-signalet hovedsakelig er modusavhengighet eller plasseringsover variasjon.",
        ]
    )

    write_csv(args.out_run_csv, run_rows)
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_placement_csv, placement_rows)
    write_csv(args.out_within_csv, within_rows)
    write_csv(args.out_between_csv, between_rows)
    write_csv(args.out_diagnosis_csv, diagnosis_rows)
    write_csv(args.out_recommendation_csv, recommendation)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")

    print(f"Wrote {args.out_summary_md}")
    print(f"Wrote {args.out_diagnosis_csv}")
    print(f"Wrote {args.out_between_csv}")


if __name__ == "__main__":
    main()
