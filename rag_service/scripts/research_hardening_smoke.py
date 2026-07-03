from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from typing import Any
from urllib import error, request


class SmokeFailure(RuntimeError):
    pass


@dataclass(frozen=True)
class HttpResult:
    status: int
    body: str
    headers: dict[str, str]

    def json(self) -> Any:
        try:
            return json.loads(self.body)
        except json.JSONDecodeError as exc:
            raise SmokeFailure(f"Expected JSON response, got: {self.body[:300]!r}") from exc


def _json_dumps(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, ensure_ascii=True)


def _request(
    method: str,
    url: str,
    *,
    token: str | None = None,
    payload: dict[str, Any] | None = None,
    timeout: float,
) -> HttpResult:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = request.Request(url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return HttpResult(resp.status, body, dict(resp.headers.items()))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return HttpResult(exc.code, body, dict(exc.headers.items()))
    except error.URLError as exc:
        raise SmokeFailure(f"Could not reach {url}: {exc}") from exc


def _join_url(base_url: str, path: str) -> str:
    return base_url.rstrip("/") + "/" + path.lstrip("/")


def _require_status(result: HttpResult, expected: int, label: str) -> None:
    if result.status != expected:
        raise SmokeFailure(
            f"{label} returned HTTP {result.status}, expected {expected}. Body: {result.body[:500]}"
        )


def _extract_hardening(payload: dict[str, Any]) -> dict[str, Any]:
    debug = payload.get("retrieval_debug")
    if not isinstance(debug, dict):
        raise SmokeFailure("Query response did not include retrieval_debug.")
    hardening = debug.get("research_hardening")
    if not isinstance(hardening, dict):
        raise SmokeFailure("Query response did not include retrieval_debug.research_hardening.")
    return hardening


def _assert_no_token_echo(payload: Any, token: str) -> None:
    if token and token in _json_dumps(payload):
        raise SmokeFailure("Research API response echoed the bearer token.")


def _summarize_query(
    payload: dict[str, Any],
    *,
    token: str,
    expected_rate_backend: str,
) -> dict[str, Any]:
    _assert_no_token_echo(payload, token)
    hardening = _extract_hardening(payload)
    for required in ("auth", "rate_limit", "citation_audit", "freshness"):
        if not isinstance(hardening.get(required), dict):
            raise SmokeFailure(f"Missing research_hardening.{required}.")

    rate_limit = hardening["rate_limit"]
    actual_backend = str(rate_limit.get("backend") or "")
    if actual_backend != expected_rate_backend:
        raise SmokeFailure(
            "Unexpected research rate-limit backend: "
            f"{actual_backend!r}, expected {expected_rate_backend!r}."
        )

    return {
        "rate_limit_backend": actual_backend,
        "rate_limit_used": rate_limit.get("used"),
        "rate_limit_remaining": rate_limit.get("remaining"),
        "citation_audit_ok": hardening["citation_audit"].get("ok"),
        "citation_count": hardening["citation_audit"].get("citation_count"),
        "freshness_ok": hardening["freshness"].get("ok"),
        "active_docs": hardening["freshness"].get("active_docs"),
    }


def run_smoke(args: argparse.Namespace) -> dict[str, Any]:
    token = args.token or os.environ.get("RESEARCH_API_TOKEN", "")
    if not token:
        raise SmokeFailure("Missing token. Pass --token or set RESEARCH_API_TOKEN.")

    base_url = args.base_url or os.environ.get("RESEARCH_BASE_URL", "http://127.0.0.1:8000")
    case_id = args.case_id
    checks: list[dict[str, Any]] = []

    anonymous_cases = _request(
        "GET",
        _join_url(base_url, "/v1/research/cases"),
        timeout=args.timeout,
    )
    _require_status(anonymous_cases, 401, "anonymous research cases")
    checks.append({"name": "anonymous_cases_rejected", "status": anonymous_cases.status})

    authenticated_cases = _request(
        "GET",
        _join_url(base_url, "/v1/research/cases"),
        token=token,
        timeout=args.timeout,
    )
    _require_status(authenticated_cases, 200, "authenticated research cases")
    cases_payload = authenticated_cases.json()
    _assert_no_token_echo(cases_payload, token)
    cases = cases_payload.get("cases")
    if not isinstance(cases, list):
        raise SmokeFailure("/v1/research/cases did not return a cases list.")
    if case_id not in {str(item.get("case_id")) for item in cases if isinstance(item, dict)}:
        raise SmokeFailure(f"Token cannot see required case_id {case_id!r}.")
    checks.append({"name": "authenticated_cases_visible", "status": authenticated_cases.status})

    query_summary: dict[str, Any] | None = None
    if not args.skip_query:
        query_response = _request(
            "POST",
            _join_url(base_url, "/v1/research/query"),
            token=token,
            payload={"case_id": case_id, "query": args.query},
            timeout=args.timeout,
        )
        if query_response.status == 200:
            query_payload = query_response.json()
            query_summary = _summarize_query(
                query_payload,
                token=token,
                expected_rate_backend=args.expected_rate_backend,
            )
            checks.append({"name": "query_hardening_audit", "status": query_response.status})
        elif args.allow_audit_fail_closed and query_response.status in {424, 503}:
            detail = query_response.json().get("detail")
            checks.append(
                {
                    "name": "query_failed_closed",
                    "status": query_response.status,
                    "detail": detail,
                }
            )
        else:
            raise SmokeFailure(
                "/v1/research/query returned "
                f"HTTP {query_response.status}. Body: {query_response.body[:1000]}"
            )

    if args.rate_limit_probe_count > 0:
        saw_limit = False
        last_status = None
        for _ in range(args.rate_limit_probe_count):
            probe = _request(
                "GET",
                _join_url(base_url, "/v1/research/cases"),
                token=token,
                timeout=args.timeout,
            )
            last_status = probe.status
            if probe.status == 429:
                saw_limit = True
                break
        if not saw_limit:
            raise SmokeFailure(
                "Rate-limit probe did not observe HTTP 429. "
                f"Last status was {last_status}; use this only with a low test limit."
            )
        checks.append({"name": "rate_limit_probe", "status": 429})

    return {
        "ok": True,
        "base_url": base_url,
        "case_id": case_id,
        "expected_rate_backend": args.expected_rate_backend,
        "checks": checks,
        "query": query_summary,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Smoke-test the token-scoped research RAG hardening surface."
    )
    parser.add_argument("--base-url", default=None, help="RAG service base URL.")
    parser.add_argument("--token", default=None, help="Research API bearer token.")
    parser.add_argument("--case-id", default="universe_project", help="Required visible case.")
    parser.add_argument(
        "--query",
        default="Hva er prosjektets navarende evidensstatus?",
        help="Query used for /v1/research/query.",
    )
    parser.add_argument(
        "--expected-rate-backend",
        default=os.environ.get("RESEARCH_EXPECTED_RATE_LIMIT_BACKEND", "postgres"),
        choices=("memory", "postgres"),
        help="Expected retrieval_debug.research_hardening.rate_limit.backend.",
    )
    parser.add_argument(
        "--skip-query",
        action="store_true",
        help="Only check auth/case visibility. Does not verify audit/freshness output.",
    )
    parser.add_argument(
        "--allow-audit-fail-closed",
        action="store_true",
        help="Allow 424/503 from /v1/research/query as a fail-closed policy check.",
    )
    parser.add_argument(
        "--rate-limit-probe-count",
        type=int,
        default=0,
        help="Optional count of extra cases requests; expects an HTTP 429 before the count ends.",
    )
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout in seconds.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = run_smoke(args)
    except SmokeFailure as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2, sort_keys=True))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
