"""Placeholder for retrieval pipeline tests.

The full retrieval test requires loading 2.3GB of BGE models, which is
too heavy for the test suite. Verify manually with:

    python -m scripts.test_retrieval "your query here"

See docs/architecture.md for details.
"""
import pytest


@pytest.mark.skip(reason="Heavy model load — run scripts/test_retrieval.py instead")
def test_retrieve_returns_results():
    """Placeholder — see module docstring."""
    pass