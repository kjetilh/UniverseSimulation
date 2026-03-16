#!/usr/bin/env python3
"""v0.10 larger-scale and scaling-collapse diagnostics for relational universe."""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v09b_asymptotic_refinement as v09b


def safe_float(value: Any, default: float = float("nan")) -> float:
    try:
        out = float(value)
    except Exception:
        return default
    if math.isnan(out) or math.isinf(out):
        return default
    return out


def quantile(values: Sequence[float], q: float) -> float:
    vals = sorted(v for v in values if math.isfinite(v))
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
    ensure_parent_dir(path)
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    keys: List[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                keys.append(key)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    head = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows[1:])
    return "\n".join([head, sep, body])


def load_rows(path: str | Path) -> List[Dict[str, Any]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def choose_candidates(candidate_csv: str | Path, *, top_n: int) -> List[v09.ScaleCandidate]:
    rows = load_rows(candidate_csv)
    if not rows:
        return v09b.default_candidates()[:top_n]
    out: List[v09.ScaleCandidate] = []
    for row in rows[:top_n]:
        out.append(
            v09.ScaleCandidate(
                str(row["candidate_name"]),
                safe_float(row["r_birth"]),
                safe_float(row["r_death"]),
                safe_float(row["p_swap"]),
                safe_float(row["p_triad"]),
                safe_float(row["p_del"]),
            )
        )
    return out


def v10_ensembles(include_384: bool) -> List[v09.ScaleEnsemble]:
    ensembles = [
        v09.ScaleEnsemble("natural48_light", 48, "light", 12, 6, 960, 40, 140),
        v09.ScaleEnsemble("natural48_deep", 48, "deep", 12, 6, 1600, 220, 380),
        v09.ScaleEnsemble("natural96_light", 96, "light", 14, 7, 2200, 80, 180),
        v09.ScaleEnsemble("natural96_deep", 96, "deep", 14, 7, 3400, 320, 520),
        v09.ScaleEnsemble("natural192_light", 192, "light", 16, 8, 4200, 120, 260),
        v09.ScaleEnsemble("natural192_deep", 192, "deep", 16, 8, 6200, 420, 700),
        v09.ScaleEnsemble("natural256_light", 256, "light", 18, 9, 5600, 180, 340),
        v09.ScaleEnsemble("natural256_deep", 256, "deep", 18, 9, 7600, 520, 860),
    ]
    if include_384:
        ensembles.extend(
            [
                v09.ScaleEnsemble("natural384_light", 384, "light", 20, 10, 7800, 260, 460),
                v09.ScaleEnsemble("natural384_deep", 384, "deep", 20, 10, 9800, 680, 1120),
            ]
        )
    return ensembles


def rmse_model(xs: Sequence[float], ys: Sequence[float], mode: str) -> float:
    points = [(float(x), float(y)) for x, y in zip(xs, ys) if math.isfinite(float(x)) and math.isfinite(float(y))]
    if len(points) < 2:
        return float("nan")
    if mode == "log":
        tx = [math.log(x) for x, _ in points]
    elif mode == "sqrt":
        tx = [math.sqrt(x) for x, _ in points]
    elif mode == "linear":
        tx = [x for x, _ in points]
    elif mode == "power":
        tx = [math.log(x) for x, _ in points]
        ys = [math.log(y + 1.0) for _, y in points]
        slope, intercept = v09b.linear_fit(tx, ys)
        preds = [math.exp(intercept + slope * x) - 1.0 for x in tx]
        obs = [y for _, y in points]
        return math.sqrt(sum((p - y) ** 2 for p, y in zip(preds, obs)) / len(obs))
    else:
        raise ValueError(mode)
    obs = [y for _, y in points]
    slope, intercept = v09b.linear_fit(tx, obs)
    preds = [slope * x + intercept for x in tx]
    return math.sqrt(sum((p - y) ** 2 for p, y in zip(preds, obs)) / len(obs))


def local_exponent_uncertainty(group_rows: Sequence[Dict[str, Any]]) -> Dict[str, float]:
    profile = v09b.size_profile(list(group_rows))
    ns = [safe_float(row["mean_initial_nodes"]) for row in profile]
    rs = [safe_float(row["mean_radius"]) for row in profile]
    alphas: List[float] = []
    for (n1, r1), (n2, r2) in zip(zip(ns, rs), zip(ns[1:], rs[1:])):
        alpha = v09b.pair_alpha(r1, n1, r2, n2)
        if math.isfinite(alpha):
            alphas.append(alpha)
    if not alphas:
        return {"local_alpha_mean": float("nan"), "local_alpha_sd": float("nan"), "tail_alpha_range": float("nan")}
    tail = alphas[-2:] if len(alphas) >= 2 else alphas
    return {
        "local_alpha_mean": statistics.mean(alphas),
        "local_alpha_sd": statistics.pstdev(alphas) if len(alphas) >= 2 else 0.0,
        "tail_alpha_range": max(tail) - min(tail) if len(tail) >= 2 else 0.0,
    }


def collapse_metrics(group_rows: Sequence[Dict[str, Any]]) -> Dict[str, float]:
    metrics = v09b.asymptotic_metrics_from_group_rows(list(group_rows))
    profile = v09b.size_profile(list(group_rows))
    alpha = safe_float(metrics["alpha_large"])
    collapsed: List[float] = []
    for row in profile[-3:]:
        n = safe_float(row["mean_initial_nodes"])
        r = safe_float(row["mean_radius"])
        if n > 0 and math.isfinite(r) and math.isfinite(alpha):
            collapsed.append((r + 1.0) / (n ** alpha))
    collapse_cv = float("nan")
    if collapsed and statistics.mean(collapsed) != 0:
        collapse_cv = statistics.pstdev(collapsed) / abs(statistics.mean(collapsed))
    return {
        **metrics,
        **local_exponent_uncertainty(group_rows),
        "collapse_cv_tail": collapse_cv,
    }


def candidate_summary(
    point: v09.ScaleCandidate,
    run_rows: Sequence[Dict[str, Any]],
    group_rows: Sequence[Dict[str, Any]],
) -> Dict[str, Any]:
    metrics = collapse_metrics(group_rows)
    mean_comp = statistics.mean(safe_float(r["composite_score"]) for r in group_rows)
    rmse_log = safe_float(metrics["rmse_log"])
    rmse_sqrt = safe_float(metrics["rmse_sqrt"])
    rmse_linear = safe_float(metrics["rmse_linear"])
    rmse_power = rmse_model(
        [safe_float(r["mean_initial_nodes"]) for r in v09b.size_profile(list(group_rows))],
        [safe_float(r["mean_radius"]) for r in v09b.size_profile(list(group_rows))],
        "power",
    )
    model_rmse = {"log": rmse_log, "sqrt": rmse_sqrt, "linear": rmse_linear, "power": rmse_power}
    best_model = min(model_rmse, key=lambda key: model_rmse[key] if math.isfinite(model_rmse[key]) else float("inf"))
    stable_tail = 1 if safe_float(metrics["tail_alpha_range"], float("inf")) < 0.25 else 0
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
        "best_radius_model": best_model,
        "rmse_log": rmse_log,
        "rmse_sqrt": rmse_sqrt,
        "rmse_linear": rmse_linear,
        "rmse_power": rmse_power,
        "stable_tail": stable_tail,
        **metrics,
    }


