from __future__ import annotations

import unittest

import relational_universe_v09_scale_and_natural_ensembles as v09


class FakeGraph:
    def __init__(self, n: int) -> None:
        self._n = n

    def num_nodes(self) -> int:
        return self._n


class FakeState:
    def __init__(self, n: int) -> None:
        self.g = FakeGraph(n)


def synthetic_run_row(value: float) -> dict:
    return {
        "meeting": 1.0,
        "first_meeting_time": 1.0,
        "final_radius_control": value,
        "total_unequal_time": value,
        "avg_local_overlap": value,
        "avg_same_descriptor": value,
        "shared_token_fraction_final": value,
        "shared_node_fraction_final": value,
        "fit_speed_control": value,
        "final_edge_diff_count": value,
        "abs_delta_tokens": value,
        "abs_delta_nodes": value,
        "abs_delta_beta1": value,
        "abs_delta_triangles": value,
        "abs_delta_spectral_radius": value,
        "abs_delta_clustering": value,
        "abs_delta_dim_proxy": value,
        "initial_nodes": 24.0,
        "initial_tokens": 4.0,
        "initial_beta1": 1.0,
        "initial_triangles": 0.0,
        "initial_spectral_radius": 2.0,
        "initial_dim_proxy": 1.0,
    }


class V09RegressionTests(unittest.TestCase):
    def test_compute_steps_for_state_is_monotonic_under_clamps(self) -> None:
        sizes = [5, 20, 50, 200]
        steps = [
            v09.compute_steps_for_state(FakeState(n), steps_per_node=4.5, min_steps=120, max_steps=300)
            for n in sizes
        ]
        self.assertEqual(steps, [120, 120, 225, 300])
        self.assertTrue(all(a <= b for a, b in zip(steps, steps[1:])))

    def test_bootstrap_tolerates_constant_metric(self) -> None:
        point = v09.ScaleCandidate("const", 0.02, 0.02, 0.02, 0.0, 0.01)
        ensembles = [
            v09.ScaleEnsemble("natural24_light", 24, "light", 10, 5, 420, 20, 80),
            v09.ScaleEnsemble("natural24_deep", 24, "deep", 10, 5, 820, 180, 320),
            v09.ScaleEnsemble("natural48_light", 48, "light", 12, 6, 960, 40, 140),
        ]
        run_rows = []
        group_rows = []
        for ens in ensembles:
            rows = []
            for _ in range(3):
                row = synthetic_run_row(1.0)
                row.update(
                    {
                        "candidate_name": point.name,
                        "r_birth": point.r_birth,
                        "r_death": point.r_death,
                        "p_swap": point.p_swap,
                        "p_triad": point.p_triad,
                        "p_del": point.p_del,
                        "ensemble": ens.name,
                        "burnin_label": ens.burnin_label,
                        "target_nodes": ens.target_nodes,
                        "seed": 1,
                        "steps": 120,
                    }
                )
                rows.append(row)
                run_rows.append(row)
            group_rows.append(v09.summarize_group(point, ens, rows))
        ranges = v09.score_ranges(group_rows)
        out = v09.bootstrap_candidate_summary(point, ensembles, run_rows, ranges, reps=10, rng_seed=1)
        self.assertIn("ci_low_mean_composite", out)
        self.assertIn("ci_low_radius_alpha", out)

    def test_burnin_sensitivity_on_synthetic_rows(self) -> None:
        rows = [
            {"target_nodes": 24, "burnin_label": "light", "composite_score": 0.8},
            {"target_nodes": 24, "burnin_label": "deep", "composite_score": 0.7},
            {"target_nodes": 48, "burnin_label": "light", "composite_score": 0.5},
            {"target_nodes": 48, "burnin_label": "deep", "composite_score": 0.6},
        ]
        self.assertAlmostEqual(v09.burnin_sensitivity(rows), 0.1, places=7)

    def test_radius_alpha_is_zero_for_constant_radius(self) -> None:
        rows = []
        for n in [24.0, 48.0, 96.0]:
            rows.append(
                {
                    "mean_initial_nodes": n,
                    "mean_final_radius_control": 5.0,
                    "mean_avg_local_overlap": 0.8,
                    "quasi_score": 0.7,
                    "mean_abs_delta_beta1": 1.0,
                }
            )
        metrics = v09.fit_scale_metrics(rows)
        self.assertAlmostEqual(metrics["radius_alpha"], 0.0, delta=1e-9)

    def test_radius_alpha_is_one_for_linear_radius(self) -> None:
        rows = []
        for n in [24.0, 48.0, 96.0]:
            rows.append(
                {
                    "mean_initial_nodes": n,
                    "mean_final_radius_control": n,
                    "mean_avg_local_overlap": 0.8,
                    "quasi_score": 0.7,
                    "mean_abs_delta_beta1": 1.0,
                }
            )
        metrics = v09.fit_scale_metrics(rows)
        self.assertAlmostEqual(metrics["radius_alpha"], 1.0, delta=0.05)


if __name__ == "__main__":
    unittest.main()
