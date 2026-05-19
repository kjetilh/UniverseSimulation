#!/usr/bin/env python3
"""v0.15cx add_chord p1/1024 genealogy holdout.

v15cw found one narrow genealogy split worth holding out:

- target 1024, placement p1, seed 7307 had no far-shell horizon and
  `birth_death_churn`
- target 1024, placement p1, seed 7351 had established far-shell horizon and
  `split_fragment`

This lab does not broaden the placement search. It tests that concrete mapping
on fresh seed deltas while keeping component trajectories and event logs as the
primary data product. The far-shell horizon label remains a downstream outcome.
"""
from __future__ import annotations

import argparse
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15cn_p2_horizon_scale_holdout as v15cn
import relational_universe_v15cs_add_chord_p0_scale_response_holdout as v15cs
import relational_universe_v15cv_add_chord_winning_placement_mechanism_probe as v15cv
import relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split as v15cw
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET_NODES = 1024
PLACEMENT = 1
PERTURBATION = "add_chord"
GROWTH_SEED = v15cv.GROWTH_SEED
LOG_EVERY = v15cv.LOG_EVERY
HOLDOUT_SEED_DELTAS = (7411, 7477, 7541, 7603)

CALIBRATION_MAP = {
    "birth_death_churn": "no_far_shell_horizon",
    "split_fragment": "established_far_shell_horizon",
}


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def profile_label() -> str:
    return f"{PERTURBATION}_p{PLACEMENT}"


def predicted_horizon_from_genealogy(pattern: str) -> str:
    return CALIBRATION_MAP.get(str(pattern), "ambiguous_from_v15cw_calibration")


def is_prediction_correct(predicted: str, observed: str) -> int:
    if predicted == "ambiguous_from_v15cw_calibration":
        return 0
    if predicted == "no_far_shell_horizon":
        return int(observed != "established_far_shell_horizon")
    return int(observed == predicted)


