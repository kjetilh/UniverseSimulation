#!/usr/bin/env python3
"""v0.15at high-burst window lab for the delayed high boundary.

This round follows v15as. v15as showed that the small horizon map had real
anchor value, but that nearby holdouts mostly collapsed down to no-high.

The next narrow question is:

can the same boundary be read more honestly as a small burst map, where the key
difference is not just whether high holds, but whether the run forms:

- a sustained high burst,
- a compact terminal burst,
- a failed early burst,
- no high burst,
- or a fading late burst?
"""
from __future__ import annotations

import argparse
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15ai_early_lock_band_lab as v15ai
import relational_universe_v15ar_high_retention_horizon_lab as v15ar
import relational_universe_v15as_horizon_map_holdout as v15as


TARGET = 48
GROWTH_SEED = 202
FULL_STEPS = 2560
LOG_EVERY = 8
WINDOW = v15ar.WINDOW
BURST_WINDOW = 8

ANCHOR_SPECS = (
    {
        "row_role": "anchor_focus",
        "placement": 2,
        "seed_delta": 239,
        "anchor_run_seed": 5002241,
        "expected_horizon_label": "established_hold_horizon",
    },
    {
        "row_role": "anchor_focus",
        "placement": 1,
        "seed_delta": 219,
        "anchor_run_seed": 5002220,
        "expected_horizon_label": "terminal_probe_horizon",
    },
    {
        "row_role": "anchor_focus",
        "placement": 2,
        "seed_delta": 219,
        "anchor_run_seed": 5002221,
        "expected_horizon_label": "failed_probe_horizon",
    },
    {
        "row_role": "anchor_focus",
        "placement": 1,
        "seed_delta": 239,
        "anchor_run_seed": 5002240,
        "expected_horizon_label": "no_high_presence",
    },
)


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


def base_run_seed_for(placement: int) -> int:
    return TARGET * 100000 + GROWTH_SEED * 1000 + int(placement)


def rolling_high_peak(bands: Sequence[str], window: int) -> tuple[int, float]:
    if not bands:
        return WINDOW, 0.0
    best_start = 0
    best_rate = -1.0
    for start in range(0, max(1, len(bands) - window + 1)):
        window_bands = bands[start:start + window]
        rate = sum(1 for band in window_bands if band == "high") / max(1, len(window_bands))
        if rate > best_rate:
            best_rate = rate
            best_start = start
    return best_start, max(0.0, best_rate)


def longest_run(values: Sequence[str], target: str) -> int:
    best = 0
    current = 0
    for value in values:
        if value == target:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def classify_burst(
    *,
    first_high_index: int,
    last_high_index: int,
    high_horizon_span: int,
    high_retention_rate: float,
    last12_high_rate: float,
    total_high_count: int,
    peak_high_window_rate: float,
) -> str:
    if first_high_index >= WINDOW:
        return "no_high_burst"
    if total_high_count == 0:
        return "no_high_burst"
    if last12_high_rate >= 0.50 and high_horizon_span >= 24 and high_retention_rate >= 0.65:
        return "sustained_hold_burst"
    if first_high_index >= 64 and total_high_count <= 4 and last12_high_rate <= 0.25:
        return "terminal_compact_burst"
    if first_high_index <= 16 and last_high_index <= 32 and high_horizon_span >= 12 and last12_high_rate == 0.0:
        return "early_failed_burst"
    if first_high_index >= 32 and total_high_count >= 8 and peak_high_window_rate >= 0.50 and last12_high_rate < 0.50:
        return "fading_late_burst"
    return "mixed_burst"


def burst_note(label: str) -> str:
    if label == "sustained_hold_burst":
        return "Runet bygger en reell high-burst som holder helt inn i tail-slutten."
    if label == "terminal_compact_burst":
        return "Runet far bare en kort, sen og kompakt high-burst."
    if label == "early_failed_burst":
        return "Runet far en tidlig high-burst som glipper og dør ut."
    if label == "no_high_burst":
        return "Runet far ingen faktisk high-burst."
    if label == "fading_late_burst":
        return "Runet naermer seg et sent hold, men high-bursten fader ut for tail-slutt."
    return "Burst-observabelen leser fortsatt ikke runet helt rent."


