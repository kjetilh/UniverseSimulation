from __future__ import annotations

import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any

from sqlalchemy import text

from app.rag.cases.loader import case_by_id, load_rag_cases
from app.rag.cases.visibility import visible_case_ids
from app.rag.index.db import engine
from app.rag.index.embedder import default_embedder
from app.rag.index.vector_store import upsert_embedding
from app.rag.index.indexer import ingest_file
from app.settings import settings

SUPPORTED_MEDIA_EXTENSIONS = {".md", ".markdown", ".txt", ".html", ".htm", ".pdf", ".docx"}
MAX_INLINE_MEDIA_BYTES = 2 * 1024 * 1024

_SAFE_FILENAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def _sha256_text(text_value: str) -> str:
    return hashlib.sha256(text_value.encode("utf-8")).hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _stable_id(*parts: str, prefix: str) -> str:
    raw = "\n".join(parts)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]
    return f"{prefix}-{digest}"


def _case_source_types(case_id: str) -> list[str]:
    cfg = load_rag_cases(settings.rag_cases_path)
    if case_id not in visible_case_ids(cfg):
        raise ValueError(f"Unknown case: {case_id}")
    selected = case_by_id(cfg, case_id)
    out: list[str] = []
    seen: set[str] = set()
    for value in list(selected.planner.docs_source_types) + list(selected.planner.prompts_source_types):
        item = (value or "").strip()
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def _require_case_source_type(case_id: str, source_type: str) -> None:
    source_types = _case_source_types(case_id)
    if source_type not in source_types:
        raise ValueError(
            f"source_type '{source_type}' is not configured for case '{case_id}'. "
            f"Configured source types: {', '.join(source_types) or '(none)'} ."
        )


def _catalog_doc_id(source_repo: str, chunk_id: str) -> str:
    return _stable_id(source_repo, chunk_id, prefix="catalog")


def _catalog_chunk_id(doc_id: str) -> str:
    return f"{doc_id}-c00000"


def _normalize_chunk(raw: dict[str, Any]) -> dict[str, Any]:
    chunk_id = str(raw.get("chunk_id") or raw.get("chunkID") or "").strip()
    title = str(raw.get("title") or "").strip()
    content = str(raw.get("content") or "").strip()
    metadata = raw.get("metadata") or {}
    if not isinstance(metadata, dict):
        raise ValueError(f"chunk '{chunk_id or '(missing)'}' metadata must be an object.")
    if not chunk_id:
        raise ValueError("Catalog chunk is missing chunk_id.")
    if not title:
        raise ValueError(f"Catalog chunk '{chunk_id}' is missing title.")
    if not content:
        raise ValueError(f"Catalog chunk '{chunk_id}' is missing content.")
    for key in ["repo", "serviceID", "cell", "contract", "status"]:
        if not str(metadata.get(key) or "").strip():
            raise ValueError(f"Catalog chunk '{chunk_id}' metadata is missing '{key}'.")
    return {
        "chunk_id": chunk_id,
        "title": title,
        "content": content,
        "metadata": metadata,
    }


def _upsert_catalog_document(
    *,
    doc_id: str,
    chunk_id: str,
    title: str,
    content: str,
    source_repo: str,
    source_commit: str,
    source_type: str,
    metadata: dict[str, Any],
) -> None:
    content_hash = _sha256_text(content)
    identifiers = {
        "catalog_source_repo": source_repo,
        "catalog_chunk_id": chunk_id,
        "serviceID": metadata.get("serviceID"),
        "cell": metadata.get("cell"),
        "contract": metadata.get("contract"),
        "status": metadata.get("status"),
    }
    meta_sources = {
        "source": "rag.catalog.publish",
        "source_repo": source_repo,
        "source_commit": source_commit,
        "chunk_metadata": metadata,
    }
    sql = text(
        """
        INSERT INTO documents(
          doc_id, title, author, year, source_type, content_hash,
          publisher, url, language, identifiers, meta_sources, file_path,
          doc_state, doc_version, state_reason, tombstoned_at, updated_at
        )
        VALUES (
          :doc_id, :title, NULL, NULL, :source_type, :content_hash,
          :publisher, NULL, :language,
          CAST(:identifiers AS jsonb), CAST(:meta_sources AS jsonb), NULL,
          'active', 1, NULL, NULL, now()
        )
        ON CONFLICT (doc_id) DO UPDATE SET
          title = EXCLUDED.title,
          source_type = EXCLUDED.source_type,
          content_hash = EXCLUDED.content_hash,
          publisher = EXCLUDED.publisher,
          language = EXCLUDED.language,
          identifiers = EXCLUDED.identifiers,
          meta_sources = EXCLUDED.meta_sources,
          doc_state = 'active',
          state_reason = NULL,
          tombstoned_at = NULL,
          updated_at = now(),
          doc_version = CASE
            WHEN documents.content_hash IS DISTINCT FROM EXCLUDED.content_hash
              OR COALESCE(documents.doc_state, 'active') <> 'active'
            THEN documents.doc_version + 1
            ELSE documents.doc_version
          END
        """
    )
    with engine().begin() as conn:
        conn.execute(
            sql,
            {
                "doc_id": doc_id,
                "title": title,
                "source_type": source_type,
                "content_hash": content_hash,
                "publisher": source_repo,
                "language": "en",
                "identifiers": _json(identifiers),
                "meta_sources": _json(meta_sources),
            },
        )

    chunk_record_id = _catalog_chunk_id(doc_id)
    chunk_sql = text(
        """
        INSERT INTO chunks(chunk_id, doc_id, section_path, ordinal, content, content_tsv)
        VALUES (:chunk_id, :doc_id, :section_path, 0, :content, to_tsvector('simple', :content))
        ON CONFLICT (chunk_id) DO UPDATE SET
          section_path = EXCLUDED.section_path,
          ordinal = EXCLUDED.ordinal,
          content = EXCLUDED.content,
          content_tsv = EXCLUDED.content_tsv
        """
    )
    with engine().begin() as conn:
        conn.execute(
            chunk_sql,
            {
                "chunk_id": chunk_record_id,
                "doc_id": doc_id,
                "section_path": chunk_id,
                "content": content.replace("\x00", ""),
            },
        )

    vec = default_embedder().embed([content])[0]
    upsert_embedding(chunk_record_id, vec)


