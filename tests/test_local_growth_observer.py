"""Synthetic observer fixtures, not legal-kernel or spontaneous-growth evidence."""
import copy
import json
import random
from types import SimpleNamespace
import unittest

from Tools.local_growth_observer import balanced_replacement, evaluate, snapshot


def cycle(nodes):
    nodes = list(nodes)
    return [(nodes[index], nodes[(index + 1) % len(nodes)]) for index in range(len(nodes))]


def state(nodes, edges, units, tick=0):
    adjacency = {node: set() for node in nodes}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    return SimpleNamespace(adjacency=adjacency, units=list(units), ticks=tick, attempts=tick)


def positive_frames(count=17):
    frames = []
    for index in range(count):
        phase = index % 8
        size = 16 + 4 * min(phase, 8 - phase)
        base = 1000 * (index // 8)
        nodes = list(range(base, base + size))
        frames.append(snapshot(state(nodes, cycle(nodes), [base], index * 4)))
    return frames


def renamed_frames(frames):
    result = []
    rename = lambda node: 19 - 13 * node
    for frame in frames:
        # This fixture has one observed component and no unseen components.
        region = frame["regions"][0]
        nodes = [rename(node) for node in region["nodes"]]
        edges = [(rename(a), rename(b)) for a, b in region["edges"]]
        result.append(snapshot(state(nodes, edges, [nodes[0]], frame["tick"])))
    return result


class LocalGrowthObserverTests(unittest.TestCase):
    def test_snapshot_core_and_disconnected_global_diagnostics(self):
        graph = state(range(7), [(0, 1), (1, 2), (2, 0), (2, 3), (4, 5)], [0, 5, 6])
        frame = snapshot(graph)
        self.assertEqual((frame["N"], frame["E"], frame["C"], frame["beta"]), (7, 5, 3, 1))
        self.assertEqual(frame["regions"][0]["core_nodes"], [0, 1, 2])
        self.assertEqual(frame["regions"][0]["core_fraction"], 3 / 4)
        self.assertEqual(frame["regions"][1]["core_nodes"], [])
        self.assertEqual(frame["regions"][2]["beta_per_edge"], 0)
        json.dumps(frame, allow_nan=False)

    def test_engineered_coarse_cycles_with_identity_replacement(self):
        result = evaluate(positive_frames())
        self.assertEqual(result["primary"], 1)
        self.assertFalse(result["insufficient_trace"])
        self.assertEqual(result["possible_windows_per_unit"], 1)
        interval = result["qualifying_intervals"][0]
        self.assertEqual((interval["start_tick"], interval["middle_tick"], interval["end_tick"]), (0, 32, 64))
        self.assertEqual((interval["min_N"], interval["max_N"]), (16, 32))
        self.assertEqual(interval["period_node_turnover"], [1, 1])
        self.assertEqual(interval["period_edge_turnover"], [1, 1])

    def test_global_consistent_label_renaming(self):
        frames = positive_frames(25)
        self.assertEqual(evaluate(frames), evaluate(renamed_frames(frames)))

    def test_frozen_structure_does_not_qualify(self):
        frames = [snapshot(state(range(16), cycle(range(16)), [0], 4 * index)) for index in range(17)]
        self.assertEqual(evaluate(frames)["primary"], 0)

    def test_pure_accretion_is_not_balanced_replacement(self):
        frames = []
        for index in range(17):
            nodes = list(range(16 + 4 * index))
            edges = cycle(range(16)) + [(0, node) for node in nodes[16:]]
            frames.append(snapshot(state(nodes, edges, [0], index * 4)))
        result = evaluate(frames)
        self.assertEqual(result["primary"], 0)
        self.assertEqual(result["per_unit"][0]["mean_lag_core_node_turnover"], 0)
        self.assertEqual(balanced_replacement({1, 2}, {1, 2, 3, 4}), 0)

    def test_unobserved_disconnected_growth_does_not_enter_unit_region(self):
        frames = []
        for index in range(17):
            size = 16 + 4 * min(index % 8, 8 - index % 8)
            other = list(range(1000, 1000 + size))
            nodes = list(range(16)) + other
            frames.append(snapshot(state(nodes, cycle(range(16)) + cycle(other), [0], 4 * index)))
        self.assertNotEqual(frames[0]["N"], frames[4]["N"])
        self.assertEqual({frame["regions"][0]["N"] for frame in frames}, {16})
        self.assertEqual(evaluate(frames)["primary"], 0)

    def test_shared_component_units_have_separate_equal_tracks(self):
        frames = positive_frames()
        for frame in frames:
            region = copy.deepcopy(frame["regions"][0])
            region["unit_index"] = 1
            frame["regions"].append(region)
        result = evaluate(frames)
        self.assertEqual(result["primary"], 1)
        self.assertEqual(len(result["qualifying_intervals"]), 2)
        self.assertEqual([row["fraction"] for row in result["per_unit"]], [1, 1])

    def test_fixed_core_membership_fails_even_with_shape_cycles(self):
        frames = []
        for index in range(17):
            size = 16 + 4 * min(index % 8, 8 - index % 8)
            frames.append(snapshot(state(range(size), cycle(range(size)), [0], 4 * index)))
        result = evaluate(frames)
        self.assertEqual(result["primary"], 0)
        self.assertEqual(result["qualifying_intervals"], [])

    def test_shuffled_synthetic_order_does_not_qualify(self):
        original = positive_frames()
        order = list(range(0, 17, 2)) + list(range(1, 17, 2))
        frames = [copy.deepcopy(original[index]) for index in order]
        for index, frame in enumerate(frames):
            frame["tick"] = frame["attempt"] = index * 4
        # This permutation tests the observer only; it is not a legal history.
        self.assertEqual(evaluate(frames)["primary"], 0)

    def test_short_trace_and_empty_units_are_explicit(self):
        result = evaluate(positive_frames(16))
        self.assertTrue(result["insufficient_trace"])
        self.assertEqual(result["primary"], 0)
        self.assertEqual(result["possible_windows_per_unit"], 0)
        result = evaluate([snapshot(state([], [], [], 0))])
        self.assertTrue(result["insufficient_trace"])
        self.assertEqual(result["unit_count"], 0)

    def test_observer_does_not_mutate_inputs_or_consume_rng(self):
        graph = state(range(16), cycle(range(16)), [0, 1])
        before = copy.deepcopy(graph)
        rng_before = random.getstate()
        frame = snapshot(graph)
        frame["regions"][0]["nodes"].append(999)
        self.assertNotIn(999, frame["regions"][1]["nodes"])
        self.assertEqual(graph.__dict__, before.__dict__)
        frames = positive_frames()
        original = copy.deepcopy(frames)
        evaluate(frames)
        self.assertEqual(frames, original)
        self.assertEqual(random.getstate(), rng_before)

    def test_duplicate_or_nonincreasing_ticks_rejected(self):
        for tick in (0, -1):
            frames = positive_frames()
            frames[1]["tick"] = tick
            with self.subTest(tick=tick), self.assertRaises(ValueError):
                evaluate(frames)
        frames = positive_frames()
        frames[0]["attempt"] = 100
        with self.assertRaisesRegex(ValueError, "increase"):
            evaluate(frames)

    def test_unequal_exposure_spacing_rejected(self):
        frames = positive_frames()
        frames[2]["tick"] = frames[2]["attempt"] = 9
        with self.assertRaisesRegex(ValueError, "spacing"):
            evaluate(frames)

    def test_empty_trace_and_changing_unit_count_rejected(self):
        with self.assertRaises(ValueError):
            evaluate([])
        frames = positive_frames()
        frames[-1]["regions"] = []
        with self.assertRaisesRegex(ValueError, "unit count"):
            evaluate(frames)

    def test_corrupt_core_and_invalid_graph_rejected(self):
        frames = positive_frames()
        frames[0]["regions"][0]["core_fraction"] = 0.3
        with self.assertRaisesRegex(ValueError, "agree"):
            evaluate(frames)
        graph = state(range(3), [(0, 1)], [0])
        graph.adjacency[0].add(2)
        with self.assertRaisesRegex(ValueError, "undirected"):
            snapshot(graph)

    def test_invalid_parameters_rejected(self):
        for kwargs in ({"lag": 0}, {"lag": True}, {"min_nodes": -1},
                       {"shape_tolerance": float("nan")}, {"turnover_min": 2},
                       {"excursion_ratio": 0.5}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                evaluate(positive_frames(), **kwargs)


if __name__ == "__main__":
    unittest.main()
