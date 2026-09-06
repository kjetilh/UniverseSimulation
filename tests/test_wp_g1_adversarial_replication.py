from __future__ import annotations

import csv
import importlib.util
import math
import random
import statistics
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


replica = load_module(
    "wp_g1_replica", ROOT / "Tools" / "causet_admissibility_replica.py"
)
reference = load_module(
    "wp_f0_reference", ROOT / "Tools" / "causet_admissibility.py"
)


class SequenceRandom:
    def __init__(self, values):
        self.values = iter(values)

    def random(self):
        return next(self.values)


class PosetContractTests(unittest.TestCase):
    def test_link_count_is_the_cover_relation_on_five_elements(self):
        # 0<1<3<4 and 0<2<3<4, with all redundant ancestor edges retained.
        parents = [set(), {0}, {0}, {0, 1, 2}, {0, 1, 2, 3}]
        independent = replica.analyze_parents(parents)
        original = reference.Poset(5, parents)
        expected_covers = {(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)}
        self.assertEqual(independent.link_count, len(expected_covers))
        self.assertEqual(original.link_count(), len(expected_covers))

    def test_link_and_interval_algorithms_on_all_topological_five_node_dags(self):
        possible_edges = [(left, right) for right in range(5) for left in range(right)]
        for mask in range(1 << len(possible_edges)):
            parents = [set() for _ in range(5)]
            for bit, (left, right) in enumerate(possible_edges):
                if mask & (1 << bit):
                    parents[right].add(left)
            independent = replica.analyze_parents(parents)
            original = reference.Poset(5, parents)
            brute_links = 0
            brute_interval = 0
            for future, past_set in enumerate(independent.ancestors):
                for past in past_set:
                    intermediates = independent.descendants[past].intersection(past_set)
                    brute_interval = max(brute_interval, len(intermediates) + 2)
                    if not intermediates:
                        brute_links += 1
            self.assertEqual(original.link_count(), brute_links, f"mask={mask}")
            self.assertEqual(original.max_interval(), brute_interval, f"mask={mask}")

    def test_max_interval_is_inclusive_and_correct(self):
        parents = [set(), {0}, {0}, {1, 2}, {0, 1, 2, 3}]
        independent = replica.analyze_parents(parents)
        original = reference.Poset(5, parents)
        self.assertEqual(independent.max_interval, 5)
        self.assertEqual(original.max_interval(), 5)

    def test_decimation_uses_transitive_closure(self):
        original = reference.Poset(3, [set(), {0}, {1}])
        kept, height, r_value = original.decimate(
            0.5, SequenceRandom([0.1, 0.9, 0.1])
        )
        self.assertEqual((kept, height, r_value), (2, 2, 1.0))
        independent = replica.analyze_parents([set(), {0}, {1}])
        self.assertEqual(
            replica.induced_observables(independent.ancestors, frozenset({0, 2})),
            (2, 1.0),
        )

    def test_mm_dimension_boundaries_and_monotonicity(self):
        self.assertTrue(math.isinf(reference.mm_dimension(0.0)))
        self.assertEqual(reference.mm_dimension(1.0), 1.0001)
        values = [reference.mm_dimension(r) for r in (0.01, 0.03, 0.1, 0.5, 1.0)]
        self.assertTrue(all(left >= right for left, right in zip(values, values[1:])))


class LoaderFailureTests(unittest.TestCase):
    def write_edges(self, rows):
        temporary = tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", newline="", delete=False
        )
        fields = [
            "growth_seed",
            "run_offset",
            "arm",
            "run_seed",
            "parent_event_id",
            "child_event_id",
        ]
        with temporary:
            writer = csv.DictWriter(temporary, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        self.addCleanup(Path(temporary.name).unlink, missing_ok=True)
        return Path(temporary.name)

    def test_loader_cannot_represent_trailing_isolates(self):
        path = self.write_edges(
            [
                {
                    "growth_seed": 1,
                    "run_offset": 2,
                    "arm": "a",
                    "run_seed": 3,
                    "parent_event_id": 0,
                    "child_event_id": 1,
                }
            ]
        )
        loaded = reference.load_histories([path])
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0][-1].n, 2)
        self.assertNotEqual(loaded[0][-1].n, 5)  # true N cannot be encoded by edge max

    def test_loader_silently_drops_an_edgeless_history(self):
        path = self.write_edges([])
        self.assertEqual(reference.load_histories([path]), [])

    def test_loader_merges_distinct_run_seeds(self):
        path = self.write_edges(
            [
                {
                    "growth_seed": 1,
                    "run_offset": 2,
                    "arm": "a",
                    "run_seed": 10,
                    "parent_event_id": 0,
                    "child_event_id": 1,
                },
                {
                    "growth_seed": 1,
                    "run_offset": 2,
                    "arm": "a",
                    "run_seed": 11,
                    "parent_event_id": 1,
                    "child_event_id": 2,
                },
            ]
        )
        loaded = reference.load_histories([path])
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0][-1].n, 3)


class FitAndAggregateTests(unittest.TestCase):
    def test_measure_uses_only_one_draw_at_p_equals_one(self):
        poset = reference.chain_bundle(64, 4)
        _, draws = reference.measure(
            "test",
            "synthetic",
            "-",
            "-",
            "-",
            poset,
            20,
            random.Random(7),
            lambda _: None,
        )
        counts = {
            p_keep: sum(float(row["p"]) == p_keep for row in draws)
            for p_keep in reference.DECIMATION_P
        }
        self.assertEqual(counts[1.0], 1)
        self.assertEqual(counts[0.5], 20)

    def test_reported_even_sample_median_is_the_upper_middle(self):
        values = [1.0, 2.0, 3.0, 100.0]
        implementation_value = sorted(values)[len(values) // 2]
        self.assertEqual(implementation_value, 3.0)
        self.assertEqual(statistics.median(values), 2.5)
        self.assertNotEqual(implementation_value, statistics.median(values))


if __name__ == "__main__":
    unittest.main()
