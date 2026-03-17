#!/usr/bin/env python3
"""Plot focused-band diagnostics for v0.10e."""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, List, Sequence

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


def plot_base_sizes(rows: Sequence[Dict[str, Any]], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    rows = sorted(rows, key=lambda r: int(r["target_nodes"]))
    xs = [int(r["target_nodes"]) for r in rows]
    ys = [safe_float(r["mean_initial_nodes"]) for r in rows]
    lows = [max(0.0, y - safe_float(r["q10_initial_nodes"])) for y, r in zip(ys, rows)]
    highs = [max(0.0, safe_float(r["q90_initial_nodes"]) - y) for y, r in zip(ys, rows)]
    ax.errorbar(xs, ys, yerr=[lows, highs], marker="o", capsize=4)
    ax.plot(xs, xs, linestyle="--", color="black", linewidth=1.0)
    ax.set_xlabel("Nominal target nodes")
    ax.set_ylabel("Realized initial nodes")
    ax.set_title("Realized start sizes per target")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_mean_composite(rows: Sequence[Dict[str, Any]], out_path: Path) -> None:
    ordered = sorted(rows, key=lambda r: safe_float(r["mean_composite"]), reverse=True)
    labels = [str(r["candidate_name"]) for r in ordered]
    vals = [safe_float(r["mean_composite"]) for r in ordered]
    lows = [max(0.0, v - safe_float(r["ci_low_mean_composite"])) for v, r in zip(vals, ordered)]
    highs = [max(0.0, safe_float(r["ci_high_mean_composite"]) - v) for v, r in zip(vals, ordered)]
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    ax.bar(labels, vals, yerr=[lows, highs], capsize=4)
    ax.set_ylabel("Mean composite")
    ax.set_title("Mean composite with bootstrap intervals")
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_focused_score(rows: Sequence[Dict[str, Any]], out_path: Path) -> None:
    ordered = sorted(rows, key=lambda r: safe_float(r["focused_score"]), reverse=True)
    labels = [str(r["candidate_name"]) for r in ordered]
    vals = [safe_float(r["focused_score"]) for r in ordered]
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    ax.bar(labels, vals)
    ax.set_ylabel("Focused score")
    ax.set_title("Focused-score ranking")
    ax.tick_params(axis="x", rotation=20)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_pairwise_heatmap(rows: Sequence[Dict[str, Any]], out_path: Path) -> None:
    names = sorted({str(r["candidate_a"]) for r in rows} | {str(r["candidate_b"]) for r in rows})
    idx = {name: i for i, name in enumerate(names)}
    matrix = [[float("nan") for _ in names] for _ in names]
    for i in range(len(names)):
        matrix[i][i] = 0.5
    for row in rows:
        a = str(row["candidate_a"])
        b = str(row["candidate_b"])
        matrix[idx[a]][idx[b]] = safe_float(row["prob_a_gt_b_mean_composite"])
    fig, ax = plt.subplots(figsize=(6.8, 5.8))
    img = ax.imshow(matrix, vmin=0.0, vmax=1.0)
    ax.set_xticks(range(len(names)), names, rotation=30, ha="right")
    ax.set_yticks(range(len(names)), names)
    ax.set_title("Pairwise P(a > b) heatmap")
    fig.colorbar(img, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_radius_profiles(rows: Sequence[Dict[str, Any]], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(str(row["candidate_name"]), []).append(row)
    for candidate, sub in sorted(grouped.items()):
        sub = sorted(sub, key=lambda r: safe_float(r["mean_initial_nodes"]))
        xs = [safe_float(r["mean_initial_nodes"]) for r in sub]
        ys = [safe_float(r["mean_radius"]) for r in sub]
        ax.plot(xs, ys, marker="o", label=candidate)
    ax.set_xlabel("Realized initial size")
    ax.set_ylabel("Mean radius")
    ax.set_title("Radius profiles by candidate")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def build_report() -> str:
    return "\n".join([
        "# v0.10e plotting og bootstrapdiagnostikk",
        "",
        "- `base_realized_sizes.png` viser at startnivåene faktisk er separerte før vi tolker kandidatforskjeller.",
        "- `mean_composite_bars.png` viser rå composite-rangering med bootstrapintervaller.",
        "- `focused_score_bars.png` viser hvorfor en kandidat kan se best ut under den sammensatte fokus-metrikken selv om rå composite peker et annet sted.",
        "- `pairwise_heatmap.png` viser hvor robuste de parvise seirene faktisk er.",
        "- `radius_profiles.png` viser om kandidatene følger ulike radiusbaner over realiserte størrelser.",
        "",
        "Plottpakken er nyttig nettopp fordi v0.10e ser ut til å splitte dommen mellom `focused_score` og `mean_composite`/pairwise.",
        "",
    ])


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Plot v0.10e focused-band diagnostics")
    ap.add_argument("--base-summary", default="Documentation/v10e_focused_band_base_summary.csv")
    ap.add_argument("--candidate-summary", default="Documentation/v10e_focused_band_candidate_summary.csv")
    ap.add_argument("--pairwise", default="Documentation/v10e_focused_band_pairwise.csv")
    ap.add_argument("--size-profiles", default="Documentation/v10e_focused_band_size_profiles.csv")
    ap.add_argument("--out-dir", default="Documentation/v10e_plots")
    ap.add_argument("--report-md", default="Documentation/v10e_plot_report.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    out_dir = ensure_dir(args.out_dir)
    base_rows = load_rows(args.base_summary)
    candidate_rows = load_rows(args.candidate_summary)
    pair_rows = load_rows(args.pairwise)
    profile_rows = load_rows(args.size_profiles)

    plot_base_sizes(base_rows, out_dir / "base_realized_sizes.png")
    plot_mean_composite(candidate_rows, out_dir / "mean_composite_bars.png")
    plot_focused_score(candidate_rows, out_dir / "focused_score_bars.png")
    plot_pairwise_heatmap(pair_rows, out_dir / "pairwise_heatmap.png")
    plot_radius_profiles(profile_rows, out_dir / "radius_profiles.png")

    report_path = Path(args.report_md)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(build_report(), encoding="utf-8")


if __name__ == "__main__":
    main()
