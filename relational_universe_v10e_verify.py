#!/usr/bin/env python3
"""Verification helpers for v0.10e focused-band outputs."""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple


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


def verify_base_separation(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    expected = [48, 96, 192, 256]
    got = [int(r["target_nodes"]) for r in rows]
    separated = all(int(r["separated_from_prev"]) == 1 for r in rows)
    return {"ok": got == expected and separated, "targets": got, "separated": separated}


def verify_top_candidate(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    ordered = sorted(rows, key=lambda r: safe_float(r["mean_composite"]), reverse=True)
    top = str(ordered[0]["candidate_name"]) if ordered else ""
    return {"ok": top != "band_best", "top_mean_composite": top}


def verify_pairwise(rows: List[Dict[str, Any]], tol: float = 0.03) -> Dict[str, Any]:
    lookup = {(str(r["candidate_a"]), str(r["candidate_b"])): safe_float(r["prob_a_gt_b_mean_composite"]) for r in rows}
    failures: List[Tuple[str, str, float]] = []
    for (a, b), pab in lookup.items():
        if (b, a) not in lookup:
            failures.append((a, b, float("nan")))
            continue
        pba = lookup[(b, a)]
        if math.isfinite(pab) and math.isfinite(pba) and abs((pab + pba) - 1.0) > tol:
            failures.append((a, b, (pab + pba) - 1.0))
    return {"ok": not failures, "failures": failures}


def verify_focused_score(rows: List[Dict[str, Any]], tol: float = 1e-9) -> Dict[str, Any]:
    failures: List[str] = []
    for row in rows:
        parts = [
            safe_float(row["score_ci_low_mean_composite"]),
            safe_float(row["score_alpha_large"]),
            safe_float(row["score_abs_alpha_jump"]),
            safe_float(row["score_linear_margin"]),
            safe_float(row["score_quasi_large"]),
        ]
        expected = sum(parts) / len(parts)
        actual = safe_float(row["focused_score"])
        if abs(expected - actual) > tol:
            failures.append(str(row["candidate_name"]))
    return {"ok": not failures, "failures": failures}


def build_markdown(report: Dict[str, Any]) -> str:
    lines = [
        "# v0.10e verifikasjon og regresjon",
        "",
        f"- base-separasjon: {'ok' if report['base_separation']['ok'] else 'FEIL'}",
        f"- toppkandidat på mean composite: {report['top_candidate']['top_mean_composite']}",
        f"- pairwise-konsistens: {'ok' if report['pairwise']['ok'] else 'FEIL'}",
        f"- focused_score-regenerering: {'ok' if report['focused_score']['ok'] else 'FEIL'}",
        "",
        "## Røde flagg",
        "",
        "- hvis startnivåene ikke lenger er separerte, faller grunnlaget for v0.10e sammen metodisk",
        "- hvis `band_best` plutselig er topprangert på `mean_composite`, er det et signal om at enten dataene eller fortolkningen har flyttet seg",
        "- hvis pairwise-tabellen ikke summerer til omtrent 1 i begge retninger, er bootstrap-sammendraget ikke konsistent",
        "- hvis `focused_score` ikke kan regenereres fra delscore-feltene, er kandidat-CSV-en ikke selvkonsistent",
        "",
    ]
    return "\n".join(lines)


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Verify v0.10e focused-band outputs")
    ap.add_argument("--base-summary", default="Documentation/v10e_focused_band_base_summary.csv")
    ap.add_argument("--candidate-summary", default="Documentation/v10e_focused_band_candidate_summary.csv")
    ap.add_argument("--pairwise", default="Documentation/v10e_focused_band_pairwise.csv")
    ap.add_argument("--report-md", default="Documentation/v10e_verification_report.md")
    ap.add_argument("--json-out", default="Documentation/v10e_verification_report.json")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    report = {
        "base_separation": verify_base_separation(load_rows(args.base_summary)),
        "top_candidate": verify_top_candidate(load_rows(args.candidate_summary)),
        "pairwise": verify_pairwise(load_rows(args.pairwise)),
        "focused_score": verify_focused_score(load_rows(args.candidate_summary)),
    }
    report_path = Path(args.report_md)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_markdown(report), encoding="utf-8")
    json_path = Path(args.json_out)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
