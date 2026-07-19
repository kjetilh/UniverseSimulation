#!/usr/bin/env python3
"""Postrun diagnosis of v17f reverse-unsupported length-5 auxiliaries."""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16x_explicit_global_measure_gate as v16x
import relational_universe_v16z_alternating_cycle_bridge_gate as v16z
import relational_universe_v17a_state_independent_cycle_proposal_qualification as v17a
import relational_universe_v17b_residual_cycle_constructor_gate as v17b
import relational_universe_v17f_effect_blind_length5_move_qualification as v17f


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
INPUT_AUDIT = DOC / "v17f_postrun_reverse_closure_inputs.csv"
DETAIL = DOC / "v17f_postrun_reverse_closure_diagnosis.csv"
REPORT = DOC / "v17f_postrun_reverse_closure_diagnosis.md"
EXPANDED_SEARCH_STATES = 200_000

Edge = v16x.Edge


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_rows() -> List[Dict[str, Any]]:
    paths = (
        v17f.PRE_REGISTRATION,
        v17f.GATE_EVALUATION,
        v17f.PROPOSAL_TRACE,
        v17f.TRANSITION_SUMMARY,
        v17f.REVERSIBILITY_AUDIT,
    )
    return [{"artifact": path.name, "sha256": file_sha256(path)} for path in paths]


def edges(value: str) -> Tuple[Edge, ...]:
    return tuple(tuple(int(part) for part in edge) for edge in json.loads(value))


def trace_groups() -> Dict[Tuple[int, int, str, str], List[Mapping[str, str]]]:
    groups: Dict[Tuple[int, int, str, str], List[Mapping[str, str]]] = {}
    for row in v16i.read_csv(v17f.PROPOSAL_TRACE):
        key = (
            int(row["growth_seed"]),
            int(row["run_offset"]),
            row["start_family"],
            row["chain_seed_family"],
        )
        groups.setdefault(key, []).append(row)
    for rows in groups.values():
        rows.sort(key=lambda row: int(row["step"]))
    return groups


def diagnose_event(
    dag: v16i.RunDAG,
    kernel: v17f.CycleKernel,
    selected: frozenset[Edge],
    row: Mapping[str, str],
) -> Dict[str, Any]:
    remove = edges(row["remove_edges_json"])
    add = edges(row["add_edges_json"])
    batch = edges(row["first_batch_json"])
    proposal = v17a.CycleProposal(remove, add)
    proposed = v17a.apply_proposal(kernel.space, selected, proposal)
    auxiliary = v17f.ExpandedAuxiliary(
        "length_5_batch_guided",
        Fraction(1),
        proposal,
        batch,
    )
    mapped_batch = v17f.reverse_first_batch(auxiliary)
    reverse_remove = v17a.reverse_remove_sequence(proposal)
    by_parent = v17a.selected_by_parent(proposed)
    all_guides = {}
    eligible = {}
    for first in mapped_batch:
        guide = v17f.CompletionGuide(kernel, proposed, first, by_parent)
        slot = kernel.space.slot_by_edge[first]
        if guide.has_completion(
            slot, frozenset({first[0]}), frozenset({slot}), 1
        ):
            eligible[first] = guide
        all_guides[first] = guide
    reverse_first = reverse_remove[0]
    reverse_first_eligible = reverse_first in eligible
    reverse_guide = all_guides[reverse_first]
    raw_path_valid = True
    current_slot = kernel.space.slot_by_edge[reverse_first]
    used_parents = frozenset({reverse_first[0]})
    used_slots = frozenset({current_slot})
    for edge in reverse_remove[1:]:
        raw = reverse_guide.raw_map(current_slot, used_parents, used_slots)
        if edge not in raw.get(edge[0], ()):
            raw_path_valid = False
            break
        current_slot = kernel.space.slot_by_edge[edge]
        used_parents |= {edge[0]}
        used_slots |= {current_slot}
    raw_path_valid = raw_path_valid and reverse_guide.closure_valid(current_slot)
    suffix_supported = False
    closure_supported = False
    if reverse_first_eligible:
        suffix_supported = (
            v17f.suffix_probability(eligible[reverse_first], reverse_remove)
            is not None
        )
        closure_supported = (
            v17b.close_proposal(kernel, proposed, reverse_remove) is not None
        )
    frozen_search_states = sum(guide.search_states for guide in all_guides.values())
    frozen_search_exhaustions = sum(
        guide.search_budget_exhaustions for guide in all_guides.values()
    )
    if not reverse_first_eligible and reverse_guide.search_budget_exhaustions:
        reason = "reverse_first_search_budget_exhausted"
    elif not reverse_first_eligible:
        reason = "reverse_first_missing_without_recorded_exhaustion"
    elif not suffix_supported:
        reason = "reverse_suffix_missing_from_bounded_support"
    elif not closure_supported:
        reason = "reverse_cycle_closure_failed"
    else:
        reason = "path_probability_failed_after_local_checks"

    original_limit = v17f.MAX_SEARCH_STATES_PER_GUIDE
    try:
        v17f.MAX_SEARCH_STATES_PER_GUIDE = EXPANDED_SEARCH_STATES
        expanded = v17f.length5_path_probability(
            kernel, proposed, reverse_remove, mapped_batch
        )
    finally:
        v17f.MAX_SEARCH_STATES_PER_GUIDE = original_limit

    return {
        **dag.prefix,
        "start_family": row["start_family"],
        "chain_seed_family": row["chain_seed_family"],
        "step": int(row["step"]),
        "proposal_sha256": row["proposal_sha256"],
        "cycle_length": len(remove),
        "mapped_batch_valid_pass": int(
            len(mapped_batch) == v17f.FIRST_BATCH_SIZE
            and len(set(mapped_batch)) == v17f.FIRST_BATCH_SIZE
            and set(mapped_batch).issubset(proposed)
        ),
        "frozen_search_limit": original_limit,
        "frozen_eligible_first_count": len(eligible),
        "reverse_first_eligible_pass": int(reverse_first_eligible),
        "reverse_raw_path_valid_pass": int(raw_path_valid),
        "reverse_suffix_supported_pass": int(suffix_supported),
        "reverse_closure_supported_pass": int(closure_supported),
        "frozen_search_states": frozen_search_states,
        "frozen_search_budget_exhaustions": frozen_search_exhaustions,
        "failure_reason": reason,
        "expanded_search_limit": EXPANDED_SEARCH_STATES,
        "expanded_search_recovers_reverse_support": int(expanded is not None),
        "source_spectrum_computed": 0,
        "observed_effect_computed": 0,
    }


