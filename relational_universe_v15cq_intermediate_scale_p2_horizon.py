#!/usr/bin/env python3
"""v0.15cq intermediate-scale p2 horizon decision.

v15cp showed that target-1024 p2 did not reappear under a step budget scaled
from the target-768 budget. The next narrow question is whether the drop happens
only near 1024 or already at the midpoint between 768 and 1024.

This lab tests one intermediate target, 896, with the same carriers, placements,
growth seed, and seed deltas as v15cn/v15cp. It is designed to decide whether p2
should remain a scale-selector candidate or be downgraded to a target-768 local
pocket/contrast observable.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15cn_p2_horizon_scale_holdout as v15cn
import relational_universe_v15cp_target1024_scaled_budget_p2_horizon as v15cp


TARGET = 896
REFERENCE_TARGET = 768
REFERENCE_STEPS = v15ac.FULL_STEPS
SCALED_STEPS = int(math.ceil(REFERENCE_STEPS * TARGET / REFERENCE_TARGET))
GROWTH_SEED = v15cn.GROWTH_SEED
PLACEMENTS = v15cn.PLACEMENTS
PERTURBATIONS = v15cn.PERTURBATIONS
SEED_DELTAS = v15cn.SEED_DELTAS

V15CN_AGGREGATE_CSV = Path("Documentation/v15cn_p2_horizon_scale_holdout_aggregate.csv")
V15CN_COMPARE_CSV = Path("Documentation/v15cn_p2_horizon_scale_holdout_compare.csv")
V15CP_AGGREGATE_CSV = Path("Documentation/v15cp_target1024_scaled_budget_aggregate.csv")
V15CP_COMPARE_CSV = Path("Documentation/v15cp_target1024_scaled_budget_compare.csv")


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def configure_v15cp_helpers() -> None:
    """Reuse v15cp's target-parametric helpers for the 896 midpoint."""
    v15cp.TARGET = TARGET
    v15cp.SCALED_STEPS = SCALED_STEPS


