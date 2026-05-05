#!/usr/bin/env python3
"""v0.15ci target-768 p2 horizon genealogy mechanism lab.

v15ch established that the target-768 p2 horizon is not just a local_swap-only
cutoff artifact. The next narrow question is mechanistic:

is the shared p2 horizon carried by a persistent outer branch, or is it rebuilt
repeatedly through outer-shell reseeding?

This round keeps the scope tight:

- target 768 only
- growth_seed 202 only
- placements 0 and 2 only
- add_chord and local_swap only
- fixed shell4+ outer definition
- fresh run seeds
"""
from __future__ import annotations

import argparse
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Set, Tuple

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
SEED_DELTAS = (3907, 3943, 3991, 4049)
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
    perturbation_offset = {"add_chord": 1411, "local_swap": 1483}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def induced_subgraph(g: v7.UGraph, nodes: Set[int]) -> v7.UGraph:
    sub = v7.UGraph()
    for node in sorted(nodes):
        if node in g.adj:
            sub.add_node(node)
    for a in sorted(nodes):
        if a not in g.adj:
            continue
        for b in g.neighbors(a):
            if b in nodes and a < b:
                sub.add_edge(a, b)
    return sub


def component_boundary_edge_count(g: v7.UGraph, component: Set[int]) -> int:
    count = 0
    for node in component:
        if node not in g.adj:
            continue
        for other in g.neighbors(node):
            if other not in component:
                count += 1
    return count


def serialize_ids(ids: Sequence[int]) -> str:
    return ",".join(str(int(x)) for x in ids)


def support_distance_metrics(base_dist: Mapping[int, int], fallback: int, component: Set[int]) -> Dict[str, float]:
    values = [float(base_dist.get(node, fallback)) for node in component]
    if not values:
        return {
            "min_support_distance": float("nan"),
            "max_support_distance": float("nan"),
            "mean_support_distance": float("nan"),
        }
    return {
        "min_support_distance": min(values),
        "max_support_distance": max(values),
        "mean_support_distance": mean_defined(values),
    }


def overlap_stats(a_nodes: Set[int], b_nodes: Set[int]) -> Tuple[int, float]:
    inter = len(a_nodes.intersection(b_nodes))
    if inter <= 0:
        return 0, 0.0
    union = len(a_nodes.union(b_nodes))
    return inter, (inter / union) if union > 0 else 0.0


def choose_dominant(candidates: Sequence[int], score_lookup: Mapping[int, Tuple[int, float]]) -> int:
    return max(candidates, key=lambda idx: (score_lookup[idx][0], score_lookup[idx][1], -idx))


