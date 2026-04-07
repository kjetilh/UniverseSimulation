#!/usr/bin/env python3
"""v0.15ae add_chord shell topology lab.

This round follows v15ac-v15ad. The local add_chord recurrence band now looks
best explained as:

- a stable damaged core
- a calm, incrementally varying shell

The next narrow question is therefore topological rather than periodic:

does the shell usually remain one connected band around the core, does it
fragment into multiple pieces, or does it often carry nontrivial local cycle
rank while still staying coherent?
"""
from __future__ import annotations

import argparse
import math
import random
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Set

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 48
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2)
SEED_DELTAS = (151, 179, 211, 239, 271, 307)
FULL_STEPS = 2560
LOG_EVERY = 8
CORE_THRESHOLD = 0.80
SHELL_THRESHOLD = 0.20


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


def induced_subgraph(g: v7.UGraph, nodes: Set[int]) -> v7.UGraph:
    sub = v7.UGraph()
    for v in sorted(nodes):
        if v in g.adj:
            sub.add_node(v)
    for a in sorted(nodes):
        if a not in g.adj:
            continue
        for b in g.neighbors(a):
            if b in nodes and a < b:
                sub.add_edge(a, b)
    return sub


def run_defect_with_control_graphs(
    base_state: v7.State,
    *,
    params: v7.Params,
    seed: int,
    steps: int,
    perturbation: str,
    center_token_index: int = 0,
    local_coupling: str = "maximal",
    log_every: int = 40,
) -> Dict[str, Any]:
    rng = random.Random(seed)
    control = base_state.clone()
    perturbed = base_state.clone()

    perturbation_info = v15.v14.v08b.apply_custom_perturbation(
        perturbed,
        perturbation,
        center_token_index=center_token_index,
    )
    support = list(perturbation_info["support"])

    next_node_id, next_token_id = v15.v14.v08b.next_ids_from_state(base_state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)

    log_rows: List[Dict[str, Any]] = []
    damaged_sets: List[Set[int]] = []
    control_graphs: List[v7.UGraph] = []

    snap0, damaged0 = v15.defect_snapshot(control, perturbed, support)
    log_rows.append({"step": 0, "t": 0.0, **snap0})
    damaged_sets.append(set(damaged0))
    control_graphs.append(control.g.clone())

    for step in range(1, steps + 1):
        v7.coupled_step(control, perturbed, manager, rng, params, local_coupling)
        if step % log_every == 0 or step == steps:
            snap, damaged = v15.defect_snapshot(control, perturbed, support)
            log_rows.append({"step": step, "t": control.t, **snap})
            damaged_sets.append(set(damaged))
            control_graphs.append(control.g.clone())

    return {
        "perturbation_info": dict(perturbation_info),
        "log_rows": log_rows,
        "damaged_sets": damaged_sets,
        "control_graphs": control_graphs,
    }


def occupancy_partition(damaged_sets: Sequence[Set[int]]) -> Dict[str, Any]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(damaged_sets))))
    tail_sets = damaged_sets[tail_start:]
    denom = max(1, len(tail_sets))
    occ: Counter[int] = Counter()
    for damaged in tail_sets:
        occ.update(damaged)
    occupancies = {node: count / denom for node, count in occ.items()}
    core_nodes = {node for node, frac in occupancies.items() if frac >= CORE_THRESHOLD}
    shell_nodes = {node for node, frac in occupancies.items() if SHELL_THRESHOLD <= frac < CORE_THRESHOLD}
    rare_nodes = {node for node, frac in occupancies.items() if 0.0 < frac < SHELL_THRESHOLD}
    return {
        "tail_start": tail_start,
        "core_nodes": core_nodes,
        "shell_nodes": shell_nodes,
        "rare_nodes": rare_nodes,
    }


def shell_core_attachment_edges(g: v7.UGraph, shell_active: Set[int], core_nodes: Set[int]) -> int:
    count = 0
    for v in shell_active:
        if v not in g.adj:
            continue
        for u in g.neighbors(v):
            if u in core_nodes:
                count += 1
    return count


def shell_attachment_node_frac(g: v7.UGraph, shell_active: Set[int], core_nodes: Set[int]) -> float:
    if not shell_active:
        return float("nan")
    attached = 0
    for v in shell_active:
        if v in g.adj and any(u in core_nodes for u in g.neighbors(v)):
            attached += 1
    return attached / max(1, len(shell_active))


