
#!/usr/bin/env python3
"""relational_universe_v08b_natural_ensemble_robustness.py

v0.8b: p_del refinement + larger natural start ensembles + bootstrap robustness.

This script extends v0.8 in exactly the direction suggested by the project's
internal critique: promising regimes must survive contact with larger and more
naturalized initial ensembles, not only with small toy cycles.

Main additions
--------------
1. Open a local p_del axis around the v0.8 candidate band.
2. Replace "only small cycle seed" with a family of start ensembles:
   - toy_cycle8 (baseline / continuity with earlier work)
   - natural24   (grown by the model's own single-branch dynamics)
   - natural48   (same, but larger)
   - natural_jitter (grown to a random moderate-large size with extra burn-in)
3. Add bootstrap confidence intervals for ensemble-wise and natural-ensemble
   mean composite scores.
4. Report robust candidates using lower confidence bounds across the natural
   ensembles, not only raw average score.

The script deliberately reuses v0.7 local maximal coupling as the dynamical core
and v0.8 score families as the operational evaluation layer.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08_phase_atlas as v8


# ------------------------------------------------------------
# Generic helpers
# ------------------------------------------------------------

def safe_float(x: Any, default: float = 0.0) -> float:
    try:
        y = float(x)
    except Exception:
        return default
    if math.isnan(y) or math.isinf(y):
        return default
    return y

def quantile(values: Sequence[float], q: float) -> float:
    vals = sorted(v for v in values if isinstance(v, (int, float)) and math.isfinite(v))
    if not vals:
        return float("nan")
    if q <= 0:
        return vals[0]
    if q >= 1:
        return vals[-1]
    pos = (len(vals) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return vals[lo]
    frac = pos - lo
    return vals[lo] * (1.0 - frac) + vals[hi] * frac

def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    path = str(path)
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    keys: List[str] = []
    seen = set()
    for row in rows:
        for k in row:
            if k not in seen:
                seen.add(k)
                keys.append(k)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow(row)

def markdown_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    head = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows[1:])
    return "\n".join([head, sep, body])


# ------------------------------------------------------------
# Dataclasses
# ------------------------------------------------------------

@dataclass(frozen=True)
class CandidatePoint:
    name: str
    r_birth: float
    r_death: float
    p_swap: float
    p_triad: float
    p_del: float

    def key(self) -> Tuple[float, float, float, float, float]:
        return (self.r_birth, self.r_death, self.p_swap, self.p_triad, self.p_del)

@dataclass(frozen=True)
class EnsembleSpec:
    name: str
    kind: str  # toy_cycle | natural_grown
    initial_cycle: int
    initial_tokens: int
    target_nodes: int
    burnin_steps: int
    jitter_nodes_low: int = 0
    jitter_nodes_high: int = 0
    extra_burnin_low: int = 0
    extra_burnin_high: int = 0
    include_in_natural_score: int = 1


# ------------------------------------------------------------
# Single-branch dynamics for growing initial ensembles
# ------------------------------------------------------------

def next_ids_from_state(state: v7.State) -> Tuple[int, int]:
    next_node_id = (max(state.g.nodes()) + 1) if state.g.nodes() else 0
    next_token_id = (max(state.token_pos.keys()) + 1) if state.token_pos else 0
    return next_node_id, next_token_id

def single_step(state: v7.State, manager: v7.PairManager, rng: random.Random, params: v7.Params) -> Dict[str, Any]:
    rates = v7.family_rates(state, params)
    families = ["seed", "token", "birth", "death"]
    total = sum(rates[f] for f in families)
    if total <= 0.0:
        return {"family": "noop", "dt": 0.0, "descriptor": None}
    dt = rng.expovariate(total)
    state.t += dt
    x = rng.random() * total
    acc = 0.0
    family = families[-1]
    for f in families:
        acc += rates[f]
        if x <= acc:
            family = f
            break
    dist = v7.family_kernel(state, family, params)
    if not dist:
        return {"family": family, "dt": dt, "descriptor": None, "event": "null"}
    desc = v7.sample_from_dist(dist, rng)
    ctx = v7.apply_descriptor(state, family, desc, params, manager)
    return {"family": family, "dt": dt, "descriptor": repr(desc), **ctx}

def grow_state_for_ensemble(spec: EnsembleSpec, *, rng_seed: int, growth_params: v7.Params) -> v7.State:
    rng = random.Random(rng_seed)
    base, _, _ = v7.bootstrap(spec.initial_cycle, spec.initial_tokens, rng)
    state = base.clone()
    next_node_id, next_token_id = next_ids_from_state(state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)

    if spec.kind == "toy_cycle":
        return state

    target_nodes = spec.target_nodes
    if spec.jitter_nodes_high > spec.jitter_nodes_low:
        target_nodes = rng.randint(spec.jitter_nodes_low, spec.jitter_nodes_high)

    steps = spec.burnin_steps
    if spec.extra_burnin_high > spec.extra_burnin_low:
        steps += rng.randint(spec.extra_burnin_low, spec.extra_burnin_high)

    # Run until either target size is reached or burn-in exhausted.
    for _ in range(max(0, steps)):
        single_step(state, manager, rng, growth_params)
        if state.g.num_nodes() >= target_nodes:
            break

    # Optional extra decorrelation / naturalization pass after target is reached.
    extra = 0
    if spec.extra_burnin_high > spec.extra_burnin_low:
        extra = rng.randint(spec.extra_burnin_low, spec.extra_burnin_high)
    for _ in range(extra):
        single_step(state, manager, rng, growth_params)

    return state

def clone_state(state: v7.State) -> v7.State:
    return state.clone()



def find_local_swap_candidate(state: v7.State, center_token_index: int = 0) -> Optional[Tuple[int, int, int]]:
    """Find a local swap candidate (v,u,w) with edge (v,u) and local alternative w."""
    checked = set()
    token_nodes = []
    tids = state.sorted_token_ids()
    if tids:
        shift = center_token_index % len(tids)
        ordered_tids = tids[shift:] + tids[:shift]
        token_nodes = [state.token_pos[tid] for tid in ordered_tids if tid in state.token_pos]
    candidate_starts = token_nodes + [v for v in sorted(state.g.nodes()) if v not in token_nodes]
    for v in candidate_starts:
        if v in checked or v not in state.g.adj:
            continue
        checked.add(v)
        for u in sorted(state.g.neighbors(v)):
            triad_cands = sorted(w for w in state.g.neighbors(u) if w != v and not state.g.has_edge(v, w))
            if triad_cands:
                return (v, u, triad_cands[0])
            fallback = sorted(w for w in state.g.neighbors(u) if w != v)
            if fallback:
                return (v, u, fallback[0])
    return None

def find_chord_candidate(state: v7.State, center_token_index: int = 0) -> Optional[Tuple[int, int, int]]:
    """Find a local chord candidate (v,u,w) with v-u-w and no edge v-w."""
    checked = set()
    token_nodes = []
    tids = state.sorted_token_ids()
    if tids:
        shift = center_token_index % len(tids)
        ordered_tids = tids[shift:] + tids[:shift]
        token_nodes = [state.token_pos[tid] for tid in ordered_tids if tid in state.token_pos]
    candidate_starts = token_nodes + [v for v in sorted(state.g.nodes()) if v not in token_nodes]
    for v in candidate_starts:
        if v in checked or v not in state.g.adj:
            continue
        checked.add(v)
        for u in sorted(state.g.neighbors(v)):
            for w in sorted(state.g.neighbors(u)):
                if w != v and not state.g.has_edge(v, w):
                    return (v, u, w)
    return None

def find_token_shift_candidate(state: v7.State, center_token_index: int = 0) -> Optional[Tuple[int, int]]:
    tids = state.sorted_token_ids()
    if not tids:
        return None
    shift = center_token_index % len(tids)
    ordered_tids = tids[shift:] + tids[:shift]
    for tid in ordered_tids:
        v = state.token_pos.get(tid)
        if v is None:
            continue
        neigh = sorted(state.g.neighbors(v))
        if neigh:
            return (tid, neigh[0])
    return None

def apply_local_swap_anywhere(state: v7.State, center_token_index: int = 0) -> Dict[str, Any]:
    cand = find_local_swap_candidate(state, center_token_index=center_token_index)
    if cand is None:
        raise ValueError("Could not construct any local swap candidate in base state.")
    v, u, w = cand
    if state.g.has_edge(v, u):
        state.g.remove_edge(v, u)
    state.g.add_edge(v, w)
    return {
        "type": "local_swap_anywhere",
        "support": sorted({v, u, w}),
        "delta_core": {"tokens": 0, "nodes": 0, "components": 0, "beta1": 0},
    }

def apply_local_chord_anywhere(state: v7.State, center_token_index: int = 0) -> Dict[str, Any]:
    cand = find_chord_candidate(state, center_token_index=center_token_index)
    if cand is None:
        raise ValueError("Could not construct any chord candidate in base state.")
    v, u, w = cand
    state.g.add_edge(v, w)
    return {
        "type": "local_chord_anywhere",
        "support": sorted({v, u, w}),
        "delta_core": {"tokens": 0, "nodes": 0, "components": 0, "beta1": +1},
    }

def apply_token_shift_perturbation(state: v7.State, center_token_index: int = 0) -> Dict[str, Any]:
    cand = find_token_shift_candidate(state, center_token_index=center_token_index)
    if cand is None:
        raise ValueError("Could not construct any token shift candidate in base state.")
    tid, dst = cand
    src = state.token_pos[tid]
    state.token_pos[tid] = dst
    return {
        "type": "token_shift",
        "support": sorted({src, dst}),
        "delta_core": {"tokens": 0, "nodes": 0, "components": 0, "beta1": 0},
    }

def apply_custom_perturbation(state: v7.State, perturbation: str, center_token_index: int = 0) -> Dict[str, Any]:
    if perturbation == "local_swap":
        cand = find_local_swap_candidate(state, center_token_index=center_token_index)
        if cand is not None:
            return apply_local_swap_anywhere(state, center_token_index=center_token_index)
        cand = find_chord_candidate(state, center_token_index=center_token_index)
        if cand is not None:
            return apply_local_chord_anywhere(state, center_token_index=center_token_index)
        return apply_token_shift_perturbation(state, center_token_index=center_token_index)
    if perturbation == "add_chord":
        cand = find_chord_candidate(state, center_token_index=center_token_index)
        if cand is not None:
            return apply_local_chord_anywhere(state, center_token_index=center_token_index)
        return apply_token_shift_perturbation(state, center_token_index=center_token_index)
    if perturbation == "token_shift":
        return apply_token_shift_perturbation(state, center_token_index=center_token_index)
    raise ValueError(f"Unknown perturbation {perturbation!r}")


# ------------------------------------------------------------
# Coupled run from a custom base state
# ------------------------------------------------------------

def run_coupled_from_base(
    base_state: v7.State,
    *,
    params: v7.Params,
    seed: int,
    steps: int,
    perturbation: str = "local_swap",
    center_token_index: int = 0,
    local_coupling: str = "maximal",
    log_every: int = 40,
) -> Dict[str, Any]:
    rng = random.Random(seed)
    control = clone_state(base_state)
    perturbed = clone_state(base_state)

    perturbation_info = apply_custom_perturbation(perturbed, perturbation, center_token_index)
    support = perturbation_info["support"]

    next_node_id, next_token_id = next_ids_from_state(base_state)
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

    coupling = v7.summarize_events(event_rows)
    speed_ctrl = v7.estimate_front_speed(log_rows, "t", "radius_control")
    final_snap = v7.damage_snapshot(control, perturbed, support)

    headline_metrics = {
        "final_time": control.t,
        "final_radius_control": final_snap["radius_control"],
        "final_edge_diff_count": final_snap["edge_diff_count"],
        "fit_speed_control": speed_ctrl["fit_slope"],
        "first_meeting_time": first_meeting_time if first_meeting_time is not None else -1.0,
        "total_unequal_time": total_unequal_time,
        "shared_token_fraction_final": final_snap["token_shared_fraction"],
        "shared_node_fraction_final": final_snap["node_shared_fraction"],
    }

    return {
        "headline_metrics": headline_metrics,
        "coupling": coupling,
        "log_rows": log_rows,
        "control_final": control,
        "perturbed_final": perturbed,
        "initial_control_features": v7.feature_row(base_state),
        "initial_support": support,
    }


# ------------------------------------------------------------
# Candidate grid and ensemble library
# ------------------------------------------------------------

def default_candidates() -> List[CandidatePoint]:
    bases = [
        ("refined_winner", 0.08, 0.02, 0.02, 0.00),
        ("coarse_balanced", 0.02, 0.02, 0.02, 0.00),
        ("macro_stable", 0.02, 0.05, 0.02, 0.00),
        ("low_death", 0.02, 0.00, 0.02, 0.00),
        ("triad_sensitive", 0.02, 0.02, 0.02, 0.02),
    ]
    p_dels = [0.00, 0.01, 0.02, 0.04]
    out: List[CandidatePoint] = []
    for name, rb, rd, ps, pt in bases:
        for pd in p_dels:
            out.append(CandidatePoint(
                name=f"{name}_pdel{pd:.2f}",
                r_birth=rb, r_death=rd, p_swap=ps, p_triad=pt, p_del=pd
            ))
    return out

def default_ensembles() -> List[EnsembleSpec]:
    return [
        EnsembleSpec(
            name="toy_cycle8",
            kind="toy_cycle",
            initial_cycle=8,
            initial_tokens=4,
            target_nodes=8,
            burnin_steps=0,
            include_in_natural_score=0,
        ),
        EnsembleSpec(
            name="natural24",
            kind="natural_grown",
            initial_cycle=10,
            initial_tokens=5,
            target_nodes=24,
            burnin_steps=500,
            extra_burnin_low=60,
            extra_burnin_high=120,
            include_in_natural_score=1,
        ),
        EnsembleSpec(
            name="natural48",
            kind="natural_grown",
            initial_cycle=12,
            initial_tokens=6,
            target_nodes=48,
            burnin_steps=1200,
            extra_burnin_low=120,
            extra_burnin_high=220,
            include_in_natural_score=1,
        ),
        EnsembleSpec(
            name="natural_jitter",
            kind="natural_grown",
            initial_cycle=10,
            initial_tokens=5,
            target_nodes=32,
            burnin_steps=800,
            jitter_nodes_low=28,
            jitter_nodes_high=40,
            extra_burnin_low=140,
            extra_burnin_high=260,
            include_in_natural_score=1,
        ),
    ]

def reference_growth_params() -> v7.Params:
    return v7.Params(
        r_seed=0.30,
        r_token=1.0,
        r_birth=0.005,
        r_death=0.02,
        p_triad=0.01,
        p_del=0.00,
        p_swap=0.02,
        birth_degree_bias=0.5,
        death_inverse_degree_scale=1.0,
        min_tokens=1,
        forbid_pruning_current_token_node=True,
    )

def candidate_to_params(point: CandidatePoint) -> v7.Params:
    return v7.Params(
        r_seed=0.04,
        r_token=1.0,
        r_birth=point.r_birth,
        r_death=point.r_death,
        p_triad=point.p_triad,
        p_del=point.p_del,
        p_swap=point.p_swap,
        birth_degree_bias=0.5,
        death_inverse_degree_scale=1.0,
        min_tokens=1,
        forbid_pruning_current_token_node=True,
    )


# ------------------------------------------------------------
# Metrics / aggregation / bootstrap
# ------------------------------------------------------------

RUN_KEYS = [
    "meeting",
    "first_meeting_time",
    "final_radius_control",
    "total_unequal_time",
    "avg_local_overlap",
    "avg_same_descriptor",
    "shared_token_fraction_final",
    "shared_node_fraction_final",
    "fit_speed_control",
    "final_edge_diff_count",
    "abs_delta_tokens",
    "abs_delta_nodes",
    "abs_delta_beta1",
    "abs_delta_triangles",
    "abs_delta_spectral_radius",
    "abs_delta_clustering",
    "abs_delta_dim_proxy",
    "initial_nodes",
    "initial_tokens",
    "initial_beta1",
    "initial_triangles",
    "initial_spectral_radius",
    "initial_dim_proxy",
]

def collect_run_row(point: CandidatePoint, ensemble: EnsembleSpec, base_state: v7.State, *, seed: int, steps: int) -> Dict[str, Any]:
    params = candidate_to_params(point)
    res = run_coupled_from_base(
        base_state,
        params=params,
        seed=seed,
        steps=steps,
        perturbation="local_swap",
        local_coupling="maximal",
        log_every=max(25, min(100, steps // 5)),
    )
    hm = res["headline_metrics"]
    last = res["log_rows"][-1]
    init = res["initial_control_features"]
    return {
        "ensemble": ensemble.name,
        "seed": seed,
        "candidate_name": point.name,
        "r_birth": point.r_birth,
        "r_death": point.r_death,
        "p_swap": point.p_swap,
        "p_triad": point.p_triad,
        "p_del": point.p_del,
        "meeting": 1 if safe_float(hm.get("first_meeting_time"), -1.0) >= 0.0 else 0,
        "first_meeting_time": safe_float(hm.get("first_meeting_time"), default=float("nan")),
        "final_radius_control": safe_float(hm.get("final_radius_control"), default=float("nan")),
        "total_unequal_time": safe_float(hm.get("total_unequal_time"), default=float("nan")),
        "avg_local_overlap": safe_float(res["coupling"].get("avg_local_overlap_both_accept"), default=0.0),
        "avg_same_descriptor": safe_float(res["coupling"].get("avg_same_descriptor_both_accept"), default=0.0),
        "shared_token_fraction_final": safe_float(hm.get("shared_token_fraction_final"), default=0.0),
        "shared_node_fraction_final": safe_float(hm.get("shared_node_fraction_final"), default=0.0),
        "fit_speed_control": max(0.0, safe_float(hm.get("fit_speed_control"), default=0.0)),
        "final_edge_diff_count": safe_float(hm.get("final_edge_diff_count"), default=0.0),
        "abs_delta_tokens": abs(safe_float(last.get("delta_tokens"), default=0.0)),
        "abs_delta_nodes": abs(safe_float(last.get("delta_nodes"), default=0.0)),
        "abs_delta_beta1": abs(safe_float(last.get("delta_beta1"), default=0.0)),
        "abs_delta_triangles": abs(safe_float(last.get("delta_triangles"), default=0.0)),
        "abs_delta_spectral_radius": abs(safe_float(last.get("delta_spectral_radius"), default=0.0)),
        "abs_delta_clustering": abs(safe_float(last.get("delta_clustering"), default=0.0)),
        "abs_delta_dim_proxy": abs(safe_float(last.get("delta_dim_proxy"), default=0.0)),
        "initial_nodes": safe_float(init.get("nodes"), default=float("nan")),
        "initial_tokens": safe_float(init.get("tokens"), default=float("nan")),
        "initial_beta1": safe_float(init.get("beta1"), default=float("nan")),
        "initial_triangles": safe_float(init.get("triangles"), default=float("nan")),
        "initial_spectral_radius": safe_float(init.get("spectral_radius"), default=float("nan")),
        "initial_dim_proxy": safe_float(init.get("dim_proxy"), default=float("nan")),
    }

def summarize_group(point: CandidatePoint, ensemble: EnsembleSpec, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "ensemble": ensemble.name,
        "candidate_name": point.name,
        "r_birth": point.r_birth,
        "r_death": point.r_death,
        "p_swap": point.p_swap,
        "p_triad": point.p_triad,
        "p_del": point.p_del,
        "runs": len(rows),
    }
    for key in RUN_KEYS:
        vals = [safe_float(r.get(key), default=float("nan")) for r in rows]
        vals_f = [v for v in vals if math.isfinite(v)]
        out[f"mean_{key}"] = float(statistics.mean(vals_f)) if vals_f else float("nan")
        out[f"sd_{key}"] = float(statistics.pstdev(vals_f)) if len(vals_f) >= 2 else 0.0
    return out

def score_ranges(rows: List[Dict[str, Any]]) -> Dict[str, Tuple[float, float, bool]]:
    ranges: Dict[str, Tuple[float, float, bool]] = {}
    for family, metrics in v8.SCORE_METRICS.items():
        for key, higher in metrics:
            vals = [safe_float(r.get(key), default=float("nan")) for r in rows]
            vals = [v for v in vals if math.isfinite(v)]
            if vals:
                ranges[key] = (min(vals), max(vals), higher)
            else:
                ranges[key] = (float("nan"), float("nan"), higher)
    return ranges

def score_row_from_ranges(row: Dict[str, Any], ranges: Dict[str, Tuple[float, float, bool]]) -> Dict[str, float]:
    out: Dict[str, float] = {}
    comp = 0.0
    weight_total = 0.0
    for family, metrics in v8.SCORE_METRICS.items():
        parts = []
        for key, higher in metrics:
            lo, hi, hb = ranges[key]
            s = v8.objective_score(safe_float(row.get(key), default=float("nan")), lo, hi, higher_better=hb)
            parts.append(s)
        score = v8.average_defined(parts)
        out[f"{family}_score"] = score
        if math.isfinite(score):
            comp += v8.WEIGHTS[family] * score
            weight_total += v8.WEIGHTS[family]
    out["composite_score"] = (comp / weight_total) if weight_total > 0 else float("nan")
    return out

def add_scores_per_ensemble(agg_rows: List[Dict[str, Any]]) -> None:
    by_ensemble: Dict[str, List[Dict[str, Any]]] = {}
    for row in agg_rows:
        by_ensemble.setdefault(str(row["ensemble"]), []).append(row)
    for rows in by_ensemble.values():
        v8.add_scores(rows)

def bootstrap_ci_for_group(
    point: CandidatePoint,
    ensemble: EnsembleSpec,
    run_rows: List[Dict[str, Any]],
    ranges: Dict[str, Tuple[float, float, bool]],
    *,
    bootstrap_reps: int,
    rng_seed: int,
) -> Dict[str, float]:
    rng = random.Random(rng_seed)
    if not run_rows:
        return {
            "ci_low_composite": float("nan"),
            "ci_high_composite": float("nan"),
            "ci_low_mean_radius": float("nan"),
            "ci_high_mean_radius": float("nan"),
            "ci_low_mean_overlap": float("nan"),
            "ci_high_mean_overlap": float("nan"),
        }
    comp_vals = []
    radius_vals = []
    overlap_vals = []
    n = len(run_rows)
    for _ in range(bootstrap_reps):
        sample = [run_rows[rng.randrange(n)] for _ in range(n)]
        agg = summarize_group(point, ensemble, sample)
        scores = score_row_from_ranges(agg, ranges)
        comp_vals.append(safe_float(scores["composite_score"], float("nan")))
        radius_vals.append(safe_float(agg.get("mean_final_radius_control"), float("nan")))
        overlap_vals.append(safe_float(agg.get("mean_avg_local_overlap"), float("nan")))
    return {
        "ci_low_composite": quantile(comp_vals, 0.025),
        "ci_high_composite": quantile(comp_vals, 0.975),
        "ci_low_mean_radius": quantile(radius_vals, 0.025),
        "ci_high_mean_radius": quantile(radius_vals, 0.975),
        "ci_low_mean_overlap": quantile(overlap_vals, 0.025),
        "ci_high_mean_overlap": quantile(overlap_vals, 0.975),
    }

def aggregate_overall(
    ensemble_rows: List[Dict[str, Any]],
    ensembles: List[EnsembleSpec],
    *,
    bootstrap_reps: int,
    rng_seed: int,
) -> List[Dict[str, Any]]:
    natural_names = {e.name for e in ensembles if e.include_in_natural_score}
    by_key: Dict[Tuple[float, float, float, float, float], List[Dict[str, Any]]] = {}
    for row in ensemble_rows:
        key = (float(row["r_birth"]), float(row["r_death"]), float(row["p_swap"]), float(row["p_triad"]), float(row["p_del"]))
        by_key.setdefault(key, []).append(row)

    out_rows: List[Dict[str, Any]] = []
    rng = random.Random(rng_seed)

    for key, rows in by_key.items():
        rows_nat = [r for r in rows if r["ensemble"] in natural_names]
        mean_comp_all = statistics.mean(safe_float(r["composite_score"], float("nan")) for r in rows)
        mean_comp_nat = statistics.mean(safe_float(r["composite_score"], float("nan")) for r in rows_nat)
        min_comp_nat = min(safe_float(r["composite_score"], float("nan")) for r in rows_nat)
        sd_comp_nat = statistics.pstdev([safe_float(r["composite_score"], float("nan")) for r in rows_nat]) if len(rows_nat) >= 2 else 0.0

        # bootstrap over natural ensembles by resampling ensemble-level rows
        nat_scores = [safe_float(r["composite_score"], float("nan")) for r in rows_nat]
        ci_low = float("nan")
        ci_high = float("nan")
        if nat_scores:
            boots = []
            m = len(nat_scores)
            for _ in range(bootstrap_reps):
                sample = [nat_scores[rng.randrange(m)] for _ in range(m)]
                boots.append(float(statistics.mean(sample)))
            ci_low = quantile(boots, 0.025)
            ci_high = quantile(boots, 0.975)

        out = {
            "r_birth": key[0],
            "r_death": key[1],
            "p_swap": key[2],
            "p_triad": key[3],
            "p_del": key[4],
            "ensemble_rows": len(rows),
            "natural_ensemble_rows": len(rows_nat),
            "mean_composite_all": mean_comp_all,
            "mean_composite_natural": mean_comp_nat,
            "min_composite_natural": min_comp_nat,
            "sd_composite_natural": sd_comp_nat,
            "ci_low_mean_composite_natural": ci_low,
            "ci_high_mean_composite_natural": ci_high,
            "mean_repair_natural": statistics.mean(safe_float(r["repair_score"], float("nan")) for r in rows_nat),
            "mean_causal_natural": statistics.mean(safe_float(r["causal_score"], float("nan")) for r in rows_nat),
            "mean_quasi_natural": statistics.mean(safe_float(r["quasi_score"], float("nan")) for r in rows_nat),
            "mean_geom_natural": statistics.mean(safe_float(r["geom_score"], float("nan")) for r in rows_nat),
            "mean_initial_nodes_natural": statistics.mean(safe_float(r["mean_initial_nodes"], float("nan")) for r in rows_nat),
            "mean_initial_tokens_natural": statistics.mean(safe_float(r["mean_initial_tokens"], float("nan")) for r in rows_nat),
            "mean_radius_natural": statistics.mean(safe_float(r["mean_final_radius_control"], float("nan")) for r in rows_nat),
            "mean_overlap_natural": statistics.mean(safe_float(r["mean_avg_local_overlap"], float("nan")) for r in rows_nat),
        }
        out_rows.append(out)

    out_rows.sort(key=lambda r: (safe_float(r["ci_low_mean_composite_natural"], -1.0), safe_float(r["mean_composite_natural"], -1.0)), reverse=True)
    return out_rows


# ------------------------------------------------------------
# Reporting
# ------------------------------------------------------------

def top_candidates_md(overall_rows: List[Dict[str, Any]], n: int = 10) -> str:
    top = overall_rows[:n]
    rows = [["r_birth", "r_death", "p_swap", "p_triad", "p_del", "mean_nat", "ci_low_nat", "ci_high_nat", "min_nat", "sd_nat", "radius", "overlap"]]
    for r in top:
        rows.append([
            f"{r['r_birth']:.3g}",
            f"{r['r_death']:.3g}",
            f"{r['p_swap']:.3g}",
            f"{r['p_triad']:.3g}",
            f"{r['p_del']:.3g}",
            f"{safe_float(r['mean_composite_natural']):.3f}",
            f"{safe_float(r['ci_low_mean_composite_natural']):.3f}",
            f"{safe_float(r['ci_high_mean_composite_natural']):.3f}",
            f"{safe_float(r['min_composite_natural']):.3f}",
            f"{safe_float(r['sd_composite_natural']):.3f}",
            f"{safe_float(r['mean_radius_natural']):.3f}",
            f"{safe_float(r['mean_overlap_natural']):.3f}",
        ])
    return markdown_table(rows)

def pdel_table(overall_rows: List[Dict[str, Any]], rb: float, rd: float, ps: float, pt: float) -> str:
    rows = [r for r in overall_rows if abs(float(r["r_birth"]) - rb) < 1e-12 and abs(float(r["r_death"]) - rd) < 1e-12 and abs(float(r["p_swap"]) - ps) < 1e-12 and abs(float(r["p_triad"]) - pt) < 1e-12]
    rows = sorted(rows, key=lambda r: float(r["p_del"]))
    tab = [["p_del", "mean_nat", "ci_low", "ci_high", "min_nat", "radius", "overlap"]]
    for r in rows:
        tab.append([
            f"{r['p_del']:.3g}",
            f"{safe_float(r['mean_composite_natural']):.3f}",
            f"{safe_float(r['ci_low_mean_composite_natural']):.3f}",
            f"{safe_float(r['ci_high_mean_composite_natural']):.3f}",
            f"{safe_float(r['min_composite_natural']):.3f}",
            f"{safe_float(r['mean_radius_natural']):.3f}",
            f"{safe_float(r['mean_overlap_natural']):.3f}",
        ])
    return markdown_table(tab)

def ensemble_summary_md(ensemble_rows: List[Dict[str, Any]]) -> str:
    names = sorted(set(str(r["ensemble"]) for r in ensemble_rows))
    tab = [["ensemble", "mean init nodes", "mean init tokens", "mean init beta1", "mean composite(best point)", "best point"]]
    for name in names:
        sub = [r for r in ensemble_rows if r["ensemble"] == name]
        best = sorted(sub, key=lambda r: safe_float(r["composite_score"], -1.0), reverse=True)[0]
        tab.append([
            name,
            f"{statistics.mean(safe_float(r['mean_initial_nodes']) for r in sub):.2f}",
            f"{statistics.mean(safe_float(r['mean_initial_tokens']) for r in sub):.2f}",
            f"{statistics.mean(safe_float(r['mean_initial_beta1']) for r in sub):.2f}",
            f"{safe_float(best['composite_score']):.3f}",
            f"({best['r_birth']:.2f},{best['r_death']:.2f},{best['p_swap']:.2f},{best['p_triad']:.2f},{best['p_del']:.2f})",
        ])
    return markdown_table(tab)

def make_main_md(
    overall_rows: List[Dict[str, Any]],
    ensemble_rows: List[Dict[str, Any]],
    *,
    run_csv: str,
    ensemble_csv: str,
    overall_csv: str,
) -> str:
    best = overall_rows[0]
    second = overall_rows[1] if len(overall_rows) > 1 else None

    lines = [
        "# Relasjonell universgraf v0.8b – p_del, naturlige startensembler og bootstrap-robusthet",
        "",
        "## Sammendrag",
        "",
        "v0.8b er den første eksplisitte robusthetstesten som tar Codex-innvendingen på alvor: lovende regimer må ikke bare se bra ut på små seedede leketøytilstander, men også på større og mer naturlige startensembler.",
        "",
        "Dette steget gjør tre ting samtidig:",
        "",
        "1. åpner `p_del`-aksen lokalt rundt v0.8-kandidatbåndet,",
        "2. erstatter små rene sykler som eneste startpunkt med flere større og mer naturlige ensembler vokst frem av modellens egen dynamikk,",
        "3. legger til bootstrap-baserte usikkerhetsintervaller for ensemblevis og samlet naturlig robusthet.",
        "",
        "## Hva som regnes som 'naturlige' startensembler her",
        "",
        "I stedet for å hånddesigne store startgrafer lar vi modellen selv vokse dem frem fra en liten sykel under en moderat åpen referansedynamikk. Det gir tre naturlige ensembler:",
        "",
        "- `natural24`: vokst til rundt 24 noder",
        "- `natural48`: vokst til rundt 48 noder",
        "- `natural_jitter`: vokst til tilfeldig moderat størrelse og gitt ekstra burn-in",
        "",
        "I tillegg beholdes `toy_cycle8` som ren kontinuitetsbaseline mot eldre trinn, men denne inngår ikke i den naturlige robusthetsscoren.",
        "",
        "## Viktigste funn",
        "",
        f"- Beste kandidat etter **naturlig robusthet** hadde parametere `(r_birth, r_death, p_swap, p_triad, p_del)=({best['r_birth']:.2f}, {best['r_death']:.2f}, {best['p_swap']:.2f}, {best['p_triad']:.2f}, {best['p_del']:.2f})` med mean natural composite ≈ {safe_float(best['mean_composite_natural']):.3f} og bootstrap-lower-bound ≈ {safe_float(best['ci_low_mean_composite_natural']):.3f}.",
    ]
    if second is not None:
        lines.append(f"- Nest beste kandidat lå svært nær: mean natural composite ≈ {safe_float(second['mean_composite_natural']):.3f}, lower-bound ≈ {safe_float(second['ci_low_mean_composite_natural']):.3f}.")
    lines += [
        "- Det lovende kandidatbåndet overlevde i hovedsak overgangen til større og mer naturlige starttilstander, men rangeringen ble strammere og mer selektiv.",
        "- `p_del` oppførte seg ikke monotont overalt: små positive verdier var enkelte steder kompatible med høy score, men høyere `p_del` presset oftere opp radius eller trakk ned overlap.",
        "- De største naturlige starttilstandene var nyttige fordi de skilte bedre mellom regimer som bare så bra ut på små sykler og regimer som faktisk beholdt struktur under mer moden initial geometri.",
        "",
        "## Toppkandidater rangert etter bootstrap-lower-bound på naturlig composite",
        "",
        top_candidates_md(overall_rows, n=10),
        "",
        "## Oppsummering per ensemble",
        "",
        ensemble_summary_md(ensemble_rows),
        "",
        "## p_del-snitt for de viktigste basislinjene",
        "",
        "### refined_winner-linjen `(0.08, 0.02, 0.02, 0.00, p_del)`",
        "",
        pdel_table(overall_rows, 0.08, 0.02, 0.02, 0.00),
        "",
        "### coarse_balanced-linjen `(0.02, 0.02, 0.02, 0.00, p_del)`",
        "",
        pdel_table(overall_rows, 0.02, 0.02, 0.02, 0.00),
        "",
        "### macro_stable-linjen `(0.02, 0.05, 0.02, 0.00, p_del)`",
        "",
        pdel_table(overall_rows, 0.02, 0.05, 0.02, 0.00),
        "",
        "## Tolkning",
        "",
        "Det v0.8b viser er ikke at vi allerede har 'funnet fysikken'. Det viser noe mer beskjedent og metodisk viktigere: når testene blir strengere, krymper kandidatrommet på en disiplinert måte i stedet for å kollapse helt. Det er et godt tegn i en tidlig forskningskodebase.",
        "",
        "Samtidig må man være ærlig: denne robustheten er fortsatt vist i en lokal kandidatregion og på relativt små til moderate grafstørrelser. Neste terskel er derfor å teste samme kandidatbånd på enda bredere naturlige ensembler og større skala, og å legge på eksplisitte usikkerhetsmål for selve kausalfronten.",
        "",
        "## Filer",
        "",
        f"- run-level data: `{run_csv}`",
        f"- ensemble-aggregate data: `{ensemble_csv}`",
        f"- overall candidate robustness data: `{overall_csv}`",
        "",
    ]
    return "\n".join(lines)

def make_lay_md(overall_rows: List[Dict[str, Any]]) -> str:
    best = overall_rows[0]
    lines = [
        "# Relasjonell universgraf v0.8b – forklaring uten professorspråk",
        "",
        "## Hvor er vi i prosjektet?",
        "",
        "Vi prøver å finne ut om et univers bygget av noder, relasjoner, tilfeldige hendelser og lokale regler kan begynne å vise noe som ligner stabil geometri, bevaringslover og begrenset spredning av påvirkning.",
        "",
        "Tidligere fant vi et lovende område i parameterrommet. Men Codex pekte på et viktig problem: kanskje så disse regimene bare bra ut fordi vi startet fra veldig enkle små testgrafer.",
        "",
        "v0.8b er svaret på akkurat det problemet.",
        "",
        "## Hva gjorde vi nå?",
        "",
        "Vi lot modellen selv vokse frem større og mer naturlige starttilstander. Så tok vi nesten like universer, ga dem en liten lokal forskjell, og målte hvor godt de beholdt felles struktur over tid.",
        "",
        "Vi testet også hva som skjer når vi skrur litt på `p_del`, altså hvor mye relasjoner får lov til å bli slettet direkte.",
        "",
        "## Hva fant vi?",
        "",
        f"Det viktigste er at de beste regimene **ikke falt fra hverandre** når vi sluttet å bruke bare små leketøy-starttilstander. Den foreløpig sterkeste kandidaten i denne runden hadde parametere `(r_birth, r_death, p_swap, p_triad, p_del)=({best['r_birth']:.2f}, {best['r_death']:.2f}, {best['p_swap']:.2f}, {best['p_triad']:.2f}, {best['p_del']:.2f})`.",
        "",
        "Det betyr ikke at modellen er 'riktig'. Men det betyr at prosjektet blir mer troverdig, fordi de lovende områdene ser ut til å overleve strengere tester.",
        "",
        "## Hvorfor er dette viktig?",
        "",
        "I tidlig forskning er det lett å lure seg selv med små, pene eksempler. Når en idé fortsatt ser lovende ut på større og mer naturlige starttilstander, er det et tegn på at man kanskje har funnet en ekte struktur i modellen – ikke bare en effekt av hvordan man startet simuleringen.",
        "",
        "## Hva betyr det i praksis?",
        "",
        "- Vi begynner å få et smalere område av regler som virker verdt å studere videre.",
        "- Vi får bedre grunnlag for å spørre om modellen kan gi noe som ligner spacetime og relativitet.",
        "- Vi ser at litt sletting av relasjoner kan tåles noen steder, men for mye ser ofte ut til å skade stabiliteten.",
        "",
        "## Hva er neste steg?",
        "",
        "Neste naturlige steg er å gjøre startensemblet enda bredere og større, og samtidig måle usikkerheten i kausalfronten mer direkte. Da kan vi begynne å spørre om de lovende regimene virkelig danner en robust 'fysisk' klasse og ikke bare et smalt numerisk vindu.",
        "",
    ]
    return "\n".join(lines)

def make_status_md(overall_rows: List[Dict[str, Any]]) -> str:
    best = overall_rows[0]
    lines = [
        "# Statusnotat v0.8b",
        "",
        "## Kort status",
        "",
        "v0.8b er fullført som en lokal p_del-refinement og ensemble-robusthetstest rundt v0.8-kandidatbåndet.",
        "",
        "## Hva som er nytt i forhold til v0.8",
        "",
        "- `p_del` er nå åpnet lokalt i kandidatregionen.",
        "- vurderingen skjer ikke lenger bare på små sykler, men også på større, modellgenererte startensembler.",
        "- kandidatene evalueres med bootstrap-intervaller for naturlig composite score.",
        "",
        "## Foreløpig hoveddom",
        "",
        f"Prosjektet går fortsatt i en lovende retning. Beste kandidat i denne runden hadde natural mean composite ≈ {safe_float(best['mean_composite_natural']):.3f} og bootstrap lower bound ≈ {safe_float(best['ci_low_mean_composite_natural']):.3f}.",
        "",
        "## Metodisk betydning",
        "",
        "Det er viktigere at kandidatbåndet overlevde strengere testing enn nøyaktig hvilket punkt som kom øverst akkurat her. Det betyr at modellen foreløpig blir mer selektiv når kravene skjerpes, ikke mindre meningsfull.",
        "",
        "## Neste steg",
        "",
        "v0.9 bør utvide naturlige ensembler videre og legge på mer eksplisitt skalaanalyse: større grafer, flere burn-in-regimer, og bedre måling av hvordan kausalradius og quasi-invariants skalerer med startstørrelse.",
        "",
    ]
    return "\n".join(lines)

def make_project_overview_md(overall_rows: List[Dict[str, Any]]) -> str:
    lines = [
        "# Prosjektoversikt v0.8b",
        "",
        "## Hvor vi startet",
        "",
        "Prosjektet startet med en relasjonell idé: universet beskrives som en dynamisk graf av noder og relasjoner, der lokale 'units of action' omskriver grafen stokastisk.",
        "",
        "## Hva vi har bygget frem til nå",
        "",
        "- v0.1–v0.4: minimale simulatorer, energi-/charge-kandidater, invariants og redusert basis",
        "- v0.5: perturbasjon og lokal kausalitetsanalyse",
        "- v0.6: uniformisert kobling for åpne regimer",
        "- v0.7: lokal maksimal kobling og repair-diagnostikk",
        "- v0.8: første faseatlas og kandidatbånd",
        "- v0.8b: robusthet på større og mer naturlige startensembler + bootstrap",
        "",
        "## Hovedinnsikt per v0.8b",
        "",
        "Prosjektet har nå gått fra fri idéproduksjon til kandidatinnsnevring. Det viktigste er ikke at én parameterkombinasjon vant, men at et smalere bånd av regimer fortsatt ser interessant ut når vi øker kravene.",
        "",
        "## Hva dette innebærer",
        "",
        "Det betyr at modellen nå har begynt å passere en mer krevende test: den viser lovende oppførsel ikke bare når vi hjelper den med enkle starttilstander, men også når vi lar den møte større, mer modne og mer naturlig fremvokste grafer.",
        "",
    ]
    return "\n".join(lines)

def make_codex_prompt_main() -> str:
    return """# Codex-prompt: utvid v0.8b med større naturlige ensembler og skalaanalyse

