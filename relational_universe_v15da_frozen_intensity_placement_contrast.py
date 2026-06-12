#!/usr/bin/env python3
"""v0.15da frozen intensity placement contrast.

v15cz showed that 1024:p1/add_chord is mostly a positive far-shell-horizon
pocket, leaving the frozen genealogy-intensity selector under-balanced.
This round keeps the v15cz score spec frozen and runs a fresh placement
contrast:

- p1 as fresh positive anchor
- p0 and p2 as weak/negative controls suggested by the prior placement map
- no score refit, no renormalization, no feature changes
"""
from __future__ import annotations

import argparse
import csv
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
import relational_universe_v15cz_pre_registered_continuous_intensity_holdout as v15cz
import relational_universe_v15q_single_defect_recurrence_lab as v15q


DOC = Path("Documentation")

TARGET_NODES = 1024
GROWTH_SEED = v15cv.GROWTH_SEED
PERTURBATION = "add_chord"
PLACEMENTS = (0, 1, 2)
POSITIVE_ANCHOR_PLACEMENT = 1
WEAK_CONTROL_PLACEMENTS = (0, 2)
LOG_EVERY = v15cv.LOG_EVERY

FRESH_SEED_DELTAS = (
    9341, 9391, 9433, 9479, 9533, 9587,
    9631, 9677, 9733, 9781, 9833, 9887,
)

PRIMARY_SCORE = v15cz.PRIMARY_SCORE
SECONDARY_SCORES = v15cz.SECONDARY_SCORES
V15CZ_SCORE_SPEC = DOC / "v15cz_pre_registered_continuous_intensity_holdout_score_spec.csv"


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def median_defined(values: Iterable[float]) -> float:
    vals = sorted(x for x in values if math.isfinite(x))
    if not vals:
        return float("nan")
    mid = len(vals) // 2
    if len(vals) % 2:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2.0


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    v15.write_csv(path, list(rows))


def profile_label(placement: int) -> str:
    return f"{PERTURBATION}_p{placement}"


def decisive_label(label: str) -> int:
    return v15cz.decisive_label(label)


