"""Rule objects and simulation driver for the feature lab."""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import List, Optional, Sequence

from .features import FULL_FEATURE_ORDER, feature_delta
from .graph_core import State, UGraph, is_bridge


@dataclass(frozen=True)
class SimulationParameters:
    """Continuous-time event rates and local rewrite probabilities."""

    r_seed: float = 0.05
    r_token: float = 1.0
    r_birth: float = 0.0
    r_death: float = 0.0
    p_triad: float = 0.08
    p_del: float = 0.04
    p_swap: float = 0.06
    avoid_disconnect: bool = False
    relocate_tokens: bool = False


@dataclass(frozen=True)
class TraversalContext:
    """Local token traversal context used by token rewrite rules."""

    token_index: int
    source: int
    destination: int


@dataclass(frozen=True)
class RuleMatch:
    """Concrete match for a rule application."""

    token_index: Optional[int] = None
    source: Optional[int] = None
    destination: Optional[int] = None
    target: Optional[int] = None
    host: Optional[int] = None


@dataclass(frozen=True)
class SimulationEvent:
    """Result of one simulator step."""

    channel: str
    event_name: str
    rule_name: str
    delta_features: Optional[dict[str, float]] = None


class Rule:
    """Base class for feature-lab rules."""

    name = "rule"

    def find_matches(
        self,
        state: State,
        traversal: Optional[TraversalContext] = None,
    ) -> List[RuleMatch]:
        raise NotImplementedError

    def apply(self, state: State, match: RuleMatch, rng: random.Random) -> None:
        raise NotImplementedError

    def delta_features(
        self,
        state: State,
        match: RuleMatch,
        feature_names: Sequence[str],
    ) -> dict[str, float]:
        """Return exact feature deltas by replaying the rule on a copy."""
        before = state.copy()
        after = state.copy()
        self.apply(after, match, random.Random(0))
        return feature_delta(before, after, feature_names)


def remove_or_relocate_tokens(state: State, removed_nodes: Sequence[int], relocate: bool, rng: random.Random) -> None:
    """Drop tokens on deleted nodes or relocate them to surviving nodes."""
    if not removed_nodes:
        return

    removed = set(removed_nodes)
    survivors = state.g.nodes()
    updated_tokens: List[int] = []
    for token in state.tokens:
        if token in removed:
            if relocate and survivors:
                updated_tokens.append(rng.choice(survivors))
            continue
        updated_tokens.append(token)
    state.tokens = updated_tokens


class SeedAttachRule(Rule):
    """Add a new leaf node attached to an existing host."""

    name = "seed"

    def __init__(self, choose_token_host: bool = True) -> None:
        self.choose_token_host = choose_token_host

    def find_matches(self, state: State, traversal: Optional[TraversalContext] = None) -> List[RuleMatch]:
        if state.g.num_nodes() == 0:
            return [RuleMatch()]

        if self.choose_token_host and state.tokens:
            hosts = sorted({token for token in state.tokens if token in state.g.adj})
        else:
            hosts = sorted(state.g.nodes())
        return [RuleMatch(host=host) for host in hosts]

    def apply(self, state: State, match: RuleMatch, rng: random.Random) -> None:
        if state.g.num_nodes() == 0:
            state.g.add_node(state.next_node_id)
            state.next_node_id += 1
            return
        if match.host is None:
            return
        new_node = state.next_node_id
        state.next_node_id += 1
        state.g.add_edge(new_node, match.host)


class TokenBirthRule(Rule):
    """Create a token on an existing node."""

    name = "birth"

    def find_matches(self, state: State, traversal: Optional[TraversalContext] = None) -> List[RuleMatch]:
        return [RuleMatch(target=node) for node in sorted(state.g.nodes())]

    def apply(self, state: State, match: RuleMatch, rng: random.Random) -> None:
        if match.target is not None:
            state.tokens.append(match.target)