def analyze_run(
    *,
    base_state: Any,
    row_role: str,
    placement: int,
    seed_delta: int,
    anchor_run_seed: int,
    expected_horizon_label: str,
    anchor_seed_delta: int,
) -> Dict[str, Any]:
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    run_seed = int(base_run_seed_for(placement) + seed_delta)
    res = v15ae.run_defect_with_control_graphs(
        base_state,
        params=params,
        seed=run_seed,
        steps=FULL_STEPS,
        perturbation="add_chord",
        center_token_index=placement,
        local_coupling="maximal",
        log_every=LOG_EVERY,
    )
    info = dict(res["perturbation_info"])
    support_signature = ",".join(str(x) for x in info.get("support", []))
    recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
    full_label = v15q.classify_recurrence_label(int(res["log_rows"][-1]["alive"]), recurrence)
    partition = v15ae.occupancy_partition(res["damaged_sets"])
    snap_rows = v15ae.shell_snapshot_rows(
        placement=placement,
        seed_delta=seed_delta,
        run_seed=run_seed,
        support_signature=support_signature,
        core_nodes=set(partition["core_nodes"]),
        shell_nodes=set(partition["shell_nodes"]),
        log_rows=res["log_rows"],
        damaged_sets=res["damaged_sets"],
        control_graphs=res["control_graphs"],
    )
    normalized = [
        v15ai.normalize_snapshot_row(
            row,
            source_group=row_role,
            anchor_seed_delta=anchor_seed_delta,
            holdout_seed_delta=seed_delta if row_role == "holdout_focus" else -1,
            family_tag="high_burst",
        )
        for row in snap_rows
        if int(row["shell_active_nodes"]) > 0
    ]
    bands = [str(row["shell_count_band"]) for row in normalized[:WINDOW]]
    high_start_raw = v15ar.first_run_ge(bands, "high", 3)
    first_high_index = WINDOW if high_start_raw is None else int(high_start_raw)
    if high_start_raw is None:
        last_high = -1
        high_horizon = 0
        retention = 0.0
    else:
        high_positions = [idx for idx, band in enumerate(bands) if band == "high" and idx >= high_start_raw]
        last_high = max(high_positions)
        horizon_slice = bands[high_start_raw:last_high + 1]
        high_horizon = len(horizon_slice)
        retention = sum(1 for band in horizon_slice if band == "high") / max(1, len(horizon_slice))
    total_high_count = sum(1 for band in bands if band == "high")
    total_mid_count = sum(1 for band in bands if band == "mid")
    peak_start, peak_rate = rolling_high_peak(bands, BURST_WINDOW)
    last12 = bands[-12:]
    last12_high_rate = sum(1 for band in last12 if band == "high") / max(1, len(last12)) if last12 else 0.0
    label = classify_burst(
        first_high_index=first_high_index,
        last_high_index=last_high,
        high_horizon_span=high_horizon,
        high_retention_rate=retention,
        last12_high_rate=last12_high_rate,
        total_high_count=total_high_count,
        peak_high_window_rate=peak_rate,
    )
    return {
        "row_role": row_role,
        "placement": int(placement),
        "anchor_run_seed": int(anchor_run_seed),
        "anchor_seed_delta": int(anchor_seed_delta),
        "seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "expected_horizon_label": expected_horizon_label,
        "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
        "support_signature": support_signature,
        "full_label": full_label,
        "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
        "first_high_index": int(first_high_index),
        "last_high_index": int(last_high),
        "high_horizon_span": int(high_horizon),
        "high_retention_rate": float(retention),
        "total_high_count": int(total_high_count),
        "total_mid_count": int(total_mid_count),
        "peak_high_window_start": int(peak_start),
        "peak_high_window_rate": float(peak_rate),
        "longest_high_run": int(longest_run(bands, "high")),
        "last12_high_rate": float(last12_high_rate),
        "burst_label": label,
        "burst_note": burst_note(label),
    }


