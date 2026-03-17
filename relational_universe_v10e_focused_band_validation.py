#!/usr/bin/env python3
"""v0.10e focused validation and local band search around band_best.

This step follows v0.10b-v0.10d:
- use the recommended ensemble regime fast_balanced / deep,
- keep the candidate set narrow and local around band_best,
- increase replication moderately (more growth seeds and more run seeds than v0.10d),
- add explicit bootstrap uncertainty and pairwise robustness probabilities,
- report realized initial sizes separately from later dynamics.

The script is intentionally self-contained and depends only on the active files
on disk that define the project state.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v09b_asymptotic_refinement as v09b
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10c_growth_regime_search as v10c


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


def mean_defined(values: Iterable[float]) -> float:
    vals = [float(v) for v in values if math.isfinite(float(v))]
    return float(statistics.mean(vals)) if vals else float("nan")


def sd_or_zero(values: Iterable[float]) -> float:
    vals = [float(v) for v in values if math.isfinite(float(v))]
    return float(statistics.pstdev(vals)) if len(vals) >= 2 else 0.0


def recommended_regime(name: str = "fast_balanced") -> v10c.FastRegime:
    for reg in v10c.default_regimes():
        if reg.name == name:
            return reg
    raise ValueError(f"Unknown growth regime: {name!r}")


def local_candidates() -> List[v09.ScaleCandidate]:
    return [
        v09.ScaleCandidate("band_best", 0.02, 0.00, 0.02, 0.00, 0.01),
        v09.ScaleCandidate("band_zero_del", 0.02, 0.00, 0.02, 0.00, 0.00),
        v09.ScaleCandidate("band_small_death", 0.02, 0.01, 0.02, 0.00, 0.01),
        v09.ScaleCandidate("band_small_triad", 0.02, 0.00, 0.02, 0.01, 0.01),
        v09.ScaleCandidate("macro_stable", 0.02, 0.05, 0.02, 0.00, 0.01),
    ]


def steps_for_state(nodes: int) -> int:
    return max(220, min(800, int(round(5.0 * nodes))))


def candidate_lookup(candidates: Sequence[v09.ScaleCandidate]) -> Dict[str, v09.ScaleCandidate]:
    return {c.name: c for c in candidates}


def build_bases(
    ensembles: Sequence[v10b.CalibrationEnsemble],
    regime: v10c.FastRegime,
    growth_seeds: Sequence[int],
) -> Tuple[Dict[Tuple[str, int], Any], List[Dict[str, Any]]]:
    base_states: Dict[Tuple[str, int], Any] = {}
    base_rows: List[Dict[str, Any]] = []
    for ens in ensembles:
        for gseed in growth_seeds:
            state, meta = v10c.grow_fast(ens, int(gseed), regime)
            base_states[(ens.name, int(gseed))] = state
            feat = v10c.feature_row(state, rng_seed=int(gseed) + 999)
            base_rows.append(
                {
                    "ensemble": ens.name,
                    "burnin_label": ens.burnin_label,
                    "target_nodes": ens.target_nodes,
                    "growth_seed": int(gseed),
                    **meta,
                    "initial_nodes": feat["nodes"],
                    "initial_tokens": feat["tokens"],
                    "initial_beta1": feat["beta1"],
                    "initial_triangles": feat["triangles"],
                    "initial_spectral_radius": feat["spectral_radius"],
                    "initial_dim_proxy": feat["dim_proxy"],
                    "initial_clustering": feat["clustering"],
                    "initial_avg_degree": feat["avg_degree"],
                    "initial_beta1_per_node": feat["beta1_per_node"],
                    "initial_triangles_per_node": feat["triangles_per_node"],
                    "initial_spectral_per_sqrtN": feat["spectral_per_sqrtN"],
                }
            )
    return base_states, base_rows


def summarize_bases(base_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_target: Dict[int, List[Dict[str, Any]]] = {}
    for row in base_rows:
        by_target.setdefault(int(row["target_nodes"]), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    prev_q90 = float("nan")
    for target in sorted(by_target):
        sub = by_target[target]
        realized = [safe_float(r["initial_nodes"]) for r in sub]
        q10 = quantile(realized, 0.10)
        q90 = quantile(realized, 0.90)
        separated_from_prev = 1
        if math.isfinite(prev_q90):
            separated_from_prev = 1 if q10 > prev_q90 else 0
        prev_q90 = q90
        out.append(
            {
                "target_nodes": target,
                "growth_replicates": len(sub),
                "mean_initial_nodes": mean_defined(realized),
                "sd_initial_nodes": sd_or_zero(realized),
                "q10_initial_nodes": q10,
                "q90_initial_nodes": q90,
                "min_initial_nodes": min(realized) if realized else float("nan"),
                "max_initial_nodes": max(realized) if realized else float("nan"),
                "mean_initial_tokens": mean_defined(safe_float(r["initial_tokens"]) for r in sub),
                "mean_initial_beta1": mean_defined(safe_float(r["initial_beta1"]) for r in sub),
                "mean_initial_triangles": mean_defined(safe_float(r["initial_triangles"]) for r in sub),
                "mean_initial_spectral_radius": mean_defined(safe_float(r["initial_spectral_radius"]) for r in sub),
                "mean_initial_dim_proxy": mean_defined(safe_float(r["initial_dim_proxy"]) for r in sub),
                "mean_initial_clustering": mean_defined(safe_float(r["initial_clustering"]) for r in sub),
                "mean_initial_beta1_per_node": mean_defined(safe_float(r["initial_beta1_per_node"]) for r in sub),
                "mean_initial_triangles_per_node": mean_defined(safe_float(r["initial_triangles_per_node"]) for r in sub),
                "mean_initial_spectral_per_sqrtN": mean_defined(safe_float(r["initial_spectral_per_sqrtN"]) for r in sub),
                "separated_from_prev": separated_from_prev,
            }
        )
    return out


def collect_run_rows(
    candidates: Sequence[v09.ScaleCandidate],
    ensembles: Sequence[v10b.CalibrationEnsemble],
    base_states: Mapping[Tuple[str, int], Any],
    growth_seeds: Sequence[int],
    run_offsets: Sequence[int],
    regime_name: str,
) -> List[Dict[str, Any]]:
    run_rows: List[Dict[str, Any]] = []
    for cand in candidates:
        name_hash = sum(ord(ch) for ch in cand.name) % 997
        for ens in ensembles:
            for gseed in growth_seeds:
                base = base_states[(ens.name, int(gseed))]
                steps = steps_for_state(base.g.num_nodes())
                for off in run_offsets:
                    seed = int(gseed) + int(off) + name_hash
                    row = v09.run_single_candidate_from_base(cand, ens, base, seed=seed, steps=steps)
                    row["growth_regime"] = regime_name
                    row["growth_seed"] = int(gseed)
                    row["run_seed"] = int(seed)
                    row["steps"] = int(steps)
                    run_rows.append(row)
    return run_rows


def summarize_groups(
    candidates: Sequence[v09.ScaleCandidate],
    ensembles: Sequence[v10b.CalibrationEnsemble],
    run_rows: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for cand in candidates:
        for ens in ensembles:
            sub = [r for r in run_rows if r["candidate_name"] == cand.name and r["ensemble"] == ens.name]
            agg = v09.summarize_group(cand, ens, list(sub))
            out.append(agg)
    v09.add_scores_to_group_rows(out)
    return out


def point_candidate_summary(candidate_name: str, group_rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    sub = [r for r in group_rows if r["candidate_name"] == candidate_name]
    asym = v09b.asymptotic_metrics_from_group_rows(list(sub))
    return {
        "candidate_name": candidate_name,
        "mean_composite": mean_defined(safe_float(r["composite_score"]) for r in sub),
        "mean_repair": mean_defined(safe_float(r["repair_score"]) for r in sub),
        "mean_causal": mean_defined(safe_float(r["causal_score"]) for r in sub),
        "mean_quasi": mean_defined(safe_float(r["quasi_score"]) for r in sub),
        "mean_geom": mean_defined(safe_float(r["geom_score"]) for r in sub),
        **asym,
    }


def bootstrap_joint(
    candidates: Sequence[v09.ScaleCandidate],
    ensembles: Sequence[v10b.CalibrationEnsemble],
    run_rows: Sequence[Dict[str, Any]],
    *,
    reps: int,
    rng_seed: int,
) -> Tuple[Dict[str, Dict[str, float]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    rng = random.Random(rng_seed)
    cand_map = candidate_lookup(candidates)
    by_key: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for row in run_rows:
        by_key.setdefault((str(row["candidate_name"]), str(row["ensemble"])), []).append(dict(row))

    metrics_store: Dict[str, Dict[str, List[float]]] = {
        cand.name: {
            "mean_composite": [],
            "mean_repair": [],
            "mean_causal": [],
            "mean_quasi": [],
            "mean_geom": [],
            "alpha_all": [],
            "alpha_large": [],
            "alpha_jump": [],
            "linear_margin": [],
            "quasi_large": [],
        }
        for cand in candidates
    }
    top_counts: Dict[str, int] = {cand.name: 0 for cand in candidates}
    pairwise_counts: Dict[Tuple[str, str], int] = {}

    for _ in range(reps):
        sample_group_rows: List[Dict[str, Any]] = []
        for cand in candidates:
            for ens in ensembles:
                rows = by_key[(cand.name, ens.name)]
                sample = [rows[rng.randrange(len(rows))] for _ in range(len(rows))]
                agg = v09.summarize_group(cand, ens, sample)
                sample_group_rows.append(agg)
        v09.add_scores_to_group_rows(sample_group_rows)

        sample_summaries: List[Dict[str, Any]] = []
        for cand in candidates:
            sub = [r for r in sample_group_rows if r["candidate_name"] == cand.name]
            asym = v09b.asymptotic_metrics_from_group_rows(sub)
            row = {
                "candidate_name": cand.name,
                "mean_composite": mean_defined(safe_float(r["composite_score"]) for r in sub),
                "mean_repair": mean_defined(safe_float(r["repair_score"]) for r in sub),
                "mean_causal": mean_defined(safe_float(r["causal_score"]) for r in sub),
                "mean_quasi": mean_defined(safe_float(r["quasi_score"]) for r in sub),
                "mean_geom": mean_defined(safe_float(r["geom_score"]) for r in sub),
                **asym,
            }
            sample_summaries.append(row)
            for key in metrics_store[cand.name]:
                metrics_store[cand.name][key].append(safe_float(row.get(key), float("nan")))

        # winner by raw mean_composite inside this bootstrap replicate
        ordered = sorted(sample_summaries, key=lambda r: safe_float(r["mean_composite"], -1.0), reverse=True)
        if ordered:
            top_counts[str(ordered[0]["candidate_name"])] += 1

        for i, a in enumerate(sample_summaries):
            for b in sample_summaries[i + 1:]:
                an = str(a["candidate_name"])
                bn = str(b["candidate_name"])
                if safe_float(a["mean_composite"]) > safe_float(b["mean_composite"]):
                    pairwise_counts[(an, bn)] = pairwise_counts.get((an, bn), 0) + 1
                elif safe_float(b["mean_composite"]) > safe_float(a["mean_composite"]):
                    pairwise_counts[(bn, an)] = pairwise_counts.get((bn, an), 0) + 1

    ci_rows: Dict[str, Dict[str, float]] = {}
    for cand in candidates:
        row: Dict[str, float] = {}
        for key, vals in metrics_store[cand.name].items():
            finite = [v for v in vals if math.isfinite(v)]
            row[f"ci_low_{key}"] = quantile(finite, 0.025)
            row[f"ci_high_{key}"] = quantile(finite, 0.975)
            row[f"boot_mean_{key}"] = mean_defined(finite)
        row["top_prob_mean_composite"] = top_counts[cand.name] / max(1, reps)
        ci_rows[cand.name] = row

    pair_rows: List[Dict[str, Any]] = []
    for a in candidates:
        for b in candidates:
            if a.name == b.name:
                continue
            wins = pairwise_counts.get((a.name, b.name), 0)
            losses = pairwise_counts.get((b.name, a.name), 0)
            denom = wins + losses
            pair_rows.append(
                {
                    "candidate_a": a.name,
                    "candidate_b": b.name,
                    "prob_a_gt_b_mean_composite": (wins / denom) if denom > 0 else float("nan"),
                    "bootstrap_comparisons": denom,
                }
            )

    top_rows = [
        {
            "candidate_name": cand.name,
            "top_prob_mean_composite": ci_rows[cand.name]["top_prob_mean_composite"],
        }
        for cand in candidates
    ]
    return ci_rows, pair_rows, top_rows


def add_focused_score(candidate_rows: List[Dict[str, Any]]) -> None:
    metrics = {
        "ci_low_mean_composite": True,
        "alpha_large": False,
        "abs_alpha_jump": False,
        "linear_margin": True,
        "quasi_large": True,
    }
    for row in candidate_rows:
        row["abs_alpha_jump"] = abs(safe_float(row.get("alpha_jump"), float("nan")))
    for key, higher in metrics.items():
        vals = [safe_float(r.get(key), float("nan")) for r in candidate_rows]
        vals = [v for v in vals if math.isfinite(v)]
        if not vals:
            continue
        lo, hi = min(vals), max(vals)
        for row in candidate_rows:
            row[f"score_{key}"] = v09.objective_score(safe_float(row.get(key), float("nan")), lo, hi, higher_better=higher)
    score_keys = [f"score_{k}" for k in metrics]
    for row in candidate_rows:
        row["focused_score"] = mean_defined(safe_float(row.get(k), float("nan")) for k in score_keys)


def size_profiles(candidate_names: Sequence[str], group_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for name in candidate_names:
        sub = [r for r in group_rows if r["candidate_name"] == name]
        for row in v09b.size_profile(list(sub)):
            out.append({"candidate_name": name, **row})
    return out


def build_markdown(
    regime_name: str,
    target_summary: Sequence[Dict[str, Any]],
    candidate_rows: Sequence[Dict[str, Any]],
    pair_rows: Sequence[Dict[str, Any]],
    profile_rows: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.10e: fokusert band-validering under anbefalt ensemble-regime")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        f"Denne runden bruker bare anbefalt generatorregime `{regime_name}` på deep-ensembler, "
        "med et smalt lokalt kandidatbånd rundt `band_best`. Målet er ikke å lage et nytt bredt atlas, "
        "men å sjekke om `band_best` fortsatt står seg når vi (i) øker replikasjonen moderat, "
        "(ii) holder startregimet fast, og (iii) undersøker noen få nærliggende parameterperturbasjoner."
    )
    lines.append("")
    lines.append("## Realiserte startstørrelser")
    lines.append("")
    lines.append("| target | mean_initial | q10 | q90 | separated_from_prev | mean_tokens | mean_beta1 | mean_triangles |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {safe_float(row['mean_initial_nodes']):.1f} | {safe_float(row['q10_initial_nodes']):.1f} | "
            f"{safe_float(row['q90_initial_nodes']):.1f} | {int(row['separated_from_prev'])} | "
            f"{safe_float(row['mean_initial_tokens']):.1f} | {safe_float(row['mean_initial_beta1']):.1f} | {safe_float(row['mean_initial_triangles']):.1f} |"
        )
    lines.append("")
    lines.append("## Kandidatsammendrag")
    lines.append("")
    lines.append("| candidate | focused_score | mean_composite | CI low composite | top_prob | alpha_large | alpha_jump | linear_margin | quasi_large |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(candidate_rows, key=lambda r: safe_float(r["focused_score"], -1.0), reverse=True):
        lines.append(
            f"| {row['candidate_name']} | {safe_float(row['focused_score']):.3f} | {safe_float(row['mean_composite']):.3f} | "
            f"{safe_float(row['ci_low_mean_composite']):.3f} | {safe_float(row['top_prob_mean_composite']):.3f} | "
            f"{safe_float(row['alpha_large']):.3f} | {safe_float(row['alpha_jump']):.3f} | {safe_float(row['linear_margin']):.3f} | {safe_float(row['quasi_large']):.3f} |"
        )
    lines.append("")
    lines.append("## Pairwise sannsynligheter (mean composite)")
    lines.append("")
    lines.append("| a | b | P(a > b) |")
    lines.append("| --- | --- | --- |")
    for row in sorted(pair_rows, key=lambda r: (str(r["candidate_a"]), str(r["candidate_b"]))):
        lines.append(
            f"| {row['candidate_a']} | {row['candidate_b']} | {safe_float(row['prob_a_gt_b_mean_composite']):.3f} |"
        )
    lines.append("")
    lines.append("## Størrelsesprofiler")
    lines.append("")
    lines.append("| candidate | target | realized_initial | radius | overlap | quasi | composite | beta1_drift |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(profile_rows, key=lambda r: (str(r["candidate_name"]), int(r["target_nodes"]))):
        lines.append(
            f"| {row['candidate_name']} | {int(row['target_nodes'])} | {safe_float(row['mean_initial_nodes']):.1f} | "
            f"{safe_float(row['mean_radius']):.2f} | {safe_float(row['mean_overlap']):.3f} | {safe_float(row['mean_quasi']):.3f} | "
            f"{safe_float(row['mean_composite']):.3f} | {safe_float(row['mean_beta1_drift']):.2f} |"
        )
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append(
        "Hvis `band_best` fortsatt vinner eller ligger svært høyt mot sine nærmeste naboer, er det et tegn på at v0.10d ikke bare var et generatorartefakt. "
        "Hvis en nær nabo overtar på både `CI low composite` og mer stabile asymptotiske mål, er det et signal om at prosjektet nå bør flytte sentrum litt bort fra den gamle referansekandidaten."
    )
    lines.append("")
    lines.append(
        "Merk at dette fortsatt er en fokusert metodisk test. Resultatene sier noe om robusthet innen det anbefalte ensemble-regimet og i et lite lokalt parameterbånd, "
        "ikke om en ferdig fysisk teori."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.10e focused validation around band_best")
    ap.add_argument("--growth-regime", type=str, default="fast_balanced")
    ap.add_argument("--targets", type=str, default="48,96,192,256")
    ap.add_argument("--growth-seeds", type=int, default=3)
    ap.add_argument("--run-seeds", type=int, default=3)
    ap.add_argument("--bootstrap-reps", type=int, default=250)
    ap.add_argument("--output-prefix", type=str, default="Documentation/v10e")
    ap.add_argument(
        "--report-md",
        type=str,
        default="Documentation/relasjonell_universgraf_v0_10e_fokusert_bandvalidering.md",
    )
    return ap


def main() -> None:
    ap = build_argparser()
    args = ap.parse_args()

    regime = recommended_regime(args.growth_regime)
    targets = [int(x) for x in args.targets.split(",") if x.strip()]
    ensembles = [e for e in v10b.build_ensembles(targets) if e.burnin_label == "deep"]
    candidates = local_candidates()
    growth_seeds = [7001 + 18 * i for i in range(args.growth_seeds)]
    run_offsets = [1101 + 22 * i for i in range(args.run_seeds)]

    base_states, base_rows = build_bases(ensembles, regime, growth_seeds)
    base_summary = summarize_bases(base_rows)

    run_rows = collect_run_rows(candidates, ensembles, base_states, growth_seeds, run_offsets, regime.name)
    group_rows = summarize_groups(candidates, ensembles, run_rows)

    ci_rows, pair_rows, top_rows = bootstrap_joint(
        candidates,
        ensembles,
        run_rows,
        reps=int(args.bootstrap_reps),
        rng_seed=19017,
    )
    top_lookup = {str(r["candidate_name"]): r for r in top_rows}

    candidate_rows: List[Dict[str, Any]] = []
    for cand in candidates:
        row = point_candidate_summary(cand.name, group_rows)
        row.update(ci_rows[cand.name])
        row["top_prob_mean_composite"] = top_lookup[cand.name]["top_prob_mean_composite"]
        candidate_rows.append(row)
    add_focused_score(candidate_rows)
    candidate_rows.sort(key=lambda r: safe_float(r["focused_score"], -1.0), reverse=True)

    profile_rows = size_profiles([c.name for c in candidates], group_rows)

    prefix = args.output_prefix
    write_csv(f"{prefix}_focused_band_base_rows.csv", base_rows)
    write_csv(f"{prefix}_focused_band_base_summary.csv", base_summary)
    write_csv(f"{prefix}_focused_band_run_rows.csv", run_rows)
    write_csv(f"{prefix}_focused_band_group_rows.csv", group_rows)
    write_csv(f"{prefix}_focused_band_candidate_summary.csv", candidate_rows)
    write_csv(f"{prefix}_focused_band_pairwise.csv", pair_rows)
    write_csv(f"{prefix}_focused_band_top_probs.csv", top_rows)
    write_csv(f"{prefix}_focused_band_size_profiles.csv", profile_rows)
    report = build_markdown(regime.name, base_summary, candidate_rows, pair_rows, profile_rows)
    report_path = Path(args.report_md)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    Path(f"{prefix}_focused_band_validation.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
