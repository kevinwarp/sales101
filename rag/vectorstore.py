"""ChromaDB vector store, persisted to disk."""

from __future__ import annotations

from functools import lru_cache

from langchain_chroma import Chroma

import config
from rag.embeddings import get_embeddings


@lru_cache(maxsize=1)
def get_vectorstore() -> Chroma:
    """Return a persistent Chroma vector store backed by Voyage AI embeddings."""
    return Chroma(
        collection_name=config.CHROMA_COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=config.CHROMA_PERSIST_DIR,
    )
