"""Explicit rule objects with analytical core and motif deltas."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import random
from typing import Dict, List, Optional, Sequence

from .features import CORE_FEATURES, MOTIF_FEATURES, comb2
from .graph_core import State, common_neighbors_count, is_bridge


def _zero_delta(feature_names: Sequence[str]) -> Dict[str, float]:
    return {name: 0.0 for name in feature_names}


@dataclass(frozen=True)
class TraversalContext:
    """Local context for one token traversal."""

    token_index: int
    source: int
    destination: int
    deg_source_before: int
    deg_destination_before: int
    common_source_destination_before: int
    bridge_source_destination_before: bool
    locality_nodes: tuple[int, ...]


@dataclass(frozen=True)
class RuleContext:
    """Concrete local context for one rule application."""

    graph_was_empty: bool = False
    host: Optional[int] = None
    host_deg_before: Optional[int] = None
    token_index: Optional[int] = None
    source: Optional[int] = None
    destination: Optional[int] = None
    target: Optional[int] = None
    deg_source_before: Optional[int] = None
    deg_destination_before: Optional[int] = None
    deg_target_before: Optional[int] = None
    common_source_destination_before: Optional[int] = None
    common_source_target_before: Optional[int] = None
    bridge_source_destination_before: Optional[bool] = None
    locality_nodes: tuple[int, ...] = ()

    def to_row(self) -> Dict[str, object]:
        row = asdict(self)
        row["locality_nodes"] = ",".join(str(node) for node in self.locality_nodes)
        return row


class Rule:
    """Base class for primitive rewrite rules."""

    name = "rule"

    def candidate_contexts(
        self,
        state: State,
        traversal: Optional[TraversalContext] = None,
    ) -> List[RuleContext]:
        raise NotImplementedError

    def applies(self, state: State, context: RuleContext) -> bool:
        raise NotImplementedError

    def apply(self, state: State, context: RuleContext, rng: random.Random) -> None:
        raise NotImplementedError

    def delta_core(self, context: RuleContext) -> Dict[str, float]:
        return _zero_delta(CORE_FEATURES)

    def delta_motif(self, context: RuleContext) -> Dict[str, Optional[float]]:
        return {name: 0.0 for name in MOTIF_FEATURES}

    def theoretical_core_delta(self) -> Dict[str, float]:
        return self.delta_core(RuleContext())


def remove_or_relocate_tokens(state: State, removed_nodes: Sequence[int], relocate: bool, rng: random.Random) -> None:
    """Drop tokens on removed nodes or relocate them to surviving nodes."""

    if not removed_nodes:
        return

    removed = set(removed_nodes)
    survivors = sorted(state.g.nodes())
    updated_tokens: List[int] = []
    for token in state.tokens:
        if token in removed:
            if relocate and survivors:
                updated_tokens.append(rng.choice(survivors))
            continue
        updated_tokens.append(token)
    state.tokens = updated_tokens


class SeedAttachRule(Rule):
    """Attach a new leaf node to an existing host."""

    name = "seed"

    def __init__(self, choose_token_host: bool = True) -> None:
        self.choose_token_host = choose_token_host

    def candidate_contexts(
        self,
        state: State,
        traversal: Optional[TraversalContext] = None,
    ) -> List[RuleContext]:
        if state.g.num_nodes() == 0:
            return [RuleContext(graph_was_empty=True)]

        if self.choose_token_host and state.tokens:
            hosts = sorted({token for token in state.tokens if token in state.g.adj})
        else:
            hosts = sorted(state.g.nodes())
        return [
            RuleContext(
                host=host,
                host_deg_before=state.g.degree(host),
                locality_nodes=(host,),
            )
            for host in hosts
        ]

    def applies(self, state: State, context: RuleContext) -> bool:
        return context.graph_was_empty or context.host in state.g.adj

    def apply(self, state: State, context: RuleContext, rng: random.Random) -> None:
        if state.g.num_nodes() == 0 or context.graph_was_empty:
            state.g.add_node(state.next_node_id)
            state.next_node_id += 1
            return
        if context.host is None:
            return
        new_node = state.next_node_id
        state.next_node_id += 1
        state.g.add_edge(new_node, context.host)

    def delta_core(self, context: RuleContext) -> Dict[str, float]:
        delta = _zero_delta(CORE_FEATURES)
        delta["nodes"] = 1.0
        if context.graph_was_empty:
            delta["components"] = 1.0
        return delta

    def delta_motif(self, context: RuleContext) -> Dict[str, Optional[float]]:
        if context.graph_was_empty:
            return {"wedges": 0.0, "triangles": 0.0, "star3": 0.0}
        host_degree = int(context.host_deg_before or 0)
        return {
            "wedges": float(host_degree),
            "triangles": 0.0,
            "star3": float(comb2(host_degree)),
        }


class TokenBirthRule(Rule):
    """Create a token on an existing node."""

    name = "birth"

    def candidate_contexts(
        self,
        state: State,
        traversal: Optional[TraversalContext] = None,
    ) -> List[RuleContext]:
        return [RuleContext(target=node, locality_nodes=(node,)) for node in sorted(state.g.nodes())]

    def applies(self, state: State, context: RuleContext) -> bool:
        return context.target in state.g.adj

    def apply(self, state: State, context: RuleContext, rng: random.Random) -> None:
        if context.target is not None:
            state.tokens.append(context.target)

    def delta_core(self, context: RuleContext) -> Dict[str, float]:
        delta = _zero_delta(CORE_FEATURES)
        delta["tokens"] = 1.0
        return delta


class TokenDeathRule(Rule):
    """Remove a token by index."""

    name = "death"

    def candidate_contexts(
        self,
        state: State,
        traversal: Optional[TraversalContext] = None,
    ) -> List[RuleContext]:
        return [RuleContext(token_index=index) for index in range(len(state.tokens))]

    def applies(self, state: State, context: RuleContext) -> bool:
        return context.token_index is not None and 0 <= context.token_index < len(state.tokens)

    def apply(self, state: State, context: RuleContext, rng: random.Random) -> None:
        if context.token_index is None:
            return
        if 0 <= context.token_index < len(state.tokens):
            state.tokens.pop(context.token_index)

    def delta_core(self, context: RuleContext) -> Dict[str, float]:
        delta = _zero_delta(CORE_FEATURES)
        delta["tokens"] = -1.0
        return delta


class DeleteTraversedEdgeRule(Rule):
    """Delete a traversed edge when it is allowed."""

    name = "delete"

    def __init__(self, avoid_disconnect: bool, relocate_tokens: bool) -> None:
        self.avoid_disconnect = avoid_disconnect
        self.relocate_tokens = relocate_tokens

    def candidate_contexts(
        self,
        state: State,
        traversal: Optional[TraversalContext] = None,
    ) -> List[RuleContext]:
        if traversal is None:
            return []
        context = RuleContext(
            token_index=traversal.token_index,
            source=traversal.source,
            destination=traversal.destination,
            deg_source_before=traversal.deg_source_before,
            deg_destination_before=traversal.deg_destination_before,
            common_source_destination_before=traversal.common_source_destination_before,
            bridge_source_destination_before=traversal.bridge_source_destination_before,
            locality_nodes=traversal.locality_nodes,
        )
        return [context] if self.applies(state, context) else []

    def applies(self, state: State, context: RuleContext) -> bool:
        if context.source is None or context.destination is None:
            return False
        if self.avoid_disconnect and bool(context.bridge_source_destination_before):
            return False
        return state.g.has_edge(context.source, context.destination)

    def apply(self, state: State, context: RuleContext, rng: random.Random) -> None:
        if context.source is None or context.destination is None:
            return
        state.g.remove_edge(context.source, context.destination)
        removed = state.g.prune_isolated()
        remove_or_relocate_tokens(state, removed, self.relocate_tokens, rng)

    def delta_core(self, context: RuleContext) -> Dict[str, float]:
        delta = _zero_delta(CORE_FEATURES)
        delta["beta1"] = -1.0
        return delta

    def delta_motif(self, context: RuleContext) -> Dict[str, Optional[float]]:
        deg_source = int(context.deg_source_before or 0)
        deg_destination = int(context.deg_destination_before or 0)
        common = int(context.common_source_destination_before or 0)
        return {
            "wedges": float(-((deg_source - 1) + (deg_destination - 1))),
            "triangles": float(-common),
            "star3": float(-(comb2(deg_source - 1) + comb2(deg_destination - 1))),
        }


class TriadicClosureRule(Rule):
    """Add an edge from the source to a local target to close a triangle."""

    name = "triad"

    def candidate_contexts(
        self,
        state: State,
        traversal: Optional[TraversalContext] = None,
    ) -> List[RuleContext]:
        if traversal is None:
            return []
        candidates = [
            target
            for target in sorted(state.g.neighbors(traversal.destination))
            if target != traversal.source and not state.g.has_edge(traversal.source, target)
        ]
        return [
            RuleContext(
                token_index=traversal.token_index,
                source=traversal.source,
                destination=traversal.destination,
                target=target,
                deg_source_before=traversal.deg_source_before,
                deg_destination_before=traversal.deg_destination_before,
                deg_target_before=state.g.degree(target),
                common_source_destination_before=traversal.common_source_destination_before,
                common_source_target_before=common_neighbors_count(state.g, traversal.source, target),
                bridge_source_destination_before=traversal.bridge_source_destination_before,
                locality_nodes=tuple(sorted({traversal.source, traversal.destination, target})),
            )
            for target in candidates
        ]

    def applies(self, state: State, context: RuleContext) -> bool:
        if context.source is None or context.target is None:
            return False
        return not state.g.has_edge(context.source, context.target)

    def apply(self, state: State, context: RuleContext, rng: random.Random) -> None:
        if context.source is None or context.target is None:
            return
        state.g.add_edge(context.source, context.target)

    def delta_core(self, context: RuleContext) -> Dict[str, float]:
        delta = _zero_delta(CORE_FEATURES)
        delta["beta1"] = 1.0
        return delta

    def delta_motif(self, context: RuleContext) -> Dict[str, Optional[float]]:
        deg_source = int(context.deg_source_before or 0)
        deg_target = int(context.deg_target_before or 0)
        common = int(context.common_source_target_before or 0)
        return {
            "wedges": float(deg_source + deg_target),
            "triangles": float(common),
            "star3": float(comb2(deg_source) + comb2(deg_target)),
        }


class StrictEdgeSwapRule(Rule):
    """Remove the traversed edge and add a new local edge instead."""

    name = "swap"

    def __init__(self, avoid_disconnect: bool, relocate_tokens: bool) -> None:
        self.avoid_disconnect = avoid_disconnect
        self.relocate_tokens = relocate_tokens

    def candidate_contexts(
        self,
        state: State,
        traversal: Optional[TraversalContext] = None,
    ) -> List[RuleContext]:
        if traversal is None:
            return []
        if self.avoid_disconnect and traversal.bridge_source_destination_before:
            return []
        candidates = [
            target
            for target in sorted(state.g.neighbors(traversal.destination))
            if target != traversal.source and not state.g.has_edge(traversal.source, target)
        ]
        return [
            RuleContext(
                token_index=traversal.token_index,
                source=traversal.source,
                destination=traversal.destination,
                target=target,
                deg_source_before=traversal.deg_source_before,
                deg_destination_before=traversal.deg_destination_before,
                deg_target_before=state.g.degree(target),
                common_source_destination_before=traversal.common_source_destination_before,
                common_source_target_before=common_neighbors_count(state.g, traversal.source, target),
                bridge_source_destination_before=traversal.bridge_source_destination_before,
                locality_nodes=tuple(sorted({traversal.source, traversal.destination, target})),
            )
            for target in candidates
        ]

    def applies(self, state: State, context: RuleContext) -> bool:
        if context.source is None or context.destination is None or context.target is None:
            return False
        if self.avoid_disconnect and bool(context.bridge_source_destination_before):
            return False
        return state.g.has_edge(context.source, context.destination) and not state.g.has_edge(context.source, context.target)

    def apply(self, state: State, context: RuleContext, rng: random.Random) -> None:
        if context.source is None or context.destination is None or context.target is None:
            return
        state.g.remove_edge(context.source, context.destination)
        state.g.add_edge(context.source, context.target)
        removed = state.g.prune_isolated()
        remove_or_relocate_tokens(state, removed, self.relocate_tokens, rng)

    def delta_core(self, context: RuleContext) -> Dict[str, float]:
        return _zero_delta(CORE_FEATURES)

    def delta_motif(self, context: RuleContext) -> Dict[str, Optional[float]]:
        deg_destination = int(context.deg_destination_before or 0)
        deg_target = int(context.deg_target_before or 0)
        common_removed = int(context.common_source_destination_before or 0)
        common_added = int(context.common_source_target_before or 0)
        return {
            "wedges": float(-(deg_destination - 1) + deg_target),
            "triangles": float(-common_removed + (common_added - 1)),
            "star3": float(-comb2(deg_destination - 1) + comb2(deg_target)),
        }


def build_traversal_context(state: State, token_index: int, source: int, destination: int) -> TraversalContext:
    """Capture the local pre-rewrite context around a traversed edge."""

    locality_nodes = {source, destination}
    locality_nodes.update(state.g.neighbors(source))
    locality_nodes.update(state.g.neighbors(destination))
    for node in list(locality_nodes):
        locality_nodes.update(state.g.neighbors(node))
    return TraversalContext(
        token_index=token_index,
        source=source,
        destination=destination,
        deg_source_before=state.g.degree(source),
        deg_destination_before=state.g.degree(destination),
        common_source_destination_before=common_neighbors_count(state.g, source, destination),
        bridge_source_destination_before=is_bridge(state.g, source, destination, bfs_cap=5000),
        locality_nodes=tuple(sorted(locality_nodes)),
    )


def diff_support_nodes(reference: State, perturbed: State) -> List[int]:
    """Return nodes whose adjacency or token occupancy differs between two states."""

    token_counts_ref = Counter(reference.tokens)
    token_counts_pert = Counter(perturbed.tokens)
    candidates = set(reference.g.nodes()) | set(perturbed.g.nodes()) | set(token_counts_ref) | set(token_counts_pert)
    diff_nodes = []
    for node in sorted(candidates):
        if reference.g.neighbors(node) != perturbed.g.neighbors(node):
            diff_nodes.append(node)
            continue
        if token_counts_ref[node] != token_counts_pert[node]:
            diff_nodes.append(node)
    return diff_nodes
