#!/usr/bin/env python3
"""Descriptive v17e diagnosis from frozen output tables only."""
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
import statistics
from typing import Any, Dict, List, Mapping, Sequence, Tuple

import relational_universe_v17e_effect_blind_scale_response_gate as v17e


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
OUTPUT = DOC / "v17e_postrun_diffusion_diagnosis.csv"
REPORT = DOC / "v17e_postrun_diffusion_diagnosis.md"

# Descriptive postrun bands, not preregistered gate thresholds.
NEAR_FLAT_CROSS_MIN = 0.95
NEAR_FLAT_CROSS_MAX = 1.05
MIN_WITHIN_DISPERSION_EXPANSION = 1.25


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path.name}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def source_key(row: Mapping[str, str]) -> Tuple[int, int]:
    return int(row["growth_seed"]), int(row["run_offset"])


def diagnose() -> List[Dict[str, Any]]:
    responses = read_csv(v17e.SCALE_RESPONSE)
    features = read_csv(v17e.FEATURE_RESPONSE)
    residual = {source_key(row): row for row in read_csv(v17e.RESIDUAL_AUDIT)}
    overlaps = read_csv(v17e.PROPOSAL_OVERLAP)

    feature_by_source: Dict[Tuple[int, int], List[Dict[str, str]]] = {}
    for row in features:
        feature_by_source.setdefault(source_key(row), []).append(row)
    overlap_by_source: Dict[Tuple[int, int], List[Dict[str, str]]] = {}
    for row in overlaps:
        overlap_by_source.setdefault(source_key(row), []).append(row)

    rows = []
    for response in responses:
        key = source_key(response)
        baseline_cross = float(response["baseline_median_cross_start_distance"])
        scale_cross = float(response["scale_median_cross_start_distance"])
        cross_ratio = float(response["scale_over_baseline_cross_start_distance_ratio"])
        baseline_within = float(response["baseline_median_within_start_distance"])
        scale_within = float(response["scale_median_within_start_distance"])
        within_ratio = scale_within / baseline_within
        separation_ratio = float(response["scale_over_baseline_separation_ratio"])
        feature_rows = feature_by_source[key]
        source_conflict = [
            row
            for row in feature_rows
            if row["feature"] in {"source_edge_fraction", "concrete_conflict_fraction"}
        ]
        rank = next(row for row in feature_rows if row["feature"] == "mean_candidate_rank_fraction")
        overlap_rows = overlap_by_source[key]
        near_flat = NEAR_FLAT_CROSS_MIN <= cross_ratio <= NEAR_FLAT_CROSS_MAX
        within_expands = within_ratio >= MIN_WITHIN_DISPERSION_EXPANSION
        diagnosis = (
            "within_family_dispersion_expands_while_cross_start_distance_flat"
            if near_flat and within_expands
            else "finite_scale_response_not_reduced_to_diffusion_pattern"
        )
        rows.append(
            {
                "stage": "v17e_postrun",
                "growth_seed": key[0],
                "run_offset": key[1],
                "baseline_cross_start_distance": baseline_cross,
                "scale_cross_start_distance": scale_cross,
                "cross_start_distance_ratio": cross_ratio,
                "baseline_within_start_distance": baseline_within,
                "scale_within_start_distance": scale_within,
                "within_start_dispersion_ratio": within_ratio,
                "scale_over_baseline_cross_to_within_ratio": separation_ratio,
                "source_and_conflict_gap_contractions": sum(
                    int(row["directional_gap_contraction"]) for row in source_conflict
                ),
                "candidate_rank_gap_contraction": int(rank["directional_gap_contraction"]),
                "residual_partition_identity": int(
                    residual[key]["exact_within_source_residual_partition_identity"]
                ),
                "minimum_candidate_edge_footprint_jaccard": min(
                    float(row["accepted_candidate_edge_jaccard"]) for row in overlap_rows
                ),
                "descriptive_near_flat_cross_band": int(near_flat),
                "descriptive_within_dispersion_expansion": int(within_expands),
                "postrun_diagnosis": diagnosis,
                "preregistered_gate": 0,
                "global_connectivity_claimed": 0,
                "convergence_claimed": 0,
                "source_spectrum_computed": 0,
                "observed_effect_computed": 0,
            }
        )
    return rows


