#!/usr/bin/env python3
"""v16z effect-blind alternating-cycle and bounded 2x2 bridge gate.

The gate compares the same source/random-cost start pairs used by v16y. It
constructs exact alternating-cycle witnesses between each pair and performs a
bounded deterministic search for a 2x2 path. It computes neither source
spectra nor observed-effect statistics.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16t_footprint_null_path_stability_gate as v16t
import relational_universe_v16w_global_null_qualification_gate as v16w
import relational_universe_v16x_explicit_global_measure_gate as v16x
import relational_universe_v16y_reversible_global_measure_gate as v16y


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

START_LEFT = "source_assignment"
START_RIGHT = "v16x_random_cost_a0"
MAX_BRIDGE_STEPS = 2048
MAX_EXPANDED_STATES = 2048
PLATEAU_SEARCH_DEPTH = 3
PLATEAU_BEAM_WIDTH = 16
MAX_PLATEAU_DISTANCE_INCREASE = 1

SOURCE_CHAIN = DOC / "v16z_source_chain.csv"
PRE_REGISTRATION = DOC / "v16z_pre_registration.csv"
CYCLE_DECOMPOSITION = DOC / "v16z_alternating_cycle_decomposition.csv"
REVERSIBILITY_AUDIT = DOC / "v16z_whole_cycle_reversibility_audit.csv"
REPRESENTATION_AUDIT = DOC / "v16z_representation_audit.csv"
BRIDGE_SUMMARY = DOC / "v16z_2x2_bridge_search_summary.csv"
BRIDGE_TRACE = DOC / "v16z_2x2_bridge_trace.csv"
SOURCE_SUMMARY = DOC / "v16z_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v16z_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16z_claim_ledger.csv"
REPORT = DOC / "v16z_alternating_cycle_bridge_gate.md"
INTERPRETATION = DOC / "v16z_interpretation_audit.md"
NEXT_DIRECTION = DOC / "v16z_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_16z_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16z.md"

Edge = v16x.Edge
Slot = v16x.Slot
BNode = Tuple[Any, ...]


@dataclass(frozen=True)
class DirectedDifferenceEdge:
    source: BNode
    target: BNode
    edge: Edge
    kind: str


@dataclass(frozen=True)
class CycleExchange:
    remove: Tuple[Edge, ...]
    add: Tuple[Edge, ...]


@dataclass
class BridgeResult:
    status: str
    path: List[v16y.SwapMove]
    trace: List[Dict[str, Any]]
    expanded_states: int
    generated_states: int
    initial_mismatch: int
    final_mismatch: int
    replay_pass: bool
    reverse_replay_pass: bool


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v16x", "frozen_state_space", v16x.PRE_REGISTRATION),
        ("v16x", "frozen_reference_endpoints", v16x.ENDPOINT_AUDIT),
        ("v16y", "reversible_measure_preregistration", v16y.PRE_REGISTRATION),
        ("v16y", "failed_start_stability_gate", v16y.GATE_EVALUATION),
        ("v16y", "start_separation_audit", DOC / "v16y_postrun_start_separation_audit.csv"),
        ("v16y", "interpretation_boundary", DOC / "v16y_interpretation_audit.md"),
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
        "gate": "v16z_alternating_cycle_bridge_gate",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_pair_accessibility_on_frozen_coarse_state_spaces",
        "source_history_count": 6,
        "state_space": v16x.COARSE_ARM,
        "start_pair": [START_LEFT, START_RIGHT],
        "right_start": "v16x_primary_seed_family_replicate_0",
        "cycle_representation": "directed_parent_slot_symmetric_difference",
        "cycle_move": "pair_specific_whole_alternating_cycle_exchange",
        "cycle_requirements": [
            "complete_symmetric_difference_coverage",
            "assignment_integrity_after_each_exchange",
            "exact_forward_and_reverse_replay",
        ],
        "bridge_move": "v16y_valid_2x2_switch",
        "bridge_search": "deterministic_monotone_then_bounded_plateau_beam",
        "instrumentation_repair_disclosure": (
            "the first preregistered execution was interrupted before any source result "
            "because plateau candidates were materialized before beam pruning; the repaired "
            "implementation retains only the streaming top-k candidates while preserving all "
            "search budgets, rankings, thresholds, and decision rules"
        ),
        "max_bridge_steps": MAX_BRIDGE_STEPS,
        "max_expanded_states": MAX_EXPANDED_STATES,
        "plateau_search_depth": PLATEAU_SEARCH_DEPTH,
        "plateau_beam_width": PLATEAU_BEAM_WIDTH,
        "max_plateau_distance_increase": MAX_PLATEAU_DISTANCE_INCREASE,
        "pre_result_streaming_memory_repair": 1,
        "failed_bounded_search_interpretation": "unresolved_not_disconnected",
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "no_early_stop": True,
        "not_claimed": [
            "global_irreducibility", "global_connectivity", "mixing", "stationarity",
            "global_uniform_sampling", "maximum_entropy", "canonical_measure",
            "disconnected_components_from_failed_search", "spectrum_effect", "physics",
            "energy", "temperature", "dimension", "Lorentz_symmetry", "spacetime",
            "particles", "entanglement",
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
        "start_pair": f"{START_LEFT};{START_RIGHT}",
        "right_start_replicate": 0,
        "max_bridge_steps": MAX_BRIDGE_STEPS,
        "max_expanded_states": MAX_EXPANDED_STATES,
        "plateau_search_depth": PLATEAU_SEARCH_DEPTH,
        "plateau_beam_width": PLATEAU_BEAM_WIDTH,
        "max_plateau_distance_increase": MAX_PLATEAU_DISTANCE_INCREASE,
        "all_cycle_integrity_required": 1,
        "all_cycle_reverse_replay_required": 1,
        "all_representation_checks_required": 1,
        "failed_bounded_search_means_disconnected": 0,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v16y.verify_outputs()
    overall = next(
        row["status"] for row in v16i.read_csv(v16y.GATE_EVALUATION)
        if row["gate"] == "v16y_overall"
    )
    if overall != "v16y_2x2_chain_finite_centers_not_stable":
        raise ValueError("v16z requires the frozen v16y start-stability failure")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v16z] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    expected = {key: str(value) for key, value in preregistration_row().items()}
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v16z preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v16z source chain changed")


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    runs = []
    for source, metadata in v16x.load_runs():
        runs.append((v16i.RunDAG(
            stage="v16z",
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


def random_cost_start(dag: v16i.RunDAG, space: v16x.StateSpace) -> frozenset[Edge]:
    _, costs = v16x.edge_costs(dag, space, v16x.PRIMARY_SEED_FAMILY, 0)
    edges, _, _ = v16x.solve_edges(space, costs)
    return edges


def frozen_start_digests() -> Dict[Tuple[int, int, str], str]:
    rows = v16i.read_csv(v16y.TRANSITION_SUMMARY)
    result: Dict[Tuple[int, int, str], str] = {}
    for row in rows:
        key = (int(row["growth_seed"]), int(row["run_offset"]), row["start_family"])
        digest = row["start_endpoint_sha256"]
        if key in result and result[key] != digest:
            raise ValueError("v16y start digest changed within family")
        result[key] = digest
    return result


def parent_node(parent: int) -> BNode:
    return ("parent", parent)


def slot_node(slot: Slot) -> BNode:
    return ("slot", slot[0], slot[1])


def node_key(node: BNode) -> str:
    return repr(node)


def directed_difference_edges(
    space: v16x.StateSpace,
    left: frozenset[Edge],
    right: frozenset[Edge],
) -> Dict[int, DirectedDifferenceEdge]:
    result: Dict[int, DirectedDifferenceEdge] = {}
    index = 0
    for edge in sorted(left - right):
        result[index] = DirectedDifferenceEdge(
            parent_node(edge[0]), slot_node(space.slot_by_edge[edge]), edge, "remove"
        )
        index += 1
    for edge in sorted(right - left):
        result[index] = DirectedDifferenceEdge(
            slot_node(space.slot_by_edge[edge]), parent_node(edge[0]), edge, "add"
        )
        index += 1
    return result


def difference_balance(edges: Mapping[int, DirectedDifferenceEdge]) -> bool:
    indegree: Counter[BNode] = Counter()
    outdegree: Counter[BNode] = Counter()
    for arc in edges.values():
        outdegree[arc.source] += 1
        indegree[arc.target] += 1
    return indegree == outdegree


def arc_key(arc: DirectedDifferenceEdge) -> Tuple[str, str, str, Edge]:
    return node_key(arc.source), node_key(arc.target), arc.kind, arc.edge


def decompose_alternating_cycles(
    space: v16x.StateSpace,
    left: frozenset[Edge],
    right: frozenset[Edge],
) -> Tuple[CycleExchange, ...]:
    if not v16x.assignment_integrity(space, left) or not v16x.assignment_integrity(space, right):
        raise ValueError("cycle decomposition requires two valid assignments")
    remaining = directed_difference_edges(space, left, right)
    if not difference_balance(remaining):
        raise ValueError("symmetric difference is not balanced")
    cycles: List[CycleExchange] = []
    while remaining:
        start_id = min(remaining, key=lambda item: arc_key(remaining[item]))
        start_node = remaining[start_id].source
        path_nodes = [start_node]
        positions = {start_node: 0}
        path_arcs: List[int] = []
        current = start_node
        while True:
            outgoing = [
                item for item, arc in remaining.items()
                if arc.source == current and item not in path_arcs
            ]
            if not outgoing:
                raise ValueError("balanced difference walk became trapped")
            selected_id = min(outgoing, key=lambda item: arc_key(remaining[item]))
            selected = remaining[selected_id]
            path_arcs.append(selected_id)
            current = selected.target
            if current in positions:
                cycle_ids = path_arcs[positions[current]:]
                cycle_arcs = [remaining[item] for item in cycle_ids]
                remove = tuple(sorted(arc.edge for arc in cycle_arcs if arc.kind == "remove"))
                add = tuple(sorted(arc.edge for arc in cycle_arcs if arc.kind == "add"))
                if not remove or len(remove) != len(add) or len(cycle_arcs) % 2:
                    raise ValueError("difference circuit was not a nonempty alternating cycle")
                cycles.append(CycleExchange(remove=remove, add=add))
                for item in cycle_ids:
                    del remaining[item]
                break
            positions[current] = len(path_nodes)
            path_nodes.append(current)
        if not difference_balance(remaining):
            raise ValueError("cycle removal broke residual balance")
    cycles.sort(key=cycle_digest)
    return tuple(cycles)


def cycle_digest(cycle: CycleExchange) -> str:
    payload = json.dumps({"remove": cycle.remove, "add": cycle.add}, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def apply_cycle(
    space: v16x.StateSpace,
    selected: frozenset[Edge],
    cycle: CycleExchange,
) -> frozenset[Edge]:
    if not set(cycle.remove).issubset(selected) or set(cycle.add) & selected:
        raise ValueError("cycle occupancy is invalid")
    result = frozenset((set(selected) - set(cycle.remove)) | set(cycle.add))
    if not v16x.assignment_integrity(space, result):
        raise ValueError("whole-cycle exchange broke assignment integrity")
    return result


def reverse_cycle(cycle: CycleExchange) -> CycleExchange:
    return CycleExchange(remove=cycle.add, add=cycle.remove)


def cycle_rows_and_audit(
    dag: v16i.RunDAG,
    space: v16x.StateSpace,
    left: frozenset[Edge],
    right: frozenset[Edge],
    cycles: Sequence[CycleExchange],
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    difference = left ^ right
    rows: List[Dict[str, Any]] = []
    current = left
    covered: set[Edge] = set()
    forward_pass = True
    for index, cycle in enumerate(cycles):
        before = current
        current = apply_cycle(space, current, cycle)
        covered.update(cycle.remove)
        covered.update(cycle.add)
        reverse_pass = apply_cycle(space, current, reverse_cycle(cycle)) == before
        forward_pass = forward_pass and reverse_pass
        rows.append({
            **dag.prefix,
            "cycle_index": index,
            "exchange_size": len(cycle.remove),
            "changed_edge_count": 2 * len(cycle.remove),
            "changed_edge_fraction_of_pair_difference": (
                2 * len(cycle.remove) / len(difference) if difference else 0.0
            ),
            "remove_edges_json": json.dumps(cycle.remove, separators=(",", ":")),
            "add_edges_json": json.dumps(cycle.add, separators=(",", ":")),
            "cycle_sha256": cycle_digest(cycle),
            "forward_integrity_pass": 1,
            "immediate_reverse_replay_pass": int(reverse_pass),
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })
    final_pass = current == right
    reverse_current = right
    for cycle in reversed(cycles):
        reverse_current = apply_cycle(space, reverse_current, reverse_cycle(cycle))
    reverse_path_pass = reverse_current == left
    coverage_pass = covered == difference
    audit = {
        **dag.prefix,
        "source_edge_count": len(left),
        "pair_symmetric_difference_edge_count": len(difference),
        "pair_changed_selected_edge_fraction": len(left - right) / len(left),
        "cycle_count": len(cycles),
        "minimum_cycle_changed_edge_count": min((2 * len(c.remove) for c in cycles), default=0),
        "maximum_cycle_changed_edge_count": max((2 * len(c.remove) for c in cycles), default=0),
        "mean_cycle_changed_edge_count": (
            sum(2 * len(c.remove) for c in cycles) / len(cycles) if cycles else 0.0
        ),
        "symmetric_difference_coverage_pass": int(coverage_pass),
        "sequential_forward_replay_pass": int(final_pass),
        "sequential_reverse_replay_pass": int(reverse_path_pass),
        "all_immediate_reverse_replay_pass": int(forward_pass),
        "whole_cycle_reversibility_pass": int(
            coverage_pass and final_pass and reverse_path_pass and forward_pass
        ),
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }
    return rows, audit


def cycle_signature(cycles: Sequence[CycleExchange]) -> Tuple[str, ...]:
    return tuple(sorted(cycle_digest(cycle) for cycle in cycles))


def representation_row(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    space: v16x.StateSpace,
    left: frozenset[Edge],
    right: frozenset[Edge],
    cycles: Sequence[CycleExchange],
) -> Dict[str, Any]:
    replay = decompose_alternating_cycles(space, left, right)
    reversed_space = v16x.StateSpace(
        arm=space.arm,
        candidates=tuple(reversed(space.candidates)),
        source_edges=space.source_edges,
        slot_by_edge=space.slot_by_edge,
        parent_demands=space.parent_demands,
        slot_demands=space.slot_demands,
        edge_count=space.edge_count,
    )
    reordered = decompose_alternating_cycles(reversed_space, left, right)
    relabeled_metadata = v16w.relabel_metadata(
        metadata, v16i.stable_seed("v16z", "semantic_relabel", *dag.key)
    )
    relabeled_space = v16x.build_state_space(dag, relabeled_metadata, v16x.COARSE_ARM)
    relabeled_right = random_cost_start(dag, relabeled_space)
    relabeled = decompose_alternating_cycles(
        relabeled_space, relabeled_space.source_edges, relabeled_right
    )
    original_signature = cycle_signature(cycles)
    exact_replay = original_signature == cycle_signature(replay)
    order_covariance = original_signature == cycle_signature(reordered)
    candidate_covariance = space.candidates == relabeled_space.candidates
    start_covariance = left == relabeled_space.source_edges and right == relabeled_right
    semantic_covariance = original_signature == cycle_signature(relabeled)
    kernel_covariance = (
        v16y.build_kernel(space).candidate_parents_by_slot
        == v16y.build_kernel(reversed_space).candidate_parents_by_slot
        == v16y.build_kernel(relabeled_space).candidate_parents_by_slot
    )
    passed = all((
        exact_replay, order_covariance, candidate_covariance, start_covariance,
        semantic_covariance, kernel_covariance,
    ))
    return {
        **dag.prefix,
        "cycle_signature_sha256": hashlib.sha256(
            json.dumps(original_signature).encode("utf-8")
        ).hexdigest(),
        "exact_replay_pass": int(exact_replay),
        "candidate_order_covariance_pass": int(order_covariance),
        "candidate_set_covariance_pass": int(candidate_covariance),
        "start_pair_covariance_pass": int(start_covariance),
        "semantic_relabel_covariance_pass": int(semantic_covariance),
        "bridge_kernel_covariance_pass": int(kernel_covariance),
        "representation_pass": int(passed),
    }


def mismatch(selected: frozenset[Edge], target: frozenset[Edge]) -> int:
    return len(selected - target)


def mismatch_after_move(
    current_mismatch: int,
    target: frozenset[Edge],
    move: v16y.SwapMove,
) -> int:
    removed_wrong = sum(edge not in target for edge in move.remove)
    added_wrong = sum(edge not in target for edge in move.add)
    return current_mismatch - removed_wrong + added_wrong


def move_key(move: v16y.SwapMove) -> Tuple[Tuple[Edge, ...], Tuple[Edge, ...]]:
    return move.remove, move.add


def bounded_plateau_escape(
    kernel: v16y.ChainKernel,
    start: frozenset[Edge],
    target: frozenset[Edge],
    baseline: int,
    expansion_budget: int,
) -> Tuple[List[v16y.SwapMove] | None, int, int]:
    frontier: List[Tuple[frozenset[Edge], List[v16y.SwapMove], int]] = [
        (start, [], baseline)
    ]
    seen = {v16x.edge_digest(start)}
    expanded = generated = 0
    for _depth in range(1, PLATEAU_SEARCH_DEPTH + 1):
        candidates: List[Tuple[frozenset[Edge], List[v16y.SwapMove], int]] = []
        candidate_digests: set[str] = set()
        best_escape: Tuple[frozenset[Edge], List[v16y.SwapMove], int] | None = None

        def rank(item: Tuple[frozenset[Edge], List[v16y.SwapMove], int]) -> Tuple[Any, ...]:
            return item[2], len(item[1]), tuple(move_key(move) for move in item[1])

        def materialize(
            state: frozenset[Edge], move: v16y.SwapMove
        ) -> frozenset[Edge]:
            # neighbor_moves already proves occupancy and assignment validity. Avoid
            # repeating the O(edge_count) integrity audit for discarded beam candidates.
            return frozenset((state - set(move.remove)) | set(move.add))

        for state, path, state_mismatch in frontier:
            if expanded >= expansion_budget:
                return None, expanded, generated
            expanded += 1
            for move in v16y.neighbor_moves(kernel, state):
                proposed_mismatch = mismatch_after_move(state_mismatch, target, move)
                if proposed_mismatch > baseline + MAX_PLATEAU_DISTANCE_INCREASE:
                    continue
                generated += 1
                proposed_path = path + [move]
                path_rank = (
                    proposed_mismatch, len(proposed_path),
                    tuple(move_key(value) for value in proposed_path),
                )
                if proposed_mismatch < baseline:
                    if best_escape is not None and path_rank >= rank(best_escape):
                        continue
                    proposed = materialize(state, move)
                    digest = v16x.edge_digest(proposed)
                    if digest in seen:
                        continue
                    best_escape = (proposed, proposed_path, proposed_mismatch)
                    continue
                if len(candidates) >= PLATEAU_BEAM_WIDTH and path_rank >= rank(candidates[-1]):
                    continue
                proposed = materialize(state, move)
                digest = v16x.edge_digest(proposed)
                if digest in seen or digest in candidate_digests:
                    continue
                item = (proposed, proposed_path, proposed_mismatch)
                candidates.append(item)
                candidate_digests.add(digest)
                candidates.sort(key=rank)
                if len(candidates) > PLATEAU_BEAM_WIDTH:
                    removed = candidates.pop()
                    candidate_digests.remove(v16x.edge_digest(removed[0]))
        if best_escape is not None:
            return best_escape[1], expanded, generated
        frontier = candidates
        seen.update(v16x.edge_digest(item[0]) for item in frontier)
        if not frontier:
            break
    return None, expanded, generated


def bounded_bridge_search(
    kernel: v16y.ChainKernel,
    start: frozenset[Edge],
    target: frozenset[Edge],
) -> BridgeResult:
    current = start
    current_mismatch = mismatch(current, target)
    initial_mismatch = current_mismatch
    path: List[v16y.SwapMove] = []
    trace: List[Dict[str, Any]] = []
    expanded = generated = 0
    status = "unresolved_no_admissible_progress"
    while current != target:
        if len(path) >= MAX_BRIDGE_STEPS:
            status = "unresolved_step_budget"
            break
        if expanded >= MAX_EXPANDED_STATES:
            status = "unresolved_expansion_budget"
            break
        expanded += 1
        moves = v16y.neighbor_moves(kernel, current)
        generated += len(moves)
        ranked = sorted(
            ((mismatch_after_move(current_mismatch, target, move), move) for move in moves),
            key=lambda item: (item[0], move_key(item[1])),
        )
        selected_path: List[v16y.SwapMove] | None = None
        search_kind = "monotone"
        if ranked and ranked[0][0] < current_mismatch:
            selected_path = [ranked[0][1]]
        else:
            search_kind = "plateau_escape"
            remaining_expansions = MAX_EXPANDED_STATES - expanded
            selected_path, used, produced = bounded_plateau_escape(
                kernel, current, target, current_mismatch, remaining_expansions
            )
            expanded += used
            generated += produced
        if not selected_path:
            status = (
                "unresolved_expansion_budget"
                if expanded >= MAX_EXPANDED_STATES
                else "unresolved_no_admissible_progress"
            )
            break
        if len(path) + len(selected_path) > MAX_BRIDGE_STEPS:
            status = "unresolved_step_budget"
            break
        for move in selected_path:
            before = current_mismatch
            before_digest = v16x.edge_digest(current)
            current = v16y.apply_move(kernel.space, current, move)
            current_mismatch = mismatch(current, target)
            path.append(move)
            trace.append({
                "bridge_step": len(path),
                "search_kind": search_kind,
                "mismatch_before": before,
                "mismatch_after": current_mismatch,
                "remove_edges_json": json.dumps(move.remove, separators=(",", ":")),
                "add_edges_json": json.dumps(move.add, separators=(",", ":")),
                "endpoint_before_sha256": before_digest,
                "endpoint_after_sha256": v16x.edge_digest(current),
            })
    if current == target:
        status = "exact_bridge_found"

    replay = start
    replay_pass = True
    try:
        for move in path:
            replay = v16y.apply_move(kernel.space, replay, move)
        replay_pass = replay == current
    except ValueError:
        replay_pass = False
    reverse = current
    reverse_pass = True
    try:
        for move in reversed(path):
            reverse = v16y.apply_move(kernel.space, reverse, v16y.reverse_move(move))
        reverse_pass = reverse == start
    except ValueError:
        reverse_pass = False
    return BridgeResult(
        status=status,
        path=path,
        trace=trace,
        expanded_states=expanded,
        generated_states=generated,
        initial_mismatch=initial_mismatch,
        final_mismatch=current_mismatch,
        replay_pass=replay_pass,
        reverse_replay_pass=reverse_pass,
    )


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
    overall: str,
) -> str:
    lines = [
        "# v16z alternating-cycle bridge gate",
        "",
        f"Status: `{overall}`.",
        "",
        "## Evidential status",
        "",
        "This gate is effect-blind. It reuses the six frozen v16x/v16y coarse state spaces and the same source/random-cost start pairs. No source spectrum or observed-effect statistic is computed.",
        "",
        "The alternating-cycle rows are exact finite combinatorial witnesses between each declared start pair. They qualify pair-specific whole-cycle exchanges, not a state-independent stochastic proposal and not a global probability law.",
        "",
        f"The 2x2 search is bounded at `{MAX_BRIDGE_STEPS}` path steps and `{MAX_EXPANDED_STATES}` expanded states per pair, with plateau depth `{PLATEAU_SEARCH_DEPTH}` and beam `{PLATEAU_BEAM_WIDTH}`. Failure to find a path is `unresolved`, never proof of disconnected components.",
        "",
        "## Source results",
        "",
    ]
    lines.extend(markdown_table(summaries, (
        "growth_seed", "run_offset", "pair_changed_selected_edge_fraction", "cycle_count",
        "maximum_cycle_changed_edge_count", "whole_cycle_reversibility_pass",
        "bridge_status", "bridge_steps", "bridge_final_mismatch",
    )))
    lines.extend(["", "## Gates", ""])
    lines.extend(markdown_table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "An exact 2x2 bridge proves only that the tested pair lies in one 2x2-switch component. It does not prove global connectivity or mixing. An unresolved bounded search proves neither separation nor slow mixing.",
        "",
        "V16z establishes no spectrum effect, global null law, energy, temperature, invariant, dimension, manifold, Lorentz symmetry, spacetime, particle, entanglement, continuum, or physical law.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    verify_frozen_sources()
    calls = implementation_call_counts()
    expected_digests = frozen_start_digests()
    cycle_rows: List[Dict[str, Any]] = []
    reversibility_rows: List[Dict[str, Any]] = []
    representation_rows: List[Dict[str, Any]] = []
    bridge_rows: List[Dict[str, Any]] = []
    trace_rows: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []

    for run_index, (dag, metadata) in enumerate(load_runs(), start=1):
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        left = space.source_edges
        right = random_cost_start(dag, space)
        left_digest = v16x.edge_digest(left)
        right_digest = v16x.edge_digest(right)
        digest_replay_pass = (
            expected_digests[(dag.growth_seed, dag.run_offset, START_LEFT)] == left_digest
            and expected_digests[(dag.growth_seed, dag.run_offset, START_RIGHT)] == right_digest
        )
        cycles = decompose_alternating_cycles(space, left, right)
        source_cycle_rows, reversibility = cycle_rows_and_audit(
            dag, space, left, right, cycles
        )
        cycle_rows.extend(source_cycle_rows)
        reversibility["frozen_start_digest_replay_pass"] = int(digest_replay_pass)
        reversibility_rows.append(reversibility)
        representation = representation_row(dag, metadata, space, left, right, cycles)
        representation_rows.append(representation)

        bridge = bounded_bridge_search(v16y.build_kernel(space), left, right)
        for row in bridge.trace:
            trace_rows.append({
                **dag.prefix,
                **row,
                "source_spectrum_computed": 0,
                "observed_effect_computed": 0,
            })
        bridge_found = bridge.status == "exact_bridge_found"
        bridge_integrity = bridge.replay_pass and bridge.reverse_replay_pass
        bridge_row = {
            **dag.prefix,
            "bridge_status": bridge.status,
            "initial_mismatch": bridge.initial_mismatch,
            "final_mismatch": bridge.final_mismatch,
            "initial_changed_selected_edge_fraction": bridge.initial_mismatch / len(left),
            "final_changed_selected_edge_fraction": bridge.final_mismatch / len(left),
            "bridge_steps": len(bridge.path),
            "expanded_states": bridge.expanded_states,
            "generated_states": bridge.generated_states,
            "max_bridge_steps": MAX_BRIDGE_STEPS,
            "max_expanded_states": MAX_EXPANDED_STATES,
            "exact_bridge_found": int(bridge_found),
            "forward_replay_pass": int(bridge.replay_pass),
            "reverse_replay_pass": int(bridge.reverse_replay_pass),
            "bridge_integrity_pass": int(bridge_integrity),
            "failed_search_means_disconnected": 0,
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        }
        bridge_rows.append(bridge_row)
        summary = {
            **dag.prefix,
            "pair_changed_selected_edge_fraction": reversibility["pair_changed_selected_edge_fraction"],
            "cycle_count": reversibility["cycle_count"],
            "minimum_cycle_changed_edge_count": reversibility["minimum_cycle_changed_edge_count"],
            "maximum_cycle_changed_edge_count": reversibility["maximum_cycle_changed_edge_count"],
            "mean_cycle_changed_edge_count": reversibility["mean_cycle_changed_edge_count"],
            "whole_cycle_reversibility_pass": reversibility["whole_cycle_reversibility_pass"],
            "representation_pass": representation["representation_pass"],
            "frozen_start_digest_replay_pass": int(digest_replay_pass),
            "bridge_status": bridge.status,
            "bridge_steps": len(bridge.path),
            "bridge_final_mismatch": bridge.final_mismatch,
            "bridge_integrity_pass": int(bridge_integrity),
            "source_qualification_pass": int(
                int(reversibility["whole_cycle_reversibility_pass"])
                and int(representation["representation_pass"])
                and digest_replay_pass
                and bridge_integrity
            ),
        }
        summaries.append(summary)
        print(
            f"[v16z] sources={run_index}/6 cycles={len(cycles)} "
            f"bridge={bridge.status} steps={len(bridge.path)} mismatch={bridge.final_mismatch}"
        )

    exclusion_pass = (
        calls == {"spectrum_calls": 0, "effect_metric_calls": 0}
        and all(int(row["source_spectrum_computed"]) == 0 for row in cycle_rows)
        and all(int(row["observed_effect_computed"]) == 0 for row in bridge_rows)
    )
    digest_pass = all(int(row["frozen_start_digest_replay_pass"]) for row in reversibility_rows)
    cycle_pass = all(int(row["whole_cycle_reversibility_pass"]) for row in reversibility_rows)
    representation_pass = all(int(row["representation_pass"]) for row in representation_rows)
    bridge_integrity_pass = all(int(row["bridge_integrity_pass"]) for row in bridge_rows)
    found_count = sum(int(row["exact_bridge_found"]) for row in bridge_rows)

    if not exclusion_pass or not digest_pass or not bridge_integrity_pass:
        overall = "v16z_accessibility_instrumentation_failed"
    elif not cycle_pass:
        overall = "v16z_whole_cycle_move_not_qualified"
    elif not representation_pass:
        overall = "v16z_cycle_representation_not_qualified"
    elif found_count == 6:
        overall = "v16z_all_tested_start_pairs_2x2_connected"
    elif found_count > 0:
        overall = "v16z_mixed_pair_accessibility_unresolved"
    else:
        overall = "v16z_bounded_2x2_accessibility_unresolved"

    gates = [
        {
            "gate": "effect_blind_integrity",
            "status": "pass" if exclusion_pass else "fail",
            "observed": f"spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}",
            "required": "0;0",
            "decision": "continue" if exclusion_pass else "instrumentation_failed",
        },
        {
            "gate": "frozen_start_pair_replay",
            "status": "pass" if digest_pass else "fail",
            "observed": f"{sum(int(row['frozen_start_digest_replay_pass']) for row in reversibility_rows)}/6",
            "required": "6/6",
            "decision": "continue" if digest_pass else "source_mismatch",
        },
        {
            "gate": "whole_cycle_exact_reversibility",
            "status": "pass" if cycle_pass else "fail",
            "observed": f"{sum(int(row['whole_cycle_reversibility_pass']) for row in reversibility_rows)}/6",
            "required": "6/6",
            "decision": "continue" if cycle_pass else "repair_cycle_move",
        },
        {
            "gate": "representation_covariance",
            "status": "pass" if representation_pass else "fail",
            "observed": f"{sum(int(row['representation_pass']) for row in representation_rows)}/6",
            "required": "6/6",
            "decision": "continue" if representation_pass else "repair_representation",
        },
        {
            "gate": "bounded_2x2_pair_accessibility",
            "status": "all_found" if found_count == 6 else ("mixed" if found_count else "unresolved"),
            "observed": f"exact_bridges={found_count}/6",
            "required": "descriptive_bounded_result",
            "decision": "tested_pairs_connected" if found_count == 6 else "unresolved_not_disconnected",
        },
        {
            "gate": "v16z_overall",
            "status": overall,
            "observed": f"exclusion={int(exclusion_pass)};digests={int(digest_pass)};cycles={int(cycle_pass)};representation={int(representation_pass)};bridges={found_count}/6",
            "required": "1;1;1;1;descriptive",
            "decision": overall,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "Each frozen source/random-cost pair has an exact alternating-cycle decomposition with reversible whole-cycle exchanges.",
            "status": "supported" if cycle_pass else "not_supported",
            "evidence": f"{CYCLE_DECOMPOSITION.name};{REVERSIBILITY_AUDIT.name}",
            "scope_limit": "six pair-specific finite witnesses; not a state-independent proposal law",
        },
        {
            "claim_id": "C2",
            "claim": "The bounded deterministic search found an exact 2x2 bridge for every tested start pair.",
            "status": "supported" if found_count == 6 else "not_supported",
            "evidence": f"{BRIDGE_SUMMARY.name};{BRIDGE_TRACE.name}",
            "scope_limit": "six declared pairs and frozen search budget only",
        },
        {
            "claim_id": "C3",
            "claim": "A failed bounded bridge search proves disconnected 2x2 components.",
            "status": "not_supported",
            "evidence": BRIDGE_SUMMARY.name,
            "scope_limit": "budget exhaustion or heuristic failure remains unresolved",
        },
        {
            "claim_id": "C4",
            "claim": "V16z proves global connectivity, mixing, a global probability law, or maximum entropy.",
            "status": "not_supported",
            "evidence": REPORT.name,
            "scope_limit": "explicit exclusions",
        },
        {
            "claim_id": "C5",
            "claim": "V16z reproduces or updates the v16s spectrum effect.",
            "status": "not_supported",
            "evidence": GATE_EVALUATION.name,
            "scope_limit": "source spectra and effect metrics excluded",
        },
    ]

    v16i.write_csv(CYCLE_DECOMPOSITION, cycle_rows)
    v16i.write_csv(REVERSIBILITY_AUDIT, reversibility_rows)
    v16i.write_csv(REPRESENTATION_AUDIT, representation_rows)
    v16i.write_csv(BRIDGE_SUMMARY, bridge_rows)
    v16i.write_csv(BRIDGE_TRACE, trace_rows)
    v16i.write_csv(SOURCE_SUMMARY, summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    REPORT.write_text(build_report(summaries, gates, overall), encoding="utf-8")

    if found_count == 6:
        interpretation = (
            "All six declared start pairs are connected by explicit 2x2 paths under the frozen bounded search. This rules out pairwise component separation for those six pairs, but not global disconnection elsewhere and not slow mixing. The v16y start separation is therefore better treated as a finite traversal/mixing problem than as evidence that these pairs occupy different components."
        )
        next_text = (
            "Do not open the spectrum effect yet. Preregister one path-length-informed finite mixing gate on the same six spaces, using the qualified 2x2 kernel and budgets scaled from the observed bridge lengths. Require convergence across starts, independent seeds and time windows before treating the component-uniform law as qualified."
        )
    elif found_count > 0:
        interpretation = (
            "Exact 2x2 connectivity was established for only part of the six declared pairs. Remaining failures are bounded-search unresolved, not evidence of disconnection. Pair-specific whole-cycle exchanges are exact witnesses for every pair."
        )
        next_text = (
            "Define and qualify a state-independent symmetric alternating-cycle proposal before spending more 2x2 budget. Preserve the unresolved labels and compare reachability only after proposal reversibility and representation checks pass."
        )
    else:
        interpretation = (
            "No exact 2x2 bridge was found within the frozen search bounds. This is unresolved: it may reflect the deterministic heuristic, the finite budget, or genuine move-component separation. Exact pair-specific whole-cycle exchanges exist for every pair."
        )
        next_text = (
            "Define and qualify a state-independent symmetric alternating-cycle proposal on the same spaces. Do not infer disconnection and do not open spectrum or effect statistics until a probability law passes start/seed/time stability."
        )
    INTERPRETATION.write_text(
        "# v16z interpretation audit\n\n"
        f"Frozen overall status: `{overall}`.\n\n{interpretation}\n\n"
        "The cycle decomposition is algebraic for the six reconstructed start pairs. The bridge products are finite search artifacts. Neither product is a physical observable or a global sampler qualification. No source spectrum or observed-effect statistic was computed.\n",
        encoding="utf-8",
    )
    NEXT_DIRECTION.write_text(
        "# v16z next direction\n\n"
        f"Status: `{overall}`.\n\n{next_text}\n",
        encoding="utf-8",
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling etter v16z\n\n"
        f"Status: `{overall}`.\n\n{next_text}\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf etter v16z\n\n"
        "Runden spoer om to tidligere startgrafer kan kobles sammen med lovlige lokale bytter. Hele forskjellen kan alltid beskrives med balanserte sykluser for de seks testparene, men det er en matematisk egenskap ved disse matchingene og ikke fysikk.\n\n"
        f"Statusen er `{overall}`. Et funnet 2x2-spor gjelder bare det konkrete paret. Et ikke funnet spor innen budsjettet er uavklart, ikke bevis for at rommet er delt.\n",
        encoding="utf-8",
    )
    print(f"[v16z] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    cycles = v16i.read_csv(CYCLE_DECOMPOSITION)
    reversibility = v16i.read_csv(REVERSIBILITY_AUDIT)
    representations = v16i.read_csv(REPRESENTATION_AUDIT)
    bridges = v16i.read_csv(BRIDGE_SUMMARY)
    trace = v16i.read_csv(BRIDGE_TRACE)
    summaries = v16i.read_csv(SOURCE_SUMMARY)
    gates = v16i.read_csv(GATE_EVALUATION)
    claims = v16i.read_csv(CLAIM_LEDGER)
    if not cycles or len(reversibility) != 6 or len(representations) != 6:
        raise ValueError("v16z cycle/reversibility row count failed")
    if len(bridges) != 6 or len(summaries) != 6 or len(claims) != 5:
        raise ValueError("v16z bridge/summary/claim row count failed")
    if not all(int(row["whole_cycle_reversibility_pass"]) for row in reversibility):
        raise ValueError("v16z whole-cycle reversibility failed")
    if not all(int(row["representation_pass"]) for row in representations):
        raise ValueError("v16z representation failed")
    if not all(int(row["bridge_integrity_pass"]) for row in bridges):
        raise ValueError("v16z bridge replay integrity failed")
    expected_trace = sum(int(row["bridge_steps"]) for row in bridges)
    if len(trace) != expected_trace:
        raise ValueError("v16z bridge trace count failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16z_overall")
    allowed = {
        "v16z_accessibility_instrumentation_failed",
        "v16z_whole_cycle_move_not_qualified",
        "v16z_cycle_representation_not_qualified",
        "v16z_all_tested_start_pairs_2x2_connected",
        "v16z_mixed_pair_accessibility_unresolved",
        "v16z_bounded_2x2_accessibility_unresolved",
    }
    if overall not in allowed:
        raise ValueError("v16z unknown overall status")
    exclusion = next(row for row in gates if row["gate"] == "effect_blind_integrity")
    if exclusion["observed"] != "spectrum=0;effect=0":
        raise ValueError("v16z effect exclusion failed")
    for path in (REPORT, INTERPRETATION, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"v16z missing report {path.name}")
    print(f"[v16z] output verification pass overall={overall}")


def self_test() -> None:
    role = ("test", ("resource",))
    klass = (role, 0, "witness")
    candidates = tuple((parent, child) for parent in range(3) for child in range(3, 6))
    source = frozenset({(0, 3), (1, 4), (2, 5)})
    target = frozenset({(0, 4), (1, 5), (2, 3)})
    space = v16x.StateSpace(
        arm="test",
        candidates=candidates,
        source_edges=source,
        slot_by_edge={edge: (edge[1], klass) for edge in candidates},
        parent_demands={0: 1, 1: 1, 2: 1},
        slot_demands={(child, klass): 1 for child in range(3, 6)},
        edge_count=3,
    )
    cycles = decompose_alternating_cycles(space, source, target)
    rows, audit = cycle_rows_and_audit(
        v16i.RunDAG("test", 6, 1, 2, "test", 3, tuple(() for _ in range(6)),
                    tuple(range(6)), tuple(0 for _ in range(6))),
        space, source, target, cycles,
    )
    if len(cycles) != 1 or len(rows) != 1 or not audit["whole_cycle_reversibility_pass"]:
        raise AssertionError("v16z alternating-cycle decomposition failed")
    bridge = bounded_bridge_search(v16y.build_kernel(space), source, target)
    if bridge.status != "exact_bridge_found" or not bridge.reverse_replay_pass:
        raise AssertionError("v16z synthetic 2x2 bridge failed")
    if implementation_call_counts() != {"spectrum_calls": 0, "effect_metric_calls": 0}:
        raise AssertionError("v16z effect exclusion audit failed")
    if spec_payload()["failed_bounded_search_interpretation"] != "unresolved_not_disconnected":
        raise AssertionError("v16z unresolved interpretation changed")
    print("[v16z] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16z alternating-cycle bridge gate")
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
