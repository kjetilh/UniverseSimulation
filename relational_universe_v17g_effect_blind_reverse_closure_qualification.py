#!/usr/bin/env python3
"""v17g qualification of a reverse-closed v17f length-5 support filter.

The frozen v17f raw generator is unchanged. A generated length-5 auxiliary is
retained as a valid proposal only when its mapped reverse auxiliary is supported
under the same bounded law. Unsupported raw auxiliaries become self-loop dead
ends before valid-yield accounting. Source spectra and observed effects remain
prohibited.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import time
from typing import Any, Dict, List, Mapping, MutableMapping, Sequence, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16x_explicit_global_measure_gate as v16x
import relational_universe_v16z_alternating_cycle_bridge_gate as v16z
import relational_universe_v17a_state_independent_cycle_proposal_qualification as v17a
import relational_universe_v17f_effect_blind_length5_move_qualification as v17f
import relational_universe_v17f_postrun_reverse_closure_diagnosis as v17f_postrun


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

TOTAL_STEPS = v17f.TOTAL_STEPS
REPRESENTATION_STEPS = v17f.REPRESENTATION_STEPS
EXPECTED_FILTERED_RAW_AUXILIARIES = 11
EXPECTED_TRACE_ROWS = 24 * TOTAL_STEPS

SOURCE_CHAIN = DOC / "v17g_source_chain.csv"
PRE_REGISTRATION = DOC / "v17g_pre_registration.csv"
PROPOSAL_TRACE = DOC / "v17g_proposal_trace.csv"
REVERSIBILITY_AUDIT = DOC / "v17g_pathwise_reversibility_audit.csv"
REPRESENTATION_AUDIT = DOC / "v17g_representation_audit.csv"
PARITY_AUDIT = DOC / "v17g_v17f_transition_parity.csv"
RUNTIME_SUPPORT_AUDIT = DOC / "v17g_runtime_support_audit.csv"
TRANSITION_SUMMARY = DOC / "v17g_chain_transition_summary.csv"
SOURCE_SUMMARY = DOC / "v17g_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v17g_gate_evaluation.csv"
GOAL_EVALUATION = DOC / "v17g_goal_evaluation.csv"
CLAIM_LEDGER = DOC / "v17g_claim_ledger.csv"
REPORT = DOC / "v17g_effect_blind_reverse_closure_qualification.md"
INTERPRETATION = DOC / "v17g_interpretation_audit.md"
NEXT_DIRECTION = DOC / "v17g_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_17g_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_17g.md"

Edge = v16x.Edge
CycleKernel = v17f.CycleKernel
ExpandedAuxiliary = v17f.ExpandedAuxiliary


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    runs = []
    for source, metadata in v17f.load_runs():
        runs.append((v16i.RunDAG(
            stage="v17g",
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
        raise ValueError("v17g requires six frozen v17f source spaces")
    return runs


def chain_key(row: Mapping[str, Any]) -> Tuple[int, int, str, str]:
    return (
        int(row["growth_seed"]),
        int(row["run_offset"]),
        str(row["start_family"]),
        str(row["chain_seed_family"]),
    )


def trace_groups(path: Path) -> Dict[Tuple[int, int, str, str], List[Dict[str, str]]]:
    groups: Dict[Tuple[int, int, str, str], List[Dict[str, str]]] = {}
    for row in v16i.read_csv(path):
        groups.setdefault(chain_key(row), []).append(row)
    for rows in groups.values():
        rows.sort(key=lambda row: int(row["step"]))
    return groups


def summary_map(path: Path) -> Dict[Tuple[int, int, str, str], Dict[str, str]]:
    return {chain_key(row): row for row in v16i.read_csv(path)}


def accepted_digest(trace: Sequence[Mapping[str, Any]]) -> str:
    payload = [
        {
            "step": int(row["step"]),
            "proposal": str(row["proposal_sha256"]),
            "after": str(row["state_after_sha256"]),
        }
        for row in trace
        if str(row["event"]) == "accepted_cycle"
    ]
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def run_chain(
    dag: v16i.RunDAG,
    kernel: CycleKernel,
    start: frozenset[Edge],
    start_family: str,
    seed_family: str,
    *,
    total_steps: int = TOTAL_STEPS,
) -> Tuple[frozenset[Edge], MutableMapping[str, Any], List[Dict[str, Any]]]:
    seed = v17f.chain_seed(dag, start_family, seed_family)
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
        reverse_filtered = False
        before_digest = v16x.edge_digest(selected)

        if rng.getrandbits(1):
            counts["nonlazy_steps"] += 1
            auxiliary = v17f.propose_expanded(kernel, selected, rng)
            if auxiliary is None:
                event = "proposal_dead_end"
                counts["proposal_dead_end"] += 1
            else:
                counts["raw_proposals"] += 1
                proposed = v17a.apply_proposal(kernel.space, selected, auxiliary.proposal)
                reverse = v17f.reverse_expanded(kernel, proposed, auxiliary)
                if reverse is None:
                    event = "reverse_filtered_dead_end"
                    reverse_filtered = True
                    counts["reverse_filtered_dead_end"] += 1
                    counts["proposal_dead_end"] += 1
                else:
                    recovered = v17a.apply_proposal(
                        kernel.space, proposed, reverse.proposal
                    )
                    if recovered != selected:
                        raise ValueError("v17g reverse auxiliary did not recover state")
                    counts["valid_proposals"] += 1
                    counts[f"valid_{auxiliary.move_class}"] += 1
                    counts["retained_reverse_supported"] += 1
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
            "first_batch_json": json.dumps(
                auxiliary.first_batch, separators=(",", ":")
            ) if auxiliary and auxiliary.first_batch else "[]",
            "eligible_first_count": auxiliary.eligible_first_count if auxiliary else 0,
            "search_states": auxiliary.search_states if auxiliary else 0,
            "search_budget_exhaustions": (
                auxiliary.search_budget_exhaustions if auxiliary else 0
            ),
            "raw_proposal_generated": int(auxiliary is not None),
            "retained_valid_proposal": int(auxiliary is not None and reverse is not None),
            "reverse_filtered_dead_end": int(reverse_filtered),
            "remove_edges_json": json.dumps(
                proposal.remove, separators=(",", ":")
            ) if proposal else "[]",
            "add_edges_json": json.dumps(
                proposal.add, separators=(",", ":")
            ) if proposal else "[]",
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
    retained_support_pass = (
        counts["valid_proposals"] == counts["retained_reverse_supported"]
    )
    movement_pass = all((
        counts["valid_proposals"] >= v17f.MIN_VALID_PROPOSALS_PER_CHAIN,
        counts["accepted_cycles"] >= v17f.MIN_ACCEPTED_CYCLES_PER_CHAIN,
        counts["accepted_length_2_4"] >= v17f.MIN_ACCEPTED_OLD_CYCLES_PER_CHAIN,
        counts["accepted_length_5_batch_guided"]
        >= v17f.MIN_ACCEPTED_LENGTH5_CYCLES_PER_CHAIN,
        len(visited) >= v17f.MIN_UNIQUE_STATES_PER_CHAIN,
        final_change >= v17f.MIN_FINAL_START_CHANGE,
        retained_support_pass,
        v16x.assignment_integrity(kernel.space, selected),
    ))
    stats: MutableMapping[str, Any] = {
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
        "raw_proposals": counts["raw_proposals"],
        "reverse_filtered_dead_end": counts["reverse_filtered_dead_end"],
        "valid_proposals": counts["valid_proposals"],
        "valid_old_cycles": counts["valid_length_2_4"],
        "valid_length5_cycles": counts["valid_length_5_batch_guided"],
        "retained_reverse_supported": counts["retained_reverse_supported"],
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
        "minimum_valid_proposals": v17f.MIN_VALID_PROPOSALS_PER_CHAIN,
        "minimum_accepted_cycles": v17f.MIN_ACCEPTED_CYCLES_PER_CHAIN,
        "minimum_accepted_old_cycles": v17f.MIN_ACCEPTED_OLD_CYCLES_PER_CHAIN,
        "minimum_accepted_length5_cycles": v17f.MIN_ACCEPTED_LENGTH5_CYCLES_PER_CHAIN,
        "minimum_unique_states": v17f.MIN_UNIQUE_STATES_PER_CHAIN,
        "minimum_final_start_change": v17f.MIN_FINAL_START_CHANGE,
        "maximum_chain_seconds": v17f.MAX_CHAIN_SECONDS,
        "final_assignment_integrity_pass": int(
            v16x.assignment_integrity(kernel.space, selected)
        ),
        "retained_reverse_support_pass": int(retained_support_pass),
        "resource_pass": int(elapsed <= v17f.MAX_CHAIN_SECONDS),
        "movement_pass": int(movement_pass),
        "accepted_transition_sha256": accepted_digest(trace),
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }
    return selected, stats, trace


def parity_row(
    stats: Mapping[str, Any],
    trace: Sequence[Mapping[str, Any]],
    old_summary: Mapping[str, str],
    old_trace: Sequence[Mapping[str, str]],
) -> Dict[str, Any]:
    if len(trace) != len(old_trace):
        raise ValueError("v17g/v17f trace length mismatch")
    raw_fields = (
        "step", "move_class", "cycle_length", "proposal_sha256",
        "first_batch_json", "eligible_first_count", "search_states",
        "search_budget_exhaustions", "remove_edges_json", "add_edges_json",
        "q_forward_numerator", "q_forward_denominator",
        "state_before_sha256", "state_after_sha256",
    )
    raw_passes = 0
    event_passes = 0
    filtered_old = []
    filtered_new = []
    for new, old in zip(trace, old_trace):
        raw_passes += int(all(str(new[field]) == str(old[field]) for field in raw_fields))
        expected_event = (
            "reverse_filtered_dead_end"
            if old["event"] == "reverse_unsupported"
            else old["event"]
        )
        event_passes += int(str(new["event"]) == expected_event)
        if old["event"] == "reverse_unsupported":
            filtered_old.append((old["step"], old["proposal_sha256"]))
        if int(new["reverse_filtered_dead_end"]):
            filtered_new.append((str(new["step"]), str(new["proposal_sha256"])))

    old_accepted = accepted_digest(old_trace)
    new_accepted = accepted_digest(trace)
    old_valid = int(old_summary["valid_proposals"])
    old_unsupported = int(old_summary["reverse_unsupported"])
    old_dead = int(old_summary["proposal_dead_end"])
    count_relation = all((
        int(stats["valid_proposals"]) == old_valid - old_unsupported,
        int(stats["proposal_dead_end"]) == old_dead + old_unsupported,
        int(stats["reverse_filtered_dead_end"]) == old_unsupported,
        int(stats["accepted_cycles"]) == int(old_summary["accepted_cycles"]),
        int(stats["accepted_edge_work"]) == int(old_summary["accepted_edge_work"]),
        int(stats["unique_state_count"]) == int(old_summary["unique_state_count"]),
    ))
    return {
        "stage": "v17g",
        "growth_seed": stats["growth_seed"],
        "run_offset": stats["run_offset"],
        "start_family": stats["start_family"],
        "chain_seed_family": stats["chain_seed_family"],
        "trace_rows": len(trace),
        "raw_generation_parity_rows": raw_passes,
        "expected_raw_generation_parity_rows": len(trace),
        "event_reclassification_parity_rows": event_passes,
        "expected_event_reclassification_parity_rows": len(trace),
        "v17f_reverse_unsupported": old_unsupported,
        "v17g_reverse_filtered_dead_end": stats["reverse_filtered_dead_end"],
        "filtered_auxiliary_identity_pass": int(filtered_old == filtered_new),
        "count_relation_pass": int(count_relation),
        "accepted_transition_parity_pass": int(old_accepted == new_accepted),
        "final_endpoint_parity_pass": int(
            str(stats["final_endpoint_sha256"])
            == old_summary["final_endpoint_sha256"]
        ),
        "v17f_accepted_transition_sha256": old_accepted,
        "v17g_accepted_transition_sha256": new_accepted,
        "v17f_final_endpoint_sha256": old_summary["final_endpoint_sha256"],
        "v17g_final_endpoint_sha256": stats["final_endpoint_sha256"],
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }


def representation_row(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    space: v16x.StateSpace,
    start: frozenset[Edge],
    start_family: str,
) -> Dict[str, Any]:
    def execute(target_space: v16x.StateSpace) -> Tuple[str, str]:
        final, stats, _ = run_chain(
            dag,
            v17a.build_kernel(target_space),
            start,
            start_family,
            "representation_seed",
            total_steps=REPRESENTATION_STEPS,
        )
        return v16x.edge_digest(final), str(stats["accepted_transition_sha256"])

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
        v16i.stable_seed("v17g", "semantic_relabel", start_family, *dag.key),
    )
    relabeled_space = v16x.build_state_space(dag, relabeled_metadata, v16x.COARSE_ARM)
    relabeled = execute(relabeled_space)
    candidate_pass = set(space.candidates) == set(relabeled_space.candidates)
    replay_pass = original == replay
    order_pass = original == reordered
    relabel_pass = original == relabeled
    return {
        **dag.prefix,
        "start_family": start_family,
        "check_steps": REPRESENTATION_STEPS,
        "original_endpoint_sha256": original[0],
        "replay_endpoint_sha256": replay[0],
        "reordered_endpoint_sha256": reordered[0],
        "relabeled_endpoint_sha256": relabeled[0],
        "original_accepted_transition_sha256": original[1],
        "replay_accepted_transition_sha256": replay[1],
        "reordered_accepted_transition_sha256": reordered[1],
        "relabeled_accepted_transition_sha256": relabeled[1],
        "candidate_set_covariance_pass": int(candidate_pass),
        "exact_replay_pass": int(replay_pass),
        "candidate_order_covariance_pass": int(order_pass),
        "semantic_relabel_covariance_pass": int(relabel_pass),
        "representation_pass": int(all((
            candidate_pass, replay_pass, order_pass, relabel_pass
        ))),
    }


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v17f", "frozen_generator", v17f.SCRIPT),
        ("v17f", "frozen_preregistration", v17f.PRE_REGISTRATION),
        ("v17f", "frozen_formal_trace", v17f.PROPOSAL_TRACE),
        ("v17f", "frozen_transition_summary", v17f.TRANSITION_SUMMARY),
        ("v17f", "formal_gate", v17f.GATE_EVALUATION),
        ("v17f", "postrun_failure_localization", v17f_postrun.DETAIL),
        ("v17f", "next_direction", v17f.NEXT_DIRECTION),
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
        "gate": "v17g_effect_blind_reverse_closure_qualification",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_probability_support_repair_only",
        "source_history_count": 6,
        "start_families": list(v17f.START_FAMILIES),
        "chain_seed_families": list(v17f.CHAIN_SEED_FAMILIES),
        "raw_generator": "exact_v17f_half_old_half_length5_generator",
        "support_filter": "mapped_reverse_supported_under_same_bounded_law",
        "filtered_auxiliary_treatment": "self_loop_before_valid_accounting",
        "new_random_draws": 0,
        "new_cycle_length": v17f.NEW_CYCLE_LENGTH,
        "first_batch_size": v17f.FIRST_BATCH_SIZE,
        "maximum_search_states_per_guide": v17f.MAX_SEARCH_STATES_PER_GUIDE,
        "total_steps": TOTAL_STEPS,
        "representation_steps": REPRESENTATION_STEPS,
        "expected_trace_rows": EXPECTED_TRACE_ROWS,
        "expected_filtered_raw_auxiliaries": EXPECTED_FILTERED_RAW_AUXILIARIES,
        "required_raw_generation_parity_rows": EXPECTED_TRACE_ROWS,
        "required_filtered_identity": EXPECTED_FILTERED_RAW_AUXILIARIES,
        "required_accepted_transition_parity": 24,
        "required_final_endpoint_parity": 24,
        "required_retained_reverse_support": 24,
        "required_representation_passes": 12,
        "required_movement_passes": 24,
        "required_resource_passes": 24,
        "success_decision": "preregister_v17h_matched_accepted_edge_work_start_memory",
        "failure_decision": "retire_bounded_search_length5_law",
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "not_claimed": [
            "new_dynamical_result", "connectivity", "irreducibility", "mixing",
            "convergence", "source_effect", "energy", "temperature", "dimension",
            "Lorentz_symmetry", "spacetime", "particles", "Bell_correlation",
            "entanglement", "universe_model",
        ],
    }


def spec_digest() -> str:
    return hashlib.sha256(json.dumps(
        spec_payload(), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()


def preregistration_row() -> Dict[str, Any]:
    return {
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "script_sha256": file_sha256(SCRIPT),
        "source_chain_sha256": file_sha256(SOURCE_CHAIN),
        "source_history_count": 6,
        "total_steps": TOTAL_STEPS,
        "expected_trace_rows": EXPECTED_TRACE_ROWS,
        "expected_filtered_raw_auxiliaries": EXPECTED_FILTERED_RAW_AUXILIARIES,
        "new_cycle_length": v17f.NEW_CYCLE_LENGTH,
        "first_batch_size": v17f.FIRST_BATCH_SIZE,
        "maximum_search_states_per_guide": v17f.MAX_SEARCH_STATES_PER_GUIDE,
        "required_raw_generation_parity_rows": EXPECTED_TRACE_ROWS,
        "required_accepted_transition_parity": 24,
        "required_final_endpoint_parity": 24,
        "required_retained_reverse_support": 24,
        "required_representation_passes": 12,
        "required_movement_passes": 24,
        "required_resource_passes": 24,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v17f.verify_outputs()
    v17f_postrun.verify_outputs()
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v17g] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    rows = v16i.read_csv(PRE_REGISTRATION)
    expected = {key: str(value) for key, value in preregistration_row().items()}
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v17g preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v17g frozen source chain changed")


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


def gate_rows(
    traces: Sequence[Mapping[str, Any]],
    transitions: Sequence[Mapping[str, Any]],
    parity: Sequence[Mapping[str, Any]],
    reversibility: Sequence[Mapping[str, Any]],
    representations: Sequence[Mapping[str, Any]],
) -> Tuple[str, List[Dict[str, Any]]]:
    calls = implementation_call_counts()
    exclusion = calls == {"spectrum_calls": 0, "effect_metric_calls": 0}
    raw_parity = sum(
        int(row["raw_generation_parity_rows"])
        for row in parity
    )
    event_parity = sum(
        int(row["event_reclassification_parity_rows"])
        for row in parity
    )
    filtered = sum(int(row["v17g_reverse_filtered_dead_end"]) for row in parity)
    filtered_identity = sum(int(row["filtered_auxiliary_identity_pass"]) for row in parity)
    count_relation = sum(int(row["count_relation_pass"]) for row in parity)
    accepted_parity = sum(int(row["accepted_transition_parity_pass"]) for row in parity)
    endpoint_parity = sum(int(row["final_endpoint_parity_pass"]) for row in parity)
    retained_support = sum(int(row["retained_reverse_support_pass"]) for row in transitions)
    representation = sum(int(row["representation_pass"]) for row in representations)
    reverse_witness = sum(
        int(row["reverse_support_pass"])
        and int(row["reverse_recovery_pass"])
        and int(row["pathwise_detailed_balance_pass"])
        for row in reversibility
    )
    movement = sum(int(row["movement_pass"]) for row in transitions)
    resource = sum(int(row["resource_pass"]) for row in transitions)
    all_pass = all((
        exclusion,
        len(traces) == EXPECTED_TRACE_ROWS,
        raw_parity == EXPECTED_TRACE_ROWS,
        event_parity == EXPECTED_TRACE_ROWS,
        filtered == EXPECTED_FILTERED_RAW_AUXILIARIES,
        filtered_identity == 24,
        count_relation == 24,
        accepted_parity == 24,
        endpoint_parity == 24,
        retained_support == 24,
        reverse_witness == 12,
        representation == 12,
        movement == 24,
        resource == 24,
    ))
    overall = (
        "v17g_reverse_closed_length5_move_qualified"
        if all_pass
        else "v17g_reverse_closure_not_qualified"
    )
    rows = [
        {"gate": "effect_blind_integrity", "status": "pass" if exclusion else "fail", "observed": f"spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}", "required": "0;0", "decision": "continue" if exclusion else "stop"},
        {"gate": "raw_generation_and_event_parity", "status": "pass" if raw_parity == EXPECTED_TRACE_ROWS and event_parity == EXPECTED_TRACE_ROWS else "fail", "observed": f"raw={raw_parity}/{EXPECTED_TRACE_ROWS};event={event_parity}/{EXPECTED_TRACE_ROWS}", "required": f"{EXPECTED_TRACE_ROWS}/{EXPECTED_TRACE_ROWS};{EXPECTED_TRACE_ROWS}/{EXPECTED_TRACE_ROWS}", "decision": "continue" if raw_parity == EXPECTED_TRACE_ROWS and event_parity == EXPECTED_TRACE_ROWS else "repair"},
        {"gate": "filtered_auxiliary_identity", "status": "pass" if filtered == 11 and filtered_identity == 24 and count_relation == 24 else "fail", "observed": f"filtered={filtered};identity={filtered_identity}/24;counts={count_relation}/24", "required": "11;24/24;24/24", "decision": "continue" if filtered == 11 and filtered_identity == 24 and count_relation == 24 else "repair"},
        {"gate": "accepted_transition_and_endpoint_parity", "status": "pass" if accepted_parity == 24 and endpoint_parity == 24 else "fail", "observed": f"accepted={accepted_parity}/24;endpoint={endpoint_parity}/24", "required": "24/24;24/24", "decision": "continue" if accepted_parity == 24 and endpoint_parity == 24 else "retire"},
        {"gate": "retained_reverse_support_and_balance", "status": "pass" if retained_support == 24 and reverse_witness == 12 else "fail", "observed": f"runtime={retained_support}/24;witness={reverse_witness}/12", "required": "24/24;12/12", "decision": "continue" if retained_support == 24 and reverse_witness == 12 else "retire"},
        {"gate": "representation_covariance", "status": "pass" if representation == 12 else "fail", "observed": f"{representation}/12", "required": "12/12", "decision": "continue" if representation == 12 else "repair"},
        {"gate": "finite_movement_and_resource", "status": "pass" if movement == 24 and resource == 24 else "fail", "observed": f"movement={movement}/24;resource={resource}/24", "required": "24/24;24/24", "decision": "continue" if movement == 24 and resource == 24 else "retire"},
        {"gate": "v17g_overall", "status": overall, "observed": f"raw={raw_parity};filtered={filtered};accepted={accepted_parity}/24;endpoint={endpoint_parity}/24;support={retained_support}/24;representation={representation}/12;movement={movement}/24;resource={resource}/24", "required": f"raw={EXPECTED_TRACE_ROWS};filtered=11;accepted=24/24;endpoint=24/24;support=24/24;representation=12/12;movement=24/24;resource=24/24", "decision": overall},
    ]
    return overall, rows


def markdown_table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    return v17f.markdown_table(rows, fields)


def write_documents(
    overall: str,
    gates: Sequence[Mapping[str, Any]],
    transitions: Sequence[Mapping[str, Any]],
    parity: Sequence[Mapping[str, Any]],
) -> None:
    minimum_valid = min(int(row["valid_proposals"]) for row in transitions)
    minimum_length5 = min(int(row["accepted_length5_cycles"]) for row in transitions)
    maximum_seconds = max(float(row["elapsed_seconds"]) for row in transitions)
    filtered = sum(int(row["reverse_filtered_dead_end"]) for row in transitions)
    REPORT.write_text("\n".join([
        "# v17g effect-blind reverse-closure qualification",
        "",
        f"Status: `{overall}`.",
        "",
        "## Purpose and goal",
        "",
        "Purpose `purpose://validation`: determine whether the exact v17f raw generator can be made reverse-closed by a deterministic support filter without changing accepted dynamics. The frozen goal requires 24,576/24,576 raw-generation parity, exact identity of all 11 filtered auxiliaries, accepted-transition and endpoint parity 24/24, retained reverse support 24/24, representation 12/12, movement 24/24 and resource 24/24.",
        "",
        "## Law change",
        "",
        "The batch size, length-5 constructor, 20,000-state bounded witness law, old-kernel mixture, starts, seeds and 1024-step budget are unchanged. A raw length-5 auxiliary whose explicitly mapped reverse auxiliary is unsupported under that same bounded law becomes a self-loop before valid-proposal accounting. No extra random draw is made. Retained auxiliary probabilities and the lazy Metropolis ratio are unchanged.",
        "",
        "## Frozen gates",
        "",
        *markdown_table(gates, ("gate", "status", "observed", "required", "decision")),
        "",
        "## Finite evidence",
        "",
        f"Across 24 chains, `{filtered}` raw auxiliaries were filtered. Minimum retained valid proposals were `{minimum_valid}`, minimum accepted length-5 cycles `{minimum_length5}`, and maximum runtime `{maximum_seconds:.6f}` seconds.",
        "",
        "## Interpretation boundary",
        "",
        "This gate changes the declared proposal support and valid-yield accounting, but deliberately reproduces every accepted v17f transition. A pass is probability-law and instrumentation qualification, not new dynamical evidence, connectivity, convergence, mixing, a source effect or physics.",
        "",
    ]), encoding="utf-8")
    INTERPRETATION.write_text(
        "# v17g interpretation audit\n\n"
        f"Frozen status is `{overall}`. Reclassifying unsupported raw auxiliaries as "
        "dead ends makes zero runtime reverse-unsupported events partly definitional; the "
        "nontrivial controls are exact raw-generation parity, identity of the filtered set, "
        "retained reverse support, pathwise balance, representation covariance, and exact "
        "accepted-transition/endpoint parity. A pass is not new movement, mixing or physics.\n",
        encoding="utf-8",
    )
    if overall == "v17g_reverse_closed_length5_move_qualified":
        next_text = (
            "Preregister v17h as an effect-blind matched accepted-edge-work start-memory "
            "gate. Compare the qualified old length-2-to-4 kernel with the qualified "
            "reverse-closed expanded kernel on the same six spaces and both frozen starts. "
            "Use independent seeds, stop each arm at the same accepted removed-edge work, "
            "and make absolute cross-start distance the primary response. Keep source "
            "spectrum and observed effects closed."
        )
        recommendation = "run v17h matched accepted-edge-work start-memory gate"
    else:
        next_text = (
            "Retire the bounded-search batch-guided length-5 law. Do not increase the "
            "search or step budget and do not inspect source effects."
        )
        recommendation = "retire the bounded-search length-5 law"
    NEXT_DIRECTION.write_text(
        f"# v17g next direction\n\nFormal status: `{overall}`.\n\n{next_text}\n",
        encoding="utf-8",
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.17g\n\n"
        f"- status: `{overall}`\n"
        f"- next: {recommendation}\n"
        "- source spectrum and observed effects remain closed\n"
        "- claim ceiling: finite proposal-support qualification, not connectivity or physics\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf v0.17g for ikke-spesialister\n\n"
        "V17f fant en liten bokforingsfeil i den nye femkoblingsflytten: noen forslag kunne "
        "ikke finnes igjen baklengs innen samme avgrensede sok. V17g beholder noyaktig samme "
        "forslagsgenerator, men lar bare et forslag telle som gyldig naar den kartlagte "
        "returen ogsa finnes. Resten blir stillstand.\n\n"
        f"Statusen er `{overall}`. Selv en bestaa-status er bare en kontroll av "
        "sannsynlighetsloven. Den sier ikke at nye globale strukturer eller fysikk er funnet.\n",
        encoding="utf-8",
    )


def run() -> None:
    verify_frozen_sources()
    old_traces = trace_groups(v17f.PROPOSAL_TRACE)
    old_summaries = summary_map(v17f.TRANSITION_SUMMARY)
    frozen_starts = v16z.frozen_start_digests()
    traces: List[Dict[str, Any]] = []
    transitions: List[Dict[str, Any]] = []
    parity: List[Dict[str, Any]] = []
    support: List[Dict[str, Any]] = []
    reversibility: List[Dict[str, Any]] = []
    representations: List[Dict[str, Any]] = []
    source_summaries: List[Dict[str, Any]] = []

    for run_index, (dag, metadata) in enumerate(load_runs(), start=1):
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        kernel = v17a.build_kernel(space)
        starts = {
            "source_assignment": space.source_edges,
            "v16x_random_cost_a0": v16z.random_cost_start(dag, space),
        }
        source_transitions = []
        source_parity = []
        source_reversibility = []
        source_representations = []
        frozen_start_passes = 0
        for start_family, start in starts.items():
            frozen_start_passes += int(
                v16x.edge_digest(start)
                == frozen_starts[(dag.growth_seed, dag.run_offset, start_family)]
            )
            source_reversibility.extend(
                v17f.reversibility_rows(dag, kernel, start, start_family)
            )
            source_representations.append(
                representation_row(dag, metadata, space, start, start_family)
            )
            for seed_family in v17f.CHAIN_SEED_FAMILIES:
                final, stats, chain_trace = run_chain(
                    dag, kernel, start, start_family, seed_family
                )
                key = chain_key(stats)
                if key not in old_traces or key not in old_summaries:
                    raise ValueError(f"missing frozen v17f chain {key}")
                chain_parity = parity_row(
                    stats, chain_trace, old_summaries[key], old_traces[key]
                )
                traces.extend(chain_trace)
                source_transitions.append(dict(stats))
                source_parity.append(chain_parity)
                support.append({
                    **dag.prefix,
                    "start_family": start_family,
                    "chain_seed_family": seed_family,
                    "raw_proposals": stats["raw_proposals"],
                    "reverse_filtered_dead_end": stats["reverse_filtered_dead_end"],
                    "retained_valid_proposals": stats["valid_proposals"],
                    "retained_reverse_supported": stats["retained_reverse_supported"],
                    "retained_reverse_support_pass": stats["retained_reverse_support_pass"],
                    "accepted_transition_parity_pass": chain_parity["accepted_transition_parity_pass"],
                    "final_endpoint_parity_pass": chain_parity["final_endpoint_parity_pass"],
                    "source_spectrum_computed": 0,
                    "observed_effect_computed": 0,
                })
                if v16x.edge_digest(final) != stats["final_endpoint_sha256"]:
                    raise ValueError("v17g final endpoint digest mismatch")

        transitions.extend(source_transitions)
        parity.extend(source_parity)
        reversibility.extend(source_reversibility)
        representations.extend(source_representations)
        source_summaries.append({
            **dag.prefix,
            "frozen_start_passes": frozen_start_passes,
            "raw_generation_parity_passes": sum(
                int(row["raw_generation_parity_rows"])
                == int(row["expected_raw_generation_parity_rows"])
                for row in source_parity
            ),
            "accepted_transition_parity_passes": sum(
                int(row["accepted_transition_parity_pass"]) for row in source_parity
            ),
            "final_endpoint_parity_passes": sum(
                int(row["final_endpoint_parity_pass"]) for row in source_parity
            ),
            "retained_reverse_support_passes": sum(
                int(row["retained_reverse_support_pass"])
                for row in source_transitions
            ),
            "representation_passes": sum(
                int(row["representation_pass"]) for row in source_representations
            ),
            "movement_passes": sum(
                int(row["movement_pass"]) for row in source_transitions
            ),
            "resource_passes": sum(
                int(row["resource_pass"]) for row in source_transitions
            ),
            "filtered_raw_auxiliaries": sum(
                int(row["reverse_filtered_dead_end"]) for row in source_transitions
            ),
            "minimum_retained_valid_proposals": min(
                int(row["valid_proposals"]) for row in source_transitions
            ),
            "maximum_chain_seconds": max(
                float(row["elapsed_seconds"]) for row in source_transitions
            ),
        })
        print(f"[v17g] source {run_index}/6 complete")

    overall, gates = gate_rows(
        traces, transitions, parity, reversibility, representations
    )
    v16i.write_csv(PROPOSAL_TRACE, traces)
    v16i.write_csv(REVERSIBILITY_AUDIT, reversibility)
    v16i.write_csv(REPRESENTATION_AUDIT, representations)
    v16i.write_csv(PARITY_AUDIT, parity)
    v16i.write_csv(RUNTIME_SUPPORT_AUDIT, support)
    v16i.write_csv(TRANSITION_SUMMARY, transitions)
    v16i.write_csv(SOURCE_SUMMARY, source_summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(GOAL_EVALUATION, [{
        "goal_id": "G1",
        "purpose_ref": PURPOSE_REF,
        "metric": "parity plus reverse-support, representation, movement and resource gates",
        "baseline": "v17f had 11/720 reverse-unsupported valid length-5 auxiliaries",
        "target": "exact v17f accepted dynamics with reverse-closed retained support",
        "timeframe": "one frozen v17g round",
        "status": "satisfied" if overall == "v17g_reverse_closed_length5_move_qualified" else "missed",
        "evidence": "v17g_gate_evaluation.csv;v17g_v17f_transition_parity.csv",
    }])
    v16i.write_csv(CLAIM_LEDGER, [
        {"claim_id": "C1", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "factual", "strength": "assertive", "claim": "v17g computes no source spectrum or observed-effect metric.", "status": "supported", "evidence": "static call audit plus output exclusion fields", "scope_limit": "v17g script and outputs"},
        {"claim_id": "C2", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "project_capability", "strength": "assertive", "claim": "The reverse-closure filter preserves v17f raw generation and accepted finite dynamics.", "status": "supported" if overall == "v17g_reverse_closed_length5_move_qualified" else "not_supported", "evidence": "v17g_v17f_transition_parity.csv", "scope_limit": "24 frozen finite chains"},
        {"claim_id": "C3", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "project_capability", "strength": "moderated", "claim": "Every retained runtime auxiliary has mapped reverse support under the same bounded law.", "status": "supported" if all(int(row["retained_reverse_support_pass"]) for row in transitions) else "not_supported", "evidence": "v17g_runtime_support_audit.csv", "scope_limit": "retained auxiliaries encountered in 24 chains"},
        {"claim_id": "C4", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "causal", "strength": "speculative", "claim": "The length-5 move connects old-kernel Markov components or reduces start memory.", "status": "not_tested", "evidence": "none", "scope_limit": "requires separate matched-work gate and connectivity analysis"},
        {"claim_id": "C5", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "project_capability", "strength": "speculative", "claim": "v17g establishes source effects, mixing, Lorentz symmetry, spacetime or a universe model.", "status": "contradicted", "evidence": "effect observables prohibited; accepted dynamics intentionally unchanged", "scope_limit": "requires separate later gates"},
    ])
    write_documents(overall, gates, transitions, parity)
    print(f"[v17g] status={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    paths = (
        PROPOSAL_TRACE, REVERSIBILITY_AUDIT, REPRESENTATION_AUDIT, PARITY_AUDIT,
        RUNTIME_SUPPORT_AUDIT, TRANSITION_SUMMARY, SOURCE_SUMMARY,
        GATE_EVALUATION, GOAL_EVALUATION, CLAIM_LEDGER, REPORT,
        INTERPRETATION, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST,
    )
    if any(not path.exists() for path in paths):
        raise ValueError("v17g output missing")
    traces = v16i.read_csv(PROPOSAL_TRACE)
    transitions = v16i.read_csv(TRANSITION_SUMMARY)
    parity = v16i.read_csv(PARITY_AUDIT)
    reversibility = v16i.read_csv(REVERSIBILITY_AUDIT)
    representations = v16i.read_csv(REPRESENTATION_AUDIT)
    if (len(traces), len(transitions), len(parity), len(reversibility), len(representations)) != (
        EXPECTED_TRACE_ROWS, 24, 24, 12, 12
    ):
        raise ValueError("v17g output row count mismatch")
    overall, expected_gates = gate_rows(
        traces, transitions, parity, reversibility, representations
    )
    stored_gates = v16i.read_csv(GATE_EVALUATION)
    if stored_gates != [
        {key: str(value) for key, value in row.items()} for row in expected_gates
    ]:
        raise ValueError("v17g gate evaluation changed")
    if any(
        int(row["source_spectrum_computed"])
        or int(row["observed_effect_computed"])
        for row in traces
    ):
        raise ValueError("v17g effect exclusion failed")
    print(f"[v17g] output verification pass overall={overall}")


def self_test() -> None:
    v17f.verify_outputs()
    v17f_postrun.verify_outputs()
    dag, metadata = load_runs()[0]
    space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
    final, stats, trace = run_chain(
        dag,
        v17a.build_kernel(space),
        space.source_edges,
        "source_assignment",
        v17f.CHAIN_SEED_FAMILIES[0],
        total_steps=REPRESENTATION_STEPS,
    )
    old = trace_groups(v17f.PROPOSAL_TRACE)[chain_key(stats)][:REPRESENTATION_STEPS]
    check = parity_row(stats, trace, summary_map(v17f.TRANSITION_SUMMARY)[chain_key(stats)], old)
    if int(check["raw_generation_parity_rows"]) != REPRESENTATION_STEPS:
        raise AssertionError("v17g raw-generation self-test failed")
    if v16x.edge_digest(final) != stats["final_endpoint_sha256"]:
        raise AssertionError("v17g endpoint self-test failed")
    if implementation_call_counts() != {"spectrum_calls": 0, "effect_metric_calls": 0}:
        raise AssertionError("v17g effect exclusion self-test failed")
    print("[v17g] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif args.prepare:
        prepare()
    elif args.verify_only:
        verify_outputs()
    else:
        run()
        verify_outputs()


if __name__ == "__main__":
    main()
