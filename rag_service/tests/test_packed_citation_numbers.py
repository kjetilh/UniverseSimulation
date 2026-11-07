from types import SimpleNamespace

from app.rag.retrieve.pack_context import pack_context


def test_prompt_numbers_follow_returned_citations_after_selection():
    def candidate(doc, ordinal, score):
        return SimpleNamespace(doc_id=doc, chunk_id=f"{doc}-{ordinal}", title=doc,
                               ordinal=ordinal, score=score, content=f"Excerpt {doc} {ordinal}")

    packed = pack_context(
        [candidate("A", 0, 1), candidate("B", 0, 2), candidate("B", 1, 3)],
        top_k=2, max_chunks_per_doc=1,
    )
    assert [c.chunk_id for c in packed.citations] == ["B-1", "A-0"]
    assert packed.context_text.split("\n\n") == [
        f"[{number}] [{cite.doc_id}::{cite.chunk_id}]\n{cite.excerpt}"
        for number, cite in enumerate(packed.citations, 1)
    ]
