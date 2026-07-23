"""Prompt templates used by the RAG chain."""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# ── Contextualise the latest question using chat history ─────────────────────
CONTEXTUALISE_SYSTEM = (
    "Given the chat history and the latest user question, "
    "reformulate the question so it can be understood without the chat history. "
    "Do NOT answer the question — just reformulate it if needed, "
    "otherwise return it as-is."
)

CONTEXTUALISE_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", CONTEXTUALISE_SYSTEM),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# ── Answer using retrieved context ───────────────────────────────────────────
QA_SYSTEM = (
    "You are a helpful assistant that answers questions using the provided context. "
    "Use the following retrieved documents to answer the question. "
    "If you cannot find the answer in the context, say so clearly.\n\n"
    "{context}"
)

QA_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", QA_SYSTEM),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
