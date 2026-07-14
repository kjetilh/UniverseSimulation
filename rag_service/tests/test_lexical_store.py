from app.rag.index import lexical_store


def test_websearch_query_keeps_version_and_drops_question_stopwords():
    query = lexical_store._websearch_query(
        "Hva viste v16j, og hvilken del av den frosne gaten feilet?"
    )

    assert query == "viste OR v16j OR del OR frosne OR gaten OR feilet"
    assert lexical_store._version_title_patterns("Sammenlign v16j med V16H og v16j") == [
        "%v16j%",
        "%v16h%",
    ]


def test_lexical_search_uses_parameterized_or_query(monkeypatch):
    seen = {}

    class FakeResult:
        def fetchall(self):
            return []

    class FakeConnection:
        def execute(self, sql, params):
            seen["sql"] = str(sql)
            seen["params"] = params
            return FakeResult()

    class FakeBegin:
        def __enter__(self):
            return FakeConnection()

        def __exit__(self, exc_type, exc, tb):
            return False

    class FakeEngine:
        def begin(self):
            return FakeBegin()

    monkeypatch.setattr(lexical_store, "engine", lambda: FakeEngine())

    result = lexical_store.lexical_search(
        "Hva viste v16j?",
        top_k=7,
        filters={"source_type": ["universe_experiments"]},
    )

    assert result == []
    assert "websearch_to_tsquery" in seen["sql"]
    assert "plainto_tsquery" not in seen["sql"]
    assert seen["params"]["lexical_q"] == "viste OR v16j"
    assert seen["params"]["title_patterns"] == ["%v16j%"]
    assert seen["params"]["source_type"] == ["universe_experiments"]
    assert seen["params"]["top_k"] == 7
    assert "d.title ILIKE ANY(:title_patterns)" in seen["sql"]
