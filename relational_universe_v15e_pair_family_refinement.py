#!/usr/bin/env python3
"""v0.15e pair-family refinement in the 48-node corridor.

This follows v0.15d. We do not widen the search. We only ask whether the two
most informative 48-node pair families lean toward different interaction
windows when we spend more budget per pair:

- pair 2-3
- pair 3-4

Method:
- same anchor regime: band_zero_del
- same deep size-separated bases
- target corridor restricted to 48
- fixed pair families only
- more run offsets per pair
- dense matched AB/BA logging around the collision window
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Set, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15b_add_chord_collision_lab as v15b
import relational_universe_v15d_collision_window_lab as v15d


TARGET = 48
PAIR_SPECS = ((2, 3), (3, 4))


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15b.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15b.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    return v15b.write_csv(path, rows)


def parse_int_list(spec: str) -> List[int]:
    return [int(part.strip()) for part in spec.split(",") if part.strip()]


def support_info(base_state: Any, placement: int) -> Optional[Dict[str, Any]]:
    return v15b.discover_single_support(base_state, placement)


def pair_is_valid(base_state: Any, a: int, b: int) -> Optional[Dict[str, Any]]:
    info_a = support_info(base_state, a)
    info_b = support_info(base_state, b)
    if info_a is None or info_b is None:
        return None
    sa = set(info_a["support"])
    sb = set(info_b["support"])
    if sa.intersection(sb):
        return None
    return {
        "placement_a": int(a),
        "placement_b": int(b),
        "min_support_distance": int(v15b.support_min_distance(base_state.g, info_a["support"], info_b["support"])),
        "support_a_size": len(sa),
        "support_b_size": len(sb),
    }


def dense_log_every(steps: int) -> int:
    return max(2, min(12, steps // 160))


def collect_rows(
    ensembles: Sequence[Any],
    base_states: Mapping[Tuple[str, int], Any],
    growth_seeds: Sequence[int],
    run_offsets: Sequence[int],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    spec = v15b.anchor_spec()
    params = v15b.v09.candidate_to_params(spec["candidate"])

    for ens in ensembles:
        if int(ens.target_nodes) != TARGET:
            continue
        for gseed in growth_seeds:
            base = base_states[(ens.name, int(gseed))]
            steps = v15b.collision_steps_for_state(base.g.num_nodes())
            log_every = dense_log_every(steps)

            for placement_a, placement_b in PAIR_SPECS:
                pair_meta = pair_is_valid(base, placement_a, placement_b)
                if pair_meta is None:
                    continue
                pair = (placement_a, placement_b)
                reversed_pair = (placement_b, placement_a)

                for run_offset in run_offsets:
                    run_seed = int(ens.target_nodes) * 100000 + int(gseed) * 1000 + int(run_offset)
                    single_a = v15b.run_sequence_from_base(
                        base,
                        params=params,
                        seed=run_seed,
                        steps=steps,
                        placements=[pair[0]],
                        local_coupling="maximal",
                        log_every=log_every,
                    )
                    single_b = v15b.run_sequence_from_base(
                        base,
                        params=params,
                        seed=run_seed,
                        steps=steps,
                        placements=[pair[1]],
                        local_coupling="maximal",
                        log_every=log_every,
                    )
                    pair_ab = v15b.run_sequence_from_base(
                        base,
                        params=params,
                        seed=run_seed,
                        steps=steps,
                        placements=list(pair),
                        local_coupling="maximal",
                        log_every=log_every,
                    )
                    pair_ba = v15b.run_sequence_from_base(
                        base,
                        params=params,
                        seed=run_seed,
                        steps=steps,
                        placements=list(reversed_pair),
                        local_coupling="maximal",
                        log_every=log_every,
                    )

                    n_snap = min(
                        len(single_a["damaged_sets"]),
                        len(single_b["damaged_sets"]),
                        len(pair_ab["damaged_sets"]),
                        len(pair_ba["damaged_sets"]),
                    )
                    union_jaccards: List[float] = []
                    order_jaccards: List[float] = []
                    control_consistency: List[float] = []
                    pair_minus_union_components: List[float] = []
                    pair_minus_union_largest_frac: List[float] = []
                    snapshot_steps: List[int] = []

                    for idx in range(n_snap):
                        union_d = set(single_a["damaged_sets"][idx]).union(single_b["damaged_sets"][idx])
                        pair_ab_d = set(pair_ab["damaged_sets"][idx])
                        pair_ba_d = set(pair_ba["damaged_sets"][idx])
                        union_jaccards.append(v15b.jaccard(pair_ab_d, union_d))
                        order_jaccards.append(v15b.jaccard(pair_ab_d, pair_ba_d))
                        snapshot_steps.append(int(pair_ab["log_rows"][idx]["step"]))

                        control_graph_ab = pair_ab["control_graphs"][idx]
                        control_graph_ba = pair_ba["control_graphs"][idx]
                        control_consistency.append(v15b.edge_jaccard_graphs(control_graph_ab, control_graph_ba))

                        union_components, union_largest_frac = v15d.component_stats(control_graph_ab, union_d)
                        pair_components = int(pair_ab["log_rows"][idx]["damage_component_count"])
                        pair_largest_frac = safe_float(pair_ab["log_rows"][idx]["largest_component_fraction"])
                        pair_minus_union_components.append(float(pair_components - union_components))
                        pair_minus_union_largest_frac.append(float(pair_largest_frac - union_largest_frac))

                    min_idx = min(range(len(union_jaccards)), key=lambda i: union_jaccards[i])
                    final_idx = len(union_jaccards) - 1
                    row = {
                        "ensemble": ens.name,
                        "target_nodes": ens.target_nodes,
                        "growth_seed": int(gseed),
                        "run_offset": int(run_offset),
                        "run_seed": int(run_seed),
                        "pair_label": f"{placement_a}-{placement_b}",
                        "placement_a": placement_a,
                        "placement_b": placement_b,
                        "min_support_distance": int(pair_meta["min_support_distance"]),
                        "n_snapshots": n_snap,
                        "mean_control_consistency": mean_defined(control_consistency),
                        "mean_order_jaccard": mean_defined(order_jaccards),
                        "mean_union_jaccard": mean_defined(union_jaccards),
                        "min_union_jaccard": union_jaccards[min_idx],
                        "min_union_step": snapshot_steps[min_idx],
                        "min_union_index_fraction": min_idx / max(1, final_idx),
                        "window_pair_minus_union_components": pair_minus_union_components[min_idx],
                        "window_pair_minus_union_largest_frac": pair_minus_union_largest_frac[min_idx],
                        "final_union_jaccard": union_jaccards[final_idx],
                        "final_pair_minus_union_components": pair_minus_union_components[final_idx],
                        "final_pair_minus_union_largest_frac": pair_minus_union_largest_frac[final_idx],
                        "pair_ab_mean_radius": safe_float(pair_ab["summary"]["mean_radius_control"]),
                        "pair_ba_mean_radius": safe_float(pair_ba["summary"]["mean_radius_control"]),
                    }
                    row["window_class"] = v15d.classify_window(row)
                    rows.append(row)
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: MutableMapping[str, List[Dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(str(row["pair_label"]), []).append(dict(row))

    out: List[Dict[str, Any]] = []
    for pair_label, grows in sorted(groups.items()):
        counts: Dict[str, int] = {}
        for row in grows:
            counts[str(row["window_class"])] = counts.get(str(row["window_class"]), 0) + 1
        out.append(
            {
                "pair_label": pair_label,
                "n_runs": len(grows),
                "mean_min_union_jaccard": mean_defined(safe_float(r["min_union_jaccard"]) for r in grows),
                "mean_final_union_jaccard": mean_defined(safe_float(r["final_union_jaccard"]) for r in grows),
                "mean_window_pair_minus_union_components": mean_defined(safe_float(r["window_pair_minus_union_components"]) for r in grows),
                "mean_final_pair_minus_union_components": mean_defined(safe_float(r["final_pair_minus_union_components"]) for r in grows),
                "binding_rate": counts.get("persistent_binding_tendency", 0) / max(1, len(grows)),
                "fragment_rate": counts.get("persistent_fragmentation_tendency", 0) / max(1, len(grows)),
                "compress_then_split_rate": counts.get("compress_then_split", 0) / max(1, len(grows)),
                "mixed_rate": counts.get("mixed_window", 0) / max(1, len(grows)),
                "dominant_window_class": max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0],
            }
        )
    return out


def recommendation_rows(target_summary: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    control_clean = min((safe_float(r["mean_control_consistency"]) for r in rows), default=1.0) >= 0.95
    out: List[Dict[str, Any]] = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and control_clean) else "unclear",
            "note": (
                "Startstørrelsene er separert og matched AB/BA-control holder seg samkjørt i den smale 48-runden."
                if (size_clean and control_clean)
                else "Enten størrelsesseparasjonen eller matched control er uklar i den smale 48-runden."
            ),
        }
    ]

    pair23 = next((row for row in aggregate if row["pair_label"] == "2-3"), None)
    pair34 = next((row for row in aggregate if row["pair_label"] == "3-4"), None)

    if pair23 and pair34:
        if safe_float(pair23["compress_then_split_rate"]) >= 0.40 and safe_float(pair34["binding_rate"]) >= 0.40:
            status = "pair_families_separate"
            note = (
                "Pair `2-3` heller mot `compress_then_split`, mens pair `3-4` heller mot binding-lignende vindu i den smale 48-runden."
            )
            next_status = "follow_pair_families"
            next_note = "Neste steg bør følge de to pair-familiene separat med lengre horisont eller enda tettere snapshots."
        else:
            status = "pair_families_still_mixed"
            note = (
                f"`2-3` og `3-4` er fortsatt blandet (2-3 compress_then_split {safe_float(pair23['compress_then_split_rate']):.3f}, 3-4 binding {safe_float(pair34['binding_rate']):.3f})."
            )
            next_status = "increase_per_pair_budget"
            next_note = "Neste steg bør være mer budsjett per pair eller enda færre, men mer kontrollerte run-seeds."
    else:
        status = "pair_selection_incomplete"
        note = "En eller begge de planlagte 48-pair-familiene manglet gyldig lokal støtte i denne runden."
        next_status = "repair_pair_selection"
        next_note = "Neste steg bør være å verifisere eller utvide de smale pair-kandidatene."

    out.append({"diagnostic_family": "pair_family_signal", "status": status, "note": note})
    out.append({"diagnostic_family": "next_step", "status": next_status, "note": next_note})
    return out


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def build_report(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], recommendation: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15e: pair family refinement")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden bruker bare de to mest informative 48-pairene fra v0.15d og bruker mer budsjett per pair for å se om de faktisk heller mot ulike interaksjonsvinduer.")
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |")
    lines.append("")
    lines.append("## Pair aggregates")
    lines.append("")
    lines.append("| pair | n | min union j | final union j | window comp delta | final comp delta | binding | compress_then_split | mixed | dominant |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['pair_label']} | {int(row['n_runs'])} | {fmt(row['mean_min_union_jaccard'])} | {fmt(row['mean_final_union_jaccard'])} | {fmt(row['mean_window_pair_minus_union_components'])} | {fmt(row['mean_final_pair_minus_union_components'])} | {fmt(row['binding_rate'])} | {fmt(row['compress_then_split_rate'])} | {fmt(row['mixed_rate'])} | {row['dominant_window_class']} |"
        )
    lines.append("")
    lines.append("## Run-level diagnostics")
    lines.append("")
    lines.append("| pair | growth | offset | min union j | min step | window comp delta | final comp delta | class |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {row['pair_label']} | {int(row['growth_seed'])} | {int(row['run_offset'])} | {fmt(row['min_union_jaccard'])} | {int(row['min_union_step'])} | {fmt(row['window_pair_minus_union_components'])} | {fmt(row['final_pair_minus_union_components'])} | {row['window_class']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    return "\n".join(lines)


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    signal = next((row for row in recommendation if row["diagnostic_family"] == "pair_family_signal"), None)
    nxt = next((row for row in recommendation if row["diagnostic_family"] == "next_step"), None)
    return "\n".join(
        [
            "# Relasjonell universgraf v0.15e for ikke-spesialister",
            "",
            "Denne runden tok bare de to mest interessante lokale defect-parene og brukte mer målebudsjett på dem.",
            "",
            f"Hoveddommen er `{signal['status'] if signal else 'ukjent'}`.",
            "",
            f"Det betyr: {signal['note'] if signal else 'ingen oppsummering tilgjengelig.'}",
            "",
            f"Neste anbefaling er: {nxt['note'] if nxt else 'ingen ny anbefaling registrert.'}",
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15e pair family refinement.")
    p.add_argument("--growth-seeds", type=str, default="101,202")
    p.add_argument("--run-offsets", type=str, default="0,5,11,17,23,29")
    p.add_argument("--out-run-csv", type=str, default="Documentation/v15e_pair_family_rows.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15e_pair_family_target_summary.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15e_pair_family_aggregate.csv")
    p.add_argument("--out-recommendation-csv", type=str, default="Documentation/v15e_pair_family_recommendations.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15e_pair_family_refinement.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15e.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15e_operativ_anbefaling.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    growth_seeds = parse_int_list(args.growth_seeds)
    run_offsets = parse_int_list(args.run_offsets)

    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15b.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)

    rows = collect_rows(ensembles, base_states, growth_seeds, run_offsets)
    aggregate = aggregate_rows(rows)
    recommendation = recommendation_rows(target_summary, aggregate, rows)

    report_md = build_report(target_summary, rows, aggregate, recommendation)
    lay_md = build_lay_summary(recommendation)
    op_md = "\n".join(
        [
            "# v0.15e operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Ikke les denne runden som bevis på partikler eller scattering-lov.",
            "- Les den som en smal test av om to konkrete 48-pair-familier faktisk peker mot ulike interaksjonstyper.",
        ]
    )

    write_csv(args.out_run_csv, rows)
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_recommendation_csv, recommendation)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")

    print(f"Wrote {args.out_summary_md}")
    print(f"Wrote {args.out_run_csv}")
    print(f"Wrote {args.out_aggregate_csv}")


if __name__ == "__main__":
    main()
