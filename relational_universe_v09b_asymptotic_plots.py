#!/usr/bin/env python3
"""Plotting helpers for relational-universe v0.9b asymptotic refinement."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, List, Sequence

import matplotlib.pyplot as plt


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
        raw = list(csv.DictReader(f))
    rows: List[Dict[str, Any]] = []
    for row in raw:
        parsed: Dict[str, Any] = {}
        for key, value in row.items():
            try:
                parsed[key] = float(value)
            except Exception:
                parsed[key] = value
        rows.append(parsed)
    return rows


def ensure_dir(path: str | Path) -> Path:
    out = Path(path)
    out.mkdir(parents=True, exist_ok=True)
    return out


def save_candidate_overview(rows: Sequence[Dict[str, Any]], out_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7, 5))
    xs = [safe_float(r.get("alpha_large")) for r in rows]
    ys = [safe_float(r.get("ci_low_mean_composite")) for r in rows]
    ax.scatter(xs, ys)
    for row, x, y in zip(rows, xs, ys):
        ax.annotate(str(row["candidate_name"]), (x, y), textcoords="offset points", xytext=(4, 4), fontsize=8)
    ax.set_title("v0.9b candidate overview")
    ax.set_xlabel("alpha_large")
    ax.set_ylabel("ci_low_mean_composite")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    path = out_dir / "v09b_candidate_overview.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def save_artifact_figure(rows: Sequence[Dict[str, Any]], out_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7, 5))
    xs = [safe_float(r.get("alpha_jump")) for r in rows]
    ys = [safe_float(r.get("linear_margin")) for r in rows]
    ax.scatter(xs, ys)
    for row, x, y in zip(rows, xs, ys):
        ax.annotate(str(row["candidate_name"]), (x, y), textcoords="offset points", xytext=(4, 4), fontsize=8)
    ax.axvline(0.0, color="grey", linewidth=1)
    ax.axhline(0.0, color="grey", linewidth=1)
    ax.set_title("Finite-size artifact diagnostics")
    ax.set_xlabel("alpha_jump")
    ax.set_ylabel("linear_margin")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    path = out_dir / "v09b_finite_size_artifacts.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def candidate_profiles(size_rows: Sequence[Dict[str, Any]], candidate_name: str) -> List[Dict[str, Any]]:
    out = [row for row in size_rows if str(row["candidate_name"]) == candidate_name]
    return sorted(out, key=lambda row: safe_float(row.get("mean_initial_nodes")))


def save_radius_profiles(size_rows: Sequence[Dict[str, Any]], out_dir: Path, *, loglog: bool) -> Path:
    fig, ax = plt.subplots(figsize=(7, 5))
    names = sorted({str(row["candidate_name"]) for row in size_rows})
    for name in names:
        sub = candidate_profiles(size_rows, name)
        xs = [safe_float(r.get("mean_initial_nodes")) for r in sub]
        ys = [safe_float(r.get("mean_radius")) for r in sub]
        if loglog:
            ys = [y + 1.0 for y in ys]
        ax.plot(xs, ys, marker="o", label=name)
    if loglog:
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title("Radius profiles (log-log)")
        ax.set_ylabel("mean_radius + 1")
        path = out_dir / "v09b_radius_profiles_loglog.png"
    else:
        ax.set_title("Radius profiles")
        ax.set_ylabel("mean_radius")
        path = out_dir / "v09b_radius_profiles_linear.png"
    ax.set_xlabel("mean_initial_nodes")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def save_focus_figure(size_rows: Sequence[Dict[str, Any]], out_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7, 5))
    for name in ["band_best", "balanced_pdel"]:
        sub = candidate_profiles(size_rows, name)
        if not sub:
            continue
        xs = [safe_float(r.get("mean_initial_nodes")) for r in sub]
        ys = [safe_float(r.get("mean_radius")) for r in sub]
        ax.plot(xs, ys, marker="o", label=name)
    ax.set_title("Focus: band_best vs balanced_pdel")
    ax.set_xlabel("mean_initial_nodes")
    ax.set_ylabel("mean_radius")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    path = out_dir / "v09b_focus_band_best_vs_balanced_pdel.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def save_refinement_figure(main_rows: Sequence[Dict[str, Any]], refined_rows: Sequence[Dict[str, Any]], out_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7, 5))
    main_map = {str(r["candidate_name"]): r for r in main_rows}
    refined_map = {str(r["candidate_name"]): r for r in refined_rows}
    for name in sorted(refined_map):
        if name not in main_map:
            continue
        x0 = safe_float(main_map[name].get("alpha_large"))
        y0 = safe_float(main_map[name].get("ci_low_mean_composite"))
        x1 = safe_float(refined_map[name].get("alpha_large"))
        y1 = safe_float(refined_map[name].get("ci_low_mean_composite"))
        ax.plot([x0, x1], [y0, y1], marker="o")
        ax.annotate(name, (x1, y1), textcoords="offset points", xytext=(4, 4), fontsize=8)
    ax.set_title("Main scan vs local refinement")
    ax.set_xlabel("alpha_large")
    ax.set_ylabel("ci_low_mean_composite")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    path = out_dir / "v09b_refinement_shift.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def make_report(candidate_rows: Sequence[Dict[str, Any]], paths: Sequence[Path]) -> str:
    best = candidate_rows[0] if candidate_rows else None
    lines = [
        "# v0.9b plotting og asymptotikk",
        "",
        "## Hvordan figurene skal leses",
        "",
        "- Kandidatoversikten viser kompromisset mellom lav `alpha_large` og høy nedre composite-grense.",
        "- Finite-size-artefakt-figuren viser om en kandidat har høy `alpha_jump` og dårlig `linear_margin`; det er nettopp der finite-size-risikoen blir synlig.",
        "- Radiusprofilene viser de rå størrelsesbanene som asymptotikk-fitene bygger på.",
        "- Fokusfiguren sammenligner `band_best` og `balanced_pdel` direkte, siden dette er den sentrale rangreverseringen i v0.9b.",
        "- Refineringsfiguren viser om lokal ekstra ensemble-varians flytter toppkandidatene mye eller lite.",
        "",
    ]
    if best is not None:
        lines.append(
            f"Den nåværende asymptotiske vinneren er `{best['candidate_name']}` med `alpha_large` ≈ {safe_float(best['alpha_large']):.3f}, `alpha_jump` ≈ {safe_float(best['alpha_jump']):.3f} og `linear_margin` ≈ {safe_float(best['linear_margin']):.3f}."
        )
        lines.append("")
    lines.append("## Filer")
    lines.append("")
    for path in paths:
        lines.append(f"- `{path.name}`")
    lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plot v0.9b asymptotic diagnostics.")
    parser.add_argument("--candidate-csv", default="Documentation/v09b_asymptotic_candidate_summary.csv")
    parser.add_argument("--size-profile-csv", default="Documentation/v09b_asymptotic_size_profiles.csv")
    parser.add_argument("--refined-csv", default="Documentation/v09b_refined_candidate_summary.csv")
    parser.add_argument("--ensemble-csv", default="Documentation/v09b_ensemble_summary.csv")
    parser.add_argument("--out-dir", default="Documentation/v09b_plots")
    parser.add_argument("--report-md", default="Documentation/v09b_plot_report.md")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    out_dir = ensure_dir(args.out_dir)
    candidate_rows = load_rows(args.candidate_csv)
    size_rows = load_rows(args.size_profile_csv)
    refined_rows = load_rows(args.refined_csv)
    _ = load_rows(args.ensemble_csv)
    paths = [
        save_candidate_overview(candidate_rows, out_dir),
        save_artifact_figure(candidate_rows, out_dir),
        save_radius_profiles(size_rows, out_dir, loglog=False),
        save_radius_profiles(size_rows, out_dir, loglog=True),
        save_focus_figure(size_rows, out_dir),
        save_refinement_figure(candidate_rows, refined_rows, out_dir),
    ]
    Path(args.report_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_md).write_text(make_report(candidate_rows, paths), encoding="utf-8")


if __name__ == "__main__":
    main()
