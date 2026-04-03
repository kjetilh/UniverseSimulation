#!/usr/bin/env python3
"""v0.15h representative collision trace lab.

This follows v15g. The goal is not more pair-offset search, but longer
genealogy-aware traces for a few representative collision runs chosen from the
shared-base `48` corridor.

We keep the same anchored regime and `add_chord` collision setup, but ask a
different question:

Do the early event-chain labels from v15g remain informative on a longer
horizon, or do they collapse into a common late-time morphology?
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15b_add_chord_collision_lab as v15b
import relational_universe_v15g_collision_genealogy_lab as v15g


TARGET = 48
PRIMARY_GROWTH_SEED = 101
PREFIX_STEPS = 420
LONG_STEPS = 1260
LOG_EVERY = 2

TRACE_SPECS = (
    {
        "trace_label": "pair23_merge_hold_split",
        "pair": (2, 3),
        "run_offset": 0,
        "expected_prefix_chain": "merge_hold_split",
    },
    {
        "trace_label": "pair23_compress_split_rebind",
        "pair": (2, 3),
        "run_offset": 11,
        "expected_prefix_chain": "compress_split_rebind",
    },
    {
        "trace_label": "pair23_split_persistent_dual",
        "pair": (2, 3),
        "run_offset": 5,
        "expected_prefix_chain": "split_persistent_dual",
    },
    {
        "trace_label": "pair34_split_persistent_dual",
        "pair": (3, 4),
        "run_offset": 5,
        "expected_prefix_chain": "split_persistent_dual",
    },
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15b.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15b.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15b.write_csv(path, rows)


def slice_order_result(order_result: Mapping[str, Any], max_step: int) -> Dict[str, Any]:
    keep = [
        idx
        for idx, row in enumerate(order_result["log_rows"])
        if int(row["step"]) <= int(max_step)
    ]
    if not keep:
        keep = [0]
    return {
        "log_rows": [order_result["log_rows"][idx] for idx in keep],
        "damaged_sets": [order_result["damaged_sets"][idx] for idx in keep],
        "control_graphs": [order_result["control_graphs"][idx] for idx in keep],
        "support_union": list(order_result["support_union"]),
        "summary": dict(order_result.get("summary", {})),
    }


def snapshot_rows_from_order_result(order_result: Mapping[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    support_union = list(order_result["support_union"])
    for idx, log_row in enumerate(order_result["log_rows"]):
        summary, _comps = v15g.snapshot_components(
            snapshot_index=idx,
            step=int(log_row["step"]),
            damaged=set(order_result["damaged_sets"][idx]),
            control_graph=order_result["control_graphs"][idx],
            support_union=support_union,
        )
        out.append(dict(summary))
    return out


def count_events_by_snapshot(
    event_rows: Sequence[Dict[str, Any]],
    event_type: str,
    start_snapshot: int,
) -> int:
    return sum(
        1
        for row in event_rows
        if str(row["event_type"]) == event_type
        and int(row["snapshot_index_to"]) >= int(start_snapshot)
    )


def classify_tail_behavior(
    *,
    tail_mean_component_count: float,
    tail_dual_fraction: float,
    tail_split_count: int,
    tail_merge_count: int,
    tail_birth_count: int,
    final_component_count: int,
) -> str:
    if tail_dual_fraction >= 0.75 and tail_mean_component_count <= 3.5:
        return "persistent_dual_tail"
    if final_component_count <= 1 and tail_merge_count >= max(1, tail_split_count):
        return "rebound_merge_tail"
    if tail_mean_component_count >= 3.0 and (tail_split_count + tail_birth_count) >= 2:
        return "active_fragmenting_tail"
    return "mixed_tail"


def summarize_tail(
    *,
    event_rows: Sequence[Dict[str, Any]],
    snapshots: Sequence[Dict[str, Any]],
) -> Dict[str, Any]:
    if not snapshots:
        return {
            "tail_start_step": -1,
            "tail_mean_component_count": float("nan"),
            "tail_mean_total_defect_mass": float("nan"),
            "tail_dual_fraction": float("nan"),
            "tail_split_count": -1,
            "tail_merge_count": -1,
            "tail_birth_count": -1,
            "tail_death_count": -1,
            "final_component_count": -1,
            "final_total_defect_mass": -1,
            "tail_behavior": "missing_snapshots",
        }

    tail_start_idx = max(0, int(math.floor(0.75 * len(snapshots))))
    tail_snapshots = snapshots[tail_start_idx:]
    tail_counts = [int(row["component_count"]) for row in tail_snapshots]
    tail_masses = [int(row["total_defect_mass"]) for row in tail_snapshots]
    tail_start_snapshot = int(tail_snapshots[0]["snapshot_index"])

    tail_split_count = count_events_by_snapshot(event_rows, "split", tail_start_snapshot)
    tail_merge_count = count_events_by_snapshot(event_rows, "merge", tail_start_snapshot)
    tail_birth_count = count_events_by_snapshot(event_rows, "birth", tail_start_snapshot)
    tail_death_count = count_events_by_snapshot(event_rows, "death", tail_start_snapshot)
    final_component_count = int(snapshots[-1]["component_count"])

    out = {
        "tail_start_step": int(tail_snapshots[0]["step"]),
        "tail_mean_component_count": mean_defined(tail_counts),
        "tail_mean_total_defect_mass": mean_defined(tail_masses),
        "tail_dual_fraction": mean_defined(1.0 if count >= 2 else 0.0 for count in tail_counts),
        "tail_split_count": int(tail_split_count),
        "tail_merge_count": int(tail_merge_count),
        "tail_birth_count": int(tail_birth_count),
        "tail_death_count": int(tail_death_count),
        "final_component_count": int(final_component_count),
        "final_total_defect_mass": int(snapshots[-1]["total_defect_mass"]),
    }
    out["tail_behavior"] = classify_tail_behavior(
        tail_mean_component_count=safe_float(out["tail_mean_component_count"]),
        tail_dual_fraction=safe_float(out["tail_dual_fraction"]),
        tail_split_count=int(out["tail_split_count"]),
        tail_merge_count=int(out["tail_merge_count"]),
        tail_birth_count=int(out["tail_birth_count"]),
        final_component_count=int(out["final_component_count"]),
    )
    return out


def run_long_trace(
    *,
    base: Any,
    pair: Tuple[int, int],
    trace_label: str,
    run_offset: int,
    expected_prefix_chain: str,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    spec = v15b.anchor_spec()
    params = v15b.v09.candidate_to_params(spec["candidate"])
    run_seed = int(TARGET) * 100000 + int(PRIMARY_GROWTH_SEED) * 1000 + int(run_offset)

    single_a = v15b.run_sequence_from_base(
        base,
        params=params,
        seed=run_seed,
        steps=LONG_STEPS,
        placements=[pair[0]],
        local_coupling="maximal",
        log_every=LOG_EVERY,
    )
    single_b = v15b.run_sequence_from_base(
        base,
        params=params,
        seed=run_seed,
        steps=LONG_STEPS,
        placements=[pair[1]],
        local_coupling="maximal",
        log_every=LOG_EVERY,
    )
    pair_ab = v15b.run_sequence_from_base(
        base,
        params=params,
        seed=run_seed,
        steps=LONG_STEPS,
        placements=[pair[0], pair[1]],
        local_coupling="maximal",
        log_every=LOG_EVERY,
    )
    pair_ba = v15b.run_sequence_from_base(
        base,
        params=params,
        seed=run_seed,
        steps=LONG_STEPS,
        placements=[pair[1], pair[0]],
        local_coupling="maximal",
        log_every=LOG_EVERY,
    )

    prefix_single_a = slice_order_result(single_a, PREFIX_STEPS)
    prefix_single_b = slice_order_result(single_b, PREFIX_STEPS)
    prefix_pair_ab = slice_order_result(pair_ab, PREFIX_STEPS)
    prefix_pair_ba = slice_order_result(pair_ba, PREFIX_STEPS)

    prefix_window_ab = v15g.order_window_metrics(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=PRIMARY_GROWTH_SEED,
        run_offset=run_offset,
        run_seed=run_seed,
        order="ab",
        single_a=prefix_single_a,
        single_b=prefix_single_b,
        pair_result=prefix_pair_ab,
        other_pair_result=prefix_pair_ba,
    )
    prefix_window_ba = v15g.order_window_metrics(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=PRIMARY_GROWTH_SEED,
        run_offset=run_offset,
        run_seed=run_seed,
        order="ba",
        single_a=prefix_single_a,
        single_b=prefix_single_b,
        pair_result=prefix_pair_ba,
        other_pair_result=prefix_pair_ab,
    )
    full_window_ab = v15g.order_window_metrics(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=PRIMARY_GROWTH_SEED,
        run_offset=run_offset,
        run_seed=run_seed,
        order="ab",
        single_a=single_a,
        single_b=single_b,
        pair_result=pair_ab,
        other_pair_result=pair_ba,
    )
    full_window_ba = v15g.order_window_metrics(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=PRIMARY_GROWTH_SEED,
        run_offset=run_offset,
        run_seed=run_seed,
        order="ba",
        single_a=single_a,
        single_b=single_b,
        pair_result=pair_ba,
        other_pair_result=pair_ab,
    )

    _prefix_comp_ab, _prefix_events_ab, prefix_summary_ab = v15g.build_order_genealogy(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=PRIMARY_GROWTH_SEED,
        run_offset=run_offset,
        run_seed=run_seed,
        order="ab",
        order_result=prefix_pair_ab,
        old_window_class=str(prefix_window_ab["window_class"]),
    )
    _prefix_comp_ba, _prefix_events_ba, prefix_summary_ba = v15g.build_order_genealogy(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=PRIMARY_GROWTH_SEED,
        run_offset=run_offset,
        run_seed=run_seed,
        order="ba",
        order_result=prefix_pair_ba,
        old_window_class=str(prefix_window_ba["window_class"]),
    )
    full_comp_ab, full_events_ab, full_summary_ab = v15g.build_order_genealogy(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=PRIMARY_GROWTH_SEED,
        run_offset=run_offset,
        run_seed=run_seed,
        order="ab",
        order_result=pair_ab,
        old_window_class=str(full_window_ab["window_class"]),
    )
    full_comp_ba, full_events_ba, full_summary_ba = v15g.build_order_genealogy(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=PRIMARY_GROWTH_SEED,
        run_offset=run_offset,
        run_seed=run_seed,
        order="ba",
        order_result=pair_ba,
        old_window_class=str(full_window_ba["window_class"]),
    )

    prefix_common = v15g.pair_run_summary(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=PRIMARY_GROWTH_SEED,
        run_offset=run_offset,
        run_seed=run_seed,
        summary_ab=prefix_summary_ab,
        summary_ba=prefix_summary_ba,
        window_ab=prefix_window_ab,
        window_ba=prefix_window_ba,
    )
    full_common = v15g.pair_run_summary(
        pair_label=f"{pair[0]}-{pair[1]}",
        growth_seed=PRIMARY_GROWTH_SEED,
        run_offset=run_offset,
        run_seed=run_seed,
        summary_ab=full_summary_ab,
        summary_ba=full_summary_ba,
        window_ab=full_window_ab,
        window_ba=full_window_ba,
    )

    snapshots_ab = snapshot_rows_from_order_result(pair_ab)
    snapshots_ba = snapshot_rows_from_order_result(pair_ba)
    tail_ab = summarize_tail(event_rows=full_events_ab, snapshots=snapshots_ab)
    tail_ba = summarize_tail(event_rows=full_events_ba, snapshots=snapshots_ba)

    component_rows: List[Dict[str, Any]] = []
    for row in full_comp_ab + full_comp_ba:
        component_rows.append(
            {
                "trace_label": trace_label,
                "expected_prefix_chain": expected_prefix_chain,
                **row,
            }
        )

    event_rows: List[Dict[str, Any]] = []
    for row in full_events_ab + full_events_ba:
        event_rows.append(
            {
                "trace_label": trace_label,
                "expected_prefix_chain": expected_prefix_chain,
                **row,
            }
        )

    summary_row = {
        "trace_label": trace_label,
        "pair_label": f"{pair[0]}-{pair[1]}",
        "growth_seed": int(PRIMARY_GROWTH_SEED),
        "run_offset": int(run_offset),
        "run_seed": int(run_seed),
        "expected_prefix_chain": expected_prefix_chain,
        "prefix_chain_label": str(prefix_common["chain_label"]),
        "full_chain_label": str(full_common["chain_label"]),
        "prefix_old_window_class": str(prefix_common["old_window_class"]),
        "full_old_window_class": str(full_common["old_window_class"]),
        "prefix_matches_expected": 1 if str(prefix_common["chain_label"]) == expected_prefix_chain else 0,
        "order_ambiguous": int(full_common["order_ambiguous"]),
        "mean_control_consistency": safe_float(full_common["mean_control_consistency"]),
        "mean_order_jaccard": safe_float(full_common["mean_order_jaccard"]),
        "mean_split_count": safe_float(full_common["split_count"]),
        "mean_merge_count": safe_float(full_common["merge_count"]),
        "mean_birth_count": safe_float(full_common["birth_count"]),
        "mean_death_count": safe_float(full_common["death_count"]),
        "mean_first_split_step": safe_float(full_common["first_split_step"]),
        "mean_first_merge_step": safe_float(full_common["first_merge_step"]),
        "mean_max_component_count": safe_float(full_common["max_component_count"]),
        "mean_component_lifetime": safe_float(full_common["mean_component_lifetime"]),
        "mean_post_first_split_dual_duration": safe_float(full_common["post_first_split_dual_duration"]),
        "mean_final_total_defect_mass": safe_float(full_common["final_total_defect_mass"]),
        "tail_start_step": mean_defined([safe_float(tail_ab["tail_start_step"]), safe_float(tail_ba["tail_start_step"])]),
        "tail_mean_component_count": mean_defined([safe_float(tail_ab["tail_mean_component_count"]), safe_float(tail_ba["tail_mean_component_count"])]),
        "tail_mean_total_defect_mass": mean_defined([safe_float(tail_ab["tail_mean_total_defect_mass"]), safe_float(tail_ba["tail_mean_total_defect_mass"])]),
        "tail_dual_fraction": mean_defined([safe_float(tail_ab["tail_dual_fraction"]), safe_float(tail_ba["tail_dual_fraction"])]),
        "tail_split_count": mean_defined([safe_float(tail_ab["tail_split_count"]), safe_float(tail_ba["tail_split_count"])]),
        "tail_merge_count": mean_defined([safe_float(tail_ab["tail_merge_count"]), safe_float(tail_ba["tail_merge_count"])]),
        "tail_birth_count": mean_defined([safe_float(tail_ab["tail_birth_count"]), safe_float(tail_ba["tail_birth_count"])]),
        "tail_death_count": mean_defined([safe_float(tail_ab["tail_death_count"]), safe_float(tail_ba["tail_death_count"])]),
        "final_component_count": mean_defined([safe_float(tail_ab["final_component_count"]), safe_float(tail_ba["final_component_count"])]),
        "final_total_defect_mass": mean_defined([safe_float(tail_ab["final_total_defect_mass"]), safe_float(tail_ba["final_total_defect_mass"])]),
        "tail_behavior_ab": str(tail_ab["tail_behavior"]),
        "tail_behavior_ba": str(tail_ba["tail_behavior"]),
        "tail_behavior_common": (
            str(tail_ab["tail_behavior"])
            if str(tail_ab["tail_behavior"]) == str(tail_ba["tail_behavior"])
            else "order_ambiguous_tail"
        ),
    }
    return component_rows, event_rows, summary_row


def recommendation_rows(summary_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    clean_order = all(int(row["order_ambiguous"]) == 0 for row in summary_rows)
    clean_ctrl = min((safe_float(row["mean_control_consistency"]) for row in summary_rows), default=1.0) >= 0.95
    recs = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (clean_order and clean_ctrl) else "unclear",
            "note": (
                "Order-control holder seg samkjørt og matched controls forblir stabile gjennom den lengre horisonten."
                if (clean_order and clean_ctrl)
                else "Enten order-control eller matched controls spriker i den lange trace-runden."
            ),
        }
    ]

    prefix_match_rate = mean_defined(float(row["prefix_matches_expected"]) for row in summary_rows)
    distinct_tails = sorted({str(row["tail_behavior_common"]) for row in summary_rows})
    distinct_full_chains = sorted({str(row["full_chain_label"]) for row in summary_rows})

    if prefix_match_rate < 0.75:
        status = "failed_trace_reconstruction"
        note = (
            f"De valgte representative tracene reproduserer ikke v15g godt nok på prefix-horisonten (match-rate {prefix_match_rate:.3f})."
        )
        next_status = "repair_trace_selection"
        next_note = "Neste steg bør være å reparere trace-utvalget eller seed-koblingen før videre tolkning."
    elif len(distinct_tails) >= 2:
        status = "long_horizon_family_difference"
        note = (
            f"Representative tracene holder ikke én felles senfase; tail-behavior skiller seg på tvers av tracene ({', '.join(distinct_tails)})."
        )
        next_status = "follow_trace_genealogies"
        next_note = "Neste steg bør følge noen få representative traces enda mer direkte, ikke starte ny bred pair-scan."
    elif len(distinct_full_chains) == 1 and distinct_full_chains[0] == "split_persistent_dual":
        status = "late_collapse_to_dual"
        note = "De tidlige chain-forskjellene ser ut til å kollapse mot en felles `split_persistent_dual`-lesning senere i løpet."
        next_status = "probe_dual_stability"
        next_note = "Neste steg bør teste hvor stabil den vedvarende dual-strukturen faktisk er, heller enn å lete etter flere coarse kollisjonstyper."
    else:
        status = "partially_structured"
        note = (
            f"Langhorisonten bevarer noe chain-struktur, men ikke rent nok til å kalle én endelig familiehistorie ({', '.join(distinct_full_chains)})."
        )
        next_status = "follow_trace_genealogies"
        next_note = "Neste steg bør være få representative traces med enda rikere hendelsesforklaringer, ikke mer offset-mikrotuning."

    recs.append({"diagnostic_family": "trace_signal", "status": status, "note": note})
    recs.append({"diagnostic_family": "next_step", "status": next_status, "note": next_note})
    return recs


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def build_report(
    *,
    target_summary: Sequence[Dict[str, Any]],
    summary_rows: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15h: representative collision traces")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden følger noen få representative v15g-traces lenger i tid. Målet er å se om de tidlige genealogy-chainene fortsatt bærer informasjon på lang horisont, eller om de kollapser til en felles senfase."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Representative traces")
    lines.append("")
    lines.append("| trace | pair | offset | expected prefix | prefix chain | full chain | tail | final comps | tail dual |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in summary_rows:
        lines.append(
            f"| {row['trace_label']} | {row['pair_label']} | {int(row['run_offset'])} | {row['expected_prefix_chain']} | {row['prefix_chain_label']} | {row['full_chain_label']} | {row['tail_behavior_common']} | {fmt(row['final_component_count'])} | {fmt(row['tail_dual_fraction'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Disse trace-kjedene er fortsatt diagnostiske arbeidskategorier, ikke partikkelbevis.")
    lines.append("- Langhorisont-runden brukes her til å teste om tidlige chain-navn holder eller vaskes ut senere.")
    lines.append("- Hvis flere traces ender likt sent, er det en nyttig negativ innsikt, ikke et nederlag.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15h representative collision traces.")
    p.add_argument("--out-component-csv", type=str, default="Documentation/v15h_representative_trace_component_trajectories.csv")
    p.add_argument("--out-event-log-csv", type=str, default="Documentation/v15h_representative_trace_event_log.csv")
    p.add_argument("--out-summary-csv", type=str, default="Documentation/v15h_representative_trace_summary.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15h_representative_trace_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15h_representative_collision_traces.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15h_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15h.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15b.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [PRIMARY_GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base = base_states[(ensembles[0].name, PRIMARY_GROWTH_SEED)]

    component_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []
    summary_rows: List[Dict[str, Any]] = []

    for spec in TRACE_SPECS:
        comp_rows, ev_rows, summary = run_long_trace(
            base=base,
            pair=tuple(spec["pair"]),
            trace_label=str(spec["trace_label"]),
            run_offset=int(spec["run_offset"]),
            expected_prefix_chain=str(spec["expected_prefix_chain"]),
        )
        component_rows.extend(comp_rows)
        event_rows.extend(ev_rows)
        summary_rows.append(summary)

    recommendation = recommendation_rows(summary_rows)
    report_md = build_report(
        target_summary=target_summary,
        summary_rows=summary_rows,
        recommendation=recommendation,
    )
    op_md = "\n".join(
        [
            "# v0.15h operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Les denne runden som langhorisont-sporing av representative collisions, ikke som ny familieoppløsning i bredde.",
            "- Ikke les tail-behavior som bevis på partikler eller universelle defect-arter.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15h",
            "",
            "Denne runden tok noen få typiske kollisjonseksempler fra forrige eksperiment og lot dem gå mye lenger.",
            "",
            "Målet var ikke å finne flere kollisjonspar. Målet var å se om de tidlige mønstrene vi hadde oppdaget fortsatt ga mening senere i forløpet, eller om alt bare endte opp likt.",
            "",
            "Det viktigste å passe på her er at disse mønstrene fortsatt bare er arbeidskategorier. De er ikke bevis på partikler eller ny fysikk. Men de kan hjelpe oss avgjøre om det finnes repeterbare typer hendelsesforløp i systemet.",
            "",
            "Hvis flere representative forløp beholder forskjellige senfaser, er det et tegn på at collision-sporet fortsatt er verdt å følge. Hvis de vaskes ut til samme type sluttoppførsel, lærer vi også noe viktig: da var de tidlige forskjellene mindre dype enn de først så ut.",
        ]
    ) + "\n"

    write_csv(args.out_component_csv, component_rows)
    write_csv(args.out_event_log_csv, event_rows)
    write_csv(args.out_summary_csv, summary_rows)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
