from src.retrieval.fusion import reciprocal_rank_fusion


def test_rrf_merges_and_ranks():
    bm25 = [{"id": "a", "content": "x"}, {"id": "b", "content": "y"}]
    vec = [{"id": "b", "content": "y"}, {"id": "c", "content": "z"}]
    fused = reciprocal_rank_fusion(bm25, vec)
    ids = [f["id"] for f in fused]
    assert "b" in ids
    assert len(ids) == 3
