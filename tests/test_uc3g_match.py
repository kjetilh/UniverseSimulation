from collections import Counter
import unittest

from Tools import local_growth_candidate as law
from Tools import uc3g_match as matches
from Tools.local_growth_observer import _region


def brute(state, tag):
    """Independent enumeration through the real transition dispatcher."""
    nodes = matches.component(state.adjacency, state.units[tag])
    rows = []
    for i, host in enumerate(state.units):
        if host not in nodes:
            continue
        cuts = Counter()
        sizes = {kind: Counter() for kind in ("slide", "bud", "collapse")}
        for kind in law.CLASSES:
            if kind == "slide":
                moves = law.admissible_moves(state, i)
            else:
                moves = [(v, None) for v in state.adjacency[host]]
            for target, carried in moves:
                after = law.clone_state(state)
                try:
                    law.apply_event(after, i, kind, target, carried)
                except ValueError:
                    if kind != "collapse":
                        raise
                    continue
                part = matches.component(after.adjacency, after.units[tag])
                k = len(_region(after.adjacency, part)["core_nodes"])
                if kind == "cut":
                    cuts[(part != nodes, k)] += 1
                else:
                    sizes[kind][k] += 1
        rows.append(dict(unit=i, degree=len(state.adjacency[host]),
                         slide_choices=sum(sizes["slide"].values()),
                         collapse_choices=sum(sizes["collapse"].values()),
                         bud_core=sorted(sizes["bud"].items()),
                         slide_core=sorted(sizes["slide"].items()),
                         collapse_core=sorted(sizes["collapse"].items()),
                         cut_split_core=sorted(cuts.items())))
    return rows


class TestMatchedOpportunity(unittest.TestCase):
    def test_branch_selects_replayable_nonisomorphic_pair_without_mutating_input(self):
        state = law.make_state(range(8), [(0, 1), (0, 2), (0, 3), (3, 4), (4, 5), (6, 7)],
                               [0, 6])
        before = law.state_snapshot(state)
        left, right, audit = matches.find_match(state, 0, [(3, 0, 34)])
        self.assertEqual(law.state_snapshot(state), before)
        self.assertEqual(law.component_partition(left), law.component_partition(state))
        self.assertEqual(left.units, right.units)
        self.assertEqual([len(v) for v in left.adjacency.values()],
                         [len(v) for v in right.adjacency.values()])
        self.assertIn((0, 3), law.edge_set(left))
        self.assertNotIn((0, 3), law.edge_set(right))
        self.assertNotEqual(audit["nonisomorphism"]["preserved"], audit["nonisomorphism"]["rewired"])
        for arm, key in ((left, "preserved_event"), (right, "rewired_event")):
            event = audit[key]
            replay = law.clone_state(state)
            law.apply_event(replay, event["unit_index"], event["kind"], event["target"], event["carried"])
            self.assertEqual(law.state_snapshot(replay), law.state_snapshot(arm))
            self.assertEqual(brute(arm, 0), audit["opportunities"])

    def test_pure_permutation_and_missing_candidates_are_rejected(self):
        symmetric = law.make_state(range(4), [(0, 1), (0, 2), (0, 3)], [0])
        self.assertIsNone(matches.find_match(symmetric, 0, [(0, 3)]))
        self.assertIsNone(matches.find_match(symmetric, 0, []))
        self.assertIsNone(matches.find_match(symmetric, 0, law.edge_set(symmetric)))
        with self.assertRaises(ValueError):
            matches.find_match(symmetric, 0, [(1, 2)])

    def test_all_class_histograms_against_kernel_on_cycles_and_branches(self):
        state = law.make_state(range(10),
                               [(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (4, 5),
                                (3, 5), (3, 6), (6, 7), (8, 9)], [3, 3, 6, 1, 8])
        before = law.state_snapshot(state)
        for tag in range(len(state.units)):
            self.assertEqual(matches.opportunity_signature(state, tag), brute(state, tag))
        self.assertEqual(law.state_snapshot(state), before)
        scores = matches.opportunity_signature(state, 0)
        self.assertIn(((True, 0), 1), scores[0]["cut_split_core"])
        self.assertNotEqual(scores[0]["cut_split_core"], scores[1]["cut_split_core"])
        self.assertEqual(scores[3]["collapse_choices"], 2)


if __name__ == "__main__":
    unittest.main()
