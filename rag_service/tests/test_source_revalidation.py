"""PostgreSQL integration checks. Set SOURCE_REVALIDATION_TEST_DSN to a disposable database."""
import hashlib
import os
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, text

from app.rag.index import source_revalidation as checks
from app.rag.ingest.chunker import chunk_text
from app.rag.ingest.cleaner import clean_text
from app.rag.ingest.metadata import compute_hash, make_doc_id


DSN = os.environ.get("SOURCE_REVALIDATION_TEST_DSN")


@unittest.skipUnless(DSN, "requires a disposable PostgreSQL database")
class TestSourceRevalidation(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        self.enterContext(patch.object(checks.settings, "ingest_root", str(self.root)))
        schema = "revalidation_test_" + uuid.uuid4().hex
        admin = create_engine(DSN)
        self.addCleanup(admin.dispose)
        with admin.begin() as conn:
            conn.exec_driver_sql(f'CREATE SCHEMA "{schema}"')
        def cleanup_schema():
            with admin.begin() as conn:
                conn.exec_driver_sql(f'DROP SCHEMA "{schema}" CASCADE')
        self.addCleanup(cleanup_schema)
        self.db = create_engine(DSN, connect_args={"options": "-csearch_path=" + schema})
        self.addCleanup(self.db.dispose)
        self.enterContext(patch.object(checks, "engine", return_value=self.db))
        migration = (Path(checks.__file__).parent / "migrations/0003_document_source_revalidation.sql")
        with self.db.begin() as conn:
            conn.exec_driver_sql("""
                CREATE TABLE documents (doc_id text PRIMARY KEY, content_hash text, doc_version int,
                    updated_at timestamptz, source_type text, file_path text, doc_state text);
                CREATE TABLE chunks (chunk_id text PRIMARY KEY, doc_id text REFERENCES documents ON DELETE CASCADE,
                    section_path text, ordinal int, content text, content_tsv tsvector);
                CREATE TABLE embeddings (chunk_id text PRIMARY KEY REFERENCES chunks ON DELETE CASCADE, embedding real[]);
            """)
            conn.execute(text(migration.read_text()))
            conn.execute(text(migration.read_text()))

    def source(self, folder, name, source_type="science"):
        path = self.root / folder / name
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(b"# Findings\r\n\r\n  Results are recorded.\r\n")
        return {"path": str(path), "source_type": source_type, "source_path": "reports/" + name,
                "raw_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

    def index(self, entry):
        path = Path(entry["path"])
        cleaned = clean_text(path.read_text())
        digest = compute_hash(cleaned)
        doc_id = make_doc_id(path, digest)
        with self.db.begin() as conn:
            conn.execute(text("""
                INSERT INTO documents VALUES
                    (:doc_id, :digest, 1, '2025-01-01 00:00:00+00', :source_type, :path, 'active')
            """), {**entry, "doc_id": doc_id, "digest": digest})
            for ch in chunk_text(doc_id, cleaned):
                conn.execute(text("""
                    INSERT INTO chunks VALUES (:chunk_id, :doc_id, :section_path, :ordinal,
                        :content, to_tsvector('simple', :content))
                """), vars(ch))
                conn.execute(text("""
                    INSERT INTO embeddings VALUES (:chunk_id, ARRAY[0.1]::real[])
                """), vars(ch))

    def count(self):
        with self.db.begin() as conn:
            return conn.exec_driver_sql("SELECT COUNT(*) FROM document_source_revalidations").scalar_one()

    def test_aliases_preserve_ingestion_time_and_corruption_invalidates(self):
        first = self.source("research", "round.md", "research")
        active = self.source("science", "round.md")
        self.index(active)
        revision = "a" * 40
        result = checks.revalidate_sources([first, active], revision)
        self.assertEqual((result["verified_files"], result["verified_docs"], result["verified_chunks"]),
                         (2, 1, 1))
        attested = result["documents"][0]
        self.assertEqual(attested["file_path"], active["path"])
        self.assertEqual(attested["source_sha256"], first["raw_sha256"])
        self.assertNotEqual(attested["content_hash"], first["raw_sha256"])
        with self.db.begin() as conn:
            unchanged = conn.exec_driver_sql("""
                SELECT r.doc_updated_at = d.updated_at AND d.updated_at < r.verified_at
                FROM documents d JOIN document_source_revalidations r USING (doc_id)
            """).scalar_one()
            self.assertTrue(unchanged)
            conn.exec_driver_sql("UPDATE chunks SET content = 'damaged'")
        self.assertEqual(self.count(), 0)
        with self.assertRaises(checks.RevalidationError):
            checks.revalidate_sources([first, active], revision)
        self.assertEqual(self.count(), 0)

    def test_raw_byte_mismatch_and_duplicate_manifest_paths(self):
        entry = self.source("science", "round.md")
        self.index(entry)
        with self.assertRaises(checks.RevalidationError):
            checks.revalidate_sources([entry, entry], "b" * 40)
        path = Path(entry["path"])
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
        with self.assertRaisesRegex(checks.RevalidationError, "Source bytes differ"):
            checks.revalidate_sources([entry], "b" * 40)
        self.assertEqual(self.count(), 0)

    def test_missing_embedding_rolls_back_whole_batch(self):
        first = self.source("science", "a.md")
        last = self.source("science", "z.md")
        self.index(first)
        self.index(last)
        checks.revalidate_sources([last], "b" * 40)
        with self.db.begin() as conn:
            conn.execute(text("DELETE FROM embeddings WHERE chunk_id LIKE :pattern"), {"pattern": "z-%"})
        self.assertEqual(self.count(), 0)
        with self.assertRaises(checks.RevalidationError):
            checks.revalidate_sources([first, last], "c" * 40)
        self.assertEqual(self.count(), 0)

    def test_moved_index_path_and_wrong_revision_fail(self):
        actual = self.source("actual", "round.md")
        other = self.source("other", "round.md")
        self.index(actual)
        with self.assertRaises(checks.RevalidationError):
            checks.revalidate_sources([other], "a" * 40)
        with self.assertRaises(checks.RevalidationError):
            checks.revalidate_sources([actual], "working-tree")
        self.assertEqual(self.count(), 0)

    def test_losing_sole_member_of_source_type_invalidates_remaining_proof(self):
        first = self.source("research", "a.md", "research")
        second = self.source("science", "z.md")
        self.index(first)
        self.index(second)
        for mutation in ("UPDATE documents SET doc_state = 'tombstone'",
                         "UPDATE documents SET source_type = 'moved'",
                         "DELETE FROM documents"):
            checks.revalidate_sources([first, second], "a" * 40)
            with self.db.begin() as conn:
                conn.execute(text(mutation + " WHERE file_path = :path"), first)
            self.assertEqual(self.count(), 0)
            with self.db.begin() as conn:
                conn.execute(text("""
                    UPDATE documents SET doc_state = 'active', source_type = 'research'
                    WHERE file_path = :path
                """), first)
