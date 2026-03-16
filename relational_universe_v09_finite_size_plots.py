#!/usr/bin/env python3
"""Finite-size plotting helpers for relational-universe v0.9 outputs."""

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


def candidate_names(rows: Sequence[Dict[str, Any]]) -> List[str]:
    return sorted({str(row["candidate_name"]) for row in rows})


def subset(rows: Sequence[Dict[str, Any]], candidate: str) -> List[Dict[str, Any]]:
    out = [row for row in rows if str(row["candidate_name"]) == candidate]
    return sorted(out, key=lambda row: (safe_float(row.get("mean_initial_nodes")), str(row.get("burnin_label"))))


def add_candidate_lines(
    ax: plt.Axes,
    rows: Sequence[Dict[str, Any]],
    *,
    x_key: str,
    y_key: str,
    log_x: bool = False,
    log_y: bool = False,
) -> None:
    for name in candidate_names(rows):
        sub = subset(rows, name)
        xs = [safe_float(row.get(x_key)) for row in sub]
        ys = [safe_float(row.get(y_key)) for row in sub]
        burnins = [str(row.get("burnin_label")) for row in sub]
        ax.plot(xs, ys, marker="o", label=name)
        for x, y, burn in zip(xs, ys, burnins):
            ax.annotate(burn, (x, y), textcoords="offset points", xytext=(3, 3), fontsize=7)
    if log_x:
        ax.set_xscale("log")
    if log_y:
        ax.set_yscale("log")
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=8)


