#!/usr/bin/env python3
"""v17d effect-blind finite stability gate for the qualified v17c kernel.

The six finite state spaces, two starts, exact bounded-cycle proposal law,
reverse auxiliary and lazy Metropolis correction are inherited from v17c.
This gate uses fresh deterministic seed families and longer chains to compare
starts, seeds and early/late windows without computing a source spectrum or an
observed-effect statistic.
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
import time
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import networkx as nx

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16t_footprint_null_path_stability_gate as v16t
import relational_universe_v16x_explicit_global_measure_gate as v16x
import relational_universe_v16z_alternating_cycle_bridge_gate as v16z
import relational_universe_v17a_state_independent_cycle_proposal_qualification as v17a
import relational_universe_v17b_residual_cycle_constructor_gate as v17b
import relational_universe_v17c_exact_counter_runtime_qualification as v17c


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

START_FAMILIES = v17c.START_FAMILIES
CHAIN_SEED_FAMILIES = ("stability_seed_c", "stability_seed_d")
TOTAL_STEPS = 2048
EARLY_STEPS = tuple(range(768, 1280, 64))
LATE_STEPS = tuple(range(1536, 2048, 64))
WINDOW_STEPS = {"early": EARLY_STEPS, "late": LATE_STEPS}
SAMPLES_PER_WINDOW = 8
MAX_CHAIN_SECONDS = 75.0
MIN_FINAL_START_CHANGE = v17c.MIN_FINAL_START_CHANGE
MIN_ACCEPTED_CYCLES_PER_WINDOW = 20
MIN_WINDOW_UNIQUE_FRACTION = 0.875
MAX_CENTER_RANGE_RATIO = v16x.MAX_CENTER_RANGE_RATIO
MAX_CROSS_TO_WITHIN_DISTANCE_RATIO = 1.25
MIN_PROPOSAL_NODE_JACCARD = 0.10
MIN_PROPOSAL_NODE_COVERAGE = 0.10

ENDPOINT_CENTER_FEATURES = (
    "source_edge_fraction",
    "normalized_mean_parent_lag",
    "mean_depth_gap",
    "concrete_conflict_fraction",
    "mean_candidate_rank_fraction",
    "mean_pairwise_changed_fraction",
)
COMPONENT_CENTER_FEATURES = (
    "residual_scc_count",
    "residual_nontrivial_scc_count",
    "largest_residual_scc_node_fraction",
    "selected_cycle_flexible_fraction",
    "source_flexible_edge_jaccard",
)

SOURCE_CHAIN = DOC / "v17d_source_chain.csv"
PRE_REGISTRATION = DOC / "v17d_pre_registration.csv"
ENDPOINT_AUDIT = DOC / "v17d_endpoint_audit.csv"
PAIRWISE_DISTANCE = DOC / "v17d_pairwise_distance.csv"
CENTER_STABILITY = DOC / "v17d_center_stability.csv"
ENDPOINT_AGREEMENT = DOC / "v17d_endpoint_agreement.csv"
COMPONENT_PROFILE = DOC / "v17d_residual_component_profile.csv"
COMPONENT_STABILITY = DOC / "v17d_residual_component_stability.csv"
PROPOSAL_FOOTPRINT = DOC / "v17d_proposal_footprint.csv"
PROPOSAL_OVERLAP = DOC / "v17d_proposal_footprint_overlap.csv"
TRANSITION_SUMMARY = DOC / "v17d_chain_transition_summary.csv"
REVERSIBILITY_AUDIT = DOC / "v17d_pathwise_reversibility_audit.csv"
REPRESENTATION_AUDIT = DOC / "v17d_representation_audit.csv"
SOURCE_SUMMARY = DOC / "v17d_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v17d_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v17d_claim_ledger.csv"
REPORT = DOC / "v17d_effect_blind_finite_stability.md"
INTERPRETATION = DOC / "v17d_interpretation_audit.md"
NEXT_DIRECTION = DOC / "v17d_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_17d_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_17d.md"

Edge = v16x.Edge
Slot = v16x.Slot
CycleKernel = v17a.CycleKernel


@dataclass
class Endpoint:
    edges: frozenset[Edge]
    row: MutableMapping[str, Any]


@dataclass
class Footprint:
    row: MutableMapping[str, Any]
    edges: frozenset[Edge]
    parents: frozenset[int]
    slots: frozenset[Slot]


@dataclass
class StabilityChainResult:
    final: frozenset[Edge]
    endpoints: List[Endpoint]
    footprints: List[Footprint]
    stats: Dict[str, Any]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v16x", "frozen_state_space", v16x.PRE_REGISTRATION),
        ("v16z", "frozen_start_pair", v16z.REVERSIBILITY_AUDIT),
        ("v17c", "qualified_preregistration", v17c.PRE_REGISTRATION),
        ("v17c", "qualified_gate", v17c.GATE_EVALUATION),
        ("v17c", "qualified_proposal_implementation", v17c.SCRIPT),
        ("v17c", "interpretation_boundary", v17c.INTERPRETATION),
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
        "gate": "v17d_effect_blind_finite_stability",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_start_seed_time_and_proposal_footprint_stability",
        "state_space": v16x.COARSE_ARM,
        "source_history_count": 6,
        "start_families": list(START_FAMILIES),
        "chain_seed_families": list(CHAIN_SEED_FAMILIES),
        "seed_independence": "stable_seed_v17d_labels_not_used_by_v17c",
        "proposal_law": "qualified_v17c_exact_counter_bounded_cycles_2_3_4",
        "stationary_target_scope": "uniform_per_bounded_cycle_proposal_connected_component",
        "total_steps": TOTAL_STEPS,
        "early_steps": list(EARLY_STEPS),
        "late_steps": list(LATE_STEPS),
        "samples_per_window": SAMPLES_PER_WINDOW,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "minimum_accepted_cycles_per_window": MIN_ACCEPTED_CYCLES_PER_WINDOW,
        "minimum_window_unique_fraction": MIN_WINDOW_UNIQUE_FRACTION,
        "maximum_center_range_ratio": MAX_CENTER_RANGE_RATIO,
        "maximum_cross_to_within_distance_ratio": MAX_CROSS_TO_WITHIN_DISTANCE_RATIO,
        "minimum_proposal_parent_and_slot_jaccard": MIN_PROPOSAL_NODE_JACCARD,
        "minimum_proposal_parent_and_slot_coverage": MIN_PROPOSAL_NODE_COVERAGE,
        "design_calibration_disclosure": (
            "before preregistration, one excluded first-source source-assignment pilot "
            "with seed label pilot_seed completed 2048 steps in 56.433774 seconds, "
            "recorded 16 endpoints, accepted 65/72 early/late cycles, displaced "
            "0.169239 from its start and inspected no source spectrum or effect metric; "
            "the 75-second bound and all stability thresholds were selected before it"
        ),
        "endpoint_center_features": list(ENDPOINT_CENTER_FEATURES),
        "residual_component_features": list(COMPONENT_CENTER_FEATURES),
        "residual_component_boundary": (
            "endpoint residual-SCC profiles and empirical accepted-proposal footprints "
            "are diagnostics, not proofs of global Markov-component connectivity"
        ),
        "required_chain_passes": 24,
        "required_endpoint_center_passes": 6 * 3 * len(ENDPOINT_CENTER_FEATURES),
        "required_endpoint_agreement_passes": 6 * 3,
        "required_component_center_passes": 6 * 3 * len(COMPONENT_CENTER_FEATURES),
        "required_proposal_overlap_passes": 6 * 3,
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "no_early_stop": True,
        "not_claimed": [
            "global_irreducibility", "mixing_time", "convergence", "global_uniformity",
            "canonical_measure", "source_effect", "energy", "temperature", "dimension",
            "Lorentz_symmetry", "spacetime", "particles", "Bell_correlation",
            "entanglement", "universe_model",
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
        "start_families": ";".join(START_FAMILIES),
        "chain_seed_families": ";".join(CHAIN_SEED_FAMILIES),
        "proposal_law": "qualified_v17c_exact_counter_bounded_cycles_2_3_4",
        "total_steps": TOTAL_STEPS,
        "early_steps": ";".join(str(value) for value in EARLY_STEPS),
        "late_steps": ";".join(str(value) for value in LATE_STEPS),
        "samples_per_window": SAMPLES_PER_WINDOW,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "minimum_accepted_cycles_per_window": MIN_ACCEPTED_CYCLES_PER_WINDOW,
        "minimum_window_unique_fraction": MIN_WINDOW_UNIQUE_FRACTION,
        "maximum_center_range_ratio": MAX_CENTER_RANGE_RATIO,
        "maximum_cross_to_within_distance_ratio": MAX_CROSS_TO_WITHIN_DISTANCE_RATIO,
        "minimum_proposal_node_jaccard": MIN_PROPOSAL_NODE_JACCARD,
        "minimum_proposal_node_coverage": MIN_PROPOSAL_NODE_COVERAGE,
        "required_chain_passes": 24,
        "required_endpoint_center_passes": 108,
        "required_endpoint_agreement_passes": 18,
        "required_component_center_passes": 90,
        "required_proposal_overlap_passes": 18,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v17c.verify_outputs()
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v17d] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    expected = {key: str(value) for key, value in preregistration_row().items()}
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v17d preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v17d source chain changed")


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    runs = []
    for source, metadata in v16x.load_runs():
        runs.append((v16i.RunDAG(
            stage="v17d",
            target_nodes=source.target_nodes,
            growth_seed=source.growth_seed,
            run_offset=source.run_offset,
            arm=source.arm,
            run_seed=source.run_seed,
            predecessors=source.predecessors,
            depths=source.depths,
            indegrees=source.indegrees,
        ), metadata))
    if len(runs) != 6:
        raise ValueError("v17d requires six frozen source histories")
    return runs


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


def chain_seed(dag: v16i.RunDAG, start_family: str, seed_family: str) -> int:
    return v16i.stable_seed("v17d", "chain", start_family, seed_family, *dag.key)


def window_for_step(step: int) -> str | None:
    for name, steps in WINDOW_STEPS.items():
        if min(steps) <= step <= max(steps):
            return name
    return None


def endpoint_row(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    space: v16x.StateSpace,
    forced_edges: frozenset[Edge],
    start_family: str,
    seed_family: str,
    window: str,
    sample_index: int,
    step: int,
    start: frozenset[Edge],
    edges: frozenset[Edge],
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
        forced_edges.issubset(edges),
    ))
    return {
        **dag.prefix,
        "state_space_arm": space.arm,
        "stochastic_measure": "v17c_exact_counter_lazy_metropolis",
        "stationary_target_scope": "uniform_per_bounded_cycle_proposal_component",
        "start_family": start_family,
        "chain_seed_family": seed_family,
        "window": window,
        "sample_index": sample_index,
        "step": step,
        "selected_edge_count": len(edges),
        "source_changed_edge_fraction": 1.0 - len(edges & space.source_edges) / space.edge_count,
        "start_changed_edge_fraction": 1.0 - len(edges & start) / space.edge_count,
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
        **structure,
        **features,
        "mean_pairwise_changed_fraction": math.nan,
        "globally_forced_edges_included_pass": int(forced_edges.issubset(edges)),
        "endpoint_integrity_pass": int(integrity),
        "endpoint_edge_sha256": v16x.edge_digest(edges),
    }


def _find(parent: Dict[Edge, Edge], edge: Edge) -> Edge:
    root = edge
    while parent[root] != root:
        root = parent[root]
    while parent[edge] != edge:
        previous = parent[edge]
        parent[edge] = root
        edge = previous
    return root


def footprint_from_cycles(
    dag: v16i.RunDAG,
    space: v16x.StateSpace,
    start_family: str,
    seed_family: str,
    window: str,
    accepted_cycles: Sequence[frozenset[Edge]],
) -> Footprint:
    touched = frozenset(edge for cycle in accepted_cycles for edge in cycle)
    parents = frozenset(edge[0] for edge in touched)
    slots = frozenset(space.slot_by_edge[edge] for edge in touched)
    union_parent: Dict[Edge, Edge] = {edge: edge for edge in touched}
    for cycle in accepted_cycles:
        ordered = sorted(cycle)
        if not ordered:
            continue
        anchor = ordered[0]
        for edge in ordered[1:]:
            left = _find(union_parent, anchor)
            right = _find(union_parent, edge)
            if left != right:
                union_parent[right] = left
    component_sizes = Counter(_find(union_parent, edge) for edge in touched)
    row: MutableMapping[str, Any] = {
        **dag.prefix,
        "start_family": start_family,
        "chain_seed_family": seed_family,
        "window": window,
        "accepted_cycle_count": len(accepted_cycles),
        "touched_candidate_edge_count": len(touched),
        "touched_candidate_edge_fraction": len(touched) / len(space.candidates),
        "touched_parent_count": len(parents),
        "touched_parent_fraction": len(parents) / len(space.parent_demands),
        "touched_slot_count": len(slots),
        "touched_slot_fraction": len(slots) / len(space.slot_demands),
        "empirical_proposal_incidence_component_count": len(component_sizes),
        "largest_empirical_component_edge_fraction": (
            max(component_sizes.values()) / len(touched) if touched else 0.0
        ),
        "minimum_accepted_cycles_per_window": MIN_ACCEPTED_CYCLES_PER_WINDOW,
        "window_proposal_coverage_pass": int(
            len(accepted_cycles) >= MIN_ACCEPTED_CYCLES_PER_WINDOW
        ),
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }
    return Footprint(row, touched, parents, slots)


def run_chain(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    kernel: CycleKernel,
    forced_edges: frozenset[Edge],
    start: frozenset[Edge],
    start_family: str,
    seed_family: str,
) -> StabilityChainResult:
    seed = chain_seed(dag, start_family, seed_family)
    rng = random.Random(seed)
    selected = start
    record_to_window = {
        step: window for window, steps in WINDOW_STEPS.items() for step in steps
    }
    endpoints: List[Endpoint] = []
    cycles_by_window: Dict[str, List[frozenset[Edge]]] = defaultdict(list)
    counts = Counter()
    accepted_lengths = Counter()
    visited = {v16x.edge_digest(selected)}
    started = time.monotonic()

    for step in range(1, TOTAL_STEPS + 1):
        if rng.getrandbits(1):
            counts["nonlazy_steps"] += 1
            auxiliary = v17c.propose_cycle(kernel, selected, rng)
            if auxiliary is None:
                counts["proposal_dead_end"] += 1
            else:
                counts["valid_proposals"] += 1
                proposed = v17a.apply_proposal(kernel.space, selected, auxiliary.proposal)
                reverse = v17c.path_probability(
                    kernel, proposed, v17a.reverse_remove_sequence(auxiliary.proposal)
                )
                if reverse is None:
                    counts["reverse_unsupported"] += 1
                else:
                    counts["reverse_supported"] += 1
                    acceptance = min(Fraction(1), reverse.probability / auxiliary.probability)
                    if v17a.exact_accept(rng, acceptance):
                        selected = proposed
                        counts["accepted_cycles"] += 1
                        cycle_length = len(auxiliary.proposal.remove)
                        accepted_lengths[cycle_length] += 1
                        if cycle_length >= 3:
                            counts["accepted_long_cycles"] += 1
                        visited.add(v16x.edge_digest(selected))
                        window = window_for_step(step)
                        if window is not None:
                            cycles_by_window[window].append(frozenset(
                                (*auxiliary.proposal.remove, *auxiliary.proposal.add)
                            ))
                    else:
                        counts["metropolis_rejects"] += 1
        else:
            counts["lazy_stays"] += 1

        if step in record_to_window:
            window = record_to_window[step]
            sample_index = WINDOW_STEPS[window].index(step)
            row = endpoint_row(
                dag, metadata, kernel.space, forced_edges, start_family,
                seed_family, window, sample_index, step, start, selected,
            )
            endpoints.append(Endpoint(selected, row))

    elapsed = time.monotonic() - started
    footprints = [
        footprint_from_cycles(
            dag, kernel.space, start_family, seed_family, window,
            cycles_by_window[window],
        )
        for window in WINDOW_STEPS
    ]
    window_unique = {}
    for window in WINDOW_STEPS:
        rows = [endpoint for endpoint in endpoints if endpoint.row["window"] == window]
        window_unique[window] = len({endpoint.row["endpoint_edge_sha256"] for endpoint in rows}) / len(rows)
    final_change = 1.0 - len(selected & start) / kernel.space.edge_count
    traversal_pass = all((
        final_change >= MIN_FINAL_START_CHANGE,
        counts["reverse_unsupported"] == 0,
        all(len(cycles_by_window[window]) >= MIN_ACCEPTED_CYCLES_PER_WINDOW for window in WINDOW_STEPS),
        all(window_unique[window] >= MIN_WINDOW_UNIQUE_FRACTION for window in WINDOW_STEPS),
        all(int(endpoint.row["endpoint_integrity_pass"]) for endpoint in endpoints),
        v16x.assignment_integrity(kernel.space, selected),
    ))
    stats = {
        **dag.prefix,
        "start_family": start_family,
        "chain_seed_family": seed_family,
        "chain_seed": seed,
        "start_endpoint_sha256": v16x.edge_digest(start),
        "final_endpoint_sha256": v16x.edge_digest(selected),
        "total_steps": TOTAL_STEPS,
        "lazy_stays": counts["lazy_stays"],
        "nonlazy_steps": counts["nonlazy_steps"],
        "proposal_dead_end": counts["proposal_dead_end"],
        "valid_proposals": counts["valid_proposals"],
        "reverse_supported": counts["reverse_supported"],
        "reverse_unsupported": counts["reverse_unsupported"],
        "accepted_cycles": counts["accepted_cycles"],
        "metropolis_rejects": counts["metropolis_rejects"],
        "accepted_long_cycles": counts["accepted_long_cycles"],
        "accepted_length_counts_json": json.dumps(dict(sorted(accepted_lengths.items())), separators=(",", ":")),
        "unique_state_count": len(visited),
        "early_accepted_cycles": len(cycles_by_window["early"]),
        "late_accepted_cycles": len(cycles_by_window["late"]),
        "early_unique_fraction": window_unique["early"],
        "late_unique_fraction": window_unique["late"],
        "final_start_changed_edge_fraction": final_change,
        "elapsed_seconds": elapsed,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "resource_pass": int(elapsed <= MAX_CHAIN_SECONDS),
        "traversal_pass": int(traversal_pass),
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }
    return StabilityChainResult(selected, endpoints, footprints, stats)


def residual_component_row(
    dag: v16i.RunDAG,
    space: v16x.StateSpace,
    source_flexible: frozenset[Edge],
    endpoint: Endpoint,
) -> Dict[str, Any]:
    residual = v16x.residual_graph(space, endpoint.edges)
    components = list(nx.strongly_connected_components(residual))
    labels = {node: index for index, component in enumerate(components) for node in component}
    flexible = frozenset(
        edge for edge in space.candidates
        if labels[v16x.parent_node(edge[0])] == labels[v16x.slot_node(space.slot_by_edge[edge])]
    )
    selected_flexible = endpoint.edges & flexible
    overlap = len(flexible & source_flexible)
    union = len(flexible | source_flexible)
    component_digest = hashlib.sha256(json.dumps(
        sorted((len(component), sorted(repr(node) for node in component)) for component in components),
        separators=(",", ":"),
    ).encode("utf-8")).hexdigest()
    return {
        **dag.prefix,
        "start_family": endpoint.row["start_family"],
        "chain_seed_family": endpoint.row["chain_seed_family"],
        "window": endpoint.row["window"],
        "sample_index": endpoint.row["sample_index"],
        "step": endpoint.row["step"],
        "endpoint_edge_sha256": endpoint.row["endpoint_edge_sha256"],
        "residual_scc_count": len(components),
        "residual_nontrivial_scc_count": sum(len(component) > 1 for component in components),
        "largest_residual_scc_node_fraction": max(map(len, components)) / residual.number_of_nodes(),
        "candidate_cycle_flexible_fraction": len(flexible) / len(space.candidates),
        "selected_cycle_flexible_fraction": len(selected_flexible) / space.edge_count,
        "source_flexible_edge_jaccard": overlap / union if union else 1.0,
        "residual_component_profile_sha256": component_digest,
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }


def pairwise_rows(dag: v16i.RunDAG, endpoints: Sequence[Endpoint]) -> List[Dict[str, Any]]:
    rows = []
    distances: Dict[int, List[float]] = defaultdict(list)
    for left_index, right_index in combinations(range(len(endpoints)), 2):
        left = endpoints[left_index]
        right = endpoints[right_index]
        changed = len(left.edges - right.edges) / len(left.edges)
        distances[left_index].append(changed)
        distances[right_index].append(changed)
        rows.append({
            **dag.prefix,
            "left_start_family": left.row["start_family"],
            "left_chain_seed_family": left.row["chain_seed_family"],
            "left_window": left.row["window"],
            "left_sample_index": left.row["sample_index"],
            "right_start_family": right.row["start_family"],
            "right_chain_seed_family": right.row["chain_seed_family"],
            "right_window": right.row["window"],
            "right_sample_index": right.row["sample_index"],
            "left_endpoint_sha256": left.row["endpoint_edge_sha256"],
            "right_endpoint_sha256": right.row["endpoint_edge_sha256"],
            "changed_edge_fraction": changed,
        })
    for index, endpoint in enumerate(endpoints):
        endpoint.row["mean_pairwise_changed_fraction"] = statistics.mean(distances[index])
    return rows


def contrast_groups(items: Sequence[Any], row_getter) -> Tuple[Tuple[str, List[Any], List[Any]], ...]:
    return (
        (
            "start_family",
            [item for item in items if row_getter(item)["start_family"] == START_FAMILIES[0]],
            [item for item in items if row_getter(item)["start_family"] == START_FAMILIES[1]],
        ),
        (
            "independent_chain_seed_family",
            [item for item in items if row_getter(item)["chain_seed_family"] == CHAIN_SEED_FAMILIES[0]],
            [item for item in items if row_getter(item)["chain_seed_family"] == CHAIN_SEED_FAMILIES[1]],
        ),
        (
            "early_vs_late_sample_window",
            [item for item in items if row_getter(item)["window"] == "early"],
            [item for item in items if row_getter(item)["window"] == "late"],
        ),
    )


def range_ratio(left: Sequence[float], right: Sequence[float]) -> Tuple[float, float, float, float]:
    left_center = statistics.median(left)
    right_center = statistics.median(right)
    shift = abs(left_center - right_center)
    combined_range = max((*left, *right)) - min((*left, *right))
    ratio = 0.0 if combined_range == 0.0 else shift / combined_range
    return left_center, right_center, shift, ratio


def center_rows(
    dag: v16i.RunDAG,
    items: Sequence[Any],
    row_getter,
    features: Sequence[str],
    profile_kind: str,
) -> List[Dict[str, Any]]:
    rows = []
    for kind, left, right in contrast_groups(items, row_getter):
        for feature in features:
            left_values = [float(row_getter(item)[feature]) for item in left]
            right_values = [float(row_getter(item)[feature]) for item in right]
            left_center, right_center, shift, ratio = range_ratio(left_values, right_values)
            rows.append({
                **dag.prefix,
                "profile_kind": profile_kind,
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


def endpoint_agreement_rows(dag: v16i.RunDAG, endpoints: Sequence[Endpoint]) -> List[Dict[str, Any]]:
    rows = []
    for kind, left, right in contrast_groups(endpoints, lambda item: item.row):
        left_ids = {id(item) for item in left}
        right_ids = {id(item) for item in right}
        within = []
        cross = []
        for first, second in combinations(endpoints, 2):
            distance = len(first.edges - second.edges) / len(first.edges)
            if (id(first) in left_ids and id(second) in left_ids) or (
                id(first) in right_ids and id(second) in right_ids
            ):
                within.append(distance)
            else:
                cross.append(distance)
        within_median = statistics.median(within)
        cross_median = statistics.median(cross)
        ratio = cross_median / within_median if within_median else (0.0 if cross_median == 0 else math.inf)
        cross_jaccard = (1.0 - cross_median) / (1.0 + cross_median)
        rows.append({
            **dag.prefix,
            "agreement_kind": kind,
            "left_endpoint_count": len(left),
            "right_endpoint_count": len(right),
            "within_pair_count": len(within),
            "cross_pair_count": len(cross),
            "median_within_changed_edge_fraction": within_median,
            "median_cross_changed_edge_fraction": cross_median,
            "median_cross_selected_edge_jaccard": cross_jaccard,
            "cross_to_within_distance_ratio": ratio,
            "maximum_allowed_ratio": MAX_CROSS_TO_WITHIN_DISTANCE_RATIO,
            "endpoint_agreement_pass": int(ratio <= MAX_CROSS_TO_WITHIN_DISTANCE_RATIO),
        })
    return rows


def set_jaccard(left: frozenset[Any], right: frozenset[Any]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 1.0


def proposal_overlap_rows(
    dag: v16i.RunDAG,
    space: v16x.StateSpace,
    footprints: Sequence[Footprint],
) -> List[Dict[str, Any]]:
    rows = []
    for kind, left, right in contrast_groups(footprints, lambda item: item.row):
        left_edges = frozenset(edge for item in left for edge in item.edges)
        right_edges = frozenset(edge for item in right for edge in item.edges)
        left_parents = frozenset(parent for item in left for parent in item.parents)
        right_parents = frozenset(parent for item in right for parent in item.parents)
        left_slots = frozenset(slot for item in left for slot in item.slots)
        right_slots = frozenset(slot for item in right for slot in item.slots)
        parent_jaccard = set_jaccard(left_parents, right_parents)
        slot_jaccard = set_jaccard(left_slots, right_slots)
        min_parent_coverage = min(len(left_parents), len(right_parents)) / len(space.parent_demands)
        min_slot_coverage = min(len(left_slots), len(right_slots)) / len(space.slot_demands)
        passed = all((
            parent_jaccard >= MIN_PROPOSAL_NODE_JACCARD,
            slot_jaccard >= MIN_PROPOSAL_NODE_JACCARD,
            min_parent_coverage >= MIN_PROPOSAL_NODE_COVERAGE,
            min_slot_coverage >= MIN_PROPOSAL_NODE_COVERAGE,
        ))
        rows.append({
            **dag.prefix,
            "overlap_kind": kind,
            "left_footprint_count": len(left),
            "right_footprint_count": len(right),
            "accepted_candidate_edge_jaccard": set_jaccard(left_edges, right_edges),
            "accepted_parent_jaccard": parent_jaccard,
            "accepted_slot_jaccard": slot_jaccard,
            "minimum_parent_coverage": min_parent_coverage,
            "minimum_slot_coverage": min_slot_coverage,
            "minimum_required_node_jaccard": MIN_PROPOSAL_NODE_JACCARD,
            "minimum_required_node_coverage": MIN_PROPOSAL_NODE_COVERAGE,
            "proposal_footprint_overlap_pass": int(passed),
            "global_component_connectivity_claimed": 0,
        })
    return rows


def markdown_table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    return v17b.markdown_table(rows, fields)


def write_documents(
    overall: str,
    gates: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    agreement: Sequence[Mapping[str, Any]],
    transitions: Sequence[Mapping[str, Any]],
) -> None:
    report = [
        "# v17d effect-blind finite stability",
        "",
        f"Status: `{overall}`.",
        "",
        "## Purpose and frozen design",
        "",
        "V17d asks whether the qualified v17c bounded-cycle chain gives compatible finite endpoint distributions across the two frozen starts, two fresh deterministic seed families, and separated early/late windows. It uses 2048 steps per chain and computes no source spectrum or observed-effect statistic.",
        "",
        "## Source qualification",
        "",
        *markdown_table(summaries, (
            "growth_seed", "run_offset", "chain_passes", "endpoint_center_passes",
            "endpoint_agreement_passes", "component_center_passes",
            "proposal_overlap_passes", "source_qualification_pass",
        )),
        "",
        "## Endpoint agreement",
        "",
        *markdown_table(agreement, (
            "growth_seed", "run_offset", "agreement_kind",
            "median_within_changed_edge_fraction", "median_cross_changed_edge_fraction",
            "cross_to_within_distance_ratio", "endpoint_agreement_pass",
        )),
        "",
        "## Gates",
        "",
        *markdown_table(gates, ("gate", "status", "observed", "required", "decision")),
        "",
        "## Runtime and traversal",
        "",
        f"Across 24 chains, maximum runtime was `{max(float(row['elapsed_seconds']) for row in transitions):.6f}` seconds, minimum final displacement was `{min(float(row['final_start_changed_edge_fraction']) for row in transitions):.6f}`, and minimum accepted-cycle counts in the early/late windows were `{min(min(int(row['early_accepted_cycles']), int(row['late_accepted_cycles'])) for row in transitions)}`.",
        "",
        "## Interpretation boundary",
        "",
        "Endpoint center and distance agreement are finite diagnostics, not convergence or mixing proofs. Residual SCCs describe alternating-cycle flexibility at sampled assignments. Empirical proposal-incidence footprints describe only accepted moves observed in these runs. Neither establishes global connectivity of the Markov state graph.",
        "",
        "No source effect, Bell correlation, entanglement, Lorentz symmetry, spacetime geometry, particle or universe model was tested.",
        "",
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    INTERPRETATION.write_text(
        "# v17d interpretation audit\n\n"
        f"Frozen status is `{overall}`. This gate can support only finite effect-blind stability on six reused state spaces. "
        "A pass is not a proof of irreducibility, convergence, mixing time, global uniformity or a canonical measure. "
        "Residual-SCC and accepted-footprint overlap are diagnostics and must not be renamed global Markov components. "
        "Source spectrum and observed-effect computations remained prohibited.\n",
        encoding="utf-8",
    )
    if overall == "v17d_effect_blind_finite_stability_qualified":
        next_text = (
            "Proceed to one preregistered independent source-spectrum effect holdout using only the frozen late-window sampler output. Keep Bell, entanglement, Lorentz and spacetime claims closed."
        )
        recommendation = "Open one independent source-spectrum holdout; do not broaden the physical claim set."
    elif overall in {
        "v17d_endpoint_centers_not_stable",
        "v17d_endpoint_agreement_not_qualified",
        "v17d_residual_component_profiles_not_stable",
    }:
        next_text = (
            "Do not inspect the source spectrum. Use the failure decomposition to preregister one scale-or-kernel decision: extend the chain only if seed and time comparisons pass while start separation remains; otherwise revise the move class."
        )
        recommendation = "Keep effects closed and make a failure-targeted scale-or-kernel decision."
    elif overall == "v17d_proposal_footprint_overlap_not_qualified":
        next_text = (
            "Do not inspect the source spectrum. Diagnose whether bounded cycle lengths 2-4 omit proposal regions shared by the two starts before spending a larger chain budget."
        )
        recommendation = "Diagnose bounded-cycle proposal coverage before any scale increase."
    else:
        next_text = (
            "Stop at the first failed integrity, reversibility, representation, traversal or resource layer and repair instrumentation without effect inspection."
        )
        recommendation = "Repair the first failed qualification layer; effects remain closed."
    NEXT_DIRECTION.write_text(
        f"# v17d next direction\n\nFormal status: `{overall}`.\n\n{next_text}\n",
        encoding="utf-8",
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.17d\n\n"
        f"- status: `{overall}`\n"
        f"- next: {recommendation}\n"
        "- claim ceiling: finite effect-blind stability on six state spaces, not convergence or physics\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf v0.17d for ikke-spesialister\n\n"
        "V17d lar den samme graf-maskinen gaa fire ganger lenger enn i v17c, fra to ulike startgrafer og med to nye tilfeldige tallrekker. Vi sammenligner tidlige og sene utsnitt, avstanden mellom grupper og hvilke deler av forslagene som faktisk blir brukt.\n\n"
        f"Statusen er `{overall}`. Selv en bestaa-status betyr bare at disse seks endelige forsokene ser innbyrdes stabile ut. Den beviser ikke at kjeden har funnet hele rommet eller at modellen beskriver fysikk.\n",
        encoding="utf-8",
    )


def run() -> None:
    verify_frozen_sources()
    v17c.install_optimized_constructor()
    frozen_starts = v16z.frozen_start_digests()
    endpoint_rows: List[MutableMapping[str, Any]] = []
    pairwise: List[Dict[str, Any]] = []
    center: List[Dict[str, Any]] = []
    agreement: List[Dict[str, Any]] = []
    component_profiles: List[Dict[str, Any]] = []
    component_stability: List[Dict[str, Any]] = []
    footprint_rows: List[MutableMapping[str, Any]] = []
    overlap: List[Dict[str, Any]] = []
    transitions: List[Dict[str, Any]] = []
    reversibility: List[Dict[str, Any]] = []
    representations: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []

    for run_index, (dag, metadata) in enumerate(load_runs(), start=1):
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        flexibility = v16x.audit_flexibility(space)
        kernel = v17a.build_kernel(space)
        starts = {
            "source_assignment": space.source_edges,
            "v16x_random_cost_a0": v16z.random_cost_start(dag, space),
        }
        source_endpoints: List[Endpoint] = []
        source_footprints: List[Footprint] = []
        source_transitions: List[Dict[str, Any]] = []
        source_reversibility: List[Dict[str, Any]] = []
        source_representations: List[Dict[str, Any]] = []
        frozen_start_passes = 0

        for start_family, start in starts.items():
            frozen_start_passes += int(
                v16x.edge_digest(start) == frozen_starts[(dag.growth_seed, dag.run_offset, start_family)]
            )
            source_reversibility.extend(v17b.reversibility_rows(dag, kernel, start, start_family))
            source_representations.append(v17b.representation_row(
                dag, metadata, space, start, start_family
            ))
            for seed_family in CHAIN_SEED_FAMILIES:
                result = run_chain(
                    dag, metadata, kernel, flexibility.forced_source_edges,
                    start, start_family, seed_family,
                )
                source_endpoints.extend(result.endpoints)
                source_footprints.extend(result.footprints)
                source_transitions.append(result.stats)

        pairwise.extend(pairwise_rows(dag, source_endpoints))
        source_center = center_rows(
            dag, source_endpoints, lambda item: item.row,
            ENDPOINT_CENTER_FEATURES, "endpoint",
        )
        source_agreement = endpoint_agreement_rows(dag, source_endpoints)
        representative_endpoints = [
            endpoint for endpoint in source_endpoints
            if int(endpoint.row["sample_index"]) == SAMPLES_PER_WINDOW - 1
        ]
        source_component_profiles = [
            residual_component_row(dag, space, flexibility.flexible_edges, endpoint)
            for endpoint in representative_endpoints
        ]
        source_component_stability = center_rows(
            dag, source_component_profiles, lambda item: item,
            COMPONENT_CENTER_FEATURES, "residual_component",
        )
        source_overlap = proposal_overlap_rows(dag, space, source_footprints)

        endpoint_rows.extend(endpoint.row for endpoint in source_endpoints)
        footprint_rows.extend(footprint.row for footprint in source_footprints)
        center.extend(source_center)
        agreement.extend(source_agreement)
        component_profiles.extend(source_component_profiles)
        component_stability.extend(source_component_stability)
        overlap.extend(source_overlap)
        transitions.extend(source_transitions)
        reversibility.extend(source_reversibility)
        representations.extend(source_representations)

        chain_passes = sum(
            int(row["traversal_pass"]) and int(row["resource_pass"])
            for row in source_transitions
        )
        endpoint_center_passes = sum(int(row["center_stability_pass"]) for row in source_center)
        endpoint_agreement_passes = sum(int(row["endpoint_agreement_pass"]) for row in source_agreement)
        component_center_passes = sum(int(row["center_stability_pass"]) for row in source_component_stability)
        proposal_overlap_passes = sum(int(row["proposal_footprint_overlap_pass"]) for row in source_overlap)
        reversibility_passes = sum(int(row["pathwise_detailed_balance_pass"]) for row in source_reversibility)
        representation_passes = sum(int(row["representation_pass"]) for row in source_representations)
        endpoint_integrity_passes = sum(int(row["endpoint_integrity_pass"]) for row in endpoint_rows if (
            int(row["growth_seed"]), int(row["run_offset"])
        ) == (dag.growth_seed, dag.run_offset))
        source_pass = all((
            frozen_start_passes == 2,
            chain_passes == 4,
            reversibility_passes == 6,
            representation_passes == 2,
            endpoint_integrity_passes == 64,
            endpoint_center_passes == 18,
            endpoint_agreement_passes == 3,
            component_center_passes == 15,
            proposal_overlap_passes == 3,
        ))
        summaries.append({
            **dag.prefix,
            "frozen_start_passes": frozen_start_passes,
            "chain_passes": chain_passes,
            "reversibility_passes": reversibility_passes,
            "representation_passes": representation_passes,
            "endpoint_integrity_passes": endpoint_integrity_passes,
            "endpoint_center_passes": endpoint_center_passes,
            "endpoint_agreement_passes": endpoint_agreement_passes,
            "component_center_passes": component_center_passes,
            "proposal_overlap_passes": proposal_overlap_passes,
            "maximum_chain_seconds": max(float(row["elapsed_seconds"]) for row in source_transitions),
            "source_qualification_pass": int(source_pass),
        })
        print(
            f"[v17d] sources={run_index}/6 chains={chain_passes}/4 "
            f"centers={endpoint_center_passes}/18 agreement={endpoint_agreement_passes}/3 "
            f"components={component_center_passes}/15 overlap={proposal_overlap_passes}/3"
        )

    calls = implementation_call_counts()
    exclusion_pass = (
        calls == {"spectrum_calls": 0, "effect_metric_calls": 0}
        and all(int(row["source_spectrum_computed"]) == 0 for row in endpoint_rows)
        and all(int(row["observed_effect_computed"]) == 0 for row in endpoint_rows)
        and all(int(row["source_spectrum_computed"]) == 0 for row in transitions)
        and all(int(row["observed_effect_computed"]) == 0 for row in transitions)
    )
    start_count = sum(int(row["frozen_start_passes"]) for row in summaries)
    integrity_count = sum(int(row["endpoint_integrity_pass"]) for row in endpoint_rows)
    reverse_count = sum(int(row["pathwise_detailed_balance_pass"]) for row in reversibility)
    representation_count = sum(int(row["representation_pass"]) for row in representations)
    traversal_count = sum(int(row["traversal_pass"]) for row in transitions)
    resource_count = sum(int(row["resource_pass"]) for row in transitions)
    endpoint_center_count = sum(int(row["center_stability_pass"]) for row in center)
    endpoint_agreement_count = sum(int(row["endpoint_agreement_pass"]) for row in agreement)
    component_center_count = sum(int(row["center_stability_pass"]) for row in component_stability)
    proposal_overlap_count = sum(int(row["proposal_footprint_overlap_pass"]) for row in overlap)

    if not exclusion_pass or start_count != 12 or integrity_count != 384:
        overall = "v17d_instrumentation_failed"
    elif reverse_count != 36:
        overall = "v17d_reversibility_not_qualified"
    elif representation_count != 12:
        overall = "v17d_representation_not_qualified"
    elif traversal_count != 24:
        overall = "v17d_finite_traversal_not_qualified"
    elif resource_count != 24:
        overall = "v17d_resource_not_qualified"
    elif endpoint_center_count != 108:
        overall = "v17d_endpoint_centers_not_stable"
    elif endpoint_agreement_count != 18:
        overall = "v17d_endpoint_agreement_not_qualified"
    elif component_center_count != 90:
        overall = "v17d_residual_component_profiles_not_stable"
    elif proposal_overlap_count != 18:
        overall = "v17d_proposal_footprint_overlap_not_qualified"
    else:
        overall = "v17d_effect_blind_finite_stability_qualified"

    gates = [
        {"gate": "effect_blind_integrity", "status": "pass" if exclusion_pass else "fail", "observed": f"spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}", "required": "0;0", "decision": "continue" if exclusion_pass else "invalidate"},
        {"gate": "frozen_start_replay", "status": "pass" if start_count == 12 else "fail", "observed": f"{start_count}/12", "required": "12/12", "decision": "continue" if start_count == 12 else "invalidate"},
        {"gate": "endpoint_integrity", "status": "pass" if integrity_count == 384 else "fail", "observed": f"{integrity_count}/384", "required": "384/384", "decision": "continue" if integrity_count == 384 else "invalidate"},
        {"gate": "pathwise_detailed_balance", "status": "pass" if reverse_count == 36 else "fail", "observed": f"{reverse_count}/36", "required": "36/36", "decision": "continue" if reverse_count == 36 else "repair_probability"},
        {"gate": "representation_covariance", "status": "pass" if representation_count == 12 else "fail", "observed": f"{representation_count}/12", "required": "12/12", "decision": "continue" if representation_count == 12 else "repair_representation"},
        {"gate": "finite_traversal", "status": "pass" if traversal_count == 24 else "fail", "observed": f"{traversal_count}/24", "required": "24/24", "decision": "continue" if traversal_count == 24 else "insufficient_traversal"},
        {"gate": "resource_bound", "status": "pass" if resource_count == 24 else "fail", "observed": f"{resource_count}/24;max={max(float(row['elapsed_seconds']) for row in transitions):.6f}s", "required": "24/24;each<=75s", "decision": "continue" if resource_count == 24 else "resource_not_qualified"},
        {"gate": "endpoint_center_stability", "status": "pass" if endpoint_center_count == 108 else "fail", "observed": f"{endpoint_center_count}/108", "required": "108/108", "decision": "continue" if endpoint_center_count == 108 else "effects_closed"},
        {"gate": "endpoint_distance_agreement", "status": "pass" if endpoint_agreement_count == 18 else "fail", "observed": f"{endpoint_agreement_count}/18", "required": "18/18", "decision": "continue" if endpoint_agreement_count == 18 else "effects_closed"},
        {"gate": "residual_component_profile_stability", "status": "pass" if component_center_count == 90 else "fail", "observed": f"{component_center_count}/90", "required": "90/90", "decision": "continue" if component_center_count == 90 else "effects_closed"},
        {"gate": "proposal_footprint_overlap", "status": "pass" if proposal_overlap_count == 18 else "fail", "observed": f"{proposal_overlap_count}/18", "required": "18/18", "decision": "continue" if proposal_overlap_count == 18 else "effects_closed"},
        {"gate": "v17d_overall", "status": overall, "observed": f"exclusion={int(exclusion_pass)};starts={start_count}/12;integrity={integrity_count}/384;reverse={reverse_count}/36;representation={representation_count}/12;traversal={traversal_count}/24;resource={resource_count}/24;centers={endpoint_center_count}/108;distance={endpoint_agreement_count}/18;components={component_center_count}/90;footprints={proposal_overlap_count}/18", "required": "1;12/12;384/384;36/36;12/12;24/24;24/24;108/108;18/18;90/90;18/18", "decision": overall},
    ]
    claims = [
        {"claim_id": "C1", "claim": "v17d computes no source spectrum or observed-effect statistic.", "status": "supported" if exclusion_pass else "not_supported", "evidence": "static call audit plus endpoint/transition fields", "scope_limit": "this script and these outputs"},
        {"claim_id": "C2", "claim": "The v17c proposal remains reversible and representation-covariant in the v17d source chain.", "status": "supported" if reverse_count == 36 and representation_count == 12 else "not_supported", "evidence": "v17d_pathwise_reversibility_audit.csv;v17d_representation_audit.csv", "scope_limit": "finite witnesses and 64-step representation checks"},
        {"claim_id": "C3", "claim": "The tested endpoints agree across starts, fresh seeds and early/late windows under all frozen finite thresholds.", "status": "supported" if endpoint_center_count == 108 and endpoint_agreement_count == 18 else "not_supported", "evidence": "v17d_center_stability.csv;v17d_endpoint_agreement.csv", "scope_limit": "six reused finite spaces and 24 chains"},
        {"claim_id": "C4", "claim": "Residual component profiles and empirical proposal footprints agree under the frozen diagnostic thresholds.", "status": "supported" if component_center_count == 90 and proposal_overlap_count == 18 else "not_supported", "evidence": "v17d_residual_component_stability.csv;v17d_proposal_footprint_overlap.csv", "scope_limit": "diagnostics, not global Markov-component proof"},
        {"claim_id": "C5", "claim": "The v17d chain is globally irreducible, converged, mixed, or uniform over the full feasible state space.", "status": "unsupported", "evidence": "none", "scope_limit": "finite diagnostics cannot prove these properties"},
        {"claim_id": "C6", "claim": "The v16s source-spectrum effect survives v17d or the model exhibits Bell correlations, entanglement, Lorentz symmetry or spacetime.", "status": "not_tested", "evidence": "effect calls prohibited and required observables absent", "scope_limit": "requires separate later gates"},
    ]

    v16i.write_csv(ENDPOINT_AUDIT, endpoint_rows)
    v16i.write_csv(PAIRWISE_DISTANCE, pairwise)
    v16i.write_csv(CENTER_STABILITY, center)
    v16i.write_csv(ENDPOINT_AGREEMENT, agreement)
    v16i.write_csv(COMPONENT_PROFILE, component_profiles)
    v16i.write_csv(COMPONENT_STABILITY, component_stability)
    v16i.write_csv(PROPOSAL_FOOTPRINT, footprint_rows)
    v16i.write_csv(PROPOSAL_OVERLAP, overlap)
    v16i.write_csv(TRANSITION_SUMMARY, transitions)
    v16i.write_csv(REVERSIBILITY_AUDIT, reversibility)
    v16i.write_csv(REPRESENTATION_AUDIT, representations)
    v16i.write_csv(SOURCE_SUMMARY, summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    write_documents(overall, gates, summaries, agreement, transitions)
    print(f"[v17d] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    expected_counts = {
        ENDPOINT_AUDIT: 384,
        PAIRWISE_DISTANCE: 6 * (64 * 63 // 2),
        CENTER_STABILITY: 108,
        ENDPOINT_AGREEMENT: 18,
        COMPONENT_PROFILE: 48,
        COMPONENT_STABILITY: 90,
        PROPOSAL_FOOTPRINT: 48,
        PROPOSAL_OVERLAP: 18,
        TRANSITION_SUMMARY: 24,
        REVERSIBILITY_AUDIT: 36,
        REPRESENTATION_AUDIT: 12,
        SOURCE_SUMMARY: 6,
        GATE_EVALUATION: 12,
        CLAIM_LEDGER: 6,
    }
    loaded = {path: v16i.read_csv(path) for path in expected_counts}
    for path, expected in expected_counts.items():
        if len(loaded[path]) != expected:
            raise ValueError(f"v17d row count failed for {path.name}: {len(loaded[path])} != {expected}")
    if implementation_call_counts() != {"spectrum_calls": 0, "effect_metric_calls": 0}:
        raise ValueError("v17d effect exclusion failed")
    if any(int(row["source_spectrum_computed"]) for row in loaded[ENDPOINT_AUDIT]):
        raise ValueError("v17d endpoint rows contain source spectrum")
    if any(int(row["observed_effect_computed"]) for row in loaded[ENDPOINT_AUDIT]):
        raise ValueError("v17d endpoint rows contain observed effect")
    overall = next(row["status"] for row in loaded[GATE_EVALUATION] if row["gate"] == "v17d_overall")
    allowed = {
        "v17d_instrumentation_failed", "v17d_reversibility_not_qualified",
        "v17d_representation_not_qualified", "v17d_finite_traversal_not_qualified",
        "v17d_resource_not_qualified", "v17d_endpoint_centers_not_stable",
        "v17d_endpoint_agreement_not_qualified",
        "v17d_residual_component_profiles_not_stable",
        "v17d_proposal_footprint_overlap_not_qualified",
        "v17d_effect_blind_finite_stability_qualified",
    }
    if overall not in allowed:
        raise ValueError(f"unknown v17d status: {overall}")
    for path in (REPORT, INTERPRETATION, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"v17d documentation missing: {path.name}")
    print(f"[v17d] output verification pass overall={overall}")


def self_test() -> None:
    v17c.self_test()
    if len(EARLY_STEPS) != SAMPLES_PER_WINDOW or len(LATE_STEPS) != SAMPLES_PER_WINDOW:
        raise AssertionError("v17d sample schedule failed")
    if set(EARLY_STEPS) & set(LATE_STEPS):
        raise AssertionError("v17d windows overlap")
    if window_for_step(EARLY_STEPS[0]) != "early" or window_for_step(LATE_STEPS[-1]) != "late":
        raise AssertionError("v17d window classification failed")
    if set_jaccard(frozenset({1, 2}), frozenset({2, 3})) != 1 / 3:
        raise AssertionError("v17d Jaccard failed")
    if implementation_call_counts() != {"spectrum_calls": 0, "effect_metric_calls": 0}:
        raise AssertionError("v17d effect exclusion audit failed")
    print("[v17d] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v17d effect-blind finite stability gate")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if sum((args.prepare_only, args.self_test, args.verify_only)) > 1:
        parser.error("choose only one mode")
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
