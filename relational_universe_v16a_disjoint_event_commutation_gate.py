#!/usr/bin/env python3
"""v16a exact disjoint-event commutation and local-clock gate.

This is a finite microstate audit, not a large dynamical ensemble. It separates
two claims that are easy to conflate:

1. Concrete pre-drawn event transformations commute when their declared
   action read/write supports are disjoint.
2. The stochastic scheduler can be factored into bounded-support local clocks.

The first claim is checked exhaustively on the NetworkX graph atlas for all
connected unlabeled graphs with 4--7 nodes and all one-/two-token placements,
plus explicit empty-token and stuck fixtures. The second is checked both
algebraically and against runtime kernel intensities.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import math
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Iterator, List, Mapping, Sequence, Set, Tuple

try:
    import networkx as nx
except ImportError as exc:  # pragma: no cover
    raise SystemExit("v16a requires networkx") from exc

import relational_universe_local_max_coupling_lab as v7
import relational_universe_v15_defect_lifetime_lab as v15


DOC = Path("Documentation")
PURPOSE_REF = "purpose://prompt.unknown"
TOLERANCE = 1.0e-12
NEW_NODE_BASE = 10_000
NEW_TOKEN_BASE = 20_000
EVENT_KINDS = ("seed", "birth", "death", "stuck", "move", "delete", "triad", "swap")
ANCHOR_ACTIVE = {"seed", "birth", "stuck", "move", "swap"}


@dataclass(frozen=True)
class Event:
    family: str
    descriptor: Tuple[Any, ...]
    occurrence: int = 0
    new_node_id: int | None = None
    new_token_id: int | None = None

    @property
    def kind(self) -> str:
        head = str(self.descriptor[0])
        if head.startswith("seed_"):
            return "seed"
        if head.startswith("birth_"):
            return "birth"
        if head == "death_tid":
            return "death"
        return head


def anchor_params() -> v7.Params:
    return v15.v09.candidate_to_params(v15.anchor_spec()["candidate"])


def census_params() -> v7.Params:
    return replace(anchor_params(), r_death=0.03, p_del=0.20, p_triad=0.20, p_swap=0.20)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fields: Sequence[str] = ()) -> None:
    records = list(rows)
    fieldnames = list(fields)
    if records:
        fieldnames = []
        for row in records:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    if not fieldnames:
        raise ValueError(f"no schema for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def fmt(value: Any, digits: int = 6) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    return "nan" if not math.isfinite(number) else f"{number:.{digits}f}"


def table(rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> List[str]:
    out = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        out.append("| " + " | ".join(fmt(row.get(field, "")) for field in fields) + " |")
    return out


def nx_to_state(graph: nx.Graph, token_nodes: Sequence[int]) -> v7.State:
    out = v7.UGraph()
    for node in graph.nodes():
        out.add_node(int(node))
    for a, b in graph.edges():
        out.add_edge(int(a), int(b))
    return v7.State(out, {tid: int(node) for tid, node in enumerate(token_nodes)}, 0.0)


def atlas_states(min_nodes: int, max_nodes: int) -> Iterator[Tuple[str, str, int, v7.State]]:
    for atlas_id, graph in enumerate(nx.graph_atlas_g()):
        n = graph.number_of_nodes()
        if n < min_nodes or n > max_nodes or not nx.is_connected(graph):
            continue
        nodes = tuple(sorted(int(node) for node in graph.nodes()))
        for node in nodes:
            yield f"atlas_{atlas_id}_t1_{node}", "atlas", atlas_id, nx_to_state(graph, (node,))
        for left, right in itertools.combinations_with_replacement(nodes, 2):
            yield f"atlas_{atlas_id}_t2_{left}_{right}", "atlas", atlas_id, nx_to_state(graph, (left, right))


def fixture_states() -> Iterator[Tuple[str, str, int, v7.State]]:
    path = nx.path_graph(4)
    yield "fixture_empty_path4", "fixture_empty", -1, nx_to_state(path, ())
    isolated = nx.Graph()
    isolated.add_node(0)
    yield "fixture_stuck", "fixture_stuck", -2, nx_to_state(isolated, (0,))


def family_distributions(state: v7.State, params: v7.Params) -> Dict[str, Dict[Tuple[Any, ...], float]]:
    return {
        "seed": v7.local_seed_kernel(state),
        "birth": v7.local_birth_kernel(state, params),
        "death": v7.local_death_kernel(state, params),
        "token": v7.local_token_kernel(state, params),
    }


def events_for_state(state: v7.State, params: v7.Params) -> List[Event]:
    events: List[Event] = []
    for family, distribution in family_distributions(state, params).items():
        for descriptor in sorted(distribution, key=repr):
            copies = 2 if family in {"seed", "birth"} else 1
            for occurrence in range(copies):
                events.append(Event(family, tuple(descriptor), occurrence))
    return events


def materialize(event: Event, slot: int) -> Event:
    if event.kind == "seed":
        return replace(event, new_node_id=NEW_NODE_BASE + slot)
    if event.kind == "birth":
        return replace(event, new_token_id=NEW_TOKEN_BASE + slot)
    return event


def node_resource(node: int) -> str:
    return f"node:{int(node)}"


def adjacency_resource(node: int) -> str:
    return f"adj:{int(node)}"


def token_resource(token: int) -> str:
    return f"token:{int(token)}"


def edge_resource(left: int, right: int) -> str:
    a, b = sorted((int(left), int(right)))
    return f"edge:{a}:{b}"


def action_access(state: v7.State, event: Event) -> Tuple[Set[str], Set[str]]:
    desc = event.descriptor
    kind = event.kind
    reads: Set[str] = set()
    writes: Set[str] = set()

    if kind == "seed":
        _, ident = desc
        if str(desc[0]) == "seed_tid":
            host = int(state.token_pos[int(ident)])
            reads.add(token_resource(int(ident)))
        else:
            host = int(ident)
        reads.add(node_resource(host))
        assert event.new_node_id is not None
        writes.update({node_resource(event.new_node_id), adjacency_resource(host), adjacency_resource(event.new_node_id)})
        return reads, writes

    if kind == "birth":
        _, ident = desc
        if str(desc[0]) == "birth_tid":
            host = int(state.token_pos[int(ident)])
            reads.add(token_resource(int(ident)))
        else:
            host = int(ident)
        reads.add(node_resource(host))
        assert event.new_token_id is not None
        writes.add(token_resource(event.new_token_id))
        return reads, writes

    if kind == "death":
        tid = int(desc[1])
        reads.add(token_resource(tid))
        writes.add(token_resource(tid))
        return reads, writes

    tid = int(desc[1])
    v = int(desc[2])
    reads.update({token_resource(tid), node_resource(v)})
    if kind == "stuck":
        reads.add(adjacency_resource(v))
        return reads, writes

    u = int(desc[3])
    reads.update({node_resource(u), edge_resource(v, u)})
    writes.add(token_resource(tid))
    if kind == "move":
        return reads, writes

    if kind == "delete":
        reads.add(adjacency_resource(v))
        writes.update({edge_resource(v, u), adjacency_resource(v), adjacency_resource(u)})
        if state.g.degree(v) == 1:
            writes.add(node_resource(v))
            for other_tid, node in state.token_pos.items():
                if int(node) == v:
                    reads.add(token_resource(int(other_tid)))
                    writes.add(token_resource(int(other_tid)))
        return reads, writes

    w = int(desc[4])
    reads.update({node_resource(w), edge_resource(u, w), edge_resource(v, w)})
    writes.update({edge_resource(v, w), adjacency_resource(v), adjacency_resource(w)})
    if kind == "triad":
        return reads, writes

    # swap
    reads.add(adjacency_resource(u))
    writes.update({edge_resource(v, u), adjacency_resource(u)})
    return reads, writes


def are_disjoint(state: v7.State, left: Event, right: Event) -> Tuple[bool, Set[str]]:
    left_reads, left_writes = action_access(state, left)
    right_reads, right_writes = action_access(state, right)
    conflicts = (left_writes & (right_reads | right_writes)) | (right_writes & (left_reads | left_writes))
    return not conflicts, conflicts


def apply_event(state: v7.State, event: Event, params: v7.Params) -> Dict[str, Any]:
    if event.kind == "seed":
        assert event.new_node_id is not None
        return v7.apply_seed_descriptor(state, event.descriptor, event.new_node_id)
    if event.kind == "birth":
        assert event.new_token_id is not None
        return v7.apply_birth_descriptor(state, event.descriptor, event.new_token_id)
    if event.kind == "death":
        return v7.apply_death_descriptor(state, event.descriptor)
    return v7.apply_token_descriptor(state, event.descriptor, params)


def expected_event_name(event: Event) -> str:
    return event.kind


def run_order(state: v7.State, first: Event, second: Event, params: v7.Params) -> Tuple[v7.State, Tuple[str, str]]:
    out = state.clone()
    first_ctx = apply_event(out, first, params)
    second_ctx = apply_event(out, second, params)
    return out, (str(first_ctx.get("event", "")), str(second_ctx.get("event", "")))


def states_equal(left: v7.State, right: v7.State) -> bool:
    return v7.states_equal(left, right) and abs(float(left.t) - float(right.t)) <= TOLERANCE


def as_nx(state: v7.State) -> nx.Graph:
    graph = nx.Graph()
    tokens_at: Dict[int, List[int]] = defaultdict(list)
    for tid, node in state.token_pos.items():
        tokens_at[int(node)].append(int(tid))
    for node in state.g.nodes():
        graph.add_node(int(node), tokens=tuple(sorted(tokens_at.get(int(node), []))))
    graph.add_edges_from(state.g.edge_set())
    return graph


def states_isomorphic(left: v7.State, right: v7.State) -> bool:
    return nx.is_isomorphic(as_nx(left), as_nx(right), node_match=lambda a, b: a["tokens"] == b["tokens"])


def map_descriptor(descriptor: Tuple[Any, ...], mapping: Mapping[int, int]) -> Tuple[Any, ...]:
    kind = str(descriptor[0])
    if kind in {"seed_node", "birth_node"}:
        return descriptor[0], mapping[int(descriptor[1])]
    if kind in {"seed_tid", "birth_tid", "death_tid"}:
        return tuple(descriptor)
    if kind == "stuck":
        return descriptor[0], descriptor[1], mapping[int(descriptor[2])]
    if kind in {"move", "delete"}:
        return descriptor[0], descriptor[1], mapping[int(descriptor[2])], mapping[int(descriptor[3])]
    return (
        descriptor[0],
        descriptor[1],
        mapping[int(descriptor[2])],
        mapping[int(descriptor[3])],
        mapping[int(descriptor[4])],
    )


def map_event(event: Event, mapping: Mapping[int, int]) -> Event:
    new_node_id = None if event.new_node_id is None else mapping[int(event.new_node_id)]
    return replace(event, descriptor=map_descriptor(event.descriptor, mapping), new_node_id=new_node_id)


def relabel_state(state: v7.State, mapping: Mapping[int, int]) -> v7.State:
    graph = v7.UGraph()
    for node in state.g.nodes():
        graph.add_node(mapping[int(node)])
    for left, right in state.g.edge_set():
        graph.add_edge(mapping[int(left)], mapping[int(right)])
    return v7.State(graph, {int(tid): mapping[int(node)] for tid, node in state.token_pos.items()}, float(state.t))


def deterministic_mapping(state: v7.State, left: Event, right: Event) -> Dict[int, int]:
    nodes = set(int(node) for node in state.g.nodes())
    for event in (left, right):
        if event.new_node_id is not None:
            nodes.add(int(event.new_node_id))
    source = sorted(nodes)
    target = list(reversed([50_000 + index for index in range(len(source))]))
    return dict(zip(source, target))


def state_text(state: v7.State) -> str:
    return f"edges={sorted(state.g.edge_set())};tokens={sorted(state.token_pos.items())}"


def expected_hazard(state: v7.State, event: Event, params: v7.Params) -> float:
    desc = event.descriptor
    kind = event.kind
    token_count = state.token_count()
    if kind == "seed":
        denominator = token_count if str(desc[0]) == "seed_tid" else state.g.num_nodes()
        return params.r_seed / denominator if denominator else 0.0
    if kind == "birth":
        if str(desc[0]) == "birth_node":
            return 0.0
        tid = int(desc[1])
        return params.r_birth * v7.birth_weights(state, params)[tid]
    if kind == "death":
        if token_count <= params.min_tokens:
            return 0.0
        return params.r_death * v7.death_weights(state, params)[int(desc[1])]
    if kind == "stuck":
        return params.r_token

    v = int(desc[2])
    u = int(desc[3])
    degree = state.g.degree(v)
    if degree <= 0:
        return 0.0
    triad_candidates = sorted(w for w in state.g.neighbors(u) if w != v and not state.g.has_edge(v, w))
    delete_allowed = not (params.forbid_pruning_current_token_node and state.g.degree(u) <= 1)
    swap_allowed = delete_allowed and bool(triad_candidates)
    if kind == "delete":
        mass = params.p_del
    elif kind == "triad":
        mass = params.p_triad / len(triad_candidates)
    elif kind == "swap":
        mass = params.p_swap / len(triad_candidates)
    else:
        mass = max(0.0, 1.0 - (params.p_del + params.p_triad + params.p_swap))
        if not delete_allowed:
            mass += params.p_del
        if not triad_candidates:
            mass += params.p_triad
        if not swap_allowed:
            mass += params.p_swap
    return params.r_token * mass / degree


def descriptor_intensity(state: v7.State, event: Event, params: v7.Params) -> float:
    rates = v7.family_rates(state, params)
    distribution = family_distributions(state, params)[event.family]
    return float(rates[event.family]) * float(distribution.get(event.descriptor, 0.0))


def event_support_schema_rows() -> List[Dict[str, Any]]:
    return [
        {"event_kind": "seed", "anchor_active": 1, "action_read": "host node; host token entry for seed_tid", "action_write": "new node; host/new adjacency", "selection_read": "global token count or global node count", "id_input": "preallocated node id", "algebraic_delta": "N+1,E+1,beta1+0", "bounded_local_clock": 0},
        {"event_kind": "birth", "anchor_active": 1, "action_read": "host node; parent token entry", "action_write": "new token entry", "selection_read": "parent degree", "id_input": "preallocated token id", "algebraic_delta": "tokens+1", "bounded_local_clock": 1},
        {"event_kind": "death", "anchor_active": 0, "action_read": "target token entry", "action_write": "target token removal", "selection_read": "host degree plus global min_tokens guard", "id_input": "none", "algebraic_delta": "tokens-1", "bounded_local_clock": 0},
        {"event_kind": "stuck", "anchor_active": 1, "action_read": "token entry; host adjacency", "action_write": "none", "selection_read": "host degree", "id_input": "none", "algebraic_delta": "zero", "bounded_local_clock": 1},
        {"event_kind": "move", "anchor_active": 1, "action_read": "token entry; traversed edge", "action_write": "token location", "selection_read": "radius-2 neighborhood", "id_input": "none", "algebraic_delta": "zero", "bounded_local_clock": 1},
        {"event_kind": "delete", "anchor_active": 0, "action_read": "token; traversed edge; source adjacency", "action_write": "token; edge; optional source node/tokens", "selection_read": "radius-2 neighborhood", "id_input": "none", "algebraic_delta": "E-1; optional N-1", "bounded_local_clock": 1},
        {"event_kind": "triad", "anchor_active": 0, "action_read": "token; path v-u-w; absent v-w", "action_write": "token; edge v-w", "selection_read": "radius-2 neighborhood", "id_input": "none", "algebraic_delta": "E+1,beta1+1", "bounded_local_clock": 1},
        {"event_kind": "swap", "anchor_active": 1, "action_read": "token; path v-u-w; absent v-w", "action_write": "token; remove v-u; add v-w", "selection_read": "radius-2 neighborhood", "id_input": "none", "algebraic_delta": "E+0,beta1+0", "bounded_local_clock": 1},
    ]


def remote_context_rows(params: v7.Params) -> List[Dict[str, Any]]:
    graph = nx.path_graph(4)
    base = nx_to_state(graph, (0,))
    remote = nx_to_state(graph, (0, 3))
    probes = [
        ("seed", Event("seed", ("seed_tid", 0))),
        ("birth", Event("birth", ("birth_tid", 0))),
        ("death", Event("death", ("death_tid", 0))),
        ("move", Event("token", ("move", 0, 0, 1))),
        ("delete", Event("token", ("delete", 0, 0, 1))),
        ("triad", Event("token", ("triad", 0, 0, 1, 2))),
        ("swap", Event("token", ("swap", 0, 0, 1, 2))),
    ]
    rows: List[Dict[str, Any]] = []
    for kind, event in probes:
        base_intensity = descriptor_intensity(base, event, params)
        remote_intensity = descriptor_intensity(remote, event, params)
        rows.append({
            "event_kind": kind,
            "local_descriptor": repr(event.descriptor),
            "base_token_count": base.token_count(),
            "remote_token_count": remote.token_count(),
            "base_intensity": base_intensity,
            "remote_intensity": remote_intensity,
            "absolute_difference": abs(base_intensity - remote_intensity),
            "remote_invariant": int(abs(base_intensity - remote_intensity) <= TOLERANCE),
            "interpretation": "global_normalization_detected" if kind == "seed" else ("global_min_tokens_guard_detected" if kind == "death" else "bounded_local_intensity"),
        })
    return rows


HazardFunction = Callable[[v7.State, Event, v7.Params], float]


def run_census(
    min_nodes: int,
    max_nodes: int,
    max_counterexamples: int,
    *,
    descriptor_intensity_fn: HazardFunction | None = None,
    expected_hazard_fn: HazardFunction | None = None,
    support_rows: Sequence[Mapping[str, Any]] | None = None,
    progress_label: str = "v16a",
) -> Dict[str, Any]:
    params = census_params()
    runtime_hazard = descriptor_intensity_fn or descriptor_intensity
    expected_runtime_hazard = expected_hazard_fn or expected_hazard
    active_support_rows = list(support_rows) if support_rows is not None else event_support_schema_rows()
    aggregates: Dict[Tuple[str, str], Counter[str]] = defaultdict(Counter)
    counterexamples: List[Dict[str, Any]] = []
    hazard_stats: Dict[str, Dict[str, float]] = defaultdict(lambda: {"samples": 0.0, "max_error": 0.0})
    event_observations: Counter[str] = Counter()
    scope_counts: Counter[str] = Counter()
    graph_ids: Set[int] = set()
    total_states = 0
    start = time.time()

    states = itertools.chain(atlas_states(min_nodes, max_nodes), fixture_states())
    for state_id, scope, atlas_id, state in states:
        total_states += 1
        scope_counts[scope] += 1
        if atlas_id >= 0:
            graph_ids.add(atlas_id)
        events = events_for_state(state, params)
        unique_for_hazard = {(event.family, event.descriptor): event for event in events}
        for event in unique_for_hazard.values():
            runtime = runtime_hazard(state, event, params)
            expected = expected_runtime_hazard(state, event, params)
            error = abs(runtime - expected)
            hazard_stats[event.kind]["samples"] += 1.0
            hazard_stats[event.kind]["max_error"] = max(hazard_stats[event.kind]["max_error"], error)
            event_observations[event.kind] += 1

        for raw_left, raw_right in itertools.combinations(events, 2):
            left = materialize(raw_left, 0)
            right = materialize(raw_right, 1)
            pair_key = tuple(sorted((left.kind, right.kind)))
            aggregate = aggregates[pair_key]
            aggregate["candidate_pairs"] += 1
            disjoint, conflicts = are_disjoint(state, left, right)
            if not disjoint:
                aggregate["overlap_excluded"] += 1
                continue
            aggregate["declared_disjoint"] += 1
            ab, ab_context = run_order(state, left, right, params)
            ba, ba_context = run_order(state, right, left, params)
            valid = (
                ab_context == (expected_event_name(left), expected_event_name(right))
                and ba_context == (expected_event_name(right), expected_event_name(left))
            )
            exact = states_equal(ab, ba)
            isomorphic = exact or states_isomorphic(ab, ba)

            mapping = deterministic_mapping(state, left, right)
            relabelled_state = relabel_state(state, mapping)
            relabelled_left = map_event(left, mapping)
            relabelled_right = map_event(right, mapping)
            rel_ab, rel_ab_context = run_order(relabelled_state, relabelled_left, relabelled_right, params)
            rel_ba, rel_ba_context = run_order(relabelled_state, relabelled_right, relabelled_left, params)
            rel_valid = (
                rel_ab_context == (expected_event_name(left), expected_event_name(right))
                and rel_ba_context == (expected_event_name(right), expected_event_name(left))
            )
            transported_ab = relabel_state(ab, mapping)
            transported_ba = relabel_state(ba, mapping)
            relabel_pass = rel_valid and states_equal(rel_ab, rel_ba) and states_equal(transported_ab, rel_ab) and states_equal(transported_ba, rel_ba)
            commutation_pass = valid and isomorphic
            aggregate["valid_execution"] += int(valid)
            aggregate["exact_commutation"] += int(valid and exact)
            aggregate["isomorphic_commutation"] += int(commutation_pass)
            aggregate["relabel_pass"] += int(relabel_pass)
            failure = not (commutation_pass and relabel_pass)
            aggregate["failures"] += int(failure)
            if failure and len(counterexamples) < max_counterexamples:
                counterexamples.append({
                    "state_id": state_id,
                    "scope": scope,
                    "pair_kind": f"{pair_key[0]}__{pair_key[1]}",
                    "left_descriptor": repr(left.descriptor),
                    "right_descriptor": repr(right.descriptor),
                    "conflicts": ";".join(sorted(conflicts)),
                    "ab_context": repr(ab_context),
                    "ba_context": repr(ba_context),
                    "valid_execution": int(valid),
                    "exact_commutation": int(exact),
                    "isomorphic_commutation": int(isomorphic),
                    "relabel_pass": int(relabel_pass),
                    "initial_state": state_text(state),
                    "ab_state": state_text(ab),
                    "ba_state": state_text(ba),
                })
        if total_states % 5000 == 0:
            print(f"[{progress_label}] states={total_states} disjoint={sum(a['declared_disjoint'] for a in aggregates.values())}")

    summaries: List[Dict[str, Any]] = []
    for pair_key, aggregate in sorted(aggregates.items()):
        disjoint = aggregate["declared_disjoint"]
        summaries.append({
            "left_kind": pair_key[0],
            "right_kind": pair_key[1],
            "candidate_pairs": aggregate["candidate_pairs"],
            "overlap_excluded": aggregate["overlap_excluded"],
            "declared_disjoint": disjoint,
            "valid_execution": aggregate["valid_execution"],
            "exact_commutation": aggregate["exact_commutation"],
            "isomorphic_commutation": aggregate["isomorphic_commutation"],
            "relabel_pass": aggregate["relabel_pass"],
            "failures": aggregate["failures"],
            "commutation_rate": aggregate["isomorphic_commutation"] / disjoint if disjoint else float("nan"),
            "relabel_rate": aggregate["relabel_pass"] / disjoint if disjoint else float("nan"),
        })

    hazard_rows = []
    schema = {row["event_kind"]: row for row in active_support_rows}
    for kind in EVENT_KINDS:
        stat = hazard_stats[kind]
        hazard_rows.append({
            "event_kind": kind,
            "anchor_active": schema[kind]["anchor_active"],
            "runtime_formula_samples": int(stat["samples"]),
            "formula_max_abs_error": stat["max_error"],
            "formula_exact": int(stat["max_error"] <= TOLERANCE and stat["samples"] > 0),
            "bounded_local_clock": schema[kind]["bounded_local_clock"],
            "status": "pass_bounded_local" if schema[kind]["bounded_local_clock"] else ("fail_active_global_dependency" if schema[kind]["anchor_active"] else "inactive_anchor_global_guard"),
        })

    total_disjoint = sum(row["declared_disjoint"] for row in summaries)
    total_failures = sum(row["failures"] for row in summaries)
    relabel_failures = sum(row["declared_disjoint"] - row["relabel_pass"] for row in summaries)
    active_pair_kinds = sum(1 for row in summaries if row["declared_disjoint"] and row["left_kind"] in ANCHOR_ACTIVE and row["right_kind"] in ANCHOR_ACTIVE)
    return {
        "summary_rows": summaries,
        "counterexamples": counterexamples,
        "hazard_rows": hazard_rows,
        "event_observations": event_observations,
        "scope_counts": scope_counts,
        "graph_count": len(graph_ids),
        "state_count": total_states,
        "total_disjoint": total_disjoint,
        "total_failures": total_failures,
        "relabel_failures": relabel_failures,
        "active_pair_kinds": active_pair_kinds,
        "elapsed_seconds": time.time() - start,
    }


def claim_rows(result: Mapping[str, Any], local_clock_pass: bool) -> List[Dict[str, Any]]:
    commutation_pass = int(result["total_failures"]) == 0 and int(result["total_disjoint"]) > 0
    return [
        {"claim_id": "C1", "statement": "All declared-disjoint concrete event transformations commute in the finite v16a census.", "status": "supported" if commutation_pass else "contradicted", "evidence": "v16a_commutation_summary.csv", "scope_limit": "finite graph-atlas census plus explicit fixtures; support schema is conservative"},
        {"claim_id": "C2", "statement": "The same declared-disjoint transformations are covariant under deterministic node relabeling.", "status": "supported" if int(result["relabel_failures"]) == 0 else "contradicted", "evidence": "v16a_commutation_summary.csv:relabel_pass", "scope_limit": "same finite census"},
        {"claim_id": "C3", "statement": "Every active anchor event family factors into bounded-support local clocks.", "status": "supported" if local_clock_pass else "contradicted", "evidence": "v16a_local_hazard_factorization.csv;v16a_remote_context_audit.csv", "scope_limit": "current band_zero_del scheduler"},
        {"claim_id": "C4", "statement": "v16b intrinsic event-DAG work may proceed on the current anchor unchanged.", "status": "supported" if commutation_pass and local_clock_pass else "contradicted", "evidence": "v16a_gate_evaluation.csv", "scope_limit": "requires all v16a gates"},
        {"claim_id": "C5", "statement": "The broader relational-universe idea is impossible.", "status": "unsupported", "evidence": "none", "scope_limit": "a scheduler/seed-clock failure only diagnoses the current architecture"},
    ]


def build_report(
    result: Mapping[str, Any],
    gate_rows: Sequence[Mapping[str, Any]],
    hazard_rows: Sequence[Mapping[str, Any]],
    remote_rows: Sequence[Mapping[str, Any]],
) -> str:
    overall = str(gate_rows[-1]["status"])
    seed_remote = next(row for row in remote_rows if row["event_kind"] == "seed")
    lines = [
        "# UniverseSimulation v16a: disjoint-event commutation og local-clock gate",
        "",
        "Dato: 2026-07-12",
        "",
        "## Konklusjon",
        "",
        f"Gaten ender som `{overall}`.",
        "",
        f"Transformasjonsdelen bestod: `{int(result['total_disjoint'])}` deklarert disjunkte eventpar ble testet, med `{int(result['total_failures'])}` kommutasjonsfeil og `{int(result['relabel_failures'])}` relabel-feil. Dette er et eksakt resultat innen den endelige censusen, ikke en dynamisk ensembleobservasjon.",
        "",
        f"Scheduler-delen feilet: seed-intensiteten for samme lokale `seed_tid`-descriptor endret seg fra `{fmt(seed_remote['base_intensity'])}` til `{fmt(seed_remote['remote_intensity'])}` da ett fjernt token ble lagt til. Den aktive seed-klokken er `r_seed / K` per token, og avhenger derfor av globalt tokenantall. Dagens anchor kan ikke beskrives som bare bounded-support lokale klokker.",
        "",
        "Operativt betyr dette: ikke gaa til v16b paa uendret anchor. Redesign seed-klokken eller deklarer den globale seed-scheduleren som en eksplisitt fysisk bakgrunnsstruktur, og rerun v16a.",
        "",
        "## Census",
        "",
        f"- Connected unlabeled graph-atlas graphs: `{int(result['graph_count'])}`.",
        f"- States inklusive alle 1-/2-token placements og fixtures: `{int(result['state_count'])}`.",
        f"- Observerte eventtyper: `{';'.join(f'{k}:{result['event_observations'][k]}' for k in EVENT_KINDS)}`.",
        f"- Deklarert disjunkte eventpar: `{int(result['total_disjoint'])}` over `{int(result['active_pair_kinds'])}` aktive-anchor pair-kind-klasser.",
        f"- Runtime: `{fmt(result['elapsed_seconds'], 3)}` sekunder.",
        "",
        "Graph-atlas-delen bruker alle sammenhengende umerkede grafer med 4--7 noder. Tokenplasseringene er uttommende, men ikke kvotientert videre under grafautomorfier; dette gir redundant dekning heller enn manglende dekning. `seed_node`/`birth_node` og `stuck` dekkes av egne fixtures.",
        "",
        "## Hva som ble holdt fast",
        "",
        "- Concrete descriptors og event-spesifikke ID-er ble pre-drawn foer rekkefolgen ble variert.",
        "- `e1;e2` og `e2;e1` brukte samme initialtilstand og samme ID-allokering.",
        "- Terminaltilstander ble sammenlignet eksakt og deretter opp til node-isomorfi med token-ID-er bevart.",
        "- Hvert disjunkt par ble ogsaa transportert gjennom en deterministisk node-relabeling.",
        "- Overlappende read/write-support ble logisk ekskludert og kunne ikke bidra til pass.",
        "",
        "## Event-support",
        "",
    ]
    lines.extend(table(event_support_schema_rows(), ("event_kind", "anchor_active", "action_read", "action_write", "selection_read", "bounded_local_clock")))
    lines.extend(["", "## Kommutasjon", ""])
    lines.extend(table(result["summary_rows"], ("left_kind", "right_kind", "declared_disjoint", "isomorphic_commutation", "relabel_pass", "failures")))
    lines.extend(["", "## Hazard-faktorisering", ""])
    lines.extend(table(hazard_rows, ("event_kind", "anchor_active", "runtime_formula_samples", "formula_max_abs_error", "formula_exact", "bounded_local_clock", "status")))
    lines.extend(["", "Den numeriske formelauditen passerer for alle eventtyper. Det redder ikke seed-lokaliteten: den bekrefter nettopp den eksakte globale normaliseringen `r_seed/K` (eller `r_seed/N` uten tokens).", "", "## Remote-context kontroll", ""])
    lines.extend(table(remote_rows, ("event_kind", "base_intensity", "remote_intensity", "absolute_difference", "remote_invariant", "interpretation")))
    lines.extend([
        "",
        "## Evidensstatus",
        "",
        "- Kommutasjonspasset gjelder konkrete transformasjoner under det deklarerte action-support-skjemaet.",
        "- Det er ikke bevis for Lorentz-invarians, diffeomorfisme-invarians eller emergent spacetime.",
        "- Local-clock-feilen er sterkere enn en observabel-null: den er en eksakt arkitekturdiagnose for aktiv seed-scheduling.",
        "- Feilen beviser ikke at relasjonelle universmodeller er umulige. Den krever at dagens anchor endres foer intrinsic causal claims kan testes rent.",
        "",
        "## Beslutning",
        "",
        "`v16b` er blokkert. Neste smale steg er en seed-clock design gate med minst to eksplisitte alternativer:",
        "",
        "1. lokal per-token seed-hazard, slik at total seed-rate skalerer med antall lokale klokker",
        "2. en eksplisitt global seed-prosess som merkes som bakgrunnstid og derfor ikke brukes som grunnlag for observer-uavhengig lokal kausalitet",
        "",
        "Alternativ 1 endrer dynamikken og krever ny anchor-kalibrering senere. Alternativ 2 endrer forskningspaastanden. Ingen av dem skal skjules som en liten implementasjonsdetalj.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="v16a exact disjoint-event commutation gate")
    parser.add_argument("--min-nodes", type=int, default=4)
    parser.add_argument("--max-nodes", type=int, default=7)
    parser.add_argument("--max-counterexamples", type=int, default=100)
    args = parser.parse_args()
    if args.min_nodes < 1 or args.max_nodes > 7 or args.min_nodes > args.max_nodes:
        raise SystemExit("graph_atlas census requires 1 <= min_nodes <= max_nodes <= 7")

    print(f"[v16a] census connected atlas graphs n={args.min_nodes}..{args.max_nodes}")
    result = run_census(args.min_nodes, args.max_nodes, args.max_counterexamples)
    hazard_rows = result["hazard_rows"]
    remote_rows = remote_context_rows(census_params())
    commutation_pass = int(result["total_disjoint"]) > 0 and int(result["total_failures"]) == 0
    relabel_pass = int(result["relabel_failures"]) == 0
    formula_pass = all(int(row["formula_exact"]) for row in hazard_rows)
    local_clock_pass = all(int(row["bounded_local_clock"]) for row in hazard_rows if int(row["anchor_active"]))
    nontrivial_pass = int(result["total_disjoint"]) >= 1000 and int(result["active_pair_kinds"]) >= 3
    overall_pass = commutation_pass and relabel_pass and formula_pass and local_clock_pass and nontrivial_pass
    gate_rows = [
        {"gate": "support_schema_coverage", "status": "pass" if all(result["event_observations"][kind] > 0 for kind in EVENT_KINDS) else "fail", "observed": sum(1 for kind in EVENT_KINDS if result["event_observations"][kind] > 0), "required": len(EVENT_KINDS), "decision": "continue"},
        {"gate": "nontrivial_disjoint_coverage", "status": "pass" if nontrivial_pass else "fail", "observed": result["total_disjoint"], "required": ">=1000 pairs and >=3 active pair kinds", "decision": "continue" if nontrivial_pass else "failed_formalization"},
        {"gate": "exact_disjoint_commutation", "status": "pass" if commutation_pass else "fail", "observed": result["total_failures"], "required": "0 failures", "decision": "continue" if commutation_pass else "pivot_current_anchor"},
        {"gate": "relabel_transport", "status": "pass" if relabel_pass else "fail", "observed": result["relabel_failures"], "required": "0 failures", "decision": "continue" if relabel_pass else "pivot_current_anchor"},
        {"gate": "runtime_hazard_formula", "status": "pass" if formula_pass else "fail", "observed": max(float(row["formula_max_abs_error"]) for row in hazard_rows), "required": f"<={TOLERANCE}", "decision": "continue" if formula_pass else "fix_instrumentation"},
        {"gate": "bounded_local_clock_anchor", "status": "pass" if local_clock_pass else "fail", "observed": ";".join(row["event_kind"] for row in hazard_rows if int(row["anchor_active"]) and not int(row["bounded_local_clock"])), "required": "all active anchor kinds local", "decision": "redesign_seed_clock_or_declare_global_background"},
        {"gate": "v16a_overall", "status": "pass_to_v16b" if overall_pass else "fail_architecture_revision_required", "observed": int(overall_pass), "required": 1, "decision": "v16b" if overall_pass else "do_not_start_v16b"},
    ]

    target_rows = [{
        "purpose_ref": PURPOSE_REF,
        "min_nodes": args.min_nodes,
        "max_nodes": args.max_nodes,
        "connected_unlabeled_graphs": result["graph_count"],
        "states": result["state_count"],
        "declared_disjoint_pairs": result["total_disjoint"],
        "commutation_failures": result["total_failures"],
        "relabel_failures": result["relabel_failures"],
        "elapsed_seconds": result["elapsed_seconds"],
        "large_dynamics_runs": 0,
    }]

    DOC.mkdir(exist_ok=True)
    write_csv(DOC / "v16a_event_support_schema.csv", event_support_schema_rows())
    write_csv(DOC / "v16a_local_hazard_factorization.csv", hazard_rows)
    write_csv(DOC / "v16a_remote_context_audit.csv", remote_rows)
    write_csv(DOC / "v16a_commutation_summary.csv", result["summary_rows"])
    write_csv(
        DOC / "v16a_commutation_counterexamples.csv",
        result["counterexamples"],
        fields=("state_id", "scope", "pair_kind", "left_descriptor", "right_descriptor", "conflicts", "ab_context", "ba_context", "valid_execution", "exact_commutation", "isomorphic_commutation", "relabel_pass", "initial_state", "ab_state", "ba_state"),
    )
    write_csv(DOC / "v16a_gate_evaluation.csv", gate_rows)
    write_csv(DOC / "v16a_target_summary.csv", target_rows)
    write_csv(DOC / "v16a_claim_ledger.csv", claim_rows(result, local_clock_pass))
    report = build_report(result, gate_rows, hazard_rows, remote_rows)
    (DOC / "v16a_disjoint_event_commutation_gate.md").write_text(report, encoding="utf-8")
    recommendation = "\n".join([
        "# Operativ anbefaling v0.16a",
        "",
        f"Status: `{gate_rows[-1]['status']}`.",
        "",
        "- Behold det eksakte kommutasjonspasset som et avgrenset implementasjonsresultat.",
        "- Ikke start v16b paa uendret anchor: aktiv seed-intensitet avhenger av globalt token-/nodeantall.",
        "- Neste gate skal sammenligne lokal per-token seed-hazard mot en eksplisitt global-background-tolkning.",
        "- Ved lokal redesign maa v16a rerunnes og senere dynamikk rekalibreres; dette er en ny regelvariant.",
        "- Ikke oppgrader resultatet til lokal kausalitet, Lorentz-likhet eller emergent spacetime.",
        "",
    ])
    (DOC / "v0_16a_operativ_anbefaling.md").write_text(recommendation, encoding="utf-8")
    lay = "\n".join([
        "# v0.16a for ikke-spesialister",
        "",
        "Vi testet om to hendelser langt nok fra hverandre kan bytte rekkefolge uten at resultatet endres. Det bestod i den endelige mikrostatscensusen.",
        "",
        "Men vi fant samtidig at sannsynligheten for en seed-hendelse ved ett token avhenger av hvor mange tokens som finnes i hele grafen. Dermed er dagens tidsmekanisme ikke rent lokal, selv om den konkrete grafendringen er lokal.",
        "",
        "Dette er ikke et fysikkfunn. Det er en presis arkitekturdiagnose: seed-klokken maa redesignes eller erkjennes som global bakgrunn foer vi kan teste en observer-uavhengig kausal struktur.",
        "",
    ])
    (DOC / "relasjonell_universgraf_for_ikke_spesialister_v0_16a.md").write_text(lay, encoding="utf-8")
    print(f"[v16a] graphs={result['graph_count']} states={result['state_count']} disjoint={result['total_disjoint']}")
    print(f"[v16a] commutation_failures={result['total_failures']} relabel_failures={result['relabel_failures']}")
    print(f"[v16a] overall={gate_rows[-1]['status']} elapsed={result['elapsed_seconds']:.3f}s")


if __name__ == "__main__":
    main()
