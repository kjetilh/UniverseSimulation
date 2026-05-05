#!/usr/bin/env python3
"""v0.15cj target-768 outer occupancy concentration lab.

v15ci showed that outer-shell genealogy alone does not explain the shared p2
horizon at target 768. The next narrow question is more local:

is p2 distinguished by a more concentrated outer occupancy spectrum even if the
outer horizon remains reseeded rather than carried by one clean branch?
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 768
GROWTH_SEED = 202
PLACEMENTS = (0, 2)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (4301, 4349, 4391, 4447)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
OUTER_DISTANCE_FLOOR = 4


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
    perturbation_offset = {"add_chord": 1511, "local_swap": 1579}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def outer_occupancy_metrics(base_graph: v7.UGraph, support: Sequence[int], damaged_sets: Sequence[Set[int]]) -> Dict[str, Any]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(damaged_sets))))
    tail_sets = damaged_sets[tail_start:]
    denom = max(1, len(tail_sets))
    base_dist = v7.bfs_distances(base_graph, support)
    fallback = (max(base_dist.values()) + 1) if base_dist else 1

    counts: Dict[int, int] = {}
    dist_mass_sum = 0.0
    total_outer_mass = 0
    outer_active_steps = 0
    for damaged in tail_sets:
        outer_nodes = {
            node
            for node in damaged
            if int(base_dist.get(node, fallback)) >= OUTER_DISTANCE_FLOOR
        }
        if outer_nodes:
            outer_active_steps += 1
        for node in outer_nodes:
            counts[node] = counts.get(node, 0) + 1
            total_outer_mass += 1
            dist_mass_sum += float(base_dist.get(node, fallback))

    if not counts:
        return {
            "outer_tail_union_nodes": 0,
            "outer_active_rate": 0.0,
            "outer_occupancy_entropy": float("nan"),
            "outer_top1_mass_share": float("nan"),
            "outer_top3_mass_share": float("nan"),
            "outer_top5_mass_share": float("nan"),
            "outer_occ_sd": float("nan"),
            "outer_core_mass_share": float("nan"),
            "outer_rare_mass_share": float("nan"),
            "outer_weighted_mean_distance": float("nan"),
        }

    occ = sorted((count / denom for count in counts.values()), reverse=True)
    mass = sum(occ)
    probs = [value / mass for value in occ]
    entropy = -sum(p * math.log(p) for p in probs if p > 0.0) / math.log(len(probs)) if len(probs) > 1 else 0.0
    mean_occ = sum(occ) / len(occ)
    occ_sd = math.sqrt(sum((value - mean_occ) ** 2 for value in occ) / max(1, len(occ) - 1)) if len(occ) > 1 else 0.0
    core_mass = sum(value for value in occ if value >= 0.80)
    rare_mass = sum(value for value in occ if 0.0 < value < 0.20)
    return {
        "outer_tail_union_nodes": int(len(occ)),
        "outer_active_rate": outer_active_steps / denom,
        "outer_occupancy_entropy": entropy,
        "outer_top1_mass_share": sum(probs[:1]),
        "outer_top3_mass_share": sum(probs[:3]),
        "outer_top5_mass_share": sum(probs[:5]),
        "outer_occ_sd": occ_sd,
        "outer_core_mass_share": core_mass / mass,
        "outer_rare_mass_share": rare_mass / mass,
        "outer_weighted_mean_distance": dist_mass_sum / max(1, total_outer_mass),
    }


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        for placement in PLACEMENTS:
            group = [
                row for row in rows
                if str(row["perturbation"]) == perturbation and int(row["placement"]) == int(placement)
            ]
            out.append(
                {
                    "profile_label": f"{perturbation}_p{int(placement)}",
                    "perturbation": perturbation,
                    "placement": int(placement),
                    "n_runs": len(group),
                    "mean_outer_tail_union_nodes": mean_defined(safe_float(row["outer_tail_union_nodes"]) for row in group),
                    "mean_outer_active_rate": mean_defined(safe_float(row["outer_active_rate"]) for row in group),
                    "mean_outer_occupancy_entropy": mean_defined(safe_float(row["outer_occupancy_entropy"]) for row in group),
                    "mean_outer_top1_mass_share": mean_defined(safe_float(row["outer_top1_mass_share"]) for row in group),
                    "mean_outer_top3_mass_share": mean_defined(safe_float(row["outer_top3_mass_share"]) for row in group),
                    "mean_outer_top5_mass_share": mean_defined(safe_float(row["outer_top5_mass_share"]) for row in group),
                    "mean_outer_occ_sd": mean_defined(safe_float(row["outer_occ_sd"]) for row in group),
                    "mean_outer_core_mass_share": mean_defined(safe_float(row["outer_core_mass_share"]) for row in group),
                    "mean_outer_rare_mass_share": mean_defined(safe_float(row["outer_rare_mass_share"]) for row in group),
                    "mean_outer_weighted_mean_distance": mean_defined(safe_float(row["outer_weighted_mean_distance"]) for row in group),
                    "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in group),
                    "mean_abs_delta_spectral_radius_rel": mean_defined(safe_float(row["abs_delta_spectral_radius_rel"]) for row in group),
                }
            )
    return out


def compare_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by = {str(row["profile_label"]): dict(row) for row in aggregate}
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        p0 = by[f"{perturbation}_p0"]
        p2 = by[f"{perturbation}_p2"]
        out.append(
            {
                "compare_label": f"{perturbation}_p2_minus_p0",
                "outer_entropy_gap_p2_minus_p0": safe_float(p2["mean_outer_occupancy_entropy"]) - safe_float(p0["mean_outer_occupancy_entropy"]),
                "outer_top3_gap_p2_minus_p0": safe_float(p2["mean_outer_top3_mass_share"]) - safe_float(p0["mean_outer_top3_mass_share"]),
                "outer_top5_gap_p2_minus_p0": safe_float(p2["mean_outer_top5_mass_share"]) - safe_float(p0["mean_outer_top5_mass_share"]),
                "outer_core_mass_gap_p2_minus_p0": safe_float(p2["mean_outer_core_mass_share"]) - safe_float(p0["mean_outer_core_mass_share"]),
                "outer_rare_mass_gap_p2_minus_p0": safe_float(p2["mean_outer_rare_mass_share"]) - safe_float(p0["mean_outer_rare_mass_share"]),
                "outer_union_gap_p2_minus_p0": safe_float(p2["mean_outer_tail_union_nodes"]) - safe_float(p0["mean_outer_tail_union_nodes"]),
                "outer_occ_sd_gap_p2_minus_p0": safe_float(p2["mean_outer_occ_sd"]) - safe_float(p0["mean_outer_occ_sd"]),
                "outer_distance_gap_p2_minus_p0": safe_float(p2["mean_outer_weighted_mean_distance"]) - safe_float(p0["mean_outer_weighted_mean_distance"]),
            }
        )
    add2 = by["add_chord_p2"]
    swap2 = by["local_swap_p2"]
    out.append(
        {
            "compare_label": "local_swap_p2_minus_add_chord_p2",
            "outer_entropy_gap_swap_minus_add": safe_float(swap2["mean_outer_occupancy_entropy"]) - safe_float(add2["mean_outer_occupancy_entropy"]),
            "outer_top3_gap_add_minus_swap": safe_float(add2["mean_outer_top3_mass_share"]) - safe_float(swap2["mean_outer_top3_mass_share"]),
            "outer_top5_gap_add_minus_swap": safe_float(add2["mean_outer_top5_mass_share"]) - safe_float(swap2["mean_outer_top5_mass_share"]),
            "outer_core_mass_gap_add_minus_swap": safe_float(add2["mean_outer_core_mass_share"]) - safe_float(swap2["mean_outer_core_mass_share"]),
            "outer_rare_mass_gap_swap_minus_add": safe_float(swap2["mean_outer_rare_mass_share"]) - safe_float(add2["mean_outer_rare_mass_share"]),
            "outer_union_gap_swap_minus_add": safe_float(swap2["mean_outer_tail_union_nodes"]) - safe_float(add2["mean_outer_tail_union_nodes"]),
            "outer_distance_gap_swap_minus_add": safe_float(swap2["mean_outer_weighted_mean_distance"]) - safe_float(add2["mean_outer_weighted_mean_distance"]),
        }
    )
    return out


def p2_support_score(row: Mapping[str, Any]) -> int:
    score = 0
    if safe_float(row["outer_entropy_gap_p2_minus_p0"]) <= -0.03:
        score += 1
    if safe_float(row["outer_top3_gap_p2_minus_p0"]) >= 0.05:
        score += 1
    if safe_float(row["outer_top5_gap_p2_minus_p0"]) >= 0.05:
        score += 1
    if safe_float(row["outer_core_mass_gap_p2_minus_p0"]) >= 0.05:
        score += 1
    if safe_float(row["outer_distance_gap_p2_minus_p0"]) >= 0.25:
        score += 1
    return score


def diagnosis_rows(
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    compares: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    by_compare = {str(row["compare_label"]): row for row in compares}
    add_score = p2_support_score(by_compare["add_chord_p2_minus_p0"])
    swap_score = p2_support_score(by_compare["local_swap_p2_minus_p0"])
    cross = by_compare["local_swap_p2_minus_add_chord_p2"]

    if add_score >= 4 and swap_score >= 4:
        status = "shared_p2_outer_concentration_candidate"
        note = (
            f"Begge carrierne viser en mer konsentrert outer-occupancy ved p2 enn ved p0 "
            f"(scores add={add_score}/5, swap={swap_score}/5)."
        )
        next_step = "measure_outer_flux_concentration"
        next_note = "Neste steg bor male om outer-massen mates gjennom noen fa foretrukne feeder-soner."
    elif add_score >= 3 or swap_score >= 3:
        status = "shared_p2_outer_concentration_weak"
        note = f"Outer-occupancy peker svakt mot en delt p2-konsentrasjon (scores add={add_score}/5, swap={swap_score}/5), men ikke rent nok ennå."
        next_step = "flux_or_feeder_observable"
        next_note = "Neste steg bor vaere en flux- eller feeder-observabel, ikke mer ren occupancy-oppsummering."
    else:
        status = "outer_concentration_not_yet"
        note = "Outer-occupancy-konsentrasjonen skiller ikke p2 fra p0 rent i begge carrierne."
        next_step = "different_p2_observable"
        next_note = "Neste steg bor vaere en annen p2-observabel, ikke mer outer-occupancy-tuning."

    carrier_alignment = "aligned"
    if (
        abs(safe_float(cross["outer_entropy_gap_swap_minus_add"])) >= 0.05
        or abs(safe_float(cross["outer_top3_gap_add_minus_swap"])) >= 0.05
    ):
        carrier_alignment = "mixed"

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "shared_p2_outer_concentration",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "carrier_alignment",
            "status": carrier_alignment,
            "note": "Carrier-alignment her betyr bare at p2-vs-p0-gapen peker samme vei i begge carrierne, ikke at alle detaljer er like.",
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
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cj: target-768 outer occupancy concentration lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om p2 skiller seg fra p0 gjennom mer konsentrert outer-occupancy selv om outer-genealogien forble reseeded i `v15ci`.")
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
    lines.append("## Outer occupancy summary")
    lines.append("")
    lines.append("| profile | outer union | active | entropy | top1 | top3 | top5 | core mass | rare mass | outer dist |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {fmt(row['mean_outer_tail_union_nodes'])} | {fmt(row['mean_outer_active_rate'])} | {fmt(row['mean_outer_occupancy_entropy'])} | {fmt(row['mean_outer_top1_mass_share'])} | {fmt(row['mean_outer_top3_mass_share'])} | {fmt(row['mean_outer_top5_mass_share'])} | {fmt(row['mean_outer_core_mass_share'])} | {fmt(row['mean_outer_rare_mass_share'])} | {fmt(row['mean_outer_weighted_mean_distance'])} |"
        )
    lines.append("")
    lines.append("## P2 versus P0")
    lines.append("")
    lines.append("| compare | entropy gap | top3 gap | top5 gap | core mass gap | rare mass gap | union gap | distance gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares[:2]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['outer_entropy_gap_p2_minus_p0'])} | {fmt(row['outer_top3_gap_p2_minus_p0'])} | {fmt(row['outer_top5_gap_p2_minus_p0'])} | {fmt(row['outer_core_mass_gap_p2_minus_p0'])} | {fmt(row['outer_rare_mass_gap_p2_minus_p0'])} | {fmt(row['outer_union_gap_p2_minus_p0'])} | {fmt(row['outer_distance_gap_p2_minus_p0'])} |"
        )
    lines.append("")
    lines.append("## Cross-carrier P2 contrast")
    lines.append("")
    lines.append("| compare | entropy gap swap-add | top3 gap add-swap | top5 gap add-swap | core mass gap add-swap | rare mass gap swap-add | union gap swap-add | distance gap swap-add |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares[2:]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['outer_entropy_gap_swap_minus_add'])} | {fmt(row['outer_top3_gap_add_minus_swap'])} | {fmt(row['outer_top5_gap_add_minus_swap'])} | {fmt(row['outer_core_mass_gap_add_minus_swap'])} | {fmt(row['outer_rare_mass_gap_swap_minus_add'])} | {fmt(row['outer_union_gap_swap_minus_add'])} | {fmt(row['outer_distance_gap_swap_minus_add'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ny p2-observabel innen samme target-768-spor, ikke et nytt skalahopp.")
    lines.append("- Positivt signal her betyr at p2 holder outer-halen på færre og tyngre noder, ikke at vi har funnet en partikkel.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15cj", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Les dette som en smal outer-occupancy-observabel ved target 768, ikke som bred fysikktolkning.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15cj",
        "",
        "Denne runden ser pa om den ytre halen ved p2 blir baaret av noen fa tunge steder, i stedet for aa vaere jevnt spredt utover.",
        "",
        f"- Hovedresultat: `{diag['shared_p2_outer_concentration']['status']}`.",
        f"- Carrier alignment: `{diag['carrier_alignment']['status']}`.",
        "",
        "Dette er fortsatt bare en smal lesning av ett lokalt signal ved target 768.",
        "Det er ikke en paastand om partikler eller spacetime-lignende struktur.",
        "",
        f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cj target-768 outer occupancy concentration lab.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cj_target768_outer_occupancy_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cj_target768_outer_occupancy_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cj_target768_outer_occupancy_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15cj_target768_outer_occupancy_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cj_target768_outer_occupancy_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cj_target768_outer_occupancy_concentration_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cj_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cj.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    base_row = next(
        row for row in base_rows
        if int(row["target_nodes"]) == TARGET and int(row["growth_seed"]) == GROWTH_SEED
    )
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
                metrics = outer_occupancy_metrics(base_state.g, list(res["perturbation_info"]["support"]), res["damaged_sets"])
                recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
                drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                info = dict(res["perturbation_info"])
                run_rows.append(
                    {
                        "profile_label": f"{perturbation}_p{int(placement)}",
                        "perturbation": perturbation,
                        "placement": int(placement),
                        "target_nodes": TARGET,
                        "growth_seed": GROWTH_SEED,
                        "seed_delta": int(seed_delta),
                        "run_seed": int(run_seed),
                        "requested_match": int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
                        "support_signature": ",".join(str(x) for x in info.get("support", [])),
                        "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                        "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                        **metrics,
                        "abs_delta_spectral_radius_rel": safe_float(drift["abs_delta_spectral_radius_rel"]),
                    }
                )

    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    aggregate = aggregate_rows(run_rows)
    compares = compare_rows(aggregate)
    diagnosis = diagnosis_rows(target_summary, run_rows, aggregate, compares)

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_compare_csv, compares)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            target_summary=target_summary,
            aggregate=aggregate,
            compares=compares,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
