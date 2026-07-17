#!/usr/bin/env python3
"""v17b effect-blind qualification of a residual-cycle enumerator proposal.

The proposal starts from the current assignment only. For one uniformly chosen
selected edge and exact length, it enumerates all simple residual alternating
cycles and samples one uniformly. Every distinguished auxiliary is paired with
the same exact length and the reversed ordered added edges. Exact lazy
Metropolis correction targets a uniform law only inside each proposal-connected
component. No source spectrum or observed-effect statistic is computed.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
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
import relational_universe_v16x_explicit_global_measure_gate as v16x
import relational_universe_v16z_alternating_cycle_bridge_gate as v16z
import relational_universe_v17a_state_independent_cycle_proposal_qualification as v17a
import relational_universe_v17a_postrun_movement_diagnosis as v17ap


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

START_FAMILIES = v17a.START_FAMILIES
CHAIN_SEED_FAMILIES = v17a.CHAIN_SEED_FAMILIES
EXACT_LENGTH_CHOICES = (2, 3, 4)
MAX_CYCLE_LENGTH = max(EXACT_LENGTH_CHOICES)
TOTAL_STEPS = v17a.TOTAL_STEPS
REPRESENTATION_STEPS = v17a.REPRESENTATION_STEPS
WITNESS_ATTEMPTS_PER_LENGTH = 128
MIN_VALID_PROPOSALS_PER_CHAIN = v17a.MIN_VALID_PROPOSALS_PER_CHAIN
MIN_ACCEPTED_CYCLES_PER_CHAIN = v17a.MIN_ACCEPTED_CYCLES_PER_CHAIN
MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN = v17a.MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN
MIN_UNIQUE_STATES_PER_CHAIN = v17a.MIN_UNIQUE_STATES_PER_CHAIN
MIN_FINAL_START_CHANGE = v17a.MIN_FINAL_START_CHANGE
MAX_CHAIN_SECONDS = v17a.MAX_CHAIN_SECONDS
MIN_PAIRED_VALID_IMPROVEMENTS = 24
MIN_MEDIAN_VALID_PROPOSAL_RATIO = 2.0

SOURCE_CHAIN = DOC / "v17b_source_chain.csv"
PRE_REGISTRATION = DOC / "v17b_pre_registration.csv"
PROPOSAL_TRACE = DOC / "v17b_residual_cycle_trace.csv"
REVERSIBILITY_AUDIT = DOC / "v17b_pathwise_reversibility_audit.csv"
REPRESENTATION_AUDIT = DOC / "v17b_representation_audit.csv"
TRANSITION_SUMMARY = DOC / "v17b_chain_transition_summary.csv"
PAIRED_IMPROVEMENT = DOC / "v17b_paired_v17a_improvement.csv"
SOURCE_SUMMARY = DOC / "v17b_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v17b_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v17b_claim_ledger.csv"
REPORT = DOC / "v17b_residual_cycle_constructor_gate.md"
INTERPRETATION = DOC / "v17b_interpretation_audit.md"
NEXT_DIRECTION = DOC / "v17b_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_17b_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_17b.md"

Edge = v16x.Edge
Slot = v16x.Slot
CycleKernel = v17a.CycleKernel
CycleProposal = v17a.CycleProposal


@dataclass(frozen=True)
class ResidualAuxiliary:
    probability: Fraction
    proposal: CycleProposal
    cycle_length: int
    cycle_count_for_start: int


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
        ("v16z", "frozen_start_pair_replay", v16z.REVERSIBILITY_AUDIT),
        ("v17a", "failed_proposal_preregistration", v17a.PRE_REGISTRATION),
        ("v17a", "failed_proposal_gate", v17a.GATE_EVALUATION),
        ("v17a", "matched_chain_baseline", v17a.TRANSITION_SUMMARY),
        ("v17a", "movement_diagnosis", v17ap.DIAGNOSIS_CSV),
        ("v17a", "proposal_implementation", v17a.SCRIPT),
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
        "gate": "v17b_residual_cycle_constructor_gate",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_residual_completion_proposal_qualification",
        "source_history_count": 6,
        "state_space": v16x.COARSE_ARM,
        "start_families": list(START_FAMILIES),
        "chain_seed_families": list(CHAIN_SEED_FAMILIES),
        "proposal": "exact_length_residual_cycle_enumerator",
        "proposal_target_dependency": "none",
        "exact_length_choices": list(EXACT_LENGTH_CHOICES),
        "maximum_cycle_length": MAX_CYCLE_LENGTH,
        "constructor_rule": "enumerate_all_simple_residual_cycles_from_sampled_selected_edge_and_length",
        "proposal_auxiliary_pairing": "same_exact_length_and_reverse_ordered_added_edges",
        "stationary_target_scope": "uniform_per_residual_proposal_connected_component",
        "metropolis_ratio": "min(1,q_reverse_auxiliary/q_forward_auxiliary)",
        "laziness_probability": "1/2",
        "total_steps": TOTAL_STEPS,
        "representation_steps": REPRESENTATION_STEPS,
        "witness_attempts_per_length": WITNESS_ATTEMPTS_PER_LENGTH,
        "minimum_valid_proposals_per_chain": MIN_VALID_PROPOSALS_PER_CHAIN,
        "minimum_accepted_cycles_per_chain": MIN_ACCEPTED_CYCLES_PER_CHAIN,
        "minimum_accepted_long_cycles_per_chain": MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN,
        "minimum_unique_states_per_chain": MIN_UNIQUE_STATES_PER_CHAIN,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "minimum_paired_valid_improvements": MIN_PAIRED_VALID_IMPROVEMENTS,
        "minimum_median_valid_proposal_ratio": MIN_MEDIAN_VALID_PROPOSAL_RATIO,
        "comparison_baseline": "matched_v17a_chain_cell",
        "design_calibration_disclosure": (
            "before preregistration, effect-blind mechanics pilots rejected an exhaustive "
            "depth-eight completion oracle and a naive per-cycle integrity check on runtime; "
            "the exact length-2-to-4 enumerator retained all previously declared movement "
            "thresholds and inspected no source spectrum or observed effect"
        ),
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "no_early_stop": True,
        "not_claimed": [
            "global_irreducibility", "mixing", "global_uniform_sampling",
            "start_seed_time_stability", "canonical_physical_measure", "spectrum_effect",
            "energy", "temperature", "dimension", "Lorentz_symmetry", "spacetime",
            "particles", "Bell_correlation", "entanglement", "universe_model",
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
        "proposal": "exact_length_residual_cycle_enumerator",
        "exact_length_choices": ";".join(str(value) for value in EXACT_LENGTH_CHOICES),
        "maximum_cycle_length": MAX_CYCLE_LENGTH,
        "total_steps": TOTAL_STEPS,
        "representation_steps": REPRESENTATION_STEPS,
        "minimum_valid_proposals_per_chain": MIN_VALID_PROPOSALS_PER_CHAIN,
        "minimum_accepted_cycles_per_chain": MIN_ACCEPTED_CYCLES_PER_CHAIN,
        "minimum_accepted_long_cycles_per_chain": MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN,
        "minimum_unique_states_per_chain": MIN_UNIQUE_STATES_PER_CHAIN,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "minimum_paired_valid_improvements": MIN_PAIRED_VALID_IMPROVEMENTS,
        "minimum_median_valid_proposal_ratio": MIN_MEDIAN_VALID_PROPOSAL_RATIO,
        "design_pilot_allowed": 1,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v17ap.verify_outputs()
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v17b] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    expected = {key: str(value) for key, value in preregistration_row().items()}
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v17b preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v17b source chain changed")


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    result = []
    for source, metadata in v16x.load_runs():
        result.append((v16i.RunDAG(
            stage="v17b",
            target_nodes=source.target_nodes,
            growth_seed=source.growth_seed,
            run_offset=source.run_offset,
            arm=source.arm,
            run_seed=source.run_seed,
            predecessors=source.predecessors,
            depths=source.depths,
            indegrees=source.indegrees,
        ), metadata))
    return result


def raw_continuations(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    by_parent: Mapping[int, Tuple[Edge, ...]],
    remove: Tuple[Edge, ...],
) -> Tuple[Edge, ...]:
    current_slot = kernel.space.slot_by_edge[remove[-1]]
    current_child = current_slot[0]
    used_parents = {edge[0] for edge in remove}
    used_slots = {kernel.space.slot_by_edge[edge] for edge in remove}
    choices = []
    for parent in kernel.candidate_parents_by_slot.get(current_slot, ()):
        if parent in used_parents or (parent, current_child) in selected:
            continue
        for edge in by_parent.get(parent, ()):
            if kernel.space.slot_by_edge[edge] not in used_slots:
                choices.append(edge)
    return tuple(sorted(choices))


def close_proposal(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    remove: Tuple[Edge, ...],
) -> CycleProposal | None:
    if len(remove) < 2:
        return None
    current_slot = kernel.space.slot_by_edge[remove[-1]]
    closure = (remove[0][0], current_slot[0])
    if closure in selected or kernel.space.slot_by_edge.get(closure) != current_slot:
        return None
    adds = v17a.derive_adds(kernel, remove)
    if adds is None or set(adds) & selected:
        return None
    # A cyclic parent permutation preserves parent and slot demands by
    # construction. Full assignment integrity is checked once after sampling.
    return CycleProposal(remove, adds)


def residual_cycle_sequences(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    first: Edge,
    cycle_length: int,
) -> Tuple[Tuple[Edge, ...], ...]:
    if cycle_length not in EXACT_LENGTH_CHOICES or first not in selected:
        return ()
    by_parent = v17a.selected_by_parent(selected)
    completed: List[Tuple[Edge, ...]] = []

    def visit(remove: Tuple[Edge, ...]) -> None:
        if len(remove) == cycle_length:
            if close_proposal(kernel, selected, remove) is not None:
                completed.append(remove)
            return
        for edge in raw_continuations(
            kernel, selected, by_parent, remove
        ):
            visit(remove + (edge,))

    visit((first,))
    return tuple(completed)


def path_probability(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    remove: Sequence[Edge],
) -> ResidualAuxiliary | None:
    ordered_remove = tuple(remove)
    cycle_length = len(ordered_remove)
    if cycle_length not in EXACT_LENGTH_CHOICES:
        return None
    if len(set(ordered_remove)) != len(ordered_remove):
        return None
    if not set(ordered_remove).issubset(selected):
        return None
    parents = [edge[0] for edge in ordered_remove]
    slots = [kernel.space.slot_by_edge[edge] for edge in ordered_remove]
    if len(set(parents)) != len(parents) or len(set(slots)) != len(slots):
        return None
    ordered_selected = tuple(sorted(selected))
    if not ordered_selected:
        return None
    cycles = residual_cycle_sequences(
        kernel, selected, ordered_remove[0], cycle_length
    )
    if ordered_remove not in cycles:
        return None
    probability = Fraction(1, len(EXACT_LENGTH_CHOICES))
    probability *= Fraction(1, len(ordered_selected))
    probability *= Fraction(1, len(cycles))
    proposal = close_proposal(kernel, selected, ordered_remove)
    if proposal is None:
        return None
    return ResidualAuxiliary(probability, proposal, cycle_length, len(cycles))


def propose_cycle(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    rng: random.Random,
    *,
    forced_length: int | None = None,
) -> ResidualAuxiliary | None:
    cycle_length = forced_length
    if cycle_length is None:
        cycle_length = EXACT_LENGTH_CHOICES[
            rng.randrange(len(EXACT_LENGTH_CHOICES))
        ]
    if cycle_length not in EXACT_LENGTH_CHOICES:
        raise ValueError("forced cycle length outside frozen choices")
    ordered_selected = tuple(sorted(selected))
    if not ordered_selected:
        return None
    first = ordered_selected[rng.randrange(len(ordered_selected))]
    cycles = residual_cycle_sequences(kernel, selected, first, cycle_length)
    if not cycles:
        return None
    remove = cycles[rng.randrange(len(cycles))]
    return path_probability(kernel, selected, remove)


def chain_seed(dag: v16i.RunDAG, start_family: str, seed_family: str) -> int:
    return v16i.stable_seed("v17b", "chain", start_family, seed_family, *dag.key)


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
        auxiliary: ResidualAuxiliary | None = None
        reverse_auxiliary: ResidualAuxiliary | None = None
        acceptance: Fraction | None = None
        accepted = False
        before_digest = v16x.edge_digest(selected)

        if rng.getrandbits(1):
            counts["nonlazy_steps"] += 1
            auxiliary = propose_cycle(kernel, selected, rng)
            if auxiliary is None:
                event = "no_bounded_residual_completion"
                counts["proposal_dead_end"] += 1
            else:
                proposed = v17a.apply_proposal(
                    kernel.space, selected, auxiliary.proposal
                )
                reverse_auxiliary = path_probability(
                    kernel,
                    proposed,
                    v17a.reverse_remove_sequence(auxiliary.proposal),
                )
                counts["valid_proposals"] += 1
                if reverse_auxiliary is None:
                    event = "reverse_unsupported"
                    counts["reverse_unsupported"] += 1
                else:
                    recovered = v17a.apply_proposal(
                        kernel.space, proposed, reverse_auxiliary.proposal
                    )
                    if recovered != selected:
                        raise ValueError("reverse residual auxiliary did not recover state")
                    counts["reverse_supported"] += 1
                    acceptance = min(
                        Fraction(1),
                        reverse_auxiliary.probability / auxiliary.probability,
                    )
                    if v17a.exact_accept(rng, acceptance):
                        selected = proposed
                        accepted = True
                        event = "accepted_cycle"
                        counts["accepted_cycles"] += 1
                        cycle_length = len(auxiliary.proposal.remove)
                        accepted_lengths[cycle_length] += 1
                        if cycle_length >= 3:
                            counts["accepted_long_cycles"] += 1
                        visited.add(v16x.edge_digest(selected))
                    else:
                        event = "metropolis_reject"
                        counts["metropolis_rejects"] += 1
        else:
            counts["lazy_stays"] += 1

        proposal = auxiliary.proposal if auxiliary else None
        after_digest = v16x.edge_digest(selected)
        trace.append({
            **dag.prefix,
            "start_family": start_family,
            "chain_seed_family": seed_family,
            "chain_seed": seed,
            "step": step,
            "event": event,
            "cycle_length_choice": auxiliary.cycle_length if auxiliary else 0,
            "cycle_length": len(proposal.remove) if proposal else 0,
            "proposal_sha256": v17a.proposal_digest(proposal) if proposal else "",
            "cycle_count_for_start": auxiliary.cycle_count_for_start if auxiliary else 0,
            "remove_edges_json": json.dumps(proposal.remove, separators=(",", ":")) if proposal else "[]",
            "add_edges_json": json.dumps(proposal.add, separators=(",", ":")) if proposal else "[]",
            "q_forward_numerator": auxiliary.probability.numerator if auxiliary else 0,
            "q_forward_denominator": auxiliary.probability.denominator if auxiliary else 0,
            "q_reverse_numerator": reverse_auxiliary.probability.numerator if reverse_auxiliary else 0,
            "q_reverse_denominator": reverse_auxiliary.probability.denominator if reverse_auxiliary else 0,
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
        "accepted_length_counts_json": json.dumps(
            dict(sorted(accepted_lengths.items())), separators=(",", ":")
        ),
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
        "cycle_length_choice": row["cycle_length_choice"],
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
    rows = []
    for cycle_length in EXACT_LENGTH_CHOICES:
        rng = random.Random(v16i.stable_seed(
            "v17b", "reversibility", start_family, cycle_length, *dag.key
        ))
        witness = None
        attempts = 0
        while witness is None and attempts < WITNESS_ATTEMPTS_PER_LENGTH:
            attempts += 1
            witness = propose_cycle(
                kernel, start, rng, forced_length=cycle_length
            )
        if witness is None:
            rows.append({
                **dag.prefix,
                "start_family": start_family,
                "cycle_length_choice": cycle_length,
                "cycle_length": 0,
                "attempts": attempts,
                "proposal_sha256": "",
                "q_forward_numerator": 0,
                "q_forward_denominator": 0,
                "q_reverse_numerator": 0,
                "q_reverse_denominator": 0,
                "reverse_support_pass": 0,
                "forward_integrity_pass": 0,
                "reverse_recovery_pass": 0,
                "pathwise_detailed_balance_pass": 0,
            })
            continue
        proposed = v17a.apply_proposal(kernel.space, start, witness.proposal)
        reverse = path_probability(
            kernel,
            proposed,
            v17a.reverse_remove_sequence(witness.proposal),
        )
        if reverse is None:
            q_reverse = Fraction(0)
            reverse_recovery = False
            balance = False
        else:
            q_reverse = reverse.probability
            reverse_recovery = v17a.apply_proposal(
                kernel.space, proposed, reverse.proposal
            ) == start
            forward_acceptance = min(
                Fraction(1), q_reverse / witness.probability
            )
            reverse_acceptance = min(
                Fraction(1), witness.probability / q_reverse
            )
            balance = (
                Fraction(1, 2) * witness.probability * forward_acceptance
                == Fraction(1, 2) * q_reverse * reverse_acceptance
            )
        rows.append({
            **dag.prefix,
            "start_family": start_family,
            "cycle_length_choice": cycle_length,
            "cycle_length": len(witness.proposal.remove),
            "attempts": attempts,
            "proposal_sha256": v17a.proposal_digest(witness.proposal),
            "q_forward_numerator": witness.probability.numerator,
            "q_forward_denominator": witness.probability.denominator,
            "q_reverse_numerator": q_reverse.numerator,
            "q_reverse_denominator": q_reverse.denominator,
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
    def execute(target_space: v16x.StateSpace, target_start: frozenset[Edge]) -> ChainResult:
        return run_chain(
            dag,
            v17a.build_kernel(target_space),
            target_start,
            start_family,
            "representation_seed",
            total_steps=REPRESENTATION_STEPS,
        )

    original = execute(space, start)
    replay = execute(space, start)
    reversed_space = v16x.StateSpace(
        arm=space.arm,
        candidates=tuple(reversed(space.candidates)),
        source_edges=space.source_edges,
        slot_by_edge=space.slot_by_edge,
        parent_demands=space.parent_demands,
        slot_demands=space.slot_demands,
        edge_count=space.edge_count,
    )
    reordered = execute(reversed_space, start)
    relabeled_metadata = v16x.v16w.relabel_metadata(
        metadata,
        v16i.stable_seed("v17b", "semantic_relabel", start_family, *dag.key),
    )
    relabeled_space = v16x.build_state_space(dag, relabeled_metadata, v16x.COARSE_ARM)
    relabeled = execute(relabeled_space, start)
    candidate_set_pass = set(space.candidates) == set(relabeled_space.candidates)
    replay_pass = original.final == replay.final and original.transition_digest == replay.transition_digest
    order_pass = original.final == reordered.final and original.transition_digest == reordered.transition_digest
    relabel_pass = original.final == relabeled.final and original.transition_digest == relabeled.transition_digest
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
        "representation_pass": int(all((candidate_set_pass, replay_pass, order_pass, relabel_pass))),
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


def paired_improvement_rows(
    transitions: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    baseline = {
        (
            int(row["growth_seed"]),
            int(row["run_offset"]),
            row["start_family"],
            row["chain_seed_family"],
        ): row
        for row in v16i.read_csv(v17a.TRANSITION_SUMMARY)
    }
    rows = []
    for row in transitions:
        key = (
            int(row["growth_seed"]),
            int(row["run_offset"]),
            str(row["start_family"]),
            str(row["chain_seed_family"]),
        )
        old = baseline[key]
        old_valid = int(old["valid_proposals"])
        new_valid = int(row["valid_proposals"])
        old_change = float(old["final_start_changed_edge_fraction"])
        new_change = float(row["final_start_changed_edge_fraction"])
        rows.append({
            "stage": "v17b",
            "growth_seed": key[0],
            "run_offset": key[1],
            "start_family": key[2],
            "chain_seed_family": key[3],
            "v17a_valid_proposals": old_valid,
            "v17b_valid_proposals": new_valid,
            "valid_proposal_ratio": new_valid / old_valid,
            "valid_proposal_improved": int(new_valid > old_valid),
            "v17a_final_start_changed_edge_fraction": old_change,
            "v17b_final_start_changed_edge_fraction": new_change,
            "final_displacement_improved": int(new_change > old_change),
        })
    return rows


def markdown_table(
    rows: Sequence[Mapping[str, Any]], fields: Sequence[str]
) -> List[str]:
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
    gates: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    transitions: Sequence[Mapping[str, Any]],
    paired: Sequence[Mapping[str, Any]],
) -> None:
    minimum_valid = min(int(row["valid_proposals"]) for row in transitions)
    minimum_accepted = min(int(row["accepted_cycles"]) for row in transitions)
    minimum_long = min(int(row["accepted_long_cycles"]) for row in transitions)
    minimum_change = min(float(row["final_start_changed_edge_fraction"]) for row in transitions)
    maximum_seconds = max(float(row["elapsed_seconds"]) for row in transitions)
    median_ratio = statistics.median(float(row["valid_proposal_ratio"]) for row in paired)
    positive_improvements = sum(int(row["valid_proposal_improved"]) for row in paired)
    report = [
        "# v17b residual cycle constructor gate",
        "",
        f"Status: `{overall}`.",
        "",
        "## Method",
        "",
        "The proposal is target-independent and effect-blind. It samples an exact cycle length from 2, 3 or 4 and one selected start edge, enumerates every simple residual alternating cycle of that length from the start, then samples one uniformly. The selected cycle is a distinguished auxiliary; the reverse uses the same exact length and reversed ordered added edges with an exact lazy Metropolis ratio.",
        "",
        "## Source qualification",
        "",
        *markdown_table(summaries, (
            "growth_seed", "run_offset", "representation_passes",
            "reversibility_passes", "movement_passes", "minimum_valid_proposals",
            "minimum_accepted_cycles", "minimum_final_start_changed_edge_fraction",
            "maximum_chain_seconds", "source_qualification_pass",
        )),
        "",
        "## Gates",
        "",
        *markdown_table(gates, ("gate", "status", "observed", "required", "decision")),
        "",
        "## Finite movement and baseline comparison",
        "",
        f"Across 24 chains, minimum valid proposals were `{minimum_valid}`, minimum accepted cycles `{minimum_accepted}`, minimum accepted length>=3 cycles `{minimum_long}`, minimum final displacement `{minimum_change:.6f}`, and maximum runtime `{maximum_seconds:.6f}` seconds.",
        "",
        f"Matched against v17a, `{positive_improvements}/24` cells increased valid-proposal count and the median ratio was `{median_ratio:.6f}`. This comparison diagnoses constructor efficiency; it does not establish convergence or mixing.",
        "",
        "## Interpretation boundary",
        "",
        "A passing residual constructor would qualify only finite representation, reverse-support, pathwise-balance and movement checks on six reused spaces. It would not prove global irreducibility, stationarity from arbitrary starts, mixing time, a canonical probability law, the v16s source effect, Bell correlations, entanglement, Lorentz symmetry, spacetime or a universe model.",
        "",
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    INTERPRETATION.write_text(
        "# v17b interpretation audit\n\n"
        f"Frozen status is `{overall}`. The residual-cycle enumerator is an algorithmic proposal mechanism, not emergent physics. "
        "Pathwise balance applies to tested distinguished auxiliaries inside proposal-connected components. "
        "Movement is finite-budget displacement, not convergence, mixing, global support, spectrum transfer, Bell nonlocality or entanglement.\n",
        encoding="utf-8",
    )
    if overall == "v17b_residual_cycle_constructor_qualified":
        next_text = (
            "Proceed to an effect-blind start/seed/time stability gate on the same six spaces. "
            "Freeze longer chains, both starts, independent seeds, early/late windows and component-overlap diagnostics. "
            "Do not inspect the source spectrum until that stability gate passes."
        )
        recommendation = "Proceed to effect-blind finite stability; keep the spectrum closed."
    else:
        next_text = (
            "Stop before stability and source-spectrum tests. Diagnose the first failed constructor layer without relaxing the frozen thresholds. "
            "If valid yield improves but displacement fails, investigate cycle-length and acceptance structure rather than merely extending the chain."
        )
        recommendation = "Stop and diagnose the first failed residual-constructor layer."
    NEXT_DIRECTION.write_text(
        f"# v17b next direction\n\nFormal status: `{overall}`.\n\n{next_text}\n",
        encoding="utf-8",
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.17b\n\n"
        f"- status: `{overall}`\n"
        f"- next: {recommendation}\n"
        "- claim ceiling: finite residual-proposal qualification, not global sampling or physics\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf v0.17b for ikke-spesialister\n\n"
        "V17a provde aa bygge en lukket flyttesti ved aa gaa fremover og haape at den traff tilbake. V17b bruker i stedet et restgraf-kart og beholder bare steg som fortsatt har en kort, gyldig vei hjem.\n\n"
        f"Statusen er `{overall}`. Selv en bestaa-status betyr bare at denne flytteregelen virker bedre i en avgrenset simulering. Den beviser ikke at alle tilstander kan naas, at kjeden er blandet, eller at grafen viser kvantekorrelasjon.\n",
        encoding="utf-8",
    )


def run() -> None:
    verify_frozen_sources()
    frozen_digests = v16z.frozen_start_digests()
    traces: List[Dict[str, Any]] = []
    reversibility: List[Dict[str, Any]] = []
    representations: List[Dict[str, Any]] = []
    transitions: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []

    for run_index, (dag, metadata) in enumerate(load_runs(), start=1):
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        kernel = v17a.build_kernel(space)
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
                traces.extend(result.trace)
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
            reversibility_passes == 6,
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
            f"[v17b] sources={run_index}/6 representation={representation_passes}/2 "
            f"balance={reversibility_passes}/6 movement={movement_passes}/4"
        )

    paired = paired_improvement_rows(transitions)
    calls = implementation_call_counts()
    exclusion_pass = (
        calls == {"spectrum_calls": 0, "effect_metric_calls": 0}
        and all(int(row["source_spectrum_computed"]) == 0 for row in traces)
        and all(int(row["observed_effect_computed"]) == 0 for row in traces)
    )
    digest_count = sum(int(row["frozen_start_digest_passes"]) for row in summaries)
    representation_count = sum(int(row["representation_pass"]) for row in representations)
    reverse_count = sum(int(row["reverse_support_pass"]) for row in reversibility)
    balance_count = sum(int(row["pathwise_detailed_balance_pass"]) for row in reversibility)
    movement_count = sum(int(row["movement_pass"]) for row in transitions)
    resource_count = sum(int(row["resource_pass"]) for row in transitions)
    valid_improvements = sum(int(row["valid_proposal_improved"]) for row in paired)
    median_valid_ratio = statistics.median(float(row["valid_proposal_ratio"]) for row in paired)
    improvement_pass = (
        valid_improvements >= MIN_PAIRED_VALID_IMPROVEMENTS
        and median_valid_ratio >= MIN_MEDIAN_VALID_PROPOSAL_RATIO
    )

    if not exclusion_pass or digest_count != 12:
        overall = "v17b_instrumentation_failed"
    elif representation_count != 12:
        overall = "v17b_representation_not_qualified"
    elif reverse_count != 36 or balance_count != 36:
        overall = "v17b_reversibility_not_qualified"
    elif not improvement_pass:
        overall = "v17b_residual_constructor_improvement_not_qualified"
    elif movement_count != 24:
        overall = "v17b_finite_movement_not_qualified"
    elif resource_count != 24:
        overall = "v17b_resource_not_qualified"
    else:
        overall = "v17b_residual_cycle_constructor_qualified"

    gates = [
        {"gate": "effect_blind_integrity", "status": "pass" if exclusion_pass else "fail", "observed": f"spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}", "required": "0;0", "decision": "continue" if exclusion_pass else "invalidate"},
        {"gate": "frozen_start_replay", "status": "pass" if digest_count == 12 else "fail", "observed": f"{digest_count}/12", "required": "12/12", "decision": "continue" if digest_count == 12 else "invalidate"},
        {"gate": "representation_covariance", "status": "pass" if representation_count == 12 else "fail", "observed": f"{representation_count}/12", "required": "12/12", "decision": "continue" if representation_count == 12 else "repair_representation"},
        {"gate": "exact_reverse_support", "status": "pass" if reverse_count == 36 else "fail", "observed": f"{reverse_count}/36", "required": "36/36", "decision": "continue" if reverse_count == 36 else "repair_constructor"},
        {"gate": "pathwise_detailed_balance", "status": "pass" if balance_count == 36 else "fail", "observed": f"{balance_count}/36", "required": "36/36", "decision": "continue" if balance_count == 36 else "repair_probability"},
        {"gate": "paired_v17a_valid_yield", "status": "pass" if improvement_pass else "fail", "observed": f"improved={valid_improvements}/24;median_ratio={median_valid_ratio:.6f}", "required": f"{MIN_PAIRED_VALID_IMPROVEMENTS}/24;>={MIN_MEDIAN_VALID_PROPOSAL_RATIO}", "decision": "continue" if improvement_pass else "retire_or_redesign"},
        {"gate": "finite_movement", "status": "pass" if movement_count == 24 else "fail", "observed": f"{movement_count}/24", "required": "24/24", "decision": "continue" if movement_count == 24 else "diagnose_first_failed_movement_layer"},
        {"gate": "resource_bound", "status": "pass" if resource_count == 24 else "fail", "observed": f"{resource_count}/24", "required": "24/24", "decision": "continue" if resource_count == 24 else "optimize_before_stability"},
        {"gate": "v17b_overall", "status": overall, "observed": f"exclusion={int(exclusion_pass)};starts={digest_count}/12;representation={representation_count}/12;reverse={reverse_count}/36;balance={balance_count}/36;improvement={int(improvement_pass)};movement={movement_count}/24;resource={resource_count}/24", "required": "1;12/12;12/12;36/36;36/36;1;24/24;24/24", "decision": overall},
    ]
    claims = [
        {"claim_id": "C1", "claim": "The v17b proposal uses the current assignment and residual completion only, without a destination target or source effect.", "status": "supported" if exclusion_pass else "not_supported", "evidence": "specification and effect-exclusion audit", "scope_limit": "algorithmic target independence; not physical locality"},
        {"claim_id": "C2", "claim": "Every tested distinguished residual auxiliary has exact reverse support and pathwise detailed balance.", "status": "supported" if reverse_count == balance_count == 36 else "not_supported", "evidence": "v17b_pathwise_reversibility_audit.csv", "scope_limit": "36 finite witnesses on six reused spaces and two starts"},
        {"claim_id": "C3", "claim": "The residual constructor materially improves valid-proposal yield over matched v17a chains.", "status": "supported" if improvement_pass else "not_supported", "evidence": "v17b_paired_v17a_improvement.csv", "scope_limit": "finite paired cells; not a mixing-rate theorem"},
        {"claim_id": "C4", "claim": "The residual constructor qualifies finite movement under the unchanged v17a budget and floors.", "status": "supported" if movement_count == 24 else "not_supported", "evidence": "v17b_chain_transition_summary.csv", "scope_limit": "finite movement; not convergence or global support"},
        {"claim_id": "C5", "claim": "The v17b kernel is globally irreducible, mixed, or uniform over the full feasible space.", "status": "unsupported", "evidence": "none", "scope_limit": "target is component-uniform only"},
        {"claim_id": "C6", "claim": "The v16s spectrum contrast survives v17b or v17b exhibits Bell correlations.", "status": "not_tested", "evidence": "spectrum/effect calls prohibited; Bell observables absent", "scope_limit": "requires later qualified stability and separate Bell operationalization"},
    ]

    v16i.write_csv(PROPOSAL_TRACE, traces)
    v16i.write_csv(REVERSIBILITY_AUDIT, reversibility)
    v16i.write_csv(REPRESENTATION_AUDIT, representations)
    v16i.write_csv(TRANSITION_SUMMARY, transitions)
    v16i.write_csv(PAIRED_IMPROVEMENT, paired)
    v16i.write_csv(SOURCE_SUMMARY, summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    write_documents(overall, gates, summaries, transitions, paired)
    print(f"[v17b] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    trace = v16i.read_csv(PROPOSAL_TRACE)
    reversibility = v16i.read_csv(REVERSIBILITY_AUDIT)
    representations = v16i.read_csv(REPRESENTATION_AUDIT)
    transitions = v16i.read_csv(TRANSITION_SUMMARY)
    paired = v16i.read_csv(PAIRED_IMPROVEMENT)
    summaries = v16i.read_csv(SOURCE_SUMMARY)
    gates = v16i.read_csv(GATE_EVALUATION)
    claims = v16i.read_csv(CLAIM_LEDGER)
    if len(trace) != 24 * TOTAL_STEPS:
        raise ValueError("v17b trace row count failed")
    if len(reversibility) != 36 or len(representations) != 12:
        raise ValueError("v17b reversibility/representation row count failed")
    if len(transitions) != 24 or len(paired) != 24 or len(summaries) != 6:
        raise ValueError("v17b transition/comparison/source row count failed")
    if len(gates) != 9 or len(claims) != 6:
        raise ValueError("v17b gate/claim row count failed")
    if implementation_call_counts() != {"spectrum_calls": 0, "effect_metric_calls": 0}:
        raise ValueError("v17b effect exclusion failed")
    if any(int(row["source_spectrum_computed"]) for row in trace):
        raise ValueError("v17b trace contains source spectrum")
    if any(int(row["observed_effect_computed"]) for row in trace):
        raise ValueError("v17b trace contains observed effect")
    overall = next(row["status"] for row in gates if row["gate"] == "v17b_overall")
    allowed = {
        "v17b_instrumentation_failed",
        "v17b_representation_not_qualified",
        "v17b_reversibility_not_qualified",
        "v17b_residual_constructor_improvement_not_qualified",
        "v17b_finite_movement_not_qualified",
        "v17b_resource_not_qualified",
        "v17b_residual_cycle_constructor_qualified",
    }
    if overall not in allowed:
        raise ValueError("v17b overall status is unknown")
    for path in (REPORT, INTERPRETATION, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"v17b documentation missing: {path.name}")
    print(f"[v17b] output verification pass overall={overall}")


def self_test() -> None:
    role = ("test", ("resource",))
    slot_class = (role, 0, "witness")
    parents = (0, 1, 2, 3)
    children = (10, 11, 12, 13)
    candidates = tuple((parent, child) for parent in parents for child in children)
    source = frozenset(zip(parents, children))
    space = v16x.StateSpace(
        arm="test",
        candidates=candidates,
        source_edges=source,
        slot_by_edge={edge: (edge[1], slot_class) for edge in candidates},
        parent_demands={parent: 1 for parent in parents},
        slot_demands={(child, slot_class): 1 for child in children},
        edge_count=4,
    )
    kernel = v17a.build_kernel(space)
    for cycle_length in EXACT_LENGTH_CHOICES:
        rng = random.Random(1000 + cycle_length)
        witness = None
        for _ in range(64):
            witness = propose_cycle(
                kernel, source, rng, forced_length=cycle_length
            )
            if witness is not None:
                break
        if witness is None:
            raise AssertionError("v17b synthetic residual completion missing")
        proposed = v17a.apply_proposal(space, source, witness.proposal)
        reverse = path_probability(
            kernel,
            proposed,
            v17a.reverse_remove_sequence(witness.proposal),
        )
        if reverse is None:
            raise AssertionError("v17b synthetic reverse support missing")
        if v17a.apply_proposal(space, proposed, reverse.proposal) != source:
            raise AssertionError("v17b synthetic reverse recovery failed")
        forward_acceptance = min(Fraction(1), reverse.probability / witness.probability)
        reverse_acceptance = min(Fraction(1), witness.probability / reverse.probability)
        if Fraction(1, 2) * witness.probability * forward_acceptance != Fraction(1, 2) * reverse.probability * reverse_acceptance:
            raise AssertionError("v17b synthetic pathwise balance failed")
    if implementation_call_counts() != {"spectrum_calls": 0, "effect_metric_calls": 0}:
        raise AssertionError("v17b effect exclusion audit failed")
    print("[v17b] self-test pass")


def pilot() -> None:
    dag, metadata = load_runs()[0]
    space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
    result = run_chain(
        dag,
        v17a.build_kernel(space),
        space.source_edges,
        "source_assignment",
        "pilot_seed",
        total_steps=128,
    )
    print(json.dumps({
        "source": list(dag.key),
        "steps": 128,
        "valid_proposals": result.stats["valid_proposals"],
        "accepted_cycles": result.stats["accepted_cycles"],
        "accepted_long_cycles": result.stats["accepted_long_cycles"],
        "unique_state_count": result.stats["unique_state_count"],
        "final_start_changed_edge_fraction": result.stats["final_start_changed_edge_fraction"],
        "elapsed_seconds": result.stats["elapsed_seconds"],
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description="v17b residual cycle constructor gate")
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
