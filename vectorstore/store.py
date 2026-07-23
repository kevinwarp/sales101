"""ChromaDB vector store backed by Voyage AI embeddings."""

from __future__ import annotations

from langchain_chroma import Chroma
from langchain_voyageai import VoyageAIEmbeddings

from config.settings import (
    CHROMA_COLLECTION_NAME,
    CHROMA_PERSIST_DIR,
    VOYAGE_API_KEY,
    VOYAGE_MODEL,
)


def get_embeddings() -> VoyageAIEmbeddings:
    """Return a Voyage AI embedding model instance."""
    return VoyageAIEmbeddings(
        voyage_api_key=VOYAGE_API_KEY,
        model=VOYAGE_MODEL,
    )


def get_vectorstore() -> Chroma:
    """Return a persistent ChromaDB vector store."""
    return Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_PERSIST_DIR,
    )


def get_retriever(search_k: int = 5):
    """Return a LangChain retriever over the vector store."""
    store = get_vectorstore()
    return store.as_retriever(search_type="similarity", search_kwargs={"k": search_k})
