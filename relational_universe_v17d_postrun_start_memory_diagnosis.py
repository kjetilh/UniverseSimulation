#!/usr/bin/env python3
"""Descriptive postrun diagnosis of the frozen v17d outputs.

This script reruns no chain and computes no source spectrum or effect metric.
It separates contracting start-sensitive feature gaps from direct endpoint
distance and audits exact residual-component profile identity within source.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import csv
import hashlib
from pathlib import Path
import statistics
from typing import Any, Dict, List, Mapping, Sequence, Tuple

import relational_universe_v16i_causal_interval_abundance_gate as v16i
import relational_universe_v17d_effect_blind_finite_stability as v17d


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
DIAGNOSIS_CSV = DOC / "v17d_postrun_start_memory_diagnosis.csv"
RESIDUAL_AUDIT_CSV = DOC / "v17d_postrun_residual_partition_audit.csv"
REPORT = DOC / "v17d_postrun_start_memory_diagnosis.md"

FEATURES = (
    "source_edge_fraction",
    "concrete_conflict_fraction",
    "mean_candidate_rank_fraction",
)
STARTS = v17d.START_FAMILIES


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_key(row: Mapping[str, str]) -> Tuple[int, int]:
    return int(row["growth_seed"]), int(row["run_offset"])


def median_feature_rows(endpoints: Sequence[Mapping[str, str]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[int, int, str, str, str], List[float]] = defaultdict(list)
    for row in endpoints:
        for feature in FEATURES:
            grouped[(*source_key(row), row["window"], row["start_family"], feature)].append(
                float(row[feature])
            )
    rows = []
    sources = sorted({source_key(row) for row in endpoints})
    for growth_seed, run_offset in sources:
        for feature in FEATURES:
            gaps = {}
            medians = {}
            for window in ("early", "late"):
                for start in STARTS:
                    medians[(window, start)] = statistics.median(
                        grouped[(growth_seed, run_offset, window, start, feature)]
                    )
                gaps[window] = abs(
                    medians[(window, STARTS[0])] - medians[(window, STARTS[1])]
                )
            rows.append({
                "stage": "v17d_postrun",
                "growth_seed": growth_seed,
                "run_offset": run_offset,
                "diagnostic_kind": "start_feature_gap",
                "metric": feature,
                "early_value": gaps["early"],
                "late_value": gaps["late"],
                "late_over_early": gaps["late"] / gaps["early"] if gaps["early"] else 0.0,
                "directional_contraction": int(gaps["late"] < gaps["early"]),
                "preregistered_gate": 0,
                "source_spectrum_computed": 0,
                "observed_effect_computed": 0,
            })
    return rows


def cross_start_distance_rows(pairwise: Sequence[Mapping[str, str]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[int, int, str], List[float]] = defaultdict(list)
    for row in pairwise:
        if row["left_start_family"] == row["right_start_family"]:
            continue
        if row["left_window"] != row["right_window"]:
            continue
        grouped[(*source_key(row), row["left_window"])].append(
            float(row["changed_edge_fraction"])
        )
    rows = []
    sources = sorted({(key[0], key[1]) for key in grouped})
    for growth_seed, run_offset in sources:
        early = statistics.median(grouped[(growth_seed, run_offset, "early")])
        late = statistics.median(grouped[(growth_seed, run_offset, "late")])
        rows.append({
            "stage": "v17d_postrun",
            "growth_seed": growth_seed,
            "run_offset": run_offset,
            "diagnostic_kind": "cross_start_endpoint_distance",
            "metric": "median_changed_edge_fraction",
            "early_value": early,
            "late_value": late,
            "late_over_early": late / early if early else 0.0,
            "directional_contraction": int(late < early),
            "preregistered_gate": 0,
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })
    return rows


def residual_audit_rows(profiles: Sequence[Mapping[str, str]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[int, int], List[Mapping[str, str]]] = defaultdict(list)
    for row in profiles:
        grouped[source_key(row)].append(row)
    rows = []
    for (growth_seed, run_offset), source_rows in sorted(grouped.items()):
        digests = {row["residual_component_profile_sha256"] for row in source_rows}
        jaccards = [float(row["source_flexible_edge_jaccard"]) for row in source_rows]
        rows.append({
            "stage": "v17d_postrun",
            "growth_seed": growth_seed,
            "run_offset": run_offset,
            "representative_endpoint_count": len(source_rows),
            "start_family_count": len({row["start_family"] for row in source_rows}),
            "seed_family_count": len({row["chain_seed_family"] for row in source_rows}),
            "window_count": len({row["window"] for row in source_rows}),
            "unique_residual_component_profile_count": len(digests),
            "minimum_source_flexible_edge_jaccard": min(jaccards),
            "maximum_source_flexible_edge_jaccard": max(jaccards),
            "exact_within_source_residual_partition_identity": int(
                len(source_rows) == 8 and len(digests) == 1 and min(jaccards) == 1.0
            ),
            "bounded_cycle_state_graph_connectivity_claimed": 0,
            "source_spectrum_computed": 0,
            "observed_effect_computed": 0,
        })
    return rows


def write_report(
    diagnosis: Sequence[Mapping[str, Any]],
    residual: Sequence[Mapping[str, Any]],
) -> None:
    feature = [row for row in diagnosis if row["diagnostic_kind"] == "start_feature_gap"]
    distance = [row for row in diagnosis if row["diagnostic_kind"] == "cross_start_endpoint_distance"]
    source_conflict = [
        row for row in feature
        if row["metric"] in {"source_edge_fraction", "concrete_conflict_fraction"}
    ]
    rank = [row for row in feature if row["metric"] == "mean_candidate_rank_fraction"]
    text = f"""# v17d postrun start-memory diagnosis

