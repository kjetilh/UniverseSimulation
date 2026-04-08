#!/usr/bin/env python3
"""v0.15ai early-lock band lab for add_chord recurrence band.

This round follows v15ah. The shell-fragmentation exceptions did not hold as
nearby local families, which sharpened the main live reading:

- the robust live family is still `early_fragment_lock`
- the right next move is a new observable inside that main family

The narrow question here is:

does `early_fragment_lock` remain too diffuse even inside the main family, or
does it collapse into a few coarse fragment-load bands (`low`, `mid`, `high`)
that are more stable than exact shell-component counts?
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15af_add_chord_shell_fragment_event_lab as v15af
import relational_universe_v15ah_shell_exception_holdout as v15ah
import relational_universe_v15q_single_defect_recurrence_lab as v15q


DOC = Path("Documentation")
IN_AE_RUNS = DOC / "v15ae_add_chord_shell_topology_runs.csv"
IN_AE_SNAPSHOTS = DOC / "v15ae_add_chord_shell_topology_snapshots.csv"
IN_AF_RUNS = DOC / "v15af_add_chord_shell_fragment_runs.csv"
IN_AH_RUNS = DOC / "v15ah_shell_exception_holdout_runs.csv"

TARGET = 48
GROWTH_SEED = 202
FULL_STEPS = 2560
LOG_EVERY = 8

BAND_ORDER = {"low": 0, "mid": 1, "high": 2}
SOURCE_ORDER = {"anchor_main_family": 0, "holdout_revert": 1, "combined": 2}


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


def band_label(component_count: int) -> str:
    if component_count <= 0:
        return "inactive"
    if component_count <= 3:
        return "low"
    if component_count <= 6:
        return "mid"
    return "high"


def top_share(counter: Counter[Any], *, tie_order: Dict[Any, int] | None = None) -> Tuple[Any, float, float]:
    total = max(1, sum(counter.values()))
    if not counter:
        return None, float("nan"), float("nan")

    def sort_key(item: Tuple[Any, int]) -> Tuple[int, int]:
        label, count = item
        if tie_order is not None and label in tie_order:
            tie = tie_order[label]
        else:
            try:
                tie = int(label)
            except Exception:
                tie = 999999
        return (-count, tie)

    ordered = sorted(counter.items(), key=sort_key)
    dominant_label, dominant_count = ordered[0]
    top2 = sum(count for _, count in ordered[:2])
    return dominant_label, dominant_count / total, top2 / total


def switch_count(labels: Sequence[Any]) -> int:
    return sum(1 for a, b in zip(labels, labels[1:]) if a != b)


def classify_band_lock(dominant_band: str, dominant_band_share: float, top2_band_share: float) -> str:
    if dominant_band not in BAND_ORDER:
        return "inactive_band"
    if dominant_band_share >= 0.60:
        return f"{dominant_band}_band_lock"
    if top2_band_share >= 0.85:
        return "two_band_drift"
    return "band_drift_lock"


def normalize_snapshot_row(
    row: Mapping[str, Any],
    *,
    source_group: str,
    anchor_seed_delta: int,
    holdout_seed_delta: int,
    family_tag: str,
) -> Dict[str, Any]:
    comp_count = int(row["shell_component_count"])
    return {
        "source_group": source_group,
        "family_tag": family_tag,
        "placement": int(row["placement"]),
        "anchor_seed_delta": int(anchor_seed_delta),
        "holdout_seed_delta": int(holdout_seed_delta),
        "seed_delta": int(row["seed_delta"]),
        "run_seed": int(row["run_seed"]),
        "support_signature": str(row["support_signature"]),
        "snapshot_index": int(row["snapshot_index"]),
        "step": int(row["step"]),
        "shell_active_nodes": int(row["shell_active_nodes"]),
        "shell_component_count": comp_count,
        "shell_count_band": band_label(comp_count),
        "largest_shell_component_fraction": safe_float(row["largest_shell_component_fraction"]),
        "shell_beta1": int(row["shell_beta1"]),
        "shell_attachment_edges_to_core": int(row["shell_attachment_edges_to_core"]),
        "shell_attachment_node_frac": safe_float(row["shell_attachment_node_frac"]),
        "shell_boundary_to_volume": safe_float(row["shell_boundary_to_volume"]),
    }


def analyze_run(
    *,
    source_group: str,
    family_tag: str,
    placement: int,
    anchor_seed_delta: int,
    holdout_seed_delta: int,
    run_seed: int,
    support_signature: str,
    requested_match: int,
    full_label: str,
    full_exact_return_rate: float,
    shell_nodes: int,
    active_snapshots: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    component_counts = [int(row["shell_component_count"]) for row in active_snapshots]
    band_counts = [str(row["shell_count_band"]) for row in active_snapshots]
    exact_counter = Counter(component_counts)
    band_counter = Counter(band_counts)
    dominant_exact_count, dominant_exact_share, top2_exact_share = top_share(exact_counter)
    dominant_band, dominant_band_share, top2_band_share = top_share(band_counter, tie_order=BAND_ORDER)
    band_lock_label = classify_band_lock(str(dominant_band), safe_float(dominant_band_share), safe_float(top2_band_share))
    shell_nodes_series = [safe_float(row["shell_active_nodes"]) for row in active_snapshots]
    attach_fracs = [safe_float(row["shell_attachment_node_frac"]) for row in active_snapshots if math.isfinite(safe_float(row["shell_attachment_node_frac"]))]
    boundary_vals = [safe_float(row["shell_boundary_to_volume"]) for row in active_snapshots if math.isfinite(safe_float(row["shell_boundary_to_volume"]))]

    return {
        "source_group": source_group,
        "family_tag": family_tag,
        "placement": int(placement),
        "anchor_seed_delta": int(anchor_seed_delta),
        "holdout_seed_delta": int(holdout_seed_delta),
        "run_seed": int(run_seed),
        "requested_match": int(requested_match),
        "support_signature": support_signature,
        "full_label": full_label,
        "full_exact_return_rate": float(full_exact_return_rate),
        "shell_nodes": int(shell_nodes),
        "tail_active_shell_snapshots": int(len(active_snapshots)),
        "mean_shell_component_count": mean_defined(component_counts),
        "q90_shell_component_count": quantile(component_counts, 0.90) if component_counts else float("nan"),
        "dominant_exact_count": int(dominant_exact_count) if dominant_exact_count is not None else -1,
        "dominant_exact_share": float(dominant_exact_share),
        "top2_exact_share": float(top2_exact_share),
        "dominant_band": str(dominant_band),
        "dominant_band_share": float(dominant_band_share),
        "top2_band_share": float(top2_band_share),
        "band_minus_exact_share": float(safe_float(dominant_band_share) - safe_float(dominant_exact_share)),
        "exact_switch_count": int(switch_count(component_counts)),
        "band_switch_count": int(switch_count(band_counts)),
        "mean_shell_active_nodes": mean_defined(shell_nodes_series),
        "mean_attachment_node_frac": mean_defined(attach_fracs),
        "mean_shell_boundary_to_volume": mean_defined(boundary_vals),
        "band_lock_label": band_lock_label,
    }


def collect_anchor_rows(
    *,
    ae_runs_in: Sequence[Mapping[str, str]],
    ae_snapshots_in: Sequence[Mapping[str, str]],
    af_runs_in: Sequence[Mapping[str, str]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    ae_run_lookup = {
        (int(row["placement"]), int(row["seed_delta"])): dict(row)
        for row in ae_runs_in
    }
    snapshot_lookup: Dict[Tuple[int, int], List[Dict[str, str]]] = defaultdict(list)
    for row in ae_snapshots_in:
        key = (int(row["placement"]), int(row["seed_delta"]))
        snapshot_lookup[key].append(dict(row))

    run_rows: List[Dict[str, Any]] = []
    snapshot_rows: List[Dict[str, Any]] = []
    for timing_row in af_runs_in:
        if str(timing_row["timing_label"]) != "early_fragment_lock":
            continue
        placement = int(timing_row["placement"])
        seed_delta = int(timing_row["seed_delta"])
        key = (placement, seed_delta)
        ae = ae_run_lookup[key]
        raw_snapshots = sorted(snapshot_lookup[key], key=lambda row: int(row["step"]))
        active_snapshots = [
            normalize_snapshot_row(
                row,
                source_group="anchor_main_family",
                anchor_seed_delta=seed_delta,
                holdout_seed_delta=-1,
                family_tag="early_fragment_lock",
            )
            for row in raw_snapshots
            if int(row["shell_active_nodes"]) > 0
        ]
        snapshot_rows.extend(active_snapshots)
        run_rows.append(
            analyze_run(
                source_group="anchor_main_family",
                family_tag="early_fragment_lock",
                placement=placement,
                anchor_seed_delta=seed_delta,
                holdout_seed_delta=-1,
                run_seed=int(ae["run_seed"]),
                support_signature=str(ae["support_signature"]),
                requested_match=int(ae["requested_match"]),
                full_label=str(ae["full_label"]),
                full_exact_return_rate=safe_float(ae["full_exact_return_rate"]),
                shell_nodes=int(ae["shell_nodes"]),
                active_snapshots=active_snapshots,
            )
        )
    return run_rows, snapshot_rows


def rerun_holdout_row(
    *,
    base_state: Any,
    row: Mapping[str, str],
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    placement = int(row["placement"])
    holdout_seed_delta = int(row["holdout_seed_delta"])
    anchor_seed_delta = int(row["anchor_seed_delta"])
    run_seed = int(row["run_seed"])
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
    active_snapshots = [
        normalize_snapshot_row(
            snap,
            source_group="holdout_revert",
            anchor_seed_delta=anchor_seed_delta,
            holdout_seed_delta=holdout_seed_delta,
            family_tag="early_fragment_lock",
        )
        for snap in snap_rows
        if int(snap["shell_active_nodes"]) > 0
    ]
    run_row = analyze_run(
        source_group="holdout_revert",
        family_tag="early_fragment_lock",
        placement=placement,
        anchor_seed_delta=anchor_seed_delta,
        holdout_seed_delta=holdout_seed_delta,
        run_seed=run_seed,
        support_signature=support_signature,
        requested_match=int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
        full_label=full_label,
        full_exact_return_rate=safe_float(recurrence["exact_return_rate"]),
        shell_nodes=int(len(partition["shell_nodes"])),
        active_snapshots=active_snapshots,
    )
    return run_row, active_snapshots


def collect_holdout_rows(
    *,
    base_state: Any,
    ah_runs_in: Sequence[Mapping[str, str]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    run_rows: List[Dict[str, Any]] = []
    snapshot_rows: List[Dict[str, Any]] = []
    for row in ah_runs_in:
        if str(row["holdout_outcome_label"]) != "reverts_to_main_family":
            continue
        if str(row["timing_label"]) != "early_fragment_lock":
            continue
        run_row, active_snapshots = rerun_holdout_row(base_state=base_state, row=row)
        run_rows.append(run_row)
        snapshot_rows.extend(active_snapshots)
    return run_rows, snapshot_rows


def aggregate_group_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    def summarize(group_type: str, group_value: str, group_rows: Sequence[Mapping[str, Any]]) -> None:
        if not group_rows:
            return
        band_labels = [str(row["band_lock_label"]) for row in group_rows]
        dominant_band_counts = Counter(str(row["dominant_band"]) for row in group_rows)
        dominant_band_mode = max(
            dominant_band_counts.items(),
            key=lambda item: (item[1], -BAND_ORDER.get(item[0], 999)),
        )[0]
        out.append(
            {
                "group_type": group_type,
                "group_value": group_value,
                "n_runs": len(group_rows),
                "band_lock_rate": mean_defined(1.0 if label.endswith("_band_lock") else 0.0 for label in band_labels),
                "low_band_lock_rate": mean_defined(1.0 if label == "low_band_lock" else 0.0 for label in band_labels),
                "mid_band_lock_rate": mean_defined(1.0 if label == "mid_band_lock" else 0.0 for label in band_labels),
                "high_band_lock_rate": mean_defined(1.0 if label == "high_band_lock" else 0.0 for label in band_labels),
                "two_band_drift_rate": mean_defined(1.0 if label == "two_band_drift" else 0.0 for label in band_labels),
                "band_drift_rate": mean_defined(1.0 if label == "band_drift_lock" else 0.0 for label in band_labels),
                "structured_band_rate": mean_defined(
                    1.0 if (label.endswith("_band_lock") or label == "two_band_drift") else 0.0
                    for label in band_labels
                ),
                "dominant_band_mode": dominant_band_mode,
                "mean_dominant_band_share": mean_defined(safe_float(row["dominant_band_share"]) for row in group_rows),
                "mean_top2_band_share": mean_defined(safe_float(row["top2_band_share"]) for row in group_rows),
                "mean_dominant_exact_share": mean_defined(safe_float(row["dominant_exact_share"]) for row in group_rows),
                "mean_top2_exact_share": mean_defined(safe_float(row["top2_exact_share"]) for row in group_rows),
                "mean_band_minus_exact_share": mean_defined(safe_float(row["band_minus_exact_share"]) for row in group_rows),
                "mean_band_switch_count": mean_defined(safe_float(row["band_switch_count"]) for row in group_rows),
                "mean_exact_switch_count": mean_defined(safe_float(row["exact_switch_count"]) for row in group_rows),
                "mean_shell_component_count": mean_defined(safe_float(row["mean_shell_component_count"]) for row in group_rows),
                "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in group_rows),
            }
        )

    for source_group in ("anchor_main_family", "holdout_revert"):
        summarize("source_group", source_group, [row for row in rows if str(row["source_group"]) == source_group])
    summarize("source_group", "combined", rows)
    for placement in sorted({int(row["placement"]) for row in rows}):
        summarize("placement", str(placement), [row for row in rows if int(row["placement"]) == placement])
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate_rows_in: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary if int(row["target_nodes"]) == TARGET)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    agg_lookup = {(str(row["group_type"]), str(row["group_value"])): row for row in aggregate_rows_in}
    combined = agg_lookup[("source_group", "combined")]
    anchors = agg_lookup[("source_group", "anchor_main_family")]
    holdouts = agg_lookup[("source_group", "holdout_revert")]
    combined_band_lock = safe_float(combined["band_lock_rate"])
    holdout_band_lock = safe_float(holdouts["band_lock_rate"])
    combined_structured = safe_float(combined["structured_band_rate"])
    holdout_structured = safe_float(holdouts["structured_band_rate"])
    uplift = safe_float(combined["mean_band_minus_exact_share"])

    if combined_structured >= 0.85 and holdout_structured >= 0.80 and uplift >= 0.10:
        status = "early_lock_has_structured_band_ladder"
        note = "Hovedfamilien er mye bedre lest som coarse low/mid/high-band med litt naboband-drift enn som ett eksakt shell-komponenttall, og dette holder ogsa pa holdout-run som falt tilbake til hovedfamilien."
        next_step = "probe_band_onset_and_switching"
        next_note = "Neste steg bor forklare nar run larser seg inn i low, mid eller high band, og hvilke run som bare driver mellom to naboband."
    elif combined_band_lock >= 0.60 and uplift >= 0.08:
        status = "coarse_band_signal_partly_supported"
        note = "Coarse load-band gjor hovedfamilien skarpere enn eksakt telling, men bandene er fortsatt ikke rene nok til en sterk subfamilie-lesning."
        next_step = "tighten_band_observable"
        next_note = "Neste steg bor se pa en litt rikere band-observabel, for eksempel band-onset eller band-skiftefrekvens."
    else:
        status = "band_observable_still_diffuse"
        note = "Selv coarse low/mid/high-band gjor ikke early-lock-familien mye skarpere enn eksakt komponenttelling."
        next_step = "pivot_observable_again"
        next_note = "Neste steg bor bytte til en annen observabel inne i hovedfamilien."

    anchor_mode = str(anchors["dominant_band_mode"])
    holdout_mode = str(holdouts["dominant_band_mode"])
    mode_note = (
        f"Ankerrun domineres mest av `{anchor_mode}`, mens holdout-revert-rundene domineres mest av `{holdout_mode}`."
    )
    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsen er rent separert og alle run i denne runden matcher onsket add_chord-perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "coarse_band_status",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "band_mode_note",
            "status": "descriptive",
            "note": mode_note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    aggregate_rows_in: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    source_rows = [row for row in aggregate_rows_in if str(row["group_type"]) == "source_group"]
    placement_rows = [row for row in aggregate_rows_in if str(row["group_type"]) == "placement"]
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15ai: early-lock band lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester en ny observabel inne i den robuste `early_fragment_lock`-familien: om hale-fragmenteringen er bedre beskrevet av coarse `low/mid/high` fragment-load-band enn av ett eksakt shell-komponenttall.")
    lines.append("")
    lines.append("## Oppsett")
    lines.append("")
    lines.append("- behold samme lokale `t48_g202` add_chord-band")
    lines.append("- behold bare run som faktisk ligger i hovedfamilien `early_fragment_lock`")
    lines.append("- bruk ankerrun fra `v15ae-v15af` og holdout-run fra `v15ah` som falt tilbake til hovedfamilien")
    lines.append("- bruk coarse band `low = 1..3`, `mid = 4..6`, `high = 7+`")
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
    lines.append("## Kildegrupper")
    lines.append("")
    lines.append("| group | n | structured | band lock | low | mid | high | band drift | band share | exact share | uplift |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(source_rows, key=lambda r: SOURCE_ORDER.get(str(r["group_value"]), 99)):
        lines.append(
            f"| {row['group_value']} | {int(row['n_runs'])} | {fmt(row['structured_band_rate'])} | {fmt(row['band_lock_rate'])} | {fmt(row['low_band_lock_rate'])} | {fmt(row['mid_band_lock_rate'])} | {fmt(row['high_band_lock_rate'])} | {fmt(row['band_drift_rate'])} | {fmt(row['mean_dominant_band_share'])} | {fmt(row['mean_dominant_exact_share'])} | {fmt(row['mean_band_minus_exact_share'])} |"
        )
    lines.append("")
    lines.append("## Per placement")
    lines.append("")
    lines.append("| placement | n | mode | low | mid | high | band share | exact share | band drift |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in sorted(placement_rows, key=lambda r: int(r["group_value"])):
        lines.append(
            f"| {int(row['group_value'])} | {int(row['n_runs'])} | {row['dominant_band_mode']} | {fmt(row['low_band_lock_rate'])} | {fmt(row['mid_band_lock_rate'])} | {fmt(row['high_band_lock_rate'])} | {fmt(row['mean_dominant_band_share'])} | {fmt(row['mean_dominant_exact_share'])} | {fmt(row['band_drift_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt ikke en ny defect-art eller en lov; det er en smal observabeltest inne i den robuste hovedfamilien.")
    lines.append("- Hvis coarse band slar eksakt telling, betyr det at hovedfamilien er bedre lest som fragment-load-band enn som ett skarpt shell-komponenttall.")
    lines.append("- Hvis coarse band fortsatt er diffust, betyr det at neste steg bor bytte observabel igjen, ikke presse samme aksen hardere.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ai early-lock band lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15ai_early_lock_band_runs.csv")
    p.add_argument("--out-snapshots-csv", type=str, default="Documentation/v15ai_early_lock_band_snapshots.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ai_early_lock_band_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ai_early_lock_band_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15ai_early_lock_band_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ai_early_lock_band_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ai_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ai.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    ae_runs = read_csv(IN_AE_RUNS)
    ae_snapshots = read_csv(IN_AE_SNAPSHOTS)
    af_runs = read_csv(IN_AF_RUNS)
    ah_runs = read_csv(IN_AH_RUNS)

    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]

    anchor_runs, anchor_snapshots = collect_anchor_rows(
        ae_runs_in=ae_runs,
        ae_snapshots_in=ae_snapshots,
        af_runs_in=af_runs,
    )
    holdout_runs, holdout_snapshots = collect_holdout_rows(
        base_state=base_state,
        ah_runs_in=ah_runs,
    )

    run_rows = sorted(
        anchor_runs + holdout_runs,
        key=lambda row: (
            SOURCE_ORDER.get(str(row["source_group"]), 99),
            int(row["placement"]),
            int(row["run_seed"]),
        ),
    )
    snapshot_rows = sorted(
        anchor_snapshots + holdout_snapshots,
        key=lambda row: (
            SOURCE_ORDER.get(str(row["source_group"]), 99),
            int(row["placement"]),
            int(row["run_seed"]),
            int(row["step"]),
        ),
    )
    aggregate = aggregate_group_rows(run_rows)
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        aggregate_rows_in=aggregate,
    )
    report_md = build_report(
        target_summary=target_summary,
        aggregate_rows_in=aggregate,
        diagnosis=diagnosis,
    )
    op_md = "\n".join(
        [
            "# v0.15ai operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en observabeltest inne i `early_fragment_lock`, ikke som en ny defect-familie-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15ai",
            "",
            "Etter at shell-unntakene viste seg a vaere lokale avvik, tester denne runden om hovedfamilien selv skjuler en enklere struktur.",
            "",
            "I stedet for a telle eksakt hvor mange shell-biter som finnes i hvert oyeblikk, deler vi dem inn i grove belastningsband: lavt, middels eller hoyt antall fragmenter.",
            "",
            "Målet er a se om hovedfamilien er mer stabil pa dette grovere nivaet enn den ser ut til a vaere ved helt eksakt telling.",
        ]
    ) + "\n"

    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_snapshots_csv, snapshot_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
