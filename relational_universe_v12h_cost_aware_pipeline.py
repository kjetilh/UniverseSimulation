#!/usr/bin/env python3
"""v0.12h cost-aware follow-up pipeline after v12g.

This script asks whether compact screening policies become operationally
competitive once screening cost is allowed to matter, rather than counting only
the expensive follow-up runs.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple


REFERENCE_POLICY = "full_basis"
REFERENCE_BUDGET = 0.50
PIPELINES = [
    ("full_basis", 0.50),
    ("spectral_only", 0.50),
    ("spectral_only", 0.667),
    ("spectral_plus_dim", 0.50),
    ("spectral_plus_dim", 0.667),
    ("random_baseline", 0.50),
]
SCREEN_COST_LEVELS = [0.00, 0.01, 0.02, 0.04, 0.06, 0.08, 0.10]
EPSILON = 0.02


def safe_float(x: Any, default: float = float("nan")) -> float:
    try:
        y = float(x)
    except Exception:
        return default
    if math.isnan(y) or math.isinf(y):
        return default
    return y


def mean_defined(values: Iterable[float]) -> float:
    vals = [safe_float(v) for v in values]
    vals = [v for v in vals if math.isfinite(v)]
    return (sum(vals) / len(vals)) if vals else float("nan")


def read_csv(path: str | Path) -> List[Dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys: List[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                keys.append(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def nearest_budget(rows: Sequence[Dict[str, Any]], target_budget: float) -> Dict[str, Any]:
    return min(rows, key=lambda r: abs(safe_float(r["budget_frac"]) - target_budget))


def estimate_test_rows(row: Dict[str, Any]) -> int:
    selected = safe_float(row["selected_rows"], 0.0)
    budget = safe_float(row["budget_frac"], 1.0)
    if budget <= 1e-12:
        return 0
    return int(round(selected / budget))


def per_split_cost_rows(policy_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_split_policy: Dict[Tuple[int, str], List[Dict[str, Any]]] = {}
    for row in policy_rows:
        by_split_policy.setdefault((int(row["split_id"]), str(row["policy_name"])), []).append(dict(row))

    split_ids = sorted({int(r["split_id"]) for r in policy_rows})
    out: List[Dict[str, Any]] = []
    for split_id in split_ids:
        ref = nearest_budget(by_split_policy[(split_id, REFERENCE_POLICY)], REFERENCE_BUDGET)
        test_rows = estimate_test_rows(ref)
        ref_hit = safe_float(ref["within_target_best_hit"])
        ref_recall = safe_float(ref["within_target_top_quartile_recall"])
        ref_lift = safe_float(ref["within_target_selected_lift"])
        ref_selected = safe_float(ref["selected_rows"])
        ref_feat = safe_float(ref["feature_count"])

        for screen_cost in SCREEN_COST_LEVELS:
            ref_total_cost = ref_selected + screen_cost * ref_feat * test_rows
            for policy_name, budget in PIPELINES:
                row = nearest_budget(by_split_policy[(split_id, policy_name)], budget)
                selected = safe_float(row["selected_rows"])
                feat = safe_float(row["feature_count"])
                total_cost = selected + screen_cost * feat * test_rows
                hit = safe_float(row["within_target_best_hit"])
                recall = safe_float(row["within_target_top_quartile_recall"])
                lift = safe_float(row["within_target_selected_lift"])
                cost_delta = total_cost - ref_total_cost
                within_eps = 1 if (hit >= ref_hit - EPSILON and recall >= ref_recall - EPSILON) else 0
                out.append(
                    {
                        "split_id": split_id,
                        "screen_cost_per_feature": screen_cost,
                        "policy_name": policy_name,
                        "budget_frac": safe_float(row["budget_frac"]),
                        "feature_count": int(feat),
                        "estimated_test_rows": test_rows,
                        "selected_rows": selected,
                        "total_cost": total_cost,
                        "ref_total_cost": ref_total_cost,
                        "cost_delta_vs_ref": cost_delta,
                        "cost_ratio_vs_ref": total_cost / ref_total_cost if ref_total_cost > 1e-12 else float("nan"),
                        "within_target_best_hit": hit,
                        "within_target_top_quartile_recall": recall,
                        "within_target_selected_lift": lift,
                        "delta_best_hit_vs_ref": hit - ref_hit,
                        "delta_recall_vs_ref": recall - ref_recall,
                        "delta_lift_vs_ref": lift - ref_lift,
                        "cost_neutral_or_better": 1 if total_cost <= ref_total_cost + 1e-12 else 0,
                        "near_match_eps_02": within_eps,
                        "cost_neutral_and_near_match": 1 if (total_cost <= ref_total_cost + 1e-12 and within_eps) else 0,
                    }
                )
    return out


def aggregate_cost_rows(cost_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    keys = sorted({(safe_float(r["screen_cost_per_feature"]), str(r["policy_name"]), safe_float(r["budget_frac"])) for r in cost_rows})
    out: List[Dict[str, Any]] = []
    for screen_cost, policy_name, budget in keys:
        sub = [
            r
            for r in cost_rows
            if abs(safe_float(r["screen_cost_per_feature"]) - screen_cost) <= 1e-12
            and str(r["policy_name"]) == policy_name
            and abs(safe_float(r["budget_frac"]) - budget) <= 1e-9
        ]
        out.append(
            {
                "screen_cost_per_feature": screen_cost,
                "policy_name": policy_name,
                "budget_frac": budget,
                "mean_total_cost": mean_defined(safe_float(r["total_cost"]) for r in sub),
                "mean_cost_ratio_vs_ref": mean_defined(safe_float(r["cost_ratio_vs_ref"]) for r in sub),
                "mean_cost_delta_vs_ref": mean_defined(safe_float(r["cost_delta_vs_ref"]) for r in sub),
                "mean_best_hit": mean_defined(safe_float(r["within_target_best_hit"]) for r in sub),
                "mean_recall": mean_defined(safe_float(r["within_target_top_quartile_recall"]) for r in sub),
                "mean_lift": mean_defined(safe_float(r["within_target_selected_lift"]) for r in sub),
                "mean_delta_best_hit_vs_ref": mean_defined(safe_float(r["delta_best_hit_vs_ref"]) for r in sub),
                "mean_delta_recall_vs_ref": mean_defined(safe_float(r["delta_recall_vs_ref"]) for r in sub),
                "cost_neutral_rate": mean_defined(safe_float(r["cost_neutral_or_better"]) for r in sub),
                "near_match_rate_eps_02": mean_defined(safe_float(r["near_match_eps_02"]) for r in sub),
                "cost_neutral_and_near_match_rate": mean_defined(safe_float(r["cost_neutral_and_near_match"]) for r in sub),
            }
        )
    return out


def screen_cost_summary_rows(aggregate_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for screen_cost in sorted({safe_float(r["screen_cost_per_feature"]) for r in aggregate_rows}):
        sub = [r for r in aggregate_rows if abs(safe_float(r["screen_cost_per_feature"]) - screen_cost) <= 1e-12]
        best = max(
            sub,
            key=lambda r: (
                safe_float(r["cost_neutral_and_near_match_rate"], -1e9),
                safe_float(r["near_match_rate_eps_02"], -1e9),
                safe_float(r["mean_cost_delta_vs_ref"], -1e9),
            ),
        )
        out.append(
            {
                "screen_cost_per_feature": screen_cost,
                "best_policy_name": best["policy_name"],
                "best_budget_frac": best["budget_frac"],
                "best_cost_neutral_and_near_match_rate": best["cost_neutral_and_near_match_rate"],
                "best_near_match_rate_eps_02": best["near_match_rate_eps_02"],
                "best_mean_cost_delta_vs_ref": best["mean_cost_delta_vs_ref"],
                "best_mean_delta_best_hit_vs_ref": best["mean_delta_best_hit_vs_ref"],
                "best_mean_delta_recall_vs_ref": best["mean_delta_recall_vs_ref"],
            }
        )
    return out


def compact_screen_cost_summary_rows(aggregate_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for screen_cost in sorted({safe_float(r["screen_cost_per_feature"]) for r in aggregate_rows}):
        sub = [
            r for r in aggregate_rows
            if abs(safe_float(r["screen_cost_per_feature"]) - screen_cost) <= 1e-12
            and str(r["policy_name"]) != REFERENCE_POLICY
            and str(r["policy_name"]) != "random_baseline"
        ]
        best = max(
            sub,
            key=lambda r: (
                safe_float(r["cost_neutral_and_near_match_rate"], -1e9),
                safe_float(r["near_match_rate_eps_02"], -1e9),
                -abs(safe_float(r["mean_cost_delta_vs_ref"], 1e9)),
            ),
        )
        out.append(
            {
                "screen_cost_per_feature": screen_cost,
                "best_compact_policy_name": best["policy_name"],
                "best_compact_budget_frac": best["budget_frac"],
                "best_compact_cost_neutral_and_near_match_rate": best["cost_neutral_and_near_match_rate"],
                "best_compact_near_match_rate_eps_02": best["near_match_rate_eps_02"],
                "best_compact_mean_cost_delta_vs_ref": best["mean_cost_delta_vs_ref"],
                "best_compact_mean_delta_best_hit_vs_ref": best["mean_delta_best_hit_vs_ref"],
                "best_compact_mean_delta_recall_vs_ref": best["mean_delta_recall_vs_ref"],
            }
        )
    return out


def build_report(
    aggregate_rows: Sequence[Dict[str, Any]],
    screen_cost_rows: Sequence[Dict[str, Any]],
    compact_rows: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.12h: kostnadsbevisst oppfølgingspipeline")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden legger et enkelt kostnadsregnskap oppa v12g. Maalet er a skille mellom to forskjellige pastander: 'samme oppfolgingsbudsjett' og 'samme totale arbeidskostnad'."
    )
    lines.append("")
    lines.append("## Kostnadsmodell")
    lines.append("")
    lines.append("- En dyr oppfolgingskjoring teller som kostnad `1.0`.")
    lines.append("- Screening teller `screen_cost_per_feature` per feature per testkandidat.")
    lines.append("- Dette er en eksplisitt arbeidsmodell, ikke ny fysikk. Den bor leses som ingeniormessig regnskap.")
    lines.append("")
    lines.append("## Policyer per skjermkostnad")
    lines.append("")
    lines.append("| screen_cost | policy | budget | cost_ratio_vs_ref | best_hit | recall | d_best_hit | d_recall | cost_neutral_rate | near_match_eps_02 | cost_neutral_and_match |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate_rows:
        lines.append(
            f"| {safe_float(row['screen_cost_per_feature']):.3f} | {row['policy_name']} | {safe_float(row['budget_frac']):.3f} | "
            f"{safe_float(row['mean_cost_ratio_vs_ref']):.3f} | {safe_float(row['mean_best_hit']):.3f} | {safe_float(row['mean_recall']):.3f} | "
            f"{safe_float(row['mean_delta_best_hit_vs_ref']):.3f} | {safe_float(row['mean_delta_recall_vs_ref']):.3f} | "
            f"{safe_float(row['cost_neutral_rate']):.3f} | {safe_float(row['near_match_rate_eps_02']):.3f} | {safe_float(row['cost_neutral_and_near_match_rate']):.3f} |"
        )
    lines.append("")
    lines.append("## Beste policy per skjermkostnad")
    lines.append("")
    lines.append("| screen_cost | best_policy | budget | cost_neutral_and_match | near_match_eps_02 | mean_cost_delta_vs_ref |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in screen_cost_rows:
        lines.append(
            f"| {safe_float(row['screen_cost_per_feature']):.3f} | {row['best_policy_name']} | {safe_float(row['best_budget_frac']):.3f} | "
            f"{safe_float(row['best_cost_neutral_and_near_match_rate']):.3f} | {safe_float(row['best_near_match_rate_eps_02']):.3f} | {safe_float(row['best_mean_cost_delta_vs_ref']):.3f} |"
        )
    lines.append("")
    lines.append("## Beste ikke-referanse-policy per skjermkostnad")
    lines.append("")
    lines.append("| screen_cost | compact_policy | budget | compact_cost_neutral_and_match | compact_near_match_eps_02 | compact_mean_cost_delta_vs_ref |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in compact_rows:
        lines.append(
            f"| {safe_float(row['screen_cost_per_feature']):.3f} | {row['best_compact_policy_name']} | {safe_float(row['best_compact_budget_frac']):.3f} | "
            f"{safe_float(row['best_compact_cost_neutral_and_near_match_rate']):.3f} | {safe_float(row['best_compact_near_match_rate_eps_02']):.3f} | {safe_float(row['best_compact_mean_cost_delta_vs_ref']):.3f} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    same_budget = next(
        (
            r
            for r in aggregate_rows
            if str(r["policy_name"]) == "spectral_only"
            and abs(safe_float(r["budget_frac"]) - 0.50) <= 1e-9
            and abs(safe_float(r["screen_cost_per_feature"]) - 0.02) <= 1e-12
        ),
        None,
    )
    costed_challenger = next(
        (
            r
            for r in aggregate_rows
            if str(r["policy_name"]) == "spectral_plus_dim"
            and abs(safe_float(r["budget_frac"]) - 0.667) <= 1e-6
            and abs(safe_float(r["screen_cost_per_feature"]) - 0.06) <= 1e-12
        ),
        None,
    )
    if same_budget is not None:
        lines.append(
            f"- Ved lav til moderat skjermkostnad ser `spectral_only@0.50` fortsatt ut som den riktige enkle same-budget-kandidaten. Ved `screen_cost=0.02` har den `cost_ratio_vs_ref={safe_float(same_budget['mean_cost_ratio_vs_ref']):.3f}` og `near_match_eps_02={safe_float(same_budget['near_match_rate_eps_02']):.3f}`."
        )
    if costed_challenger is not None:
        lines.append(
            f"- Naar skjermkostnaden blir tydelig ikke-neglisjerbar, blir en tyngre kompakt policy plausibel: `spectral_plus_dim@0.667` ved `screen_cost=0.06` har `cost_ratio_vs_ref={safe_float(costed_challenger['mean_cost_ratio_vs_ref']):.3f}` og `cost_neutral_and_match={safe_float(costed_challenger['cost_neutral_and_near_match_rate']):.3f}`."
        )
    lines.append(
        "- Repoet stotter derfor ikke en universell enkel vinner. Det stotter en betinget lesning: hvis screening er nesten gratis, behold `full_basis@0.50`; hvis screeningkostnaden faktisk teller litt, blir `spectral_only@0.50` mer konkurransedyktig; og ved hoyere skjermkostnad kan `spectral_plus_dim@0.667` bli en kostnadsnoytral utfordrer."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(screen_cost_rows: Sequence[Dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# v0.12h for ikke-spesialister",
            "",
            "Denne runden sjekker om den enkle geometriregelen blir mer attraktiv hvis vi teller kostnaden ved selve screeningen, ikke bare de tunge oppfolgingskjoringene.",
            "",
            "- Hvis screening nesten er gratis, er `full_basis@0.50` fortsatt best.",
            "- Hvis screening faktisk koster noe, blir kompakte regler mer interessante enn forrige runde tydet pa.",
            "",
        ]
    )


def build_recommendation() -> str:
    return "\n".join(
        [
            "# v0.12h operativ anbefaling",
            "",
            "Behold `full_basis@0.50` som standardbenchmark hvis screeningkostnaden er liten eller ukjent.",
            "Behold `spectral_only@0.50` som den viktigste enkle same-budget-kandidaten.",
            "Hvis vi senere kan ansla at screeningkostnaden faktisk er ikke-neglisjerbar, bor vi teste `spectral_plus_dim@0.667` som kostnadsnoytral utfordrer mot referansen.",
            "Det neste naturlige steget er derfor en eksplisitt arbeidsflyt med valgt kostnadsmodell eller virkelig veggklokketid: maal faktisk tid/kostnad for `full_basis@0.50` mot `spectral_only@0.50` og `spectral_plus_dim@0.667`.",
            "",
        ]
    )


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12h cost-aware follow-up pipeline")
    ap.add_argument("--policy-rows-csv", default="Documentation/v12f_budget_policy_rows.csv")
    ap.add_argument("--output-prefix", default="Documentation/v12h_cost_aware_pipeline")
    ap.add_argument("--report-md", default="Documentation/v12h_cost_aware_pipeline.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12h.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12h_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    policy_rows = read_csv(args.policy_rows_csv)
    cost_rows = per_split_cost_rows(policy_rows)
    aggregate_rows = aggregate_cost_rows(cost_rows)
    screen_cost_rows = screen_cost_summary_rows(aggregate_rows)
    compact_rows = compact_screen_cost_summary_rows(aggregate_rows)

    prefix = args.output_prefix
    write_csv(f"{prefix}_split_rows.csv", cost_rows)
    write_csv(f"{prefix}_aggregate.csv", aggregate_rows)
    write_csv(f"{prefix}_summary.csv", screen_cost_rows)
    write_csv(f"{prefix}_compact_summary.csv", compact_rows)

    for path, content in [
        (args.report_md, build_report(aggregate_rows, screen_cost_rows, compact_rows)),
        (args.lay_md, build_lay_summary(screen_cost_rows)),
        (args.recommendation_md, build_recommendation()),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