def run_single(
    *,
    base_state: Any,
    base_row: Mapping[str, Any],
    params: Any,
    placement: int,
    seed_delta: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    run_seed = v15cn.run_seed_for(
        target=TARGET_NODES,
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
        "placement": placement,
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
        "source_scope": f"v15da_fresh_p{placement}",
    }
    return comps, events, row


def add_frozen_scores(
    raw_rows: Sequence[Mapping[str, Any]],
    spec_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    scored_rows: List[Dict[str, Any]] = []
    blind_rows: List[Dict[str, Any]] = []
    for raw in raw_rows:
        enriched = v15cy.enriched_row(raw, lab="v15da", source_scope=str(raw["source_scope"]))
        primary, components = v15cz.apply_score_spec(enriched, spec_rows)
        label = str(enriched["far_shell_horizon_label"])
        scored = {
            **dict(raw),
            **{key: enriched[key] for key in v15cy.EVALUATED_METRICS if key in enriched},
            PRIMARY_SCORE: primary,
            "decisive_label": decisive_label(label),
            "pre_registered_primary_score": PRIMARY_SCORE,
            "mixed_excluded_from_primary_auc": int(label == "mixed_far_shell_horizon"),
            "score_source": "v15cz_frozen_spec_no_refit",
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


def pairwise_auc_for_rows(rows: Sequence[Mapping[str, Any]], metric: str) -> float:
    return v15cz.pairwise_auc_for_rows(rows, metric)


def scaled_average_ranks(scores: Sequence[float]) -> List[int]:
    indexed = sorted(enumerate(scores), key=lambda pair: pair[1])
    scaled = [0] * len(scores)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        # Average 1-based rank, scaled by 2 to keep half-ranks integral.
        avg_scaled_rank = (i + 1 + j)
        for k in range(i, j):
            scaled[indexed[k][0]] = avg_scaled_rank
        i = j
    return scaled


def exact_rank_dp_pvalue(rows: Sequence[Mapping[str, Any]], metric: str) -> Tuple[float, str, int]:
    pairs = [
        (safe_float(row[metric]), int(row["decisive_label"]))
        for row in rows
        if int(row["decisive_label"]) in (0, 1) and math.isfinite(safe_float(row[metric]))
    ]
    if not pairs:
        return float("nan"), "undefined", 0
    scores = [score for score, _ in pairs]
    labels = [label for _, label in pairs]
    n = len(scores)
    n_pos = sum(labels)
    n_neg = n - n_pos
    if n_pos == 0 or n_neg == 0:
        return float("nan"), "undefined_unbalanced", 0

    ranks2 = scaled_average_ranks(scores)
    observed_sum = sum(rank for rank, label in zip(ranks2, labels) if label == 1)
    observed_u2 = observed_sum - n_pos * (n_pos + 1)

    dp: List[Dict[int, int]] = [dict() for _ in range(n_pos + 1)]
    dp[0][0] = 1
    for rank in ranks2:
        for k in range(min(n_pos, len(ranks2)), 0, -1):
            for rank_sum, count in list(dp[k - 1].items()):
                dp[k][rank_sum + rank] = dp[k].get(rank_sum + rank, 0) + count
    ge = 0
    total = 0
    base = n_pos * (n_pos + 1)
    for rank_sum, count in dp[n_pos].items():
        total += count
        if rank_sum - base >= observed_u2:
            ge += count
    return ge / total if total else float("nan"), "exact_rank_dp", total


def metric_score_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    decisive = [row for row in run_rows if int(row["decisive_label"]) in (0, 1)]
    established = [row for row in decisive if int(row["decisive_label"]) == 1]
    no_horizon = [row for row in decisive if int(row["decisive_label"]) == 0]
    metrics = (PRIMARY_SCORE, *SECONDARY_SCORES)
    rows: List[Dict[str, Any]] = []
    for metric in metrics:
        est_values = [safe_float(row[metric]) for row in established]
        no_values = [safe_float(row[metric]) for row in no_horizon]
        p_value, p_method, p_total = exact_rank_dp_pvalue(run_rows, metric)
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
                "median_delta_established_minus_no": median_defined(est_values) - median_defined(no_values),
                "auc_established_vs_no": pairwise_auc_for_rows(run_rows, metric),
                "one_sided_p": p_value,
                "p_method": p_method,
                "p_total_assignments": p_total,
                "spearman_vs_horizon_span_all": v15cy.spearman_metric(run_rows, metric, "high_horizon_span"),
            }
        )
    return rows


def placement_summary_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    by_placement: Dict[int, List[Mapping[str, Any]]] = {}
    for row in run_rows:
        by_placement.setdefault(int(safe_float(row["placement"])), []).append(row)
    for placement, group in sorted(by_placement.items()):
        labels = Counter(str(row["far_shell_horizon_label"]) for row in group)
        patterns = Counter(str(row["genealogy_pattern"]) for row in group)
        rows.append(
            {
                "placement": f"p{placement}",
                "role": "fresh_positive_anchor" if placement == POSITIVE_ANCHOR_PLACEMENT else "fresh_weak_control",
                "source_scope": ";".join(sorted({str(row.get("source_scope", "")) for row in group})),
                "n_runs": len(group),
                "n_established": labels.get("established_far_shell_horizon", 0),
                "n_no_horizon": labels.get("no_far_shell_horizon", 0),
                "n_mixed": labels.get("mixed_far_shell_horizon", 0),
                "horizon_labels": ";".join(f"{key}:{value}" for key, value in sorted(labels.items())),
                "genealogy_patterns": ";".join(f"{key}:{value}" for key, value in sorted(patterns.items())),
                "mean_primary_score": mean_defined(safe_float(row[PRIMARY_SCORE]) for row in group),
                "median_primary_score": median_defined(safe_float(row[PRIMARY_SCORE]) for row in group),
                "mean_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group),
                "mean_churn_event_count": mean_defined(safe_float(row["churn_event_count"]) for row in group),
                "mean_max_component_count": mean_defined(safe_float(row["max_component_count"]) for row in group),
                "mean_max_total_defect_mass": mean_defined(safe_float(row["max_total_defect_mass"]) for row in group),
            }
        )
    return rows


def matched_seed_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_key: Dict[int, Dict[int, Mapping[str, Any]]] = {}
    for row in run_rows:
        seed_delta = int(safe_float(row["seed_delta"]))
        placement = int(safe_float(row["placement"]))
        by_key.setdefault(seed_delta, {})[placement] = row
    rows: List[Dict[str, Any]] = []
    for seed_delta, group in sorted(by_key.items()):
        if any(placement not in group for placement in PLACEMENTS):
            continue
        p0 = group[0]
        p1 = group[1]
        p2 = group[2]
        rows.append(
            {
                "seed_delta": seed_delta,
                "p0_label": p0["far_shell_horizon_label"],
                "p1_label": p1["far_shell_horizon_label"],
                "p2_label": p2["far_shell_horizon_label"],
                "p0_score": safe_float(p0[PRIMARY_SCORE]),
                "p1_score": safe_float(p1[PRIMARY_SCORE]),
                "p2_score": safe_float(p2[PRIMARY_SCORE]),
                "p1_minus_p0_score": safe_float(p1[PRIMARY_SCORE]) - safe_float(p0[PRIMARY_SCORE]),
                "p1_minus_p2_score": safe_float(p1[PRIMARY_SCORE]) - safe_float(p2[PRIMARY_SCORE]),
                "p0_horizon_span": safe_float(p0["high_horizon_span"]),
                "p1_horizon_span": safe_float(p1["high_horizon_span"]),
                "p2_horizon_span": safe_float(p2["high_horizon_span"]),
                "p1_pattern": p1["genealogy_pattern"],
                "p0_pattern": p0["genealogy_pattern"],
                "p2_pattern": p2["genealogy_pattern"],
            }
        )
    return rows


def scope_summary_rows(
    run_rows: Sequence[Mapping[str, Any]],
    metric_scores: Sequence[Mapping[str, Any]],
    placement_summary: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    labels = Counter(str(row["far_shell_horizon_label"]) for row in run_rows)
    primary = next(row for row in metric_scores if str(row["metric"]) == PRIMARY_SCORE)
    p1 = next(row for row in placement_summary if str(row["placement"]) == "p1")
    controls = [row for row in placement_summary if str(row["placement"]) in ("p0", "p2")]
    control_no = sum(int(row["n_no_horizon"]) for row in controls)
    control_est = sum(int(row["n_established"]) for row in controls)
    control_mixed = sum(int(row["n_mixed"]) for row in controls)
    control_mean_score = mean_defined(safe_float(row["mean_primary_score"]) for row in controls)
    return [
        {
            "scope": "v15da_fresh_p0_p1_p2_frozen_score_contrast",
            "n_seed_deltas": len(FRESH_SEED_DELTAS),
            "n_runs": len(run_rows),
            "n_decisive": int(primary["n_decisive"]),
            "n_established": int(primary["n_established"]),
            "n_no_horizon": int(primary["n_no_horizon"]),
            "n_mixed": int(primary["n_mixed_excluded"]),
            "horizon_labels": ";".join(f"{key}:{value}" for key, value in sorted(labels.items())),
            "primary_auc": safe_float(primary["auc_established_vs_no"]),
            "primary_one_sided_p": safe_float(primary["one_sided_p"]),
            "primary_p_method": primary["p_method"],
            "primary_median_delta": safe_float(primary["median_delta_established_minus_no"]),
            "primary_mean_established": safe_float(primary["mean_established"]),
            "primary_mean_no_horizon": safe_float(primary["mean_no_horizon"]),
            "p1_established": int(p1["n_established"]),
            "p1_no_horizon": int(p1["n_no_horizon"]),
            "p1_mixed": int(p1["n_mixed"]),
            "p1_mean_score": safe_float(p1["mean_primary_score"]),
            "control_established": control_est,
            "control_no_horizon": control_no,
            "control_mixed": control_mixed,
            "control_mean_score": control_mean_score,
            "p1_minus_control_mean_score": safe_float(p1["mean_primary_score"]) - control_mean_score,
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
    strict_match = min((int(safe_float(row["requested_match"])) for row in run_rows), default=0) == 1
    primary = next(row for row in metric_scores if str(row["metric"]) == PRIMARY_SCORE)
    summary = scope_summary[0]
    auc = safe_float(primary["auc_established_vs_no"])
    p_value = safe_float(primary["one_sided_p"])
    median_delta = safe_float(primary["median_delta_established_minus_no"])
    enough_balance = (
        int(summary["n_decisive"]) >= 16
        and int(summary["n_established"]) >= 8
        and int(summary["n_no_horizon"]) >= 8
    )
    negative_controls_valid = int(summary["control_no_horizon"]) >= 8

    if not negative_controls_valid:
        status = "negative_controls_invalid_or_broader_pocket"
        note = (
            f"p0/p2 gav bare {int(summary['control_no_horizon'])} no_horizon og "
            f"{int(summary['control_established'])} established; kontrollene balanserer ikke testen."
        )
        next_status = "choose_weaker_control_or_report_broader_placement_landscape"
        next_note = "Ikke refit score; finn svakere kontroll eller rapporter at add_chord-lommen er bredere enn antatt."
    elif enough_balance and auc >= 0.80 and p_value <= 0.01 and median_delta >= 0.15:
        status = "frozen_intensity_placement_contrast_supported"
        note = (
            f"Frossen v15cz-score skiller established/no_horizon: AUC={fmt(auc)}, "
            f"p={fmt(p_value)}, median_delta={fmt(median_delta)}."
        )
        next_status = "test_second_growth_seed_or_adjacent_target_without_refit"
        next_note = "Neste steg bor teste samme frosne score paa ny growth_seed eller nabotarget, ikke endre scoren."
    elif enough_balance and (auc < 0.75 or p_value > 0.05 or median_delta <= 0):
        status = "frozen_intensity_placement_contrast_failed"
        note = f"Balansen er nok, men primarscoren holder ikke: AUC={fmt(auc)}, p={fmt(p_value)}, median_delta={fmt(median_delta)}."
        next_status = "downgrade_score_to_descriptive_observable"
        next_note = "Genealogy-intensity bor da brukes deskriptivt, ikke som selector."
    elif enough_balance:
        status = "frozen_intensity_placement_contrast_promising_not_confirmed"
        note = f"Balansen er nok, men kriteriene er ikke sterke nok: AUC={fmt(auc)}, p={fmt(p_value)}, median_delta={fmt(median_delta)}."
        next_status = "report_as_promising_only"
        next_note = "Ikke oppgrader; behold som lovende, ikke validert."
    else:
        status = "contrast_inconclusive_balance"
        note = (
            f"Kontrasten gir ikke nok balansert decisive data: decisive={int(summary['n_decisive'])}, "
            f"established={int(summary['n_established'])}, no_horizon={int(summary['n_no_horizon'])}."
        )
        next_status = "extend_same_contrast_without_refit"
        next_note = "Forleng kun samme pre-registrerte kontrast hvis mer balanse trengs."

    return [
        {
            "diagnostic_family": "advisor_panel",
            "status": "remote_codex_panel_used_claude_unavailable",
            "note": "Claude CLI svarte Not logged in; to remote Codex sub-agents anbefalte frozen-score placement-kontrast. Lokale modeller ble unngatt.",
        },
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
            "status": "frozen_v15cz_score_no_refit",
            "note": "Score-spec er lastet fra v15cz-artefakten og brukt uten refit paa fresh p0/p1/p2-runs.",
        },
        {"diagnostic_family": "primary_contrast", "status": status, "note": note},
        {"diagnostic_family": "next_step", "status": next_status, "note": next_note},
    ]


def advisor_note_rows() -> List[Dict[str, Any]]:
    return [
        {
            "advisor": "Claude CLI",
            "status": "unavailable",
            "note": "Remote call attempted, but CLI returned Not logged in.",
        },
        {
            "advisor": "Codex methodology sub-agent",
            "status": "completed",
            "note": "Recommended 36 fresh 1024/add_chord runs: placements p0,p1,p2 over 12 fresh seed deltas; keep v15cz score frozen; p0/p2 as weak controls; do not include p3 as negative.",
        },
        {
            "advisor": "Codex physics/concept sub-agent",
            "status": "completed",
            "note": "Recommended capped claim threshold: clean artifacts, fresh reproducibility, >=8 positive and >=8 negative decisive outcomes, clear candidate/control gap, frozen selector validation, and no particle/Lorentz/invariant/entanglement claim.",
        },
    ]


def build_report(
    *,
    placement_summary: Sequence[Mapping[str, Any]],
    matched_rows: Sequence[Mapping[str, Any]],
    metric_scores: Sequence[Mapping[str, Any]],
    scope_summary: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15da: frozen intensity placement contrast")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden tester frossen v15cz `genealogy_intensity_index` mot en fresh placement-kontrast.")
    lines.append("Nye dynamiske runs er `1024/add_chord` for `p0`, `p1` og `p2` paa samme friske seed-deltaer.")
    lines.append("Score-spec er lastet fra v15cz og ikke refittet.")
    lines.append("")
    lines.append("## Advisor panel")
    lines.append("")
    lines.append("- Claude CLI ble forsokt, men svarte `Not logged in`.")
    lines.append("- To remote Codex-subagenter anbefalte frozen-score placement-kontrast, ikke p1-only extension.")
    lines.append("- Panelets claim-tak er lavt: hoyst `robust placement-conditioned mesoscale structure signal`, ikke partikler eller spacetime.")
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
    lines.append(f"| primary score | {PRIMARY_SCORE} |")
    lines.append("| primary outcome | established vs no_far_shell; non-decisive labels excluded |")
    lines.append("")
    lines.append("## Placement summary")
    lines.append("")
    lines.append("| placement | role | n | established | no | mixed | mean score | mean horizon | labels |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in placement_summary:
        lines.append(
            f"| {row['placement']} | {row['role']} | {int(row['n_runs'])} | {int(row['n_established'])} | {int(row['n_no_horizon'])} | {int(row['n_mixed'])} | {fmt(row['mean_primary_score'])} | {fmt(row['mean_horizon_span'])} | {row['horizon_labels']} |"
        )
    lines.append("")
    lines.append("## Primary and secondary metrics")
    lines.append("")
    lines.append("| metric | role | decisive | est | no | mixed | AUC | p | method | median delta | span rho |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in metric_scores:
        lines.append(
            f"| {row['metric']} | {row['test_role']} | {int(row['n_decisive'])} | {int(row['n_established'])} | {int(row['n_no_horizon'])} | {int(row['n_mixed_excluded'])} | {fmt(row['auc_established_vs_no'])} | {fmt(row['one_sided_p'])} | {row['p_method']} | {fmt(row['median_delta_established_minus_no'])} | {fmt(row['spearman_vs_horizon_span_all'])} |"
        )
    lines.append("")
    lines.append("## Matched seed contrast")
    lines.append("")
    lines.append("| seed | p0 label | p1 label | p2 label | p0 score | p1 score | p2 score | p1-p0 | p1-p2 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in matched_rows:
        lines.append(
            f"| {int(row['seed_delta'])} | {row['p0_label']} | {row['p1_label']} | {row['p2_label']} | {fmt(row['p0_score'])} | {fmt(row['p1_score'])} | {fmt(row['p2_score'])} | {fmt(row['p1_minus_p0_score'])} | {fmt(row['p1_minus_p2_score'])} |"
        )
    lines.append("")
    lines.append("## Scope summary")
    lines.append("")
    row = scope_summary[0]
    lines.append(f"- labels: `{row['horizon_labels']}`")
    lines.append(f"- primary AUC: `{fmt(row['primary_auc'])}`")
    lines.append(f"- primary one-sided p: `{fmt(row['primary_one_sided_p'])}` via `{row['primary_p_method']}`")
    lines.append(f"- primary median delta: `{fmt(row['primary_median_delta'])}`")
    lines.append(f"- p1 minus control mean score: `{fmt(row['p1_minus_control_mean_score'])}`")
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Hva dette kan og ikke kan vise")
    lines.append("")
    lines.append("- Positivt funn her kan styrke at frossen genealogy-intensitet skiller etablerte far-shell-runs fra no-horizon-runs i et placement-betinget add_chord-landskap.")
    lines.append("- Det beviser ikke partikler, Lorentz-likhet, entanglement, global invariant eller universell emergent geometri.")
    lines.append("- For en forsiktig `dette kan bygge univers-lignende struktur`-claim maa repoet vise flere uavhengige robuste signaler: repeterbare defects, ikke-trivielle interaksjoner, skalaoverforing, kontrollert anisotropi og minst en pre-registrert observabel som generaliserer uten refit.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15da", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke refit v15cz-scoren paa v15da.")
    lines.append("- Ikke bruk v15da til aa paasta partikler, Lorentz-likhet, entanglement eller global invariant.")
    lines.append("- Hvis kontrasten stottes, neste steg maa fortsatt vaere en ny uavhengig kontroll, ikke en claim-oppgradering.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15da",
        "",
        "Denne runden spurte et strengere sporsmal: naar vi ikke endrer scoren etterpaa, skiller den sterke p1-plasseringen seg fra svakere p0/p2-plasseringer?",
        "",
        f"- Scorekontroll: `{diag['pre_registration_control']['status']}`.",
        f"- Primarkontrast: `{diag['primary_contrast']['status']}`.",
        "",
        "Dette er fortsatt ikke en fysikklov. Det er et forsok paa aa finne ut om robuste, repeterbare struktursignaler kan bygges opp fra lokale regler.",
        "",
        f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
    ]
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15da frozen intensity placement contrast.")
    p.add_argument("--out-target-csv", default=str(DOC / "v15da_frozen_intensity_placement_contrast_target_summary.csv"))
    p.add_argument("--out-components-csv", default=str(DOC / "v15da_frozen_intensity_placement_contrast_component_trajectories.csv"))
    p.add_argument("--out-events-csv", default=str(DOC / "v15da_frozen_intensity_placement_contrast_event_log.csv"))
    p.add_argument("--out-blind-csv", default=str(DOC / "v15da_frozen_intensity_placement_contrast_blind_scores.csv"))
    p.add_argument("--out-runs-csv", default=str(DOC / "v15da_frozen_intensity_placement_contrast_runs.csv"))
    p.add_argument("--out-placement-csv", default=str(DOC / "v15da_frozen_intensity_placement_contrast_placement_summary.csv"))
    p.add_argument("--out-matched-csv", default=str(DOC / "v15da_frozen_intensity_placement_contrast_matched_seed_compare.csv"))
    p.add_argument("--out-metric-csv", default=str(DOC / "v15da_frozen_intensity_placement_contrast_metric_scores.csv"))
    p.add_argument("--out-scope-csv", default=str(DOC / "v15da_frozen_intensity_placement_contrast_scope_summary.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15da_frozen_intensity_placement_contrast_diagnosis.csv"))
    p.add_argument("--out-advisor-csv", default=str(DOC / "v15da_advisor_panel_notes.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15da_frozen_intensity_placement_contrast.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15da_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15da.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    spec_rows = read_csv(V15CZ_SCORE_SPEC)
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
    raw_rows: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        for seed_delta in FRESH_SEED_DELTAS:
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

    run_rows, blind_rows = add_frozen_scores(raw_rows, spec_rows)
    metric_scores = metric_score_rows(run_rows)
    placement_summary = placement_summary_rows(run_rows)
    matched_rows = matched_seed_rows(run_rows)
    scope_summary = scope_summary_rows(run_rows, metric_scores, placement_summary)
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

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_components_csv, component_rows)
    write_csv(args.out_events_csv, event_rows)
    write_csv(args.out_blind_csv, blind_rows)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_placement_csv, placement_summary)
    write_csv(args.out_matched_csv, matched_rows)
    write_csv(args.out_metric_csv, metric_scores)
    write_csv(args.out_scope_csv, scope_summary)
    write_csv(args.out_diagnosis_csv, diagnosis)
    write_csv(args.out_advisor_csv, advisor_note_rows())
    Path(args.out_summary_md).write_text(
        build_report(
            placement_summary=placement_summary,
            matched_rows=matched_rows,
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
