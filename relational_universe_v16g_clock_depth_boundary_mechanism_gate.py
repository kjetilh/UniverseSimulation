#!/usr/bin/env python3
"""v16g clock/depth boundary mechanism gate.

This gate asks whether the v16f clock/depth anti-alignment is explained by the
pre-event scheduler-rate profile and event-family/local descriptor hazards.
It reconstructs those quantities exactly from frozen event histories, then
compares the observed clock map with residual-permutation null clocks.

v16e histories already exist, so this is a frozen-data analysis holdout, not a
new dynamical holdout. The simulation clock is not physical proper time. This
gate does not test Lorentz symmetry, spacetime, continuum limits, particles,
entanglement, or universal causality.
"""
from __future__ import annotations

import argparse
import ast
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
import relational_universe_v16a_disjoint_event_commutation_gate as v16a
import relational_universe_v16ac_local_seed_adapter_gate as v16ac
import relational_universe_v16b_intrinsic_event_dag_gate as v16b
import relational_universe_v16c_three_scale_coarse_graining_pilot as v16c
import relational_universe_v16e_clock_slab_map_gate as v16e
import relational_universe_v16f_cross_map_relation_gate as v16f


DOC = Path("Documentation")
SCRIPT = Path("relational_universe_v16g_clock_depth_boundary_mechanism_gate.py")
CALIBRATION_AUDIT = DOC / "v16g_design_calibration_rate_audit.csv"
CALIBRATION_RUNS = DOC / "v16g_design_calibration_mechanism_runs.csv"
CALIBRATION_NULLS = DOC / "v16g_design_calibration_conditional_nulls.csv"
DESIGN_SELECTION = DOC / "v16g_design_selection.csv"
PREREG = DOC / "v16g_pre_registration.csv"

SELECTED_CLOCK_BINS = (128, 64, 32)
DEPTH_WINDOW = 16
CALIBRATION_NULL_REPLICATES = 64
HOLDOUT_NULL_REPLICATES = 64
ARMS = ("current_global", "exposure_matched_local")
PRIMARY_ARM = "exposure_matched_local"
NULL_FAMILIES = (
    "shuffled_waiting_time",
    "total_rate_profile",
    "event_family_rate_profile",
    "family_descriptor_hazard_profile",
)
PRIMARY_NULL_FAMILY = "total_rate_profile"

# These thresholds are design constants, calibrated only against v16c/v16d.
MIN_MEDIAN_EXPLAINED_FRACTION = 0.50
MIN_CONDITIONALLY_NONSURPRISING_FRACTION = 5.0 / 6.0
MAX_ABS_CONDITIONAL_Z = 2.0
MIN_EMPIRICAL_LOWER_TAIL_P = 0.05
TOLERANCE = 1.0e-12

read_csv = v16c.read_csv
write_csv = v16c.write_csv
mean = v16c.mean
median = v16c.median
sample_sd = v16e.sample_sd
stable_seed = v16e.stable_seed
RUN_FIELDS = ("growth_seed", "run_offset", "arm", "run_seed")

STAGES: Dict[str, Dict[str, Any]] = {
    "v16c": {
        "target_nodes": 1024,
        "event_log": DOC / "v16c_event_log.csv",
        "membership": DOC / "v16c_coarse_membership.csv",
        "run_summary": DOC / "v16c_run_summary.csv",
        "prereg": DOC / "v16c_pre_registration.csv",
    },
    "v16d": {
        "target_nodes": 1536,
        "event_log": DOC / "v16d_event_log.csv",
        "membership": DOC / "v16d_coarse_membership.csv",
        "run_summary": DOC / "v16d_run_summary.csv",
        "prereg": DOC / "v16d_pre_registration.csv",
    },
    "v16e": {
        "target_nodes": 1536,
        "event_log": DOC / "v16e_event_log.csv",
        "membership": DOC / "v16f_depth_membership.csv",
        "run_summary": DOC / "v16e_run_summary.csv",
        "prereg": DOC / "v16e_pre_registration.csv",
    },
}


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


