CREATE TABLE IF NOT EXISTS rag_research_rate_limits (
  token_fingerprint TEXT NOT NULL,
  window_start TIMESTAMPTZ NOT NULL,
  used INTEGER NOT NULL DEFAULT 0,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (token_fingerprint, window_start)
);

CREATE INDEX IF NOT EXISTS rag_research_rate_limits_updated_at_idx
  ON rag_research_rate_limits(updated_at);
