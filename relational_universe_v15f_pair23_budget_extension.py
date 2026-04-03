#!/usr/bin/env python3
"""v0.15f deeper budget on the 48-node pair 2-3 family.

This follows v0.15e. The pair-family picture stayed mixed, but pair 2-3
remained the most plausible candidate for a specific window type. This round
does not widen the search. It only asks:

If we spend more budget on pair 2-3 in the 48-node corridor, does
`compress_then_split` become a stable family reading, or does the result stay
mixed?
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Set, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15b_add_chord_collision_lab as v15b
import relational_universe_v15d_collision_window_lab as v15d
import relational_universe_v15e_pair_family_refinement as v15e


TARGET = 48
PAIR = (2, 3)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15b.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15b.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    return v15b.write_csv(path, rows)


def parse_int_list(spec: str) -> List[int]:
    return [int(part.strip()) for part in spec.split(",") if part.strip()]


def extra_dense_log_every(steps: int) -> int:
    return max(1, min(8, steps // 240))


def pair_meta(base_state: Any) -> Optional[Dict[str, Any]]:
    return v15e.pair_is_valid(base_state, PAIR[0], PAIR[1])


def collect_rows(
    ensembles: Sequence[Any],
    base_states: Mapping[Tuple[str, int], Any],
    growth_seeds: Sequence[int],
    run_offsets: Sequence[int],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    rows: List[Dict[str, Any]] = []
    availability: List[Dict[str, Any]] = []
    spec = v15b.anchor_spec()
    params = v15b.v09.candidate_to_params(spec["candidate"])

    for ens in ensembles:
        if int(ens.target_nodes) != TARGET:
            continue
        for gseed in growth_seeds:
            base = base_states[(ens.name, int(gseed))]
            meta = pair_meta(base)
            availability.append(
                {
                    "ensemble": ens.name,
                    "target_nodes": ens.target_nodes,
                    "growth_seed": int(gseed),
                    "pair_label": f"{PAIR[0]}-{PAIR[1]}",
                    "pair_available": 1 if meta is not None else 0,
                    "min_support_distance": int(meta["min_support_distance"]) if meta is not None else -1,
                }
            )
            if meta is None:
                continue

            steps = v15b.collision_steps_for_state(base.g.num_nodes())
            log_every = extra_dense_log_every(steps)
            pair = (PAIR[0], PAIR[1])
            reversed_pair = (PAIR[1], PAIR[0])

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
                    "pair_label": f"{PAIR[0]}-{PAIR[1]}",
                    "min_support_distance": int(meta["min_support_distance"]),
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
    return rows, availability


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[str(row["window_class"])] = counts.get(str(row["window_class"]), 0) + 1
    total = max(1, len(rows))
    return [
        {
            "pair_label": f"{PAIR[0]}-{PAIR[1]}",
            "n_runs": len(rows),
            "mean_min_union_jaccard": mean_defined(safe_float(r["min_union_jaccard"]) for r in rows),
            "mean_final_union_jaccard": mean_defined(safe_float(r["final_union_jaccard"]) for r in rows),
            "mean_window_pair_minus_union_components": mean_defined(safe_float(r["window_pair_minus_union_components"]) for r in rows),
            "mean_final_pair_minus_union_components": mean_defined(safe_float(r["final_pair_minus_union_components"]) for r in rows),
            "compress_then_split_rate": counts.get("compress_then_split", 0) / total,
            "split_then_bind_rate": counts.get("split_then_bind", 0) / total,
            "binding_rate": counts.get("persistent_binding_tendency", 0) / total,
            "fragment_rate": counts.get("persistent_fragmentation_tendency", 0) / total,
            "mixed_rate": counts.get("mixed_window", 0) / total,
            "dominant_window_class": max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0] if counts else "none",
        }
    ]


def recommendation_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], availability: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    control_clean = min((safe_float(r["mean_control_consistency"]) for r in rows), default=1.0) >= 0.95
    available_rate = mean_defined(float(r["pair_available"]) for r in availability)
    agg = aggregate[0] if aggregate else {}

    out: List[Dict[str, Any]] = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and control_clean and available_rate >= 0.999) else "unclear",
            "note": (
                "Startstørrelsene er separert, pair 2-3 er faktisk tilgjengelig i denne smale runden, og matched AB/BA-control holder seg samkjørt."
                if (size_clean and control_clean and available_rate >= 0.999)
                else "Enten størrelsesseparasjonen, pair-tilgjengeligheten eller matched control er uklar i den smale 2-3-runden."
            ),
        }
    ]

    cts = safe_float(agg.get("compress_then_split_rate", 0.0))
    stb = safe_float(agg.get("split_then_bind_rate", 0.0))
    bind = safe_float(agg.get("binding_rate", 0.0))
    mixed = safe_float(agg.get("mixed_rate", 1.0))

    if cts >= 0.50 and mixed <= 0.40:
        status = "compress_then_split_supported"
        note = f"Mer budsjett på pair 2-3 gjør `compress_then_split` til den klare hovedlesningen ({cts:.3f})."
        next_status = "follow_pair23_family"
        next_note = "Neste steg bør være å følge 2-3-familien lengre i tid og se om den senere stabiliserer en sekundær split-struktur."
    elif cts > stb and cts > bind:
        status = "compress_then_split_leading_but_mixed"
        note = f"`compress_then_split` leder for pair 2-3 ({cts:.3f}), men mixed-andelen er fortsatt for høy ({mixed:.3f}) til en ren dom."
        next_status = "increase_budget_or_fix_base"
        next_note = "Neste steg bør være enda mer budsjett på samme base eller en enda strammere seed-familie rundt de run-offsettene som støttet signalet."
    else:
        status = "pair23_still_mixed"
        note = f"Pair 2-3 er fortsatt blandet (compress_then_split {cts:.3f}, split_then_bind {stb:.3f}, binding {bind:.3f}, mixed {mixed:.3f})."
        next_status = "pause_or_reframe"
        next_note = "Neste steg bør være å enten stoppe denne mikroraffineringen eller skifte til lengre defect-følging i stedet for flere møtevindusrunder."

    out.append({"diagnostic_family": "pair23_signal", "status": status, "note": note})
    out.append({"diagnostic_family": "next_step", "status": next_status, "note": next_note})
    return out


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def build_report(
    target_summary: Sequence[Dict[str, Any]],
    rows: Sequence[Dict[str, Any]],
    availability: Sequence[Dict[str, Any]],
    aggregate: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15f: pair 2-3 budget extension")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden bruker ekstra budsjett på bare pair 2-3 i 48-korridoren for å se om `compress_then_split` blir en stabil familielesning.")
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |")
    lines.append("")
    lines.append("## Pair availability")
    lines.append("")
    lines.append("| growth | pair available | min support distance |")
    lines.append("| --- | --- | --- |")
    for row in availability:
        lines.append(f"| {int(row['growth_seed'])} | {int(row['pair_available'])} | {int(row['min_support_distance'])} |")
    lines.append("")
    lines.append("## Aggregate")
    lines.append("")
    lines.append("| pair | n | min union j | final union j | window comp delta | final comp delta | compress_then_split | split_then_bind | binding | mixed | dominant |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['pair_label']} | {int(row['n_runs'])} | {fmt(row['mean_min_union_jaccard'])} | {fmt(row['mean_final_union_jaccard'])} | {fmt(row['mean_window_pair_minus_union_components'])} | {fmt(row['mean_final_pair_minus_union_components'])} | {fmt(row['compress_then_split_rate'])} | {fmt(row['split_then_bind_rate'])} | {fmt(row['binding_rate'])} | {fmt(row['mixed_rate'])} | {row['dominant_window_class']} |"
        )
    lines.append("")
    lines.append("## Run-level diagnostics")
    lines.append("")
    lines.append("| offset | min union j | min step | window comp delta | final comp delta | class |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {int(row['run_offset'])} | {fmt(row['min_union_jaccard'])} | {int(row['min_union_step'])} | {fmt(row['window_pair_minus_union_components'])} | {fmt(row['final_pair_minus_union_components'])} | {row['window_class']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    return "\n".join(lines)


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    signal = next((row for row in recommendation if row["diagnostic_family"] == "pair23_signal"), None)
    nxt = next((row for row in recommendation if row["diagnostic_family"] == "next_step"), None)
    return "\n".join(
        [
            "# Relasjonell universgraf v0.15f for ikke-spesialister",
            "",
            "Denne runden brukte ekstra målebudsjett på ett bestemt lokalt defect-par for å se om mønsteret ble tydeligere.",
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
    p = argparse.ArgumentParser(description="v0.15f pair 2-3 budget extension.")
    p.add_argument("--growth-seeds", type=str, default="101")
    p.add_argument("--run-offsets", type=str, default="0,2,5,8,11,14,17,20,23,26,29,32,35,38,41,44")
    p.add_argument("--out-run-csv", type=str, default="Documentation/v15f_pair23_rows.csv")
    p.add_argument("--out-availability-csv", type=str, default="Documentation/v15f_pair23_availability.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15f_pair23_target_summary.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15f_pair23_aggregate.csv")
    p.add_argument("--out-recommendation-csv", type=str, default="Documentation/v15f_pair23_recommendations.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15f_pair23_budget_extension.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15f.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15f_operativ_anbefaling.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    growth_seeds = parse_int_list(args.growth_seeds)
    run_offsets = parse_int_list(args.run_offsets)

    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15b.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)

    rows, availability = collect_rows(ensembles, base_states, growth_seeds, run_offsets)
    aggregate = aggregate_rows(rows)
    recommendation = recommendation_rows(target_summary, rows, availability, aggregate)

    report_md = build_report(target_summary, rows, availability, aggregate, recommendation)
    lay_md = build_lay_summary(recommendation)
    op_md = "\n".join(
        [
            "# v0.15f operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Ikke les denne runden som bevis på partikler eller scattering-lov.",
            "- Les den som en smal test av om pair 2-3 faktisk stabiliserer ett tydelig møtevindusmønster under mer budsjett.",
        ]
    )

    write_csv(args.out_run_csv, rows)
    write_csv(args.out_availability_csv, availability)
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
