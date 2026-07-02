from __future__ import annotations

from dataclasses import dataclass
import hashlib
from threading import Lock
import time
from typing import Any, Protocol

from fastapi import HTTPException, status
from sqlalchemy import text

from app.api.case_browse import _case_source_types
from app.models.schemas import Citation, QueryResponse
from app.rag.index.db import engine
from app.settings import settings


class ResearchIdentityLike(Protocol):
    token: str
    label: str | None
    scopes: frozenset[str]
    case_ids: frozenset[str] | None


@dataclass(frozen=True)
class RateLimitDecision:
    ok: bool
    token_fingerprint: str
    backend: str
    limit_per_minute: int
    burst: int
    used: int
    remaining: int
    retry_after_seconds: int = 0


_RATE_LOCK = Lock()
_RATE_BUCKETS: dict[str, tuple[int, int]] = {}
_SUPPORTED_RATE_LIMIT_BACKENDS = {"memory", "postgres"}


def token_fingerprint(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()[:16]


def _rate_limit_backend() -> str:
    backend = (settings.research_rate_limit_backend or "memory").strip().lower()
    if backend not in _SUPPORTED_RATE_LIMIT_BACKENDS:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unsupported research rate-limit backend: {backend}",
        )
    return backend


def _memory_rate_limit(
    *,
    token_key: str,
    current: float,
    window: int,
    limit: int,
    burst: int,
) -> RateLimitDecision:
    allowed = max(limit, burst)
    with _RATE_LOCK:
        bucket_window, used = _RATE_BUCKETS.get(token_key, (window, 0))
        if bucket_window != window:
            bucket_window, used = window, 0
        used += 1
        _RATE_BUCKETS[token_key] = (bucket_window, used)

    remaining = max(0, allowed - used)
    retry_after = max(1, int(((window + 1) * 60) - current))
    return RateLimitDecision(
        ok=used <= allowed,
        token_fingerprint=token_key,
        backend="memory",
        limit_per_minute=limit,
        burst=burst,
        used=used,
        remaining=remaining,
        retry_after_seconds=0 if used <= allowed else retry_after,
    )


def _postgres_rate_limit(
    *,
    token_key: str,
    current: float,
    window: int,
    limit: int,
    burst: int,
) -> RateLimitDecision:
    allowed = max(limit, burst)
    window_start_epoch = window * 60
    sql = text(
        """
        INSERT INTO rag_research_rate_limits(token_fingerprint, window_start, used, updated_at)
        VALUES (:token_fingerprint, to_timestamp(:window_start_epoch), 1, now())
        ON CONFLICT (token_fingerprint, window_start)
        DO UPDATE SET used = rag_research_rate_limits.used + 1,
                      updated_at = now()
        RETURNING used
        """
    )
    try:
        with engine().begin() as conn:
            used = int(
                conn.execute(
                    sql,
                    {
                        "token_fingerprint": token_key,
                        "window_start_epoch": window_start_epoch,
                    },
                ).scalar_one()
            )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Research rate-limit backend is unavailable. "
                "Run migrations and verify PostgreSQL connectivity."
            ),
        ) from exc

    remaining = max(0, allowed - used)
    retry_after = max(1, int(((window + 1) * 60) - current))
    return RateLimitDecision(
        ok=used <= allowed,
        token_fingerprint=token_key,
        backend="postgres",
        limit_per_minute=limit,
        burst=burst,
        used=used,
        remaining=remaining,
        retry_after_seconds=0 if used <= allowed else retry_after,
    )


def check_research_rate_limit(identity: ResearchIdentityLike, *, now: float | None = None) -> RateLimitDecision:
    limit = max(0, int(settings.research_rate_limit_per_minute))
    burst = max(1, int(settings.research_rate_limit_burst))
    key = token_fingerprint(identity.token)
    backend = _rate_limit_backend()
    if limit <= 0:
        return RateLimitDecision(
            ok=True,
            token_fingerprint=key,
            backend=backend,
            limit_per_minute=0,
            burst=burst,
            used=0,
            remaining=burst,
        )

    current = time.time() if now is None else now
    window = int(current // 60)
    if backend == "postgres":
        return _postgres_rate_limit(
            token_key=key,
            current=current,
            window=window,
            limit=limit,
            burst=burst,
        )
    return _memory_rate_limit(
        token_key=key,
        current=current,
        window=window,
        limit=limit,
        burst=burst,
    )


def enforce_research_rate_limit(identity: ResearchIdentityLike) -> RateLimitDecision:
    decision = check_research_rate_limit(identity)
    if decision.ok:
        return decision
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Research API rate limit exceeded.",
        headers={"Retry-After": str(decision.retry_after_seconds)},
    )


def _citation_payload(citation: Citation) -> dict[str, Any]:
    if hasattr(citation, "model_dump"):
        return citation.model_dump()
    return citation.dict()


