"""ChromaDB vector index using local BGE embeddings (no OpenAI)."""
import chromadb
from sentence_transformers import SentenceTransformer
from src.config import CHROMA_DIR, EMBEDDING_MODEL

# Loaded lazily on first use — downloads ~80MB once, then cached
_model = None
_chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def _embed(texts: list[str]) -> list[list[float]]:
    """Return embeddings as plain Python lists (Chroma-friendly)."""
    model = get_model()
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return [v.tolist() for v in vectors]


def build_vector_index(chunks: list[dict]):
    try:
        _chroma.delete_collection("docs")
    except Exception:
        pass
    coll = _chroma.create_collection("docs", metadata={"hnsw:space": "cosine"})

    batch = 100
    for i in range(0, len(chunks), batch):
        chunk_batch = chunks[i : i + batch]
        texts = [c["content"] for c in chunk_batch]
        coll.add(
            ids=[c["id"] for c in chunk_batch],
            embeddings=_embed(texts),
            documents=texts,
            metadatas=[{"source": c["source"], "page": c["page"]} for c in chunk_batch],
        )
        print(f"  embedded {min(i + batch, len(chunks))}/{len(chunks)}")
    print(f"Vector index built with {len(chunks)} chunks")


def vector_search(query: str, top_k: int = 20) -> list[dict]:
    coll = _chroma.get_collection("docs")
    q_emb = _embed([query])[0]
    res = coll.query(query_embeddings=[q_emb], n_results=top_k)
    out = []
    for rank, (doc, meta, dist) in enumerate(zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    )):
        out.append({
            "id": res["ids"][0][rank],
            "content": doc,
            "source": meta["source"],
            "page": meta["page"],
            "vector_score": 1 - dist,
            "vector_rank": rank + 1,
        })
    return out