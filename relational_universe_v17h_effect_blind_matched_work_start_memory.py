#!/usr/bin/env python3
"""v17h effect-blind matched accepted-work start-memory comparison.

The qualified v17c length-2-to-4 kernel and qualified v17g reverse-closed
expanded kernel are compared on the same six spaces and both frozen starts.
Each chain stops at exactly the same accepted removed-edge work. Source spectra
and observed-effect metrics remain prohibited.
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
from typing import Any, Dict, List, Mapping, MutableMapping, Sequence, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16x_explicit_global_measure_gate as v16x
import relational_universe_v16z_alternating_cycle_bridge_gate as v16z
import relational_universe_v17a_state_independent_cycle_proposal_qualification as v17a
import relational_universe_v17c_exact_counter_runtime_qualification as v17c
import relational_universe_v17f_effect_blind_length5_move_qualification as v17f
import relational_universe_v17g_effect_blind_reverse_closure_qualification as v17g


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

KERNEL_ARMS = ("old_length_2_4", "expanded_reverse_closed_length_2_5")
START_FAMILIES = v17f.START_FAMILIES
CHAIN_SEED_FAMILIES = ("matched_work_seed_g", "matched_work_seed_h")
ACCEPTED_EDGE_WORK_TARGET = 192
MAX_ATTEMPTS = 4096
MAX_CHAIN_SECONDS = 120.0
MIN_ACCEPTED_CYCLES = 32
MIN_UNIQUE_STATES = 33
MIN_FINAL_START_CHANGE = 0.04
MIN_EXPANDED_LENGTH5_CYCLES = 2
MAX_MATERIAL_CROSS_START_RATIO = 0.90
EXPECTED_CHAINS = 6 * 2 * 2 * 2

SOURCE_CHAIN = DOC / "v17h_source_chain.csv"
PRE_REGISTRATION = DOC / "v17h_pre_registration.csv"
PROPOSAL_TRACE = DOC / "v17h_proposal_trace.csv"
ENDPOINT_AUDIT = DOC / "v17h_endpoint_audit.csv"
PAIRWISE_DISTANCE = DOC / "v17h_pairwise_distance.csv"
KERNEL_DISTANCE_SUMMARY = DOC / "v17h_kernel_distance_summary.csv"
MATCHED_WORK_COMPARISON = DOC / "v17h_matched_work_comparison.csv"
TRANSITION_SUMMARY = DOC / "v17h_chain_transition_summary.csv"
SOURCE_SUMMARY = DOC / "v17h_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v17h_gate_evaluation.csv"
GOAL_EVALUATION = DOC / "v17h_goal_evaluation.csv"
CLAIM_LEDGER = DOC / "v17h_claim_ledger.csv"
REPORT = DOC / "v17h_effect_blind_matched_work_start_memory.md"
INTERPRETATION = DOC / "v17h_interpretation_audit.md"
NEXT_DIRECTION = DOC / "v17h_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_17h_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_17h.md"

Edge = v16x.Edge
CycleKernel = v17a.CycleKernel
ExpandedAuxiliary = v17f.ExpandedAuxiliary


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
    for source, metadata in v17g.load_runs():
        result.append((v16i.RunDAG(
            stage="v17h",
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
        raise ValueError("v17h requires six frozen v17g spaces")
    return result


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v17c", "qualified_old_kernel", v17c.SCRIPT),
        ("v17c", "qualified_old_gate", v17c.GATE_EVALUATION),
        ("v17g", "qualified_expanded_kernel", v17g.SCRIPT),
        ("v17g", "qualified_expanded_preregistration", v17g.PRE_REGISTRATION),
        ("v17g", "qualified_expanded_gate", v17g.GATE_EVALUATION),
        ("v17g", "matched_work_direction", v17g.NEXT_DIRECTION),
        ("v16z", "frozen_start_pair", v16z.REVERSIBILITY_AUDIT),
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
        "gate": "v17h_effect_blind_matched_accepted_work_start_memory",
        "purpose_ref": PURPOSE_REF,
        "scope": "relative_finite_start_memory_at_equal_accepted_removed_edge_work",
        "source_history_count": 6,
        "kernel_arms": list(KERNEL_ARMS),
        "start_families": list(START_FAMILIES),
        "chain_seed_families": list(CHAIN_SEED_FAMILIES),
        "seed_independence": "stable_seed_v17h_includes_kernel_arm_and_new_labels",
        "accepted_edge_work_target": ACCEPTED_EDGE_WORK_TARGET,
        "work_definition": "sum_removed_edges_over_accepted_cycles",
        "maximum_attempts": MAX_ATTEMPTS,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "terminal_rule": (
            "after exact Metropolis acceptance, self-loop if the cycle would overshoot "
            "the work target or leave exactly one unreachable work unit"
        ),
        "terminal_rule_scope_limit": (
            "symmetric finite stopping rule; not stationary sampling and may induce "
            "a small terminal conditioning bias"
        ),
        "minimum_accepted_cycles": MIN_ACCEPTED_CYCLES,
        "minimum_unique_states": MIN_UNIQUE_STATES,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "minimum_expanded_length5_cycles": MIN_EXPANDED_LENGTH5_CYCLES,
        "primary_metric": (
            "expanded_median_absolute_cross_start_distance_divided_by_old_median"
        ),
        "primary_threshold": MAX_MATERIAL_CROSS_START_RATIO,
        "primary_requirement": "six_of_six_sources_each_at_or_below_threshold",
        "design_calibration_disclosure": (
            "work target 192 selected from already published throughput floors: "
            "v17c minimum accepted edge work 196 and v17g minimum 235"
        ),
        "required_chain_count": EXPECTED_CHAINS,
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "not_claimed": [
            "global_irreducibility", "mixing_time", "convergence",
            "component_connectivity", "global_uniformity", "source_effect",
            "energy", "temperature", "dimension", "Lorentz_symmetry",
            "spacetime", "particles", "Bell_correlation", "entanglement",
            "universe_model",
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
        "kernel_arms": ";".join(KERNEL_ARMS),
        "start_families": ";".join(START_FAMILIES),
        "chain_seed_families": ";".join(CHAIN_SEED_FAMILIES),
        "accepted_edge_work_target": ACCEPTED_EDGE_WORK_TARGET,
        "maximum_attempts": MAX_ATTEMPTS,
        "maximum_chain_seconds": MAX_CHAIN_SECONDS,
        "minimum_accepted_cycles": MIN_ACCEPTED_CYCLES,
        "minimum_unique_states": MIN_UNIQUE_STATES,
        "minimum_final_start_change": MIN_FINAL_START_CHANGE,
        "minimum_expanded_length5_cycles": MIN_EXPANDED_LENGTH5_CYCLES,
        "maximum_material_cross_start_ratio": MAX_MATERIAL_CROSS_START_RATIO,
        "required_chain_count": EXPECTED_CHAINS,
        "required_primary_source_passes": 6,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v17c.verify_outputs()
    v17g.verify_outputs()
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v17h] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    expected = {key: str(value) for key, value in preregistration_row().items()}
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v17h preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v17h source chain changed")


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


def chain_seed(
    dag: v16i.RunDAG,
    kernel_arm: str,
    start_family: str,
    seed_family: str,
) -> int:
    return v16i.stable_seed(
        "v17h", "matched_work", kernel_arm, start_family, seed_family, *dag.key
    )


def old_auxiliary(
    kernel: CycleKernel,
    selected: frozenset[Edge],
    rng: random.Random,
) -> ExpandedAuxiliary | None:
    auxiliary = v17c.propose_cycle(kernel, selected, rng)
    if auxiliary is None:
        return None
    return ExpandedAuxiliary(
        "length_2_4", auxiliary.probability, auxiliary.proposal
    )


def reverse_old(
    kernel: CycleKernel,
    proposed: frozenset[Edge],
    auxiliary: ExpandedAuxiliary,
) -> ExpandedAuxiliary | None:
    reverse = v17c.path_probability(
        kernel, proposed, v17a.reverse_remove_sequence(auxiliary.proposal)
    )
    if reverse is None:
        return None
    return ExpandedAuxiliary(
        "length_2_4", reverse.probability, reverse.proposal
    )


def boundary_allows(work_before: int, cycle_length: int, target: int) -> bool:
    remaining = target - work_before
    return cycle_length <= remaining and remaining - cycle_length != 1


def run_chain(
    dag: v16i.RunDAG,
    kernel: CycleKernel,
    start: frozenset[Edge],
    kernel_arm: str,
    start_family: str,
    seed_family: str,
    *,
    work_target: int = ACCEPTED_EDGE_WORK_TARGET,
    max_attempts: int = MAX_ATTEMPTS,
) -> ChainResult:
    seed = chain_seed(dag, kernel_arm, start_family, seed_family)
    rng = random.Random(seed)
    selected = start
    trace: List[Dict[str, Any]] = []
    counts = Counter()
    accepted_lengths = Counter()
    accepted_work = 0
    visited = {v16x.edge_digest(selected)}
    started = time.monotonic()

    for attempt in range(1, max_attempts + 1):
        if accepted_work == work_target:
            break
        event = "lazy_stay"
        auxiliary: ExpandedAuxiliary | None = None
        reverse: ExpandedAuxiliary | None = None
        acceptance: Fraction | None = None
        accepted = False
        reverse_filtered = False
        work_before = accepted_work
        state_before = v16x.edge_digest(selected)

        if rng.getrandbits(1):
            counts["nonlazy_attempts"] += 1
            if kernel_arm == KERNEL_ARMS[0]:
                auxiliary = old_auxiliary(kernel, selected, rng)
            elif kernel_arm == KERNEL_ARMS[1]:
                auxiliary = v17f.propose_expanded(kernel, selected, rng)
            else:
                raise ValueError(f"unknown kernel arm {kernel_arm}")

            if auxiliary is None:
                event = "proposal_dead_end"
                counts["proposal_dead_end"] += 1
            else:
                counts["raw_proposals"] += 1
                proposed = v17a.apply_proposal(
                    kernel.space, selected, auxiliary.proposal
                )
                reverse = (
                    reverse_old(kernel, proposed, auxiliary)
                    if kernel_arm == KERNEL_ARMS[0]
                    else v17f.reverse_expanded(kernel, proposed, auxiliary)
                )
                if reverse is None:
                    if kernel_arm == KERNEL_ARMS[1]:
                        event = "reverse_filtered_dead_end"
                        reverse_filtered = True
                        counts["reverse_filtered_dead_end"] += 1
                        counts["proposal_dead_end"] += 1
                    else:
                        event = "reverse_unsupported"
                        counts["reverse_unsupported"] += 1
                else:
                    recovered = v17a.apply_proposal(
                        kernel.space, proposed, reverse.proposal
                    )
                    if recovered != selected:
                        raise ValueError("v17h reverse auxiliary did not recover state")
                    counts["valid_proposals"] += 1
                    counts["retained_reverse_supported"] += 1
                    counts[f"valid_{auxiliary.move_class}"] += 1
                    acceptance = min(
                        Fraction(1), reverse.probability / auxiliary.probability
                    )
                    if v17a.exact_accept(rng, acceptance):
                        cycle_length = len(auxiliary.proposal.remove)
                        if not boundary_allows(
                            accepted_work, cycle_length, work_target
                        ):
                            event = "work_boundary_reject"
                            counts["work_boundary_rejects"] += 1
                        else:
                            selected = proposed
                            accepted = True
                            event = "accepted_cycle"
                            accepted_work += cycle_length
                            accepted_lengths[cycle_length] += 1
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
            "kernel_arm": kernel_arm,
            "start_family": start_family,
            "chain_seed_family": seed_family,
            "chain_seed": seed,
            "attempt": attempt,
            "event": event,
            "move_class": auxiliary.move_class if auxiliary else "none",
            "cycle_length": len(proposal.remove) if proposal else 0,
            "proposal_sha256": v17a.proposal_digest(proposal) if proposal else "",
            "raw_proposal_generated": int(auxiliary is not None),
            "retained_valid_proposal": int(auxiliary is not None and reverse is not None),
            "reverse_filtered_dead_end": int(reverse_filtered),
            "q_forward_numerator": auxiliary.probability.numerator if auxiliary else 0,
            "q_forward_denominator": auxiliary.probability.denominator if auxiliary else 0,
            "q_reverse_numerator": reverse.probability.numerator if reverse else 0,
            "q_reverse_denominator": reverse.probability.denominator if reverse else 0,
            "acceptance_numerator": acceptance.numerator if acceptance else 0,
            "acceptance_denominator": acceptance.denominator if acceptance else 0,
            "accepted": int(accepted),
            "accepted_edge_work_before": work_before,
            "accepted_edge_work_after": accepted_work,
            "state_before_sha256": state_before,
            "state_after_sha256": v16x.edge_digest(selected),
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })

    elapsed = time.monotonic() - started
    attempts = len(trace)
    final_change = 1.0 - len(selected & start) / kernel.space.edge_count
    work_pass = accepted_work == work_target
    reverse_pass = (
        counts["reverse_unsupported"] == 0
        and counts["valid_proposals"] == counts["retained_reverse_supported"]
    )
    movement_pass = all((
        work_pass,
        counts["accepted_cycles"] >= MIN_ACCEPTED_CYCLES,
        len(visited) >= MIN_UNIQUE_STATES,
        final_change >= MIN_FINAL_START_CHANGE,
        (
            counts["accepted_length_5_batch_guided"]
            >= MIN_EXPANDED_LENGTH5_CYCLES
            if kernel_arm == KERNEL_ARMS[1]
            else counts["accepted_length_5_batch_guided"] == 0
        ),
        reverse_pass,
        v16x.assignment_integrity(kernel.space, selected),
    ))
    stats: MutableMapping[str, Any] = {
        **dag.prefix,
        "kernel_arm": kernel_arm,
        "start_family": start_family,
        "chain_seed_family": seed_family,
        "chain_seed": seed,
        "start_endpoint_sha256": v16x.edge_digest(start),
        "final_endpoint_sha256": v16x.edge_digest(selected),
        "attempts": attempts,
        "maximum_attempts": max_attempts,
        "lazy_stays": counts["lazy_stays"],
        "nonlazy_attempts": counts["nonlazy_attempts"],
        "proposal_dead_end": counts["proposal_dead_end"],
        "raw_proposals": counts["raw_proposals"],
        "reverse_filtered_dead_end": counts["reverse_filtered_dead_end"],
        "reverse_unsupported": counts["reverse_unsupported"],
        "valid_proposals": counts["valid_proposals"],
        "retained_reverse_supported": counts["retained_reverse_supported"],
        "accepted_cycles": counts["accepted_cycles"],
        "accepted_old_cycles": counts["accepted_length_2_4"],
        "accepted_length5_cycles": counts["accepted_length_5_batch_guided"],
        "accepted_edge_work": accepted_work,
        "accepted_edge_work_target": work_target,
        "work_boundary_rejects": counts["work_boundary_rejects"],
        "metropolis_rejects": counts["metropolis_rejects"],
        "accepted_length_counts_json": json.dumps(
            dict(sorted(accepted_lengths.items())), separators=(",", ":")
        ),
        "unique_state_count": len(visited),
        "final_start_changed_edge_fraction": final_change,
        "elapsed_seconds": elapsed,
        "final_assignment_integrity_pass": int(
            v16x.assignment_integrity(kernel.space, selected)
        ),
        "matched_work_pass": int(work_pass),
        "retained_reverse_support_pass": int(reverse_pass),
        "movement_pass": int(movement_pass),
        "resource_pass": int(
            attempts <= max_attempts and elapsed <= MAX_CHAIN_SECONDS
        ),
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }
    return ChainResult(selected, stats, trace)


def endpoint_row(result: ChainResult) -> MutableMapping[str, Any]:
    stats = result.stats
    return {
        "stage": "v17h",
        "target_nodes": stats["target_nodes"],
        "growth_seed": stats["growth_seed"],
        "run_offset": stats["run_offset"],
        "arm": stats["arm"],
        "run_seed": stats["run_seed"],
        "kernel_arm": stats["kernel_arm"],
        "start_family": stats["start_family"],
        "chain_seed_family": stats["chain_seed_family"],
        "accepted_edge_work": stats["accepted_edge_work"],
        "selected_edge_count": len(result.final),
        "final_start_changed_edge_fraction": stats["final_start_changed_edge_fraction"],
        "endpoint_edge_sha256": stats["final_endpoint_sha256"],
        "endpoint_integrity_pass": stats["final_assignment_integrity_pass"],
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
        for row in rows if row["relation"] == "within_start"
    ]
    cross = [
        float(row["changed_edge_fraction"])
        for row in rows if row["relation"] == "cross_start"
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
    old = float(by_arm[KERNEL_ARMS[0]]["median_cross_start_distance"])
    expanded = float(by_arm[KERNEL_ARMS[1]]["median_cross_start_distance"])
    ratio = expanded / old if old else (0.0 if expanded == 0 else math.inf)
    old_within = float(by_arm[KERNEL_ARMS[0]]["median_within_start_distance"])
    expanded_within = float(
        by_arm[KERNEL_ARMS[1]]["median_within_start_distance"]
    )
    return {
        **dag.prefix,
        "accepted_edge_work_per_chain": ACCEPTED_EDGE_WORK_TARGET,
        "old_median_cross_start_distance": old,
        "expanded_median_cross_start_distance": expanded,
        "expanded_over_old_cross_start_distance_ratio": ratio,
        "directional_cross_start_reduction": int(expanded < old),
        "material_cross_start_reduction_pass": int(
            ratio <= MAX_MATERIAL_CROSS_START_RATIO
        ),
        "old_median_within_start_distance": old_within,
        "expanded_median_within_start_distance": expanded_within,
        "expanded_over_old_within_start_distance_ratio": (
            expanded_within / old_within
            if old_within else (0.0 if expanded_within == 0 else math.inf)
        ),
        "maximum_material_cross_start_ratio": MAX_MATERIAL_CROSS_START_RATIO,
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }


def gate_rows(
    transitions: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
    frozen_start_passes: int,
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
    work_count = sum(
        int(row["matched_work_pass"])
        and int(row["final_assignment_integrity_pass"])
        for row in transitions
    )
    reverse_count = sum(
        int(row["retained_reverse_support_pass"]) for row in transitions
    )
    movement_count = sum(int(row["movement_pass"]) for row in transitions)
    resource_count = sum(int(row["resource_pass"]) for row in transitions)
    expanded_exercise = sum(
        int(row["accepted_length5_cycles"]) >= MIN_EXPANDED_LENGTH5_CYCLES
        for row in transitions if row["kernel_arm"] == KERNEL_ARMS[1]
    )
    primary_count = sum(
        int(row["material_cross_start_reduction_pass"])
        for row in comparisons
    )

    if not exclusion_pass or frozen_start_passes != 12:
        overall = "v17h_instrumentation_failed"
    elif work_count != EXPECTED_CHAINS or reverse_count != EXPECTED_CHAINS:
        overall = "v17h_matched_work_or_support_not_qualified"
    elif movement_count != EXPECTED_CHAINS or expanded_exercise != 24:
        overall = "v17h_finite_movement_not_qualified"
    elif resource_count != EXPECTED_CHAINS:
        overall = "v17h_resource_not_qualified"
    elif primary_count == 6:
        overall = "v17h_expanded_kernel_matched_work_start_distance_reduced"
    else:
        overall = "v17h_expanded_kernel_no_uniform_matched_work_gain"

    ratios = [
        float(row["expanded_over_old_cross_start_distance_ratio"])
        for row in comparisons
    ]
    gates = [
        {"gate": "effect_blind_integrity", "status": "pass" if exclusion_pass else "fail", "observed": f"spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}", "required": "0;0", "decision": "continue" if exclusion_pass else "invalidate"},
        {"gate": "frozen_start_integrity", "status": "pass" if frozen_start_passes == 12 else "fail", "observed": f"{frozen_start_passes}/12", "required": "12/12", "decision": "continue" if frozen_start_passes == 12 else "invalidate"},
        {"gate": "exact_matched_work_and_endpoint_integrity", "status": "pass" if work_count == EXPECTED_CHAINS else "fail", "observed": f"{work_count}/{EXPECTED_CHAINS};work={ACCEPTED_EDGE_WORK_TARGET}", "required": f"{EXPECTED_CHAINS}/{EXPECTED_CHAINS};each={ACCEPTED_EDGE_WORK_TARGET}", "decision": "continue" if work_count == EXPECTED_CHAINS else "repair_stopping_rule"},
        {"gate": "retained_reverse_support", "status": "pass" if reverse_count == EXPECTED_CHAINS else "fail", "observed": f"{reverse_count}/{EXPECTED_CHAINS}", "required": f"{EXPECTED_CHAINS}/{EXPECTED_CHAINS}", "decision": "continue" if reverse_count == EXPECTED_CHAINS else "invalidate"},
        {"gate": "finite_movement_and_length5_exercise", "status": "pass" if movement_count == EXPECTED_CHAINS and expanded_exercise == 24 else "fail", "observed": f"movement={movement_count}/{EXPECTED_CHAINS};expanded_length5={expanded_exercise}/24", "required": f"{EXPECTED_CHAINS}/{EXPECTED_CHAINS};24/24", "decision": "continue" if movement_count == EXPECTED_CHAINS and expanded_exercise == 24 else "do_not_compare_start_memory"},
        {"gate": "resource_bound", "status": "pass" if resource_count == EXPECTED_CHAINS else "fail", "observed": f"{resource_count}/{EXPECTED_CHAINS};max={max(float(row['elapsed_seconds']) for row in transitions):.6f}s", "required": f"{EXPECTED_CHAINS}/{EXPECTED_CHAINS};each<={MAX_CHAIN_SECONDS:.0f}s", "decision": "continue" if resource_count == EXPECTED_CHAINS else "retire_or_optimize"},
        {"gate": "primary_matched_work_cross_start_reduction", "status": "pass" if primary_count == 6 else "fail", "observed": f"{primary_count}/6;ratio={min(ratios):.6f}-{max(ratios):.6f}", "required": f"6/6;each<={MAX_MATERIAL_CROSS_START_RATIO:.2f}", "decision": "replicate_at_fresh_work_levels" if primary_count == 6 else "retire_current_length5_as_uniform_start_memory_remedy"},
        {"gate": "v17h_overall", "status": overall, "observed": f"exclusion={int(exclusion_pass)};starts={frozen_start_passes}/12;work={work_count}/{EXPECTED_CHAINS};support={reverse_count}/{EXPECTED_CHAINS};movement={movement_count}/{EXPECTED_CHAINS};length5={expanded_exercise}/24;resource={resource_count}/{EXPECTED_CHAINS};primary={primary_count}/6", "required": f"1;12/12;{EXPECTED_CHAINS}/{EXPECTED_CHAINS};{EXPECTED_CHAINS}/{EXPECTED_CHAINS};{EXPECTED_CHAINS}/{EXPECTED_CHAINS};24/24;{EXPECTED_CHAINS}/{EXPECTED_CHAINS};6/6", "decision": overall},
    ]
    return overall, gates


def markdown_table(
    rows: Sequence[Mapping[str, Any]], fields: Sequence[str]
) -> List[str]:
    return v17g.markdown_table(rows, fields)


def write_documents(
    overall: str,
    gates: Sequence[Mapping[str, Any]],
    transitions: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
) -> None:
    ratios = [
        float(row["expanded_over_old_cross_start_distance_ratio"])
        for row in comparisons
    ]
    directional = sum(
        int(row["directional_cross_start_reduction"]) for row in comparisons
    )
    primary = sum(
        int(row["material_cross_start_reduction_pass"])
        for row in comparisons
    )
    report = [
        "# v17h effect-blind matched accepted-work start-memory gate",
        "",
        f"Status: `{overall}`.",
        "",
        "## Purpose and frozen design",
        "",
        "Purpose `purpose://validation`: test whether the reverse-closed expanded length-2-to-5 kernel reduces finite start memory more efficiently than the qualified old length-2-to-4 kernel at exactly equal realized accepted work. Six frozen spaces, both starts and two new seed families are used. Source spectra and observed effects are prohibited.",
        "",
        f"Every chain targets exactly `{ACCEPTED_EDGE_WORK_TARGET}` accepted removed-edge units. The terminal rule rejects a Metropolis-accepted cycle only if it would overshoot the target or leave one unreachable unit. This is a symmetric finite stopping rule, not stationary sampling, and may add a small terminal conditioning bias.",
        "",
        "## Frozen gates",
        "",
        *markdown_table(gates, ("gate", "status", "observed", "required", "decision")),
        "",
        "## Primary matched-work response",
        "",
        *markdown_table(comparisons, (
            "growth_seed", "run_offset", "old_median_cross_start_distance",
            "expanded_median_cross_start_distance",
            "expanded_over_old_cross_start_distance_ratio",
            "directional_cross_start_reduction",
            "material_cross_start_reduction_pass",
        )),
        "",
        f"Directional reduction occurred in `{directional}/6`; material reduction passed `{primary}/6`. Expanded/old cross-start ratios ranged `{min(ratios):.6f}-{max(ratios):.6f}` with median `{statistics.median(ratios):.6f}`.",
        "",
        "## Finite execution",
        "",
        f"All results are based on `{len(transitions)}` finite chains. Maximum runtime was `{max(float(row['elapsed_seconds']) for row in transitions):.6f}` seconds, maximum attempts `{max(int(row['attempts']) for row in transitions)}`, and minimum accepted length-5 count in the expanded arm `{min(int(row['accepted_length5_cycles']) for row in transitions if row['kernel_arm'] == KERNEL_ARMS[1])}`.",
        "",
        "## Claim boundary",
        "",
        "This is a relative finite efficiency/start-memory comparison. Even a pass would not establish global connectivity, convergence, mixing, a source effect, geometry or physics. A failure rejects only this fixed length-5 expansion as a uniform start-memory remedy under the frozen work target.",
        "",
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    INTERPRETATION.write_text(
        "# v17h interpretation audit\n\n"
        f"Frozen status is `{overall}`. Equal accepted edge-work removes the known unequal-realized-work confound, but the terminal exact-work rule conditions the final few proposals and the test remains finite. Relative cross-start distance is not connectivity or mixing. No source spectrum, observed effect, Bell observable, Lorentz diagnostic or physical invariant was computed.\n",
        encoding="utf-8",
    )
    if overall == "v17h_expanded_kernel_matched_work_start_distance_reduced":
        next_text = (
            "Preregister a fresh work-level response replication at 192 and 384 accepted edge-work with new seeds. Require the relative reduction to persist across work levels before reopening any source spectrum."
        )
        recommendation = "replicate the matched-work reduction at fresh work levels"
    elif overall == "v17h_expanded_kernel_no_uniform_matched_work_gain":
        next_text = (
            "Retire the current fixed length-5 expansion as a uniform start-memory remedy. Keep source effects closed. The next effect-blind design should target direct cross-start accessibility with a larger algebraically declared move, not add more work to the same 50/50 kernel."
        )
        recommendation = "retire the current length-5 expansion as a uniform start-memory remedy"
    else:
        next_text = (
            "Stop at the first failed instrumentation, support, movement or resource layer. Repair that layer without inspecting source spectra or observed effects, then preregister a replacement gate."
        )
        recommendation = "repair the first failed frozen layer"
    NEXT_DIRECTION.write_text(
        f"# v17h next direction\n\nFormal status: `{overall}`.\n\n{next_text}\n",
        encoding="utf-8",
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.17h\n\n"
        f"- status: `{overall}`\n"
        f"- next: {recommendation}\n"
        "- source spectrum and observed effects remain closed\n"
        "- claim ceiling: relative finite matched-work response, not connectivity or physics\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf v0.17h for ikke-spesialister\n\n"
        "V17h gir den gamle og den utvidede flytteregelen noyaktig samme mengde faktisk utfort grafarbeid. Dermed kan vi sporre om lengde-5-flytt reduserer avhengigheten av startpunktet, uten aa forveksle flere endringer med en bedre regel.\n\n"
        f"Statusen er `{overall}`. Resultatet gjelder 48 endelige kjoeringer og sier ikke at hele tilstandsrommet er sammenhengende, mikset eller fysisk.\n",
        encoding="utf-8",
    )


def run() -> None:
    verify_frozen_sources()
    frozen_starts = v16z.frozen_start_digests()
    traces: List[Dict[str, Any]] = []
    transitions: List[Dict[str, Any]] = []
    endpoint_rows: List[Dict[str, Any]] = []
    pairwise: List[Dict[str, Any]] = []
    kernel_summaries: List[Dict[str, Any]] = []
    comparisons: List[Dict[str, Any]] = []
    source_summaries: List[Dict[str, Any]] = []
    frozen_start_passes = 0

    for run_index, (dag, metadata) in enumerate(load_runs(), start=1):
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        kernel = v17a.build_kernel(space)
        starts = {
            "source_assignment": space.source_edges,
            "v16x_random_cost_a0": v16z.random_cost_start(dag, space),
        }
        source_frozen_start_passes = 0
        for start_family, start in starts.items():
            start_pass = int(
                v16x.edge_digest(start)
                == frozen_starts[(dag.growth_seed, dag.run_offset, start_family)]
            )
            frozen_start_passes += start_pass
            source_frozen_start_passes += start_pass

        source_transitions: List[Mapping[str, Any]] = []
        source_kernel_summaries: List[Mapping[str, Any]] = []
        for kernel_arm in KERNEL_ARMS:
            endpoints: List[Endpoint] = []
            for start_family, start in starts.items():
                for seed_family in CHAIN_SEED_FAMILIES:
                    result = run_chain(
                        dag, kernel, start, kernel_arm, start_family, seed_family
                    )
                    traces.extend(result.trace)
                    transitions.append(dict(result.stats))
                    source_transitions.append(result.stats)
                    row = endpoint_row(result)
                    endpoint_rows.append(dict(row))
                    endpoints.append(Endpoint(result.final, row))
            arm_pairwise = pairwise_rows(dag, kernel_arm, endpoints)
            pairwise.extend(arm_pairwise)
            summary = kernel_distance_row(dag, kernel_arm, arm_pairwise)
            kernel_summaries.append(summary)
            source_kernel_summaries.append(summary)

        comparison = comparison_row(dag, source_kernel_summaries)
        comparisons.append(comparison)
        source_summaries.append({
            **dag.prefix,
            "chain_count": len(source_transitions),
            "frozen_start_passes": source_frozen_start_passes,
            "matched_work_passes": sum(
                int(row["matched_work_pass"]) for row in source_transitions
            ),
            "reverse_support_passes": sum(
                int(row["retained_reverse_support_pass"])
                for row in source_transitions
            ),
            "movement_passes": sum(
                int(row["movement_pass"]) for row in source_transitions
            ),
            "resource_passes": sum(
                int(row["resource_pass"]) for row in source_transitions
            ),
            "minimum_expanded_length5_cycles": min(
                int(row["accepted_length5_cycles"])
                for row in source_transitions
                if row["kernel_arm"] == KERNEL_ARMS[1]
            ),
            "maximum_attempts_used": max(
                int(row["attempts"]) for row in source_transitions
            ),
            "maximum_chain_seconds": max(
                float(row["elapsed_seconds"]) for row in source_transitions
            ),
            "expanded_over_old_cross_start_distance_ratio": comparison[
                "expanded_over_old_cross_start_distance_ratio"
            ],
            "material_cross_start_reduction_pass": comparison[
                "material_cross_start_reduction_pass"
            ],
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })
        print(f"[v17h] source {run_index}/6 complete")

    overall, gates = gate_rows(transitions, comparisons, frozen_start_passes)
    v16i.write_csv(PROPOSAL_TRACE, traces)
    v16i.write_csv(ENDPOINT_AUDIT, endpoint_rows)
    v16i.write_csv(PAIRWISE_DISTANCE, pairwise)
    v16i.write_csv(KERNEL_DISTANCE_SUMMARY, kernel_summaries)
    v16i.write_csv(MATCHED_WORK_COMPARISON, comparisons)
    v16i.write_csv(TRANSITION_SUMMARY, transitions)
    v16i.write_csv(SOURCE_SUMMARY, source_summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(GOAL_EVALUATION, [{
        "goal_id": "G1",
        "purpose_ref": PURPOSE_REF,
        "metric": "material cross-start distance reduction at exact matched accepted work",
        "baseline": "old qualified length-2-to-4 kernel",
        "target": "expanded/old median cross-start distance <=0.90 in 6/6 sources",
        "timeframe": "one frozen v17h round",
        "status": "satisfied" if overall == "v17h_expanded_kernel_matched_work_start_distance_reduced" else "missed",
        "evidence": "v17h_matched_work_comparison.csv;v17h_gate_evaluation.csv",
    }])
    v16i.write_csv(CLAIM_LEDGER, [
        {"claim_id": "C1", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "factual", "strength": "assertive", "claim": "v17h computes no source spectrum or observed-effect metric.", "status": "supported", "evidence": "static call audit plus runtime exclusion fields", "scope_limit": "v17h script and outputs"},
        {"claim_id": "C2", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "project_capability", "strength": "assertive", "claim": "Both kernel arms complete exactly equal accepted removed-edge work with valid endpoints.", "status": "supported" if all(int(row["matched_work_pass"]) and int(row["final_assignment_integrity_pass"]) for row in transitions) else "not_supported", "evidence": "v17h_chain_transition_summary.csv", "scope_limit": "48 finite chains; terminal conditioning rule applies"},
        {"claim_id": "C3", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "empirical", "strength": "moderated", "claim": "The expanded kernel reduces median absolute cross-start distance by at least 10 percent in every source at matched work.", "status": "supported" if overall == "v17h_expanded_kernel_matched_work_start_distance_reduced" else "not_supported", "evidence": "v17h_matched_work_comparison.csv", "scope_limit": "six reused spaces, two starts, two new seed families, work 192"},
        {"claim_id": "C4", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "causal", "strength": "speculative", "claim": "The expanded move graph is globally connected or mixed.", "status": "not_tested", "evidence": "none", "scope_limit": "finite relative endpoint distance cannot establish connectivity or mixing"},
        {"claim_id": "C5", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "project_capability", "strength": "speculative", "claim": "v17h establishes source effects, geometry, Lorentz symmetry, spacetime or a universe model.", "status": "contradicted", "evidence": "effect observables prohibited and no physical diagnostic computed", "scope_limit": "requires separate later gates"},
    ])
    write_documents(overall, gates, transitions, comparisons)
    print(f"[v17h] status={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    paths = (
        PROPOSAL_TRACE, ENDPOINT_AUDIT, PAIRWISE_DISTANCE,
        KERNEL_DISTANCE_SUMMARY, MATCHED_WORK_COMPARISON, TRANSITION_SUMMARY,
        SOURCE_SUMMARY, GATE_EVALUATION, GOAL_EVALUATION, CLAIM_LEDGER,
        REPORT, INTERPRETATION, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST,
    )
    if any(not path.exists() for path in paths):
        raise ValueError("v17h output missing")
    traces = v16i.read_csv(PROPOSAL_TRACE)
    endpoints = v16i.read_csv(ENDPOINT_AUDIT)
    pairwise = v16i.read_csv(PAIRWISE_DISTANCE)
    kernel_summaries = v16i.read_csv(KERNEL_DISTANCE_SUMMARY)
    comparisons = v16i.read_csv(MATCHED_WORK_COMPARISON)
    transitions = v16i.read_csv(TRANSITION_SUMMARY)
    summaries = v16i.read_csv(SOURCE_SUMMARY)
    if len(transitions) != EXPECTED_CHAINS or len(endpoints) != EXPECTED_CHAINS:
        raise ValueError("v17h chain/endpoint row count mismatch")
    if (len(pairwise), len(kernel_summaries), len(comparisons), len(summaries)) != (
        72, 12, 6, 6
    ):
        raise ValueError("v17h comparison row count mismatch")
    if len(traces) != sum(int(row["attempts"]) for row in transitions):
        raise ValueError("v17h trace length mismatch")
    frozen_start_passes = sum(
        int(row["frozen_start_passes"]) for row in summaries
    )
    _, expected_gates = gate_rows(
        transitions, comparisons, frozen_start_passes
    )
    stored_gates = v16i.read_csv(GATE_EVALUATION)
    if stored_gates != [
        {key: str(value) for key, value in row.items()} for row in expected_gates
    ]:
        raise ValueError("v17h gate evaluation changed")
    if implementation_call_counts() != {
        "spectrum_calls": 0, "effect_metric_calls": 0
    }:
        raise ValueError("v17h effect exclusion failed")
    if any(
        int(row["source_spectrum_computed"])
        or int(row["observed_effect_computed"])
        for row in traces
    ):
        raise ValueError("v17h trace contains prohibited effect data")
    overall = next(
        row["status"] for row in stored_gates if row["gate"] == "v17h_overall"
    )
    print(f"[v17h] output verification pass overall={overall}")


def self_test() -> None:
    v17c.verify_outputs()
    v17g.verify_outputs()
    dag, metadata = load_runs()[0]
    space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
    kernel = v17a.build_kernel(space)
    for kernel_arm in KERNEL_ARMS:
        result = run_chain(
            dag,
            kernel,
            space.source_edges,
            kernel_arm,
            "source_assignment",
            CHAIN_SEED_FAMILIES[0],
            work_target=12,
            max_attempts=512,
        )
        if int(result.stats["accepted_edge_work"]) != 12:
            raise AssertionError("v17h exact-work self-test failed")
        if not v16x.assignment_integrity(space, result.final):
            raise AssertionError("v17h endpoint self-test failed")
    if implementation_call_counts() != {
        "spectrum_calls": 0, "effect_metric_calls": 0
    }:
        raise AssertionError("v17h effect exclusion self-test failed")
    print("[v17h] self-test pass")


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
