#!/usr/bin/env python3
"""v0.9b size-extension and asymptotic diagnostics for relational universe."""

from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import relational_universe_v09_scale_and_natural_ensembles as v09


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


def parse_candidates(candidate_csv: str | Path, *, top_n: int) -> List[v09.ScaleCandidate]:
    rows = load_rows(candidate_csv)
    if not rows:
        return v09.default_candidates()[:top_n]
    out: List[v09.ScaleCandidate] = []
    for row in rows[:top_n]:
        out.append(
            v09.ScaleCandidate(
                name=str(row["candidate_name"]),
                r_birth=safe_float(row["r_birth"]),
                r_death=safe_float(row["r_death"]),
                p_swap=safe_float(row["p_swap"]),
                p_triad=safe_float(row["p_triad"]),
                p_del=safe_float(row["p_del"]),
            )
        )
    return out


def extended_ensembles() -> List[v09.ScaleEnsemble]:
    return [
        v09.ScaleEnsemble("natural96_light", 96, "light", 14, 7, 2200, 80, 180),
        v09.ScaleEnsemble("natural96_deep", 96, "deep", 14, 7, 3400, 320, 520),
        v09.ScaleEnsemble("natural144_light", 144, "light", 16, 8, 3400, 120, 240),
        v09.ScaleEnsemble("natural144_deep", 144, "deep", 16, 8, 4800, 320, 560),
        v09.ScaleEnsemble("natural192_light", 192, "light", 18, 9, 4600, 160, 300),
        v09.ScaleEnsemble("natural192_deep", 192, "deep", 18, 9, 6200, 420, 700),
    ]


def filter_tail(group_rows: Sequence[Dict[str, Any]], *, min_target: int) -> List[Dict[str, Any]]:
    return [row for row in group_rows if int(round(safe_float(row["target_nodes"]))) >= min_target]


def asymptotic_metrics(group_rows: Sequence[Dict[str, Any]], *, min_target: int, extrapolate_to: int) -> Dict[str, float]:
    tail = filter_tail(group_rows, min_target=min_target)
    scale = v09.fit_scale_metrics(tail)
    log_n = math.log(float(extrapolate_to))
    radius_pred = float("nan")
    overlap_pred = float("nan")
    quasi_pred = float("nan")
    if math.isfinite(scale["radius_alpha"]) and math.isfinite(scale["radius_alpha_intercept"]):
        radius_pred = math.exp(scale["radius_alpha_intercept"] + scale["radius_alpha"] * log_n) - 1.0
    if math.isfinite(scale["overlap_vs_logN_slope"]) and math.isfinite(scale["overlap_vs_logN_intercept"]):
        overlap_pred = scale["overlap_vs_logN_intercept"] + scale["overlap_vs_logN_slope"] * log_n
    if math.isfinite(scale["quasi_vs_logN_slope"]) and math.isfinite(scale["quasi_vs_logN_intercept"]):
        quasi_pred = scale["quasi_vs_logN_intercept"] + scale["quasi_vs_logN_slope"] * log_n
    return {
        "tail_group_rows": len(tail),
        "radius_alpha_tail": scale["radius_alpha"],
        "radius_alpha_tail_intercept": scale["radius_alpha_intercept"],
        "overlap_vs_logN_tail_slope": scale["overlap_vs_logN_slope"],
        "quasi_vs_logN_tail_slope": scale["quasi_vs_logN_slope"],
        f"pred_radius_at_{extrapolate_to}": radius_pred,
        f"pred_overlap_at_{extrapolate_to}": overlap_pred,
        f"pred_quasi_at_{extrapolate_to}": quasi_pred,
    }