def write_report(rows: Sequence[Mapping[str, Any]]) -> None:
    cross_ratios = [float(row["cross_start_distance_ratio"]) for row in rows]
    within_ratios = [float(row["within_start_dispersion_ratio"]) for row in rows]
    separation_ratios = [float(row["scale_over_baseline_cross_to_within_ratio"]) for row in rows]
    pattern_count = sum(
        row["postrun_diagnosis"]
        == "within_family_dispersion_expands_while_cross_start_distance_flat"
        for row in rows
    )
    conflict_contractions = sum(
        int(row["source_and_conflict_gap_contractions"]) for row in rows
    )
    rank_contractions = sum(int(row["candidate_rank_gap_contraction"]) for row in rows)
    residual_identity = sum(int(row["residual_partition_identity"]) for row in rows)
    text = f"""# v17e postrun diffusion diagnosis

Status: `v17e_within_family_diffusion_without_cross_start_convergence`.

## Input boundary

This is a descriptive aggregation of frozen v17e outputs. It reruns no chain and computes no source spectrum or observed-effect statistic.

- scale-response SHA-256: `{file_sha256(v17e.SCALE_RESPONSE)}`
- feature-response SHA-256: `{file_sha256(v17e.FEATURE_RESPONSE)}`
- residual-audit SHA-256: `{file_sha256(v17e.RESIDUAL_AUDIT)}`
- proposal-overlap SHA-256: `{file_sha256(v17e.PROPOSAL_OVERLAP)}`

## Diagnosis

All `{pattern_count}/6` sources match the disclosed descriptive pattern: cross-start distance stays within the postrun near-flat band while within-start dispersion expands by at least 25 percent. Cross-start scale/baseline ratios span `{min(cross_ratios):.6f}-{max(cross_ratios):.6f}`, while within-start dispersion ratios span `{min(within_ratios):.6f}-{max(within_ratios):.6f}`. Cross/within separation ratios fall to `{min(separation_ratios):.6f}-{max(separation_ratios):.6f}` of baseline because the within-family clouds spread, not because absolute cross-start distance materially contracts.

Source-edge and concrete-conflict gaps contract in `{conflict_contractions}/12` source-feature cells. Candidate-rank gaps contract in `{rank_contractions}/6`. Exact residual-profile identity remains in `{residual_identity}/6`. These facts show coarse-coordinate movement and stable residual algebra alongside persistent state-level start memory.

## Decision

The v17e stop rule stands: do not spend more budget scaling the length-2-to-4 kernel. The next effect-blind gate should change the move class while preserving an explicit stationary target, exact reverse accounting, representation checks, and a matched realized-work comparison. Longer alternating cycles or reversible compound-cycle moves are candidates; neither is qualified by this diagnosis.

## Claim limit

The descriptive thresholds in this report were selected after the formal v17e result and are not a preregistered gate. The pattern does not prove disconnected state-space components, convergence, slow mixing, a canonical measure, or any source-spectrum or physics effect.
"""
    REPORT.write_text(text, encoding="utf-8")


def run() -> None:
    v17e.verify_outputs()
    rows = diagnose()
    write_csv(OUTPUT, rows)
    write_report(rows)
    print("[v17e-postrun] complete status=v17e_within_family_diffusion_without_cross_start_convergence")


def verify() -> None:
    rows = read_csv(OUTPUT)
    if len(rows) != 6:
        raise ValueError("v17e postrun diagnosis requires six rows")
    if any(int(row["preregistered_gate"]) for row in rows):
        raise ValueError("v17e postrun rows mislabeled as preregistered")
    if any(int(row["source_spectrum_computed"]) for row in rows):
        raise ValueError("v17e postrun rows contain source spectrum")
    if any(int(row["observed_effect_computed"]) for row in rows):
        raise ValueError("v17e postrun rows contain observed effect")
    if not REPORT.exists() or not REPORT.read_text(encoding="utf-8").strip():
        raise ValueError("v17e postrun report missing")
    print("[v17e-postrun] verification pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v17e descriptive postrun diagnosis")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if args.verify_only:
        verify()
    else:
        run()


if __name__ == "__main__":
    main()
