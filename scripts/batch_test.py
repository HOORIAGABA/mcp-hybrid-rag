import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.retrieval.hybrid_retriever import retrieve

QUERIES = [
    # "How did foreign currency fluctuations affect Apple's net sales in 2023?",
    # "How much did Apple spend on research and development in 2023?",
    # "What was Apple's total net sales in 2023?",
    # "What was Apple's total operating income in 2023?",
    # "What was Apple's revenue from the Americas segment in 2023?",
    # "What was Apple's revenue from the Greater China segment in 2023?",
    # "Why did Apple's iPhone net sales decrease in 2023?",
    # "What were Apple's main risk factors related to foreign exchange?",
    # "What was Microsoft's research and development expense in 2023?",
    # "What was Alphabet's research and development expense in 2023?",
    # "What was Tesla's net income in 2023?",
    # "What did Apple's CEO say about AI strategy in 2023?",
    "What was Microsoft's total revenue in fiscal 2023?",
    "What was Alphabet's total revenue in 2023?",
    "What was Apple's net income in 2023?",
    "What drove Apple's Services revenue growth in 2023?",
    "What are Microsoft's main risk factors related to cloud competition?",
    "What was Apple's iPhone net sales in 2023?",
    "What was Microsoft's revenue from the Intelligent Cloud segment in 2023?",
    "Compare Apple's and Microsoft's research and development spending in 2023.",
    "Which company had higher total revenue in 2023: Apple or Microsoft?",
    "What was Amazon's net income in 2023?",
]

for q in QUERIES:
    print(f"\n{'=' * 80}\nQUERY: {q}\n{'=' * 80}")
    results = retrieve(q, top_k=3)
    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['id']}  rerank={r.get('rerank_score', 0):.3f}")
        print(f"    {r['content'][:200]}\n")
