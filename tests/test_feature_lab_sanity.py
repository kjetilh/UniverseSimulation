"""Sanity checks for the refactored feature lab."""

from __future__ import annotations

import random
import unittest

from feature_lab.features import feature_row
from feature_lab.graph_core import State, UGraph
from feature_lab.rules import StrictEdgeSwapRule, TraversalContext


def build_sample_state() -> State:
    """Create a small connected graph with one token."""
    graph = UGraph()
    for edge in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        graph.add_edge(*edge)
    return State(g=graph, tokens=[0], t=0.0, next_node_id=4)


class FeatureLabSanityTests(unittest.TestCase):
    """Basic algebraic and rule-level invariants."""

    def test_beta1_identity(self) -> None:
        state = build_sample_state()
        row = feature_row(state)
        self.assertEqual(row["beta1"], row["edges"] - row["nodes"] + row["components"])

    def test_degree_square_identity(self) -> None:
        state = build_sample_state()
        row = feature_row(state)
        self.assertEqual(row["deg_sq_sum"], 2.0 * row["wedges"] + 2.0 * row["edges"])

    def test_strict_edge_swap_preserves_edges(self) -> None:
        state = build_sample_state()
        rule = StrictEdgeSwapRule(avoid_disconnect=False, relocate_tokens=False)
        traversal = TraversalContext(token_index=0, source=0, destination=1)
        matches = rule.find_matches(state, traversal)
        self.assertTrue(matches)
        match = next(match for match in matches if match.target == 2)
        delta = rule.delta_features(state, match, ["edges"])
        before_edges = state.g.num_edges()
        rule.apply(state, match, random.Random(0))
        self.assertEqual(before_edges, state.g.num_edges())
        self.assertEqual(delta["edges"], 0.0)


if __name__ == "__main__":
    unittest.main()
