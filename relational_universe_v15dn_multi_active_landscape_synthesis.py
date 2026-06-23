#!/usr/bin/env python3
"""v0.15dn multi-active landscape synthesis.

No-new-dynamics synthesis after v15dm.

Goal:
- stop treating the 1024/add_chord placement problem as a single-winner
  selector problem,
- combine the v15dl and v15dm placement landscapes,
- evaluate whether pre-run morphology can propose a small active placement set
  per base without simply selecting every placement,
- keep the result as a post-hoc observable-design screen, not a validated
  physics or selector claim.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


DOC = Path("Documentation")

TARGET_NODES = 1024
PLACEMENTS = (0, 1, 2)
ACTIVE_ESTABLISHED_RATE = 0.50

V15DL_PLACEMENT_CSV = DOC / "v15dl_base_landscape_placement_summary.csv"
V15DM_PLACEMENT_CSV = DOC / "v15dm_frozen_return_placement_summary.csv"
V15DM_MORPHOLOGY_CSV = DOC / "v15dm_frozen_return_pre_run_ranking.csv"

MORPHOLOGY_METRICS = (
    "mean_support_degree",
    "support_ball_1",
    "support_ball_2",
    "support_ball_3",
    "support_ball2_minus_ball1",
    "support_ball3_minus_ball1",
    "support_ball3_minus_ball2",
    "support_boundary_to_volume",
    "support_pairwise_mean_distance",
    "support_pairwise_max_distance",
    "ball3_over_ball1",
    "local_ball3_node_count",
    "local_ball3_beta1",
    "local_ball3_boundary_to_volume",
    "base_ball3_efficiency",
    "post_ball3_efficiency",
    "delta_ball3_efficiency",
    "base_ball3_mean_pair_distance",
    "post_ball3_mean_pair_distance",
    "delta_ball3_mean_pair_distance",
    "base_support_harmonic_reach",
    "post_support_harmonic_reach",
    "delta_support_harmonic_reach",
    "base_return_t2",
    "base_return_t4",
    "base_return_t6",
    "post_return_t2",
    "post_return_t4",
    "post_return_t6",
    "delta_return_t2",
    "delta_return_t4",
    "delta_return_t6",
    "base_return_spectral_dim_proxy",
    "post_return_spectral_dim_proxy",
    "delta_return_spectral_dim_proxy",
    "base_mean_forman_incident_support",
    "post_mean_forman_incident_support",
    "delta_mean_forman_incident_support",
    "new_edge_count",
    "new_edge_mean_forman",
    "new_edge_min_forman",
)

DYNAMIC_AUDIT_METRICS = (
    "median_w32_mean_boundary_per_mass",
    "mean_w32_mean_boundary_per_mass",
    "median_static_mean_support_degree",
    "mean_static_mean_support_degree",
    "median_genealogy_intensity_index",
    "mean_genealogy_intensity_index",
)

EPSILON_RULES = (
    ("eps_0p005", 0.005),
    ("eps_0p010", 0.010),
    ("eps_0p015", 0.015),
    ("eps_0p020", 0.020),
    ("eps_0p030", 0.030),
)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    seen = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                fieldnames.append(str(key))
                seen.add(key)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def safe_float(x: Any, default: float = float("nan")) -> float:
    try:
        if x is None or x == "":
            return default
        return float(x)
    except (TypeError, ValueError):
        return default


def safe_int(x: Any, default: int = 0) -> int:
    y = safe_float(x)
    if not math.isfinite(y):
        return default
    return int(y)


def safe_div(num: float, den: float) -> float:
    if not math.isfinite(num) or not math.isfinite(den) or den == 0:
        return float("nan")
    return num / den


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def median_defined(values: Iterable[Any]) -> float:
    vals = sorted(x for x in (safe_float(v) for v in values) if math.isfinite(x))
    if not vals:
        return float("nan")
    mid = len(vals) // 2
    if len(vals) % 2:
        return vals[mid]
    return 0.5 * (vals[mid - 1] + vals[mid])


def mean_defined(values: Iterable[Any]) -> float:
    vals = [x for x in (safe_float(v) for v in values) if math.isfinite(x)]
    return sum(vals) / len(vals) if vals else float("nan")


def pairwise_auc(positive: Sequence[float], negative: Sequence[float]) -> float:
    pos = [x for x in positive if math.isfinite(x)]
    neg = [x for x in negative if math.isfinite(x)]
    if not pos or not neg:
        return float("nan")
    wins = 0.0
    total = 0.0
    for p in pos:
        for n in neg:
            total += 1.0
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return wins / total


def rankdata(values: Sequence[float]) -> List[float]:
    pairs = sorted((v, i) for i, v in enumerate(values))
    ranks = [0.0] * len(values)
    i = 0
    while i < len(pairs):
        j = i + 1
        while j < len(pairs) and pairs[j][0] == pairs[i][0]:
            j += 1
        rank = (i + 1 + j) / 2.0
        for _, original_index in pairs[i:j]:
            ranks[original_index] = rank
        i = j
    return ranks


def spearman(xs: Sequence[Any], ys: Sequence[Any]) -> float:
    pairs = [
        (safe_float(x), safe_float(y))
        for x, y in zip(xs, ys)
        if math.isfinite(safe_float(x)) and math.isfinite(safe_float(y))
    ]
    if len(pairs) < 2:
        return float("nan")
    rx = rankdata([p[0] for p in pairs])
    ry = rankdata([p[1] for p in pairs])
    mean_x = sum(rx) / len(rx)
    mean_y = sum(ry) / len(ry)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(rx, ry))
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in rx))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ry))
    if den_x == 0.0 or den_y == 0.0:
        return float("nan")
    return num / (den_x * den_y)


def feature_family(metric: str) -> str:
    if metric.startswith("support_") or metric in {"mean_support_degree", "ball3_over_ball1"}:
        return "support_volume_topology"
    if "return" in metric:
        return "return_probability"
    if "forman" in metric or "new_edge" in metric:
        return "curvature_shortcut"
    if "efficiency" in metric or "pair_distance" in metric or "harmonic" in metric:
        return "shortcut_reach"
    if metric.startswith("local_ball3"):
        return "local_volume_topology"
    return "other"


def group_by_seed(rows: Sequence[Mapping[str, Any]]) -> Dict[int, List[Mapping[str, Any]]]:
    grouped: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[safe_int(row.get("growth_seed"))].append(row)
    return dict(sorted(grouped.items()))


def normalize_support_signature(row: Mapping[str, Any]) -> str:
    for key in ("support_signature", "support_signature_mode", "morph_support_signature"):
        val = str(row.get(key, "")).strip()
        if val:
            return val
    return ""


def morphology_for_v15dl(row: Mapping[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for metric in MORPHOLOGY_METRICS:
        if metric in row and str(row.get(metric, "")) != "":
            out[metric] = row[metric]
        elif f"morph_{metric}" in row:
            out[metric] = row[f"morph_{metric}"]
    return out


def load_combined_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []

    dl_rows = read_csv(V15DL_PLACEMENT_CSV)
    for raw in dl_rows:
        row: Dict[str, Any] = {
            "source": "v15dl",
            "target_nodes": safe_int(raw.get("target_nodes"), TARGET_NODES),
            "growth_seed": safe_int(raw.get("growth_seed")),
            "placement": safe_int(raw.get("placement")),
            "profile_label": raw.get("profile_label", f"add_chord_p{raw.get('placement', '')}"),
            "n_runs": safe_int(raw.get("n_runs")),
            "label_counts": raw.get("label_counts", ""),
            "established_rate": safe_float(raw.get("established_rate")),
            "active_placement": int(safe_float(raw.get("established_rate")) >= ACTIVE_ESTABLISHED_RATE),
            "mixed_rate": safe_float(raw.get("mixed_rate")),
            "no_horizon_rate": safe_float(raw.get("no_horizon_rate")),
            "mean_horizon_span": safe_float(raw.get("mean_high_horizon_span")),
            "median_boundary_mass": safe_float(raw.get("median_boundary_mass")),
            "median_genealogy_intensity": safe_float(raw.get("median_genealogy_intensity")),
            "support_signature": normalize_support_signature(raw),
        }
        for metric in DYNAMIC_AUDIT_METRICS:
            if metric in raw:
                row[metric] = safe_float(raw.get(metric))
        row.update(morphology_for_v15dl(raw))
        rows.append(row)

    dm_by_key = {
        (safe_int(row.get("growth_seed")), safe_int(row.get("placement"))): row
        for row in read_csv(V15DM_MORPHOLOGY_CSV)
    }
    for raw in read_csv(V15DM_PLACEMENT_CSV):
        key = (safe_int(raw.get("growth_seed")), safe_int(raw.get("placement")))
        morph = dm_by_key.get(key, {})
        established_rate = safe_float(raw.get("established_rate"))
        row = {
            "source": "v15dm",
            "target_nodes": TARGET_NODES,
            "growth_seed": key[0],
            "placement": key[1],
            "profile_label": morph.get("profile_label", f"add_chord_p{key[1]}"),
            "n_runs": safe_int(raw.get("n_runs")),
            "label_counts": raw.get("label_counts", ""),
            "established_rate": established_rate,
            "active_placement": int(established_rate >= ACTIVE_ESTABLISHED_RATE),
            "mixed_rate": safe_float(raw.get("mixed_rate")),
            "no_horizon_rate": safe_float(raw.get("no_horizon_rate")),
            "mean_horizon_span": safe_float(raw.get("mean_horizon_span")),
            "median_boundary_mass": safe_float(raw.get("median_boundary_mass")),
            "median_genealogy_intensity": safe_float(raw.get("median_genealogy_intensity")),
            "support_signature": normalize_support_signature(morph) or normalize_support_signature(raw),
            "pre_run_primary_rank": safe_int(raw.get("pre_run_primary_rank")),
            "pre_run_top1": safe_int(raw.get("pre_run_top1")),
            "pre_run_top2": safe_int(raw.get("pre_run_top2")),
        }
        for metric in MORPHOLOGY_METRICS:
            if metric in morph:
                row[metric] = safe_float(morph.get(metric))
        rows.append(row)

    rows = sorted(rows, key=lambda r: (safe_int(r["growth_seed"]), safe_int(r["placement"])))
    expected_keys = {(seed, placement) for seed in {safe_int(r["growth_seed"]) for r in rows} for placement in PLACEMENTS}
    actual_keys = {(safe_int(r["growth_seed"]), safe_int(r["placement"])) for r in rows}
    missing = sorted(expected_keys - actual_keys)
    if missing:
        raise ValueError(f"Missing placement rows for {missing}")
    return rows


def oriented_value(row: Mapping[str, Any], metric: str, direction: str) -> float:
    value = safe_float(row.get(metric))
    return -value if direction == "low" else value


def active_set(group: Sequence[Mapping[str, Any]]) -> set[int]:
    return {safe_int(row.get("placement")) for row in group if safe_int(row.get("active_placement")) == 1}


def predicted_top_k(group: Sequence[Mapping[str, Any]], metric: str, direction: str, k: int) -> set[int]:
    ranked = sorted(
        group,
        key=lambda row: (-oriented_value(row, metric, direction), safe_int(row.get("placement"))),
    )
    return {safe_int(row.get("placement")) for row in ranked[:k] if math.isfinite(oriented_value(row, metric, direction))}


def predicted_epsilon(group: Sequence[Mapping[str, Any]], metric: str, direction: str, epsilon: float) -> set[int]:
    scored = [
        (safe_int(row.get("placement")), oriented_value(row, metric, direction))
        for row in group
        if math.isfinite(oriented_value(row, metric, direction))
    ]
    if not scored:
        return set()
    best = max(score for _, score in scored)
    return {placement for placement, score in scored if best - score <= epsilon}


def predicted_above_median(group: Sequence[Mapping[str, Any]], metric: str, direction: str) -> set[int]:
    scored = [
        (safe_int(row.get("placement")), oriented_value(row, metric, direction))
        for row in group
        if math.isfinite(oriented_value(row, metric, direction))
    ]
    if not scored:
        return set()
    med = median_defined(score for _, score in scored)
    return {placement for placement, score in scored if score >= med}


def score_set_rule(
    rows: Sequence[Mapping[str, Any]],
    *,
    metric: str,
    direction: str,
    rule_type: str,
    rule_param: str,
    predictions_by_seed: Mapping[int, set[int]],
) -> Dict[str, Any]:
    by_seed = group_by_seed(rows)
    seed_details = []
    seed_count = len(by_seed)
    total_active = 0
    total_predicted = 0
    total_captured = 0
    total_missed = 0
    total_false_positive = 0
    exact_matches = 0
    full_coverage = 0
    abstains = 0
    for seed, group in by_seed.items():
        actual = active_set(group)
        predicted = set(predictions_by_seed.get(seed, set()))
        captured = actual & predicted
        missed = actual - predicted
        false_positive = predicted - actual
        total_active += len(actual)
        total_predicted += len(predicted)
        total_captured += len(captured)
        total_missed += len(missed)
        total_false_positive += len(false_positive)
        exact_matches += int(predicted == actual)
        full_coverage += int(bool(actual) and not missed)
        abstains += int(not predicted)
        seed_details.append(
            (
                f"{seed}:pred={format_set(predicted)}"
                f"/active={format_set(actual)}"
                f"/miss={format_set(missed)}"
                f"/fp={format_set(false_positive)}"
            )
        )
    coverage = safe_div(total_captured, total_active)
    precision = safe_div(total_captured, total_predicted)
    burden = safe_div(total_predicted, seed_count * len(PLACEMENTS))
    mean_predicted = safe_div(total_predicted, seed_count)
    if coverage == 1.0 and mean_predicted < len(PLACEMENTS) and total_false_positive == 0:
        status = "posthoc_exact_compact_set_candidate"
    elif coverage == 1.0 and mean_predicted < len(PLACEMENTS):
        status = "posthoc_full_coverage_nontrivial_set_candidate"
    elif coverage >= 0.80 and mean_predicted < len(PLACEMENTS):
        status = "posthoc_partial_nontrivial_set_scout"
    elif coverage == 1.0:
        status = "trivial_full_coverage_selects_all"
    else:
        status = "not_set_selector_ready"
    return {
        "metric": metric,
        "feature_family": feature_family(metric),
        "direction": direction,
        "rule_type": rule_type,
        "rule_param": rule_param,
        "seed_count": seed_count,
        "coverage_fraction": coverage,
        "precision_fraction": precision,
        "burden_fraction": burden,
        "mean_predicted_count": mean_predicted,
        "total_active": total_active,
        "total_predicted": total_predicted,
        "total_captured": total_captured,
        "total_missed": total_missed,
        "total_false_positive": total_false_positive,
        "exact_set_match_rate": safe_div(exact_matches, seed_count),
        "full_coverage_seed_rate": safe_div(full_coverage, seed_count),
        "abstain_seed_count": abstains,
        "rule_status": status,
        "seed_details": " | ".join(seed_details),
        "posthoc_warning": "rule screened after seeing v15dl/v15dm outcomes; not validated",
    }


def set_rule_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    by_seed = group_by_seed(rows)
    for metric in MORPHOLOGY_METRICS:
        if not any(math.isfinite(safe_float(row.get(metric))) for row in rows):
            continue
        for direction in ("high", "low"):
            for k in (1, 2, 3):
                predictions = {
                    seed: predicted_top_k(group, metric, direction, k)
                    for seed, group in by_seed.items()
                }
                out.append(
                    score_set_rule(
                        rows,
                        metric=metric,
                        direction=direction,
                        rule_type="top_k",
                        rule_param=str(k),
                        predictions_by_seed=predictions,
                    )
                )
            for label, epsilon in EPSILON_RULES:
                predictions = {
                    seed: predicted_epsilon(group, metric, direction, epsilon)
                    for seed, group in by_seed.items()
                }
                out.append(
                    score_set_rule(
                        rows,
                        metric=metric,
                        direction=direction,
                        rule_type="epsilon_from_best",
                        rule_param=label,
                        predictions_by_seed=predictions,
                    )
                )
            predictions = {
                seed: predicted_above_median(group, metric, direction)
                for seed, group in by_seed.items()
            }
            out.append(
                score_set_rule(
                    rows,
                    metric=metric,
                    direction=direction,
                    rule_type="above_or_equal_median",
                    rule_param="within_seed",
                    predictions_by_seed=predictions,
                )
            )
    return sorted(
        out,
        key=lambda r: (
            -safe_float(r["coverage_fraction"]),
            safe_float(r["burden_fraction"]),
            -safe_float(r["precision_fraction"]),
            safe_float(r["total_false_positive"]),
            str(r["metric"]),
            str(r["direction"]),
            str(r["rule_type"]),
            str(r["rule_param"]),
        ),
    )


def metric_score_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    active = [row for row in rows if safe_int(row.get("active_placement")) == 1]
    inactive = [row for row in rows if safe_int(row.get("active_placement")) == 0]
    out: List[Dict[str, Any]] = []
    for metric in MORPHOLOGY_METRICS:
        if not any(math.isfinite(safe_float(row.get(metric))) for row in rows):
            continue
        high_values_active = [safe_float(row.get(metric)) for row in active]
        high_values_inactive = [safe_float(row.get(metric)) for row in inactive]
        high_auc = pairwise_auc(high_values_active, high_values_inactive)
        low_auc = pairwise_auc([-x for x in high_values_active], [-x for x in high_values_inactive])
        best_direction = "high" if safe_float(high_auc) >= safe_float(low_auc) else "low"
        out.append(
            {
                "metric": metric,
                "feature_family": feature_family(metric),
                "n_active_placements": len(active),
                "n_inactive_placements": len(inactive),
                "auc_active_vs_inactive_high": high_auc,
                "auc_active_vs_inactive_low": low_auc,
                "best_direction_posthoc": best_direction,
                "best_auc_posthoc": max(safe_float(high_auc), safe_float(low_auc)),
                "spearman_vs_established_rate_raw": spearman(
                    [row.get(metric) for row in rows],
                    [row.get("established_rate") for row in rows],
                ),
                "median_active_raw": median_defined(row.get(metric) for row in active),
                "median_inactive_raw": median_defined(row.get(metric) for row in inactive),
            }
        )
    return sorted(out, key=lambda r: (-safe_float(r["best_auc_posthoc"]), str(r["metric"])))


def seed_summary_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for seed, group in group_by_seed(rows).items():
        actual = active_set(group)
        strongest = sorted(group, key=lambda r: (-safe_float(r.get("established_rate")), safe_int(r.get("placement"))))
        out.append(
            {
                "growth_seed": seed,
                "source": ";".join(sorted({str(row.get("source", "")) for row in group})),
                "placement_count": len(group),
                "active_count": len(actual),
                "active_placements": format_set(actual),
                "landscape_class": landscape_class(actual),
                "strongest_placement": f"p{safe_int(strongest[0].get('placement'))}" if strongest else "",
                "strongest_established_rate": safe_float(strongest[0].get("established_rate")) if strongest else float("nan"),
                "placement_rates": ";".join(
                    f"p{safe_int(row.get('placement'))}:{fmt(row.get('established_rate'))}"
                    for row in sorted(group, key=lambda r: safe_int(r.get("placement")))
                ),
                "support_signatures": ";".join(
                    f"p{safe_int(row.get('placement'))}:{row.get('support_signature', '')}"
                    for row in sorted(group, key=lambda r: safe_int(r.get("placement")))
                ),
            }
        )
    return out


def landscape_class(actual: set[int]) -> str:
    if not actual:
        return "no_active_placement"
    if len(actual) == 1:
        return f"single_active_p{next(iter(actual))}"
    return "multi_active_" + "_".join(f"p{x}" for x in sorted(actual))


def format_set(values: Iterable[int]) -> str:
    vals = sorted(values)
    return ";".join(f"p{x}" for x in vals) if vals else "none"


def best_nontrivial_rules(set_rules: Sequence[Mapping[str, Any]]) -> List[Mapping[str, Any]]:
    useful = []
    for row in set_rules:
        mean_predicted = safe_float(row.get("mean_predicted_count"))
        if not math.isfinite(mean_predicted) or mean_predicted >= len(PLACEMENTS):
            continue
        if str(row.get("rule_type")) == "top_k" and safe_int(row.get("rule_param"), len(PLACEMENTS)) >= len(PLACEMENTS):
            continue
        useful.append(row)
    return useful[:12]


def diagnosis_rows(
    *,
    placement_rows: Sequence[Mapping[str, Any]],
    metric_scores: Sequence[Mapping[str, Any]],
    set_rules: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    by_seed = group_by_seed(placement_rows)
    active_patterns = {tuple(sorted(active_set(group))) for group in by_seed.values()}
    active_counts = [len(active_set(group)) for group in by_seed.values()]
    best_metric = metric_scores[0] if metric_scores else {}
    nontrivial = best_nontrivial_rules(set_rules)
    best_rule = nontrivial[0] if nontrivial else (set_rules[0] if set_rules else {})
    exact_compact = [
        row for row in set_rules
        if str(row.get("rule_status")) == "posthoc_exact_compact_set_candidate"
    ]
    full_nontrivial = [
        row for row in set_rules
        if str(row.get("rule_status")) == "posthoc_full_coverage_nontrivial_set_candidate"
    ]
    trivial_full = [
        row for row in set_rules
        if str(row.get("rule_status")) == "trivial_full_coverage_selects_all"
    ]
    if exact_compact:
        set_status = "posthoc_exact_compact_set_candidate_not_validated"
        next_step = "freeze_compact_set_rule_for_fresh_multi_seed_holdout_before_claiming_selector"
        note = (
            f"Best exact compact rule is {exact_compact[0].get('metric')}/"
            f"{exact_compact[0].get('direction')}/{exact_compact[0].get('rule_type')}="
            f"{exact_compact[0].get('rule_param')}."
        )
    elif full_nontrivial:
        set_status = "posthoc_full_coverage_nontrivial_but_false_positive_set_rule"
        next_step = "treat_as_observable_design_not_selector; require_fresh_holdout_if_used"
        note = (
            f"Best nontrivial full-coverage rule still has false positives: "
            f"{full_nontrivial[0].get('seed_details')}."
        )
    elif trivial_full:
        set_status = "only_trivial_full_coverage_selects_all"
        next_step = "do_not_spend_holdout_budget_on_this_set_rule"
        note = "Full coverage is available by selecting every placement; that does not reduce uncertainty."
    else:
        set_status = "no_compact_set_rule_screen_found"
        next_step = "move_to_response_mechanism_or_new_pre_run_observable"
        note = "Existing pre-run morphology does not give a compact active-set screen on these seeds."
    return [
        {
            "diagnostic_family": "input_scope",
            "status": "no_new_dynamics_synthesis",
            "note": "Combined v15dl seeds 202/303/404 and v15dm seed 505; old dynamic outputs are reused only as response labels.",
        },
        {
            "diagnostic_family": "landscape_state",
            "status": "multi_active_base_conditioned_landscape",
            "note": (
                f"Active sets by seed: "
                f"{'; '.join(f'{seed}:{format_set(active_set(group))}' for seed, group in by_seed.items())}. "
                f"Unique active patterns={len(active_patterns)}; active count range={min(active_counts)}-{max(active_counts)}."
            ),
        },
        {
            "diagnostic_family": "placement_selector_language",
            "status": "single_winner_selector_deprioritized",
            "note": "v15dm showed active p0;p2 while frozen top1/top2 return ranking captured only one active placement.",
        },
        {
            "diagnostic_family": "metric_screen",
            "status": "posthoc_metric_audit_only",
            "note": (
                f"Best placement-level metric is {best_metric.get('metric', '')}/"
                f"{best_metric.get('best_direction_posthoc', '')} with AUC={fmt(best_metric.get('best_auc_posthoc'))}; "
                "this is descriptive because it is screened after outcomes."
            ),
        },
        {
            "diagnostic_family": "set_rule_screen",
            "status": set_status,
            "note": note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": "Do not promote any set rule without a fresh pre-registered holdout over at least two new growth seeds.",
        },
    ]


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str], limit: int | None = None) -> List[str]:
    clipped = list(rows[:limit] if limit is not None else rows)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in clipped:
        vals = []
        for field in fields:
            val = row.get(field, "")
            vals.append(fmt(val) if isinstance(val, float) else str(val))
        lines.append("| " + " | ".join(vals) + " |")
    return lines


def build_report(
    *,
    placement_rows: Sequence[Mapping[str, Any]],
    seed_rows: Sequence[Mapping[str, Any]],
    metric_scores: Sequence[Mapping[str, Any]],
    set_rules: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dn: multi-active landscape synthesis")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er en no-new-dynamics syntese etter v15dm.")
    lines.append("Den kombinerer eksisterende `1024/add_chord/p0,p1,p2`-resultater fra growth seeds `202`, `303`, `404` og `505`.")
    lines.append("Formaalet er aa teste om pre-run morfologi kan foreslaa et lite aktivt plasseringssett per base,")
    lines.append("i stedet for aa fortsette med en single-winner selector som v15dm allerede svekket.")
    lines.append("Alle set-regler her er post-hoc screens; de er observabeldesign, ikke validerte selectors.")
    lines.append("")
    lines.append("## Seed landscapes")
    lines.append("")
    lines.extend(table(seed_rows, ("growth_seed", "source", "landscape_class", "active_placements", "placement_rates")))
    lines.append("")
    lines.append("## Placement rows")
    lines.append("")
    lines.extend(
        table(
            placement_rows,
            (
                "growth_seed",
                "placement",
                "source",
                "label_counts",
                "established_rate",
                "active_placement",
                "support_signature",
                "delta_return_t2",
                "delta_return_t4",
                "base_return_spectral_dim_proxy",
            ),
        )
    )
    lines.append("")
    lines.append("## Best placement-level morphology audits")
    lines.append("")
    lines.extend(
        table(
            metric_scores,
            (
                "metric",
                "feature_family",
                "best_direction_posthoc",
                "best_auc_posthoc",
                "spearman_vs_established_rate_raw",
                "median_active_raw",
                "median_inactive_raw",
            ),
            limit=12,
        )
    )
    lines.append("")
    lines.append("## Best active-set screens")
    lines.append("")
    lines.extend(
        table(
            set_rules,
            (
                "metric",
                "direction",
                "rule_type",
                "rule_param",
                "coverage_fraction",
                "precision_fraction",
                "burden_fraction",
                "mean_predicted_count",
                "exact_set_match_rate",
                "total_false_positive",
                "rule_status",
            ),
            limit=16,
        )
    )
    lines.append("")
    lines.append("## Best nontrivial active-set screens")
    lines.append("")
    lines.extend(
        table(
            best_nontrivial_rules(set_rules),
            (
                "metric",
                "direction",
                "rule_type",
                "rule_param",
                "coverage_fraction",
                "precision_fraction",
                "burden_fraction",
                "mean_predicted_count",
                "exact_set_match_rate",
                "total_false_positive",
                "rule_status",
            ),
            limit=12,
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
    lines.append("- Resultatet skal ikke brukes som Lorentz-, invariant-, entanglement-, partikkel- eller universell-geometri-evidens.")
    lines.append("- Hvis en set-regel ser lovende ut, er den en kandidat til frossen holdout, ikke en oppdaget lov.")
    lines.append("- Hvis full coverage krever aa velge alle placements, har regelen ikke redusert usikkerhet.")
    lines.append("- Det interessante spoersmaalet etter v15dn er om vi kan lage en pre-run observabel som predikerer aktivt sett med lavere burden enn `p0;p1;p2`.")
    lines.append("")
    return "\n".join(lines)


def build_recommendation(diagnosis: Sequence[Mapping[str, Any]], set_rules: Sequence[Mapping[str, Any]]) -> str:
    status_by_family = {str(row["diagnostic_family"]): str(row["status"]) for row in diagnosis}
    best_nontrivial = best_nontrivial_rules(set_rules)
    lines = [
        "# Operativ anbefaling v0.15dn",
        "",
        "## Kortversjon",
        "",
        "v15dn flytter add_chord/1024-problemet fra single-winner selector til aktivt-sett-landskap.",
        "Dette er riktig retning fordi v15dm viste at samme base kan ha mer enn en aktiv placement.",
        "",
        "## Status",
        "",
        f"- Landskap: `{status_by_family.get('landscape_state', '')}`.",
        f"- Set-regel: `{status_by_family.get('set_rule_screen', '')}`.",
        f"- Neste steg: `{status_by_family.get('next_step', '')}`.",
        "",
        "## Praktisk anbefaling",
        "",
    ]
    if best_nontrivial:
        best = best_nontrivial[0]
        lines.append(
            f"- Beste ikke-trivielle screen akkurat naa er `{best.get('metric')}`/"
            f"`{best.get('direction')}`/`{best.get('rule_type')}={best.get('rule_param')}` "
            f"med coverage `{fmt(best.get('coverage_fraction'))}` og burden `{fmt(best.get('burden_fraction'))}`."
        )
        lines.append("- Ikke kjor fresh holdout foer vi har bestemt om denne regelen skal fryses uten videre justering.")
    else:
        lines.append("- Ingen ikke-triviell set-regel er sterk nok til holdout. Bygg en ny pre-run observabel foerst.")
    lines.append("- Unngaa aa refitte genealogy-intensity eller dynamiske responser inn i selector-claim; de er response/audit, ikke pre-run.")
    lines.append("- Hvis vi bruker ny dynamikk, boer den teste en frossen aktivt-sett-regel paa minst to nye growth seeds.")
    lines.append("")
    return "\n".join(lines)


def build_non_specialist_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Relasjonell universgraf for ikke-spesialister v0.15dn",
        "",
        "Denne runden handler om en ganske jordna metodefeil vi vil unngaa:",
        "naar vi tester tre mulige lokale inngrep i samme graf, kan det hende at mer enn ett av dem er aktivt.",
        "Da blir det feil aa late som oppgaven alltid er aa finne en enkelt vinner.",
        "",
        "v15dn bruker derfor gamle resultater og spoer: kan vi, foer dynamikken kjoeres, se nok i lokal grafmorfologi til aa foreslaa et lite sett av aktive kandidater?",
        "Det er nyttig bare hvis settet er mindre enn aa velge alt.",
        "",
        "## Hva vi ikke paastaar",
        "",
        "- Vi paastaar ikke at dette er partikler.",
        "- Vi paastaar ikke Lorentz-likhet eller romtid.",
        "- Vi paastaar ikke en invariant.",
        "- Vi bruker dette som strengere instrumentering for aa se om signalet er reproduserbart.",
        "",
        "## Hva som teller som fremgang",
        "",
        "Fremgang her er ikke et stort ord, men en bedre beslutning:",
        "enten finner vi en liten frossen regel som fortjener fresh holdout,",
        "eller saa laerer vi at dagens pre-run morfologi ikke er nok og maa byttes ut.",
        "",
        "## Operativ diagnose",
        "",
    ]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}`.")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-report", default=str(DOC / "v15dn_multi_active_landscape_synthesis.md"))
    p.add_argument("--out-placement-csv", default=str(DOC / "v15dn_multi_active_landscape_placement_rows.csv"))
    p.add_argument("--out-seed-csv", default=str(DOC / "v15dn_multi_active_landscape_seed_summary.csv"))
    p.add_argument("--out-set-rule-csv", default=str(DOC / "v15dn_multi_active_landscape_set_rule_scores.csv"))
    p.add_argument("--out-metric-csv", default=str(DOC / "v15dn_multi_active_landscape_metric_scores.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15dn_multi_active_landscape_diagnosis.csv"))
    p.add_argument("--out-recommendation-md", default=str(DOC / "v0_15dn_operativ_anbefaling.md"))
    p.add_argument(
        "--out-non-specialist-md",
        default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15dn.md"),
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    placement_rows = load_combined_rows()
    seed_rows = seed_summary_rows(placement_rows)
    metric_scores = metric_score_rows(placement_rows)
    set_rules = set_rule_rows(placement_rows)
    diagnosis = diagnosis_rows(
        placement_rows=placement_rows,
        metric_scores=metric_scores,
        set_rules=set_rules,
    )

    write_csv(Path(args.out_placement_csv), placement_rows)
    write_csv(Path(args.out_seed_csv), seed_rows)
    write_csv(Path(args.out_metric_csv), metric_scores)
    write_csv(Path(args.out_set_rule_csv), set_rules)
    write_csv(Path(args.out_diagnosis_csv), diagnosis)
    Path(args.out_report).write_text(
        build_report(
            placement_rows=placement_rows,
            seed_rows=seed_rows,
            metric_scores=metric_scores,
            set_rules=set_rules,
            diagnosis=diagnosis,
        )
    )
    Path(args.out_recommendation_md).write_text(build_recommendation(diagnosis, set_rules))
    Path(args.out_non_specialist_md).write_text(build_non_specialist_note(diagnosis))

    print(f"Wrote {args.out_report}")
    print(f"Wrote {args.out_set_rule_csv}")
    print(f"Wrote {args.out_diagnosis_csv}")


if __name__ == "__main__":
    main()
