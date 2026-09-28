from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.retrieval.hybrid_retriever import retrieve, vector_only_retrieve

app = FastAPI(title="Hybrid RAG API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchResponse(BaseModel):
    mode: str
    results: list[dict]


@app.get("/search", response_model=SearchResponse)
async def search(q: str, mode: str = "hybrid", top_k: int = 5):
    if mode == "vector":
        return SearchResponse(mode="vector", results=vector_only_retrieve(q, top_k=top_k))
    return SearchResponse(mode="hybrid", results=retrieve(q, top_k=top_k))


@app.get("/health")
async def health():
    return {"status": "ok"}
