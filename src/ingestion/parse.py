"""Parse HTML filings into per-page (per-section) text."""
from pathlib import Path
from bs4 import BeautifulSoup
from src.config import DATA_RAW


def parse_html(html_path: Path) -> list[dict]:
    """Extract text from an HTML filing, chunked by top-level headings."""
    raw = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "lxml")

    # Strip scripts, styles, and hidden elements
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # SEC filings wrap content in <div> blocks. We split on top-level text.
    text = soup.get_text(separator="\n", strip=True)

    # Collapse excessive blank lines
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    cleaned = "\n".join(lines)

    # Split into "pages" of ~4000 chars so page metadata stays meaningful
    # (SEC HTML has no real pagination, so we synthesize logical pages)
    pages = []
    page_size = 4000
    for i in range(0, len(cleaned), page_size):
        pages.append({
            "source": html_path.name,
            "page": i // page_size + 1,
            "text": cleaned[i : i + page_size],
        })
    return pages


def parse_all() -> list[dict]:
    """Parse every .htm/.html file in data/raw/."""
    docs = []
    for path in DATA_RAW.glob("*"):
        if path.suffix.lower() in (".htm", ".html"):
            docs.extend(parse_html(path))
    return docs


if __name__ == "__main__":
    docs = parse_all()
    print(f"Parsed {len(docs)} logical pages")