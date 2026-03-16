#!/usr/bin/env python3
"""Plotting helpers for the relational-universe v0.8 phase atlas."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np


SCORES = [
    ("composite_score", "Composite score"),
    ("repair_score", "Repair score"),
    ("causal_score", "Causal score"),
    ("quasi_score", "Quasi score"),
    ("geom_score", "Geometry proxy score"),
]


def ensure_dir(path: str | Path) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def load_rows(path: str | Path) -> List[Dict[str, float | int]]:
    with open(path, newline="", encoding="utf-8") as f:
        raw = list(csv.DictReader(f))
    rows: List[Dict[str, float | int]] = []
    for row in raw:
        out: Dict[str, float | int] = {}
        for key, value in row.items():
            try:
                if key == "pareto":
                    out[key] = int(float(value))
                else:
                    out[key] = float(value)
            except Exception:
                out[key] = value
        rows.append(out)
    return rows


def axis_labels(rows: Sequence[Dict[str, float | int]]) -> Tuple[List[str], List[str]]:
    x_labels = sorted({f"rb={row['r_birth']:.2f}\nrd={row['r_death']:.2f}" for row in rows})
    y_labels = sorted({f"ps={row['p_swap']:.2f}\npt={row['p_triad']:.2f}\npd={row['p_del']:.2f}" for row in rows})
    return x_labels, y_labels


def matrix_for(rows: Sequence[Dict[str, float | int]], value_key: str) -> Tuple[np.ndarray, List[Tuple[int, int]]]:
    x_labels, y_labels = axis_labels(rows)
    x_index = {label: idx for idx, label in enumerate(x_labels)}
    y_index = {label: idx for idx, label in enumerate(y_labels)}
    matrix = np.full((len(y_labels), len(x_labels)), np.nan, dtype=float)
    pareto_points: List[Tuple[int, int]] = []
    for row in rows:
        x_label = f"rb={row['r_birth']:.2f}\nrd={row['r_death']:.2f}"
        y_label = f"ps={row['p_swap']:.2f}\npt={row['p_triad']:.2f}\npd={row['p_del']:.2f}"
        i = y_index[y_label]
        j = x_index[x_label]
        matrix[i, j] = float(row[value_key])
        if int(row.get("pareto", 0)) == 1:
            pareto_points.append((i, j))
    return matrix, pareto_points


def save_heatmap(rows: Sequence[Dict[str, float | int]], value_key: str, title: str, out_path: str | Path) -> None:
    x_labels, y_labels = axis_labels(rows)
    matrix, pareto_points = matrix_for(rows, value_key)
    fig, ax = plt.subplots(figsize=(max(8, len(x_labels) * 0.9), max(6, len(y_labels) * 0.6)))
    im = ax.imshow(matrix, aspect="auto", cmap="viridis")
    ax.set_title(title)
    ax.set_xticks(range(len(x_labels)))
    ax.set_xticklabels(x_labels, rotation=45, ha="right")
    ax.set_yticks(range(len(y_labels)))
    ax.set_yticklabels(y_labels)
    for i, j in pareto_points:
        ax.scatter(j, i, marker="s", s=90, facecolors="none", edgecolors="white", linewidths=1.5)
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(value_key)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def make_report_md(
    coarse_rows: Sequence[Dict[str, float | int]],
    refined_rows: Sequence[Dict[str, float | int]],
    out_dir: str | Path,
) -> str:
    lines = [
        "# v0.8 atlas heatmaps",
        "",
        "## Observasjon",
        "",
        "- Hver figur viser én score om gangen, uten subplots.",
        "- Kolonnene er `(r_birth, r_death)`-kombinasjoner, og radene er `(p_swap, p_triad, p_del)`-kombinasjoner.",
        "- Hvite markeringer er Paretofront-punkter.",
        "",
        "## Tolkning",
        "",
        "- Dette er ikke et fullstendig fasekart over hele parameterrommet. Det er en visualisering av det valgte coarse/refined-slicet.",
        "- `p_del = 0` ble brukt i coarse-atlaset fordi v0.8 startet fra den delen av rommet som så mest lovende ut uten sletting; refined-runden åpner denne aksen svakt igjen.",
        "- Paretofront er nyttig fordi repair, causalitet, quasi-stabilitet og geometri-proxy konkurrerer. Et punkt kan være svært godt på én akse uten å være globalt best.",
        "",
        "## Spekulasjon som fortsatt må holdes nede",
        "",
        "- Et varmt område i `composite_score` er ikke i seg selv en fase.",
        "- Et Pareto-punkt er ikke nødvendigvis fysisk interessant; det kan også være et kompromisspunkt uten sterk spacetime-lesning.",
        "",
        "## Filer",
        "",
    ]
    for dataset in ["coarse", "refined"]:
        for score_key, _ in SCORES:
            lines.append(f"- `{dataset}_{score_key}_heatmap.png`")
    lines.extend([
        "",
        f"_Coarse rows: {len(coarse_rows)}_",
        "",
        f"_Refined rows: {len(refined_rows)}_",
        "",
    ])
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Heatmaps and Pareto overlays for the v0.8 phase atlas.")
    p.add_argument("--input-prefix", type=str, default="Documentation/v08_phase_atlas")
    p.add_argument("--out-dir", type=str, default="Documentation/v08_phase_atlas_plots")
    return p


def main() -> None:
    args = build_parser().parse_args()
    input_prefix = Path(args.input_prefix)
    out_dir = Path(args.out_dir)
    ensure_dir(out_dir)

    coarse_csv = input_prefix.with_name(input_prefix.name + "_coarse.csv")
    refined_csv = input_prefix.with_name(input_prefix.name + "_refined.csv")
    coarse_rows = load_rows(coarse_csv)
    refined_rows = load_rows(refined_csv)

    for dataset_name, rows in [("coarse", coarse_rows), ("refined", refined_rows)]:
        for score_key, title in SCORES:
            out_path = out_dir / f"{dataset_name}_{score_key}_heatmap.png"
            save_heatmap(rows, score_key, f"{dataset_name}: {title}", out_path)

    report_path = out_dir / "v08_phase_atlas_heatmaps.md"
    report_path.write_text(make_report_md(coarse_rows, refined_rows, out_dir), encoding="utf-8")
    print(
        {
            "coarse_csv": str(coarse_csv),
            "refined_csv": str(refined_csv),
            "out_dir": str(out_dir),
            "report_md": str(report_path),
        }
    )


if __name__ == "__main__":
    main()
