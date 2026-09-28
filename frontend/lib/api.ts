export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function search(q: string, mode: "vector" | "hybrid", topK = 5) {
  const res = await fetch(`${API_URL}/search?q=${encodeURIComponent(q)}&mode=${mode}&top_k=${topK}`);
  return res.json();
}
