#!/usr/bin/env python3
"""relational_universe_v07_phase_probe.py

Exploratory v0.8 phase-map scan built on top of the v0.7 local maximal
coupling lab. The script preserves the earlier grid-driven CLI, but extends
the output from a light candidate probe to a compact regime map that combines:

1. repair / meeting,
2. radius propagation / front speed,
3. macro drift,
4. geometry proxies.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List

import relational_universe_local_max_coupling_lab as lab


def ensure_parent_dir(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def write_csv(path: str, rows: List[Dict[str, Any]]) -> None:
    ensure_parent_dir(path)
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    keys = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def write_text(path: str, text: str) -> None:
    ensure_parent_dir(path)
    Path(path).write_text(text, encoding="utf-8")


def markdown_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    head = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows[1:])
    return "\n".join([head, sep, body])


def parse_grid(text: str) -> List[float]:
    return [float(x.strip()) for x in text.split(",") if x.strip()]


def finite_or_nan(value: float) -> float:
    return value if math.isfinite(value) else float("nan")


def sort_value(value: float, reverse: bool = False) -> float:
    if not math.isfinite(value):
        return -float("inf") if reverse else float("inf")
    return value


def add_minmax_score(rows: List[Dict[str, Any]], source_key: str, dest_key: str, larger_is_better: bool) -> None:
    values = [float(row[source_key]) for row in rows if math.isfinite(float(row[source_key]))]
    if not values:
        for row in rows:
            row[dest_key] = 0.0
        return
    lo = min(values)
    hi = max(values)
    if hi - lo <= 1e-12:
        for row in rows:
            row[dest_key] = 1.0
        return
    for row in rows:
        value = float(row[source_key])
        if not math.isfinite(value):
            row[dest_key] = 0.0
            continue
        scaled = (value - lo) / (hi - lo)
        row[dest_key] = scaled if larger_is_better else 1.0 - scaled


def add_composite_scores(rows: List[Dict[str, Any]]) -> None:
    add_minmax_score(rows, "meeting_fraction", "_score_meeting", True)
    add_minmax_score(rows, "mean_avg_local_overlap", "_score_overlap", True)
    add_minmax_score(rows, "mean_same_descriptor_rate", "_score_same_desc", True)
    add_minmax_score(rows, "mean_total_unequal_time", "_score_unequal", False)
    add_minmax_score(rows, "mean_final_radius_control", "_score_radius", False)
    add_minmax_score(rows, "fit_speed_control", "_score_speed", False)
    add_minmax_score(rows, "drift_beta1_abs", "_score_beta1_drift", False)
    add_minmax_score(rows, "drift_tokens_abs", "_score_tokens_drift", False)
    add_minmax_score(rows, "mean_spectral_radius", "_score_spectral", True)
    add_minmax_score(rows, "mean_clustering", "_score_clustering", True)
    add_minmax_score(rows, "mean_dim_proxy", "_score_dim", True)

    for row in rows:
        row["repair_score"] = (
            0.35 * row["_score_meeting"]
            + 0.25 * row["_score_overlap"]
            + 0.20 * row["_score_same_desc"]
            + 0.20 * row["_score_unequal"]
        )
        row["cone_score"] = (
            0.45 * row["_score_radius"]
            + 0.35 * row["_score_speed"]
            + 0.20 * row["_score_unequal"]
        )
        row["invariant_score"] = (
            0.50 * row["_score_beta1_drift"]
            + 0.50 * row["_score_tokens_drift"]
        )
        row["geometry_score"] = (
            0.35 * row["_score_dim"]
            + 0.35 * row["_score_clustering"]
            + 0.30 * row["_score_spectral"]
        )
        row["sweet_spot_score"] = (
            0.35 * row["repair_score"]
            + 0.25 * row["cone_score"]
            + 0.20 * row["invariant_score"]
            + 0.20 * row["geometry_score"]
        )


def top_rows(rows: List[Dict[str, Any]], key: str, top_k: int, reverse: bool = True) -> List[Dict[str, Any]]:
    return sorted(rows, key=lambda row: sort_value(float(row[key]), reverse=reverse), reverse=reverse)[:top_k]


def build_params_row(summary: Dict[str, Any], rb: float, rd: float, ps: float, pt: float, pd: float) -> Dict[str, Any]:
    row = {
        "r_birth": rb,
        "r_death": rd,
        "p_swap": ps,
        "p_triad": pt,
        "p_del": pd,
        "runs": summary["runs"],
        "meeting_fraction": summary["meeting_fraction"],
        "mean_first_meeting_time_conditional": summary["mean_first_meeting_time_conditional"],
        "mean_total_unequal_time": summary["mean_total_unequal_time"],
        "mean_final_radius_control": summary["mean_final_radius_control"],
        "fit_speed_control": summary["mean_fit_speed_control"],
        "mean_avg_local_overlap": summary["mean_avg_local_overlap"],
        "mean_same_descriptor_rate": summary["mean_same_descriptor_rate"],
        "drift_beta1": summary["mean_drift_beta1"],
        "drift_tokens": summary["mean_drift_tokens"],
        "drift_beta1_abs": abs(summary["mean_drift_beta1"]),
        "drift_tokens_abs": abs(summary["mean_drift_tokens"]),
        "mean_spectral_radius": summary["mean_spectral_radius"],
        "mean_clustering": summary["mean_clustering"],
        "mean_dim_proxy": summary["mean_dim_proxy"],
        "mean_shared_token_fraction_final": summary["mean_shared_token_fraction_final"],
        "mean_shared_node_fraction_final": summary["mean_shared_node_fraction_final"],
    }
    return {key: finite_or_nan(float(value)) if isinstance(value, (int, float)) else value for key, value in row.items()}


def rows_to_table(title: str, rows: Iterable[Dict[str, Any]], score_key: str) -> List[str]:
    table_rows = [[
        "r_birth",
        "r_death",
        "p_swap",
        "p_triad",
        "p_del",
        "score",
        "meeting",
        "overlap",
        "same_desc",
        "unequal",
        "radius",
        "speed",
        "|drift_beta1|",
        "|drift_tokens|",
        "dim",
    ]]
    for row in rows:
        table_rows.append([
            f"{row['r_birth']:.3g}",
            f"{row['r_death']:.3g}",
            f"{row['p_swap']:.3g}",
            f"{row['p_triad']:.3g}",
            f"{row['p_del']:.3g}",
            f"{row[score_key]:.3f}",
            f"{row['meeting_fraction']:.3g}",
            f"{row['mean_avg_local_overlap']:.3g}",
            f"{row['mean_same_descriptor_rate']:.3g}",
            f"{row['mean_total_unequal_time']:.3g}",
            f"{row['mean_final_radius_control']:.3g}",
            f"{row['fit_speed_control']:.3g}",
            f"{row['drift_beta1_abs']:.3g}",
            f"{row['drift_tokens_abs']:.3g}",
            f"{row['mean_dim_proxy']:.3g}",
        ])
    return [f"## {title}", "", markdown_table(table_rows), ""]


def make_report_md(args: argparse.Namespace, rows: List[Dict[str, Any]], csv_path: str) -> str:
    sweet = top_rows(rows, "sweet_spot_score", args.top_k)
    repair = top_rows(rows, "repair_score", args.top_k)
    cone = top_rows(rows, "cone_score", args.top_k)
    invariant = top_rows(rows, "invariant_score", args.top_k)
    geometry = top_rows(rows, "geometry_score", args.top_k)

    lines = [
        "# v0.8 fasekart over repair, kausalitet, drift og geometri",
        "",
        "## Formål",
        "",
        "Dette er første egentlige fasekart over det fokuserte parameterrommet rundt de mest lovende v0.7-punktene. Hvert gridpunkt kombinerer repair-mål, frontdiagnostikk, makrodrift og geometri-proksier i én rad.",
        "",
        "## Metode",
        "",
        f"- lokal kobling: `{args.coupling_mode}`",
        f"- perturbasjon: `{args.perturbation}`",
        f"- steg per run: `{args.steps}`",
        f"- seeds per gridpunkt: `{args.multirun_seeds}`",
        f"- antall gridpunkter: `{len(rows)}`",
        "- `drift_beta1` og `drift_tokens` er her definert som netto endring per event i kontrollgrenen over kjøringen.",
        "- `fit_speed_control` er lineær tilpasning av radius mot event-tid i kontrollgrenen. Den er et grovt frontmål, ikke en streng bound.",
        "- `geometry_score` er eksplisitt heuristisk: den rangerer høyere `dim_proxy`, `clustering` og `spectral_radius`, men uten å påstå at det finnes en unik riktig geometri-signatur.",
        "",
        "## Hovedlesning",
        "",
        "- repair-vennlig: høy `meeting_fraction`, høy lokal overlap og lav `total_unequal_time`.",
        "- cone-vennlig: lav `mean_final_radius_control` og lav `fit_speed_control`.",
        "- invariant-vennlig: liten absolutt drift i `beta1` og `tokens`.",
        "- geometri-vennlig: høyere `dim_proxy`/`clustering`/`spectral_radius` uten samtidig stor drift.",
        "",
        *rows_to_table("Sweet spot-kandidater", sweet, "sweet_spot_score"),
        *rows_to_table("Repair-vennlige punkter", repair, "repair_score"),
        *rows_to_table("Cone-vennlige punkter", cone, "cone_score"),
        *rows_to_table("Invariant-vennlige punkter", invariant, "invariant_score"),
        *rows_to_table("Geometri-vennlige punkter", geometry, "geometry_score"),
        "## Vurdering",
        "",
    ]

    if sweet:
        best = sweet[0]
        lines.extend([
            f"Det beste kompromisset i denne scanningen ligger ved `r_birth={best['r_birth']:.3g}`, `r_death={best['r_death']:.3g}`, `p_swap={best['p_swap']:.3g}`, `p_triad={best['p_triad']:.3g}`, `p_del={best['p_del']:.3g}`.",
            "",
            "Dette er ikke et bevis på et unikt optimalt regime, men et praktisk sweet spot for neste runde: punktet kombinerer høyere repair-score enn de fleste konkurrenter med moderat radius, lavere drift og relativt strukturerte geometri-proksier.",
            "",
        ])

    lines.extend([
        "## Hva som er data, og hva som er tolkning",
        "",
        "- Data: alle tall i CSV-en og tabellene over.",
        "- Tolkning: at et punkt er `repair-vennlig`, `cone-vennlig`, `invariant-vennlig` eller `geometri-vennlig` er en operasjonell merkelapp basert på scorene over.",
        "- Spekulasjon: at et slikt sweet spot faktisk er en kandidat for emergent spacetime. Det krever mer presis skalering, flere seeds og helst strengere lokale koblinger i åpne familier.",
        "",
        f"_CSV: `{csv_path}`_",
        "",
    ])
    return "\n".join(lines)


def make_status_md(rows: List[Dict[str, Any]]) -> str:
    sweet = top_rows(rows, "sweet_spot_score", 3)
    repair = top_rows(rows, "repair_score", 3)
    invariant = top_rows(rows, "invariant_score", 3)
    lines = [
        "# Relasjonell universgraf – status v0.8 fasekart",
        "",
        "## Hva som er nytt",
        "- Vi har nå ett samlet parameterkart som rangerer repair, radius/front, makrodrift og geometri-proksier samtidig.",
        "- Kartet bruker maksimal lokal kobling som standard og ligger derfor på toppen av v0.7-metodikken.",
        "",
        "## Kort dom",
    ]
    for idx, row in enumerate(sweet, start=1):
        lines.append(
            f"{idx}. sweet spot-kandidat: r_birth={row['r_birth']:.3g}, r_death={row['r_death']:.3g}, p_swap={row['p_swap']:.3g}, p_triad={row['p_triad']:.3g}, p_del={row['p_del']:.3g}, sweet_score={row['sweet_spot_score']:.3f}"
        )
    lines.extend([
        "",
        "## Hva som ser mest lovende ut",
    ])
    if repair:
        r = repair[0]
        lines.append(
            f"- Repair-vennlig: r_birth={r['r_birth']:.3g}, r_death={r['r_death']:.3g}, p_swap={r['p_swap']:.3g}, p_triad={r['p_triad']:.3g}, p_del={r['p_del']:.3g}"
        )
    if invariant:
        r = invariant[0]
        lines.append(
            f"- Invariant-vennlig: r_birth={r['r_birth']:.3g}, r_death={r['r_death']:.3g}, p_swap={r['p_swap']:.3g}, p_triad={r['p_triad']:.3g}, p_del={r['p_del']:.3g}"
        )
    lines.extend([
        "",
        "## Hva som fortsatt mangler",
        "- Mer presis statistikk på de beste punktene.",
        "- Skalering med flere seeds og lengre runs.",
        "- Eventuelt v0.7+-arbeid med enda skarpere lokal kobling i åpne familier hvis repair fortsatt ser skjør ut.",
        "",
    ])
    return "\n".join(lines)


def make_lay_md(rows: List[Dict[str, Any]]) -> str:
    sweet = top_rows(rows, "sweet_spot_score", 1)
    best = sweet[0] if sweet else None
    lines = [
        "# Forklaring for ikke-spesialister – v0.8 fasekart",
        "",
        "Vi har laget et kart over hvilke innstillinger i modellen som ser mest lovende ut når vi spør fire ting samtidig:",
        "",
        "1. reparerer to nesten like universer forskjellen sin?",
        "2. sprer forskjellen seg med liten eller stor radius?",
        "3. driver de store størrelsene mye eller lite?",
        "4. ser grafen fortsatt ut til å ha en lesbar geometri?",
        "",
    ]
    if best is not None:
        lines.extend([
            "Det mest lovende punktet i denne runden var:",
            "",
            f"- birth ≈ {best['r_birth']:.3g}",
            f"- death ≈ {best['r_death']:.3g}",
            f"- swap ≈ {best['p_swap']:.3g}",
            f"- triad ≈ {best['p_triad']:.3g}",
            f"- delete ≈ {best['p_del']:.3g}",
            "",
            "Det betyr ikke at vi har funnet `det riktige universet`.",
            "Det betyr bare at denne delen av parameterrommet ser ut til å balansere reparasjon, begrenset spredning og struktur bedre enn naboene sine.",
            "",
        ])
    lines.extend([
        "Det viktigste resultatet er derfor ikke én magisk konstant, men at kartet nå peker på et smalere område som er verdt å studere mye grundigere.",
        "",
    ])
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="v0.8 phase-map scan on top of the v0.7 local maximal coupling lab.")
    p.add_argument("--out-prefix", type=str, default="v08_phase_map")
    p.add_argument("--steps", type=int, default=500)
    p.add_argument("--start-seed", type=int, default=1400)
    p.add_argument("--multirun-seeds", type=int, default=4)
    p.add_argument("--initial-cycle", type=int, default=8)
    p.add_argument("--initial-tokens", type=int, default=4)
    p.add_argument("--r-seed", type=float, default=0.04)
    p.add_argument("--r-token", type=float, default=1.0)
    p.add_argument("--r-birth-grid", type=str, default="0.02,0.05,0.08")
    p.add_argument("--r-death-grid", type=str, default="0.00,0.02,0.05")
    p.add_argument("--p-swap-grid", type=str, default="0.02,0.04,0.08")
    p.add_argument("--p-triad-grid", type=str, default="0.00,0.01,0.03")
    p.add_argument("--p-del-grid", type=str, default="0.00,0.01")
    p.add_argument("--perturbation", type=str, default="local_swap", choices=["local_swap", "add_chord"])
    p.add_argument("--coupling-mode", type=str, default="maximal", choices=["maximal", "rank"])
    p.add_argument("--top-k", type=int, default=8)
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    base = lab.build_parser().parse_args([])
    base.steps = args.steps
    base.seed = args.start_seed
    base.multirun_seeds = args.multirun_seeds
    base.initial_cycle = args.initial_cycle
    base.initial_tokens = args.initial_tokens
    base.r_seed = args.r_seed
    base.r_token = args.r_token
    base.perturbation = args.perturbation

    rb_grid = parse_grid(args.r_birth_grid)
    rd_grid = parse_grid(args.r_death_grid)
    ps_grid = parse_grid(args.p_swap_grid)
    pt_grid = parse_grid(args.p_triad_grid)
    pd_grid = parse_grid(args.p_del_grid)

    rows: List[Dict[str, Any]] = []
    for idx, (rb, rd, ps, pt, pd) in enumerate(itertools.product(rb_grid, rd_grid, ps_grid, pt_grid, pd_grid)):
        if pt + pd + ps > 1.0 + 1e-12:
            continue
        point_args = argparse.Namespace(**vars(base))
        point_args.r_birth = rb
        point_args.r_death = rd
        point_args.p_swap = ps
        point_args.p_triad = pt
        point_args.p_del = pd
        point_args.local_coupling = args.coupling_mode
        point_args.seed = args.start_seed + 100 * idx
        stats = lab.collect_multirun_statistics(
            point_args,
            seeds=list(range(point_args.seed, point_args.seed + point_args.multirun_seeds)),
            coupling_modes=[args.coupling_mode],
        )
        summary = stats["summaries"][args.coupling_mode]
        rows.append(build_params_row(summary, rb, rd, ps, pt, pd))

    add_composite_scores(rows)

    csv_path = f"{args.out_prefix}.csv"
    report_md_path = f"{args.out_prefix}.md"
    status_md_path = f"{args.out_prefix}_status.md"
    lay_md_path = f"{args.out_prefix}_lay.md"

    write_csv(csv_path, rows)
    write_text(report_md_path, make_report_md(args, rows, csv_path))
    write_text(status_md_path, make_status_md(rows))
    write_text(lay_md_path, make_lay_md(rows))
    print({
        "csv": csv_path,
        "report_md": report_md_path,
        "status_md": status_md_path,
        "lay_md": lay_md_path,
        "rows": len(rows),
    })


if __name__ == "__main__":
    main()
