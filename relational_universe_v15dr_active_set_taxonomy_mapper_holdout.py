#!/usr/bin/env python3
"""v0.15dr pre-registered active-set taxonomy mapper holdout.

Fresh dynamic holdout after v15dq.

Goal:
- stop refitting the failed v15do/v15dp two-type guard,
- train a tiny, deterministic mapper from v15dq repeated-class contrasts only,
- let the mapper abstain as `unknown` when fresh morphology is outside the
  learned repeated-class envelope,
- run fresh 1024/add_chord dynamics for p0,p1,p2 and evaluate the mapper.

This is still local defect/response-landscape work. It is not evidence for
particles, Lorentz behavior, entanglement, global invariants, or universal
geometry.
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
import relational_universe_v15dq_active_set_taxonomy_synthesis as v15dq


DOC = Path("Documentation")

TARGET_NODES = 1024
GROWTH_SEEDS = (808, 909, 1001, 1103)
PERTURBATION = "add_chord"
PLACEMENTS = (0, 1, 2)
ACTIVE_ESTABLISHED_RATE = 0.50
FRESH_SEED_DELTAS = (17011, 17053, 17107, 17167)

KNOWN_CLASSES = ("multi_active_p0_p2", "single_active_p1")
ACTIVE_SET_BY_CLASS = {
    "multi_active_p0_p2": frozenset({0, 2}),
    "single_active_p1": frozenset({1}),
    "unknown": frozenset(),
}

# Fixed before fresh dynamics. These are selected from v15dq repeated-class
# clean contrasts, with family diversity preferred over maximizing count.
MAPPER_FEATURES = (
    "new_edge_mean_forman_p2_minus_p1",
    "local_ball3_beta1_p2",
    "base_return_t2_p1",
    "base_return_t2_p0_minus_p1",
    "support_ball_3_p2",
    "local_ball3_boundary_to_volume_p0_minus_p1",
)
MAPPER_SOURCE = "v15dq_repeated_class_contrasts_family_diverse_fixed_before_v15dr"
MIN_PRESENT_FEATURES = 4
MIN_ENVELOPE_HITS = 4
MIN_WINNING_VOTES = 4
MIN_VOTE_MARGIN = 2
ENVELOPE_BUFFER_FRACTION = 0.25


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15dn.safe_float(x, default)


def safe_int(x: Any, default: int = 0) -> int:
    return v15dn.safe_int(x, default)


def safe_div(num: float, den: float) -> float:
    if not math.isfinite(num) or not math.isfinite(den) or den == 0.0:
        return float("nan")
    return num / den


def fmt(x: Any, digits: int = 3) -> str:
    return v15dn.fmt(x, digits=digits)


def mean_defined(values: Iterable[Any]) -> float:
    return v15dn.mean_defined(values)


def median_defined(values: Iterable[Any]) -> float:
    return v15dn.median_defined(values)


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    return v15dn.read_csv(Path(path))


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    v15dn.write_csv(Path(path), rows)


def format_set(values: Iterable[int]) -> str:
    vals = sorted(int(x) for x in values)
    return ";".join(f"p{x}" for x in vals) if vals else "none"


def set_from_label(label: str) -> set[int]:
    return v15dq.parse_set(label)


def active_set_for_class(label: str) -> frozenset[int]:
    return ACTIVE_SET_BY_CLASS.get(label, frozenset())


def build_bases() -> Tuple[Dict[int, Any], Dict[int, Mapping[str, Any]], Sequence[Mapping[str, Any]]]:
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))

    states: Dict[int, Any] = {}
    base_by_seed: Dict[int, Mapping[str, Any]] = {}
    for seed in GROWTH_SEEDS:
        states[seed] = base_states[(ensembles[0].name, seed)]
        base_by_seed[seed] = next(
            row
            for row in base_rows
            if int(row["growth_seed"]) == seed and int(row["target_nodes"]) == TARGET_NODES
        )

    target_summary = [
        {
            **dict(row),
            "holdout_growth_seeds": ";".join(str(seed) for seed in GROWTH_SEEDS),
            "holdout_kind": "v15dr_active_set_taxonomy_mapper",
        }
        for row in v10e.summarize_bases(base_rows)
        if int(row["target_nodes"]) == TARGET_NODES
    ]
    return states, base_by_seed, target_summary


def morphology_rows_for_seed(base_state: Any, growth_seed: int) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        row = dict(v15dl.morphology_for_seed_placement(base_state, growth_seed, placement))
        row["mapper_source"] = MAPPER_SOURCE
        row["pre_registered_before_dynamics"] = 1
        rows.append(row)
    return rows


def seed_feature_row_from_morphology(
    growth_seed: int,
    morphology_rows: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    placements = {safe_int(row["placement"]): row for row in morphology_rows}
    row: Dict[str, Any] = {
        "growth_seed": growth_seed,
        "mapper_source": MAPPER_SOURCE,
    }
    for metric in v15dn.MORPHOLOGY_METRICS:
        vals = {p: safe_float(placements.get(p, {}).get(metric)) for p in PLACEMENTS}
        if not any(math.isfinite(v) for v in vals.values()):
            continue
        for p in PLACEMENTS:
            row[f"{metric}_p{p}"] = vals[p]
        row[f"{metric}_p0_minus_p1"] = vals[0] - vals[1]
        row[f"{metric}_p2_minus_p1"] = vals[2] - vals[1]
        row[f"{metric}_p2_minus_p0"] = vals[2] - vals[0]
        row[f"{metric}_range"] = max(vals.values()) - min(vals.values())
    return row


def training_seed_feature_rows() -> List[Dict[str, Any]]:
    placement_rows = v15dq.load_placement_rows()
    seed_rows = v15dq.seed_summary_rows(placement_rows)
    return v15dq.seed_feature_rows(seed_rows, placement_rows)


def fit_mapper_spec() -> List[Dict[str, Any]]:
    training_rows = training_seed_feature_rows()
    by_class: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in training_rows:
        klass = str(row["landscape_class"])
        if klass in KNOWN_CLASSES:
            by_class[klass].append(row)

    spec_rows: List[Dict[str, Any]] = []
    for feature in MAPPER_FEATURES:
        class_values: Dict[str, List[float]] = {}
        for klass in KNOWN_CLASSES:
            vals = [
                safe_float(row.get(feature))
                for row in by_class.get(klass, [])
                if math.isfinite(safe_float(row.get(feature)))
            ]
            class_values[klass] = vals
        if any(not vals for vals in class_values.values()):
            raise RuntimeError(f"Mapper feature missing in training data: {feature}")

        medians = {klass: median_defined(vals) for klass, vals in class_values.items()}
        high_class = max(KNOWN_CLASSES, key=lambda klass: medians[klass])
        low_class = next(klass for klass in KNOWN_CLASSES if klass != high_class)
        high_min = min(class_values[high_class])
        high_max = max(class_values[high_class])
        low_min = min(class_values[low_class])
        low_max = max(class_values[low_class])
        clean_separation = int(high_min > low_max or low_min > high_max)
        if high_min > low_max:
            threshold = 0.5 * (high_min + low_max)
        elif low_min > high_max:
            threshold = 0.5 * (low_min + high_max)
        else:
            threshold = 0.5 * (medians[high_class] + medians[low_class])
        global_min = min(low_min, high_min)
        global_max = max(low_max, high_max)
        span = max(1e-12, global_max - global_min)
        buffer = span * ENVELOPE_BUFFER_FRACTION
        spec_rows.append(
            {
                "feature": feature,
                "metric": v15dq.feature_metric_name(feature),
                "feature_family": v15dn.feature_family(v15dq.feature_metric_name(feature)),
                "mapper_source": MAPPER_SOURCE,
                "high_class": high_class,
                "low_class": low_class,
                "threshold_high_class_if_value_ge": threshold,
                "clean_training_separation": clean_separation,
                "training_multi_active_p0_p2_min": min(class_values["multi_active_p0_p2"]),
                "training_multi_active_p0_p2_median": medians["multi_active_p0_p2"],
                "training_multi_active_p0_p2_max": max(class_values["multi_active_p0_p2"]),
                "training_single_active_p1_min": min(class_values["single_active_p1"]),
                "training_single_active_p1_median": medians["single_active_p1"],
                "training_single_active_p1_max": max(class_values["single_active_p1"]),
                "known_envelope_min": global_min,
                "known_envelope_max": global_max,
                "known_envelope_buffered_min": global_min - buffer,
                "known_envelope_buffered_max": global_max + buffer,
            }
        )
    return spec_rows


def mapper_prediction_row(
    *,
    growth_seed: int,
    seed_features: Mapping[str, Any],
    mapper_spec: Sequence[Mapping[str, Any]],
    morphology_rows: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    votes: Counter[str] = Counter()
    feature_votes: List[str] = []
    present = 0
    envelope_hits = 0
    outside_envelope = 0
    for spec in mapper_spec:
        feature = str(spec["feature"])
        value = safe_float(seed_features.get(feature))
        if not math.isfinite(value):
            feature_votes.append(f"{feature}=missing")
            continue
        present += 1
        if safe_float(spec["known_envelope_buffered_min"]) <= value <= safe_float(spec["known_envelope_buffered_max"]):
            envelope_hits += 1
        else:
            outside_envelope += 1
        high_class = str(spec["high_class"])
        low_class = str(spec["low_class"])
        vote = high_class if value >= safe_float(spec["threshold_high_class_if_value_ge"]) else low_class
        votes[vote] += 1
        feature_votes.append(f"{feature}:{fmt(value)}->{vote}")

    sorted_votes = sorted(((votes[klass], klass) for klass in KNOWN_CLASSES), reverse=True)
    winning_votes, winning_class = sorted_votes[0]
    runner_up_votes = sorted_votes[1][0]
    vote_margin = winning_votes - runner_up_votes

    reason = "known_class_decisive"
    predicted_type = winning_class
    if present < MIN_PRESENT_FEATURES:
        predicted_type = "unknown"
        reason = "too_few_present_features"
    elif envelope_hits < MIN_ENVELOPE_HITS:
        predicted_type = "unknown"
        reason = "outside_known_repeated_class_envelope"
    elif winning_votes < MIN_WINNING_VOTES or vote_margin < MIN_VOTE_MARGIN:
        predicted_type = "unknown"
        reason = "ambiguous_repeated_class_votes"

    predicted_set = active_set_for_class(predicted_type)
    by_placement = {safe_int(row["placement"]): row for row in morphology_rows}
    out: Dict[str, Any] = {
        "target_nodes": TARGET_NODES,
        "growth_seed": growth_seed,
        "perturbation": PERTURBATION,
        "mapper_source": MAPPER_SOURCE,
        "mapper_feature_count": len(mapper_spec),
        "present_feature_count": present,
        "known_envelope_hits": envelope_hits,
        "outside_envelope_count": outside_envelope,
        "multi_active_p0_p2_votes": votes["multi_active_p0_p2"],
        "single_active_p1_votes": votes["single_active_p1"],
        "winning_vote_margin": vote_margin,
        "predicted_type": predicted_type,
        "predicted_active_placements": format_set(predicted_set),
        "mapper_reason": reason,
        "feature_votes": ";".join(feature_votes),
        "pre_registered_before_dynamics": 1,
        "p0_support_signature": by_placement[0]["support_signature"],
        "p1_support_signature": by_placement[1]["support_signature"],
        "p2_support_signature": by_placement[2]["support_signature"],
    }
    for feature in MAPPER_FEATURES:
        out[feature] = seed_features.get(feature, "")
    return out


def run_single(
    *,
    growth_seed: int,
    base_state: Any,
    base_row: Mapping[str, Any],
    params: Any,
    placement: int,
    seed_delta: int,
) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    v15dk.GROWTH_SEED = int(growth_seed)
    v15dk.FRESH_SEED_DELTAS = FRESH_SEED_DELTAS
    comps, events, row = v15dk.run_single(
        base_state=base_state,
        base_row=base_row,
        params=params,
        placement=int(placement),
        seed_delta=int(seed_delta),
    )
    out = dict(row)
    out["source_scope"] = f"v15dr_growth_seed_{growth_seed}_p{placement}"
    out["pre_registered_taxonomy_mapper_holdout"] = 1
    out["pre_registered_active_set_type_guard_holdout"] = 0
    out["pre_registered_support_rank_holdout"] = 0
    out["pre_registered_return_probability_holdout"] = 0
    out["mapper_source"] = MAPPER_SOURCE
    return comps, events, out


def enrich_rows_seed_aware(
    *,
    raw_rows: Sequence[Mapping[str, Any]],
    component_rows: Sequence[Mapping[str, Any]],
    spec_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    return v15dp_enrich_rows_seed_aware(
        raw_rows=raw_rows,
        component_rows=component_rows,
        spec_rows=spec_rows,
    )


def v15dp_enrich_rows_seed_aware(
    *,
    raw_rows: Sequence[Mapping[str, Any]],
    component_rows: Sequence[Mapping[str, Any]],
    spec_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    raw_by_seed: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    comps_by_seed: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in raw_rows:
        raw_by_seed[safe_int(row["growth_seed"])].append(row)
    for row in component_rows:
        comps_by_seed[safe_int(row["growth_seed"])].append(row)

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


def add_pre_run_mapper_fields(
    run_rows: Sequence[Mapping[str, Any]],
    mapper_rows: Sequence[Mapping[str, Any]],
    morphology_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    mapper_by_seed = {safe_int(row["growth_seed"]): row for row in mapper_rows}
    morph_by_seed_placement = {
        (safe_int(row["growth_seed"]), safe_int(row["placement"])): row
        for row in morphology_rows
    }
    out: List[Dict[str, Any]] = []
    for raw in run_rows:
        row = dict(raw)
        seed = safe_int(row["growth_seed"])
        placement = safe_int(row["placement"])
        mapper = mapper_by_seed[seed]
        morph = morph_by_seed_placement[(seed, placement)]
        predicted_set = set_from_label(str(mapper["predicted_active_placements"]))
        row["mapper_source"] = MAPPER_SOURCE
        row["mapper_predicted_type"] = mapper["predicted_type"]
        row["mapper_predicted_active_placements"] = mapper["predicted_active_placements"]
        row["mapper_reason"] = mapper["mapper_reason"]
        row["mapper_present_feature_count"] = mapper["present_feature_count"]
        row["mapper_known_envelope_hits"] = mapper["known_envelope_hits"]
        row["mapper_outside_envelope_count"] = mapper["outside_envelope_count"]
        row["mapper_multi_active_p0_p2_votes"] = mapper["multi_active_p0_p2_votes"]
        row["mapper_single_active_p1_votes"] = mapper["single_active_p1_votes"]
        row["mapper_winning_vote_margin"] = mapper["winning_vote_margin"]
        row["mapper_placement_predicted_active"] = int(placement in predicted_set)
        for field in (
            "delta_return_t2",
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
    mapper_rows: Sequence[Mapping[str, Any]],
    morphology_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    mapper_by_seed = {safe_int(row["growth_seed"]): row for row in mapper_rows}
    morph_by_seed_placement = {
        (safe_int(row["growth_seed"]), safe_int(row["placement"])): row
        for row in morphology_rows
    }
    grouped: Dict[Tuple[int, int], List[Mapping[str, Any]]] = defaultdict(list)
    for row in run_rows:
        grouped[(safe_int(row["growth_seed"]), safe_int(row["placement"]))].append(row)

    out: List[Dict[str, Any]] = []
    for (seed, placement), group in sorted(grouped.items()):
        counts = Counter(str(row["far_shell_horizon_label"]) for row in group)
        n = len(group)
        established_rate = counts.get("established_far_shell_horizon", 0) / max(1, n)
        mapper = mapper_by_seed[seed]
        morph = morph_by_seed_placement[(seed, placement)]
        predicted_set = set_from_label(str(mapper["predicted_active_placements"]))
        out.append(
            {
                "growth_seed": seed,
                "placement": placement,
                "support_signature": morph["support_signature"],
                "mapper_predicted_type": mapper["predicted_type"],
                "mapper_predicted_active_placements": mapper["predicted_active_placements"],
                "mapper_reason": mapper["mapper_reason"],
                "mapper_placement_predicted_active": int(placement in predicted_set),
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
    mapper_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    mapper_by_seed = {safe_int(row["growth_seed"]): row for row in mapper_rows}
    rows_by_seed: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in placement_rows:
        rows_by_seed[safe_int(row["growth_seed"])].append(row)

    out: List[Dict[str, Any]] = []
    for seed, group in sorted(rows_by_seed.items()):
        active_set = frozenset(
            safe_int(row["placement"])
            for row in group
            if safe_int(row.get("active_placement")) == 1
        )
        actual_type = v15dq.landscape_class(active_set)
        mapper = mapper_by_seed[seed]
        predicted_type = str(mapper["predicted_type"])
        predicted_set = set(active_set_for_class(predicted_type))
        actual = set(active_set)
        captured = actual & predicted_set
        false_positive = predicted_set - actual
        missed = actual - predicted_set
        actual_known = actual_type in KNOWN_CLASSES
        predicted_known = predicted_type in KNOWN_CLASSES
        abstained = predicted_type == "unknown"
        out.append(
            {
                "growth_seed": seed,
                "actual_type": actual_type,
                "actual_active_placements": format_set(actual),
                "actual_known_repeated_class": int(actual_known),
                "predicted_type": predicted_type,
                "predicted_active_placements": format_set(predicted_set),
                "mapper_reason": mapper["mapper_reason"],
                "mapper_abstained": int(abstained),
                "known_class_type_hit": int(actual_known and predicted_type == actual_type),
                "known_class_false_ood": int(actual_known and abstained),
                "ood_correct_abstain": int((not actual_known) and abstained),
                "ood_false_known_prediction": int((not actual_known) and predicted_known),
                "exact_set_match": int(actual == predicted_set),
                "captured_placements": format_set(captured),
                "missed_placements": format_set(missed),
                "false_positive_placements": format_set(false_positive),
                "coverage_fraction": safe_div(len(captured), len(actual)),
                "precision_fraction": safe_div(len(captured), len(predicted_set)),
                "burden_fraction": safe_div(len(predicted_set), len(PLACEMENTS)),
                "placement_rates": ";".join(
                    f"p{safe_int(row['placement'])}:{fmt(row['established_rate'])}"
                    for row in sorted(group, key=lambda x: safe_int(x["placement"]))
                ),
                "multi_active_p0_p2_votes": mapper["multi_active_p0_p2_votes"],
                "single_active_p1_votes": mapper["single_active_p1_votes"],
                "known_envelope_hits": mapper["known_envelope_hits"],
                "outside_envelope_count": mapper["outside_envelope_count"],
            }
        )
    return out


def aggregate_evaluation_rows(seed_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    seed_count = len(seed_rows)
    known_rows = [row for row in seed_rows if safe_int(row["actual_known_repeated_class"]) == 1]
    ood_rows = [row for row in seed_rows if safe_int(row["actual_known_repeated_class"]) == 0]
    exact = sum(safe_int(row["exact_set_match"]) for row in seed_rows)
    known_hits = sum(safe_int(row["known_class_type_hit"]) for row in known_rows)
    known_false_ood = sum(safe_int(row["known_class_false_ood"]) for row in known_rows)
    ood_correct = sum(safe_int(row["ood_correct_abstain"]) for row in ood_rows)
    ood_false_known = sum(safe_int(row["ood_false_known_prediction"]) for row in ood_rows)

    total_active = 0
    total_predicted = 0
    total_captured = 0
    total_false_positive = 0
    total_missed = 0
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

    return [
        {
            "key": "mapper_source",
            "value": MAPPER_SOURCE,
            "evidence": ";".join(MAPPER_FEATURES),
        },
        {
            "key": "seed_count",
            "value": seed_count,
            "evidence": ";".join(str(row["growth_seed"]) for row in seed_rows),
        },
        {
            "key": "known_class_seed_count",
            "value": len(known_rows),
            "evidence": ";".join(str(row["growth_seed"]) for row in known_rows) or "none",
        },
        {
            "key": "ood_seed_count",
            "value": len(ood_rows),
            "evidence": ";".join(str(row["growth_seed"]) for row in ood_rows) or "none",
        },
        {
            "key": "known_class_type_accuracy",
            "value": fmt(safe_div(known_hits, len(known_rows))),
            "evidence": f"known_hits={known_hits}; known_rows={len(known_rows)}; known_false_ood={known_false_ood}",
        },
        {
            "key": "ood_abstain_accuracy",
            "value": fmt(safe_div(ood_correct, len(ood_rows))),
            "evidence": f"ood_correct_abstain={ood_correct}; ood_rows={len(ood_rows)}; ood_false_known={ood_false_known}",
        },
        {
            "key": "overall_exact_set_match_rate",
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
            "key": "mapper_status",
            "value": mapper_status(seed_rows),
            "evidence": "fresh active-set taxonomy mapper holdout; no refit after dynamics",
        },
    ]


def mapper_status(seed_rows: Sequence[Mapping[str, Any]]) -> str:
    if not seed_rows:
        return "mapper_failed_no_rows"
    known_rows = [row for row in seed_rows if safe_int(row["actual_known_repeated_class"]) == 1]
    ood_rows = [row for row in seed_rows if safe_int(row["actual_known_repeated_class"]) == 0]
    known_hits = sum(safe_int(row["known_class_type_hit"]) for row in known_rows)
    ood_correct = sum(safe_int(row["ood_correct_abstain"]) for row in ood_rows)
    exact = sum(safe_int(row["exact_set_match"]) for row in seed_rows)
    if known_rows and known_hits == len(known_rows) and (not ood_rows or ood_correct == len(ood_rows)):
        return "taxonomy_mapper_supported_small_holdout"
    if ood_rows and ood_correct == len(ood_rows) and not known_rows:
        return "taxonomy_mapper_only_ood_tested"
    if exact == len(seed_rows):
        return "taxonomy_mapper_exact_sets_supported_small_holdout"
    if known_rows and known_hits > 0:
        return "taxonomy_mapper_partial_known_class_signal"
    if ood_rows and ood_correct > 0:
        return "taxonomy_mapper_partial_ood_signal"
    return "taxonomy_mapper_not_supported"


def group_summary_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["analysis_group"])].append(row)
    out: List[Dict[str, Any]] = []
    for group, group_rows in sorted(grouped.items()):
        labels = Counter(str(row["far_shell_horizon_label"]) for row in group_rows)
        placements = Counter(f"p{safe_int(row['placement'])}" for row in group_rows)
        seeds = Counter(str(safe_int(row["growth_seed"])) for row in group_rows)
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
        key = (safe_int(row["growth_seed"]), safe_int(row["seed_delta"]))
        by_seed_delta[key][safe_int(row["placement"])] = row

    out: List[Dict[str, Any]] = []
    for (growth_seed, seed_delta), group in sorted(by_seed_delta.items()):
        if any(p not in group for p in PLACEMENTS):
            continue
        p0, p1, p2 = group[0], group[1], group[2]
        out.append(
            {
                "growth_seed": growth_seed,
                "seed_delta": seed_delta,
                "mapper_predicted_type": p0.get("mapper_predicted_type", ""),
                "mapper_predicted_active_placements": p0.get("mapper_predicted_active_placements", ""),
                "mapper_reason": p0.get("mapper_reason", ""),
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
    size_clean = all(safe_int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((safe_int(row["requested_match"]) for row in run_rows), default=0) == 1
    labels = Counter(str(row["far_shell_horizon_label"]) for row in run_rows)
    actual_types = Counter(str(row["actual_type"]) for row in seed_eval)
    predicted_types = Counter(str(row["predicted_type"]) for row in seed_eval)
    mapper = next(row for row in aggregate_eval if row["key"] == "mapper_status")
    known_acc = next(row for row in aggregate_eval if row["key"] == "known_class_type_accuracy")
    ood_acc = next(row for row in aggregate_eval if row["key"] == "ood_abstain_accuracy")
    exact = next(row for row in aggregate_eval if row["key"] == "overall_exact_set_match_rate")
    coverage = next(row for row in aggregate_eval if row["key"] == "coverage_fraction")
    precision = next(row for row in aggregate_eval if row["key"] == "precision_fraction")
    primary_dynamic = next(row for row in metric_rows if str(row["metric"]) == v15dg.PRIMARY_METRIC)

    if mapper["value"] in {
        "taxonomy_mapper_supported_small_holdout",
        "taxonomy_mapper_exact_sets_supported_small_holdout",
    }:
        next_status = "replicate_taxonomy_mapper_with_more_growth_seeds"
        next_note = "Mapperen traff liten holdout; neste runde bor replikere frossen mapper med flere growth seeds."
    elif mapper["value"] == "taxonomy_mapper_only_ood_tested":
        next_status = "increase_seed_count_to_hit_known_and_unknown_classes"
        next_note = "Holdouten testet bare OOD/unknown-adferd; vi trenger flere seeds for kjent klasse-treff."
    elif mapper["value"] in {"taxonomy_mapper_partial_known_class_signal", "taxonomy_mapper_partial_ood_signal"}:
        next_status = "taxonomy_mapper_promising_but_not_selector_grade"
        next_note = "Det finnes delsignal, men ikke nok til selector-claim; bruk flere seeds eller enklere atlas."
    else:
        next_status = "retire_this_mapper_or_expand_taxonomy_atlas"
        next_note = "Mapperen traff ikke; neste gevinst er trolig mer klassefrekvens/atlas, ikke refit av samme features."

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
            "status": "taxonomy_mapper_written_before_dynamics",
            "note": (
                "Mapperen bruker bare v15dq repeated-class contrasts, skriver pre-run mapper CSV foer run-loop, "
                "og refittes ikke etter outcome."
            ),
        },
        {
            "diagnostic_family": "outcome_balance",
            "status": "fresh_growth_seed_taxonomy_recorded",
            "note": (
                f"Run labels: {';'.join(f'{k}:{v}' for k, v in sorted(labels.items()))}. "
                f"Actual seed types: {';'.join(f'{k}:{v}' for k, v in sorted(actual_types.items()))}. "
                f"Predicted types: {';'.join(f'{k}:{v}' for k, v in sorted(predicted_types.items()))}."
            ),
        },
        {
            "diagnostic_family": "mapper_result",
            "status": str(mapper["value"]),
            "note": (
                f"known_class_type_accuracy={known_acc['value']}; ood_abstain_accuracy={ood_acc['value']}; "
                f"exact_set_match={exact['value']}; coverage={coverage['value']}; precision={precision['value']}."
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
    mapper_spec: Sequence[Mapping[str, Any]],
    mapper_rows: Sequence[Mapping[str, Any]],
    placement_rows: Sequence[Mapping[str, Any]],
    seed_eval: Sequence[Mapping[str, Any]],
    aggregate_eval: Sequence[Mapping[str, Any]],
    metric_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dr: active-set taxonomy mapper holdout")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er en fresh dynamic holdout av en liten taxonomy-mapper etter v15dq.")
    lines.append("Mapperen trenes bare paa repeated-class contrasts fra v15dq og kan eksplisitt svare `unknown`.")
    lines.append("Pre-run mapper CSV skrives foer dynamikk-loop; dynamiske observabler brukes bare til evaluering og audit.")
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
                {"field": "known_classes", "value": ";".join(KNOWN_CLASSES)},
                {"field": "mapper_source", "value": MAPPER_SOURCE},
            ],
            ("field", "value"),
        )
    )
    lines.append("")
    lines.append("## Mapper feature spec")
    lines.append("")
    lines.extend(
        table(
            mapper_spec,
            (
                "feature",
                "feature_family",
                "high_class",
                "threshold_high_class_if_value_ge",
                "clean_training_separation",
            ),
        )
    )
    lines.append("")
    lines.append("## Pre-run mapper")
    lines.append("")
    lines.extend(
        table(
            mapper_rows,
            (
                "growth_seed",
                "predicted_type",
                "predicted_active_placements",
                "mapper_reason",
                "multi_active_p0_p2_votes",
                "single_active_p1_votes",
                "known_envelope_hits",
                "outside_envelope_count",
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
                "mapper_predicted_type",
                "mapper_placement_predicted_active",
                "label_counts",
                "established_rate",
                "active_placement",
                "median_boundary_mass",
                "median_genealogy_intensity",
            ),
        )
    )
    lines.append("")
    lines.append("## Seed-level mapper evaluation")
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
                "mapper_reason",
                "known_class_type_hit",
                "ood_correct_abstain",
                "exact_set_match",
                "placement_rates",
            ),
        )
    )
    lines.append("")
    lines.append("## Aggregate mapper evaluation")
    lines.append("")
    lines.extend(table(aggregate_eval, ("key", "value", "evidence")))
    lines.append("")
    lines.append("## Dynamic metric audit")
    lines.append("")
    lines.extend(
        table(
            metric_rows,
            ("metric", "role", "auc_established_vs_no", "median_established_raw", "median_no_horizon_raw"),
        )
    )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette tester om active-set-landskapet kan kartlegges bedre enn single-feature guards.")
    lines.append("- `unknown` er et legitimt svar hvis fresh seed faller utenfor repeated-class-rommet.")
    lines.append("- Ikke oppgrader dette til invariant/Lorentz/partikkel/entanglement-claim.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15dr", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke refit mapperen etter v15dr-outcome.")
    lines.append("- Hvis mapperen feiler, gaa mot klassefrekvens/landskapsatlas heller enn ny single-feature guard.")
    lines.append("- Hvis mapperen treffer, repliker samme frosne mapper paa flere growth seeds foer selector-sprak.")
    lines.append("- Ikke oppgrader til invariant/Lorentz/partikkel/entanglement-claim.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15dr",
            "",
            "Denne runden tester ikke en ny fysisk lov. Den tester om vi kan lage et kart over hvilke lokale plasseringer som blir aktive.",
            "",
            "Mapperen faar lov til aa si `unknown` naar en ny startgraf ikke ligner nok paa de klassene vi allerede har sett flere ganger.",
            "",
            f"- Hovedlesning: `{diag['mapper_result']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Dette er nyttig hvis vi vil vite om add_chord-landskapet har repeterbar struktur, eller om det fortsatt er for base-betinget og heterogent.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15dr active-set taxonomy mapper holdout.")
    p.add_argument("--reuse-existing", action="store_true", help="Regenerate aggregate/report files from existing v15dr CSV outputs.")
    p.add_argument("--out-target-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_target_summary.csv"))
    p.add_argument("--out-mapper-spec-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_spec.csv"))
    p.add_argument("--out-mapper-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_pre_run_mapper.csv"))
    p.add_argument("--out-morphology-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_pre_run_morphology.csv"))
    p.add_argument("--out-components-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_component_trajectories.csv"))
    p.add_argument("--out-events-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_event_log.csv"))
    p.add_argument("--out-blind-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_blind_scores.csv"))
    p.add_argument("--out-runs-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_run_features.csv"))
    p.add_argument("--out-placement-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_placement_summary.csv"))
    p.add_argument("--out-seed-eval-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_seed_evaluation.csv"))
    p.add_argument("--out-eval-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_evaluation.csv"))
    p.add_argument("--out-groups-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_group_summary.csv"))
    p.add_argument("--out-matched-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_matched_seed_compare.csv"))
    p.add_argument("--out-metrics-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_metric_scores.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15dr_active_set_taxonomy_mapper_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15dr_active_set_taxonomy_mapper_holdout.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15dr_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15dr.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.reuse_existing:
        target_summary = read_csv(args.out_target_csv)
        mapper_spec = read_csv(args.out_mapper_spec_csv)
        mapper_rows = read_csv(args.out_mapper_csv)
        morphology_rows = read_csv(args.out_morphology_csv)
        component_rows = read_csv(args.out_components_csv)
        event_rows = read_csv(args.out_events_csv)
        blind_rows = read_csv(args.out_blind_csv)
        run_rows = read_csv(args.out_runs_csv)
    else:
        spec_rows = read_csv(v15da.V15CZ_SCORE_SPEC)
        mapper_spec = fit_mapper_spec()
        base_states, base_rows, target_summary = build_bases()
        params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])

        mapper_rows: List[Dict[str, Any]] = []
        morphology_rows: List[Dict[str, Any]] = []
        for growth_seed in GROWTH_SEEDS:
            seed_morph = morphology_rows_for_seed(base_states[growth_seed], growth_seed)
            morphology_rows.extend(seed_morph)
            seed_features = seed_feature_row_from_morphology(growth_seed, seed_morph)
            mapper_rows.append(
                mapper_prediction_row(
                    growth_seed=growth_seed,
                    seed_features=seed_features,
                    mapper_spec=mapper_spec,
                    morphology_rows=seed_morph,
                )
            )

        write_csv(args.out_mapper_spec_csv, mapper_spec)
        write_csv(args.out_morphology_csv, morphology_rows)
        write_csv(args.out_mapper_csv, mapper_rows)
        print(f"wrote mapper spec {args.out_mapper_spec_csv}")
        print(f"wrote pre-run morphology {args.out_morphology_csv}")
        print(f"wrote pre-run mapper {args.out_mapper_csv}")
        for row in mapper_rows:
            print(
                "pre-run mapper "
                f"seed={safe_int(row['growth_seed'])} "
                f"pred={row['predicted_type']}/{row['predicted_active_placements']} "
                f"reason={row['mapper_reason']} "
                f"votes=p0p2:{row['multi_active_p0_p2_votes']},p1:{row['single_active_p1_votes']}"
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
        run_rows = add_pre_run_mapper_fields(run_rows, mapper_rows, morphology_rows)

    metric_rows = v15dg.metric_score_rows(run_rows)
    group_rows = group_summary_rows(run_rows)
    matched_rows = matched_seed_rows(run_rows)
    placement_rows = placement_summary_rows(run_rows, mapper_rows, morphology_rows)
    seed_eval = seed_evaluation_rows(placement_rows, mapper_rows)
    aggregate_eval = aggregate_evaluation_rows(seed_eval)
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        seed_eval=seed_eval,
        aggregate_eval=aggregate_eval,
        metric_rows=metric_rows,
    )

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_mapper_spec_csv, mapper_spec)
    write_csv(args.out_mapper_csv, mapper_rows)
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
            mapper_spec=mapper_spec,
            mapper_rows=mapper_rows,
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
