import os
import warnings
from pathlib import Path

from bs4 import XMLParsedAsHTMLWarning
from dotenv import load_dotenv

load_dotenv()



os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
warnings.filterwarnings("ignore", message=".*capture\\(\\) takes 1 positional argument.*")

ROOT = Path(__file__).resolve().parent.parent

DATA_RAW = Path(os.getenv("DATA_RAW", ROOT / "data/raw"))
DATA_PROCESSED = Path(os.getenv("DATA_PROCESSED", ROOT / "data/processed"))
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", ROOT / "index/chroma"))
BM25_DIR = Path(os.getenv("BM25_DIR", ROOT / "index/bm25"))

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
RERANKER_MODEL = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-base")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K_RETRIEVE = 20  # per retriever before fusion
TOP_K_FINAL = 5  # after rerank
RRF_K = 60

for p in [DATA_RAW, DATA_PROCESSED, CHROMA_DIR, BM25_DIR]:
    p.mkdir(parents=True, exist_ok=True)
