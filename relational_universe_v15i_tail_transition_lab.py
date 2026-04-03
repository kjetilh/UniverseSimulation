#!/usr/bin/env python3
"""v0.15i tail transition lab built on v15h representative traces.

This is a narrow follow-up to v15h. It does not run new broad collision scans.
Instead it reads the long-horizon representative traces and asks whether the
late-time tail can be decomposed into a small number of more explicit
transition patterns.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, DefaultDict, Dict, Iterable, List, Mapping, Sequence, Tuple


V15H_SUMMARY = "Documentation/v15h_representative_trace_summary.csv"
V15H_COMPONENTS = "Documentation/v15h_representative_trace_component_trajectories.csv"
V15H_EVENTS = "Documentation/v15h_representative_trace_event_log.csv"
V15H_TARGET = "Documentation/v15h_representative_trace_target_summary.csv"


def safe_float(x: Any, default: float = float("nan")) -> float:
    try:
        y = float(x)
    except (TypeError, ValueError):
        return default
    return y


def mean_defined(values: Iterable[float]) -> float:
    vals = [float(v) for v in values if math.isfinite(float(v))]
    if not vals:
        return float("nan")
    return sum(vals) / len(vals)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def tail_transition_label(
    *,
    final_component_count: int,
    total_major_events: int,
    topology_change_count: int,
    birth_death_total: int,
    split_count: int,
    merge_count: int,
    quiet_suffix_steps: int,
    tail_dual_fraction: float,
) -> str:
    if final_component_count <= 1 and total_major_events == 0 and topology_change_count == 0:
        return "quiet_singleton_lock"
    if (
        final_component_count <= 1
        and birth_death_total == 0
        and split_count >= 2
        and merge_count >= 2
        and quiet_suffix_steps >= 40
    ):
        return "merge_rebound_lock"
    if (
        final_component_count <= 1
        and birth_death_total >= 2
        and total_major_events >= 4
        and quiet_suffix_steps >= 60
    ):
        return "fragmenting_lock"
    if final_component_count >= 2 and tail_dual_fraction >= 0.75:
        return "persistent_dual_tail"
    return "mixed_tail_transition"


def major_event_type(row: Mapping[str, str]) -> bool:
    return str(row["event_type"]) in {"split", "merge", "birth", "death"}


def derive_trace_rows(
    summary_rows: Sequence[Mapping[str, str]],
    component_rows: Sequence[Mapping[str, str]],
    event_rows: Sequence[Mapping[str, str]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    by_trace_order_components: DefaultDict[Tuple[str, str], List[Dict[str, str]]] = defaultdict(list)
    by_trace_order_events: DefaultDict[Tuple[str, str], List[Dict[str, str]]] = defaultdict(list)
    for row in component_rows:
        by_trace_order_components[(str(row["trace_label"]), str(row["order"]))].append(dict(row))
    for row in event_rows:
        by_trace_order_events[(str(row["trace_label"]), str(row["order"]))].append(dict(row))

    order_rows: List[Dict[str, Any]] = []
    segment_rows: List[Dict[str, Any]] = []
    summary_out: List[Dict[str, Any]] = []

    for summary in summary_rows:
        trace_label = str(summary["trace_label"])
        expected_prefix_chain = str(summary["expected_prefix_chain"])
        tail_start_step = int(float(summary["tail_start_step"]))
        trace_order_labels: List[str] = []
        trace_order_rows: List[Dict[str, Any]] = []

        for order in ("ab", "ba"):
            comp_rows = sorted(
                by_trace_order_components[(trace_label, order)],
                key=lambda r: (int(r["snapshot_index"]), int(r["component_local_index"])),
            )
            event_subrows = sorted(
                by_trace_order_events[(trace_label, order)],
                key=lambda r: (int(r["snapshot_index_to"]), int(r["step_to"]), str(r["event_type"])),
            )

            snapshots: List[Dict[str, Any]] = []
            last_snapshot_idx = None
            current = None
            for row in comp_rows:
                snapshot_idx = int(row["snapshot_index"])
                if snapshot_idx != last_snapshot_idx:
                    if current is not None:
                        snapshots.append(current)
                    current = {
                        "snapshot_index": snapshot_idx,
                        "step": int(row["step"]),
                        "component_count": int(row["component_count"]),
                        "total_defect_mass": int(row["total_defect_mass"]),
                    }
                    last_snapshot_idx = snapshot_idx
            if current is not None:
                snapshots.append(current)

            tail_snapshots = [row for row in snapshots if int(row["step"]) >= tail_start_step]
            tail_events = [row for row in event_subrows if int(row["step_to"]) >= tail_start_step and major_event_type(row)]

            split_count = sum(1 for row in tail_events if str(row["event_type"]) == "split")
            merge_count = sum(1 for row in tail_events if str(row["event_type"]) == "merge")
            birth_count = sum(1 for row in tail_events if str(row["event_type"]) == "birth")
            death_count = sum(1 for row in tail_events if str(row["event_type"]) == "death")
            total_major_events = split_count + merge_count + birth_count + death_count

            topology_change_count = sum(
                1
                for a, b in zip(tail_snapshots, tail_snapshots[1:])
                if int(a["component_count"]) != int(b["component_count"])
            )
            dual_fraction = mean_defined(
                1.0 if int(row["component_count"]) >= 2 else 0.0 for row in tail_snapshots
            )
            final_component_count = int(tail_snapshots[-1]["component_count"]) if tail_snapshots else -1
            final_total_defect_mass = int(tail_snapshots[-1]["total_defect_mass"]) if tail_snapshots else -1
            last_major_step = max((int(row["step_to"]) for row in tail_events), default=-1)
            quiet_suffix_steps = (
                (int(tail_snapshots[-1]["step"]) - last_major_step)
                if tail_snapshots and last_major_step >= 0
                else (int(tail_snapshots[-1]["step"]) - tail_start_step if tail_snapshots else -1)
            )

            label = tail_transition_label(
                final_component_count=final_component_count,
                total_major_events=total_major_events,
                topology_change_count=topology_change_count,
                birth_death_total=birth_count + death_count,
                split_count=split_count,
                merge_count=merge_count,
                quiet_suffix_steps=quiet_suffix_steps,
                tail_dual_fraction=safe_float(dual_fraction),
            )
            trace_order_labels.append(label)

            order_row = {
                "trace_label": trace_label,
                "pair_label": str(summary["pair_label"]),
                "order": order,
                "expected_prefix_chain": expected_prefix_chain,
                "prefix_chain_label": str(summary["prefix_chain_label"]),
                "full_chain_label": str(summary["full_chain_label"]),
                "tail_start_step": tail_start_step,
                "tail_snapshot_count": len(tail_snapshots),
                "split_count": int(split_count),
                "merge_count": int(merge_count),
                "birth_count": int(birth_count),
                "death_count": int(death_count),
                "total_major_events": int(total_major_events),
                "topology_change_count": int(topology_change_count),
                "tail_dual_fraction": safe_float(dual_fraction),
                "final_component_count": int(final_component_count),
                "final_total_defect_mass": int(final_total_defect_mass),
                "last_major_step": int(last_major_step),
                "quiet_suffix_steps": int(quiet_suffix_steps),
                "tail_transition_label": label,
            }
            order_rows.append(order_row)
            trace_order_rows.append(order_row)

            prev_event_step = None
            segment_index = 0
            current_segment_events: List[Dict[str, str]] = []
            for event in tail_events:
                step_to = int(event["step_to"])
                if prev_event_step is None or (step_to - prev_event_step) <= 40:
                    current_segment_events.append(event)
                else:
                    segment_index += 1
                    current_segment_events = [event]
                prev_event_step = step_to

                counts = defaultdict(int)
                for row in current_segment_events:
                    counts[str(row["event_type"])] += 1
                segment_rows.append(
                    {
                        "trace_label": trace_label,
                        "order": order,
                        "segment_index": segment_index,
                        "segment_start_step": int(current_segment_events[0]["step_to"]),
                        "segment_end_step": int(current_segment_events[-1]["step_to"]),
                        "segment_event_count": len(current_segment_events),
                        "split_count": counts["split"],
                        "merge_count": counts["merge"],
                        "birth_count": counts["birth"],
                        "death_count": counts["death"],
                    }
                )

        common_tail = trace_order_labels[0] if len(set(trace_order_labels)) == 1 else "order_ambiguous_tail"
        summary_out.append(
            {
                "trace_label": trace_label,
                "pair_label": str(summary["pair_label"]),
                "expected_prefix_chain": expected_prefix_chain,
                "prefix_chain_label": str(summary["prefix_chain_label"]),
                "full_chain_label": str(summary["full_chain_label"]),
                "v15h_tail_behavior_common": str(summary["tail_behavior_common"]),
                "order_ambiguous_tail": 0 if common_tail != "order_ambiguous_tail" else 1,
                "tail_transition_label": common_tail,
                "tail_transition_labels_by_order": ",".join(trace_order_labels),
                "mean_total_major_events": mean_defined(float(row["total_major_events"]) for row in trace_order_rows),
                "mean_topology_change_count": mean_defined(float(row["topology_change_count"]) for row in trace_order_rows),
                "mean_tail_dual_fraction": mean_defined(float(row["tail_dual_fraction"]) for row in trace_order_rows),
                "mean_quiet_suffix_steps": mean_defined(float(row["quiet_suffix_steps"]) for row in trace_order_rows),
                "final_component_count": mean_defined(float(row["final_component_count"]) for row in trace_order_rows),
                "final_total_defect_mass": mean_defined(float(row["final_total_defect_mass"]) for row in trace_order_rows),
            }
        )

    aggregate_rows: List[Dict[str, Any]] = []
    by_label: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in summary_out:
        by_label[str(row["tail_transition_label"])].append(row)
    total = max(1, len(summary_out))
    for label, rows in sorted(by_label.items()):
        aggregate_rows.append(
            {
                "tail_transition_label": label,
                "n_traces": len(rows),
                "rate": len(rows) / total,
                "mean_total_major_events": mean_defined(safe_float(row["mean_total_major_events"]) for row in rows),
                "mean_topology_change_count": mean_defined(safe_float(row["mean_topology_change_count"]) for row in rows),
                "mean_tail_dual_fraction": mean_defined(safe_float(row["mean_tail_dual_fraction"]) for row in rows),
                "mean_quiet_suffix_steps": mean_defined(safe_float(row["mean_quiet_suffix_steps"]) for row in rows),
            }
        )

    return order_rows, segment_rows, summary_out, aggregate_rows


def recommendation_rows(summary_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    order_clean = all(int(row["order_ambiguous_tail"]) == 0 for row in summary_rows)
    labels = sorted({str(row["tail_transition_label"]) for row in summary_rows})
    out = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if order_clean else "unclear",
            "note": (
                "Tail-overgangene er order-stabile i denne runden."
                if order_clean
                else "Tail-overgangene spriker mellom AB og BA for minst ett representativt trace."
            ),
        }
    ]
    if order_clean and len(labels) >= 3:
        signal_status = "tail_families_sharpened"
        signal_note = (
            f"v15h sine grove tail-typer brytes videre ned i minst tre repeterbare overganger ({', '.join(labels)})."
        )
        next_status = "trace_event_explanations"
        next_note = "Neste steg bør forklare disse overgangene med eksplisitte hendelseskjeder, ikke ny bred pair-scan."
    elif order_clean and len(labels) == 2:
        signal_status = "tail_families_partially_sharpened"
        signal_note = (
            f"Senfasen er skarpere enn i v15h, men samler seg fortsatt bare i to overgangstyper ({', '.join(labels)})."
        )
        next_status = "trace_event_explanations"
        next_note = "Neste steg bør forklare hva som skiller de to tail-overgangene eksplisitt."
    else:
        signal_status = "tail_signal_still_mixed"
        signal_note = "Tail-overgangene blir ikke renere nok til å bære en tydelig ny familiestruktur ennå."
        next_status = "pause_new_scans"
        next_note = "Neste steg bør være forklarende analyse av få traces eller et nytt defect-spørsmål, ikke flere små pair-iterasjoner."
    out.append({"diagnostic_family": "tail_signal", "status": signal_status, "note": signal_note})
    out.append({"diagnostic_family": "next_step", "status": next_status, "note": next_note})
    return out


def build_report(
    *,
    target_rows: Sequence[Mapping[str, str]],
    summary_rows: Sequence[Mapping[str, Any]],
    aggregate_rows: Sequence[Mapping[str, Any]],
    recommendation: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15i: tail transition lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden analyserer bare de representative v15h-tracene. Målet er å gjøre senfase-overgangene mer presise enn `mixed_tail` og `rebound_merge_tail`."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_rows:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Trace-tail overganger")
    lines.append("")
    lines.append("| trace | prefix chain | v15h tail | v15i tail | major events | topology changes | quiet suffix |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in summary_rows:
        lines.append(
            f"| {row['trace_label']} | {row['prefix_chain_label']} | {row['v15h_tail_behavior_common']} | {row['tail_transition_label']} | {fmt(row['mean_total_major_events'])} | {fmt(row['mean_topology_change_count'])} | {fmt(row['mean_quiet_suffix_steps'])} |"
        )
    lines.append("")
    lines.append("## Aggregate tail labels")
    lines.append("")
    lines.append("| tail label | n traces | rate | mean events | mean changes | mean quiet suffix |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in aggregate_rows:
        lines.append(
            f"| {row['tail_transition_label']} | {int(row['n_traces'])} | {fmt(row['rate'])} | {fmt(row['mean_total_major_events'])} | {fmt(row['mean_topology_change_count'])} | {fmt(row['mean_quiet_suffix_steps'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt trace-diagnostikk, ikke bevis på partikler eller universelle defect-arter.")
    lines.append("- Poenget er å se om senfasen kan deles opp i noen få repeterbare overgangstyper.")
    lines.append("- Hvis vi får flere slike typer enn i v15h, betyr det at collision-sporet blir mer forklarbart uten å bli oversolgt.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15i tail transition lab.")
    p.add_argument("--summary-in", type=str, default=V15H_SUMMARY)
    p.add_argument("--components-in", type=str, default=V15H_COMPONENTS)
    p.add_argument("--events-in", type=str, default=V15H_EVENTS)
    p.add_argument("--target-in", type=str, default=V15H_TARGET)
    p.add_argument("--out-order-csv", type=str, default="Documentation/v15i_tail_transition_order_rows.csv")
    p.add_argument("--out-segments-csv", type=str, default="Documentation/v15i_tail_transition_segments.csv")
    p.add_argument("--out-summary-csv", type=str, default="Documentation/v15i_tail_transition_summary.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15i_tail_transition_aggregate.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15i_tail_transition_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15i_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15i.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    summary_rows = read_csv(args.summary_in)
    component_rows = read_csv(args.components_in)
    event_rows = read_csv(args.events_in)
    target_rows = read_csv(args.target_in)

    order_rows, segment_rows, trace_rows, aggregate_rows = derive_trace_rows(
        summary_rows=summary_rows,
        component_rows=component_rows,
        event_rows=event_rows,
    )
    recommendation = recommendation_rows(trace_rows)
    report_md = build_report(
        target_rows=target_rows,
        summary_rows=trace_rows,
        aggregate_rows=aggregate_rows,
        recommendation=recommendation,
    )
    op_md = "\n".join(
        [
            "# v0.15i operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Les denne runden som en skarpere senfase-lesning av representative traces, ikke som ny fysikk.",
            "- Ikke les nye tail-labels som defect-arter; les dem som arbeidskategorier for sporbar senmorfologi.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15i",
            "",
            "Denne runden tok de lange kollisjonseksemplene fra v15h og beskrev slutten av dem mer presist.",
            "",
            "I stedet for bare å si at en senfase var \"blandet\" eller \"rebound\", prøvde vi å se om sluttfasen faktisk faller i noen få repeterbare overgangstyper.",
            "",
            "Det viktige her er fortsatt nøkternhet: dette er arbeidskategorier for hvordan et forløp slutter, ikke bevis på nye partikler eller arter i systemet.",
            "",
            "Hvis senfasen blir skarpere på denne måten, betyr det at vi gradvis får en mer forklarbar defect-dynamikk uten å måtte lete bredt i nye offset-runder.",
        ]
    ) + "\n"

    write_csv(args.out_order_csv, order_rows)
    write_csv(args.out_segments_csv, segment_rows)
    write_csv(args.out_summary_csv, trace_rows)
    write_csv(args.out_aggregate_csv, aggregate_rows)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
