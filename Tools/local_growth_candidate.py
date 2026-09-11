"""UC3: chosen local node-growth/decomposition extension of the UC2 kernel.

Nodes remain unweighted and untyped; the unit population is fixed. A bud
creates a triangle on an existing edge and moves the selected unit onto the
newborn node. This explicitly permits traversal of a relation created within
that birth event. All other traversals use a pre-event edge. Collapse removes
only an unshared degree-two triangular host; cut keeps all nodes and units.

The four integer class weights are a frozen design choice, not an estimated
balance law. A blocked class is not replaced by another class. Node identities
are never reused by the transition API; next_node_id is bookkeeping, not a
physical node property. No limits silently disable birth within this kernel.
"""
from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable, Sequence

from Tools.local_change_candidate import (
    State,
    admissible_moves,
    apply_move,
    component_partition,
    edge_set,
    make_state as make_base_state,
    state_snapshot as base_snapshot,
    validate_state as validate_base_state,
)

CLASSES = ("slide", "bud", "collapse", "cut")
DEFAULT_WEIGHTS = (4, 1, 2, 1)


@dataclass
class GrowthState(State):
    next_node_id: int | None = None

    def __post_init__(self) -> None:
        validate_base_state(self)
        if self.next_node_id is None:
            self.next_node_id = max(0, max(self.adjacency, default=-1) + 1)
        validate_state(self)


@dataclass(frozen=True)
class StepEvent:
    changed: bool
    kind: str | None
    unit_index: int | None
    source: int | None
    target: int | None
    carried: int | None
    born: int | None
    removed: int | None
    reason: str


def _integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_state(state: GrowthState) -> None:
    if not isinstance(state, GrowthState):
        raise ValueError("Expected a GrowthState with a persistent birth-ID counter")
    validate_base_state(state)
    if (not _integer(state.next_node_id) or state.next_node_id < 0 or
            state.next_node_id <= max(state.adjacency, default=-1)):
        raise ValueError("Birth-ID counter must be nonnegative and above existing node names")


def make_state(nodes: Iterable[int], edges: Iterable[tuple[int, int]],
               units: Iterable[int], next_node_id: int | None = None) -> GrowthState:
    base = make_base_state(nodes, edges, units)
    return GrowthState(base.adjacency, base.units, next_node_id=next_node_id)


def clone_state(state: GrowthState) -> GrowthState:
    validate_state(state)
    return GrowthState({v: set(ns) for v, ns in state.adjacency.items()},
                       list(state.units), state.ticks, state.attempts, state.next_node_id)


def state_snapshot(state: GrowthState) -> tuple:
    """Immutable observation, including counters; not a physical-state quotient."""
    validate_state(state)
    return base_snapshot(state) + (state.next_node_id,)


def _validate_unit_index(state: GrowthState, unit_index: int) -> None:
    if not _integer(unit_index) or not 0 <= unit_index < len(state.units):
        raise ValueError("Unit index is out of range")


def _collapse_neighbors(state: GrowthState, source: int) -> tuple[int, ...]:
    neighbors = state.adjacency[source]
    if len(neighbors) != 2 or state.units.count(source) != 1:
        return ()
    a, b = sorted(neighbors)
    return (a, b) if b in state.adjacency[a] else ()


