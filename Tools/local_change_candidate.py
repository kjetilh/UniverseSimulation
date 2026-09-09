"""UC2: a finite, fixed-population slice of local units-of-change dynamics.

A unit at v moves to an existing neighbor u while relocating another incident
edge (a, v) to (a, u). Nodes have no physical attributes; integer names and unit
list positions are bookkeeping only. No node/unit births, deaths, pruning,
global reconnections, weights, or stored orientation are implemented here.

Slides preserve the node set, edge count, connected-component partition and
therefore cycle rank. They cannot create a simultaneous graph cycle from a
tree. A temporal closed itinerary can nevertheless occur on changing trees.
"""
from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable


@dataclass
class State:
    adjacency: dict[int, set[int]]
    units: list[int]
    ticks: int = 0
    attempts: int = 0

    def __post_init__(self) -> None:
        validate_state(self)


@dataclass(frozen=True)
class StepResult:
    changed: bool
    unit_index: int | None
    source: int | None
    target: int | None
    carried: int | None
    reason: str


def _integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_state(state: State) -> None:
    """Reject invalid inputs before any transition or random draw."""
    if not isinstance(state, State):
        raise ValueError("Expected a State")
    if not isinstance(state.adjacency, dict):
        raise ValueError("Adjacency must be a dictionary")
    neighbor_containers = set()
    for node, neighbors in state.adjacency.items():
        if not _integer(node) or not isinstance(neighbors, set):
            raise ValueError("Node names must be integers and neighbors must be sets")
        if id(neighbors) in neighbor_containers:
            raise ValueError("Nodes must own distinct mutable neighbor sets")
        neighbor_containers.add(id(neighbors))
        for neighbor in neighbors:
            if not _integer(neighbor) or neighbor == node:
                raise ValueError("Edges must join distinct integer nodes")
            if neighbor not in state.adjacency:
                raise ValueError("An edge refers to an absent node")
            reverse = state.adjacency[neighbor]
            if not isinstance(reverse, set) or node not in reverse:
                raise ValueError("Adjacency must be symmetric")
    if not isinstance(state.units, list) or any(
        not _integer(node) or node not in state.adjacency for node in state.units
    ):
        raise ValueError("Every persistent unit must occupy an existing node")
    if any(not _integer(value) or value < 0 for value in (state.ticks, state.attempts)):
        raise ValueError("Counters must be nonnegative integers")
    if state.ticks > state.attempts:
        raise ValueError("Successful changes cannot exceed attempts")


def make_state(
    nodes: Iterable[int], edges: Iterable[tuple[int, int]], units: Iterable[int]
) -> State:
    """Construct owned containers; isolated nodes and coincident units are valid."""
    node_list = list(nodes)
    if any(not _integer(node) for node in node_list):
        raise ValueError("Node names must be integers")
    if len(set(node_list)) != len(node_list):
        raise ValueError("Node names must be unique")
    adjacency = {node: set() for node in node_list}
    for edge in edges:
        if not isinstance(edge, (tuple, list)) or len(edge) != 2:
            raise ValueError("Each edge must have exactly two endpoints")
        a, b = edge
        if not _integer(a) or not _integer(b) or a == b:
            raise ValueError("Edges must join distinct integer nodes")
        if a not in adjacency or b not in adjacency:
            raise ValueError("An edge refers to an absent node")
        if b in adjacency[a]:
            raise ValueError("Duplicate undirected edge")
        adjacency[a].add(b)
        adjacency[b].add(a)
    return State(adjacency, list(units))


def clone_state(state: State) -> State:
    validate_state(state)
    return State({node: set(ns) for node, ns in state.adjacency.items()},
                 list(state.units), state.ticks, state.attempts)


def edge_set(state: State) -> frozenset[tuple[int, int]]:
    validate_state(state)
    return frozenset((a, b) for a, ns in state.adjacency.items() for b in ns if a < b)


def component_partition(state: State) -> frozenset[frozenset[int]]:
    validate_state(state)
    remaining = set(state.adjacency)
    components = []
    while remaining:
        start = min(remaining)
        component = {start}
        stack = [start]
        remaining.remove(start)
        while stack:
            for neighbor in state.adjacency[stack.pop()]:
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    component.add(neighbor)
                    stack.append(neighbor)
        components.append(frozenset(component))
    return frozenset(components)


def state_snapshot(state: State) -> tuple:
    """Stable, immutable observation including both counters."""
    validate_state(state)
    return (tuple(sorted(state.adjacency)), tuple(sorted(edge_set(state))),
            tuple(state.units), state.ticks, state.attempts)


def _validate_unit_index(state: State, unit_index: int) -> None:
    if not _integer(unit_index) or not 0 <= unit_index < len(state.units):
        raise ValueError("Unit index is out of range")


def _moves_at(state: State, source: int) -> tuple[tuple[int, int], ...]:
    neighbors = sorted(state.adjacency[source])
    return tuple((target, carried) for target in neighbors for carried in neighbors
                 if carried != target and carried not in state.adjacency[target])


def admissible_moves(state: State, unit_index: int) -> tuple[tuple[int, int], ...]:
    """Return all (target, carried-neighbor) choices, in stable name order.

    Uniform sampling over this list is equivariant under renaming. Sorting
    makes seeded replay deterministic; it does not promise the same seeded
    path under an arbitrary renaming of nodes.
    """
    validate_state(state)
    _validate_unit_index(state, unit_index)
    return _moves_at(state, state.units[unit_index])


def _apply_valid_move(state: State, unit_index: int, target: int, carried: int) -> StepResult:
    source = state.units[unit_index]
    state.adjacency[source].remove(carried)
    state.adjacency[carried].remove(source)
    state.adjacency[target].add(carried)
    state.adjacency[carried].add(target)
    state.units[unit_index] = target
    state.attempts += 1
    state.ticks += 1
    return StepResult(True, unit_index, source, target, carried, "slide")


def apply_move(state: State, unit_index: int, target: int, carried: int) -> StepResult:
    """Execute one specified legal change; invalid calls mutate nothing."""
    validate_state(state)
    _validate_unit_index(state, unit_index)
    if not _integer(target) or not _integer(carried):
        raise ValueError("Move endpoints must be integers")
    if (target, carried) not in _moves_at(state, state.units[unit_index]):
        raise ValueError("Move is not an admissible local endpoint relocation")
    return _apply_valid_move(state, unit_index, target, carried)


def attempt_step(state: State, rng: random.Random) -> StepResult:
    """Choose a uniform unit, then a uniform legal slide at its position.

    A blocked selection increments only attempts. Units at leaves or isolated
    nodes persist in place. The caller owns the random stream; observation
    does not consume it. No resampling of a blocked unit is performed.
    """
    validate_state(state)
    if not state.units:
        state.attempts += 1
        return StepResult(False, None, None, None, None, "no_units")
    unit_index = rng.randrange(len(state.units))
    source = state.units[unit_index]
    moves = _moves_at(state, source)
    if not moves:
        state.attempts += 1
        return StepResult(False, unit_index, source, None, None, "blocked")
    target, carried = moves[rng.randrange(len(moves))]
    return _apply_valid_move(state, unit_index, target, carried)
