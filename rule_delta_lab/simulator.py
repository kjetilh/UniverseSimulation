"""Simulation driver for the rule-delta lab."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
import random
from typing import Any, Dict, List, Optional, Sequence

from .analysis import TheoremRow, build_markdown_report
from .features import CORE_FEATURES, MOTIF_FEATURES, REDUCED_FEATURES, feature_row
from .graph_core import State, bootstrap
from .rules import (
    DeleteTraversedEdgeRule,
    Rule,
    RuleContext,
    SeedAttachRule,
    StrictEdgeSwapRule,
    TokenBirthRule,
    TokenDeathRule,
    TraversalContext,
    TriadicClosureRule,
    build_traversal_context,
)


@dataclass(frozen=True)
class SimulationParameters:
    """Continuous-time rates and local rule probabilities."""

    r_seed: float = 0.05
    r_token: float = 1.0
    r_birth: float = 0.0
    r_death: float = 0.0
    p_triad: float = 0.0
    p_del: float = 0.0
    p_swap: float = 0.06
    avoid_disconnect: bool = False
    relocate_tokens: bool = False


@dataclass(frozen=True)
class SimulationEvent:
    """One executed event with exact local metadata."""

    channel: str
    event_name: str
    rule_name: str
    context: Optional[RuleContext]
    predicted_delta: Dict[str, Optional[float]]


class RuleDeltaSimulator:
    """Explicit rule-engine for rule-conditioned delta analysis."""

    def __init__(self, params: SimulationParameters) -> None:
        self.params = params
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

    def theorem_rows(self) -> List[TheoremRow]:
        """Return exact statements for the primitive rules."""

        return [
            TheoremRow("seed", self.seed_rule.theoretical_core_delta(), self.seed_rule.delta_motif(RuleContext()), "Ny bladnode festes til eksisterende komponent."),
            TheoremRow("birth", self.birth_rule.theoretical_core_delta(), self.birth_rule.delta_motif(RuleContext()), "Token fødes på eksisterende node."),
            TheoremRow("death", self.death_rule.theoretical_core_delta(), self.death_rule.delta_motif(RuleContext()), "Token dør."),
            TheoremRow("triad", self.triad_rule.theoretical_core_delta(), {"wedges": 0.0, "triangles": 0.0, "star3": 0.0}, "Ny intern kant opprettes i samme komponent."),
            TheoremRow("delete", self.delete_rule.theoretical_core_delta(), {"wedges": 0.0, "triangles": 0.0, "star3": 0.0}, "Ikke-bro-kant fjernes i samme komponent."),
            TheoremRow("swap", self.swap_rule.theoretical_core_delta(), {"wedges": 0.0, "triangles": 0.0, "star3": 0.0}, "En kant fjernes og en annen legges inn lokalt."),
            TheoremRow("move", {name: 0.0 for name in CORE_FEATURES}, {name: 0.0 for name in MOTIF_FEATURES}, "Ren traversering uten omskriving."),
        ]

    def step(self, state: State, rng: random.Random) -> SimulationEvent:
        n_tokens = len(state.tokens)
        channels = [
            ("seed", max(0.0, self.params.r_seed)),
            ("token", max(0.0, self.params.r_token) * n_tokens),
            ("birth", max(0.0, self.params.r_birth)),
            ("death", max(0.0, self.params.r_death)),
        ]
        total = sum(rate for _, rate in channels)
        if total <= 0.0:
            return SimulationEvent(channel="noop", event_name="noop", rule_name="noop", context=None, predicted_delta={})

        state.t += rng.expovariate(total)
        choice = rng.random() * total
        cumulative = 0.0
        selected_channel = "noop"
        for channel_name, rate in channels:
            cumulative += rate
            if choice <= cumulative:
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
        return SimulationEvent(channel="noop", event_name="noop", rule_name="noop", context=None, predicted_delta={})

    def _predicted_delta(self, rule: Rule, context: RuleContext) -> Dict[str, Optional[float]]:
        predicted: Dict[str, Optional[float]] = {name: 0.0 for name in REDUCED_FEATURES}
        predicted.update(rule.delta_core(context))
        predicted.update(rule.delta_motif(context))
        for name in ["c4", "spectral_radius", "clustering", "dim_proxy"]:
            predicted[name] = None
        return predicted

    def _apply_nonlocal_rule(self, state: State, rule: Rule, rng: random.Random, channel: str) -> SimulationEvent:
        contexts = rule.candidate_contexts(state)
        if not contexts:
            return SimulationEvent(channel=channel, event_name="noop", rule_name="noop", context=None, predicted_delta={})
        context = contexts[rng.randrange(len(contexts))]
        predicted = self._predicted_delta(rule, context)
        rule.apply(state, context, rng)
        return SimulationEvent(channel=channel, event_name=rule.name, rule_name=rule.name, context=context, predicted_delta=predicted)

    def _token_step(self, state: State, rng: random.Random) -> SimulationEvent:
        if not state.tokens:
            return SimulationEvent(channel="token", event_name="noop", rule_name="noop", context=None, predicted_delta={})

        token_index = rng.randrange(len(state.tokens))
        source = state.tokens[token_index]
        neighbors = sorted(state.g.neighbors(source))
        if not neighbors:
            return SimulationEvent(channel="token", event_name="stuck", rule_name="stuck", context=None, predicted_delta={name: 0.0 for name in REDUCED_FEATURES})

        destination = neighbors[rng.randrange(len(neighbors))]
        traversal = build_traversal_context(state, token_index, source, destination)
        state.tokens[token_index] = destination

        roll = rng.random()
        if roll < self.params.p_del:
            return self._apply_token_rule(state, self.delete_rule, traversal, rng)
        roll -= self.params.p_del
        if roll < self.params.p_triad:
            return self._apply_token_rule(state, self.triad_rule, traversal, rng)
        roll -= self.params.p_triad
        if roll < self.params.p_swap:
            return self._apply_token_rule(state, self.swap_rule, traversal, rng)
        move_context = RuleContext(
            token_index=traversal.token_index,
            source=traversal.source,
            destination=traversal.destination,
            deg_source_before=traversal.deg_source_before,
            deg_destination_before=traversal.deg_destination_before,
            common_source_destination_before=traversal.common_source_destination_before,
            bridge_source_destination_before=traversal.bridge_source_destination_before,
            locality_nodes=traversal.locality_nodes,
        )
        return SimulationEvent(channel="token", event_name="move", rule_name="move", context=move_context, predicted_delta={name: 0.0 for name in REDUCED_FEATURES})

    def _apply_token_rule(
        self,
        state: State,
        rule: Rule,
        traversal: TraversalContext,
        rng: random.Random,
    ) -> SimulationEvent:
        contexts = rule.candidate_contexts(state, traversal)
        if not contexts:
            move_context = RuleContext(
                token_index=traversal.token_index,
                source=traversal.source,
                destination=traversal.destination,
                deg_source_before=traversal.deg_source_before,
                deg_destination_before=traversal.deg_destination_before,
                common_source_destination_before=traversal.common_source_destination_before,
                bridge_source_destination_before=traversal.bridge_source_destination_before,
                locality_nodes=traversal.locality_nodes,
            )
            return SimulationEvent(channel="token", event_name="move", rule_name="move", context=move_context, predicted_delta={name: 0.0 for name in REDUCED_FEATURES})
        context = contexts[rng.randrange(len(contexts))]
        predicted = self._predicted_delta(rule, context)
        rule.apply(state, context, rng)
        return SimulationEvent(channel="token", event_name=rule.name, rule_name=rule.name, context=context, predicted_delta=predicted)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reduced-basis and rule-conditioned delta-F lab.")
    parser.add_argument("--steps", type=int, default=12000)
    parser.add_argument("--seed", type=int, default=11)
    parser.add_argument("--initial-cycle", type=int, default=6)
    parser.add_argument("--initial-tokens", type=int, default=4)
    parser.add_argument("--r-seed", type=float, default=0.05)
    parser.add_argument("--r-token", type=float, default=1.0)
    parser.add_argument("--r-birth", type=float, default=0.0)
    parser.add_argument("--r-death", type=float, default=0.0)
    parser.add_argument("--p-triad", type=float, default=0.0)
    parser.add_argument("--p-del", type=float, default=0.0)
    parser.add_argument("--p-swap", type=float, default=0.06)
    parser.add_argument("--avoid-disconnect", action="store_true")
    parser.add_argument("--relocate-tokens", action="store_true")
    parser.add_argument("--closed-topological", action="store_true", help="Convenience preset: seed+swap, no triad/delete/birth/death, avoid_disconnect on.")
    parser.add_argument("--open-topological", action="store_true", help="Convenience preset: seed+triad+delete+swap, no birth/death, avoid_disconnect on.")
    parser.add_argument("--out-csv", type=str, default="rule_delta_events.csv")
    parser.add_argument("--out-md", type=str, default="rule_delta_summary.md")
    return parser


def apply_presets(args: argparse.Namespace) -> None:
    if args.closed_topological:
        args.p_triad = 0.0
        args.p_del = 0.0
        args.p_swap = max(args.p_swap, 0.06)
        args.r_birth = 0.0
        args.r_death = 0.0
        args.avoid_disconnect = True
        args.relocate_tokens = True
    if args.open_topological:
        args.p_triad = max(args.p_triad, 0.10)
        args.p_del = max(args.p_del, 0.10)
        args.p_swap = max(args.p_swap, 0.06)
        args.r_birth = 0.0
        args.r_death = 0.0
        args.avoid_disconnect = True
        args.relocate_tokens = True


def run(args: argparse.Namespace) -> None:
    apply_presets(args)
    rng = random.Random(args.seed)
    state = bootstrap(args.initial_cycle, args.initial_tokens, rng)
    simulator = RuleDeltaSimulator(
        SimulationParameters(
            r_seed=args.r_seed,
            r_token=args.r_token,
            r_birth=args.r_birth,
            r_death=args.r_death,
            p_triad=args.p_triad,
            p_del=args.p_del,
            p_swap=args.p_swap,
            avoid_disconnect=args.avoid_disconnect,
            relocate_tokens=args.relocate_tokens,
        )
    )

    event_rows: List[Dict[str, Any]] = []
    for index in range(args.steps):
        before = feature_row(state)
        event = simulator.step(state, rng)
        after = feature_row(state)

        row: Dict[str, Any] = {
            "i": index,
            "t_before": before["t"],
            "t_after": after["t"],
            "event": event.event_name,
            "channel": event.channel,
            "rule_name": event.rule_name,
        }
        if event.context is not None:
            row.update(event.context.to_row())
        for name in REDUCED_FEATURES:
            row[f"before_{name}"] = before[name]
            row[f"after_{name}"] = after[name]
            row[f"d_{name}"] = after[name] - before[name]
            predicted = event.predicted_delta.get(name)
            row[f"pred_{name}"] = "" if predicted is None else predicted
        event_rows.append(row)

    fieldnames = sorted({key for row in event_rows for key in row})
    with open(args.out_csv, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(event_rows)

    markdown = build_markdown_report(args, event_rows, args.out_csv, simulator.theorem_rows())
    with open(args.out_md, "w", encoding="utf-8") as handle:
        handle.write(markdown)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    run(args)
    return 0

