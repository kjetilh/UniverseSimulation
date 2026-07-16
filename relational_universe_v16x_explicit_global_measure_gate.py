#!/usr/bin/env python3
"""v16x effect-blind qualification of an explicit global matching measure.

The gate first resolves the v16w forced-edge ambiguity exactly on the six
frozen event DAGs. It then samples the surviving coarse v16v state space with
integer min-cost flow under exchangeable pseudo-random edge costs. No source
spectrum or observed-effect statistic is computed.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import random
import statistics
import time
from itertools import combinations
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import networkx as nx

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16n_coarse_event_resource_null_calibration as v16n
import relational_universe_v16s_fresh_event_footprint_holdout as v16s
import relational_universe_v16t_footprint_null_path_stability_gate as v16t
import relational_universe_v16v_global_edge_slot_feasibility_gate as v16v
import relational_universe_v16w_global_null_qualification_gate as v16w


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

COARSE_ARM = "coarse_v16v_slot_space"
CONFLICT_ARM = "actual_concrete_conflict_only"
PRIMARY_SEED_FAMILY = "seed_family_a"
SENSITIVITY_SEED_FAMILY = "seed_family_b"
PRIMARY_REPLICATES = 16
SENSITIVITY_REPLICATES = 16
CHECK_REPLICATES = (0, 5, 10, 15)
RELABEL_SEEDS = (1901, 1902, 1903, 1904)
WITNESSES_PER_SOURCE_ARM = 4
INTEGER_WEIGHT_MAX = (1 << 63) - 1
MIN_UNIQUE_FRACTION = v16w.MIN_UNIQUE_FRACTION
MIN_MEDIAN_PAIRWISE_CHANGE = v16w.MIN_MEDIAN_PAIRWISE_CHANGE
MIN_VARIABLE_UNION_COVERAGE = v16w.MIN_CANDIDATE_UNION_COVERAGE
MIN_EFFECTIVE_VARIABLE_SUPPORT_RATIO = v16w.MIN_EFFECTIVE_EDGE_SUPPORT_RATIO
MAX_VARIABLE_EDGE_INCLUSION_RATE = v16w.MAX_NONFORCED_EDGE_INCLUSION_RATE
MAX_CENTER_RANGE_RATIO = v16w.MAX_BATCH_CENTER_RANGE_RATIO
FROZEN_NONTRIVIAL_CHANGE_FLOOR = v16v.MIN_CHANGED_EDGE_FRACTION

CENTER_FEATURES = (
    "source_edge_fraction",
    "normalized_mean_parent_lag",
    "mean_depth_gap",
    "concrete_conflict_fraction",
    "mean_candidate_rank_fraction",
    "mean_pairwise_changed_fraction",
)

SOURCE_CHAIN = DOC / "v16x_source_chain.csv"
PRE_REGISTRATION = DOC / "v16x_pre_registration.csv"
STATE_SPACE_AUDIT = DOC / "v16x_state_space_forced_edge_audit.csv"
ENDPOINT_AUDIT = DOC / "v16x_sampler_endpoint_audit.csv"
PAIRWISE_DISTANCE = DOC / "v16x_pairwise_endpoint_distance.csv"
REPRESENTATION_AUDIT = DOC / "v16x_representation_audit.csv"
BATCH_STABILITY = DOC / "v16x_batch_center_stability.csv"
SEED_STABILITY = DOC / "v16x_seed_family_stability.csv"
SOURCE_SUMMARY = DOC / "v16x_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v16x_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16x_claim_ledger.csv"
REPORT = DOC / "v16x_explicit_global_measure_gate.md"
NEXT_DIRECTION = DOC / "v16x_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_16x_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16x.md"

Edge = Tuple[int, int]
Slot = Tuple[int, v16v.SlotClass]
Node = Tuple[Any, ...]


@dataclass(frozen=True)
class StateSpace:
    arm: str
    candidates: Tuple[Edge, ...]
    source_edges: frozenset[Edge]
    slot_by_edge: Mapping[Edge, Slot]
    parent_demands: Mapping[int, int]
    slot_demands: Mapping[Slot, int]
    edge_count: int


@dataclass(frozen=True)
class FlexibilityAudit:
    flexible_edges: frozenset[Edge]
    forced_source_edges: frozenset[Edge]
    scc_count: int
    witness_count: int
    witness_integrity_pass: bool


@dataclass(frozen=True)
class Endpoint:
    seed_family: str
    replicate: int
    edges: frozenset[Edge]
    row: MutableMapping[str, Any]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v16s", "frozen_event_histories", v16s.EVENT_LOG),
        ("v16s", "frozen_dependency_edges", v16s.EDGE_LOG),
        ("v16v", "global_state_space_definition", v16v.PRE_REGISTRATION),
        ("v16v", "global_state_space_source_chain", v16v.SOURCE_CHAIN),
        ("v16w", "failed_sampler_qualification", v16w.GATE_EVALUATION),
        ("v16w", "sampler_failure_interpretation", DOC / "v16w_interpretation_audit.md"),
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
        "gate": "v16x_explicit_global_measure_gate",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_state_space_decision_and_explicit_measure_qualification",
        "source_history_count": 6,
        "state_space_arms": [COARSE_ARM, CONFLICT_ARM],
        "forced_edge_method": "source_residual_scc_with_alternating_cycle_witnesses",
        "state_space_change_floor_reused_from_v16v": FROZEN_NONTRIVIAL_CHANGE_FLOOR,
        "design_calibration_disclosure": (
            "forced-edge counts on the six frozen sources were inspected before the formal run; "
            "the deterministic state-space audit is not a fresh holdout"
        ),
        "sampler_state_space_rule": (
            "use coarse arm only if every coarse source can exceed the frozen change floor and "
            "every conflict-only source cannot"
        ),
        "stochastic_measure": "exchangeable_uniform_63bit_integer_edge_cost_minimum_b_matching",
        "solver": "networkx_network_simplex_integer_cost_and_capacity",
        "primary_seed_family": PRIMARY_SEED_FAMILY,
        "sensitivity_seed_family": SENSITIVITY_SEED_FAMILY,
        "primary_replicates_per_source": PRIMARY_REPLICATES,
        "sensitivity_replicates_per_source": SENSITIVITY_REPLICATES,
        "check_replicates": list(CHECK_REPLICATES),
        "semantic_relabel_seeds": list(RELABEL_SEEDS),
        "integer_weight_max": INTEGER_WEIGHT_MAX,
        "nominal_isolation_collision_bound_per_endpoint": "candidate_count/integer_weight_max",
        "nominal_bound_assumes_ideal_independent_uniform_weights": True,
        "implementation_uses_seeded_pseudorandom_generator": True,
        "minimum_unique_fraction": MIN_UNIQUE_FRACTION,
        "minimum_median_pairwise_change": MIN_MEDIAN_PAIRWISE_CHANGE,
        "minimum_variable_union_coverage": MIN_VARIABLE_UNION_COVERAGE,
        "minimum_effective_variable_support_ratio": MIN_EFFECTIVE_VARIABLE_SUPPORT_RATIO,
        "maximum_variable_edge_inclusion_rate": MAX_VARIABLE_EDGE_INCLUSION_RATE,
        "maximum_center_range_ratio": MAX_CENTER_RANGE_RATIO,
        "candidate_insertion_covariance_required": True,
        "semantic_relabel_covariance_required": True,
        "all_globally_forced_edges_required_in_every_endpoint": True,
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "local_switch_construction_allowed": False,
        "no_early_stop": True,
        "not_claimed": [
            "uniform_sampling", "maximum_entropy", "canonical_measure", "mixing",
            "stationarity", "physics", "energy", "temperature", "dimension",
            "Lorentz_symmetry", "spacetime", "particles", "entanglement",
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
        "state_space_arms": f"{COARSE_ARM};{CONFLICT_ARM}",
        "forced_edge_method": "residual_scc_alternating_cycle",
        "state_space_change_floor": FROZEN_NONTRIVIAL_CHANGE_FLOOR,
        "state_space_counts_inspected_during_design": 1,
        "stochastic_measure": "uniform_63bit_integer_edge_cost_minimum_b_matching",
        "primary_replicates_per_source": PRIMARY_REPLICATES,
        "sensitivity_replicates_per_source": SENSITIVITY_REPLICATES,
        "check_replicates": ";".join(str(value) for value in CHECK_REPLICATES),
        "semantic_relabel_seeds": ";".join(str(value) for value in RELABEL_SEEDS),
        "integer_weight_max": INTEGER_WEIGHT_MAX,
        "minimum_unique_fraction": MIN_UNIQUE_FRACTION,
        "minimum_median_pairwise_change": MIN_MEDIAN_PAIRWISE_CHANGE,
        "minimum_variable_union_coverage": MIN_VARIABLE_UNION_COVERAGE,
        "minimum_effective_variable_support_ratio": MIN_EFFECTIVE_VARIABLE_SUPPORT_RATIO,
        "maximum_variable_edge_inclusion_rate": MAX_VARIABLE_EDGE_INCLUSION_RATE,
        "maximum_center_range_ratio": MAX_CENTER_RANGE_RATIO,
        "local_switch_construction_allowed": 0,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v16w.verify_outputs()
    overall = next(
        row["status"] for row in v16i.read_csv(v16w.GATE_EVALUATION)
        if row["gate"] == "v16w_overall"
    )
    if overall != "v16w_global_null_qualification_instrumentation_failed":
        raise ValueError("v16x requires the frozen v16w instrumentation failure")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v16x] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    rows = v16i.read_csv(PRE_REGISTRATION)
    expected = {key: str(value) for key, value in preregistration_row().items()}
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v16x preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v16x source chain changed")


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    loaded: List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]] = []
    for source, metadata in v16w.load_runs():
        loaded.append((v16i.RunDAG(
            stage="v16x",
            target_nodes=source.target_nodes,
            growth_seed=source.growth_seed,
            run_offset=source.run_offset,
            arm=source.arm,
            run_seed=source.run_seed,
            predecessors=source.predecessors,
            depths=source.depths,
            indegrees=source.indegrees,
        ), metadata))
    if len(loaded) != 6:
        raise ValueError("v16x requires six frozen v16s histories")
    return loaded


def build_state_space(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    arm: str,
) -> StateSpace:
    model = v16v.build_matching_model(dag, metadata)
    if arm == COARSE_ARM:
        candidates = tuple(sorted(model.candidates))
    elif arm == CONFLICT_ARM:
        candidates = tuple(sorted(
            edge for edge in model.candidates
            if v16n.conflict_channels(metadata[edge[0]], metadata[edge[1]])
        ))
    else:
        raise ValueError(f"unknown state-space arm {arm}")
    source_edges = frozenset(model.source_edges)
    if not source_edges.issubset(candidates):
        raise ValueError(f"{arm} removed a source dependency edge")
    slot_by_edge = {
        edge: (edge[1], v16v.slot_class(edge[0], edge[1], dag.depths, metadata))
        for edge in candidates
    }
    parent_demands = Counter(parent for parent, _ in source_edges)
    slot_demands = Counter(slot_by_edge[edge] for edge in source_edges)
    space = StateSpace(
        arm=arm,
        candidates=candidates,
        source_edges=source_edges,
        slot_by_edge=slot_by_edge,
        parent_demands=dict(parent_demands),
        slot_demands=dict(slot_demands),
        edge_count=len(source_edges),
    )
    if not assignment_integrity(space, source_edges):
        raise ValueError(f"source assignment is invalid in {arm}")
    return space


def parent_node(parent: int) -> Node:
    return ("parent", parent)


def slot_node(slot: Slot) -> Node:
    return ("slot", slot[0], slot[1])


def node_edge(parent: Node, slot: Node) -> Edge:
    if parent[0] != "parent" or slot[0] != "slot":
        raise ValueError("node_edge requires parent and slot nodes")
    return int(parent[1]), int(slot[1])


def assignment_integrity(space: StateSpace, selected: Iterable[Edge]) -> bool:
    edges = frozenset(selected)
    if len(edges) != space.edge_count or not edges.issubset(space.candidates):
        return False
    return (
        Counter(parent for parent, _ in edges) == Counter(space.parent_demands)
        and Counter(space.slot_by_edge[edge] for edge in edges) == Counter(space.slot_demands)
    )


def residual_graph(space: StateSpace, selected: frozenset[Edge]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for parent in sorted(space.parent_demands):
        graph.add_node(parent_node(parent))
    for slot in sorted(space.slot_demands, key=lambda value: (value[0], repr(value[1]))):
        graph.add_node(slot_node(slot))
    for edge in space.candidates:
        left = parent_node(edge[0])
        right = slot_node(space.slot_by_edge[edge])
        if edge in selected:
            graph.add_edge(right, left)
        else:
            graph.add_edge(left, right)
    return graph


def alternating_cycle_witness(
    space: StateSpace,
    residual: nx.DiGraph,
    selected_edge: Edge,
) -> frozenset[Edge]:
    if selected_edge not in space.source_edges:
        raise ValueError("witness target must be selected in the source assignment")
    left = parent_node(selected_edge[0])
    right = slot_node(space.slot_by_edge[selected_edge])
    path = nx.shortest_path(residual, source=left, target=right)
    changed = set(space.source_edges)
    changed.remove(selected_edge)
    for first, second in zip(path, path[1:]):
        if first[0] == "parent" and second[0] == "slot":
            changed.add(node_edge(first, second))
        elif first[0] == "slot" and second[0] == "parent":
            changed.remove(node_edge(second, first))
        else:
            raise ValueError("residual path did not alternate")
    result = frozenset(changed)
    if result == space.source_edges or not assignment_integrity(space, result):
        raise ValueError("alternating-cycle witness failed")
    return result


def audit_flexibility(space: StateSpace) -> FlexibilityAudit:
    residual = residual_graph(space, space.source_edges)
    components = list(nx.strongly_connected_components(residual))
    labels = {node: index for index, component in enumerate(components) for node in component}
    flexible = frozenset(
        edge for edge in space.candidates
        if labels[parent_node(edge[0])] == labels[slot_node(space.slot_by_edge[edge])]
    )
    forced = frozenset(space.source_edges - flexible)
    witness_edges = sorted(space.source_edges & flexible)[:WITNESSES_PER_SOURCE_ARM]
    witness_pass = True
    for edge in witness_edges:
        witness = alternating_cycle_witness(space, residual, edge)
        witness_pass = witness_pass and edge not in witness and assignment_integrity(space, witness)
    return FlexibilityAudit(
        flexible_edges=flexible,
        forced_source_edges=forced,
        scc_count=len(components),
        witness_count=len(witness_edges),
        witness_integrity_pass=witness_pass,
    )


def state_space_row(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    space: StateSpace,
    audit: FlexibilityAudit,
) -> Dict[str, Any]:
    flexible_source = space.source_edges & audit.flexible_edges
    flexible_non_source = audit.flexible_edges - space.source_edges
    maximum_change = len(flexible_source) / space.edge_count
    concrete_candidates = sum(
        bool(v16n.conflict_channels(metadata[parent], metadata[child]))
        for parent, child in space.candidates
    )
    return {
        **dag.prefix,
        "state_space_arm": space.arm,
        "candidate_edge_count": len(space.candidates),
        "source_edge_count": space.edge_count,
        "concrete_conflict_candidate_count": concrete_candidates,
        "concrete_conflict_candidate_fraction": concrete_candidates / len(space.candidates),
        "residual_scc_count": audit.scc_count,
        "globally_flexible_edge_count": len(audit.flexible_edges),
        "globally_forced_source_edge_count": len(audit.forced_source_edges),
        "globally_forced_source_edge_fraction": len(audit.forced_source_edges) / space.edge_count,
        "flexible_source_edge_count": len(flexible_source),
        "flexible_non_source_edge_count": len(flexible_non_source),
        "maximum_possible_changed_edge_fraction": maximum_change,
        "frozen_nontrivial_change_floor": FROZEN_NONTRIVIAL_CHANGE_FLOOR,
        "nontrivial_change_possible_pass": int(maximum_change >= FROZEN_NONTRIVIAL_CHANGE_FLOOR),
        "alternating_cycle_witness_count": audit.witness_count,
        "alternating_cycle_witness_integrity_pass": int(audit.witness_integrity_pass),
    }


def edge_costs(
    dag: v16i.RunDAG,
    space: StateSpace,
    seed_family: str,
    replicate: int,
) -> Tuple[int, Dict[Edge, int]]:
    seed = v16i.stable_seed("v16x", "integer_cost_measure", seed_family, *dag.key, replicate)
    rng = random.Random(seed)
    costs = {
        edge: rng.randrange(1, INTEGER_WEIGHT_MAX + 1)
        for edge in space.candidates
    }
    return seed, costs


def permuted_insertion_order(
    dag: v16i.RunDAG,
    space: StateSpace,
    replicate: int,
) -> Tuple[Edge, ...]:
    edges = list(space.candidates)
    rng = random.Random(v16i.stable_seed("v16x", "insertion_order", *dag.key, replicate))
    rng.shuffle(edges)
    return tuple(edges)


def solve_edges(
    space: StateSpace,
    costs: Mapping[Edge, int],
    insertion_order: Sequence[Edge] | None = None,
) -> Tuple[frozenset[Edge], int, float]:
    order = tuple(space.candidates if insertion_order is None else insertion_order)
    if len(order) != len(space.candidates) or set(order) != set(space.candidates):
        raise ValueError("insertion order must be a full candidate permutation")
    graph = nx.DiGraph()
    for parent, demand in sorted(space.parent_demands.items()):
        graph.add_node(parent_node(parent), demand=-int(demand))
    for slot, demand in sorted(space.slot_demands.items(), key=lambda item: (item[0][0], repr(item[0][1]))):
        graph.add_node(slot_node(slot), demand=int(demand))
    for edge in order:
        graph.add_edge(
            parent_node(edge[0]),
            slot_node(space.slot_by_edge[edge]),
            capacity=1,
            weight=int(costs[edge]),
        )
    started = time.monotonic()
    objective_cost, flow = nx.network_simplex(graph)
    elapsed = time.monotonic() - started
    selected = frozenset(
        node_edge(node, target)
        for node, targets in flow.items()
        if node[0] == "parent"
        for target, amount in targets.items()
        if amount
    )
    if not assignment_integrity(space, selected):
        raise ValueError("integer min-cost flow returned an invalid assignment")
    return selected, int(objective_cost), elapsed


def edge_digest(edges: Iterable[Edge]) -> str:
    payload = json.dumps(sorted(edges), separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def endpoint_features(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    space: StateSpace,
    edges: frozenset[Edge],
) -> Dict[str, float]:
    edge_count = len(edges)
    bucket_candidates: Dict[Slot, List[int]] = defaultdict(list)
    for edge in space.candidates:
        bucket_candidates[space.slot_by_edge[edge]].append(edge[0])
    rank_fraction: Dict[Edge, float] = {}
    for slot, parents in bucket_candidates.items():
        ordered = sorted(parents)
        denominator = max(1, len(ordered) - 1)
        for rank, parent in enumerate(ordered):
            rank_fraction[(parent, slot[0])] = rank / denominator
    return {
        "source_edge_fraction": len(edges & space.source_edges) / edge_count,
        "normalized_mean_parent_lag": sum(child - parent for parent, child in edges) / (
            edge_count * len(dag.predecessors)
        ),
        "mean_depth_gap": sum(
            dag.depths[child] - dag.depths[parent] for parent, child in edges
        ) / edge_count,
        "concrete_conflict_fraction": sum(
            bool(v16n.conflict_channels(metadata[parent], metadata[child]))
            for parent, child in edges
        ) / edge_count,
        "mean_candidate_rank_fraction": sum(rank_fraction[edge] for edge in edges) / edge_count,
    }


def solve_endpoint(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    space: StateSpace,
    flexibility: FlexibilityAudit,
    seed_family: str,
    replicate: int,
    *,
    insertion_order: Sequence[Edge] | None = None,
    check_kind: str = "sample",
) -> Endpoint:
    seed, costs = edge_costs(dag, space, seed_family, replicate)
    selected, objective_cost, elapsed = solve_edges(space, costs, insertion_order)
    predecessors: List[List[int]] = [[] for _ in dag.predecessors]
    for parent, child in selected:
        predecessors[child].append(parent)
    rewired = tuple(tuple(sorted(parents)) for parents in predecessors)
    structure = v16t.final_structure_audit(dag, metadata, rewired)
    slot_pass = v16v.slot_signature(rewired, dag.depths, metadata) == v16v.slot_signature(
        dag.predecessors, dag.depths, metadata
    )
    forced_pass = flexibility.forced_source_edges.issubset(selected)
    integrity = all((
        assignment_integrity(space, selected),
        int(structure["structure_pass"]),
        slot_pass,
        forced_pass,
    ))
    features = endpoint_features(dag, metadata, space, selected)
    row: Dict[str, Any] = {
        **dag.prefix,
        "state_space_arm": space.arm,
        "stochastic_measure": "uniform_63bit_integer_edge_cost_minimum_b_matching",
        "seed_family": seed_family,
        "replicate": replicate,
        "check_kind": check_kind,
        "objective_seed": seed,
        "candidate_edge_count": len(space.candidates),
        "selected_edge_count": len(selected),
        "objective_cost": objective_cost,
        "solver_seconds": elapsed,
        "nominal_isolation_collision_bound": len(space.candidates) / INTEGER_WEIGHT_MAX,
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
        "local_switch_steps": 0,
        **structure,
        **features,
        "mean_pairwise_changed_fraction": math.nan,
        "per_child_slot_signature_pass": int(slot_pass),
        "globally_forced_edges_included_pass": int(forced_pass),
        "endpoint_integrity_pass": int(integrity),
        "endpoint_edge_sha256": edge_digest(selected),
    }
    return Endpoint(seed_family, replicate, selected, row)


def pairwise_rows(
    dag: v16i.RunDAG,
    endpoints: Sequence[Endpoint],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    distances: Dict[int, List[float]] = defaultdict(list)
    edge_count = len(endpoints[0].edges)
    for left, right in combinations(endpoints, 2):
        changed = len(left.edges - right.edges) / edge_count
        distances[left.replicate].append(changed)
        distances[right.replicate].append(changed)
        rows.append({
            **dag.prefix,
            "seed_family": left.seed_family,
            "left_replicate": left.replicate,
            "right_replicate": right.replicate,
            "left_endpoint_sha256": left.row["endpoint_edge_sha256"],
            "right_endpoint_sha256": right.row["endpoint_edge_sha256"],
            "changed_edge_fraction": changed,
        })
    for endpoint in endpoints:
        endpoint.row["mean_pairwise_changed_fraction"] = statistics.mean(distances[endpoint.replicate])
    return rows


def ensemble_summary(
    space: StateSpace,
    flexibility: FlexibilityAudit,
    endpoints: Sequence[Endpoint],
) -> Dict[str, Any]:
    counts = Counter(edge for endpoint in endpoints for edge in endpoint.edges)
    variable = flexibility.flexible_edges
    variable_counts = {edge: counts[edge] for edge in variable if counts[edge]}
    total_variable_occurrences = sum(variable_counts.values())
    probabilities = [count / total_variable_occurrences for count in variable_counts.values()]
    entropy = -sum(value * math.log(value) for value in probabilities) if probabilities else 0.0
    effective_support = math.exp(entropy) / len(variable) if variable else 0.0
    pairwise = [
        len(left.edges - right.edges) / space.edge_count
        for left, right in combinations(endpoints, 2)
    ]
    return {
        "endpoint_count": len(endpoints),
        "successful_endpoint_count": sum(int(endpoint.row["endpoint_integrity_pass"]) for endpoint in endpoints),
        "unique_endpoint_fraction": len({endpoint.row["endpoint_edge_sha256"] for endpoint in endpoints}) / len(endpoints),
        "minimum_source_changed_edge_fraction": min(
            1.0 - len(endpoint.edges & space.source_edges) / space.edge_count for endpoint in endpoints
        ),
        "median_pairwise_changed_edge_fraction": statistics.median(pairwise),
        "minimum_pairwise_changed_edge_fraction": min(pairwise),
        "variable_candidate_union_coverage": len(variable_counts) / len(variable) if variable else 0.0,
        "effective_variable_support_ratio": effective_support,
        "maximum_variable_edge_inclusion_rate": max(
            (count / len(endpoints) for count in variable_counts.values()), default=0.0
        ),
        "all_forced_edges_included_pass": int(all(
            flexibility.forced_source_edges.issubset(endpoint.edges) for endpoint in endpoints
        )),
    }


def range_ratio(left: Sequence[float], right: Sequence[float]) -> Tuple[float, float, float, float]:
    left_median = statistics.median(left)
    right_median = statistics.median(right)
    shift = abs(left_median - right_median)
    combined_range = max((*left, *right)) - min((*left, *right))
    ratio = 0.0 if combined_range == 0.0 else shift / combined_range
    return left_median, right_median, shift, ratio


def stability_rows(
    dag: v16i.RunDAG,
    left: Sequence[Endpoint],
    right: Sequence[Endpoint],
    kind: str,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for feature in CENTER_FEATURES:
        left_values = [float(endpoint.row[feature]) for endpoint in left]
        right_values = [float(endpoint.row[feature]) for endpoint in right]
        left_center, right_center, shift, ratio = range_ratio(left_values, right_values)
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
        "local_switch_calls": names["footprint_rewire"] + names["exact_footprint_path"],
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
    state_rows: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16x explicit global measure gate",
        "",
        f"Status: `{overall}`.",
        "",
        "## Evidential status",
        "",
        "This is an effect-blind deterministic state-space audit followed by a preregistered finite sampler qualification. The forced-edge counts were inspected during design and are not a fresh holdout. Sampler endpoints, representation checks, and seed-family checks were generated only after the specification and script hash were frozen.",
        "",
        "No source spectrum or observed-effect statistic was computed.",
        "",
        "## State-space audit",
        "",
    ]
    lines.extend(markdown_table(state_rows, (
        "growth_seed", "run_offset", "state_space_arm", "candidate_edge_count",
        "globally_forced_source_edge_fraction", "flexible_non_source_edge_count",
        "maximum_possible_changed_edge_fraction", "nontrivial_change_possible_pass",
    )))
    lines.extend([
        "",
        "A source edge is globally forced exactly when it is not part of an alternating cycle in the source assignment residual graph. Strongly connected components classify this property; explicit alternating-cycle flips validate sampled flexible-source witnesses. The exact-conflict arm is judged against the already frozen v16v 10% nontrivial-change floor, not a new v16x-tuned threshold.",
        "",
        "## Explicit measure",
        "",
        "The surviving coarse state space receives independent seeded pseudo-random integer costs in `[1, 2^63-1]` on canonically ordered candidate edges. An integer-capacity `network_simplex` solve selects the minimum-cost feasible b-matching. No source-retention term is present. Under ideal independent uniform weights, the isolation-lemma collision bound is at most `candidate_count/(2^63-1)` per endpoint. The implementation is deterministic pseudorandom, so that nominal bound is not promoted to a physical or cryptographic guarantee.",
        "",
        "This defines an explicit edge-exchangeable random-cost measure. It is not uniform over feasible matchings, maximum entropy, canonical, or proven representative.",
        "",
        "## Source qualification",
        "",
    ])
    lines.extend(markdown_table(summaries, (
        "growth_seed", "run_offset", "primary_unique_fraction",
        "primary_median_pairwise_change", "primary_variable_union_coverage",
        "primary_effective_variable_support_ratio", "representation_pass",
        "batch_center_pass", "seed_family_pass", "source_qualification_pass",
    )))
    lines.extend(["", "## Gates", ""])
    lines.extend(markdown_table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "A pass would establish only finite implementation qualification for this declared random-cost measure on six frozen DAGs. It would not validate the old LP procedure, prove uniform sampling, establish a canonical null, or reproduce the v16s effect.",
        "",
        "A failure still narrows the method: it identifies whether representation covariance, finite diversity, seed-family stability, or the state-space choice remains unresolved before effect inspection.",
        "",
        "V16x establishes no energy, temperature, invariant, dimension, manifold, Lorentz symmetry, spacetime, particle, entanglement, continuum, or physical law.",
        "",
        "## Algorithm references",
        "",
        "- Mulmuley, Vazirani, and Vazirani, *Matching is as Easy as Matrix Inversion* (1987), DOI: https://doi.org/10.1145/28395.383347",
        "- NetworkX `network_simplex` documentation: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.flow.network_simplex.html",
        "",
    ])
    return "\n".join(lines)


def build_next_direction(overall: str) -> str:
    if overall == "v16x_explicit_integer_cost_measure_finitely_qualified":
        decision = (
            "Freeze the exact v16x state space and integer-cost measure. The next gate may be a single "
            "fresh-history independent-null effect test with concrete-conflict fraction reported as a "
            "predeclared stratification diagnostic. Do not reuse the six v16s histories as confirmatory data."
        )
    else:
        decision = (
            "Do not compute a source spectrum. Repair only the failed v16x layer: representation covariance, "
            "finite ensemble concentration, or seed-family center stability. Keep the exact-conflict state "
            "space retired if its deterministic maximum possible change remains below the frozen 10% floor."
        )
    return "\n".join([
        "# v16x interpretation and next direction",
        "",
        f"Status: `{overall}`.",
        "",
        "## Decision",
        "",
        decision,
        "",
        "## Separate mechanism track",
        "",
        "Action density and change intensity remain separate downstream hypotheses. V16x does not define energy or temperature.",
        "",
    ])


def run() -> None:
    verify_frozen_sources()
    runs = load_runs()
    calls = implementation_call_counts()
    state_rows: List[Dict[str, Any]] = []
    endpoint_rows: List[MutableMapping[str, Any]] = []
    pairwise: List[Dict[str, Any]] = []
    representation_rows: List[Dict[str, Any]] = []
    batch_rows: List[Dict[str, Any]] = []
    seed_rows: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []

    spaces: Dict[Tuple[int, int, str, int], Dict[str, StateSpace]] = {}
    flexes: Dict[Tuple[int, int, str, int], Dict[str, FlexibilityAudit]] = {}
    for dag, metadata in runs:
        spaces[dag.key] = {}
        flexes[dag.key] = {}
        for arm in (COARSE_ARM, CONFLICT_ARM):
            space = build_state_space(dag, metadata, arm)
            flexibility = audit_flexibility(space)
            spaces[dag.key][arm] = space
            flexes[dag.key][arm] = flexibility
            state_rows.append(state_space_row(dag, metadata, space, flexibility))

    coarse_rows = [row for row in state_rows if row["state_space_arm"] == COARSE_ARM]
    conflict_rows = [row for row in state_rows if row["state_space_arm"] == CONFLICT_ARM]
    state_choice_pass = (
        all(int(row["nontrivial_change_possible_pass"]) for row in coarse_rows)
        and all(not int(row["nontrivial_change_possible_pass"]) for row in conflict_rows)
        and all(int(row["alternating_cycle_witness_integrity_pass"]) for row in state_rows)
    )

    for run_index, (dag, metadata) in enumerate(runs, start=1):
        space = spaces[dag.key][COARSE_ARM]
        flexibility = flexes[dag.key][COARSE_ARM]
        primary = [
            solve_endpoint(dag, metadata, space, flexibility, PRIMARY_SEED_FAMILY, replicate)
            for replicate in range(PRIMARY_REPLICATES)
        ]
        sensitivity = [
            solve_endpoint(dag, metadata, space, flexibility, SENSITIVITY_SEED_FAMILY, replicate)
            for replicate in range(SENSITIVITY_REPLICATES)
        ]
        pairwise.extend(pairwise_rows(dag, primary))
        pairwise.extend(pairwise_rows(dag, sensitivity))
        endpoint_rows.extend(endpoint.row for endpoint in (*primary, *sensitivity))

        primary_by_replicate = {endpoint.replicate: endpoint for endpoint in primary}
        for check_index, replicate in enumerate(CHECK_REPLICATES):
            original = primary_by_replicate[replicate]
            replay = solve_endpoint(
                dag, metadata, space, flexibility, PRIMARY_SEED_FAMILY, replicate,
                check_kind="exact_replay",
            )
            reordered = solve_endpoint(
                dag, metadata, space, flexibility, PRIMARY_SEED_FAMILY, replicate,
                insertion_order=permuted_insertion_order(dag, space, replicate),
                check_kind="candidate_insertion_permutation",
            )
            relabeled_metadata = v16w.relabel_metadata(metadata, RELABEL_SEEDS[check_index])
            relabeled_space = build_state_space(dag, relabeled_metadata, COARSE_ARM)
            relabeled_flexibility = audit_flexibility(relabeled_space)
            relabeled = solve_endpoint(
                dag, relabeled_metadata, relabeled_space, relabeled_flexibility,
                PRIMARY_SEED_FAMILY, replicate, check_kind="semantic_role_relabel",
            )
            candidate_covariance = space.candidates == relabeled_space.candidates
            representation_rows.append({
                **dag.prefix,
                "replicate": replicate,
                "relabel_seed": RELABEL_SEEDS[check_index],
                "source_endpoint_sha256": original.row["endpoint_edge_sha256"],
                "replay_endpoint_sha256": replay.row["endpoint_edge_sha256"],
                "permuted_insertion_endpoint_sha256": reordered.row["endpoint_edge_sha256"],
                "relabeled_endpoint_sha256": relabeled.row["endpoint_edge_sha256"],
                "replay_integrity_pass": replay.row["endpoint_integrity_pass"],
                "insertion_integrity_pass": reordered.row["endpoint_integrity_pass"],
                "relabel_integrity_pass": relabeled.row["endpoint_integrity_pass"],
                "candidate_set_covariance_pass": int(candidate_covariance),
                "exact_replay_pass": int(original.edges == replay.edges),
                "candidate_insertion_covariance_pass": int(original.edges == reordered.edges),
                "semantic_role_relabel_covariance_pass": int(original.edges == relabeled.edges),
                "representation_pass": int(
                    candidate_covariance
                    and original.edges == replay.edges == reordered.edges == relabeled.edges
                    and int(replay.row["endpoint_integrity_pass"])
                    and int(reordered.row["endpoint_integrity_pass"])
                    and int(relabeled.row["endpoint_integrity_pass"])
                ),
            })

        midpoint = len(primary) // 2
        source_batch_rows = stability_rows(
            dag, primary[:midpoint], primary[midpoint:], "primary_half_batch"
        )
        source_seed_rows = stability_rows(
            dag, primary, sensitivity, "independent_seed_family"
        )
        batch_rows.extend(source_batch_rows)
        seed_rows.extend(source_seed_rows)
        primary_summary = ensemble_summary(space, flexibility, primary)
        sensitivity_summary = ensemble_summary(space, flexibility, sensitivity)
        source_representation = [
            row for row in representation_rows
            if int(row["growth_seed"]) == dag.growth_seed and int(row["run_offset"]) == dag.run_offset
        ]
        representation_pass = all(int(row["representation_pass"]) for row in source_representation)
        diversity_pass = all((
            primary_summary["successful_endpoint_count"] == PRIMARY_REPLICATES,
            primary_summary["unique_endpoint_fraction"] >= MIN_UNIQUE_FRACTION,
            primary_summary["median_pairwise_changed_edge_fraction"] >= MIN_MEDIAN_PAIRWISE_CHANGE,
            primary_summary["variable_candidate_union_coverage"] >= MIN_VARIABLE_UNION_COVERAGE,
            primary_summary["effective_variable_support_ratio"] >= MIN_EFFECTIVE_VARIABLE_SUPPORT_RATIO,
            primary_summary["maximum_variable_edge_inclusion_rate"] <= MAX_VARIABLE_EDGE_INCLUSION_RATE,
            int(primary_summary["all_forced_edges_included_pass"]),
        ))
        batch_pass = all(int(row["center_stability_pass"]) for row in source_batch_rows)
        seed_pass = all(int(row["center_stability_pass"]) for row in source_seed_rows)
        source_pass = all((
            state_choice_pass, representation_pass, diversity_pass, batch_pass, seed_pass,
            sensitivity_summary["successful_endpoint_count"] == SENSITIVITY_REPLICATES,
        ))
        summaries.append({
            **dag.prefix,
            "candidate_edge_count": len(space.candidates),
            "globally_forced_source_edge_count": len(flexibility.forced_source_edges),
            "primary_successful_endpoints": primary_summary["successful_endpoint_count"],
            "primary_unique_fraction": primary_summary["unique_endpoint_fraction"],
            "primary_minimum_source_change": primary_summary["minimum_source_changed_edge_fraction"],
            "primary_median_pairwise_change": primary_summary["median_pairwise_changed_edge_fraction"],
            "primary_variable_union_coverage": primary_summary["variable_candidate_union_coverage"],
            "primary_effective_variable_support_ratio": primary_summary["effective_variable_support_ratio"],
            "primary_max_variable_edge_inclusion_rate": primary_summary["maximum_variable_edge_inclusion_rate"],
            "sensitivity_successful_endpoints": sensitivity_summary["successful_endpoint_count"],
            "sensitivity_unique_fraction": sensitivity_summary["unique_endpoint_fraction"],
            "representation_pass": int(representation_pass),
            "endpoint_diversity_pass": int(diversity_pass),
            "batch_center_pass": int(batch_pass),
            "seed_family_pass": int(seed_pass),
            "state_space_choice_pass": int(state_choice_pass),
            "source_qualification_pass": int(source_pass),
        })
        print(
            f"[v16x] sources={run_index}/{len(runs)} "
            f"unique={primary_summary['unique_endpoint_fraction']:.3f} "
            f"pairwise={primary_summary['median_pairwise_changed_edge_fraction']:.3f} "
            f"repr={int(representation_pass)} diversity={int(diversity_pass)} "
            f"batch={int(batch_pass)} seed={int(seed_pass)}"
        )

    expected_endpoints = 6 * (PRIMARY_REPLICATES + SENSITIVITY_REPLICATES)
    integrity_pass = (
        len(endpoint_rows) == expected_endpoints
        and all(int(row["endpoint_integrity_pass"]) for row in endpoint_rows)
        and all(int(row["globally_forced_edges_included_pass"]) for row in endpoint_rows)
    )
    witness_pass = all(int(row["alternating_cycle_witness_integrity_pass"]) for row in state_rows)
    representation_pass = all(int(row["representation_pass"]) for row in representation_rows)
    diversity_pass = all(int(row["endpoint_diversity_pass"]) for row in summaries)
    batch_pass = all(int(row["batch_center_pass"]) for row in summaries)
    seed_pass = all(int(row["seed_family_pass"]) for row in summaries)
    exclusion_pass = calls == {"local_switch_calls": 0, "spectrum_calls": 0, "effect_metric_calls": 0}

    if not integrity_pass or not witness_pass or not exclusion_pass:
        overall = "v16x_explicit_measure_instrumentation_failed"
    elif not state_choice_pass:
        overall = "v16x_state_space_choice_unresolved"
    elif not representation_pass:
        overall = "v16x_integer_measure_representation_not_qualified"
    elif not diversity_pass:
        overall = "v16x_integer_measure_endpoint_diversity_not_qualified"
    elif not batch_pass:
        overall = "v16x_integer_measure_batch_center_unstable"
    elif not seed_pass:
        overall = "v16x_integer_measure_seed_family_unstable"
    else:
        overall = "v16x_explicit_integer_cost_measure_finitely_qualified"

    gates = [
        {
            "gate": "effect_blind_endpoint_integrity",
            "status": "pass" if integrity_pass and exclusion_pass else "fail",
            "observed": f"endpoints={sum(int(row['endpoint_integrity_pass']) for row in endpoint_rows)}/{len(endpoint_rows)};switch={calls['local_switch_calls']};spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}",
            "required": f"{expected_endpoints}/{expected_endpoints};0;0;0",
            "decision": "continue" if integrity_pass and exclusion_pass else "instrumentation_failed",
        },
        {
            "gate": "global_forced_edge_witness_integrity",
            "status": "pass" if witness_pass else "fail",
            "observed": f"arms={sum(int(row['alternating_cycle_witness_integrity_pass']) for row in state_rows)}/{len(state_rows)};witnesses={sum(int(row['alternating_cycle_witness_count']) for row in state_rows)}",
            "required": f"arms={len(state_rows)}/{len(state_rows)}",
            "decision": "continue" if witness_pass else "repair_forced_edge_audit",
        },
        {
            "gate": "effect_blind_state_space_choice",
            "status": "pass" if state_choice_pass else "fail",
            "observed": f"coarse_nontrivial={sum(int(row['nontrivial_change_possible_pass']) for row in coarse_rows)}/6;conflict_nontrivial={sum(int(row['nontrivial_change_possible_pass']) for row in conflict_rows)}/6",
            "required": "coarse_nontrivial=6/6;conflict_nontrivial=0/6",
            "decision": "coarse_measure_with_conflict_stratification" if state_choice_pass else "state_space_unresolved",
        },
        {
            "gate": "representation_covariance",
            "status": "pass" if representation_pass else "fail",
            "observed": f"{sum(int(row['representation_pass']) for row in representation_rows)}/{len(representation_rows)}",
            "required": f"{len(representation_rows)}/{len(representation_rows)}",
            "decision": "continue" if representation_pass else "repair_integer_measure",
        },
        {
            "gate": "finite_endpoint_diversity",
            "status": "pass" if diversity_pass else "fail",
            "observed": f"sources={sum(int(row['endpoint_diversity_pass']) for row in summaries)}/6",
            "required": "sources=6/6",
            "decision": "continue" if diversity_pass else "measure_concentrated",
        },
        {
            "gate": "finite_batch_center_stability",
            "status": "pass" if batch_pass else "fail",
            "observed": f"features={sum(int(row['center_stability_pass']) for row in batch_rows)}/{len(batch_rows)}",
            "required": f"{len(batch_rows)}/{len(batch_rows)}",
            "decision": "continue" if batch_pass else "increase_or_repair_sampling",
        },
        {
            "gate": "independent_seed_family_stability",
            "status": "pass" if seed_pass else "fail",
            "observed": f"features={sum(int(row['center_stability_pass']) for row in seed_rows)}/{len(seed_rows)}",
            "required": f"{len(seed_rows)}/{len(seed_rows)}",
            "decision": "finitely_qualified" if seed_pass else "measure_seed_unstable",
        },
        {
            "gate": "v16x_overall",
            "status": overall,
            "observed": f"integrity={int(integrity_pass)};witness={int(witness_pass)};state={int(state_choice_pass)};representation={int(representation_pass)};diversity={int(diversity_pass)};batch={int(batch_pass)};seed={int(seed_pass)};exclusion={int(exclusion_pass)}",
            "required": "1;1;1;1;1;1;1;1",
            "decision": overall,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "The residual-SCC audit separates globally forced source edges from edges on feasible alternating cycles for the frozen state spaces.",
            "status": "supported" if witness_pass else "not_supported",
            "evidence": "v16x_state_space_forced_edge_audit.csv",
            "scope_limit": "six frozen finite source DAGs; deterministic design audit, not fresh holdout",
        },
        {
            "claim_id": "C2",
            "claim": "Exact concrete-conflict preservation leaves enough global freedom to meet the frozen 10% nontrivial-change floor.",
            "status": "supported" if all(int(row["nontrivial_change_possible_pass"]) for row in conflict_rows) else "not_supported",
            "evidence": "v16x_state_space_forced_edge_audit.csv",
            "scope_limit": "same six source DAGs and v16v slot constraints",
        },
        {
            "claim_id": "C3",
            "claim": "The declared integer-cost measure is replayable and covariant to tested insertion-order and semantic-role representations.",
            "status": "supported" if representation_pass else "not_supported",
            "evidence": "v16x_representation_audit.csv",
            "scope_limit": "four checks per source under seeded pseudorandom costs",
        },
        {
            "claim_id": "C4",
            "claim": "The declared measure has adequate finite diversity and stable centers across half-batches and independent seed families.",
            "status": "supported" if diversity_pass and batch_pass and seed_pass else "not_supported",
            "evidence": "v16x_source_qualification_summary.csv;v16x_batch_center_stability.csv;v16x_seed_family_stability.csv",
            "scope_limit": "16 endpoints per seed family on each of six frozen sources",
        },
        {
            "claim_id": "C5",
            "claim": "V16x establishes uniform sampling, maximum entropy, a canonical null, or physical structure.",
            "status": "not_supported",
            "evidence": "v16x_explicit_global_measure_gate.md",
            "scope_limit": "explicit exclusions",
        },
    ]

    v16i.write_csv(STATE_SPACE_AUDIT, state_rows)
    v16i.write_csv(ENDPOINT_AUDIT, endpoint_rows)
    v16i.write_csv(PAIRWISE_DISTANCE, pairwise)
    v16i.write_csv(REPRESENTATION_AUDIT, representation_rows)
    v16i.write_csv(BATCH_STABILITY, batch_rows)
    v16i.write_csv(SEED_STABILITY, seed_rows)
    v16i.write_csv(SOURCE_SUMMARY, summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    REPORT.write_text(build_report(state_rows, summaries, gates, overall), encoding="utf-8")
    NEXT_DIRECTION.write_text(build_next_direction(overall), encoding="utf-8")
    RECOMMENDATION.write_text(
        "# Operativ anbefaling etter v16x\n\n"
        f"Status: `{overall}`.\n\n"
        + (
            "Frys v16x-målet og bruk nye historier i en enkelt forhåndsregistrert independent-null effektgate. Rapporter konkret konfliktandel som diagnostisk stratum. Ikke kall målet uniformt eller kanonisk.\n"
            if overall == "v16x_explicit_integer_cost_measure_finitely_qualified"
            else "Ikke åpne spektrum eller effekt. Reparer bare det eksplisitt feile samplerlaget.\n"
        ),
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf etter v16x\n\n"
        "Runden undersøker først hvilke årsakskanter som faktisk kan byttes globalt, og bruker deretter en heltallsbasert tilfeldig kostnadsregel for å velge mellom gyldige grafer. Den måler foreløpig bare om kontrollmetoden er stabil; den tester ikke om hovedsignalet finnes.\n\n"
        f"Statusen er `{overall}`. Resultatet er ikke bevis for fysikk, romtid eller naturlover.\n",
        encoding="utf-8",
    )
    print(f"[v16x] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    state_rows = v16i.read_csv(STATE_SPACE_AUDIT)
    endpoints = v16i.read_csv(ENDPOINT_AUDIT)
    pairwise = v16i.read_csv(PAIRWISE_DISTANCE)
    representations = v16i.read_csv(REPRESENTATION_AUDIT)
    batch = v16i.read_csv(BATCH_STABILITY)
    seed = v16i.read_csv(SEED_STABILITY)
    summaries = v16i.read_csv(SOURCE_SUMMARY)
    gates = v16i.read_csv(GATE_EVALUATION)
    expected_endpoints = 6 * (PRIMARY_REPLICATES + SENSITIVITY_REPLICATES)
    expected_pairwise = 6 * 2 * (PRIMARY_REPLICATES * (PRIMARY_REPLICATES - 1) // 2)
    if len(state_rows) != 12 or len(endpoints) != expected_endpoints:
        raise ValueError("v16x state/endpoint row counts failed")
    if len(pairwise) != expected_pairwise or len(representations) != 6 * len(CHECK_REPLICATES):
        raise ValueError("v16x pairwise/representation row counts failed")
    if len(batch) != 6 * len(CENTER_FEATURES) or len(seed) != 6 * len(CENTER_FEATURES):
        raise ValueError("v16x stability row counts failed")
    if len(summaries) != 6 or not all(int(row["endpoint_integrity_pass"]) for row in endpoints):
        raise ValueError("v16x endpoint integrity failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16x_overall")
    allowed = {
        "v16x_explicit_measure_instrumentation_failed",
        "v16x_state_space_choice_unresolved",
        "v16x_integer_measure_representation_not_qualified",
        "v16x_integer_measure_endpoint_diversity_not_qualified",
        "v16x_integer_measure_batch_center_unstable",
        "v16x_integer_measure_seed_family_unstable",
        "v16x_explicit_integer_cost_measure_finitely_qualified",
    }
    if overall not in allowed:
        raise ValueError("v16x unknown overall status")
    exclusion = next(row for row in gates if row["gate"] == "effect_blind_endpoint_integrity")
    if "switch=0;spectrum=0;effect=0" not in exclusion["observed"]:
        raise ValueError("v16x effect exclusion failed")
    for path in (REPORT, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"v16x missing report {path.name}")
    print(f"[v16x] output verification pass overall={overall}")


def self_test() -> None:
    role: v16v.Role = ("test", ("resource",))
    klass: v16v.SlotClass = (role, 0, "witness")
    candidates = ((0, 2), (0, 3), (1, 2), (1, 3))
    slot_by_edge = {edge: (edge[1], klass) for edge in candidates}
    space = StateSpace(
        arm="test",
        candidates=candidates,
        source_edges=frozenset({(0, 2), (1, 3)}),
        slot_by_edge=slot_by_edge,
        parent_demands={0: 1, 1: 1},
        slot_demands={(2, klass): 1, (3, klass): 1},
        edge_count=2,
    )
    audit = audit_flexibility(space)
    if audit.forced_source_edges or audit.flexible_edges != frozenset(candidates):
        raise AssertionError("v16x flexible 2x2 audit failed")
    if not audit.witness_integrity_pass or audit.witness_count != 2:
        raise AssertionError("v16x alternating-cycle witnesses failed")
    costs = {(0, 2): 4, (0, 3): 1, (1, 2): 2, (1, 3): 3}
    selected, _, _ = solve_edges(space, costs)
    reversed_order, _, _ = solve_edges(space, costs, tuple(reversed(candidates)))
    if selected != frozenset({(0, 3), (1, 2)}) or selected != reversed_order:
        raise AssertionError("v16x exact integer flow covariance failed")
    forced_space = StateSpace(
        arm="forced_test",
        candidates=((0, 2), (1, 3)),
        source_edges=frozenset({(0, 2), (1, 3)}),
        slot_by_edge={(0, 2): (2, klass), (1, 3): (3, klass)},
        parent_demands={0: 1, 1: 1},
        slot_demands={(2, klass): 1, (3, klass): 1},
        edge_count=2,
    )
    forced_audit = audit_flexibility(forced_space)
    if forced_audit.forced_source_edges != forced_space.source_edges:
        raise AssertionError("v16x forced-edge audit failed")
    if implementation_call_counts() != {
        "local_switch_calls": 0,
        "spectrum_calls": 0,
        "effect_metric_calls": 0,
    }:
        raise AssertionError("v16x effect exclusion audit failed")
    if spec_payload()["source_spectrum_computation_allowed"]:
        raise AssertionError("v16x source spectrum must be prohibited")
    print("[v16x] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16x effect-blind explicit global measure gate")
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