def apply_event(state: GrowthState, unit_index: int, kind: str,
                target: int | None = None, carried: int | None = None) -> StepEvent:
    """Apply a specified event; invalid inputs change neither state nor counters.

    slide: target=u, carried=a uses the unchanged UC2 endpoint relocation.
    bud: target=u specifies the existing anchor adjacent to source v; carried
         must be omitted. The returned target/born is newborn w and returned
         carried is the anchor u. Add v-w,u-w, retain v-u, move this unit to w.
    collapse: target=u is a neighbor of the triangular degree-two source v.
         carried may be omitted or name its other neighbor a. Move to u and
         remove v with both its edges; no other unit may occupy v.
    cut: target=u is an existing neighbor; carried must be omitted. Traverse
         v-u and remove that edge, retaining even isolated nodes and units.

    One accepted atomic rewrite is one tick, irrespective of its edge count.
    """
    validate_state(state)
    _validate_unit_index(state, unit_index)
    if kind not in CLASSES:
        raise ValueError("Unknown local growth event class")
    if not _integer(target):
        raise ValueError("A specified event requires an integer target/anchor")
    source = state.units[unit_index]
    if kind == "slide":
        result = apply_move(state, unit_index, target, carried)
        return StepEvent(True, kind, unit_index, source, result.target,
                         result.carried, None, None, "slide")

    if target not in state.adjacency[source]:
        raise ValueError("Target/anchor must be adjacent to the source before the event")
    if kind in ("bud", "cut") and carried is not None:
        raise ValueError("Bud and cut accept only one specified neighbor")
    if kind == "collapse":
        neighbors = _collapse_neighbors(state, source)
        if not neighbors:
            raise ValueError("Collapse requires an unshared degree-two triangular host")
        other = next(v for v in neighbors if v != target)
        if carried is not None and (not _integer(carried) or carried != other):
            raise ValueError("Collapse carried endpoint must be the other neighbor")

    # Every domain precondition is checked above; no invalid request partially
    # edits adjacency, unit positions, allocation state, or observer counters.
    born = removed = None
    if kind == "bud":
        anchor = target
        born = state.next_node_id
        state.adjacency[born] = {source, anchor}
        state.adjacency[source].add(born)
        state.adjacency[anchor].add(born)
        state.units[unit_index] = born
        state.next_node_id += 1
        target, carried = born, anchor
    elif kind == "collapse":
        carried = other
        state.adjacency[target].remove(source)
        state.adjacency[carried].remove(source)
        del state.adjacency[source]
        state.units[unit_index] = target
        removed = source
    else:  # cut
        state.adjacency[source].remove(target)
        state.adjacency[target].remove(source)
        state.units[unit_index] = target
    state.attempts += 1
    state.ticks += 1
    return StepEvent(True, kind, unit_index, source, target, carried, born, removed, kind)


def _validate_weights(weights: Sequence[int]) -> int:
    if (not isinstance(weights, (tuple, list)) or len(weights) != len(CLASSES) or
            any(not _integer(w) or w < 0 for w in weights) or sum(weights) <= 0):
        raise ValueError("Four nonnegative integer class weights with positive sum are required")
    return sum(weights)


def attempt_step(state: GrowthState, rng: random.Random,
                 weights: Sequence[int] = DEFAULT_WEIGHTS) -> StepEvent:
    """Draw unit uniformly, class by integer weights, then its local target.

    Sorted choices provide deterministic replay, not identical seeded paths
    under arbitrary renaming. Transition probabilities are label-equivariant.
    There is no resampling of a blocked unit/class. Callers must impose finite
    attempt budgets or report absorption; successful-tick targets may stall.
    """
    validate_state(state)
    total = _validate_weights(weights)
    if not state.units:
        state.attempts += 1
        return StepEvent(False, None, None, None, None, None, None, None, "no_units")
    unit_index = rng.randrange(len(state.units))
    source = state.units[unit_index]
    draw = rng.randrange(total)
    for kind, weight in zip(CLASSES, weights):
        if draw < weight:
            break
        draw -= weight

    if kind == "slide":
        choices = admissible_moves(state, unit_index)
        if choices:
            target, carried = choices[rng.randrange(len(choices))]
            return apply_event(state, unit_index, kind, target, carried)
    else:
        neighbors = (_collapse_neighbors(state, source) if kind == "collapse"
                     else tuple(sorted(state.adjacency[source])))
        if neighbors:
            return apply_event(state, unit_index, kind, neighbors[rng.randrange(len(neighbors))])
    state.attempts += 1
    return StepEvent(False, kind, unit_index, source, None, None, None, None, "blocked")
