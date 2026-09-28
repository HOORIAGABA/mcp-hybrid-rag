"""Evaluate retrieval quality: Precision@K, Recall@K, MRR."""

import json
from datetime import datetime
from pathlib import Path

from src.retrieval.hybrid_retriever import retrieve, vector_only_retrieve

GOLDEN_PATH = Path(__file__).parent / "golden_queries.json"
K = 5


def load_golden():
    with open(GOLDEN_PATH) as f:
        return json.load(f)["queries"]


def precision_at_k(retrieved_ids, relevant_ids, k):
    hits = sum(1 for rid in retrieved_ids[:k] if rid in relevant_ids)
    return hits / k


def recall_at_k(retrieved_ids, relevant_ids, k):
    if not relevant_ids:
        return 0.0
    hits = sum(1 for rid in retrieved_ids[:k] if rid in relevant_ids)
    return hits / len(relevant_ids)


def mrr(retrieved_ids, relevant_ids):
    for i, rid in enumerate(retrieved_ids, 1):
        if rid in relevant_ids:
            return 1.0 / i
    return 0.0


def evaluate_mode(mode, queries):
    results = []
    for q in queries:
        # Skip negative controls (no ground truth to compare against)
        if not q.get("relevant_chunks"):
            continue

        if mode == "vector":
            chunks = vector_only_retrieve(q["question"], top_k=K)
        else:
            chunks = retrieve(q["question"], top_k=K)

        retrieved_ids = [c["id"] for c in chunks]
        relevant_ids = set(q["relevant_chunks"])

        results.append(
            {
                "id": q["id"],
                "query": q["question"][:55],
                "category": q.get("category", "unknown"),
                "p@k": precision_at_k(retrieved_ids, relevant_ids, K),
                "r@k": recall_at_k(retrieved_ids, relevant_ids, K),
                "mrr": mrr(retrieved_ids, relevant_ids),
            }
        )
    return results


def aggregate(results):
    if not results:
        return {"precision": 0, "recall": 0, "mrr": 0}
    n = len(results)
    return {
        "precision": sum(r["p@k"] for r in results) / n,
        "recall": sum(r["r@k"] for r in results) / n,
        "mrr": sum(r["mrr"] for r in results) / n,
    }


def save_results(vec_results, hyb_results, path="results/evaluation.json"):
    """Write per-query and aggregate results to JSON."""
    Path(path).parent.mkdir(exist_ok=True)
    payload = {
        "timestamp": datetime.now().isoformat(),
        "k": K,
        "vector_only": {
            "per_query": vec_results,
            "aggregate": aggregate(vec_results),
        },
        "hybrid_rerank": {
            "per_query": hyb_results,
            "aggregate": aggregate(hyb_results),
        },
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nResults saved to {path}")


def print_comparison(queries):
    vec_results = evaluate_mode("vector", queries)
    hyb_results = evaluate_mode("hybrid", queries)

    print("=" * 80)
    print(f"RETRIEVAL EVALUATION (K={K})")
    print("=" * 80)

    print(f"\n{'Query':<56} {'Vec':>8} {'Hyb':>8}")
    print("-" * 80)
    for v, h in zip(vec_results, hyb_results):
        print(f"{v['query']:<56} P={v['p@k']:.2f}  P={h['p@k']:.2f}")

    v_agg = aggregate(vec_results)
    h_agg = aggregate(hyb_results)

    print("-" * 80)
    print(f"{'AVERAGE (n=' + str(len(vec_results)) + ')':<56} {'Vec':>8} {'Hyb':>8}")
    print(f"{'Precision@' + str(K):<56} {v_agg['precision']:>8.3f} {h_agg['precision']:>8.3f}")
    print(f"{'Recall@' + str(K):<56} {v_agg['recall']:>8.3f} {h_agg['recall']:>8.3f}")
    print(f"{'MRR':<56} {v_agg['mrr']:>8.3f} {h_agg['mrr']:>8.3f}")
    print("=" * 80)

    # Per-category breakdown
    print("\nPER-CATEGORY (Hybrid):")
    categories = set(r["category"] for r in hyb_results)
    for cat in sorted(categories):
        cat_results = [r for r in hyb_results if r["category"] == cat]
        agg = aggregate(cat_results)
        print(f"  {cat:<15} n={len(cat_results)}  P@K={agg['precision']:.3f}  MRR={agg['mrr']:.3f}")

    # Save both JSON and human-readable text
    save_results(vec_results, hyb_results)


if __name__ == "__main__":
    queries = load_golden()
    print_comparison(queries)
