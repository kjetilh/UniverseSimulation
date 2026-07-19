#!/usr/bin/env python3
"""v17f qualification of a bounded-search length-5 cycle move.

The expanded kernel is a 50/50 mixture of the qualified v17c length-2-to-4
kernel and a new fixed length-5 auxiliary. The new auxiliary samples an
ordered batch of current edges, retains only first edges with a deterministic
bounded completion witness, and uses exact forward/reverse auxiliary
probabilities in a lazy Metropolis step. Source spectra and observed effects
remain prohibited.
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
import relational_universe_v17b_residual_cycle_constructor_gate as v17b
import relational_universe_v17c_exact_counter_runtime_qualification as v17c
import relational_universe_v17e_effect_blind_scale_response_gate as v17e


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

START_FAMILIES = v17c.START_FAMILIES
CHAIN_SEED_FAMILIES = ("move_seed_e", "move_seed_f")
OLD_LENGTH_CHOICES = (2, 3, 4)
NEW_CYCLE_LENGTH = 5
FIRST_BATCH_SIZE = 4
MAX_SEARCH_STATES_PER_GUIDE = 20_000
TOTAL_STEPS = 1024
REPRESENTATION_STEPS = 64
REVERSIBILITY_ATTEMPTS = 128
MIN_VALID_PROPOSALS_PER_CHAIN = 96
MIN_ACCEPTED_CYCLES_PER_CHAIN = 64
MIN_ACCEPTED_OLD_CYCLES_PER_CHAIN = 32
MIN_ACCEPTED_LENGTH5_CYCLES_PER_CHAIN = 4
MIN_UNIQUE_STATES_PER_CHAIN = 64
MIN_FINAL_START_CHANGE = 0.05
MAX_CHAIN_SECONDS = 120.0
DESIGN_PILOT_ATTEMPTS = 64

DESIGN_PILOT = DOC / "v17f_excluded_design_pilot.csv"
SOURCE_CHAIN = DOC / "v17f_source_chain.csv"
PRE_REGISTRATION = DOC / "v17f_pre_registration.csv"
PROPOSAL_TRACE = DOC / "v17f_proposal_trace.csv"
REVERSIBILITY_AUDIT = DOC / "v17f_pathwise_reversibility_audit.csv"
REPRESENTATION_AUDIT = DOC / "v17f_representation_audit.csv"
TRANSITION_SUMMARY = DOC / "v17f_chain_transition_summary.csv"
SOURCE_SUMMARY = DOC / "v17f_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v17f_gate_evaluation.csv"
GOAL_EVALUATION = DOC / "v17f_goal_evaluation.csv"
CLAIM_LEDGER = DOC / "v17f_claim_ledger.csv"
REPORT = DOC / "v17f_effect_blind_length5_move_qualification.md"
INTERPRETATION = DOC / "v17f_interpretation_audit.md"
NEXT_DIRECTION = DOC / "v17f_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_17f_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_17f.md"

Edge = v16x.Edge
Slot = v16x.Slot
CycleKernel = v17a.CycleKernel
CycleProposal = v17a.CycleProposal


@dataclass(frozen=True)
class Length5Auxiliary:
    probability: Fraction
    proposal: CycleProposal
    first_batch: Tuple[Edge, ...]
    eligible_first_count: int
    search_states: int
    search_budget_exhaustions: int


@dataclass(frozen=True)
class ExpandedAuxiliary:
    move_class: str
    probability: Fraction
    proposal: CycleProposal
    first_batch: Tuple[Edge, ...] = ()
    eligible_first_count: int = 0
    search_states: int = 0
    search_budget_exhaustions: int = 0


@dataclass
class ChainResult:
    final: frozenset[Edge]
    stats: MutableMapping[str, Any]
    trace: List[Dict[str, Any]]
    transition_digest: str


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    result = []
    for source, metadata in v17c.load_runs():
        result.append((v16i.RunDAG(
            stage="v17f",
            target_nodes=source.target_nodes,
            growth_seed=source.growth_seed,
            run_offset=source.run_offset,
            arm=source.arm,
            run_seed=source.run_seed,
            predecessors=source.predecessors,
            depths=source.depths,
            indegrees=source.indegrees,
        ), metadata))
    if len(result) != 6:
        raise ValueError("v17f requires six frozen source histories")
    return result


class CompletionGuide:
    """Deterministic bounded witness search for one distinguished first edge."""

    def __init__(
        self,
        kernel: CycleKernel,
        selected: frozenset[Edge],
        first: Edge,
        by_parent: Mapping[int, Tuple[Edge, ...]],
    ) -> None:
        self.kernel = kernel
        self.selected = selected
        self.first = first
        self.by_parent = by_parent
        self._raw_cache: Dict[Slot, Dict[int, Tuple[Edge, ...]]] = {}
        self._existence_cache: Dict[
            Tuple[Slot, frozenset[int], frozenset[Slot], int], bool
        ] = {}
        self.search_states = 0
        self.search_budget_exhaustions = 0

    def raw_map(
        self,
        current_slot: Slot,
        used_parents: frozenset[int],
        used_slots: frozenset[Slot],
    ) -> Dict[int, Tuple[Edge, ...]]:
        base = self._raw_cache.get(current_slot)
        if base is None:
            current_child = current_slot[0]
            base = {}
            for parent in self.kernel.candidate_parents_by_slot.get(current_slot, ()):
                if (parent, current_child) in self.selected:
                    continue
                edges = tuple(sorted(self.by_parent.get(parent, ())))
                if edges:
                    base[parent] = edges
            self._raw_cache[current_slot] = base
        result = {}
        for parent, edges in base.items():
            if parent in used_parents:
                continue
            available = tuple(
                edge for edge in edges
                if self.kernel.space.slot_by_edge[edge] not in used_slots
            )
            if available:
                result[parent] = available
        return result

    def closure_valid(self, current_slot: Slot) -> bool:
        closure = (self.first[0], current_slot[0])
        return (
            closure not in self.selected
            and self.kernel.space.slot_by_edge.get(closure) == current_slot
        )

    def has_completion(
        self,
        current_slot: Slot,
        used_parents: frozenset[int],
        used_slots: frozenset[Slot],
        depth: int,
    ) -> bool:
        key = (current_slot, used_parents, used_slots, depth)
        cached = self._existence_cache.get(key)
        if cached is not None:
            return cached
        if self.search_states >= MAX_SEARCH_STATES_PER_GUIDE:
            self.search_budget_exhaustions += 1
            self._existence_cache[key] = False
            return False
        self.search_states += 1
        if depth == NEW_CYCLE_LENGTH:
            result = self.closure_valid(current_slot)
        else:
            result = False
            raw = self.raw_map(current_slot, used_parents, used_slots)
            for parent in sorted(raw):
                for edge in raw[parent]:
                    slot = self.kernel.space.slot_by_edge[edge]
                    if self.has_completion(
                        slot,
                        used_parents | {parent},
                        used_slots | {slot},
                        depth + 1,
                    ):
                        result = True
                        break
                if result:
                    break
        self._existence_cache[key] = result
        return result

    def viable_edges(
        self,
        current_slot: Slot,
        used_parents: frozenset[int],
        used_slots: frozenset[Slot],
        depth: int,
        parent: int,
    ) -> Tuple[Edge, ...]:
        result = []
        for edge in self.raw_map(current_slot, used_parents, used_slots).get(parent, ()):
            slot = self.kernel.space.slot_by_edge[edge]
            if self.has_completion(
                slot,
                used_parents | {parent},
                used_slots | {slot},
                depth + 1,
            ):
                result.append(edge)
        return tuple(result)


def eligible_first_guides(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    batch: Sequence[Edge],
    by_parent: Mapping[int, Tuple[Edge, ...]],
) -> Dict[Edge, CompletionGuide]:
    result = {}
    for first in batch:
        guide = CompletionGuide(kernel, selected, first, by_parent)
        slot = kernel.space.slot_by_edge[first]
        if guide.has_completion(
            slot, frozenset({first[0]}), frozenset({slot}), 1
        ):
            result[first] = guide
    return result


def suffix_probability(
    guide: CompletionGuide,
    remove: Sequence[Edge],
) -> Fraction | None:
    ordered = tuple(remove)
    current_slot = guide.kernel.space.slot_by_edge[ordered[0]]
    used_parents = frozenset({ordered[0][0]})
    used_slots = frozenset({current_slot})
    probability = Fraction(1)
    for depth, edge in enumerate(ordered[1:], start=1):
        raw = guide.raw_map(current_slot, used_parents, used_slots)
        parents = tuple(sorted(raw))
        if edge[0] not in raw:
            return None
        viable = guide.viable_edges(
            current_slot, used_parents, used_slots, depth, edge[0]
        )
        if edge not in viable:
            return None
        probability *= Fraction(1, len(parents))
        probability *= Fraction(1, len(viable))
        current_slot = guide.kernel.space.slot_by_edge[edge]
        used_parents |= {edge[0]}
        used_slots |= {current_slot}
    return probability


def sample_suffix(
    guide: CompletionGuide,
    rng: random.Random,
) -> Tuple[Fraction, Tuple[Edge, ...]] | None:
    remove = [guide.first]
    current_slot = guide.kernel.space.slot_by_edge[guide.first]
    used_parents = frozenset({guide.first[0]})
    used_slots = frozenset({current_slot})
    probability = Fraction(1)
    while len(remove) < NEW_CYCLE_LENGTH:
        depth = len(remove)
        raw = guide.raw_map(current_slot, used_parents, used_slots)
        parents = tuple(sorted(raw))
        if not parents:
            return None
        parent = parents[rng.randrange(len(parents))]
        viable = guide.viable_edges(
            current_slot, used_parents, used_slots, depth, parent
        )
        probability *= Fraction(1, len(parents))
        if not viable:
            return None
        edge = viable[rng.randrange(len(viable))]
        probability *= Fraction(1, len(viable))
        remove.append(edge)
        current_slot = guide.kernel.space.slot_by_edge[edge]
        used_parents |= {parent}
        used_slots |= {current_slot}
    return probability, tuple(remove)


def length5_path_probability(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    remove: Sequence[Edge],
    first_batch: Sequence[Edge],
) -> Length5Auxiliary | None:
    ordered = tuple(remove)
    batch = tuple(first_batch)
    if (
        len(ordered) != NEW_CYCLE_LENGTH
        or len(set(ordered)) != NEW_CYCLE_LENGTH
        or not set(ordered).issubset(selected)
        or len(batch) != FIRST_BATCH_SIZE
        or len(set(batch)) != FIRST_BATCH_SIZE
        or not set(batch).issubset(selected)
    ):
        return None
    by_parent = v17a.selected_by_parent(selected)
    eligible = eligible_first_guides(kernel, selected, batch, by_parent)
    guide = eligible.get(ordered[0])
    if guide is None:
        return None
    suffix = suffix_probability(guide, ordered)
    proposal = v17b.close_proposal(kernel, selected, ordered)
    if suffix is None or proposal is None:
        return None
    probability = Fraction(1, math.perm(len(selected), FIRST_BATCH_SIZE))
    probability *= Fraction(1, len(eligible))
    probability *= suffix
    guides = tuple(eligible.values())
    return Length5Auxiliary(
        probability,
        proposal,
        batch,
        len(eligible),
        sum(item.search_states for item in guides),
        sum(item.search_budget_exhaustions for item in guides),
    )


def propose_length5(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    rng: random.Random,
) -> Length5Auxiliary | None:
    batch = tuple(rng.sample(tuple(sorted(selected)), FIRST_BATCH_SIZE))
    by_parent = v17a.selected_by_parent(selected)
    eligible = eligible_first_guides(kernel, selected, batch, by_parent)
    if not eligible:
        return None
    first_edges = tuple(edge for edge in batch if edge in eligible)
    first = first_edges[rng.randrange(len(first_edges))]
    guide = eligible[first]
    suffix = sample_suffix(guide, rng)
    if suffix is None:
        return None
    suffix_q, remove = suffix
    proposal = v17b.close_proposal(kernel, selected, remove)
    if proposal is None:
        raise AssertionError("v17f guided completion failed closure")
    probability = Fraction(1, math.perm(len(selected), FIRST_BATCH_SIZE))
    probability *= Fraction(1, len(eligible))
    probability *= suffix_q
    guides = tuple(eligible.values())
    return Length5Auxiliary(
        probability,
        proposal,
        batch,
        len(eligible),
        sum(item.search_states for item in guides),
        sum(item.search_budget_exhaustions for item in guides),
    )


def reverse_first_batch(auxiliary: Length5Auxiliary | ExpandedAuxiliary) -> Tuple[Edge, ...]:
    reverse_remove = v17a.reverse_remove_sequence(auxiliary.proposal)
    mapping = {
        old: new for old, new in zip(auxiliary.proposal.remove, reverse_remove)
    }
    return tuple(mapping.get(edge, edge) for edge in auxiliary.first_batch)


def propose_expanded(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    rng: random.Random,
) -> ExpandedAuxiliary | None:
    if rng.getrandbits(1):
        old = v17c.propose_cycle(kernel, selected, rng)
        if old is None:
            return None
        return ExpandedAuxiliary(
            "length_2_4",
            Fraction(1, 2) * old.probability,
            old.proposal,
        )
    new = propose_length5(kernel, selected, rng)
    if new is None:
        return None
    return ExpandedAuxiliary(
        "length_5_batch_guided",
        Fraction(1, 2) * new.probability,
        new.proposal,
        new.first_batch,
        new.eligible_first_count,
        new.search_states,
        new.search_budget_exhaustions,
    )


def reverse_expanded(
    kernel: CycleKernel,
    proposed: frozenset[Edge],
    auxiliary: ExpandedAuxiliary,
) -> ExpandedAuxiliary | None:
    reverse_remove = v17a.reverse_remove_sequence(auxiliary.proposal)
    if auxiliary.move_class == "length_2_4":
        reverse = v17c.path_probability(kernel, proposed, reverse_remove)
        if reverse is None:
            return None
        return ExpandedAuxiliary(
            "length_2_4",
            Fraction(1, 2) * reverse.probability,
            reverse.proposal,
        )
    reverse = length5_path_probability(
        kernel, proposed, reverse_remove, reverse_first_batch(auxiliary)
    )
    if reverse is None:
        return None
    return ExpandedAuxiliary(
        "length_5_batch_guided",
        Fraction(1, 2) * reverse.probability,
        reverse.proposal,
        reverse.first_batch,
        reverse.eligible_first_count,
        reverse.search_states,
        reverse.search_budget_exhaustions,
    )


def chain_seed(dag: v16i.RunDAG, start_family: str, seed_family: str) -> int:
    return v16i.stable_seed("v17f", "chain", start_family, seed_family, *dag.key)


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
    accepted_edge_work = 0
    started = time.monotonic()

    for step in range(1, total_steps + 1):
        event = "lazy_stay"
        auxiliary: ExpandedAuxiliary | None = None
        reverse: ExpandedAuxiliary | None = None
        acceptance: Fraction | None = None
        accepted = False
        before_digest = v16x.edge_digest(selected)

        if rng.getrandbits(1):
            counts["nonlazy_steps"] += 1
            auxiliary = propose_expanded(kernel, selected, rng)
            if auxiliary is None:
                event = "proposal_dead_end"
                counts["proposal_dead_end"] += 1
            else:
                counts[f"valid_{auxiliary.move_class}"] += 1
                counts["valid_proposals"] += 1
                proposed = v17a.apply_proposal(kernel.space, selected, auxiliary.proposal)
                reverse = reverse_expanded(kernel, proposed, auxiliary)
                if reverse is None:
                    event = "reverse_unsupported"
                    counts["reverse_unsupported"] += 1
                else:
                    recovered = v17a.apply_proposal(
                        kernel.space, proposed, reverse.proposal
                    )
                    if recovered != selected:
                        raise ValueError("v17f reverse auxiliary did not recover state")
                    counts["reverse_supported"] += 1
                    acceptance = min(
                        Fraction(1), reverse.probability / auxiliary.probability
                    )
                    if v17a.exact_accept(rng, acceptance):
                        selected = proposed
                        accepted = True
                        event = "accepted_cycle"
                        length = len(auxiliary.proposal.remove)
                        accepted_lengths[length] += 1
                        accepted_edge_work += length
                        counts["accepted_cycles"] += 1
                        counts[f"accepted_{auxiliary.move_class}"] += 1
                        visited.add(v16x.edge_digest(selected))
                    else:
                        event = "metropolis_reject"
                        counts["metropolis_rejects"] += 1
        else:
            counts["lazy_stays"] += 1

        proposal = auxiliary.proposal if auxiliary else None
        trace.append({
            **dag.prefix,
            "start_family": start_family,
            "chain_seed_family": seed_family,
            "chain_seed": seed,
            "step": step,
            "event": event,
            "move_class": auxiliary.move_class if auxiliary else "none",
            "cycle_length": len(proposal.remove) if proposal else 0,
            "proposal_sha256": v17a.proposal_digest(proposal) if proposal else "",
            "first_batch_json": json.dumps(auxiliary.first_batch, separators=(",", ":")) if auxiliary and auxiliary.first_batch else "[]",
            "eligible_first_count": auxiliary.eligible_first_count if auxiliary else 0,
            "search_states": auxiliary.search_states if auxiliary else 0,
            "search_budget_exhaustions": auxiliary.search_budget_exhaustions if auxiliary else 0,
            "old_one_step_length_support": int(
                bool(proposal) and len(proposal.remove) in OLD_LENGTH_CHOICES
            ),
            "remove_edges_json": json.dumps(proposal.remove, separators=(",", ":")) if proposal else "[]",
            "add_edges_json": json.dumps(proposal.add, separators=(",", ":")) if proposal else "[]",
            "q_forward_numerator": auxiliary.probability.numerator if auxiliary else 0,
            "q_forward_denominator": auxiliary.probability.denominator if auxiliary else 0,
            "q_reverse_numerator": reverse.probability.numerator if reverse else 0,
            "q_reverse_denominator": reverse.probability.denominator if reverse else 0,
            "acceptance_numerator": acceptance.numerator if acceptance else 0,
            "acceptance_denominator": acceptance.denominator if acceptance else 0,
            "accepted": int(accepted),
            "state_before_sha256": before_digest,
            "state_after_sha256": v16x.edge_digest(selected),
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })

    elapsed = time.monotonic() - started
    final_change = 1.0 - len(selected & start) / kernel.space.edge_count
    movement_pass = all((
        counts["valid_proposals"] >= MIN_VALID_PROPOSALS_PER_CHAIN,
        counts["accepted_cycles"] >= MIN_ACCEPTED_CYCLES_PER_CHAIN,
        counts["accepted_length_2_4"] >= MIN_ACCEPTED_OLD_CYCLES_PER_CHAIN,
        counts["accepted_length_5_batch_guided"] >= MIN_ACCEPTED_LENGTH5_CYCLES_PER_CHAIN,
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
        "valid_old_cycles": counts["valid_length_2_4"],
        "valid_length5_cycles": counts["valid_length_5_batch_guided"],
        "reverse_supported": counts["reverse_supported"],
        "reverse_unsupported": counts["reverse_unsupported"],
        "accepted_cycles": counts["accepted_cycles"],
        "accepted_old_cycles": counts["accepted_length_2_4"],
        "accepted_length5_cycles": counts["accepted_length_5_batch_guided"],
        "accepted_edge_work": accepted_edge_work,
        "metropolis_rejects": counts["metropolis_rejects"],
        "accepted_length_counts_json": json.dumps(
            dict(sorted(accepted_lengths.items())), separators=(",", ":")
        ),
        "unique_state_count": len(visited),
        "final_start_changed_edge_fraction": final_change,
        "elapsed_seconds": elapsed,
        "minimum_valid_proposals": MIN_VALID_PROPOSALS_PER_CHAIN,
        "minimum_accepted_cycles": MIN_ACCEPTED_CYCLES_PER_CHAIN,
        "minimum_accepted_old_cycles": MIN_ACCEPTED_OLD_CYCLES_PER_CHAIN,
        "minimum_accepted_length5_cycles": MIN_ACCEPTED_LENGTH5_CYCLES_PER_CHAIN,
        "minimum_unique_states": MIN_UNIQUE_STATES_PER_CHAIN,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "final_assignment_integrity_pass": int(
            v16x.assignment_integrity(kernel.space, selected)
        ),
        "resource_pass": int(elapsed <= MAX_CHAIN_SECONDS),
        "movement_pass": int(movement_pass),
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }
    digest_payload = [{
        "event": row["event"],
        "move_class": row["move_class"],
        "cycle_length": row["cycle_length"],
        "proposal": row["proposal_sha256"],
        "accepted": row["accepted"],
        "after": row["state_after_sha256"],
    } for row in trace]
    digest = hashlib.sha256(json.dumps(
        digest_payload, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()
    return ChainResult(selected, stats, trace, digest)


def run_design_pilot() -> None:
    rows = []
    dag, metadata = load_runs()[0]
    space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
    kernel = v17a.build_kernel(space)
    starts = {
        "source_assignment": space.source_edges,
        "v16x_random_cost_a0": v16z.random_cost_start(dag, space),
    }
    for start_family, start in starts.items():
        selected = start
        rng = random.Random(v16i.stable_seed(
            "v17f", "excluded_design_pilot", start_family, *dag.key
        ))
        counts = Counter()
        proposal_seconds = []
        eligible_counts = []
        search_states = 0
        search_exhaustions = 0
        started = time.monotonic()
        for _ in range(DESIGN_PILOT_ATTEMPTS):
            proposal_started = time.monotonic()
            auxiliary = propose_length5(kernel, selected, rng)
            proposal_seconds.append(time.monotonic() - proposal_started)
            if auxiliary is None:
                counts["dead_end"] += 1
                continue
            counts["valid"] += 1
            eligible_counts.append(auxiliary.eligible_first_count)
            search_states += auxiliary.search_states
            search_exhaustions += auxiliary.search_budget_exhaustions
            proposed = v17a.apply_proposal(space, selected, auxiliary.proposal)
            reverse = length5_path_probability(
                kernel,
                proposed,
                v17a.reverse_remove_sequence(auxiliary.proposal),
                reverse_first_batch(auxiliary),
            )
            if reverse is None:
                counts["reverse_unsupported"] += 1
                continue
            counts["reverse_supported"] += 1
            acceptance = min(Fraction(1), reverse.probability / auxiliary.probability)
            if v17a.exact_accept(rng, acceptance):
                selected = proposed
                counts["accepted"] += 1
        rows.append({
            **dag.prefix,
            "pilot_excluded_from_formal_gate": 1,
            "start_family": start_family,
            "cycle_length": NEW_CYCLE_LENGTH,
            "first_batch_size": FIRST_BATCH_SIZE,
            "maximum_search_states_per_guide": MAX_SEARCH_STATES_PER_GUIDE,
            "attempts": DESIGN_PILOT_ATTEMPTS,
            "valid_proposals": counts["valid"],
            "accepted_cycles": counts["accepted"],
            "reverse_unsupported": counts["reverse_unsupported"],
            "minimum_eligible_first_count": min(eligible_counts) if eligible_counts else 0,
            "maximum_eligible_first_count": max(eligible_counts) if eligible_counts else 0,
            "search_states": search_states,
            "search_budget_exhaustions": search_exhaustions,
            "maximum_proposal_seconds": max(proposal_seconds),
            "elapsed_seconds": time.monotonic() - started,
            "final_start_changed_edge_fraction": 1.0 - len(selected & start) / space.edge_count,
            "final_endpoint_sha256": v16x.edge_digest(selected),
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })
    v16i.write_csv(DESIGN_PILOT, rows)
    print(f"[v17f] excluded design pilot rows={len(rows)}")


def design_pilot_disclosure() -> List[Dict[str, Any]]:
    if not DESIGN_PILOT.exists():
        raise ValueError("run --design-pilot before v17f preregistration")
    fields = (
        "growth_seed", "run_offset", "start_family", "attempts",
        "valid_proposals", "accepted_cycles", "reverse_unsupported",
        "maximum_proposal_seconds", "elapsed_seconds",
        "source_spectrum_computed", "observed_effect_computed",
    )
    return [
        {field: row[field] for field in fields}
        for row in v16i.read_csv(DESIGN_PILOT)
    ]


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v17a", "previous_length_2_8_failure", v17a.GATE_EVALUATION),
        ("v17b", "residual_constructor_repair", v17b.GATE_EVALUATION),
        ("v17c", "qualified_exact_counter", v17c.GATE_EVALUATION),
        ("v17c", "qualified_length_2_4_implementation", v17c.SCRIPT),
        ("v17e", "retired_scale_growth", v17e.GATE_EVALUATION),
        ("v17e", "move_class_decision", v17e.NEXT_DIRECTION),
        ("v17f", "excluded_effect_blind_design_pilot", DESIGN_PILOT),
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
        "gate": "v17f_effect_blind_length5_move_qualification",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_expanded_move_class_probability_representation_traversal_resource",
        "goal": {
            "baseline": "v17e retired further scale growth of exact cycles length 2-4",
            "target": (
                "12/12 length-5 reverse witnesses; 12/12 representation; "
                "24/24 finite movement and resource; >=4 accepted length-5 cycles per chain"
            ),
            "timeframe": "one frozen v17f round",
        },
        "state_space": v16x.COARSE_ARM,
        "source_history_count": 6,
        "start_families": list(START_FAMILIES),
        "chain_seed_families": list(CHAIN_SEED_FAMILIES),
        "proposal_law": "half_v17c_length_2_4_half_bounded_search_batch_guided_length_5",
        "old_length_choices": list(OLD_LENGTH_CHOICES),
        "new_cycle_length": NEW_CYCLE_LENGTH,
        "first_batch_size": FIRST_BATCH_SIZE,
        "first_batch_law": "uniform_ordered_sample_without_replacement",
        "first_choice_law": "uniform_among_batch_edges_with_bounded_completion_witness",
        "suffix_law": "uniform_raw_parent_then_uniform_bounded_witness_edge_or_dead_end",
        "maximum_search_states_per_guide": MAX_SEARCH_STATES_PER_GUIDE,
        "proposal_auxiliary_pairing": "reverse_cycle_plus_bijectively_mapped_ordered_first_batch",
        "stationary_target_scope": "uniform_per_expanded_proposal_connected_component",
        "metropolis_ratio": "min(1,q_reverse_auxiliary/q_forward_auxiliary)",
        "laziness_probability": "1/2",
        "total_steps": TOTAL_STEPS,
        "representation_steps": REPRESENTATION_STEPS,
        "reversibility_attempts": REVERSIBILITY_ATTEMPTS,
        "minimum_valid_proposals_per_chain": MIN_VALID_PROPOSALS_PER_CHAIN,
        "minimum_accepted_cycles_per_chain": MIN_ACCEPTED_CYCLES_PER_CHAIN,
        "minimum_accepted_old_cycles_per_chain": MIN_ACCEPTED_OLD_CYCLES_PER_CHAIN,
        "minimum_accepted_length5_cycles_per_chain": MIN_ACCEPTED_LENGTH5_CYCLES_PER_CHAIN,
        "minimum_unique_states_per_chain": MIN_UNIQUE_STATES_PER_CHAIN,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "design_pilot_disclosure": design_pilot_disclosure(),
        "required_frozen_start_replays": 12,
        "required_reversibility_witnesses": 12,
        "required_novel_one_step_witnesses": 12,
        "required_representation_passes": 12,
        "required_movement_passes": 24,
        "required_resource_passes": 24,
        "failure_decision": "do_not_run_start_memory_comparison_with_unqualified_move",
        "success_decision": "preregister_v17g_matched_accepted_edge_work_start_memory_gate",
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "no_early_stop": True,
        "not_claimed": [
            "global_irreducibility", "mixing", "convergence", "global_uniformity",
            "canonical_measure", "expanded_component_connectivity", "source_effect",
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
        "design_pilot_sha256": file_sha256(DESIGN_PILOT),
        "source_history_count": 6,
        "state_space": v16x.COARSE_ARM,
        "start_families": ";".join(START_FAMILIES),
        "chain_seed_families": ";".join(CHAIN_SEED_FAMILIES),
        "proposal_law": "half_v17c_length_2_4_half_bounded_search_batch_guided_length_5",
        "old_length_choices": ";".join(str(value) for value in OLD_LENGTH_CHOICES),
        "new_cycle_length": NEW_CYCLE_LENGTH,
        "first_batch_size": FIRST_BATCH_SIZE,
        "maximum_search_states_per_guide": MAX_SEARCH_STATES_PER_GUIDE,
        "total_steps": TOTAL_STEPS,
        "representation_steps": REPRESENTATION_STEPS,
        "reversibility_attempts": REVERSIBILITY_ATTEMPTS,
        "minimum_valid_proposals_per_chain": MIN_VALID_PROPOSALS_PER_CHAIN,
        "minimum_accepted_cycles_per_chain": MIN_ACCEPTED_CYCLES_PER_CHAIN,
        "minimum_accepted_old_cycles_per_chain": MIN_ACCEPTED_OLD_CYCLES_PER_CHAIN,
        "minimum_accepted_length5_cycles_per_chain": MIN_ACCEPTED_LENGTH5_CYCLES_PER_CHAIN,
        "minimum_unique_states_per_chain": MIN_UNIQUE_STATES_PER_CHAIN,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "required_frozen_start_replays": 12,
        "required_reversibility_witnesses": 12,
        "required_novel_one_step_witnesses": 12,
        "required_representation_passes": 12,
        "required_movement_passes": 24,
        "required_resource_passes": 24,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v17e.verify_outputs()
    if len(v16i.read_csv(DESIGN_PILOT)) != 2:
        raise ValueError("v17f excluded design pilot must contain two rows")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v17f] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    expected = {key: str(value) for key, value in preregistration_row().items()}
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v17f preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v17f source chain changed")


def reversibility_rows(
    dag: v16i.RunDAG,
    kernel: CycleKernel,
    start: frozenset[Edge],
    start_family: str,
) -> List[Dict[str, Any]]:
    rng = random.Random(v16i.stable_seed(
        "v17f", "reversibility", start_family, *dag.key
    ))
    witness = None
    attempts = 0
    while witness is None and attempts < REVERSIBILITY_ATTEMPTS:
        attempts += 1
        witness = propose_length5(kernel, start, rng)
    if witness is None:
        return [{
            **dag.prefix,
            "start_family": start_family,
            "cycle_length": 0,
            "attempts": attempts,
            "proposal_sha256": "",
            "first_batch_sha256": "",
            "eligible_first_count": 0,
            "q_forward_numerator": 0,
            "q_forward_denominator": 0,
            "q_reverse_numerator": 0,
            "q_reverse_denominator": 0,
            "reverse_support_pass": 0,
            "reverse_recovery_pass": 0,
            "batch_roundtrip_pass": 0,
            "old_kernel_one_step_unsupported_pass": 0,
            "pathwise_detailed_balance_pass": 0,
            "forward_search_states": 0,
            "reverse_search_states": 0,
        }]
    proposed = v17a.apply_proposal(kernel.space, start, witness.proposal)
    reverse_batch = reverse_first_batch(witness)
    reverse = length5_path_probability(
        kernel,
        proposed,
        v17a.reverse_remove_sequence(witness.proposal),
        reverse_batch,
    )
    recovered = False
    batch_roundtrip = False
    balance = False
    q_forward = Fraction(1, 2) * witness.probability
    q_reverse = Fraction(0)
    if reverse is not None:
        recovered = v17a.apply_proposal(
            kernel.space, proposed, reverse.proposal
        ) == start
        batch_roundtrip = reverse_first_batch(reverse) == witness.first_batch
        q_reverse = Fraction(1, 2) * reverse.probability
        alpha_forward = min(Fraction(1), q_reverse / q_forward)
        alpha_reverse = min(Fraction(1), q_forward / q_reverse)
        balance = q_forward * alpha_forward == q_reverse * alpha_reverse
    old_unsupported = v17c.path_probability(
        kernel, start, witness.proposal.remove
    ) is None
    return [{
        **dag.prefix,
        "start_family": start_family,
        "cycle_length": len(witness.proposal.remove),
        "attempts": attempts,
        "proposal_sha256": v17a.proposal_digest(witness.proposal),
        "first_batch_sha256": hashlib.sha256(json.dumps(
            witness.first_batch, separators=(",", ":")
        ).encode("utf-8")).hexdigest(),
        "eligible_first_count": witness.eligible_first_count,
        "q_forward_numerator": q_forward.numerator,
        "q_forward_denominator": q_forward.denominator,
        "q_reverse_numerator": q_reverse.numerator,
        "q_reverse_denominator": q_reverse.denominator,
        "reverse_support_pass": int(reverse is not None),
        "reverse_recovery_pass": int(recovered),
        "batch_roundtrip_pass": int(batch_roundtrip),
        "old_kernel_one_step_unsupported_pass": int(old_unsupported),
        "pathwise_detailed_balance_pass": int(balance),
        "forward_search_states": witness.search_states,
        "reverse_search_states": reverse.search_states if reverse else 0,
    }]


def representation_row(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    space: v16x.StateSpace,
    start: frozenset[Edge],
    start_family: str,
) -> Dict[str, Any]:
    def execute(target_space: v16x.StateSpace) -> ChainResult:
        return run_chain(
            dag,
            v17a.build_kernel(target_space),
            start,
            start_family,
            "representation_seed",
            total_steps=REPRESENTATION_STEPS,
        )

    original = execute(space)
    replay = execute(space)
    reordered_space = v16x.StateSpace(
        arm=space.arm,
        candidates=tuple(reversed(space.candidates)),
        source_edges=space.source_edges,
        slot_by_edge=space.slot_by_edge,
        parent_demands=space.parent_demands,
        slot_demands=space.slot_demands,
        edge_count=space.edge_count,
    )
    reordered = execute(reordered_space)
    relabeled_metadata = v16x.v16w.relabel_metadata(
        metadata,
        v16i.stable_seed("v17f", "semantic_relabel", start_family, *dag.key),
    )
    relabeled_space = v16x.build_state_space(dag, relabeled_metadata, v16x.COARSE_ARM)
    relabeled = execute(relabeled_space)
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
        "representation_pass": int(all((
            candidate_set_pass, replay_pass, order_pass, relabel_pass
        ))),
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


def markdown_table(
    rows: Sequence[Mapping[str, Any]], fields: Sequence[str]
) -> List[str]:
    return v17b.markdown_table(rows, fields)


def write_documents(
    overall: str,
    gates: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    transitions: Sequence[Mapping[str, Any]],
    pilot_rows: Sequence[Mapping[str, Any]],
) -> None:
    maximum_seconds = max(float(row["elapsed_seconds"]) for row in transitions)
    minimum_length5 = min(int(row["accepted_length5_cycles"]) for row in transitions)
    minimum_old = min(int(row["accepted_old_cycles"]) for row in transitions)
    minimum_change = min(
        float(row["final_start_changed_edge_fraction"]) for row in transitions
    )
    minimum_work = min(int(row["accepted_edge_work"]) for row in transitions)
    report = [
        "# v17f effect-blind length-5 move qualification",
        "",
        f"Status: `{overall}`.",
        "",
        "## Purpose and measurable goal",
        "",
        "Purpose `purpose://validation`: determine whether one genuinely new one-step move can be added without weakening probability, representation, traversal or resource discipline. Goal G1 requires frozen starts 12/12, length-5 reverse/batch/novelty witnesses 12/12, representation 12/12, finite movement 24/24 and resource 24/24.",
        "",
        "## Evidential starting point",
        "",
        "V17e retired further scale growth of the exact length-2-to-4 kernel after material cross-start contraction passed 0/6. V17f does not reinterpret that result. It qualifies a different move component before any new start-memory comparison.",
        "",
        "## Proposal law",
        "",
        "The expanded chain chooses the qualified v17c length-2-to-4 component or the new fixed length-5 component with probability 1/2. The length-5 auxiliary samples an ordered batch of four selected edges uniformly without replacement, chooses uniformly among batch edges with a deterministic completion witness under a 20,000-state DFS cap, then samples each raw parent and each witness-supported selected edge uniformly. A dead branch is a self-loop.",
        "",
        "The reverse auxiliary uses the reversed added-edge path and a bijective map of the ordered first-edge batch. Exact auxiliary probabilities enter a lazy Metropolis correction. The declared target is uniform only within each connected component of this expanded proposal kernel.",
        "",
        "## Excluded design pilot",
        "",
        *markdown_table(pilot_rows, (
            "growth_seed", "run_offset", "start_family", "attempts",
            "valid_proposals", "accepted_cycles", "reverse_unsupported",
            "maximum_proposal_seconds", "elapsed_seconds",
        )),
        "",
        "The pilot selected only algorithmic bounds. It was excluded from the formal six-source gate and computed no source spectrum or observed effect.",
        "",
        "## Source qualification",
        "",
        *markdown_table(summaries, (
            "growth_seed", "run_offset", "frozen_start_passes",
            "reversibility_passes", "novel_one_step_passes",
            "representation_passes", "movement_passes", "resource_passes",
            "minimum_accepted_length5_cycles", "maximum_chain_seconds",
            "source_qualification_pass",
        )),
        "",
        "## Gates",
        "",
        *markdown_table(gates, ("gate", "status", "observed", "required", "decision")),
        "",
        "## Finite chain evidence",
        "",
        f"Across 24 formal chains, the minimum accepted old-cycle count was `{minimum_old}`, the minimum accepted length-5 count `{minimum_length5}`, minimum accepted-edge work `{minimum_work}`, minimum final displacement `{minimum_change:.6f}`, and maximum runtime `{maximum_seconds:.6f}` seconds.",
        "",
        "## Claim boundary",
        "",
        "A qualified result establishes only a finite, effect-blind move implementation with tested pathwise detailed balance, representation covariance, traversal and resource behavior. A length-5 transition being outside the old kernel's one-step length support does not show that it crosses an old connected component; it may still be a composition of old moves.",
        "",
        "No source spectrum, observed effect, convergence, mixing, irreducibility, energy, temperature, Lorentz symmetry, spacetime, particle, Bell correlation, entanglement or universe model was tested.",
        "",
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    INTERPRETATION.write_text(
        "# v17f interpretation audit\n\n"
        f"Frozen status is `{overall}`. Algebraic one-step novelty, generator hygiene, "
        "finite reversibility witnesses, representation replay and observed chain movement "
        "are separate evidence layers. The bounded witness search defines the proposal law; "
        "it does not enumerate every length-5 cycle. One-step novelty does not prove a new "
        "Markov component bridge. Source spectrum and observed effects remained prohibited.\n",
        encoding="utf-8",
    )
    if overall == "v17f_length5_move_component_qualified":
        next_text = (
            "Preregister v17g as an effect-blind matched-realized-work start-memory gate. "
            "Compare the old length-2-to-4 kernel with the expanded v17f kernel on the same "
            "six spaces, two starts and independent seeds. Match cumulative accepted removed-edge "
            "work exactly; require the expanded kernel to reduce absolute cross-start distance, "
            "not merely the cross/within ratio. Keep source spectrum closed."
        )
        recommendation = (
            "run one matched accepted-edge-work start-memory comparison; do not open effects"
        )
    elif overall in {
        "v17f_length5_exercise_not_qualified",
        "v17f_finite_movement_not_qualified",
    }:
        next_text = (
            "Retire this bounded-search batch-guided length-5 law. Do not rescue it with a larger "
            "step budget. Select a different move class with a separately auditable reverse law."
        )
        recommendation = "retire this length-5 proposal law and redesign the move class"
    elif overall == "v17f_resource_not_qualified":
        next_text = (
            "Do not run a start-memory comparison. Optimize only the deterministic witness "
            "implementation while preserving exact transition replay, or retire it if the "
            "frozen resource bound cannot be met."
        )
        recommendation = "repair resource behavior without changing the frozen probability law"
    else:
        next_text = (
            "Stop at the first failed instrumentation, reverse, batch-pairing, novelty or "
            "representation layer. Repair that layer without inspecting source spectrum."
        )
        recommendation = "repair the first failed qualification layer; effects remain closed"
    NEXT_DIRECTION.write_text(
        f"# v17f next direction\n\nFormal status: `{overall}`.\n\n{next_text}\n",
        encoding="utf-8",
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.17f\n\n"
        f"- status: `{overall}`\n"
        f"- next: {recommendation}\n"
        "- claim ceiling: finite effect-blind move qualification, not connectivity or physics\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf v0.17f for ikke-spesialister\n\n"
        "V17e viste at det ikke hjalp nok aa la den samme typen smaa graf-flytt gaa lenger. "
        "V17f tester derfor en ny type flytt som bytter fem koblinger i en lukket syklus. "
        "Den gamle flytten beholdes i halvparten av forslagene, mens den nye flytten maa vise "
        "at den kan reverseres, ikke avhenger av representasjonsrekkefolge, faktisk blir brukt "
        "og holder tidsgrensen.\n\n"
        f"Statusen er `{overall}`. Selv en bestaa-status sier ikke at de to tidligere "
        "startfamiliene er koblet sammen. Det krever en egen senere sammenligning med noyaktig "
        "samme mengde realisert grafarbeid.\n",
        encoding="utf-8",
    )


def run() -> None:
    verify_frozen_sources()
    if tuple(v17c.EXACT_LENGTH_CHOICES) != OLD_LENGTH_CHOICES:
        raise ValueError("v17f old kernel length choices changed")
    frozen_starts = v16z.frozen_start_digests()
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
        source_reversibility = []
        source_representations = []
        source_transitions = []
        frozen_start_passes = 0
        for start_family, start in starts.items():
            frozen_start_passes += int(
                v16x.edge_digest(start)
                == frozen_starts[(dag.growth_seed, dag.run_offset, start_family)]
            )
            source_reversibility.extend(
                reversibility_rows(dag, kernel, start, start_family)
            )
            source_representations.append(
                representation_row(dag, metadata, space, start, start_family)
            )
            for seed_family in CHAIN_SEED_FAMILIES:
                result = run_chain(
                    dag, kernel, start, start_family, seed_family
                )
                result.stats["transition_sha256"] = result.transition_digest
                traces.extend(result.trace)
                source_transitions.append(dict(result.stats))

        reversibility.extend(source_reversibility)
        representations.extend(source_representations)
        transitions.extend(source_transitions)
        reverse_passes = sum(
            int(row["reverse_support_pass"])
            and int(row["reverse_recovery_pass"])
            and int(row["pathwise_detailed_balance_pass"])
            for row in source_reversibility
        )
        batch_passes = sum(
            int(row["batch_roundtrip_pass"]) for row in source_reversibility
        )
        novelty_passes = sum(
            int(row["old_kernel_one_step_unsupported_pass"])
            for row in source_reversibility
        )
        representation_passes = sum(
            int(row["representation_pass"]) for row in source_representations
        )
        movement_passes = sum(
            int(row["movement_pass"]) for row in source_transitions
        )
        resource_passes = sum(
            int(row["resource_pass"]) for row in source_transitions
        )
        integrity_passes = sum(
            int(row["final_assignment_integrity_pass"])
            for row in source_transitions
        )
        source_pass = all((
            frozen_start_passes == 2,
            reverse_passes == 2,
            batch_passes == 2,
            novelty_passes == 2,
            representation_passes == 2,
            movement_passes == 4,
            resource_passes == 4,
            integrity_passes == 4,
        ))
        summaries.append({
            **dag.prefix,
            "frozen_start_passes": frozen_start_passes,
            "reversibility_passes": reverse_passes,
            "batch_roundtrip_passes": batch_passes,
            "novel_one_step_passes": novelty_passes,
            "representation_passes": representation_passes,
            "movement_passes": movement_passes,
            "resource_passes": resource_passes,
            "integrity_passes": integrity_passes,
            "minimum_accepted_length5_cycles": min(
                int(row["accepted_length5_cycles"]) for row in source_transitions
            ),
            "minimum_final_start_changed_edge_fraction": min(
                float(row["final_start_changed_edge_fraction"])
                for row in source_transitions
            ),
            "maximum_chain_seconds": max(
                float(row["elapsed_seconds"]) for row in source_transitions
            ),
            "source_qualification_pass": int(source_pass),
        })
        print(
            f"[v17f] sources={run_index}/6 reverse={reverse_passes}/2 "
            f"representation={representation_passes}/2 movement={movement_passes}/4 "
            f"resource={resource_passes}/4"
        )

    calls = implementation_call_counts()
    exclusion_pass = all((
        calls == {"spectrum_calls": 0, "effect_metric_calls": 0},
        all(int(row["source_spectrum_computed"]) == 0 for row in traces),
        all(int(row["observed_effect_computed"]) == 0 for row in traces),
        all(int(row["source_spectrum_computed"]) == 0 for row in transitions),
        all(int(row["observed_effect_computed"]) == 0 for row in transitions),
    ))
    start_count = sum(int(row["frozen_start_passes"]) for row in summaries)
    reverse_count = sum(
        int(row["reverse_support_pass"])
        and int(row["reverse_recovery_pass"])
        and int(row["pathwise_detailed_balance_pass"])
        for row in reversibility
    )
    batch_count = sum(int(row["batch_roundtrip_pass"]) for row in reversibility)
    novelty_count = sum(
        int(row["old_kernel_one_step_unsupported_pass"]) for row in reversibility
    )
    representation_count = sum(
        int(row["representation_pass"]) for row in representations
    )
    integrity_count = sum(
        int(row["final_assignment_integrity_pass"]) for row in transitions
    )
    length5_exercise_count = sum(
        int(row["accepted_length5_cycles"])
        >= MIN_ACCEPTED_LENGTH5_CYCLES_PER_CHAIN
        for row in transitions
    )
    movement_count = sum(int(row["movement_pass"]) for row in transitions)
    resource_count = sum(int(row["resource_pass"]) for row in transitions)

    if not exclusion_pass or start_count != 12 or integrity_count != 24:
        overall = "v17f_instrumentation_failed"
    elif reverse_count != 12:
        overall = "v17f_reversibility_not_qualified"
    elif batch_count != 12:
        overall = "v17f_batch_pairing_not_qualified"
    elif novelty_count != 12:
        overall = "v17f_one_step_novelty_not_qualified"
    elif representation_count != 12:
        overall = "v17f_representation_not_qualified"
    elif length5_exercise_count != 24:
        overall = "v17f_length5_exercise_not_qualified"
    elif movement_count != 24:
        overall = "v17f_finite_movement_not_qualified"
    elif resource_count != 24:
        overall = "v17f_resource_not_qualified"
    else:
        overall = "v17f_length5_move_component_qualified"

    gates = [
        {"gate": "effect_blind_integrity", "status": "pass" if exclusion_pass else "fail", "observed": f"spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}", "required": "0;0", "decision": "continue" if exclusion_pass else "invalidate"},
        {"gate": "frozen_start_and_assignment_integrity", "status": "pass" if start_count == 12 and integrity_count == 24 else "fail", "observed": f"starts={start_count}/12;final_integrity={integrity_count}/24", "required": "12/12;24/24", "decision": "continue" if start_count == 12 and integrity_count == 24 else "invalidate"},
        {"gate": "length5_pathwise_detailed_balance", "status": "pass" if reverse_count == 12 else "fail", "observed": f"{reverse_count}/12", "required": "12/12", "decision": "continue" if reverse_count == 12 else "repair_probability"},
        {"gate": "ordered_batch_reverse_pairing", "status": "pass" if batch_count == 12 else "fail", "observed": f"{batch_count}/12", "required": "12/12", "decision": "continue" if batch_count == 12 else "repair_auxiliary_mapping"},
        {"gate": "new_one_step_length_support", "status": "pass" if novelty_count == 12 else "fail", "observed": f"{novelty_count}/12", "required": "12/12", "decision": "one_step_novelty_only" if novelty_count == 12 else "not_novel"},
        {"gate": "representation_covariance", "status": "pass" if representation_count == 12 else "fail", "observed": f"{representation_count}/12", "required": "12/12", "decision": "continue" if representation_count == 12 else "repair_representation"},
        {"gate": "length5_finite_exercise", "status": "pass" if length5_exercise_count == 24 else "fail", "observed": f"{length5_exercise_count}/24;min={min(int(row['accepted_length5_cycles']) for row in transitions)}", "required": f"24/24;each>={MIN_ACCEPTED_LENGTH5_CYCLES_PER_CHAIN}", "decision": "continue" if length5_exercise_count == 24 else "retire_candidate"},
        {"gate": "finite_traversal_and_resource", "status": "pass" if movement_count == resource_count == 24 else "fail", "observed": f"movement={movement_count}/24;resource={resource_count}/24;max={max(float(row['elapsed_seconds']) for row in transitions):.6f}s", "required": f"24/24;24/24;each<={MAX_CHAIN_SECONDS:.0f}s", "decision": "continue" if movement_count == resource_count == 24 else "do_not_compare_start_memory"},
        {"gate": "v17f_overall", "status": overall, "observed": f"exclusion={int(exclusion_pass)};starts={start_count}/12;integrity={integrity_count}/24;reverse={reverse_count}/12;batch={batch_count}/12;novelty={novelty_count}/12;representation={representation_count}/12;exercise={length5_exercise_count}/24;movement={movement_count}/24;resource={resource_count}/24", "required": "1;12/12;24/24;12/12;12/12;12/12;12/12;24/24;24/24;24/24", "decision": overall},
    ]
    goal_status = "satisfied" if overall == "v17f_length5_move_component_qualified" else "missed"
    goals = [{
        "goal_id": "G1",
        "purpose_ref": PURPOSE_REF,
        "metric": "all frozen probability, representation, finite exercise, movement and resource gates",
        "baseline": "v17e retired length-2-to-4 scale growth; no qualified replacement move",
        "target": "reverse/batch/novelty/representation 12/12 and exercise/movement/resource 24/24",
        "timeframe": "v17f formal round",
        "status": goal_status,
        "evidence": "v17f_gate_evaluation.csv;v17f_source_qualification_summary.csv",
    }]
    claims = [
        {"claim_id": "C1", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "factual", "strength": "assertive", "claim": "v17f computes no source spectrum or observed-effect statistic.", "status": "supported" if exclusion_pass else "contradicted", "evidence": "static call audit plus trace/summary exclusion fields", "scope_limit": "this script and tracked outputs"},
        {"claim_id": "C2", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "factual", "strength": "moderated", "claim": "The tested length-5 auxiliaries have reverse support, batch roundtrip and pathwise detailed balance.", "status": "supported" if reverse_count == batch_count == 12 else "not_supported", "evidence": "v17f_pathwise_reversibility_audit.csv", "scope_limit": "12 finite witnesses; not an exhaustive state-space proof"},
        {"claim_id": "C3", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "factual", "strength": "assertive", "claim": "Each tested length-5 witness is outside the old kernel's one-step length support.", "status": "supported" if novelty_count == 12 else "not_supported", "evidence": "v17f_pathwise_reversibility_audit.csv", "scope_limit": "one-step novelty only; not connected-component novelty"},
        {"claim_id": "C4", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "project_capability", "strength": "moderated", "claim": "The expanded kernel qualifies finite representation, exercise, traversal and resource behavior under all frozen thresholds.", "status": "supported" if overall == "v17f_length5_move_component_qualified" else "not_supported", "evidence": "v17f_representation_audit.csv;v17f_chain_transition_summary.csv", "scope_limit": "six finite spaces and 24 chains"},
        {"claim_id": "C5", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "causal", "strength": "speculative", "claim": "The length-5 move crosses a connected component inaccessible to the old kernel.", "status": "not_tested", "evidence": "none", "scope_limit": "one-step novelty does not establish this"},
        {"claim_id": "C6", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "statistical", "strength": "speculative", "claim": "The expanded kernel reduces cross-start memory under matched realized work.", "status": "not_tested", "evidence": "no matched-work comparison in v17f", "scope_limit": "candidate question for v17g only after qualification"},
        {"claim_id": "C7", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "project_capability", "strength": "speculative", "claim": "v17f establishes source effects, Bell correlations, entanglement, Lorentz symmetry, spacetime or a universe model.", "status": "contradicted", "evidence": "required observables were prohibited or absent", "scope_limit": "requires separate later operational gates"},
    ]

    v16i.write_csv(PROPOSAL_TRACE, traces)
    v16i.write_csv(REVERSIBILITY_AUDIT, reversibility)
    v16i.write_csv(REPRESENTATION_AUDIT, representations)
    v16i.write_csv(TRANSITION_SUMMARY, transitions)
    v16i.write_csv(SOURCE_SUMMARY, summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(GOAL_EVALUATION, goals)
    v16i.write_csv(CLAIM_LEDGER, claims)
    write_documents(
        overall, gates, summaries, transitions, v16i.read_csv(DESIGN_PILOT)
    )
    print(f"[v17f] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    pilot_rows = v16i.read_csv(DESIGN_PILOT)
    traces = v16i.read_csv(PROPOSAL_TRACE)
    reversibility = v16i.read_csv(REVERSIBILITY_AUDIT)
    representations = v16i.read_csv(REPRESENTATION_AUDIT)
    transitions = v16i.read_csv(TRANSITION_SUMMARY)
    summaries = v16i.read_csv(SOURCE_SUMMARY)
    gates = v16i.read_csv(GATE_EVALUATION)
    goals = v16i.read_csv(GOAL_EVALUATION)
    claims = v16i.read_csv(CLAIM_LEDGER)
    if len(pilot_rows) != 2:
        raise ValueError("v17f design pilot row count failed")
    if len(traces) != 24 * TOTAL_STEPS:
        raise ValueError("v17f trace row count failed")
    if len(reversibility) != 12 or len(representations) != 12:
        raise ValueError("v17f reversibility/representation row count failed")
    if len(transitions) != 24 or len(summaries) != 6:
        raise ValueError("v17f transition/source row count failed")
    if len(gates) != 9 or len(goals) != 1 or len(claims) != 7:
        raise ValueError("v17f gate/goal/claim row count failed")
    if implementation_call_counts() != {
        "spectrum_calls": 0,
        "effect_metric_calls": 0,
    }:
        raise ValueError("v17f effect exclusion failed")
    for rows in (pilot_rows, traces, transitions):
        if any(int(row["source_spectrum_computed"]) for row in rows):
            raise ValueError("v17f output contains source spectrum")
        if any(int(row["observed_effect_computed"]) for row in rows):
            raise ValueError("v17f output contains observed effect")
    candidate_rows = [
        row for row in traces
        if row["move_class"] == "length_5_batch_guided"
    ]
    if not candidate_rows:
        raise ValueError("v17f trace contains no length-5 proposal")
    if any(int(row["cycle_length"]) != NEW_CYCLE_LENGTH for row in candidate_rows):
        raise ValueError("v17f length-5 trace contains another cycle length")
    if any(int(row["old_one_step_length_support"]) for row in candidate_rows):
        raise ValueError("v17f length-5 trace was marked old one-step support")
    if any(row["status"] not in {"satisfied", "missed"} for row in goals):
        raise ValueError("v17f goal status is not terminal")
    overall = next(row["status"] for row in gates if row["gate"] == "v17f_overall")
    allowed = {
        "v17f_instrumentation_failed",
        "v17f_reversibility_not_qualified",
        "v17f_batch_pairing_not_qualified",
        "v17f_one_step_novelty_not_qualified",
        "v17f_representation_not_qualified",
        "v17f_length5_exercise_not_qualified",
        "v17f_finite_movement_not_qualified",
        "v17f_resource_not_qualified",
        "v17f_length5_move_component_qualified",
    }
    if overall not in allowed:
        raise ValueError("v17f overall status is unknown")
    for path in (
        REPORT, INTERPRETATION, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST
    ):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"v17f documentation missing: {path.name}")
    print(f"[v17f] output verification pass overall={overall}")


def self_test() -> None:
    role = ("test", ("resource",))
    slot_class = (role, 0, "witness")
    parents = tuple(range(6))
    children = tuple(range(10, 16))
    candidates = tuple(
        (parent, child) for parent in parents for child in children
    )
    source = frozenset(zip(parents, children))
    space = v16x.StateSpace(
        arm="test",
        candidates=candidates,
        source_edges=source,
        slot_by_edge={edge: (edge[1], slot_class) for edge in candidates},
        parent_demands={parent: 1 for parent in parents},
        slot_demands={(child, slot_class): 1 for child in children},
        edge_count=6,
    )
    kernel = v17a.build_kernel(space)
    rng = random.Random(1705001)
    witness = None
    for _ in range(256):
        witness = propose_length5(kernel, source, rng)
        if witness is not None:
            break
    if witness is None:
        raise AssertionError("v17f synthetic length-5 witness missing")
    proposed = v17a.apply_proposal(space, source, witness.proposal)
    reverse = length5_path_probability(
        kernel,
        proposed,
        v17a.reverse_remove_sequence(witness.proposal),
        reverse_first_batch(witness),
    )
    if reverse is None:
        raise AssertionError("v17f synthetic reverse support missing")
    if v17a.apply_proposal(space, proposed, reverse.proposal) != source:
        raise AssertionError("v17f synthetic reverse recovery failed")
    if reverse_first_batch(reverse) != witness.first_batch:
        raise AssertionError("v17f synthetic batch roundtrip failed")
    q_forward = Fraction(1, 2) * witness.probability
    q_reverse = Fraction(1, 2) * reverse.probability
    alpha_forward = min(Fraction(1), q_reverse / q_forward)
    alpha_reverse = min(Fraction(1), q_forward / q_reverse)
    if q_forward * alpha_forward != q_reverse * alpha_reverse:
        raise AssertionError("v17f synthetic pathwise balance failed")
    if v17c.path_probability(kernel, source, witness.proposal.remove) is not None:
        raise AssertionError("v17f synthetic move is old one-step length support")
    dag = v16i.RunDAG(
        stage="v17f_test",
        target_nodes=6,
        growth_seed=1,
        run_offset=2,
        arm="test",
        run_seed=3,
        predecessors=tuple(() for _ in range(6)),
        depths=tuple(0 for _ in range(6)),
        indegrees=tuple(0 for _ in range(6)),
    )
    first = run_chain(
        dag, kernel, source, "source_assignment", "self_test", total_steps=64
    )
    second = run_chain(
        dag, kernel, source, "source_assignment", "self_test", total_steps=64
    )
    if first.final != second.final or first.transition_digest != second.transition_digest:
        raise AssertionError("v17f deterministic replay failed")
    if implementation_call_counts() != {
        "spectrum_calls": 0,
        "effect_metric_calls": 0,
    }:
        raise AssertionError("v17f effect exclusion audit failed")
    print("[v17f] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="v17f effect-blind length-5 move qualification"
    )
    parser.add_argument("--design-pilot", action="store_true")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if sum((
        args.design_pilot,
        args.prepare_only,
        args.self_test,
        args.verify_only,
    )) > 1:
        parser.error("choose at most one mode")
    if args.design_pilot:
        run_design_pilot()
    elif args.prepare_only:
        prepare()
    elif args.self_test:
        self_test()
    elif args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
