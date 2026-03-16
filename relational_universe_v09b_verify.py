#!/usr/bin/env python3
"""Verification helpers for v0.9b asymptotic outputs."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Sequence


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


def formula_checks(candidate_rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    jump_fail = []
    margin_fail = []
    for row in candidate_rows:
        alpha_large = safe_float(row.get("alpha_large"))
        alpha_all = safe_float(row.get("alpha_all"))
        alpha_jump = safe_float(row.get("alpha_jump"))
        if math.isfinite(alpha_large) and math.isfinite(alpha_all) and math.isfinite(alpha_jump):
            if abs(alpha_jump - (alpha_large - alpha_all)) > 1e-6:
                jump_fail.append(str(row["candidate_name"]))
        rmse_linear = safe_float(row.get("rmse_linear"))
        rmse_log = safe_float(row.get("rmse_log"))
        rmse_sqrt = safe_float(row.get("rmse_sqrt"))
        linear_margin = safe_float(row.get("linear_margin"))
        if all(math.isfinite(v) for v in [rmse_linear, rmse_log, rmse_sqrt, linear_margin]):
            expected = rmse_linear - min(rmse_log, rmse_sqrt)
            if abs(linear_margin - expected) > 1e-6:
                margin_fail.append(str(row["candidate_name"]))
    return {"ok": not jump_fail and not margin_fail, "alpha_jump_failures": jump_fail, "linear_margin_failures": margin_fail}


def ranking_check(candidate_rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    scores = [safe_float(row.get("asymptotic_score"), -1.0) for row in candidate_rows]
    return {"ok": all(a >= b - 1e-12 for a, b in zip(scores, scores[1:])), "best_candidate": str(candidate_rows[0]["candidate_name"]) if candidate_rows else ""}


def size_profile_check(size_rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    counts: Dict[str, int] = {}
    for row in size_rows:
        counts[str(row["candidate_name"])] = counts.get(str(row["candidate_name"]), 0) + 1
    ok = bool(counts) and all(count >= 4 for count in counts.values())
    return {"ok": ok, "counts": counts}


def missing_data_check() -> Dict[str, Any]:
    return {"ok": True, "note": "Handled in regression tests via explicit empty/short input checks."}


def build_summary(candidate_rows: Sequence[Dict[str, Any]], size_rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "candidate_columns": column_check(candidate_rows, {"candidate_name", "alpha_all", "alpha_large", "alpha_jump", "linear_margin", "asymptotic_score"}),
        "size_profile_columns": column_check(size_rows, {"candidate_name", "target_nodes", "mean_initial_nodes", "mean_radius"}),
        "formulas": formula_checks(candidate_rows),
        "ranking": ranking_check(candidate_rows),
        "size_profiles": size_profile_check(size_rows),
        "missing_data": missing_data_check(),
    }


def make_report(summary: Dict[str, Any]) -> str:
    lines = [
        "# v0.9b verifikasjon",
        "",
        f"- Kandidatkolonner: {'pass' if summary['candidate_columns']['ok'] else 'FAIL'}",
        f"- Størrelseprofilkolonner: {'pass' if summary['size_profile_columns']['ok'] else 'FAIL'}",
        f"- Formelkontroller: {'pass' if summary['formulas']['ok'] else 'FAIL'}",
        f"- Rangering: {'pass' if summary['ranking']['ok'] else 'FAIL'}",
        f"- Størrelseprofiler: {'pass' if summary['size_profiles']['ok'] else 'FAIL'}",
        "",
        f"Beste kandidat i denne filen er `{summary['ranking']['best_candidate']}`.",
        "",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify v0.9b asymptotic outputs.")
    parser.add_argument("--candidate-csv", default="Documentation/v09b_asymptotic_candidate_summary.csv")
    parser.add_argument("--size-profile-csv", default="Documentation/v09b_asymptotic_size_profiles.csv")
    parser.add_argument("--report-md", default="Documentation/v09b_verification_report.md")
    parser.add_argument("--json-out", default="Documentation/v09b_verification_report.json")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    candidate_rows = load_rows(args.candidate_csv)
    size_rows = load_rows(args.size_profile_csv)
    summary = build_summary(candidate_rows, size_rows)
    Path(args.report_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_md).write_text(make_report(summary), encoding="utf-8")
    Path(args.json_out).write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    main()