def run_rows_with_holdout_fields(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        pattern = str(row["genealogy_pattern"])
        observed = str(row["far_shell_horizon_label"])
        predicted = predicted_horizon_from_genealogy(pattern)
        known = int(predicted != "ambiguous_from_v15cw_calibration")
        correct = is_prediction_correct(predicted, observed) if known else 0
        out.append(
            {
                **dict(row),
                "holdout_role": "fresh_seed_holdout",
                "v15cw_expected_from_genealogy": predicted,
                "v15cw_mapping_known": known,
                "v15cw_mapping_correct": correct,
            }
        )
    return out


def aggregate_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    known = [row for row in run_rows if int(row["v15cw_mapping_known"]) == 1]
    established = [row for row in run_rows if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon"]
    no_horizon = [row for row in run_rows if str(row["far_shell_horizon_label"]) != "established_far_shell_horizon"]
    patterns = Counter(str(row["genealogy_pattern"]) for row in run_rows)
    horizon_patterns = {str(row["genealogy_pattern"]) for row in established}
    no_horizon_patterns = {str(row["genealogy_pattern"]) for row in no_horizon}
    return [
        {
            "target_nodes": TARGET_NODES,
            "profile_label": profile_label(),
            "placement": PLACEMENT,
            "n_runs": len(run_rows),
            "holdout_seed_deltas": ";".join(str(int(row["seed_delta"])) for row in run_rows),
            "established_far_shell_rate": mean_defined(
                1.0 if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon" else 0.0
                for row in run_rows
            ),
            "mean_high_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in run_rows),
            "genealogy_patterns": ";".join(f"{k}:{v}" for k, v in sorted(patterns.items())),
            "horizon_patterns": ";".join(sorted(horizon_patterns)),
            "no_horizon_patterns": ";".join(sorted(no_horizon_patterns)),
            "pattern_separates_outcome": int(bool(established) and bool(no_horizon) and horizon_patterns.isdisjoint(no_horizon_patterns)),
            "known_mapping_n": len(known),
            "known_mapping_rate": len(known) / max(1, len(run_rows)),
            "known_mapping_match_rate": mean_defined(float(row["v15cw_mapping_correct"]) for row in known),
            "mean_split_count": mean_defined(safe_float(row["split_count"]) for row in run_rows),
            "mean_birth_count": mean_defined(safe_float(row["birth_count"]) for row in run_rows),
            "mean_death_count": mean_defined(safe_float(row["death_count"]) for row in run_rows),
            "mean_churn_event_count": mean_defined(safe_float(row["churn_event_count"]) for row in run_rows),
            "mean_max_component_count": mean_defined(safe_float(row["max_component_count"]) for row in run_rows),
            "mean_max_total_defect_mass": mean_defined(safe_float(row["max_total_defect_mass"]) for row in run_rows),
        }
    ]


def chain_summary_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    groups: Dict[str, List[Mapping[str, Any]]] = {}
    for row in run_rows:
        groups.setdefault(str(row["genealogy_pattern"]), []).append(row)
    out: List[Dict[str, Any]] = []
    for pattern, rows in sorted(groups.items()):
        known = [row for row in rows if int(row["v15cw_mapping_known"]) == 1]
        out.append(
            {
                "genealogy_pattern": pattern,
                "n_runs": len(rows),
                "seed_deltas": ";".join(str(int(row["seed_delta"])) for row in rows),
                "v15cw_expected_from_genealogy": predicted_horizon_from_genealogy(pattern),
                "known_mapping_match_rate": mean_defined(float(row["v15cw_mapping_correct"]) for row in known),
                "established_far_shell_rate": mean_defined(
                    1.0 if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon" else 0.0
                    for row in rows
                ),
                "mean_high_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in rows),
                "mean_churn_event_count": mean_defined(safe_float(row["churn_event_count"]) for row in rows),
                "mean_max_component_count": mean_defined(safe_float(row["max_component_count"]) for row in rows),
                "mean_max_total_defect_mass": mean_defined(safe_float(row["max_total_defect_mass"]) for row in rows),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    agg = aggregate[0]
    known_n = int(agg["known_mapping_n"])
    known_rate = safe_float(agg["known_mapping_rate"])
    match_rate = safe_float(agg["known_mapping_match_rate"])
    separates = int(agg["pattern_separates_outcome"]) == 1
    has_both_outcomes = (
        0.0 < safe_float(agg["established_far_shell_rate"]) < 1.0
    )
    patterns = str(agg["genealogy_patterns"])

    if known_n >= 2 and match_rate >= 0.75 and separates and has_both_outcomes:
        holdout_status = "p1_1024_genealogy_axis_supported"
        holdout_note = (
            f"v15cw mapping kjennes for {known_n}/{len(run_rows)} holdout-runs og matcher med rate {fmt(match_rate)}; "
            "horizon/no-horizon patterns er disjunkte."
        )
        next_step = "test_p1_1024_genealogy_axis_on_second_growth_seed"
        next_note = "Neste steg bor teste samme konkrete akse paa en ny growth seed, ikke utvide placement-rommet for tidlig."
    elif known_n >= 1 and match_rate >= 0.75:
        holdout_status = "p1_1024_genealogy_axis_one_sided_or_partial"
        holdout_note = (
            f"v15cw mapping matcher kjente holdout-patterns med rate {fmt(match_rate)}, men bare {known_n}/{len(run_rows)} "
            f"runs traff kalibrerte patterns; patterns={patterns}."
        )
        next_step = "increase_p1_1024_holdout_until_both_sides_or_new_patterns"
        next_note = "Neste steg bor enten oke n for p1/1024 eller lage en mer robust genealogy-klassifikator foer generalisering."
    elif known_n >= 1:
        holdout_status = "p1_1024_genealogy_axis_weakened"
        holdout_note = (
            f"Kalibrerte v15cw-patterns dukket opp, men mappingen matcher bare med rate {fmt(match_rate)}."
        )
        next_step = "retire_p1_1024_genealogy_as_selector"
        next_note = "Neste steg bor lete etter en ny observabel; genealogy alene skal ikke brukes som selector."
    else:
        holdout_status = "p1_1024_specific_genealogy_axis_not_reproduced"
        holdout_note = (
            f"Ingen holdout-runs traff de to kalibrerte v15cw-patterns; patterns={patterns}. "
            f"Dette svekker den konkrete birth_death_churn/split_fragment-mappingen, selv om genealogy-intensitet fortsatt kan vaere informativ."
        )
        next_step = "build_continuous_genealogy_intensity_observable"
        next_note = "Neste steg bor score churn, split-timing, dual-duration og max-mass som kontinuerlige observabler mot horizon, ikke legge mer vekt paa grove event-chain labels."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelse er ren og alle requested add_chord-perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Enten startstorrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        },
        {
            "diagnostic_family": "holdout_scope",
            "status": "narrow_p1_1024_only",
            "note": f"Target {TARGET_NODES}, placement p{PLACEMENT}, growth_seed {GROWTH_SEED}, seeds {HOLDOUT_SEED_DELTAS}.",
        },
        {"diagnostic_family": "genealogy_holdout", "status": holdout_status, "note": holdout_note},
        {"diagnostic_family": "next_step", "status": next_step, "note": next_note},
    ]


def build_report(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    chain_summary: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cx: p1/1024 genealogy holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden holder ut den konkrete v15cw-hypotesen for `add_chord_p1` ved target `1024`.")
    lines.append("Den utvider ikke placement-rommet. Primaerdata er component trajectories og event logs; far-shell horizon er downstream outcome.")
    lines.append("")
    lines.append("## Design")
    lines.append("")
    lines.append("| field | value |")
    lines.append("| --- | --- |")
    lines.append(f"| target | {TARGET_NODES} |")
    lines.append(f"| placement | p{PLACEMENT} |")
    lines.append(f"| growth seed | {GROWTH_SEED} |")
    lines.append(f"| holdout seed deltas | {';'.join(str(x) for x in HOLDOUT_SEED_DELTAS)} |")
    lines.append("| v15cw calibration | `birth_death_churn -> no_far_shell_horizon`; `split_fragment -> established_far_shell_horizon` |")
    lines.append("")
    lines.append("## Startstorrelse")
    lines.append("")
    lines.append("| target | mean initial | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'],1)} | {fmt(row['q10_initial_nodes'],1)} | {fmt(row['q90_initial_nodes'],1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Per-run holdout")
    lines.append("")
    lines.append("| seed | horizon | genealogy pattern | expected from v15cw | match | split | birth | death | churn | max comps | max mass |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in run_rows:
        lines.append(
            f"| {int(row['seed_delta'])} | {row['far_shell_horizon_label']} | {row['genealogy_pattern']} | {row['v15cw_expected_from_genealogy']} | {int(row['v15cw_mapping_correct']) if int(row['v15cw_mapping_known']) else 'ambiguous'} | {int(row['split_count'])} | {int(row['birth_count'])} | {int(row['death_count'])} | {int(row['churn_event_count'])} | {int(row['max_component_count'])} | {int(row['max_total_defect_mass'])} |"
        )
    lines.append("")
    lines.append("## Aggregate")
    lines.append("")
    lines.append("| n | est rate | horizon | patterns | known mapping n | match rate | separates outcome | mean churn | mean max comps |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {int(row['n_runs'])} | {fmt(row['established_far_shell_rate'])} | {fmt(row['mean_high_horizon_span'])} | {row['genealogy_patterns']} | {int(row['known_mapping_n'])} | {fmt(row['known_mapping_match_rate'])} | {int(row['pattern_separates_outcome'])} | {fmt(row['mean_churn_event_count'])} | {fmt(row['mean_max_component_count'])} |"
        )
    lines.append("")
    lines.append("## Chain summary")
    lines.append("")
    lines.append("| pattern | n | seeds | expected | est rate | mean horizon | mean churn | mean max mass |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in chain_summary:
        lines.append(
            f"| {row['genealogy_pattern']} | {int(row['n_runs'])} | {row['seed_deltas']} | {row['v15cw_expected_from_genealogy']} | {fmt(row['established_far_shell_rate'])} | {fmt(row['mean_high_horizon_span'])} | {fmt(row['mean_churn_event_count'])} | {fmt(row['mean_max_total_defect_mass'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en holdout av en konkret genealogy-mapping, ikke en ny partikkel-, Lorentz- eller invariantpaastand.")
    lines.append("- Positivt resultat betyr bare at p1/1024-genealogien kan brukes som lokal selector under denne growth seeden.")
    lines.append("- Negativt eller ambivalent resultat betyr at genealogy fortsatt er nyttig diagnostikk, men ikke en stabil selector alene.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15cx", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Dette er en smal holdout av `1024/p1`, ikke en bred placement-search.")
    lines.append("- Ikke oppgrader resultatet til partikler, global invariant, Lorentz-likhet eller entanglement-sprak.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15cx",
        "",
        "Denne runden spurte: holder det smale genealogy-signalet vi saa i forrige runde naar vi bytter friske tilfeldige seeds?",
        "",
        f"- Scope: `{diag['holdout_scope']['status']}`.",
        f"- Holdout: `{diag['genealogy_holdout']['status']}`.",
        "",
        "Poenget er ikke aa bevise at noe er en partikkel. Poenget er aa se om skadens komponenthistorikk faktisk kan forutsi hvilke runs som faar lang hale.",
        "",
        f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cx add_chord p1/1024 genealogy holdout.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cx_p1_1024_genealogy_holdout_target_summary.csv")
    p.add_argument("--out-components-csv", type=str, default="Documentation/v15cx_p1_1024_genealogy_holdout_component_trajectories.csv")
    p.add_argument("--out-events-csv", type=str, default="Documentation/v15cx_p1_1024_genealogy_holdout_event_log.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cx_p1_1024_genealogy_holdout_runs.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cx_p1_1024_genealogy_holdout_aggregate.csv")
    p.add_argument("--out-chain-csv", type=str, default="Documentation/v15cx_p1_1024_genealogy_holdout_chain_summary.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cx_p1_1024_genealogy_holdout_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cx_p1_1024_genealogy_holdout.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cx_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cx.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    base_row = next(
        row for row in base_rows
        if int(row["growth_seed"]) == GROWTH_SEED and int(row["target_nodes"]) == TARGET_NODES
    )
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])

    component_rows: List[Dict[str, Any]] = []
    event_rows: List[Dict[str, Any]] = []
    run_rows: List[Dict[str, Any]] = []

    for seed_delta in HOLDOUT_SEED_DELTAS:
        run_seed = v15cn.run_seed_for(
            target=TARGET_NODES,
            perturbation=PERTURBATION,
            placement=PLACEMENT,
            seed_delta=seed_delta,
        )
        res = v15ae.run_defect_with_control_graphs(
            base_state,
            params=params,
            seed=run_seed,
            steps=v15cs.scaled_steps_for_target(TARGET_NODES),
            perturbation=PERTURBATION,
            center_token_index=PLACEMENT,
            local_coupling="maximal",
            log_every=LOG_EVERY,
        )
        info = dict(res["perturbation_info"])
        support = [int(x) for x in info.get("support", [])]
        support_signature = ",".join(str(x) for x in support)
        base_dist = v7.bfs_distances(base_state.g, support)
        fallback = (max(base_dist.values()) + 1) if base_dist else 1
        snapshot_rows = v15cv.snapshot_rows_for_run(
            target=TARGET_NODES,
            placement=PLACEMENT,
            seed_delta=seed_delta,
            run_seed=run_seed,
            support_signature=support_signature,
            log_rows=res["log_rows"],
            damaged_sets=res["damaged_sets"],
            control_graphs=res["control_graphs"],
            base_dist=base_dist,
            fallback=fallback,
        )
        recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
        final_drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
        support_features = v15cv.support_mechanism_features(
            target=TARGET_NODES,
            base_state=base_state,
            placement=PLACEMENT,
            seed_delta=seed_delta,
            run_seed=run_seed,
            support=support,
        )
        mechanism_row = v15cv.run_summary_row(
            target=TARGET_NODES,
            placement=PLACEMENT,
            seed_delta=seed_delta,
            run_seed=run_seed,
            requested_match=int(v15.v14.perturbation_requested_match(PERTURBATION, str(info.get("type", "unknown")))),
            support_signature=support_signature,
            support_features=support_features,
            recurrence=recurrence,
            final_drift=final_drift,
            snapshot_rows=snapshot_rows,
        )
        run_ids = {
            "target_nodes": TARGET_NODES,
            "growth_seed": GROWTH_SEED,
            "profile_label": profile_label(),
            "perturbation": PERTURBATION,
            "placement": PLACEMENT,
            "seed_delta": int(seed_delta),
            "run_seed": int(run_seed),
            "support_signature": support_signature,
        }
        comps, events, genealogy_summary = v15cw.genealogy_for_run(
            run_ids=run_ids,
            log_rows=res["log_rows"],
            damaged_sets=res["damaged_sets"],
            control_graphs=res["control_graphs"],
            support=support,
        )
        component_rows.extend(comps)
        event_rows.extend(events)
        run_rows.append({**mechanism_row, **genealogy_summary})

    run_rows = run_rows_with_holdout_fields(run_rows)
    target_summary = [
        row for row in v10e.summarize_bases(base_rows)
        if int(row["target_nodes"]) == TARGET_NODES
    ]
    aggregate = aggregate_rows(run_rows)
    chain_summary = chain_summary_rows(run_rows)
    diagnosis = diagnosis_rows(target_summary=target_summary, run_rows=run_rows, aggregate=aggregate)

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_components_csv, component_rows)
    write_csv(args.out_events_csv, event_rows)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_chain_csv, chain_summary)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            target_summary=target_summary,
            run_rows=run_rows,
            aggregate=aggregate,
            chain_summary=chain_summary,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
