#!/usr/bin/env python3
"""Verification helpers for v0.10f frontier outputs."""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, List


def safe_float(x: Any, default: float = float("nan")) -> float:
    try:
        y = float(x)
    except Exception:
        return default
    if math.isnan(y) or math.isinf(y):
        return default
    return y


def load_rows(path: str | Path) -> List[Dict[str, Any]]:
    with Path(path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def verify_base_levels(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    expected = [48, 96, 192, 256]
    got = [int(r["target_nodes"]) for r in rows]
    separated = all(int(r["separated_from_prev"]) == 1 for r in rows)
    exact = all(safe_float(r["mean_initial_nodes"]) == int(r["target_nodes"]) for r in rows)
    return {"ok": got == expected and separated and exact, "targets": got, "separated": separated, "exact": exact}


def verify_frontier_order(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_name = {str(r["candidate_name"]): r for r in rows}
    failures: List[str] = []
    if "band_small_triad" in by_name and "band_zero_del" in by_name:
        if safe_float(by_name["band_small_triad"]["mean_composite"]) >= safe_float(by_name["band_zero_del"]["mean_composite"]):
            failures.append("band_small_triad should be below band_zero_del on mean_composite")
    if "frontier_diag_mid" in by_name:
        if safe_float(by_name["frontier_diag_mid"]["focused_score"]) <= safe_float(by_name["band_zero_del"]["focused_score"]):
            failures.append("frontier_diag_mid should be above band_zero_del on focused_score")
        if safe_float(by_name["band_zero_del"]["top_prob_mean_composite"]) <= safe_float(by_name["frontier_diag_mid"]["top_prob_mean_composite"]):
            failures.append("band_zero_del should be above frontier_diag_mid on top_prob_mean_composite")
    elif "frontier_triad_only" in by_name:
        if safe_float(by_name["frontier_triad_only"]["focused_score"]) <= safe_float(by_name["band_zero_del"]["focused_score"]):
            failures.append("frontier_triad_only should be above band_zero_del on focused_score")
        if safe_float(by_name["band_zero_del"]["top_prob_mean_composite"]) <= safe_float(by_name["frontier_triad_only"]["top_prob_mean_composite"]):
            failures.append("band_zero_del should be above frontier_triad_only on top_prob_mean_composite")
    return {"ok": not failures, "failures": failures}


def verify_report_text(recommendation_md: str | Path) -> Dict[str, Any]:
    text = Path(recommendation_md).read_text(encoding="utf-8")
    bad = "band_small_triad" in text and "operativ" in text.lower()
    return {"ok": not bad}


def build_markdown(report: Dict[str, Any]) -> str:
    return "\n".join([
        "# v0.10f verifikasjon og regresjon",
        "",
        f"- base-nivåer: {'ok' if report['base_levels']['ok'] else 'FEIL'}",
        f"- frontier-orden: {'ok' if report['frontier_order']['ok'] else 'FEIL'}",
        f"- anbefalingstekst uten band_small_triad som operativ front: {'ok' if report['report_text']['ok'] else 'FEIL'}",
        "",
        "## Kritiske regresjoner",
        "",
        "- hvis 48, 96, 192 og 256 ikke lenger er eksakt realiserte, faller v0.10f-frontieren metodisk sammen",
        "- hvis `band_small_triad` igjen behandles som operativ frontkandidat, er v13-dommen brutt",
        "- hvis raw winner og focused-score-winner ikke lenger skilles riktig, mister v0.10f sin viktigste frontier-innsikt",
        "",
    ])


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Verify v0.10f frontier outputs")
    ap.add_argument("--base-summary", default="Documentation/v10f_frontier_base_summary.csv")
    ap.add_argument("--final-candidates", default="Documentation/v10f_frontier_final_candidate_summary.csv")
    ap.add_argument("--recommendation-md", default="Documentation/v0_10f_operativ_anbefaling.md")
    ap.add_argument("--report-md", default="Documentation/v10f_verification_report.md")
    ap.add_argument("--json-out", default="Documentation/v10f_verification_report.json")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    report = {
        "base_levels": verify_base_levels(load_rows(args.base_summary)),
        "frontier_order": verify_frontier_order(load_rows(args.final_candidates)),
        "report_text": verify_report_text(args.recommendation_md),
    }
    md = Path(args.report_md)
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(build_markdown(report), encoding="utf-8")
    js = Path(args.json_out)
    js.parent.mkdir(parents=True, exist_ok=True)
    js.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
