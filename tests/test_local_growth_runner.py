"""UC3 runner regressions: tiny procedural fixtures, not registered research runs."""
from __future__ import annotations

import copy
import csv
import itertools
import json
from pathlib import Path
import random
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Tools import run_local_growth_candidate as runner

kernel = runner.kernel


class RowCollector:
    def __init__(self):
        self.rows = []

    def writerow(self, row):
        self.rows.append(copy.deepcopy(row))


def enumerated_dyck(n, interval, minimum):
    """Independent brute-force oracle, used only for n <= 5."""
    words = []
    for ups in itertools.combinations(range(2 * n), n):
        ups = set(ups)
        height, reached = 0, minimum == 0
        word = []
        for step in range(2 * n):
            kind = "bud" if step in ups else "collapse"
            height += 1 if kind == "bud" else -1
            if height < 0:
                break
            reached |= (step + 1) % interval == 0 and height >= minimum
            word.append(kind)
        else:
            if reached:
                words.append(word)
    return words


class DyckTests(unittest.TestCase):
    def test_exact_small_counts_match_independent_enumeration(self):
        catalan = [1, 2, 5, 14, 42]
        for n in range(1, 6):
            self.assertEqual(runner.dyck_completions(0, 0, False, n, 1, 0), catalan[n - 1])
            for interval in (1, 2, 3):
                for minimum in range(n + 2):
                    with self.subTest(n=n, interval=interval, minimum=minimum):
                        expected = enumerated_dyck(n, interval, minimum)
                        self.assertEqual(
                            runner.dyck_completions(0, 0, False, n, interval, minimum),
                            len(expected),
                        )

    def test_every_conditional_word_has_exact_uniform_branch_counts(self):
        # Verify every branch's integer sampling range against enumerated
        # suffixes, not against the implementation's own completion function.
        words = enumerated_dyck(5, 2, 2)
        case = self

        class WordRng:
            def __init__(self, wanted):
                self.wanted = wanted
                self.prefix = []

            def randrange(self, stop):
                candidates = [w for w in words if w[:len(self.prefix)] == self.prefix]
                up_count = sum(w[len(self.prefix)] == "bud" for w in candidates)
                case.assertEqual(stop, len(candidates))
                kind = self.wanted[len(self.prefix)]
                self.prefix.append(kind)
                return 0 if kind == "bud" else up_count

        for word in words:
            self.assertEqual(runner.dyck_word(5, WordRng(word), 2, 2), word)

    def test_observed_not_hidden_peak_and_invalid_parameters(self):
        # UUDD reaches height two, but it is invisible at an interval of four.
        self.assertEqual(runner.dyck_completions(0, 0, False, 2, 4, 2), 0)
        for args in ((2, 4, 2), (0, 1, 0), (True, 1, 0), (2, 0, 0), (2, 1, -1)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                runner.dyck_word(args[0], random.Random(7), args[1], args[2])


class ExposureTests(unittest.TestCase):
    settings = dict(lag=8, min_nodes=4, min_core_nodes=4,
                    size_tolerance=.1, shape_tolerance=.05,
                    excursion_ratio=1.5, turnover_min=.25)

    def apply(self, observer, state, tag, kind, target):
        before = kernel.clone_state(state)
        event = kernel.apply_event(state, tag, kind, target)
        split = runner.check_transition(before, state, event)
        observer.advance(before, state, event, split)
        return event

    def fan_with_unrelated_events(self, insert_unrelated):
        state = kernel.make_state(
            [0, 1, 2, 3, 100, 101],
            [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3), (100, 101)],
            [1, 3, 100],
        )
        observer = runner.ExposureObserver(state, 1)
        for kind in (["bud"] * 4 + ["collapse"] * 4) * 4:
            if insert_unrelated:
                self.apply(observer, state, 2, "bud", 101)
                self.apply(observer, state, 2, "collapse", 100)
            if kind == "bud":
                self.apply(observer, state, 1, kind, 0)
            else:
                target = next(v for v in state.adjacency[state.units[0]] if v != 0)
                self.apply(observer, state, 0, kind, target)
        return observer, observer.result(self.settings)

    def test_unrelated_component_events_do_not_change_tag_scores_or_clocks(self):
        baseline, base_result = self.fan_with_unrelated_events(False)
        inserted, inserted_result = self.fan_with_unrelated_events(True)
        self.assertEqual(baseline.clocks, [32, 32, 0])
        self.assertEqual(inserted.clocks, [32, 32, 64])
        self.assertEqual(base_result["per_unit"][:2], inserted_result["per_unit"][:2])
        self.assertEqual(base_result["per_unit"][0]["fraction"], 1)
        # Absolute attempt/global times differ legitimately; local phase,
        # replacement and event attribution must be unchanged even though
        # unrelated births also change subsequent allocated node IDs.
        diagnostics = {"start_global_tick", "end_global_tick", "start_attempt", "end_attempt"}
        strip = lambda rows: [{k: v for k, v in row.items() if k not in diagnostics}
                              for row in rows if row["unit_index"] < 2]
        self.assertEqual(strip(base_result["qualifying_intervals"]),
                         strip(inserted_result["qualifying_intervals"]))
        self.assertGreater(inserted.metadata[0][-1]["global_tick"],
                           baseline.metadata[0][-1]["global_tick"])

    def test_cut_counts_once_for_both_descendants_then_clocks_separate(self):
        state = kernel.make_state(range(4), [(0, 1), (1, 2), (2, 3)], [0, 1, 2, 3])
        observer = runner.ExposureObserver(state, 1)
        self.apply(observer, state, 1, "cut", 2)
        self.assertEqual(observer.clocks, [1, 1, 1, 1])
        for counts in observer.counts:
            self.assertEqual((counts["cut"], counts["split"]), (1, 1))
        self.assertEqual(observer.histories[0][-1]["regions"][0]["nodes"], [0, 1])
        self.assertEqual(observer.histories[1][-1]["regions"][0]["nodes"], [2, 3])
        self.apply(observer, state, 0, "bud", 1)
        self.assertEqual(observer.clocks, [2, 1, 1, 1])
        self.assertEqual([len(h) for h in observer.histories], [3, 2, 2, 2])
        self.assertEqual([c["bud"] for c in observer.counts], [1, 0, 0, 0])
        # Collapse deletes the observer's host, not its persistent tag/history.
        self.apply(observer, state, 0, "collapse", 0)
        self.assertEqual(observer.clocks, [3, 1, 1, 1])
        self.assertEqual(observer.histories[0][-1]["regions"][0]["nodes"], [0, 1])

    def test_observer_on_off_preserves_state_events_and_rng(self):
        job = dict(run_id="fixture", role="candidate", n=8, units=2, interval=1, seed=47)
        states, rngs = [], []
        for _ in range(2):
            state, rng, _ = runner.initialize(job)
            states.append(state)
            rngs.append(rng)
        initial = kernel.state_snapshot(states[0])
        emitted = []
        observer = runner.ExposureObserver(states[0], 1, emitted.append)
        self.assertEqual(kernel.state_snapshot(states[0]), initial)
        accepted = 0
        for _ in range(64):
            before = kernel.clone_state(states[0])
            observed = kernel.attempt_step(states[0], rngs[0])
            unobserved = kernel.attempt_step(states[1], rngs[1])
            self.assertEqual(observed, unobserved)
            accepted += observed.changed
            split = runner.check_transition(before, states[0], observed)
            old_clocks = list(observer.clocks)
            observer.advance(before, states[0], observed, split)
            if not observed.changed:
                self.assertEqual(observer.clocks, old_clocks)
            self.assertEqual(kernel.state_snapshot(states[0]), kernel.state_snapshot(states[1]))
            self.assertEqual(rngs[0].getstate(), rngs[1].getstate())
        self.assertGreater(accepted, 0)
        observer.result(self.settings)
        self.assertEqual(kernel.state_snapshot(states[0]), kernel.state_snapshot(states[1]))
        self.assertEqual(rngs[0].getstate(), rngs[1].getstate())
        self.assertTrue(emitted)


