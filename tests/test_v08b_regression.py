from __future__ import annotations

import csv
import unittest
from pathlib import Path

import relational_universe_v08b_verify as verify


ROOT = Path(__file__).resolve().parents[1]
RUN_CSV = ROOT / "Documentation" / "v08b_natural_ensemble_runs.csv"
ENSEMBLE_CSV = ROOT / "Documentation" / "v08b_natural_ensemble_aggregate.csv"
OVERALL_CSV = ROOT / "Documentation" / "v08b_candidate_robustness.csv"


def load_rows(path: Path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class V08BRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.run_rows = load_rows(RUN_CSV)
        cls.ensemble_rows = load_rows(ENSEMBLE_CSV)
        cls.overall_rows = load_rows(OVERALL_CSV)

    def test_csv_structures_are_backward_compatible(self) -> None:
        self.assertTrue(verify.column_check(self.run_rows, verify.RUN_REQUIRED_COLUMNS)["ok"])
        self.assertTrue(verify.column_check(self.ensemble_rows, verify.ENSEMBLE_REQUIRED_COLUMNS)["ok"])
        self.assertTrue(verify.column_check(self.overall_rows, verify.OVERALL_REQUIRED_COLUMNS)["ok"])

    def test_natural_ensembles_remain_larger_than_toy_baseline(self) -> None:
        result = verify.verify_ensemble_growth(self.run_rows)
        self.assertTrue(result["ok"])
        natural = result["natural_mean_nodes"]
        self.assertGreater(natural["natural24"], 20.0)
        self.assertGreater(natural["natural48"], 40.0)
        self.assertGreater(natural["natural_jitter"], 28.0)

    def test_top_candidate_does_not_collapse(self) -> None:
        ranked = sorted(
            self.overall_rows,
            key=lambda row: (
                float(row["ci_low_mean_composite_natural"]),
                float(row["mean_composite_natural"]),
            ),
            reverse=True,
        )
        top = ranked[0]
        self.assertGreater(float(top["mean_composite_natural"]), 0.62)
        self.assertGreater(float(top["ci_low_mean_composite_natural"]), 0.55)

    def test_bootstrap_ranking_stays_stable(self) -> None:
        result = verify.ranking_stability(
            self.ensemble_rows,
            bootstrap_seeds=[314159, 314160, 314170, 314180, 314190],
            bootstrap_reps=200,
        )
        self.assertTrue(result["ok"])
        self.assertLessEqual(max(result["top_candidate_positions"]), 2)
        self.assertGreaterEqual(result["common_top3_count"], 2)


if __name__ == "__main__":
    unittest.main()
