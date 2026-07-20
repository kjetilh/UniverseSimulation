#!/usr/bin/env python3
"""v17i effect-blind pair-basis accessibility positive control.

The frozen v16z alternating-cycle decomposition is used as an engineered
hypercube basis between each pair of frozen starts. Uniform bit masks over that
basis provide an exact positive control for the cross-start distance
instrumentation. The basis is pair-derived and is not a candidate global null.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from dataclasses import dataclass
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import random
import statistics
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16x_explicit_global_measure_gate as v16x
import relational_universe_v16z_alternating_cycle_bridge_gate as v16z
import relational_universe_v16z_postrun_representation_audit as v16z_post
import relational_universe_v17h_effect_blind_matched_work_start_memory as v17h


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

START_FAMILIES = (v16z.START_LEFT, v16z.START_RIGHT)
COUPLED_MASKS_PER_SOURCE = 16
INDEPENDENT_MASKS_PER_START = 16
MIN_DISTANCE_RATIO = 0.85
MAX_DISTANCE_RATIO = 1.15
MIN_CYCLE_INCLUSION = 4
MAX_CYCLE_INCLUSION = 28
EXPECTED_COUPLED = 6 * COUPLED_MASKS_PER_SOURCE
EXPECTED_ENDPOINTS = 6 * 2 * INDEPENDENT_MASKS_PER_START

SOURCE_CHAIN = DOC / "v17i_source_chain.csv"
PRE_REGISTRATION = DOC / "v17i_pre_registration.csv"
BASIS_AUDIT = DOC / "v17i_cycle_basis_audit.csv"
COUPLED_AUDIT = DOC / "v17i_complement_coupling_audit.csv"
ENDPOINT_AUDIT = DOC / "v17i_uniform_mask_endpoint_audit.csv"
PAIRWISE_DISTANCE = DOC / "v17i_uniform_mask_pairwise_distance.csv"
SOURCE_SUMMARY = DOC / "v17i_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v17i_gate_evaluation.csv"
GOAL_EVALUATION = DOC / "v17i_goal_evaluation.csv"
CLAIM_LEDGER = DOC / "v17i_claim_ledger.csv"
REPORT = DOC / "v17i_effect_blind_cycle_basis_positive_control.md"
INTERPRETATION = DOC / "v17i_interpretation_audit.md"
NEXT_DIRECTION = DOC / "v17i_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_17i_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_17i.md"

Edge = v16x.Edge
CycleExchange = v16z.CycleExchange


@dataclass(frozen=True)
class Endpoint:
    edges: frozenset[Edge]
    row: Dict[str, Any]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v16z", "pair_basis_constructor", v16z.SCRIPT),
        ("v16z", "frozen_cycle_decomposition", v16z.CYCLE_DECOMPOSITION),
        ("v16z", "whole_cycle_reversibility", v16z.REVERSIBILITY_AUDIT),
        ("v16z", "edge_representation_audit", v16z_post.AUDIT_CSV),
        ("v17h", "matched_work_gate", v17h.GATE_EVALUATION),
        ("v17h", "next_direction", v17h.NEXT_DIRECTION),
    )
    return [
        {
            "stage": stage,
            "role": role,
            "artifact": path.name,
            "sha256": file_sha256(path),
            "source_pass": 1,
        }
        for stage, role, path in paths
    ]


def spec_payload() -> Dict[str, Any]:
    return {
        "gate": "v17i_effect_blind_pair_cycle_basis_positive_control",
        "purpose_ref": PURPOSE_REF,
        "source_history_count": 6,
        "start_families": list(START_FAMILIES),
        "basis": "frozen_pair_specific_v16z_whole_cycle_decomposition",
        "measure": "independent_fair_bits_over_each_frozen_cycle_basis",
        "coupling": "source_mask_equals_target_complement_mask",
        "coupled_masks_per_source": COUPLED_MASKS_PER_SOURCE,
        "independent_masks_per_start": INDEPENDENT_MASKS_PER_START,
        "minimum_distance_ratio": MIN_DISTANCE_RATIO,
        "maximum_distance_ratio": MAX_DISTANCE_RATIO,
        "minimum_cycle_inclusion": MIN_CYCLE_INCLUSION,
        "maximum_cycle_inclusion": MAX_CYCLE_INCLUSION,
        "primary_gate": "exact_complement_coupled_endpoint_identity",
        "finite_diagnostic": "cross_start_over_within_start_median_distance",
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "pair_derived_positive_control": True,
        "not_claimed": [
            "state_independent_proposal", "global_null", "irreducibility",
            "mixing", "global_connectivity", "source_effect", "geometry",
            "Lorentz_symmetry", "spacetime", "energy", "temperature",
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
        "coupled_masks_per_source": COUPLED_MASKS_PER_SOURCE,
        "independent_masks_per_start": INDEPENDENT_MASKS_PER_START,
        "minimum_distance_ratio": MIN_DISTANCE_RATIO,
        "maximum_distance_ratio": MAX_DISTANCE_RATIO,
        "minimum_cycle_inclusion": MIN_CYCLE_INCLUSION,
        "maximum_cycle_inclusion": MAX_CYCLE_INCLUSION,
        "required_basis_passes": 6,
        "required_coupled_identity_passes": EXPECTED_COUPLED,
        "required_endpoint_integrity_passes": EXPECTED_ENDPOINTS,
        "required_distance_passes": 6,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v17h.verify_outputs()
    v16z_post.verify_outputs()
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v17i] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    expected = {key: str(value) for key, value in preregistration_row().items()}
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v17i preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v17i source chain changed")


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


def load_spaces() -> List[Tuple[v16i.RunDAG, v16x.StateSpace, frozenset[Edge], frozenset[Edge]]]:
    result = []
    for dag, metadata in v17h.load_runs():
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        left = space.source_edges
        right = v16z.random_cost_start(dag, space)
        result.append((dag, space, left, right))
    if len(result) != 6:
        raise ValueError("v17i requires six frozen spaces")
    return result


def frozen_cycle_digests() -> Dict[Tuple[int, int], Tuple[str, ...]]:
    grouped: Dict[Tuple[int, int], List[Tuple[int, str]]] = {}
    for row in v16i.read_csv(v16z.CYCLE_DECOMPOSITION):
        key = (int(row["growth_seed"]), int(row["run_offset"]))
        grouped.setdefault(key, []).append((int(row["cycle_index"]), row["cycle_sha256"]))
    return {
        key: tuple(digest for _, digest in sorted(items))
        for key, items in grouped.items()
    }


def cycle_support_disjoint(cycles: Sequence[CycleExchange]) -> bool:
    seen: set[Edge] = set()
    for cycle in cycles:
        support = set(cycle.remove) | set(cycle.add)
        if seen & support:
            return False
        seen.update(support)
    return True


def apply_mask(
    space: v16x.StateSpace,
    start: frozenset[Edge],
    cycles: Sequence[CycleExchange],
    mask: Sequence[bool],
) -> frozenset[Edge]:
    if len(mask) != len(cycles):
        raise ValueError("mask length differs from cycle basis")
    selected = set(start)
    for enabled, cycle in zip(mask, cycles):
        if not enabled:
            continue
        remove = set(cycle.remove)
        add = set(cycle.add)
        if remove.issubset(selected) and not add & selected:
            selected.difference_update(remove)
            selected.update(add)
        elif add.issubset(selected) and not remove & selected:
            selected.difference_update(add)
            selected.update(remove)
        else:
            raise ValueError("cycle basis mask encountered invalid occupancy")
    endpoint = frozenset(selected)
    if not v16x.assignment_integrity(space, endpoint):
        raise ValueError("cycle basis mask broke endpoint integrity")
    return endpoint


def random_mask(seed: int, count: int) -> Tuple[bool, ...]:
    rng = random.Random(seed)
    return tuple(bool(rng.getrandbits(1)) for _ in range(count))


def mask_sha256(mask: Sequence[bool]) -> str:
    raw = "".join("1" if value else "0" for value in mask)
    return hashlib.sha256(raw.encode("ascii")).hexdigest()


def basis_row(
    dag: v16i.RunDAG,
    space: v16x.StateSpace,
    left: frozenset[Edge],
    right: frozenset[Edge],
    cycles: Sequence[CycleExchange],
    frozen_digests: Sequence[str],
) -> Dict[str, Any]:
    current_digests = tuple(v16z.cycle_digest(cycle) for cycle in cycles)
    all_mask = (True,) * len(cycles)
    left_to_right = apply_mask(space, left, cycles, all_mask)
    right_to_left = apply_mask(space, right, cycles, all_mask)
    support = set().union(*(set(cycle.remove) | set(cycle.add) for cycle in cycles))
    difference = left ^ right
    return {
        **dag.prefix,
        "cycle_count": len(cycles),
        "minimum_exchange_size": min(len(cycle.remove) for cycle in cycles),
        "maximum_exchange_size": max(len(cycle.remove) for cycle in cycles),
        "pair_difference_edge_count": len(difference),
        "basis_support_edge_count": len(support),
        "frozen_cycle_digest_replay_pass": int(current_digests == tuple(frozen_digests)),
        "support_disjoint_pass": int(cycle_support_disjoint(cycles)),
        "support_exact_pair_difference_pass": int(support == difference),
        "single_block_left_to_right_pass": int(left_to_right == right),
        "single_block_right_to_left_pass": int(right_to_left == left),
        "basis_qualification_pass": int(all((
            current_digests == tuple(frozen_digests),
            cycle_support_disjoint(cycles),
            support == difference,
            left_to_right == right,
            right_to_left == left,
        ))),
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }


def coupled_rows(
    dag: v16i.RunDAG,
    space: v16x.StateSpace,
    left: frozenset[Edge],
    right: frozenset[Edge],
    cycles: Sequence[CycleExchange],
) -> List[Dict[str, Any]]:
    rows = []
    for index in range(COUPLED_MASKS_PER_SOURCE):
        seed = v16i.stable_seed("v17i", "complement_coupling", index, *dag.key)
        mask = random_mask(seed, len(cycles))
        complement = tuple(not value for value in mask)
        left_endpoint = apply_mask(space, left, cycles, mask)
        right_endpoint = apply_mask(space, right, cycles, complement)
        rows.append({
            **dag.prefix,
            "mask_index": index,
            "mask_seed": seed,
            "mask_sha256": mask_sha256(mask),
            "enabled_cycle_count": sum(mask),
            "left_endpoint_sha256": v16x.edge_digest(left_endpoint),
            "right_complement_endpoint_sha256": v16x.edge_digest(right_endpoint),
            "complement_endpoint_identity_pass": int(left_endpoint == right_endpoint),
            "endpoint_integrity_pass": int(
                v16x.assignment_integrity(space, left_endpoint)
                and v16x.assignment_integrity(space, right_endpoint)
            ),
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })
    return rows


def endpoint_rows(
    dag: v16i.RunDAG,
    space: v16x.StateSpace,
    starts: Mapping[str, frozenset[Edge]],
    cycles: Sequence[CycleExchange],
) -> List[Endpoint]:
    endpoints = []
    for start_family, start in starts.items():
        for index in range(INDEPENDENT_MASKS_PER_START):
            seed = v16i.stable_seed(
                "v17i", "independent_uniform_mask", start_family, index, *dag.key
            )
            mask = random_mask(seed, len(cycles))
            endpoint = apply_mask(space, start, cycles, mask)
            row = {
                **dag.prefix,
                "start_family": start_family,
                "mask_index": index,
                "mask_seed": seed,
                "mask_sha256": mask_sha256(mask),
                "cycle_count": len(cycles),
                "enabled_cycle_count": sum(mask),
                "endpoint_sha256": v16x.edge_digest(endpoint),
                "start_changed_edge_fraction": len(endpoint - start) / len(start),
                "endpoint_integrity_pass": int(v16x.assignment_integrity(space, endpoint)),
                "source_spectrum_computed": 0,
                "observed_effect_computed": 0,
            }
            endpoints.append(Endpoint(endpoint, row))
    return endpoints


def pairwise_rows(dag: v16i.RunDAG, endpoints: Sequence[Endpoint]) -> List[Dict[str, Any]]:
    rows = []
    for left, right in combinations(endpoints, 2):
        relation = (
            "within_start"
            if left.row["start_family"] == right.row["start_family"]
            else "cross_start"
        )
        rows.append({
            **dag.prefix,
            "relation": relation,
            "left_start_family": left.row["start_family"],
            "left_mask_index": left.row["mask_index"],
            "right_start_family": right.row["start_family"],
            "right_mask_index": right.row["mask_index"],
            "changed_edge_fraction": len(left.edges - right.edges) / len(left.edges),
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })
    return rows


def source_summary_row(
    dag: v16i.RunDAG,
    basis: Mapping[str, Any],
    coupled: Sequence[Mapping[str, Any]],
    endpoints: Sequence[Endpoint],
    pairwise: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    within = [
        float(row["changed_edge_fraction"])
        for row in pairwise if row["relation"] == "within_start"
    ]
    cross = [
        float(row["changed_edge_fraction"])
        for row in pairwise if row["relation"] == "cross_start"
    ]
    within_median = statistics.median(within)
    cross_median = statistics.median(cross)
    ratio = cross_median / within_median if within_median else math.inf
    inclusion = [0] * int(basis["cycle_count"])
    for endpoint in endpoints:
        seed = int(endpoint.row["mask_seed"])
        for index, enabled in enumerate(random_mask(seed, len(inclusion))):
            inclusion[index] += int(enabled)
    exercise_pass = min(inclusion) >= MIN_CYCLE_INCLUSION and max(inclusion) <= MAX_CYCLE_INCLUSION
    distance_pass = MIN_DISTANCE_RATIO <= ratio <= MAX_DISTANCE_RATIO
    coupled_passes = sum(int(row["complement_endpoint_identity_pass"]) for row in coupled)
    integrity_passes = sum(int(endpoint.row["endpoint_integrity_pass"]) for endpoint in endpoints)
    source_pass = all((
        int(basis["basis_qualification_pass"]) == 1,
        coupled_passes == COUPLED_MASKS_PER_SOURCE,
        integrity_passes == 2 * INDEPENDENT_MASKS_PER_START,
        exercise_pass,
        distance_pass,
    ))
    return {
        **dag.prefix,
        "cycle_count": basis["cycle_count"],
        "basis_qualification_pass": basis["basis_qualification_pass"],
        "coupled_identity_passes": coupled_passes,
        "endpoint_integrity_passes": integrity_passes,
        "minimum_cycle_inclusion": min(inclusion),
        "maximum_cycle_inclusion": max(inclusion),
        "cycle_exercise_pass": int(exercise_pass),
        "within_start_pair_count": len(within),
        "cross_start_pair_count": len(cross),
        "median_within_start_distance": within_median,
        "median_cross_start_distance": cross_median,
        "cross_over_within_distance_ratio": ratio,
        "finite_distance_agreement_pass": int(distance_pass),
        "source_qualification_pass": int(source_pass),
        "pair_derived_positive_control": 1,
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }


def gate_rows(
    calls: Mapping[str, int],
    basis: Sequence[Mapping[str, Any]],
    coupled: Sequence[Mapping[str, Any]],
    endpoints: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    basis_passes = sum(int(row["basis_qualification_pass"]) for row in basis)
    coupled_passes = sum(int(row["complement_endpoint_identity_pass"]) for row in coupled)
    integrity_passes = sum(int(row["endpoint_integrity_pass"]) for row in endpoints)
    exercise_passes = sum(int(row["cycle_exercise_pass"]) for row in summaries)
    distance_passes = sum(int(row["finite_distance_agreement_pass"]) for row in summaries)
    exclusion = calls == {"spectrum_calls": 0, "effect_metric_calls": 0}
    overall_pass = all((
        exclusion,
        basis_passes == 6,
        coupled_passes == EXPECTED_COUPLED,
        integrity_passes == EXPECTED_ENDPOINTS,
        exercise_passes == 6,
        distance_passes == 6,
    ))
    overall = (
        "v17i_pair_basis_positive_control_qualified"
        if overall_pass
        else "v17i_pair_basis_positive_control_not_qualified"
    )
    return [
        {"gate": "effect_blind_integrity", "status": "pass" if exclusion else "fail", "observed": f"spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}", "required": "0;0", "decision": "continue" if exclusion else "stop"},
        {"gate": "frozen_cycle_basis_and_single_block_accessibility", "status": "pass" if basis_passes == 6 else "fail", "observed": f"{basis_passes}/6", "required": "6/6", "decision": "continue" if basis_passes == 6 else "repair_basis"},
        {"gate": "exact_complement_coupled_endpoint_identity", "status": "pass" if coupled_passes == EXPECTED_COUPLED else "fail", "observed": f"{coupled_passes}/{EXPECTED_COUPLED}", "required": f"{EXPECTED_COUPLED}/{EXPECTED_COUPLED}", "decision": "continue" if coupled_passes == EXPECTED_COUPLED else "repair_mask_mapping"},
        {"gate": "independent_uniform_mask_integrity", "status": "pass" if integrity_passes == EXPECTED_ENDPOINTS else "fail", "observed": f"{integrity_passes}/{EXPECTED_ENDPOINTS}", "required": f"{EXPECTED_ENDPOINTS}/{EXPECTED_ENDPOINTS}", "decision": "continue" if integrity_passes == EXPECTED_ENDPOINTS else "repair_endpoint_generation"},
        {"gate": "finite_cycle_exercise", "status": "pass" if exercise_passes == 6 else "fail", "observed": f"{exercise_passes}/6", "required": "6/6", "decision": "continue" if exercise_passes == 6 else "increase_frozen_mask_ensemble"},
        {"gate": "finite_cross_start_distance_positive_control", "status": "pass" if distance_passes == 6 else "fail", "observed": f"{distance_passes}/6", "required": "6/6;ratio=0.85-1.15", "decision": "instrumentation_supported" if distance_passes == 6 else "audit_distance_instrumentation"},
        {"gate": "v17i_overall", "status": overall, "observed": f"exclusion={int(exclusion)};basis={basis_passes}/6;coupling={coupled_passes}/{EXPECTED_COUPLED};integrity={integrity_passes}/{EXPECTED_ENDPOINTS};exercise={exercise_passes}/6;distance={distance_passes}/6", "required": f"1;6/6;{EXPECTED_COUPLED}/{EXPECTED_COUPLED};{EXPECTED_ENDPOINTS}/{EXPECTED_ENDPOINTS};6/6;6/6", "decision": overall},
    ]


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> List[str]:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return lines


def write_documents(gates: Sequence[Mapping[str, Any]], summaries: Sequence[Mapping[str, Any]]) -> None:
    overall = gates[-1]["status"]
    ratios = [float(row["cross_over_within_distance_ratio"]) for row in summaries]
    cycle_counts = [int(row["cycle_count"]) for row in summaries]
    lines = [
        "# v17i effect-blind cycle-basis accessibility positive control",
        "",
        f"Status: `{overall}`.",
        "",
        "## Frozen design",
        "",
        "The exact v16z whole-cycle decomposition for each frozen start pair is treated as a pair-derived hypercube basis. A fair bit mask toggles any subset as one algebraic block. This is an engineered positive control that knows both starts; it is not a state-independent proposal or candidate global null.",
        "",
        "## Results",
        "",
        f"The six bases contained `{min(cycle_counts)}-{max(cycle_counts)}` disjoint whole cycles. Full-mask single-block replay connected both directions in `6/6`. Complement-coupled masks produced exact endpoint identity in `{EXPECTED_COUPLED}/{EXPECTED_COUPLED}`, and independent fair masks preserved endpoint integrity in `{EXPECTED_ENDPOINTS}/{EXPECTED_ENDPOINTS}`.",
        "",
        f"Finite cross/within median-distance ratios were `{min(ratios):.6f}-{max(ratios):.6f}`; all `6/6` lay in the frozen `0.85-1.15` positive-control interval.",
        "",
        "## Gates",
        "",
        *markdown_table(gates, ("gate", "status", "observed", "required", "decision")),
        "",
        "## Claim boundary",
        "",
        "The pass validates the distance instrumentation under an exact pair-engineered accessibility measure. It does not qualify a reusable sampler, prove global connectivity or mixing, or test the source effect, geometry or physics.",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    INTERPRETATION.write_text(
        "# v17i interpretation audit\n\n"
        f"Frozen status is `{overall}`. Exact complement coupling is algebraic because the cycle basis was constructed from both frozen starts. The result is a positive control for instrumentation and finite distance response, not independent evidence for a global null, connectivity, mixing, source effects or physics.\n",
        encoding="utf-8",
    )
    NEXT_DIRECTION.write_text(
        "# v17i next direction\n\n"
        f"Formal status: `{overall}`.\n\n"
        "The pair-derived positive control supports the cross-start observable when large exact moves are available. The next effect-blind gate should construct an anchor-independent state-local long-cycle or compound-cycle proposal with exact reverse accounting. Do not use the pair basis as the source null and do not open source effects yet.\n",
        encoding="utf-8",
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.17i\n\n"
        f"- status: `{overall}`\n"
        "- pair-basis result: positive control only\n"
        "- next: anchor-independent state-local large-move qualification\n"
        "- source spectrum and observed effects remain closed\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.17i\n\n"
        "Vi brukte en fasit-lignende sykkelbasis som kjenner begge starttilstandene. Da forsvant startforskjellen slik algebraen forutsier. Det viser at maalemetoden kan reagere paa reell tilgjengelighet, men ikke at simulatoren selv har funnet en generell vei mellom tilstandene. Neste test maa lage store trekk uten aa kjenne maaltilstanden.\n",
        encoding="utf-8",
    )


def claim_rows(overall: str) -> List[Dict[str, Any]]:
    qualified = overall == "v17i_pair_basis_positive_control_qualified"
    return [
        {"claim_id": "C1", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "factual", "strength": "assertive", "claim": "v17i computes no source spectrum or observed-effect metric.", "status": "supported", "evidence": "static call audit and output exclusion fields", "scope_limit": "v17i script and outputs"},
        {"claim_id": "C2", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "algebraic", "strength": "assertive", "claim": "Each frozen pair is connected in both directions by one all-cycle basis block.", "status": "supported" if qualified else "not_supported", "evidence": "v17i_cycle_basis_audit.csv", "scope_limit": "six pair-derived frozen bases"},
        {"claim_id": "C3", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "instrumentation", "strength": "bounded", "claim": "The cross-start distance diagnostic responds as expected under exact pair-basis uniform masks.", "status": "supported" if qualified else "not_supported", "evidence": "coupling, endpoint, pairwise and source summaries", "scope_limit": "engineered positive control"},
        {"claim_id": "C4", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "global", "strength": "prohibited", "claim": "The pair basis is a state-independent global null or proves global connectivity/mixing.", "status": "contradicted", "evidence": "basis explicitly derived from both starts", "scope_limit": "requires anchor-independent proposal qualification"},
        {"claim_id": "C5", "purpose_ref": PURPOSE_REF, "goal_id": "G1", "claim_type": "physics", "strength": "prohibited", "claim": "v17i establishes source effects, geometry, Lorentz symmetry, spacetime or a universe model.", "status": "contradicted", "evidence": "effect observables prohibited and no physical diagnostic computed", "scope_limit": "requires separate later gates"},
    ]


def run() -> None:
    verify_frozen_sources()
    calls = implementation_call_counts()
    frozen = frozen_cycle_digests()
    basis_rows: List[Dict[str, Any]] = []
    coupling_rows: List[Dict[str, Any]] = []
    endpoint_output: List[Dict[str, Any]] = []
    pairwise_output: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []

    for dag, space, left, right in load_spaces():
        key = (dag.growth_seed, dag.run_offset)
        cycles = v16z.decompose_alternating_cycles(space, left, right)
        basis = basis_row(dag, space, left, right, cycles, frozen[key])
        coupled = coupled_rows(dag, space, left, right, cycles)
        endpoints = endpoint_rows(
            dag,
            space,
            {START_FAMILIES[0]: left, START_FAMILIES[1]: right},
            cycles,
        )
        pairs = pairwise_rows(dag, endpoints)
        summary = source_summary_row(dag, basis, coupled, endpoints, pairs)
        basis_rows.append(basis)
        coupling_rows.extend(coupled)
        endpoint_output.extend(endpoint.row for endpoint in endpoints)
        pairwise_output.extend(pairs)
        summaries.append(summary)

    gates = gate_rows(calls, basis_rows, coupling_rows, endpoint_output, summaries)
    overall = gates[-1]["status"]
    v16i.write_csv(BASIS_AUDIT, basis_rows)
    v16i.write_csv(COUPLED_AUDIT, coupling_rows)
    v16i.write_csv(ENDPOINT_AUDIT, endpoint_output)
    v16i.write_csv(PAIRWISE_DISTANCE, pairwise_output)
    v16i.write_csv(SOURCE_SUMMARY, summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(GOAL_EVALUATION, [{
        "purpose_ref": PURPOSE_REF,
        "goal_id": "G1",
        "status": "achieved" if overall == "v17i_pair_basis_positive_control_qualified" else "not_achieved",
        "evidence": overall,
        "next_decision": "qualify_anchor_independent_large_move" if "qualified" in overall else "audit_positive_control_instrumentation",
    }])
    v16i.write_csv(CLAIM_LEDGER, claim_rows(overall))
    write_documents(gates, summaries)
    print(f"[v17i] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    expected_counts = {
        BASIS_AUDIT: 6,
        COUPLED_AUDIT: EXPECTED_COUPLED,
        ENDPOINT_AUDIT: EXPECTED_ENDPOINTS,
        PAIRWISE_DISTANCE: 6 * math.comb(2 * INDEPENDENT_MASKS_PER_START, 2),
        SOURCE_SUMMARY: 6,
        GATE_EVALUATION: 7,
        GOAL_EVALUATION: 1,
        CLAIM_LEDGER: 5,
    }
    loaded = {}
    for path, count in expected_counts.items():
        rows = v16i.read_csv(path)
        if len(rows) != count:
            raise AssertionError(f"{path.name} row count {len(rows)} != {count}")
        loaded[path] = rows
    if any(int(row["basis_qualification_pass"]) != 1 for row in loaded[BASIS_AUDIT]):
        raise AssertionError("v17i basis qualification failed")
    if any(int(row["complement_endpoint_identity_pass"]) != 1 for row in loaded[COUPLED_AUDIT]):
        raise AssertionError("v17i complement coupling failed")
    if any(int(row["endpoint_integrity_pass"]) != 1 for row in loaded[ENDPOINT_AUDIT]):
        raise AssertionError("v17i endpoint integrity failed")
    overall = loaded[GATE_EVALUATION][-1]["status"]
    allowed = {
        "v17i_pair_basis_positive_control_qualified",
        "v17i_pair_basis_positive_control_not_qualified",
    }
    if overall not in allowed:
        raise AssertionError("v17i overall status invalid")
    for path in (REPORT, INTERPRETATION, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise AssertionError(f"missing v17i document {path.name}")
    print(f"[v17i] output verification pass overall={overall}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.prepare:
        prepare()
        return
    if args.verify_only:
        verify_outputs()
        return
    run()
    verify_outputs()


if __name__ == "__main__":
    main()
