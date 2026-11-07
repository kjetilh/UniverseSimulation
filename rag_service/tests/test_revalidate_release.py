import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts.revalidate_sources import run_revalidation


class RevalidateReleaseTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name).resolve()
        self.release = root / "release"
        self.mirror = root / "uploads"
        self.release.mkdir()
        source = self.release / "docs" / "results.md"
        source.parent.mkdir()
        source.write_bytes(b"first line\r\nsecond line\n")
        self.config = self.release / "sources.toml"
        config = (
            f'[orchestrator]\ningest_root = "{self.mirror}"\ningest_live_subdir = "live"\n'
            'admin_base_url = "http://localhost"\nadmin_api_key_env = "TEST_REVALIDATE_KEY"\n'
        )
        for name in ("reports", "evidence"):
            config += (
                f'[[source]]\nname = "{name}"\nrepo_path = "/production-checkout"\n'
                f'repo_subpath = "docs"\nsource_type = "{name}"\ntarget_subdir = "{name}"\n'
                'include = ["*.md"]\n'
            )
            target = self.mirror / "live" / name / source.name
            target.parent.mkdir(parents=True)
            target.write_bytes(source.read_bytes())
        self.config.write_text(config)
        for args in (
            ["init", "-q"], ["add", "."],
            ["-c", "user.name=Test", "-c", "user.email=test@example.invalid",
             "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"],
        ):
            subprocess.run(["git", *args], cwd=self.release, check=True)
        self.sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=self.release, text=True
        ).strip()

    def run_plan(self):
        return run_revalidation(self.config, self.release, self.sha, plan_only=True)

    def test_plan_proves_both_raw_mirrors_and_their_one_git_path_without_posting(self):
        with patch("scripts.revalidate_sources._http_json_request") as post:
            result = self.run_plan()
        post.assert_not_called()
        self.assertEqual(result["source_file_count"], 1)
        self.assertEqual(result["mirror_count"], 2)
        self.assertEqual({r["source_path"] for r in result["manifest"]}, {"docs/results.md"})
        self.assertEqual({r["raw_sha256"] for r in result["manifest"]},
                         {hashlib.sha256(b"first line\r\nsecond line\n").hexdigest()})

    def test_rejects_normalization_only_mirror_drift(self):
        (self.mirror / "live/reports/results.md").write_bytes(b"first line\nsecond line\n")
        with self.assertRaisesRegex(ValueError, "Mirror bytes differ"):
            self.run_plan()

    def test_rejects_matching_mirrors_when_worktree_disagrees_with_the_git_blob(self):
        subprocess.run(
            ["git", "update-index", "--assume-unchanged", "docs/results.md"],
            cwd=self.release, check=True,
        )
        for path in (self.release / "docs/results.md", *self.mirror.rglob("results.md")):
            path.write_bytes(b"uncommitted replacement")
        with self.assertRaisesRegex(ValueError, "Release bytes differ from the commit"):
            self.run_plan()

    def test_rejects_unexpected_mirror_file_and_dirty_config(self):
        extra = self.mirror / "live/reports/extra.md"
        extra.touch()
        with self.assertRaisesRegex(ValueError, "Mirror inventory differs"):
            self.run_plan()
        extra.unlink()
        self.config.write_text(self.config.read_text() + "\n")
        with self.assertRaisesRegex(ValueError, "worktree must be clean"):
            self.run_plan()

    def test_same_revision_required_and_missing_verified_doc_is_a_failure(self):
        with self.assertRaisesRegex(ValueError, "HEAD differs"):
            run_revalidation(self.config, self.release, "0"*40, plan_only=True)
        summary = {"verified_files": 2, "verified_docs": 0, "source_revision": self.sha}
        with patch.dict(os.environ, TEST_REVALIDATE_KEY="test"), patch(
            "scripts.revalidate_sources._http_json_request",
            return_value=(200, {"ok": True, "summary": summary})
        ) as post:
            result = run_revalidation(self.config, self.release, self.sha)
        self.assertFalse(result["ok"])
        self.assertEqual(post.call_args.kwargs["url"], "http://localhost/v1/admin/revalidate")
        self.assertEqual(len(post.call_args.kwargs["payload"]["files"]), 2)
