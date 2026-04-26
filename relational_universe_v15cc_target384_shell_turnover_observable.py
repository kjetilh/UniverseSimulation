#!/usr/bin/env python3
"""v0.15cc target-384 shell-turnover observable.

After v15cb showed that the concrete target-384 candidate map does not
replicate cleanly, this round changes observable rather than scaling
immediately. It asks whether time-resolved shell turnover splits the broad
outer-diffuse profiles from the p2-heavy profiles more clearly than the
previous static feature summaries.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v14c_local_isotropy_diagnostics as v14c
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ac_add_chord_core_shell_lab as v15ac
import relational_universe_v15ad_add_chord_boundary_shell_lab as v15ad
import relational_universe_v15aw_local_swap_core_shell_lab as v15aw
import relational_universe_v15bl_conditional_quasi_invariant_lab as v15bl
import relational_universe_v15bv_family_structure_symmetry_lab as v15bv
import relational_universe_v15q_single_defect_recurrence_lab as v15q


TARGET = 384
GROWTH_SEED = 202
PLACEMENTS = (0, 1, 2, 3)
PERTURBATIONS = ("add_chord", "local_swap")
SEED_DELTAS = (2003, 2039, 2063)
FULL_STEPS = v15ac.FULL_STEPS
LOG_EVERY = v15ac.LOG_EVERY

QUARTET = ("add_chord_p0", "add_chord_p1", "local_swap_p0", "local_swap_p3")
P2_PAIR = ("add_chord_p2", "local_swap_p2")
TURNOVER_DISTANCE_KEYS = (
    "mean_inner_share",
    "mean_outer_share",
    "mean_shell4plus_share",
    "mean_weighted_bucket_index",
    "mean_tail_shell_entropy",
    "mean_inner_refresh",
    "mean_outer_refresh",
    "mean_turnover_gradient",
    "mean_outer_burst_rate",
    "mean_tail_damage_cv",
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    return v15.safe_float(x, default)


def mean_defined(values: Iterable[float]) -> float:
    return v15.mean_defined(values)


def write_csv(path: str | Path, rows: List[Dict[str, Any]]) -> None:
    v15.write_csv(path, rows)


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def run_seed_for(*, perturbation: str, placement: int, seed_delta: int) -> int:
    perturbation_offset = {"add_chord": 701, "local_swap": 751}[perturbation]
    return TARGET * 1_000_000 + GROWTH_SEED * 10_000 + int(placement) * 1_000 + int(seed_delta) + perturbation_offset


def bucket_distance(dist: int) -> int:
    if dist <= 0:
        return 0
    if dist == 1:
        return 1
    if dist == 2:
        return 2
    if dist == 3:
        return 3
    return 4


def entropy_of_shares(shares: Sequence[float]) -> float:
    vals = [float(x) for x in shares if float(x) > 0.0]
    if len(vals) <= 1:
        return 0.0
    total = sum(vals)
    probs = [x / total for x in vals]
    return -sum(p * math.log(p) for p in probs if p > 0.0) / math.log(len(probs))


def adjacent_jaccard(sets: Sequence[Set[int]]) -> List[float]:
    return [v15.jaccard(sets[i], sets[i + 1]) for i in range(len(sets) - 1)]


def sd_or_zero(values: Sequence[float]) -> float:
    vals = [float(v) for v in values if math.isfinite(float(v))]
    if len(vals) <= 1:
        return 0.0
    mean_v = sum(vals) / len(vals)
    return math.sqrt(sum((x - mean_v) ** 2 for x in vals) / (len(vals) - 1))


def shell_turnover_metrics(base_state: v7.State, support: Sequence[int], damaged_sets: Sequence[Set[int]]) -> Dict[str, Any]:
    tail_start = max(0, int(math.floor(v15q.TAIL_START_FRAC * len(damaged_sets))))
    tail_sets = list(damaged_sets[tail_start:])
    if not tail_sets:
        return {
            "tail_snapshot_count": 0,
            "mean_inner_share": float("nan"),
            "mean_outer_share": float("nan"),
            "mean_shell4plus_share": float("nan"),
            "mean_weighted_bucket_index": float("nan"),
            "mean_tail_shell_entropy": float("nan"),
            "mean_inner_refresh": float("nan"),
            "mean_outer_refresh": float("nan"),
            "mean_turnover_gradient": float("nan"),
            "mean_outer_burst_rate": float("nan"),
            "mean_tail_damage_cv": float("nan"),
        }

    dist_map = v7.bfs_distances(base_state.g, support)
    fallback = (max(dist_map.values()) + 1) if dist_map else 1

    bucket_sets_by_snapshot: List[Dict[int, Set[int]]] = []
    share_rows: List[Dict[str, float]] = []
    damage_sizes: List[float] = []
    for damaged in tail_sets:
        damage_sizes.append(float(len(damaged)))
        buckets: Dict[int, Set[int]] = {0: set(), 1: set(), 2: set(), 3: set(), 4: set()}
        for node in damaged:
            d = int(dist_map.get(node, fallback))
            buckets[bucket_distance(d)].add(node)
        total = max(1.0, float(len(damaged)))
        shares = {f"share_{k}": len(v) / total for k, v in buckets.items()}
        inner_share = shares["share_0"] + shares["share_1"]
        outer_share = shares["share_3"] + shares["share_4"]
        weighted_bucket_index = sum(k * shares[f"share_{k}"] for k in range(5))
        tail_shell_entropy = entropy_of_shares([shares[f"share_{k}"] for k in range(5)])
        share_rows.append(
            {
                **shares,
                "inner_share": inner_share,
                "outer_share": outer_share,
                "weighted_bucket_index": weighted_bucket_index,
                "tail_shell_entropy": tail_shell_entropy,
            }
        )
        bucket_sets_by_snapshot.append(buckets)

    inner_sets = [buckets[0].union(buckets[1]) for buckets in bucket_sets_by_snapshot]
    outer_sets = [buckets[3].union(buckets[4]) for buckets in bucket_sets_by_snapshot]
    inner_refresh = [1.0 - x for x in adjacent_jaccard(inner_sets)]
    outer_refresh = [1.0 - x for x in adjacent_jaccard(outer_sets)]
    outer_burst_rate = mean_defined(1.0 if x >= 0.65 else 0.0 for x in outer_refresh)
    mean_inner_refresh = mean_defined(inner_refresh)
    mean_outer_refresh = mean_defined(outer_refresh)

    mean_size = mean_defined(damage_sizes)
    tail_damage_cv = (sd_or_zero(damage_sizes) / mean_size) if mean_size > 0.0 and math.isfinite(mean_size) else float("nan")

    return {
        "tail_snapshot_count": len(tail_sets),
        "mean_inner_share": mean_defined(row["inner_share"] for row in share_rows),
        "mean_outer_share": mean_defined(row["outer_share"] for row in share_rows),
        "mean_shell4plus_share": mean_defined(row["share_4"] for row in share_rows),
        "mean_weighted_bucket_index": mean_defined(row["weighted_bucket_index"] for row in share_rows),
        "mean_tail_shell_entropy": mean_defined(row["tail_shell_entropy"] for row in share_rows),
        "mean_inner_refresh": mean_inner_refresh,
        "mean_outer_refresh": mean_outer_refresh,
        "mean_turnover_gradient": mean_outer_refresh - mean_inner_refresh,
        "mean_outer_burst_rate": outer_burst_rate,
        "mean_tail_damage_cv": tail_damage_cv,
    }


def classify_turnover_family(
    *,
    mean_outer_share: float,
    mean_shell4plus_share: float,
    mean_inner_refresh: float,
    mean_outer_refresh: float,
    mean_outer_burst_rate: float,
    mean_weighted_bucket_index: float,
    mean_core_share: float,
) -> str:
    if (
        mean_outer_share >= 0.58
        and mean_shell4plus_share >= 0.18
        and mean_outer_refresh <= 0.45
        and mean_core_share < 0.40
    ):
        return "outer_diffuse_persistent"
    if (
        mean_outer_share >= 0.58
        and mean_outer_refresh > 0.45
        and mean_outer_burst_rate >= 0.20
    ):
        return "outer_diffuse_turnover"
    if (
        mean_core_share >= 0.45
        and mean_inner_refresh <= 0.45
        and mean_weighted_bucket_index <= 2.20
    ):
        return "inner_core_lock"
    if mean_outer_share >= 0.52 and mean_weighted_bucket_index >= 2.35:
        return "outer_weighted_diffuse"
    return "mixed_turnover"


def aggregate_profile(rows: Sequence[Mapping[str, Any]], *, perturbation: str, placement: int) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "profile_label": v15bv.profile_label(perturbation, placement),
        "perturbation": perturbation,
        "target_nodes": TARGET,
        "growth_seed": GROWTH_SEED,
        "placement": int(placement),
        "n_runs": len(rows),
        "mean_full_coarse_return_rate": mean_defined(safe_float(row["full_coarse_return_rate"]) for row in rows),
        "mean_core_share": mean_defined(safe_float(row["core_share_of_union"]) for row in rows),
        "mean_shell_share": mean_defined(safe_float(row["shell_share_of_union"]) for row in rows),
        "mean_rare_share": mean_defined(safe_float(row["rare_share_of_union"]) for row in rows),
        "mean_abs_delta_spectral_radius_rel": mean_defined(safe_float(row["abs_delta_spectral_radius_rel"]) for row in rows),
        "mean_abs_delta_dim_proxy_rel": mean_defined(safe_float(row["abs_delta_dim_proxy_rel"]) for row in rows),
        "mean_shell_refresh": mean_defined(safe_float(row["mean_shell_refresh"]) for row in rows),
    }
    for key in TURNOVER_DISTANCE_KEYS:
        out[key] = mean_defined(safe_float(row[key]) for row in rows)
    out["turnover_family_label"] = classify_turnover_family(
        mean_outer_share=safe_float(out["mean_outer_share"], 0.0),
        mean_shell4plus_share=safe_float(out["mean_shell4plus_share"], 0.0),
        mean_inner_refresh=safe_float(out["mean_inner_refresh"], 1.0),
        mean_outer_refresh=safe_float(out["mean_outer_refresh"], 1.0),
        mean_outer_burst_rate=safe_float(out["mean_outer_burst_rate"], 0.0),
        mean_weighted_bucket_index=safe_float(out["mean_weighted_bucket_index"], 0.0),
        mean_core_share=safe_float(out["mean_core_share"], 0.0),
    )
    return out


def minmax(values: Sequence[float]) -> Tuple[float, float]:
    finite = [x for x in values if math.isfinite(x)]
    if not finite:
        return 0.0, 0.0
    return min(finite), max(finite)


def normalized_distance(a: Mapping[str, Any], b: Mapping[str, Any], keys: Sequence[str], ranges: Mapping[str, Tuple[float, float]]) -> float:
    vals: List[float] = []
    for key in keys:
        av = safe_float(a.get(key))
        bv = safe_float(b.get(key))
        lo, hi = ranges[key]
        if not math.isfinite(av) or not math.isfinite(bv):
            continue
        span = hi - lo
        vals.append(0.0 if span <= 0.0 else abs(av - bv) / span)
    return mean_defined(vals)


def pairwise_rows(aggregate: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    ranges = {key: minmax([safe_float(row.get(key)) for row in aggregate]) for key in TURNOVER_DISTANCE_KEYS}
    out: List[Dict[str, Any]] = []
    for i, a in enumerate(aggregate):
        for b in aggregate[i + 1 :]:
            dist = normalized_distance(a, b, TURNOVER_DISTANCE_KEYS, ranges)
            out.append(
                {
                    "profile_a": str(a["profile_label"]),
                    "profile_b": str(b["profile_label"]),
                    "family_a": str(a["turnover_family_label"]),
                    "family_b": str(b["turnover_family_label"]),
                    "same_turnover_family": int(str(a["turnover_family_label"]) == str(b["turnover_family_label"])),
                    "turnover_distance": dist,
                }
            )
    out.sort(key=lambda row: safe_float(row["turnover_distance"]))
    for idx, row in enumerate(out, start=1):
        row["distance_rank"] = idx
    return out


def summary_rows(aggregate: Sequence[Mapping[str, Any]], pairwise: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_profile = {str(row["profile_label"]): row for row in aggregate}
    quartet_labels = [str(by_profile[p]["turnover_family_label"]) for p in QUARTET]
    quartet_majority = max(sorted(set(quartet_labels)), key=quartet_labels.count)
    quartet_majority_count = quartet_labels.count(quartet_majority)
    p2_labels = [str(by_profile[p]["turnover_family_label"]) for p in P2_PAIR]
    p2_same = int(p2_labels[0] == p2_labels[1])
    p2_label = p2_labels[0] if p2_same else "split"

    quartet_pairs = [row for row in pairwise if str(row["profile_a"]) in QUARTET and str(row["profile_b"]) in QUARTET]
    quartet_to_p2 = [
        row
        for row in pairwise
        if (str(row["profile_a"]) in QUARTET and str(row["profile_b"]) in P2_PAIR)
        or (str(row["profile_b"]) in QUARTET and str(row["profile_a"]) in P2_PAIR)
    ]
    p2_pair = next(
        row
        for row in pairwise
        if {str(row["profile_a"]), str(row["profile_b"])} == set(P2_PAIR)
    )

    return [
        {
            "quartet_majority_label": quartet_majority,
            "quartet_majority_count": quartet_majority_count,
            "p2_pair_same_label": p2_same,
            "p2_pair_label": p2_label,
            "quartet_mean_turnover_distance": mean_defined(safe_float(row["turnover_distance"]) for row in quartet_pairs),
            "quartet_to_p2_mean_turnover_distance": mean_defined(safe_float(row["turnover_distance"]) for row in quartet_to_p2),
            "p2_pair_turnover_distance": safe_float(p2_pair["turnover_distance"]),
        }
    ]


def diagnosis_rows(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    run_rows: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    summary: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    size_clean = all(int(row["separated_from_prev"]) == 1 for row in target_summary)
    strict_match = min((int(row["requested_match"]) for row in run_rows), default=0) == 1
    quartet_majority_count = int(summary["quartet_majority_count"])
    quartet_label = str(summary["quartet_majority_label"])
    p2_same = int(summary["p2_pair_same_label"])
    p2_label = str(summary["p2_pair_label"])
    quartet_mean = safe_float(summary["quartet_mean_turnover_distance"])
    quartet_to_p2 = safe_float(summary["quartet_to_p2_mean_turnover_distance"])
    p2_pair_distance = safe_float(summary["p2_pair_turnover_distance"])

    if (
        quartet_majority_count >= 3
        and p2_same == 1
        and quartet_label != p2_label
        and quartet_label != "mixed_turnover"
        and p2_label != "mixed_turnover"
        and quartet_mean + 0.10 <= quartet_to_p2
    ):
        status = "turnover_families_supported"
        note = (
            f"Quartetet samler seg rundt `{quartet_label}` ({quartet_majority_count}/4), "
            f"p2-paret samler seg rundt `{p2_label}`, og quartetet ligger tettere internt enn mot p2."
        )
        next_step = "holdout_turnover_families"
        next_note = "Neste steg bor holde ut denne turnover-strukturen pa friske seeds."
    elif quartet_majority_count >= 3 or (p2_same == 1 and p2_label != "mixed_turnover"):
        status = "turnover_structure_weak"
        note = (
            f"Turnover-observabelen gir en svak struktur: quartet-majoritet {quartet_majority_count}/4, "
            f"p2-pair-same {p2_same}, p2-distance {fmt(p2_pair_distance)}."
        )
        next_step = "new_scale_decision"
        next_note = "Neste steg bor vaere ny skalaavgjorelse heller enn mer turnover-tuning."
    else:
        status = "turnover_structure_not_yet"
        note = (
            f"Turnover-observabelen splitter ikke target-384-profiler rent: quartet-majoritet {quartet_majority_count}/4, "
            f"p2-pair-same {p2_same}."
        )
        next_step = "new_scale_decision"
        next_note = "Neste steg bor vaere ny skalaavgjorelse."

    observed_groups = {
        label: sorted(str(row["profile_label"]) for row in aggregate if str(row["turnover_family_label"]) == label)
        for label in sorted({str(row["turnover_family_label"]) for row in aggregate})
    }
    observed_note = " | ".join(f"{label}:{','.join(vals)}" for label, vals in observed_groups.items())

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if (size_clean and strict_match) else "unclear",
            "note": (
                "Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon."
                if (size_clean and strict_match)
                else "Enten startstorrelsesseparasjon eller perturbasjonsmatching er uklar."
            ),
        },
        {
            "diagnostic_family": "turnover_structure",
            "status": status,
            "note": note,
        },
        {
            "diagnostic_family": "observed_turnover_groups",
            "status": "observed",
            "note": observed_note,
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def build_report(
    *,
    target_summary: Sequence[Mapping[str, Any]],
    aggregate: Sequence[Mapping[str, Any]],
    pairwise: Sequence[Mapping[str, Any]],
    summary: Mapping[str, Any],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15cc: target-384 shell-turnover observable")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Denne runden bruker en ny observabel: tidsopplost shell-turnover rundt support ved target `384`.")
    lines.append("Sporsmalet er om dette skiller quartetet fra p2-paret tydeligere enn de tidligere statiske family-labelene.")
    lines.append("")
    lines.append("## Startstorrelse")
    lines.append("")
    lines.append("| target | mean initial | q10 | q90 | separated |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in target_summary:
        lines.append(
            f"| {int(row['target_nodes'])} | {fmt(row['mean_initial_nodes'], 1)} | {fmt(row['q10_initial_nodes'], 1)} | {fmt(row['q90_initial_nodes'], 1)} | {int(row['separated_from_prev'])} |"
        )
    lines.append("")
    lines.append("## Aggregert turnover")
    lines.append("")
    lines.append("| profile | family | inner share | outer share | shell4+ | inner refresh | outer refresh | gradient | burst | distance |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in aggregate:
        lines.append(
            f"| {row['profile_label']} | {row['turnover_family_label']} | {fmt(row['mean_inner_share'])} | {fmt(row['mean_outer_share'])} | {fmt(row['mean_shell4plus_share'])} | {fmt(row['mean_inner_refresh'])} | {fmt(row['mean_outer_refresh'])} | {fmt(row['mean_turnover_gradient'])} | {fmt(row['mean_outer_burst_rate'])} | {fmt(row['mean_weighted_bucket_index'])} |"
        )
    lines.append("")
    lines.append("## Quartet / P2 summary")
    lines.append("")
    lines.append("| quartet majority | quartet count | p2 same | p2 label | quartet mean dist | quartet->p2 mean dist | p2 pair dist |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    lines.append(
        f"| {summary['quartet_majority_label']} | {int(summary['quartet_majority_count'])} | {int(summary['p2_pair_same_label'])} | {summary['p2_pair_label']} | {fmt(summary['quartet_mean_turnover_distance'])} | {fmt(summary['quartet_to_p2_mean_turnover_distance'])} | {fmt(summary['p2_pair_turnover_distance'])} |"
    )
    lines.append("")
    lines.append("## Naermeste turnover-par")
    lines.append("")
    lines.append("| rank | profile A | profile B | same family | turnover dist |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in pairwise[:8]:
        lines.append(
            f"| {int(row['distance_rank'])} | {row['profile_a']} | {row['profile_b']} | {int(row['same_turnover_family'])} | {fmt(row['turnover_distance'])} |"
        )
    lines.append("")
    lines.append("## Operativ lesning")
    lines.append("")
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("## Tolkning")
    lines.append("")
    lines.append("- Dette er en ny observabelklasse, ikke mer terskelarbeid pa gamle family-labels.")
    lines.append("- Positivt signal her betyr at target-384 struktur ligger i tidsopplost turnover, ikke bare i statiske tail-snitter.")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15cc target-384 shell-turnover observable.")
    p.add_argument("--out-target-csv", type=str, default="Documentation/v15cc_target384_shell_turnover_target_summary.csv")
    p.add_argument("--out-runs-csv", type=str, default="Documentation/v15cc_target384_shell_turnover_rows.csv")
    p.add_argument("--out-aggregate-csv", type=str, default="Documentation/v15cc_target384_shell_turnover_aggregate.csv")
    p.add_argument("--out-pairwise-csv", type=str, default="Documentation/v15cc_target384_shell_turnover_pairwise.csv")
    p.add_argument("--out-summary-csv", type=str, default="Documentation/v15cc_target384_shell_turnover_summary.csv")
    p.add_argument("--out-diagnosis-csv", type=str, default="Documentation/v15cc_target384_shell_turnover_diagnosis.csv")
    p.add_argument("--out-summary-md", type=str, default="Documentation/v15cc_target384_shell_turnover_observable.md")
    p.add_argument("--out-op-md", type=str, default="Documentation/v0_15cc_operativ_anbefaling.md")
    p.add_argument("--out-lay-md", type=str, default="Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cc.md")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET])
    base_states, base_rows = v10e.build_bases(ensembles, regime, [GROWTH_SEED])
    base_state = base_states[(ensembles[0].name, GROWTH_SEED)]
    base_row = next(row for row in base_rows if int(row["target_nodes"]) == TARGET and int(row["growth_seed"]) == GROWTH_SEED)
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])
    run_rows: List[Dict[str, Any]] = []

    for perturbation in PERTURBATIONS:
        for placement in PLACEMENTS:
            for seed_delta in SEED_DELTAS:
                run_seed = run_seed_for(perturbation=perturbation, placement=placement, seed_delta=seed_delta)
                res = v15q.run_defect_with_sets(
                    base_state,
                    params=params,
                    seed=run_seed,
                    steps=FULL_STEPS,
                    perturbation=perturbation,
                    center_token_index=placement,
                    local_coupling="maximal",
                    log_every=LOG_EVERY,
                )
                recurrence = v15q.recurrence_metrics(res["log_rows"], res["damaged_sets"])
                info = dict(res["perturbation_info"])
                support = [int(x) for x in info.get("support", [])]
                core_shell = (
                    v15ac.core_shell_metrics(res["damaged_sets"], support)
                    if perturbation == "add_chord"
                    else v15aw.core_shell_metrics(res["damaged_sets"], support)
                )
                shell = v15ad.shell_metrics(res["log_rows"], res["damaged_sets"])
                turnover = shell_turnover_metrics(base_state, support, res["damaged_sets"])
                drift = v15bl.relative_drift_fields(res["log_rows"][-1], base_row)
                run_rows.append(
                    {
                        "profile_label": v15bv.profile_label(perturbation, placement),
                        "perturbation": perturbation,
                        "target_nodes": TARGET,
                        "growth_seed": GROWTH_SEED,
                        "placement": int(placement),
                        "seed_delta": int(seed_delta),
                        "run_seed": int(run_seed),
                        "requested_match": int(v15.v14.perturbation_requested_match(perturbation, str(info.get("type", "unknown")))),
                        "full_coarse_return_rate": safe_float(recurrence["coarse_return_rate"]),
                        "core_share_of_union": safe_float(core_shell["core_share_of_union"]),
                        "shell_share_of_union": safe_float(core_shell["shell_share_of_union"]),
                        "rare_share_of_union": safe_float(core_shell["rare_share_of_union"]),
                        "mean_shell_refresh": safe_float(shell["mean_shell_refresh"]),
                        **turnover,
                        **drift,
                    }
                )

    aggregate = [
        aggregate_profile(
            [row for row in run_rows if str(row["perturbation"]) == perturbation and int(row["placement"]) == int(placement)],
            perturbation=perturbation,
            placement=placement,
        )
        for perturbation in PERTURBATIONS
        for placement in PLACEMENTS
    ]
    aggregate.sort(key=lambda row: (str(row["perturbation"]), int(row["placement"])))
    pairwise = pairwise_rows(aggregate)
    summary = summary_rows(aggregate, pairwise)[0]
    target_summary = [row for row in v10e.summarize_bases(base_rows) if int(row["target_nodes"]) == TARGET]
    diagnosis = diagnosis_rows(
        target_summary=target_summary,
        run_rows=run_rows,
        aggregate=aggregate,
        summary=summary,
    )
    report_md = build_report(
        target_summary=target_summary,
        aggregate=aggregate,
        pairwise=pairwise,
        summary=summary,
        diagnosis=diagnosis,
    )
    op_md = "\n".join(
        [
            "# v0.15cc operativ anbefaling",
            "",
            *[f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}" for row in diagnosis],
            "",
            "- Les dette som en ny target-384 observabelklasse, ikke som mer family-label-tuning.",
        ]
    ) + "\n"
    lay_md = "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0_15cc",
            "",
            "Denne runden ser ikke bare på hvor skaden er i senfasen, men hvor fort de ulike sonene rundt startpunktet bytter hvilke noder som er aktive.",
            "",
            "Tanken er at to mønstre kan se like ut i snitt, men likevel ha helt ulik indre turnover over tid.",
        ]
    ) + "\n"

    write_csv(args.out_target_csv, target_summary)
    write_csv(args.out_runs_csv, run_rows)
    write_csv(args.out_aggregate_csv, aggregate)
    write_csv(args.out_pairwise_csv, pairwise)
    write_csv(args.out_summary_csv, [summary])
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(report_md, encoding="utf-8")
    Path(args.out_op_md).write_text(op_md, encoding="utf-8")
    Path(args.out_lay_md).write_text(lay_md, encoding="utf-8")


if __name__ == "__main__":
    main()
