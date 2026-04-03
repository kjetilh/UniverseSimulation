#!/usr/bin/env python3
"""v0.15l holdout failure explainer.

This is a narrow analysis-only follow-up to v15k. It does not run new
simulations. It compares v15j anchor mechanisms against the v15k holdout traces
to explain why the local mechanism story failed to generalize.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


ANCHOR_SUMMARY = "Documentation/v15j_tail_mechanism_summary.csv"
HOLDOUT_SUMMARY = "Documentation/v15k_mechanism_holdout_v15j_summary.csv"


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


def classify_break(
    *,
    anchor_birth_death_rate: float,
    holdout_birth_death_rate: float,
    anchor_quiet: float,
    holdout_quiet: float,
    anchor_events: float,
    holdout_events: float,
    anchor_segments: float,
    holdout_segments: float,
    anchor_changes: float,
    holdout_changes: float,
) -> Tuple[str, str]:
    reasons: List[str] = []
    if anchor_birth_death_rate < 0.5 and holdout_birth_death_rate >= 0.5:
        reasons.append("birth_death_intrusion")
    if anchor_quiet >= 40 and holdout_quiet <= 0.5 * anchor_quiet:
        reasons.append("quiet_suffix_collapse")
    if holdout_segments >= anchor_segments + 1.0:
        reasons.append("segment_complexity_growth")
    if holdout_events >= anchor_events + 8.0:
        reasons.append("event_overload")
    if holdout_changes >= anchor_changes + 4.0:
        reasons.append("topology_churn_growth")

    if not reasons and holdout_events < anchor_events and holdout_quiet < anchor_quiet:
        reasons.append("weaker_locking_without_clean_alternative")
    if not reasons:
        reasons.append("mixed_break_without_single_driver")

    if "birth_death_intrusion" in reasons and "quiet_suffix_collapse" in reasons:
        primary = "birth_death_plus_quiet_collapse"
    elif "birth_death_intrusion" in reasons:
        primary = "birth_death_intrusion"
    elif "quiet_suffix_collapse" in reasons:
        primary = "quiet_suffix_collapse"
    elif "event_overload" in reasons or "topology_churn_growth" in reasons:
        primary = "tail_overactivity"
    elif "segment_complexity_growth" in reasons:
        primary = "segment_complexity_growth"
    else:
        primary = reasons[0]
    return primary, ",".join(reasons)


def derive_rows(
    anchor_rows: Sequence[Mapping[str, str]],
    holdout_rows: Sequence[Mapping[str, str]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    anchor_lookup = {
        (str(row["pair_label"]), str(row["prefix_chain_label"])): row
        for row in anchor_rows
    }

    comparison_rows: List[Dict[str, Any]] = []
    for row in holdout_rows:
        key = (str(row["pair_label"]), str(row["prefix_chain_label"]))
        anchor = anchor_lookup[key]
        anchor_birth = safe_float(anchor["birth_death_segment_rate"])
        hold_birth = safe_float(row["birth_death_segment_rate"])
        anchor_quiet = safe_float(anchor["mean_quiet_suffix_steps"])
        hold_quiet = safe_float(row["mean_quiet_suffix_steps"])
        anchor_events = safe_float(anchor["mean_total_major_events"])
        hold_events = safe_float(row["mean_total_major_events"])
        anchor_segments = safe_float(anchor["mean_segment_count"])
        hold_segments = safe_float(row["mean_segment_count"])
        anchor_changes = safe_float(anchor["mean_topology_change_count"])
        hold_changes = safe_float(row["mean_topology_change_count"])
        primary, reasons = classify_break(
            anchor_birth_death_rate=anchor_birth,
            holdout_birth_death_rate=hold_birth,
            anchor_quiet=anchor_quiet,
            holdout_quiet=hold_quiet,
            anchor_events=anchor_events,
            holdout_events=hold_events,
            anchor_segments=anchor_segments,
            holdout_segments=hold_segments,
            anchor_changes=anchor_changes,
            holdout_changes=hold_changes,
        )
        comparison_rows.append(
            {
                "trace_label": str(row["trace_label"]),
                "pair_label": str(row["pair_label"]),
                "prefix_chain_label": str(row["prefix_chain_label"]),
                "anchor_mechanism_label": str(anchor["tail_mechanism_label"]),
                "holdout_mechanism_label": str(row["observed_mechanism_label"]),
                "primary_break_driver": primary,
                "break_driver_tokens": reasons,
                "delta_segment_count": hold_segments - anchor_segments,
                "delta_total_major_events": hold_events - anchor_events,
                "delta_topology_change_count": hold_changes - anchor_changes,
                "delta_quiet_suffix_steps": hold_quiet - anchor_quiet,
                "delta_birth_death_segment_rate": hold_birth - anchor_birth,
            }
        )

    aggregate: Dict[str, Dict[str, Any]] = {}
    total = max(1, len(comparison_rows))
    for row in comparison_rows:
        key = str(row["primary_break_driver"])
        bucket = aggregate.setdefault(
            key,
            {
                "primary_break_driver": key,
                "n_traces": 0,
                "mean_delta_segment_count": 0.0,
                "mean_delta_total_major_events": 0.0,
                "mean_delta_topology_change_count": 0.0,
                "mean_delta_quiet_suffix_steps": 0.0,
                "mean_delta_birth_death_segment_rate": 0.0,
            },
        )
        bucket["n_traces"] += 1
        for field in (
            "delta_segment_count",
            "delta_total_major_events",
            "delta_topology_change_count",
            "delta_quiet_suffix_steps",
            "delta_birth_death_segment_rate",
        ):
            bucket[f"mean_{field}"] += safe_float(row[field])

    aggregate_rows: List[Dict[str, Any]] = []
    for key, bucket in sorted(aggregate.items()):
        n = max(1, int(bucket["n_traces"]))
        aggregate_rows.append(
            {
                "primary_break_driver": key,
                "n_traces": int(bucket["n_traces"]),
                "rate": int(bucket["n_traces"]) / total,
                "mean_delta_segment_count": bucket["mean_delta_segment_count"] / n,
                "mean_delta_total_major_events": bucket["mean_delta_total_major_events"] / n,
                "mean_delta_topology_change_count": bucket["mean_delta_topology_change_count"] / n,
                "mean_delta_quiet_suffix_steps": bucket["mean_delta_quiet_suffix_steps"] / n,
                "mean_delta_birth_death_segment_rate": bucket["mean_delta_birth_death_segment_rate"] / n,
            }
        )
    return comparison_rows, aggregate_rows


def recommendation_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    drivers = sorted({str(row["primary_break_driver"]) for row in rows})
    if drivers:
        status = "holdout_failure_explained_locally"
        note = (
            f"Holdout-bruddet kan leses som noen fa lokale bruddmodi ({', '.join(drivers)}), ikke bare ren uforklarlig stoy."
        )
        next_status = "pivot_question"
        next_note = "Neste steg bør være et nytt defect-spørsmål, ikke mer av samme collision-generalisering."
    else:
        status = "holdout_failure_still_opaque"
        note = "Selv forklaringsrunden klarer ikke å si mye om hvorfor holdoutene falt tilbake til mixed."
        next_status = "pivot_question"
        next_note = "Neste steg bør likevel være et nytt defect-spørsmål, siden collision-sporet nå har lav marginalverdi."
    return [
        {"diagnostic_family": "failure_explanation", "status": status, "note": note},
        {"diagnostic_family": "next_step", "status": next_status, "note": next_note},
    ]


def build_report(
    rows: Sequence[Mapping[str, Any]],
    aggregate_rows: Sequence[Mapping[str, Any]],
    recommendation: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15l: holdout failure explainer")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden forklarer hvorfor v15j sine lokale tail-mekanismer ikke generaliserte på v15k-holdoutene."
    )
    lines.append("")
    lines.append("## Per-trace sammenlikning")
    lines.append("")
    lines.append("| trace | anchor mech | holdout mech | primary driver | d events | d quiet | d birth/death |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {row['trace_label']} | {row['anchor_mechanism_label']} | {row['holdout_mechanism_label']} | {row['primary_break_driver']} | {fmt(row['delta_total_major_events'])} | {fmt(row['delta_quiet_suffix_steps'])} | {fmt(row['delta_birth_death_segment_rate'])} |"
        )
    lines.append("")
    lines.append("## Aggregate bruddmodi")
    lines.append("")
    lines.append("| break driver | n | rate | mean d events | mean d quiet |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in aggregate_rows:
        lines.append(
            f"| {row['primary_break_driver']} | {int(row['n_traces'])} | {fmt(row['rate'])} | {fmt(row['mean_delta_total_major_events'])} | {fmt(row['mean_delta_quiet_suffix_steps'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en lokal forklaringsanalyse, ikke en ny mekanismelov.")
    lines.append("- Verdien her er å vise at holdout-bruddet ikke var helt vilkårlig, men heller ikke sterkt nok til å redde collision-generaliseringen.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15l holdout failure explainer.")
    p.add_argument("--anchor-summary", type=str, default=ANCHOR_SUMMARY)
    p.add_argument("--holdout-summary", type=str, default=HOLDOUT_SUMMARY)
    p.add_argument("--out-comparison-csv", type=str, default="Documentation/v15l_holdout_failure_comparison.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15l_holdout_failure_aggregate.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15l_holdout_failure_explainer.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15l_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15l.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    anchor_rows = read_csv(args.anchor_summary)
    holdout_rows = read_csv(args.holdout_summary)
    rows, aggregate_rows = derive_rows(anchor_rows, holdout_rows)
    recommendation = recommendation_rows(rows)
    report_md = build_report(rows, aggregate_rows, recommendation)
    op_md = "\n".join(
        [
            "# v0.15l operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Les denne runden som forklaring av v15k-bruddet, ikke som en ny positiv mekanismepåstand.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15l",
            "",
            "Denne runden spør ikke om vi fant nye mekanismer. Den spør hvorfor de mekanismene vi trodde vi så, ikke holdt på nye eksempler.",
            "",
            "Det er nyttig fordi det sier om vi bare hadde støy, eller om vi traff noen lokale mønstre som senere ble forstyrret av andre hendelser.",
        ]
    ) + "\n"

    write_csv(args.out_comparison_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate_rows)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
