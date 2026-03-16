#!/usr/bin/env python3
"""v0.10c growth-regime search for larger natural start ensembles.

This script compares a few computationally tractable growth generators after
v0.10b showed that the original reference-growth regime fails to realize large
nominal sizes reliably. The new generators are explicitly generator-level
constructions. They are not claimed to be the same as the fully coupled CTMC
used elsewhere in the project; they are a practical attempt to produce larger,
still non-trivial start ensembles for later dynamical tests.
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
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v10b_ensemble_calibration as v10b


def safe_float(x: Any, default: float = float("nan")) -> float:
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


def mean_or_nan(values: Iterable[float]) -> float:
    vals = [float(v) for v in values if math.isfinite(float(v))]
    return float(statistics.mean(vals)) if vals else float("nan")


def sd_or_zero(values: Iterable[float]) -> float:
    vals = [float(v) for v in values if math.isfinite(float(v))]
    return float(statistics.pstdev(vals)) if len(vals) >= 2 else 0.0


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    path = Path(path)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys: List[str] = []
    seen = set()
    for row in rows:
        for k in row:
            if k not in seen:
                seen.add(k)
                keys.append(k)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow(row)


@dataclass(frozen=True)
class FastParams:
    seed_rate: float
    move_rate: float
    triad_rate: float
    swap_rate: float
    token_birth_rate: float
    token_death_rate: float
    prune_rate: float
    seed_triangle_prob: float = 0.05
    min_tokens: int = 1


@dataclass(frozen=True)
class FastRegime:
    name: str
    phase1: FastParams
    phase2: Optional[FastParams]
    rel_tol: float = 0.10
    min_fraction: float = 0.10
    max_steps_factor: float = 8.0
    hold_steps_light: int = 20
    hold_steps_deep: int = 60


def token_count_on_node(state: v7.State) -> Dict[int, int]:
    out: Dict[int, int] = {}
    for _, v in state.token_pos.items():
        out[v] = out.get(v, 0) + 1
    return out


def choose_anchor_node(state: v7.State, rng: random.Random) -> int:
    counts = token_count_on_node(state)
    vs = state.g.nodes()
    weights: List[float] = []
    for v in vs:
        w = 1.0 + 0.2 * state.g.degree(v) + 0.8 * counts.get(v, 0)
        weights.append(max(0.01, w))
    total = sum(weights)
    x = rng.random() * total
    acc = 0.0
    for v, w in zip(vs, weights):
        acc += w
        if x <= acc:
            return v
    return vs[-1]


def fast_step(state: v7.State, manager: v7.PairManager, rng: random.Random, params: FastParams) -> str:
    ops: List[str] = []
    weights: List[float] = []

    if state.g.num_nodes() > 0:
        ops.append("seed")
        weights.append(params.seed_rate)
    if state.token_count() > 0:
        ops.extend(["move", "triad", "swap", "tbirth"])
        weights.extend([params.move_rate, params.triad_rate, params.swap_rate, params.token_birth_rate])
    if state.token_count() > params.min_tokens:
        ops.append("tdeath")
        weights.append(params.token_death_rate)
    token_nodes = set(state.token_pos.values())
    prunable = [v for v in state.g.nodes() if state.g.degree(v) == 1 and v not in token_nodes]
    if prunable:
        ops.append("prune")
        weights.append(params.prune_rate)

    total = sum(weights)
    if total <= 0.0:
        return "noop"
    x = rng.random() * total
    acc = 0.0
    op = ops[-1]
    for o, w in zip(ops, weights):
        acc += w
        if x <= acc:
            op = o
            break

    if op == "seed":
        anchor = choose_anchor_node(state, rng)
        nid = manager.alloc_node_id()
        state.g.add_edge(anchor, nid)
        if rng.random() < params.seed_triangle_prob:
            neigh = [u for u in state.g.neighbors(anchor) if u != nid]
            if neigh:
                state.g.add_edge(nid, rng.choice(neigh))
        return op

    if op == "move":
        tid = rng.choice(state.sorted_token_ids())
        v = state.token_pos[tid]
        neigh = list(state.g.neighbors(v))
        if neigh:
            state.token_pos[tid] = rng.choice(neigh)
        return op

    if op == "triad":
        tids = state.sorted_token_ids()
        rng.shuffle(tids)
        for tid in tids:
            v = state.token_pos[tid]
            neigh = list(state.g.neighbors(v))
            rng.shuffle(neigh)
            for u in neigh:
                cands = [w for w in state.g.neighbors(u) if w != v and not state.g.has_edge(v, w)]
                if cands:
                    state.g.add_edge(v, rng.choice(cands))
                    return op
        return "move"

    if op == "swap":
        tids = state.sorted_token_ids()
        rng.shuffle(tids)
        for tid in tids:
            v = state.token_pos[tid]
            neigh = list(state.g.neighbors(v))
            rng.shuffle(neigh)
            for u in neigh:
                cands = [w for w in state.g.neighbors(u) if w != v and not state.g.has_edge(v, w)]
                if cands:
                    state.g.remove_edge(v, u)
                    state.g.add_edge(v, rng.choice(cands))
                    return op
        return "move"

    if op == "tbirth":
        tid = rng.choice(state.sorted_token_ids())
        v = state.token_pos[tid]
        neigh = list(state.g.neighbors(v))
        loc = v if (not neigh or rng.random() < 0.5) else rng.choice(neigh)
        state.token_pos[manager.alloc_token_id()] = loc
        return op

    if op == "tdeath":
        tids = state.sorted_token_ids()
        tids.sort(key=lambda tid: (state.g.degree(state.token_pos[tid]), tid))
        if tids:
            del state.token_pos[tids[0]]
        return op

    if op == "prune":
        v = rng.choice(prunable)
        state.g.remove_node(v)
        return op

    return "noop"


def grow_fast(ensemble: v10b.CalibrationEnsemble, seed: int, regime: FastRegime) -> Tuple[v7.State, Dict[str, Any]]:
    rng = random.Random(seed)
    base, _, _ = v7.bootstrap(ensemble.initial_cycle, ensemble.initial_tokens, rng)
    state = base.clone()
    next_node_id, next_token_id = v08b.next_ids_from_state(state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)

    target = ensemble.target_nodes
    lo = math.floor(target * (1.0 - regime.rel_tol))
    hi = math.ceil(target * (1.0 + regime.rel_tol))
    min_steps = int(ensemble.burnin_steps * regime.min_fraction)
    max_steps = int(ensemble.burnin_steps * regime.max_steps_factor / 10.0 + ensemble.extra_burnin_high)
    hold = regime.hold_steps_deep if ensemble.burnin_label == "deep" else regime.hold_steps_light

    best = state.clone()
    best_err = abs(state.g.num_nodes() - target)
    first_hit: Optional[int] = None
    last_in_band: Optional[v7.State] = None

    for step in range(max_steps):
        params = regime.phase1
        if regime.phase2 is not None and state.g.num_nodes() >= lo:
            params = regime.phase2
        fast_step(state, manager, rng, params)
        n = state.g.num_nodes()
        err = abs(n - target)
        if err < best_err:
            best_err = err
            best = state.clone()
        if step + 1 >= min_steps and lo <= n <= hi:
            if first_hit is None:
                first_hit = step + 1
            last_in_band = state.clone()
            hold -= 1
            if hold <= 0:
                break
        elif first_hit is not None:
            hold -= 1
            if hold <= 0:
                break

    return last_in_band or best, {
        "first_hit_step": float(first_hit) if first_hit is not None else float("nan"),
        "hit_target_band": 1 if first_hit is not None else 0,
        "growth_steps_executed": float(step + 1),
        "target_low": float(lo),
        "target_high": float(hi),
    }


def feature_row(state: v7.State, rng_seed: int) -> Dict[str, float]:
    feat = v10b.feature_row(state, rng_seed=rng_seed)
    return dict(feat)


def default_regimes() -> List[FastRegime]:
    return [
        FastRegime(
            "fast_ref",
            FastParams(seed_rate=0.7, move_rate=0.35, triad_rate=0.03, swap_rate=0.02, token_birth_rate=0.01, token_death_rate=0.008, prune_rate=0.004, seed_triangle_prob=0.06),
            None,
            rel_tol=0.10, min_fraction=0.10, max_steps_factor=8.0, hold_steps_light=20, hold_steps_deep=60,
        ),
        FastRegime(
            "fast_balanced",
            FastParams(seed_rate=1.0, move_rate=0.20, triad_rate=0.03, swap_rate=0.02, token_birth_rate=0.012, token_death_rate=0.006, prune_rate=0.003, seed_triangle_prob=0.08),
            FastParams(seed_rate=0.20, move_rate=0.50, triad_rate=0.05, swap_rate=0.03, token_birth_rate=0.008, token_death_rate=0.008, prune_rate=0.004, seed_triangle_prob=0.04),
            rel_tol=0.10, min_fraction=0.08, max_steps_factor=10.0, hold_steps_light=30, hold_steps_deep=90,
        ),
        FastRegime(
            "fast_push",
            FastParams(seed_rate=1.3, move_rate=0.10, triad_rate=0.02, swap_rate=0.01, token_birth_rate=0.010, token_death_rate=0.004, prune_rate=0.002, seed_triangle_prob=0.04),
            FastParams(seed_rate=0.25, move_rate=0.45, triad_rate=0.04, swap_rate=0.03, token_birth_rate=0.008, token_death_rate=0.008, prune_rate=0.004, seed_triangle_prob=0.03),
            rel_tol=0.10, min_fraction=0.06, max_steps_factor=10.0, hold_steps_light=25, hold_steps_deep=80,
        ),
    ]


def anchor_statistics(calibration_rows: List[Dict[str, Any]]) -> Tuple[Dict[str, float], Dict[str, float]]:
    anchor_source = [
        r for r in calibration_rows
        if int(r["target_nodes"]) <= 96 and safe_float(r["abs_rel_size_error"], 9.0) <= 0.20
    ]
    keys = [
        "realized_beta1_per_node",
        "realized_triangles_per_node",
        "realized_clustering",
        "realized_dim_proxy",
        "realized_spectral_per_sqrtN",
    ]
    med = {k: statistics.median(float(r[k]) for r in anchor_source) for k in keys}
    sd = {}
    for k in keys:
        vals = [float(r[k]) for r in anchor_source]
        s = statistics.pstdev(vals) if len(vals) >= 2 else 0.1
        sd[k] = s if s > 1e-6 else 0.1
    return med, sd


def naturalness_score(feat: Dict[str, float], med: Dict[str, float], sd: Dict[str, float]) -> float:
    mapping = {
        "realized_beta1_per_node": "beta1_per_node",
        "realized_triangles_per_node": "triangles_per_node",
        "realized_clustering": "clustering",
        "realized_dim_proxy": "dim_proxy",
        "realized_spectral_per_sqrtN": "spectral_per_sqrtN",
    }
    zs = []
    for ref_key, feat_key in mapping.items():
        z = abs(float(feat[feat_key]) - med[ref_key]) / sd[ref_key]
        zs.append(z)
    mean_z = sum(zs) / max(1, len(zs))
    return float(1.0 / (1.0 + mean_z))


def collect_run_row(
    regime: FastRegime,
    ensemble: v10b.CalibrationEnsemble,
    seed: int,
    med: Dict[str, float],
    sd: Dict[str, float],
) -> Dict[str, Any]:
    state, meta = grow_fast(ensemble, seed, regime)
    feat = feature_row(state, rng_seed=seed + 999)
    return {
        "regime": regime.name,
        "ensemble": ensemble.name,
        "target_nodes": ensemble.target_nodes,
        "burnin_label": ensemble.burnin_label,
        "seed": seed,
        **meta,
        "realized_nodes": feat["nodes"],
        "realized_tokens": feat["tokens"],
        "realized_beta1": feat["beta1"],
        "realized_triangles": feat["triangles"],
        "realized_spectral_radius": feat["spectral_radius"],
        "realized_dim_proxy": feat["dim_proxy"],
        "realized_clustering": feat["clustering"],
        "realized_avg_degree": feat["avg_degree"],
        "realized_beta1_per_node": feat["beta1_per_node"],
        "realized_triangles_per_node": feat["triangles_per_node"],
        "realized_spectral_per_sqrtN": feat["spectral_per_sqrtN"],
        "abs_rel_size_error": abs(feat["nodes"] - ensemble.target_nodes) / max(float(ensemble.target_nodes), 1.0),
        "within_target_band": 1 if abs(feat["nodes"] - ensemble.target_nodes) / max(float(ensemble.target_nodes), 1.0) <= 0.10 else 0,
        "naturalness_score": naturalness_score(feat, med, sd),
    }


def summarize_runs(run_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: Dict[Tuple[str, str, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        key = (str(row["regime"]), str(row["burnin_label"]), int(row["target_nodes"]))
        groups.setdefault(key, []).append(row)
    out: List[Dict[str, Any]] = []
    for (regime, burnin_label, target), sub in sorted(groups.items()):
        out.append({
            "regime": regime,
            "burnin_label": burnin_label,
            "target_nodes": target,
            "runs": len(sub),
            "mean_realized_nodes": mean_or_nan(r["realized_nodes"] for r in sub),
            "sd_realized_nodes": sd_or_zero(r["realized_nodes"] for r in sub),
            "q10_realized_nodes": quantile([float(r["realized_nodes"]) for r in sub], 0.10),
            "q90_realized_nodes": quantile([float(r["realized_nodes"]) for r in sub], 0.90),
            "mean_abs_rel_size_error": mean_or_nan(r["abs_rel_size_error"] for r in sub),
            "hit_rate": mean_or_nan(r["within_target_band"] for r in sub),
            "mean_naturalness_score": mean_or_nan(r["naturalness_score"] for r in sub),
            "mean_beta1_per_node": mean_or_nan(r["realized_beta1_per_node"] for r in sub),
            "mean_triangles_per_node": mean_or_nan(r["realized_triangles_per_node"] for r in sub),
            "mean_clustering": mean_or_nan(r["realized_clustering"] for r in sub),
            "mean_dim_proxy": mean_or_nan(r["realized_dim_proxy"] for r in sub),
            "mean_spectral_per_sqrtN": mean_or_nan(r["realized_spectral_per_sqrtN"] for r in sub),
        })
    return out


def summarize_regimes(summary_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for row in summary_rows:
        groups.setdefault(str(row["regime"]), []).append(row)
    out: List[Dict[str, Any]] = []
    for regime, sub in sorted(groups.items()):
        size_score = statistics.mean(1.0 - min(1.0, safe_float(r["mean_abs_rel_size_error"]) / 0.12) for r in sub)
        hit_score = statistics.mean(safe_float(r["hit_rate"]) for r in sub)
        nat_score = statistics.mean(safe_float(r["mean_naturalness_score"]) for r in sub)
        out.append({
            "regime": regime,
            "mean_abs_rel_size_error": statistics.mean(safe_float(r["mean_abs_rel_size_error"]) for r in sub),
            "mean_hit_rate": hit_score,
            "mean_naturalness_score": nat_score,
            "sd_realized_nodes_mean": statistics.mean(safe_float(r["sd_realized_nodes"]) for r in sub),
            "composite_score": 0.45 * size_score + 0.30 * hit_score + 0.25 * nat_score,
        })
    out.sort(key=lambda r: safe_float(r["composite_score"]), reverse=True)
    return out


def overlap_rows(summary_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for row in summary_rows:
        groups.setdefault((str(row["regime"]), str(row["burnin_label"])), []).append(row)
    out: List[Dict[str, Any]] = []
    for (regime, burnin_label), sub in sorted(groups.items()):
        sub_sorted = sorted(sub, key=lambda r: int(r["target_nodes"]))
        for a, b in zip(sub_sorted[:-1], sub_sorted[1:]):
            a_lo = safe_float(a["q10_realized_nodes"])
            a_hi = safe_float(a["q90_realized_nodes"])
            b_lo = safe_float(b["q10_realized_nodes"])
            b_hi = safe_float(b["q90_realized_nodes"])
            overlap = max(0.0, min(a_hi, b_hi) - max(a_lo, b_lo))
            union = max(a_hi, b_hi) - min(a_lo, b_lo)
            out.append({
                "regime": regime,
                "burnin_label": burnin_label,
                "target_a": int(a["target_nodes"]),
                "target_b": int(b["target_nodes"]),
                "gap_q90_to_q10": b_lo - a_hi,
                "overlap_fraction": (overlap / union) if union > 0 else 0.0,
                "strictly_separated": 1 if a_hi < b_lo else 0,
            })
    return out


def build_markdown(regime_rows: List[Dict[str, Any]], summary_rows: List[Dict[str, Any]], overlap: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# v0.10c growth-regime search")
    lines.append("")
    lines.append("Dette dokumentet sammenligner noen få alternative growth-regimer etter at v0.10b viste at referansegeneratoren ikke skalerte troverdig til store nominelle størrelser.")
    lines.append("")
    lines.append("## Viktig tolkning")
    lines.append("")
    lines.append("- `fast_ref`, `fast_balanced` og `fast_push` er **generatorregimer**, ikke nye fysiske teorier.")
    lines.append("- De er ment som praktiske ensemblebyggere for storskala tester.")
    lines.append("- God størrelse-treff alene er ikke nok; vi må også se på frøvarians og en enkel naturalness-proxy.")
    lines.append("")
    lines.append("## Regime-aggregater")
    lines.append("")
    lines.append("| regime | mean_abs_rel_err | hit_rate | naturalness | sd_nodes_mean | composite |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in regime_rows:
        lines.append(
            f"| {row['regime']} | {safe_float(row['mean_abs_rel_size_error']):.3f} | {safe_float(row['mean_hit_rate']):.2f} | "
            f"{safe_float(row['mean_naturalness_score']):.3f} | {safe_float(row['sd_realized_nodes_mean']):.2f} | {safe_float(row['composite_score']):.3f} |"
        )
    lines.append("")
    lines.append("## Per størrelse og burn-in-label")
    lines.append("")
    lines.append("| regime | burnin | target | realized_mean | q10 | q90 | hit_rate | naturalness |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in summary_rows:
        lines.append(
            f"| {row['regime']} | {row['burnin_label']} | {int(row['target_nodes'])} | {safe_float(row['mean_realized_nodes']):.1f} | "
            f"{safe_float(row['q10_realized_nodes']):.1f} | {safe_float(row['q90_realized_nodes']):.1f} | "
            f"{safe_float(row['hit_rate']):.2f} | {safe_float(row['mean_naturalness_score']):.3f} |"
        )
    lines.append("")
    lines.append("## Nivåseparasjon")
    lines.append("")
    lines.append("| regime | burnin | A | B | gap_q90_to_q10 | overlap_fraction | separated |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in overlap:
        lines.append(
            f"| {row['regime']} | {row['burnin_label']} | {int(row['target_a'])} | {int(row['target_b'])} | "
            f"{safe_float(row['gap_q90_to_q10']):.1f} | {safe_float(row['overlap_fraction']):.2f} | {int(row['strictly_separated'])} |"
        )
    lines.append("")
    lines.append("## Kort dom")
    lines.append("")
    lines.append("Et regime er ikke automatisk bedre bare fordi det treffer målstørrelsen eksakt. Hvis dette oppnås ved å produsere for enkle eller for smale strukturer, må det sies eksplisitt.")
    lines.append("I praksis bør prosjektet foretrekke et regime som både treffer størrelse og bevarer et rimelig forhold til de mindre, mer troverdige naturlige strukturene.")
    lines.append("")
    return "\n".join(lines) + "\n"


def load_calibration_runs(path: str | Path) -> List[Dict[str, Any]]:
    with Path(path).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.10c growth-regime search")
    ap.add_argument("--calibration-runs", type=str, default="/mnt/data/v10b_ensemble_calibration_runs.csv")
    ap.add_argument("--targets", type=str, default="96,192,256")
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--output-prefix", type=str, default="/mnt/data/v10c")
    return ap


def main() -> None:
    ap = build_argparser()
    args = ap.parse_args()

    calibration_rows = load_calibration_runs(args.calibration_runs)
    med, sd = anchor_statistics(calibration_rows)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [e for e in v10b.build_ensembles(targets)]
    growth_seeds = [2000 + 17 * i for i in range(args.seeds)]

    run_rows: List[Dict[str, Any]] = []
    for regime in default_regimes():
        for ens in ensembles:
            for seed in growth_seeds:
                run_rows.append(collect_run_row(regime, ens, seed, med, sd))

    summary_rows = summarize_runs(run_rows)
    regime_rows = summarize_regimes(summary_rows)
    overlap = overlap_rows(summary_rows)

    prefix = args.output_prefix
    write_csv(f"{prefix}_growth_regime_runs.csv", run_rows)
    write_csv(f"{prefix}_growth_regime_summary.csv", summary_rows)
    write_csv(f"{prefix}_growth_regime_overall.csv", regime_rows)
    write_csv(f"{prefix}_growth_regime_overlap.csv", overlap)
    Path(f"{prefix}_growth_regime_search.md").write_text(build_markdown(regime_rows, summary_rows, overlap), encoding="utf-8")


if __name__ == "__main__":
    main()
