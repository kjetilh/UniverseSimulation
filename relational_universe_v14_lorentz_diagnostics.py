#!/usr/bin/env python3
"""v0.14 Lorentz diagnostics with explicit artifact controls.

This round is intentionally narrower than the v13 geometry refinements.
It does not claim Lorentz-likeness from a single front-speed fit. Instead it
tests one operational sub-question under tight controls:

1. Does the damage front have roughly similar effective speed across different
   local perturbation types when we reuse the *same* base states and seeds?
2. Does that answer survive a nearby regime control?
3. Are the measurements still clean after checking size separation, fallback
   perturbations, and support-size differences?

The output should be read as a diagnostic, not as proof of relativistic
symmetry. Isotropy, microframe hiding, and IR dispersion are explicitly left
for later work.
"""
from __future__ import annotations

import argparse
import math
import random
import statistics
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e


ANCHOR_CANDIDATE = "band_zero_del"
CONTROL_CANDIDATE = "band_pdel_0005"
PERTURBATIONS = ("local_swap", "add_chord", "token_shift")
PRIMARY_STRUCTURAL_PAIR = ("local_swap", "add_chord")


def safe_float(x: Any, default: float = float("nan")) -> float:
    try:
        y = float(x)
    except Exception:
        return default
    if math.isnan(y) or math.isinf(y):
        return default
    return y


def mean_defined(values: Iterable[float]) -> float:
    vals = [float(v) for v in values if math.isfinite(float(v))]
    return float(statistics.mean(vals)) if vals else float("nan")


def sd_or_zero(values: Iterable[float]) -> float:
    vals = [float(v) for v in values if math.isfinite(float(v))]
    return float(statistics.pstdev(vals)) if len(vals) >= 2 else 0.0


