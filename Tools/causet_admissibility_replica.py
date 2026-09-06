#!/usr/bin/env python3
"""Independent, set-based replication and adversarial checks for WP-G1.

The history path intentionally depends only on the frozen WP-F0 prose
specification and the already-materialized v16b/v16c/v16d CSV histories.  It
does not import the WP-F0 implementation.
"""
from __future__ import annotations

import argparse
import bisect
import csv
import glob
import hashlib
import json
import math
import random
import statistics
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "Documentation"
PROGRAM = DOC / "Program"

P_LEVELS = (1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125)
DECIMATION_DRAWS = 32
FINAL_DRAWS = 20
HISTORY_OUTPUT = PROGRAM / "WP-G1_replica_per_history.csv"
DRAW_OUTPUT = PROGRAM / "WP-G1_replica_decimation_draws.csv"
BLIND_HISTORY_OUTPUT = PROGRAM / "WP-G1_blind_replica_per_history.csv"
BLIND_DRAW_OUTPUT = PROGRAM / "WP-G1_blind_replica_decimation_draws.csv"
BLIND_MANIFEST = PROGRAM / "WP-G1_blind_manifest.json"
COMPARISON_OUTPUT = PROGRAM / "WP-G1_replica_comparison.csv"
CROSS_BUNDLE_OUTPUT = PROGRAM / "WP-G1_cross_edge_bundle.csv"
CONFLICT_CALIBRATION_OUTPUT = PROGRAM / "WP-G1_conflict_d2_calibration.csv"
CONFLICT_D2_OUTPUT = PROGRAM / "WP-G1_conflict_d2.csv"
FINE_INVENTORY_OUTPUT = PROGRAM / "WP-G1_fine_dag_inventory.csv"
THETA_SCALING_OUTPUT = PROGRAM / "WP-G1_theta_scaling.csv"
CHAIN_THEORY_OUTPUT = PROGRAM / "WP-G1_chain_bundle_theory.csv"
CHAIN_PROCEDURE_OUTPUT = PROGRAM / "WP-G1_chain_bundle_procedure.csv"
BOOTSTRAP_OUTPUT = PROGRAM / "WP-G1_bootstrap_unit_comparison.csv"

HISTORY_SOURCES = (
    (
        "v16b",
        DOC / "v16b_dependency_edges.csv",
        DOC / "v16b_run_summary.csv",
    ),
    (
        "v16c_fine",
        DOC / "v16c_fine_dependency_edges.csv",
        DOC / "v16c_run_summary.csv",
    ),
    (
        "v16d_fine",
        DOC / "v16d_fine_dependency_edges.csv",
        DOC / "v16d_run_summary.csv",
    ),
)

RUN_KEY = ("growth_seed", "run_offset", "arm", "run_seed")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    records = list(rows)
    if not records:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in records:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_key(row: Mapping[str, str]) -> tuple[str, ...]:
    return tuple(row[field] for field in RUN_KEY)


def stable_seed(parts: Iterable[Any]) -> int:
    payload = "|".join(str(part) for part in parts).encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


@dataclass(frozen=True)
class PosetAnalysis:
    n: int
    parents: tuple[frozenset[int], ...]
    ancestors: tuple[frozenset[int], ...]
    descendants: tuple[frozenset[int], ...]
    depths: tuple[int, ...]
    comparable_pairs: int
    link_count: int
    max_interval: int

    @property
    def raw_edge_count(self) -> int:
        return sum(len(row) for row in self.parents)

    @property
    def height(self) -> int:
        return max(self.depths, default=-1) + 1


def analyze_parents(parents_input: Sequence[Iterable[int]]) -> PosetAnalysis:
    """Compute closure observables using Python sets, not integer bitsets."""
    n = len(parents_input)
    parents = tuple(frozenset(int(parent) for parent in row) for row in parents_input)
    ancestors_mut: list[set[int]] = []
    depths: list[int] = []
    for child, direct_parents in enumerate(parents):
        if any(parent < 0 or parent >= child for parent in direct_parents):
            raise ValueError(f"history is not in topological event order at child {child}")
        closure: set[int] = set()
        depth = 0
        for parent in direct_parents:
            closure.add(parent)
            closure.update(ancestors_mut[parent])
            depth = max(depth, depths[parent] + 1)
        ancestors_mut.append(closure)
        depths.append(depth)

    descendants_mut = [set() for _ in range(n)]
    for child, closure in enumerate(ancestors_mut):
        for ancestor in closure:
            descendants_mut[ancestor].add(child)

    # Every cover relation of a DAG's reachability order is present among its
    # original edges.  An edge p->v is redundant exactly when another direct
    # predecessor q of v is reachable from p.
    link_count = 0
    for direct_parents in parents:
        for parent in direct_parents:
            if not any(
                other != parent and parent in ancestors_mut[other]
                for other in direct_parents
            ):
                link_count += 1

    max_interval = 1 if n else 0
    for future, past_set in enumerate(ancestors_mut):
        del future  # event order is encoded in past_set
        for past in past_set:
            inclusive_size = len(descendants_mut[past].intersection(past_set)) + 2
            max_interval = max(max_interval, inclusive_size)

    ancestors = tuple(frozenset(row) for row in ancestors_mut)
    descendants = tuple(frozenset(row) for row in descendants_mut)
    return PosetAnalysis(
        n=n,
        parents=parents,
        ancestors=ancestors,
        descendants=descendants,
        depths=tuple(depths),
        comparable_pairs=sum(len(row) for row in ancestors),
        link_count=link_count,
        max_interval=max_interval,
    )


