"""Find the opening of a report named in the original question and already retrieved."""

import re

from sqlalchemy import bindparam, text

from app.rag.cases.loader import case_by_id, load_rag_cases
from app.rag.index.db import engine
from app.rag.retrieve.hybrid import RetrievedChunk, _row_to_chunk
from app.settings import settings


def named_report_leads(
    question: str, candidates: list[RetrievedChunk], filters: dict, case_id: str | None,
) -> list[RetrievedChunk]:
    reports = {}
    scores = {}
    for chunk in candidates:
        title = (chunk.title or "").lower()
        name = title.removesuffix("_report")
        if name and name != title and re.search(
            rf"(?<!\w){re.escape(name)}(?:_report)?(?!\w)", question, re.IGNORECASE
        ):
            reports[chunk.doc_id] = (chunk.title, chunk.source_type)
            if chunk.ordinal == 0:
                scores[chunk.chunk_id] = chunk.score

    if "doc_id" in filters:
        reports = {key: value for key, value in reports.items() if key in filters["doc_id"]}
    if not reports:
        return []

    # Candidate IDs restrict this lookup even for a multi-query plan. Intersect
    # the selected case with the effective source filter, including legacy routing.
    source_types = filters.get("source_type")
    if case_id:
        case = case_by_id(load_rag_cases(settings.rag_cases_path), case_id)
        case_types = set(case.planner.docs_source_types + case.planner.prompts_source_types)
        source_types = case_types if source_types is None else case_types.intersection(source_types)

    clauses = ["d.doc_id IN :ids", "c.ordinal = 0", "COALESCE(d.doc_state, 'active') = 'active'"]
    params = {"ids": list(reports)}
    binds = [bindparam("ids", expanding=True)]
    if source_types is not None:
        if not source_types:
            return []
        clauses.append("d.source_type IN :sources")
        params["sources"] = sorted(source_types)
        binds.append(bindparam("sources", expanding=True))
    if "year_gte" in filters:
        clauses.append("d.year >= :year")
        params["year"] = int(filters["year_gte"])
    sql = text(f"""
        SELECT c.chunk_id, c.doc_id, c.ordinal, d.title, d.author, d.year, d.source_type,
               d.publisher, d.url, d.language, d.identifiers, c.content, 0.0 AS score
        FROM chunks c JOIN documents d ON d.doc_id = c.doc_id
        WHERE {" AND ".join(clauses)}
        ORDER BY d.doc_id, c.chunk_id
    """).bindparams(*binds)
    with engine().begin() as conn:
        rows = conn.execute(sql, params).fetchall()
    leads = []
    for row in rows:
        lead = _row_to_chunk(row, "named_report_lead")
        if reports.get(lead.doc_id) == (lead.title, lead.source_type):
            lead.score = scores.get(lead.chunk_id, 0.0)
            leads.append(lead)
    return leads