def bootstrap_asymptotics(
    point: v09.ScaleCandidate,
    ensembles: Sequence[v09.ScaleEnsemble],
    run_rows: Sequence[Dict[str, Any]],
    ranges: Dict[str, Tuple[float, float, bool]],
    *,
    min_target: int,
    extrapolate_to: int,
    reps: int,
    rng_seed: int,
) -> Dict[str, float]:
    rng = random.Random(rng_seed)
    by_ensemble: Dict[str, List[Dict[str, Any]]] = {}
    for row in run_rows:
        by_ensemble.setdefault(str(row["ensemble"]), []).append(row)
    radius_vals: List[float] = []
    overlap_vals: List[float] = []
    quasi_vals: List[float] = []
    pred_radius_vals: List[float] = []
    for _ in range(max(1, reps)):
        sample_group_rows: List[Dict[str, Any]] = []
        for ensemble in ensembles:
            rows = by_ensemble.get(ensemble.name, [])
            if not rows:
                continue
            sample = [rows[rng.randrange(len(rows))] for _ in range(len(rows))]
            agg = v09.summarize_group(point, ensemble, sample)
            agg.update(v09.score_row_from_ranges(agg, ranges))
            sample_group_rows.append(agg)
        metrics = asymptotic_metrics(sample_group_rows, min_target=min_target, extrapolate_to=extrapolate_to)
        radius_vals.append(metrics["radius_alpha_tail"])
        overlap_vals.append(metrics["overlap_vs_logN_tail_slope"])
        quasi_vals.append(metrics["quasi_vs_logN_tail_slope"])
        pred_radius_vals.append(metrics[f"pred_radius_at_{extrapolate_to}"])
    return {
        "ci_low_radius_alpha_tail": quantile(radius_vals, 0.025),
        "ci_high_radius_alpha_tail": quantile(radius_vals, 0.975),
        "ci_low_overlap_vs_logN_tail": quantile(overlap_vals, 0.025),
        "ci_high_overlap_vs_logN_tail": quantile(overlap_vals, 0.975),
        "ci_low_quasi_vs_logN_tail": quantile(quasi_vals, 0.025),
        "ci_high_quasi_vs_logN_tail": quantile(quasi_vals, 0.975),
        f"ci_low_pred_radius_at_{extrapolate_to}": quantile(pred_radius_vals, 0.025),
        f"ci_high_pred_radius_at_{extrapolate_to}": quantile(pred_radius_vals, 0.975),
    }


def asymptotic_summary_rows(
    candidates: Sequence[v09.ScaleCandidate],
    ensembles: Sequence[v09.ScaleEnsemble],
    run_rows: Sequence[Dict[str, Any]],
    group_rows: Sequence[Dict[str, Any]],
    candidate_rows: Sequence[Dict[str, Any]],
    *,
    min_target: int,
    extrapolate_to: int,
    bootstrap_reps: int,
    bootstrap_seed: int,
) -> List[Dict[str, Any]]:
    ranges = v09.score_ranges(list(group_rows))
    candidate_lookup = {str(row["candidate_name"]): row for row in candidate_rows}
    rows: List[Dict[str, Any]] = []
    for index, point in enumerate(candidates):
        sub_group = [row for row in group_rows if str(row["candidate_name"]) == point.name]
        sub_run = [row for row in run_rows if str(row["candidate_name"]) == point.name]
        asym = asymptotic_metrics(sub_group, min_target=min_target, extrapolate_to=extrapolate_to)
        boot = bootstrap_asymptotics(
            point,
            ensembles,
            sub_run,
            ranges,
            min_target=min_target,
            extrapolate_to=extrapolate_to,
            reps=bootstrap_reps,
            rng_seed=bootstrap_seed + index * 101,
        )
        base = candidate_lookup.get(point.name, {})
        rows.append(
            {
                "candidate_name": point.name,
                "r_birth": point.r_birth,
                "r_death": point.r_death,
                "p_swap": point.p_swap,
                "p_triad": point.p_triad,
                "p_del": point.p_del,
                "mean_composite": safe_float(base.get("mean_composite")),
                "ci_low_mean_composite": safe_float(base.get("ci_low_mean_composite")),
                **asym,
                **boot,
            }
        )
    rows.sort(
        key=lambda row: (
            safe_float(row["ci_low_mean_composite"], -1.0),
            -safe_float(row["radius_alpha_tail"], float("inf")),
        ),
        reverse=True,
    )
    return rows


def top_table(rows: Sequence[Dict[str, Any]], extrapolate_to: int) -> str:
    table = [[
        "candidate",
        "mean composite",
        "CI low",
        "tail radius α",
        "tail overlap slope",
        "tail quasi slope",
        f"pred radius@{extrapolate_to}",
    ]]
    for row in rows[:6]:
        table.append([
            str(row["candidate_name"]),
            f"{safe_float(row['mean_composite']):.3f}",
            f"{safe_float(row['ci_low_mean_composite']):.3f}",
            f"{safe_float(row['radius_alpha_tail']):.3f}",
            f"{safe_float(row['overlap_vs_logN_tail_slope']):.3f}",
            f"{safe_float(row['quasi_vs_logN_tail_slope']):.3f}",
            f"{safe_float(row[f'pred_radius_at_{extrapolate_to}']):.2f}",
        ])
    return markdown_table(table)