def _tombstone_missing_catalog_docs(
    *,
    source_repo: str,
    source_type: str,
    keep_doc_ids: set[str],
) -> int:
    select_sql = text(
        """
        SELECT doc_id
        FROM documents
        WHERE source_type = :source_type
          AND COALESCE(doc_state, 'active') = 'active'
          AND identifiers->>'catalog_source_repo' = :source_repo
        """
    )
    update_sql = text(
        """
        UPDATE documents
        SET doc_state = 'tombstone',
            state_reason = 'removed_from_catalog_publish',
            tombstoned_at = COALESCE(tombstoned_at, now()),
            updated_at = now(),
            doc_version = doc_version + 1
        WHERE doc_id = :doc_id
        """
    )
    changed = 0
    with engine().begin() as conn:
        rows = conn.execute(
            select_sql,
            {"source_type": source_type, "source_repo": source_repo},
        ).mappings().all()
        for row in rows:
            doc_id = str(row["doc_id"])
            if doc_id in keep_doc_ids:
                continue
            conn.execute(update_sql, {"doc_id": doc_id})
            changed += 1
    return changed


def catalog_status(case_id: str, source_repo: str, source_type: str) -> dict[str, Any]:
    _require_case_source_type(case_id, source_type)
    sql = text(
        """
        SELECT
          COUNT(*) FILTER (WHERE COALESCE(doc_state, 'active') = 'active') AS active_docs,
          COUNT(*) FILTER (WHERE doc_state = 'tombstone') AS tombstoned_docs,
          COUNT(*) AS total_docs,
          MAX(updated_at) AS updated_at
        FROM documents
        WHERE source_type = :source_type
          AND identifiers->>'catalog_source_repo' = :source_repo
        """
    )
    latest_sql = text(
        """
        SELECT meta_sources->>'source_commit' AS source_commit
        FROM documents
        WHERE source_type = :source_type
          AND identifiers->>'catalog_source_repo' = :source_repo
        ORDER BY updated_at DESC NULLS LAST, doc_id
        LIMIT 1
        """
    )
    with engine().begin() as conn:
        row = conn.execute(
            sql,
            {"source_type": source_type, "source_repo": source_repo},
        ).mappings().first()
        latest = conn.execute(
            latest_sql,
            {"source_type": source_type, "source_repo": source_repo},
        ).mappings().first()
    return {
        "ok": True,
        "case_id": case_id,
        "source_repo": source_repo,
        "source_type": source_type,
        "source_commit": (latest or {}).get("source_commit"),
        "active_docs": int((row or {}).get("active_docs") or 0),
        "tombstoned_docs": int((row or {}).get("tombstoned_docs") or 0),
        "total_docs": int((row or {}).get("total_docs") or 0),
        "updated_at": str((row or {}).get("updated_at") or "") or None,
        "errors": [],
    }