def run_rows(*, base_state: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for spec in ANCHOR_SPECS:
        rows.append(
            analyze_run(
                base_state=base_state,
                row_role=str(spec["row_role"]),
                placement=int(spec["placement"]),
                seed_delta=int(spec["seed_delta"]),
                anchor_run_seed=int(spec["anchor_run_seed"]),
                expected_horizon_label=str(spec["expected_horizon_label"]),
                anchor_seed_delta=int(spec["seed_delta"]),
            )
        )
    for spec in v15as.HOLDOUT_SPECS:
        for holdout_seed_delta in spec["holdout_seed_deltas"]:
            rows.append(
                analyze_run(
                    base_state=base_state,
                    row_role="holdout_focus",
                    placement=int(spec["placement"]),
                    seed_delta=int(holdout_seed_delta),
                    anchor_run_seed=int(spec["anchor_run_seed"]),
                    expected_horizon_label=str(spec["expected_horizon_label"]),
                    anchor_seed_delta=int(spec["anchor_seed_delta"]),
                )
            )
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    def add_group(group_type: str, group_value: str, group_rows: Sequence[Dict[str, Any]]) -> None:
        if not group_rows:
            return
        burst_counter = Counter(str(row["burst_label"]) for row in group_rows)
        burst_mode = max(burst_counter.items(), key=lambda item: (item[1], item[0]))[0]
        out.append(
            {
                "group_type": group_type,
                "group_value": group_value,
                "n_runs": len(group_rows),
                "sustained_hold_burst_rate": mean_defined(
                    1.0 if str(row["burst_label"]) == "sustained_hold_burst" else 0.0 for row in group_rows
                ),
                "terminal_compact_burst_rate": mean_defined(
                    1.0 if str(row["burst_label"]) == "terminal_compact_burst" else 0.0 for row in group_rows
                ),
                "early_failed_burst_rate": mean_defined(
                    1.0 if str(row["burst_label"]) == "early_failed_burst" else 0.0 for row in group_rows
                ),
                "no_high_burst_rate": mean_defined(
                    1.0 if str(row["burst_label"]) == "no_high_burst" else 0.0 for row in group_rows
                ),
                "fading_late_burst_rate": mean_defined(
                    1.0 if str(row["burst_label"]) == "fading_late_burst" else 0.0 for row in group_rows
                ),
                "mixed_burst_rate": mean_defined(
                    1.0 if str(row["burst_label"]) == "mixed_burst" else 0.0 for row in group_rows
                ),
                "burst_mode": burst_mode,
                "mean_total_high_count": mean_defined(safe_float(row["total_high_count"]) for row in group_rows),
                "mean_peak_high_window_rate": mean_defined(safe_float(row["peak_high_window_rate"]) for row in group_rows),
                "mean_last12_high_rate": mean_defined(safe_float(row["last12_high_rate"]) for row in group_rows),
                "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in group_rows),
            }
        )

    for row_role in ("anchor_focus", "holdout_focus"):
        add_group("row_role", row_role, [row for row in rows if str(row["row_role"]) == row_role])
    for expected in sorted({str(row["expected_horizon_label"]) for row in rows}):
        add_group("expected_horizon_label", expected, [row for row in rows if str(row["expected_horizon_label"]) == expected])
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Dict[str, Any]],
    rows: Sequence[Dict[str, Any]],
    aggregate: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary if int(row["target_nodes"]) == TARGET)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    agg_lookup = {(str(row["group_type"]), str(row["group_value"])): row for row in aggregate}
    anchors = agg_lookup[("row_role", "anchor_focus")]
    holdouts = agg_lookup[("row_role", "holdout_focus")]
    expected_labels = {str(row["burst_label"]) for row in rows if str(row["row_role"]) == "anchor_focus"}
    if expected_labels >= {"sustained_hold_burst", "terminal_compact_burst", "early_failed_burst", "no_high_burst"}:
        if safe_float(holdouts["no_high_burst_rate"]) >= 0.60 or safe_float(holdouts["fading_late_burst_rate"]) >= 0.20:
            status = "burst_map_sharpens_holdout_collapse"
            note = "Burst-observabelen holder ankerkartet rent og viser samtidig at naerliggende holdouts hovedsakelig kollapser til `no_high_burst`, med et lite restspor av `fading_late_burst` i stedet for ekte hold."
            next_step = "explain_fading_late_burst"
            next_note = "Neste steg bor forklare det lille `fading_late_burst`-sporet i stedet for a presse horisontkartet hardere."
        else:
            status = "burst_map_supported_but_flat"
            note = "Burst-observabelen holder ankerkartet rent, men holdouts gir nesten bare total no-high-kollaps."
            next_step = "tighten_no_high_boundary"
            next_note = "Neste steg bor forklare hva som skiller full no-high-kollaps fra selv svake high-forsok."
    else:
        status = "burst_map_still_mixed"
        note = "Burst-observabelen gjor ikke den skjore high-grensen ren nok ennå."
        next_step = "change_boundary_observable_again"
        next_note = "Neste steg bor bytte observabel igjen i stedet for a presse burst-kartet hardere."
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
            "diagnostic_family": "burst_map_status",
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
    target_summary: Sequence[Dict[str, Any]],
    rows: Sequence[Dict[str, Any]],
    aggregate: Sequence[Dict[str, Any]],
    diagnosis: Sequence[Dict[str, Any]],
) -> str:
    row_role_rows = [row for row in aggregate if str(row["group_type"]) == "row_role"]
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15at: high burst window lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om den skjore high-grensen leses bedre som et lite burst-kart enn som bare horisont- eller impulse-etiketter.")
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
    lines.append("## Focus runs")
    lines.append("")
    lines.append("| role | run seed | expected horizon | first high | last high | total high | peak start | peak rate | burst label |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(rows, key=lambda r: (str(r["row_role"]), int(r["run_seed"]))):
        lines.append(
            f"| {row['row_role']} | {int(row['run_seed'])} | {row['expected_horizon_label']} | {int(row['first_high_index'])} | {int(row['last_high_index'])} | {int(row['total_high_count'])} | {int(row['peak_high_window_start'])} | {fmt(row['peak_high_window_rate'])} | {row['burst_label']} |"
        )
    lines.append("")
    lines.append("## Aggregate by role")
    lines.append("")
    lines.append("| role | n | sustained | terminal | failed | no-high | fading late | mixed | burst mode |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in row_role_rows:
        lines.append(
            f"| {row['group_value']} | {int(row['n_runs'])} | {fmt(row['sustained_hold_burst_rate'])} | {fmt(row['terminal_compact_burst_rate'])} | {fmt(row['early_failed_burst_rate'])} | {fmt(row['no_high_burst_rate'])} | {fmt(row['fading_late_burst_rate'])} | {fmt(row['mixed_burst_rate'])} | {row['burst_mode']} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en liten burst-runde rundt samme boundary-run, ikke en ny bred seed-scan.")
    lines.append("- Les burst-labelene som lokale high-forlop, ikke som nye defect-arter.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15at high burst window lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15at_high_burst_window_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15at_high_burst_window_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15at_high_burst_window_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15at_high_burst_window_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15at_high_burst_window_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15at_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15at.md")
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
    report_md = build_report(target_summary=target_summary, rows=rows, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15at operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en smal burst-observabel rundt den skjore high-grensen, ikke som en ny bred defect-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15at",
            "",
            "Etter at horisont-kartet viste at bare no-high er lokalt robust, prover denne runden en enklere lesning: om runet i det hele tatt lager en reell high-burst, og om den holder, feiler tidlig eller fader sent.",
            "",
            "Målet er a fa et mer jordnaert kart over den skjore grensen mellom high-forsok og ingen high.",
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
