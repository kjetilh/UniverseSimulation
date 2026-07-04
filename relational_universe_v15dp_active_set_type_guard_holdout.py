#!/usr/bin/env python3
"""v0.15dp pre-registered active-set type-guard holdout.

Fresh two-growth-seed dynamic holdout for the v15do candidate generator:

    delta_return_t2(p0) >= delta_return_t2(p1) -> p0_p2
    otherwise                                      -> p1_only

Discipline:
- compute the guard from base/add_chord morphology before any dynamic run,
- write the guard CSV before the run loop,
- keep scope narrow: target 1024, add_chord, placements p0,p1,p2,
- judge active-set type after dynamics without refitting thresholds,
- keep this as a local defect/response selector test, not physics language.
"""
from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15da_frozen_intensity_placement_contrast as v15da
import relational_universe_v15dg_boundary_mass_holdout as v15dg
import relational_universe_v15dk_pre_registered_support_rank_holdout as v15dk
import relational_universe_v15dl_base_landscape_morphology_synthesis as v15dl
import relational_universe_v15dn_multi_active_landscape_synthesis as v15dn


DOC = Path("Documentation")

TARGET_NODES = 1024
GROWTH_SEEDS = (606, 707)
PERTURBATION = "add_chord"
PLACEMENTS = (0, 1, 2)
ACTIVE_ESTABLISHED_RATE = 0.50

GUARD_METRIC = "delta_return_t2"
GUARD_LEFT_PLACEMENT = 0
GUARD_RIGHT_PLACEMENT = 1
GUARD_COMPARISON = "p0_ge_p1"
GUARD_TRUE_TYPE = "p0_p2"
GUARD_FALSE_TYPE = "p1_only"
GUARD_SOURCE = "v15do_best_sorted_posthoc_rule_pre_registered_for_v15dp"

OBSERVED_TYPES = {
    "p1_only": frozenset({1}),
    "p0_p2": frozenset({0, 2}),
}

FRESH_SEED_DELTAS = (15007, 15061, 15121, 15187)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def safe_div(num: float, den: float) -> float:
    if not math.isfinite(num) or not math.isfinite(den) or den == 0.0:
        return float("nan")
    return num / den


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def median_defined(values: Iterable[float]) -> float:
    vals = sorted(x for x in (safe_float(v) for v in values) if math.isfinite(x))
    if not vals:
        return float("nan")
    mid = len(vals) // 2
    if len(vals) % 2:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2.0


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    return v15dk.read_csv(path)


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    v15dn.write_csv(Path(path), rows)


def format_set(values: Iterable[int]) -> str:
    vals = sorted(int(x) for x in values)
    return ";".join(f"p{x}" for x in vals) if vals else "none"


def set_from_label(label: str) -> set[int]:
    if not label or label == "none":
        return set()
    out: set[int] = set()
    for part in label.split(";"):
        part = part.strip()
        if part.startswith("p"):
            out.add(int(part[1:]))
    return out


def predicted_set_for_type(label: str) -> frozenset[int]:
    return OBSERVED_TYPES.get(label, frozenset())


def actual_type_for_set(active_set: frozenset[int]) -> str:
    for label, expected in OBSERVED_TYPES.items():
        if active_set == expected:
            return label
    return "other"


def build_bases() -> Tuple[Dict[int, Any], Dict[int, Mapping[str, Any]], Sequence[Mapping[str, Any]]]:
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))

    states: Dict[int, Any] = {}
    base_by_seed: Dict[int, Mapping[str, Any]] = {}
    for seed in GROWTH_SEEDS:
        states[seed] = base_states[(ensembles[0].name, seed)]
        base_by_seed[seed] = next(
            row for row in base_rows
            if int(row["growth_seed"]) == seed and int(row["target_nodes"]) == TARGET_NODES
        )

    target_summary = [
        {
            **dict(row),
            "holdout_growth_seeds": ";".join(str(seed) for seed in GROWTH_SEEDS),
        }
        for row in v10e.summarize_bases(base_rows)
        if int(row["target_nodes"]) == TARGET_NODES
    ]
    return states, base_by_seed, target_summary


def morphology_rows_for_seed(base_state: Any, growth_seed: int) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        row = dict(v15dl.morphology_for_seed_placement(base_state, growth_seed, placement))
        row["guard_metric"] = GUARD_METRIC
        row["guard_comparison"] = GUARD_COMPARISON
        row["guard_source"] = GUARD_SOURCE
        rows.append(row)
    return rows


