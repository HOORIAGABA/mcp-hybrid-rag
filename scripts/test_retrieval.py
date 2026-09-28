"""CLI: test retrieval before touching MCP or frontend."""

import sys

from src.retrieval.hybrid_retriever import retrieve


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "What was ROIC for IBM in 2006?"
    results = retrieve(query, top_k=5)
    print(f"Query: {query}\n")
    for i, r in enumerate(results, 1):
        print(
            f"[{i}] {r['id']}  {r['source']} p.{r['page']}  rerank={r.get('rerank_score', 0):.3f}"
        )
        print(f"    {r['content'][:300]}\n")


if __name__ == "__main__":
    main()
