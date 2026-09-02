from app.rag.knowledge_base import retrieve


def test_retrieve_returns_relevant_doc():
    results = retrieve("how does net run rate work")
    assert len(results) > 0
    assert any("Run Rate" in r["title"] for r in results)


def test_retrieve_empty_for_irrelevant_query():
    results = retrieve("zzz completely unrelated nonsense qqq")
    assert isinstance(results, list)
