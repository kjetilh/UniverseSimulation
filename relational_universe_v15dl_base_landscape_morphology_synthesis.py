#!/usr/bin/env python3
"""v0.15dl base-landscape morphology synthesis.

No-new-dynamics synthesis after v15dk.

Goal:
- retire the failed low-support rank as a selector candidate,
- consolidate the 1024/add_chord placement landscape over growth seeds
  202, 303, and 404,
- add cheap pre-run graph morphology observables inspired by causal/graph
  geometry analogies, without treating them as physics claims,
- decide whether any morphology rule is good enough to freeze for a small
  fresh holdout.

This script reconstructs base graphs and one add_chord probe per
(growth_seed, placement). It does not run defect dynamics.
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Set, Tuple

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15ae_add_chord_shell_topology_lab as v15ae
import relational_universe_v15cv_add_chord_winning_placement_mechanism_probe as v15cv
import relational_universe_v15da_frozen_intensity_placement_contrast as v15da


DOC = Path("Documentation")

TARGET_NODES = 1024
GROWTH_SEEDS = (202, 303, 404)
PLACEMENTS = (0, 1, 2)
PERTURBATION = "add_chord"
ACTIVE_ESTABLISHED_RATE = 0.50
RANDOM_WALK_STEPS = (2, 4, 6)

RUN_FEATURE_FILES = (
    ("v15dg", DOC / "v15dg_boundary_mass_run_features.csv"),
    ("v15dh", DOC / "v15dh_boundary_mass_run_features.csv"),
    ("v15dk", DOC / "v15dk_support_rank_run_features.csv"),
)
TARGET_FILES = (
    ("v15dg", DOC / "v15dg_boundary_mass_target_summary.csv"),
    ("v15dh", DOC / "v15dh_boundary_mass_target_summary.csv"),
    ("v15dk", DOC / "v15dk_support_rank_target_summary.csv"),
)

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

RESPONSE_AUDIT_METRICS = (
    "w32_mean_boundary_per_mass",
    "static_mean_support_degree",
    "genealogy_intensity_index",
)


def safe_float(x: Any, default: float = float("nan")) -> float:
    try:
        if x is None or x == "":
            return default
        return float(x)
    except (TypeError, ValueError):
        return default


def safe_div(num: float, den: float) -> float:
    if not math.isfinite(num) or not math.isfinite(den) or den == 0.0:
        return float("nan")
    return num / den


def fmt(x: Any, digits: int = 3) -> str:
    y = safe_float(x)
    if not math.isfinite(y):
        return "nan"
    return f"{y:.{digits}f}"


def mean_defined(values: Iterable[float]) -> float:
    vals = [safe_float(x) for x in values]
    vals = [x for x in vals if math.isfinite(x)]
    return sum(vals) / len(vals) if vals else float("nan")


def median_defined(values: Iterable[float]) -> float:
    vals = sorted(x for x in (safe_float(v) for v in values) if math.isfinite(x))
    if not vals:
        return float("nan")
    mid = len(vals) // 2
    if len(vals) % 2:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2.0


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: str | Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_label_counts(raw: str) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for item in str(raw).split(";"):
        if not item or ":" not in item:
            continue
        key, val = item.rsplit(":", 1)
        try:
            out[key] = int(val)
        except ValueError:
            out[key] = 0
    return out


def mode_string(values: Sequence[str]) -> str:
    vals = [str(v) for v in values if str(v) != ""]
    if not vals:
        return ""
    counts = Counter(vals)
    best = max(counts.values())
    return "|".join(sorted(k for k, v in counts.items() if v == best))


def pairwise_auc(pos_values: Sequence[float], neg_values: Sequence[float]) -> float:
    pos = [x for x in pos_values if math.isfinite(x)]
    neg = [x for x in neg_values if math.isfinite(x)]
    if not pos or not neg:
        return float("nan")
    wins = 0.0
    total = 0
    for p in pos:
        for n in neg:
            total += 1
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return wins / total if total else float("nan")


def rank_values(values: Sequence[float]) -> List[float]:
    indexed = sorted((safe_float(v), i) for i, v in enumerate(values))
    ranks = [float("nan")] * len(values)
    pos = 0
    while pos < len(indexed):
        val = indexed[pos][0]
        end = pos
        while end < len(indexed) and indexed[end][0] == val:
            end += 1
        rank = (pos + 1 + end) / 2.0
        for _, original in indexed[pos:end]:
            ranks[original] = rank
        pos = end
    return ranks


def spearman(xs: Sequence[float], ys: Sequence[float]) -> float:
    pts = [(safe_float(x), safe_float(y)) for x, y in zip(xs, ys)]
    pts = [(x, y) for x, y in pts if math.isfinite(x) and math.isfinite(y)]
    if len(pts) < 3:
        return float("nan")
    rx = rank_values([x for x, _ in pts])
    ry = rank_values([y for _, y in pts])
    mx = mean_defined(rx)
    my = mean_defined(ry)
    num = sum((x - mx) * (y - my) for x, y in zip(rx, ry))
    denx = math.sqrt(sum((x - mx) ** 2 for x in rx))
    deny = math.sqrt(sum((y - my) ** 2 for y in ry))
    return safe_div(num, denx * deny)


def load_run_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for lab, path in RUN_FEATURE_FILES:
        for raw in read_csv(path):
            row: Dict[str, Any] = dict(raw)
            row["source_lab"] = lab
            rows.append(row)
    return rows


def load_target_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for lab, path in TARGET_FILES:
        for raw in read_csv(path):
            row: Dict[str, Any] = dict(raw)
            row["source_lab"] = lab
            rows.append(row)
    return rows


def placement_summary_rows(run_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[int, int], List[Mapping[str, Any]]] = defaultdict(list)
    for row in run_rows:
        if int(safe_float(row.get("target_nodes"))) != TARGET_NODES:
            continue
        seed = int(safe_float(row.get("growth_seed")))
        placement = int(safe_float(row.get("placement")))
        if seed in GROWTH_SEEDS and placement in PLACEMENTS:
            grouped[(seed, placement)].append(row)

    out: List[Dict[str, Any]] = []
    for (seed, placement), group in sorted(grouped.items()):
        counts = Counter(str(row.get("far_shell_horizon_label", "")) for row in group)
        n = len(group)
        established_rate = counts.get("established_far_shell_horizon", 0) / max(1, n)
        row: Dict[str, Any] = {
            "target_nodes": TARGET_NODES,
            "growth_seed": seed,
            "placement": placement,
            "profile_label": f"{PERTURBATION}_p{placement}",
            "source_labs": ";".join(sorted({str(x.get("source_lab", "")) for x in group})),
            "n_runs": n,
            "support_signature_mode": mode_string([str(x.get("support_signature", "")) for x in group]),
            "support_signature_unique_count": len({str(x.get("support_signature", "")) for x in group}),
            "label_counts": ";".join(f"{key}:{counts[key]}" for key in sorted(counts)),
            "established_rate": established_rate,
            "active_placement": int(established_rate >= ACTIVE_ESTABLISHED_RATE),
            "mixed_rate": counts.get("mixed_far_shell_horizon", 0) / max(1, n),
            "no_horizon_rate": counts.get("no_far_shell_horizon", 0) / max(1, n),
            "mean_high_horizon_span": mean_defined(safe_float(x.get("high_horizon_span")) for x in group),
            "median_high_horizon_span": median_defined(safe_float(x.get("high_horizon_span")) for x in group),
            "median_boundary_mass": median_defined(safe_float(x.get("w32_mean_boundary_per_mass")) for x in group),
            "median_genealogy_intensity": median_defined(safe_float(x.get("genealogy_intensity_index")) for x in group),
        }
        for metric in RESPONSE_AUDIT_METRICS:
            row[f"median_{metric}"] = median_defined(safe_float(x.get(metric)) for x in group)
            row[f"mean_{metric}"] = mean_defined(safe_float(x.get(metric)) for x in group)
        out.append(row)
    return out


def bfs_limited(g: Any, sources: Iterable[int], max_depth: int | None = None) -> Dict[int, int]:
    seen: Dict[int, int] = {}
    queue: List[int] = []
    for source in sources:
        s = int(source)
        if s in seen:
            continue
        seen[s] = 0
        queue.append(s)
    head = 0
    while head < len(queue):
        v = queue[head]
        head += 1
        depth = seen[v]
        if max_depth is not None and depth >= max_depth:
            continue
        for u in g.neighbors(v):
            if u not in seen:
                seen[int(u)] = depth + 1
                queue.append(int(u))
    return seen


def induced_subgraph(g: Any, nodes: Iterable[int]) -> v7.UGraph:
    keep = {int(x) for x in nodes}
    sub = v7.UGraph()
    for v in keep:
        sub.add_node(v)
    for v in keep:
        for u in g.neighbors(v):
            if u in keep and v < u:
                sub.add_edge(v, int(u))
    return sub


def boundary_to_volume(g: Any, nodes: Iterable[int]) -> float:
    keep = {int(x) for x in nodes}
    if not keep:
        return float("nan")
    return v15.boundary_edge_count(g, keep) / max(1, len(keep))


def pair_distance_stats(g: Any, nodes: Sequence[int]) -> Dict[str, float]:
    nodes = sorted({int(x) for x in nodes})
    distances: List[float] = []
    inv_sum = 0.0
    pair_count = 0
    for idx, a in enumerate(nodes):
        dist = bfs_limited(g, [a])
        for b in nodes[idx + 1:]:
            pair_count += 1
            d = dist.get(b)
            if d is None or d <= 0:
                continue
            distances.append(float(d))
            inv_sum += 1.0 / float(d)
    return {
        "pair_count": float(pair_count),
        "connected_pair_count": float(len(distances)),
        "mean_pair_distance": mean_defined(distances),
        "efficiency": safe_div(inv_sum, pair_count),
    }


def harmonic_reach_from_support(g: Any, support: Sequence[int]) -> float:
    dist = bfs_limited(g, support)
    vals = [1.0 / d for node, d in dist.items() if d > 0]
    return mean_defined(vals)


def random_walk_returns(g: Any, support: Sequence[int], steps: Sequence[int]) -> Dict[str, float]:
    max_step = max(steps)
    wanted = set(int(x) for x in steps)
    accum: Dict[int, List[float]] = {int(x): [] for x in steps}
    for start in sorted({int(x) for x in support}):
        probs: Dict[int, float] = {start: 1.0}
        for t in range(1, max_step + 1):
            nxt: Dict[int, float] = defaultdict(float)
            for node, prob in probs.items():
                ns = list(g.neighbors(node))
                if not ns:
                    nxt[node] += prob
                    continue
                share = prob / len(ns)
                for nbr in ns:
                    nxt[int(nbr)] += share
            probs = dict(nxt)
            if t in wanted:
                accum[t].append(float(probs.get(start, 0.0)))
    out = {f"return_t{t}": mean_defined(accum[t]) for t in steps}
    out["return_spectral_dim_proxy"] = return_spectral_dim_proxy(out, steps)
    return out


def return_spectral_dim_proxy(return_row: Mapping[str, float], steps: Sequence[int]) -> float:
    pts: List[Tuple[float, float]] = []
    for t in steps:
        p = safe_float(return_row.get(f"return_t{t}"))
        if p > 0.0:
            pts.append((math.log(float(t)), math.log(p)))
    if len(pts) < 2:
        return float("nan")
    slope, _ = v7.linear_fit([x for x, _ in pts], [y for _, y in pts])
    return -2.0 * slope if math.isfinite(slope) else float("nan")


def forman_edge(g: Any, a: int, b: int) -> float:
    return 4.0 - float(g.degree(a)) - float(g.degree(b))


def incident_support_edges(g: Any, support: Sequence[int]) -> Set[Tuple[int, int]]:
    support_set = {int(x) for x in support}
    out: Set[Tuple[int, int]] = set()
    for a in support_set:
        for b in g.neighbors(a):
            edge = (a, int(b)) if a < int(b) else (int(b), a)
            out.add(edge)
    return out


def edge_forman_stats(g: Any, edges: Iterable[Tuple[int, int]], prefix: str) -> Dict[str, float]:
    values = [forman_edge(g, int(a), int(b)) for a, b in edges]
    return {
        f"{prefix}_count": float(len(values)),
        f"{prefix}_mean_forman": mean_defined(values),
        f"{prefix}_min_forman": min(values) if values else float("nan"),
        f"{prefix}_max_forman": max(values) if values else float("nan"),
    }


def support_for_placement(base_state: Any, placement: int) -> Tuple[List[int], Dict[str, Any], Any]:
    probe = base_state.clone()
    info = v15.v14.v08b.apply_custom_perturbation(
        probe,
        PERTURBATION,
        center_token_index=int(placement),
    )
    support = [int(x) for x in info.get("support", [])]
    return support, dict(info), probe


def base_states_by_seed() -> Tuple[Dict[int, Any], List[Mapping[str, Any]]]:
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, base_rows = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    by_seed = {
        int(seed): base_states[(ensembles[0].name, int(seed))]
        for seed in GROWTH_SEEDS
    }
    return by_seed, base_rows


def morphology_for_seed_placement(base_state: Any, growth_seed: int, placement: int) -> Dict[str, Any]:
    support, info, probe = support_for_placement(base_state, placement)
    support_set = set(support)
    base_g = base_state.g
    post_g = probe.g

    support_features = v15cv.support_mechanism_features(
        target=TARGET_NODES,
        base_state=base_state,
        placement=int(placement),
        seed_delta=-1,
        run_seed=-1,
        support=support,
    )
    ball1 = safe_float(support_features.get("support_ball_1"))
    ball2 = safe_float(support_features.get("support_ball_2"))
    ball3 = safe_float(support_features.get("support_ball_3"))

    ball3_nodes = set(bfs_limited(base_g, support, max_depth=3).keys())
    ball3_base_sub = induced_subgraph(base_g, ball3_nodes)
    base_pair = pair_distance_stats(base_g, sorted(ball3_nodes))
    post_pair = pair_distance_stats(post_g, sorted(ball3_nodes))
    base_return = random_walk_returns(base_g, support, RANDOM_WALK_STEPS)
    post_return = random_walk_returns(post_g, support, RANDOM_WALK_STEPS)

    base_edges = base_g.edge_set()
    post_edges = post_g.edge_set()
    new_edges = sorted(post_edges - base_edges)
    removed_edges = sorted(base_edges - post_edges)
    base_incident = incident_support_edges(base_g, support)
    post_incident = incident_support_edges(post_g, support)
    base_forman = edge_forman_stats(base_g, base_incident, "base_incident_support_edge")
    post_forman = edge_forman_stats(post_g, post_incident, "post_incident_support_edge")
    new_forman = edge_forman_stats(post_g, new_edges, "new_edge")

    row: Dict[str, Any] = {
        "target_nodes": TARGET_NODES,
        "growth_seed": int(growth_seed),
        "placement": int(placement),
        "profile_label": f"{PERTURBATION}_p{placement}",
        "perturbation": PERTURBATION,
        "support_signature": ",".join(str(x) for x in support),
        "requested_match": int(v15.v14.perturbation_requested_match(PERTURBATION, str(info.get("type", "unknown")))),
        "base_nodes": int(base_g.num_nodes()),
        "base_edges": int(base_g.num_edges()),
        "base_beta1": int(v7.beta1_cycle_rank(base_g)),
        "support_ball2_minus_ball1": ball2 - ball1 if math.isfinite(ball2) and math.isfinite(ball1) else float("nan"),
        "support_ball3_minus_ball1": ball3 - ball1 if math.isfinite(ball3) and math.isfinite(ball1) else float("nan"),
        "support_ball3_minus_ball2": ball3 - ball2 if math.isfinite(ball3) and math.isfinite(ball2) else float("nan"),
        "local_ball3_node_count": len(ball3_nodes),
        "local_ball3_internal_edges": int(ball3_base_sub.num_edges()),
        "local_ball3_beta1": int(v7.beta1_cycle_rank(ball3_base_sub)),
        "local_ball3_boundary_to_volume": boundary_to_volume(base_g, ball3_nodes),
        "base_ball3_pair_count": base_pair["pair_count"],
        "base_ball3_connected_pair_count": base_pair["connected_pair_count"],
        "base_ball3_mean_pair_distance": base_pair["mean_pair_distance"],
        "base_ball3_efficiency": base_pair["efficiency"],
        "post_ball3_mean_pair_distance": post_pair["mean_pair_distance"],
        "post_ball3_efficiency": post_pair["efficiency"],
        "delta_ball3_mean_pair_distance": post_pair["mean_pair_distance"] - base_pair["mean_pair_distance"],
        "delta_ball3_efficiency": post_pair["efficiency"] - base_pair["efficiency"],
        "base_support_harmonic_reach": harmonic_reach_from_support(base_g, support),
        "post_support_harmonic_reach": harmonic_reach_from_support(post_g, support),
        "new_edge_count": len(new_edges),
        "removed_edge_count": len(removed_edges),
        "new_edges": ";".join(f"{a}-{b}" for a, b in new_edges),
        "removed_edges": ";".join(f"{a}-{b}" for a, b in removed_edges),
    }
    row.update({k: support_features[k] for k in support_features if k not in row})
    row["delta_support_harmonic_reach"] = safe_float(row["post_support_harmonic_reach"]) - safe_float(row["base_support_harmonic_reach"])
    for t in RANDOM_WALK_STEPS:
        row[f"base_return_t{t}"] = base_return[f"return_t{t}"]
        row[f"post_return_t{t}"] = post_return[f"return_t{t}"]
        row[f"delta_return_t{t}"] = post_return[f"return_t{t}"] - base_return[f"return_t{t}"]
    row["base_return_spectral_dim_proxy"] = base_return["return_spectral_dim_proxy"]
    row["post_return_spectral_dim_proxy"] = post_return["return_spectral_dim_proxy"]
    row["delta_return_spectral_dim_proxy"] = (
        post_return["return_spectral_dim_proxy"] - base_return["return_spectral_dim_proxy"]
    )
    row["base_mean_forman_incident_support"] = base_forman["base_incident_support_edge_mean_forman"]
    row["base_min_forman_incident_support"] = base_forman["base_incident_support_edge_min_forman"]
    row["post_mean_forman_incident_support"] = post_forman["post_incident_support_edge_mean_forman"]
    row["post_min_forman_incident_support"] = post_forman["post_incident_support_edge_min_forman"]
    row["delta_mean_forman_incident_support"] = (
        row["post_mean_forman_incident_support"] - row["base_mean_forman_incident_support"]
    )
    row["new_edge_mean_forman"] = new_forman["new_edge_mean_forman"]
    row["new_edge_min_forman"] = new_forman["new_edge_min_forman"]
    row["support_over_ball3_fraction"] = safe_div(safe_float(row["support_size"]), safe_float(row["support_ball_3"]))
    row["support_ball1_over_ball3"] = safe_div(ball1, ball3)
    return row


def morphology_rows() -> List[Dict[str, Any]]:
    states, _base_rows = base_states_by_seed()
    out: List[Dict[str, Any]] = []
    for seed in GROWTH_SEEDS:
        for placement in PLACEMENTS:
            out.append(morphology_for_seed_placement(states[seed], seed, placement))
    return out


def merge_placement_and_morphology(
    placement_rows: Sequence[Mapping[str, Any]],
    morphology: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    morph_by_key = {
        (int(row["growth_seed"]), int(row["placement"])): row
        for row in morphology
    }
    out: List[Dict[str, Any]] = []
    for raw in placement_rows:
        key = (int(raw["growth_seed"]), int(raw["placement"]))
        row = dict(raw)
        row.update({f"morph_{k}": v for k, v in morph_by_key[key].items() if k not in {"growth_seed", "placement"}})
        for metric in MORPHOLOGY_METRICS:
            if metric in morph_by_key[key]:
                row[metric] = morph_by_key[key][metric]
        out.append(row)
    return sorted(out, key=lambda r: (int(r["growth_seed"]), int(r["placement"])))


def oriented_value(row: Mapping[str, Any], metric: str, direction: str) -> float:
    value = safe_float(row.get(metric))
    return -value if direction == "low" else value


def metric_score_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    active = [row for row in rows if int(safe_float(row.get("active_placement"))) == 1]
    inactive = [row for row in rows if int(safe_float(row.get("active_placement"))) == 0]
    out: List[Dict[str, Any]] = []
    for metric in MORPHOLOGY_METRICS:
        high_auc = pairwise_auc(
            [safe_float(row.get(metric)) for row in active],
            [safe_float(row.get(metric)) for row in inactive],
        )
        low_auc = pairwise_auc(
            [-safe_float(row.get(metric)) for row in active],
            [-safe_float(row.get(metric)) for row in inactive],
        )
        best_direction = "high" if safe_float(high_auc) >= safe_float(low_auc) else "low"
        best_auc = max(safe_float(high_auc), safe_float(low_auc))
        out.append(
            {
                "metric": metric,
                "feature_family": feature_family(metric),
                "n_active_placements": len(active),
                "n_inactive_placements": len(inactive),
                "auc_active_vs_inactive_high": high_auc,
                "auc_active_vs_inactive_low": low_auc,
                "best_direction_posthoc": best_direction,
                "best_auc_posthoc": best_auc,
                "spearman_vs_established_rate_raw": spearman(
                    [safe_float(row.get(metric)) for row in rows],
                    [safe_float(row.get("established_rate")) for row in rows],
                ),
                "median_active_raw": median_defined(safe_float(row.get(metric)) for row in active),
                "median_inactive_raw": median_defined(safe_float(row.get(metric)) for row in inactive),
            }
        )
    return sorted(out, key=lambda r: (-safe_float(r["best_auc_posthoc"]), str(r["metric"])))


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


def rule_score_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    by_seed: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        by_seed[int(row["growth_seed"])].append(row)
    for metric in MORPHOLOGY_METRICS:
        for direction in ("high", "low"):
            seed_rows: List[Dict[str, Any]] = []
            total_active = 0
            top1_capture = 0
            top2_capture = 0
            top1_hit = 0
            top2_hit = 0
            top1_inactive = 0
            top2_inactive = 0
            for seed, group in sorted(by_seed.items()):
                ranked = sorted(
                    group,
                    key=lambda row: (-oriented_value(row, metric, direction), int(row["placement"])),
                )
                active_set = {int(row["placement"]) for row in group if int(row["active_placement"]) == 1}
                top1 = {int(row["placement"]) for row in ranked[:1]}
                top2 = {int(row["placement"]) for row in ranked[:2]}
                total_active += len(active_set)
                top1_capture += len(active_set & top1)
                top2_capture += len(active_set & top2)
                top1_hit += int(bool(active_set & top1))
                top2_hit += int(bool(active_set & top2))
                top1_inactive += len(top1 - active_set)
                top2_inactive += len(top2 - active_set)
                seed_rows.append(
                    {
                        "seed": seed,
                        "ranked": ";".join(f"p{int(row['placement'])}" for row in ranked),
                        "active": ";".join(f"p{x}" for x in sorted(active_set)),
                    }
                )
            top1_frac = safe_div(top1_capture, total_active)
            top2_frac = safe_div(top2_capture, total_active)
            top1_hit_rate = safe_div(top1_hit, len(by_seed))
            top2_hit_rate = safe_div(top2_hit, len(by_seed))
            if top1_frac == 1.0 and top1_hit_rate == 1.0:
                status = "posthoc_full_top1_candidate_not_validated"
            elif top2_frac == 1.0 and top2_hit_rate == 1.0:
                status = "posthoc_top2_candidate_not_validated"
            elif top2_hit_rate == 1.0 and top2_frac >= 0.75:
                status = "weak_posthoc_top2_scout"
            else:
                status = "not_selector_ready"
            out.append(
                {
                    "metric": metric,
                    "feature_family": feature_family(metric),
                    "direction": direction,
                    "growth_seed_count": len(by_seed),
                    "top1_hit_rate": top1_hit_rate,
                    "top2_hit_rate": top2_hit_rate,
                    "top1_capture_fraction": top1_frac,
                    "top2_capture_fraction": top2_frac,
                    "top1_inactive_selected": top1_inactive,
                    "top2_inactive_selected": top2_inactive,
                    "ranked_by_seed": " | ".join(f"{r['seed']}:{r['ranked']} active={r['active']}" for r in seed_rows),
                    "rule_status": status,
                    "posthoc_warning": "rule derived after seeing v15dg/v15dh/v15dk outcomes",
                }
            )
    return sorted(
        out,
        key=lambda r: (
            -safe_float(r["top1_capture_fraction"]),
            -safe_float(r["top2_capture_fraction"]),
            safe_float(r["top1_inactive_selected"]),
            str(r["metric"]),
            str(r["direction"]),
        ),
    )


def landscape_shift_rows(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    by_seed: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        by_seed[int(row["growth_seed"])].append(row)
    for seed, group in sorted(by_seed.items()):
        active = [row for row in group if int(row["active_placement"]) == 1]
        strongest = sorted(group, key=lambda row: (-safe_float(row["established_rate"]), int(row["placement"])))
        out.append(
            {
                "growth_seed": seed,
                "active_placements": ";".join(f"p{int(row['placement'])}" for row in active),
                "strongest_placement": f"p{int(strongest[0]['placement'])}" if strongest else "",
                "strongest_established_rate": safe_float(strongest[0]["established_rate"]) if strongest else float("nan"),
                "landscape_class": landscape_class(active, group),
                "placement_rates": ";".join(
                    f"p{int(row['placement'])}:{fmt(row['established_rate'])}" for row in sorted(group, key=lambda r: int(r["placement"]))
                ),
                "support_signatures": ";".join(
                    f"p{int(row['placement'])}:{row.get('support_signature_mode', '')}"
                    for row in sorted(group, key=lambda r: int(r["placement"]))
                ),
            }
        )
    return out


def landscape_class(active: Sequence[Mapping[str, Any]], group: Sequence[Mapping[str, Any]]) -> str:
    if not active:
        return "no_active_placement"
    if len(active) == 1:
        return f"single_active_p{int(active[0]['placement'])}"
    return "multi_active_" + "_".join(f"p{int(row['placement'])}" for row in active)


def diagnosis_rows(
    *,
    target_rows: Sequence[Mapping[str, Any]],
    placement_rows: Sequence[Mapping[str, Any]],
    morphology: Sequence[Mapping[str, Any]],
    metric_scores: Sequence[Mapping[str, Any]],
    rule_scores: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    separated = [int(safe_float(row.get("separated_from_prev"), 1)) for row in target_rows]
    artifact_clean = all(x == 1 for x in separated) and all(int(row.get("requested_match", 0)) == 1 for row in morphology)
    active_by_seed = {
        int(seed): [int(row["placement"]) for row in group if int(row["active_placement"]) == 1]
        for seed, group in group_by_seed(placement_rows).items()
    }
    active_patterns = {tuple(v) for v in active_by_seed.values()}
    best_rule = rule_scores[0] if rule_scores else {}
    best_metric = metric_scores[0] if metric_scores else {}
    if best_rule and str(best_rule.get("rule_status")) in {
        "posthoc_full_top1_candidate_not_validated",
        "posthoc_top2_candidate_not_validated",
        "weak_posthoc_top2_scout",
    }:
        morphology_status = str(best_rule.get("rule_status"))
        next_step = "freeze_best_morphology_rule_for_small_v15dm_holdout"
        next_note = (
            f"Beste post-hoc regel er `{best_rule.get('metric')}`/{best_rule.get('direction')}; "
            "den maa fryses foer ny dynamikk og kan ikke rapporteres som validert."
        )
    else:
        morphology_status = "no_selector_ready_morphology_rule"
        next_step = "do_not_spend_dynamic_budget_on_selector_holdout_yet"
        next_note = "Ingen pre-run morfologiregel er sterk nok paa eksisterende seeds til aa rettferdiggjore frozen holdout."

    return [
        {
            "diagnostic_family": "artifact_control",
            "status": "clean" if artifact_clean else "unclear",
            "note": "Target summaries are separated and add_chord requested-match is clean." if artifact_clean else "Artifact hygiene needs inspection before claims.",
        },
        {
            "diagnostic_family": "landscape_state",
            "status": "base_conditioned_placement_landscape",
            "note": f"Active placements vary by growth seed: {active_by_seed}; unique patterns={len(active_patterns)}.",
        },
        {
            "diagnostic_family": "retired_selector",
            "status": "low_support_rank_retired",
            "note": "v15dk top1/top2 support-rank capture was zero; low local support volume/gap should not be reused as selector.",
        },
        {
            "diagnostic_family": "morphology_screen",
            "status": morphology_status,
            "note": (
                f"Best placement-level AUC metric is `{best_metric.get('metric', '')}` "
                f"with posthoc AUC={fmt(best_metric.get('best_auc_posthoc'))}; "
                f"best rule status={best_rule.get('rule_status', '')}."
            ),
        },
        {
            "diagnostic_family": "next_step",
            "status": next_step,
            "note": next_note,
        },
    ]


def group_by_seed(rows: Sequence[Mapping[str, Any]]) -> Dict[int, List[Mapping[str, Any]]]:
    grouped: Dict[int, List[Mapping[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[int(row["growth_seed"])].append(row)
    return grouped


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
    landscape_rows: Sequence[Mapping[str, Any]],
    morphology: Sequence[Mapping[str, Any]],
    metric_scores: Sequence[Mapping[str, Any]],
    rule_scores: Sequence[Mapping[str, Any]],
    diagnosis: Sequence[Mapping[str, Any]],
) -> str:
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15dl: base-landscape morphology synthesis")
    lines.append("")
    lines.append("## Formal")
    lines.append("")
    lines.append("Dette er en no-new-dynamics syntese etter v15dk.")
    lines.append("Den samler eksisterende `1024/add_chord/p0,p1,p2`-resultater fra growth seeds `202`, `303` og `404`,")
    lines.append("og legger til billige pre-run morfologiobservabler paa basegrafen og add_chord-proben.")
    lines.append("Gamle dynamiske labels brukes bare som responskolonner, ikke som nye runtime-resultater.")
    lines.append("")
    lines.append("## Landscape by growth seed")
    lines.append("")
    lines.extend(table(landscape_rows, ("growth_seed", "landscape_class", "active_placements", "placement_rates")))
    lines.append("")
    lines.append("## Placement summary")
    lines.append("")
    lines.extend(
        table(
            placement_rows,
            (
                "growth_seed",
                "placement",
                "label_counts",
                "established_rate",
                "mean_high_horizon_span",
                "support_signature_mode",
                "support_ball_1",
                "support_ball_2",
                "support_ball_3",
                "delta_ball3_efficiency",
                "base_return_spectral_dim_proxy",
            ),
        )
    )
    lines.append("")
    lines.append("## Best morphology screens")
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
    lines.append("## Best rule screens")
    lines.append("")
    lines.extend(
        table(
            rule_scores,
            (
                "metric",
                "direction",
                "top1_capture_fraction",
                "top2_capture_fraction",
                "top1_inactive_selected",
                "top2_inactive_selected",
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
    lines.append("## Evidensgrenser")
    lines.append("")
    lines.append("- Dette er ikke ny dynamikk; alle outcome-kolonner kommer fra eksisterende v15dg/v15dh/v15dk-run.")
    lines.append("- Morfologireglene er post-hoc screens. De kan foreslaa en frossen v15dm-test, men er ikke validert her.")
    lines.append("- Ikke bruk dette som Lorentz-, global invariant-, entanglement-, partikkel- eller universell geometri-claim.")
    return "\n".join(lines) + "\n"


def build_operational_note(diagnosis: Sequence[Mapping[str, Any]], rule_scores: Sequence[Mapping[str, Any]]) -> str:
    best = rule_scores[0] if rule_scores else {}
    lines = ["# Operativ anbefaling v0.15dl", ""]
    for row in diagnosis:
        lines.append(f"- `{row['diagnostic_family']}`: `{row['status']}` fordi {row['note']}")
    lines.append("")
    lines.append("- Ikke gjenbruk low-support-rank som selector.")
    lines.append("- Behandle beste morfologiregel som post-hoc kandidat, ikke som evidens.")
    if best:
        lines.append(
            f"- Hvis vi gaar til v15dm, frys `{best.get('metric')}` med retning `{best.get('direction')}` foer ny dynamikk."
        )
    lines.append("- Ikke oppgrader funnene til invariant/Lorentz/partikkel/entanglement-claim.")
    return "\n".join(lines) + "\n"


def build_lay_note(diagnosis: Sequence[Mapping[str, Any]]) -> str:
    diag = {str(row["diagnostic_family"]): row for row in diagnosis}
    return "\n".join(
        [
            "# Relasjonell universgraf for ikke-spesialister v0.15dl",
            "",
            "Denne runden brukte ikke mer simulasjonsbudsjett. Den saa paa gamle resultater og spurte:",
            "finnes det noe i selve startgrafens lokale form som kan forklare hvilke add_chord-plasseringer som virker?",
            "",
            f"- Landskapet: `{diag['landscape_state']['status']}`.",
            f"- Gammel support-rank: `{diag['retired_selector']['status']}`.",
            f"- Ny morfologiscreen: `{diag['morphology_screen']['status']}`.",
            f"- Neste steg: `{diag['next_step']['status']}`.",
            "",
            "Dette er en forsiktig prior-test, ikke en paastand om en ferdig fysikklov.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="v0.15dl base-landscape morphology synthesis.")
    p.add_argument("--out-target-csv", default=str(DOC / "v15dl_base_landscape_target_summary.csv"))
    p.add_argument("--out-morphology-csv", default=str(DOC / "v15dl_base_landscape_morphology_features.csv"))
    p.add_argument("--out-placement-csv", default=str(DOC / "v15dl_base_landscape_placement_summary.csv"))
    p.add_argument("--out-landscape-csv", default=str(DOC / "v15dl_base_landscape_seed_summary.csv"))
    p.add_argument("--out-metric-csv", default=str(DOC / "v15dl_base_landscape_metric_scores.csv"))
    p.add_argument("--out-rule-csv", default=str(DOC / "v15dl_base_landscape_rule_scores.csv"))
    p.add_argument("--out-diagnosis-csv", default=str(DOC / "v15dl_base_landscape_diagnosis.csv"))
    p.add_argument("--out-summary-md", default=str(DOC / "v15dl_base_landscape_morphology_synthesis.md"))
    p.add_argument("--out-op-md", default=str(DOC / "v0_15dl_operativ_anbefaling.md"))
    p.add_argument("--out-lay-md", default=str(DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_15dl.md"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_rows = load_run_rows()
    target_rows = load_target_rows()
    placement_base = placement_summary_rows(run_rows)
    morphology = morphology_rows()
    placement_rows = merge_placement_and_morphology(placement_base, morphology)
    landscape_rows = landscape_shift_rows(placement_rows)
    metric_scores = metric_score_rows(placement_rows)
    rule_scores = rule_score_rows(placement_rows)
    diagnosis = diagnosis_rows(
        target_rows=target_rows,
        placement_rows=placement_rows,
        morphology=morphology,
        metric_scores=metric_scores,
        rule_scores=rule_scores,
    )

    write_csv(args.out_target_csv, target_rows)
    write_csv(args.out_morphology_csv, morphology)
    write_csv(args.out_placement_csv, placement_rows)
    write_csv(args.out_landscape_csv, landscape_rows)
    write_csv(args.out_metric_csv, metric_scores)
    write_csv(args.out_rule_csv, rule_scores)
    write_csv(args.out_diagnosis_csv, diagnosis)
    Path(args.out_summary_md).write_text(
        build_report(
            placement_rows=placement_rows,
            landscape_rows=landscape_rows,
            morphology=morphology,
            metric_scores=metric_scores,
            rule_scores=rule_scores,
            diagnosis=diagnosis,
        ),
        encoding="utf-8",
    )
    Path(args.out_op_md).write_text(build_operational_note(diagnosis, rule_scores), encoding="utf-8")
    Path(args.out_lay_md).write_text(build_lay_note(diagnosis), encoding="utf-8")
    print(f"wrote {args.out_summary_md}")
    print(f"wrote {args.out_diagnosis_csv}")


if __name__ == "__main__":
    main()
