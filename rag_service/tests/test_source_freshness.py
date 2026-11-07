from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine

from app.api import research_hardening


@pytest.fixture
def corpus(monkeypatch):
    db = create_engine("sqlite://")
    recent = datetime.now(timezone.utc) - timedelta(minutes=2)
    old = recent - timedelta(days=3)
    with db.begin() as conn:
        conn.exec_driver_sql("""CREATE TABLE documents (
            doc_id TEXT PRIMARY KEY, content_hash TEXT, file_path TEXT, source_type TEXT,
            doc_state TEXT, doc_version INTEGER, updated_at TEXT
        )""")
        conn.exec_driver_sql("""CREATE TABLE document_source_revalidations (
            doc_id TEXT PRIMARY KEY, content_hash TEXT, file_path TEXT, source_type TEXT,
            doc_version INTEGER, doc_updated_at TEXT, source_revision TEXT, verified_at TEXT
        )""")
        conn.exec_driver_sql(
            "INSERT INTO documents VALUES (?, ?, ?, ?, 'active', 1, ?)",
            [
                ("a", "hash-a", "/a", "reports", old.isoformat(" ")),
                ("b", "hash-b", "/b", "results", old.isoformat(" ")),
                ("outside", "third", "/other", "other_case", recent.isoformat(" ")),
            ],
        )
        conn.exec_driver_sql(
            """INSERT INTO document_source_revalidations
               SELECT doc_id, content_hash, file_path, source_type, doc_version, updated_at, ?, ?
               FROM documents WHERE doc_id IN ('a', 'b')""",
            ("a" * 40, recent.isoformat(" ")),
        )
    monkeypatch.setattr(research_hardening, "engine", lambda: db)
    monkeypatch.setattr(research_hardening, "_case_source_types", lambda _: ["reports", "results"])
    monkeypatch.setattr(research_hardening.settings, "research_freshness_max_age_seconds", 86400)
    yield db
    db.dispose()


def test_complete_case_revalidation_preserves_the_document_update_date(corpus):
    outcome = research_hardening.corpus_freshness("test")
    assert outcome["ok"]
    assert outcome["age_basis"] == "oldest_complete_source_revalidation"
    assert outcome["revalidated_docs"] == outcome["active_docs"] == 2
    assert outcome["revalidation_source_revision"] == "a" * 40
    assert outcome["newest_updated_at"] < outcome["oldest_source_verified_at"]


@pytest.mark.parametrize("mutation", [
    "DELETE FROM document_source_revalidations WHERE doc_id = 'b'",
    "UPDATE document_source_revalidations SET source_revision = 'different' WHERE doc_id = 'b'",
    "UPDATE documents SET content_hash = 'changed' WHERE doc_id = 'b'",
    "UPDATE documents SET doc_version = 2 WHERE doc_id = 'b'",
    "UPDATE documents SET file_path = '/moved' WHERE doc_id = 'b'",
    "UPDATE documents SET source_type = 'reports' WHERE doc_id = 'b'",
    "UPDATE documents SET updated_at = '2001-01-01 00:00:00+00:00' WHERE doc_id = 'b'",
    "UPDATE document_source_revalidations SET verified_at = '2999-01-01' WHERE doc_id = 'b'",
])
def test_incomplete_or_mismatched_evidence_cannot_refresh_a_stale_case(corpus, mutation):
    with corpus.begin() as conn:
        conn.exec_driver_sql(mutation)
    outcome = research_hardening.corpus_freshness("test")
    assert not outcome["ok"]
    assert not outcome["revalidation_complete"]
    assert outcome["revalidation_source_revision"] is None
    assert outcome["age_basis"] == "newest_document_update"
    assert outcome["violations"][0]["rule"] == "corpus_stale"


def test_oldest_attestation_bounds_verified_case_age(corpus):
    stale = datetime.now(timezone.utc) - timedelta(days=2)
    with corpus.begin() as conn:
        conn.exec_driver_sql(
            "UPDATE document_source_revalidations SET verified_at = ? WHERE doc_id = 'b'",
            (stale.isoformat(" "),),
        )
    outcome = research_hardening.corpus_freshness("test")
    assert outcome["revalidation_complete"]
    assert outcome["age_basis"] == "oldest_complete_source_revalidation"
    assert not outcome["ok"]
    assert outcome["violations"][0]["rule"] == "corpus_stale"


def test_pending_tombstone_blocks_even_a_fully_verified_active_set(corpus):
    with corpus.begin() as conn:
        conn.exec_driver_sql("UPDATE documents SET doc_state = 'tombstone_pending' WHERE doc_id = 'b'")
    outcome = research_hardening.corpus_freshness("test")
    assert outcome["revalidated_docs"] == outcome["active_docs"] == 1
    assert not outcome["ok"]
    assert outcome["violations"] == [{"rule": "tombstone_pending_documents", "actual": 1}]


def test_recent_ingest_still_satisfies_the_existing_age_rule(corpus):
    recent = datetime.now(timezone.utc) - timedelta(minutes=1)
    with corpus.begin() as conn:
        conn.exec_driver_sql("DELETE FROM document_source_revalidations")
        conn.exec_driver_sql("UPDATE documents SET updated_at = ? WHERE doc_id = 'b'", (recent.isoformat(" "),))
    outcome = research_hardening.corpus_freshness("test")
    assert outcome["ok"]
    assert outcome["revalidated_docs"] == 0
    assert outcome["age_basis"] == "newest_document_update"