def bootstrap_tail_uncertainty(
    point: v09.ScaleCandidate,
    ensembles: Sequence[v09.ScaleEnsemble],
    run_rows: Sequence[Dict[str, Any]],
    *,
    reps: int,
    rng_seed: int,
) -> Dict[str, float]:
    rng = __import__("random").Random(rng_seed)
    by_ensemble: Dict[str, List[Dict[str, Any]]] = {}
    for row in run_rows:
        by_ensemble.setdefault(str(row["ensemble"]), []).append(row)
    alpha_vals: List[float] = []
    collapse_vals: List[float] = []
    for _ in range(max(1, reps)):
        sample_group: List[Dict[str, Any]] = []
        for ensemble in ensembles:
            rows = by_ensemble.get(ensemble.name, [])
            if not rows:
                continue
            sample = [rows[rng.randrange(len(rows))] for _ in range(len(rows))]
            agg = v09.summarize_group(point, ensemble, sample)
            sample_group.append(agg)
        if not sample_group:
            continue
        v09.add_scores_to_group_rows(sample_group)
        metrics = collapse_metrics(sample_group)
        alpha_vals.append(safe_float(metrics["alpha_large"]))
        collapse_vals.append(safe_float(metrics["collapse_cv_tail"]))
    return {
        "ci_low_alpha_large": quantile(alpha_vals, 0.025),
        "ci_high_alpha_large": quantile(alpha_vals, 0.975),
        "ci_low_collapse_cv_tail": quantile(collapse_vals, 0.025),
        "ci_high_collapse_cv_tail": quantile(collapse_vals, 0.975),
    }


