"""Bounded UC2 correctness checks; these are not evidence for emergent physics."""
import copy
from itertools import combinations
import random
import unittest

from Tools import local_change_candidate as model
from Tools.units_of_change_conformance import circulation_coverage


def all_small_graphs():
    for n in range(1, 5):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            yield n, [edge for bit, edge in enumerate(possible) if mask & (1 << bit)]


def beta(state):
    return len(model.edge_set(state)) - len(state.adjacency) + len(model.component_partition(state))


class LocalChangeTests(unittest.TestCase):
    def test_exhaustive_every_small_graph_position_and_move(self):
        positions = moves_checked = 0
        for n, edges in all_small_graphs():
            for source in range(n):
                original = model.make_state(range(n), edges, [source])
                positions += 1
                expected = {(u, a) for u in range(n) for a in range(n)
                            if u != a and u in original.adjacency[source]
                            and a in original.adjacency[source]
                            and a not in original.adjacency[u]}
                self.assertEqual(set(model.admissible_moves(original, 0)), expected)
                for target, carried in expected:
                    state = model.clone_state(original)
                    before_edges = model.edge_set(state)
                    result = model.apply_move(state, 0, target, carried)
                    moves_checked += 1
                    model.validate_state(state)
                    self.assertTrue(result.changed)
                    self.assertEqual((result.source, result.target), (source, target))
                    self.assertEqual(set(state.adjacency), set(original.adjacency))
                    self.assertEqual(len(model.edge_set(state)), len(before_edges))
                    self.assertEqual(len(model.edge_set(state) ^ before_edges), 2)
                    self.assertEqual(model.component_partition(state), model.component_partition(original))
                    self.assertEqual(beta(state), beta(original))
                    self.assertEqual(state.units, [target])
                    self.assertEqual((state.ticks, state.attempts), (1, 1))
                    self.assertIn(source, state.adjacency[target])
                    self.assertIn((source, carried), model.admissible_moves(state, 0))
                    model.apply_move(state, 0, source, carried)
                    self.assertEqual(model.state_snapshot(state)[:3], model.state_snapshot(original)[:3])
                    self.assertEqual((state.ticks, state.attempts), (2, 2))
        self.assertEqual(positions, 285)
        self.assertEqual(moves_checked, 198)

    def test_exhaustive_transition_law_equivariance(self):
        renaming = {0: 17, 1: -4, 2: 9, 3: 3}
        for n, edges in all_small_graphs():
            for source in range(n):
                state = model.make_state(range(n), edges, [source])
                renamed = model.make_state([renaming[i] for i in range(n)],
                                           [(renaming[a], renaming[b]) for a, b in edges],
                                           [renaming[source]])
                moves = model.admissible_moves(state, 0)
                renamed_moves = model.admissible_moves(renamed, 0)
                self.assertEqual({(renaming[u], renaming[a]) for u, a in moves}, set(renamed_moves))
                # Every corresponding move has probability 1 / number of moves.
                self.assertEqual(len(moves), len(renamed_moves))
                for target, carried in moves:
                    left, right = model.clone_state(state), model.clone_state(renamed)
                    model.apply_move(left, 0, target, carried)
                    model.apply_move(right, 0, renaming[target], renaming[carried])
                    self.assertEqual({renaming[v]: {renaming[w] for w in ns}
                                      for v, ns in left.adjacency.items()}, right.adjacency)
                    self.assertEqual([renaming[v] for v in left.units], right.units)

    def test_blocked_isolated_leaf_clique_and_empty(self):
        fixtures = [([0], [], [0]), ([0, 1], [(0, 1)], [0]),
                    ([0, 1, 2], [(0, 1), (1, 2), (0, 2)], [1]),
                    ([0], [], []), ([], [], [])]
        for nodes, edges, units in fixtures:
            state = model.make_state(nodes, edges, units)
            before = model.state_snapshot(state)
            result = model.attempt_step(state, random.Random(7))
            self.assertFalse(result.changed)
            self.assertEqual(model.state_snapshot(state)[:3], before[:3])
            self.assertEqual((state.ticks, state.attempts), (0, 1))

    def test_invalid_moves_are_transactional(self):
        original = model.make_state(range(4), [(0, 1), (0, 2)], [0])
        for index, target, carried in [(0, 1, 1), (0, 0, 1), (0, 3, 1),
                                       (0, 1, 3), (0, 10, 2), (-1, 1, 2),
                                       (1, 1, 2), (True, 1, 2), (0, True, 2),
                                       (0, 1, "2")]:
            state = model.clone_state(original)
            before = model.state_snapshot(state)
            with self.assertRaises(ValueError):
                model.apply_move(state, index, target, carried)
            self.assertEqual(model.state_snapshot(state), before)
        triangle = model.make_state(range(3), [(0, 1), (0, 2), (1, 2)], [0])
        before = model.state_snapshot(triangle)
        with self.assertRaises(ValueError):
            model.apply_move(triangle, 0, 1, 2)
        self.assertEqual(model.state_snapshot(triangle), before)

    def test_invalid_state_rejected_before_mutation_or_randomness(self):
        corruptions = [lambda s: s.units.append(99),
                       lambda s: s.adjacency[0].remove(1),
                       lambda s: s.adjacency[0].add(0),
                       lambda s: setattr(s, "ticks", 1)]
        for corrupt in corruptions:
            state = model.make_state(range(3), [(0, 1), (0, 2)], [0])
            corrupt(state)
            before = copy.deepcopy(state)
            rng = random.Random(9)
            rng_before = rng.getstate()
            with self.assertRaises(ValueError):
                model.attempt_step(state, rng)
            self.assertEqual(state, before)
            self.assertEqual(rng.getstate(), rng_before)

    def test_invalid_construction_and_owned_inputs(self):
        fixtures = [([0, 0], [], []), ([False], [], []), ([0], [(0, 0)], []),
                    ([0], [(0, 1)], []), ([0, 1], [(0, 1), (1, 0)], []),
                    ([0], [], [1]), ([0, 1], [(0,)], [])]
        for nodes, edges, units in fixtures:
            with self.assertRaises(ValueError):
                model.make_state(nodes, edges, units)
        nodes, edges, units = [0, 1, 2], [(0, 1), (0, 2)], [0, 0]
        state = model.make_state(nodes, edges, units)
        before = (nodes[:], edges[:], units[:])
        model.apply_move(state, 0, 1, 2)
        self.assertEqual((nodes, edges, units), before)
        self.assertEqual(state.units, [1, 0])

    def test_shared_mutable_adjacency_is_rejected_transactionally(self):
        # Opposite C4 vertices have equal neighbor values, but may not share
        # the same mutable container: a slide would otherwise edit both.
        state = model.make_state(range(4), [(0, 1), (1, 2), (2, 3), (3, 0)], [0])
        state.adjacency[2] = state.adjacency[0]
        before = copy.deepcopy(state)
        with self.assertRaises(ValueError):
            model.apply_move(state, 0, 1, 3)
        self.assertEqual(state, before)
        shared = {1, 3}
        with self.assertRaises(ValueError):
            model.State({0: shared, 2: shared, 1: {0, 2}, 3: {0, 2}}, [0])

    def test_uniform_scheduler_uses_all_units_including_blocked(self):
        class Choices:
            def __init__(self, values):
                self.values, self.bounds = iter(values), []

            def randrange(self, upper):
                self.bounds.append(upper)
                value = next(self.values)
                assert 0 <= value < upper
                return value

        original = model.make_state(range(4), [(0, 1), (0, 2)], [0, 3])
        outcomes = set()
        for move_index in range(2):
            state = model.clone_state(original)
            rng = Choices([0, move_index])
            result = model.attempt_step(state, rng)
            self.assertEqual(rng.bounds, [2, 2])
            outcomes.add((result.target, result.carried))
        self.assertEqual(outcomes, {(1, 2), (2, 1)})
        state = model.clone_state(original)
        rng = Choices([1])
        self.assertFalse(model.attempt_step(state, rng).changed)
        self.assertEqual(rng.bounds, [2])
        self.assertEqual(state.units, [0, 3])

    def test_multiple_units_never_cross_components(self):
        state = model.make_state(range(7), [(0, 1), (1, 2), (3, 4), (4, 5)], [1, 4, 6, 1])
        components = model.component_partition(state)
        memberships = [next(c for c in components if v in c) for v in state.units]
        rng = random.Random(271828)
        successes = 0
        for _ in range(256):
            before = list(state.units)
            result = model.attempt_step(state, rng)
            successes += result.changed
            self.assertEqual(model.component_partition(state), components)
            self.assertEqual(len(state.units), 4)
            for index, (position, component) in enumerate(zip(state.units, memberships)):
                self.assertIn(position, component)
                if index != result.unit_index:
                    self.assertEqual(position, before[index])
        self.assertEqual((state.ticks, state.attempts), (successes, 256))
        self.assertLess(state.ticks, state.attempts)

    def test_seeded_replay_and_observer_noninterference(self):
        initial = model.make_state(range(6), [(0, 1), (0, 2), (2, 3), (2, 4), (4, 5)], [0])
        left, right = model.clone_state(initial), model.clone_state(initial)
        rng_left, rng_right = random.Random(314159), random.Random(314159)
        global_before = random.getstate()
        history = [0]
        for _ in range(256):
            before = model.state_snapshot(right)
            stream_before = rng_right.getstate()
            model.edge_set(right)
            model.component_partition(right)
            circulation_coverage(history)
            self.assertEqual(model.state_snapshot(right), before)
            self.assertEqual(rng_right.getstate(), stream_before)
            first = model.attempt_step(left, rng_left)
            second = model.attempt_step(right, rng_right)
            self.assertEqual(first, second)
            self.assertEqual(model.state_snapshot(left), model.state_snapshot(right))
            history.append(second.target)
            self.assertEqual(beta(left), 0)
        self.assertEqual(random.getstate(), global_before)
        self.assertEqual(left.ticks, 256)

    def test_temporal_orbit_has_no_simultaneous_graph_cycle(self):
        state = model.make_state(range(3), [(0, 1), (0, 2)], [0])
        initial = model.state_snapshot(state)[:3]
        history = [0]
        for _ in range(3):
            for target, carried in [(1, 2), (2, 0), (0, 1)]:
                result = model.apply_move(state, 0, target, carried)
                history.append(result.target)
                self.assertEqual(beta(state), 0)
                self.assertEqual(len(model.edge_set(state)), 2)
            self.assertEqual(model.state_snapshot(state)[:3], initial)
        self.assertEqual(circulation_coverage(history), 1.0)
        self.assertEqual((state.ticks, state.attempts), (9, 9))


if __name__ == "__main__":
    unittest.main()
