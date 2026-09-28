export default function ComparisonToggle({
  mode, onChange,
}: { mode: "vector" | "hybrid"; onChange: (m: "vector" | "hybrid") => void }) {
  return (
    <div className="inline-flex rounded border border-gray-700 overflow-hidden">
      <button
        className={`px-4 py-2 ${mode === "vector" ? "bg-blue-600" : "bg-gray-900"}`}
        onClick={() => onChange("vector")}
      >
        Vector only
      </button>
      <button
        className={`px-4 py-2 ${mode === "hybrid" ? "bg-blue-600" : "bg-gray-900"}`}
        onClick={() => onChange("hybrid")}
      >
        Hybrid + Rerank
      </button>
    </div>
  );
}
