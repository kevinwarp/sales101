"""Interactive terminal chat interface for the RAG application."""

from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from rag.chain import build_rag_chain

console = Console()


def run_chat() -> None:
    """Launch an interactive chat session."""
    console.print(
        Panel(
            "[bold green]Sales101 RAG Chat[/]\n"
            "Ask questions about your ingested documents.\n"
            'Type "quit" or "exit" to leave.',
            expand=False,
        )
    )

    chain = build_rag_chain()
    chat_history: list[HumanMessage | AIMessage] = []

    while True:
        try:
            user_input = console.input("[bold cyan]You:[/] ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit", "q"}:
            console.print("[dim]Goodbye![/]")
            break

        result = chain.invoke({"input": user_input, "chat_history": chat_history})

        answer: str = result["answer"]
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=answer))

        console.print()
        console.print("[bold magenta]Assistant:[/]")
        console.print(Markdown(answer))

        # Show source documents if present.
        source_docs = result.get("context", [])
        if source_docs:
            sources = {d.metadata.get("source_name", "unknown") for d in source_docs}
            console.print(
                f"\n[dim]Sources: {', '.join(sorted(sources))}[/]"
            )
        console.print()
