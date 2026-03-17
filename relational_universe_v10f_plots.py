#!/usr/bin/env python3
"""Plot frontier diagnostics for v0.10f."""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, List

import matplotlib.pyplot as plt


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


def ensure_dir(path: str | Path) -> Path:
    out = Path(path)
    out.mkdir(parents=True, exist_ok=True)
    return out


def plot_composite_vs_focused(rows: List[Dict[str, Any]], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.8, 5.0))
    for row in rows:
        x = safe_float(row["mean_composite"])
        y = safe_float(row["focused_score"])
        ax.scatter([x], [y])
        ax.annotate(str(row["candidate_name"]), (x, y), xytext=(4, 4), textcoords="offset points", fontsize=8)
    ax.set_xlabel("Mean composite")
    ax.set_ylabel("Focused score")
    ax.set_title("Broad frontier: composite vs focused score")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_alpha_vs_ci(rows: List[Dict[str, Any]], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.8, 5.0))
    for row in rows:
        x = safe_float(row["alpha_large"])
        y = safe_float(row["ci_low_mean_composite"])
        ax.scatter([x], [y])
        ax.annotate(str(row["candidate_name"]), (x, y), xytext=(4, 4), textcoords="offset points", fontsize=8)
    ax.set_xlabel("alpha_large")
    ax.set_ylabel("CI low mean composite")
    ax.set_title("Broad frontier: asymptotics vs conservative raw score")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_pairwise_heatmap(rows: List[Dict[str, Any]], out_path: Path) -> None:
    names = sorted({str(r["candidate_a"]) for r in rows} | {str(r["candidate_b"]) for r in rows})
    idx = {name: i for i, name in enumerate(names)}
    matrix = [[0.5 for _ in names] for _ in names]
    for row in rows:
        a = str(row["candidate_a"])
        b = str(row["candidate_b"])
        matrix[idx[a]][idx[b]] = safe_float(row["prob_a_gt_b_mean_composite"])
    fig, ax = plt.subplots(figsize=(6.6, 5.8))
    img = ax.imshow(matrix, vmin=0.0, vmax=1.0)
    ax.set_xticks(range(len(names)), names, rotation=25, ha="right")
    ax.set_yticks(range(len(names)), names)
    ax.set_title("Final frontier pairwise heatmap")
    fig.colorbar(img, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_final_profiles(rows: List[Dict[str, Any]], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.8, 5.0))
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row["candidate_name"]), []).append(row)
    for name, sub in sorted(grouped.items()):
        sub = sorted(sub, key=lambda r: int(r["target_nodes"]))
        xs = [int(r["target_nodes"]) for r in sub]
        ys = [safe_float(r["mean_radius"]) for r in sub]
        ax.plot(xs, ys, marker="o", label=name)
    ax.set_xlabel("Target nodes")
    ax.set_ylabel("Mean radius")
    ax.set_title("Final frontier size profiles")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def build_report() -> str:
    return "\n".join([
        "# v0.10f plotting og frontierdiagnostikk",
        "",
        "- `composite_vs_focused.png` viser om råvinner og focused-score-vinner faktisk er samme punkt eller ikke.",
        "- `alpha_vs_ci_low.png` viser kompromisset mellom asymptotisk disiplin og konservativ råscore.",
        "- `final_pairwise_heatmap.png` gjør finalistspenningen synlig som en enkel sannsynlighetsmatrise.",
        "- `final_size_profiles.png` viser om finalistene følger tydelig ulike radiusbaner over 48, 96, 192 og 256.",
        "",
    ])


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Plot frontier diagnostics for v0.10f")
    ap.add_argument("--broad-candidates", default="Documentation/v10f_frontier_broad_candidate_summary.csv")
    ap.add_argument("--final-candidates", default="Documentation/v10f_frontier_final_candidate_summary.csv")
    ap.add_argument("--final-pairwise", default="Documentation/v10f_frontier_final_pairwise.csv")
    ap.add_argument("--final-size-profiles", default="Documentation/v10f_frontier_final_size_profiles.csv")
    ap.add_argument("--out-dir", default="Documentation/v10f_plots")
    ap.add_argument("--report-md", default="Documentation/v10f_plot_report.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    out_dir = ensure_dir(args.out_dir)
    broad = load_rows(args.broad_candidates)
    final = load_rows(args.final_candidates)
    pairwise = load_rows(args.final_pairwise)
    profiles = load_rows(args.final_size_profiles)

    plot_composite_vs_focused(broad, out_dir / "composite_vs_focused.png")
    plot_alpha_vs_ci(broad, out_dir / "alpha_vs_ci_low.png")
    plot_pairwise_heatmap(pairwise, out_dir / "final_pairwise_heatmap.png")
    plot_final_profiles(profiles, out_dir / "final_size_profiles.png")

    report_path = Path(args.report_md)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_report(), encoding="utf-8")


if __name__ == "__main__":
    main()
