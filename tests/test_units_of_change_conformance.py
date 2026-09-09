"""Small analytic checks for the UC1 instrument, not universe-model tests."""
import unittest

from Tools.units_of_change_conformance import circulation_coverage, sign_probability


class CirculationTests(unittest.TestCase):
    def test_three_laps_required(self):
        self.assertEqual(circulation_coverage([0, 1, 2, 0, 1, 2, 0]), 0)
        self.assertEqual(circulation_coverage([0, 1, 2, 0, 1, 2, 0, 1, 2, 0]), 1)

    def test_backtracking_and_path_are_not_cycles(self):
        self.assertEqual(circulation_coverage([0, 1] * 20), 0)
        self.assertEqual(circulation_coverage(list(range(40))), 0)

    def test_overlapping_laps_count_once(self):
        self.assertEqual(circulation_coverage([i % 4 for i in range(41)]), 1)

    def test_relabelling_and_reversal(self):
        path = [i % 3 for i in range(15)] + [8, 9, 10]
        labels = {node: 100 - 7 * node for node in set(path)}
        value = circulation_coverage(path)
        self.assertEqual(value, circulation_coverage([labels[node] for node in path]))
        self.assertEqual(value, circulation_coverage(path[::-1]))

    def test_incomplete_and_acyclic(self):
        for path in ([], [1], [1, 2], [1, 2, 3]):
            self.assertEqual(circulation_coverage(path), 0)

    def test_sign_probability(self):
        self.assertEqual(sign_probability(16, 0), 1 / 65536)
        self.assertEqual(sign_probability(0, 0), 1)
        self.assertEqual(sign_probability(1, 1), .75)


if __name__ == "__main__":
    unittest.main()
