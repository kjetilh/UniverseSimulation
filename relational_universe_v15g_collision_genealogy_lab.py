#!/usr/bin/env python3
"""v0.15g collision genealogy lab for add_chord defects.

This follows v15b-v15f. The collision signal is real, but pair-family
micro-refinement with coarse window labels is no longer buying much.

The next narrow step is to keep the same matched collision setup and replace
coarse terminal labels with richer genealogy-aware observables:

- component trajectories over time
- split / merge / birth / death event logs
- event-chain summaries

This is still a narrow `48`-corridor experiment. It does not reopen frontier
search, Lorentz, or broad pair-offset scanning.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15b_add_chord_collision_lab as v15b
import relational_universe_v15d_collision_window_lab as v15d
import relational_universe_v15e_pair_family_refinement as v15e


TARGET = 48
PAIR_SPECS = ((2, 3), (3, 4))
CHAIN_PRECEDENCE = (
    "compress_split_rebind",
    "merge_hold_split",
    "split_persistent_dual",
    "split_fragment",
    "heterogeneous",
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15b.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15b.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    return v15b.write_csv(path, rows)


def parse_int_list(spec: str) -> List[int]:
    return [int(part.strip()) for part in spec.split(",") if part.strip()]


def induced_subgraph(g: v7.UGraph, nodes: Set[int]) -> v7.UGraph:
    sub = v7.UGraph()
    for v in sorted(nodes):
        if v in g.adj:
            sub.add_node(v)
    for a in sorted(nodes):
        if a not in g.adj:
            continue
        for b in g.neighbors(a):
            if b in nodes and a < b:
                sub.add_edge(a, b)
    return sub


def component_boundary_edge_count(g: v7.UGraph, component: Set[int]) -> int:
    count = 0
    for v in component:
        if v not in g.adj:
            continue
        for u in g.neighbors(v):
            if u not in component:
                count += 1
    return count


def component_min_distance(g: v7.UGraph, a_nodes: Set[int], b_nodes: Set[int]) -> float:
    if not a_nodes or not b_nodes:
        return float("nan")
    dist = v7.bfs_distances(g, a_nodes)
    vals = [dist[v] for v in b_nodes if v in dist]
    if not vals:
        return float("nan")
    return float(min(vals))


def support_distance_metrics(g: v7.UGraph, support: Sequence[int], component: Set[int]) -> Dict[str, float]:
    dist = v7.bfs_distances(g, support)
    vals = [float(dist[v]) for v in component if v in dist]
    if not vals:
        return {
            "min_support_distance": float("nan"),
            "max_support_distance": float("nan"),
            "mean_support_distance": float("nan"),
        }
    return {
        "min_support_distance": min(vals),
        "max_support_distance": max(vals),
        "mean_support_distance": mean_defined(vals),
    }


def serialize_ids(ids: Sequence[int]) -> str:
    return ",".join(str(int(x)) for x in ids)


def overlap_stats(a_nodes: Set[int], b_nodes: Set[int]) -> Tuple[int, float]:
    inter = len(a_nodes.intersection(b_nodes))
    if inter <= 0:
        return 0, 0.0
    union = len(a_nodes.union(b_nodes))
    jac = (inter / union) if union > 0 else 0.0
    return inter, float(jac)


def snapshot_components(
    *,
    snapshot_index: int,
    step: int,
    damaged: Set[int],
    control_graph: v7.UGraph,
    support_union: Sequence[int],
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    comps = v15.damaged_components(control_graph, damaged)
    comps.sort(key=lambda comp: (min(comp) if comp else -1, len(comp)))
    damaged_count = len(damaged)
    largest = max((len(comp) for comp in comps), default=0)
    summary = {
        "snapshot_index": int(snapshot_index),
        "step": int(step),
        "total_defect_mass": int(damaged_count),
        "component_count": int(len(comps)),
        "largest_component_fraction": (largest / damaged_count) if damaged_count > 0 else 0.0,
    }

    comp_rows: List[Dict[str, Any]] = []
    for local_idx, comp in enumerate(comps):
        sub = induced_subgraph(control_graph, comp)
        boundary = component_boundary_edge_count(control_graph, comp)
        distances = support_distance_metrics(control_graph, support_union, comp)
        comp_rows.append(
            {
                "snapshot_index": int(snapshot_index),
                "step": int(step),
                "component_local_index": int(local_idx),
                "nodes": set(comp),
                "size_nodes": int(len(comp)),
                "size_fraction": (len(comp) / damaged_count) if damaged_count > 0 else 0.0,
                "internal_edge_count": int(sub.num_edges()),
                "beta1_local": int(v7.beta1_cycle_rank(sub)),
                "boundary_edge_count": int(boundary),
                "boundary_to_volume": (boundary / len(comp)) if comp else 0.0,
                **distances,
            }
        )
    return summary, comp_rows


def choose_dominant(
    candidates: Sequence[int],
    score_lookup: Mapping[int, Tuple[int, float]],
) -> int:
    return max(
        candidates,
        key=lambda idx: (
            score_lookup[idx][0],
            score_lookup[idx][1],
            -idx,
        ),
    )


def build_order_genealogy(
    *,
    pair_label: str,
    growth_seed: int,
    run_offset: int,
    run_seed: int,
    order: str,
    order_result: Mapping[str, Any],
    old_window_class: str,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    support_union = list(order_result["support_union"])
    snapshots: List[Dict[str, Any]] = []
    for idx, log_row in enumerate(order_result["log_rows"]):
        summary, comps = snapshot_components(
            snapshot_index=idx,
            step=int(log_row["step"]),
            damaged=set(order_result["damaged_sets"][idx]),
            control_graph=order_result["control_graphs"][idx],
            support_union=support_union,
        )
        snapshots.append({"summary": summary, "components": comps})

    component_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []
    next_component_id = 1

    def emit_component_rows(
        comps: Sequence[Dict[str, Any]],
        snapshot_summary: Mapping[str, Any],
    ) -> None:
        for comp in comps:
            component_rows.append(
                {
                    "pair_label": pair_label,
                    "growth_seed": int(growth_seed),
                    "run_offset": int(run_offset),
                    "run_seed": int(run_seed),
                    "order": order,
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
                    "total_defect_mass": int(snapshot_summary["total_defect_mass"]),
                    "component_count": int(snapshot_summary["component_count"]),
                    "largest_component_fraction": safe_float(snapshot_summary["largest_component_fraction"]),
                }
            )

    first_summary = snapshots[0]["summary"]
    for comp in snapshots[0]["components"]:
        comp["component_id"] = next_component_id
        next_component_id += 1
        comp["parent_ids"] = []
    emit_component_rows(snapshots[0]["components"], first_summary)

    for snap_idx in range(1, len(snapshots)):
        prev_snapshot = snapshots[snap_idx - 1]
        curr_snapshot = snapshots[snap_idx]
        prev_comps = prev_snapshot["components"]
        curr_comps = curr_snapshot["components"]

        parent_children: Dict[int, List[int]] = {i: [] for i in range(len(prev_comps))}
        child_parents: Dict[int, List[int]] = {i: [] for i in range(len(curr_comps))}
        parent_child_scores: Dict[Tuple[int, int], Tuple[int, float]] = {}

        for p_idx, prev_comp in enumerate(prev_comps):
            for c_idx, curr_comp in enumerate(curr_comps):
                inter, jac = overlap_stats(set(prev_comp["nodes"]), set(curr_comp["nodes"]))
                if inter <= 0:
                    continue
                parent_children[p_idx].append(c_idx)
                child_parents[c_idx].append(p_idx)
                parent_child_scores[(p_idx, c_idx)] = (inter, jac)

        dominant_child: Dict[int, int] = {}
        for p_idx, child_ids in parent_children.items():
            if child_ids:
                scores = {c_idx: parent_child_scores[(p_idx, c_idx)] for c_idx in child_ids}
                dominant_child[p_idx] = choose_dominant(child_ids, scores)

        dominant_parent: Dict[int, int] = {}
        for c_idx, parent_ids in child_parents.items():
            if parent_ids:
                scores = {p_idx: parent_child_scores[(p_idx, c_idx)] for p_idx in parent_ids}
                dominant_parent[c_idx] = choose_dominant(parent_ids, scores)

        for c_idx, curr_comp in enumerate(curr_comps):
            parents = child_parents.get(c_idx, [])
            curr_comp["parent_ids"] = sorted(prev_comps[p]["component_id"] for p in parents)
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

        compress_flag = (
            int(curr_summary["component_count"]) < int(prev_summary["component_count"])
            and safe_float(curr_summary["largest_component_fraction"])
            >= safe_float(prev_summary["largest_component_fraction"]) + 0.10
        )
        if compress_flag:
            event_rows.append(
                {
                    "pair_label": pair_label,
                    "growth_seed": int(growth_seed),
                    "run_offset": int(run_offset),
                    "run_seed": int(run_seed),
                    "order": order,
                    "snapshot_index_from": int(prev_summary["snapshot_index"]),
                    "snapshot_index_to": int(curr_summary["snapshot_index"]),
                    "step_from": int(prev_summary["step"]),
                    "step_to": int(curr_summary["step"]),
                    "event_type": "compress",
                    "parent_ids": "",
                    "child_ids": "",
                    "parent_count": 0,
                    "child_count": 0,
                    "component_count_before": int(prev_summary["component_count"]),
                    "component_count_after": int(curr_summary["component_count"]),
                    "total_defect_mass_before": int(prev_summary["total_defect_mass"]),
                    "total_defect_mass_after": int(curr_summary["total_defect_mass"]),
                    "largest_component_fraction_before": safe_float(prev_summary["largest_component_fraction"]),
                    "largest_component_fraction_after": safe_float(curr_summary["largest_component_fraction"]),
                    "daughter_min_separation": float("nan"),
                }
            )

        for p_idx, children in parent_children.items():
            parent_comp = prev_comps[p_idx]
            parent_id = int(parent_comp["component_id"])
            if not children:
                event_rows.append(
                    {
                        "pair_label": pair_label,
                        "growth_seed": int(growth_seed),
                        "run_offset": int(run_offset),
                        "run_seed": int(run_seed),
                        "order": order,
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
                        "total_defect_mass_before": int(prev_summary["total_defect_mass"]),
                        "total_defect_mass_after": int(curr_summary["total_defect_mass"]),
                        "largest_component_fraction_before": safe_float(prev_summary["largest_component_fraction"]),
                        "largest_component_fraction_after": safe_float(curr_summary["largest_component_fraction"]),
                        "daughter_min_separation": float("nan"),
                    }
                )
            elif len(children) == 1 and len(child_parents.get(children[0], [])) == 1:
                child_id = int(curr_comps[children[0]]["component_id"])
                event_rows.append(
                    {
                        "pair_label": pair_label,
                        "growth_seed": int(growth_seed),
                        "run_offset": int(run_offset),
                        "run_seed": int(run_seed),
                        "order": order,
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
                        "total_defect_mass_before": int(prev_summary["total_defect_mass"]),
                        "total_defect_mass_after": int(curr_summary["total_defect_mass"]),
                        "largest_component_fraction_before": safe_float(prev_summary["largest_component_fraction"]),
                        "largest_component_fraction_after": safe_float(curr_summary["largest_component_fraction"]),
                        "daughter_min_separation": float("nan"),
                    }
                )
            elif len(children) > 1:
                child_ids = [int(curr_comps[c]["component_id"]) for c in children]
                separations = [
                    component_min_distance(
                        order_result["control_graphs"][snap_idx],
                        set(curr_comps[a]["nodes"]),
                        set(curr_comps[b]["nodes"]),
                    )
                    for i, a in enumerate(children)
                    for b in children[i + 1:]
                ]
                finite_sep = [v for v in separations if math.isfinite(v)]
                event_rows.append(
                    {
                        "pair_label": pair_label,
                        "growth_seed": int(growth_seed),
                        "run_offset": int(run_offset),
                        "run_seed": int(run_seed),
                        "order": order,
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
                        "total_defect_mass_before": int(prev_summary["total_defect_mass"]),
                        "total_defect_mass_after": int(curr_summary["total_defect_mass"]),
                        "largest_component_fraction_before": safe_float(prev_summary["largest_component_fraction"]),
                        "largest_component_fraction_after": safe_float(curr_summary["largest_component_fraction"]),
                        "daughter_min_separation": min(finite_sep) if finite_sep else float("nan"),
                    }
                )

        for c_idx, parents in child_parents.items():
            child_id = int(curr_comps[c_idx]["component_id"])
            if not parents:
                event_rows.append(
                    {
                        "pair_label": pair_label,
                        "growth_seed": int(growth_seed),
                        "run_offset": int(run_offset),
                        "run_seed": int(run_seed),
                        "order": order,
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
                        "total_defect_mass_before": int(prev_summary["total_defect_mass"]),
                        "total_defect_mass_after": int(curr_summary["total_defect_mass"]),
                        "largest_component_fraction_before": safe_float(prev_summary["largest_component_fraction"]),
                        "largest_component_fraction_after": safe_float(curr_summary["largest_component_fraction"]),
                        "daughter_min_separation": float("nan"),
                    }
                )
            elif len(parents) > 1:
                parent_ids = [int(prev_comps[p]["component_id"]) for p in parents]
                event_rows.append(
                    {
                        "pair_label": pair_label,
                        "growth_seed": int(growth_seed),
                        "run_offset": int(run_offset),
                        "run_seed": int(run_seed),
                        "order": order,
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
                        "total_defect_mass_before": int(prev_summary["total_defect_mass"]),
                        "total_defect_mass_after": int(curr_summary["total_defect_mass"]),
                        "largest_component_fraction_before": safe_float(prev_summary["largest_component_fraction"]),
                        "largest_component_fraction_after": safe_float(curr_summary["largest_component_fraction"]),
                        "daughter_min_separation": float("nan"),
                    }
                )

        emit_component_rows(curr_comps, curr_summary)

    snapshots_meta = [snap["summary"] for snap in snapshots]
    counts_by_snapshot = {
        int(s["snapshot_index"]): int(s["component_count"])
        for s in snapshots_meta
    }
    mass_by_snapshot = {
        int(s["snapshot_index"]): int(s["total_defect_mass"])
        for s in snapshots_meta
    }
    step_by_snapshot = {
        int(s["snapshot_index"]): int(s["step"])
        for s in snapshots_meta
    }

    event_by_type: Dict[str, List[Dict[str, Any]]] = {}
    for row in event_rows:
        event_by_type.setdefault(str(row["event_type"]), []).append(row)

    split_rows = event_by_type.get("split", [])
    merge_rows = event_by_type.get("merge", [])
    birth_rows = event_by_type.get("birth", [])
    death_rows = event_by_type.get("death", [])
    compress_rows = event_by_type.get("compress", [])

    first_split_step = min((int(r["step_to"]) for r in split_rows), default=-1)
    first_merge_step = min((int(r["step_to"]) for r in merge_rows), default=-1)
    first_split_idx = min((int(r["snapshot_index_to"]) for r in split_rows), default=-1)

    lifetimes: List[int] = []
    by_component: MutableMapping[int, List[Dict[str, Any]]] = {}
    for row in component_rows:
        by_component.setdefault(int(row["component_id"]), []).append(row)
    for cid, rows in by_component.items():
        rows.sort(key=lambda r: (int(r["snapshot_index"]), int(r["step"])))
        lifetime = int(rows[-1]["step"]) - int(rows[0]["step"])
        lifetimes.append(lifetime)

    post_first_split_dual_duration = -1
    if first_split_idx >= 0:
        active_indices: List[int] = []
        for idx in range(first_split_idx, len(snapshots_meta)):
            if counts_by_snapshot.get(idx, 0) >= 2:
                active_indices.append(idx)
            elif active_indices:
                break
        if len(active_indices) >= 1:
            post_first_split_dual_duration = (
                step_by_snapshot[active_indices[-1]] - step_by_snapshot[first_split_idx]
            )

    min_daughter_sep = min(
        (safe_float(r["daughter_min_separation"]) for r in split_rows if math.isfinite(safe_float(r["daughter_min_separation"]))),
        default=float("nan"),
    )

    split_snapshot_indices = sorted(int(r["snapshot_index_to"]) for r in split_rows)
    merge_snapshot_indices = sorted(int(r["snapshot_index_to"]) for r in merge_rows)
    birth_snapshot_indices = sorted(int(r["snapshot_index_to"]) for r in birth_rows)

    def has_merge_within(split_idx: int, max_gap: int) -> bool:
        return any(split_idx < m <= split_idx + max_gap for m in merge_snapshot_indices)

    def has_split_after(idx: int, min_gap: int, max_gap: int) -> bool:
        return any(idx + min_gap <= s <= idx + max_gap for s in split_snapshot_indices)

    def has_birth_or_count_increase(split_idx: int, max_gap: int) -> bool:
        start_count = counts_by_snapshot.get(split_idx, 0)
        birth_hit = any(split_idx < b <= split_idx + max_gap for b in birth_snapshot_indices)
        count_hit = any(
            counts_by_snapshot.get(idx, 0) > start_count
            for idx in range(split_idx + 1, min(len(snapshots_meta), split_idx + max_gap + 1))
        )
        return birth_hit or count_hit

    def split_has_persistent_dual(split_idx: int) -> bool:
        consecutive = 0
        for idx in range(split_idx, len(snapshots_meta)):
            if counts_by_snapshot.get(idx, 0) >= 2:
                consecutive += 1
                if consecutive >= 3:
                    return True
            elif consecutive > 0:
                return False
        return False

    compress_indices = sorted(int(r["snapshot_index_to"]) for r in compress_rows)
    merge_indices = merge_snapshot_indices
    split_indices = split_snapshot_indices

    def has_quiet_window_after(event_idx: int, quiet_snapshots: int = 2) -> bool:
        stop = min(len(snapshots_meta), event_idx + quiet_snapshots + 1)
        for idx in range(event_idx + 1, stop):
            if any(
                int(r["snapshot_index_to"]) == idx and str(r["event_type"]) in {"split", "merge"}
                for r in event_rows
            ):
                return False
        return True

    first_compress_idx = min(compress_indices, default=-1)
    first_split_idx = min(split_indices, default=-1)
    first_merge_idx = min(merge_indices, default=-1)

    compress_before_first_split = (
        first_split_idx >= 0
        and any(first_split_idx - 2 <= c < first_split_idx for c in compress_indices)
    )
    first_split_rebind = first_split_idx >= 0 and has_merge_within(first_split_idx, 3)
    has_compress_split_rebind = compress_before_first_split and first_split_rebind
    has_merge_hold_split = (
        first_merge_idx >= 0
        and has_quiet_window_after(first_merge_idx, 2)
        and has_split_after(first_merge_idx, 3, 5)
    )
    has_split_persistent_dual = first_split_idx >= 0 and split_has_persistent_dual(first_split_idx)
    has_split_fragment = first_split_idx >= 0 and has_birth_or_count_increase(first_split_idx, 2)

    if has_compress_split_rebind:
        chain_label = "compress_split_rebind"
    elif has_merge_hold_split:
        chain_label = "merge_hold_split"
    elif has_split_persistent_dual:
        chain_label = "split_persistent_dual"
    elif has_split_fragment:
        chain_label = "split_fragment"
    else:
        chain_label = "heterogeneous"

    order_summary = {
        "pair_label": pair_label,
        "growth_seed": int(growth_seed),
        "run_offset": int(run_offset),
        "run_seed": int(run_seed),
        "order": order,
        "chain_label": chain_label,
        "old_window_class": old_window_class,
        "split_count": len(split_rows),
        "merge_count": len(merge_rows),
        "birth_count": len(birth_rows),
        "death_count": len(death_rows),
        "first_split_step": first_split_step,
        "first_merge_step": first_merge_step,
        "max_component_count": max((int(s["component_count"]) for s in snapshots_meta), default=0),
        "mean_component_lifetime": mean_defined(lifetimes),
        "max_component_lifetime": max(lifetimes) if lifetimes else -1,
        "post_first_split_dual_duration": post_first_split_dual_duration,
        "max_total_defect_mass": max((int(s["total_defect_mass"]) for s in snapshots_meta), default=0),
        "mean_total_defect_mass": mean_defined(int(s["total_defect_mass"]) for s in snapshots_meta),
        "final_total_defect_mass": int(snapshots_meta[-1]["total_defect_mass"]),
        "min_daughter_separation_after_first_split": min_daughter_sep,
        "compress_count": len(compress_rows),
    }
    return component_rows, event_rows, order_summary


def order_window_metrics(
    *,
    pair_label: str,
    growth_seed: int,
    run_offset: int,
    run_seed: int,
    order: str,
    single_a: Mapping[str, Any],
    single_b: Mapping[str, Any],
    pair_result: Mapping[str, Any],
    other_pair_result: Mapping[str, Any],
) -> Dict[str, Any]:
    n_snap = min(
        len(single_a["damaged_sets"]),
        len(single_b["damaged_sets"]),
        len(pair_result["damaged_sets"]),
        len(other_pair_result["damaged_sets"]),
    )
    union_jaccards: List[float] = []
    order_jaccards: List[float] = []
    control_consistency: List[float] = []
    pair_minus_union_components: List[float] = []
    pair_minus_union_largest_frac: List[float] = []
    snapshot_steps: List[int] = []

    for idx in range(n_snap):
        union_d = set(single_a["damaged_sets"][idx]).union(single_b["damaged_sets"][idx])
        pair_d = set(pair_result["damaged_sets"][idx])
        other_pair_d = set(other_pair_result["damaged_sets"][idx])
        union_jaccards.append(v15b.jaccard(pair_d, union_d))
        order_jaccards.append(v15b.jaccard(pair_d, other_pair_d))
        snapshot_steps.append(int(pair_result["log_rows"][idx]["step"]))

        control_graph = pair_result["control_graphs"][idx]
        other_control_graph = other_pair_result["control_graphs"][idx]
        control_consistency.append(v15b.edge_jaccard_graphs(control_graph, other_control_graph))

        union_components, union_largest_frac = v15d.component_stats(control_graph, union_d)
        pair_components = int(pair_result["log_rows"][idx]["damage_component_count"])
        pair_largest_frac = safe_float(pair_result["log_rows"][idx]["largest_component_fraction"])
        pair_minus_union_components.append(float(pair_components - union_components))
        pair_minus_union_largest_frac.append(float(pair_largest_frac - union_largest_frac))

    min_idx = min(range(len(union_jaccards)), key=lambda i: union_jaccards[i])
    final_idx = len(union_jaccards) - 1
    row = {
        "pair_label": pair_label,
        "growth_seed": int(growth_seed),
        "run_offset": int(run_offset),
        "run_seed": int(run_seed),
        "order": order,
        "mean_control_consistency": mean_defined(control_consistency),
        "mean_order_jaccard": mean_defined(order_jaccards),
        "mean_union_jaccard": mean_defined(union_jaccards),
        "min_union_jaccard": union_jaccards[min_idx],
        "min_union_step": snapshot_steps[min_idx],
        "min_union_index_fraction": min_idx / max(1, final_idx),
        "window_pair_minus_union_components": pair_minus_union_components[min_idx],
        "window_pair_minus_union_largest_frac": pair_minus_union_largest_frac[min_idx],
        "final_union_jaccard": union_jaccards[final_idx],
        "final_pair_minus_union_components": pair_minus_union_components[final_idx],
        "final_pair_minus_union_largest_frac": pair_minus_union_largest_frac[final_idx],
        "pair_mean_radius": safe_float(pair_result["summary"]["mean_radius_control"]),
    }
    row["window_class"] = v15d.classify_window(row)
    return row


def pair_availability_rows(
    ensembles: Sequence[Any],
    base_states: Mapping[Tuple[str, int], Any],
    growth_seeds: Sequence[int],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for ens in ensembles:
        if int(ens.target_nodes) != TARGET:
            continue
        for gseed in growth_seeds:
            base = base_states[(ens.name, int(gseed))]
            for a, b in PAIR_SPECS:
                meta = v15e.pair_is_valid(base, a, b)
                rows.append(
                    {
                        "ensemble": ens.name,
                        "target_nodes": int(ens.target_nodes),
                        "growth_seed": int(gseed),
                        "pair_label": f"{a}-{b}",
                        "pair_available": 1 if meta is not None else 0,
                        "min_support_distance": int(meta["min_support_distance"]) if meta is not None else -1,
                        "support_a_size": int(meta["support_a_size"]) if meta is not None else -1,
                        "support_b_size": int(meta["support_b_size"]) if meta is not None else -1,
                    }
                )
    return rows


def run_pair_genealogy(
    *,
    base: Any,
    pair: Tuple[int, int],
    growth_seed: int,
    run_offset: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    spec = v15b.anchor_spec()
    params = v15b.v09.candidate_to_params(spec["candidate"])
    steps = v15b.collision_steps_for_state(base.g.num_nodes())
    run_seed = int(TARGET) * 100000 + int(growth_seed) * 1000 + int(run_offset)

    single_a = v15b.run_sequence_from_base(
        base,
        params=params,
        seed=run_seed,
        steps=steps,
        placements=[pair[0]],
        local_coupling="maximal",
        log_every=2,
    )
    single_b = v15b.run_sequence_from_base(
        base,
        params=params,
        seed=run_seed,
        steps=steps,
        placements=[pair[1]],
        local_coupling="maximal",
        log_every=2,
    )
    pair_ab = v15b.run_sequence_from_base(
        base,
        params=params,
        seed=run_seed,
        steps=steps,
        placements=[pair[0], pair[1]],
        local_coupling="maximal",
        log_every=2,
    )
    pair_ba = v15b.run_sequence_from_base(
        base,
        params=params,
        seed=run_seed,
        steps=steps,
        placements=[pair[1], pair[0]],
        local_coupling="maximal",
        log_every=2,
    )

    metrics_ab = order_window_metrics(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=growth_seed,
        run_offset=run_offset,
        run_seed=run_seed,
        order="ab",
        single_a=single_a,
        single_b=single_b,
        pair_result=pair_ab,
        other_pair_result=pair_ba,
    )
    metrics_ba = order_window_metrics(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=growth_seed,
        run_offset=run_offset,
        run_seed=run_seed,
        order="ba",
        single_a=single_a,
        single_b=single_b,
        pair_result=pair_ba,
        other_pair_result=pair_ab,
    )

    comp_ab, events_ab, summary_ab = build_order_genealogy(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=growth_seed,
        run_offset=run_offset,
        run_seed=run_seed,
        order="ab",
        order_result=pair_ab,
        old_window_class=str(metrics_ab["window_class"]),
    )
    comp_ba, events_ba, summary_ba = build_order_genealogy(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=growth_seed,
        run_offset=run_offset,
        run_seed=run_seed,
        order="ba",
        order_result=pair_ba,
        old_window_class=str(metrics_ba["window_class"]),
    )

    return comp_ab + comp_ba, events_ab + events_ba, summary_ab, summary_ba, {
        "metrics_ab": metrics_ab,
        "metrics_ba": metrics_ba,
    }


def pair_run_summary(
    *,
    pair_label: str,
    growth_seed: int,
    run_offset: int,
    run_seed: int,
    summary_ab: Mapping[str, Any],
    summary_ba: Mapping[str, Any],
    window_ab: Mapping[str, Any],
    window_ba: Mapping[str, Any],
) -> Dict[str, Any]:
    ambiguous = int(
        str(summary_ab["chain_label"]) != str(summary_ba["chain_label"])
        or int(summary_ab["split_count"]) != int(summary_ba["split_count"])
        or int(summary_ab["merge_count"]) != int(summary_ba["merge_count"])
        or int(summary_ab["birth_count"]) != int(summary_ba["birth_count"])
        or int(summary_ab["death_count"]) != int(summary_ba["death_count"])
        or str(window_ab["window_class"]) != str(window_ba["window_class"])
    )

    common_chain = (
        str(summary_ab["chain_label"])
        if str(summary_ab["chain_label"]) == str(summary_ba["chain_label"])
        else "order_ambiguous"
    )
    common_window = (
        str(window_ab["window_class"])
        if str(window_ab["window_class"]) == str(window_ba["window_class"])
        else "order_ambiguous_window"
    )
    return {
        "pair_label": pair_label,
        "growth_seed": int(growth_seed),
        "run_offset": int(run_offset),
        "run_seed": int(run_seed),
        "order_ambiguous": ambiguous,
        "chain_label": common_chain,
        "old_window_class": common_window,
        "mean_control_consistency": mean_defined(
            [safe_float(window_ab["mean_control_consistency"]), safe_float(window_ba["mean_control_consistency"])]
        ),
        "mean_order_jaccard": mean_defined(
            [safe_float(window_ab["mean_order_jaccard"]), safe_float(window_ba["mean_order_jaccard"])]
        ),
        "split_count": mean_defined([safe_float(summary_ab["split_count"]), safe_float(summary_ba["split_count"])]),
        "merge_count": mean_defined([safe_float(summary_ab["merge_count"]), safe_float(summary_ba["merge_count"])]),
        "birth_count": mean_defined([safe_float(summary_ab["birth_count"]), safe_float(summary_ba["birth_count"])]),
        "death_count": mean_defined([safe_float(summary_ab["death_count"]), safe_float(summary_ba["death_count"])]),
        "first_split_step": mean_defined([safe_float(summary_ab["first_split_step"]), safe_float(summary_ba["first_split_step"])]),
        "first_merge_step": mean_defined([safe_float(summary_ab["first_merge_step"]), safe_float(summary_ba["first_merge_step"])]),
        "max_component_count": mean_defined([safe_float(summary_ab["max_component_count"]), safe_float(summary_ba["max_component_count"])]),
        "mean_component_lifetime": mean_defined([safe_float(summary_ab["mean_component_lifetime"]), safe_float(summary_ba["mean_component_lifetime"])]),
        "max_component_lifetime": mean_defined([safe_float(summary_ab["max_component_lifetime"]), safe_float(summary_ba["max_component_lifetime"])]),
        "post_first_split_dual_duration": mean_defined(
            [safe_float(summary_ab["post_first_split_dual_duration"]), safe_float(summary_ba["post_first_split_dual_duration"])]
        ),
        "max_total_defect_mass": mean_defined([safe_float(summary_ab["max_total_defect_mass"]), safe_float(summary_ba["max_total_defect_mass"])]),
        "mean_total_defect_mass": mean_defined([safe_float(summary_ab["mean_total_defect_mass"]), safe_float(summary_ba["mean_total_defect_mass"])]),
        "final_total_defect_mass": mean_defined([safe_float(summary_ab["final_total_defect_mass"]), safe_float(summary_ba["final_total_defect_mass"])]),
        "min_daughter_separation_after_first_split": mean_defined(
            [safe_float(summary_ab["min_daughter_separation_after_first_split"]), safe_float(summary_ba["min_daughter_separation_after_first_split"])]
        ),
    }


def collect_primary_rows(
    *,
    ensembles: Sequence[Any],
    base_states: Mapping[Tuple[str, int], Any],
    growth_seeds: Sequence[int],
    run_offsets: Sequence[int],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    component_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []
    pair_run_rows: List[Dict[str, Any]] = []
    order_rows: List[Dict[str, Any]] = []

    for ens in ensembles:
        if int(ens.target_nodes) != TARGET:
            continue
        for growth_seed in growth_seeds:
            base = base_states[(ens.name, int(growth_seed))]
            for pair in PAIR_SPECS:
                meta = v15e.pair_is_valid(base, pair[0], pair[1])
                if meta is None:
                    continue
                for run_offset in run_offsets:
                    comp_rows, ev_rows, summary_ab, summary_ba, window_rows = run_pair_genealogy(
                        base=base,
                        pair=pair,
                        growth_seed=int(growth_seed),
                        run_offset=int(run_offset),
                    )
                    component_rows.extend(comp_rows)
                    event_rows.extend(ev_rows)
                    order_rows.extend([dict(summary_ab), dict(summary_ba)])
                    pair_run_rows.append(
                        pair_run_summary(
                            pair_label=f"{pair[0]}-{pair[1]}",
                            growth_seed=int(growth_seed),
                            run_offset=int(run_offset),
                            run_seed=int(TARGET) * 100000 + int(growth_seed) * 1000 + int(run_offset),
                            summary_ab=summary_ab,
                            summary_ba=summary_ba,
                            window_ab=window_rows["metrics_ab"],
                            window_ba=window_rows["metrics_ba"],
                        )
                    )
    return component_rows, event_rows, pair_run_rows, order_rows


def event_chain_rows(pair_run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: MutableMapping[str, List[Dict[str, Any]]] = {}
    for row in pair_run_rows:
        if int(row["order_ambiguous"]) == 1:
            continue
        groups.setdefault(str(row["pair_label"]), []).append(dict(row))

    out: List[Dict[str, Any]] = []
    for pair_label, rows in sorted(groups.items()):
        total = max(1, len(rows))
        counts: Dict[str, int] = {}
        for row in rows:
            counts[str(row["chain_label"])] = counts.get(str(row["chain_label"]), 0) + 1
        for chain_label in CHAIN_PRECEDENCE:
            out.append(
                {
                    "pair_label": pair_label,
                    "chain_label": chain_label,
                    "n_runs": counts.get(chain_label, 0),
                    "rate": counts.get(chain_label, 0) / total,
                }
            )
    return out


def aggregate_pair_runs(pair_run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_pair: MutableMapping[str, List[Dict[str, Any]]] = {}
    for row in pair_run_rows:
        by_pair.setdefault(str(row["pair_label"]), []).append(dict(row))

    out: List[Dict[str, Any]] = []
    for pair_label, rows in sorted(by_pair.items()):
        included = [r for r in rows if int(r["order_ambiguous"]) == 0]
        total = max(1, len(included))
        chain_counts: Dict[str, int] = {}
        window_counts: Dict[str, int] = {}
        for row in included:
            chain_counts[str(row["chain_label"])] = chain_counts.get(str(row["chain_label"]), 0) + 1
            window_counts[str(row["old_window_class"])] = window_counts.get(str(row["old_window_class"]), 0) + 1
        dominant_chain = max(chain_counts.items(), key=lambda kv: (kv[1], kv[0]))[0] if chain_counts else "none"
        dominant_window = max(window_counts.items(), key=lambda kv: (kv[1], kv[0]))[0] if window_counts else "none"
        out.append(
            {
                "pair_label": pair_label,
                "n_pair_runs": len(rows),
                "n_included_runs": len(included),
                "order_ambiguous_count": sum(int(r["order_ambiguous"]) for r in rows),
                "mean_control_consistency": mean_defined(safe_float(r["mean_control_consistency"]) for r in rows),
                "mean_order_jaccard": mean_defined(safe_float(r["mean_order_jaccard"]) for r in rows),
                "mean_split_count": mean_defined(safe_float(r["split_count"]) for r in included),
                "mean_merge_count": mean_defined(safe_float(r["merge_count"]) for r in included),
                "mean_birth_count": mean_defined(safe_float(r["birth_count"]) for r in included),
                "mean_death_count": mean_defined(safe_float(r["death_count"]) for r in included),
                "mean_first_split_step": mean_defined(safe_float(r["first_split_step"]) for r in included if safe_float(r["first_split_step"]) >= 0),
                "mean_first_merge_step": mean_defined(safe_float(r["first_merge_step"]) for r in included if safe_float(r["first_merge_step"]) >= 0),
                "mean_max_component_count": mean_defined(safe_float(r["max_component_count"]) for r in included),
                "mean_component_lifetime": mean_defined(safe_float(r["mean_component_lifetime"]) for r in included),
                "max_component_lifetime": max((safe_float(r["max_component_lifetime"]) for r in included), default=float("nan")),
                "mean_post_first_split_dual_duration": mean_defined(
                    safe_float(r["post_first_split_dual_duration"]) for r in included if safe_float(r["post_first_split_dual_duration"]) >= 0
                ),
                "mean_max_total_defect_mass": mean_defined(safe_float(r["max_total_defect_mass"]) for r in included),
                "mean_mean_total_defect_mass": mean_defined(safe_float(r["mean_total_defect_mass"]) for r in included),
                "mean_final_total_defect_mass": mean_defined(safe_float(r["final_total_defect_mass"]) for r in included),
                "mean_min_daughter_separation_after_first_split": mean_defined(
                    safe_float(r["min_daughter_separation_after_first_split"])
                    for r in included
                    if math.isfinite(safe_float(r["min_daughter_separation_after_first_split"]))
                ),
                "compress_split_rebind_rate": chain_counts.get("compress_split_rebind", 0) / total,
                "merge_hold_split_rate": chain_counts.get("merge_hold_split", 0) / total,
                "split_persistent_dual_rate": chain_counts.get("split_persistent_dual", 0) / total,
                "split_fragment_rate": chain_counts.get("split_fragment", 0) / total,
                "heterogeneous_rate": chain_counts.get("heterogeneous", 0) / total,
                "dominant_chain_label": dominant_chain,
                "old_window_binding_rate": window_counts.get("persistent_binding_tendency", 0) / total,
                "old_window_compress_then_split_rate": window_counts.get("compress_then_split", 0) / total,
                "old_window_mixed_rate": window_counts.get("mixed_window", 0) / total,
                "dominant_old_window_class": dominant_window,
            }
        )
    return out


def recommendation_rows(
    *,
    target_summary: Sequence[Dict[str, Any]],
    availability_rows: Sequence[Dict[str, Any]],
    aggregate_rows: Sequence[Dict[str, Any]],
    pair_run_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    all_pairs_present = all(int(row["pair_available"]) == 1 for row in availability_rows if int(row["growth_seed"]) == 101)
    control_clean = min((safe_float(row["mean_control_consistency"]) for row in aggregate_rows), default=1.0) >= 0.95
    out = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and all_pairs_present and control_clean) else "unclear",
            "note": (
                "Startstørrelsene er separert, begge pair-familiene finnes på den delte 101-basen, og order-control holder seg samkjørt."
                if (size_clean and all_pairs_present and control_clean)
                else "Enten størrelsesseparasjon, pair-tilgjengelighet eller order-control er uklar i v15g."
            ),
        }
    ]

    ambiguous_rate = mean_defined(float(row["order_ambiguous"]) for row in pair_run_rows)
    by_pair = {str(row["pair_label"]): row for row in aggregate_rows}
    pair23 = by_pair.get("2-3")
    pair34 = by_pair.get("3-4")

    if ambiguous_rate > 0.25:
        signal_status = "failed_instrumentation"
        signal_note = (
            f"Order-ambiguiteten er for høy ({ambiguous_rate:.3f}) til å lese genealogy-chainene trygt som robust familiesignal."
        )
        next_status = "tighten_genealogy_matching"
        next_note = "Neste steg bør være en liten instrumenteringsfiks i matching eller ID-propagasjon, ikke bredere kjøring."
    elif pair23 and pair34:
        pair23_dom = str(pair23["dominant_chain_label"])
        pair34_dom = str(pair34["dominant_chain_label"])
        pair23_het = safe_float(pair23["heterogeneous_rate"])
        pair34_het = safe_float(pair34["heterogeneous_rate"])
        if pair23_dom != pair34_dom and max(pair23_het, pair34_het) < 0.50:
            signal_status = "repeatable_event_chains_found"
            signal_note = (
                f"`2-3` og `3-4` skiller seg nå på dominant genealogy-chain (`{pair23_dom}` vs `{pair34_dom}`) uten at heterogenitet dominerer begge."
            )
            next_status = "follow_chain_difference"
            next_note = "Neste steg bør følge den nye chain-separasjonen med få representative lange trajectories."
        elif pair23_het >= 0.50 and pair34_het >= 0.50:
            signal_status = "real_but_heterogeneous"
            signal_note = (
                f"Begge pair-familiene forblir hovedsakelig heterogene (`2-3` {pair23_het:.3f}, `3-4` {pair34_het:.3f}) selv med genealogy-sporing."
            )
            next_status = "change_observable_or_question"
            next_note = "Neste steg bør være lengre representative trajectories eller annen defect-observasjon, ikke mer pair-offset finjustering."
        else:
            signal_status = "partially_structured"
            signal_note = (
                f"Genealogy-sporingen reduserer noe usikkerhet, men pair-familiene kollapser fortsatt ikke rent til én liten chain-familie (`2-3` {pair23_dom}, `3-4` {pair34_dom})."
            )
            next_status = "follow_representative_traces"
            next_note = "Neste steg bør være å følge noen få representative runs lenger i tid med de samme observablene."
    else:
        signal_status = "pair_comparison_incomplete"
        signal_note = "En eller begge pair-familiene manglet i den delte basen, så genealogy-sammenlikningen ble ufullstendig."
        next_status = "repair_shared_base"
        next_note = "Neste steg bør være å sikre et delt grunnlag før videre pair-sammenlikning."

    out.append({"diagnostic_family": "genealogy_signal", "status": signal_status, "note": signal_note})
    out.append({"diagnostic_family": "next_step", "status": next_status, "note": next_note})
    return out


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def build_report(
    *,
    target_summary: Sequence[Dict[str, Any]],
    availability_rows: Sequence[Dict[str, Any]],
    aggregate_rows: Sequence[Dict[str, Any]],
    chain_rows: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15g: collision genealogy lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden holder samme add_chord-kollisjonsoppsett som v15b-v15f, men lar genealogy, event-kjeder og komponentbaner være hovedproduktet i stedet for de gamle coarse window-etikettene."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Pair availability audit")
    lines.append("")
    lines.append("| growth | pair | available | min dist |")
    lines.append("| --- | --- | --- | --- |")
    for row in availability_rows:
        lines.append(
            f"| {int(row['growth_seed'])} | {row['pair_label']} | {int(row['pair_available'])} | {int(row['min_support_distance'])} |"
        )
    lines.append("")
    lines.append("## Aggregate genealogy signals")
    lines.append("")
    lines.append("| pair | included | ambiguous | split | merge | birth | death | mean lifetime | max comps | dual duration | dominant chain | hetero | old mixed |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate_rows:
        lines.append(
            f"| {row['pair_label']} | {int(row['n_included_runs'])} | {int(row['order_ambiguous_count'])} | {fmt(row['mean_split_count'])} | {fmt(row['mean_merge_count'])} | {fmt(row['mean_birth_count'])} | {fmt(row['mean_death_count'])} | {fmt(row['mean_component_lifetime'])} | {fmt(row['mean_max_component_count'])} | {fmt(row['mean_post_first_split_dual_duration'])} | {row['dominant_chain_label']} | {fmt(row['heterogeneous_rate'])} | {fmt(row['old_window_mixed_rate'])} |"
        )
    lines.append("")
    lines.append("## Event-chain frequencies")
    lines.append("")
    lines.append("| pair | chain | n | rate |")
    lines.append("| --- | --- | --- | --- |")
    for row in chain_rows:
        lines.append(
            f"| {row['pair_label']} | {row['chain_label']} | {int(row['n_runs'])} | {fmt(row['rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- `split`, `merge`, `birth` og `death` er genealogy-hendelser i den lokale damagesonen, ikke partikkelbevis.")
    lines.append("- `compress_split_rebind`, `merge_hold_split`, `split_persistent_dual` og `split_fragment` er diagnostiske chain-navn, ikke fysiske arter.")
    lines.append("- De gamle `window_class`-etikettene beholdes bare som downstream-sammenlikning.")
    lines.append("")
    return "\n".join(lines)


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    signal = next((row for row in recommendation if row["diagnostic_family"] == "genealogy_signal"), None)
    nxt = next((row for row in recommendation if row["diagnostic_family"] == "next_step"), None)
    return "\n".join(
        [
            "# Relasjonell universgraf v0.15g for ikke-spesialister",
            "",
            "Denne runden prøvde ikke bare å gi hver kollisjon ett sluttstempel. Den fulgte i stedet hvordan skaden deler seg, slår seg sammen og lever videre over tid.",
            "",
            f"Hoveddommen er `{signal['status'] if signal else 'ukjent'}`.",
            "",
            f"Det betyr: {signal['note'] if signal else 'ingen oppsummering tilgjengelig.'}",
            "",
            f"Neste anbefaling er: {nxt['note'] if nxt else 'ingen ny anbefaling registrert.'}",
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15g collision genealogy lab.")
    p.add_argument("--primary-growth-seeds", type=str, default="101")
    p.add_argument("--audit-growth-seeds", type=str, default="101,202")
    p.add_argument("--run-offsets", type=str, default="0,5,11,17,23,29")
    p.add_argument("--out-component-csv", type=str, default="Documentation/v15g_collision_genealogy_component_trajectories.csv")
    p.add_argument("--out-event-log-csv", type=str, default="Documentation/v15g_collision_genealogy_event_log.csv")
    p.add_argument("--out-event-aggregate-csv", type=str, default="Documentation/v15g_collision_genealogy_event_aggregate.csv")
    p.add_argument("--out-event-chain-csv", type=str, default="Documentation/v15g_collision_genealogy_event_chains.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15g_collision_genealogy_target_summary.csv")
    p.add_argument("--out-availability-csv", type=str, default="Documentation/v15g_collision_genealogy_pair_availability.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15g_collision_genealogy_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15g_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15g.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    primary_growth_seeds = parse_int_list(args.primary_growth_seeds)
    audit_growth_seeds = parse_int_list(args.audit_growth_seeds)
    run_offsets = parse_int_list(args.run_offsets)

    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15b.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, audit_growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)
    availability = pair_availability_rows(ensembles, base_states, audit_growth_seeds)

    component_rows, event_rows, pair_run_rows, _order_rows = collect_primary_rows(
        ensembles=ensembles,
        base_states=base_states,
        growth_seeds=primary_growth_seeds,
        run_offsets=run_offsets,
    )
    aggregate = aggregate_pair_runs(pair_run_rows)
    chains = event_chain_rows(pair_run_rows)
    recommendation = recommendation_rows(
        target_summary=target_summary,
        availability_rows=availability,
        aggregate_rows=aggregate,
        pair_run_rows=pair_run_rows,
    )

    report_md = build_report(
        target_summary=target_summary,
        availability_rows=availability,
        aggregate_rows=aggregate,
        chain_rows=chains,
        recommendation=recommendation,
    )
    op_md = "\n".join(
        [
            "# v0.15g operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Ikke les genealogy-chainene som bevis på partikler eller scattering-lov.",
            "- Les dem som et forsøk på å redusere `mixed` til færre og mer repeterbare hendelsesforløp.",
        ]
    )
    lay_md = build_lay_summary(recommendation)

    write_csv(args.out_component_csv, component_rows)
    write_csv(args.out_event_log_csv, event_rows)
    write_csv(args.out_event_aggregate_csv, aggregate)
    write_csv(args.out_event_chain_csv, chains)
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_availability_csv, availability)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")

    print(f"Wrote {args.out_summary_md}")
    print(f"Wrote {args.out_component_csv}")
    print(f"Wrote {args.out_event_log_csv}")
    print(f"Wrote {args.out_event_aggregate_csv}")


if __name__ == "__main__":
    main()
