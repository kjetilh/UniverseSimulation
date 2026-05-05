#!/usr/bin/env python3
"""v0.15ck target-768 outer feeder flux lab.

v15ci and v15cj narrowed the target-768 p2 question:

- outer genealogy is too generic; p0 is outer-active too
- outer occupancy concentration points only weakly toward a shared p2 story

The next narrow step is a feeder/flux observable:

when new outer-shell damage appears, does it tend to be fed through a small set
of inner-shell feeder nodes, and is that more concentrated at p2 than at p0?
"""
from __future__ import annotations

import argparse
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 768
GROWTH_SEED = 202
PLACEMENTS = (0, 2)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (4507, 4561, 4603, 4651)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
OUTER_DISTANCE_FLOOR = 4
INNER_FEEDER_DISTANCE = 3


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
    perturbation_offset = {"add_chord": 1611, "local_swap": 1687}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def classify_nodes(damaged: Set[int], base_dist: Mapping[int, int], fallback: int) -> Tuple[Set[int], Set[int]]:
    outer = {
        node for node in damaged
        if int(base_dist.get(node, fallback)) >= OUTER_DISTANCE_FLOOR
    }
    feeder = {
        node for node in damaged
        if int(base_dist.get(node, fallback)) == INNER_FEEDER_DISTANCE
    }
    return outer, feeder


def mass_top_share(counter: Counter[int], top_k: int) -> float:
    total = sum(counter.values())
    if total <= 0:
        return float("nan")
    return sum(count for _node, count in counter.most_common(top_k)) / total


def flux_snapshot_rows(
    *,
    perturbation: str,
    placement: int,
    seed_delta: int,
    run_seed: int,
    support_signature: str,
    log_rows: Sequence[Mapping[str, Any]],
    damaged_sets: Sequence[Set[int]],
    control_graphs: Sequence[v7.UGraph],
    base_dist: Mapping[int, int],
    fallback: int,
) -> List[Dict[str, Any]]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(log_rows))))
    rows: List[Dict[str, Any]] = []
    for idx in range(tail_start + 1, len(log_rows)):
        prev_damaged = set(damaged_sets[idx - 1])
        curr_damaged = set(damaged_sets[idx])
        prev_outer, prev_feeder = classify_nodes(prev_damaged, base_dist, fallback)
        curr_outer, _curr_feeder = classify_nodes(curr_damaged, base_dist, fallback)
        new_outer = curr_outer.difference(prev_outer)
        control_graph = control_graphs[idx]

        feeder_contrib: Counter[int] = Counter()
        self_contrib: Counter[int] = Counter()
        new_outer_with_feeder = 0
        new_outer_with_outer_parent = 0
        for node in new_outer:
            feeder_hits = []
            outer_hits = []
            if node in control_graph.adj:
                for nbr in control_graph.neighbors(node):
                    if nbr in prev_feeder:
                        feeder_hits.append(nbr)
                        feeder_contrib[nbr] += 1
                    if nbr in prev_outer:
                        outer_hits.append(nbr)
                        self_contrib[nbr] += 1
            if feeder_hits:
                new_outer_with_feeder += 1
            if outer_hits:
                new_outer_with_outer_parent += 1

        rows.append(
            {
                "profile_label": f"{perturbation}_p{int(placement)}",
                "perturbation": perturbation,
                "placement": int(placement),
                "seed_delta": int(seed_delta),
                "run_seed": int(run_seed),
                "support_signature": support_signature,
                "snapshot_index": int(idx - tail_start),
                "step": int(log_rows[idx]["step"]),
                "prev_outer_nodes": int(len(prev_outer)),
                "curr_outer_nodes": int(len(curr_outer)),
                "new_outer_nodes": int(len(new_outer)),
                "prev_feeder_nodes": int(len(prev_feeder)),
                "new_outer_feeder_coverage": (new_outer_with_feeder / len(new_outer)) if new_outer else float("nan"),
                "new_outer_self_parent_coverage": (new_outer_with_outer_parent / len(new_outer)) if new_outer else float("nan"),
                "feeder_source_count": int(len(feeder_contrib)),
                "self_parent_source_count": int(len(self_contrib)),
                "feeder_top1_share": mass_top_share(feeder_contrib, 1),
                "feeder_top3_share": mass_top_share(feeder_contrib, 3),
                "self_parent_top1_share": mass_top_share(self_contrib, 1),
                "self_parent_top3_share": mass_top_share(self_contrib, 3),
            }
        )
    return rows


