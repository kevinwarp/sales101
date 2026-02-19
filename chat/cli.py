"""Rich-powered interactive CLI chat loop."""

from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from rag.chain import build_chain

console = Console()


def start() -> None:
    """Launch the interactive chat REPL."""
    console.print(
        Panel(
            "[bold green]Sales101 RAG Chat[/bold green]\n"
            "Ask questions about your ingested documents.\n"
            "Type [bold]quit[/bold] or [bold]exit[/bold] to stop.",
            title="Welcome",
        )
    )

    chain = build_chain()
    chat_history: list[tuple[str, str]] = []

    while True:
        try:
            question = console.input("[bold cyan]You:[/bold cyan] ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not question:
            continue
        if question.lower() in {"quit", "exit"}:
            break

        result = chain.invoke(
            {"question": question, "chat_history": chat_history}
        )

        answer: str = result["answer"]
        sources = result.get("source_documents", [])

        console.print()
        console.print(Markdown(answer))

        if sources:
            seen: set[str] = set()
            names = []
            for doc in sources:
                name = doc.metadata.get("filename", doc.metadata.get("source", "unknown"))
                if name not in seen:
                    seen.add(name)
                    names.append(name)
            console.print(f"\n[dim]Sources: {', '.join(names)}[/dim]")

        console.print()
        chat_history.append((question, answer))

    console.print("\n[bold]Goodbye![/bold]")
