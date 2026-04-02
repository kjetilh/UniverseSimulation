#!/usr/bin/env python3
"""v0.15c collision-type lab for add_chord defects.

This follows v0.15b, where separated paired add_chord runs deviated clearly
from the union of matched single-defect runs under clean controls.

The next question is narrower:
what kind of deviation are we seeing?

This script keeps the same artifact-aware matched-run setup and assigns
heuristic interaction classes such as:
- near_superposition
- annihilation_like
- binding_like
- secondary_split_like
- pass_through_like
- mixed_collision

These are operational labels, not particle claims.
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


def classify_collision(metrics: Mapping[str, Any]) -> str:
    control_consistency = safe_float(metrics["mean_control_consistency"])
    mean_union_j = safe_float(metrics["mean_union_jaccard"])
    min_union_j = safe_float(metrics["min_union_jaccard"])
    final_union_j = safe_float(metrics["final_union_jaccard"])
    final_order_j = safe_float(metrics["final_order_jaccard"])
    final_pair_damage = safe_float(metrics["final_pair_damage_fraction"])
    final_union_damage = safe_float(metrics["final_union_damage_fraction"])
    final_pair_comp = int(metrics["final_pair_component_count"])
    final_union_comp = int(metrics["final_union_component_count"])
    final_pair_largest = safe_float(metrics["final_pair_largest_component_fraction"])
    final_union_largest = safe_float(metrics["final_union_largest_component_fraction"])
    final_pair_alive = int(metrics["final_pair_alive"])

    if control_consistency < 0.95:
        return "artifact_risk"
    if mean_union_j >= 0.85 and final_union_j >= 0.90:
        return "near_superposition"
    if (
        final_union_damage > 0.0
        and final_pair_damage <= 0.50 * final_union_damage
        and final_union_j <= 0.70
    ):
        return "annihilation_like"
    if (
        final_pair_comp <= max(1, final_union_comp - 1)
        and final_pair_largest >= min(1.0, final_union_largest + 0.15)
        and final_union_j <= 0.75
    ):
        return "binding_like"
    if (
        final_pair_comp >= final_union_comp + 1
        and final_pair_largest <= max(0.0, final_union_largest - 0.15)
        and final_union_j <= 0.75
    ):
        return "secondary_split_like"
    if min_union_j <= 0.70 and final_union_j >= 0.80 and final_order_j >= 0.85:
        return "pass_through_like"
    if final_pair_alive == 0 and final_union_j <= 0.75:
        return "annihilation_like"
    return "mixed_collision"


def collect_collision_rows(
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
            log_every = max(12, min(80, steps // 24))
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
                final_union_damage_fraction = 0.0
                final_pair_damage_fraction = 0.0
                final_union_components = 0
                final_pair_components = 0
                final_union_largest_fraction = 0.0
                final_pair_largest_fraction = 0.0
                final_pair_alive = 0

                for idx in range(n_snap):
                    union_d = set(single_a["damaged_sets"][idx]).union(single_b["damaged_sets"][idx])
                    pair_ab_d = set(pair_ab["damaged_sets"][idx])
                    pair_ba_d = set(pair_ba["damaged_sets"][idx])
                    union_jaccards.append(v15b.jaccard(pair_ab_d, union_d))
                    order_jaccards.append(v15b.jaccard(pair_ab_d, pair_ba_d))

                    control_graph_ab = pair_ab["control_graphs"][idx]
                    control_graph_ba = pair_ba["control_graphs"][idx]
                    control_consistency.append(v15b.edge_jaccard_graphs(control_graph_ab, control_graph_ba))

                    if idx == n_snap - 1:
                        final_union_damage_fraction = len(union_d) / initial_nodes
                        final_pair_damage_fraction = len(pair_ab_d) / initial_nodes
                        final_union_components, final_union_largest_fraction = component_stats(control_graph_ab, union_d)
                        final_pair_components = int(pair_ab["log_rows"][idx]["damage_component_count"])
                        final_pair_largest_fraction = safe_float(pair_ab["log_rows"][idx]["largest_component_fraction"])
                        final_pair_alive = int(pair_ab["log_rows"][idx]["alive"])

                metrics = {
                    "mean_union_jaccard": mean_defined(union_jaccards),
                    "min_union_jaccard": min(union_jaccards) if union_jaccards else float("nan"),
                    "final_union_jaccard": union_jaccards[-1] if union_jaccards else float("nan"),
                    "mean_order_jaccard": mean_defined(order_jaccards),
                    "final_order_jaccard": order_jaccards[-1] if order_jaccards else float("nan"),
                    "mean_control_consistency": mean_defined(control_consistency),
                    "final_union_damage_fraction": final_union_damage_fraction,
                    "final_pair_damage_fraction": final_pair_damage_fraction,
                    "final_union_component_count": final_union_components,
                    "final_pair_component_count": final_pair_components,
                    "final_union_largest_component_fraction": final_union_largest_fraction,
                    "final_pair_largest_component_fraction": final_pair_largest_fraction,
                    "final_pair_alive": final_pair_alive,
                    "single_a_mean_radius": safe_float(single_a["summary"]["mean_radius_control"]),
                    "single_b_mean_radius": safe_float(single_b["summary"]["mean_radius_control"]),
                    "pair_ab_mean_radius": safe_float(pair_ab["summary"]["mean_radius_control"]),
                    "pair_ba_mean_radius": safe_float(pair_ba["summary"]["mean_radius_control"]),
                }
                collision_class = classify_collision(metrics)
                rows.append(
                    {
                        "ensemble": ens.name,
                        "target_nodes": ens.target_nodes,
                        "growth_seed": int(gseed),
                        "run_offset": int(run_offset),
                        "run_seed": int(run_seed),
                        "placement_a": pair[0],
                        "placement_b": pair[1],
                        "min_support_distance": int(chosen["min_support_distance"]),
                        **metrics,
                        "collision_class": collision_class,
                    }
                )
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    class_groups: MutableMapping[str, List[Dict[str, Any]]] = {}
    for row in rows:
        class_groups.setdefault(str(row["collision_class"]), []).append(dict(row))

    out: List[Dict[str, Any]] = []
    for collision_class, grows in sorted(class_groups.items()):
        out.append(
            {
                "collision_class": collision_class,
                "n_runs": len(grows),
                "mean_union_jaccard": mean_defined(safe_float(r["mean_union_jaccard"]) for r in grows),
                "mean_final_union_jaccard": mean_defined(safe_float(r["final_union_jaccard"]) for r in grows),
                "mean_order_jaccard": mean_defined(safe_float(r["mean_order_jaccard"]) for r in grows),
                "mean_control_consistency": mean_defined(safe_float(r["mean_control_consistency"]) for r in grows),
                "mean_final_pair_damage_fraction": mean_defined(safe_float(r["final_pair_damage_fraction"]) for r in grows),
                "mean_final_union_damage_fraction": mean_defined(safe_float(r["final_union_damage_fraction"]) for r in grows),
                "mean_final_pair_component_count": mean_defined(safe_float(r["final_pair_component_count"]) for r in grows),
                "mean_final_union_component_count": mean_defined(safe_float(r["final_union_component_count"]) for r in grows),
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
                "Startstørrelsene er separert og matched control-grenene holder seg samkjørte på tvers av single/pair/AB/BA."
                if (size_clean and control_clean)
                else "Enten størrelsesseparasjonen eller matched control-konsistensen er uklar."
            ),
        }
    ]

    total = max(1, len(rows))
    rates = {
        key: sum(1 for r in rows if str(r["collision_class"]) == key) / total
        for key in (
            "near_superposition",
            "annihilation_like",
            "binding_like",
            "secondary_split_like",
            "pass_through_like",
            "mixed_collision",
            "artifact_risk",
        )
    }

    if rates["artifact_risk"] > 0.10:
        signal_status = "artifact_risk"
        signal_note = f"For mange rader er fortsatt analysemessig uklare (`artifact_risk` {rates['artifact_risk']:.3f})."
        next_status = "tighten_collision_setup"
        next_note = "Neste steg bør være enda strengere matched kontroll eller kortere diagnostiske vinduer."
    elif rates["secondary_split_like"] >= 0.50:
        signal_status = "secondary_split_dominant"
        signal_note = f"Parvise add_chord-defects ser oftest ut til å skape mer fragmentert sluttskade enn unionen av single-runs (`secondary_split_like` {rates['secondary_split_like']:.3f})."
        next_status = "test_secondary_split_family"
        next_note = "Neste steg bør være en direkte test av secondary split: flere snapshot-tider, komponentbaner og eventuell tredjepassasje."
    elif rates["binding_like"] >= 0.50:
        signal_status = "binding_like_dominant"
        signal_note = f"Parvise add_chord-defects ser oftest ut til å samle seg i færre/slankere sluttkomponenter enn unionen av single-runs (`binding_like` {rates['binding_like']:.3f})."
        next_status = "test_binding_family"
        next_note = "Neste steg bør være en direkte bindingstest med lengre horisont og mer eksplisitt komponentsporing."
    elif rates["annihilation_like"] >= 0.50:
        signal_status = "annihilation_like_dominant"
        signal_note = f"Parvise add_chord-defects dempes ofte kraftig relativt til unionen av single-runs (`annihilation_like` {rates['annihilation_like']:.3f})."
        next_status = "test_annihilation_family"
        next_note = "Neste steg bør være en mer direkte dempings-/annihilasjonstest med lengre levetidshorisont."
    elif rates["pass_through_like"] >= 0.50:
        signal_status = "pass_through_like_dominant"
        signal_note = f"Parvise add_chord-defects viser ofte midlertidig interaksjon men ender nær separert sluttgeometri (`pass_through_like` {rates['pass_through_like']:.3f})."
        next_status = "test_pass_through_family"
        next_note = "Neste steg bør være tettere snapshot-sporing rundt kollisjonstidspunktet."
    elif rates["near_superposition"] >= 0.50:
        signal_status = "mostly_superposed"
        signal_note = f"Selv etter v15b ser sluttklassifiseringen fortsatt mest ut som nær superposisjon (`near_superposition` {rates['near_superposition']:.3f})."
        next_status = "longer_horizon_before_collision"
        next_note = "Neste steg bør være lengre runder heller enn videre kollisjonsklassifisering."
    else:
        signal_status = "mixed_collision_family"
        signal_note = (
            f"Kollisjonsklassene splitter seg fortsatt (`secondary_split_like` {rates['secondary_split_like']:.3f}, "
            f"`binding_like` {rates['binding_like']:.3f}, `annihilation_like` {rates['annihilation_like']:.3f}, "
            f"`pass_through_like` {rates['pass_through_like']:.3f})."
        )
        next_status = "tighten_interaction_type"
        next_note = "Neste steg bør være en enda smalere interaksjonstest med flere snapshots og eksplisitt komponentsporing rundt møtet."

    out.append({"diagnostic_family": "collision_type_signal", "status": signal_status, "note": signal_note})
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
    lines.append("# Relasjonell universgraf v0.15c: collision type lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden følger opp v0.15b og prøver å klassifisere hvilken type interaksjon de parvise `add_chord`-defectene faktisk ser ut til å ha."
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
    lines.append("## Collision classes")
    lines.append("")
    lines.append("| class | n | mean union jaccard | final union jaccard | order jaccard | control consistency | pair damage | union damage | pair comps | union comps |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['collision_class']} | {int(row['n_runs'])} | {fmt(row['mean_union_jaccard'])} | {fmt(row['mean_final_union_jaccard'])} | {fmt(row['mean_order_jaccard'])} | {fmt(row['mean_control_consistency'])} | {fmt(row['mean_final_pair_damage_fraction'])} | {fmt(row['mean_final_union_damage_fraction'])} | {fmt(row['mean_final_pair_component_count'])} | {fmt(row['mean_final_union_component_count'])} |"
        )
    lines.append("")
    lines.append("## Run-level diagnostics")
    lines.append("")
    lines.append("| target | pair | dist | mean union j | final union j | final order j | control | pair dmg | union dmg | pair comps | union comps | class |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {int(row['target_nodes'])} | {int(row['placement_a'])}-{int(row['placement_b'])} | {int(row['min_support_distance'])} | {fmt(row['mean_union_jaccard'])} | {fmt(row['final_union_jaccard'])} | {fmt(row['final_order_jaccard'])} | {fmt(row['mean_control_consistency'])} | {fmt(row['final_pair_damage_fraction'])} | {fmt(row['final_union_damage_fraction'])} | {fmt(row['final_pair_component_count'])} | {fmt(row['final_union_component_count'])} | {row['collision_class']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Heuristiske klasser")
    lines.append("")
    lines.append("- `near_superposition`: pair-run ser nesten ut som unionen av single-runs også ved slutten.")
    lines.append("- `annihilation_like`: pair-run ender betydelig svakere enn unionen av single-runs.")
    lines.append("- `binding_like`: pair-run ender i færre og mer konsentrerte komponenter enn unionen.")
    lines.append("- `secondary_split_like`: pair-run ender i flere og mer fragmenterte komponenter enn unionen.")
    lines.append("- `pass_through_like`: pair-run avviker underveis, men ender nær separert sluttgeometri.")
    lines.append("- `mixed_collision`: det er et kollisjonssignal, men ikke en ren type ennå.")
    lines.append("")
    lines.append("Disse etikettene er diagnostiske arbeidsnavn, ikke bevis på fysiske partikkelklasser.")
    lines.append("")
    return "\n".join(lines)


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    signal = next((row for row in recommendation if row["diagnostic_family"] == "collision_type_signal"), None)
    nxt = next((row for row in recommendation if row["diagnostic_family"] == "next_step"), None)
    return "\n".join(
        [
            "# Relasjonell universgraf v0.15c for ikke-spesialister",
            "",
            "Denne runden prøvde ikke bare å se om to defects påvirker hverandre, men hvilken type påvirkning det ligner mest på.",
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
    p = argparse.ArgumentParser(description="v0.15c collision type lab.")
    p.add_argument("--targets", type=str, default="48,96,192,256")
    p.add_argument("--growth-seeds", type=str, default="101,202")
    p.add_argument("--run-offsets", type=str, default="0,17")
    p.add_argument("--placement-count", type=int, default=6)
    p.add_argument("--out-run-csv", type=str, default="Documentation/v15c_collision_type_rows.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15c_collision_type_target_summary.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15c_collision_type_aggregate.csv")
    p.add_argument("--out-recommendation-csv", type=str, default="Documentation/v15c_collision_type_recommendations.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15c_collision_type_lab.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15c.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15c_operativ_anbefaling.md")
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

    rows = collect_collision_rows(ensembles, base_states, growth_seeds, run_offsets, args.placement_count)
    aggregate = aggregate_rows(rows)
    recommendation = recommendation_rows(target_summary, rows)

    report_md = build_report(target_summary, rows, aggregate, recommendation)
    lay_md = build_lay_summary(recommendation)
    op_md = "\n".join(
        [
            "# v0.15c operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Ikke les denne runden som bevis på partikler eller scattering-lov.",
            "- Les den som en smal, artefaktbevisst klassifisering av hvilken type pair-run-avvik `add_chord` ser ut til å ha.",
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