def audit_citations(response: QueryResponse) -> dict[str, Any]:
    citations = list(response.citations or [])
    unique_docs = {str(c.doc_id) for c in citations if str(c.doc_id or "").strip()}
    missing_required_fields: list[dict[str, Any]] = []
    public_download_leaks: list[str] = []

    for idx, citation in enumerate(citations):
        payload = _citation_payload(citation)
        missing = [
            field
            for field in ("doc_id", "chunk_id", "title", "excerpt")
            if not str(payload.get(field) or "").strip()
        ]
        if missing:
            missing_required_fields.append({"index": idx, "missing": missing})

        download_url = str(payload.get("download_url") or "")
        if download_url.startswith("/v1/documents/"):
            public_download_leaks.append(download_url)

    min_citations = max(0, int(settings.research_min_citations))
    min_unique_docs = max(0, int(settings.research_min_unique_docs))
    safe_no_source_answer = (
        len(citations) == 0
        and "ikke dokumentert i kildene" in (response.answer or "").lower()
    )
    violations: list[dict[str, Any]] = []
    if not safe_no_source_answer and len(citations) < min_citations:
        violations.append(
            {
                "rule": "min_citations",
                "expected_gte": min_citations,
                "actual": len(citations),
            }
        )
    if not safe_no_source_answer and len(unique_docs) < min_unique_docs:
        violations.append(
            {
                "rule": "min_unique_docs",
                "expected_gte": min_unique_docs,
                "actual": len(unique_docs),
            }
        )
    if missing_required_fields:
        violations.append({"rule": "required_citation_fields", "items": missing_required_fields[:10]})
    if public_download_leaks:
        violations.append({"rule": "public_download_url_leak", "items": public_download_leaks[:10]})

    return {
        "ok": not violations,
        "safe_no_source_answer": safe_no_source_answer,
        "citation_count": len(citations),
        "unique_doc_count": len(unique_docs),
        "min_citations": min_citations,
        "min_unique_docs": min_unique_docs,
        "violations": violations,
    }


def corpus_freshness(case_id: str) -> dict[str, Any]:
    source_types = _case_source_types(case_id)
    if not source_types:
        return {
            "ok": False,
            "status": "no_source_types",
            "case_id": case_id,
            "source_types": [],
            "violations": [{"rule": "case_has_no_source_types"}],
        }

    sql = text(
        """
        SELECT
          COUNT(*) FILTER (WHERE COALESCE(doc_state, 'active') = 'active') AS active_docs,
          COUNT(*) FILTER (WHERE doc_state = 'tombstone_pending') AS tombstone_pending_docs,
          MAX(updated_at) AS newest_updated_at,
          MIN(updated_at) AS oldest_updated_at
        FROM documents
        WHERE source_type = ANY(:source_types)
        """
    )
    with engine().begin() as conn:
        row = dict(conn.execute(sql, {"source_types": source_types}).mappings().one())

    active_docs = int(row.get("active_docs") or 0)
    tombstone_pending_docs = int(row.get("tombstone_pending_docs") or 0)
    newest = row.get("newest_updated_at")
    age_seconds: int | None = None
    if newest is not None:
        try:
            age_seconds = max(0, int(time.time() - newest.timestamp()))
        except Exception:
            age_seconds = None

    max_age = max(0, int(settings.research_freshness_max_age_seconds))
    violations: list[dict[str, Any]] = []
    if active_docs <= 0:
        violations.append({"rule": "no_active_documents"})
    if tombstone_pending_docs > 0:
        violations.append(
            {"rule": "tombstone_pending_documents", "actual": tombstone_pending_docs}
        )
    if max_age > 0 and age_seconds is not None and age_seconds > max_age:
        violations.append(
            {
                "rule": "corpus_stale",
                "max_age_seconds": max_age,
                "actual_age_seconds": age_seconds,
            }
        )
    if max_age > 0 and age_seconds is None:
        violations.append({"rule": "freshness_unknown"})

    return {
        "ok": not violations,
        "case_id": case_id,
        "source_types": source_types,
        "active_docs": active_docs,
        "tombstone_pending_docs": tombstone_pending_docs,
        "newest_updated_at": newest.isoformat() if hasattr(newest, "isoformat") else None,
        "oldest_updated_at": (
            row.get("oldest_updated_at").isoformat()
            if hasattr(row.get("oldest_updated_at"), "isoformat")
            else None
        ),
        "age_seconds": age_seconds,
        "max_age_seconds": max_age,
        "enforced": bool(settings.research_enforce_freshness),
        "violations": violations,
    }


def attach_research_hardening_audit(
    response: QueryResponse,
    *,
    identity: ResearchIdentityLike,
    rate_limit: RateLimitDecision,
    case_id: str,
) -> QueryResponse:
    debug = dict(response.retrieval_debug or {})
    citation_audit = audit_citations(response)
    freshness = corpus_freshness(case_id)
    debug["research_hardening"] = {
        "auth": {
            "token_label": identity.label,
            "token_fingerprint": rate_limit.token_fingerprint,
            "scopes": sorted(identity.scopes),
            "case_scoped": identity.case_ids is not None,
        },
        "rate_limit": {
            "backend": rate_limit.backend,
            "limit_per_minute": rate_limit.limit_per_minute,
            "burst": rate_limit.burst,
            "used": rate_limit.used,
            "remaining": rate_limit.remaining,
        },
        "citation_audit": citation_audit,
        "freshness": freshness,
    }

    if settings.research_enforce_response_audit and not citation_audit["ok"]:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={
                "message": "Research response failed citation audit.",
                "citation_audit": citation_audit,
            },
        )

    if settings.research_enforce_freshness and not freshness["ok"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "message": "Research corpus freshness check failed.",
                "freshness": freshness,
            },
        )

    return QueryResponse(
        answer=response.answer,
        citations=response.citations,
        retrieval_debug=debug,
        trace=debug.get("query_plan") if isinstance(debug.get("query_plan"), dict) else response.trace,
    )
