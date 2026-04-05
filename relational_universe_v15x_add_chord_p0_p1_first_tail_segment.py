#!/usr/bin/env python3
"""v0.15x add_chord p0-vs-p1 first-tail-segment lab.

This is the next narrow step after v15w. It keeps the same base and the same
small holdout seeds, but stops arguing from static support contrast alone.
Instead it looks at the first tail segment before exact-return lock, to ask
whether p1 tends to win by earlier consolidation while p0 wins by calmer
pre-lock behavior.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 48
GROWTH_SEED = 202
PLACEMENTS = (0, 1)
SEED_DELTAS = (151, 179, 211, 239, 271, 307)
FULL_STEPS = 2560
LOG_EVERY = 8


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def quantile(values: Sequence[float], q: float) -> float:
    return v15.quantile(values, q)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def segment_bounds(log_rows: Sequence[Dict[str, Any]], first_exact_step: float) -> Tuple[int, int]:
    tail_start_idx = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(log_rows))))
    if not math.isfinite(first_exact_step) or first_exact_step < 0:
        return tail_start_idx, len(log_rows) - 1
    end_idx = tail_start_idx
    for idx in range(tail_start_idx, len(log_rows)):
        if safe_float(log_rows[idx]["step"]) >= first_exact_step:
            end_idx = idx
            break
    return tail_start_idx, end_idx


def adjacency_jaccards(damaged_sets: Sequence[set[int]], start_idx: int, end_idx: int) -> List[float]:
    vals: List[float] = []
    for idx in range(start_idx, end_idx):
        vals.append(v15.jaccard(damaged_sets[idx], damaged_sets[idx + 1]))
    return vals


def exact_hits_after_step(log_rows: Sequence[Dict[str, Any]], damaged_sets: Sequence[set[int]], start_step: float) -> Tuple[float, int]:
    hits: List[int] = []
    for idx, row in enumerate(log_rows):
        if safe_float(row["step"]) < start_step:
            continue
        cur_set = damaged_sets[idx]
        best_exact = -1.0
        for prev in range(0, max(0, idx - v15q.MIN_GAP_SNAPSHOTS)):
            best_exact = max(best_exact, v15q.exact_jaccard(cur_set, damaged_sets[prev]))
        hits.append(1 if math.isfinite(best_exact) and best_exact >= 0.95 else 0)
    return mean_defined(hits), sum(1 for a, b in zip(hits, hits[1:]) if a != b)


def run_rows(*, base_state: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    for placement in PLACEMENTS:
        base_run_seed = TARGET * 100000 + GROWTH_SEED * 1000 + int(placement)
        for seed_delta in SEED_DELTAS:
            run_seed = int(base_run_seed + seed_delta)
            res = v15q.run_defect_with_sets(
                base_state,
                params=params,
                seed=run_seed,
                steps=FULL_STEPS,
                perturbation="add_chord",
                center_token_index=placement,
                local_coupling="maximal",
                log_every=LOG_EVERY,
            )
            metrics = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
            first_exact = safe_float(metrics["first_exact_return_step"])
            start_idx, end_idx = segment_bounds(res["log_rows"], first_exact)
            seg_rows = res["log_rows"][start_idx : end_idx + 1]
            seg_sets = res["damaged_sets"][start_idx : end_idx + 1]
            adj = adjacency_jaccards(res["damaged_sets"], start_idx, end_idx)
            post_exact_hit_rate, post_exact_switch_count = exact_hits_after_step(res["log_rows"], res["damaged_sets"], first_exact)
            info = dict(res["perturbation_info"])
            rows.append(
                {
                    "target_nodes": TARGET,
                    "growth_seed": GROWTH_SEED,
                    "placement": int(placement),
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
                    "support_signature": ",".join(str(x) for x in info.get("support", [])),
                    "full_exact_return_rate": safe_float(metrics["exact_return_rate"]),
                    "first_exact_return_step": first_exact,
                    "segment_snapshot_count": len(seg_rows),
                    "mean_prelock_component_count": mean_defined(safe_float(r["damage_component_count"]) for r in seg_rows),
                    "mean_prelock_largest_fraction": mean_defined(safe_float(r["largest_component_fraction"]) for r in seg_rows),
                    "mean_prelock_boundary_to_volume": mean_defined(safe_float(r["boundary_to_volume"]) for r in seg_rows),
                    "mean_prelock_radius": mean_defined(
                        safe_float(r["radius_control"]) for r in seg_rows if safe_float(r["radius_control"]) >= 0
                    ),
                    "mean_prelock_adjacent_jaccard": mean_defined(adj),
                    "post_exact_hit_rate": post_exact_hit_rate,
                    "post_exact_switch_count": int(post_exact_switch_count),
                    "mean_prelock_damage_nodes": mean_defined(safe_float(r["damaged_nodes_count"]) for r in seg_rows),
                    "segment_start_step": safe_float(seg_rows[0]["step"]),
                    "segment_end_step": safe_float(seg_rows[-1]["step"]),
                    "full_label": v15q.classify_recurrence_label(int(res["log_rows"][-1]["alive"]), metrics),
                }
            )
    return rows


def duel_label(
    *,
    first_gap: float,
    component_gap: float,
    largest_gap: float,
    boundary_gap: float,
    jaccard_gap: float,
    post_switch_gap: float,
    exact_gap: float,
) -> str:
    p1_earlier = first_gap <= -8.0
    p1_more_consolidated = component_gap <= -0.25 and largest_gap >= 0.03
    p0_calmer = jaccard_gap <= -0.03 and post_switch_gap >= 3 and boundary_gap >= 0.05
    p1_clean = p1_earlier and p1_more_consolidated and boundary_gap <= 0.0 and exact_gap >= 0.05
    if p1_clean:
        return "p1_earlier_consolidation"
    if p1_earlier and p0_calmer:
        return "speed_stability_tradeoff"
    if p0_calmer and exact_gap <= -0.05:
        return "p0_calmer_tail"
    if p1_more_consolidated and exact_gap > 0:
        return "p1_soft_consolidation_edge"
    return "mixed_first_segment"


def duel_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    by_delta: Dict[int, Dict[int, Dict[str, Any]]] = {}
    for row in rows:
        by_delta.setdefault(int(row["seed_delta"]), {})[int(row["placement"])] = row
    for seed_delta in sorted(by_delta):
        pair = by_delta[seed_delta]
        if set(pair) != {0, 1}:
            continue
        p0 = pair[0]
        p1 = pair[1]
        first_gap = safe_float(p1["first_exact_return_step"]) - safe_float(p0["first_exact_return_step"])
        component_gap = safe_float(p1["mean_prelock_component_count"]) - safe_float(p0["mean_prelock_component_count"])
        largest_gap = safe_float(p1["mean_prelock_largest_fraction"]) - safe_float(p0["mean_prelock_largest_fraction"])
        boundary_gap = safe_float(p1["mean_prelock_boundary_to_volume"]) - safe_float(p0["mean_prelock_boundary_to_volume"])
        jaccard_gap = safe_float(p1["mean_prelock_adjacent_jaccard"]) - safe_float(p0["mean_prelock_adjacent_jaccard"])
        post_switch_gap = safe_float(p1["post_exact_switch_count"]) - safe_float(p0["post_exact_switch_count"])
        exact_gap = safe_float(p1["full_exact_return_rate"]) - safe_float(p0["full_exact_return_rate"])
        out.append(
            {
                "seed_delta": int(seed_delta),
                "p0_first_exact_return_step": safe_float(p0["first_exact_return_step"]),
                "p1_first_exact_return_step": safe_float(p1["first_exact_return_step"]),
                "p1_minus_p0_first_gap": first_gap,
                "p0_mean_prelock_component_count": safe_float(p0["mean_prelock_component_count"]),
                "p1_mean_prelock_component_count": safe_float(p1["mean_prelock_component_count"]),
                "p1_minus_p0_component_gap": component_gap,
                "p0_mean_prelock_largest_fraction": safe_float(p0["mean_prelock_largest_fraction"]),
                "p1_mean_prelock_largest_fraction": safe_float(p1["mean_prelock_largest_fraction"]),
                "p1_minus_p0_largest_gap": largest_gap,
                "p0_mean_prelock_boundary_to_volume": safe_float(p0["mean_prelock_boundary_to_volume"]),
                "p1_mean_prelock_boundary_to_volume": safe_float(p1["mean_prelock_boundary_to_volume"]),
                "p1_minus_p0_boundary_gap": boundary_gap,
                "p0_mean_prelock_adjacent_jaccard": safe_float(p0["mean_prelock_adjacent_jaccard"]),
                "p1_mean_prelock_adjacent_jaccard": safe_float(p1["mean_prelock_adjacent_jaccard"]),
                "p1_minus_p0_jaccard_gap": jaccard_gap,
                "p0_post_exact_switch_count": safe_float(p0["post_exact_switch_count"]),
                "p1_post_exact_switch_count": safe_float(p1["post_exact_switch_count"]),
                "p1_minus_p0_post_switch_gap": post_switch_gap,
                "p0_full_exact_return_rate": safe_float(p0["full_exact_return_rate"]),
                "p1_full_exact_return_rate": safe_float(p1["full_exact_return_rate"]),
                "p1_minus_p0_exact_gap": exact_gap,
                "duel_label": duel_label(
                    first_gap=first_gap,
                    component_gap=component_gap,
                    largest_gap=largest_gap,
                    boundary_gap=boundary_gap,
                    jaccard_gap=jaccard_gap,
                    post_switch_gap=post_switch_gap,
                    exact_gap=exact_gap,
                ),
            }
        )
    return out


def aggregate_duels(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    labels = sorted({str(row["duel_label"]) for row in rows})
    total = max(1, len(rows))
    out: List[Dict[str, Any]] = []
    for label in labels:
        grp = [row for row in rows if str(row["duel_label"]) == label]
        out.append(
            {
                "duel_label": label,
                "n_duels": len(grp),
                "rate": len(grp) / total,
                "mean_p1_minus_p0_first_gap": mean_defined(safe_float(row["p1_minus_p0_first_gap"]) for row in grp),
                "mean_p1_minus_p0_component_gap": mean_defined(safe_float(row["p1_minus_p0_component_gap"]) for row in grp),
                "mean_p1_minus_p0_largest_gap": mean_defined(safe_float(row["p1_minus_p0_largest_gap"]) for row in grp),
                "mean_p1_minus_p0_boundary_gap": mean_defined(safe_float(row["p1_minus_p0_boundary_gap"]) for row in grp),
                "mean_p1_minus_p0_jaccard_gap": mean_defined(safe_float(row["p1_minus_p0_jaccard_gap"]) for row in grp),
                "mean_p1_minus_p0_post_switch_gap": mean_defined(safe_float(row["p1_minus_p0_post_switch_gap"]) for row in grp),
                "mean_p1_minus_p0_exact_gap": mean_defined(safe_float(row["p1_minus_p0_exact_gap"]) for row in grp),
            }
        )
    return out


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], run_rows_out: Sequence[Dict[str, Any]], duel_aggr: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    counts = {str(row["duel_label"]): int(row["n_duels"]) for row in duel_aggr}
    total = max(1, sum(counts.values()))
    p1_early = counts.get("p1_earlier_consolidation", 0) / total
    tradeoff = counts.get("speed_stability_tradeoff", 0) / total
    p0_calm = counts.get("p0_calmer_tail", 0) / total
    p1_soft = counts.get("p1_soft_consolidation_edge", 0) / total
    if p1_early >= 0.33 and (p1_early + p1_soft) >= 0.50:
        status = "p1_often_wins_by_earlier_consolidation"
        note = "P1 vinner ofte når den låser tidligere og med litt sterkere pre-lock-konsolidering enn p0."
        next_step = "inspect_first_segment_structure"
        next_note = "Neste steg bør sammenligne første tail-segment snapshot-for-snapshot for p0 og p1."
    elif tradeoff >= 0.33 or p0_calm >= 0.33:
        status = "speed_stability_tradeoff_remains"
        note = "P0-vs-p1 ser fortsatt best ut som en ekte tradeoff mellom tidligere lås og roligere tail-lock."
        next_step = "inspect_tradeoff_seed_cases"
        next_note = "Neste steg bør fokusere bare på seedene der tradeoff-en er tydeligst."
    else:
        status = "first_segment_still_mixed"
        note = "Første tail-segment gjør forskjellen mer konkret, men ikke rent nok til én enkel mekanisme."
        next_step = "stay_tiny"
        next_note = "Neste steg bør være en enda mindre forklaringsrunde på én eller to seed-caser."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": "Startstørrelsene er rent separert i denne første-tail-segment-runden." if size_clean else "Størrelsesseparasjonen er uklar i denne runden.",
        },
        {
            "diagnostic_family": "duel_family_snapshot",
            "status": f"p1_early={fmt(p1_early)};p1_soft={fmt(p1_soft)};tradeoff={fmt(tradeoff)};p0_calm={fmt(p0_calm)}",
            "note": "Dette oppsummerer hvordan p0 og p1 skiller lag i første tail-segment på de samme små holdout-seedene.",
        },
        {
            "diagnostic_family": "first_segment_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, target_summary: Sequence[Dict[str, Any]], duel_aggr: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15x: add_chord p0-vs-p1 first tail segment")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden sammenligner bare første tail-segment for `p0` og `p1`, for å se om forskjellen deres skyldes tidligere konsolidering, roligere tail-lock eller en blanding."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        if int(row["target_nodes"]) != TARGET:
            continue
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Duel aggregate")
    lines.append("")
    lines.append("| duel label | n | rate | first gap | component gap | largest gap | boundary gap | jaccard gap | post-switch gap | exact gap |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in duel_aggr:
        lines.append(
            f"| {row['duel_label']} | {int(row['n_duels'])} | {fmt(row['rate'])} | {fmt(row['mean_p1_minus_p0_first_gap'],1)} | {fmt(row['mean_p1_minus_p0_component_gap'])} | {fmt(row['mean_p1_minus_p0_largest_gap'])} | {fmt(row['mean_p1_minus_p0_boundary_gap'])} | {fmt(row['mean_p1_minus_p0_jaccard_gap'])} | {fmt(row['mean_p1_minus_p0_post_switch_gap'])} | {fmt(row['mean_p1_minus_p0_exact_gap'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en første-tail-segment-runde på samme `p0`/`p1`-dueller, ikke en ny seed-scan.")
    lines.append("- Les dette som lokal onset-mekanikk, ikke som generell defect-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15x add_chord p0-vs-p1 first tail segment.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15x_add_chord_p0_p1_first_tail_segment_runs.csv")
    p.add_argument("--out-duels-csv", type=str, default="Documentation/v15x_add_chord_p0_p1_first_tail_segment_duels.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15x_add_chord_p0_p1_first_tail_segment_aggregate.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15x_add_chord_p0_p1_first_tail_segment_target_summary.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15x_add_chord_p0_p1_first_tail_segment_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15x_add_chord_p0_p1_first_tail_segment.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15x_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15x.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    run_rows_out = run_rows(base_state=base_state)
    duel_rows_out = duel_rows(run_rows_out)
    duel_aggr = aggregate_duels(duel_rows_out)
    diagnosis = diagnosis_rows(target_summary, run_rows_out, duel_aggr)
    report_md = build_report(target_summary=target_summary, duel_aggr=duel_aggr, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15x operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in diagnosis
            ],
            "",
            "- Les denne runden som en første-tail-segment-test for `p0` vs `p1`, ikke som bredere band-mapping.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15x",
            "",
            "Denne runden ser bare på det første lille stykket av senfasen der `p0` og `p1` begynner å skille lag.",
            "",
            "Målet er å se om `p1` pleier å vinne ved å samle seg tidligere, eller om `p0` vinner ved å roe seg raskere ned når låsen først er på plass.",
        ]
    ) + "\n"
    write_csv(args.out_runs_csv, run_rows_out)
    write_csv(args.out_duels_csv, duel_rows_out)
    write_csv(args.out_aggregate_csv, duel_aggr)
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
