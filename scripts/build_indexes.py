import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ingestion.chunk import chunk_documents
from src.ingestion.download import download_dataset
from src.ingestion.parse import parse_all
from src.retrieval.bm25_index import build_bm25
from src.retrieval.vector_index import build_vector_index


def main():
    print("Step 1: Download filings")
    download_dataset()

    print("Step 2: Parse filings")
    pages = parse_all()
    print(f"Parsed {len(pages)} logical pages")

    print("Step 3: Chunk")
    chunks = chunk_documents(pages)
    print(f"Created {len(chunks)} chunks")

    print("Step 4: Build BM25")
    build_bm25(chunks)

    print("Step 5: Build vector index")
    build_vector_index(chunks)

    print("Done.")


if __name__ == "__main__":
    main()
