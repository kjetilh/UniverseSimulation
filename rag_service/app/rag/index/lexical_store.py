import re

from sqlalchemy import text
from app.rag.index.db import engine


_TOKEN_RE = re.compile(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ_]+")
_VERSION_TOKEN_RE = re.compile(r"\bv\d+[a-z]{1,3}\b", re.IGNORECASE)
_STOPWORDS = {
    "a",
    "about",
    "an",
    "and",
    "as",
    "av",
    "ble",
    "de",
    "den",
    "det",
    "en",
    "er",
    "et",
    "for",
    "fra",
    "from",
    "how",
    "hva",
    "hvem",
    "hvilke",
    "hvilken",
    "hvor",
    "hvordan",
    "hvorfor",
    "i",
    "in",
    "is",
    "med",
    "of",
    "og",
    "om",
    "on",
    "på",
    "som",
    "the",
    "til",
    "to",
    "var",
    "was",
    "were",
    "what",
    "where",
    "which",
    "who",
    "why",
    "with",
}


def _websearch_query(query: str) -> str:
    tokens: list[str] = []
    seen: set[str] = set()
    for raw in _TOKEN_RE.findall(query.lower()):
        if len(raw) < 2 or raw in _STOPWORDS or raw in seen:
            continue
        seen.add(raw)
        tokens.append(raw)
        if len(tokens) >= 32:
            break
    if not tokens:
        tokens = [raw.lower() for raw in _TOKEN_RE.findall(query)[:8] if len(raw) >= 2]
    return " OR ".join(tokens)


def _version_title_patterns(query: str) -> list[str]:
    return [f"%{token}%" for token in dict.fromkeys(_VERSION_TOKEN_RE.findall(query.lower()))]


def lexical_search(query: str, top_k: int = 50, filters: dict | None = None):
    filters = filters or {}
    where = [
        "c.content_tsv @@ websearch_to_tsquery('simple', :lexical_q)",
        "COALESCE(d.doc_state, 'active') = 'active'",
    ]
    params = {"lexical_q": _websearch_query(query), "top_k": top_k}
    title_patterns = _version_title_patterns(query)
    if title_patterns:
        title_boost_sql = "CASE WHEN d.title ILIKE ANY(:title_patterns) THEN 2.0 ELSE 0.0 END"
        params["title_patterns"] = title_patterns
    else:
        title_boost_sql = "0.0"

    if "year_gte" in filters:
        where.append("d.year >= :year_gte")
        params["year_gte"] = int(filters["year_gte"])
    if "source_type" in filters:
        where.append("d.source_type = ANY(:source_type)")
        params["source_type"] = filters["source_type"]
    if "doc_id" in filters:
        where.append("d.doc_id = ANY(:doc_id)")
        params["doc_id"] = filters["doc_id"]

    where_sql = "WHERE " + " AND ".join(where)

    sql = f'''
    SELECT c.chunk_id, c.doc_id, c.ordinal, d.title, d.author, d.year, d.source_type,
           d.publisher, d.url, d.language, d.identifiers,
           c.content,
           ts_rank_cd(c.content_tsv, websearch_to_tsquery('simple', :lexical_q))
             + {title_boost_sql} AS score
    FROM chunks c
    JOIN documents d ON d.doc_id = c.doc_id
    {where_sql}
    ORDER BY score DESC, c.doc_id, c.ordinal, c.chunk_id
    LIMIT :top_k
    '''
    with engine().begin() as conn:
        return conn.execute(text(sql), params).fetchall()
