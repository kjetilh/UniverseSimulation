#!/usr/bin/env python3
"""v0.15bt same-locus carrier timing lab.

After v15bs showed that add_chord and local_swap are close on static same-locus
carrier summaries, test whether they differ more clearly in timing texture:

- when shell fragmentation starts
- how strongly it locks in
- how attachment behaves once fragmentation starts
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15af_add_chord_shell_fragment_event_lab as v15af
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 96
GROWTH_SEED = 202
PLACEMENT = 3
SEED_DELTAS = (719, 751, 787, 823, 859, 887)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
PERTURBATIONS = ("add_chord", "local_swap")


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


def segment_rows_for_run(
    *,
    perturbation: str,
    seed_delta: int,
    run_seed: int,
    support_signature: str,
    rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if not rows:
        return out
    states = [v15af.shell_state({k: str(v) for k, v in row.items()}) for row in rows]
    start = 0
    for idx in range(1, len(rows) + 1):
        if idx < len(rows) and states[idx] == states[start]:
            continue
        seg_rows = rows[start:idx]
        attach = [safe_float(r["shell_attachment_node_frac"]) for r in seg_rows if math.isfinite(safe_float(r["shell_attachment_node_frac"]))]
        boundary = [safe_float(r["shell_boundary_to_volume"]) for r in seg_rows if math.isfinite(safe_float(r["shell_boundary_to_volume"]))]
        active_nodes = [safe_float(r["shell_active_nodes"]) for r in seg_rows]
        out.append(
            {
                "perturbation": perturbation,
                "seed_delta": int(seed_delta),
                "run_seed": int(run_seed),
                "support_signature": support_signature,
                "segment_index": int(len(out)),
                "segment_state": states[start],
                "start_snapshot_index": int(seg_rows[0]["snapshot_index"]),
                "end_snapshot_index": int(seg_rows[-1]["snapshot_index"]),
                "start_step": int(seg_rows[0]["step"]),
                "end_step": int(seg_rows[-1]["step"]),
                "segment_snapshot_count": int(len(seg_rows)),
                "mean_attachment_node_frac": mean_defined(attach),
                "mean_shell_boundary_to_volume": mean_defined(boundary),
                "mean_shell_active_nodes": mean_defined(active_nodes),
            }
        )
        start = idx
    return out


def classify_timing_texture(
    *,
    first_fragment_local_index: int,
    fragmented_suffix_rate: float,
    state_switch_count: int,
    first_fragment_attachment: float,
    max_connected_segment_snapshots: int,
) -> str:
    if first_fragment_local_index >= 0 and first_fragment_local_index <= 1 and fragmented_suffix_rate >= 0.85:
        if first_fragment_attachment >= 0.85:
            return "anchored_early_fragment_lock"
        return "looser_early_fragment_lock"
    if first_fragment_local_index >= 2 and fragmented_suffix_rate >= 0.85:
        return "delayed_fragment_lock"
    if fragmented_suffix_rate < 0.45 and state_switch_count >= 6 and max_connected_segment_snapshots >= 16:
        return "connected_resistance_churn"
    if fragmented_suffix_rate >= 0.45 and state_switch_count >= 6:
        return "intermittent_fragment_churn"
    return "mixed_fragment_timing"


def analyze_run(
    *,
    perturbation: str,
    seed_delta: int,
    run_seed: int,
    support_signature: str,
    snapshot_rows: Sequence[Mapping[str, Any]],
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    active_rows = [row for row in snapshot_rows if int(row["shell_active_nodes"]) > 0]
    active_states = [v15af.shell_state({k: str(v) for k, v in row.items()}) for row in active_rows]
    frag_flags = [1 if st == "fragmented" else 0 for st in active_states]
    first_fragment_local_index = next((i for i, x in enumerate(frag_flags) if x == 1), -1)
    first_fragment_step = int(active_rows[first_fragment_local_index]["step"]) if first_fragment_local_index >= 0 else -1
    fragmented_suffix = frag_flags[first_fragment_local_index:] if first_fragment_local_index >= 0 else []
    fragmented_suffix_rate = (sum(fragmented_suffix) / len(fragmented_suffix)) if fragmented_suffix else 0.0
    state_switch_count = sum(1 for a, b in zip(active_states, active_states[1:]) if a != b)

    segments = segment_rows_for_run(
        perturbation=perturbation,
        seed_delta=seed_delta,
        run_seed=run_seed,
        support_signature=support_signature,
        rows=active_rows,
    )
    frag_segments = [row for row in segments if str(row["segment_state"]) == "fragmented"]
    connected_segments = [row for row in segments if str(row["segment_state"]) == "connected"]
    first_fragment_attachment = safe_float(frag_segments[0]["mean_attachment_node_frac"]) if frag_segments else float("nan")
    max_connected_segment_snapshots = max((int(row["segment_snapshot_count"]) for row in connected_segments), default=0)
    timing_label = classify_timing_texture(
        first_fragment_local_index=int(first_fragment_local_index),
        fragmented_suffix_rate=float(fragmented_suffix_rate),
        state_switch_count=int(state_switch_count),
        first_fragment_attachment=safe_float(first_fragment_attachment, 0.0),
        max_connected_segment_snapshots=int(max_connected_segment_snapshots),
    )
    run_row = {
        "perturbation": perturbation,
        "target_nodes": TARGET,
        "growth_seed": GROWTH_SEED,
        "placement": PLACEMENT,
        "seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "support_signature": support_signature,
        "first_fragment_local_index": int(first_fragment_local_index),
        "first_fragment_step": int(first_fragment_step),
        "fragmented_suffix_rate": float(fragmented_suffix_rate),
        "state_switch_count": int(state_switch_count),
        "segment_count": int(len(segments)),
        "first_fragment_attachment": safe_float(first_fragment_attachment),
        "max_connected_segment_snapshots": int(max_connected_segment_snapshots),
        "final_shell_state": active_states[-1] if active_states else "inactive",
        "timing_label": timing_label,
    }
    return run_row, segments


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for perturbation in PERTURBATIONS:
        group = [row for row in rows if str(row["perturbation"]) == perturbation]
        out.append(
            {
                "perturbation": perturbation,
                "n_runs": len(group),
                "anchored_early_fragment_lock_rate": mean_defined(
                    1.0 if str(row["timing_label"]) == "anchored_early_fragment_lock" else 0.0 for row in group
                ),
                "looser_early_fragment_lock_rate": mean_defined(
                    1.0 if str(row["timing_label"]) == "looser_early_fragment_lock" else 0.0 for row in group
                ),
                "delayed_fragment_lock_rate": mean_defined(
                    1.0 if str(row["timing_label"]) == "delayed_fragment_lock" else 0.0 for row in group
                ),
                "intermittent_fragment_churn_rate": mean_defined(
                    1.0 if str(row["timing_label"]) == "intermittent_fragment_churn" else 0.0 for row in group
                ),
                "connected_resistance_churn_rate": mean_defined(
                    1.0 if str(row["timing_label"]) == "connected_resistance_churn" else 0.0 for row in group
                ),
                "mean_first_fragment_step": mean_defined(
                    safe_float(row["first_fragment_step"]) for row in group if int(row["first_fragment_step"]) >= 0
                ),
                "mean_fragmented_suffix_rate": mean_defined(safe_float(row["fragmented_suffix_rate"]) for row in group),
                "mean_state_switch_count": mean_defined(safe_float(row["state_switch_count"]) for row in group),
                "mean_first_fragment_attachment": mean_defined(safe_float(row["first_fragment_attachment"]) for row in group),
            }
        )
    return out


def comparison_row(aggregate: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    by = {str(row["perturbation"]): dict(row) for row in aggregate}
    add = by["add_chord"]
    swap = by["local_swap"]
    return {
        "compare_label": "carrier_timing_add_chord_vs_local_swap_at_96_p3",
        "anchored_lock_gap_add_minus_swap": safe_float(add["anchored_early_fragment_lock_rate"]) - safe_float(swap["anchored_early_fragment_lock_rate"]),
        "looser_lock_gap_add_minus_swap": safe_float(add["looser_early_fragment_lock_rate"]) - safe_float(swap["looser_early_fragment_lock_rate"]),
        "delayed_lock_gap_add_minus_swap": safe_float(add["delayed_fragment_lock_rate"]) - safe_float(swap["delayed_fragment_lock_rate"]),
        "churn_gap_swap_minus_add": safe_float(swap["intermittent_fragment_churn_rate"]) - safe_float(add["intermittent_fragment_churn_rate"]),
        "first_fragment_step_gap_swap_minus_add": safe_float(swap["mean_first_fragment_step"]) - safe_float(add["mean_first_fragment_step"]),
        "attachment_gap_add_minus_swap": safe_float(add["mean_first_fragment_attachment"]) - safe_float(swap["mean_first_fragment_attachment"]),
        "switch_gap_swap_minus_add": safe_float(swap["mean_state_switch_count"]) - safe_float(add["mean_state_switch_count"]),
    }


def diagnosis_rows(target_summary: Sequence[Mapping[str, Any]], run_rows: Sequence[Mapping[str, Any]], aggregate: Sequence[Mapping[str, Any]], compare: Mapping[str, Any]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    anchored_gap = safe_float(compare["anchored_lock_gap_add_minus_swap"])
    churn_gap = safe_float(compare["churn_gap_swap_minus_add"])
    attachment_gap = safe_float(compare["attachment_gap_add_minus_swap"])
    if anchored_gap >= 0.30 and attachment_gap >= 0.05:
        status = "add_chord_anchor_lock_edge_supported"
        note = "add_chord gar oftere tidlig inn i en forankret fragment-lock enn local_swap ved samme locus."
        next_step = "compare_lock_geometry_to_spectral"
        next_note = "Neste steg bor knytte denne timing-fordelen til hvilke geometri-sider add_chord faktisk baerer bedre."
    elif churn_gap >= 0.30:
        status = "local_swap_churn_edge_supported"
        note = "local_swap holder oftere en mer churn-preget timingtekstur enn add_chord ved samme locus."
        next_step = "probe_churn_invariant_link"
        next_note = "Neste steg bor teste om spectral-signalet faktisk er koblet til denne churn-teksturen."
    else:
        status = "carrier_timing_still_mixed"
        note = "Timing-observabelen gjor ikke carrier-duellen ren nok ved samme locus."
        next_step = "new_cross_carrier_observable"
        next_note = "Neste steg bor bruke en helt ny carrier-observabel, ikke flere timing-varianter av samme duell."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsen er ren og alle timing-runs matcher onsket perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "carrier_timing_compare",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    compare: Mapping[str, Any],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bt: same-locus carrier timing lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om add_chord og local_swap skiller lag tydeligere i timingtekstur enn i de statiske carrier-maalingene fra v15bs.")
    lines.append("")
    lines.append("## Startstorrelse")
    lines.append("")
    lines.append("| target | mean initial | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Timing summary")
    lines.append("")
    lines.append("| perturbation | anchored early lock | looser early lock | delayed lock | churn | first fragment step | first fragment attach | switches |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['perturbation']} | {fmt(row['anchored_early_fragment_lock_rate'])} | {fmt(row['looser_early_fragment_lock_rate'])} | {fmt(row['delayed_fragment_lock_rate'])} | {fmt(row['intermittent_fragment_churn_rate'])} | {fmt(row['mean_first_fragment_step'])} | {fmt(row['mean_first_fragment_attachment'])} | {fmt(row['mean_state_switch_count'])} |"
        )
    lines.append("")
    lines.append("## Timing deltas")
    lines.append("")
    lines.append("| anchored gap add-swap | churn gap swap-add | fragment step gap swap-add | attach gap add-swap | switch gap swap-add |")
    lines.append("| --- | --- | --- | --- | --- |")
    lines.append(
        f"| {fmt(compare['anchored_lock_gap_add_minus_swap'])} | {fmt(compare['churn_gap_swap_minus_add'])} | {fmt(compare['first_fragment_step_gap_swap_minus_add'])} | {fmt(compare['attachment_gap_add_minus_swap'])} | {fmt(compare['switch_gap_swap_minus_add'])} |"
    )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en timingobservabel pa samme locus, ikke en ny bred carrier-scan.")
    lines.append("- Positivt signal her betyr bare at carrierne skiller lag i hvordan de laaser seg inn i halen, ikke at vi allerede har en full geometri-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bt same-locus carrier timing lab.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15bt_same_locus_carrier_timing_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15bt_same_locus_carrier_timing_runs.csv")
    p.add_argument("--out-segments-csv", type=str, default="Documentation/v15bt_same_locus_carrier_timing_segments.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15bt_same_locus_carrier_timing_aggregate.csv")
    p.add_argument("--out-compare-csv", type=str, default="Documentation/v15bt_same_locus_carrier_timing_compare.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bt_same_locus_carrier_timing_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bt_same_locus_carrier_timing_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bt_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bt.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    run_rows: List[Dict[str, Any]] = []
    segment_rows: List[Dict[str, Any]] = []

    for perturbation in PERTURBATIONS:
        for seed_delta in SEED_DELTAS:
            run_seed = TARGET * 100000 + GROWTH_SEED * 1000 + PLACEMENT * 100 + int(seed_delta)
            if perturbation == "local_swap":
                run_seed += 7
            res = v15ae.run_defect_with_control_graphs(
                base_state,
                params=params,
                seed=run_seed,
                steps=FULL_STEPS,
                perturbation=perturbation,
                center_token_index=PLACEMENT,
                local_coupling="maximal",
                log_every=LOG_EVERY,
            )
            info = dict(res["perturbation_info"])
            support = [int(x) for x in info.get("support", [])]
            partition = v15ae.occupancy_partition(res["damaged_sets"])
            snapshots = v15ae.shell_snapshot_rows(
                placement=PLACEMENT,
                seed_delta=seed_delta,
                run_seed=run_seed,
                support_signature=",".join(str(x) for x in support),
                core_nodes=set(partition["core_nodes"]),
                shell_nodes=set(partition["shell_nodes"]),
                log_rows=res["log_rows"],
                damaged_sets=res["damaged_sets"],
                control_graphs=res["control_graphs"],
            )
            run_row, segments = analyze_run(
                perturbation=perturbation,
                seed_delta=seed_delta,
                run_seed=run_seed,
                support_signature=",".join(str(x) for x in support),
                snapshot_rows=snapshots,
            )
            run_row["requested_match"] = int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown"))))
            run_rows.append(run_row)
            segment_rows.extend(segments)

    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    aggregate = aggregate_rows(run_rows)
    compare = comparison_row(aggregate)
    diagnosis = diagnosis_rows(target_summary, run_rows, aggregate, compare)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, compare=compare, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bt operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en timingobservabel ved samme locus, ikke som en ny bred carrier-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bt",
            "",
            "Denne runden sammenlikner ikke bare hvor store skadesporene blir, men hvordan de faller inn i sin sene form over tid.",
            "",
            "Poenget er å se om de to forstyrrelsene har ulik rytme og låsemåte, selv når sluttbildene ser ganske like ut.",
        ]
    ) + "\n"
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_segments_csv, segment_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_compare_csv, [compare])
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
