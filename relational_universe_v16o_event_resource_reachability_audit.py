#!/usr/bin/env python3
"""v16o: exact reachability audit for two event/resource edge-color rules.

The audit enumerates every unordered pair of direct edges in the six v16n
calibration DAGs. It computes no interval spectrum and performs no rewiring.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16j_interval_strict_null_gate as v16j
import relational_universe_v16n_coarse_event_resource_null_calibration as v16n


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
SCRIPT = Path(__file__).resolve()
PURPOSE_REF = "purpose://validation"
SAMPLE_LEGAL_PAIRS_PER_RUN = 32
MIN_PROMISING_LEGAL_EDGE_FRACTION = 0.10

SOURCE_CHAIN = DOC / "v16o_source_chain.csv"
PRE_REGISTRATION = DOC / "v16o_pre_registration.csv"
RUN_SUMMARY = DOC / "v16o_reachability_run_summary.csv"
REJECTION_COUNTS = DOC / "v16o_rejection_counts.csv"
LEGAL_PAIR_SAMPLES = DOC / "v16o_legal_pair_samples.csv"
GATE_EVALUATION = DOC / "v16o_gate_evaluation.csv"
CLAIM_LEDGER = DOC / "v16o_claim_ledger.csv"
REPORT = DOC / "v16o_event_resource_reachability_audit.md"
RECOMMENDATION = DOC / "v0_16o_operativ_anbefaling.md"
NONSPECIALIST = DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16o.md"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_chain_rows() -> List[Dict[str, Any]]:
    paths = [
        ("v16n", "null_implementation", Path(v16n.__file__)),
        ("v16n", "calibration_events", v16n.EVENT_LOG),
        ("v16n", "calibration_edges", v16n.EDGE_LOG),
        ("v16n", "qualification", v16n.QUALIFICATION),
        ("v16n", "interpretation_audit", DOC / "v16n_interpretation_audit.csv"),
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
        "gate": "v16o_event_resource_reachability_audit",
        "purpose_ref": PURPOSE_REF,
        "source": "six_v16n_calibration_dags",
        "enumeration": "all_unordered_direct_edge_pairs",
        "rules": [
            "v16n_same_color_pair",
            "general_global_two_color_multiset",
        ],
        "rejection_order": [
            "same_parent_or_child",
            "scheduler_order",
            "duplicate_edge",
            "missing_actual_cross_conflict",
            "global_color_multiset",
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
    v16n.verify_outputs()
    qualification = v16i.read_csv(v16n.QUALIFICATION)
    if len(qualification) != 1 or qualification[0]["status"] != "v16n_coarse_event_resource_sampler_not_qualified":
        raise ValueError("v16o requires the frozen v16n non-qualification")
    v16i.write_csv(SOURCE_CHAIN, source_chain_rows())
    v16i.write_csv(PRE_REGISTRATION, [{
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "script_sha256": file_sha256(SCRIPT),
        "source_chain_sha256": file_sha256(SOURCE_CHAIN),
        "source_run_count": len(v16n.assignments()),
        "same_color_rule": 1,
        "general_color_multiset_rule": 1,
        "exact_pair_enumeration": 1,
        "minimum_promising_legal_edge_fraction": MIN_PROMISING_LEGAL_EDGE_FRACTION,
        "spectrum_computation_allowed": 0,
        "rewiring_allowed": 0,
    }])
    print(f"[v16o] prepared digest={spec_digest()}")


def verify_frozen_sources() -> None:
    prereg = v16i.read_csv(PRE_REGISTRATION)
    if len(prereg) != 1:
        raise ValueError("v16o preregistration row count failed")
    expected = {
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "script_sha256": file_sha256(SCRIPT),
        "source_chain_sha256": file_sha256(SOURCE_CHAIN),
        "source_run_count": str(len(v16n.assignments())),
        "same_color_rule": "1",
        "general_color_multiset_rule": "1",
        "exact_pair_enumeration": "1",
        "minimum_promising_legal_edge_fraction": str(MIN_PROMISING_LEGAL_EDGE_FRACTION),
        "spectrum_computation_allowed": "0",
        "rewiring_allowed": "0",
    }
    if prereg[0] != expected:
        raise ValueError("v16o preregistration changed")
    frozen = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in v16i.read_csv(SOURCE_CHAIN)
    }
    current = {
        (row["stage"], row["role"], row["artifact"]): row["sha256"]
        for row in source_chain_rows()
    }
    if frozen != current:
        raise ValueError("v16o source chain changed")


def run_key(row: Mapping[str, Any]) -> Tuple[int, int, str, int]:
    return (
        int(row["growth_seed"]),
        int(row["run_offset"]),
        str(row["arm"]),
        int(row["run_seed"]),
    )


def load_runs() -> List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]]:
    grouped: Dict[Tuple[int, int, str, int], List[Dict[str, str]]] = defaultdict(list)
    for row in v16i.read_csv(v16n.EVENT_LOG):
        grouped[run_key(row)].append(row)
    runs: List[Tuple[v16i.RunDAG, Tuple[Dict[str, Any], ...]]] = []
    for key in sorted(grouped):
        rows = sorted(grouped[key], key=lambda row: int(row["event_id"]))
        metadata, audit = v16n.event_metadata(rows)
        if not int(audit["event_id_mapping_total_pass"]):
            raise ValueError("v16o metadata mapping failed")
        predecessors = tuple(
            tuple(int(value) for value in row["direct_predecessors"].split(";") if value)
            for row in rows
        )
        depths = tuple(int(row["causal_depth"]) for row in rows)
        if tuple(v16i.recompute_depths(predecessors)) != depths:
            raise ValueError("v16o source depth mismatch")
        growth_seed, run_offset, arm, run_seed = key
        dag = v16i.RunDAG(
            stage="v16o",
            target_nodes=v16n.TARGET_NODES,
            growth_seed=growth_seed,
            run_offset=run_offset,
            arm=arm,
            run_seed=run_seed,
            predecessors=predecessors,
            depths=depths,
            indegrees=tuple(len(parents) for parents in predecessors),
        )
        runs.append((dag, metadata))
    if len(runs) != len(v16n.assignments()):
        raise ValueError("v16o source run count failed")
    return runs


def candidate_reason(
    first: Tuple[int, int],
    second: Tuple[int, int],
    first_color: v16n.EdgeColor,
    second_color: v16n.EdgeColor,
    edge_set: Set[Tuple[int, int]],
    predecessors: Sequence[Sequence[int]],
    depths: Sequence[int],
    metadata: Sequence[Mapping[str, Any]],
) -> Tuple[str, Optional[v16n.EdgeColor], Optional[v16n.EdgeColor]]:
    parent_a, child_b = first
    parent_c, child_d = second
    if parent_a == parent_c or child_b == child_d:
        return "same_parent_or_child", None, None
    new_first = (parent_a, child_d)
    new_second = (parent_c, child_b)
    if parent_a >= child_d or parent_c >= child_b:
        return "scheduler_order", None, None
    if new_first in edge_set or new_second in edge_set or new_first == new_second:
        return "duplicate_edge", None, None
    new_first_color = v16n.edge_color(*new_first, metadata)
    new_second_color = v16n.edge_color(*new_second, metadata)
    if new_first_color is None or new_second_color is None:
        return "missing_actual_cross_conflict", new_first_color, new_second_color
    if sorted((new_first_color, new_second_color)) != sorted((first_color, second_color)):
        return "global_color_multiset", new_first_color, new_second_color
    if sorted((v16j.lag_bin(parent_a, child_b), v16j.lag_bin(parent_c, child_d))) != sorted((v16j.lag_bin(parent_a, child_d), v16j.lag_bin(parent_c, child_b))):
        return "global_dyadic_age_bin_multiset", new_first_color, new_second_color
    next_b = (set(predecessors[child_b]) - {parent_a}) | {parent_c}
    next_d = (set(predecessors[child_d]) - {parent_c}) | {parent_a}
    if (
        not next_b
        or not next_d
        or max(depths[parent] for parent in next_b) != depths[child_b] - 1
        or max(depths[parent] for parent in next_d) != depths[child_d] - 1
    ):
        return "exact_child_depth", new_first_color, new_second_color
    return "legal", new_first_color, new_second_color


def audit_run(
    dag: v16i.RunDAG,
    metadata: Sequence[Mapping[str, Any]],
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    edges = [
        (parent, child)
        for child, parents in enumerate(dag.predecessors)
        for parent in parents
    ]
    colors = [v16n.edge_color(parent, child, metadata) for parent, child in edges]
    if any(color is None for color in colors):
        raise ValueError("v16o source edge lacks a color")
    typed_colors = [color for color in colors if color is not None]
    edge_set = set(edges)
    general_counts: Counter[str] = Counter()
    same_counts: Counter[str] = Counter()
    general_legal_edges: Set[int] = set()
    same_legal_edges: Set[int] = set()
    samples: List[Dict[str, Any]] = []

    for first_index in range(len(edges) - 1):
        first = edges[first_index]
        first_color = typed_colors[first_index]
        for second_index in range(first_index + 1, len(edges)):
            second = edges[second_index]
            second_color = typed_colors[second_index]
            reason, new_first_color, new_second_color = candidate_reason(
                first,
                second,
                first_color,
                second_color,
                edge_set,
                dag.predecessors,
                dag.depths,
                metadata,
            )
            general_counts[reason] += 1
            if first_color == second_color:
                same_counts[reason] += 1
            if reason == "legal":
                general_legal_edges.update((first_index, second_index))
                if first_color == second_color:
                    same_legal_edges.update((first_index, second_index))
                if len(samples) < SAMPLE_LEGAL_PAIRS_PER_RUN:
                    samples.append({
                        **dag.prefix,
                        "first_edge_index": first_index,
                        "second_edge_index": second_index,
                        "old_first_edge": f"{first[0]}>{first[1]}",
                        "old_second_edge": f"{second[0]}>{second[1]}",
                        "new_first_edge": f"{first[0]}>{second[1]}",
                        "new_second_edge": f"{second[0]}>{first[1]}",
                        "old_first_color": v16n.color_text(first_color),
                        "old_second_color": v16n.color_text(second_color),
                        "new_first_color": v16n.color_text(new_first_color) if new_first_color is not None else "",
                        "new_second_color": v16n.color_text(new_second_color) if new_second_color is not None else "",
                        "same_color_pair": int(first_color == second_color),
                    })

    total_pairs = math.comb(len(edges), 2)
    same_pairs = sum(same_counts.values())
    summary = {
        **dag.prefix,
        "edge_count": len(edges),
        "all_unordered_edge_pairs": total_pairs,
        "same_color_edge_pairs": same_pairs,
        "same_color_legal_pairs": same_counts["legal"],
        "same_color_legal_edge_count": len(same_legal_edges),
        "same_color_legal_edge_fraction": len(same_legal_edges) / len(edges),
        "general_multiset_legal_pairs": general_counts["legal"],
        "general_multiset_legal_edge_count": len(general_legal_edges),
        "general_multiset_legal_edge_fraction": len(general_legal_edges) / len(edges),
        "general_multiset_reachable": int(general_counts["legal"] > 0),
        "general_multiset_promising_support": int(
            len(general_legal_edges) / len(edges) >= MIN_PROMISING_LEGAL_EDGE_FRACTION
        ),
    }
    rejection_rows: List[Dict[str, Any]] = []
    for rule, counts, denominator in (
        ("v16n_same_color", same_counts, same_pairs),
        ("general_color_multiset", general_counts, total_pairs),
    ):
        for reason in spec_payload()["rejection_order"]:
            count = counts[reason]
            rejection_rows.append({
                **dag.prefix,
                "rule": rule,
                "reason": reason,
                "pair_count": count,
                "pair_fraction": count / denominator if denominator else 0.0,
            })
    return summary, rejection_rows, samples


def build_report(
    summaries: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16o event/resource reachability audit",
        "",
        f"Status: `{overall}`.",
        "",
        "V16o exactly enumerates every unordered direct-edge pair in the six saved v16n calibration DAGs. It compares the frozen same-color proposal with the more general global two-color multiset rule. It performs no rewiring and computes no interval spectrum.",
        "",
        f"Specification digest: `{spec_digest()}`.",
        "",
        "## Per-run support",
        "",
    ]
    lines.extend(v16i.table(summaries, (
        "growth_seed", "run_offset", "edge_count", "all_unordered_edge_pairs",
        "same_color_legal_pairs", "same_color_legal_edge_fraction",
        "general_multiset_legal_pairs", "general_multiset_legal_edge_fraction",
        "general_multiset_promising_support",
    )))
    lines.extend(["", "## Gates", ""])
    lines.extend(v16i.table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "Reachability is necessary but not sufficient for a useful sampler. Legal static swaps do not establish chain connectivity, mixing, convergence, stationarity, independence, representativeness, or uniformity.",
        "",
        "No event/resource-conditioned spectrum effect or physical claim is evaluated here.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    verify_frozen_sources()
    summaries: List[Dict[str, Any]] = []
    rejections: List[Dict[str, Any]] = []
    samples: List[Dict[str, Any]] = []
    runs = load_runs()
    for index, (dag, metadata) in enumerate(runs, start=1):
        summary, run_rejections, run_samples = audit_run(dag, metadata)
        summaries.append(summary)
        rejections.extend(run_rejections)
        samples.extend(run_samples)
        print(
            f"[v16o] runs={index}/{len(runs)} pairs={summary['all_unordered_edge_pairs']} "
            f"same_legal={summary['same_color_legal_pairs']} general_legal={summary['general_multiset_legal_pairs']}"
        )

    same_confirmed = all(int(row["same_color_legal_pairs"]) == 0 for row in summaries)
    general_reachable = all(int(row["general_multiset_reachable"]) for row in summaries)
    general_promising = all(int(row["general_multiset_promising_support"]) for row in summaries)
    if not same_confirmed:
        overall = "v16o_v16n_zero_move_diagnosis_not_reproduced"
    elif general_promising:
        overall = "v16o_general_color_multiset_support_promising"
    elif general_reachable:
        overall = "v16o_general_color_multiset_reachable_but_sparse"
    else:
        overall = "v16o_actual_conflict_color_null_structurally_immobile"
    total_pairs = sum(int(row["all_unordered_edge_pairs"]) for row in summaries)
    total_general_legal = sum(int(row["general_multiset_legal_pairs"]) for row in summaries)
    gates = [
        {
            "gate": "exact_pair_enumeration",
            "status": "pass",
            "observed": f"runs={len(summaries)};pairs={total_pairs}",
            "required": f"runs={len(v16n.assignments())};all_pairs_exact",
            "decision": "continue",
        },
        {
            "gate": "v16n_same_color_zero_move_reproduction",
            "status": "pass" if same_confirmed else "fail",
            "observed": sum(int(row["same_color_legal_pairs"]) for row in summaries),
            "required": 0,
            "decision": "diagnosed" if same_confirmed else "audit_mismatch",
        },
        {
            "gate": "general_color_multiset_reachability",
            "status": "pass" if general_reachable else "fail",
            "observed": f"legal_pairs={total_general_legal};runs_with_moves={sum(int(row['general_multiset_reachable']) for row in summaries)}/{len(summaries)}",
            "required": f"runs_with_moves={len(summaries)}/{len(summaries)}",
            "decision": "continue" if general_reachable else "retire_actual_conflict_color_null",
        },
        {
            "gate": "general_color_multiset_support",
            "status": "pass" if general_promising else "fail",
            "observed": min(float(row["general_multiset_legal_edge_fraction"]) for row in summaries),
            "required": f">={MIN_PROMISING_LEGAL_EDGE_FRACTION}",
            "decision": "qualify_sampler_next" if general_promising else "do_not_run_effect_gate",
        },
        {
            "gate": "spectrum_and_rewiring_exclusion",
            "status": "pass",
            "observed": "spectrum=0;rewires=0",
            "required": "0;0",
            "decision": "diagnostic_only",
        },
        {
            "gate": "v16o_overall",
            "status": overall,
            "observed": f"same_zero={int(same_confirmed)};general_reachable={int(general_reachable)};general_promising={int(general_promising)}",
            "required": "diagnostic_branch",
            "decision": overall,
        },
    ]
    claims = [
        {
            "claim_id": "C1",
            "claim": "The v16n same-color proposal has no legal first transition on the six calibration DAGs.",
            "status": "supported" if same_confirmed else "unsupported",
            "evidence": "v16o_reachability_run_summary.csv;v16o_rejection_counts.csv",
            "scope_limit": "exact static enumeration on six finite DAGs",
        },
        {
            "claim_id": "C2",
            "claim": "The general global two-color multiset rule has enough static legal support to justify effect-blind sampler qualification.",
            "status": "supported" if general_promising else "unsupported",
            "evidence": "v16o_reachability_run_summary.csv",
            "scope_limit": "reachability is not chain mixing",
        },
        {
            "claim_id": "C3",
            "claim": "The v16m spectrum contrast survives event/resource conditioning.",
            "status": "not_evaluated",
            "evidence": "none",
            "scope_limit": "no spectrum computed",
        },
        {
            "claim_id": "C4",
            "claim": "The reachable proposal is converged, representative, or uniform.",
            "status": "unsupported",
            "evidence": "none",
            "scope_limit": "static legal-pair audit only",
        },
    ]

    v16i.write_csv(RUN_SUMMARY, summaries)
    v16i.write_csv(REJECTION_COUNTS, rejections)
    if samples:
        v16i.write_csv(LEGAL_PAIR_SAMPLES, samples)
    else:
        v16i.write_csv(LEGAL_PAIR_SAMPLES, [{
            "status": "no_general_legal_pairs",
            "note": "placeholder row because no legal pair sample exists",
        }])
    v16i.write_csv(GATE_EVALUATION, gates)
    v16i.write_csv(CLAIM_LEDGER, claims)
    REPORT.write_text(build_report(summaries, gates, overall), encoding="utf-8")
    next_step = {
        "v16o_general_color_multiset_support_promising": "build an effect-blind general-multiset sampler qualification gate",
        "v16o_general_color_multiset_reachable_but_sparse": "diagnose proposal support before any sampler or effect gate",
        "v16o_actual_conflict_color_null_structurally_immobile": "retire actual-conflict edge colors and test the weaker event-side footprint null",
        "v16o_v16n_zero_move_diagnosis_not_reproduced": "repair the reachability audit mismatch",
    }[overall]
    RECOMMENDATION.write_text(
        "# Operativ anbefaling v0.16o\n\n"
        f"Status: `{overall}`.\n\n"
        f"Next: {next_step}.\n\n"
        "No spectrum effect or physical geometry was evaluated.\n",
        encoding="utf-8",
    )
    NONSPECIALIST.write_text(
        "# Relasjonell universgraf for ikke-spesialister v0.16o\n\n"
        f"Statusen er `{overall}`. Runden teller noeyaktig hvilke kantbytter kontrollmodellen faktisk tillater. Den tester ikke universsignal eller fysikk.\n",
        encoding="utf-8",
    )
    print(f"[v16o] complete overall={overall} general_legal={total_general_legal}")


def verify_outputs() -> None:
    verify_frozen_sources()
    summaries = v16i.read_csv(RUN_SUMMARY)
    rejections = v16i.read_csv(REJECTION_COUNTS)
    gates = v16i.read_csv(GATE_EVALUATION)
    if len(summaries) != len(v16n.assignments()):
        raise ValueError("v16o summary row count failed")
    if len(rejections) != len(summaries) * 2 * len(spec_payload()["rejection_order"]):
        raise ValueError("v16o rejection row count failed")
    if any(sum(int(row["pair_count"]) for row in rejections if run_key(row) == run_key(summary) and row["rule"] == "general_color_multiset") != int(summary["all_unordered_edge_pairs"]) for summary in summaries):
        raise ValueError("v16o general pair accounting failed")
    overall = next(row["status"] for row in gates if row["gate"] == "v16o_overall")
    allowed = {
        "v16o_v16n_zero_move_diagnosis_not_reproduced",
        "v16o_general_color_multiset_support_promising",
        "v16o_general_color_multiset_reachable_but_sparse",
        "v16o_actual_conflict_color_null_structurally_immobile",
    }
    if overall not in allowed:
        raise ValueError("v16o unknown status")
    print(f"[v16o] output verification pass overall={overall}")


def self_test() -> None:
    metadata = (
        {"family": "token", "event_type": "move", "reads": frozenset({"token:1"}), "writes": frozenset({"token:1"})},
        {"family": "token", "event_type": "move", "reads": frozenset({"token:1"}), "writes": frozenset({"token:1"})},
        {"family": "token", "event_type": "move", "reads": frozenset({"token:1"}), "writes": frozenset({"token:1"})},
        {"family": "token", "event_type": "move", "reads": frozenset({"token:1"}), "writes": frozenset({"token:1"})},
    )
    color = v16n.edge_color(0, 2, metadata)
    assert color is not None
    reason, _, _ = candidate_reason(
        (0, 2),
        (1, 3),
        color,
        color,
        {(0, 2), (1, 3)},
        ((), (), (0,), (1,)),
        (0, 0, 1, 1),
        metadata,
    )
    if reason != "global_dyadic_age_bin_multiset":
        raise AssertionError(f"v16o rejection ordering failed: {reason}")
    print("[v16o] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16o event/resource reachability audit")
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
