#!/usr/bin/env python3
"""v0.15cp target-1024 scaled-budget p2 horizon.

v15cn showed that the target-768 p2 far-shell pocket did not automatically
survive to target 1024 under the same absolute step budget. v15co then made the
selection policy explicit: before using p2 as a universe-like selector, test
whether the 1024 negative was simply a budget normalization issue.

This lab keeps the design narrow:

- same operational regime as v15cn (`band_zero_del` through v10e recommendation)
- same growth seed 202
- same target 1024 only
- same p0/p2 placements
- same add_chord/local_swap carriers
- same seed deltas
- one changed variable: step budget scaled from the target-768 budget
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15cn_p2_horizon_scale_holdout as v15cn
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 1024
REFERENCE_TARGET = 768
REFERENCE_STEPS = v15ac.FULL_STEPS
SCALED_STEPS = int(math.ceil(REFERENCE_STEPS * TARGET / REFERENCE_TARGET))
GROWTH_SEED = v15cn.GROWTH_SEED
PLACEMENTS = v15cn.PLACEMENTS
PERTURBATIONS = v15cn.PERTURBATIONS
SEED_DELTAS = v15cn.SEED_DELTAS
LOG_EVERY = v15ac.LOG_EVERY

PREVIOUS_AGGREGATE_CSV = Path("Documentation/v15cn_p2_horizon_scale_holdout_aggregate.csv")


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with Path(path).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def analyze_run(
    *,
    base_state: Any,
    base_row: Mapping[str, Any],
    perturbation: str,
    placement: int,
    seed_delta: int,
) -> Dict[str, Any]:
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    run_seed = v15cn.run_seed_for(
        target=TARGET,
        perturbation=perturbation,
        placement=placement,
        seed_delta=seed_delta,
    )
    res = v15q.run_defect_with_sets(
        base_state,
        params=params,
        seed=run_seed,
        steps=SCALED_STEPS,
        perturbation=perturbation,
        center_token_index=placement,
        local_coupling="maximal",
        log_every=LOG_EVERY,
    )
    recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
    info = dict(res["perturbation_info"])
    support = [int(x) for x in info.get("support", [])]
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(res["log_rows"]))))
    tail_series = v15cn.raw_far_shell_tail_series(base_state, support, res["damaged_sets"][tail_start:])
    horizon = v15cn.horizon_fields(tail_series)
    drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
    return {
        "budget_label": "scaled_from_768",
        "profile_label": f"{perturbation}_p{int(placement)}",
        "perturbation": perturbation,
        "target_nodes": TARGET,
        "reference_target_nodes": REFERENCE_TARGET,
        "growth_seed": GROWTH_SEED,
        "placement": int(placement),
        "seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "reference_step_budget": int(REFERENCE_STEPS),
        "step_budget": int(SCALED_STEPS),
        "budget_scale_factor": float(TARGET / REFERENCE_TARGET),
        "log_every": int(LOG_EVERY),
        "requested_match": int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
        "support_signature": ",".join(str(x) for x in support),
        "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
        "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
        "mean_far_shell_share": mean_defined(safe_float(row["far_shell_share"]) for row in tail_series),
        "q90_far_shell_share": v15.quantile([safe_float(row["far_shell_share"]) for row in tail_series], 0.90)
        if tail_series
        else float("nan"),
        "mean_weighted_mean_distance": mean_defined(safe_float(row["weighted_mean_distance"]) for row in tail_series),
        "max_weighted_mean_distance": max((safe_float(row["weighted_mean_distance"]) for row in tail_series), default=float("nan")),
        **horizon,
        **drift,
    }


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        for placement in PLACEMENTS:
            group = [
                row
                for row in rows
                if str(row["perturbation"]) == perturbation and int(row["placement"]) == int(placement)
            ]
            out.append(
                {
                    "budget_label": "scaled_from_768",
                    "target_nodes": TARGET,
                    "reference_target_nodes": REFERENCE_TARGET,
                    "profile_label": f"{perturbation}_p{int(placement)}",
                    "perturbation": perturbation,
                    "placement": int(placement),
                    "n_runs": len(group),
                    "step_budget": int(SCALED_STEPS),
                    "budget_scale_factor": float(TARGET / REFERENCE_TARGET),
                    "established_far_shell_rate": mean_defined(
                        1.0 if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon" else 0.0
                        for row in group
                    ),
                    "late_probe_rate": mean_defined(
                        1.0 if str(row["far_shell_horizon_label"]) == "late_far_shell_probe" else 0.0 for row in group
                    ),
                    "failed_far_shell_rate": mean_defined(
                        1.0 if str(row["far_shell_horizon_label"]) == "failed_far_shell_horizon" else 0.0
                        for row in group
                    ),
                    "no_far_shell_rate": mean_defined(
                        1.0 if str(row["far_shell_horizon_label"]) == "no_far_shell_horizon" else 0.0 for row in group
                    ),
                    "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in group),
                    "mean_high_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group),
                    "mean_high_retention_rate": mean_defined(safe_float(row["high_retention_rate"]) for row in group),
                    "mean_last12_high_rate": mean_defined(safe_float(row["last12_high_rate"]) for row in group),
                    "mean_total_high_count": mean_defined(safe_float(row["total_high_count"]) for row in group),
                    "mean_longest_high_run": mean_defined(safe_float(row["longest_high_run"]) for row in group),
                    "mean_far_shell_share": mean_defined(safe_float(row["mean_far_shell_share"]) for row in group),
                    "mean_q90_far_shell_share": mean_defined(safe_float(row["q90_far_shell_share"]) for row in group),
                    "mean_weighted_mean_distance": mean_defined(safe_float(row["mean_weighted_mean_distance"]) for row in group),
                    "mean_abs_delta_spectral_radius_rel": mean_defined(
                        safe_float(row["abs_delta_spectral_radius_rel"]) for row in group
                    ),
                }
            )
    return out


def compare_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_key = {(str(row["perturbation"]), int(row["placement"])): row for row in aggregate}
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        p0 = by_key[(perturbation, 0)]
        p2 = by_key[(perturbation, 2)]
        row: Dict[str, Any] = {
            "budget_label": "scaled_from_768",
            "target_nodes": TARGET,
            "reference_target_nodes": REFERENCE_TARGET,
            "compare_label": f"{perturbation}_p2_minus_p0",
            "perturbation": perturbation,
            "step_budget": int(SCALED_STEPS),
            "established_rate_gap": safe_float(p2["established_far_shell_rate"]) - safe_float(p0["established_far_shell_rate"]),
            "no_horizon_control_gap": safe_float(p0["no_far_shell_rate"]) - safe_float(p2["no_far_shell_rate"]),
            "high_retention_gap": safe_float(p2["mean_high_retention_rate"]) - safe_float(p0["mean_high_retention_rate"]),
            "last12_high_gap": safe_float(p2["mean_last12_high_rate"]) - safe_float(p0["mean_last12_high_rate"]),
            "high_horizon_gap": safe_float(p2["mean_high_horizon_span"]) - safe_float(p0["mean_high_horizon_span"]),
            "total_high_gap": safe_float(p2["mean_total_high_count"]) - safe_float(p0["mean_total_high_count"]),
            "far_share_gap": safe_float(p2["mean_far_shell_share"]) - safe_float(p0["mean_far_shell_share"]),
            "q90_far_share_gap": safe_float(p2["mean_q90_far_shell_share"]) - safe_float(p0["mean_q90_far_shell_share"]),
            "distance_gap": safe_float(p2["mean_weighted_mean_distance"]) - safe_float(p0["mean_weighted_mean_distance"]),
            "spectral_gap": safe_float(p2["mean_abs_delta_spectral_radius_rel"]) - safe_float(p0["mean_abs_delta_spectral_radius_rel"]),
            "p2_established_rate": safe_float(p2["established_far_shell_rate"]),
            "p0_no_horizon_rate": safe_float(p0["no_far_shell_rate"]),
        }
        row["support_score"] = int(v15cn.p2_support_score(row))
        row["candidate_supported"] = int(
            int(row["support_score"]) >= 4
            and safe_float(row["p2_established_rate"]) >= 0.50
            and safe_float(row["p0_no_horizon_rate"]) >= 0.50
        )
        out.append(row)
    return out


def budget_compare_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    previous = [
        row
        for row in read_csv(PREVIOUS_AGGREGATE_CSV)
        if int(row["target_nodes"]) == TARGET and str(row["profile_label"]) in {str(x["profile_label"]) for x in aggregate}
    ]
    previous_by_profile = {str(row["profile_label"]): row for row in previous}
    out: List[Dict[str, Any]] = []
    for current in aggregate:
        old = previous_by_profile[str(current["profile_label"])]
        out.append(
            {
                "target_nodes": TARGET,
                "profile_label": current["profile_label"],
                "perturbation": current["perturbation"],
                "placement": int(current["placement"]),
                "absolute_step_budget": int(REFERENCE_STEPS),
                "scaled_step_budget": int(SCALED_STEPS),
                "established_rate_absolute": safe_float(old["established_far_shell_rate"]),
                "established_rate_scaled": safe_float(current["established_far_shell_rate"]),
                "established_rate_delta": safe_float(current["established_far_shell_rate"]) - safe_float(old["established_far_shell_rate"]),
                "horizon_span_absolute": safe_float(old["mean_high_horizon_span"]),
                "horizon_span_scaled": safe_float(current["mean_high_horizon_span"]),
                "horizon_span_delta": safe_float(current["mean_high_horizon_span"]) - safe_float(old["mean_high_horizon_span"]),
                "last12_high_absolute": safe_float(old["mean_last12_high_rate"]),
                "last12_high_scaled": safe_float(current["mean_last12_high_rate"]),
                "last12_high_delta": safe_float(current["mean_last12_high_rate"]) - safe_float(old["mean_last12_high_rate"]),
                "distance_absolute": safe_float(old["mean_weighted_mean_distance"]),
                "distance_scaled": safe_float(current["mean_weighted_mean_distance"]),
                "distance_delta": safe_float(current["mean_weighted_mean_distance"]) - safe_float(old["mean_weighted_mean_distance"]),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    compares: Sequence[Mapping[str, Any]],
    budget_compare: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    supported = [row for row in compares if int(row["candidate_supported"]) == 1]
    shared = len(supported) == len(PERTURBATIONS)
    any_supported = bool(supported)
    revived_profiles = [
        row
        for row in budget_compare
        if int(row["placement"]) == 2 and safe_float(row["established_rate_scaled"]) > safe_float(row["established_rate_absolute"])
    ]
    p0_horizon_delta = sum(
        safe_float(row["horizon_span_delta"])
        for row in budget_compare
        if int(row["placement"]) == 0
    )
    p2_horizon_delta = sum(
        safe_float(row["horizon_span_delta"])
        for row in budget_compare
        if int(row["placement"]) == 2
    )

    if shared:
        status = "scaled_budget_p2_shared_supported"
        note = "Target 1024 supports p2 in both carriers after budget scaling."
        next_step = "replicate_scaled_budget_and_intermediate_scale"
        next_note = "Neste steg bor replikere skalert 1024 og ett mellomtarget foer sterkere skala-sprak."
    elif any_supported:
        carriers = ";".join(str(row["perturbation"]) for row in supported)
        status = "scaled_budget_p2_carrier_specific"
        note = f"Target 1024 supports p2 after budget scaling in carrier(s): {carriers}."
        next_step = "carrier_specific_scale_validation"
        next_note = "Neste steg bor teste om dette er carrier-scope eller robust p2-scale."
    elif revived_profiles:
        profiles = ";".join(str(row["profile_label"]) for row in revived_profiles)
        status = "scaled_budget_p2_partial_revived_but_not_supported"
        note = f"Scaled budget improves p2 established rate for {profiles}, but not enough to pass support criteria."
        next_step = "intermediate_scale_before_more_1024_budget"
        next_note = "Neste steg bor teste mellomtarget foer mer 1024-budsjett; p2 er ikke rent gjenopplivet."
    else:
        status = "scaled_budget_p2_not_supported"
        note = "Budget scaling from target 768 to 1024 did not revive p2 under the existing support criteria."
        next_step = "intermediate_scale_or_retire_p2_as_scale_selector"
        next_note = "Neste steg bor enten teste ett mellomtarget eller nedgradere p2 som skala-selector."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelse er ren og alle requested perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Enten startstorrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        },
        {
            "diagnostic_family": "budget_scope",
            "status": "scaled_from_target768",
            "note": f"Target 1024 bruker step_budget={SCALED_STEPS}, skalert fra {REFERENCE_STEPS} ved target 768.",
        },
        {
            "diagnostic_family": "budget_effect",
            "status": (
                "p2_budget_response"
                if p2_horizon_delta > 0.0
                else "p0_budget_response_without_p2"
                if p0_horizon_delta > 0.0
                else "no_far_shell_budget_response"
            ),
            "note": (
                f"Samlet horizon-span delta er p0={fmt(p0_horizon_delta)} og p2={fmt(p2_horizon_delta)} mot v15cn same-absolute-budget."
            ),
        },
        {
            "diagnostic_family": "target1024_scaled_budget_p2",
            "status": status,
            "note": note,
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
    compares: Sequence[Mapping[str, Any]],
    budget_compare: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cp: target-1024 scaled-budget p2 horizon")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester den minste budsjettforklaringen etter `v15cn` og `v15co`.")
    lines.append("Den holder target `1024`, p0/p2, carriers, growth seed og seed-deltaer fast, men skalerer step budget fra target `768`.")
    lines.append("")
    lines.append("## Budget")
    lines.append("")
    lines.append("| reference target | target | reference steps | scaled steps | scale factor |")
    lines.append("| --- | --- | --- | --- | --- |")
    lines.append(f"| {REFERENCE_TARGET} | {TARGET} | {REFERENCE_STEPS} | {SCALED_STEPS} | {fmt(TARGET / REFERENCE_TARGET)} |")
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
    lines.append("## Profile summary")
    lines.append("")
    lines.append("| profile | established | none | horizon | retention | last12 high | total high | far share | distance | spectral rel |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {fmt(row['established_far_shell_rate'])} | {fmt(row['no_far_shell_rate'])} | {fmt(row['mean_high_horizon_span'])} | {fmt(row['mean_high_retention_rate'])} | {fmt(row['mean_last12_high_rate'])} | {fmt(row['mean_total_high_count'])} | {fmt(row['mean_far_shell_share'])} | {fmt(row['mean_weighted_mean_distance'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} |"
        )
    lines.append("")
    lines.append("## P2 versus P0")
    lines.append("")
    lines.append("| compare | est gap | control none gap | retention gap | last12 gap | horizon gap | distance gap | support score | supported |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['established_rate_gap'])} | {fmt(row['no_horizon_control_gap'])} | {fmt(row['high_retention_gap'])} | {fmt(row['last12_high_gap'])} | {fmt(row['high_horizon_gap'])} | {fmt(row['distance_gap'])} | {int(row['support_score'])} | {int(row['candidate_supported'])} |"
        )
    lines.append("")
    lines.append("## Budget comparison versus v15cn")
    lines.append("")
    lines.append("| profile | absolute established | scaled established | delta | absolute horizon | scaled horizon | horizon delta |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in budget_compare:
        lines.append(
            f"| {row['profile_label']} | {fmt(row['established_rate_absolute'])} | {fmt(row['established_rate_scaled'])} | {fmt(row['established_rate_delta'])} | {fmt(row['horizon_span_absolute'])} | {fmt(row['horizon_span_scaled'])} | {fmt(row['horizon_span_delta'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en smal budsjett-normaliseringstest, ikke et nytt bredt target-search.")
    lines.append("- Positivt signal betyr bare at target-1024-p2 var budsjettfoelsomt under v15cn, ikke at p2 er universell.")
    lines.append("- Negativt signal betyr at p2 som scale-selector svekkes, men ett mellomtarget kan fortsatt skille gradvis overgang fra skarp target-lomme.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15cp", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke les dette som global invariant-, Lorentz- eller entanglement-evidens. Dette er en skalert budsjett-test av en p2 far-shell-observabel.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    by_family = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15cp",
        "",
        "Denne runden sjekker om target-1024 feilet i forrige p2-test bare fordi den fikk for lite tid.",
        "",
        f"- Hovedresultat: `{by_family['target1024_scaled_budget_p2']['status']}`.",
        f"- Kontrollstatus: `{by_family['artifact_control']['status']}`.",
        f"- Budsjett: `{by_family['budget_scope']['status']}`.",
        "",
        "Hvis p2 kommer tilbake med mer tid, er 1024-negativen fra forrige runde mindre alvorlig.",
        "Hvis p2 fortsatt ikke kommer tilbake, blir det mer sannsynlig at p2-lommen er lokal for 768 eller trenger en annen skalaovergang.",
        "",
        f"- Neste steg: `{by_family['next_step']['status']}` fordi {by_family['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cp target-1024 scaled-budget p2 horizon.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cp_target1024_scaled_budget_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cp_target1024_scaled_budget_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cp_target1024_scaled_budget_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15cp_target1024_scaled_budget_compare.csv")
    p.add_argument("--out-budget-compare-csv", type=str, default="Documentation/v15cp_target1024_scaled_budget_budget_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cp_target1024_scaled_budget_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cp_target1024_scaled_budget_p2_horizon_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cp_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cp.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if not PREVIOUS_AGGREGATE_CSV.exists():
        raise FileNotFoundError(f"Missing v15cn aggregate for budget comparison: {PREVIOUS_AGGREGATE_CSV}")

    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    base_row = next(
        row
        for row in base_rows
        if int(row["growth_seed"]) == GROWTH_SEED and int(row["target_nodes"]) == TARGET
    )

    run_rows = [
        analyze_run(
            base_state=base_state,
            base_row=base_row,
            perturbation=perturbation,
            placement=placement,
            seed_delta=seed_delta,
        )
        for perturbation in PERTURBATIONS
        for placement in PLACEMENTS
        for seed_delta in SEED_DELTAS
    ]
    aggregate = aggregate_rows(run_rows)
    compares = compare_rows(aggregate)
    budget_compare = budget_compare_rows(aggregate)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        compares=compares,
        budget_compare=budget_compare,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_compare_csv, compares)
    write_csv(args.out_budget_compare_csv, budget_compare)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            target_summary=target_summary,
            aggregate=aggregate,
            compares=compares,
            budget_compare=budget_compare,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
