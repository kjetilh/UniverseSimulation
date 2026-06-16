#!/usr/bin/env python3
"""v0.15dh second-growth-seed boundary/mass holdout.

v15dg supported the frozen v15df strict pre-entry candidate
`w32_mean_boundary_per_mass` on fresh seed deltas at growth seed 202. This
round keeps target, perturbation, placements, budget, and metric fixed, but
moves the base growth seed to 303.

Discipline:
- no metric refit
- no route-entry/retention features
- fresh seed deltas not used by v15da/v15dg
- static support geometry reported only as confound/audit
- growth seed stamped explicitly, not inherited from v15da/v15cv constants
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15cs_add_chord_p0_scale_response_holdout as v15cs
import relational_universe_v15cv_add_chord_winning_placement_mechanism_probe as v15cv
import relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split as v15cw
import relational_universe_v15da_frozen_intensity_placement_contrast as v15da
import relational_universe_v15df_pre_entry_support_topology_synthesis as v15df
import relational_universe_v15dg_boundary_mass_holdout as v15dg
import relational_universe_v15q_single_defect_recurrence_lab as v15q


DOC = Path("Documentation")

TARGET_NODES = 1024
GROWTH_SEED = 303
PERTURBATION = "add_chord"
PLACEMENTS = (0, 1, 2)
PRIMARY_METRIC = v15dg.PRIMARY_METRIC
PRIMARY_DIRECTION = v15dg.PRIMARY_DIRECTION
STATIC_AUDIT_METRIC = v15dg.STATIC_AUDIT_METRIC
LOG_EVERY = v15da.LOG_EVERY

FRESH_SEED_DELTAS = (
    11003, 11057, 11113, 11171,
    11239, 11311, 11383, 11447,
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def profile_label(placement: int) -> str:
    return f"{PERTURBATION}_p{int(placement)}"


def run_seed_for(*, target: int, growth_seed: int, perturbation: str, placement: int, seed_delta: int) -> int:
    perturbation_offset = {"add_chord": 1913, "local_swap": 1979}[perturbation]
    return (
        int(target) * 1_000_000
        + int(growth_seed) * 10_000
        + int(placement) * 1_000
        + int(seed_delta)
        + perturbation_offset
    )


def run_single(
    *,
    base_state: Any,
    base_row: Mapping[str, Any],
    params: Any,
    placement: int,
    seed_delta: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    run_seed = run_seed_for(
        target=TARGET_NODES,
        growth_seed=GROWTH_SEED,
        perturbation=PERTURBATION,
        placement=placement,
        seed_delta=seed_delta,
    )
    res = v15ae.run_defect_with_control_graphs(
        base_state,
        params=params,
        seed=run_seed,
        steps=v15cs.scaled_steps_for_target(TARGET_NODES),
        perturbation=PERTURBATION,
        center_token_index=placement,
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
        placement=placement,
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
        placement=placement,
        seed_delta=seed_delta,
        run_seed=run_seed,
        support=support,
    )
    mechanism_row = v15cv.run_summary_row(
        target=TARGET_NODES,
        placement=placement,
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
        "profile_label": profile_label(placement),
        "perturbation": PERTURBATION,
        "placement": int(placement),
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
    row = {
        **mechanism_row,
        **genealogy_summary,
        "growth_seed": GROWTH_SEED,
        "profile_label": profile_label(placement),
        "source_scope": f"v15dh_growth_seed_{GROWTH_SEED}_p{placement}",
        "pre_registered_growth_seed_holdout": 1,
    }
    return comps, events, row


def count_rows(
    rows: Sequence[Mapping[str, Any]],
    *,
    placement: int | None = None,
    label: str | None = None,
) -> int:
    total = 0
    for row in rows:
        if placement is not None and int(safe_float(row["placement"])) != int(placement):
            continue
        if label is not None and str(row["far_shell_horizon_label"]) != label:
            continue
        total += 1
    return total


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(safe_float(row["requested_match"])) for row in run_rows), default=0) == 1
    labels: Dict[str, int] = {}
    for row in run_rows:
        labels[str(row["far_shell_horizon_label"])] = labels.get(str(row["far_shell_horizon_label"]), 0) + 1
    label_note = ";".join(f"{key}:{labels[key]}" for key in sorted(labels))

    primary = next(row for row in metric_rows if str(row["metric"]) == PRIMARY_METRIC)
    static = next(row for row in metric_rows if str(row["metric"]) == STATIC_AUDIT_METRIC)
    baseline = next(row for row in metric_rows if str(row["metric"]) == v15da.PRIMARY_SCORE)

    n_p1_est = count_rows(run_rows, placement=1, label="established_far_shell_horizon")
    n_p1_no = count_rows(run_rows, placement=1, label="no_far_shell_horizon")
    n_p0_est = count_rows(run_rows, placement=0, label="established_far_shell_horizon")
    n_p2_est = count_rows(run_rows, placement=2, label="established_far_shell_horizon")
    n_p0_false = int(primary["n_p0_high_score_no_horizon"])
    auc_all = safe_float(primary["auc_established_vs_no"])
    static_auc_all = safe_float(static["auc_established_vs_no"])
    baseline_auc_all = safe_float(baseline["auc_established_vs_no"])

    if n_p1_est == 0 and (n_p0_est + n_p2_est) > 0:
        landscape_status = "growth_seed_303_placement_landscape_changed"
        landscape_note = (
            f"p1 har {n_p1_no}/{len(FRESH_SEED_DELTAS)} no-horizon og 0 established, "
            f"mens p0 har {n_p0_est} established og p2 har {n_p2_est} established."
        )
    else:
        landscape_status = "growth_seed_303_same_anchor_possible"
        landscape_note = (
            f"p1-established={n_p1_est}, p1-no-horizon={n_p1_no}, "
            f"p0-established={n_p0_est}, p2-established={n_p2_est}."
        )

    if n_p1_est == 0 and auc_all < 0.55:
        primary_status = "boundary_mass_not_growth_seed_transferable_under_original_anchor"
        primary_note = (
            f"`{PRIMARY_METRIC}` har AUC={fmt(auc_all)} established-vs-no, "
            "og den opprinnelige p1-positive kontrasten finnes ikke paa growth seed 303."
        )
    elif n_p1_est >= 4 and n_p0_false >= 3 and safe_float(primary["auc_p1_established_vs_p0_false_positive"]) >= 0.80:
        primary_status = "boundary_mass_growth_seed_transfer_supported"
        primary_note = (
            f"`{PRIMARY_METRIC}` har AUC={fmt(primary['auc_p1_established_vs_p0_false_positive'])} "
            "mot p0 false positives med balansert p1-anchor."
        )
    else:
        primary_status = "boundary_mass_growth_seed_holdout_inconclusive_balance"
        primary_note = (
            f"`{PRIMARY_METRIC}` har AUC={fmt(auc_all)} established-vs-no; "
            f"p1-established={n_p1_est}, p0-high-score/no-horizon={n_p0_false}."
        )

    if static_auc_all < 0.50:
        static_status = "static_support_not_transferable_as_selector"
        static_note = (
            f"`{STATIC_AUDIT_METRIC}` har AUC={fmt(static_auc_all)} established-vs-no; "
            "supportgeometrien er fortsatt viktig, men retningen fra v15dg transferer ikke som selector."
        )
    else:
        static_status = "static_support_reported_not_primary"
        static_note = (
            f"`{STATIC_AUDIT_METRIC}` har AUC={fmt(static_auc_all)} established-vs-no "
            "og rapporteres som placement/support-audit, ikke dynamisk selector."
        )

    if baseline_auc_all >= 0.80:
        baseline_status = "genealogy_intensity_correlates_overall_not_primary"
        baseline_note = (
            f"Baseline genealogy-intensity har AUC={fmt(baseline_auc_all)} established-vs-no, "
            "men er ikke den pre-registrerte primary selector her og skal ikke refittes til claim."
        )
    else:
        baseline_status = "genealogy_intensity_control"
        baseline_note = f"Baseline genealogy-intensity har AUC={fmt(baseline_auc_all)} established-vs-no."

    next_status = "compare_growth_seed_support_signatures_before_more_dynamics"
    next_note = (
        "Neste steg bor vaere en no-new-dynamics syntese av v15dg/v15dh som sammenligner "
        "base/support-signaturer og placement-respons, foer mer label-budget brukes."
    )

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelse er ren og requested add_chord-perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Startstorrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        },
        {
            "diagnostic_family": "pre_registration",
            "status": "frozen_w32_boundary_mass_no_refit",
            "note": (
                f"Primarmetric er frosset til `{PRIMARY_METRIC}` fra v15df/v15dg; "
                f"growth seed er endret til {GROWTH_SEED}, og route-entry brukes ikke som feature."
            ),
        },
        {
            "diagnostic_family": "outcome_balance",
            "status": "holdout_label_balance_anchor_changed",
            "note": (
                f"Labels: {label_note}; p1-established={n_p1_est}, "
                f"p1-no-horizon={n_p1_no}, p0-established={n_p0_est}, p2-established={n_p2_est}."
            ),
        },
        {
            "diagnostic_family": "placement_landscape",
            "status": landscape_status,
            "note": landscape_note,
        },
        {
            "diagnostic_family": "primary_result",
            "status": primary_status,
            "note": primary_note,
        },
        {
            "diagnostic_family": "static_confound_audit",
            "status": static_status,
            "note": static_note,
        },
        {
            "diagnostic_family": "baseline_check",
            "status": baseline_status,
            "note": baseline_note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_status,
            "note": next_note,
        },
    ]


def build_report(
    *,
    group_rows: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
    matched_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dh: boundary/mass growth-seed holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er en second-growth-seed holdout av v15df/v15dg-kandidaten.")
    lines.append(f"Primarmetric er fortsatt frosset til `{PRIMARY_METRIC}` med retning `{PRIMARY_DIRECTION}`.")
    lines.append("Target, perturbation, placements og budget holdes fast fra v15dg.")
    lines.append("Growth seed flyttes fra 202 til 303.")
    lines.append("Statisk supportgeometri rapporteres bare som confound/audit.")
    lines.append("Route-entry/retention brukes ikke som candidate feature.")
    lines.append("")
    lines.append("## Pre-registered scope")
    lines.append("")
    lines.append("| field | value |")
    lines.append("| --- | --- |")
    lines.append(f"| target | {TARGET_NODES} |")
    lines.append(f"| growth seed | {GROWTH_SEED} |")
    lines.append(f"| perturbation | {PERTURBATION} |")
    lines.append(f"| placements | {';'.join(f'p{x}' for x in PLACEMENTS)} |")
    lines.append(f"| seed deltas | {';'.join(str(x) for x in FRESH_SEED_DELTAS)} |")
    lines.append(f"| primary metric | {PRIMARY_METRIC} |")
    lines.append(f"| static audit | {STATIC_AUDIT_METRIC} |")
    lines.append("")
    lines.append("## Group summary")
    lines.append("")
    lines.append("| group | n | placements | labels | boundary/mass | static degree | genealogy intensity | mean horizon |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in group_rows:
        lines.append(
            f"| {row['analysis_group']} | {int(row['n_runs'])} | {row['placements']} | {row['labels']} | "
            f"{fmt(row['median_boundary_mass'])} | {fmt(row['median_static_support_degree'])} | "
            f"{fmt(row['median_genealogy_intensity'])} | {fmt(row['mean_horizon_span'])} |"
        )
    lines.append("")
    lines.append("## Metric scores")
    lines.append("")
    lines.append("| metric | role | AUC est/no | AUC p1/p0 false | AUC p1/p2 no | median p1 | median p0 false | median p2 no |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in metric_rows:
        lines.append(
            f"| {row['metric']} | {row['role']} | {fmt(row['auc_established_vs_no'])} | "
            f"{fmt(row['auc_p1_established_vs_p0_false_positive'])} | "
            f"{fmt(row['auc_p1_established_vs_p2_no_horizon'])} | "
            f"{fmt(row['median_p1_established_raw'])} | {fmt(row['median_p0_false_positive_raw'])} | "
            f"{fmt(row['median_p2_no_horizon_raw'])} |"
        )
    lines.append("")
    lines.append("## Matched seed comparison")
    lines.append("")
    lines.append("| seed | p0 label | p1 label | p2 label | p0 group | p1 group | p2 group | p0 bm | p1 bm | p2 bm | p1-p0 | p1-p2 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in matched_rows:
        lines.append(
            f"| {int(row['seed_delta'])} | {row['p0_label']} | {row['p1_label']} | {row['p2_label']} | "
            f"{row['p0_analysis_group']} | {row['p1_analysis_group']} | {row['p2_analysis_group']} | "
            f"{fmt(row['p0_boundary_mass'])} | {fmt(row['p1_boundary_mass'])} | {fmt(row['p2_boundary_mass'])} | "
            f"{fmt(row['p1_minus_p0_boundary_mass'])} | {fmt(row['p1_minus_p2_boundary_mass'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette tester base-state-transfer for en lokal pre-entry observabel; det kan ikke bevise partikler, Lorentz-likhet, entanglement eller global invariant.")
    lines.append("- Hvis support-audit fortsatt skiller renere enn dynamikken, er support-confound fortsatt live.")
    lines.append("- Hvis boundary/mass faller paa ny growth seed, skal kandidaten nedgraderes til growth-seed-spesifikk observabel.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15dh", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke refit `w32_mean_boundary_per_mass` etter denne holdouten.")
    lines.append("- Ikke bruk statisk supportgeometri som dynamisk selector.")
    lines.append("- Ikke oppgrader til invariant/Lorentz/partikkel/entanglement-claim.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15dh",
            "",
            "Denne runden testet om samme tidlige form-maaling holder naar startgrafen bygges fra en annen growth seed.",
            "",
            "Det viktige er at maalet ikke ble justert etter resultatene.",
            "",
            f"- Hovedlesning: `{diag['primary_result']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Dette er fortsatt en lokal observabel-test, ikke en paastand om en fysikklov.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15dh second-growth-seed boundary/mass holdout.")
    p.add_argument("--reuse-existing", action="store_true", help="Regenerate aggregate/report files from existing v15dh CSV outputs.")
    p.add_argument("--out-target-csv", default=str(DOC / "v15dh_boundary_mass_target_summary.csv"))
    p.add_argument("--out-components-csv", default=str(DOC / "v15dh_boundary_mass_component_trajectories.csv"))
    p.add_argument("--out-events-csv", default=str(DOC / "v15dh_boundary_mass_event_log.csv"))
    p.add_argument("--out-blind-csv", default=str(DOC / "v15dh_boundary_mass_blind_scores.csv"))
    p.add_argument("--out-runs-csv", default=str(DOC / "v15dh_boundary_mass_run_features.csv"))
    p.add_argument("--out-groups-csv", default=str(DOC / "v15dh_boundary_mass_group_summary.csv"))
    p.add_argument("--out-matched-csv", default=str(DOC / "v15dh_boundary_mass_matched_seed_compare.csv"))
    p.add_argument("--out-metrics-csv", default=str(DOC / "v15dh_boundary_mass_metric_scores.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15dh_boundary_mass_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15dh_boundary_mass_growth_seed_holdout.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15dh_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15dh.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.reuse_existing:
        run_rows = read_csv(args.out_runs_csv)
        blind_rows = read_csv(args.out_blind_csv)
        component_rows = read_csv(args.out_components_csv)
        event_rows = read_csv(args.out_events_csv)
        target_summary = read_csv(args.out_target_csv)
    else:
        spec_rows = read_csv(v15da.V15CZ_SCORE_SPEC)
        regime = v10e.recommended_regime("fast_balanced")
        ensembles = v15.deep_ensembles([TARGET_NODES])
        base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
        base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
        base_row = next(
            row for row in base_rows
            if int(row["growth_seed"]) == GROWTH_SEED and int(row["target_nodes"]) == TARGET_NODES
        )
        params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])

        component_rows = []
        event_rows = []
        raw_rows: List[Dict[str, Any]] = []
        for placement in PLACEMENTS:
            for seed_delta in FRESH_SEED_DELTAS:
                print(f"running growth_seed {GROWTH_SEED} p{placement} seed_delta {seed_delta}")
                comps, events, row = run_single(
                    base_state=base_state,
                    base_row=base_row,
                    params=params,
                    placement=int(placement),
                    seed_delta=int(seed_delta),
                )
                component_rows.extend(comps)
                event_rows.extend(events)
                raw_rows.append(row)

        run_rows, blind_rows = v15dg.enrich_holdout_rows(
            raw_rows=raw_rows,
            component_rows=component_rows,
            spec_rows=spec_rows,
        )
        target_summary = [
            row for row in v10e.summarize_bases(base_rows)
            if int(row["target_nodes"]) == TARGET_NODES
        ]

    metric_rows = v15dg.metric_score_rows(run_rows)
    group_rows = v15dg.group_summary_rows(run_rows)
    matched_rows = v15dg.matched_seed_rows(run_rows)
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        metric_rows=metric_rows,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_components_csv, component_rows)
    write_csv(args.out_events_csv, event_rows)
    write_csv(args.out_blind_csv, blind_rows)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_groups_csv, group_rows)
    write_csv(args.out_matched_csv, matched_rows)
    write_csv(args.out_metrics_csv, metric_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            group_rows=group_rows,
            metric_rows=metric_rows,
            matched_rows=matched_rows,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")
    print(f"wrote {args.out_summary_md}")
    print(f"wrote {args.out_diagnosis_csv}")


if __name__ == "__main__":
    main()
