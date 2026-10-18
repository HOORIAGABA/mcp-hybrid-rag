FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build the BM25 + Chroma indexes at image build time.
# No API keys needed -- embeddings (bge-small-en-v1.5) and the reranker
# (bge-reranker-v2-m3) both run locally via sentence-transformers.
RUN python -m scripts.build_indexes

# Hugging Face Spaces routes traffic to port 7860
ENV PORT=7860
EXPOSE 7860

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
