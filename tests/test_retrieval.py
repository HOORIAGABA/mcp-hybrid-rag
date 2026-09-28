from src.retrieval.hybrid_retriever import retrieve


def test_retrieve_returns_results():
    results = retrieve("IBM revenue", top_k=3)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "content" in results[0]
