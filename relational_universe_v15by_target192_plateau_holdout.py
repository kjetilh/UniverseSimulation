#!/usr/bin/env python3
"""v0.15by target-192 plateau holdout.

v15bx found a more ordered target-192 family pattern:

- six profiles in spectral_diffuse_rare_family
- both p2 profiles in mixed_family
- no full support+carrier near-symmetry

This holdout uses fresh seeds and the same observable stack. It treats the
v15bx map as a falsifiable expectation, not as an established family law.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15ad_add_chord_boundary_shell_lab as v15ad
import relational_universe_v15aw_local_swap_core_shell_lab as v15aw
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15bv_family_structure_symmetry_lab as v15bv
import relational_universe_v15bx_scale_jump_family_probe as v15bx
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 192
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2, 3)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (1511, 1531, 1559, 1583, 1601, 1627)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY

EXPECTED_FAMILY = {
    "add_chord_p0": "spectral_diffuse_rare_family",
    "add_chord_p1": "spectral_diffuse_rare_family",
    "add_chord_p2": "mixed_family",
    "add_chord_p3": "spectral_diffuse_rare_family",
    "local_swap_p0": "spectral_diffuse_rare_family",
    "local_swap_p1": "spectral_diffuse_rare_family",
    "local_swap_p2": "mixed_family",
    "local_swap_p3": "spectral_diffuse_rare_family",
}


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


def run_seed_for(*, perturbation: str, placement: int, seed_delta: int) -> int:
    perturbation_offset = {"add_chord": 311, "local_swap": 367}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def with_holdout_columns(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in aggregate:
        cur = dict(row)
        profile = str(cur["profile_label"])
        expected = EXPECTED_FAMILY[profile]
        observed = str(cur["family_label"])
        cur["expected_family_label"] = expected
        cur["family_match_expected"] = int(observed == expected)
        cur["expected_plateau_member"] = int(expected == "spectral_diffuse_rare_family")
        cur["plateau_retained"] = int(expected == "spectral_diffuse_rare_family" and observed == "spectral_diffuse_rare_family")
        cur["p2_outlier_expected"] = int(profile.endswith("_p2"))
        cur["p2_outlier_retained"] = int(profile.endswith("_p2") and observed == "mixed_family")
        spectral_margin = 0.18 - safe_float(cur["mean_rare_share"])
        rare_margin = safe_float(cur["mean_rare_share"]) - 0.18
        core_margin = 0.45 - safe_float(cur["mean_core_share"])
        rank_margin = 1.5 - safe_float(cur["spectral_rank_nontrivial"])
        cur["spectral_diffuse_rare_min_margin"] = min(rare_margin, core_margin, rank_margin)
        cur["p2_mixed_rare_margin"] = spectral_margin if profile.endswith("_p2") else float("nan")
        out.append(cur)
    return out


def holdout_summary_rows(aggregate: Sequence[Mapping[str, Any]], pairwise: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    plateau = [row for row in aggregate if int(row["expected_plateau_member"]) == 1]
    p2 = [row for row in aggregate if int(row["p2_outlier_expected"]) == 1]
    full_near = [row for row in pairwise if str(row["symmetry_label"]) == "support_and_carrier_near_symmetry"]
    return [
        {
            "summary_family": "all_profiles",
            "n_profiles": len(aggregate),
            "match_rate": mean_defined(float(row["family_match_expected"]) for row in aggregate),
            "plateau_retention_rate": mean_defined(float(row["plateau_retained"]) for row in plateau),
            "p2_outlier_retention_rate": mean_defined(float(row["p2_outlier_retained"]) for row in p2),
            "mean_plateau_margin": mean_defined(safe_float(row["spectral_diffuse_rare_min_margin"]) for row in plateau),
            "mean_p2_mixed_rare_margin": mean_defined(safe_float(row["p2_mixed_rare_margin"]) for row in p2),
            "full_near_symmetry_count": len(full_near),
        },
        {
            "summary_family": "expected_plateau",
            "n_profiles": len(plateau),
            "match_rate": mean_defined(float(row["family_match_expected"]) for row in plateau),
            "plateau_retention_rate": mean_defined(float(row["plateau_retained"]) for row in plateau),
            "p2_outlier_retention_rate": float("nan"),
            "mean_plateau_margin": mean_defined(safe_float(row["spectral_diffuse_rare_min_margin"]) for row in plateau),
            "mean_p2_mixed_rare_margin": float("nan"),
            "full_near_symmetry_count": len(full_near),
        },
        {
            "summary_family": "expected_p2_outliers",
            "n_profiles": len(p2),
            "match_rate": mean_defined(float(row["family_match_expected"]) for row in p2),
            "plateau_retention_rate": float("nan"),
            "p2_outlier_retention_rate": mean_defined(float(row["p2_outlier_retained"]) for row in p2),
            "mean_plateau_margin": float("nan"),
            "mean_p2_mixed_rare_margin": mean_defined(safe_float(row["p2_mixed_rare_margin"]) for row in p2),
            "full_near_symmetry_count": len(full_near),
        },
    ]


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    summary: Sequence[Mapping[str, Any]],
    pairwise: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    all_summary = next(row for row in summary if str(row["summary_family"]) == "all_profiles")
    plateau_summary = next(row for row in summary if str(row["summary_family"]) == "expected_plateau")
    p2_summary = next(row for row in summary if str(row["summary_family"]) == "expected_p2_outliers")
    match_rate = safe_float(all_summary["match_rate"], 0.0)
    plateau_rate = safe_float(plateau_summary["plateau_retention_rate"], 0.0)
    p2_rate = safe_float(p2_summary["p2_outlier_retention_rate"], 0.0)
    full_near = [row for row in pairwise if str(row["symmetry_label"]) == "support_and_carrier_near_symmetry"]
    observed_plateau = [
        str(row["profile_label"])
        for row in aggregate
        if str(row["family_label"]) == "spectral_diffuse_rare_family"
    ]

    if match_rate >= 0.875 and plateau_rate >= 0.90 and p2_rate >= 0.50:
        status = "target192_plateau_holdout_supported"
        note = (
            f"Holdouten matcher {fmt(match_rate)} av v15bx map; plateau-retention er {fmt(plateau_rate)} "
            f"og p2-outlier-retention er {fmt(p2_rate)}."
        )
        next_step = "probe_plateau_mechanism"
        next_note = "Neste steg bor forklare hvorfor target-192 plateauet er spectral/diffuse/rare og hvorfor p2 skiller seg ut."
    elif plateau_rate >= 0.90:
        status = "target192_plateau_supported_p2_unstable"
        note = f"Plateauet holder ({fmt(plateau_rate)}), men p2-avviket holder svakere ({fmt(p2_rate)})."
        next_step = "holdout_p2_boundary_or_mechanism"
        next_note = "Neste steg bor skille plateau-mekanismen fra p2-boundaryen, ikke hoppe videre ennå."
    elif match_rate >= 0.625:
        status = "target192_plateau_weak_holdout"
        note = f"Target-192 map holder delvis ({fmt(match_rate)}), men ikke rent nok til mekanismeforklaring."
        next_step = "target384_or_new_observable"
        next_note = "Neste steg bor enten hoppe til target 384 eller bytte observabel, ikke presse target 192 terskler."
    else:
        status = "target192_plateau_not_replicated"
        note = f"Target-192 map replikerer ikke rent ({fmt(match_rate)})."
        next_step = "larger_scale_jump"
        next_note = "Neste steg bor vaere target 384 med samme observabler eller en ny observabelklasse."

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
            "diagnostic_family": "target192_plateau_holdout",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "observed_plateau_members",
            "status": "observed",
            "note": ";".join(observed_plateau),
        },
        {
            "diagnostic_family": "symmetry_holdout",
            "status": "no_full_near_symmetry" if not full_near else "full_near_symmetry_candidate",
            "note": (
                "Ingen profilpar er naere i bade support- og carrier-feature-rom."
                if not full_near
                else f"{len(full_near)} profilpar er full feature-level near-symmetry-kandidater."
            ),
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
    summary: Sequence[Mapping[str, Any]],
    pairwise: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15by: target-192 plateau holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om target-192 plateauet fra `v15bx` holder pa friske seeds.")
    lines.append("Forventningen er seks `spectral_diffuse_rare_family`-profiler og to p2-profiler som `mixed_family`.")
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
    lines.append("## Holdout family map")
    lines.append("")
    lines.append("| profile | expected | observed | match | coarse | core | shell | rare | spectral rel | plateau margin |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {row['expected_family_label']} | {row['family_label']} | {int(row['family_match_expected'])} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_core_share'])} | {fmt(row['mean_shell_share'])} | {fmt(row['mean_rare_share'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} | {fmt(row['spectral_diffuse_rare_min_margin'])} |"
        )
    lines.append("")
    lines.append("## Holdout summary")
    lines.append("")
    lines.append("| group | n | match rate | plateau retention | p2 retention | plateau margin | p2 rare margin | full near symmetries |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in summary:
        lines.append(
            f"| {row['summary_family']} | {int(row['n_profiles'])} | {fmt(row['match_rate'])} | {fmt(row['plateau_retention_rate'])} | {fmt(row['p2_outlier_retention_rate'])} | {fmt(row['mean_plateau_margin'])} | {fmt(row['mean_p2_mixed_rare_margin'])} | {int(row['full_near_symmetry_count'])} |"
        )
    lines.append("")
    lines.append("## Beste pairwise feature-avstander")
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
    lines.append("- Dette er en holdout av et scale-jump signal, ikke en ny search.")
    lines.append("- Hvis plateauet holder, er neste sporsmal mekanisme: hvorfor spectral/diffuse/rare, og hvorfor p2-avviket?")
    lines.append("- Ingen symmetry-lesning skal overstige feature-level evidensen.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15by target-192 plateau holdout.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15by_target192_plateau_holdout_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15by_target192_plateau_holdout_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15by_target192_plateau_holdout_aggregate.csv")
    p.add_argument("--out-summary-csv", type=str, default="Documentation/v15by_target192_plateau_holdout_summary.csv")
    p.add_argument("--out-pairwise-csv", type=str, default="Documentation/v15by_target192_plateau_holdout_pairwise.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15by_target192_plateau_holdout_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15by_target192_plateau_holdout_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15by_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15by.md")
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
                core_shell = (
                    v15ac.core_shell_metrics(res["damaged_sets"], support)
                    if perturbation == "add_chord"
                    else v15aw.core_shell_metrics(res["damaged_sets"], support)
                )
                shell = v15ad.shell_metrics(res["log_rows"], res["damaged_sets"])
                support_features = v14c.support_geometry_features(base_state, support)
                drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                run_rows.append(
                    {
                        "profile_label": v15bv.profile_label(perturbation, placement),
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
        v15bx.aggregate_profile(
            [row for row in run_rows if str(row["perturbation"]) == perturbation and int(row["placement"]) == int(placement)],
            perturbation=perturbation,
            placement=placement,
        )
        for perturbation in PERTURBATIONS
        for placement in PLACEMENTS
    ]
    aggregate = with_holdout_columns(sorted(aggregate, key=lambda row: (str(row["perturbation"]), int(row["placement"]))))
    pairwise = v15bv.pairwise_rows(aggregate)
    summary = holdout_summary_rows(aggregate, pairwise)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        aggregate=aggregate,
        summary=summary,
        pairwise=pairwise,
    )
    report_md = build_report(
        target_summary=target_summary,
        aggregate=aggregate,
        summary=summary,
        pairwise=pairwise,
        diagnosis=diagnosis,
    )
    op_md = "\n".join(
        [
            "# v0.15by operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les dette som holdout av target-192 plateauet, ikke som en ny bred scale scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15by",
            "",
            "Forrige runde fant et mer ordnet monster pa storrelse 192: de fleste profilene lignet hverandre, mens p2 skilte seg ut.",
            "",
            "Denne runden sjekker om akkurat det gjentar seg med nye tilfeldige seeds.",
        ]
    ) + "\n"

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_summary_csv, summary)
    write_csv(args.out_pairwise_csv, pairwise)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
