"""Voyage AI embedding function, configured from env vars."""

from __future__ import annotations

from functools import lru_cache

from langchain_voyageai import VoyageAIEmbeddings

import config


@lru_cache(maxsize=1)
def get_embeddings() -> VoyageAIEmbeddings:
    """Return a cached Voyage AI embeddings instance."""
    return VoyageAIEmbeddings(
        voyage_api_key=config.VOYAGE_API_KEY,
        model=config.VOYAGE_EMBED_MODEL,
    )
