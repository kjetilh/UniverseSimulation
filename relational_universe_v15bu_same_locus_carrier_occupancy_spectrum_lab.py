#!/usr/bin/env python3
"""v0.15bu same-locus carrier occupancy spectrum lab.

After v15bs and v15bt stayed mixed, test a new carrier observable:
how concentrated is the tail occupancy spectrum over damaged nodes?
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 96
GROWTH_SEED = 202
PLACEMENT = 3
SEED_DELTAS = (719, 751, 787, 823, 859, 887)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
PERTURBATIONS = ("add_chord", "local_swap")


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


def occupancy_spectrum_metrics(damaged_sets: Sequence[set[int]]) -> Dict[str, Any]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(damaged_sets))))
    tail_sets = damaged_sets[tail_start:]
    denom = max(1, len(tail_sets))
    counts: Dict[int, int] = {}
    for damaged in tail_sets:
        for node in damaged:
            counts[node] = counts.get(node, 0) + 1
    if not counts:
        return {
            "tail_union_nodes": 0,
            "occupancy_entropy": float("nan"),
            "top1_mass_share": float("nan"),
            "top3_mass_share": float("nan"),
            "top5_mass_share": float("nan"),
            "mean_occ": float("nan"),
            "occ_sd": float("nan"),
        }
    occ = sorted((count / denom for count in counts.values()), reverse=True)
    mass = sum(occ)
    probs = [x / mass for x in occ]
    entropy = -sum(p * math.log(p) for p in probs if p > 0.0) / math.log(len(probs)) if len(probs) > 1 else 0.0
    mean_occ = sum(occ) / len(occ)
    occ_sd = math.sqrt(sum((x - mean_occ) ** 2 for x in occ) / max(1, len(occ) - 1)) if len(occ) > 1 else 0.0
    return {
        "tail_union_nodes": int(len(occ)),
        "occupancy_entropy": entropy,
        "top1_mass_share": sum(probs[:1]),
        "top3_mass_share": sum(probs[:3]),
        "top5_mass_share": sum(probs[:5]),
        "mean_occ": mean_occ,
        "occ_sd": occ_sd,
    }


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        group = [row for row in rows if str(row["perturbation"]) == perturbation]
        out.append(
            {
                "perturbation": perturbation,
                "n_runs": len(group),
                "mean_tail_union_nodes": mean_defined(safe_float(row["tail_union_nodes"]) for row in group),
                "mean_occupancy_entropy": mean_defined(safe_float(row["occupancy_entropy"]) for row in group),
                "mean_top1_mass_share": mean_defined(safe_float(row["top1_mass_share"]) for row in group),
                "mean_top3_mass_share": mean_defined(safe_float(row["top3_mass_share"]) for row in group),
                "mean_top5_mass_share": mean_defined(safe_float(row["top5_mass_share"]) for row in group),
                "mean_occ_sd": mean_defined(safe_float(row["occ_sd"]) for row in group),
                "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in group),
            }
        )
    return out


def comparison_row(aggregate: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    by = {str(row["perturbation"]): dict(row) for row in aggregate}
    add = by["add_chord"]
    swap = by["local_swap"]
    return {
        "compare_label": "carrier_occupancy_spectrum_add_chord_vs_local_swap_at_96_p3",
        "entropy_gap_swap_minus_add": safe_float(swap["mean_occupancy_entropy"]) - safe_float(add["mean_occupancy_entropy"]),
        "top1_gap_add_minus_swap": safe_float(add["mean_top1_mass_share"]) - safe_float(swap["mean_top1_mass_share"]),
        "top3_gap_add_minus_swap": safe_float(add["mean_top3_mass_share"]) - safe_float(swap["mean_top3_mass_share"]),
        "top5_gap_add_minus_swap": safe_float(add["mean_top5_mass_share"]) - safe_float(swap["mean_top5_mass_share"]),
        "union_gap_swap_minus_add": safe_float(swap["mean_tail_union_nodes"]) - safe_float(add["mean_tail_union_nodes"]),
        "occ_sd_gap_add_minus_swap": safe_float(add["mean_occ_sd"]) - safe_float(swap["mean_occ_sd"]),
    }


def diagnosis_rows(target_summary: Sequence[Mapping[str, Any]], run_rows: Sequence[Mapping[str, Any]], aggregate: Sequence[Mapping[str, Any]], compare: Mapping[str, Any]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    entropy_gap = safe_float(compare["entropy_gap_swap_minus_add"])
    top3_gap = safe_float(compare["top3_gap_add_minus_swap"])
    union_gap = safe_float(compare["union_gap_swap_minus_add"])
    if entropy_gap >= 0.05 and top3_gap >= 0.05:
        status = "occupancy_concentration_split_supported"
        note = "add_chord har et tydelig mer konsentrert hale-spekter enn local_swap ved samme locus, mens local_swap sprer mer masse over flere noder."
        next_step = "use_concentration_as_cross_carrier_observable"
        next_note = "Neste steg bor bruke occupancy-konsentrasjon som carrier-observabel i stedet for flere timing- eller coarse-share-varianter."
    elif union_gap >= 5.0:
        status = "occupancy_support_spread_edge_supported"
        note = "local_swap sprer tail-unionen merkbart bredere enn add_chord, men konsentrasjonsprofilen er ikke ren nok ennå."
        next_step = "refine_spectrum_summary"
        next_note = "Neste steg bor raffinere spekter-observabelen heller enn a bytte bort hele carrier-sporet."
    else:
        status = "occupancy_spectrum_still_mixed"
        note = "Heller ikke occupancy-spekteret splitter carrierne rent ved samme locus."
        next_step = "pause_same_locus_duels"
        next_note = "Neste steg bor forlate samme-locus-duellene og heller lete etter en ny familiestruktur eller et nytt skalahopp."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsen er ren og alle occupancy-runs matcher onsket perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "carrier_occupancy_compare",
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
    compare: Mapping[str, Any],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bu: same-locus carrier occupancy spectrum lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om add_chord og local_swap skiller lag tydeligere i hvor konsentrert haleopptreden er over skadede noder.")
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
    lines.append("## Occupancy spectrum summary")
    lines.append("")
    lines.append("| perturbation | tail union | entropy | top1 share | top3 share | top5 share | occ sd | coarse return |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['perturbation']} | {fmt(row['mean_tail_union_nodes'])} | {fmt(row['mean_occupancy_entropy'])} | {fmt(row['mean_top1_mass_share'])} | {fmt(row['mean_top3_mass_share'])} | {fmt(row['mean_top5_mass_share'])} | {fmt(row['mean_occ_sd'])} | {fmt(row['mean_full_coarse_return_rate'])} |"
        )
    lines.append("")
    lines.append("## Spectrum deltas")
    lines.append("")
    lines.append("| entropy gap swap-add | top3 gap add-swap | union gap swap-add | occ sd gap add-swap |")
    lines.append("| --- | --- | --- | --- |")
    lines.append(
        f"| {fmt(compare['entropy_gap_swap_minus_add'])} | {fmt(compare['top3_gap_add_minus_swap'])} | {fmt(compare['union_gap_swap_minus_add'])} | {fmt(compare['occ_sd_gap_add_minus_swap'])} |"
    )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ny observabelklasse pa samme locus, ikke mer av de gamle timing- eller core/shell-snittene.")
    lines.append("- Positivt signal her betyr at carrierne skiller lag i konsentrasjonsgeometri, ikke nodvendigvis i alle andre beskrivelser samtidig.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bu same-locus carrier occupancy spectrum lab.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15bu_same_locus_carrier_occupancy_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15bu_same_locus_carrier_occupancy_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15bu_same_locus_carrier_occupancy_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15bu_same_locus_carrier_occupancy_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bu_same_locus_carrier_occupancy_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bu_same_locus_carrier_occupancy_spectrum_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bu_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bu.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    run_rows: List[Dict[str, Any]] = []

    for perturbation in PERTURBATIONS:
        for seed_delta in SEED_DELTAS:
            run_seed = TARGET * 100000 + GROWTH_SEED * 1000 + PLACEMENT * 100 + int(seed_delta)
            if perturbation == "local_swap":
                run_seed += 7
            res = v15ae.run_defect_with_control_graphs(
                base_state,
                params=params,
                seed=run_seed,
                steps=FULL_STEPS,
                perturbation=perturbation,
                center_token_index=PLACEMENT,
                local_coupling="maximal",
                log_every=LOG_EVERY,
            )
            metrics = occupancy_spectrum_metrics(res["damaged_sets"])
            info = dict(res["perturbation_info"])
            recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
            run_rows.append(
                {
                    "perturbation": perturbation,
                    "target_nodes": TARGET,
                    "growth_seed": GROWTH_SEED,
                    "placement": PLACEMENT,
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
                    "support_signature": ",".join(str(x) for x in info.get("support", [])),
                    "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                    **metrics,
                }
            )

    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    aggregate = aggregate_rows(run_rows)
    compare = comparison_row(aggregate)
    diagnosis = diagnosis_rows(target_summary, run_rows, aggregate, compare)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, compare=compare, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bu operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en occupancy-observabel pa samme locus, ikke som en ny bred carrier-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bu",
            "",
            "Denne runden ser pa om skaden er samlet rundt noen fa noder eller spres utover mange noder i senfasen.",
            "",
            "Tanken er at to forstyrrelser kan se like ut i grove snitt, men likevel ha ulik indre konsentrasjon.",
        ]
    ) + "\n"
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_compare_csv, [compare])
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