def shell_snapshot_rows(
    *,
    placement: int,
    seed_delta: int,
    run_seed: int,
    support_signature: str,
    core_nodes: Set[int],
    shell_nodes: Set[int],
    log_rows: Sequence[Dict[str, Any]],
    damaged_sets: Sequence[Set[int]],
    control_graphs: Sequence[v7.UGraph],
) -> List[Dict[str, Any]]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(log_rows))))
    rows: List[Dict[str, Any]] = []
    for idx in range(tail_start, len(log_rows)):
        control_graph = control_graphs[idx]
        damaged = damaged_sets[idx]
        shell_active = damaged.intersection(shell_nodes)
        comps = v15.damaged_components(control_graph, shell_active)
        sub = induced_subgraph(control_graph, shell_active)
        largest = max((len(comp) for comp in comps), default=0)
        comp_count = len(comps)
        attachment_edges = shell_core_attachment_edges(control_graph, shell_active, core_nodes)
        rows.append(
            {
                "placement": int(placement),
                "seed_delta": int(seed_delta),
                "run_seed": int(run_seed),
                "support_signature": support_signature,
                "snapshot_index": int(idx),
                "step": int(log_rows[idx]["step"]),
                "shell_active_nodes": int(len(shell_active)),
                "shell_component_count": int(comp_count),
                "largest_shell_component_fraction": (largest / len(shell_active)) if shell_active else float("nan"),
                "shell_beta1": int(v7.beta1_cycle_rank(sub)),
                "shell_connected_active": int(comp_count <= 1) if shell_active else -1,
                "shell_fragmented_active": int(comp_count >= 2) if shell_active else -1,
                "shell_loop_present": int(v7.beta1_cycle_rank(sub) > 0) if shell_active else -1,
                "shell_attachment_edges_to_core": int(attachment_edges),
                "shell_attachment_node_frac": safe_float(shell_attachment_node_frac(control_graph, shell_active, core_nodes)),
                "shell_boundary_to_volume": (v15.boundary_edge_count(control_graph, shell_active) / len(shell_active)) if shell_active else float("nan"),
            }
        )
    return rows


def classify_shell_topology(
    *,
    connected_rate: float,
    fragmented_rate: float,
    loop_rate: float,
    mean_component_count: float,
    mean_largest_fraction: float,
) -> str:
    if connected_rate >= 0.80 and loop_rate >= 0.40 and mean_component_count <= 1.30:
        return "looped_shell_band"
    if connected_rate >= 0.80 and fragmented_rate <= 0.20 and mean_largest_fraction >= 0.80:
        return "connected_shell_band"
    if fragmented_rate >= 0.45 or mean_component_count >= 2.00 or mean_largest_fraction <= 0.60:
        return "fragmented_shell_band"
    return "mixed_shell_topology"


