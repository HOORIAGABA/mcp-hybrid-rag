"use client";
import { useState } from "react";
import SearchBar from "@/components/SearchBar";
import ResultsList from "@/components/ResultsList";
import ComparisonToggle from "@/components/ComparisonToggle";

export default function Home() {
  const [query, setQuery] = useState("");
  const [mode, setMode] = useState<"vector" | "hybrid">("hybrid");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  async function runSearch(q: string, m: string) {
    setLoading(true);
    const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const res = await fetch(`${api}/search?q=${encodeURIComponent(q)}&mode=${m}&top_k=5`);
    const data = await res.json();
    setResults(data.results);
    setLoading(false);
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Hybrid RAG Demo</h1>
      <p className="text-gray-400">
        Compare pure vector retrieval against hybrid (BM25 + vector) with reranking.
      </p>
      <SearchBar
        value={query}
        onChange={setQuery}
        onSubmit={() => runSearch(query, mode)}
      />
      <ComparisonToggle mode={mode} onChange={(m) => { setMode(m); if (query) runSearch(query, m); }} />
      {loading && <p className="text-gray-400">Searching...</p>}
      <ResultsList results={results} mode={mode} />
    </div>
  );
}
