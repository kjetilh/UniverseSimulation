#!/usr/bin/env python3
"""v0.10b ensemble calibration for natural-growth start states.

This script treats the ensemble generator itself as the object of study.
It calibrates the existing natural-growth regime, measures realized sizes and
structural features, adds an adaptive size-targeting heuristic, and reports
which nominal size levels are actually usable for later asymptotic analysis.

Ground truth note
-----------------
The user prompt referenced a v0.10 scale-collapse file, but in the present
workspace the active codebase on disk is v0.8b/v0.9/v0.9b. This script is
therefore built directly on those files rather than patching a missing v0.10
module.
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


# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------

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
    path.parent.mkdir(parents=True, exist_ok=True)
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


# ---------------------------------------------------------------------------
# Ensemble and regime definitions
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CalibrationEnsemble:
    name: str
    target_nodes: int
    burnin_label: str  # light / deep
    initial_cycle: int
    initial_tokens: int
    burnin_steps: int
    extra_burnin_low: int
    extra_burnin_high: int


@dataclass(frozen=True)
class CalibrationMethod:
    name: str  # baseline / adaptive
    rel_tol: float = 0.10
    max_growth_factor: float = 4.0
    min_fraction_of_baseline: float = 0.30
    hold_steps: int = 60
    snapshot_stride: int = 5


def default_targets() -> List[int]:
    return [24, 48, 96, 128, 160, 192, 256]


def initial_cycle_for_target(target: int) -> int:
    base = 10.0 + 2.0 * math.log(max(target, 24) / 24.0, 2.0)
    return max(8, int(round(base)))


def initial_tokens_for_target(target: int) -> int:
    base = 5.0 + math.log(max(target, 24) / 24.0, 2.0)
    return max(4, int(round(base)))


def baseline_budget(target: int, burnin_label: str) -> Tuple[int, int, int]:
    # Light/deep schedules anchored in v0.9/v0.9b and gently extrapolated.
    if burnin_label == "light":
        burn = int(round(22.0 * target))
        extra_low = int(round(max(20.0, 0.90 * math.sqrt(target) * 10.0)))
        extra_high = int(round(max(80.0, 1.85 * math.sqrt(target) * 10.0)))
    else:
        burn = int(round(34.0 * target))
        extra_low = int(round(max(160.0, 2.2 * math.sqrt(target) * 10.0)))
        extra_high = int(round(max(300.0, 3.9 * math.sqrt(target) * 10.0)))
    return burn, extra_low, extra_high


def build_ensembles(targets: Sequence[int]) -> List[CalibrationEnsemble]:
    out: List[CalibrationEnsemble] = []
    for target in targets:
        for label in ("light", "deep"):
            burn, lo, hi = baseline_budget(target, label)
            out.append(
                CalibrationEnsemble(
                    name=f"natural{target}_{label}",
                    target_nodes=int(target),
                    burnin_label=label,
                    initial_cycle=initial_cycle_for_target(int(target)),
                    initial_tokens=initial_tokens_for_target(int(target)),
                    burnin_steps=burn,
                    extra_burnin_low=lo,
                    extra_burnin_high=hi,
                )
            )
    return out


def reference_growth_params() -> v7.Params:
    return v08b.reference_growth_params()


def reference_spec(ensemble: CalibrationEnsemble) -> v08b.EnsembleSpec:
    return v08b.EnsembleSpec(
        name=ensemble.name,
        kind="natural_grown",
        initial_cycle=ensemble.initial_cycle,
        initial_tokens=ensemble.initial_tokens,
        target_nodes=ensemble.target_nodes,
        burnin_steps=ensemble.burnin_steps,
        extra_burnin_low=ensemble.extra_burnin_low,
        extra_burnin_high=ensemble.extra_burnin_high,
        include_in_natural_score=1,
    )


def feature_row(state: v7.State, rng_seed: int) -> Dict[str, float]:
    rng = random.Random(rng_seed)
    feat = v7.feature_row(state, rng=rng)
    nodes = max(1.0, feat["nodes"])
    comps = max(1.0, feat["components"])
    edges = feat["beta1"] + feat["nodes"] - feat["components"]
    avg_degree = 2.0 * edges / nodes
    feat["avg_degree"] = float(avg_degree)
    feat["beta1_per_node"] = float(feat["beta1"] / nodes)
    feat["triangles_per_node"] = float(feat["triangles"] / nodes)
    feat["spectral_per_sqrtN"] = float(feat["spectral_radius"] / math.sqrt(nodes))
    return feat


# ---------------------------------------------------------------------------
# Growth drivers
# ---------------------------------------------------------------------------

def adaptive_grow_state(
    ensemble: CalibrationEnsemble,
    *,
    rng_seed: int,
    growth_params: v7.Params,
    method: CalibrationMethod,
) -> Tuple[v7.State, Dict[str, Any]]:
    rng = random.Random(rng_seed)
    base, _, _ = v7.bootstrap(ensemble.initial_cycle, ensemble.initial_tokens, rng)
    state = base.clone()
    next_node_id, next_token_id = v08b.next_ids_from_state(state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)

    target = float(ensemble.target_nodes)
    lo = math.floor(target * (1.0 - method.rel_tol))
    hi = math.ceil(target * (1.0 + method.rel_tol))
    min_steps = int(round(method.min_fraction_of_baseline * ensemble.burnin_steps))
    max_steps = int(round(method.max_growth_factor * ensemble.burnin_steps + ensemble.extra_burnin_high))

    best_state = state.clone()
    best_err = abs(state.g.num_nodes() - target)
    in_band_snapshots = 0
    first_hit_step: Optional[int] = None
    last_in_band: Optional[v7.State] = None
    total_steps = 0
    hold_remaining = method.hold_steps

    for step in range(max_steps):
        total_steps = step + 1
        v08b.single_step(state, manager, rng, growth_params)
        n = state.g.num_nodes()
        err = abs(n - target)
        if err < best_err:
            best_err = err
            best_state = state.clone()
        if step + 1 >= min_steps and lo <= n <= hi:
            if first_hit_step is None:
                first_hit_step = step + 1
            if (step + 1) % max(1, method.snapshot_stride) == 0:
                last_in_band = state.clone()
                in_band_snapshots += 1
            hold_remaining -= 1
            if hold_remaining <= 0:
                break
        elif first_hit_step is not None:
            # Once the process has entered the target band, we keep looking a little
            # longer, but not forever. This avoids taking a single transient hit as
            # the final calibrated ensemble.
            hold_remaining -= 1
            if hold_remaining <= 0:
                break

    chosen = last_in_band or best_state
    meta = {
        "target_low": float(lo),
        "target_high": float(hi),
        "target_rel_tol": float(method.rel_tol),
        "min_steps": float(min_steps),
        "max_steps": float(max_steps),
        "growth_steps_executed": float(total_steps),
        "first_hit_step": float(first_hit_step) if first_hit_step is not None else float("nan"),
        "hit_target_band": 1 if first_hit_step is not None else 0,
        "in_band_snapshots": float(in_band_snapshots),
        "chosen_from_last_in_band": 1 if last_in_band is not None else 0,
    }
    return chosen, meta


def generate_state(
    ensemble: CalibrationEnsemble,
    *,
    rng_seed: int,
    growth_params: v7.Params,
    method: CalibrationMethod,
) -> Tuple[v7.State, Dict[str, Any]]:
    if method.name == "baseline":
        state = v08b.grow_state_for_ensemble(reference_spec(ensemble), rng_seed=rng_seed, growth_params=growth_params)
        meta = {
            "target_low": float("nan"),
            "target_high": float("nan"),
            "target_rel_tol": float("nan"),
            "min_steps": float(ensemble.burnin_steps),
            "max_steps": float(ensemble.burnin_steps + ensemble.extra_burnin_high),
            "growth_steps_executed": float("nan"),
            "first_hit_step": float("nan"),
            "hit_target_band": 0,
            "in_band_snapshots": float("nan"),
            "chosen_from_last_in_band": 0,
        }
        return state, meta
    if method.name == "adaptive":
        return adaptive_grow_state(ensemble, rng_seed=rng_seed, growth_params=growth_params, method=method)
    raise ValueError(f"Unknown calibration method: {method.name}")


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

RUN_FEATURE_KEYS = [
    "nodes",
    "tokens",
    "beta1",
    "triangles",
    "spectral_radius",
    "dim_proxy",
    "clustering",
    "avg_degree",
    "beta1_per_node",
    "triangles_per_node",
    "spectral_per_sqrtN",
]


def collect_run_row(
    ensemble: CalibrationEnsemble,
    *,
    method: CalibrationMethod,
    growth_params: v7.Params,
    seed: int,
) -> Dict[str, Any]:
    state, meta = generate_state(ensemble, rng_seed=seed, growth_params=growth_params, method=method)
    feat = feature_row(state, rng_seed=seed + 999)
    row: Dict[str, Any] = {
        "ensemble": ensemble.name,
        "target_nodes": ensemble.target_nodes,
        "burnin_label": ensemble.burnin_label,
        "initial_cycle": ensemble.initial_cycle,
        "initial_tokens_nominal": ensemble.initial_tokens,
        "burnin_steps_nominal": ensemble.burnin_steps,
        "extra_burnin_low": ensemble.extra_burnin_low,
        "extra_burnin_high": ensemble.extra_burnin_high,
        "method": method.name,
        "seed": seed,
        **meta,
    }
    row.update({f"realized_{k}": v for k, v in feat.items()})
    row["abs_rel_size_error"] = abs(feat["nodes"] - ensemble.target_nodes) / max(float(ensemble.target_nodes), 1.0)
    row["within_target_band"] = 1 if (
        math.isfinite(meta.get("target_low", float("nan")))
        and meta["target_low"] <= feat["nodes"] <= meta["target_high"]
    ) else (1 if method.name == "baseline" and abs(feat["nodes"] - ensemble.target_nodes) / max(float(ensemble.target_nodes), 1.0) <= 0.10 else 0)
    return row


def summarize_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: Dict[Tuple[str, str, int], List[Dict[str, Any]]] = {}
    for row in rows:
        key = (str(row["method"]), str(row["burnin_label"]), int(row["target_nodes"]))
        groups.setdefault(key, []).append(row)
    out: List[Dict[str, Any]] = []
    for (method, burnin_label, target), sub in sorted(groups.items()):
        rec: Dict[str, Any] = {
            "method": method,
            "burnin_label": burnin_label,
            "target_nodes": target,
            "runs": len(sub),
            "hit_rate": mean_or_nan(row["within_target_band"] for row in sub),
            "mean_abs_rel_size_error": mean_or_nan(row["abs_rel_size_error"] for row in sub),
            "sd_abs_rel_size_error": sd_or_zero(row["abs_rel_size_error"] for row in sub),
            "mean_hit_target_band": mean_or_nan(row["hit_target_band"] for row in sub),
            "mean_growth_steps_executed": mean_or_nan(safe_float(row.get("growth_steps_executed"), float("nan")) for row in sub),
            "mean_first_hit_step": mean_or_nan(safe_float(row.get("first_hit_step"), float("nan")) for row in sub),
        }
        vals_nodes = [safe_float(row["realized_nodes"], float("nan")) for row in sub]
        rec["mean_realized_nodes"] = mean_or_nan(vals_nodes)
        rec["sd_realized_nodes"] = sd_or_zero(vals_nodes)
        rec["min_realized_nodes"] = min(v for v in vals_nodes if math.isfinite(v)) if vals_nodes else float("nan")
        rec["max_realized_nodes"] = max(v for v in vals_nodes if math.isfinite(v)) if vals_nodes else float("nan")
        rec["q10_realized_nodes"] = quantile(vals_nodes, 0.10)
        rec["q25_realized_nodes"] = quantile(vals_nodes, 0.25)
        rec["q50_realized_nodes"] = quantile(vals_nodes, 0.50)
        rec["q75_realized_nodes"] = quantile(vals_nodes, 0.75)
        rec["q90_realized_nodes"] = quantile(vals_nodes, 0.90)
        for key in RUN_FEATURE_KEYS[1:]:
            vals = [safe_float(row[f"realized_{key}"], float("nan")) for row in sub]
            rec[f"mean_realized_{key}"] = mean_or_nan(vals)
            rec[f"sd_realized_{key}"] = sd_or_zero(vals)
        out.append(rec)
    return out


def size_overlap_rows(summary_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_group: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for row in summary_rows:
        by_group.setdefault((str(row["method"]), str(row["burnin_label"])), []).append(row)
    out: List[Dict[str, Any]] = []
    for (method, burnin_label), sub in sorted(by_group.items()):
        sub_sorted = sorted(sub, key=lambda r: int(r["target_nodes"]))
        for a, b in zip(sub_sorted[:-1], sub_sorted[1:]):
            a_lo = safe_float(a["q10_realized_nodes"])
            a_hi = safe_float(a["q90_realized_nodes"])
            b_lo = safe_float(b["q10_realized_nodes"])
            b_hi = safe_float(b["q90_realized_nodes"])
            overlap = max(0.0, min(a_hi, b_hi) - max(a_lo, b_lo))
            union = max(a_hi, b_hi) - min(a_lo, b_lo)
            out.append({
                "method": method,
                "burnin_label": burnin_label,
                "target_a": int(a["target_nodes"]),
                "target_b": int(b["target_nodes"]),
                "a_q10": a_lo,
                "a_q90": a_hi,
                "b_q10": b_lo,
                "b_q90": b_hi,
                "gap_q90_to_q10": b_lo - a_hi,
                "overlap_width": overlap,
                "overlap_fraction": (overlap / union) if union > 0 else 0.0,
                "strictly_separated": 1 if a_hi < b_lo else 0,
            })
    return out


def usable_levels(summary_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    by_group: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for row in summary_rows:
        by_group.setdefault((str(row["method"]), str(row["burnin_label"])), []).append(row)
    for (method, burnin_label), sub in sorted(by_group.items()):
        sub_sorted = sorted(sub, key=lambda r: int(r["target_nodes"]))
        chosen: List[int] = []
        last_q90 = -float("inf")
        for row in sub_sorted:
            q10 = safe_float(row["q10_realized_nodes"])
            q90 = safe_float(row["q90_realized_nodes"])
            if not chosen:
                chosen.append(int(row["target_nodes"]))
                last_q90 = q90
            else:
                if q10 > last_q90:
                    chosen.append(int(row["target_nodes"]))
                    last_q90 = q90
        out.append({
            "method": method,
            "burnin_label": burnin_label,
            "usable_nominal_levels": ",".join(str(x) for x in chosen),
            "usable_level_count": len(chosen),
        })
    return out


def calibration_markdown(summary_rows: List[Dict[str, Any]], overlap_rows: List[Dict[str, Any]], usable_rows: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# v0.10b ensemble calibration")
    lines.append("")
    lines.append("Dette dokumentet kalibrerer den naturlige ensemble-generatoren før videre asymptotisk tolkning.")
    lines.append("Målet er å skille tydelig mellom nominell størrelse, realisert initial størrelse og senere dynamisk utvikling.")
    lines.append("")
    lines.append("## Hovedpoeng")
    lines.append("")
    lines.append("- `baseline` = gammel generatorlogikk med fast burn-in og ekstra burn-in.")
    lines.append("- `adaptive` = samme mikrodynamikk, men med en enkel, dokumentert størrelses-kalibrering som stopper på et in-band snapshot hvis mulig.")
    lines.append("- Et størrelsesnivå regnes bare som operativt separert hvis 10–90% intervallene ikke overlapper med nabonivået.")
    lines.append("")
    lines.append("## Oppsummering av realiserte størrelser")
    lines.append("")
    headers = [
        "method", "burnin", "target", "mean_realized", "sd", "q10", "q90", "hit_rate", "abs_rel_err"
    ]
    table_rows = []
    for row in sorted(summary_rows, key=lambda r: (r["method"], r["burnin_label"], int(r["target_nodes"]))):
        table_rows.append([
            str(row["method"]),
            str(row["burnin_label"]),
            str(int(row["target_nodes"])),
            f"{safe_float(row['mean_realized_nodes']):.1f}",
            f"{safe_float(row['sd_realized_nodes']):.1f}",
            f"{safe_float(row['q10_realized_nodes']):.1f}",
            f"{safe_float(row['q90_realized_nodes']):.1f}",
            f"{safe_float(row['hit_rate']):.2f}",
            f"{safe_float(row['mean_abs_rel_size_error']):.3f}",
        ])
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for r in table_rows:
        lines.append("| " + " | ".join(r) + " |")
    lines.append("")
    lines.append("## Overlapp mellom nabonivåer")
    lines.append("")
    headers2 = ["method", "burnin", "A", "B", "gap_q90_to_q10", "overlap_fraction", "strictly_separated"]
    lines.append("| " + " | ".join(headers2) + " |")
    lines.append("| " + " | ".join("---" for _ in headers2) + " |")
    for row in sorted(overlap_rows, key=lambda r: (r["method"], r["burnin_label"], int(r["target_a"]))):
        lines.append("| " + " | ".join([
            str(row["method"]),
            str(row["burnin_label"]),
            str(int(row["target_a"])),
            str(int(row["target_b"])),
            f"{safe_float(row['gap_q90_to_q10']):.1f}",
            f"{safe_float(row['overlap_fraction']):.2f}",
            str(int(row["strictly_separated"])),
        ]) + " |")
    lines.append("")
    lines.append("## Grei operativ lesning")
    lines.append("")
    for row in sorted(usable_rows, key=lambda r: (r["method"], r["burnin_label"])):
        lines.append(f"- `{row['method']}` / `{row['burnin_label']}`: brukbare nominelle nivåer = {row['usable_nominal_levels']} (count={int(row['usable_level_count'])})")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("Hvis et nominelt nivå realiserer omtrent samme nodeantall som et nabonivå, er det et generatorproblem, ikke et asymptotisk funn.")
    lines.append("Negative eller ekstreme eksponenter under slike forhold må tolkes som metodiske artefakter inntil generatoren er reparert eller byttet ut.")
    lines.append("")
    return "\n".join(lines) + "\n"


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.10b ensemble calibration")
    ap.add_argument("--seeds", type=int, default=4, help="growth seeds per ensemble/method")
    ap.add_argument("--output-prefix", type=str, default="Documentation/v10b")
    ap.add_argument(
        "--report-md",
        type=str,
        default="Documentation/relasjonell_universgraf_v0_10b_generator_kalibrering_og_growth_regimer.md",
    )
    ap.add_argument(
        "--operational-csv",
        type=str,
        default="Documentation/v10b_operational_levels.csv",
    )
    ap.add_argument("--targets", type=str, default="24,48,96,192,256")
    ap.add_argument("--adaptive-max-growth-factor", type=float, default=2.0)
    ap.add_argument("--adaptive-rel-tol", type=float, default=0.10)
    ap.add_argument("--adaptive-hold-steps", type=int, default=30)
    return ap


def main() -> None:
    ap = build_argparser()
    args = ap.parse_args()

    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = build_ensembles(targets)
    methods = [
        CalibrationMethod("baseline", rel_tol=0.10, max_growth_factor=1.0, min_fraction_of_baseline=1.0, hold_steps=0, snapshot_stride=1),
        CalibrationMethod("adaptive", rel_tol=args.adaptive_rel_tol, max_growth_factor=args.adaptive_max_growth_factor, min_fraction_of_baseline=0.30, hold_steps=args.adaptive_hold_steps, snapshot_stride=5),
    ]
    growth_params = reference_growth_params()
    growth_seeds = [1000 + i * 17 for i in range(args.seeds)]

    run_rows: List[Dict[str, Any]] = []
    for method in methods:
        for ensemble in ensembles:
            for seed in growth_seeds:
                run_rows.append(collect_run_row(ensemble, method=method, growth_params=growth_params, seed=seed))

    summary_rows = summarize_rows(run_rows)
    overlap_rows = size_overlap_rows(summary_rows)
    usable_rows = usable_levels(summary_rows)

    prefix = args.output_prefix
    write_csv(f"{prefix}_ensemble_calibration_runs.csv", run_rows)
    write_csv(f"{prefix}_ensemble_calibration_summary.csv", summary_rows)
    write_csv(f"{prefix}_ensemble_size_overlap.csv", overlap_rows)
    write_csv(f"{prefix}_usable_levels.csv", usable_rows)
    write_csv(args.operational_csv, usable_rows)
    report_path = Path(args.report_md)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(calibration_markdown(summary_rows, overlap_rows, usable_rows), encoding="utf-8")
    Path(f"{prefix}_ensemble_calibration.md").write_text(calibration_markdown(summary_rows, overlap_rows, usable_rows), encoding="utf-8")


if __name__ == "__main__":
    main()
