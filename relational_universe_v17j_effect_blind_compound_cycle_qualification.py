#!/usr/bin/env python3
"""v17j effect-blind anchor-independent compound-cycle qualification.

Two exact state-local length-2-to-4 cycle proposals are composed into one
auxiliary-path proposal. The reverse auxiliary is the two mapped reverses in
opposite order. A symmetric endpoint filter retains only blocks changing at
least six edges; filtered paths remain self-loops and are not renormalized.
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
import relational_universe_v17c_exact_counter_runtime_qualification as v17c
import relational_universe_v17g_effect_blind_reverse_closure_qualification as v17g
import relational_universe_v17h_effect_blind_matched_work_start_memory as v17h
import relational_universe_v17i_effect_blind_cycle_basis_positive_control as v17i


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

START_FAMILIES = v17c.START_FAMILIES
CHAIN_SEED_FAMILIES = ("compound_seed_i", "compound_seed_j")
SUBCYCLE_LENGTHS = v17c.EXACT_LENGTH_CHOICES
PILOT_STEPS = 96
TOTAL_STEPS = 256
REPRESENTATION_STEPS = 48
MIN_NET_CHANGED_EDGES = 6
MIN_RETAINED_BLOCKS_PER_CHAIN = 4
MIN_ACCEPTED_BLOCKS_PER_CHAIN = 2
MIN_UNIQUE_STATES_PER_CHAIN = 3
MAX_CHAIN_SECONDS = 60.0
EXPECTED_CHAINS = 6 * 2 * 2
EXPECTED_REPRESENTATION_ROWS = 6 * 2

DESIGN_CALIBRATION = DOC / "v17j_design_calibration.csv"
SOURCE_CHAIN = DOC / "v17j_source_chain.csv"
PRE_REGISTRATION = DOC / "v17j_pre_registration.csv"
PROPOSAL_TRACE = DOC / "v17j_compound_proposal_trace.csv"
REVERSE_AUDIT = DOC / "v17j_reverse_path_audit.csv"
ENDPOINT_AUDIT = DOC / "v17j_endpoint_audit.csv"
REPRESENTATION_AUDIT = DOC / "v17j_representation_audit.csv"
TRANSITION_SUMMARY = DOC / "v17j_chain_transition_summary.csv"
SOURCE_SUMMARY = DOC / "v17j_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v17j_gate_evaluation.csv"
GOAL_EVALUATION = DOC / "v17j_goal_evaluation.csv"
CLAIM_LEDGER = DOC / "v17j_claim_ledger.csv"
REPORT = DOC / "v17j_effect_blind_compound_cycle_qualification.md"
INTERPRETATION = DOC / "v17j_interpretation_audit.md"
NEXT_DIRECTION = DOC / "v17j_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_17j_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_17j.md"

Edge = v16x.Edge
CycleKernel = v17a.CycleKernel
ResidualAuxiliary = v17c.ResidualAuxiliary


@dataclass(frozen=True)
class CompoundAuxiliary:
    first: ResidualAuxiliary
    second: ResidualAuxiliary
    probability: Fraction


@dataclass
class CompoundAttempt:
    status: str
    auxiliary: CompoundAuxiliary | None = None
    reverse: CompoundAuxiliary | None = None
    intermediate: frozenset[Edge] | None = None
    endpoint: frozenset[Edge] | None = None
    recovered: frozenset[Edge] | None = None
    reverse_again_endpoint: frozenset[Edge] | None = None
    net_changed_edges: int = 0


@dataclass
class ChainResult:
    final: frozenset[Edge]
    stats: MutableMapping[str, Any]
    trace: List[Dict[str, Any]]
    reverse_rows: List[Dict[str, Any]]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    result = []
    for source, metadata in v17h.load_runs():
        result.append((v16i.RunDAG(
            stage="v17j",
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
        raise ValueError("v17j requires six frozen source spaces")
    return result


def load_spaces() -> List[
    Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...], v16x.StateSpace, frozenset[Edge], frozenset[Edge]]
]:
    result = []
    for dag, metadata in load_runs():
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        left = space.source_edges
        right = v16z.random_cost_start(dag, space)
        result.append((dag, metadata, space, left, right))
    return result


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v17c", "exact_state_local_subcycle_kernel", v17c.SCRIPT),
        ("v17c", "qualified_exact_counter_gate", v17c.GATE_EVALUATION),
        ("v17g", "reverse_closed_length5_context", v17g.GATE_EVALUATION),
        ("v17h", "matched_work_negative_result", v17h.GATE_EVALUATION),
        ("v17h", "large_move_direction", v17h.NEXT_DIRECTION),
        ("v17i", "pair_basis_positive_control", v17i.GATE_EVALUATION),
        ("v17i", "anchor_independent_direction", v17i.NEXT_DIRECTION),
        ("v17j", "effect_blind_design_calibration", DESIGN_CALIBRATION),
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
        "gate": "v17j_effect_blind_anchor_independent_compound_cycle_qualification",
        "purpose_ref": PURPOSE_REF,
        "scope": "proposal_probability_reversibility_representation_traversal_resource_only",
        "source_history_count": 8,
        "start_families": list(START_FAMILIES),
        "chain_seed_families": list(CHAIN_SEED_FAMILIES),
        "subcycle_kernel": "v17c_exact_state_local_length_2_to_4",
        "subcycle_lengths": list(SUBCYCLE_LENGTHS),
        "compound_path": "sample_first_apply_sample_second",
        "forward_probability": "q_first_times_q_second",
        "reverse_path": "mapped_reverse_second_then_mapped_reverse_first",
        "reverse_probability": "q_reverse_second_times_q_reverse_first",
        "metropolis_ratio": "min(1,q_reverse_path/q_forward_path)",
        "laziness_probability": "1/2",
        "symmetric_endpoint_filter": f"net_changed_edges_at_least_{MIN_NET_CHANGED_EDGES}",
        "filtered_path_treatment": "self_loop_without_renormalization",
        "total_steps": TOTAL_STEPS,
        "representation_steps": REPRESENTATION_STEPS,
        "minimum_retained_blocks_per_chain": MIN_RETAINED_BLOCKS_PER_CHAIN,
        "minimum_accepted_blocks_per_chain": MIN_ACCEPTED_BLOCKS_PER_CHAIN,
        "minimum_unique_states_per_chain": MIN_UNIQUE_STATES_PER_CHAIN,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "required_chain_count": EXPECTED_CHAINS,
        "required_representation_rows": EXPECTED_REPRESENTATION_ROWS,
        "design_calibration": "one_frozen_source_left_start_effect_blind_technical_pilot",
        "proposal_target_dependency": "none",
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "not_claimed": [
            "global_connectivity", "irreducibility", "mixing", "convergence",
            "stationary_sample", "source_effect", "energy", "temperature",
            "dimension", "Lorentz_symmetry", "spacetime", "particles",
            "Bell_correlation", "entanglement", "universe_model",
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
        "design_calibration_sha256": file_sha256(DESIGN_CALIBRATION),
        "source_history_count": 8,
        "start_families": ";".join(START_FAMILIES),
        "chain_seed_families": ";".join(CHAIN_SEED_FAMILIES),
        "subcycle_lengths": ";".join(str(value) for value in SUBCYCLE_LENGTHS),
        "total_steps": TOTAL_STEPS,
        "representation_steps": REPRESENTATION_STEPS,
        "minimum_net_changed_edges": MIN_NET_CHANGED_EDGES,
        "minimum_retained_blocks_per_chain": MIN_RETAINED_BLOCKS_PER_CHAIN,
        "minimum_accepted_blocks_per_chain": MIN_ACCEPTED_BLOCKS_PER_CHAIN,
        "minimum_unique_states_per_chain": MIN_UNIQUE_STATES_PER_CHAIN,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "required_chain_count": EXPECTED_CHAINS,
        "required_reverse_path_pass_fraction": 1.0,
        "required_pathwise_balance_pass_fraction": 1.0,
        "required_endpoint_integrity_pass_fraction": 1.0,
        "required_compound_exercise_chains": EXPECTED_CHAINS,
        "required_representation_passes": EXPECTED_REPRESENTATION_ROWS,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def implementation_call_counts() -> Dict[str, int]:
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    global_calls = Counter()
    proposal_calls = Counter()
    proposal_scope = {
        "propose_subcycle", "reverse_subcycle", "reverse_compound", "propose_compound"
    }
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = ""
        if isinstance(node.func, ast.Attribute):
            name = node.func.attr
        elif isinstance(node.func, ast.Name):
            name = node.func.id
        global_calls[name] += 1
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name not in proposal_scope:
            continue
        for child in ast.walk(node):
            if not isinstance(child, ast.Call):
                continue
            if isinstance(child.func, ast.Attribute):
                proposal_calls[child.func.attr] += 1
            elif isinstance(child.func, ast.Name):
                proposal_calls[child.func.id] += 1
    forbidden = (
        "random_cost_start", "decompose_alternating_cycles",
        "interval_spectrum", "jensen_shannon",
    )
    return {
        "spectrum_calls": global_calls["interval_spectrum"],
        "effect_metric_calls": global_calls["jensen_shannon"],
        "proposal_forbidden_calls": sum(proposal_calls[name] for name in forbidden),
    }


def prepare() -> None:
    v17c.verify_outputs()
    v17g.verify_outputs()
    v17h.verify_outputs()
    v17i.verify_outputs()
    rows = v16i.read_csv(DESIGN_CALIBRATION)
    if len(rows) != 1 or rows[0].get("script_sha256") != file_sha256(SCRIPT):
        raise ValueError("run a current-script v17j --pilot before prepare")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v17j] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    expected = {key: str(value) for key, value in preregistration_row().items()}
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v17j preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v17j source chain changed")


def reverse_remove(auxiliary: ResidualAuxiliary) -> Tuple[Edge, ...]:
    return v17a.reverse_remove_sequence(auxiliary.proposal)


def propose_subcycle(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    rng: random.Random,
) -> ResidualAuxiliary | None:
    return v17c.propose_cycle(kernel, selected, rng)


def reverse_subcycle(
    kernel: CycleKernel,
    proposed: frozenset[Edge],
    auxiliary: ResidualAuxiliary,
) -> ResidualAuxiliary | None:
    return v17c.path_probability(kernel, proposed, reverse_remove(auxiliary))


def reverse_compound(
    kernel: CycleKernel,
    endpoint: frozenset[Edge],
    auxiliary: CompoundAuxiliary,
) -> Tuple[CompoundAuxiliary, frozenset[Edge]] | None:
    reverse_first = reverse_subcycle(kernel, endpoint, auxiliary.second)
    if reverse_first is None:
        return None
    intermediate = v17a.apply_proposal(kernel.space, endpoint, reverse_first.proposal)
    reverse_second = reverse_subcycle(kernel, intermediate, auxiliary.first)
    if reverse_second is None:
        return None
    recovered = v17a.apply_proposal(kernel.space, intermediate, reverse_second.proposal)
    if len(endpoint - recovered) < MIN_NET_CHANGED_EDGES:
        return None
    reverse = CompoundAuxiliary(
        reverse_first,
        reverse_second,
        reverse_first.probability * reverse_second.probability,
    )
    return reverse, recovered


def propose_compound(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    rng: random.Random,
) -> CompoundAttempt:
    first = propose_subcycle(kernel, selected, rng)
    if first is None:
        return CompoundAttempt("first_dead_end")
    intermediate = v17a.apply_proposal(kernel.space, selected, first.proposal)
    if reverse_subcycle(kernel, intermediate, first) is None:
        return CompoundAttempt("first_reverse_unsupported", intermediate=intermediate)

    second = propose_subcycle(kernel, intermediate, rng)
    if second is None:
        return CompoundAttempt("second_dead_end", intermediate=intermediate)
    endpoint = v17a.apply_proposal(kernel.space, intermediate, second.proposal)
    if reverse_subcycle(kernel, endpoint, second) is None:
        return CompoundAttempt(
            "second_reverse_unsupported", intermediate=intermediate, endpoint=endpoint
        )

    net_changed = len(selected - endpoint)
    if net_changed < MIN_NET_CHANGED_EDGES:
        return CompoundAttempt(
            "symmetric_net_filter",
            intermediate=intermediate,
            endpoint=endpoint,
            net_changed_edges=net_changed,
        )

    auxiliary = CompoundAuxiliary(
        first, second, first.probability * second.probability
    )
    reverse_result = reverse_compound(kernel, endpoint, auxiliary)
    if reverse_result is None:
        return CompoundAttempt(
            "compound_reverse_unsupported",
            auxiliary=auxiliary,
            intermediate=intermediate,
            endpoint=endpoint,
            net_changed_edges=net_changed,
        )
    reverse, recovered = reverse_result
    reverse_again_result = reverse_compound(kernel, recovered, reverse)
    if reverse_again_result is None:
        return CompoundAttempt(
            "compound_reverse_involution_failed",
            auxiliary=auxiliary,
            reverse=reverse,
            intermediate=intermediate,
            endpoint=endpoint,
            recovered=recovered,
            net_changed_edges=net_changed,
        )
    _, reverse_again_endpoint = reverse_again_result
    return CompoundAttempt(
        "retained",
        auxiliary=auxiliary,
        reverse=reverse,
        intermediate=intermediate,
        endpoint=endpoint,
        recovered=recovered,
        reverse_again_endpoint=reverse_again_endpoint,
        net_changed_edges=net_changed,
    )


def fraction_fields(prefix: str, value: Fraction | None) -> Dict[str, int]:
    return {
        f"{prefix}_numerator": value.numerator if value is not None else 0,
        f"{prefix}_denominator": value.denominator if value is not None else 1,
    }


def edge_json(edges: Iterable[Edge]) -> str:
    return json.dumps([list(edge) for edge in sorted(edges)], separators=(",", ":"))


def proposal_digest(auxiliary: CompoundAuxiliary | None) -> str:
    if auxiliary is None:
        return ""
    payload = {
        "first_remove": list(auxiliary.first.proposal.remove),
        "first_add": list(auxiliary.first.proposal.add),
        "second_remove": list(auxiliary.second.proposal.remove),
        "second_add": list(auxiliary.second.proposal.add),
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def chain_seed(dag: v16i.RunDAG, start_family: str, seed_family: str) -> int:
    return v16i.stable_seed("v17j", "compound_chain", start_family, seed_family, *dag.key)


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
    visited = {v16x.edge_digest(start)}
    counts = Counter()
    accepted_lengths = Counter()
    accepted_net_changes: List[int] = []
    trace: List[Dict[str, Any]] = []
    reverse_rows: List[Dict[str, Any]] = []
    started = time.monotonic()

    for step in range(total_steps):
        state_before = selected
        event = "lazy_stay"
        accepted = False
        attempt = CompoundAttempt("not_drawn")
        acceptance: Fraction | None = None
        exact_balance = False
        endpoint_integrity = True

        if rng.getrandbits(1):
            counts["nonlazy_attempts"] += 1
            attempt = propose_compound(kernel, selected, rng)
            counts[attempt.status] += 1
            event = attempt.status
            if attempt.status == "retained":
                if not all((attempt.auxiliary, attempt.reverse, attempt.endpoint)):
                    raise AssertionError("retained compound attempt missing fields")
                forward = attempt.auxiliary.probability
                reverse = attempt.reverse.probability
                acceptance = min(Fraction(1), reverse / forward)
                reverse_acceptance = min(Fraction(1), forward / reverse)
                exact_balance = forward * acceptance == reverse * reverse_acceptance
                endpoint_integrity = v16x.assignment_integrity(
                    kernel.space, attempt.endpoint
                )
                counts["retained_blocks"] += 1
                if rng.randrange(acceptance.denominator) < acceptance.numerator:
                    selected = attempt.endpoint
                    accepted = True
                    event = "accepted_compound"
                    counts["accepted_blocks"] += 1
                    accepted_lengths[len(attempt.auxiliary.first.proposal.remove)] += 1
                    accepted_lengths[len(attempt.auxiliary.second.proposal.remove)] += 1
                    accepted_net_changes.append(attempt.net_changed_edges)
                else:
                    event = "metropolis_reject"
                    counts["metropolis_reject"] += 1

                reverse_rows.append({
                    **dag.prefix,
                    "start_family": start_family,
                    "chain_seed_family": seed_family,
                    "step": step,
                    "proposal_sha256": proposal_digest(attempt.auxiliary),
                    "reverse_proposal_sha256": proposal_digest(attempt.reverse),
                    "first_cycle_length": len(attempt.auxiliary.first.proposal.remove),
                    "second_cycle_length": len(attempt.auxiliary.second.proposal.remove),
                    "net_changed_edges": attempt.net_changed_edges,
                    "roundtrip_pass": int(attempt.recovered == state_before),
                    "reverse_involution_pass": int(
                        attempt.reverse_again_endpoint == attempt.endpoint
                    ),
                    "forward_endpoint_integrity_pass": int(endpoint_integrity),
                    "recovered_endpoint_integrity_pass": int(
                        attempt.recovered is not None
                        and v16x.assignment_integrity(kernel.space, attempt.recovered)
                    ),
                    "exact_pathwise_balance_pass": int(exact_balance),
                    **fraction_fields("q_forward", forward),
                    **fraction_fields("q_reverse", reverse),
                    **fraction_fields("acceptance", acceptance),
                    **fraction_fields("reverse_acceptance", reverse_acceptance),
                    "source_spectrum_computed": 0,
                    "observed_effect_computed": 0,
                })

        state_after = selected
        visited.add(v16x.edge_digest(selected))
        first_length = (
            len(attempt.auxiliary.first.proposal.remove)
            if attempt.auxiliary is not None else 0
        )
        second_length = (
            len(attempt.auxiliary.second.proposal.remove)
            if attempt.auxiliary is not None else 0
        )
        trace.append({
            **dag.prefix,
            "start_family": start_family,
            "chain_seed_family": seed_family,
            "chain_seed": seed,
            "step": step,
            "event": event,
            "attempt_status": attempt.status,
            "accepted": int(accepted),
            "first_cycle_length": first_length,
            "second_cycle_length": second_length,
            "net_changed_edges": attempt.net_changed_edges,
            "proposal_sha256": proposal_digest(attempt.auxiliary),
            "state_before_sha256": v16x.edge_digest(state_before),
            "state_after_sha256": v16x.edge_digest(state_after),
            "endpoint_integrity_pass": int(endpoint_integrity),
            "exact_pathwise_balance_pass": int(exact_balance) if attempt.status == "retained" else 0,
            **fraction_fields("acceptance", acceptance),
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })

    runtime = time.monotonic() - started
    final_change = len(selected - start) / len(start)
    retained = counts["retained_blocks"]
    accepted_count = counts["accepted_blocks"]
    movement_pass = all((
        retained >= MIN_RETAINED_BLOCKS_PER_CHAIN,
        accepted_count >= MIN_ACCEPTED_BLOCKS_PER_CHAIN,
        len(visited) >= MIN_UNIQUE_STATES_PER_CHAIN,
        min(accepted_net_changes, default=0) >= MIN_NET_CHANGED_EDGES,
    ))
    resource_pass = runtime <= MAX_CHAIN_SECONDS
    stats: MutableMapping[str, Any] = {
        **dag.prefix,
        "start_family": start_family,
        "chain_seed_family": seed_family,
        "chain_seed": seed,
        "total_steps": total_steps,
        "nonlazy_attempts": counts["nonlazy_attempts"],
        "first_dead_end": counts["first_dead_end"],
        "first_reverse_unsupported": counts["first_reverse_unsupported"],
        "second_dead_end": counts["second_dead_end"],
        "second_reverse_unsupported": counts["second_reverse_unsupported"],
        "symmetric_net_filter": counts["symmetric_net_filter"],
        "compound_reverse_unsupported": counts["compound_reverse_unsupported"],
        "compound_reverse_involution_failed": counts["compound_reverse_involution_failed"],
        "retained_blocks": retained,
        "accepted_blocks": accepted_count,
        "metropolis_reject": counts["metropolis_reject"],
        "accepted_length2_subcycles": accepted_lengths[2],
        "accepted_length3_subcycles": accepted_lengths[3],
        "accepted_length4_subcycles": accepted_lengths[4],
        "minimum_accepted_net_changed_edges": min(accepted_net_changes, default=0),
        "maximum_accepted_net_changed_edges": max(accepted_net_changes, default=0),
        "mean_accepted_net_changed_edges": (
            statistics.fmean(accepted_net_changes) if accepted_net_changes else 0.0
        ),
        "unique_state_count": len(visited),
        "final_start_changed_edge_fraction": final_change,
        "final_endpoint_sha256": v16x.edge_digest(selected),
        "final_endpoint_integrity_pass": int(v16x.assignment_integrity(kernel.space, selected)),
        "movement_pass": int(movement_pass),
        "runtime_seconds": runtime,
        "resource_pass": int(resource_pass),
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }
    return ChainResult(selected, stats, trace, reverse_rows)


def pilot() -> None:
    dag, _, space, left, _ = load_spaces()[0]
    result = run_chain(
        dag, v17a.build_kernel(space), left, START_FAMILIES[0],
        "design_calibration_seed", total_steps=PILOT_STEPS,
    )
    row = {
        "stage": "v17j_design_calibration",
        "script_sha256": file_sha256(SCRIPT),
        "growth_seed": dag.growth_seed,
        "run_offset": dag.run_offset,
        "start_family": START_FAMILIES[0],
        "pilot_steps": PILOT_STEPS,
        "nonlazy_attempts": result.stats["nonlazy_attempts"],
        "retained_blocks": result.stats["retained_blocks"],
        "accepted_blocks": result.stats["accepted_blocks"],
        "unique_state_count": result.stats["unique_state_count"],
        "minimum_accepted_net_changed_edges": result.stats["minimum_accepted_net_changed_edges"],
        "maximum_accepted_net_changed_edges": result.stats["maximum_accepted_net_changed_edges"],
        "runtime_seconds": result.stats["runtime_seconds"],
        "reverse_rows": len(result.reverse_rows),
        "reverse_all_pass": int(bool(result.reverse_rows) and all(
            int(row["roundtrip_pass"])
            and int(row["reverse_involution_pass"])
            and int(row["exact_pathwise_balance_pass"])
            and int(row["forward_endpoint_integrity_pass"])
            and int(row["recovered_endpoint_integrity_pass"])
            for row in result.reverse_rows
        )),
        "pilot_scope": "one_source_one_start_effect_blind_technical_only",
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }
    v16i.write_csv(DESIGN_CALIBRATION, [row])
    print(
        "[v17j] pilot "
        f"retained={row['retained_blocks']} accepted={row['accepted_blocks']} "
        f"unique={row['unique_state_count']} runtime={float(row['runtime_seconds']):.3f}s"
    )


def representation_row(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    space: v16x.StateSpace,
    start: frozenset[Edge],
    start_family: str,
) -> Dict[str, Any]:
    def execute(target_space: v16x.StateSpace) -> Tuple[str, str]:
        result = run_chain(
            dag, v17a.build_kernel(target_space), start, start_family,
            "representation_seed", total_steps=REPRESENTATION_STEPS,
        )
        accepted = [
            (row["step"], row["proposal_sha256"], row["state_after_sha256"])
            for row in result.trace if int(row["accepted"])
        ]
        digest = hashlib.sha256(
            json.dumps(accepted, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return v16x.edge_digest(result.final), digest

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
        v16i.stable_seed("v17j", "semantic_relabel", start_family, *dag.key),
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
        "original_transition_sha256": original[1],
        "replay_transition_sha256": replay[1],
        "reordered_transition_sha256": reordered[1],
        "relabeled_transition_sha256": relabeled[1],
        "candidate_set_covariance_pass": int(candidate_pass),
        "exact_replay_pass": int(replay_pass),
        "candidate_order_covariance_pass": int(order_pass),
        "semantic_relabel_covariance_pass": int(relabel_pass),
        "representation_pass": int(all((
            candidate_pass, replay_pass, order_pass, relabel_pass
        ))),
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }


def endpoint_row(result: ChainResult, start: frozenset[Edge]) -> Dict[str, Any]:
    return {
        "stage": "v17j",
        "growth_seed": result.stats["growth_seed"],
        "run_offset": result.stats["run_offset"],
        "start_family": result.stats["start_family"],
        "chain_seed_family": result.stats["chain_seed_family"],
        "start_endpoint_sha256": v16x.edge_digest(start),
        "final_endpoint_sha256": result.stats["final_endpoint_sha256"],
        "final_start_changed_edge_fraction": result.stats["final_start_changed_edge_fraction"],
        "final_endpoint_integrity_pass": result.stats["final_endpoint_integrity_pass"],
        "accepted_blocks": result.stats["accepted_blocks"],
        "unique_state_count": result.stats["unique_state_count"],
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }


def source_summary_rows(
    summaries: Sequence[Mapping[str, Any]],
    reverse_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[int, int], List[Mapping[str, Any]]] = {}
    reverse_grouped: Dict[Tuple[int, int], List[Mapping[str, Any]]] = {}
    for row in summaries:
        grouped.setdefault((int(row["growth_seed"]), int(row["run_offset"])), []).append(row)
    for row in reverse_rows:
        reverse_grouped.setdefault(
            (int(row["growth_seed"]), int(row["run_offset"])), []
        ).append(row)
    output = []
    for key in sorted(grouped):
        rows = grouped[key]
        audits = reverse_grouped.get(key, [])
        reverse_pass = bool(audits) and all(
            int(row["roundtrip_pass"])
            and int(row["reverse_involution_pass"])
            and int(row["exact_pathwise_balance_pass"])
            and int(row["forward_endpoint_integrity_pass"])
            and int(row["recovered_endpoint_integrity_pass"])
            for row in audits
        )
        chain_passes = sum(
            int(row["movement_pass"])
            and int(row["resource_pass"])
            and int(row["final_endpoint_integrity_pass"])
            for row in rows
        )
        source_pass = len(rows) == 4 and chain_passes == 4 and reverse_pass
        output.append({
            "stage": "v17j",
            "growth_seed": key[0],
            "run_offset": key[1],
            "chain_count": len(rows),
            "chain_qualification_passes": chain_passes,
            "retained_blocks": sum(int(row["retained_blocks"]) for row in rows),
            "accepted_blocks": sum(int(row["accepted_blocks"]) for row in rows),
            "minimum_chain_retained_blocks": min(int(row["retained_blocks"]) for row in rows),
            "minimum_chain_accepted_blocks": min(int(row["accepted_blocks"]) for row in rows),
            "minimum_chain_unique_states": min(int(row["unique_state_count"]) for row in rows),
            "reverse_audit_rows": len(audits),
            "all_reverse_path_pass": int(reverse_pass),
            "source_qualification_pass": int(source_pass),
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })
    return output


def gate_rows(
    calls: Mapping[str, int],
    summaries: Sequence[Mapping[str, Any]],
    reverse_rows: Sequence[Mapping[str, Any]],
    representations: Sequence[Mapping[str, Any]],
    sources: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    effect_blind = calls == {
        "spectrum_calls": 0,
        "effect_metric_calls": 0,
        "proposal_forbidden_calls": 0,
    }
    chain_count_pass = len(summaries) == EXPECTED_CHAINS
    reverse_passes = sum(
        int(row["roundtrip_pass"])
        and int(row["reverse_involution_pass"])
        and int(row["exact_pathwise_balance_pass"])
        and int(row["forward_endpoint_integrity_pass"])
        and int(row["recovered_endpoint_integrity_pass"])
        for row in reverse_rows
    )
    reverse_pass = bool(reverse_rows) and reverse_passes == len(reverse_rows)
    compound_exercise = sum(
        int(row["retained_blocks"]) >= MIN_RETAINED_BLOCKS_PER_CHAIN
        and int(row["accepted_blocks"]) >= MIN_ACCEPTED_BLOCKS_PER_CHAIN
        and int(row["minimum_accepted_net_changed_edges"]) >= MIN_NET_CHANGED_EDGES
        for row in summaries
    )
    movement = sum(int(row["movement_pass"]) for row in summaries)
    resources = sum(int(row["resource_pass"]) for row in summaries)
    endpoints = sum(int(row["final_endpoint_integrity_pass"]) for row in summaries)
    representation = sum(int(row["representation_pass"]) for row in representations)
    source_passes = sum(int(row["source_qualification_pass"]) for row in sources)
    overall_pass = all((
        effect_blind,
        chain_count_pass,
        reverse_pass,
        compound_exercise == EXPECTED_CHAINS,
        movement == EXPECTED_CHAINS,
        resources == EXPECTED_CHAINS,
        endpoints == EXPECTED_CHAINS,
        representation == EXPECTED_REPRESENTATION_ROWS,
        source_passes == 6,
    ))
    overall = (
        "v17j_anchor_independent_compound_cycle_qualified"
        if overall_pass
        else "v17j_anchor_independent_compound_cycle_not_qualified"
    )
    return [
        {"gate": "effect_blind_and_proposal_scope_independence", "status": "pass" if effect_blind else "fail", "observed": f"spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']};proposal_forbidden={calls['proposal_forbidden_calls']}", "required": "0;0;0", "decision": "continue" if effect_blind else "stop"},
        {"gate": "formal_chain_count", "status": "pass" if chain_count_pass else "fail", "observed": f"{len(summaries)}/{EXPECTED_CHAINS}", "required": f"{EXPECTED_CHAINS}/{EXPECTED_CHAINS}", "decision": "continue" if chain_count_pass else "repair_execution"},
        {"gate": "exact_reverse_involution_balance_integrity", "status": "pass" if reverse_pass else "fail", "observed": f"{reverse_passes}/{len(reverse_rows)}", "required": "all_retained", "decision": "continue" if reverse_pass else "repair_proposal"},
        {"gate": "finite_compound_large_move_exercise", "status": "pass" if compound_exercise == EXPECTED_CHAINS else "fail", "observed": f"{compound_exercise}/{EXPECTED_CHAINS}", "required": f"{EXPECTED_CHAINS}/{EXPECTED_CHAINS};retained>={MIN_RETAINED_BLOCKS_PER_CHAIN};accepted>={MIN_ACCEPTED_BLOCKS_PER_CHAIN};net>={MIN_NET_CHANGED_EDGES}", "decision": "continue" if compound_exercise == EXPECTED_CHAINS else "retire_or_recalibrate"},
        {"gate": "finite_movement", "status": "pass" if movement == EXPECTED_CHAINS else "fail", "observed": f"{movement}/{EXPECTED_CHAINS}", "required": f"{EXPECTED_CHAINS}/{EXPECTED_CHAINS}", "decision": "continue" if movement == EXPECTED_CHAINS else "retire_or_recalibrate"},
        {"gate": "endpoint_integrity", "status": "pass" if endpoints == EXPECTED_CHAINS else "fail", "observed": f"{endpoints}/{EXPECTED_CHAINS}", "required": f"{EXPECTED_CHAINS}/{EXPECTED_CHAINS}", "decision": "continue" if endpoints == EXPECTED_CHAINS else "repair_proposal"},
        {"gate": "representation_covariance", "status": "pass" if representation == EXPECTED_REPRESENTATION_ROWS else "fail", "observed": f"{representation}/{EXPECTED_REPRESENTATION_ROWS}", "required": f"{EXPECTED_REPRESENTATION_ROWS}/{EXPECTED_REPRESENTATION_ROWS}", "decision": "continue" if representation == EXPECTED_REPRESENTATION_ROWS else "repair_representation"},
        {"gate": "resource_bound", "status": "pass" if resources == EXPECTED_CHAINS else "fail", "observed": f"{resources}/{EXPECTED_CHAINS};max={max(float(row['runtime_seconds']) for row in summaries):.6f}s", "required": f"{EXPECTED_CHAINS}/{EXPECTED_CHAINS};each<={MAX_CHAIN_SECONDS}s", "decision": "continue" if resources == EXPECTED_CHAINS else "retire_or_optimize"},
        {"gate": "per_source_qualification", "status": "pass" if source_passes == 6 else "fail", "observed": f"{source_passes}/6", "required": "6/6", "decision": "matched_work_next" if source_passes == 6 else "localize_failure"},
        {"gate": "v17j_overall", "status": overall, "observed": f"effect_blind={int(effect_blind)};chains={len(summaries)};reverse={reverse_passes}/{len(reverse_rows)};exercise={compound_exercise}/{EXPECTED_CHAINS};movement={movement}/{EXPECTED_CHAINS};representation={representation}/{EXPECTED_REPRESENTATION_ROWS};sources={source_passes}/6", "required": f"1;{EXPECTED_CHAINS};all;{EXPECTED_CHAINS};{EXPECTED_CHAINS};{EXPECTED_REPRESENTATION_ROWS};6", "decision": overall},
    ]


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> List[str]:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return lines


def claim_rows(overall: str) -> List[Dict[str, Any]]:
    qualified = overall == "v17j_anchor_independent_compound_cycle_qualified"
    return [
        {"claim_id": "C1", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "factual", "strength": "assertive", "claim": "v17j computes no source spectrum or observed-effect metric.", "status": "supported", "evidence": "static call audit and output exclusion fields", "scope_limit": "v17j only"},
        {"claim_id": "C2", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "algorithmic", "strength": "assertive", "claim": "The compound proposal uses only the current state and frozen candidate graph, not the paired target start.", "status": "supported", "evidence": "proposal-scope AST audit and function signatures", "scope_limit": "proposal construction; paired starts remain evaluation anchors"},
        {"claim_id": "C3", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "algebraic", "strength": "assertive", "claim": "Every retained auxiliary path has an exact reverse involution and exact pathwise Metropolis balance.", "status": "supported" if qualified else "not_supported", "evidence": "v17j_reverse_path_audit.csv", "scope_limit": "retained finite sampled auxiliary paths"},
        {"claim_id": "C4", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "finite_simulation", "strength": "bounded", "claim": "The compound law exercises accepted net-large moves with integrity and representation covariance on all frozen evaluation chains.", "status": "supported" if qualified else "not_supported", "evidence": "transition, endpoint, representation and source summaries", "scope_limit": "six spaces, two starts and two seed families"},
        {"claim_id": "C5", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "global", "strength": "prohibited", "claim": "v17j proves global connectivity, irreducibility, mixing, convergence or a stationary sample.", "status": "contradicted", "evidence": "finite qualification does not establish global state-space properties", "scope_limit": "requires separate formal or scaling evidence"},
        {"claim_id": "C6", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "physics", "strength": "prohibited", "claim": "v17j establishes source effects, energy, geometry, Lorentz symmetry, spacetime or a universe model.", "status": "contradicted", "evidence": "effect observables prohibited and no physical diagnostics computed", "scope_limit": "requires later gates"},
    ]


def write_documents(
    gates: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    reverse_rows: Sequence[Mapping[str, Any]],
) -> None:
    overall = gates[-1]["status"]
    qualified = overall == "v17j_anchor_independent_compound_cycle_qualified"
    retained = sum(int(row["retained_blocks"]) for row in summaries)
    accepted = sum(int(row["accepted_blocks"]) for row in summaries)
    min_retained = min(int(row["retained_blocks"]) for row in summaries)
    min_accepted = min(int(row["accepted_blocks"]) for row in summaries)
    max_runtime = max(float(row["runtime_seconds"]) for row in summaries)
    next_step = (
        "Run a separate v17k effect-blind matched accepted-work comparison between the qualified compound law and the v17h expanded single-cycle law. Keep source effects closed."
        if qualified
        else "Localize whether failure came from reverse accounting, finite exercise, representation, or resources. Do not use this compound law in a source null; consider a separately qualified monolithic long-cycle counter only if the compound mechanism is retired."
    )
    lines = [
        "# v17j effect-blind anchor-independent compound-cycle qualification",
        "",
        f"Status: `{overall}`.",
        "",
        "## Purpose and frozen design",
        "",
        "The gate asks whether a larger reusable proposal can be built without the v17i pair basis. It composes two exact state-local v17c cycles into one auxiliary path. The second cycle is sampled from the first intermediate state. The mapped reverse applies the second reverse first and the first reverse second.",
        "",
        f"The forward density is the exact product `q1*q2`; the reverse density is the exact reversed-path product. Blocks with fewer than `{MIN_NET_CHANGED_EDGES}` net changed edges are symmetric self-loops without renormalization. Source spectra and observed effects were prohibited.",
        "",
        "## Formal result",
        "",
        f"The formal run covered `{len(summaries)}` chains. It retained `{retained}` compound blocks and accepted `{accepted}`. The weakest chain retained `{min_retained}` and accepted `{min_accepted}` blocks. All retained-path audits passed in `{sum(int(row['roundtrip_pass']) and int(row['reverse_involution_pass']) and int(row['exact_pathwise_balance_pass']) for row in reverse_rows)}/{len(reverse_rows)}`. Maximum chain runtime was `{max_runtime:.6f}` seconds.",
        "",
        "## Gates",
        "",
        *markdown_table(gates, ("gate", "status", "observed", "required", "decision")),
        "",
        "## Evidential boundary",
        "",
        "A qualification result concerns the implemented finite proposal law: target independence of proposal construction, exact sampled auxiliary-path reversal, endpoint integrity, representation covariance, finite movement and resource bounds. It is not evidence of global connectivity, mixing, equilibrium, source effects or physics.",
        "",
        "## Next decision",
        "",
        next_step,
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    INTERPRETATION.write_text(
        "# v17j interpretation audit\n\n"
        f"Formal status: `{overall}`.\n\n"
        "The two-cycle block is anchor-independent at proposal time: it sees the current assignment and candidate graph, not the paired evaluation start. Exact balance is a property of retained sampled auxiliary paths, not proof that the finite chains mixed or connected the whole component. The net-change filter is symmetric and rejected paths remain self-loops; no conditioned proposal normalization was introduced. Source effects and physics remain untested.\n",
        encoding="utf-8",
    )
    NEXT_DIRECTION.write_text(
        "# v17j next direction\n\n"
        f"Formal status: `{overall}`.\n\n{next_step}\n",
        encoding="utf-8",
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.17j\n\n"
        f"- status: `{overall}`\n"
        f"- retained compound blocks: `{retained}`\n"
        f"- accepted compound blocks: `{accepted}`\n"
        f"- next: {next_step}\n"
        "- source spectrum and observed effects remain closed\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.17j\n\n"
        "I stedet for aa bruke en fasit som kjenner begge starttilstandene, lar denne testen simulatoren velge to lokale omkoblinger etter hverandre og behandle dem som ett stort forslag. Den regner den noeyaktige sannsynligheten for aa gaa samme vei baklengs. En bestaatt gate betyr at dette er et teknisk ryddig og faktisk brukt stort lokalt trekk. Det betyr ikke at hele tilstandsrommet er koblet, at kjeden har blandet seg, eller at noen fysisk effekt er paavist.\n",
        encoding="utf-8",
    )


def run() -> None:
    verify_frozen_sources()
    calls = implementation_call_counts()
    trace_rows: List[Dict[str, Any]] = []
    reverse_rows: List[Dict[str, Any]] = []
    endpoint_rows: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []
    representations: List[Dict[str, Any]] = []

    for dag, metadata, space, left, right in load_spaces():
        kernel = v17a.build_kernel(space)
        starts = {START_FAMILIES[0]: left, START_FAMILIES[1]: right}
        for start_family, start in starts.items():
            representations.append(
                representation_row(dag, metadata, space, start, start_family)
            )
            for seed_family in CHAIN_SEED_FAMILIES:
                result = run_chain(
                    dag, kernel, start, start_family, seed_family,
                    total_steps=TOTAL_STEPS,
                )
                trace_rows.extend(result.trace)
                reverse_rows.extend(result.reverse_rows)
                endpoint_rows.append(endpoint_row(result, start))
                summaries.append(dict(result.stats))

    sources = source_summary_rows(summaries, reverse_rows)
    gates = gate_rows(calls, summaries, reverse_rows, representations, sources)
    overall = gates[-1]["status"]
    v16i.write_csv(PROPOSAL_TRACE, trace_rows)
    v16i.write_csv(REVERSE_AUDIT, reverse_rows)
    v16i.write_csv(ENDPOINT_AUDIT, endpoint_rows)
    v16i.write_csv(REPRESENTATION_AUDIT, representations)
    v16i.write_csv(TRANSITION_SUMMARY, summaries)
    v16i.write_csv(SOURCE_SUMMARY, sources)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(GOAL_EVALUATION, [{
        "purpose_ref": PURPOSE_REF,
        "goal_id": "G1",
        "metric": "effect_blind_anchor_independent_compound_proposal_qualification",
        "baseline": "v17i pair-derived positive control only",
        "target": "exact reverse, finite large-move exercise, representation and resource pass",
        "status": "satisfied" if overall == "v17j_anchor_independent_compound_cycle_qualified" else "missed",
        "evidence": overall,
        "next_decision": "v17k_matched_work_start_memory" if "qualified" in overall else "localize_or_retire_compound_law",
    }])
    v16i.write_csv(CLAIM_LEDGER, claim_rows(overall))
    write_documents(gates, summaries, reverse_rows)
    print(f"[v17j] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    fixed_counts = {
        PROPOSAL_TRACE: EXPECTED_CHAINS * TOTAL_STEPS,
        ENDPOINT_AUDIT: EXPECTED_CHAINS,
        REPRESENTATION_AUDIT: EXPECTED_REPRESENTATION_ROWS,
        TRANSITION_SUMMARY: EXPECTED_CHAINS,
        SOURCE_SUMMARY: 6,
        GATE_EVALUATION: 10,
        GOAL_EVALUATION: 1,
        CLAIM_LEDGER: 6,
    }
    loaded: Dict[Path, List[Dict[str, str]]] = {}
    for path, expected in fixed_counts.items():
        rows = v16i.read_csv(path)
        if len(rows) != expected:
            raise AssertionError(f"{path.name} row count {len(rows)} != {expected}")
        loaded[path] = rows
    reverse_rows = v16i.read_csv(REVERSE_AUDIT)
    expected_reverse = sum(
        int(row["retained_blocks"]) for row in loaded[TRANSITION_SUMMARY]
    )
    if len(reverse_rows) != expected_reverse or not reverse_rows:
        raise AssertionError("v17j reverse audit row count mismatch or empty")
    if any(not all((
        int(row["roundtrip_pass"]),
        int(row["reverse_involution_pass"]),
        int(row["forward_endpoint_integrity_pass"]),
        int(row["recovered_endpoint_integrity_pass"]),
        int(row["exact_pathwise_balance_pass"]),
    )) for row in reverse_rows):
        raise AssertionError("v17j retained reverse path audit failed")
    if any(int(row["final_endpoint_integrity_pass"]) != 1 for row in loaded[ENDPOINT_AUDIT]):
        raise AssertionError("v17j endpoint integrity failed")
    overall = loaded[GATE_EVALUATION][-1]["status"]
    if overall not in {
        "v17j_anchor_independent_compound_cycle_qualified",
        "v17j_anchor_independent_compound_cycle_not_qualified",
    }:
        raise AssertionError("v17j overall status invalid")
    for path in (REPORT, INTERPRETATION, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise AssertionError(f"missing v17j document {path.name}")
    print(f"[v17j] output verification pass overall={overall}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    selected = sum((args.pilot, args.prepare, args.verify_only))
    if selected > 1:
        raise SystemExit("choose only one of --pilot, --prepare, --verify-only")
    if args.pilot:
        pilot()
    elif args.prepare:
        prepare()
    elif args.verify_only:
        verify_outputs()
    else:
        run()
        verify_outputs()


if __name__ == "__main__":
    main()