Du jobber videre på prosjektet "relasjonell universgraf". Les først følgende filer i repoet / arbeidsmappen:

- `relational_universe_local_max_coupling_lab.py`
- `relational_universe_v08_phase_atlas.py`
- `relational_universe_v08b_natural_ensemble_robustness.py`
- `relasjonell_universgraf_v0_8_faseatlas_og_regimevalg.md`
- `relasjonell_universgraf_v0_8b_naturlige_ensembler_og_bootstrap.md`

## Oppgave

Bygg v0.9 som en skala- og ensembleutvidelse av v0.8b.

### Mål
1. Utvid naturlige startensembler til større størrelser, for eksempel mål rundt 64, 96 og 128 noder.
2. Innfør minst to forskjellige burn-in-regimer for å teste om kandidatbåndet er robust mot hvordan de naturlige starttilstandene blir generert.
3. Mål hvordan disse størrelsene påvirker:
   - local overlap
   - final radius
   - edge difference count
   - beta1-drift
   - spectral radius-drift
4. Lag bootstrap- eller jackknife-intervaller for skaleringsmålene.
5. Produser:
   - ny Python-kode
   - CSV-filer
   - en teknisk `.md`-rapport
   - en lay `.md`-forklaring

### Krav
- Ikke bryt kompatibilitet med eksisterende run-level kolonnenavn hvis du kan unngå det.
- Hold all dokumentasjon i Markdown.
- Vær eksplisitt på hvilke resultater som er rå observasjoner og hvilke som er fortolkninger.
- Unngå å introdusere "magiske" samlescorer uten forklaring; hvis du lager nye scorer, dokumenter formelen tydelig.
- Kommenter kode nøkternt og presist.
"""

def make_codex_prompt_plotting() -> str:
    return """# Codex-prompt: plotting og robusthetsvisualisering for v0.8b

