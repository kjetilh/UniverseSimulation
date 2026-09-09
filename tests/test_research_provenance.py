"""Bounded tests for explicit provenance validation and source-byte identity."""
import copy
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from Tools.build_research_provenance import build


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        self.root.mkdir()
        (self.root / "rule.md").write_text("# Rule\nA relation changes locally.\n", encoding="utf-8")
        (self.root / "code.py").write_bytes(b"# implementation fixture\n")
        self.manifest = {"schema_version": 1, "title": "Fixture provenance",
                         "nodes": [{"id": "rule:local", "kind": "user_rule", "status": "planned",
                                    "source": "rule.md", "anchor": "rule"},
                                   {"id": "code:kernel", "kind": "code", "status": "verified",
                                    "source": "code.py"}],
                         "edges": [{"source": "code:kernel", "target": "rule:local",
                                    "relation": "implements"}]}

    def build(self, manifest=None):
        return build(self.manifest if manifest is None else manifest, self.root, "2026-09-10")

    def test_hashes_status_date_and_anchor_are_explicit(self):
        result = self.build()
        rows = list(csv.DictReader(io.StringIO(result["nodes_csv"])))
        self.assertEqual([row["id"] for row in rows], ["code:kernel", "rule:local"])
        self.assertEqual(rows[1]["sha256"], hashlib.sha256((self.root / "rule.md").read_bytes()).hexdigest())
        self.assertEqual(rows[1]["source"], "rule.md")
        self.assertEqual(rows[1]["anchor"], "rule")
        self.assertEqual(rows[1]["date"], "2026-09-10")
        self.assertEqual(rows[1]["status"], "planned")
        edge = list(csv.DictReader(io.StringIO(result["edges_csv"])))[0]
        self.assertEqual(edge["source_sha256"], rows[0]["sha256"])
        self.assertEqual(edge["target_status"], "planned")
        self.assertIn("not verified scientific conclusions", result["markdown"])
        self.assertIn("anchors are unverified", result["markdown"])

    def test_deterministic_and_manifest_order_independent(self):
        other = copy.deepcopy(self.manifest)
        other["nodes"].reverse()
        self.assertEqual(self.build(), self.build(other))
        self.assertEqual(self.build(), self.build())

    def test_source_change_changes_hash(self):
        before = self.build()
        (self.root / "code.py").write_bytes(b"# changed implementation\n")
        self.assertNotEqual(before["nodes_csv"], self.build()["nodes_csv"])
        self.assertNotEqual(before["edges_csv"], self.build()["edges_csv"])

    def test_absolute_traversal_and_noncanonical_paths_rejected(self):
        for path in (str(self.root / "rule.md"), "../repo/rule.md", "sub/../rule.md",
                     "./rule.md", "sub//rule.md", "C:/rule.md", "sub\\rule.md", ""):
            with self.subTest(path=path):
                manifest = copy.deepcopy(self.manifest)
                manifest["nodes"][0]["source"] = path
                with self.assertRaises(ValueError):
                    self.build(manifest)

    def test_outside_root_symlink_rejected(self):
        outside = Path(self.temporary.name) / "outside.md"
        outside.write_text("outside", encoding="utf-8")
        (self.root / "escape.md").symlink_to(outside)
        self.manifest["nodes"][0]["source"] = "escape.md"
        with self.assertRaisesRegex(ValueError, "outside root"):
            self.build()

    def test_inside_root_symlink_uses_target_bytes(self):
        (self.root / "alias.md").symlink_to(self.root / "rule.md")
        self.manifest["nodes"][0]["source"] = "alias.md"
        row = list(csv.DictReader(io.StringIO(self.build()["nodes_csv"])))[1]
        self.assertEqual(row["source"], "alias.md")
        self.assertEqual(row["sha256"], hashlib.sha256((self.root / "rule.md").read_bytes()).hexdigest())

    def test_missing_source_and_directory_rejected(self):
        (self.root / "directory").mkdir()
        for path in ("missing.md", "directory"):
            with self.subTest(path=path):
                self.manifest["nodes"][0]["source"] = path
                with self.assertRaises(ValueError):
                    self.build()

    def test_duplicate_ids_and_invalid_ids_rejected(self):
        duplicate = copy.deepcopy(self.manifest)
        duplicate["nodes"].append(copy.deepcopy(duplicate["nodes"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate node id"):
            self.build(duplicate)
        for node_id in ("", "space id", "[link]", "id\nrow", None):
            with self.subTest(node_id=node_id):
                self.manifest["nodes"][0]["id"] = node_id
                with self.assertRaises(ValueError):
                    self.build()

    def test_unknown_kind_status_and_node_field_rejected(self):
        for key, value in (("kind", "physics_proof"), ("status", "true"), ("confidence", 1)):
            with self.subTest(key=key):
                manifest = copy.deepcopy(self.manifest)
                manifest["nodes"][0][key] = value
                with self.assertRaises(ValueError):
                    self.build(manifest)

    def test_missing_endpoint_unknown_relation_and_duplicate_edges_rejected(self):
        for key, value in (("source", "missing"), ("target", "missing"),
                           ("relation", "proves_physics"), ("relation", None)):
            with self.subTest(key=key, value=value):
                manifest = copy.deepcopy(self.manifest)
                manifest["edges"][0][key] = value
                with self.assertRaises(ValueError):
                    self.build(manifest)
        self.manifest["edges"].append(copy.deepcopy(self.manifest["edges"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate edge"):
            self.build()

    def test_dates_are_explicit_and_valid(self):
        for date in ("2026-9-10", "20260910", "2026-02-30", "today", None):
            with self.subTest(date=date):
                with self.assertRaises(ValueError):
                    build(self.manifest, self.root, date)

    def test_schema_and_container_types_validated(self):
        for key, value in (("nodes", {}), ("nodes", []), ("edges", {}),
                           ("schema_version", 2), ("schema_version", True), ("unknown", "x")):
            with self.subTest(key=key, value=value):
                manifest = copy.deepcopy(self.manifest)
                manifest[key] = value
                with self.assertRaises(ValueError):
                    self.build(manifest)

    def test_markdown_does_not_activate_manifest_links(self):
        self.manifest["title"] = "<b>Claim</b> | [link](https://example.invalid)"
        self.manifest["nodes"][0]["anchor"] = "a|b`[c]"
        markdown = self.build()["markdown"]
        self.assertNotIn("<b>", markdown)
        self.assertNotIn("[link]", markdown)
        self.assertIn("a&#124;b&#96;&#91;c&#93;", markdown)

    def test_cli_outputs_match_api_and_refuse_source_overwrite(self):
        manifest_path = self.root / "manifest.json"
        manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        script = Path(__file__).resolve().parents[1] / "Tools/build_research_provenance.py"
        command = [sys.executable, str(script), "--manifest", str(manifest_path),
                   "--root", str(self.root), "--date", "2026-09-10", "--out"]
        result = subprocess.run(command + [str(self.root / "generated/index")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / "generated/index.md").read_text(encoding="utf-8"), self.build()["markdown"])
        before = (self.root / "rule.md").read_bytes()
        result = subprocess.run(command + [str(self.root / "rule")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("must not overwrite", result.stderr)
        self.assertEqual((self.root / "rule.md").read_bytes(), before)
        self.assertFalse((self.root / "rule_nodes.csv").exists())

    def test_cli_refuses_output_hardlink_to_source(self):
        manifest_path = self.root / "manifest.json"
        manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        os.link(self.root / "rule.md", self.root / "aliased.md")
        before = (self.root / "rule.md").read_bytes()
        script = Path(__file__).resolve().parents[1] / "Tools/build_research_provenance.py"
        result = subprocess.run([sys.executable, str(script), "--manifest", str(manifest_path),
                                 "--root", str(self.root), "--date", "2026-09-10",
                                 "--out", str(self.root / "aliased")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("must not overwrite", result.stderr)
        self.assertEqual((self.root / "rule.md").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
