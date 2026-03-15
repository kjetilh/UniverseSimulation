"""Coupled-run perturbation lab with a shared RNG stream."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import hashlib
import math
import random
from typing import Any, Dict, Iterable, List, Optional, Sequence

from .features import REDUCED_FEATURES, feature_row
from .graph_core import State, bootstrap, multi_source_distances
from .rules import (
    DeleteTraversedEdgeRule,
    Rule,
    RuleContext,
    StrictEdgeSwapRule,
    TraversalContext,
    TriadicClosureRule,
    build_traversal_context,
    diff_support_nodes,
)
from .simulator import RuleDeltaSimulator, SimulationParameters


class SharedRNGStream:
    """Semantic RNG stream keyed by event index and label."""

    def __init__(self, seed: int) -> None:
        self.seed = seed

    def _unit(self, event_index: int, label: str) -> float:
        payload = f"{self.seed}:{event_index}:{label}".encode("utf-8")
        digest = hashlib.blake2b(payload, digest_size=8).digest()
        value = int.from_bytes(digest, "big")
        return (value + 0.5) / float(1 << 64)

    def random(self, event_index: int, label: str) -> float:
        value = self._unit(event_index, label)
        return min(max(value, 1e-15), 1.0 - 1e-15)

    def randrange(self, event_index: int, label: str, stop: int) -> int:
        if stop <= 0:
            raise ValueError("stop must be positive")
        return min(int(self.random(event_index, label) * stop), stop - 1)

    def choice(self, event_index: int, label: str, values: Sequence[int]) -> int:
        if not values:
            raise ValueError("cannot choose from an empty sequence")
        return values[self.randrange(event_index, label, len(values))]

    def expovariate(self, event_index: int, label: str, rate: float) -> float:
        if rate <= 0.0:
            raise ValueError("rate must be positive")
        return -math.log(1.0 - self.random(event_index, label)) / rate


@dataclass(frozen=True)
class PerturbationChoice:
    """Chosen one-off local perturbation."""

    rule_name: str
    context: RuleContext
    support_nodes: tuple[int, ...]


def _direct_support(rule_name: str, context: RuleContext) -> tuple[int, ...]:
    nodes = set()
    for node in [context.source, context.destination]:
        if node is not None:
            nodes.add(node)
    if rule_name in {"triad", "swap"} and context.target is not None:
        nodes.add(context.target)
    return tuple(sorted(nodes))


def _pick_context(
    contexts: Sequence[RuleContext],
    stream: SharedRNGStream,
    event_index: int,
    label: str,
) -> RuleContext:
    return contexts[stream.randrange(event_index, label, len(contexts))]


def _sample_traversal(state: State, stream: SharedRNGStream, event_index: int, prefix: str) -> Optional[TraversalContext]:
    if not state.tokens:
        return None
    token_index = stream.randrange(event_index, f"{prefix}:token_index", len(state.tokens))
    source = state.tokens[token_index]
    neighbors = sorted(state.g.neighbors(source))
    if not neighbors:
        return None
    destination = stream.choice(event_index, f"{prefix}:neighbor", neighbors)
    return build_traversal_context(state, token_index, source, destination)


def choose_local_perturbation(
    state: State,
    params: SimulationParameters,
    stream: SharedRNGStream,
    perturbation: str,
) -> PerturbationChoice:
    """Choose one applicable local perturbation on the current state."""

    traversal = _sample_traversal(state, stream, 0, "perturb")
    if traversal is None:
        raise RuntimeError("Could not sample a local perturbation because no traversable token was found")

    rules: List[Rule]
    if perturbation == "delete":
        rules = [DeleteTraversedEdgeRule(params.avoid_disconnect, params.relocate_tokens)]
    elif perturbation == "triad":
        rules = [TriadicClosureRule()]
    elif perturbation == "swap":
        rules = [StrictEdgeSwapRule(params.avoid_disconnect, params.relocate_tokens)]
    else:
        rules = [
            DeleteTraversedEdgeRule(params.avoid_disconnect, params.relocate_tokens),
            TriadicClosureRule(),
            StrictEdgeSwapRule(params.avoid_disconnect, params.relocate_tokens),
        ]

    for rule in rules:
        contexts = rule.candidate_contexts(state, traversal)
        if contexts:
            context = _pick_context(contexts, stream, 0, f"perturb:{rule.name}:context")
            return PerturbationChoice(rule.name, context, _direct_support(rule.name, context))
    raise RuntimeError(f"No applicable local perturbation found for mode '{perturbation}'")


def apply_local_perturbation(
    state: State,
    params: SimulationParameters,
    choice: PerturbationChoice,
) -> None:
    """Apply a one-off intervention without advancing event time."""

    token_index = choice.context.token_index
    if token_index is not None and choice.context.destination is not None and 0 <= token_index < len(state.tokens):
        state.tokens[token_index] = choice.context.destination
    rng = random.Random(0)
    if choice.rule_name == "delete":
        rule: Rule = DeleteTraversedEdgeRule(params.avoid_disconnect, params.relocate_tokens)
    elif choice.rule_name == "triad":
        rule = TriadicClosureRule()
    elif choice.rule_name == "swap":
        rule = StrictEdgeSwapRule(params.avoid_disconnect, params.relocate_tokens)
    else:
        raise ValueError(f"Unsupported perturbation rule: {choice.rule_name}")
    rule.apply(state, choice.context, rng)


def _step_shared(
    state: State,
    params: SimulationParameters,
    simulator: RuleDeltaSimulator,
    stream: SharedRNGStream,
    event_index: int,
) -> str:
    n_tokens = len(state.tokens)
    channels = [
        ("seed", max(0.0, params.r_seed)),
        ("token", max(0.0, params.r_token) * n_tokens),
        ("birth", max(0.0, params.r_birth)),
        ("death", max(0.0, params.r_death)),
    ]
    total = sum(rate for _, rate in channels)
    if total <= 0.0:
        return "noop"

    state.t += stream.expovariate(event_index, "dt", total)
    choice = stream.random(event_index, "channel") * total
    cumulative = 0.0
    channel = "noop"
    for name, rate in channels:
        cumulative += rate
        if choice <= cumulative:
            channel = name
            break

    if channel == "seed":
        contexts = simulator.seed_rule.candidate_contexts(state)
        if not contexts:
            return "noop"
        context = _pick_context(contexts, stream, event_index, "seed:context")
        simulator.seed_rule.apply(state, context, random.Random(0))
        return "seed"

    if channel == "birth":
        contexts = simulator.birth_rule.candidate_contexts(state)
        if not contexts:
            return "noop"
        context = _pick_context(contexts, stream, event_index, "birth:context")
        simulator.birth_rule.apply(state, context, random.Random(0))
        return "birth"

    if channel == "death":
        contexts = simulator.death_rule.candidate_contexts(state)
        if not contexts:
            return "noop"
        context = _pick_context(contexts, stream, event_index, "death:context")
        simulator.death_rule.apply(state, context, random.Random(0))
        return "death"

    traversal = _sample_traversal(state, stream, event_index, "token")
    if traversal is None:
        return "stuck"
    state.tokens[traversal.token_index] = traversal.destination

    roll = stream.random(event_index, "token:rewrite")
    if roll < params.p_del:
        contexts = simulator.delete_rule.candidate_contexts(state, traversal)
        if contexts:
            context = _pick_context(contexts, stream, event_index, "delete:context")
            simulator.delete_rule.apply(state, context, random.Random(0))
            return "delete"
        return "move"
    roll -= params.p_del
    if roll < params.p_triad:
        contexts = simulator.triad_rule.candidate_contexts(state, traversal)
        if contexts:
            context = _pick_context(contexts, stream, event_index, "triad:context")
            simulator.triad_rule.apply(state, context, random.Random(0))
            return "triad"
        return "move"
    roll -= params.p_triad
    if roll < params.p_swap:
        contexts = simulator.swap_rule.candidate_contexts(state, traversal)
        if contexts:
            context = _pick_context(contexts, stream, event_index, "swap:context")
            simulator.swap_rule.apply(state, context, random.Random(0))
            return "swap"
        return "move"
    return "move"


def _distance_histogram(
    diff_nodes: Iterable[int],
    ref_distances: Dict[int, int],
    pert_distances: Dict[int, int],
    max_distance: int,
) -> tuple[Dict[int, int], int]:
    histogram = defaultdict(int)
    spread_radius = 0
    for node in diff_nodes:
        candidates = []
        if node in ref_distances:
            candidates.append(ref_distances[node])
        if node in pert_distances:
            candidates.append(pert_distances[node])
        if not candidates:
            histogram[max_distance + 1] += 1
            continue
        distance = min(candidates)
        histogram[min(distance, max_distance + 1)] += 1
        spread_radius = max(spread_radius, distance)
    return dict(histogram), spread_radius


def build_perturbation_report(
    rows: Sequence[Dict[str, Any]],
    csv_path: str,
    perturbation_choice: PerturbationChoice,
    args: Any,
) -> str:
    max_radius = max((int(row["spread_radius"]) for row in rows), default=0)
    first_hit: Dict[int, int] = {}
    for row in rows:
        radius = int(row["spread_radius"])
        first_hit.setdefault(radius, int(row["event_index"]))

    lines = [
        "# Perturbation Lab",
        "",
        "## Metode",
        "",
        "To simuleringer startes fra samme warmup-tilstand og drives deretter av samme semantiske RNG-strøm.",
        "En ekstra lokal omskriving settes inn bare i den perturberte kopien før den kopla kjøringen starter.",
        "",
        "## Eksakte antagelser",
        "",
        "- Samme event-indeks bruker samme RNG-nøkler i begge kjøringer.",
        "- Perturbasjonen er lokal og følger en eksisterende primitiv regel.",
        "- `spread_radius` måles som største grafdistanse fra perturbasjonens initiale support til de noder som fortsatt er forskjellige.",
        "",
        "## Kjøringsparametre",
        "",
        f"- steps: {args.steps}",
        f"- warmup_steps: {args.warmup_steps}",
        f"- seed: {args.seed}",
        f"- perturbation: {args.perturbation}",
        f"- actual_perturbation: {perturbation_choice.rule_name}",
        f"- support_nodes: {', '.join(str(node) for node in perturbation_choice.support_nodes)}",
        "",
        "## Numeriske observasjoner",
        "",
        f"- max_spread_radius: {max_radius}",
        f"- final_spread_radius: {int(rows[-1]['spread_radius']) if rows else 0}",
        f"- final_c_star_event: {float(rows[-1]['c_star_event']) if rows else 0.0:.6g}",
        f"- final_c_star_time: {float(rows[-1]['c_star_time']) if rows else 0.0:.6g}",
        "",
        "### Første treff per radius",
        "",
    ]
    if first_hit:
        for radius in sorted(first_hit):
            lines.append(f"- radius {radius}: event {first_hit[radius]}")
    else:
        lines.append("- ingen spredning utover initial support")

    lines.extend(
        [
            "",
            "### Tolkning",
            "",
            "#### Teorem/identitet",
            "",
            "- Den delte RNG-strømmen betyr at observerte avvik skyldes tilstandsavhengighet etter perturbasjonen, ikke ulik ekstern støy.",
            "",
            "#### Numerisk observasjon",
            "",
            "- `c_star_event` og `c_star_time` er empiriske overkanter i denne kjøringen, ikke universelle konstanter.",
            "",
            "#### Spekulativ fortolkning",
            "",
            "- Hvis `spread_radius` vokser lineært over mange kjøringer og regimer, kan dette tolkes som en effektiv causal-cone-lignende front i universgrafen.",
            "",
            f"_CSV med rå perturbasjonsdata: `{csv_path}`_",
            "",
        ]
    )
    return "\n".join(lines)


def build_parser() -> Any:
    import argparse

    parser = argparse.ArgumentParser(description="Coupled perturbation lab for the relational universe graph.")
    parser.add_argument("--steps", type=int, default=1500)
    parser.add_argument("--warmup-steps", type=int, default=300)
    parser.add_argument("--seed", type=int, default=23)
    parser.add_argument("--initial-cycle", type=int, default=6)
    parser.add_argument("--initial-tokens", type=int, default=4)
    parser.add_argument("--r-seed", type=float, default=0.05)
    parser.add_argument("--r-token", type=float, default=1.0)
    parser.add_argument("--r-birth", type=float, default=0.0)
    parser.add_argument("--r-death", type=float, default=0.0)
    parser.add_argument("--p-triad", type=float, default=0.10)
    parser.add_argument("--p-del", type=float, default=0.10)
    parser.add_argument("--p-swap", type=float, default=0.06)
    parser.add_argument("--avoid-disconnect", action="store_true")
    parser.add_argument("--relocate-tokens", action="store_true")
    parser.add_argument("--perturbation", choices=("auto", "delete", "triad", "swap"), default="auto")
    parser.add_argument("--max-distance", type=int, default=6)
    parser.add_argument("--out-csv", type=str, default="rule_delta_perturbation_events.csv")
    parser.add_argument("--out-md", type=str, default="rule_delta_perturbation_summary.md")
    return parser


def run(args: Any) -> None:
    params = SimulationParameters(
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
    bootstrap_rng = random.Random(args.seed)
    base_state = bootstrap(args.initial_cycle, args.initial_tokens, bootstrap_rng)
    warmup_sim = RuleDeltaSimulator(params)
    warmup_stream = SharedRNGStream(args.seed)
    for event_index in range(1, args.warmup_steps + 1):
        _step_shared(base_state, params, warmup_sim, warmup_stream, event_index)

    reference = base_state.copy()
    perturbed = base_state.copy()
    perturbation_choice = choose_local_perturbation(reference.copy(), params, warmup_stream, args.perturbation)
    apply_local_perturbation(perturbed, params, perturbation_choice)
    initial_support = perturbation_choice.support_nodes
    if not initial_support:
        raise RuntimeError("Initial perturbation support was empty")

    simulator = RuleDeltaSimulator(params)
    stream = SharedRNGStream(args.seed + 1)
    rows: List[Dict[str, Any]] = []
    previous_radius = 0
    c_star_event = 0.0
    c_star_time = 0.0

    for event_index in range(1, args.steps + 1):
        event_ref = _step_shared(reference, params, simulator, stream, event_index)
        event_pert = _step_shared(perturbed, params, simulator, stream, event_index)
        diff_nodes = diff_support_nodes(reference, perturbed)
        ref_distances = multi_source_distances(reference.g, initial_support)
        pert_distances = multi_source_distances(perturbed.g, initial_support)
        histogram, spread_radius = _distance_histogram(diff_nodes, ref_distances, pert_distances, args.max_distance)

        elapsed_mean_time = max(0.5 * (reference.t + perturbed.t) - base_state.t, 0.0)
        instantaneous_speed = float(spread_radius - previous_radius)
        avg_speed_event = float(spread_radius) / float(event_index)
        avg_speed_time = float(spread_radius) / elapsed_mean_time if elapsed_mean_time > 0.0 else 0.0
        c_star_event = max(c_star_event, instantaneous_speed, avg_speed_event)
        c_star_time = max(c_star_time, avg_speed_time)
        previous_radius = spread_radius

        row: Dict[str, Any] = {
            "event_index": event_index,
            "event_ref": event_ref,
            "event_pert": event_pert,
            "t_ref": reference.t,
            "t_pert": perturbed.t,
            "diff_node_count": len(diff_nodes),
            "spread_radius": spread_radius,
            "instantaneous_speed": instantaneous_speed,
            "avg_speed_event": avg_speed_event,
            "avg_speed_time": avg_speed_time,
            "c_star_event": c_star_event,
            "c_star_time": c_star_time,
        }
        for distance in range(args.max_distance + 1):
            row[f"distance_{distance}"] = histogram.get(distance, 0)
        row[f"distance_gt_{args.max_distance}"] = histogram.get(args.max_distance + 1, 0)

        ref_row = feature_row(reference)
        pert_row = feature_row(perturbed)
        for feature in REDUCED_FEATURES:
            row[f"diff_{feature}"] = pert_row[feature] - ref_row[feature]
        rows.append(row)

    import csv

    fieldnames = sorted({key for row in rows for key in row})
    with open(args.out_csv, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    markdown = build_perturbation_report(rows, args.out_csv, perturbation_choice, args)
    with open(args.out_md, "w", encoding="utf-8") as handle:
        handle.write(markdown)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    run(args)
    return 0
