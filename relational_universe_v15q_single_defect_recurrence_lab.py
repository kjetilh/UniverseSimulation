#!/usr/bin/env python3
"""v0.15q single-defect recurrence lab.

This round investigates the next likely defect question after the token_shift
fragility line weakened under better local controls:

do single defects show meaningful return / recurrence behavior in their late
damage morphology, or do they mostly keep drifting?

This is not a new collision round. It is a narrow single-defect follow-up in
the stable `band_zero_del` regime.
"""
from __future__ import annotations

import argparse
import math
import random
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15


TARGETS = (48, 96)
GROWTH_SEEDS = (101, 202)
PLACEMENTS = (0, 1, 2, 3)
PERTURBATIONS = ("add_chord", "local_swap", "token_shift")
STEPS = 1280
LOG_EVERY = 8
MIN_GAP_SNAPSHOTS = 4
TAIL_START_FRAC = 0.60


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def quantile(values: Sequence[float], q: float) -> float:
    return v15.quantile(values, q)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    return v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def run_defect_with_sets(
    base_state: v7.State,
    *,
    params: v7.Params,
    seed: int,
    steps: int,
    perturbation: str,
    center_token_index: int = 0,
    local_coupling: str = "maximal",
    log_every: int = 40,
) -> Dict[str, Any]:
    rng = random.Random(seed)
    control = base_state.clone()
    perturbed = base_state.clone()

    perturbation_info = v15.v14.v08b.apply_custom_perturbation(
        perturbed,
        perturbation,
        center_token_index=center_token_index,
    )
    support = list(perturbation_info["support"])

    next_node_id, next_token_id = v15.v14.v08b.next_ids_from_state(base_state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)

    log_rows: List[Dict[str, Any]] = []
    damaged_sets: List[Set[int]] = []
    prev_damaged: Optional[Set[int]] = None
    shape_jaccards: List[float] = []
    first_zero_step: Optional[int] = None
    last_alive_step = 0

    snap0, damaged0 = v15.defect_snapshot(control, perturbed, support)
    log_rows.append({"step": 0, "t": 0.0, **snap0})
    damaged_sets.append(set(damaged0))
    if damaged0:
        last_alive_step = 0
    prev_damaged = set(damaged0)

    equal_prev = v7.states_equal(control, perturbed)
    first_meeting_time = 0.0 if equal_prev else None

    for step in range(1, steps + 1):
        v7.coupled_step(control, perturbed, manager, rng, params, local_coupling)
        equal_now = v7.states_equal(control, perturbed)
        if equal_now and not equal_prev and first_meeting_time is None:
            first_meeting_time = control.t
        equal_prev = equal_now
        if step % log_every == 0 or step == steps:
            snap, damaged = v15.defect_snapshot(control, perturbed, support)
            if prev_damaged is not None:
                shape_jaccards.append(v15.jaccard(prev_damaged, damaged))
            prev_damaged = set(damaged)
            if snap["alive"]:
                last_alive_step = step
            elif first_zero_step is None:
                first_zero_step = step
            log_rows.append({"step": step, "t": control.t, **snap})
            damaged_sets.append(set(damaged))

    final = log_rows[-1]
    initial_nodes = max(1.0, safe_float(v7.feature_row(base_state, rng=random.Random(seed + 999)).get("nodes")))
    alive_fraction = mean_defined(float(row["alive"]) for row in log_rows)
    mean_damage_fraction = mean_defined(safe_float(row["damaged_nodes_count"]) / initial_nodes for row in log_rows)
    max_damage_fraction = max((safe_float(row["damaged_nodes_count"]) / initial_nodes for row in log_rows), default=0.0)
    mean_radius = mean_defined(safe_float(row["radius_control"]) for row in log_rows if safe_float(row["radius_control"]) >= 0)
    max_radius = max((safe_float(row["radius_control"]) for row in log_rows if safe_float(row["radius_control"]) >= 0), default=-1.0)
    mean_components = mean_defined(safe_float(row["damage_component_count"]) for row in log_rows)
    max_components = max((int(row["damage_component_count"]) for row in log_rows), default=0)
    mean_largest_fraction = mean_defined(safe_float(row["largest_component_fraction"]) for row in log_rows)
    mean_boundary_to_volume = mean_defined(safe_float(row["boundary_to_volume"]) for row in log_rows)
    mean_shape_stability = mean_defined(shape_jaccards)
    last_alive_fraction = float(last_alive_step / max(1, steps))
    final_alive = int(final["alive"])

    if final_alive == 0 and alive_fraction <= 0.60 and last_alive_fraction <= 0.75:
        outcome = "dies_out"
    elif final_alive == 1 and mean_radius <= 2.0 and mean_damage_fraction <= 0.08 and mean_components <= 1.30:
        outcome = "persistent_localized"
    elif final_alive == 1 and max_components >= 2 and mean_largest_fraction <= 0.78:
        outcome = "persistent_split"
    elif final_alive == 1 and mean_radius >= 2.5 and mean_damage_fraction >= 0.05:
        outcome = "persistent_diffuse"
    else:
        outcome = "mixed_transient"

    return {
        "perturbation_info": dict(perturbation_info),
        "log_rows": log_rows,
        "damaged_sets": damaged_sets,
        "summary": {
            "final_alive": final_alive,
            "alive_fraction": alive_fraction,
            "last_alive_fraction": last_alive_fraction,
            "first_zero_step": first_zero_step if first_zero_step is not None else -1,
            "mean_damage_fraction": mean_damage_fraction,
            "max_damage_fraction": max_damage_fraction,
            "mean_radius_control": mean_radius,
            "max_radius_control": max_radius,
            "mean_component_count": mean_components,
            "max_component_count": max_components,
            "mean_largest_component_fraction": mean_largest_fraction,
            "mean_boundary_to_volume": mean_boundary_to_volume,
            "mean_shape_stability": mean_shape_stability,
            "outcome_class": outcome,
            "first_meeting_time": first_meeting_time if first_meeting_time is not None else -1.0,
        },
    }


