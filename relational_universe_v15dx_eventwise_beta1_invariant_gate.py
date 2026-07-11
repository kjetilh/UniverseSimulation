#!/usr/bin/env python3
"""v0.15dx eventwise beta1 invariant gate.

This gate follows v15dw by removing the paired damage observable entirely.
Each branch evolves with its own RNG and its own id allocator. The primary
observable is the exact eventwise change in beta1 = E - N + C.

The anchor regime is tested separately from two minimal rule deformations.
An anchor pass supports only a conditional rule invariant. A nonzero delta in
the deformation probes is a counterexample to universality, not a failure of
the anchor audit and not evidence for emergent physics.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
from collections import Counter, defaultdict
from dataclasses import replace
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15dv_relabel_invariant_chord_constructor as v15dv
import relational_universe_v15dw_constructor_coupling_factorial_gate as v15dw


DOC = Path("Documentation")
PURPOSE_REF = "purpose://prompt.unknown"
TARGET_NODES = 1024
GROWTH_SEEDS = (202, 303)
PLACEMENTS = (0, 1, 2)
FRESH_SEED_DELTAS = (20507, 20563)
STEPS = 3414
CHECK_EVERY = 128

ANCHOR = "band_zero_del"
TRIAD_PROBE = "triad_002"
DELETE_PROBE = "delete_002"
REGIMES = (ANCHOR, TRIAD_PROBE, DELETE_PROBE)
BRANCHES = ("control", "perturbed")

Chord = Tuple[int, int, int]


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def safe_float(value: Any, default: float = float("nan")) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return default
    return result if math.isfinite(result) else default


def mean_defined(values: Iterable[Any]) -> float:
    finite = [safe_float(value) for value in values]
    finite = [value for value in finite if math.isfinite(value)]
    return sum(finite) / len(finite) if finite else float("nan")


def fmt(value: Any, digits: int = 3) -> str:
    number = safe_float(value)
    return "nan" if not math.isfinite(number) else f"{number:.{digits}f}"


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    records = list(rows)
    if not records:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: List[str] = []
    for row in records:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with Path(path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [fmt(row.get(field)) if isinstance(row.get(field), float) else str(row.get(field, "")) for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return lines


def chord_text(chord: Chord) -> str:
    return "-".join(str(int(node)) for node in chord)


def parse_chord(text: str) -> Chord:
    parts = tuple(int(part) for part in str(text).split("-") if part)
    if len(parts) != 3:
        raise ValueError(f"invalid chord: {text!r}")
    return parts  # type: ignore[return-value]


def beta1(state: Any, components: int) -> int:
    return int(state.g.num_edges() - state.g.num_nodes() + components)


def params_for_regime(regime: str) -> Any:
    anchor = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    if regime == ANCHOR:
        return anchor
    if regime == TRIAD_PROBE:
        return replace(anchor, p_triad=0.02, p_del=0.0)
    if regime == DELETE_PROBE:
        return replace(anchor, p_triad=0.0, p_del=0.02)
    raise ValueError(f"unknown regime {regime}")


def run_seed_for(row: Mapping[str, Any]) -> int:
    regime_code = {ANCHOR: 0, TRIAD_PROBE: 1, DELETE_PROBE: 2}[str(row["regime"])]
    branch_code = 0 if str(row["branch"]) == "control" else 1
    return (
        TARGET_NODES * 1_000_000
        + safe_int(row["growth_seed"]) * 10_000
        + safe_int(row["placement"]) * 1_000
        + safe_int(row["seed_delta"])
        + regime_code * 100_000_000
        + branch_code * 10_000_000
        + 2027
    )


def candidate_seed_for(growth_seed: int, placement: int, seed_delta: int) -> int:
    return 15_000_000_000 + growth_seed * 100_000 + placement * 10_000 + seed_delta + 173


def pre_registration_rows(base_states: Mapping[int, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for regime in REGIMES:
        growth_seeds = GROWTH_SEEDS if regime == ANCHOR else (GROWTH_SEEDS[0],)
        placements = PLACEMENTS if regime == ANCHOR else (PLACEMENTS[0],)
        for growth_seed in growth_seeds:
            base = base_states[growth_seed]
            for placement in placements:
                for seed_delta in FRESH_SEED_DELTAS:
                    candidate_seed = candidate_seed_for(growth_seed, placement, seed_delta)
                    candidate, metadata = v15dv.sample_uniform_chord_candidate(
                        base,
                        placement,
                        random.Random(candidate_seed),
                    )
                    for branch in BRANCHES:
                        row: Dict[str, Any] = {
                            "purpose_ref": PURPOSE_REF,
                            "target_nodes": TARGET_NODES,
                            "regime": regime,
                            "growth_seed": growth_seed,
                            "placement": placement,
                            "seed_delta": seed_delta,
                            "branch": branch,
                            "candidate_seed": candidate_seed,
                            "uniform_candidate": chord_text(candidate),
                            "candidate_scope": metadata["candidate_scope"],
                            "candidate_count": metadata["candidate_count"],
                            "constructor": "uniform_relabel_invariant",
                            "independent_branch_rng": 1,
                            "steps": STEPS,
                            "pre_registered_before_dynamics": 1,
                        }
                        row["run_seed"] = run_seed_for(row)
                        rows.append(row)
    return rows


def choose_family(rates: Mapping[str, float], rng: random.Random) -> Tuple[str, float]:
    total = sum(max(0.0, float(rate)) for rate in rates.values())
    if total <= 0.0:
        return "noop", 0.0
    x = rng.random() * total
    cumulative = 0.0
    family = "death"
    for candidate in ("seed", "token", "birth", "death"):
        cumulative += max(0.0, float(rates[candidate]))
        if x <= cumulative:
            family = candidate
            break
    return family, total


def expected_delta_status(event_type: str, delta: int) -> int:
    if event_type == "triad":
        return int(delta == 1)
    if event_type == "delete":
        return int(delta in {-1, 0})
    return int(delta == 0)


def single_step(
    state: Any,
    manager: Any,
    rng: random.Random,
    params: Any,
    components: int,
    step: int,
) -> Tuple[Dict[str, Any], int]:
    before_nodes = state.g.num_nodes()
    before_edges = state.g.num_edges()
    before_components = components
    before_beta1 = beta1(state, before_components)
    rates = v7.family_rates(state, params)
    family, total_rate = choose_family(rates, rng)
    if total_rate <= 0.0:
        return {
            "step": step,
            "family": "noop",
            "event_type": "noop",
            "dt": 0.0,
            "before_nodes": before_nodes,
            "after_nodes": before_nodes,
            "before_edges": before_edges,
            "after_edges": before_edges,
            "before_components": before_components,
            "after_components": before_components,
            "before_beta1": before_beta1,
            "after_beta1": before_beta1,
            "delta_nodes": 0,
            "delta_edges": 0,
            "delta_components": 0,
            "delta_beta1": 0,
            "expected_delta_match": 1,
            "component_tracker_match": 1,
        }, components

    dt = rng.expovariate(total_rate)
    state.t += dt
    kernel = v7.family_kernel(state, family, params)
    if not kernel:
        raise RuntimeError(f"empty kernel for positive-rate family {family}")
    descriptor = v7.sample_from_dist(kernel, rng)
    context = v7.apply_descriptor(state, family, descriptor, params, manager)
    event_type = str(context.get("event", "unknown"))

    after_components = before_components
    if event_type in {"delete", "triad", "swap"}:
        after_components = v7.count_components(state.g)
    component_tracker_match = 1
    if step % CHECK_EVERY == 0:
        exact_components = v7.count_components(state.g)
        component_tracker_match = int(exact_components == after_components)
        after_components = exact_components

    after_nodes = state.g.num_nodes()
    after_edges = state.g.num_edges()
    after_beta1 = beta1(state, after_components)
    delta = after_beta1 - before_beta1
    return {
        "step": step,
        "family": family,
        "event_type": event_type,
        "descriptor": repr(descriptor),
        "dt": dt,
        "before_nodes": before_nodes,
        "after_nodes": after_nodes,
        "before_edges": before_edges,
        "after_edges": after_edges,
        "before_components": before_components,
        "after_components": after_components,
        "before_beta1": before_beta1,
        "after_beta1": after_beta1,
        "delta_nodes": after_nodes - before_nodes,
        "delta_edges": after_edges - before_edges,
        "delta_components": after_components - before_components,
        "delta_beta1": delta,
        "expected_delta_match": expected_delta_status(event_type, delta),
        "component_tracker_match": component_tracker_match,
    }, after_components


def run_branch(base_state: Any, assignment: Mapping[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    state = base_state.clone()
    branch = str(assignment["branch"])
    candidate = parse_chord(str(assignment["uniform_candidate"]))
    perturbation_applied = 0
    if branch == "perturbed":
        v15dw.apply_candidate(state, candidate, "uniform_relabel_invariant")
        perturbation_applied = 1

    initial_components = v7.count_components(state.g)
    initial_beta1 = beta1(state, initial_components)
    next_node_id, next_token_id = v08b.next_ids_from_state(state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)
    rng = random.Random(safe_int(assignment["run_seed"]))
    params = params_for_regime(str(assignment["regime"]))
    components = initial_components
    events: List[Dict[str, Any]] = []
    prefix = {
        "target_nodes": TARGET_NODES,
        "regime": assignment["regime"],
        "growth_seed": safe_int(assignment["growth_seed"]),
        "placement": safe_int(assignment["placement"]),
        "seed_delta": safe_int(assignment["seed_delta"]),
        "branch": branch,
        "run_seed": safe_int(assignment["run_seed"]),
        "uniform_candidate": assignment["uniform_candidate"],
    }
    for step in range(1, STEPS + 1):
        event, components = single_step(state, manager, rng, params, components, step)
        events.append({**prefix, **event})

    exact_final_components = v7.count_components(state.g)
    final_beta1 = beta1(state, exact_final_components)
    event_counts = Counter(str(event["event_type"]) for event in events)
    nonzero = [event for event in events if safe_int(event["delta_beta1"]) != 0]
    run_row = {
        **prefix,
        "independent_branch_rng": 1,
        "perturbation_applied": perturbation_applied,
        "steps": STEPS,
        "initial_nodes": base_state.g.num_nodes(),
        "initial_edges": base_state.g.num_edges() + perturbation_applied,
        "initial_components": initial_components,
        "initial_beta1": initial_beta1,
        "final_nodes": state.g.num_nodes(),
        "final_edges": state.g.num_edges(),
        "final_components": exact_final_components,
        "final_beta1": final_beta1,
        "beta1_drift": final_beta1 - initial_beta1,
        "nonzero_beta1_event_count": len(nonzero),
        "expected_delta_violation_count": sum(1 - safe_int(event["expected_delta_match"]) for event in events),
        "component_tracker_violation_count": sum(1 - safe_int(event["component_tracker_match"]) for event in events),
        "event_counts": ";".join(f"{name}:{count}" for name, count in sorted(event_counts.items())),
        "triad_event_count": event_counts.get("triad", 0),
        "delete_event_count": event_counts.get("delete", 0),
        "swap_event_count": event_counts.get("swap", 0),
        "seed_event_count": event_counts.get("seed", 0),
        "birth_event_count": event_counts.get("birth", 0),
        "death_event_count": event_counts.get("death", 0),
    }
    return events, run_row


def transition_summary_rows(events: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[str, str], List[Mapping[str, Any]]] = defaultdict(list)
    for event in events:
        grouped[(str(event["regime"]), str(event["event_type"]))].append(event)
    rows: List[Dict[str, Any]] = []
    for (regime, event_type), group in sorted(grouped.items()):
        deltas = Counter(safe_int(event["delta_beta1"]) for event in group)
        rows.append({
            "regime": regime,
            "event_type": event_type,
            "n_events": len(group),
            "delta_beta1_counts": ";".join(f"{delta}:{count}" for delta, count in sorted(deltas.items())),
            "nonzero_rate": sum(count for delta, count in deltas.items() if delta != 0) / len(group),
            "expected_delta_match_rate": mean_defined(event["expected_delta_match"] for event in group),
            "component_tracker_match_rate": mean_defined(event["component_tracker_match"] for event in group),
        })
    return rows


def transition_algebra_rows() -> List[Dict[str, Any]]:
    return [
        {"event_type": "seed", "delta_nodes": 1, "delta_edges": 1, "delta_components": 0, "allowed_delta_beta1": "0", "status": "implementation_fact"},
        {"event_type": "birth/death/move/stuck", "delta_nodes": 0, "delta_edges": 0, "delta_components": 0, "allowed_delta_beta1": "0", "status": "implementation_fact"},
        {"event_type": "swap", "delta_nodes": 0, "delta_edges": 0, "delta_components": 0, "allowed_delta_beta1": "0", "status": "implementation_fact_runtime_audited"},
        {"event_type": "triad", "delta_nodes": 0, "delta_edges": 1, "delta_components": 0, "allowed_delta_beta1": "+1", "status": "implementation_fact_runtime_audited"},
        {"event_type": "delete", "delta_nodes": "0_or_-1", "delta_edges": -1, "delta_components": "0_or_+1", "allowed_delta_beta1": "-1_or_0", "status": "implementation_fact_runtime_audited"},
    ]


def regime_summary_rows(runs: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for run in runs:
        grouped[str(run["regime"])].append(run)
    rows: List[Dict[str, Any]] = []
    for regime, group in sorted(grouped.items()):
        rows.append({
            "regime": regime,
            "n_runs": len(group),
            "n_control": sum(str(run["branch"]) == "control" for run in group),
            "n_perturbed": sum(str(run["branch"]) == "perturbed" for run in group),
            "zero_drift_run_rate": mean_defined(int(safe_int(run["beta1_drift"]) == 0) for run in group),
            "total_nonzero_beta1_events": sum(safe_int(run["nonzero_beta1_event_count"]) for run in group),
            "total_triad_events": sum(safe_int(run["triad_event_count"]) for run in group),
            "total_delete_events": sum(safe_int(run["delete_event_count"]) for run in group),
            "expected_delta_violation_count": sum(safe_int(run["expected_delta_violation_count"]) for run in group),
            "component_tracker_violation_count": sum(safe_int(run["component_tracker_violation_count"]) for run in group),
        })
    return rows


def sector_offset_rows(runs: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    anchor = [run for run in runs if str(run["regime"]) == ANCHOR]
    grouped: Dict[Tuple[int, int, int], Dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for run in anchor:
        key = (safe_int(run["growth_seed"]), safe_int(run["placement"]), safe_int(run["seed_delta"]))
        grouped[key][str(run["branch"])] = run
    rows: List[Dict[str, Any]] = []
    for (growth_seed, placement, seed_delta), pair in sorted(grouped.items()):
        control = pair["control"]
        perturbed = pair["perturbed"]
        rows.append({
            "growth_seed": growth_seed,
            "placement": placement,
            "seed_delta": seed_delta,
            "initial_beta1_offset": safe_int(perturbed["initial_beta1"]) - safe_int(control["initial_beta1"]),
            "final_beta1_offset": safe_int(perturbed["final_beta1"]) - safe_int(control["final_beta1"]),
            "both_branches_zero_drift": int(
                safe_int(control["beta1_drift"]) == 0 and safe_int(perturbed["beta1_drift"]) == 0
            ),
        })
    return rows


def evaluation_rows(
    preregistration: Sequence[Mapping[str, Any]],
    runs: Sequence[Mapping[str, Any]],
    regimes: Sequence[Mapping[str, Any]],
    transitions: Sequence[Mapping[str, Any]],
    offsets: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    regime_by_name = {str(row["regime"]): row for row in regimes}
    anchor = regime_by_name[ANCHOR]
    triad = regime_by_name[TRIAD_PROBE]
    delete = regime_by_name[DELETE_PROBE]
    anchor_pass = (
        safe_float(anchor["zero_drift_run_rate"]) == 1.0
        and safe_int(anchor["total_nonzero_beta1_events"]) == 0
        and safe_int(anchor["expected_delta_violation_count"]) == 0
        and safe_int(anchor["component_tracker_violation_count"]) == 0
    )
    sector_pass = bool(offsets) and all(
        safe_int(row["initial_beta1_offset"]) == 1
        and safe_int(row["final_beta1_offset"]) == 1
        and safe_int(row["both_branches_zero_drift"]) == 1
        for row in offsets
    )
    triad_falsifier = safe_int(triad["total_triad_events"]) > 0 and safe_int(triad["total_nonzero_beta1_events"]) > 0
    delete_observed = safe_int(delete["total_delete_events"]) > 0
    universal_contradicted = triad_falsifier
    artifact_clean = (
        len(preregistration) == len(runs)
        and all(safe_int(row.get("pre_registered_before_dynamics")) == 1 for row in preregistration)
        and all(safe_int(row.get("independent_branch_rng")) == 1 for row in runs)
    )
    diagnosis = (
        "conditional_exact_beta1_sector_invariant_not_universal"
        if artifact_clean and anchor_pass and sector_pass and universal_contradicted
        else "eventwise_beta1_gate_inconclusive"
    )
    return [
        {"key": "scope", "value": "independent_branch_eventwise_beta1", "evidence": f"runs={len(runs)}; events={len(runs) * STEPS}"},
        {"key": "artifact_control", "value": "clean" if artifact_clean else "failed", "evidence": "pre_registered rows equal runs; independent RNG per branch"},
        {"key": "anchor_eventwise_conservation", "value": "pass" if anchor_pass else "fail", "evidence": f"zero_drift_rate={fmt(anchor['zero_drift_run_rate'])}; nonzero_events={anchor['total_nonzero_beta1_events']}"},
        {"key": "add_chord_sector_offset", "value": "pass" if sector_pass else "fail", "evidence": f"paired_assignments={len(offsets)}; required offset=1 at initial and final"},
        {"key": "triad_deformation_falsifier", "value": "pass" if triad_falsifier else "fail", "evidence": f"triad_events={triad['total_triad_events']}; nonzero_events={triad['total_nonzero_beta1_events']}"},
        {"key": "delete_deformation_coverage", "value": "pass" if delete_observed else "fail", "evidence": f"delete_events={delete['total_delete_events']}; nonzero_events={delete['total_nonzero_beta1_events']}"},
        {"key": "universal_beta1_invariance", "value": "contradicted" if universal_contradicted else "unresolved", "evidence": "one valid nonzero deformation event is a counterexample"},
        {"key": "diagnosis", "value": diagnosis, "evidence": "anchor conservation and sector offset are conditional on the frozen rule family"},
        {"key": "next_step", "value": "derive_sector_mechanism_then_test_sector_conditioned_dynamics" if diagnosis.startswith("conditional_exact") else "repair_eventwise_instrumentation", "evidence": "do not relabel algebraic conservation as emergent physics"},
    ]


def claim_rows(evaluation: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_key = {str(row["key"]): str(row["value"]) for row in evaluation}
    return [
        {
            "claim_id": "claim.v15dx.anchor-beta1-invariant",
            "claim_type": "factual",
            "strength": "assertive",
            "statement": "Every observed independent-branch transition in band_zero_del preserves beta1 exactly.",
            "evaluation": "supported" if by_key["anchor_eventwise_conservation"] == "pass" else "contradicted",
            "evidence_ref": "v15dx_transition_delta_summary.csv:band_zero_del",
        },
        {
            "claim_id": "claim.v15dx.add-chord-sector",
            "claim_type": "factual",
            "strength": "assertive",
            "statement": "The uniform add_chord perturbation creates a beta1 sector offset of exactly one that is preserved by anchor dynamics.",
            "evaluation": "supported" if by_key["add_chord_sector_offset"] == "pass" else "contradicted",
            "evidence_ref": "v15dx_sector_offsets.csv",
        },
        {
            "claim_id": "claim.v15dx.universal-beta1-invariant",
            "claim_type": "project_capability",
            "strength": "moderated",
            "statement": "Beta1 is invariant across the broader local rule family.",
            "evaluation": "contradicted" if by_key["universal_beta1_invariance"] == "contradicted" else "open",
            "evidence_ref": "v15dx_transition_delta_summary.csv:triad_002;delete_002",
        },
        {
            "claim_id": "claim.v15dx.emergent-physics",
            "claim_type": "project_capability",
            "strength": "moderated",
            "statement": "The observed beta1 conservation is evidence of emergent universe-like physics.",
            "evaluation": "unsupported",
            "evidence_ref": "v15dx_gate_evaluation.csv:diagnosis",
        },
    ]


def render_report(
    regimes: Sequence[Mapping[str, Any]],
    transitions: Sequence[Mapping[str, Any]],
    offsets: Sequence[Mapping[str, Any]],
    evaluation: Sequence[Mapping[str, Any]],
    claims: Sequence[Mapping[str, Any]],
) -> str:
    by_key = {str(row["key"]): str(row["value"]) for row in evaluation}
    lines = [
        "# Relasjonell universgraf v0.15dx: eventwise beta1 invariant gate",
        "",
        "## Formaal og maal",
        "",
        f"`purposeRef`: `{PURPOSE_REF}`.",
        "",
        "Test om `beta1 = E - N + C` er en eksakt global invariant som hver lokal interaksjon respekterer i anchor-regimet, og skill dette fra universal eller emergent fysikk.",
        "",
        "| goal | target | status |",
        "| --- | --- | --- |",
        f"| G1 anchor eventwise conservation | zero nonzero beta1 events | {'satisfied' if by_key['anchor_eventwise_conservation'] == 'pass' else 'missed'} |",
        f"| G2 add_chord sector offset | initial and final offset exactly +1 | {'satisfied' if by_key['add_chord_sector_offset'] == 'pass' else 'missed'} |",
        f"| G3 universality falsifier | observed legal deformation with nonzero beta1 delta | {'satisfied' if by_key['universal_beta1_invariance'] == 'contradicted' else 'missed'} |",
        "",
        "## Frozen scope",
        "",
        f"- target `{TARGET_NODES}`; anchor growth seeds `{';'.join(map(str, GROWTH_SEEDS))}`; placements `p0,p1,p2`",
        f"- fresh dynamic seed deltas `{';'.join(map(str, FRESH_SEED_DELTAS))}`",
        f"- `{STEPS}` transitions per branch; branches use independent RNG and independent id allocation",
        "- perturbed branches use the uniform relabel-invariant add_chord constructor",
        "- deformations change only `p_triad` or `p_del` from `0.00` to `0.02`",
        "",
        "## Algebraic transition facts",
        "",
        "| event | graph delta | beta1 consequence | status |",
        "| --- | --- | --- | --- |",
        "| seed | one node plus one edge | 0 | implementation fact |",
        "| birth/death/move/stuck | no graph change | 0 | implementation fact |",
        "| swap | remove v-u, add v-w through u-neighbor w | 0 when component count is preserved | runtime audited |",
        "| triad | add v-w where v-u-w already connects endpoints | +1 | runtime falsifier |",
        "| delete | remove v-u; bridge status determines component delta | -1 or 0 | runtime audited |",
        "",
        "These are rule-level facts. Runtime agreement checks implementation fidelity; it does not turn the identity into emergent physics.",
        "",
        "## Regime outcomes",
        "",
    ]
    lines.extend(table(regimes, ("regime", "n_runs", "zero_drift_run_rate", "total_nonzero_beta1_events", "total_triad_events", "total_delete_events", "expected_delta_violation_count")))
    lines.extend(["", "## Transition deltas", ""])
    lines.extend(table(transitions, ("regime", "event_type", "n_events", "delta_beta1_counts", "nonzero_rate", "expected_delta_match_rate")))
    lines.extend(["", "## Sector offsets", ""])
    lines.extend(table(offsets, ("growth_seed", "placement", "seed_delta", "initial_beta1_offset", "final_beta1_offset", "both_branches_zero_drift")))
    lines.extend(["", "## Claim adjudication", ""])
    lines.extend(table(claims, ("claim_id", "statement", "evaluation", "evidence_ref")))
    lines.extend(["", "## Decision", ""])
    lines.extend(table(evaluation, ("key", "value", "evidence")))
    lines.extend([
        "",
        "Den presise evidensstatusen er en betinget topologisk sektor-invariant i `band_zero_del`. Den er global i den smale betydningen at alle tillatte anchor-overganger respekterer den. Triad-deformasjonen viser samtidig at den ikke er en universell lov for hele regelfamilien.",
        "",
    ])
    return "\n".join(lines)


def render_operational(evaluation: Sequence[Mapping[str, Any]]) -> str:
    by_key = {str(row["key"]): str(row["value"]) for row in evaluation}
    return "\n".join([
        "# Operativ anbefaling v0.15dx",
        "",
        f"- `artifact_control`: `{by_key['artifact_control']}`.",
        f"- `anchor_eventwise_conservation`: `{by_key['anchor_eventwise_conservation']}`.",
        f"- `add_chord_sector_offset`: `{by_key['add_chord_sector_offset']}`.",
        f"- `universal_beta1_invariance`: `{by_key['universal_beta1_invariance']}`.",
        f"- `diagnosis`: `{by_key['diagnosis']}`.",
        f"- `next_step`: `{by_key['next_step']}`.",
        "",
        "Behold beta1 som en eksplisitt regimebetinget sektorvariabel.",
        "Ikke presenter den som emergent, Lorentz-lik eller universell invariant.",
        "Neste dynamiske sporsmaal er om sektor +0 og +1 har repeterbart ulike marginale responser under samme anchor-regler.",
        "",
    ])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reuse-existing", action="store_true")
    parser.add_argument("--out-pre-registration-csv", default=str(DOC / "v15dx_pre_registration.csv"))
    parser.add_argument("--out-event-log-csv", default=str(DOC / "v15dx_event_log.csv"))
    parser.add_argument("--out-run-summary-csv", default=str(DOC / "v15dx_run_summary.csv"))
    parser.add_argument("--out-transition-algebra-csv", default=str(DOC / "v15dx_transition_algebra.csv"))
    parser.add_argument("--out-regime-summary-csv", default=str(DOC / "v15dx_regime_summary.csv"))
    parser.add_argument("--out-transition-summary-csv", default=str(DOC / "v15dx_transition_delta_summary.csv"))
    parser.add_argument("--out-sector-offsets-csv", default=str(DOC / "v15dx_sector_offsets.csv"))
    parser.add_argument("--out-evaluation-csv", default=str(DOC / "v15dx_gate_evaluation.csv"))
    parser.add_argument("--out-claims-csv", default=str(DOC / "v15dx_claim_ledger.csv"))
    parser.add_argument("--out-report", default=str(DOC / "v15dx_eventwise_beta1_invariant_gate.md"))
    parser.add_argument("--out-operational", default=str(DOC / "v0_15dx_operativ_anbefaling.md"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.reuse_existing:
        preregistration = read_csv(args.out_pre_registration_csv)
        events = read_csv(args.out_event_log_csv)
        runs = read_csv(args.out_run_summary_csv)
    else:
        base_states, _, _ = v15dw.build_bases()
        preregistration = pre_registration_rows(base_states)
        write_csv(args.out_pre_registration_csv, preregistration)
        events: List[Dict[str, Any]] = []
        runs: List[Dict[str, Any]] = []
        for index, assignment in enumerate(preregistration, start=1):
            print(
                f"running {index}/{len(preregistration)} {assignment['regime']} "
                f"growth_seed={assignment['growth_seed']} p{assignment['placement']} "
                f"seed_delta={assignment['seed_delta']} branch={assignment['branch']}",
                flush=True,
            )
            branch_events, run = run_branch(base_states[safe_int(assignment["growth_seed"])], assignment)
            events.extend(branch_events)
            runs.append(run)
        write_csv(args.out_event_log_csv, events)
        write_csv(args.out_run_summary_csv, runs)

    if len(preregistration) != 32 or len(runs) != 32:
        raise ValueError(f"expected 32 preregistered runs, got {len(preregistration)} assignments and {len(runs)} runs")
    if len(events) != len(runs) * STEPS:
        raise ValueError(f"expected {len(runs) * STEPS} events, got {len(events)}")

    transitions = transition_summary_rows(events)
    algebra = transition_algebra_rows()
    regimes = regime_summary_rows(runs)
    offsets = sector_offset_rows(runs)
    evaluation = evaluation_rows(preregistration, runs, regimes, transitions, offsets)
    claims = claim_rows(evaluation)
    write_csv(args.out_transition_algebra_csv, algebra)
    write_csv(args.out_regime_summary_csv, regimes)
    write_csv(args.out_transition_summary_csv, transitions)
    write_csv(args.out_sector_offsets_csv, offsets)
    write_csv(args.out_evaluation_csv, evaluation)
    write_csv(args.out_claims_csv, claims)
    Path(args.out_report).write_text(render_report(regimes, transitions, offsets, evaluation, claims), encoding="utf-8")
    Path(args.out_operational).write_text(render_operational(evaluation), encoding="utf-8")
    for row in evaluation:
        print(f"{row['key']}: {row['value']} ({row['evidence']})")


if __name__ == "__main__":
    main()
