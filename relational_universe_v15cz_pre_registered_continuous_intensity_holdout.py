#!/usr/bin/env python3
"""v0.15cz pre-registered continuous genealogy intensity holdout.

v15cy found a promising but post-hoc continuous genealogy-intensity signal.
This round freezes the score specification from v15cw/v15cx calibration rows
before evaluating new p1/1024/add_chord holdout runs.

Confirmatory discipline:
- score inputs are genealogy/event/mass fields only
- normalization min/max is fit on calibration rows only
- holdout rows are scored with the frozen spec
- mixed far-shell outcomes are reported separately, not half-positive in the
  primary binary AUC
"""
from __future__ import annotations

import argparse
import itertools
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15cn_p2_horizon_scale_holdout as v15cn
import relational_universe_v15cs_add_chord_p0_scale_response_holdout as v15cs
import relational_universe_v15cv_add_chord_winning_placement_mechanism_probe as v15cv
import relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split as v15cw
import relational_universe_v15cy_continuous_genealogy_intensity_synthesis as v15cy
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET_NODES = 1024
PLACEMENT = 1
PERTURBATION = "add_chord"
GROWTH_SEED = v15cv.GROWTH_SEED
LOG_EVERY = v15cv.LOG_EVERY

HOLDOUT_SEED_DELTAS = (
    8101, 8117, 8171, 8219, 8273, 8317,
    8363, 8419, 8461, 8521, 8573, 8627,
    8681, 8731, 8791, 8849, 8893, 8951,
    9001, 9059, 9113, 9167, 9221, 9281,
)

PRIMARY_SCORE = "genealogy_intensity_index"
SECONDARY_SCORES = (
    "compress_per_step",
    "first_split_earliness",
    "max_component_count_per_target",
    "churn_per_step",
    "birth_death_per_step",
)
PRIMARY_FEATURES = v15cy.INDEX_FEATURES