def run_v10(
    candidates: Sequence[v09.ScaleCandidate],
    ensembles: Sequence[v09.ScaleEnsemble],
    growth_seeds: Sequence[int],
    *,
    steps_per_node: float,
    min_steps: int,
    max_steps: int,
    bootstrap_reps: int,
) -> Dict[str, Any]:
    base_states, ensemble_meta = v09.build_base_states(list(ensembles), list(growth_seeds))
    run_rows_all: List[Dict[str, Any]] = []
    group_rows_all: List[Dict[str, Any]] = []
    candidate_rows: List[Dict[str, Any]] = []
    size_profiles: List[Dict[str, Any]] = []

    for index, point in enumerate(candidates):
        run_rows: List[Dict[str, Any]] = []
        group_rows: List[Dict[str, Any]] = []
        for ensemble in ensembles:
            sub_rows: List[Dict[str, Any]] = []
            for seed in growth_seeds:
                base = base_states[(ensemble.name, int(seed))]
                steps = v09.compute_steps_for_state(base, steps_per_node, min_steps, max_steps)
                row = v09.run_single_candidate_from_base(point, ensemble, base, seed=int(seed), steps=steps)
                sub_rows.append(row)
                run_rows.append(row)
            agg = v09.summarize_group(point, ensemble, sub_rows)
            group_rows.append(agg)
        v09.add_scores_to_group_rows(group_rows)
        summary = candidate_summary(point, run_rows, group_rows)
        summary.update(bootstrap_tail_uncertainty(point, ensembles, run_rows, reps=bootstrap_reps, rng_seed=1700 + index * 97))
        candidate_rows.append(summary)
        run_rows_all.extend(run_rows)
        group_rows_all.extend(group_rows)
        for row in v09b.size_profile(group_rows):
            size_profiles.append({"candidate_name": point.name, **row})

    candidate_rows.sort(
        key=lambda row: (
            int(row["stable_tail"]),
            -safe_float(row["collapse_cv_tail"], float("inf")),
            -safe_float(row["alpha_large"], float("inf")),
            safe_float(row["mean_composite"], -1.0),
        ),
        reverse=True,
    )
    return {
        "ensemble_meta_rows": ensemble_meta,
        "run_rows": run_rows_all,
        "group_rows": group_rows_all,
        "candidate_rows": candidate_rows,
        "size_profiles": size_profiles,
    }


def write_md(path: str | Path, content: str) -> None:
    ensure_parent_dir(path)
    Path(path).write_text(content, encoding="utf-8")


def technical_md(candidate_rows: Sequence[Dict[str, Any]], *, include_384: bool) -> str:
    best = candidate_rows[0] if candidate_rows else None
    rows = [["candidate", "composite", "alpha_large", "collapse_cv_tail", "best model", "stable tail"]]
    for row in candidate_rows[:6]:
        rows.append([
            str(row["candidate_name"]),
            f"{safe_float(row['mean_composite']):.3f}",
            f"{safe_float(row['alpha_large']):.3f}",
            f"{safe_float(row['collapse_cv_tail']):.3f}",
            str(row["best_radius_model"]),
            str(int(row["stable_tail"])),
        ])
    lines = [
        "# Relasjonell universgraf v0.10 – større skala og skaleringskollaps",
        "",
        "v0.10 løfter skalaen videre enn v0.9b og prøver samtidig en mer eksplisitt kollaps-lesning av radiusfronten.",
        "",
        f"- inkluderer 384-nivå: {'ja' if include_384 else 'nei'}",
        "",
        markdown_table(rows),
        "",
    ]
    if best is not None:
        lines.extend([
            f"Beste kandidat i denne runden er `{best['candidate_name']}`.",
            f"Den har alpha_large ≈ {safe_float(best['alpha_large']):.3f}, collapse_cv_tail ≈ {safe_float(best['collapse_cv_tail']):.3f} og beste radiusmodell `{best['best_radius_model']}`.",
            "",
            "## Tolkning",
            "",
            "Pre-asymptotiske mønstre viser seg typisk som store hopp i lokale eksponenter og svak kollaps i tailen. Et mer stabilt storskala-regime bør derimot få mindre tail-spredning og et mer konsistent modellvalg.",
            "",
        ])
    return "\n".join(lines)


def lay_md(candidate_rows: Sequence[Dict[str, Any]]) -> str:
    best = candidate_rows[0] if candidate_rows else None
    lines = [
        "# Relasjonell universgraf v0.10 – enkel forklaring",
        "",
        "I v0.10 spør vi om de beste kandidatene fortsatt oppfører seg ryddig når universene blir enda større, og om kurvene deres begynner å ligne en felles skalaform i stedet for bare pene enkelttall.",
        "",
    ]
    if best is not None:
        lines.append(f"Den foreløpig sterkeste kandidaten i denne runden er `{best['candidate_name']}`.")
        lines.append("")
    return "\n".join(lines)


def overview_md() -> str:
    return """# Prosjektoversikt v0.10

v0.10 bygger direkte på v0.9b:

- større naturlige ensembler,
- flere growth seeds for toppkandidatene,
- eksplisitt modellvalg mellom log, sqrt, linear og power-law,
- enkel kollapsdiagnostikk for radiusfronten,
- tydeligere skille mellom pre-asymptotiske mønstre og mer stabile tail-regimer.
"""