def flux_run_summary(
    *,
    perturbation: str,
    placement: int,
    seed_delta: int,
    run_seed: int,
    requested_match: int,
    support_signature: str,
    recurrence: Mapping[str, Any],
    drift: Mapping[str, Any],
    snapshot_rows: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    rows_with_births = [row for row in snapshot_rows if int(row["new_outer_nodes"]) > 0]
    if rows_with_births:
        mean_feeder_cov = mean_defined(
            safe_float(row["new_outer_feeder_coverage"])
            for row in rows_with_births
            if math.isfinite(safe_float(row["new_outer_feeder_coverage"]))
        )
        mean_self_cov = mean_defined(
            safe_float(row["new_outer_self_parent_coverage"])
            for row in rows_with_births
            if math.isfinite(safe_float(row["new_outer_self_parent_coverage"]))
        )
        mean_feeder_top1 = mean_defined(
            safe_float(row["feeder_top1_share"])
            for row in rows_with_births
            if math.isfinite(safe_float(row["feeder_top1_share"]))
        )
        mean_feeder_top3 = mean_defined(
            safe_float(row["feeder_top3_share"])
            for row in rows_with_births
            if math.isfinite(safe_float(row["feeder_top3_share"]))
        )
    else:
        mean_feeder_cov = float("nan")
        mean_self_cov = float("nan")
        mean_feeder_top1 = float("nan")
        mean_feeder_top3 = float("nan")

    total_new_outer = sum(int(row["new_outer_nodes"]) for row in snapshot_rows)
    total_prev_outer = sum(int(row["prev_outer_nodes"]) for row in snapshot_rows)
    total_prev_feeder = sum(int(row["prev_feeder_nodes"]) for row in snapshot_rows)

    if (
        math.isfinite(mean_feeder_cov)
        and mean_feeder_cov >= 0.60
        and math.isfinite(mean_feeder_top3)
        and mean_feeder_top3 >= 0.50
    ):
        flux_label = "concentrated_feeder_flux"
    elif math.isfinite(mean_feeder_cov) and mean_feeder_cov >= 0.60:
        flux_label = "diffuse_feeder_flux"
    elif math.isfinite(mean_self_cov) and mean_self_cov >= 0.60:
        flux_label = "self_propagating_outer_flux"
    else:
        flux_label = "mixed_flux"

    return {
        "profile_label": f"{perturbation}_p{int(placement)}",
        "perturbation": perturbation,
        "placement": int(placement),
        "seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "requested_match": int(requested_match),
        "support_signature": support_signature,
        "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
        "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
        "snapshots_with_outer_births": len(rows_with_births),
        "total_new_outer_nodes": int(total_new_outer),
        "total_prev_outer_nodes": int(total_prev_outer),
        "total_prev_feeder_nodes": int(total_prev_feeder),
        "outer_birth_intensity": (total_new_outer / max(1, len(snapshot_rows))),
        "mean_feeder_coverage": mean_feeder_cov,
        "mean_self_parent_coverage": mean_self_cov,
        "mean_feeder_top1_share": mean_feeder_top1,
        "mean_feeder_top3_share": mean_feeder_top3,
        "flux_label": flux_label,
        "abs_delta_spectral_radius_rel": safe_float(drift["abs_delta_spectral_radius_rel"]),
    }


def aggregate_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        for placement in PLACEMENTS:
            group = [
                row for row in run_rows
                if str(row["perturbation"]) == perturbation and int(row["placement"]) == int(placement)
            ]
            out.append(
                {
                    "profile_label": f"{perturbation}_p{int(placement)}",
                    "perturbation": perturbation,
                    "placement": int(placement),
                    "n_runs": len(group),
                    "concentrated_feeder_flux_rate": mean_defined(
                        1.0 if str(row["flux_label"]) == "concentrated_feeder_flux" else 0.0 for row in group
                    ),
                    "diffuse_feeder_flux_rate": mean_defined(
                        1.0 if str(row["flux_label"]) == "diffuse_feeder_flux" else 0.0 for row in group
                    ),
                    "self_propagating_outer_flux_rate": mean_defined(
                        1.0 if str(row["flux_label"]) == "self_propagating_outer_flux" else 0.0 for row in group
                    ),
                    "mixed_flux_rate": mean_defined(
                        1.0 if str(row["flux_label"]) == "mixed_flux" else 0.0 for row in group
                    ),
                    "mean_outer_birth_intensity": mean_defined(safe_float(row["outer_birth_intensity"]) for row in group),
                    "mean_feeder_coverage": mean_defined(safe_float(row["mean_feeder_coverage"]) for row in group),
                    "mean_self_parent_coverage": mean_defined(safe_float(row["mean_self_parent_coverage"]) for row in group),
                    "mean_feeder_top1_share": mean_defined(safe_float(row["mean_feeder_top1_share"]) for row in group),
                    "mean_feeder_top3_share": mean_defined(safe_float(row["mean_feeder_top3_share"]) for row in group),
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
                "concentrated_rate_gap": safe_float(p2["concentrated_feeder_flux_rate"]) - safe_float(p0["concentrated_feeder_flux_rate"]),
                "feeder_coverage_gap": safe_float(p2["mean_feeder_coverage"]) - safe_float(p0["mean_feeder_coverage"]),
                "feeder_top1_gap": safe_float(p2["mean_feeder_top1_share"]) - safe_float(p0["mean_feeder_top1_share"]),
                "feeder_top3_gap": safe_float(p2["mean_feeder_top3_share"]) - safe_float(p0["mean_feeder_top3_share"]),
                "self_parent_gap": safe_float(p2["mean_self_parent_coverage"]) - safe_float(p0["mean_self_parent_coverage"]),
                "birth_intensity_gap": safe_float(p2["mean_outer_birth_intensity"]) - safe_float(p0["mean_outer_birth_intensity"]),
            }
        )
    add2 = by["add_chord_p2"]
    swap2 = by["local_swap_p2"]
    out.append(
        {
            "compare_label": "local_swap_p2_minus_add_chord_p2",
            "concentrated_rate_gap": safe_float(swap2["concentrated_feeder_flux_rate"]) - safe_float(add2["concentrated_feeder_flux_rate"]),
            "feeder_coverage_gap": safe_float(swap2["mean_feeder_coverage"]) - safe_float(add2["mean_feeder_coverage"]),
            "feeder_top1_gap": safe_float(swap2["mean_feeder_top1_share"]) - safe_float(add2["mean_feeder_top1_share"]),
            "feeder_top3_gap": safe_float(swap2["mean_feeder_top3_share"]) - safe_float(add2["mean_feeder_top3_share"]),
            "self_parent_gap": safe_float(swap2["mean_self_parent_coverage"]) - safe_float(add2["mean_self_parent_coverage"]),
            "birth_intensity_gap": safe_float(swap2["mean_outer_birth_intensity"]) - safe_float(add2["mean_outer_birth_intensity"]),
        }
    )
    return out


def feeder_support_score(row: Mapping[str, Any]) -> int:
    score = 0
    if safe_float(row["concentrated_rate_gap"]) >= 0.25:
        score += 1
    if safe_float(row["feeder_coverage_gap"]) >= 0.10:
        score += 1
    if safe_float(row["feeder_top1_gap"]) >= 0.05:
        score += 1
    if safe_float(row["feeder_top3_gap"]) >= 0.10:
        score += 1
    if safe_float(row["birth_intensity_gap"]) >= 0.25:
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
    add_score = feeder_support_score(by_compare["add_chord_p2_minus_p0"])
    swap_score = feeder_support_score(by_compare["local_swap_p2_minus_p0"])

    if add_score >= 4 and swap_score >= 4:
        status = "shared_p2_feeder_flux_candidate"
        note = f"Begge carrierne viser mer konsentrert feeder-flux ved p2 enn ved p0 (scores add={add_score}/5, swap={swap_score}/5)."
        next_step = "follow_feeder_nodes"
        next_note = "Neste steg bor spore hvilke konkrete feeder-noder eller smale soner som baerer outer-fluksen."
    elif add_score >= 3 or swap_score >= 3:
        status = "shared_p2_feeder_flux_weak"
        note = f"Feeder-flux peker svakt mot en p2-spesifikk mating av outer-halen (scores add={add_score}/5, swap={swap_score}/5), men ikke rent nok ennå."
        next_step = "trace_concrete_feeder_cases"
        next_note = "Neste steg bor vaere case-sporing av de sterkeste feeder-runene heller enn flere brede oppsummeringer."
    else:
        status = "feeder_flux_not_yet"
        note = "Feeder-fluxen skiller ikke p2 fra p0 rent i begge carrierne."
        next_step = "different_mechanism_axis"
        next_note = "Neste steg bor vaere en annen mekanismeakse enn outer-flux."

    carrier_alignment = "aligned"
    cross = by_compare["local_swap_p2_minus_add_chord_p2"]
    if abs(safe_float(cross["feeder_top3_gap"])) >= 0.10:
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
            "diagnostic_family": "shared_p2_feeder_flux",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "carrier_alignment",
            "status": carrier_alignment,
            "note": "Carrier-alignment her betyr bare at p2-vs-p0-feeder-gapen peker samme vei i begge carrierne.",
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
    lines.append("# Relasjonell universgraf v0.15ck: target-768 outer feeder flux lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om ny outer-masse ved p2 mates gjennom fa, konsentrerte feeder-soner fra inner shell-3.")
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
    lines.append("## Aggregate feeder flux")
    lines.append("")
    lines.append("| profile | concentrated | diffuse | self-prop | mixed | birth intensity | feeder cov | feeder top1 | feeder top3 | self-parent cov |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {fmt(row['concentrated_feeder_flux_rate'])} | {fmt(row['diffuse_feeder_flux_rate'])} | {fmt(row['self_propagating_outer_flux_rate'])} | {fmt(row['mixed_flux_rate'])} | {fmt(row['mean_outer_birth_intensity'])} | {fmt(row['mean_feeder_coverage'])} | {fmt(row['mean_feeder_top1_share'])} | {fmt(row['mean_feeder_top3_share'])} | {fmt(row['mean_self_parent_coverage'])} |"
        )
    lines.append("")
    lines.append("## P2 versus P0")
    lines.append("")
    lines.append("| compare | concentrated gap | feeder cov gap | feeder top1 gap | feeder top3 gap | self-parent gap | birth intensity gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in compares[:2]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['concentrated_rate_gap'])} | {fmt(row['feeder_coverage_gap'])} | {fmt(row['feeder_top1_gap'])} | {fmt(row['feeder_top3_gap'])} | {fmt(row['self_parent_gap'])} | {fmt(row['birth_intensity_gap'])} |"
        )
    lines.append("")
    lines.append("## Cross-carrier P2 contrast")
    lines.append("")
    lines.append("| compare | concentrated gap | feeder cov gap | feeder top1 gap | feeder top3 gap | self-parent gap | birth intensity gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in compares[2:]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['concentrated_rate_gap'])} | {fmt(row['feeder_coverage_gap'])} | {fmt(row['feeder_top1_gap'])} | {fmt(row['feeder_top3_gap'])} | {fmt(row['self_parent_gap'])} | {fmt(row['birth_intensity_gap'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en smal flux-observabel ved target 768, ikke et nytt skalahopp.")
    lines.append("- Positivt signal her betyr bare at outer-halen mates gjennom fa indre feeder-soner ved p2.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15ck", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Les dette som en smal feeder-flux-observabel, ikke som bevis for partikler eller universell geometri.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15ck",
        "",
        "Denne runden ser pa om den ytre halen ved p2 blir matet fra noen fa indre steder, i stedet for aa vokse jevnt overalt.",
        "",
        f"- Hovedresultat: `{diag['shared_p2_feeder_flux']['status']}`.",
        f"- Carrier alignment: `{diag['carrier_alignment']['status']}`.",
        "",
        "Dette er fortsatt bare en liten, lokal mekanisk test ved target 768.",
        "Det er ikke en paastand om partikler eller verdensgeometri.",
        "",
        f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ck target-768 outer feeder flux lab.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15ck_target768_outer_feeder_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15ck_target768_outer_feeder_runs.csv")
    p.add_argument("--out-snapshot-csv", type=str, default="Documentation/v15ck_target768_outer_feeder_snapshot_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ck_target768_outer_feeder_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15ck_target768_outer_feeder_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ck_target768_outer_feeder_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ck_target768_outer_feeder_flux_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ck_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ck.md")
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
    snapshot_rows: List[Dict[str, Any]] = []

    for perturbation in PERTURBATIONS:
        for placement in PLACEMENTS:
            for seed_delta in SEED_DELTAS:
                run_seed = run_seed_for(perturbation=perturbation, placement=placement, seed_delta=seed_delta)
                res = v15ae.run_defect_with_control_graphs(
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
                drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                info = dict(res["perturbation_info"])
                support = [int(x) for x in info.get("support", [])]
                base_dist = v7.bfs_distances(base_state.g, support)
                fallback = (max(base_dist.values()) + 1) if base_dist else 1
                rows = flux_snapshot_rows(
                    perturbation=perturbation,
                    placement=placement,
                    seed_delta=seed_delta,
                    run_seed=run_seed,
                    support_signature=",".join(str(x) for x in support),
                    log_rows=res["log_rows"],
                    damaged_sets=res["damaged_sets"],
                    control_graphs=res["control_graphs"],
                    base_dist=base_dist,
                    fallback=fallback,
                )
                snapshot_rows.extend(rows)
                run_rows.append(
                    flux_run_summary(
                        perturbation=perturbation,
                        placement=placement,
                        seed_delta=seed_delta,
                        run_seed=run_seed,
                        requested_match=int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
                        support_signature=",".join(str(x) for x in support),
                        recurrence=recurrence,
                        drift=drift,
                        snapshot_rows=rows,
                    )
                )

    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    aggregate = aggregate_rows(run_rows)
    compares = compare_rows(aggregate)
    diagnosis = diagnosis_rows(target_summary, run_rows, aggregate, compares)

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_snapshot_csv, snapshot_rows)
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
