"""Verify release files against their indexed representation before recording freshness."""

from __future__ import annotations

import hashlib
import re
import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from sqlalchemy import text
from sqlalchemy.engine import Connection

from app.rag.index.db import engine
from app.rag.ingest.chunker import Chunk, chunk_text
from app.rag.ingest.cleaner import clean_text
from app.rag.ingest.loaders import load_any
from app.rag.ingest.metadata import compute_hash, make_doc_id
from app.settings import settings


class RevalidationError(ValueError):
    """A release file or its indexed representation failed verification."""


@dataclass
class Mirror:
    path: Path
    source_type: str
    source_path: str
    raw_sha256: str
    stat_key: tuple[int, ...]


def _stat_key(path: Path) -> tuple[int, ...]:
    st = path.lstat()
    if not stat.S_ISREG(st.st_mode):
        raise RevalidationError(f"Expected a regular source file: {path}")
    return st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns


def _read_manifest(files: list[dict[str, str]]) -> dict[str, list[Mirror]]:
    if not files:
        raise RevalidationError("Empty source manifest")
    groups: dict[str, list[Mirror]] = {}
    seen: set[Path] = set()
    root = Path(settings.ingest_root).resolve(strict=True)
    for entry in files:
        path = Path(entry["path"])
        source_path = entry["source_path"]
        repo_path = PurePosixPath(source_path)
        if (repo_path.is_absolute() or ".." in repo_path.parts
                or not repo_path.parts or str(repo_path) != source_path):
            raise RevalidationError(f"Invalid repository path: {source_path}")
        if not path.is_absolute() or path.resolve(strict=True) != path or not path.is_relative_to(root):
            raise RevalidationError(f"Invalid mirror path: {path}")
        if path in seen or not entry["source_type"].strip():
            raise RevalidationError(f"Duplicate mirror or missing source type: {path}")
        if path.name != repo_path.name:
            raise RevalidationError(f"Mirror filename differs from release source: {path}")
        raw_sha256 = entry["raw_sha256"]
        if not re.fullmatch(r"[0-9a-f]{64}", raw_sha256):
            raise RevalidationError(f"Invalid source digest: {source_path}")
        stat_key = _stat_key(path)
        if hashlib.sha256(path.read_bytes()).hexdigest() != raw_sha256:
            raise RevalidationError(f"Source bytes differ from the release: {path}")
        mirrors = groups.setdefault(source_path, [])
        if mirrors and mirrors[0].raw_sha256 != raw_sha256:
            raise RevalidationError(f"Release aliases disagree: {source_path}")
        mirrors.append(Mirror(path, entry["source_type"], source_path, raw_sha256, stat_key))
        seen.add(path)
    return groups


def _verify_chunks(conn: Connection, doc_id: str, chunks: list[Chunk]) -> None:
    rows = conn.execute(text("""
        SELECT c.chunk_id, c.ordinal, c.section_path, c.content,
               (c.content_tsv = to_tsvector('simple', c.content)) IS TRUE AS lexical_ok,
               e.chunk_id IS NOT NULL AS has_embedding
        FROM chunks c LEFT JOIN embeddings e USING (chunk_id)
        WHERE c.doc_id = :doc_id ORDER BY c.ordinal, c.chunk_id
    """), {"doc_id": doc_id}).mappings().all()
    if len(rows) != len(chunks):
        raise RevalidationError(f"Indexed chunk count differs for {doc_id}")
    for row, chunk in zip(rows, chunks):
        if ((row["chunk_id"], row["ordinal"], row["section_path"], row["content"]) !=
                (chunk.chunk_id, chunk.ordinal, chunk.section_path, chunk.content)
                or not row["lexical_ok"] or not row["has_embedding"]):
            raise RevalidationError(f"Chunk, lexical index or embedding differs for {chunk.chunk_id}")


