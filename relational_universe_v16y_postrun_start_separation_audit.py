#!/usr/bin/env python3
"""Aggregate the frozen v16y outputs without rerunning chains or effects."""
from __future__ import annotations

from collections import defaultdict
import statistics
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"

ENDPOINTS = DOC / "v16y_chain_endpoint_audit.csv"
PAIRWISE = DOC / "v16y_chain_pairwise_distance.csv"
STABILITY = DOC / "v16y_chain_center_stability.csv"
PROFILES = DOC / "v16y_marginal_concentration_profile.csv"
GATES = DOC / "v16y_gate_evaluation.csv"

OUTPUT = DOC / "v16y_postrun_start_separation_audit.csv"
REPORT = DOC / "v16y_postrun_start_separation_audit.md"

SOURCE_START = "source_assignment"
RANDOM_START = "v16x_random_cost_a0"
CHAIN_LAW = "lazy_degree_corrected_uniform_neighbor_2x2_metropolis"
REFERENCE_LAW = "v16x_integer_random_cost_minimum_b_matching"
FEATURES = (
    "source_edge_fraction",
    "concrete_conflict_fraction",
    "mean_candidate_rank_fraction",
    "log_neighbor_degree",
)


def run_key(row: Mapping[str, str]) -> Tuple[int, int]:
    return int(row["growth_seed"]), int(row["run_offset"])


def mean(values: Iterable[float]) -> float:
    materialized = list(values)
    if not materialized:
        raise ValueError("empty aggregate")
    return statistics.mean(materialized)


def build_rows() -> List[Dict[str, Any]]:
    endpoints = v16i.read_csv(ENDPOINTS)
    pairwise = v16i.read_csv(PAIRWISE)
    stability = v16i.read_csv(STABILITY)
    profiles = v16i.read_csv(PROFILES)
    keys = sorted({run_key(row) for row in endpoints})
    if len(keys) != 6:
        raise ValueError("v16y post-run audit requires six source histories")

    endpoint_groups: Dict[Tuple[int, int, str], List[Mapping[str, str]]] = defaultdict(list)
    for row in endpoints:
        endpoint_groups[(*run_key(row), row["start_family"])].append(row)

    distance_groups: Dict[Tuple[int, int, str], List[float]] = defaultdict(list)
    for row in pairwise:
        left = row["left_start_family"]
        right = row["right_start_family"]
        relation = f"within_{left}" if left == right else "cross_start"
        distance_groups[(*run_key(row), relation)].append(float(row["changed_edge_fraction"]))

    failure_counts: Dict[Tuple[int, int, str], int] = defaultdict(int)
    for row in stability:
        if not int(row["center_stability_pass"]):
            failure_counts[(*run_key(row), row["stability_kind"])] += 1

    profile_by_key = {
        (*run_key(row), row["probability_law"]): row for row in profiles
    }
    rows: List[Dict[str, Any]] = []
    for growth_seed, run_offset in keys:
        source_rows = endpoint_groups[(growth_seed, run_offset, SOURCE_START)]
        random_rows = endpoint_groups[(growth_seed, run_offset, RANDOM_START)]
        if len(source_rows) != 16 or len(random_rows) != 16:
            raise ValueError("v16y post-run audit expected 16 endpoints per start")
        source_medians = {
            feature: statistics.median(float(row[feature]) for row in source_rows)
            for feature in FEATURES
        }
        random_medians = {
            feature: statistics.median(float(row[feature]) for row in random_rows)
            for feature in FEATURES
        }
        chain_profile = profile_by_key[(growth_seed, run_offset, CHAIN_LAW)]
        reference_profile = profile_by_key[(growth_seed, run_offset, REFERENCE_LAW)]
        rows.append({
            "growth_seed": growth_seed,
            "run_offset": run_offset,
            "source_start_median_source_edge_fraction": source_medians["source_edge_fraction"],
            "random_start_median_source_edge_fraction": random_medians["source_edge_fraction"],
            "source_start_median_concrete_conflict_fraction": source_medians["concrete_conflict_fraction"],
            "random_start_median_concrete_conflict_fraction": random_medians["concrete_conflict_fraction"],
            "source_start_median_candidate_rank_fraction": source_medians["mean_candidate_rank_fraction"],
            "random_start_median_candidate_rank_fraction": random_medians["mean_candidate_rank_fraction"],
            "source_start_median_log_neighbor_degree": source_medians["log_neighbor_degree"],
            "random_start_median_log_neighbor_degree": random_medians["log_neighbor_degree"],
            "within_source_start_mean_changed_fraction": mean(
                distance_groups[(growth_seed, run_offset, f"within_{SOURCE_START}")]
            ),
            "within_random_start_mean_changed_fraction": mean(
                distance_groups[(growth_seed, run_offset, f"within_{RANDOM_START}")]
            ),
            "cross_start_mean_changed_fraction": mean(
                distance_groups[(growth_seed, run_offset, "cross_start")]
            ),
            "start_family_failed_feature_count": failure_counts[(growth_seed, run_offset, "start_family")],
            "chain_seed_failed_feature_count": failure_counts[(growth_seed, run_offset, "independent_chain_seed_family")],
            "time_window_failed_feature_count": failure_counts[(growth_seed, run_offset, "early_vs_late_sample_window")],
            "chain_variable_edges_in_every_endpoint": chain_profile["variable_edges_included_every_endpoint"],
            "chain_maximum_variable_edge_inclusion_rate": chain_profile["maximum_variable_edge_inclusion_rate"],
            "reference_maximum_variable_edge_inclusion_rate": reference_profile["maximum_variable_edge_inclusion_rate"],
            "chain_mean_variable_edge_binary_entropy": chain_profile["mean_variable_edge_binary_entropy"],
            "reference_mean_variable_edge_binary_entropy": reference_profile["mean_variable_edge_binary_entropy"],
            "observed_interpretation": "finite_start_separation_consistent_with_slow_or_disconnected_2x2_accessibility",
            "disconnected_component_proven": 0,
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })
    return rows


