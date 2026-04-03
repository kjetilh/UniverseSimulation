#!/usr/bin/env python3
"""v0.15d collision window lab for add_chord defects.

This follows v0.15c. The collision signal is real, but the type remains mixed.
The next narrow step is to resolve the interaction window more directly:

- keep the same artifact-aware matched-run setup
- focus on the most informative lower-size corridor
- log more densely
- compare pair-vs-union structure at the strongest interaction time

This is a windowed diagnostic, not a new broad search.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Set, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15b_add_chord_collision_lab as v15b


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15b.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15b.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    return v15b.write_csv(path, rows)


def parse_int_list(spec: str) -> List[int]:
    return [int(part.strip()) for part in spec.split(",") if part.strip()]


def component_stats(g: Any, damaged: Set[int]) -> Tuple[int, float]:
    comps = v15.damaged_components(g, damaged)
    damaged_count = len(damaged)
    largest = max((len(comp) for comp in comps), default=0)
    frac = (largest / damaged_count) if damaged_count > 0 else 0.0
    return len(comps), float(frac)


def dense_log_every(steps: int) -> int:
    return max(4, min(20, steps // 90))


def classify_window(row: Mapping[str, Any]) -> str:
    control = safe_float(row["mean_control_consistency"])
    min_union_j = safe_float(row["min_union_jaccard"])
    min_idx_frac = safe_float(row["min_union_index_fraction"])
    final_delta_comp = safe_float(row["final_pair_minus_union_components"])
    min_delta_comp = safe_float(row["window_pair_minus_union_components"])
    final_delta_largest = safe_float(row["final_pair_minus_union_largest_frac"])
    min_delta_largest = safe_float(row["window_pair_minus_union_largest_frac"])

    if control < 0.95:
        return "artifact_risk"
    if min_idx_frac <= 0.10 or min_idx_frac >= 0.90:
        return "boundary_window"
    if min_union_j >= 0.75:
        return "weak_window"
    if min_delta_comp <= -2.0 and final_delta_comp <= -1.0 and min_delta_largest >= 0.10 and final_delta_largest >= 0.10:
        return "persistent_binding_tendency"
    if min_delta_comp >= 2.0 and final_delta_comp >= 1.0 and min_delta_largest <= -0.10 and final_delta_largest <= -0.10:
        return "persistent_fragmentation_tendency"
    if min_delta_comp <= -2.0 and final_delta_comp >= 1.0:
        return "compress_then_split"
    if min_delta_comp >= 2.0 and final_delta_comp <= -1.0:
        return "split_then_bind"
    return "mixed_window"


def collect_window_rows(
    ensembles: Sequence[Any],
    base_states: Mapping[Tuple[str, int], Any],
    growth_seeds: Sequence[int],
    run_offsets: Sequence[int],
    placement_count: int,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    spec = v15b.anchor_spec()
    params = v15b.v09.candidate_to_params(spec["candidate"])

    for ens in ensembles:
        for gseed in growth_seeds:
            base = base_states[(ens.name, int(gseed))]
            chosen = v15b.choose_collision_pair(base, placement_count)
            if chosen is None:
                continue
            pair = (int(chosen["placement_a"]), int(chosen["placement_b"]))
            reversed_pair = (pair[1], pair[0])
            steps = v15b.collision_steps_for_state(base.g.num_nodes())
            log_every = dense_log_every(steps)
            initial_nodes = max(1.0, safe_float(v15b.v7.feature_row(base).get("nodes")))

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

                    union_components, union_largest_frac = component_stats(control_graph_ab, union_d)
                    pair_components = int(pair_ab["log_rows"][idx]["damage_component_count"])
                    pair_largest_frac = safe_float(pair_ab["log_rows"][idx]["largest_component_fraction"])
                    pair_minus_union_components.append(float(pair_components - union_components))
                    pair_minus_union_largest_frac.append(float(pair_largest_frac - union_largest_frac))

                min_idx = min(range(len(union_jaccards)), key=lambda i: union_jaccards[i])
                final_idx = len(union_jaccards) - 1
                final_union_damage_fraction = len(set(single_a["damaged_sets"][final_idx]).union(single_b["damaged_sets"][final_idx])) / initial_nodes
                final_pair_damage_fraction = len(set(pair_ab["damaged_sets"][final_idx])) / initial_nodes

                row = {
                    "ensemble": ens.name,
                    "target_nodes": ens.target_nodes,
                    "growth_seed": int(gseed),
                    "run_offset": int(run_offset),
                    "run_seed": int(run_seed),
                    "placement_a": pair[0],
                    "placement_b": pair[1],
                    "min_support_distance": int(chosen["min_support_distance"]),
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
                    "final_pair_damage_fraction": final_pair_damage_fraction,
                    "final_union_damage_fraction": final_union_damage_fraction,
                    "pair_ab_mean_radius": safe_float(pair_ab["summary"]["mean_radius_control"]),
                    "pair_ba_mean_radius": safe_float(pair_ba["summary"]["mean_radius_control"]),
                }
                row["window_class"] = classify_window(row)
                rows.append(row)
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: MutableMapping[str, List[Dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(str(row["window_class"]), []).append(dict(row))

    out: List[Dict[str, Any]] = []
    for window_class, grows in sorted(groups.items()):
        out.append(
            {
                "window_class": window_class,
                "n_runs": len(grows),
                "mean_min_union_jaccard": mean_defined(safe_float(r["min_union_jaccard"]) for r in grows),
                "mean_final_union_jaccard": mean_defined(safe_float(r["final_union_jaccard"]) for r in grows),
                "mean_window_pair_minus_union_components": mean_defined(safe_float(r["window_pair_minus_union_components"]) for r in grows),
                "mean_final_pair_minus_union_components": mean_defined(safe_float(r["final_pair_minus_union_components"]) for r in grows),
                "mean_window_pair_minus_union_largest_frac": mean_defined(safe_float(r["window_pair_minus_union_largest_frac"]) for r in grows),
                "mean_final_pair_minus_union_largest_frac": mean_defined(safe_float(r["final_pair_minus_union_largest_frac"]) for r in grows),
                "mean_min_union_index_fraction": mean_defined(safe_float(r["min_union_index_fraction"]) for r in grows),
            }
        )
    return out


def recommendation_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    control_clean = min((safe_float(r["mean_control_consistency"]) for r in rows), default=1.0) >= 0.95
    out: List[Dict[str, Any]] = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and control_clean) else "unclear",
            "note": (
                "Startstørrelsene er separert og matched AB/BA-control holder seg samkjørt også i den tettere møtesporingen."
                if (size_clean and control_clean)
                else "Enten størrelsesseparasjonen eller matched control er uklar i den tettere møtesporingen."
            ),
        }
    ]

    total = max(1, len(rows))
    rates = {
        key: sum(1 for r in rows if str(r["window_class"]) == key) / total
        for key in (
            "persistent_binding_tendency",
            "persistent_fragmentation_tendency",
            "compress_then_split",
            "split_then_bind",
            "mixed_window",
            "boundary_window",
            "weak_window",
            "artifact_risk",
        )
    }

    if rates["artifact_risk"] > 0.10:
        status = "artifact_risk"
        note = f"For mange rader er fortsatt metodisk uklare (`artifact_risk` {rates['artifact_risk']:.3f})."
        next_status = "tighten_control_further"
        next_note = "Neste steg bør være enda strengere kontroll eller kortere matched-vindu."
    elif rates["persistent_fragmentation_tendency"] >= 0.50:
        status = "fragmentation_window_dominant"
        note = f"Det tette møtevinduet peker oftest mot vedvarende ekstra fragmentering (`persistent_fragmentation_tendency` {rates['persistent_fragmentation_tendency']:.3f})."
        next_status = "follow_fragmentation_family"
        next_note = "Neste steg bør spore om ekstra komponenter stabiliserer seg eller fortsetter å splitte videre."
    elif rates["persistent_binding_tendency"] >= 0.50:
        status = "binding_window_dominant"
        note = f"Det tette møtevinduet peker oftest mot varig samling i færre komponenter (`persistent_binding_tendency` {rates['persistent_binding_tendency']:.3f})."
        next_status = "follow_binding_family"
        next_note = "Neste steg bør være lengre horisont for å se om de færre komponentene holder seg samlet."
    elif rates["compress_then_split"] >= 0.40:
        status = "compress_then_split_signal"
        note = f"Det tette møtevinduet peker ofte mot kompresjon ved møtet og senere ny splitting (`compress_then_split` {rates['compress_then_split']:.3f})."
        next_status = "trace_mid_window_morphology"
        next_note = "Neste steg bør være enda tettere morfologisporing gjennom møte- og ettervinduet."
    else:
        status = "mixed_window_family"
        note = (
            f"Møtevinduet er fortsatt blandet (`persistent_fragmentation_tendency` {rates['persistent_fragmentation_tendency']:.3f}, "
            f"`persistent_binding_tendency` {rates['persistent_binding_tendency']:.3f}, "
            f"`compress_then_split` {rates['compress_then_split']:.3f}, `mixed_window` {rates['mixed_window']:.3f})."
        )
        next_status = "narrow_pair_selection"
        next_note = "Neste steg bør være enda smalere pair-selection eller flere snapshots rundt møtet i én liten størrelseskorridor."

    out.append({"diagnostic_family": "collision_window_signal", "status": status, "note": note})
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
    aggregate: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15d: collision window lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden går smalere enn v0.15c og ser på selve interaksjonsvinduet der pair-runen avviker mest fra unionen av matched single-runs."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Window classes")
    lines.append("")
    lines.append("| class | n | min union j | final union j | window comp delta | final comp delta | window largest delta | final largest delta | min index frac |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['window_class']} | {int(row['n_runs'])} | {fmt(row['mean_min_union_jaccard'])} | {fmt(row['mean_final_union_jaccard'])} | {fmt(row['mean_window_pair_minus_union_components'])} | {fmt(row['mean_final_pair_minus_union_components'])} | {fmt(row['mean_window_pair_minus_union_largest_frac'])} | {fmt(row['mean_final_pair_minus_union_largest_frac'])} | {fmt(row['mean_min_union_index_fraction'])} |"
        )
    lines.append("")
    lines.append("## Run-level window diagnostics")
    lines.append("")
    lines.append("| target | pair | dist | min union j | min step | min idx frac | window comp delta | final comp delta | window largest delta | final largest delta | class |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {int(row['target_nodes'])} | {int(row['placement_a'])}-{int(row['placement_b'])} | {int(row['min_support_distance'])} | {fmt(row['min_union_jaccard'])} | {int(row['min_union_step'])} | {fmt(row['min_union_index_fraction'])} | {fmt(row['window_pair_minus_union_components'])} | {fmt(row['final_pair_minus_union_components'])} | {fmt(row['window_pair_minus_union_largest_frac'])} | {fmt(row['final_pair_minus_union_largest_frac'])} | {row['window_class']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Heuristiske møtevindusklasser")
    lines.append("")
    lines.append("- `persistent_binding_tendency`: pair-run ligger under unionen i komponenttall både i møtevinduet og ved slutten.")
    lines.append("- `persistent_fragmentation_tendency`: pair-run ligger over unionen i komponenttall både i møtevinduet og ved slutten.")
    lines.append("- `compress_then_split`: pair-run komprimerer ved møtet, men ender senere mer fragmentert.")
    lines.append("- `split_then_bind`: pair-run splitter først, men ender senere mer samlet.")
    lines.append("- `mixed_window`: interaksjonsvinduet er reelt, men ikke skarpt nok til én type.")
    lines.append("")
    return "\n".join(lines)


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    signal = next((row for row in recommendation if row["diagnostic_family"] == "collision_window_signal"), None)
    nxt = next((row for row in recommendation if row["diagnostic_family"] == "next_step"), None)
    return "\n".join(
        [
            "# Relasjonell universgraf v0.15d for ikke-spesialister",
            "",
            "Denne runden så tettere på selve øyeblikket der to lokale defects ser ut til å påvirke hverandre mest.",
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
    p = argparse.ArgumentParser(description="v0.15d collision window lab.")
    p.add_argument("--targets", type=str, default="48,96")
    p.add_argument("--growth-seeds", type=str, default="101,202")
    p.add_argument("--run-offsets", type=str, default="0,17")
    p.add_argument("--placement-count", type=int, default=6)
    p.add_argument("--out-run-csv", type=str, default="Documentation/v15d_collision_window_rows.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15d_collision_window_target_summary.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15d_collision_window_aggregate.csv")
    p.add_argument("--out-recommendation-csv", type=str, default="Documentation/v15d_collision_window_recommendations.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15d_collision_window_lab.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15d.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15d_operativ_anbefaling.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    targets = parse_int_list(args.targets)
    growth_seeds = parse_int_list(args.growth_seeds)
    run_offsets = parse_int_list(args.run_offsets)

    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15b.deep_ensembles(targets)
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)

    rows = collect_window_rows(ensembles, base_states, growth_seeds, run_offsets, args.placement_count)
    aggregate = aggregate_rows(rows)
    recommendation = recommendation_rows(target_summary, rows)

    report_md = build_report(target_summary, rows, aggregate, recommendation)
    lay_md = build_lay_summary(recommendation)
    op_md = "\n".join(
        [
            "# v0.15d operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Ikke les denne runden som bevis på partikler eller scattering-lov.",
            "- Les den som en smal møtevindusdiagnostikk av hvordan pair-runen avviker fra unionen av matched single-runs.",
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
