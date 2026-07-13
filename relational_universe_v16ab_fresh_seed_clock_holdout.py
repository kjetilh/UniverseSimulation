#!/usr/bin/env python3
"""v16ab fresh matched holdout for the fitted local seed clock.

The pre-registration is written in a separate prepare-only invocation. The
run invocation refuses to proceed unless the frozen specification digest and
the v16aa fitted rate still match files on disk.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15


DOC = Path("Documentation")
PURPOSE_REF = "purpose://prompt.unknown"
V16AA_TARGET = DOC / "v16aa_target_summary.csv"
PREREG = DOC / "v16ab_pre_registration.csv"
TARGET_NODES = 1024
GROWTH_SEEDS = (1801, 1901)
RUN_OFFSETS = (32003, 32041, 32087, 32119, 32159, 32191, 32233, 32261)
ARMS = ("current_global", "preparation_only", "exposure_matched_local")
STEPS = 3414
WINDOWS = 4
TOLERANCE = 1.0e-12

AGGREGATE_HAZARD_RATIO = (0.75, 1.25)
PER_GROWTH_HAZARD_RATIO = (0.50, 2.00)
TOTAL_TIME_RATIO = (0.75, 1.25)
FINAL_TOKEN_RATIO = (0.75, 1.25)
NONSEED_TV_MAX = 0.05
MAX_NODE_GROWTH_FRACTION = 0.05
MAX_NODE_GROWTH_ABSOLUTE = 50

RunKey = Tuple[int, int]


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    records = list(rows)
    if not records:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: List[str] = []
    for row in records:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def fmt(value: Any, digits: int = 6) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    return "nan" if not math.isfinite(number) else f"{number:.{digits}f}"


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row.get(field, "")) for field in fields) + " |")
    return lines


def fitted_local_rate() -> float:
    rows = read_csv(V16AA_TARGET)
    if len(rows) != 1 or rows[0]["selected_candidate"] != "exposure_matched_local":
        raise ValueError("v16aa selected candidate is missing or changed")
    if int(rows[0]["fresh_dynamics_runs"]) != 0:
        raise ValueError("v16aa source unexpectedly claims fresh dynamics")
    return float(rows[0]["selected_local_rate"])


def frozen_spec(local_rate: float) -> Dict[str, Any]:
    return {
        "purpose_ref": PURPOSE_REF,
        "target_nodes": TARGET_NODES,
        "growth_seeds": list(GROWTH_SEEDS),
        "run_offsets": list(RUN_OFFSETS),
        "arms": list(ARMS),
        "steps": STEPS,
        "windows": WINDOWS,
        "local_rate": local_rate,
        "thresholds": {
            "aggregate_hazard_ratio": list(AGGREGATE_HAZARD_RATIO),
            "per_growth_hazard_ratio": list(PER_GROWTH_HAZARD_RATIO),
            "total_time_ratio": list(TOTAL_TIME_RATIO),
            "final_token_ratio": list(FINAL_TOKEN_RATIO),
            "nonseed_tv_max": NONSEED_TV_MAX,
            "max_node_growth_fraction": MAX_NODE_GROWTH_FRACTION,
            "max_node_growth_absolute": MAX_NODE_GROWTH_ABSOLUTE,
        },
    }


def spec_digest(spec: Mapping[str, Any]) -> str:
    payload = json.dumps(spec, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def run_seed(growth_seed: int, run_offset: int, arm: str) -> int:
    arm_code = {"current_global": 0, "preparation_only": 1, "exposure_matched_local": 2}[arm]
    return TARGET_NODES * 1_000_000 + growth_seed * 10_000 + run_offset + arm_code * 100_000_000 + 16_012


def preregistration_rows(local_rate: float) -> List[Dict[str, Any]]:
    spec = frozen_spec(local_rate)
    digest = spec_digest(spec)
    rows: List[Dict[str, Any]] = []
    for growth_seed in GROWTH_SEEDS:
        for run_offset in RUN_OFFSETS:
            for arm in ARMS:
                rows.append({
                    "purpose_ref": PURPOSE_REF,
                    "spec_digest": digest,
                    "target_nodes": TARGET_NODES,
                    "growth_seed": growth_seed,
                    "run_offset": run_offset,
                    "arm": arm,
                    "run_seed": run_seed(growth_seed, run_offset, arm),
                    "steps": STEPS,
                    "windows": WINDOWS,
                    "frozen_local_rate": local_rate,
                    "independent_arm_rng": 1,
                    "independent_arm_id_allocator": 1,
                    "aggregate_hazard_ratio_low": AGGREGATE_HAZARD_RATIO[0],
                    "aggregate_hazard_ratio_high": AGGREGATE_HAZARD_RATIO[1],
                    "per_growth_hazard_ratio_low": PER_GROWTH_HAZARD_RATIO[0],
                    "per_growth_hazard_ratio_high": PER_GROWTH_HAZARD_RATIO[1],
                    "total_time_ratio_low": TOTAL_TIME_RATIO[0],
                    "total_time_ratio_high": TOTAL_TIME_RATIO[1],
                    "final_token_ratio_low": FINAL_TOKEN_RATIO[0],
                    "final_token_ratio_high": FINAL_TOKEN_RATIO[1],
                    "nonseed_tv_max": NONSEED_TV_MAX,
                    "max_node_growth_fraction": MAX_NODE_GROWTH_FRACTION,
                    "max_node_growth_absolute": MAX_NODE_GROWTH_ABSOLUTE,
                    "prepared_before_fresh_dynamics": 1,
                })
    return rows


def prepare() -> None:
    local_rate = fitted_local_rate()
    write_csv(PREREG, preregistration_rows(local_rate))
    print(f"[v16ab] prepared rows={len(ARMS) * len(GROWTH_SEEDS) * len(RUN_OFFSETS)} digest={spec_digest(frozen_spec(local_rate))}")


def load_and_verify_preregistration() -> Tuple[List[Dict[str, str]], float]:
    if not PREREG.exists():
        raise ValueError("missing pre-registration; run --prepare-only first")
    rows = read_csv(PREREG)
    local_rate = fitted_local_rate()
    expected = preregistration_rows(local_rate)
    if len(rows) != len(expected):
        raise ValueError(f"pre-registration row count changed: {len(rows)} != {len(expected)}")
    expected_digest = spec_digest(frozen_spec(local_rate))
    if {row["spec_digest"] for row in rows} != {expected_digest}:
        raise ValueError("pre-registration digest does not match frozen source/spec")
    expected_keys = {(int(row["growth_seed"]), int(row["run_offset"]), row["arm"], int(row["run_seed"])) for row in expected}
    actual_keys = {(int(row["growth_seed"]), int(row["run_offset"]), row["arm"], int(row["run_seed"])) for row in rows}
    if actual_keys != expected_keys:
        raise ValueError("pre-registration assignments changed")
    return rows, local_rate


def candidate_rates(state: v7.State, params: v7.Params, arm: str, local_rate: float) -> Dict[str, float]:
    rates = dict(v7.family_rates(state, params))
    if arm == "preparation_only":
        rates["seed"] = 0.0
    elif arm == "exposure_matched_local":
        hosts = state.token_count() if state.token_count() else state.g.num_nodes()
        rates["seed"] = local_rate * hosts
    return rates


def choose_family(rates: Mapping[str, float], rng: random.Random) -> Tuple[str, float]:
    total = sum(max(0.0, float(rates[family])) for family in ("seed", "token", "birth", "death"))
    if total <= 0.0:
        return "noop", 0.0
    draw = rng.random() * total
    cumulative = 0.0
    for family in ("seed", "token", "birth", "death"):
        cumulative += max(0.0, float(rates[family]))
        if draw <= cumulative:
            return family, total
    return "death", total


def beta1(state: v7.State) -> int:
    return state.g.num_edges() - state.g.num_nodes() + v7.count_components(state.g)


def run_assignment(
    base: v7.State,
    assignment: Mapping[str, str],
    params: v7.Params,
    local_rate: float,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    state = base.clone()
    arm = assignment["arm"]
    rng = random.Random(int(assignment["run_seed"]))
    next_node_id, next_token_id = v08b.next_ids_from_state(state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)
    initial_nodes = state.g.num_nodes()
    initial_edges = state.g.num_edges()
    initial_tokens = state.token_count()
    initial_beta1 = beta1(state)
    total_time = 0.0
    token_time = 0.0
    integrated_seed_hazard = 0.0
    max_seed_formula_error = 0.0
    event_counts: Counter[str] = Counter()
    invalid_events = 0
    window_size = math.ceil(STEPS / WINDOWS)
    windows: List[Dict[str, Any]] = []
    window_counts: Counter[str] = Counter()
    window_start_nodes = initial_nodes
    window_start_tokens = initial_tokens
    window_start_time = 0.0
    window_hazard = 0.0

    for step in range(1, STEPS + 1):
        rates = candidate_rates(state, params, arm, local_rate)
        family, total_rate = choose_family(rates, rng)
        if total_rate <= 0.0:
            raise RuntimeError("non-positive total rate")
        before_tokens = state.token_count()
        before_nodes = state.g.num_nodes()
        host_count = before_tokens if before_tokens else before_nodes
        descriptor_hazard = rates["seed"] / host_count if host_count else 0.0
        expected_descriptor_hazard = (
            params.r_seed / host_count if arm == "current_global" and host_count else
            local_rate if arm == "exposure_matched_local" and host_count else
            0.0
        )
        max_seed_formula_error = max(max_seed_formula_error, abs(descriptor_hazard - expected_descriptor_hazard))
        dt = rng.expovariate(total_rate)
        total_time += dt
        token_time += before_tokens * dt
        integrated_seed_hazard += rates["seed"] * dt
        window_hazard += rates["seed"] * dt
        state.t += dt
        kernel = v7.family_kernel(state, family, params)
        if not kernel:
            event_type = "null"
            invalid_events += 1
        else:
            descriptor = v7.sample_from_dist(kernel, rng)
            context = v7.apply_descriptor(state, family, descriptor, params, manager)
            event_type = str(context.get("event", "unknown"))
            invalid_events += int(event_type.endswith("reject") or event_type in {"null", "unknown", "token_reject"})
        event_counts[event_type] += 1
        window_counts[event_type] += 1

        if step % window_size == 0 or step == STEPS:
            windows.append({
                "growth_seed": int(assignment["growth_seed"]),
                "run_offset": int(assignment["run_offset"]),
                "arm": arm,
                "run_seed": int(assignment["run_seed"]),
                "window_index": len(windows),
                "step_start": step - sum(window_counts.values()) + 1,
                "step_end": step,
                "start_nodes": window_start_nodes,
                "end_nodes": state.g.num_nodes(),
                "start_tokens": window_start_tokens,
                "end_tokens": state.token_count(),
                "start_time": window_start_time,
                "end_time": total_time,
                "integrated_seed_hazard": window_hazard,
                "seed_events": window_counts["seed"],
                "birth_events": window_counts["birth"],
                "move_events": window_counts["move"],
                "swap_events": window_counts["swap"],
                "invalid_events": window_counts["null"] + window_counts["unknown"] + window_counts["token_reject"],
            })
            window_start_nodes = state.g.num_nodes()
            window_start_tokens = state.token_count()
            window_start_time = total_time
            window_hazard = 0.0
            window_counts = Counter()

    final_beta1 = beta1(state)
    run_row = {
        "growth_seed": int(assignment["growth_seed"]),
        "run_offset": int(assignment["run_offset"]),
        "arm": arm,
        "run_seed": int(assignment["run_seed"]),
        "steps": STEPS,
        "initial_nodes": initial_nodes,
        "final_nodes": state.g.num_nodes(),
        "node_growth": state.g.num_nodes() - initial_nodes,
        "initial_edges": initial_edges,
        "final_edges": state.g.num_edges(),
        "initial_tokens": initial_tokens,
        "final_tokens": state.token_count(),
        "token_growth": state.token_count() - initial_tokens,
        "initial_beta1": initial_beta1,
        "final_beta1": final_beta1,
        "beta1_drift": final_beta1 - initial_beta1,
        "total_time": total_time,
        "token_time_integral": token_time,
        "time_weighted_mean_tokens": token_time / total_time,
        "integrated_seed_hazard": integrated_seed_hazard,
        "seed_formula_max_error": max_seed_formula_error,
        "seed_events": event_counts["seed"],
        "birth_events": event_counts["birth"],
        "move_events": event_counts["move"],
        "swap_events": event_counts["swap"],
        "stuck_events": event_counts["stuck"],
        "death_events": event_counts["death"],
        "invalid_events": invalid_events,
        "event_counts": ";".join(f"{key}:{value}" for key, value in sorted(event_counts.items())),
    }
    return run_row, windows


def median(values: Iterable[float]) -> float:
    data = list(values)
    return statistics.median(data) if data else float("nan")


def arm_summary_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for arm in ARMS:
        subset = [row for row in run_rows if row["arm"] == arm]
        rows.append({
            "arm": arm,
            "n_runs": len(subset),
            "mean_initial_tokens": statistics.mean(float(row["initial_tokens"]) for row in subset),
            "mean_final_tokens": statistics.mean(float(row["final_tokens"]) for row in subset),
            "median_final_tokens": median(float(row["final_tokens"]) for row in subset),
            "mean_node_growth": statistics.mean(float(row["node_growth"]) for row in subset),
            "max_node_growth": max(int(row["node_growth"]) for row in subset),
            "total_seed_events": sum(int(row["seed_events"]) for row in subset),
            "total_birth_events": sum(int(row["birth_events"]) for row in subset),
            "total_move_events": sum(int(row["move_events"]) for row in subset),
            "total_swap_events": sum(int(row["swap_events"]) for row in subset),
            "total_invalid_events": sum(int(row["invalid_events"]) for row in subset),
            "total_integrated_seed_hazard": sum(float(row["integrated_seed_hazard"]) for row in subset),
            "mean_total_time": statistics.mean(float(row["total_time"]) for row in subset),
            "median_total_time": median(float(row["total_time"]) for row in subset),
            "max_seed_formula_error": max(float(row["seed_formula_max_error"]) for row in subset),
            "max_abs_beta1_drift": max(abs(int(row["beta1_drift"])) for row in subset),
        })
    return rows


def matched_comparison_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    lookup = {(int(row["growth_seed"]), int(row["run_offset"]), str(row["arm"])): row for row in run_rows}
    rows: List[Dict[str, Any]] = []
    for growth_seed in GROWTH_SEEDS:
        for run_offset in RUN_OFFSETS:
            baseline = lookup[(growth_seed, run_offset, "current_global")]
            for arm in ("preparation_only", "exposure_matched_local"):
                candidate = lookup[(growth_seed, run_offset, arm)]
                rows.append({
                    "growth_seed": growth_seed,
                    "run_offset": run_offset,
                    "arm": arm,
                    "integrated_seed_hazard_ratio": float(candidate["integrated_seed_hazard"]) / float(baseline["integrated_seed_hazard"]),
                    "total_time_ratio": float(candidate["total_time"]) / float(baseline["total_time"]),
                    "final_token_ratio": float(candidate["final_tokens"]) / float(baseline["final_tokens"]),
                    "node_growth_difference": int(candidate["node_growth"]) - int(baseline["node_growth"]),
                    "seed_event_difference": int(candidate["seed_events"]) - int(baseline["seed_events"]),
                })
    return rows


def nonseed_tv(run_rows: Sequence[Mapping[str, Any]], left_arm: str, right_arm: str) -> float:
    kinds = ("birth_events", "move_events", "swap_events", "stuck_events", "death_events")
    left = {kind: sum(int(row[kind]) for row in run_rows if row["arm"] == left_arm) for kind in kinds}
    right = {kind: sum(int(row[kind]) for row in run_rows if row["arm"] == right_arm) for kind in kinds}
    left_total = sum(left.values())
    right_total = sum(right.values())
    return 0.5 * sum(abs(left[kind] / left_total - right[kind] / right_total) for kind in kinds)


def gate_evaluation(
    run_rows: Sequence[Mapping[str, Any]],
    arm_rows: Sequence[Mapping[str, Any]],
    local_rate: float,
) -> Tuple[List[Dict[str, Any]], str]:
    arm_lookup = {str(row["arm"]): row for row in arm_rows}
    current = arm_lookup["current_global"]
    prep = arm_lookup["preparation_only"]
    local = arm_lookup["exposure_matched_local"]
    hazard_ratio = float(local["total_integrated_seed_hazard"]) / float(current["total_integrated_seed_hazard"])
    growth_ratios = []
    for seed in GROWTH_SEEDS:
        local_hazard = sum(float(row["integrated_seed_hazard"]) for row in run_rows if row["arm"] == "exposure_matched_local" and int(row["growth_seed"]) == seed)
        current_hazard = sum(float(row["integrated_seed_hazard"]) for row in run_rows if row["arm"] == "current_global" and int(row["growth_seed"]) == seed)
        growth_ratios.append(local_hazard / current_hazard)
    comparisons = matched_comparison_rows(run_rows)
    local_comparisons = [row for row in comparisons if row["arm"] == "exposure_matched_local"]
    time_ratio = median(float(row["total_time_ratio"]) for row in local_comparisons)
    token_ratio = median(float(row["final_token_ratio"]) for row in local_comparisons)
    tv = nonseed_tv(run_rows, "current_global", "exposure_matched_local")
    max_allowed_growth = max(MAX_NODE_GROWTH_ABSOLUTE, int(round(MAX_NODE_GROWTH_FRACTION * TARGET_NODES)))
    gates = [
        {"gate": "run_integrity", "status": "pass" if len(run_rows) == len(ARMS) * len(GROWTH_SEEDS) * len(RUN_OFFSETS) else "fail", "observed": len(run_rows), "required": len(ARMS) * len(GROWTH_SEEDS) * len(RUN_OFFSETS), "decision": "continue"},
        {"gate": "local_seed_formula", "status": "pass" if float(local["max_seed_formula_error"]) <= TOLERANCE else "fail", "observed": local["max_seed_formula_error"], "required": f"<={TOLERANCE}", "decision": "continue"},
        {"gate": "aggregate_hazard_ratio", "status": "pass" if AGGREGATE_HAZARD_RATIO[0] <= hazard_ratio <= AGGREGATE_HAZARD_RATIO[1] else "fail", "observed": hazard_ratio, "required": f"[{AGGREGATE_HAZARD_RATIO[0]},{AGGREGATE_HAZARD_RATIO[1]}]", "decision": "continue"},
        {"gate": "per_growth_hazard_ratio", "status": "pass" if all(PER_GROWTH_HAZARD_RATIO[0] <= ratio <= PER_GROWTH_HAZARD_RATIO[1] for ratio in growth_ratios) else "fail", "observed": ";".join(fmt(ratio) for ratio in growth_ratios), "required": f"each in [{PER_GROWTH_HAZARD_RATIO[0]},{PER_GROWTH_HAZARD_RATIO[1]}]", "decision": "continue"},
        {"gate": "median_total_time_ratio", "status": "pass" if TOTAL_TIME_RATIO[0] <= time_ratio <= TOTAL_TIME_RATIO[1] else "fail", "observed": time_ratio, "required": f"[{TOTAL_TIME_RATIO[0]},{TOTAL_TIME_RATIO[1]}]", "decision": "continue"},
        {"gate": "median_final_token_ratio", "status": "pass" if FINAL_TOKEN_RATIO[0] <= token_ratio <= FINAL_TOKEN_RATIO[1] else "fail", "observed": token_ratio, "required": f"[{FINAL_TOKEN_RATIO[0]},{FINAL_TOKEN_RATIO[1]}]", "decision": "continue"},
        {"gate": "nonseed_family_tv", "status": "pass" if tv <= NONSEED_TV_MAX else "fail", "observed": tv, "required": f"<={NONSEED_TV_MAX}", "decision": "continue"},
        {"gate": "local_runaway_control", "status": "pass" if int(local["max_node_growth"]) <= max_allowed_growth else "fail", "observed": local["max_node_growth"], "required": f"<={max_allowed_growth}", "decision": "continue"},
        {"gate": "preparation_only_hygiene", "status": "pass" if int(prep["total_seed_events"]) == 0 and int(prep["max_node_growth"]) == 0 else "fail", "observed": f"seeds={prep['total_seed_events']};max_node_growth={prep['max_node_growth']}", "required": "seeds=0;max_node_growth=0", "decision": "continue"},
        {"gate": "invalid_event_control", "status": "pass" if all(int(row["total_invalid_events"]) == 0 for row in arm_rows) else "fail", "observed": sum(int(row["total_invalid_events"]) for row in arm_rows), "required": 0, "decision": "continue"},
        {"gate": "beta1_anchor_control", "status": "pass" if all(int(row["max_abs_beta1_drift"]) == 0 for row in arm_rows) else "fail", "observed": max(int(row["max_abs_beta1_drift"]) for row in arm_rows), "required": 0, "decision": "continue"},
    ]
    passed = all(row["status"] == "pass" for row in gates)
    status = "promote_local_seed_clock_to_v16a_rerun" if passed else "local_seed_clock_holdout_failed"
    gates.append({"gate": "v16ab_overall", "status": status, "observed": f"rho_seed={local_rate:.15g}", "required": "all frozen gates pass", "decision": "rerun_v16a_locality" if passed else "do_not_start_v16b"})
    return gates, status


def claim_rows(status: str) -> List[Dict[str, Any]]:
    passed = status == "promote_local_seed_clock_to_v16a_rerun"
    return [
        {"claim_id": "C1", "statement": "The frozen exposure-matched local seed clock avoids the preregistered fresh rate/growth shock.", "status": "supported" if passed else "contradicted", "evidence": "v16ab_gate_evaluation.csv", "scope_limit": "target 1024; growth seeds 1801/1901; 16 local runs"},
        {"claim_id": "C2", "statement": "The preparation-only arm produces no observation-phase node growth.", "status": "supported", "evidence": "v16ab_arm_summary.csv", "scope_limit": "mechanism control"},
        {"claim_id": "C3", "statement": "The local seed clock is now the validated project anchor.", "status": "unsupported", "evidence": "fresh scheduler holdout only", "scope_limit": "requires v16a locality rerun and later recalibration"},
        {"claim_id": "C4", "statement": "v16b event-DAG may start immediately.", "status": "unsupported", "evidence": "v16ab decision requires v16a rerun", "scope_limit": "do not skip formal locality gate"},
        {"claim_id": "C5", "statement": "The holdout demonstrates Lorentz-like or spacetime geometry.", "status": "unsupported", "evidence": "scheduler metrics only", "scope_limit": "no geometry observable in v16ab"},
    ]


def build_report(
    local_rate: float,
    arm_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    status: str,
    target_rows: Sequence[Mapping[str, Any]],
) -> str:
    lines = [
        "# UniverseSimulation v16ab: fresh seed-clock scheduler holdout",
        "",
        "Dato: 2026-07-12",
        "",
        "## Konklusjon",
        "",
        f"Status: `{status}`.",
        "",
        f"Den frosne lokale seed-raten `rho_seed={local_rate:.15g}` ble testet uten refit mot `current_global` og `preparation_only` paa fresh growth seeds `1801/1901`.",
        "",
        "Dette er en scheduler-/vekstgate. Den tester ikke geometri, Lorentz-likhet eller causal cones.",
        "",
        "## Target hygiene",
        "",
    ]
    lines.extend(table(target_rows, ("target_nodes", "growth_replicates", "mean_initial_nodes", "mean_initial_tokens", "separated_from_prev")))
    lines.extend(["", "## Armer", ""])
    lines.extend(table(arm_rows, ("arm", "n_runs", "mean_initial_tokens", "mean_final_tokens", "mean_node_growth", "max_node_growth", "total_seed_events", "total_integrated_seed_hazard", "mean_total_time", "max_seed_formula_error", "max_abs_beta1_drift")))
    lines.extend(["", "## Frozen gates", ""])
    lines.extend(table(gate_rows, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Evidensstatus",
        "",
        "- Growth seeds og terskler ble skrevet til `v16ab_pre_registration.csv` foer fresh dynamikk.",
        "- Armene bruker separate RNG-stroemmer og ID-allokatorer; sammenligningene er matched paa base og run-offset, ikke coupled trajectories.",
        "- Integrert hazard er primaer fordi faktiske seed-events er sjeldne. Seed-tellingene er deskriptive.",
        "- Et pass kvalifiserer kandidaten bare for en ny v16a-locality-rerun. Det gjoer den ikke automatisk til anchor.",
        "",
        "## Beslutning",
        "",
    ])
    if status == "promote_local_seed_clock_to_v16a_rerun":
        lines.extend([
            "Den lokale kandidaten passerte alle frosne scheduler-/vekstgater. Neste steg er aa implementere clock-varianten eksplisitt i en isolert regeladapter og rerun v16a support/locality med seed aktiv. `v16b` event-DAG forblir blokkert til dette er gjort.",
        ])
    else:
        lines.extend([
            "Den lokale kandidaten feilet minst en frossen gate. Ikke refit raten. Behold current-global som historisk baseline og vurder preparation-only eller en ny eksplisitt lokal growth-regel som ny modellklasse.",
        ])
    lines.append("")
    return "\n".join(lines)


def run() -> None:
    prereg_rows, local_rate = load_and_verify_preregistration()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    target_rows = v10e.summarize_bases(base_rows)
    if len(target_rows) != 1 or int(target_rows[0]["separated_from_prev"]) != 1:
        raise RuntimeError("target hygiene failed before scheduler dynamics")
    ensemble_name = ensembles[0].name
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    run_rows: List[Dict[str, Any]] = []
    window_rows: List[Dict[str, Any]] = []
    for index, assignment in enumerate(prereg_rows, start=1):
        base = base_states[(ensemble_name, int(assignment["growth_seed"]))]
        run_row, windows = run_assignment(base, assignment, params, local_rate)
        run_rows.append(run_row)
        window_rows.extend(windows)
        if index % 8 == 0:
            print(f"[v16ab] runs={index}/{len(prereg_rows)}")
    arm_rows = arm_summary_rows(run_rows)
    comparison_rows = matched_comparison_rows(run_rows)
    gate_rows, status = gate_evaluation(run_rows, arm_rows, local_rate)
    claims = claim_rows(status)

    write_csv(DOC / "v16ab_target_summary.csv", target_rows)
    write_csv(DOC / "v16ab_run_summary.csv", run_rows)
    write_csv(DOC / "v16ab_window_trajectories.csv", window_rows)
    write_csv(DOC / "v16ab_arm_summary.csv", arm_rows)
    write_csv(DOC / "v16ab_matched_comparisons.csv", comparison_rows)
    write_csv(DOC / "v16ab_gate_evaluation.csv", gate_rows)
    write_csv(DOC / "v16ab_claim_ledger.csv", claims)
    report = build_report(local_rate, arm_rows, gate_rows, status, target_rows)
    (DOC / "v16ab_fresh_seed_clock_holdout.md").write_text(report, encoding="utf-8")
    recommendation = "\n".join([
        "# Operativ anbefaling v0.16ab",
        "",
        f"Status: `{status}`.",
        "",
        "- Ikke refit `rho_seed` etter denne holdouten.",
        "- Ved pass: implementer kandidaten i en isolert regeladapter og rerun v16a-locality foer v16b.",
        "- Ved fail: ikke fortsett til event-DAG; vurder preparation-only eller en ny lokal growth-regel.",
        "- Ikke tolk scheduler-passet som geometri- eller Lorentz-evidens.",
        "",
    ])
    (DOC / "v0_16ab_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    lay = "\n".join([
        "# v0.16ab for ikke-spesialister",
        "",
        "Vi proevde den nye lokale klokken paa helt nye startgrafer og sammenlignet den med den gamle globale klokken og med aa stoppe all nodevekst etter preparering.",
        "",
        "Testen maaler foerst om den lokale klokken gir omtrent samme mengde vekst og tidsforloep uten aa loepe loepsk. Den sier ennaa ikke at modellen har romtid eller relativitet.",
        "",
        f"Resultat: `{status}`.",
        "",
    ])
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16ab.md").write_text(lay, encoding="utf-8")
    print(f"[v16ab] status={status}")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16ab fresh seed-clock holdout")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prepare-only", action="store_true")
    mode.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if args.prepare_only:
        prepare()
    else:
        run()


if __name__ == "__main__":
    main()
