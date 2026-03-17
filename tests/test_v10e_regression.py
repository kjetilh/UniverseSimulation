from __future__ import annotations

import csv
import unittest
from pathlib import Path

import relational_universe_v10e_verify as verify


ROOT = Path(__file__).resolve().parents[1]


def load_csv(name: str):
    with (ROOT / "Documentation" / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class V10ERegressionTests(unittest.TestCase):
    def test_base_levels_are_separated(self) -> None:
        result = verify.verify_base_separation(load_csv("v10e_focused_band_base_summary.csv"))
        self.assertTrue(result["ok"])

    def test_band_best_is_not_top_mean_composite(self) -> None:
        result = verify.verify_top_candidate(load_csv("v10e_focused_band_candidate_summary.csv"))
        self.assertTrue(result["ok"])
        self.assertEqual(result["top_mean_composite"], "band_zero_del")

    def test_pairwise_table_is_consistent(self) -> None:
        result = verify.verify_pairwise(load_csv("v10e_focused_band_pairwise.csv"))
        self.assertTrue(result["ok"], msg=str(result["failures"]))

    def test_focused_score_regenerates(self) -> None:
        result = verify.verify_focused_score(load_csv("v10e_focused_band_candidate_summary.csv"))
        self.assertTrue(result["ok"], msg=str(result["failures"]))


if __name__ == "__main__":
    unittest.main()