def exact_jaccard(a: Set[int], b: Set[int]) -> float:
    return v15.jaccard(a, b)


def coarse_signature(row: Mapping[str, Any]) -> Tuple[int, int, int, int, int]:
    alive = int(row["alive"])
    comp_bin = min(6, int(round(safe_float(row["damage_component_count"]))))
    radius = safe_float(row["radius_control"])
    radius_bin = -1 if not math.isfinite(radius) or radius < 0 else min(12, int(round(radius)))
    largest_bin = min(4, int(math.floor(4.0 * safe_float(row["largest_component_fraction"]) + 1e-9)))
    boundary = safe_float(row["boundary_to_volume"])
    boundary_bin = -1 if not math.isfinite(boundary) else min(8, int(round(boundary)))
    return alive, comp_bin, radius_bin, largest_bin, boundary_bin


def recurrence_metrics(log_rows: Sequence[Dict[str, Any]], damaged_sets: Sequence[Set[int]]) -> Dict[str, Any]:
    tail_start = max(0, int(math.floor(TAIL_START_FRAC * len(log_rows))))
    max_exact_scores: List[float] = []
    coarse_return_hits = 0
    exact_return_hits = 0
    near_return_hits = 0
    first_exact_step = -1.0
    first_coarse_step = -1.0
    for idx in range(tail_start, len(log_rows)):
        cur_set = damaged_sets[idx]
        cur_sig = coarse_signature(log_rows[idx])
        best_exact = -1.0
        coarse_hit = False
        for prev in range(0, max(0, idx - MIN_GAP_SNAPSHOTS)):
            best_exact = max(best_exact, exact_jaccard(cur_set, damaged_sets[prev]))
            if coarse_signature(log_rows[prev]) == cur_sig:
                coarse_hit = True
        if best_exact < 0.0:
            best_exact = float("nan")
        max_exact_scores.append(best_exact)
        if math.isfinite(best_exact) and best_exact >= 0.95:
            exact_return_hits += 1
            if first_exact_step < 0:
                first_exact_step = safe_float(log_rows[idx]["step"])
        elif math.isfinite(best_exact) and best_exact >= 0.75:
            near_return_hits += 1
        if coarse_hit:
            coarse_return_hits += 1
            if first_coarse_step < 0:
                first_coarse_step = safe_float(log_rows[idx]["step"])
    denom = max(1, len(max_exact_scores))
    return {
        "tail_snapshot_count": denom,
        "exact_return_rate": exact_return_hits / denom,
        "coarse_return_rate": coarse_return_hits / denom,
        "near_return_rate": near_return_hits / denom,
        "max_exact_return_jaccard": max((x for x in max_exact_scores if math.isfinite(x)), default=float("nan")),
        "mean_max_exact_return_jaccard": mean_defined(x for x in max_exact_scores if math.isfinite(x)),
        "first_exact_return_step": first_exact_step,
        "first_coarse_return_step": first_coarse_step,
    }


