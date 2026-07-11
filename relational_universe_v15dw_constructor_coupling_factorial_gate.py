#!/usr/bin/env python3
"""v0.15dw constructor x coupling factorial gate.

Fresh dynamic gate after v15du/v15dv.

Factors:
- constructor: legacy_first_sorted vs uniform_relabel_invariant
- coupling: maximal vs rank

The experiment keeps target, regime, perturbation family, placements, base
growth seeds, step budget, and run seeds paired. Constructor randomness uses a
separate RNG so uniform candidate selection does not shift the dynamic random
stream. Assignments are written before the dynamic loop.

This is an artifact/coupling robustness gate for the local add_chord response.
It is not evidence for particles, Lorentz invariance, entanglement, global
invariants, or universal geometry.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15cn_p2_horizon_scale_holdout as v15cn
import relational_universe_v15cs_add_chord_p0_scale_response_holdout as v15cs
import relational_universe_v15q_single_defect_recurrence_lab as v15q
import relational_universe_v15dv_relabel_invariant_chord_constructor as v15dv


DOC = Path("Documentation")

TARGET_NODES = 1024
GROWTH_SEEDS = (202, 303)
PLACEMENTS = (0, 1, 2)
CONSTRUCTORS = ("legacy_first_sorted", "uniform_relabel_invariant")
COUPLINGS = ("maximal", "rank")
FRESH_SEED_DELTAS = (19511, 19571, 19633, 19697)
STEPS = v15cs.scaled_steps_for_target(TARGET_NODES)
LOG_EVERY = 8
ACTIVE_ESTABLISHED_RATE = 0.50

MIN_CELL_LABEL_AGREEMENT = 0.80
MAX_MEDIAN_ESTABLISHED_RATE_GAP = 0.20
MAX_MEDIAN_NORMALIZED_HORIZON_GAP = 0.15

Chord = Tuple[int, int, int]


def safe_float(value: Any, default: float = float("nan")) -> float:
    return v15.safe_float(value, default)


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def safe_div(numerator: float, denominator: float) -> float:
    if not math.isfinite(numerator) or not math.isfinite(denominator) or denominator == 0.0:
        return float("nan")
    return numerator / denominator


def mean_defined(values: Iterable[Any]) -> float:
    vals = [safe_float(value) for value in values]
    finite = [value for value in vals if math.isfinite(value)]
    return sum(finite) / len(finite) if finite else float("nan")


def median_defined(values: Iterable[Any]) -> float:
    vals = sorted(value for value in (safe_float(item) for item in values) if math.isfinite(value))
    if not vals:
        return float("nan")
    mid = len(vals) // 2
    if len(vals) % 2:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2.0


def fmt(value: Any, digits: int = 3) -> str:
    numeric = safe_float(value)
    if not math.isfinite(numeric):
        return "nan"
    return f"{numeric:.{digits}f}"


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]], *, empty_fieldnames: Sequence[str] = ()) -> None:
    target = Path(path)
    records = list(rows)
    if not records:
        with target.open("w", newline="", encoding="utf-8") as handle:
            if empty_fieldnames:
                csv.DictWriter(handle, fieldnames=list(empty_fieldnames)).writeheader()
        return
    fieldnames: List[str] = []
    for row in records:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    if not rows:
        return ["No rows."]
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values: List[str] = []
        for field in fields:
            value = row.get(field, "")
            values.append(fmt(value) if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return lines


def chord_text(chord: Chord) -> str:
    return "-".join(str(int(node)) for node in chord)


def parse_chord(text: str) -> Chord:
    parts = tuple(int(part) for part in str(text).split("-") if part != "")
    if len(parts) != 3:
        raise ValueError(f"invalid chord {text!r}")
    return parts  # type: ignore[return-value]


def run_seed_for(*, growth_seed: int, placement: int, seed_delta: int) -> int:
    return (
        TARGET_NODES * 1_000_000
        + int(growth_seed) * 10_000
        + int(placement) * 1_000
        + int(seed_delta)
        + 1913
    )


def constructor_seed_for(*, growth_seed: int, placement: int, seed_delta: int) -> int:
    return (
        15_000_000_000
        + int(growth_seed) * 100_000
        + int(placement) * 10_000
        + int(seed_delta)
    )


def build_bases() -> Tuple[Dict[int, Any], List[Mapping[str, Any]], List[Mapping[str, Any]]]:
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    states = {seed: base_states[(ensembles[0].name, seed)] for seed in GROWTH_SEEDS}
    base_by_seed = {
        seed: next(
            row
            for row in base_rows
            if int(row["growth_seed"]) == seed and int(row["target_nodes"]) == TARGET_NODES
        )
        for seed in GROWTH_SEEDS
    }
    target_summary = [
        dict(row)
        for row in v10e.summarize_bases(base_rows)
        if int(row["target_nodes"]) == TARGET_NODES
    ]
    return states, [base_by_seed[seed] for seed in GROWTH_SEEDS], target_summary


def assignment_rows(base_states: Mapping[int, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for growth_seed in GROWTH_SEEDS:
        state = base_states[growth_seed]
        for placement in PLACEMENTS:
            legacy = v08b.find_chord_candidate(state, center_token_index=placement)
            if legacy is None:
                raise ValueError(f"missing legacy chord for growth_seed={growth_seed}, placement={placement}")
            distribution, candidate_scope, selected_token_id = v15dv.chord_distribution(state, placement)
            for seed_delta in FRESH_SEED_DELTAS:
                constructor_seed = constructor_seed_for(
                    growth_seed=growth_seed,
                    placement=placement,
                    seed_delta=seed_delta,
                )
                uniform, metadata = v15dv.sample_uniform_chord_candidate(
                    state,
                    placement,
                    random.Random(constructor_seed),
                )
                rows.append(
                    {
                        "target_nodes": TARGET_NODES,
                        "growth_seed": growth_seed,
                        "placement": placement,
                        "seed_delta": seed_delta,
                        "run_seed": run_seed_for(
                            growth_seed=growth_seed,
                            placement=placement,
                            seed_delta=seed_delta,
                        ),
                        "constructor_seed": constructor_seed,
                        "selected_token_id": selected_token_id,
                        "candidate_scope": candidate_scope,
                        "candidate_count": len(distribution),
                        "legacy_candidate": chord_text(legacy),
                        "uniform_candidate": chord_text(uniform),
                        "uniform_matches_legacy": int(tuple(uniform) == tuple(legacy)),
                        "uniform_selection_policy": metadata["selection_policy"],
                        "pre_registered_before_dynamics": 1,
                    }
                )
    return rows


def apply_candidate(state: Any, candidate: Chord, constructor: str) -> Dict[str, Any]:
    source, bridge, target = (int(node) for node in candidate)
    if not state.g.has_edge(source, bridge) or not state.g.has_edge(bridge, target):
        raise ValueError(f"candidate path missing for {candidate}")
    if state.g.has_edge(source, target):
        raise ValueError(f"candidate chord already exists for {candidate}")
    state.g.add_edge(source, target)
    return {
        "type": "local_chord_anywhere" if constructor == "legacy_first_sorted" else "local_chord_uniform_token_rooted",
        "support": sorted({source, bridge, target}),
        "ordered_candidate": candidate,
        "delta_core": {"tokens": 0, "nodes": 0, "components": 0, "beta1": 1},
    }


def lean_snapshot(control: Any, perturbed: Any, support: Sequence[int]) -> Tuple[Dict[str, Any], Set[int]]:
    damaged = v7.damaged_nodes(control, perturbed)
    edge_diff = v7.edge_symmetric_difference(control, perturbed)
    radius_control = v7.radius_from_support(control.g, support, damaged)
    radius_perturbed = v7.radius_from_support(perturbed.g, support, damaged)
    components = v15.damaged_components(control.g, damaged)
    largest = max((len(component) for component in components), default=0)
    boundary = v15.boundary_edge_count(control.g, damaged)
    shared_tokens = set(control.token_pos).intersection(perturbed.token_pos)
    token_union = set(control.token_pos).union(perturbed.token_pos)
    shared_nodes = set(control.g.nodes()).intersection(perturbed.g.nodes())
    node_union = set(control.g.nodes()).union(perturbed.g.nodes())
    return (
        {
            "edge_diff_count": len(edge_diff),
            "damaged_nodes_count": len(damaged),
            "radius_control": -1 if radius_control is None else int(radius_control),
            "radius_perturbed": -1 if radius_perturbed is None else int(radius_perturbed),
            "damage_component_count": len(components),
            "largest_component_fraction": safe_div(largest, len(damaged)) if damaged else 0.0,
            "boundary_edge_count": boundary,
            "boundary_to_volume": safe_div(boundary, len(damaged)) if damaged else 0.0,
            "alive": int(bool(damaged)),
            "state_equal": int(v7.states_equal(control, perturbed)),
            "token_shared_fraction": safe_div(len(shared_tokens), len(token_union)) if token_union else 1.0,
            "node_shared_fraction": safe_div(len(shared_nodes), len(node_union)) if node_union else 1.0,
            "control_nodes": control.g.num_nodes(),
            "perturbed_nodes": perturbed.g.num_nodes(),
            "control_edges": control.g.num_edges(),
            "perturbed_edges": perturbed.g.num_edges(),
            "control_tokens": control.token_count(),
            "perturbed_tokens": perturbed.token_count(),
        },
        set(damaged),
    )


def final_marginal_fields(base_state: Any, control: Any, perturbed: Any) -> Dict[str, Any]:
    base_components = v7.count_components(base_state.g)
    control_components = v7.count_components(control.g)
    perturbed_components = v7.count_components(perturbed.g)
    base_beta1 = base_state.g.num_edges() - base_state.g.num_nodes() + base_components
    control_beta1 = control.g.num_edges() - control.g.num_nodes() + control_components
    perturbed_beta1 = perturbed.g.num_edges() - perturbed.g.num_nodes() + perturbed_components
    return {
        "base_nodes": base_state.g.num_nodes(),
        "base_edges": base_state.g.num_edges(),
        "base_tokens": base_state.token_count(),
        "base_components": base_components,
        "base_beta1": base_beta1,
        "final_control_nodes": control.g.num_nodes(),
        "final_control_edges": control.g.num_edges(),
        "final_control_tokens": control.token_count(),
        "final_control_components": control_components,
        "final_control_beta1": control_beta1,
        "final_perturbed_nodes": perturbed.g.num_nodes(),
        "final_perturbed_edges": perturbed.g.num_edges(),
        "final_perturbed_tokens": perturbed.token_count(),
        "final_perturbed_components": perturbed_components,
        "final_perturbed_beta1": perturbed_beta1,
        "control_node_drift_rel": safe_div(control.g.num_nodes() - base_state.g.num_nodes(), base_state.g.num_nodes()),
        "perturbed_node_drift_rel": safe_div(perturbed.g.num_nodes() - base_state.g.num_nodes(), base_state.g.num_nodes()),
        "control_edge_drift_rel": safe_div(control.g.num_edges() - base_state.g.num_edges(), base_state.g.num_edges()),
        "perturbed_edge_drift_rel": safe_div(perturbed.g.num_edges() - base_state.g.num_edges(), base_state.g.num_edges()),
        "control_beta1_drift_rel": safe_div(control_beta1 - base_beta1, max(1, abs(base_beta1))),
        "perturbed_beta1_drift_rel": safe_div(perturbed_beta1 - base_beta1, max(1, abs(base_beta1))),
        "control_token_drift_rel": safe_div(control.token_count() - base_state.token_count(), max(1, base_state.token_count())),
        "perturbed_token_drift_rel": safe_div(perturbed.token_count() - base_state.token_count(), max(1, base_state.token_count())),
    }


def flatten_coupling_summary(summary: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "coupling_total_events": safe_int(summary.get("total_potential_events")),
        "coupling_both_accept_total": safe_int(summary.get("both_accept_total")),
        "coupling_one_sided_total": safe_int(summary.get("one_sided_total")),
        "coupling_null_total": safe_int(summary.get("null_total")),
        "coupling_avg_local_overlap_both_accept": safe_float(summary.get("avg_local_overlap_both_accept")),
        "coupling_avg_same_descriptor_both_accept": safe_float(summary.get("avg_same_descriptor_both_accept")),
    }


def run_factor_cell(
    *,
    base_state: Any,
    assignment: Mapping[str, Any],
    constructor: str,
    coupling: str,
    params: Any,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    growth_seed = safe_int(assignment["growth_seed"])
    placement = safe_int(assignment["placement"])
    seed_delta = safe_int(assignment["seed_delta"])
    run_seed = safe_int(assignment["run_seed"])
    candidate_field = "legacy_candidate" if constructor == "legacy_first_sorted" else "uniform_candidate"
    candidate = parse_chord(str(assignment[candidate_field]))

    control = base_state.clone()
    perturbed = base_state.clone()
    perturbation_info = apply_candidate(perturbed, candidate, constructor)
    support = [int(node) for node in perturbation_info["support"]]
    support_signature = ",".join(str(node) for node in support)
    next_node_id, next_token_id = v08b.next_ids_from_state(base_state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)
    rng = random.Random(run_seed)

    log_rows: List[Dict[str, Any]] = []
    damaged_sets: List[Set[int]] = []
    event_rows: List[Dict[str, Any]] = []

    snapshot0, damaged0 = lean_snapshot(control, perturbed, support)
    log_rows.append({"step": 0, "t": 0.0, **snapshot0})
    damaged_sets.append(damaged0)
    for step in range(1, STEPS + 1):
        event = v7.coupled_step(control, perturbed, manager, rng, params, coupling)
        event_rows.append(event)
        if step % LOG_EVERY == 0 or step == STEPS:
            snapshot, damaged = lean_snapshot(control, perturbed, support)
            log_rows.append({"step": step, "t": control.t, **snapshot})
            damaged_sets.append(damaged)

    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(log_rows))))
    tail_series = v15cn.raw_far_shell_tail_series(base_state, support, damaged_sets[tail_start:])
    horizon = v15cn.horizon_fields(tail_series)
    normalized_horizon_span = safe_div(
        safe_float(horizon["high_horizon_span"]),
        safe_float(horizon["tail_snapshot_count"]),
    )
    coupling_summary = flatten_coupling_summary(v7.summarize_events(event_rows))
    marginal = final_marginal_fields(base_state, control, perturbed)

    snapshot_rows: List[Dict[str, Any]] = []
    for snapshot_index, row in enumerate(log_rows):
        snapshot_rows.append(
            {
                "target_nodes": TARGET_NODES,
                "growth_seed": growth_seed,
                "placement": placement,
                "seed_delta": seed_delta,
                "run_seed": run_seed,
                "constructor": constructor,
                "coupling": coupling,
                "candidate": chord_text(candidate),
                "support_signature": support_signature,
                "snapshot_index": snapshot_index,
                **row,
            }
        )

    run_row = {
        "target_nodes": TARGET_NODES,
        "growth_seed": growth_seed,
        "placement": placement,
        "seed_delta": seed_delta,
        "run_seed": run_seed,
        "constructor_seed": safe_int(assignment["constructor_seed"]),
        "constructor": constructor,
        "coupling": coupling,
        "candidate": chord_text(candidate),
        "legacy_candidate": assignment["legacy_candidate"],
        "uniform_candidate": assignment["uniform_candidate"],
        "uniform_matches_legacy": safe_int(assignment["uniform_matches_legacy"]),
        "candidate_count": safe_int(assignment["candidate_count"]),
        "support_signature": support_signature,
        "actual_perturbation": perturbation_info["type"],
        "requested_match": 1,
        "step_budget": STEPS,
        "log_every": LOG_EVERY,
        "final_time": safe_float(log_rows[-1]["t"]),
        "mean_damage_fraction": mean_defined(safe_div(row["damaged_nodes_count"], TARGET_NODES) for row in log_rows),
        "max_damage_fraction": max(safe_div(safe_float(row["damaged_nodes_count"]), TARGET_NODES) for row in log_rows),
        "mean_radius_control": mean_defined(row["radius_control"] for row in log_rows if safe_float(row["radius_control"]) >= 0),
        "max_radius_control": max((safe_float(row["radius_control"]) for row in log_rows if safe_float(row["radius_control"]) >= 0), default=-1.0),
        "mean_component_count": mean_defined(row["damage_component_count"] for row in log_rows),
        "mean_boundary_to_volume": mean_defined(row["boundary_to_volume"] for row in log_rows),
        "final_alive": safe_int(log_rows[-1]["alive"]),
        "mean_far_shell_share": mean_defined(row["far_shell_share"] for row in tail_series),
        "mean_weighted_mean_distance": mean_defined(row["weighted_mean_distance"] for row in tail_series),
        "normalized_horizon_span": normalized_horizon_span,
        **horizon,
        **coupling_summary,
        **marginal,
    }
    return snapshot_rows, run_row


def cell_summary_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[int, int, str, str], List[Mapping[str, Any]]] = defaultdict(list)
    for row in run_rows:
        grouped[
            (
                safe_int(row["growth_seed"]),
                safe_int(row["placement"]),
                str(row["constructor"]),
                str(row["coupling"]),
            )
        ].append(row)
    out: List[Dict[str, Any]] = []
    for (growth_seed, placement, constructor, coupling), group in sorted(grouped.items()):
        labels = Counter(str(row["far_shell_horizon_label"]) for row in group)
        established_rate = safe_div(labels.get("established_far_shell_horizon", 0), len(group))
        out.append(
            {
                "growth_seed": growth_seed,
                "placement": placement,
                "constructor": constructor,
                "coupling": coupling,
                "n_runs": len(group),
                "label_counts": ";".join(f"{key}:{labels[key]}" for key in sorted(labels)),
                "established_rate": established_rate,
                "active_cell": int(established_rate >= ACTIVE_ESTABLISHED_RATE),
                "mean_normalized_horizon_span": mean_defined(row["normalized_horizon_span"] for row in group),
                "median_normalized_horizon_span": median_defined(row["normalized_horizon_span"] for row in group),
                "mean_high_retention_rate": mean_defined(row["high_retention_rate"] for row in group),
                "mean_far_shell_share": mean_defined(row["mean_far_shell_share"] for row in group),
                "mean_damage_fraction": mean_defined(row["mean_damage_fraction"] for row in group),
                "mean_control_node_drift_rel": mean_defined(row["control_node_drift_rel"] for row in group),
                "mean_perturbed_node_drift_rel": mean_defined(row["perturbed_node_drift_rel"] for row in group),
                "mean_control_edge_drift_rel": mean_defined(row["control_edge_drift_rel"] for row in group),
                "mean_perturbed_edge_drift_rel": mean_defined(row["perturbed_edge_drift_rel"] for row in group),
                "mean_control_beta1_drift_rel": mean_defined(row["control_beta1_drift_rel"] for row in group),
                "mean_perturbed_beta1_drift_rel": mean_defined(row["perturbed_beta1_drift_rel"] for row in group),
                "mean_coupling_overlap": mean_defined(row["coupling_avg_local_overlap_both_accept"] for row in group),
                "mean_same_descriptor_rate": mean_defined(row["coupling_avg_same_descriptor_both_accept"] for row in group),
            }
        )
    return out


def compare_factor(
    cells: Sequence[Mapping[str, Any]],
    *,
    factor: str,
    level_a: str,
    level_b: str,
    fixed_factor: str,
    fixed_level: str,
) -> Dict[str, Any]:
    subset = [row for row in cells if str(row[fixed_factor]) == fixed_level]
    by_key = {
        (safe_int(row["growth_seed"]), safe_int(row["placement"]), str(row[factor])): row
        for row in subset
    }
    pairs: List[Tuple[Mapping[str, Any], Mapping[str, Any]]] = []
    for growth_seed in GROWTH_SEEDS:
        for placement in PLACEMENTS:
            pairs.append(
                (
                    by_key[(growth_seed, placement, level_a)],
                    by_key[(growth_seed, placement, level_b)],
                )
            )
    label_agreement = mean_defined(int(safe_int(a["active_cell"]) == safe_int(b["active_cell"])) for a, b in pairs)
    established_gaps = [abs(safe_float(a["established_rate"]) - safe_float(b["established_rate"])) for a, b in pairs]
    horizon_gaps = [
        abs(safe_float(a["mean_normalized_horizon_span"]) - safe_float(b["mean_normalized_horizon_span"]))
        for a, b in pairs
    ]
    node_gaps = [
        abs(safe_float(a["mean_perturbed_node_drift_rel"]) - safe_float(b["mean_perturbed_node_drift_rel"]))
        for a, b in pairs
    ]
    beta1_gaps = [
        abs(safe_float(a["mean_perturbed_beta1_drift_rel"]) - safe_float(b["mean_perturbed_beta1_drift_rel"]))
        for a, b in pairs
    ]
    median_established_gap = median_defined(established_gaps)
    median_horizon_gap = median_defined(horizon_gaps)
    passes = (
        label_agreement >= MIN_CELL_LABEL_AGREEMENT
        and median_established_gap <= MAX_MEDIAN_ESTABLISHED_RATE_GAP
        and median_horizon_gap <= MAX_MEDIAN_NORMALIZED_HORIZON_GAP
    )
    return {
        "effect": f"{factor}_effect",
        "fixed_factor": fixed_factor,
        "fixed_level": fixed_level,
        "level_a": level_a,
        "level_b": level_b,
        "n_paired_cells": len(pairs),
        "cell_label_agreement": label_agreement,
        "majority_flip_count": sum(safe_int(a["active_cell"]) != safe_int(b["active_cell"]) for a, b in pairs),
        "median_absolute_established_rate_gap": median_established_gap,
        "max_absolute_established_rate_gap": max(established_gaps),
        "median_absolute_normalized_horizon_gap": median_horizon_gap,
        "max_absolute_normalized_horizon_gap": max(horizon_gaps),
        "median_absolute_perturbed_node_drift_gap": median_defined(node_gaps),
        "median_absolute_perturbed_beta1_drift_gap": median_defined(beta1_gaps),
        "factor_gate_pass": int(passes),
        "factor_status": "stable_under_factor" if passes else "factor_sensitive",
    }


def factor_comparison_rows(cells: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for coupling in COUPLINGS:
        rows.append(
            compare_factor(
                cells,
                factor="constructor",
                level_a="legacy_first_sorted",
                level_b="uniform_relabel_invariant",
                fixed_factor="coupling",
                fixed_level=coupling,
            )
        )
    for constructor in CONSTRUCTORS:
        rows.append(
            compare_factor(
                cells,
                factor="coupling",
                level_a="maximal",
                level_b="rank",
                fixed_factor="constructor",
                fixed_level=constructor,
            )
        )
    return rows


def evaluation_rows(
    *,
    assignments: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
    target_summary: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    constructor_rows = [row for row in comparisons if row["effect"] == "constructor_effect"]
    coupling_rows = [row for row in comparisons if row["effect"] == "coupling_effect"]
    constructor_pass = int(all(safe_int(row["factor_gate_pass"]) == 1 for row in constructor_rows))
    coupling_pass = int(all(safe_int(row["factor_gate_pass"]) == 1 for row in coupling_rows))
    size_clean = int(all(safe_int(row.get("separated_from_prev")) == 1 for row in target_summary))
    requested_clean = int(all(safe_int(row["requested_match"]) == 1 for row in run_rows))
    assignment_match_rate = mean_defined(row["uniform_matches_legacy"] for row in assignments)

    if constructor_pass and coupling_pass:
        diagnosis = "response_signal_factorially_stable_candidate"
        next_step = "fresh_scale_or_rule_ablation_with_uniform_constructor"
    elif constructor_pass and not coupling_pass:
        diagnosis = "damage_response_coupling_sensitive"
        next_step = "retire_joint_damage_as_physics_observable_and_test_marginal_branches"
    elif not constructor_pass and coupling_pass:
        diagnosis = "legacy_constructor_materially_shapes_response"
        next_step = "retire_legacy_placement_landscape_and_rebuild_with_uniform_constructor"
    else:
        diagnosis = "response_not_factorially_robust"
        next_step = "stop_far_shell_physics_interpretation_and_return_to_marginal_observables"

    return [
        {
            "key": "scope",
            "value": "fresh_constructor_by_coupling_factorial",
            "evidence": f"runs={len(run_rows)}; growth_seeds={len(GROWTH_SEEDS)}; placements={len(PLACEMENTS)}; seed_deltas={len(FRESH_SEED_DELTAS)}",
        },
        {
            "key": "artifact_control",
            "value": "clean" if size_clean and requested_clean else "unclear",
            "evidence": f"target_separated={size_clean}; requested_match={requested_clean}",
        },
        {
            "key": "uniform_matches_legacy_assignment_rate",
            "value": fmt(assignment_match_rate),
            "evidence": "constructor effect is informative only when uniform sampling often selects a different valid chord",
        },
        {
            "key": "constructor_gate",
            "value": "pass" if constructor_pass else "fail",
            "evidence": ";".join(
                f"{row['fixed_level']}:agree={fmt(row['cell_label_agreement'])},est_gap={fmt(row['median_absolute_established_rate_gap'])},horizon_gap={fmt(row['median_absolute_normalized_horizon_gap'])}"
                for row in constructor_rows
            ),
        },
        {
            "key": "coupling_gate",
            "value": "pass" if coupling_pass else "fail",
            "evidence": ";".join(
                f"{row['fixed_level']}:agree={fmt(row['cell_label_agreement'])},est_gap={fmt(row['median_absolute_established_rate_gap'])},horizon_gap={fmt(row['median_absolute_normalized_horizon_gap'])}"
                for row in coupling_rows
            ),
        },
        {
            "key": "diagnosis",
            "value": diagnosis,
            "evidence": "allOf(constructor robustness, coupling robustness) with fixed thresholds",
        },
        {
            "key": "next_step",
            "value": next_step,
            "evidence": "deduced from failed or satisfied factor gates; no selector refit",
        },
    ]


def claim_ledger_rows(evaluation: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_key = {str(row["key"]): str(row["value"]) for row in evaluation}
    return [
        {
            "claim_id": "claim.v15dw.constructor-robust",
            "claim_type": "statistical",
            "strength": "moderated",
            "statement": "The target-1024 add_chord response is robust to legacy versus uniform relabel-invariant constructor policy.",
            "evaluation": "supported" if by_key["constructor_gate"] == "pass" else "contradicted",
            "evidence_ref": "v15dw_factor_comparisons.csv:constructor_effect",
        },
        {
            "claim_id": "claim.v15dw.coupling-robust",
            "claim_type": "statistical",
            "strength": "moderated",
            "statement": "The target-1024 add_chord damage/horizon response is robust to maximal versus rank coupling.",
            "evaluation": "supported" if by_key["coupling_gate"] == "pass" else "contradicted",
            "evidence_ref": "v15dw_factor_comparisons.csv:coupling_effect",
        },
        {
            "claim_id": "claim.v15dw.factorially-robust-response",
            "claim_type": "project_capability",
            "strength": "moderated",
            "statement": "The current far-shell response is robust enough to justify the next physics-facing gate.",
            "evaluation": "supported" if by_key["diagnosis"] == "response_signal_factorially_stable_candidate" else "unsupported",
            "evidence_ref": "v15dw_factorial_evaluation.csv:diagnosis",
        },
    ]


def render_report(
    *,
    cells: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
    evaluation: Sequence[Mapping[str, Any]],
    claims: Sequence[Mapping[str, Any]],
) -> str:
    by_key = {str(row["key"]): row for row in evaluation}
    max_median_node_gap = max(
        float(row["median_absolute_perturbed_node_drift_gap"]) for row in comparisons
    )
    max_median_beta1_gap = max(
        float(row["median_absolute_perturbed_beta1_drift_gap"]) for row in comparisons
    )
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dw: constructor x coupling factorial gate")
    lines.append("")
    lines.append("## Formaal og maal")
    lines.append("")
    lines.append("`purposeRef`: `purpose://prompt.unknown`.")
    lines.append("Candidate intake: avgjoer om target-1024 add_chord response overlever baade en relabel-invariant perturbation policy og et alternativt korrekt stochastic coupling.")
    lines.append("")
    lines.append("| goal | metric | target | status |")
    lines.append("| --- | --- | --- | --- |")
    lines.append(f"| G1 constructor robustness | cell agreement, established gap, normalized horizon gap | >= {MIN_CELL_LABEL_AGREEMENT:.2f}, <= {MAX_MEDIAN_ESTABLISHED_RATE_GAP:.2f}, <= {MAX_MEDIAN_NORMALIZED_HORIZON_GAP:.2f} | {by_key['constructor_gate']['value']} |")
    lines.append(f"| G2 coupling robustness | same three frozen metrics | >= {MIN_CELL_LABEL_AGREEMENT:.2f}, <= {MAX_MEDIAN_ESTABLISHED_RATE_GAP:.2f}, <= {MAX_MEDIAN_NORMALIZED_HORIZON_GAP:.2f} | {by_key['coupling_gate']['value']} |")
    lines.append(f"| G3 next decision | allOf(G1,G2) | documented diagnosis | {by_key['diagnosis']['value']} |")
    lines.append("")
    lines.append("## Frozen scope")
    lines.append("")
    lines.append(f"- target: `{TARGET_NODES}`")
    lines.append(f"- growth seeds: `{';'.join(str(seed) for seed in GROWTH_SEEDS)}`")
    lines.append(f"- placements: `{';'.join(f'p{placement}' for placement in PLACEMENTS)}`")
    lines.append(f"- fresh seed deltas: `{';'.join(str(seed) for seed in FRESH_SEED_DELTAS)}`")
    lines.append(f"- constructors: `{';'.join(CONSTRUCTORS)}`")
    lines.append(f"- couplings: `{';'.join(COUPLINGS)}`")
    lines.append(f"- step budget: `{STEPS}`; log every `{LOG_EVERY}`")
    lines.append("- constructor RNG is separate from dynamic RNG; assignments were written before dynamics")
    lines.append("")
    lines.append("## Cell outcomes")
    lines.append("")
    lines.extend(
        table(
            cells,
            (
                "growth_seed",
                "placement",
                "constructor",
                "coupling",
                "n_runs",
                "label_counts",
                "established_rate",
                "active_cell",
                "mean_normalized_horizon_span",
                "mean_far_shell_share",
                "mean_perturbed_node_drift_rel",
                "mean_perturbed_beta1_drift_rel",
            ),
        )
    )
    lines.append("")
    lines.append("## Factor gates")
    lines.append("")
    lines.extend(
        table(
            comparisons,
            (
                "effect",
                "fixed_level",
                "n_paired_cells",
                "cell_label_agreement",
                "majority_flip_count",
                "median_absolute_established_rate_gap",
                "median_absolute_normalized_horizon_gap",
                "median_absolute_perturbed_node_drift_gap",
                "median_absolute_perturbed_beta1_drift_gap",
                "factor_status",
            ),
        )
    )
    lines.append("")
    lines.append("## Claim adjudication")
    lines.append("")
    lines.extend(table(claims, ("claim_id", "statement", "evaluation", "evidence_ref")))
    lines.append("")
    lines.append("Root composition: `allOf(constructor robustness, coupling robustness)`. A failed premise makes the root unsupported; it does not prove that all local dynamics are trivial.")
    lines.append("")
    lines.append("## Evidential separation")
    lines.append("")
    lines.append(
        "The joint damage/far-shell classification is factor-sensitive, while the factor contrasts keep "
        f"the largest median perturbed-node drift gap at `{max_median_node_gap:.6f}` and the largest "
        f"median perturbed-beta1 drift gap at `{max_median_beta1_gap:.6f}`."
    )
    lines.append("")
    lines.append(
        "This is evidence against treating the present far-shell observable as a robust physics-facing "
        "signal. It is not evidence that the marginal graph dynamics are identical, trivial, symmetric, "
        "or universe-like; those are separate claims requiring separately preregistered observables."
    )
    lines.append("")
    lines.append("## Decision")
    lines.append("")
    lines.extend(table(evaluation, ("key", "value", "evidence")))
    lines.append("")
    lines.append("Marginal branch drifts are reported separately from joint damage. Constructor hygiene and coupling robustness are necessary artifact gates, not sufficient evidence for physical symmetry or a universe-like law.")
    lines.append("")
    return "\n".join(lines)


def render_operational(evaluation: Sequence[Mapping[str, Any]]) -> str:
    by_key = {str(row["key"]): row for row in evaluation}
    return "\n".join(
        [
            "# Operativ anbefaling v0.15dw",
            "",
            f"- `artifact_control`: `{by_key['artifact_control']['value']}`.",
            f"- `constructor_gate`: `{by_key['constructor_gate']['value']}`.",
            f"- `coupling_gate`: `{by_key['coupling_gate']['value']}`.",
            f"- `diagnosis`: `{by_key['diagnosis']['value']}`.",
            f"- `next_step`: `{by_key['next_step']['value']}`.",
            "",
            "Ikke refit placement-selector eller symmetry-labels fra denne runden.",
            "Pensjoner far-shell/joint-damage som physics-facing observabel i denne formen; ikke pensjoner hele dynamikken.",
            "Neste gate maa preregistrere en marginal grenobservabel som ikke avhenger av kontrollkoblingen.",
            "Et factor-gate pass er bare tillatelse til neste avgrensede test, ikke en physics claim.",
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reuse-existing", action="store_true", help="Regenerate aggregates/reports from existing run and assignment CSVs.")
    parser.add_argument("--out-pre-registration-csv", default=str(DOC / "v15dw_constructor_coupling_pre_registration.csv"))
    parser.add_argument("--out-snapshots-csv", default=str(DOC / "v15dw_constructor_coupling_snapshots.csv"))
    parser.add_argument("--out-runs-csv", default=str(DOC / "v15dw_constructor_coupling_runs.csv"))
    parser.add_argument("--out-cells-csv", default=str(DOC / "v15dw_constructor_coupling_cells.csv"))
    parser.add_argument("--out-comparisons-csv", default=str(DOC / "v15dw_factor_comparisons.csv"))
    parser.add_argument("--out-evaluation-csv", default=str(DOC / "v15dw_factorial_evaluation.csv"))
    parser.add_argument("--out-claims-csv", default=str(DOC / "v15dw_factorial_claim_ledger.csv"))
    parser.add_argument("--out-target-csv", default=str(DOC / "v15dw_target_summary.csv"))
    parser.add_argument("--out-report", default=str(DOC / "v15dw_constructor_coupling_factorial_gate.md"))
    parser.add_argument("--out-operational", default=str(DOC / "v0_15dw_operativ_anbefaling.md"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.reuse_existing:
        assignments = read_csv(args.out_pre_registration_csv)
        run_rows = read_csv(args.out_runs_csv)
        target_summary = read_csv(args.out_target_csv)
    else:
        base_states, _, target_summary = build_bases()
        assignments = assignment_rows(base_states)
        write_csv(args.out_pre_registration_csv, assignments)
        write_csv(args.out_target_csv, target_summary)
        assignment_by_key = {
            (safe_int(row["growth_seed"]), safe_int(row["placement"]), safe_int(row["seed_delta"])): row
            for row in assignments
        }
        params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
        snapshots: List[Dict[str, Any]] = []
        run_rows: List[Dict[str, Any]] = []
        total_runs = len(GROWTH_SEEDS) * len(PLACEMENTS) * len(FRESH_SEED_DELTAS) * len(CONSTRUCTORS) * len(COUPLINGS)
        run_index = 0
        for growth_seed in GROWTH_SEEDS:
            for placement in PLACEMENTS:
                for seed_delta in FRESH_SEED_DELTAS:
                    assignment = assignment_by_key[(growth_seed, placement, seed_delta)]
                    for constructor in CONSTRUCTORS:
                        for coupling in COUPLINGS:
                            run_index += 1
                            print(
                                f"running {run_index}/{total_runs} growth_seed={growth_seed} p{placement} "
                                f"seed_delta={seed_delta} constructor={constructor} coupling={coupling}",
                                flush=True,
                            )
                            run_snapshots, run_row = run_factor_cell(
                                base_state=base_states[growth_seed],
                                assignment=assignment,
                                constructor=constructor,
                                coupling=coupling,
                                params=params,
                            )
                            snapshots.extend(run_snapshots)
                            run_rows.append(run_row)
        write_csv(args.out_snapshots_csv, snapshots)
        write_csv(args.out_runs_csv, run_rows)

    expected_runs = len(GROWTH_SEEDS) * len(PLACEMENTS) * len(FRESH_SEED_DELTAS) * len(CONSTRUCTORS) * len(COUPLINGS)
    if len(run_rows) != expected_runs:
        raise ValueError(f"expected {expected_runs} runs, found {len(run_rows)}")
    cells = cell_summary_rows(run_rows)
    comparisons = factor_comparison_rows(cells)
    evaluation = evaluation_rows(
        assignments=assignments,
        run_rows=run_rows,
        comparisons=comparisons,
        target_summary=target_summary,
    )
    claims = claim_ledger_rows(evaluation)

    write_csv(args.out_cells_csv, cells)
    write_csv(args.out_comparisons_csv, comparisons)
    write_csv(args.out_evaluation_csv, evaluation)
    write_csv(args.out_claims_csv, claims)
    Path(args.out_report).write_text(
        render_report(cells=cells, comparisons=comparisons, evaluation=evaluation, claims=claims),
        encoding="utf-8",
    )
    Path(args.out_operational).write_text(render_operational(evaluation), encoding="utf-8")

    for row in evaluation:
        print(f"{row['key']}: {row['value']} ({row['evidence']})")


if __name__ == "__main__":
    main()
