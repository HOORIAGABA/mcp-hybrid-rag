import ResultCard from "./ResultCard";

export default function ResultsList({ results, mode }: { results: any[]; mode: string }) {
  if (!results.length) return null;
  return (
    <div className="space-y-4">
      {results.map((r, i) => (
        <ResultCard key={r.id || i} result={r} rank={i + 1} mode={mode} />
      ))}
    </div>
  );
}
