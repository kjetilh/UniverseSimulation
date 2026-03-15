
#!/usr/bin/env python3
"""relational_universe_uniformized_scan.py

Batch runner / parameter-scan harness for v0.6 uniformized coupling lab.
It imports `relational_universe_uniformized_coupling_lab.py`, runs many seeds
over a parameter grid, and writes both raw CSV and a markdown summary.

Typical use
-----------
python relational_universe_uniformized_scan.py \
  --steps 5000 \
  --seeds 20 \
  --p-triad-values 0.0,0.03,0.05 \
  --p-del-values 0.0,0.02,0.03 \
  --r-birth-values 0.006,0.01 \
  --r-death-values 0.005,0.009 \
  --out-csv scan.csv \
  --out-summary-md scan_summary.md
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import itertools
import json
import math
import os
import random
import statistics
import sys
from typing import Any, Dict, List

import numpy as np
import pandas as pd


def load_v06(module_path: str):
    spec = importlib.util.spec_from_file_location("v06lab_scan", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["v06lab_scan"] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def parse_float_list(s: str) -> List[float]:
    return [float(x.strip()) for x in s.split(",") if x.strip()]

def markdown_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    head = "| " + " | ".join(rows[0]) + " |"
    sep = "| " + " | ".join("---" for _ in rows[0]) + " |"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows[1:])
    return "\n".join([head, sep, body])

def estimate_front_speed(v06, log_rows):
    return v06.estimate_front_speed(log_rows, "t", "radius_control")

def run_once(v06, seed: int, steps: int, params, perturbation: str, center_token_index: int, initial_cycle: int, initial_tokens: int, log_every: int) -> Dict[str, Any]:
    rng = random.Random(seed)
    base, next_node_id, next_token_id = v06.bootstrap(initial_cycle, initial_tokens, rng)
    control = base.clone()
    perturbed = base.clone()
    perturbation_info = v06.apply_perturbation(perturbed, perturbation, center_token_index)
    support = perturbation_info["support"]
    manager = v06.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)

    log_rows = []
    event_rows = []

    snap0 = v06.damage_snapshot(control, perturbed, support)
    log_rows.append({"step": 0, "t": 0.0, **snap0})
    max_radius_control = max(-1, snap0["radius_control"])
    max_radius_perturbed = max(-1, snap0["radius_perturbed"])

    for step in range(1, steps + 1):
        shared = v06.coupled_step(control, perturbed, manager, rng, params)
        event_rows.append({
            "family": shared["family"],
            "accept_control": int(bool(shared.get("accept_control", False))),
            "accept_perturbed": int(bool(shared.get("accept_perturbed", False))),
        })
        if step % log_every == 0 or step == steps:
            snap = v06.damage_snapshot(control, perturbed, support)
            max_radius_control = max(max_radius_control, snap["radius_control"])
            max_radius_perturbed = max(max_radius_perturbed, snap["radius_perturbed"])
            log_rows.append({"step": step, "t": control.t, **snap})

    final = log_rows[-1]
    speed = estimate_front_speed(v06, log_rows)
    coupling = v06.summarize_coupling([
        {
            "family": r["family"],
            "accept_control": r["accept_control"],
            "accept_perturbed": r["accept_perturbed"],
        }
        for r in event_rows
    ])

    return {
        "seed": seed,
        "final_t": float(final["t"]),
        "final_radius_control": int(final["radius_control"]),
        "max_radius_control": int(max_radius_control),
        "final_radius_perturbed": int(final["radius_perturbed"]),
        "max_radius_perturbed": int(max_radius_perturbed),
        "final_edge_diff_count": int(final["edge_diff_count"]),
        "final_damaged_nodes_count": int(final["damaged_nodes_count"]),
        "final_delta_tokens": float(final["delta_tokens"]),
        "final_delta_beta1": float(final["delta_beta1"]),
        "final_core_l1": float(final["core_l1"]),
        "final_regime_l1": float(final["regime_l1"]),
        "fit_speed_control": float(speed["fit_slope"]),
        "both_accept_total": int(coupling["both_accept_total"]),
        "one_sided_total": int(coupling["one_sided_total"]),
        "null_total": int(coupling["null_total"]),
        "both_accept_frac": coupling["both_accept_total"] / max(1, coupling["total_potential_events"]),
        "one_sided_frac": coupling["one_sided_total"] / max(1, coupling["total_potential_events"]),
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Batch scan for v0.6 uniformized coupling lab.")
    p.add_argument("--module-path", type=str, default="relational_universe_uniformized_coupling_lab.py")
    p.add_argument("--steps", type=int, default=5000)
    p.add_argument("--seeds", type=int, default=10)
    p.add_argument("--seed-offset", type=int, default=1000)
    p.add_argument("--initial-cycle", type=int, default=8)
    p.add_argument("--initial-tokens", type=int, default=4)
    p.add_argument("--log-every", type=int, default=50)
    p.add_argument("--perturbation", type=str, default="local_swap", choices=["local_swap", "add_chord"])
    p.add_argument("--center-token-index", type=int, default=0)

    p.add_argument("--r-seed", type=float, default=0.04)
    p.add_argument("--r-token", type=float, default=1.0)
    p.add_argument("--birth-degree-bias-values", type=str, default="0.75")
    p.add_argument("--death-inverse-degree-scale-values", type=str, default="1.0")
    p.add_argument("--r-birth-values", type=str, default="0.01")
    p.add_argument("--r-death-values", type=str, default="0.009")
    p.add_argument("--p-triad-values", type=str, default="0.0,0.05")
    p.add_argument("--p-del-values", type=str, default="0.0,0.03")
    p.add_argument("--p-swap-values", type=str, default="0.08")
    p.add_argument("--min-tokens", type=int, default=1)

    p.add_argument("--out-csv", type=str, default="uniformized_scan_stats.csv")
    p.add_argument("--out-summary-md", type=str, default="uniformized_scan_summary.md")
    return p


def main() -> None:
    args = build_parser().parse_args()
    v06 = load_v06(args.module_path)

    grids = {
        "birth_degree_bias": parse_float_list(args.birth_degree_bias_values),
        "death_inverse_degree_scale": parse_float_list(args.death_inverse_degree_scale_values),
        "r_birth": parse_float_list(args.r_birth_values),
        "r_death": parse_float_list(args.r_death_values),
        "p_triad": parse_float_list(args.p_triad_values),
        "p_del": parse_float_list(args.p_del_values),
        "p_swap": parse_float_list(args.p_swap_values),
    }

    rows = []
    for combo in itertools.product(
        grids["birth_degree_bias"],
        grids["death_inverse_degree_scale"],
        grids["r_birth"],
        grids["r_death"],
        grids["p_triad"],
        grids["p_del"],
        grids["p_swap"],
    ):
        bdb, dids, rb, rd, pt, pdel, ps = combo
        regime = f"rb={rb}_rd={rd}_pt={pt}_pd={pdel}_ps={ps}_bdb={bdb}_dids={dids}"
        params = v06.Params(
            r_seed=args.r_seed,
            r_token=args.r_token,
            r_birth=rb,
            r_death=rd,
            p_triad=pt,
            p_del=pdel,
            p_swap=ps,
            birth_degree_bias=bdb,
            death_inverse_degree_scale=dids,
            min_tokens=args.min_tokens,
        )
        for i in range(args.seeds):
            seed = args.seed_offset + i
            row = run_once(
                v06=v06,
                seed=seed,
                steps=args.steps,
                params=params,
                perturbation=args.perturbation,
                center_token_index=args.center_token_index,
                initial_cycle=args.initial_cycle,
                initial_tokens=args.initial_tokens,
                log_every=args.log_every,
            )
            row["regime"] = regime
            row["r_birth"] = rb
            row["r_death"] = rd
            row["p_triad"] = pt
            row["p_del"] = pdel
            row["p_swap"] = ps
            row["birth_degree_bias"] = bdb
            row["death_inverse_degree_scale"] = dids
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(args.out_csv, index=False)

    agg = df.groupby("regime").agg({
        "final_radius_control": ["mean", "std", "median", "min", "max"],
        "max_radius_control": ["mean", "std", "median", "min", "max"],
        "final_delta_tokens": ["mean", "std", "median", "min", "max"],
        "fit_speed_control": ["mean", "std", "median", "min", "max"],
        "both_accept_frac": ["mean", "std", "median", "min", "max"],
        "one_sided_frac": ["mean", "std", "median", "min", "max"],
    })
    agg.columns = ["_".join(c) for c in agg.columns]
    agg = agg.reset_index().sort_values(["max_radius_control_mean", "one_sided_frac_mean"], ascending=[False, True])

    rows_md = [[
        "regime",
        "max_radius_mean",
        "final_radius_mean",
        "delta_tokens_mean",
        "fit_speed_mean",
        "both_accept_frac_mean",
        "one_sided_frac_mean",
    ]]
    for _, r in agg.iterrows():
        rows_md.append([
            str(r["regime"]),
            f"{r['max_radius_control_mean']:.4g}",
            f"{r['final_radius_control_mean']:.4g}",
            f"{r['final_delta_tokens_mean']:.4g}",
            f"{r['fit_speed_control_mean']:.4g}",
            f"{r['both_accept_frac_mean']:.4g}",
            f"{r['one_sided_frac_mean']:.4g}",
        ])

    summary = "\n".join([
        "# Uniformized coupling scan summary",
        "",
        "## Hva denne filen er",
        "",
        "Dette er en batch-oppsummering av v0.6-laben over et eksplisitt parametergrid.",
        "Hensikten er å finne regimer som samtidig gir:",
        "",
        "- merkbar, men ikke ukontrollert one-sided coupling",
        "- rimelig høy both-accept-fraksjon",
        "- og en målbar, ikke-triviell radiusutbredelse.",
        "",
        "## Resultattabell",
        "",
        markdown_table(rows_md),
        "",
        "## Tolkning",
        "",
        "Høye `both_accept_frac` betyr at de to grenene fortsatt drives sterkt av felles støy.",
        "Høye `one_sided_frac` betyr at regimet virkelig er åpent nok til at familywise uniformization gjør en forskjell.",
        "Et regime er ofte mest interessant når begge tallene er moderate: nok felles struktur til å måle kausalitet, nok åpenhet til at testen er genuint ny i forhold til v0.5.",
        "",
        f"_Rå CSV: `{args.out_csv}`_",
        "",
    ])
    with open(args.out_summary_md, "w", encoding="utf-8") as f:
        f.write(summary)

    print(json.dumps({
        "rows": len(df),
        "regimes": int(df["regime"].nunique()),
        "out_csv": args.out_csv,
        "out_summary_md": args.out_summary_md,
    }, indent=2))


if __name__ == "__main__":
    main()