FORBIDDEN_SCORE_INPUTS = (
    "far_shell_horizon_label",
    "horizon_binary_established",
    "horizon_ordered",
    "high_horizon_span",
    "high_retention_rate",
    "last12_high_rate",
    "tail_mean_far_shell_share",
    "tail_mean_weighted_mean_distance",
    "lab",
    "source_scope",
    "seed_delta",
    "run_seed",
    "genealogy_pattern",
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    v15.write_csv(path, list(rows))


def profile_label() -> str:
    return f"{PERTURBATION}_p{PLACEMENT}"


def clamp01(x: float) -> float:
    if not math.isfinite(x):
        return 0.0
    return max(0.0, min(1.0, x))


def fit_score_spec(calibration_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    spec: List[Dict[str, Any]] = []
    weight = 1.0 / len(PRIMARY_FEATURES)
    for feature in PRIMARY_FEATURES:
        values = [safe_float(row[feature]) for row in calibration_rows]
        values = [x for x in values if math.isfinite(x)]
        if not values:
            raise ValueError(f"No finite calibration values for feature {feature}")
        spec.append(
            {
                "score_name": PRIMARY_SCORE,
                "feature": feature,
                "feature_min": min(values),
                "feature_max": max(values),
                "weight": weight,
                "direction": "higher_is_stronger",
                "fit_scope": "v15cw_plus_v15cx_calibration_only",
                "n_calibration_rows": len(calibration_rows),
                "is_primary_input": 1,
            }
        )
    for forbidden in FORBIDDEN_SCORE_INPUTS:
        spec.append(
            {
                "score_name": PRIMARY_SCORE,
                "feature": forbidden,
                "feature_min": "",
                "feature_max": "",
                "weight": 0.0,
                "direction": "forbidden_score_input",
                "fit_scope": "never_use_in_score",
                "n_calibration_rows": len(calibration_rows),
                "is_primary_input": 0,
            }
        )
    return spec


def apply_score_spec(row: Mapping[str, Any], spec_rows: Sequence[Mapping[str, Any]]) -> Tuple[float, Dict[str, float]]:
    score = 0.0
    components: Dict[str, float] = {}
    for spec in spec_rows:
        if int(safe_float(spec.get("is_primary_input", 0))) != 1:
            continue
        feature = str(spec["feature"])
        lo = safe_float(spec["feature_min"])
        hi = safe_float(spec["feature_max"])
        weight = safe_float(spec["weight"])
        raw = safe_float(row[feature])
        if hi <= lo:
            normalized = 0.5
        else:
            normalized = clamp01((raw - lo) / (hi - lo))
        components[feature] = normalized
        score += weight * normalized
    return score, components


def decisive_label(label: str) -> int:
    if str(label) == "established_far_shell_horizon":
        return 1
    if str(label) == "no_far_shell_horizon":
        return 0
    return -1


def pairwise_auc_for_rows(rows: Sequence[Mapping[str, Any]], metric: str) -> float:
    decisive = [row for row in rows if int(row["decisive_label"]) in (0, 1)]
    if not decisive:
        return float("nan")
    converted = [
        {**dict(row), "horizon_binary_established": int(row["decisive_label"])}
        for row in decisive
    ]
    return v15cy.pairwise_auc(converted, metric)


def exact_one_sided_rank_pvalue(rows: Sequence[Mapping[str, Any]], metric: str) -> float:
    decisive = [row for row in rows if int(row["decisive_label"]) in (0, 1)]
    labels = [int(row["decisive_label"]) for row in decisive]
    scores = [safe_float(row[metric]) for row in decisive]
    pairs = [(s, y) for s, y in zip(scores, labels) if math.isfinite(s)]
    if not pairs:
        return float("nan")
    scores = [s for s, _ in pairs]
    labels = [y for _, y in pairs]
    n = len(scores)
    n_pos = sum(labels)
    n_neg = n - n_pos
    if n_pos == 0 or n_neg == 0:
        return float("nan")

    observed_pos = {idx for idx, y in enumerate(labels) if y == 1}
    observed_u = mann_whitney_u(scores, observed_pos)
    total = 0
    ge = 0
    for combo in itertools.combinations(range(n), n_pos):
        total += 1
        u = mann_whitney_u(scores, set(combo))
        if u >= observed_u - 1e-12:
            ge += 1
    return ge / total if total else float("nan")


def mann_whitney_u(scores: Sequence[float], positive_indices: set[int]) -> float:
    u = 0.0
    n = len(scores)
    for i in positive_indices:
        for j in range(n):
            if j in positive_indices:
                continue
            if scores[i] > scores[j]:
                u += 1.0
            elif scores[i] == scores[j]:
                u += 0.5
    return u


def median_defined(values: Iterable[float]) -> float:
    vals = sorted(x for x in values if math.isfinite(x))
    if not vals:
        return float("nan")
    mid = len(vals) // 2
    if len(vals) % 2:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2.0


def load_calibration_rows() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    rows = v15cy.load_runs()
    manifest: List[Dict[str, Any]] = []
    by_source: Dict[Tuple[str, str], List[Mapping[str, Any]]] = {}
    for row in rows:
        by_source.setdefault((str(row["lab"]), str(row["source_scope"])), []).append(row)
    for (lab, scope), group in sorted(by_source.items()):
        labels = Counter(str(row["far_shell_horizon_label"]) for row in group)
        manifest.append(
            {
                "lab": lab,
                "source_scope": scope,
                "n_rows": len(group),
                "target_nodes": ";".join(sorted({str(int(row["target_nodes"])) for row in group})),
                "placements": ";".join(sorted({f"p{int(row['placement'])}" for row in group})),
                "seed_deltas": ";".join(str(int(row["seed_delta"])) for row in group),
                "horizon_labels": ";".join(f"{key}:{value}" for key, value in sorted(labels.items())),
            }
        )
    return rows, manifest


def run_single_holdout(
    *,
    base_state: Any,
    base_row: Mapping[str, Any],
    params: Any,
    seed_delta: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
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
    return comps, events, {**mechanism_row, **genealogy_summary}


def add_frozen_scores(run_rows: Sequence[Mapping[str, Any]], spec_rows: Sequence[Mapping[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    scored_rows: List[Dict[str, Any]] = []
    blind_rows: List[Dict[str, Any]] = []
    for raw in run_rows:
        enriched = v15cy.enriched_row(raw, lab="v15cz", source_scope="pre_registered_holdout")
        primary, components = apply_score_spec(enriched, spec_rows)
        label = str(enriched["far_shell_horizon_label"])
        scored = {
            **dict(raw),
            **{key: enriched[key] for key in v15cy.EVALUATED_METRICS if key in enriched},
            PRIMARY_SCORE: primary,
            "decisive_label": decisive_label(label),
            "pre_registered_primary_score": PRIMARY_SCORE,
            "mixed_excluded_from_primary_auc": int(label == "mixed_far_shell_horizon"),
        }
        for feature, value in components.items():
            scored[f"frozen_component_{feature}"] = value
        scored_rows.append(scored)
        blind_rows.append(
            {
                "target_nodes": int(enriched["target_nodes"]),
                "growth_seed": int(enriched["growth_seed"]),
                "profile_label": str(enriched["profile_label"]),
                "placement": int(enriched["placement"]),
                "seed_delta": int(enriched["seed_delta"]),
                "run_seed": int(enriched["run_seed"]),
                "support_signature": str(enriched["support_signature"]),
                PRIMARY_SCORE: primary,
                "compress_per_step": safe_float(enriched["compress_per_step"]),
                "first_split_earliness": safe_float(enriched["first_split_earliness"]),
                "max_component_count_per_target": safe_float(enriched["max_component_count_per_target"]),
                "churn_per_step": safe_float(enriched["churn_per_step"]),
                "birth_death_per_step": safe_float(enriched["birth_death_per_step"]),
            }
        )
    return scored_rows, blind_rows


def metric_score_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    decisive = [row for row in run_rows if int(row["decisive_label"]) in (0, 1)]
    established = [row for row in decisive if int(row["decisive_label"]) == 1]
    no_horizon = [row for row in decisive if int(row["decisive_label"]) == 0]
    metrics = (PRIMARY_SCORE, *SECONDARY_SCORES)
    rows: List[Dict[str, Any]] = []
    for metric in metrics:
        est_values = [safe_float(row[metric]) for row in established]
        no_values = [safe_float(row[metric]) for row in no_horizon]
        rows.append(
            {
                "metric": metric,
                "test_role": "primary" if metric == PRIMARY_SCORE else "secondary",
                "n_decisive": len(decisive),
                "n_established": len(established),
                "n_no_horizon": len(no_horizon),
                "n_mixed_excluded": sum(1 for row in run_rows if str(row["far_shell_horizon_label"]) == "mixed_far_shell_horizon"),
                "mean_established": mean_defined(est_values),
                "mean_no_horizon": mean_defined(no_values),
                "median_established": median_defined(est_values),
                "median_no_horizon": median_defined(no_values),
                "mean_delta_established_minus_no": mean_defined(est_values) - mean_defined(no_values),
                "auc_established_vs_no": pairwise_auc_for_rows(run_rows, metric),
                "exact_one_sided_p": exact_one_sided_rank_pvalue(run_rows, metric),
                "spearman_vs_horizon_span_all": v15cy.spearman_metric(run_rows, metric, "high_horizon_span"),
            }
        )
    return rows


def scope_summary_rows(run_rows: Sequence[Mapping[str, Any]], metric_scores: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    labels = Counter(str(row["far_shell_horizon_label"]) for row in run_rows)
    patterns = Counter(str(row["genealogy_pattern"]) for row in run_rows)
    primary = next(row for row in metric_scores if str(row["metric"]) == PRIMARY_SCORE)
    established = [row for row in run_rows if str(row["far_shell_horizon_label"]) == "established_far_shell_horizon"]
    no_horizon = [row for row in run_rows if str(row["far_shell_horizon_label"]) == "no_far_shell_horizon"]
    mixed = [row for row in run_rows if str(row["far_shell_horizon_label"]) == "mixed_far_shell_horizon"]
    return [
        {
            "scope": "v15cz_p1_1024_pre_registered_holdout",
            "n_scheduled": len(HOLDOUT_SEED_DELTAS),
            "n_runs": len(run_rows),
            "n_decisive": int(primary["n_decisive"]),
            "n_established": len(established),
            "n_no_horizon": len(no_horizon),
            "n_mixed": len(mixed),
            "horizon_labels": ";".join(f"{key}:{value}" for key, value in sorted(labels.items())),
            "genealogy_patterns": ";".join(f"{key}:{value}" for key, value in sorted(patterns.items())),
            "primary_auc": safe_float(primary["auc_established_vs_no"]),
            "primary_exact_p": safe_float(primary["exact_one_sided_p"]),
            "primary_mean_established": safe_float(primary["mean_established"]),
            "primary_mean_no_horizon": safe_float(primary["mean_no_horizon"]),
            "mean_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in run_rows),
            "mean_primary_score": mean_defined(safe_float(row[PRIMARY_SCORE]) for row in run_rows),
            "mean_churn_event_count": mean_defined(safe_float(row["churn_event_count"]) for row in run_rows),
            "mean_max_component_count": mean_defined(safe_float(row["max_component_count"]) for row in run_rows),
            "mean_max_total_defect_mass": mean_defined(safe_float(row["max_total_defect_mass"]) for row in run_rows),
        }
    ]


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    metric_scores: Sequence[Mapping[str, Any]],
    scope_summary: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    primary = next(row for row in metric_scores if str(row["metric"]) == PRIMARY_SCORE)
    summary = scope_summary[0]
    n_decisive = int(summary["n_decisive"])
    n_established = int(summary["n_established"])
    n_no = int(summary["n_no_horizon"])
    auc = safe_float(primary["auc_established_vs_no"])
    pval = safe_float(primary["exact_one_sided_p"])
    mean_delta = safe_float(primary["mean_delta_established_minus_no"])
    enough_decisive = n_decisive >= 20 and n_established >= 8 and n_no >= 8

    if enough_decisive and auc >= 0.75 and pval < 0.05 and mean_delta > 0:
        status = "pre_registered_intensity_supported"
        note = (
            f"Primary frozen score AUC={fmt(auc)}, p={fmt(pval)}, decisive={n_decisive}, "
            f"established={n_established}, no_horizon={n_no}."
        )
        next_step = "extend_to_p3_or_second_growth_seed"
        next_note = "Neste steg kan teste generalisering til p3/1024 eller ny growth_seed uten aa refitte score."
    elif enough_decisive and (auc <= 0.60 or mean_delta <= 0):
        status = "pre_registered_intensity_failed"
        note = (
            f"Primary frozen score holder ikke: AUC={fmt(auc)}, p={fmt(pval)}, delta={fmt(mean_delta)}."
        )
        next_step = "downgrade_genealogy_to_diagnostic_phase_coupling_next"
        next_note = "Genealogy-intensity bor nedgraderes til diagnostikk; neste observabel bor vaere timing/phase-coupling mot band-entry."
    elif enough_decisive:
        status = "pre_registered_intensity_not_confirmed"
        note = (
            f"Decisive n er nok, men confirmatory kriterier holder ikke: AUC={fmt(auc)}, p={fmt(pval)}, delta={fmt(mean_delta)}."
        )
        next_step = "treat_secondary_success_as_exploratory_only"
        next_note = "Sekundaermetrikker kan gi nye hypoteser, men primarscoren er ikke validert."
    else:
        status = "pre_registered_intensity_inconclusive_balance"
        note = (
            f"Ikke nok balansert decisive data for confirmatory test: decisive={n_decisive}, "
            f"established={n_established}, no_horizon={n_no}, mixed={int(summary['n_mixed'])}; AUC={fmt(auc)}, p={fmt(pval)}."
        )
        next_step = "run_pre_registered_extension_or_report_inconclusive"
        next_note = "Forleng bare etter den pre-registrerte balanse-regelen; ikke endre score eller metric."

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
            "diagnostic_family": "pre_registration_control",
            "status": "frozen_score_applied",
            "note": "Score-spec er fit paa v15cw/v15cx calibration rows og brukt uten refit paa v15cz holdout.",
        },
        {
            "diagnostic_family": "primary_test",
            "status": status,
            "note": note,
        },
        {"diagnostic_family": "next_step", "status": next_step, "note": next_note},
    ]


def build_report(
    *,
    spec_rows: Sequence[Mapping[str, Any]],
    calibration_manifest: Sequence[Mapping[str, Any]],
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    metric_scores: Sequence[Mapping[str, Any]],
    scope_summary: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cz: pre-registered continuous intensity holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden fryser v15cy genealogy-intensity-scoren foer nye `1024/p1/add_chord` holdout-runs evalueres.")
    lines.append("Score-input er genealogy/event/mass-felter. Horizon-felter brukes bare som downstream fasit.")
    lines.append("")
    lines.append("## Pre-registered scope")
    lines.append("")
    lines.append("| field | value |")
    lines.append("| --- | --- |")
    lines.append(f"| target | {TARGET_NODES} |")
    lines.append(f"| placement | p{PLACEMENT} |")
    lines.append(f"| perturbation | {PERTURBATION} |")
    lines.append(f"| growth seed | {GROWTH_SEED} |")
    lines.append(f"| scheduled seed deltas | {';'.join(str(x) for x in HOLDOUT_SEED_DELTAS)} |")
    lines.append(f"| primary score | {PRIMARY_SCORE} |")
    lines.append("| primary outcome | established vs no_far_shell only; mixed excluded from primary AUC |")
    lines.append("")
    lines.append("## Calibration manifest")
    lines.append("")
    lines.append("| lab | scope | n | targets | placements | labels |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for row in calibration_manifest:
        lines.append(
            f"| {row['lab']} | {row['source_scope']} | {int(row['n_rows'])} | {row['target_nodes']} | {row['placements']} | {row['horizon_labels']} |"
        )
    lines.append("")
    lines.append("## Frozen score inputs")
    lines.append("")
    lines.append("| feature | min | max | weight |")
    lines.append("| --- | --- | --- | --- |")
    for row in spec_rows:
        if int(safe_float(row.get("is_primary_input", 0))) == 1:
            lines.append(
                f"| {row['feature']} | {fmt(row['feature_min'])} | {fmt(row['feature_max'])} | {fmt(row['weight'])} |"
            )
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
    lines.append("| seed | horizon | primary score | pattern | churn | max comps | max mass |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for row in run_rows:
        lines.append(
            f"| {int(row['seed_delta'])} | {row['far_shell_horizon_label']} | {fmt(row[PRIMARY_SCORE])} | {row['genealogy_pattern']} | {int(row['churn_event_count'])} | {int(row['max_component_count'])} | {int(row['max_total_defect_mass'])} |"
        )
    lines.append("")
    lines.append("## Primary and secondary metrics")
    lines.append("")
    lines.append("| metric | role | decisive | est | no | mixed | AUC | p | delta | span rho |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in metric_scores:
        lines.append(
            f"| {row['metric']} | {row['test_role']} | {int(row['n_decisive'])} | {int(row['n_established'])} | {int(row['n_no_horizon'])} | {int(row['n_mixed_excluded'])} | {fmt(row['auc_established_vs_no'])} | {fmt(row['exact_one_sided_p'])} | {fmt(row['mean_delta_established_minus_no'])} | {fmt(row['spearman_vs_horizon_span_all'])} |"
        )
    lines.append("")
    lines.append("## Scope summary")
    lines.append("")
    row = scope_summary[0]
    lines.append(f"- labels: `{row['horizon_labels']}`")
    lines.append(f"- patterns: `{row['genealogy_patterns']}`")
    lines.append(f"- primary AUC: `{fmt(row['primary_auc'])}`")
    lines.append(f"- primary exact p: `{fmt(row['primary_exact_p'])}`")
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en pre-registrert lokal selector-test, ikke en partikkel-, invariant-, Lorentz- eller entanglement-paastand.")
    lines.append("- Sekundaermetrikker kan bare generere nye hypoteser hvis primaerscoren feiler.")
    lines.append("- Mixed outcomes er ikke halvpositive i primaertesten.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15cz", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Score ble frosset fra v15cw/v15cx foer v15cz-holdout-evaluering.")
    lines.append("- Ikke refit score, normalisering eller metric etter aa ha sett holdout-resultatet.")
    lines.append("- Ikke oppgrader dette til partikler, global invariant, Lorentz-likhet eller entanglement.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15cz",
        "",
        "Denne runden gjorde en strengere test: vi bestemte paa forhaand hvordan vi skulle score skadehistorien, og saa testet vi nye runs uten aa endre scoren.",
        "",
        f"- Pre-registrering: `{diag['pre_registration_control']['status']}`.",
        f"- Primartest: `{diag['primary_test']['status']}`.",
        "",
        "Dette handler ikke om aa bevise partikler eller fysikklover. Det handler om aa se om et lokalt skademaal faktisk kan forutsi hvilke runs som faar lang hale.",
        "",
        f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cz pre-registered continuous genealogy intensity holdout.")
    p.add_argument("--out-score-spec-csv", type=str, default="Documentation/v15cz_pre_registered_continuous_intensity_holdout_score_spec.csv")
    p.add_argument("--out-calibration-csv", type=str, default="Documentation/v15cz_pre_registered_continuous_intensity_holdout_calibration_manifest.csv")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cz_pre_registered_continuous_intensity_holdout_target_summary.csv")
    p.add_argument("--out-components-csv", type=str, default="Documentation/v15cz_pre_registered_continuous_intensity_holdout_component_trajectories.csv")
    p.add_argument("--out-events-csv", type=str, default="Documentation/v15cz_pre_registered_continuous_intensity_holdout_event_log.csv")
    p.add_argument("--out-blind-scores-csv", type=str, default="Documentation/v15cz_pre_registered_continuous_intensity_holdout_blind_scores.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cz_pre_registered_continuous_intensity_holdout_runs.csv")
    p.add_argument("--out-metric-csv", type=str, default="Documentation/v15cz_pre_registered_continuous_intensity_holdout_metric_scores.csv")
    p.add_argument("--out-scope-csv", type=str, default="Documentation/v15cz_pre_registered_continuous_intensity_holdout_scope_summary.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cz_pre_registered_continuous_intensity_holdout_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cz_pre_registered_continuous_intensity_holdout.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cz_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cz.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    calibration_rows, calibration_manifest = load_calibration_rows()
    spec_rows = fit_score_spec(calibration_rows)

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
    raw_run_rows: List[Dict[str, Any]] = []

    for seed_delta in HOLDOUT_SEED_DELTAS:
        comps, events, row = run_single_holdout(
            base_state=base_state,
            base_row=base_row,
            params=params,
            seed_delta=int(seed_delta),
        )
        component_rows.extend(comps)
        event_rows.extend(events)
        raw_run_rows.append(row)

    run_rows, blind_scores = add_frozen_scores(raw_run_rows, spec_rows)
    metric_scores = metric_score_rows(run_rows)
    scope_summary = scope_summary_rows(run_rows, metric_scores)
    target_summary = [
        row for row in v10e.summarize_bases(base_rows)
        if int(row["target_nodes"]) == TARGET_NODES
    ]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        metric_scores=metric_scores,
        scope_summary=scope_summary,
    )

    write_csv(args.out_score_spec_csv, spec_rows)
    write_csv(args.out_calibration_csv, calibration_manifest)
    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_components_csv, component_rows)
    write_csv(args.out_events_csv, event_rows)
    write_csv(args.out_blind_scores_csv, blind_scores)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_metric_csv, metric_scores)
    write_csv(args.out_scope_csv, scope_summary)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            spec_rows=spec_rows,
            calibration_manifest=calibration_manifest,
            target_summary=target_summary,
            run_rows=run_rows,
            metric_scores=metric_scores,
            scope_summary=scope_summary,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")


if __name__ == "__main__":
    main()
