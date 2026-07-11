#!/usr/bin/env python3
"""v0.15du relabel and local-isomorphism symmetry gate.

No-new-dynamics audit after v15dt.

This script separates three questions that earlier feature-level
"near-symmetry" labels did not separate:

1. Does the stochastic transition kernel transform covariantly when graph
   node ids are relabelled?
2. Does the deterministic add_chord perturbation constructor select the
   transported chord under the same relabelling?
3. Do marked local perturbation environments form repeated exact
   isomorphism classes, and do existing dynamic responses agree inside them?

The result is an implementation/observable gate. It is not evidence for a
physical symmetry, Noether law, Lorentz invariance, particles, entanglement,
or a universal geometry.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

try:
    import networkx as nx
except ImportError as exc:  # pragma: no cover - explicit runtime dependency gate
    raise SystemExit("v15du requires networkx for exact marked-graph isomorphism") from exc

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v08b_natural_ensemble_robustness as v08b
import relational_universe_v10e_focused_band_validation as v10e
import relational_universe_v15_defect_lifetime_lab as v15
import relational_universe_v15dl_base_landscape_morphology_synthesis as v15dl
import relational_universe_v15dn_multi_active_landscape_synthesis as v15dn
import relational_universe_v15dq_active_set_taxonomy_synthesis as v15dq


DOC = Path("Documentation")

TARGET_NODES = 1024
PERTURBATION = "add_chord"
PLACEMENTS = (0, 1, 2)
GROWTH_SEEDS = (
    202,
    303,
    404,
    505,
    606,
    707,
    808,
    909,
    1001,
    1103,
    1201,
    1301,
    1409,
    1511,
    1601,
    1709,
)
RELABEL_SEEDS = (19001, 19037, 19081, 19121)
LOCAL_RADII = (1, 2, 3)
LOCAL_MATCH_MODES = ("structural", "boundary_aware")
KERNEL_TOLERANCE = 1.0e-12

V15DR_PLACEMENT_CSV = DOC / "v15dr_active_set_taxonomy_mapper_placement_summary.csv"
V15DS_PLACEMENT_CSV = DOC / "v15ds_active_set_landscape_atlas_placement_summary.csv"


def safe_float(value: Any, default: float = float("nan")) -> float:
    return v15dn.safe_float(value, default)


def safe_int(value: Any, default: int = 0) -> int:
    return v15dn.safe_int(value, default)


def safe_div(numerator: float, denominator: float) -> float:
    if not math.isfinite(numerator) or not math.isfinite(denominator) or denominator == 0.0:
        return float("nan")
    return numerator / denominator


def fmt(value: Any, digits: int = 3) -> str:
    return v15dn.fmt(value, digits=digits)


def mean_defined(values: Iterable[Any]) -> float:
    return v15dn.mean_defined(values)


def median_defined(values: Iterable[Any]) -> float:
    return v15dn.median_defined(values)


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(
    path: str | Path,
    rows: Sequence[Mapping[str, Any]],
    *,
    empty_fieldnames: Sequence[str] = (),
) -> None:
    target = Path(path)
    if rows or not empty_fieldnames:
        v15dn.write_csv(target, rows)
        return
    with target.open("w", newline="", encoding="utf-8") as handle:
        csv.DictWriter(handle, fieldnames=list(empty_fieldnames)).writeheader()


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    if not rows:
        return ["No rows."]
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values: List[str] = []
        for field in fields:
            value = row.get(field, "")
            if isinstance(value, float):
                values.append(fmt(value))
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return lines


def load_placement_rows() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for raw in v15dq.load_placement_rows():
        seed = safe_int(raw.get("growth_seed"))
        if seed not in GROWTH_SEEDS:
            continue
        rows.append(
            {
                "source": "v15dq",
                "growth_seed": seed,
                "placement": safe_int(raw.get("placement")),
                "established_rate": safe_float(raw.get("established_rate")),
                "active_placement": safe_int(raw.get("active_placement")),
                "n_runs": safe_int(raw.get("n_runs")),
                "label_counts": str(raw.get("label_counts", "")),
            }
        )
    for source, path in (("v15dr", V15DR_PLACEMENT_CSV), ("v15ds", V15DS_PLACEMENT_CSV)):
        for raw in read_csv(path):
            seed = safe_int(raw.get("growth_seed"))
            if seed not in GROWTH_SEEDS:
                continue
            rows.append(
                {
                    "source": source,
                    "growth_seed": seed,
                    "placement": safe_int(raw.get("placement")),
                    "established_rate": safe_float(raw.get("established_rate")),
                    "active_placement": safe_int(raw.get("active_placement")),
                    "n_runs": safe_int(raw.get("n_runs")),
                    "label_counts": str(raw.get("label_counts", "")),
                }
            )
    rows.sort(key=lambda row: (safe_int(row["growth_seed"]), safe_int(row["placement"])))
    expected = {(seed, placement) for seed in GROWTH_SEEDS for placement in PLACEMENTS}
    observed = {(safe_int(row["growth_seed"]), safe_int(row["placement"])) for row in rows}
    if observed != expected or len(rows) != len(expected):
        missing = sorted(expected - observed)
        duplicates = len(rows) - len(observed)
        raise ValueError(f"placement input mismatch: missing={missing}; duplicate_count={duplicates}")
    return rows


def build_bases() -> Dict[int, Any]:
    regime = v10e.recommended_regime("fast_balanced")
    ensembles = v15.deep_ensembles([TARGET_NODES])
    base_states, _ = v10e.build_bases(ensembles, regime, list(GROWTH_SEEDS))
    return {seed: base_states[(ensembles[0].name, seed)] for seed in GROWTH_SEEDS}


def relabel_mapping(nodes: Sequence[int], seed: int) -> Dict[int, int]:
    source = sorted(int(node) for node in nodes)
    target = list(source)
    random.Random(seed).shuffle(target)
    return dict(zip(source, target))


def relabel_state(state: Any, mapping: Mapping[int, int]) -> Any:
    graph = v7.UGraph()
    for node in state.g.nodes():
        graph.add_node(mapping[int(node)])
    for a, b in state.g.edge_set():
        graph.add_edge(mapping[int(a)], mapping[int(b)])
    token_pos = {int(tid): mapping[int(node)] for tid, node in state.token_pos.items()}
    return v7.State(graph, token_pos, float(state.t))


def map_edge_set(edges: Iterable[Tuple[int, int]], mapping: Mapping[int, int]) -> set[Tuple[int, int]]:
    out: set[Tuple[int, int]] = set()
    for a, b in edges:
        ma = mapping[int(a)]
        mb = mapping[int(b)]
        out.add((ma, mb) if ma < mb else (mb, ma))
    return out


def map_descriptor(descriptor: Tuple[Any, ...], mapping: Mapping[int, int]) -> Tuple[Any, ...]:
    kind = str(descriptor[0])
    if kind in {"seed_node", "birth_node"}:
        return (descriptor[0], mapping[int(descriptor[1])])
    if kind in {"seed_tid", "birth_tid", "death_tid"}:
        return tuple(descriptor)
    if kind == "stuck":
        return (descriptor[0], descriptor[1], mapping[int(descriptor[2])])
    if kind in {"move", "delete"}:
        return (
            descriptor[0],
            descriptor[1],
            mapping[int(descriptor[2])],
            mapping[int(descriptor[3])],
        )
    if kind in {"triad", "swap"}:
        return (
            descriptor[0],
            descriptor[1],
            mapping[int(descriptor[2])],
            mapping[int(descriptor[3])],
            mapping[int(descriptor[4])],
        )
    raise ValueError(f"unknown descriptor kind {kind!r}")


def transported_distribution(
    distribution: Mapping[Tuple[Any, ...], float],
    mapping: Mapping[int, int],
) -> Dict[Tuple[Any, ...], float]:
    return {map_descriptor(descriptor, mapping): float(probability) for descriptor, probability in distribution.items()}


def distribution_max_error(left: Mapping[Any, float], right: Mapping[Any, float]) -> float:
    keys = set(left).union(right)
    return max((abs(float(left.get(key, 0.0)) - float(right.get(key, 0.0))) for key in keys), default=0.0)


def candidate_text(candidate: Tuple[int, int, int] | None) -> str:
    if candidate is None:
        return "none"
    return "-".join(str(int(node)) for node in candidate)


def relabel_trial_rows(base_states: Mapping[int, Any], params: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for growth_seed in GROWTH_SEEDS:
        base_state = base_states[growth_seed]
        for placement in PLACEMENTS:
            original_candidate = v08b.find_chord_candidate(base_state, center_token_index=placement)
            if original_candidate is None:
                raise ValueError(f"no add_chord candidate for growth_seed={growth_seed}, placement={placement}")
            original_post = base_state.clone()
            original_info = v08b.apply_local_chord_anywhere(original_post, center_token_index=placement)
            for relabel_seed in RELABEL_SEEDS:
                mapping = relabel_mapping(base_state.g.nodes(), growth_seed * 100_000 + placement * 1_000 + relabel_seed)
                relabelled = relabel_state(base_state, mapping)
                relabelled_candidate = v08b.find_chord_candidate(relabelled, center_token_index=placement)
                transported_candidate = tuple(mapping[int(node)] for node in original_candidate)
                relabelled_post = relabelled.clone()
                relabelled_info = v08b.apply_local_chord_anywhere(relabelled_post, center_token_index=placement)

                rate_original = v7.family_rates(base_state, params)
                rate_relabelled = v7.family_rates(relabelled, params)
                rate_max_error = max(abs(rate_original[key] - rate_relabelled[key]) for key in rate_original)
                kernel_errors: Dict[str, float] = {}
                for family in ("seed", "token", "birth", "death"):
                    original_kernel = v7.family_kernel(base_state, family, params)
                    relabelled_kernel = v7.family_kernel(relabelled, family, params)
                    transported = transported_distribution(original_kernel, mapping)
                    kernel_errors[family] = distribution_max_error(transported, relabelled_kernel)
                kernel_max_error = max(kernel_errors.values(), default=0.0)

                transported_post_edges = map_edge_set(original_post.g.edge_set(), mapping)
                post_graph_equivariant = int(transported_post_edges == relabelled_post.g.edge_set())
                transported_support = {mapping[int(node)] for node in original_info["support"]}
                support_equivariant = int(transported_support == {int(node) for node in relabelled_info["support"]})
                constructor_equivariant = int(tuple(relabelled_candidate or ()) == transported_candidate)
                rows.append(
                    {
                        "target_nodes": TARGET_NODES,
                        "growth_seed": growth_seed,
                        "placement": placement,
                        "relabel_seed": relabel_seed,
                        "original_candidate": candidate_text(original_candidate),
                        "transported_candidate": candidate_text(transported_candidate),
                        "relabelled_constructor_candidate": candidate_text(relabelled_candidate),
                        "family_rate_max_error": rate_max_error,
                        "seed_kernel_max_error": kernel_errors["seed"],
                        "token_kernel_max_error": kernel_errors["token"],
                        "birth_kernel_max_error": kernel_errors["birth"],
                        "death_kernel_max_error": kernel_errors["death"],
                        "kernel_max_error": kernel_max_error,
                        "transition_kernel_equivariant": int(rate_max_error <= KERNEL_TOLERANCE and kernel_max_error <= KERNEL_TOLERANCE),
                        "constructor_equivariant": constructor_equivariant,
                        "support_equivariant": support_equivariant,
                        "post_graph_equivariant": post_graph_equivariant,
                    }
                )
    return rows


def support_distances(graph: Any, support: Sequence[int], radius: int) -> Dict[int, int]:
    all_distances = v15dl.bfs_limited(graph, support, max_depth=radius)
    return {int(node): int(distance) for node, distance in all_distances.items() if int(distance) <= radius}


def marked_local_graph(base_state: Any, placement: int, radius: int, mode: str) -> Tuple[Any, Tuple[int, int, int]]:
    candidate = v08b.find_chord_candidate(base_state, center_token_index=placement)
    if candidate is None:
        raise ValueError(f"no candidate for placement {placement}")
    source, bridge, target = (int(node) for node in candidate)
    support = (source, bridge, target)
    distances = support_distances(base_state.g, support, radius)
    nodes = set(distances)
    token_counts = Counter(int(node) for node in base_state.token_pos.values())
    selected_tid = base_state.sorted_token_ids()[placement % len(base_state.sorted_token_ids())]
    selected_token_node = int(base_state.token_pos[selected_tid])

    graph = nx.Graph()
    for node in sorted(nodes):
        role = "ordinary"
        if node == source:
            role = "chord_source"
        elif node == bridge:
            role = "chord_bridge"
        elif node == target:
            role = "chord_target"
        internal_degree = sum(1 for neighbor in base_state.g.neighbors(node) if int(neighbor) in nodes)
        external_degree = base_state.g.degree(node) - internal_degree
        label_parts = [
            f"role={role}",
            f"distance={distances[node]}",
            f"token_count={token_counts.get(node, 0)}",
            f"selected_token={int(node == selected_token_node)}",
        ]
        if mode == "boundary_aware":
            label_parts.append(f"external_degree={external_degree}")
        graph.add_node(node, mark="|".join(label_parts))
    for a, b in base_state.g.edge_set():
        if int(a) in nodes and int(b) in nodes:
            graph.add_edge(int(a), int(b))
    return graph, (source, bridge, target)


def graph_hash(graph: Any) -> str:
    return nx.weisfeiler_lehman_graph_hash(graph, node_attr="mark", iterations=4)


def graph_isomorphic(left: Any, right: Any) -> bool:
    matcher = nx.algorithms.isomorphism.categorical_node_match("mark", "")
    return nx.is_isomorphic(left, right, node_match=matcher)


class UnionFind:
    def __init__(self, items: Iterable[str]) -> None:
        self.parent = {item: item for item in items}

    def find(self, item: str) -> str:
        parent = self.parent[item]
        if parent != item:
            self.parent[item] = self.find(parent)
        return self.parent[item]

    def union(self, left: str, right: str) -> None:
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left != root_right:
            self.parent[root_right] = root_left


def local_isomorphism_rows(
    base_states: Mapping[int, Any],
    placement_rows: Sequence[Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    outcome_by_key = {
        (safe_int(row["growth_seed"]), safe_int(row["placement"])): row
        for row in placement_rows
    }
    context_rows: List[Dict[str, Any]] = []
    graph_by_context: Dict[Tuple[str, int, str], Any] = {}
    for growth_seed in GROWTH_SEEDS:
        for placement in PLACEMENTS:
            outcome = outcome_by_key[(growth_seed, placement)]
            context_id = f"g{growth_seed}_p{placement}"
            for radius in LOCAL_RADII:
                for mode in LOCAL_MATCH_MODES:
                    graph, candidate = marked_local_graph(base_states[growth_seed], placement, radius, mode)
                    digest = graph_hash(graph)
                    graph_by_context[(context_id, radius, mode)] = graph
                    context_rows.append(
                        {
                            "context_id": context_id,
                            "source": outcome["source"],
                            "growth_seed": growth_seed,
                            "placement": placement,
                            "radius": radius,
                            "match_mode": mode,
                            "node_count": graph.number_of_nodes(),
                            "edge_count": graph.number_of_edges(),
                            "marked_graph_hash": digest,
                            "candidate": candidate_text(candidate),
                            "established_rate": safe_float(outcome["established_rate"]),
                            "active_placement": safe_int(outcome["active_placement"]),
                        }
                    )

    pair_rows: List[Dict[str, Any]] = []
    class_rows: List[Dict[str, Any]] = []
    for radius in LOCAL_RADII:
        for mode in LOCAL_MATCH_MODES:
            subset = [row for row in context_rows if row["radius"] == radius and row["match_mode"] == mode]
            by_hash: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
            for row in subset:
                by_hash[str(row["marked_graph_hash"])].append(row)
            union_find = UnionFind(str(row["context_id"]) for row in subset)
            for candidates in by_hash.values():
                if len(candidates) < 2:
                    continue
                for left, right in itertools.combinations(candidates, 2):
                    left_id = str(left["context_id"])
                    right_id = str(right["context_id"])
                    left_graph = graph_by_context[(left_id, radius, mode)]
                    right_graph = graph_by_context[(right_id, radius, mode)]
                    if not graph_isomorphic(left_graph, right_graph):
                        continue
                    union_find.union(left_id, right_id)
                    rate_left = safe_float(left["established_rate"])
                    rate_right = safe_float(right["established_rate"])
                    pair_rows.append(
                        {
                            "radius": radius,
                            "match_mode": mode,
                            "context_a": left_id,
                            "context_b": right_id,
                            "growth_seed_a": safe_int(left["growth_seed"]),
                            "growth_seed_b": safe_int(right["growth_seed"]),
                            "placement_a": safe_int(left["placement"]),
                            "placement_b": safe_int(right["placement"]),
                            "cross_seed": int(safe_int(left["growth_seed"]) != safe_int(right["growth_seed"])),
                            "cross_placement": int(safe_int(left["placement"]) != safe_int(right["placement"])),
                            "active_a": safe_int(left["active_placement"]),
                            "active_b": safe_int(right["active_placement"]),
                            "active_agreement": int(safe_int(left["active_placement"]) == safe_int(right["active_placement"])),
                            "established_rate_a": rate_left,
                            "established_rate_b": rate_right,
                            "absolute_rate_gap": abs(rate_left - rate_right),
                            "node_count": safe_int(left["node_count"]),
                            "edge_count": safe_int(left["edge_count"]),
                            "marked_graph_hash": left["marked_graph_hash"],
                        }
                    )
            classes: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
            for row in subset:
                classes[union_find.find(str(row["context_id"]))].append(row)
            repeated = [group for group in classes.values() if len(group) >= 2]
            for class_index, group in enumerate(sorted(repeated, key=lambda values: (-len(values), str(values[0]["context_id"]))), start=1):
                rates = [safe_float(row["established_rate"]) for row in group]
                actives = [safe_int(row["active_placement"]) for row in group]
                class_rows.append(
                    {
                        "radius": radius,
                        "match_mode": mode,
                        "equivalence_class": f"r{radius}_{mode}_{class_index}",
                        "n_contexts": len(group),
                        "n_growth_seeds": len({safe_int(row["growth_seed"]) for row in group}),
                        "n_placements": len({safe_int(row["placement"]) for row in group}),
                        "contexts": ";".join(str(row["context_id"]) for row in sorted(group, key=lambda value: str(value["context_id"]))),
                        "active_fraction": mean_defined(actives),
                        "established_rate_range": max(rates) - min(rates),
                        "response_constant": int(len(set(actives)) == 1),
                    }
                )
    return context_rows, pair_rows, class_rows


def exact_sign_flip_pvalue(differences: Sequence[float]) -> float:
    nonzero = [float(value) for value in differences if math.isfinite(float(value)) and abs(float(value)) > 1.0e-15]
    if not nonzero:
        return 1.0
    observed = abs(sum(nonzero) / len(nonzero))
    extreme = 0
    total = 1 << len(nonzero)
    for mask in range(total):
        signed_sum = 0.0
        for index, value in enumerate(nonzero):
            signed_sum += value if mask & (1 << index) else -value
        if abs(signed_sum / len(nonzero)) >= observed - 1.0e-15:
            extreme += 1
    return extreme / total


def placement_exchange_rows(placement_rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    by_seed: Dict[int, Dict[int, Mapping[str, Any]]] = defaultdict(dict)
    for row in placement_rows:
        by_seed[safe_int(row["growth_seed"])][safe_int(row["placement"])] = row
    out: List[Dict[str, Any]] = []
    for placement in PLACEMENTS:
        rows = [by_seed[seed][placement] for seed in GROWTH_SEEDS]
        out.append(
            {
                "comparison": f"p{placement}_marginal",
                "n_growth_seeds": len(rows),
                "mean_established_rate": mean_defined(row["established_rate"] for row in rows),
                "median_established_rate": median_defined(row["established_rate"] for row in rows),
                "active_seed_count": sum(safe_int(row["active_placement"]) for row in rows),
                "active_seed_fraction": mean_defined(row["active_placement"] for row in rows),
                "paired_active_agreement": "",
                "mean_signed_rate_difference": "",
                "median_absolute_rate_difference": "",
                "exact_sign_flip_pvalue": "",
            }
        )
    for left, right in itertools.combinations(PLACEMENTS, 2):
        left_rows = [by_seed[seed][left] for seed in GROWTH_SEEDS]
        right_rows = [by_seed[seed][right] for seed in GROWTH_SEEDS]
        differences = [safe_float(a["established_rate"]) - safe_float(b["established_rate"]) for a, b in zip(left_rows, right_rows)]
        agreements = [int(safe_int(a["active_placement"]) == safe_int(b["active_placement"])) for a, b in zip(left_rows, right_rows)]
        out.append(
            {
                "comparison": f"p{left}_minus_p{right}",
                "n_growth_seeds": len(differences),
                "mean_established_rate": "",
                "median_established_rate": "",
                "active_seed_count": "",
                "active_seed_fraction": "",
                "paired_active_agreement": mean_defined(agreements),
                "mean_signed_rate_difference": mean_defined(differences),
                "median_absolute_rate_difference": median_defined(abs(value) for value in differences),
                "exact_sign_flip_pvalue": exact_sign_flip_pvalue(differences),
            }
        )
    return out


def local_summary_rows(
    pair_rows: Sequence[Mapping[str, Any]],
    class_rows: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for radius in LOCAL_RADII:
        for mode in LOCAL_MATCH_MODES:
            pairs = [row for row in pair_rows if safe_int(row["radius"]) == radius and row["match_mode"] == mode]
            cross_seed = [row for row in pairs if safe_int(row["cross_seed"]) == 1]
            classes = [row for row in class_rows if safe_int(row["radius"]) == radius and row["match_mode"] == mode]
            out.append(
                {
                    "radius": radius,
                    "match_mode": mode,
                    "isomorphic_pair_count": len(pairs),
                    "cross_seed_isomorphic_pair_count": len(cross_seed),
                    "repeated_equivalence_class_count": len(classes),
                    "max_equivalence_class_size": max((safe_int(row["n_contexts"]) for row in classes), default=1),
                    "cross_seed_active_agreement": mean_defined(row["active_agreement"] for row in cross_seed),
                    "cross_seed_median_absolute_rate_gap": median_defined(row["absolute_rate_gap"] for row in cross_seed),
                }
            )
    return out


def evaluation_rows(
    relabel_rows: Sequence[Mapping[str, Any]],
    local_summary: Sequence[Mapping[str, Any]],
    placement_exchange: Sequence[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    kernel_pass_rate = mean_defined(row["transition_kernel_equivariant"] for row in relabel_rows)
    constructor_pass_rate = mean_defined(row["constructor_equivariant"] for row in relabel_rows)
    post_graph_pass_rate = mean_defined(row["post_graph_equivariant"] for row in relabel_rows)
    radius3_boundary = next(
        row
        for row in local_summary
        if safe_int(row["radius"]) == 3 and row["match_mode"] == "boundary_aware"
    )
    p0_p2 = next(row for row in placement_exchange if row["comparison"] == "p0_minus_p2")

    if kernel_pass_rate < 1.0:
        diagnosis = "transition_kernel_relabel_failure"
        next_step = "fix_transition_kernel_before_any_symmetry_holdout"
    elif constructor_pass_rate < 1.0:
        diagnosis = "kernel_equivariant_but_constructor_breaks_relabel_symmetry"
        next_step = "replace_constructor_with_distributionally_relabel_invariant_candidate_sampling"
    elif safe_int(radius3_boundary["cross_seed_isomorphic_pair_count"]) >= 3:
        diagnosis = "radius3_boundary_aware_local_witnesses_found"
        next_step = "pre_register_transported_local_quasi_equivalence_holdout"
    else:
        diagnosis = "relabel_gate_clean_but_no_radius3_local_witness"
        next_step = "do_not_spend_dynamic_budget_on_current_symmetry_observable"

    return [
        {
            "key": "scope",
            "value": "v15dq_plus_v15dr_plus_v15ds_no_new_dynamics",
            "evidence": f"growth_seeds={len(GROWTH_SEEDS)}; placements={len(PLACEMENTS)}; relabel_trials={len(relabel_rows)}",
        },
        {
            "key": "transition_kernel_relabel_equivariance",
            "value": fmt(kernel_pass_rate),
            "evidence": f"tolerance={KERNEL_TOLERANCE:.1e}",
        },
        {
            "key": "add_chord_constructor_relabel_equivariance",
            "value": fmt(constructor_pass_rate),
            "evidence": "transported candidate must equal candidate found after node relabel",
        },
        {
            "key": "post_perturbation_graph_relabel_equivariance",
            "value": fmt(post_graph_pass_rate),
            "evidence": "transported post-edge-set equality",
        },
        {
            "key": "radius3_boundary_aware_cross_seed_witnesses",
            "value": safe_int(radius3_boundary["cross_seed_isomorphic_pair_count"]),
            "evidence": f"active_agreement={fmt(radius3_boundary['cross_seed_active_agreement'])}; median_rate_gap={fmt(radius3_boundary['cross_seed_median_absolute_rate_gap'])}",
        },
        {
            "key": "p0_p2_exchange_audit",
            "value": fmt(p0_p2["exact_sign_flip_pvalue"]),
            "evidence": f"paired_active_agreement={fmt(p0_p2['paired_active_agreement'])}; mean_rate_difference={fmt(p0_p2['mean_signed_rate_difference'])}",
        },
        {
            "key": "diagnosis",
            "value": diagnosis,
            "evidence": "implementation gate precedes physical symmetry language",
        },
        {
            "key": "next_step",
            "value": next_step,
            "evidence": "no fresh dynamics unless representation and local-witness gates justify them",
        },
    ]


def advisor_claim_rows() -> List[Dict[str, Any]]:
    return [
        {
            "claim_id": "claim.v15du.nontrivial-response",
            "claim_type": "factual",
            "strength": "moderated",
            "statement": "The repo contains reproducible, nontrivial local add_chord response signals in a narrow target-1024 regime.",
            "status_before_v15du": "partly_supported",
            "counter_or_qualifier": "Damage and horizon are coupling-defined and remain seed, scale, and placement sensitive.",
        },
        {
            "claim_id": "claim.v15du.universe-like-law",
            "claim_type": "project_capability",
            "strength": "assertive",
            "statement": "The current model has demonstrated universe-like effective law structure.",
            "status_before_v15du": "contradicted",
            "counter_or_qualifier": "Lorentz, global invariants, universality, and predictive effective laws are not validated.",
        },
        {
            "claim_id": "claim.v15du.symmetry-next",
            "claim_type": "normative",
            "strength": "moderated",
            "statement": "A relabel and marked-local-isomorphism gate should precede another feature-level symmetry holdout.",
            "status_before_v15du": "supported",
            "counter_or_qualifier": "If the gate passes without local witnesses, symmetry is clean but not dynamically testable in this observable.",
        },
        {
            "claim_id": "claim.v15du.impossibility",
            "claim_type": "factual",
            "strength": "moderated",
            "statement": "Finite failed experiments cannot prove that no universe-like model exists in the broad starting idea.",
            "status_before_v15du": "supported",
            "counter_or_qualifier": "They can falsify a frozen selector, mechanism, rule class, or parameter-domain claim; a scoped no-go theorem could prove more.",
        },
    ]


def render_report(
    *,
    local_summary: Sequence[Mapping[str, Any]],
    placement_exchange: Sequence[Mapping[str, Any]],
    evaluation: Sequence[Mapping[str, Any]],
) -> str:
    eval_by_key = {str(row["key"]): row for row in evaluation}
    diagnosis = str(eval_by_key["diagnosis"]["value"])
    next_step = str(eval_by_key["next_step"]["value"])
    lines: List[str] = []
    lines.append("# Relasjonell universgraf v0.15du: relabel- og symmetrigate")
    lines.append("")
    lines.append("## Formaal og maal")
    lines.append("")
    lines.append("`purposeRef`: `purpose://prompt.unknown`.")
    lines.append("Candidate intake: undersoek om en minimal relasjonell rewrite-modell kan gi robuste univers-lignende effektive lover uten aa lese implementasjonsartefakter som fysikk.")
    lines.append("")
    lines.append("| goal | baseline | target | status | evidence |")
    lines.append("| --- | --- | --- | --- | --- |")
    lines.append("| G1: representation gate | node-id invarians var antatt, ikke direkte auditert | maal kernel og constructor separat | satisfied | v15du relabel trials |")
    lines.append("| G2: symmetry witness | tidligere near-symmetry var feature-avstand | krev eksakt markert lokal isomorfi | satisfied | radius 1-3 isomorphism audit |")
    lines.append("| G3: research decision | flere konkurrerende neste spor | velg stopp/go uten fabricated physics claim | satisfied | evaluation + panel adjudication |")
    lines.append("")
    lines.append("## Premissene som faktisk testes")
    lines.append("")
    lines.append("- Mikrotilstanden er en endelig, enkel, urettet graf med node-ID-er som representasjon, ikke fysisk koordinat.")
    lines.append("- Lokale stokastiske rewrite-hendelser er units of action; simulatorens tokens og placement-indekser er instrumentering og skal ikke automatisk leses som primitive partikler.")
    lines.append("- Tid, geometri, excitations og bevaringslover maa i prosjektets sterke program oppstaa som robuste makrobeskrivelser; de er ikke gitt av at koden kan kjoere.")
    lines.append("- En ommerking av node-ID-er skal ikke endre overgangssannsynlighetene. En perturbasjonskonstruktoer som velger etter numerisk nodeorden maa auditeres separat.")
    lines.append("")
    lines.append("## Evidensstige")
    lines.append("")
    lines.append("| level | hva som kan hevdes | minste evidenstype | dagens status |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 0 | modellen er matematisk og maskinelt definert | spesifikasjon + reproducerbar kode | oppfylt |")
    lines.append("| 1 | observabelen er fri for kjente representasjons-/generatorartefakter | relabel-, kontroll- og hygiene-gater | delvis; v15du avgjoer ny gate |")
    lines.append("| 2 | en ikke-triviell lokal respons finnes | matched controls og reproduserbare trajectories | avgrenset stotte |")
    lines.append("| 3 | responsen er robust | fresh growth seeds, skalaer, korrekte koblinger og alternative konstruktoerer | ikke oppfylt samlet |")
    lines.append("| 4 | en effektiv klasse/lov predikerer nytt | helt frossen analyse og minst to uavhengige holdout-blokker | ikke oppfylt |")
    lines.append("| 5 | en mekanisme er identifisert | preregistrerte inngrep/ablasjoner som endrer effekten | ikke oppfylt |")
    lines.append("| 6 | univers-lignende lovstruktur | samtidig lokalitet, symmetri, quasi-invariant/skala, stabile excitations og prediktiv coarse-graining | ikke oppfylt |")
    lines.append("| 7 | en mulig universbygger er konstruktivt vist | ett fullt spesifisert system som passerer level 1-6 robust | aapen |")
    lines.append("")
    lines.append("Ett konstruktivt system kan logisk vise mulighet, men bare dersom hele claim-bunten er demonstrert samtidig og artefaktfritt. Mange mislykkede kandidater kan avvise konkrete selectors, mekanismer og avgrensede regelklasser, men kan ikke bevise at den brede ideen er umulig. En sterk negativ konklusjon krever et no-go-teorem for en presist definert klasse eller uttommende analyse av et endelig rom.")
    lines.append("")
    lines.append("## Hvor mye evidens er nok")
    lines.append("")
    lines.append("- Tre fresh graph-witnesses er bare en kandidatgate for lokal quasi-ekvivalens, ikke endelig bevis.")
    lines.append("- Robusthetsclaims maa bruke growth seed som generaliseringsenhet, rapportere usikkerhet og effektstoerrelse, og overleve minst to frosne holdout-runder.")
    lines.append("- Skala- eller lovclaims maa vise samme dimensjonsloese relasjon over minst tre stoerrelser med en predefinert finite-size trend; et enkelt scale jump er ikke renormalisering.")
    lines.append("- Symmetri maa foerst ha en eksplisitt transformasjon og kernel-kovarians. Dynamisk quasi-symmetri maa deretter slaa matched ikke-isomorfe nullpar.")
    lines.append("- Lorentz-lignende språk krever placement-/mode-uavhengig propagasjon, isotropi og en stabil dispersjons-/frontlov; dagens repo er fortsatt `not_yet`.")
    lines.append("- En endelig run-mengde bestemmes med power/precision fra observert variasjon. Fast n alene er ikke bevisstandarden.")
    lines.append("")
    lines.append("## v15du design")
    lines.append("")
    lines.append(f"- target: `{TARGET_NODES}`")
    lines.append(f"- perturbation: `{PERTURBATION}`")
    lines.append(f"- growth seeds: `{';'.join(str(seed) for seed in GROWTH_SEEDS)}`")
    lines.append(f"- placements: `{';'.join(f'p{placement}' for placement in PLACEMENTS)}`")
    lines.append(f"- relabel seeds per context: `{';'.join(str(seed) for seed in RELABEL_SEEDS)}`")
    lines.append("- local witnesses: exact marked graph isomorphism at radius 1, 2, and 3, both without and with boundary-degree marks")
    lines.append("- existing dynamics only: v15dq + v15dr + v15ds placement outcomes; no new defect dynamics")
    lines.append("")
    lines.append("## Relabel-resultat")
    lines.append("")
    lines.extend(table(evaluation[1:4], ("key", "value", "evidence")))
    lines.append("")
    lines.append("Kernel-kovarians og constructor-kovarians er ulike evidenstyper. At kjernen passerer kan ikke reparere en constructor som velger en annen fysisk chord etter ren node-ommerking.")
    lines.append("")
    lines.append("## Markert lokal isomorfi")
    lines.append("")
    lines.extend(
        table(
            local_summary,
            (
                "radius",
                "match_mode",
                "isomorphic_pair_count",
                "cross_seed_isomorphic_pair_count",
                "repeated_equivalence_class_count",
                "max_equivalence_class_size",
                "cross_seed_active_agreement",
                "cross_seed_median_absolute_rate_gap",
            ),
        )
    )
    lines.append("")
    lines.append("En radius-1 match er bare en lokal kontur. Boundary-aware radius-3 isomorfi er sterkere, men er fortsatt ikke en global graph automorphism eller en fysisk symmetry group.")
    lines.append("")
    lines.append("## Placement-exchange audit")
    lines.append("")
    lines.extend(
        table(
            placement_exchange,
            (
                "comparison",
                "n_growth_seeds",
                "mean_established_rate",
                "active_seed_fraction",
                "paired_active_agreement",
                "mean_signed_rate_difference",
                "median_absolute_rate_difference",
                "exact_sign_flip_pvalue",
            ),
        )
    )
    lines.append("")
    lines.append("En hoy p-verdi er ikke bevis for exchange-symmetri. Tabellen er en sensitivitetsaudit av placement-labelene, ikke en fysisk invarianttest.")
    lines.append("")
    lines.append("## Raadgiverpanel og claim-adjudikasjon")
    lines.append("")
    lines.append("- Fysikk-/metodeskeptikeren krevde en eksplisitt relabel- eller marked-isomorphism witness foer symmetry-språk.")
    lines.append("- Emergens-steelman rangerte kernel/automorphism-gaten foran nye feature-avstander, deretter lokal quasi-konjugasjon, interaction og conditional quasi-invariants.")
    lines.append("- Evidensdommeren understreket at far-shell damage er coupling-definert, og at neste dynamiske hovedgate senere maa teste coupling-uavhengighet.")
    lines.append("- Panelet er ikke en avstemning. Enigheten brukes som argumentstruktur; reporesultatet avgjoer diagnosen.")
    lines.append("")
    lines.append("Root claim: `En symmetry-holdout er berettiget naa`.")
    lines.append("Composition: `allOf(kernel relabel covariance, constructor covariance, repeated marked local witnesses)` undercuttes dersom constructor eller witness-gaten feiler.")
    lines.append("")
    lines.append("## Eksterne metodeankere")
    lines.append("")
    lines.append("- Bombelli, Henson og Sorkin viser at diskrethet og Lorentz-symmetri har skarpe kompatibilitetskrav; saerlig kan ikke en endelig-valens graf hentes equivariant fra en Poisson-sprinkling. Dette er en guardrail, ikke evidens for repoet: https://arxiv.org/abs/gr-qc/0605006")
    lines.append("- Reversible Causal Graph Dynamics formaliserer shift-invariance, bounded-speed causality og reversibility som eksplisitte krav til grafdynamikk. Repoet har ikke automatisk disse egenskapene: https://arxiv.org/abs/1502.04368")
    lines.append("- Quantum Graphity viser at permutasjonsinvariant mikrofysikk og emergent lavdimensjonal geometri er en legitim modellklasse, men analogien overfoerer ingen resultater til denne generatoren: https://arxiv.org/abs/hep-th/0611197")
    lines.append("")
    lines.append("## Beslutning")
    lines.append("")
    lines.append(f"- diagnosis: `{diagnosis}`")
    lines.append(f"- next_step: `{next_step}`")
    lines.append("- claim ceiling: `implementation-level relabel covariance and/or local marked quasi-equivalence`, aldri fysisk symmetri fra denne runden alene")
    lines.append("")
    lines.append("## Aapne spor etter gaten")
    lines.append("")
    lines.append("1. Coupling-invariance: samme frozen marginal observables under maximal og rank coupling.")
    lines.append("2. Constructor/null: uniformly sampled relabel-invariant chord mot matched random chord og no-op.")
    lines.append("3. Conditional quasi-invariants: bare innen en holdout-validert dynamisk ekvivalensklasse.")
    lines.append("4. Ekte coarse-graining/RG: nestede beskrivelser av samme graf, ikke separate target-genereringer.")
    lines.append("5. Lorentz-/causal-spor: eksplisitt kernel-locality og mode/placement-independent frontlov.")
    lines.append("")
    return "\n".join(lines)


def render_operational(evaluation: Sequence[Mapping[str, Any]]) -> str:
    by_key = {str(row["key"]): row for row in evaluation}
    return "\n".join(
        [
            "# Operativ anbefaling v0.15du",
            "",
            f"- `transition_kernel_relabel_equivariance`: `{by_key['transition_kernel_relabel_equivariance']['value']}`.",
            f"- `add_chord_constructor_relabel_equivariance`: `{by_key['add_chord_constructor_relabel_equivariance']['value']}`.",
            f"- `radius3_boundary_aware_cross_seed_witnesses`: `{by_key['radius3_boundary_aware_cross_seed_witnesses']['value']}`.",
            f"- `diagnosis`: `{by_key['diagnosis']['value']}`.",
            f"- `next_step`: `{by_key['next_step']['value']}`.",
            "",
            "Ikke kall feature-naerhet eller lokal isomorfi fysisk symmetri uten en eksplisitt transformasjon, kernel-kovarians og fresh dynamisk holdout mot matched nullpar.",
            "Ikke bruk en constructor som bryter relabel-kovarians til aa trekke placement-fysikk uten separat artifact-kontroll.",
            "Neste senere fysikkgate er coupling-uavhengighet; den er ikke testet av v15du.",
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-report", default=str(DOC / "v15du_relabel_symmetry_gate.md"))
    parser.add_argument("--out-relabel-csv", default=str(DOC / "v15du_relabel_symmetry_trials.csv"))
    parser.add_argument("--out-context-csv", default=str(DOC / "v15du_marked_local_contexts.csv"))
    parser.add_argument("--out-pairs-csv", default=str(DOC / "v15du_marked_local_isomorphism_pairs.csv"))
    parser.add_argument("--out-classes-csv", default=str(DOC / "v15du_marked_local_equivalence_classes.csv"))
    parser.add_argument("--out-local-summary-csv", default=str(DOC / "v15du_marked_local_isomorphism_summary.csv"))
    parser.add_argument("--out-placement-csv", default=str(DOC / "v15du_placement_exchange_audit.csv"))
    parser.add_argument("--out-evaluation-csv", default=str(DOC / "v15du_symmetry_gate_evaluation.csv"))
    parser.add_argument("--out-advisor-csv", default=str(DOC / "v15du_advisor_claim_ledger.csv"))
    parser.add_argument("--out-operational", default=str(DOC / "v0_15du_operativ_anbefaling.md"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    placement_rows = load_placement_rows()
    base_states = build_bases()
    params = v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])

    relabel_rows = relabel_trial_rows(base_states, params)
    context_rows, pair_rows, class_rows = local_isomorphism_rows(base_states, placement_rows)
    local_summary = local_summary_rows(pair_rows, class_rows)
    placement_exchange = placement_exchange_rows(placement_rows)
    evaluation = evaluation_rows(relabel_rows, local_summary, placement_exchange)
    advisor_rows = advisor_claim_rows()

    write_csv(args.out_relabel_csv, relabel_rows)
    write_csv(args.out_context_csv, context_rows)
    write_csv(
        args.out_pairs_csv,
        pair_rows,
        empty_fieldnames=(
            "radius",
            "match_mode",
            "context_a",
            "context_b",
            "growth_seed_a",
            "growth_seed_b",
            "placement_a",
            "placement_b",
            "cross_seed",
            "cross_placement",
            "active_a",
            "active_b",
            "active_agreement",
            "established_rate_a",
            "established_rate_b",
            "absolute_rate_gap",
            "node_count",
            "edge_count",
            "marked_graph_hash",
        ),
    )
    write_csv(
        args.out_classes_csv,
        class_rows,
        empty_fieldnames=(
            "radius",
            "match_mode",
            "equivalence_class",
            "n_contexts",
            "n_growth_seeds",
            "n_placements",
            "contexts",
            "active_fraction",
            "established_rate_range",
            "response_constant",
        ),
    )
    write_csv(args.out_local_summary_csv, local_summary)
    write_csv(args.out_placement_csv, placement_exchange)
    write_csv(args.out_evaluation_csv, evaluation)
    write_csv(args.out_advisor_csv, advisor_rows)
    Path(args.out_report).write_text(
        render_report(
            local_summary=local_summary,
            placement_exchange=placement_exchange,
            evaluation=evaluation,
        ),
        encoding="utf-8",
    )
    Path(args.out_operational).write_text(render_operational(evaluation), encoding="utf-8")

    for row in evaluation:
        print(f"{row['key']}: {row['value']} ({row['evidence']})")


if __name__ == "__main__":
    main()
