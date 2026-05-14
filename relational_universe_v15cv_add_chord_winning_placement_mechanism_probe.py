#!/usr/bin/env python3
"""v0.15cv add_chord winning-placement mechanism probe.

v15cu made p0/p2 labels the wrong primary axis. The live signal is now a
placement landscape:

- p1 is strong persistent at both 896 and 1024
- p3 is dead at 896 but dominant at 1024

This lab reruns only the v15cu p1/p3 cases with richer mechanism observables:
support geometry, support topology, and early launch trajectories. It does not
add more label budget and does not claim particles, Lorentz behavior, or global
invariants.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15cg_target768_far_shell_horizon_lab as v15cg
import relational_universe_v15cn_p2_horizon_scale_holdout as v15cn
import relational_universe_v15cs_add_chord_p0_scale_response_holdout as v15cs
import relational_universe_v15ct_response_fingerprint_synthesis as v15ct
import relational_universe_v15cu_add_chord_placement_response_map as v15cu
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGETS = (896, 1024)
PLACEMENTS = (1, 3)
PERTURBATION = "add_chord"
GROWTH_SEED = v15cu.GROWTH_SEED
SEED_DELTAS = v15cu.FRESH_SEED_DELTAS
REFERENCE_TARGET = v15cu.REFERENCE_TARGET
REFERENCE_STEPS = v15cu.REFERENCE_STEPS
LOG_EVERY = v15cu.LOG_EVERY
EARLY_STEP_LIMIT = 640

COMPARE_KEYS = (
    "established_far_shell_rate",
    "mean_high_horizon_span",
    "mean_high_retention_rate",
    "mean_last12_high_rate",
    "early_high_band_rate",
    "mean_first_outer_step",
    "mean_first_high_step",
    "mean_early_outer_share",
    "max_early_outer_share",
    "mean_early_weighted_distance",
    "early_outer_slope",
    "early_distance_slope",
    "mean_early_damage_nodes",
    "max_early_damage_nodes",
    "mean_early_component_count",
    "mean_support_degree",
    "support_ball_3",
    "shell2_over_shell1",
    "ball3_over_ball1",
    "support_pairwise_mean_distance",
    "support_boundary_to_volume",
    "support_internal_edge_count",
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def finite_mean(values: Iterable[float]) -> float:
    vals = [safe_float(x) for x in values]
    vals = [x for x in vals if math.isfinite(x)]
    return sum(vals) / len(vals) if vals else float("nan")


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def profile_label(placement: int) -> str:
    return f"{PERTURBATION}_p{int(placement)}"


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


def horizon_band(*, outer_share: float, weighted_distance: float) -> str:
    if outer_share >= v15cg.HIGH_SHARE_THRESHOLD and weighted_distance >= v15cg.HIGH_DISTANCE_THRESHOLD:
        return "high"
    if outer_share >= v15cg.MID_SHARE_THRESHOLD and weighted_distance >= v15cg.MID_DISTANCE_THRESHOLD:
        return "mid"
    return "low"


def linear_slope(rows: Sequence[Mapping[str, Any]], key: str) -> float:
    pts = [(safe_float(row["step"]), safe_float(row[key])) for row in rows]
    pts = [(x, y) for x, y in pts if math.isfinite(x) and math.isfinite(y)]
    if len(pts) < 2:
        return float("nan")
    slope, _ = v7.linear_fit([x for x, _ in pts], [y for _, y in pts])
    return slope


def first_step_where(rows: Sequence[Mapping[str, Any]], predicate: Any) -> float:
    for row in rows:
        if predicate(row):
            return safe_float(row["step"])
    return float("nan")


def pairwise_support_distances(base_state: Any, support: Sequence[int]) -> List[int]:
    out: List[int] = []
    nodes = [int(x) for x in support]
    for idx, a in enumerate(nodes):
        dist = v7.bfs_distances(base_state.g, [a])
        for b in nodes[idx + 1:]:
            if b in dist:
                out.append(int(dist[b]))
    return out


def support_mechanism_features(
    *,
    target: int,
    base_state: Any,
    placement: int,
    seed_delta: int,
    run_seed: int,
    support: Sequence[int],
) -> Dict[str, Any]:
    support_set = {int(x) for x in support}
    geom = v14c.support_geometry_features(base_state, list(support_set))
    sub = v15ae.induced_subgraph(base_state.g, support_set)
    boundary = v15.boundary_edge_count(base_state.g, support_set)
    pair_dists = pairwise_support_distances(base_state, list(support_set))
    return {
        "target_nodes": int(target),
        "growth_seed": GROWTH_SEED,
        "placement": int(placement),
        "profile_label": profile_label(placement),
        "seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "support_signature": ",".join(str(x) for x in support),
        "support_size": safe_float(geom["support_size"]),
        "mean_support_degree": safe_float(geom["mean_support_degree"]),
        "min_support_degree": safe_float(geom["min_support_degree"]),
        "max_support_degree": safe_float(geom["max_support_degree"]),
        "support_ball_1": safe_float(geom["support_ball_1"]),
        "support_ball_2": safe_float(geom["support_ball_2"]),
        "support_ball_3": safe_float(geom["support_ball_3"]),
        "support_shell_1": safe_float(geom["support_shell_1"]),
        "support_shell_2": safe_float(geom["support_shell_2"]),
        "support_shell_3": safe_float(geom["support_shell_3"]),
        "shell2_over_shell1": safe_float(geom["shell2_over_shell1"]),
        "ball3_over_ball1": safe_float(geom["ball3_over_ball1"]),
        "support_internal_edge_count": int(sub.num_edges()),
        "support_beta1": int(v7.beta1_cycle_rank(sub)),
        "support_boundary_edge_count": int(boundary),
        "support_boundary_to_volume": boundary / max(1, len(support_set)),
        "support_pairwise_min_distance": min(pair_dists) if pair_dists else float("nan"),
        "support_pairwise_mean_distance": mean_defined(float(x) for x in pair_dists),
        "support_pairwise_max_distance": max(pair_dists) if pair_dists else float("nan"),
    }


def snapshot_rows_for_run(
    *,
    target: int,
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
    out: List[Dict[str, Any]] = []
    for idx, row in enumerate(log_rows):
        damaged = set(damaged_sets[idx])
        control_graph = control_graphs[idx]
        counts = shell_counts(damaged, base_dist, fallback)
        total = max(1, len(damaged))
        shell23 = counts["shell2"] + counts["shell3"]
        outer_share = counts["outer"] / total
        weighted_distance = mean_distance(damaged, base_dist, fallback)
        gate_active = {node for node in damaged if int(base_dist.get(node, -999)) in (2, 3)}
        gate_sub = v15ae.induced_subgraph(control_graph, gate_active)
        gate_boundary = v15.boundary_edge_count(control_graph, gate_active)
        out.append(
            {
                "target_nodes": int(target),
                "growth_seed": GROWTH_SEED,
                "profile_label": profile_label(placement),
                "perturbation": PERTURBATION,
                "placement": int(placement),
                "seed_delta": int(seed_delta),
                "run_seed": int(run_seed),
                "support_signature": support_signature,
                "snapshot_index": int(idx),
                "step": int(row["step"]),
                "early_window": int(int(row["step"]) <= EARLY_STEP_LIMIT),
                "damaged_nodes": int(len(damaged)),
                "shell0_nodes": int(counts["shell0"]),
                "shell1_nodes": int(counts["shell1"]),
                "shell2_nodes": int(counts["shell2"]),
                "shell3_nodes": int(counts["shell3"]),
                "shell23_nodes": int(shell23),
                "outer_nodes": int(counts["outer"]),
                "near_support_nodes": int(counts["shell0"] + counts["shell1"]),
                "shell23_share": shell23 / total,
                "shell3_share": counts["shell3"] / total,
                "outer_share": outer_share,
                "near_support_share": (counts["shell0"] + counts["shell1"]) / total,
                "weighted_mean_distance": weighted_distance,
                "radius_control": int(row["radius_control"]),
                "component_count": int(row["damage_component_count"]),
                "largest_component_fraction": safe_float(row["largest_component_fraction"]),
                "boundary_to_volume": safe_float(row["boundary_to_volume"]),
                "gate_beta1": int(v7.beta1_cycle_rank(gate_sub)),
                "gate_component_count": int(len(v15.damaged_components(control_graph, gate_active))),
                "gate_boundary_edge_count": int(gate_boundary),
                "gate_boundary_to_volume": gate_boundary / len(gate_active) if gate_active else float("nan"),
                "horizon_band": horizon_band(outer_share=outer_share, weighted_distance=weighted_distance),
            }
        )
    return out


def horizon_fields(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(rows))))
    tail_rows = list(rows[tail_start:])
    bands = [str(row["horizon_band"]) for row in tail_rows]
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


def trigger_label_for_run(rows: Sequence[Mapping[str, Any]]) -> str:
    first_high = first_step_where(rows, lambda row: str(row["horizon_band"]) == "high")
    first_outer = first_step_where(rows, lambda row: int(row["outer_nodes"]) > 0)
    early = [row for row in rows if int(row["early_window"]) == 1]
    max_outer = max((safe_float(row["outer_share"]) for row in early), default=0.0)
    max_shell23 = max((safe_float(row["shell23_share"]) for row in early), default=0.0)
    max_damage = max((int(row["damaged_nodes"]) for row in early), default=0)
    if math.isfinite(first_high) and first_high <= 128:
        return "immediate_high_launch"
    if math.isfinite(first_high) and first_high <= EARLY_STEP_LIMIT:
        return "early_high_launch"
    if math.isfinite(first_outer) and first_outer <= EARLY_STEP_LIMIT and max_outer >= 0.35:
        return "early_outer_mass_without_high"
    if max_shell23 >= 0.35 and max_damage >= 8:
        return "inner_gate_load_without_outer_horizon"
    return "quiet_or_delayed_launch"


def run_summary_row(
    *,
    target: int,
    placement: int,
    seed_delta: int,
    run_seed: int,
    requested_match: int,
    support_signature: str,
    support_features: Mapping[str, Any],
    recurrence: Mapping[str, Any],
    final_drift: Mapping[str, Any],
    snapshot_rows: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    early = [row for row in snapshot_rows if int(row["early_window"]) == 1]
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(snapshot_rows))))
    tail = list(snapshot_rows[tail_start:])
    horizon = horizon_fields(snapshot_rows)
    return {
        "target_nodes": int(target),
        "growth_seed": GROWTH_SEED,
        "profile_label": profile_label(placement),
        "perturbation": PERTURBATION,
        "placement": int(placement),
        "seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "requested_match": int(requested_match),
        "support_signature": support_signature,
        "step_budget": int(v15cs.scaled_steps_for_target(target)),
        "log_every": int(LOG_EVERY),
        "early_step_limit": int(EARLY_STEP_LIMIT),
        "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
        "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
        "first_shell1_step": first_step_where(snapshot_rows, lambda row: int(row["shell1_nodes"]) > 0),
        "first_shell2_step": first_step_where(snapshot_rows, lambda row: int(row["shell2_nodes"]) > 0),
        "first_shell3_step": first_step_where(snapshot_rows, lambda row: int(row["shell3_nodes"]) > 0),
        "first_outer_step": first_step_where(snapshot_rows, lambda row: int(row["outer_nodes"]) > 0),
        "first_mid_step": first_step_where(snapshot_rows, lambda row: str(row["horizon_band"]) == "mid"),
        "first_high_step": first_step_where(snapshot_rows, lambda row: str(row["horizon_band"]) == "high"),
        "early_high_band_rate": mean_defined(
            1.0 if str(row["horizon_band"]) == "high" else 0.0 for row in early
        ),
        "early_mid_or_high_rate": mean_defined(
            1.0 if str(row["horizon_band"]) in {"mid", "high"} else 0.0 for row in early
        ),
        "mean_early_damage_nodes": mean_defined(safe_float(row["damaged_nodes"]) for row in early),
        "max_early_damage_nodes": max((safe_float(row["damaged_nodes"]) for row in early), default=float("nan")),
        "mean_early_shell23_share": mean_defined(safe_float(row["shell23_share"]) for row in early),
        "max_early_shell23_share": max((safe_float(row["shell23_share"]) for row in early), default=float("nan")),
        "mean_early_outer_share": mean_defined(safe_float(row["outer_share"]) for row in early),
        "max_early_outer_share": max((safe_float(row["outer_share"]) for row in early), default=float("nan")),
        "mean_early_weighted_distance": mean_defined(safe_float(row["weighted_mean_distance"]) for row in early),
        "max_early_weighted_distance": max((safe_float(row["weighted_mean_distance"]) for row in early), default=float("nan")),
        "early_outer_slope": linear_slope(early, "outer_share"),
        "early_distance_slope": linear_slope(early, "weighted_mean_distance"),
        "early_radius_slope": linear_slope(early, "radius_control"),
        "tail_mean_far_shell_share": mean_defined(safe_float(row["outer_share"]) for row in tail),
        "tail_mean_weighted_mean_distance": mean_defined(safe_float(row["weighted_mean_distance"]) for row in tail),
        "mean_early_component_count": mean_defined(safe_float(row["component_count"]) for row in early),
        "max_early_component_count": max((safe_float(row["component_count"]) for row in early), default=float("nan")),
        "mean_early_largest_component_fraction": mean_defined(
            safe_float(row["largest_component_fraction"]) for row in early
        ),
        "mean_early_boundary_to_volume": mean_defined(safe_float(row["boundary_to_volume"]) for row in early),
        "mean_early_gate_beta1": mean_defined(safe_float(row["gate_beta1"]) for row in early),
        "mean_early_gate_boundary_to_volume": mean_defined(
            safe_float(row["gate_boundary_to_volume"]) for row in early
        ),
        "trigger_label": trigger_label_for_run(snapshot_rows),
        "support_size": safe_float(support_features["support_size"]),
        "mean_support_degree": safe_float(support_features["mean_support_degree"]),
        "min_support_degree": safe_float(support_features["min_support_degree"]),
        "max_support_degree": safe_float(support_features["max_support_degree"]),
        "support_ball_1": safe_float(support_features["support_ball_1"]),
        "support_ball_2": safe_float(support_features["support_ball_2"]),
        "support_ball_3": safe_float(support_features["support_ball_3"]),
        "shell2_over_shell1": safe_float(support_features["shell2_over_shell1"]),
        "ball3_over_ball1": safe_float(support_features["ball3_over_ball1"]),
        "support_internal_edge_count": safe_float(support_features["support_internal_edge_count"]),
        "support_boundary_to_volume": safe_float(support_features["support_boundary_to_volume"]),
        "support_pairwise_mean_distance": safe_float(support_features["support_pairwise_mean_distance"]),
        **horizon,
        "final_abs_delta_spectral_radius_rel": safe_float(final_drift["abs_delta_spectral_radius_rel"]),
        "final_abs_delta_beta1_rel": safe_float(final_drift["abs_delta_beta1_rel"]),
        "final_abs_delta_dim_proxy_rel": safe_float(final_drift["abs_delta_dim_proxy_rel"]),
    }


def aggregate_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for target in TARGETS:
        for placement in PLACEMENTS:
            group = [
                row for row in run_rows
                if int(row["target_nodes"]) == int(target) and int(row["placement"]) == int(placement)
            ]
            row: Dict[str, Any] = {
                "target_nodes": int(target),
                "growth_seed": GROWTH_SEED,
                "profile_label": profile_label(placement),
                "perturbation": PERTURBATION,
                "placement": int(placement),
                "n_runs": len(group),
                "seed_deltas": ";".join(str(int(row["seed_delta"])) for row in group),
                "support_signatures": ";".join(sorted({str(row["support_signature"]) for row in group})),
                "step_budget": int(v15cs.scaled_steps_for_target(target)),
                "established_far_shell_rate": mean_defined(
                    1.0 if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon" else 0.0
                    for row in group
                ),
                "no_far_shell_rate": mean_defined(
                    1.0 if str(row["far_shell_horizon_label"]) == "no_far_shell_horizon" else 0.0
                    for row in group
                ),
                "mean_high_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group),
                "mean_high_retention_rate": mean_defined(safe_float(row["high_retention_rate"]) for row in group),
                "mean_last12_high_rate": mean_defined(safe_float(row["last12_high_rate"]) for row in group),
                "mean_far_shell_share": mean_defined(safe_float(row["tail_mean_far_shell_share"]) for row in group),
                "mean_weighted_mean_distance": mean_defined(
                    safe_float(row["tail_mean_weighted_mean_distance"]) for row in group
                ),
                "early_high_band_rate": mean_defined(safe_float(row["early_high_band_rate"]) for row in group),
                "early_mid_or_high_rate": mean_defined(safe_float(row["early_mid_or_high_rate"]) for row in group),
                "mean_first_outer_step": finite_mean(safe_float(row["first_outer_step"]) for row in group),
                "mean_first_high_step": finite_mean(safe_float(row["first_high_step"]) for row in group),
                "mean_early_damage_nodes": mean_defined(safe_float(row["mean_early_damage_nodes"]) for row in group),
                "max_early_damage_nodes": mean_defined(safe_float(row["max_early_damage_nodes"]) for row in group),
                "mean_early_shell23_share": mean_defined(safe_float(row["mean_early_shell23_share"]) for row in group),
                "max_early_shell23_share": mean_defined(safe_float(row["max_early_shell23_share"]) for row in group),
                "mean_early_outer_share": mean_defined(safe_float(row["mean_early_outer_share"]) for row in group),
                "max_early_outer_share": mean_defined(safe_float(row["max_early_outer_share"]) for row in group),
                "mean_early_weighted_distance": mean_defined(
                    safe_float(row["mean_early_weighted_distance"]) for row in group
                ),
                "max_early_weighted_distance": mean_defined(
                    safe_float(row["max_early_weighted_distance"]) for row in group
                ),
                "early_outer_slope": mean_defined(safe_float(row["early_outer_slope"]) for row in group),
                "early_distance_slope": mean_defined(safe_float(row["early_distance_slope"]) for row in group),
                "early_radius_slope": mean_defined(safe_float(row["early_radius_slope"]) for row in group),
                "mean_early_component_count": mean_defined(
                    safe_float(row["mean_early_component_count"]) for row in group
                ),
                "mean_early_largest_component_fraction": mean_defined(
                    safe_float(row["mean_early_largest_component_fraction"]) for row in group
                ),
                "mean_early_boundary_to_volume": mean_defined(
                    safe_float(row["mean_early_boundary_to_volume"]) for row in group
                ),
                "mean_early_gate_beta1": mean_defined(safe_float(row["mean_early_gate_beta1"]) for row in group),
                "mean_support_degree": mean_defined(safe_float(row["mean_support_degree"]) for row in group),
                "support_ball_1": mean_defined(safe_float(row["support_ball_1"]) for row in group),
                "support_ball_2": mean_defined(safe_float(row["support_ball_2"]) for row in group),
                "support_ball_3": mean_defined(safe_float(row["support_ball_3"]) for row in group),
                "shell2_over_shell1": mean_defined(safe_float(row["shell2_over_shell1"]) for row in group),
                "ball3_over_ball1": mean_defined(safe_float(row["ball3_over_ball1"]) for row in group),
                "support_internal_edge_count": mean_defined(
                    safe_float(row["support_internal_edge_count"]) for row in group
                ),
                "support_boundary_to_volume": mean_defined(
                    safe_float(row["support_boundary_to_volume"]) for row in group
                ),
                "support_pairwise_mean_distance": mean_defined(
                    safe_float(row["support_pairwise_mean_distance"]) for row in group
                ),
                "mean_abs_delta_spectral_radius_rel": mean_defined(
                    safe_float(row["final_abs_delta_spectral_radius_rel"]) for row in group
                ),
                "trigger_labels": ";".join(sorted({str(row["trigger_label"]) for row in group})),
            }
            row["response_strength_score"] = v15ct.response_strength_score(row)
            row["response_class"] = v15ct.response_class(row)
            out.append(row)
    return out


def compare_row(label: str, left: Mapping[str, Any], right: Mapping[str, Any]) -> Dict[str, Any]:
    row: Dict[str, Any] = {
        "compare_label": label,
        "left_profile": left["profile_label"],
        "right_profile": right["profile_label"],
        "left_target_nodes": int(left["target_nodes"]),
        "right_target_nodes": int(right["target_nodes"]),
        "left_response_class": left["response_class"],
        "right_response_class": right["response_class"],
    }
    for key in COMPARE_KEYS:
        row[f"{key}_gap"] = safe_float(left[key]) - safe_float(right[key])
    return row


def compare_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by = {(int(row["target_nodes"]), int(row["placement"])): dict(row) for row in aggregate}
    return [
        compare_row("target896_p3_minus_p1", by[(896, 3)], by[(896, 1)]),
        compare_row("target1024_p3_minus_p1", by[(1024, 3)], by[(1024, 1)]),
        compare_row("p1_1024_minus_896", by[(1024, 1)], by[(896, 1)]),
        compare_row("p3_1024_minus_896", by[(1024, 3)], by[(896, 3)]),
    ]


def gap_score(row: Mapping[str, Any], specs: Sequence[Tuple[str, float, str]]) -> int:
    score = 0
    for key, threshold, direction in specs:
        value = safe_float(row.get(f"{key}_gap"))
        if not math.isfinite(value):
            continue
        if direction == "ge" and value >= threshold:
            score += 1
        elif direction == "le" and value <= threshold:
            score += 1
    return score


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    compares: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    by_profile = {(int(row["target_nodes"]), int(row["placement"])): row for row in aggregate}
    by_compare = {str(row["compare_label"]): row for row in compares}

    p1_stable = (
        "persistent_far_shell" in str(by_profile[(896, 1)]["response_class"])
        and "persistent_far_shell" in str(by_profile[(1024, 1)]["response_class"])
    )
    p3_switch = (
        "persistent_far_shell" not in str(by_profile[(896, 3)]["response_class"])
        and "persistent_far_shell" in str(by_profile[(1024, 3)]["response_class"])
    )

    p3_cross = by_compare["p3_1024_minus_896"]
    p3_launch_score = gap_score(
        p3_cross,
        (
            ("early_high_band_rate", 0.25, "ge"),
            ("mean_first_high_step", -128.0, "le"),
            ("mean_early_outer_share", 0.20, "ge"),
            ("max_early_outer_share", 0.20, "ge"),
            ("early_outer_slope", 0.0005, "ge"),
            ("mean_early_weighted_distance", 1.0, "ge"),
        ),
    )
    p3_geometry_score = gap_score(
        p3_cross,
        (
            ("mean_support_degree", 0.25, "ge"),
            ("support_ball_3", 8.0, "ge"),
            ("ball3_over_ball1", 0.50, "ge"),
            ("support_pairwise_mean_distance", 1.0, "ge"),
            ("support_boundary_to_volume", 0.50, "ge"),
        ),
    )

    p1_cross = by_compare["p1_1024_minus_896"]
    p1_launch_shift = gap_score(
        p1_cross,
        (
            ("early_high_band_rate", 0.25, "ge"),
            ("mean_early_outer_share", 0.20, "ge"),
            ("mean_early_weighted_distance", 1.0, "ge"),
        ),
    )

    if p1_stable:
        p1_status = "p1_stable_persistent_bridge"
        p1_note = "p1 er persistent ved baade 896 og 1024 under samme fresh-seed scope."
    else:
        p1_status = "p1_not_stable"
        p1_note = "p1 holder ikke persistent response ved begge target i denne mekanismeproben."

    if p3_switch:
        p3_status = "p3_target_switch_confirmed"
        p3_note = "p3 er ikke persistent ved 896, men er persistent ved 1024."
    else:
        p3_status = "p3_switch_not_confirmed"
        p3_note = "p3 viser ikke den forventede target-spesifikke switchen i denne proben."

    if p3_launch_score >= 4:
        launch_status = "early_launch_explains_p3_switch_candidate"
        launch_note = f"Tidlig launch skiller p3 1024 fra p3 896 med score {p3_launch_score}/6."
    elif p3_launch_score >= 2:
        launch_status = "early_launch_partial_for_p3_switch"
        launch_note = f"Tidlig launch peker delvis mot p3-switchen med score {p3_launch_score}/6."
    else:
        launch_status = "early_launch_not_sufficient"
        launch_note = f"Tidlig launch forklarer ikke p3-switchen rent (score {p3_launch_score}/6)."

    if p3_geometry_score >= 3:
        geometry_status = "support_geometry_explains_p3_switch_candidate"
        geometry_note = f"Static support geometry skiller p3 1024 fra p3 896 med score {p3_geometry_score}/5."
    elif p3_geometry_score >= 2:
        geometry_status = "support_geometry_partial_for_p3_switch"
        geometry_note = f"Static support geometry peker delvis mot p3-switchen med score {p3_geometry_score}/5."
    else:
        geometry_status = "support_geometry_not_sufficient"
        geometry_note = f"Static support geometry forklarer ikke p3-switchen rent (score {p3_geometry_score}/5)."

    if p1_stable and p3_switch and (p3_launch_score >= 2 or p3_geometry_score >= 2):
        next_step = "holdout_p1_p3_mechanism_axis"
        next_note = (
            "Neste steg bor holde ut p1/p3-mekanismeaksen paa nye seed-deltaer, med samme tidlig-launch og supportgeometri."
        )
    elif p1_stable and p3_switch:
        next_step = "add_genealogy_to_p1_p3_seed_splits"
        next_note = (
            "P1/p3-landskapet holder, men mekanismen er ikke forklart; neste steg bor legge til per-run genealogi."
        )
    else:
        next_step = "retire_winning_placement_mechanism_probe"
        next_note = "Mekanismeproben reproduserer ikke nok av v15cu-landskapet til aa fortsette denne aksen."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelser er rene og alle requested add_chord-perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Enten startstorrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        },
        {"diagnostic_family": "p1_bridge", "status": p1_status, "note": p1_note},
        {"diagnostic_family": "p3_switch", "status": p3_status, "note": p3_note},
        {"diagnostic_family": "early_launch_axis", "status": launch_status, "note": launch_note},
        {"diagnostic_family": "support_geometry_axis", "status": geometry_status, "note": geometry_note},
        {
            "diagnostic_family": "p1_target_shift",
            "status": "p1_launch_changes_across_target" if p1_launch_shift >= 2 else "p1_launch_relatively_stable",
            "note": f"p1 1024-minus-896 early-launch shift score er {p1_launch_shift}/3.",
        },
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
    lines.append("# Relasjonell universgraf v0.15cv: add_chord winning-placement mechanism probe")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden rerunner bare v15cu sine p1/p3-cases med rikere mekanismeobservabler.")
    lines.append("Maalet er aa se om target-switchen kan knyttes til supportgeometri og tidlig launch, ikke aa score flere labels.")
    lines.append("")
    lines.append("## Design")
    lines.append("")
    lines.append("| field | value |")
    lines.append("| --- | --- |")
    lines.append(f"| targets | {';'.join(str(x) for x in TARGETS)} |")
    lines.append(f"| placements | {';'.join('p' + str(x) for x in PLACEMENTS)} |")
    lines.append(f"| seed deltas | {';'.join(str(x) for x in SEED_DELTAS)} |")
    lines.append(f"| early step limit | {EARLY_STEP_LIMIT} |")
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
    lines.append("## Aggregate mechanism")
    lines.append("")
    lines.append("| target | placement | class | est | horizon | early high | first high | early outer | early distance | support ball3 | ball3/ball1 | trigger labels |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['target_nodes'])} | p{int(row['placement'])} | {row['response_class']} | {fmt(row['established_far_shell_rate'])} | {fmt(row['mean_high_horizon_span'])} | {fmt(row['early_high_band_rate'])} | {fmt(row['mean_first_high_step'],1)} | {fmt(row['mean_early_outer_share'])} | {fmt(row['mean_early_weighted_distance'])} | {fmt(row['support_ball_3'],1)} | {fmt(row['ball3_over_ball1'])} | {row['trigger_labels']} |"
        )
    lines.append("")
    lines.append("## Contrasts")
    lines.append("")
    lines.append("| compare | horizon gap | early high gap | first high gap | early outer gap | distance gap | ball3 gap | ball3/ball1 gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['mean_high_horizon_span_gap'])} | {fmt(row['early_high_band_rate_gap'])} | {fmt(row['mean_first_high_step_gap'],1)} | {fmt(row['mean_early_outer_share_gap'])} | {fmt(row['mean_early_weighted_distance_gap'])} | {fmt(row['support_ball_3_gap'],1)} | {fmt(row['ball3_over_ball1_gap'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- P1/p3 er fortsatt heuristiske placement-profiler, ikke partikler.")
    lines.append("- En mekanismeakse her betyr bare at support/launch-observabler kan forklare noe av placement-landskapet.")
    lines.append("- Hvis mekanismen holder, neste steg er holdout. Hvis ikke, maa vi til genealogi/per-run seed-splits.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15cv", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Dette er en mekanismeprobe for add_chord-placement-landskapet, ikke en global invariant- eller Lorentz-test.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15cv",
        "",
        "Denne runden spor hvorfor bestemte add_chord-plasseringer svarer sterkt.",
        "",
        f"- P1-bro: `{diag['p1_bridge']['status']}`.",
        f"- P3-switch: `{diag['p3_switch']['status']}`.",
        f"- Tidlig launch: `{diag['early_launch_axis']['status']}`.",
        f"- Supportgeometri: `{diag['support_geometry_axis']['status']}`.",
        "",
        "Hvis dette holder, har vi en bedre forklaring enn navnelapper som p0 og p2. Det er fortsatt ikke bevis for partikler eller romtid.",
        "",
        f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cv add_chord winning-placement mechanism probe.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cv_add_chord_winning_placement_target_summary.csv")
    p.add_argument("--out-support-csv", type=str, default="Documentation/v15cv_add_chord_winning_placement_support_geometry.csv")
    p.add_argument("--out-snapshot-csv", type=str, default="Documentation/v15cv_add_chord_winning_placement_snapshot_rows.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cv_add_chord_winning_placement_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cv_add_chord_winning_placement_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15cv_add_chord_winning_placement_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cv_add_chord_winning_placement_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cv_add_chord_winning_placement_mechanism_probe.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cv_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cv.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles(list(TARGETS))
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    by_target_state = {ens.target_nodes: base_states[(ens.name, GROWTH_SEED)] for ens in ensembles}
    by_target_row = {
        int(row["target_nodes"]): row
        for row in base_rows
        if int(row["growth_seed"]) == GROWTH_SEED and int(row["target_nodes"]) in TARGETS
    }
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    support_rows: List[Dict[str, Any]] = []
    snapshot_rows: List[Dict[str, Any]] = []
    run_rows: List[Dict[str, Any]] = []

    for target in TARGETS:
        base_state = by_target_state[int(target)]
        base_row = by_target_row[int(target)]
        for placement in PLACEMENTS:
            for seed_delta in SEED_DELTAS:
                run_seed = v15cn.run_seed_for(
                    target=target,
                    perturbation=PERTURBATION,
                    placement=placement,
                    seed_delta=seed_delta,
                )
                res = v15ae.run_defect_with_control_graphs(
                    base_state,
                    params=params,
                    seed=run_seed,
                    steps=v15cs.scaled_steps_for_target(target),
                    perturbation=PERTURBATION,
                    center_token_index=placement,
                    local_coupling="maximal",
                    log_every=LOG_EVERY,
                )
                info = dict(res["perturbation_info"])
                support = [int(x) for x in info.get("support", [])]
                support_signature = ",".join(str(x) for x in support)
                support_features = support_mechanism_features(
                    target=target,
                    base_state=base_state,
                    placement=placement,
                    seed_delta=seed_delta,
                    run_seed=run_seed,
                    support=support,
                )
                support_rows.append(support_features)
                base_dist = v7.bfs_distances(base_state.g, support)
                fallback = (max(base_dist.values()) + 1) if base_dist else 1
                rows = snapshot_rows_for_run(
                    target=target,
                    placement=placement,
                    seed_delta=seed_delta,
                    run_seed=run_seed,
                    support_signature=support_signature,
                    log_rows=res["log_rows"],
                    damaged_sets=res["damaged_sets"],
                    control_graphs=res["control_graphs"],
                    base_dist=base_dist,
                    fallback=fallback,
                )
                snapshot_rows.extend(rows)
                recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
                final_drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                run_rows.append(
                    run_summary_row(
                        target=target,
                        placement=placement,
                        seed_delta=seed_delta,
                        run_seed=run_seed,
                        requested_match=int(v15.v14.perturbation_requested_match(PERTURBATION, str(info.get("type", "unknown")))),
                        support_signature=support_signature,
                        support_features=support_features,
                        recurrence=recurrence,
                        final_drift=final_drift,
                        snapshot_rows=rows,
                    )
                )

    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) in TARGETS]
    aggregate = aggregate_rows(run_rows)
    compares = compare_rows(aggregate)
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        aggregate=aggregate,
        compares=compares,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_support_csv, support_rows)
    write_csv(args.out_snapshot_csv, snapshot_rows)
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
