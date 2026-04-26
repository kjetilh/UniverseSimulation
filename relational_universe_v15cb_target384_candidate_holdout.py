#!/usr/bin/env python3
"""v0.15cb target-384 candidate holdout.

v15bz found the first stronger target-384 family structure:

- spectral_diffuse_rare quartet:
  add_chord_p0, add_chord_p1, local_swap_p0, local_swap_p3
- rare_diffuse pair:
  add_chord_p2, local_swap_p2
- add_chord_p3 as spectral_core
- local_swap_p1 as mixed
- two full feature-level near-symmetry candidates:
  add_chord_p0 / add_chord_p1
  add_chord_p0 / local_swap_p0

This script is the narrow holdout of that exact map.
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
import relational_universe_v15bv_family_structure_symmetry_lab as v15bv
import relational_universe_v15bz_target384_family_probe as v15bz
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 384
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2, 3)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (1901, 1931, 1963)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY

EXPECTED_FAMILY = {
    "add_chord_p0": "spectral_diffuse_rare_family",
    "add_chord_p1": "spectral_diffuse_rare_family",
    "add_chord_p2": "rare_diffuse_family",
    "add_chord_p3": "spectral_core_family",
    "local_swap_p0": "spectral_diffuse_rare_family",
    "local_swap_p1": "mixed_family",
    "local_swap_p2": "rare_diffuse_family",
    "local_swap_p3": "spectral_diffuse_rare_family",
}
EXPECTED_FULL_NEAR_PAIRS = {
    ("add_chord_p0", "add_chord_p1"),
    ("add_chord_p0", "local_swap_p0"),
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
    perturbation_offset = {"add_chord": 607, "local_swap": 659}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def pair_key(a: str, b: str) -> Tuple[str, str]:
    return tuple(sorted((a, b)))


def with_holdout_columns(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in aggregate:
        cur = dict(row)
        profile = str(cur["profile_label"])
        expected = EXPECTED_FAMILY[profile]
        observed = str(cur["family_label"])
        cur["expected_family_label"] = expected
        cur["family_match_expected"] = int(observed == expected)
        cur["expected_spectral_diffuse_rare_member"] = int(expected == "spectral_diffuse_rare_family")
        cur["expected_rare_diffuse_member"] = int(expected == "rare_diffuse_family")
        cur["quartet_retained"] = int(expected == "spectral_diffuse_rare_family" and observed == "spectral_diffuse_rare_family")
        cur["rare_pair_retained"] = int(expected == "rare_diffuse_family" and observed == "rare_diffuse_family")
        out.append(cur)
    return out


def symmetry_summary_rows(pairwise: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_pair = {pair_key(str(row["profile_a"]), str(row["profile_b"])): row for row in pairwise}
    out: List[Dict[str, Any]] = []
    for a, b in sorted(EXPECTED_FULL_NEAR_PAIRS):
        row = by_pair[pair_key(a, b)]
        out.append(
            {
                "profile_a": a,
                "profile_b": b,
                "retained_full_near": int(str(row["symmetry_label"]) == "support_and_carrier_near_symmetry"),
                "support_distance": safe_float(row["support_distance"]),
                "carrier_distance": safe_float(row["carrier_distance"]),
                "combined_distance": safe_float(row["combined_distance"]),
                "combined_rank": int(row["combined_rank"]),
                "observed_symmetry_label": str(row["symmetry_label"]),
            }
        )
    return out


def holdout_summary_rows(aggregate: Sequence[Mapping[str, Any]], symmetry_summary: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    quartet = [row for row in aggregate if int(row["expected_spectral_diffuse_rare_member"]) == 1]
    rare_pair = [row for row in aggregate if int(row["expected_rare_diffuse_member"]) == 1]
    sym_retained = mean_defined(float(row["retained_full_near"]) for row in symmetry_summary)
    return [
        {
            "summary_family": "all_profiles",
            "n_profiles": len(aggregate),
            "match_rate": mean_defined(float(row["family_match_expected"]) for row in aggregate),
            "quartet_retention_rate": mean_defined(float(row["quartet_retained"]) for row in quartet),
            "rare_pair_retention_rate": mean_defined(float(row["rare_pair_retained"]) for row in rare_pair),
            "full_near_retention_rate": sym_retained,
        },
        {
            "summary_family": "spectral_diffuse_rare_quartet",
            "n_profiles": len(quartet),
            "match_rate": mean_defined(float(row["family_match_expected"]) for row in quartet),
            "quartet_retention_rate": mean_defined(float(row["quartet_retained"]) for row in quartet),
            "rare_pair_retention_rate": float("nan"),
            "full_near_retention_rate": sym_retained,
        },
        {
            "summary_family": "rare_diffuse_pair",
            "n_profiles": len(rare_pair),
            "match_rate": mean_defined(float(row["family_match_expected"]) for row in rare_pair),
            "quartet_retention_rate": float("nan"),
            "rare_pair_retention_rate": mean_defined(float(row["rare_pair_retained"]) for row in rare_pair),
            "full_near_retention_rate": sym_retained,
        },
    ]


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    summary: Sequence[Mapping[str, Any]],
    symmetry_summary: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    all_summary = next(row for row in summary if str(row["summary_family"]) == "all_profiles")
    quartet_summary = next(row for row in summary if str(row["summary_family"]) == "spectral_diffuse_rare_quartet")
    rare_summary = next(row for row in summary if str(row["summary_family"]) == "rare_diffuse_pair")
    match_rate = safe_float(all_summary["match_rate"], 0.0)
    quartet_rate = safe_float(quartet_summary["quartet_retention_rate"], 0.0)
    rare_rate = safe_float(rare_summary["rare_pair_retention_rate"], 0.0)
    full_near_rate = safe_float(all_summary["full_near_retention_rate"], 0.0)
    observed_quartet = [
        str(row["profile_label"])
        for row in aggregate
        if str(row["family_label"]) == "spectral_diffuse_rare_family"
    ]
    retained_pairs = [
        f"{row['profile_a']}::{row['profile_b']}"
        for row in symmetry_summary
        if int(row["retained_full_near"]) == 1
    ]

    if match_rate >= 0.75 and quartet_rate >= 0.75 and rare_rate >= 0.50 and full_near_rate >= 0.50:
        status = "target384_candidates_holdout_supported"
        note = (
            f"Match-rate {fmt(match_rate)}, quartet-retention {fmt(quartet_rate)}, rare-pair-retention {fmt(rare_rate)} "
            f"og near-symmetry-retention {fmt(full_near_rate)}."
        )
        next_step = "probe_target384_mechanism"
        next_note = "Neste steg bor forklare target-384-kandidatene mekanisk, ikke bare holde ut flere labels."
    elif quartet_rate >= 0.75 and full_near_rate >= 0.50:
        status = "target384_quartet_supported_pair_unstable"
        note = f"Quartet holder ({fmt(quartet_rate)}) og near-symmetry delvis ({fmt(full_near_rate)}), men resten av map-en er svakere."
        next_step = "focus_on_quartet_mechanism"
        next_note = "Neste steg bor fokusere mekanisk pa spectral_diffuse_rare-quartetet."
    elif match_rate >= 0.625:
        status = "target384_candidates_weak_holdout"
        note = f"Target-384-kandidatene holder delvis ({fmt(match_rate)}), men ikke rent nok til a laase map-en."
        next_step = "target384_second_holdout_or_mechanism"
        next_note = "Neste steg bor vaere enten en enda smalere target-384 holdout eller en mekanismeobservabel."
    else:
        status = "target384_candidates_not_replicated"
        note = f"Target-384-kandidatene replikerer ikke rent ({fmt(match_rate)})."
        next_step = "new_observable_or_scale_decision"
        next_note = "Neste steg bor bytte observabel eller ta en ny skalaavgjorelse."

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
            "diagnostic_family": "target384_holdout",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "observed_quartet",
            "status": "observed",
            "note": ";".join(observed_quartet),
        },
        {
            "diagnostic_family": "retained_full_near_pairs",
            "status": "observed",
            "note": ";".join(retained_pairs) if retained_pairs else "none",
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
    symmetry_summary: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cb: target-384 candidate holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden holder ut den konkrete target-384-kandidatmappen fra `v15bz`.")
    lines.append("Det inkluderer bade family-labels og de to full feature-level near-symmetry-kandidatene.")
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
    lines.append("| profile | expected | observed | match | coarse | core | shell | rare | spectral rel |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {row['expected_family_label']} | {row['family_label']} | {int(row['family_match_expected'])} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_core_share'])} | {fmt(row['mean_shell_share'])} | {fmt(row['mean_rare_share'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} |"
        )
    lines.append("")
    lines.append("## Holdout summary")
    lines.append("")
    lines.append("| group | n | match rate | quartet retention | rare-pair retention | full near retention |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in summary:
        lines.append(
            f"| {row['summary_family']} | {int(row['n_profiles'])} | {fmt(row['match_rate'])} | {fmt(row['quartet_retention_rate'])} | {fmt(row['rare_pair_retention_rate'])} | {fmt(row['full_near_retention_rate'])} |"
        )
    lines.append("")
    lines.append("## Expected full near-symmetry pairs")
    lines.append("")
    lines.append("| pair | retained | support dist | carrier dist | combined | rank | observed label |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in symmetry_summary:
        lines.append(
            f"| {row['profile_a']} / {row['profile_b']} | {int(row['retained_full_near'])} | {fmt(row['support_distance'])} | {fmt(row['carrier_distance'])} | {fmt(row['combined_distance'])} | {int(row['combined_rank'])} | {row['observed_symmetry_label']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en holdout av konkrete target-384 kandidater, ikke et nytt target-384 search.")
    lines.append("- Positivt signal betyr at både cluster-strukturen og de beste near-symmetry-parene faktisk har noen ben å stå på.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cb target-384 candidate holdout.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cb_target384_candidate_holdout_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cb_target384_candidate_holdout_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cb_target384_candidate_holdout_aggregate.csv")
    p.add_argument("--out-summary-csv", type=str, default="Documentation/v15cb_target384_candidate_holdout_summary.csv")
    p.add_argument("--out-symmetry-csv", type=str, default="Documentation/v15cb_target384_candidate_holdout_symmetry_summary.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cb_target384_candidate_holdout_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cb_target384_candidate_holdout_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cb_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cb.md")
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
        v15bz.aggregate_profile(
            [row for row in run_rows if str(row["perturbation"]) == perturbation and int(row["placement"]) == int(placement)],
            perturbation=perturbation,
            placement=placement,
        )
        for perturbation in PERTURBATIONS
        for placement in PLACEMENTS
    ]
    aggregate = with_holdout_columns(sorted(aggregate, key=lambda row: (str(row["perturbation"]), int(row["placement"]))))
    pairwise = v15bv.pairwise_rows(aggregate)
    symmetry_summary = symmetry_summary_rows(pairwise)
    summary = holdout_summary_rows(aggregate, symmetry_summary)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        aggregate=aggregate,
        summary=summary,
        symmetry_summary=symmetry_summary,
    )
    report_md = build_report(
        target_summary=target_summary,
        aggregate=aggregate,
        summary=summary,
        symmetry_summary=symmetry_summary,
        diagnosis=diagnosis,
    )
    op_md = "\n".join(
        [
            "# v0.15cb operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les dette som holdout av target-384-kandidater, ikke som et bredt nytt target-384-sok.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15cb",
            "",
            "Forrige runde fant noen konkrete kandidater ved storrelse 384: en liten gruppe som lignet hverandre, et p2-par, og et par som sa nesten speilsymmetriske ut i de malte feature-ene.",
            "",
            "Denne runden sjekker om akkurat de kandidatene holder pa nye tilfeldige seeds.",
        ]
    ) + "\n"

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_summary_csv, summary)
    write_csv(args.out_symmetry_csv, symmetry_summary)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
