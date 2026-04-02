#!/usr/bin/env python3
"""v0.15 defect lifetime lab around the stable anchor regime.

This round asks a different question than the v14 Lorentz diagnostics:
do local perturbations in the stable `band_zero_del` regime produce any
repeatable mesoscale defect behavior such as:

- fast extinction
- persistent localization
- persistent diffuse spread
- multi-component / split damage

The goal is not to prove particles or fields. It is to test whether the model
supports robust local excitations with a recognizable lifetime / morphology,
under the same artifact-aware workflow used in the later v11-v14 chain.
"""
from __future__ import annotations

import argparse
import math
import random
import statistics
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v09_scale_and_natural_ensembles as v09
import relational_universe_v10b_ensemble_calibration as v10b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14_lorentz_diagnostics as v14


ANCHOR_NAME = v14.ANCHOR_CANDIDATE
PERTURBATIONS = ("local_swap", "add_chord", "token_shift")


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v14.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v14.mean_defined(values)


def sd_or_zero(values: Iterable[float]) -> float:
    return v14.sd_or_zero(values)


def quantile(values: Sequence[float], q: float) -> float:
    return v14.quantile(values, q)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v10b.write_csv(path, rows)


def anchor_spec() -> Dict[str, Any]:
    return {
        "candidate": v09.ScaleCandidate(ANCHOR_NAME, 0.02, 0.00, 0.02, 0.00, 0.00),
        "candidate_role": "anchor",
    }


def deep_ensembles(targets: Sequence[int]) -> List[v10b.CalibrationEnsemble]:
    return [ens for ens in v10b.build_ensembles(targets) if ens.burnin_label == "deep"]


def defect_steps_for_state(nodes: int) -> int:
    return max(360, min(1600, int(round(7.0 * nodes))))


def damaged_components(g: v7.UGraph, damaged: Set[int]) -> List[Set[int]]:
    relevant = {v for v in damaged if v in g.adj}
    if not relevant:
        return []
    comps: List[Set[int]] = []
    seen: Set[int] = set()
    for start in sorted(relevant):
        if start in seen:
            continue
        comp = {start}
        seen.add(start)
        stack = [start]
        while stack:
            v = stack.pop()
            for u in g.neighbors(v):
                if u in relevant and u not in seen:
                    seen.add(u)
                    comp.add(u)
                    stack.append(u)
        comps.append(comp)
    return comps


def boundary_edge_count(g: v7.UGraph, damaged: Set[int]) -> int:
    count = 0
    for v in damaged:
        if v not in g.adj:
            continue
        for u in g.neighbors(v):
            if u not in damaged:
                count += 1
    return count


def jaccard(a: Set[int], b: Set[int]) -> float:
    union = a.union(b)
    if not union:
        return 1.0
    return float(len(a.intersection(b)) / len(union))


def defect_snapshot(control: v7.State, perturbed: v7.State, support: Sequence[int]) -> Tuple[Dict[str, Any], Set[int]]:
    base = v7.damage_snapshot(control, perturbed, support)
    damaged = v7.damaged_nodes(control, perturbed)
    comps = damaged_components(control.g, damaged)
    largest = max((len(comp) for comp in comps), default=0)
    damaged_count = len(damaged)
    boundary = boundary_edge_count(control.g, damaged)
    return (
        {
            **base,
            "damage_component_count": len(comps),
            "largest_component_fraction": (largest / damaged_count) if damaged_count > 0 else 0.0,
            "boundary_edge_count": boundary,
            "boundary_to_volume": (boundary / damaged_count) if damaged_count > 0 else 0.0,
            "alive": 1 if damaged_count > 0 else 0,
        },
        damaged,
    )


