"""Download 10-K filings from SEC EDGAR.

SEC EDGAR requires a User-Agent header with your name and email.
Edit the USER_AGENT constant below before running.
"""
import urllib.request
import time
from pathlib import Path
from src.config import DATA_RAW
from tqdm import tqdm

# REQUIRED: SEC EDGAR requires identifying yourself. Use real values.
USER_AGENT = "Hooria hooriagava129@gmail.com"

# Real SEC EDGAR 10-K URLs. These are the raw filing documents.
# Adding a few companies gives you a more interesting corpus.
FILINGS = [
    # Apple 2023 10-K
    ("apple_2023_10k.htm",
     "https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm"),
    # Microsoft 2023 10-K
    ("microsoft_2023_10k.htm",
     "https://www.sec.gov/Archives/edgar/data/789019/000095017023035122/msft-20230630.htm"),
    # IBM 2023 10-K
    ("ibm_2023_10k.htm",
     "https://www.sec.gov/Archives/edgar/data/51143/000155837024002463/ibm-20231231.htm"),
    # Alphabet 2023 10-K
    ("alphabet_2023_10k.htm",
     "https://www.sec.gov/Archives/edgar/data/1652044/000165204424000022/goog-20231231.htm"),
]


def download_dataset():
    """Download SEC filings to data/raw/."""
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    saved = 0
    for name, url in tqdm(FILINGS, desc="Downloading 10-Ks"):
        out = DATA_RAW / name
        if out.exists() and out.stat().st_size > 0:
            print(f"  already exists: {name}")
            saved += 1
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as resp:
                out.write_bytes(resp.read())
            saved += 1
            time.sleep(0.5)  # polite rate limit per SEC guidelines
        except Exception as e:
            print(f"  FAILED {name}: {e}")
    print(f"Saved {saved}/{len(FILINGS)} filings to {DATA_RAW}")


if __name__ == "__main__":
    download_dataset()