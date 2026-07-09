#!/usr/bin/env python3
"""v0.15dt OOD-first stratified selector synthesis.

No-new-dynamics synthesis after v15ds.

Goal:
- use the now-stabilizing active-set atlas as a training/evaluation object,
- build an OOD-first, class-stratified selector candidate from pre-run
  morphology only,
- evaluate it by leave-one-seed-out on repeated classes and explicit singleton
  OOD abstention,
- decide whether a fresh dynamic holdout is warranted.

This is selector-design work for a local add_chord response landscape. It is
not evidence for particles, Lorentz behavior, entanglement, global invariants,
or universal geometry.
"""
from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v15dn_multi_active_landscape_synthesis as v15dn
import relational_universe_v15dq_active_set_taxonomy_synthesis as v15dq
import relational_universe_v15dr_active_set_taxonomy_mapper_holdout as v15dr


DOC = Path("Documentation")

TARGET_NODES = 1024
PERTURBATION = "add_chord"
PLACEMENTS = (0, 1, 2)
REPEATED_CLASS_MIN_SEEDS = 3
MAX_FEATURES = 8
MAX_FEATURES_PER_FAMILY = 2
MIN_FEATURE_CLASS_COVERAGE = 2
MIN_PRESENT_FEATURES = 6
MIN_ENVELOPE_HITS = 3
MAX_MEAN_DISTANCE = 1.25
MIN_DISTANCE_MARGIN = 0.15
ENVELOPE_BUFFER_FRACTION = 0.20
SYNTHESIS_SOURCE = "v15dt_ood_first_stratified_selector_from_v15dq_v15dr_v15ds"

V15DR_MORPHOLOGY_CSV = DOC / "v15dr_active_set_taxonomy_mapper_pre_run_morphology.csv"
V15DR_SEED_EVAL_CSV = DOC / "v15dr_active_set_taxonomy_mapper_seed_evaluation.csv"
V15DS_MORPHOLOGY_CSV = DOC / "v15ds_active_set_landscape_atlas_pre_run_morphology.csv"
V15DS_SEED_SUMMARY_CSV = DOC / "v15ds_active_set_landscape_atlas_seed_summary.csv"

METADATA_FIELDS = {
    "source",
    "target_nodes",
    "growth_seed",
    "perturbation",
    "landscape_class",
    "active_count",
    "active_placements",
    "covered_by_v15do_two_type_space",
    "new_after_v15dp_type",
    "class_seen_before_v15ds",
    "new_class_in_v15ds",
    "strongest_placement",
    "strongest_established_rate",
    "p0_established_rate",
    "p1_established_rate",
    "p2_established_rate",
    "placement_rates",
    "support_signatures",
    "mapper_source",
    "atlas_source",
}


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


def feature_metric_name(feature: str) -> str:
    return v15dq.feature_metric_name(feature)


def feature_family(feature: str) -> str:
    return v15dn.feature_family(feature_metric_name(feature))


def pairwise_auc(positive: Sequence[float], negative: Sequence[float]) -> float:
    return v15dn.pairwise_auc(positive, negative)


def median_abs_dev(values: Sequence[float]) -> float:
    vals = sorted(x for x in values if math.isfinite(x))
    if not vals:
        return float("nan")
    med = median_defined(vals)
    return median_defined(abs(x - med) for x in vals)


def grouped_morphology_rows(path: Path) -> Dict[int, List[Mapping[str, Any]]]:
    grouped: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in read_csv(path):
        grouped[safe_int(row["growth_seed"])].append(row)
    return dict(sorted(grouped.items()))


