#!/usr/bin/env python3
"""v0.15ca target-192 radial occupancy mechanism lab.

This is the mechanism-side follow-up to v15bx/v15by. It does not try to refine
family labels further. Instead it asks:

what radial occupancy pattern around the perturbation support separates the
target-192 p1/p2 boundary, if anything?

The setup is intentionally narrow:
- target 192 only
- growth seed 202 only
- placements 1 and 2 only
- add_chord and local_swap only
- fresh seeds
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15ad_add_chord_boundary_shell_lab as v15ad
import relational_universe_v15aw_local_swap_core_shell_lab as v15aw
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15bu_same_locus_carrier_occupancy_spectrum_lab as v15bu
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 192
GROWTH_SEED = 202
PLACEMENTS = (1, 2)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (1663, 1693, 1721, 1753)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY


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
    perturbation_offset = {"add_chord": 503, "local_swap": 557}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def weighted_shell_entropy(masses: Sequence[float]) -> float:
    vals = [float(x) for x in masses if float(x) > 0.0]
    if len(vals) <= 1:
        return 0.0
    total = sum(vals)
    probs = [x / total for x in vals]
    return -sum(p * math.log(p) for p in probs if p > 0.0) / math.log(len(probs))


def radial_occupancy_metrics(base_state: v7.State, support: Sequence[int], damaged_sets: Sequence[Set[int]]) -> Dict[str, Any]:
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
            "participation_ratio": float("nan"),
            "effective_support_fraction": float("nan"),
            "weighted_mean_distance": float("nan"),
            "weighted_distance_sd": float("nan"),
            "shell0_mass_share": float("nan"),
            "shell1_mass_share": float("nan"),
            "shell2_mass_share": float("nan"),
            "shell3_mass_share": float("nan"),
            "shell4plus_mass_share": float("nan"),
            "shell_entropy": float("nan"),
            "rare_mass_share": float("nan"),
        }

    occ = {node: count / denom for node, count in counts.items()}
    total_mass = sum(occ.values())
    probs = {node: mass / total_mass for node, mass in occ.items()}
    entropy = -sum(p * math.log(p) for p in probs.values() if p > 0.0) / math.log(len(probs)) if len(probs) > 1 else 0.0
    participation = 1.0 / sum(p * p for p in probs.values())
    effective_support_fraction = participation / max(1.0, len(probs))

    dist = v7.bfs_distances(base_state.g, support)
    fallback_distance = (max(dist.values()) + 1) if dist else 1
    shell_mass = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
    mean_distance = 0.0
    rare_mass = 0.0
    for node, p in probs.items():
        d = int(dist.get(node, fallback_distance))
        bucket = d if d <= 3 else 4
        shell_mass[bucket] += p
        mean_distance += p * d
        if occ[node] < 0.20:
            rare_mass += p
    sd = math.sqrt(sum(p * (int(dist.get(node, fallback_distance)) - mean_distance) ** 2 for node, p in probs.items()))
    shell_entropy = weighted_shell_entropy([shell_mass[k] for k in (0, 1, 2, 3, 4)])
    return {
        "tail_union_nodes": int(len(probs)),
        "occupancy_entropy": entropy,
        "participation_ratio": participation,
        "effective_support_fraction": effective_support_fraction,
        "weighted_mean_distance": mean_distance,
        "weighted_distance_sd": sd,
        "shell0_mass_share": shell_mass[0],
        "shell1_mass_share": shell_mass[1],
        "shell2_mass_share": shell_mass[2],
        "shell3_mass_share": shell_mass[3],
        "shell4plus_mass_share": shell_mass[4],
        "shell_entropy": shell_entropy,
        "rare_mass_share": rare_mass,
    }


def aggregate_profile(rows: Sequence[Mapping[str, Any]], *, perturbation: str, placement: int) -> Dict[str, Any]:
    return {
        "profile_label": f"{perturbation}_p{int(placement)}",
        "perturbation": perturbation,
        "placement": int(placement),
        "n_runs": len(rows),
        "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in rows),
        "mean_occupancy_entropy": mean_defined(safe_float(row["occupancy_entropy"]) for row in rows),
        "mean_participation_ratio": mean_defined(safe_float(row["participation_ratio"]) for row in rows),
        "mean_effective_support_fraction": mean_defined(safe_float(row["effective_support_fraction"]) for row in rows),
        "mean_weighted_mean_distance": mean_defined(safe_float(row["weighted_mean_distance"]) for row in rows),
        "mean_weighted_distance_sd": mean_defined(safe_float(row["weighted_distance_sd"]) for row in rows),
        "mean_shell0_mass_share": mean_defined(safe_float(row["shell0_mass_share"]) for row in rows),
        "mean_shell1_mass_share": mean_defined(safe_float(row["shell1_mass_share"]) for row in rows),
        "mean_shell2_mass_share": mean_defined(safe_float(row["shell2_mass_share"]) for row in rows),
        "mean_shell3_mass_share": mean_defined(safe_float(row["shell3_mass_share"]) for row in rows),
        "mean_shell4plus_mass_share": mean_defined(safe_float(row["shell4plus_mass_share"]) for row in rows),
        "mean_shell_entropy": mean_defined(safe_float(row["shell_entropy"]) for row in rows),
        "mean_rare_mass_share": mean_defined(safe_float(row["rare_mass_share"]) for row in rows),
        "mean_abs_delta_spectral_radius_rel": mean_defined(safe_float(row["abs_delta_spectral_radius_rel"]) for row in rows),
        "mean_abs_delta_dim_proxy_rel": mean_defined(safe_float(row["abs_delta_dim_proxy_rel"]) for row in rows),
    }


def comparison_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by = {str(row["profile_label"]): dict(row) for row in aggregate}
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        p1 = by[f"{perturbation}_p1"]
        p2 = by[f"{perturbation}_p2"]
        out.append(
            {
                "perturbation": perturbation,
                "weighted_mean_distance_gap_p2_minus_p1": safe_float(p2["mean_weighted_mean_distance"]) - safe_float(p1["mean_weighted_mean_distance"]),
                "shell4plus_gap_p2_minus_p1": safe_float(p2["mean_shell4plus_mass_share"]) - safe_float(p1["mean_shell4plus_mass_share"]),
                "shell_entropy_gap_p2_minus_p1": safe_float(p2["mean_shell_entropy"]) - safe_float(p1["mean_shell_entropy"]),
                "participation_gap_p2_minus_p1": safe_float(p2["mean_participation_ratio"]) - safe_float(p1["mean_participation_ratio"]),
                "rare_mass_gap_p2_minus_p1": safe_float(p2["mean_rare_mass_share"]) - safe_float(p1["mean_rare_mass_share"]),
                "spectral_rel_gap_p2_minus_p1": safe_float(p2["mean_abs_delta_spectral_radius_rel"]) - safe_float(p1["mean_abs_delta_spectral_radius_rel"]),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    diffuse_edges = 0
    rare_edges = 0
    for row in comparisons:
        if safe_float(row["weighted_mean_distance_gap_p2_minus_p1"]) >= 0.10 and safe_float(row["shell4plus_gap_p2_minus_p1"]) >= 0.03:
            diffuse_edges += 1
        if safe_float(row["rare_mass_gap_p2_minus_p1"]) >= 0.05 and safe_float(row["participation_gap_p2_minus_p1"]) >= 1.0:
            rare_edges += 1

    if diffuse_edges >= 2 and rare_edges >= 1:
        status = "radial_diffuse_boundary_supported"
        note = "p2 ligger lenger ute i radial occupancy og bærer mer rare/distributed masse enn p1 i begge perturbasjoner."
        next_step = "connect_radial_boundary_to_scale"
        next_note = "Neste steg bor teste om denne radial-/rare-aksen er det som styrer target-192/384 overgangen."
    elif diffuse_edges >= 1 or rare_edges >= 1:
        status = "radial_diffuse_boundary_weak"
        note = "Det finnes en svak p1/p2-radial eller rare-masseforskjell, men ikke sterkt nok til en ren mekanismeclaim."
        next_step = "target384_or_second_mechanism"
        next_note = "Neste steg bor enten koble dette til target 384 eller velge en ny mekanismeobservabel."
    else:
        status = "radial_diffuse_boundary_not_yet"
        note = "Den nye radial occupancy-observabelen forklarer ikke p1/p2-grensen rent."
        next_step = "target384_or_new_mechanism"
        next_note = "Neste steg bor vaere target 384 eller en annen mekanismeobservabel, ikke mer av samme p1/p2-runde."

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
            "diagnostic_family": "radial_mechanism",
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
    comparisons: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15ca: target-192 radial occupancy mechanism lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden bruker en ny observabelklasse: radial occupancy-fordeling rundt perturbasjonssupport.")
    lines.append("Sporsmalet er om p1/p2-grensen ved target 192 faktisk ser ut som en radial/rare/distributed overgang.")
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
    lines.append("## Aggregert radial occupancy")
    lines.append("")
    lines.append("| profile | coarse | occ entropy | participation | mean dist | shell4+ | rare mass | spectral rel |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_occupancy_entropy'])} | {fmt(row['mean_participation_ratio'])} | {fmt(row['mean_weighted_mean_distance'])} | {fmt(row['mean_shell4plus_mass_share'])} | {fmt(row['mean_rare_mass_share'])} | {fmt(row['mean_abs_delta_spectral_radius_rel'])} |"
        )
    lines.append("")
    lines.append("## P2 minus P1")
    lines.append("")
    lines.append("| perturbation | mean dist gap | shell4+ gap | shell entropy gap | participation gap | rare mass gap | spectral rel gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in comparisons:
        lines.append(
            f"| {row['perturbation']} | {fmt(row['weighted_mean_distance_gap_p2_minus_p1'])} | {fmt(row['shell4plus_gap_p2_minus_p1'])} | {fmt(row['shell_entropy_gap_p2_minus_p1'])} | {fmt(row['participation_gap_p2_minus_p1'])} | {fmt(row['rare_mass_gap_p2_minus_p1'])} | {fmt(row['spectral_rel_gap_p2_minus_p1'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en mekanismeobservabel, ikke en ny family-label-runde.")
    lines.append("- Positivt signal her betyr at p2 virkelig ligger lenger ute og mer distribuert enn p1, ikke bare at labelene er forskjellige.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ca target-192 radial occupancy mechanism lab.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15ca_target192_radial_occupancy_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15ca_target192_radial_occupancy_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ca_target192_radial_occupancy_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15ca_target192_radial_occupancy_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ca_target192_radial_occupancy_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ca_target192_radial_occupancy_mechanism_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ca_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ca.md")
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
                radial = radial_occupancy_metrics(base_state, support, res["damaged_sets"])
                occ = v15bu.occupancy_spectrum_metrics(res["damaged_sets"])
                drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                run_rows.append(
                    {
                        "profile_label": f"{perturbation}_p{int(placement)}",
                        "perturbation": perturbation,
                        "target_nodes": TARGET,
                        "growth_seed": GROWTH_SEED,
                        "placement": int(placement),
                        "seed_delta": int(seed_delta),
                        "run_seed": int(run_seed),
                        "requested_match": int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
                        "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                        "core_share_of_union": safe_float(core_shell["core_share_of_union"]),
                        "shell_share_of_union": safe_float(core_shell["shell_share_of_union"]),
                        "rare_share_of_union": safe_float(core_shell["rare_share_of_union"]),
                        "mean_shell_refresh": safe_float(shell["mean_shell_refresh"]),
                        **occ,
                        **radial,
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
    comparisons = comparison_rows(aggregate)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        comparisons=comparisons,
    )
    report_md = build_report(
        target_summary=target_summary,
        aggregate=aggregate,
        comparisons=comparisons,
        diagnosis=diagnosis,
    )
    op_md = "\n".join(
        [
            "# v0.15ca operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les dette som en mekanismeobservabel for target-192 p1/p2-grensen, ikke som en ny family-label-runde.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0_15ca",
            "",
            "Denne runden ser ikke bare på hvilke noder som blir skadet, men hvor langt fra startområdet skaden faktisk sprer massen sin i senfasen.",
            "",
            "Tanken er at p2 kanskje er mer utoverflytende og finfordelt enn p1, og at det kan forklare hvorfor target 192 ser bredt spectral/diffuse/rare ut.",
        ]
    ) + "\n"

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_compare_csv, comparisons)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