def run_defect_from_base(
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

    perturbation_info = v14.v08b.apply_custom_perturbation(
        perturbed,
        perturbation,
        center_token_index=center_token_index,
    )
    support = list(perturbation_info["support"])

    next_node_id, next_token_id = v14.v08b.next_ids_from_state(base_state)
    manager = v7.PairManager(next_node_id=next_node_id, next_token_id=next_token_id)

    log_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []

    prev_damaged: Optional[Set[int]] = None
    shape_jaccards: List[float] = []
    first_zero_step: Optional[int] = None
    last_alive_step = 0

    snap0, damaged0 = defect_snapshot(control, perturbed, support)
    log_rows.append({"step": 0, "t": 0.0, **snap0})
    if damaged0:
        last_alive_step = 0
    prev_damaged = set(damaged0)

    equal_prev = v7.states_equal(control, perturbed)
    first_meeting_time = 0.0 if equal_prev else None

    for step in range(1, steps + 1):
        ev = v7.coupled_step(control, perturbed, manager, rng, params, local_coupling)
        ev["step"] = step
        ev["t"] = control.t
        event_rows.append(ev)

        equal_now = v7.states_equal(control, perturbed)
        if equal_now and not equal_prev and first_meeting_time is None:
            first_meeting_time = control.t
        equal_prev = equal_now

        if step % log_every == 0 or step == steps:
            snap, damaged = defect_snapshot(control, perturbed, support)
            if prev_damaged is not None:
                shape_jaccards.append(jaccard(prev_damaged, damaged))
            prev_damaged = set(damaged)
            if snap["alive"]:
                last_alive_step = step
            elif first_zero_step is None:
                first_zero_step = step
            log_rows.append({"step": step, "t": control.t, **snap})

    final = log_rows[-1]
    initial_nodes = max(1.0, safe_float(v7.feature_row(base_state, rng=random.Random(seed + 999)).get("nodes")))
    alive_fraction = mean_defined(float(row["alive"]) for row in log_rows)
    mean_damage_fraction = mean_defined(safe_float(row["damaged_nodes_count"]) / initial_nodes for row in log_rows)
    max_damage_fraction = max((safe_float(row["damaged_nodes_count"]) / initial_nodes for row in log_rows), default=0.0)
    mean_radius = mean_defined(safe_float(row["radius_control"]) for row in log_rows if safe_float(row["radius_control"]) >= 0)
    max_radius = max((safe_float(row["radius_control"]) for row in log_rows if safe_float(row["radius_control"]) >= 0), default=-1.0)
    mean_components = mean_defined(safe_float(row["damage_component_count"]) for row in log_rows)
    max_components = max((int(row["damage_component_count"]) for row in log_rows), default=0)
    mean_largest_fraction = mean_defined(safe_float(row["largest_component_fraction"]) for row in log_rows)
    mean_boundary_to_volume = mean_defined(safe_float(row["boundary_to_volume"]) for row in log_rows)
    mean_shape_stability = mean_defined(shape_jaccards)
    last_alive_fraction = float(last_alive_step / max(1, steps))
    final_alive = int(final["alive"])

    if final_alive == 0 and alive_fraction <= 0.60 and last_alive_fraction <= 0.75:
        outcome = "dies_out"
    elif final_alive == 1 and mean_radius <= 2.0 and mean_damage_fraction <= 0.08 and mean_components <= 1.30:
        outcome = "persistent_localized"
    elif final_alive == 1 and max_components >= 2 and mean_largest_fraction <= 0.78:
        outcome = "persistent_split"
    elif final_alive == 1 and mean_radius >= 2.5 and mean_damage_fraction >= 0.05:
        outcome = "persistent_diffuse"
    else:
        outcome = "mixed_transient"

    return {
        "perturbation_info": dict(perturbation_info),
        "log_rows": log_rows,
        "event_rows": event_rows,
        "summary": {
            "final_alive": final_alive,
            "alive_fraction": alive_fraction,
            "last_alive_fraction": last_alive_fraction,
            "first_zero_step": first_zero_step if first_zero_step is not None else -1,
            "mean_damage_fraction": mean_damage_fraction,
            "max_damage_fraction": max_damage_fraction,
            "mean_radius_control": mean_radius,
            "max_radius_control": max_radius,
            "mean_component_count": mean_components,
            "max_component_count": max_components,
            "mean_largest_component_fraction": mean_largest_fraction,
            "mean_boundary_to_volume": mean_boundary_to_volume,
            "mean_shape_stability": mean_shape_stability,
            "outcome_class": outcome,
            "first_meeting_time": first_meeting_time if first_meeting_time is not None else -1.0,
            "fit_speed_control": safe_float(v7.estimate_front_speed(log_rows, "t", "radius_control")["fit_slope"]),
            "mean_shared_node_fraction_final": safe_float(final["node_shared_fraction"]),
        },
    }


def collect_run_rows(
    spec: Mapping[str, Any],
    ensembles: Sequence[v10b.CalibrationEnsemble],
    base_states: Mapping[Tuple[str, int], Any],
    growth_seeds: Sequence[int],
    run_offsets: Sequence[int],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    cand = spec["candidate"]
    params = v09.candidate_to_params(cand)
    for ens in ensembles:
        for gseed in growth_seeds:
            base = base_states[(ens.name, int(gseed))]
            steps = defect_steps_for_state(base.g.num_nodes())
            log_every = max(10, min(80, steps // 24))
            for run_offset in run_offsets:
                run_seed = int(ens.target_nodes) * 100000 + int(gseed) * 1000 + int(run_offset)
                for perturbation in PERTURBATIONS:
                    res = run_defect_from_base(
                        base,
                        params=params,
                        seed=run_seed,
                        steps=steps,
                        perturbation=perturbation,
                        local_coupling="maximal",
                        log_every=log_every,
                    )
                    perturb_info = res["perturbation_info"]
                    actual = str(perturb_info.get("type", "unknown"))
                    requested_match = v14.perturbation_requested_match(perturbation, actual)
                    support = list(perturb_info.get("support", []))
                    summary = res["summary"]
                    rows.append(
                        {
                            "candidate_name": cand.name,
                            "ensemble": ens.name,
                            "target_nodes": ens.target_nodes,
                            "growth_seed": int(gseed),
                            "run_offset": int(run_offset),
                            "run_seed": int(run_seed),
                            "steps": int(steps),
                            "requested_perturbation": perturbation,
                            "actual_perturbation": actual,
                            "requested_match": 1 if requested_match else 0,
                            "support_size": len(support),
                            "support_signature": ",".join(str(x) for x in support),
                            **summary,
                        }
                    )
    return rows


def aggregate_rows(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: MutableMapping[str, List[Dict[str, Any]]] = {}
    for row in run_rows:
        grouped.setdefault(str(row["requested_perturbation"]), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for perturbation, rows in sorted(grouped.items()):
        outcome_counts: Dict[str, int] = {}
        for row in rows:
            outcome = str(row["outcome_class"])
            outcome_counts[outcome] = outcome_counts.get(outcome, 0) + 1
        dominant = max(outcome_counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
        out.append(
            {
                "requested_perturbation": perturbation,
                "n_runs": len(rows),
                "strict_match_rate": mean_defined(float(r["requested_match"]) for r in rows),
                "mean_alive_fraction": mean_defined(safe_float(r["alive_fraction"]) for r in rows),
                "mean_mean_damage_fraction": mean_defined(safe_float(r["mean_damage_fraction"]) for r in rows),
                "mean_max_damage_fraction": mean_defined(safe_float(r["max_damage_fraction"]) for r in rows),
                "mean_radius_control": mean_defined(safe_float(r["mean_radius_control"]) for r in rows),
                "mean_fit_speed_control": mean_defined(safe_float(r["fit_speed_control"]) for r in rows),
                "mean_component_count": mean_defined(safe_float(r["mean_component_count"]) for r in rows),
                "mean_largest_component_fraction": mean_defined(safe_float(r["mean_largest_component_fraction"]) for r in rows),
                "mean_boundary_to_volume": mean_defined(safe_float(r["mean_boundary_to_volume"]) for r in rows),
                "mean_shape_stability": mean_defined(safe_float(r["mean_shape_stability"]) for r in rows),
                "dominant_outcome_class": dominant,
                "outcome_dies_out_rate": outcome_counts.get("dies_out", 0) / max(1, len(rows)),
                "outcome_persistent_localized_rate": outcome_counts.get("persistent_localized", 0) / max(1, len(rows)),
                "outcome_persistent_split_rate": outcome_counts.get("persistent_split", 0) / max(1, len(rows)),
                "outcome_persistent_diffuse_rate": outcome_counts.get("persistent_diffuse", 0) / max(1, len(rows)),
                "outcome_mixed_transient_rate": outcome_counts.get("mixed_transient", 0) / max(1, len(rows)),
            }
        )
    return out


def outcome_by_target_rows(run_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: MutableMapping[Tuple[str, int], List[Dict[str, Any]]] = {}
    for row in run_rows:
        grouped.setdefault((str(row["requested_perturbation"]), int(row["target_nodes"])), []).append(dict(row))
    out: List[Dict[str, Any]] = []
    for (perturbation, target_nodes), rows in sorted(grouped.items()):
        out.append(
            {
                "requested_perturbation": perturbation,
                "target_nodes": target_nodes,
                "n_runs": len(rows),
                "mean_alive_fraction": mean_defined(safe_float(r["alive_fraction"]) for r in rows),
                "mean_radius_control": mean_defined(safe_float(r["mean_radius_control"]) for r in rows),
                "persistent_localized_rate": mean_defined(1.0 if str(r["outcome_class"]) == "persistent_localized" else 0.0 for r in rows),
                "persistent_split_rate": mean_defined(1.0 if str(r["outcome_class"]) == "persistent_split" else 0.0 for r in rows),
                "persistent_diffuse_rate": mean_defined(1.0 if str(r["outcome_class"]) == "persistent_diffuse" else 0.0 for r in rows),
                "dies_out_rate": mean_defined(1.0 if str(r["outcome_class"]) == "dies_out" else 0.0 for r in rows),
            }
        )
    return out


def recommendation_rows(
    target_summary: Sequence[Dict[str, Any]],
    aggregate: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((safe_float(row["strict_match_rate"], 0.0) for row in aggregate), default=0.0) >= 0.999
    out.append(
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstørrelsene er separert og alle testede perturbasjoner holder ønsket lokale type i denne runden."
                if (size_clean and strict_match)
                else "Enten størrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        }
    )

    best_localized = max(aggregate, key=lambda r: safe_float(r["outcome_persistent_localized_rate"]), default=None)
    best_split = max(aggregate, key=lambda r: safe_float(r["outcome_persistent_split_rate"]), default=None)
    best_diffuse = max(aggregate, key=lambda r: safe_float(r["outcome_persistent_diffuse_rate"]), default=None)

    interesting = False
    notes: List[str] = []
    if best_localized and safe_float(best_localized["outcome_persistent_localized_rate"]) >= 0.25:
        interesting = True
        notes.append(
            f"`{best_localized['requested_perturbation']}` har ikke-triviell andel `persistent_localized` ({safe_float(best_localized['outcome_persistent_localized_rate']):.3f})."
        )
    if best_split and safe_float(best_split["outcome_persistent_split_rate"]) >= 0.20:
        interesting = True
        notes.append(
            f"`{best_split['requested_perturbation']}` viser `persistent_split` oftere enn rent tilfeldig transientstøy ({safe_float(best_split['outcome_persistent_split_rate']):.3f})."
        )
    if best_diffuse and safe_float(best_diffuse["outcome_persistent_diffuse_rate"]) >= 0.30:
        interesting = True
        notes.append(
            f"`{best_diffuse['requested_perturbation']}` gir vedvarende diffuse eksitasjoner i merkbar andel kjøringer ({safe_float(best_diffuse['outcome_persistent_diffuse_rate']):.3f})."
        )

    if interesting:
        status = "interesting_mesoscale_signal"
        note = " ".join(notes)
        next_status = "follow_objects"
        next_note = "Neste steg bør være å følge den mest lovende utfallstypen mer direkte, for eksempel med kollisjoner eller lengre levetidsrunder."
    else:
        status = "mostly_transient"
        note = "De fleste lokale perturbasjoner ser fortsatt ut som transient eller diffuse skadefelt, ikke som rene langlivede lokale objekter."
        next_status = "pause_or_retarget"
        next_note = "Neste steg bør enten være lengre oppfølging av den minst dårlige perturbasjonen eller et skifte til en annen eksitasjonstype."

    out.append(
        {
            "diagnostic_family": "defect_lifetime_signal",
            "status": status,
            "note": note,
        }
    )
    out.append(
        {
            "diagnostic_family": "next_step",
            "status": next_status,
            "note": next_note,
        }
    )
    return out


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def build_report(
    target_summary: Sequence[Dict[str, Any]],
    aggregate: Sequence[Dict[str, Any]],
    by_target: Sequence[Dict[str, Any]],
    recommendation: Sequence[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15: defect lifetime lab")
    lines.append("")
    lines.append("## Formål")
    lines.append("")
    lines.append(
        "Denne runden ser ikke etter Lorentz-likhet. Den tester om lokale perturbasjoner i `band_zero_del` skaper gjentagbare mesoskalafenomener som dør ut, forblir lokalisert, splitter seg eller blir vedvarende diffuse."
    )
    lines.append("")
    lines.append("## Startstørrelser")
    lines.append("")
    lines.append("| target | mean initial nodes | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Perturbasjonssammendrag")
    lines.append("")
    lines.append("| perturbation | alive | mean radius | mean components | localized | split | diffuse | dies out | dominant |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['requested_perturbation']} | {fmt(row['mean_alive_fraction'])} | {fmt(row['mean_radius_control'])} | {fmt(row['mean_component_count'])} | {fmt(row['outcome_persistent_localized_rate'])} | {fmt(row['outcome_persistent_split_rate'])} | {fmt(row['outcome_persistent_diffuse_rate'])} | {fmt(row['outcome_dies_out_rate'])} | {row['dominant_outcome_class']} |"
        )
    lines.append("")
    lines.append("## Outcome etter størrelse")
    lines.append("")
    lines.append("| perturbation | target | alive | radius | localized | split | diffuse | dies out |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in by_target:
        lines.append(
            f"| {row['requested_perturbation']} | {int(row['target_nodes'])} | {fmt(row['mean_alive_fraction'])} | {fmt(row['mean_radius_control'])} | {fmt(row['persistent_localized_rate'])} | {fmt(row['persistent_split_rate'])} | {fmt(row['persistent_diffuse_rate'])} | {fmt(row['dies_out_rate'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in recommendation:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Heuristisk klassifisering")
    lines.append("")
    lines.append("- `dies_out`: skaden kollapser tidlig og holder seg ikke aktiv lenge.")
    lines.append("- `persistent_localized`: skaden holder seg i live, men forblir liten og relativt sammenhengende.")
    lines.append("- `persistent_split`: skaden holder seg i live og viser fler-komponentmønster.")
    lines.append("- `persistent_diffuse`: skaden holder seg i live og sprer seg bredt.")
    lines.append("- `mixed_transient`: ingen ren type dominerer klart.")
    lines.append("")
    lines.append("Disse klassene er heuristiske arbeidskategorier, ikke nye fysiske partikkeltyper.")
    lines.append("")
    return "\n".join(lines)


def build_lay_summary(recommendation: Sequence[Dict[str, Any]]) -> str:
    signal = next((row for row in recommendation if row["diagnostic_family"] == "defect_lifetime_signal"), None)
    nxt = next((row for row in recommendation if row["diagnostic_family"] == "next_step"), None)
    return "\n".join(
        [
            "# Relasjonell universgraf v0.15 for ikke-spesialister",
            "",
            "Denne runden spurte om små lokale inngrep i grafen lager noe som oppfører seg som et lite objekt med egen levetid, eller bare forbigående skade.",
            "",
            f"Hoveddommen er `{signal['status'] if signal else 'ukjent'}`.",
            "",
            f"Det betyr: {signal['note'] if signal else 'ingen oppsummering tilgjengelig.'}",
            "",
            f"Neste anbefaling er: {nxt['note'] if nxt else 'ingen ny anbefaling registrert.'}",
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15 defect lifetime lab.")
    p.add_argument("--targets", type=str, default="48,96,192,256")
    p.add_argument("--growth-seeds", type=str, default="101,202")
    p.add_argument("--run-offsets", type=str, default="0,17")
    p.add_argument("--out-run-csv", type=str, default="Documentation/v15_defect_lifetime_run_rows.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15_defect_lifetime_target_summary.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15_defect_lifetime_aggregate.csv")
    p.add_argument("--out-by-target-csv", type=str, default="Documentation/v15_defect_lifetime_by_target.csv")
    p.add_argument("--out-recommendation-csv", type=str, default="Documentation/v15_defect_lifetime_recommendations.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15_defect_lifetime_lab.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15_operativ_anbefaling.md")
    return p.parse_args()


def parse_int_list(spec: str) -> List[int]:
    return [int(part.strip()) for part in spec.split(",") if part.strip()]


def main() -> None:
    args = parse_args()
    targets = parse_int_list(args.targets)
    growth_seeds = parse_int_list(args.growth_seeds)
    run_offsets = parse_int_list(args.run_offsets)

    spec = anchor_spec()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = deep_ensembles(targets)
    base_states, base_rows = v10e.build_bases(ensembles, regime, growth_seeds)
    target_summary = v10e.summarize_bases(base_rows)

    run_rows = collect_run_rows(spec, ensembles, base_states, growth_seeds, run_offsets)
    aggregate = aggregate_rows(run_rows)
    by_target = outcome_by_target_rows(run_rows)
    recommendation = recommendation_rows(target_summary, aggregate)

    report_md = build_report(target_summary, aggregate, by_target, recommendation)
    lay_md = build_lay_summary(recommendation)
    op_md = "\n".join(
        [
            "# v0.15 operativ anbefaling",
            "",
            *[
                f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}"
                for row in recommendation
            ],
            "",
            "- Ikke les denne runden som bevis på partikler eller felt.",
            "- Les den som en arbeidsdiagnostikk av om lokale eksitasjoner får repeterbar mesoskopisk levetid eller form.",
        ]
    )

    write_csv(args.out_run_csv, run_rows)
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_by_target_csv, by_target)
    write_csv(args.out_recommendation_csv, recommendation)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")

    print(f"Wrote {args.out_summary_md}")
    print(f"Wrote {args.out_aggregate_csv}")
    print(f"Wrote {args.out_by_target_csv}")


if __name__ == "__main__":
    main()