def induced_observables(
    ancestors: Sequence[frozenset[int]], selected: frozenset[int]
) -> tuple[int, float]:
    """Height and comparability of the closure-induced selected subposet."""
    if not selected:
        return 0, 0.0
    selected_depth: dict[int, int] = {}
    comparable_pairs = 0
    for event in sorted(selected):
        selected_past = ancestors[event].intersection(selected)
        comparable_pairs += len(selected_past)
        selected_depth[event] = 1 + max(
            (selected_depth[past] for past in selected_past), default=0
        )
    n_selected = len(selected)
    denominator = n_selected * (n_selected - 1) // 2
    r_value = comparable_pairs / denominator if denominator else 0.0
    return max(selected_depth.values()), r_value


def linear_slope(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        return float("nan")
    x_bar = statistics.fmean(xs)
    y_bar = statistics.fmean(ys)
    denominator = sum((x - x_bar) ** 2 for x in xs)
    if denominator == 0.0:
        return float("nan")
    return sum((x - x_bar) * (y - y_bar) for x, y in zip(xs, ys)) / denominator


def fit_draw_slope(points: Sequence[tuple[float, int]]) -> float:
    eligible = [(p_keep, height) for p_keep, height in points if height >= 8]
    if len({p_keep for p_keep, _ in eligible}) < 2:
        return float("nan")
    return linear_slope(
        [math.log(p_keep) for p_keep, _ in eligible],
        [math.log(height) for _, height in eligible],
    )


def percentile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(value for value in values if math.isfinite(value))
    if not ordered:
        return float("nan")
    index = probability * (len(ordered) - 1)
    low = math.floor(index)
    high = math.ceil(index)
    if low == high:
        return ordered[low]
    weight = index - low
    return ordered[low] * (1.0 - weight) + ordered[high] * weight


def bootstrap_draw_slope(
    draws_by_p: Mapping[float, Sequence[int]], rng: random.Random, reps: int = 1000
) -> tuple[float, float, float]:
    points = [
        (p_keep, int(height))
        for p_keep, heights in draws_by_p.items()
        for height in heights
    ]
    estimate = fit_draw_slope(points)
    samples: list[float] = []
    for _ in range(reps):
        sample = [
            (p_keep, rng.choice(list(heights)))
            for p_keep, heights in draws_by_p.items()
            for _ in heights
        ]
        samples.append(fit_draw_slope(sample))
    return estimate, percentile(samples, 0.025), percentile(samples, 0.975)


def mm_r(dimension: float) -> float:
    return (
        math.gamma(dimension + 1)
        * math.gamma(dimension / 2)
        / (2.0 * math.gamma(1.5 * dimension))
    )


def mm_dimension(r_value: float) -> float:
    low, high = 1.0, 80.0
    if r_value >= mm_r(low):
        return low
    if r_value <= 0.0:
        return float("inf")
    while mm_r(high) > r_value and high < 640.0:
        high *= 2.0
    if mm_r(high) > r_value:
        return float("inf")
    for _ in range(200):
        middle = (low + high) / 2.0
        if mm_r(middle) > r_value:
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def decimation_rows(
    source: str,
    key: tuple[str, ...],
    analysis: PosetAnalysis,
) -> tuple[list[dict[str, Any]], float, int]:
    rows: list[dict[str, Any]] = []
    seed = stable_seed(("WP-G1-blind-decimation", source, *key))
    rng = random.Random(seed)
    all_events = frozenset(range(analysis.n))
    for p_keep in P_LEVELS:
        for draw in range(DECIMATION_DRAWS):
            selected = (
                all_events
                if p_keep == 1.0
                else frozenset(
                    event for event in range(analysis.n) if rng.random() < p_keep
                )
            )
            height, r_value = induced_observables(analysis.ancestors, selected)
            rows.append(
                {
                    "source": source,
                    **dict(zip(RUN_KEY, key)),
                    "decimation_seed": seed,
                    "p": p_keep,
                    "draw": draw,
                    "n_selected": len(selected),
                    "height": height,
                    "r": r_value,
                    "height_fit_eligible": int(height >= 8),
                }
            )

    mean_by_p: list[tuple[float, float]] = []
    for p_keep in P_LEVELS:
        heights = [float(row["height"]) for row in rows if row["p"] == p_keep]
        mean_height = statistics.fmean(heights)
        if mean_height >= 8.0:
            mean_by_p.append((p_keep, mean_height))
    slope = linear_slope(
        [math.log(p_keep) for p_keep, _ in mean_by_p],
        [math.log(height) for _, height in mean_by_p],
    )
    return rows, slope, len(mean_by_p)


def load_history(
    edge_rows: Sequence[Mapping[str, str]], n_events: int
) -> list[set[int]]:
    parents = [set() for _ in range(n_events)]
    for row in edge_rows:
        parent = int(row["parent_event_id"])
        child = int(row["child_event_id"])
        if not (0 <= parent < child < n_events):
            raise ValueError(f"invalid edge {parent}->{child} for N={n_events}")
        parents[child].add(parent)
    return parents


def analyze_histories() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    history_rows: list[dict[str, Any]] = []
    all_draw_rows: list[dict[str, Any]] = []
    for source, edge_path, summary_path in HISTORY_SOURCES:
        edges_by_run: dict[tuple[str, ...], list[dict[str, str]]] = {}
        for edge in read_csv(edge_path):
            edges_by_run.setdefault(run_key(edge), []).append(edge)
        summaries = read_csv(summary_path)
        for index, summary in enumerate(summaries, start=1):
            key = run_key(summary)
            n_events = int(summary["n_events"])
            analysis = analyze_parents(load_history(edges_by_run.get(key, []), n_events))
            possible_pairs = n_events * (n_events - 1) // 2
            r_value = analysis.comparable_pairs / possible_pairs if possible_pairs else 0.0
            r_floor = sum(analysis.depths) / possible_pairs if possible_pairs else 0.0
            floor_ratio = r_value / r_floor if r_floor else float("inf")
            height = analysis.height
            theta = (
                r_value * (n_events - 1) / (height - 1)
                if height > 1
                else float("inf")
            )
            draw_rows, slope, fit_levels = decimation_rows(source, key, analysis)
            all_draw_rows.extend(draw_rows)
            history_rows.append(
                {
                    "source": source,
                    **dict(zip(RUN_KEY, key)),
                    "n_events": n_events,
                    "raw_edges": analysis.raw_edge_count,
                    "raw_edges_per_event": analysis.raw_edge_count / n_events,
                    "comparable_pairs": analysis.comparable_pairs,
                    "r": r_value,
                    "r_floor": r_floor,
                    "r_over_r_floor": floor_ratio,
                    "height": height,
                    "link_count": analysis.link_count,
                    "links_per_event": analysis.link_count / n_events,
                    "max_interval": analysis.max_interval,
                    "max_interval_fraction": analysis.max_interval / n_events,
                    "theta": theta,
                    "decimation_slope": slope,
                    "decimation_fit_levels": fit_levels,
                    "decimation_draws_per_p": DECIMATION_DRAWS,
                }
            )
            print(
                f"[replica] {source} {index}/{len(summaries)} "
                f"arm={summary['arm']} N={n_events} r={r_value:.6f} "
                f"links/N={analysis.link_count / n_events:.6f}"
            )
        unused = set(edges_by_run).difference(run_key(row) for row in summaries)
        if unused:
            raise ValueError(f"{source}: edge runs absent from summary: {sorted(unused)}")
    if len(history_rows) != 36:
        raise ValueError(f"expected 36 histories, found {len(history_rows)}")
    return history_rows, all_draw_rows


def measure_decimation(
    analysis: PosetAnalysis,
    rng: random.Random,
    draws_per_p: int,
    p_one_draws: int,
) -> tuple[list[dict[str, Any]], float, float, float]:
    raw_rows: list[dict[str, Any]] = []
    by_p: dict[float, list[int]] = defaultdict(list)
    all_events = frozenset(range(analysis.n))
    for p_keep in P_LEVELS:
        count = p_one_draws if p_keep == 1.0 else draws_per_p
        for draw in range(count):
            selected = (
                all_events
                if p_keep == 1.0
                else frozenset(
                    event for event in range(analysis.n) if rng.random() < p_keep
                )
            )
            height, r_value = induced_observables(analysis.ancestors, selected)
            by_p[p_keep].append(height)
            raw_rows.append(
                {
                    "p": p_keep,
                    "draw": draw,
                    "kept": len(selected),
                    "L": height,
                    "r_p": r_value,
                }
            )
    slope, ci_low, ci_high = bootstrap_draw_slope(by_p, rng)
    return raw_rows, slope, ci_low, ci_high


def history_metric_row(
    label: str,
    source: str,
    growth_seed: str,
    run_offset: str,
    arm: str,
    analysis: PosetAnalysis,
    slope: float,
    ci_low: float,
    ci_high: float,
    seconds: float,
) -> dict[str, Any]:
    n_events = analysis.n
    pairs = n_events * (n_events - 1) // 2
    r_value = analysis.comparable_pairs / pairs if pairs else 0.0
    r_floor = sum(analysis.depths) / pairs if pairs else 0.0
    height = analysis.height
    theta = r_value * (n_events - 1) / (height - 1) if height > 1 else float("nan")
    row = {
        "label": label,
        "source": source,
        "growth_seed": growth_seed,
        "run_offset": run_offset,
        "arm": arm,
        "N": n_events,
        "raw_edges": analysis.raw_edge_count,
        "raw_edges_per_event": analysis.raw_edge_count / n_events if n_events else 0.0,
        "links": analysis.link_count,
        "links_per_event": analysis.link_count / n_events if n_events else 0.0,
        "comparable_pairs": analysis.comparable_pairs,
        "r": r_value,
        "r_floor": r_floor,
        "r_over_floor": r_value / r_floor if r_floor else float("nan"),
        "longest_chain_h": height,
        "theta": theta,
        "max_interval": analysis.max_interval,
        "max_interval_frac": analysis.max_interval / n_events if n_events else 0.0,
        "d_MM_corrected": mm_dimension(r_value),
        "decimation_s": slope,
        "s_ci_lo": ci_low,
        "s_ci_hi": ci_high,
        "s_ci_width": ci_high - ci_low,
        "g01_pass": int(bool(r_floor) and r_value / r_floor >= 2.0),
        "g02_pass": int(bool(n_events) and analysis.link_count / n_events >= 5.0),
        "g03_pass": int(bool(n_events) and analysis.max_interval / n_events >= 0.05),
        "g04_pass": int(theta >= 5.0),
        "seconds": round(seconds, 3),
    }
    row["gate0_pass"] = int(
        row["g01_pass"]
        and row["g02_pass"]
        and row["g03_pass"]
        and row["g04_pass"]
    )
    return row


def analyze_histories_final() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    history_rows: list[dict[str, Any]] = []
    draw_rows: list[dict[str, Any]] = []
    for source, edge_path, summary_path in HISTORY_SOURCES:
        edges_by_run: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
        for edge in read_csv(edge_path):
            edges_by_run[run_key(edge)].append(edge)
        summaries = read_csv(summary_path)
        for index, summary in enumerate(summaries, start=1):
            started = time.perf_counter()
            key = run_key(summary)
            analysis = analyze_parents(
                load_history(edges_by_run.get(key, []), int(summary["n_events"]))
            )
            rng = random.Random(stable_seed(("WP-G1-final-history", source, *key)))
            decimated, slope, ci_low, ci_high = measure_decimation(
                analysis, rng, FINAL_DRAWS, FINAL_DRAWS
            )
            prefix = {
                "label": "history",
                "source": edge_path.stem,
                "growth_seed": key[0],
                "run_offset": key[1],
                "arm": key[2],
                "N": analysis.n,
            }
            draw_rows.extend({**prefix, **row} for row in decimated)
            history_rows.append(
                history_metric_row(
                    "history",
                    edge_path.stem,
                    key[0],
                    key[1],
                    key[2],
                    analysis,
                    slope,
                    ci_low,
                    ci_high,
                    time.perf_counter() - started,
                )
            )
            print(
                f"[replica-final] {source} {index}/{len(summaries)} "
                f"arm={key[2]} s={slope:.6f}"
            )
    if len(history_rows) != 36:
        raise ValueError(f"expected 36 histories, found {len(history_rows)}")
    return history_rows, draw_rows


def write_comparison(replica_rows: Sequence[Mapping[str, Any]]) -> None:
    reference_rows = [
        row
        for row in read_csv(PROGRAM / "WP-F0_admissibility_per_history.csv")
        if row["label"] == "history"
    ]
    key_fields = ("growth_seed", "run_offset", "arm", "N")
    reference = {
        tuple(str(row[field]) for field in key_fields): row for row in reference_rows
    }
    metric_fields = (
        "raw_edges",
        "raw_edges_per_event",
        "links",
        "links_per_event",
        "comparable_pairs",
        "r",
        "r_floor",
        "r_over_floor",
        "longest_chain_h",
        "theta",
        "max_interval",
        "max_interval_frac",
        "decimation_s",
    )
    rows: list[dict[str, Any]] = []
    for replica in replica_rows:
        key = tuple(str(replica[field]) for field in key_fields)
        original = reference[key]
        for metric in metric_fields:
            left = float(replica[metric])
            right = float(original[metric])
            absolute = abs(left - right)
            relative = absolute / abs(right) if right else absolute
            rows.append(
                {
                    **{field: replica[field] for field in key_fields},
                    "metric": metric,
                    "replica": left,
                    "wp_f0": right,
                    "absolute_difference": absolute,
                    "relative_difference": relative,
                    "within_one_percent": int(relative <= 0.01),
                    "wp_f0_s_ci_contains_replica": (
                        int(float(original["s_ci_lo"]) <= left <= float(original["s_ci_hi"]))
                        if metric == "decimation_s"
                        else ""
                    ),
                }
            )
    write_csv(COMPARISON_OUTPUT, rows)


def cross_edge_bundle(
    n_events: int, chains: int, target_edges: int, rng: random.Random
) -> list[set[int]]:
    if n_events % chains:
        raise ValueError("cross-edge reference requires equal chain lengths")
    chain_length = n_events // chains
    parents = [set() for _ in range(n_events)]
    for event in range(chains, n_events):
        parents[event].add(event - chains)
    if target_edges < n_events - chains:
        raise ValueError("target has fewer edges than the base chain bundle")
    attempts = 0
    while sum(len(row) for row in parents) < target_edges:
        attempts += 1
        if attempts > 1_000_000:
            raise RuntimeError("could not place requested unique cross edges")
        source_layer = rng.randrange(chain_length - 1)
        target_layer = rng.randrange(source_layer + 1, chain_length)
        source_chain = rng.randrange(chains)
        target_chain = rng.randrange(chains - 1)
        if target_chain >= source_chain:
            target_chain += 1
        source = source_layer * chains + source_chain
        target = target_layer * chains + target_chain
        parents[target].add(source)
    return parents


def run_cross_bundle_attack() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for replicate in range(24):
        started = time.perf_counter()
        seed = stable_seed((2026090601, replicate))
        analysis = analyze_parents(
            cross_edge_bundle(2048, 32, 2328, random.Random(seed))
        )
        rng = random.Random(stable_seed((seed, "decimation")))
        _, slope, ci_low, ci_high = measure_decimation(
            analysis, rng, FINAL_DRAWS, 1
        )
        row = history_metric_row(
            "cross_edge_chain_bundle",
            "synthetic_preregistered",
            "-",
            str(replicate),
            "-",
            analysis,
            slope,
            ci_low,
            ci_high,
            time.perf_counter() - started,
        )
        rows.append(
            {
                "replicate": replicate,
                "seed": seed,
                "added_cross_edges": 312,
                **row,
            }
        )
        print(
            f"[premise 2.1] replicate={replicate + 1}/24 "
            f"r={row['r']:.6f} theta={row['theta']:.6f}"
        )
    write_csv(CROSS_BUNDLE_OUTPUT, rows)
    return rows


def conflict_dag_parents(
    accesses: Sequence[tuple[Iterable[int], Iterable[int]]]
) -> list[set[int]]:
    parents: list[set[int]] = []
    last_writer: dict[int, int] = {}
    readers_since_write: dict[int, set[int]] = defaultdict(set)
    for event, (reads_input, writes_input) in enumerate(accesses):
        reads = set(reads_input)
        writes = set(writes_input)
        predecessors: set[int] = set()
        for resource in reads:
            if resource in last_writer:
                predecessors.add(last_writer[resource])
        for resource in writes:
            if resource in last_writer:
                predecessors.add(last_writer[resource])
            predecessors.update(readers_since_write.get(resource, set()))
        parents.append(predecessors)
        for resource in reads.difference(writes):
            readers_since_write[resource].add(event)
        for resource in writes:
            last_writer[resource] = event
            readers_since_write[resource].clear()
    return parents


def d2_conflict_case(
    n_events: int, resource_pool: int, rng: random.Random
) -> tuple[list[tuple[float, float]], list[set[int]]]:
    points = sorted(
        ((rng.random(), rng.random()) for _ in range(n_events)),
        key=lambda point: point[0] + point[1],
    )
    accesses = []
    for _ in points:
        resource_count = rng.randint(1, 3)
        resources = tuple(rng.sample(range(resource_pool), resource_count))
        accesses.append((resources, resources))
    return points, conflict_dag_parents(accesses)


def d2_order_summary(points: Sequence[tuple[float, float]]) -> tuple[float, int]:
    ordered = sorted(points, key=lambda point: point[0])
    values = sorted(point[1] for point in ordered)
    ranks = {value: index + 1 for index, value in enumerate(values)}
    fenwick = [0] * (len(values) + 1)

    def query(index: int) -> int:
        total = 0
        while index:
            total += fenwick[index]
            index -= index & -index
        return total

    def add(index: int) -> None:
        while index < len(fenwick):
            fenwick[index] += 1
            index += index & -index

    comparable = 0
    lis_tails: list[float] = []
    for _, value in ordered:
        rank = ranks[value]
        comparable += query(rank - 1)
        add(rank)
        position = bisect.bisect_left(lis_tails, value)
        if position == len(lis_tails):
            lis_tails.append(value)
        else:
            lis_tails[position] = value
    n_events = len(points)
    pairs = n_events * (n_events - 1) // 2
    return comparable / pairs if pairs else 0.0, len(lis_tails)


def calibrate_conflict_resource_pool() -> tuple[int, list[dict[str, Any]]]:
    target = 1.13671875
    rows: list[dict[str, Any]] = []
    for resource_pool in range(512, 4097, 128):
        edge_rates = []
        for replicate in range(8):
            seed = stable_seed((2026090602, resource_pool, replicate))
            _, parents = d2_conflict_case(2048, resource_pool, random.Random(seed))
            edge_rates.append(sum(len(row) for row in parents) / 2048)
        median_rate = statistics.median(edge_rates)
        rows.append(
            {
                "resource_pool": resource_pool,
                "calibration_replicates": len(edge_rates),
                "median_raw_edges_per_event": median_rate,
                "min_raw_edges_per_event": min(edge_rates),
                "max_raw_edges_per_event": max(edge_rates),
                "target_raw_edges_per_event": target,
                "absolute_target_error": abs(median_rate - target),
            }
        )
    selected = min(rows, key=lambda row: (row["absolute_target_error"], row["resource_pool"]))
    for row in rows:
        row["selected"] = int(row is selected)
    write_csv(CONFLICT_CALIBRATION_OUTPUT, rows)
    return int(selected["resource_pool"]), rows


def run_conflict_d2_attack() -> list[dict[str, Any]]:
    resource_pool, _ = calibrate_conflict_resource_pool()
    rows: list[dict[str, Any]] = []
    for replicate in range(24):
        started = time.perf_counter()
        seed = stable_seed((2026090603, replicate))
        points, parents = d2_conflict_case(
            2048, resource_pool, random.Random(seed)
        )
        d2_r_value, d2_height = d2_order_summary(points)
        analysis = analyze_parents(parents)
        rng = random.Random(stable_seed((seed, "decimation")))
        _, slope, ci_low, ci_high = measure_decimation(
            analysis, rng, FINAL_DRAWS, 1
        )
        row = history_metric_row(
            "d2_through_conflict_dag",
            "synthetic_preregistered",
            "-",
            str(replicate),
            "-",
            analysis,
            slope,
            ci_low,
            ci_high,
            time.perf_counter() - started,
        )
        rows.append(
            {
                "replicate": replicate,
                "seed": seed,
                "resource_pool": resource_pool,
                "underlying_d2_r": d2_r_value,
                "underlying_d2_height": d2_height,
                "underlying_d2_theta": d2_r_value * 2047 / (d2_height - 1),
                **row,
            }
        )
        print(
            f"[premise 2.2] replicate={replicate + 1}/24 pool={resource_pool} "
            f"raw/N={row['raw_edges_per_event']:.6f} theta={row['theta']:.6f}"
        )
    write_csv(CONFLICT_D2_OUTPUT, rows)
    return rows


def fine_source_specs() -> list[tuple[str, Path, Path]]:
    paths = [DOC / "v16b_dependency_edges.csv"]
    paths.extend(Path(path) for path in sorted(glob.glob(str(DOC / "*fine_dependency_edges.csv"))))
    specs: list[tuple[str, Path, Path]] = []
    seen: set[Path] = set()
    for edge_path in paths:
        if edge_path in seen:
            continue
        seen.add(edge_path)
        if edge_path.name == "v16b_dependency_edges.csv":
            summary_path = DOC / "v16b_run_summary.csv"
        else:
            prefix = edge_path.name.removesuffix("_fine_dependency_edges.csv")
            summary_path = DOC / f"{prefix}_run_summary.csv"
        if not summary_path.exists():
            raise FileNotFoundError(f"missing run summary for {edge_path.name}")
        specs.append((edge_path.stem, edge_path, summary_path))
    return specs


def build_fine_inventory() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source, edge_path, summary_path in fine_source_specs():
        edges_by_run: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
        for edge in read_csv(edge_path):
            edges_by_run[run_key(edge)].append(edge)
        summaries = read_csv(summary_path)
        for summary in summaries:
            key = run_key(summary)
            analysis = analyze_parents(
                load_history(edges_by_run.get(key, []), int(summary["n_events"]))
            )
            pairs = analysis.n * (analysis.n - 1) // 2
            r_value = analysis.comparable_pairs / pairs
            r_floor = sum(analysis.depths) / pairs
            theta = r_value * (analysis.n - 1) / (analysis.height - 1)
            rows.append(
                {
                    "source": source,
                    "edge_sha256": sha256(edge_path),
                    "summary_sha256": sha256(summary_path),
                    **dict(zip(RUN_KEY, key)),
                    "N": analysis.n,
                    "raw_edges": analysis.raw_edge_count,
                    "r": r_value,
                    "r_floor": r_floor,
                    "r_over_floor": r_value / r_floor,
                    "height": analysis.height,
                    "theta": theta,
                    "qualifies_as_fine_N_other_than_2048_or_3072": int(
                        analysis.n not in {2048, 3072}
                    ),
                }
            )
        print(f"[premise 2.3] inventoried {source}: {len(summaries)} histories")
    write_csv(FINE_INVENTORY_OUTPUT, rows)
    return rows


def theta_extrapolation(
    n_low: int, theta_low: float, n_high: int, theta_high: float
) -> tuple[float, float]:
    exponent = math.log(theta_high / theta_low) / math.log(n_high / n_low)
    if exponent <= 0.0:
        return exponent, float("nan")
    log10_target_n = (
        math.log(n_high) + math.log(5.0 / theta_high) / exponent
    ) / math.log(10.0)
    return exponent, log10_target_n


def fit_theta_scaling(inventory: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    scopes = {
        "WP-F0_sources": {
            "v16b_dependency_edges",
            "v16c_fine_dependency_edges",
            "v16d_fine_dependency_edges",
        },
        "all_fine_on_disk": {str(row["source"]) for row in inventory},
    }
    output: list[dict[str, Any]] = []
    for scope, sources in scopes.items():
        for arm in ("current_global", "exposure_matched_local"):
            selected = [
                row
                for row in inventory
                if row["source"] in sources and row["arm"] == arm
            ]
            by_n: dict[int, list[float]] = defaultdict(list)
            for row in selected:
                by_n[int(row["N"])].append(float(row["theta"]))
            sizes = sorted(by_n)
            if len(sizes) != 2:
                output.append(
                    {
                        "scope": scope,
                        "arm": arm,
                        "status": f"requires exactly two N values; observed {sizes}",
                    }
                )
                continue
            n_low, n_high = sizes
            theta_low = statistics.median(by_n[n_low])
            theta_high = statistics.median(by_n[n_high])
            exponent, log10_target = theta_extrapolation(
                n_low, theta_low, n_high, theta_high
            )
            rng = random.Random(stable_seed((2026090604, scope, arm)))
            boot_exponents: list[float] = []
            boot_log10_targets: list[float] = []
            for _ in range(20000):
                low_sample = rng.choices(by_n[n_low], k=len(by_n[n_low]))
                high_sample = rng.choices(by_n[n_high], k=len(by_n[n_high]))
                boot_exponent, boot_target = theta_extrapolation(
                    n_low,
                    statistics.median(low_sample),
                    n_high,
                    statistics.median(high_sample),
                )
                boot_exponents.append(boot_exponent)
                if math.isfinite(boot_target):
                    boot_log10_targets.append(boot_target)
            output.append(
                {
                    "scope": scope,
                    "arm": arm,
                    "status": "descriptive_two_point_extrapolation_only",
                    "N_low": n_low,
                    "N_high": n_high,
                    "histories_low": len(by_n[n_low]),
                    "histories_high": len(by_n[n_high]),
                    "theta_median_low": theta_low,
                    "theta_median_high": theta_high,
                    "power_exponent": exponent,
                    "power_exponent_ci_low": percentile(boot_exponents, 0.025),
                    "power_exponent_ci_high": percentile(boot_exponents, 0.975),
                    "positive_exponent_bootstrap_fraction": sum(
                        value > 0.0 for value in boot_exponents
                    )
                    / len(boot_exponents),
                    "log10_N_at_theta_5": log10_target,
                    "log10_N_at_theta_5_ci_low": percentile(boot_log10_targets, 0.025),
                    "log10_N_at_theta_5_ci_high": percentile(boot_log10_targets, 0.975),
                    "extrapolation_warning": "only two N values; later sources may not be exchangeable",
                }
            )
    write_csv(THETA_SCALING_OUTPUT, output)
    return output


def max_binomial_distribution(trials: int, copies: int, p_keep: float) -> list[float]:
    binomial_cdf: list[float] = []
    cumulative = 0.0
    for value in range(trials + 1):
        probability = (
            math.comb(trials, value)
            * p_keep**value
            * (1.0 - p_keep) ** (trials - value)
        )
        cumulative += probability
        binomial_cdf.append(min(1.0, cumulative))
    maximum_cdf = [value**copies for value in binomial_cdf]
    probabilities = []
    previous = 0.0
    for value in maximum_cdf:
        probabilities.append(max(0.0, value - previous))
        previous = value
    probabilities[-1] += 1.0 - sum(probabilities)
    return probabilities


def cdf_from_probabilities(probabilities: Sequence[float]) -> list[float]:
    cumulative = 0.0
    result = []
    for probability in probabilities:
        cumulative += probability
        result.append(min(1.0, cumulative))
    result[-1] = 1.0
    return result


def sample_discrete_cdf(cdf: Sequence[float], rng: random.Random) -> int:
    return bisect.bisect_left(cdf, rng.random())


def run_chain_bundle_theory() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    distributions = {
        p_keep: max_binomial_distribution(64, 32, p_keep) for p_keep in P_LEVELS
    }
    theory_rows = []
    for p_keep in P_LEVELS:
        probabilities = distributions[p_keep]
        eligible_probability = sum(probabilities[8:])
        expected_height = sum(
            height * probability for height, probability in enumerate(probabilities)
        )
        expected_log_height_eligible = (
            sum(
                math.log(height) * probabilities[height]
                for height in range(8, len(probabilities))
            )
            / eligible_probability
            if eligible_probability
            else float("nan")
        )
        theory_rows.append(
            {
                "p": p_keep,
                "distribution": "max_32_iid_Binomial_64_p",
                "expected_L": expected_height,
                "probability_L_at_least_8": eligible_probability,
                "expected_log_L_given_L_at_least_8": expected_log_height_eligible,
            }
        )
    write_csv(CHAIN_THEORY_OUTPUT, theory_rows)

    cdfs = {p_keep: cdf_from_probabilities(values) for p_keep, values in distributions.items()}
    rng = random.Random(2026090605)
    wp_f0_slopes: list[float] = []
    literal_slopes: list[float] = []
    for _ in range(200000):
        points_by_p: dict[float, list[int]] = {}
        for p_keep in P_LEVELS:
            if p_keep == 1.0:
                points_by_p[p_keep] = [64] * 20
            else:
                points_by_p[p_keep] = [
                    sample_discrete_cdf(cdfs[p_keep], rng) for _ in range(20)
                ]
        literal_points = [
            (p_keep, height)
            for p_keep, heights in points_by_p.items()
            for height in heights
        ]
        wp_f0_points = [
            (p_keep, height)
            for p_keep, heights in points_by_p.items()
            for height in (heights[:1] if p_keep == 1.0 else heights)
        ]
        literal_slopes.append(fit_draw_slope(literal_points))
        wp_f0_slopes.append(fit_draw_slope(wp_f0_points))
    reference = next(
        row
        for row in read_csv(PROGRAM / "WP-F0_admissibility_per_history.csv")
        if row["label"] == "ref_chain_bundle_32"
    )
    observed = float(reference["decimation_s"])
    procedure_rows = []
    for name, values in (
        ("WP-F0_one_p1_draw", wp_f0_slopes),
        ("literal_20_draws_every_p", literal_slopes),
    ):
        procedure_rows.append(
            {
                "procedure": name,
                "replicates": len(values),
                "mean_s": statistics.fmean(values),
                "median_s": statistics.median(values),
                "s_ci_low": percentile(values, 0.025),
                "s_ci_high": percentile(values, 0.975),
                "WP_F0_observed_s": observed,
                "observed_minus_mean": observed - statistics.fmean(values),
            }
        )
    write_csv(CHAIN_PROCEDURE_OUTPUT, procedure_rows)
    return theory_rows, procedure_rows


def bootstrap_unit_audit() -> list[dict[str, Any]]:
    source_rows = [
        row
        for row in read_csv(PROGRAM / "WP-F0_decimation_draws.csv")
        if row["label"] == "history"
    ]
    aggregate_rows = {
        (row["arm"], int(row["N"])): row
        for row in read_csv(PROGRAM / "WP-F0_admissibility_by_arm.csv")
        if row["label"] == "history"
    }
    output: list[dict[str, Any]] = []
    for arm, n_events in sorted(aggregate_rows):
        selected = [
            row
            for row in source_rows
            if row["arm"] == arm and int(row["N"]) == n_events
        ]
        histories: dict[tuple[str, str, str], list[tuple[float, int]]] = defaultdict(list)
        for row in selected:
            history_key = (row["source"], row["growth_seed"], row["run_offset"])
            histories[history_key].append((float(row["p"]), int(row["L"])))
        pooled_by_p: dict[float, list[int]] = defaultdict(list)
        for points in histories.values():
            for p_keep, height in points:
                pooled_by_p[p_keep].append(height)
        rng = random.Random(stable_seed((2026090606, arm, n_events)))
        within_samples: list[float] = []
        cluster_samples: list[float] = []
        history_keys = list(histories)
        for _ in range(20000):
            within_points = [
                (p_keep, rng.choice(heights))
                for p_keep, heights in pooled_by_p.items()
                for _ in heights
            ]
            within_samples.append(fit_draw_slope(within_points))
            chosen = rng.choices(history_keys, k=len(history_keys))
            cluster_points = [point for key in chosen for point in histories[key]]
            cluster_samples.append(fit_draw_slope(cluster_points))
        central = fit_draw_slope(
            [point for points in histories.values() for point in points]
        )
        reported = aggregate_rows[(arm, n_events)]
        for method, samples in (
            ("within_p_draws_WP_F0", within_samples),
            ("history_cluster", cluster_samples),
        ):
            low = percentile(samples, 0.025)
            high = percentile(samples, 0.975)
            output.append(
                {
                    "arm": arm,
                    "N": n_events,
                    "histories": len(histories),
                    "method": method,
                    "central_s": central,
                    "ci_low": low,
                    "ci_high": high,
                    "ci_width": high - low,
                    "WP_F0_reported_s": reported["pooled_s"],
                    "WP_F0_reported_ci_low": reported["pooled_s_ci_lo"],
                    "WP_F0_reported_ci_high": reported["pooled_s_ci_hi"],
                    "WP_F0_reported_ci_width": reported["pooled_s_ci_width"],
                }
            )
    write_csv(BOOTSTRAP_OUTPUT, output)
    return output


def run_premise_attacks() -> None:
    run_cross_bundle_attack()
    run_conflict_d2_attack()
    inventory = build_fine_inventory()
    fit_theta_scaling(inventory)
    run_chain_bundle_theory()
    bootstrap_unit_audit()
    print("[premise] wrote attacks 2.1--2.4 and bootstrap-unit audit")


def write_blind_manifest() -> None:
    source_paths = [path for _, edge, summary in HISTORY_SOURCES for path in (edge, summary)]
    source_paths.extend(
        [
            PROGRAM / "WP-F0_dimension_admissibility.md",
            ROOT / "relational_universe_v16b_intrinsic_event_dag_gate.py",
            Path(__file__),
            BLIND_HISTORY_OUTPUT,
            BLIND_DRAW_OUTPUT,
        ]
    )
    manifest = {
        "phase": "blind-history-replication-before-WP-F0-code-or-result-inspection",
        "algorithm": "Python frozenset transitive closure; no integer bitsets",
        "decimation_draws_per_p": DECIMATION_DRAWS,
        "files": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in source_paths
        },
    }
    BLIND_MANIFEST.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def self_test() -> None:
    chain = analyze_parents([set(), {0}, {1}, {2}, {3}])
    assert chain.height == 5
    assert chain.comparable_pairs == 10
    assert chain.link_count == 4
    assert chain.max_interval == 5

    redundant = analyze_parents([set(), {0}, {0, 1}, {0, 1, 2}, {0, 1, 2, 3}])
    assert redundant.link_count == 4
    assert redundant.max_interval == 5

    height, r_value = induced_observables(chain.ancestors, frozenset({0, 2, 4}))
    assert height == 3  # closure-induced, despite omitted original edges
    assert r_value == 1.0

    antichain = analyze_parents([set() for _ in range(5)])
    assert antichain.height == 1
    assert antichain.comparable_pairs == 0
    assert antichain.link_count == 0
    assert antichain.max_interval == 1
    print("[replica] self-test pass")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--blind-histories", action="store_true")
    parser.add_argument("--final-histories", action="store_true")
    parser.add_argument("--premise-attacks", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    if args.blind_histories:
        if BLIND_HISTORY_OUTPUT.exists() or BLIND_DRAW_OUTPUT.exists():
            raise FileExistsError("blind artifacts already exist; refusing to overwrite them")
        histories, draws = analyze_histories()
        write_csv(BLIND_HISTORY_OUTPUT, histories)
        write_csv(BLIND_DRAW_OUTPUT, draws)
        write_blind_manifest()
        print(
            f"[replica] wrote histories={len(histories)} draws={len(draws)} "
            f"manifest={BLIND_MANIFEST.relative_to(ROOT)}"
        )
    if args.final_histories:
        histories, draws = analyze_histories_final()
        write_csv(HISTORY_OUTPUT, histories)
        write_csv(DRAW_OUTPUT, draws)
        write_comparison(histories)
        print(
            f"[replica-final] wrote histories={len(histories)} draws={len(draws)} "
            f"comparison={COMPARISON_OUTPUT.relative_to(ROOT)}"
        )
    if args.premise_attacks:
        run_premise_attacks()
    if not any(
        (
            args.self_test,
            args.blind_histories,
            args.final_histories,
            args.premise_attacks,
        )
    ):
        parser.error(
            "select --self-test, --blind-histories, --final-histories, or --premise-attacks"
        )


if __name__ == "__main__":
    main()
