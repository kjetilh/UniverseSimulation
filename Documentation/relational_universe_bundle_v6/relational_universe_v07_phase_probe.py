
#!/usr/bin/env python3
"""relational_universe_v07_phase_probe.py

Small parameter-grid probe built on top of v0.7 local maximal coupling lab.
The purpose is not to produce a final phase diagram, but to cheaply identify
candidate regimes for v0.8.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import math
import statistics
from typing import Any, Dict, List

import relational_universe_local_max_coupling_lab as lab


def write_csv(path: str, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write("")
        return
    keys = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def markdown_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    head = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows[1:])
    return "\n".join([head, sep, body])


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Parameter probe on top of v0.7 local maximal coupling lab.")
    p.add_argument("--out-prefix", type=str, default="v07_phase_probe")
    p.add_argument("--steps", type=int, default=800)
    p.add_argument("--start-seed", type=int, default=1000)
    p.add_argument("--multirun-seeds", type=int, default=8)
    p.add_argument("--initial-cycle", type=int, default=8)
    p.add_argument("--initial-tokens", type=int, default=4)
    p.add_argument("--r-seed", type=float, default=0.04)
    p.add_argument("--r-token", type=float, default=1.0)
    p.add_argument("--r-birth-grid", type=str, default="0.0,0.05")
    p.add_argument("--r-death-grid", type=str, default="0.0,0.05")
    p.add_argument("--p-swap-grid", type=str, default="0.04,0.08")
    p.add_argument("--p-triad-grid", type=str, default="0.0,0.03")
    p.add_argument("--p-del-grid", type=str, default="0.0,0.01")
    p.add_argument("--perturbation", type=str, default="local_swap", choices=["local_swap", "add_chord"])
    p.add_argument("--coupling-mode", type=str, default="maximal", choices=["maximal", "rank"])
    return p


def parse_grid(text: str) -> List[float]:
    return [float(x.strip()) for x in text.split(",") if x.strip()]


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
        a = argparse.Namespace(**vars(base))
        a.r_birth = rb
        a.r_death = rd
        a.p_swap = ps
        a.p_triad = pt
        a.p_del = pd
        a.local_coupling = args.coupling_mode
        a.seed = args.start_seed + 100 * idx
        stats = lab.collect_multirun_statistics(a, seeds=list(range(a.seed, a.seed + a.multirun_seeds)), coupling_modes=[args.coupling_mode])
        s = stats["summaries"][args.coupling_mode]
        row = {
            "r_birth": rb,
            "r_death": rd,
            "p_swap": ps,
            "p_triad": pt,
            "p_del": pd,
            "runs": s["runs"],
            "meeting_fraction": s["meeting_fraction"],
            "mean_first_meeting_time_conditional": s["mean_first_meeting_time_conditional"],
            "mean_final_radius_control": s["mean_final_radius_control"],
            "mean_total_unequal_time": s["mean_total_unequal_time"],
            "mean_avg_local_overlap": s["mean_avg_local_overlap"],
            "mean_same_descriptor_rate": s["mean_same_descriptor_rate"],
            "mean_shared_token_fraction_final": s["mean_shared_token_fraction_final"],
            "mean_shared_node_fraction_final": s["mean_shared_node_fraction_final"],
        }
        rows.append(row)

    csv_path = f"{args.out_prefix}.csv"
    md_path = f"{args.out_prefix}.md"
    write_csv(csv_path, rows)

    best_overlap = sorted(rows, key=lambda r: (r["mean_avg_local_overlap"], -r["mean_total_unequal_time"]), reverse=True)[:5]
    best_repair = sorted(rows, key=lambda r: (r["meeting_fraction"], -r["mean_total_unequal_time"], r["mean_shared_token_fraction_final"]), reverse=True)[:5]
    best_cone = sorted(rows, key=lambda r: (-r["mean_final_radius_control"], r["mean_total_unequal_time"]))[:5]

    def rows_to_table(title: str, sub: List[Dict[str, Any]]) -> List[str]:
        trows = [["r_birth", "r_death", "p_swap", "p_triad", "p_del", "meeting_frac", "mean_overlap", "same_desc", "unequal_time", "shared_token_frac", "final_radius"]]
        for r in sub:
            trows.append([
                f"{r['r_birth']:.3g}",
                f"{r['r_death']:.3g}",
                f"{r['p_swap']:.3g}",
                f"{r['p_triad']:.3g}",
                f"{r['p_del']:.3g}",
                f"{r['meeting_fraction']:.3g}",
                f"{r['mean_avg_local_overlap']:.3g}",
                f"{r['mean_same_descriptor_rate']:.3g}",
                f"{r['mean_total_unequal_time']:.3g}",
                f"{r['mean_shared_token_fraction_final']:.3g}",
                f"{r['mean_final_radius_control']:.3g}",
            ])
        return [f"## {title}", "", markdown_table(trows), ""]

    lines = [
        "# v0.7 faseprobe",
        "",
        "Dette er ikke et endelig fasekart. Det er en hurtig sonde for å finne lovende regimer før v0.8.",
        "",
        f"- coupling_mode: {args.coupling_mode}",
        f"- perturbation: {args.perturbation}",
        f"- steps per run: {args.steps}",
        f"- seeds per grid point: {args.multirun_seeds}",
        f"- antall gridpunkter: {len(rows)}",
        "",
        *rows_to_table("Beste lokal overlap", best_overlap),
        *rows_to_table("Beste repair (meeting/unequal/shared token)", best_repair),
        *rows_to_table("Mest begrenset radius (lav radius + lav unequal time)", best_cone),
        f"_CSV: `{csv_path}`_",
        "",
    ]
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print({"csv": csv_path, "md": md_path, "rows": len(rows)})


if __name__ == "__main__":
    main()
