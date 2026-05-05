#!/usr/bin/env python3
"""v0.15cl target-768 inner gate / global budget lab.

v15ch made the target-768 p2 horizon worth following. v15ci-v15ck then
tested obvious outer-tail mechanisms and did not get a clean shared p2
mechanism:

- outer genealogy was too generic
- outer occupancy was weak / carrier-split
- outer feeder flux was not clean

This round moves the mechanism axis inward. It asks whether p2's outer
horizon is preceded by an inner shell2/3 gate signal, and whether that signal
looks like redistribution under relatively stable global budget observables
rather than just more damage everywhere.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15cg_target768_far_shell_horizon_lab as v15cg
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 768
GROWTH_SEED = 202
PLACEMENTS = (0, 2)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (4703, 4751, 4801, 4861)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
OUTER_DISTANCE_FLOOR = 4
INNER_GATE_DISTANCES = (2, 3)
PRE_WINDOW = 8
POST_WINDOW = 12


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
    perturbation_offset = {"add_chord": 1811, "local_swap": 1877}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def rel_from_delta(row: Mapping[str, Any], key: str, base_row: Mapping[str, Any], base_key: str, floor: float = 1.0) -> float:
    denom = max(float(floor), abs(safe_float(base_row[base_key], floor)))
    return abs(safe_float(row.get(key), 0.0)) / denom


def induced_subgraph(g: v7.UGraph, nodes: Set[int]) -> v7.UGraph:
    sub = v7.UGraph()
    for node in nodes:
        if node in g.adj:
            sub.add_node(node)
    for a in nodes:
        if a not in g.adj:
            continue
        for b in g.neighbors(a):
            if b in nodes and a < b:
                sub.add_edge(a, b)
    return sub


def shell_counts(damaged: Set[int], base_dist: Mapping[int, int], fallback: int) -> Dict[str, int]:
    counts = {"shell0": 0, "shell1": 0, "shell2": 0, "shell3": 0, "outer": 0}
    for node in damaged:
        dist = int(base_dist.get(node, fallback))
        if dist <= 0:
            counts["shell0"] += 1
        elif dist == 1:
            counts["shell1"] += 1
        elif dist == 2:
            counts["shell2"] += 1
        elif dist == 3:
            counts["shell3"] += 1
        else:
            counts["outer"] += 1
    return counts


def mean_distance(damaged: Set[int], base_dist: Mapping[int, int], fallback: int) -> float:
    if not damaged:
        return 0.0
    return sum(int(base_dist.get(node, fallback)) for node in damaged) / max(1, len(damaged))


def gate_nodes(damaged: Set[int], base_dist: Mapping[int, int]) -> Set[int]:
    return {node for node in damaged if int(base_dist.get(node, -999)) in INNER_GATE_DISTANCES}


def snapshot_rows_for_run(
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
    base_row: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(log_rows))))
    out: List[Dict[str, Any]] = []
    for idx in range(tail_start, len(log_rows)):
        damaged = set(damaged_sets[idx])
        counts = shell_counts(damaged, base_dist, fallback)
        total = max(1, len(damaged))
        shell23 = counts["shell2"] + counts["shell3"]
        outer = counts["outer"]
        control_graph = control_graphs[idx]
        gate_active = gate_nodes(damaged, base_dist)
        gate_sub = induced_subgraph(control_graph, gate_active)
        gate_boundary = v15.boundary_edge_count(control_graph, gate_active)
        far_share = outer / total
        weighted_distance = mean_distance(damaged, base_dist, fallback)
        if far_share >= v15cg.HIGH_SHARE_THRESHOLD and weighted_distance >= v15cg.HIGH_DISTANCE_THRESHOLD:
            horizon_band = "high"
        elif far_share >= v15cg.MID_SHARE_THRESHOLD and weighted_distance >= v15cg.MID_DISTANCE_THRESHOLD:
            horizon_band = "mid"
        else:
            horizon_band = "low"
        row = log_rows[idx]
        out.append(
            {
                "profile_label": f"{perturbation}_p{int(placement)}",
                "perturbation": perturbation,
                "placement": int(placement),
                "seed_delta": int(seed_delta),
                "run_seed": int(run_seed),
                "support_signature": support_signature,
                "snapshot_index": int(idx),
                "tail_index": int(idx - tail_start),
                "step": int(row["step"]),
                "damaged_nodes": int(len(damaged)),
                "shell0_nodes": int(counts["shell0"]),
                "shell1_nodes": int(counts["shell1"]),
                "shell2_nodes": int(counts["shell2"]),
                "shell3_nodes": int(counts["shell3"]),
                "shell23_nodes": int(shell23),
                "outer_nodes": int(outer),
                "shell23_share": shell23 / total,
                "outer_share": far_share,
                "weighted_mean_distance": weighted_distance,
                "horizon_band": horizon_band,
                "gate_beta1": int(v7.beta1_cycle_rank(gate_sub)),
                "gate_component_count": int(len(v15.damaged_components(control_graph, gate_active))),
                "gate_boundary_edges": int(gate_boundary),
                "gate_boundary_to_volume": (gate_boundary / len(gate_active)) if gate_active else float("nan"),
                "abs_delta_nodes_rel": rel_from_delta(row, "delta_nodes", base_row, "initial_nodes", floor=1.0),
                "abs_delta_beta1_rel": rel_from_delta(row, "delta_beta1", base_row, "initial_beta1", floor=1.0),
                "abs_delta_spectral_radius_rel": rel_from_delta(row, "delta_spectral_radius", base_row, "initial_spectral_radius", floor=1e-9),
                "abs_delta_dim_proxy_rel": rel_from_delta(row, "delta_dim_proxy", base_row, "initial_dim_proxy", floor=1e-9),
                "abs_delta_triangles_rel": rel_from_delta(row, "delta_triangles", base_row, "initial_triangles", floor=1.0),
            }
        )
    return out


def horizon_summary(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    bands = [str(row["horizon_band"]) for row in rows]
    high_start_raw = v15cg.first_run_ge(bands, "high", 3)
    window = len(bands)
    high_start = window if high_start_raw is None else int(high_start_raw)
    if high_start_raw is None:
        last_high = -1
        high_horizon = 0
        retention = 0.0
    else:
        high_positions = [idx for idx, band in enumerate(bands) if band == "high" and idx >= high_start_raw]
        last_high = max(high_positions)
        horizon_slice = bands[high_start_raw:last_high + 1]
        high_horizon = len(horizon_slice)
        retention = sum(1 for band in horizon_slice if band == "high") / max(1, len(horizon_slice))
    last12 = bands[-12:]
    last12_high_rate = sum(1 for band in last12 if band == "high") / max(1, len(last12)) if last12 else 0.0
    total_high_count = sum(1 for band in bands if band == "high")
    total_mid_count = sum(1 for band in bands if band == "mid")
    label = v15cg.classify_far_shell_horizon(
        high_start_index=high_start,
        last_high_index=last_high,
        high_horizon_span=high_horizon,
        high_retention_rate=retention,
        last12_high_rate=last12_high_rate,
        total_high_count=total_high_count,
        window=window,
    )
    return {
        "tail_snapshot_count": int(window),
        "high_start_index": int(high_start),
        "last_high_index": int(last_high),
        "high_horizon_span": int(high_horizon),
        "high_retention_rate": float(retention),
        "last12_high_rate": float(last12_high_rate),
        "total_high_count": int(total_high_count),
        "total_mid_count": int(total_mid_count),
        "longest_high_run": int(v15cg.longest_run(bands, "high")),
        "far_shell_horizon_label": label,
    }


def opposite_motion_rate(rows: Sequence[Mapping[str, Any]]) -> float:
    hits = 0
    trials = 0
    prev = None
    for row in rows:
        if prev is not None:
            d_outer = safe_float(row["outer_share"]) - safe_float(prev["outer_share"])
            d_gate = safe_float(row["shell23_share"]) - safe_float(prev["shell23_share"])
            if abs(d_outer) >= 0.01 or abs(d_gate) >= 0.01:
                trials += 1
                if d_outer * d_gate < 0:
                    hits += 1
        prev = row
    if trials <= 0:
        return float("nan")
    return hits / trials


def run_summary(
    *,
    perturbation: str,
    placement: int,
    seed_delta: int,
    run_seed: int,
    requested_match: int,
    support_signature: str,
    recurrence: Mapping[str, Any],
    final_drift: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    horizon = horizon_summary(rows)
    high_start = int(horizon["high_start_index"])
    window = len(rows)
    if high_start < window:
        pre_rows = list(rows[max(0, high_start - PRE_WINDOW):high_start])
        post_rows = list(rows[high_start:min(window, high_start + POST_WINDOW)])
    else:
        pre_rows = list(rows[:min(window, PRE_WINDOW)])
        post_rows = list(rows[max(0, window - POST_WINDOW):])
    if not pre_rows:
        pre_rows = list(rows[:1])
    if not post_rows:
        post_rows = list(rows[-1:])

    shell23_values = [safe_float(row["shell23_share"]) for row in rows]
    peak_idx = max(range(len(rows)), key=lambda idx: shell23_values[idx]) if rows else -1
    after_peak = list(rows[peak_idx:]) if peak_idx >= 0 else []
    peak_shell23 = shell23_values[peak_idx] if peak_idx >= 0 else float("nan")
    post_shell23_mean = mean_defined(safe_float(row["shell23_share"]) for row in post_rows)
    gate_release = peak_shell23 - post_shell23_mean if math.isfinite(peak_shell23) and math.isfinite(post_shell23_mean) else float("nan")
    outer_at_peak = safe_float(rows[peak_idx]["outer_share"]) if peak_idx >= 0 else float("nan")
    outer_after_peak = max((safe_float(row["outer_share"]) for row in after_peak), default=float("nan"))
    outer_after_gate_gain = outer_after_peak - outer_at_peak if math.isfinite(outer_after_peak) and math.isfinite(outer_at_peak) else float("nan")
    high_start_for_lag = high_start if high_start < window else float("nan")
    gate_lead_to_horizon = high_start_for_lag - peak_idx if math.isfinite(safe_float(high_start_for_lag)) and peak_idx >= 0 else float("nan")

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
        **horizon,
        "mean_outer_share": mean_defined(safe_float(row["outer_share"]) for row in rows),
        "mean_shell23_share": mean_defined(safe_float(row["shell23_share"]) for row in rows),
        "pre_horizon_mean_shell23_share": mean_defined(safe_float(row["shell23_share"]) for row in pre_rows),
        "pre_horizon_peak_shell23_share": max((safe_float(row["shell23_share"]) for row in pre_rows), default=float("nan")),
        "post_horizon_mean_shell23_share": post_shell23_mean,
        "gate_release_after_peak": gate_release,
        "outer_after_gate_gain": outer_after_gate_gain,
        "gate_lead_to_horizon_snapshots": gate_lead_to_horizon,
        "opposite_shell23_outer_motion_rate": opposite_motion_rate(rows),
        "mean_gate_boundary_to_volume": mean_defined(
            safe_float(row["gate_boundary_to_volume"])
            for row in rows
            if math.isfinite(safe_float(row["gate_boundary_to_volume"]))
        ),
        "mean_gate_beta1": mean_defined(safe_float(row["gate_beta1"]) for row in rows),
        "mean_abs_delta_spectral_radius_rel_tail": mean_defined(safe_float(row["abs_delta_spectral_radius_rel"]) for row in rows),
        "mean_abs_delta_beta1_rel_tail": mean_defined(safe_float(row["abs_delta_beta1_rel"]) for row in rows),
        "mean_abs_delta_dim_proxy_rel_tail": mean_defined(safe_float(row["abs_delta_dim_proxy_rel"]) for row in rows),
        "final_abs_delta_spectral_radius_rel": safe_float(final_drift["abs_delta_spectral_radius_rel"]),
        "final_abs_delta_beta1_rel": safe_float(final_drift["abs_delta_beta1_rel"]),
        "final_abs_delta_dim_proxy_rel": safe_float(final_drift["abs_delta_dim_proxy_rel"]),
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
                    "established_far_shell_rate": mean_defined(
                        1.0 if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon" else 0.0 for row in group
                    ),
                    "mean_high_retention_rate": mean_defined(safe_float(row["high_retention_rate"]) for row in group),
                    "mean_last12_high_rate": mean_defined(safe_float(row["last12_high_rate"]) for row in group),
                    "mean_outer_share": mean_defined(safe_float(row["mean_outer_share"]) for row in group),
                    "mean_shell23_share": mean_defined(safe_float(row["mean_shell23_share"]) for row in group),
                    "mean_pre_horizon_peak_shell23_share": mean_defined(safe_float(row["pre_horizon_peak_shell23_share"]) for row in group),
                    "mean_gate_release_after_peak": mean_defined(safe_float(row["gate_release_after_peak"]) for row in group),
                    "mean_outer_after_gate_gain": mean_defined(safe_float(row["outer_after_gate_gain"]) for row in group),
                    "mean_gate_lead_to_horizon_snapshots": mean_defined(
                        safe_float(row["gate_lead_to_horizon_snapshots"])
                        for row in group
                        if math.isfinite(safe_float(row["gate_lead_to_horizon_snapshots"]))
                    ),
                    "mean_opposite_shell23_outer_motion_rate": mean_defined(
                        safe_float(row["opposite_shell23_outer_motion_rate"])
                        for row in group
                        if math.isfinite(safe_float(row["opposite_shell23_outer_motion_rate"]))
                    ),
                    "mean_gate_boundary_to_volume": mean_defined(safe_float(row["mean_gate_boundary_to_volume"]) for row in group),
                    "mean_gate_beta1": mean_defined(safe_float(row["mean_gate_beta1"]) for row in group),
                    "mean_abs_delta_spectral_radius_rel_tail": mean_defined(safe_float(row["mean_abs_delta_spectral_radius_rel_tail"]) for row in group),
                    "mean_abs_delta_beta1_rel_tail": mean_defined(safe_float(row["mean_abs_delta_beta1_rel_tail"]) for row in group),
                    "mean_abs_delta_dim_proxy_rel_tail": mean_defined(safe_float(row["mean_abs_delta_dim_proxy_rel_tail"]) for row in group),
                }
            )
    return out


def compare_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by = {str(row["profile_label"]): dict(row) for row in aggregate}
    keys = [
        "established_far_shell_rate",
        "mean_pre_horizon_peak_shell23_share",
        "mean_gate_release_after_peak",
        "mean_outer_after_gate_gain",
        "mean_opposite_shell23_outer_motion_rate",
        "mean_gate_boundary_to_volume",
        "mean_abs_delta_spectral_radius_rel_tail",
        "mean_abs_delta_beta1_rel_tail",
    ]
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        p0 = by[f"{perturbation}_p0"]
        p2 = by[f"{perturbation}_p2"]
        row: Dict[str, Any] = {"compare_label": f"{perturbation}_p2_minus_p0"}
        for key in keys:
            row[f"{key}_gap"] = safe_float(p2[key]) - safe_float(p0[key])
        out.append(row)
    add2 = by["add_chord_p2"]
    swap2 = by["local_swap_p2"]
    row = {"compare_label": "local_swap_p2_minus_add_chord_p2"}
    for key in keys:
        row[f"{key}_gap"] = safe_float(swap2[key]) - safe_float(add2[key])
    out.append(row)
    return out


def p2_gate_score(row: Mapping[str, Any]) -> int:
    score = 0
    if safe_float(row["established_far_shell_rate_gap"]) >= 0.25:
        score += 1
    if safe_float(row["mean_pre_horizon_peak_shell23_share_gap"]) >= 0.04:
        score += 1
    if safe_float(row["mean_gate_release_after_peak_gap"]) >= 0.03:
        score += 1
    if safe_float(row["mean_outer_after_gate_gain_gap"]) >= 0.05:
        score += 1
    if safe_float(row["mean_opposite_shell23_outer_motion_rate_gap"]) >= 0.05:
        score += 1
    return score


def global_budget_score(row: Mapping[str, Any]) -> int:
    score = 0
    if safe_float(row["mean_outer_after_gate_gain_gap"]) >= 0.05:
        score += 1
    if safe_float(row["mean_opposite_shell23_outer_motion_rate_gap"]) >= 0.05:
        score += 1
    if safe_float(row["mean_abs_delta_spectral_radius_rel_tail_gap"]) <= 0.003:
        score += 1
    if safe_float(row["mean_abs_delta_beta1_rel_tail_gap"]) <= 0.010:
        score += 1
    return score


def diagnosis_rows(
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    compares: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    by_compare = {str(row["compare_label"]): row for row in compares}
    add_gate = p2_gate_score(by_compare["add_chord_p2_minus_p0"])
    swap_gate = p2_gate_score(by_compare["local_swap_p2_minus_p0"])
    add_budget = global_budget_score(by_compare["add_chord_p2_minus_p0"])
    swap_budget = global_budget_score(by_compare["local_swap_p2_minus_p0"])

    if add_gate >= 4 and swap_gate >= 4:
        gate_status = "shared_p2_inner_gate_candidate"
        gate_note = f"Begge carrierne viser p2-gate/horizon-kobling (scores add={add_gate}/5, swap={swap_gate}/5)."
    elif add_gate >= 3 or swap_gate >= 3:
        gate_status = "inner_gate_weak_or_carrier_split"
        gate_note = f"Indre gate-observabler peker bare delvis mot p2 (scores add={add_gate}/5, swap={swap_gate}/5)."
    else:
        gate_status = "inner_gate_not_yet"
        gate_note = f"Shell2/3-gate skiller ikke p2 fra p0 rent (scores add={add_gate}/5, swap={swap_gate}/5)."

    if add_budget >= 3 and swap_budget >= 3:
        budget_status = "global_budget_coupling_candidate"
        budget_note = f"P2 viser mer shell-redistribusjon uten tilsvarende sterkere global drift i begge carrierne (scores add={add_budget}/4, swap={swap_budget}/4)."
        next_step = "holdout_inner_gate_budget"
        next_note = "Neste steg bor holde ut inner-gate/global-budget-koblingen paa friske seeds."
    elif add_budget >= 3 or swap_budget >= 3:
        budget_status = "global_budget_coupling_weak_or_carrier_split"
        budget_note = f"Budget-koblingen er interessant, men carrier-splittet eller for svak (scores add={add_budget}/4, swap={swap_budget}/4)."
        next_step = "mechanism_axis_still_open"
        next_note = "Neste steg bor enten skjerpe gate-observabelen eller teste en annen indre mekanismeakse."
    else:
        budget_status = "global_budget_coupling_not_yet"
        budget_note = f"Det finnes ikke nok evidens for at p2-horisonten er global-budget-koblet i denne observabelen (scores add={add_budget}/4, swap={swap_budget}/4)."
        next_step = "try_local_trigger_or_scale_holdout"
        next_note = "Neste steg bor ikke oppgradere globale invarianter; prov en ren lokal trigger eller hold p2-horisonten ut paa ny skala."

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
        {"diagnostic_family": "shared_p2_inner_gate", "status": gate_status, "note": gate_note},
        {"diagnostic_family": "global_budget_coupling", "status": budget_status, "note": budget_note},
        {"diagnostic_family": "next_step", "status": next_step, "note": next_note},
    ]


def build_report(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    compares: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cl: target-768 inner gate / global budget lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om p2-horisonten ved target 768 er koblet til en indre shell2/3-gate og global budget-lignende redistribusjon.")
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
    lines.append("## Aggregate inner gate / budget")
    lines.append("")
    lines.append("| profile | horizon | pre gate peak | gate release | outer gain | opposite motion | spectral drift | beta1 drift |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {fmt(row['established_far_shell_rate'])} | {fmt(row['mean_pre_horizon_peak_shell23_share'])} | {fmt(row['mean_gate_release_after_peak'])} | {fmt(row['mean_outer_after_gate_gain'])} | {fmt(row['mean_opposite_shell23_outer_motion_rate'])} | {fmt(row['mean_abs_delta_spectral_radius_rel_tail'])} | {fmt(row['mean_abs_delta_beta1_rel_tail'])} |"
        )
    lines.append("")
    lines.append("## P2 versus P0")
    lines.append("")
    lines.append("| compare | horizon gap | pre gate gap | release gap | outer gain gap | opposite motion gap | spectral drift gap | beta1 drift gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares[:2]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['established_far_shell_rate_gap'])} | {fmt(row['mean_pre_horizon_peak_shell23_share_gap'])} | {fmt(row['mean_gate_release_after_peak_gap'])} | {fmt(row['mean_outer_after_gate_gain_gap'])} | {fmt(row['mean_opposite_shell23_outer_motion_rate_gap'])} | {fmt(row['mean_abs_delta_spectral_radius_rel_tail_gap'])} | {fmt(row['mean_abs_delta_beta1_rel_tail_gap'])} |"
        )
    lines.append("")
    lines.append("## Cross-carrier P2 contrast")
    lines.append("")
    lines.append("| compare | horizon gap | pre gate gap | release gap | outer gain gap | opposite motion gap | spectral drift gap | beta1 drift gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares[2:]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['established_far_shell_rate_gap'])} | {fmt(row['mean_pre_horizon_peak_shell23_share_gap'])} | {fmt(row['mean_gate_release_after_peak_gap'])} | {fmt(row['mean_outer_after_gate_gain_gap'])} | {fmt(row['mean_opposite_shell23_outer_motion_rate_gap'])} | {fmt(row['mean_abs_delta_spectral_radius_rel_tail_gap'])} | {fmt(row['mean_abs_delta_beta1_rel_tail_gap'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en smal mekanismeobservabel, ikke et bevis for globale invarianter.")
    lines.append("- Positivt signal betyr bare at p2-horisonten kan vaere koblet til indre redistribusjon under relativt stabile globale budget-metrikker.")
    lines.append("- Negativt signal betyr at globale invariant-spraak ikke bor oppgraderes her; da bor neste steg vaere ren lokal trigger eller ny skala.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15cl", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Les dette som en test av indre gate/global-budget-kobling, ikke som bevis for partikler eller universell geometri.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15cl",
        "",
        "Denne runden tester om den ytre p2-halen ved target 768 starter med en indre omfordeling rundt shell2/shell3.",
        "",
        f"- Inner gate: `{diag['shared_p2_inner_gate']['status']}`.",
        f"- Global budget-kobling: `{diag['global_budget_coupling']['status']}`.",
        "",
        "Dette er fortsatt bare en mekanismetest. Det viser ikke partikler, romtid eller en global bevaringslov.",
        "",
        f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cl target-768 inner gate / global budget lab.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cl_target768_inner_gate_global_budget_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cl_target768_inner_gate_global_budget_runs.csv")
    p.add_argument("--out-snapshot-csv", type=str, default="Documentation/v15cl_target768_inner_gate_global_budget_snapshot_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cl_target768_inner_gate_global_budget_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15cl_target768_inner_gate_global_budget_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cl_target768_inner_gate_global_budget_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cl_target768_inner_gate_global_budget_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cl_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cl.md")
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
                final_drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                info = dict(res["perturbation_info"])
                support = [int(x) for x in info.get("support", [])]
                support_signature = ",".join(str(x) for x in support)
                base_dist = v7.bfs_distances(base_state.g, support)
                fallback = (max(base_dist.values()) + 1) if base_dist else 1
                rows = snapshot_rows_for_run(
                    perturbation=perturbation,
                    placement=placement,
                    seed_delta=seed_delta,
                    run_seed=run_seed,
                    support_signature=support_signature,
                    log_rows=res["log_rows"],
                    damaged_sets=res["damaged_sets"],
                    control_graphs=res["control_graphs"],
                    base_dist=base_dist,
                    fallback=fallback,
                    base_row=base_row,
                )
                snapshot_rows.extend(rows)
                run_rows.append(
                    run_summary(
                        perturbation=perturbation,
                        placement=placement,
                        seed_delta=seed_delta,
                        run_seed=run_seed,
                        requested_match=int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
                        support_signature=support_signature,
                        recurrence=recurrence,
                        final_drift=final_drift,
                        rows=rows,
                    )
                )

    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    aggregate = aggregate_rows(run_rows)
    compares = compare_rows(aggregate)
    diagnosis = diagnosis_rows(target_summary, run_rows, compares)

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