def write_technical_md(path: str | Path, asym_rows: Sequence[Dict[str, Any]], *, min_target: int, extrapolate_to: int) -> None:
    best = asym_rows[0] if asym_rows else None
    lines = [
        "# Relasjonell universgraf v0.9b – størrelse og asymptotikk",
        "",
        "## Hva som er nytt i forhold til v0.9",
        "",
        "v0.9b utvider samme metodiske oppsett til større naturlige ensembler og skiller eksplisitt mellom rå målinger og skalaekstrapolasjon.",
        "",
        f"- Tail-analyse bruker bare gruppenivåer med målskala >= {min_target}.",
        f"- Ekstrapolasjonene i denne runden er rapportert ved nominell størrelse {extrapolate_to}.",
        "",
        "## Rå observasjon vs ekstrapolasjon",
        "",
        "- Rå observasjon: run- og group-CSV-ene viser hva som faktisk ble målt ved de konkrete ensemble-størrelsene.",
        "- Ekstrapolasjon: asymptotic-summary-CSV-en viser tail-fits og projiserte verdier. Disse er modellbaserte lesninger av dataene, ikke direkte observasjoner.",
        "",
        "## Kandidater",
        "",
        top_table(asym_rows, extrapolate_to),
        "",
    ]
    if best is not None:
        lines.extend([
            "## Foreløpig beste asymptotiske kandidat",
            "",
            f"- kandidat: `{best['candidate_name']}`",
            f"- mean composite: {safe_float(best['mean_composite']):.3f}",
            f"- tail radius α: {safe_float(best['radius_alpha_tail']):.3f}",
            f"- tail overlap slope: {safe_float(best['overlap_vs_logN_tail_slope']):.3f}",
            f"- tail quasi slope: {safe_float(best['quasi_vs_logN_tail_slope']):.3f}",
            f"- predikert radius ved {extrapolate_to}: {safe_float(best[f'pred_radius_at_{extrapolate_to}']):.2f}",
            "",
            "## Tolkning",
            "",
            "En lovende kandidat i v0.9b bør kombinere akseptabel composite med en lav tail-radius-eksponent og ikke for negativ tail-slope i overlap og quasi. Dette er fortsatt en asymptotisk lesning av begrensede data, ikke et bevis på en endelig storklassesfase.",
            "",
        ])
    write_path = Path(path)
    write_path.parent.mkdir(parents=True, exist_ok=True)
    write_path.write_text("\n".join(lines), encoding="utf-8")


