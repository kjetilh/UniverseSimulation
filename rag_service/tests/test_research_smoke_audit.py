"""Closure smoke checks using only stdlib fixtures; no service, DB or credentials."""
from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "research_hardening_smoke.py"
SPEC = importlib.util.spec_from_file_location("uc2_research_smoke_audit", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
smoke = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = smoke
SPEC.loader.exec_module(smoke)


def query_response():
    return {
        "answer": "A measured result with stated limits [1][2].",
        "citations": [
            {
                "doc_id": "uc2-result-doc", "chunk_id": "result-1",
                "title": "UC2 result", "excerpt": "The bounded candidate result.",
                "score": 0.9, "url": None,
                "download_url": "/v1/research/documents/uc2-result-doc/download?sig=fixture",
            },
            {
                "doc_id": "limits-doc", "chunk_id": "limits-1",
                "title": "Claim limits", "excerpt": "No general physics claim.",
                "score": 0.8, "url": None,
                "download_url": "/v1/research/documents/limits-doc/download?sig=fixture",
            },
        ],
        "retrieval_debug": {
            "research_hardening": {
                "auth": {"token_label": "synthetic", "case_scoped": True,
                         "scopes": ["research:read"]},
                "rate_limit": {"backend": "postgres", "used": 2, "remaining": 28},
                "citation_audit": {"ok": True, "citation_count": 2, "violations": []},
                "freshness": {"ok": True, "active_docs": 2, "violations": []},
            },
        },
    }


class QueryAuditTests(unittest.TestCase):
    def summarize(self, payload, **kwargs):
        return smoke._summarize_query(
            payload, token="synthetic-bearer", expected_rate_backend="postgres", **kwargs
        )

    def test_success_without_optional_matcher(self):
        result = self.summarize(query_response())
        self.assertTrue(result["citation_audit_ok"])
        self.assertTrue(result["freshness_ok"])
        self.assertEqual(result["actual_citation_count"], 2)
        self.assertEqual(result["matched_required_citations"], [])

    def test_audits_require_literal_true(self):
        for audit in ("citation_audit", "freshness"):
            for value in (False, None, "true", 1, {}, []):
                with self.subTest(audit=audit, value=value):
                    response = query_response()
                    response["retrieval_debug"]["research_hardening"][audit]["ok"] = value
                    with self.assertRaisesRegex(smoke.SmokeFailure, audit):
                        self.summarize(response)
            response = query_response()
            del response["retrieval_debug"]["research_hardening"][audit]["ok"]
            with self.assertRaisesRegex(smoke.SmokeFailure, audit):
                self.summarize(response)

    def test_missing_or_malformed_audit_structure(self):
        for payload in ([], None, {}, {"retrieval_debug": {}}, {"retrieval_debug": []}):
            with self.subTest(payload=payload), self.assertRaises(smoke.SmokeFailure):
                self.summarize(payload)
        for field in ("auth", "rate_limit", "citation_audit", "freshness"):
            response = query_response()
            del response["retrieval_debug"]["research_hardening"][field]
            with self.subTest(field=field), self.assertRaises(smoke.SmokeFailure):
                self.summarize(response)

    def test_actual_citations_required_even_when_audit_reports_success(self):
        for citations in (None, [], {}, "citation", [{}], [None]):
            response = query_response()
            response["citations"] = citations
            with self.subTest(citations=citations), self.assertRaises(smoke.SmokeFailure):
                self.summarize(response)
        response = query_response()
        del response["citations"]
        with self.assertRaises(smoke.SmokeFailure):
            self.summarize(response)

    def test_incomplete_citation_rejected(self):
        for field in ("doc_id", "chunk_id", "title", "excerpt"):
            for value in (None, " ", 12):
                response = query_response()
                response["citations"][0][field] = value
                with self.subTest(field=field, value=value), self.assertRaises(smoke.SmokeFailure):
                    self.summarize(response)

    def test_identity_match_is_case_insensitive_and_literal(self):
        for field in ("doc_id", "title", "url", "download_url"):
            response = query_response()
            response["citations"][0][field] = "prefix UC2_report.md suffix"
            result = self.summarize(response, required_citation_substring=" uc2_REPORT.md ")
            self.assertEqual(len(result["matched_required_citations"]), 1)
        with self.assertRaises(smoke.SmokeFailure):
            self.summarize(query_response(), required_citation_substring="UC2.*")

    def test_answer_and_excerpt_do_not_satisfy_identity_requirement(self):
        response = query_response()
        response["answer"] = "fresh-round-identity"
        response["citations"][0]["excerpt"] = "fresh-round-identity"
        with self.assertRaisesRegex(smoke.SmokeFailure, "No actual citation identity"):
            self.summarize(response, required_citation_substring="fresh-round-identity")

    def test_empty_requirement_rejected(self):
        with self.assertRaises(smoke.SmokeFailure):
            self.summarize(query_response(), required_citation_substring=" ")

    def test_backend_and_token_echo_checks_preserved(self):
        response = query_response()
        response["retrieval_debug"]["research_hardening"]["rate_limit"]["backend"] = "memory"
        with self.assertRaisesRegex(smoke.SmokeFailure, "rate-limit backend"):
            self.summarize(response)
        response = query_response()
        response["answer"] = "synthetic-bearer"
        with self.assertRaisesRegex(smoke.SmokeFailure, "echoed"):
            self.summarize(response)


class CliAuditTests(unittest.TestCase):
    def run_cli(self, extra=(), response=None, query_status=200):
        def http(status, body):
            return smoke.HttpResult(status, json.dumps(body), {})

        responses = [
            http(401, {"detail": "unauthorized"}),
            http(200, {"cases": [{"case_id": "universe_project"}]}),
            http(query_status, query_response() if response is None else response),
        ]
        output = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), patch.object(
            smoke, "_request", side_effect=responses
        ) as request_mock, redirect_stdout(output):
            status = smoke.main([
                "--token", "synthetic-bearer", "--base-url", "http://fixture.invalid",
                "--expected-rate-backend", "postgres", *extra,
            ])
        return status, json.loads(output.getvalue()), request_mock.call_count

    def test_cli_forwards_matcher_and_reports_matching_citation(self):
        status, output, calls = self.run_cli(("--required-citation-substring", "UC2 result"))
        self.assertEqual((status, calls), (0, 3))
        self.assertTrue(output["ok"])
        self.assertEqual(output["query"]["matched_required_citations"][0]["doc_id"],
                         "uc2-result-doc")

    def test_cli_match_failure_is_nonzero(self):
        status, output, calls = self.run_cli(("--required-citation-substring", "UC3"))
        self.assertEqual((status, calls), (1, 3))
        self.assertFalse(output["ok"])

    def test_cli_rejects_failed_audits_and_empty_citations(self):
        for audit in ("citation_audit", "freshness"):
            response = query_response()
            response["retrieval_debug"]["research_hardening"][audit]["ok"] = False
            status, output, _ = self.run_cli(response=response)
            self.assertEqual(status, 1)
            self.assertFalse(output["ok"])
        response = query_response()
        response["citations"] = []
        self.assertEqual(self.run_cli(response=response)[0], 1)

    def test_matcher_cannot_be_bypassed_with_diagnostic_modes(self):
        for flag in ("--skip-query", "--allow-audit-fail-closed"):
            status, output, calls = self.run_cli(("--required-citation-substring", "UC2", flag))
            self.assertEqual((status, calls), (1, 0))
            self.assertFalse(output["ok"])
        self.assertEqual(self.run_cli(("--required-citation-substring", " "))[0], 1)

    def test_existing_calls_and_diagnostic_modes_still_work(self):
        self.assertEqual(self.run_cli()[0], 0)
        status, output, calls = self.run_cli(("--skip-query",))
        self.assertEqual((status, calls, output["query"]), (0, 2, None))
        status, output, calls = self.run_cli(
            ("--allow-audit-fail-closed",), response={"detail": "blocked audit"}, query_status=424
        )
        self.assertEqual((status, calls), (0, 3))
        self.assertEqual(output["checks"][-1]["name"], "query_failed_closed")


if __name__ == "__main__":
    unittest.main()