def save_composite_plot(group_rows: Sequence[Dict[str, Any]], out_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7, 5))
    add_candidate_lines(ax, group_rows, x_key="mean_initial_nodes", y_key="composite_score")
    ax.set_title("Composite score vs initial size")
    ax.set_xlabel("mean_initial_nodes")
    ax.set_ylabel("composite_score")
    fig.tight_layout()
    path = out_dir / "v09_composite_vs_size.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def save_radius_linear(group_rows: Sequence[Dict[str, Any]], out_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(7, 5))
    add_candidate_lines(ax, group_rows, x_key="mean_initial_nodes", y_key="mean_final_radius_control")
    ax.set_title("Radius vs initial size")
    ax.set_xlabel("mean_initial_nodes")
    ax.set_ylabel("mean_final_radius_control")
    fig.tight_layout()
    path = out_dir / "v09_radius_vs_size_linear.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def save_radius_loglog(group_rows: Sequence[Dict[str, Any]], out_dir: Path) -> Path:
    shifted = []
    for row in group_rows:
        shifted.append(dict(row, radius_plus_one=safe_float(row.get("mean_final_radius_control")) + 1.0))
    fig, ax = plt.subplots(figsize=(7, 5))
    add_candidate_lines(ax, shifted, x_key="mean_initial_nodes", y_key="radius_plus_one", log_x=True, log_y=True)
    ax.set_title("Radius vs initial size (log-log)")
    ax.set_xlabel("mean_initial_nodes")
    ax.set_ylabel("mean_final_radius_control + 1")
    fig.tight_layout()
    path = out_dir / "v09_radius_vs_size_loglog.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def save_overlap_logsize(group_rows: Sequence[Dict[str, Any]], out_dir: Path) -> Path:
    transformed = []
    for row in group_rows:
        transformed.append(dict(row, log_initial_nodes=math.log(max(2.0, safe_float(row.get("mean_initial_nodes"))))))
    fig, ax = plt.subplots(figsize=(7, 5))
    add_candidate_lines(ax, transformed, x_key="log_initial_nodes", y_key="mean_avg_local_overlap")
    ax.set_title("Overlap vs log(initial size)")
    ax.set_xlabel("log(mean_initial_nodes)")
    ax.set_ylabel("mean_avg_local_overlap")
    fig.tight_layout()
    path = out_dir / "v09_overlap_vs_logsize.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def save_quasi_logsize(group_rows: Sequence[Dict[str, Any]], out_dir: Path) -> Path:
    transformed = []
    for row in group_rows:
        transformed.append(dict(row, log_initial_nodes=math.log(max(2.0, safe_float(row.get("mean_initial_nodes"))))))
    fig, ax = plt.subplots(figsize=(7, 5))
    add_candidate_lines(ax, transformed, x_key="log_initial_nodes", y_key="quasi_score")
    ax.set_title("Quasi score vs log(initial size)")
    ax.set_xlabel("log(mean_initial_nodes)")
    ax.set_ylabel("quasi_score")
    fig.tight_layout()
    path = out_dir / "v09_quasi_vs_logsize.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def make_report(candidate_rows: Sequence[Dict[str, Any]], paths: Sequence[Path]) -> str:
    best = candidate_rows[0] if candidate_rows else None
    lines = [
        "# v0.9 finite-size plottingrapport",
        "",
        "## Figurene",
        "",
        "- `v09_composite_vs_size.png`: viser om composite-score holder seg oppe eller kollapser når de naturlige starttilstandene blir større.",
        "- `v09_radius_vs_size_linear.png`: viser rå radiusvekst uten skaletransformasjon.",
        "- `v09_radius_vs_size_loglog.png`: er den relevante figuren for sublineær skadeutbredelse, fordi en svakere enn lineær log-log-helning støtter ideen om begrenset frontvekst.",
        "- `v09_overlap_vs_logsize.png`: viser om repair/overlap holder seg stabilt eller synker med størrelse.",
        "- `v09_quasi_vs_logsize.png`: viser om quasi-score forvitrer med log-størrelse.",
        "",
        "## Kort tolkning per figur",
        "",
    ]
    if best is not None:
        radius_alpha = safe_float(best.get("radius_alpha"))
        ci_high_alpha = safe_float(best.get("ci_high_radius_alpha"))
        lines.extend(
            [
                f"- Composite-figuren bør leses sammen med kandidatrangeringen. Den nåværende toppkandidaten er `{best['candidate_name']}` med mean composite ≈ {safe_float(best.get('mean_composite')):.3f}.",
                f"- Radius log-log-figuren støtter en tentativ sublineær lesning hvis man fokuserer på toppkandidaten: radius α ≈ {radius_alpha:.3f} og øvre bootstrapgrense ≈ {ci_high_alpha:.3f}. Dette er fortsatt et numerisk hint, ikke et bevis.",
                f"- Overlap-figuren styrker hypotesen bare dersom kurvene ikke faller bratt med størrelse. For toppkandidaten er overlap-slope ≈ {safe_float(best.get('overlap_vs_logN_slope')):.3f}.",
                f"- Quasi-figuren svekker hypotesen hvis quasi-score synker raskt med log-størrelse. For toppkandidaten er quasi-slope ≈ {safe_float(best.get('quasi_vs_logN_slope')):.3f}.",
                "",
            ]
        )
    lines.append("## Filer")
    lines.append("")
    for path in paths:
        lines.append(f"- `{path.name}`")
    lines.append("")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plot finite-size diagnostics for v0.9 outputs.")
    parser.add_argument("--group-csv", default="Documentation/v09_scale_group_rows.csv")
    parser.add_argument("--candidate-csv", default="Documentation/v09_scale_candidate_summary.csv")
    parser.add_argument("--out-dir", default="Documentation/v09_finite_size_plots")
    parser.add_argument("--report-md", default="Documentation/v09_finite_size_plots.md")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    out_dir = ensure_dir(args.out_dir)
    group_rows = load_rows(args.group_csv)
    candidate_rows = load_rows(args.candidate_csv)
    paths = [
        save_composite_plot(group_rows, out_dir),
        save_radius_linear(group_rows, out_dir),
        save_radius_loglog(group_rows, out_dir),
        save_overlap_logsize(group_rows, out_dir),
        save_quasi_logsize(group_rows, out_dir),
    ]
    Path(args.report_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report_md).write_text(make_report(candidate_rows, paths), encoding="utf-8")


if __name__ == "__main__":
    main()
