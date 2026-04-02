#!/usr/bin/env python3
"""v0.15b add_chord collision lab.

This follows v0.15, where `add_chord` was the clearest persistent-split family.
The question here is narrower:

If we seed two separated `add_chord` perturbations on the same base graph, does
the paired run behave roughly like the union of two matched single-defect runs,
or do we see consistent interaction / collision effects?

Methodological safeguards:
- same anchor regime: band_zero_del
- same deep size-separated bases
- same seed and same control branch for single and paired runs
- selected placement pairs must have disjoint initial supports
- run both orders (A then B, B then A) to expose order sensitivity artifacts
"""
from __future__ import annotations

import argparse
import math
import random
import statistics
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14_lorentz_diagnostics as v14
import relational_universe_v15_defect_lifetime_lab as v15


ANCHOR_NAME = v14.ANCHOR_CANDIDATE
PERTURBATION = "add_chord"


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v14.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v14.mean_defined(values)


def quantile(values: Sequence[float], q: float) -> float:
    return v14.quantile(values, q)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v10b.write_csv(path, rows)


def anchor_spec() -> Dict[str, Any]:
    return {
        "candidate": v09.ScaleCandidate(ANCHOR_NAME, 0.02, 0.00, 0.02, 0.00, 0.00),
        "candidate_role": "anchor",
    }


def deep_ensembles(targets: Sequence[int]) -> List[v10b.CalibrationEnsemble]:
    return [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]


def collision_steps_for_state(nodes: int) -> int:
    return max(420, min(1800, int(round(8.0 * nodes))))


def jaccard(a: Set[int], b: Set[int]) -> float:
    union = a.union(b)
    if not union:
        return 1.0
    return float(len(a.intersection(b)) / len(union))


def edge_jaccard_graphs(a: v7.UGraph, b: v7.UGraph) -> float:
    ea = a.edge_set()
    eb = b.edge_set()
    union = ea.union(eb)
    if not union:
        return 1.0
    return float(len(ea.intersection(eb)) / len(union))


def support_min_distance(g: v7.UGraph, a: Sequence[int], b: Sequence[int]) -> int:
    dist = v7.bfs_distances(g, a)
    vals = [dist[v] for v in b if v in dist]
    return min(vals) if vals else 999999


def discover_single_support(base_state: v7.State, placement: int) -> Optional[Dict[str, Any]]:
    trial = base_state.clone()
    info = v14.v08b.apply_custom_perturbation(trial, PERTURBATION, center_token_index=placement)
    actual = str(info.get("type", "unknown"))
    if not v14.perturbation_requested_match(PERTURBATION, actual):
        return None
    support = list(info.get("support", []))
    return {
        "placement_index": int(placement),
        "support": support,
        "support_signature": ",".join(str(x) for x in support),
        "support_size": len(support),
    }


def choose_collision_pair(base_state: v7.State, placement_count: int) -> Optional[Dict[str, Any]]:
    singles: List[Dict[str, Any]] = []
    token_count = max(1, len(base_state.sorted_token_ids()))
    for placement in range(min(token_count, placement_count)):
        info = discover_single_support(base_state, placement)
        if info is not None:
            singles.append(info)
    candidates: List[Dict[str, Any]] = []
    for i in range(len(singles)):
        for j in range(i + 1, len(singles)):
            a = singles[i]
            b = singles[j]
            sa = set(a["support"])
            sb = set(b["support"])
            if sa.intersection(sb):
                continue
            min_dist = support_min_distance(base_state.g, a["support"], b["support"])
            candidates.append(
                {
                    "placement_a": int(a["placement_index"]),
                    "placement_b": int(b["placement_index"]),
                    "support_a": list(a["support"]),
                    "support_b": list(b["support"]),
                    "min_support_distance": int(min_dist),
                    "combined_support_size": len(sa.union(sb)),
                }
            )
    if not candidates:
        return None
    candidates.sort(
        key=lambda row: (
            int(row["min_support_distance"]),
            int(row["combined_support_size"]),
            -abs(int(row["placement_b"]) - int(row["placement_a"])),
        ),
        reverse=True,
    )
    return candidates[0]


