"""BM25 index with pickle persistence."""
import pickle
import re
from pathlib import Path
from rank_bm25 import BM25Okapi
from src.config import BM25_DIR


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def build_bm25(chunks: list[dict]):
    corpus_tokens = [tokenize(c["content"]) for c in chunks]
    bm25 = BM25Okapi(corpus_tokens)
    BM25_DIR.mkdir(parents=True, exist_ok=True)
    with open(BM25_DIR / "bm25.pkl", "wb") as f:
        pickle.dump({"bm25": bm25, "chunks": chunks}, f)
    print(f"BM25 index built with {len(chunks)} chunks")


def load_bm25():
    with open(BM25_DIR / "bm25.pkl", "rb") as f:
        data = pickle.load(f)
    return data["bm25"], data["chunks"]


def bm25_search(query: str, top_k: int = 20) -> list[dict]:
    bm25, chunks = load_bm25()
    scores = bm25.get_scores(tokenize(query))
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    return [
        {**chunks[i], "bm25_score": float(scores[i]), "bm25_rank": rank + 1}
        for rank, i in enumerate(ranked)
    ]
