"""Reciprocal Rank Fusion."""

from src.config import RRF_K


def reciprocal_rank_fusion(bm25_results: list[dict], vector_results: list[dict]) -> list[dict]:
    scores = {}
    payload = {}

    for rank, doc in enumerate(bm25_results, start=1):
        scores[doc["id"]] = scores.get(doc["id"], 0) + 1 / (RRF_K + rank)
        payload[doc["id"]] = {**doc, "bm25_rank": rank}

    for rank, doc in enumerate(vector_results, start=1):
        scores[doc["id"]] = scores.get(doc["id"], 0) + 1 / (RRF_K + rank)
        if doc["id"] in payload:
            payload[doc["id"]]["vector_rank"] = rank
        else:
            payload[doc["id"]] = {**doc, "vector_rank": rank}

    fused = []
    for doc_id, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        item = payload[doc_id]
        item["rrf_score"] = score
        fused.append(item)
    return fused
