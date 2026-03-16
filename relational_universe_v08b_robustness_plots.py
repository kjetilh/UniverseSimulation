#!/usr/bin/env python3
"""Plotting helpers for the relational-universe v0.8b natural-ensemble scan."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np


def safe_float(value: Any, default: float = float("nan")) -> float:
    try:
        out = float(value)
    except Exception:
        return default
    if math.isnan(out) or math.isinf(out):
        return default
    return out


def ensure_dir(path: str | Path) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


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


def finite(values: Iterable[float]) -> List[float]:
    return [float(v) for v in values if math.isfinite(float(v))]


def unique_sorted(rows: Sequence[Dict[str, Any]], key: str) -> List[float]:
    return sorted({safe_float(row.get(key)) for row in rows if math.isfinite(safe_float(row.get(key)))})


def heatmap_matrix(rows: Sequence[Dict[str, Any]], *, x_key: str, y_key: str, value_key: str) -> Tuple[np.ndarray, List[float], List[float]]:
    x_vals = unique_sorted(rows, x_key)
    y_vals = unique_sorted(rows, y_key)
    grid = np.full((len(y_vals), len(x_vals)), np.nan, dtype=float)
    x_index = {value: idx for idx, value in enumerate(x_vals)}
    y_index = {value: idx for idx, value in enumerate(y_vals)}
    for row in rows:
        x = safe_float(row.get(x_key))
        y = safe_float(row.get(y_key))
        val = safe_float(row.get(value_key))
        if math.isfinite(x) and math.isfinite(y) and math.isfinite(val):
            grid[y_index[y], x_index[x]] = val
    return grid, x_vals, y_vals


def save_heatmaps(overall_rows: Sequence[Dict[str, Any]], out_dir: Path) -> List[Path]:
    outputs: List[Path] = []
    slices = sorted(
        {
            (
                safe_float(row.get("r_death")),
                safe_float(row.get("p_swap")),
                safe_float(row.get("p_triad")),
            )
            for row in overall_rows
        }
    )
    for r_death, p_swap, p_triad in slices:
        rows = [
            row for row in overall_rows
            if abs(safe_float(row.get("r_death")) - r_death) < 1e-12
            and abs(safe_float(row.get("p_swap")) - p_swap) < 1e-12
            and abs(safe_float(row.get("p_triad")) - p_triad) < 1e-12
        ]
        if not rows:
            continue
        matrix, x_vals, y_vals = heatmap_matrix(rows, x_key="r_birth", y_key="p_del", value_key="mean_composite_natural")
        fig, ax = plt.subplots(figsize=(max(5, len(x_vals) * 1.2), max(4, len(y_vals) * 0.9)))
        im = ax.imshow(matrix, aspect="auto", origin="lower")
        ax.set_title(
            f"Natural mean composite\nr_death={r_death:.2f}, p_swap={p_swap:.2f}, p_triad={p_triad:.2f}"
        )
        ax.set_xlabel("r_birth")
        ax.set_ylabel("p_del")
        ax.set_xticks(range(len(x_vals)))
        ax.set_xticklabels([f"{x:.2f}" for x in x_vals])
        ax.set_yticks(range(len(y_vals)))
        ax.set_yticklabels([f"{y:.2f}" for y in y_vals])
        for i in range(len(y_vals)):
            for j in range(len(x_vals)):
                value = matrix[i, j]
                if math.isfinite(value):
                    ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=8)
        fig.colorbar(im, ax=ax, label="mean_composite_natural")
        fig.tight_layout()
        out_path = out_dir / f"v08b_heatmap_rd{r_death:.2f}_ps{p_swap:.2f}_pt{p_triad:.2f}.png"
        fig.savefig(out_path, dpi=180)
        plt.close(fig)
        outputs.append(out_path)
    return outputs


def save_errorbar_plot(overall_rows: Sequence[Dict[str, Any]], out_dir: Path) -> Path:
    ranked = sorted(
        overall_rows,
        key=lambda row: (
            safe_float(row.get("ci_low_mean_composite_natural"), -1.0),
            safe_float(row.get("mean_composite_natural"), -1.0),
        ),
        reverse=True,
    )
    labels = [
        f"rb={safe_float(r['r_birth']):.2f}\nrd={safe_float(r['r_death']):.2f}\npd={safe_float(r['p_del']):.2f}"
        for r in ranked
    ]
    means = [safe_float(r.get("mean_composite_natural")) for r in ranked]
    ci_low = [safe_float(r.get("ci_low_mean_composite_natural")) for r in ranked]
    ci_high = [safe_float(r.get("ci_high_mean_composite_natural")) for r in ranked]
    yerr = np.array([[max(0.0, m - lo) for m, lo in zip(means, ci_low)], [max(0.0, hi - m) for m, hi in zip(means, ci_high)]])

    fig, ax = plt.subplots(figsize=(max(9, len(labels) * 0.5), 5))
    ax.errorbar(range(len(labels)), means, yerr=yerr, fmt="o", capsize=4)
    ax.set_title("Bootstrap intervals for natural mean composite")
    ax.set_xlabel("Candidate")
    ax.set_ylabel("mean_composite_natural")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    out_path = out_dir / "v08b_bootstrap_errorbars.png"
    fig.savefig(out_path, dpi=180)
    plt.close(fig)
    return out_path


def save_initial_size_plot(run_rows: Sequence[Dict[str, Any]], out_dir: Path) -> Path:
    ensembles = sorted({str(row["ensemble"]) for row in run_rows})
    data = [
        finite(safe_float(row.get("initial_nodes")) for row in run_rows if str(row["ensemble"]) == ensemble)
        for ensemble in ensembles
    ]
    fig, ax = plt.subplots(figsize=(max(7, len(ensembles) * 1.4), 5))
    ax.boxplot(data, tick_labels=ensembles, showmeans=True)
    ax.set_title("Initial node-count distributions by ensemble")
    ax.set_ylabel("initial_nodes")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    out_path = out_dir / "v08b_initial_size_distributions.png"
    fig.savefig(out_path, dpi=180)
    plt.close(fig)
    return out_path


def save_overlap_radius_scatter(run_rows: Sequence[Dict[str, Any]], out_dir: Path) -> Path:
    x = [safe_float(row.get("final_radius_control")) for row in run_rows]
    y = [safe_float(row.get("avg_local_overlap")) for row in run_rows]
    color = [safe_float(row.get("p_del"), 0.0) for row in run_rows]
    fig, ax = plt.subplots(figsize=(7, 5))
    sc = ax.scatter(x, y, c=color, cmap="viridis", alpha=0.8)
    ax.set_title("Overlap vs final radius, colored by p_del")
    ax.set_xlabel("final_radius_control")
    ax.set_ylabel("avg_local_overlap")
    ax.grid(True, alpha=0.25)
    fig.colorbar(sc, ax=ax, label="p_del")
    fig.tight_layout()
    out_path = out_dir / "v08b_overlap_vs_radius.png"
    fig.savefig(out_path, dpi=180)
    plt.close(fig)
    return out_path


def make_report_md(
    heatmaps: Sequence[Path],
    errorbar_plot: Path,
    size_plot: Path,
    scatter_plot: Path,
) -> str:
    lines = [
        "# v0.8b plottingrapport",
        "",
        "## Hva figurene viser",
        "",
        "- Heatmaps viser `mean_composite_natural` i slicer der `(r_death, p_swap, p_triad)` holdes fast og aksene er `r_birth` mot `p_del`.",
        "- Errorbar-plottet viser punktestimat og bootstrap-intervall for hver kandidat rangert etter `ci_low_mean_composite_natural`.",
        "- Size-distribution-plottet viser hvor store de ulike startensemblefamiliene faktisk ble målt i `initial_nodes`.",
        "- Scatter-plottet viser koblingen mellom `avg_local_overlap` og `final_radius_control`, med `p_del` som fargekode.",
        "",
        "## Hvordan figurene bør leses",
        "",
        "- Heatmaps er nyttige for å se hvor følsom den naturlige robustheten er for små endringer i `p_del` og `r_birth`.",
        "- Errorbars skiller mellom høye punktestimater og kandidater som også har løftet hele nedre bootstrap-båndet.",
        "- Size-distribution-plottet er en ren ensemblekontroll: her skal de naturlige ensemblefamiliene ligge klart over `toy_cycle8`.",
        "- Scatter-plottet sier ikke hva som er årsak, men det viser om høy overlap typisk sammenfaller med mindre slutt-radius i dette datasettet.",
        "",
        "## Filer",
        "",
    ]
    for path in heatmaps:
        lines.append(f"- `{path.name}`")
    lines.extend(
        [
            f"- `{errorbar_plot.name}`",
            f"- `{size_plot.name}`",
            f"- `{scatter_plot.name}`",
            "",
        ]
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate v0.8b natural-ensemble robustness plots.")
    parser.add_argument("--run-csv", type=str, default="Documentation/v08b_natural_ensemble_runs.csv")
    parser.add_argument("--ensemble-csv", type=str, default="Documentation/v08b_natural_ensemble_aggregate.csv")
    parser.add_argument("--overall-csv", type=str, default="Documentation/v08b_candidate_robustness.csv")
    parser.add_argument("--out-dir", type=str, default="Documentation/v08b_plots")
    parser.add_argument("--report-md", type=str, default="Documentation/v08b_plot_report.md")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_rows = load_rows(args.run_csv)
    _ = load_rows(args.ensemble_csv)
    overall_rows = load_rows(args.overall_csv)
    out_dir = Path(args.out_dir)
    ensure_dir(out_dir)
    Path(args.report_md).parent.mkdir(parents=True, exist_ok=True)

    heatmaps = save_heatmaps(overall_rows, out_dir)
    errorbar_plot = save_errorbar_plot(overall_rows, out_dir)
    size_plot = save_initial_size_plot(run_rows, out_dir)
    scatter_plot = save_overlap_radius_scatter(run_rows, out_dir)

    Path(args.report_md).write_text(
        make_report_md(heatmaps, errorbar_plot, size_plot, scatter_plot),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