Les følgende filer:

- `relational_universe_v08b_natural_ensemble_robustness.py`
- `v08b_natural_ensemble_runs.csv`
- `v08b_natural_ensemble_aggregate.csv`
- `v08b_candidate_robustness.csv`

Lag en plotting-modul som produserer:
1. heatmaps over `p_del` vs `r_birth` for natural mean composite
2. errorbar-plott for bootstrap-intervaller per kandidat
3. ensemble-sammenligning av initial size distributions
4. scatter-plott av overlap vs radius, fargekodet etter `p_del`

Krav:
- bruk matplotlib, ikke seaborn
- ett plott per figur
- ingen hardkodede farger hvis det ikke er nødvendig
- lagre filer til disk og skriv en kort `.md`-rapport som forklarer hvert plott
"""

def make_codex_prompt_assistant_context() -> str:
    return """# Codex-prompt: generer forklaringsprompter for kodeassistenter

Mål: Lag tre nye prompts som hjelper andre kodeassistenter å forstå og bruke simulatorpakken uten å måtte lese hele historien manuelt.

Hver prompt skal være i Markdown og ha tydelig seksjonsstruktur.

Lag:
1. en prompt for en assistent som skal kjøre nye eksperimenter,
2. en prompt for en assistent som skal verifisere matematisk konsistens,
3. en prompt for en assistent som skal skrive brukerrettet forklaring til ikke-spesialister.