def _verify_document(conn: Connection, mirrors: list[Mirror], doc_id: str,
                     content_hash: str, chunks: list[Chunk]) -> dict:
    aliases = {str(m.path): m.source_type for m in mirrors}
    rows = conn.execute(text("""
        SELECT doc_id, content_hash, doc_version, updated_at AS doc_updated_at,
               source_type, file_path
        FROM documents WHERE doc_state = 'active' AND
          (doc_id = :doc_id OR file_path = ANY(CAST(:paths AS text[])))
    """), {"doc_id": doc_id, "paths": list(aliases)}).mappings().all()
    if len(rows) != 1:
        raise RevalidationError(f"Expected exactly one active indexed document for {doc_id}")
    doc = dict(rows[0])
    if (doc["doc_id"] != doc_id or doc["content_hash"] != content_hash
            or doc["file_path"] not in aliases or aliases[doc["file_path"]] != doc["source_type"]):
        raise RevalidationError(f"Indexed document identity differs for {doc_id}")
    _verify_chunks(conn, doc_id, chunks)
    return {**doc, "source_path": mirrors[0].source_path, "source_sha256": mirrors[0].raw_sha256,
            "chunk_count": len(chunks)}


def revalidate_sources(files: list[dict[str, str]], source_revision: str) -> dict:
    """Commit one receipt per indexed document only after every check succeeds."""
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", source_revision):
        raise RevalidationError("Expected a full lowercase Git revision")
    groups = _read_manifest(files)
    expected = {}
    for source_path, mirrors in sorted(groups.items()):
        representative = mirrors[0].path
        clean = clean_text(load_any(representative))
        digest = compute_hash(clean)
        doc_id = make_doc_id(representative, digest)
        if doc_id in expected:
            raise RevalidationError(f"Distinct release paths produce the same doc_id: {source_path}")
        expected[doc_id] = (mirrors, digest, chunk_text(doc_id, clean))

    with engine().begin() as conn:
        # Keep the searchable rows stable through the receipt write. Ordinary
        # research reads remain available while ingestion waits for this batch.
        conn.execute(text("SET LOCAL lock_timeout = '10s'"))
        conn.execute(text("LOCK TABLE documents, chunks, embeddings IN SHARE MODE"))
        documents = [
            _verify_document(conn, mirrors, doc_id, digest, chunks)
            for doc_id, (mirrors, digest, chunks) in sorted(expected.items())
        ]
        for mirrors in groups.values():
            for mirror in mirrors:
                if (mirror.path.resolve(strict=True) != mirror.path
                        or _stat_key(mirror.path) != mirror.stat_key):
                    raise RevalidationError(f"Mirror changed during verification: {mirror.path}")
        verified_at = conn.execute(text("SELECT transaction_timestamp()")).scalar_one()
        for doc in documents:
            doc.update(source_revision=source_revision, verified_at=verified_at)
        conn.execute(text("""
            INSERT INTO document_source_revalidations
              (doc_id, doc_version, doc_updated_at, content_hash, source_type, file_path,
               source_path, source_sha256, source_revision, chunk_count, verified_at)
            VALUES (:doc_id, :doc_version, :doc_updated_at, :content_hash, :source_type, :file_path,
                    :source_path, :source_sha256, :source_revision, :chunk_count, :verified_at)
            ON CONFLICT (doc_id) DO UPDATE SET
              doc_version = EXCLUDED.doc_version, doc_updated_at = EXCLUDED.doc_updated_at,
              content_hash = EXCLUDED.content_hash, source_type = EXCLUDED.source_type,
              file_path = EXCLUDED.file_path, source_path = EXCLUDED.source_path,
              source_sha256 = EXCLUDED.source_sha256, source_revision = EXCLUDED.source_revision,
              chunk_count = EXCLUDED.chunk_count, verified_at = EXCLUDED.verified_at
        """), documents)
    return {
        "source_revision": source_revision, "verified_at": verified_at.isoformat(),
        "verified_files": len(files), "alias_files": len(files) - len(documents),
        "verified_docs": len(documents), "verified_chunks": sum(d["chunk_count"] for d in documents),
        "documents": [{**doc, "doc_updated_at": doc["doc_updated_at"].isoformat(),
                       "verified_at": verified_at.isoformat()} for doc in documents],
    }