def classify_recurrence_label(final_alive: int, metrics: Mapping[str, Any]) -> str:
    exact_rate = safe_float(metrics["exact_return_rate"])
    coarse_rate = safe_float(metrics["coarse_return_rate"])
    near_rate = safe_float(metrics["near_return_rate"])
    max_exact = safe_float(metrics["max_exact_return_jaccard"])
    if final_alive == 0:
        if coarse_rate >= 0.30 or exact_rate >= 0.10:
            return "extinct_after_return"
        return "extinct_without_return"
    if exact_rate >= 0.20 and coarse_rate >= 0.40:
        return "cyclic_return"
    if coarse_rate >= 0.40:
        return "morphology_return"
    if near_rate >= 0.20 or max_exact >= 0.80:
        return "near_return"
    return "drifting_tail"


def run_rows(*, ensembles: Sequence[Any], base_states: Mapping[Tuple[str, int], Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    for ens in ensembles:
        target = int(ens.target_nodes)
        if target not in TARGETS:
            continue
        for growth_seed in GROWTH_SEEDS:
            base = base_states[(ens.name, int(growth_seed))]
            for perturbation in PERTURBATIONS:
                for placement in PLACEMENTS:
                    run_seed = target * 100000 + int(growth_seed) * 1000 + int(placement)
                    res = run_defect_with_sets(
                        base,
                        params=params,
                        seed=run_seed,
                        steps=STEPS,
                        perturbation=perturbation,
                        center_token_index=int(placement),
                        local_coupling="maximal",
                        log_every=LOG_EVERY,
                    )
                    info = dict(res["perturbation_info"])
                    actual = str(info.get("type", "unknown"))
                    requested_match = 1 if v15.v14.perturbation_requested_match(perturbation, actual) else 0
                    support = list(info.get("support", []))
                    summary = dict(res["summary"])
                    recur = recurrence_metrics(res["log_rows"], res["damaged_sets"])
                    recurrence_label = classify_recurrence_label(int(summary["final_alive"]), recur)
                    rows.append(
                        {
                            "target_nodes": target,
                            "growth_seed": int(growth_seed),
                            "placement": int(placement),
                            "run_seed": int(run_seed),
                            "requested_perturbation": perturbation,
                            "actual_perturbation": actual,
                            "requested_match": int(requested_match),
                            "support_size": len(support),
                            "support_signature": ",".join(str(x) for x in support),
                            "final_alive": int(summary["final_alive"]),
                            "mean_radius_control": safe_float(summary["mean_radius_control"]),
                            "mean_component_count": safe_float(summary["mean_component_count"]),
                            "outcome_class": str(summary["outcome_class"]),
                            **recur,
                            "recurrence_label": recurrence_label,
                        }
                    )
    return rows


def aggregate_rows(run_rows_: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: MutableMapping[Tuple[str, int], List[Dict[str, Any]]] = {}
    for row in run_rows_:
        grouped.setdefault((str(row["requested_perturbation"]), int(row["target_nodes"])), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for (perturbation, target_nodes), rows in sorted(grouped.items()):
        counts: Dict[str, int] = {}
        for row in rows:
            counts[str(row["recurrence_label"])] = counts.get(str(row["recurrence_label"]), 0) + 1
        dominant = max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
        out.append(
            {
                "requested_perturbation": perturbation,
                "target_nodes": int(target_nodes),
                "n_runs": len(rows),
                "strict_match_rate": mean_defined(float(r["requested_match"]) for r in rows),
                "cyclic_return_rate": mean_defined(1.0 if str(r["recurrence_label"]) == "cyclic_return" else 0.0 for r in rows),
                "morphology_return_rate": mean_defined(1.0 if str(r["recurrence_label"]) == "morphology_return" else 0.0 for r in rows),
                "near_return_rate": mean_defined(1.0 if str(r["recurrence_label"]) == "near_return" else 0.0 for r in rows),
                "extinct_after_return_rate": mean_defined(1.0 if str(r["recurrence_label"]) == "extinct_after_return" else 0.0 for r in rows),
                "extinct_without_return_rate": mean_defined(1.0 if str(r["recurrence_label"]) == "extinct_without_return" else 0.0 for r in rows),
                "drifting_tail_rate": mean_defined(1.0 if str(r["recurrence_label"]) == "drifting_tail" else 0.0 for r in rows),
                "mean_exact_return_rate": mean_defined(safe_float(r["exact_return_rate"]) for r in rows),
                "mean_coarse_return_rate": mean_defined(safe_float(r["coarse_return_rate"]) for r in rows),
                "mean_max_exact_return_jaccard": mean_defined(safe_float(r["max_exact_return_jaccard"]) for r in rows),
                "dominant_recurrence_label": dominant,
            }
        )
    return out


def recommendation_rows(target_summary: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((safe_float(row["strict_match_rate"]) for row in aggregate), default=0.0) >= 0.999
    add_best = max(
        (safe_float(r["cyclic_return_rate"]) + safe_float(r["morphology_return_rate"]) for r in aggregate if str(r["requested_perturbation"]) == "add_chord"),
        default=0.0,
    )
    swap_best = max(
        (safe_float(r["cyclic_return_rate"]) + safe_float(r["morphology_return_rate"]) for r in aggregate if str(r["requested_perturbation"]) == "local_swap"),
        default=0.0,
    )
    token_best = max(
        (safe_float(r["cyclic_return_rate"]) + safe_float(r["morphology_return_rate"]) for r in aggregate if str(r["requested_perturbation"]) == "token_shift"),
        default=0.0,
    )
    rows = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er rent separert og alle testede perturbasjoner matcher ønsket type."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        }
    ]
    if max(add_best, swap_best, token_best) >= 0.40:
        best_name = "add_chord" if add_best >= max(swap_best, token_best) else ("local_swap" if swap_best >= token_best else "token_shift")
        rows.append(
            {
                "diagnostic_family": "recurrence_signal",
                "status": "late_return_signal_present",
                "note": f"`{best_name}` viser den tydeligste senfase-returstrukturen i denne smale runden, men fortsatt bare som lokal defect-dynamikk.",
            }
        )
        rows.append(
            {
                "diagnostic_family": "next_step",
                "status": "follow_recurrence_family",
                "note": f"Neste steg bør være en enda smalere retur-/recurrence-runde for `{best_name}`, ikke brede defect-paastander.",
            }
        )
    else:
        rows.append(
            {
                "diagnostic_family": "recurrence_signal",
                "status": "mostly_drifting",
                "note": "Single defects viser for det meste drifting eller bare svake near-return-signaler i denne runden.",
            }
        )
        rows.append(
            {
                "diagnostic_family": "next_step",
                "status": "pivot_again",
                "note": "Neste steg bør være et annet smalt defect-spørsmål enn recurrence langs denne aksen.",
            }
        )
    return rows


def build_report(*, target_summary: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], recommendation: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15q: single-defect recurrence lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden spør om single defects kommer tilbake til tidligere morfologier i senfasen, eller om de for det meste bare fortsetter å drive."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        if int(row["target_nodes"]) not in TARGETS:
            continue
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Aggregate recurrence")
    lines.append("")
    lines.append("| perturbation | target | cyclic | morphology return | near return | extinct-after-return | drifting | dominant |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['requested_perturbation']} | {int(row['target_nodes'])} | {fmt(row['cyclic_return_rate'])} | {fmt(row['morphology_return_rate'])} | {fmt(row['near_return_rate'])} | {fmt(row['extinct_after_return_rate'])} | {fmt(row['drifting_tail_rate'])} | {row['dominant_recurrence_label']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en single-defect-runde, ikke en collision-runde.")
    lines.append("- Les dette som morfologisk recurrence i lokale defects, ikke som partikkelbevis eller generell geometri.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15q single-defect recurrence lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15q_single_defect_recurrence_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15q_single_defect_recurrence_aggregate.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15q_single_defect_recurrence_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15q_single_defect_recurrence_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15q_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15q.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles(list(TARGETS))
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    target_summary = v10e.summarize_bases(base_rows)
    rows = run_rows(ensembles=ensembles, base_states=base_states)
    aggregate = aggregate_rows(rows)
    recommendation = recommendation_rows(target_summary, aggregate)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, recommendation=recommendation)
    op_md = "\n".join(
        [
            "# v0.15q operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Les denne runden som single-defect recurrence, ikke som partikkelbevis.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15q",
            "",
            "Denne runden spør om en lokal skade i grafen noen ganger finner tilbake til lignende former senere, i stedet for bare å fortsette å endre seg.",
            "",
            "Det er interessant fordi det kan tyde på en enkel type lokal hukommelse eller retur, selv uten å påstå noe stort om fysikk.",
        ]
    ) + "\n"
    write_csv(args.out_runs_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
