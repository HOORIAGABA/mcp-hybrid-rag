"""MCP tool exposing the hybrid retriever.

Uses a background THREAD (not asyncio task) for model loading.
FastMCP's mcp.run() manages the event loop itself.
"""
# --- Set environment variables BEFORE importing torch/transformers/sentence-transformers ---
import os

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TQDM_DISABLE", "1")

# --- Now the heavy imports ---
import threading
import time

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from src.retrieval.hybrid_retriever import retrieve

mcp = FastMCP("hybrid-rag", host="127.0.0.1", port=8765)

# Global flag: are models loaded yet?
_models_ready = False


def _load_models_sync():
    """Load both models in a background thread."""
    global _models_ready
    print("Loading models in background...", flush=True)

    from src.retrieval.reranker import get_model as get_reranker

    get_reranker()
    print("Reranker loaded.", flush=True)

    from src.retrieval.vector_index import _embed
    from src.retrieval.vector_index import get_model as get_embedder

    get_embedder()
    _embed(["warmup"])
    print("Embedder loaded.", flush=True)

    _models_ready = True
    print("Models ready.", flush=True)


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    )
)
async def search_financial_docs(query: str, top_k: int = 5) -> str:
    """Search financial reports using hybrid retrieval (BM25 + vector) with reranking."""
    # Wait for models if not ready yet
    if not _models_ready:
        print("Tool called — waiting for models...", flush=True)
        while not _models_ready:
            time.sleep(1)

    results = retrieve(query, top_k=top_k)
    if not results:
        return "No results."
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(
            f"[{i}] {r['source']} p.{r['page']} (rerank={r.get('rerank_score', 0):.3f})\n"
            f"{r['content'][:400]}\n"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    threading.Thread(target=_load_models_sync, daemon=True).start()

    if "--http" in sys.argv:
        print("Starting MCP server on http://127.0.0.1:8765/mcp", flush=True)
        mcp.run(transport="streamable-http")
    else:
        print("Starting MCP server (models loading in background)...", flush=True)
        mcp.run()
