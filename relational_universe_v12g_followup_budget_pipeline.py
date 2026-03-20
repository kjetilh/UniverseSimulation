#!/usr/bin/env python3
"""v0.12g direct follow-up pipeline evaluation based on v0.12f policy rows.

This step turns the v0.12f budget curves into a more operational reading:
which compact policies can match or nearly match the reference screening
pipeline, and how many expensive follow-up runs they would actually save.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple


REFERENCE_POLICY = "full_basis"
REFERENCE_BUDGET = 0.50
CANDIDATE_PIPELINES = [
    ("full_basis", 0.50),
    ("spectral_only", 0.3333333),
    ("spectral_only", 0.50),
    ("spectral_only", 0.6666667),
    ("spectral_plus_dim", 0.3333333),
    ("spectral_plus_dim", 0.50),
    ("spectral_plus_dim", 0.6666667),
    ("random_baseline", 0.50),
]
EPSILONS = [0.00, 0.01, 0.02]


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


def pipeline_rows(policy_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_split_policy: Dict[Tuple[int, str], List[Dict[str, Any]]] = {}
    for row in policy_rows:
        key = (int(row["split_id"]), str(row["policy_name"]))
        by_split_policy.setdefault(key, []).append(dict(row))

    split_ids = sorted({int(r["split_id"]) for r in policy_rows})
    out: List[Dict[str, Any]] = []
    for split_id in split_ids:
        ref_rows = by_split_policy[(split_id, REFERENCE_POLICY)]
        ref = nearest_budget(ref_rows, REFERENCE_BUDGET)
        ref_hit = safe_float(ref["within_target_best_hit"])
        ref_recall = safe_float(ref["within_target_top_quartile_recall"])
        ref_lift = safe_float(ref["within_target_selected_lift"])
        ref_budget = safe_float(ref["budget_frac"])

        for policy_name, budget in CANDIDATE_PIPELINES:
            sub = by_split_policy[(split_id, policy_name)]
            row = nearest_budget(sub, budget)
            hit = safe_float(row["within_target_best_hit"])
            recall = safe_float(row["within_target_top_quartile_recall"])
            lift = safe_float(row["within_target_selected_lift"])
            actual_budget = safe_float(row["budget_frac"])
            selected_rows = safe_float(row["selected_rows"])
            entry: Dict[str, Any] = {
                "split_id": split_id,
                "policy_name": policy_name,
                "budget_frac": actual_budget,
                "selected_rows": selected_rows,
                "saved_followups_vs_all_frac": 1.0 - actual_budget,
                "saved_followups_vs_reference_frac": ref_budget - actual_budget,
                "within_target_best_hit": hit,
                "within_target_top_quartile_recall": recall,
                "within_target_selected_lift": lift,
                "ref_best_hit": ref_hit,
                "ref_top_quartile_recall": ref_recall,
                "ref_selected_lift": ref_lift,
                "delta_best_hit_vs_ref": hit - ref_hit,
                "delta_top_quartile_recall_vs_ref": recall - ref_recall,
                "delta_selected_lift_vs_ref": lift - ref_lift,
            }
            for eps in EPSILONS:
                suffix = f"{int(round(eps * 100)):02d}"
                entry[f"match_hit_eps_{suffix}"] = 1 if hit >= ref_hit - eps else 0
                entry[f"match_recall_eps_{suffix}"] = 1 if recall >= ref_recall - eps else 0
                entry[f"match_joint_eps_{suffix}"] = 1 if (hit >= ref_hit - eps and recall >= ref_recall - eps) else 0
            out.append(entry)
    return out


def pipeline_summary(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    keys = sorted({(str(r["policy_name"]), safe_float(r["budget_frac"])) for r in rows})
    out: List[Dict[str, Any]] = []
    for policy_name, budget in keys:
        sub = [r for r in rows if str(r["policy_name"]) == policy_name and abs(safe_float(r["budget_frac"]) - budget) <= 1e-9]
        entry: Dict[str, Any] = {
            "policy_name": policy_name,
            "budget_frac": budget,
            "mean_saved_followups_vs_all_frac": mean_defined(safe_float(r["saved_followups_vs_all_frac"]) for r in sub),
            "mean_saved_followups_vs_reference_frac": mean_defined(safe_float(r["saved_followups_vs_reference_frac"]) for r in sub),
            "mean_best_hit": mean_defined(safe_float(r["within_target_best_hit"]) for r in sub),
            "mean_top_quartile_recall": mean_defined(safe_float(r["within_target_top_quartile_recall"]) for r in sub),
            "mean_selected_lift": mean_defined(safe_float(r["within_target_selected_lift"]) for r in sub),
            "mean_delta_best_hit_vs_ref": mean_defined(safe_float(r["delta_best_hit_vs_ref"]) for r in sub),
            "mean_delta_top_quartile_recall_vs_ref": mean_defined(safe_float(r["delta_top_quartile_recall_vs_ref"]) for r in sub),
            "mean_delta_selected_lift_vs_ref": mean_defined(safe_float(r["delta_selected_lift_vs_ref"]) for r in sub),
        }
        for eps in EPSILONS:
            suffix = f"{int(round(eps * 100)):02d}"
            entry[f"joint_match_rate_eps_{suffix}"] = mean_defined(safe_float(r[f"match_joint_eps_{suffix}"]) for r in sub)
            entry[f"hit_match_rate_eps_{suffix}"] = mean_defined(safe_float(r[f"match_hit_eps_{suffix}"]) for r in sub)
            entry[f"recall_match_rate_eps_{suffix}"] = mean_defined(safe_float(r[f"match_recall_eps_{suffix}"]) for r in sub)
        out.append(entry)

    def sort_key(row: Dict[str, Any]) -> Tuple[float, float, float]:
        return (
            safe_float(row["joint_match_rate_eps_02"], -1e9),
            safe_float(row["mean_saved_followups_vs_reference_frac"], -1e9),
            safe_float(row["mean_delta_best_hit_vs_ref"], -1e9),
        )

    out.sort(key=sort_key, reverse=True)
    for idx, row in enumerate(out, start=1):
        row["rank"] = idx
    return out


def build_report(summary_rows: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.12g: direkte oppfølgingspipeline etter v12f")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden oversetter v12f til et mer operativt sporsmal: finnes det en kompakt screeningpolicy som faktisk kan erstatte eller naesten erstatte `full_basis@0.50` i en oppfolgingspipeline, og hvor mange dyre oppfolgingskjoringer sparer vi da?"
    )
    lines.append("")
    lines.append("## Referanse")
    lines.append("")
    lines.append(
        f"- Referansepipeline er `{REFERENCE_POLICY}@{REFERENCE_BUDGET:.2f}`. Den er valgt fordi v12f viste at dette er den sterkeste praktiske benchmarken for screening."
    )
    lines.append("- Vi sammenligner kompakte policyer mot denne referansen, ikke bare mot `simulate_all`.")
    lines.append("")
    lines.append("## Hvordan metricene leses")
    lines.append("")
    lines.append("- `mean_saved_followups_vs_all_frac`: andel dyre oppfolgingskjoringer spart mot a simulere alle kandidater.")
    lines.append("- `mean_saved_followups_vs_reference_frac`: ekstra spart andel mot referansepipeline. Positiv verdi betyr billigere enn `full_basis@0.50`.")
    lines.append("- `joint_match_rate_eps_00`: andel split der policyen matcher eller slar referansen pa baade `within_target_best_hit` og `within_target_top_quartile_recall` uten toleranse.")
    lines.append("- `joint_match_rate_eps_02`: samme, men med `0.02` absolutt toleranse. Dette er den mest praktiske naer-match-metrikken her.")
    lines.append("")
    lines.append("## Pipeline-sammendrag")
    lines.append("")
    lines.append("| rank | policy | budget | save_vs_all | save_vs_ref | best_hit | recall | d_best_hit_vs_ref | d_recall_vs_ref | match_exact | match_eps_02 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in summary_rows:
        lines.append(
            f"| {int(row['rank'])} | {row['policy_name']} | {safe_float(row['budget_frac']):.3f} | "
            f"{safe_float(row['mean_saved_followups_vs_all_frac']):.3f} | {safe_float(row['mean_saved_followups_vs_reference_frac']):.3f} | "
            f"{safe_float(row['mean_best_hit']):.3f} | {safe_float(row['mean_top_quartile_recall']):.3f} | "
            f"{safe_float(row['mean_delta_best_hit_vs_ref']):.3f} | {safe_float(row['mean_delta_top_quartile_recall_vs_ref']):.3f} | "
            f"{safe_float(row['joint_match_rate_eps_00']):.3f} | {safe_float(row['joint_match_rate_eps_02']):.3f} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    ref = next((r for r in summary_rows if str(r["policy_name"]) == REFERENCE_POLICY and abs(safe_float(r["budget_frac"]) - REFERENCE_BUDGET) <= 1e-9), None)
    compact_same = next((r for r in summary_rows if str(r["policy_name"]) == "spectral_only" and abs(safe_float(r["budget_frac"]) - 0.50) <= 1e-9), None)
    compact_cheaper = next((r for r in summary_rows if str(r["policy_name"]) == "spectral_only" and abs(safe_float(r["budget_frac"]) - 0.3333333) <= 1e-6), None)
    compact_heavier = next((r for r in summary_rows if str(r["policy_name"]) == "spectral_only" and abs(safe_float(r["budget_frac"]) - 0.6666667) <= 1e-6), None)
    if ref is not None:
        lines.append(
            f"- Referansen `{REFERENCE_POLICY}@{REFERENCE_BUDGET:.2f}` holder `best_hit={safe_float(ref['mean_best_hit']):.3f}` og `recall={safe_float(ref['mean_top_quartile_recall']):.3f}`."
        )
    if compact_same is not None:
        lines.append(
            f"- `spectral_only@0.50` er den naermeste kompakte erstatningen: `d_best_hit_vs_ref={safe_float(compact_same['mean_delta_best_hit_vs_ref']):.3f}`, `d_recall_vs_ref={safe_float(compact_same['mean_delta_top_quartile_recall_vs_ref']):.3f}`, men `save_vs_ref=0.000`."
        )
    if compact_cheaper is not None:
        lines.append(
            f"- `spectral_only@0.333` gir faktisk ekstra sparing (`save_vs_ref={safe_float(compact_cheaper['mean_saved_followups_vs_reference_frac']):.3f}`), men taper tydelig mot referansen pa bade hit og recall."
        )
    if compact_heavier is not None:
        lines.append(
            f"- `spectral_only@0.667` matcher referansen lettere, men koster mer (`save_vs_ref={safe_float(compact_heavier['mean_saved_followups_vs_reference_frac']):.3f}`)."
        )
    lines.append(
        "- Derfor stotter repoet forelopig ikke en kompakt policy som gir klar ekstra budsjettgevinst mot `full_basis@0.50` ved omtrent samme kvalitet. Det vi har er en enkel same-budget-substitutt, ikke en klar billigere vinner."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def build_lay_summary(summary_rows: Sequence[Dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# v0.12g for ikke-spesialister",
            "",
            "Denne runden sjekker om en enkel geometriregel faktisk kan erstatte den sterkeste screeningmetoden uten at vi mister for mye kvalitet.",
            "",
            "- Svaret akkurat na er: ikke helt.",
            "- `spectral_only` er den beste enkle regelen, men den gir ikke en klar ekstra budsjettgevinst mot `full_basis@0.50`.",
            "",
        ]
    )


def build_recommendation(summary_rows: Sequence[Dict[str, Any]]) -> str:
    lines = ["# v0.12g operativ anbefaling", ""]
    lines.append(
        "Behold `full_basis@0.50` som praktisk screeningbenchmark. Repoet stotter ennå ikke at en kompakt policy er klart billigere ved omtrent samme kvalitet."
    )
    lines.append(
        "Behold `spectral_only@0.50` som den enkleste naermatch-kandidaten. Den er interessant fordi den ligger naert referansen pa samme budsjett, ikke fordi den forelopig gir ekstra besparelse."
    )
    lines.append(
        "Det riktige neste steget er derfor ikke ny frontier-tuning, men en enda mer direkte arbeidsflyt-test: bruk `spectral_only@0.50` til a foresla kandidater, sammenlign den mot `full_basis@0.50`, og maal faktiske oppfolgingskjoringer, ikke bare offline match-rater."
    )
    lines.append("")
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="v0.12g direct follow-up pipeline")
    ap.add_argument("--policy-rows-csv", default="Documentation/v12f_budget_policy_rows.csv")
    ap.add_argument("--output-prefix", default="Documentation/v12g_followup_pipeline")
    ap.add_argument("--report-md", default="Documentation/v12g_followup_budget_pipeline.md")
    ap.add_argument("--lay-md", default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_12g.md")
    ap.add_argument("--recommendation-md", default="Documentation/v0_12g_operativ_anbefaling.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    policy_rows = read_csv(args.policy_rows_csv)
    split_rows = pipeline_rows(policy_rows)
    summary_rows = pipeline_summary(split_rows)

    prefix = args.output_prefix
    write_csv(f"{prefix}_split_rows.csv", split_rows)
    write_csv(f"{prefix}_summary.csv", summary_rows)

    for path, content in [
        (args.report_md, build_report(summary_rows)),
        (args.lay_md, build_lay_summary(summary_rows)),
        (args.recommendation_md, build_recommendation(summary_rows)),
    ]:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
