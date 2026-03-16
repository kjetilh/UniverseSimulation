#!/usr/bin/env python3
"""v0.9 scale analysis for larger natural ensembles and burn-in regimes."""

from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b


METRICS = [
    "avg_local_overlap",
    "final_radius_control",
    "final_edge_diff_count",
    "abs_drift_beta1_per_step",
    "abs_drift_spectral_radius_per_step",
]


@dataclass(frozen=True)
class ScaleEnsembleSpec:
    name: str
    target_nodes: int
    burnin_regime: str
    initial_cycle: int
    initial_tokens: int
    burnin_steps: int
    extra_burnin_low: int
    extra_burnin_high: int
    jitter_low: int
    jitter_high: int


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


def bootstrap_interval(values: Sequence[float], *, reps: int, rng_seed: int) -> Tuple[float, float]:
    vals = [float(v) for v in values if math.isfinite(float(v))]
    if not vals:
        return float("nan"), float("nan")
    if len(vals) == 1:
        return vals[0], vals[0]
    rng = random.Random(rng_seed)
    means: List[float] = []
    n = len(vals)
    for _ in range(max(1, reps)):
        sample = [vals[rng.randrange(n)] for _ in range(n)]
        means.append(float(statistics.mean(sample)))
    return quantile(means, 0.025), quantile(means, 0.975)


