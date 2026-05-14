#!/usr/bin/env python3
"""v0.15cw add_chord p1/p3 genealogy seed-split lab.

v15cv confirmed the p1/p3 placement landscape but rejected simple static
support-geometry and early-launch explanations. This round keeps the exact
p1/p3, target 896/1024, seed 7307/7351 scope and adds genealogy-aware component
tracking.

Primary product:
- component trajectories
- split / merge / birth / death / compress event logs
- run-level genealogy pattern summaries

The far-shell horizon label remains a downstream outcome, not the primary
observable.
"""
from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15cn_p2_horizon_scale_holdout as v15cn
import relational_universe_v15cs_add_chord_p0_scale_response_holdout as v15cs
import relational_universe_v15cv_add_chord_winning_placement_mechanism_probe as v15cv
import relational_universe_v15g_collision_genealogy_lab as v15g
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGETS = v15cv.TARGETS
PLACEMENTS = v15cv.PLACEMENTS
SEED_DELTAS = v15cv.SEED_DELTAS
PERTURBATION = v15cv.PERTURBATION
GROWTH_SEED = v15cv.GROWTH_SEED
LOG_EVERY = v15cv.LOG_EVERY


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


def emit_component_rows(
    *,
    out: List[Dict[str, Any]],
    run_ids: Mapping[str, Any],
    comps: Sequence[Dict[str, Any]],
    snapshot_summary: Mapping[str, Any],
) -> None:
    for comp in comps:
        out.append(
            {
                **run_ids,
                "snapshot_index": int(snapshot_summary["snapshot_index"]),
                "step": int(snapshot_summary["step"]),
                "component_local_index": int(comp["component_local_index"]),
                "component_id": int(comp["component_id"]),
                "parent_ids": v15g.serialize_ids(comp.get("parent_ids", [])),
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


def emit_event(
    *,
    out: List[Dict[str, Any]],
    run_ids: Mapping[str, Any],
    prev_summary: Mapping[str, Any],
    curr_summary: Mapping[str, Any],
    event_type: str,
    parent_ids: Sequence[int] | str,
    child_ids: Sequence[int] | str,
    parent_count: int,
    child_count: int,
    daughter_min_separation: float = float("nan"),
) -> None:
    parent_text = parent_ids if isinstance(parent_ids, str) else v15g.serialize_ids(parent_ids)
    child_text = child_ids if isinstance(child_ids, str) else v15g.serialize_ids(child_ids)
    out.append(
        {
            **run_ids,
            "snapshot_index_from": int(prev_summary["snapshot_index"]),
            "snapshot_index_to": int(curr_summary["snapshot_index"]),
            "step_from": int(prev_summary["step"]),
            "step_to": int(curr_summary["step"]),
            "event_type": event_type,
            "parent_ids": parent_text,
            "child_ids": child_text,
            "parent_count": int(parent_count),
            "child_count": int(child_count),
            "component_count_before": int(prev_summary["component_count"]),
            "component_count_after": int(curr_summary["component_count"]),
            "total_defect_mass_before": int(prev_summary["total_defect_mass"]),
            "total_defect_mass_after": int(curr_summary["total_defect_mass"]),
            "largest_component_fraction_before": safe_float(prev_summary["largest_component_fraction"]),
            "largest_component_fraction_after": safe_float(curr_summary["largest_component_fraction"]),
            "daughter_min_separation": safe_float(daughter_min_separation),
        }
    )


def genealogy_for_run(
    *,
    run_ids: Mapping[str, Any],
    log_rows: Sequence[Mapping[str, Any]],
    damaged_sets: Sequence[Set[int]],
    control_graphs: Sequence[v7.UGraph],
    support: Sequence[int],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    snapshots: List[Dict[str, Any]] = []
    for idx, log_row in enumerate(log_rows):
        summary, comps = v15g.snapshot_components(
            snapshot_index=idx,
            step=int(log_row["step"]),
            damaged=set(damaged_sets[idx]),
            control_graph=control_graphs[idx],
            support_union=support,
        )
        snapshots.append({"summary": summary, "components": comps})

    component_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []
    next_component_id = 1

    first_summary = snapshots[0]["summary"]
    for comp in snapshots[0]["components"]:
        comp["component_id"] = next_component_id
        next_component_id += 1
        comp["parent_ids"] = []
    emit_component_rows(out=component_rows, run_ids=run_ids, comps=snapshots[0]["components"], snapshot_summary=first_summary)

    for snap_idx in range(1, len(snapshots)):
        prev_snapshot = snapshots[snap_idx - 1]
        curr_snapshot = snapshots[snap_idx]
        prev_comps = prev_snapshot["components"]
        curr_comps = curr_snapshot["components"]
        prev_summary = prev_snapshot["summary"]
        curr_summary = curr_snapshot["summary"]

        parent_children: Dict[int, List[int]] = {i: [] for i in range(len(prev_comps))}
        child_parents: Dict[int, List[int]] = {i: [] for i in range(len(curr_comps))}
        parent_child_scores: Dict[Tuple[int, int], Tuple[int, float]] = {}

        for p_idx, prev_comp in enumerate(prev_comps):
            for c_idx, curr_comp in enumerate(curr_comps):
                inter, jac = v15g.overlap_stats(set(prev_comp["nodes"]), set(curr_comp["nodes"]))
                if inter <= 0:
                    continue
                parent_children[p_idx].append(c_idx)
                child_parents[c_idx].append(p_idx)
                parent_child_scores[(p_idx, c_idx)] = (inter, jac)

        dominant_child: Dict[int, int] = {}
        for p_idx, child_ids in parent_children.items():
            if child_ids:
                scores = {c_idx: parent_child_scores[(p_idx, c_idx)] for c_idx in child_ids}
                dominant_child[p_idx] = v15g.choose_dominant(child_ids, scores)

        dominant_parent: Dict[int, int] = {}
        for c_idx, parent_ids in child_parents.items():
            if parent_ids:
                scores = {p_idx: parent_child_scores[(p_idx, c_idx)] for p_idx in parent_ids}
                dominant_parent[c_idx] = v15g.choose_dominant(parent_ids, scores)

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

        compress_flag = (
            int(curr_summary["component_count"]) < int(prev_summary["component_count"])
            and safe_float(curr_summary["largest_component_fraction"])
            >= safe_float(prev_summary["largest_component_fraction"]) + 0.10
        )
        if compress_flag:
            emit_event(
                out=event_rows,
                run_ids=run_ids,
                prev_summary=prev_summary,
                curr_summary=curr_summary,
                event_type="compress",
                parent_ids="",
                child_ids="",
                parent_count=0,
                child_count=0,
            )

        for p_idx, children in parent_children.items():
            parent_comp = prev_comps[p_idx]
            parent_id = int(parent_comp["component_id"])
            if not children:
                emit_event(
                    out=event_rows,
                    run_ids=run_ids,
                    prev_summary=prev_summary,
                    curr_summary=curr_summary,
                    event_type="death",
                    parent_ids=[parent_id],
                    child_ids="",
                    parent_count=1,
                    child_count=0,
                )
            elif len(children) == 1 and len(child_parents.get(children[0], [])) == 1:
                child_id = int(curr_comps[children[0]]["component_id"])
                emit_event(
                    out=event_rows,
                    run_ids=run_ids,
                    prev_summary=prev_summary,
                    curr_summary=curr_summary,
                    event_type="persist",
                    parent_ids=[parent_id],
                    child_ids=[child_id],
                    parent_count=1,
                    child_count=1,
                )
            elif len(children) > 1:
                child_ids = [int(curr_comps[c]["component_id"]) for c in children]
                separations = [
                    v15g.component_min_distance(
                        control_graphs[snap_idx],
                        set(curr_comps[a]["nodes"]),
                        set(curr_comps[b]["nodes"]),
                    )
                    for i, a in enumerate(children)
                    for b in children[i + 1:]
                ]
                finite_sep = [x for x in separations if math.isfinite(safe_float(x))]
                emit_event(
                    out=event_rows,
                    run_ids=run_ids,
                    prev_summary=prev_summary,
                    curr_summary=curr_summary,
                    event_type="split",
                    parent_ids=[parent_id],
                    child_ids=child_ids,
                    parent_count=1,
                    child_count=len(children),
                    daughter_min_separation=min(finite_sep) if finite_sep else float("nan"),
                )

        for c_idx, parents in child_parents.items():
            child_id = int(curr_comps[c_idx]["component_id"])
            if not parents:
                emit_event(
                    out=event_rows,
                    run_ids=run_ids,
                    prev_summary=prev_summary,
                    curr_summary=curr_summary,
                    event_type="birth",
                    parent_ids="",
                    child_ids=[child_id],
                    parent_count=0,
                    child_count=1,
                )
            elif len(parents) > 1:
                parent_ids = [int(prev_comps[p]["component_id"]) for p in parents]
                emit_event(
                    out=event_rows,
                    run_ids=run_ids,
                    prev_summary=prev_summary,
                    curr_summary=curr_summary,
                    event_type="merge",
                    parent_ids=parent_ids,
                    child_ids=[child_id],
                    parent_count=len(parents),
                    child_count=1,
                )

        emit_component_rows(out=component_rows, run_ids=run_ids, comps=curr_comps, snapshot_summary=curr_summary)

    snapshots_meta = [snap["summary"] for snap in snapshots]
    event_by_type: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in event_rows:
        event_by_type[str(row["event_type"])].append(row)

    split_rows = event_by_type.get("split", [])
    merge_rows = event_by_type.get("merge", [])
    birth_rows = event_by_type.get("birth", [])
    death_rows = event_by_type.get("death", [])
    compress_rows = event_by_type.get("compress", [])

    by_component: MutableMapping[int, List[Dict[str, Any]]] = defaultdict(list)
    for row in component_rows:
        by_component[int(row["component_id"])].append(row)
    lifetimes = []
    for rows in by_component.values():
        rows.sort(key=lambda r: (int(r["snapshot_index"]), int(r["step"])))
        lifetimes.append(int(rows[-1]["step"]) - int(rows[0]["step"]))

    counts_by_snapshot = {int(s["snapshot_index"]): int(s["component_count"]) for s in snapshots_meta}
    step_by_snapshot = {int(s["snapshot_index"]): int(s["step"]) for s in snapshots_meta}
    max_component_count = max(counts_by_snapshot.values(), default=0)
    first_split_idx = min((int(r["snapshot_index_to"]) for r in split_rows), default=-1)
    first_split_step = min((int(r["step_to"]) for r in split_rows), default=-1)
    first_birth_step = min((int(r["step_to"]) for r in birth_rows), default=-1)
    first_merge_step = min((int(r["step_to"]) for r in merge_rows), default=-1)

    post_split_dual_duration = -1
    if first_split_idx >= 0:
        active = []
        for idx in range(first_split_idx, len(snapshots_meta)):
            if counts_by_snapshot.get(idx, 0) >= 2:
                active.append(idx)
            elif active:
                break
        if active:
            post_split_dual_duration = step_by_snapshot[active[-1]] - step_by_snapshot[first_split_idx]

    min_daughter_sep = min(
        (safe_float(r["daughter_min_separation"]) for r in split_rows if math.isfinite(safe_float(r["daughter_min_separation"]))),
        default=float("nan"),
    )

    split_count = len(split_rows)
    merge_count = len(merge_rows)
    birth_count = len(birth_rows)
    death_count = len(death_rows)
    compress_count = len(compress_rows)
    churn_count = split_count + merge_count + birth_count + death_count

    if max_component_count <= 1 and churn_count == 0:
        genealogy_pattern = "single_component_stable"
    elif split_count > 0 and post_split_dual_duration >= 3 * LOG_EVERY:
        genealogy_pattern = "split_persistent_dual"
    elif split_count > 0 and birth_count > 0:
        genealogy_pattern = "split_fragment"
    elif merge_count > 0 and split_count > 0:
        genealogy_pattern = "merge_split_churn"
    elif birth_count + death_count >= 4:
        genealogy_pattern = "birth_death_churn"
    elif max_component_count >= 3:
        genealogy_pattern = "multi_component_churn"
    else:
        genealogy_pattern = "heterogeneous_genealogy"

    summary = {
        **run_ids,
        "genealogy_pattern": genealogy_pattern,
        "split_count": int(split_count),
        "merge_count": int(merge_count),
        "birth_count": int(birth_count),
        "death_count": int(death_count),
        "compress_count": int(compress_count),
        "churn_event_count": int(churn_count),
        "first_split_step": int(first_split_step),
        "first_birth_step": int(first_birth_step),
        "first_merge_step": int(first_merge_step),
        "max_component_count": int(max_component_count),
        "mean_component_lifetime": mean_defined(float(x) for x in lifetimes),
        "max_component_lifetime": max(lifetimes) if lifetimes else 0,
        "post_first_split_dual_duration": int(post_split_dual_duration),
        "min_daughter_separation_after_first_split": safe_float(min_daughter_sep),
        "max_total_defect_mass": max((int(s["total_defect_mass"]) for s in snapshots_meta), default=0),
        "mean_total_defect_mass": mean_defined(float(s["total_defect_mass"]) for s in snapshots_meta),
        "final_total_defect_mass": int(snapshots_meta[-1]["total_defect_mass"]) if snapshots_meta else 0,
        "max_largest_component_fraction": max((safe_float(s["largest_component_fraction"]) for s in snapshots_meta), default=0.0),
        "final_component_count": int(snapshots_meta[-1]["component_count"]) if snapshots_meta else 0,
    }
    return component_rows, event_rows, summary


def aggregate_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for target in TARGETS:
        for placement in PLACEMENTS:
            group = [
                row for row in run_rows
                if int(row["target_nodes"]) == int(target) and int(row["placement"]) == int(placement)
            ]
            patterns = Counter(str(row["genealogy_pattern"]) for row in group)
            horizon_group = [
                row for row in group
                if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon"
            ]
            no_horizon_group = [
                row for row in group
                if str(row["far_shell_horizon_label"]) != "established_far_shell_horizon"
            ]
            out.append(
                {
                    "target_nodes": int(target),
                    "profile_label": profile_label(placement),
                    "placement": int(placement),
                    "n_runs": len(group),
                    "established_far_shell_rate": mean_defined(
                        1.0 if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon" else 0.0
                        for row in group
                    ),
                    "mean_high_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group),
                    "dominant_genealogy_pattern": patterns.most_common(1)[0][0] if patterns else "",
                    "genealogy_patterns": ";".join(f"{k}:{v}" for k, v in sorted(patterns.items())),
                    "mean_split_count": mean_defined(safe_float(row["split_count"]) for row in group),
                    "mean_merge_count": mean_defined(safe_float(row["merge_count"]) for row in group),
                    "mean_birth_count": mean_defined(safe_float(row["birth_count"]) for row in group),
                    "mean_death_count": mean_defined(safe_float(row["death_count"]) for row in group),
                    "mean_churn_event_count": mean_defined(safe_float(row["churn_event_count"]) for row in group),
                    "mean_max_component_count": mean_defined(safe_float(row["max_component_count"]) for row in group),
                    "mean_max_total_defect_mass": mean_defined(safe_float(row["max_total_defect_mass"]) for row in group),
                    "mean_final_total_defect_mass": mean_defined(safe_float(row["final_total_defect_mass"]) for row in group),
                    "horizon_patterns": ";".join(sorted({str(row["genealogy_pattern"]) for row in horizon_group})),
                    "no_horizon_patterns": ";".join(sorted({str(row["genealogy_pattern"]) for row in no_horizon_group})),
                    "pattern_separates_outcome": int(
                        bool(horizon_group)
                        and bool(no_horizon_group)
                        and {str(row["genealogy_pattern"]) for row in horizon_group}.isdisjoint(
                            {str(row["genealogy_pattern"]) for row in no_horizon_group}
                        )
                    ),
                }
            )
    return out


def chain_summary_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    groups: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in run_rows:
        groups[str(row["genealogy_pattern"])].append(row)
    out: List[Dict[str, Any]] = []
    for pattern, rows in sorted(groups.items()):
        out.append(
            {
                "genealogy_pattern": pattern,
                "n_runs": len(rows),
                "established_far_shell_rate": mean_defined(
                    1.0 if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon" else 0.0
                    for row in rows
                ),
                "targets": ";".join(sorted({str(int(row["target_nodes"])) for row in rows})),
                "placements": ";".join(sorted({f"p{int(row['placement'])}" for row in rows})),
                "seed_deltas": ";".join(sorted({str(int(row["seed_delta"])) for row in rows})),
                "mean_high_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in rows),
                "mean_churn_event_count": mean_defined(safe_float(row["churn_event_count"]) for row in rows),
                "mean_max_component_count": mean_defined(safe_float(row["max_component_count"]) for row in rows),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    chain_summary: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    by_key = {(int(row["target_nodes"]), int(row["placement"])): row for row in aggregate}
    p1_bridge = (
        safe_float(by_key[(896, 1)]["established_far_shell_rate"]) >= 0.5
        and safe_float(by_key[(1024, 1)]["established_far_shell_rate"]) >= 0.5
    )
    p3_switch = (
        safe_float(by_key[(896, 3)]["established_far_shell_rate"]) == 0.0
        and safe_float(by_key[(1024, 3)]["established_far_shell_rate"]) >= 1.0
    )
    separated_groups = [row for row in aggregate if int(row["pattern_separates_outcome"]) == 1]
    mixed_patterns = [
        row for row in chain_summary
        if 0.0 < safe_float(row["established_far_shell_rate"]) < 1.0
    ]

    if separated_groups:
        separated_labels = ";".join(
            f"{int(row['target_nodes'])}:p{int(row['placement'])}" for row in separated_groups
        )
        genealogy_status = "genealogy_separates_limited_seed_splits"
        genealogy_note = (
            f"{len(separated_groups)} target/placement-grupper ({separated_labels}) har disjunkte genealogy patterns for horizon vs no-horizon."
        )
        next_step = "holdout_p1_1024_genealogy_split_axis"
        next_note = "Neste steg bor holde ut den konkrete p1/1024 genealogy-splitten paa nye seeds foer generalisering."
    elif mixed_patterns:
        genealogy_status = "genealogy_partially_informative_but_not_clean"
        genealogy_note = (
            "Genealogy patterns varierer, men minst ett pattern blander horizon og no-horizon under denne lille n."
        )
        next_step = "increase_p1_p3_genealogy_replicates"
        next_note = "Neste steg bor oke n for p1/p3 genealogy uten aa utvide placement-rommet."
    else:
        genealogy_status = "genealogy_not_informative_here"
        genealogy_note = "Genealogy patterns skiller ikke horizon/no-horizon i denne smale proben."
        next_step = "seek_non_genealogy_observable"
        next_note = "Neste steg bor lete etter en annen observabel enn komponentgenealogi."

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
        {
            "diagnostic_family": "landscape_reproduction",
            "status": "p1_bridge_p3_switch_reproduced" if (p1_bridge and p3_switch) else "landscape_not_fully_reproduced",
            "note": f"p1_bridge={int(p1_bridge)}, p3_switch={int(p3_switch)} under genealogy rerun.",
        },
        {"diagnostic_family": "genealogy_axis", "status": genealogy_status, "note": genealogy_note},
        {"diagnostic_family": "next_step", "status": next_step, "note": next_note},
    ]


def build_report(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    chain_summary: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cw: add_chord p1/p3 genealogy seed split")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden holder v15cv-scope fast og legger til komponentgenealogi per run.")
    lines.append("Far-shell horizon er downstream outcome; primaerdata er component trajectories og event logs.")
    lines.append("")
    lines.append("## Design")
    lines.append("")
    lines.append("| field | value |")
    lines.append("| --- | --- |")
    lines.append(f"| targets | {';'.join(str(x) for x in TARGETS)} |")
    lines.append(f"| placements | {';'.join('p' + str(x) for x in PLACEMENTS)} |")
    lines.append(f"| seed deltas | {';'.join(str(x) for x in SEED_DELTAS)} |")
    lines.append("")
    lines.append("## Startstorrelse")
    lines.append("")
    lines.append("| target | mean initial | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Per-run genealogy")
    lines.append("")
    lines.append("| target | placement | seed | horizon | genealogy pattern | split | birth | death | max comps | max mass |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in run_rows:
        lines.append(
            f"| {int(row['target_nodes'])} | p{int(row['placement'])} | {int(row['seed_delta'])} | {row['far_shell_horizon_label']} | {row['genealogy_pattern']} | {int(row['split_count'])} | {int(row['birth_count'])} | {int(row['death_count'])} | {int(row['max_component_count'])} | {int(row['max_total_defect_mass'])} |"
        )
    lines.append("")
    lines.append("## Aggregate")
    lines.append("")
    lines.append("| target | placement | est | horizon | patterns | separates outcome | mean churn | mean max comps |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['target_nodes'])} | p{int(row['placement'])} | {fmt(row['established_far_shell_rate'])} | {fmt(row['mean_high_horizon_span'])} | {row['genealogy_patterns']} | {int(row['pattern_separates_outcome'])} | {fmt(row['mean_churn_event_count'])} | {fmt(row['mean_max_component_count'])} |"
        )
    lines.append("")
    lines.append("## Chain summary")
    lines.append("")
    lines.append("| pattern | n | est rate | targets | placements | mean horizon | mean churn |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in chain_summary:
        lines.append(
            f"| {row['genealogy_pattern']} | {int(row['n_runs'])} | {fmt(row['established_far_shell_rate'])} | {row['targets']} | {row['placements']} | {fmt(row['mean_high_horizon_span'])} | {fmt(row['mean_churn_event_count'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Genealogy patterns er mekanismeobservabler, ikke partikkelklasser.")
    lines.append("- En positiv separation betyr bare at komponenthistorikk forklarer seed-splits bedre enn statisk supportgeometri.")
    lines.append("- En negativ separation betyr at p1/p3-landskapet fortsatt er ekte, men mekanismen krever annen observabel eller mer n.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15cw", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Dette er en smal add_chord-genealogy-probe, ikke en Lorentz-, invariant- eller partikkelpaastand.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15cw",
        "",
        "Denne runden ser paa historien til skadekomponentene: deler de seg, doer de, smelter de sammen, eller holder de seg samlet?",
        "",
        f"- Landskap: `{diag['landscape_reproduction']['status']}`.",
        f"- Genealogi: `{diag['genealogy_axis']['status']}`.",
        "",
        "Dette sier ikke at vi har funnet partikler. Det tester bare om komponenthistorikk forklarer hvorfor noen runs faar lang hale og andre ikke.",
        "",
        f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cw add_chord p1/p3 genealogy seed split lab.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cw_add_chord_p1_p3_genealogy_target_summary.csv")
    p.add_argument("--out-components-csv", type=str, default="Documentation/v15cw_add_chord_p1_p3_genealogy_component_trajectories.csv")
    p.add_argument("--out-events-csv", type=str, default="Documentation/v15cw_add_chord_p1_p3_genealogy_event_log.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cw_add_chord_p1_p3_genealogy_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cw_add_chord_p1_p3_genealogy_aggregate.csv")
    p.add_argument("--out-chain-csv", type=str, default="Documentation/v15cw_add_chord_p1_p3_genealogy_chain_summary.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cw_add_chord_p1_p3_genealogy_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cw_add_chord_p1_p3_genealogy_seed_split.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cw_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cw.md")
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

    component_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []
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
                base_dist = v7.bfs_distances(base_state.g, support)
                fallback = (max(base_dist.values()) + 1) if base_dist else 1
                snapshot_rows = v15cv.snapshot_rows_for_run(
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
                recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
                final_drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                support_features = v15cv.support_mechanism_features(
                    target=target,
                    base_state=base_state,
                    placement=placement,
                    seed_delta=seed_delta,
                    run_seed=run_seed,
                    support=support,
                )
                mechanism_row = v15cv.run_summary_row(
                    target=target,
                    placement=placement,
                    seed_delta=seed_delta,
                    run_seed=run_seed,
                    requested_match=int(v15.v14.perturbation_requested_match(PERTURBATION, str(info.get("type", "unknown")))),
                    support_signature=support_signature,
                    support_features=support_features,
                    recurrence=recurrence,
                    final_drift=final_drift,
                    snapshot_rows=snapshot_rows,
                )
                run_ids = {
                    "target_nodes": int(target),
                    "growth_seed": GROWTH_SEED,
                    "profile_label": profile_label(placement),
                    "perturbation": PERTURBATION,
                    "placement": int(placement),
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "support_signature": support_signature,
                }
                comps, events, genealogy_summary = genealogy_for_run(
                    run_ids=run_ids,
                    log_rows=res["log_rows"],
                    damaged_sets=res["damaged_sets"],
                    control_graphs=res["control_graphs"],
                    support=support,
                )
                component_rows.extend(comps)
                event_rows.extend(events)
                run_rows.append({**mechanism_row, **genealogy_summary})

    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) in TARGETS]
    aggregate = aggregate_rows(run_rows)
    chain_summary = chain_summary_rows(run_rows)
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        aggregate=aggregate,
        chain_summary=chain_summary,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_components_csv, component_rows)
    write_csv(args.out_events_csv, event_rows)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_chain_csv, chain_summary)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            target_summary=target_summary,
            run_rows=run_rows,
            aggregate=aggregate,
            chain_summary=chain_summary,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
