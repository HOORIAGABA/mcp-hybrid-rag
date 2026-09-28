"""Main entrypoint: hybrid retrieval + reranking."""

from src.config import TOP_K_FINAL, TOP_K_RETRIEVE
from src.retrieval.bm25_index import bm25_search
from src.retrieval.fusion import reciprocal_rank_fusion
from src.retrieval.reranker import rerank
from src.retrieval.vector_index import vector_search


def retrieve(query: str, top_k: int = TOP_K_FINAL) -> list[dict]:
    bm25_res = bm25_search(query, top_k=TOP_K_RETRIEVE)
    vec_res = vector_search(query, top_k=TOP_K_RETRIEVE)
    fused = reciprocal_rank_fusion(bm25_res, vec_res)
    final = rerank(query, fused[:TOP_K_RETRIEVE], top_k=top_k)
    return final


def vector_only_retrieve(query: str, top_k: int = TOP_K_FINAL) -> list[dict]:
    return vector_search(query, top_k=top_k)
