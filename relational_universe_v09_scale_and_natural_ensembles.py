#!/usr/bin/env python3
"""relational_universe_v09_scale_and_natural_ensembles.py

v0.9: scale analysis on larger natural ensembles with multiple burn-in regimes.

This step extends v0.8b in the direction suggested by the project's internal
critique: promising regimes must survive contact with larger and more natural
start ensembles, and we should measure how key observables scale with size.

Main additions
--------------
1. Evaluate a focused candidate band from v0.8b on larger natural ensembles.
2. Introduce multiple burn-in regimes (light and deep) at each target size.
3. Use event budgets proportional to initial size for fairer cross-scale runs.
4. Estimate scale diagnostics for:
   - radius / front spread
   - local overlap / repair quality
   - quasi-invariant preservation
5. Add bootstrap intervals for mean score and scale slopes.
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
import zipfile

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08_phase_atlas as v8
import relational_universe_v08b_natural_ensemble_robustness as v08b


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


def ensure_parent_dir(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    path = str(path)
    ensure_parent_dir(path)
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


def write_text(path: str | Path, content: str) -> None:
    ensure_parent_dir(path)
    Path(path).write_text(content, encoding="utf-8")


def linear_fit(xs: Sequence[float], ys: Sequence[float]) -> Tuple[float, float]:
    pts = [(float(x), float(y)) for x, y in zip(xs, ys) if math.isfinite(float(x)) and math.isfinite(float(y))]
    if len(pts) < 2:
        return float("nan"), float("nan")
    xbar = statistics.mean(x for x, _ in pts)
    ybar = statistics.mean(y for _, y in pts)
    sxx = sum((x - xbar) ** 2 for x, _ in pts)
    if sxx <= 0.0:
        return float("nan"), float("nan")
    sxy = sum((x - xbar) * (y - ybar) for x, y in pts)
    slope = sxy / sxx
    intercept = ybar - slope * xbar
    return float(slope), float(intercept)


def objective_score(value: float, lo: float, hi: float, higher_better: bool = True) -> float:
    return v8.objective_score(value, lo, hi, higher_better)


def average_defined(values: Iterable[float]) -> float:
    return v8.average_defined(list(values))


# ------------------------------------------------------------
# Candidate and ensemble definitions
# ------------------------------------------------------------

@dataclass(frozen=True)
class ScaleCandidate:
    name: str
    r_birth: float
    r_death: float
    p_swap: float
    p_triad: float
    p_del: float

    def key(self) -> Tuple[float, float, float, float, float]:
        return (self.r_birth, self.r_death, self.p_swap, self.p_triad, self.p_del)


@dataclass(frozen=True)
class ScaleEnsemble:
    name: str
    target_nodes: int
    burnin_label: str  # light / deep
    initial_cycle: int
    initial_tokens: int
    burnin_steps: int
    extra_burnin_low: int
    extra_burnin_high: int


def default_candidates() -> List[ScaleCandidate]:
    # Focused diversity band from v0.8b top region plus one higher-birth control.
    return [
        ScaleCandidate("band_best", 0.02, 0.00, 0.02, 0.00, 0.01),
        ScaleCandidate("balanced_pdel", 0.02, 0.02, 0.02, 0.00, 0.01),
        ScaleCandidate("triad_runner", 0.02, 0.02, 0.02, 0.02, 0.00),
        ScaleCandidate("macro_stable", 0.02, 0.05, 0.02, 0.00, 0.01),
        ScaleCandidate("high_birth", 0.08, 0.02, 0.02, 0.00, 0.01),
    ]


def default_scale_ensembles() -> List[ScaleEnsemble]:
    return [
        ScaleEnsemble("natural24_light", 24, "light", 10, 5, 420, 20, 80),
        ScaleEnsemble("natural24_deep", 24, "deep", 10, 5, 820, 180, 320),
        ScaleEnsemble("natural48_light", 48, "light", 12, 6, 960, 40, 140),
        ScaleEnsemble("natural48_deep", 48, "deep", 12, 6, 1600, 220, 380),
        ScaleEnsemble("natural96_light", 96, "light", 14, 7, 2200, 80, 180),
        ScaleEnsemble("natural96_deep", 96, "deep", 14, 7, 3400, 320, 520),
    ]


def to_v08b_spec(e: ScaleEnsemble) -> v08b.EnsembleSpec:
    return v08b.EnsembleSpec(
        name=e.name,
        kind="natural_grown",
        initial_cycle=e.initial_cycle,
        initial_tokens=e.initial_tokens,
        target_nodes=e.target_nodes,
        burnin_steps=e.burnin_steps,
        extra_burnin_low=e.extra_burnin_low,
        extra_burnin_high=e.extra_burnin_high,
        include_in_natural_score=1,
    )


def candidate_to_params(point: ScaleCandidate) -> v7.Params:
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
# Growth and coupled-run helpers
# ------------------------------------------------------------

def reference_growth_params() -> v7.Params:
    return v08b.reference_growth_params()


def run_single_candidate_from_base(point: ScaleCandidate, ensemble: ScaleEnsemble, base_state: v7.State, *, seed: int, steps: int) -> Dict[str, Any]:
    params = candidate_to_params(point)
    res = v08b.run_coupled_from_base(
        base_state,
        params=params,
        seed=seed,
        steps=steps,
        perturbation="local_swap",
        local_coupling="maximal",
        log_every=max(20, min(120, steps // 6)),
    )
    hm = res["headline_metrics"]
    last = res["log_rows"][-1]
    init = res["initial_control_features"]
    return {
        "candidate_name": point.name,
        "r_birth": point.r_birth,
        "r_death": point.r_death,
        "p_swap": point.p_swap,
        "p_triad": point.p_triad,
        "p_del": point.p_del,
        "ensemble": ensemble.name,
        "burnin_label": ensemble.burnin_label,
        "target_nodes": ensemble.target_nodes,
        "seed": seed,
        "steps": steps,
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


def summarize_group(point: ScaleCandidate, ensemble: ScaleEnsemble, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "candidate_name": point.name,
        "r_birth": point.r_birth,
        "r_death": point.r_death,
        "p_swap": point.p_swap,
        "p_triad": point.p_triad,
        "p_del": point.p_del,
        "ensemble": ensemble.name,
        "burnin_label": ensemble.burnin_label,
        "target_nodes": ensemble.target_nodes,
        "runs": len(rows),
    }
    for key in RUN_KEYS:
        vals = [safe_float(r.get(key), default=float("nan")) for r in rows]
        vals_f = [v for v in vals if math.isfinite(v)]
        out[f"mean_{key}"] = float(statistics.mean(vals_f)) if vals_f else float("nan")
        out[f"sd_{key}"] = float(statistics.pstdev(vals_f)) if len(vals_f) >= 2 else 0.0
    return out


# ------------------------------------------------------------
# Scoring and scale diagnostics
# ------------------------------------------------------------

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
            parts.append(v8.objective_score(safe_float(row.get(key), default=float("nan")), lo, hi, higher_better=hb))
        score = v8.average_defined(parts)
        out[f"{family}_score"] = score
        if math.isfinite(score):
            comp += v8.WEIGHTS[family] * score
            weight_total += v8.WEIGHTS[family]
    out["composite_score"] = (comp / weight_total) if weight_total > 0 else float("nan")
    return out


def add_scores_to_group_rows(group_rows: List[Dict[str, Any]]) -> None:
    ranges = score_ranges(group_rows)
    for row in group_rows:
        row.update(score_row_from_ranges(row, ranges))


def burnin_sensitivity(group_rows: List[Dict[str, Any]]) -> float:
    by_size: Dict[int, Dict[str, float]] = {}
    for row in group_rows:
        size = int(round(safe_float(row["target_nodes"])))
        lab = str(row["burnin_label"])
        by_size.setdefault(size, {})[lab] = safe_float(row.get("composite_score"), float("nan"))
    diffs = []
    for size, labs in by_size.items():
        if "light" in labs and "deep" in labs and math.isfinite(labs["light"]) and math.isfinite(labs["deep"]):
            diffs.append(abs(labs["light"] - labs["deep"]))
    return float(statistics.mean(diffs)) if diffs else float("nan")


def fit_scale_metrics(group_rows: List[Dict[str, Any]]) -> Dict[str, float]:
    xs_lnN = []
    ys_ln_radius = []
    ys_overlap = []
    ys_quasi = []
    ys_beta1_ln = []
    ys_radius_over_logN = []
    ys_radius_over_sqrtN = []
    for row in group_rows:
        N = safe_float(row.get("mean_initial_nodes"), float("nan"))
        R = safe_float(row.get("mean_final_radius_control"), float("nan"))
        O = safe_float(row.get("mean_avg_local_overlap"), float("nan"))
        Q = safe_float(row.get("quasi_score"), float("nan"))
        B = safe_float(row.get("mean_abs_delta_beta1"), float("nan"))
        if N > 1 and math.isfinite(R):
            xs_lnN.append(math.log(N))
            ys_ln_radius.append(math.log(R + 1.0))
            ys_overlap.append(O)
            ys_quasi.append(Q)
            ys_beta1_ln.append(math.log(B + 1.0))
            ys_radius_over_logN.append(R / max(math.log(N + 1.0), 1e-9))
            ys_radius_over_sqrtN.append(R / math.sqrt(N))
    slope_alpha, intercept_alpha = linear_fit(xs_lnN, ys_ln_radius)
    slope_overlap, intercept_overlap = linear_fit(xs_lnN, ys_overlap)
    slope_quasi, intercept_quasi = linear_fit(xs_lnN, ys_quasi)
    slope_beta1, intercept_beta1 = linear_fit(xs_lnN, ys_beta1_ln)
    return {
        "radius_alpha": slope_alpha,
        "radius_alpha_intercept": intercept_alpha,
        "overlap_vs_logN_slope": slope_overlap,
        "overlap_vs_logN_intercept": intercept_overlap,
        "quasi_vs_logN_slope": slope_quasi,
        "quasi_vs_logN_intercept": intercept_quasi,
        "beta1_drift_alpha": slope_beta1,
        "beta1_drift_alpha_intercept": intercept_beta1,
        "mean_radius_over_logN": float(statistics.mean(ys_radius_over_logN)) if ys_radius_over_logN else float("nan"),
        "mean_radius_over_sqrtN": float(statistics.mean(ys_radius_over_sqrtN)) if ys_radius_over_sqrtN else float("nan"),
    }


def bootstrap_candidate_summary(
    point: ScaleCandidate,
    ensembles: List[ScaleEnsemble],
    run_rows: List[Dict[str, Any]],
    ranges: Dict[str, Tuple[float, float, bool]],
    *,
    reps: int,
    rng_seed: int,
) -> Dict[str, float]:
    rng = random.Random(rng_seed)
    boots_mean_comp = []
    boots_radius_alpha = []
    boots_overlap_slope = []
    boots_quasi_slope = []
    boots_burnin_sens = []

    by_ens: Dict[str, List[Dict[str, Any]]] = {}
    for row in run_rows:
        by_ens.setdefault(str(row["ensemble"]), []).append(row)

    for _ in range(reps):
        sample_group_rows = []
        for ens in ensembles:
            rows = by_ens.get(ens.name, [])
            if not rows:
                continue
            sample = [rows[rng.randrange(len(rows))] for _ in range(len(rows))]
            agg = summarize_group(point, ens, sample)
            agg.update(score_row_from_ranges(agg, ranges))
            sample_group_rows.append(agg)
        if not sample_group_rows:
            continue
        boots_mean_comp.append(float(statistics.mean(safe_float(r["composite_score"], float("nan")) for r in sample_group_rows)))
        sc = fit_scale_metrics(sample_group_rows)
        boots_radius_alpha.append(sc["radius_alpha"])
        boots_overlap_slope.append(sc["overlap_vs_logN_slope"])
        boots_quasi_slope.append(sc["quasi_vs_logN_slope"])
        boots_burnin_sens.append(burnin_sensitivity(sample_group_rows))

    return {
        "ci_low_mean_composite": quantile(boots_mean_comp, 0.025),
        "ci_high_mean_composite": quantile(boots_mean_comp, 0.975),
        "ci_low_radius_alpha": quantile(boots_radius_alpha, 0.025),
        "ci_high_radius_alpha": quantile(boots_radius_alpha, 0.975),
        "ci_low_overlap_vs_logN": quantile(boots_overlap_slope, 0.025),
        "ci_high_overlap_vs_logN": quantile(boots_overlap_slope, 0.975),
        "ci_low_quasi_vs_logN": quantile(boots_quasi_slope, 0.025),
        "ci_high_quasi_vs_logN": quantile(boots_quasi_slope, 0.975),
        "ci_low_burnin_sensitivity": quantile(boots_burnin_sens, 0.025),
        "ci_high_burnin_sensitivity": quantile(boots_burnin_sens, 0.975),
    }


def candidate_summary_rows(
    candidates: List[ScaleCandidate],
    ensembles: List[ScaleEnsemble],
    run_rows: List[Dict[str, Any]],
    group_rows: List[Dict[str, Any]],
    *,
    bootstrap_reps: int,
    bootstrap_seed: int,
) -> List[Dict[str, Any]]:
    ranges = score_ranges(group_rows)
    out: List[Dict[str, Any]] = []
    for i, point in enumerate(candidates):
        sub_group = [r for r in group_rows if r["candidate_name"] == point.name]
        sub_runs = [r for r in run_rows if r["candidate_name"] == point.name]
        if not sub_group:
            continue
        mean_comp = statistics.mean(safe_float(r["composite_score"], float("nan")) for r in sub_group)
        min_comp = min(safe_float(r["composite_score"], float("nan")) for r in sub_group)
        mean_repair = statistics.mean(safe_float(r["repair_score"], float("nan")) for r in sub_group)
        mean_causal = statistics.mean(safe_float(r["causal_score"], float("nan")) for r in sub_group)
        mean_quasi = statistics.mean(safe_float(r["quasi_score"], float("nan")) for r in sub_group)
        mean_geom = statistics.mean(safe_float(r["geom_score"], float("nan")) for r in sub_group)
        scale = fit_scale_metrics(sub_group)
        burn_sens = burnin_sensitivity(sub_group)
        boot = bootstrap_candidate_summary(point, ensembles, sub_runs, ranges, reps=bootstrap_reps, rng_seed=bootstrap_seed + 1000 * i)
        out.append({
            "candidate_name": point.name,
            "r_birth": point.r_birth,
            "r_death": point.r_death,
            "p_swap": point.p_swap,
            "p_triad": point.p_triad,
            "p_del": point.p_del,
            "group_rows": len(sub_group),
            "run_rows": len(sub_runs),
            "mean_composite": mean_comp,
            "min_composite": min_comp,
            "mean_repair": mean_repair,
            "mean_causal": mean_causal,
            "mean_quasi": mean_quasi,
            "mean_geom": mean_geom,
            "burnin_sensitivity": burn_sens,
            **scale,
            **boot,
        })
    # ranking: first by lower CI on composite, then by smaller radius alpha, then by smaller burn-in sensitivity
    out.sort(key=lambda r: (
        safe_float(r["ci_low_mean_composite"], -1.0),
        -safe_float(r["radius_alpha"], float("inf")),
        -safe_float(r["burnin_sensitivity"], float("inf"))
    ), reverse=True)
    return out


# ------------------------------------------------------------
# Ensemble generation / execution
# ------------------------------------------------------------

def build_base_states(ensembles: List[ScaleEnsemble], growth_seeds: Sequence[int]) -> Tuple[Dict[Tuple[str, int], v7.State], List[Dict[str, Any]]]:
    out: Dict[Tuple[str, int], v7.State] = {}
    meta_rows: List[Dict[str, Any]] = []
    growth_params = reference_growth_params()
    for ens in ensembles:
        spec = to_v08b_spec(ens)
        for s in growth_seeds:
            state = v08b.grow_state_for_ensemble(spec, rng_seed=int(s), growth_params=growth_params)
            out[(ens.name, int(s))] = state
            feats = v7.feature_row(state)
            meta_rows.append({
                "ensemble": ens.name,
                "burnin_label": ens.burnin_label,
                "target_nodes": ens.target_nodes,
                "growth_seed": int(s),
                "initial_nodes": safe_float(feats.get("nodes"), float("nan")),
                "initial_tokens": safe_float(feats.get("tokens"), float("nan")),
                "initial_beta1": safe_float(feats.get("beta1"), float("nan")),
                "initial_triangles": safe_float(feats.get("triangles"), float("nan")),
                "initial_spectral_radius": safe_float(feats.get("spectral_radius"), float("nan")),
                "initial_dim_proxy": safe_float(feats.get("dim_proxy"), float("nan")),
            })
    return out, meta_rows


def compute_steps_for_state(state: v7.State, steps_per_node: float, min_steps: int, max_steps: int) -> int:
    n = max(1.0, float(state.g.num_nodes()))
    steps = int(round(steps_per_node * n))
    steps = max(int(min_steps), steps)
    steps = min(int(max_steps), steps)
    return steps


def run_v09(
    candidates: List[ScaleCandidate],
    ensembles: List[ScaleEnsemble],
    growth_seeds: Sequence[int],
    *,
    steps_per_node: float,
    min_steps: int,
    max_steps: int,
    bootstrap_reps: int,
    bootstrap_seed: int,
) -> Dict[str, Any]:
    base_states, ensemble_meta = build_base_states(ensembles, growth_seeds)
    run_rows: List[Dict[str, Any]] = []
    group_rows: List[Dict[str, Any]] = []

    # candidate x ensemble x seed on a shared library of naturalized bases
    for point in candidates:
        for ens in ensembles:
            sub_rows = []
            for seed in growth_seeds:
                base = base_states[(ens.name, int(seed))]
                steps = compute_steps_for_state(base, steps_per_node, min_steps, max_steps)
                row = run_single_candidate_from_base(point, ens, base, seed=int(seed), steps=steps)
                run_rows.append(row)
                sub_rows.append(row)
            agg = summarize_group(point, ens, sub_rows)
            group_rows.append(agg)

    add_scores_to_group_rows(group_rows)
    cand_rows = candidate_summary_rows(
        candidates,
        ensembles,
        run_rows,
        group_rows,
        bootstrap_reps=bootstrap_reps,
        bootstrap_seed=bootstrap_seed,
    )

    # attach scores to ensemble meta summaries
    ens_summary: List[Dict[str, Any]] = []
    by_ens_meta: Dict[str, List[Dict[str, Any]]] = {}
    for r in ensemble_meta:
        by_ens_meta.setdefault(r["ensemble"], []).append(r)
    for ens in ensembles:
        rows = by_ens_meta.get(ens.name, [])
        out = {
            "ensemble": ens.name,
            "burnin_label": ens.burnin_label,
            "target_nodes": ens.target_nodes,
            "runs": len(rows),
        }
        for key in ["initial_nodes", "initial_tokens", "initial_beta1", "initial_triangles", "initial_spectral_radius", "initial_dim_proxy"]:
            vals = [safe_float(r[key], float("nan")) for r in rows]
            vals = [v for v in vals if math.isfinite(v)]
            out[f"mean_{key}"] = float(statistics.mean(vals)) if vals else float("nan")
            out[f"sd_{key}"] = float(statistics.pstdev(vals)) if len(vals) >= 2 else 0.0
        ens_summary.append(out)

    return {
        "ensemble_meta_rows": ensemble_meta,
        "ensemble_summary_rows": ens_summary,
        "run_rows": run_rows,
        "group_rows": group_rows,
        "candidate_summary_rows": cand_rows,
    }


# ------------------------------------------------------------
# Markdown reporting
# ------------------------------------------------------------

def top_candidates_table(rows: List[Dict[str, Any]], n: int = 5) -> str:
    head = [[
        "candidate", "r_birth", "r_death", "p_swap", "p_triad", "p_del",
        "mean composite", "CI low", "radius α", "overlap slope", "quasi slope", "burn-in sens"
    ]]
    for r in rows[:n]:
        head.append([
            str(r["candidate_name"]),
            f"{safe_float(r['r_birth']):.2f}",
            f"{safe_float(r['r_death']):.2f}",
            f"{safe_float(r['p_swap']):.2f}",
            f"{safe_float(r['p_triad']):.2f}",
            f"{safe_float(r['p_del']):.2f}",
            f"{safe_float(r['mean_composite']):.3f}",
            f"{safe_float(r['ci_low_mean_composite']):.3f}",
            f"{safe_float(r['radius_alpha']):.3f}",
            f"{safe_float(r['overlap_vs_logN_slope']):.3f}",
            f"{safe_float(r['quasi_vs_logN_slope']):.3f}",
            f"{safe_float(r['burnin_sensitivity']):.3f}",
        ])
    return markdown_table(head)


def ensemble_table(rows: List[Dict[str, Any]]) -> str:
    head = [["ensemble", "burn-in", "target", "mean nodes", "mean tokens", "mean β1", "mean spectral radius", "mean dim proxy"]]
    for r in rows:
        head.append([
            str(r["ensemble"]), str(r["burnin_label"]), str(int(round(safe_float(r['target_nodes'])))),
            f"{safe_float(r['mean_initial_nodes']):.1f}",
            f"{safe_float(r['mean_initial_tokens']):.1f}",
            f"{safe_float(r['mean_initial_beta1']):.1f}",
            f"{safe_float(r['mean_initial_spectral_radius']):.2f}",
            f"{safe_float(r['mean_initial_dim_proxy']):.2f}",
        ])
    return markdown_table(head)


def best_group_table(group_rows: List[Dict[str, Any]], candidate_name: str) -> str:
    sub = [r for r in group_rows if r["candidate_name"] == candidate_name]
    sub = sorted(sub, key=lambda r: (safe_float(r["target_nodes"]), str(r["burnin_label"])))
    head = [["ensemble", "target", "burn-in", "composite", "repair", "causal", "quasi", "geom", "radius", "overlap", "|Δβ1|", "init nodes"]]
    for r in sub:
        head.append([
            str(r["ensemble"]),
            str(int(round(safe_float(r['target_nodes'])))),
            str(r["burnin_label"]),
            f"{safe_float(r['composite_score']):.3f}",
            f"{safe_float(r['repair_score']):.3f}",
            f"{safe_float(r['causal_score']):.3f}",
            f"{safe_float(r['quasi_score']):.3f}",
            f"{safe_float(r['geom_score']):.3f}",
            f"{safe_float(r['mean_final_radius_control']):.2f}",
            f"{safe_float(r['mean_avg_local_overlap']):.3f}",
            f"{safe_float(r['mean_abs_delta_beta1']):.2f}",
            f"{safe_float(r['mean_initial_nodes']):.1f}",
        ])
    return markdown_table(head)


def write_main_report(path: str | Path, results: Dict[str, Any], args: argparse.Namespace) -> None:
    cand_rows = results["candidate_summary_rows"]
    group_rows = results["group_rows"]
    ens_rows = results["ensemble_summary_rows"]
    best = cand_rows[0] if cand_rows else None
    second = cand_rows[1] if len(cand_rows) >= 2 else None

    lines: List[str] = [
        "# Relasjonell universgraf v0.9 – skalaanalyse, større naturlige ensembler og burn-in-sensitivitet",
        "",
        "## Sammendrag",
        "",
        "v0.9 tar det neste metodisk riktige steget etter v0.8b: i stedet for bare å spørre hvilke regimer som er robuste på naturlige ensembler, spør vi hvordan denne robustheten **skalerer** når de naturlige starttilstandene blir større og når de får forskjellig modenhet før perturbasjonen settes inn.",
        "",
        "Dette steget gjør fire ting samtidig:",
        "",
        "1. evaluerer et fokusert kandidatbånd fra v0.8b på større naturlige ensembler,",
        "2. introduserer både lett og dyp burn-in ved hver skala,",
        "3. bruker hendelsesbudsjetter som vokser med initial størrelse,",
        "4. estimerer skalaindikatorer for radius/front, overlap/repair og quasi-invariant-bevaring.",
        "",
        "## Metode",
        "",
        f"- kandidater testet: {len(cand_rows)}",
        f"- naturlige ensembler: {len(ens_rows)}",
        f"- growth seeds per ensemble: {args.num_growth_seeds}",
        f"- event-budsjett: steps = clamp(round({args.steps_per_node:.1f} * N_init), {args.min_steps}, {args.max_steps})",
        f"- bootstrap-replikater for kandidatoppsummeringer: {args.bootstrap_reps}",
        "",
        "Naturlige starttilstander er fortsatt vokst frem av modellens egen dynamikk, ikke hånddesignet. Dermed blir v0.9 en strengere test av om kandidatbåndet overlever kontakt med større og mer moden intern geometri.",
        "",
        "## Startensembler",
        "",
        ensemble_table(ens_rows),
        "",
    ]
    if best is not None:
        lines.extend([
            "## Viktigste funn",
            "",
            f"- Høyest rangert kandidat i v0.9 ble `{best['candidate_name']}` med mean composite ≈ {safe_float(best['mean_composite']):.3f} og bootstrap lower bound ≈ {safe_float(best['ci_low_mean_composite']):.3f}.",
            f"- Samme kandidat hadde radius-eksponent α ≈ {safe_float(best['radius_alpha']):.3f} og burn-in-sensitivitet ≈ {safe_float(best['burnin_sensitivity']):.3f}.",
            f"- Overlap-vs-logN-slope var ≈ {safe_float(best['overlap_vs_logN_slope']):.3f}, mens quasi-vs-logN-slope var ≈ {safe_float(best['quasi_vs_logN_slope']):.3f}.",
        ])
        if second is not None:
            lines.append(f"- Neste kandidat lå nær med mean composite ≈ {safe_float(second['mean_composite']):.3f} og bootstrap lower bound ≈ {safe_float(second['ci_low_mean_composite']):.3f}.")
        lines.extend([
            "",
            "Disse tallene betyr ikke at vi har etablert en fysisk teori. De betyr at kandidatrommet igjen blir **smalere** når testen blir strengere, og at vi nå kan begynne å skille mellom kandidater som bare er robuste på moderate naturlige ensembler og kandidater som også ser rimelige ut under skalaøkning.",
            "",
            "## Toppkandidater",
            "",
            top_candidates_table(cand_rows, n=min(6, len(cand_rows))),
            "",
            f"## Gruppeprofil for beste kandidat: `{best['candidate_name']}`",
            "",
            best_group_table(group_rows, str(best["candidate_name"])),
            "",
            "## Hvordan skalaindikatorene skal leses",
            "",
            "- **radius α**: log-log-helning for `(radius + 1)` mot `N`. Lavere verdi betyr at fronten vokser mer sublineært med størrelse.",
            "- **overlap slope**: helning for local-overlap mot `log N`. Mindre negativ eller positiv helning er bedre.",
            "- **quasi slope**: helning for quasi-score mot `log N`. Høyere verdi betyr at quasi-invariant-bevaring ikke kollapser raskt med skala.",
            "- **burn-in sensitivity**: gjennomsnittlig differanse i composite mellom lett og dyp burn-in ved samme målskala. Lavere er bedre.",
            "",
            "## Tolkning",
            "",
            "Det mest interessante i v0.9 er ikke bare hvem som vant, men at analysen nå skiller mellom tre typer robusthet samtidig:",
            "",
            "1. **ensemble-robusthet**: kandidaten må gjøre det bra på flere naturlige startfamilier,",
            "2. **burn-in-robusthet**: kandidaten må ikke være sterkt avhengig av én spesifikk modenhetsgrad,",
            "3. **skala-robusthet**: radius og drift bør ikke eksplodere ukontrollert når initial størrelse øker.",
            "",
            "Hvis et kandidatbånd fortsatt ser bra ut under alle tre testene, er det metodisk langt mer interessant enn et regime som bare er pent på små hånddesignede startgrafer.",
            "",
            "## Referanser til metodefamilier",
            "",
            "Denne typen v0.9-analyse er inspirert av klassisk finite-size scaling og bootstrap-tradisjonen: man forsøker å lese av hvordan observerbare størrelser endrer seg med systemstørrelse og å sette intervaller på estimerte størrelser ved resampling. I vår setting er dette ikke et vanlig gittersystem, men metodologien er beslektet.",
            "",
            "- M. E. Fisher og M. N. Barber, *Scaling Theory for Finite-Size Effects in the Critical Region*, Phys. Rev. Lett. 28, 1516 (1972). DOI: 10.1103/PhysRevLett.28.1516",
            "- B. Efron, *Bootstrap Methods: Another Look at the Jackknife*, Ann. Statist. 7(1), 1–26 (1979). DOI: 10.1214/aos/1176344552",
            "",
            "## Filer",
            "",
            "- run-level data: `v09_scale_run_rows.csv`",
            "- group-level data: `v09_scale_group_rows.csv`",
            "- candidate summary data: `v09_scale_candidate_summary.csv`",
            "- ensemble summary data: `v09_scale_ensemble_summary.csv`",
        ])
    write_text(path, "\n".join(lines) + "\n")


def write_status(path: str | Path, results: Dict[str, Any]) -> None:
    cand_rows = results["candidate_summary_rows"]
    best = cand_rows[0] if cand_rows else None
    lines = [
        "# Statusnotat v0.9",
        "",
        "## Hvor vi er",
        "",
        "Prosjektet har nå passert tre terskler:",
        "",
        "1. Vi har identifisert et smalt kandidatbånd i åpne regimer (v0.8 og v0.8b).",
        "2. Vi har vist at dette båndet ikke kollapser umiddelbart når starttilstandene blir mer naturlige.",
        "3. Vi har begynt å måle **skalering** i stedet for bare enkel robusthet.",
        "",
        "v0.9 betyr derfor at prosjektet ikke lenger bare leter etter 'gode punkter', men etter punkter som oppfører seg disiplinert når naturlig ensemble, modenhet og størrelse varierer samtidig.",
        "",
    ]
    if best is not None:
        lines.extend([
            "## Foreløpig beste kandidat",
            "",
            f"- kandidat: `{best['candidate_name']}`",
            f"- mean composite: {safe_float(best['mean_composite']):.3f}",
            f"- bootstrap lower bound: {safe_float(best['ci_low_mean_composite']):.3f}",
            f"- radius α: {safe_float(best['radius_alpha']):.3f}",
            f"- overlap slope: {safe_float(best['overlap_vs_logN_slope']):.3f}",
            f"- quasi slope: {safe_float(best['quasi_vs_logN_slope']):.3f}",
            f"- burn-in sensitivity: {safe_float(best['burnin_sensitivity']):.3f}",
            "",
            "## Hva dette innebærer",
            "",
            "Det viktigste er ikke at ett regime er 'sant', men at prosjektet nå kan formulere presise, kvantitative kriterier for hva som teller som et bedre regime. Det gjør videre arbeid mer vitenskapelig og mindre impressionistisk.",
            "",
            "## Neste naturlige steg",
            "",
            "v0.9 peker mot v0.10: større naturlige ensembler, eksplisitt skalaekstrapolasjon og et mer bevisst skille mellom ekte sublineær kausalfront og ren finite-size-artefakt.",
        ])
    write_text(path, "\n".join(lines) + "\n")


def write_overview(path: str | Path, results: Dict[str, Any]) -> None:
    cand_rows = results["candidate_summary_rows"]
    best = cand_rows[0] if cand_rows else None
    lines = [
        "# Prosjektoversikt v0.9",
        "",
        "## Hovedidé",
        "",
        "Universet modelleres som en dynamisk relasjonsgraf der noder, relasjoner, stokastiske units of action og emergente mønstre er de grunnleggende ingrediensene. Spacetime, partikler, energi og korrelasjoner skal ikke legges inn for hånd, men oppstå som robuste makroregimer.",
        "",
        "## Hva som er etablert før v0.9",
        "",
        "- v0.4: redusert basis og regelbetingede ΔF-matriser",
        "- v0.5: perturbasjon og kausalitetslab",
        "- v0.6–v0.7: uniformisert og lokal maksimal kobling for åpne regimer",
        "- v0.8: faseatlas i et moderat åpent parameterbånd",
        "- v0.8b: naturlige ensembler, p_del-akse og bootstrap-robusthet",
        "",
        "## Hva v0.9 legger til",
        "",
        "v0.9 spør hvordan de lovende kandidatene oppfører seg når man samtidig varierer:",
        "",
        "1. størrelsen på naturlige starttilstander,",
        "2. hvor modent startuniverset er (burn-in),",
        "3. hvor lenge man lar paret utvikle seg relativt til initial størrelse.",
        "",
        "## Hvor vi står etter v0.9",
        "",
    ]
    if best is not None:
        lines.append(f"Foreløpig ser kandidatpunktet `{best['candidate_name']}` best ut i denne runden, men den dypere innsikten er at prosjektet nå opererer med et **smalt og målbart kandidatbånd** snarere enn løse idéer.")
    lines.extend([
        "",
        "## Hva som fortsatt mangler",
        "",
        "- videre skalaøkning",
        "- bedre estimater av asymptotisk frontvekst",
        "- kobling mellom disse regimene og mer konkrete effektive felt/proper-time-observabler",
        "- senere: testbare hypoteser og falsifiserbare signaturer",
    ])
    write_text(path, "\n".join(lines) + "\n")


def write_lay_summary(path: str | Path, results: Dict[str, Any]) -> None:
    cand_rows = results["candidate_summary_rows"]
    best = cand_rows[0] if cand_rows else None
    lines = [
        "# Relasjonell universgraf v0.9 – forklaring for ikke-spesialister",
        "",
        "## Hva prøver vi å finne ut?",
        "",
        "Vi prøver ikke å bevise at vi allerede har bygget en ny fysikkteori. Vi prøver å teste om en enkel idé – at universet kan forstås som et nettverk av relasjoner som endrer seg – kan gi stabile mønstre som ligner noe vi kjenner fra fysikk.",
        "",
        "## Hva gjorde vi i denne runden?",
        "",
        "Tidligere så vi at noen innstillinger i simulatoren så lovende ut. Men det var fortsatt mulig at de bare virket fordi vi startet med små og litt kunstige eksempler. Derfor gjorde vi tre ting:",
        "",
        "1. Vi lot simulatoren bygge større startuniverser selv.",
        "2. Vi lot noen av startuniversene være unge og andre være mer modne før testen begynte.",
        "3. Vi målte om forstyrrelser sprer seg på en kontrollert måte når universet blir større.",
        "",
    ]
    if best is not None:
        lines.extend([
            "## Hva fant vi?",
            "",
            f"Den foreløpig beste kandidaten i denne runden heter `{best['candidate_name']}`.",
            "",
            "Det viktige er ikke navnet, men at denne kandidaten klarte seg bedre enn de andre når vi gjorde startuniversene større og mer naturlige.",
            "",
            f"Den hadde en gjennomsnittlig robusthetsscore på omtrent {safe_float(best['mean_composite']):.3f}. Den hadde også en radius-eksponent på omtrent {safe_float(best['radius_alpha']):.3f}, som tyder på at skade/forstyrrelse ikke bare blåser opp helt ukontrollert med størrelse.",
            "",
            "## Hvorfor er dette interessant?",
            "",
            "Fordi et godt forskningsprosjekt ofte ser slik ut i starten: Når testene blir strengere, overlever ikke alt – men noen få kandidater gjør det, og kandidatfeltet blir smalere. Det er mye bedre enn en modell som bare virker tilfeldig eller kan forklare hva som helst.",
            "",
            "## Hva betyr det ikke?",
            "",
            "Det betyr ikke at vi har bevist hvordan universet faktisk er bygget opp. Det betyr bare at noen få regimer i simulatoren oppfører seg på en måte som fortsatt er verdt å studere videre.",
            "",
            "## Hva skjer videre?",
            "",
            "Neste steg er å presse disse kandidatene enda hardere: større skala, flere typer naturlige startuniverser og bedre måter å avgjøre om vi ser ekte struktur eller bare effekter av at systemene fortsatt er relativt små.",
        ])
    write_text(path, "\n".join(lines) + "\n")


def write_main_findings(path: str | Path, results: Dict[str, Any]) -> None:
    cand_rows = results["candidate_summary_rows"]
    lines = [
        "# v0.9 – hovedfunn og implikasjoner",
        "",
        "## Hovedfunn",
        "",
    ]
    for i, r in enumerate(cand_rows[:5], start=1):
        lines.append(
            f"{i}. `{r['candidate_name']}`: mean composite ≈ {safe_float(r['mean_composite']):.3f}, CI low ≈ {safe_float(r['ci_low_mean_composite']):.3f}, radius α ≈ {safe_float(r['radius_alpha']):.3f}, burn-in sensitivity ≈ {safe_float(r['burnin_sensitivity']):.3f}."
        )
    lines.extend([
        "",
        "## Implikasjoner",
        "",
        "- Prosjektet har passert fra enkel robusthetsjakt til eksplisitt skalaanalyse.",
        "- Kandidater kan nå sammenliknes ikke bare på samlet score, men på hvordan de reagerer på større naturlige initialbetingelser.",
        "- En lavere radius-eksponent sammen med akseptabel overlap- og quasi-bevaring er en mer fysisk interessant signatur enn bare høy score på små grafer.",
    ])
    write_text(path, "\n".join(lines) + "\n")


def write_glossary(path: str | Path) -> None:
    lines = [
        "# Ordliste v0.9",
        "",
        "- **burn-in**: en innledende modningsperiode der simuleringen får utvikle struktur før selve testen starter.",
        "- **candidate band / kandidatbånd**: et lite område i parameterrommet som fortsatt ser lovende ut etter flere tester.",
        "- **composite score**: en samlet score bygget fra repair, causal, quasi og geom.",
        "- **finite-size scaling**: en metode for å studere hvordan observasjoner endrer seg når systemstørrelsen øker.",
        "- **bootstrap**: en resampling-metode for å anslå usikkerhetsintervaller.",
        "- **quasi-invariant**: en størrelse som ikke er eksakt bevart, men som driver sakte i et bestemt regime.",
        "- **radius α**: helningen i en log-log-tilpasning av `(radius + 1)` mot systemstørrelse `N`.",
        "- **repair**: hvor godt to nesten like universgrener holder seg synkroniserte eller reparerer forskjeller.",
        "- **causal/front**: hvordan en lokal forskjell ser ut til å spre seg gjennom grafen.",
    ]
    write_text(path, "\n".join(lines) + "\n")


def write_readme(path: str | Path, produced: List[str]) -> None:
    lines = [
        "# README – bundle v0.9",
        "",
        "Denne pakken inneholder:",
        "",
    ]
    for p in produced:
        lines.append(f"- `{Path(p).name}`")
    lines.extend([
        "",
        "Kjernedokumentet er `relasjonell_universgraf_v0_9_skalaanalyse_og_store_ensembler.md`.",
        "Python-koden som genererer v0.9-resultatene er `relational_universe_v09_scale_and_natural_ensembles.py`.",
    ])
    write_text(path, "\n".join(lines) + "\n")


def write_codex_prompts(base_dir: Path, prompt_dir: Optional[Path] = None) -> List[str]:
    out_paths = []

    def emit(filename: str, content: str) -> None:
        primary = base_dir / filename
        write_text(primary, content)
        out_paths.append(str(primary))
        if prompt_dir is not None:
            secondary = prompt_dir / filename
            write_text(secondary, content)

    emit(
        "codex_prompt_v0_9b_storrelse_og_asymptotikk.md",
        """# Codex-prompt: v0.9b størrelse, asymptotikk og større naturlige ensembler