def glossary_md() -> str:
    return """# Ordliste v0.10

- **collapse_cv_tail**: variasjon i den kollapsede tail-størrelsen `(radius+1)/N^alpha` over de største nivåene.
- **stable tail**: en enkel indikator for om lokale eksponenter i tailen holder seg forholdsvis samlet.
- **best radius model**: hvilken enkel familie (`log`, `sqrt`, `linear`, `power`) som passer radius best i RMSE-forstand.
"""


def findings_md(candidate_rows: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.10 – hovedfunn og implikasjoner", ""]
    for idx, row in enumerate(candidate_rows[:5], start=1):
        lines.append(
            f"{idx}. `{row['candidate_name']}`: composite ≈ {safe_float(row['mean_composite']):.3f}, alpha_large ≈ {safe_float(row['alpha_large']):.3f}, collapse_cv_tail ≈ {safe_float(row['collapse_cv_tail']):.3f}, best model `{row['best_radius_model']}`."
        )
    lines.append("")
    lines.append("Dette er fortsatt en streng arbeidslesning, ikke en endelig fysisk konklusjon.")
    return "\n".join(lines)


def readme_md(produced: Sequence[str]) -> str:
    lines = ["# README – relational_universe_bundle_v10_generated", ""]
    for item in produced:
        lines.append(f"- `{Path(item).name}`")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run larger-scale collapse diagnostics for relational universe.")
    parser.add_argument("--v09b-candidate-csv", default="Documentation/v09b_asymptotic_candidate_summary.csv")
    parser.add_argument("--out-dir", default="Documentation")
    parser.add_argument("--candidate-top-n", type=int, default=2)
    parser.add_argument("--growth-seeds", default="401,503,607")
    parser.add_argument("--steps-per-node", type=float, default=4.2)
    parser.add_argument("--min-steps", type=int, default=140)
    parser.add_argument("--max-steps", type=int, default=760)
    parser.add_argument("--bootstrap-reps", type=int, default=40)
    parser.add_argument("--include-384", action="store_true")
    parser.add_argument("--bundle-zip", default="Documentation/relational_universe_bundle_v10_generated.zip")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    candidates = choose_candidates(args.v09b_candidate_csv, top_n=args.candidate_top_n)
    ensembles = v10_ensembles(include_384=args.include_384)
    growth_seeds = [int(piece.strip()) for piece in args.growth_seeds.split(",") if piece.strip()]
    result = run_v10(
        candidates,
        ensembles,
        growth_seeds,
        steps_per_node=args.steps_per_node,
        min_steps=args.min_steps,
        max_steps=args.max_steps,
        bootstrap_reps=args.bootstrap_reps,
    )
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    run_csv = out_dir / "v10_scale_run_rows.csv"
    group_csv = out_dir / "v10_scale_group_rows.csv"
    cand_csv = out_dir / "v10_scale_candidate_summary.csv"
    profile_csv = out_dir / "v10_scale_size_profiles.csv"
    write_csv(run_csv, result["run_rows"])
    write_csv(group_csv, result["group_rows"])
    write_csv(cand_csv, result["candidate_rows"])
    write_csv(profile_csv, result["size_profiles"])
    tech_md = out_dir / "relasjonell_universgraf_v0_10_storre_skala_og_kollaps.md"
    status_md = out_dir / "relasjonell_universgraf_status_v0_10.md"
    overview = out_dir / "prosjektoversikt_v0_10.md"
    lay = out_dir / "relasjonell_universgraf_for_ikke_spesialister_v0_10.md"
    glossary = out_dir / "ordliste_v0_10.md"
    findings = out_dir / "v0_10_hovedfunn_og_implikasjoner.md"
    write_md(tech_md, technical_md(result["candidate_rows"], include_384=args.include_384))
    write_md(status_md, technical_md(result["candidate_rows"], include_384=args.include_384))
    write_md(overview, overview_md())
    write_md(lay, lay_md(result["candidate_rows"]))
    write_md(glossary, glossary_md())
    write_md(findings, findings_md(result["candidate_rows"]))
    produced = [str(run_csv), str(group_csv), str(cand_csv), str(profile_csv), str(tech_md), str(status_md), str(overview), str(lay), str(glossary), str(findings)]
    readme = out_dir / "README_relational_universe_bundle_v10_generated.md"
    write_md(readme, readme_md(produced))
    produced.append(str(readme))
    if args.bundle_zip:
        bundle = Path(args.bundle_zip)
        ensure_parent_dir(bundle)
        with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in produced:
                zf.write(path, arcname=Path(path).name)


if __name__ == "__main__":
    main()
