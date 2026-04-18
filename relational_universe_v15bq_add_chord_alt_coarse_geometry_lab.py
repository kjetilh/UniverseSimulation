#!/usr/bin/env python3
"""v0.15bq add_chord alternative coarse-geometry lab.

Follow-up to v15bn-v15bp.

Question:
if the simple share-based coarse geometry fails to transfer 48/p2 -> 96/p3,
does a richer shell-dynamics / shell-topology coarse geometry do any better?
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15ad_add_chord_boundary_shell_lab as v15ad
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15q_single_defect_recurrence_lab as v15q


GROWTH_SEED = 202
SEED_DELTAS = (331, 359, 389, 419, 449, 479)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY
ALT_COARSE_KEYS = [
    "mean_shell_refresh",
    "mean_burst_rate",
    "mean_shell_cover",
    "mean_boundary_sd",
    "mean_shell_connected_rate",
    "mean_shell_fragmented_rate",
    "mean_shell_loop_rate",
    "mean_largest_shell_component_fraction",
    "mean_attachment_node_frac",
]
PROFILES = (
    {"profile_label": "anchor_48_p2", "role": "anchor", "target_nodes": 48, "placement": 2},
    {"profile_label": "candidate_96_p3", "role": "candidate", "target_nodes": 96, "placement": 3},
    {"profile_label": "control_96_p1", "role": "control", "target_nodes": 96, "placement": 1},
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


def aggregate_profile(rows: Sequence[Mapping[str, Any]], profile: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "profile_label": str(profile["profile_label"]),
        "role": str(profile["role"]),
        "target_nodes": int(profile["target_nodes"]),
        "placement": int(profile["placement"]),
        "n_runs": len(rows),
        "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in rows),
        "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in rows),
        "mean_shell_refresh": mean_defined(safe_float(row["mean_shell_refresh"]) for row in rows),
        "mean_burst_rate": mean_defined(safe_float(row["burst_rate"]) for row in rows),
        "mean_shell_cover": mean_defined(safe_float(row["mean_shell_cover"]) for row in rows),
        "mean_boundary_sd": mean_defined(safe_float(row["sd_boundary_to_volume"]) for row in rows),
        "mean_shell_connected_rate": mean_defined(safe_float(row["shell_connected_rate"]) for row in rows),
        "mean_shell_fragmented_rate": mean_defined(safe_float(row["shell_fragmented_rate"]) for row in rows),
        "mean_shell_loop_rate": mean_defined(safe_float(row["shell_loop_rate"]) for row in rows),
        "mean_largest_shell_component_fraction": mean_defined(
            safe_float(row["mean_largest_shell_component_fraction"]) for row in rows
        ),
        "mean_attachment_node_frac": mean_defined(safe_float(row["mean_attachment_node_frac"]) for row in rows),
        "mean_core_share_of_union": mean_defined(safe_float(row["core_share_of_union"]) for row in rows),
        "mean_shell_share_of_union": mean_defined(safe_float(row["shell_share_of_union"]) for row in rows),
        "mean_rare_share_of_union": mean_defined(safe_float(row["rare_share_of_union"]) for row in rows),
    }


def comparison_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    agg_map = {str(row["profile_label"]): dict(row) for row in aggregate}
    anchor = agg_map["anchor_48_p2"]
    out: List[Dict[str, Any]] = []
    for key in ("candidate_96_p3", "control_96_p1"):
        other = agg_map[key]
        alt_distance = sum(abs(safe_float(other[name]) - safe_float(anchor[name])) for name in ALT_COARSE_KEYS)
        share_distance = (
            abs(safe_float(other["mean_core_share_of_union"]) - safe_float(anchor["mean_core_share_of_union"]))
            + abs(safe_float(other["mean_shell_share_of_union"]) - safe_float(anchor["mean_shell_share_of_union"]))
            + abs(safe_float(other["mean_rare_share_of_union"]) - safe_float(anchor["mean_rare_share_of_union"]))
        )
        out.append(
            {
                "anchor_profile": "anchor_48_p2",
                "other_profile": key,
                "other_role": str(other["role"]),
                "alt_coarse_distance": alt_distance,
                "share_distance": share_distance,
                "mean_shell_refresh": safe_float(other["mean_shell_refresh"]),
                "mean_shell_connected_rate": safe_float(other["mean_shell_connected_rate"]),
                "mean_shell_fragmented_rate": safe_float(other["mean_shell_fragmented_rate"]),
                "mean_attachment_node_frac": safe_float(other["mean_attachment_node_frac"]),
            }
        )
    out.sort(key=lambda row: safe_float(row["alt_coarse_distance"]))
    for idx, row in enumerate(out, start=1):
        row["alt_rank"] = idx
    return out


def diagnosis_rows(target_summary: Sequence[Mapping[str, Any]], rows: Sequence[Mapping[str, Any]], comparisons: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    candidate = next(row for row in comparisons if str(row["other_profile"]) == "candidate_96_p3")
    control = next(row for row in comparisons if str(row["other_profile"]) == "control_96_p1")
    alt_gap = safe_float(control["alt_coarse_distance"]) - safe_float(candidate["alt_coarse_distance"])
    share_gap = safe_float(control["share_distance"]) - safe_float(candidate["share_distance"])

    if alt_gap >= 0.08:
        status = "alt_coarse_bridge_supported"
        note = (
            f"96/p3 ligger naermere 48/p2 enn 96/p1 pa shell-dynamikk/topologi med gap {fmt(alt_gap)}, "
            f"selv om share-gapet bare er {fmt(share_gap)}."
        )
        next_step = "holdout_alt_geometry_claim"
        next_note = "Neste steg kan bruke denne alternative coarse-geometrien som den riktige add_chord-skalaobservabelen."
    elif alt_gap > 0.0:
        status = "alt_coarse_bridge_weak"
        note = (
            f"96/p3 slar sa vidt 96/p1 pa alternativ coarse-geometri med gap {fmt(alt_gap)}, men ikke nok til en ren ny claim."
        )
        next_step = "explain_alt_bridge"
        next_note = "Neste steg bor forklare hva i shell-geometrien som gir denne svake fordelen."
    else:
        status = "alt_coarse_bridge_not_yet"
        note = (
            f"96/p3 er ikke naermere 48/p2 enn 96/p1 pa shell-dynamikk/topologi; alt-gapet er {fmt(alt_gap)}."
        )
        next_step = "pivot_observable_or_carrier"
        next_note = "Neste steg bor ga til en ny observabel eller et annet carrier-spor, ikke presse videre pa samme add_chord-skalaovergang."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsene er rent separert og alle add_chord-runs matcher onsket perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "alt_coarse_bridge",
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
    target_summary: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    comparisons: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15bq: add_chord alternative coarse geometry lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester om shell-dynamikk og shell-topologi gir en bedre liten scale-transfer-lesning for add_chord enn de enkle core/shell/rare-share-maalene.")
    lines.append("")
    lines.append("## Startstorrelser")
    lines.append("")
    lines.append("| target | mean initial | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Aggregate profiler")
    lines.append("")
    lines.append("| profile | role | exact | coarse | refresh | burst | shell cover | connected | fragmented | loop | attach frac |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {row['role']} | {fmt(row['mean_full_exact_return_rate'])} | {fmt(row['mean_full_coarse_return_rate'])} | {fmt(row['mean_shell_refresh'])} | {fmt(row['mean_burst_rate'])} | {fmt(row['mean_shell_cover'])} | {fmt(row['mean_shell_connected_rate'])} | {fmt(row['mean_shell_fragmented_rate'])} | {fmt(row['mean_shell_loop_rate'])} | {fmt(row['mean_attachment_node_frac'])} |"
        )
    lines.append("")
    lines.append("## Anker-sammenlikning")
    lines.append("")
    lines.append("| other profile | role | alt coarse distance | share distance | shell refresh | connected | fragmented | attach frac | alt rank |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in comparisons:
        lines.append(
            f"| {row['other_profile']} | {row['other_role']} | {fmt(row['alt_coarse_distance'])} | {fmt(row['share_distance'])} | {fmt(row['mean_shell_refresh'])} | {fmt(row['mean_shell_connected_rate'])} | {fmt(row['mean_shell_fragmented_rate'])} | {fmt(row['mean_attachment_node_frac'])} | {int(row['alt_rank'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en alternativ coarse-geometri-test av samme smale add_chord-skalahypotese.")
    lines.append("- Positivt signal her betyr bare at shell-dynamikk/topologi er en bedre coarse observabel enn share-pakken, ikke at scale-transfer er generelt lost.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15bq add_chord alternative coarse geometry lab.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15bq_add_chord_alt_coarse_geometry_target_summary.csv")
    p.add_argument("--out-rows-csv", type=str, default="Documentation/v15bq_add_chord_alt_coarse_geometry_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15bq_add_chord_alt_coarse_geometry_aggregate.csv")
    p.add_argument("--out-comparison-csv", type=str, default="Documentation/v15bq_add_chord_alt_coarse_geometry_comparison.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15bq_add_chord_alt_coarse_geometry_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15bq_add_chord_alt_coarse_geometry_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15bq_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15bq.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    targets = sorted({int(profile["target_nodes"]) for profile in PROFILES})
    ensembles = v15.deep_ensembles(targets)
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    ensemble_by_target = {int(ens.target_nodes): ens for ens in ensembles}
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    rows: List[Dict[str, Any]] = []

    for profile in PROFILES:
        target = int(profile["target_nodes"])
        placement = int(profile["placement"])
        ens = ensemble_by_target[target]
        base_state = base_states[(ens.name, GROWTH_SEED)]
        for seed_delta in SEED_DELTAS:
            run_seed = target * 100000 + GROWTH_SEED * 1000 + placement * 100 + int(seed_delta)
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
            recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
            info = dict(res["perturbation_info"])
            support = list(info.get("support", []))
            core_shell = v15ac.core_shell_metrics(res["damaged_sets"], support)
            shell = v15ad.shell_metrics(res["log_rows"], res["damaged_sets"])
            partition = v15ae.occupancy_partition(res["damaged_sets"])
            snap_rows = v15ae.shell_snapshot_rows(
                placement=placement,
                seed_delta=seed_delta,
                run_seed=run_seed,
                support_signature=",".join(str(x) for x in support),
                core_nodes=set(partition["core_nodes"]),
                shell_nodes=set(partition["shell_nodes"]),
                log_rows=res["log_rows"],
                damaged_sets=res["damaged_sets"],
                control_graphs=res["control_graphs"],
            )
            active_rows = [row for row in snap_rows if int(row["shell_active_nodes"]) > 0]
            rows.append(
                {
                    "profile_label": str(profile["profile_label"]),
                    "role": str(profile["role"]),
                    "target_nodes": target,
                    "growth_seed": GROWTH_SEED,
                    "placement": placement,
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
                    "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                    "core_share_of_union": safe_float(core_shell["core_share_of_union"]),
                    "shell_share_of_union": safe_float(core_shell["shell_share_of_union"]),
                    "rare_share_of_union": safe_float(core_shell["rare_share_of_union"]),
                    "mean_shell_refresh": safe_float(shell["mean_shell_refresh"]),
                    "burst_rate": safe_float(shell["burst_rate"]),
                    "mean_shell_cover": safe_float(shell["mean_shell_cover"]),
                    "sd_boundary_to_volume": safe_float(shell["sd_boundary_to_volume"]),
                    "shell_connected_rate": mean_defined(float(row["shell_connected_active"]) for row in active_rows) if active_rows else float("nan"),
                    "shell_fragmented_rate": mean_defined(float(row["shell_fragmented_active"]) for row in active_rows) if active_rows else float("nan"),
                    "shell_loop_rate": mean_defined(float(row["shell_loop_present"]) for row in active_rows) if active_rows else float("nan"),
                    "mean_largest_shell_component_fraction": mean_defined(
                        safe_float(row["largest_shell_component_fraction"]) for row in active_rows
                    ),
                    "mean_attachment_node_frac": mean_defined(
                        safe_float(row["shell_attachment_node_frac"])
                        for row in active_rows
                        if math.isfinite(safe_float(row["shell_attachment_node_frac"]))
                    ),
                }
            )

    aggregate = [aggregate_profile([row for row in rows if str(row["profile_label"]) == str(profile["profile_label"])], profile) for profile in PROFILES]
    aggregate.sort(key=lambda row: ("anchor" not in str(row["role"]), int(row["target_nodes"]), int(row["placement"])))
    comparisons = comparison_rows(aggregate)
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) in targets]
    diagnosis = diagnosis_rows(target_summary, rows, comparisons)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, comparisons=comparisons, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15bq operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en alternativ coarse-geometri-test av samme smale add_chord-skalahypotese, ikke som en bred ny transfer-claim.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15bq",
            "",
            "Denne runden sjekker om den beste 96-kandidaten ligner 48-familien bedre hvis vi ser pa hvordan randen flimrer og henger sammen, ikke bare hvor stor kjernen og randen er.",
            "",
            "Kort sagt: kanskje den riktige grove formen sitter i randdynamikken, ikke i enkle andeler.",
        ]
    ) + "\n"
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_rows_csv, rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_comparison_csv, comparisons)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