def pre_run_guard_row(morphology_rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    by_placement = {int(row["placement"]): row for row in morphology_rows}
    p0 = by_placement[GUARD_LEFT_PLACEMENT]
    p1 = by_placement[GUARD_RIGHT_PLACEMENT]
    left = safe_float(p0[GUARD_METRIC])
    right = safe_float(p1[GUARD_METRIC])
    condition = int(left >= right)
    predicted_type = GUARD_TRUE_TYPE if condition else GUARD_FALSE_TYPE
    predicted_set = predicted_set_for_type(predicted_type)
    growth_seed = int(p0["growth_seed"])
    return {
        "target_nodes": TARGET_NODES,
        "growth_seed": growth_seed,
        "perturbation": PERTURBATION,
        "guard_metric": GUARD_METRIC,
        "guard_comparison": GUARD_COMPARISON,
        "guard_condition_true": condition,
        "left_placement": f"p{GUARD_LEFT_PLACEMENT}",
        "right_placement": f"p{GUARD_RIGHT_PLACEMENT}",
        "left_value": left,
        "right_value": right,
        "margin_left_minus_right": left - right if math.isfinite(left) and math.isfinite(right) else float("nan"),
        "predicted_type": predicted_type,
        "predicted_active_placements": format_set(predicted_set),
        "guard_source": GUARD_SOURCE,
        "posthoc_warning": "candidate chosen from v15do; validation requires this fresh holdout",
        "pre_registered_before_dynamics": 1,
        "p0_support_signature": by_placement[0]["support_signature"],
        "p1_support_signature": by_placement[1]["support_signature"],
        "p2_support_signature": by_placement[2]["support_signature"],
        "p0_delta_return_t2": safe_float(by_placement[0][GUARD_METRIC]),
        "p1_delta_return_t2": safe_float(by_placement[1][GUARD_METRIC]),
        "p2_delta_return_t2": safe_float(by_placement[2][GUARD_METRIC]),
        "p0_delta_return_t4": safe_float(by_placement[0].get("delta_return_t4")),
        "p1_delta_return_t4": safe_float(by_placement[1].get("delta_return_t4")),
        "p2_delta_return_t4": safe_float(by_placement[2].get("delta_return_t4")),
        "p0_local_ball3_beta1": safe_float(by_placement[0].get("local_ball3_beta1")),
        "p1_local_ball3_beta1": safe_float(by_placement[1].get("local_ball3_beta1")),
        "p2_local_ball3_beta1": safe_float(by_placement[2].get("local_ball3_beta1")),
    }


def patch_v15dk_globals(growth_seed: int) -> None:
    v15dk.GROWTH_SEED = int(growth_seed)
    v15dk.FRESH_SEED_DELTAS = FRESH_SEED_DELTAS


def run_single(
    *,
    growth_seed: int,
    base_state: Any,
    base_row: Mapping[str, Any],
    params: Any,
    placement: int,
    seed_delta: int,
) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    patch_v15dk_globals(growth_seed)
    comps, events, row = v15dk.run_single(
        base_state=base_state,
        base_row=base_row,
        params=params,
        placement=int(placement),
        seed_delta=int(seed_delta),
    )
    out = dict(row)
    out["source_scope"] = f"v15dp_growth_seed_{growth_seed}_p{placement}"
    out["pre_registered_active_set_type_guard_holdout"] = 1
    out["pre_registered_support_rank_holdout"] = 0
    out["pre_registered_return_probability_holdout"] = 0
    out["guard_metric"] = GUARD_METRIC
    out["guard_comparison"] = GUARD_COMPARISON
    return comps, events, out


def enrich_rows_seed_aware(
    *,
    raw_rows: Sequence[Mapping[str, Any]],
    component_rows: Sequence[Mapping[str, Any]],
    spec_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    raw_by_seed: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    comps_by_seed: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in raw_rows:
        raw_by_seed[int(safe_float(row["growth_seed"]))].append(row)
    for row in component_rows:
        comps_by_seed[int(safe_float(row["growth_seed"]))].append(row)

    out_rows: List[Dict[str, Any]] = []
    blind_rows: List[Dict[str, Any]] = []
    for seed in sorted(raw_by_seed):
        scored, blind = v15dg.enrich_holdout_rows(
            raw_rows=raw_by_seed[seed],
            component_rows=comps_by_seed[seed],
            spec_rows=spec_rows,
        )
        out_rows.extend(scored)
        blind_rows.extend(blind)
    return out_rows, blind_rows


def add_pre_run_guard_fields(
    run_rows: Sequence[Mapping[str, Any]],
    guard_rows: Sequence[Mapping[str, Any]],
    morphology_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    guard_by_seed = {int(row["growth_seed"]): row for row in guard_rows}
    morph_by_seed_placement = {
        (int(row["growth_seed"]), int(row["placement"])): row
        for row in morphology_rows
    }
    out: List[Dict[str, Any]] = []
    for raw in run_rows:
        row = dict(raw)
        seed = int(safe_float(row["growth_seed"]))
        placement = int(safe_float(row["placement"]))
        guard = guard_by_seed[seed]
        morph = morph_by_seed_placement[(seed, placement)]
        row["guard_metric"] = GUARD_METRIC
        row["guard_comparison"] = GUARD_COMPARISON
        row["guard_predicted_type"] = guard["predicted_type"]
        row["guard_predicted_active_placements"] = guard["predicted_active_placements"]
        row["guard_condition_true"] = guard["guard_condition_true"]
        row["guard_left_value"] = guard["left_value"]
        row["guard_right_value"] = guard["right_value"]
        row["guard_margin_left_minus_right"] = guard["margin_left_minus_right"]
        row["guard_placement_predicted_active"] = int(placement in set_from_label(str(guard["predicted_active_placements"])))
        for field in (
            GUARD_METRIC,
            "delta_return_t4",
            "delta_return_t6",
            "base_return_spectral_dim_proxy",
            "post_return_spectral_dim_proxy",
            "local_ball3_beta1",
            "local_ball3_boundary_to_volume",
            "support_ball3_minus_ball1",
            "support_ball3_minus_ball2",
            "new_edge_mean_forman",
        ):
            row[field] = morph.get(field, "")
        out.append(row)
    return out


def placement_summary_rows(
    run_rows: Sequence[Mapping[str, Any]],
    guard_rows: Sequence[Mapping[str, Any]],
    morphology_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    guard_by_seed = {int(row["growth_seed"]): row for row in guard_rows}
    morph_by_seed_placement = {
        (int(row["growth_seed"]), int(row["placement"])): row
        for row in morphology_rows
    }
    grouped: Dict[Tuple[int, int], List[Mapping[str, Any]]] = defaultdict(list)
    for row in run_rows:
        grouped[(int(safe_float(row["growth_seed"])), int(safe_float(row["placement"])))].append(row)

    out: List[Dict[str, Any]] = []
    for (seed, placement), group in sorted(grouped.items()):
        counts = Counter(str(row["far_shell_horizon_label"]) for row in group)
        n = len(group)
        established_rate = counts.get("established_far_shell_horizon", 0) / max(1, n)
        guard = guard_by_seed[seed]
        morph = morph_by_seed_placement[(seed, placement)]
        out.append(
            {
                "growth_seed": seed,
                "placement": placement,
                "support_signature": morph["support_signature"],
                "guard_metric": GUARD_METRIC,
                "guard_metric_value": safe_float(morph[GUARD_METRIC]),
                "guard_predicted_type": guard["predicted_type"],
                "guard_predicted_active_placements": guard["predicted_active_placements"],
                "guard_placement_predicted_active": int(placement in set_from_label(str(guard["predicted_active_placements"]))),
                "n_runs": n,
                "label_counts": ";".join(f"{key}:{counts[key]}" for key in sorted(counts)),
                "established_rate": established_rate,
                "active_placement": int(established_rate >= ACTIVE_ESTABLISHED_RATE),
                "mixed_rate": counts.get("mixed_far_shell_horizon", 0) / max(1, n),
                "no_horizon_rate": counts.get("no_far_shell_horizon", 0) / max(1, n),
                "mean_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group),
                "median_boundary_mass": median_defined(safe_float(row.get(v15dg.PRIMARY_METRIC)) for row in group),
                "median_genealogy_intensity": median_defined(safe_float(row.get(v15da.PRIMARY_SCORE)) for row in group),
            }
        )
    return out


def seed_evaluation_rows(
    placement_rows: Sequence[Mapping[str, Any]],
    guard_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    guard_by_seed = {int(row["growth_seed"]): row for row in guard_rows}
    rows_by_seed: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in placement_rows:
        rows_by_seed[int(row["growth_seed"])].append(row)

    out: List[Dict[str, Any]] = []
    for seed, group in sorted(rows_by_seed.items()):
        active_set = frozenset(
            int(row["placement"])
            for row in group
            if int(safe_float(row["active_placement"])) == 1
        )
        guard = guard_by_seed[seed]
        predicted_type = str(guard["predicted_type"])
        predicted_set = set(predicted_set_for_type(predicted_type))
        actual_set = set(active_set)
        captured = actual_set & predicted_set
        false_positive = predicted_set - actual_set
        missed = actual_set - predicted_set
        actual_type = actual_type_for_set(active_set)
        out.append(
            {
                "growth_seed": seed,
                "actual_type": actual_type,
                "actual_active_placements": format_set(actual_set),
                "predicted_type": predicted_type,
                "predicted_active_placements": format_set(predicted_set),
                "type_hit": int(actual_type == predicted_type),
                "exact_set_match": int(actual_set == predicted_set),
                "captured_placements": format_set(captured),
                "missed_placements": format_set(missed),
                "false_positive_placements": format_set(false_positive),
                "coverage_fraction": safe_div(len(captured), len(actual_set)),
                "precision_fraction": safe_div(len(captured), len(predicted_set)),
                "burden_fraction": safe_div(len(predicted_set), len(PLACEMENTS)),
                "placement_rates": ";".join(
                    f"p{int(row['placement'])}:{fmt(row['established_rate'])}"
                    for row in sorted(group, key=lambda x: int(x["placement"]))
                ),
                "guard_margin_left_minus_right": safe_float(guard["margin_left_minus_right"]),
                "guard_left_value": safe_float(guard["left_value"]),
                "guard_right_value": safe_float(guard["right_value"]),
            }
        )
    return out


def aggregate_evaluation_rows(seed_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    total_active = 0
    total_predicted = 0
    total_captured = 0
    total_false_positive = 0
    total_missed = 0
    type_hits = 0
    exact = 0
    for row in seed_rows:
        actual = set_from_label(str(row["actual_active_placements"]))
        predicted = set_from_label(str(row["predicted_active_placements"]))
        captured = set_from_label(str(row["captured_placements"]))
        false_positive = set_from_label(str(row["false_positive_placements"]))
        missed = set_from_label(str(row["missed_placements"]))
        total_active += len(actual)
        total_predicted += len(predicted)
        total_captured += len(captured)
        total_false_positive += len(false_positive)
        total_missed += len(missed)
        type_hits += int(safe_float(row["type_hit"]))
        exact += int(safe_float(row["exact_set_match"]))

    seed_count = len(seed_rows)
    return [
        {
            "key": "guard_rule",
            "value": f"{GUARD_METRIC}/{GUARD_COMPARISON}->true={GUARD_TRUE_TYPE};false={GUARD_FALSE_TYPE}",
            "evidence": GUARD_SOURCE,
        },
        {
            "key": "seed_count",
            "value": seed_count,
            "evidence": ";".join(str(row["growth_seed"]) for row in seed_rows),
        },
        {
            "key": "type_accuracy",
            "value": fmt(safe_div(type_hits, seed_count)),
            "evidence": f"type_hits={type_hits}; seed_count={seed_count}",
        },
        {
            "key": "exact_set_match_rate",
            "value": fmt(safe_div(exact, seed_count)),
            "evidence": f"exact_matches={exact}; seed_count={seed_count}",
        },
        {
            "key": "coverage_fraction",
            "value": fmt(safe_div(total_captured, total_active)),
            "evidence": f"captured={total_captured}; active={total_active}; missed={total_missed}",
        },
        {
            "key": "precision_fraction",
            "value": fmt(safe_div(total_captured, total_predicted)),
            "evidence": f"captured={total_captured}; predicted={total_predicted}; false_positive={total_false_positive}",
        },
        {
            "key": "burden_fraction",
            "value": fmt(safe_div(total_predicted, seed_count * len(PLACEMENTS))),
            "evidence": f"predicted={total_predicted}; possible={seed_count * len(PLACEMENTS)}",
        },
        {
            "key": "guard_status",
            "value": guard_status(seed_rows),
            "evidence": "fresh two-growth-seed active-set type holdout; no refit after dynamics",
        },
    ]


def guard_status(seed_rows: Sequence[Mapping[str, Any]]) -> str:
    if not seed_rows:
        return "guard_failed_no_rows"
    actual_types = {str(row["actual_type"]) for row in seed_rows}
    if "other" in actual_types:
        return "guard_inconclusive_unobserved_active_set_type"
    exact = sum(int(safe_float(row["exact_set_match"])) for row in seed_rows)
    type_hits = sum(int(safe_float(row["type_hit"])) for row in seed_rows)
    if exact == len(seed_rows):
        return "type_guard_supported_small_holdout"
    if type_hits == len(seed_rows):
        return "type_guard_type_hit_but_set_mismatch"
    if type_hits > 0:
        return "type_guard_partial_not_selector_grade"
    return "type_guard_not_supported"


def group_summary_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["analysis_group"])].append(row)
    out: List[Dict[str, Any]] = []
    for group, group_rows in sorted(grouped.items()):
        labels = Counter(str(row["far_shell_horizon_label"]) for row in group_rows)
        placements = Counter(f"p{int(safe_float(row['placement']))}" for row in group_rows)
        seeds = Counter(str(int(safe_float(row["growth_seed"]))) for row in group_rows)
        out.append(
            {
                "analysis_group": group,
                "n_runs": len(group_rows),
                "growth_seeds": ";".join(f"{k}:{v}" for k, v in sorted(seeds.items())),
                "placements": ";".join(f"{k}:{v}" for k, v in sorted(placements.items())),
                "labels": ";".join(f"{k}:{v}" for k, v in sorted(labels.items())),
                "median_boundary_mass": median_defined(safe_float(row[v15dg.PRIMARY_METRIC]) for row in group_rows),
                "median_static_support_degree": median_defined(safe_float(row[v15dg.STATIC_AUDIT_METRIC]) for row in group_rows),
                "median_genealogy_intensity": median_defined(safe_float(row[v15da.PRIMARY_SCORE]) for row in group_rows),
                "mean_horizon_span": mean_defined(safe_float(row["high_horizon_span"]) for row in group_rows),
            }
        )
    return out


def matched_seed_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_seed_delta: Dict[Tuple[int, int], Dict[int, Mapping[str, Any]]] = defaultdict(dict)
    for row in rows:
        key = (int(safe_float(row["growth_seed"])), int(safe_float(row["seed_delta"])))
        by_seed_delta[key][int(safe_float(row["placement"]))] = row

    out: List[Dict[str, Any]] = []
    for (growth_seed, seed_delta), group in sorted(by_seed_delta.items()):
        if any(p not in group for p in PLACEMENTS):
            continue
        p0, p1, p2 = group[0], group[1], group[2]
        out.append(
            {
                "growth_seed": growth_seed,
                "seed_delta": seed_delta,
                "guard_predicted_type": p0.get("guard_predicted_type", ""),
                "guard_predicted_active_placements": p0.get("guard_predicted_active_placements", ""),
                "p0_label": p0["far_shell_horizon_label"],
                "p1_label": p1["far_shell_horizon_label"],
                "p2_label": p2["far_shell_horizon_label"],
                "p0_analysis_group": p0["analysis_group"],
                "p1_analysis_group": p1["analysis_group"],
                "p2_analysis_group": p2["analysis_group"],
                "p0_boundary_mass": safe_float(p0[v15dg.PRIMARY_METRIC]),
                "p1_boundary_mass": safe_float(p1[v15dg.PRIMARY_METRIC]),
                "p2_boundary_mass": safe_float(p2[v15dg.PRIMARY_METRIC]),
                "p0_genealogy_intensity": safe_float(p0[v15da.PRIMARY_SCORE]),
                "p1_genealogy_intensity": safe_float(p1[v15da.PRIMARY_SCORE]),
                "p2_genealogy_intensity": safe_float(p2[v15da.PRIMARY_SCORE]),
            }
        )
    return out


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    seed_eval: Sequence[Mapping[str, Any]],
    aggregate_eval: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(safe_float(row["requested_match"])) for row in run_rows), default=0) == 1
    labels = Counter(str(row["far_shell_horizon_label"]) for row in run_rows)
    actual_types = Counter(str(row["actual_type"]) for row in seed_eval)
    guard = next(row for row in aggregate_eval if row["key"] == "guard_status")
    exact = next(row for row in aggregate_eval if row["key"] == "exact_set_match_rate")
    type_acc = next(row for row in aggregate_eval if row["key"] == "type_accuracy")
    coverage = next(row for row in aggregate_eval if row["key"] == "coverage_fraction")
    precision = next(row for row in aggregate_eval if row["key"] == "precision_fraction")
    primary_dynamic = next(row for row in metric_rows if str(row["metric"]) == v15dg.PRIMARY_METRIC)

    if guard["value"] == "type_guard_supported_small_holdout":
        next_status = "replicate_frozen_type_guard_or_increase_seed_count"
        next_note = (
            "Guarden traff begge fresh seeds, men n=2 er fortsatt lite; neste runde bor bruke samme frosne guard "
            "paa flere growth seeds foer selector-sprak."
        )
    elif guard["value"] == "type_guard_inconclusive_unobserved_active_set_type":
        next_status = "extend_type_taxonomy_before_guard_judgement"
        next_note = "Holdouten ga en aktiv-sett-type utenfor p1_only/p0_p2; guarden kan ikke vurderes uten type-utvidelse."
    else:
        next_status = "retire_this_type_guard_as_selector_candidate"
        next_note = "Den frosne v15do-guarden traff ikke godt nok; ikke refit samme regel etter outcome."

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
            "status": "type_guard_written_before_dynamics",
            "note": (
                f"Guard er frosset til `{GUARD_METRIC}/{GUARD_COMPARISON}` -> `{GUARD_TRUE_TYPE}` "
                f"ellers `{GUARD_FALSE_TYPE}`, og pre-run CSV skrives foer dynamikk-loop."
            ),
        },
        {
            "diagnostic_family": "outcome_balance",
            "status": "fresh_growth_seed_label_balance_recorded",
            "note": (
                f"Run labels: {';'.join(f'{k}:{v}' for k, v in sorted(labels.items()))}. "
                f"Actual seed types: {';'.join(f'{k}:{v}' for k, v in sorted(actual_types.items()))}."
            ),
        },
        {
            "diagnostic_family": "type_guard_result",
            "status": str(guard["value"]),
            "note": (
                f"type_accuracy={type_acc['value']}; exact_set_match={exact['value']}; "
                f"coverage={coverage['value']}; precision={precision['value']}."
            ),
        },
        {
            "diagnostic_family": "dynamic_boundary_mass_audit",
            "status": "reported_descriptive_not_primary_selector",
            "note": f"`{v15dg.PRIMARY_METRIC}` AUC established-vs-no={fmt(primary_dynamic['auc_established_vs_no'])}.",
        },
        {
            "diagnostic_family": "next_step",
            "status": next_status,
            "note": next_note,
        },
    ]


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        vals = []
        for field in fields:
            val = row.get(field, "")
            vals.append(fmt(val) if isinstance(val, float) else str(val))
        lines.append("| " + " | ".join(vals) + " |")
    return lines


