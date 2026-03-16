from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

import relational_universe_v09b_asymptotic_refinement as v09b


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_CSV = ROOT / "Documentation" / "v09b_asymptotic_candidate_summary.csv"
SIZE_CSV = ROOT / "Documentation" / "v09b_asymptotic_size_profiles.csv"


def load_rows(path: Path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class V09BRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidate_rows = load_rows(CANDIDATE_CSV)
        cls.size_rows = load_rows(SIZE_CSV)

    def test_alpha_jump_formula(self) -> None:
        for row in self.candidate_rows:
            alpha_large = float(row["alpha_large"])
            alpha_all = float(row["alpha_all"])
            alpha_jump = float(row["alpha_jump"])
            self.assertAlmostEqual(alpha_jump, alpha_large - alpha_all, places=6)

    def test_linear_margin_formula(self) -> None:
        for row in self.candidate_rows:
            expected = float(row["rmse_linear"]) - min(float(row["rmse_log"]), float(row["rmse_sqrt"]))
            self.assertAlmostEqual(float(row["linear_margin"]), expected, places=6)

    def test_asymptotic_score_ranking_is_monotone(self) -> None:
        scores = [float(row["asymptotic_score"]) for row in self.candidate_rows]
        self.assertTrue(all(a >= b for a, b in zip(scores, scores[1:])))

    def test_size_profiles_have_expected_scales(self) -> None:
        counts = {}
        for row in self.size_rows:
            counts[row["candidate_name"]] = counts.get(row["candidate_name"], 0) + 1
        self.assertTrue(all(count == 4 for count in counts.values()))

    def test_missing_data_is_handled_cleanly(self) -> None:
        with self.assertRaises(ValueError):
            v09b.asymptotic_metrics_from_group_rows([])

    def test_write_csv_preserves_columns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "regen.csv"
            v09b.write_csv(out, self.candidate_rows)
            with open(out, newline="", encoding="utf-8") as f:
                regen = list(csv.DictReader(f))
            self.assertEqual(list(regen[0].keys()), list(self.candidate_rows[0].keys()))

    def test_band_best_beats_balanced_pdel_on_artifact_metrics(self) -> None:
        rows = {row["candidate_name"]: row for row in self.candidate_rows}
        band = rows["band_best"]
        balanced = rows["balanced_pdel"]
        self.assertLess(float(band["alpha_jump"]), float(balanced["alpha_jump"]))
        self.assertGreater(float(band["linear_margin"]), float(balanced["linear_margin"]))


if __name__ == "__main__":
    unittest.main()
