export default function SearchBar({
  value, onChange, onSubmit,
}: { value: string; onChange: (v: string) => void; onSubmit: () => void }) {
  return (
    <div className="flex gap-2">
      <input
        className="flex-1 bg-gray-900 border border-gray-700 rounded px-3 py-2"
        placeholder="Ask something about the financial reports..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && onSubmit()}
      />
      <button
        className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded font-medium"
        onClick={onSubmit}
      >
        Search
      </button>
    </div>
  );
}
