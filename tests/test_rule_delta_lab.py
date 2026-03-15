"""Tests for the refactored rule-delta lab."""

from __future__ import annotations

import random
import unittest

from rule_delta_lab.features import CORE_FEATURES, MOTIF_FEATURES, feature_delta, feature_row
from rule_delta_lab.graph_core import State, UGraph
from rule_delta_lab.perturbation import SharedRNGStream, apply_local_perturbation, choose_local_perturbation
from rule_delta_lab.rules import (
    DeleteTraversedEdgeRule,
    SeedAttachRule,
    StrictEdgeSwapRule,
    TriadicClosureRule,
    build_traversal_context,
    diff_support_nodes,
)
from rule_delta_lab.simulator import SimulationParameters


def build_state(edges: list[tuple[int, int]], tokens: list[int], next_node_id: int) -> State:
    graph = UGraph()
    for edge in edges:
        graph.add_edge(*edge)
    return State(g=graph, tokens=list(tokens), t=0.0, next_node_id=next_node_id)


class RuleDeltaFormulaTests(unittest.TestCase):
    """Analytical delta formulas should match exact before/after feature differences."""

    def assert_formula_matches(
        self,
        state: State,
        rule,
        context,
    ) -> None:
        before = state.copy()
        after = state.copy()
        rule.apply(after, context, random.Random(0))
        actual = feature_delta(before, after, CORE_FEATURES + MOTIF_FEATURES)
        predicted = {}
        predicted.update(rule.delta_core(context))
        predicted.update(rule.delta_motif(context))
        for name in CORE_FEATURES + MOTIF_FEATURES:
            self.assertEqual(actual[name], predicted[name], msg=f"Mismatch for {rule.name}:{name}")

    def test_seed_formula(self) -> None:
        state = build_state([(0, 1), (1, 2), (2, 0)], [0], 3)
        rule = SeedAttachRule()
        context = next(ctx for ctx in rule.candidate_contexts(state) if ctx.host == 0)
        self.assert_formula_matches(state, rule, context)

    def test_triad_formula(self) -> None:
        state = build_state([(0, 1), (1, 2), (0, 3), (2, 3)], [0], 4)
        rule = TriadicClosureRule()
        traversal = build_traversal_context(state, token_index=0, source=0, destination=1)
        context = next(ctx for ctx in rule.candidate_contexts(state, traversal) if ctx.target == 2)
        self.assert_formula_matches(state, rule, context)

    def test_delete_formula(self) -> None:
        state = build_state([(0, 1), (1, 2), (2, 0), (0, 3), (1, 4)], [0], 5)
        rule = DeleteTraversedEdgeRule(avoid_disconnect=True, relocate_tokens=True)
        traversal = build_traversal_context(state, token_index=0, source=0, destination=1)
        context = rule.candidate_contexts(state, traversal)[0]
        self.assert_formula_matches(state, rule, context)

    def test_swap_formula_and_edge_count(self) -> None:
        state = build_state([(0, 1), (1, 2), (0, 3), (1, 3), (2, 3), (2, 4)], [0], 5)
        rule = StrictEdgeSwapRule(avoid_disconnect=True, relocate_tokens=True)
        traversal = build_traversal_context(state, token_index=0, source=0, destination=1)
        context = next(ctx for ctx in rule.candidate_contexts(state, traversal) if ctx.target == 2)
        before_edges = state.g.num_edges()
        self.assert_formula_matches(state, rule, context)

        after = state.copy()
        rule.apply(after, context, random.Random(0))
        self.assertEqual(before_edges, after.g.num_edges())

    def test_algebraic_identities_still_hold_after_swap(self) -> None:
        state = build_state([(0, 1), (1, 2), (2, 3), (3, 0)], [0], 4)
        row = feature_row(state)
        self.assertEqual(row["beta1"], row["edges"] - row["nodes"] + row["components"])
        self.assertEqual(row["deg_sq_sum"], 2.0 * row["wedges"] + 2.0 * row["edges"])

    def test_local_perturbation_creates_local_difference(self) -> None:
        state = build_state([(0, 1), (1, 2), (2, 0), (1, 3), (2, 4)], [0], 5)
        params = SimulationParameters(p_triad=0.1, p_del=0.1, p_swap=0.1, avoid_disconnect=True, relocate_tokens=True)
        stream = SharedRNGStream(7)
        choice = choose_local_perturbation(state.copy(), params, stream, "auto")
        perturbed = state.copy()
        apply_local_perturbation(perturbed, params, choice)
        diff_nodes = diff_support_nodes(state, perturbed)
        self.assertTrue(diff_nodes)
        self.assertTrue(set(diff_nodes).issubset(set(choice.support_nodes)))


if __name__ == "__main__":
    unittest.main()
