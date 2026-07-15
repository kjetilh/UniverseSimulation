#!/usr/bin/env python3
"""v16v: effect-blind feasibility gate for an independent global DAG null.

The construction is a global bipartite b-matching between parent out-degree
capacity and per-child edge-slot classes. It does not use the local edge-swap
chain and computes neither source spectra nor observed-effect statistics.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import random
import time
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_matrix

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16j_interval_strict_null_gate as v16j
import relational_universe_v16p_event_footprint_reachability_audit as v16p
import relational_universe_v16s_fresh_event_footprint_holdout as v16s
import relational_universe_v16t_footprint_null_path_stability_gate as v16t
import relational_universe_v16u_matched_effort_footprint_stability_gate as v16u


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

REPLICATES = 8
MIN_DISTINCT_RECONSTRUCTIONS = 4
MIN_UNIQUE_FRACTION = 0.75
MIN_CHANGED_EDGE_FRACTION = 0.10
RANDOM_TIE_BREAK_SCALE = 1e-9
INTEGRALITY_TOLERANCE = 1e-7
EQUALITY_TOLERANCE = 1e-7
SOLVER_TIME_LIMIT_SECONDS = 120.0
NULL_FAMILY = "global_child_slot_b_matching_exact_degree_depth_age_footprint"

SOURCE_CHAIN = DOC / "v16v_source_chain.csv"
PRE_REGISTRATION = DOC / "v16v_pre_registration.csv"
SLOT_SUPPORT = DOC / "v16v_edge_slot_support.csv"
RECONSTRUCTION_AUDIT = DOC / "v16v_global_reconstruction_audit.csv"
SOURCE_SUMMARY = DOC / "v16v_source_feasibility_summary.csv"
GATE_EVALUATION = DOC / "v16v_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16v_claim_ledger.csv"
REPORT = DOC / "v16v_global_edge_slot_feasibility_gate.md"
NEXT_DIRECTION = DOC / "v16v_next_direction_assessment.md"
ACTION_ENERGY_HYPOTHESIS = DOC / "v16v_units_of_action_energy_temperature_hypothesis.md"
RECOMMENDATION = DOC / "v0_16v_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16v.md"

Role = Tuple[str, Tuple[str, ...]]
SlotClass = Tuple[Role, int, str]
RunKey = Tuple[int, int, str, int]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v16s", "frozen_event_histories", v16s.EVENT_LOG),
        ("v16s", "frozen_dependency_edges", v16s.EDGE_LOG),
        ("v16s", "fresh_history_gate", v16s.GATE_EVALUATION),
        ("v16p", "event_footprint_definition", Path(v16p.__file__)),
        ("v16u", "matched_effort_gate", v16u.GATE_EVALUATION),
        ("v16u", "independent_null_recommendation", v16u.NEXT_DIRECTION if hasattr(v16u, "NEXT_DIRECTION") else DOC / "v16u_next_direction_assessment.md"),
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
        "gate": "v16v_global_edge_slot_feasibility_gate",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_independent_global_null_feasibility_and_diversity",
        "source_history_count": 6,
        "source_arm": v16s.PRIMARY_ARM,
        "null_family": NULL_FAMILY,
        "construction": "global_bipartite_b_matching_linear_program",
        "parent_constraint": "exact_outdegree_capacity",
        "child_slot_class": [
            "exact_source_event_role",
            "exact_dyadic_parent_age_bin",
            "exact_depth_witness_or_lower_class",
        ],
        "target_event_role": "fixed_by_child",
        "duplicate_parent_child_edges": "forbidden_by_one_variable_per_pair",
        "objective": "minimize_retained_source_edges_then_independent_random_tie_break",
        "replicates_per_source": REPLICATES,
        "minimum_distinct_reconstructions_per_source": MIN_DISTINCT_RECONSTRUCTIONS,
        "minimum_unique_fraction_per_source": MIN_UNIQUE_FRACTION,
        "minimum_changed_edge_fraction": MIN_CHANGED_EDGE_FRACTION,
        "random_tie_break_scale": RANDOM_TIE_BREAK_SCALE,
        "integrality_tolerance": INTEGRALITY_TOLERANCE,
        "equality_tolerance": EQUALITY_TOLERANCE,
        "solver_time_limit_seconds": SOLVER_TIME_LIMIT_SECONDS,
        "all_source_dags_must_pass": True,
        "local_switch_construction_allowed": False,
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "no_early_stop": True,
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
        "source_arm": v16s.PRIMARY_ARM,
        "null_family": NULL_FAMILY,
        "replicates_per_source": REPLICATES,
        "minimum_distinct_reconstructions_per_source": MIN_DISTINCT_RECONSTRUCTIONS,
        "minimum_unique_fraction_per_source": MIN_UNIQUE_FRACTION,
        "minimum_changed_edge_fraction": MIN_CHANGED_EDGE_FRACTION,
        "random_tie_break_scale": RANDOM_TIE_BREAK_SCALE,
        "solver_time_limit_seconds": SOLVER_TIME_LIMIT_SECONDS,
        "local_switch_construction_allowed": 0,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v16u.verify_outputs()
    overall = next(
        row["status"] for row in v16i.read_csv(v16u.GATE_EVALUATION)
        if row["gate"] == "v16u_overall"
    )
    if overall != "v16u_footprint_null_centers_stable_under_exact_matched_effort":
        raise ValueError("v16v requires the frozen successful v16u gate")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v16v] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    rows = v16i.read_csv(PRE_REGISTRATION)
    expected = {key: str(value) for key, value in preregistration_row().items()}
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v16v preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v16v source chain changed")


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    loaded: List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]] = []
    for dag, metadata in v16u.load_runs():
        loaded.append((v16i.RunDAG(
            stage="v16v",
            target_nodes=dag.target_nodes,
            growth_seed=dag.growth_seed,
            run_offset=dag.run_offset,
            arm=dag.arm,
            run_seed=dag.run_seed,
            predecessors=dag.predecessors,
            depths=dag.depths,
            indegrees=dag.indegrees,
        ), metadata))
    if len(loaded) != 6:
        raise ValueError("v16v requires six frozen v16s histories")
    return loaded


def role_text(role: Role) -> str:
    return f"{role[0]}[{'&'.join(role[1])}]"


def depth_relation(parent: int, child: int, depths: Sequence[int]) -> str:
    if depths[parent] == depths[child] - 1:
        return "witness"
    if depths[parent] < depths[child] - 1:
        return "lower"
    return "incompatible"


def slot_class(
    parent: int,
    child: int,
    depths: Sequence[int],
    metadata: Sequence[Mapping[str, Any]],
) -> SlotClass:
    if parent >= child:
        raise ValueError("slot class requires scheduler order")
    return (
        v16p.source_role(metadata[parent]),
        v16j.lag_bin(parent, child),
        depth_relation(parent, child, depths),
    )


def slot_signature(
    predecessors: Sequence[Sequence[int]],
    depths: Sequence[int],
    metadata: Sequence[Mapping[str, Any]],
) -> Tuple[Tuple[int, Tuple[Tuple[str, int], ...]], ...]:
    rows = []
    for child, parents in enumerate(predecessors):
        counts = Counter(
            f"{role_text(role)}|age={age_bin}|depth={relation}"
            for role, age_bin, relation in (
                slot_class(parent, child, depths, metadata) for parent in parents
            )
        )
        rows.append((child, tuple(sorted(counts.items()))))
    return tuple(rows)


@dataclass(frozen=True)
class MatchingModel:
    candidates: Tuple[Tuple[int, int], ...]
    source_edges: frozenset[Tuple[int, int]]
    constraint_matrix: csr_matrix
    demands: np.ndarray
    support_rows: Tuple[Dict[str, Any], ...]
    source_assignment_pass: bool
    edge_count: int
    active_parent_count: int
    slot_class_count: int


def build_matching_model(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
) -> MatchingModel:
    original = dag.predecessors
    source_edges = frozenset(
        (parent, child) for child, parents in enumerate(original) for parent in parents
    )
    parent_demands = v16j.outdegrees(original)
    parent_rows = {
        parent: index
        for index, parent in enumerate(parent for parent, demand in enumerate(parent_demands) if demand)
    }

    requirements: Dict[Tuple[int, SlotClass], int] = {}
    requirements_by_child: Dict[int, Counter[SlotClass]] = {}
    for child, parents in enumerate(original):
        counts = Counter(slot_class(parent, child, dag.depths, metadata) for parent in parents)
        if any(relation == "incompatible" for _, _, relation in counts):
            raise ValueError("source edge has incompatible depth")
        requirements_by_child[child] = counts
        for klass, count in sorted(counts.items(), key=lambda item: repr(item[0])):
            requirements[(child, klass)] = count

    class_rows = {
        key: len(parent_rows) + index
        for index, key in enumerate(sorted(requirements, key=lambda item: (item[0], repr(item[1]))))
    }

    candidates: List[Tuple[int, int]] = []
    candidate_classes: List[SlotClass] = []
    support: Counter[Tuple[int, SlotClass]] = Counter()
    for child in range(len(original)):
        required = requirements_by_child[child]
        if not required:
            continue
        for parent in range(child):
            klass = slot_class(parent, child, dag.depths, metadata)
            if klass in required and parent_demands[parent] > 0:
                candidates.append((parent, child))
                candidate_classes.append(klass)
                support[(child, klass)] += 1

    row_indices: List[int] = []
    column_indices: List[int] = []
    data: List[float] = []
    for column, ((parent, child), klass) in enumerate(zip(candidates, candidate_classes)):
        row_indices.extend((parent_rows[parent], class_rows[(child, klass)]))
        column_indices.extend((column, column))
        data.extend((1.0, 1.0))

    constraint_count = len(parent_rows) + len(class_rows)
    matrix = coo_matrix(
        (data, (row_indices, column_indices)),
        shape=(constraint_count, len(candidates)),
        dtype=float,
    ).tocsr()
    demands = np.zeros(constraint_count, dtype=float)
    for parent, row in parent_rows.items():
        demands[row] = parent_demands[parent]
    for key, row in class_rows.items():
        demands[row] = requirements[key]

    candidate_index = {edge: index for index, edge in enumerate(candidates)}
    source_vector = np.zeros(len(candidates), dtype=float)
    source_assignment_pass = all(edge in candidate_index for edge in source_edges)
    if source_assignment_pass:
        for edge in source_edges:
            source_vector[candidate_index[edge]] = 1.0
        source_assignment_pass = bool(
            np.max(np.abs(matrix @ source_vector - demands), initial=0.0) <= EQUALITY_TOLERANCE
        )

    support_rows: List[Dict[str, Any]] = []
    for (child, klass), demand in sorted(requirements.items(), key=lambda item: (item[0][0], repr(item[0][1]))):
        role, age_bin, relation = klass
        candidate_count = support[(child, klass)]
        support_rows.append({
            **dag.prefix,
            "child_event_id": child,
            "child_depth": dag.depths[child],
            "source_role": role_text(role),
            "target_role": v16p.role_text(v16p.target_role(metadata[child])),
            "dyadic_age_bin": age_bin,
            "depth_relation": relation,
            "required_slot_count": demand,
            "candidate_parent_count": candidate_count,
            "support_surplus": candidate_count - demand,
            "local_support_pass": int(candidate_count >= demand),
        })

    return MatchingModel(
        candidates=tuple(candidates),
        source_edges=source_edges,
        constraint_matrix=matrix,
        demands=demands,
        support_rows=tuple(support_rows),
        source_assignment_pass=source_assignment_pass,
        edge_count=len(source_edges),
        active_parent_count=len(parent_rows),
        slot_class_count=len(class_rows),
    )


def reconstruct(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    model: MatchingModel,
    replicate: int,
) -> Tuple[Tuple[Tuple[int, ...], ...] | None, Dict[str, Any]]:
    seed = v16i.stable_seed("v16v", "global_objective", *dag.key, replicate)
    rng = random.Random(seed)
    source_mask = np.fromiter(
        (1.0 if edge in model.source_edges else 0.0 for edge in model.candidates),
        dtype=float,
        count=len(model.candidates),
    )
    jitter = np.fromiter(
        (rng.random() * RANDOM_TIE_BREAK_SCALE for _ in model.candidates),
        dtype=float,
        count=len(model.candidates),
    )
    objective = source_mask + jitter
    started = time.monotonic()
    result = linprog(
        objective,
        A_eq=model.constraint_matrix,
        b_eq=model.demands,
        bounds=(0.0, 1.0),
        method="highs",
        options={"time_limit": SOLVER_TIME_LIMIT_SECONDS, "presolve": True},
    )
    elapsed = time.monotonic() - started
    base = {
        **dag.prefix,
        "null_family": NULL_FAMILY,
        "reconstruction_replicate": replicate,
        "objective_seed": seed,
        "candidate_edge_count": len(model.candidates),
        "constraint_count": model.constraint_matrix.shape[0],
        "solver_status": int(result.status),
        "solver_success": int(result.success),
        "solver_message": str(result.message),
        "solver_iterations": int(result.nit),
        "solver_seconds": elapsed,
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
        "local_switch_steps": 0,
    }
    if not result.success or result.x is None:
        return None, {
            **base,
            "integrality_error": math.nan,
            "equality_residual": math.nan,
            "selected_edge_count": 0,
            "retained_source_edge_count": 0,
            "changed_edge_count": 0,
            "changed_edge_fraction": 0.0,
            "edge_count_pass": 0,
            "scheduler_order_pass": 0,
            "indegree_sequence_pass": 0,
            "outdegree_sequence_pass": 0,
            "depth_sequence_pass": 0,
            "global_age_bin_histogram_pass": 0,
            "global_event_footprint_histogram_pass": 0,
            "per_child_slot_signature_pass": 0,
            "structure_pass": 0,
            "change_pass": 0,
            "reconstruction_integrity_pass": 0,
            "null_edge_sha256": "",
        }

    values = np.asarray(result.x, dtype=float)
    rounded = np.rint(values)
    integrality_error = float(np.max(np.abs(values - rounded), initial=0.0))
    equality_residual = float(
        np.max(np.abs(model.constraint_matrix @ rounded - model.demands), initial=0.0)
    )
    selected = [model.candidates[index] for index, value in enumerate(rounded) if value > 0.5]
    predecessors: List[List[int]] = [[] for _ in dag.predecessors]
    for parent, child in selected:
        predecessors[child].append(parent)
    rewired = tuple(tuple(sorted(parents)) for parents in predecessors)
    audit = v16t.final_structure_audit(dag, metadata, rewired)
    slot_pass = slot_signature(rewired, dag.depths, metadata) == slot_signature(
        dag.predecessors, dag.depths, metadata
    )
    change_pass = float(audit["changed_edge_fraction"]) >= MIN_CHANGED_EDGE_FRACTION
    integrity_pass = all((
        result.success,
        integrality_error <= INTEGRALITY_TOLERANCE,
        equality_residual <= EQUALITY_TOLERANCE,
        int(audit["structure_pass"]),
        slot_pass,
        len(selected) == model.edge_count,
    ))
    return rewired, {
        **base,
        "integrality_error": integrality_error,
        "equality_residual": equality_residual,
        "selected_edge_count": len(selected),
        "retained_source_edge_count": model.edge_count - int(audit["changed_edge_count"]),
        **audit,
        "per_child_slot_signature_pass": int(slot_pass),
        "change_pass": int(change_pass),
        "reconstruction_integrity_pass": int(integrity_pass),
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
        "local_switch_calls": names["footprint_rewire"] + names["exact_footprint_path"],
        "spectrum_calls": names["interval_spectrum"],
        "effect_metric_calls": names["jensen_shannon"],
    }


def summarize_source(
    dag: v16i.RunDAG,
    model: MatchingModel,
    audits: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    successful = [row for row in audits if int(row["reconstruction_integrity_pass"])]
    digests = {str(row["null_edge_sha256"]) for row in successful}
    unique_count = len(digests)
    unique_fraction = unique_count / REPLICATES
    min_change = min((float(row["changed_edge_fraction"]) for row in successful), default=0.0)
    all_support = all(int(row["local_support_pass"]) for row in model.support_rows)
    feasibility_pass = (
        model.source_assignment_pass
        and all_support
        and len(successful) == REPLICATES
    )
    diversity_pass = (
        unique_count >= MIN_DISTINCT_RECONSTRUCTIONS
        and unique_fraction >= MIN_UNIQUE_FRACTION
        and min_change >= MIN_CHANGED_EDGE_FRACTION
    )
    return {
        **dag.prefix,
        "null_family": NULL_FAMILY,
        "node_count": len(dag.predecessors),
        "edge_count": model.edge_count,
        "active_parent_count": model.active_parent_count,
        "slot_class_count": model.slot_class_count,
        "candidate_edge_count": len(model.candidates),
        "candidate_to_source_edge_ratio": len(model.candidates) / model.edge_count,
        "minimum_slot_candidate_parent_count": min(
            int(row["candidate_parent_count"]) for row in model.support_rows
        ),
        "minimum_slot_support_surplus": min(
            int(row["support_surplus"]) for row in model.support_rows
        ),
        "blocked_slot_class_count": sum(
            not int(row["local_support_pass"]) for row in model.support_rows
        ),
        "source_assignment_pass": int(model.source_assignment_pass),
        "successful_reconstructions": len(successful),
        "required_reconstructions": REPLICATES,
        "distinct_reconstruction_count": unique_count,
        "unique_reconstruction_fraction": unique_fraction,
        "minimum_changed_edge_fraction": min_change,
        "maximum_changed_edge_fraction": max(
            (float(row["changed_edge_fraction"]) for row in successful), default=0.0
        ),
        "all_reconstruction_integrity_pass": int(len(successful) == REPLICATES),
        "feasibility_pass": int(feasibility_pass),
        "diversity_pass": int(diversity_pass),
        "source_gate_pass": int(feasibility_pass and diversity_pass),
    }


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> List[str]:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = row[column]
            values.append(f"{value:.6f}" if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return lines


def build_report(
    summaries: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16v global edge-slot feasibility gate",
        "",
        f"Status: `{overall}`.",
        "",
        "V16v is an effect-blind feasibility and diversity audit for a null construction independent of the local event-footprint switch chain. It computes no source interval spectrum and no observed/null effect statistic.",
        "",
        f"Specification digest: `{spec_digest()}`.",
        "",
        "## Frozen construction",
        "",
        "Each original parent contributes its exact out-degree as capacity. Each child contributes edge-slot demand classified by source event role, dyadic parent-age bin, and whether the parent is an exact causal-depth witness or a lower-depth parent. The child fixes the target event role. One variable exists per legal parent-child pair, so duplicate edges are impossible.",
        "",
        "The complete assignment is solved globally as a bipartite b-matching linear program. Bipartite incidence makes the feasible polytope integral; every returned solution is nevertheless checked explicitly for integrality and equality residual. The objective first minimizes retained source edges, then uses an independently seeded random tie-break. No edge-swap trajectory is used.",
        "",
        f"All six sources receive `{REPLICATES}` objectives. A source passes only with all reconstructions structurally valid, at least `{MIN_DISTINCT_RECONSTRUCTIONS}` distinct endpoints, unique fraction at least `{MIN_UNIQUE_FRACTION:.2f}`, and changed-edge fraction at least `{MIN_CHANGED_EDGE_FRACTION:.2f}`.",
        "",
        "## Source summaries",
        "",
    ]
    lines.extend(markdown_table(summaries, (
        "growth_seed", "run_offset", "edge_count", "candidate_edge_count",
        "minimum_slot_candidate_parent_count", "successful_reconstructions",
        "distinct_reconstruction_count", "minimum_changed_edge_fraction",
        "source_gate_pass",
    )))
    lines.extend(["", "## Gates", ""])
    lines.extend(markdown_table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Evidential boundary",
        "",
        "A pass establishes only that the six frozen finite source DAGs admit multiple exact global reconstructions under this stronger per-child slot constraint, and that the implementation is independent of the local switch path. It does not establish a probability measure, uniformity, representativeness, stationarity, or equivalence to the local-switch null.",
        "",
        "V16v does not re-evaluate the v16s spectrum contrast. It establishes no energy, temperature, dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particle, entanglement, invariant, or physical law.",
        "",
    ])
    return "\n".join(lines)


def build_next_direction(overall: str) -> str:
    passed = overall == "v16v_independent_global_null_family_feasible_and_diverse"
    if passed:
        decision = (
            "Freeze the global edge-slot construction and run v16w as an effect-blind qualification gate. "
            "Increase endpoint count, test replay and relabel invariance, quantify endpoint diversity and "
            "center stability within the global family, and still exclude every source spectrum. Only after "
            "qualification may one preregister a single independent-null effect test."
        )
    else:
        decision = (
            "Do not relax constraints post hoc. Identify whether the block is local slot support, solver "
            "integrity, changed-edge reach, or endpoint diversity. Test only the smallest predeclared "
            "effect-blind relaxation, or retire this independent-null route."
        )
    return "\n".join([
        "# v16v interpretation and next direction",
        "",
        f"Status: `{overall}`.",
        "",
        "## Decision",
        "",
        decision,
        "",
        "## Units of action and effective temperature",
        "",
        "The user-proposed cooling question is retained as a separate mechanism hypothesis. The current model has mobile action carriers and local rewrite events, so local realized change may support an emergent energy-density candidate. Temperature is not yet defined, and the older weighted energy functional is not evidence that one emerged.",
        "",
        "The smallest defensible future gate must first define local edit work and action flux on intrinsic causal windows, then test whether their distribution supports a reproducible intensive fluctuation parameter. Uniformly multiplying all Gillespie rates is not cooling: it changes elapsed clock time while leaving the embedded event-order distribution unchanged. A legitimate intervention must alter action-carrier density or relative rewrite/acceptance statistics while matching total observation effort.",
        "",
        "Keep this mechanism gate downstream of v16w so an unresolved null-family issue is not confused with thermodynamic interpretation.",
        "",
    ])


def build_action_energy_hypothesis() -> str:
    return "\n".join([
        "# Units of action, emergent energy, and a cooling hypothesis",
        "",
        "Date: 2026-07-15",
        "",
        "## Repo-grounded starting point",
        "",
        "The base simulator defines local rewrite events as units of action and implements mobile tokens as action carriers. Token count was also used in an early candidate energy functional, alongside cycle rank and graph stress. Those weighted terms were chosen diagnostics; they did not demonstrate emergent energy.",
        "",
        "A stronger route starts from realized change rather than naming token count energy. For an intrinsic region R and causal window W, record:",
        "",
        "- local edit work: created/deleted nodes and edges per event under a frozen nonnegative edit metric;",
        "- action-carrier occupancy and flux through the boundary of R;",
        "- event-family composition and local waiting-time statistics;",
        "- persistence, recurrence, and breakup rates of matched defect morphologies.",
        "",
        "A candidate local energy density must aggregate these microscopic changes consistently and support a balance equation: change inside R equals local production plus inward flux minus outward flux, within declared residuals. A candidate effective temperature should then be inferred from repeatable fluctuation or entropy-vs-energy behavior, not declared equal to one simulator parameter.",
        "",
        "## Cooling hypothesis",
        "",
        "The physical analogy is legitimate but not evidence. In the real early universe, extreme temperature prevented some bound structures; expansion and cooling enabled quarks to form hadrons and later nuclei and neutral atoms. Authoritative background: CERN, 'The early universe' and 'Heavy ions and quark-gluon plasma'; NASA, 'Universe overview'.",
        "",
        "Repo hypothesis: at high local action density, persistent structures may be disrupted faster than they bind; at intermediate density they may form and anneal; at very low density they may fail to encounter or repair. This predicts a non-monotonic stability window, not simply 'colder is always better'.",
        "",
        "## Smallest future experiment",
        "",
        "1. Freeze one defect constructor, one placement family, matched graph bases, and intrinsic observation windows.",
        "2. Intervene on action-carrier density or relative local rewrite acceptance at three levels; do not scale every rate uniformly.",
        "3. Match total accepted local events or causal-window exposure across levels.",
        "4. Measure formation probability, lifetime, recurrence, breakup hazard, local edit-work density, and boundary action flux.",
        "5. Require a fresh holdout to reproduce any ordered or non-monotonic relation.",
        "",
        "Until a local balance law and reproducible intensive parameter exist, use 'action density' or 'change intensity', not physical energy or temperature.",
        "",
        "## Sources",
        "",
        "- https://home.cern/science/physics/early-universe/",
        "- https://home.cern/science/physics/heavy-ions-and-quark-gluon-plasma/",
        "- https://science.nasa.gov/universe/overview/",
        "",
    ])


def run() -> None:
    verify_frozen_sources()
    runs = load_runs()
    call_counts = implementation_call_counts()
    support_rows: List[Dict[str, Any]] = []
    audit_rows: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []

    for run_index, (dag, metadata) in enumerate(runs, start=1):
        model = build_matching_model(dag, metadata)
        support_rows.extend(model.support_rows)
        source_audits: List[Dict[str, Any]] = []
        for replicate in range(REPLICATES):
            _, audit = reconstruct(dag, metadata, model, replicate)
            source_audits.append(audit)
            audit_rows.append(audit)
        summary = summarize_source(dag, model, source_audits)
        summaries.append(summary)
        print(
            f"[v16v] sources={run_index}/{len(runs)} "
            f"success={summary['successful_reconstructions']}/{REPLICATES} "
            f"unique={summary['distinct_reconstruction_count']} "
            f"min_change={float(summary['minimum_changed_edge_fraction']):.6f}"
        )

    expected = len(runs) * REPLICATES
    support_pass = all(
        int(row["source_assignment_pass"]) and int(row["blocked_slot_class_count"]) == 0
        for row in summaries
    )
    reconstruction_pass = (
        len(audit_rows) == expected
        and all(int(row["reconstruction_integrity_pass"]) for row in audit_rows)
    )
    diversity_pass = all(int(row["diversity_pass"]) for row in summaries)
    independence_pass = call_counts["local_switch_calls"] == 0
    exclusion_pass = call_counts["spectrum_calls"] == 0 and call_counts["effect_metric_calls"] == 0

    if not support_pass:
        overall = "v16v_global_edge_slot_support_infeasible"
    elif not reconstruction_pass:
        overall = "v16v_global_reconstruction_instrumentation_failed"
    elif not diversity_pass:
        overall = "v16v_global_constraints_nearly_determine_sources"
    elif not independence_pass or not exclusion_pass:
        overall = "v16v_effect_blind_independence_audit_failed"
    else:
        overall = "v16v_independent_global_null_family_feasible_and_diverse"

    gates = [
        {
            "gate": "frozen_source_and_slot_support",
            "status": "pass" if support_pass else "fail",
            "observed": f"sources={sum(int(row['source_assignment_pass']) for row in summaries)}/6;blocked={sum(int(row['blocked_slot_class_count']) for row in summaries)}",
            "required": "sources=6/6;blocked=0",
            "decision": "continue" if support_pass else "diagnose_smallest_constraint_block",
        },
        {
            "gate": "global_reconstruction_integrity",
            "status": "pass" if reconstruction_pass else "fail",
            "observed": f"{sum(int(row['reconstruction_integrity_pass']) for row in audit_rows)}/{len(audit_rows)}",
            "required": f"{expected}/{expected}",
            "decision": "continue" if reconstruction_pass else "instrumentation_failed",
        },
        {
            "gate": "per_source_endpoint_diversity",
            "status": "pass" if diversity_pass else "fail",
            "observed": ";".join(
                f"{int(row['growth_seed'])}:{int(row['run_offset'])}=u{int(row['distinct_reconstruction_count'])},c{float(row['minimum_changed_edge_fraction']):.6f}"
                for row in summaries
            ),
            "required": f"unique>={MIN_DISTINCT_RECONSTRUCTIONS};fraction>={MIN_UNIQUE_FRACTION};change>={MIN_CHANGED_EDGE_FRACTION}",
            "decision": "diverse" if diversity_pass else "route_nearly_determined",
        },
        {
            "gate": "independent_from_local_switch_path",
            "status": "pass" if independence_pass else "fail",
            "observed": f"local_switch_calls={call_counts['local_switch_calls']}",
            "required": "0",
            "decision": "independent_construction" if independence_pass else "reject",
        },
        {
            "gate": "observed_spectrum_and_effect_exclusion",
            "status": "pass" if exclusion_pass else "fail",
            "observed": f"source_spectrum_calls={call_counts['spectrum_calls']};effect_metric_calls={call_counts['effect_metric_calls']}",
            "required": "0;0",
            "decision": "effect_blind" if exclusion_pass else "reject",
        },
        {
            "gate": "v16v_overall",
            "status": overall,
            "observed": f"support={int(support_pass)};integrity={int(reconstruction_pass)};diversity={int(diversity_pass)};independence={int(independence_pass)};exclusion={int(exclusion_pass)}",
            "required": "1;1;1;1;1",
            "decision": overall,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "All six frozen v16s DAGs admit multiple exact global edge-slot reconstructions.",
            "status": "supported" if overall == "v16v_independent_global_null_family_feasible_and_diverse" else "not_supported",
            "evidence": "v16v_source_feasibility_summary.csv;v16v_global_reconstruction_audit.csv",
            "scope_limit": "six finite source DAGs and the frozen stronger per-child slot classes",
        },
        {
            "claim_id": "C2",
            "claim": "The v16v reconstruction is independent of the v16q local switch trajectory.",
            "status": "supported" if independence_pass else "not_supported",
            "evidence": "v16v_gate_evaluation.csv;relational_universe_v16v_global_edge_slot_feasibility_gate.py",
            "scope_limit": "construction independence, not statistical independence of resulting distributions",
        },
        {
            "claim_id": "C3",
            "claim": "The independent global null is qualified as a representative sampling distribution.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "feasibility and diversity do not establish a probability measure or representativeness",
        },
        {
            "claim_id": "C4",
            "claim": "The v16s observed spectrum contrast survives the independent global null.",
            "status": "not_evaluated",
            "evidence": "v16v_gate_evaluation.csv",
            "scope_limit": "source spectra and effect metrics were excluded",
        },
        {
            "claim_id": "C5",
            "claim": "Units of action have been shown to constitute physical energy or temperature.",
            "status": "unsupported",
            "evidence": "v16v_units_of_action_energy_temperature_hypothesis.md",
            "scope_limit": "a repo-grounded future hypothesis only",
        },
    ]

    v16i.write_csv(SLOT_SUPPORT, support_rows)
    v16i.write_csv(RECONSTRUCTION_AUDIT, audit_rows)
    v16i.write_csv(SOURCE_SUMMARY, summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    REPORT.write_text(build_report(summaries, gates, overall), encoding="utf-8")
    NEXT_DIRECTION.write_text(build_next_direction(overall), encoding="utf-8")
    ACTION_ENERGY_HYPOTHESIS.write_text(build_action_energy_hypothesis(), encoding="utf-8")
    RECOMMENDATION.write_text(
        "# Operativ anbefaling etter v16v\n\n"
        f"Status: `{overall}`.\n\n"
        + (
            "Frys den globale edge-slot-konstruksjonen og kvalifiser den effektblindt i v16w foer én ny effekttest. Hold action-energy/temperature-hypotesen som neste mekanismespor.\n"
            if overall == "v16v_independent_global_null_family_feasible_and_diverse"
            else "Ikke bruk en uavhengig effekt-test ennå. Diagnostiser minste blokkerende constraint uten post-hoc effektinnsyn.\n"
        ),
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.16v\n\n"
        f"Statusen er `{overall}`. Denne runden forsøker å bygge hele kontrollgrafen på nytt i ett globalt matching-problem, uten den gamle lokale bytteprosessen og uten å se på hovedsignalet. Dette tester om kontrollfamilien kan gjøres mer uavhengig; det er ikke et funn av energi, temperatur eller romtid.\n",
        encoding="utf-8",
    )
    print(f"[v16v] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    audits = v16i.read_csv(RECONSTRUCTION_AUDIT)
    summaries = v16i.read_csv(SOURCE_SUMMARY)
    gates = v16i.read_csv(GATE_EVALUATION)
    expected = 6 * REPLICATES
    if len(audits) != expected or len(summaries) != 6:
        raise ValueError("v16v output row counts failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16v_overall")
    allowed = {
        "v16v_global_edge_slot_support_infeasible",
        "v16v_global_reconstruction_instrumentation_failed",
        "v16v_global_constraints_nearly_determine_sources",
        "v16v_effect_blind_independence_audit_failed",
        "v16v_independent_global_null_family_feasible_and_diverse",
    }
    if overall not in allowed:
        raise ValueError("v16v unknown overall status")
    exclusion = next(row for row in gates if row["gate"] == "observed_spectrum_and_effect_exclusion")
    independence = next(row for row in gates if row["gate"] == "independent_from_local_switch_path")
    if exclusion["status"] != "pass" or independence["status"] != "pass":
        raise ValueError("v16v effect-blind independence failed")
    if overall == "v16v_independent_global_null_family_feasible_and_diverse":
        if not all(int(row["reconstruction_integrity_pass"]) for row in audits):
            raise ValueError("v16v reconstruction integrity failed")
        if not all(int(row["source_gate_pass"]) for row in summaries):
            raise ValueError("v16v source gate failed")
    for path in (REPORT, NEXT_DIRECTION, ACTION_ENERGY_HYPOTHESIS, RECOMMENDATION, NONSPECIALIST):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"v16v missing report {path.name}")
    print(f"[v16v] output verification pass overall={overall}")


def self_test() -> None:
    predecessors = (
        (), (), (), (), (), (),
        (0, 1), (2, 3),
        (), (), (), (),
    )
    depths = tuple(v16i.recompute_depths(predecessors))
    dag = v16i.RunDAG(
        stage="v16v_test",
        target_nodes=12,
        growth_seed=1,
        run_offset=2,
        arm="test",
        run_seed=3,
        predecessors=predecessors,
        depths=depths,
        indegrees=tuple(len(parents) for parents in predecessors),
    )
    metadata = tuple({"family": "swap", "writes": {"graph:any"}, "reads": {"graph:any"}} for _ in predecessors)
    model = build_matching_model(dag, metadata)
    if not model.source_assignment_pass or len(model.candidates) <= model.edge_count:
        raise AssertionError("v16v synthetic candidate model failed")
    rewired, audit = reconstruct(dag, metadata, model, 0)
    if rewired is None or not int(audit["reconstruction_integrity_pass"]):
        raise AssertionError("v16v synthetic reconstruction failed")
    if implementation_call_counts() != {
        "local_switch_calls": 0,
        "spectrum_calls": 0,
        "effect_metric_calls": 0,
    }:
        raise AssertionError("v16v implementation exclusion audit failed")
    payload = spec_payload()
    if payload["source_spectrum_computation_allowed"] or payload["observed_effect_computation_allowed"]:
        raise AssertionError("v16v effect exclusion payload failed")
    print("[v16v] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16v independent global edge-slot feasibility gate")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if sum((args.prepare_only, args.self_test, args.verify_only)) > 1:
        parser.error("choose at most one mode")
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
