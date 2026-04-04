#!/usr/bin/env python3
"""v0.15r add_chord long-horizon recurrence refinement.

This round narrows the v15q recurrence signal to a handful of representative
`add_chord` traces. It asks whether the late-return signal survives on a longer
horizon, and whether the traces that looked cyclic at v15q stay cyclic or
soften into coarse morphology return.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q


PREFIX_STEPS = 1280
FULL_STEPS = 2560
LOG_EVERY = 8
PROFILES = (
    {
        "profile_id": "t48_g202_p2",
        "target_nodes": 48,
        "growth_seed": 202,
        "placement": 2,
        "expected_prefix_label": "cyclic_return",
        "role": "cyclic_candidate_primary",
    },
    {
        "profile_id": "t96_g202_p3",
        "target_nodes": 96,
        "growth_seed": 202,
        "placement": 3,
        "expected_prefix_label": "cyclic_return",
        "role": "cyclic_candidate_secondary",
    },
    {
        "profile_id": "t48_g101_p3",
        "target_nodes": 48,
        "growth_seed": 101,
        "placement": 3,
        "expected_prefix_label": "morphology_return",
        "role": "morphology_control_primary",
    },
    {
        "profile_id": "t48_g202_p1",
        "target_nodes": 48,
        "growth_seed": 202,
        "placement": 1,
        "expected_prefix_label": "morphology_return",
        "role": "morphology_control_secondary",
    },
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    return v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def subset_trace(log_rows: Sequence[Dict[str, Any]], damaged_sets: Sequence[set[int]], max_step: int) -> Tuple[List[Dict[str, Any]], List[set[int]]]:
    sub_rows: List[Dict[str, Any]] = []
    sub_sets: List[set[int]] = []
    for row, damaged in zip(log_rows, damaged_sets):
        if int(row["step"]) <= max_step:
            sub_rows.append(dict(row))
            sub_sets.append(set(damaged))
    return sub_rows, sub_sets


def transition_label(prefix_label: str, full_label: str) -> str:
    if prefix_label == "cyclic_return" and full_label == "cyclic_return":
        return "sustained_cyclic_return"
    if prefix_label == "cyclic_return" and full_label == "morphology_return":
        return "cyclic_softens_to_morphology_return"
    if prefix_label == "morphology_return" and full_label == "morphology_return":
        return "sustained_morphology_return"
    if full_label == "extinct_after_return":
        return "return_then_extinction"
    if full_label == "drifting_tail":
        return "return_decay"
    return "mixed_transition"


def run_rows(*, ensembles: Sequence[Any], base_states: Mapping[Tuple[str, int], Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    ens_by_target = {int(ens.target_nodes): ens for ens in ensembles}
    for profile in PROFILES:
        target = int(profile["target_nodes"])
        growth_seed = int(profile["growth_seed"])
        placement = int(profile["placement"])
        base = base_states[(ens_by_target[target].name, growth_seed)]
        run_seed = target * 100000 + growth_seed * 1000 + placement
        res = v15q.run_defect_with_sets(
            base,
            params=params,
            seed=run_seed,
            steps=FULL_STEPS,
            perturbation="add_chord",
            center_token_index=placement,
            local_coupling="maximal",
            log_every=LOG_EVERY,
        )
        info = dict(res["perturbation_info"])
        actual = str(info.get("type", "unknown"))
        requested_match = 1 if v15.v14.perturbation_requested_match("add_chord", actual) else 0
        support = list(info.get("support", []))

        prefix_rows, prefix_sets = subset_trace(res["log_rows"], res["damaged_sets"], PREFIX_STEPS)
        full_rows, full_sets = list(res["log_rows"]), list(res["damaged_sets"])
        prefix_metrics = v15q.recurrence_metrics(prefix_rows, prefix_sets)
        full_metrics = v15q.recurrence_metrics(full_rows, full_sets)
        prefix_label = v15q.classify_recurrence_label(int(prefix_rows[-1]["alive"]), prefix_metrics)
        full_label = v15q.classify_recurrence_label(int(full_rows[-1]["alive"]), full_metrics)
        rows.append(
            {
                "profile_id": str(profile["profile_id"]),
                "role": str(profile["role"]),
                "target_nodes": target,
                "growth_seed": growth_seed,
                "placement": placement,
                "run_seed": int(run_seed),
                "requested_match": int(requested_match),
                "support_signature": ",".join(str(x) for x in support),
                "expected_prefix_label": str(profile["expected_prefix_label"]),
                "prefix_label": prefix_label,
                "full_label": full_label,
                "transition_label": transition_label(prefix_label, full_label),
                "prefix_exact_return_rate": safe_float(prefix_metrics["exact_return_rate"]),
                "prefix_coarse_return_rate": safe_float(prefix_metrics["coarse_return_rate"]),
                "prefix_max_exact_return_jaccard": safe_float(prefix_metrics["max_exact_return_jaccard"]),
                "full_exact_return_rate": safe_float(full_metrics["exact_return_rate"]),
                "full_coarse_return_rate": safe_float(full_metrics["coarse_return_rate"]),
                "full_max_exact_return_jaccard": safe_float(full_metrics["max_exact_return_jaccard"]),
                "full_first_exact_return_step": safe_float(full_metrics["first_exact_return_step"]),
                "full_first_coarse_return_step": safe_float(full_metrics["first_coarse_return_step"]),
            }
        )
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        out.append(
            {
                "profile_id": str(row["profile_id"]),
                "role": str(row["role"]),
                "expected_prefix_label": str(row["expected_prefix_label"]),
                "prefix_label": str(row["prefix_label"]),
                "full_label": str(row["full_label"]),
                "transition_label": str(row["transition_label"]),
                "prefix_exact_return_rate": safe_float(row["prefix_exact_return_rate"]),
                "prefix_coarse_return_rate": safe_float(row["prefix_coarse_return_rate"]),
                "full_exact_return_rate": safe_float(row["full_exact_return_rate"]),
                "full_coarse_return_rate": safe_float(row["full_coarse_return_rate"]),
                "full_max_exact_return_jaccard": safe_float(row["full_max_exact_return_jaccard"]),
            }
        )
    return out


def recommendation_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    sustained_cycles = sum(1 for row in rows if str(row["transition_label"]) == "sustained_cyclic_return")
    softened = sum(1 for row in rows if str(row["transition_label"]) == "cyclic_softens_to_morphology_return")
    sustained_morph = sum(1 for row in rows if str(row["transition_label"]) == "sustained_morphology_return")
    out = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er rent separert og de valgte add_chord-profilene matcher ønsket perturbasjonstype."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        }
    ]
    if sustained_cycles >= 1:
        out.append(
            {
                "diagnostic_family": "long_horizon_recurrence",
                "status": "cyclic_return_survives",
                "note": "Minst én add_chord-profil holder ekte cyclic_return også på lengre horisont.",
            }
        )
        out.append(
            {
                "diagnostic_family": "next_step",
                "status": "map_cycle_family",
                "note": "Neste steg bør være en enda smalere kartlegging rundt den overlevende add_chord-cycle-familien.",
            }
        )
    elif softened + sustained_morph >= 2:
        out.append(
            {
                "diagnostic_family": "long_horizon_recurrence",
                "status": "morphology_return_persists",
                "note": "Lang horisont støtter fortsatt retur, men mest som grov morfologisk retur heller enn ren eksakt syklus.",
            }
        )
        out.append(
            {
                "diagnostic_family": "next_step",
                "status": "follow_morphology_return",
                "note": "Neste steg bør være å forklare hva som faktisk holder morfologien stabil i add_chord-familien, ikke å overselge syklisitet.",
            }
        )
    else:
        out.append(
            {
                "diagnostic_family": "long_horizon_recurrence",
                "status": "return_weakens",
                "note": "Lang horisont svekker recurrence-lesningen nok til at dette ikke bør være hovedspor uten ny instrumentering.",
            }
        )
        out.append(
            {
                "diagnostic_family": "next_step",
                "status": "pivot_again",
                "note": "Neste steg bør være et annet smalt defect-spørsmål enn add_chord recurrence langs denne aksen.",
            }
        )
    return out


def build_report(*, target_summary: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], recommendation: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15r: add_chord long-horizon recurrence")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden følger bare noen få representative `add_chord`-traces lenger for å se om senfase-retur overlever på lang horisont."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        if int(row["target_nodes"]) not in {48, 96}:
            continue
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Profile transitions")
    lines.append("")
    lines.append("| profile | role | expected prefix | prefix | full | transition | prefix exact | full exact | full coarse |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_id']} | {row['role']} | {row['expected_prefix_label']} | {row['prefix_label']} | {row['full_label']} | {row['transition_label']} | {fmt(row['prefix_exact_return_rate'])} | {fmt(row['full_exact_return_rate'])} | {fmt(row['full_coarse_return_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en lang-horisont-runde for representative add_chord-profiler, ikke en bred ny scan.")
    lines.append("- Les dette som recurrence i local defects, ikke som partikkelbevis eller generell geometri.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15r add_chord long-horizon recurrence refinement.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15r_add_chord_long_horizon_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15r_add_chord_long_horizon_aggregate.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15r_add_chord_long_horizon_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15r_add_chord_long_horizon_recurrence.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15r_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15r.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([48, 96])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [101, 202])
    target_summary = v10e.summarize_bases(base_rows)
    rows = run_rows(ensembles=ensembles, base_states=base_states)
    aggregate = aggregate_rows(rows)
    recommendation = recommendation_rows(target_summary, rows)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, recommendation=recommendation)
    op_md = "\n".join(
        [
            "# v0.15r operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Les denne runden som lang-horisont add_chord recurrence, ikke som partikkelbevis.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15r",
            "",
            "Denne runden følger noen få lovende `add_chord`-skader lenger i tid for å se om de virkelig vender tilbake til lignende former senere.",
            "",
            "Det er nyttig fordi det kan skille mellom kortvarig likhet og mer robust lokal retur.",
        ]
    ) + "\n"
    write_csv(args.out_runs_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
