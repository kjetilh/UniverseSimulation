#!/usr/bin/env python3
"""v16h fresh directly rate-logged clock/depth mechanism holdout.

This gate validates the v16g total-rate explanation on fresh dynamics. It logs
all pre-event family rates and the selected descriptor hazard while each event
is generated, then applies the frozen v16g residual-permutation analysis.

This is a finite simulator-mechanism test. The simulation clock is not physical
proper time, and this gate does not test Lorentz symmetry, spacetime, continuum
limits, particles, entanglement, or universal causality.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v16a_disjoint_event_commutation_gate as v16a
import relational_universe_v16ac_local_seed_adapter_gate as v16ac
import relational_universe_v16b_intrinsic_event_dag_gate as v16b
import relational_universe_v16c_three_scale_coarse_graining_pilot as v16c
import relational_universe_v16g_clock_depth_boundary_mechanism_gate as v16g


DOC = Path("Documentation")
SCRIPT = Path("relational_universe_v16h_fresh_rate_logged_mechanism_holdout.py")
PREREG = DOC / "v16h_pre_registration.csv"
FROZEN_BASELINE = DOC / "v16h_frozen_v16g_baseline.csv"

TARGET_NODES = 1536
EVENTS_PER_INITIAL_NODE = 2
STEPS = TARGET_NODES * EVENTS_PER_INITIAL_NODE
GROWTH_SEEDS = (4001, 4127)
RUN_OFFSETS = (81013, 81047, 81091)
ARMS = ("current_global", "exposure_matched_local")
PRIMARY_ARM = "exposure_matched_local"
DEPTH_WINDOW = 16
CLOCK_BINS = (128, 64, 32)
NULL_REPLICATES = 64
TOPOLOGICAL_REPLAYS = 2
MIN_REORDERED_POSITION_FRACTION = 0.10
MIN_MEDIAN_EXPLAINED_FRACTION = 0.50
MIN_CONDITIONALLY_NONSURPRISING_FRACTION = 5.0 / 6.0
MIN_GROUP_NONSURPRISING_FRACTION = 0.50
MAX_ABS_CONDITIONAL_Z = 2.0
MIN_EMPIRICAL_LOWER_TAIL_P = 0.05
BASE_GAP_TRANSFER_RANGE = (0.50, 2.00)
DIRECT_RATE_TOLERANCE = 1.0e-12

V16G_SCRIPT = Path("relational_universe_v16g_clock_depth_boundary_mechanism_gate.py")
V16G_GATE = DOC / "v16g_gate_evaluation.csv"
V16G_EXECUTION = DOC / "v16g_execution_audit.csv"
V16G_LOCAL = DOC / "v16g_local_mechanism_gate.csv"
V16G_RUNS = DOC / "v16g_mechanism_run_summary.csv"
V16E_PREREG = DOC / "v16e_pre_registration.csv"

read_csv = v16c.read_csv
write_csv = v16c.write_csv
mean = v16c.mean
median = v16c.median
sample_sd = v16g.sample_sd
RUN_FIELDS = ("growth_seed", "run_offset", "arm", "run_seed")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_key(row: Mapping[str, Any]) -> Tuple[str, ...]:
    return tuple(str(row[field]) for field in RUN_FIELDS)


def numeric_prefix(key: Sequence[str]) -> Dict[str, Any]:
    return {
        "growth_seed": int(key[0]),
        "run_offset": int(key[1]),
        "arm": key[2],
        "run_seed": int(key[3]),
    }


def group_rows(rows: Iterable[Mapping[str, Any]]) -> Dict[Tuple[str, ...], List[Dict[str, Any]]]:
    grouped: Dict[Tuple[str, ...], List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[run_key(row)].append(dict(row))
    return grouped


def run_seed(growth_seed: int, run_offset: int, arm: str) -> int:
    base = 1_800_000_000 + growth_seed * 10_000 + run_offset
    return base + (100_000_000 if arm == "exposure_matched_local" else 0)


def frozen_local_rate() -> float:
    rows = read_csv(V16E_PREREG)
    values = {float(row["frozen_local_rate"]) for row in rows}
    if len(values) != 1 or abs(next(iter(values)) - v16ac.FROZEN_LOCAL_RATE) > DIRECT_RATE_TOLERANCE:
        raise ValueError("v16e preregistration does not match the frozen local adapter rate")
    return values.pop()


def source_contract_rows() -> Tuple[List[Dict[str, Any]], bool]:
    gates = read_csv(V16G_GATE)
    overall = [row for row in gates if row["gate"] == "v16g_overall"]
    execution = read_csv(V16G_EXECUTION)
    required = "pass_to_v16h_fresh_rate_logged_mechanism_holdout"
    gate_pass = len(overall) == 1 and overall[0]["status"] == required
    audit_pass = (
        len(execution) == 1
        and int(execution[0]["primary_gate_affected"]) == 0
        and int(execution[0]["design_changed"]) == 0
        and int(execution[0]["source_data_changed"]) == 0
    )
    rows = [
        {
            "source": "v16g_overall",
            "artifact": V16G_GATE.name,
            "sha256": file_sha256(V16G_GATE),
            "observed": overall[0]["status"] if len(overall) == 1 else "invalid",
            "required": required,
            "source_pass": int(gate_pass),
        },
        {
            "source": "v16g_execution_audit",
            "artifact": V16G_EXECUTION.name,
            "sha256": file_sha256(V16G_EXECUTION),
            "observed": "primary_unaffected" if audit_pass else "invalid",
            "required": "primary_unaffected;design_unchanged;source_unchanged",
            "source_pass": int(audit_pass),
        },
        {
            "source": "frozen_local_rate",
            "artifact": V16E_PREREG.name,
            "sha256": file_sha256(V16E_PREREG),
            "observed": frozen_local_rate(),
            "required": v16ac.FROZEN_LOCAL_RATE,
            "source_pass": 1,
        },
    ]
    return rows, gate_pass and audit_pass


def frozen_baseline_rows() -> List[Dict[str, Any]]:
    local = read_csv(V16G_LOCAL)
    rows: List[Dict[str, Any]] = []
    for clock_bins in CLOCK_BINS:
        selected = [row for row in local if int(row["clock_bins"]) == clock_bins]
        if len(selected) != 1 or int(selected[0]["local_mechanism_pass"]) != 1:
            raise ValueError(f"v16g local baseline is incomplete for bins={clock_bins}")
        row = selected[0]
        rows.append({
            "clock_bins": clock_bins,
            "source_primary_arm": row["primary_arm"],
            "source_n_runs": int(row["n_runs"]),
            "source_median_waiting_minus_observed_nmi": float(row["median_waiting_minus_observed_nmi"]),
            "source_median_rate_explained_fraction": float(row["median_rate_explained_fraction"]),
            "source_conditionally_nonsurprising_fraction": float(row["conditionally_nonsurprising_fraction"]),
            "base_gap_ratio_low": BASE_GAP_TRANSFER_RANGE[0],
            "base_gap_ratio_high": BASE_GAP_TRANSFER_RANGE[1],
            "source_local_sha256": file_sha256(V16G_LOCAL),
            "source_runs_sha256": file_sha256(V16G_RUNS),
            "frozen_before_fresh_dynamics": 1,
        })
    return rows


def frozen_spec() -> Dict[str, Any]:
    return {
        "gate": "v16h_fresh_direct_rate_logged_mechanism_holdout",
        "target_nodes": TARGET_NODES,
        "events_per_initial_node": EVENTS_PER_INITIAL_NODE,
        "steps": STEPS,
        "growth_seeds": list(GROWTH_SEEDS),
        "run_offsets": list(RUN_OFFSETS),
        "arms": list(ARMS),
        "primary_arm": PRIMARY_ARM,
        "depth_window": DEPTH_WINDOW,
        "clock_bins": list(CLOCK_BINS),
        "null_families": list(v16g.NULL_FAMILIES),
        "primary_null_family": v16g.PRIMARY_NULL_FAMILY,
        "null_replicates": NULL_REPLICATES,
        "topological_replays": TOPOLOGICAL_REPLAYS,
        "min_reordered_position_fraction": MIN_REORDERED_POSITION_FRACTION,
        "min_median_explained_fraction": MIN_MEDIAN_EXPLAINED_FRACTION,
        "min_conditionally_nonsurprising_fraction": MIN_CONDITIONALLY_NONSURPRISING_FRACTION,
        "min_group_nonsurprising_fraction": MIN_GROUP_NONSURPRISING_FRACTION,
        "max_abs_conditional_z": MAX_ABS_CONDITIONAL_Z,
        "min_empirical_lower_tail_p": MIN_EMPIRICAL_LOWER_TAIL_P,
        "base_gap_transfer_range": list(BASE_GAP_TRANSFER_RANGE),
        "direct_rate_tolerance": DIRECT_RATE_TOLERANCE,
        "success_decision": "validate_total_rate_mechanism_and_retire_clock_depth_common_geometry",
        "scope": "finite_fresh_dynamics_simulator_mechanism",
    }


def spec_digest() -> str:
    payload = json.dumps(frozen_spec(), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def preregistration_rows() -> List[Dict[str, Any]]:
    if not FROZEN_BASELINE.exists():
        raise ValueError("missing frozen v16g baseline; run --prepare-only")
    source_rows, source_pass = source_contract_rows()
    if not source_pass:
        raise ValueError(f"v16g source contract failed: {source_rows}")
    rows: List[Dict[str, Any]] = []
    for growth_seed in GROWTH_SEEDS:
        for run_offset in RUN_OFFSETS:
            for arm in ARMS:
                rows.append({
                    "purpose_ref": "purpose://prompt.unknown",
                    "spec_digest": spec_digest(),
                    "holdout_script_sha256": file_sha256(SCRIPT),
                    "v16g_script_sha256": file_sha256(V16G_SCRIPT),
                    "source_gate_sha256": file_sha256(V16G_GATE),
                    "source_execution_audit_sha256": file_sha256(V16G_EXECUTION),
                    "frozen_baseline_sha256": file_sha256(FROZEN_BASELINE),
                    "target_nodes": TARGET_NODES,
                    "events_per_initial_node": EVENTS_PER_INITIAL_NODE,
                    "growth_seed": growth_seed,
                    "run_offset": run_offset,
                    "arm": arm,
                    "run_seed": run_seed(growth_seed, run_offset, arm),
                    "steps": STEPS,
                    "depth_window": DEPTH_WINDOW,
                    "clock_bins": ";".join(str(value) for value in CLOCK_BINS),
                    "null_replicates_per_family": NULL_REPLICATES,
                    "primary_null_family": v16g.PRIMARY_NULL_FAMILY,
                    "frozen_local_rate": frozen_local_rate(),
                    "min_median_explained_fraction": MIN_MEDIAN_EXPLAINED_FRACTION,
                    "min_conditionally_nonsurprising_fraction": MIN_CONDITIONALLY_NONSURPRISING_FRACTION,
                    "min_group_nonsurprising_fraction": MIN_GROUP_NONSURPRISING_FRACTION,
                    "base_gap_ratio_low": BASE_GAP_TRANSFER_RANGE[0],
                    "base_gap_ratio_high": BASE_GAP_TRANSFER_RANGE[1],
                    "prepared_before_fresh_dynamics": 1,
                })
    return rows


def prepare() -> None:
    source_rows, source_pass = source_contract_rows()
    if not source_pass:
        raise ValueError(f"v16g source contract failed: {source_rows}")
    write_csv(FROZEN_BASELINE, frozen_baseline_rows())
    rows = preregistration_rows()
    write_csv(PREREG, rows)
    print(f"[v16h] prepared rows={len(rows)} digest={rows[0]['spec_digest']}")


def load_and_verify_preregistration() -> Tuple[List[Dict[str, str]], float, List[Dict[str, Any]]]:
    if not PREREG.exists():
        raise ValueError("missing v16h preregistration; run --prepare-only")
    source_rows, source_pass = source_contract_rows()
    if not source_pass:
        raise ValueError("v16g source contract no longer passes")
    observed = read_csv(PREREG)
    expected = preregistration_rows()
    expected_strings = [{key: str(value) for key, value in row.items()} for row in expected]
    if observed != expected_strings:
        raise ValueError("v16h preregistration changed")
    rates = {float(row["frozen_local_rate"]) for row in observed}
    if len(rates) != 1:
        raise ValueError("v16h preregistration has inconsistent local rates")
    return observed, rates.pop(), source_rows


def run_assignment(
    base: v7.State,
    assignment: Mapping[str, str],
    params: v7.Params,
    adapter: v16ac.LocalSeedClockAdapter,
) -> Tuple[
    List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any],
    List[Dict[str, Any]], Dict[str, Any], v16b.DependencyDAG,
]:
    initial_state = base.clone()
    state = base.clone()
    rng = random.Random(int(assignment["run_seed"]))
    next_node_id, next_token_id = v08b.next_ids_from_state(state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)
    dag = v16b.DependencyDAG()
    trace: List[v16b.TraceEvent] = []
    direct_rates: List[Dict[str, Any]] = []
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
        pre_nodes = state.g.num_nodes()
        pre_tokens = state.token_count()
        rates = (
            v7.family_rates(state, params)
            if assignment["arm"] == "current_global"
            else adapter.family_rates(state, params)
        )
        family, total_rate = v16b.choose_family(rates, rng)
        rate_sum = sum(max(0.0, float(rates[name])) for name in ("seed", "token", "birth", "death"))
        invalid_events += int(total_rate <= 0.0 or abs(total_rate - rate_sum) > DIRECT_RATE_TOLERANCE)
        dt = rng.expovariate(total_rate)
        total_time += dt
        state.t += dt
        kernel = adapter.family_kernel(state, family, params)
        if not kernel:
            raise RuntimeError(f"empty kernel for positive family {family}")
        descriptor = tuple(v7.sample_from_dist(kernel, rng))
        descriptor_probability = float(kernel.get(descriptor, 0.0))
        selected_family_rate = float(rates[family])
        concrete_hazard = selected_family_rate * descriptor_probability
        invalid_events += int(descriptor_probability <= 0.0 or concrete_hazard <= 0.0)
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
        direct_rates.append({
            "stage": "v16h_fresh_dynamics",
            **prefix,
            "event_id": step - 1,
            "step": step,
            "family": family,
            "event_type": event_type,
            "dt": dt,
            "time": total_time,
            "pre_event_nodes": pre_nodes,
            "pre_event_tokens": pre_tokens,
            "seed_rate": float(rates["seed"]),
            "token_rate": float(rates["token"]),
            "birth_rate": float(rates["birth"]),
            "death_rate": float(rates["death"]),
            "total_rate": total_rate,
            "selected_family_rate": selected_family_rate,
            "selected_family_rate_fraction": selected_family_rate / total_rate,
            "descriptor_probability": descriptor_probability,
            "concrete_descriptor_hazard": concrete_hazard,
            "normalized_waiting_residual": dt * total_rate,
        })

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
    for event_type in v16b.EVENT_TYPES:
        run_row[f"{event_type}_events"] = event_counts[event_type]
    return event_rows, dependency_rows, direct_rates, run_row, replay_rows, relabel_row, dag


def direct_rate_audit(
    base: v7.State,
    event_rows: Sequence[Mapping[str, Any]],
    direct_rows: Sequence[Mapping[str, Any]],
    run_row: Mapping[str, Any],
    local_rate: float,
) -> Dict[str, Any]:
    reconstructed, reconstruction = v16g.reconstruct_run_rates(
        base, event_rows, run_row, local_rate, "v16h_direct_log_reconstruction"
    )
    direct_by_id = {int(row["event_id"]): row for row in direct_rows}
    reconstructed_by_id = {int(row["event_id"]): row for row in reconstructed}
    discrete_errors = 0
    max_abs_error = 0.0
    numeric_fields = (
        "dt", "time", "pre_event_nodes", "pre_event_tokens", "total_rate",
        "selected_family_rate", "selected_family_rate_fraction", "descriptor_probability",
        "concrete_descriptor_hazard", "normalized_waiting_residual",
    )
    for event_id in range(len(event_rows)):
        direct = direct_by_id[event_id]
        replay = reconstructed_by_id[event_id]
        discrete_errors += int(direct["family"] != replay["family"] or direct["event_type"] != replay["event_type"])
        for field in numeric_fields:
            max_abs_error = max(max_abs_error, abs(float(direct[field]) - float(replay[field])))
        family_sum = sum(float(direct[f"{name}_rate"]) for name in ("seed", "token", "birth", "death"))
        max_abs_error = max(max_abs_error, abs(family_sum - float(direct["total_rate"])))
    prefix = {field: run_row[field] for field in RUN_FIELDS}
    parity = (
        len(direct_rows) == STEPS
        and len(reconstructed) == STEPS
        and int(reconstruction["reconstruction_pass"]) == 1
        and discrete_errors == 0
        and max_abs_error <= DIRECT_RATE_TOLERANCE
    )
    return {
        **prefix,
        "direct_rows": len(direct_rows),
        "reconstructed_rows": len(reconstructed),
        "reconstruction_total_errors": int(reconstruction["total_errors"]),
        "discrete_parity_errors": discrete_errors,
        "max_abs_numeric_error": max_abs_error,
        "tolerance": DIRECT_RATE_TOLERANCE,
        "residual_mean": mean(float(row["normalized_waiting_residual"]) for row in direct_rows),
        "residual_sd": sample_sd(float(row["normalized_waiting_residual"]) for row in direct_rows),
        "direct_log_parity_pass": int(parity),
    }


def grouped_mechanism_rows(
    run_rows: Sequence[Mapping[str, Any]], field: str,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    values = sorted({str(row[field]) for row in run_rows})
    for clock_bins in CLOCK_BINS:
        for value in values:
            selected = [row for row in run_rows if str(row[field]) == value and int(row["clock_bins"]) == clock_bins]
            explained = [float(row["rate_explained_fraction"]) for row in selected]
            nonsurprising = [
                abs(float(row["rate_conditional_z"])) <= MAX_ABS_CONDITIONAL_Z
                and float(row["rate_lower_tail_p"]) >= MIN_EMPIRICAL_LOWER_TAIL_P
                for row in selected
            ]
            rows.append({
                "group_field": field,
                "group_value": value,
                "clock_bins": clock_bins,
                "n_runs": len(selected),
                "median_rate_explained_fraction": median(explained),
                "conditionally_nonsurprising_fraction": mean(nonsurprising),
                "min_group_nonsurprising_fraction": MIN_GROUP_NONSURPRISING_FRACTION,
                "group_mechanism_pass": int(
                    median(explained) >= MIN_MEDIAN_EXPLAINED_FRACTION
                    and mean(nonsurprising) >= MIN_GROUP_NONSURPRISING_FRACTION
                ),
            })
    return rows


def baseline_transfer_rows(
    local_rows: Sequence[Mapping[str, Any]], baseline_rows: Sequence[Mapping[str, str]],
) -> List[Dict[str, Any]]:
    baseline = {int(row["clock_bins"]): row for row in baseline_rows}
    rows: List[Dict[str, Any]] = []
    for fresh in local_rows:
        clock_bins = int(fresh["clock_bins"])
        source = baseline[clock_bins]
        source_gap = float(source["source_median_waiting_minus_observed_nmi"])
        fresh_gap = float(fresh["median_waiting_minus_observed_nmi"])
        ratio = fresh_gap / source_gap if source_gap else 0.0
        rows.append({
            "clock_bins": clock_bins,
            "v16g_median_waiting_minus_observed_nmi": source_gap,
            "v16h_median_waiting_minus_observed_nmi": fresh_gap,
            "v16h_over_v16g_gap_ratio": ratio,
            "ratio_low": BASE_GAP_TRANSFER_RANGE[0],
            "ratio_high": BASE_GAP_TRANSFER_RANGE[1],
            "baseline_transfer_pass": int(BASE_GAP_TRANSFER_RANGE[0] <= ratio <= BASE_GAP_TRANSFER_RANGE[1]),
        })
    return rows


def gate_evaluation(
    source_pass: bool,
    target_rows: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    replay_rows: Sequence[Mapping[str, Any]],
    relabel_rows: Sequence[Mapping[str, Any]],
    map_audits: Sequence[Mapping[str, Any]],
    direct_audits: Sequence[Mapping[str, Any]],
    mechanism_rows: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
    baseline_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], str]:
    expected_runs = len(GROWTH_SEEDS) * len(RUN_OFFSETS) * len(ARMS)
    target_pass = len(target_rows) == 1 and int(target_rows[0]["mean_initial_nodes"]) == TARGET_NODES
    run_pass = len(run_rows) == expected_runs and all(
        int(row["n_events"]) == STEPS and int(row["invalid_events"]) == 0
        and int(row["fine_acyclic"]) == 1 and int(row["fine_edge_witness_errors"]) == 0
        for row in run_rows
    )
    replay_pass = (
        len(replay_rows) == expected_runs * TOPOLOGICAL_REPLAYS
        and all(
            int(row["topological_order_valid"]) and int(row["context_failures"]) == 0
            and int(row["final_structure_equal"]) and float(row["changed_position_fraction"]) >= MIN_REORDERED_POSITION_FRACTION
            for row in replay_rows
        )
    )
    relabel_pass = len(relabel_rows) == expected_runs and all(
        int(row["relabel_pass"]) and int(row["coarse_map_transport_pass"]) for row in relabel_rows
    )
    map_pass = len(map_audits) == expected_runs and all(int(row["map_integrity_pass"]) for row in map_audits)
    direct_pass = len(direct_audits) == expected_runs and all(int(row["direct_log_parity_pass"]) for row in direct_audits)
    relation_pass = len(mechanism_rows) == expected_runs * len(CLOCK_BINS) and all(
        float(row["waiting_minus_observed_nmi"]) > 0.0 for row in mechanism_rows
    )
    local_pass = len(local_rows) == len(CLOCK_BINS) and all(int(row["local_mechanism_pass"]) for row in local_rows)
    baseline_pass = len(baseline_rows) == len(CLOCK_BINS) and all(int(row["baseline_transfer_pass"]) for row in baseline_rows)
    growth_pass = len(growth_rows) == len(GROWTH_SEEDS) * len(CLOCK_BINS) and all(int(row["group_mechanism_pass"]) for row in growth_rows)
    scheduler_pass = len(scheduler_rows) == len(ARMS) * len(CLOCK_BINS) and all(int(row["group_mechanism_pass"]) for row in scheduler_rows)
    instrumentation = all((source_pass, target_pass, run_pass, replay_pass, relabel_pass, map_pass, direct_pass))
    mechanism = all((relation_pass, local_pass, baseline_pass, growth_pass, scheduler_pass))
    if not instrumentation:
        overall = "v16h_instrumentation_failed"
    elif mechanism:
        overall = "total_rate_mechanism_validated_retire_clock_depth_common_geometry"
    else:
        overall = "fresh_total_rate_mechanism_not_validated_reassess_clock_map"
    gates = [
        {"gate": "v16g_source_contract", "status": "pass" if source_pass else "fail", "observed": int(source_pass), "required": 1, "decision": "continue" if source_pass else "stop"},
        {"gate": "fresh_target_hygiene", "status": "pass" if target_pass else "fail", "observed": target_rows[0]["mean_initial_nodes"] if len(target_rows) == 1 else len(target_rows), "required": TARGET_NODES, "decision": "continue" if target_pass else "repair_target"},
        {"gate": "fresh_run_and_dag_integrity", "status": "pass" if run_pass else "fail", "observed": f"runs={len(run_rows)};invalid={sum(int(row['invalid_events']) for row in run_rows)}", "required": f"runs={expected_runs};invalid=0", "decision": "continue" if run_pass else "repair_runtime"},
        {"gate": "topological_replay", "status": "pass" if replay_pass else "fail", "observed": f"replays={len(replay_rows)};failures={sum(not int(row['final_structure_equal']) or int(row['context_failures']) for row in replay_rows)}", "required": f"replays={expected_runs * TOPOLOGICAL_REPLAYS};failures=0", "decision": "continue" if replay_pass else "repair_support"},
        {"gate": "relabel_and_depth_map", "status": "pass" if relabel_pass and map_pass else "fail", "observed": f"relabel={sum(int(row['relabel_pass']) for row in relabel_rows)}/{len(relabel_rows)};maps={sum(int(row['map_integrity_pass']) for row in map_audits)}/{len(map_audits)}", "required": f"{expected_runs}/{expected_runs};{expected_runs}/{expected_runs}", "decision": "continue" if relabel_pass and map_pass else "repair_map"},
        {"gate": "direct_rate_log_parity", "status": "pass" if direct_pass else "fail", "observed": f"passes={sum(int(row['direct_log_parity_pass']) for row in direct_audits)}/{len(direct_audits)};max_error={max(float(row['max_abs_numeric_error']) for row in direct_audits):.3e}", "required": f"{expected_runs}/{expected_runs};max_error<={DIRECT_RATE_TOLERANCE}", "decision": "continue" if direct_pass else "repair_rate_log"},
        {"gate": "v16f_relation_fresh_reproduction", "status": "pass" if relation_pass else "fail", "observed": f"positive_gap={sum(float(row['waiting_minus_observed_nmi']) > 0.0 for row in mechanism_rows)}/{len(mechanism_rows)}", "required": f"{expected_runs * len(CLOCK_BINS)}/{expected_runs * len(CLOCK_BINS)}", "decision": "continue" if relation_pass else "reassess_clock_map"},
        {"gate": "fresh_total_rate_mechanism", "status": "pass" if local_pass else "fail", "observed": f"passing_bins={sum(int(row['local_mechanism_pass']) for row in local_rows)}/{len(local_rows)}", "required": f"{len(CLOCK_BINS)}/{len(CLOCK_BINS)}", "decision": "retire_common_geometry" if local_pass else "mechanism_not_validated"},
        {"gate": "v16g_to_v16h_gap_transfer", "status": "pass" if baseline_pass else "fail", "observed": ";".join(f"{row['clock_bins']}:{float(row['v16h_over_v16g_gap_ratio']):.6f}" for row in baseline_rows), "required": f"each in [{BASE_GAP_TRANSFER_RANGE[0]},{BASE_GAP_TRANSFER_RANGE[1]}]", "decision": "continue" if baseline_pass else "hold_transfer"},
        {"gate": "fresh_growth_transfer", "status": "pass" if growth_pass else "fail", "observed": f"passing_groups={sum(int(row['group_mechanism_pass']) for row in growth_rows)}/{len(growth_rows)}", "required": f"{len(growth_rows)}/{len(growth_rows)}", "decision": "continue" if growth_pass else "growth_sensitive"},
        {"gate": "fresh_scheduler_transfer", "status": "pass" if scheduler_pass else "fail", "observed": f"passing_groups={sum(int(row['group_mechanism_pass']) for row in scheduler_rows)}/{len(scheduler_rows)}", "required": f"{len(scheduler_rows)}/{len(scheduler_rows)}", "decision": "continue" if scheduler_pass else "scheduler_sensitive"},
        {"gate": "v16h_overall", "status": overall, "observed": f"instrumentation={int(instrumentation)};mechanism={int(mechanism)}", "required": "instrumentation=1;mechanism=1", "decision": overall},
    ]
    return gates, overall


def claim_rows(overall: str) -> List[Dict[str, Any]]:
    validated = overall == "total_rate_mechanism_validated_retire_clock_depth_common_geometry"
    return [
        {"claim_id": "C1", "claim": "Fresh v16h events carry complete direct pre-event rate logs that match exact post-run reconstruction.", "status": "supported" if validated else "tested", "evidence": "v16h_direct_rate_audit.csv;v16h_direct_rate_event_log.csv", "scope_limit": "declared simulator, fresh finite histories"},
        {"claim_id": "C2", "claim": "The pre-event total-rate profile explains the v16f clock/depth anti-alignment on fresh dynamics.", "status": "supported" if validated else "unsupported", "evidence": "v16h_local_mechanism_gate.csv;v16h_baseline_transfer.csv", "scope_limit": "target 1536, two growth seeds, two scheduler arms, three clock resolutions"},
        {"claim_id": "C3", "claim": "Clock and depth maps provide independent evidence for one common emergent geometry.", "status": "unsupported", "evidence": "v16h_mechanism_run_summary.csv", "scope_limit": "the observed relation is accounted for by scheduler total-rate structure"},
        {"claim_id": "C4", "claim": "Event-family or concrete descriptor hazards define additional physical species or local laws.", "status": "unsupported", "evidence": "v16h_mechanism_run_summary.csv", "scope_limit": "secondary conditioning only; heuristic simulator observables"},
        {"claim_id": "C5", "claim": "The result establishes physical time, Lorentz symmetry, spacetime, continuum, particles, entanglement, or universal causality.", "status": "unsupported", "evidence": "none", "scope_limit": "not tested"},
    ]


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


def build_report(
    target_rows: Sequence[Mapping[str, Any]], direct_audits: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]], baseline_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]], scheduler_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]], overall: str,
) -> str:
    lines = [
        "# v16h fresh directly rate-logged mechanism holdout",
        "",
        f"Status: `{overall}`.",
        "",
        "## Evidential role",
        "",
        "v16h is a fresh dynamical holdout of the v16g total-rate explanation. New growth seeds and run offsets were frozen before execution. Target, event density, scheduler arms, depth/clock maps, null families, statistics, directions, and thresholds were unchanged.",
        "",
        f"Specification digest: `{spec_digest()}`. Script and v16g source hashes are locked in `v16h_pre_registration.csv`.",
        "",
        "## Direct-rate instrumentation",
        "",
        "Each event logs all four pre-event family rates, selected family rate, descriptor probability, concrete descriptor hazard, and unit-rate residual before the state mutation. An independent replay reconstructs the same quantities from the event history and must match within the frozen tolerance.",
        "",
    ]
    lines.extend(table(direct_audits, ("growth_seed", "run_offset", "arm", "direct_rows", "reconstruction_total_errors", "max_abs_numeric_error", "residual_mean", "residual_sd", "direct_log_parity_pass")))
    lines.extend(["", "## Fresh primary result", ""])
    lines.extend(table(local_rows, ("clock_bins", "n_runs", "median_waiting_minus_observed_nmi", "median_rate_explained_fraction", "median_family_rate_increment_over_rate", "median_family_hazard_increment_over_rate", "conditionally_nonsurprising_fraction", "local_mechanism_pass")))
    lines.extend(["", "## Frozen-baseline transfer", ""])
    lines.extend(table(baseline_rows, ("clock_bins", "v16g_median_waiting_minus_observed_nmi", "v16h_median_waiting_minus_observed_nmi", "v16h_over_v16g_gap_ratio", "ratio_low", "ratio_high", "baseline_transfer_pass")))
    lines.extend(["", "## Growth and scheduler diagnostics", ""])
    lines.extend(table(growth_rows, ("group_field", "group_value", "clock_bins", "median_rate_explained_fraction", "conditionally_nonsurprising_fraction", "group_mechanism_pass")))
    lines.append("")
    lines.extend(table(scheduler_rows, ("group_field", "group_value", "clock_bins", "median_rate_explained_fraction", "conditionally_nonsurprising_fraction", "group_mechanism_pass")))
    lines.extend(["", "## Gate evaluation", ""])
    lines.extend(table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation",
        "",
        "A full pass validates a finite simulator mechanism: the varying pre-event total rate accounts for the previously stable clock/depth partition relation on fresh histories. It therefore closes the simple common-geometry synthesis rather than strengthening it. The depth map remains a valid architecture artifact and the clock map remains a scheduler-sensitive diagnostic, but their relation is not independent geometry evidence.",
        "",
        "This does not establish physical time, Lorentz symmetry, metric spacetime, a continuum limit, particles, entanglement, or universal causal laws.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    assignments, local_rate, source_rows = load_and_verify_preregistration()
    adapter = v16ac.LocalSeedClockAdapter(local_rate)
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(
        ensembles, v10e.recommended_regime("fast_balanced"), list(GROWTH_SEEDS)
    )
    target_rows = v10e.summarize_bases(base_rows)
    if len(target_rows) != 1 or int(target_rows[0]["mean_initial_nodes"]) != TARGET_NODES:
        raise RuntimeError("v16h target hygiene failed")
    ensemble_name = ensembles[0].name
    params = v16a.anchor_params()
    event_rows: List[Dict[str, Any]] = []
    edge_rows: List[Dict[str, Any]] = []
    direct_rate_rows: List[Dict[str, Any]] = []
    direct_audits: List[Dict[str, Any]] = []
    run_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    relabel_rows: List[Dict[str, Any]] = []
    memberships: List[Dict[str, Any]] = []
    coarse_edges: List[Dict[str, Any]] = []
    map_summaries: List[Dict[str, Any]] = []
    map_audits: List[Dict[str, Any]] = []
    mechanism_rows: List[Dict[str, Any]] = []
    null_rows: List[Dict[str, Any]] = []
    for index, assignment in enumerate(assignments, start=1):
        base = base_states[(ensemble_name, int(assignment["growth_seed"]))]
        events, edges, rates, run_row, replays, relabel, dag = run_assignment(
            base, assignment, params, adapter
        )
        prefix = {field: run_row[field] for field in RUN_FIELDS}
        member_rows, coarse_edge_rows, map_summary, map_audit = v16c.coarse_grain(
            dag, DEPTH_WINDOW, prefix
        )
        depth = v16g.assignments_from_membership(member_rows, STEPS, "coarse_event_id")
        for clock_bins in CLOCK_BINS:
            mechanism_prefix = {
                "stage": "v16h_fresh_dynamics_holdout",
                **prefix,
                "depth_window": DEPTH_WINDOW,
                "clock_bins": clock_bins,
            }
            summary, nulls = v16g.mechanism_products(
                rates, depth, mechanism_prefix, NULL_REPLICATES, "v16h-fresh-dynamics-holdout"
            )
            mechanism_rows.append(summary)
            null_rows.extend(nulls)
        direct_audit = direct_rate_audit(base, events, rates, run_row, local_rate)
        if not int(direct_audit["direct_log_parity_pass"]):
            raise RuntimeError(f"v16h direct-rate parity failed: {direct_audit}")
        event_rows.extend(events)
        edge_rows.extend(edges)
        direct_rate_rows.extend(rates)
        direct_audits.append(direct_audit)
        run_rows.append(run_row)
        replay_rows.extend(replays)
        relabel_rows.append(relabel)
        memberships.extend(member_rows)
        coarse_edges.extend(coarse_edge_rows)
        map_summaries.append(map_summary)
        map_audits.append(map_audit)
        print(f"[v16h] runs={index}/{len(assignments)} arm={assignment['arm']} residual_mean={float(direct_audit['residual_mean']):.6f}")

    local_rows = v16g.local_mechanism_rows(mechanism_rows)
    baseline_rows = baseline_transfer_rows(local_rows, read_csv(FROZEN_BASELINE))
    growth_rows = grouped_mechanism_rows(mechanism_rows, "growth_seed")
    scheduler_rows = grouped_mechanism_rows(mechanism_rows, "arm")
    gates, overall = gate_evaluation(
        True, target_rows, run_rows, replay_rows, relabel_rows, map_audits,
        direct_audits, mechanism_rows, local_rows, baseline_rows, growth_rows, scheduler_rows,
    )
    write_csv(DOC / "v16h_source_chain.csv", source_rows)
    write_csv(DOC / "v16h_target_summary.csv", target_rows)
    write_csv(DOC / "v16h_event_log.csv", event_rows)
    write_csv(DOC / "v16h_fine_dependency_edges.csv", edge_rows)
    write_csv(DOC / "v16h_run_summary.csv", run_rows)
    write_csv(DOC / "v16h_topological_replay_audit.csv", replay_rows)
    write_csv(DOC / "v16h_relabel_replay_audit.csv", relabel_rows)
    write_csv(DOC / "v16h_depth_membership.csv", memberships)
    write_csv(DOC / "v16h_depth_coarse_edges.csv", coarse_edges)
    write_csv(DOC / "v16h_depth_map_summary.csv", map_summaries)
    write_csv(DOC / "v16h_depth_map_audit.csv", map_audits)
    write_csv(DOC / "v16h_direct_rate_event_log.csv", direct_rate_rows)
    write_csv(DOC / "v16h_direct_rate_audit.csv", direct_audits)
    write_csv(DOC / "v16h_mechanism_run_summary.csv", mechanism_rows)
    write_csv(DOC / "v16h_conditional_null_distribution.csv", null_rows)
    write_csv(DOC / "v16h_local_mechanism_gate.csv", local_rows)
    write_csv(DOC / "v16h_baseline_transfer.csv", baseline_rows)
    write_csv(DOC / "v16h_growth_mechanism_transfer.csv", growth_rows)
    write_csv(DOC / "v16h_scheduler_mechanism_transfer.csv", scheduler_rows)
    write_csv(DOC / "v16h_gate_evaluation.csv", gates)
    write_csv(DOC / "v16h_claim_ledger.csv", claim_rows(overall))
    (DOC / "v16h_fresh_rate_logged_mechanism_holdout.md").write_text(
        build_report(target_rows, direct_audits, local_rows, baseline_rows, growth_rows, scheduler_rows, gates, overall),
        encoding="utf-8",
    )
    recommendation = "\n".join([
        "# Operativ anbefaling v0.16h",
        "",
        f"Status: `{overall}`.",
        "",
        "- Ved full pass: avslutt clock/depth common-geometry-syntesen; totalrateprofilen er validert som den parsimoniske mekanismen.",
        "- Behold depth-kartet som arkitekturartefakt og clock-kartet som scheduler-sensitiv diagnostikk, ikke som to uavhengige geometrikart.",
        "- Ikke bruk mer budsjett paa samme clock/depth-NMI eller et tredje kart uten en ny, uavhengig fysisk motivert observabel.",
        "- Ikke presenter resultatet som fysisk tid, Lorentz-symmetri, spacetime, continuum, partikler eller entanglement.",
        "",
    ])
    (DOC / "v0_16h_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    lay = "\n".join([
        "# v0.16h for ikke-spesialister",
        "",
        "Vi kjoerte helt nye simuleringer og skrev ned den faktiske hendelsesraten foer hver hendelse. Deretter testet vi den samme forklaringen som ble funnet i gamle data, uten aa justere den til de nye resultatene.",
        "",
        f"Statusen er `{overall}`. En full pass betyr at forskjellen mellom klokke- og avhengighetskartet forklares av simulatorens varierende hendelsesrate. Det er nyttig mekanismekunnskap, men ikke tegn paa fysisk romtid.",
        "",
    ])
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16h.md").write_text(lay, encoding="utf-8")
    print(f"[v16h] overall={overall} runs={len(run_rows)} events={len(event_rows)} nulls={len(null_rows)}")


def verify_outputs() -> None:
    assignments, _, _ = load_and_verify_preregistration()
    expected_runs = len(assignments)
    events = read_csv(DOC / "v16h_event_log.csv")
    rates = read_csv(DOC / "v16h_direct_rate_event_log.csv")
    audits = read_csv(DOC / "v16h_direct_rate_audit.csv")
    runs = read_csv(DOC / "v16h_run_summary.csv")
    replays = read_csv(DOC / "v16h_topological_replay_audit.csv")
    relabels = read_csv(DOC / "v16h_relabel_replay_audit.csv")
    memberships = read_csv(DOC / "v16h_depth_membership.csv")
    maps = read_csv(DOC / "v16h_depth_map_audit.csv")
    mechanisms = read_csv(DOC / "v16h_mechanism_run_summary.csv")
    nulls = read_csv(DOC / "v16h_conditional_null_distribution.csv")
    gates = read_csv(DOC / "v16h_gate_evaluation.csv")
    assert expected_runs == 12
    assert len(events) == expected_runs * STEPS
    assert len(rates) == len(events)
    assert len(audits) == expected_runs and all(int(row["direct_log_parity_pass"]) for row in audits)
    assert len(runs) == expected_runs and all(int(row["invalid_events"]) == 0 for row in runs)
    assert len(replays) == expected_runs * TOPOLOGICAL_REPLAYS
    assert len(relabels) == expected_runs and all(int(row["relabel_pass"]) for row in relabels)
    assert len(memberships) == expected_runs * STEPS
    assert len(maps) == expected_runs and all(int(row["map_integrity_pass"]) for row in maps)
    assert len(mechanisms) == expected_runs * len(CLOCK_BINS)
    assert len(nulls) == len(mechanisms) * NULL_REPLICATES * len(v16g.NULL_FAMILIES)
    assert {row["null_family"] for row in nulls} == set(v16g.NULL_FAMILIES)
    for row in rates + mechanisms:
        for value in row.values():
            assert str(value).lower() not in {"nan", "inf", "-inf"}
    overall = [row for row in gates if row["gate"] == "v16h_overall"]
    assert len(overall) == 1 and overall[0]["status"] in {
        "total_rate_mechanism_validated_retire_clock_depth_common_geometry",
        "fresh_total_rate_mechanism_not_validated_reassess_clock_map",
        "v16h_instrumentation_failed",
    }
    print(f"[v16h] output verification pass runs={expected_runs} events={len(events)} nulls={len(nulls)} overall={overall[0]['status']}")


def self_test() -> None:
    assert STEPS == TARGET_NODES * EVENTS_PER_INITIAL_NODE
    assert CLOCK_BINS == v16g.SELECTED_CLOCK_BINS
    assert DEPTH_WINDOW == v16g.DEPTH_WINDOW
    assert NULL_REPLICATES == v16g.HOLDOUT_NULL_REPLICATES
    assert v16g.PRIMARY_NULL_FAMILY == "total_rate_profile"
    assert len({run_seed(growth, offset, arm) for growth in GROWTH_SEEDS for offset in RUN_OFFSETS for arm in ARMS}) == 12
    fake_local = [
        {"clock_bins": bins, "median_waiting_minus_observed_nmi": 0.01 * (index + 1)}
        for index, bins in enumerate(CLOCK_BINS)
    ]
    fake_baseline = [
        {"clock_bins": bins, "source_median_waiting_minus_observed_nmi": 0.01 * (index + 1)}
        for index, bins in enumerate(CLOCK_BINS)
    ]
    assert all(int(row["baseline_transfer_pass"]) for row in baseline_transfer_rows(fake_local, fake_baseline))
    print("[v16h] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16h fresh directly rate-logged mechanism holdout")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if sum((args.prepare_only, args.self_test, args.verify_only)) > 1:
        parser.error("choose at most one mode")
    if args.self_test:
        self_test()
    elif args.prepare_only:
        prepare()
    elif args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
