"""Chunk parsed filing text into retrievable pieces with metadata preserved."""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(pages: list[dict]) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = []
    for page in pages:
        for i, chunk_text in enumerate(splitter.split_text(page["text"])):
            chunks.append({
                "id": f"{page['source']}_p{page['page']}_c{i}",
                "content": chunk_text,
                "source": page["source"],
                "page": page["page"],
            })
    return chunks