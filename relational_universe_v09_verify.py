#!/usr/bin/env python3
"""Verification helpers for relational-universe v0.9 outputs."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Sequence


RUN_REQUIRED_COLUMNS = {
    "candidate_name",
    "ensemble",
    "burnin_label",
    "target_nodes",
    "seed",
    "steps",
    "final_radius_control",
    "avg_local_overlap",
    "initial_nodes",
}

GROUP_REQUIRED_COLUMNS = {
    "candidate_name",
    "ensemble",
    "burnin_label",
    "target_nodes",
    "mean_initial_nodes",
    "composite_score",
    "repair_score",
    "causal_score",
    "quasi_score",
    "geom_score",
}

CANDIDATE_REQUIRED_COLUMNS = {
    "candidate_name",
    "mean_composite",
    "ci_low_mean_composite",
    "radius_alpha",
    "overlap_vs_logN_slope",
    "quasi_vs_logN_slope",
    "burnin_sensitivity",
}


def safe_float(value: Any, default: float = float("nan")) -> float:
    try:
        out = float(value)
    except Exception:
        return default
    if math.isnan(out) or math.isinf(out):
        return default
    return out


def load_rows(path: str | Path) -> List[Dict[str, Any]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def column_check(rows: Sequence[Dict[str, Any]], required: Sequence[str]) -> Dict[str, Any]:
    if not rows:
        return {"ok": False, "missing": sorted(required)}
    present = set(rows[0].keys())
    missing = sorted(set(required) - present)
    return {"ok": not missing, "missing": missing}


def verify_candidate_ranking(candidate_rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    if not candidate_rows:
        return {"ok": False, "reason": "no candidate rows"}
    cis = [safe_float(row["ci_low_mean_composite"], -1.0) for row in candidate_rows]
    nonincreasing = all(a >= b - 1e-12 for a, b in zip(cis, cis[1:]))
    best = candidate_rows[0]
    return {
        "ok": nonincreasing,
        "best_candidate": str(best["candidate_name"]),
        "best_ci_low": safe_float(best["ci_low_mean_composite"]),
    }


def verify_group_coverage(group_rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    pairs = {(str(row["candidate_name"]), str(row["ensemble"])) for row in group_rows}
    burnins = {str(row["burnin_label"]) for row in group_rows}
    targets = sorted({int(round(safe_float(row["target_nodes"], 0.0))) for row in group_rows})
    ok = "light" in burnins and "deep" in burnins and len(targets) >= 3 and len(pairs) == len(group_rows)
    return {"ok": ok, "targets": targets, "burnins": sorted(burnins), "rows": len(group_rows)}


def build_summary(run_rows: Sequence[Dict[str, Any]], group_rows: Sequence[Dict[str, Any]], candidate_rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "run_columns": column_check(run_rows, RUN_REQUIRED_COLUMNS),
        "group_columns": column_check(group_rows, GROUP_REQUIRED_COLUMNS),
        "candidate_columns": column_check(candidate_rows, CANDIDATE_REQUIRED_COLUMNS),
        "candidate_ranking": verify_candidate_ranking(candidate_rows),
        "group_coverage": verify_group_coverage(group_rows),
    }


def make_report(summary: Dict[str, Any]) -> str:
    lines = [
        "# v0.9 verifikasjon",
        "",
        "## Hva som ble sjekket",
        "",
        "- at run-, group- og candidate-CSV-ene har de forventede kolonnene,",
        "- at kandidatfilen faktisk er sortert etter nedre bootstrapgrense på composite,",
        "- at group-rows dekker både `light` og `deep` burn-in og minst tre målstørrelser.",
        "",
        "## Resultat",
        "",
        f"- Run CSV kolonner: {'pass' if summary['run_columns']['ok'] else 'FAIL'}",
        f"- Group CSV kolonner: {'pass' if summary['group_columns']['ok'] else 'FAIL'}",
        f"- Candidate CSV kolonner: {'pass' if summary['candidate_columns']['ok'] else 'FAIL'}",
        f"- Kandidatrangering: {'pass' if summary['candidate_ranking']['ok'] else 'FAIL'}",
        f"- Group coverage: {'pass' if summary['group_coverage']['ok'] else 'FAIL'}",
        "",
        "## Detaljer",
        "",
        f"- Beste kandidat i filen er `{summary['candidate_ranking']['best_candidate']}` med CI low ≈ {summary['candidate_ranking']['best_ci_low']:.3f}.",
        f"- Observerte target-nivåer: {summary['group_coverage']['targets']}",
        f"- Observerte burn-in labels: {summary['group_coverage']['burnins']}",
        "",
        "Merk at denne verifikasjonen er en output-kontroll. De egentlige regresjonstestene ligger i en egen testfil.",
        "",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify v0.9 CSV outputs and summarize health.")
    parser.add_argument("--run-csv", default="Documentation/v09_scale_run_rows.csv")
    parser.add_argument("--group-csv", default="Documentation/v09_scale_group_rows.csv")
    parser.add_argument("--candidate-csv", default="Documentation/v09_scale_candidate_summary.csv")
    parser.add_argument("--report-md", default="Documentation/v09_verification_report.md")
    parser.add_argument("--json-out", default="Documentation/v09_verification_report.json")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_rows = load_rows(args.run_csv)
    group_rows = load_rows(args.group_csv)
    candidate_rows = load_rows(args.candidate_csv)
    summary = build_summary(run_rows, group_rows, candidate_rows)
    Path(args.report_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_md).write_text(make_report(summary), encoding="utf-8")
    Path(args.json_out).write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    main()