class TokenDeathRule(Rule):
    """Remove a token by index."""

    name = "death"

    def find_matches(self, state: State, traversal: Optional[TraversalContext] = None) -> List[RuleMatch]:
        return [RuleMatch(token_index=index) for index in range(len(state.tokens))]

    def apply(self, state: State, match: RuleMatch, rng: random.Random) -> None:
        if match.token_index is None:
            return
        if 0 <= match.token_index < len(state.tokens):
            state.tokens.pop(match.token_index)


class DeleteTraversedEdgeRule(Rule):
    """Delete the traversed edge if allowed by the regime."""

    name = "delete"

    def __init__(self, avoid_disconnect: bool, relocate_tokens: bool) -> None:
        self.avoid_disconnect = avoid_disconnect
        self.relocate_tokens = relocate_tokens

    def find_matches(self, state: State, traversal: Optional[TraversalContext] = None) -> List[RuleMatch]:
        if traversal is None:
            return []
        if self.avoid_disconnect and is_bridge(state.g, traversal.source, traversal.destination, bfs_cap=5000):
            return []
        return [
            RuleMatch(
                token_index=traversal.token_index,
                source=traversal.source,
                destination=traversal.destination,
            )
        ]

    def apply(self, state: State, match: RuleMatch, rng: random.Random) -> None:
        if match.source is None or match.destination is None:
            return
        state.g.remove_edge(match.source, match.destination)
        removed_nodes = state.g.prune_isolated()
        remove_or_relocate_tokens(state, removed_nodes, self.relocate_tokens, rng)


class TriadicClosureRule(Rule):
    """Close a triangle from the traversed edge."""

    name = "triad"

    def find_matches(self, state: State, traversal: Optional[TraversalContext] = None) -> List[RuleMatch]:
        if traversal is None:
            return []
        candidates = [
            neighbor
            for neighbor in sorted(state.g.neighbors(traversal.destination))
            if neighbor != traversal.source and not state.g.has_edge(traversal.source, neighbor)
        ]
        return [
            RuleMatch(
                token_index=traversal.token_index,
                source=traversal.source,
                destination=traversal.destination,
                target=target,
            )
            for target in candidates
        ]

    def apply(self, state: State, match: RuleMatch, rng: random.Random) -> None:
        if match.source is None or match.target is None:
            return
        state.g.add_edge(match.source, match.target)


class StrictEdgeSwapRule(Rule):
    """Replace the traversed edge by a new local edge."""

    name = "swap"

    def __init__(self, avoid_disconnect: bool, relocate_tokens: bool) -> None:
        self.avoid_disconnect = avoid_disconnect
        self.relocate_tokens = relocate_tokens

    def find_matches(self, state: State, traversal: Optional[TraversalContext] = None) -> List[RuleMatch]:
        if traversal is None:
            return []
        if self.avoid_disconnect and is_bridge(state.g, traversal.source, traversal.destination, bfs_cap=5000):
            return []

        candidates = [
            neighbor
            for neighbor in sorted(state.g.neighbors(traversal.destination))
            if neighbor != traversal.source and not state.g.has_edge(traversal.source, neighbor)
        ]
        return [
            RuleMatch(
                token_index=traversal.token_index,
                source=traversal.source,
                destination=traversal.destination,
                target=target,
            )
            for target in candidates
        ]

    def apply(self, state: State, match: RuleMatch, rng: random.Random) -> None:
        if match.source is None or match.destination is None or match.target is None:
            return
        state.g.remove_edge(match.source, match.destination)
        state.g.add_edge(match.source, match.target)
        removed_nodes = state.g.prune_isolated()
        remove_or_relocate_tokens(state, removed_nodes, self.relocate_tokens, rng)


