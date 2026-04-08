#!/usr/bin/env python3
"""v0.15af add_chord shell fragment event lab.

This round follows v15ae and asks a narrower timing question inside the same
local add_chord cycle band:

if the shell is usually fragmented, does that fragmentation begin almost
immediately in the tail and then lock in, or does it arrive later through
smaller local event chains?

This script runs no new simulations. It analyzes the real v15ae snapshot data.
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
IN_SNAPSHOTS = DOC / "v15ae_add_chord_shell_topology_snapshots.csv"
IN_RUNS = DOC / "v15ae_add_chord_shell_topology_runs.csv"
IN_TARGET = DOC / "v15ae_add_chord_shell_topology_target_summary.csv"

TARGET = 48
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2)


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


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def shell_state(row: Mapping[str, str]) -> str:
    active = int(row["shell_active_nodes"])
    if active <= 0:
        return "inactive"
    return "fragmented" if int(row["shell_component_count"]) >= 2 else "connected"


def classify_fragment_timing(
    *,
    first_fragment_local_index: int,
    fragmented_suffix_rate: float,
    state_switch_count: int,
    max_connected_segment_snapshots: int,
) -> str:
    if first_fragment_local_index >= 0 and first_fragment_local_index <= 1 and fragmented_suffix_rate >= 0.85:
        return "early_fragment_lock"
    if first_fragment_local_index >= 2 and fragmented_suffix_rate >= 0.85:
        return "delayed_fragment_lock"
    if fragmented_suffix_rate < 0.45 and state_switch_count >= 8 and max_connected_segment_snapshots >= 24:
        return "connected_resistance_churn"
    if fragmented_suffix_rate >= 0.45 and state_switch_count >= 6:
        return "intermittent_fragment_churn"
    return "mixed_fragment_timing"


def segment_rows_for_run(
    placement: int,
    seed_delta: int,
    run_seed: int,
    support_signature: str,
    rows: Sequence[Mapping[str, str]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if not rows:
        return out
    start = 0
    states = [shell_state(r) for r in rows]
    for idx in range(1, len(rows) + 1):
        if idx < len(rows) and states[idx] == states[start]:
            continue
        seg_rows = rows[start:idx]
        comp_counts = [safe_float(r["shell_component_count"]) for r in seg_rows]
        attach_fracs = [safe_float(r["shell_attachment_node_frac"]) for r in seg_rows if math.isfinite(safe_float(r["shell_attachment_node_frac"]))]
        boundary_vals = [safe_float(r["shell_boundary_to_volume"]) for r in seg_rows if math.isfinite(safe_float(r["shell_boundary_to_volume"]))]
        out.append(
            {
                "placement": int(placement),
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
                "mean_shell_component_count": mean_defined(comp_counts),
                "mean_attachment_node_frac": mean_defined(attach_fracs),
                "mean_shell_boundary_to_volume": mean_defined(boundary_vals),
            }
        )
        start = idx
    return out


def run_analysis(
    *,
    snapshot_rows_in: Sequence[Mapping[str, str]],
    run_rows_in: Sequence[Mapping[str, str]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    by_run: Dict[Tuple[int, int], List[Dict[str, str]]] = defaultdict(list)
    support_lookup: Dict[Tuple[int, int], Tuple[int, str]] = {}

    for row in run_rows_in:
        key = (int(row["placement"]), int(row["seed_delta"]))
        support_lookup[key] = (int(row["run_seed"]), str(row["support_signature"]))

    for row in snapshot_rows_in:
        key = (int(row["placement"]), int(row["seed_delta"]))
        by_run[key].append(dict(row))

    run_rows_out: List[Dict[str, Any]] = []
    segment_rows_out: List[Dict[str, Any]] = []

    for placement in PLACEMENTS:
        for seed_delta in sorted(k[1] for k in by_run if k[0] == placement):
            key = (placement, seed_delta)
            rows = sorted(by_run[key], key=lambda r: int(r["step"]))
            run_seed, support_signature = support_lookup[key]
            active_rows = [r for r in rows if int(r["shell_active_nodes"]) > 0]
            active_states = [shell_state(r) for r in active_rows]
            frag_flags = [1 if st == "fragmented" else 0 for st in active_states]
            first_fragment_local_index = next((i for i, x in enumerate(frag_flags) if x == 1), -1)
            first_fragment_step = int(active_rows[first_fragment_local_index]["step"]) if first_fragment_local_index >= 0 else -1
            connected_prefix_snapshots = int(first_fragment_local_index) if first_fragment_local_index >= 0 else len(active_rows)
            connected_prefix_steps = connected_prefix_snapshots * 8
            fragmented_suffix = frag_flags[first_fragment_local_index:] if first_fragment_local_index >= 0 else []
            fragmented_suffix_rate = (sum(fragmented_suffix) / len(fragmented_suffix)) if fragmented_suffix else 0.0
            state_switch_count = sum(1 for a, b in zip(active_states, active_states[1:]) if a != b)

            seg_rows = segment_rows_for_run(
                placement=placement,
                seed_delta=seed_delta,
                run_seed=run_seed,
                support_signature=support_signature,
                rows=active_rows,
            )
            segment_rows_out.extend(seg_rows)

            frag_segments = [r for r in seg_rows if str(r["segment_state"]) == "fragmented"]
            connected_segments = [r for r in seg_rows if str(r["segment_state"]) == "connected"]
            max_fragment_segment_snapshots = max((int(r["segment_snapshot_count"]) for r in frag_segments), default=0)
            max_connected_segment_snapshots = max((int(r["segment_snapshot_count"]) for r in connected_segments), default=0)

            timing_label = classify_fragment_timing(
                first_fragment_local_index=first_fragment_local_index,
                fragmented_suffix_rate=float(fragmented_suffix_rate),
                state_switch_count=int(state_switch_count),
                max_connected_segment_snapshots=int(max_connected_segment_snapshots),
            )
            run_rows_out.append(
                {
                    "target_nodes": TARGET,
                    "growth_seed": GROWTH_SEED,
                    "placement": int(placement),
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "support_signature": support_signature,
                    "first_fragment_local_index": int(first_fragment_local_index),
                    "first_fragment_step": int(first_fragment_step),
                    "connected_prefix_snapshots": int(connected_prefix_snapshots),
                    "connected_prefix_steps": int(connected_prefix_steps),
                    "fragmented_suffix_rate": float(fragmented_suffix_rate),
                    "state_switch_count": int(state_switch_count),
                    "segment_count": int(len(seg_rows)),
                    "max_fragment_segment_snapshots": int(max_fragment_segment_snapshots),
                    "max_connected_segment_snapshots": int(max_connected_segment_snapshots),
                    "final_shell_state": active_states[-1] if active_states else "inactive",
                    "timing_label": timing_label,
                }
            )
    return run_rows_out, segment_rows_out


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        group = [row for row in rows if int(row["placement"]) == placement]
        out.append(
            {
                "placement": int(placement),
                "n_runs": len(group),
                "early_fragment_lock_rate": mean_defined(1.0 if str(row["timing_label"]) == "early_fragment_lock" else 0.0 for row in group),
                "delayed_fragment_lock_rate": mean_defined(1.0 if str(row["timing_label"]) == "delayed_fragment_lock" else 0.0 for row in group),
                "intermittent_fragment_churn_rate": mean_defined(1.0 if str(row["timing_label"]) == "intermittent_fragment_churn" else 0.0 for row in group),
                "connected_resistance_churn_rate": mean_defined(1.0 if str(row["timing_label"]) == "connected_resistance_churn" else 0.0 for row in group),
                "mixed_fragment_timing_rate": mean_defined(1.0 if str(row["timing_label"]) == "mixed_fragment_timing" else 0.0 for row in group),
                "mean_first_fragment_step": mean_defined(safe_float(row["first_fragment_step"]) for row in group if safe_float(row["first_fragment_step"]) >= 0),
                "mean_connected_prefix_steps": mean_defined(safe_float(row["connected_prefix_steps"]) for row in group),
                "mean_fragmented_suffix_rate": mean_defined(safe_float(row["fragmented_suffix_rate"]) for row in group),
                "mean_state_switch_count": mean_defined(safe_float(row["state_switch_count"]) for row in group),
                "mean_max_fragment_segment_snapshots": mean_defined(safe_float(row["max_fragment_segment_snapshots"]) for row in group),
                "mean_max_connected_segment_snapshots": mean_defined(safe_float(row["max_connected_segment_snapshots"]) for row in group),
            }
        )
    return out


def diagnosis_rows(target_summary: Sequence[Mapping[str, str]], aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary if int(row["target_nodes"]) == TARGET)
    p0 = next(row for row in aggregate if int(row["placement"]) == 0)
    p1 = next(row for row in aggregate if int(row["placement"]) == 1)
    p2 = next(row for row in aggregate if int(row["placement"]) == 2)

    if min(
        safe_float(p0["early_fragment_lock_rate"]),
        safe_float(p1["early_fragment_lock_rate"]),
        safe_float(p2["early_fragment_lock_rate"]),
    ) >= 0.50:
        status = "fragmentation_is_usually_early_lock"
        note = "Shell-fragmenteringen ser oftest ut til a starte tidlig i halevinduet og deretter holde seg som en lokal lock med minoritetsavvik."
        next_step = "inspect_minor_exceptions"
        next_note = "Neste steg bor forklare minoritetsavvikene, spesielt forsinket onset i `p1` og connected-resistance-caset i `p2`."
    elif max(
        safe_float(p0["intermittent_fragment_churn_rate"]),
        safe_float(p1["intermittent_fragment_churn_rate"]),
        safe_float(p2["intermittent_fragment_churn_rate"]),
    ) >= 0.50:
        status = "fragmentation_is_churn_dominated"
        note = "Fragmenteringen ser ikke ut til a lase tidlig; den ser heller ut som vedvarende lokal churn gjennom halevinduet."
        next_step = "localize_switch_clusters"
        next_note = "Neste steg bor lokalisere hvilke smale tidspunkter som driver de mange switchene."
    else:
        status = "fragment_timing_still_mixed"
        note = "Fragment-timing-observabelen gjor shell-signalet mer konkret, men ikke rent nok til en enkel tidlig-lock- eller churn-lesning ennå."
        next_step = "stay_fragment_local"
        next_note = "Neste steg bor vaere en enda mindre lokal hendelsesrunde i samme halevindu."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if size_clean else "unclear",
            "note": (
                "Startstorrelsene er fortsatt rent separert; denne runden bruker bare de ekte v15ae-snapshottene og legger ikke inn ny simulasjonsstoy."
                if size_clean
                else "Storrelsesseparasjonen er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "fragment_timing_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(*, target_summary: Sequence[Mapping[str, str]], aggregate: Sequence[Mapping[str, Any]], diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15af: add_chord shell fragment event lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden kjorer ingen nye simuleringer. Den bruker de ekte `v15ae`-snapshottene for a lokalisere nar shell-fragmentering starter og om den holder tidlig eller kommer senere gjennom mindre lokale hendelser.")
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
    lines.append("## Fragment timing summary")
    lines.append("")
    lines.append("| placement | n | early lock | delayed lock | intermittent churn | connected resistance | mean first frag step | mean prefix steps | mean suffix frag | mean switches |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['placement'])} | {int(row['n_runs'])} | {fmt(row['early_fragment_lock_rate'])} | {fmt(row['delayed_fragment_lock_rate'])} | {fmt(row['intermittent_fragment_churn_rate'])} | {fmt(row['connected_resistance_churn_rate'])} | {fmt(row['mean_first_fragment_step'],1)} | {fmt(row['mean_connected_prefix_steps'],1)} | {fmt(row['mean_fragmented_suffix_rate'])} | {fmt(row['mean_state_switch_count'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ren analyse av `v15ae`-snapshottene, ikke en ny bred defect-run.")
    lines.append("- Les dette som timing i shell-fragmenteringen, ikke som en ny generell defect-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15af add_chord shell fragment event lab.")
    p.add_argument("--snapshots-in", type=str, default=str(IN_SNAPSHOTS))
    p.add_argument("--runs-in", type=str, default=str(IN_RUNS))
    p.add_argument("--target-in", type=str, default=str(IN_TARGET))
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15af_add_chord_shell_fragment_runs.csv")
    p.add_argument("--out-segments-csv", type=str, default="Documentation/v15af_add_chord_shell_fragment_segments.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15af_add_chord_shell_fragment_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15af_add_chord_shell_fragment_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15af_add_chord_shell_fragment_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15af_add_chord_shell_fragment_event_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15af_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15af.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    snapshot_rows_in = read_csv(args.snapshots_in)
    run_rows_in = read_csv(args.runs_in)
    target_summary = read_csv(args.target_in)
    run_rows_out, segment_rows_out = run_analysis(snapshot_rows_in=snapshot_rows_in, run_rows_in=run_rows_in)
    aggregate = aggregate_rows(run_rows_out)
    diagnosis = diagnosis_rows(target_summary, aggregate)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15af operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en timing-analyse av shell-fragmentering i de eksisterende v15ae-snapshottene, ikke som en ny bred simulasjonsrunde.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15af",
            "",
            "Etter at vi fant at randen ofte er oppdelt i flere biter, ser denne runden pa nar det skjer: er randen oppdelt nesten med en gang i senfasen, eller deler den seg senere?",
            "",
            "Vi bruker derfor de samme snapshottene som forrige runde og markerer nar shellen gar fra en samlet form til flere biter.",
        ]
    ) + "\n"
    write_csv(args.out_runs_csv, run_rows_out)
    write_csv(args.out_segments_csv, segment_rows_out)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_target_csv, [dict(row) for row in target_summary])
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
