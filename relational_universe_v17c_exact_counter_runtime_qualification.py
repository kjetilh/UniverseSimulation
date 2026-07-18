#!/usr/bin/env python3
"""v17c exact-counter runtime qualification for the v17b proposal law.

The proposal law, starts, seeds, step budget, laziness and exact Metropolis
ratio are inherited unchanged from v17b. Only the implementation changes: an
exact dynamic-programming counter selects one uniform completion rank without
materializing the full support or recounting the forward support. Source
spectrum and observed-effect statistics remain prohibited.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import statistics
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16x_explicit_global_measure_gate as v16x
import relational_universe_v16z_alternating_cycle_bridge_gate as v16z
import relational_universe_v17a_state_independent_cycle_proposal_qualification as v17a
import relational_universe_v17b_residual_cycle_constructor_gate as v17b


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

START_FAMILIES = v17b.START_FAMILIES
CHAIN_SEED_FAMILIES = v17b.CHAIN_SEED_FAMILIES
EXACT_LENGTH_CHOICES = v17b.EXACT_LENGTH_CHOICES
TOTAL_STEPS = v17b.TOTAL_STEPS
REPRESENTATION_STEPS = v17b.REPRESENTATION_STEPS
MIN_VALID_PROPOSALS_PER_CHAIN = v17b.MIN_VALID_PROPOSALS_PER_CHAIN
MIN_ACCEPTED_CYCLES_PER_CHAIN = v17b.MIN_ACCEPTED_CYCLES_PER_CHAIN
MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN = v17b.MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN
MIN_UNIQUE_STATES_PER_CHAIN = v17b.MIN_UNIQUE_STATES_PER_CHAIN
MIN_FINAL_START_CHANGE = v17b.MIN_FINAL_START_CHANGE
MAX_CHAIN_SECONDS = v17b.MAX_CHAIN_SECONDS

SOURCE_CHAIN = DOC / "v17c_source_chain.csv"
PRE_REGISTRATION = DOC / "v17c_pre_registration.csv"
COUNTER_PARITY_AUDIT = DOC / "v17c_counter_parity_audit.csv"
PROPOSAL_TRACE = DOC / "v17c_exact_counter_trace.csv"
REVERSIBILITY_AUDIT = DOC / "v17c_pathwise_reversibility_audit.csv"
REPRESENTATION_AUDIT = DOC / "v17c_representation_audit.csv"
TRANSITION_SUMMARY = DOC / "v17c_chain_transition_summary.csv"
PAIRED_RUNTIME = DOC / "v17c_paired_v17b_runtime.csv"
SOURCE_SUMMARY = DOC / "v17c_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v17c_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v17c_claim_ledger.csv"
REPORT = DOC / "v17c_exact_counter_runtime_qualification.md"
INTERPRETATION = DOC / "v17c_interpretation_audit.md"
NEXT_DIRECTION = DOC / "v17c_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_17c_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_17c.md"

Edge = v16x.Edge
Slot = v16x.Slot
CycleKernel = v17a.CycleKernel
CycleProposal = v17a.CycleProposal
ResidualAuxiliary = v17b.ResidualAuxiliary


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v17b", "frozen_preregistration", v17b.PRE_REGISTRATION),
        ("v17b", "failed_resource_gate", v17b.GATE_EVALUATION),
        ("v17b", "matched_transition_baseline", v17b.TRANSITION_SUMMARY),
        ("v17b", "exact_trace_baseline", v17b.PROPOSAL_TRACE),
        ("v17b", "proposal_implementation", v17b.SCRIPT),
        ("v17b", "postrun_runtime_diagnosis", DOC / "v17b_postrun_runtime_diagnosis.md"),
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
        "gate": "v17c_exact_counter_runtime_qualification",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_implementation_equivalence_and_runtime_qualification",
        "state_space": v16x.COARSE_ARM,
        "source_history_count": 6,
        "start_families": list(START_FAMILIES),
        "chain_seed_families": list(CHAIN_SEED_FAMILIES),
        "proposal_law": "identical_to_frozen_v17b_ordered_residual_cycle_law",
        "implementation": "exact_state_counter_plus_uniform_depth_first_rank",
        "counter_state": "current_slot_used_parents_used_slots_depth_with_fixed_first_parent",
        "terminal_lemma": (
            "distinct selected parents and slots plus residual continuation validity "
            "reduce terminal validity to the exact closure-edge test"
        ),
        "exact_length_choices": list(EXACT_LENGTH_CHOICES),
        "proposal_auxiliary_pairing": "same_exact_length_and_reverse_ordered_added_edges",
        "metropolis_ratio": "min(1,q_reverse_auxiliary/q_forward_auxiliary)",
        "laziness_probability": "1/2",
        "total_steps": TOTAL_STEPS,
        "representation_steps": REPRESENTATION_STEPS,
        "minimum_valid_proposals_per_chain": MIN_VALID_PROPOSALS_PER_CHAIN,
        "minimum_accepted_cycles_per_chain": MIN_ACCEPTED_CYCLES_PER_CHAIN,
        "minimum_accepted_long_cycles_per_chain": MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN,
        "minimum_unique_states_per_chain": MIN_UNIQUE_STATES_PER_CHAIN,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "required_counter_parity_cells": 36,
        "required_exact_chain_replays": 24,
        "required_movement_passes": 24,
        "required_resource_passes": 24,
        "failure_decision": "retire_full_bounded_cycle_enumeration_as_active_sampler",
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
        "proposal_law": "identical_to_frozen_v17b_ordered_residual_cycle_law",
        "implementation": "exact_state_counter_plus_uniform_depth_first_rank",
        "exact_length_choices": ";".join(str(value) for value in EXACT_LENGTH_CHOICES),
        "total_steps": TOTAL_STEPS,
        "representation_steps": REPRESENTATION_STEPS,
        "minimum_valid_proposals_per_chain": MIN_VALID_PROPOSALS_PER_CHAIN,
        "minimum_accepted_cycles_per_chain": MIN_ACCEPTED_CYCLES_PER_CHAIN,
        "minimum_accepted_long_cycles_per_chain": MIN_ACCEPTED_LONG_CYCLES_PER_CHAIN,
        "minimum_unique_states_per_chain": MIN_UNIQUE_STATES_PER_CHAIN,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "required_counter_parity_cells": 36,
        "required_exact_chain_replays": 24,
        "required_movement_passes": 24,
        "required_resource_passes": 24,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v17b.verify_outputs()
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v17c] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    expected = {key: str(value) for key, value in preregistration_row().items()}
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v17c preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v17c source chain changed")


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    result = []
    for source, metadata in v16x.load_runs():
        result.append((v16i.RunDAG(
            stage="v17c",
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


class ExactResidualCounter:
    """Count and rank ordered residual cycles without storing complete paths."""

    def __init__(
        self,
        kernel: CycleKernel,
        selected: frozenset[Edge],
        first: Edge,
        cycle_length: int,
    ) -> None:
        self.kernel = kernel
        self.selected = selected
        self.first = first
        self.cycle_length = cycle_length
        self.by_parent = v17a.selected_by_parent(selected)
        self._raw_cache: Dict[Slot, Tuple[Edge, ...]] = {}
        self._root_branches: Tuple[Tuple[Edge, int], ...] | None = None
        slots_by_parent = getattr(kernel, "_v17c_candidate_slots_by_parent", None)
        if slots_by_parent is None:
            mutable: Dict[int, set[Slot]] = defaultdict(set)
            for slot, parents in kernel.candidate_parents_by_slot.items():
                for parent in parents:
                    mutable[parent].add(slot)
            slots_by_parent = {
                parent: frozenset(slots) for parent, slots in mutable.items()
            }
            object.__setattr__(
                kernel, "_v17c_candidate_slots_by_parent", slots_by_parent
            )
        self.closable_slots = slots_by_parent.get(first[0], frozenset())

    def _raw_choices(self, current_slot: Slot) -> Tuple[Edge, ...]:
        cached = self._raw_cache.get(current_slot)
        if cached is not None:
            return cached
        current_child = current_slot[0]
        choices = []
        for parent in self.kernel.candidate_parents_by_slot.get(current_slot, ()):
            if (parent, current_child) in self.selected:
                continue
            choices.extend(self.by_parent.get(parent, ()))
        result = tuple(sorted(choices))
        self._raw_cache[current_slot] = result
        return result

    def _continuations(
        self,
        current_slot: Slot,
        used_parents: frozenset[int],
        used_slots: frozenset[Slot],
    ) -> Tuple[Edge, ...]:
        return tuple(
            edge for edge in self._raw_choices(current_slot)
            if edge[0] not in used_parents
            and self.kernel.space.slot_by_edge[edge] not in used_slots
        )

    def _closure_valid(self, current_slot: Slot) -> bool:
        closure = (self.first[0], current_slot[0])
        return (
            current_slot in self.closable_slots
            and closure not in self.selected
        )

    def _terminal_count(
        self,
        current_slot: Slot,
        used_parents: frozenset[int],
        used_slots: frozenset[Slot],
    ) -> int:
        total = 0
        slot_by_edge = self.kernel.space.slot_by_edge
        first_parent = self.first[0]
        for edge in self._raw_choices(current_slot):
            slot = slot_by_edge[edge]
            if (
                edge[0] not in used_parents
                and slot not in used_slots
                and slot in self.closable_slots
                and (first_parent, slot[0]) not in self.selected
            ):
                total += 1
        return total

    def _subtree_count(
        self,
        current_slot: Slot,
        used_parents: frozenset[int],
        used_slots: frozenset[Slot],
        depth: int,
    ) -> int:
        if depth == self.cycle_length:
            return int(self._closure_valid(current_slot))
        if depth + 1 == self.cycle_length:
            return self._terminal_count(current_slot, used_parents, used_slots)
        total = 0
        for edge in self._continuations(current_slot, used_parents, used_slots):
            slot = self.kernel.space.slot_by_edge[edge]
            total += self._subtree_count(
                slot,
                used_parents | {edge[0]},
                used_slots | {slot},
                depth + 1,
            )
        return total

    def _branch_counts(
        self,
        current_slot: Slot,
        used_parents: frozenset[int],
        used_slots: frozenset[Slot],
        depth: int,
    ) -> Tuple[Tuple[Edge, int], ...]:
        branches = []
        for edge in self._continuations(current_slot, used_parents, used_slots):
            slot = self.kernel.space.slot_by_edge[edge]
            if depth + 1 == self.cycle_length:
                count = int(self._closure_valid(slot))
            else:
                count = self._subtree_count(
                    slot,
                    used_parents | {edge[0]},
                    used_slots | {slot},
                    depth + 1,
                )
            if count:
                branches.append((edge, count))
        return tuple(branches)

    def count(self) -> int:
        if (
            self.cycle_length not in EXACT_LENGTH_CHOICES
            or self.first not in self.selected
        ):
            return 0
        if self._root_branches is not None:
            return sum(count for _, count in self._root_branches)
        slot = self.kernel.space.slot_by_edge[self.first]
        self._root_branches = self._branch_counts(
            slot, frozenset({self.first[0]}), frozenset({slot}), 1
        )
        return sum(count for _, count in self._root_branches)

    def supports(self, remove: Sequence[Edge]) -> bool:
        ordered = tuple(remove)
        if (
            len(ordered) != self.cycle_length
            or not ordered
            or ordered[0] != self.first
            or len(set(ordered)) != len(ordered)
            or not set(ordered).issubset(self.selected)
        ):
            return False
        current_slot = self.kernel.space.slot_by_edge[self.first]
        used_parents = frozenset({self.first[0]})
        used_slots = frozenset({current_slot})
        for edge in ordered[1:]:
            if edge not in self._continuations(current_slot, used_parents, used_slots):
                return False
            current_slot = self.kernel.space.slot_by_edge[edge]
            used_parents |= {edge[0]}
            used_slots |= {current_slot}
        return (
            self._closure_valid(current_slot)
            and v17b.close_proposal(self.kernel, self.selected, ordered) is not None
        )

    def sample(self, rank: int) -> Tuple[Edge, ...]:
        total = self.count()
        if rank < 0 or rank >= total:
            raise IndexError("residual completion rank outside exact support")
        remove = (self.first,)
        current_slot = self.kernel.space.slot_by_edge[self.first]
        used_parents = frozenset({self.first[0]})
        used_slots = frozenset({current_slot})
        branches = self._root_branches
        if branches is None:
            raise AssertionError("exact counter root branches were not initialized")
        while len(remove) < self.cycle_length:
            for edge, branch_count in branches:
                if rank < branch_count:
                    slot = self.kernel.space.slot_by_edge[edge]
                    remove += (edge,)
                    current_slot = slot
                    used_parents |= {edge[0]}
                    used_slots |= {slot}
                    break
                rank -= branch_count
            else:
                raise AssertionError("exact counter rank traversal exhausted support")
            if len(remove) < self.cycle_length:
                branches = self._branch_counts(
                    current_slot,
                    used_parents,
                    used_slots,
                    len(remove),
                )
        if not self.supports(remove):
            raise AssertionError("exact counter produced an unsupported completion")
        return remove


def path_probability(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    remove: Sequence[Edge],
) -> ResidualAuxiliary | None:
    ordered = tuple(remove)
    if not ordered or len(ordered) not in EXACT_LENGTH_CHOICES:
        return None
    ordered_selected = tuple(sorted(selected))
    if not ordered_selected:
        return None
    counter = ExactResidualCounter(kernel, selected, ordered[0], len(ordered))
    count = counter.count()
    if count == 0 or not counter.supports(ordered):
        return None
    proposal = v17b.close_proposal(kernel, selected, ordered)
    if proposal is None:
        return None
    probability = Fraction(1, len(EXACT_LENGTH_CHOICES))
    probability *= Fraction(1, len(ordered_selected))
    probability *= Fraction(1, count)
    return ResidualAuxiliary(probability, proposal, len(ordered), count)


def propose_cycle(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    rng: random.Random,
    *,
    forced_length: int | None = None,
) -> ResidualAuxiliary | None:
    cycle_length = forced_length
    if cycle_length is None:
        cycle_length = EXACT_LENGTH_CHOICES[rng.randrange(len(EXACT_LENGTH_CHOICES))]
    if cycle_length not in EXACT_LENGTH_CHOICES:
        raise ValueError("forced cycle length outside frozen choices")
    ordered_selected = tuple(sorted(selected))
    if not ordered_selected:
        return None
    first = ordered_selected[rng.randrange(len(ordered_selected))]
    counter = ExactResidualCounter(kernel, selected, first, cycle_length)
    count = counter.count()
    if count == 0:
        return None
    remove = counter.sample(rng.randrange(count))
    proposal = v17b.close_proposal(kernel, selected, remove)
    if proposal is None:
        raise AssertionError("sampled exact completion failed proposal closure")
    probability = Fraction(1, len(EXACT_LENGTH_CHOICES))
    probability *= Fraction(1, len(ordered_selected))
    probability *= Fraction(1, count)
    return ResidualAuxiliary(probability, proposal, cycle_length, count)


def install_optimized_constructor() -> None:
    # The frozen v17b runner supplies the unchanged chain and audit semantics.
    v17b.propose_cycle = propose_cycle
    v17b.path_probability = path_probability


def support_sha256(sequences: Iterable[Sequence[Edge]]) -> str:
    digest = hashlib.sha256()
    for sequence in sequences:
        digest.update(json.dumps(tuple(sequence), separators=(",", ":")).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def counter_parity_rows(
    dag: v16i.RunDAG,
    kernel: CycleKernel,
    start: frozenset[Edge],
    start_family: str,
) -> List[Dict[str, Any]]:
    rows = []
    for cycle_length in EXACT_LENGTH_CHOICES:
        first = None
        counter = None
        for candidate in sorted(start):
            candidate_counter = ExactResidualCounter(
                kernel, start, candidate, cycle_length
            )
            if candidate_counter.count():
                first = candidate
                counter = candidate_counter
                break
        if first is None or counter is None:
            rows.append({
                **dag.prefix,
                "start_family": start_family,
                "cycle_length": cycle_length,
                "first_edge_json": "[]",
                "v17b_completion_count": 0,
                "v17c_completion_count": 0,
                "count_parity_pass": 0,
                "baseline_subset_pass": 0,
                "rank_order_sample_pass": 0,
                "support_parity_pass": 0,
                "support_sha256": "",
            })
            continue
        baseline = v17b.residual_cycle_sequences(kernel, start, first, cycle_length)
        sample_ranks = sorted(set((0, len(baseline) // 2, len(baseline) - 1)))
        count_pass = len(baseline) == counter.count()
        subset_pass = all(counter.supports(sequence) for sequence in baseline)
        rank_pass = all(counter.sample(rank) == baseline[rank] for rank in sample_ranks)
        support_pass = count_pass and subset_pass and rank_pass
        rows.append({
            **dag.prefix,
            "start_family": start_family,
            "cycle_length": cycle_length,
            "first_edge_json": json.dumps(first, separators=(",", ":")),
            "v17b_completion_count": len(baseline),
            "v17c_completion_count": counter.count(),
            "count_parity_pass": int(count_pass),
            "baseline_subset_pass": int(subset_pass),
            "rank_order_sample_pass": int(rank_pass),
            "support_parity_pass": int(support_pass),
            "support_sha256": support_sha256(baseline),
        })
    return rows


def baseline_transition_digests() -> Dict[Tuple[int, int, str, str], str]:
    grouped: Dict[Tuple[int, int, str, str], List[Mapping[str, str]]] = defaultdict(list)
    for row in v16i.read_csv(v17b.PROPOSAL_TRACE):
        key = (
            int(row["growth_seed"]), int(row["run_offset"]),
            row["start_family"], row["chain_seed_family"],
        )
        grouped[key].append(row)
    result = {}
    for key, rows in grouped.items():
        payload = [{
            "event": row["event"],
            "cycle_length_choice": int(row["cycle_length_choice"]),
            "cycle_length": int(row["cycle_length"]),
            "proposal": row["proposal_sha256"],
            "accepted": int(row["accepted"]),
            "after": row["state_after_sha256"],
        } for row in sorted(rows, key=lambda item: int(item["step"]))]
        result[key] = hashlib.sha256(json.dumps(
            payload, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")).hexdigest()
    return result


def paired_runtime_rows(
    transitions: Sequence[Mapping[str, Any]],
    transition_digests: Mapping[Tuple[int, int, str, str], str],
) -> List[Dict[str, Any]]:
    baseline = {
        (
            int(row["growth_seed"]), int(row["run_offset"]),
            row["start_family"], row["chain_seed_family"],
        ): row
        for row in v16i.read_csv(v17b.TRANSITION_SUMMARY)
    }
    fields = (
        "valid_proposals", "accepted_cycles", "accepted_long_cycles",
        "unique_state_count", "final_endpoint_sha256",
        "final_start_changed_edge_fraction", "movement_pass",
    )
    rows = []
    for row in transitions:
        key = (
            int(row["growth_seed"]), int(row["run_offset"]),
            str(row["start_family"]), str(row["chain_seed_family"]),
        )
        old = baseline[key]
        summary_pass = all(str(row[field]) == str(old[field]) for field in fields)
        replay_pass = row["transition_sha256"] == transition_digests[key]
        old_seconds = float(old["elapsed_seconds"])
        new_seconds = float(row["elapsed_seconds"])
        rows.append({
            "stage": "v17c",
            "growth_seed": key[0],
            "run_offset": key[1],
            "start_family": key[2],
            "chain_seed_family": key[3],
            "v17b_elapsed_seconds": old_seconds,
            "v17c_elapsed_seconds": new_seconds,
            "runtime_ratio_v17c_over_v17b": new_seconds / old_seconds,
            "runtime_improved": int(new_seconds < old_seconds),
            "summary_parity_pass": int(summary_pass),
            "transition_sha256_v17b": transition_digests[key],
            "transition_sha256_v17c": row["transition_sha256"],
            "exact_transition_replay_pass": int(replay_pass),
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
    paired: Sequence[Mapping[str, Any]],
) -> None:
    minimum_valid = min(int(row["valid_proposals"]) for row in transitions)
    minimum_accepted = min(int(row["accepted_cycles"]) for row in transitions)
    minimum_long = min(int(row["accepted_long_cycles"]) for row in transitions)
    minimum_change = min(float(row["final_start_changed_edge_fraction"]) for row in transitions)
    maximum_seconds = max(float(row["elapsed_seconds"]) for row in transitions)
    median_ratio = statistics.median(float(row["runtime_ratio_v17c_over_v17b"]) for row in paired)
    improved = sum(int(row["runtime_improved"]) for row in paired)
    report = [
        "# v17c exact-counter runtime qualification",
        "",
        f"Status: `{overall}`.",
        "",
        "## Purpose and frozen goal",
        "",
        "Purpose: determine whether the exact v17b proposal law can meet its already frozen finite resource bound without changing its dynamics. Goal: exact support/count parity 36/36, exact chain replay 24/24, movement 24/24 and runtime <=60 seconds 24/24.",
        "",
        "## Method",
        "",
        "v17c keeps the v17b starts, seeds, 512-step budget, cycle lengths, laziness and exact reverse auxiliary. It replaces complete-tuple materialization and duplicate forward enumeration with an exact dynamic-programming completion counter. One random rank is sampled uniformly and traversed in the same depth-first order as v17b.",
        "",
        "## Source qualification",
        "",
        *markdown_table(summaries, (
            "growth_seed", "run_offset", "counter_parity_passes",
            "representation_passes", "reversibility_passes", "exact_replay_passes",
            "movement_passes", "resource_passes", "maximum_chain_seconds",
            "source_qualification_pass",
        )),
        "",
        "## Gates",
        "",
        *markdown_table(gates, ("gate", "status", "observed", "required", "decision")),
        "",
        "## Runtime and finite movement",
        "",
        f"Across 24 chains, minimum valid proposals were `{minimum_valid}`, minimum accepted cycles `{minimum_accepted}`, minimum accepted length>=3 cycles `{minimum_long}`, minimum final displacement `{minimum_change:.6f}`, and maximum runtime `{maximum_seconds:.6f}` seconds.",
        "",
        f"Runtime improved in `{improved}/24` matched cells; the median v17c/v17b runtime ratio was `{median_ratio:.6f}`. Exact transition replay, not similarity of aggregate outcomes, is the implementation-equivalence test.",
        "",
        "## Claim boundary",
        "",
        "This gate tests an implementation of one finite proposal law. It does not establish global irreducibility, convergence, mixing, a canonical measure, source-effect survival, Bell correlations, entanglement, Lorentz symmetry, spacetime or a universe model.",
        "",
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    INTERPRETATION.write_text(
        "# v17c interpretation audit\n\n"
        f"Frozen status is `{overall}`. Counter parity and exact chain replay are algorithmic equivalence evidence. "
        "The resource result concerns this implementation on 24 finite chains. Finite movement is not convergence, mixing or global support. "
        "No source spectrum, observed effect, Bell observable or physical invariant was computed.\n",
        encoding="utf-8",
    )
    if overall == "v17c_exact_counter_runtime_qualified":
        next_text = (
            "Proceed to v17d effect-blind finite stability on the same six spaces. Freeze longer early/late windows, both starts and independent seed families, and require within-source endpoint/component agreement before reopening the source spectrum."
        )
        recommendation = "Proceed to effect-blind finite stability; keep source effects and physics claims closed."
    elif overall == "v17c_resource_not_qualified":
        next_text = (
            "Retire full bounded-cycle enumeration as the active sampler. Do not relax the 60-second bound. The next design must avoid exhaustive exact completion over the full local support while preserving a separately auditable proposal law."
        )
        recommendation = "Retire exhaustive bounded-cycle enumeration as the active sampler."
    else:
        next_text = (
            "Stop at the first failed equivalence, reversibility or movement layer. Repair instrumentation without inspecting source spectrum or observed effect, then preregister a replacement gate."
        )
        recommendation = "Stop and repair the first failed frozen layer."
    NEXT_DIRECTION.write_text(
        f"# v17c next direction\n\nFormal status: `{overall}`.\n\n{next_text}\n",
        encoding="utf-8",
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.17c\n\n"
        f"- status: `{overall}`\n"
        f"- next: {recommendation}\n"
        "- claim ceiling: exact finite implementation/runtime qualification, not global sampling or physics\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf v0.17c for ikke-spesialister\n\n"
        "V17c endrer ikke hvilke graf-flytt som kan velges. Den teller de samme mulighetene uten aa lagre hele listen, og bruker ett tilfeldig nummer til aa velge samme plass i den samme rekkefolgen. Dermed kan vi kreve noyaktig samme kjede som i v17b og maale bare tidsgevinsten.\n\n"
        f"Statusen er `{overall}`. En bestaa-status kvalifiserer bare denne endelige algoritmen for neste stabilitetstest. Den er ikke bevis for kvantefysikk, romtid eller et univers.\n",
        encoding="utf-8",
    )


def run() -> None:
    verify_frozen_sources()
    install_optimized_constructor()
    frozen_digests = v16z.frozen_start_digests()
    baseline_digests = baseline_transition_digests()
    traces: List[Dict[str, Any]] = []
    parity: List[Dict[str, Any]] = []
    reversibility: List[Dict[str, Any]] = []
    representations: List[Dict[str, Any]] = []
    transitions: List[Dict[str, Any]] = []
    transition_digests: Dict[Tuple[int, int, str, str], str] = {}
    digest_passes_by_source: Dict[Tuple[int, int], int] = {}

    for run_index, (dag, metadata) in enumerate(load_runs(), start=1):
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        kernel = v17a.build_kernel(space)
        starts = {
            "source_assignment": space.source_edges,
            "v16x_random_cost_a0": v16z.random_cost_start(dag, space),
        }
        digest_passes = 0
        for start_family, start in starts.items():
            frozen = frozen_digests[(dag.growth_seed, dag.run_offset, start_family)]
            digest_passes += int(v16x.edge_digest(start) == frozen)
            parity.extend(counter_parity_rows(dag, kernel, start, start_family))
            representations.append(v17b.representation_row(
                dag, metadata, space, start, start_family
            ))
            reversibility.extend(v17b.reversibility_rows(
                dag, kernel, start, start_family
            ))
            for seed_family in CHAIN_SEED_FAMILIES:
                result = v17b.run_chain(
                    dag, kernel, start, start_family, seed_family
                )
                result.stats["transition_sha256"] = result.transition_digest
                traces.extend(result.trace)
                transitions.append(dict(result.stats))
                transition_digests[(
                    dag.growth_seed, dag.run_offset, start_family, seed_family
                )] = result.transition_digest
        digest_passes_by_source[(dag.growth_seed, dag.run_offset)] = digest_passes
        print(f"[v17c] sources={run_index}/6")

    paired = paired_runtime_rows(transitions, baseline_digests)
    summaries = []
    for dag, _ in load_runs():
        source_key = (dag.growth_seed, dag.run_offset)
        source_parity = [row for row in parity if (int(row["growth_seed"]), int(row["run_offset"])) == source_key]
        source_representation = [row for row in representations if (int(row["growth_seed"]), int(row["run_offset"])) == source_key]
        source_reversibility = [row for row in reversibility if (int(row["growth_seed"]), int(row["run_offset"])) == source_key]
        source_transitions = [row for row in transitions if (int(row["growth_seed"]), int(row["run_offset"])) == source_key]
        source_paired = [row for row in paired if (int(row["growth_seed"]), int(row["run_offset"])) == source_key]
        parity_passes = sum(int(row["support_parity_pass"]) for row in source_parity)
        representation_passes = sum(int(row["representation_pass"]) for row in source_representation)
        reversibility_passes = sum(int(row["pathwise_detailed_balance_pass"]) for row in source_reversibility)
        replay_passes = sum(int(row["exact_transition_replay_pass"]) for row in source_paired)
        movement_passes = sum(int(row["movement_pass"]) for row in source_transitions)
        resource_passes = sum(int(row["resource_pass"]) for row in source_transitions)
        source_pass = all((
            digest_passes_by_source[source_key] == 2,
            parity_passes == 6,
            representation_passes == 2,
            reversibility_passes == 6,
            replay_passes == 4,
            movement_passes == 4,
            resource_passes == 4,
        ))
        summaries.append({
            **dag.prefix,
            "frozen_start_digest_passes": digest_passes_by_source[source_key],
            "counter_parity_passes": parity_passes,
            "representation_passes": representation_passes,
            "reversibility_passes": reversibility_passes,
            "exact_replay_passes": replay_passes,
            "movement_passes": movement_passes,
            "resource_passes": resource_passes,
            "minimum_valid_proposals": min(int(row["valid_proposals"]) for row in source_transitions),
            "minimum_accepted_cycles": min(int(row["accepted_cycles"]) for row in source_transitions),
            "minimum_final_start_changed_edge_fraction": min(float(row["final_start_changed_edge_fraction"]) for row in source_transitions),
            "maximum_chain_seconds": max(float(row["elapsed_seconds"]) for row in source_transitions),
            "source_qualification_pass": int(source_pass),
        })

    calls = implementation_call_counts()
    exclusion_pass = (
        calls == {"spectrum_calls": 0, "effect_metric_calls": 0}
        and all(int(row["source_spectrum_computed"]) == 0 for row in traces)
        and all(int(row["observed_effect_computed"]) == 0 for row in traces)
    )
    digest_count = sum(int(row["frozen_start_digest_passes"]) for row in summaries)
    parity_count = sum(int(row["support_parity_pass"]) for row in parity)
    representation_count = sum(int(row["representation_pass"]) for row in representations)
    reverse_count = sum(int(row["reverse_support_pass"]) for row in reversibility)
    balance_count = sum(int(row["pathwise_detailed_balance_pass"]) for row in reversibility)
    replay_count = sum(int(row["exact_transition_replay_pass"]) for row in paired)
    summary_parity_count = sum(int(row["summary_parity_pass"]) for row in paired)
    movement_count = sum(int(row["movement_pass"]) for row in transitions)
    resource_count = sum(int(row["resource_pass"]) for row in transitions)

    if not exclusion_pass or digest_count != 12:
        overall = "v17c_instrumentation_failed"
    elif parity_count != 36:
        overall = "v17c_counter_parity_not_qualified"
    elif replay_count != 24 or summary_parity_count != 24:
        overall = "v17c_transition_equivalence_not_qualified"
    elif representation_count != 12:
        overall = "v17c_representation_not_qualified"
    elif reverse_count != 36 or balance_count != 36:
        overall = "v17c_reversibility_not_qualified"
    elif movement_count != 24:
        overall = "v17c_finite_movement_not_qualified"
    elif resource_count != 24:
        overall = "v17c_resource_not_qualified"
    else:
        overall = "v17c_exact_counter_runtime_qualified"

    gates = [
        {"gate": "effect_blind_integrity", "status": "pass" if exclusion_pass else "fail", "observed": f"spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}", "required": "0;0", "decision": "continue" if exclusion_pass else "invalidate"},
        {"gate": "frozen_start_replay", "status": "pass" if digest_count == 12 else "fail", "observed": f"{digest_count}/12", "required": "12/12", "decision": "continue" if digest_count == 12 else "invalidate"},
        {"gate": "exact_counter_support_parity", "status": "pass" if parity_count == 36 else "fail", "observed": f"{parity_count}/36", "required": "36/36", "decision": "continue" if parity_count == 36 else "repair_counter"},
        {"gate": "exact_v17b_transition_replay", "status": "pass" if replay_count == summary_parity_count == 24 else "fail", "observed": f"trace={replay_count}/24;summary={summary_parity_count}/24", "required": "24/24;24/24", "decision": "continue" if replay_count == summary_parity_count == 24 else "reject_implementation_change"},
        {"gate": "representation_covariance", "status": "pass" if representation_count == 12 else "fail", "observed": f"{representation_count}/12", "required": "12/12", "decision": "continue" if representation_count == 12 else "repair_representation"},
        {"gate": "exact_reverse_support", "status": "pass" if reverse_count == 36 else "fail", "observed": f"{reverse_count}/36", "required": "36/36", "decision": "continue" if reverse_count == 36 else "repair_constructor"},
        {"gate": "pathwise_detailed_balance", "status": "pass" if balance_count == 36 else "fail", "observed": f"{balance_count}/36", "required": "36/36", "decision": "continue" if balance_count == 36 else "repair_probability"},
        {"gate": "finite_movement", "status": "pass" if movement_count == 24 else "fail", "observed": f"{movement_count}/24", "required": "24/24", "decision": "continue" if movement_count == 24 else "reject_implementation_change"},
        {"gate": "resource_bound", "status": "pass" if resource_count == 24 else "fail", "observed": f"{resource_count}/24", "required": "24/24", "decision": "continue" if resource_count == 24 else "retire_full_bounded_cycle_enumeration"},
        {"gate": "v17c_overall", "status": overall, "observed": f"exclusion={int(exclusion_pass)};starts={digest_count}/12;counter={parity_count}/36;replay={replay_count}/24;representation={representation_count}/12;reverse={reverse_count}/36;balance={balance_count}/36;movement={movement_count}/24;resource={resource_count}/24", "required": "1;12/12;36/36;24/24;12/12;36/36;36/36;24/24;24/24", "decision": overall},
    ]
    claims = [
        {"claim_id": "C1", "claim": "v17c computes no source spectrum or observed-effect statistic.", "status": "supported" if exclusion_pass else "not_supported", "evidence": "effect-blind implementation audit and trace", "scope_limit": "static and runtime exclusion for this script"},
        {"claim_id": "C2", "claim": "The exact counter has the same ordered completion support as v17b on all frozen witness cells.", "status": "supported" if parity_count == 36 else "not_supported", "evidence": "v17c_counter_parity_audit.csv", "scope_limit": "36 finite start/length cells"},
        {"claim_id": "C3", "claim": "v17c exactly replays the frozen v17b transition paths.", "status": "supported" if replay_count == summary_parity_count == 24 else "not_supported", "evidence": "v17c_paired_v17b_runtime.csv", "scope_limit": "24 frozen 512-step chains"},
        {"claim_id": "C4", "claim": "The exact counter qualifies the frozen finite movement and runtime gates.", "status": "supported" if movement_count == resource_count == 24 else "not_supported", "evidence": "v17c_chain_transition_summary.csv", "scope_limit": "24 finite chains on six reused spaces"},
        {"claim_id": "C5", "claim": "The v17c kernel is globally irreducible, mixed, or uniform over the full feasible space.", "status": "unsupported", "evidence": "none", "scope_limit": "target remains component-uniform only"},
        {"claim_id": "C6", "claim": "The v16s spectrum contrast survives v17c or v17c exhibits Bell correlations.", "status": "not_tested", "evidence": "spectrum/effect calls prohibited; Bell observables absent", "scope_limit": "requires later qualified gates"},
    ]

    v16i.write_csv(COUNTER_PARITY_AUDIT, parity)
    v16i.write_csv(PROPOSAL_TRACE, traces)
    v16i.write_csv(REVERSIBILITY_AUDIT, reversibility)
    v16i.write_csv(REPRESENTATION_AUDIT, representations)
    v16i.write_csv(TRANSITION_SUMMARY, transitions)
    v16i.write_csv(PAIRED_RUNTIME, paired)
    v16i.write_csv(SOURCE_SUMMARY, summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    write_documents(overall, gates, summaries, transitions, paired)
    print(f"[v17c] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    parity = v16i.read_csv(COUNTER_PARITY_AUDIT)
    trace = v16i.read_csv(PROPOSAL_TRACE)
    reversibility = v16i.read_csv(REVERSIBILITY_AUDIT)
    representations = v16i.read_csv(REPRESENTATION_AUDIT)
    transitions = v16i.read_csv(TRANSITION_SUMMARY)
    paired = v16i.read_csv(PAIRED_RUNTIME)
    summaries = v16i.read_csv(SOURCE_SUMMARY)
    gates = v16i.read_csv(GATE_EVALUATION)
    claims = v16i.read_csv(CLAIM_LEDGER)
    if len(parity) != 36 or len(trace) != 24 * TOTAL_STEPS:
        raise ValueError("v17c parity/trace row count failed")
    if len(reversibility) != 36 or len(representations) != 12:
        raise ValueError("v17c reversibility/representation row count failed")
    if len(transitions) != 24 or len(paired) != 24 or len(summaries) != 6:
        raise ValueError("v17c transition/comparison/source row count failed")
    if len(gates) != 10 or len(claims) != 6:
        raise ValueError("v17c gate/claim row count failed")
    if implementation_call_counts() != {"spectrum_calls": 0, "effect_metric_calls": 0}:
        raise ValueError("v17c effect exclusion failed")
    if any(int(row["source_spectrum_computed"]) for row in trace):
        raise ValueError("v17c trace contains source spectrum")
    if any(int(row["observed_effect_computed"]) for row in trace):
        raise ValueError("v17c trace contains observed effect")
    overall = next(row["status"] for row in gates if row["gate"] == "v17c_overall")
    allowed = {
        "v17c_instrumentation_failed",
        "v17c_counter_parity_not_qualified",
        "v17c_transition_equivalence_not_qualified",
        "v17c_representation_not_qualified",
        "v17c_reversibility_not_qualified",
        "v17c_finite_movement_not_qualified",
        "v17c_resource_not_qualified",
        "v17c_exact_counter_runtime_qualified",
    }
    if overall not in allowed:
        raise ValueError("v17c overall status is unknown")
    for path in (REPORT, INTERPRETATION, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"v17c documentation missing: {path.name}")
    print(f"[v17c] output verification pass overall={overall}")


def synthetic_space() -> Tuple[v16x.StateSpace, frozenset[Edge]]:
    role = ("test", ("resource",))
    slot_class = (role, 0, "witness")
    parents = (0, 1, 2, 3)
    children = (10, 11, 12, 13)
    candidates = tuple((parent, child) for parent in parents for child in children)
    source = frozenset(zip(parents, children))
    return v16x.StateSpace(
        arm="test",
        candidates=candidates,
        source_edges=source,
        slot_by_edge={edge: (edge[1], slot_class) for edge in candidates},
        parent_demands={parent: 1 for parent in parents},
        slot_demands={(child, slot_class): 1 for child in children},
        edge_count=4,
    ), source


def self_test() -> None:
    space, source = synthetic_space()
    kernel = v17a.build_kernel(space)
    for cycle_length in EXACT_LENGTH_CHOICES:
        for first in sorted(source):
            baseline = v17b.residual_cycle_sequences(
                kernel, source, first, cycle_length
            )
            counter = ExactResidualCounter(kernel, source, first, cycle_length)
            if counter.count() != len(baseline):
                raise AssertionError("v17c synthetic completion count parity failed")
            for rank, sequence in enumerate(baseline):
                if not counter.supports(sequence) or counter.sample(rank) != sequence:
                    raise AssertionError("v17c synthetic ordered support parity failed")
                baseline_aux = v17b.path_probability(kernel, source, sequence)
                optimized_aux = path_probability(kernel, source, sequence)
                if baseline_aux is None or optimized_aux is None:
                    raise AssertionError("v17c synthetic path support missing")
                if baseline_aux.probability != optimized_aux.probability:
                    raise AssertionError("v17c synthetic path probability parity failed")
    if implementation_call_counts() != {"spectrum_calls": 0, "effect_metric_calls": 0}:
        raise AssertionError("v17c effect exclusion audit failed")
    print("[v17c] self-test pass")


def pilot() -> None:
    install_optimized_constructor()
    dag, metadata = load_runs()[0]
    space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
    result = v17b.run_chain(
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
    parser = argparse.ArgumentParser(description="v17c exact-counter runtime qualification")
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
