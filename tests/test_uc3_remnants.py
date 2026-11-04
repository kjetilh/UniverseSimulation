"""Small specified event sequences, not sampled runs or effect references."""
import unittest

from Tools.observe_uc3_remnants import Replay


def branched():
    # The two new triangles are connected by a chain; its internal nodes
    # also belong to the 2-core until the bridge is cut.
    r = Replay(dict(run_id="fixture", nodes=list(range(6)),
                    edges=[(i, i+1) for i in range(5)], unit_hosts=[0, 4, 2, 1]))
    r.step(0, "bud", 1)    # left triangle on (0,1), newborn 6
    r.step(1, "bud", 5)    # right triangle on (4,5), newborn 7
    r.step(2, "cut", 3)
    return r


class RemnantTests(unittest.TestCase):
    def test_split_and_delayed_renewal(self):
        r = branched()
        row = r.tag_rows()[0]
        self.assertEqual((row["peak_tick"], row["peak_core"], row["loss_tick"], row["loss_core"]),
                         (2, 8, 3, 3))
        self.assertTrue(row["loss_split"])
        self.assertEqual(row["retained_edges"], 4)
        self.assertEqual(row["followup_edits"], 0)
        r.step(0, "bud", 0)   # (6,0,born tick 1); K from 3 to 4
        self.assertIsNone(r.tag_rows()[0]["joint_growth_tick"])
        r.step(0, "bud", 0)   # newly added (8,0), no hit; K reaches 5
        row = r.tag_rows()[0]
        self.assertEqual((row["post_initial_hit_tick"],row["joint_growth_tick"]), (4,5))
        self.assertEqual([(b["incident_R"],b["degree"],b["hit"]) for b in r.buds
                          if b["unit_index"] == 0], [(2,2,True),(0,2,False)])
        self.assertEqual(r.tag_rows()[1]["followup_edits"],0)

    def test_recreation_is_not_survival(self):
        r = branched()
        r.step(0, "cut", 0)          # destroy the prior (6,0)
        r.step(3, "slide", 0, 6)     # recreate (0,6) through node 1
        r.step(0, "bud", 6)
        bud = next(b for b in r.buds if b["unit_index"] == 0)
        self.assertEqual((bud["source"],bud["anchor"],bud["edge_birth_tick"]), (0,6,5))
        self.assertFalse(bud["hit"])
        self.assertEqual((bud["incident_R"],bud["degree"]), (1,2))

    def test_living_remnant_outside_current_core(self):
        r = branched()
        r.step(3, "bud", 2)   # (1,2) was in the peak core; now a pendant edge
        bud = next(b for b in r.buds if b["unit_index"] == 0)
        self.assertTrue(bud["hit"])
        self.assertEqual(bud["edge_birth_tick"],0)
        self.assertIsNone(r.tag_rows()[0]["post_initial_hit_tick"])

    def test_window_and_no_opportunity(self):
        r = branched()
        for _ in range(17):
            r.step(0, "bud", 0)
        left,right = r.tag_rows()[:2]
        self.assertEqual((left["seen_edits"],left["followup_edits"],left["followup_end_tick"]), (20,16,19))
        self.assertEqual((right["stage"],right["followup_edits"]), ("no_bud",0))
        self.assertFalse(any(b["tick"]==20 for b in r.buds))

    def test_missing_episode_not_a_zero_hit_episode(self):
        r = Replay(dict(run_id="tree",nodes=[0,1],edges=[(0,1)],unit_hosts=[0]))
        r.step(0,"bud",1)
        self.assertEqual(r.tag_rows()[0]["stage"],"no_peak")
        r.step(0,"bud",1)
        self.assertEqual(r.tag_rows()[0]["stage"],"no_loss")
        self.assertIsNone(r.tag_rows()[0]["loss_tick"])