def publish_catalog(payload: dict[str, Any], *, actor: str | None = None) -> dict[str, Any]:
    case_id = str(payload.get("case_id") or "").strip()
    source_repo = str(payload.get("source_repo") or "").strip()
    source_commit = str(payload.get("source_commit") or "working-tree").strip()
    source_type = str(payload.get("source_type") or "").strip()
    replace_source = bool(payload.get("replace_source", True))
    dry_run = bool(payload.get("dry_run", False))
    raw_chunks = payload.get("chunks") or []
    if not case_id:
        raise ValueError("case_id is required.")
    if not source_repo:
        raise ValueError("source_repo is required.")
    if not source_type:
        raise ValueError("source_type is required.")
    if not isinstance(raw_chunks, list) or not raw_chunks:
        raise ValueError("chunks must be a non-empty list.")
    _require_case_source_type(case_id, source_type)
    chunks = [_normalize_chunk(c) for c in raw_chunks]
    doc_ids = {_catalog_doc_id(source_repo, c["chunk_id"]) for c in chunks}
    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "case_id": case_id,
            "source_repo": source_repo,
            "source_type": source_type,
            "source_commit": source_commit,
            "published_chunks": len(chunks),
            "active_docs": len(doc_ids),
            "tombstoned_docs": 0,
            "errors": [],
            "updated_at": _now_iso(),
        }
    for chunk in chunks:
        _upsert_catalog_document(
            doc_id=_catalog_doc_id(source_repo, chunk["chunk_id"]),
            chunk_id=chunk["chunk_id"],
            title=chunk["title"],
            content=chunk["content"],
            source_repo=source_repo,
            source_commit=source_commit,
            source_type=source_type,
            metadata=chunk["metadata"],
        )
    tombstoned = (
        _tombstone_missing_catalog_docs(
            source_repo=source_repo,
            source_type=source_type,
            keep_doc_ids=doc_ids,
        )
        if replace_source
        else 0
    )
    status = catalog_status(case_id, source_repo, source_type)
    status.update(
        {
            "published_chunks": len(chunks),
            "tombstoned_docs": tombstoned,
            "actor": actor,
            "source_commit": source_commit,
            "updated_at": _now_iso(),
        }
    )
    return status


def reindex_catalog(case_id: str, source_repo: str, source_type: str) -> dict[str, Any]:
    _require_case_source_type(case_id, source_type)
    sql = text(
        """
        SELECT c.chunk_id, c.content
        FROM chunks c
        JOIN documents d ON d.doc_id = c.doc_id
        WHERE d.source_type = :source_type
          AND COALESCE(d.doc_state, 'active') = 'active'
          AND d.identifiers->>'catalog_source_repo' = :source_repo
        ORDER BY c.doc_id, c.ordinal, c.chunk_id
        """
    )
    with engine().begin() as conn:
        rows = conn.execute(
            sql,
            {"source_type": source_type, "source_repo": source_repo},
        ).mappings().all()
    contents = [str(row["content"]) for row in rows]
    if contents:
        vecs = default_embedder().embed(contents)
        for row, vec in zip(rows, vecs):
            upsert_embedding(str(row["chunk_id"]), vec)
    status = catalog_status(case_id, source_repo, source_type)
    status["reindexed_chunks"] = len(rows)
    status["updated_at"] = _now_iso()
    return status


def _safe_filename(name: str) -> str:
    cleaned = _SAFE_FILENAME_RE.sub("_", Path(name).name.strip())
    return cleaned or "media.bin"


def _media_status_query(case_id: str, source_repo: str | None, source_type: str) -> dict[str, Any]:
    _require_case_source_type(case_id, source_type)
    clauses = ["source_type = :source_type", "identifiers ? 'media_id'"]
    params: dict[str, Any] = {"source_type": source_type}
    if source_repo:
        clauses.append("identifiers->>'media_source_repo' = :source_repo")
        params["source_repo"] = source_repo
    sql = text(
        f"""
        SELECT
          COUNT(*) FILTER (WHERE COALESCE(doc_state, 'active') = 'active') AS active_docs,
          COUNT(*) FILTER (WHERE doc_state = 'tombstone') AS tombstoned_docs,
          COUNT(*) AS total_docs,
          MAX(updated_at) AS updated_at
        FROM documents
        WHERE {' AND '.join(clauses)}
        """
    )
    with engine().begin() as conn:
        row = conn.execute(sql, params).mappings().first()
    return {
        "ok": True,
        "case_id": case_id,
        "source_repo": source_repo,
        "source_type": source_type,
        "active_docs": int((row or {}).get("active_docs") or 0),
        "tombstoned_docs": int((row or {}).get("tombstoned_docs") or 0),
        "total_docs": int((row or {}).get("total_docs") or 0),
        "updated_at": str((row or {}).get("updated_at") or "") or None,
        "errors": [],
    }


def media_status(case_id: str, source_repo: str | None, source_type: str) -> dict[str, Any]:
    return _media_status_query(case_id, source_repo, source_type)


