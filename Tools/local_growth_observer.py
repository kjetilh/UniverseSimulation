"""UC3 graph-only observation of coarse growth/decomposition with replacement.

This observer follows the current connected component of each persistent unit;
it never pools disconnected components into one apparent organism. Unit list
positions are observer identities, not graph attributes. Snapshot history,
node names, counters and computed core membership do not feed the dynamics.
The endpoint describes two repeated coarse periods, not exact graph recurrence,
self-maintenance, life, or a physical invariant. Legal reference histories and
candidate interpretation remain the caller's responsibility.
"""
from __future__ import annotations

from collections import deque
import math


def _integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _components(adjacency: dict[int, set[int]]) -> list[set[int]]:
    remaining = set(adjacency)
    components = []
    while remaining:
        start = min(remaining)
        remaining.remove(start)
        component, stack = {start}, [start]
        while stack:
            for neighbor in adjacency[stack.pop()]:
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    component.add(neighbor)
                    stack.append(neighbor)
        components.append(component)
    return components


def _region(adjacency: dict[int, set[int]], nodes: set[int]) -> dict:
    degrees = {node: len(adjacency[node]) for node in nodes}
    queue = deque(sorted(node for node, degree in degrees.items() if degree < 2))
    core = set(nodes)
    while queue:
        node = queue.popleft()
        if node not in core:
            continue
        core.remove(node)
        for neighbor in adjacency[node]:
            if neighbor in core:
                degrees[neighbor] -= 1
                if degrees[neighbor] < 2:
                    queue.append(neighbor)
    edges = sorted((node, neighbor) for node in nodes
                   for neighbor in adjacency[node] if node < neighbor)
    core_edges = [edge for edge in edges if edge[0] in core and edge[1] in core]
    count, edge_count = len(nodes), len(edges)
    beta = edge_count - count + 1
    return {"nodes": sorted(nodes), "edges": [list(edge) for edge in edges],
            "core_nodes": sorted(core), "core_edges": [list(edge) for edge in core_edges],
            "N": count, "E": edge_count, "beta": beta,
            "core_fraction": len(core) / count,
            "beta_per_edge": beta / edge_count if edge_count else 0.0}


def _counters(tick: object, attempt: object) -> None:
    if (not _integer(tick) or not _integer(attempt)
            or tick < 0 or attempt < tick):
        raise ValueError("tick and attempt must be nonnegative integers with tick <= attempt")


def snapshot(state: object) -> dict:
    """Return JSON-ready observation without mutation or random draws.

    The state supplies adjacency (integer -> neighbor set), units (persistent
    positions in list order), ticks and attempts. No kernel import is needed.
    Global N/E/C/beta are diagnostic; endpoint gates use unit regions only.
    """
    try:
        adjacency, units = state.adjacency, state.units
        tick, attempt = state.ticks, state.attempts
    except AttributeError as exc:
        raise ValueError("state must provide adjacency, units, ticks and attempts") from exc
    _counters(tick, attempt)
    if not isinstance(adjacency, dict):
        raise ValueError("adjacency must be a dictionary")
    for node, neighbors in adjacency.items():
        if not _integer(node) or not isinstance(neighbors, (set, frozenset)):
            raise ValueError("nodes must be integers with neighbor sets")
        for neighbor in neighbors:
            if (not _integer(neighbor) or neighbor == node or neighbor not in adjacency
                    or not isinstance(adjacency[neighbor], (set, frozenset))
                    or node not in adjacency[neighbor]):
                raise ValueError("adjacency must describe a simple undirected graph")
    if not isinstance(units, list) or any(not _integer(node) or node not in adjacency for node in units):
        raise ValueError("every persistent unit must occupy an existing node")
    components = _components(adjacency)
    component_of = {node: index for index, nodes in enumerate(components) for node in nodes}
    cache = {}
    regions = []
    for unit_index, host in enumerate(units):
        component_index = component_of[host]
        if component_index not in cache:
            cache[component_index] = _region(adjacency, components[component_index])
        region = cache[component_index]
        # Fresh containers keep callers from changing another unit's observation.
        regions.append({**region, "unit_index": unit_index,
                        "nodes": list(region["nodes"]), "core_nodes": list(region["core_nodes"]),
                        "edges": [list(edge) for edge in region["edges"]],
                        "core_edges": [list(edge) for edge in region["core_edges"]]})
    count = len(adjacency)
    edge_count = sum(len(neighbors) for neighbors in adjacency.values()) // 2
    return {"tick": tick, "attempt": attempt, "N": count, "E": edge_count,
            "C": len(components), "beta": edge_count - count + len(components), "regions": regions}


def balanced_replacement(old: set, new: set) -> float:
    """Two-sided replacement: additions without departures score zero."""
    return min(len(old - new), len(new - old)) / max(1, len(old), len(new))


