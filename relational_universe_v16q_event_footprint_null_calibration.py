#!/usr/bin/env python3
"""v16q: effect-blind calibration of the event-footprint DAG null."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import random
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16j_interval_strict_null_gate as v16j
import relational_universe_v16k_fresh_strict_null_replication as v16k
import relational_universe_v16n_coarse_event_resource_null_calibration as v16n
import relational_universe_v16o_event_resource_reachability_audit as v16o
import relational_universe_v16p_event_footprint_reachability_audit as v16p


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

PRIMARY_REPLICATES = v16j.NULL_REPLICATES
PRIMARY_SWAP_MULTIPLIER = v16j.TARGET_ACCEPTED_SWAPS_PER_EDGE
LONGER_REPLICATES = v16k.LONGER_NULL_REPLICATES
LONGER_SWAP_MULTIPLIER = v16k.LONGER_TARGET_SWAP_MULTIPLIER
ATTEMPT_CEILING_LADDER = (60, 120, 240, 480)
MIN_CHANGED_EDGE_FRACTION = v16j.MIN_CHANGED_EDGE_FRACTION
MIN_UNIQUE_NULL_FRACTION = v16j.MIN_UNIQUE_NULL_FRACTION
NULL_FAMILY = "degree_depth_age_event_footprint_double_edge_swap"

SOURCE_CHAIN = DOC / "v16q_source_chain.csv"
PRE_REGISTRATION = DOC / "v16q_pre_registration.csv"
FOOTPRINT_SUPPORT = DOC / "v16q_footprint_support.csv"
CALIBRATION_AUDIT = DOC / "v16q_sampler_calibration_integrity.csv"
CEILING_SUMMARY = DOC / "v16q_attempt_ceiling_summary.csv"
QUALIFICATION = DOC / "v16q_sampler_qualification.csv"
GATE_EVALUATION = DOC / "v16q_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16q_claim_ledger.csv"
REPORT = DOC / "v16q_event_footprint_null_calibration.md"
RECOMMENDATION = DOC / "v0_16q_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16q.md"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = [
        ("v16n", "calibration_events", v16n.EVENT_LOG),
        ("v16n", "calibration_edges", v16n.EDGE_LOG),
        ("v16p", "footprint_definition", Path(v16p.__file__)),
        ("v16p", "reachability_summary", v16p.RUN_SUMMARY),
        ("v16p", "reachability_gate", v16p.GATE_EVALUATION),
    ]
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
        "gate": "v16q_event_footprint_null_calibration",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_sampler_calibration_only",
        "source": "six_frozen_v16n_calibration_dags",
        "null_family": NULL_FAMILY,
        "edge_footprint": [
            "parent_event_family",
            "parent_write_namespace_set",
            "child_event_family",
            "child_read_namespace_set",
        ],
        "concrete_resource_overlap_required": False,
        "preserves": [
            "event_count",
            "scheduler_order",
            "exact_per_event_indegree",
            "exact_per_event_outdegree",
            "exact_causal_depth_sequence",
            "global_dyadic_parent_age_bin_histogram",
            "global_event_footprint_histogram",
        ],
        "does_not_preserve": [
            "concrete_resource_identity",
            "actual_resource_conflict_for_every_null_edge",
            "exact_parent_age_per_edge",
            "per_child_age_bin_multiset",
            "per_child_footprint_multiset",
        ],
        "primary_replicates": PRIMARY_REPLICATES,
        "primary_swap_multiplier": PRIMARY_SWAP_MULTIPLIER,
        "longer_replicates": LONGER_REPLICATES,
        "longer_swap_multiplier": LONGER_SWAP_MULTIPLIER,
        "attempt_ceiling_ladder": list(ATTEMPT_CEILING_LADDER),
        "ceiling_selection": "lowest_ceiling_with_all_primary_and_longer_perturbations_valid",
        "min_changed_edge_fraction": MIN_CHANGED_EDGE_FRACTION,
        "min_unique_null_fraction": MIN_UNIQUE_NULL_FRACTION,
        "spectrum_computation_allowed": False,
    }


def spec_digest() -> str:
    raw = json.dumps(spec_payload(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def prepare() -> None:
    v16p.verify_outputs()
    gate = next(row for row in v16i.read_csv(v16p.GATE_EVALUATION) if row["gate"] == "v16p_overall")
    if gate["status"] != "v16p_event_footprint_static_support_promising":
        raise ValueError("v16q requires the frozen v16p promising-support result")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [{
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "script_sha256": file_sha256(SCRIPT),
        "source_chain_sha256": file_sha256(SOURCE_CHAIN),
        "source_run_count": len(v16n.assignments()),
        "primary_replicates": PRIMARY_REPLICATES,
        "primary_swap_multiplier": PRIMARY_SWAP_MULTIPLIER,
        "longer_replicates": LONGER_REPLICATES,
        "longer_swap_multiplier": LONGER_SWAP_MULTIPLIER,
        "attempt_ceiling_ladder": ";".join(str(value) for value in ATTEMPT_CEILING_LADDER),
        "min_changed_edge_fraction": MIN_CHANGED_EDGE_FRACTION,
        "min_unique_null_fraction": MIN_UNIQUE_NULL_FRACTION,
        "spectrum_computation_allowed": 0,
    }])
    print(f"[v16q] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1:
        raise ValueError("v16q preregistration row count failed")
    expected = {
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "script_sha256": file_sha256(SCRIPT),
        "source_chain_sha256": file_sha256(SOURCE_CHAIN),
        "source_run_count": str(len(v16n.assignments())),
        "primary_replicates": str(PRIMARY_REPLICATES),
        "primary_swap_multiplier": str(PRIMARY_SWAP_MULTIPLIER),
        "longer_replicates": str(LONGER_REPLICATES),
        "longer_swap_multiplier": str(LONGER_SWAP_MULTIPLIER),
        "attempt_ceiling_ladder": ";".join(str(value) for value in ATTEMPT_CEILING_LADDER),
        "min_changed_edge_fraction": str(MIN_CHANGED_EDGE_FRACTION),
        "min_unique_null_fraction": str(MIN_UNIQUE_NULL_FRACTION),
        "spectrum_computation_allowed": "0",
    }
    if rows[0] != expected:
        raise ValueError("v16q preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v16q source chain changed")


def footprint_signature(
    predecessors: Sequence[Sequence[int]],
    metadata: Sequence[Mapping[str, Any]],
) -> Tuple[Tuple[str, int], ...]:
    counts: Counter[str] = Counter()
    for child, parents in enumerate(predecessors):
        for parent in parents:
            counts[v16p.footprint_text(v16p.edge_footprint(parent, child, metadata))] += 1
    return tuple(sorted(counts.items()))


def footprint_rewire(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    seed: int,
    *,
    target_swap_multiplier: float,
    max_attempts_per_edge: int,
) -> Tuple[Tuple[Tuple[int, ...], ...], Dict[str, Any]]:
    rng = random.Random(seed)
    original = tuple(tuple(parents) for parents in dag.predecessors)
    predecessors: List[Set[int]] = [set(parents) for parents in original]
    edges = [(parent, child) for child, parents in enumerate(original) for parent in parents]
    edge_set = set(edges)
    original_edges = set(edges)
    edge_count = len(edges)
    footprints = [v16p.edge_footprint(parent, child, metadata) for parent, child in edges]
    buckets: Dict[v16p.Footprint, List[int]] = defaultdict(list)
    for index, footprint in enumerate(footprints):
        buckets[footprint].append(index)
    bucket_positions = [0] * edge_count
    for indices in buckets.values():
        for position, index in enumerate(indices):
            bucket_positions[index] = position
    eligible = tuple(index for indices in buckets.values() if len(indices) >= 2 for index in indices)
    target_swaps = max(1, math.ceil(edge_count * target_swap_multiplier))
    max_attempts = max(target_swaps, edge_count * max_attempts_per_edge)
    attempts = 0
    accepted = 0

    while attempts < max_attempts and eligible:
        attempts += 1
        first_index = eligible[rng.randrange(len(eligible))]
        bucket = buckets[footprints[first_index]]
        second_position = rng.randrange(len(bucket) - 1)
        first_position = bucket_positions[first_index]
        if second_position >= first_position:
            second_position += 1
        second_index = bucket[second_position]
        parent_a, child_b = edges[first_index]
        parent_c, child_d = edges[second_index]
        if parent_a == parent_c or child_b == child_d:
            continue
        new_first = (parent_a, child_d)
        new_second = (parent_c, child_b)
        if parent_a >= child_d or parent_c >= child_b:
            continue
        if new_first in edge_set or new_second in edge_set or new_first == new_second:
            continue
        if v16p.edge_footprint(*new_first, metadata) != footprints[first_index]:
            continue
        if v16p.edge_footprint(*new_second, metadata) != footprints[second_index]:
            continue
        old_bins = sorted((v16j.lag_bin(parent_a, child_b), v16j.lag_bin(parent_c, child_d)))
        new_bins = sorted((v16j.lag_bin(parent_a, child_d), v16j.lag_bin(parent_c, child_b)))
        if old_bins != new_bins:
            continue
        next_b = (predecessors[child_b] - {parent_a}) | {parent_c}
        next_d = (predecessors[child_d] - {parent_c}) | {parent_a}
        if (
            not next_b
            or not next_d
            or max(dag.depths[parent] for parent in next_b) != dag.depths[child_b] - 1
            or max(dag.depths[parent] for parent in next_d) != dag.depths[child_d] - 1
        ):
            continue
        edge_set.remove((parent_a, child_b))
        edge_set.remove((parent_c, child_d))
        edge_set.add(new_first)
        edge_set.add(new_second)
        edges[first_index] = new_first
        edges[second_index] = new_second
        predecessors[child_b] = next_b
        predecessors[child_d] = next_d
        accepted += 1
        if accepted >= target_swaps:
            changed = edge_count - len(original_edges & edge_set)
            if changed / edge_count >= MIN_CHANGED_EDGE_FRACTION:
                break

    rewired = tuple(tuple(sorted(parents)) for parents in predecessors)
    changed_edges = edge_count - len(original_edges & edge_set)
    changed_fraction = changed_edges / edge_count
    edge_count_pass = sum(len(parents) for parents in rewired) == edge_count
    order_pass = all(parent < child for child, parents in enumerate(rewired) for parent in parents)
    indegree_pass = tuple(len(parents) for parents in rewired) == dag.indegrees
    outdegree_pass = v16j.outdegrees(rewired) == v16j.outdegrees(original)
    depth_pass = tuple(v16i.recompute_depths(rewired)) == dag.depths
    age_pass = v16j.global_age_signature(rewired) == v16j.global_age_signature(original)
    footprint_pass = footprint_signature(rewired, metadata) == footprint_signature(original, metadata)
    completion_pass = accepted >= target_swaps and changed_fraction >= MIN_CHANGED_EDGE_FRACTION
    structure_pass = all((
        edge_count_pass, order_pass, indegree_pass, outdegree_pass,
        depth_pass, age_pass, footprint_pass,
    ))
    actual_conflict_edges = sum(
        v16n.edge_color(parent, child, metadata) is not None
        for child, parents in enumerate(rewired)
        for parent in parents
    )
    return rewired, {
        "edge_count": edge_count,
        "eligible_edge_count": len(eligible),
        "eligible_edge_fraction": len(eligible) / edge_count,
        "footprint_bucket_count": len(buckets),
        "movable_footprint_bucket_count": sum(len(indices) >= 2 for indices in buckets.values()),
        "target_accepted_swaps": target_swaps,
        "accepted_swaps": accepted,
        "attempted_swaps": attempts,
        "attempts_per_edge": attempts / edge_count,
        "acceptance_rate": accepted / attempts if attempts else 0.0,
        "changed_edge_count": changed_edges,
        "changed_edge_fraction": changed_fraction,
        "edge_count_pass": int(edge_count_pass),
        "scheduler_order_pass": int(order_pass),
        "indegree_sequence_pass": int(indegree_pass),
        "outdegree_sequence_pass": int(outdegree_pass),
        "depth_sequence_pass": int(depth_pass),
        "global_age_bin_histogram_pass": int(age_pass),
        "global_event_footprint_histogram_pass": int(footprint_pass),
        "actual_resource_conflict_edge_fraction": actual_conflict_edges / edge_count,
        "completion_and_change_pass": int(completion_pass),
        "structure_pass": int(structure_pass),
        "null_edge_sha256": v16j.edge_digest(rewired),
    }


def calibration_family(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    *,
    label: str,
    replicates: int,
    target_swap_multiplier: float,
    ceiling: int,
    prior_passes: Mapping[int, Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for replicate in range(replicates):
        seed = v16i.stable_seed("v16q", label, *dag.key, replicate, f"swap={target_swap_multiplier:.6f}")
        if replicate in prior_passes:
            audit = dict(prior_passes[replicate])
            audit["attempt_ceiling"] = ceiling
            audit["reused_from_lower_ceiling"] = 1
        else:
            _, measured = footprint_rewire(
                dag,
                metadata,
                seed,
                target_swap_multiplier=target_swap_multiplier,
                max_attempts_per_edge=ceiling,
            )
            audit = {
                **dag.prefix,
                "calibration_family": label,
                "target_swap_multiplier": target_swap_multiplier,
                "null_replicate": replicate,
                "null_seed": seed,
                "attempt_ceiling": ceiling,
                "reused_from_lower_ceiling": 0,
                **measured,
            }
        rows.append(audit)
    unique_count = len({row["null_edge_sha256"] for row in rows})
    unique_fraction = unique_count / len(rows)
    for row in rows:
        row["run_unique_null_count"] = unique_count
        row["run_unique_null_fraction"] = unique_fraction
        row["run_uniqueness_pass"] = int(unique_fraction >= MIN_UNIQUE_NULL_FRACTION)
        row["perturbation_integrity_pass"] = int(
            int(row["structure_pass"])
            and int(row["completion_and_change_pass"])
            and int(row["run_uniqueness_pass"])
        )
    return rows


def support_rows(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    counts: Counter[str] = Counter()
    for child, parents in enumerate(dag.predecessors):
        for parent in parents:
            counts[v16p.footprint_text(v16p.edge_footprint(parent, child, metadata))] += 1
    total = sum(counts.values())
    return [{
        **dag.prefix,
        "footprint": footprint,
        "edge_count": count,
        "edge_fraction": count / total,
        "bucket_movable_by_size": int(count >= 2),
    } for footprint, count in sorted(counts.items())]


def ceiling_summary_rows(audits: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    expected = len(v16n.assignments()) * (PRIMARY_REPLICATES + LONGER_REPLICATES)
    rows: List[Dict[str, Any]] = []
    for ceiling in ATTEMPT_CEILING_LADDER:
        selected = [row for row in audits if int(row["attempt_ceiling"]) == ceiling]
        passed = sum(int(row["perturbation_integrity_pass"]) for row in selected)
        rows.append({
            "attempt_ceiling": ceiling,
            "n_perturbations": len(selected),
            "integrity_passes": passed,
            "required_passes": expected,
            "max_attempts_per_edge_observed": max((float(row["attempts_per_edge"]) for row in selected), default=0.0),
            "min_changed_edge_fraction": min((float(row["changed_edge_fraction"]) for row in selected), default=0.0),
            "min_acceptance_rate": min((float(row["acceptance_rate"]) for row in selected), default=0.0),
            "min_actual_resource_conflict_edge_fraction": min((float(row["actual_resource_conflict_edge_fraction"]) for row in selected), default=0.0),
            "all_unique_within_run": int(bool(selected) and all(int(row["run_uniqueness_pass"]) for row in selected)),
            "ceiling_qualification_pass": int(len(selected) == expected and passed == expected),
        })
    return rows


def build_report(
    ceiling_rows: Sequence[Mapping[str, Any]],
    qualification: Mapping[str, Any],
    gates: Sequence[Mapping[str, Any]],
) -> str:
    lines = [
        "# v16q event-footprint null calibration",
        "",
        f"Status: `{qualification['status']}`.",
        "",
        "V16q is an effect-blind sampler calibration on the six frozen v16n DAGs. The proposal preserves event family plus source write-namespace and target read-namespace footprints, but does not require concrete resource overlap on proposed edges. No interval spectrum is computed.",
        "",
        f"Specification digest: `{spec_digest()}`.",
        "",
        "## Attempt ceiling ladder",
        "",
    ]
    lines.extend(v16i.table(ceiling_rows, (
        "attempt_ceiling", "n_perturbations", "integrity_passes", "required_passes",
        "max_attempts_per_edge_observed", "min_changed_edge_fraction",
        "min_acceptance_rate", "min_actual_resource_conflict_edge_fraction",
        "ceiling_qualification_pass",
    )))
    lines.extend(["", "## Gates", ""])
    lines.extend(v16i.table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "Qualification means only that the frozen procedure completed, generated unique changed DAGs, and preserved its declared finite-DAG invariants on this calibration corpus. It does not prove irreducibility, convergence, stationarity, independence, representativeness, or uniformity.",
        "",
        "Concrete resource conflict is deliberately not invariant under this coarse footprint rule. The reported retained-conflict fraction is diagnostic, not a qualification condition.",
        "",
        "No interval-spectrum effect or physical geometry claim is evaluated here.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    verify_frozen_sources()
    runs = v16o.load_runs()
    supports: List[Dict[str, Any]] = []
    for dag, metadata in runs:
        supports.extend(support_rows(dag, metadata))

    all_audits: List[Dict[str, Any]] = []
    selected_ceiling: Optional[int] = None
    prior: Dict[Tuple[Tuple[int, int, str, int], str], Dict[int, Dict[str, Any]]] = defaultdict(dict)
    for ceiling in ATTEMPT_CEILING_LADDER:
        ceiling_audits: List[Dict[str, Any]] = []
        for dag, metadata in runs:
            for label, replicates, multiplier in (
                ("primary_0075", PRIMARY_REPLICATES, PRIMARY_SWAP_MULTIPLIER),
                ("longer_0100", LONGER_REPLICATES, LONGER_SWAP_MULTIPLIER),
            ):
                key = (dag.key, label)
                rows = calibration_family(
                    dag,
                    metadata,
                    label=label,
                    replicates=replicates,
                    target_swap_multiplier=multiplier,
                    ceiling=ceiling,
                    prior_passes=prior[key],
                )
                ceiling_audits.extend(rows)
                prior[key] = {
                    int(row["null_replicate"]): dict(row)
                    for row in rows if int(row["perturbation_integrity_pass"])
                }
        all_audits.extend(ceiling_audits)
        passed = sum(int(row["perturbation_integrity_pass"]) for row in ceiling_audits)
        print(f"[v16q] ceiling={ceiling} integrity={passed}/{len(ceiling_audits)}")
        if passed == len(ceiling_audits):
            selected_ceiling = ceiling
            break

    ceiling_rows = ceiling_summary_rows(all_audits)
    qualified = selected_ceiling is not None
    status = "v16q_event_footprint_sampler_qualified" if qualified else "v16q_event_footprint_sampler_not_qualified"
    qualification = {
        "status": status,
        "selected_attempt_ceiling": "" if selected_ceiling is None else selected_ceiling,
        "selection_used_interval_spectrum": 0,
        "calibration_histories": len(runs),
        "primary_perturbations_required": len(runs) * PRIMARY_REPLICATES,
        "longer_perturbations_required": len(runs) * LONGER_REPLICATES,
        "next_step": (
            "freeze_posthoc_v16m_event_footprint_sensitivity_gate"
            if qualified else "repair_or_retire_event_footprint_sampler_without_spectrum"
        ),
    }
    gates = [
        {
            "gate": "frozen_source_and_footprint_support",
            "status": "pass",
            "observed": f"runs={len(runs)};v16p=promising",
            "required": f"runs={len(v16n.assignments())};v16p=promising",
            "decision": "continue",
        },
        {
            "gate": "effect_blind_attempt_ceiling_qualification",
            "status": "pass" if qualified else "fail",
            "observed": "none" if selected_ceiling is None else selected_ceiling,
            "required": "lowest_frozen_ceiling_with_all_288_perturbations_valid",
            "decision": "qualify" if qualified else "stop_without_spectrum",
        },
        {
            "gate": "spectrum_exclusion",
            "status": "pass",
            "observed": 0,
            "required": 0,
            "decision": "calibration_only",
        },
        {
            "gate": "v16q_overall",
            "status": status,
            "observed": f"ceiling={selected_ceiling}",
            "required": "ceiling=qualified",
            "decision": status,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "The frozen event-footprint sampler completed and preserved its declared invariants on six calibration DAGs.",
            "status": "supported" if qualified else "unsupported",
            "evidence": "v16q_sampler_qualification.csv;v16q_sampler_calibration_integrity.csv",
            "scope_limit": "effect-blind finite-DAG calibration only",
        },
        {
            "claim_id": "C2",
            "claim": "The sampler is converged, irreducible, stationary, independent, representative, or uniform.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "completion and integrity do not establish a sampling distribution",
        },
        {
            "claim_id": "C3",
            "claim": "The v16m interval-spectrum contrast survives event-footprint conditioning.",
            "status": "not_evaluated",
            "evidence": "none",
            "scope_limit": "v16q computes no interval spectra",
        },
        {
            "claim_id": "C4",
            "claim": "Dimension, Lorentz symmetry, spacetime, continuum physics, particles, or entanglement were established.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "sampler instrumentation only",
        },
    ]
    v16i.write_csv(FOOTPRINT_SUPPORT, supports)
    v16i.write_csv(CALIBRATION_AUDIT, all_audits)
    v16i.write_csv(CEILING_SUMMARY, ceiling_rows)
    v16i.write_csv(QUALIFICATION, [qualification])
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    REPORT.write_text(build_report(ceiling_rows, qualification, gates), encoding="utf-8")
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.16q\n\n"
        f"Status: `{status}`.\n\n"
        f"Selected attempt ceiling: `{qualification['selected_attempt_ceiling']}`.\n\n"
        f"Next: {qualification['next_step']}.\n\n"
        "No interval-spectrum effect, sampler convergence, or physical geometry was evaluated.\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.16q\n\n"
        f"Statusen er `{status}`. Denne runden tester om en grov kontrollgenerator faktisk kan lage mange endrede hendelsesgrafer uten aa bryte de avtalte strukturreglene. Den tester ikke universsignal eller fysikk.\n",
        encoding="utf-8",
    )
    print(f"[v16q] complete status={status} ceiling={qualification['selected_attempt_ceiling']}")


def verify_outputs() -> None:
    verify_frozen_sources()
    qualification = v16i.read_csv(QUALIFICATION)
    audits = v16i.read_csv(CALIBRATION_AUDIT)
    gates = v16i.read_csv(GATE_EVALUATION)
    if len(qualification) != 1:
        raise ValueError("v16q qualification row count failed")
    status = qualification[0]["status"]
    allowed = {"v16q_event_footprint_sampler_qualified", "v16q_event_footprint_sampler_not_qualified"}
    if status not in allowed:
        raise ValueError("v16q unknown status")
    if status == "v16q_event_footprint_sampler_qualified":
        ceiling = int(qualification[0]["selected_attempt_ceiling"])
        selected = [row for row in audits if int(row["attempt_ceiling"]) == ceiling]
        expected = len(v16n.assignments()) * (PRIMARY_REPLICATES + LONGER_REPLICATES)
        if len(selected) != expected or not all(int(row["perturbation_integrity_pass"]) for row in selected):
            raise ValueError("v16q selected ceiling integrity failed")
    if next(row["status"] for row in gates if row["gate"] == "spectrum_exclusion") != "pass":
        raise ValueError("v16q spectrum exclusion failed")
    print(f"[v16q] output verification pass status={status}")


def self_test() -> None:
    metadata = (
        {"family": "token", "reads": frozenset({"node:0"}), "writes": frozenset({"edge:0"})},
        {"family": "token", "reads": frozenset({"node:1"}), "writes": frozenset({"edge:1"})},
        {"family": "token", "reads": frozenset({"node:2"}), "writes": frozenset({"edge:2"})},
        {"family": "token", "reads": frozenset({"node:3"}), "writes": frozenset({"edge:3"})},
    )
    diamond = ((), (), (0, 1), (0, 1))
    dag = v16i.RunDAG(
        "test", 4, 1, 2, v16n.PRIMARY_ARM, 3,
        diamond,
        tuple(v16i.recompute_depths(diamond)),
        tuple(len(parents) for parents in diamond),
    )
    _, audit = footprint_rewire(
        dag,
        metadata,
        v16i.stable_seed("v16q", "self-test"),
        target_swap_multiplier=0.1,
        max_attempts_per_edge=60,
    )
    if not int(audit["structure_pass"]):
        raise AssertionError("v16q structural self-test failed")
    print("[v16q] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16q event-footprint null calibration")
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