def _validate_media_extension(filename: str, mime_type: str | None) -> None:
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_MEDIA_EXTENSIONS:
        raise ValueError(f"Unsupported media extension '{suffix}'.")
    if not mime_type:
        return
    allowed = {
        ".md": {"text/markdown", "text/plain", "application/octet-stream"},
        ".markdown": {"text/markdown", "text/plain", "application/octet-stream"},
        ".txt": {"text/plain", "application/octet-stream"},
        ".html": {"text/html", "application/xhtml+xml", "application/octet-stream"},
        ".htm": {"text/html", "application/xhtml+xml", "application/octet-stream"},
        ".pdf": {"application/pdf", "application/octet-stream"},
        ".docx": {
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/octet-stream",
        },
    }
    if mime_type not in allowed.get(suffix, set()):
        raise ValueError(f"mime_type '{mime_type}' does not match extension '{suffix}'.")


def publish_media(payload: dict[str, Any], *, actor: str | None = None) -> dict[str, Any]:
    case_id = str(payload.get("case_id") or "").strip()
    source_type = str(payload.get("source_type") or "").strip()
    media = payload.get("media") or {}
    metadata = payload.get("metadata") or {}
    if not isinstance(media, dict):
        raise ValueError("media must be an object.")
    if not isinstance(metadata, dict):
        raise ValueError("metadata must be an object.")
    if not case_id:
        raise ValueError("case_id is required.")
    if not source_type:
        raise ValueError("source_type is required.")
    _require_case_source_type(case_id, source_type)

    filename = _safe_filename(str(media.get("filename") or "media.bin"))
    mime_type = str(media.get("mime_type") or "").strip() or None
    _validate_media_extension(filename, mime_type)
    delivery = media.get("delivery") or {}
    if not isinstance(delivery, dict):
        raise ValueError("media.delivery must be an object.")
    mode = str(delivery.get("mode") or "").strip()
    if mode != "inlineBase64":
        raise ValueError("Only inlineBase64 delivery is supported in v1.")
    encoded = str(delivery.get("bytes_base64") or "").strip()
    if not encoded:
        raise ValueError("inlineBase64 delivery requires bytes_base64.")
    try:
        data = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise ValueError("bytes_base64 is not valid base64.") from exc
    if len(data) > MAX_INLINE_MEDIA_BYTES:
        raise ValueError(f"inlineBase64 media exceeds {MAX_INLINE_MEDIA_BYTES} bytes.")
    declared_size = media.get("size_bytes")
    if declared_size is not None and int(declared_size) != len(data):
        raise ValueError("size_bytes does not match decoded media bytes.")
    sha256 = str(media.get("sha256") or "").strip().lower()
    actual_sha256 = _sha256_bytes(data)
    if sha256 and sha256 != actual_sha256:
        raise ValueError("sha256 does not match decoded media bytes.")
    media_id = str(media.get("media_id") or f"sha256:{actual_sha256}").strip()

    root = Path(settings.ingest_root).expanduser().resolve(strict=False)
    media_root = (root / "cell_media" / source_type).resolve(strict=False)
    if root != media_root and root not in media_root.parents:
        raise ValueError("Resolved media path escapes ingest root.")
    media_root.mkdir(parents=True, exist_ok=True)
    path = media_root / f"{actual_sha256[:16]}-{filename}"
    path.write_bytes(data)

    doc_id = ingest_file(path, source_type=source_type)
    identifiers = {
        "media_id": media_id,
        "media_sha256": actual_sha256,
        "media_filename": filename,
        "media_mime_type": mime_type,
        "media_source_repo": metadata.get("source_repo"),
        "subject_kind": metadata.get("subject_kind"),
    }
    meta_sources = {
        "source": "rag.media.publish",
        "metadata": metadata,
        "actor": actor,
    }
    update_sql = text(
        """
        UPDATE documents
        SET identifiers = CAST(:identifiers AS jsonb),
            meta_sources = CAST(:meta_sources AS jsonb),
            publisher = COALESCE(:publisher, publisher),
            updated_at = now()
        WHERE doc_id = :doc_id
        """
    )
    with engine().begin() as conn:
        conn.execute(
            update_sql,
            {
                "doc_id": doc_id,
                "identifiers": _json(identifiers),
                "meta_sources": _json(meta_sources),
                "publisher": metadata.get("source_repo"),
            },
        )
    status = media_status(case_id, metadata.get("source_repo"), source_type)
    status.update(
        {
            "media_id": media_id,
            "doc_id": doc_id,
            "sha256": actual_sha256,
            "filename": filename,
            "size_bytes": len(data),
            "actor": actor,
            "updated_at": _now_iso(),
        }
    )
    return status
