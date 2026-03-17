from __future__ import annotations

import csv
import unittest
from pathlib import Path

import relational_universe_v10f_verify as verify


ROOT = Path(__file__).resolve().parents[1]


def load_csv(name: str):
    with (ROOT / "Documentation" / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class V10FRegressionTests(unittest.TestCase):
    def test_base_levels_exact(self) -> None:
        result = verify.verify_base_levels(load_csv("v10f_frontier_base_summary.csv"))
        self.assertTrue(result["ok"])

    def test_frontier_order(self) -> None:
        result = verify.verify_frontier_order(load_csv("v10f_frontier_final_candidate_summary.csv"))
        self.assertTrue(result["ok"], msg=str(result["failures"]))

    def test_recommendation_excludes_band_small_triad(self) -> None:
        result = verify.verify_report_text(ROOT / "Documentation" / "v0_10f_operativ_anbefaling.md")
        self.assertTrue(result["ok"])


if __name__ == "__main__":
    unittest.main()
