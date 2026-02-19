"""RAG chain: history-aware retrieval + Claude question-answering."""

from __future__ import annotations

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_anthropic import ChatAnthropic

from config.settings import ANTHROPIC_API_KEY, ANTHROPIC_MODEL
from rag.prompts import CONTEXTUALISE_PROMPT, QA_PROMPT
from vectorstore.store import get_retriever


def get_llm() -> ChatAnthropic:
    """Return the Claude chat model."""
    return ChatAnthropic(
        model=ANTHROPIC_MODEL,
        anthropic_api_key=ANTHROPIC_API_KEY,
        temperature=0,
        max_tokens=4096,
    )


def build_rag_chain():
    """Construct and return the full conversational RAG chain.

    The chain:
    1. Contextualises the user question using chat history.
    2. Retrieves relevant document chunks from ChromaDB.
    3. Answers the question with Claude, citing the retrieved context.
    """
    llm = get_llm()
    retriever = get_retriever()

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, CONTEXTUALISE_PROMPT
    )

    qa_chain = create_stuff_documents_chain(llm, QA_PROMPT)

    return create_retrieval_chain(history_aware_retriever, qa_chain)
