from fastapi import FastAPI
from fastapi.testclient import TestClient
from types import SimpleNamespace

from app.api import research_hardening, routes_research
from app.models.schemas import Citation, QueryResponse
from app.settings import settings


def _client(monkeypatch, token: str = "research-token") -> TestClient:
    monkeypatch.setattr(
        settings,
        "research_api_tokens_json",
        (
            '{"%s":{"label":"public-test",'
            '"scopes":["research:read"],'
            '"case_ids":["universe_project"]}}'
        )
        % token,
    )
    monkeypatch.setattr(settings, "research_allow_query_access_token", False)
    monkeypatch.setattr(settings, "research_rate_limit_backend", "memory")
    monkeypatch.setattr(settings, "research_rate_limit_per_minute", 60)
    monkeypatch.setattr(settings, "research_rate_limit_burst", 60)
    monkeypatch.setattr(settings, "research_min_citations", 2)
    monkeypatch.setattr(settings, "research_min_unique_docs", 1)
    monkeypatch.setattr(settings, "research_enforce_response_audit", True)
    monkeypatch.setattr(settings, "research_enforce_freshness", False)
    research_hardening._RATE_BUCKETS.clear()

    app = FastAPI()
    app.include_router(routes_research.router)
    return TestClient(app)


def _freshness_ok(case_id: str):
    return {
        "ok": True,
        "case_id": case_id,
        "source_types": ["universe_status"],
        "active_docs": 4,
        "tombstone_pending_docs": 0,
        "newest_updated_at": "2026-06-28T00:00:00+00:00",
        "oldest_updated_at": "2026-06-20T00:00:00+00:00",
        "age_seconds": 0,
        "max_age_seconds": 0,
        "enforced": False,
        "violations": [],
    }


def _two_citation_response(req):
    del req
    return QueryResponse(
        answer="Svar med dokumenterte kilder.",
        citations=[
            Citation(
                doc_id="doc-1",
                title="A",
                chunk_id="c1",
                score=0.9,
                excerpt="alpha",
            ),
            Citation(
                doc_id="doc-2",
                title="B",
                chunk_id="c2",
                score=0.8,
                excerpt="beta",
            ),
        ],
        retrieval_debug={"query_plan": {"case_id": "universe_project"}},
    )


def test_research_query_rejects_query_access_token_by_default(monkeypatch):
    client = _client(monkeypatch, token="query-token-disabled")

    response = client.get("/v1/research/cases?access_token=query-token-disabled")

    assert response.status_code == 401
    assert "Authorization: Bearer" in response.json()["detail"]


def test_research_query_attaches_hardening_audit(monkeypatch):
    monkeypatch.setattr(routes_research, "_require_case_access", lambda case_id, identity: None)
    monkeypatch.setattr(routes_research, "_run_query", _two_citation_response)
    monkeypatch.setattr(research_hardening, "corpus_freshness", _freshness_ok)
    client = _client(monkeypatch, token="audit-token")

    response = client.post(
        "/v1/research/query",
        headers={"Authorization": "Bearer audit-token"},
        json={"case_id": "universe_project", "query": "Hva vet vi?"},
    )

    assert response.status_code == 200
    payload = response.json()
    hardening = payload["retrieval_debug"]["research_hardening"]
    assert hardening["auth"]["token_label"] == "public-test"
    assert hardening["rate_limit"]["backend"] == "memory"
    assert hardening["rate_limit"]["remaining"] == 59
    assert hardening["citation_audit"]["ok"] is True
    assert hardening["citation_audit"]["citation_count"] == 2
    assert hardening["freshness"]["ok"] is True
    assert payload["trace"] == {"case_id": "universe_project"}


def test_research_query_fails_closed_on_citation_audit_violation(monkeypatch):
    def one_citation_response(req):
        del req
        return QueryResponse(
            answer="For svakt dokumentert svar.",
            citations=[
                Citation(
                    doc_id="doc-1",
                    title="A",
                    chunk_id="c1",
                    score=0.9,
                    excerpt="alpha",
                )
            ],
            retrieval_debug={"query_plan": {"case_id": "universe_project"}},
        )

    monkeypatch.setattr(routes_research, "_require_case_access", lambda case_id, identity: None)
    monkeypatch.setattr(routes_research, "_run_query", one_citation_response)
    monkeypatch.setattr(research_hardening, "corpus_freshness", _freshness_ok)
    client = _client(monkeypatch, token="citation-fail-token")

    response = client.post(
        "/v1/research/query",
        headers={"Authorization": "Bearer citation-fail-token"},
        json={"case_id": "universe_project", "query": "Hva vet vi?"},
    )

    assert response.status_code == 424
    detail = response.json()["detail"]
    assert detail["message"] == "Research response failed citation audit."
    assert detail["citation_audit"]["violations"][0]["rule"] == "min_citations"


def test_research_rate_limit_is_enforced(monkeypatch):
    def safe_no_source_response(req):
        del req
        return QueryResponse(
            answer="Ikke dokumentert i kildene.",
            citations=[],
            retrieval_debug={"query_plan": {"case_id": "universe_project"}},
        )

    monkeypatch.setattr(routes_research, "_require_case_access", lambda case_id, identity: None)
    monkeypatch.setattr(routes_research, "_run_query", safe_no_source_response)
    monkeypatch.setattr(research_hardening, "corpus_freshness", _freshness_ok)
    client = _client(monkeypatch, token="rate-limit-token")
    monkeypatch.setattr(settings, "research_rate_limit_per_minute", 1)
    monkeypatch.setattr(settings, "research_rate_limit_burst", 1)

    first = client.post(
        "/v1/research/query",
        headers={"Authorization": "Bearer rate-limit-token"},
        json={"case_id": "universe_project", "query": "Hva vet vi?"},
    )
    second = client.post(
        "/v1/research/query",
        headers={"Authorization": "Bearer rate-limit-token"},
        json={"case_id": "universe_project", "query": "Hva vet vi?"},
    )

    assert first.status_code == 200
    assert second.status_code == 429
    assert "Retry-After" in second.headers


def test_postgres_rate_limit_backend_uses_shared_counter(monkeypatch):
    seen = {}

    class FakeResult:
        def scalar_one(self):
            return 2

    class FakeConnection:
        def execute(self, sql, params):
            seen["sql"] = str(sql)
            seen["params"] = params
            return FakeResult()

    class FakeBegin:
        def __enter__(self):
            return FakeConnection()

        def __exit__(self, exc_type, exc, tb):
            return False

    class FakeEngine:
        def begin(self):
            return FakeBegin()

    monkeypatch.setattr(settings, "research_rate_limit_backend", "postgres")
    monkeypatch.setattr(settings, "research_rate_limit_per_minute", 5)
    monkeypatch.setattr(settings, "research_rate_limit_burst", 5)
    monkeypatch.setattr(research_hardening, "engine", lambda: FakeEngine())

    decision = research_hardening.check_research_rate_limit(
        SimpleNamespace(token="postgres-token"),
        now=120.0,
    )

    assert decision.ok is True
    assert decision.backend == "postgres"
    assert decision.used == 2
    assert decision.remaining == 3
    assert "ON CONFLICT" in seen["sql"]
    assert seen["params"]["window_start_epoch"] == 120
