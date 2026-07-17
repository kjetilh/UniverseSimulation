#!/usr/bin/env python3
"""v17a effect-blind qualification of a state-local alternating-cycle proposal.

The proposal samples a distinguished, oriented alternating cycle from the
current assignment only. Each auxiliary path is paired bijectively with its
reversed path, and a lazy Metropolis correction uses the exact forward and
reverse path probabilities. The declared target is uniform only inside each
connected component of this proposal kernel. No source spectrum or observed
effect statistic is computed.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random
import statistics
import time
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16v_global_edge_slot_feasibility_gate as v16v
import relational_universe_v16x_explicit_global_measure_gate as v16x
import relational_universe_v16y_reversible_global_measure_gate as v16y
import relational_universe_v16z_alternating_cycle_bridge_gate as v16z
import relational_universe_v16z_postrun_representation_audit as v16zp


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

START_FAMILIES = ("source_assignment", "v16x_random_cost_a0")
CHAIN_SEED_FAMILIES = ("chain_seed_a", "chain_seed_b")
MIN_CYCLE_LENGTH = 2
MAX_CYCLE_LENGTH = 8
TOTAL_STEPS = 512
REPRESENTATION_STEPS = 96
WITNESS_ATTEMPTS_PER_LENGTH = 256
MIN_VALID_PROPOSALS_PER_CHAIN = 64
MIN_ACCEPTED_CYCLES_PER_CHAIN = 32
MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN = 16
MIN_UNIQUE_STATES_PER_CHAIN = 16
MIN_FINAL_START_CHANGE = 0.05
MAX_CHAIN_SECONDS = 60.0

SOURCE_CHAIN = DOC / "v17a_source_chain.csv"
PRE_REGISTRATION = DOC / "v17a_pre_registration.csv"
PROPOSAL_TRACE = DOC / "v17a_cycle_proposal_trace.csv"
REVERSIBILITY_AUDIT = DOC / "v17a_pathwise_reversibility_audit.csv"
REPRESENTATION_AUDIT = DOC / "v17a_representation_audit.csv"
TRANSITION_SUMMARY = DOC / "v17a_chain_transition_summary.csv"
SOURCE_SUMMARY = DOC / "v17a_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v17a_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v17a_claim_ledger.csv"
REPORT = DOC / "v17a_state_independent_cycle_proposal_qualification.md"
INTERPRETATION = DOC / "v17a_interpretation_audit.md"
NEXT_DIRECTION = DOC / "v17a_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_17a_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_17a.md"

Edge = v16x.Edge
Slot = v16x.Slot


@dataclass(frozen=True)
class CycleProposal:
    remove: Tuple[Edge, ...]
    add: Tuple[Edge, ...]


@dataclass(frozen=True)
class CycleKernel:
    space: v16x.StateSpace
    candidate_parents_by_slot: Mapping[Slot, Tuple[int, ...]]


@dataclass
class ChainResult:
    final: frozenset[Edge]
    stats: MutableMapping[str, Any]
    trace: List[Dict[str, Any]]
    transition_digest: str


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v16x", "frozen_state_space", v16x.PRE_REGISTRATION),
        ("v16x", "frozen_reference_endpoints", v16x.ENDPOINT_AUDIT),
        ("v16y", "failed_start_stability_gate", v16y.GATE_EVALUATION),
        ("v16y", "reversible_2x2_measure_preregistration", v16y.PRE_REGISTRATION),
        ("v16z", "pair_cycle_preregistration", v16z.PRE_REGISTRATION),
        ("v16z", "pair_cycle_replay", v16z.REVERSIBILITY_AUDIT),
        ("v16z", "failed_formal_gate", v16z.GATE_EVALUATION),
        ("v16z", "corrected_edge_move_covariance", v16zp.AUDIT_CSV),
        ("v16z", "interpretation_boundary", v16z.INTERPRETATION),
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
        "gate": "v17a_state_independent_cycle_proposal_qualification",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_state_local_oriented_cycle_proposal_qualification",
        "source_history_count": 6,
        "state_space": v16x.COARSE_ARM,
        "start_families": list(START_FAMILIES),
        "chain_seed_families": list(CHAIN_SEED_FAMILIES),
        "proposal": "state_local_distinguished_oriented_alternating_cycle",
        "proposal_target_dependency": "none",
        "proposal_auxiliary_pairing": "reverse_ordered_added_edges",
        "stationary_target_scope": "uniform_per_cycle_proposal_connected_component",
        "metropolis_ratio": "min(1,q_reverse_auxiliary/q_forward_auxiliary)",
        "laziness_probability": "1/2",
        "minimum_cycle_length": MIN_CYCLE_LENGTH,
        "maximum_cycle_length": MAX_CYCLE_LENGTH,
        "total_steps": TOTAL_STEPS,
        "representation_steps": REPRESENTATION_STEPS,
        "witness_attempts_per_length": WITNESS_ATTEMPTS_PER_LENGTH,
        "minimum_valid_proposals_per_chain": MIN_VALID_PROPOSALS_PER_CHAIN,
        "minimum_accepted_cycles_per_chain": MIN_ACCEPTED_CYCLES_PER_CHAIN,
        "minimum_accepted_long_cycles_per_chain": MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN,
        "minimum_unique_states_per_chain": MIN_UNIQUE_STATES_PER_CHAIN,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "representation_scope": "candidate_order_and_semantic_slot_role_relabel_at_both_starts",
        "design_calibration_disclosure": (
            "synthetic pathwise-balance tests and one source-only effect-blind runtime pilot "
            "may run before preregistration; no source spectrum or effect statistic may be inspected"
        ),
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "no_early_stop": True,
        "not_claimed": [
            "global_irreducibility", "mixing", "global_uniform_sampling",
            "start_seed_time_stability", "canonical_physical_measure", "spectrum_effect",
            "energy", "temperature", "dimension", "Lorentz_symmetry", "spacetime",
            "particles", "entanglement", "universe_model",
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
        "proposal": "state_local_distinguished_oriented_alternating_cycle",
        "stationary_target_scope": "uniform_per_cycle_proposal_component",
        "minimum_cycle_length": MIN_CYCLE_LENGTH,
        "maximum_cycle_length": MAX_CYCLE_LENGTH,
        "total_steps": TOTAL_STEPS,
        "representation_steps": REPRESENTATION_STEPS,
        "witness_attempts_per_length": WITNESS_ATTEMPTS_PER_LENGTH,
        "minimum_valid_proposals_per_chain": MIN_VALID_PROPOSALS_PER_CHAIN,
        "minimum_accepted_cycles_per_chain": MIN_ACCEPTED_CYCLES_PER_CHAIN,
        "minimum_accepted_long_cycles_per_chain": MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN,
        "minimum_unique_states_per_chain": MIN_UNIQUE_STATES_PER_CHAIN,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "design_pilot_allowed": 1,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v16zp.verify_outputs()
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v17a] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    expected = {key: str(value) for key, value in preregistration_row().items()}
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v17a preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v17a source chain changed")


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    runs = []
    for source, metadata in v16x.load_runs():
        runs.append((v16i.RunDAG(
            stage="v17a",
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


def build_kernel(space: v16x.StateSpace) -> CycleKernel:
    grouped: Dict[Slot, set[int]] = defaultdict(set)
    for edge in space.candidates:
        grouped[space.slot_by_edge[edge]].add(edge[0])
    return CycleKernel(space, {
        slot: tuple(sorted(parents)) for slot, parents in grouped.items()
    })


def selected_by_parent(selected: Iterable[Edge]) -> Dict[int, Tuple[Edge, ...]]:
    grouped: Dict[int, List[Edge]] = defaultdict(list)
    for edge in selected:
        grouped[edge[0]].append(edge)
    return {parent: tuple(sorted(edges)) for parent, edges in grouped.items()}


def choice_map(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    by_parent: Mapping[int, Tuple[Edge, ...]],
    current_slot: Slot,
    used_parents: frozenset[int],
    used_slots: frozenset[Slot],
    *,
    closure_parent: int | None,
) -> Dict[int, Tuple[Edge, ...]]:
    result: Dict[int, Tuple[Edge, ...]] = {}
    current_child = current_slot[0]
    for parent in kernel.candidate_parents_by_slot.get(current_slot, ()):
        if parent in used_parents or (parent, current_child) in selected:
            continue
        edges = []
        for edge in by_parent.get(parent, ()):
            slot = kernel.space.slot_by_edge[edge]
            if slot in used_slots:
                continue
            if closure_parent is not None:
                if closure_parent not in kernel.candidate_parents_by_slot.get(slot, ()):
                    continue
                if (closure_parent, slot[0]) in selected:
                    continue
            edges.append(edge)
        if edges:
            result[parent] = tuple(edges)
    return result


def derive_adds(kernel: CycleKernel, remove: Sequence[Edge]) -> Tuple[Edge, ...] | None:
    if not remove:
        return None
    adds = tuple(
        (remove[(index + 1) % len(remove)][0], edge[1])
        for index, edge in enumerate(remove)
    )
    if len(set(adds)) != len(adds):
        return None
    for old, new in zip(remove, adds):
        if kernel.space.slot_by_edge.get(new) != kernel.space.slot_by_edge[old]:
            return None
    return adds


def path_probability(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    remove: Sequence[Edge],
) -> Tuple[Fraction, CycleProposal] | None:
    length = len(remove)
    if not MIN_CYCLE_LENGTH <= length <= MAX_CYCLE_LENGTH:
        return None
    if len(set(remove)) != length or not set(remove).issubset(selected):
        return None
    parents = [edge[0] for edge in remove]
    slots = [kernel.space.slot_by_edge[edge] for edge in remove]
    if len(set(parents)) != length or len(set(slots)) != length:
        return None

    ordered_selected = tuple(sorted(selected))
    if not ordered_selected:
        return None
    probability = Fraction(1, MAX_CYCLE_LENGTH - MIN_CYCLE_LENGTH + 1)
    probability *= Fraction(1, len(ordered_selected))
    by_parent = selected_by_parent(selected)
    used_parents = {parents[0]}
    used_slots = {slots[0]}

    for index in range(length - 1):
        closure_parent = parents[0] if index == length - 2 else None
        choices = choice_map(
            kernel, selected, by_parent, slots[index],
            frozenset(used_parents), frozenset(used_slots),
            closure_parent=closure_parent,
        )
        parent_options = tuple(sorted(choices))
        next_parent = parents[index + 1]
        next_edge = remove[index + 1]
        if next_parent not in choices or next_edge not in choices[next_parent]:
            return None
        probability *= Fraction(1, len(parent_options))
        probability *= Fraction(1, len(choices[next_parent]))
        used_parents.add(next_parent)
        used_slots.add(slots[index + 1])

    adds = derive_adds(kernel, remove)
    if adds is None or set(adds) & selected:
        return None
    proposal = CycleProposal(tuple(remove), adds)
    try:
        apply_proposal(kernel.space, selected, proposal)
    except ValueError:
        return None
    return probability, proposal


def propose_cycle(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    rng: random.Random,
    *,
    forced_length: int | None = None,
) -> Tuple[Fraction, CycleProposal] | None:
    length = forced_length
    if length is None:
        length = rng.randrange(MIN_CYCLE_LENGTH, MAX_CYCLE_LENGTH + 1)
    if not MIN_CYCLE_LENGTH <= length <= MAX_CYCLE_LENGTH:
        raise ValueError("forced cycle length outside frozen bounds")
    ordered_selected = tuple(sorted(selected))
    if not ordered_selected:
        return None
    first = ordered_selected[rng.randrange(len(ordered_selected))]
    remove = [first]
    by_parent = selected_by_parent(selected)
    used_parents = {first[0]}
    used_slots = {kernel.space.slot_by_edge[first]}

    for index in range(length - 1):
        current_slot = kernel.space.slot_by_edge[remove[-1]]
        closure_parent = first[0] if index == length - 2 else None
        choices = choice_map(
            kernel, selected, by_parent, current_slot,
            frozenset(used_parents), frozenset(used_slots),
            closure_parent=closure_parent,
        )
        parent_options = tuple(sorted(choices))
        if not parent_options:
            return None
        parent = parent_options[rng.randrange(len(parent_options))]
        edges = choices[parent]
        edge = edges[rng.randrange(len(edges))]
        remove.append(edge)
        used_parents.add(parent)
        used_slots.add(kernel.space.slot_by_edge[edge])
    return path_probability(kernel, selected, tuple(remove))


def apply_proposal(
    space: v16x.StateSpace,
    selected: frozenset[Edge],
    proposal: CycleProposal,
) -> frozenset[Edge]:
    if not set(proposal.remove).issubset(selected) or set(proposal.add) & selected:
        raise ValueError("invalid cycle proposal occupancy")
    result = frozenset((set(selected) - set(proposal.remove)) | set(proposal.add))
    if not v16x.assignment_integrity(space, result):
        raise ValueError("cycle proposal broke assignment integrity")
    return result


def reverse_remove_sequence(proposal: CycleProposal) -> Tuple[Edge, ...]:
    return tuple(reversed(proposal.add))


def proposal_digest(proposal: CycleProposal) -> str:
    payload = json.dumps({
        "remove": proposal.remove,
        "add": proposal.add,
    }, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def exact_accept(rng: random.Random, probability: Fraction) -> bool:
    if probability <= 0 or probability > 1:
        raise ValueError("acceptance probability outside [0,1]")
    return probability == 1 or rng.randrange(probability.denominator) < probability.numerator


def chain_seed(dag: v16i.RunDAG, start_family: str, seed_family: str) -> int:
    return v16i.stable_seed("v17a", "chain", start_family, seed_family, *dag.key)


def run_chain(
    dag: v16i.RunDAG,
    kernel: CycleKernel,
    start: frozenset[Edge],
    start_family: str,
    seed_family: str,
    *,
    total_steps: int = TOTAL_STEPS,
) -> ChainResult:
    seed = chain_seed(dag, start_family, seed_family)
    rng = random.Random(seed)
    selected = start
    trace: List[Dict[str, Any]] = []
    visited = {v16x.edge_digest(selected)}
    counts = Counter()
    accepted_lengths = Counter()
    started = time.monotonic()

    for step in range(1, total_steps + 1):
        event = "lazy_stay"
        proposal: CycleProposal | None = None
        q_forward: Fraction | None = None
        q_reverse: Fraction | None = None
        acceptance: Fraction | None = None
        accepted = False
        before_digest = v16x.edge_digest(selected)

        if rng.getrandbits(1):
            counts["nonlazy_steps"] += 1
            proposed_auxiliary = propose_cycle(kernel, selected, rng)
            if proposed_auxiliary is None:
                event = "proposal_dead_end"
                counts["proposal_dead_end"] += 1
            else:
                q_forward, proposal = proposed_auxiliary
                proposed = apply_proposal(kernel.space, selected, proposal)
                reverse = path_probability(kernel, proposed, reverse_remove_sequence(proposal))
                counts["valid_proposals"] += 1
                if reverse is None:
                    event = "reverse_unsupported"
                    counts["reverse_unsupported"] += 1
                else:
                    q_reverse, reverse_proposal = reverse
                    if apply_proposal(kernel.space, proposed, reverse_proposal) != selected:
                        raise ValueError("reverse auxiliary did not recover prior state")
                    counts["reverse_supported"] += 1
                    acceptance = min(Fraction(1), q_reverse / q_forward)
                    if exact_accept(rng, acceptance):
                        selected = proposed
                        accepted = True
                        event = "accepted_cycle"
                        counts["accepted_cycles"] += 1
                        accepted_lengths[len(proposal.remove)] += 1
                        if len(proposal.remove) >= 3:
                            counts["accepted_long_cycles"] += 1
                        visited.add(v16x.edge_digest(selected))
                    else:
                        event = "metropolis_reject"
                        counts["metropolis_rejects"] += 1
        else:
            counts["lazy_stays"] += 1

        after_digest = v16x.edge_digest(selected)
        trace.append({
            **dag.prefix,
            "start_family": start_family,
            "chain_seed_family": seed_family,
            "chain_seed": seed,
            "step": step,
            "event": event,
            "cycle_length": len(proposal.remove) if proposal else 0,
            "proposal_sha256": proposal_digest(proposal) if proposal else "",
            "remove_edges_json": json.dumps(proposal.remove, separators=(",", ":")) if proposal else "[]",
            "add_edges_json": json.dumps(proposal.add, separators=(",", ":")) if proposal else "[]",
            "q_forward_numerator": q_forward.numerator if q_forward else 0,
            "q_forward_denominator": q_forward.denominator if q_forward else 0,
            "q_reverse_numerator": q_reverse.numerator if q_reverse else 0,
            "q_reverse_denominator": q_reverse.denominator if q_reverse else 0,
            "acceptance_numerator": acceptance.numerator if acceptance else 0,
            "acceptance_denominator": acceptance.denominator if acceptance else 0,
            "accepted": int(accepted),
            "state_before_sha256": before_digest,
            "state_after_sha256": after_digest,
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })

    elapsed = time.monotonic() - started
    final_change = 1.0 - len(selected & start) / kernel.space.edge_count
    movement_pass = all((
        counts["valid_proposals"] >= MIN_VALID_PROPOSALS_PER_CHAIN,
        counts["accepted_cycles"] >= MIN_ACCEPTED_CYCLES_PER_CHAIN,
        counts["accepted_long_cycles"] >= MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN,
        len(visited) >= MIN_UNIQUE_STATES_PER_CHAIN,
        final_change >= MIN_FINAL_START_CHANGE,
        counts["reverse_unsupported"] == 0,
        v16x.assignment_integrity(kernel.space, selected),
    ))
    stats: Dict[str, Any] = {
        **dag.prefix,
        "start_family": start_family,
        "chain_seed_family": seed_family,
        "chain_seed": seed,
        "start_endpoint_sha256": v16x.edge_digest(start),
        "final_endpoint_sha256": v16x.edge_digest(selected),
        "total_steps": total_steps,
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
        "final_start_changed_edge_fraction": final_change,
        "elapsed_seconds": elapsed,
        "minimum_valid_proposals": MIN_VALID_PROPOSALS_PER_CHAIN,
        "minimum_accepted_cycles": MIN_ACCEPTED_CYCLES_PER_CHAIN,
        "minimum_accepted_long_cycles": MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN,
        "minimum_unique_states": MIN_UNIQUE_STATES_PER_CHAIN,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "resource_pass": int(elapsed <= MAX_CHAIN_SECONDS),
        "movement_pass": int(movement_pass),
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }
    digest_payload = [{
        "event": row["event"],
        "cycle_length": row["cycle_length"],
        "proposal": row["proposal_sha256"],
        "accepted": row["accepted"],
        "after": row["state_after_sha256"],
    } for row in trace]
    transition_digest = hashlib.sha256(json.dumps(
        digest_payload, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()
    return ChainResult(selected, stats, trace, transition_digest)


def reversibility_rows(
    dag: v16i.RunDAG,
    kernel: CycleKernel,
    start: frozenset[Edge],
    start_family: str,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for length in range(MIN_CYCLE_LENGTH, MAX_CYCLE_LENGTH + 1):
        rng = random.Random(v16i.stable_seed(
            "v17a", "reversibility", start_family, length, *dag.key
        ))
        witness = None
        attempts = 0
        while witness is None and attempts < WITNESS_ATTEMPTS_PER_LENGTH:
            attempts += 1
            witness = propose_cycle(kernel, start, rng, forced_length=length)
        if witness is None:
            rows.append({
                **dag.prefix,
                "start_family": start_family,
                "cycle_length": length,
                "attempts": attempts,
                "proposal_sha256": "",
                "q_forward_numerator": 0,
                "q_forward_denominator": 0,
                "q_reverse_numerator": 0,
                "q_reverse_denominator": 0,
                "forward_acceptance_numerator": 0,
                "forward_acceptance_denominator": 0,
                "reverse_acceptance_numerator": 0,
                "reverse_acceptance_denominator": 0,
                "reverse_support_pass": 0,
                "forward_integrity_pass": 0,
                "reverse_recovery_pass": 0,
                "pathwise_detailed_balance_pass": 0,
            })
            continue
        q_forward, proposal = witness
        proposed = apply_proposal(kernel.space, start, proposal)
        reverse = path_probability(kernel, proposed, reverse_remove_sequence(proposal))
        if reverse is None:
            q_reverse = Fraction(0)
            reverse_recovery = False
            balance = False
            reverse_acceptance = Fraction(0)
        else:
            q_reverse, reverse_proposal = reverse
            reverse_recovery = apply_proposal(kernel.space, proposed, reverse_proposal) == start
            forward_acceptance = min(Fraction(1), q_reverse / q_forward)
            reverse_acceptance = min(Fraction(1), q_forward / q_reverse)
            forward_flow = Fraction(1, 2) * q_forward * forward_acceptance
            reverse_flow = Fraction(1, 2) * q_reverse * reverse_acceptance
            balance = forward_flow == reverse_flow
        forward_acceptance = min(Fraction(1), q_reverse / q_forward) if q_reverse else Fraction(0)
        rows.append({
            **dag.prefix,
            "start_family": start_family,
            "cycle_length": length,
            "attempts": attempts,
            "proposal_sha256": proposal_digest(proposal),
            "q_forward_numerator": q_forward.numerator,
            "q_forward_denominator": q_forward.denominator,
            "q_reverse_numerator": q_reverse.numerator,
            "q_reverse_denominator": q_reverse.denominator,
            "forward_acceptance_numerator": forward_acceptance.numerator,
            "forward_acceptance_denominator": forward_acceptance.denominator,
            "reverse_acceptance_numerator": reverse_acceptance.numerator,
            "reverse_acceptance_denominator": reverse_acceptance.denominator,
            "reverse_support_pass": int(reverse is not None),
            "forward_integrity_pass": int(v16x.assignment_integrity(kernel.space, proposed)),
            "reverse_recovery_pass": int(reverse_recovery),
            "pathwise_detailed_balance_pass": int(balance),
        })
    return rows


def representation_row(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    space: v16x.StateSpace,
    start: frozenset[Edge],
    start_family: str,
) -> Dict[str, Any]:
    original = run_chain(
        dag, build_kernel(space), start, start_family, "representation_seed",
        total_steps=REPRESENTATION_STEPS,
    )
    replay = run_chain(
        dag, build_kernel(space), start, start_family, "representation_seed",
        total_steps=REPRESENTATION_STEPS,
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
    reordered = run_chain(
        dag, build_kernel(reversed_space), start, start_family, "representation_seed",
        total_steps=REPRESENTATION_STEPS,
    )
    relabeled_metadata = v16x.v16w.relabel_metadata(
        metadata, v16i.stable_seed("v17a", "semantic_relabel", start_family, *dag.key)
    )
    relabeled_space = v16x.build_state_space(dag, relabeled_metadata, v16x.COARSE_ARM)
    relabeled = run_chain(
        dag, build_kernel(relabeled_space), start, start_family, "representation_seed",
        total_steps=REPRESENTATION_STEPS,
    )
    candidate_set_pass = set(space.candidates) == set(relabeled_space.candidates)
    replay_pass = (
        original.final == replay.final
        and original.transition_digest == replay.transition_digest
    )
    order_pass = (
        original.final == reordered.final
        and original.transition_digest == reordered.transition_digest
    )
    relabel_pass = (
        original.final == relabeled.final
        and original.transition_digest == relabeled.transition_digest
    )
    passed = all((candidate_set_pass, replay_pass, order_pass, relabel_pass))
    return {
        **dag.prefix,
        "start_family": start_family,
        "check_steps": REPRESENTATION_STEPS,
        "original_endpoint_sha256": v16x.edge_digest(original.final),
        "replay_endpoint_sha256": v16x.edge_digest(replay.final),
        "reordered_endpoint_sha256": v16x.edge_digest(reordered.final),
        "relabeled_endpoint_sha256": v16x.edge_digest(relabeled.final),
        "original_transition_sha256": original.transition_digest,
        "replay_transition_sha256": replay.transition_digest,
        "reordered_transition_sha256": reordered.transition_digest,
        "relabeled_transition_sha256": relabeled.transition_digest,
        "candidate_set_covariance_pass": int(candidate_set_pass),
        "exact_replay_pass": int(replay_pass),
        "candidate_order_covariance_pass": int(order_pass),
        "semantic_relabel_covariance_pass": int(relabel_pass),
        "representation_pass": int(passed),
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


def write_documents(
    overall: str,
    gate_rows: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    transition_rows: Sequence[Mapping[str, Any]],
) -> None:
    qualified = overall == "v17a_state_independent_cycle_proposal_qualified"
    minimum_acceptance = min(int(row["accepted_cycles"]) for row in transition_rows)
    minimum_long = min(int(row["accepted_long_cycles"]) for row in transition_rows)
    minimum_change = min(float(row["final_start_changed_edge_fraction"]) for row in transition_rows)
    maximum_seconds = max(float(row["elapsed_seconds"]) for row in transition_rows)
    report = [
        "# v17a state-independent cycle proposal qualification",
        "",
        f"Status: `{overall}`.",
        "",
        "## Evidential status",
        "",
        "The proposal uses only the current valid assignment and the frozen candidate graph. It does not inspect the paired target assignment, source spectrum, or observed effect.",
        "",
        "A proposal is a distinguished oriented alternating cycle of length `2-8`. Its reverse auxiliary is the reversed ordered list of added edges. The lazy Metropolis acceptance uses the exact ratio of those two auxiliary-path probabilities. This establishes only pathwise detailed balance for tested transitions and a component-uniform target, never global connectivity or mixing.",
        "",
        "## Source qualification",
        "",
        *markdown_table(summaries, (
            "growth_seed", "run_offset", "representation_passes", "reversibility_passes",
            "movement_passes", "minimum_accepted_cycles", "minimum_final_start_changed_edge_fraction",
            "maximum_chain_seconds", "source_qualification_pass",
        )),
        "",
        "## Gates",
        "",
        *markdown_table(gate_rows, ("gate", "status", "observed", "required", "decision")),
        "",
        "## Interpretation boundary",
        "",
        f"Across the finite chains, minimum accepted cycles were `{minimum_acceptance}`, minimum accepted length>=3 cycles were `{minimum_long}`, minimum final start change was `{minimum_change:.6f}`, and maximum chain runtime was `{maximum_seconds:.6f}` seconds.",
        "",
        "State-independent here means target-independent: the proposal law depends on the current state, as every Markov kernel does. A qualified finite proposal does not establish irreducibility, convergence, mixing, a global uniform law, or a physical ensemble.",
        "",
        "V17a establishes no source-spectrum effect, energy, temperature, invariant, dimension, Lorentz symmetry, spacetime, particle, entanglement, continuum, or universe model.",
        "",
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    INTERPRETATION.write_text(
        "# v17a interpretation audit\n\n"
        f"Frozen status is `{overall}`. "
        "The algebraic claim is limited to exact assignment-preserving cycle exchanges and pathwise auxiliary detailed balance on tested transitions. "
        "The generated trajectories are finite proposal diagnostics on six reused spaces. They do not prove global irreducibility, stationarity from arbitrary starts, convergence, mixing time, or physical probability. "
        "No source spectrum or observed-effect statistic was computed.\n",
        encoding="utf-8",
    )
    if qualified:
        next_text = (
            "The next gate should be `v17b_cycle_measure_start_seed_time_stability`, still effect-blind on the same six spaces. "
            "Freeze longer chains, at least two starts and two independent chain-seed families, compare early/late windows, and add component-overlap diagnostics. "
            "Only if start, seed and time stability all pass may a fresh global-null holdout reopen the frozen v16s spectrum contrast."
        )
        recommendation = "Proceed to v17b finite stability; do not compute the source spectrum yet."
    else:
        next_text = (
            "Do not run a start/seed/time effect comparison. Diagnose the first failed v17a layer. "
            "Repair only representation or reverse-support instrumentation failures; if exact pathwise balance passes but finite movement fails, retire this bounded cycle proposal rather than increasing budget automatically."
        )
        recommendation = "Stop before spectrum/effect and repair or retire the failed proposal layer."
    NEXT_DIRECTION.write_text(
        "# v17a next direction\n\n"
        f"Formal status: `{overall}`.\n\n{next_text}\n",
        encoding="utf-8",
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.17a\n\n"
        f"- status: `{overall}`\n"
        f"- next: {recommendation}\n"
        "- claim ceiling: finite target-independent proposal qualification, not global sampling or physics\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf v0.17a for ikke-spesialister\n\n"
        "Denne runden tester en ny maate aa flytte mellom gyldige globale hendelsesgrafer paa uten aa vite hvilken maalgraf man vil ende i. "
        "Hvert forslag kan gaa eksakt tilbake, og forskjeller i hvor lett frem- og tilbakeslaget foreslaas blir korrigert matematisk.\n\n"
        f"Statusen er `{overall}`. Selv en bestaa-status betyr bare at flytteregelen er en kvalifisert kandidat for en senere stabilitetstest. "
        "Den beviser ikke at alle grafer kan naas, at kjeden er blandet, eller at resultatet er en fysisk lov.\n",
        encoding="utf-8",
    )


def run() -> None:
    verify_frozen_sources()
    frozen_digests = v16z.frozen_start_digests()
    trace_rows: List[Dict[str, Any]] = []
    reversibility: List[Dict[str, Any]] = []
    representations: List[Dict[str, Any]] = []
    transitions: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []

    for run_index, (dag, metadata) in enumerate(load_runs(), start=1):
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        kernel = build_kernel(space)
        starts = {
            "source_assignment": space.source_edges,
            "v16x_random_cost_a0": v16z.random_cost_start(dag, space),
        }
        digest_passes = {}
        for start_family, start in starts.items():
            frozen = frozen_digests[(dag.growth_seed, dag.run_offset, start_family)]
            digest_passes[start_family] = int(v16x.edge_digest(start) == frozen)
            representations.append(representation_row(
                dag, metadata, space, start, start_family
            ))
            reversibility.extend(reversibility_rows(
                dag, kernel, start, start_family
            ))
            for seed_family in CHAIN_SEED_FAMILIES:
                result = run_chain(dag, kernel, start, start_family, seed_family)
                trace_rows.extend(result.trace)
                transitions.append(dict(result.stats))

        source_representation = [
            row for row in representations
            if int(row["growth_seed"]) == dag.growth_seed
            and int(row["run_offset"]) == dag.run_offset
        ]
        source_reversibility = [
            row for row in reversibility
            if int(row["growth_seed"]) == dag.growth_seed
            and int(row["run_offset"]) == dag.run_offset
        ]
        source_transitions = [
            row for row in transitions
            if int(row["growth_seed"]) == dag.growth_seed
            and int(row["run_offset"]) == dag.run_offset
        ]
        representation_passes = sum(int(row["representation_pass"]) for row in source_representation)
        reversibility_passes = sum(int(row["pathwise_detailed_balance_pass"]) for row in source_reversibility)
        movement_passes = sum(int(row["movement_pass"]) for row in source_transitions)
        resource_passes = sum(int(row["resource_pass"]) for row in source_transitions)
        source_pass = all((
            sum(digest_passes.values()) == 2,
            representation_passes == 2,
            reversibility_passes == 14,
            movement_passes == 4,
            resource_passes == 4,
        ))
        summaries.append({
            **dag.prefix,
            "frozen_start_digest_passes": sum(digest_passes.values()),
            "representation_passes": representation_passes,
            "reversibility_passes": reversibility_passes,
            "movement_passes": movement_passes,
            "resource_passes": resource_passes,
            "minimum_valid_proposals": min(int(row["valid_proposals"]) for row in source_transitions),
            "minimum_accepted_cycles": min(int(row["accepted_cycles"]) for row in source_transitions),
            "minimum_accepted_long_cycles": min(int(row["accepted_long_cycles"]) for row in source_transitions),
            "minimum_unique_state_count": min(int(row["unique_state_count"]) for row in source_transitions),
            "minimum_final_start_changed_edge_fraction": min(float(row["final_start_changed_edge_fraction"]) for row in source_transitions),
            "maximum_chain_seconds": max(float(row["elapsed_seconds"]) for row in source_transitions),
            "source_qualification_pass": int(source_pass),
        })
        print(
            f"[v17a] sources={run_index}/6 representation={representation_passes}/2 "
            f"balance={reversibility_passes}/14 movement={movement_passes}/4"
        )

    calls = implementation_call_counts()
    exclusion_pass = (
        calls == {"spectrum_calls": 0, "effect_metric_calls": 0}
        and all(int(row["source_spectrum_computed"]) == 0 for row in trace_rows)
        and all(int(row["observed_effect_computed"]) == 0 for row in trace_rows)
    )
    digest_count = sum(int(row["frozen_start_digest_passes"]) for row in summaries)
    representation_count = sum(int(row["representation_pass"]) for row in representations)
    reverse_support_count = sum(int(row["reverse_support_pass"]) for row in reversibility)
    balance_count = sum(int(row["pathwise_detailed_balance_pass"]) for row in reversibility)
    movement_count = sum(int(row["movement_pass"]) for row in transitions)
    resource_count = sum(int(row["resource_pass"]) for row in transitions)

    if not exclusion_pass or digest_count != 12:
        overall = "v17a_instrumentation_failed"
    elif representation_count != 12:
        overall = "v17a_cycle_proposal_representation_not_qualified"
    elif reverse_support_count != 84:
        overall = "v17a_cycle_reverse_support_not_qualified"
    elif balance_count != 84:
        overall = "v17a_pathwise_detailed_balance_not_qualified"
    elif movement_count != 24:
        overall = "v17a_cycle_proposal_finite_movement_not_qualified"
    elif resource_count != 24:
        overall = "v17a_cycle_proposal_resource_not_qualified"
    else:
        overall = "v17a_state_independent_cycle_proposal_qualified"

    gate_rows = [
        {
            "gate": "effect_blind_integrity",
            "status": "pass" if exclusion_pass else "fail",
            "observed": f"spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}",
            "required": "0;0",
            "decision": "continue" if exclusion_pass else "invalidate",
        },
        {
            "gate": "frozen_start_replay",
            "status": "pass" if digest_count == 12 else "fail",
            "observed": f"{digest_count}/12",
            "required": "12/12",
            "decision": "continue" if digest_count == 12 else "invalidate",
        },
        {
            "gate": "representation_covariance",
            "status": "pass" if representation_count == 12 else "fail",
            "observed": f"{representation_count}/12",
            "required": "12/12",
            "decision": "continue" if representation_count == 12 else "repair_representation",
        },
        {
            "gate": "exact_reverse_auxiliary_support",
            "status": "pass" if reverse_support_count == 84 else "fail",
            "observed": f"{reverse_support_count}/84",
            "required": "84/84",
            "decision": "continue" if reverse_support_count == 84 else "repair_or_retire_proposal",
        },
        {
            "gate": "pathwise_detailed_balance",
            "status": "pass" if balance_count == 84 else "fail",
            "observed": f"{balance_count}/84",
            "required": "84/84",
            "decision": "continue" if balance_count == 84 else "repair_metropolis_ratio",
        },
        {
            "gate": "finite_movement",
            "status": "pass" if movement_count == 24 else "fail",
            "observed": f"{movement_count}/24",
            "required": "24/24",
            "decision": "continue" if movement_count == 24 else "retire_or_redesign_proposal",
        },
        {
            "gate": "resource_bound",
            "status": "pass" if resource_count == 24 else "fail",
            "observed": f"{resource_count}/24",
            "required": "24/24",
            "decision": "continue" if resource_count == 24 else "optimize_before_stability",
        },
        {
            "gate": "v17a_overall",
            "status": overall,
            "observed": (
                f"exclusion={int(exclusion_pass)};starts={digest_count}/12;"
                f"representation={representation_count}/12;reverse={reverse_support_count}/84;"
                f"balance={balance_count}/84;movement={movement_count}/24;resource={resource_count}/24"
            ),
            "required": "1;12/12;12/12;84/84;84/84;24/24;24/24",
            "decision": overall,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "The implemented cycle proposal is target-independent and uses only the current assignment plus frozen candidates.",
            "status": "supported" if exclusion_pass else "not_supported",
            "evidence": "specification and effect-exclusion audit",
            "scope_limit": "algorithmic proposal property; not physical state independence",
        },
        {
            "claim_id": "C2",
            "claim": "Every tested oriented auxiliary has exact reverse support and satisfies pathwise detailed balance.",
            "status": "supported" if reverse_support_count == balance_count == 84 else "not_supported",
            "evidence": "v17a_pathwise_reversibility_audit.csv",
            "scope_limit": "84 finite witnesses across six spaces and two starts",
        },
        {
            "claim_id": "C3",
            "claim": "The finite proposal execution is replay-, candidate-order-, and semantic-role-relabel covariant on both starts.",
            "status": "supported" if representation_count == 12 else "not_supported",
            "evidence": "v17a_representation_audit.csv",
            "scope_limit": "tested role relabel; not a proof of every graph automorphism",
        },
        {
            "claim_id": "C4",
            "claim": "The proposal has qualified finite movement under the frozen 512-step budget.",
            "status": "supported" if movement_count == 24 else "not_supported",
            "evidence": "v17a_chain_transition_summary.csv",
            "scope_limit": "finite mobility; not convergence or mixing",
        },
        {
            "claim_id": "C5",
            "claim": "The cycle kernel is globally irreducible, mixed, or uniform over the full feasible space.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "v17a target is component-uniform only",
        },
        {
            "claim_id": "C6",
            "claim": "The frozen v16s spectrum contrast survives the v17a measure.",
            "status": "not_tested",
            "evidence": "spectrum and effect calls are prohibited",
            "scope_limit": "requires later stability qualification and fresh holdout",
        },
    ]

    v16i.write_csv(PROPOSAL_TRACE, trace_rows)
    v16i.write_csv(REVERSIBILITY_AUDIT, reversibility)
    v16i.write_csv(REPRESENTATION_AUDIT, representations)
    v16i.write_csv(TRANSITION_SUMMARY, transitions)
    v16i.write_csv(SOURCE_SUMMARY, summaries)
    v16i.write_csv(GATE_EVALUATION, gate_rows)
    v16i.write_csv(CLAIM_LEDGER, claims)
    write_documents(overall, gate_rows, summaries, transitions)
    print(f"[v17a] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    trace = v16i.read_csv(PROPOSAL_TRACE)
    reversibility = v16i.read_csv(REVERSIBILITY_AUDIT)
    representations = v16i.read_csv(REPRESENTATION_AUDIT)
    transitions = v16i.read_csv(TRANSITION_SUMMARY)
    summaries = v16i.read_csv(SOURCE_SUMMARY)
    gates = v16i.read_csv(GATE_EVALUATION)
    claims = v16i.read_csv(CLAIM_LEDGER)
    if len(trace) != 24 * TOTAL_STEPS:
        raise ValueError("v17a proposal trace row count failed")
    if len(reversibility) != 84 or len(representations) != 12:
        raise ValueError("v17a reversibility/representation row count failed")
    if len(transitions) != 24 or len(summaries) != 6:
        raise ValueError("v17a transition/source row count failed")
    if len(gates) != 8 or len(claims) != 6:
        raise ValueError("v17a gate/claim row count failed")
    if implementation_call_counts() != {"spectrum_calls": 0, "effect_metric_calls": 0}:
        raise ValueError("v17a effect exclusion failed")
    if any(int(row["source_spectrum_computed"]) for row in trace):
        raise ValueError("v17a trace contains spectrum computation")
    if any(int(row["observed_effect_computed"]) for row in trace):
        raise ValueError("v17a trace contains effect computation")
    overall = next(row["status"] for row in gates if row["gate"] == "v17a_overall")
    allowed = {
        "v17a_instrumentation_failed",
        "v17a_cycle_proposal_representation_not_qualified",
        "v17a_cycle_reverse_support_not_qualified",
        "v17a_pathwise_detailed_balance_not_qualified",
        "v17a_cycle_proposal_finite_movement_not_qualified",
        "v17a_cycle_proposal_resource_not_qualified",
        "v17a_state_independent_cycle_proposal_qualified",
    }
    if overall not in allowed:
        raise ValueError("v17a overall status is unknown")
    for path in (REPORT, INTERPRETATION, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"v17a documentation missing: {path.name}")
    print(f"[v17a] output verification pass overall={overall}")


def self_test() -> None:
    role: v16v.Role = ("test", ("resource",))
    klass: v16v.SlotClass = (role, 0, "witness")
    parents = (0, 1, 2)
    children = (10, 11, 12)
    candidates = tuple((parent, child) for parent in parents for child in children)
    source = frozenset({(0, 10), (1, 11), (2, 12)})
    space = v16x.StateSpace(
        arm="test",
        candidates=candidates,
        source_edges=source,
        slot_by_edge={edge: (edge[1], klass) for edge in candidates},
        parent_demands={parent: 1 for parent in parents},
        slot_demands={(child, klass): 1 for child in children},
        edge_count=3,
    )
    kernel = build_kernel(space)
    remove = ((0, 10), (1, 11), (2, 12))
    forward = path_probability(kernel, source, remove)
    if forward is None:
        raise AssertionError("v17a synthetic forward path missing")
    q_forward, proposal = forward
    proposed = apply_proposal(space, source, proposal)
    reverse = path_probability(kernel, proposed, reverse_remove_sequence(proposal))
    if reverse is None:
        raise AssertionError("v17a synthetic reverse path missing")
    q_reverse, reverse_proposal = reverse
    if apply_proposal(space, proposed, reverse_proposal) != source:
        raise AssertionError("v17a synthetic reverse recovery failed")
    left = Fraction(1, 2) * q_forward * min(Fraction(1), q_reverse / q_forward)
    right = Fraction(1, 2) * q_reverse * min(Fraction(1), q_forward / q_reverse)
    if left != right:
        raise AssertionError("v17a synthetic pathwise balance failed")
    if implementation_call_counts() != {"spectrum_calls": 0, "effect_metric_calls": 0}:
        raise AssertionError("v17a effect exclusion audit failed")
    if spec_payload()["proposal_target_dependency"] != "none":
        raise AssertionError("v17a proposal must be target-independent")
    print("[v17a] self-test pass")


def pilot() -> None:
    dag, metadata = load_runs()[0]
    space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
    result = run_chain(
        dag, build_kernel(space), space.source_edges,
        "source_assignment", "pilot_seed", total_steps=128,
    )
    stats = result.stats
    print(json.dumps({
        "source": list(dag.key),
        "steps": 128,
        "valid_proposals": stats["valid_proposals"],
        "accepted_cycles": stats["accepted_cycles"],
        "accepted_long_cycles": stats["accepted_long_cycles"],
        "unique_state_count": stats["unique_state_count"],
        "final_start_changed_edge_fraction": stats["final_start_changed_edge_fraction"],
        "elapsed_seconds": stats["elapsed_seconds"],
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description="v17a state-independent cycle proposal qualification")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if sum((args.prepare_only, args.self_test, args.pilot, args.verify_only)) > 1:
        parser.error("choose only one mode")
    if args.prepare_only:
        prepare()
    elif args.self_test:
        self_test()
    elif args.pilot:
        pilot()
    elif args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
