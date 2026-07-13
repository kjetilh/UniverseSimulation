#!/usr/bin/env python3
"""v16d preregistered target-scale holdout of the frozen v16c map.

The v16c quotient implementation, scale windows, transition observables, and
thresholds remain unchanged. The only research axis is target size: 1024 to
1536, with the event budget mechanically fixed at two events per initial node.

This is a finite architecture holdout. It does not test continuum limits,
Lorentz symmetry, spacetime, particles, entanglement, or universal causality.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v16a_disjoint_event_commutation_gate as v16a
import relational_universe_v16ac_local_seed_adapter_gate as v16ac
import relational_universe_v16b_intrinsic_event_dag_gate as v16b
import relational_universe_v16c_three_scale_coarse_graining_pilot as v16c


DOC = Path("Documentation")
PURPOSE_REF = "purpose://prompt.unknown"
SOURCE_SCRIPT = Path("relational_universe_v16c_three_scale_coarse_graining_pilot.py")
SOURCE_GATE = DOC / "v16c_gate_evaluation.csv"
SOURCE_PREREG = DOC / "v16c_pre_registration.csv"
SOURCE_TARGET = DOC / "v16c_target_summary.csv"
SOURCE_TRANSITIONS = DOC / "v16c_transition_ratios.csv"
FROZEN_BASELINE = DOC / "v16d_frozen_v16c_baseline.csv"
PREREG = DOC / "v16d_pre_registration.csv"

SOURCE_TARGET_NODES = 1024
TARGET_NODES = 1536
EVENTS_PER_INITIAL_NODE = 2
STEPS = TARGET_NODES * EVENTS_PER_INITIAL_NODE
GROWTH_SEEDS = (3407, 3511)
RUN_OFFSETS = (61001, 61043, 61091)
ARMS = ("current_global", "exposure_matched_local")
TOPOLOGICAL_REPLAYS = 2
SCALE_WINDOWS = (1, 4, 16)
TRANSITIONS = ((1, 4), (4, 16))
PRIMARY_METRICS = (
    "causal_depth_retention",
    "antichain_width_retention",
    "dependency_density_retention",
)
EVENT_TYPES = v16b.EVENT_TYPES
TOLERANCE = 1.0e-12

# These are intentionally identical to v16c.
MAX_LOCAL_TRANSITION_CV = 0.40
GROWTH_MEDIAN_RATIO_RANGE = (0.60, 1.67)
SCHEDULER_MEDIAN_RATIO_RANGE = (0.60, 1.67)
TARGET_MEDIAN_RATIO_RANGE = (0.60, 1.67)
MAX_NONSEED_EVENT_TV = 0.05
MIN_REORDERED_POSITION_FRACTION = 0.10
MIN_SCALE16_COARSE_NODES = 16
MIN_SCALE16_NODE_RETENTION = 0.01
MAX_SCALE16_NODE_RETENTION = 0.90

read_csv = v16c.read_csv
write_csv = v16c.write_csv
file_sha256 = v16c.file_sha256
fmt = v16c.fmt
table = v16c.table
mean = v16c.mean
median = v16c.median
coefficient_of_variation = v16c.coefficient_of_variation
ratio = v16c.ratio


def frozen_map_contract_pass() -> bool:
    return all((
        v16c.SCALE_WINDOWS == SCALE_WINDOWS,
        v16c.TRANSITIONS == TRANSITIONS,
        v16c.PRIMARY_METRICS == PRIMARY_METRICS,
        v16c.TOPOLOGICAL_REPLAYS == TOPOLOGICAL_REPLAYS,
        abs(v16c.MAX_LOCAL_TRANSITION_CV - MAX_LOCAL_TRANSITION_CV) <= TOLERANCE,
        v16c.GROWTH_MEDIAN_RATIO_RANGE == GROWTH_MEDIAN_RATIO_RANGE,
        v16c.SCHEDULER_MEDIAN_RATIO_RANGE == SCHEDULER_MEDIAN_RATIO_RANGE,
        abs(v16c.MAX_NONSEED_EVENT_TV - MAX_NONSEED_EVENT_TV) <= TOLERANCE,
        abs(v16c.MIN_REORDERED_POSITION_FRACTION - MIN_REORDERED_POSITION_FRACTION) <= TOLERANCE,
        v16c.MIN_SCALE16_COARSE_NODES == MIN_SCALE16_COARSE_NODES,
        abs(v16c.MIN_SCALE16_NODE_RETENTION - MIN_SCALE16_NODE_RETENTION) <= TOLERANCE,
        abs(v16c.MAX_SCALE16_NODE_RETENTION - MAX_SCALE16_NODE_RETENTION) <= TOLERANCE,
    ))


def source_without_baseline_rows() -> Tuple[List[Dict[str, Any]], bool]:
    gate_rows = read_csv(SOURCE_GATE)
    overall = [row for row in gate_rows if row["gate"] == "v16c_overall"]
    subgates = [row for row in gate_rows if row["gate"] != "v16c_overall"]
    prereg_verified = True
    prereg_error = "verified"
    try:
        v16c.load_and_verify_preregistration()
    except (AssertionError, KeyError, RuntimeError, ValueError) as error:
        prereg_verified = False
        prereg_error = f"{type(error).__name__}:{error}"
    rows = [
        {
            "check": "v16c_overall",
            "observed": overall[0]["status"] if len(overall) == 1 else f"rows={len(overall)}",
            "required": "pass_to_v16d_scale_holdout",
            "status": "pass" if len(overall) == 1 and overall[0]["status"] == "pass_to_v16d_scale_holdout" else "fail",
        },
        {
            "check": "v16c_all_subgates",
            "observed": sum(row["status"] != "pass" for row in subgates),
            "required": 0,
            "status": "pass" if subgates and all(row["status"] == "pass" for row in subgates) else "fail",
        },
        {
            "check": "v16c_preregistration_reverified",
            "observed": prereg_error,
            "required": "verified",
            "status": "pass" if prereg_verified else "fail",
        },
        {
            "check": "frozen_map_and_threshold_contract",
            "observed": int(frozen_map_contract_pass()),
            "required": 1,
            "status": "pass" if frozen_map_contract_pass() else "fail",
        },
        {
            "check": "v16c_source_script_sha256",
            "observed": file_sha256(SOURCE_SCRIPT),
            "required": "frozen into v16d preregistration",
            "status": "pass",
        },
    ]
    return rows, all(row["status"] == "pass" for row in rows)


def expected_baseline_rows() -> List[Dict[str, Any]]:
    source_rows = read_csv(SOURCE_TRANSITIONS)
    local = [row for row in source_rows if row["arm"] == "exposure_matched_local"]
    rows: List[Dict[str, Any]] = []
    for source_window, target_window in TRANSITIONS:
        transition = f"{source_window}_to_{target_window}"
        for metric in PRIMARY_METRICS:
            values = [
                float(row["retention_ratio"])
                for row in local
                if row["transition"] == transition and row["metric"] == metric
            ]
            rows.append({
                "artifact_role": "frozen_v16c_local_baseline_not_v16d_evidence",
                "source_target_nodes": SOURCE_TARGET_NODES,
                "transition": transition,
                "metric": metric,
                "n_source_runs": len(values),
                "source_local_median": median(values),
                "source_transition_sha256": file_sha256(SOURCE_TRANSITIONS),
            })
    return rows


def freeze_baseline() -> None:
    source_rows, source_pass = source_without_baseline_rows()
    if not source_pass:
        raise RuntimeError(f"v16c source contract failed: {source_rows}")
    rows = expected_baseline_rows()
    if len(rows) != len(TRANSITIONS) * len(PRIMARY_METRICS):
        raise RuntimeError("incomplete v16c baseline")
    write_csv(FROZEN_BASELINE, rows)
    print(
        f"[v16d] froze baseline rows={len(rows)} source_sha256={rows[0]['source_transition_sha256']} "
        f"baseline_sha256={file_sha256(FROZEN_BASELINE)}"
    )


def baseline_verified() -> bool:
    if not FROZEN_BASELINE.exists():
        return False
    observed = read_csv(FROZEN_BASELINE)
    expected = expected_baseline_rows()
    if len(observed) != len(expected):
        return False
    key_fields = ("transition", "metric")
    observed_lookup = {tuple(row[field] for field in key_fields): row for row in observed}
    for row in expected:
        key = tuple(str(row[field]) for field in key_fields)
        candidate = observed_lookup.get(key)
        if candidate is None:
            return False
        if candidate["artifact_role"] != row["artifact_role"]:
            return False
        if int(candidate["source_target_nodes"]) != SOURCE_TARGET_NODES:
            return False
        if int(candidate["n_source_runs"]) != int(row["n_source_runs"]):
            return False
        if abs(float(candidate["source_local_median"]) - float(row["source_local_median"])) > TOLERANCE:
            return False
        if candidate["source_transition_sha256"] != row["source_transition_sha256"]:
            return False
    return True


def source_contract_rows() -> Tuple[List[Dict[str, Any]], bool, float]:
    rows, source_pass = source_without_baseline_rows()
    rows.append({
        "check": "frozen_v16c_baseline",
        "observed": file_sha256(FROZEN_BASELINE) if FROZEN_BASELINE.exists() else "missing",
        "required": "six exact local transition medians",
        "status": "pass" if baseline_verified() else "fail",
    })
    return rows, source_pass and baseline_verified(), v16ac.FROZEN_LOCAL_RATE


def baseline_values() -> Dict[Tuple[str, str], float]:
    if not baseline_verified():
        raise ValueError("v16d frozen baseline failed verification")
    return {
        (row["transition"], row["metric"]): float(row["source_local_median"])
        for row in read_csv(FROZEN_BASELINE)
    }


def frozen_spec(local_rate: float) -> Dict[str, Any]:
    baseline = baseline_values()
    return {
        "purpose_ref": PURPOSE_REF,
        "source_script_sha256": file_sha256(SOURCE_SCRIPT),
        "source_gate_sha256": file_sha256(SOURCE_GATE),
        "source_prereg_sha256": file_sha256(SOURCE_PREREG),
        "source_target_sha256": file_sha256(SOURCE_TARGET),
        "frozen_baseline_sha256": file_sha256(FROZEN_BASELINE),
        "source_target_nodes": SOURCE_TARGET_NODES,
        "target_nodes": TARGET_NODES,
        "event_budget_policy": "two_events_per_initial_target_node",
        "events_per_initial_node": EVENTS_PER_INITIAL_NODE,
        "steps": STEPS,
        "growth_seeds": list(GROWTH_SEEDS),
        "run_offsets": list(RUN_OFFSETS),
        "arms": list(ARMS),
        "topological_replays": TOPOLOGICAL_REPLAYS,
        "local_rate": local_rate,
        "coarse_map": {
            "scale_windows": list(SCALE_WINDOWS),
            "depth_bin": "floor(fine_causal_depth / scale_window)",
            "contraction": "weak_components_of_direct_fine_edges_inside_each_depth_bin",
            "quotient_edge": "at_least_one_direct_fine_edge_between_components",
            "implementation": "imported_unchanged_from_v16c",
        },
        "primary_metrics": list(PRIMARY_METRICS),
        "transitions": [list(pair) for pair in TRANSITIONS],
        "frozen_source_local_medians": {
            f"{transition}:{metric}": value
            for (transition, metric), value in sorted(baseline.items())
        },
        "thresholds": {
            "max_local_transition_cv": MAX_LOCAL_TRANSITION_CV,
            "growth_median_ratio_range": list(GROWTH_MEDIAN_RATIO_RANGE),
            "scheduler_median_ratio_range": list(SCHEDULER_MEDIAN_RATIO_RANGE),
            "target_median_ratio_range": list(TARGET_MEDIAN_RATIO_RANGE),
            "max_nonseed_event_tv": MAX_NONSEED_EVENT_TV,
            "min_reordered_position_fraction": MIN_REORDERED_POSITION_FRACTION,
            "min_scale16_coarse_nodes": MIN_SCALE16_COARSE_NODES,
            "min_scale16_node_retention": MIN_SCALE16_NODE_RETENTION,
            "max_scale16_node_retention": MAX_SCALE16_NODE_RETENTION,
        },
    }


def spec_digest(spec: Mapping[str, Any]) -> str:
    payload = json.dumps(spec, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def run_seed(growth_seed: int, run_offset: int, arm: str) -> int:
    arm_code = {"current_global": 0, "exposure_matched_local": 1}[arm]
    return TARGET_NODES * 1_000_000 + growth_seed * 10_000 + run_offset + arm_code * 100_000_000 + 16_004


def preregistration_rows(local_rate: float) -> List[Dict[str, Any]]:
    digest = spec_digest(frozen_spec(local_rate))
    rows: List[Dict[str, Any]] = []
    for growth_seed in GROWTH_SEEDS:
        for run_offset in RUN_OFFSETS:
            for arm in ARMS:
                rows.append({
                    "purpose_ref": PURPOSE_REF,
                    "spec_digest": digest,
                    "source_script_sha256": file_sha256(SOURCE_SCRIPT),
                    "source_gate_sha256": file_sha256(SOURCE_GATE),
                    "frozen_baseline_sha256": file_sha256(FROZEN_BASELINE),
                    "source_target_nodes": SOURCE_TARGET_NODES,
                    "target_nodes": TARGET_NODES,
                    "events_per_initial_node": EVENTS_PER_INITIAL_NODE,
                    "growth_seed": growth_seed,
                    "run_offset": run_offset,
                    "arm": arm,
                    "run_seed": run_seed(growth_seed, run_offset, arm),
                    "steps": STEPS,
                    "topological_replays": TOPOLOGICAL_REPLAYS,
                    "scale_windows": ";".join(map(str, SCALE_WINDOWS)),
                    "primary_metrics": ";".join(PRIMARY_METRICS),
                    "frozen_local_rate": local_rate,
                    "max_local_transition_cv": MAX_LOCAL_TRANSITION_CV,
                    "target_ratio_low": TARGET_MEDIAN_RATIO_RANGE[0],
                    "target_ratio_high": TARGET_MEDIAN_RATIO_RANGE[1],
                    "prepared_before_fresh_dynamics": 1,
                })
    return rows


def prepare() -> None:
    source_rows, source_pass, local_rate = source_contract_rows()
    if not source_pass:
        raise RuntimeError(f"v16c source contract failed: {source_rows}")
    rows = preregistration_rows(local_rate)
    write_csv(PREREG, rows)
    print(f"[v16d] prepared rows={len(rows)} digest={rows[0]['spec_digest']}")


def load_and_verify_preregistration() -> Tuple[List[Dict[str, str]], float, List[Dict[str, Any]]]:
    if not PREREG.exists():
        raise ValueError("missing v16d preregistration; run --prepare-only first")
    source_rows, source_pass, local_rate = source_contract_rows()
    if not source_pass:
        raise RuntimeError("v16c source contract no longer passes")
    observed = read_csv(PREREG)
    expected = preregistration_rows(local_rate)
    expected_digest = spec_digest(frozen_spec(local_rate))
    if len(observed) != len(expected):
        raise ValueError("v16d preregistration row count changed")
    if {row["spec_digest"] for row in observed} != {expected_digest}:
        raise ValueError("v16d preregistration digest changed")
    fields = ("growth_seed", "run_offset", "arm", "run_seed")
    observed_keys = {tuple(row[field] for field in fields) for row in observed}
    expected_keys = {tuple(str(row[field]) for field in fields) for row in expected}
    if observed_keys != expected_keys:
        raise ValueError("v16d preregistration assignments changed")
    return observed, local_rate, source_rows


def run_assignment(
    base: v7.State,
    assignment: Mapping[str, str],
    params: v7.Params,
    adapter: v16ac.LocalSeedClockAdapter,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any], List[Dict[str, Any]], Dict[str, Any], v16b.DependencyDAG]:
    initial_state = base.clone()
    state = base.clone()
    rng = random.Random(int(assignment["run_seed"]))
    next_node_id, next_token_id = v08b.next_ids_from_state(state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)
    dag = v16b.DependencyDAG()
    trace: List[v16b.TraceEvent] = []
    event_counts: Counter[str] = Counter()
    invalid_events = 0
    total_time = 0.0
    prefix = {
        "growth_seed": int(assignment["growth_seed"]),
        "run_offset": int(assignment["run_offset"]),
        "arm": assignment["arm"],
        "run_seed": int(assignment["run_seed"]),
    }
    for step in range(1, STEPS + 1):
        rates = v7.family_rates(state, params) if assignment["arm"] == "current_global" else adapter.family_rates(state, params)
        family, total_rate = v16b.choose_family(rates, rng)
        if total_rate <= 0.0:
            raise RuntimeError("non-positive total rate")
        dt = rng.expovariate(total_rate)
        total_time += dt
        state.t += dt
        kernel = adapter.family_kernel(state, family, params)
        if not kernel:
            raise RuntimeError(f"empty kernel for positive family {family}")
        descriptor = tuple(v7.sample_from_dist(kernel, rng))
        concrete = v16b.materialize_event(family, descriptor, manager)
        reads, writes = v16a.action_access(state, concrete)
        dag.add(reads, writes)
        context = adapter.apply_descriptor(state, family, descriptor, params, manager)
        event_type = str(context.get("event", "unknown"))
        invalid_events += int(event_type != concrete.kind)
        if concrete.new_node_id is not None:
            invalid_events += int(int(context.get("new_node", -1)) != concrete.new_node_id)
        if concrete.new_token_id is not None:
            invalid_events += int(int(context.get("new_token_id", -1)) != concrete.new_token_id)
        event_counts[event_type] += 1
        trace.append(v16b.TraceEvent(step - 1, family, event_type, concrete, tuple(sorted(reads)), tuple(sorted(writes)), dt, total_time))

    final_state = state.clone()
    analysis = dag.analyze()
    event_rows: List[Dict[str, Any]] = []
    for item in trace:
        predecessors = dag.predecessors[item.event_id]
        event_rows.append({
            **prefix,
            "event_id": item.event_id,
            "step": item.event_id + 1,
            "family": item.family,
            "event_type": item.event_type,
            "descriptor": repr(item.event.descriptor),
            "new_node_id": "" if item.event.new_node_id is None else item.event.new_node_id,
            "new_token_id": "" if item.event.new_token_id is None else item.event.new_token_id,
            "dt": item.dt,
            "time": item.time,
            "read_resources": ";".join(item.reads),
            "write_resources": ";".join(item.writes),
            "direct_predecessors": ";".join(str(parent) for parent in sorted(predecessors)),
            "indegree": len(predecessors),
            "causal_depth": analysis["depths"][item.event_id],
        })
    dependency_rows = v16b.edge_rows(prefix, dag)
    replay_rows = v16c.replay_audit(initial_state, final_state, trace, dag, params, prefix, int(assignment["run_seed"]))
    relabel_row = v16b.relabel_replay(initial_state, final_state, trace, dag, params, prefix)
    relabel_row["coarse_map_transport_pass"] = int(
        int(relabel_row["edge_set_equal"]) == 1 and int(relabel_row["depth_sequence_equal"]) == 1
    )
    run_row: Dict[str, Any] = {
        **prefix,
        "steps": STEPS,
        "initial_nodes": initial_state.g.num_nodes(),
        "final_nodes": final_state.g.num_nodes(),
        "initial_tokens": initial_state.token_count(),
        "final_tokens": final_state.token_count(),
        "total_time": total_time,
        "invalid_events": invalid_events,
        "n_events": analysis["n_events"],
        "fine_edges": analysis["edge_count"],
        "fine_causal_depth": analysis["causal_depth"],
        "fine_max_layer_width": analysis["max_layer_width"],
        "fine_comparable_pair_fraction": analysis["comparable_pair_fraction"],
        "fine_acyclic": analysis["acyclic"],
        "fine_edge_witness_errors": analysis["edge_witness_errors"],
        "topological_replay_failures": sum(
            not (int(row["topological_order_valid"]) and int(row["context_failures"]) == 0 and int(row["final_structure_equal"]))
            for row in replay_rows
        ),
        "min_reordered_position_fraction": min(float(row["changed_position_fraction"]) for row in replay_rows),
        "relabel_pass": relabel_row["relabel_pass"],
        "coarse_map_transport_pass": relabel_row["coarse_map_transport_pass"],
    }
    for event_type in EVENT_TYPES:
        run_row[f"{event_type}_events"] = event_counts[event_type]
    return event_rows, dependency_rows, run_row, replay_rows, relabel_row, dag


def local_stability_rows(transition_data: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    local = [row for row in transition_data if row["arm"] == "exposure_matched_local"]
    for source, target in TRANSITIONS:
        transition = f"{source}_to_{target}"
        for metric in PRIMARY_METRICS:
            values = [float(row["retention_ratio"]) for row in local if row["transition"] == transition and row["metric"] == metric]
            cv = coefficient_of_variation(values)
            rows.append({
                "transition": transition,
                "metric": metric,
                "n_runs": len(values),
                "mean_retention": mean(values),
                "median_retention": median(values),
                "retention_cv": cv,
                "max_cv": MAX_LOCAL_TRANSITION_CV,
                "local_stability_pass": int(cv <= MAX_LOCAL_TRANSITION_CV),
            })
    return rows


def growth_transfer_rows(transition_data: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    local = [row for row in transition_data if row["arm"] == "exposure_matched_local"]
    for source, target in TRANSITIONS:
        transition = f"{source}_to_{target}"
        for metric in PRIMARY_METRICS:
            medians = {
                seed: median(
                    float(row["retention_ratio"])
                    for row in local
                    if row["transition"] == transition and row["metric"] == metric and int(row["growth_seed"]) == seed
                )
                for seed in GROWTH_SEEDS
            }
            value_ratio = ratio(medians[GROWTH_SEEDS[1]], medians[GROWTH_SEEDS[0]])
            rows.append({
                "transition": transition,
                "metric": metric,
                f"growth_{GROWTH_SEEDS[0]}_median": medians[GROWTH_SEEDS[0]],
                f"growth_{GROWTH_SEEDS[1]}_median": medians[GROWTH_SEEDS[1]],
                "second_over_first_ratio": value_ratio,
                "ratio_low": GROWTH_MEDIAN_RATIO_RANGE[0],
                "ratio_high": GROWTH_MEDIAN_RATIO_RANGE[1],
                "growth_transfer_pass": int(GROWTH_MEDIAN_RATIO_RANGE[0] <= value_ratio <= GROWTH_MEDIAN_RATIO_RANGE[1]),
            })
    return rows


def nonseed_event_tv(run_rows: Sequence[Mapping[str, Any]]) -> float:
    event_types = ("birth", "move", "swap", "stuck", "death", "delete", "triad")
    distributions: Dict[str, Dict[str, float]] = {}
    for arm in ARMS:
        counts = {event_type: sum(int(row[f"{event_type}_events"]) for row in run_rows if row["arm"] == arm) for event_type in event_types}
        total = sum(counts.values())
        distributions[arm] = {event_type: counts[event_type] / total if total else 0.0 for event_type in event_types}
    return 0.5 * sum(abs(distributions[ARMS[0]][event_type] - distributions[ARMS[1]][event_type]) for event_type in event_types)


def scheduler_transfer_rows(
    transition_data: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    tv = nonseed_event_tv(run_rows)
    for source, target in TRANSITIONS:
        transition = f"{source}_to_{target}"
        for metric in PRIMARY_METRICS:
            medians = {
                arm: median(
                    float(row["retention_ratio"])
                    for row in transition_data
                    if row["transition"] == transition and row["metric"] == metric and row["arm"] == arm
                )
                for arm in ARMS
            }
            value_ratio = ratio(medians["exposure_matched_local"], medians["current_global"])
            rows.append({
                "transition": transition,
                "metric": metric,
                "current_global_median": medians["current_global"],
                "local_median": medians["exposure_matched_local"],
                "local_over_global_ratio": value_ratio,
                "ratio_low": SCHEDULER_MEDIAN_RATIO_RANGE[0],
                "ratio_high": SCHEDULER_MEDIAN_RATIO_RANGE[1],
                "scheduler_transfer_pass": int(SCHEDULER_MEDIAN_RATIO_RANGE[0] <= value_ratio <= SCHEDULER_MEDIAN_RATIO_RANGE[1]),
                "nonseed_event_tv": tv,
                "nonseed_tv_pass": int(tv <= MAX_NONSEED_EVENT_TV),
            })
    return rows


def target_transfer_rows(transition_data: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    baseline = baseline_values()
    local = [row for row in transition_data if row["arm"] == "exposure_matched_local"]
    for source, target in TRANSITIONS:
        transition = f"{source}_to_{target}"
        for metric in PRIMARY_METRICS:
            holdout_median = median(
                float(row["retention_ratio"])
                for row in local
                if row["transition"] == transition and row["metric"] == metric
            )
            source_median = baseline[(transition, metric)]
            value_ratio = ratio(holdout_median, source_median)
            rows.append({
                "transition": transition,
                "metric": metric,
                "source_target_nodes": SOURCE_TARGET_NODES,
                "holdout_target_nodes": TARGET_NODES,
                "source_local_median": source_median,
                "holdout_local_median": holdout_median,
                "holdout_over_source_ratio": value_ratio,
                "ratio_low": TARGET_MEDIAN_RATIO_RANGE[0],
                "ratio_high": TARGET_MEDIAN_RATIO_RANGE[1],
                "target_transfer_pass": int(TARGET_MEDIAN_RATIO_RANGE[0] <= value_ratio <= TARGET_MEDIAN_RATIO_RANGE[1]),
            })
    return rows


def holdout_target_rows(base_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows = v10e.summarize_bases(base_rows)
    if len(rows) != 1:
        raise RuntimeError("v16d expected one target summary row")
    source = read_csv(SOURCE_TARGET)
    if len(source) != 1 or int(source[0]["target_nodes"]) != SOURCE_TARGET_NODES:
        raise RuntimeError("v16c target source is invalid")
    row = dict(rows[0])
    row["source_target_nodes"] = SOURCE_TARGET_NODES
    row["source_q90_initial_nodes"] = float(source[0]["q90_initial_nodes"])
    row["separated_from_source"] = int(float(row["q10_initial_nodes"]) > float(source[0]["q90_initial_nodes"]))
    row["event_budget"] = STEPS
    row["events_per_initial_target_node"] = EVENTS_PER_INITIAL_NODE
    return [row]


def gate_evaluation(
    source_pass: bool,
    target_rows: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    replay_rows: Sequence[Mapping[str, Any]],
    relabel_rows: Sequence[Mapping[str, Any]],
    scale_rows: Sequence[Mapping[str, Any]],
    map_rows: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
    target_transfer: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], str]:
    expected_runs = len(GROWTH_SEEDS) * len(RUN_OFFSETS) * len(ARMS)
    target_pass = (
        len(target_rows) == 1
        and int(target_rows[0]["separated_from_source"]) == 1
        and int(target_rows[0]["mean_initial_nodes"]) == TARGET_NODES
    )
    run_integrity = len(run_rows) == expected_runs and all(int(row["n_events"]) == STEPS and int(row["invalid_events"]) == 0 for row in run_rows)
    fine_dag_integrity = all(int(row["fine_acyclic"]) and int(row["fine_edge_witness_errors"]) == 0 and int(row["fine_edges"]) > 0 for row in run_rows)
    replay_pass = (
        len(replay_rows) == expected_runs * TOPOLOGICAL_REPLAYS
        and all(int(row["topological_order_valid"]) and int(row["context_failures"]) == 0 and int(row["final_structure_equal"]) for row in replay_rows)
        and all(float(row["changed_position_fraction"]) >= MIN_REORDERED_POSITION_FRACTION for row in replay_rows)
    )
    relabel_pass = len(relabel_rows) == expected_runs and all(int(row["relabel_pass"]) and int(row["coarse_map_transport_pass"]) for row in relabel_rows)
    map_integrity = len(map_rows) == expected_runs * len(SCALE_WINDOWS) and all(int(row["map_integrity_pass"]) for row in map_rows)
    identity_pass = all(
        int(row["identity_membership_pass"]) and int(row["identity_edge_pass"])
        for row in map_rows if int(row["scale_window"]) == 1
    )
    by_run: Dict[Tuple[int, int, str], Dict[int, Mapping[str, Any]]] = defaultdict(dict)
    for row in scale_rows:
        by_run[(int(row["growth_seed"]), int(row["run_offset"]), str(row["arm"]))][int(row["scale_window"])] = row
    strict_compression = len(by_run) == expected_runs and all(
        int(scales[1]["coarse_nodes"]) > int(scales[4]["coarse_nodes"]) > int(scales[16]["coarse_nodes"])
        for scales in by_run.values()
    )
    scale16_rows = [row for row in scale_rows if int(row["scale_window"]) == 16]
    nondegenerate = len(scale16_rows) == expected_runs and all(
        int(row["coarse_nodes"]) >= MIN_SCALE16_COARSE_NODES
        and MIN_SCALE16_NODE_RETENTION <= float(row["node_retention"]) <= MAX_SCALE16_NODE_RETENTION
        for row in scale16_rows
    )
    local_stability = all(int(row["local_stability_pass"]) for row in local_rows)
    growth_transfer = all(int(row["growth_transfer_pass"]) for row in growth_rows)
    scheduler_transfer = all(int(row["scheduler_transfer_pass"]) and int(row["nonseed_tv_pass"]) for row in scheduler_rows)
    target_passed = all(int(row["target_transfer_pass"]) for row in target_transfer)
    exact_map_pass = all((source_pass, target_pass, run_integrity, fine_dag_integrity, replay_pass, relabel_pass, map_integrity, identity_pass, strict_compression, nondegenerate))
    all_pass = exact_map_pass and local_stability and growth_transfer and scheduler_transfer and target_passed
    if all_pass:
        overall = "pass_to_v16e_independent_coarse_map_gate"
    elif exact_map_pass:
        overall = "finite_coarse_map_not_target_transferable"
    else:
        overall = "v16d_instrumentation_failed"
    gates = [
        {"gate": "v16c_source_contract", "status": "pass" if source_pass else "fail", "observed": int(source_pass), "required": 1, "decision": "continue"},
        {"gate": "target_1536_hygiene", "status": "pass" if target_pass else "fail", "observed": f"mean={target_rows[0]['mean_initial_nodes'] if target_rows else 'missing'};separated={target_rows[0]['separated_from_source'] if target_rows else 'missing'}", "required": f"mean={TARGET_NODES};separated=1", "decision": "continue" if target_pass else "stop"},
        {"gate": "fresh_run_integrity", "status": "pass" if run_integrity else "fail", "observed": f"runs={len(run_rows)};invalid={sum(int(row['invalid_events']) for row in run_rows)}", "required": f"runs={expected_runs};invalid=0", "decision": "continue"},
        {"gate": "fine_dag_integrity", "status": "pass" if fine_dag_integrity else "fail", "observed": f"acyclic={sum(int(row['fine_acyclic']) for row in run_rows)};witness_errors={sum(int(row['fine_edge_witness_errors']) for row in run_rows)}", "required": f"acyclic={expected_runs};witness_errors=0", "decision": "continue"},
        {"gate": "fresh_topological_replay", "status": "pass" if replay_pass else "fail", "observed": f"replays={len(replay_rows)};min_reorder={min(float(row['changed_position_fraction']) for row in replay_rows):.6f};failures={sum(not int(row['final_structure_equal']) or int(row['context_failures']) for row in replay_rows)}", "required": f"replays={expected_runs * TOPOLOGICAL_REPLAYS};failures=0", "decision": "continue" if replay_pass else "repair_support"},
        {"gate": "relabel_and_map_transport", "status": "pass" if relabel_pass else "fail", "observed": sum(int(row["relabel_pass"]) and int(row["coarse_map_transport_pass"]) for row in relabel_rows), "required": expected_runs, "decision": "continue" if relabel_pass else "repair_map"},
        {"gate": "quotient_map_integrity", "status": "pass" if map_integrity else "fail", "observed": f"passes={sum(int(row['map_integrity_pass']) for row in map_rows)}/{len(map_rows)}", "required": expected_runs * len(SCALE_WINDOWS), "decision": "continue" if map_integrity else "repair_map"},
        {"gate": "scale1_identity", "status": "pass" if identity_pass else "fail", "observed": int(identity_pass), "required": 1, "decision": "continue" if identity_pass else "repair_map"},
        {"gate": "strict_three_scale_compression", "status": "pass" if strict_compression else "fail", "observed": int(strict_compression), "required": 1, "decision": "continue" if strict_compression else "reject_target_transfer"},
        {"gate": "scale16_nondegenerate", "status": "pass" if nondegenerate else "fail", "observed": f"nodes={min(int(row['coarse_nodes']) for row in scale16_rows)}-{max(int(row['coarse_nodes']) for row in scale16_rows)};retention={min(float(row['node_retention']) for row in scale16_rows):.6f}-{max(float(row['node_retention']) for row in scale16_rows):.6f}", "required": f"nodes>={MIN_SCALE16_COARSE_NODES};retention in [{MIN_SCALE16_NODE_RETENTION},{MAX_SCALE16_NODE_RETENTION}]", "decision": "continue" if nondegenerate else "reject_target_transfer"},
        {"gate": "local_transition_cv", "status": "pass" if local_stability else "fail", "observed": ";".join(f"{row['transition']}:{row['metric']}={float(row['retention_cv']):.6f}" for row in local_rows), "required": f"each<={MAX_LOCAL_TRANSITION_CV}", "decision": "continue" if local_stability else "hold"},
        {"gate": "growth_seed_transfer", "status": "pass" if growth_transfer else "fail", "observed": ";".join(f"{row['transition']}:{row['metric']}={float(row['second_over_first_ratio']):.6f}" for row in growth_rows), "required": f"each in [{GROWTH_MEDIAN_RATIO_RANGE[0]},{GROWTH_MEDIAN_RATIO_RANGE[1]}]", "decision": "continue" if growth_transfer else "hold"},
        {"gate": "target_1024_to_1536_transfer", "status": "pass" if target_passed else "fail", "observed": ";".join(f"{row['transition']}:{row['metric']}={float(row['holdout_over_source_ratio']):.6f}" for row in target_transfer), "required": f"each in [{TARGET_MEDIAN_RATIO_RANGE[0]},{TARGET_MEDIAN_RATIO_RANGE[1]}]", "decision": "continue" if target_passed else "retire_scale_family"},
        {"gate": "scheduler_diagnostic_transfer", "status": "pass" if scheduler_transfer else "fail", "observed": ";".join(f"{row['transition']}:{row['metric']}={float(row['local_over_global_ratio']):.6f}" for row in scheduler_rows) + f";tv={float(scheduler_rows[0]['nonseed_event_tv']):.6f}", "required": f"ratios in [{SCHEDULER_MEDIAN_RATIO_RANGE[0]},{SCHEDULER_MEDIAN_RATIO_RANGE[1]}];tv<={MAX_NONSEED_EVENT_TV}", "decision": "continue" if scheduler_transfer else "hold"},
        {"gate": "v16d_overall", "status": overall, "observed": int(all_pass), "required": 1, "decision": "design_independent_map_gate" if all_pass else ("retire_target_transfer_claim" if exact_map_pass else "repair_instrumentation")},
    ]
    return gates, overall


def claim_rows(status: str) -> List[Dict[str, Any]]:
    exact = status in {"pass_to_v16e_independent_coarse_map_gate", "finite_coarse_map_not_target_transferable"}
    target = status == "pass_to_v16e_independent_coarse_map_gate"
    return [
        {"claim_id": "C1", "statement": "The unchanged v16c map produces witnessed acyclic quotient DAGs on fresh target-1536 histories.", "status": "supported" if exact else "not_supported", "evidence": "v16d_map_audit.csv;v16d_coarse_dependency_edges.csv", "scope_limit": "finite target 1536 under the declared event support schema"},
        {"claim_id": "C2", "statement": "Local transition-ratio medians transfer from target 1024 to 1536 within the frozen bounds.", "status": "supported" if target else "not_supported", "evidence": "v16d_target_transfer.csv;v16d_gate_evaluation.csv", "scope_limit": "one target step, equal two-events-per-target-node exposure, broad pilot bounds"},
        {"claim_id": "C3", "statement": "The target-1536 quotients remain stable across fresh growth seeds and the scheduler diagnostic.", "status": "supported" if target else "not_supported", "evidence": "v16d_growth_transfer.csv;v16d_scheduler_transfer.csv", "scope_limit": "two growth seeds and six runs per arm"},
        {"claim_id": "C4", "statement": "The imported quotient map remains invariant under concrete node relabeling.", "status": "supported" if exact else "not_supported", "evidence": "v16d_relabel_replay_audit.csv", "scope_limit": "preserved event edge sets and depth sequences"},
        {"claim_id": "C5", "statement": "Target transfer establishes a continuum limit, Lorentz symmetry, or emergent spacetime.", "status": "unsupported", "evidence": "none", "scope_limit": "not tested by v16d"},
        {"claim_id": "C6", "statement": "The depth-window map is independent physical evidence rather than a chosen coarse-graining convention.", "status": "unsupported", "evidence": "none", "scope_limit": "v16d deliberately reuses the same construction; an independent map is still required"},
    ]


def build_report(
    source_rows: Sequence[Mapping[str, Any]],
    target_rows: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    scale_rows: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
    target_transfer: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# UniverseSimulation v16d: preregistered target-scale holdout",
        "",
        "## Research question",
        "",
        "Does the exact frozen v16c quotient map retain its transition-ratio family when target size increases from 1024 to 1536 at the same two-events-per-initial-target-node exposure?",
        "",
        "## Evidential separation",
        "",
        "- Frozen architecture: the v16c script hash, map, scales, metrics, and thresholds were locked before fresh target-1536 dynamics.",
        "- Frozen reference: six target-1024 local medians were copied from v16c into a separate baseline artifact before preregistration.",
        "- Actual dynamics: twelve new target-1536 histories were generated after preregistration.",
        "- Primary holdout: target-1536 local medians divided by the frozen target-1024 local medians.",
        "- Diagnostic control: current-global remains a scheduler contrast, not the primary architecture candidate.",
        "- Negative boundary: continuum, Lorentz, spacetime, particle, entanglement, and universal-causality claims were not tested.",
        "",
        "## Source contract",
        "",
    ]
    lines.extend(table(source_rows, ("check", "observed", "required", "status")))
    lines.extend([
        "",
        "## Frozen holdout design",
        "",
        f"Target `{TARGET_NODES}`, source target `{SOURCE_TARGET_NODES}`, fresh growth seeds `{GROWTH_SEEDS[0]}/{GROWTH_SEEDS[1]}`, offsets `{RUN_OFFSETS[0]}/{RUN_OFFSETS[1]}/{RUN_OFFSETS[2]}`, `{STEPS}` events (`{EVENTS_PER_INITIAL_NODE}` per target node), and the unchanged scheduler arms.",
        "",
        "The quotient map is imported from the hash-locked v16c script. No target-1536 calibration was performed before preregistration.",
        "",
        "Target hygiene:",
        "",
    ])
    lines.extend(table(target_rows, ("target_nodes", "growth_replicates", "mean_initial_nodes", "q10_initial_nodes", "source_q90_initial_nodes", "separated_from_source", "event_budget")))
    lines.extend(["", "## Fine histories", ""])
    lines.extend(table(run_rows, ("growth_seed", "run_offset", "arm", "n_events", "fine_edges", "fine_causal_depth", "fine_max_layer_width", "topological_replay_failures", "relabel_pass", "coarse_map_transport_pass")))
    lines.extend(["", "## Three-scale quotients", ""])
    lines.extend(table(scale_rows, ("growth_seed", "run_offset", "arm", "scale_window", "coarse_nodes", "coarse_edges", "node_retention", "causal_depth", "max_layer_width", "comparable_pair_fraction", "dependency_density")))
    lines.extend(["", "## Local stability", ""])
    lines.extend(table(local_rows, ("transition", "metric", "median_retention", "retention_cv", "local_stability_pass")))
    lines.extend(["", "## Growth-seed transfer", ""])
    lines.extend(table(growth_rows, ("transition", "metric", f"growth_{GROWTH_SEEDS[0]}_median", f"growth_{GROWTH_SEEDS[1]}_median", "second_over_first_ratio", "growth_transfer_pass")))
    lines.extend(["", "## Primary target transfer", ""])
    lines.extend(table(target_transfer, ("transition", "metric", "source_local_median", "holdout_local_median", "holdout_over_source_ratio", "target_transfer_pass")))
    lines.extend(["", "## Scheduler diagnostic", ""])
    lines.extend(table(scheduler_rows, ("transition", "metric", "current_global_median", "local_median", "local_over_global_ratio", "scheduler_transfer_pass", "nonseed_event_tv", "nonseed_tv_pass")))
    lines.extend(["", "## Gate evaluation", ""])
    lines.extend(table(gate_rows, ("gate", "status", "observed", "required", "decision")))
    lines.extend(["", f"Overall status: `{overall}`.", "", "## Interpretation", ""])
    if overall == "pass_to_v16e_independent_coarse_map_gate":
        lines.append("The unchanged finite quotient construction survives a fresh target increase from 1024 to 1536 under equal event density, including exact structural controls and broad transition-ratio transfer bounds. This justifies testing an independent coarse map; it does not justify another same-map scale extension by default.")
    elif overall == "finite_coarse_map_not_target_transferable":
        lines.append("The map remains technically valid at target 1536, but at least one frozen transition ratio fails target or robustness transfer. Retain the quotient as instrumentation and retire the current finite scale-family claim without refitting this holdout.")
    else:
        lines.append("An exact source, target, replay, relabel, witness, identity, compression, or non-collapse condition failed. Treat the round as instrumentation failure rather than target-scale evidence.")
    lines.extend([
        "",
        "Causal-depth retention remains construction-adjacent because the map itself bins by depth. Antichain-width and dependency-density retention are less direct, but all three still come from one chosen map. Target transfer is therefore stronger than v16c repetition, yet it is not map-independent evidence.",
        "",
        "## Evidential boundary",
        "",
        "A pass supports one reproducible finite hierarchy across two target sizes. It does not establish convergence as target grows, a metric, a continuum, Lorentz covariance, quantum structure, or laws matching our universe.",
        "",
        "## Next decision",
        "",
    ])
    if overall == "pass_to_v16e_independent_coarse_map_gate":
        lines.append("Design one preregistered v16e contrast whose primary map is not defined by causal-depth bins. It must be relabel-invariant, witnessed, and evaluated against null/coarsening controls before more target scaling.")
    elif overall == "finite_coarse_map_not_target_transferable":
        lines.append("Stop this scale-family track. Diagnose the failed frozen ratio descriptively, but do not tune windows, metrics, or thresholds on v16d.")
    else:
        lines.append("Repair the smallest exact instrumentation defect before any new dynamics; do not reinterpret partial output as a scale result.")
    lines.append("")
    return "\n".join(lines)


def verify_outputs() -> None:
    assignments, _, _ = load_and_verify_preregistration()
    expected_runs = len(assignments)
    run_rows = read_csv(DOC / "v16d_run_summary.csv")
    event_rows = read_csv(DOC / "v16d_event_log.csv")
    fine_edges = read_csv(DOC / "v16d_fine_dependency_edges.csv")
    memberships = read_csv(DOC / "v16d_coarse_membership.csv")
    coarse_edges = read_csv(DOC / "v16d_coarse_dependency_edges.csv")
    scale_rows = read_csv(DOC / "v16d_scale_summary.csv")
    map_rows = read_csv(DOC / "v16d_map_audit.csv")
    replay_rows = read_csv(DOC / "v16d_topological_replay_audit.csv")
    relabel_rows = read_csv(DOC / "v16d_relabel_replay_audit.csv")
    target_rows = read_csv(DOC / "v16d_target_transfer.csv")
    gate_rows = read_csv(DOC / "v16d_gate_evaluation.csv")
    key_fields = ("growth_seed", "run_offset", "arm", "run_seed")

    def key(row: Mapping[str, str]) -> Tuple[str, ...]:
        return tuple(row[field] for field in key_fields)

    assignment_keys = {key(row) for row in assignments}
    assert len(run_rows) == expected_runs and {key(row) for row in run_rows} == assignment_keys
    assert len(event_rows) == expected_runs * STEPS
    assert len(memberships) == expected_runs * STEPS * len(SCALE_WINDOWS)
    assert len(scale_rows) == expected_runs * len(SCALE_WINDOWS)
    assert len(map_rows) == expected_runs * len(SCALE_WINDOWS)
    assert len(replay_rows) == expected_runs * TOPOLOGICAL_REPLAYS
    assert len(relabel_rows) == expected_runs
    assert len(target_rows) == len(TRANSITIONS) * len(PRIMARY_METRICS)
    assert all(int(row["map_integrity_pass"]) == 1 for row in map_rows)
    assert all(int(row["relabel_pass"]) == 1 and int(row["coarse_map_transport_pass"]) == 1 for row in relabel_rows)
    assert all(
        int(row["topological_order_valid"]) == 1
        and int(row["context_failures"]) == 0
        and int(row["final_structure_equal"]) == 1
        for row in replay_rows
    )

    events_by_run: Dict[Tuple[str, ...], Set[int]] = defaultdict(set)
    fine_edge_count: Counter[Tuple[str, ...]] = Counter()
    memberships_by_run_scale: Dict[Tuple[Tuple[str, ...], int], List[Dict[str, str]]] = defaultdict(list)
    coarse_edges_by_run_scale: Dict[Tuple[Tuple[str, ...], int], List[Dict[str, str]]] = defaultdict(list)
    scale_by_run: Dict[Tuple[Tuple[str, ...], int], Dict[str, str]] = {}
    for row in event_rows:
        events_by_run[key(row)].add(int(row["event_id"]))
    for row in fine_edges:
        fine_edge_count[key(row)] += 1
    for row in memberships:
        memberships_by_run_scale[(key(row), int(row["scale_window"]))].append(row)
    for row in coarse_edges:
        assert int(row["fine_edge_witness_count"]) >= 1
        coarse_edges_by_run_scale[(key(row), int(row["scale_window"]))].append(row)
    for row in scale_rows:
        scale_by_run[(key(row), int(row["scale_window"]))] = row
    for run_key in assignment_keys:
        assert events_by_run[run_key] == set(range(STEPS))
        for window in SCALE_WINDOWS:
            member_rows = memberships_by_run_scale[(run_key, window)]
            assert {int(row["event_id"]) for row in member_rows} == set(range(STEPS))
            scale = scale_by_run[(run_key, window)]
            assert len({int(row["coarse_event_id"]) for row in member_rows}) == int(scale["coarse_nodes"])
            assert len(coarse_edges_by_run_scale[(run_key, window)]) == int(scale["coarse_edges"])
            if window == 1:
                assert all(int(row["event_id"]) == int(row["coarse_event_id"]) for row in member_rows)
                assert len(coarse_edges_by_run_scale[(run_key, window)]) == fine_edge_count[run_key]
    overall = [row for row in gate_rows if row["gate"] == "v16d_overall"]
    assert len(overall) == 1 and overall[0]["status"] in {
        "pass_to_v16e_independent_coarse_map_gate",
        "finite_coarse_map_not_target_transferable",
        "v16d_instrumentation_failed",
    }
    print(
        f"[v16d] output verification pass runs={expected_runs} events={len(event_rows)} "
        f"memberships={len(memberships)} coarse_edges={len(coarse_edges)} overall={overall[0]['status']}"
    )


def self_test() -> None:
    assert frozen_map_contract_pass()
    assert STEPS == TARGET_NODES * EVENTS_PER_INITIAL_NODE
    dag = v16b.DependencyDAG()
    dag.predecessors = [
        {},
        {},
        {0: {"RAW:node:0"}},
        {1: {"RAW:node:1"}},
        {2: {"RAW:node:2"}, 3: {"RAW:node:3"}},
    ]
    prefix = {"growth_seed": -1, "run_offset": -1, "arm": "self_test", "run_seed": 1}
    scale_rows: List[Dict[str, Any]] = []
    for window in SCALE_WINDOWS:
        membership, edges, summary, audit = v16c.coarse_grain(dag, window, prefix)
        assert len(membership) == 5
        assert int(audit["map_integrity_pass"]) == 1
        assert all(int(row["fine_edge_witness_count"]) >= 1 for row in edges)
        scale_rows.append(summary)
    assert int(scale_rows[0]["coarse_nodes"]) == 5
    assert len(v16c.transition_rows(scale_rows)) == len(TRANSITIONS) * len(PRIMARY_METRICS)
    print("[v16d] self-test pass")


def run() -> None:
    assignments, local_rate, source_rows = load_and_verify_preregistration()
    adapter = v16ac.LocalSeedClockAdapter(local_rate)
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    target_rows = holdout_target_rows(base_rows)
    if int(target_rows[0]["separated_from_source"]) != 1 or int(target_rows[0]["mean_initial_nodes"]) != TARGET_NODES:
        raise RuntimeError("v16d target hygiene failed")
    ensemble_name = ensembles[0].name
    params = v16a.anchor_params()
    event_rows: List[Dict[str, Any]] = []
    fine_edge_rows: List[Dict[str, Any]] = []
    run_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    relabel_rows: List[Dict[str, Any]] = []
    membership_rows: List[Dict[str, Any]] = []
    coarse_edge_rows: List[Dict[str, Any]] = []
    scale_rows: List[Dict[str, Any]] = []
    map_rows: List[Dict[str, Any]] = []
    transitions: List[Dict[str, Any]] = []
    for index, assignment in enumerate(assignments, start=1):
        base = base_states[(ensemble_name, int(assignment["growth_seed"]))]
        events, fine_edges, run_row, replays, relabel, dag = run_assignment(base, assignment, params, adapter)
        prefix = {key: run_row[key] for key in ("growth_seed", "run_offset", "arm", "run_seed")}
        run_scales: List[Dict[str, Any]] = []
        for window in SCALE_WINDOWS:
            memberships, coarse_edges, summary, audit = v16c.coarse_grain(dag, window, prefix)
            membership_rows.extend(memberships)
            coarse_edge_rows.extend(coarse_edges)
            scale_rows.append(summary)
            run_scales.append(summary)
            map_rows.append(audit)
        transitions.extend(v16c.transition_rows(run_scales))
        event_rows.extend(events)
        fine_edge_rows.extend(fine_edges)
        run_rows.append(run_row)
        replay_rows.extend(replays)
        relabel_rows.append(relabel)
        print(
            f"[v16d] runs={index}/{len(assignments)} arm={assignment['arm']} "
            f"nodes={run_scales[0]['coarse_nodes']}/{run_scales[1]['coarse_nodes']}/{run_scales[2]['coarse_nodes']}"
        )

    local_rows = local_stability_rows(transitions)
    growth_rows = growth_transfer_rows(transitions)
    scheduler_rows = scheduler_transfer_rows(transitions, run_rows)
    target_transfer = target_transfer_rows(transitions)
    gate_rows, overall = gate_evaluation(
        True, target_rows, run_rows, replay_rows, relabel_rows, scale_rows, map_rows,
        local_rows, growth_rows, scheduler_rows, target_transfer,
    )
    write_csv(DOC / "v16d_source_chain.csv", source_rows)
    write_csv(DOC / "v16d_target_summary.csv", target_rows)
    write_csv(DOC / "v16d_event_log.csv", event_rows)
    write_csv(DOC / "v16d_fine_dependency_edges.csv", fine_edge_rows)
    write_csv(DOC / "v16d_run_summary.csv", run_rows)
    write_csv(DOC / "v16d_coarse_membership.csv", membership_rows)
    write_csv(DOC / "v16d_coarse_dependency_edges.csv", coarse_edge_rows)
    write_csv(DOC / "v16d_scale_summary.csv", scale_rows)
    write_csv(DOC / "v16d_transition_ratios.csv", transitions)
    write_csv(DOC / "v16d_map_audit.csv", map_rows)
    write_csv(DOC / "v16d_topological_replay_audit.csv", replay_rows)
    write_csv(DOC / "v16d_relabel_replay_audit.csv", relabel_rows)
    write_csv(DOC / "v16d_local_stability.csv", local_rows)
    write_csv(DOC / "v16d_growth_transfer.csv", growth_rows)
    write_csv(DOC / "v16d_scheduler_transfer.csv", scheduler_rows)
    write_csv(DOC / "v16d_target_transfer.csv", target_transfer)
    write_csv(DOC / "v16d_gate_evaluation.csv", gate_rows)
    write_csv(DOC / "v16d_claim_ledger.csv", claim_rows(overall))
    report = build_report(
        source_rows, target_rows, run_rows, scale_rows, local_rows, growth_rows,
        scheduler_rows, target_transfer, gate_rows, overall,
    )
    (DOC / "v16d_target_scale_holdout.md").write_text(report, encoding="utf-8")
    recommendation = "\n".join([
        "# Operativ anbefaling v0.16d",
        "",
        f"Status: `{overall}`.",
        "",
        "- Behold resultatet avgrenset til det uendrede v16c-kartet ved target 1024 og 1536 med lik eventtetthet.",
        "- Ved full pass: test ett uavhengig, relabel-invariant coarse-map i v16e; ikke skaler samme map videre som standard.",
        "- Ved target-transfer-fail: behold kartet som instrumentering, men avslutt scale-family-claim uten refit.",
        "- Ved strukturell fail: reparer bare minste instrumenteringsfeil foer ny dynamikk.",
        "- Ikke promoter finite target-transfer til continuum, spacetime, Lorentz-symmetri eller universell kausalitet.",
        "",
    ])
    (DOC / "v0_16d_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    lay = "\n".join([
        "# v0.16d for ikke-spesialister",
        "",
        "Vi beholdt noeyaktig samme maate aa lage grove hendelsesgrafer paa, men oekte startgrafen fra 1024 til 1536 noder. Antall hendelser ble oekt mekanisk slik at hver startnode fortsatt fikk samme gjennomsnittlige eksponering.",
        "",
        f"Statusen er `{overall}`. En full pass betyr at dette bestemte endelige kartet oppfoerer seg likt nok paa to stoerrelser til aa fortjene en test med en uavhengig coarse-graining. Det er ikke et bevis for kontinuerlig romtid eller relativitet.",
        "",
    ])
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16d.md").write_text(lay, encoding="utf-8")
    print(
        f"[v16d] overall={overall} runs={len(run_rows)} events={len(event_rows)} "
        f"fine_edges={len(fine_edge_rows)} memberships={len(membership_rows)}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="v16d target-scale holdout")
    parser.add_argument("--freeze-baseline", action="store_true")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    selected = sum((args.freeze_baseline, args.prepare_only, args.self_test, args.verify_only))
    if selected > 1:
        raise ValueError("choose only one mode")
    if args.self_test:
        self_test()
    elif args.freeze_baseline:
        freeze_baseline()
    elif args.prepare_only:
        prepare()
    elif args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