def build_report(rows: Sequence[Mapping[str, Any]]) -> str:
    cross = mean(float(row["cross_start_mean_changed_fraction"]) for row in rows)
    within_source = mean(float(row["within_source_start_mean_changed_fraction"]) for row in rows)
    within_random = mean(float(row["within_random_start_mean_changed_fraction"]) for row in rows)
    variable_every = [int(row["chain_variable_edges_in_every_endpoint"]) for row in rows]
    return f"""# v16y post-run start-separation audit

## Frozen evidence

The v16y gate remains `v16y_2x2_chain_finite_centers_not_stable`. This audit only aggregates its frozen endpoint, pairwise, stability and marginal-profile CSV files. It reruns no chain, source spectrum or observed-effect statistic.

- Mean cross-start endpoint distance: `{cross:.6f}`.
- Mean within-source-start endpoint distance: `{within_source:.6f}`.
- Mean within-random-start endpoint distance: `{within_random:.6f}`.
- All `24` failed center rows are start-family comparisons: four features on each of six sources.
- Independent chain-seed and early/late-window comparisons have `0` failures.
- The chain leaves `{min(variable_every)}-{max(variable_every)}` globally variable edges present in every one of its 32 pooled endpoints per source.
- The chain maximum variable-edge inclusion rate is `1.000` on all six sources, and its mean variable-edge binary entropy is lower than the random-cost reference on all six.

## Interpretation

The implemented 2x2 chain is reversible, mobile and locally repeatable at the frozen budget, but its finite endpoint distribution remains strongly start-dependent. This is consistent with either very slow traversal or distinct accessibility components under 2x2 moves. It does **not** prove disconnection because no complete reachability or mixing argument was run.

Simply doubling the budget is not yet the most diagnostic next step: the finite chains changed only about eight percent of their own starting edges while the two endpoint clouds remain about forty-two percent apart. A targeted move-class audit can first determine whether longer alternating cycles provide explicit bridges that 2x2 swaps miss.

## Next gate

Run `v16z_alternating_cycle_bridge_gate` effect-blind on the same six state spaces and the same source/random-cost start pairs:

1. decompose each start-pair symmetric difference into valid alternating cycles;
2. report cycle-length and changed-edge coverage distributions;
3. test exact forward/reverse integrity for whole-cycle moves;
4. attempt bounded 2x2 bridge searches and label failure as unresolved, never as proof of disconnection;
5. only if a reversible longer-cycle kernel is qualified, compare its finite start/seed/time stability before any spectrum effect.

No statement here establishes global irreducibility, mixing, uniform sampling, a canonical null or physics.
"""


def verify(rows: Sequence[Mapping[str, Any]]) -> None:
    if len(rows) != 6:
        raise ValueError("v16y post-run audit row count failed")
    if any(int(row["start_family_failed_feature_count"]) != 4 for row in rows):
        raise ValueError("v16y post-run start-family failure count changed")
    if any(int(row["chain_seed_failed_feature_count"]) for row in rows):
        raise ValueError("v16y post-run seed-family failures changed")
    if any(int(row["time_window_failed_feature_count"]) for row in rows):
        raise ValueError("v16y post-run time-window failures changed")
    if any(float(row["chain_maximum_variable_edge_inclusion_rate"]) != 1.0 for row in rows):
        raise ValueError("v16y post-run chain concentration changed")
    status = next(
        row["status"] for row in v16i.read_csv(GATES) if row["gate"] == "v16y_overall"
    )
    if status != "v16y_2x2_chain_finite_centers_not_stable":
        raise ValueError("v16y post-run frozen status changed")


def main() -> None:
    rows = build_rows()
    verify(rows)
    v16i.write_csv(OUTPUT, rows)
    REPORT.write_text(build_report(rows), encoding="utf-8")
    print("[v16y-postrun] start-separation audit pass")


if __name__ == "__main__":
    main()
