#!/usr/bin/env python3
"""v0.15av post-peak fade holdout around the seed-231 micro-boundary.

This round follows v15au. v15au showed that the remaining small boundary
structure is not just "weaker hold"; it is a real `post_peak_fade` path.

The next narrow question is:

is that path a tiny local transition band around seed 231, or just a singleton
between a hold case and a no-launch case?
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15au_post_peak_fade_explainer as v15au


TARGET = 48
GROWTH_SEED = 202
PLACEMENT = 2

CASE_SPECS = (
    {"case_role": "lower_holdout", "case_label": "lower_215", "seed_delta": 215, "expected_burst_label": "unknown_near_fade"},
    {"case_role": "lower_holdout", "case_label": "lower_223", "seed_delta": 223, "expected_burst_label": "unknown_near_fade"},
    {"case_role": "anchor_fade", "case_label": "anchor_231", "seed_delta": 231, "expected_burst_label": "fading_late_burst"},
    {"case_role": "upper_context", "case_label": "upper_239", "seed_delta": 239, "expected_burst_label": "sustained_hold_burst"},
    {"case_role": "upper_context", "case_label": "upper_247", "seed_delta": 247, "expected_burst_label": "no_high_burst"},
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if y != y:
        return "nan"
    return f"{y:.{digits}f}"


def run_rows(*, base_state: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for spec in CASE_SPECS:
        row = v15au.analyze_case(
            base_state=base_state,
            case_label=str(spec["case_label"]),
            placement=PLACEMENT,
            seed_delta=int(spec["seed_delta"]),
            expected_burst_label=str(spec["expected_burst_label"]),
        )
        row["case_role"] = str(spec["case_role"])
        rows.append(row)
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    lower = [row for row in rows if str(row["case_role"]) == "lower_holdout"]
    fade_count = sum(1 for row in lower if str(row["post_peak_label"]) == "post_peak_fade")
    no_launch_count = sum(1 for row in lower if str(row["post_peak_label"]) == "no_launch_tail")
    hold_count = sum(1 for row in lower if str(row["post_peak_label"]) == "post_peak_hold")
    return [
        {
            "group_type": "lower_holdout_summary",
            "group_value": "seed_231_neighborhood",
            "n_runs": len(lower),
            "post_peak_fade_rate": fade_count / max(1, len(lower)),
            "no_launch_tail_rate": no_launch_count / max(1, len(lower)),
            "post_peak_hold_rate": hold_count / max(1, len(lower)),
            "mean_post_peak_high_rate": mean_defined(safe_float(row["post_peak_high_rate"]) for row in lower),
            "mean_post_peak_mid_rate": mean_defined(safe_float(row["post_peak_mid_rate"]) for row in lower),
            "mean_last12_high_rate": mean_defined(safe_float(row["last12_high_rate"]) for row in lower),
        }
    ]


def diagnosis_rows(*, target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary if int(row["target_nodes"]) == TARGET)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    ag = aggregate[0]
    fade_rate = safe_float(ag["post_peak_fade_rate"])
    no_launch_rate = safe_float(ag["no_launch_tail_rate"])
    hold_rate = safe_float(ag["post_peak_hold_rate"])
    if fade_rate >= 0.50:
        status = "small_fade_band_supported"
        note = "Minst ett av de nye nedre nabopunktene holder som `post_peak_fade`, sa fading-sporet ser ut til a vaere et lite lokalt band og ikke bare ett singleton-case."
        next_step = "tighten_fade_band_edges"
        next_note = "Neste steg bor kartlegge den nederste fade-kanten enda smalere."
    elif no_launch_rate >= 1.0:
        status = "fade_singleton_not_supported"
        note = "Begge nye nedre nabopunktene faller til `no_launch_tail`, sa fading-sporet ser best ut som et singleton-aktig overgangspunkt mellom hold og no-launch."
        next_step = "stop_fade_expansion"
        next_note = "Neste steg bor ikke vaere bredere fade-scan; dette er bedre lest som et lokalt overgangspunkt."
    elif no_launch_rate > 0.0 and fade_rate > 0.0:
        status = "fade_transition_supported"
        note = "De nye nedre nabopunktene splitter mellom `post_peak_fade` og `no_launch_tail`, sa seed 231 sitter pa en liten lokal overgangssone."
        next_step = "probe_transition_edge"
        next_note = "Neste steg bor vaere en enda smalere test av overgangen mellom fade og no-launch."
    elif hold_rate > 0.0:
        status = "fade_zone_tilts_upward"
        note = "Et nedre nabopunkt holder fortsatt som post-peak hold, sa fade-sonen er ikke monotont avgrenset nedover."
        next_step = "probe_nonmonotone_fade_edge"
        next_note = "Neste steg bor forklare den ikke-monotone kanten i stedet for a scanne bredere."
    else:
        status = "fade_holdout_mixed"
        note = "De nye nedre nabopunktene gir fortsatt ikke et rent nok svar pa om fading-sporet er singleton eller lite band."
        next_step = "change_fade_holdout_observable"
        next_note = "Neste steg bor bytte observabel rundt fade-holdout-sporet."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsene er rent separert og alle run i denne runden matcher onsket add_chord-perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "fade_holdout_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15av: post-peak fade holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester bare den nederste lokale nabosonen rundt fading-caset ved seed `231` i placement `2`.")
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
    lines.append("## Cases")
    lines.append("")
    lines.append("| role | case | seed delta | post high | post mid | last12 high | post-peak label |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            f"| {row['case_role']} | {row['case_label']} | {int(row['seed_delta'])} | {fmt(row['post_peak_high_rate'])} | {fmt(row['post_peak_mid_rate'])} | {fmt(row['last12_high_rate'])} | {row['post_peak_label']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en minimal holdout rundt fading-caset, ikke en ny bred scan.")
    lines.append("- Les dette som lokal overgangsstruktur, ikke som nye defect-arter.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15av post-peak fade holdout.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15av_post_peak_fade_holdout_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15av_post_peak_fade_holdout_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15av_post_peak_fade_holdout_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15av_post_peak_fade_holdout_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15av_post_peak_fade_holdout.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15av_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15av.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    rows = run_rows(base_state=base_state)
    aggregate = aggregate_rows(rows)
    diagnosis = diagnosis_rows(target_summary=target_summary, rows=rows, aggregate=aggregate)
    report_md = build_report(target_summary=target_summary, rows=rows, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15av operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en minimal fade-holdout, ikke som en ny bred defect-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15av",
            "",
            "Etter at vi fant et lite fading-spor, tester denne runden om det sporet finnes igjen i de aller naermeste nedre nabotilfellene.",
            "",
            "Maalet er a avgjore om fading er et lite lokalt band eller bare ett smalt overgangspunkt.",
        ]
    ) + "\n"
    write_csv(args.out_runs_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
