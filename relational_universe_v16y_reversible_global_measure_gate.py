#!/usr/bin/env python3
"""v16y effect-blind comparison of two global matching probability laws.

The frozen v16x integer random-cost law is replayed as a reference. A lazy
Metropolis chain proposes uniformly among valid 2x2 assignment switches and
corrects for state-dependent neighbor degree. Its stationary target is uniform
only on each connected component of the 2-switch graph. No source spectrum or
observed-effect statistic is computed.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import random
import statistics
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16n_coarse_event_resource_null_calibration as v16n
import relational_universe_v16t_footprint_null_path_stability_gate as v16t
import relational_universe_v16v_global_edge_slot_feasibility_gate as v16v
import relational_universe_v16x_explicit_global_measure_gate as v16x
import relational_universe_v16x_postrun_concentration_audit as v16xp


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

MEASURE_REFERENCE = "v16x_integer_random_cost_minimum_b_matching"
MEASURE_CHAIN = "lazy_degree_corrected_uniform_neighbor_2x2_metropolis"
START_FAMILIES = ("source_assignment", "v16x_random_cost_a0")
CHAIN_SEED_FAMILIES = ("chain_seed_a", "chain_seed_b")
TOTAL_STEPS = 512
BURNIN_STEPS = 256
THIN_STEPS = 32
SAMPLES_PER_CHAIN = 8
REVERSIBILITY_WITNESSES_PER_START = 4
REPRESENTATION_STEPS = 32
MIN_FINAL_START_CHANGE = 0.05
MIN_ACCEPTED_SWAPS_PER_EDGE = 0.05
MIN_CHAIN_UNIQUE_FRACTION = 0.875
MAX_CENTER_RANGE_RATIO = v16x.MAX_CENTER_RANGE_RATIO
MIN_REFERENCE_SUPPORT_RATIO = 0.50
MIN_IMPROVED_SOURCES = 4

CENTER_FEATURES = (
    "source_edge_fraction",
    "normalized_mean_parent_lag",
    "mean_depth_gap",
    "concrete_conflict_fraction",
    "mean_candidate_rank_fraction",
    "log_neighbor_degree",
    "mean_pairwise_changed_fraction",
)

SOURCE_CHAIN = DOC / "v16y_source_chain.csv"
PRE_REGISTRATION = DOC / "v16y_pre_registration.csv"
REVERSIBILITY_AUDIT = DOC / "v16y_proposal_reversibility_audit.csv"
REPRESENTATION_AUDIT = DOC / "v16y_representation_audit.csv"
REFERENCE_REPLAY = DOC / "v16y_random_cost_reference_replay.csv"
TRANSITION_SUMMARY = DOC / "v16y_chain_transition_summary.csv"
ENDPOINT_AUDIT = DOC / "v16y_chain_endpoint_audit.csv"
PAIRWISE_DISTANCE = DOC / "v16y_chain_pairwise_distance.csv"
STABILITY_AUDIT = DOC / "v16y_chain_center_stability.csv"
CONCENTRATION_PROFILE = DOC / "v16y_marginal_concentration_profile.csv"
MEASURE_COMPARISON = DOC / "v16y_measure_comparison.csv"
SOURCE_SUMMARY = DOC / "v16y_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v16y_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16y_claim_ledger.csv"
REPORT = DOC / "v16y_reversible_global_measure_gate.md"
INTERPRETATION = DOC / "v16y_interpretation_audit.md"
NEXT_DIRECTION = DOC / "v16y_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_16y_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16y.md"

Edge = v16x.Edge
Slot = v16x.Slot


@dataclass(frozen=True, order=True)
class SwapMove:
    remove: Tuple[Edge, Edge]
    add: Tuple[Edge, Edge]


@dataclass(frozen=True)
class ChainKernel:
    space: v16x.StateSpace
    candidate_parents_by_slot: Mapping[Slot, Tuple[int, ...]]


@dataclass
class Sample:
    edges: frozenset[Edge]
    row: MutableMapping[str, Any]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v16x", "frozen_measure_preregistration", v16x.PRE_REGISTRATION),
        ("v16x", "frozen_measure_source_chain", v16x.SOURCE_CHAIN),
        ("v16x", "frozen_reference_endpoints", v16x.ENDPOINT_AUDIT),
        ("v16x", "frozen_forced_edge_audit", v16x.STATE_SPACE_AUDIT),
        ("v16x", "frozen_gate_decision", v16x.GATE_EVALUATION),
        ("v16x", "combined_seed_concentration", v16xp.CONCENTRATION_AUDIT),
        ("v16x", "interpretation_boundary", DOC / "v16x_interpretation_audit.md"),
    )
    return [{
        "stage": stage,
        "role": role,
        "artifact": path.name,
        "sha256": file_sha256(path),
        "source_pass": 1,
    } for stage, role, path in paths]


def spec_payload() -> Dict[str, Any]:
    return {
        "gate": "v16y_reversible_global_measure_gate",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_probability_law_comparison_on_frozen_coarse_state_space",
        "source_history_count": 6,
        "state_space": v16x.COARSE_ARM,
        "reference_measure": MEASURE_REFERENCE,
        "candidate_measure": MEASURE_CHAIN,
        "candidate_stationary_target": "uniform_on_each_2x2_switch_connected_component",
        "proposal": "uniform_valid_2x2_neighbor",
        "proposal_correction": "metropolis_min_1_degree_current_over_degree_proposed",
        "laziness_probability": "1/2",
        "start_families": list(START_FAMILIES),
        "chain_seed_families": list(CHAIN_SEED_FAMILIES),
        "total_steps": TOTAL_STEPS,
        "burnin_steps": BURNIN_STEPS,
        "thin_steps": THIN_STEPS,
        "samples_per_chain": SAMPLES_PER_CHAIN,
        "reference_endpoints_per_source": v16x.PRIMARY_REPLICATES + v16x.SENSITIVITY_REPLICATES,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "minimum_accepted_swaps_per_edge": MIN_ACCEPTED_SWAPS_PER_EDGE,
        "minimum_chain_unique_fraction": MIN_CHAIN_UNIQUE_FRACTION,
        "maximum_center_range_ratio": MAX_CENTER_RANGE_RATIO,
        "minimum_reference_support_ratio": MIN_REFERENCE_SUPPORT_RATIO,
        "minimum_sources_with_concentration_profile_improvement": MIN_IMPROVED_SOURCES,
        "design_calibration_disclosure": (
            "before preregistration, the naive selected-edge-pair proposal was inspected at "
            "50 proposals per edge and full valid-neighbor enumeration was timed on all six "
            "frozen sources; no spectrum or effect statistic was inspected"
        ),
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "no_early_stop": True,
        "not_claimed": [
            "global_irreducibility", "mixing", "global_uniform_sampling", "maximum_entropy",
            "canonical_measure", "spectrum_effect", "physics", "energy", "temperature",
            "dimension", "Lorentz_symmetry", "spacetime", "particles", "entanglement",
        ],
    }


def spec_digest() -> str:
    raw = json.dumps(spec_payload(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def preregistration_row() -> Dict[str, Any]:
    return {
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "script_sha256": file_sha256(SCRIPT),
        "source_chain_sha256": file_sha256(SOURCE_CHAIN),
        "source_history_count": 6,
        "state_space": v16x.COARSE_ARM,
        "reference_measure": MEASURE_REFERENCE,
        "candidate_measure": MEASURE_CHAIN,
        "stationary_target_scope": "uniform_per_2x2_connected_component",
        "start_families": ";".join(START_FAMILIES),
        "chain_seed_families": ";".join(CHAIN_SEED_FAMILIES),
        "total_steps": TOTAL_STEPS,
        "burnin_steps": BURNIN_STEPS,
        "thin_steps": THIN_STEPS,
        "samples_per_chain": SAMPLES_PER_CHAIN,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "minimum_accepted_swaps_per_edge": MIN_ACCEPTED_SWAPS_PER_EDGE,
        "minimum_chain_unique_fraction": MIN_CHAIN_UNIQUE_FRACTION,
        "maximum_center_range_ratio": MAX_CENTER_RANGE_RATIO,
        "minimum_reference_support_ratio": MIN_REFERENCE_SUPPORT_RATIO,
        "minimum_improved_sources": MIN_IMPROVED_SOURCES,
        "design_pilot_inspected": 1,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v16x.verify_outputs()
    v16xp.verify_outputs()
    overall = next(
        row["status"] for row in v16i.read_csv(v16x.GATE_EVALUATION)
        if row["gate"] == "v16x_overall"
    )
    if overall != "v16x_integer_measure_endpoint_diversity_not_qualified":
        raise ValueError("v16y requires the frozen v16x diversity failure")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v16y] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    expected = {key: str(value) for key, value in preregistration_row().items()}
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v16y preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v16y source chain changed")


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    runs = []
    for source, metadata in v16x.load_runs():
        runs.append((v16i.RunDAG(
            stage="v16y",
            target_nodes=source.target_nodes,
            growth_seed=source.growth_seed,
            run_offset=source.run_offset,
            arm=source.arm,
            run_seed=source.run_seed,
            predecessors=source.predecessors,
            depths=source.depths,
            indegrees=source.indegrees,
        ), metadata))
    return runs


def build_kernel(space: v16x.StateSpace) -> ChainKernel:
    grouped: Dict[Slot, set[int]] = defaultdict(set)
    for edge in space.candidates:
        grouped[space.slot_by_edge[edge]].add(edge[0])
    return ChainKernel(space, {
        slot: tuple(sorted(parents)) for slot, parents in grouped.items()
    })


def neighbor_moves(kernel: ChainKernel, selected: frozenset[Edge]) -> Tuple[SwapMove, ...]:
    space = kernel.space
    if not v16x.assignment_integrity(space, selected):
        raise ValueError("neighbor enumeration requires a valid assignment")
    by_parent: Dict[int, List[Edge]] = defaultdict(list)
    for edge in selected:
        by_parent[edge[0]].append(edge)
    for edges in by_parent.values():
        edges.sort()

    moves: set[SwapMove] = set()
    for first in sorted(selected):
        parent = first[0]
        first_slot = space.slot_by_edge[first]
        for other_parent in kernel.candidate_parents_by_slot[first_slot]:
            if other_parent == parent:
                continue
            first_cross = (other_parent, first_slot[0])
            if first_cross in selected:
                continue
            for second in by_parent.get(other_parent, ()):
                second_slot = space.slot_by_edge[second]
                if second_slot == first_slot:
                    continue
                second_cross = (parent, second_slot[0])
                if second_cross in selected:
                    continue
                if space.slot_by_edge.get(second_cross) != second_slot:
                    continue
                remove = tuple(sorted((first, second)))
                add = tuple(sorted((first_cross, second_cross)))
                if len(set((*remove, *add))) != 4:
                    continue
                moves.add(SwapMove(remove=remove, add=add))
    return tuple(sorted(moves))


def apply_move(
    space: v16x.StateSpace,
    selected: frozenset[Edge],
    move: SwapMove,
) -> frozenset[Edge]:
    if not set(move.remove).issubset(selected) or set(move.add) & selected:
        raise ValueError("invalid 2x2 move occupancy")
    result = frozenset((set(selected) - set(move.remove)) | set(move.add))
    if not v16x.assignment_integrity(space, result):
        raise ValueError("2x2 move broke assignment integrity")
    return result


def reverse_move(move: SwapMove) -> SwapMove:
    return SwapMove(remove=move.add, add=move.remove)


def accepted_transition_probability(degree_left: int, degree_right: int) -> Fraction:
    if degree_left <= 0 or degree_right <= 0:
        raise ValueError("accepted transition requires positive neighbor degree")
    return Fraction(1, 2 * max(degree_left, degree_right))


def advance_chain(
    kernel: ChainKernel,
    start: frozenset[Edge],
    seed: int,
    *,
    total_steps: int,
    record_steps: Iterable[int] = (),
) -> Tuple[frozenset[Edge], Tuple[SwapMove, ...], Dict[str, Any], List[Tuple[int, frozenset[Edge], int]]]:
    rng = random.Random(seed)
    selected = start
    moves = neighbor_moves(kernel, selected)
    record_set = set(record_steps)
    records: List[Tuple[int, frozenset[Edge], int]] = []
    lazy_stays = nonlazy = accepted = mh_rejects = trapped = 0
    min_degree = max_degree = len(moves)
    for step in range(1, total_steps + 1):
        if rng.getrandbits(1) == 0:
            lazy_stays += 1
        elif not moves:
            nonlazy += 1
            trapped += 1
        else:
            nonlazy += 1
            move = moves[rng.randrange(len(moves))]
            proposed = apply_move(kernel.space, selected, move)
            proposed_moves = neighbor_moves(kernel, proposed)
            if reverse_move(move) not in proposed_moves:
                raise ValueError("2x2 proposal lacked its reverse move")
            acceptance = min(1.0, len(moves) / len(proposed_moves))
            if rng.random() < acceptance:
                selected = proposed
                moves = proposed_moves
                accepted += 1
            else:
                mh_rejects += 1
        min_degree = min(min_degree, len(moves))
        max_degree = max(max_degree, len(moves))
        if step in record_set:
            records.append((step, selected, len(moves)))
    stats = {
        "total_steps": total_steps,
        "lazy_stays": lazy_stays,
        "nonlazy_proposals": nonlazy,
        "accepted_swaps": accepted,
        "mh_rejects": mh_rejects,
        "trapped_nonlazy_steps": trapped,
        "minimum_neighbor_degree": min_degree,
        "maximum_neighbor_degree": max_degree,
    }
    return selected, moves, stats, records


def expected_record_steps() -> Tuple[int, ...]:
    return tuple(BURNIN_STEPS + THIN_STEPS * index for index in range(1, SAMPLES_PER_CHAIN + 1))


def endpoint_row(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    space: v16x.StateSpace,
    flexibility: v16x.FlexibilityAudit,
    start_family: str,
    chain_seed_family: str,
    sample_index: int,
    step: int,
    start: frozenset[Edge],
    edges: frozenset[Edge],
    neighbor_degree: int,
) -> MutableMapping[str, Any]:
    predecessors: List[List[int]] = [[] for _ in dag.predecessors]
    for parent, child in edges:
        predecessors[child].append(parent)
    rewired = tuple(tuple(sorted(parents)) for parents in predecessors)
    structure = v16t.final_structure_audit(dag, metadata, rewired)
    features = v16x.endpoint_features(dag, metadata, space, edges)
    integrity = all((
        v16x.assignment_integrity(space, edges),
        int(structure["structure_pass"]),
        flexibility.forced_source_edges.issubset(edges),
    ))
    return {
        **dag.prefix,
        "state_space_arm": space.arm,
        "stochastic_measure": MEASURE_CHAIN,
        "stationary_target_scope": "uniform_per_2x2_connected_component",
        "start_family": start_family,
        "chain_seed_family": chain_seed_family,
        "sample_index": sample_index,
        "step": step,
        "selected_edge_count": len(edges),
        "neighbor_degree": neighbor_degree,
        "log_neighbor_degree": math.log1p(neighbor_degree),
        "source_changed_edge_fraction": 1.0 - len(edges & space.source_edges) / space.edge_count,
        "start_changed_edge_fraction": 1.0 - len(edges & start) / space.edge_count,
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
        **structure,
        **features,
        "mean_pairwise_changed_fraction": math.nan,
        "globally_forced_edges_included_pass": int(flexibility.forced_source_edges.issubset(edges)),
        "endpoint_integrity_pass": int(integrity),
        "endpoint_edge_sha256": v16x.edge_digest(edges),
    }


def frozen_reference_digests() -> Dict[Tuple[int, int, str, int], str]:
    return {
        (
            int(row["growth_seed"]), int(row["run_offset"]),
            row["seed_family"], int(row["replicate"]),
        ): row["endpoint_edge_sha256"]
        for row in v16i.read_csv(v16x.ENDPOINT_AUDIT)
    }


def replay_reference(
    dag: v16i.RunDAG,
    space: v16x.StateSpace,
    flexibility: v16x.FlexibilityAudit,
    expected: Mapping[Tuple[int, int, str, int], str],
) -> Tuple[List[Sample], List[Dict[str, Any]]]:
    samples: List[Sample] = []
    rows: List[Dict[str, Any]] = []
    for seed_family, count in (
        (v16x.PRIMARY_SEED_FAMILY, v16x.PRIMARY_REPLICATES),
        (v16x.SENSITIVITY_SEED_FAMILY, v16x.SENSITIVITY_REPLICATES),
    ):
        for replicate in range(count):
            _, costs = v16x.edge_costs(dag, space, seed_family, replicate)
            edges, _, _ = v16x.solve_edges(space, costs)
            digest = v16x.edge_digest(edges)
            expected_digest = expected[(dag.growth_seed, dag.run_offset, seed_family, replicate)]
            integrity = (
                v16x.assignment_integrity(space, edges)
                and flexibility.forced_source_edges.issubset(edges)
            )
            row = {
                **dag.prefix,
                "reference_measure": MEASURE_REFERENCE,
                "seed_family": seed_family,
                "replicate": replicate,
                "endpoint_edge_sha256": digest,
                "expected_endpoint_edge_sha256": expected_digest,
                "digest_replay_pass": int(digest == expected_digest),
                "endpoint_integrity_pass": int(integrity),
                "source_spectrum_computed": 0,
                "observed_effect_computed": 0,
            }
            rows.append(row)
            samples.append(Sample(edges, row))
    return samples, rows


def reversibility_rows(
    dag: v16i.RunDAG,
    kernel: ChainKernel,
    starts: Mapping[str, frozenset[Edge]],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for start_family, start in starts.items():
        moves = neighbor_moves(kernel, start)
        if len(moves) < REVERSIBILITY_WITNESSES_PER_START:
            raise ValueError("insufficient 2x2 reversibility witnesses")
        indexes = [
            index * len(moves) // REVERSIBILITY_WITNESSES_PER_START
            for index in range(REVERSIBILITY_WITNESSES_PER_START)
        ]
        for witness_index, move_index in enumerate(indexes):
            move = moves[move_index]
            proposed = apply_move(kernel.space, start, move)
            proposed_moves = neighbor_moves(kernel, proposed)
            reverse_present = reverse_move(move) in proposed_moves
            forward = accepted_transition_probability(len(moves), len(proposed_moves))
            reverse = accepted_transition_probability(len(proposed_moves), len(moves))
            rows.append({
                **dag.prefix,
                "start_family": start_family,
                "witness_index": witness_index,
                "current_neighbor_degree": len(moves),
                "proposed_neighbor_degree": len(proposed_moves),
                "forward_probability_numerator": forward.numerator,
                "forward_probability_denominator": forward.denominator,
                "reverse_probability_numerator": reverse.numerator,
                "reverse_probability_denominator": reverse.denominator,
                "reverse_move_present": int(reverse_present),
                "proposed_integrity_pass": int(v16x.assignment_integrity(kernel.space, proposed)),
                "detailed_balance_pass": int(reverse_present and forward == reverse),
            })
    return rows


def representation_row(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    space: v16x.StateSpace,
) -> Dict[str, Any]:
    seed = v16i.stable_seed("v16y", "representation", *dag.key)
    original_kernel = build_kernel(space)
    original, _, _, _ = advance_chain(
        original_kernel, space.source_edges, seed, total_steps=REPRESENTATION_STEPS
    )
    replay, _, _, _ = advance_chain(
        original_kernel, space.source_edges, seed, total_steps=REPRESENTATION_STEPS
    )
    reversed_space = v16x.StateSpace(
        arm=space.arm,
        candidates=tuple(reversed(space.candidates)),
        source_edges=space.source_edges,
        slot_by_edge=space.slot_by_edge,
        parent_demands=space.parent_demands,
        slot_demands=space.slot_demands,
        edge_count=space.edge_count,
    )
    reordered, _, _, _ = advance_chain(
        build_kernel(reversed_space), space.source_edges, seed, total_steps=REPRESENTATION_STEPS
    )
    relabeled = v16x.v16w.relabel_metadata(
        metadata, v16i.stable_seed("v16y", "relabel", *dag.key)
    )
    relabeled_space = v16x.build_state_space(dag, relabeled, v16x.COARSE_ARM)
    relabeled_result, _, _, _ = advance_chain(
        build_kernel(relabeled_space), relabeled_space.source_edges, seed,
        total_steps=REPRESENTATION_STEPS,
    )
    candidate_covariance = space.candidates == relabeled_space.candidates
    passed = (
        original == replay == reordered == relabeled_result
        and candidate_covariance
        and v16x.assignment_integrity(space, original)
    )
    return {
        **dag.prefix,
        "check_steps": REPRESENTATION_STEPS,
        "source_endpoint_sha256": v16x.edge_digest(original),
        "replay_endpoint_sha256": v16x.edge_digest(replay),
        "reordered_endpoint_sha256": v16x.edge_digest(reordered),
        "relabeled_endpoint_sha256": v16x.edge_digest(relabeled_result),
        "candidate_set_covariance_pass": int(candidate_covariance),
        "exact_replay_pass": int(original == replay),
        "candidate_order_covariance_pass": int(original == reordered),
        "semantic_relabel_covariance_pass": int(original == relabeled_result),
        "representation_pass": int(passed),
    }


def chain_seed(dag: v16i.RunDAG, start_family: str, seed_family: str) -> int:
    return v16i.stable_seed("v16y", "chain", start_family, seed_family, *dag.key)


def run_chains(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    kernel: ChainKernel,
    flexibility: v16x.FlexibilityAudit,
    starts: Mapping[str, frozenset[Edge]],
) -> Tuple[List[Sample], List[Dict[str, Any]]]:
    samples: List[Sample] = []
    transitions: List[Dict[str, Any]] = []
    record_steps = expected_record_steps()
    for start_family in START_FAMILIES:
        start = starts[start_family]
        for seed_family in CHAIN_SEED_FAMILIES:
            seed = chain_seed(dag, start_family, seed_family)
            final, final_moves, stats, records = advance_chain(
                kernel, start, seed, total_steps=TOTAL_STEPS, record_steps=record_steps
            )
            if len(records) != SAMPLES_PER_CHAIN:
                raise ValueError("chain sample schedule failed")
            for sample_index, (step, edges, degree) in enumerate(records):
                row = endpoint_row(
                    dag, metadata, kernel.space, flexibility, start_family, seed_family,
                    sample_index, step, start, edges, degree,
                )
                samples.append(Sample(edges, row))
            final_change = 1.0 - len(final & start) / kernel.space.edge_count
            accepted_per_edge = stats["accepted_swaps"] / kernel.space.edge_count
            unique_fraction = len({
                v16x.edge_digest(edges) for _, edges, _ in records
            }) / len(records)
            movement_pass = (
                final_change >= MIN_FINAL_START_CHANGE
                and accepted_per_edge >= MIN_ACCEPTED_SWAPS_PER_EDGE
                and unique_fraction >= MIN_CHAIN_UNIQUE_FRACTION
                and stats["minimum_neighbor_degree"] > 0
                and v16x.assignment_integrity(kernel.space, final)
            )
            transitions.append({
                **dag.prefix,
                "start_family": start_family,
                "chain_seed_family": seed_family,
                "chain_seed": seed,
                "start_endpoint_sha256": v16x.edge_digest(start),
                "final_endpoint_sha256": v16x.edge_digest(final),
                **stats,
                "final_neighbor_degree": len(final_moves),
                "accepted_swaps_per_edge": accepted_per_edge,
                "final_start_changed_edge_fraction": final_change,
                "sample_unique_fraction": unique_fraction,
                "minimum_final_start_change": MIN_FINAL_START_CHANGE,
                "minimum_accepted_swaps_per_edge": MIN_ACCEPTED_SWAPS_PER_EDGE,
                "minimum_chain_unique_fraction": MIN_CHAIN_UNIQUE_FRACTION,
                "movement_pass": int(movement_pass),
            })
    return samples, transitions


def pairwise_rows(dag: v16i.RunDAG, samples: Sequence[Sample]) -> List[Dict[str, Any]]:
    distances: Dict[int, List[float]] = defaultdict(list)
    rows: List[Dict[str, Any]] = []
    edge_count = len(samples[0].edges)
    for left_index, right_index in combinations(range(len(samples)), 2):
        left, right = samples[left_index], samples[right_index]
        changed = len(left.edges - right.edges) / edge_count
        distances[left_index].append(changed)
        distances[right_index].append(changed)
        rows.append({
            **dag.prefix,
            "left_start_family": left.row["start_family"],
            "left_chain_seed_family": left.row["chain_seed_family"],
            "left_sample_index": left.row["sample_index"],
            "right_start_family": right.row["start_family"],
            "right_chain_seed_family": right.row["chain_seed_family"],
            "right_sample_index": right.row["sample_index"],
            "left_endpoint_sha256": left.row["endpoint_edge_sha256"],
            "right_endpoint_sha256": right.row["endpoint_edge_sha256"],
            "changed_edge_fraction": changed,
        })
    for index, sample in enumerate(samples):
        sample.row["mean_pairwise_changed_fraction"] = statistics.mean(distances[index])
    return rows


def range_ratio(left: Sequence[float], right: Sequence[float]) -> Tuple[float, float, float, float]:
    left_center = statistics.median(left)
    right_center = statistics.median(right)
    shift = abs(left_center - right_center)
    combined_range = max((*left, *right)) - min((*left, *right))
    ratio = 0.0 if combined_range == 0.0 else shift / combined_range
    return left_center, right_center, shift, ratio


def stability_rows(
    dag: v16i.RunDAG,
    samples: Sequence[Sample],
) -> List[Dict[str, Any]]:
    comparisons = (
        (
            "start_family",
            [sample for sample in samples if sample.row["start_family"] == START_FAMILIES[0]],
            [sample for sample in samples if sample.row["start_family"] == START_FAMILIES[1]],
        ),
        (
            "independent_chain_seed_family",
            [sample for sample in samples if sample.row["chain_seed_family"] == CHAIN_SEED_FAMILIES[0]],
            [sample for sample in samples if sample.row["chain_seed_family"] == CHAIN_SEED_FAMILIES[1]],
        ),
        (
            "early_vs_late_sample_window",
            [sample for sample in samples if int(sample.row["sample_index"]) < SAMPLES_PER_CHAIN // 2],
            [sample for sample in samples if int(sample.row["sample_index"]) >= SAMPLES_PER_CHAIN // 2],
        ),
    )
    rows: List[Dict[str, Any]] = []
    for kind, left, right in comparisons:
        for feature in CENTER_FEATURES:
            values_left = [float(sample.row[feature]) for sample in left]
            values_right = [float(sample.row[feature]) for sample in right]
            left_center, right_center, shift, ratio = range_ratio(values_left, values_right)
            rows.append({
                **dag.prefix,
                "stability_kind": kind,
                "feature": feature,
                "left_count": len(left),
                "right_count": len(right),
                "left_median": left_center,
                "right_median": right_center,
                "absolute_center_shift": shift,
                "center_shift_range_ratio": ratio,
                "maximum_allowed_ratio": MAX_CENTER_RANGE_RATIO,
                "center_stability_pass": int(ratio <= MAX_CENTER_RANGE_RATIO),
            })
    return rows


def binary_entropy(probability: float) -> float:
    if probability <= 0.0 or probability >= 1.0:
        return 0.0
    return -probability * math.log2(probability) - (1.0 - probability) * math.log2(1.0 - probability)


def concentration_profile(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    space: v16x.StateSpace,
    flexibility: v16x.FlexibilityAudit,
    law: str,
    samples: Sequence[Sample],
) -> Dict[str, Any]:
    counts = Counter(edge for sample in samples for edge in sample.edges)
    variable = flexibility.flexible_edges
    n = len(samples)
    ranked = sorted(variable, key=lambda edge: (-counts[edge], edge))
    top = ranked[0]
    occupied = {edge: counts[edge] for edge in variable if counts[edge]}
    total_occurrences = sum(occupied.values())
    probabilities = [count / total_occurrences for count in occupied.values()]
    entropy = -sum(value * math.log(value) for value in probabilities) if probabilities else 0.0
    effective_support = math.exp(entropy) / len(variable) if variable else 0.0
    mean_binary_entropy = statistics.mean(binary_entropy(counts[edge] / n) for edge in variable)
    return {
        **dag.prefix,
        "probability_law": law,
        "endpoint_count": n,
        "globally_variable_edge_count": len(variable),
        "variable_union_count": len(occupied),
        "variable_union_coverage": len(occupied) / len(variable),
        "effective_variable_support_ratio": effective_support,
        "mean_variable_edge_binary_entropy": mean_binary_entropy,
        "maximum_variable_edge_inclusion_count": counts[top],
        "maximum_variable_edge_inclusion_rate": counts[top] / n,
        "top_parent_event_id": top[0],
        "top_child_event_id": top[1],
        "top_edge_is_source": int(top in space.source_edges),
        "top_edge_has_concrete_conflict": int(bool(
            v16n.conflict_channels(metadata[top[0]], metadata[top[1]])
        )),
        "variable_edges_included_every_endpoint": sum(counts[edge] == n for edge in variable),
        "variable_edges_included_at_least_95pct": sum(counts[edge] / n >= 0.95 for edge in variable),
        "variable_edges_with_mid_marginal": sum(0.05 < counts[edge] / n < 0.95 for edge in variable),
        "all_forced_edges_included_pass": int(all(
            flexibility.forced_source_edges.issubset(sample.edges) for sample in samples
        )),
    }


def compare_profiles(
    dag: v16i.RunDAG,
    reference: Mapping[str, Any],
    chain: Mapping[str, Any],
) -> Dict[str, Any]:
    reference_effective = float(reference["effective_variable_support_ratio"])
    reference_union = float(reference["variable_union_coverage"])
    effective_ratio = float(chain["effective_variable_support_ratio"]) / reference_effective
    union_ratio = float(chain["variable_union_coverage"]) / reference_union
    top_improved = (
        float(chain["maximum_variable_edge_inclusion_rate"])
        < float(reference["maximum_variable_edge_inclusion_rate"])
    )
    entropy_improved = (
        float(chain["mean_variable_edge_binary_entropy"])
        > float(reference["mean_variable_edge_binary_entropy"])
    )
    support_pass = (
        effective_ratio >= MIN_REFERENCE_SUPPORT_RATIO
        and union_ratio >= MIN_REFERENCE_SUPPORT_RATIO
    )
    passed = top_improved and entropy_improved and support_pass
    return {
        **dag.prefix,
        "reference_max_inclusion_rate": reference["maximum_variable_edge_inclusion_rate"],
        "chain_max_inclusion_rate": chain["maximum_variable_edge_inclusion_rate"],
        "maximum_inclusion_rate_delta": (
            float(chain["maximum_variable_edge_inclusion_rate"])
            - float(reference["maximum_variable_edge_inclusion_rate"])
        ),
        "reference_mean_binary_entropy": reference["mean_variable_edge_binary_entropy"],
        "chain_mean_binary_entropy": chain["mean_variable_edge_binary_entropy"],
        "mean_binary_entropy_delta": (
            float(chain["mean_variable_edge_binary_entropy"])
            - float(reference["mean_variable_edge_binary_entropy"])
        ),
        "effective_support_ratio_chain_over_reference": effective_ratio,
        "union_coverage_ratio_chain_over_reference": union_ratio,
        "minimum_reference_support_ratio": MIN_REFERENCE_SUPPORT_RATIO,
        "top_concentration_improved": int(top_improved),
        "marginal_entropy_improved": int(entropy_improved),
        "support_retention_pass": int(support_pass),
        "measure_comparison_pass": int(passed),
    }


def implementation_call_counts() -> Dict[str, int]:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    names = Counter()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute):
            names[node.func.attr] += 1
        elif isinstance(node.func, ast.Name):
            names[node.func.id] += 1
    return {
        "spectrum_calls": names["interval_spectrum"],
        "effect_metric_calls": names["jensen_shannon"],
    }


def markdown_table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = []
        for field in fields:
            value = row[field]
            values.append(f"{value:.6f}" if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return lines


def build_report(
    summaries: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16y reversible global-measure gate",
        "",
        f"Status: `{overall}`.",
        "",
        "## Evidential status",
        "",
        "This is an effect-blind probability-law comparison on the same six frozen coarse global matching spaces used by v16x. It computes no source spectrum or observed-effect statistic.",
        "",
        "The candidate chain is lazy and Metropolis-corrected. Its accepted transition probability is exactly `1 / (2 * max(degree(x), degree(y)))` in both directions. This gives a uniform stationary target only inside each connected component of the valid 2x2-switch graph. The run does not prove global connectivity or mixing.",
        "",
        "Before preregistration, a design pilot measured the low acceptance of naive random selected-edge pairs and timed exact valid-neighbor enumeration. Those effect-blind implementation observations selected the fixed 512-step budget; they are not fresh evidence.",
        "",
        "## Source qualification",
        "",
    ]
    lines.extend(markdown_table(summaries, (
        "growth_seed", "run_offset", "reference_replay_pass", "reversibility_pass",
        "representation_pass", "movement_pass", "center_stability_pass",
        "measure_comparison_pass", "source_qualification_pass",
    )))
    lines.extend(["", "## Probability-law comparison", ""])
    lines.extend(markdown_table(comparisons, (
        "growth_seed", "run_offset", "reference_max_inclusion_rate",
        "chain_max_inclusion_rate", "mean_binary_entropy_delta",
        "effective_support_ratio_chain_over_reference",
        "union_coverage_ratio_chain_over_reference", "measure_comparison_pass",
    )))
    lines.extend(["", "## Gates", ""])
    lines.extend(markdown_table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "A pass would establish finite qualification of this declared component-uniform chain under two starts, two independent seeds and three center comparisons. It would not prove irreducibility, convergence, global uniformity, maximum entropy or a canonical null.",
        "",
        "A failure distinguishes algebra/reversibility defects, insufficient finite mobility, start/seed/time instability, and failure to improve the v16x concentration profile.",
        "",
        "V16y establishes no spectrum effect, energy, temperature, invariant, dimension, manifold, Lorentz symmetry, spacetime, particle, entanglement, continuum, or physical law.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    verify_frozen_sources()
    calls = implementation_call_counts()
    expected_digests = frozen_reference_digests()
    reversibility: List[Dict[str, Any]] = []
    representations: List[Dict[str, Any]] = []
    reference_rows: List[Dict[str, Any]] = []
    transitions: List[Dict[str, Any]] = []
    endpoint_rows: List[MutableMapping[str, Any]] = []
    pairwise: List[Dict[str, Any]] = []
    stability: List[Dict[str, Any]] = []
    profiles: List[Dict[str, Any]] = []
    comparisons: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []

    for run_index, (dag, metadata) in enumerate(load_runs(), start=1):
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        flexibility = v16x.audit_flexibility(space)
        kernel = build_kernel(space)
        reference_samples, source_reference_rows = replay_reference(
            dag, space, flexibility, expected_digests
        )
        reference_rows.extend(source_reference_rows)
        random_start = next(
            sample.edges for sample in reference_samples
            if sample.row["seed_family"] == v16x.PRIMARY_SEED_FAMILY
            and int(sample.row["replicate"]) == 0
        )
        starts = {
            "source_assignment": space.source_edges,
            "v16x_random_cost_a0": random_start,
        }
        source_reversibility = reversibility_rows(dag, kernel, starts)
        reversibility.extend(source_reversibility)
        source_representation = representation_row(dag, metadata, space)
        representations.append(source_representation)
        source_samples, source_transitions = run_chains(
            dag, metadata, kernel, flexibility, starts
        )
        transitions.extend(source_transitions)
        pairwise.extend(pairwise_rows(dag, source_samples))
        endpoint_rows.extend(sample.row for sample in source_samples)
        source_stability = stability_rows(dag, source_samples)
        stability.extend(source_stability)
        reference_profile = concentration_profile(
            dag, metadata, space, flexibility, MEASURE_REFERENCE, reference_samples
        )
        chain_profile = concentration_profile(
            dag, metadata, space, flexibility, MEASURE_CHAIN, source_samples
        )
        profiles.extend((reference_profile, chain_profile))
        comparison = compare_profiles(dag, reference_profile, chain_profile)
        comparisons.append(comparison)

        reference_pass = all(
            int(row["digest_replay_pass"]) and int(row["endpoint_integrity_pass"])
            for row in source_reference_rows
        )
        reversibility_pass = all(int(row["detailed_balance_pass"]) for row in source_reversibility)
        movement_pass = all(int(row["movement_pass"]) for row in source_transitions)
        stability_pass = all(int(row["center_stability_pass"]) for row in source_stability)
        integrity_pass = all(int(sample.row["endpoint_integrity_pass"]) for sample in source_samples)
        source_pass = all((
            reference_pass, reversibility_pass, int(source_representation["representation_pass"]),
            movement_pass, stability_pass, integrity_pass,
            int(comparison["measure_comparison_pass"]),
        ))
        summaries.append({
            **dag.prefix,
            "reference_replay_pass": int(reference_pass),
            "reversibility_pass": int(reversibility_pass),
            "representation_pass": source_representation["representation_pass"],
            "movement_pass": int(movement_pass),
            "center_stability_pass": int(stability_pass),
            "endpoint_integrity_pass": int(integrity_pass),
            "measure_comparison_pass": comparison["measure_comparison_pass"],
            "minimum_final_start_changed_edge_fraction": min(
                float(row["final_start_changed_edge_fraction"]) for row in source_transitions
            ),
            "minimum_accepted_swaps_per_edge_observed": min(
                float(row["accepted_swaps_per_edge"]) for row in source_transitions
            ),
            "minimum_sample_unique_fraction": min(
                float(row["sample_unique_fraction"]) for row in source_transitions
            ),
            "source_qualification_pass": int(source_pass),
        })
        print(
            f"[v16y] sources={run_index}/6 replay={int(reference_pass)} "
            f"reversible={int(reversibility_pass)} movement={int(movement_pass)} "
            f"stability={int(stability_pass)} comparison={comparison['measure_comparison_pass']}"
        )

    expected_reference = 6 * (v16x.PRIMARY_REPLICATES + v16x.SENSITIVITY_REPLICATES)
    expected_endpoints = 6 * len(START_FAMILIES) * len(CHAIN_SEED_FAMILIES) * SAMPLES_PER_CHAIN
    integrity_pass = (
        len(endpoint_rows) == expected_endpoints
        and all(int(row["endpoint_integrity_pass"]) for row in endpoint_rows)
        and calls == {"spectrum_calls": 0, "effect_metric_calls": 0}
    )
    reference_pass = (
        len(reference_rows) == expected_reference
        and all(int(row["digest_replay_pass"]) for row in reference_rows)
        and all(int(row["endpoint_integrity_pass"]) for row in reference_rows)
    )
    reversibility_pass = all(int(row["detailed_balance_pass"]) for row in reversibility)
    representation_pass = all(int(row["representation_pass"]) for row in representations)
    movement_pass = all(int(row["movement_pass"]) for row in transitions)
    center_pass = all(int(row["center_stability_pass"]) for row in stability)
    improved_sources = sum(int(row["measure_comparison_pass"]) for row in comparisons)
    comparison_pass = improved_sources >= MIN_IMPROVED_SOURCES

    if not integrity_pass or not reference_pass:
        overall = "v16y_reversible_measure_instrumentation_failed"
    elif not reversibility_pass:
        overall = "v16y_detailed_balance_not_qualified"
    elif not representation_pass:
        overall = "v16y_chain_representation_not_qualified"
    elif not movement_pass:
        overall = "v16y_2x2_chain_finite_mobility_not_qualified"
    elif not center_pass:
        overall = "v16y_2x2_chain_finite_centers_not_stable"
    elif not comparison_pass:
        overall = "v16y_2x2_chain_concentration_profile_not_improved"
    else:
        overall = "v16y_reversible_component_measure_finitely_qualified"

    gates = [
        {
            "gate": "effect_blind_endpoint_integrity",
            "status": "pass" if integrity_pass else "fail",
            "observed": f"endpoints={sum(int(row['endpoint_integrity_pass']) for row in endpoint_rows)}/{len(endpoint_rows)};spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}",
            "required": f"{expected_endpoints}/{expected_endpoints};0;0",
            "decision": "continue" if integrity_pass else "instrumentation_failed",
        },
        {
            "gate": "frozen_random_cost_reference_replay",
            "status": "pass" if reference_pass else "fail",
            "observed": f"{sum(int(row['digest_replay_pass']) for row in reference_rows)}/{len(reference_rows)}",
            "required": f"{expected_reference}/{expected_reference}",
            "decision": "continue" if reference_pass else "reference_mismatch",
        },
        {
            "gate": "exact_detailed_balance_reversibility",
            "status": "pass" if reversibility_pass else "fail",
            "observed": f"{sum(int(row['detailed_balance_pass']) for row in reversibility)}/{len(reversibility)}",
            "required": f"{len(reversibility)}/{len(reversibility)}",
            "decision": "continue" if reversibility_pass else "repair_proposal",
        },
        {
            "gate": "representation_covariance",
            "status": "pass" if representation_pass else "fail",
            "observed": f"{sum(int(row['representation_pass']) for row in representations)}/{len(representations)}",
            "required": f"{len(representations)}/{len(representations)}",
            "decision": "continue" if representation_pass else "repair_representation",
        },
        {
            "gate": "finite_chain_mobility",
            "status": "pass" if movement_pass else "fail",
            "observed": f"chains={sum(int(row['movement_pass']) for row in transitions)}/{len(transitions)}",
            "required": f"chains={len(transitions)}/{len(transitions)}",
            "decision": "continue" if movement_pass else "increase_budget_or_move_class",
        },
        {
            "gate": "start_seed_time_center_stability",
            "status": "pass" if center_pass else "fail",
            "observed": f"features={sum(int(row['center_stability_pass']) for row in stability)}/{len(stability)}",
            "required": f"{len(stability)}/{len(stability)}",
            "decision": "continue" if center_pass else "not_finitely_stable",
        },
        {
            "gate": "concentration_profile_improvement",
            "status": "pass" if comparison_pass else "fail",
            "observed": f"sources={improved_sources}/6",
            "required": f"sources>={MIN_IMPROVED_SOURCES}/6",
            "decision": "finitely_qualified" if comparison_pass else "profile_not_improved",
        },
        {
            "gate": "v16y_overall",
            "status": overall,
            "observed": f"integrity={int(integrity_pass)};reference={int(reference_pass)};reversibility={int(reversibility_pass)};representation={int(representation_pass)};movement={int(movement_pass)};centers={int(center_pass)};profile={int(comparison_pass)}",
            "required": "1;1;1;1;1;1;1",
            "decision": overall,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "The implemented lazy degree-corrected 2x2 chain satisfies detailed balance for the declared component-uniform target on tested transitions.",
            "status": "supported" if reversibility_pass else "not_supported",
            "evidence": REVERSIBILITY_AUDIT.name,
            "scope_limit": "finite implementation witnesses; stationary target is per connected component",
        },
        {
            "claim_id": "C2",
            "claim": "The chain has adequate finite mobility and start/seed/time stability under the preregistered 512-step budget.",
            "status": "supported" if movement_pass and center_pass else "not_supported",
            "evidence": f"{TRANSITION_SUMMARY.name};{STABILITY_AUDIT.name}",
            "scope_limit": "six frozen sources; finite diagnostics do not prove mixing",
        },
        {
            "claim_id": "C3",
            "claim": "The component-uniform chain improves concentration while retaining at least half the random-cost reference support on at least four sources.",
            "status": "supported" if comparison_pass else "not_supported",
            "evidence": f"{CONCENTRATION_PROFILE.name};{MEASURE_COMPARISON.name}",
            "scope_limit": "32 endpoints per law and source",
        },
        {
            "claim_id": "C4",
            "claim": "V16y proves global connectivity, mixing, global uniformity, maximum entropy, or a canonical null.",
            "status": "not_supported",
            "evidence": REPORT.name,
            "scope_limit": "explicit exclusions",
        },
        {
            "claim_id": "C5",
            "claim": "V16y reproduces or updates the v16s spectrum effect.",
            "status": "not_supported",
            "evidence": GATE_EVALUATION.name,
            "scope_limit": "source spectrum and effect metrics excluded",
        },
    ]

    v16i.write_csv(REVERSIBILITY_AUDIT, reversibility)
    v16i.write_csv(REPRESENTATION_AUDIT, representations)
    v16i.write_csv(REFERENCE_REPLAY, reference_rows)
    v16i.write_csv(TRANSITION_SUMMARY, transitions)
    v16i.write_csv(ENDPOINT_AUDIT, endpoint_rows)
    v16i.write_csv(PAIRWISE_DISTANCE, pairwise)
    v16i.write_csv(STABILITY_AUDIT, stability)
    v16i.write_csv(CONCENTRATION_PROFILE, profiles)
    v16i.write_csv(MEASURE_COMPARISON, comparisons)
    v16i.write_csv(SOURCE_SUMMARY, summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    REPORT.write_text(build_report(summaries, gates, comparisons, overall), encoding="utf-8")
    INTERPRETATION.write_text(
        "# v16y interpretation audit\n\n"
        f"Frozen overall status: `{overall}`.\n\n"
        "The algebraic result is limited to detailed balance for the implemented lazy Metropolis transitions. The generated chain products are finite diagnostics on six reused state spaces. They do not prove global irreducibility, mixing or global uniformity. No source spectrum or observed-effect statistic was computed.\n\n"
        f"The concentration-profile comparison passed on `{improved_sources}/6` sources; the preregistered requirement was at least `{MIN_IMPROVED_SOURCES}/6`. Read `v16y_measure_comparison.csv`, `v16y_chain_transition_summary.csv`, and `v16y_chain_center_stability.csv` before assigning sampler meaning.\n",
        encoding="utf-8",
    )
    if overall == "v16y_reversible_component_measure_finitely_qualified":
        next_text = (
            "Run a fresh-history effect-blind transfer qualification of the same chain before any spectrum statistic. Preserve the 512-step budget and all diagnostics. Only after transfer passes should an independent-null effect gate be preregistered."
        )
    elif not movement_pass:
        next_text = (
            "Do not add spectrum or effect. Determine whether the smallest repair is a larger preregistered budget or a reversible longer alternating-cycle move; use the transition rows to distinguish slow movement from trapping."
        )
    elif not center_pass:
        next_text = (
            "Do not add spectrum or effect. Use one budget-doubling center-stability gate with the same proposal and no threshold changes; retire the 2x2 chain if start or time-window dependence persists."
        )
    else:
        next_text = (
            "Do not add spectrum or effect. Compare a reversible longer-cycle proposal on the same state space because the 2x2 component law did not improve the concentration/support profile sufficiently."
        )
    NEXT_DIRECTION.write_text(
        "# v16y next direction\n\n"
        f"Status: `{overall}`.\n\n{next_text}\n",
        encoding="utf-8",
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling etter v16y\n\n"
        f"Status: `{overall}`.\n\n{next_text}\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf etter v16y\n\n"
        "Runden sammenligner to maater aa trekke gyldige aarsaksgrafer paa. Den nye kjeden er konstruert slik at hvert lovlig bytte har samme korrigerte sannsynlighet begge veier, men bare innen den delen av grafrommet som slike bytter faktisk kan naa.\n\n"
        f"Statusen er `{overall}`. Dette er en kontroll av utvalgsmetoden, ikke et bevis for romtid, partikler eller naturlover.\n",
        encoding="utf-8",
    )
    print(f"[v16y] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    reversibility = v16i.read_csv(REVERSIBILITY_AUDIT)
    representations = v16i.read_csv(REPRESENTATION_AUDIT)
    reference = v16i.read_csv(REFERENCE_REPLAY)
    transitions = v16i.read_csv(TRANSITION_SUMMARY)
    endpoints = v16i.read_csv(ENDPOINT_AUDIT)
    pairwise = v16i.read_csv(PAIRWISE_DISTANCE)
    stability = v16i.read_csv(STABILITY_AUDIT)
    profiles = v16i.read_csv(CONCENTRATION_PROFILE)
    comparisons = v16i.read_csv(MEASURE_COMPARISON)
    summaries = v16i.read_csv(SOURCE_SUMMARY)
    gates = v16i.read_csv(GATE_EVALUATION)
    expected_endpoints = 6 * len(START_FAMILIES) * len(CHAIN_SEED_FAMILIES) * SAMPLES_PER_CHAIN
    expected_pairwise = 6 * (32 * 31 // 2)
    if len(reversibility) != 6 * len(START_FAMILIES) * REVERSIBILITY_WITNESSES_PER_START:
        raise ValueError("v16y reversibility row count failed")
    if len(representations) != 6 or len(reference) != 192:
        raise ValueError("v16y representation/reference row count failed")
    if len(transitions) != 24 or len(endpoints) != expected_endpoints:
        raise ValueError("v16y transition/endpoint row count failed")
    if len(pairwise) != expected_pairwise or len(stability) != 6 * 3 * len(CENTER_FEATURES):
        raise ValueError("v16y pairwise/stability row count failed")
    if len(profiles) != 12 or len(comparisons) != 6 or len(summaries) != 6:
        raise ValueError("v16y profile/summary row count failed")
    if not all(int(row["endpoint_integrity_pass"]) for row in endpoints):
        raise ValueError("v16y endpoint integrity failed")
    if not all(int(row["digest_replay_pass"]) for row in reference):
        raise ValueError("v16y reference replay failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16y_overall")
    allowed = {
        "v16y_reversible_measure_instrumentation_failed",
        "v16y_detailed_balance_not_qualified",
        "v16y_chain_representation_not_qualified",
        "v16y_2x2_chain_finite_mobility_not_qualified",
        "v16y_2x2_chain_finite_centers_not_stable",
        "v16y_2x2_chain_concentration_profile_not_improved",
        "v16y_reversible_component_measure_finitely_qualified",
    }
    if overall not in allowed:
        raise ValueError("v16y unknown overall status")
    exclusion = next(row for row in gates if row["gate"] == "effect_blind_endpoint_integrity")
    if "spectrum=0;effect=0" not in exclusion["observed"]:
        raise ValueError("v16y effect exclusion failed")
    for path in (REPORT, INTERPRETATION, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"v16y missing report {path.name}")
    print(f"[v16y] output verification pass overall={overall}")


def self_test() -> None:
    role: v16v.Role = ("test", ("resource",))
    klass: v16v.SlotClass = (role, 0, "witness")
    candidates = ((0, 2), (0, 3), (1, 2), (1, 3))
    space = v16x.StateSpace(
        arm="test",
        candidates=candidates,
        source_edges=frozenset({(0, 2), (1, 3)}),
        slot_by_edge={edge: (edge[1], klass) for edge in candidates},
        parent_demands={0: 1, 1: 1},
        slot_demands={(2, klass): 1, (3, klass): 1},
        edge_count=2,
    )
    kernel = build_kernel(space)
    moves = neighbor_moves(kernel, space.source_edges)
    if len(moves) != 1:
        raise AssertionError("v16y 2x2 neighbor enumeration failed")
    other = apply_move(space, space.source_edges, moves[0])
    reverse = neighbor_moves(kernel, other)
    if reverse_move(moves[0]) not in reverse:
        raise AssertionError("v16y reverse move failed")
    if accepted_transition_probability(len(moves), len(reverse)) != Fraction(1, 2):
        raise AssertionError("v16y detailed balance probability failed")
    first, _, _, _ = advance_chain(kernel, space.source_edges, 7, total_steps=32)
    second, _, _, _ = advance_chain(kernel, space.source_edges, 7, total_steps=32)
    reversed_space = v16x.StateSpace(
        arm=space.arm,
        candidates=tuple(reversed(space.candidates)),
        source_edges=space.source_edges,
        slot_by_edge=space.slot_by_edge,
        parent_demands=space.parent_demands,
        slot_demands=space.slot_demands,
        edge_count=space.edge_count,
    )
    reordered, _, _, _ = advance_chain(
        build_kernel(reversed_space), space.source_edges, 7, total_steps=32
    )
    if first != second or first != reordered:
        raise AssertionError("v16y replay/order covariance failed")
    if implementation_call_counts() != {"spectrum_calls": 0, "effect_metric_calls": 0}:
        raise AssertionError("v16y effect exclusion audit failed")
    if spec_payload()["source_spectrum_computation_allowed"]:
        raise AssertionError("v16y source spectrum must be prohibited")
    print("[v16y] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16y reversible global-measure gate")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if sum((args.prepare_only, args.self_test, args.verify_only)) > 1:
        parser.error("choose at most one mode")
    if args.prepare_only:
        prepare()
    elif args.self_test:
        self_test()
    elif args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