Du arbeider i en kodebase for prosjektet `relational_universe_*`.

Mål:
1. utvid v0.9-analysen til større naturlige ensembler (for eksempel målskala 144 og 192 noder),
2. bevar samme metodiske struktur som i v0.9: naturlig vekst, delt basebibliotek per ensemble/seed, lokal swap-perturbasjon, maksimal lokal kobling,
3. legg til eksplisitt asymptotisk analyse av radius, overlap og quasi-score,
4. skill tydelig mellom rå endring i observabler og skalaekstrapolasjon.

Krav:
- bruk markdown-filer for dokumentasjon,
- skriv ny Python-kode i egen fil,
- gjenbruk eksisterende hjelpefunksjoner der det er naturlig,
- lag CSV-utdata både på run-nivå, group-nivå og candidate-nivå,
- beregn bootstrap-intervaller for skalahelninger,
- dokumenter antakelser og begrensninger.

Tekniske føringer:
- hold lokalitet eksplisitt,
- ikke innfør nye primitive relasjonstyper,
- ikke bytt ut scoring uten å dokumentere hvorfor,
- dersom du lager plots, bruk matplotlib og lagre dem til filer.

Lever:
- ny Python-fil,
- minst tre nye markdown-filer,
- README,
- kort oppsummering av funn og hva de innebærer.
"""
    )

    emit(
        "codex_prompt_v0_9_plotting_og_finite_size.md",
        """# Codex-prompt: plotting, finite-size og bootstrap-diagnostikk for v0.9

