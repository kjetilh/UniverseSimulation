#!/usr/bin/env python3
"""Plot generator diagnostics for v0.10b-v0.10d."""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

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


def plot_nominal_vs_realized(summary_rows: Sequence[Dict[str, Any]], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    grouped: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for row in summary_rows:
        grouped.setdefault((str(row["method"]), str(row["burnin_label"])), []).append(row)
    for (method, burnin), rows in sorted(grouped.items()):
        rows = sorted(rows, key=lambda r: int(r["target_nodes"]))
        xs = [int(r["target_nodes"]) for r in rows]
        ys = [safe_float(r["mean_realized_nodes"]) for r in rows]
        ax.plot(xs, ys, marker="o", label=f"{method}/{burnin}")
    all_targets = sorted({int(r["target_nodes"]) for r in summary_rows})
    ax.plot(all_targets, all_targets, linestyle="--", color="black", linewidth=1.2, label="ideal")
    ax.set_xlabel("Nominal target nodes")
    ax.set_ylabel("Realized mean nodes")
    ax.set_title("Nominal vs realized size")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_q10_q90(summary_rows: Sequence[Dict[str, Any]], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    chosen = [
        row for row in summary_rows
        if (str(row["method"]), str(row["burnin_label"])) in {("baseline", "deep"), ("adaptive", "deep")}
    ]
    grouped: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for row in chosen:
        grouped.setdefault((str(row["method"]), str(row["burnin_label"])), []).append(row)
    for (method, burnin), rows in sorted(grouped.items()):
        rows = sorted(rows, key=lambda r: int(r["target_nodes"]))
        xs = [int(r["target_nodes"]) for r in rows]
        ys = [safe_float(r["mean_realized_nodes"]) for r in rows]
        lows = [y - safe_float(r["q10_realized_nodes"]) for y, r in zip(ys, rows)]
        highs = [safe_float(r["q90_realized_nodes"]) - y for y, r in zip(ys, rows)]
        ax.errorbar(xs, ys, yerr=[lows, highs], marker="o", capsize=4, label=f"{method}/{burnin}")
    ax.set_xlabel("Nominal target nodes")
    ax.set_ylabel("Realized mean nodes with q10-q90")
    ax.set_title("Realized size bands")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_growth_regimes(overall_rows: Sequence[Dict[str, Any]], out_path: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.2))
    rows = list(overall_rows)
    labels = [str(r["regime"]) for r in rows]
    xs = range(len(rows))
    metrics = [
        ("mean_abs_rel_size_error", "Size error", True),
        ("mean_hit_rate", "Hit rate", False),
        ("mean_naturalness_score", "Naturalness", False),
    ]
    for ax, (key, title, invert) in zip(axes, metrics):
        vals = [safe_float(r[key]) for r in rows]
        ax.bar(list(xs), vals)
        ax.set_xticks(list(xs), labels, rotation=20)
        ax.set_title(title)
        if invert:
            ax.invert_yaxis()
        ax.grid(axis="y", alpha=0.25)
    fig.suptitle("Growth regime comparison")
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_size_profiles(size_rows: Sequence[Dict[str, Any]], out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 5.2))
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for row in size_rows:
        grouped.setdefault(str(row["candidate_name"]), []).append(row)
    for candidate, rows in sorted(grouped.items()):
        rows = sorted(rows, key=lambda r: safe_float(r["mean_initial_nodes"]))
        xs = [safe_float(r["mean_initial_nodes"]) for r in rows]
        ys = [safe_float(r["mean_radius"]) for r in rows]
        ax.plot(xs, ys, marker="o", label=candidate)
    ax.set_xlabel("Realized initial nodes")
    ax.set_ylabel("Mean radius")
    ax.set_title("Calibrated candidate size profiles")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def build_report(paths: Sequence[Path]) -> str:
    names = [p.name for p in paths]
    return "\n".join([
        "# v0.10b plotting og generator-diagnostikk",
        "",
        "- `nominal_vs_realized.png` viser om generatoren faktisk treffer større nominelle nivåer eller bare flater ut.",
        "- `realized_size_bands.png` viser q10-q90-båndene og dermed om nivåene faktisk separerer.",
        "- `growth_regime_comparison.png` viser kompromisset mellom størrelse-treff, hit-rate og naturalness-proxy.",
        "- `calibrated_size_profiles.png` viser kandidatprofilene etter kalibrert rerun.",
        "",
        "## Filer",
        "",
        *[f"- `{name}`" for name in names],
        "",
        "Disse figurene skal leses som generator- og finite-size-diagnostikk først, og som kandidatdiagnostikk deretter.",
        "",
    ])


def build_argparser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Plot v0.10b-v0.10d generator diagnostics")
    ap.add_argument("--calibration-summary", default="Documentation/v10b_ensemble_calibration_summary.csv")
    ap.add_argument("--growth-overall", default="Documentation/v10c_growth_regime_overall.csv")
    ap.add_argument("--size-profiles", default="Documentation/v10d_calibrated_scale_size_profiles.csv")
    ap.add_argument("--out-dir", default="Documentation/v10b_plots")
    ap.add_argument("--report-md", default="Documentation/v10b_plot_report.md")
    return ap


def main() -> None:
    args = build_argparser().parse_args()
    out_dir = ensure_dir(args.out_dir)
    calibration_rows = load_rows(args.calibration_summary)
    overall_rows = load_rows(args.growth_overall)
    size_rows = load_rows(args.size_profiles)

    nominal_path = out_dir / "nominal_vs_realized.png"
    bands_path = out_dir / "realized_size_bands.png"
    regimes_path = out_dir / "growth_regime_comparison.png"
    profiles_path = out_dir / "calibrated_size_profiles.png"

    plot_nominal_vs_realized(calibration_rows, nominal_path)
    plot_q10_q90(calibration_rows, bands_path)
    plot_growth_regimes(overall_rows, regimes_path)
    plot_size_profiles(size_rows, profiles_path)

    report_path = Path(args.report_md)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        build_report([nominal_path, bands_path, regimes_path, profiles_path]),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