def quantile(values: Sequence[float], q: float) -> float:
    vals = sorted(v for v in values if isinstance(v, (int, float)) and math.isfinite(v))
    if not vals:
        return float("nan")
    if q <= 0.0:
        return float(vals[0])
    if q >= 1.0:
        return float(vals[-1])
    pos = (len(vals) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return float(vals[lo])
    frac = pos - lo
    return float(vals[lo] * (1.0 - frac) + vals[hi] * frac)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v10b.write_csv(path, rows)


def perturbation_requested_match(requested: str, actual: str) -> bool:
    if requested == "local_swap":
        return actual == "local_swap_anywhere"
    if requested == "add_chord":
        return actual == "local_chord_anywhere"
    if requested == "token_shift":
        return actual == "token_shift"
    return False


def perturbation_category(actual: str) -> str:
    if actual == "local_swap_anywhere":
        return "local_swap"
    if actual == "local_chord_anywhere":
        return "add_chord"
    if actual == "token_shift":
        return "token_shift"
    return actual


def candidate_specs() -> List[Dict[str, Any]]:
    return [
        {
            "candidate": v09.ScaleCandidate(ANCHOR_CANDIDATE, 0.02, 0.00, 0.02, 0.00, 0.00),
            "candidate_role": "anchor",
        },
        {
            "candidate": v09.ScaleCandidate(CONTROL_CANDIDATE, 0.02, 0.00, 0.02, 0.00, 0.005),
            "candidate_role": "near_delete_control",
        },
    ]


def candidate_meta() -> Dict[str, Dict[str, Any]]:
    return {spec["candidate"].name: spec for spec in candidate_specs()}


def deep_ensembles(targets: Sequence[int]) -> List[v10b.CalibrationEnsemble]:
    return [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]


def steps_for_state(nodes: int) -> int:
    return v10e.steps_for_state(nodes)


def radius_drop_rate(log_rows: Sequence[Dict[str, Any]], key: str = "radius_control") -> float:
    vals = [int(row[key]) for row in log_rows if int(row[key]) >= 0]
    if len(vals) < 2:
        return 0.0
    drops = sum(1 for a, b in zip(vals, vals[1:]) if b < a)
    return float(drops / max(1, len(vals) - 1))


def max_radius(log_rows: Sequence[Dict[str, Any]], key: str = "radius_control") -> int:
    vals = [int(row[key]) for row in log_rows if int(row[key]) >= 0]
    return max(vals) if vals else -1


def first_hit_steps(log_rows: Sequence[Dict[str, Any]], key_r: str, r_max: int) -> Dict[int, Optional[int]]:
    out: Dict[int, Optional[int]] = {r: None for r in range(r_max + 1)}
    for row in log_rows:
        rad = int(row[key_r])
        if rad < 0:
            continue
        step = int(row["step"])
        for r in range(rad + 1):
            if r in out and out[r] is None:
                out[r] = step
    return out


def first_hit_times_safe(log_rows: Sequence[Dict[str, Any]], key_r: str, key_t: str, r_max: int) -> Dict[int, Optional[float]]:
    out: Dict[int, Optional[float]] = {r: None for r in range(r_max + 1)}
    for row in log_rows:
        rad = int(row[key_r])
        if rad < 0:
            continue
        t = float(row[key_t])
        for r in range(rad + 1):
            if r in out and out[r] is None:
                out[r] = t
    return out


def run_coupled_from_base_with_info(
    base_state: v7.State,
    *,
    params: v7.Params,
    seed: int,
    steps: int,
    perturbation: str,
    center_token_index: int = 0,
    local_coupling: str = "maximal",
    log_every: int = 40,
) -> Dict[str, Any]:
    rng = random.Random(seed)
    control = base_state.clone()
    perturbed = base_state.clone()

    perturbation_info = v08b.apply_custom_perturbation(
        perturbed,
        perturbation,
        center_token_index=center_token_index,
    )
    support = list(perturbation_info["support"])

    next_node_id, next_token_id = v08b.next_ids_from_state(base_state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)

    event_rows: List[Dict[str, Any]] = []
    log_rows: List[Dict[str, Any]] = []

    equal_prev = v7.states_equal(control, perturbed)
    first_meeting_step = 0 if equal_prev else None
    first_meeting_time = 0.0 if equal_prev else None
    meeting_count = 1 if equal_prev else 0
    total_unequal_time = 0.0
    unequal_start_t = 0.0 if not equal_prev else None

    for step in range(1, steps + 1):
        ev = v7.coupled_step(control, perturbed, manager, rng, params, local_coupling)
        ev["step"] = step
        ev["t"] = control.t
        event_rows.append(ev)

        equal_now = v7.states_equal(control, perturbed)
        if equal_now and not equal_prev:
            if first_meeting_step is None:
                first_meeting_step = step
                first_meeting_time = control.t
            meeting_count += 1
            if unequal_start_t is not None:
                total_unequal_time += control.t - unequal_start_t
                unequal_start_t = None
        elif (not equal_now) and equal_prev:
            unequal_start_t = control.t
        equal_prev = equal_now

        if step % log_every == 0 or step == 1 or step == steps:
            snap = v7.damage_snapshot(control, perturbed, support)
            log_rows.append({"step": step, "t": control.t, **snap})

    if unequal_start_t is not None:
        total_unequal_time += control.t - unequal_start_t

    final_snap = v7.damage_snapshot(control, perturbed, support)
    speed_ctrl = v7.estimate_front_speed(log_rows, "t", "radius_control")
    speed_pert = v7.estimate_front_speed(log_rows, "t", "radius_perturbed")
    hit_ctrl = first_hit_times_safe(log_rows, "radius_control", "t", 4)
    hit_step_ctrl = first_hit_steps(log_rows, "radius_control", 4)
    hit_pert = first_hit_times_safe(log_rows, "radius_perturbed", "t", 4)
    hit_step_pert = first_hit_steps(log_rows, "radius_perturbed", 4)

    headline_metrics = {
        "final_time": control.t,
        "final_radius_control": final_snap["radius_control"],
        "final_radius_perturbed": final_snap["radius_perturbed"],
        "final_edge_diff_count": final_snap["edge_diff_count"],
        "fit_speed_control": speed_ctrl["fit_slope"],
        "fit_speed_perturbed": speed_pert["fit_slope"],
        "max_ratio_control": speed_ctrl["max_ratio"],
        "max_ratio_perturbed": speed_pert["max_ratio"],
        "max_radius_control": max_radius(log_rows, "radius_control"),
        "max_radius_perturbed": max_radius(log_rows, "radius_perturbed"),
        "first_meeting_time": first_meeting_time if first_meeting_time is not None else -1.0,
        "first_meeting_step": first_meeting_step if first_meeting_step is not None else -1,
        "meeting_count": meeting_count,
        "total_unequal_time": total_unequal_time,
        "shared_token_fraction_final": final_snap["token_shared_fraction"],
        "shared_node_fraction_final": final_snap["node_shared_fraction"],
        "radius_drop_rate_control": radius_drop_rate(log_rows, "radius_control"),
        "radius_drop_rate_perturbed": radius_drop_rate(log_rows, "radius_perturbed"),
    }
    for r in range(5):
        headline_metrics[f"hit_t_control_r{r}"] = hit_ctrl[r] if hit_ctrl[r] is not None else float("nan")
        headline_metrics[f"hit_t_perturbed_r{r}"] = hit_pert[r] if hit_pert[r] is not None else float("nan")
        headline_metrics[f"hit_step_control_r{r}"] = hit_step_ctrl[r] if hit_step_ctrl[r] is not None else -1
        headline_metrics[f"hit_step_perturbed_r{r}"] = hit_step_pert[r] if hit_step_pert[r] is not None else -1

    return {
        "headline_metrics": headline_metrics,
        "coupling": v7.summarize_events(event_rows),
        "log_rows": log_rows,
        "control_final": control,
        "perturbed_final": perturbed,
        "initial_control_features": v7.feature_row(base_state, rng=random.Random(seed + 999)),
        "initial_support": support,
        "perturbation_info": dict(perturbation_info),
    }


def collect_run_rows(
    specs: Sequence[Dict[str, Any]],
    ensembles: Sequence[v10b.CalibrationEnsemble],
    base_states: Mapping[Tuple[str, int], v7.State],
    growth_seeds: Sequence[int],
    run_offsets: Sequence[int],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for spec in specs:
        cand = spec["candidate"]
        params = v09.candidate_to_params(cand)
        for ens in ensembles:
            for gseed in growth_seeds:
                base = base_states[(ens.name, int(gseed))]
                steps = steps_for_state(base.g.num_nodes())
                log_every = max(12, min(80, steps // 10))
                for run_offset in run_offsets:
                    run_seed = int(ens.target_nodes) * 100000 + int(gseed) * 1000 + int(run_offset)
                    for requested in PERTURBATIONS:
                        res = run_coupled_from_base_with_info(
                            base,
                            params=params,
                            seed=run_seed,
                            steps=steps,
                            perturbation=requested,
                            local_coupling="maximal",
                            log_every=log_every,
                        )
                        hm = res["headline_metrics"]
                        init = res["initial_control_features"]
                        perturb_info = res["perturbation_info"]
                        actual = str(perturb_info.get("type", "unknown"))
                        actual_category = perturbation_category(actual)
                        requested_match = perturbation_requested_match(requested, actual)
                        support = perturb_info.get("support", [])
                        rows.append(
                            {
                                "candidate_name": cand.name,
                                "candidate_role": spec["candidate_role"],
                                "ensemble": ens.name,
                                "burnin_label": ens.burnin_label,
                                "target_nodes": ens.target_nodes,
                                "growth_seed": int(gseed),
                                "run_offset": int(run_offset),
                                "run_seed": int(run_seed),
                                "steps": int(steps),
                                "log_every": int(log_every),
                                "requested_perturbation": requested,
                                "actual_perturbation": actual,
                                "actual_perturbation_category": actual_category,
                                "requested_match": 1 if requested_match else 0,
                                "fallback_used": 0 if requested_match else 1,
                                "support_size": len(support),
                                "support_signature": ",".join(str(x) for x in support),
                                "initial_nodes": safe_float(init.get("nodes")),
                                "initial_tokens": safe_float(init.get("tokens")),
                                "initial_beta1": safe_float(init.get("beta1")),
                                "initial_triangles": safe_float(init.get("triangles")),
                                "initial_spectral_radius": safe_float(init.get("spectral_radius")),
                                "initial_dim_proxy": safe_float(init.get("dim_proxy")),
                                "avg_local_overlap": safe_float(res["coupling"].get("avg_local_overlap_both_accept"), 0.0),
                                "avg_same_descriptor": safe_float(res["coupling"].get("avg_same_descriptor_both_accept"), 0.0),
                                "final_radius_control": safe_float(hm.get("final_radius_control")),
                                "final_radius_perturbed": safe_float(hm.get("final_radius_perturbed")),
                                "max_radius_control": safe_float(hm.get("max_radius_control")),
                                "max_radius_perturbed": safe_float(hm.get("max_radius_perturbed")),
                                "fit_speed_control": safe_float(hm.get("fit_speed_control")),
                                "fit_speed_perturbed": safe_float(hm.get("fit_speed_perturbed")),
                                "max_ratio_control": safe_float(hm.get("max_ratio_control")),
                                "max_ratio_perturbed": safe_float(hm.get("max_ratio_perturbed")),
                                "radius_drop_rate_control": safe_float(hm.get("radius_drop_rate_control"), 0.0),
                                "radius_drop_rate_perturbed": safe_float(hm.get("radius_drop_rate_perturbed"), 0.0),
                                "first_meeting_time": safe_float(hm.get("first_meeting_time")),
                                "total_unequal_time": safe_float(hm.get("total_unequal_time")),
                                "shared_token_fraction_final": safe_float(hm.get("shared_token_fraction_final")),
                                "shared_node_fraction_final": safe_float(hm.get("shared_node_fraction_final")),
                                "hit_t_control_r2": safe_float(hm.get("hit_t_control_r2")),
                                "hit_t_control_r3": safe_float(hm.get("hit_t_control_r3")),
                                "hit_t_perturbed_r2": safe_float(hm.get("hit_t_perturbed_r2")),
                                "hit_t_perturbed_r3": safe_float(hm.get("hit_t_perturbed_r3")),
                                "hit_step_control_r2": int(hm.get("hit_step_control_r2", -1)),
                                "hit_step_control_r3": int(hm.get("hit_step_control_r3", -1)),
                                "edge_diff_count_final": safe_float(hm.get("final_edge_diff_count")),
                            }
                        )
    return rows


def summarize_runs(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: MutableMapping[Tuple[str, str], List[Dict[str, Any]]] = {}
    for row in run_rows:
        key = (str(row["candidate_name"]), str(row["requested_perturbation"]))
        groups.setdefault(key, []).append(dict(row))

    out: List[Dict[str, Any]] = []
    for (candidate_name, requested), rows in sorted(groups.items()):
        actual_match = [r for r in rows if int(r["requested_match"]) == 1]
        out.append(
            {
                "candidate_name": candidate_name,
                "requested_perturbation": requested,
                "n_runs": len(rows),
                "n_strict_requested_match": len(actual_match),
                "fallback_rate": mean_defined(float(r["fallback_used"]) for r in rows),
                "mean_support_size": mean_defined(safe_float(r["support_size"]) for r in rows),
                "mean_fit_speed_control": mean_defined(safe_float(r["fit_speed_control"]) for r in rows),
                "sd_fit_speed_control": sd_or_zero(safe_float(r["fit_speed_control"]) for r in rows),
                "mean_max_ratio_control": mean_defined(safe_float(r["max_ratio_control"]) for r in rows),
                "mean_max_radius_control": mean_defined(safe_float(r["max_radius_control"]) for r in rows),
                "mean_hit_t_control_r2": mean_defined(safe_float(r["hit_t_control_r2"]) for r in rows),
                "mean_hit_t_control_r3": mean_defined(safe_float(r["hit_t_control_r3"]) for r in rows),
                "hit_fraction_r2": mean_defined(1.0 if math.isfinite(safe_float(r["hit_t_control_r2"])) else 0.0 for r in rows),
                "hit_fraction_r3": mean_defined(1.0 if math.isfinite(safe_float(r["hit_t_control_r3"])) else 0.0 for r in rows),
                "mean_radius_drop_rate": mean_defined(safe_float(r["radius_drop_rate_control"]) for r in rows),
                "mean_avg_local_overlap": mean_defined(safe_float(r["avg_local_overlap"]) for r in rows),
                "mean_shared_node_fraction_final": mean_defined(safe_float(r["shared_node_fraction_final"]) for r in rows),
            }
        )
    return out


def artifact_checks(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: MutableMapping[Tuple[str, str], List[Dict[str, Any]]] = {}
    for row in run_rows:
        key = (str(row["candidate_name"]), str(row["requested_perturbation"]))
        groups.setdefault(key, []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for (candidate_name, requested), rows in sorted(groups.items()):
        support_sizes = [safe_float(r["support_size"]) for r in rows]
        strict_rows = [r for r in rows if int(r["requested_match"]) == 1]
        out.append(
            {
                "candidate_name": candidate_name,
                "requested_perturbation": requested,
                "n_runs": len(rows),
                "n_strict_requested_match": len(strict_rows),
                "fallback_rate": mean_defined(float(r["fallback_used"]) for r in rows),
                "min_support_size": min(support_sizes) if support_sizes else float("nan"),
                "max_support_size": max(support_sizes) if support_sizes else float("nan"),
                "q10_fit_speed_control": quantile([safe_float(r["fit_speed_control"]) for r in rows], 0.10),
                "q90_fit_speed_control": quantile([safe_float(r["fit_speed_control"]) for r in rows], 0.90),
                "mean_radius_drop_rate": mean_defined(safe_float(r["radius_drop_rate_control"]) for r in rows),
                "mean_shared_node_fraction_final": mean_defined(safe_float(r["shared_node_fraction_final"]) for r in rows),
                "artifact_flag": (
                    "fallback_risk"
                    if mean_defined(float(r["fallback_used"]) for r in rows) > 0.10
                    else "clean_enough"
                ),
            }
        )
    return out


def pairwise_perturbation_summary(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    matched: MutableMapping[Tuple[str, str, int, int], Dict[str, Dict[str, Any]]] = {}
    for row in run_rows:
        key = (
            str(row["candidate_name"]),
            str(row["ensemble"]),
            int(row["growth_seed"]),
            int(row["run_offset"]),
        )
        matched.setdefault(key, {})[str(row["requested_perturbation"])] = dict(row)

    records: MutableMapping[Tuple[str, str], List[Dict[str, Any]]] = {}
    for (candidate_name, _, _, _), lookup in matched.items():
        for left, right in combinations(PERTURBATIONS, 2):
            if left not in lookup or right not in lookup:
                continue
            lrow = lookup[left]
            rrow = lookup[right]
            strict = int(lrow["requested_match"]) == 1 and int(rrow["requested_match"]) == 1
            mean_speed_mag = max(
                1e-9,
                0.5 * (abs(safe_float(lrow["fit_speed_control"])) + abs(safe_float(rrow["fit_speed_control"]))),
            )
            mean_hit_mag = max(
                1e-9,
                0.5 * (
                    abs(safe_float(lrow["hit_t_control_r2"], 0.0)) +
                    abs(safe_float(rrow["hit_t_control_r2"], 0.0))
                ),
            )
            records.setdefault((candidate_name, f"{left}__vs__{right}"), []).append(
                {
                    "strict": strict,
                    "abs_delta_fit_speed": abs(safe_float(lrow["fit_speed_control"]) - safe_float(rrow["fit_speed_control"])),
                    "rel_delta_fit_speed": abs(safe_float(lrow["fit_speed_control"]) - safe_float(rrow["fit_speed_control"])) / mean_speed_mag,
                    "abs_delta_hit_t_r2": abs(safe_float(lrow["hit_t_control_r2"]) - safe_float(rrow["hit_t_control_r2"])),
                    "rel_delta_hit_t_r2": abs(safe_float(lrow["hit_t_control_r2"]) - safe_float(rrow["hit_t_control_r2"])) / mean_hit_mag,
                    "abs_delta_hit_t_r3": abs(safe_float(lrow["hit_t_control_r3"]) - safe_float(rrow["hit_t_control_r3"])),
                    "abs_delta_radius_drop": abs(safe_float(lrow["radius_drop_rate_control"]) - safe_float(rrow["radius_drop_rate_control"])),
                    "abs_delta_support": abs(safe_float(lrow["support_size"]) - safe_float(rrow["support_size"])),
                }
            )

    out: List[Dict[str, Any]] = []
    for (candidate_name, pair_name), rows in sorted(records.items()):
        strict_rows = [r for r in rows if int(r["strict"]) == 1]
        left, right = pair_name.split("__vs__")
        scope = "primary_structural" if {left, right} == set(PRIMARY_STRUCTURAL_PAIR) else "diagnostic"
        source = strict_rows if strict_rows else rows
        out.append(
            {
                "candidate_name": candidate_name,
                "pair_name": pair_name,
                "scope": scope,
                "n_pairs_all": len(rows),
                "n_pairs_strict": len(strict_rows),
                "strict_fraction": len(strict_rows) / max(1, len(rows)),
                "mean_abs_delta_fit_speed": mean_defined(safe_float(r["abs_delta_fit_speed"]) for r in source),
                "mean_rel_delta_fit_speed": mean_defined(safe_float(r["rel_delta_fit_speed"]) for r in source),
                "mean_abs_delta_hit_t_r2": mean_defined(safe_float(r["abs_delta_hit_t_r2"]) for r in source),
                "mean_rel_delta_hit_t_r2": mean_defined(safe_float(r["rel_delta_hit_t_r2"]) for r in source),
                "mean_abs_delta_hit_t_r3": mean_defined(safe_float(r["abs_delta_hit_t_r3"]) for r in source),
                "mean_abs_delta_radius_drop": mean_defined(safe_float(r["abs_delta_radius_drop"]) for r in source),
                "mean_abs_delta_support": mean_defined(safe_float(r["abs_delta_support"]) for r in source),
            }
        )
    return out


def regime_gap_summary(aggregate_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    lookup = {(str(r["candidate_name"]), str(r["requested_perturbation"])): dict(r) for r in aggregate_rows}
    out: List[Dict[str, Any]] = []
    for requested in PERTURBATIONS:
        anchor = lookup.get((ANCHOR_CANDIDATE, requested))
        control = lookup.get((CONTROL_CANDIDATE, requested))
        if not anchor or not control:
            continue
        out.append(
            {
                "requested_perturbation": requested,
                "delta_mean_fit_speed_control": safe_float(control["mean_fit_speed_control"]) - safe_float(anchor["mean_fit_speed_control"]),
                "delta_mean_hit_t_control_r2": safe_float(control["mean_hit_t_control_r2"]) - safe_float(anchor["mean_hit_t_control_r2"]),
                "delta_mean_hit_t_control_r3": safe_float(control["mean_hit_t_control_r3"]) - safe_float(anchor["mean_hit_t_control_r3"]),
                "delta_fallback_rate": safe_float(control["fallback_rate"]) - safe_float(anchor["fallback_rate"]),
            }
        )
    return out


def recommendation_rows(
    target_summary: Sequence[Dict[str, Any]],
    artifact_rows: Sequence[Dict[str, Any]],
    pairwise_rows: Sequence[Dict[str, Any]],
    regime_gap_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    out.append(
        {
            "diagnostic_family": "generator_size_separation",
            "status": "clean" if size_clean else "unclear",
            "note": (
                "De dype startstørrelsene er fortsatt rent separert; frontmålingene ser ikke ut som en ren ensemblekollaps."
                if size_clean
                else "Startstørrelsene er ikke rent separert; Lorentz-diagnostikken bør ikke leses hardt."
            ),
        }
    )

    worst_fallback = max((safe_float(r["fallback_rate"], 0.0) for r in artifact_rows), default=0.0)
    artifact_status = "clean_enough" if worst_fallback <= 0.10 else "fallback_risk"
    out.append(
        {
            "diagnostic_family": "perturbation_artifact_control",
            "status": artifact_status,
            "note": (
                "Fallback-raten er lav nok til at de primære sammenlikningene kan leses som lokale perturbasjoner."
                if artifact_status == "clean_enough"
                else "Minst én perturbasjon faller for ofte tilbake til en annen operasjon; dette svekker Lorentz-lesningen."
            ),
        }
    )

    primary = [r for r in pairwise_rows if str(r["scope"]) == "primary_structural"]
    worst_rel_speed = max((safe_float(r["mean_rel_delta_fit_speed"]) for r in primary), default=float("nan"))
    worst_rel_hit = max((safe_float(r["mean_rel_delta_hit_t_r2"]) for r in primary), default=float("nan"))
    regime_gap = max((abs(safe_float(r["delta_mean_fit_speed_control"])) for r in regime_gap_rows), default=float("nan"))

    if size_clean and artifact_status == "clean_enough" and math.isfinite(worst_rel_speed):
        if worst_rel_speed <= 0.15 and worst_rel_hit <= 0.20 and regime_gap <= 0.015:
            status = "tentative_local_universality"
            note = (
                "De primære strukturelle perturbasjonene gir ganske like frontmålinger lokalt, og nærkontrollen driver ikke hastigheten mye."
            )
        else:
            status = "mode_dependent_not_yet"
            note = (
                "Frontmålingene varierer fortsatt for mye mellom perturbasjonstyper og/eller nærkontrollregimer til å kalle dette Lorentz-likt."
            )
    else:
        status = "artifact_limited"
        note = "Artefaktkontrollene er ikke rene nok til å lese frontmålingene som en Lorentz-diagnostikk."

    out.append(
        {
            "diagnostic_family": "lorentz_like_front_speed",
            "status": status,
            "note": note,
        }
    )
    out.append(
        {
            "diagnostic_family": "next_step",
            "status": (
                "targeted_followup_ok"
                if status == "tentative_local_universality"
                else "keep_local_and_narrow"
            ),
            "note": (
                "Neste steg kan være en litt større Lorentz-batch med isotropi-/dispersion-kontroll."
                if status == "tentative_local_universality"
                else "Neste steg bør fortsatt være smalt: enten dypere matched perturbation-runder eller en egen isotropi-diagnostikk, ikke bred oppskalering."
            ),
        }
    )
    return out


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def build_report(
    target_summary: Sequence[Dict[str, Any]],
    aggregate_rows: Sequence[Dict[str, Any]],
    artifact_rows: Sequence[Dict[str, Any]],
    pairwise_rows: Sequence[Dict[str, Any]],
    regime_gap_rows: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.14: smal Lorentz-diagnostikk med artefaktkontroll")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden prøver ikke å bevise Lorentz-likhet. Den tester en smalere og mer operasjonell del av spørsmålet: om skadefronten har omtrent samme effektive fart for ulike lokale perturbasjoner når vi bruker de samme basegrafene, de samme seedene og en eksplisitt fallback-kontroll."
    )
    lines.append("")
    lines.append("## Hva som holdes fast")
    lines.append("")
    lines.append("- Samme dype, size-separerte startensembler brukes på tvers av alle perturbasjonstyper.")
    lines.append("- Samme basegraf og samme run-seed brukes når vi sammenlikner perturbasjoner.")
    lines.append("- Den aktive frontier-kandidaten `band_zero_del` er ankerregime.")
    lines.append("- `band_pdel_0005` er en nær kontroll, ikke en ny frontier-scan.")
    lines.append("- Vi logger faktisk perturbasjonstype etter fallback, slik at vi ikke antar at ønsket inngrep faktisk ble brukt.")
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Perturbasjon og artefaktkontroll")
    lines.append("")
    lines.append("| regime | requested | fallback_rate | support_size | fit_speed q10-q90 | artifact_flag |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in artifact_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['requested_perturbation']} | {fmt(row['fallback_rate'])} | {fmt(row['min_support_size'],1)}-{fmt(row['max_support_size'],1)} | {fmt(row['q10_fit_speed_control'])}-{fmt(row['q90_fit_speed_control'])} | {row['artifact_flag']} |"
        )
    lines.append("")
    lines.append("## Aggregert frontbilde")
    lines.append("")
    lines.append("| regime | requested | n | strict | mean fit_speed | mean hit t(r=2) | mean hit t(r=3) | mean drop rate |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['requested_perturbation']} | {int(row['n_runs'])} | {int(row['n_strict_requested_match'])} | {fmt(row['mean_fit_speed_control'])} | {fmt(row['mean_hit_t_control_r2'])} | {fmt(row['mean_hit_t_control_r3'])} | {fmt(row['mean_radius_drop_rate'])} |"
        )
    lines.append("")
    lines.append("## Matchede perturbasjonssammenlikninger")
    lines.append("")
    lines.append("| regime | pair | scope | strict_fraction | rel speed gap | rel hit gap r2 | support gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in pairwise_rows:
        lines.append(
            f"| {row['candidate_name']} | {row['pair_name']} | {row['scope']} | {fmt(row['strict_fraction'])} | {fmt(row['mean_rel_delta_fit_speed'])} | {fmt(row['mean_rel_delta_hit_t_r2'])} | {fmt(row['mean_abs_delta_support'],1)} |"
        )
    lines.append("")
    lines.append("## Nær regimekontroll")
    lines.append("")
    lines.append("| requested | delta fit_speed (control-anchor) | delta hit t(r=2) | delta fallback |")
    lines.append("| --- | --- | --- | --- |")
    for row in regime_gap_rows:
        lines.append(
            f"| {row['requested_perturbation']} | {fmt(row['delta_mean_fit_speed_control'])} | {fmt(row['delta_mean_hit_t_control_r2'])} | {fmt(row['delta_fallback_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Viktig avgrensning")
    lines.append("")
    lines.append("- Denne runden tester ikke isotropi i flere retninger på samme basegraf.")
    lines.append("- Den tester heller ikke IR-dispersjon eller mikroframe-hiding direkte.")
    lines.append("- Derfor kan et positivt resultat her bare være en lokal støtte for videre Lorentz-diagnostikk, ikke en full bekreftelse.")
    lines.append("")
    return "\n".join(lines)


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    lorentz_row = next((row for row in recommendation if row["diagnostic_family"] == "lorentz_like_front_speed"), None)
    next_row = next((row for row in recommendation if row["diagnostic_family"] == "next_step"), None)
    lines = [
        "# Relasjonell universgraf v0.14 for ikke-spesialister",
        "",
        "Vi testet om en lokal forstyrrelse ser ut til å spre seg med omtrent samme fart når vi lager ulike typer små inngrep i den samme grafen.",
        "",
        "For å unngå juks eller skjulte simulasjonsartefakter brukte vi de samme startgrafene, de samme tilfeldige seedene og logget når et ønsket inngrep faktisk måtte falle tilbake til en annen type inngrep.",
        "",
        f"Hoveddommen nå er `{lorentz_row['status'] if lorentz_row else 'ukjent'}`.",
        "",
        f"Det betyr: {lorentz_row['note'] if lorentz_row else 'Lorentz-diagnostikken er ikke oppsummert ennå.'}",
        "",
        f"Neste anbefaling er: {next_row['note'] if next_row else 'ingen ny anbefaling registrert.'}",
        "",
        "Kort sagt: vi ser fortsatt lokalitet og begrenset spredning, men vi har ikke vist noe som ligner en robust universell lyshastighet ennå.",
        "",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.14 Lorentz diagnostics with artifact controls.")
    p.add_argument("--targets", type=str, default="48,96,192,256")
    p.add_argument("--growth-seeds", type=str, default="101,202")
    p.add_argument("--run-offsets", type=str, default="0,17")
    p.add_argument("--out-run-csv", type=str, default="Documentation/v14_lorentz_run_rows.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v14_lorentz_target_summary.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v14_lorentz_aggregate_summary.csv")
    p.add_argument("--out-pairwise-csv", type=str, default="Documentation/v14_lorentz_pairwise_perturbation_summary.csv")
    p.add_argument("--out-artifact-csv", type=str, default="Documentation/v14_lorentz_artifact_checks.csv")
    p.add_argument("--out-regime-gap-csv", type=str, default="Documentation/v14_lorentz_regime_gap_summary.csv")
    p.add_argument("--out-recommendation-csv", type=str, default="Documentation/v14_lorentz_recommendations.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v14_lorentz_diagnostics.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_14.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_14_operativ_anbefaling.md")
    return p.parse_args()


def parse_int_list(spec: str) -> List[int]:
    return [int(part.strip()) for part in spec.split(",") if part.strip()]


def main() -> None:
    args = parse_args()
    targets = parse_int_list(args.targets)
    growth_seeds = parse_int_list(args.growth_seeds)
    run_offsets = parse_int_list(args.run_offsets)

    specs = candidate_specs()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = deep_ensembles(targets)
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)

    run_rows = collect_run_rows(specs, ensembles, base_states, growth_seeds, run_offsets)
    aggregate_rows = summarize_runs(run_rows)
    artifact_rows = artifact_checks(run_rows)
    pairwise_rows = pairwise_perturbation_summary(run_rows)
    regime_gap_rows = regime_gap_summary(aggregate_rows)
    recommendation = recommendation_rows(target_summary, artifact_rows, pairwise_rows, regime_gap_rows)

    report_md = build_report(
        target_summary=target_summary,
        aggregate_rows=aggregate_rows,
        artifact_rows=artifact_rows,
        pairwise_rows=pairwise_rows,
        regime_gap_rows=regime_gap_rows,
        recommendation=recommendation,
    )
    lay_md = build_lay_summary(recommendation)
    op_md = "\n".join(
        [
            "# v0.14 operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Ikke les denne runden som et bevis på Lorentz-likhet.",
            "- Les den som en ren diagnostikk av om frontfarten begynner å se universell ut under strammere kontroll.",
        ]
    )

    write_csv(args.out_run_csv, run_rows)
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_aggregate_csv, aggregate_rows)
    write_csv(args.out_pairwise_csv, pairwise_rows)
    write_csv(args.out_artifact_csv, artifact_rows)
    write_csv(args.out_regime_gap_csv, regime_gap_rows)
    write_csv(args.out_recommendation_csv, recommendation)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")

    print(f"Wrote {args.out_summary_md}")
    print(f"Wrote {args.out_aggregate_csv}")
    print(f"Wrote {args.out_pairwise_csv}")


if __name__ == "__main__":
    main()