def scale_ladder_rows(
    *,
    aggregate_896: Sequence[Mapping[str, Any]],
    compares_896: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    aggregate_768 = [
        row
        for row in read_csv(V15CN_AGGREGATE_CSV)
        if int(row["target_nodes"]) == 768
    ]
    compare_768 = [
        row
        for row in read_csv(V15CN_COMPARE_CSV)
        if int(row["target_nodes"]) == 768
    ]
    aggregate_1024 = read_csv(V15CP_AGGREGATE_CSV)
    compare_1024 = read_csv(V15CP_COMPARE_CSV)

    out: List[Dict[str, Any]] = []
    groups = [
        (768, "v15cn_same_absolute_2560", aggregate_768, compare_768),
        (TARGET, "v15cq_scaled_from_768", list(aggregate_896), list(compares_896)),
        (1024, "v15cp_scaled_from_768", aggregate_1024, compare_1024),
    ]
    for target, budget_label, aggregate, compares in groups:
        compare_by_pert = {str(row["perturbation"]): row for row in compares}
        by_profile = {str(row["profile_label"]): row for row in aggregate}
        for perturbation in PERTURBATIONS:
            p0 = by_profile[f"{perturbation}_p0"]
            p2 = by_profile[f"{perturbation}_p2"]
            comp = compare_by_pert[perturbation]
            out.append(
                {
                    "target_nodes": int(target),
                    "budget_label": budget_label,
                    "perturbation": perturbation,
                    "p0_established_rate": safe_float(p0["established_far_shell_rate"]),
                    "p2_established_rate": safe_float(p2["established_far_shell_rate"]),
                    "p0_horizon_span": safe_float(p0["mean_high_horizon_span"]),
                    "p2_horizon_span": safe_float(p2["mean_high_horizon_span"]),
                    "p0_no_horizon_rate": safe_float(p0["no_far_shell_rate"]),
                    "p2_no_horizon_rate": safe_float(p2["no_far_shell_rate"]),
                    "p2_minus_p0_established_gap": safe_float(comp["established_rate_gap"]),
                    "p2_minus_p0_horizon_gap": safe_float(comp["high_horizon_gap"]),
                    "p2_support_score": int(float(comp["support_score"])),
                    "p2_candidate_supported": int(float(comp["candidate_supported"])),
                }
            )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    compares: Sequence[Mapping[str, Any]],
    scale_ladder: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    supported_896 = [row for row in compares if int(row["candidate_supported"]) == 1]
    partial_896 = [
        row
        for row in compares
        if int(row["candidate_supported"]) == 0
        and (safe_float(row["p2_established_rate"]) > 0.0 or int(row["support_score"]) >= 2)
    ]
    target768_supported = [
        row
        for row in scale_ladder
        if int(row["target_nodes"]) == 768 and int(row["p2_candidate_supported"]) == 1
    ]
    target1024_supported = [
        row
        for row in scale_ladder
        if int(row["target_nodes"]) == 1024 and int(row["p2_candidate_supported"]) == 1
    ]

    if supported_896:
        status = "intermediate_p2_supported"
        note = "Target 896 supports p2 in at least one carrier, so the scale drop is not immediately above 768."
        next_step = "bracket_896_to_1024_or_replicate_896"
        next_note = "Neste steg bor enten replikere 896 eller bracketter fallet mellom 896 og 1024."
    elif partial_896:
        status = "intermediate_p2_partial_not_supported"
        note = "Target 896 has some p2 movement but does not pass support criteria."
        next_step = "replicate_or_retire_cautiously"
        next_note = "Neste steg bor enten replikere midpoint med litt mer seed-budget eller nedgradere p2 forsiktig."
    elif target768_supported and not target1024_supported:
        status = "intermediate_p2_not_supported_between_768_and_1024"
        note = "Target 768 had p2 support, but target 896 and scaled-budget 1024 do not."
        next_step = "retire_p2_as_scale_selector_keep_local_pocket"
        next_note = "Neste steg bor beholde p2 som target-768 lokal lomme/kontrast, men ikke som skala-selector."
    else:
        status = "p2_scale_selector_not_supported"
        note = "Scale ladder does not support p2 as a scale selector under current observables."
        next_step = "retire_p2_scale_selector"
        next_note = "Neste steg bor flytte innsatsen til andre observabler eller bruke p2 bare som lokal kontroll."

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
            "status": "intermediate_scaled_from_target768",
            "note": f"Target 896 bruker step_budget={SCALED_STEPS}, skalert fra {REFERENCE_STEPS} ved target 768.",
        },
        {
            "diagnostic_family": "intermediate_scale_p2",
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
    scale_ladder: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cq: intermediate-scale p2 horizon")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester ett mellomtarget mellom `768` og `1024` etter at skalert target-1024-budsjett ikke gjenopplivet p2.")
    lines.append("Maalet er aa avgjoere om p2 fortsatt kan brukes som skala-selector, eller boer nedgraderes til target-768 lokal lomme/kontrast.")
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
    lines.append("## Scale ladder")
    lines.append("")
    lines.append("| target | budget | carrier | p2 est | p2 horizon | p2 score | p2 supported |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in scale_ladder:
        lines.append(
            f"| {int(row['target_nodes'])} | {row['budget_label']} | {row['perturbation']} | {fmt(row['p2_established_rate'])} | {fmt(row['p2_horizon_span'])} | {int(row['p2_support_score'])} | {int(row['p2_candidate_supported'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en midpoint-test, ikke et bredt skala-sok.")
    lines.append("- Hvis 896 stoetter p2, er p2 ikke bare target-768-lokal og fallet maa brackettes.")
    lines.append("- Hvis 896 ikke stoetter p2, boer p2 nedgraderes som skala-selector og beholdes bare som lokal lomme/kontrast.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15cq", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke les dette som global invariant-, Lorentz- eller entanglement-evidens. Dette er en midpoint-test av p2 som skala-selector.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    by_family = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15cq",
        "",
        "Denne runden tester et mellompunkt, target 896, mellom den lovende storrelsen 768 og den negative storrelsen 1024.",
        "",
        f"- Hovedresultat: `{by_family['intermediate_scale_p2']['status']}`.",
        f"- Kontrollstatus: `{by_family['artifact_control']['status']}`.",
        f"- Budsjett: `{by_family['budget_scope']['status']}`.",
        "",
        "Hvis 896 ogsaa feiler, er p2 sannsynligvis ikke en god skala-peker akkurat naa.",
        "Da kan p2 fortsatt brukes som lokal kontrast ved 768, men ikke som tegn paa universell struktur.",
        "",
        f"- Neste steg: `{by_family['next_step']['status']}` fordi {by_family['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cq intermediate-scale p2 horizon.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cq_intermediate_scale_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cq_intermediate_scale_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cq_intermediate_scale_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15cq_intermediate_scale_compare.csv")
    p.add_argument("--out-scale-ladder-csv", type=str, default="Documentation/v15cq_intermediate_scale_ladder.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cq_intermediate_scale_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cq_intermediate_scale_p2_horizon_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cq_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cq.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    for path in [V15CN_AGGREGATE_CSV, V15CN_COMPARE_CSV, V15CP_AGGREGATE_CSV, V15CP_COMPARE_CSV]:
        if not path.exists():
            raise FileNotFoundError(f"Missing required scale-ladder input: {path}")

    configure_v15cp_helpers()
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
        v15cp.analyze_run(
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
    aggregate = v15cp.aggregate_rows(run_rows)
    compares = v15cp.compare_rows(aggregate)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    scale_ladder = scale_ladder_rows(aggregate_896=aggregate, compares_896=compares)
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        compares=compares,
        scale_ladder=scale_ladder,
    )

    v15cp.write_csv(args.out_target_csv, target_summary)
    v15cp.write_csv(args.out_runs_csv, run_rows)
    v15cp.write_csv(args.out_aggregate_csv, aggregate)
    v15cp.write_csv(args.out_compare_csv, compares)
    v15cp.write_csv(args.out_scale_ladder_csv, scale_ladder)
    v15cp.write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            target_summary=target_summary,
            aggregate=aggregate,
            compares=compares,
            scale_ladder=scale_ladder,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
