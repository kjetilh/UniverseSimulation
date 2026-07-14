#!/usr/bin/env python3
"""v16p: exact reachability audit for an event-side footprint null.

The audit groups direct edges by the source event's write footprint and the
target event's read footprint, then enumerates every within-bucket edge pair.
It performs no rewiring and computes no interval spectrum.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Set, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16j_interval_strict_null_gate as v16j
import relational_universe_v16n_coarse_event_resource_null_calibration as v16n
import relational_universe_v16o_event_resource_reachability_audit as v16o


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"
MIN_PROMISING_LEGAL_EDGE_FRACTION = 0.10
SAMPLE_LEGAL_PAIRS_PER_RUN = 32

SOURCE_CHAIN = DOC / "v16p_source_chain.csv"
PRE_REGISTRATION = DOC / "v16p_pre_registration.csv"
BUCKET_SUMMARY = DOC / "v16p_footprint_bucket_summary.csv"
RUN_SUMMARY = DOC / "v16p_reachability_run_summary.csv"
REJECTION_COUNTS = DOC / "v16p_rejection_counts.csv"
LEGAL_PAIR_SAMPLES = DOC / "v16p_legal_pair_samples.csv"
GATE_EVALUATION = DOC / "v16p_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16p_claim_ledger.csv"
REPORT = DOC / "v16p_event_footprint_reachability_audit.md"
RECOMMENDATION = DOC / "v0_16p_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16p.md"

Role = Tuple[str, Tuple[str, ...]]
Footprint = Tuple[Role, Role]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = [
        ("v16n", "calibration_events", v16n.EVENT_LOG),
        ("v16n", "calibration_edges", v16n.EDGE_LOG),
        ("v16o", "source_loader_and_exact_audit", Path(v16o.__file__)),
        ("v16o", "actual_conflict_reachability", v16o.RUN_SUMMARY),
        ("v16o", "gate_evaluation", v16o.GATE_EVALUATION),
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
        "gate": "v16p_event_footprint_reachability_audit",
        "purpose_ref": PURPOSE_REF,
        "source": "six_v16n_calibration_dags",
        "source_role": "event_family_plus_write_namespace_set",
        "target_role": "event_family_plus_read_namespace_set",
        "proposal": "double_edge_swap_within_equal_source_target_role_bucket",
        "concrete_resource_overlap_required": False,
        "rejection_order": [
            "same_parent_or_child",
            "scheduler_order",
            "duplicate_edge",
            "global_dyadic_age_bin_multiset",
            "exact_child_depth",
            "legal",
        ],
        "minimum_promising_legal_edge_fraction": MIN_PROMISING_LEGAL_EDGE_FRACTION,
        "sample_legal_pairs_per_run": SAMPLE_LEGAL_PAIRS_PER_RUN,
        "spectrum_computation_allowed": False,
        "rewiring_allowed": False,
    }


def spec_digest() -> str:
    raw = json.dumps(spec_payload(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def prepare() -> None:
    v16o.verify_outputs()
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [{
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "script_sha256": file_sha256(SCRIPT),
        "source_chain_sha256": file_sha256(SOURCE_CHAIN),
        "source_run_count": len(v16n.assignments()),
        "minimum_promising_legal_edge_fraction": MIN_PROMISING_LEGAL_EDGE_FRACTION,
        "spectrum_computation_allowed": 0,
        "rewiring_allowed": 0,
    }])
    print(f"[v16p] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    rows = v16i.read_csv(PRE_REGISTRATION)
    if len(rows) != 1:
        raise ValueError("v16p preregistration row count failed")
    expected = {
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "script_sha256": file_sha256(SCRIPT),
        "source_chain_sha256": file_sha256(SOURCE_CHAIN),
        "source_run_count": str(len(v16n.assignments())),
        "minimum_promising_legal_edge_fraction": str(MIN_PROMISING_LEGAL_EDGE_FRACTION),
        "spectrum_computation_allowed": "0",
        "rewiring_allowed": "0",
    }
    if rows[0] != expected:
        raise ValueError("v16p preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v16p source chain changed")


def namespace_mask(resources: Sequence[str]) -> Tuple[str, ...]:
    namespaces = tuple(sorted({v16n.resource_namespace(resource) for resource in resources}))
    return namespaces or ("none",)


def source_role(event: Mapping[str, Any]) -> Role:
    return str(event["family"]), namespace_mask(event["writes"])


def target_role(event: Mapping[str, Any]) -> Role:
    return str(event["family"]), namespace_mask(event["reads"])


def edge_footprint(parent: int, child: int, metadata: Sequence[Mapping[str, Any]]) -> Footprint:
    return source_role(metadata[parent]), target_role(metadata[child])


def role_text(role: Role) -> str:
    return f"{role[0]}[{'&'.join(role[1])}]"


def footprint_text(footprint: Footprint) -> str:
    return f"{role_text(footprint[0])}->{role_text(footprint[1])}"


def candidate_reason(
    first: Tuple[int, int],
    second: Tuple[int, int],
    edge_set: Set[Tuple[int, int]],
    predecessors: Sequence[Sequence[int]],
    depths: Sequence[int],
) -> str:
    parent_a, child_b = first
    parent_c, child_d = second
    if parent_a == parent_c or child_b == child_d:
        return "same_parent_or_child"
    new_first = (parent_a, child_d)
    new_second = (parent_c, child_b)
    if parent_a >= child_d or parent_c >= child_b:
        return "scheduler_order"
    if new_first in edge_set or new_second in edge_set or new_first == new_second:
        return "duplicate_edge"
    old_bins = sorted((v16j.lag_bin(parent_a, child_b), v16j.lag_bin(parent_c, child_d)))
    new_bins = sorted((v16j.lag_bin(parent_a, child_d), v16j.lag_bin(parent_c, child_b)))
    if old_bins != new_bins:
        return "global_dyadic_age_bin_multiset"
    next_b = (set(predecessors[child_b]) - {parent_a}) | {parent_c}
    next_d = (set(predecessors[child_d]) - {parent_c}) | {parent_a}
    if (
        not next_b
        or not next_d
        or max(depths[parent] for parent in next_b) != depths[child_b] - 1
        or max(depths[parent] for parent in next_d) != depths[child_d] - 1
    ):
        return "exact_child_depth"
    return "legal"


def audit_run(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    edges = [(parent, child) for child, parents in enumerate(dag.predecessors) for parent in parents]
    edge_set = set(edges)
    buckets: Dict[Footprint, List[int]] = defaultdict(list)
    for index, (parent, child) in enumerate(edges):
        buckets[edge_footprint(parent, child, metadata)].append(index)

    counts: Counter[str] = Counter()
    legal_edges: Set[int] = set()
    samples: List[Dict[str, Any]] = []
    bucket_rows: List[Dict[str, Any]] = []
    for footprint in sorted(buckets):
        indices = buckets[footprint]
        bucket_counts: Counter[str] = Counter()
        bucket_legal_edges: Set[int] = set()
        for first_position in range(len(indices) - 1):
            first_index = indices[first_position]
            first = edges[first_index]
            for second_position in range(first_position + 1, len(indices)):
                second_index = indices[second_position]
                second = edges[second_index]
                reason = candidate_reason(first, second, edge_set, dag.predecessors, dag.depths)
                counts[reason] += 1
                bucket_counts[reason] += 1
                if reason == "legal":
                    legal_edges.update((first_index, second_index))
                    bucket_legal_edges.update((first_index, second_index))
                    if len(samples) < SAMPLE_LEGAL_PAIRS_PER_RUN:
                        samples.append({
                            **dag.prefix,
                            "footprint": footprint_text(footprint),
                            "first_edge_index": first_index,
                            "second_edge_index": second_index,
                            "old_first_edge": f"{first[0]}>{first[1]}",
                            "old_second_edge": f"{second[0]}>{second[1]}",
                            "new_first_edge": f"{first[0]}>{second[1]}",
                            "new_second_edge": f"{second[0]}>{first[1]}",
                        })
        pair_count = math.comb(len(indices), 2)
        bucket_rows.append({
            **dag.prefix,
            "footprint": footprint_text(footprint),
            "edge_count": len(indices),
            "candidate_pair_count": pair_count,
            "legal_pair_count": bucket_counts["legal"],
            "legal_edge_count": len(bucket_legal_edges),
            "legal_edge_fraction": len(bucket_legal_edges) / len(indices),
        })

    eligible_edges = {index for indices in buckets.values() if len(indices) >= 2 for index in indices}
    candidate_pairs = sum(math.comb(len(indices), 2) for indices in buckets.values())
    summary = {
        **dag.prefix,
        "edge_count": len(edges),
        "footprint_bucket_count": len(buckets),
        "movable_footprint_bucket_count": sum(len(indices) >= 2 for indices in buckets.values()),
        "eligible_edge_count": len(eligible_edges),
        "eligible_edge_fraction": len(eligible_edges) / len(edges),
        "all_unordered_edge_pairs": math.comb(len(edges), 2),
        "within_footprint_candidate_pairs": candidate_pairs,
        "legal_pairs": counts["legal"],
        "legal_edge_count": len(legal_edges),
        "legal_edge_fraction": len(legal_edges) / len(edges),
        "reachable": int(counts["legal"] > 0),
        "promising_support": int(len(legal_edges) / len(edges) >= MIN_PROMISING_LEGAL_EDGE_FRACTION),
    }
    rejection_rows = [{
        **dag.prefix,
        "reason": reason,
        "pair_count": counts[reason],
        "pair_fraction": counts[reason] / candidate_pairs if candidate_pairs else 0.0,
    } for reason in spec_payload()["rejection_order"]]
    return summary, bucket_rows, rejection_rows, samples


def build_report(
    summaries: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16p event-footprint reachability audit",
        "",
        f"Status: `{overall}`.",
        "",
        "V16p exactly enumerates all direct-edge pairs that share a source-write/target-read event footprint in the six saved v16n calibration DAGs. The footprint retains event family and resource namespace sets, but it does not require a concrete shared resource ID on proposed null edges.",
        "",
        "The round performs no rewiring and computes no interval spectrum. It is an effect-blind support diagnostic, not an effect test.",
        "",
        f"Specification digest: `{spec_digest()}`.",
        "",
        "## Per-run support",
        "",
    ]
    lines.extend(v16i.table(summaries, (
        "growth_seed", "run_offset", "edge_count", "eligible_edge_fraction",
        "within_footprint_candidate_pairs", "legal_pairs", "legal_edge_fraction",
        "promising_support",
    )))
    lines.extend(["", "## Gates", ""])
    lines.extend(v16i.table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "Static reachability is necessary but not sufficient for a useful null sampler. It does not establish chain connectivity, mixing, convergence, stationarity, independence, representativeness, or uniformity.",
        "",
        "The footprint is a coarse event-side conditioning rule. It does not preserve concrete resource identity and does not test a physical mechanism. No v16m spectrum effect is evaluated here.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    verify_frozen_sources()
    summaries: List[Dict[str, Any]] = []
    bucket_rows: List[Dict[str, Any]] = []
    rejection_rows: List[Dict[str, Any]] = []
    samples: List[Dict[str, Any]] = []
    runs = v16o.load_runs()
    for index, (dag, metadata) in enumerate(runs, start=1):
        summary, run_buckets, run_rejections, run_samples = audit_run(dag, metadata)
        summaries.append(summary)
        bucket_rows.extend(run_buckets)
        rejection_rows.extend(run_rejections)
        samples.extend(run_samples)
        print(
            f"[v16p] runs={index}/{len(runs)} candidates={summary['within_footprint_candidate_pairs']} "
            f"legal={summary['legal_pairs']} edge_fraction={summary['legal_edge_fraction']:.6f}"
        )

    reachable = all(int(row["reachable"]) for row in summaries)
    promising = all(int(row["promising_support"]) for row in summaries)
    if promising:
        overall = "v16p_event_footprint_static_support_promising"
    elif reachable:
        overall = "v16p_event_footprint_reachable_but_sparse"
    else:
        overall = "v16p_event_footprint_structurally_immobile"
    total_candidates = sum(int(row["within_footprint_candidate_pairs"]) for row in summaries)
    total_legal = sum(int(row["legal_pairs"]) for row in summaries)
    min_fraction = min(float(row["legal_edge_fraction"]) for row in summaries)
    gates = [
        {
            "gate": "exact_within_footprint_enumeration",
            "status": "pass",
            "observed": f"runs={len(summaries)};candidate_pairs={total_candidates}",
            "required": f"runs={len(v16n.assignments())};all_within_bucket_pairs_exact",
            "decision": "continue",
        },
        {
            "gate": "all_run_reachability",
            "status": "pass" if reachable else "fail",
            "observed": f"legal_pairs={total_legal};runs_with_moves={sum(int(row['reachable']) for row in summaries)}/{len(summaries)}",
            "required": f"runs_with_moves={len(summaries)}/{len(summaries)}",
            "decision": "continue" if reachable else "retire_footprint_swap_null",
        },
        {
            "gate": "all_run_static_support",
            "status": "pass" if promising else "fail",
            "observed": min_fraction,
            "required": f">={MIN_PROMISING_LEGAL_EDGE_FRACTION}",
            "decision": "qualify_sampler_next" if promising else "do_not_run_effect_gate",
        },
        {
            "gate": "spectrum_and_rewiring_exclusion",
            "status": "pass",
            "observed": "spectrum=0;rewires=0",
            "required": "0;0",
            "decision": "diagnostic_only",
        },
        {
            "gate": "v16p_overall",
            "status": overall,
            "observed": f"reachable={int(reachable)};promising={int(promising)};min_legal_edge_fraction={min_fraction:.12f}",
            "required": "diagnostic_branch",
            "decision": overall,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "The event-footprint proposal has at least one legal static transition in every audited DAG.",
            "status": "supported" if reachable else "unsupported",
            "evidence": "v16p_reachability_run_summary.csv;v16p_rejection_counts.csv",
            "scope_limit": "exact static enumeration on six finite calibration DAGs",
        },
        {
            "claim_id": "C2",
            "claim": "The event-footprint proposal has at least 10 percent legal edge coverage in every audited DAG.",
            "status": "supported" if promising else "unsupported",
            "evidence": "v16p_reachability_run_summary.csv",
            "scope_limit": "threshold qualifies only a later sampler calibration attempt",
        },
        {
            "claim_id": "C3",
            "claim": "The event-footprint proposal is mixed, converged, representative, or uniform.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "no Markov chain was run",
        },
        {
            "claim_id": "C4",
            "claim": "The v16m interval-spectrum contrast survives event-footprint conditioning.",
            "status": "not_evaluated",
            "evidence": "none",
            "scope_limit": "no interval spectrum computed",
        },
    ]

    v16i.write_csv(BUCKET_SUMMARY, bucket_rows)
    v16i.write_csv(RUN_SUMMARY, summaries)
    v16i.write_csv(REJECTION_COUNTS, rejection_rows)
    v16i.write_csv(LEGAL_PAIR_SAMPLES, samples if samples else [{
        "status": "no_legal_pairs",
        "note": "placeholder row because no legal pair sample exists",
    }])
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    REPORT.write_text(build_report(summaries, gates, overall), encoding="utf-8")
    next_step = {
        "v16p_event_footprint_static_support_promising": "build an effect-blind event-footprint sampler qualification gate before any spectrum test",
        "v16p_event_footprint_reachable_but_sparse": "retire or redesign the footprint swap null without inspecting the v16m effect",
        "v16p_event_footprint_structurally_immobile": "retire the resource-aware swap-null route and choose a different null family",
    }[overall]
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.16p\n\n"
        f"Status: `{overall}`.\n\n"
        f"Next: {next_step}.\n\n"
        "No spectrum effect, sampler mixing, or physical geometry was evaluated.\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.16p\n\n"
        f"Statusen er `{overall}`. Runden teller noeyaktig om en grovere kontrollregel har nok mulige kantbytter til aa kunne testes videre. Den tester ikke universsignal eller fysikk.\n",
        encoding="utf-8",
    )
    print(f"[v16p] complete overall={overall} legal={total_legal}")


def verify_outputs() -> None:
    verify_frozen_sources()
    summaries = v16i.read_csv(RUN_SUMMARY)
    buckets = v16i.read_csv(BUCKET_SUMMARY)
    rejections = v16i.read_csv(REJECTION_COUNTS)
    gates = v16i.read_csv(GATE_EVALUATION)
    if len(summaries) != len(v16n.assignments()):
        raise ValueError("v16p summary row count failed")
    if len(rejections) != len(summaries) * len(spec_payload()["rejection_order"]):
        raise ValueError("v16p rejection row count failed")
    for summary in summaries:
        key = v16o.run_key(summary)
        candidate_total = sum(
            int(row["pair_count"]) for row in rejections if v16o.run_key(row) == key
        )
        if candidate_total != int(summary["within_footprint_candidate_pairs"]):
            raise ValueError("v16p candidate pair accounting failed")
        bucket_total = sum(
            int(row["candidate_pair_count"]) for row in buckets if v16o.run_key(row) == key
        )
        if bucket_total != candidate_total:
            raise ValueError("v16p bucket pair accounting failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16p_overall")
    allowed = {
        "v16p_event_footprint_static_support_promising",
        "v16p_event_footprint_reachable_but_sparse",
        "v16p_event_footprint_structurally_immobile",
    }
    if overall not in allowed:
        raise ValueError("v16p unknown status")
    print(f"[v16p] output verification pass overall={overall}")


def self_test() -> None:
    metadata = (
        {"family": "token", "reads": frozenset({"node:0"}), "writes": frozenset({"edge:0"})},
        {"family": "token", "reads": frozenset({"node:1"}), "writes": frozenset({"edge:1"})},
        {"family": "token", "reads": frozenset({"node:2"}), "writes": frozenset({"edge:2"})},
        {"family": "token", "reads": frozenset({"node:3"}), "writes": frozenset({"edge:3"})},
    )
    if edge_footprint(0, 2, metadata) != edge_footprint(1, 3, metadata):
        raise AssertionError("v16p namespace roles should ignore concrete resource ids")
    reason = candidate_reason(
        (0, 2),
        (1, 3),
        {(0, 2), (1, 3)},
        ((), (), (0,), (1,)),
        (0, 0, 1, 1),
    )
    if reason != "global_dyadic_age_bin_multiset":
        raise AssertionError(f"v16p rejection ordering failed: {reason}")
    print("[v16p] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16p event-footprint reachability audit")
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