class FeatureLabSimulator:
    """Continuous-time simulator using explicit rule objects."""

    def __init__(
        self,
        params: SimulationParameters,
        delta_feature_names: Optional[Sequence[str]] = None,
    ) -> None:
        self.params = params
        self.delta_feature_names = list(delta_feature_names) if delta_feature_names else None
        self.seed_rule = SeedAttachRule(choose_token_host=True)
        self.birth_rule = TokenBirthRule()
        self.death_rule = TokenDeathRule()
        self.delete_rule = DeleteTraversedEdgeRule(
            avoid_disconnect=params.avoid_disconnect,
            relocate_tokens=params.relocate_tokens,
        )
        self.triad_rule = TriadicClosureRule()
        self.swap_rule = StrictEdgeSwapRule(
            avoid_disconnect=params.avoid_disconnect,
            relocate_tokens=params.relocate_tokens,
        )

    def step(self, state: State, rng: random.Random) -> SimulationEvent:
        """Advance the simulation by one Gillespie-style event."""
        n_tokens = len(state.tokens)
        channels = [
            ("seed", max(0.0, self.params.r_seed)),
            ("token", max(0.0, self.params.r_token) * n_tokens),
            ("birth", max(0.0, self.params.r_birth)),
            ("death", max(0.0, self.params.r_death)),
        ]
        total = sum(rate for _, rate in channels)
        if total <= 0.0:
            return SimulationEvent(channel="noop", event_name="noop", rule_name="noop")

        state.t += rng.expovariate(total)
        choice = rng.random() * total
        accum = 0.0
        selected_channel = "noop"
        for channel_name, rate in channels:
            accum += rate
            if choice <= accum:
                selected_channel = channel_name
                break

        if selected_channel == "seed":
            return self._apply_nonlocal_rule(state, self.seed_rule, rng, channel="seed")
        if selected_channel == "birth":
            return self._apply_nonlocal_rule(state, self.birth_rule, rng, channel="birth")
        if selected_channel == "death":
            return self._apply_nonlocal_rule(state, self.death_rule, rng, channel="death")
        if selected_channel == "token":
            return self._token_step(state, rng)
        return SimulationEvent(channel="noop", event_name="noop", rule_name="noop")

    def _apply_nonlocal_rule(self, state: State, rule: Rule, rng: random.Random, channel: str) -> SimulationEvent:
        matches = rule.find_matches(state)
        if not matches:
            return SimulationEvent(channel=channel, event_name="noop", rule_name=rule.name)
        match = rng.choice(matches)
        delta = rule.delta_features(state, match, self.delta_feature_names or FULL_FEATURE_ORDER)
        rule.apply(state, match, rng)
        return SimulationEvent(channel=channel, event_name=rule.name, rule_name=rule.name, delta_features=delta)

    def _token_step(self, state: State, rng: random.Random) -> SimulationEvent:
        if not state.tokens:
            return SimulationEvent(channel="token", event_name="noop", rule_name="noop")

        token_index = rng.randrange(len(state.tokens))
        source = state.tokens[token_index]
        destination = state.g.random_neighbor(source, rng)
        if destination is None:
            return SimulationEvent(channel="token", event_name="stuck", rule_name="stuck")

        state.tokens[token_index] = destination
        traversal = TraversalContext(token_index=token_index, source=source, destination=destination)

        roll = rng.random()
        if roll < self.params.p_del:
            return self._apply_token_rule(state, self.delete_rule, traversal, rng)
        roll -= self.params.p_del
        if roll < self.params.p_triad:
            return self._apply_token_rule(state, self.triad_rule, traversal, rng)
        roll -= self.params.p_triad
        if roll < self.params.p_swap:
            return self._apply_token_rule(state, self.swap_rule, traversal, rng)
        return SimulationEvent(channel="token", event_name="move", rule_name="move", delta_features=self._zero_delta())

    def _apply_token_rule(
        self,
        state: State,
        rule: Rule,
        traversal: TraversalContext,
        rng: random.Random,
    ) -> SimulationEvent:
        matches = rule.find_matches(state, traversal)
        if not matches:
            return SimulationEvent(channel="token", event_name="move", rule_name="move", delta_features=self._zero_delta())
        match = rng.choice(matches)
        delta = rule.delta_features(state, match, self.delta_feature_names or FULL_FEATURE_ORDER)
        rule.apply(state, match, rng)
        return SimulationEvent(channel="token", event_name=rule.name, rule_name=rule.name, delta_features=delta)

    def _zero_delta(self) -> Optional[dict[str, float]]:
        if self.delta_feature_names is None:
            return None
        return {name: 0.0 for name in self.delta_feature_names}
