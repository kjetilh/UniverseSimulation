#!/usr/bin/env python3
"""v0.15as horizon-map holdout for the add_chord high boundary.

This round follows v15ar. v15ar gave real new knowledge: the delayed high
boundary looked sharper as a small horizon map than as a pure launch-impulse
view.

The next narrow question is:

does that horizon map hold on a few nearby seeds around the representative
anchors, or is it mostly an anchor-only description?
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


TARGET = 48
GROWTH_SEED = 202
FULL_STEPS = 2560
LOG_EVERY = 8
WINDOW = v15ar.WINDOW

HOLDOUT_SPECS = (
    {
        "placement": 2,
        "anchor_run_seed": 5002241,
        "anchor_seed_delta": 239,
        "expected_horizon_label": "established_hold_horizon",
        "holdout_seed_deltas": (231, 247),
    },
    {
        "placement": 1,
        "anchor_run_seed": 5002220,
        "anchor_seed_delta": 219,
        "expected_horizon_label": "terminal_probe_horizon",
        "holdout_seed_deltas": (211, 227),
    },
    {
        "placement": 2,
        "anchor_run_seed": 5002221,
        "anchor_seed_delta": 219,
        "expected_horizon_label": "failed_probe_horizon",
        "holdout_seed_deltas": (211, 227),
    },
    {
        "placement": 1,
        "anchor_run_seed": 5002240,
        "anchor_seed_delta": 239,
        "expected_horizon_label": "no_high_presence",
        "holdout_seed_deltas": (231, 247),
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


def holdout_status(expected: str, observed: str) -> str:
    if observed == expected:
        return "expected_horizon_replicates"
    if observed == "mixed_horizon":
        return "mixed_holdout"
    return "different_horizon"


def holdout_note(status: str, expected: str, observed: str) -> str:
    if status == "expected_horizon_replicates":
        return f"Holdout-runet holder forventet `{expected}`."
    if status == "mixed_holdout":
        return f"Holdout-runet blir ikke rent lest; forventet `{expected}`, observert `{observed}`."
    return f"Holdout-runet skifter fra forventet `{expected}` til `{observed}`."


def analyze_holdout_run(
    *,
    base_state: Any,
    placement: int,
    anchor_seed_delta: int,
    holdout_seed_delta: int,
    anchor_run_seed: int,
    expected_horizon_label: str,
) -> Dict[str, Any]:
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    run_seed = int(base_run_seed_for(placement) + holdout_seed_delta)
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
        seed_delta=holdout_seed_delta,
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
            source_group="horizon_holdout",
            anchor_seed_delta=anchor_seed_delta,
            holdout_seed_delta=holdout_seed_delta,
            family_tag="high_horizon",
        )
        for row in snap_rows
        if int(row["shell_active_nodes"]) > 0
    ]
    bands = [str(row["shell_count_band"]) for row in normalized[:WINDOW]]
    high_start_raw = v15ar.first_run_ge(bands, "high", 3)
    high_start = WINDOW if high_start_raw is None else int(high_start_raw)
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
    last12 = bands[-12:]
    last12_high = sum(1 for band in last12 if band == "high") / max(1, len(last12)) if last12 else 0.0
    last12_mid = sum(1 for band in last12 if band == "mid") / max(1, len(last12)) if last12 else 0.0
    last12_low = sum(1 for band in last12 if band == "low") / max(1, len(last12)) if last12 else 0.0
    observed = v15ar.classify_horizon(
        high_start_index=high_start,
        last_high_index=last_high,
        high_horizon_span=high_horizon,
        high_retention_rate=retention,
        last12_high_rate=last12_high,
    )
    status = holdout_status(expected_horizon_label, observed)
    return {
        "target_nodes": TARGET,
        "growth_seed": GROWTH_SEED,
        "placement": int(placement),
        "anchor_run_seed": int(anchor_run_seed),
        "anchor_seed_delta": int(anchor_seed_delta),
        "holdout_seed_delta": int(holdout_seed_delta),
        "run_seed": int(run_seed),
        "expected_horizon_label": expected_horizon_label,
        "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
        "support_signature": support_signature,
        "full_label": full_label,
        "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
        "high_start_index": int(high_start),
        "last_high_index": int(last_high),
        "high_horizon_span": int(high_horizon),
        "high_retention_rate": float(retention),
        "last12_high_rate": float(last12_high),
        "last12_mid_rate": float(last12_mid),
        "last12_low_rate": float(last12_low),
        "observed_horizon_label": observed,
        "holdout_status": status,
        "holdout_note": holdout_note(status, expected_horizon_label, observed),
    }


def run_rows(*, base_state: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for spec in HOLDOUT_SPECS:
        for holdout_seed_delta in spec["holdout_seed_deltas"]:
            rows.append(
                analyze_holdout_run(
                    base_state=base_state,
                    placement=int(spec["placement"]),
                    anchor_seed_delta=int(spec["anchor_seed_delta"]),
                    holdout_seed_delta=int(holdout_seed_delta),
                    anchor_run_seed=int(spec["anchor_run_seed"]),
                    expected_horizon_label=str(spec["expected_horizon_label"]),
                )
            )
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for spec in HOLDOUT_SPECS:
        placement = int(spec["placement"])
        anchor_seed_delta = int(spec["anchor_seed_delta"])
        expected = str(spec["expected_horizon_label"])
        group = [
            row
            for row in rows
            if int(row["placement"]) == placement
            and int(row["anchor_seed_delta"]) == anchor_seed_delta
            and str(row["expected_horizon_label"]) == expected
        ]
        observed_counter = Counter(str(row["observed_horizon_label"]) for row in group)
        observed_mode = max(
            observed_counter.items(),
            key=lambda item: (item[1], item[0]),
        )[0]
        out.append(
            {
                "placement": placement,
                "anchor_run_seed": int(spec["anchor_run_seed"]),
                "anchor_seed_delta": anchor_seed_delta,
                "expected_horizon_label": expected,
                "n_holdouts": len(group),
                "match_rate": mean_defined(
                    1.0 if str(row["observed_horizon_label"]) == expected else 0.0 for row in group
                ),
                "mixed_holdout_rate": mean_defined(
                    1.0 if str(row["holdout_status"]) == "mixed_holdout" else 0.0 for row in group
                ),
                "different_horizon_rate": mean_defined(
                    1.0 if str(row["holdout_status"]) == "different_horizon" else 0.0 for row in group
                ),
                "observed_mode": observed_mode,
                "mean_high_start_index": mean_defined(safe_float(row["high_start_index"]) for row in group),
                "mean_high_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group),
                "mean_high_retention_rate": mean_defined(safe_float(row["high_retention_rate"]) for row in group),
                "mean_last12_high_rate": mean_defined(safe_float(row["last12_high_rate"]) for row in group),
                "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in group),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Dict[str, Any]],
    rows: Sequence[Dict[str, Any]],
    aggregate: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary if int(row["target_nodes"]) == TARGET)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    mean_match = mean_defined(safe_float(row["match_rate"]) for row in aggregate)
    families_supported = sum(1 for row in aggregate if safe_float(row["match_rate"]) >= 0.50)
    families_mixed = sum(1 for row in aggregate if safe_float(row["mixed_holdout_rate"]) > 0.0)
    if families_supported >= 3 and mean_match >= 0.50:
        status = "horizon_map_partly_holds"
        note = "Flere av horisontfamiliene holder pa noen fa naerliggende seeds, sa horisont-kartet ser ut til a ha lokal baeree vne utover bare anker-runene."
        next_step = "probe_best_horizon_family"
        next_note = "Neste steg bor vaere en enda smalere forklarings- eller holdout-runde rundt den sterkest replikerende horisontfamilien."
    elif mean_match >= 0.25 or families_mixed >= 2:
        status = "horizon_map_holdout_mixed"
        note = "Horisont-kartet gir fortsatt nyttig struktur pa holdouts, men holder ikke rent nok som lokalt lovmessig kart ennå."
        next_step = "tighten_failed_probe_horizon"
        next_note = "Neste steg bor vaere en enda smalere observabel eller holdout rundt failed-probe og terminal-probe-grensen."
    else:
        status = "horizon_map_not_yet"
        note = "De naerliggende holdout-runene bekrefter ikke horisont-kartet rent nok; dette ser forelopig best ut som en ankerbeskrivelse."
        next_step = "change_high_boundary_observable_again"
        next_note = "Neste steg bor bytte observabel igjen i stedet for a presse horisont-kartet hardere."
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsene er rent separert og alle holdout-runene matcher onsket add_chord-perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjonen eller perturbasjonsmatchen er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "horizon_holdout_status",
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
    aggregate: Sequence[Dict[str, Any]],
    diagnosis: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15as: horizon map holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om det lille high-horisont-kartet fra `v15ar` holder pa noen fa naerliggende seeds rundt de representative anker-runene.")
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
    lines.append("## Holdout summary")
    lines.append("")
    lines.append("| placement | anchor run | anchor delta | expected | match | mixed | different | observed mode | mean horizon | mean retention |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['placement'])} | {int(row['anchor_run_seed'])} | {int(row['anchor_seed_delta'])} | {row['expected_horizon_label']} | {fmt(row['match_rate'])} | {fmt(row['mixed_holdout_rate'])} | {fmt(row['different_horizon_rate'])} | {row['observed_mode']} | {fmt(row['mean_high_horizon_span'])} | {fmt(row['mean_high_retention_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en liten holdout-runde rundt horisontankrene, ikke en ny bred seed-scan.")
    lines.append("- Les horisont-labelene som lokale high-forlop, ikke som nye defect-arter.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15as horizon map holdout.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15as_horizon_map_holdout_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15as_horizon_map_holdout_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15as_horizon_map_holdout_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15as_horizon_map_holdout_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15as_horizon_map_holdout.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15as_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15as.md")
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
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15as operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en smal holdout-test av horisont-kartet, ikke som en ny bred defect-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15as",
            "",
            "Etter at `v15ar` viste at high-grensen kan leses som et lite horisont-kart, tester denne runden om de samme typene dukker opp igjen i noen fa naerliggende tilfeller.",
            "",
            "Målet er ikke a bevise nye arter, men a se om kartet har lokal baeree vne utover de opprinnelige anker-runene.",
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
