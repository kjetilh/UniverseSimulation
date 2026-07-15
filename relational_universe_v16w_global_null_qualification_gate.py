#!/usr/bin/env python3
"""v16w effect-blind qualification of the global edge-slot null procedure.

This gate qualifies procedure behavior only. It never computes a source
spectrum or an observed/null effect. The frozen v16v global b-matching
constraints are retained while replay, representation covariance, endpoint
diversity, finite batch-center stability, and objective sensitivity are tested.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import random
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from statistics import median
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import numpy as np
from scipy.optimize import linprog

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16n_coarse_event_resource_null_calibration as v16n
import relational_universe_v16v_global_edge_slot_feasibility_gate as v16v


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

PRIMARY_REPLICATES = 32
SENSITIVITY_REPLICATES = 16
CHECK_REPLICATES = (0, 7, 15, 31)
RELABEL_SEEDS = (161803, 271828, 314159, 577215)
OBJECTIVE_ARMS = ("retain_min", "random_priority")
PRIMARY_ARM = "retain_min"
SENSITIVITY_ARM = "random_priority"

MIN_UNIQUE_FRACTION = 0.90
MIN_MEDIAN_PAIRWISE_CHANGE = 0.20
MIN_CANDIDATE_UNION_COVERAGE = 0.20
MIN_EFFECTIVE_EDGE_SUPPORT_RATIO = 0.10
MAX_NONFORCED_EDGE_INCLUSION_RATE = 0.95
MAX_BATCH_CENTER_RANGE_RATIO = 0.35
MAX_OBJECTIVE_CENTER_RANGE_RATIO = 0.35
MIN_CHANGED_EDGE_FRACTION = 0.10
LEXICOGRAPHIC_JITTER_BUDGET = 0.25
INTEGRALITY_TOLERANCE = 1e-7
EQUALITY_TOLERANCE = 1e-7
SOLVER_TIME_LIMIT_SECONDS = 120.0

NULL_FAMILY = "global_child_slot_b_matching_exact_degree_depth_age_footprint"
CENTER_FEATURES = (
    "source_edge_fraction",
    "normalized_mean_parent_lag",
    "mean_depth_gap",
    "concrete_conflict_fraction",
    "mean_candidate_rank_fraction",
    "mean_pairwise_changed_fraction",
)

SOURCE_CHAIN = DOC / "v16w_source_chain.csv"
PRE_REGISTRATION = DOC / "v16w_pre_registration.csv"
ENDPOINT_AUDIT = DOC / "v16w_endpoint_audit.csv"
PAIRWISE_DISTANCE = DOC / "v16w_pairwise_endpoint_distance.csv"
REPLAY_ORDER_AUDIT = DOC / "v16w_replay_and_order_audit.csv"
ROLE_RELABEL_AUDIT = DOC / "v16w_role_relabel_audit.csv"
BATCH_CENTER_STABILITY = DOC / "v16w_batch_center_stability.csv"
OBJECTIVE_SENSITIVITY = DOC / "v16w_objective_sensitivity.csv"
SOURCE_SUMMARY = DOC / "v16w_source_qualification_summary.csv"
GATE_EVALUATION = DOC / "v16w_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16w_claim_ledger.csv"
REPORT = DOC / "v16w_global_null_qualification_gate.md"
NEXT_DIRECTION = DOC / "v16w_next_direction_assessment.md"
RECOMMENDATION = DOC / "v0_16w_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16w.md"


@dataclass
class Endpoint:
    objective_arm: str
    replicate: int
    edges: frozenset[Tuple[int, int]]
    row: Dict[str, Any]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v16s", "frozen_event_histories", v16v.v16s.EVENT_LOG),
        ("v16s", "frozen_dependency_edges", v16v.v16s.EDGE_LOG),
        ("v16v", "global_feasibility_gate", v16v.GATE_EVALUATION),
        ("v16v", "global_feasibility_report", v16v.REPORT),
        ("v16v", "global_constraint_preregistration", v16v.PRE_REGISTRATION),
        ("v16v", "global_constraint_source_chain", v16v.SOURCE_CHAIN),
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
        "gate": "v16w_global_null_qualification_gate",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_global_null_procedure_qualification",
        "source_history_count": 6,
        "source_arm": v16v.v16s.PRIMARY_ARM,
        "null_family": NULL_FAMILY,
        "constraints": "frozen_v16v_global_edge_slot_b_matching",
        "primary_objective": "minimize_retained_source_edges_then_edge_keyed_random_tie_break",
        "sensitivity_objective": "edge_keyed_random_linear_priority_without_source_retention_term",
        "lexicographic_jitter_budget": LEXICOGRAPHIC_JITTER_BUDGET,
        "primary_replicates_per_source": PRIMARY_REPLICATES,
        "sensitivity_replicates_per_source": SENSITIVITY_REPLICATES,
        "check_replicates": list(CHECK_REPLICATES),
        "role_relabel_seeds": list(RELABEL_SEEDS),
        "minimum_unique_fraction": MIN_UNIQUE_FRACTION,
        "minimum_median_pairwise_change": MIN_MEDIAN_PAIRWISE_CHANGE,
        "minimum_candidate_union_coverage": MIN_CANDIDATE_UNION_COVERAGE,
        "minimum_effective_edge_support_ratio": MIN_EFFECTIVE_EDGE_SUPPORT_RATIO,
        "maximum_nonforced_edge_inclusion_rate": MAX_NONFORCED_EDGE_INCLUSION_RATE,
        "maximum_batch_center_range_ratio": MAX_BATCH_CENTER_RANGE_RATIO,
        "maximum_objective_center_range_ratio": MAX_OBJECTIVE_CENTER_RANGE_RATIO,
        "minimum_changed_edge_fraction": MIN_CHANGED_EDGE_FRACTION,
        "center_features": list(CENTER_FEATURES),
        "exact_replay_required": True,
        "candidate_column_order_covariance_required": True,
        "semantic_role_relabel_covariance_required": True,
        "all_source_dags_must_pass": True,
        "source_spectrum_computation_allowed": False,
        "observed_effect_computation_allowed": False,
        "local_switch_construction_allowed": False,
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
        "null_family": NULL_FAMILY,
        "primary_replicates_per_source": PRIMARY_REPLICATES,
        "sensitivity_replicates_per_source": SENSITIVITY_REPLICATES,
        "check_replicates": ";".join(str(value) for value in CHECK_REPLICATES),
        "role_relabel_seeds": ";".join(str(value) for value in RELABEL_SEEDS),
        "minimum_unique_fraction": MIN_UNIQUE_FRACTION,
        "minimum_median_pairwise_change": MIN_MEDIAN_PAIRWISE_CHANGE,
        "minimum_candidate_union_coverage": MIN_CANDIDATE_UNION_COVERAGE,
        "minimum_effective_edge_support_ratio": MIN_EFFECTIVE_EDGE_SUPPORT_RATIO,
        "maximum_nonforced_edge_inclusion_rate": MAX_NONFORCED_EDGE_INCLUSION_RATE,
        "maximum_batch_center_range_ratio": MAX_BATCH_CENTER_RANGE_RATIO,
        "maximum_objective_center_range_ratio": MAX_OBJECTIVE_CENTER_RANGE_RATIO,
        "lexicographic_jitter_budget": LEXICOGRAPHIC_JITTER_BUDGET,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
        "local_switch_construction_allowed": 0,
    }


def prepare() -> None:
    v16v.verify_outputs()
    overall = next(
        row["status"] for row in v16i.read_csv(v16v.GATE_EVALUATION)
        if row["gate"] == "v16v_overall"
    )
    if overall != "v16v_independent_global_null_family_feasible_and_diverse":
        raise ValueError("v16w requires the successful frozen v16v gate")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v16w] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    rows = v16i.read_csv(PRE_REGISTRATION)
    expected = {key: str(value) for key, value in preregistration_row().items()}
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v16w preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v16w source chain changed")


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    runs = []
    for source, metadata in v16v.load_runs():
        runs.append((v16i.RunDAG(
            stage="v16w",
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
        raise ValueError("v16w requires six frozen source histories")
    return runs


def unit_weight(*parts: Any) -> float:
    payload = "|".join(str(part) for part in parts).encode("utf-8")
    value = int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")
    return (value + 0.5) / float(1 << 64)


def objective_weights(
    dag: v16i.RunDAG,
    model: v16v.MatchingModel,
    objective_arm: str,
    replicate: int,
) -> np.ndarray:
    random_weights = np.fromiter(
        (
            unit_weight("v16w", objective_arm, *dag.key, replicate, parent, child)
            for parent, child in model.candidates
        ),
        dtype=float,
        count=len(model.candidates),
    )
    if objective_arm == PRIMARY_ARM:
        source_mask = np.fromiter(
            (1.0 if edge in model.source_edges else 0.0 for edge in model.candidates),
            dtype=float,
            count=len(model.candidates),
        )
        tie_scale = LEXICOGRAPHIC_JITTER_BUDGET / model.edge_count
        return source_mask + tie_scale * random_weights
    if objective_arm == SENSITIVITY_ARM:
        return random_weights
    raise ValueError(f"unknown objective arm {objective_arm}")


def endpoint_features(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    model: v16v.MatchingModel,
    edges: frozenset[Tuple[int, int]],
) -> Dict[str, float]:
    edge_count = len(edges)
    if edge_count == 0:
        return {feature: math.nan for feature in CENTER_FEATURES[:-1]}
    source_edge_fraction = len(edges & model.source_edges) / edge_count
    normalized_mean_parent_lag = sum(child - parent for parent, child in edges) / (
        edge_count * len(dag.predecessors)
    )
    mean_depth_gap = sum(dag.depths[child] - dag.depths[parent] for parent, child in edges) / edge_count
    concrete_conflict_fraction = sum(
        bool(v16n.conflict_channels(metadata[parent], metadata[child]))
        for parent, child in edges
    ) / edge_count

    bucket_candidates: Dict[Tuple[int, v16v.SlotClass], List[int]] = defaultdict(list)
    for parent, child in model.candidates:
        bucket_candidates[(child, v16v.slot_class(parent, child, dag.depths, metadata))].append(parent)
    rank_fraction: Dict[Tuple[int, int], float] = {}
    for (child, _), parents in bucket_candidates.items():
        ordered = sorted(parents)
        denominator = max(1, len(ordered) - 1)
        for rank, parent in enumerate(ordered):
            rank_fraction[(parent, child)] = rank / denominator
    mean_candidate_rank_fraction = sum(rank_fraction[edge] for edge in edges) / edge_count
    return {
        "source_edge_fraction": source_edge_fraction,
        "normalized_mean_parent_lag": normalized_mean_parent_lag,
        "mean_depth_gap": mean_depth_gap,
        "concrete_conflict_fraction": concrete_conflict_fraction,
        "mean_candidate_rank_fraction": mean_candidate_rank_fraction,
    }


def solve_endpoint(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    model: v16v.MatchingModel,
    objective_arm: str,
    replicate: int,
    *,
    column_order: Sequence[int] | None = None,
    check_kind: str = "primary",
) -> Endpoint:
    weights = objective_weights(dag, model, objective_arm, replicate)
    if column_order is None:
        order = np.arange(len(model.candidates), dtype=int)
    else:
        order = np.asarray(column_order, dtype=int)
        if sorted(order.tolist()) != list(range(len(model.candidates))):
            raise ValueError("column order must be a full permutation")
    started = time.monotonic()
    result = linprog(
        weights[order],
        A_eq=model.constraint_matrix[:, order],
        b_eq=model.demands,
        bounds=(0.0, 1.0),
        method="highs",
        options={"time_limit": SOLVER_TIME_LIMIT_SECONDS, "presolve": True},
    )
    elapsed = time.monotonic() - started
    base = {
        **dag.prefix,
        "null_family": NULL_FAMILY,
        "objective_arm": objective_arm,
        "replicate": replicate,
        "check_kind": check_kind,
        "objective_seed": v16i.stable_seed("v16w", objective_arm, *dag.key, replicate),
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
        return Endpoint(objective_arm, replicate, frozenset(), {
            **base,
            "integrality_error": math.nan,
            "equality_residual": math.nan,
            "selected_edge_count": 0,
            "changed_edge_fraction": 0.0,
            "source_edge_fraction": math.nan,
            "normalized_mean_parent_lag": math.nan,
            "mean_depth_gap": math.nan,
            "concrete_conflict_fraction": math.nan,
            "mean_candidate_rank_fraction": math.nan,
            "mean_pairwise_changed_fraction": math.nan,
            "structure_pass": 0,
            "per_child_slot_signature_pass": 0,
            "endpoint_integrity_pass": 0,
            "endpoint_edge_sha256": "",
        })

    values_in_order = np.rint(np.asarray(result.x, dtype=float))
    canonical_values = np.zeros(len(model.candidates), dtype=float)
    canonical_values[order] = values_in_order
    raw_values = np.zeros(len(model.candidates), dtype=float)
    raw_values[order] = np.asarray(result.x, dtype=float)
    integrality_error = float(np.max(np.abs(raw_values - canonical_values), initial=0.0))
    equality_residual = float(np.max(
        np.abs(model.constraint_matrix @ canonical_values - model.demands), initial=0.0
    ))
    edges = frozenset(
        model.candidates[index]
        for index, selected in enumerate(canonical_values)
        if selected > 0.5
    )
    predecessors: List[List[int]] = [[] for _ in dag.predecessors]
    for parent, child in edges:
        predecessors[child].append(parent)
    rewired = tuple(tuple(sorted(parents)) for parents in predecessors)
    structure = v16v.v16t.final_structure_audit(dag, metadata, rewired)
    slot_pass = v16v.slot_signature(rewired, dag.depths, metadata) == v16v.slot_signature(
        dag.predecessors, dag.depths, metadata
    )
    integrity = all((
        result.success,
        integrality_error <= INTEGRALITY_TOLERANCE,
        equality_residual <= EQUALITY_TOLERANCE,
        int(structure["structure_pass"]),
        slot_pass,
        len(edges) == model.edge_count,
    ))
    features = endpoint_features(dag, metadata, model, edges)
    digest = hashlib.sha256(
        json.dumps(sorted(edges), separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return Endpoint(objective_arm, replicate, edges, {
        **base,
        "integrality_error": integrality_error,
        "equality_residual": equality_residual,
        "selected_edge_count": len(edges),
        "changed_edge_fraction": float(structure["changed_edge_fraction"]),
        **features,
        "mean_pairwise_changed_fraction": math.nan,
        "structure_pass": int(structure["structure_pass"]),
        "per_child_slot_signature_pass": int(slot_pass),
        "endpoint_integrity_pass": int(integrity),
        "endpoint_edge_sha256": digest,
    })


def pairwise_rows(
    dag: v16i.RunDAG,
    endpoints: Sequence[Endpoint],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    by_replicate: Dict[int, List[float]] = defaultdict(list)
    edge_count = sum(len(parents) for parents in dag.predecessors)
    for left, right in combinations(endpoints, 2):
        intersection = len(left.edges & right.edges)
        union = len(left.edges | right.edges)
        changed_fraction = 1.0 - intersection / edge_count
        jaccard = intersection / union if union else 1.0
        by_replicate[left.replicate].append(changed_fraction)
        by_replicate[right.replicate].append(changed_fraction)
        rows.append({
            **dag.prefix,
            "objective_arm": left.objective_arm,
            "left_replicate": left.replicate,
            "right_replicate": right.replicate,
            "shared_edge_count": intersection,
            "edge_union_count": union,
            "pairwise_changed_edge_fraction": changed_fraction,
            "pairwise_edge_jaccard": jaccard,
        })
    for endpoint in endpoints:
        endpoint.row["mean_pairwise_changed_fraction"] = (
            sum(by_replicate[endpoint.replicate]) / len(by_replicate[endpoint.replicate])
        )
    return rows


def nonforced_candidates(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    model: v16v.MatchingModel,
) -> frozenset[Tuple[int, int]]:
    demand: Counter[Tuple[int, v16v.SlotClass]] = Counter()
    for child, parents in enumerate(dag.predecessors):
        demand.update(
            (child, v16v.slot_class(parent, child, dag.depths, metadata))
            for parent in parents
        )
    support: Counter[Tuple[int, v16v.SlotClass]] = Counter(
        (child, v16v.slot_class(parent, child, dag.depths, metadata))
        for parent, child in model.candidates
    )
    return frozenset(
        edge for edge in model.candidates
        if support[(edge[1], v16v.slot_class(edge[0], edge[1], dag.depths, metadata))]
        > demand[(edge[1], v16v.slot_class(edge[0], edge[1], dag.depths, metadata))]
    )


def ensemble_summary(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    model: v16v.MatchingModel,
    endpoints: Sequence[Endpoint],
) -> Dict[str, Any]:
    counts = Counter(edge for endpoint in endpoints for edge in endpoint.edges)
    selected_total = sum(counts.values())
    probabilities = [count / selected_total for count in counts.values()] if selected_total else []
    entropy = -sum(value * math.log(value) for value in probabilities if value > 0.0)
    effective_support_ratio = math.exp(entropy) / len(model.candidates) if probabilities else 0.0
    nonforced = nonforced_candidates(dag, metadata, model)
    maximum_inclusion = max(
        (counts[edge] / len(endpoints) for edge in nonforced), default=0.0
    )
    pairwise = [
        1.0 - len(left.edges & right.edges) / model.edge_count
        for left, right in combinations(endpoints, 2)
    ]
    unique_count = len({endpoint.row["endpoint_edge_sha256"] for endpoint in endpoints})
    return {
        "successful_endpoints": sum(int(endpoint.row["endpoint_integrity_pass"]) for endpoint in endpoints),
        "endpoint_count": len(endpoints),
        "unique_endpoint_count": unique_count,
        "unique_endpoint_fraction": unique_count / len(endpoints),
        "minimum_source_changed_edge_fraction": min(float(endpoint.row["changed_edge_fraction"]) for endpoint in endpoints),
        "median_pairwise_changed_edge_fraction": median(pairwise),
        "minimum_pairwise_changed_edge_fraction": min(pairwise),
        "candidate_edge_union_count": len(counts),
        "candidate_edge_union_coverage": len(counts) / len(model.candidates),
        "effective_edge_support_ratio": effective_support_ratio,
        "maximum_nonforced_edge_inclusion_rate": maximum_inclusion,
    }


def range_ratio(left: Sequence[float], right: Sequence[float]) -> Tuple[float, float, float, float]:
    left_center = median(left)
    right_center = median(right)
    combined = [*left, *right]
    span = max(combined) - min(combined)
    shift = abs(left_center - right_center)
    ratio = 0.0 if span <= 1e-15 and shift <= 1e-15 else shift / max(span, 1e-15)
    return left_center, right_center, shift, ratio


def batch_center_rows(dag: v16i.RunDAG, endpoints: Sequence[Endpoint]) -> List[Dict[str, Any]]:
    midpoint = len(endpoints) // 2
    rows = []
    for feature in CENTER_FEATURES:
        left = [float(endpoint.row[feature]) for endpoint in endpoints[:midpoint]]
        right = [float(endpoint.row[feature]) for endpoint in endpoints[midpoint:]]
        first, second, shift, ratio = range_ratio(left, right)
        rows.append({
            **dag.prefix,
            "feature": feature,
            "first_batch_count": len(left),
            "second_batch_count": len(right),
            "first_batch_median": first,
            "second_batch_median": second,
            "absolute_center_shift": shift,
            "combined_range": max([*left, *right]) - min([*left, *right]),
            "center_shift_range_ratio": ratio,
            "maximum_allowed_ratio": MAX_BATCH_CENTER_RANGE_RATIO,
            "center_stability_pass": int(ratio <= MAX_BATCH_CENTER_RANGE_RATIO),
        })
    return rows


def objective_sensitivity_rows(
    dag: v16i.RunDAG,
    primary: Sequence[Endpoint],
    sensitivity: Sequence[Endpoint],
) -> List[Dict[str, Any]]:
    rows = []
    for feature in CENTER_FEATURES:
        left = [float(endpoint.row[feature]) for endpoint in primary]
        right = [float(endpoint.row[feature]) for endpoint in sensitivity]
        primary_center, sensitivity_center, shift, ratio = range_ratio(left, right)
        rows.append({
            **dag.prefix,
            "feature": feature,
            "primary_objective": PRIMARY_ARM,
            "sensitivity_objective": SENSITIVITY_ARM,
            "primary_count": len(left),
            "sensitivity_count": len(right),
            "primary_median": primary_center,
            "sensitivity_median": sensitivity_center,
            "absolute_center_shift": shift,
            "combined_range": max([*left, *right]) - min([*left, *right]),
            "center_shift_range_ratio": ratio,
            "maximum_allowed_ratio": MAX_OBJECTIVE_CENTER_RANGE_RATIO,
            "objective_sensitivity_pass": int(ratio <= MAX_OBJECTIVE_CENTER_RANGE_RATIO),
        })
    return rows


def permuted_columns(dag: v16i.RunDAG, replicate: int, count: int) -> List[int]:
    order = list(range(count))
    random.Random(v16i.stable_seed("v16w", "column_order", *dag.key, replicate)).shuffle(order)
    return order


def relabel_metadata(
    metadata: Sequence[Mapping[str, Any]],
    seed: int,
) -> Tuple[Dict[str, Any], ...]:
    families = sorted({str(row["family"]) for row in metadata})
    namespaces = sorted({
        v16n.resource_namespace(resource)
        for row in metadata
        for resource in (*row["reads"], *row["writes"])
    })
    family_targets = [f"family_{index}" for index in range(len(families))]
    namespace_targets = [f"namespace_{index}" for index in range(len(namespaces))]
    rng = random.Random(seed)
    rng.shuffle(family_targets)
    rng.shuffle(namespace_targets)
    family_map = dict(zip(families, family_targets))
    namespace_map = dict(zip(namespaces, namespace_targets))

    resources = sorted({
        resource
        for row in metadata
        for resource in (*row["reads"], *row["writes"])
    })
    resource_map: Dict[str, str] = {}
    for resource in resources:
        namespace = v16n.resource_namespace(resource)
        digest = hashlib.sha256(f"{seed}|{resource}".encode("utf-8")).hexdigest()[:20]
        resource_map[resource] = f"{namespace_map[namespace]}:{digest}"
    return tuple({
        **dict(row),
        "family": family_map[str(row["family"])],
        "reads": frozenset(resource_map[value] for value in row["reads"]),
        "writes": frozenset(resource_map[value] for value in row["writes"]),
    } for row in metadata)


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


def markdown_table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")
    return lines


def build_report(
    summaries: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    objective_rows: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    failed_objective = [
        row for row in objective_rows if not int(row["objective_sensitivity_pass"])
    ]
    lines = [
        "# v16w global-null qualification gate",
        "",
        f"Status: `{overall}`.",
        "",
        "## Frozen design",
        "",
        f"The six v16s source DAGs and v16v edge-slot constraints remain fixed. Each source receives `{PRIMARY_REPLICATES}` source-retention-minimizing endpoints and `{SENSITIVITY_REPLICATES}` pure random-priority endpoints. The script computes no source spectrum and no observed-effect statistic.",
        "",
        "The primary tie-break is keyed by the candidate edge rather than candidate-column order. Its total possible contribution is below `0.25`, so a one-edge source-retention difference remains lexicographically dominant with margin above `0.75`.",
        "",
        "## Source qualification summary",
        "",
        *markdown_table(summaries, (
            "growth_seed", "run_offset", "primary_unique_fraction",
            "primary_median_pairwise_change", "primary_candidate_union_coverage",
            "primary_effective_edge_support_ratio", "batch_center_pass",
            "objective_sensitivity_pass", "source_qualification_pass",
        )),
        "",
        "## Gate evaluation",
        "",
        *markdown_table(gates, ("gate", "status", "observed", "required", "decision")),
        "",
        "## Objective sensitivity",
        "",
    ]
    if failed_objective:
        lines.extend([
            "The following null-only feature comparisons exceeded the frozen range-ratio threshold:",
            "",
            *markdown_table(failed_objective, (
                "growth_seed", "run_offset", "feature", "primary_median",
                "sensitivity_median", "center_shift_range_ratio",
                "maximum_allowed_ratio",
            )),
        ])
    else:
        lines.append("All frozen objective-sensitivity comparisons passed.")
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "A pass qualifies only replay, finite endpoint diversity, representation covariance, finite batch-center stability, and limited objective robustness for this algorithmic family. It does not establish uniform sampling, mixing, stationarity, a canonical probability measure, or representativeness.",
        "",
        "A failure is also informative: it means the feasible global family is materially selected by an arbitrary solver objective or another implementation choice. Do not run an observed-effect comparison until the failed qualification layer is repaired and frozen effect-blind.",
        "",
        "V16w establishes no energy, temperature, invariant, dimension, manifold, Lorentz symmetry, spacetime, particle, entanglement, continuum, or physical law.",
        "",
    ])
    return "\n".join(lines)


def build_next_direction(overall: str) -> str:
    if overall == "v16w_global_null_procedure_qualified_effect_blind":
        decision = (
            "Freeze the qualified global procedure and preregister one fresh-history independent-null effect holdout. Generate the histories only after the effect gate is frozen. Keep action-density instrumentation downstream."
        )
    elif overall == "v16w_global_null_objective_dependent_not_qualified":
        decision = (
            "Do not compute the v16s effect under this family. The next gate must define an explicit stochastic measure over feasible b-matchings, preferably a maximum-entropy or otherwise auditable distribution, and qualify that sampler effect-blind."
        )
    else:
        decision = (
            "Do not compute an observed effect. Repair the smallest failed replay, representation, diversity, or finite-center layer without inspecting source spectra."
        )
    return "\n".join([
        "# v16w interpretation and next direction",
        "",
        f"Status: `{overall}`.",
        "",
        "## Decision",
        "",
        decision,
        "",
        "## Units of change",
        "",
        "The action-density/emergent-energy hypothesis remains promising but separate. It must not be used to interpret an event-DAG contrast while the global null distribution remains unqualified.",
        "",
    ])


def run() -> None:
    verify_frozen_sources()
    runs = load_runs()
    calls = implementation_call_counts()
    endpoint_rows: List[Dict[str, Any]] = []
    pairwise_output: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    relabel_rows: List[Dict[str, Any]] = []
    batch_rows: List[Dict[str, Any]] = []
    objective_rows: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []

    for source_index, (dag, metadata) in enumerate(runs, start=1):
        model = v16v.build_matching_model(dag, metadata)
        primary = [
            solve_endpoint(dag, metadata, model, PRIMARY_ARM, replicate)
            for replicate in range(PRIMARY_REPLICATES)
        ]
        sensitivity = [
            solve_endpoint(dag, metadata, model, SENSITIVITY_ARM, replicate)
            for replicate in range(SENSITIVITY_REPLICATES)
        ]
        pairwise_output.extend(pairwise_rows(dag, primary))
        pairwise_output.extend(pairwise_rows(dag, sensitivity))
        endpoint_rows.extend(endpoint.row for endpoint in (*primary, *sensitivity))

        primary_by_replicate = {endpoint.replicate: endpoint for endpoint in primary}
        for replicate in CHECK_REPLICATES:
            original = primary_by_replicate[replicate]
            replay = solve_endpoint(
                dag, metadata, model, PRIMARY_ARM, replicate, check_kind="replay"
            )
            reordered = solve_endpoint(
                dag,
                metadata,
                model,
                PRIMARY_ARM,
                replicate,
                column_order=permuted_columns(dag, replicate, len(model.candidates)),
                check_kind="candidate_column_permutation",
            )
            replay_rows.append({
                **dag.prefix,
                "replicate": replicate,
                "source_endpoint_sha256": original.row["endpoint_edge_sha256"],
                "replay_endpoint_sha256": replay.row["endpoint_edge_sha256"],
                "permuted_column_endpoint_sha256": reordered.row["endpoint_edge_sha256"],
                "replay_integrity_pass": int(replay.row["endpoint_integrity_pass"]),
                "column_permutation_integrity_pass": int(reordered.row["endpoint_integrity_pass"]),
                "exact_replay_pass": int(original.edges == replay.edges),
                "candidate_column_order_covariance_pass": int(original.edges == reordered.edges),
            })

        reference = primary_by_replicate[0]
        reference_support_profile = sorted(
            (
                int(row["child_event_id"]),
                int(row["dyadic_age_bin"]),
                row["depth_relation"],
                int(row["required_slot_count"]),
                int(row["candidate_parent_count"]),
            )
            for row in model.support_rows
        )
        for seed in RELABEL_SEEDS:
            relabeled_metadata = relabel_metadata(metadata, seed)
            relabeled_model = v16v.build_matching_model(dag, relabeled_metadata)
            relabeled_endpoint = solve_endpoint(
                dag,
                relabeled_metadata,
                relabeled_model,
                PRIMARY_ARM,
                0,
                check_kind="semantic_role_relabel",
            )
            relabeled_profile = sorted(
                (
                    int(row["child_event_id"]),
                    int(row["dyadic_age_bin"]),
                    row["depth_relation"],
                    int(row["required_slot_count"]),
                    int(row["candidate_parent_count"]),
                )
                for row in relabeled_model.support_rows
            )
            candidate_pass = model.candidates == relabeled_model.candidates
            support_pass = reference_support_profile == relabeled_profile
            relabel_rows.append({
                **dag.prefix,
                "relabel_seed": seed,
                "candidate_edge_count": len(relabeled_model.candidates),
                "source_endpoint_sha256": reference.row["endpoint_edge_sha256"],
                "relabeled_endpoint_sha256": relabeled_endpoint.row["endpoint_edge_sha256"],
                "candidate_set_covariance_pass": int(candidate_pass),
                "support_profile_covariance_pass": int(support_pass),
                "relabeled_endpoint_integrity_pass": int(relabeled_endpoint.row["endpoint_integrity_pass"]),
                "semantic_role_relabel_endpoint_covariance_pass": int(reference.edges == relabeled_endpoint.edges),
                "role_relabel_pass": int(
                    candidate_pass
                    and support_pass
                    and int(relabeled_endpoint.row["endpoint_integrity_pass"])
                    and reference.edges == relabeled_endpoint.edges
                ),
            })

        primary_summary = ensemble_summary(dag, metadata, model, primary)
        sensitivity_summary = ensemble_summary(dag, metadata, model, sensitivity)
        source_batch_rows = batch_center_rows(dag, primary)
        source_objective_rows = objective_sensitivity_rows(dag, primary, sensitivity)
        batch_rows.extend(source_batch_rows)
        objective_rows.extend(source_objective_rows)
        source_replay = [row for row in replay_rows if int(row["growth_seed"]) == dag.growth_seed and int(row["run_offset"]) == dag.run_offset]
        source_relabel = [row for row in relabel_rows if int(row["growth_seed"]) == dag.growth_seed and int(row["run_offset"]) == dag.run_offset]

        integrity_pass = (
            primary_summary["successful_endpoints"] == PRIMARY_REPLICATES
            and sensitivity_summary["successful_endpoints"] == SENSITIVITY_REPLICATES
        )
        replay_pass = all(
            int(row["exact_replay_pass"])
            and int(row["candidate_column_order_covariance_pass"])
            for row in source_replay
        )
        relabel_pass = all(int(row["role_relabel_pass"]) for row in source_relabel)
        diversity_pass = all((
            primary_summary["unique_endpoint_fraction"] >= MIN_UNIQUE_FRACTION,
            primary_summary["minimum_source_changed_edge_fraction"] >= MIN_CHANGED_EDGE_FRACTION,
            primary_summary["median_pairwise_changed_edge_fraction"] >= MIN_MEDIAN_PAIRWISE_CHANGE,
            primary_summary["candidate_edge_union_coverage"] >= MIN_CANDIDATE_UNION_COVERAGE,
            primary_summary["effective_edge_support_ratio"] >= MIN_EFFECTIVE_EDGE_SUPPORT_RATIO,
            primary_summary["maximum_nonforced_edge_inclusion_rate"] <= MAX_NONFORCED_EDGE_INCLUSION_RATE,
        ))
        center_pass = all(int(row["center_stability_pass"]) for row in source_batch_rows)
        objective_pass = all(int(row["objective_sensitivity_pass"]) for row in source_objective_rows)
        source_pass = all((
            integrity_pass,
            replay_pass,
            relabel_pass,
            diversity_pass,
            center_pass,
            objective_pass,
        ))
        summaries.append({
            **dag.prefix,
            "candidate_edge_count": len(model.candidates),
            "source_edge_count": model.edge_count,
            "primary_successful_endpoints": primary_summary["successful_endpoints"],
            "primary_unique_fraction": primary_summary["unique_endpoint_fraction"],
            "primary_minimum_source_change": primary_summary["minimum_source_changed_edge_fraction"],
            "primary_median_pairwise_change": primary_summary["median_pairwise_changed_edge_fraction"],
            "primary_minimum_pairwise_change": primary_summary["minimum_pairwise_changed_edge_fraction"],
            "primary_candidate_union_coverage": primary_summary["candidate_edge_union_coverage"],
            "primary_effective_edge_support_ratio": primary_summary["effective_edge_support_ratio"],
            "primary_max_nonforced_edge_inclusion_rate": primary_summary["maximum_nonforced_edge_inclusion_rate"],
            "sensitivity_successful_endpoints": sensitivity_summary["successful_endpoints"],
            "sensitivity_unique_fraction": sensitivity_summary["unique_endpoint_fraction"],
            "integrity_pass": int(integrity_pass),
            "replay_and_column_order_pass": int(replay_pass),
            "role_relabel_pass": int(relabel_pass),
            "endpoint_diversity_pass": int(diversity_pass),
            "batch_center_pass": int(center_pass),
            "objective_sensitivity_pass": int(objective_pass),
            "source_qualification_pass": int(source_pass),
        })
        print(
            f"[v16w] sources={source_index}/{len(runs)} "
            f"unique={primary_summary['unique_endpoint_fraction']:.3f} "
            f"pair={primary_summary['median_pairwise_changed_edge_fraction']:.3f} "
            f"center={int(center_pass)} objective={int(objective_pass)}"
        )

    expected_endpoints = 6 * (PRIMARY_REPLICATES + SENSITIVITY_REPLICATES)
    integrity_pass = len(endpoint_rows) == expected_endpoints and all(int(row["integrity_pass"]) for row in summaries)
    replay_pass = len(replay_rows) == 6 * len(CHECK_REPLICATES) and all(
        int(row["exact_replay_pass"]) and int(row["candidate_column_order_covariance_pass"])
        for row in replay_rows
    )
    relabel_pass = len(relabel_rows) == 6 * len(RELABEL_SEEDS) and all(
        int(row["role_relabel_pass"]) for row in relabel_rows
    )
    diversity_pass = all(int(row["endpoint_diversity_pass"]) for row in summaries)
    center_pass = all(int(row["batch_center_pass"]) for row in summaries)
    objective_pass = all(int(row["objective_sensitivity_pass"]) for row in summaries)
    exclusion_pass = calls == {"local_switch_calls": 0, "spectrum_calls": 0, "effect_metric_calls": 0}

    if not integrity_pass or not replay_pass or not relabel_pass or not exclusion_pass:
        overall = "v16w_global_null_qualification_instrumentation_failed"
    elif not diversity_pass:
        overall = "v16w_global_null_endpoint_diversity_not_qualified"
    elif not center_pass:
        overall = "v16w_global_null_batch_center_unstable"
    elif not objective_pass:
        overall = "v16w_global_null_objective_dependent_not_qualified"
    else:
        overall = "v16w_global_null_procedure_qualified_effect_blind"

    gates = [
        {
            "gate": "endpoint_integrity_and_effect_exclusion",
            "status": "pass" if integrity_pass and exclusion_pass else "fail",
            "observed": f"endpoints={sum(int(row['endpoint_integrity_pass']) for row in endpoint_rows)}/{len(endpoint_rows)};switch={calls['local_switch_calls']};spectrum={calls['spectrum_calls']};effect={calls['effect_metric_calls']}",
            "required": f"{expected_endpoints}/{expected_endpoints};0;0;0",
            "decision": "continue" if integrity_pass and exclusion_pass else "instrumentation_failed",
        },
        {
            "gate": "replay_and_representation_covariance",
            "status": "pass" if replay_pass and relabel_pass else "fail",
            "observed": f"replay_order={sum(int(row['exact_replay_pass']) and int(row['candidate_column_order_covariance_pass']) for row in replay_rows)}/{len(replay_rows)};relabel={sum(int(row['role_relabel_pass']) for row in relabel_rows)}/{len(relabel_rows)}",
            "required": f"{len(replay_rows)}/{len(replay_rows)};{len(relabel_rows)}/{len(relabel_rows)}",
            "decision": "continue" if replay_pass and relabel_pass else "repair_representation_dependence",
        },
        {
            "gate": "primary_endpoint_diversity",
            "status": "pass" if diversity_pass else "fail",
            "observed": f"sources={sum(int(row['endpoint_diversity_pass']) for row in summaries)}/6",
            "required": "6/6",
            "decision": "continue" if diversity_pass else "family_collapsed_or_concentrated",
        },
        {
            "gate": "finite_batch_center_stability",
            "status": "pass" if center_pass else "fail",
            "observed": f"features={sum(int(row['center_stability_pass']) for row in batch_rows)}/{len(batch_rows)}",
            "required": f"{len(batch_rows)}/{len(batch_rows)}",
            "decision": "continue" if center_pass else "increase_or_revise_sampler",
        },
        {
            "gate": "objective_sensitivity",
            "status": "pass" if objective_pass else "fail",
            "observed": f"features={sum(int(row['objective_sensitivity_pass']) for row in objective_rows)}/{len(objective_rows)}",
            "required": f"{len(objective_rows)}/{len(objective_rows)}",
            "decision": "qualified_limited_objective_robustness" if objective_pass else "define_explicit_stochastic_measure",
        },
        {
            "gate": "v16w_overall",
            "status": overall,
            "observed": f"integrity={int(integrity_pass)};replay={int(replay_pass)};relabel={int(relabel_pass)};diversity={int(diversity_pass)};center={int(center_pass)};objective={int(objective_pass)};exclusion={int(exclusion_pass)}",
            "required": "1;1;1;1;1;1;1",
            "decision": overall,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "The v16w primary global procedure is exactly replayable and invariant to tested candidate-column and semantic-role relabel representations.",
            "status": "supported" if replay_pass and relabel_pass else "not_supported",
            "evidence": "v16w_replay_and_order_audit.csv;v16w_role_relabel_audit.csv",
            "scope_limit": "tested finite sources, keyed objectives, four endpoint checks and four semantic relabels per source",
        },
        {
            "claim_id": "C2",
            "claim": "The v16w primary global procedure produces a diverse finite endpoint ensemble with stable half-batch centers.",
            "status": "supported" if diversity_pass and center_pass else "not_supported",
            "evidence": "v16w_source_qualification_summary.csv;v16w_batch_center_stability.csv",
            "scope_limit": "32 endpoints per each of six frozen source DAGs",
        },
        {
            "claim_id": "C3",
            "claim": "The global endpoint family is insensitive to replacing source-retention minimization with pure random edge priority.",
            "status": "supported" if objective_pass else "not_supported",
            "evidence": "v16w_objective_sensitivity.csv",
            "scope_limit": "six null-only center features and the frozen range-ratio threshold",
        },
        {
            "claim_id": "C4",
            "claim": "The global null is a uniform, stationary, maximum-entropy or representative probability distribution.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "finite procedure qualification cannot establish these properties",
        },
        {
            "claim_id": "C5",
            "claim": "The v16s observed spectrum contrast survives the qualified global null.",
            "status": "not_evaluated",
            "evidence": "v16w_gate_evaluation.csv",
            "scope_limit": "source spectra and effect metrics were prohibited",
        },
        {
            "claim_id": "C6",
            "claim": "The result establishes physical energy, temperature, geometry or spacetime.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "effect-blind finite event-DAG procedure audit only",
        },
    ]

    v16i.write_csv(ENDPOINT_AUDIT, endpoint_rows)
    v16i.write_csv(PAIRWISE_DISTANCE, pairwise_output)
    v16i.write_csv(REPLAY_ORDER_AUDIT, replay_rows)
    v16i.write_csv(ROLE_RELABEL_AUDIT, relabel_rows)
    v16i.write_csv(BATCH_CENTER_STABILITY, batch_rows)
    v16i.write_csv(OBJECTIVE_SENSITIVITY, objective_rows)
    v16i.write_csv(SOURCE_SUMMARY, summaries)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    REPORT.write_text(build_report(summaries, gates, objective_rows, overall), encoding="utf-8")
    NEXT_DIRECTION.write_text(build_next_direction(overall), encoding="utf-8")
    RECOMMENDATION.write_text(
        "# Operativ anbefaling etter v16w\n\n"
        f"Status: `{overall}`.\n\n"
        + (
            "Frys prosedyren og kjor én fresh-history independent-null effect holdout.\n"
            if overall == "v16w_global_null_procedure_qualified_effect_blind"
            else "Ikke kjor source-effekten. Definer og kvalifiser en eksplisitt stokastisk fordeling over feasible globale matchinger.\n"
        ),
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.16w\n\n"
        f"Statusen er `{overall}`. Runden tester om den globale kontrollgeneratoren gir samme type svar ved gjentakelse, navnebytte, annen intern rekkefolge og en alternativ solver-prioritering. Den ser ikke paa hovedsignalet og er ikke et funn av fysikk.\n",
        encoding="utf-8",
    )
    print(f"[v16w] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    endpoints = v16i.read_csv(ENDPOINT_AUDIT)
    replay = v16i.read_csv(REPLAY_ORDER_AUDIT)
    relabel = v16i.read_csv(ROLE_RELABEL_AUDIT)
    summaries = v16i.read_csv(SOURCE_SUMMARY)
    gates = v16i.read_csv(GATE_EVALUATION)
    expected = 6 * (PRIMARY_REPLICATES + SENSITIVITY_REPLICATES)
    if len(endpoints) != expected or len(summaries) != 6:
        raise ValueError("v16w output row counts failed")
    if len(replay) != 6 * len(CHECK_REPLICATES) or len(relabel) != 6 * len(RELABEL_SEEDS):
        raise ValueError("v16w covariance audit row counts failed")
    if not all(int(row["endpoint_integrity_pass"]) for row in endpoints):
        raise ValueError("v16w endpoint integrity failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16w_overall")
    allowed = {
        "v16w_global_null_qualification_instrumentation_failed",
        "v16w_global_null_endpoint_diversity_not_qualified",
        "v16w_global_null_batch_center_unstable",
        "v16w_global_null_objective_dependent_not_qualified",
        "v16w_global_null_procedure_qualified_effect_blind",
    }
    if overall not in allowed:
        raise ValueError("v16w unknown overall status")
    exclusion = next(row for row in gates if row["gate"] == "endpoint_integrity_and_effect_exclusion")
    if "switch=0;spectrum=0;effect=0" not in exclusion["observed"]:
        raise ValueError("v16w effect exclusion failed")
    for path in (REPORT, NEXT_DIRECTION, RECOMMENDATION, NONSPECIALIST):
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"v16w missing report {path.name}")
    print(f"[v16w] output verification pass overall={overall}")


def self_test() -> None:
    predecessors = (
        (), (), (), (), (), (),
        (0, 1), (2, 3),
        (), (), (), (),
    )
    depths = tuple(v16i.recompute_depths(predecessors))
    dag = v16i.RunDAG(
        stage="v16w_test",
        target_nodes=12,
        growth_seed=1,
        run_offset=2,
        arm="test",
        run_seed=3,
        predecessors=predecessors,
        depths=depths,
        indegrees=tuple(len(parents) for parents in predecessors),
    )
    metadata = tuple({
        "family": "swap" if index % 2 else "token",
        "event_type": "test",
        "writes": frozenset({f"node:{index % 4}"}),
        "reads": frozenset({f"node:{(index + 1) % 4}"}),
    } for index in range(len(predecessors)))
    model = v16v.build_matching_model(dag, metadata)
    tie_scale = LEXICOGRAPHIC_JITTER_BUDGET / model.edge_count
    if model.edge_count * tie_scale >= 1.0:
        raise AssertionError("v16w lexicographic tie-break margin failed")
    original = solve_endpoint(dag, metadata, model, PRIMARY_ARM, 0)
    replay = solve_endpoint(dag, metadata, model, PRIMARY_ARM, 0, check_kind="replay")
    reordered = solve_endpoint(
        dag,
        metadata,
        model,
        PRIMARY_ARM,
        0,
        column_order=permuted_columns(dag, 0, len(model.candidates)),
        check_kind="candidate_column_permutation",
    )
    relabeled_metadata = relabel_metadata(metadata, RELABEL_SEEDS[0])
    relabeled_model = v16v.build_matching_model(dag, relabeled_metadata)
    relabeled = solve_endpoint(dag, relabeled_metadata, relabeled_model, PRIMARY_ARM, 0)
    if not all(int(item.row["endpoint_integrity_pass"]) for item in (original, replay, reordered, relabeled)):
        raise AssertionError("v16w synthetic endpoint integrity failed")
    if not (original.edges == replay.edges == reordered.edges == relabeled.edges):
        raise AssertionError("v16w synthetic covariance failed")
    if implementation_call_counts() != {
        "local_switch_calls": 0,
        "spectrum_calls": 0,
        "effect_metric_calls": 0,
    }:
        raise AssertionError("v16w effect exclusion audit failed")
    if spec_payload()["source_spectrum_computation_allowed"]:
        raise AssertionError("v16w source spectrum must be prohibited")
    print("[v16w] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16w effect-blind global-null qualification gate")
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