def load_overall_rows(path: str | Path) -> List[Dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def candidate_key(row: Dict[str, Any]) -> Tuple[float, float, float, float, float]:
    return (
        round(safe_float(row.get("r_birth"), 0.0), 6),
        round(safe_float(row.get("r_death"), 0.0), 6),
        round(safe_float(row.get("p_swap"), 0.0), 6),
        round(safe_float(row.get("p_triad"), 0.0), 6),
        round(safe_float(row.get("p_del"), 0.0), 6),
    )


def pick_candidates(overall_csv: str | Path, *, top_n: int) -> List[v08b.CandidatePoint]:
    rows = load_overall_rows(overall_csv)
    if rows:
        ranked = sorted(
            rows,
            key=lambda row: (
                safe_float(row.get("ci_low_mean_composite_natural"), -1.0),
                safe_float(row.get("mean_composite_natural"), -1.0),
            ),
            reverse=True,
        )
        out: List[v08b.CandidatePoint] = []
        seen = set()
        for row in ranked:
            key = candidate_key(row)
            if key in seen:
                continue
            seen.add(key)
            out.append(
                v08b.CandidatePoint(
                    name=f"v08b_top_{len(out) + 1}",
                    r_birth=key[0],
                    r_death=key[1],
                    p_swap=key[2],
                    p_triad=key[3],
                    p_del=key[4],
                )
            )
            if len(out) >= top_n:
                return out
    return v08b.default_candidates()[:top_n]


def scale_ensembles() -> List[ScaleEnsembleSpec]:
    return [
        ScaleEnsembleSpec("natural64_moderate", 64, "moderate", 12, 6, 2200, 100, 180, 58, 70),
        ScaleEnsembleSpec("natural64_deep", 64, "deep", 12, 6, 2600, 240, 420, 58, 70),
        ScaleEnsembleSpec("natural96_moderate", 96, "moderate", 14, 7, 3600, 120, 220, 88, 104),
        ScaleEnsembleSpec("natural96_deep", 96, "deep", 14, 7, 4400, 320, 520, 88, 104),
        ScaleEnsembleSpec("natural128_moderate", 128, "moderate", 16, 8, 5200, 160, 280, 116, 136),
        ScaleEnsembleSpec("natural128_deep", 128, "deep", 16, 8, 6200, 420, 680, 116, 136),
    ]


def growth_spec(plan: ScaleEnsembleSpec) -> v08b.EnsembleSpec:
    return v08b.EnsembleSpec(
        name=plan.name,
        kind="natural_grown",
        initial_cycle=plan.initial_cycle,
        initial_tokens=plan.initial_tokens,
        target_nodes=plan.target_nodes,
        burnin_steps=plan.burnin_steps,
        jitter_nodes_low=plan.jitter_low,
        jitter_nodes_high=plan.jitter_high,
        extra_burnin_low=plan.extra_burnin_low,
        extra_burnin_high=plan.extra_burnin_high,
        include_in_natural_score=1,
    )


def collect_scale_run(
    point: v08b.CandidatePoint,
    plan: ScaleEnsembleSpec,
    base_state: v7.State,
    *,
    seed: int,
    steps: int,
) -> Dict[str, Any]:
    params = v08b.candidate_to_params(point)
    result = v08b.run_coupled_from_base(
        base_state,
        params=params,
        seed=seed,
        steps=steps,
        perturbation="local_swap",
        local_coupling="maximal",
        log_every=max(30, min(120, steps // 5)),
    )
    init = result["initial_control_features"]
    final_features = v7.feature_row(result["control_final"])
    hm = result["headline_metrics"]
    drift_beta1 = (safe_float(final_features.get("beta1")) - safe_float(init.get("beta1"))) / float(max(steps, 1))
    drift_spectral = (safe_float(final_features.get("spectral_radius")) - safe_float(init.get("spectral_radius"))) / float(max(steps, 1))
    return {
        "ensemble": plan.name,
        "burnin_regime": plan.burnin_regime,
        "size_target": plan.target_nodes,
        "seed": seed,
        "candidate_name": point.name,
        "r_birth": point.r_birth,
        "r_death": point.r_death,
        "p_swap": point.p_swap,
        "p_triad": point.p_triad,
        "p_del": point.p_del,
        "initial_nodes": safe_float(init.get("nodes")),
        "initial_tokens": safe_float(init.get("tokens")),
        "initial_beta1": safe_float(init.get("beta1")),
        "initial_spectral_radius": safe_float(init.get("spectral_radius")),
        "final_radius_control": safe_float(hm.get("final_radius_control")),
        "final_edge_diff_count": safe_float(hm.get("final_edge_diff_count")),
        "avg_local_overlap": safe_float(result["coupling"].get("avg_local_overlap_both_accept"), 0.0),
        "shared_token_fraction_final": safe_float(hm.get("shared_token_fraction_final"), 0.0),
        "shared_node_fraction_final": safe_float(hm.get("shared_node_fraction_final"), 0.0),
        "fit_speed_control": max(0.0, safe_float(hm.get("fit_speed_control"), 0.0)),
        "drift_beta1_per_step": drift_beta1,
        "abs_drift_beta1_per_step": abs(drift_beta1),
        "drift_spectral_radius_per_step": drift_spectral,
        "abs_drift_spectral_radius_per_step": abs(drift_spectral),
    }


def summarize_group(rows: Sequence[Dict[str, Any]], *, bootstrap_reps: int, rng_seed: int) -> Dict[str, Any]:
    sample = list(rows)
    first = sample[0]
    out: Dict[str, Any] = {
        "ensemble": first["ensemble"],
        "burnin_regime": first["burnin_regime"],
        "size_target": first["size_target"],
        "candidate_name": first["candidate_name"],
        "r_birth": first["r_birth"],
        "r_death": first["r_death"],
        "p_swap": first["p_swap"],
        "p_triad": first["p_triad"],
        "p_del": first["p_del"],
        "runs": len(sample),
        "mean_initial_nodes": statistics.mean(safe_float(r["initial_nodes"]) for r in sample),
    }
    for metric in METRICS:
        vals = [safe_float(r[metric]) for r in sample]
        out[f"mean_{metric}"] = statistics.mean(vals)
        out[f"sd_{metric}"] = statistics.pstdev(vals) if len(vals) >= 2 else 0.0
        lo, hi = bootstrap_interval(vals, reps=bootstrap_reps, rng_seed=rng_seed + sum(ord(c) for c in metric))
        out[f"ci_low_{metric}"] = lo
        out[f"ci_high_{metric}"] = hi
    return out


def linear_slope(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) < 2 or len(ys) < 2:
        return float("nan")
    x_mean = statistics.mean(xs)
    y_mean = statistics.mean(ys)
    denom = sum((x - x_mean) ** 2 for x in xs)
    if abs(denom) < 1e-12:
        return float("nan")
    numer = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    return numer / denom


def summarize_slopes(
    run_rows: Sequence[Dict[str, Any]],
    *,
    bootstrap_reps: int,
    rng_seed: int,
) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[str, str, float, float, float, float, float], List[Dict[str, Any]]] = {}
    for row in run_rows:
        key = (
            str(row["candidate_name"]),
            str(row["burnin_regime"]),
            safe_float(row["r_birth"]),
            safe_float(row["r_death"]),
            safe_float(row["p_swap"]),
            safe_float(row["p_triad"]),
            safe_float(row["p_del"]),
        )
        grouped.setdefault(key, []).append(row)

    out: List[Dict[str, Any]] = []
    for key, rows in grouped.items():
        for metric in METRICS:
            by_size: Dict[int, List[Dict[str, Any]]] = {}
            for row in rows:
                by_size.setdefault(int(safe_float(row["size_target"])), []).append(row)
            xs = [statistics.mean(safe_float(r["initial_nodes"]) for r in sub) for _, sub in sorted(by_size.items())]
            ys = [statistics.mean(safe_float(r[metric]) for r in sub) for _, sub in sorted(by_size.items())]
            slope = linear_slope(xs, ys)
            boot_slopes: List[float] = []
            rng = random.Random(rng_seed + sum(ord(c) for c in metric) + len(rows))
            if len(xs) >= 2:
                for _ in range(max(1, bootstrap_reps)):
                    xs_boot: List[float] = []
                    ys_boot: List[float] = []
                    for _, sub in sorted(by_size.items()):
                        n = len(sub)
                        resample = [sub[rng.randrange(n)] for _ in range(n)]
                        xs_boot.append(statistics.mean(safe_float(r["initial_nodes"]) for r in resample))
                        ys_boot.append(statistics.mean(safe_float(r[metric]) for r in resample))
                    boot_slopes.append(linear_slope(xs_boot, ys_boot))
            out.append(
                {
                    "candidate_name": key[0],
                    "burnin_regime": key[1],
                    "r_birth": key[2],
                    "r_death": key[3],
                    "p_swap": key[4],
                    "p_triad": key[5],
                    "p_del": key[6],
                    "metric": metric,
                    "slope_per_initial_node": slope,
                    "ci_low_slope": quantile(boot_slopes, 0.025),
                    "ci_high_slope": quantile(boot_slopes, 0.975),
                }
            )
    return out


def top_table(aggregate_rows: Sequence[Dict[str, Any]]) -> str:
    ranked = sorted(
        aggregate_rows,
        key=lambda row: (
            -safe_float(row["mean_avg_local_overlap"]),
            safe_float(row["mean_final_radius_control"]),
            safe_float(row["mean_abs_drift_beta1_per_step"]),
        ),
    )
    rows = [["candidate", "burnin", "target", "mean init", "overlap", "radius", "edge diff", "|beta1 drift|", "|spectral drift|"]]
    for row in ranked[:12]:
        rows.append(
            [
                row["candidate_name"],
                str(row["burnin_regime"]),
                str(int(safe_float(row["size_target"]))),
                f"{safe_float(row['mean_initial_nodes']):.1f}",
                f"{safe_float(row['mean_avg_local_overlap']):.3f}",
                f"{safe_float(row['mean_final_radius_control']):.3f}",
                f"{safe_float(row['mean_final_edge_diff_count']):.3f}",
                f"{safe_float(row['mean_abs_drift_beta1_per_step']):.4f}",
                f"{safe_float(row['mean_abs_drift_spectral_radius_per_step']):.4f}",
            ]
        )
    return markdown_table(rows)


def slope_table(slopes: Sequence[Dict[str, Any]]) -> str:
    rows = [["candidate", "burnin", "metric", "slope", "ci_low", "ci_high"]]
    chosen = [
        row for row in slopes
        if row["metric"] in {"avg_local_overlap", "final_radius_control", "abs_drift_beta1_per_step", "abs_drift_spectral_radius_per_step"}
    ]
    chosen = sorted(chosen, key=lambda row: (str(row["candidate_name"]), str(row["burnin_regime"]), str(row["metric"])))
    for row in chosen[:16]:
        rows.append(
            [
                str(row["candidate_name"]),
                str(row["burnin_regime"]),
                str(row["metric"]),
                f"{safe_float(row['slope_per_initial_node']):.5f}",
                f"{safe_float(row['ci_low_slope']):.5f}",
                f"{safe_float(row['ci_high_slope']):.5f}",
            ]
        )
    return markdown_table(rows)


def make_technical_md(
    candidates: Sequence[v08b.CandidatePoint],
    aggregate_rows: Sequence[Dict[str, Any]],
    slope_rows: Sequence[Dict[str, Any]],
    *,
    run_csv: str,
    aggregate_csv: str,
    slope_csv: str,
) -> str:
    lines = [
        "# Relasjonell universgraf v0.9 – skala og naturlige ensembler",
        "",
        "## Hva som ble gjort",
        "",
        "v0.9 tar v0.8b-kandidatbåndet og presser det mot større, modellvokste startensembler. I denne runden brukes naturlige målområder rundt 64, 96 og 128 noder, og hvert størrelsesnivå kjøres i to burn-in-regimer: `moderate` og `deep`.",
        "",
        "De faktiske realiserte startstørrelsene må leses fra `mean_initial_nodes` i aggregate-CSV-en; veksten treffer ikke alltid nominalt mål eksakt.",
        "",
        "Kandidatene i denne runden er hentet fra toppdelen av v0.8b-rangeringen etter `ci_low_mean_composite_natural`; v0.9 innfører ingen ny samlescore. Fokus ligger i stedet på rå størrelsesavhengige mål og bootstrap-intervaller.",
        "",
        "## Mål som rapporteres",
        "",
        "- `avg_local_overlap`",
        "- `final_radius_control`",
        "- `final_edge_diff_count`",
        "- `abs_drift_beta1_per_step`",
        "- `abs_drift_spectral_radius_per_step`",
        "",
        "Merk forskjellen mellom observasjon og fortolkning:",
        "",
        "- observasjon: bootstrap-intervallene og slope-estimatene i CSV-filene,",
        "- fortolkning: om små eller flate slope-verdier faktisk betyr en robust makroskopisk klasse.",
        "",
        "## Kandidater i v0.9-shortlisten",
        "",
    ]
    for point in candidates:
        lines.append(
            f"- `{point.name}` = ({point.r_birth:.2f}, {point.r_death:.2f}, {point.p_swap:.2f}, {point.p_triad:.2f}, {point.p_del:.2f})"
        )
    lines.extend(
        [
            "",
            "## Aggregerte gruppeestimater",
            "",
            top_table(aggregate_rows),
            "",
            "## Skalaslope-estimater",
            "",
            slope_table(slope_rows),
            "",
            "## Foreløpig tolkning",
            "",
            "Hvis et regime er virkelig robust på tvers av naturlig skala, bør vi se at overlap ikke kollapser raskt når initial størrelse vokser, samtidig som slutt-radius og de to driftmålene ikke blåser opp ukontrollert. Det er dette slope-tabellen forsøker å synliggjøre.",
            "",
            "Denne runden beviser ikke en skarp faseovergang. Den svarer bare på en smalere, viktigere metodefråge: om de beste v0.8b-kandidatene fortsatt ser lesbare ut når starttilstandene blir større og mer naturlig genererte.",
            "",
            "## Filer",
            "",
            f"- run CSV: `{run_csv}`",
            f"- aggregate CSV: `{aggregate_csv}`",
            f"- slope CSV: `{slope_csv}`",
            "",
        ]
    )
    return "\n".join(lines)


def make_lay_md(aggregate_rows: Sequence[Dict[str, Any]], slope_rows: Sequence[Dict[str, Any]]) -> str:
    best_overlap = max(aggregate_rows, key=lambda row: safe_float(row["mean_avg_local_overlap"], -1.0))
    best_radius = min(aggregate_rows, key=lambda row: safe_float(row["mean_final_radius_control"], float("inf")))
    calmest = min(slope_rows, key=lambda row: abs(safe_float(row["slope_per_initial_node"], float("inf"))))
    lines = [
        "# Relasjonell universgraf v0.9 – enkel forklaring",
        "",
        "## Hva er nytt her?",
        "",
        "I stedet for bare å spørre hvilke regler som ser bra ut på moderate testgrafer, spør vi nå om de samme reglene fortsatt holder formen når startuniversene blir mye større.",
        "",
        "Størrelsene i denne runden er målområder, ikke eksakte fasitsvar. Derfor er det de realiserte startstørrelsene i CSV-filene som teller analytisk.",
        "",
        "Vi måler ikke dette med én ny totalscore. Vi ser direkte på fem ting: lokal likhet mellom grenene, hvor langt forskjellen sprer seg, hvor mange kanter som er forskjellige til slutt, og hvor mye to sentrale strukturmål driver.",
        "",
        "## Hva ser mest lovende ut akkurat nå?",
        "",
        f"- Høyest lokal overlap i denne runden kom fra `{best_overlap['candidate_name']}` i `{best_overlap['burnin_regime']}` ved mål {int(safe_float(best_overlap['size_target']))} noder.",
        f"- Lavest slutt-radius kom fra `{best_radius['candidate_name']}` i `{best_radius['burnin_regime']}` ved mål {int(safe_float(best_radius['size_target']))} noder.",
        f"- Den flatteste enkeltslope-estimatet kom på metrikken `{calmest['metric']}` for `{calmest['candidate_name']}` i `{calmest['burnin_regime']}`.",
        "",
        "## Hvordan dette bør tolkes",
        "",
        "Hvis de beste kandidatene fortsatt ser rimelig stabile ut når grafen blir mye større, er det et bedre tegn enn at de bare var pene på små leketøy-eksempler. Hvis de derimot forverres raskt med størrelse, er det en advarsel om at vi kanskje bare har funnet et småskala-fenomen.",
        "",
        "Dette steget sier derfor mer om prosjektets modenhet enn om endelig fysikk. Vi prøver å finne ut om de samme mønstrene overlever når vi slutter å holde universet kunstig lite.",
        "",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scale the v0.8b candidate band to larger natural ensembles.")
    parser.add_argument("--steps", type=int, default=240)
    parser.add_argument("--seeds", type=str, default="301,302,303,304")
    parser.add_argument("--candidate-top-n", type=int, default=4)
    parser.add_argument("--bootstrap-reps", type=int, default=200)
    parser.add_argument("--growth-seed-offset", type=int, default=9000)
    parser.add_argument("--v08b-overall-csv", type=str, default="Documentation/v08b_candidate_robustness.csv")
    parser.add_argument("--run-csv", type=str, default="Documentation/v09_scale_runs.csv")
    parser.add_argument("--aggregate-csv", type=str, default="Documentation/v09_scale_aggregate.csv")
    parser.add_argument("--slope-csv", type=str, default="Documentation/v09_scale_slopes.csv")
    parser.add_argument("--tech-md", type=str, default="Documentation/relasjonell_universgraf_v0_9_skala_og_naturlige_ensembler.md")
    parser.add_argument("--lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_9.md")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    seeds = [int(piece.strip()) for piece in args.seeds.split(",") if piece.strip()]
    candidates = pick_candidates(args.v08b_overall_csv, top_n=args.candidate_top_n)
    ensembles = scale_ensembles()
    growth_params = v08b.reference_growth_params()

    base_cache: Dict[Tuple[str, int], v7.State] = {}
    for plan in ensembles:
        spec = growth_spec(plan)
        for index, seed in enumerate(seeds):
            growth_seed = args.growth_seed_offset + plan.target_nodes * 100 + index * 13 + sum(ord(c) for c in plan.name)
            base_cache[(plan.name, seed)] = v08b.grow_state_for_ensemble(spec, rng_seed=growth_seed, growth_params=growth_params)

    run_rows: List[Dict[str, Any]] = []
    for point in candidates:
        for plan in ensembles:
            for seed in seeds:
                base_state = base_cache[(plan.name, seed)]
                run_rows.append(collect_scale_run(point, plan, base_state, seed=seed, steps=args.steps))

    grouped: Dict[Tuple[str, str, int, float, float, float, float, float], List[Dict[str, Any]]] = {}
    for row in run_rows:
        key = (
            str(row["candidate_name"]),
            str(row["burnin_regime"]),
            int(safe_float(row["size_target"])),
            safe_float(row["r_birth"]),
            safe_float(row["r_death"]),
            safe_float(row["p_swap"]),
            safe_float(row["p_triad"]),
            safe_float(row["p_del"]),
        )
        grouped.setdefault(key, []).append(row)

    aggregate_rows = [
        summarize_group(rows, bootstrap_reps=args.bootstrap_reps, rng_seed=1000 + idx * 17)
        for idx, rows in enumerate(grouped.values())
    ]
    slope_rows = summarize_slopes(run_rows, bootstrap_reps=args.bootstrap_reps, rng_seed=24680)

    write_csv(args.run_csv, run_rows)
    write_csv(args.aggregate_csv, aggregate_rows)
    write_csv(args.slope_csv, slope_rows)
    for path in [args.tech_md, args.lay_md]:
        ensure_parent_dir(path)
    Path(args.tech_md).write_text(
        make_technical_md(
            candidates,
            aggregate_rows,
            slope_rows,
            run_csv=args.run_csv,
            aggregate_csv=args.aggregate_csv,
            slope_csv=args.slope_csv,
        ),
        encoding="utf-8",
    )
    Path(args.lay_md).write_text(make_lay_md(aggregate_rows, slope_rows), encoding="utf-8")


if __name__ == "__main__":
    main()