class RunCaseBudgetTests(unittest.TestCase):
    def fixture_spec(self):
        spec = json.loads(runner.SPEC.read_text())
        spec["candidate"].update(max_attempts=7, max_changes=3, node_cap=16)
        return spec

    def run_state(self, state, rng, spec):
        job = dict(run_id="budget-fixture", role="candidate", n=len(state.adjacency),
                   units=len(state.units), interval=1, seed=0)
        events, frames = RowCollector(), RowCollector()
        with patch.object(runner, "initialize", return_value=(state, rng, dict(job))):
            _, summary, detail = runner.run_case(job, spec, events, frames)
        return summary, detail, events.rows, frames.rows

    def test_blocked_class_uses_attempt_budget_without_retry_or_exposure(self):
        class BlockedCollapseRng:
            draws = 0

            def randrange(self, stop):
                self.draws += 1
                return 5 if stop == 8 else 0

        state = kernel.make_state(range(4), [(0, 1), (1, 2), (2, 3)], [0])
        rng = BlockedCollapseRng()
        summary, _, events, frames = self.run_state(state, rng, self.fixture_spec())
        self.assertEqual((summary["stop"], summary["attempts"], summary["ticks"]),
                         ("attempt_budget", 7, 0))
        self.assertEqual(summary["blocked_collapse"], 7)
        self.assertEqual(summary["integrated_expected_node_drift"], 7 / 8)
        self.assertEqual(rng.draws, 14)  # one unit and one class draw per attempt
        self.assertEqual([row["attempt"] for row in events], list(range(1, 8)))
        self.assertTrue(all(not row["changed"] and row["tick"] == 0 for row in events))
        self.assertEqual(len(frames), 1)
        self.assertEqual(summary["max_component_exposures"], 0)

    def test_node_cap_censors_births_instead_of_disabling_the_birth_class(self):
        class BudRng:
            def randrange(self, stop):
                return 4 if stop == 8 else 0

        for cap, expected_changes, stop in ((4, 2, "node_cap_censored"), (16, 3, "change_budget")):
            with self.subTest(cap=cap):
                state = kernel.make_state(range(2), [(0, 1)], [0])
                spec = self.fixture_spec()
                spec["candidate"]["node_cap"] = cap
                summary, _, events, _ = self.run_state(state, BudRng(), spec)
                self.assertEqual((summary["stop"], summary["ticks"], summary["attempts"]),
                                 (stop, expected_changes, expected_changes))
                self.assertEqual(summary["final_N"], 2 + expected_changes)
                self.assertEqual(summary["bud"], expected_changes)
                self.assertEqual(len(events), expected_changes)

    def test_activity_absorption_does_not_require_all_graph_nodes_isolated(self):
        state = kernel.make_state(range(4), [(1, 2), (2, 3), (1, 3)], [0])
        summary, _, events, frames = self.run_state(state, random.Random(7), self.fixture_spec())
        self.assertEqual(summary["stop"], "activity_absorbed")
        self.assertEqual((summary["final_N"], summary["final_E"], summary["final_C"]), (4, 3, 2))
        self.assertEqual((summary["attempts"], summary["ticks"]), (0, 0))
        self.assertEqual(events, [])
        self.assertEqual(len(frames), 1)


class RunnerEvidenceTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="uc3-runner-test-")
        self.addCleanup(directory.cleanup)
        self.out = Path(directory.name)
        spec = json.loads(runner.SPEC.read_text())
        spec["calibration"].update(node_count=4, replicates=8, periods=4,
                                   buds_per_period=4, snapshot_interval=1,
                                   null_observed_height_min=2, seed_start=101)
        spec["observer"].update(lag=8, min_nodes=4, min_core_nodes=4)
        spec["candidate"].update(node_counts=[4, 8], replicates_per_size=2,
                                 max_attempts=24, max_changes=12, node_cap=32,
                                 seed_start=201)
        self.spec_path = self.out / "fixture_protocol.json"
        self.spec_path.write_text(json.dumps(spec))
        protocol_patch = patch.object(runner, "SPEC", self.spec_path)
        protocol_patch.start()
        self.addCleanup(protocol_patch.stop)
        # source_hashes reads the patched SPEC itself: this evidence explicitly
        # binds the temporary protocol, never the registered UC3 workload.
        self.spec = spec
        self.calibration = runner.measure("calibration", self.out)
        self.assertTrue(self.calibration["reference_gate_pass"])
        self.assertEqual(self.calibration["source_sha256"]["preregistration"],
                         runner.digest(self.spec_path))

    def path(self, suffix=".json", stage="calibration"):
        return self.out / ("UC3_" + stage + suffix)

    def record(self, stage="calibration"):
        return json.loads(self.path(stage=stage).read_text())

    def save_record(self, record, stage="calibration"):
        self.path(stage=stage).write_text(json.dumps(record))

    def rehash(self, suffix, stage="calibration"):
        record = self.record(stage)
        path = self.path(suffix, stage)
        record["evidence_sha256"][path.name] = runner.digest(path)
        self.save_record(record, stage)

    def edit_csv(self, suffix, mutate, stage="calibration"):
        path = self.path(suffix, stage)
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            fields, rows = reader.fieldnames, list(reader)
        mutate(rows)
        with path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        self.rehash(suffix, stage)

    def assert_no_candidate_output(self):
        self.assertFalse(any(self.path(suffix, "candidate").exists()
                             for suffix in (".json", *runner.SUFFIXES)))

    def test_tiny_calibration_and_candidate_replay_all_products(self):
        verified = runner.verify("calibration", self.out)
        self.assertEqual((verified["replayed_runs"], verified["replayed_changes"]), (16, 512))
        self.assertTrue(verified["all_products_match"])
        record = runner.measure("candidate", self.out)
        self.assertEqual(record["candidate_effect_gate"], "not_defined_descriptive_only")
        verified = runner.verify("candidate", self.out)
        self.assertEqual(verified["replayed_runs"], 4)
        self.assertLessEqual(verified["replayed_attempts"], 96)
        self.assertTrue(verified["all_products_match"])

    def test_measure_never_overwrites_any_existing_product(self):
        original = {p.name: p.read_bytes() for p in self.out.iterdir() if p.is_file()}
        with self.assertRaises(FileExistsError):
            runner.measure("calibration", self.out)
        self.assertEqual(original, {p.name: p.read_bytes() for p in self.out.iterdir() if p.is_file()})
        for suffix in (".json", *runner.SUFFIXES):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory(prefix="uc3-overwrite-test-") as tmp:
                out = Path(tmp)
                sentinel = out / ("UC3_calibration" + suffix)
                sentinel.write_bytes(b"existing evidence\n")
                with self.assertRaises(FileExistsError):
                    runner.measure("calibration", out)
                self.assertEqual(sentinel.read_bytes(), b"existing evidence\n")
                self.assertEqual(list(out.iterdir()), [sentinel])

    def test_rehashed_summary_trace_frames_and_observations_are_rejected(self):
        for suffix in ("_summary.csv", "_events.csv", "_frames.csv", "_observations.json"):
            with self.subTest(suffix=suffix):
                path, old_record = self.path(suffix), self.record()
                original = path.read_bytes()
                if suffix == "_summary.csv":
                    self.edit_csv(suffix, lambda rows: rows[0].update(final_N=999))
                elif suffix == "_events.csv":
                    self.edit_csv(suffix, lambda rows: rows[0].update(target=999))
                elif suffix == "_frames.csv":
                    self.edit_csv(suffix, lambda rows: rows[0].update(local_tick=999))
                else:
                    rows = json.loads(path.read_text())
                    rows[0]["primary"] = -1
                    path.write_text(json.dumps(rows))
                    self.rehash(suffix)
                with self.assertRaisesRegex(RuntimeError, "Seeded replay"):
                    runner.verify("calibration", self.out)
                path.write_bytes(original)
                self.save_record(old_record)

    def test_rehashed_initial_seed_and_duplicate_summary_schedule_rejected(self):
        path = self.path("_initial.json")
        original, original_record = path.read_bytes(), self.record()
        initial = json.loads(path.read_text())
        initial[0]["seed"] += 1
        path.write_text(json.dumps(initial))
        self.rehash("_initial.json")
        with self.assertRaisesRegex(RuntimeError, "Seeded replay"):
            runner.verify("calibration", self.out)
        # Independent second mutation on another evidence product.
        path.write_bytes(original)
        self.save_record(original_record)
        self.edit_csv("_summary.csv", lambda rows: rows.__setitem__(-1, dict(rows[0])))
        with self.assertRaisesRegex(RuntimeError, "Seeded replay"):
            runner.verify("calibration", self.out)

    def test_changed_protocol_schedule_rejected_even_with_current_source_hash(self):
        spec = copy.deepcopy(self.spec)
        spec["calibration"]["periods"] += 1
        self.spec_path.write_text(json.dumps(spec))
        record = self.record()
        record["source_sha256"] = runner.source_hashes()
        self.save_record(record)
        with self.assertRaisesRegex(RuntimeError, "Seeded replay"):
            runner.verify("calibration", self.out)

    def test_forged_gate_and_aggregate_fields_are_recomputed(self):
        for field, value in {
            "reference_gate_pass": False, "positive_median": -1,
            "null_median": 2, "paired_signs": [-1] * 8,
            "one_sided_sign_score": 1, "squared_signs_identical": False,
            "conditional_dyck_words": -1, "total_attempts": -1,
        }.items():
            with self.subTest(field=field):
                record = copy.deepcopy(self.calibration)
                record[field] = value
                self.save_record(record)
                with self.assertRaisesRegex(RuntimeError, "Seeded replay"):
                    runner.verify("calibration", self.out)
        self.save_record(self.calibration)

    def test_stale_source_evidence_and_manifest_fail_closed(self):
        record = self.record()
        record["source_sha256"]["preregistration"] = "wrong"
        self.save_record(record)
        with self.assertRaisesRegex(RuntimeError, "stale source/protocol"):
            runner.verify("calibration", self.out)
        self.save_record(self.calibration)
        record = self.record()
        del record["evidence_sha256"][self.path("_events.csv").name]
        self.save_record(record)
        with self.assertRaisesRegex(RuntimeError, "manifest"):
            runner.verify("calibration", self.out)
        self.save_record(self.calibration)
        events = self.path("_events.csv")
        events.write_bytes(events.read_bytes() + b"\n")
        with self.assertRaisesRegex(RuntimeError, "checksum"):
            runner.verify("calibration", self.out)

    def test_missing_and_forged_references_block_before_candidate_output(self):
        with tempfile.TemporaryDirectory(prefix="uc3-no-reference-test-") as tmp:
            out = Path(tmp)
            with self.assertRaises(FileNotFoundError):
                runner.measure("candidate", out)
            self.assertEqual(list(out.iterdir()), [])
        record = self.record()
        record["positive_median"] = -1
        self.save_record(record)
        with self.assertRaisesRegex(RuntimeError, "Seeded replay"):
            runner.measure("candidate", self.out)
        self.assert_no_candidate_output()

    def test_genuine_failed_reference_gate_blocks_candidate(self):
        # One pair cannot qualify the <= .05 sign gate. This is an honest
        # failed temporary calibration, not merely a flipped stored boolean.
        spec = copy.deepcopy(self.spec)
        spec["calibration"]["replicates"] = 1
        self.spec_path.write_text(json.dumps(spec))
        with tempfile.TemporaryDirectory(prefix="uc3-failed-reference-test-") as tmp:
            out = Path(tmp)
            record = runner.measure("calibration", out)
            self.assertFalse(record["reference_gate_pass"])
            self.assertTrue(runner.verify("calibration", out)["all_products_match"])
            with self.assertRaisesRegex(RuntimeError, "Reference gate failed"):
                runner.measure("candidate", out)
            self.assertFalse(any(p.name.startswith("UC3_candidate") for p in out.iterdir()))

    def test_candidate_binds_reference_record_and_recursively_checks_raw_evidence(self):
        runner.measure("candidate", self.out)
        record = self.record("candidate")
        record["calibration_sha256"] = "wrong"
        self.save_record(record, "candidate")
        with self.assertRaisesRegex(RuntimeError, "Seeded replay"):
            runner.verify("candidate", self.out)
        record["calibration_sha256"] = runner.digest(self.path())
        self.save_record(record, "candidate")
        self.edit_csv("_events.csv", lambda rows: rows[0].update(target=999))
        with self.assertRaisesRegex(RuntimeError, "Seeded replay"):
            runner.verify("candidate", self.out)


if __name__ == "__main__":
    unittest.main()
