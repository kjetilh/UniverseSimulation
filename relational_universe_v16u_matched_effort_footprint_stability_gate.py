#!/usr/bin/env python3
"""v16u: effect-blind footprint-null stability at exact matched effort.

The source DAG spectrum and every observed/null effect metric are excluded. The
gate burns each source/replicate to the qualified change floor, branches from
that state, and compares null-spectrum centers after exact accepted-swap
increments K, 2K, and a prefix-matched K+K segmented path.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
import math
from pathlib import Path
import random
from typing import Any, Dict, List, Mapping, Sequence, Set, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16j_interval_strict_null_gate as v16j
import relational_universe_v16n_coarse_event_resource_null_calibration as v16n
import relational_universe_v16p_event_footprint_reachability_audit as v16p
import relational_universe_v16q_event_footprint_null_calibration as v16q
import relational_universe_v16s_fresh_event_footprint_holdout as v16s
import relational_universe_v16t_footprint_null_path_stability_gate as v16t


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"

REPLICATES = 16
BURNIN_SWAP_MULTIPLIER = 0.100
K_ACCEPTED_SWAPS_PER_EDGE = 0.100
MAX_ATTEMPTS_PER_EDGE = 240
MIN_CHANGED_EDGE_FRACTION = v16q.MIN_CHANGED_EDGE_FRACTION
MIN_UNIQUE_NULL_FRACTION = v16q.MIN_UNIQUE_NULL_FRACTION
MAX_CENTER_SHIFT_RATIO = 2.0

PROTOCOLS: Tuple[str, ...] = (
    "burnin",
    "direct_plus_k",
    "direct_plus_2k",
    "staged_plus_k_plus_k",
)
COMPARISONS: Tuple[Tuple[str, str, str, str], ...] = (
    ("burnin_vs_plus_k", "burnin", "direct_plus_k", "realized_length"),
    ("plus_k_vs_plus_2k", "direct_plus_k", "direct_plus_2k", "realized_length"),
    ("burnin_vs_plus_2k", "burnin", "direct_plus_2k", "realized_length"),
    (
        "direct_plus_2k_vs_staged_plus_k_plus_k",
        "direct_plus_2k",
        "staged_plus_k_plus_k",
        "path_segmentation",
    ),
)

SOURCE_CHAIN = DOC / "v16u_source_chain.csv"
PRE_REGISTRATION = DOC / "v16u_pre_registration.csv"
NULL_DISTRIBUTION = DOC / "v16u_null_spectrum_distribution.csv"
PERTURBATION_AUDIT = DOC / "v16u_matched_effort_perturbation_audit.csv"
REALIZED_EFFORT_AUDIT = DOC / "v16u_realized_effort_audit.csv"
PROTOCOL_SUMMARY = DOC / "v16u_null_protocol_summary.csv"
CENTER_COMPARISON = DOC / "v16u_null_center_comparison.csv"
GATE_EVALUATION = DOC / "v16u_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16u_claim_ledger.csv"
REPORT = DOC / "v16u_matched_effort_footprint_stability_gate.md"
RECOMMENDATION = DOC / "v0_16u_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16u.md"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = (
        ("v16s", "fresh_event_histories", v16s.EVENT_LOG),
        ("v16s", "fresh_dependency_edges", v16s.EDGE_LOG),
        ("v16s", "fresh_history_gate", v16s.GATE_EVALUATION),
        ("v16q", "footprint_sampler_implementation", Path(v16q.__file__)),
        ("v16q", "sampler_qualification", v16q.QUALIFICATION),
        ("v16t", "frozen_stability_implementation", Path(v16t.__file__)),
        ("v16t", "realized_effort_interpretation_audit", DOC / "v16t_realized_effort_interpretation_audit.csv"),
        ("v16t", "matched_effort_next_direction", DOC / "v16t_next_direction_assessment.md"),
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
        "gate": "v16u_matched_effort_footprint_stability_gate",
        "purpose_ref": PURPOSE_REF,
        "scope": "effect_blind_exact_realized_effort_stability_on_six_frozen_v16s_histories",
        "source_history_count": 6,
        "source_arm": v16s.PRIMARY_ARM,
        "null_family": v16q.NULL_FAMILY,
        "burnin_swap_multiplier": BURNIN_SWAP_MULTIPLIER,
        "burnin_min_changed_edge_fraction": MIN_CHANGED_EDGE_FRACTION,
        "k_formula": "ceil(source_edge_count*0.100)",
        "k_accepted_swaps_per_edge": K_ACCEPTED_SWAPS_PER_EDGE,
        "protocols": list(PROTOCOLS),
        "comparisons": [
            {"label": label, "left": left, "right": right, "gate_family": family}
            for label, left, right, family in COMPARISONS
        ],
        "path_isolation": "direct_2k_and_staged_k_plus_k_share_the_exact_k_prefix",
        "replicates_per_protocol_per_history": REPLICATES,
        "max_attempts_per_edge_per_path": MAX_ATTEMPTS_PER_EDGE,
        "min_unique_null_fraction": MIN_UNIQUE_NULL_FRACTION,
        "center_metric": "jensen_shannon_between_protocol_mean_spectra",
        "dispersion_metric": "median_pooled_leave_one_out_jensen_shannon",
        "center_shift_ratio": "center_js/max(pooled_leave_one_out_median,epsilon)",
        "max_center_shift_ratio": MAX_CENTER_SHIFT_RATIO,
        "all_source_dags_must_pass": True,
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
        "protocols": ";".join(PROTOCOLS),
        "replicates_per_protocol_per_history": REPLICATES,
        "burnin_swap_multiplier": BURNIN_SWAP_MULTIPLIER,
        "k_accepted_swaps_per_edge": K_ACCEPTED_SWAPS_PER_EDGE,
        "max_attempts_per_edge_per_path": MAX_ATTEMPTS_PER_EDGE,
        "min_changed_edge_fraction": MIN_CHANGED_EDGE_FRACTION,
        "min_unique_null_fraction": MIN_UNIQUE_NULL_FRACTION,
        "max_center_shift_ratio": MAX_CENTER_SHIFT_RATIO,
        "path_prefix_reused": 1,
        "source_spectrum_computation_allowed": 0,
        "observed_effect_computation_allowed": 0,
    }


def prepare() -> None:
    v16t.verify_outputs()
    audit = next(
        row for row in v16i.read_csv(DOC / "v16t_realized_effort_interpretation_audit.csv")
        if row["audit_item"] == "overall_semantic"
    )
    if audit["status"] != "v16t_center_stability_observed_but_length_path_decomposition_inconclusive":
        raise ValueError("v16u requires the frozen v16t realized-effort diagnosis")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [preregistration_row()])
    print(f"[v16u] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    rows = v16i.read_csv(PRE_REGISTRATION)
    expected = {key: str(value) for key, value in preregistration_row().items()}
    if len(rows) != 1 or rows[0] != expected:
        raise ValueError("v16u preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v16u source chain changed")


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    loaded = []
    for dag, metadata in v16t.load_runs():
        loaded.append((v16i.RunDAG(
            stage="v16u",
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
        raise ValueError("v16u requires six frozen v16s histories")
    return loaded


def with_predecessors(dag: v16i.RunDAG, predecessors: Sequence[Sequence[int]]) -> v16i.RunDAG:
    return v16i.RunDAG(
        stage="v16u",
        target_nodes=dag.target_nodes,
        growth_seed=dag.growth_seed,
        run_offset=dag.run_offset,
        arm=dag.arm,
        run_seed=dag.run_seed,
        predecessors=tuple(tuple(parents) for parents in predecessors),
        depths=dag.depths,
        indegrees=dag.indegrees,
    )


def exact_footprint_path(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    seed: int,
    accepted_targets: Sequence[int],
) -> Tuple[Dict[int, Tuple[Tuple[int, ...], ...]], Dict[int, Dict[str, Any]]]:
    """Return exact accepted-swap checkpoints without a changed-edge stop rule."""
    targets = tuple(sorted(set(int(value) for value in accepted_targets)))
    if not targets or targets[0] <= 0:
        raise ValueError("v16u exact targets must be positive")
    rng = random.Random(seed)
    original = tuple(tuple(parents) for parents in dag.predecessors)
    predecessors: List[Set[int]] = [set(parents) for parents in original]
    edges = [(parent, child) for child, parents in enumerate(original) for parent in parents]
    edge_set = set(edges)
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
    max_target = targets[-1]
    max_attempts = max(max_target, edge_count * MAX_ATTEMPTS_PER_EDGE)
    attempts = 0
    accepted = 0
    states: Dict[int, Tuple[Tuple[int, ...], ...]] = {}
    audits: Dict[int, Dict[str, Any]] = {}

    while attempts < max_attempts and accepted < max_target and eligible:
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
        if accepted in targets:
            state = tuple(tuple(sorted(parents)) for parents in predecessors)
            structure = v16t.final_structure_audit(dag, metadata, state)
            states[accepted] = state
            audits[accepted] = {
                "target_accepted_swaps": accepted,
                "accepted_swaps": accepted,
                "attempted_swaps": attempts,
                "attempts_per_edge": attempts / edge_count,
                "acceptance_rate": accepted / attempts if attempts else 0.0,
                "eligible_edge_count": len(eligible),
                "eligible_edge_fraction": len(eligible) / edge_count,
                "footprint_bucket_count": len(buckets),
                "movable_footprint_bucket_count": sum(
                    len(indices) >= 2 for indices in buckets.values()
                ),
                **structure,
                "target_exact_pass": 1,
                "completion_pass": 1,
            }

    final_state = tuple(tuple(sorted(parents)) for parents in predecessors)
    for target in targets:
        if target in states:
            continue
        structure = v16t.final_structure_audit(dag, metadata, final_state)
        states[target] = final_state
        audits[target] = {
            "target_accepted_swaps": target,
            "accepted_swaps": accepted,
            "attempted_swaps": attempts,
            "attempts_per_edge": attempts / edge_count,
            "acceptance_rate": accepted / attempts if attempts else 0.0,
            "eligible_edge_count": len(eligible),
            "eligible_edge_fraction": len(eligible) / edge_count,
            "footprint_bucket_count": len(buckets),
            "movable_footprint_bucket_count": sum(
                len(indices) >= 2 for indices in buckets.values()
            ),
            **structure,
            "target_exact_pass": 0,
            "completion_pass": 0,
        }
    return states, audits


def run_replicate(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
    replicate: int,
) -> Tuple[Dict[str, Tuple[Tuple[int, ...], ...]], Dict[str, Dict[str, Any]], Dict[str, Any]]:
    burnin_seed = v16i.stable_seed("v16u", "burnin", *dag.key, replicate)
    burnin, burnin_stage = v16q.footprint_rewire(
        dag,
        metadata,
        burnin_seed,
        target_swap_multiplier=BURNIN_SWAP_MULTIPLIER,
        max_attempts_per_edge=MAX_ATTEMPTS_PER_EDGE,
    )
    burnin_source_audit = v16t.final_structure_audit(dag, metadata, burnin)
    edge_count = int(burnin_source_audit["edge_count"])
    k_swaps = max(1, math.ceil(edge_count * K_ACCEPTED_SWAPS_PER_EDGE))
    burnin_dag = with_predecessors(dag, burnin)

    direct_seed = v16i.stable_seed("v16u", "direct_prefix_stream", *dag.key, replicate, k_swaps)
    direct_states, direct_audits = exact_footprint_path(
        burnin_dag, metadata, direct_seed, (k_swaps, 2 * k_swaps)
    )
    direct_k = direct_states[k_swaps]
    direct_2k = direct_states[2 * k_swaps]

    staged_seed = v16i.stable_seed("v16u", "staged_reset_stream", *dag.key, replicate, k_swaps)
    staged_start_dag = with_predecessors(dag, direct_k)
    staged_states, staged_audits = exact_footprint_path(
        staged_start_dag, metadata, staged_seed, (k_swaps,)
    )
    staged_2k = staged_states[k_swaps]

    states = {
        "burnin": burnin,
        "direct_plus_k": direct_k,
        "direct_plus_2k": direct_2k,
        "staged_plus_k_plus_k": staged_2k,
    }
    direct_k_audit = direct_audits[k_swaps]
    direct_2k_audit = direct_audits[2 * k_swaps]
    staged_second_audit = staged_audits[k_swaps]
    prefix_digest = v16j.edge_digest(direct_k)
    staged_prefix_digest = v16j.edge_digest(staged_start_dag.predecessors)
    prefix_reuse_pass = int(prefix_digest == staged_prefix_digest)
    burnin_pass = int(
        int(burnin_stage["completion_and_change_pass"])
        and int(burnin_source_audit["structure_pass"])
        and float(burnin_source_audit["changed_edge_fraction"]) >= MIN_CHANGED_EDGE_FRACTION
    )
    direct_k_pass = int(
        int(direct_k_audit["target_exact_pass"])
        and int(direct_k_audit["structure_pass"])
    )
    direct_2k_pass = int(
        int(direct_2k_audit["target_exact_pass"])
        and int(direct_2k_audit["structure_pass"])
    )
    staged_pass = int(
        direct_k_pass
        and int(staged_second_audit["target_exact_pass"])
        and int(staged_second_audit["structure_pass"])
    )
    staged_total_accepted = int(direct_k_audit["accepted_swaps"]) + int(
        staged_second_audit["accepted_swaps"]
    )
    matched_effort_pass = int(
        direct_2k_pass
        and staged_pass
        and int(direct_2k_audit["accepted_swaps"]) == 2 * k_swaps
        and staged_total_accepted == 2 * k_swaps
    )

    audits: Dict[str, Dict[str, Any]] = {}
    protocol_details = {
        "burnin": {
            "incremental_target_swaps": 0,
            "incremental_accepted_swaps": 0,
            "incremental_attempted_swaps": 0,
            "segment_1_target_swaps": 0,
            "segment_1_accepted_swaps": 0,
            "segment_2_target_swaps": 0,
            "segment_2_accepted_swaps": 0,
            "incremental_changed_edge_fraction": 0.0,
            "exact_effort_pass": burnin_pass,
        },
        "direct_plus_k": {
            "incremental_target_swaps": k_swaps,
            "incremental_accepted_swaps": direct_k_audit["accepted_swaps"],
            "incremental_attempted_swaps": direct_k_audit["attempted_swaps"],
            "segment_1_target_swaps": k_swaps,
            "segment_1_accepted_swaps": direct_k_audit["accepted_swaps"],
            "segment_2_target_swaps": 0,
            "segment_2_accepted_swaps": 0,
            "incremental_changed_edge_fraction": direct_k_audit["changed_edge_fraction"],
            "exact_effort_pass": direct_k_pass,
        },
        "direct_plus_2k": {
            "incremental_target_swaps": 2 * k_swaps,
            "incremental_accepted_swaps": direct_2k_audit["accepted_swaps"],
            "incremental_attempted_swaps": direct_2k_audit["attempted_swaps"],
            "segment_1_target_swaps": 2 * k_swaps,
            "segment_1_accepted_swaps": direct_2k_audit["accepted_swaps"],
            "segment_2_target_swaps": 0,
            "segment_2_accepted_swaps": 0,
            "incremental_changed_edge_fraction": direct_2k_audit["changed_edge_fraction"],
            "exact_effort_pass": direct_2k_pass,
        },
        "staged_plus_k_plus_k": {
            "incremental_target_swaps": 2 * k_swaps,
            "incremental_accepted_swaps": staged_total_accepted,
            "incremental_attempted_swaps": int(direct_k_audit["attempted_swaps"])
            + int(staged_second_audit["attempted_swaps"]),
            "segment_1_target_swaps": k_swaps,
            "segment_1_accepted_swaps": direct_k_audit["accepted_swaps"],
            "segment_2_target_swaps": k_swaps,
            "segment_2_accepted_swaps": staged_second_audit["accepted_swaps"],
            "incremental_changed_edge_fraction": v16t.final_structure_audit(
                burnin_dag, metadata, staged_2k
            )["changed_edge_fraction"],
            "exact_effort_pass": staged_pass,
        },
    }
    for protocol, state in states.items():
        source_audit = v16t.final_structure_audit(dag, metadata, state)
        details = protocol_details[protocol]
        total_accepted = int(burnin_stage["accepted_swaps"]) + int(
            details["incremental_accepted_swaps"]
        )
        audits[protocol] = {
            **dag.prefix,
            "protocol": protocol,
            "null_replicate": replicate,
            "burnin_seed": burnin_seed,
            "direct_prefix_seed": direct_seed,
            "staged_reset_seed": staged_seed,
            "edge_count": edge_count,
            "k_accepted_swaps": k_swaps,
            "burnin_target_accepted_swaps": burnin_stage["target_accepted_swaps"],
            "burnin_accepted_swaps": burnin_stage["accepted_swaps"],
            "burnin_attempted_swaps": burnin_stage["attempted_swaps"],
            "burnin_changed_edge_fraction": burnin_source_audit["changed_edge_fraction"],
            "burnin_pass": burnin_pass,
            **details,
            "total_accepted_swaps_since_source": total_accepted,
            "direct_k_prefix_edge_sha256": prefix_digest,
            "staged_k_prefix_edge_sha256": staged_prefix_digest,
            "path_prefix_reuse_pass": prefix_reuse_pass,
            "matched_direct_staged_effort_pass": matched_effort_pass,
            "final_changed_edge_fraction_from_source": source_audit["changed_edge_fraction"],
            "final_structure_pass": source_audit["structure_pass"],
            "null_edge_sha256": source_audit["null_edge_sha256"],
        }

    effort = {
        **dag.prefix,
        "null_replicate": replicate,
        "edge_count": edge_count,
        "k_accepted_swaps": k_swaps,
        "burnin_accepted_swaps": burnin_stage["accepted_swaps"],
        "burnin_changed_edge_fraction": burnin_source_audit["changed_edge_fraction"],
        "direct_plus_k_accepted_swaps": direct_k_audit["accepted_swaps"],
        "direct_plus_2k_accepted_swaps": direct_2k_audit["accepted_swaps"],
        "staged_segment_1_accepted_swaps": direct_k_audit["accepted_swaps"],
        "staged_segment_2_accepted_swaps": staged_second_audit["accepted_swaps"],
        "staged_total_accepted_swaps": staged_total_accepted,
        "direct_staged_effort_difference": int(direct_2k_audit["accepted_swaps"])
        - staged_total_accepted,
        "burnin_pass": burnin_pass,
        "direct_plus_k_exact_pass": direct_k_pass,
        "direct_plus_2k_exact_pass": direct_2k_pass,
        "staged_k_plus_k_exact_pass": staged_pass,
        "path_prefix_reuse_pass": prefix_reuse_pass,
        "matched_effort_pass": matched_effort_pass,
    }
    return states, audits, effort


def run_products(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    products: Dict[str, List[Dict[str, Any]]] = {label: [] for label in PROTOCOLS}
    audits: Dict[str, List[Dict[str, Any]]] = {label: [] for label in PROTOCOLS}
    effort_rows: List[Dict[str, Any]] = []
    for replicate in range(REPLICATES):
        states, replicate_audits, effort = run_replicate(dag, metadata, replicate)
        effort_rows.append(effort)
        for protocol in PROTOCOLS:
            products[protocol].append(v16i.interval_spectrum(states[protocol]))
            audits[protocol].append(replicate_audits[protocol])

    null_rows: List[Dict[str, Any]] = []
    audit_rows: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []
    for protocol in PROTOCOLS:
        protocol_products = products[protocol]
        protocol_audits = audits[protocol]
        unique_count = len({row["null_edge_sha256"] for row in protocol_audits})
        unique_fraction = unique_count / REPLICATES
        spectra = [row["probabilities"] for row in protocol_products]
        center = v16i.mean_spectrum(spectra)
        leave_one_out = [
            v16i.jensen_shannon(spectrum, v16i.mean_spectrum(spectra, skip=index))
            for index, spectrum in enumerate(spectra)
        ]
        for replicate, (product, audit) in enumerate(zip(protocol_products, protocol_audits)):
            audit["run_unique_null_count"] = unique_count
            audit["run_unique_null_fraction"] = unique_fraction
            audit["run_uniqueness_pass"] = int(unique_fraction >= MIN_UNIQUE_NULL_FRACTION)
            audit["perturbation_integrity_pass"] = int(
                int(audit["burnin_pass"])
                and int(audit["exact_effort_pass"])
                and int(audit["final_structure_pass"])
                and int(audit["run_uniqueness_pass"])
            )
            audit_rows.append(audit)
            null_rows.append({
                **dag.prefix,
                "protocol": protocol,
                "null_replicate": replicate,
                "null_edge_sha256": audit["null_edge_sha256"],
                "comparable_pairs": product["comparable_pairs"],
                "leave_one_out_js": leave_one_out[replicate],
                "mean_open_volume": product["mean_open_volume"],
                "tail_mass_ge_8": product["tail_mass_ge_8"],
                "spectrum_entropy": product["spectrum_entropy"],
                **{
                    f"prob_{label}": product["probabilities"][index]
                    for index, (label, _, _) in enumerate(v16i.INTERVAL_BINS)
                },
            })
        summaries.append({
            **dag.prefix,
            "protocol": protocol,
            "null_replicates": REPLICATES,
            "mean_k_accepted_swaps": v16i.mean(float(row["k_accepted_swaps"]) for row in protocol_audits),
            "mean_burnin_accepted_swaps": v16i.mean(
                float(row["burnin_accepted_swaps"]) for row in protocol_audits
            ),
            "mean_incremental_accepted_swaps": v16i.mean(
                float(row["incremental_accepted_swaps"]) for row in protocol_audits
            ),
            "min_incremental_accepted_swaps": min(
                int(row["incremental_accepted_swaps"]) for row in protocol_audits
            ),
            "max_incremental_accepted_swaps": max(
                int(row["incremental_accepted_swaps"]) for row in protocol_audits
            ),
            "median_leave_one_out_js": v16i.median(leave_one_out),
            "mean_open_volume": v16i.mean(row["mean_open_volume"] for row in protocol_products),
            "mean_tail_mass_ge_8": v16i.mean(row["tail_mass_ge_8"] for row in protocol_products),
            "min_burnin_changed_edge_fraction": min(
                float(row["burnin_changed_edge_fraction"]) for row in protocol_audits
            ),
            "unique_null_fraction": unique_fraction,
            "all_perturbation_integrity_pass": int(
                all(int(row["perturbation_integrity_pass"]) for row in protocol_audits)
            ),
            **{
                f"center_prob_{label}": center[index]
                for index, (label, _, _) in enumerate(v16i.INTERVAL_BINS)
            },
        })
    return null_rows, audit_rows, effort_rows, summaries


def comparison_rows(
    null_rows: Sequence[Mapping[str, Any]],
    runs: Sequence[v16i.RunDAG],
) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[Tuple[int, int, str, int], str], List[Mapping[str, Any]]] = defaultdict(list)
    for row in null_rows:
        grouped[(v16i.run_key(row), str(row["protocol"]))].append(row)
    probability_fields = [f"prob_{label}" for label, _, _ in v16i.INTERVAL_BINS]
    rows: List[Dict[str, Any]] = []
    for dag in runs:
        for comparison, left_label, right_label, gate_family in COMPARISONS:
            left = sorted(grouped[(dag.key, left_label)], key=lambda row: int(row["null_replicate"]))
            right = sorted(grouped[(dag.key, right_label)], key=lambda row: int(row["null_replicate"]))
            if len(left) != REPLICATES or len(right) != REPLICATES:
                raise ValueError("v16u incomplete null ensemble")
            left_spectra = [[float(row[field]) for field in probability_fields] for row in left]
            right_spectra = [[float(row[field]) for field in probability_fields] for row in right]
            left_center = v16i.mean_spectrum(left_spectra)
            right_center = v16i.mean_spectrum(right_spectra)
            center_js = v16i.jensen_shannon(left_center, right_center)
            pooled_dispersion = v16i.median([
                *(float(row["leave_one_out_js"]) for row in left),
                *(float(row["leave_one_out_js"]) for row in right),
            ])
            ratio = center_js / max(pooled_dispersion, v16j.EPSILON)
            rows.append({
                **dag.prefix,
                "comparison": comparison,
                "gate_family": gate_family,
                "left_protocol": left_label,
                "right_protocol": right_label,
                "center_jensen_shannon": center_js,
                "pooled_median_leave_one_out_js": pooled_dispersion,
                "center_shift_ratio": ratio,
                "max_absolute_bin_delta": max(
                    abs(left_value - right_value)
                    for left_value, right_value in zip(left_center, right_center)
                ),
                "threshold": MAX_CENTER_SHIFT_RATIO,
                "stability_pass": int(ratio <= MAX_CENTER_SHIFT_RATIO),
            })
    return rows


def build_report(
    summaries: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16u matched-effort footprint-null stability gate",
        "",
        f"Status: `{overall}`.",
        "",
        "V16u repairs the known v16t realized-effort confound. It is effect-blind: only rewired null DAG spectra are computed; source spectra and observed/null effect metrics are excluded.",
        "",
        f"Specification digest: `{spec_digest()}`.",
        "",
        "## Frozen design",
        "",
        f"Each of the six frozen v16s DAGs has `{REPLICATES}` shared burn-in replicates. Burn-in uses the qualified footprint sampler until at least `{MIN_CHANGED_EDGE_FRACTION:.3f}` of source edges differ. From each frozen burn-in state, `K = ceil(0.100 * source edge count)` accepted swaps are used as the exact effort unit.",
        "",
        "The direct path records exact `+K` and `+2K` checkpoints from one RNG stream. The staged path branches from the exact same `+K` checkpoint, resets the RNG stream, and advances exactly another `+K`. Direct and staged endpoints therefore both contain exactly `+2K` accepted swaps after an identical prefix.",
        "",
        f"A center comparison passes when Jensen-Shannon center shift is at most `{MAX_CENTER_SHIFT_RATIO}` times pooled median leave-one-out dispersion. Every source DAG must pass.",
        "",
        "## Protocol summaries",
        "",
    ]
    lines.extend(v16i.table(summaries, (
        "growth_seed", "run_offset", "protocol", "mean_k_accepted_swaps",
        "mean_burnin_accepted_swaps", "mean_incremental_accepted_swaps",
        "median_leave_one_out_js", "min_burnin_changed_edge_fraction",
        "all_perturbation_integrity_pass",
    )))
    lines.extend(["", "## Null-center comparisons", ""])
    lines.extend(v16i.table(comparisons, (
        "growth_seed", "run_offset", "comparison", "center_jensen_shannon",
        "pooled_median_leave_one_out_js", "center_shift_ratio", "stability_pass",
    )))
    lines.extend(["", "## Gates", ""])
    lines.extend(v16i.table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Evidential boundary",
        "",
        "A pass supports null-center stability under the tested exact realized lengths and prefix-matched segmentation. It does not prove irreducibility, mixing time, convergence, stationarity, independence, representativeness, uniform sampling, or independence from every alternative null construction.",
        "",
        "V16u does not re-evaluate the v16s observed spectrum contrast. It establishes no dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particle, entanglement, invariant, or physical law.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    verify_frozen_sources()
    loaded = load_runs()
    null_rows: List[Dict[str, Any]] = []
    audit_rows: List[Dict[str, Any]] = []
    effort_rows: List[Dict[str, Any]] = []
    summaries: List[Dict[str, Any]] = []
    for run_index, (dag, metadata) in enumerate(loaded, start=1):
        products, audits, efforts, run_summaries = run_products(dag, metadata)
        null_rows.extend(products)
        audit_rows.extend(audits)
        effort_rows.extend(efforts)
        summaries.extend(run_summaries)
        print(f"[v16u] source_runs={run_index}/{len(loaded)} replicates={REPLICATES}")

    comparisons = comparison_rows(null_rows, [dag for dag, _ in loaded])
    expected_outputs = len(loaded) * len(PROTOCOLS) * REPLICATES
    expected_efforts = len(loaded) * REPLICATES
    source_pass = len(loaded) == 6
    integrity_pass = (
        len(audit_rows) == expected_outputs
        and all(int(row["perturbation_integrity_pass"]) for row in audit_rows)
    )
    exact_effort_pass = (
        len(effort_rows) == expected_efforts
        and all(
            int(row["direct_plus_k_exact_pass"])
            and int(row["direct_plus_2k_exact_pass"])
            and int(row["staged_k_plus_k_exact_pass"])
            for row in effort_rows
        )
    )
    matched_effort_pass = (
        len(effort_rows) == expected_efforts
        and all(int(row["matched_effort_pass"]) for row in effort_rows)
    )
    prefix_pass = (
        len(effort_rows) == expected_efforts
        and all(int(row["path_prefix_reuse_pass"]) for row in effort_rows)
    )
    length_rows = [row for row in comparisons if row["gate_family"] == "realized_length"]
    path_rows = [row for row in comparisons if row["gate_family"] == "path_segmentation"]
    length_pass = len(length_rows) == 18 and all(int(row["stability_pass"]) for row in length_rows)
    path_pass = len(path_rows) == 6 and all(int(row["stability_pass"]) for row in path_rows)
    if not source_pass or not integrity_pass:
        overall = "v16u_matched_effort_instrumentation_failed"
    elif not exact_effort_pass or not matched_effort_pass or not prefix_pass:
        overall = "v16u_matched_effort_design_not_realized"
    elif not length_pass:
        overall = "v16u_footprint_null_center_exact_length_unstable"
    elif not path_pass:
        overall = "v16u_footprint_null_center_matched_path_dependent"
    else:
        overall = "v16u_footprint_null_centers_stable_under_exact_matched_effort"

    gates = [
        {
            "gate": "frozen_source_integrity",
            "status": "pass" if source_pass else "fail",
            "observed": f"source_dags={len(loaded)}",
            "required": "source_dags=6",
            "decision": "continue" if source_pass else "repair",
        },
        {
            "gate": "all_protocol_perturbation_integrity",
            "status": "pass" if integrity_pass else "fail",
            "observed": f"{sum(int(row['perturbation_integrity_pass']) for row in audit_rows)}/{len(audit_rows)}",
            "required": f"{expected_outputs}/{expected_outputs}",
            "decision": "continue" if integrity_pass else "instrumentation_failed",
        },
        {
            "gate": "exact_increment_realization",
            "status": "pass" if exact_effort_pass else "fail",
            "observed": f"{sum(int(row['direct_plus_k_exact_pass']) and int(row['direct_plus_2k_exact_pass']) and int(row['staged_k_plus_k_exact_pass']) for row in effort_rows)}/{len(effort_rows)}",
            "required": f"{expected_efforts}/{expected_efforts}",
            "decision": "continue" if exact_effort_pass else "instrumentation_failed",
        },
        {
            "gate": "direct_staged_matched_effort",
            "status": "pass" if matched_effort_pass else "fail",
            "observed": f"{sum(int(row['matched_effort_pass']) for row in effort_rows)}/{len(effort_rows)};max_abs_difference={max((abs(int(row['direct_staged_effort_difference'])) for row in effort_rows), default=-1)}",
            "required": f"{expected_efforts}/{expected_efforts};difference=0",
            "decision": "continue" if matched_effort_pass else "instrumentation_failed",
        },
        {
            "gate": "shared_k_prefix",
            "status": "pass" if prefix_pass else "fail",
            "observed": f"{sum(int(row['path_prefix_reuse_pass']) for row in effort_rows)}/{len(effort_rows)}",
            "required": f"{expected_efforts}/{expected_efforts}",
            "decision": "continue" if prefix_pass else "instrumentation_failed",
        },
        {
            "gate": "exact_realized_length_null_center_stability",
            "status": "pass" if length_pass else "fail",
            "observed": f"{sum(int(row['stability_pass']) for row in length_rows)}/{len(length_rows)};max_ratio={max((float(row['center_shift_ratio']) for row in length_rows), default=float('nan')):.6f}",
            "required": f"18/18;ratio<={MAX_CENTER_SHIFT_RATIO}",
            "decision": "stable" if length_pass else "procedure_conditional",
        },
        {
            "gate": "matched_effort_path_segmentation_stability",
            "status": "pass" if path_pass else "fail",
            "observed": f"{sum(int(row['stability_pass']) for row in path_rows)}/{len(path_rows)};max_ratio={max((float(row['center_shift_ratio']) for row in path_rows), default=float('nan')):.6f}",
            "required": f"6/6;ratio<={MAX_CENTER_SHIFT_RATIO}",
            "decision": "stable" if path_pass else "procedure_conditional",
        },
        {
            "gate": "observed_spectrum_and_effect_exclusion",
            "status": "pass",
            "observed": "source_spectra=0;observed_effect_metrics=0",
            "required": "0;0",
            "decision": "effect_blind",
        },
        {
            "gate": "v16u_overall",
            "status": overall,
            "observed": f"integrity={int(integrity_pass)};effort={int(matched_effort_pass)};length={int(length_pass)};path={int(path_pass)}",
            "required": "1;1;1;1",
            "decision": overall,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "The v16u direct +2K and staged +K+K endpoints used exactly matched accepted-swap effort after an identical K prefix.",
            "status": "supported" if matched_effort_pass and prefix_pass else "unsupported",
            "evidence": "v16u_realized_effort_audit.csv",
            "scope_limit": "six frozen finite source DAGs and sixteen branches each",
        },
        {
            "claim_id": "C2",
            "claim": "The event-footprint null center is stable across burn-in, exact +K, exact +2K, and prefix-matched +K+K under the frozen ratio gate.",
            "status": "supported" if length_pass and path_pass else "not_supported",
            "evidence": "v16u_null_center_comparison.csv;v16u_gate_evaluation.csv",
            "scope_limit": "tested effort range, finite null ensembles, and this local switch family",
        },
        {
            "claim_id": "C3",
            "claim": "The v16s observed spectrum contrast was replicated or re-evaluated in v16u.",
            "status": "not_evaluated",
            "evidence": "v16u_gate_evaluation.csv",
            "scope_limit": "source spectra and observed-effect metrics were excluded",
        },
        {
            "claim_id": "C4",
            "claim": "The footprint sampler is irreducible, mixed, converged, stationary, representative, or uniform.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "finite center stability is not a Markov-chain proof",
        },
        {
            "claim_id": "C5",
            "claim": "Dimension, Lorentz symmetry, spacetime, particles, entanglement, invariants, or physical laws were established.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "null-sampler instrumentation only",
        },
    ]
    v16i.write_csv(NULL_DISTRIBUTION, null_rows)
    v16i.write_csv(PERTURBATION_AUDIT, audit_rows)
    v16i.write_csv(REALIZED_EFFORT_AUDIT, effort_rows)
    v16i.write_csv(PROTOCOL_SUMMARY, summaries)
    v16i.write_csv(CENTER_COMPARISON, comparisons)
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    REPORT.write_text(build_report(summaries, comparisons, gates, overall), encoding="utf-8")
    next_step = (
        "construct_and_qualify_an_independent_effect_blind_event_dag_null_family"
        if overall == "v16u_footprint_null_centers_stable_under_exact_matched_effort"
        else "repair_or_retire_the_procedure_conditional_footprint_null_before_effect_work"
    )
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.16u\n\n"
        f"Status: `{overall}`.\n\n"
        f"Next: `{next_step}`.\n\n"
        "V16u is effect-blind. It tests exact realized null-sampler effort, not the observed v16s effect and not physical geometry.\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.16u\n\n"
        f"Statusen er `{overall}`. Denne runden starter flere kontrollforlop fra noyaktig samme oppvarmede tilstand og gir dem noyaktig like mange godkjente endringer. Dermed kan vi skille faktisk kjorelengde fra et stoppkriterium som forstyrret v16t. Runden tester fortsatt bare kontrollgeneratoren, ikke om signalet er fysikk.\n",
        encoding="utf-8",
    )
    print(f"[v16u] complete overall={overall}")


def verify_outputs() -> None:
    verify_frozen_sources()
    nulls = v16i.read_csv(NULL_DISTRIBUTION)
    audits = v16i.read_csv(PERTURBATION_AUDIT)
    efforts = v16i.read_csv(REALIZED_EFFORT_AUDIT)
    summaries = v16i.read_csv(PROTOCOL_SUMMARY)
    comparisons = v16i.read_csv(CENTER_COMPARISON)
    gates = v16i.read_csv(GATE_EVALUATION)
    expected_outputs = 6 * len(PROTOCOLS) * REPLICATES
    expected_efforts = 6 * REPLICATES
    if len(nulls) != expected_outputs or len(audits) != expected_outputs:
        raise ValueError("v16u null or perturbation-audit row count failed")
    if len(efforts) != expected_efforts:
        raise ValueError("v16u effort-audit row count failed")
    if len(summaries) != 6 * len(PROTOCOLS) or len(comparisons) != 6 * len(COMPARISONS):
        raise ValueError("v16u summary or comparison row count failed")
    null_keys = {
        (v16i.run_key(row), row["protocol"], int(row["null_replicate"])) for row in nulls
    }
    audit_keys = {
        (v16i.run_key(row), row["protocol"], int(row["null_replicate"])) for row in audits
    }
    if null_keys != audit_keys or len(null_keys) != expected_outputs:
        raise ValueError("v16u null/audit identity mismatch")
    if any(int(row["direct_staged_effort_difference"]) != 0 for row in efforts):
        raise ValueError("v16u direct/staged effort mismatch")
    if any(
        int(row["direct_plus_2k_accepted_swaps"]) != 2 * int(row["k_accepted_swaps"])
        or int(row["staged_total_accepted_swaps"]) != 2 * int(row["k_accepted_swaps"])
        for row in efforts
    ):
        raise ValueError("v16u exact 2K realization failed")
    exclusion = next(row for row in gates if row["gate"] == "observed_spectrum_and_effect_exclusion")
    if exclusion["status"] != "pass" or exclusion["observed"] != "source_spectra=0;observed_effect_metrics=0":
        raise ValueError("v16u effect-blind exclusion failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16u_overall")
    allowed = {
        "v16u_matched_effort_instrumentation_failed",
        "v16u_matched_effort_design_not_realized",
        "v16u_footprint_null_center_exact_length_unstable",
        "v16u_footprint_null_center_matched_path_dependent",
        "v16u_footprint_null_centers_stable_under_exact_matched_effort",
    }
    if overall not in allowed:
        raise ValueError("v16u unknown overall status")
    print(f"[v16u] output verification pass overall={overall}")


def self_test() -> None:
    if REPLICATES != 16 or MAX_ATTEMPTS_PER_EDGE != 240:
        raise AssertionError("v16u frozen budget changed")
    if BURNIN_SWAP_MULTIPLIER != 0.100 or K_ACCEPTED_SWAPS_PER_EDGE != 0.100:
        raise AssertionError("v16u burn-in or K definition changed")
    if len(PROTOCOLS) != 4 or len(COMPARISONS) != 4:
        raise AssertionError("v16u protocol matrix changed")
    if MAX_CENTER_SHIFT_RATIO != 2.0:
        raise AssertionError("v16u frozen threshold changed")
    if math.ceil(3523 * K_ACCEPTED_SWAPS_PER_EDGE) != 353:
        raise AssertionError("v16u K formula failed")
    payload = spec_payload()
    if payload["source_spectrum_computation_allowed"] or payload["observed_effect_computation_allowed"]:
        raise AssertionError("v16u effect-blind exclusion changed")
    if payload["path_isolation"] != "direct_2k_and_staged_k_plus_k_share_the_exact_k_prefix":
        raise AssertionError("v16u path isolation changed")
    print("[v16u] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16u matched-effort footprint-null stability gate")
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
