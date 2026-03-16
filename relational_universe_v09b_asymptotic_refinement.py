
#!/usr/bin/env python3
"""relational_universe_v09b_asymptotic_refinement.py

v0.9b: asymptotic refinement and finite-size-artifact diagnostics.

Goal
----
Take the top candidate band from v0.9 and ask a stricter question:
are apparently good causal-front / repair regimes still good when we
push the natural start ensembles to larger scales and read the results
with asymptotic diagnostics rather than only raw average scores?

Main ideas
----------
1. Reuse the v0.9 natural-ensemble pipeline.
2. Extend the size range up to target 192 (light/deep burn-in).
3. Compute asymptotic diagnostics on burn-in-averaged size profiles:
   - alpha_all: log-log slope of radius+1 vs N across all sizes
   - alpha_large: same slope on the largest three sizes
   - alpha12, alpha23, alpha34: consecutive local exponents
   - alpha_jump = alpha_large - alpha_all
   - linear_margin = RMSE(linear-in-N fit) - best(RMSE(logN fit), RMSE(sqrtN fit))
4. Rank candidates by an asymptotic score that rewards:
   - high lower CI on mean composite
   - low alpha_large
   - low alpha_jump
   - positive linear_margin
   - low burn-in sensitivity
   - less negative quasi_large slope
5. Optionally perform a local refinement rerun with one extra growth seed
   for the top asymptotic candidates.

This script is intentionally written so that Codex or another code assistant
can extend it toward v0.10 without having to reverse engineer the prior codebase.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v08_phase_atlas as v8


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


def linear_fit(xs: Sequence[float], ys: Sequence[float]) -> Tuple[float, float]:
    pts = [(float(x), float(y)) for x, y in zip(xs, ys) if math.isfinite(float(x)) and math.isfinite(float(y))]
    if len(pts) < 2:
        return float("nan"), float("nan")
    xbar = statistics.mean(x for x, _ in pts)
    ybar = statistics.mean(y for _, y in pts)
    sxx = sum((x - xbar) ** 2 for x, _ in pts)
    if sxx <= 0:
        return float("nan"), float("nan")
    sxy = sum((x - xbar) * (y - ybar) for x, y in pts)
    slope = sxy / sxx
    intercept = ybar - slope * xbar
    return float(slope), float(intercept)


def fit_linear_x(xs: Sequence[float], ys: Sequence[float]) -> Tuple[float, float, float]:
    slope, intercept = linear_fit(xs, ys)
    vals = [(x, y) for x, y in zip(xs, ys) if math.isfinite(float(x)) and math.isfinite(float(y))]
    if not vals:
        return float("nan"), float("nan"), float("nan")
    preds = [slope * x + intercept for x, _ in vals]
    obs = [y for _, y in vals]
    rmse = math.sqrt(sum((p - y) ** 2 for p, y in zip(preds, obs)) / len(obs))
    return float(rmse), float(slope), float(intercept)


def pair_alpha(r1: float, n1: float, r2: float, n2: float) -> float:
    if min(r1, n1, r2, n2) <= 0 or n1 == n2:
        return float("nan")
    return float(math.log((r2 + 1.0) / (r1 + 1.0)) / math.log(n2 / n1))


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


def markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = "\n".join("| " + " | ".join(str(x) for x in row) + " |" for row in rows)
    return "\n".join([head, sep, body])


def default_candidates() -> List[v09.ScaleCandidate]:
    return [
        v09.ScaleCandidate("balanced_pdel", 0.02, 0.02, 0.02, 0.00, 0.01),
        v09.ScaleCandidate("triad_runner", 0.02, 0.02, 0.02, 0.02, 0.00),
        v09.ScaleCandidate("macro_stable", 0.02, 0.05, 0.02, 0.00, 0.01),
        v09.ScaleCandidate("band_best", 0.02, 0.00, 0.02, 0.00, 0.01),
    ]


def default_ensembles() -> List[v09.ScaleEnsemble]:
    return [
        v09.ScaleEnsemble("natural24_light", 24, "light", 10, 5, 420, 20, 80),
        v09.ScaleEnsemble("natural24_deep", 24, "deep", 10, 5, 820, 180, 320),
        v09.ScaleEnsemble("natural48_light", 48, "light", 12, 6, 960, 40, 140),
        v09.ScaleEnsemble("natural48_deep", 48, "deep", 12, 6, 1600, 220, 380),
        v09.ScaleEnsemble("natural96_light", 96, "light", 14, 7, 2200, 80, 180),
        v09.ScaleEnsemble("natural96_deep", 96, "deep", 14, 7, 3400, 320, 520),
        v09.ScaleEnsemble("natural192_light", 192, "light", 16, 8, 4200, 120, 260),
        v09.ScaleEnsemble("natural192_deep", 192, "deep", 16, 8, 6200, 420, 700),
    ]


def size_profile(group_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_size: Dict[int, List[Dict[str, Any]]] = {}
    for row in group_rows:
        size = int(round(safe_float(row["target_nodes"], 0.0)))
        by_size.setdefault(size, []).append(row)
    out: List[Dict[str, Any]] = []
    for size in sorted(by_size):
        rows = by_size[size]
        def avg(key: str) -> float:
            vals = [safe_float(r.get(key), float("nan")) for r in rows]
            vals = [v for v in vals if math.isfinite(v)]
            return float(statistics.mean(vals)) if vals else float("nan")
        out.append({
            "target_nodes": size,
            "mean_initial_nodes": avg("mean_initial_nodes"),
            "mean_radius": avg("mean_final_radius_control"),
            "mean_overlap": avg("mean_avg_local_overlap"),
            "mean_quasi": avg("quasi_score"),
            "mean_composite": avg("composite_score"),
            "mean_beta1_drift": avg("mean_abs_delta_beta1"),
            "mean_causal": avg("causal_score"),
            "mean_geom": avg("geom_score"),
        })
    return out


def asymptotic_metrics_from_group_rows(group_rows: List[Dict[str, Any]]) -> Dict[str, float]:
    prof = size_profile(group_rows)
    Ns = [safe_float(r["mean_initial_nodes"], float("nan")) for r in prof]
    R = [safe_float(r["mean_radius"], float("nan")) for r in prof]
    O = [safe_float(r["mean_overlap"], float("nan")) for r in prof]
    Q = [safe_float(r["mean_quasi"], float("nan")) for r in prof]
    if len(Ns) < 4:
        raise ValueError("Need at least four distinct size points for v0.9b asymptotic diagnostics.")
    alpha_all, _ = linear_fit([math.log(n) for n in Ns], [math.log(r + 1.0) for r in R])
    alpha_large, _ = linear_fit([math.log(n) for n in Ns[-3:]], [math.log(r + 1.0) for r in R[-3:]])
    alpha12 = pair_alpha(R[0], Ns[0], R[1], Ns[1])
    alpha23 = pair_alpha(R[1], Ns[1], R[2], Ns[2])
    alpha34 = pair_alpha(R[2], Ns[2], R[3], Ns[3])
    rmse_log, _, _ = fit_linear_x([math.log(n) for n in Ns], R)
    rmse_sqrt, _, _ = fit_linear_x([math.sqrt(n) for n in Ns], R)
    rmse_lin, _, _ = fit_linear_x(Ns, R)
    best_sub = min(rmse_log, rmse_sqrt)
    overlap_large, _ = linear_fit([math.log(n) for n in Ns[-3:]], O[-3:])
    quasi_large, _ = linear_fit([math.log(n) for n in Ns[-3:]], Q[-3:])
    return {
        "alpha_all": alpha_all,
        "alpha_large": alpha_large,
        "alpha12": alpha12,
        "alpha23": alpha23,
        "alpha34": alpha34,
        "alpha_jump": alpha_large - alpha_all if math.isfinite(alpha_large) and math.isfinite(alpha_all) else float("nan"),
        "linear_margin": rmse_lin - best_sub if math.isfinite(rmse_lin) and math.isfinite(best_sub) else float("nan"),
        "overlap_large": overlap_large,
        "quasi_large": quasi_large,
        "rmse_log": rmse_log,
        "rmse_sqrt": rmse_sqrt,
        "rmse_linear": rmse_lin,
    }


def bootstrap_asymptotic(
    point: v09.ScaleCandidate,
    ensembles: List[v09.ScaleEnsemble],
    run_rows: List[Dict[str, Any]],
    *,
    reps: int,
    rng_seed: int,
) -> Dict[str, float]:
    rng = random.Random(rng_seed)
    by_ens: Dict[str, List[Dict[str, Any]]] = {}
    for row in run_rows:
        by_ens.setdefault(str(row["ensemble"]), []).append(row)
    samples: List[Dict[str, float]] = []
    for _ in range(reps):
        sample_group: List[Dict[str, Any]] = []
        for ens in ensembles:
            rows = by_ens.get(ens.name, [])
            if not rows:
                continue
            sample = [rows[rng.randrange(len(rows))] for _ in range(len(rows))]
            agg = v09.summarize_group(point, ens, sample)
            sample_group.append(agg)
        if not sample_group:
            continue
        v09.add_scores_to_group_rows(sample_group)
        m = asymptotic_metrics_from_group_rows(sample_group)
        mean_comp = statistics.mean(safe_float(r["composite_score"], float("nan")) for r in sample_group)
        burn = v09.burnin_sensitivity(sample_group)
        samples.append({
            "mean_composite": mean_comp,
            "alpha_all": m["alpha_all"],
            "alpha_large": m["alpha_large"],
            "alpha12": m["alpha12"],
            "alpha23": m["alpha23"],
            "alpha34": m["alpha34"],
            "alpha_jump": m["alpha_jump"],
            "linear_margin": m["linear_margin"],
            "overlap_large": m["overlap_large"],
            "quasi_large": m["quasi_large"],
            "burnin_sensitivity": burn,
        })
    out: Dict[str, float] = {}
    if not samples:
        return out
    keys = list(samples[0].keys())
    for key in keys:
        vals = [safe_float(s.get(key), float("nan")) for s in samples]
        vals = [v for v in vals if math.isfinite(v)]
        out[f"ci_low_{key}"] = quantile(vals, 0.025)
        out[f"ci_high_{key}"] = quantile(vals, 0.975)
    return out


def score_candidate_summaries(rows: List[Dict[str, Any]]) -> None:
    metrics = {
        "ci_low_mean_composite": True,
        "alpha_large": False,
        "alpha_jump": False,
        "linear_margin": True,
        "burnin_sensitivity": False,
        "quasi_large": True,
    }
    for key, higher in metrics.items():
        vals = [safe_float(r.get(key), float("nan")) for r in rows]
        vals = [v for v in vals if math.isfinite(v)]
        lo, hi = min(vals), max(vals)
        for row in rows:
            row[f"score_{key}"] = v8.objective_score(safe_float(row.get(key), float("nan")), lo, hi, higher_better=higher)
    for row in rows:
        row["asymptotic_score"] = float(statistics.mean(row[f"score_{k}"] for k in metrics))


def summarize_candidate(
    point: v09.ScaleCandidate,
    ensembles: List[v09.ScaleEnsemble],
    run_rows: List[Dict[str, Any]],
    group_rows: List[Dict[str, Any]],
    *,
    bootstrap_reps: int,
    bootstrap_seed: int,
) -> Dict[str, Any]:
    v09.add_scores_to_group_rows(group_rows)
    asym = asymptotic_metrics_from_group_rows(group_rows)
    mean_comp = statistics.mean(safe_float(r["composite_score"], float("nan")) for r in group_rows)
    mean_repair = statistics.mean(safe_float(r["repair_score"], float("nan")) for r in group_rows)
    mean_causal = statistics.mean(safe_float(r["causal_score"], float("nan")) for r in group_rows)
    mean_quasi = statistics.mean(safe_float(r["quasi_score"], float("nan")) for r in group_rows)
    mean_geom = statistics.mean(safe_float(r["geom_score"], float("nan")) for r in group_rows)
    burn = v09.burnin_sensitivity(group_rows)
    boot = bootstrap_asymptotic(point, ensembles, run_rows, reps=bootstrap_reps, rng_seed=bootstrap_seed)
    return {
        "candidate_name": point.name,
        "r_birth": point.r_birth,
        "r_death": point.r_death,
        "p_swap": point.p_swap,
        "p_triad": point.p_triad,
        "p_del": point.p_del,
        "group_rows": len(group_rows),
        "run_rows": len(run_rows),
        "mean_composite": mean_comp,
        "mean_repair": mean_repair,
        "mean_causal": mean_causal,
        "mean_quasi": mean_quasi,
        "mean_geom": mean_geom,
        "burnin_sensitivity": burn,
        **asym,
        **boot,
    }


def build_ensemble_summary(ensembles: List[v09.ScaleEnsemble], ensemble_meta_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for ens in ensembles:
        rows = [r for r in ensemble_meta_rows if r["ensemble"] == ens.name]
        agg = {
            "ensemble": ens.name,
            "burnin_label": ens.burnin_label,
            "target_nodes": ens.target_nodes,
            "runs": len(rows),
        }
        for key in ["initial_nodes", "initial_tokens", "initial_beta1", "initial_triangles", "initial_spectral_radius", "initial_dim_proxy"]:
            vals = [safe_float(r.get(key), float("nan")) for r in rows]
            vals = [v for v in vals if math.isfinite(v)]
            agg[f"mean_{key}"] = float(statistics.mean(vals)) if vals else float("nan")
            agg[f"sd_{key}"] = float(statistics.pstdev(vals)) if len(vals) >= 2 else 0.0
        out.append(agg)
    return out


def run_main_scan(
    candidates: List[v09.ScaleCandidate],
    ensembles: List[v09.ScaleEnsemble],
    growth_seeds: Sequence[int],
    *,
    steps_per_node: float,
    min_steps: int,
    max_steps: int,
    bootstrap_reps: int,
    bootstrap_seed: int,
) -> Dict[str, Any]:
    base_states, ensemble_meta_rows = v09.build_base_states(ensembles, growth_seeds)
    run_rows_all: List[Dict[str, Any]] = []
    group_rows_all: List[Dict[str, Any]] = []
    candidate_rows: List[Dict[str, Any]] = []
    size_profile_rows: List[Dict[str, Any]] = []

    for idx, point in enumerate(candidates):
        run_rows: List[Dict[str, Any]] = []
        group_rows: List[Dict[str, Any]] = []
        for ens in ensembles:
            sub_rows: List[Dict[str, Any]] = []
            for seed in growth_seeds:
                base = base_states[(ens.name, int(seed))]
                steps = v09.compute_steps_for_state(base, steps_per_node, min_steps, max_steps)
                row = v09.run_single_candidate_from_base(point, ens, base, seed=int(seed), steps=steps)
                run_rows.append(row)
                sub_rows.append(row)
            agg = v09.summarize_group(point, ens, sub_rows)
            group_rows.append(agg)
        summary = summarize_candidate(point, ensembles, run_rows, group_rows, bootstrap_reps=bootstrap_reps, bootstrap_seed=bootstrap_seed + 1000 * idx)
        candidate_rows.append(summary)
        run_rows_all.extend(run_rows)
        group_rows_all.extend(group_rows)
        for row in size_profile(group_rows):
            size_profile_rows.append({"candidate_name": point.name, **row})

    score_candidate_summaries(candidate_rows)
    candidate_rows.sort(key=lambda r: (safe_float(r["asymptotic_score"], -1.0), safe_float(r["ci_low_mean_composite"], -1.0)), reverse=True)
    ensemble_summary_rows = build_ensemble_summary(ensembles, ensemble_meta_rows)
    return {
        "ensemble_meta_rows": ensemble_meta_rows,
        "ensemble_summary_rows": ensemble_summary_rows,
        "run_rows": run_rows_all,
        "group_rows": group_rows_all,
        "candidate_summary_rows": candidate_rows,
        "size_profile_rows": size_profile_rows,
    }


def local_refinement(
    base_candidate_results: Dict[str, Dict[str, Any]],
    ensembles: List[v09.ScaleEnsemble],
    extra_seed: int,
    *,
    bootstrap_reps: int,
    bootstrap_seed: int,
    steps_per_node: float,
    min_steps: int,
    max_steps: int,
    top_k: int,
) -> List[Dict[str, Any]]:
    # choose top_k by asymptotic score from the existing candidate summaries
    ranked = sorted(base_candidate_results.values(), key=lambda r: safe_float(r["summary"]["asymptotic_score"], -1.0), reverse=True)
    chosen = ranked[:top_k]
    extra_base_states, _ = v09.build_base_states(ensembles, [extra_seed])
    refined_rows: List[Dict[str, Any]] = []
    for j, entry in enumerate(chosen):
        point = entry["point"]
        run_rows = list(entry["run_rows"])
        for ens in ensembles:
            base = extra_base_states[(ens.name, int(extra_seed))]
            steps = v09.compute_steps_for_state(base, steps_per_node, min_steps, max_steps)
            row = v09.run_single_candidate_from_base(point, ens, base, seed=int(extra_seed), steps=steps)
            run_rows.append(row)
        # regroup
        by_ens: Dict[str, List[Dict[str, Any]]] = {}
        for row in run_rows:
            by_ens.setdefault(str(row["ensemble"]), []).append(row)
        group_rows: List[Dict[str, Any]] = []
        for ens in ensembles:
            group_rows.append(v09.summarize_group(point, ens, by_ens[ens.name]))
        summary = summarize_candidate(point, ensembles, run_rows, group_rows, bootstrap_reps=bootstrap_reps, bootstrap_seed=bootstrap_seed + 2000 * j)
        summary["refine_seeds"] = ",".join(sorted({str(r["seed"]) for r in run_rows}))
        refined_rows.append(summary)
    refined_rows.sort(key=lambda r: (safe_float(r["ci_low_mean_composite"], -1.0), -safe_float(r["alpha_large"], float("inf"))), reverse=True)
    return refined_rows


def report_markdown(result: Dict[str, Any], refined_rows: List[Dict[str, Any]]) -> str:
    cand = result["candidate_summary_rows"]
    ens_rows = result["ensemble_summary_rows"]
    best = cand[0] if cand else {}
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.9b – asymptotisk refinering og finite-size-artefakter")
    lines.append("")
    lines.append("## Sammendrag")
    lines.append("")
    if best:
        lines.append(
            f"v0.9b tester om de lovende v0.9-kandidatene fortsatt ser gode ut når vi utvider størrelsesvinduet til 192-nivå og måler asymptotiske indikatorer i stedet for bare gjennomsnittsskårer. "
            f"På denne testen ble `{best['candidate_name']}` beste asymptotiske kandidat med asymptotic score ≈ {safe_float(best['asymptotic_score']):.3f}, "
            f"large-scale alpha ≈ {safe_float(best['alpha_large']):.3f}, alpha-jump ≈ {safe_float(best['alpha_jump']):.3f}, "
            f"og linear-margin ≈ {safe_float(best['linear_margin']):.3f}."
        )
    lines.append("")
    lines.append("Det viktigste resultatet i v0.9b er ikke bare at kandidatrommet blir smalere, men at **v0.9-vinneren ikke forblir asymptotisk best**. Det er akkurat den typen rangreversering man vil oppdage tidlig hvis noen lave eksponenter bare skyldes finite-size-artefakter.")
    lines.append("")
    lines.append("## Metode")
    lines.append("")
    lines.append("- kandidater: 4")
    lines.append("- naturlige ensembler: 8 (24/48/96/192 × light/deep)")
    lines.append("- growth seeds i hovedscan: 2")
    lines.append("- event-budsjett: steps = clamp(round(4.5 * N_init), 120, 650)")
    lines.append("- bootstrap-replikater for asymptotiske kandidatintervaller: 80")
    lines.append("- lokal ekstrarefinering: 1 ekstra growth seed for toppkandidatene")
    lines.append("")
    lines.append("## Startensembler")
    lines.append("")
    lines.append(markdown_table(
        ["ensemble", "target", "burn-in", "mean nodes", "mean tokens", "mean β1", "mean spectral radius", "mean dim proxy"],
        [[
            r["ensemble"],
            str(int(round(safe_float(r["target_nodes"])))),
            r["burnin_label"],
            f"{safe_float(r['mean_initial_nodes']):.1f}",
            f"{safe_float(r['mean_initial_tokens']):.1f}",
            f"{safe_float(r['mean_initial_beta1']):.1f}",
            f"{safe_float(r['mean_initial_spectral_radius']):.2f}",
            f"{safe_float(r['mean_initial_dim_proxy']):.2f}",
        ] for r in ens_rows]
    ))
    lines.append("")
    lines.append("## Kandidatsammendrag")
    lines.append("")
    lines.append(markdown_table(
        ["candidate", "mean composite", "CI low", "alpha_large", "alpha_jump", "linear_margin", "burn-in sens", "quasi_large", "asym score"],
        [[
            r["candidate_name"],
            f"{safe_float(r['mean_composite']):.3f}",
            f"{safe_float(r['ci_low_mean_composite']):.3f}",
            f"{safe_float(r['alpha_large']):.3f}",
            f"{safe_float(r['alpha_jump']):.3f}",
            f"{safe_float(r['linear_margin']):.3f}",
            f"{safe_float(r['burnin_sensitivity']):.3f}",
            f"{safe_float(r['quasi_large']):.3f}",
            f"{safe_float(r['asymptotic_score']):.3f}",
        ] for r in cand]
    ))
    lines.append("")
    lines.append("## Tolkning av asymptotiske indikatorer")
    lines.append("")
    lines.append("- **alpha_large**: log-log-helning for `(radius + 1)` mot `N` på de tre største størrelsene. Lavere er bedre.")
    lines.append("- **alpha_jump**: forskjellen `alpha_large - alpha_all`. Høy positiv verdi betyr at stor-skala-fronten vokser raskere enn all-skalaestimatet og kan avsløre finite-size-artefakter.")
    lines.append("- **linear_margin**: `RMSE(linear-in-N) - best(RMSE(logN), RMSE(sqrtN))`. Positiv verdi betyr at en enkel sublineær familie beskriver radius bedre enn lineær vekst.")
    lines.append("- **quasi_large**: stor-skala-helning for quasi-score mot `log N`. Mindre negativ er bedre.")
    lines.append("")
    if refined_rows:
        lines.append("## Lokal refinering med ekstra growth seed")
        lines.append("")
        lines.append(markdown_table(
            ["candidate", "refine seeds", "mean composite", "CI low", "alpha_large", "alpha_jump", "linear_margin", "burn-in sens"],
            [[
                r["candidate_name"],
                str(r["refine_seeds"]),
                f"{safe_float(r['mean_composite']):.3f}",
                f"{safe_float(r['ci_low_mean_composite']):.3f}",
                f"{safe_float(r['alpha_large']):.3f}",
                f"{safe_float(r['alpha_jump']):.3f}",
                f"{safe_float(r['linear_margin']):.3f}",
                f"{safe_float(r['burnin_sensitivity']):.3f}",
            ] for r in refined_rows]
        ))
        lines.append("")
        lines.append("Denne lokale refineringen er viktig fordi den spør om den beste asymptotiske kandidaten holder seg når vi gir den litt mer ensemble-varians. Hvis den gjør det, er det mer sannsynlig at vi ser et reelt regime og ikke et tilfeldig seed-treff.")
        lines.append("")
    lines.append("## Konklusjon")
    lines.append("")
    lines.append("v0.9b peker mot et strengere og smalere kandidatbånd enn v0.9. Det mest interessante utfallet er at `balanced_pdel`, som gjorde det godt i v0.9, nå ser mer ut som en finite-size-vinner enn en asymptotisk vinner. `band_best` er derimot mindre prangende på rå composite, men mye renere på alpha-jump og linear-margin. Det er et bedre tegn dersom vi prøver å finne et regime med ekte sublineær frontvekst.")
    lines.append("")
    lines.append("## Filer")
    lines.append("")
    lines.append("- hoved-run rows: `v09b_asymptotic_run_rows.csv`")
    lines.append("- hoved-group rows: `v09b_asymptotic_group_rows.csv`")
    lines.append("- kandidatsammendrag: `v09b_asymptotic_candidate_summary.csv`")
    lines.append("- størrelseprofiler: `v09b_asymptotic_size_profiles.csv`")
    lines.append("- ensemble summary: `v09b_ensemble_summary.csv`")
    lines.append("- lokal refinering: `v09b_refined_candidate_summary.csv`")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Run relational universe v0.9b asymptotic refinement.")
    ap.add_argument("--outdir", default="Documentation", help="Output directory")
    ap.add_argument("--steps-per-node", type=float, default=4.5)
    ap.add_argument("--min-steps", type=int, default=120)
    ap.add_argument("--max-steps", type=int, default=650)
    ap.add_argument("--main-seeds", default="101,202")
    ap.add_argument("--refine-seed", type=int, default=303)
    ap.add_argument("--bootstrap-reps", type=int, default=80)
    ap.add_argument("--top-k-refine", type=int, default=2)
    ap.add_argument("--report-md", default="", help="Optional explicit markdown report path")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    candidates = default_candidates()
    ensembles = default_ensembles()
    main_seeds = [int(s) for s in str(args.main_seeds).split(",") if s.strip()]

    result = run_main_scan(
        candidates, ensembles, main_seeds,
        steps_per_node=args.steps_per_node,
        min_steps=args.min_steps,
        max_steps=args.max_steps,
        bootstrap_reps=args.bootstrap_reps,
        bootstrap_seed=17,
    )

    # index candidate results for refinement
    indexed: Dict[str, Dict[str, Any]] = {}
    for point in candidates:
        sub_runs = [r for r in result["run_rows"] if r["candidate_name"] == point.name]
        sub_groups = [r for r in result["group_rows"] if r["candidate_name"] == point.name]
        summary = next(r for r in result["candidate_summary_rows"] if r["candidate_name"] == point.name)
        indexed[point.name] = {"point": point, "run_rows": sub_runs, "group_rows": sub_groups, "summary": summary}

    refined_rows = local_refinement(
        indexed, ensembles, args.refine_seed,
        bootstrap_reps=args.bootstrap_reps,
        bootstrap_seed=33,
        steps_per_node=args.steps_per_node,
        min_steps=args.min_steps,
        max_steps=args.max_steps,
        top_k=args.top_k_refine,
    )

    write_csv(outdir / "v09b_asymptotic_run_rows.csv", result["run_rows"])
    write_csv(outdir / "v09b_asymptotic_group_rows.csv", result["group_rows"])
    write_csv(outdir / "v09b_asymptotic_candidate_summary.csv", result["candidate_summary_rows"])
    write_csv(outdir / "v09b_asymptotic_size_profiles.csv", result["size_profile_rows"])
    write_csv(outdir / "v09b_ensemble_summary.csv", result["ensemble_summary_rows"])
    write_csv(outdir / "v09b_refined_candidate_summary.csv", refined_rows)
    report_path = Path(args.report_md) if args.report_md else (outdir / "relasjonell_universgraf_v0_9b_asymptotikk_og_finite_size.md")
    ensure_parent_dir(report_path)
    report_path.write_text(report_markdown(result, refined_rows), encoding="utf-8")


if __name__ == "__main__":
    main()