def _validate_region(region: object, index: int) -> tuple[set, set]:
    fields = {"unit_index", "nodes", "edges", "core_nodes", "core_edges", "N", "E", "beta",
              "core_fraction", "beta_per_edge"}
    if not isinstance(region, dict) or set(region) != fields or region["unit_index"] != index:
        raise ValueError("regions must contain the declared fields in persistent unit order")
    nodes = region["nodes"]
    if (not isinstance(nodes, list) or not nodes or any(not _integer(node) for node in nodes)
            or nodes != sorted(set(nodes))):
        raise ValueError("region nodes must be a nonempty sorted list of unique integer names")
    adjacency = {node: set() for node in nodes}
    if not isinstance(region["edges"], list):
        raise ValueError("region edges must be a list")
    for edge in region["edges"]:
        if (not isinstance(edge, list) or len(edge) != 2
                or any(not _integer(node) or node not in adjacency for node in edge)
                or edge[0] >= edge[1] or edge[1] in adjacency[edge[0]]):
            raise ValueError("region edges must be unique sorted-endpoint undirected edges")
        a, b = edge
        adjacency[a].add(b)
        adjacency[b].add(a)
    if len(_components(adjacency)) != 1:
        raise ValueError("a unit region must be a single connected component")
    expected = _region(adjacency, set(nodes))
    if any(region[key] != value for key, value in expected.items()):
        raise ValueError("region fields must agree with the observed graph and its 2-core")
    if any(not _integer(region[key]) for key in ("unit_index", "N", "E", "beta")):
        raise ValueError("region counts and unit indices must be integers")
    return set(region["core_nodes"]), {tuple(edge) for edge in region["core_edges"]}