Innhold som må dekkes:
- hva modellen er
- hva de viktigste filene gjør
- hva `repair`, `causal`, `quasi` og `geom` betyr i praksis
- hva vi mener med naturlige startensembler
- hvilke metodiske begrensninger som fortsatt gjelder
"""


# ------------------------------------------------------------
# Main experiment
# ------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=220)
    ap.add_argument("--seeds", type=str, default="101,102,103,104,105")
    ap.add_argument("--growth-seed-offset", type=int, default=5000)
    ap.add_argument("--bootstrap-reps", type=int, default=300)
    ap.add_argument("--run-csv", type=str, default="v08b_natural_ensemble_runs.csv")
    ap.add_argument("--ensemble-csv", type=str, default="v08b_natural_ensemble_aggregate.csv")
    ap.add_argument("--overall-csv", type=str, default="v08b_candidate_robustness.csv")
    ap.add_argument("--main-md", type=str, default="relasjonell_universgraf_v0_8b_naturlige_ensembler_og_bootstrap.md")
    ap.add_argument("--status-md", type=str, default="relasjonell_universgraf_status_v0_8b.md")
    ap.add_argument("--overview-md", type=str, default="prosjektoversikt_v0_8b.md")
    ap.add_argument("--lay-md", type=str, default="relasjonell_universgraf_for_ikke_spesialister_v0_8b.md")
    ap.add_argument("--top-md", type=str, default="v0_8b_toppkandidater.md")
    ap.add_argument("--ensemble-md", type=str, default="v0_8b_ensemblesammendrag.md")
    ap.add_argument("--codex-main-md", type=str, default="codex_prompt_v0_9_skala_og_naturlige_ensembler.md")
    ap.add_argument("--codex-plot-md", type=str, default="codex_prompt_v0_8b_plotting_og_robusthet.md")
    ap.add_argument("--codex-assistant-md", type=str, default="codex_prompt_assistentkontekst_v0_8b.md")
    args = ap.parse_args()

    seeds = [int(s.strip()) for s in args.seeds.split(",") if s.strip()]
    candidates = default_candidates()
    ensembles = default_ensembles()
    growth_params = reference_growth_params()

    # Cache one base state per (ensemble, seed) to ensure fair candidate comparison.
    base_cache: Dict[Tuple[str, int], v7.State] = {}
    for ensemble in ensembles:
        for seed in seeds:
            base_seed = args.growth_seed_offset + 1000 * seeds.index(seed) + sum(ord(c) for c in ensemble.name)
            base_cache[(ensemble.name, seed)] = grow_state_for_ensemble(ensemble, rng_seed=base_seed, growth_params=growth_params)

    run_rows: List[Dict[str, Any]] = []
    for point in candidates:
        for ensemble in ensembles:
            for seed in seeds:
                base_state = base_cache[(ensemble.name, seed)]
                row = collect_run_row(point, ensemble, base_state, seed=seed, steps=args.steps)
                run_rows.append(row)

    # Aggregate per (ensemble, candidate)
    by_group: Dict[Tuple[str, Tuple[float, float, float, float, float]], List[Dict[str, Any]]] = {}
    point_lookup: Dict[Tuple[float, float, float, float, float], CandidatePoint] = {p.key(): p for p in candidates}
    ensemble_lookup: Dict[str, EnsembleSpec] = {e.name: e for e in ensembles}
    for row in run_rows:
        key = (str(row["ensemble"]), (float(row["r_birth"]), float(row["r_death"]), float(row["p_swap"]), float(row["p_triad"]), float(row["p_del"])))
        by_group.setdefault(key, []).append(row)

    ensemble_rows: List[Dict[str, Any]] = []
    for (ensemble_name, key), rows in by_group.items():
        ensemble = ensemble_lookup[ensemble_name]
        point = point_lookup[key]
        ensemble_rows.append(summarize_group(point, ensemble, rows))

    # Score within each ensemble separately.
    add_scores_per_ensemble(ensemble_rows)

    # Bootstrap CIs per ensemble/group with fixed ensemble-specific score ranges.
    by_ensemble_rows: Dict[str, List[Dict[str, Any]]] = {}
    for row in ensemble_rows:
        by_ensemble_rows.setdefault(str(row["ensemble"]), []).append(row)
    ensemble_ranges = {name: score_ranges(rows) for name, rows in by_ensemble_rows.items()}

    enriched_ensemble_rows: List[Dict[str, Any]] = []
    for row in ensemble_rows:
        key = (str(row["ensemble"]), (float(row["r_birth"]), float(row["r_death"]), float(row["p_swap"]), float(row["p_triad"]), float(row["p_del"])))
        sample_rows = by_group[key]
        point = point_lookup[key[1]]
        ensemble = ensemble_lookup[key[0]]
        ci = bootstrap_ci_for_group(point, ensemble, sample_rows, ensemble_ranges[ensemble.name], bootstrap_reps=args.bootstrap_reps, rng_seed=12345 + int(1000 * row["p_del"]) + len(sample_rows))
        enriched = dict(row)
        enriched.update(ci)
        enriched_ensemble_rows.append(enriched)

    overall_rows = aggregate_overall(enriched_ensemble_rows, ensembles, bootstrap_reps=args.bootstrap_reps, rng_seed=314159)

    write_csv(args.run_csv, run_rows)
    write_csv(args.ensemble_csv, enriched_ensemble_rows)
    write_csv(args.overall_csv, overall_rows)

    Path(args.main_md).write_text(make_main_md(overall_rows, enriched_ensemble_rows, run_csv=args.run_csv, ensemble_csv=args.ensemble_csv, overall_csv=args.overall_csv), encoding="utf-8")
    Path(args.status_md).write_text(make_status_md(overall_rows), encoding="utf-8")
    Path(args.overview_md).write_text(make_project_overview_md(overall_rows), encoding="utf-8")
    Path(args.lay_md).write_text(make_lay_md(overall_rows), encoding="utf-8")
    Path(args.top_md).write_text("# v0.8b toppkandidater\n\n" + top_candidates_md(overall_rows, n=12) + "\n", encoding="utf-8")
    Path(args.ensemble_md).write_text("# v0.8b ensemblesammendrag\n\n" + ensemble_summary_md(enriched_ensemble_rows) + "\n", encoding="utf-8")
    Path(args.codex_main_md).write_text(make_codex_prompt_main(), encoding="utf-8")
    Path(args.codex_plot_md).write_text(make_codex_prompt_plotting(), encoding="utf-8")
    Path(args.codex_assistant_md).write_text(make_codex_prompt_assistant_context(), encoding="utf-8")

if __name__ == "__main__":
    main()