def write_status_md(path: str | Path, asym_rows: Sequence[Dict[str, Any]]) -> None:
    best = asym_rows[0] if asym_rows else None
    lines = [
        "# Statusnotat v0.9b",
        "",
        "v0.9b presser v0.9-kandidatene til større naturlige ensembler og legger til en eksplisitt tail-lest asymptotikk.",
        "",
    ]
    if best is not None:
        lines.extend([
            f"- Foreløpig beste kandidat: `{best['candidate_name']}`",
            f"- Tail radius α: {safe_float(best['radius_alpha_tail']):.3f}",
            f"- Tail overlap slope: {safe_float(best['overlap_vs_logN_tail_slope']):.3f}",
            f"- Tail quasi slope: {safe_float(best['quasi_vs_logN_tail_slope']):.3f}",
        ])
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_lay_md(path: str | Path, asym_rows: Sequence[Dict[str, Any]], extrapolate_to: int) -> None:
    best = asym_rows[0] if asym_rows else None
    lines = [
        "# Relasjonell universgraf v0.9b – enkel forklaring",
        "",
        "I denne runden gjør vi ikke bare større tester. Vi prøver også å lese hvilken retning kandidatene peker i hvis universene blir enda større enn det vi faktisk rakk å simulere direkte.",
        "",
        "Det betyr at vi skiller mellom to ting:",
        "- hva simulatoren faktisk målte på de store grafene vi kjørte,",
        "- og hva en forsiktig skala-tilpasning antyder for enda større størrelser.",
        "",
    ]
    if best is not None:
        lines.extend([
            f"Den mest lovende kandidaten i denne runden er `{best['candidate_name']}`.",
            f"Dersom tail-tilpasningen holder, antyder den en radius rundt {safe_float(best[f'pred_radius_at_{extrapolate_to}']):.2f} ved nominell størrelse {extrapolate_to}.",
            "",
            "Dette er fortsatt ikke et bevis. Men det er en mer moden måte å spørre om prosjektet holder retning når vi ikke lenger bare ser på små eller mellomstore eksempler.",
        ])
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_findings_md(path: str | Path, asym_rows: Sequence[Dict[str, Any]]) -> None:
    lines = [
        "# v0.9b – hovedfunn og implikasjoner",
        "",
    ]
    for index, row in enumerate(asym_rows[:5], start=1):
        lines.append(
            f"{index}. `{row['candidate_name']}`: composite ≈ {safe_float(row['mean_composite']):.3f}, tail radius α ≈ {safe_float(row['radius_alpha_tail']):.3f}, tail overlap slope ≈ {safe_float(row['overlap_vs_logN_tail_slope']):.3f}, tail quasi slope ≈ {safe_float(row['quasi_vs_logN_tail_slope']):.3f}."
        )
    lines.extend([
        "",
        "Dette betyr at prosjektet nå har tatt et første steg fra ren finite-size-lesning til eksplisitt asymptotisk hypotesebygging. Det øker verdien av de gode kandidatene, men øker også kravet til ærlighet om usikkerhet.",
    ])
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_readme(path: str | Path, produced: Sequence[str]) -> None:
    lines = ["# README – v0.9b størrelse og asymptotikk", ""]
    for item in produced:
        lines.append(f"- `{Path(item).name}`")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extend v0.9 to larger ensembles and asymptotic diagnostics.")
    parser.add_argument("--v09-candidate-csv", default="Documentation/v09_scale_candidate_summary.csv")
    parser.add_argument("--out-dir", default="Documentation")
    parser.add_argument("--candidate-top-n", type=int, default=3)
    parser.add_argument("--num-growth-seeds", type=int, default=2)
    parser.add_argument("--growth-seed-start", type=int, default=701)
    parser.add_argument("--steps-per-node", type=float, default=4.5)
    parser.add_argument("--min-steps", type=int, default=140)
    parser.add_argument("--max-steps", type=int, default=420)
    parser.add_argument("--bootstrap-reps", type=int, default=40)
    parser.add_argument("--bootstrap-seed", type=int, default=23456)
    parser.add_argument("--tail-min-target", type=int, default=96)
    parser.add_argument("--extrapolate-to", type=int, default=256)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    candidates = parse_candidates(args.v09_candidate_csv, top_n=args.candidate_top_n)
    ensembles = extended_ensembles()
    growth_seeds = [args.growth_seed_start + 101 * i for i in range(args.num_growth_seeds)]
    results = v09.run_v09(
        candidates,
        ensembles,
        growth_seeds,
        steps_per_node=args.steps_per_node,
        min_steps=args.min_steps,
        max_steps=args.max_steps,
        bootstrap_reps=args.bootstrap_reps,
        bootstrap_seed=args.bootstrap_seed,
    )
    asym_rows = asymptotic_summary_rows(
        candidates,
        ensembles,
        results["run_rows"],
        results["group_rows"],
        results["candidate_summary_rows"],
        min_target=args.tail_min_target,
        extrapolate_to=args.extrapolate_to,
        bootstrap_reps=args.bootstrap_reps,
        bootstrap_seed=args.bootstrap_seed + 900,
    )

    run_csv = out_dir / "v09b_scale_run_rows.csv"
    group_csv = out_dir / "v09b_scale_group_rows.csv"
    cand_csv = out_dir / "v09b_scale_candidate_summary.csv"
    ens_csv = out_dir / "v09b_scale_ensemble_summary.csv"
    asym_csv = out_dir / "v09b_scale_asymptotic_summary.csv"
    write_csv(run_csv, results["run_rows"])
    write_csv(group_csv, results["group_rows"])
    write_csv(cand_csv, results["candidate_summary_rows"])
    write_csv(ens_csv, results["ensemble_summary_rows"])
    write_csv(asym_csv, asym_rows)

    tech_md = out_dir / "relasjonell_universgraf_v0_9b_storrelse_og_asymptotikk.md"
    status_md = out_dir / "relasjonell_universgraf_status_v0_9b.md"
    lay_md = out_dir / "relasjonell_universgraf_for_ikke_spesialister_v0_9b.md"
    findings_md = out_dir / "v0_9b_hovedfunn_og_implikasjoner.md"
    readme_md = out_dir / "README_relational_universe_bundle_v9b.md"
    write_technical_md(tech_md, asym_rows, min_target=args.tail_min_target, extrapolate_to=args.extrapolate_to)
    write_status_md(status_md, asym_rows)
    write_lay_md(lay_md, asym_rows, extrapolate_to=args.extrapolate_to)
    write_findings_md(findings_md, asym_rows)
    write_readme(readme_md, [str(run_csv), str(group_csv), str(cand_csv), str(ens_csv), str(asym_csv), str(tech_md), str(status_md), str(lay_md), str(findings_md)])


if __name__ == "__main__":
    main()
