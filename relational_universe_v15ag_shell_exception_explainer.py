#!/usr/bin/env python3
"""v0.15ag shell exception explainer for add_chord recurrence band.

This round follows v15af. Most shell fragmentation now looks like an early
tail lock, but a few minority traces remain:

- delayed fragment lock
- connected resistance churn
- intermittent / mixed churn cases

The goal here is not to reopen scanning, but to explain whether these
exceptions themselves collapse into a small set of local mechanisms.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v15_defect_lifetime_lab as v15


DOC = Path("Documentation")
IN_AE = DOC / "v15ae_add_chord_shell_topology_runs.csv"
IN_AF_RUNS = DOC / "v15af_add_chord_shell_fragment_runs.csv"
IN_AF_SEGMENTS = DOC / "v15af_add_chord_shell_fragment_segments.csv"
IN_TARGET = DOC / "v15af_add_chord_shell_fragment_target_summary.csv"
TARGET = 48


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def classify_exception_mechanism(
    *,
    timing_label: str,
    connected_prefix_steps: float,
    longest_connected_steps: float,
    final_fragment_steps: float,
    fragmented_suffix_rate: float,
    state_switch_count: float,
    mean_shell_component_count: float,
) -> str:
    if (
        timing_label == "delayed_fragment_lock"
        and connected_prefix_steps >= 24.0
        and final_fragment_steps >= 400.0
        and fragmented_suffix_rate >= 0.90
    ):
        return "two_stage_fragment_lock"
    if (
        timing_label == "connected_resistance_churn"
        and longest_connected_steps >= 160.0
        and fragmented_suffix_rate <= 0.35
        and mean_shell_component_count <= 1.5
    ):
        return "singleton_resistance_case"
    if (
        timing_label == "intermittent_fragment_churn"
        and longest_connected_steps >= 96.0
        and final_fragment_steps >= 112.0
        and state_switch_count >= 6.0
    ):
        return "alternating_to_late_lock"
    if (
        timing_label == "mixed_fragment_timing"
        and longest_connected_steps >= 128.0
        and final_fragment_steps >= 560.0
        and fragmented_suffix_rate >= 0.80
    ):
        return "near_lock_boundary_case"
    return "residual_exception"


def mechanism_note(label: str) -> str:
    if label == "two_stage_fragment_lock":
        return "Runet holder shellen samlet litt lenger, men går deretter inn i en sterk og varig fragment-lock i to store faser."
    if label == "singleton_resistance_case":
        return "Runet motstår fragmentering lenge gjennom lange singleton-platåer og mange små bytter før shellen til slutt gir etter."
    if label == "alternating_to_late_lock":
        return "Runet veksler mellom samlet og fragmentert shell en stund, men ender likevel i en tydelig sen fragment-lock."
    if label == "near_lock_boundary_case":
        return "Runet ligger nær early-lock-familien, men beholder akkurat nok connected motstand til å bli en grensetilstand."
    return "Runet forklares ikke rent av de små lokale unntaksmekanismene ennå."


def build_rows(
    *,
    ae_rows_in: Sequence[Mapping[str, str]],
    af_rows_in: Sequence[Mapping[str, str]],
    seg_rows_in: Sequence[Mapping[str, str]],
) -> List[Dict[str, Any]]:
    ae_lookup = {
        (int(row["placement"]), int(row["seed_delta"])): dict(row)
        for row in ae_rows_in
    }
    seg_lookup: Dict[Tuple[int, int], List[Dict[str, str]]] = defaultdict(list)
    for row in seg_rows_in:
        key = (int(row["placement"]), int(row["seed_delta"]))
        seg_lookup[key].append(dict(row))

    out: List[Dict[str, Any]] = []
    for row in af_rows_in:
        timing_label = str(row["timing_label"])
        if timing_label == "early_fragment_lock":
            continue
        key = (int(row["placement"]), int(row["seed_delta"]))
        ae = ae_lookup[key]
        segments = sorted(seg_lookup[key], key=lambda r: int(r["segment_index"]))
        connected_segments = [seg for seg in segments if str(seg["segment_state"]) == "connected"]
        fragmented_segments = [seg for seg in segments if str(seg["segment_state"]) == "fragmented"]

        first_connected_steps = (
            safe_float(connected_segments[0]["segment_snapshot_count"]) * 8.0
            if connected_segments and int(connected_segments[0]["segment_index"]) == 0
            else 0.0
        )
        longest_connected_steps = max((safe_float(seg["segment_snapshot_count"]) * 8.0 for seg in connected_segments), default=0.0)
        final_fragment_steps = (
            safe_float(fragmented_segments[-1]["segment_snapshot_count"]) * 8.0
            if fragmented_segments and str(segments[-1]["segment_state"]) == "fragmented"
            else 0.0
        )
        mean_fragment_segment_comp = mean_defined(
            safe_float(seg["mean_shell_component_count"]) for seg in fragmented_segments
        )
        mean_connected_boundary = mean_defined(
            safe_float(seg["mean_shell_boundary_to_volume"]) for seg in connected_segments
        )
        mechanism_label = classify_exception_mechanism(
            timing_label=timing_label,
            connected_prefix_steps=safe_float(row["connected_prefix_steps"]),
            longest_connected_steps=longest_connected_steps,
            final_fragment_steps=final_fragment_steps,
            fragmented_suffix_rate=safe_float(row["fragmented_suffix_rate"]),
            state_switch_count=safe_float(row["state_switch_count"]),
            mean_shell_component_count=safe_float(ae["mean_shell_component_count"]),
        )
        out.append(
            {
                "placement": int(row["placement"]),
                "seed_delta": int(row["seed_delta"]),
                "run_seed": int(row["run_seed"]),
                "support_signature": row["support_signature"],
                "timing_label": timing_label,
                "exception_mechanism_label": mechanism_label,
                "connected_prefix_steps": safe_float(row["connected_prefix_steps"]),
                "fragmented_suffix_rate": safe_float(row["fragmented_suffix_rate"]),
                "state_switch_count": safe_float(row["state_switch_count"]),
                "segment_count": int(row["segment_count"]),
                "longest_connected_steps": longest_connected_steps,
                "final_fragment_steps": final_fragment_steps,
                "mean_shell_component_count": safe_float(ae["mean_shell_component_count"]),
                "mean_shell_connected_rate": safe_float(ae["shell_connected_rate"]),
                "mean_full_exact_return_rate": safe_float(ae["full_exact_return_rate"]),
                "shell_nodes": int(ae["shell_nodes"]),
                "mean_fragment_segment_comp": mean_fragment_segment_comp,
                "mean_connected_boundary_to_volume": mean_connected_boundary,
                "mechanism_note": mechanism_note(mechanism_label),
            }
        )
    return out


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    labels = sorted({str(row["exception_mechanism_label"]) for row in rows})
    out: List[Dict[str, Any]] = []
    total = max(1, len(rows))
    for label in labels:
        grp = [row for row in rows if str(row["exception_mechanism_label"]) == label]
        out.append(
            {
                "exception_mechanism_label": label,
                "n_runs": len(grp),
                "rate": len(grp) / total,
                "mean_connected_prefix_steps": mean_defined(safe_float(row["connected_prefix_steps"]) for row in grp),
                "mean_longest_connected_steps": mean_defined(safe_float(row["longest_connected_steps"]) for row in grp),
                "mean_final_fragment_steps": mean_defined(safe_float(row["final_fragment_steps"]) for row in grp),
                "mean_fragmented_suffix_rate": mean_defined(safe_float(row["fragmented_suffix_rate"]) for row in grp),
                "mean_state_switch_count": mean_defined(safe_float(row["state_switch_count"]) for row in grp),
                "mean_full_exact_return_rate": mean_defined(safe_float(row["mean_full_exact_return_rate"]) for row in grp),
            }
        )
    return out


def diagnosis_rows(
    target_summary: Sequence[Mapping[str, str]],
    rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary if int(row["target_nodes"]) == TARGET)
    labels = {str(row["exception_mechanism_label"]) for row in rows}
    alt_count = sum(1 for row in rows if str(row["exception_mechanism_label"]) == "alternating_to_late_lock")
    if labels >= {"two_stage_fragment_lock", "singleton_resistance_case", "near_lock_boundary_case"} and alt_count >= 2:
        status = "minority_exceptions_are_locally_explainable"
        note = "Minoritetsavvikene kollapser til et lite lokalt sett: totrinns fragment-lock, singleton-resistens, en boundary-case og en liten gruppe alternating-to-late-lock spor."
        next_step = "target_exception_holdout"
        next_note = "Neste steg bor teste om akkurat disse unntaksmekanismene holder pa noen fa nye naerliggende seeds, ikke scanne bredere."
    elif len(labels) <= 3:
        status = "minority_exceptions_partly_explainable"
        note = "Unntakene er mer strukturert enn ren stoy, men kollapser ikke helt til et lite nok mekanismesett ennå."
        next_step = "refine_exception_thresholds"
        next_note = "Neste steg bor skjerpe tersklene rundt de mest informative unntakene."
    else:
        status = "minority_exceptions_still_mixed"
        note = "Selv minoritetsavvikene er fortsatt for heterogene til en liten lokal forklaring."
        next_step = "change_exception_observable"
        next_note = "Neste steg bor bruke en annen observabel inne i unntakene, ikke flere labels."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": (
                "Startstorrelsene er fortsatt rent separert; denne runden forklarer bare de ekte minoritetsavvikene fra v15af."
                if size_clean
                else "Storrelsesseparasjonen er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "exception_mechanism_status",
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
    target_summary: Sequence[Mapping[str, str]],
    rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15ag: shell exception explainer")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden kjorer ingen nye simuleringer. Den forklarer bare minoritetsavvikene fra `v15af` for a se om de kollapser til et lite lokalt mekanismesett.")
    lines.append("")
    lines.append("## Startstorrelser")
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
    lines.append("## Exception runs")
    lines.append("")
    lines.append("| placement | seed | timing | mechanism | prefix steps | longest connected | final fragment | suffix frag | switches | exact return |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {int(row['placement'])} | {int(row['seed_delta'])} | {row['timing_label']} | {row['exception_mechanism_label']} | {fmt(row['connected_prefix_steps'],1)} | {fmt(row['longest_connected_steps'],1)} | {fmt(row['final_fragment_steps'],1)} | {fmt(row['fragmented_suffix_rate'])} | {fmt(row['state_switch_count'])} | {fmt(row['mean_full_exact_return_rate'])} |"
        )
    lines.append("")
    lines.append("## Exception aggregate")
    lines.append("")
    lines.append("| mechanism | n | rate | mean prefix | mean final fragment | mean suffix frag | mean switches |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['exception_mechanism_label']} | {int(row['n_runs'])} | {fmt(row['rate'])} | {fmt(row['mean_connected_prefix_steps'],1)} | {fmt(row['mean_final_fragment_steps'],1)} | {fmt(row['mean_fragmented_suffix_rate'])} | {fmt(row['mean_state_switch_count'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren unntaksforklaring inne i `v15af`, ikke en ny scan.")
    lines.append("- Les mekanismene som lokale forklaringskategorier, ikke som nye defect-arter.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ag shell exception explainer.")
    p.add_argument("--ae-in", type=str, default=str(IN_AE))
    p.add_argument("--af-runs-in", type=str, default=str(IN_AF_RUNS))
    p.add_argument("--af-segments-in", type=str, default=str(IN_AF_SEGMENTS))
    p.add_argument("--target-in", type=str, default=str(IN_TARGET))
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15ag_shell_exception_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ag_shell_exception_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ag_shell_exception_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15ag_shell_exception_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ag_shell_exception_explainer.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ag_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ag.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    ae_rows_in = read_csv(args.ae_in)
    af_rows_in = read_csv(args.af_runs_in)
    seg_rows_in = read_csv(args.af_segments_in)
    target_summary = read_csv(args.target_in)
    rows = build_rows(ae_rows_in=ae_rows_in, af_rows_in=af_rows_in, seg_rows_in=seg_rows_in)
    aggregate = aggregate_rows(rows)
    diagnosis = diagnosis_rows(target_summary, rows, aggregate)
    report_md = build_report(target_summary=target_summary, rows=rows, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15ag operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en forklaring av minoritetsavvikene i v15af, ikke som en ny bred defect-run.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15ag",
            "",
            "Etter at vi sa at shell-fragmentering vanligvis låser tidlig, ser denne runden bare på unntakene: de få løpene som ikke passer helt inn i hovedmønsteret.",
            "",
            "Målet er å finne ut om disse unntakene likevel følger noen få små lokale mønstre, eller om de bare er blandet støy.",
        ]
    ) + "\n"
    write_csv(args.out_rows_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_target_csv, [dict(row) for row in target_summary])
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
