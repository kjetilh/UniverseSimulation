#!/usr/bin/env python3
"""v16n: effect-blind calibration of a coarse event/resource-aware DAG null.

This round qualifies sampler movement and preservation only. It must not
compute interval spectra or inspect v16m effect values when selecting the
attempt ceiling. A qualified sampler can support a later mechanism gate; it
does not establish convergence, uniformity, geometry, or physics.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import random
import shutil
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v16a_disjoint_event_commutation_gate as v16a
import relational_universe_v16ac_local_seed_adapter_gate as v16ac
import relational_universe_v16h_fresh_rate_logged_mechanism_holdout as v16h
import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16j_interval_strict_null_gate as v16j
import relational_universe_v16k_fresh_strict_null_replication as v16k
import relational_universe_v16m_qualified_sampler_fresh_holdout as v16m


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

TARGET_NODES = v16m.TARGET_NODES
STEPS = v16m.STEPS
PRIMARY_ARM = v16m.PRIMARY_ARM
GROWTH_SEEDS = tuple(
    7000 + v16i.stable_seed("v16n", "calibration-growth", index) % 2000
    for index in range(2)
)
RUN_OFFSETS = tuple(
    110000 + v16i.stable_seed("v16n", "calibration-offset", index) % 9000
    for index in range(3)
)
EXCLUDED_GROWTH_SEEDS = tuple(sorted({
    5203,
    5389,
    *v16k.GROWTH_SEEDS,
    *v16m.GROWTH_SEEDS,
}))

PRIMARY_REPLICATES = v16j.NULL_REPLICATES
PRIMARY_SWAP_MULTIPLIER = v16j.TARGET_ACCEPTED_SWAPS_PER_EDGE
LONGER_REPLICATES = v16k.LONGER_NULL_REPLICATES
LONGER_SWAP_MULTIPLIER = v16k.LONGER_TARGET_SWAP_MULTIPLIER
ATTEMPT_CEILING_LADDER = (240, 480, 960, 1920)
MIN_CHANGED_EDGE_FRACTION = v16j.MIN_CHANGED_EDGE_FRACTION
MIN_UNIQUE_NULL_FRACTION = v16j.MIN_UNIQUE_NULL_FRACTION
NULL_FAMILY = "degree_depth_age_coarse_event_resource_color_double_edge_swap"

SOURCE_CHAIN = DOC / "v16n_source_chain.csv"
PRE_REGISTRATION = DOC / "v16n_pre_registration.csv"
TARGET_SUMMARY = DOC / "v16n_target_summary.csv"
EVENT_LOG = DOC / "v16n_calibration_event_log.csv"
EDGE_LOG = DOC / "v16n_calibration_fine_dependency_edges.csv"
RUN_SUMMARY = DOC / "v16n_calibration_run_summary.csv"
METADATA_AUDIT = DOC / "v16n_event_metadata_audit.csv"
COLOR_SUPPORT = DOC / "v16n_edge_color_support.csv"
CALIBRATION_AUDIT = DOC / "v16n_sampler_calibration_integrity.csv"
CEILING_SUMMARY = DOC / "v16n_attempt_ceiling_summary.csv"
QUALIFICATION = DOC / "v16n_sampler_qualification.csv"
GATE_EVALUATION = DOC / "v16n_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16n_claim_ledger.csv"
REPORT = DOC / "v16n_coarse_event_resource_null_calibration.md"
RECOMMENDATION = DOC / "v0_16n_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16n.md"

EdgeColor = Tuple[str, str, Tuple[str, ...]]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assignments() -> List[Dict[str, Any]]:
    return [
        {
            "growth_seed": growth_seed,
            "run_offset": run_offset,
            "arm": PRIMARY_ARM,
            "run_seed": v16h.run_seed(growth_seed, run_offset, PRIMARY_ARM),
        }
        for growth_seed in GROWTH_SEEDS
        for run_offset in RUN_OFFSETS
    ]


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = [
        ("v16h", "fresh_dynamics_implementation", Path(v16h.__file__)),
        ("v16j", "base_strict_null_implementation", Path(v16j.__file__)),
        ("v16m", "replicated_holdout_implementation", Path(v16m.__file__)),
        ("v16m", "replicated_holdout_gate", DOC / "v16m_gate_evaluation.csv"),
        ("v16n", "panel_direction_report", DOC / "v16n_panel_direction_report.md"),
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
        "gate": "v16n_coarse_event_resource_null_calibration",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_sampler_calibration_only",
        "target_nodes": TARGET_NODES,
        "steps": STEPS,
        "growth_seeds": list(GROWTH_SEEDS),
        "run_offsets": list(RUN_OFFSETS),
        "arm": PRIMARY_ARM,
        "excluded_growth_seeds": list(EXCLUDED_GROWTH_SEEDS),
        "null_family": NULL_FAMILY,
        "edge_color": [
            "parent_event_family",
            "child_event_family",
            "actual_shared_resource_conflict_direction_and_namespace",
        ],
        "conflict_directions": ["write-read", "write-write", "read-write"],
        "resource_namespace_rule": "prefix_before_first_colon",
        "preserves": [
            "event_count",
            "scheduler_order",
            "exact_per_event_indegree",
            "exact_per_event_outdegree",
            "exact_causal_depth_sequence",
            "global_dyadic_parent_age_bin_histogram",
            "global_coarse_event_resource_edge_color_histogram",
            "actual_resource_conflict_for_every_null_edge",
        ],
        "does_not_preserve": [
            "exact_parent_age_per_edge",
            "per_child_age_bin_multiset",
            "per_child_edge_color_multiset",
            "exact_resource_identity_edge_histogram",
            "event_type_transition_histogram",
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
        "no_early_scientific_stop": True,
    }


def spec_digest() -> str:
    raw = json.dumps(spec_payload(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def preregistration_rows() -> List[Dict[str, Any]]:
    return [
        {
            "purpose_ref": PURPOSE_REF,
            "spec_digest": spec_digest(),
            "script_sha256": file_sha256(SCRIPT),
            "source_chain_sha256": file_sha256(SOURCE_CHAIN),
            "target_nodes": TARGET_NODES,
            "steps": STEPS,
            **assignment,
            "primary_replicates": PRIMARY_REPLICATES,
            "primary_swap_multiplier": PRIMARY_SWAP_MULTIPLIER,
            "longer_replicates": LONGER_REPLICATES,
            "longer_swap_multiplier": LONGER_SWAP_MULTIPLIER,
            "attempt_ceiling_ladder": ";".join(str(value) for value in ATTEMPT_CEILING_LADDER),
            "spectrum_computation_allowed": 0,
            "calibration_history_generated_after_freeze": 1,
        }
        for assignment in assignments()
    ]


def prepare() -> None:
    v16m.verify_outputs()
    if set(GROWTH_SEEDS) & set(EXCLUDED_GROWTH_SEEDS):
        raise ValueError("v16n calibration seeds overlap prior or quarantined seeds")
    if shutil.disk_usage(ROOT).free < v16k.MIN_FREE_BYTES:
        raise RuntimeError("v16n preflight requires at least 250 MiB free")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    rows = preregistration_rows()
    v16i.write_csv(PRE_REGISTRATION, rows)
    print(f"[v16n] prepared runs={len(rows)} digest={spec_digest()}")


def load_and_verify_preregistration() -> List[Dict[str, str]]:
    observed = v16i.read_csv(PRE_REGISTRATION)
    expected = [{key: str(value) for key, value in row.items()} for row in preregistration_rows()]
    if observed != expected:
        raise ValueError("v16n preregistration changed")
    frozen_sources = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current_sources = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen_sources != current_sources:
        raise ValueError("v16n source chain changed")
    return observed


def split_resources(value: Any) -> frozenset[str]:
    return frozenset(part for part in str(value).split(";") if part)


def resource_namespace(resource: str) -> str:
    prefix, separator, _ = resource.partition(":")
    return prefix if separator and prefix else "other"


def event_metadata(events: Sequence[Mapping[str, Any]]) -> Tuple[Tuple[Dict[str, Any], ...], Dict[str, Any]]:
    ordered = sorted(events, key=lambda row: int(row["event_id"]))
    ids = [int(row["event_id"]) for row in ordered]
    expected = list(range(len(ordered)))
    total_mapping = ids == expected
    metadata = tuple({
        "family": str(row["family"]),
        "event_type": str(row["event_type"]),
        "reads": split_resources(row["read_resources"]),
        "writes": split_resources(row["write_resources"]),
    } for row in ordered)
    payload = [
        {
            "event_id": event_id,
            "family": row["family"],
            "event_type": row["event_type"],
            "reads": sorted(row["reads"]),
            "writes": sorted(row["writes"]),
        }
        for event_id, row in enumerate(metadata)
    ]
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    namespaces = Counter(
        resource_namespace(resource)
        for row in metadata
        for resource in (*row["reads"], *row["writes"])
    )
    return metadata, {
        "event_rows": len(ordered),
        "event_id_mapping_total_pass": int(total_mapping),
        "metadata_sha256": digest,
        "resource_namespaces": ";".join(f"{key}:{value}" for key, value in sorted(namespaces.items())),
        "other_namespace_count": namespaces.get("other", 0),
    }


def conflict_channels(parent: Mapping[str, Any], child: Mapping[str, Any]) -> Tuple[str, ...]:
    channels: Set[str] = set()
    for direction, shared in (
        ("write-read", parent["writes"] & child["reads"]),
        ("write-write", parent["writes"] & child["writes"]),
        ("read-write", parent["reads"] & child["writes"]),
    ):
        channels.update(f"{direction}:{resource_namespace(resource)}" for resource in shared)
    return tuple(sorted(channels))


def edge_color(parent: int, child: int, metadata: Sequence[Mapping[str, Any]]) -> Optional[EdgeColor]:
    channels = conflict_channels(metadata[parent], metadata[child])
    if not channels:
        return None
    return (str(metadata[parent]["family"]), str(metadata[child]["family"]), channels)


def color_text(color: EdgeColor) -> str:
    return f"{color[0]}->{color[1]}|{'&'.join(color[2])}"


def color_signature(
    predecessors: Sequence[Sequence[int]],
    metadata: Sequence[Mapping[str, Any]],
) -> Tuple[Tuple[str, int], ...]:
    counts: Counter[str] = Counter()
    for child, parents in enumerate(predecessors):
        for parent in parents:
            color = edge_color(parent, child, metadata)
            counts["missing_actual_conflict" if color is None else color_text(color)] += 1
    return tuple(sorted(counts.items()))


def coarse_rewire(
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
    edges: List[Tuple[int, int]] = [
        (parent, child)
        for child, parents in enumerate(original)
        for parent in parents
    ]
    edge_set = set(edges)
    original_edges = set(edges)
    edge_count = len(edges)
    colors = [edge_color(parent, child, metadata) for parent, child in edges]
    if any(color is None for color in colors):
        raise ValueError("v16n source DAG contains an edge without an actual resource conflict")
    buckets: Dict[EdgeColor, List[int]] = defaultdict(list)
    for index, color in enumerate(colors):
        assert color is not None
        buckets[color].append(index)
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
        bucket_color = colors[first_index]
        assert bucket_color is not None
        candidates = buckets[bucket_color]
        second_position = rng.randrange(len(candidates) - 1)
        first_position = bucket_positions[first_index]
        if second_position >= first_position:
            second_position += 1
        second_index = candidates[second_position]
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
        if edge_color(*new_first, metadata) != bucket_color:
            continue
        if edge_color(*new_second, metadata) != bucket_color:
            continue

        old_age_bins = sorted((v16j.lag_bin(parent_a, child_b), v16j.lag_bin(parent_c, child_d)))
        new_age_bins = sorted((v16j.lag_bin(parent_a, child_d), v16j.lag_bin(parent_c, child_b)))
        if new_age_bins != old_age_bins:
            continue

        next_b = (predecessors[child_b] - {parent_a}) | {parent_c}
        next_d = (predecessors[child_d] - {parent_c}) | {parent_a}
        if not next_b or not next_d:
            continue
        if max(dag.depths[parent] for parent in next_b) != dag.depths[child_b] - 1:
            continue
        if max(dag.depths[parent] for parent in next_d) != dag.depths[child_d] - 1:
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
            changed_now = edge_count - len(original_edges & edge_set)
            if changed_now / edge_count >= MIN_CHANGED_EDGE_FRACTION:
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
    color_pass = color_signature(rewired, metadata) == color_signature(original, metadata)
    conflict_pass = all(
        edge_color(parent, child, metadata) is not None
        for child, parents in enumerate(rewired)
        for parent in parents
    )
    completion_pass = accepted >= target_swaps and changed_fraction >= MIN_CHANGED_EDGE_FRACTION
    structure_pass = all((
        edge_count_pass,
        order_pass,
        indegree_pass,
        outdegree_pass,
        depth_pass,
        age_pass,
        color_pass,
        conflict_pass,
    ))
    return rewired, {
        "edge_count": edge_count,
        "eligible_edge_count": len(eligible),
        "eligible_edge_fraction": len(eligible) / edge_count if edge_count else 0.0,
        "color_bucket_count": len(buckets),
        "movable_color_bucket_count": sum(len(indices) >= 2 for indices in buckets.values()),
        "target_accepted_swaps": target_swaps,
        "accepted_swaps": accepted,
        "attempted_swaps": attempts,
        "attempts_per_edge": attempts / edge_count if edge_count else 0.0,
        "acceptance_rate": accepted / attempts if attempts else 0.0,
        "changed_edge_count": changed_edges,
        "changed_edge_fraction": changed_fraction,
        "edge_count_pass": int(edge_count_pass),
        "scheduler_order_pass": int(order_pass),
        "indegree_sequence_pass": int(indegree_pass),
        "outdegree_sequence_pass": int(outdegree_pass),
        "depth_sequence_pass": int(depth_pass),
        "global_age_bin_histogram_pass": int(age_pass),
        "global_edge_color_histogram_pass": int(color_pass),
        "actual_resource_conflict_edges_pass": int(conflict_pass),
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
        seed = v16i.stable_seed(
            "v16n",
            label,
            *dag.key,
            replicate,
            f"swap={target_swap_multiplier:.6f}",
        )
        if replicate in prior_passes:
            audit = dict(prior_passes[replicate])
            audit["attempt_ceiling"] = ceiling
            audit["reused_from_lower_ceiling"] = 1
        else:
            _, audit = coarse_rewire(
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
                **audit,
            }
        rows.append(audit)

    unique_count = len({row["null_edge_sha256"] for row in rows})
    unique_fraction = unique_count / len(rows) if rows else 0.0
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


def calibration_dag(assignment: Mapping[str, Any], events: Sequence[Mapping[str, Any]], dependency_dag: Any) -> v16i.RunDAG:
    source = v16k.run_dag_from_history(assignment, events, dependency_dag)
    return v16i.RunDAG(
        stage="v16n_calibration",
        target_nodes=source.target_nodes,
        growth_seed=source.growth_seed,
        run_offset=source.run_offset,
        arm=source.arm,
        run_seed=source.run_seed,
        predecessors=source.predecessors,
        depths=source.depths,
        indegrees=source.indegrees,
    )


def support_rows(dag: v16i.RunDAG, metadata: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    counts: Counter[str] = Counter()
    for child, parents in enumerate(dag.predecessors):
        for parent in parents:
            color = edge_color(parent, child, metadata)
            counts["missing_actual_conflict" if color is None else color_text(color)] += 1
    return [
        {
            **dag.prefix,
            "edge_color": color,
            "edge_count": count,
            "edge_fraction": count / sum(counts.values()),
            "bucket_movable_by_size": int(count >= 2),
        }
        for color, count in sorted(counts.items())
    ]


def ceiling_summary_rows(audits: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    expected = len(assignments()) * (PRIMARY_REPLICATES + LONGER_REPLICATES)
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
            "min_eligible_edge_fraction": min((float(row["eligible_edge_fraction"]) for row in selected), default=0.0),
            "all_unique_within_run": int(bool(selected) and all(int(row["run_uniqueness_pass"]) for row in selected)),
            "ceiling_qualification_pass": int(len(selected) == expected and passed == expected),
        })
    return rows


def build_report(
    metadata_rows: Sequence[Mapping[str, Any]],
    ceiling_rows: Sequence[Mapping[str, Any]],
    qualification: Mapping[str, Any],
    gates: Sequence[Mapping[str, Any]],
) -> str:
    lines = [
        "# v16n coarse event/resource null calibration",
        "",
        f"Status: `{qualification['status']}`.",
        "",
        "v16n is an effect-blind sampler calibration. It generated six new calibration histories after freezing the event/resource color, proposal rule, ceiling ladder, integrity criteria, assignments, and source hashes. No interval spectrum was computed in this round.",
        "",
        f"Specification digest: `{spec_digest()}`.",
        "",
        "## Coarse edge color",
        "",
        "Each edge color contains parent family, child family, and the sorted set of actual shared-resource conflict channels. Channels retain access direction and the namespace before the first colon, but not the concrete resource identity. Proposed swaps must preserve the global color histogram and every resulting edge must still have an actual concrete read/write conflict.",
        "",
        "This is stronger than the v16j degree/depth/age null but weaker than exact resource-identity or per-child conditioning.",
        "",
        "## Metadata audit",
        "",
    ]
    lines.extend(v16i.table(metadata_rows, (
        "growth_seed", "run_offset", "event_rows", "event_id_mapping_total_pass",
        "other_namespace_count", "metadata_sha256",
    )))
    lines.extend(["", "## Attempt ceiling ladder", ""])
    lines.extend(v16i.table(ceiling_rows, (
        "attempt_ceiling", "n_perturbations", "integrity_passes", "required_passes",
        "max_attempts_per_edge_observed", "min_changed_edge_fraction",
        "min_eligible_edge_fraction", "ceiling_qualification_pass",
    )))
    lines.extend(["", "## Gates", ""])
    lines.extend(v16i.table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "A qualified result means only that this frozen constrained perturbation procedure completed and preserved its declared finite-DAG invariants on the calibration corpus. It does not prove irreducibility, convergence, stationarity, independence, representativeness, or uniform sampling.",
        "",
        "No effect, dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particle, entanglement, or physical-law claim is evaluated here.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    prereg = load_and_verify_preregistration()
    if shutil.disk_usage(ROOT).free < v16k.MIN_FREE_BYTES:
        raise RuntimeError("v16n run preflight requires at least 250 MiB free")
    adapter = v16ac.LocalSeedClockAdapter(v16h.frozen_local_rate())
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(
        ensembles, v10e.recommended_regime("fast_balanced"), list(GROWTH_SEEDS)
    )
    target_rows = v10e.summarize_bases(base_rows)
    ensemble_name = ensembles[0].name
    params = v16a.anchor_params()

    events_all: List[Dict[str, Any]] = []
    edges_all: List[Dict[str, Any]] = []
    run_rows: List[Dict[str, Any]] = []
    metadata_rows: List[Dict[str, Any]] = []
    supports: List[Dict[str, Any]] = []
    dags: List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]] = []

    for index, assignment in enumerate(prereg, start=1):
        base = base_states[(ensemble_name, int(assignment["growth_seed"]))]
        events, edges, rates, run_row, _, _, dependency_dag = v16h.run_assignment(
            base, assignment, params, adapter
        )
        direct = v16h.direct_rate_audit(base, events, rates, run_row, v16h.frozen_local_rate())
        if not int(direct["direct_log_parity_pass"]):
            raise RuntimeError("v16n direct-rate parity failed")
        dag = calibration_dag(assignment, events, dependency_dag)
        metadata, metadata_audit = event_metadata(events)
        if len(metadata) != len(dag.predecessors):
            raise RuntimeError("v16n event metadata and DAG sizes differ")
        if not int(metadata_audit["event_id_mapping_total_pass"]):
            raise RuntimeError("v16n event metadata mapping failed")
        if any(edge_color(parent, child, metadata) is None for child, parents in enumerate(dag.predecessors) for parent in parents):
            raise RuntimeError("v16n source edge lacks actual conflict witness")
        metadata_rows.append({**dag.prefix, **metadata_audit})
        supports.extend(support_rows(dag, metadata))
        dags.append((dag, metadata))
        events_all.extend(events)
        edges_all.extend(edges)
        run_rows.append(run_row)
        print(f"[v16n] calibration histories={index}/{len(prereg)} edges={sum(len(row) for row in dag.predecessors)}")

    all_audits: List[Dict[str, Any]] = []
    selected_ceiling: Optional[int] = None
    prior: Dict[Tuple[Tuple[int, int, str, int], str], Dict[int, Dict[str, Any]]] = defaultdict(dict)
    for ceiling in ATTEMPT_CEILING_LADDER:
        ceiling_rows: List[Dict[str, Any]] = []
        for dag, metadata in dags:
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
                ceiling_rows.extend(rows)
                prior[key] = {
                    int(row["null_replicate"]): dict(row)
                    for row in rows
                    if int(row["perturbation_integrity_pass"])
                }
        all_audits.extend(ceiling_rows)
        passed = sum(int(row["perturbation_integrity_pass"]) for row in ceiling_rows)
        print(f"[v16n] ceiling={ceiling} integrity={passed}/{len(ceiling_rows)}")
        if passed == len(ceiling_rows):
            selected_ceiling = ceiling
            break

    ceiling_rows = ceiling_summary_rows(all_audits)
    target_pass = (
        len(target_rows) == 1
        and int(float(target_rows[0]["mean_initial_nodes"])) == TARGET_NODES
        and int(target_rows[0]["separated_from_prev"]) == 1
    )
    history_pass = (
        target_pass
        and len(run_rows) == len(assignments())
        and all(
            int(row["n_events"]) == STEPS
            and int(row["invalid_events"]) == 0
            and int(row["fine_acyclic"]) == 1
            and int(row["fine_edge_witness_errors"]) == 0
            and int(row["topological_replay_failures"]) == 0
            and int(row["relabel_pass"]) == 1
            for row in run_rows
        )
        and all(int(row["event_id_mapping_total_pass"]) for row in metadata_rows)
    )
    qualified = selected_ceiling is not None and history_pass
    status = (
        "v16n_coarse_event_resource_sampler_qualified"
        if qualified
        else "v16n_coarse_event_resource_sampler_not_qualified"
    )
    qualification = {
        "status": status,
        "selected_attempt_ceiling": "" if selected_ceiling is None else selected_ceiling,
        "selection_used_interval_spectrum": 0,
        "calibration_histories": len(run_rows),
        "primary_perturbations_required": len(assignments()) * PRIMARY_REPLICATES,
        "longer_perturbations_required": len(assignments()) * LONGER_REPLICATES,
        "next_step": (
            "freeze_and_apply_to_v16m_as_posthoc_mechanism_sensitivity"
            if qualified
            else "repair_or_retire_coarse_event_resource_sampler"
        ),
    }
    gates = [
        {
            "gate": "fresh_calibration_history_and_metadata_integrity",
            "status": "pass" if history_pass else "fail",
            "observed": f"runs={len(run_rows)};events={len(events_all)};metadata={sum(int(row['event_id_mapping_total_pass']) for row in metadata_rows)}/{len(metadata_rows)}",
            "required": f"runs={len(assignments())};events={len(assignments()) * STEPS};metadata={len(assignments())}/{len(assignments())}",
            "decision": "continue" if history_pass else "repair",
        },
        {
            "gate": "effect_blind_attempt_ceiling_qualification",
            "status": "pass" if selected_ceiling is not None else "fail",
            "observed": "none" if selected_ceiling is None else selected_ceiling,
            "required": "lowest_frozen_ceiling_with_all_288_perturbations_valid",
            "decision": "qualify" if selected_ceiling is not None else "stop_without_spectrum",
        },
        {
            "gate": "spectrum_exclusion",
            "status": "pass",
            "observed": 0,
            "required": 0,
            "decision": "calibration_only",
        },
        {
            "gate": "v16n_overall",
            "status": status,
            "observed": f"history={int(history_pass)};ceiling={selected_ceiling}",
            "required": "history=1;ceiling=qualified",
            "decision": status,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "The frozen coarse event/resource sampler completed and preserved its declared invariants on six fresh calibration histories.",
            "status": "supported" if qualified else "unsupported",
            "evidence": "v16n_sampler_qualification.csv;v16n_sampler_calibration_integrity.csv",
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
            "claim": "The v16m interval-spectrum contrast survives coarse event/resource conditioning.",
            "status": "not_evaluated",
            "evidence": "none",
            "scope_limit": "v16n computes no interval spectra",
        },
        {
            "claim_id": "C4",
            "claim": "Dimension, Lorentz symmetry, spacetime, continuum physics, particles, or entanglement were established.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "sampler instrumentation only",
        },
    ]

    v16i.write_csv(TARGET_SUMMARY, target_rows)
    v16i.write_csv(EVENT_LOG, events_all)
    v16i.write_csv(EDGE_LOG, edges_all)
    v16i.write_csv(RUN_SUMMARY, run_rows)
    v16i.write_csv(METADATA_AUDIT, metadata_rows)
    v16i.write_csv(COLOR_SUPPORT, supports)
    v16i.write_csv(CALIBRATION_AUDIT, all_audits)
    v16i.write_csv(CEILING_SUMMARY, ceiling_rows)
    v16i.write_csv(QUALIFICATION, [qualification])
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    REPORT.write_text(build_report(metadata_rows, ceiling_rows, qualification, gates), encoding="utf-8")
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.16n\n\n"
        f"Status: `{status}`.\n\n"
        f"Selected attempt ceiling: `{qualification['selected_attempt_ceiling']}`.\n\n"
        f"Next: {qualification['next_step']}.\n\n"
        "This calibration does not evaluate an interval-spectrum effect or authorize a geometry claim.\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.16n\n\n"
        f"Statusen er `{status}`. Denne runden tester bare om en strengere kontrollgenerator kan bevege hendelsesgrafene uten aa bryte de avtalte strukturreglene. Den tester ikke om signalet finnes, og den finner ikke romtid eller naturlover.\n",
        encoding="utf-8",
    )
    print(f"[v16n] complete status={status} ceiling={qualification['selected_attempt_ceiling']}")


def verify_outputs() -> None:
    load_and_verify_preregistration()
    qualification = v16i.read_csv(QUALIFICATION)
    gates = v16i.read_csv(GATE_EVALUATION)
    audits = v16i.read_csv(CALIBRATION_AUDIT)
    if len(qualification) != 1:
        raise ValueError("v16n qualification row count failed")
    status = qualification[0]["status"]
    allowed = {
        "v16n_coarse_event_resource_sampler_qualified",
        "v16n_coarse_event_resource_sampler_not_qualified",
    }
    if status not in allowed:
        raise ValueError("v16n unknown status")
    if len(v16i.read_csv(RUN_SUMMARY)) != len(assignments()):
        raise ValueError("v16n run count failed")
    if len(v16i.read_csv(EVENT_LOG)) != len(assignments()) * STEPS:
        raise ValueError("v16n event count failed")
    if status == "v16n_coarse_event_resource_sampler_qualified":
        ceiling = int(qualification[0]["selected_attempt_ceiling"])
        selected = [row for row in audits if int(row["attempt_ceiling"]) == ceiling]
        expected = len(assignments()) * (PRIMARY_REPLICATES + LONGER_REPLICATES)
        if len(selected) != expected or not all(int(row["perturbation_integrity_pass"]) for row in selected):
            raise ValueError("v16n selected ceiling integrity failed")
    if next(row["status"] for row in gates if row["gate"] == "spectrum_exclusion") != "pass":
        raise ValueError("v16n spectrum exclusion failed")
    print(f"[v16n] output verification pass status={status}")


def self_test() -> None:
    rows = assignments()
    if len(rows) != 6 or len({row["run_seed"] for row in rows}) != 6:
        raise AssertionError("v16n assignments failed")
    if set(GROWTH_SEEDS) & set(EXCLUDED_GROWTH_SEEDS):
        raise AssertionError("v16n seeds overlap excluded histories")
    metadata = (
        {"family": "token", "event_type": "move", "reads": frozenset({"token:1"}), "writes": frozenset({"token:1"})},
        {"family": "token", "event_type": "move", "reads": frozenset({"token:1"}), "writes": frozenset({"token:1"})},
        {"family": "token", "event_type": "move", "reads": frozenset({"token:1"}), "writes": frozenset({"token:1"})},
        {"family": "token", "event_type": "move", "reads": frozenset({"token:1"}), "writes": frozenset({"token:1"})},
    )
    color = edge_color(0, 1, metadata)
    if color is None or "write-read:token" not in color[2]:
        raise AssertionError("v16n edge color failed")
    diamond = ((), (), (0, 1), (0, 1))
    dag = v16i.RunDAG(
        "test", 4, 1, 2, PRIMARY_ARM, 3,
        diamond,
        tuple(v16i.recompute_depths(diamond)),
        tuple(len(parents) for parents in diamond),
    )
    _, audit = coarse_rewire(
        dag,
        metadata,
        v16i.stable_seed("v16n", "self-test"),
        target_swap_multiplier=0.1,
        max_attempts_per_edge=240,
    )
    if not int(audit["structure_pass"]):
        raise AssertionError("v16n structural self-test failed")
    print(f"[v16n] self-test pass seeds={GROWTH_SEEDS} offsets={RUN_OFFSETS}")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16n coarse event/resource null calibration")
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