def tail_snapshot_components(
    *,
    snapshot_index: int,
    step: int,
    damaged: Set[int],
    control_graph: v7.UGraph,
    base_dist: Mapping[int, int],
    fallback: int,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    outer_nodes = {
        node
        for node in damaged
        if int(base_dist.get(node, fallback)) >= OUTER_DISTANCE_FLOOR
    }
    dists = [int(base_dist.get(node, fallback)) for node in outer_nodes]
    comps = v15.damaged_components(control_graph, outer_nodes)
    comps.sort(key=lambda comp: (min(comp) if comp else -1, len(comp)))
    outer_mass = len(outer_nodes)
    largest = max((len(comp) for comp in comps), default=0)
    summary = {
        "snapshot_index": int(snapshot_index),
        "step": int(step),
        "outer_active": 1 if outer_mass > 0 else 0,
        "outer_mass": int(outer_mass),
        "outer_share_of_damage": (outer_mass / max(1, len(damaged))) if damaged else 0.0,
        "component_count": int(len(comps)),
        "largest_component_fraction": (largest / outer_mass) if outer_mass > 0 else 0.0,
        "mean_outer_distance": mean_defined(dists) if dists else float("nan"),
    }
    rows: List[Dict[str, Any]] = []
    for local_idx, comp in enumerate(comps):
        sub = induced_subgraph(control_graph, comp)
        boundary = component_boundary_edge_count(control_graph, comp)
        rows.append(
            {
                "snapshot_index": int(snapshot_index),
                "step": int(step),
                "component_local_index": int(local_idx),
                "nodes": set(comp),
                "size_nodes": int(len(comp)),
                "size_fraction": (len(comp) / outer_mass) if outer_mass > 0 else 0.0,
                "internal_edge_count": int(sub.num_edges()),
                "beta1_local": int(v7.beta1_cycle_rank(sub)),
                "boundary_edge_count": int(boundary),
                "boundary_to_volume": (boundary / len(comp)) if comp else 0.0,
                **support_distance_metrics(base_dist, fallback, comp),
            }
        )
    return summary, rows


def build_tail_genealogy(
    *,
    perturbation: str,
    placement: int,
    growth_seed: int,
    seed_delta: int,
    run_seed: int,
    tail_log_rows: Sequence[Mapping[str, Any]],
    tail_damaged_sets: Sequence[Set[int]],
    tail_control_graphs: Sequence[v7.UGraph],
    base_dist: Mapping[int, int],
    fallback: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    snapshots: List[Dict[str, Any]] = []
    for idx, log_row in enumerate(tail_log_rows):
        summary, comps = tail_snapshot_components(
            snapshot_index=idx,
            step=int(log_row["step"]),
            damaged=set(tail_damaged_sets[idx]),
            control_graph=tail_control_graphs[idx],
            base_dist=base_dist,
            fallback=fallback,
        )
        snapshots.append({"summary": summary, "components": comps})

    component_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []
    next_component_id = 1

    def emit_component_rows(snapshot_summary: Mapping[str, Any], comps: Sequence[Mapping[str, Any]]) -> None:
        for comp in comps:
            component_rows.append(
                {
                    "profile_label": f"{perturbation}_p{int(placement)}",
                    "perturbation": perturbation,
                    "placement": int(placement),
                    "growth_seed": int(growth_seed),
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "snapshot_index": int(snapshot_summary["snapshot_index"]),
                    "step": int(snapshot_summary["step"]),
                    "component_local_index": int(comp["component_local_index"]),
                    "component_id": int(comp["component_id"]),
                    "parent_ids": serialize_ids(comp.get("parent_ids", [])),
                    "size_nodes": int(comp["size_nodes"]),
                    "size_fraction": safe_float(comp["size_fraction"]),
                    "internal_edge_count": int(comp["internal_edge_count"]),
                    "beta1_local": int(comp["beta1_local"]),
                    "boundary_edge_count": int(comp["boundary_edge_count"]),
                    "boundary_to_volume": safe_float(comp["boundary_to_volume"]),
                    "min_support_distance": safe_float(comp["min_support_distance"]),
                    "max_support_distance": safe_float(comp["max_support_distance"]),
                    "mean_support_distance": safe_float(comp["mean_support_distance"]),
                    "outer_mass": int(snapshot_summary["outer_mass"]),
                    "outer_share_of_damage": safe_float(snapshot_summary["outer_share_of_damage"]),
                    "component_count": int(snapshot_summary["component_count"]),
                    "largest_component_fraction": safe_float(snapshot_summary["largest_component_fraction"]),
                }
            )

    if snapshots:
        first_summary = snapshots[0]["summary"]
        for comp in snapshots[0]["components"]:
            comp["component_id"] = next_component_id
            comp["parent_ids"] = []
            next_component_id += 1
        emit_component_rows(first_summary, snapshots[0]["components"])

    for snap_idx in range(1, len(snapshots)):
        prev_snapshot = snapshots[snap_idx - 1]
        curr_snapshot = snapshots[snap_idx]
        prev_comps = prev_snapshot["components"]
        curr_comps = curr_snapshot["components"]

        parent_children: Dict[int, List[int]] = {idx: [] for idx in range(len(prev_comps))}
        child_parents: Dict[int, List[int]] = {idx: [] for idx in range(len(curr_comps))}
        scores: Dict[Tuple[int, int], Tuple[int, float]] = {}

        for p_idx, prev_comp in enumerate(prev_comps):
            for c_idx, curr_comp in enumerate(curr_comps):
                inter, jac = overlap_stats(set(prev_comp["nodes"]), set(curr_comp["nodes"]))
                if inter <= 0:
                    continue
                parent_children[p_idx].append(c_idx)
                child_parents[c_idx].append(p_idx)
                scores[(p_idx, c_idx)] = (inter, jac)

        dominant_child: Dict[int, int] = {}
        for p_idx, child_ids in parent_children.items():
            if child_ids:
                dominant_child[p_idx] = choose_dominant(child_ids, {c_idx: scores[(p_idx, c_idx)] for c_idx in child_ids})

        dominant_parent: Dict[int, int] = {}
        for c_idx, parent_ids in child_parents.items():
            if parent_ids:
                dominant_parent[c_idx] = choose_dominant(parent_ids, {p_idx: scores[(p_idx, c_idx)] for p_idx in parent_ids})

        for c_idx, curr_comp in enumerate(curr_comps):
            parents = child_parents.get(c_idx, [])
            curr_comp["parent_ids"] = sorted(int(prev_comps[p]["component_id"]) for p in parents)
            if not parents:
                curr_comp["component_id"] = next_component_id
                next_component_id += 1
            elif len(parents) == 1 and len(parent_children[parents[0]]) == 1:
                curr_comp["component_id"] = int(prev_comps[parents[0]]["component_id"])
            elif len(parents) == 1 and len(parent_children[parents[0]]) > 1:
                if dominant_child.get(parents[0]) == c_idx:
                    curr_comp["component_id"] = int(prev_comps[parents[0]]["component_id"])
                else:
                    curr_comp["component_id"] = next_component_id
                    next_component_id += 1
            else:
                curr_comp["component_id"] = int(prev_comps[dominant_parent[c_idx]]["component_id"])

        prev_summary = prev_snapshot["summary"]
        curr_summary = curr_snapshot["summary"]

        for p_idx, children in parent_children.items():
            parent_id = int(prev_comps[p_idx]["component_id"])
            if not children:
                event_rows.append(
                    {
                        "profile_label": f"{perturbation}_p{int(placement)}",
                        "perturbation": perturbation,
                        "placement": int(placement),
                        "growth_seed": int(growth_seed),
                        "seed_delta": int(seed_delta),
                        "run_seed": int(run_seed),
                        "snapshot_index_from": int(prev_summary["snapshot_index"]),
                        "snapshot_index_to": int(curr_summary["snapshot_index"]),
                        "step_from": int(prev_summary["step"]),
                        "step_to": int(curr_summary["step"]),
                        "event_type": "death",
                        "parent_ids": str(parent_id),
                        "child_ids": "",
                        "parent_count": 1,
                        "child_count": 0,
                        "component_count_before": int(prev_summary["component_count"]),
                        "component_count_after": int(curr_summary["component_count"]),
                        "outer_mass_before": int(prev_summary["outer_mass"]),
                        "outer_mass_after": int(curr_summary["outer_mass"]),
                    }
                )
            elif len(children) == 1 and len(child_parents.get(children[0], [])) == 1:
                child_id = int(curr_comps[children[0]]["component_id"])
                event_rows.append(
                    {
                        "profile_label": f"{perturbation}_p{int(placement)}",
                        "perturbation": perturbation,
                        "placement": int(placement),
                        "growth_seed": int(growth_seed),
                        "seed_delta": int(seed_delta),
                        "run_seed": int(run_seed),
                        "snapshot_index_from": int(prev_summary["snapshot_index"]),
                        "snapshot_index_to": int(curr_summary["snapshot_index"]),
                        "step_from": int(prev_summary["step"]),
                        "step_to": int(curr_summary["step"]),
                        "event_type": "persist",
                        "parent_ids": str(parent_id),
                        "child_ids": str(child_id),
                        "parent_count": 1,
                        "child_count": 1,
                        "component_count_before": int(prev_summary["component_count"]),
                        "component_count_after": int(curr_summary["component_count"]),
                        "outer_mass_before": int(prev_summary["outer_mass"]),
                        "outer_mass_after": int(curr_summary["outer_mass"]),
                    }
                )
            elif len(children) > 1:
                child_ids = [int(curr_comps[idx]["component_id"]) for idx in children]
                event_rows.append(
                    {
                        "profile_label": f"{perturbation}_p{int(placement)}",
                        "perturbation": perturbation,
                        "placement": int(placement),
                        "growth_seed": int(growth_seed),
                        "seed_delta": int(seed_delta),
                        "run_seed": int(run_seed),
                        "snapshot_index_from": int(prev_summary["snapshot_index"]),
                        "snapshot_index_to": int(curr_summary["snapshot_index"]),
                        "step_from": int(prev_summary["step"]),
                        "step_to": int(curr_summary["step"]),
                        "event_type": "split",
                        "parent_ids": str(parent_id),
                        "child_ids": serialize_ids(child_ids),
                        "parent_count": 1,
                        "child_count": len(children),
                        "component_count_before": int(prev_summary["component_count"]),
                        "component_count_after": int(curr_summary["component_count"]),
                        "outer_mass_before": int(prev_summary["outer_mass"]),
                        "outer_mass_after": int(curr_summary["outer_mass"]),
                    }
                )

        for c_idx, parents in child_parents.items():
            child_id = int(curr_comps[c_idx]["component_id"])
            if not parents:
                event_rows.append(
                    {
                        "profile_label": f"{perturbation}_p{int(placement)}",
                        "perturbation": perturbation,
                        "placement": int(placement),
                        "growth_seed": int(growth_seed),
                        "seed_delta": int(seed_delta),
                        "run_seed": int(run_seed),
                        "snapshot_index_from": int(prev_summary["snapshot_index"]),
                        "snapshot_index_to": int(curr_summary["snapshot_index"]),
                        "step_from": int(prev_summary["step"]),
                        "step_to": int(curr_summary["step"]),
                        "event_type": "birth",
                        "parent_ids": "",
                        "child_ids": str(child_id),
                        "parent_count": 0,
                        "child_count": 1,
                        "component_count_before": int(prev_summary["component_count"]),
                        "component_count_after": int(curr_summary["component_count"]),
                        "outer_mass_before": int(prev_summary["outer_mass"]),
                        "outer_mass_after": int(curr_summary["outer_mass"]),
                    }
                )
            elif len(parents) > 1:
                parent_ids = [int(prev_comps[p]["component_id"]) for p in parents]
                event_rows.append(
                    {
                        "profile_label": f"{perturbation}_p{int(placement)}",
                        "perturbation": perturbation,
                        "placement": int(placement),
                        "growth_seed": int(growth_seed),
                        "seed_delta": int(seed_delta),
                        "run_seed": int(run_seed),
                        "snapshot_index_from": int(prev_summary["snapshot_index"]),
                        "snapshot_index_to": int(curr_summary["snapshot_index"]),
                        "step_from": int(prev_summary["step"]),
                        "step_to": int(curr_summary["step"]),
                        "event_type": "merge",
                        "parent_ids": serialize_ids(parent_ids),
                        "child_ids": str(child_id),
                        "parent_count": len(parents),
                        "child_count": 1,
                        "component_count_before": int(prev_summary["component_count"]),
                        "component_count_after": int(curr_summary["component_count"]),
                        "outer_mass_before": int(prev_summary["outer_mass"]),
                        "outer_mass_after": int(curr_summary["outer_mass"]),
                    }
                )

        emit_component_rows(curr_summary, curr_comps)

    snapshots_meta = [snap["summary"] for snap in snapshots]
    return snapshots_meta, component_rows, event_rows


def longest_active_run(flags: Sequence[int]) -> int:
    best = 0
    current = 0
    for flag in flags:
        if int(flag) == 1:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def classify_mechanism(
    *,
    active_rate: float,
    dominant_presence_rate: float,
    dominant_mass_share: float,
    turnover_rate: float,
    lateborn_mass_share: float,
    reactivation_count: int,
) -> str:
    if active_rate < 0.40:
        return "outer_probe_only"
    if (
        active_rate >= 0.60
        and dominant_presence_rate >= 0.70
        and dominant_mass_share >= 0.55
        and turnover_rate <= 0.50
        and lateborn_mass_share <= 0.30
        and reactivation_count <= 1
    ):
        return "persistent_outer_branch"
    if (
        active_rate >= 0.60
        and (
            lateborn_mass_share >= 0.35
            or turnover_rate >= 0.75
            or reactivation_count >= 2
        )
    ):
        return "reseeded_outer_horizon"
    return "mixed_outer_horizon"


def summarize_run(
    *,
    perturbation: str,
    placement: int,
    growth_seed: int,
    seed_delta: int,
    run_seed: int,
    raw_row: Mapping[str, Any],
    tail_snapshots: Sequence[Mapping[str, Any]],
    component_rows: Sequence[Mapping[str, Any]],
    event_rows: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    active_flags = [int(row["outer_active"]) for row in tail_snapshots]
    active_snapshots = sum(active_flags)
    total_snapshots = max(1, len(tail_snapshots))
    active_rate = active_snapshots / total_snapshots
    active_indices = [idx for idx, flag in enumerate(active_flags) if flag == 1]
    first_active_idx = min(active_indices, default=-1)
    reactivation_count = 0
    if active_indices:
        prev_idx = active_indices[0]
        for idx in active_indices[1:]:
            if idx > prev_idx + 1:
                reactivation_count += 1
            prev_idx = idx

    event_counts = Counter(str(row["event_type"]) for row in event_rows)
    by_component: MutableMapping[int, List[Mapping[str, Any]]] = {}
    for row in component_rows:
        by_component.setdefault(int(row["component_id"]), []).append(row)

    total_mass_over_time = sum(int(row["size_nodes"]) for row in component_rows)
    component_stats: List[Dict[str, Any]] = []
    for component_id, rows in by_component.items():
        ordered = sorted(rows, key=lambda row: (int(row["snapshot_index"]), int(row["step"])))
        component_stats.append(
            {
                "component_id": int(component_id),
                "first_snapshot_index": int(ordered[0]["snapshot_index"]),
                "active_snapshots": len(ordered),
                "mass_over_time": sum(int(row["size_nodes"]) for row in ordered),
            }
        )
    component_stats.sort(
        key=lambda row: (
            int(row["mass_over_time"]),
            int(row["active_snapshots"]),
            -int(row["component_id"]),
        ),
        reverse=True,
    )
    dominant = component_stats[0] if component_stats else None
    dominant_presence_rate = (
        (int(dominant["active_snapshots"]) / max(1, active_snapshots))
        if dominant and active_snapshots > 0
        else 0.0
    )
    dominant_mass_share = (
        (int(dominant["mass_over_time"]) / max(1, total_mass_over_time))
        if dominant and total_mass_over_time > 0
        else 0.0
    )
    lateborn_mass_share = (
        sum(
            int(row["mass_over_time"])
            for row in component_stats
            if first_active_idx >= 0 and int(row["first_snapshot_index"]) > first_active_idx
        )
        / max(1, total_mass_over_time)
        if total_mass_over_time > 0
        else 0.0
    )
    mean_component_count_when_active = mean_defined(
        safe_float(row["component_count"]) for row in tail_snapshots if int(row["outer_active"]) == 1
    )
    mean_outer_mass_when_active = mean_defined(
        safe_float(row["outer_mass"]) for row in tail_snapshots if int(row["outer_active"]) == 1
    )
    turnover_rate = (event_counts.get("birth", 0) + event_counts.get("death", 0)) / max(1, active_snapshots)
    mechanism_label = classify_mechanism(
        active_rate=active_rate,
        dominant_presence_rate=dominant_presence_rate,
        dominant_mass_share=dominant_mass_share,
        turnover_rate=turnover_rate,
        lateborn_mass_share=lateborn_mass_share,
        reactivation_count=reactivation_count,
    )
    return {
        "profile_label": f"{perturbation}_p{int(placement)}",
        "perturbation": perturbation,
        "placement": int(placement),
        "growth_seed": int(growth_seed),
        "seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "requested_match": int(raw_row["requested_match"]),
        "support_signature": str(raw_row["support_signature"]),
        "full_exact_return_rate": safe_float(raw_row["full_exact_return_rate"]),
        "full_coarse_return_rate": safe_float(raw_row["full_coarse_return_rate"]),
        "tail_snapshot_count": int(total_snapshots),
        "outer_active_rate": float(active_rate),
        "longest_active_run_snapshots": int(longest_active_run(active_flags)),
        "reactivation_count": int(reactivation_count),
        "birth_count": int(event_counts.get("birth", 0)),
        "death_count": int(event_counts.get("death", 0)),
        "split_count": int(event_counts.get("split", 0)),
        "merge_count": int(event_counts.get("merge", 0)),
        "turnover_rate": float(turnover_rate),
        "dominant_lineage_presence_rate": float(dominant_presence_rate),
        "dominant_lineage_mass_share": float(dominant_mass_share),
        "lateborn_mass_share": float(lateborn_mass_share),
        "mean_component_count_when_active": mean_component_count_when_active,
        "mean_outer_mass_when_active": mean_outer_mass_when_active,
        "dominant_component_active_snapshots": int(dominant["active_snapshots"]) if dominant else 0,
        "dominant_component_first_snapshot_index": int(dominant["first_snapshot_index"]) if dominant else -1,
        "mechanism_label": mechanism_label,
        "abs_delta_spectral_radius_rel": safe_float(raw_row["abs_delta_spectral_radius_rel"]),
    }


def dominant_mechanism(rows: Sequence[Mapping[str, Any]]) -> str:
    counts = Counter(str(row["mechanism_label"]) for row in rows)
    if not counts:
        return "none"
    return max(counts.items(), key=lambda item: (item[1], item[0]))[0]


def aggregate_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        for placement in PLACEMENTS:
            group = [
                row
                for row in run_rows
                if str(row["perturbation"]) == perturbation and int(row["placement"]) == int(placement)
            ]
            out.append(
                {
                    "profile_label": f"{perturbation}_p{int(placement)}",
                    "perturbation": perturbation,
                    "placement": int(placement),
                    "n_runs": len(group),
                    "persistent_outer_branch_rate": mean_defined(
                        1.0 if str(row["mechanism_label"]) == "persistent_outer_branch" else 0.0 for row in group
                    ),
                    "reseeded_outer_horizon_rate": mean_defined(
                        1.0 if str(row["mechanism_label"]) == "reseeded_outer_horizon" else 0.0 for row in group
                    ),
                    "mixed_outer_horizon_rate": mean_defined(
                        1.0 if str(row["mechanism_label"]) == "mixed_outer_horizon" else 0.0 for row in group
                    ),
                    "outer_probe_only_rate": mean_defined(
                        1.0 if str(row["mechanism_label"]) == "outer_probe_only" else 0.0 for row in group
                    ),
                    "mean_outer_active_rate": mean_defined(safe_float(row["outer_active_rate"]) for row in group),
                    "mean_longest_active_run_snapshots": mean_defined(safe_float(row["longest_active_run_snapshots"]) for row in group),
                    "mean_reactivation_count": mean_defined(safe_float(row["reactivation_count"]) for row in group),
                    "mean_birth_count": mean_defined(safe_float(row["birth_count"]) for row in group),
                    "mean_death_count": mean_defined(safe_float(row["death_count"]) for row in group),
                    "mean_split_count": mean_defined(safe_float(row["split_count"]) for row in group),
                    "mean_merge_count": mean_defined(safe_float(row["merge_count"]) for row in group),
                    "mean_turnover_rate": mean_defined(safe_float(row["turnover_rate"]) for row in group),
                    "mean_dominant_lineage_presence_rate": mean_defined(safe_float(row["dominant_lineage_presence_rate"]) for row in group),
                    "mean_dominant_lineage_mass_share": mean_defined(safe_float(row["dominant_lineage_mass_share"]) for row in group),
                    "mean_lateborn_mass_share": mean_defined(safe_float(row["lateborn_mass_share"]) for row in group),
                    "mean_component_count_when_active": mean_defined(safe_float(row["mean_component_count_when_active"]) for row in group),
                    "mean_outer_mass_when_active": mean_defined(safe_float(row["mean_outer_mass_when_active"]) for row in group),
                    "mean_abs_delta_spectral_radius_rel": mean_defined(safe_float(row["abs_delta_spectral_radius_rel"]) for row in group),
                    "dominant_mechanism_label": dominant_mechanism(group),
                }
            )
    return out


def compare_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_profile = {str(row["profile_label"]): row for row in aggregate}
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        p0 = by_profile[f"{perturbation}_p0"]
        p2 = by_profile[f"{perturbation}_p2"]
        out.append(
            {
                "compare_label": f"{perturbation}_p2_minus_p0",
                "outer_active_gap": safe_float(p2["mean_outer_active_rate"]) - safe_float(p0["mean_outer_active_rate"]),
                "persistent_rate_gap": safe_float(p2["persistent_outer_branch_rate"]) - safe_float(p0["persistent_outer_branch_rate"]),
                "reseeded_rate_gap": safe_float(p2["reseeded_outer_horizon_rate"]) - safe_float(p0["reseeded_outer_horizon_rate"]),
                "dominant_presence_gap": safe_float(p2["mean_dominant_lineage_presence_rate"]) - safe_float(p0["mean_dominant_lineage_presence_rate"]),
                "dominant_mass_gap": safe_float(p2["mean_dominant_lineage_mass_share"]) - safe_float(p0["mean_dominant_lineage_mass_share"]),
                "lateborn_mass_gap": safe_float(p2["mean_lateborn_mass_share"]) - safe_float(p0["mean_lateborn_mass_share"]),
                "turnover_gap": safe_float(p2["mean_turnover_rate"]) - safe_float(p0["mean_turnover_rate"]),
                "reactivation_gap": safe_float(p2["mean_reactivation_count"]) - safe_float(p0["mean_reactivation_count"]),
            }
        )
    add2 = by_profile["add_chord_p2"]
    swap2 = by_profile["local_swap_p2"]
    out.append(
        {
            "compare_label": "local_swap_p2_minus_add_chord_p2",
            "outer_active_gap": safe_float(swap2["mean_outer_active_rate"]) - safe_float(add2["mean_outer_active_rate"]),
            "persistent_rate_gap": safe_float(swap2["persistent_outer_branch_rate"]) - safe_float(add2["persistent_outer_branch_rate"]),
            "reseeded_rate_gap": safe_float(swap2["reseeded_outer_horizon_rate"]) - safe_float(add2["reseeded_outer_horizon_rate"]),
            "dominant_presence_gap": safe_float(swap2["mean_dominant_lineage_presence_rate"]) - safe_float(add2["mean_dominant_lineage_presence_rate"]),
            "dominant_mass_gap": safe_float(swap2["mean_dominant_lineage_mass_share"]) - safe_float(add2["mean_dominant_lineage_mass_share"]),
            "lateborn_mass_gap": safe_float(swap2["mean_lateborn_mass_share"]) - safe_float(add2["mean_lateborn_mass_share"]),
            "turnover_gap": safe_float(swap2["mean_turnover_rate"]) - safe_float(add2["mean_turnover_rate"]),
            "reactivation_gap": safe_float(swap2["mean_reactivation_count"]) - safe_float(add2["mean_reactivation_count"]),
        }
    )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    compares: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    by_profile = {str(row["profile_label"]): row for row in aggregate}
    by_compare = {str(row["compare_label"]): row for row in compares}

    add0 = by_profile["add_chord_p0"]
    add2 = by_profile["add_chord_p2"]
    swap0 = by_profile["local_swap_p0"]
    swap2 = by_profile["local_swap_p2"]

    add_gap = by_compare["add_chord_p2_minus_p0"]
    swap_gap = by_compare["local_swap_p2_minus_p0"]

    both_p2_persistent = (
        safe_float(add2["persistent_outer_branch_rate"]) >= 0.50
        and safe_float(swap2["persistent_outer_branch_rate"]) >= 0.50
    )
    both_p2_reseeded = (
        safe_float(add2["reseeded_outer_horizon_rate"]) >= 0.50
        and safe_float(swap2["reseeded_outer_horizon_rate"]) >= 0.50
    )
    both_p2_stronger_than_controls = (
        safe_float(add_gap["outer_active_gap"]) >= 0.25
        and safe_float(swap_gap["outer_active_gap"]) >= 0.25
    )

    if both_p2_persistent and both_p2_stronger_than_controls:
        status = "shared_p2_persistent_branch_candidate"
        note = (
            f"Begge p2-profiler holder outer-horisonten over p0-kontrollene og leses best som vedvarende ytre grein "
            f"(persistent rates add={fmt(add2['persistent_outer_branch_rate'])}, swap={fmt(swap2['persistent_outer_branch_rate'])})."
        )
        next_step = "measure_outer_branch_anchor_coupling"
        next_note = "Neste steg bor male hvordan den vedvarende ytre greinen kobler seg til indre skade, ikke gjenapne family-kartet."
    elif both_p2_reseeded and both_p2_stronger_than_controls:
        status = "shared_p2_reseeded_horizon_candidate"
        note = (
            f"Begge p2-profiler holder outer-horisonten over p0-kontrollene, men mekanikken ser best ut som re-seeding "
            f"(reseeded rates add={fmt(add2['reseeded_outer_horizon_rate'])}, swap={fmt(swap2['reseeded_outer_horizon_rate'])})."
        )
        next_step = "measure_inner_to_outer_flux"
        next_note = "Neste steg bor male om ny ytre masse kontinuerlig mates fra indre skade."
    elif both_p2_stronger_than_controls:
        status = "shared_p2_horizon_mechanism_mixed"
        note = (
            f"Begge p2-profiler holder outer-horisonten over p0-kontrollene, men genealogien kollapser ikke til én ren mekanisme "
            f"(dominant labels add={add2['dominant_mechanism_label']}, swap={swap2['dominant_mechanism_label']})."
        )
        next_step = "compare_persistent_vs_reseeded_cases"
        next_note = "Neste steg bor skille de mest vedvarende og mest reseedede p2-runene i samme observable-rom."
    else:
        status = "shared_p2_horizon_mechanism_not_yet"
        note = "Outer-genealogien er ikke sterk nok til aa gi en ren delt p2-mekanismefortelling ennå."
        next_step = "new_p2_observable"
        next_note = "Neste steg bor vaere en annen p2-observabel, ikke mer av samme genealogiklasse."

    carrier_alignment = (
        "aligned"
        if str(add2["dominant_mechanism_label"]) == str(swap2["dominant_mechanism_label"])
        and str(add2["dominant_mechanism_label"]) != "mixed_outer_horizon"
        else "mixed"
    )

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
            "diagnostic_family": "shared_p2_horizon_mechanism",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "carrier_alignment",
            "status": carrier_alignment,
            "note": (
                f"Dominant mekanikk ved p2 er add_chord={add2['dominant_mechanism_label']}, local_swap={swap2['dominant_mechanism_label']}."
            ),
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
    lines.append("# Relasjonell universgraf v0.15ci: target-768 p2 horizon genealogy mechanism lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om den delte p2-horisonten ved target `768` best leses som en vedvarende ytre grein eller som gjentatt outer re-seeding.")
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
    lines.append("| profile | dominant mech | persistent | reseeded | mixed | probe | active | dominant presence | dominant mass | lateborn mass | turnover | reactivation |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {row['dominant_mechanism_label']} | {fmt(row['persistent_outer_branch_rate'])} | {fmt(row['reseeded_outer_horizon_rate'])} | {fmt(row['mixed_outer_horizon_rate'])} | {fmt(row['outer_probe_only_rate'])} | {fmt(row['mean_outer_active_rate'])} | {fmt(row['mean_dominant_lineage_presence_rate'])} | {fmt(row['mean_dominant_lineage_mass_share'])} | {fmt(row['mean_lateborn_mass_share'])} | {fmt(row['mean_turnover_rate'])} | {fmt(row['mean_reactivation_count'])} |"
        )
    lines.append("")
    lines.append("## P2 versus P0")
    lines.append("")
    lines.append("| compare | active gap | persistent gap | reseeded gap | dominant presence gap | dominant mass gap | lateborn gap | turnover gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares[:2]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['outer_active_gap'])} | {fmt(row['persistent_rate_gap'])} | {fmt(row['reseeded_rate_gap'])} | {fmt(row['dominant_presence_gap'])} | {fmt(row['dominant_mass_gap'])} | {fmt(row['lateborn_mass_gap'])} | {fmt(row['turnover_gap'])} |"
        )
    lines.append("")
    lines.append("## Cross-carrier P2 contrast")
    lines.append("")
    lines.append("| compare | active gap | persistent gap | reseeded gap | dominant presence gap | dominant mass gap | lateborn gap | turnover gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in compares[2:]:
        lines.append(
            f"| {row['compare_label']} | {fmt(row['outer_active_gap'])} | {fmt(row['persistent_rate_gap'])} | {fmt(row['reseeded_rate_gap'])} | {fmt(row['dominant_presence_gap'])} | {fmt(row['dominant_mass_gap'])} | {fmt(row['lateborn_mass_gap'])} | {fmt(row['turnover_gap'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en smal mekanismerunde rundt p2-lommen ved target `768`, ikke et nytt bredt target-sok.")
    lines.append("- Positivt signal her betyr bare at outer-genealogien bærer repeterbar informasjon om hvordan horisonten holdes oppe.")
    lines.append("- Ingen av disse labelene skal leses som partikler eller universell geometri.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15ci", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Les dette som en smal genealogilesning av outer-horisonten, ikke som bevis for partikler eller spacetime.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15ci",
        "",
        "Denne runden ser pa om den ytre delen av monsteret holder seg i live som samme grein, eller om nye ytre biter stadig blir dannet underveis.",
        "",
        f"- Hovedresultat: `{diag['shared_p2_horizon_mechanism']['status']}`.",
        f"- Carrier alignment: `{diag['carrier_alignment']['status']}`.",
        "",
        "Dette er fortsatt bare en lokal, teknisk lesning av én smal effekt ved target 768.",
        "Det er ikke en paastand om partikler eller universets geometri.",
        "",
        f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ci target-768 p2 horizon genealogy mechanism lab.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15ci_target768_p2_horizon_genealogy_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15ci_target768_p2_horizon_genealogy_runs.csv")
    p.add_argument("--out-component-csv", type=str, default="Documentation/v15ci_target768_p2_horizon_genealogy_component_rows.csv")
    p.add_argument("--out-event-csv", type=str, default="Documentation/v15ci_target768_p2_horizon_genealogy_event_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ci_target768_p2_horizon_genealogy_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15ci_target768_p2_horizon_genealogy_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ci_target768_p2_horizon_genealogy_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ci_target768_p2_horizon_genealogy_mechanism_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ci_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ci.md")
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
    component_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []

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
                info = dict(res["perturbation_info"])
                support = [int(x) for x in info.get("support", [])]
                base_dist = v7.bfs_distances(base_state.g, support)
                fallback = (max(base_dist.values()) + 1) if base_dist else 1
                tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(res["log_rows"]))))
                tail_snapshots, comp_rows, ev_rows = build_tail_genealogy(
                    perturbation=perturbation,
                    placement=placement,
                    growth_seed=GROWTH_SEED,
                    seed_delta=seed_delta,
                    run_seed=run_seed,
                    tail_log_rows=res["log_rows"][tail_start:],
                    tail_damaged_sets=res["damaged_sets"][tail_start:],
                    tail_control_graphs=res["control_graphs"][tail_start:],
                    base_dist=base_dist,
                    fallback=fallback,
                )
                drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                raw_row = {
                    "requested_match": int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
                    "support_signature": ",".join(str(x) for x in support),
                    "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                    "abs_delta_spectral_radius_rel": safe_float(drift["abs_delta_spectral_radius_rel"]),
                }
                run_rows.append(
                    summarize_run(
                        perturbation=perturbation,
                        placement=placement,
                        growth_seed=GROWTH_SEED,
                        seed_delta=seed_delta,
                        run_seed=run_seed,
                        raw_row=raw_row,
                        tail_snapshots=tail_snapshots,
                        component_rows=comp_rows,
                        event_rows=ev_rows,
                    )
                )
                component_rows.extend(comp_rows)
                event_rows.extend(ev_rows)

    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    aggregate = aggregate_rows(run_rows)
    compares = compare_rows(aggregate)
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        aggregate=aggregate,
        compares=compares,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_component_csv, component_rows)
    write_csv(args.out_event_csv, event_rows)
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
