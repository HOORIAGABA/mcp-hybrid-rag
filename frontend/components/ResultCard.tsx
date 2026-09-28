export default function ResultCard({
  result, rank, mode,
}: { result: any; rank: number; mode: string }) {
  return (
    <div className="border border-gray-800 rounded p-4 bg-gray-900">
      <div className="flex justify-between text-sm text-gray-400 mb-2">
        <span>#{rank} — {result.source} p.{result.page}</span>
        <span>
          {mode === "hybrid" && result.rerank_score !== undefined && (
            <>rerank={result.rerank_score.toFixed(3)} </>
          )}
          {result.bm25_rank && <>| bm25#{result.bm25_rank} </>}
          {result.vector_rank && <>| vec#{result.vector_rank}</>}
        </span>
      </div>
      <p className="text-gray-200 whitespace-pre-wrap">{result.content}</p>
    </div>
  );
}