def run_sequence_from_base(
    base_state: v7.State,
    *,
    params: v7.Params,
    seed: int,
    steps: int,
    placements: Sequence[int],
    local_coupling: str = "maximal",
    log_every: int = 40,
) -> Dict[str, Any]:
    rng = random.Random(seed)
    control = base_state.clone()
    perturbed = base_state.clone()

    perturbations: List[Dict[str, Any]] = []
    support_union: Set[int] = set()
    for placement in placements:
        info = v14.v08b.apply_custom_perturbation(perturbed, PERTURBATION, center_token_index=int(placement))
        actual = str(info.get("type", "unknown"))
        support = list(info.get("support", []))
        perturbations.append(
            {
                "placement_index": int(placement),
                "actual_perturbation": actual,
                "requested_match": 1 if v14.perturbation_requested_match(PERTURBATION, actual) else 0,
                "support": support,
            }
        )
        support_union.update(support)

    next_node_id, next_token_id = v14.v08b.next_ids_from_state(base_state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)

    log_rows: List[Dict[str, Any]] = []
    damaged_sets: List[Set[int]] = []
    control_graphs: List[v7.UGraph] = []

    snap0, damaged0 = v15.defect_snapshot(control, perturbed, sorted(support_union))
    log_rows.append({"step": 0, "t": 0.0, **snap0})
    damaged_sets.append(set(damaged0))
    control_graphs.append(control.g.clone())

    initial_nodes = max(1.0, safe_float(v7.feature_row(base_state).get("nodes")))

    for step in range(1, steps + 1):
        v7.coupled_step(control, perturbed, manager, rng, params, local_coupling)
        if step % log_every == 0 or step == steps:
            snap, damaged = v15.defect_snapshot(control, perturbed, sorted(support_union))
            log_rows.append({"step": step, "t": control.t, **snap})
            damaged_sets.append(set(damaged))
            control_graphs.append(control.g.clone())

    final = log_rows[-1]
    summary = {
        "mean_damage_fraction": mean_defined(
            safe_float(row["damaged_nodes_count"]) / initial_nodes
            for row in log_rows
        ),
        "mean_radius_control": mean_defined(safe_float(row["radius_control"]) for row in log_rows if safe_float(row["radius_control"]) >= 0),
        "mean_component_count": mean_defined(safe_float(row["damage_component_count"]) for row in log_rows),
        "mean_largest_component_fraction": mean_defined(safe_float(row["largest_component_fraction"]) for row in log_rows),
        "mean_shape_stability": mean_defined(
            jaccard(a, b) for a, b in zip(damaged_sets, damaged_sets[1:])
        ),
        "final_alive": int(final["alive"]),
        "fit_speed_control": safe_float(v7.estimate_front_speed(log_rows, "t", "radius_control")["fit_slope"]),
    }
    return {
        "perturbations": perturbations,
        "support_union": sorted(support_union),
        "log_rows": log_rows,
        "damaged_sets": damaged_sets,
        "control_graphs": control_graphs,
        "summary": summary,
    }