def seed_feature_row_from_morphology(
    *,
    source: str,
    growth_seed: int,
    landscape_class: str,
    active_placements: str,
    morphology_rows: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    row = v15dr.seed_feature_row_from_morphology(growth_seed, morphology_rows)
    row["source"] = source
    row["target_nodes"] = TARGET_NODES
    row["perturbation"] = PERTURBATION
    row["landscape_class"] = landscape_class
    row["active_placements"] = active_placements
    row["active_count"] = len(set_from_label(active_placements))
    return row


def load_v15dq_seed_features() -> List[Dict[str, Any]]:
    placement_rows = v15dq.load_placement_rows()
    seed_rows = v15dq.seed_summary_rows(placement_rows)
    feature_rows = v15dq.seed_feature_rows(seed_rows, placement_rows)
    out: List[Dict[str, Any]] = []
    for row in feature_rows:
        new_row = dict(row)
        new_row["source"] = "v15dq"
        new_row["target_nodes"] = TARGET_NODES
        new_row["perturbation"] = PERTURBATION
        out.append(new_row)
    return out


def load_v15dr_seed_features() -> List[Dict[str, Any]]:
    eval_by_seed = {safe_int(row["growth_seed"]): row for row in read_csv(V15DR_SEED_EVAL_CSV)}
    out: List[Dict[str, Any]] = []
    for seed, rows in grouped_morphology_rows(V15DR_MORPHOLOGY_CSV).items():
        meta = eval_by_seed[seed]
        out.append(
            seed_feature_row_from_morphology(
                source="v15dr",
                growth_seed=seed,
                landscape_class=str(meta["actual_type"]),
                active_placements=str(meta["actual_active_placements"]),
                morphology_rows=rows,
            )
        )
    return out


def load_v15ds_seed_features() -> List[Dict[str, Any]]:
    summary_by_seed = {safe_int(row["growth_seed"]): row for row in read_csv(V15DS_SEED_SUMMARY_CSV)}
    out: List[Dict[str, Any]] = []
    for seed, rows in grouped_morphology_rows(V15DS_MORPHOLOGY_CSV).items():
        meta = summary_by_seed[seed]
        out.append(
            seed_feature_row_from_morphology(
                source="v15ds",
                growth_seed=seed,
                landscape_class=str(meta["landscape_class"]),
                active_placements=str(meta["active_placements"]),
                morphology_rows=rows,
            )
        )
    return out


def load_seed_features() -> List[Dict[str, Any]]:
    rows = load_v15dq_seed_features() + load_v15dr_seed_features() + load_v15ds_seed_features()
    return sorted(rows, key=lambda row: (str(row["source"]), safe_int(row["growth_seed"])))


def class_count_rows(seed_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for row in seed_rows:
        grouped[str(row["landscape_class"])].append(row)
    out: List[Dict[str, Any]] = []
    for klass, group in sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        out.append(
            {
                "landscape_class": klass,
                "n_seeds": len(group),
                "seed_fraction": safe_div(len(group), len(seed_rows)),
                "growth_seeds": ";".join(str(safe_int(row["growth_seed"])) for row in group),
                "sources": ";".join(sorted(set(str(row["source"]) for row in group))),
                "active_placements_examples": ";".join(sorted(set(str(row["active_placements"]) for row in group))),
                "selector_role": "repeated_trainable" if len(group) >= REPEATED_CLASS_MIN_SEEDS else "singleton_ood",
            }
        )
    return out


def repeated_classes(seed_rows: Sequence[Mapping[str, Any]]) -> List[str]:
    counts = Counter(str(row["landscape_class"]) for row in seed_rows)
    return sorted(klass for klass, count in counts.items() if count >= REPEATED_CLASS_MIN_SEEDS)


def feature_candidates(seed_rows: Sequence[Mapping[str, Any]], train_classes: Sequence[str]) -> List[str]:
    features: List[str] = []
    for key in seed_rows[0].keys():
        if key in METADATA_FIELDS:
            continue
        if key.endswith("_established_rate"):
            continue
        values = [safe_float(row.get(key)) for row in seed_rows]
        if len([x for x in values if math.isfinite(x)]) < len(seed_rows) - 1:
            continue
        if len(set(round(x, 12) for x in values if math.isfinite(x))) <= 1:
            continue
        ok = True
        for klass in train_classes:
            class_vals = [
                safe_float(row.get(key))
                for row in seed_rows
                if str(row["landscape_class"]) == klass and math.isfinite(safe_float(row.get(key)))
            ]
            if len(class_vals) < MIN_FEATURE_CLASS_COVERAGE:
                ok = False
                break
        if ok:
            features.append(key)
    return sorted(features)


def feature_score_rows(seed_rows: Sequence[Mapping[str, Any]], train_classes: Sequence[str]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    candidate_features = feature_candidates(seed_rows, train_classes)
    train_rows = [row for row in seed_rows if str(row["landscape_class"]) in train_classes]
    ood_rows = [row for row in seed_rows if str(row["landscape_class"]) not in train_classes]

    for feature in candidate_features:
        by_class: Dict[str, List[float]] = {}
        for klass in train_classes:
            by_class[klass] = [
                safe_float(row.get(feature))
                for row in train_rows
                if str(row["landscape_class"]) == klass and math.isfinite(safe_float(row.get(feature)))
            ]
        class_medians = {klass: median_defined(vals) for klass, vals in by_class.items()}
        med_range = max(class_medians.values()) - min(class_medians.values())
        within_mad = mean_defined(median_abs_dev(vals) for vals in by_class.values())
        separation_score = safe_div(med_range, within_mad + 1e-9)

        one_vs_rest_aucs: List[float] = []
        for klass in train_classes:
            pos = by_class[klass]
            neg = [
                value
                for other, vals in by_class.items()
                if other != klass
                for value in vals
            ]
            auc = pairwise_auc(pos, neg)
            one_vs_rest_aucs.append(max(auc, 1.0 - auc) if math.isfinite(auc) else float("nan"))

        ood_values = [
            safe_float(row.get(feature))
            for row in ood_rows
            if math.isfinite(safe_float(row.get(feature)))
        ]
        train_values = [
            safe_float(row.get(feature))
            for row in train_rows
            if math.isfinite(safe_float(row.get(feature)))
        ]
        train_min = min(train_values) if train_values else float("nan")
        train_max = max(train_values) if train_values else float("nan")
        ood_outside_fraction = safe_div(
            sum(1 for value in ood_values if value < train_min or value > train_max),
            len(ood_values),
        )

        rows.append(
            {
                "feature": feature,
                "metric": feature_metric_name(feature),
                "feature_family": feature_family(feature),
                "macro_oriented_auc": mean_defined(one_vs_rest_aucs),
                "separation_score": separation_score,
                "class_median_range": med_range,
                "mean_within_class_mad": within_mad,
                "ood_outside_train_range_fraction": ood_outside_fraction,
                "n_train_values": len(train_values),
                "n_ood_values": len(ood_values),
                "class_medians": ";".join(f"{klass}:{fmt(class_medians[klass])}" for klass in train_classes),
            }
        )
    return sorted(
        rows,
        key=lambda row: (
            -safe_float(row["macro_oriented_auc"]),
            -safe_float(row["separation_score"]),
            str(row["feature"]),
        ),
    )


def selected_feature_rows(feature_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    selected: List[Dict[str, Any]] = []
    family_counts: Counter[str] = Counter()
    for row in feature_rows:
        family = str(row["feature_family"])
        if family_counts[family] >= MAX_FEATURES_PER_FAMILY:
            continue
        out = dict(row)
        out["selector_feature_rank"] = len(selected) + 1
        selected.append(out)
        family_counts[family] += 1
        if len(selected) >= MAX_FEATURES:
            break
    return selected


def quantiles(values: Sequence[float]) -> Tuple[float, float, float]:
    vals = sorted(x for x in values if math.isfinite(x))
    if not vals:
        return (float("nan"), float("nan"), float("nan"))
    return (vals[0], median_defined(vals), vals[-1])


def normalizer_rows(seed_rows: Sequence[Mapping[str, Any]], selected_features: Sequence[str]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for feature in selected_features:
        vals = [safe_float(row.get(feature)) for row in seed_rows if math.isfinite(safe_float(row.get(feature)))]
        qmin, qmed, qmax = quantiles(vals)
        mad = median_abs_dev(vals)
        scale = mad if math.isfinite(mad) and mad > 1e-9 else (qmax - qmin)
        if not math.isfinite(scale) or scale <= 1e-9:
            scale = 1.0
        rows.append(
            {
                "feature": feature,
                "global_min": qmin,
                "global_median": qmed,
                "global_max": qmax,
                "global_mad": mad,
                "normalization_scale": scale,
            }
        )
    return rows


def fit_class_profiles(
    seed_rows: Sequence[Mapping[str, Any]],
    train_classes: Sequence[str],
    selected_features: Sequence[str],
    *,
    excluded_seed: int | None = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    training_rows = [
        row
        for row in seed_rows
        if str(row["landscape_class"]) in train_classes and safe_int(row["growth_seed"]) != excluded_seed
    ]
    normalizers = normalizer_rows(training_rows, selected_features)
    norm_by_feature = {str(row["feature"]): row for row in normalizers}

    profile_rows: List[Dict[str, Any]] = []
    for klass in train_classes:
        class_rows = [row for row in training_rows if str(row["landscape_class"]) == klass]
        for feature in selected_features:
            vals = [
                safe_float(row.get(feature))
                for row in class_rows
                if math.isfinite(safe_float(row.get(feature)))
            ]
            if not vals:
                continue
            qmin, qmed, qmax = quantiles(vals)
            span = max(1e-9, qmax - qmin)
            buffer = span * ENVELOPE_BUFFER_FRACTION
            profile_rows.append(
                {
                    "landscape_class": klass,
                    "feature": feature,
                    "metric": feature_metric_name(feature),
                    "feature_family": feature_family(feature),
                    "class_n_train": len(class_rows),
                    "feature_n_train": len(vals),
                    "class_min": qmin,
                    "class_median": qmed,
                    "class_max": qmax,
                    "buffered_min": qmin - buffer,
                    "buffered_max": qmax + buffer,
                    "normalization_scale": safe_float(norm_by_feature[feature]["normalization_scale"], 1.0),
                }
            )
    return profile_rows, normalizers


def predict_one(
    seed_row: Mapping[str, Any],
    train_classes: Sequence[str],
    profile_rows: Sequence[Mapping[str, Any]],
    selected_features: Sequence[str],
) -> Dict[str, Any]:
    profiles_by_class_feature = {
        (str(row["landscape_class"]), str(row["feature"])): row
        for row in profile_rows
    }
    class_scores: Dict[str, Dict[str, Any]] = {}
    for klass in train_classes:
        distances: List[float] = []
        present = 0
        envelope_hits = 0
        missing = 0
        feature_notes: List[str] = []
        for feature in selected_features:
            profile = profiles_by_class_feature.get((klass, feature))
            value = safe_float(seed_row.get(feature))
            if profile is None or not math.isfinite(value):
                missing += 1
                continue
            present += 1
            scale = max(1e-9, safe_float(profile.get("normalization_scale"), 1.0))
            distance = abs(value - safe_float(profile["class_median"])) / scale
            distances.append(distance)
            hit = safe_float(profile["buffered_min"]) <= value <= safe_float(profile["buffered_max"])
            envelope_hits += int(hit)
            feature_notes.append(f"{feature}:{fmt(value)}:{fmt(distance)}:{'hit' if hit else 'miss'}")
        mean_distance = mean_defined(distances)
        class_scores[klass] = {
            "present": present,
            "missing": missing,
            "envelope_hits": envelope_hits,
            "mean_distance": mean_distance,
            "feature_notes": ";".join(feature_notes),
        }

    ranked = sorted(
        class_scores.items(),
        key=lambda kv: (
            safe_float(kv[1]["mean_distance"], float("inf")),
            -safe_int(kv[1]["envelope_hits"]),
            kv[0],
        ),
    )
    best_class, best = ranked[0]
    second_class, second = ranked[1] if len(ranked) > 1 else ("none", {"mean_distance": float("inf")})
    margin = safe_float(second["mean_distance"], float("inf")) - safe_float(best["mean_distance"], float("inf"))
    reason = "accepted_repeated_class"
    predicted = best_class
    if safe_int(best["present"]) < MIN_PRESENT_FEATURES:
        predicted = "unknown"
        reason = "too_few_present_features"
    elif safe_int(best["envelope_hits"]) < MIN_ENVELOPE_HITS:
        predicted = "unknown"
        reason = "too_few_envelope_hits"
    elif safe_float(best["mean_distance"]) > MAX_MEAN_DISTANCE:
        predicted = "unknown"
        reason = "mean_distance_too_high"
    elif margin < MIN_DISTANCE_MARGIN:
        predicted = "unknown"
        reason = "ambiguous_nearest_class"

    return {
        "predicted_class": predicted,
        "prediction_reason": reason,
        "nearest_class": best_class,
        "second_class": second_class,
        "nearest_mean_distance": best["mean_distance"],
        "second_mean_distance": second["mean_distance"],
        "distance_margin": margin,
        "nearest_envelope_hits": best["envelope_hits"],
        "nearest_present_features": best["present"],
        "nearest_feature_notes": best["feature_notes"],
    }


def leave_one_out_rows(
    seed_rows: Sequence[Mapping[str, Any]],
    train_classes: Sequence[str],
    selected_features: Sequence[str],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for seed_row in sorted(seed_rows, key=lambda row: safe_int(row["growth_seed"])):
        seed = safe_int(seed_row["growth_seed"])
        actual_class = str(seed_row["landscape_class"])
        actual_repeated = actual_class in train_classes
        excluded_seed = seed if actual_repeated else None
        profile_rows, _ = fit_class_profiles(
            seed_rows,
            train_classes,
            selected_features,
            excluded_seed=excluded_seed,
        )
        pred = predict_one(seed_row, train_classes, profile_rows, selected_features)
        predicted = str(pred["predicted_class"])
        out.append(
            {
                "growth_seed": seed,
                "source": seed_row["source"],
                "actual_class": actual_class,
                "actual_active_placements": seed_row["active_placements"],
                "actual_repeated_train_class": int(actual_repeated),
                "predicted_class": predicted,
                "prediction_reason": pred["prediction_reason"],
                "nearest_class": pred["nearest_class"],
                "second_class": pred["second_class"],
                "nearest_mean_distance": pred["nearest_mean_distance"],
                "second_mean_distance": pred["second_mean_distance"],
                "distance_margin": pred["distance_margin"],
                "nearest_envelope_hits": pred["nearest_envelope_hits"],
                "nearest_present_features": pred["nearest_present_features"],
                "repeated_class_hit": int(actual_repeated and predicted == actual_class),
                "repeated_class_miss": int(actual_repeated and predicted not in {actual_class, "unknown"}),
                "repeated_class_abstain": int(actual_repeated and predicted == "unknown"),
                "singleton_ood_correct_abstain": int((not actual_repeated) and predicted == "unknown"),
                "singleton_ood_false_known": int((not actual_repeated) and predicted in train_classes),
                "nearest_feature_notes": pred["nearest_feature_notes"],
            }
        )
    return out


def final_profile_rows(
    seed_rows: Sequence[Mapping[str, Any]],
    train_classes: Sequence[str],
    selected_features: Sequence[str],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    return fit_class_profiles(seed_rows, train_classes, selected_features, excluded_seed=None)


def evaluation_rows(
    loo_rows: Sequence[Mapping[str, Any]],
    selected_features: Sequence[str],
    train_classes: Sequence[str],
) -> List[Dict[str, Any]]:
    repeated = [row for row in loo_rows if safe_int(row["actual_repeated_train_class"]) == 1]
    singleton = [row for row in loo_rows if safe_int(row["actual_repeated_train_class"]) == 0]
    repeated_hits = sum(safe_int(row["repeated_class_hit"]) for row in repeated)
    repeated_abstain = sum(safe_int(row["repeated_class_abstain"]) for row in repeated)
    repeated_miss = sum(safe_int(row["repeated_class_miss"]) for row in repeated)
    singleton_abstain = sum(safe_int(row["singleton_ood_correct_abstain"]) for row in singleton)
    singleton_false_known = sum(safe_int(row["singleton_ood_false_known"]) for row in singleton)

    return [
        {
            "key": "synthesis_source",
            "value": SYNTHESIS_SOURCE,
            "evidence": "no-new-dynamics OOD-first class-stratified selector synthesis",
        },
        {
            "key": "train_classes",
            "value": ";".join(train_classes),
            "evidence": f"min_seed_count={REPEATED_CLASS_MIN_SEEDS}",
        },
        {
            "key": "selected_features",
            "value": ";".join(selected_features),
            "evidence": f"max_features={MAX_FEATURES}; max_per_family={MAX_FEATURES_PER_FAMILY}",
        },
        {
            "key": "repeated_leave_one_out_accuracy",
            "value": fmt(safe_div(repeated_hits, len(repeated))),
            "evidence": f"hits={repeated_hits}; repeated={len(repeated)}; abstain={repeated_abstain}; miss={repeated_miss}",
        },
        {
            "key": "singleton_ood_abstain_accuracy",
            "value": fmt(safe_div(singleton_abstain, len(singleton))),
            "evidence": f"abstain={singleton_abstain}; singleton={len(singleton)}; false_known={singleton_false_known}",
        },
        {
            "key": "repeated_abstain_fraction",
            "value": fmt(safe_div(repeated_abstain, len(repeated))),
            "evidence": "abstention on trainable repeated classes",
        },
        {
            "key": "selector_candidate_status",
            "value": selector_candidate_status(loo_rows),
            "evidence": "leave-one-seed-out repeated classes plus singleton OOD abstention",
        },
    ]


def selector_candidate_status(loo_rows: Sequence[Mapping[str, Any]]) -> str:
    repeated = [row for row in loo_rows if safe_int(row["actual_repeated_train_class"]) == 1]
    singleton = [row for row in loo_rows if safe_int(row["actual_repeated_train_class"]) == 0]
    repeated_acc = safe_div(sum(safe_int(row["repeated_class_hit"]) for row in repeated), len(repeated))
    repeated_abstain = safe_div(sum(safe_int(row["repeated_class_abstain"]) for row in repeated), len(repeated))
    singleton_acc = safe_div(sum(safe_int(row["singleton_ood_correct_abstain"]) for row in singleton), len(singleton))
    if repeated_acc >= 0.75 and singleton_acc >= 1.0 and repeated_abstain <= 0.25:
        return "ood_first_selector_candidate_promising_for_fresh_holdout"
    if repeated_acc >= 0.60 and singleton_acc >= 1.0:
        return "ood_first_selector_candidate_weak_but_holdout_worthy"
    if singleton_acc < 1.0 and repeated_acc >= 0.75:
        return "repeated_class_signal_but_ood_guard_failed"
    if repeated_acc < 0.60 and singleton_acc >= 1.0:
        return "ood_guard_ok_but_class_prediction_weak"
    return "selector_candidate_not_supported"


def diagnosis_rows(
    *,
    seed_rows: Sequence[Mapping[str, Any]],
    class_rows: Sequence[Mapping[str, Any]],
    selected_features: Sequence[Mapping[str, Any]],
    loo_rows: Sequence[Mapping[str, Any]],
    eval_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    status = next(row for row in eval_rows if row["key"] == "selector_candidate_status")
    repeated_acc = next(row for row in eval_rows if row["key"] == "repeated_leave_one_out_accuracy")
    ood_acc = next(row for row in eval_rows if row["key"] == "singleton_ood_abstain_accuracy")
    train_classes = next(row for row in eval_rows if row["key"] == "train_classes")
    class_counts = ";".join(
        f"{row['landscape_class']}:{row['n_seeds']}"
        for row in class_rows
    )

    if status["value"] in {
        "ood_first_selector_candidate_promising_for_fresh_holdout",
        "ood_first_selector_candidate_weak_but_holdout_worthy",
    }:
        next_status = "pre_register_fresh_ood_first_selector_holdout"
        next_note = "Kandidaten har nok no-new-dynamics signal til at neste runtime bor vaere en fresh holdout uten refit."
    elif status["value"] == "repeated_class_signal_but_ood_guard_failed":
        next_status = "harden_ood_abstention_before_runtime"
        next_note = "Klasseprediksjon ser mulig ut, men singleton/OOD-vakten er ikke trygg nok til fresh selector-run."
    elif status["value"] == "ood_guard_ok_but_class_prediction_weak":
        next_status = "improve_class_profiles_or_add_one_atlas_round"
        next_note = "OOD-abstention fungerer, men repeated-class prediksjon er for svak; mer atlas eller bedre profiler trengs."
    else:
        next_status = "do_not_spend_dynamic_budget_on_this_selector"
        next_note = "No-new-dynamics selectoren er for svak; ikke bruk fresh runtime paa denne kandidaten."

    return [
        {
            "diagnostic_family": "input_scope",
            "status": "combined_v15dq_v15dr_v15ds_no_new_dynamics",
            "note": f"Seed count={len(seed_rows)}; class counts={class_counts}.",
        },
        {
            "diagnostic_family": "class_stratification",
            "status": "repeated_classes_trainable_singletons_ood",
            "note": f"Train classes={train_classes['value']}; singletons behandles som OOD/unknown.",
        },
        {
            "diagnostic_family": "feature_selection",
            "status": "posthoc_family_diverse_candidate",
            "note": (
                f"Selected {len(selected_features)} pre-run morphology features. "
                "Dette er kandidatdesign, ikke validert selector."
            ),
        },
        {
            "diagnostic_family": "leave_one_out_result",
            "status": str(status["value"]),
            "note": (
                f"Repeated LOO accuracy={repeated_acc['value']}; singleton OOD abstain accuracy={ood_acc['value']}."
            ),
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
    class_rows: Sequence[Mapping[str, Any]],
    selected_rows: Sequence[Mapping[str, Any]],
    profile_rows: Sequence[Mapping[str, Any]],
    loo_rows: Sequence[Mapping[str, Any]],
    eval_rows: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dt: OOD-first stratified selector synthesis")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er en no-new-dynamics selector-syntese etter v15ds.")
    lines.append("Den kombinerer v15dq+v15dr+v15ds, bruker bare pre-run morphology, og evaluerer med leave-one-seed-out.")
    lines.append("Singleton-klasser behandles som OOD/unknown, ikke som trenbare klasser.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.extend(
        table(
            [
                {"field": "target", "value": TARGET_NODES},
                {"field": "perturbation", "value": PERTURBATION},
                {"field": "placements", "value": ";".join(f"p{x}" for x in PLACEMENTS)},
                {"field": "repeated_class_min_seeds", "value": REPEATED_CLASS_MIN_SEEDS},
                {"field": "max_features", "value": MAX_FEATURES},
                {"field": "synthesis_source", "value": SYNTHESIS_SOURCE},
            ],
            ("field", "value"),
        )
    )
    lines.append("")
    lines.append("## Class roles")
    lines.append("")
    lines.extend(table(class_rows, ("landscape_class", "n_seeds", "growth_seeds", "selector_role")))
    lines.append("")
    lines.append("## Selected features")
    lines.append("")
    lines.extend(
        table(
            selected_rows,
            (
                "selector_feature_rank",
                "feature",
                "feature_family",
                "macro_oriented_auc",
                "separation_score",
                "ood_outside_train_range_fraction",
            ),
        )
    )
    lines.append("")
    lines.append("## Candidate class profiles")
    lines.append("")
    lines.extend(
        table(
            profile_rows,
            (
                "landscape_class",
                "feature",
                "class_n_train",
                "class_median",
                "buffered_min",
                "buffered_max",
            ),
        )
    )
    lines.append("")
    lines.append("## Leave-one-seed-out evaluation")
    lines.append("")
    lines.extend(
        table(
            loo_rows,
            (
                "growth_seed",
                "source",
                "actual_class",
                "actual_repeated_train_class",
                "predicted_class",
                "prediction_reason",
                "nearest_class",
                "nearest_mean_distance",
                "distance_margin",
                "nearest_envelope_hits",
                "repeated_class_hit",
                "singleton_ood_correct_abstain",
            ),
        )
    )
    lines.append("")
    lines.append("## Aggregate evaluation")
    lines.append("")
    lines.extend(table(eval_rows, ("key", "value", "evidence")))
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er post-hoc kandidatdesign, ikke en validated selector.")
    lines.append("- En fresh holdout er bare berettiget hvis OOD-vakten og repeated-class treffsikkerheten begge er sterke nok.")
    lines.append("- Ikke oppgrader dette til invariant/Lorentz/partikkel/entanglement-claim.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = ["# Operativ anbefaling v0.15dt", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke kall dette validert selector uten fresh holdout.")
    lines.append("- Hvis status er holdout-worthy, neste runde maa skrive selector-spec foer dynamikk.")
    lines.append("- Hvis OOD-vakten feiler, ikke bruk mer runtime paa samme selector.")
    lines.append("- Ikke oppgrader til invariant/Lorentz/partikkel/entanglement-claim.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15dt",
            "",
            "Denne runden bruker ikke ny simulasjon. Den ser paa de klassene vi allerede har funnet, og spoer om det finnes en forsiktig maate aa kjenne dem igjen foer simulasjonen starter.",
            "",
            "Det viktigste kravet er at systemet maa kunne si `unknown` naar en startgraf ikke ligner nok paa de repeterte klassene.",
            "",
            f"- Hovedlesning: `{diag['leave_one_out_result']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}` fordi {diag['next_step']['note']}",
            "",
            "Hvis denne typen kandidat skal bli nyttig, maa den overleve en fresh holdout. Uten det er den bare et godt kartnotat.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15dt OOD-first stratified selector synthesis.")
    p.add_argument("--out-seed-features-csv", default=str(DOC / "v15dt_ood_first_selector_seed_features.csv"))
    p.add_argument("--out-class-csv", default=str(DOC / "v15dt_ood_first_selector_class_roles.csv"))
    p.add_argument("--out-feature-scores-csv", default=str(DOC / "v15dt_ood_first_selector_feature_scores.csv"))
    p.add_argument("--out-selected-csv", default=str(DOC / "v15dt_ood_first_selector_selected_features.csv"))
    p.add_argument("--out-profile-csv", default=str(DOC / "v15dt_ood_first_selector_class_profiles.csv"))
    p.add_argument("--out-normalizer-csv", default=str(DOC / "v15dt_ood_first_selector_normalizers.csv"))
    p.add_argument("--out-loo-csv", default=str(DOC / "v15dt_ood_first_selector_leave_one_out.csv"))
    p.add_argument("--out-eval-csv", default=str(DOC / "v15dt_ood_first_selector_evaluation.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15dt_ood_first_selector_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15dt_ood_first_stratified_selector_synthesis.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15dt_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15dt.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    seed_rows = load_seed_features()
    class_rows = class_count_rows(seed_rows)
    train_classes = repeated_classes(seed_rows)
    feature_rows = feature_score_rows(seed_rows, train_classes)
    selected_rows = selected_feature_rows(feature_rows)
    selected_features = [str(row["feature"]) for row in selected_rows]
    profile_rows, normalizer_rows_out = final_profile_rows(seed_rows, train_classes, selected_features)
    loo_rows = leave_one_out_rows(seed_rows, train_classes, selected_features)
    eval_rows = evaluation_rows(loo_rows, selected_features, train_classes)
    diagnosis = diagnosis_rows(
        seed_rows=seed_rows,
        class_rows=class_rows,
        selected_features=selected_rows,
        loo_rows=loo_rows,
        eval_rows=eval_rows,
    )

    write_csv(args.out_seed_features_csv, seed_rows)
    write_csv(args.out_class_csv, class_rows)
    write_csv(args.out_feature_scores_csv, feature_rows)
    write_csv(args.out_selected_csv, selected_rows)
    write_csv(args.out_profile_csv, profile_rows)
    write_csv(args.out_normalizer_csv, normalizer_rows_out)
    write_csv(args.out_loo_csv, loo_rows)
    write_csv(args.out_eval_csv, eval_rows)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            class_rows=class_rows,
            selected_rows=selected_rows,
            profile_rows=profile_rows,
            loo_rows=loo_rows,
            eval_rows=eval_rows,
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