def group_rows(rows: Iterable[Mapping[str, str]]) -> Dict[Tuple[str, ...], List[Dict[str, str]]]:
    grouped: Dict[Tuple[str, ...], List[Dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[run_key(row)].append(dict(row))
    return grouped


def expected_event_count(prereg_rows: Sequence[Mapping[str, str]]) -> int:
    values = {int(row["steps"]) for row in prereg_rows}
    if len(values) != 1:
        raise ValueError("stage preregistration has inconsistent step counts")
    return values.pop()


def split_resources(value: str) -> Tuple[str, ...]:
    return tuple(item for item in value.split(";") if item)


def summary_for_key(
    summaries: Mapping[Tuple[str, ...], List[Dict[str, str]]],
    key: Tuple[str, ...],
) -> Dict[str, str]:
    rows = summaries.get(key, [])
    if len(rows) != 1:
        raise ValueError(f"expected one run summary for {key}, found {len(rows)}")
    return rows[0]


def reconstruct_run_rates(
    base: v7.State,
    source_events: Sequence[Mapping[str, str]],
    source_summary: Mapping[str, str],
    local_rate: float,
    stage: str,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    events = sorted(source_events, key=lambda row: int(row["event_id"]))
    if not events:
        raise ValueError("cannot reconstruct an empty run")
    prefix = {"stage": stage, **numeric_prefix(run_key(events[0]))}
    arm = str(prefix["arm"])
    params = v16a.anchor_params()
    adapter = v16ac.LocalSeedClockAdapter(local_rate)
    state = base.clone()
    next_node_id, next_token_id = v08b.next_ids_from_state(state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)
    dag = v16b.DependencyDAG()
    rate_rows: List[Dict[str, Any]] = []
    errors: Counter[str] = Counter()
    event_counts: Counter[str] = Counter()

    for expected_id, row in enumerate(events):
        event_id = int(row["event_id"])
        errors["event_id"] += int(event_id != expected_id)
        family = row["family"]
        descriptor = tuple(ast.literal_eval(row["descriptor"]))
        rates = (
            v7.family_rates(state, params)
            if arm == "current_global"
            else adapter.family_rates(state, params)
        )
        total_rate = sum(max(0.0, float(rates[name])) for name in ("seed", "token", "birth", "death"))
        selected_family_rate = float(rates.get(family, 0.0))
        errors["nonpositive_total_rate"] += int(total_rate <= 0.0)
        errors["nonpositive_selected_family_rate"] += int(selected_family_rate <= 0.0)
        dt = float(row["dt"])
        state.t += dt
        errors["cumulative_time"] += int(abs(state.t - float(row["time"])) > 1.0e-10)

        kernel = adapter.family_kernel(state, family, params)
        descriptor_probability = float(kernel.get(descriptor, 0.0))
        errors["descriptor_support"] += int(descriptor_probability <= 0.0)
        concrete = v16b.materialize_event(family, descriptor, manager)
        errors["event_type"] += int(concrete.kind != row["event_type"])
        errors["new_node_id"] += int(
            ("" if concrete.new_node_id is None else str(concrete.new_node_id)) != row["new_node_id"]
        )
        errors["new_token_id"] += int(
            ("" if concrete.new_token_id is None else str(concrete.new_token_id)) != row["new_token_id"]
        )
        reads, writes = v16a.action_access(state, concrete)
        errors["read_resources"] += int(tuple(sorted(reads)) != split_resources(row["read_resources"]))
        errors["write_resources"] += int(tuple(sorted(writes)) != split_resources(row["write_resources"]))
        dag.add(reads, writes)
        expected_predecessors = tuple(sorted(dag.predecessors[event_id]))
        observed_predecessors = tuple(int(value) for value in split_resources(row["direct_predecessors"]))
        errors["direct_predecessors"] += int(expected_predecessors != observed_predecessors)
        pre_event_nodes = state.g.num_nodes()
        pre_event_tokens = state.token_count()
        context = adapter.apply_descriptor(state, family, descriptor, params, manager)
        errors["apply_event_type"] += int(str(context.get("event", "unknown")) != row["event_type"])
        event_counts[row["event_type"]] += 1
        concrete_hazard = selected_family_rate * descriptor_probability
        errors["nonpositive_concrete_hazard"] += int(concrete_hazard <= 0.0)
        rate_rows.append({
            **prefix,
            "event_id": event_id,
            "step": int(row["step"]),
            "family": family,
            "event_type": row["event_type"],
            "dt": dt,
            "time": float(row["time"]),
            "pre_event_nodes": pre_event_nodes,
            "pre_event_tokens": pre_event_tokens,
            "total_rate": total_rate,
            "selected_family_rate": selected_family_rate,
            "selected_family_rate_fraction": selected_family_rate / total_rate if total_rate else 0.0,
            "descriptor_probability": descriptor_probability,
            "concrete_descriptor_hazard": concrete_hazard,
            "normalized_waiting_residual": dt * total_rate,
        })

    analysis = dag.analyze()
    for row in events:
        event_id = int(row["event_id"])
        errors["causal_depth"] += int(int(row["causal_depth"]) != int(analysis["depths"][event_id]))
    errors["final_nodes"] += int(state.g.num_nodes() != int(source_summary["final_nodes"]))
    errors["final_tokens"] += int(state.token_count() != int(source_summary["final_tokens"]))
    errors["final_time"] += int(abs(state.t - float(source_summary["total_time"])) > 1.0e-10)
    errors["event_count"] += int(len(events) != int(source_summary["n_events"]))
    for event_type in v16b.EVENT_TYPES:
        errors[f"{event_type}_count"] += int(event_counts[event_type] != int(source_summary[f"{event_type}_events"]))
    nonzero_errors = {name: count for name, count in errors.items() if count}
    residuals = [float(row["normalized_waiting_residual"]) for row in rate_rows]
    audit = {
        **prefix,
        "source_events": len(events),
        "reconstructed_events": len(rate_rows),
        "error_categories": len(nonzero_errors),
        "total_errors": sum(nonzero_errors.values()),
        "error_detail": json.dumps(nonzero_errors, sort_keys=True, separators=(",", ":")),
        "residual_mean": mean(residuals),
        "residual_sd": sample_sd(residuals),
        "min_total_rate": min(float(row["total_rate"]) for row in rate_rows),
        "max_total_rate": max(float(row["total_rate"]) for row in rate_rows),
        "min_concrete_hazard": min(float(row["concrete_descriptor_hazard"]) for row in rate_rows),
        "max_concrete_hazard": max(float(row["concrete_descriptor_hazard"]) for row in rate_rows),
        "reconstruction_pass": int(not nonzero_errors),
    }
    return rate_rows, audit


def depth_assignments(
    membership_rows: Sequence[Mapping[str, str]],
    event_count: int,
) -> List[int]:
    selected = [row for row in membership_rows if int(row["scale_window"]) == DEPTH_WINDOW]
    return v16f.assignments_from_membership(selected, event_count, "coarse_event_id")


def hazard_strata(rate_rows: Sequence[Mapping[str, Any]]) -> List[str]:
    labels = ["" for _ in rate_rows]
    by_family: Dict[str, List[int]] = defaultdict(list)
    for index, row in enumerate(rate_rows):
        by_family[str(row["family"])].append(index)
    for family, indices in by_family.items():
        bin_count = min(4, max(1, len(indices) // 8))
        ordered = sorted(indices, key=lambda index: (float(rate_rows[index]["concrete_descriptor_hazard"]), index))
        for rank, index in enumerate(ordered):
            quantile = min(bin_count - 1, rank * bin_count // len(ordered))
            labels[index] = f"{family}:q{quantile}of{bin_count}"
    if any(not label for label in labels):
        raise AssertionError("hazard stratum assignment incomplete")
    return labels


def permute_within_groups(
    values: Sequence[float],
    groups: Sequence[str],
    seed: int,
) -> Tuple[List[float], float]:
    if len(values) != len(groups):
        raise ValueError("value/group length mismatch")
    result = list(values)
    indices_by_group: Dict[str, List[int]] = defaultdict(list)
    for index, group in enumerate(groups):
        indices_by_group[group].append(index)
    rng = random.Random(seed)
    for indices in indices_by_group.values():
        shuffled = [values[index] for index in indices]
        rng.shuffle(shuffled)
        for index, value in zip(indices, shuffled):
            result[index] = value
    changed = mean(left != right for left, right in zip(values, result)) if values else 0.0
    return result, changed


def conditional_dts(
    rate_rows: Sequence[Mapping[str, Any]],
    null_family: str,
    seed: int,
) -> Tuple[List[float], float]:
    dts = [float(row["dt"]) for row in rate_rows]
    if null_family == "shuffled_waiting_time":
        shuffled = list(dts)
        random.Random(seed).shuffle(shuffled)
        return shuffled, mean(left != right for left, right in zip(dts, shuffled))
    residuals = [float(row["normalized_waiting_residual"]) for row in rate_rows]
    total_rates = [float(row["total_rate"]) for row in rate_rows]
    if null_family == "total_rate_profile":
        groups = ["all"] * len(rate_rows)
    elif null_family == "event_family_rate_profile":
        groups = [str(row["family"]) for row in rate_rows]
    elif null_family == "family_descriptor_hazard_profile":
        groups = hazard_strata(rate_rows)
    else:
        raise ValueError(f"unknown null family {null_family}")
    shuffled_residuals, changed = permute_within_groups(residuals, groups, seed)
    return [residual / rate for residual, rate in zip(shuffled_residuals, total_rates)], changed


def empirical_lower_tail_p(observed: float, null_values: Sequence[float]) -> float:
    return (1.0 + sum(value <= observed for value in null_values)) / (len(null_values) + 1.0)


def mechanism_products(
    rate_rows: Sequence[Mapping[str, Any]],
    depth: Sequence[int],
    prefix: Mapping[str, Any],
    null_replicates: int,
    seed_tag: str,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    dts = [float(row["dt"]) for row in rate_rows]
    bin_count = int(prefix["clock_bins"])
    observed_clock = v16e.normalized_clock_bins(dts, bin_count)
    observed_nmi = v16f.partition_information(observed_clock, depth)["normalized_mutual_information"]
    values_by_family: Dict[str, List[float]] = defaultdict(list)
    null_rows: List[Dict[str, Any]] = []
    seed_parts = tuple(prefix[field] for field in ("stage", "growth_seed", "run_offset", "arm", "run_seed", "clock_bins"))
    for null_family in NULL_FAMILIES:
        for null_index in range(null_replicates):
            null_seed = stable_seed(seed_tag, null_family, *seed_parts, null_index)
            null_dts, changed_fraction = conditional_dts(rate_rows, null_family, null_seed)
            assignments = v16e.normalized_clock_bins(null_dts, bin_count)
            nmi = v16f.partition_information(assignments, depth)["normalized_mutual_information"]
            values_by_family[null_family].append(nmi)
            null_rows.append({
                **prefix,
                "null_family": null_family,
                "null_index": null_index,
                "null_seed": null_seed,
                "normalized_mutual_information": nmi,
                "occupied_clock_bins": len(set(assignments)),
                "permuted_value_fraction": changed_fraction,
            })
    waiting_mean = mean(values_by_family["shuffled_waiting_time"])
    base_gap = waiting_mean - observed_nmi
    summary: Dict[str, Any] = {
        **prefix,
        "event_count": len(rate_rows),
        "depth_components": len(set(depth)),
        "observed_nmi": observed_nmi,
        "waiting_null_mean_nmi": waiting_mean,
        "waiting_minus_observed_nmi": base_gap,
    }
    for null_family in NULL_FAMILIES[1:]:
        values = values_by_family[null_family]
        family_mean = mean(values)
        family_sd = sample_sd(values)
        stem = {
            "total_rate_profile": "rate",
            "event_family_rate_profile": "family_rate",
            "family_descriptor_hazard_profile": "family_hazard",
        }[null_family]
        summary[f"{stem}_null_mean_nmi"] = family_mean
        summary[f"{stem}_null_sd_nmi"] = family_sd
        summary[f"observed_minus_{stem}_null"] = observed_nmi - family_mean
        summary[f"{stem}_conditional_z"] = (observed_nmi - family_mean) / family_sd if family_sd else 0.0
        summary[f"{stem}_lower_tail_p"] = empirical_lower_tail_p(observed_nmi, values)
        summary[f"{stem}_explained_fraction"] = (
            (waiting_mean - family_mean) / base_gap if abs(base_gap) > TOLERANCE else 0.0
        )
    return summary, null_rows


def reconstruct_stage(stage: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[Tuple[str, ...], List[Dict[str, str]]]]:
    spec = STAGES[stage]
    prereg = read_csv(spec["prereg"])
    expected_events = expected_event_count(prereg)
    local_rates = {float(row["frozen_local_rate"]) for row in prereg}
    if len(local_rates) != 1:
        raise ValueError(f"{stage} preregistration does not freeze one local rate")
    local_rate = local_rates.pop()
    events_by_run = group_rows(read_csv(spec["event_log"]))
    summaries_by_run = group_rows(read_csv(spec["run_summary"]))
    memberships_by_run = group_rows(read_csv(spec["membership"]))
    expected_keys = {run_key(row) for row in prereg}
    if set(events_by_run) != expected_keys or set(summaries_by_run) != expected_keys or set(memberships_by_run) != expected_keys:
        raise ValueError(f"{stage} source run keys do not match preregistration")
    ensembles = v15.deep_ensembles([int(spec["target_nodes"])])
    growth_seeds = sorted({int(row["growth_seed"]) for row in prereg})
    bases, _ = v10e.build_bases(ensembles, v10e.recommended_regime("fast_balanced"), growth_seeds)
    ensemble_name = ensembles[0].name
    all_rates: List[Dict[str, Any]] = []
    audits: List[Dict[str, Any]] = []
    rates_by_run: Dict[Tuple[str, ...], List[Dict[str, str]]] = {}
    for index, prereg_row in enumerate(prereg, start=1):
        key = run_key(prereg_row)
        rates, audit = reconstruct_run_rates(
            bases[(ensemble_name, int(prereg_row["growth_seed"]))],
            events_by_run[key],
            summary_for_key(summaries_by_run, key),
            local_rate,
            stage,
        )
        if len(rates) != expected_events or not int(audit["reconstruction_pass"]):
            raise RuntimeError(f"{stage} rate reconstruction failed for {key}: {audit}")
        all_rates.extend(rates)
        audits.append(audit)
        rates_by_run[key] = [dict(row) for row in rates]
        print(f"[v16g] reconstruct stage={stage} run={index}/{len(prereg)} arm={prereg_row['arm']}")
    return all_rates, audits, memberships_by_run


def design_audit() -> None:
    all_audits: List[Dict[str, Any]] = []
    all_runs: List[Dict[str, Any]] = []
    all_nulls: List[Dict[str, Any]] = []
    for stage in ("v16c", "v16d"):
        rate_rows, audits, memberships_by_run = reconstruct_stage(stage)
        all_audits.extend(audits)
        rates_by_run = group_rows(rate_rows)
        for index, (key, rate_rows) in enumerate(sorted(rates_by_run.items()), start=1):
            depth = depth_assignments(memberships_by_run[key], len(rate_rows))
            for clock_bins in SELECTED_CLOCK_BINS:
                prefix = {
                    "stage": stage,
                    **numeric_prefix(key),
                    "depth_window": DEPTH_WINDOW,
                    "clock_bins": clock_bins,
                }
                summary, nulls = mechanism_products(
                    rate_rows, depth, prefix, CALIBRATION_NULL_REPLICATES, "v16g-design-calibration"
                )
                all_runs.append(summary)
                all_nulls.extend(nulls)
            print(f"[v16g] calibrate stage={stage} run={index}/{len(rates_by_run)}")
    write_csv(CALIBRATION_AUDIT, all_audits)
    write_csv(CALIBRATION_RUNS, all_runs)
    write_csv(CALIBRATION_NULLS, all_nulls)
    print(f"[v16g] design audit rows={len(all_runs)} nulls={len(all_nulls)}")


def selection_rows(calibration_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for stage in ("v16c", "v16d"):
        for clock_bins in SELECTED_CLOCK_BINS:
            selected = [
                row for row in calibration_rows
                if row["stage"] == stage and row["arm"] == PRIMARY_ARM and int(row["clock_bins"]) == clock_bins
            ]
            stem = primary_stem()
            explained = [float(row[f"{stem}_explained_fraction"]) for row in selected]
            z_values = [float(row[f"{stem}_conditional_z"]) for row in selected]
            p_values = [float(row[f"{stem}_lower_tail_p"]) for row in selected]
            base_gaps = [float(row["waiting_minus_observed_nmi"]) for row in selected]
            nonsurprising = [
                abs(z_value) <= MAX_ABS_CONDITIONAL_Z and p_value >= MIN_EMPIRICAL_LOWER_TAIL_P
                for z_value, p_value in zip(z_values, p_values)
            ]
            rows.append({
                "stage": stage,
                "clock_bins": clock_bins,
                "primary_arm": PRIMARY_ARM,
                "primary_null_family": PRIMARY_NULL_FAMILY,
                "n_runs": len(selected),
                "median_waiting_minus_observed_nmi": median(base_gaps),
                "negative_relation_fraction": mean(value > 0.0 for value in base_gaps),
                "median_rate_explained_fraction": median(float(row["rate_explained_fraction"]) for row in selected),
                "median_family_rate_explained_fraction": median(float(row["family_rate_explained_fraction"]) for row in selected),
                "median_family_hazard_explained_fraction": median(
                    float(row["family_hazard_explained_fraction"]) for row in selected
                ),
                "median_primary_explained_fraction": median(explained),
                "median_family_rate_increment_over_rate": median(
                    float(row["family_rate_explained_fraction"]) - float(row["rate_explained_fraction"])
                    for row in selected
                ),
                "median_family_hazard_increment_over_rate": median(
                    float(row["family_hazard_explained_fraction"]) - float(row["rate_explained_fraction"])
                    for row in selected
                ),
                "conditionally_nonsurprising_fraction": mean(nonsurprising),
                "min_median_explained_fraction": MIN_MEDIAN_EXPLAINED_FRACTION,
                "min_conditionally_nonsurprising_fraction": MIN_CONDITIONALLY_NONSURPRISING_FRACTION,
                "calibration_supports_primary_mechanism": int(
                    len(selected) == 6
                    and median(base_gaps) > 0.0
                    and median(explained) >= MIN_MEDIAN_EXPLAINED_FRACTION
                    and mean(nonsurprising) >= MIN_CONDITIONALLY_NONSURPRISING_FRACTION
                ),
            })
    return rows


def frozen_spec() -> Dict[str, Any]:
    return {
        "gate": "v16g_clock_depth_boundary_mechanism",
        "analysis_holdout": "existing_v16e_histories_not_used_for_design_calibration",
        "design_stages": ["v16c", "v16d"],
        "holdout_stage": "v16e",
        "depth_window": DEPTH_WINDOW,
        "clock_bins": list(SELECTED_CLOCK_BINS),
        "null_families": list(NULL_FAMILIES),
        "primary_null_family": PRIMARY_NULL_FAMILY,
        "residual_definition": "dt_times_pre_event_total_rate",
        "hazard_definition": "selected_family_rate_times_descriptor_probability",
        "hazard_strata": "within_family_rank_quantiles_up_to_4_with_at_least_8_events_per_bin",
        "calibration_null_replicates": CALIBRATION_NULL_REPLICATES,
        "holdout_null_replicates": HOLDOUT_NULL_REPLICATES,
        "primary_arm": PRIMARY_ARM,
        "min_median_explained_fraction": MIN_MEDIAN_EXPLAINED_FRACTION,
        "min_conditionally_nonsurprising_fraction": MIN_CONDITIONALLY_NONSURPRISING_FRACTION,
        "max_abs_conditional_z": MAX_ABS_CONDITIONAL_Z,
        "min_empirical_lower_tail_p": MIN_EMPIRICAL_LOWER_TAIL_P,
        "result_scope": "finite_frozen_histories_scheduler_mechanism_only",
    }


def spec_digest() -> str:
    payload = json.dumps(frozen_spec(), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def freeze_design() -> None:
    calibration_rows = read_csv(CALIBRATION_RUNS)
    audits = read_csv(CALIBRATION_AUDIT)
    nulls = read_csv(CALIBRATION_NULLS)
    if len(calibration_rows) != 72 or len(audits) != 24 or len(nulls) != 72 * CALIBRATION_NULL_REPLICATES * len(NULL_FAMILIES):
        raise ValueError("v16g calibration artifact coverage is incomplete")
    if not all(int(row["reconstruction_pass"]) for row in audits):
        raise ValueError("v16g calibration rate reconstruction failed")
    rows = selection_rows(calibration_rows)
    digest = spec_digest()
    for row in rows:
        row["spec_digest"] = digest
        row["calibration_runs_sha256"] = file_sha256(CALIBRATION_RUNS)
        row["calibration_nulls_sha256"] = file_sha256(CALIBRATION_NULLS)
        row["prepared_before_v16e_mechanism_computation"] = 1
    write_csv(DESIGN_SELECTION, rows)
    print(
        f"[v16g] design frozen digest={digest} supported="
        f"{sum(int(row['calibration_supports_primary_mechanism']) for row in rows)}/{len(rows)}"
    )


def source_contract_rows() -> Tuple[List[Dict[str, Any]], bool]:
    gates = read_csv(DOC / "v16f_gate_evaluation.csv")
    overall = [row for row in gates if row["gate"] == "v16f_overall"]
    expected = "pass_to_v16g_clock_depth_boundary_mechanism_gate"
    passed = len(overall) == 1 and overall[0]["status"] == expected
    rows = [{
        "source": "v16f_cross_map_relation_gate",
        "artifact": "v16f_gate_evaluation.csv",
        "sha256": file_sha256(DOC / "v16f_gate_evaluation.csv"),
        "observed_status": overall[0]["status"] if len(overall) == 1 else "invalid",
        "required_status": expected,
        "source_pass": int(passed),
    }]
    return rows, passed


def preregistration_rows() -> List[Dict[str, Any]]:
    source_rows, source_pass = source_contract_rows()
    if not source_pass:
        raise ValueError(f"v16f source contract failed: {source_rows}")
    selection = read_csv(DESIGN_SELECTION)
    if len(selection) != 6 or {row["spec_digest"] for row in selection} != {spec_digest()}:
        raise ValueError("v16g design selection is missing or stale")
    assignments = read_csv(STAGES["v16e"]["prereg"])
    selection_hash = file_sha256(DESIGN_SELECTION)
    rows: List[Dict[str, Any]] = []
    for assignment in assignments:
        rows.append({
            "purpose_ref": assignment.get("purpose_ref", "purpose://prompt.unknown"),
            "spec_digest": spec_digest(),
            "source_event_log_sha256": file_sha256(STAGES["v16e"]["event_log"]),
            "source_depth_membership_sha256": file_sha256(STAGES["v16e"]["membership"]),
            "source_run_summary_sha256": file_sha256(STAGES["v16e"]["run_summary"]),
            "design_selection_sha256": selection_hash,
            "target_nodes": int(assignment["target_nodes"]),
            "growth_seed": int(assignment["growth_seed"]),
            "run_offset": int(assignment["run_offset"]),
            "arm": assignment["arm"],
            "run_seed": int(assignment["run_seed"]),
            "steps": int(assignment["steps"]),
            "depth_window": DEPTH_WINDOW,
            "clock_bins": ";".join(str(value) for value in SELECTED_CLOCK_BINS),
            "null_replicates_per_family": HOLDOUT_NULL_REPLICATES,
            "primary_null_family": PRIMARY_NULL_FAMILY,
            "min_median_explained_fraction": MIN_MEDIAN_EXPLAINED_FRACTION,
            "min_conditionally_nonsurprising_fraction": MIN_CONDITIONALLY_NONSURPRISING_FRACTION,
            "prepared_before_v16e_mechanism_computation": 1,
        })
    return rows


def prepare() -> None:
    rows = preregistration_rows()
    write_csv(PREREG, rows)
    print(f"[v16g] prepared rows={len(rows)} digest={rows[0]['spec_digest']}")


def load_and_verify_preregistration() -> List[Dict[str, str]]:
    if not PREREG.exists():
        raise ValueError("missing v16g preregistration; run --prepare-only first")
    observed = read_csv(PREREG)
    expected = preregistration_rows()
    if observed != [{key: str(value) for key, value in row.items()} for row in expected]:
        raise ValueError("v16g preregistration changed")
    return observed


def primary_stem() -> str:
    return {
        "total_rate_profile": "rate",
        "event_family_rate_profile": "family_rate",
        "family_descriptor_hazard_profile": "family_hazard",
    }[PRIMARY_NULL_FAMILY]


def local_mechanism_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    stem = primary_stem()
    for clock_bins in SELECTED_CLOCK_BINS:
        selected = [row for row in run_rows if row["arm"] == PRIMARY_ARM and int(row["clock_bins"]) == clock_bins]
        explained = [float(row[f"{stem}_explained_fraction"]) for row in selected]
        base_gaps = [float(row["waiting_minus_observed_nmi"]) for row in selected]
        nonsurprising = [
            abs(float(row[f"{stem}_conditional_z"])) <= MAX_ABS_CONDITIONAL_Z
            and float(row[f"{stem}_lower_tail_p"]) >= MIN_EMPIRICAL_LOWER_TAIL_P
            for row in selected
        ]
        rows.append({
            "clock_bins": clock_bins,
            "primary_arm": PRIMARY_ARM,
            "n_runs": len(selected),
            "median_waiting_minus_observed_nmi": median(base_gaps),
            "negative_relation_fraction": mean(value > 0.0 for value in base_gaps),
            "median_rate_explained_fraction": median(float(row["rate_explained_fraction"]) for row in selected),
            "median_family_rate_explained_fraction": median(float(row["family_rate_explained_fraction"]) for row in selected),
            "median_family_hazard_explained_fraction": median(float(row["family_hazard_explained_fraction"]) for row in selected),
            "median_primary_explained_fraction": median(explained),
            "median_family_rate_increment_over_rate": median(
                float(row["family_rate_explained_fraction"]) - float(row["rate_explained_fraction"])
                for row in selected
            ),
            "median_family_hazard_increment_over_rate": median(
                float(row["family_hazard_explained_fraction"]) - float(row["rate_explained_fraction"])
                for row in selected
            ),
            "conditionally_nonsurprising_fraction": mean(nonsurprising),
            "local_mechanism_pass": int(
                len(selected) == 6
                and median(base_gaps) > 0.0
                and median(explained) >= MIN_MEDIAN_EXPLAINED_FRACTION
                and mean(nonsurprising) >= MIN_CONDITIONALLY_NONSURPRISING_FRACTION
            ),
        })
    return rows


def grouped_mechanism_rows(
    run_rows: Sequence[Mapping[str, Any]],
    field: str,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    stem = primary_stem()
    values = sorted({str(row[field]) for row in run_rows})
    for clock_bins in SELECTED_CLOCK_BINS:
        for value in values:
            selected = [row for row in run_rows if str(row[field]) == value and int(row["clock_bins"]) == clock_bins]
            explained = [float(row[f"{stem}_explained_fraction"]) for row in selected]
            nonsurprising = [
                abs(float(row[f"{stem}_conditional_z"])) <= MAX_ABS_CONDITIONAL_Z
                and float(row[f"{stem}_lower_tail_p"]) >= MIN_EMPIRICAL_LOWER_TAIL_P
                for row in selected
            ]
            rows.append({
                "group_field": field,
                "group_value": value,
                "clock_bins": clock_bins,
                "n_runs": len(selected),
                "median_primary_explained_fraction": median(explained),
                "conditionally_nonsurprising_fraction": mean(nonsurprising),
                "group_mechanism_pass": int(
                    median(explained) >= MIN_MEDIAN_EXPLAINED_FRACTION
                    and mean(nonsurprising) >= 0.50
                ),
            })
    return rows


def gate_evaluation(
    audits: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], str]:
    reconstruction_pass = len(audits) == 12 and all(int(row["reconstruction_pass"]) for row in audits)
    relation_reproduced = all(float(row["waiting_minus_observed_nmi"]) > 0.0 for row in run_rows)
    local_pass = len(local_rows) == 3 and all(int(row["local_mechanism_pass"]) for row in local_rows)
    growth_pass = len(growth_rows) == 6 and all(int(row["group_mechanism_pass"]) for row in growth_rows)
    scheduler_pass = len(scheduler_rows) == 6 and all(int(row["group_mechanism_pass"]) for row in scheduler_rows)
    if not reconstruction_pass:
        overall = "v16g_instrumentation_failed"
    elif not relation_reproduced:
        overall = "v16f_relation_not_reproduced_stop_mechanism_claim"
    elif local_pass and growth_pass and scheduler_pass:
        overall = "pass_to_v16h_fresh_rate_logged_mechanism_holdout"
    else:
        overall = "rate_family_mechanism_not_supported_stop_cross_map_synthesis"
    rows = [
        {"gate": "exact_rate_reconstruction", "status": "pass" if reconstruction_pass else "fail", "observed": f"audits={len(audits)};failures={sum(not int(row['reconstruction_pass']) for row in audits)}", "required": "12 audits;failures=0", "decision": "continue" if reconstruction_pass else "repair_instrumentation"},
        {"gate": "v16f_relation_reproduction", "status": "pass" if relation_reproduced else "fail", "observed": f"positive_waiting_minus_observed={sum(float(row['waiting_minus_observed_nmi']) > 0.0 for row in run_rows)}/{len(run_rows)}", "required": f"{len(run_rows)}/{len(run_rows)}", "decision": "continue" if relation_reproduced else "stop_mechanism_claim"},
        {"gate": "total_rate_profile_mechanism", "status": "pass" if local_pass else "fail", "observed": f"passing_bins={sum(int(row['local_mechanism_pass']) for row in local_rows)}/{len(local_rows)}", "required": "3/3", "decision": "fresh_holdout" if local_pass else "stop_cross_map_synthesis"},
        {"gate": "growth_transfer", "status": "pass" if growth_pass else "fail", "observed": f"passing_groups={sum(int(row['group_mechanism_pass']) for row in growth_rows)}/{len(growth_rows)}", "required": "6/6", "decision": "continue" if growth_pass else "do_not_generalize"},
        {"gate": "scheduler_transfer", "status": "pass" if scheduler_pass else "fail", "observed": f"passing_groups={sum(int(row['group_mechanism_pass']) for row in scheduler_rows)}/{len(scheduler_rows)}", "required": "6/6", "decision": "continue" if scheduler_pass else "scheduler_sensitive"},
        {"gate": "v16g_overall", "status": overall, "observed": f"reconstruction={int(reconstruction_pass)};relation={int(relation_reproduced)};local={int(local_pass)};growth={int(growth_pass)};scheduler={int(scheduler_pass)}", "required": "all five gates pass for fresh rate-logged holdout", "decision": overall},
    ]
    return rows, overall


def claim_rows(overall: str) -> List[Dict[str, Any]]:
    mechanism_supported = overall == "pass_to_v16h_fresh_rate_logged_mechanism_holdout"
    return [
        {"claim_id": "C1", "claim": "Pre-event total rates, selected family rates, and concrete descriptor hazards are exactly reconstructable for all frozen v16e events.", "status": "supported", "evidence": "v16g_rate_reconstruction_audit.csv", "scope_limit": "declared simulator and frozen v16e event histories"},
        {"claim_id": "C2", "claim": "Pre-event total-rate conditioning explains a material share of the v16f clock/depth anti-alignment.", "status": "supported" if mechanism_supported else "unsupported", "evidence": "v16g_local_mechanism_gate.csv;v16g_mechanism_run_summary.csv", "scope_limit": "finite analysis holdout; mechanism requires a fresh dynamical holdout"},
        {"claim_id": "C3", "claim": "Event-family and concrete descriptor-hazard conditioning add a material explanation beyond the total-rate profile.", "status": "unsupported", "evidence": "v16g_local_mechanism_gate.csv;v16g_mechanism_run_summary.csv", "scope_limit": "secondary median increments are near zero; not a separately gated mechanism"},
        {"claim_id": "C4", "claim": "The clock/depth relation is an independent common emergent geometry after scheduler conditioning.", "status": "unsupported", "evidence": "none", "scope_limit": "v16g tests a scheduler mechanism, not geometric equivalence"},
        {"claim_id": "C5", "claim": "The simulation clock is physical proper time or supports Lorentz symmetry or spacetime.", "status": "unsupported", "evidence": "none", "scope_limit": "no observer transformations, metric, light cones, or continuum limit are tested"},
        {"claim_id": "C6", "claim": "The result establishes particles, entanglement, or universal causal laws.", "status": "unsupported", "evidence": "none", "scope_limit": "not tested"},
    ]


def execution_audit_rows() -> List[Dict[str, Any]]:
    return [{
        "event": "pre_holdout_group_diagnostic_threshold_serialization_omission",
        "observed": "growth_scheduler_group_nonsurprising_threshold_0.50_was_literal_in_frozen_code_but_absent_from_spec_digest_payload",
        "change": "documented_only_no_threshold_data_statistic_seed_or_result_change",
        "primary_gate_affected": 0,
        "secondary_transfer_gate_affected": 1,
        "design_changed": 0,
        "source_data_changed": 0,
        "holdout_recomputed_after_change": 0,
        "interpretation": "primary_local_mechanism_is_digest_locked;growth_and_scheduler_transfer_have_weaker_manifest_audit",
    }]


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
    audits: Sequence[Mapping[str, Any]],
    local_rows: Sequence[Mapping[str, Any]],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    design_rows = read_csv(DESIGN_SELECTION)
    execution_rows = execution_audit_rows()
    primary_explained = [float(row["median_rate_explained_fraction"]) for row in local_rows]
    family_increment = [float(row["median_family_rate_increment_over_rate"]) for row in local_rows]
    hazard_increment = [float(row["median_family_hazard_increment_over_rate"]) for row in local_rows]
    lines = [
        "# v16g clock-depth boundary mechanism gate",
        "",
        f"Status: `{overall}`.",
        "",
        "## Question and evidential role",
        "",
        "v16g asks whether the stable v16f clock/depth anti-alignment is produced by the simulator's pre-event scheduler-rate profile and event-family/local descriptor hazards. It is a frozen-data analysis holdout on v16e, not a fresh dynamical holdout.",
        "",
        "## Design discipline",
        "",
        "Only v16c/v16d were used for mechanism design. Their parsimonious total-rate-profile null already explained approximately the full old-data gap, while family and descriptor-hazard conditioning added little. Total rate was therefore frozen as primary before the v16e mechanism values were computed; richer conditioning remained secondary. The preregistration locks source hashes, assignments, null families, seeds, statistics, directions, and thresholds.",
        "",
    ]
    lines.extend(table(design_rows, ("stage", "clock_bins", "primary_null_family", "median_rate_explained_fraction", "median_family_rate_increment_over_rate", "median_family_hazard_increment_over_rate", "conditionally_nonsurprising_fraction", "calibration_supports_primary_mechanism")))
    lines.extend([
        "",
        f"Frozen specification digest: `{spec_digest()}`.",
        "",
        "## Exact reconstruction",
        "",
        "Rates are reconstructed before each stored event. The normalized residual is `dt * total_rate`; the concrete descriptor hazard is `selected_family_rate * descriptor_probability`. Every replay must reproduce descriptor support, event kind, allocated IDs, resources, direct dependency predecessors, causal depth, event counts, final census, and total simulation time.",
        "",
        "## Conditional nulls",
        "",
        "- `shuffled_waiting_time` destroys the eventwise waiting-time/rate pairing and is the v16f-style baseline.",
        "- `total_rate_profile` shuffles unit-rate residuals globally and reconstructs each waiting time using its original pre-event total rate.",
        "- `event_family_rate_profile` shuffles residuals only within event family.",
        "- `family_descriptor_hazard_profile` additionally restricts shuffling to within-family rank-quantiles of concrete descriptor hazard.",
        "",
        "The preregistered primary is `total_rate_profile`; family and descriptor-hazard conditioning are secondary incremental diagnostics. An explained fraction of `1` means the conditional-null mean reaches the observed NMI from the unconditional waiting-time-null mean. It does not mean that a physical law has been derived.",
        "",
        "## Reconstruction audit",
        "",
    ])
    lines.extend(table(audits, ("growth_seed", "run_offset", "arm", "source_events", "total_errors", "residual_mean", "reconstruction_pass")))
    lines.extend(["", "## Primary local result", ""])
    lines.extend(table(local_rows, ("clock_bins", "n_runs", "median_waiting_minus_observed_nmi", "median_rate_explained_fraction", "median_family_rate_increment_over_rate", "median_family_hazard_increment_over_rate", "conditionally_nonsurprising_fraction", "local_mechanism_pass")))
    lines.extend([
        "",
        f"Across the three primary resolutions, the total-rate profile explains median fractions `{min(primary_explained):.6f}` to `{max(primary_explained):.6f}` of the unconditional clock/depth gap. The median event-family increment ranges from `{min(family_increment):.6f}` to `{max(family_increment):.6f}` and the descriptor-hazard increment from `{min(hazard_increment):.6f}` to `{max(hazard_increment):.6f}`. The parsimonious result is therefore a total scheduler-rate mechanism; no separate family or concrete-hazard mechanism is supported by these secondary medians.",
    ])
    lines.extend(["", "## Growth and scheduler diagnostics", ""])
    lines.extend(table(growth_rows, ("group_field", "group_value", "clock_bins", "median_primary_explained_fraction", "conditionally_nonsurprising_fraction", "group_mechanism_pass")))
    lines.append("")
    lines.extend(table(scheduler_rows, ("group_field", "group_value", "clock_bins", "median_primary_explained_fraction", "conditionally_nonsurprising_fraction", "group_mechanism_pass")))
    lines.extend(["", "## Gate evaluation", ""])
    lines.extend(table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend(["", "## Execution audit", ""])
    lines.extend(table(execution_rows, ("event", "change", "primary_gate_affected", "secondary_transfer_gate_affected", "design_changed", "source_data_changed")))
    lines.extend([
        "",
        "The `0.50` conditional-nonsurprise threshold used by the growth/scheduler diagnostics was present in the frozen code before holdout execution but omitted from the serialized spec-digest payload. No threshold, data, statistic, seed, or result was changed after opening v16e. The primary local gate is digest-locked; growth/scheduler transfer therefore has weaker manifest evidence and remains supportive rather than independently decisive.",
    ])
    lines.extend([
        "",
        "## Interpretation limits",
        "",
        "A pass identifies a finite simulator mechanism capable of accounting for the relative partition statistic and justifies one fresh rate-logged holdout. It weakens, rather than strengthens, any claim that the two maps are independent coordinates of one geometry: the cross-map relation is currently best understood as scheduler-rate-induced. A failure means the tested scheduler/rate mechanism is insufficient; it does not turn the maps into physical spacetime.",
        "",
        "No result here establishes Lorentz symmetry, proper time, a spacetime metric, a continuum limit, particles, entanglement, or universal causal laws.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    prereg = load_and_verify_preregistration()
    source_rows, source_pass = source_contract_rows()
    if not source_pass:
        raise RuntimeError("v16f source contract no longer passes")
    rate_rows, audits, memberships_by_run = reconstruct_stage("v16e")
    rates_by_run = group_rows(rate_rows)
    run_rows: List[Dict[str, Any]] = []
    null_rows: List[Dict[str, Any]] = []
    for index, prereg_row in enumerate(prereg, start=1):
        key = run_key(prereg_row)
        run_rates = rates_by_run[key]
        depth = depth_assignments(memberships_by_run[key], len(run_rates))
        for clock_bins in SELECTED_CLOCK_BINS:
            prefix = {
                "stage": "v16e_analysis_holdout",
                **numeric_prefix(key),
                "depth_window": DEPTH_WINDOW,
                "clock_bins": clock_bins,
            }
            summary, nulls = mechanism_products(
                run_rates, depth, prefix, HOLDOUT_NULL_REPLICATES, "v16g-analysis-holdout"
            )
            run_rows.append(summary)
            null_rows.extend(nulls)
        print(f"[v16g] mechanism run={index}/{len(prereg)} arm={prereg_row['arm']}")
    local_rows = local_mechanism_rows(run_rows)
    growth_rows = grouped_mechanism_rows(run_rows, "growth_seed")
    scheduler_rows = grouped_mechanism_rows(run_rows, "arm")
    gates, overall = gate_evaluation(audits, run_rows, local_rows, growth_rows, scheduler_rows)
    write_csv(DOC / "v16g_source_chain.csv", source_rows)
    write_csv(DOC / "v16g_rate_reconstruction_event_log.csv", rate_rows)
    write_csv(DOC / "v16g_rate_reconstruction_audit.csv", audits)
    write_csv(DOC / "v16g_mechanism_run_summary.csv", run_rows)
    write_csv(DOC / "v16g_conditional_null_distribution.csv", null_rows)
    write_csv(DOC / "v16g_local_mechanism_gate.csv", local_rows)
    write_csv(DOC / "v16g_growth_mechanism_transfer.csv", growth_rows)
    write_csv(DOC / "v16g_scheduler_mechanism_transfer.csv", scheduler_rows)
    write_csv(DOC / "v16g_gate_evaluation.csv", gates)
    write_csv(DOC / "v16g_execution_audit.csv", execution_audit_rows())
    write_csv(DOC / "v16g_claim_ledger.csv", claim_rows(overall))
    (DOC / "v16g_clock_depth_boundary_mechanism_gate.md").write_text(
        build_report(audits, local_rows, growth_rows, scheduler_rows, gates, overall), encoding="utf-8"
    )
    recommendation = "\n".join([
        "# Operativ anbefaling v0.16g",
        "",
        f"Status: `{overall}`.",
        "",
        "- Ved full pass: kjoer ett ferskt dynamisk v16h-holdout som logger pre-event-rater direkte og bruker samme frosne residual-nulltest.",
        "- Ikke legg til et tredje kart eller oek skala foer mekanismen er testet paa ferske histories.",
        "- Behandle v16f-relasjonen som scheduler-rate-indusert inntil et ferskt direkte-logget holdout eventuelt avkrefter det; ikke som uavhengig geometri.",
        "- Ikke presenter simulation clock som proper time eller resultatet som Lorentz-, spacetime- eller continuum-evidens.",
        "",
    ])
    (DOC / "v0_16g_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    lay = "\n".join([
        "# v0.16g for ikke-spesialister",
        "",
        "Vi testet om forskjellen mellom klokke- og avhengighetskartet kan forklares av hvor raskt simulatoren tillater ulike hendelser. Vi rekonstruerte derfor den faktiske raten foer hver hendelse og sammenlignet med kontroller som beholdt rateprofilen, men flyttet den tilfeldige ventetiden. Rateprofilen forklarte omtrent hele forskjellen; mer detaljert inndeling etter hendelsestype ga nesten ingen ekstra forklaring.",
        "",
        f"Statusen er `{overall}`. Selv en full pass betyr bare at vi har funnet en sannsynlig simulatormekanisme og boer bekrefte den i en ny kjoering; det er ikke et bevis paa fysisk tid eller romtid.",
        "",
    ])
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16g.md").write_text(lay, encoding="utf-8")
    print(f"[v16g] overall={overall} events={len(rate_rows)} runs={len(run_rows)} nulls={len(null_rows)}")


def verify_outputs() -> None:
    prereg = load_and_verify_preregistration()
    rates = read_csv(DOC / "v16g_rate_reconstruction_event_log.csv")
    audits = read_csv(DOC / "v16g_rate_reconstruction_audit.csv")
    runs = read_csv(DOC / "v16g_mechanism_run_summary.csv")
    nulls = read_csv(DOC / "v16g_conditional_null_distribution.csv")
    execution = read_csv(DOC / "v16g_execution_audit.csv")
    gates = read_csv(DOC / "v16g_gate_evaluation.csv")
    assert len(prereg) == 12
    assert len(rates) == 12 * 3072
    assert len(audits) == 12 and all(int(row["reconstruction_pass"]) for row in audits)
    assert len(runs) == 12 * len(SELECTED_CLOCK_BINS)
    assert len(nulls) == len(runs) * HOLDOUT_NULL_REPLICATES * len(NULL_FAMILIES)
    assert {row["null_family"] for row in nulls} == set(NULL_FAMILIES)
    assert len(execution) == 1
    assert int(execution[0]["primary_gate_affected"]) == 0
    assert int(execution[0]["design_changed"]) == 0
    assert int(execution[0]["source_data_changed"]) == 0
    for row in runs:
        for field, value in row.items():
            if field.endswith(("_nmi", "_fraction", "_z", "_p")):
                assert math.isfinite(float(value)), (field, value)
    overall = [row for row in gates if row["gate"] == "v16g_overall"]
    assert len(overall) == 1 and overall[0]["status"] in {
        "pass_to_v16h_fresh_rate_logged_mechanism_holdout",
        "rate_family_mechanism_not_supported_stop_cross_map_synthesis",
        "v16f_relation_not_reproduced_stop_mechanism_claim",
        "v16g_instrumentation_failed",
    }
    print(f"[v16g] output verification pass events={len(rates)} runs={len(runs)} nulls={len(nulls)} overall={overall[0]['status']}")


def self_test() -> None:
    values = [0.1, 0.2, 0.3, 0.4]
    groups = ["a", "a", "b", "b"]
    shuffled, changed = permute_within_groups(values, groups, 3)
    assert sorted(shuffled[:2]) == values[:2]
    assert sorted(shuffled[2:]) == values[2:]
    assert 0.0 <= changed <= 1.0
    fake = [
        {
            "dt": 0.1 + index * 0.01,
            "total_rate": 2.0 + index,
            "family": "token",
            "concrete_descriptor_hazard": 0.01 + index,
            "normalized_waiting_residual": (0.1 + index * 0.01) * (2.0 + index),
        }
        for index in range(16)
    ]
    dts, fraction = conditional_dts(fake, "family_descriptor_hazard_profile", 7)
    assert len(dts) == len(fake) and all(value > 0.0 for value in dts)
    assert 0.0 <= fraction <= 1.0
    assert abs(empirical_lower_tail_p(0.0, [1.0, 2.0]) - 1.0 / 3.0) < TOLERANCE
    print("[v16g] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16g clock/depth boundary mechanism gate")
    parser.add_argument("--design-audit", action="store_true")
    parser.add_argument("--freeze-design", action="store_true")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    modes = sum((args.design_audit, args.freeze_design, args.prepare_only, args.self_test, args.verify_only))
    if modes > 1:
        parser.error("choose at most one mode")
    if args.self_test:
        self_test()
    elif args.design_audit:
        design_audit()
    elif args.freeze_design:
        freeze_design()
    elif args.prepare_only:
        prepare()
    elif args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