Oppgave:
Lag en analysemodule som leser `v09_scale_group_rows.csv` og `v09_scale_candidate_summary.csv` og produserer:

1. plott av composite-score mot initial størrelse,
2. plott av radius mot størrelse både lineært og log-log,
3. plott av overlap og quasi-score mot log størrelse,
4. en markdown-rapport som forklarer hvilke figurer som støtter eller svekker hypotesen om sublineær skadeutbredelse.

Krav:
- bruk matplotlib, ikke seaborn,
- ett plot per figur,
- ingen spesifikk fargestil,
- lagre alle figurer til filer,
- skriv en kort tolkning per figur i markdown.
"""
    )

    emit(
        "codex_prompt_v0_9_verifikasjon_og_regresjon.md",
        """# Codex-prompt: verifikasjon og regresjonstester for v0.9

Du skal styrke påliteligheten i v0.9-koden.

Oppgaver:
1. legg inn regresjonstester for at `compute_steps_for_state` er monotont stigende i `N` innenfor klammegrensene,
2. test at bootstrap-rutinene ikke krasjer når én metric er konstant,
3. test at burn-in-sensitivitet beregnes riktig på syntetiske group-rows,
4. test at radius_alpha blir ~0 når radius er konstant på tvers av størrelser,
5. test at radius_alpha blir ~1 når radius er proporsjonal med N.