Status: `v17d_start_sensitive_features_contract_but_endpoint_separation_persists`.

## Input boundary

This is a descriptive postrun aggregation of the frozen v17d CSV files. It reruns no chain and computes no source spectrum or observed-effect statistic.

- endpoint input SHA-256: `{file_sha256(v17d.ENDPOINT_AUDIT)}`
- pairwise input SHA-256: `{file_sha256(v17d.PAIRWISE_DISTANCE)}`
- residual-profile input SHA-256: `{file_sha256(v17d.COMPONENT_PROFILE)}`

## Diagnosis

The early-to-late gap contracts for source-edge fraction and concrete-conflict fraction in `{sum(int(row['directional_contraction']) for row in source_conflict)}/{len(source_conflict)}` source-feature cells. Candidate-rank gap contracts in `{sum(int(row['directional_contraction']) for row in rank)}/{len(rank)}` sources. This is directional finite movement, not convergence.

Direct cross-start endpoint distance contracts in `{sum(int(row['directional_contraction']) for row in distance)}/{len(distance)}` sources, but the late/early ratios span `{min(float(row['late_over_early']) for row in distance):.6f}` to `{max(float(row['late_over_early']) for row in distance):.6f}`. The state-level separation is therefore effectively flat over the observed windows even while selected coarse features move toward each other.

All `{sum(int(row['exact_within_source_residual_partition_identity']) for row in residual)}/{len(residual)}` sources have one exact residual-component profile digest across both starts, both seeds and both windows, with flexible-edge Jaccard `1.0`. This rules out a changing residual-SCC partition as the explanation for the observed start memory. It does not prove that the length-2-to-4 proposal state graph is connected.

## Next decision

One bounded effect-blind scale extension is justified because traversal, resource, seed agreement, time-window distance agreement, residual profiles and proposal-node overlap passed while start memory remained and the start-sensitive feature gaps moved directionally. The next gate must checkpoint a substantially longer chain and test whether direct cross-start distance responds to scale. If it remains flat, stop scaling this kernel and change the move class. Source effects remain closed.

## Claim limit

This diagnosis does not establish convergence, slow mixing, hidden disconnection, a canonical measure or any physical effect. It only separates observed feature contraction from persistent endpoint separation in the finite v17d data.
"""
    REPORT.write_text(text, encoding="utf-8")


def run() -> None:
    v17d.verify_outputs()
    endpoints = read_rows(v17d.ENDPOINT_AUDIT)
    pairwise = read_rows(v17d.PAIRWISE_DISTANCE)
    profiles = read_rows(v17d.COMPONENT_PROFILE)
    diagnosis = median_feature_rows(endpoints) + cross_start_distance_rows(pairwise)
    residual = residual_audit_rows(profiles)
    v16i.write_csv(DIAGNOSIS_CSV, diagnosis)
    v16i.write_csv(RESIDUAL_AUDIT_CSV, residual)
    write_report(diagnosis, residual)
    print("[v17d-postrun] complete status=v17d_start_sensitive_features_contract_but_endpoint_separation_persists")


def verify() -> None:
    diagnosis = read_rows(DIAGNOSIS_CSV)
    residual = read_rows(RESIDUAL_AUDIT_CSV)
    if len(diagnosis) != 24 or len(residual) != 6:
        raise ValueError("v17d postrun row counts failed")
    if any(int(row["source_spectrum_computed"]) for row in diagnosis + residual):
        raise ValueError("v17d postrun source spectrum exclusion failed")
    if any(int(row["observed_effect_computed"]) for row in diagnosis + residual):
        raise ValueError("v17d postrun effect exclusion failed")
    if not all(int(row["exact_within_source_residual_partition_identity"]) for row in residual):
        raise ValueError("v17d postrun residual identity summary changed")
    if not REPORT.exists() or not REPORT.read_text(encoding="utf-8").strip():
        raise ValueError("v17d postrun report missing")
    print("[v17d-postrun] verification pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v17d postrun start-memory diagnosis")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if args.verify_only:
        verify()
    else:
        run()


if __name__ == "__main__":
    main()