def build_report(
    *,
    guard_rows: Sequence[Mapping[str, Any]],
    placement_rows: Sequence[Mapping[str, Any]],
    seed_eval: Sequence[Mapping[str, Any]],
    aggregate_eval: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dp: active-set type-guard holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er en fresh two-growth-seed holdout av en enkelt frossen v15do type-guard.")
    lines.append("Guarden beregnes fra basegraf/add_chord-probe foer dynamikk og skrives til CSV foer run-loop.")
    lines.append("Dynamiske observabler brukes til evaluering/audit, ikke til refit av guarden.")
    lines.append("")
    lines.append("## Pre-registered scope")
    lines.append("")
    lines.extend(
        table(
            [
                {"field": "target", "value": TARGET_NODES},
                {"field": "growth_seeds", "value": ";".join(str(seed) for seed in GROWTH_SEEDS)},
                {"field": "perturbation", "value": PERTURBATION},
                {"field": "placements", "value": ";".join(f"p{x}" for x in PLACEMENTS)},
                {"field": "seed_deltas", "value": ";".join(str(x) for x in FRESH_SEED_DELTAS)},
                {"field": "guard", "value": f"{GUARD_METRIC}/{GUARD_COMPARISON} -> {GUARD_TRUE_TYPE} else {GUARD_FALSE_TYPE}"},
            ],
            ("field", "value"),
        )
    )
    lines.append("")
    lines.append("## Pre-run guard")
    lines.append("")
    lines.extend(
        table(
            guard_rows,
            (
                "growth_seed",
                "left_value",
                "right_value",
                "margin_left_minus_right",
                "predicted_type",
                "predicted_active_placements",
                "p0_support_signature",
                "p1_support_signature",
                "p2_support_signature",
            ),
        )
    )
    lines.append("")
    lines.append("## Placement outcomes")
    lines.append("")
    lines.extend(
        table(
            placement_rows,
            (
                "growth_seed",
                "placement",
                "guard_metric_value",
                "guard_placement_predicted_active",
                "label_counts",
                "established_rate",
                "active_placement",
                "median_boundary_mass",
                "median_genealogy_intensity",
            ),
        )
    )
    lines.append("")
    lines.append("## Seed-level guard evaluation")
    lines.append("")
    lines.extend(
        table(
            seed_eval,
            (
                "growth_seed",
                "actual_type",
                "actual_active_placements",
                "predicted_type",
                "predicted_active_placements",
                "type_hit",
                "exact_set_match",
                "placement_rates",
            ),
        )
    )
    lines.append("")
    lines.append("## Aggregate guard evaluation")
    lines.append("")
    lines.extend(table(aggregate_eval, ("key", "value", "evidence")))
    lines.append("")
    lines.append("## Dynamic metric audit")
    lines.append("")
    lines.extend(table(metric_rows, ("metric", "role", "auc_established_vs_no", "median_established_raw", "median_no_horizon_raw")))
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en lokal defect/response holdout av en type-guard, ikke evidens for partikler, Lorentz-likhet, entanglement eller global invariant.")
    lines.append("- Treffer guarden, er det en selector-kandidat som maa replikeres paa flere seeds; den er ikke en fysikklov.")
    lines.append("- Feiler guarden, skal akkurat denne v15do-regelen pensjoneres eller nedgraderes til deskriptiv kandidatgenerator.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15dp", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke refit `delta_return_t2/p0_ge_p1` etter outcome.")
    lines.append("- Ikke generaliser fra n=2 til global selector uten replikasjon.")
    lines.append("- Ikke oppgrader til invariant/Lorentz/partikkel/entanglement-claim.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15dp",
            "",
            "Denne runden tester en regel som ble valgt foer simulasjonen starter.",
            "",
            "Regelen spoer: hvis p0 ser minst like bra ut som p1 paa en lokal return-probability-maaling, skal vi forvente at p0 og p2 blir aktive; ellers skal bare p1 bli aktiv.",
            "",
            f"- Hovedlesning: `{diag['type_guard_result']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Dette er en test av en lokal valgregel, ikke en paastand om at modellen allerede har fysisk lovmessighet.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15dp active-set type-guard holdout.")
    p.add_argument("--reuse-existing", action="store_true", help="Regenerate aggregate/report files from existing v15dp CSV outputs.")
    p.add_argument("--out-target-csv", default=str(DOC / "v15dp_active_set_type_guard_target_summary.csv"))
    p.add_argument("--out-guard-csv", default=str(DOC / "v15dp_active_set_type_guard_pre_run_guard.csv"))
    p.add_argument("--out-morphology-csv", default=str(DOC / "v15dp_active_set_type_guard_pre_run_morphology.csv"))
    p.add_argument("--out-components-csv", default=str(DOC / "v15dp_active_set_type_guard_component_trajectories.csv"))
    p.add_argument("--out-events-csv", default=str(DOC / "v15dp_active_set_type_guard_event_log.csv"))
    p.add_argument("--out-blind-csv", default=str(DOC / "v15dp_active_set_type_guard_blind_scores.csv"))
    p.add_argument("--out-runs-csv", default=str(DOC / "v15dp_active_set_type_guard_run_features.csv"))
    p.add_argument("--out-placement-csv", default=str(DOC / "v15dp_active_set_type_guard_placement_summary.csv"))
    p.add_argument("--out-seed-eval-csv", default=str(DOC / "v15dp_active_set_type_guard_seed_evaluation.csv"))
    p.add_argument("--out-eval-csv", default=str(DOC / "v15dp_active_set_type_guard_evaluation.csv"))
    p.add_argument("--out-groups-csv", default=str(DOC / "v15dp_active_set_type_guard_group_summary.csv"))
    p.add_argument("--out-matched-csv", default=str(DOC / "v15dp_active_set_type_guard_matched_seed_compare.csv"))
    p.add_argument("--out-metrics-csv", default=str(DOC / "v15dp_active_set_type_guard_metric_scores.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15dp_active_set_type_guard_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15dp_active_set_type_guard_holdout.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15dp_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15dp.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.reuse_existing:
        target_summary = read_csv(args.out_target_csv)
        guard_rows = read_csv(args.out_guard_csv)
        morphology_rows = read_csv(args.out_morphology_csv)
        component_rows = read_csv(args.out_components_csv)
        event_rows = read_csv(args.out_events_csv)
        blind_rows = read_csv(args.out_blind_csv)
        run_rows = read_csv(args.out_runs_csv)
    else:
        spec_rows = read_csv(v15da.V15CZ_SCORE_SPEC)
        base_states, base_rows, target_summary = build_bases()
        params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])

        guard_rows: List[Dict[str, Any]] = []
        morphology_rows: List[Dict[str, Any]] = []
        for growth_seed in GROWTH_SEEDS:
            seed_morph = morphology_rows_for_seed(base_states[growth_seed], growth_seed)
            morphology_rows.extend(seed_morph)
            guard_rows.append(pre_run_guard_row(seed_morph))

        write_csv(args.out_morphology_csv, morphology_rows)
        write_csv(args.out_guard_csv, guard_rows)
        print(f"wrote pre-run morphology {args.out_morphology_csv}")
        print(f"wrote pre-run guard {args.out_guard_csv}")
        for row in guard_rows:
            print(
                "pre-run guard "
                f"seed={int(row['growth_seed'])} "
                f"{GUARD_METRIC}(p0)={fmt(row['left_value'])} "
                f"{GUARD_METRIC}(p1)={fmt(row['right_value'])} "
                f"pred={row['predicted_type']}/{row['predicted_active_placements']}"
            )

        component_rows: List[Dict[str, Any]] = []
        event_rows: List[Dict[str, Any]] = []
        raw_rows: List[Dict[str, Any]] = []
        for growth_seed in GROWTH_SEEDS:
            for placement in PLACEMENTS:
                for seed_delta in FRESH_SEED_DELTAS:
                    print(f"running growth_seed {growth_seed} p{placement} seed_delta {seed_delta}")
                    comps, events, row = run_single(
                        growth_seed=growth_seed,
                        base_state=base_states[growth_seed],
                        base_row=base_rows[growth_seed],
                        params=params,
                        placement=int(placement),
                        seed_delta=int(seed_delta),
                    )
                    component_rows.extend(comps)
                    event_rows.extend(events)
                    raw_rows.append(row)

        run_rows, blind_rows = enrich_rows_seed_aware(
            raw_rows=raw_rows,
            component_rows=component_rows,
            spec_rows=spec_rows,
        )
        run_rows = add_pre_run_guard_fields(run_rows, guard_rows, morphology_rows)

    metric_rows = v15dg.metric_score_rows(run_rows)
    group_rows = group_summary_rows(run_rows)
    matched_rows = matched_seed_rows(run_rows)
    placement_rows = placement_summary_rows(run_rows, guard_rows, morphology_rows)
    seed_eval = seed_evaluation_rows(placement_rows, guard_rows)
    aggregate_eval = aggregate_evaluation_rows(seed_eval)
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        seed_eval=seed_eval,
        aggregate_eval=aggregate_eval,
        metric_rows=metric_rows,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_guard_csv, guard_rows)
    write_csv(args.out_morphology_csv, morphology_rows)
    write_csv(args.out_components_csv, component_rows)
    write_csv(args.out_events_csv, event_rows)
    write_csv(args.out_blind_csv, blind_rows)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_placement_csv, placement_rows)
    write_csv(args.out_seed_eval_csv, seed_eval)
    write_csv(args.out_eval_csv, aggregate_eval)
    write_csv(args.out_groups_csv, group_rows)
    write_csv(args.out_matched_csv, matched_rows)
    write_csv(args.out_metrics_csv, metric_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            guard_rows=guard_rows,
            placement_rows=placement_rows,
            seed_eval=seed_eval,
            aggregate_eval=aggregate_eval,
            metric_rows=metric_rows,
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
