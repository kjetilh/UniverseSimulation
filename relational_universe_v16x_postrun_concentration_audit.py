#!/usr/bin/env python3
"""Post-run decomposition of the frozen v16x finite-diversity failure.

This audit regenerates only the declared v16x null endpoints. It verifies every
edge-set digest against the frozen output and combines the two seed families to
measure whether the 16-endpoint inclusion-rate failure persists at 32 draws.
It does not change the v16x gate status and computes no source spectrum.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import math
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v16n_coarse_event_resource_null_calibration as v16n
import relational_universe_v16v_global_edge_slot_feasibility_gate as v16v
import relational_universe_v16x_explicit_global_measure_gate as v16x


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
CONCENTRATION_AUDIT = DOC / "v16x_postrun_combined_seed_concentration.csv"
DIVERSITY_DECOMPOSITION = DOC / "v16x_postrun_diversity_decomposition.csv"
REPORT = DOC / "v16x_postrun_concentration_audit.md"


def markdown_table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = []
        for field in fields:
            value = row[field]
            values.append(f"{value:.6f}" if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return lines


def criterion_rows(summary: Mapping[str, str]) -> List[Dict[str, Any]]:
    criteria = (
        ("unique_endpoint_fraction", float(summary["primary_unique_fraction"]), v16x.MIN_UNIQUE_FRACTION, ">="),
        ("median_pairwise_changed_edge_fraction", float(summary["primary_median_pairwise_change"]), v16x.MIN_MEDIAN_PAIRWISE_CHANGE, ">="),
        ("variable_candidate_union_coverage", float(summary["primary_variable_union_coverage"]), v16x.MIN_VARIABLE_UNION_COVERAGE, ">="),
        ("effective_variable_support_ratio", float(summary["primary_effective_variable_support_ratio"]), v16x.MIN_EFFECTIVE_VARIABLE_SUPPORT_RATIO, ">="),
        ("maximum_variable_edge_inclusion_rate", float(summary["primary_max_variable_edge_inclusion_rate"]), v16x.MAX_VARIABLE_EDGE_INCLUSION_RATE, "<="),
    )
    rows: List[Dict[str, Any]] = []
    for criterion, observed, threshold, direction in criteria:
        passed = observed >= threshold if direction == ">=" else observed <= threshold
        rows.append({
            "stage": "v16x_postrun",
            "growth_seed": int(summary["growth_seed"]),
            "run_offset": int(summary["run_offset"]),
            "criterion": criterion,
            "observed": observed,
            "threshold": threshold,
            "direction": direction,
            "criterion_pass": int(passed),
        })
    return rows


def wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> tuple[float, float]:
    proportion = successes / trials
    denominator = 1.0 + z * z / trials
    center = (proportion + z * z / (2.0 * trials)) / denominator
    radius = z * math.sqrt(
        proportion * (1.0 - proportion) / trials + z * z / (4.0 * trials * trials)
    ) / denominator
    return center - radius, center + radius


def run() -> None:
    v16x.verify_outputs()
    prereg = v16i.read_csv(v16x.PRE_REGISTRATION)
    if len(prereg) != 1 or prereg[0]["script_sha256"] != v16x.file_sha256(v16x.SCRIPT):
        raise ValueError("v16x frozen script hash no longer matches preregistration")
    endpoint_rows = v16i.read_csv(v16x.ENDPOINT_AUDIT)
    expected_digests = {
        (
            int(row["growth_seed"]), int(row["run_offset"]),
            row["seed_family"], int(row["replicate"]),
        ): row["endpoint_edge_sha256"]
        for row in endpoint_rows
    }
    summaries = {
        (int(row["growth_seed"]), int(row["run_offset"])): row
        for row in v16i.read_csv(v16x.SOURCE_SUMMARY)
    }
    concentration_rows: List[Dict[str, Any]] = []
    decomposition_rows: List[Dict[str, Any]] = []
    replay_count = 0

    for run_index, (dag, metadata) in enumerate(v16x.load_runs(), start=1):
        space = v16x.build_state_space(dag, metadata, v16x.COARSE_ARM)
        flexibility = v16x.audit_flexibility(space)
        counts_by_family: Dict[str, Counter[v16x.Edge]] = {}
        for seed_family, replicate_count in (
            (v16x.PRIMARY_SEED_FAMILY, v16x.PRIMARY_REPLICATES),
            (v16x.SENSITIVITY_SEED_FAMILY, v16x.SENSITIVITY_REPLICATES),
        ):
            counts: Counter[v16x.Edge] = Counter()
            for replicate in range(replicate_count):
                _, costs = v16x.edge_costs(dag, space, seed_family, replicate)
                selected, _, _ = v16x.solve_edges(space, costs)
                digest = v16x.edge_digest(selected)
                expected = expected_digests[(
                    dag.growth_seed, dag.run_offset, seed_family, replicate,
                )]
                if digest != expected:
                    raise ValueError(
                        f"v16x endpoint replay mismatch {dag.growth_seed}/{dag.run_offset}/"
                        f"{seed_family}/{replicate}"
                    )
                replay_count += 1
                counts.update(selected & flexibility.flexible_edges)
            counts_by_family[seed_family] = counts

        primary_counts = counts_by_family[v16x.PRIMARY_SEED_FAMILY]
        sensitivity_counts = counts_by_family[v16x.SENSITIVITY_SEED_FAMILY]
        combined = primary_counts + sensitivity_counts
        variable = flexibility.flexible_edges
        ranked = sorted(variable, key=lambda edge: (-combined[edge], edge))
        top = ranked[0]
        combined_trials = v16x.PRIMARY_REPLICATES + v16x.SENSITIVITY_REPLICATES
        combined_count = combined[top]
        lower, upper = wilson_interval(combined_count, combined_trials)
        slot = space.slot_by_edge[top]
        role, age_bin, depth_relation = slot[1]
        bucket = [edge for edge in space.candidates if space.slot_by_edge[edge] == slot]
        concentration_rows.append({
            **dag.prefix,
            "globally_variable_edge_count": len(variable),
            "top_parent_event_id": top[0],
            "top_child_event_id": top[1],
            "top_edge_is_source": int(top in space.source_edges),
            "top_edge_has_concrete_conflict": int(bool(v16n.conflict_channels(metadata[top[0]], metadata[top[1]]))),
            "top_edge_source_role": v16v.role_text(role),
            "top_edge_age_bin": age_bin,
            "top_edge_depth_relation": depth_relation,
            "top_edge_slot_candidate_count": len(bucket),
            "top_edge_slot_demand": space.slot_demands[slot],
            "primary_inclusion_count": primary_counts[top],
            "primary_trial_count": v16x.PRIMARY_REPLICATES,
            "sensitivity_inclusion_count": sensitivity_counts[top],
            "sensitivity_trial_count": v16x.SENSITIVITY_REPLICATES,
            "combined_inclusion_count": combined_count,
            "combined_trial_count": combined_trials,
            "combined_inclusion_rate": combined_count / combined_trials,
            "combined_wilson_95_low": lower,
            "combined_wilson_95_high": upper,
            "maximum_allowed_rate": v16x.MAX_VARIABLE_EDGE_INCLUSION_RATE,
            "combined_rate_pass": int(combined_count / combined_trials <= v16x.MAX_VARIABLE_EDGE_INCLUSION_RATE),
            "variable_edges_included_32_of_32": sum(combined[edge] == combined_trials for edge in variable),
            "variable_edges_included_at_least_31_of_32": sum(combined[edge] >= combined_trials - 1 for edge in variable),
            "variable_edges_included_at_least_30_of_32": sum(combined[edge] >= combined_trials - 2 for edge in variable),
            "endpoint_digest_replay_pass": 1,
        })
        decomposition_rows.extend(criterion_rows(summaries[(dag.growth_seed, dag.run_offset)]))
        print(
            f"[v16x-postrun] sources={run_index}/6 "
            f"combined_max={combined_count}/{combined_trials} "
            f"edge={top[0]}->{top[1]}"
        )

    expected_replays = 6 * (v16x.PRIMARY_REPLICATES + v16x.SENSITIVITY_REPLICATES)
    if replay_count != expected_replays:
        raise ValueError("v16x post-run replay count failed")
    v16i.write_csv(CONCENTRATION_AUDIT, concentration_rows)
    v16i.write_csv(DIVERSITY_DECOMPOSITION, decomposition_rows)

    combined_passes = sum(int(row["combined_rate_pass"]) for row in concentration_rows)
    batch = v16i.read_csv(v16x.BATCH_STABILITY)
    failed_batch = [row for row in batch if not int(row["center_stability_pass"])]
    seed = v16i.read_csv(v16x.SEED_STABILITY)
    failed_seed = [row for row in seed if not int(row["center_stability_pass"])]
    lines = [
        "# v16x post-run concentration audit",
        "",
        "This audit does not change the frozen v16x result `v16x_integer_measure_endpoint_diversity_not_qualified`. It regenerates the already declared endpoints, verifies their edge-set digests, and asks why the finite gate failed.",
        "",
        f"All `{replay_count}/{expected_replays}` endpoint digests replayed exactly. No source spectrum or observed-effect statistic was computed.",
        "",
        "## Failure decomposition",
        "",
        "Uniqueness, pairwise distance, variable-edge union coverage, and effective variable support passed on all six sources. Four sources failed only because at least one globally variable edge appeared in all 16 primary endpoints. This criterion correctly remains failed in the frozen gate.",
        "",
        "## Combined independent seed families",
        "",
    ]
    lines.extend(markdown_table(concentration_rows, (
        "growth_seed", "run_offset", "top_parent_event_id", "top_child_event_id",
        "primary_inclusion_count", "sensitivity_inclusion_count",
        "combined_inclusion_rate", "combined_rate_pass",
        "variable_edges_included_32_of_32", "variable_edges_included_at_least_31_of_32",
    )))
    lines.extend([
        "",
        f"The combined 32-endpoint rate passes the old `0.95` ceiling on `{combined_passes}/6` sources. This is descriptive post-run evidence, not a retroactive gate pass.",
        "",
        "## Center stability",
        "",
        f"The frozen half-batch gate failed `{len(failed_batch)}/36` features; independent seed-family stability failed `{len(failed_seed)}/36` features.",
    ])
    if failed_batch:
        row = failed_batch[0]
        lines.extend([
            "",
            f"The half-batch failure was `{row['feature']}` at `{row['growth_seed']}/{row['run_offset']}`: absolute median shift `{float(row['absolute_center_shift']):.6f}` and range ratio `{float(row['center_shift_range_ratio']):.6f}`.",
        ])
    lines.extend([
        "",
        "## Decision boundary",
        "",
        "If the 32-endpoint combined ceiling passes broadly, the smallest next gate is a preregistered endpoint-budget extension of this same measure, not an effect test. If high-inclusion edges remain above the ceiling, the measure is genuinely concentrated on those edge choices and needs a different probability law or explicit conditioning.",
        "",
        "This audit establishes no uniformity, maximum entropy, canonical null, spectrum effect, energy, temperature, geometry, Lorentz symmetry, spacetime, particle, entanglement, or physical law.",
        "",
    ])
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[v16x-postrun] complete combined_rate_pass={combined_passes}/6")


def verify_outputs() -> None:
    concentration = v16i.read_csv(CONCENTRATION_AUDIT)
    decomposition = v16i.read_csv(DIVERSITY_DECOMPOSITION)
    if len(concentration) != 6 or len(decomposition) != 30:
        raise ValueError("v16x post-run output row counts failed")
    if not all(int(row["endpoint_digest_replay_pass"]) for row in concentration):
        raise ValueError("v16x post-run digest replay failed")
    if not REPORT.exists() or not REPORT.read_text(encoding="utf-8").strip():
        raise ValueError("v16x post-run report missing")
    print("[v16x-postrun] output verification pass")


if __name__ == "__main__":
    run()
    verify_outputs()