def collect_run_rows(
    spec: Mapping[str, Any],
    ensembles: Sequence[v10b.CalibrationEnsemble],
    base_states: Mapping[Tuple[str, int], Any],
    growth_seeds: Sequence[int],
    run_offsets: Sequence[int],
    placement_count: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    pair_rows: List[Dict[str, Any]] = []
    interaction_rows: List[Dict[str, Any]] = []
    cand = spec["candidate"]
    params = v09.candidate_to_params(cand)

    for ens in ensembles:
        for gseed in growth_seeds:
            base = base_states[(ens.name, int(gseed))]
            chosen = choose_collision_pair(base, placement_count)
            if chosen is None:
                continue
            steps = collision_steps_for_state(base.g.num_nodes())
            log_every = max(12, min(80, steps // 24))
            pair = (int(chosen["placement_a"]), int(chosen["placement_b"]))
            reversed_pair = (pair[1], pair[0])
            for run_offset in run_offsets:
                run_seed = int(ens.target_nodes) * 100000 + int(gseed) * 1000 + int(run_offset)
                single_a = run_sequence_from_base(
                    base,
                    params=params,
                    seed=run_seed,
                    steps=steps,
                    placements=[pair[0]],
                    local_coupling="maximal",
                    log_every=log_every,
                )
                single_b = run_sequence_from_base(
                    base,
                    params=params,
                    seed=run_seed,
                    steps=steps,
                    placements=[pair[1]],
                    local_coupling="maximal",
                    log_every=log_every,
                )
                pair_ab = run_sequence_from_base(
                    base,
                    params=params,
                    seed=run_seed,
                    steps=steps,
                    placements=list(pair),
                    local_coupling="maximal",
                    log_every=log_every,
                )
                pair_ba = run_sequence_from_base(
                    base,
                    params=params,
                    seed=run_seed,
                    steps=steps,
                    placements=list(reversed_pair),
                    local_coupling="maximal",
                    log_every=log_every,
                )

                pair_runs = {"ab": pair_ab, "ba": pair_ba}
                for order_name, result in pair_runs.items():
                    pert_matches = min(int(p["requested_match"]) for p in result["perturbations"])
                    pair_rows.append(
                        {
                            "ensemble": ens.name,
                            "target_nodes": ens.target_nodes,
                            "growth_seed": int(gseed),
                            "run_offset": int(run_offset),
                            "run_seed": int(run_seed),
                            "placement_a": pair[0],
                            "placement_b": pair[1],
                            "order": order_name,
                            "min_support_distance": int(chosen["min_support_distance"]),
                            "requested_match_rate": pert_matches,
                            **result["summary"],
                        }
                    )

                union_jaccards_ab: List[float] = []
                union_jaccards_ba: List[float] = []
                pair_order_jaccards: List[float] = []
                union_component_deltas_ab: List[float] = []
                union_component_deltas_ba: List[float] = []
                control_edge_jaccards: List[float] = []

                for idx in range(min(len(single_a["damaged_sets"]), len(single_b["damaged_sets"]), len(pair_ab["damaged_sets"]), len(pair_ba["damaged_sets"]))):
                    union_d = set(single_a["damaged_sets"][idx]).union(single_b["damaged_sets"][idx])
                    pair_ab_d = set(pair_ab["damaged_sets"][idx])
                    pair_ba_d = set(pair_ba["damaged_sets"][idx])
                    union_jaccards_ab.append(jaccard(pair_ab_d, union_d))
                    union_jaccards_ba.append(jaccard(pair_ba_d, union_d))
                    pair_order_jaccards.append(jaccard(pair_ab_d, pair_ba_d))

                    control_graph_ab = pair_ab["control_graphs"][idx]
                    control_graph_ba = pair_ba["control_graphs"][idx]
                    union_components_ab = len(v15.damaged_components(control_graph_ab, union_d))
                    union_components_ba = len(v15.damaged_components(control_graph_ba, union_d))
                    union_component_deltas_ab.append(
                        safe_float(pair_ab["log_rows"][idx]["damage_component_count"]) - union_components_ab
                    )
                    union_component_deltas_ba.append(
                        safe_float(pair_ba["log_rows"][idx]["damage_component_count"]) - union_components_ba
                    )
                    control_edge_jaccards.append(edge_jaccard_graphs(control_graph_ab, control_graph_ba))

                mean_pair_union_ab = mean_defined(union_jaccards_ab)
                mean_pair_union_ba = mean_defined(union_jaccards_ba)
                mean_pair_order = mean_defined(pair_order_jaccards)
                mean_comp_delta_ab = mean_defined(union_component_deltas_ab)
                mean_comp_delta_ba = mean_defined(union_component_deltas_ba)
                mean_control_edge_jaccard = mean_defined(control_edge_jaccards)

                if mean_control_edge_jaccard < 0.95:
                    interaction_status = "control_divergent"
                elif mean_pair_union_ab <= 0.70 and mean_pair_union_ba <= 0.70 and mean_pair_order >= 0.75:
                    interaction_status = "interaction_supported"
                elif mean_pair_order <= 0.60:
                    interaction_status = "order_sensitive"
                elif mean_pair_union_ab >= 0.85 and mean_pair_union_ba >= 0.85:
                    interaction_status = "near_superposition"
                else:
                    interaction_status = "mixed"

                interaction_rows.append(
                    {
                        "ensemble": ens.name,
                        "target_nodes": ens.target_nodes,
                        "growth_seed": int(gseed),
                        "run_offset": int(run_offset),
                        "run_seed": int(run_seed),
                        "placement_a": pair[0],
                        "placement_b": pair[1],
                        "min_support_distance": int(chosen["min_support_distance"]),
                        "single_a_mean_radius": safe_float(single_a["summary"]["mean_radius_control"]),
                        "single_b_mean_radius": safe_float(single_b["summary"]["mean_radius_control"]),
                        "pair_ab_mean_radius": safe_float(pair_ab["summary"]["mean_radius_control"]),
                        "pair_ba_mean_radius": safe_float(pair_ba["summary"]["mean_radius_control"]),
                        "mean_pair_union_jaccard_ab": mean_pair_union_ab,
                        "mean_pair_union_jaccard_ba": mean_pair_union_ba,
                        "mean_pair_order_jaccard": mean_pair_order,
                        "mean_component_delta_vs_union_ab": mean_comp_delta_ab,
                        "mean_component_delta_vs_union_ba": mean_comp_delta_ba,
                        "mean_control_edge_jaccard_ab_ba": mean_control_edge_jaccard,
                        "interaction_status": interaction_status,
                    }
                )
    return pair_rows, interaction_rows


def aggregate_collision_rows(pair_rows: Sequence[Dict[str, Any]], interaction_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    order_groups: MutableMapping[str, List[Dict[str, Any]]] = {}
    for row in pair_rows:
        order_groups.setdefault(str(row["order"]), []).append(dict(row))

    interaction_counts: Dict[str, int] = {}
    for row in interaction_rows:
        key = str(row["interaction_status"])
        interaction_counts[key] = interaction_counts.get(key, 0) + 1

    out: List[Dict[str, Any]] = []
    for order, rows in sorted(order_groups.items()):
        out.append(
            {
                "order": order,
                "n_runs": len(rows),
                "mean_radius_control": mean_defined(safe_float(r["mean_radius_control"]) for r in rows),
                "mean_component_count": mean_defined(safe_float(r["mean_component_count"]) for r in rows),
                "mean_largest_component_fraction": mean_defined(safe_float(r["mean_largest_component_fraction"]) for r in rows),
                "mean_shape_stability": mean_defined(safe_float(r["mean_shape_stability"]) for r in rows),
                "mean_fit_speed_control": mean_defined(safe_float(r["fit_speed_control"]) for r in rows),
            }
        )
    out.append(
        {
            "order": "interaction_status",
            "n_runs": len(interaction_rows),
            "mean_radius_control": interaction_counts.get("interaction_supported", 0) / max(1, len(interaction_rows)),
            "mean_component_count": interaction_counts.get("near_superposition", 0) / max(1, len(interaction_rows)),
            "mean_largest_component_fraction": interaction_counts.get("order_sensitive", 0) / max(1, len(interaction_rows)),
            "mean_shape_stability": interaction_counts.get("mixed", 0) / max(1, len(interaction_rows)),
            "mean_fit_speed_control": mean_defined(safe_float(r["mean_pair_order_jaccard"]) for r in interaction_rows),
        }
    )
    return out


def recommendation_rows(target_summary: Sequence[Dict[str, Any]], interaction_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_clean = (
        min((safe_float(r["mean_control_edge_jaccard_ab_ba"], 1.0) for r in interaction_rows), default=1.0) >= 0.95
        and min((int(r["min_support_distance"]) for r in interaction_rows), default=999999) >= 2
    )
    out.append(
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean and strict_clean else "unclear",
            "note": (
                "Startstørrelsene er separert, placement-paret er faktisk lokalt separert, og kontrollgrenene holder seg samkjørte mellom AB/BA."
                if size_clean and strict_clean
                else "Enten størrelsesseparasjonen, pair-separasjonen eller matched control-grenen er uklar."
            ),
        }
    )
    total = max(1, len(interaction_rows))
    interaction_rate = sum(1 for r in interaction_rows if str(r["interaction_status"]) == "interaction_supported") / total
    superposition_rate = sum(1 for r in interaction_rows if str(r["interaction_status"]) == "near_superposition") / total
    order_rate = sum(1 for r in interaction_rows if str(r["interaction_status"]) == "order_sensitive") / total
    control_divergent_rate = sum(1 for r in interaction_rows if str(r["interaction_status"]) == "control_divergent") / total

    if control_divergent_rate > 0.10:
        status = "artifact_risk"
        note = f"For mange rader har divergerende kontrollgrener (`control_divergent` {control_divergent_rate:.3f}), så kollisjonslesningen er ikke trygg ennå."
        next_status = "tighten_control_matching"
        next_note = "Neste steg bør være enda strengere matched control-spor eller en analyse som ikke avhenger av cross-run union."
    elif interaction_rate >= 0.50 and order_rate <= 0.25:
        status = "collision_signal_present"
        note = f"Parvise defects avviker ofte fra unionen av matched single-runs (`interaction_supported` {interaction_rate:.3f}) uten sterk ordresensitivitet."
        next_status = "follow_collision_family"
        next_note = "Neste steg bør være en mer direkte kollisjonsklassifisering: annihilation, pass-through, binding eller secondary split."
    elif superposition_rate >= 0.50:
        status = "mostly_superposed"
        note = f"De doble defect-runene ligger ofte nær unionen av single-runs (`near_superposition` {superposition_rate:.3f}), så sterke kollisjonssignaler er ikke vist ennå."
        next_status = "longer_horizon_before_collision"
        next_note = "Neste steg bør heller være lengre defect-folging enn mer kollisjonsbredde."
    else:
        status = "mixed"
        note = f"Kollisjonstesten gir blandede utfall (`interaction_supported` {interaction_rate:.3f}, `near_superposition` {superposition_rate:.3f}, `order_sensitive` {order_rate:.3f})."
        next_status = "tighten_collision_setup"
        next_note = "Neste steg bør være enda strengere pair-selection eller større separasjon mellom de to initiale defectene."

    out.append(
        {
            "diagnostic_family": "collision_signal",
            "status": status,
            "note": note,
        }
    )
    out.append(
        {
            "diagnostic_family": "next_step",
            "status": next_status,
            "note": next_note,
        }
    )
    return out


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def build_report(
    target_summary: Sequence[Dict[str, Any]],
    aggregate_rows: Sequence[Dict[str, Any]],
    interaction_rows: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15b: add_chord collision lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester om to separerte `add_chord`-defects oppfører seg som ren superposisjon av to single-runs, eller om vi ser reelle interaksjonssignaler."
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
    lines.append("## Pair orders")
    lines.append("")
    lines.append("| order | n | mean radius | mean components | mean largest frac | mean shape stability | fit_speed |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate_rows:
        if str(row["order"]) == "interaction_status":
            continue
        lines.append(
            f"| {row['order']} | {int(row['n_runs'])} | {fmt(row['mean_radius_control'])} | {fmt(row['mean_component_count'])} | {fmt(row['mean_largest_component_fraction'])} | {fmt(row['mean_shape_stability'])} | {fmt(row['mean_fit_speed_control'])} |"
        )
    lines.append("")
    lines.append("## Interaction diagnostics")
    lines.append("")
    lines.append("| target | pair | dist | pair-union ab | pair-union ba | order jaccard | control jaccard | comp delta ab | comp delta ba | status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in interaction_rows:
        lines.append(
            f"| {int(row['target_nodes'])} | {int(row['placement_a'])}-{int(row['placement_b'])} | {int(row['min_support_distance'])} | {fmt(row['mean_pair_union_jaccard_ab'])} | {fmt(row['mean_pair_union_jaccard_ba'])} | {fmt(row['mean_pair_order_jaccard'])} | {fmt(row['mean_control_edge_jaccard_ab_ba'])} | {fmt(row['mean_component_delta_vs_union_ab'])} | {fmt(row['mean_component_delta_vs_union_ba'])} | {row['interaction_status']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- `near_superposition` betyr at dobbeltdefect-rundet ligner unionen av to matched single-runs.")
    lines.append("- `interaction_supported` betyr at begge orders avviker tydelig fra unionen, uten sterk ordresensitivitet.")
    lines.append("- `order_sensitive` betyr at selve konstruksjonen av dobbeltdefecten er skjør og ma strammes inn videre.")
    lines.append("- `control_divergent` betyr at matched control-grenene ikke er like nok mellom AB/BA til at cross-run union-sammenlikningen er trygg.")
    lines.append("")
    return "\n".join(lines)


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    signal = next((row for row in recommendation if row["diagnostic_family"] == "collision_signal"), None)
    nxt = next((row for row in recommendation if row["diagnostic_family"] == "next_step"), None)
    return "\n".join(
        [
            "# Relasjonell universgraf v0.15b for ikke-spesialister",
            "",
            "Denne runden testet om to lokale defects oppfører seg som to uavhengige forstyrrelser, eller om de faktisk påvirker hverandre.",
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
    p = argparse.ArgumentParser(description="v0.15b add_chord collision lab.")
    p.add_argument("--targets", type=str, default="48,96,192,256")
    p.add_argument("--growth-seeds", type=str, default="101,202")
    p.add_argument("--run-offsets", type=str, default="0,17")
    p.add_argument("--placement-count", type=int, default=6)
    p.add_argument("--out-pair-csv", type=str, default="Documentation/v15b_add_chord_collision_pair_rows.csv")
    p.add_argument("--out-interaction-csv", type=str, default="Documentation/v15b_add_chord_collision_interactions.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15b_add_chord_collision_target_summary.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15b_add_chord_collision_aggregate.csv")
    p.add_argument("--out-recommendation-csv", type=str, default="Documentation/v15b_add_chord_collision_recommendations.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15b_add_chord_collision_lab.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15b.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15b_operativ_anbefaling.md")
    return p.parse_args()


def parse_int_list(spec: str) -> List[int]:
    return [int(part.strip()) for part in spec.split(",") if part.strip()]


def main() -> None:
    args = parse_args()
    targets = parse_int_list(args.targets)
    growth_seeds = parse_int_list(args.growth_seeds)
    run_offsets = parse_int_list(args.run_offsets)

    spec = anchor_spec()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = deep_ensembles(targets)
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)

    pair_rows, interaction_rows = collect_run_rows(
        spec, ensembles, base_states, growth_seeds, run_offsets, args.placement_count
    )
    aggregate = aggregate_collision_rows(pair_rows, interaction_rows)
    recommendation = recommendation_rows(target_summary, interaction_rows)

    report_md = build_report(target_summary, aggregate, interaction_rows, recommendation)
    lay_md = build_lay_summary(recommendation)
    op_md = "\n".join(
        [
            "# v0.15b operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Ikke les denne runden som bevis på partikkelspredning eller binding.",
            "- Les den som en smal test av om to add_chord-defects bare superponerer eller faktisk interagerer.",
        ]
    )

    write_csv(args.out_pair_csv, pair_rows)
    write_csv(args.out_interaction_csv, interaction_rows)
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_recommendation_csv, recommendation)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")

    print(f"Wrote {args.out_summary_md}")
    print(f"Wrote {args.out_interaction_csv}")
    print(f"Wrote {args.out_aggregate_csv}")


if __name__ == "__main__":
    main()
