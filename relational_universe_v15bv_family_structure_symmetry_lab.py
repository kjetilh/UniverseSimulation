#!/usr/bin/env python3
"""v0.15bv family-structure and feature-symmetry lab.

After the same-locus carrier duels stayed mixed through static, timing, and
occupancy observables, this round stops squeezing p3 alone. It asks a narrower
but wider-in-locus question:

do add_chord and local_swap profiles at target 96 / growth seed 202 organize
into repeatable carrier families across nearby placements, and are any of
those families near-symmetric at the feature level?

The symmetry language here is deliberately modest: these are normalized
support/carrier feature near-symmetries, not graph automorphisms.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15ad_add_chord_boundary_shell_lab as v15ad
import relational_universe_v15aw_local_swap_core_shell_lab as v15aw
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 96
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2, 3)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (911, 947, 983, 1019)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
NONTRIVIAL_METRICS = v15bl.NONTRIVIAL_REL_METRICS

SUPPORT_DISTANCE_KEYS = (
    "mean_support_degree",
    "support_ball_1",
    "support_ball_2",
    "support_ball_3",
    "shell2_over_shell1",
)
CARRIER_DISTANCE_KEYS = (
    "mean_full_coarse_return_rate",
    "mean_core_share",
    "mean_shell_share",
    "mean_rare_share",
    "mean_shell_refresh",
    "mean_abs_delta_spectral_radius_rel",
    "mean_abs_delta_dim_proxy_rel",
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def profile_label(perturbation: str, placement: int) -> str:
    return f"{perturbation}_p{int(placement)}"


def run_seed_for(*, perturbation: str, placement: int, seed_delta: int) -> int:
    perturbation_offset = {"add_chord": 0, "local_swap": 37}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def family_label(row: Mapping[str, Any]) -> str:
    coarse = safe_float(row["mean_full_coarse_return_rate"], 0.0)
    core = safe_float(row["mean_core_share"], 0.0)
    shell = safe_float(row["mean_shell_share"], 0.0)
    rare = safe_float(row["mean_rare_share"], 0.0)
    spectral_rank = int(safe_float(row["spectral_rank_nontrivial"], 99))
    dim_minus_spectral = safe_float(row["mean_dim_minus_spectral"], 0.0)
    support_ball_2 = safe_float(row["support_ball_2"], 0.0)
    shell2 = safe_float(row["shell2_over_shell1"], 0.0)

    if coarse >= 0.72 and core >= 0.50 and rare <= 0.15:
        return "geometry_core_family"
    if spectral_rank == 1 and dim_minus_spectral >= 0.02 and core >= 0.45:
        return "spectral_core_family"
    if spectral_rank == 1 and rare >= 0.18:
        return "spectral_diffuse_rare_family"
    if rare >= 0.20 and core < 0.45:
        return "rare_diffuse_family"
    if shell >= 0.35 and support_ball_2 >= 18.0 and shell2 >= 1.20:
        return "expanded_shell_family"
    return "mixed_family"


def aggregate_profile(rows: Sequence[Mapping[str, Any]], *, perturbation: str, placement: int) -> Dict[str, Any]:
    nontrivial_pairs = [
        (metric, mean_defined(safe_float(row[metric]) for row in rows))
        for metric in NONTRIVIAL_METRICS
    ]
    nontrivial_pairs.sort(key=lambda item: item[1])
    rank_map = {metric: idx for idx, (metric, _) in enumerate(nontrivial_pairs, start=1)}
    best_metric, best_mean = nontrivial_pairs[0]
    out: Dict[str, Any] = {
        "profile_label": profile_label(perturbation, placement),
        "perturbation": perturbation,
        "target_nodes": TARGET,
        "growth_seed": GROWTH_SEED,
        "placement": int(placement),
        "n_runs": len(rows),
        "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in rows),
        "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in rows),
        "mean_core_share": mean_defined(safe_float(row["core_share_of_union"]) for row in rows),
        "mean_shell_share": mean_defined(safe_float(row["shell_share_of_union"]) for row in rows),
        "mean_rare_share": mean_defined(safe_float(row["rare_share_of_union"]) for row in rows),
        "mean_mean_core_cover": mean_defined(safe_float(row["mean_core_cover"]) for row in rows),
        "mean_shell_refresh": mean_defined(safe_float(row["mean_shell_refresh"]) for row in rows),
        "mean_burst_rate": mean_defined(safe_float(row["burst_rate"]) for row in rows),
        "mean_shell_cover": mean_defined(safe_float(row["mean_shell_cover"]) for row in rows),
        "mean_boundary_to_volume_sd": mean_defined(safe_float(row["sd_boundary_to_volume"]) for row in rows),
        "mean_abs_delta_spectral_radius_rel": mean_defined(safe_float(row["abs_delta_spectral_radius_rel"]) for row in rows),
        "mean_abs_delta_dim_proxy_rel": mean_defined(safe_float(row["abs_delta_dim_proxy_rel"]) for row in rows),
        "mean_dim_minus_spectral": mean_defined(
            safe_float(row["abs_delta_dim_proxy_rel"]) - safe_float(row["abs_delta_spectral_radius_rel"])
            for row in rows
        ),
        "best_nontrivial_metric": best_metric,
        "best_nontrivial_mean_relative_drift": best_mean,
        "spectral_rank_nontrivial": rank_map["abs_delta_spectral_radius_rel"],
        "dim_rank_nontrivial": rank_map["abs_delta_dim_proxy_rel"],
    }
    for key in SUPPORT_DISTANCE_KEYS:
        out[key] = mean_defined(safe_float(row[key]) for row in rows)
    out["family_label"] = family_label(out)
    return out


def minmax(values: Sequence[float]) -> Tuple[float, float]:
    finite = [x for x in values if math.isfinite(x)]
    if not finite:
        return 0.0, 0.0
    return min(finite), max(finite)


def normalized_distance(a: Mapping[str, Any], b: Mapping[str, Any], keys: Sequence[str], ranges: Mapping[str, Tuple[float, float]]) -> float:
    vals: List[float] = []
    for key in keys:
        av = safe_float(a.get(key))
        bv = safe_float(b.get(key))
        lo, hi = ranges[key]
        if not math.isfinite(av) or not math.isfinite(bv):
            continue
        span = hi - lo
        vals.append(0.0 if span <= 0.0 else abs(av - bv) / span)
    return mean_defined(vals)


def symmetry_label(*, support_distance: float, carrier_distance: float) -> str:
    if support_distance <= 0.20 and carrier_distance <= 0.20:
        return "support_and_carrier_near_symmetry"
    if support_distance <= 0.20:
        return "support_only_near_symmetry"
    if carrier_distance <= 0.20:
        return "carrier_only_near_symmetry"
    return "no_near_symmetry"


def pairwise_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    all_keys = list(SUPPORT_DISTANCE_KEYS) + list(CARRIER_DISTANCE_KEYS)
    ranges = {key: minmax([safe_float(row.get(key)) for row in aggregate]) for key in all_keys}
    out: List[Dict[str, Any]] = []
    for i, a in enumerate(aggregate):
        for b in aggregate[i + 1 :]:
            support_distance = normalized_distance(a, b, SUPPORT_DISTANCE_KEYS, ranges)
            carrier_distance = normalized_distance(a, b, CARRIER_DISTANCE_KEYS, ranges)
            combined_distance = mean_defined([support_distance, carrier_distance])
            out.append(
                {
                    "profile_a": str(a["profile_label"]),
                    "profile_b": str(b["profile_label"]),
                    "perturbation_a": str(a["perturbation"]),
                    "perturbation_b": str(b["perturbation"]),
                    "placement_a": int(a["placement"]),
                    "placement_b": int(b["placement"]),
                    "family_a": str(a["family_label"]),
                    "family_b": str(b["family_label"]),
                    "same_perturbation": int(str(a["perturbation"]) == str(b["perturbation"])),
                    "same_placement": int(int(a["placement"]) == int(b["placement"])),
                    "family_match": int(str(a["family_label"]) == str(b["family_label"])),
                    "support_distance": support_distance,
                    "carrier_distance": carrier_distance,
                    "combined_distance": combined_distance,
                    "symmetry_label": symmetry_label(
                        support_distance=support_distance,
                        carrier_distance=carrier_distance,
                    ),
                }
            )
    out.sort(key=lambda row: safe_float(row["combined_distance"]))
    for idx, row in enumerate(out, start=1):
        row["combined_rank"] = idx
    return out


def family_summary_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    labels = sorted({str(row["family_label"]) for row in aggregate})
    out: List[Dict[str, Any]] = []
    for label in labels:
        group = [row for row in aggregate if str(row["family_label"]) == label]
        out.append(
            {
                "family_label": label,
                "n_profiles": len(group),
                "profiles": ";".join(str(row["profile_label"]) for row in group),
                "perturbations": ";".join(sorted({str(row["perturbation"]) for row in group})),
                "placements": ";".join(str(row["placement"]) for row in group),
                "mean_coarse_return": mean_defined(safe_float(row["mean_full_coarse_return_rate"]) for row in group),
                "mean_core_share": mean_defined(safe_float(row["mean_core_share"]) for row in group),
                "mean_rare_share": mean_defined(safe_float(row["mean_rare_share"]) for row in group),
                "mean_spectral_rel": mean_defined(safe_float(row["mean_abs_delta_spectral_radius_rel"]) for row in group),
            }
        )
    out.sort(key=lambda row: (-int(row["n_profiles"]), str(row["family_label"])))
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    family_summary: Sequence[Mapping[str, Any]],
    pairwise: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    repeated_families = [row for row in family_summary if int(row["n_profiles"]) >= 2 and str(row["family_label"]) != "mixed_family"]
    mixed_count = sum(1 for row in family_summary if str(row["family_label"]) == "mixed_family" for _ in range(int(row["n_profiles"])))
    full_near = [row for row in pairwise if str(row["symmetry_label"]) == "support_and_carrier_near_symmetry"]
    support_near = [row for row in pairwise if str(row["symmetry_label"]) == "support_only_near_symmetry"]
    carrier_near = [row for row in pairwise if str(row["symmetry_label"]) == "carrier_only_near_symmetry"]

    if repeated_families and full_near:
        status = "family_structure_with_near_symmetry_supported"
        note = (
            f"{len(repeated_families)} ikke-trivielle family-labels gjentas, og {len(full_near)} profilpar er near-symmetric "
            "i bade support- og carrier-feature-rommet."
        )
        next_step = "holdout_family_symmetry_candidates"
        next_note = "Neste steg bor validere de beste familie-/near-symmetry-kandidatene pa nye seeds for samme target for a se om strukturen holder."
    elif repeated_families:
        status = "family_structure_without_symmetry_supported"
        note = f"{len(repeated_families)} ikke-trivielle family-labels gjentas, men ingen profilpar er naere pa bade support og carrier."
        next_step = "holdout_repeated_families"
        next_note = "Neste steg bor teste om de repeterte family-labelene holder under flere seeds for samme placements."
    elif full_near or support_near or carrier_near:
        status = "weak_family_structure"
        note = (
            f"Family-labelene gjentas ikke rent, men pairwise-tabellen har {len(full_near)} full, "
            f"{len(support_near)} support-only og {len(carrier_near)} carrier-only near-symmetry-kandidater."
        )
        next_step = "inspect_or_scale_jump"
        next_note = "Hvis de beste parene ikke er substantielt interessante, bor neste steg vaere et nytt skalahopp."
    else:
        status = "family_structure_not_yet"
        note = f"Profilene kollapser ikke til gjentatte ikke-trivielle familier; mixed-antallet er {mixed_count} av {len(run_rows) // len(SEED_DELTAS)} profiler."
        next_step = "new_scale_jump"
        next_note = "Neste steg bor vaere et skalahopp heller enn mer family-squeezing ved target 96."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Enten startstorrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        },
        {
            "diagnostic_family": "family_structure",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "symmetry_scope",
            "status": "feature_level_only",
            "note": "Symmetri her betyr bare lav normalisert avstand i valgte support/carrier-features, ikke automorfier eller fysisk symmetri.",
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    family_summary: Sequence[Mapping[str, Any]],
    pairwise: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bv: family-structure and feature-symmetry lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden leter etter familiestruktur etter at samme-locus-duellene mellom add_chord og local_swap ble blandet.")
    lines.append("Oppsettet er smalt: target 96, growth seed 202, placements 0-3, perturbasjonene add_chord og local_swap, og fire nye holdout-seeds per profil.")
    lines.append("")
    lines.append("Symmetri betyr her bare feature-level near-symmetry: lav normalisert avstand i support-geometri og carrier-observabler. Det er ikke en graph automorphism claim.")
    lines.append("")
    lines.append("## Startstorrelse")
    lines.append("")
    lines.append("| target | mean initial | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Aggregert profilkart")
    lines.append("")
    lines.append("| profile | family | coarse | core | shell | rare | spectral rel | dim rel | support b2 | shell2/shell1 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {row['family_label']} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_core_share'])} | {fmt(row['mean_shell_share'])} | {fmt(row['mean_rare_share'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} | {fmt(row['mean_abs_delta_dim_proxy_rel'])} | {fmt(row['support_ball_2'])} | {fmt(row['shell2_over_shell1'])} |"
        )
    lines.append("")
    lines.append("## Family summary")
    lines.append("")
    lines.append("| family | n | profiles | mean coarse | mean core | mean rare | mean spectral rel |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in family_summary:
        lines.append(
            f"| {row['family_label']} | {int(row['n_profiles'])} | {row['profiles']} | {fmt(row['mean_coarse_return'])} | {fmt(row['mean_core_share'])} | {fmt(row['mean_rare_share'])} | {fmt(row['mean_spectral_rel'])} |"
        )
    lines.append("")
    lines.append("## Beste feature-level near-symmetry-kandidater")
    lines.append("")
    lines.append("| rank | profile A | profile B | family match | support dist | carrier dist | combined | symmetry label |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in pairwise[:8]:
        lines.append(
            f"| {int(row['combined_rank'])} | {row['profile_a']} | {row['profile_b']} | {int(row['family_match'])} | {fmt(row['support_distance'])} | {fmt(row['carrier_distance'])} | {fmt(row['combined_distance'])} | {row['symmetry_label']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en familie-/symmetriobservabel, ikke en ny bred placement scan.")
    lines.append("- Repeterte family-labels er heuristiske grupperinger av målte carrier-features; de skal ikke leses som partikkelarter.")
    lines.append("- Near-symmetry-kandidater er nyttige hvis de gir konkrete holdout-kandidater; ellers er riktig reaksjon skalahopp, ikke mer terskelfiksing.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bv family-structure and feature-symmetry lab.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15bv_family_structure_symmetry_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15bv_family_structure_symmetry_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15bv_family_structure_symmetry_aggregate.csv")
    p.add_argument("--out-family-csv", type=str, default="Documentation/v15bv_family_structure_symmetry_family_summary.csv")
    p.add_argument("--out-pairwise-csv", type=str, default="Documentation/v15bv_family_structure_symmetry_pairwise.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bv_family_structure_symmetry_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bv_family_structure_symmetry_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bv_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bv.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    base_row = next(row for row in base_rows if int(row["target_nodes"]) == TARGET and int(row["growth_seed"]) == GROWTH_SEED)
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    run_rows: List[Dict[str, Any]] = []

    for perturbation in PERTURBATIONS:
        for placement in PLACEMENTS:
            for seed_delta in SEED_DELTAS:
                run_seed = run_seed_for(perturbation=perturbation, placement=placement, seed_delta=seed_delta)
                res = v15q.run_defect_with_sets(
                    base_state,
                    params=params,
                    seed=run_seed,
                    steps=FULL_STEPS,
                    perturbation=perturbation,
                    center_token_index=placement,
                    local_coupling="maximal",
                    log_every=LOG_EVERY,
                )
                recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
                info = dict(res["perturbation_info"])
                support = [int(x) for x in info.get("support", [])]
                if perturbation == "add_chord":
                    core_shell = v15ac.core_shell_metrics(res["damaged_sets"], support)
                else:
                    core_shell = v15aw.core_shell_metrics(res["damaged_sets"], support)
                shell = v15ad.shell_metrics(res["log_rows"], res["damaged_sets"])
                support_features = v14c.support_geometry_features(base_state, support)
                drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                run_rows.append(
                    {
                        "profile_label": profile_label(perturbation, placement),
                        "perturbation": perturbation,
                        "target_nodes": TARGET,
                        "growth_seed": GROWTH_SEED,
                        "placement": int(placement),
                        "seed_delta": int(seed_delta),
                        "run_seed": int(run_seed),
                        "requested_match": int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
                        "support_signature": ",".join(str(x) for x in support),
                        "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                        "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                        "core_share_of_union": safe_float(core_shell["core_share_of_union"]),
                        "shell_share_of_union": safe_float(core_shell["shell_share_of_union"]),
                        "rare_share_of_union": safe_float(core_shell["rare_share_of_union"]),
                        "mean_core_cover": safe_float(core_shell["mean_core_cover"]),
                        "core_shell_label": str(core_shell["label"]),
                        "mean_shell_refresh": safe_float(shell["mean_shell_refresh"]),
                        "burst_rate": safe_float(shell["burst_rate"]),
                        "mean_shell_cover": safe_float(shell["mean_shell_cover"]),
                        "sd_boundary_to_volume": safe_float(shell["sd_boundary_to_volume"]),
                        **support_features,
                        **drift,
                    }
                )

    aggregate = [
        aggregate_profile(
            [row for row in run_rows if str(row["perturbation"]) == perturbation and int(row["placement"]) == int(placement)],
            perturbation=perturbation,
            placement=placement,
        )
        for perturbation in PERTURBATIONS
        for placement in PLACEMENTS
    ]
    aggregate.sort(key=lambda row: (str(row["perturbation"]), int(row["placement"])))
    family_summary = family_summary_rows(aggregate)
    pairwise = pairwise_rows(aggregate)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        family_summary=family_summary,
        pairwise=pairwise,
    )

    report_md = build_report(
        target_summary=target_summary,
        aggregate=aggregate,
        family_summary=family_summary,
        pairwise=pairwise,
        diagnosis=diagnosis,
    )
    op_md = "\n".join(
        [
            "# v0.15bv operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Bruk family-/near-symmetry-kandidater bare som holdout-kandidater. Ikke les dem som partikler eller eksakte symmetrier.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bv",
            "",
            "Denne runden ser etter om de lokale forstyrrelsene faller i noen faa gjenkjennelige familier naar vi flytter startstedet litt rundt.",
            "",
            "Et ekstra pluss ville vaert om to ulike profiler ligner hverandre baade i lokal startgeometri og i hvordan skaden utvikler seg. Det kalles her bare en feature-naer symmetri, ikke en bevist fysisk symmetri.",
        ]
    ) + "\n"

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_family_csv, family_summary)
    write_csv(args.out_pairwise_csv, pairwise)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
