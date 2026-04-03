#!/usr/bin/env python3
"""v0.15k mechanism holdout validation.

This follows v15j. We do not open a new broad collision search. Instead we run
long-horizon holdout traces on new offsets from the already identified v15g
prefix families and ask:

Do the v15j tail mechanisms recur on nearby holdout traces from the same
pair/prefix family?
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15b_add_chord_collision_lab as v15b
import relational_universe_v15h_representative_collision_traces as v15h
import relational_universe_v15i_tail_transition_lab as v15i
import relational_universe_v15j_tail_mechanism_lab as v15j


TARGET = 48
PRIMARY_GROWTH_SEED = 101
ANCHOR_MECHANISM_SUMMARY = "Documentation/v15j_tail_mechanism_summary.csv"

HOLDOUT_TRACE_SPECS = (
    {
        "trace_label": "pair23_merge_hold_split_holdout",
        "pair": (2, 3),
        "run_offset": 17,
        "expected_prefix_chain": "merge_hold_split",
    },
    {
        "trace_label": "pair23_compress_split_rebind_holdout",
        "pair": (2, 3),
        "run_offset": 23,
        "expected_prefix_chain": "compress_split_rebind",
    },
    {
        "trace_label": "pair23_split_persistent_dual_holdout",
        "pair": (2, 3),
        "run_offset": 29,
        "expected_prefix_chain": "split_persistent_dual",
    },
    {
        "trace_label": "pair34_split_persistent_dual_holdout",
        "pair": (3, 4),
        "run_offset": 11,
        "expected_prefix_chain": "split_persistent_dual",
    },
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15b.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15b.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15b.write_csv(path, rows)


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def load_expected_mechanisms(path: str | Path) -> Dict[Tuple[str, str], str]:
    rows = read_csv(path)
    mapping: Dict[Tuple[str, str], str] = {}
    for row in rows:
        mapping[(str(row["pair_label"]), str(row["prefix_chain_label"]))] = str(row["tail_mechanism_label"])
    return mapping


def recommendation_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    prefix_clean = all(int(row["prefix_matches_expected"]) == 1 for row in rows)
    order_clean = all(int(row["order_ambiguous_tail"]) == 0 and int(row["order_ambiguous_mechanism"]) == 0 for row in rows)
    match_rate = mean_defined(float(row["matches_expected_mechanism"]) for row in rows)
    out = [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (prefix_clean and order_clean) else "unclear",
            "note": (
                "Holdout-tracene reproduserer forventet prefix-chain og holder seg order-stabile i tail og mekanikk."
                if (prefix_clean and order_clean)
                else "Minst ett holdout-trace spriker enten i prefix-chain eller mellom AB og BA."
            ),
        }
    ]
    if match_rate >= 0.999:
        status = "mechanism_generalization_supported"
        note = "Alle holdout-tracene lander i samme tail-mekanisme som ankertracene fra v15j."
        next_status = "test_mechanism_thresholds"
        next_note = "Neste steg bør teste hvilke terskler som utløser mekanismeskift, ikke lete etter nye familier."
    elif match_rate >= 0.5:
        status = "mechanism_generalization_partial"
        note = f"Holdout-tracene holder mekanismelesningen delvis, men ikke helt rent (match-rate {match_rate:.3f})."
        next_status = "locate_threshold_break"
        next_note = "Neste steg bør lokalisere hvor generaliseringen bryter, ikke åpne bred scanning."
    else:
        status = "mechanism_generalization_weak"
        note = f"Holdout-tracene bekrefter ikke mekanismelesningen godt nok (match-rate {match_rate:.3f})."
        next_status = "pause_threshold_claims"
        next_note = "Neste steg bør være en mindre påstand: forklarende spor, men ikke stabil generalisering."
    out.append({"diagnostic_family": "generalization_signal", "status": status, "note": note})
    out.append({"diagnostic_family": "next_step", "status": next_status, "note": next_note})
    return out


def build_report(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    summary_rows: Sequence[Mapping[str, Any]],
    recommendation: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15k: mechanism holdout validation")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden tester om mekanismelesningen fra v15j holder på nye, nærliggende holdout-traces fra de samme v15g-familiene."
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
    lines.append("## Holdout mechanism check")
    lines.append("")
    lines.append("| trace | pair | offset | prefix | expected mechanism | observed mechanism | match |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in summary_rows:
        lines.append(
            f"| {row['trace_label']} | {row['pair_label']} | {int(row['run_offset'])} | {row['prefix_chain_label']} | {row['expected_mechanism_label']} | {row['observed_mechanism_label']} | {int(row['matches_expected_mechanism'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt en smal generaliseringstest, ikke ny fysikk.")
    lines.append("- Et positivt utfall betyr bare at de samme mekanismene ser ut til å komme igjen på nærliggende holdout-traces.")
    lines.append("- Et negativt utfall ville ha betydd at v15j var for lokalt overfit. Det er derfor nyttig uansett vei.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15k mechanism holdout validation.")
    p.add_argument("--anchor-mechanisms", type=str, default=ANCHOR_MECHANISM_SUMMARY)
    p.add_argument("--out-component-csv", type=str, default="Documentation/v15k_mechanism_holdout_component_trajectories.csv")
    p.add_argument("--out-event-log-csv", type=str, default="Documentation/v15k_mechanism_holdout_event_log.csv")
    p.add_argument("--out-v15h-summary-csv", type=str, default="Documentation/v15k_mechanism_holdout_v15h_summary.csv")
    p.add_argument("--out-v15i-summary-csv", type=str, default="Documentation/v15k_mechanism_holdout_v15i_summary.csv")
    p.add_argument("--out-v15j-summary-csv", type=str, default="Documentation/v15k_mechanism_holdout_v15j_summary.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15k_mechanism_holdout_aggregate.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15k_mechanism_holdout_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15k_mechanism_holdout_validation.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15k_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15k.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    expected_mechanisms = load_expected_mechanisms(args.anchor_mechanisms)

    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15b.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [PRIMARY_GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base = base_states[(ensembles[0].name, PRIMARY_GROWTH_SEED)]

    component_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []
    v15h_summary_rows: List[Dict[str, Any]] = []

    for spec in HOLDOUT_TRACE_SPECS:
        comp_rows, ev_rows, summary_row = v15h.run_long_trace(
            base=base,
            pair=tuple(spec["pair"]),
            trace_label=str(spec["trace_label"]),
            run_offset=int(spec["run_offset"]),
            expected_prefix_chain=str(spec["expected_prefix_chain"]),
        )
        component_rows.extend(comp_rows)
        event_rows.extend(ev_rows)
        v15h_summary_rows.append(summary_row)

    _order_rows, segment_rows, v15i_summary_rows, _v15i_aggregate = v15i.derive_trace_rows(
        summary_rows=v15h_summary_rows,
        component_rows=component_rows,
        event_rows=event_rows,
    )
    mechanism_order_rows, v15j_summary_rows, v15j_aggregate = v15j.derive_rows(
        order_rows=_order_rows,
        segment_rows=segment_rows,
        summary_rows=v15i_summary_rows,
    )

    summary_out: List[Dict[str, Any]] = []
    for row in v15j_summary_rows:
        pair_label = str(row["pair_label"])
        prefix_chain = str(row["prefix_chain_label"])
        expected_mech = expected_mechanisms.get((pair_label, prefix_chain), "unknown_anchor")
        observed_mech = str(row["tail_mechanism_label"])
        summary_out.append(
            {
                "trace_label": str(row["trace_label"]),
                "pair_label": pair_label,
                "run_offset": next(
                    int(r["run_offset"]) for r in v15h_summary_rows if str(r["trace_label"]) == str(row["trace_label"])
                ),
                "prefix_chain_label": prefix_chain,
                "prefix_matches_expected": next(
                    int(r["prefix_matches_expected"])
                    for r in v15h_summary_rows
                    if str(r["trace_label"]) == str(row["trace_label"])
                ),
                "v15i_tail_transition_label": str(row["v15i_tail_transition_label"]),
                "order_ambiguous_tail": next(
                    int(r["order_ambiguous_tail"])
                    for r in v15i_summary_rows
                    if str(r["trace_label"]) == str(row["trace_label"])
                ),
                "expected_mechanism_label": expected_mech,
                "observed_mechanism_label": observed_mech,
                "matches_expected_mechanism": 1 if observed_mech == expected_mech else 0,
                "order_ambiguous_mechanism": int(row["order_ambiguous_mechanism"]),
                "mean_segment_count": safe_float(row["mean_segment_count"]),
                "mean_total_major_events": safe_float(row["mean_total_major_events"]),
                "mean_topology_change_count": safe_float(row["mean_topology_change_count"]),
                "mean_quiet_suffix_steps": safe_float(row["mean_quiet_suffix_steps"]),
                "birth_death_segment_rate": safe_float(row["birth_death_segment_rate"]),
            }
        )

    aggregate_rows: List[Dict[str, Any]] = []
    total = max(1, len(summary_out))
    matched = sum(int(row["matches_expected_mechanism"]) for row in summary_out)
    aggregate_rows.append(
        {
            "diagnostic": "holdout_mechanism_match_rate",
            "n_traces": len(summary_out),
            "n_matches": matched,
            "rate": matched / total,
        }
    )
    for row in v15j_aggregate:
        aggregate_rows.append(
            {
                "diagnostic": f"mechanism::{row['tail_mechanism_label']}",
                "n_traces": int(row["n_traces"]),
                "n_matches": "",
                "rate": safe_float(row["rate"]),
                "mean_segment_count": safe_float(row["mean_segment_count"]),
                "mean_total_major_events": safe_float(row["mean_total_major_events"]),
                "mean_topology_change_count": safe_float(row["mean_topology_change_count"]),
                "mean_quiet_suffix_steps": safe_float(row["mean_quiet_suffix_steps"]),
            }
        )

    recommendation = recommendation_rows(summary_out)
    report_md = build_report(
        target_summary=target_summary,
        summary_rows=summary_out,
        recommendation=recommendation,
    )
    op_md = "\n".join(
        [
            "# v0.15k operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Les denne runden som holdout-validering av v15j, ikke som ny familiesøk.",
            "- Ikke les generalisering som partikkelbevis; les det som støtte for at mekanismene ikke bare var lokale etiketter.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15k",
            "",
            "Denne runden tar de forklaringene vi hadde for lange kollisjonsforløp og tester dem på nye, nærliggende eksempler.",
            "",
            "Spørsmålet er enkelt: hvis vi fant en god mekanisk forklaring i v15j, dukker den samme forklaringen opp igjen på lignende forløp, eller var den bare en lokal historie for akkurat de første eksemplene?",
            "",
            "Det gjør denne runden til en nøktern generaliseringstest, ikke en jakt på noe mer spektakulært.",
        ]
    ) + "\n"

    write_csv(args.out_component_csv, component_rows)
    write_csv(args.out_event_log_csv, event_rows)
    write_csv(args.out_v15h_summary_csv, v15h_summary_rows)
    write_csv(args.out_v15i_summary_csv, v15i_summary_rows)
    write_csv(args.out_v15j_summary_csv, summary_out)
    write_csv(args.out_aggregate_csv, aggregate_rows)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
