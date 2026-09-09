"""UC2 runner regressions on tiny temporary protocols, never research runs."""
from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Tools import run_local_change_candidate as runner
from Tools.local_change_candidate import component_partition, make_state


class PrueferWord:
    def __init__(self, word):
        self.values = iter(word)

    def randrange(self, _n):
        return next(self.values)


class ConstructionTests(unittest.TestCase):
    def test_all_pruefer_words_give_unique_connected_trees(self):
        for n in range(2, 6):
            trees = set()
            for word in itertools.product(range(n), repeat=n - 2):
                edges = runner.uniform_tree(n, PrueferWord(word))
                state = make_state(range(n), edges, [0])
                self.assertEqual(len(edges), n - 1)
                self.assertEqual(len(component_partition(state)), 1)
                trees.add(tuple(edges))
            self.assertEqual(len(trees), n ** (n - 2))

    def test_state_signature_excludes_counters_but_includes_unit_host(self):
        state = make_state(range(3), [(0, 1), (0, 2)], [0])
        initial = runner.signature(state)
        state.ticks = state.attempts = 7
        self.assertEqual(runner.signature(state), initial)
        state.units[0] = 1
        self.assertNotEqual(runner.signature(state), initial)


class RunnerEvidenceTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="uc2-runner-test-")
        self.addCleanup(directory.cleanup)
        self.out = Path(directory.name)
        spec = json.loads(runner.SPEC.read_text())
        spec["calibration"].update(replicates=8, steps=12)
        spec["candidate"].update(node_counts=[4, 5], replicates_per_size=2, steps=12)
        self.spec_path = self.out / "fixture_protocol.json"
        self.spec_path.write_text(json.dumps(spec))
        protocol_patch = patch.object(runner, "SPEC", self.spec_path)
        hash_patch = patch.object(runner, "source_hashes", self.fixture_hashes)
        protocol_patch.start()
        hash_patch.start()
        self.addCleanup(protocol_patch.stop)
        self.addCleanup(hash_patch.stop)
        self.calibration = runner.measure("calibration", self.out)
        self.assertTrue(self.calibration["reference_gate_pass"])

    def fixture_hashes(self):
        # A temporary protocol must never claim the tracked protocol's hash.
        return {
            "fixture_protocol.json": runner.digest(self.spec_path),
            "Tools/run_local_change_candidate.py": runner.digest(Path(runner.__file__)),
        }

    def record_path(self, stage="calibration"):
        return self.out / f"UC2_{stage}.json"

    def load_record(self, stage="calibration"):
        return json.loads(self.record_path(stage).read_text())

    def save_record(self, record, stage="calibration"):
        self.record_path(stage).write_text(json.dumps(record))

    def refresh_evidence_hash(self, name, stage="calibration"):
        record = self.load_record(stage)
        record["evidence_sha256"][name] = runner.digest(self.out / name)
        self.save_record(record, stage)

    def load_csv(self, name):
        with (self.out / name).open(newline="") as handle:
            return list(csv.DictReader(handle))

    def save_csv(self, name, rows):
        with (self.out / name).open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        self.refresh_evidence_hash(name)

    def test_tiny_calibration_and_candidate_seeded_replay(self):
        verified = runner.verify("calibration", self.out)
        self.assertEqual((verified["replayed_runs"], verified["replayed_changes"]), (16, 192))
        record = runner.measure("candidate", self.out)
        self.assertEqual(record["candidate_effect_gate"], "not_defined_descriptive_only")
        verified = runner.verify("candidate", self.out)
        self.assertEqual((verified["replayed_runs"], verified["replayed_changes"]), (4, 48))

    def test_forged_gate_and_aggregate_fields_are_recomputed(self):
        forged_values = {
            "positive_median": -1, "null_median": 2,
            "paired_signs": [-1] * 8, "one_sided_sign_score": 1,
            "squared_signs_identical": False, "reference_gate_pass": False,
        }
        for field, value in forged_values.items():
            with self.subTest(field=field):
                record = dict(self.calibration)
                record[field] = value
                self.save_record(record)
                with self.assertRaisesRegex(RuntimeError, "Reference gate/metrics"):
                    runner.verify("calibration", self.out)
        self.save_record(self.calibration)

    def test_initial_schedule_change_rejected_even_with_updated_hash(self):
        name = "UC2_calibration_initial.json"
        original = json.loads((self.out / name).read_text())
        for field, value in (("seed", -1), ("steps", 11), ("role", "null")):
            rows = json.loads(json.dumps(original))
            rows[0][field] = value
            (self.out / name).write_text(json.dumps(rows))
            self.refresh_evidence_hash(name)
            with self.subTest(field=field), self.assertRaisesRegex(RuntimeError, "run schedule"):
                runner.verify("calibration", self.out)

    def test_prior_small_off_protocol_fixture_no_longer_qualifies(self):
        # Change the expected workload, while preserving honest current hashes.
        spec = json.loads(self.spec_path.read_text())
        spec["calibration"]["steps"] = 13
        self.spec_path.write_text(json.dumps(spec))
        record = self.load_record()
        record["source_sha256"] = self.fixture_hashes()
        self.save_record(record)
        with self.assertRaisesRegex(RuntimeError, "run schedule"):
            runner.verify("calibration", self.out)

    def test_duplicate_summary_run_ids_rejected(self):
        name = "UC2_calibration_summary.csv"
        rows = self.load_csv(name)
        rows[-1] = dict(rows[0])
        self.save_csv(name, rows)
        with self.assertRaisesRegex(RuntimeError, "Summary run IDs"):
            runner.verify("calibration", self.out)

    def test_summary_state_counts_recomputed(self):
        name = "UC2_calibration_summary.csv"
        rows = self.load_csv(name)
        rows[0]["distinct_observed_states"] = 999
        self.save_csv(name, rows)
        with self.assertRaisesRegex(RuntimeError, "Trace/summary"):
            runner.verify("calibration", self.out)

    def test_legal_alternative_null_move_rejected_by_seeded_replay(self):
        name = "UC2_calibration_events.csv"
        rows = self.load_csv(name)
        first_null = next(row for row in rows if row["run_id"] == "null-0")
        # Both ordered neighbor choices are legal on the initial three-node tree.
        first_null["target"], first_null["carried"] = first_null["carried"], first_null["target"]
        self.save_csv(name, rows)
        with self.assertRaisesRegex(RuntimeError, "seeded preregistered dynamics"):
            runner.verify("calibration", self.out)

    def test_missing_evidence_hash_rejected(self):
        record = self.load_record()
        del record["evidence_sha256"]["UC2_calibration_events.csv"]
        self.save_record(record)
        with self.assertRaises(RuntimeError):
            runner.verify("calibration", self.out)

    def test_stale_sources_and_evidence_fail(self):
        record = self.load_record()
        record["source_sha256"]["fixture_protocol.json"] = "wrong"
        self.save_record(record)
        with self.assertRaisesRegex(RuntimeError, "Source/protocol hash"):
            runner.verify("calibration", self.out)
        self.save_record(self.calibration)
        events = self.out / "UC2_calibration_events.csv"
        events.write_text(events.read_text() + "\n")
        with self.assertRaisesRegex(RuntimeError, "Evidence hash"):
            runner.verify("calibration", self.out)

    def test_failed_references_block_candidate_before_output(self):
        record = self.load_record()
        record["reference_gate_pass"] = False
        self.save_record(record)
        with self.assertRaisesRegex(RuntimeError, "stale or unqualified"):
            runner.measure("candidate", self.out)
        self.assertFalse((self.out / "UC2_candidate_events.csv").exists())

    def test_forged_pass_with_wrong_metrics_blocks_candidate(self):
        record = self.load_record()
        record["positive_median"] = 0
        self.save_record(record)
        with self.assertRaisesRegex(RuntimeError, "Reference gate/metrics"):
            runner.measure("candidate", self.out)
        self.assertFalse((self.out / "UC2_candidate_events.csv").exists())

    def test_candidate_rejects_changed_calibration_record(self):
        runner.measure("candidate", self.out)
        record = self.load_record()
        record["claim_limit"] += " Changed record."
        self.save_record(record)
        with self.assertRaises(RuntimeError):
            runner.verify("candidate", self.out)

    def test_candidate_rechecks_referenced_calibration_evidence(self):
        runner.measure("candidate", self.out)
        events = self.out / "UC2_calibration_events.csv"
        events.write_text(events.read_text() + "\n")
        with self.assertRaisesRegex(RuntimeError, "Evidence hash"):
            runner.verify("candidate", self.out)


if __name__ == "__main__":
    unittest.main()
