CREATE TABLE IF NOT EXISTS document_source_revalidations (
  doc_id TEXT PRIMARY KEY REFERENCES documents(doc_id) ON DELETE CASCADE,
  doc_version INT NOT NULL,
  doc_updated_at TIMESTAMPTZ NOT NULL,
  content_hash TEXT NOT NULL,
  source_type TEXT NOT NULL,
  file_path TEXT NOT NULL,
  source_path TEXT NOT NULL,
  source_sha256 TEXT NOT NULL CHECK (source_sha256 ~ '^[0-9a-f]{64}$'),
  source_revision TEXT NOT NULL CHECK (source_revision ~ '^([0-9a-f]{40}|[0-9a-f]{64})$'),
  chunk_count INT NOT NULL CHECK (chunk_count >= 0),
  verified_at TIMESTAMPTZ NOT NULL
);

-- An attestation describes a particular searchable representation. Ingestion uses
-- several transactions, so invalidate even if only a chunk or embedding was written.
CREATE OR REPLACE FUNCTION invalidate_document_source_revalidation() RETURNS TRIGGER
LANGUAGE plpgsql AS $$
DECLARE
  old_document TEXT;
  new_document TEXT;
BEGIN
  IF TG_OP = 'TRUNCATE' THEN
    DELETE FROM document_source_revalidations;
    RETURN NULL;
  END IF;
  IF TG_TABLE_NAME = 'documents' THEN
    -- Losing a sole member of a source type can shrink the case denominator.
    -- The remaining receipts cannot establish coverage of that changed corpus.
    IF TG_OP = 'DELETE' OR OLD.source_type IS DISTINCT FROM NEW.source_type
        OR OLD.doc_state IS DISTINCT FROM NEW.doc_state THEN
      DELETE FROM document_source_revalidations;
      RETURN NULL;
    END IF;
  END IF;
  IF TG_OP <> 'INSERT' THEN
    IF TG_TABLE_NAME = 'embeddings' THEN
      SELECT doc_id INTO old_document FROM chunks WHERE chunk_id = OLD.chunk_id;
    ELSE
      old_document := OLD.doc_id;
    END IF;
  END IF;
  IF TG_OP <> 'DELETE' THEN
    IF TG_TABLE_NAME = 'embeddings' THEN
      SELECT doc_id INTO new_document FROM chunks WHERE chunk_id = NEW.chunk_id;
    ELSE
      new_document := NEW.doc_id;
    END IF;
  END IF;
  DELETE FROM document_source_revalidations WHERE doc_id IN (old_document, new_document);
  RETURN NULL;
END;
$$;

DROP TRIGGER IF EXISTS invalidate_source_check ON documents;
CREATE TRIGGER invalidate_source_check AFTER UPDATE OR DELETE ON documents
FOR EACH ROW EXECUTE FUNCTION invalidate_document_source_revalidation();
DROP TRIGGER IF EXISTS invalidate_source_check ON chunks;
CREATE TRIGGER invalidate_source_check AFTER INSERT OR UPDATE OR DELETE ON chunks
FOR EACH ROW EXECUTE FUNCTION invalidate_document_source_revalidation();
DROP TRIGGER IF EXISTS invalidate_source_check ON embeddings;
CREATE TRIGGER invalidate_source_check AFTER INSERT OR UPDATE OR DELETE ON embeddings
FOR EACH ROW EXECUTE FUNCTION invalidate_document_source_revalidation();
DROP TRIGGER IF EXISTS invalidate_truncated_source_checks ON chunks;
CREATE TRIGGER invalidate_truncated_source_checks AFTER TRUNCATE ON chunks
FOR EACH STATEMENT EXECUTE FUNCTION invalidate_document_source_revalidation();
DROP TRIGGER IF EXISTS invalidate_truncated_source_checks ON embeddings;
CREATE TRIGGER invalidate_truncated_source_checks AFTER TRUNCATE ON embeddings
FOR EACH STATEMENT EXECUTE FUNCTION invalidate_document_source_revalidation();
