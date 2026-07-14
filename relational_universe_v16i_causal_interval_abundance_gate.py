#!/usr/bin/env python3
"""v16i: preregistered causal-interval abundance analysis holdout.

The primary observable is the dyadic distribution of open interval volumes for
all comparable pairs in an intrinsic event DAG.  The structural null preserves
event count, scheduler order, every event's indegree, and the complete causal-
depth layer profile while rewiring direct parents.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple


ROOT = Path(__file__).resolve().parent
DOC = ROOT / "Documentation"
PURPOSE_REF = "purpose://prompt.unknown"

CALIBRATION_STAGES = ("v16c", "v16d")
HOLDOUT_STAGE = "v16h"
PRIMARY_ARM = "exposure_matched_local"
ARMS = ("current_global", PRIMARY_ARM)
RUN_FIELDS = ("growth_seed", "run_offset", "arm", "run_seed")

INTERVAL_BINS: Tuple[Tuple[str, int, int], ...] = (
    ("open_0", 0, 0),
    ("open_1", 1, 1),
    ("open_2_3", 2, 3),
    ("open_4_7", 4, 7),
    ("open_8_15", 8, 15),
    ("open_16_31", 16, 31),
    ("open_32_63", 32, 63),
    ("open_64_127", 64, 127),
    ("open_128_plus", 128, 10**18),
)
NULL_FAMILY = "scheduler_order_layer_indegree_rewire"
NULL_REPLICATES = 64
ISOMORPHISM_REPLAYS = 2
EPSILON = 1e-15

MIN_LOCAL_MEDIAN_EFFECT_RATIO = 2.0
MIN_LOCAL_POSITIVE_FRACTION = 5.0 / 6.0
MIN_LOCAL_P_LE_010_FRACTION = 0.5
MAX_EMPIRICAL_P = 0.10
GROUP_MIN_MEDIAN_EFFECT_RATIO = 1.0
GROUP_MIN_POSITIVE_FRACTION = 5.0 / 6.0
TARGET_TRANSFER_RANGE = (0.5, 2.0)

STAGE_FILES = {
    "v16c": {
        "events": "v16c_event_log.csv",
        "edges": "v16c_fine_dependency_edges.csv",
        "runs": "v16c_run_summary.csv",
        "gates": "v16c_gate_evaluation.csv",
        "expected": "pass_to_v16d_scale_holdout",
        "target": 1024,
    },
    "v16d": {
        "events": "v16d_event_log.csv",
        "edges": "v16d_fine_dependency_edges.csv",
        "runs": "v16d_run_summary.csv",
        "gates": "v16d_gate_evaluation.csv",
        "expected": "pass_to_v16e_independent_coarse_map_gate",
        "target": 1536,
    },
    "v16h": {
        "events": "v16h_event_log.csv",
        "edges": "v16h_fine_dependency_edges.csv",
        "runs": "v16h_run_summary.csv",
        "gates": "v16h_gate_evaluation.csv",
        "expected": "total_rate_mechanism_validated_retire_clock_depth_common_geometry",
        "target": 1536,
    },
}

CALIBRATION_RUNS = DOC / "v16i_design_calibration_interval_runs.csv"
CALIBRATION_SPECTRA = DOC / "v16i_design_calibration_interval_spectra.csv"
CALIBRATION_NULLS = DOC / "v16i_design_calibration_null_distribution.csv"
CALIBRATION_NULL_AUDIT = DOC / "v16i_design_calibration_null_integrity.csv"
DESIGN_SELECTION = DOC / "v16i_design_selection.csv"
FROZEN_BASELINE = DOC / "v16i_frozen_v16d_interval_baseline.csv"
PRE_REGISTRATION = DOC / "v16i_pre_registration.csv"
SOURCE_CHAIN = DOC / "v16i_source_chain.csv"


@dataclass(frozen=True)
class RunDAG:
    stage: str
    target_nodes: int
    growth_seed: int
    run_offset: int
    arm: str
    run_seed: int
    predecessors: Tuple[Tuple[int, ...], ...]
    depths: Tuple[int, ...]
    indegrees: Tuple[int, ...]

    @property
    def prefix(self) -> Dict[str, Any]:
        return {
            "stage": self.stage,
            "target_nodes": self.target_nodes,
            "growth_seed": self.growth_seed,
            "run_offset": self.run_offset,
            "arm": self.arm,
            "run_seed": self.run_seed,
        }

    @property
    def key(self) -> Tuple[int, int, str, int]:
        return (self.growth_seed, self.run_offset, self.arm, self.run_seed)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_seed(*parts: Any) -> int:
    payload = "|".join(str(part) for part in parts).encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def median(values: Iterable[float]) -> float:
    data = list(values)
    if not data:
        raise ValueError("median requires data")
    return statistics.median(data)


def mean(values: Iterable[float]) -> float:
    data = list(values)
    if not data:
        raise ValueError("mean requires data")
    return statistics.mean(data)


def spec_payload() -> Dict[str, Any]:
    return {
        "purpose_ref": PURPOSE_REF,
        "calibration_stages": list(CALIBRATION_STAGES),
        "holdout_stage": HOLDOUT_STAGE,
        "primary_arm": PRIMARY_ARM,
        "interval_bins": [list(row) for row in INTERVAL_BINS],
        "primary_metric": "full_spectrum_jensen_shannon_effect_ratio",
        "null_family": NULL_FAMILY,
        "null_preserves": [
            "event_count",
            "scheduler_order",
            "per_event_indegree",
            "per_event_causal_depth",
            "causal_depth_layer_profile",
        ],
        "null_replicates": NULL_REPLICATES,
        "isomorphism_replays": ISOMORPHISM_REPLAYS,
        "epsilon": EPSILON,
        "thresholds": {
            "min_local_median_effect_ratio": MIN_LOCAL_MEDIAN_EFFECT_RATIO,
            "min_local_positive_fraction": MIN_LOCAL_POSITIVE_FRACTION,
            "max_empirical_p": MAX_EMPIRICAL_P,
            "min_local_p_le_010_fraction": MIN_LOCAL_P_LE_010_FRACTION,
            "group_min_median_effect_ratio": GROUP_MIN_MEDIAN_EFFECT_RATIO,
            "group_min_positive_fraction": GROUP_MIN_POSITIVE_FRACTION,
            "target_transfer_range": list(TARGET_TRANSFER_RANGE),
        },
    }


def spec_digest() -> str:
    payload = json.dumps(spec_payload(), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def run_key(row: Mapping[str, Any]) -> Tuple[int, int, str, int]:
    return (
        int(row["growth_seed"]),
        int(row["run_offset"]),
        str(row["arm"]),
        int(row["run_seed"]),
    )


def source_status(stage: str) -> str:
    rows = read_csv(DOC / STAGE_FILES[stage]["gates"])
    overall = [row for row in rows if row["gate"] == f"{stage}_overall"]
    if len(overall) != 1:
        raise ValueError(f"missing {stage} overall gate")
    return overall[0]["status"]


def recompute_depths(predecessors: Sequence[Sequence[int]]) -> List[int]:
    depths: List[int] = []
    for child, parents in enumerate(predecessors):
        if any(parent < 0 or parent >= child for parent in parents):
            raise ValueError(f"non-topological parent at child {child}")
        depths.append(0 if not parents else 1 + max(depths[parent] for parent in parents))
    return depths


def load_stage(stage: str) -> List[RunDAG]:
    config = STAGE_FILES[stage]
    if source_status(stage) != config["expected"]:
        raise ValueError(f"unexpected {stage} status")
    event_rows = read_csv(DOC / config["events"])
    edge_rows = read_csv(DOC / config["edges"])
    run_rows = read_csv(DOC / config["runs"])
    events_by_key: Dict[Tuple[int, int, str, int], List[Dict[str, str]]] = defaultdict(list)
    edges_by_key: Dict[Tuple[int, int, str, int], List[Dict[str, str]]] = defaultdict(list)
    for row in event_rows:
        events_by_key[run_key(row)].append(row)
    for row in edge_rows:
        edges_by_key[run_key(row)].append(row)
    expected_keys = {run_key(row) for row in run_rows}
    if set(events_by_key) != expected_keys or set(edges_by_key) != expected_keys:
        raise ValueError(f"{stage} event/edge/run keys disagree")
    dags: List[RunDAG] = []
    for key in sorted(expected_keys):
        events = sorted(events_by_key[key], key=lambda row: int(row["event_id"]))
        if [int(row["event_id"]) for row in events] != list(range(len(events))):
            raise ValueError(f"{stage} non-contiguous event ids: {key}")
        predecessors: List[List[int]] = [[] for _ in events]
        for edge in edges_by_key[key]:
            parent = int(edge["parent_event_id"])
            child = int(edge["child_event_id"])
            predecessors[child].append(parent)
        predecessors = [sorted(set(parents)) for parents in predecessors]
        depths = recompute_depths(predecessors)
        observed_depths = [int(row["causal_depth"]) for row in events]
        observed_indegrees = [int(row["indegree"]) for row in events]
        if depths != observed_depths:
            raise ValueError(f"{stage} depth reconstruction failed: {key}")
        if [len(parents) for parents in predecessors] != observed_indegrees:
            raise ValueError(f"{stage} indegree reconstruction failed: {key}")
        for row, parents in zip(events, predecessors):
            logged = [] if not row["direct_predecessors"] else sorted(int(value) for value in row["direct_predecessors"].split(";"))
            if logged != parents:
                raise ValueError(f"{stage} direct predecessor log failed: {key}")
        dags.append(RunDAG(
            stage=stage,
            target_nodes=int(config["target"]),
            growth_seed=key[0],
            run_offset=key[1],
            arm=key[2],
            run_seed=key[3],
            predecessors=tuple(tuple(parents) for parents in predecessors),
            depths=tuple(depths),
            indegrees=tuple(observed_indegrees),
        ))
    return dags


def transitive_closure(predecessors: Sequence[Sequence[int]]) -> Tuple[List[int], List[int]]:
    n_events = len(predecessors)
    ancestors = [0] * n_events
    successors: List[List[int]] = [[] for _ in range(n_events)]
    for child, parents in enumerate(predecessors):
        bits = 0
        for parent in parents:
            bits |= ancestors[parent] | (1 << parent)
            successors[parent].append(child)
        ancestors[child] = bits
    descendants = [0] * n_events
    for parent in range(n_events - 1, -1, -1):
        bits = 0
        for child in successors[parent]:
            bits |= descendants[child] | (1 << child)
        descendants[parent] = bits
    return ancestors, descendants


def interval_spectrum(predecessors: Sequence[Sequence[int]]) -> Dict[str, Any]:
    ancestors, descendants = transitive_closure(predecessors)
    counts = [0] * len(INTERVAL_BINS)
    open_volume_sum = 0
    max_open_volume = 0
    for future, ancestor_bits in enumerate(ancestors):
        remaining = ancestor_bits
        while remaining:
            bit = remaining & -remaining
            past = bit.bit_length() - 1
            remaining -= bit
            open_volume = (descendants[past] & ancestors[future]).bit_count()
            open_volume_sum += open_volume
            max_open_volume = max(max_open_volume, open_volume)
            for index, (_, low, high) in enumerate(INTERVAL_BINS):
                if low <= open_volume <= high:
                    counts[index] += 1
                    break
    comparable_pairs = sum(counts)
    if comparable_pairs == 0:
        raise ValueError("interval spectrum requires comparable pairs")
    probabilities = [count / comparable_pairs for count in counts]
    entropy = -sum(value * math.log(value, 2) for value in probabilities if value > 0.0)
    return {
        "counts": counts,
        "probabilities": probabilities,
        "comparable_pairs": comparable_pairs,
        "mean_open_volume": open_volume_sum / comparable_pairs,
        "max_open_volume": max_open_volume,
        "tail_mass_ge_8": sum(probabilities[4:]),
        "spectrum_entropy": entropy,
    }


def jensen_shannon(left: Sequence[float], right: Sequence[float]) -> float:
    midpoint = [(a + b) / 2.0 for a, b in zip(left, right)]

    def divergence(values: Sequence[float]) -> float:
        return sum(
            value * math.log(value / center, 2)
            for value, center in zip(values, midpoint)
            if value > 0.0 and center > 0.0
        )

    return 0.5 * divergence(left) + 0.5 * divergence(right)


def mean_spectrum(spectra: Sequence[Sequence[float]], skip: int | None = None) -> List[float]:
    count = len(spectra) - int(skip is not None)
    if count <= 0:
        raise ValueError("mean spectrum requires at least one row")
    return [
        sum(row[index] for row_index, row in enumerate(spectra) if row_index != skip) / count
        for index in range(len(INTERVAL_BINS))
    ]


def rewire_layer_indegree(dag: RunDAG, seed: int) -> Tuple[Tuple[Tuple[int, ...], ...], Dict[str, Any]]:
    rng = random.Random(seed)
    nodes_by_depth: Dict[int, List[int]] = defaultdict(list)
    predecessors: List[Tuple[int, ...]] = []
    for child, (depth, indegree) in enumerate(zip(dag.depths, dag.indegrees)):
        if depth == 0:
            if indegree != 0:
                raise ValueError("depth-zero event has parents")
            parents: List[int] = []
        else:
            required_pool = nodes_by_depth[depth - 1]
            lower_pool = [
                node
                for candidate_depth, nodes in nodes_by_depth.items()
                if candidate_depth < depth
                for node in nodes
            ]
            if not required_pool or len(lower_pool) < indegree:
                raise ValueError("null cannot preserve depth and indegree")
            required = rng.choice(required_pool)
            remainder = [node for node in lower_pool if node != required]
            parents = [required] + rng.sample(remainder, indegree - 1)
        predecessors.append(tuple(sorted(parents)))
        nodes_by_depth[depth].append(child)
    recomputed = recompute_depths(predecessors)
    depth_pass = tuple(recomputed) == dag.depths
    indegree_pass = tuple(len(row) for row in predecessors) == dag.indegrees
    order_pass = all(parent < child for child, parents in enumerate(predecessors) for parent in parents)
    layer_pass = Counter(recomputed) == Counter(dag.depths)
    return tuple(predecessors), {
        "depth_sequence_pass": int(depth_pass),
        "indegree_sequence_pass": int(indegree_pass),
        "scheduler_order_pass": int(order_pass),
        "layer_profile_pass": int(layer_pass),
        "null_integrity_pass": int(depth_pass and indegree_pass and order_pass and layer_pass),
    }


def random_topological_order(predecessors: Sequence[Sequence[int]], seed: int) -> List[int]:
    rng = random.Random(seed)
    successors: List[List[int]] = [[] for _ in predecessors]
    remaining = [len(parents) for parents in predecessors]
    for child, parents in enumerate(predecessors):
        for parent in parents:
            successors[parent].append(child)
    ready = [node for node, count in enumerate(remaining) if count == 0]
    order: List[int] = []
    while ready:
        index = rng.randrange(len(ready))
        node = ready.pop(index)
        order.append(node)
        for child in successors[node]:
            remaining[child] -= 1
            if remaining[child] == 0:
                ready.append(child)
    if len(order) != len(predecessors):
        raise ValueError("DAG has a cycle")
    return order


def remap_predecessors(predecessors: Sequence[Sequence[int]], order: Sequence[int]) -> Tuple[Tuple[int, ...], ...]:
    mapping = {old: new for new, old in enumerate(order)}
    remapped: List[Tuple[int, ...] | None] = [None] * len(order)
    for old_child in order:
        new_child = mapping[old_child]
        remapped[new_child] = tuple(sorted(mapping[parent] for parent in predecessors[old_child]))
    return tuple(row if row is not None else () for row in remapped)


def analyze_run(
    dag: RunDAG,
    include_isomorphism: bool,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    observed = interval_spectrum(dag.predecessors)
    null_products: List[Dict[str, Any]] = []
    null_integrity_rows: List[Dict[str, Any]] = []
    for replicate in range(NULL_REPLICATES):
        seed = stable_seed("v16i", dag.stage, *dag.key, NULL_FAMILY, replicate)
        rewired, integrity = rewire_layer_indegree(dag, seed)
        product = interval_spectrum(rewired)
        null_products.append(product)
        null_integrity_rows.append({
            **dag.prefix,
            "null_family": NULL_FAMILY,
            "null_replicate": replicate,
            "null_seed": seed,
            **integrity,
        })
    null_spectra = [row["probabilities"] for row in null_products]
    null_center = mean_spectrum(null_spectra)
    observed_js = jensen_shannon(observed["probabilities"], null_center)
    null_self_js = [
        jensen_shannon(row, mean_spectrum(null_spectra, skip=index))
        for index, row in enumerate(null_spectra)
    ]
    null_median_js = median(null_self_js)
    effect_ratio = observed_js / max(null_median_js, EPSILON)
    empirical_p = (1 + sum(value >= observed_js for value in null_self_js)) / (NULL_REPLICATES + 1)
    summary = {
        **dag.prefix,
        "n_events": len(dag.predecessors),
        "direct_edges": sum(dag.indegrees),
        "causal_depth": max(dag.depths) + 1,
        "comparable_pairs": observed["comparable_pairs"],
        "observed_js_to_null_center": observed_js,
        "null_median_leave_one_out_js": null_median_js,
        "js_effect_ratio": effect_ratio,
        "empirical_p_upper": empirical_p,
        "effect_positive": int(effect_ratio > 1.0),
        "p_le_010": int(empirical_p <= MAX_EMPIRICAL_P),
        "observed_mean_open_volume": observed["mean_open_volume"],
        "null_mean_open_volume": mean(row["mean_open_volume"] for row in null_products),
        "observed_tail_mass_ge_8": observed["tail_mass_ge_8"],
        "null_mean_tail_mass_ge_8": mean(row["tail_mass_ge_8"] for row in null_products),
        "tail_mass_ge_8_delta": observed["tail_mass_ge_8"] - mean(row["tail_mass_ge_8"] for row in null_products),
        "observed_spectrum_entropy": observed["spectrum_entropy"],
        "null_mean_spectrum_entropy": mean(row["spectrum_entropy"] for row in null_products),
        "max_open_interval_volume": observed["max_open_volume"],
    }
    spectrum_rows = [
        {
            **dag.prefix,
            "bin_label": label,
            "open_volume_low": low,
            "open_volume_high": "" if high >= 10**18 else high,
            "observed_count": observed["counts"][index],
            "observed_probability": observed["probabilities"][index],
            "null_mean_probability": null_center[index],
            "observed_minus_null_probability": observed["probabilities"][index] - null_center[index],
        }
        for index, (label, low, high) in enumerate(INTERVAL_BINS)
    ]
    null_rows = [
        {
            **dag.prefix,
            "null_family": NULL_FAMILY,
            "null_replicate": replicate,
            "null_seed": null_integrity_rows[replicate]["null_seed"],
            "comparable_pairs": product["comparable_pairs"],
            "leave_one_out_js": null_self_js[replicate],
            "mean_open_volume": product["mean_open_volume"],
            "tail_mass_ge_8": product["tail_mass_ge_8"],
            "spectrum_entropy": product["spectrum_entropy"],
            **{
                f"prob_{label}": product["probabilities"][index]
                for index, (label, _, _) in enumerate(INTERVAL_BINS)
            },
        }
        for replicate, product in enumerate(null_products)
    ]
    isomorphism_rows: List[Dict[str, Any]] = []
    if include_isomorphism:
        for replay in range(ISOMORPHISM_REPLAYS):
            seed = stable_seed("v16i", "isomorphism", *dag.key, replay)
            order = random_topological_order(dag.predecessors, seed)
            remapped = remap_predecessors(dag.predecessors, order)
            transported = interval_spectrum(remapped)
            isomorphism_rows.append({
                **dag.prefix,
                "replay": replay,
                "replay_seed": seed,
                "changed_position_fraction": sum(index != node for index, node in enumerate(order)) / len(order),
                "comparable_pairs_equal": int(transported["comparable_pairs"] == observed["comparable_pairs"]),
                "interval_counts_equal": int(transported["counts"] == observed["counts"]),
                "max_probability_error": max(abs(a - b) for a, b in zip(transported["probabilities"], observed["probabilities"])),
                "isomorphism_pass": int(transported["counts"] == observed["counts"]),
            })
    return summary, spectrum_rows, null_rows, null_integrity_rows, isomorphism_rows


def analyze_stage(stage: str, include_isomorphism: bool) -> Tuple[List[Dict[str, Any]], ...]:
    summaries: List[Dict[str, Any]] = []
    spectra: List[Dict[str, Any]] = []
    nulls: List[Dict[str, Any]] = []
    null_audits: List[Dict[str, Any]] = []
    isomorphisms: List[Dict[str, Any]] = []
    dags = load_stage(stage)
    for index, dag in enumerate(dags, start=1):
        summary, spectrum_rows, null_rows, audit_rows, iso_rows = analyze_run(dag, include_isomorphism)
        summaries.append(summary)
        spectra.extend(spectrum_rows)
        nulls.extend(null_rows)
        null_audits.extend(audit_rows)
        isomorphisms.extend(iso_rows)
        print(f"[v16i] stage={stage} runs={index}/{len(dags)} arm={dag.arm} ratio={float(summary['js_effect_ratio']):.6f}")
    return summaries, spectra, nulls, null_audits, isomorphisms


def aggregate_rows(rows: Sequence[Mapping[str, Any]], field: str, min_ratio: float, min_positive: float) -> List[Dict[str, Any]]:
    output: List[Dict[str, Any]] = []
    for value in sorted({str(row[field]) for row in rows}):
        subset = [row for row in rows if str(row[field]) == value]
        ratio_value = median(float(row["js_effect_ratio"]) for row in subset)
        positive_fraction = mean(float(row["effect_positive"]) for row in subset)
        significant_fraction = mean(float(row["p_le_010"]) for row in subset)
        output.append({
            "group_field": field,
            "group_value": value,
            "n_runs": len(subset),
            "median_js_effect_ratio": ratio_value,
            "positive_fraction": positive_fraction,
            "p_le_010_fraction": significant_fraction,
            "min_median_effect_ratio": min_ratio,
            "min_positive_fraction": min_positive,
            "group_pass": int(ratio_value >= min_ratio and positive_fraction >= min_positive),
        })
    return output


def local_gate_row(rows: Sequence[Mapping[str, Any]], stage: str) -> Dict[str, Any]:
    subset = [row for row in rows if row["arm"] == PRIMARY_ARM]
    ratio_value = median(float(row["js_effect_ratio"]) for row in subset)
    positive_fraction = mean(float(row["effect_positive"]) for row in subset)
    significant_fraction = mean(float(row["p_le_010"]) for row in subset)
    passed = (
        len(subset) == 6
        and ratio_value >= MIN_LOCAL_MEDIAN_EFFECT_RATIO
        and positive_fraction >= MIN_LOCAL_POSITIVE_FRACTION
        and significant_fraction >= MIN_LOCAL_P_LE_010_FRACTION
    )
    return {
        "stage": stage,
        "target_nodes": int(subset[0]["target_nodes"]),
        "primary_arm": PRIMARY_ARM,
        "n_runs": len(subset),
        "median_js_effect_ratio": ratio_value,
        "positive_fraction": positive_fraction,
        "p_le_010_fraction": significant_fraction,
        "min_median_effect_ratio": MIN_LOCAL_MEDIAN_EFFECT_RATIO,
        "min_positive_fraction": MIN_LOCAL_POSITIVE_FRACTION,
        "min_p_le_010_fraction": MIN_LOCAL_P_LE_010_FRACTION,
        "local_gate_pass": int(passed),
    }


def source_chain_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for stage in (*CALIBRATION_STAGES, HOLDOUT_STAGE):
        config = STAGE_FILES[stage]
        for role in ("events", "edges", "runs", "gates"):
            path = DOC / config[role]
            rows.append({
                "stage": stage,
                "role": role,
                "artifact": path.name,
                "sha256": file_sha256(path),
                "source_status": source_status(stage),
                "expected_status": config["expected"],
                "source_pass": int(source_status(stage) == config["expected"]),
            })
    for artifact in ("v16h_direct_rate_audit.csv", "v16h_execution_audit.csv", "v16h_pre_registration.csv"):
        path = DOC / artifact
        rows.append({
            "stage": HOLDOUT_STAGE,
            "role": "audit",
            "artifact": artifact,
            "sha256": file_sha256(path),
            "source_status": "present",
            "expected_status": "present",
            "source_pass": 1,
        })
    return rows


def prepare() -> None:
    all_summaries: List[Dict[str, Any]] = []
    all_spectra: List[Dict[str, Any]] = []
    all_nulls: List[Dict[str, Any]] = []
    all_null_audits: List[Dict[str, Any]] = []
    local_rows: List[Dict[str, Any]] = []
    for stage in CALIBRATION_STAGES:
        summaries, spectra, nulls, audits, _ = analyze_stage(stage, include_isomorphism=False)
        all_summaries.extend(summaries)
        all_spectra.extend(spectra)
        all_nulls.extend(nulls)
        all_null_audits.extend(audits)
        local_rows.append(local_gate_row(summaries, stage))
    v16c_row = next(row for row in local_rows if row["stage"] == "v16c")
    v16d_row = next(row for row in local_rows if row["stage"] == "v16d")
    target_ratio = float(v16d_row["median_js_effect_ratio"]) / float(v16c_row["median_js_effect_ratio"])
    design_pass = (
        all(int(row["local_gate_pass"]) for row in local_rows)
        and TARGET_TRANSFER_RANGE[0] <= target_ratio <= TARGET_TRANSFER_RANGE[1]
        and all(int(row["null_integrity_pass"]) for row in all_null_audits)
    )
    selection = [{
        "candidate": "causal_interval_abundance_full_spectrum_js",
        "primary_metric": "observed_js_to_null_center_over_median_null_leave_one_out_js",
        "null_family": NULL_FAMILY,
        "v16c_local_median_effect_ratio": v16c_row["median_js_effect_ratio"],
        "v16d_local_median_effect_ratio": v16d_row["median_js_effect_ratio"],
        "v16d_over_v16c_effect_ratio": target_ratio,
        "v16c_positive_fraction": v16c_row["positive_fraction"],
        "v16d_positive_fraction": v16d_row["positive_fraction"],
        "v16c_p_le_010_fraction": v16c_row["p_le_010_fraction"],
        "v16d_p_le_010_fraction": v16d_row["p_le_010_fraction"],
        "target_ratio_low": TARGET_TRANSFER_RANGE[0],
        "target_ratio_high": TARGET_TRANSFER_RANGE[1],
        "design_pass": int(design_pass),
        "selected_for_v16h_holdout": int(design_pass),
    }]
    baseline = [{
        "source_stage": "v16d",
        "source_target_nodes": v16d_row["target_nodes"],
        "source_primary_arm": PRIMARY_ARM,
        "source_n_runs": v16d_row["n_runs"],
        "source_median_js_effect_ratio": v16d_row["median_js_effect_ratio"],
        "source_positive_fraction": v16d_row["positive_fraction"],
        "source_p_le_010_fraction": v16d_row["p_le_010_fraction"],
        "holdout_ratio_low": TARGET_TRANSFER_RANGE[0],
        "holdout_ratio_high": TARGET_TRANSFER_RANGE[1],
    }]
    write_csv(CALIBRATION_RUNS, all_summaries)
    write_csv(CALIBRATION_SPECTRA, all_spectra)
    write_csv(CALIBRATION_NULLS, all_nulls)
    write_csv(CALIBRATION_NULL_AUDIT, all_null_audits)
    write_csv(DESIGN_SELECTION, selection)
    write_csv(FROZEN_BASELINE, baseline)
    sources = source_chain_rows()
    write_csv(SOURCE_CHAIN, sources)
    if not design_pass:
        raise RuntimeError("v16i design calibration did not support freezing the candidate")
    holdout_dags = load_stage(HOLDOUT_STAGE)
    script_hash = file_sha256(Path(__file__))
    source_hash = file_sha256(SOURCE_CHAIN)
    baseline_hash = file_sha256(FROZEN_BASELINE)
    selection_hash = file_sha256(DESIGN_SELECTION)
    prereg = [{
        "purpose_ref": PURPOSE_REF,
        "spec_digest": spec_digest(),
        "holdout_script_sha256": script_hash,
        "source_chain_sha256": source_hash,
        "design_selection_sha256": selection_hash,
        "frozen_baseline_sha256": baseline_hash,
        "holdout_stage": HOLDOUT_STAGE,
        "target_nodes": dag.target_nodes,
        "growth_seed": dag.growth_seed,
        "run_offset": dag.run_offset,
        "arm": dag.arm,
        "run_seed": dag.run_seed,
        "n_events": len(dag.predecessors),
        "interval_bins": ";".join(label for label, _, _ in INTERVAL_BINS),
        "null_family": NULL_FAMILY,
        "null_replicates": NULL_REPLICATES,
        "isomorphism_replays": ISOMORPHISM_REPLAYS,
        "min_local_median_effect_ratio": MIN_LOCAL_MEDIAN_EFFECT_RATIO,
        "min_local_positive_fraction": MIN_LOCAL_POSITIVE_FRACTION,
        "max_empirical_p": MAX_EMPIRICAL_P,
        "min_local_p_le_010_fraction": MIN_LOCAL_P_LE_010_FRACTION,
        "target_ratio_low": TARGET_TRANSFER_RANGE[0],
        "target_ratio_high": TARGET_TRANSFER_RANGE[1],
        "prepared_before_holdout_interval_analysis": 1,
    } for dag in holdout_dags]
    write_csv(PRE_REGISTRATION, prereg)
    print(f"[v16i] prepared runs={len(prereg)} digest={spec_digest()} target_ratio={target_ratio:.6f}")


def load_and_verify_preregistration() -> List[RunDAG]:
    prereg = read_csv(PRE_REGISTRATION)
    if len(prereg) != 12:
        raise ValueError("v16i preregistration must contain 12 assignments")
    if {row["spec_digest"] for row in prereg} != {spec_digest()}:
        raise ValueError("v16i spec digest mismatch")
    if {row["holdout_script_sha256"] for row in prereg} != {file_sha256(Path(__file__))}:
        raise ValueError("v16i script changed after preregistration")
    if {row["source_chain_sha256"] for row in prereg} != {file_sha256(SOURCE_CHAIN)}:
        raise ValueError("v16i source chain changed after preregistration")
    if {row["design_selection_sha256"] for row in prereg} != {file_sha256(DESIGN_SELECTION)}:
        raise ValueError("v16i design selection changed after preregistration")
    if {row["frozen_baseline_sha256"] for row in prereg} != {file_sha256(FROZEN_BASELINE)}:
        raise ValueError("v16i frozen baseline changed after preregistration")
    sources = source_chain_rows()
    observed = {(row["stage"], row["role"], row["artifact"]): row["sha256"] for row in read_csv(SOURCE_CHAIN)}
    current = {(row["stage"], row["role"], row["artifact"]): row["sha256"] for row in sources}
    if observed != current or not all(int(row["source_pass"]) for row in sources):
        raise ValueError("v16i source artifacts changed")
    direct = read_csv(DOC / "v16h_direct_rate_audit.csv")
    if len(direct) != 12 or not all(int(row["direct_log_parity_pass"]) for row in direct):
        raise ValueError("v16h direct-rate source audit failed")
    dags = load_stage(HOLDOUT_STAGE)
    expected_keys = {(int(row["growth_seed"]), int(row["run_offset"]), row["arm"], int(row["run_seed"])) for row in prereg}
    if {dag.key for dag in dags} != expected_keys:
        raise ValueError("v16i holdout assignments changed")
    return dags


def target_transfer_row(local_row: Mapping[str, Any]) -> Dict[str, Any]:
    baseline = read_csv(FROZEN_BASELINE)
    if len(baseline) != 1:
        raise ValueError("v16i frozen baseline must contain one row")
    source = float(baseline[0]["source_median_js_effect_ratio"])
    holdout = float(local_row["median_js_effect_ratio"])
    value = holdout / source
    return {
        "source_stage": "v16d",
        "holdout_stage": HOLDOUT_STAGE,
        "source_target_nodes": baseline[0]["source_target_nodes"],
        "holdout_target_nodes": local_row["target_nodes"],
        "source_median_js_effect_ratio": source,
        "holdout_median_js_effect_ratio": holdout,
        "holdout_over_source_ratio": value,
        "ratio_low": TARGET_TRANSFER_RANGE[0],
        "ratio_high": TARGET_TRANSFER_RANGE[1],
        "target_transfer_pass": int(TARGET_TRANSFER_RANGE[0] <= value <= TARGET_TRANSFER_RANGE[1]),
    }


def gate_evaluation(
    summaries: Sequence[Mapping[str, Any]],
    null_audits: Sequence[Mapping[str, Any]],
    isomorphisms: Sequence[Mapping[str, Any]],
    local_row: Mapping[str, Any],
    target_row: Mapping[str, Any],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], str]:
    source_pass = source_status(HOLDOUT_STAGE) == STAGE_FILES[HOLDOUT_STAGE]["expected"]
    run_pass = len(summaries) == 12 and all(int(row["n_events"]) == 3072 for row in summaries)
    null_pass = len(null_audits) == 12 * NULL_REPLICATES and all(int(row["null_integrity_pass"]) for row in null_audits)
    iso_pass = len(isomorphisms) == 12 * ISOMORPHISM_REPLAYS and all(int(row["isomorphism_pass"]) for row in isomorphisms)
    local_pass = int(local_row["local_gate_pass"]) == 1
    target_pass = int(target_row["target_transfer_pass"]) == 1
    growth_pass = len(growth_rows) == 2 and all(int(row["group_pass"]) for row in growth_rows)
    scheduler_pass = len(scheduler_rows) == 2 and all(int(row["group_pass"]) for row in scheduler_rows)
    instrumentation = all((source_pass, run_pass, null_pass, iso_pass))
    evidence = all((local_pass, target_pass, growth_pass, scheduler_pass))
    if not instrumentation:
        overall = "v16i_instrumentation_failed"
    elif evidence:
        overall = "causal_interval_abundance_supported_beyond_layer_indegree_null"
    else:
        overall = "causal_interval_abundance_not_supported_under_frozen_null"
    gates = [
        {"gate": "v16h_source_contract", "status": "pass" if source_pass else "fail", "observed": int(source_pass), "required": 1, "decision": "continue" if source_pass else "stop"},
        {"gate": "holdout_run_integrity", "status": "pass" if run_pass else "fail", "observed": f"runs={len(summaries)};events={sum(int(row['n_events']) for row in summaries)}", "required": "runs=12;events=36864", "decision": "continue" if run_pass else "repair_input"},
        {"gate": "layer_indegree_null_integrity", "status": "pass" if null_pass else "fail", "observed": f"passes={sum(int(row['null_integrity_pass']) for row in null_audits)}/{len(null_audits)}", "required": f"{12 * NULL_REPLICATES}/{12 * NULL_REPLICATES}", "decision": "continue" if null_pass else "repair_null"},
        {"gate": "event_poset_isomorphism", "status": "pass" if iso_pass else "fail", "observed": f"passes={sum(int(row['isomorphism_pass']) for row in isomorphisms)}/{len(isomorphisms)}", "required": f"{12 * ISOMORPHISM_REPLAYS}/{12 * ISOMORPHISM_REPLAYS}", "decision": "continue" if iso_pass else "repair_observable"},
        {"gate": "local_interval_abundance", "status": "pass" if local_pass else "fail", "observed": f"median_ratio={float(local_row['median_js_effect_ratio']):.6f};positive={float(local_row['positive_fraction']):.6f};p_le_010={float(local_row['p_le_010_fraction']):.6f}", "required": f"median>={MIN_LOCAL_MEDIAN_EFFECT_RATIO};positive>={MIN_LOCAL_POSITIVE_FRACTION};p_le_010>={MIN_LOCAL_P_LE_010_FRACTION}", "decision": "continue" if local_pass else "retire_interval_candidate"},
        {"gate": "v16d_to_v16h_target_transfer", "status": "pass" if target_pass else "fail", "observed": float(target_row["holdout_over_source_ratio"]), "required": f"in [{TARGET_TRANSFER_RANGE[0]},{TARGET_TRANSFER_RANGE[1]}]", "decision": "continue" if target_pass else "target_sensitive"},
        {"gate": "growth_seed_transfer", "status": "pass" if growth_pass else "fail", "observed": f"passing_groups={sum(int(row['group_pass']) for row in growth_rows)}/{len(growth_rows)}", "required": "2/2", "decision": "continue" if growth_pass else "growth_sensitive"},
        {"gate": "scheduler_transfer", "status": "pass" if scheduler_pass else "fail", "observed": f"passing_groups={sum(int(row['group_pass']) for row in scheduler_rows)}/{len(scheduler_rows)}", "required": "2/2", "decision": "continue" if scheduler_pass else "scheduler_sensitive"},
        {"gate": "v16i_overall", "status": overall, "observed": f"instrumentation={int(instrumentation)};evidence={int(evidence)}", "required": "instrumentation=1;evidence=1", "decision": overall},
    ]
    return gates, overall


def claim_rows(overall: str) -> List[Dict[str, Any]]:
    supported = overall == "causal_interval_abundance_supported_beyond_layer_indegree_null"
    return [
        {"claim_id": "C1", "claim": "The causal-interval abundance spectrum is an exact isomorphism-invariant function of each witnessed event DAG.", "status": "supported", "evidence": "v16i_event_poset_isomorphism_audit.csv;v16i_interval_spectrum.csv", "scope_limit": "finite event DAGs under the declared read/write support schema"},
        {"claim_id": "C2", "claim": "The v16h interval spectrum differs repeatably from a null preserving scheduler order, causal-depth layers, and per-event indegree.", "status": "supported" if supported else "unsupported", "evidence": "v16i_interval_run_summary.csv;v16i_local_interval_gate.csv", "scope_limit": "one structural null family; no outdegree or resource-age preservation"},
        {"claim_id": "C3", "claim": "The interval-abundance contrast transfers across the tested target, growth-seed, and scheduler groups.", "status": "supported" if supported else "unsupported", "evidence": "v16i_target_transfer.csv;v16i_growth_transfer.csv;v16i_scheduler_transfer.csv", "scope_limit": "targets 1024/1536 and the declared finite histories"},
        {"claim_id": "C4", "claim": "The interval spectrum establishes a dimension, manifold, Lorentz symmetry, or spacetime geometry.", "status": "unsupported", "evidence": "none", "scope_limit": "interval abundance is a topology diagnostic, not a validated physical geometry"},
        {"claim_id": "C5", "claim": "The structural null excludes every scheduler, degree-sequence, or rule artifact.", "status": "unsupported", "evidence": "v16i_null_integrity_audit.csv", "scope_limit": "outdegree sequence, parent age, resource type, and event family are not jointly preserved"},
    ]


def fmt(value: Any, digits: int = 6) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    return str(value) if not math.isfinite(number) else f"{number:.{digits}f}"


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row.get(field, "")) for field in fields) + " |")
    return lines


def build_report(
    summaries: Sequence[Mapping[str, Any]],
    local_row: Mapping[str, Any],
    target_row: Mapping[str, Any],
    growth_rows: Sequence[Mapping[str, Any]],
    scheduler_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    overall: str,
) -> str:
    lines = [
        "# v16i causal-interval abundance gate",
        "",
        f"Status: `{overall}`.",
        "",
        "## Question and evidential role",
        "",
        "v16i asks whether intrinsic event-DAG interval topology contains a repeatable signal beyond event count, scheduler order, the full causal-depth layer profile, and every event's indegree. It is an analysis holdout on existing v16h histories. No new dynamics were generated.",
        "",
        f"The full-spectrum Jensen-Shannon effect ratio was selected on v16c/v16d only and frozen before any v16h interval value was computed. Specification digest: `{spec_digest()}`.",
        "",
        "## Observable and structural null",
        "",
        "For every comparable event pair `(past, future)`, the open interval is the set of events causally after `past` and causally before `future`. Exact open-interval cardinalities are accumulated into the frozen dyadic bins `0, 1, 2-3, ..., 128+`.",
        "",
        "The null rewires direct parents while preserving event count, original scheduler order, each event's indegree, each event's causal depth, and the complete depth-layer profile. It does not preserve outdegree, parent-age distribution, event family, or read/write resource type. A positive result is therefore narrower than a mechanism claim.",
        "",
        "## Holdout run results",
        "",
    ]
    lines.extend(table(summaries, ("growth_seed", "run_offset", "arm", "comparable_pairs", "observed_js_to_null_center", "null_median_leave_one_out_js", "js_effect_ratio", "empirical_p_upper", "tail_mass_ge_8_delta")))
    lines.extend(["", "## Primary and transfer gates", ""])
    lines.extend(table([local_row], ("n_runs", "median_js_effect_ratio", "positive_fraction", "p_le_010_fraction", "local_gate_pass")))
    lines.append("")
    lines.extend(table([target_row], ("source_median_js_effect_ratio", "holdout_median_js_effect_ratio", "holdout_over_source_ratio", "target_transfer_pass")))
    lines.append("")
    lines.extend(table(growth_rows, ("group_field", "group_value", "n_runs", "median_js_effect_ratio", "positive_fraction", "group_pass")))
    lines.append("")
    lines.extend(table(scheduler_rows, ("group_field", "group_value", "n_runs", "median_js_effect_ratio", "positive_fraction", "group_pass")))
    lines.extend(["", "## Gate evaluation", ""])
    lines.extend(table(gates, ("gate", "status", "observed", "required", "decision")))
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "A pass supports a repeatable finite-poset interval-abundance structure not reduced to the frozen layer+indegree null. It does not establish a causal-set dimension, manifoldlikeness, Lorentz invariance, physical time, continuum behavior, particles, entanglement, or a spacetime geometry.",
        "",
        "Before any stronger interpretation, the smallest next mechanism gate is a stricter null that also preserves direct in/out-degree and parent-age structure. Failure there would identify the present signal as a degree/age wiring artifact.",
        "",
    ])
    return "\n".join(lines)


def run() -> None:
    dags = load_and_verify_preregistration()
    summaries: List[Dict[str, Any]] = []
    spectra: List[Dict[str, Any]] = []
    nulls: List[Dict[str, Any]] = []
    null_audits: List[Dict[str, Any]] = []
    isomorphisms: List[Dict[str, Any]] = []
    for index, dag in enumerate(dags, start=1):
        summary, spectrum_rows, null_rows, audit_rows, iso_rows = analyze_run(dag, include_isomorphism=True)
        summaries.append(summary)
        spectra.extend(spectrum_rows)
        nulls.extend(null_rows)
        null_audits.extend(audit_rows)
        isomorphisms.extend(iso_rows)
        print(f"[v16i] holdout={index}/{len(dags)} arm={dag.arm} ratio={float(summary['js_effect_ratio']):.6f}")
    local_row = local_gate_row(summaries, HOLDOUT_STAGE)
    target_row = target_transfer_row(local_row)
    growth_rows = aggregate_rows(summaries, "growth_seed", GROUP_MIN_MEDIAN_EFFECT_RATIO, GROUP_MIN_POSITIVE_FRACTION)
    scheduler_rows = aggregate_rows(summaries, "arm", GROUP_MIN_MEDIAN_EFFECT_RATIO, GROUP_MIN_POSITIVE_FRACTION)
    gates, overall = gate_evaluation(summaries, null_audits, isomorphisms, local_row, target_row, growth_rows, scheduler_rows)
    write_csv(DOC / "v16i_interval_run_summary.csv", summaries)
    write_csv(DOC / "v16i_interval_spectrum.csv", spectra)
    write_csv(DOC / "v16i_interval_null_distribution.csv", nulls)
    write_csv(DOC / "v16i_null_integrity_audit.csv", null_audits)
    write_csv(DOC / "v16i_event_poset_isomorphism_audit.csv", isomorphisms)
    write_csv(DOC / "v16i_local_interval_gate.csv", [local_row])
    write_csv(DOC / "v16i_target_transfer.csv", [target_row])
    write_csv(DOC / "v16i_growth_transfer.csv", growth_rows)
    write_csv(DOC / "v16i_scheduler_transfer.csv", scheduler_rows)
    write_csv(DOC / "v16i_gate_evaluation.csv", gates)
    write_csv(DOC / "v16i_claim_ledger.csv", claim_rows(overall))
    report = build_report(summaries, local_row, target_row, growth_rows, scheduler_rows, gates, overall)
    (DOC / "v16i_causal_interval_abundance_gate.md").write_text(report, encoding="utf-8")
    recommendation = "\n".join([
        "# Operativ anbefaling v0.16i",
        "",
        f"Status: `{overall}`.",
        "",
        "- Ved pass: behold causal interval abundance som en uavhengig poset-observabel, men ikke kall den dimensjon eller geometri.",
        "- Neste minste mekanismegate er en strengere null som ogsaa bevarer direkte in/out-degree og parent-age-struktur.",
        "- Ved fail: pensjoner denne intervallkandidaten under dagens event-DAG og velg en ny fysisk motivert observabel.",
        "- Ikke oppgrader til Lorentz-, spacetime-, continuum-, partikkel- eller entanglement-claim.",
        "",
    ])
    (DOC / "v0_16i_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    lay = "\n".join([
        "# Relasjonell universgraf for ikke-spesialister v0.16i",
        "",
        "v16i teller hvor mange andre hendelser som ligger kausalt mellom to avhengige hendelser. Fordelingen sammenlignes med kunstige DAG-er som har samme rekkefolge, dybdelag og antall direkte foreldre per hendelse.",
        "",
        f"Resultatstatus: `{overall}`.",
        "",
        "Selv et positivt resultat viser bare at event-DAG-en har repeterbar intervallstruktur utover akkurat denne kontrollen. Det viser ikke at modellen har funnet fysisk romtid.",
        "",
    ])
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16i.md").write_text(lay, encoding="utf-8")
    print(f"[v16i] overall={overall} runs={len(summaries)} nulls={len(nulls)}")


def verify_outputs() -> None:
    summaries = read_csv(DOC / "v16i_interval_run_summary.csv")
    spectra = read_csv(DOC / "v16i_interval_spectrum.csv")
    nulls = read_csv(DOC / "v16i_interval_null_distribution.csv")
    null_audits = read_csv(DOC / "v16i_null_integrity_audit.csv")
    isomorphisms = read_csv(DOC / "v16i_event_poset_isomorphism_audit.csv")
    gates = read_csv(DOC / "v16i_gate_evaluation.csv")
    if len(summaries) != 12 or len(spectra) != 12 * len(INTERVAL_BINS):
        raise ValueError("v16i summary/spectrum row count failed")
    if len(nulls) != 12 * NULL_REPLICATES or len(null_audits) != len(nulls):
        raise ValueError("v16i null row count failed")
    if len(isomorphisms) != 12 * ISOMORPHISM_REPLAYS:
        raise ValueError("v16i isomorphism row count failed")
    if not all(int(row["null_integrity_pass"]) for row in null_audits):
        raise ValueError("v16i null integrity failed")
    if not all(int(row["isomorphism_pass"]) for row in isomorphisms):
        raise ValueError("v16i isomorphism failed")
    overall = [row for row in gates if row["gate"] == "v16i_overall"]
    allowed = {
        "causal_interval_abundance_supported_beyond_layer_indegree_null",
        "causal_interval_abundance_not_supported_under_frozen_null",
        "v16i_instrumentation_failed",
    }
    if len(overall) != 1 or overall[0]["status"] not in allowed:
        raise ValueError("v16i overall status failed")
    for path in DOC.glob("v16i_*.csv"):
        for row in read_csv(path):
            if any(str(value).lower() in {"nan", "inf", "-inf"} for value in row.values()):
                raise ValueError(f"nonfinite literal in {path}")
    print(f"[v16i] output verification pass overall={overall[0]['status']}")


def self_test() -> None:
    chain = ((), (0,), (1,))
    product = interval_spectrum(chain)
    assert product["counts"][0] == 2 and product["counts"][1] == 1
    diamond = ((), (0,), (0,), (1, 2))
    product = interval_spectrum(diamond)
    assert product["counts"][0] == 4 and product["counts"][2] == 1
    assert abs(jensen_shannon(product["probabilities"], product["probabilities"])) <= EPSILON
    order = random_topological_order(diamond, 16)
    remapped = remap_predecessors(diamond, order)
    assert interval_spectrum(remapped)["counts"] == product["counts"]
    fake = RunDAG("test", 4, 1, 2, PRIMARY_ARM, 3, diamond, tuple(recompute_depths(diamond)), tuple(len(row) for row in diamond))
    rewired, audit = rewire_layer_indegree(fake, 17)
    assert audit["null_integrity_pass"] == 1
    assert tuple(recompute_depths(rewired)) == fake.depths
    assert spec_digest() == spec_digest()
    print("[v16i] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser(description="v16i causal-interval abundance gate")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if sum((args.prepare_only, args.self_test, args.verify_only)) > 1:
        parser.error("choose at most one mode")
    if args.prepare_only:
        prepare()
    elif args.self_test:
        self_test()
    elif args.verify_only:
        verify_outputs()
    else:
        run()


if __name__ == "__main__":
    main()