Krav:
- skriv testene i en egen Python-fil,
- legg ved kort markdown-notat om hva som ble testet og hvorfor det er viktig.
"""
    )

    emit(
        "codex_prompt_assistentkontekst_v0_9.md",
        """# Assistentkontekst v0.9

Prosjektet undersøker om en relasjonell universgraf med noder, én relasjonstype og stokastiske units of action kan utvikle robuste makroregimer som ligner spacetime, kausal struktur og quasi-bevarte størrelser.

Status til og med v0.9:
- v0.4: redusert basis og ΔF-klassifikasjon,
- v0.5: perturbasjon og kausalitetslab,
- v0.6–v0.7: uniformisert / lokal maksimal kobling,
- v0.8: faseatlas,
- v0.8b: naturlige ensembler og bootstrap-robusthet,
- v0.9: større naturlige ensembler, burn-in-regimer og eksplisitt skalaanalyse.

Når du skriver kode eller analyser for prosjektet, skal du:
- holde fast ved én relasjonstype,
- bruke markdown for dokumentasjon,
- være tydelig på forskjellen mellom eksakte invariants, quasi-invariants og rene grafidentiteter,
- være ærlig om usikkerhet,
- prioritere reproducerbare, testbare analyser fremfor løse spekulasjoner.
"""
    )

    return out_paths


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.9 scale analysis on larger natural ensembles")
    p.add_argument("--outdir", default="Documentation")
    p.add_argument("--prompt-dir", default="Prompts")
    p.add_argument("--num-growth-seeds", type=int, default=3)
    p.add_argument("--growth-seed-start", type=int, default=101)
    p.add_argument("--steps-per-node", type=float, default=8.0)
    p.add_argument("--min-steps", type=int, default=220)
    p.add_argument("--max-steps", type=int, default=900)
    p.add_argument("--bootstrap-reps", type=int, default=300)
    p.add_argument("--bootstrap-seed", type=int, default=12345)
    p.add_argument("--bundle-zip", default="")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    candidates = default_candidates()
    ensembles = default_scale_ensembles()
    growth_seeds = [args.growth_seed_start + 101 * i for i in range(args.num_growth_seeds)]

    results = run_v09(
        candidates,
        ensembles,
        growth_seeds,
        steps_per_node=args.steps_per_node,
        min_steps=args.min_steps,
        max_steps=args.max_steps,
        bootstrap_reps=args.bootstrap_reps,
        bootstrap_seed=args.bootstrap_seed,
    )

    run_csv = outdir / "v09_scale_run_rows.csv"
    group_csv = outdir / "v09_scale_group_rows.csv"
    cand_csv = outdir / "v09_scale_candidate_summary.csv"
    ens_csv = outdir / "v09_scale_ensemble_summary.csv"
    write_csv(run_csv, results["run_rows"])
    write_csv(group_csv, results["group_rows"])
    write_csv(cand_csv, results["candidate_summary_rows"])
    write_csv(ens_csv, results["ensemble_summary_rows"])

    report = outdir / "relasjonell_universgraf_v0_9_skalaanalyse_og_store_ensembler.md"
    status = outdir / "relasjonell_universgraf_status_v0_9.md"
    overview = outdir / "prosjektoversikt_v0_9.md"
    lay = outdir / "relasjonell_universgraf_for_ikke_spesialister_v0_9.md"
    findings = outdir / "v0_9_hovedfunn_og_implikasjoner.md"
    glossary = outdir / "ordliste_v0_9.md"
    write_main_report(report, results, args)
    write_status(status, results)
    write_overview(overview, results)
    write_lay_summary(lay, results)
    write_main_findings(findings, results)
    write_glossary(glossary)

    prompt_dir = Path(args.prompt_dir) if args.prompt_dir else None
    prompt_paths = write_codex_prompts(outdir, prompt_dir=prompt_dir)

    produced = [
        str(report), str(status), str(overview), str(lay), str(findings), str(glossary),
        str(run_csv), str(group_csv), str(cand_csv), str(ens_csv),
        *prompt_paths,
        str(Path(__file__).resolve()),
    ]
    readme = outdir / "README_relational_universe_bundle_v9.md"
    write_readme(readme, produced)
    produced.append(str(readme))

    bundle = None
    if args.bundle_zip:
        bundle = Path(args.bundle_zip)
        ensure_parent_dir(bundle)
        with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for p in produced:
                zf.write(p, arcname=Path(p).name)

    print("WROTE", report)
    print("WROTE", status)
    print("WROTE", overview)
    print("WROTE", lay)
    print("WROTE", findings)
    print("WROTE", glossary)
    print("WROTE", run_csv)
    print("WROTE", group_csv)
    print("WROTE", cand_csv)
    print("WROTE", ens_csv)
    for p in prompt_paths:
        print("WROTE", p)
    print("WROTE", readme)
    if bundle is not None:
        print("WROTE", bundle)


if __name__ == "__main__":
    main()