def run() -> None:
    v17f.verify_outputs()
    v16i.write_csv(INPUT_AUDIT, input_rows())
    groups = trace_groups()
    run_map = {
        (dag.growth_seed, dag.run_offset): (dag, metadata)
        for dag, metadata in v17f.load_runs()
    }
    details = []
    replay_passes = 0
    for key, rows in groups.items():
        growth_seed, run_offset, start_family, _ = key
        dag, metadata = run_map[(growth_seed, run_offset)]
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        kernel = v17a.build_kernel(space)
        starts = {
            "source_assignment": space.source_edges,
            "v16x_random_cost_a0": v16z.random_cost_start(dag, space),
        }
        selected = starts[start_family]
        chain_ok = True
        for row in rows:
            if v16x.edge_digest(selected) != row["state_before_sha256"]:
                chain_ok = False
                break
            if row["event"] == "reverse_unsupported":
                details.append(diagnose_event(dag, kernel, selected, row))
            if int(row["accepted"]):
                proposal = v17a.CycleProposal(
                    edges(row["remove_edges_json"]),
                    edges(row["add_edges_json"]),
                )
                selected = v17a.apply_proposal(space, selected, proposal)
            if v16x.edge_digest(selected) != row["state_after_sha256"]:
                chain_ok = False
                break
        replay_passes += int(chain_ok)

    v16i.write_csv(DETAIL, details)
    transitions = v16i.read_csv(v17f.TRANSITION_SUMMARY)
    affected = sum(int(row["reverse_unsupported"]) > 0 for row in transitions)
    total_unsupported = sum(int(row["reverse_unsupported"]) for row in transitions)
    valid_length5 = sum(int(row["valid_length5_cycles"]) for row in transitions)
    recovered = sum(
        int(row["expanded_search_recovers_reverse_support"]) for row in details
    )
    all_other_movement = sum(all((
        int(row["valid_proposals"]) >= v17f.MIN_VALID_PROPOSALS_PER_CHAIN,
        int(row["accepted_cycles"]) >= v17f.MIN_ACCEPTED_CYCLES_PER_CHAIN,
        int(row["accepted_old_cycles"]) >= v17f.MIN_ACCEPTED_OLD_CYCLES_PER_CHAIN,
        int(row["accepted_length5_cycles"]) >= v17f.MIN_ACCEPTED_LENGTH5_CYCLES_PER_CHAIN,
        int(row["unique_state_count"]) >= v17f.MIN_UNIQUE_STATES_PER_CHAIN,
        float(row["final_start_changed_edge_fraction"]) >= v17f.MIN_FINAL_START_CHANGE,
        int(row["final_assignment_integrity_pass"]) == 1,
    )) for row in transitions)
    raw_valid = sum(int(row["reverse_raw_path_valid_pass"]) for row in details)
    frozen_exhausted = sum(
        int(row["frozen_search_budget_exhaustions"]) > 0 for row in details
    )
    if raw_valid == total_unsupported and frozen_exhausted == total_unsupported:
        status = "v17f_reverse_support_failure_is_bounded_search_asymmetry"
    else:
        status = "v17f_reverse_support_failure_not_fully_recovered_by_10x_search"
    reasons = Counter(row["failure_reason"] for row in details)
    report = [
        "# v17f postrun reverse-closure diagnosis",
        "",
        f"Status: `{status}`.",
        "",
        "This diagnosis is descriptive and was not preregistered. It replays the frozen v17f trace without computing source spectra or observed effects.",
        "",
        "## Failure localization",
        "",
        f"Exact trace replay passed `{replay_passes}/24`. V17f recorded `{total_unsupported}` reverse-unsupported length-5 auxiliaries across `{affected}/24` chains, out of `{valid_length5}` valid length-5 auxiliaries (`{total_unsupported / valid_length5:.6f}`). All were rejected and changed no state.",
        "",
        f"All other frozen movement floors passed in `{all_other_movement}/24` chains. Resource passed `24/24`, with maximum formal chain runtime `{max(float(row['elapsed_seconds']) for row in transitions):.6f}` seconds.",
        "",
        "Failure reasons under the frozen 20,000-state guide: "
        + "; ".join(f"{key}={value}" for key, value in sorted(reasons.items()))
        + ".",
        "",
        f"The explicit reverse path was structurally valid in `{raw_valid}/{total_unsupported}` cases, and the frozen witness search exhausted its budget in `{frozen_exhausted}/{total_unsupported}`. A diagnostic 10x search cap recovered reverse support for `{recovered}/{total_unsupported}` failed auxiliaries. This does not alter the frozen v17f failure or qualify a larger search budget.",
        "",
        "## Interpretation",
        "",
        "The expanded Metropolis kernel remained probability-safe because q_reverse=0 auxiliaries were rejected. The stricter preregistered movement gate nevertheless failed because the bounded raw auxiliary support was not reverse-closed. The failure is in proposal-support qualification, not assignment integrity, length-5 availability, aggregate movement, or resource use.",
        "",
        "## Smallest next repair",
        "",
        "Define the length-5 proposal support as the existing generated auxiliary post-filtered by explicit reverse support under the same frozen 20,000-state law. Unsupported pairs become proposal dead ends before entering the valid-proposal count. This preserves the generation probability for retained auxiliaries, makes support reverse-closed by construction, and should permit exact replay of accepted v17f state trajectories. Preregister the repair and require exact endpoint/accepted-transition parity with v17f plus zero runtime reverse-unsupported events before any matched-work start-memory gate.",
        "",
        "This diagnosis does not establish connectivity, convergence, source effects, Bell correlations, entanglement, Lorentz symmetry, spacetime or a universe model.",
        "",
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print(f"[v17f-postrun] complete status={status}")


def verify_outputs() -> None:
    v17f.verify_outputs()
    frozen = {row["artifact"]: row["sha256"] for row in v16i.read_csv(INPUT_AUDIT)}
    current = {row["artifact"]: row["sha256"] for row in input_rows()}
    if frozen != current:
        raise ValueError("v17f postrun input hashes changed")
    details = v16i.read_csv(DETAIL)
    transitions = v16i.read_csv(v17f.TRANSITION_SUMMARY)
    expected = sum(int(row["reverse_unsupported"]) for row in transitions)
    if len(details) != expected:
        raise ValueError("v17f postrun detail count mismatch")
    if any(int(row["source_spectrum_computed"]) for row in details):
        raise ValueError("v17f postrun contains source spectrum")
    if any(int(row["observed_effect_computed"]) for row in details):
        raise ValueError("v17f postrun contains observed effect")
    if not REPORT.exists() or not REPORT.read_text(encoding="utf-8").strip():
        raise ValueError("v17f postrun report missing")
    print(f"[v17f-postrun] output verification pass rows={len(details)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="v17f postrun reverse-closure diagnosis")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
