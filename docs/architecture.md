# Architecture

## Pipeline Stages

### 1. Ingestion (`src/ingestion/`)

| File | Purpose |
|---|---|
| `download.py` | Fetches SEC 10-K filings from EDGAR. Uses a descriptive User-Agent header per SEC guidelines. |
| `parse.py` | Extracts text from HTML filings. Strips scripts and styles, collapses blank lines, splits into ~4,000-char logical pages. |
| `chunk.py` | Splits page text into ~800-char chunks with 150-char overlap. Uses `RecursiveCharacterTextSplitter` with paragraph-level separators. |

### 2. Indexing (`src/retrieval/`)

| File | Purpose |
|---|---|
| `bm25_index.py` | Builds a BM25Okapi index over tokenized chunks. Pickled to `index/bm25/bm25.pkl`. |
| `vector_index.py` | Embeds chunks with `BAAI/bge-small-en-v1.5` and stores in ChromaDB at `index/chroma/`. |

### 3. Query-Time Retrieval (`src/retrieval/`)

| File | Purpose |
|---|---|
| `hybrid_retriever.py` | Orchestrates the full pipeline: BM25 → vector → RRF → rerank. Exposes `retrieve()` and `vector_only_retrieve()`. |
| `fusion.py` | Reciprocal Rank Fusion with k=60. Combines two ranked lists into one. |
| `reranker.py` | Loads `BAAI/bge-reranker-v2-m3` lazily and reranks candidate chunks. |

### 4. Serving (`src/api/`, `src/mcp_server/`)

| File | Purpose |
|---|---|
| `api/main.py` | FastAPI app. `GET /search?q=...&mode=hybrid|vector`. CORS enabled for frontend. |
| `mcp_server/server.py` | MCP tool `search_financial_docs`. Loads models at import time so the Inspector's initialize handshake succeeds. |

## Design Decisions

### Why RRF and not score averaging?

BM25 scores and cosine similarities live on completely different scales (unbounded positive vs. bounded [-1, 1]). Averaging them requires normalization, which is fragile. RRF only uses *ranks*, so it's scale-invariant.

### Why two-stage retrieval?

The cross-encoder (reranker) is 50–100x slower than the bi-encoders (BM25, embeddings). Running it on the full 1,700-chunk corpus would take ~30 seconds per query. Running it on the top-20 fused candidates takes ~2 seconds. Two-stage retrieval balances accuracy and latency.

### Why local models?

No API keys, no per-query cost, no vendor lock-in. Runs entirely on CPU. The trade-off is larger downloads (~2.3GB) and slower cold starts.

### Why no LangChain?

See the README section "Why No LangChain."

## Data Flow

```
Query: "How did foreign currency fluctuations affect Apple's net sales in 2023?"

BM25 path:
  tokenize → score 1,709 chunks → top-20 by score
  (correct chunk: rank #20)

Vector path:
  embed query → cosine similarity → top-20
  (correct chunk: rank #12)

RRF Fusion:
  merge ranked lists with k=60 → top-20 unique chunks
  (correct chunk: rank ~#8)

Rerank:
  cross-encoder scores 20 (query, chunk) pairs → top-5
  (correct chunk: rank #1, rerank=0.983)

Return:
  top-5 chunks with full trace metadata
```

## Extension Points

| Want to... | Change |
|---|---|
| Swap the reranker | `src/config.py` — `RERANKER_MODEL` |
| Swap the embedder | `src/config.py` — `EMBEDDING_MODEL`, then rebuild indexes |
| Change chunk size | `src/config.py` — `CHUNK_SIZE`, `CHUNK_OVERLAP` |
| Add a new corpus | Add URLs to `FILINGS` in `src/ingestion/download.py` |
| Add an LLM answer step | New module in `src/generation/`, called after `retrieve()` |