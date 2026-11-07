from types import SimpleNamespace

import pytest
from sqlalchemy import create_engine

from app.rag import pipeline
from app.rag.planner.deterministic import PlanResult
from app.rag.retrieve import named_report


def chunk(doc_id, title, ordinal, score, source_type="universe_experiments"):
    return SimpleNamespace(doc_id=doc_id, chunk_id=f"{doc_id}-{ordinal}", title=title,
                           ordinal=ordinal, score=score, content=f"Section {ordinal}",
                           source_type=source_type)


@pytest.fixture
def report_db(monkeypatch):
    db = create_engine("sqlite://")
    with db.begin() as conn:
        conn.exec_driver_sql("""CREATE TABLE documents (
            doc_id TEXT, title TEXT, author TEXT, year INTEGER, source_type TEXT, publisher TEXT,
            url TEXT, language TEXT, identifiers TEXT, doc_state TEXT)""")
        conn.exec_driver_sql("CREATE TABLE chunks (chunk_id TEXT, doc_id TEXT, ordinal INTEGER, content TEXT)")
        for doc_id, source, state in [
            ("result", "universe_experiments", "active"),
            ("other", "haven_service_catalog", "active"),
            ("stale", "universe_experiments", "tombstone_pending"),
            ("unretrieved", "universe_experiments", "active"),
        ]:
            conn.exec_driver_sql(
                "INSERT INTO documents(doc_id, title, year, source_type, doc_state) VALUES (?, ?, 2026, ?, ?)",
                (doc_id, "EX7_report", source, state),
            )
            conn.exec_driver_sql("INSERT INTO chunks VALUES (?, ?, 0, 'Whole-study summary')",
                                 (doc_id + "-0", doc_id))
    monkeypatch.setattr(named_report, "engine", lambda: db)
    yield
    db.dispose()


def test_normal_query_adds_lead_and_keeps_best_section_within_both_limits(report_db, monkeypatch):
    original = "Hva fant EX7?"
    candidates = [chunk("incidental", "Previous study", 4, 10),
                  chunk("result", "EX7_report", 2, 3), chunk("result", "EX7_report", 1, 2)]
    monkeypatch.setattr(pipeline, "_retrieve_candidates", lambda **_: (candidates, "rewritten text"))
    monkeypatch.setattr(pipeline, "resolve_effective_paths", lambda **_: ("p", "a", "p", "a"))
    captured = {}

    def compose(question, packed, **options):
        captured.update(question=question, context=packed.context_text, instruction=options["router_instruction"])
        return "Resultatet i rapporten [1]."

    monkeypatch.setattr(pipeline, "compose_answer", compose)
    plan = PlanResult(filters={"rag_case_id": "universe_project", "source_type": ["universe_experiments"]},
                      retrieval={"max_chunks_per_doc": 2, "top_k_final": 3},
                      trace={}, prompt_instruction=None, case_id=None, evaluation=None)
    result = pipeline._run_planned_single_pass(
        message=original, plan=plan, top_k=3, model_profile=None, prompt_profile_case_id=None,
    )
    assert [c.chunk_id for c in result.citations] == ["result-0", "result-2", "incidental-4"]
    assert captured["question"] == original
    assert captured["context"].startswith("[1] [result::result-0]\nWhole-study summary")
    assert result.retrieval_debug["named_report_lead_chunks"] == ["result-0"]
    assert result.citations[0].score == 0  # Additional context has no hybrid retrieval score.


def test_lookup_respects_case_year_source_doc_id_active_state_and_candidates(report_db):
    cands = [chunk("result", "EX7_report", 1, 2), chunk("stale", "EX7_report", 1, 2),
             chunk("other", "EX7_report", 1, 2, "haven_service_catalog")]
    allowed = {"source_type": ["universe_experiments", "haven_service_catalog"]}
    assert [c.doc_id for c in named_report.named_report_leads(
        "EX7_report.md", cands, allowed, "universe_project"
    )] == ["result"]
    for extra in ({"year_gte": 2027}, {"doc_id": ["unretrieved"]}, {"source_type": ["haven_service_catalog"]}):
        assert not named_report.named_report_leads("EX7", cands, {**allowed, **extra}, "universe_project")


def test_unmentioned_report_or_longer_identifier_does_not_query_database(monkeypatch):
    monkeypatch.setattr(named_report, "engine", lambda: pytest.fail("Unexpected report lookup"))
    for question in ("EX7R", "related study"):
        assert named_report.named_report_leads(
            question, [chunk("result", "EX7_report", 2, 1)], {}, None
        ) == []
