#!/usr/bin/env python3
"""v0.15ah shell exception holdout for add_chord recurrence band.

This round follows v15ag. The minority shell-fragmentation exceptions now look
locally explainable, but we still do not know whether those exception
mechanisms replicate on nearby seeds.

This is a narrow holdout test:
- same local `t48_g202` add_chord band
- only nearby holdout seeds around the known exception anchors
- same shell-topology and fragment-timing observables
"""
from __future__ import annotations

import argparse
import math
import random
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15af_add_chord_shell_fragment_event_lab as v15af
import relational_universe_v15ag_shell_exception_explainer as v15ag


TARGET = 48
GROWTH_SEED = 202
FULL_STEPS = 2560
LOG_EVERY = 8

HOLDOUT_SPECS = (
    {
        "placement": 0,
        "anchor_seed_delta": 239,
        "expected_mechanism": "alternating_to_late_lock",
        "holdout_seed_deltas": (231, 247),
    },
    {
        "placement": 1,
        "anchor_seed_delta": 151,
        "expected_mechanism": "alternating_to_late_lock",
        "holdout_seed_deltas": (143, 159),
    },
    {
        "placement": 1,
        "anchor_seed_delta": 179,
        "expected_mechanism": "two_stage_fragment_lock",
        "holdout_seed_deltas": (171, 187),
    },
    {
        "placement": 1,
        "anchor_seed_delta": 211,
        "expected_mechanism": "near_lock_boundary_case",
        "holdout_seed_deltas": (203, 219),
    },
    {
        "placement": 2,
        "anchor_seed_delta": 151,
        "expected_mechanism": "singleton_resistance_case",
        "holdout_seed_deltas": (143, 159),
    },
    {
        "placement": 2,
        "anchor_seed_delta": 211,
        "expected_mechanism": "alternating_to_late_lock",
        "holdout_seed_deltas": (203, 219),
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


def outcome_label(expected_mechanism: str, timing_label: str, mechanism_label: str) -> str:
    if mechanism_label == expected_mechanism:
        return "expected_exception_replicates"
    if timing_label == "early_fragment_lock":
        return "reverts_to_main_family"
    if mechanism_label in {
        "alternating_to_late_lock",
        "two_stage_fragment_lock",
        "singleton_resistance_case",
        "near_lock_boundary_case",
    }:
        return "different_exception_mechanism"
    return "unresolved_holdout"


def analyze_holdout_run(
    *,
    base_state: Any,
    placement: int,
    seed_delta: int,
    expected_mechanism: str,
) -> Dict[str, Any]:
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    base_run_seed = TARGET * 100000 + GROWTH_SEED * 1000 + int(placement)
    run_seed = int(base_run_seed + seed_delta)

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

    active_rows = [r for r in snap_rows if int(r["shell_active_nodes"]) > 0]
    active_states = [v15af.shell_state({k: str(v) for k, v in row.items()}) for row in active_rows]
    frag_flags = [1 if st == "fragmented" else 0 for st in active_states]
    first_fragment_local_index = next((i for i, x in enumerate(frag_flags) if x == 1), -1)
    first_fragment_step = int(active_rows[first_fragment_local_index]["step"]) if first_fragment_local_index >= 0 else -1
    connected_prefix_steps = max(0, first_fragment_local_index) * LOG_EVERY
    fragmented_suffix = frag_flags[first_fragment_local_index:] if first_fragment_local_index >= 0 else []
    fragmented_suffix_rate = (sum(fragmented_suffix) / len(fragmented_suffix)) if fragmented_suffix else 0.0
    state_switch_count = sum(1 for a, b in zip(active_states, active_states[1:]) if a != b)
    seg_rows = v15af.segment_rows_for_run(
        placement=placement,
        seed_delta=seed_delta,
        run_seed=run_seed,
        support_signature=support_signature,
        rows=[{k: str(v) for k, v in row.items()} for row in active_rows],
    )
    frag_segments = [r for r in seg_rows if str(r["segment_state"]) == "fragmented"]
    connected_segments = [r for r in seg_rows if str(r["segment_state"]) == "connected"]
    max_connected_segment_snapshots = max((int(r["segment_snapshot_count"]) for r in connected_segments), default=0)
    longest_connected_steps = max_connected_segment_snapshots * LOG_EVERY
    final_fragment_steps = (
        safe_float(frag_segments[-1]["segment_snapshot_count"]) * LOG_EVERY
        if frag_segments and str(seg_rows[-1]["segment_state"]) == "fragmented"
        else 0.0
    )
    timing_label = v15af.classify_fragment_timing(
        first_fragment_local_index=first_fragment_local_index,
        fragmented_suffix_rate=float(fragmented_suffix_rate),
        state_switch_count=int(state_switch_count),
        max_connected_segment_snapshots=int(max_connected_segment_snapshots),
    )
    mean_shell_component_count = mean_defined(safe_float(row["shell_component_count"]) for row in active_rows)
    mechanism_label = (
        "early_fragment_lock"
        if timing_label == "early_fragment_lock"
        else v15ag.classify_exception_mechanism(
            timing_label=timing_label,
            connected_prefix_steps=float(connected_prefix_steps),
            longest_connected_steps=float(longest_connected_steps),
            final_fragment_steps=float(final_fragment_steps),
            fragmented_suffix_rate=float(fragmented_suffix_rate),
            state_switch_count=float(state_switch_count),
            mean_shell_component_count=float(mean_shell_component_count),
        )
    )

    return {
        "target_nodes": TARGET,
        "growth_seed": GROWTH_SEED,
        "placement": int(placement),
        "anchor_seed_delta": int(seed_delta),  # overwritten by caller for clarity
        "holdout_seed_delta": int(seed_delta),
        "run_seed": int(run_seed),
        "expected_mechanism": expected_mechanism,
        "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
        "support_signature": support_signature,
        "full_label": full_label,
        "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
        "shell_nodes": int(len(partition["shell_nodes"])),
        "first_fragment_step": int(first_fragment_step),
        "connected_prefix_steps": int(connected_prefix_steps),
        "fragmented_suffix_rate": float(fragmented_suffix_rate),
        "state_switch_count": int(state_switch_count),
        "longest_connected_steps": float(longest_connected_steps),
        "final_fragment_steps": float(final_fragment_steps),
        "timing_label": timing_label,
        "holdout_mechanism_label": mechanism_label,
        "holdout_outcome_label": outcome_label(expected_mechanism, timing_label, mechanism_label),
    }


def run_rows(*, base_state: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for spec in HOLDOUT_SPECS:
        placement = int(spec["placement"])
        anchor_seed_delta = int(spec["anchor_seed_delta"])
        expected_mechanism = str(spec["expected_mechanism"])
        for holdout_seed_delta in spec["holdout_seed_deltas"]:
            row = analyze_holdout_run(
                base_state=base_state,
                placement=placement,
                seed_delta=int(holdout_seed_delta),
                expected_mechanism=expected_mechanism,
            )
            row["anchor_seed_delta"] = anchor_seed_delta
            rows.append(row)
    return rows


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for spec in HOLDOUT_SPECS:
        placement = int(spec["placement"])
        anchor_seed_delta = int(spec["anchor_seed_delta"])
        expected_mechanism = str(spec["expected_mechanism"])
        group = [
            row
            for row in rows
            if int(row["placement"]) == placement and int(row["anchor_seed_delta"]) == anchor_seed_delta
        ]
        out.append(
            {
                "placement": placement,
                "anchor_seed_delta": anchor_seed_delta,
                "expected_mechanism": expected_mechanism,
                "n_holdouts": len(group),
                "expected_match_rate": mean_defined(
                    1.0 if str(row["holdout_mechanism_label"]) == expected_mechanism else 0.0 for row in group
                ),
                "main_family_revert_rate": mean_defined(
                    1.0 if str(row["holdout_mechanism_label"]) == "early_fragment_lock" else 0.0 for row in group
                ),
                "different_exception_rate": mean_defined(
                    1.0 if str(row["holdout_outcome_label"]) == "different_exception_mechanism" else 0.0 for row in group
                ),
                "unresolved_rate": mean_defined(
                    1.0 if str(row["holdout_outcome_label"]) == "unresolved_holdout" else 0.0 for row in group
                ),
                "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in group),
                "mean_fragmented_suffix_rate": mean_defined(safe_float(row["fragmented_suffix_rate"]) for row in group),
                "mean_state_switch_count": mean_defined(safe_float(row["state_switch_count"]) for row in group),
            }
        )
    return out


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    mean_expected_match = mean_defined(safe_float(row["expected_match_rate"]) for row in aggregate)
    mean_revert = mean_defined(safe_float(row["main_family_revert_rate"]) for row in aggregate)
    anchor_families_with_replication = sum(1 for row in aggregate if safe_float(row["expected_match_rate"]) >= 0.50)

    if anchor_families_with_replication >= 3 and mean_expected_match >= 0.50:
        status = "exception_mechanisms_partly_hold"
        note = "Flere av unntaksmekanismene replikerer faktisk på nærliggende holdout-seeds, så dette er mer enn bare pen ankerbeskrivelse."
        next_step = "probe_best_exception_family"
        next_note = "Neste steg bør være en enda smalere oppfølging av den best replikerende unntaksfamilien."
    elif mean_revert >= 0.50:
        status = "exceptions_mostly_revert_to_main_family"
        note = "De fleste nærliggende holdouts faller tilbake til `early_fragment_lock`, så hovedkunnskapen er at unntakene er lokale avvik rundt en sterk hovedfamilie."
        next_step = "stop_exception_expansion"
        next_note = "Neste steg bør ikke være bredere unntaks-scan; vi bør heller bruke dette som støtte for at early-lock-familien er den robuste live-lesningen."
    else:
        status = "exception_holdout_mixed"
        note = "Holdout-runden viser noe struktur, men ikke rent nok til å si at unntaksmekanismene allerede generaliserer eller kollapser tilbake til hovedfamilien."
        next_step = "tighten_exception_holdout"
        next_note = "Neste steg bør være en enda mindre holdout rundt bare de mest informative unntaksankrene."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er rent separert og alle holdout-radene matcher ønsket add_chord-perturbasjon."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "exception_holdout_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, target_summary: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]], diagnosis: Sequence[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15ah: shell exception holdout")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append("Denne runden tester om de små unntaksmekanismene fra `v15ag` faktisk replikerer på noen få nærliggende holdout-seeds, eller om de fleste holdouts faller tilbake til hovedfamilien `early_fragment_lock`.")
    lines.append("")
    lines.append("## Startstørrelser")
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
    lines.append("| placement | anchor seed | expected | match | revert to main | different exception | unresolved | exact return |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['placement'])} | {int(row['anchor_seed_delta'])} | {row['expected_mechanism']} | {fmt(row['expected_match_rate'])} | {fmt(row['main_family_revert_rate'])} | {fmt(row['different_exception_rate'])} | {fmt(row['unresolved_rate'])} | {fmt(row['mean_full_exact_return_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en liten holdout-runde rundt de kjente unntakene, ikke en ny bred seed-scan.")
    lines.append("- Les dette som test av lokal generalisering, ikke som bevis for nye defect-arter.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ah shell exception holdout.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15ah_shell_exception_holdout_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ah_shell_exception_holdout_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ah_shell_exception_holdout_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15ah_shell_exception_holdout_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ah_shell_exception_holdout.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ah_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ah.md")
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
    diagnosis = diagnosis_rows(target_summary, rows, aggregate)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15ah operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en smal holdout-test av unntaksmekanismene, ikke som en ny bred defect-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15ah",
            "",
            "Etter at vi fant noen få lokale unntak fra hovedmønsteret, tester denne runden om de samme unntakene dukker opp igjen i noen få nærliggende tilfeller.",
            "",
            "Målet er å finne ut om de små unntakene faktisk gjentar seg, eller om de fleste nærliggende tilfeller faller tilbake til hovedmønsteret.",
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
