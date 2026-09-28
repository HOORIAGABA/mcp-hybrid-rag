"""BGE cross-encoder reranker."""

from sentence_transformers import CrossEncoder

from src.config import RERANKER_MODEL

_model = None


def get_model():
    global _model
    if _model is None:
        _model = CrossEncoder(RERANKER_MODEL)
    return _model


def rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
    if not candidates:
        return []
    model = get_model()
    pairs = [(query, c["content"]) for c in candidates]
    scores = model.predict(pairs)
    for c, s in zip(candidates, scores):
        c["rerank_score"] = float(s)
    ranked = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
    return ranked[:top_k]