def _validate_frames(frames: list[dict]) -> list[list[tuple[set, set]]]:
    if not isinstance(frames, list) or not frames:
        raise ValueError("frames must be a nonempty list")
    unit_count = None
    previous_tick = previous_attempt = -1
    spacing = None
    sets = []
    for frame in frames:
        if not isinstance(frame, dict) or set(frame) != {"tick", "attempt", "N", "E", "C", "beta", "regions"}:
            raise ValueError("frame fields must match snapshot output")
        _counters(frame["tick"], frame["attempt"])
        if frame["tick"] <= previous_tick or frame["attempt"] <= previous_attempt:
            raise ValueError("frame ticks and attempts must strictly increase")
        if previous_tick >= 0:
            difference = frame["tick"] - previous_tick
            if spacing is not None and difference != spacing:
                raise ValueError("frame ticks must have equal caller-chosen exposure spacing")
            spacing = difference
        previous_tick, previous_attempt = frame["tick"], frame["attempt"]
        if any(not _integer(frame[key]) or frame[key] < 0 for key in ("N", "E", "C", "beta")):
            raise ValueError("global graph counts must be nonnegative integers")
        if frame["beta"] != frame["E"] - frame["N"] + frame["C"] or frame["C"] > frame["N"]:
            raise ValueError("global cycle rank and component counts are inconsistent")
        if (frame["N"] == 0 and (frame["E"] != 0 or frame["C"] != 0)
                or frame["N"] > 0 and frame["C"] == 0
                or frame["E"] > frame["N"] * (frame["N"] - 1) // 2):
            raise ValueError("global graph counts are impossible for a simple graph")
        if not isinstance(frame["regions"], list):
            raise ValueError("regions must be a list")
        if unit_count is not None and len(frame["regions"]) != unit_count:
            raise ValueError("persistent unit count must remain constant")
        unit_count = len(frame["regions"])
        frame_sets = []
        observed_nodes, observed_edges, observed_components = set(), set(), []
        component_edges = {}
        for index, region in enumerate(frame["regions"]):
            frame_sets.append(_validate_region(region, index))
            nodes = set(region["nodes"])
            for prior in observed_components:
                if nodes & prior and nodes != prior:
                    raise ValueError("unit components must be identical or disjoint within a frame")
            if nodes not in observed_components:
                observed_components.append(nodes)
            node_key = frozenset(nodes)
            edge_key = frozenset(tuple(edge) for edge in region["edges"])
            if node_key in component_edges and component_edges[node_key] != edge_key:
                raise ValueError("shared unit components must have identical edge sets")
            component_edges[node_key] = edge_key
            observed_nodes.update(nodes)
            observed_edges.update(tuple(edge) for edge in region["edges"])
        if (len(observed_nodes) > frame["N"] or len(observed_edges) > frame["E"]
                or len(observed_components) > frame["C"]):
            raise ValueError("unit components exceed global graph counts")
        sets.append(frame_sets)
    return sets


def evaluate(frames: list[dict], lag: int = 8, min_nodes: int = 16,
             min_core_nodes: int = 4, size_tolerance: float = 0.10,
             shape_tolerance: float = 0.05, excursion_ratio: float = 1.5,
             turnover_min: float = 0.25) -> dict:
    """Measure fixed-lag coarse recurrence within each persistent unit's region.

    Callers supply equally spaced snapshots on an explicitly declared exposure
    clock. UC3 uses each persistent unit's current-component edit exposure, so
    later edits to disconnected fragments do not advance its clock. This module
    can check spacing, not the causal relevance of edits: the runner must audit
    that mapping. No sampling, smoothing, best-lag search, RNG, or dynamics
    occurs here. A window contains 2*lag+1 frames. Its two inclusive periods
    must match in relative size and
    coarse topology, each grow/decompose by the declared max/min ratio, and
    replace core nodes and edges between corresponding period endpoints.

    The primary is the mean of unit-wise qualifying/possible fractions. Units
    sharing a component are intentionally separate observer tracks, not
    statistically independent replicates. Empty/short exposure is explicit.
    """
    for name, value in (("lag", lag), ("min_nodes", min_nodes), ("min_core_nodes", min_core_nodes)):
        if not _integer(value) or value <= 0:
            raise ValueError(f"{name} must be a positive integer")
    for name, value in (("size_tolerance", size_tolerance), ("shape_tolerance", shape_tolerance),
                        ("excursion_ratio", excursion_ratio), ("turnover_min", turnover_min)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{name} must be a finite number")
        if (name == "excursion_ratio" and value < 1) or (name != "excursion_ratio" and not 0 <= value <= 1):
            raise ValueError(f"{name} is outside its allowed range")
    sets = _validate_frames(frames)
    units = len(frames[0]["regions"])
    possible = max(0, len(frames) - 2 * lag)
    intervals, per_unit = [], []
    for unit in range(units):
        regions = [frame["regions"][unit] for frame in frames]
        node_turnover = [balanced_replacement(sets[start][unit][0], sets[start + lag][unit][0])
                         for start in range(max(0, len(frames) - lag))]
        edge_turnover = [balanced_replacement(sets[start][unit][1], sets[start + lag][unit][1])
                         for start in range(max(0, len(frames) - lag))]
        qualified = eligible = 0
        for start in range(possible):
            middle, end = start + lag, start + 2 * lag
            window = regions[start:end + 1]
            if any(region["N"] < min_nodes or len(region["core_nodes"]) < min_core_nodes for region in window):
                continue
            eligible += 1
            if any(abs(a["N"] - b["N"]) / max(a["N"], b["N"]) > size_tolerance
                   or abs(a["core_fraction"] - b["core_fraction"]) > shape_tolerance
                   or abs(a["beta_per_edge"] - b["beta_per_edge"]) > shape_tolerance
                   for a, b in zip(regions[start:middle + 1], regions[middle:end + 1])):
                continue
            ratios = [max(region["N"] for region in period) / min(region["N"] for region in period)
                      for period in (regions[start:middle + 1], regions[middle:end + 1])]
            if min(ratios) < excursion_ratio:
                continue
            nt = [node_turnover[start], node_turnover[middle]]
            et = [edge_turnover[start], edge_turnover[middle]]
            if min(nt + et) < turnover_min:
                continue
            qualified += 1
            intervals.append({"unit_index": unit, "start_frame": start, "end_frame": end,
                              "start_tick": frames[start]["tick"], "middle_tick": frames[middle]["tick"],
                              "end_tick": frames[end]["tick"], "min_N": min(region["N"] for region in window),
                              "max_N": max(region["N"] for region in window),
                              "period_node_turnover": nt, "period_edge_turnover": et,
                              "period_excursion_ratios": ratios})
        core_sizes = [len(region["core_nodes"]) for region in regions]
        per_unit.append({"unit_index": unit, "possible_windows": possible,
                         "size_core_eligible_windows": eligible, "qualifying_windows": qualified,
                         "fraction": qualified / possible if possible else 0.0,
                         "mean_lag_core_node_turnover": sum(node_turnover) / len(node_turnover) if node_turnover else 0.0,
                         "mean_lag_core_edge_turnover": sum(edge_turnover) / len(edge_turnover) if edge_turnover else 0.0,
                         "min_core_nodes": min(core_sizes), "max_core_nodes": max(core_sizes)})
    return {"primary": sum(row["fraction"] for row in per_unit) / units if units else 0.0,
            "insufficient_trace": not units or possible == 0,
            "possible_windows_per_unit": possible, "unit_count": units,
            "frame_count": len(frames), "per_unit": per_unit, "qualifying_intervals": intervals,
            "scope": "Coarse component growth/decomposition recurrence with core replacement; "
                     "not full-state recurrence or evidence of a macroscopic organism. "
                     "Persistent-unit tracks are not independent replicates."}
