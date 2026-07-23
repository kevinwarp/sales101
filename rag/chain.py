"""Conversational retrieval chain: Claude LLM + ChromaDB retriever."""

from __future__ import annotations

from functools import lru_cache

from langchain.chains import ConversationalRetrievalChain
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

import config
from rag.vectorstore import get_vectorstore

SYSTEM_PROMPT = """\
You are a helpful sales assistant. Answer the user's question using ONLY the
context retrieved from the company's document store. If the context does not
contain enough information to answer, say so clearly — do not make things up.

When citing information, mention the source document name if available.
"""

QA_PROMPT = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template(
            "Context:\n{context}\n\nQuestion: {question}"
        ),
    ]
)


@lru_cache(maxsize=1)
def get_llm() -> ChatAnthropic:
    """Return a cached ChatAnthropic (Claude) instance."""
    return ChatAnthropic(
        model=config.ANTHROPIC_MODEL,
        anthropic_api_key=config.ANTHROPIC_API_KEY,
        temperature=0.2,
        max_tokens=2048,
    )


def build_chain() -> ConversationalRetrievalChain:
    """Build and return the conversational RAG chain."""
    retriever = get_vectorstore().as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5},
    )

    return ConversationalRetrievalChain.from_llm(
        llm=get_llm(),
        retriever=retriever,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        return_source_documents=True,
        verbose=False,
    )
