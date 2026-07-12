#!/usr/bin/env python3
"""v0.15dz local beta1-sector transport gate.

Fresh independent-sector dynamics on growth seeds 404/505. Primary observables
are within-branch changes in marked cycle-neighborhood geometry, so the trivial
initial +1 beta1 offset is excluded from the response test.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15dv_relabel_invariant_chord_constructor as v15dv
import relational_universe_v15dw_constructor_coupling_factorial_gate as v15dw
import relational_universe_v15dx_eventwise_beta1_invariant_gate as v15dx
import relational_universe_v15dy_sector_conditioned_marginal_response_gate as v15dy


DOC = Path("Documentation")
PURPOSE_REF = "purpose://prompt.unknown"
TARGET_NODES = 1024
GROWTH_SEEDS = (404, 505)
PLACEMENTS = (0, 1, 2)
FRESH_SEED_DELTAS = (21317, 21379, 21433, 21491)
SECTORS = ("beta1_base", "beta1_plus1")
STEPS = 3414
LOG_EVERY = 16
TAIL_START_FRACTION = 0.75
RADII = (1, 2, 3)

PRIMARY_METRICS = (
    "tail_delta_local_beta1_r1",
    "tail_delta_local_beta1_r2",
    "tail_delta_local_beta1_r3",
    "tail_delta_cycle_density_r2",
)
MAX_HOLM_P = 0.05
MIN_AUC_SEPARATION = 0.70
MIN_RELATIVE_MEDIAN_GAP = 0.10
MIN_PLACEMENT_DIRECTION_FRACTION = 2.0 / 3.0
MIN_CHORD_LOSS_COVERAGE = 0.25

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
    vals = [safe_float(value) for value in values]
    vals = [value for value in vals if math.isfinite(value)]
    return sum(vals) / len(vals) if vals else float("nan")


def median_defined(values: Iterable[Any]) -> float:
    vals = sorted(value for value in (safe_float(item) for item in values) if math.isfinite(value))
    if not vals:
        return float("nan")
    mid = len(vals) // 2
    return vals[mid] if len(vals) % 2 else (vals[mid - 1] + vals[mid]) / 2.0


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
        vals = [fmt(row.get(field)) if isinstance(row.get(field), float) else str(row.get(field, "")) for field in fields]
        lines.append("| " + " | ".join(vals) + " |")
    return lines


def chord_text(chord: Chord) -> str:
    return "-".join(str(int(node)) for node in chord)


def parse_chord(text: str) -> Chord:
    parts = tuple(int(part) for part in str(text).split("-") if part)
    if len(parts) != 3:
        raise ValueError(f"invalid chord {text!r}")
    return parts  # type: ignore[return-value]


def build_bases() -> Tuple[Dict[int, Any], List[Mapping[str, Any]]]:
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    states, rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    by_seed = {seed: states[(ensembles[0].name, seed)] for seed in GROWTH_SEEDS}
    summary = [dict(row) for row in v10e.summarize_bases(rows) if safe_int(row["target_nodes"]) == TARGET_NODES]
    return by_seed, summary


def candidate_seed_for(growth_seed: int, placement: int, seed_delta: int) -> int:
    return 15_000_000_000 + growth_seed * 100_000 + placement * 10_000 + seed_delta + 397


def run_seed_for(growth_seed: int, placement: int, seed_delta: int, sector: str) -> int:
    sector_code = 0 if sector == "beta1_base" else 1
    return TARGET_NODES * 1_000_000 + growth_seed * 10_000 + placement * 1_000 + seed_delta + sector_code * 10_000_000 + 2143


def pre_registration_rows(base_states: Mapping[int, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for growth_seed in GROWTH_SEEDS:
        base = base_states[growth_seed]
        for placement in PLACEMENTS:
            for seed_delta in FRESH_SEED_DELTAS:
                candidate_seed = candidate_seed_for(growth_seed, placement, seed_delta)
                candidate, metadata = v15dv.sample_uniform_chord_candidate(base, placement, random.Random(candidate_seed))
                for sector in SECTORS:
                    rows.append({
                        "purpose_ref": PURPOSE_REF,
                        "target_nodes": TARGET_NODES,
                        "regime": "band_zero_del",
                        "growth_seed": growth_seed,
                        "placement": placement,
                        "seed_delta": seed_delta,
                        "sector": sector,
                        "run_seed": run_seed_for(growth_seed, placement, seed_delta, sector),
                        "candidate_seed": candidate_seed,
                        "uniform_candidate": chord_text(candidate),
                        "candidate_scope": metadata["candidate_scope"],
                        "candidate_count": metadata["candidate_count"],
                        "constructor": "uniform_relabel_invariant",
                        "steps": STEPS,
                        "log_every": LOG_EVERY,
                        "primary_metrics": ";".join(PRIMARY_METRICS),
                        "raw_initial_beta1_offset_excluded": 1,
                        "pre_registered_before_dynamics": 1,
                    })
    return rows


def ball_nodes(g: Any, support: Set[int], radius: int) -> Set[int]:
    distances = v7.bfs_distances(g, support)
    return {node for node, distance in distances.items() if distance <= radius}


def induced_metrics(g: Any, nodes: Set[int]) -> Dict[str, Any]:
    present = {node for node in nodes if node in g.adj}
    edges = sum(1 for a in present for b in g.neighbors(a) if b in present and a < b)
    sub = v7.UGraph()
    for node in present:
        sub.add_node(node)
    for a in present:
        for b in g.neighbors(a):
            if b in present and a < b:
                sub.add_edge(a, b)
    components = v7.count_components(sub) if present else 0
    beta1 = edges - len(present) + components
    boundary = sum(1 for node in present for neighbor in g.neighbors(node) if neighbor not in present)
    return {
        "nodes": len(present),
        "edges": edges,
        "components": components,
        "beta1": beta1,
        "cycle_density": beta1 / max(1, len(present)),
        "boundary": boundary,
        "boundary_to_volume": boundary / max(1, len(present)),
    }


def local_snapshot(state: Any, support: Set[int], chord: Chord) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "chord_present": int(state.g.has_edge(chord[0], chord[2])),
        "global_beta1": v15dx.beta1(state, v7.count_components(state.g)),
        "tokens_total": state.token_count(),
    }
    for radius in RADII:
        nodes = ball_nodes(state.g, support, radius)
        metrics = induced_metrics(state.g, nodes)
        token_count = sum(node in nodes for node in state.token_pos.values())
        for key, value in metrics.items():
            result[f"local_{key}_r{radius}"] = value
        result[f"local_tokens_r{radius}"] = token_count
        result[f"local_token_fraction_r{radius}"] = token_count / max(1, state.token_count())
    return result


def touched_nodes(event_type: str, descriptor: Tuple[Any, ...], context: Mapping[str, Any]) -> Set[int]:
    nodes: Set[int] = set()
    for key in ("host", "new_node", "node", "node_before", "v_before", "u_before"):
        value = context.get(key)
        if isinstance(value, int):
            nodes.add(value)
    if event_type in {"triad", "swap"} and len(descriptor) >= 5:
        nodes.add(int(descriptor[4]))
    return nodes


def single_step_local(state: Any, manager: Any, rng: random.Random, params: Any, components: int, step: int) -> Tuple[Dict[str, Any], int]:
    before_beta1 = v15dx.beta1(state, components)
    rates = v7.family_rates(state, params)
    family, total_rate = v15dx.choose_family(rates, rng)
    if total_rate <= 0.0:
        return {"event_type": "noop", "dt": 0.0, "delta_beta1": 0, "touched_nodes": set()}, components
    dt = rng.expovariate(total_rate)
    state.t += dt
    kernel = v7.family_kernel(state, family, params)
    if not kernel:
        raise RuntimeError(f"empty kernel for positive family {family}")
    descriptor = v7.sample_from_dist(kernel, rng)
    context = v7.apply_descriptor(state, family, descriptor, params, manager)
    event_type = str(context.get("event", "unknown"))
    after_components = components
    if event_type in {"delete", "triad", "swap"} or step % 128 == 0:
        after_components = v7.count_components(state.g)
    after_beta1 = v15dx.beta1(state, after_components)
    return {
        "event_type": event_type,
        "dt": dt,
        "delta_beta1": after_beta1 - before_beta1,
        "touched_nodes": touched_nodes(event_type, descriptor, context),
    }, after_components


def run_sector(base_state: Any, assignment: Mapping[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    state = base_state.clone()
    sector = str(assignment["sector"])
    chord = parse_chord(str(assignment["uniform_candidate"]))
    support = set(chord)
    if sector == "beta1_plus1":
        v15dw.apply_candidate(state, chord, "uniform_relabel_invariant")
    initial = local_snapshot(state, support, chord)
    initial_fixed_ball_r2 = ball_nodes(state.g, support, 2)
    initial_global_beta1 = safe_int(initial["global_beta1"])
    components = v7.count_components(state.g)
    next_node_id, next_token_id = v08b.next_ids_from_state(state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)
    rng = random.Random(safe_int(assignment["run_seed"]))
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])

    rows: List[Dict[str, Any]] = []
    local_event_count = 0
    event_count = 0
    beta1_violation_count = 0
    first_chord_absent_step = -1

    def append_snapshot(step: int) -> None:
        snapshot = local_snapshot(state, support, chord)
        row: Dict[str, Any] = {
            "target_nodes": TARGET_NODES,
            "growth_seed": safe_int(assignment["growth_seed"]),
            "placement": safe_int(assignment["placement"]),
            "seed_delta": safe_int(assignment["seed_delta"]),
            "sector": sector,
            "run_seed": safe_int(assignment["run_seed"]),
            "uniform_candidate": assignment["uniform_candidate"],
            "step": step,
            "time": state.t,
            "local_event_rate_fixed_r2": local_event_count / max(1, event_count),
            **snapshot,
        }
        for radius in RADII:
            row[f"delta_local_beta1_r{radius}"] = safe_float(snapshot[f"local_beta1_r{radius}"]) - safe_float(initial[f"local_beta1_r{radius}"])
            row[f"delta_cycle_density_r{radius}"] = safe_float(snapshot[f"local_cycle_density_r{radius}"]) - safe_float(initial[f"local_cycle_density_r{radius}"])
            row[f"delta_local_token_fraction_r{radius}"] = safe_float(snapshot[f"local_token_fraction_r{radius}"]) - safe_float(initial[f"local_token_fraction_r{radius}"])
        rows.append(row)

    append_snapshot(0)
    for step in range(1, STEPS + 1):
        event, components = single_step_local(state, manager, rng, params, components, step)
        event_count += 1
        beta1_violation_count += int(safe_int(event["delta_beta1"]) != 0)
        if set(event["touched_nodes"]).intersection(initial_fixed_ball_r2):
            local_event_count += 1
        if first_chord_absent_step < 0 and not state.g.has_edge(chord[0], chord[2]):
            first_chord_absent_step = step
        if step % LOG_EVERY == 0 or step == STEPS:
            append_snapshot(step)

    tail_index = int(math.floor(TAIL_START_FRACTION * len(rows)))
    tail = rows[tail_index:]
    run: Dict[str, Any] = {
        "target_nodes": TARGET_NODES,
        "growth_seed": safe_int(assignment["growth_seed"]),
        "placement": safe_int(assignment["placement"]),
        "seed_delta": safe_int(assignment["seed_delta"]),
        "sector": sector,
        "run_seed": safe_int(assignment["run_seed"]),
        "uniform_candidate": assignment["uniform_candidate"],
        "initial_global_beta1": initial_global_beta1,
        "final_global_beta1": safe_int(rows[-1]["global_beta1"]),
        "global_beta1_drift": safe_int(rows[-1]["global_beta1"]) - initial_global_beta1,
        "beta1_violation_count": beta1_violation_count,
        "first_chord_absent_step": first_chord_absent_step,
        "chord_lost": int(first_chord_absent_step >= 0),
        "tail_chord_survival_rate": mean_defined(row["chord_present"] for row in tail),
        "tail_local_event_rate_fixed_r2": mean_defined(row["local_event_rate_fixed_r2"] for row in tail),
        "tail_delta_local_token_fraction_r2": mean_defined(row["delta_local_token_fraction_r2"] for row in tail),
    }
    for radius in RADII:
        run[f"initial_local_beta1_r{radius}"] = initial[f"local_beta1_r{radius}"]
        run[f"tail_delta_local_beta1_r{radius}"] = mean_defined(row[f"delta_local_beta1_r{radius}"] for row in tail)
        run[f"tail_delta_cycle_density_r{radius}"] = mean_defined(row[f"delta_cycle_density_r{radius}"] for row in tail)
    return rows, run


def comparison_rows(runs: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    paired: Dict[Tuple[int, int, int], Dict[str, Mapping[str, Any]]] = defaultdict(dict)
    for run in runs:
        key = (safe_int(run["growth_seed"]), safe_int(run["placement"]), safe_int(run["seed_delta"]))
        paired[key][str(run["sector"])] = run
    if len(paired) != 24 or any(set(pair) != set(SECTORS) for pair in paired.values()):
        raise ValueError("expected 24 complete sector pairs")
    rows: List[Dict[str, Any]] = []
    for metric in PRIMARY_METRICS:
        base_values: List[float] = []
        plus_values: List[float] = []
        differences: List[float] = []
        by_growth: Dict[int, List[float]] = defaultdict(list)
        by_placement: Dict[int, List[float]] = defaultdict(list)
        for (growth_seed, placement, _), pair in sorted(paired.items()):
            base = safe_float(pair["beta1_base"][metric])
            plus = safe_float(pair["beta1_plus1"][metric])
            difference = plus - base
            base_values.append(base)
            plus_values.append(plus)
            differences.append(difference)
            by_growth[growth_seed].append(difference)
            by_placement[placement].append(difference)
        median_base = median_defined(base_values)
        median_plus = median_defined(plus_values)
        median_difference = median_defined(differences)
        global_direction = v15dy.direction(median_difference)
        growth_match = sum(v15dy.direction(median_defined(values)) == global_direction and global_direction != 0 for values in by_growth.values()) / len(GROWTH_SEEDS)
        placement_match = sum(v15dy.direction(median_defined(values)) == global_direction and global_direction != 0 for values in by_placement.values()) / len(PLACEMENTS)
        auc = v15dy.auc_score(plus_values, base_values)
        positive = sum(value > 0 for value in differences)
        negative = sum(value < 0 for value in differences)
        nonzero = positive + negative
        rows.append({
            "metric": metric,
            "n_pairs": len(differences),
            "median_beta1_base": median_base,
            "median_beta1_plus1": median_plus,
            "median_paired_difference": median_difference,
            "relative_median_gap": abs(median_plus - median_base) / max(abs(median_base), 1.0 / STEPS),
            "positive_pair_count": positive,
            "negative_pair_count": negative,
            "zero_pair_count": len(differences) - nonzero,
            "sign_consistency": max(positive, negative) / nonzero if nonzero else 0.0,
            "sign_test_p": v15dy.sign_test_p(differences),
            "auc_plus1_vs_base": auc,
            "auc_separation": max(auc, 1.0 - auc),
            "global_direction": global_direction,
            "growth_seed_direction_match": growth_match,
            "placement_direction_match": placement_match,
        })
    v15dy.holm_adjust(rows)
    for row in rows:
        row["metric_gate_pass"] = int(
            safe_float(row["holm_p"]) <= MAX_HOLM_P
            and safe_float(row["auc_separation"]) >= MIN_AUC_SEPARATION
            and safe_float(row["relative_median_gap"]) >= MIN_RELATIVE_MEDIAN_GAP
            and safe_float(row["growth_seed_direction_match"]) == 1.0
            and safe_float(row["placement_direction_match"]) >= MIN_PLACEMENT_DIRECTION_FRACTION
        )
        row["metric_status"] = "local_transport_candidate" if safe_int(row["metric_gate_pass"]) else "not_supported"
    return rows


def diagnostic_rows(runs: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for sector in SECTORS:
        group = [run for run in runs if str(run["sector"]) == sector]
        rows.append({
            "sector": sector,
            "n_runs": len(group),
            "plus1_chord_loss_rate": mean_defined(run["chord_lost"] for run in group) if sector == "beta1_plus1" else float("nan"),
            "mean_tail_candidate_edge_presence_rate": mean_defined(run["tail_chord_survival_rate"] for run in group),
            "mean_tail_local_event_rate_fixed_r2": mean_defined(run["tail_local_event_rate_fixed_r2"] for run in group),
            "mean_tail_delta_local_token_fraction_r2": mean_defined(run["tail_delta_local_token_fraction_r2"] for run in group),
            "global_beta1_clean_rate": mean_defined(int(safe_int(run["global_beta1_drift"]) == 0 and safe_int(run["beta1_violation_count"]) == 0) for run in group),
        })
    return rows


def evaluation_rows(preregistration: Sequence[Mapping[str, Any]], runs: Sequence[Mapping[str, Any]], comparisons: Sequence[Mapping[str, Any]], diagnostics: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    artifact_clean = len(preregistration) == 48 and len(runs) == 48 and len({safe_int(row["run_seed"]) for row in preregistration}) == 48 and all(safe_int(row["pre_registered_before_dynamics"]) == 1 for row in preregistration)
    invariant_clean = all(safe_int(run["global_beta1_drift"]) == 0 and safe_int(run["beta1_violation_count"]) == 0 for run in runs)
    passing = [str(row["metric"]) for row in comparisons if safe_int(row["metric_gate_pass"]) == 1]
    plus_diag = next(row for row in diagnostics if str(row["sector"]) == "beta1_plus1")
    chord_loss_coverage = safe_float(plus_diag["plus1_chord_loss_rate"])
    if not artifact_clean or not invariant_clean:
        diagnosis = "local_sector_transport_instrumentation_failed"
        next_step = "repair_local_cycle_instrumentation"
    elif passing and chord_loss_coverage >= MIN_CHORD_LOSS_COVERAGE:
        diagnosis = "local_beta1_sector_transport_candidate"
        next_step = "fresh_base_holdout_conditioned_on_chord_loss"
    elif passing:
        diagnosis = "static_chord_footprint_unresolved"
        next_step = "extend_budget_only_until_chord_loss_coverage_is_adequate"
    else:
        diagnosis = "no_adjusted_local_beta1_sector_response_detected"
        next_step = "retire_beta1_as_dynamic_track_keep_as_conditional_sector_label"
    return [
        {"key": "scope", "value": "fresh_local_cycle_neighborhood_response", "evidence": f"runs={len(runs)}; pairs={len(runs)//2}; snapshots_per_run={1 + math.ceil(STEPS / LOG_EVERY)}"},
        {"key": "artifact_control", "value": "clean" if artifact_clean else "failed", "evidence": "48 preregistered unique independent runs"},
        {"key": "global_beta1_conservation", "value": "pass" if invariant_clean else "fail", "evidence": "zero eventwise and final beta1 drift required"},
        {"key": "local_primary_gate", "value": "pass" if passing else "fail", "evidence": f"passing_metrics={';'.join(passing) if passing else 'none'}"},
        {"key": "plus1_chord_loss_coverage", "value": fmt(chord_loss_coverage), "evidence": f"minimum_for_transport_claim={MIN_CHORD_LOSS_COVERAGE}"},
        {"key": "diagnosis", "value": diagnosis, "evidence": "raw initial +1 offset excluded; global v15dy metrics remain negative controls"},
        {"key": "next_step", "value": next_step, "evidence": "predeclared stop rule; no metric refit"},
    ]


def claim_rows(evaluation: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_key = {str(row["key"]): str(row["value"]) for row in evaluation}
    return [
        {"claim_id": "claim.v15dz.local-sector-response", "claim_type": "statistical", "strength": "moderated", "statement": "The beta1 +1 sector changes adjusted local cycle-neighborhood dynamics under band_zero_del.", "evaluation": "supported_candidate" if by_key["local_primary_gate"] == "pass" else "unsupported", "evidence_ref": "v15dz_local_observable_comparisons.csv"},
        {"claim_id": "claim.v15dz.transport-beyond-chord", "claim_type": "causal", "strength": "moderated", "statement": "Any local sector response persists beyond the original chord edge.", "evaluation": "open" if by_key["diagnosis"] == "static_chord_footprint_unresolved" else "supported_candidate" if by_key["diagnosis"] == "local_beta1_sector_transport_candidate" else "unsupported", "evidence_ref": "v15dz_sector_diagnostics.csv"},
        {"claim_id": "claim.v15dz.physical-topological-charge", "claim_type": "project_capability", "strength": "moderated", "statement": "The beta1 sector is a physical topological charge analogous to a particle property.", "evaluation": "unsupported", "evidence_ref": "v15dz_gate_evaluation.csv:diagnosis"},
    ]


def render_report(comparisons: Sequence[Mapping[str, Any]], diagnostics: Sequence[Mapping[str, Any]], evaluation: Sequence[Mapping[str, Any]], claims: Sequence[Mapping[str, Any]]) -> str:
    by_key = {str(row["key"]): str(row["value"]) for row in evaluation}
    lines = [
        "# Relasjonell universgraf v0.15dz: local beta1-sector transport gate",
        "",
        "## Formaal og maal",
        "",
        f"`purposeRef`: `{PURPOSE_REF}`.",
        "",
        "Test om beta1-sektor +1 har justert lokal cycle-neighborhood-dynamikk utover den trivielle initiale chorden.",
        "",
        "| goal | target | status |",
        "| --- | --- | --- |",
        f"| G1 clean fresh holdout | 48 independent runs; zero invariant violations | {'satisfied' if by_key['artifact_control'] == 'clean' and by_key['global_beta1_conservation'] == 'pass' else 'missed'} |",
        f"| G2 adjusted local response | at least one frozen local metric passes | {'satisfied' if by_key['local_primary_gate'] == 'pass' else 'missed'} |",
        "| G3 stop decision | transport, static footprint, or retire | satisfied |",
        "",
        "## Frozen design",
        "",
        f"- target `{TARGET_NODES}`; growth seeds `{';'.join(map(str, GROWTH_SEEDS))}`; placements `p0,p1,p2`",
        f"- fresh seed deltas `{';'.join(map(str, FRESH_SEED_DELTAS))}`; `{STEPS}` events; log every `{LOG_EVERY}`",
        "- independent base/+1 branches; uniform relabel-invariant add_chord",
        f"- primary metrics: `{';'.join(PRIMARY_METRICS)}`",
        "- every primary metric is a within-branch change from its own t0 local geometry",
        "- chord survival, local token occupancy and local event incidence are diagnostics only",
        "",
        "## Local observable comparisons",
        "",
    ]
    lines.extend(table(comparisons, ("metric", "n_pairs", "median_beta1_base", "median_beta1_plus1", "median_paired_difference", "relative_median_gap", "sign_consistency", "holm_p", "auc_separation", "growth_seed_direction_match", "placement_direction_match", "metric_status")))
    lines.extend(["", "## Mechanism diagnostics", ""])
    lines.extend(table(diagnostics, ("sector", "n_runs", "plus1_chord_loss_rate", "mean_tail_candidate_edge_presence_rate", "mean_tail_local_event_rate_fixed_r2", "mean_tail_delta_local_token_fraction_r2", "global_beta1_clean_rate")))
    lines.extend(["", "## Claim adjudication", ""])
    lines.extend(table(claims, ("claim_id", "statement", "evaluation", "evidence_ref")))
    lines.extend(["", "## Decision", ""])
    lines.extend(table(evaluation, ("key", "value", "evidence")))
    lines.extend(["", "A negative result activates the preregistered stop rule for beta1 as a dynamic track. The exact conditional sector invariant remains valid independently of this response gate.", ""])
    return "\n".join(lines)


def render_operational(evaluation: Sequence[Mapping[str, Any]]) -> str:
    by_key = {str(row["key"]): str(row["value"]) for row in evaluation}
    return "\n".join([
        "# Operativ anbefaling v0.15dz",
        "",
        f"- `artifact_control`: `{by_key['artifact_control']}`.",
        f"- `global_beta1_conservation`: `{by_key['global_beta1_conservation']}`.",
        f"- `local_primary_gate`: `{by_key['local_primary_gate']}`.",
        f"- `plus1_chord_loss_coverage`: `{by_key['plus1_chord_loss_coverage']}`.",
        f"- `diagnosis`: `{by_key['diagnosis']}`.",
        f"- `next_step`: `{by_key['next_step']}`.",
        "",
        "Ikke bruk raw lokal +1 beta1 eller chord survival som primary response.",
        "Ved negativ gate: behold beta1 som eksakt regimebetinget sektorlabel, men avslutt dynamisk beta1-refinement.",
        "",
    ])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reuse-existing", action="store_true")
    parser.add_argument("--out-pre-registration-csv", default=str(DOC / "v15dz_pre_registration.csv"))
    parser.add_argument("--out-snapshots-csv", default=str(DOC / "v15dz_local_snapshots.csv"))
    parser.add_argument("--out-runs-csv", default=str(DOC / "v15dz_run_summary.csv"))
    parser.add_argument("--out-comparisons-csv", default=str(DOC / "v15dz_local_observable_comparisons.csv"))
    parser.add_argument("--out-diagnostics-csv", default=str(DOC / "v15dz_sector_diagnostics.csv"))
    parser.add_argument("--out-evaluation-csv", default=str(DOC / "v15dz_gate_evaluation.csv"))
    parser.add_argument("--out-claims-csv", default=str(DOC / "v15dz_claim_ledger.csv"))
    parser.add_argument("--out-target-csv", default=str(DOC / "v15dz_target_summary.csv"))
    parser.add_argument("--out-report", default=str(DOC / "v15dz_local_sector_transport_gate.md"))
    parser.add_argument("--out-operational", default=str(DOC / "v0_15dz_operativ_anbefaling.md"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.reuse_existing:
        preregistration = read_csv(args.out_pre_registration_csv)
        snapshots = read_csv(args.out_snapshots_csv)
        runs = read_csv(args.out_runs_csv)
    else:
        base_states, target_summary = build_bases()
        preregistration = pre_registration_rows(base_states)
        write_csv(args.out_pre_registration_csv, preregistration)
        write_csv(args.out_target_csv, target_summary)
        snapshots: List[Dict[str, Any]] = []
        runs: List[Dict[str, Any]] = []
        for index, assignment in enumerate(preregistration, start=1):
            print(f"running {index}/{len(preregistration)} growth_seed={assignment['growth_seed']} p{assignment['placement']} seed_delta={assignment['seed_delta']} sector={assignment['sector']}", flush=True)
            run_snapshots, run = run_sector(base_states[safe_int(assignment["growth_seed"])], assignment)
            snapshots.extend(run_snapshots)
            runs.append(run)
        write_csv(args.out_snapshots_csv, snapshots)
        write_csv(args.out_runs_csv, runs)
    expected_snapshots = 48 * (1 + math.ceil(STEPS / LOG_EVERY))
    if len(preregistration) != 48 or len(runs) != 48 or len(snapshots) != expected_snapshots:
        raise ValueError(f"v15dz data shape mismatch: assignments={len(preregistration)} runs={len(runs)} snapshots={len(snapshots)} expected_snapshots={expected_snapshots}")
    comparisons = comparison_rows(runs)
    diagnostics = diagnostic_rows(runs)
    evaluation = evaluation_rows(preregistration, runs, comparisons, diagnostics)
    claims = claim_rows(evaluation)
    write_csv(args.out_comparisons_csv, comparisons)
    write_csv(args.out_diagnostics_csv, diagnostics)
    write_csv(args.out_evaluation_csv, evaluation)
    write_csv(args.out_claims_csv, claims)
    Path(args.out_report).write_text(render_report(comparisons, diagnostics, evaluation, claims), encoding="utf-8")
    Path(args.out_operational).write_text(render_operational(evaluation), encoding="utf-8")
    for row in evaluation:
        print(f"{row['key']}: {row['value']} ({row['evidence']})")


if __name__ == "__main__":
    main()
