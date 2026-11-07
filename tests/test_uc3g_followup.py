import hashlib
import json
import unittest
from unittest.mock import patch

from Tools import local_growth_candidate as kernel
from Tools import uc3g_followup as runner


class TestFollowup(unittest.TestCase):
    def test_positive_starts_after_setup_and_requires_two_core_nodes(self):
        state = kernel.make_state(range(3), [(0, 1), (1, 2), (0, 2)], [0])
        state.ticks, state.attempts = 41, 99
        before = kernel.state_snapshot(state)
        result = runner.follow(state, 0, 19, "positive")
        self.assertEqual((3, 5, 2, 2, 2, "hit"),
                         (result["k_start"], result["k_final"], result["first_hit"],
                          result["exposure"], result["attempts"], result["stop"]))
        self.assertEqual(before, kernel.state_snapshot(state))
        self.assertEqual(result, runner.follow(state, 0, 19, "positive"))

    def test_null_reverses_one_setup_slide_then_repeats_to_the_window(self):
        state = kernel.make_state(range(4), [(0, 1), (1, 2), (0, 2), (0, 3)], [0])
        setup = dict(unit_index=0, source=0, target=1, carried=3)
        kernel.apply_event(state, 0, "slide", 1, 3)
        result = runner.follow(state, 0, 1, "null", setup)
        self.assertEqual((False, None, 16, 16, "window", 3),
                         (result["success"], result["first_hit"], result["exposure"],
                          result["attempts"], result["stop"], result["k_final"]))
        trace = hashlib.sha256()
        for tick in range(1, 17):
            source = tick % 2
            row = [tick, tick, True, "slide", 0, source, 1 - source, 3, None, None, "slide", 3]
            trace.update((json.dumps(row, separators=(",", ":")) + "\n").encode("ascii"))
        self.assertEqual(trace.hexdigest(), result["trace_sha256"])

    def test_split_counts_once_and_follows_only_the_tag(self):
        state = kernel.make_state(range(5), [(0, 1), (1, 2), (0, 2), (2, 3), (3, 4)], [4, 3, 0])
        def detach_tag(local, rng):
            return kernel.apply_event(local, 1, "cut", 4)
        with patch.object(kernel, "attempt_step", side_effect=detach_tag):
            result = runner.follow(state, 0, 112)
        self.assertEqual((1, 1, 3, 0, "absorbed", False),
                         (result["exposure"], result["attempts"], result["k_start"],
                          result["k_final"], result["stop"], result["censored"]))

    def test_adding_disconnected_activity_has_no_effect(self):
        edges = [(0, 1), (1, 2)]
        active = kernel.make_state(range(3), edges, [0, 1], next_node_id=8)
        whole = kernel.make_state(range(6), edges + [(3, 4), (4, 5), (3, 5)],
                                  [0, 1, 3, 4], next_node_id=8)
        self.assertEqual(runner.follow(active, 1, 711), runner.follow(whole, 1, 711))

    def test_blocked_attempt_is_not_exposure_or_a_completed_zero(self):
        state = kernel.make_state(range(2), [(0, 1)], [0])
        attempt = kernel.attempt_step
        with patch.object(runner, "ATTEMPT_CAP", 1), patch.object(
            kernel, "attempt_step", side_effect=lambda s, rng: attempt(s, rng, weights=(1, 0, 0, 0))
        ):
            result = runner.follow(state, 0, 19)
        self.assertEqual(("attempt_cap", 1, 0, None, True),
                         (result["stop"], result["attempts"], result["exposure"],
                          result["first_hit"], result["censored"]))


if __name__ == "__main__":
    unittest.main()
