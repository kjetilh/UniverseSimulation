#!/usr/bin/env python3
"""v17k effect-blind compound-vs-single-cycle matched-work gate.

The qualified v17j two-subcycle proposal and the v17h reverse-closed expanded
single-cycle proposal are compared on the same six spaces and frozen start
pairs. Every chain stops at exactly equal accepted gross removed-edge work.
Source spectra and observed-effect metrics remain prohibited.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
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
from typing import Any, Dict, List, Mapping, MutableMapping, Sequence, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16x_explicit_global_measure_gate as v16x
import relational_universe_v16z_alternating_cycle_bridge_gate as v16z
import relational_universe_v17a_state_independent_cycle_proposal_qualification as v17a
import relational_universe_v17f_effect_blind_length5_move_qualification as v17f
import relational_universe_v17h_effect_blind_matched_work_start_memory as v17h
import relational_universe_v17i_effect_blind_cycle_basis_positive_control as v17i
import relational_universe_v17j_effect_blind_compound_cycle_qualification as v17j


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

KERNEL_ARMS = (
    "expanded_reverse_closed_length_2_5",
    "compound_two_length_2_4_net6",
)
START_FAMILIES = v17h.START_FAMILIES
CHAIN_SEED_FAMILIES = ("matched_work_seed_k", "matched_work_seed_l")
ACCEPTED_GROSS_EDGE_WORK_TARGET = 192
WORK_INCREMENTS = {
    KERNEL_ARMS[0]: (2, 3, 4, 5),
    KERNEL_ARMS[1]: (6, 7, 8),
}
PILOT_WORK_TARGET = 48
PILOT_MAX_ATTEMPTS = 4096
MAX_ATTEMPTS = 16384
MAX_CHAIN_SECONDS = 900.0
MIN_UNIQUE_STATES = 20
MIN_FINAL_START_CHANGE = 0.04
MIN_EXPANDED_LENGTH5_CYCLES = 2
MAX_MATERIAL_CROSS_START_RATIO = 0.90
EXPECTED_CHAINS = 6 * 2 * 2 * 2

DESIGN_CALIBRATION = DOC / "v17k_design_calibration.csv"
SOURCE_CHAIN = DOC / "v17k_source_chain.csv"
PRE_REGISTRATION = DOC / "v17k_pre_registration.csv"
PROPOSAL_LAW_AUDIT = DOC / "v17k_proposal_law_audit.csv"
PROPOSAL_TRACE = DOC / "v17k_proposal_trace.csv"
ENDPOINT_AUDIT = DOC / "v17k_endpoint_audit.csv"
PAIRWISE_DISTANCE = DOC / "v17k_pairwise_distance.csv"
KERNEL_DISTANCE_SUMMARY = DOC / "v17k_kernel_distance_summary.csv"
MATCHED_WORK_COMPARISON = DOC / "v17k_matched_work_comparison.csv"
TRANSITION_SUMMARY = DOC / "v17k_chain_transition_summary.csv"
SOURCE_SUMMARY = DOC / "v17k_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v17k_gate_evaluation.csv"
GOAL_EVALUATION = DOC / "v17k_goal_evaluation.csv"
CLAIM_LEDGER = DOC / "v17k_claim_ledger.csv"
REPORT = DOC / "v17k_effect_blind_compound_matched_work_start_memory.md"
INTERPRETATION = DOC / "v17k_interpretation_audit.md"
NEXT_DIRECTION = DOC / "v17k_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_17k_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_17k.md"

Edge = v16x.Edge
CycleKernel = v17a.CycleKernel


@dataclass
class ChainResult:
    final: frozenset[Edge]
    stats: MutableMapping[str, Any]
    trace: List[Dict[str, Any]]


@dataclass
class Endpoint:
    edges: frozenset[Edge]
    row: MutableMapping[str, Any]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    result = []
    for source, metadata in v17h.load_runs():
        result.append((
            v16i.RunDAG(
                stage="v17k",
                target_nodes=source.target_nodes,
                growth_seed=source.growth_seed,
                run_offset=source.run_offset,
                arm=source.arm,
                run_seed=source.run_seed,
                predecessors=source.predecessors,
                depths=source.depths,
                indegrees=source.indegrees,
            ),
            metadata,
        ))
    if len(result) != 6:
        raise ValueError("v17k requires six frozen source spaces")
    return result


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v16z", "frozen_start_pair", v16z.REVERSIBILITY_AUDIT),
        ("v17h", "expanded_single_cycle_implementation", v17h.SCRIPT),
        ("v17h", "expanded_single_cycle_preregistration", v17h.PRE_REGISTRATION),
        ("v17h", "expanded_single_cycle_gate", v17h.GATE_EVALUATION),
        ("v17i", "start_distance_positive_control", v17i.GATE_EVALUATION),
        ("v17j", "compound_proposal_implementation", v17j.SCRIPT),
        ("v17j", "compound_proposal_preregistration", v17j.PRE_REGISTRATION),
        ("v17j", "compound_proposal_gate", v17j.GATE_EVALUATION),
        ("v17k", "effect_blind_design_calibration", DESIGN_CALIBRATION),
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
        "gate": "v17k_effect_blind_compound_matched_work_start_memory",
        "purpose_ref": PURPOSE_REF,
        "scope": "relative_finite_start_memory_at_equal_accepted_gross_removed_edge_work",
        "source_history_count": 9,
        "kernel_arms": list(KERNEL_ARMS),
        "start_families": list(START_FAMILIES),
        "chain_seed_families": list(CHAIN_SEED_FAMILIES),
        "seed_independence": "stable_seed_v17k_includes_arm_start_seed_and_source_key",
        "accepted_gross_edge_work_target": ACCEPTED_GROSS_EDGE_WORK_TARGET,
        "work_definition": {
            KERNEL_ARMS[0]: "removed_edges_in_accepted_single_cycle",
            KERNEL_ARMS[1]: (
                "removed_edges_in_accepted_first_subcycle_plus_"
                "removed_edges_in_accepted_second_subcycle"
            ),
        },
        "net_endpoint_change_treatment": (
            "logged_separately_and_never_substituted_for_gross_work"
        ),
        "work_increments": {
            arm: list(values) for arm, values in WORK_INCREMENTS.items()
        },
        "maximum_attempts": MAX_ATTEMPTS,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "parallel_execution": (
            "source_spaces_may_run_in_separate_processes; per-chain seeds and "
            "source-index aggregation order are invariant"
        ),
        "terminal_rule": (
            "after exact Metropolis acceptance, self-loop if proposal overshoots "
            "the target or leaves a remainder not representable by the arm's "
            "declared accepted-work increments"
        ),
        "terminal_rule_scope_limit": (
            "finite work-conditioned endpoint comparison; not stationary sampling "
            "and may induce terminal conditioning bias"
        ),
        "minimum_unique_states": MIN_UNIQUE_STATES,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "minimum_expanded_length5_cycles": MIN_EXPANDED_LENGTH5_CYCLES,
        "primary_metric": (
            "compound_median_absolute_cross_start_distance_divided_by_"
            "expanded_single_cycle_median"
        ),
        "primary_threshold": MAX_MATERIAL_CROSS_START_RATIO,
        "primary_requirement": "six_of_six_sources_each_at_or_below_threshold",
        "threshold_provenance": "unchanged_from_published_v17h_gate",
        "design_calibration": (
            "one_source_one_start_both_arms_work_completion_and_runtime_only"
        ),
        "design_calibration_work_target": PILOT_WORK_TARGET,
        "design_calibration_excludes": (
            "cross_start_distance;within_start_distance;source_spectrum;observed_effect"
        ),
        "required_chain_count": EXPECTED_CHAINS,
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
        "source_history_count": 9,
        "kernel_arms": ";".join(KERNEL_ARMS),
        "start_families": ";".join(START_FAMILIES),
        "chain_seed_families": ";".join(CHAIN_SEED_FAMILIES),
        "accepted_gross_edge_work_target": ACCEPTED_GROSS_EDGE_WORK_TARGET,
        "expanded_work_increments": ";".join(
            str(value) for value in WORK_INCREMENTS[KERNEL_ARMS[0]]
        ),
        "compound_work_increments": ";".join(
            str(value) for value in WORK_INCREMENTS[KERNEL_ARMS[1]]
        ),
        "maximum_attempts": MAX_ATTEMPTS,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "minimum_unique_states": MIN_UNIQUE_STATES,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "minimum_expanded_length5_cycles": MIN_EXPANDED_LENGTH5_CYCLES,
        "maximum_material_cross_start_ratio": MAX_MATERIAL_CROSS_START_RATIO,
        "required_chain_count": EXPECTED_CHAINS,
        "required_primary_source_passes": 6,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
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


def prepare() -> None:
    v17h.verify_outputs()
    v17i.verify_outputs()
    v17j.verify_outputs()
    pilot_rows = v16i.read_csv(DESIGN_CALIBRATION)
    if (
        len(pilot_rows) != 2
        or any(row.get("script_sha256") != file_sha256(SCRIPT) for row in pilot_rows)
        or any(int(row.get("matched_work_pass", 0)) != 1 for row in pilot_rows)
    ):
        raise ValueError("run a current-script successful v17k --pilot before prepare")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v17k] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    expected = {key: str(value) for key, value in preregistration_row().items()}
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v17k preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v17k source chain changed")


def chain_seed(
    dag: v16i.RunDAG,
    kernel_arm: str,
    start_family: str,
    seed_family: str,
) -> int:
    return v16i.stable_seed(
        "v17k",
        "matched_gross_removed_edge_work",
        kernel_arm,
        start_family,
        seed_family,
        *dag.key,
    )


def reachable_remainders(target: int, increments: Sequence[int]) -> frozenset[int]:
    reachable = {0}
    for total in range(target + 1):
        if total not in reachable:
            continue
        for increment in increments:
            candidate = total + increment
            if candidate <= target:
                reachable.add(candidate)
    return frozenset(reachable)


def boundary_allows(
    work_before: int,
    proposal_work: int,
    target: int,
    reachable: frozenset[int],
) -> bool:
    remaining_after = target - work_before - proposal_work
    return remaining_after >= 0 and remaining_after in reachable


def minimum_accepted_events(kernel_arm: str, target: int) -> int:
    return math.ceil(target / max(WORK_INCREMENTS[kernel_arm]))


def proposal_law_rows() -> List[Dict[str, Any]]:
    return [
        {
            "kernel_arm": KERNEL_ARMS[0],
            "proposal_function": "v17f.propose_expanded",
            "reverse_function": "v17f.reverse_expanded",
            "qualification_context": "v17g_reverse_closed_self_loop_filter",
            "source_script": v17h.SCRIPT.name,
            "source_script_sha256": file_sha256(v17h.SCRIPT),
            "forward_density": "qualified_expanded_auxiliary_probability",
            "reverse_density": "mapped_reverse_auxiliary_probability",
            "gross_work_definition": "len(proposal.remove)",
            "net_change_separate": 1,
            "proposal_law_reimplemented": 0,
            "audit_pass": 1,
        },
        {
            "kernel_arm": KERNEL_ARMS[1],
            "proposal_function": "v17j.propose_compound",
            "reverse_function": "v17j.reverse_compound",
            "qualification_context": "v17j_exact_compound_path_and_net6_filter",
            "source_script": v17j.SCRIPT.name,
            "source_script_sha256": file_sha256(v17j.SCRIPT),
            "forward_density": "q_first_times_q_second",
            "reverse_density": "q_reverse_second_times_q_reverse_first",
            "gross_work_definition": (
                "len(first.proposal.remove)+len(second.proposal.remove)"
            ),
            "net_change_separate": 1,
            "proposal_law_reimplemented": 0,
            "audit_pass": 1,
        },
    ]


def fraction_fields(prefix: str, value: Fraction | None) -> Dict[str, int]:
    return {
        f"{prefix}_numerator": value.numerator if value is not None else 0,
        f"{prefix}_denominator": value.denominator if value is not None else 1,
    }


def run_chain(
    dag: v16i.RunDAG,
    kernel: CycleKernel,
    start: frozenset[Edge],
    kernel_arm: str,
    start_family: str,
    seed_family: str,
    *,
    work_target: int = ACCEPTED_GROSS_EDGE_WORK_TARGET,
    max_attempts: int = MAX_ATTEMPTS,
) -> ChainResult:
    if kernel_arm not in KERNEL_ARMS:
        raise ValueError(f"unknown v17k kernel arm {kernel_arm}")
    increments = WORK_INCREMENTS[kernel_arm]
    reachable = reachable_remainders(work_target, increments)
    if work_target not in reachable:
        raise ValueError(f"work target {work_target} unreachable for {kernel_arm}")

    seed = chain_seed(dag, kernel_arm, start_family, seed_family)
    rng = random.Random(seed)
    selected = start
    trace: List[Dict[str, Any]] = []
    counts = Counter()
    accepted_work_counts = Counter()
    accepted_gross_work = 0
    accepted_net_changed_work = 0
    visited = {v16x.edge_digest(selected)}
    started = time.monotonic()

    for attempt_index in range(1, max_attempts + 1):
        if accepted_gross_work == work_target:
            break

        state_before = selected
        state_before_digest = v16x.edge_digest(selected)
        event = "lazy_stay"
        move_class = "none"
        proposal_sha256 = ""
        first_length = 0
        second_length = 0
        proposal_work = 0
        net_changed_edges = 0
        forward: Fraction | None = None
        reverse: Fraction | None = None
        acceptance: Fraction | None = None
        accepted = False
        endpoint_integrity = True
        roundtrip_pass = True
        exact_balance_pass = True
        reverse_supported = False

        if rng.getrandbits(1):
            counts["nonlazy_attempts"] += 1
            if kernel_arm == KERNEL_ARMS[0]:
                auxiliary = v17f.propose_expanded(kernel, selected, rng)
                if auxiliary is None:
                    event = "proposal_dead_end"
                    counts["proposal_dead_end"] += 1
                else:
                    counts["raw_proposals"] += 1
                    move_class = auxiliary.move_class
                    first_length = len(auxiliary.proposal.remove)
                    proposal_work = first_length
                    proposed = v17a.apply_proposal(
                        kernel.space, selected, auxiliary.proposal
                    )
                    net_changed_edges = len(selected - proposed)
                    proposal_sha256 = v17a.proposal_digest(auxiliary.proposal)
                    reverse_auxiliary = v17f.reverse_expanded(
                        kernel, proposed, auxiliary
                    )
                    if reverse_auxiliary is None:
                        event = "reverse_filtered_dead_end"
                        counts["reverse_filtered_dead_end"] += 1
                    else:
                        reverse_supported = True
                        counts["retained_reverse_supported"] += 1
                        recovered = v17a.apply_proposal(
                            kernel.space, proposed, reverse_auxiliary.proposal
                        )
                        roundtrip_pass = recovered == selected
                        endpoint_integrity = v16x.assignment_integrity(
                            kernel.space, proposed
                        )
                        forward = auxiliary.probability
                        reverse = reverse_auxiliary.probability
                        acceptance = min(Fraction(1), reverse / forward)
                        reverse_acceptance = min(Fraction(1), forward / reverse)
                        exact_balance_pass = (
                            forward * acceptance
                            == reverse * reverse_acceptance
                        )
                        if not roundtrip_pass:
                            counts["roundtrip_failures"] += 1
                            event = "roundtrip_failure"
                        elif not exact_balance_pass:
                            counts["exact_balance_failures"] += 1
                            event = "exact_balance_failure"
                        elif not endpoint_integrity:
                            counts["endpoint_integrity_failures"] += 1
                            event = "endpoint_integrity_failure"
                        elif v17a.exact_accept(rng, acceptance):
                            if not boundary_allows(
                                accepted_gross_work,
                                proposal_work,
                                work_target,
                                reachable,
                            ):
                                event = "work_boundary_reject"
                                counts["work_boundary_rejects"] += 1
                            else:
                                selected = proposed
                                accepted = True
                                event = "accepted_single_cycle"
                        else:
                            event = "metropolis_reject"
                            counts["metropolis_rejects"] += 1
            else:
                compound_attempt = v17j.propose_compound(kernel, selected, rng)
                counts[compound_attempt.status] += 1
                event = compound_attempt.status
                if compound_attempt.status == "retained":
                    if not all((
                        compound_attempt.auxiliary,
                        compound_attempt.reverse,
                        compound_attempt.endpoint,
                        compound_attempt.recovered,
                    )):
                        raise AssertionError(
                            "retained v17k compound attempt missing fields"
                        )
                    counts["raw_proposals"] += 1
                    counts["retained_reverse_supported"] += 1
                    reverse_supported = True
                    move_class = "compound_two_subcycles"
                    first_length = len(
                        compound_attempt.auxiliary.first.proposal.remove
                    )
                    second_length = len(
                        compound_attempt.auxiliary.second.proposal.remove
                    )
                    proposal_work = first_length + second_length
                    net_changed_edges = compound_attempt.net_changed_edges
                    proposal_sha256 = v17j.proposal_digest(
                        compound_attempt.auxiliary
                    )
                    proposed = compound_attempt.endpoint
                    forward = compound_attempt.auxiliary.probability
                    reverse = compound_attempt.reverse.probability
                    acceptance = min(Fraction(1), reverse / forward)
                    reverse_acceptance = min(Fraction(1), forward / reverse)
                    roundtrip_pass = compound_attempt.recovered == selected
                    exact_balance_pass = (
                        forward * acceptance
                        == reverse * reverse_acceptance
                    )
                    endpoint_integrity = v16x.assignment_integrity(
                        kernel.space, proposed
                    )
                    if proposal_work not in WORK_INCREMENTS[kernel_arm]:
                        counts["work_definition_failures"] += 1
                        event = "work_definition_failure"
                    elif not roundtrip_pass:
                        counts["roundtrip_failures"] += 1
                        event = "roundtrip_failure"
                    elif not exact_balance_pass:
                        counts["exact_balance_failures"] += 1
                        event = "exact_balance_failure"
                    elif not endpoint_integrity:
                        counts["endpoint_integrity_failures"] += 1
                        event = "endpoint_integrity_failure"
                    elif v17a.exact_accept(rng, acceptance):
                        if not boundary_allows(
                            accepted_gross_work,
                            proposal_work,
                            work_target,
                            reachable,
                        ):
                            event = "work_boundary_reject"
                            counts["work_boundary_rejects"] += 1
                        else:
                            selected = proposed
                            accepted = True
                            event = "accepted_compound"
                    else:
                        event = "metropolis_reject"
                        counts["metropolis_rejects"] += 1
        else:
            counts["lazy_stays"] += 1

        work_before = accepted_gross_work
        net_work_before = accepted_net_changed_work
        if accepted:
            accepted_gross_work += proposal_work
            accepted_net_changed_work += net_changed_edges
            accepted_work_counts[proposal_work] += 1
            counts["accepted_events"] += 1
            counts[f"accepted_{move_class}"] += 1
            visited.add(v16x.edge_digest(selected))

        trace.append({
            **dag.prefix,
            "kernel_arm": kernel_arm,
            "start_family": start_family,
            "chain_seed_family": seed_family,
            "chain_seed": seed,
            "attempt": attempt_index,
            "event": event,
            "move_class": move_class,
            "proposal_sha256": proposal_sha256,
            "first_cycle_length": first_length,
            "second_cycle_length": second_length,
            "proposal_gross_removed_edge_work": proposal_work,
            "proposal_net_changed_edges": net_changed_edges,
            "reverse_supported": int(reverse_supported),
            "roundtrip_pass": int(roundtrip_pass),
            "exact_pathwise_balance_pass": int(exact_balance_pass),
            "proposal_endpoint_integrity_pass": int(endpoint_integrity),
            **fraction_fields("q_forward", forward),
            **fraction_fields("q_reverse", reverse),
            **fraction_fields("acceptance", acceptance),
            "accepted": int(accepted),
            "accepted_gross_edge_work_before": work_before,
            "accepted_gross_edge_work_after": accepted_gross_work,
            "accepted_net_changed_edge_work_before": net_work_before,
            "accepted_net_changed_edge_work_after": accepted_net_changed_work,
            "state_before_sha256": state_before_digest,
            "state_after_sha256": v16x.edge_digest(selected),
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })

    elapsed = time.monotonic() - started
    attempts = len(trace)
    final_change = len(selected - start) / len(start)
    work_pass = accepted_gross_work == work_target
    proposal_integrity_pass = all((
        counts["roundtrip_failures"] == 0,
        counts["exact_balance_failures"] == 0,
        counts["endpoint_integrity_failures"] == 0,
        counts["work_definition_failures"] == 0,
    ))
    minimum_events = minimum_accepted_events(kernel_arm, work_target)
    arm_exercise_pass = (
        counts["accepted_length_5_batch_guided"]
        >= MIN_EXPANDED_LENGTH5_CYCLES
        if kernel_arm == KERNEL_ARMS[0]
        else counts["accepted_compound_two_subcycles"] >= minimum_events
    )
    movement_pass = all((
        work_pass,
        proposal_integrity_pass,
        counts["accepted_events"] >= minimum_events,
        len(visited) >= MIN_UNIQUE_STATES,
        final_change >= MIN_FINAL_START_CHANGE,
        arm_exercise_pass,
        v16x.assignment_integrity(kernel.space, selected),
    ))
    resource_pass = attempts <= max_attempts and elapsed <= MAX_CHAIN_SECONDS
    stats: MutableMapping[str, Any] = {
        **dag.prefix,
        "kernel_arm": kernel_arm,
        "start_family": start_family,
        "chain_seed_family": seed_family,
        "chain_seed": seed,
        "attempts": attempts,
        "maximum_attempts": max_attempts,
        "lazy_stays": counts["lazy_stays"],
        "nonlazy_attempts": counts["nonlazy_attempts"],
        "proposal_dead_end": counts["proposal_dead_end"],
        "first_dead_end": counts["first_dead_end"],
        "first_reverse_unsupported": counts["first_reverse_unsupported"],
        "second_dead_end": counts["second_dead_end"],
        "second_reverse_unsupported": counts["second_reverse_unsupported"],
        "symmetric_net_filter": counts["symmetric_net_filter"],
        "compound_reverse_unsupported": counts["compound_reverse_unsupported"],
        "compound_reverse_involution_failed": counts[
            "compound_reverse_involution_failed"
        ],
        "raw_proposals": counts["raw_proposals"],
        "reverse_filtered_dead_end": counts["reverse_filtered_dead_end"],
        "retained_reverse_supported": counts["retained_reverse_supported"],
        "roundtrip_failures": counts["roundtrip_failures"],
        "exact_balance_failures": counts["exact_balance_failures"],
        "endpoint_integrity_failures": counts["endpoint_integrity_failures"],
        "work_definition_failures": counts["work_definition_failures"],
        "accepted_events": counts["accepted_events"],
        "accepted_single_cycles": counts["accepted_length_2_4"]
        + counts["accepted_length_5_batch_guided"],
        "accepted_length5_cycles": counts["accepted_length_5_batch_guided"],
        "accepted_compound_blocks": counts["accepted_compound_two_subcycles"],
        "accepted_gross_edge_work": accepted_gross_work,
        "accepted_gross_edge_work_target": work_target,
        "accepted_net_changed_edge_work": accepted_net_changed_work,
        "net_to_gross_accepted_work_ratio": (
            accepted_net_changed_work / accepted_gross_work
            if accepted_gross_work else 0.0
        ),
        "work_boundary_rejects": counts["work_boundary_rejects"],
        "metropolis_rejects": counts["metropolis_rejects"],
        "accepted_work_increment_counts_json": json.dumps(
            dict(sorted(accepted_work_counts.items())), separators=(",", ":")
        ),
        "minimum_required_accepted_events": minimum_events,
        "unique_state_count": len(visited),
        "final_start_changed_edge_fraction": final_change,
        "final_endpoint_sha256": v16x.edge_digest(selected),
        "final_endpoint_integrity_pass": int(
            v16x.assignment_integrity(kernel.space, selected)
        ),
        "matched_work_pass": int(work_pass),
        "proposal_integrity_pass": int(proposal_integrity_pass),
        "arm_exercise_pass": int(arm_exercise_pass),
        "movement_pass": int(movement_pass),
        "elapsed_seconds": elapsed,
        "resource_pass": int(resource_pass),
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }
    return ChainResult(selected, stats, trace)


def pilot() -> None:
    v17h.verify_outputs()
    v17j.verify_outputs()
    dag, metadata = load_runs()[0]
    space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
    kernel = v17a.build_kernel(space)
    start = space.source_edges
    rows = []
    for kernel_arm in KERNEL_ARMS:
        result = run_chain(
            dag,
            kernel,
            start,
            kernel_arm,
            START_FAMILIES[0],
            "design_calibration_seed",
            work_target=PILOT_WORK_TARGET,
            max_attempts=PILOT_MAX_ATTEMPTS,
        )
        rows.append({
            "stage": "v17k_design_calibration",
            "script_sha256": file_sha256(SCRIPT),
            "growth_seed": dag.growth_seed,
            "run_offset": dag.run_offset,
            "start_family": START_FAMILIES[0],
            "kernel_arm": kernel_arm,
            "pilot_work_target": PILOT_WORK_TARGET,
            "attempts": result.stats["attempts"],
            "accepted_events": result.stats["accepted_events"],
            "accepted_gross_edge_work": result.stats[
                "accepted_gross_edge_work"
            ],
            "matched_work_pass": result.stats["matched_work_pass"],
            "proposal_integrity_pass": result.stats["proposal_integrity_pass"],
            "resource_pass": result.stats["resource_pass"],
            "elapsed_seconds": result.stats["elapsed_seconds"],
            "cross_start_distance_computed": 0,
            "within_start_distance_computed": 0,
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })
    v16i.write_csv(DESIGN_CALIBRATION, rows)
    print("[v17k] effect-blind technical pilot complete")


def endpoint_row(result: ChainResult) -> MutableMapping[str, Any]:
    stats = result.stats
    return {
        "stage": "v17k",
        "target_nodes": stats["target_nodes"],
        "growth_seed": stats["growth_seed"],
        "run_offset": stats["run_offset"],
        "arm": stats["arm"],
        "run_seed": stats["run_seed"],
        "kernel_arm": stats["kernel_arm"],
        "start_family": stats["start_family"],
        "chain_seed_family": stats["chain_seed_family"],
        "accepted_gross_edge_work": stats["accepted_gross_edge_work"],
        "accepted_net_changed_edge_work": stats[
            "accepted_net_changed_edge_work"
        ],
        "selected_edge_count": len(result.final),
        "final_start_changed_edge_fraction": stats[
            "final_start_changed_edge_fraction"
        ],
        "endpoint_edge_sha256": stats["final_endpoint_sha256"],
        "endpoint_integrity_pass": stats["final_endpoint_integrity_pass"],
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }


def pairwise_rows(
    dag: v16i.RunDAG,
    kernel_arm: str,
    endpoints: Sequence[Endpoint],
) -> List[Dict[str, Any]]:
    rows = []
    for left, right in combinations(endpoints, 2):
        relation = (
            "within_start"
            if left.row["start_family"] == right.row["start_family"]
            else "cross_start"
        )
        distance = len(left.edges - right.edges) / len(left.edges)
        rows.append({
            **dag.prefix,
            "kernel_arm": kernel_arm,
            "relation": relation,
            "left_start_family": left.row["start_family"],
            "left_chain_seed_family": left.row["chain_seed_family"],
            "right_start_family": right.row["start_family"],
            "right_chain_seed_family": right.row["chain_seed_family"],
            "left_endpoint_sha256": left.row["endpoint_edge_sha256"],
            "right_endpoint_sha256": right.row["endpoint_edge_sha256"],
            "changed_edge_fraction": distance,
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })
    return rows


def kernel_distance_row(
    dag: v16i.RunDAG,
    kernel_arm: str,
    rows: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    within = [
        float(row["changed_edge_fraction"])
        for row in rows
        if row["relation"] == "within_start"
    ]
    cross = [
        float(row["changed_edge_fraction"])
        for row in rows
        if row["relation"] == "cross_start"
    ]
    within_median = statistics.median(within)
    cross_median = statistics.median(cross)
    return {
        **dag.prefix,
        "kernel_arm": kernel_arm,
        "within_start_pair_count": len(within),
        "cross_start_pair_count": len(cross),
        "median_within_start_distance": within_median,
        "median_cross_start_distance": cross_median,
        "cross_to_within_distance_ratio": (
            cross_median / within_median if within_median else math.inf
        ),
        "minimum_cross_start_distance": min(cross),
        "maximum_cross_start_distance": max(cross),
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }


def comparison_row(
    dag: v16i.RunDAG,
    summaries: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    by_arm = {str(row["kernel_arm"]): row for row in summaries}
    expanded = float(
        by_arm[KERNEL_ARMS[0]]["median_cross_start_distance"]
    )
    compound = float(
        by_arm[KERNEL_ARMS[1]]["median_cross_start_distance"]
    )
    ratio = (
        compound / expanded
        if expanded
        else (0.0 if compound == 0 else math.inf)
    )
    expanded_within = float(
        by_arm[KERNEL_ARMS[0]]["median_within_start_distance"]
    )
    compound_within = float(
        by_arm[KERNEL_ARMS[1]]["median_within_start_distance"]
    )
    return {
        **dag.prefix,
        "accepted_gross_edge_work_per_chain": ACCEPTED_GROSS_EDGE_WORK_TARGET,
        "expanded_median_cross_start_distance": expanded,
        "compound_median_cross_start_distance": compound,
        "compound_over_expanded_cross_start_distance_ratio": ratio,
        "directional_cross_start_reduction": int(compound < expanded),
        "material_cross_start_reduction_pass": int(
            ratio <= MAX_MATERIAL_CROSS_START_RATIO
        ),
        "expanded_median_within_start_distance": expanded_within,
        "compound_median_within_start_distance": compound_within,
        "compound_over_expanded_within_start_distance_ratio": (
            compound_within / expanded_within
            if expanded_within
            else (0.0 if compound_within == 0 else math.inf)
        ),
        "maximum_material_cross_start_ratio": MAX_MATERIAL_CROSS_START_RATIO,
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }


def gate_rows(
    transitions: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
    frozen_start_passes: int,
    proposal_laws: Sequence[Mapping[str, Any]],
) -> Tuple[str, List[Dict[str, Any]]]:
    calls = implementation_call_counts()
    exclusion_pass = (
        calls == {"spectrum_calls": 0, "effect_metric_calls": 0}
        and all(
            not int(row["source_spectrum_computed"])
            and not int(row["observed_effect_computed"])
            for row in transitions
        )
    )
    law_pass = (
        len(proposal_laws) == 2
        and all(int(row["audit_pass"]) for row in proposal_laws)
        and all(not int(row["proposal_law_reimplemented"]) for row in proposal_laws)
    )
    work_count = sum(
        int(row["matched_work_pass"])
        and int(row["final_endpoint_integrity_pass"])
        for row in transitions
    )
    proposal_integrity_count = sum(
        int(row["proposal_integrity_pass"]) for row in transitions
    )
    movement_count = sum(int(row["movement_pass"]) for row in transitions)
    exercise_count = sum(int(row["arm_exercise_pass"]) for row in transitions)
    resource_count = sum(int(row["resource_pass"]) for row in transitions)
    primary_count = sum(
        int(row["material_cross_start_reduction_pass"])
        for row in comparisons
    )

    if not exclusion_pass or frozen_start_passes != 12 or not law_pass:
        overall = "v17k_instrumentation_failed"
    elif (
        work_count != EXPECTED_CHAINS
        or proposal_integrity_count != EXPECTED_CHAINS
    ):
        overall = "v17k_matched_work_or_proposal_integrity_not_qualified"
    elif movement_count != EXPECTED_CHAINS or exercise_count != EXPECTED_CHAINS:
        overall = "v17k_finite_movement_not_qualified"
    elif resource_count != EXPECTED_CHAINS:
        overall = "v17k_resource_not_qualified"
    elif primary_count == 6:
        overall = "v17k_compound_matched_work_start_distance_reduced"
    else:
        overall = "v17k_compound_no_uniform_matched_work_gain"

    ratios = [
        float(row["compound_over_expanded_cross_start_distance_ratio"])
        for row in comparisons
    ]
    max_runtime = max(float(row["elapsed_seconds"]) for row in transitions)
    gates = [
        {"gate": "effect_blind_integrity", "status": "pass" if exclusion_pass else "fail", "observed": f"spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}", "required": "0;0", "decision": "continue" if exclusion_pass else "invalidate"},
        {"gate": "frozen_start_integrity", "status": "pass" if frozen_start_passes == 12 else "fail", "observed": f"{frozen_start_passes}/12", "required": "12/12", "decision": "continue" if frozen_start_passes == 12 else "invalidate"},
        {"gate": "qualified_proposal_law_reuse", "status": "pass" if law_pass else "fail", "observed": f"{sum(int(row['audit_pass']) for row in proposal_laws)}/2;reimplemented={sum(int(row['proposal_law_reimplemented']) for row in proposal_laws)}", "required": "2/2;reimplemented=0", "decision": "continue" if law_pass else "invalidate"},
        {"gate": "exact_matched_gross_work_and_endpoint_integrity", "status": "pass" if work_count == EXPECTED_CHAINS else "fail", "observed": f"{work_count}/{EXPECTED_CHAINS};work={ACCEPTED_GROSS_EDGE_WORK_TARGET}", "required": f"{EXPECTED_CHAINS}/{EXPECTED_CHAINS};each={ACCEPTED_GROSS_EDGE_WORK_TARGET}", "decision": "continue" if work_count == EXPECTED_CHAINS else "repair_stopping_rule"},
        {"gate": "exact_reverse_balance_and_work_definition", "status": "pass" if proposal_integrity_count == EXPECTED_CHAINS else "fail", "observed": f"{proposal_integrity_count}/{EXPECTED_CHAINS}", "required": f"{EXPECTED_CHAINS}/{EXPECTED_CHAINS}", "decision": "continue" if proposal_integrity_count == EXPECTED_CHAINS else "invalidate"},
        {"gate": "finite_movement_and_arm_exercise", "status": "pass" if movement_count == EXPECTED_CHAINS and exercise_count == EXPECTED_CHAINS else "fail", "observed": f"movement={movement_count}/{EXPECTED_CHAINS};exercise={exercise_count}/{EXPECTED_CHAINS}", "required": f"{EXPECTED_CHAINS}/{EXPECTED_CHAINS};{EXPECTED_CHAINS}/{EXPECTED_CHAINS}", "decision": "continue" if movement_count == EXPECTED_CHAINS and exercise_count == EXPECTED_CHAINS else "do_not_compare_start_memory"},
        {"gate": "resource_bound", "status": "pass" if resource_count == EXPECTED_CHAINS else "fail", "observed": f"{resource_count}/{EXPECTED_CHAINS};max={max_runtime:.6f}s", "required": f"{EXPECTED_CHAINS}/{EXPECTED_CHAINS};each<={MAX_CHAIN_SECONDS:.0f}s", "decision": "continue" if resource_count == EXPECTED_CHAINS else "optimize_or_retire"},
        {"gate": "primary_compound_cross_start_reduction", "status": "pass" if primary_count == 6 else "fail", "observed": f"{primary_count}/6;ratio={min(ratios):.6f}-{max(ratios):.6f}", "required": f"6/6;each<={MAX_MATERIAL_CROSS_START_RATIO:.2f}", "decision": "fresh_work_level_replication" if primary_count == 6 else "retire_current_two_cycle_law_as_uniform_remedy"},
        {"gate": "v17k_overall", "status": overall, "observed": f"exclusion={int(exclusion_pass)};starts={frozen_start_passes}/12;laws={int(law_pass)};work={work_count}/{EXPECTED_CHAINS};proposal={proposal_integrity_count}/{EXPECTED_CHAINS};movement={movement_count}/{EXPECTED_CHAINS};exercise={exercise_count}/{EXPECTED_CHAINS};resource={resource_count}/{EXPECTED_CHAINS};primary={primary_count}/6", "required": f"1;12/12;1;{EXPECTED_CHAINS}/{EXPECTED_CHAINS};{EXPECTED_CHAINS}/{EXPECTED_CHAINS};{EXPECTED_CHAINS}/{EXPECTED_CHAINS};{EXPECTED_CHAINS}/{EXPECTED_CHAINS};{EXPECTED_CHAINS}/{EXPECTED_CHAINS};6/6", "decision": overall},
    ]
    return overall, gates


def markdown_table(
    rows: Sequence[Mapping[str, Any]],
    fields: Sequence[str],
) -> List[str]:
    return v17h.markdown_table(rows, fields)


def claim_rows(
    overall: str,
    transitions: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    valid_comparison = overall in {
        "v17k_compound_matched_work_start_distance_reduced",
        "v17k_compound_no_uniform_matched_work_gain",
    }
    positive = overall == "v17k_compound_matched_work_start_distance_reduced"
    exact_work = all(
        int(row["matched_work_pass"])
        and int(row["final_endpoint_integrity_pass"])
        for row in transitions
    )
    return [
        {"claim_id": "C1", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "factual", "strength": "assertive", "claim": "v17k computes no source spectrum or observed-effect metric.", "status": "supported", "evidence": "static call audit and output exclusion fields", "scope_limit": "v17k script and outputs"},
        {"claim_id": "C2", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "algorithmic", "strength": "assertive", "claim": "v17k calls the qualified expanded and compound proposal implementations directly without reimplementing their proposal laws.", "status": "supported", "evidence": "v17k_proposal_law_audit.csv and frozen source hashes", "scope_limit": "proposal calls; the finite work terminal rule is new evaluation conditioning"},
        {"claim_id": "C3", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "finite_simulation", "strength": "assertive", "claim": "Both arms complete exactly equal accepted gross removed-edge work with valid endpoints.", "status": "supported" if exact_work else "not_supported", "evidence": "v17k_chain_transition_summary.csv", "scope_limit": "48 finite chains; terminal conditioning applies"},
        {"claim_id": "C4", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "empirical", "strength": "moderated", "claim": "The compound law reduces median absolute cross-start distance by at least 10 percent relative to the expanded single-cycle law in every source.", "status": "supported" if positive else ("not_supported" if valid_comparison else "not_tested"), "evidence": "v17k_matched_work_comparison.csv", "scope_limit": "six reused spaces, two starts, two fresh seed families, gross work 192"},
        {"claim_id": "C5", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "empirical", "strength": "bounded", "claim": "The current two-subcycle law fails the preregistered criterion for a uniform matched-work start-memory gain.", "status": "supported" if overall == "v17k_compound_no_uniform_matched_work_gain" else ("contradicted" if positive else "not_tested"), "evidence": "v17k_gate_evaluation.csv", "scope_limit": "does not reject all compound, long-cycle or algebraic moves"},
        {"claim_id": "C6", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "global", "strength": "prohibited", "claim": "v17k proves global connectivity, irreducibility, mixing, convergence or stationary sampling.", "status": "contradicted", "evidence": "finite work-conditioned endpoint comparison cannot establish global state-space properties", "scope_limit": "requires separate formal or scaling evidence"},
        {"claim_id": "C7", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "physics", "strength": "prohibited", "claim": "v17k establishes source effects, geometry, Lorentz symmetry, spacetime, particles, Bell correlations or a universe model.", "status": "contradicted", "evidence": "effect observables prohibited and no physical diagnostics computed", "scope_limit": "requires later gates"},
    ]


def write_documents(
    overall: str,
    gates: Sequence[Mapping[str, Any]],
    transitions: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
) -> None:
    ratios = [
        float(row["compound_over_expanded_cross_start_distance_ratio"])
        for row in comparisons
    ]
    directional = sum(
        int(row["directional_cross_start_reduction"])
        for row in comparisons
    )
    primary = sum(
        int(row["material_cross_start_reduction_pass"])
        for row in comparisons
    )
    max_runtime = max(float(row["elapsed_seconds"]) for row in transitions)
    max_attempts = max(int(row["attempts"]) for row in transitions)
    min_compound_blocks = min(
        int(row["accepted_compound_blocks"])
        for row in transitions
        if row["kernel_arm"] == KERNEL_ARMS[1]
    )
    min_expanded_length5 = min(
        int(row["accepted_length5_cycles"])
        for row in transitions
        if row["kernel_arm"] == KERNEL_ARMS[0]
    )

    if overall == "v17k_compound_matched_work_start_distance_reduced":
        next_text = (
            "Preregister a fresh work-level replication with new seeds at gross "
            "accepted work 192 and 384. Keep source effects closed until the "
            "relative reduction survives both work levels."
        )
        recommendation = (
            "replicate the compound matched-work gain at fresh work levels"
        )
    elif overall == "v17k_compound_no_uniform_matched_work_gain":
        next_text = (
            "Retire this exact two-subcycle net-6 law as a uniform start-memory "
            "remedy. Keep source effects closed. Diagnose whether the remaining "
            "barrier is move diameter or accessibility-component structure before "
            "choosing a monolithic long-cycle proposal."
        )
        recommendation = (
            "retire the current two-subcycle law as a uniform start-memory remedy"
        )
    else:
        next_text = (
            "Stop at the first failed instrumentation, work, proposal-integrity, "
            "movement or resource layer. Repair that layer effect-blind and "
            "preregister a replacement before interpreting endpoint distances."
        )
        recommendation = "repair the first failed frozen layer"

    report = [
        "# v17k effect-blind compound matched-work start-memory gate",
        "",
        f"Status: `{overall}`.",
        "",
        "## Purpose and frozen design",
        "",
        "Purpose `purpose://validation`: test whether the qualified v17j two-subcycle law reduces finite start memory more efficiently than v17h's reverse-closed expanded single-cycle law. The gate uses the same six spaces and frozen start pairs with two new seed families. Source spectra and observed effects are prohibited.",
        "",
        f"Every chain targets exactly `{ACCEPTED_GROSS_EDGE_WORK_TARGET}` accepted gross removed-edge units. Single-cycle work is the accepted cycle's removed-edge count. Compound work is the sum of the two accepted subcycle removed-edge counts. Net endpoint change is logged separately and is never substituted for gross work.",
        "",
        "The terminal rule turns a Metropolis-accepted proposal into a self-loop if it overshoots the work target or leaves a remainder not representable by that arm's declared work increments. This is finite work conditioning, not stationary sampling, and may introduce endpoint bias.",
        "",
        "## Frozen gates",
        "",
        *markdown_table(
            gates,
            ("gate", "status", "observed", "required", "decision"),
        ),
        "",
        "## Primary matched-work response",
        "",
        *markdown_table(
            comparisons,
            (
                "growth_seed",
                "run_offset",
                "expanded_median_cross_start_distance",
                "compound_median_cross_start_distance",
                "compound_over_expanded_cross_start_distance_ratio",
                "directional_cross_start_reduction",
                "material_cross_start_reduction_pass",
            ),
        ),
        "",
        f"Directional reduction occurred in `{directional}/6`; material reduction passed `{primary}/6`. Compound/expanded cross-start ratios ranged `{min(ratios):.6f}-{max(ratios):.6f}` with median `{statistics.median(ratios):.6f}`.",
        "",
        "## Finite execution",
        "",
        f"The formal comparison contains `{len(transitions)}` chains. Maximum runtime was `{max_runtime:.6f}` seconds and maximum attempts were `{max_attempts}`. The weakest compound chain accepted `{min_compound_blocks}` blocks; the weakest expanded chain accepted `{min_expanded_length5}` length-5 cycles. Gross work, net work and endpoint distance remain separate products.",
        "",
        "## Claim boundary",
        "",
        "This is a relative finite efficiency/start-memory comparison. Even a positive result would not establish global connectivity, irreducibility, convergence, mixing, a stationary distribution, source effects, geometry or physics. A negative result rejects only this exact two-subcycle law as a uniform remedy under the frozen design.",
        "",
        "## Next decision",
        "",
        next_text,
        "",
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    INTERPRETATION.write_text(
        "# v17k interpretation audit\n\n"
        f"Formal status: `{overall}`.\n\n"
        "Exact gross accepted-work matching removes unequal realized rewrite work as an explanation for the arm comparison, but it does not turn finite endpoints into stationary samples. The arm-specific reachable-remainder rule conditions terminal proposals and may bias the last transitions. Net changed edges are not counted as gross work. Cross-start distance is an evaluation observable validated by v17i's pair-engineered positive control, not a proof of connectivity or mixing. No source spectrum, observed effect, Bell observable, Lorentz diagnostic or physical invariant was computed.\n",
        encoding="utf-8",
    )
    NEXT_DIRECTION.write_text(
        "# v17k next direction\n\n"
        f"Formal status: `{overall}`.\n\n{next_text}\n",
        encoding="utf-8",
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.17k\n\n"
        f"- status: `{overall}`\n"
        f"- directional compound reduction: `{directional}/6`\n"
        f"- material compound reduction: `{primary}/6`\n"
        f"- next: {recommendation}\n"
        "- source spectrum and observed effects remain closed\n"
        "- claim ceiling: relative finite matched-work response, not connectivity or physics\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.17k\n\n"
        "V17k gir en regel som gjoer to lokale omkoblinger samlet, og en regel som gjoer en omkobling om gangen, noyaktig samme mengde faktisk akseptert grafarbeid. Da kan vi sammenligne hvor mye minnene om to ulike startpunkter gjenstaar uten at den ene regelen bare har faatt jobbe mer.\n\n"
        f"Statusen er `{overall}`. Resultatet gjelder et avgrenset finite eksperiment. Det beviser ikke at hele tilstandsrommet er sammenhengende eller mikset, og det er ikke et fysisk funn.\n",
        encoding="utf-8",
    )


def run_source(run_index: int) -> Dict[str, Any]:
    dag, metadata = load_runs()[run_index]
    frozen_starts = v16z.frozen_start_digests()
    traces: List[Dict[str, Any]] = []
    transitions: List[Dict[str, Any]] = []
    endpoint_rows: List[Dict[str, Any]] = []
    pairwise: List[Dict[str, Any]] = []
    kernel_summaries: List[Dict[str, Any]] = []
    space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
    kernel = v17a.build_kernel(space)
    starts = {
        START_FAMILIES[0]: space.source_edges,
        START_FAMILIES[1]: v16z.random_cost_start(dag, space),
    }
    source_frozen_start_passes = sum(
        int(
            v16x.edge_digest(start)
            == frozen_starts[(dag.growth_seed, dag.run_offset, start_family)]
        )
        for start_family, start in starts.items()
    )

    source_kernel_summaries: List[Mapping[str, Any]] = []
    for kernel_arm in KERNEL_ARMS:
        endpoints: List[Endpoint] = []
        for start_family, start in starts.items():
            for seed_family in CHAIN_SEED_FAMILIES:
                result = run_chain(
                    dag,
                    kernel,
                    start,
                    kernel_arm,
                    start_family,
                    seed_family,
                )
                traces.extend(result.trace)
                transitions.append(dict(result.stats))
                row = endpoint_row(result)
                endpoint_rows.append(dict(row))
                endpoints.append(Endpoint(result.final, row))
        arm_pairwise = pairwise_rows(dag, kernel_arm, endpoints)
        pairwise.extend(arm_pairwise)
        summary = kernel_distance_row(dag, kernel_arm, arm_pairwise)
        kernel_summaries.append(summary)
        source_kernel_summaries.append(summary)

    comparison = comparison_row(dag, source_kernel_summaries)
    source_summary = {
        **dag.prefix,
        "chain_count": len(transitions),
        "frozen_start_passes": source_frozen_start_passes,
        "matched_work_passes": sum(
            int(row["matched_work_pass"]) for row in transitions
        ),
        "proposal_integrity_passes": sum(
            int(row["proposal_integrity_pass"]) for row in transitions
        ),
        "movement_passes": sum(
            int(row["movement_pass"]) for row in transitions
        ),
        "arm_exercise_passes": sum(
            int(row["arm_exercise_pass"]) for row in transitions
        ),
        "resource_passes": sum(
            int(row["resource_pass"]) for row in transitions
        ),
        "minimum_compound_blocks": min(
            int(row["accepted_compound_blocks"])
            for row in transitions
            if row["kernel_arm"] == KERNEL_ARMS[1]
        ),
        "minimum_expanded_length5_cycles": min(
            int(row["accepted_length5_cycles"])
            for row in transitions
            if row["kernel_arm"] == KERNEL_ARMS[0]
        ),
        "maximum_attempts_used": max(
            int(row["attempts"]) for row in transitions
        ),
        "maximum_chain_seconds": max(
            float(row["elapsed_seconds"]) for row in transitions
        ),
        "compound_over_expanded_cross_start_distance_ratio": comparison[
            "compound_over_expanded_cross_start_distance_ratio"
        ],
        "material_cross_start_reduction_pass": comparison[
            "material_cross_start_reduction_pass"
        ],
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }
    return {
        "run_index": run_index,
        "frozen_start_passes": source_frozen_start_passes,
        "traces": traces,
        "transitions": transitions,
        "endpoint_rows": endpoint_rows,
        "pairwise": pairwise,
        "kernel_summaries": kernel_summaries,
        "comparison": comparison,
        "source_summary": source_summary,
    }


def run(*, workers: int = 1) -> None:
    verify_frozen_sources()
    proposal_laws = proposal_law_rows()
    traces: List[Dict[str, Any]] = []
    transitions: List[Dict[str, Any]] = []
    endpoint_rows: List[Dict[str, Any]] = []
    pairwise: List[Dict[str, Any]] = []
    kernel_summaries: List[Dict[str, Any]] = []
    comparisons: List[Dict[str, Any]] = []
    source_summaries: List[Dict[str, Any]] = []
    frozen_start_passes = 0

    indices = list(range(len(load_runs())))
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            source_results = list(executor.map(run_source, indices))
    else:
        source_results = [run_source(index) for index in indices]

    for source_result in sorted(
        source_results,
        key=lambda item: int(item["run_index"]),
    ):
        frozen_start_passes += int(source_result["frozen_start_passes"])
        traces.extend(source_result["traces"])
        transitions.extend(source_result["transitions"])
        endpoint_rows.extend(source_result["endpoint_rows"])
        pairwise.extend(source_result["pairwise"])
        kernel_summaries.extend(source_result["kernel_summaries"])
        comparisons.append(source_result["comparison"])
        source_summaries.append(source_result["source_summary"])
        print(f"[v17k] source {int(source_result['run_index']) + 1}/6 complete")

    overall, gates = gate_rows(
        transitions,
        comparisons,
        frozen_start_passes,
        proposal_laws,
    )
    v16i.write_csv(PROPOSAL_LAW_AUDIT, proposal_laws)
    v16i.write_csv(PROPOSAL_TRACE, traces)
    v16i.write_csv(ENDPOINT_AUDIT, endpoint_rows)
    v16i.write_csv(PAIRWISE_DISTANCE, pairwise)
    v16i.write_csv(KERNEL_DISTANCE_SUMMARY, kernel_summaries)
    v16i.write_csv(MATCHED_WORK_COMPARISON, comparisons)
    v16i.write_csv(TRANSITION_SUMMARY, transitions)
    v16i.write_csv(SOURCE_SUMMARY, source_summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    goal_status = (
        "satisfied"
        if overall == "v17k_compound_matched_work_start_distance_reduced"
        else (
            "missed"
            if overall == "v17k_compound_no_uniform_matched_work_gain"
            else "blocked"
        )
    )
    v16i.write_csv(GOAL_EVALUATION, [{
        "goal_id": "G1",
        "purpose_ref": PURPOSE_REF,
        "metric": (
            "material compound cross-start distance reduction at exact matched "
            "accepted gross work"
        ),
        "baseline": "qualified v17h expanded reverse-closed single-cycle law",
        "target": (
            "compound/expanded median cross-start distance <=0.90 in 6/6 sources"
        ),
        "timeframe": "one frozen v17k round",
        "status": goal_status,
        "evidence": "v17k_matched_work_comparison.csv;v17k_gate_evaluation.csv",
        "next_decision": overall,
    }])
    v16i.write_csv(CLAIM_LEDGER, claim_rows(overall, transitions))
    write_documents(overall, gates, transitions, comparisons)
    print(f"[v17k] status={overall}")


def verify_trace_integrity(
    traces: Sequence[Mapping[str, str]],
    transitions: Sequence[Mapping[str, str]],
) -> None:
    grouped: Dict[Tuple[str, ...], List[Mapping[str, str]]] = defaultdict(list)
    for row in traces:
        key = (
            row["growth_seed"],
            row["run_offset"],
            row["kernel_arm"],
            row["start_family"],
            row["chain_seed_family"],
        )
        grouped[key].append(row)

    transition_by_key = {
        (
            row["growth_seed"],
            row["run_offset"],
            row["kernel_arm"],
            row["start_family"],
            row["chain_seed_family"],
        ): row
        for row in transitions
    }
    if set(grouped) != set(transition_by_key):
        raise ValueError("v17k trace/transition chain keys differ")

    for key, rows in grouped.items():
        expected_before = 0
        expected_net_before = 0
        for expected_attempt, row in enumerate(rows, start=1):
            if int(row["attempt"]) != expected_attempt:
                raise ValueError("v17k attempt sequence changed")
            before = int(row["accepted_gross_edge_work_before"])
            after = int(row["accepted_gross_edge_work_after"])
            net_before = int(row["accepted_net_changed_edge_work_before"])
            net_after = int(row["accepted_net_changed_edge_work_after"])
            if before != expected_before or net_before != expected_net_before:
                raise ValueError("v17k cumulative work discontinuity")
            if int(row["accepted"]):
                if after - before != int(row["proposal_gross_removed_edge_work"]):
                    raise ValueError("v17k accepted gross work increment mismatch")
                if net_after - net_before != int(row["proposal_net_changed_edges"]):
                    raise ValueError("v17k accepted net work increment mismatch")
                if row["state_before_sha256"] == row["state_after_sha256"]:
                    raise ValueError("v17k accepted transition became a self-loop")
            elif after != before or net_after != net_before:
                raise ValueError("v17k rejected transition changed cumulative work")
            expected_before = after
            expected_net_before = net_after
        transition = transition_by_key[key]
        if expected_before != int(transition["accepted_gross_edge_work"]):
            raise ValueError("v17k trace final gross work mismatch")
        if expected_net_before != int(
            transition["accepted_net_changed_edge_work"]
        ):
            raise ValueError("v17k trace final net work mismatch")


def verify_outputs() -> None:
    verify_frozen_sources()
    paths = (
        PROPOSAL_LAW_AUDIT,
        PROPOSAL_TRACE,
        ENDPOINT_AUDIT,
        PAIRWISE_DISTANCE,
        KERNEL_DISTANCE_SUMMARY,
        MATCHED_WORK_COMPARISON,
        TRANSITION_SUMMARY,
        SOURCE_SUMMARY,
        GATE_EVALUATION,
        GOAL_EVALUATION,
        CLAIM_LEDGER,
        REPORT,
        INTERPRETATION,
        NEXT_DIRECTION,
        RECOMMENDATION,
        NONSPECIALIST,
    )
    if any(not path.exists() for path in paths):
        raise ValueError("v17k output missing")

    proposal_laws = v16i.read_csv(PROPOSAL_LAW_AUDIT)
    traces = v16i.read_csv(PROPOSAL_TRACE)
    endpoints = v16i.read_csv(ENDPOINT_AUDIT)
    pairwise = v16i.read_csv(PAIRWISE_DISTANCE)
    kernel_summaries = v16i.read_csv(KERNEL_DISTANCE_SUMMARY)
    comparisons = v16i.read_csv(MATCHED_WORK_COMPARISON)
    transitions = v16i.read_csv(TRANSITION_SUMMARY)
    summaries = v16i.read_csv(SOURCE_SUMMARY)
    if len(proposal_laws) != 2:
        raise ValueError("v17k proposal-law audit row count mismatch")
    if len(transitions) != EXPECTED_CHAINS or len(endpoints) != EXPECTED_CHAINS:
        raise ValueError("v17k chain/endpoint row count mismatch")
    if (len(pairwise), len(kernel_summaries), len(comparisons), len(summaries)) != (
        72,
        12,
        6,
        6,
    ):
        raise ValueError("v17k comparison row count mismatch")
    if len(traces) != sum(int(row["attempts"]) for row in transitions):
        raise ValueError("v17k trace length mismatch")
    verify_trace_integrity(traces, transitions)
    if any(
        int(row["accepted_gross_edge_work"])
        != ACCEPTED_GROSS_EDGE_WORK_TARGET
        or not int(row["matched_work_pass"])
        or not int(row["final_endpoint_integrity_pass"])
        for row in transitions
    ):
        raise ValueError("v17k exact matched-work or endpoint integrity failed")
    if any(
        int(row["roundtrip_failures"])
        or int(row["exact_balance_failures"])
        or int(row["endpoint_integrity_failures"])
        or int(row["work_definition_failures"])
        or not int(row["proposal_integrity_pass"])
        for row in transitions
    ):
        raise ValueError("v17k proposal integrity failed")

    frozen_start_passes = sum(
        int(row["frozen_start_passes"]) for row in summaries
    )
    _, expected_gates = gate_rows(
        transitions,
        comparisons,
        frozen_start_passes,
        proposal_laws,
    )
    stored_gates = v16i.read_csv(GATE_EVALUATION)
    if stored_gates != [
        {key: str(value) for key, value in row.items()}
        for row in expected_gates
    ]:
        raise ValueError("v17k gate evaluation changed")
    if implementation_call_counts() != {
        "spectrum_calls": 0,
        "effect_metric_calls": 0,
    }:
        raise ValueError("v17k effect exclusion failed")
    if any(
        int(row["source_spectrum_computed"])
        or int(row["observed_effect_computed"])
        for row in traces
    ):
        raise ValueError("v17k trace contains prohibited effect data")
    if any(
        int(row["cross_start_distance_computed"])
        or int(row["within_start_distance_computed"])
        or int(row["source_spectrum_computed"])
        or int(row["observed_effect_computed"])
        for row in v16i.read_csv(DESIGN_CALIBRATION)
    ):
        raise ValueError("v17k design calibration exceeded declared scope")
    overall = next(
        row["status"]
        for row in stored_gates
        if row["gate"] == "v17k_overall"
    )
    if overall not in {
        "v17k_instrumentation_failed",
        "v17k_matched_work_or_proposal_integrity_not_qualified",
        "v17k_finite_movement_not_qualified",
        "v17k_resource_not_qualified",
        "v17k_compound_matched_work_start_distance_reduced",
        "v17k_compound_no_uniform_matched_work_gain",
    }:
        raise ValueError("v17k overall status invalid")
    print(f"[v17k] output verification pass overall={overall}")


def self_test() -> None:
    v17h.verify_outputs()
    v17j.verify_outputs()
    dag, metadata = load_runs()[0]
    space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
    kernel = v17a.build_kernel(space)
    for kernel_arm in KERNEL_ARMS:
        result = run_chain(
            dag,
            kernel,
            space.source_edges,
            kernel_arm,
            START_FAMILIES[0],
            "self_test_seed",
            work_target=24,
            max_attempts=4096,
        )
        if int(result.stats["accepted_gross_edge_work"]) != 24:
            raise AssertionError("v17k exact-work self-test failed")
        if not int(result.stats["proposal_integrity_pass"]):
            raise AssertionError("v17k proposal-integrity self-test failed")
        if not v16x.assignment_integrity(space, result.final):
            raise AssertionError("v17k endpoint self-test failed")
    if implementation_call_counts() != {
        "spectrum_calls": 0,
        "effect_metric_calls": 0,
    }:
        raise AssertionError("v17k effect exclusion self-test failed")
    print("[v17k] self-test pass")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Source-space worker processes for the formal run; seeds are unchanged.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    selected = sum((
        args.pilot,
        args.prepare,
        args.verify_only,
        args.self_test,
    ))
    if selected > 1:
        raise SystemExit(
            "choose only one of --pilot, --prepare, --verify-only, --self-test"
        )
    if args.workers < 1 or args.workers > 6:
        raise SystemExit("--workers must be between 1 and 6")
    if args.pilot:
        pilot()
    elif args.prepare:
        prepare()
    elif args.verify_only:
        verify_outputs()
    elif args.self_test:
        self_test()
    else:
        run(workers=args.workers)
        verify_outputs()


if __name__ == "__main__":
    main()
