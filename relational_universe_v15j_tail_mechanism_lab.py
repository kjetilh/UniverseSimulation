#!/usr/bin/env python3
"""v0.15j tail mechanism lab.

This follows v15i. The goal is not to produce new tail labels, but to explain
the existing late-time transition types with explicit segment-level mechanisms.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, DefaultDict, Dict, Iterable, List, Mapping, Sequence, Tuple


V15H_TARGET = "Documentation/v15h_representative_trace_target_summary.csv"
V15I_ORDER = "Documentation/v15i_tail_transition_order_rows.csv"
V15I_SEGMENTS = "Documentation/v15i_tail_transition_segments.csv"
V15I_SUMMARY = "Documentation/v15i_tail_transition_summary.csv"


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


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


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


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def classify_segment_mechanism(
    *,
    total_major_events: int,
    segment_count: int,
    birth_count: int,
    death_count: int,
    split_count: int,
    merge_count: int,
    quiet_suffix_steps: int,
    topology_change_count: int,
) -> str:
    if total_major_events == 0 and segment_count == 0 and quiet_suffix_steps >= 200:
        return "quiet_relaxation_lock"
    if (
        segment_count >= 2
        and birth_count == 0
        and death_count == 0
        and split_count >= 4
        and merge_count >= 4
        and abs(split_count - merge_count) <= 2
        and quiet_suffix_steps >= 40
    ):
        return "balanced_rebound_cycle"
    if (
        segment_count >= 1
        and (birth_count + death_count) >= 2
        and split_count >= 2
        and merge_count >= 1
        and topology_change_count >= 8
        and quiet_suffix_steps >= 60
    ):
        return "fragmenting_repair_cycle"
    return "mixed_mechanism"


def derive_rows(
    *,
    order_rows: Sequence[Mapping[str, str]],
    segment_rows: Sequence[Mapping[str, str]],
    summary_rows: Sequence[Mapping[str, str]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    by_trace_order_segments: DefaultDict[Tuple[str, str], List[Dict[str, str]]] = defaultdict(list)
    for row in segment_rows:
        by_trace_order_segments[(str(row["trace_label"]), str(row["order"]))].append(dict(row))

    mechanism_rows: List[Dict[str, Any]] = []
    trace_rows: List[Dict[str, Any]] = []
    aggregate_rows: List[Dict[str, Any]] = []

    for row in order_rows:
        trace_label = str(row["trace_label"])
        order = str(row["order"])
        segments = sorted(
            by_trace_order_segments[(trace_label, order)],
            key=lambda r: (int(r["segment_index"]), int(r["segment_end_step"])),
        )
        segment_count = len({int(seg["segment_index"]) for seg in segments})
        max_segment_event_count = max((int(seg["segment_event_count"]) for seg in segments), default=0)
        has_birth_death_segment = any(
            (int(seg["birth_count"]) + int(seg["death_count"])) > 0 for seg in segments
        )
        max_balance_gap = max(
            (abs(int(seg["split_count"]) - int(seg["merge_count"])) for seg in segments),
            default=0,
        )
        mechanism_label = classify_segment_mechanism(
            total_major_events=int(float(row["total_major_events"])),
            segment_count=segment_count,
            birth_count=int(float(row["birth_count"])),
            death_count=int(float(row["death_count"])),
            split_count=int(float(row["split_count"])),
            merge_count=int(float(row["merge_count"])),
            quiet_suffix_steps=int(float(row["quiet_suffix_steps"])),
            topology_change_count=int(float(row["topology_change_count"])),
        )
        mechanism_rows.append(
            {
                "trace_label": trace_label,
                "pair_label": str(row["pair_label"]),
                "order": order,
                "expected_prefix_chain": str(row["expected_prefix_chain"]),
                "prefix_chain_label": str(row["prefix_chain_label"]),
                "full_chain_label": str(row["full_chain_label"]),
                "tail_transition_label": str(row["tail_transition_label"]),
                "segment_count": int(segment_count),
                "max_segment_event_count": int(max_segment_event_count),
                "has_birth_death_segment": 1 if has_birth_death_segment else 0,
                "max_balance_gap": int(max_balance_gap),
                "total_major_events": int(float(row["total_major_events"])),
                "topology_change_count": int(float(row["topology_change_count"])),
                "quiet_suffix_steps": int(float(row["quiet_suffix_steps"])),
                "tail_mechanism_label": mechanism_label,
            }
        )

    by_trace: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in mechanism_rows:
        by_trace[str(row["trace_label"])].append(row)
    summary_lookup = {str(row["trace_label"]): row for row in summary_rows}

    for trace_label, rows in sorted(by_trace.items()):
        labels = sorted({str(row["tail_mechanism_label"]) for row in rows})
        common_label = labels[0] if len(labels) == 1 else "order_ambiguous_mechanism"
        base = summary_lookup[trace_label]
        trace_rows.append(
            {
                "trace_label": trace_label,
                "pair_label": str(base["pair_label"]),
                "prefix_chain_label": str(base["prefix_chain_label"]),
                "v15i_tail_transition_label": str(base["tail_transition_label"]),
                "tail_mechanism_label": common_label,
                "mechanism_labels_by_order": ",".join(str(row["tail_mechanism_label"]) for row in rows),
                "order_ambiguous_mechanism": 0 if common_label != "order_ambiguous_mechanism" else 1,
                "mean_segment_count": mean_defined(float(row["segment_count"]) for row in rows),
                "mean_total_major_events": mean_defined(float(row["total_major_events"]) for row in rows),
                "mean_topology_change_count": mean_defined(float(row["topology_change_count"]) for row in rows),
                "mean_quiet_suffix_steps": mean_defined(float(row["quiet_suffix_steps"]) for row in rows),
                "mean_max_segment_event_count": mean_defined(float(row["max_segment_event_count"]) for row in rows),
                "birth_death_segment_rate": mean_defined(float(row["has_birth_death_segment"]) for row in rows),
            }
        )

    by_label: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in trace_rows:
        by_label[str(row["tail_mechanism_label"])].append(row)
    total = max(1, len(trace_rows))
    for label, rows in sorted(by_label.items()):
        aggregate_rows.append(
            {
                "tail_mechanism_label": label,
                "n_traces": len(rows),
                "rate": len(rows) / total,
                "mean_segment_count": mean_defined(safe_float(row["mean_segment_count"]) for row in rows),
                "mean_total_major_events": mean_defined(safe_float(row["mean_total_major_events"]) for row in rows),
                "mean_topology_change_count": mean_defined(safe_float(row["mean_topology_change_count"]) for row in rows),
                "mean_quiet_suffix_steps": mean_defined(safe_float(row["mean_quiet_suffix_steps"]) for row in rows),
            }
        )

    return mechanism_rows, trace_rows, aggregate_rows


def recommendation_rows(trace_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    order_clean = all(int(row["order_ambiguous_mechanism"]) == 0 for row in trace_rows)
    labels = sorted({str(row["tail_mechanism_label"]) for row in trace_rows})
    out = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if order_clean else "unclear",
            "note": (
                "Mekanismelabelene er order-stabile i denne runden."
                if order_clean
                else "Minst ett trace fikk ulike mekanismelabels mellom AB og BA."
            ),
        }
    ]
    if order_clean and len(labels) >= 3:
        signal_status = "tail_mechanisms_explained"
        signal_note = (
            f"De tre v15i-tail-overgangene kan na forklares av tre enkle segmentmekanismer ({', '.join(labels)})."
        )
        next_status = "test_mechanism_thresholds"
        next_note = "Neste steg bør teste hvilke terskler som utløser disse mekanismene, ikke nye pair-offset-sok."
    elif order_clean and len(labels) == 2:
        signal_status = "partially_explained"
        signal_note = (
            f"Tail-overgangene er mer forklarte enn før, men samler seg fortsatt bare i to mekanismelabels ({', '.join(labels)})."
        )
        next_status = "test_mechanism_thresholds"
        next_note = "Neste steg bør prøve å forklare terskelovergangen mellom de to mekanismene."
    else:
        signal_status = "still_mixed"
        signal_note = "Mekanismelesningen gjør ikke tail-signalene klart enklere enn v15i alene."
        next_status = "pause_new_scans"
        next_note = "Neste steg bør være en annen defect-vinkel, ikke mer tail-labeling."
    out.append({"diagnostic_family": "mechanism_signal", "status": signal_status, "note": signal_note})
    out.append({"diagnostic_family": "next_step", "status": next_status, "note": next_note})
    return out


def build_report(
    *,
    target_rows: Sequence[Mapping[str, str]],
    trace_rows: Sequence[Mapping[str, Any]],
    aggregate_rows: Sequence[Mapping[str, Any]],
    recommendation: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15j: tail mechanism lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden forklarer v15i sine tail-overganger med eksplisitte segmentmekanismer i stedet for bare overgangsnavn."
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
    lines.append("## Trace mechanisms")
    lines.append("")
    lines.append("| trace | v15i tail | mechanism | segments | events | quiet suffix |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in trace_rows:
        lines.append(
            f"| {row['trace_label']} | {row['v15i_tail_transition_label']} | {row['tail_mechanism_label']} | {fmt(row['mean_segment_count'])} | {fmt(row['mean_total_major_events'])} | {fmt(row['mean_quiet_suffix_steps'])} |"
        )
    lines.append("")
    lines.append("## Aggregate mechanisms")
    lines.append("")
    lines.append("| mechanism | n traces | rate | mean segments | mean events |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in aggregate_rows:
        lines.append(
            f"| {row['tail_mechanism_label']} | {int(row['n_traces'])} | {fmt(row['rate'])} | {fmt(row['mean_segment_count'])} | {fmt(row['mean_total_major_events'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt forklarende arbeidskategorier, ikke partikkelbevis.")
    lines.append("- Poenget er at senfasen na beskrives med enklere mekanismer enn i v15i alene.")
    lines.append("- Hvis disse mekanismene holder, er neste riktige steg terskeltesting, ikke ny bred collision-scan.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15j tail mechanism lab.")
    p.add_argument("--target-in", type=str, default=V15H_TARGET)
    p.add_argument("--order-in", type=str, default=V15I_ORDER)
    p.add_argument("--segments-in", type=str, default=V15I_SEGMENTS)
    p.add_argument("--summary-in", type=str, default=V15I_SUMMARY)
    p.add_argument("--out-order-csv", type=str, default="Documentation/v15j_tail_mechanism_order_rows.csv")
    p.add_argument("--out-summary-csv", type=str, default="Documentation/v15j_tail_mechanism_summary.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15j_tail_mechanism_aggregate.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15j_tail_mechanism_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15j_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15j.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    target_rows = read_csv(args.target_in)
    order_rows = read_csv(args.order_in)
    segment_rows = read_csv(args.segments_in)
    summary_rows = read_csv(args.summary_in)

    mechanism_rows, trace_rows, aggregate_rows = derive_rows(
        order_rows=order_rows,
        segment_rows=segment_rows,
        summary_rows=summary_rows,
    )
    recommendation = recommendation_rows(trace_rows)
    report_md = build_report(
        target_rows=target_rows,
        trace_rows=trace_rows,
        aggregate_rows=aggregate_rows,
        recommendation=recommendation,
    )
    op_md = "\n".join(
        [
            "# v0.15j operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Les denne runden som mekanisk forklaring av v15i, ikke som ny fysikk.",
            "- Ikke les mekanismelabels som defect-arter; les dem som enklere beskrivelser av senfase-forlop.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15j",
            "",
            "Denne runden prøver å forklare hvordan de lange kollisjonsforløpene ender.",
            "",
            "I stedet for bare å si at et forløp har én eller annen tail-type, spør vi om sluttfasen kan beskrives med en enklere mekanisme: stille låsing, rebound mellom split og merge, eller mer fragmenterende reparasjon.",
            "",
            "Det gjør ikke funnene mer spektakulære. Det gjør dem mer forståelige. Og det er akkurat det vi trenger nå.",
        ]
    ) + "\n"

    write_csv(args.out_order_csv, mechanism_rows)
    write_csv(args.out_summary_csv, trace_rows)
    write_csv(args.out_aggregate_csv, aggregate_rows)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