def run_rows(*, base_state: Any) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    runs: List[Dict[str, Any]] = []
    snapshots: List[Dict[str, Any]] = []
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    for placement in PLACEMENTS:
        base_run_seed = TARGET * 100000 + GROWTH_SEED * 1000 + int(placement)
        for seed_delta in SEED_DELTAS:
            run_seed = int(base_run_seed + seed_delta)
            res = run_defect_with_control_graphs(
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
            partition = occupancy_partition(res["damaged_sets"])
            core_nodes = set(partition["core_nodes"])
            shell_nodes = set(partition["shell_nodes"])
            rare_nodes = set(partition["rare_nodes"])
            snap_rows = shell_snapshot_rows(
                placement=placement,
                seed_delta=seed_delta,
                run_seed=run_seed,
                support_signature=support_signature,
                core_nodes=core_nodes,
                shell_nodes=shell_nodes,
                log_rows=res["log_rows"],
                damaged_sets=res["damaged_sets"],
                control_graphs=res["control_graphs"],
            )
            snapshots.extend(snap_rows)

            active_rows = [row for row in snap_rows if int(row["shell_active_nodes"]) > 0]
            component_counts = [safe_float(row["shell_component_count"]) for row in active_rows]
            largest_fractions = [safe_float(row["largest_shell_component_fraction"]) for row in active_rows]
            betas = [safe_float(row["shell_beta1"]) for row in active_rows]
            connected_rate = mean_defined(float(row["shell_connected_active"]) for row in active_rows) if active_rows else float("nan")
            fragmented_rate = mean_defined(float(row["shell_fragmented_active"]) for row in active_rows) if active_rows else float("nan")
            loop_rate = mean_defined(float(row["shell_loop_present"]) for row in active_rows) if active_rows else float("nan")
            attachments = [safe_float(row["shell_attachment_edges_to_core"]) for row in active_rows]
            attach_frac = [safe_float(row["shell_attachment_node_frac"]) for row in active_rows if math.isfinite(safe_float(row["shell_attachment_node_frac"]))]
            boundary_vals = [safe_float(row["shell_boundary_to_volume"]) for row in active_rows if math.isfinite(safe_float(row["shell_boundary_to_volume"]))]
            topology_label = classify_shell_topology(
                connected_rate=safe_float(connected_rate),
                fragmented_rate=safe_float(fragmented_rate),
                loop_rate=safe_float(loop_rate),
                mean_component_count=mean_defined(component_counts),
                mean_largest_fraction=mean_defined(largest_fractions),
            ) if active_rows else "shell_absent"

            runs.append(
                {
                    "target_nodes": TARGET,
                    "growth_seed": GROWTH_SEED,
                    "placement": int(placement),
                    "seed_delta": int(seed_delta),
                    "run_seed": int(run_seed),
                    "requested_match": int(v15.v14.perturbation_requested_match("add_chord", str(info.get("type", "unknown")))),
                    "support_signature": support_signature,
                    "full_label": full_label,
                    "full_exact_return_rate": safe_float(recurrence["exact_return_rate"]),
                    "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                    "core_nodes": int(len(core_nodes)),
                    "shell_nodes": int(len(shell_nodes)),
                    "rare_nodes": int(len(rare_nodes)),
                    "tail_active_shell_snapshots": int(len(active_rows)),
                    "mean_shell_component_count": mean_defined(component_counts),
                    "q90_shell_component_count": quantile(component_counts, 0.90) if component_counts else float("nan"),
                    "shell_connected_rate": safe_float(connected_rate),
                    "shell_fragmented_rate": safe_float(fragmented_rate),
                    "shell_loop_rate": safe_float(loop_rate),
                    "mean_largest_shell_component_fraction": mean_defined(largest_fractions),
                    "mean_shell_beta1": mean_defined(betas),
                    "mean_attachment_edges_to_core": mean_defined(attachments),
                    "mean_attachment_node_frac": mean_defined(attach_frac),
                    "mean_shell_boundary_to_volume": mean_defined(boundary_vals),
                    "topology_label": topology_label,
                }
            )
    return runs, snapshots


def aggregate_rows(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        group = [row for row in rows if int(row["placement"]) == int(placement)]
        out.append(
            {
                "placement": int(placement),
                "n_runs": len(group),
                "cyclic_rate": mean_defined(1.0 if str(row["full_label"]) == "cyclic_return" else 0.0 for row in group),
                "connected_shell_rate": mean_defined(1.0 if str(row["topology_label"]) == "connected_shell_band" else 0.0 for row in group),
                "looped_shell_rate": mean_defined(1.0 if str(row["topology_label"]) == "looped_shell_band" else 0.0 for row in group),
                "fragmented_shell_rate": mean_defined(1.0 if str(row["topology_label"]) == "fragmented_shell_band" else 0.0 for row in group),
                "mixed_shell_rate": mean_defined(1.0 if str(row["topology_label"]) == "mixed_shell_topology" else 0.0 for row in group),
                "mean_full_exact_return_rate": mean_defined(safe_float(row["full_exact_return_rate"]) for row in group),
                "mean_shell_component_count": mean_defined(safe_float(row["mean_shell_component_count"]) for row in group),
                "mean_shell_connected_rate": mean_defined(safe_float(row["shell_connected_rate"]) for row in group),
                "mean_shell_fragmented_rate": mean_defined(safe_float(row["shell_fragmented_rate"]) for row in group),
                "mean_shell_loop_rate": mean_defined(safe_float(row["shell_loop_rate"]) for row in group),
                "mean_largest_shell_component_fraction": mean_defined(safe_float(row["mean_largest_shell_component_fraction"]) for row in group),
                "mean_shell_beta1": mean_defined(safe_float(row["mean_shell_beta1"]) for row in group),
                "mean_attachment_node_frac": mean_defined(safe_float(row["mean_attachment_node_frac"]) for row in group),
            }
        )
    return out


def diagnosis_rows(target_summary: Sequence[Dict[str, Any]], rows: Sequence[Dict[str, Any]], aggregate: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in rows), default=0) == 1
    p0 = next(row for row in aggregate if int(row["placement"]) == 0)
    p1 = next(row for row in aggregate if int(row["placement"]) == 1)
    p2 = next(row for row in aggregate if int(row["placement"]) == 2)

    if min(safe_float(p0["connected_shell_rate"]), safe_float(p1["connected_shell_rate"]), safe_float(p2["connected_shell_rate"])) >= 0.50:
        status = "cycle_band_has_connected_shell"
        note = "Randen ser vanligvis ut som ett sammenhengende band rundt kjernen, ikke som mange frie biter."
        next_step = "probe_shell_events"
        next_note = "Neste steg bør se pa rolige rand-hendelser og hvor shellen faktisk legges til eller trekkes fra."
    elif max(safe_float(p0["fragmented_shell_rate"]), safe_float(p1["fragmented_shell_rate"]), safe_float(p2["fragmented_shell_rate"])) >= 0.50:
        status = "cycle_band_has_fragmented_shell_zone"
        note = "Minst ett av de lokale punktene ser ofte ut til a bryte randen opp i flere separate biter."
        next_step = "localize_fragment_events"
        next_note = "Neste steg bør finne hvor i halen disse fragmenteringene oppstar, ikke scanne bredere."
    elif max(safe_float(p0["looped_shell_rate"]), safe_float(p1["looped_shell_rate"]), safe_float(p2["looped_shell_rate"])) >= 0.50:
        status = "cycle_band_has_looped_shell_zone"
        note = "Randen bærer ofte lokal cycle-rank uten a miste all sammenheng, sa topologi er en del av signalet."
        next_step = "track_shell_loops"
        next_note = "Neste steg bør folge nar lokale shell-lokker dannes og brytes."
    else:
        status = "shell_topology_still_mixed"
        note = "Topologiobservabelen gjor bandet mer konkret, men ikke rent nok til en enkel connected/fragmented/looped-lesning ennå."
        next_step = "stay_shell_local"
        next_note = "Neste steg bør vaere en enda mindre randhendelsesrunde i samme band."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsene er rent separert og alle shell-topologiprofilene matcher onsket add_chord-perturbasjon."
                if (size_clean and strict_match)
                else "Enten storrelsesseparasjon eller perturbasjonsmatching er uklar i denne runden."
            ),
        },
        {
            "diagnostic_family": "shell_topology_status",
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
    lines.append("# Relasjonell universgraf v0.15ae: add_chord shell topology lab")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden spør om den rolige variable randen rundt add_chord-kjernen vanligvis holder seg sammenhengende, blir fragmentert, eller bærer lokal cycle-rank.")
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
    lines.append("## Shell-topology summary")
    lines.append("")
    lines.append("| placement | n | cyclic | connected shell | looped shell | fragmented shell | mixed shell | mean comp | mean connected | mean loop |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['placement'])} | {int(row['n_runs'])} | {fmt(row['cyclic_rate'])} | {fmt(row['connected_shell_rate'])} | {fmt(row['looped_shell_rate'])} | {fmt(row['fragmented_shell_rate'])} | {fmt(row['mixed_shell_rate'])} | {fmt(row['mean_shell_component_count'])} | {fmt(row['mean_shell_connected_rate'])} | {fmt(row['mean_shell_loop_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er fortsatt samme smale `t48_g202`-band, ikke en ny bred scan.")
    lines.append("- Les topologi her som en lokal randobservabel, ikke som bevis for en generell defect-lov.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15ae add_chord shell topology lab.")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15ae_add_chord_shell_topology_runs.csv")
    p.add_argument("--out-snapshots-csv", type=str, default="Documentation/v15ae_add_chord_shell_topology_snapshots.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15ae_add_chord_shell_topology_aggregate.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15ae_add_chord_shell_topology_diagnosis.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15ae_add_chord_shell_topology_target_summary.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15ae_add_chord_shell_topology_lab.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15ae_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ae.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    target_summary = v10e.summarize_bases(base_rows)
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    runs, snapshots = run_rows(base_state=base_state)
    aggregate = aggregate_rows(runs)
    diagnosis = diagnosis_rows(target_summary, runs, aggregate)
    report_md = build_report(target_summary=target_summary, aggregate=aggregate, diagnosis=diagnosis)
    op_md = "\n".join(
        [
            "# v0.15ae operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les denne runden som en shell-topologiobservabel inne i samme lokale add_chord-band, ikke som en ny bred defect-scan.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15ae",
            "",
            "Etter at vi fant en stabil kjerne med en rolig flimrende rand, ser denne runden pa formen til randen: holder den seg stort sett samlet, eller deles den ofte opp i flere biter?",
            "",
            "Vi maaler derfor hvor mange separate randbiter som finnes i senfasen, og om randen ofte lager lokale lokker.",
        ]
    ) + "\n"
    write_csv(args.out_runs_csv, runs)
    write_csv(args.out_snapshots_csv, snapshots)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_target_csv, target_summary)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
