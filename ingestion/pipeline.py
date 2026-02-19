"""Document ingestion pipeline: download → parse → chunk → store."""

from __future__ import annotations

import tempfile
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from rich.console import Console
from rich.progress import track

from config.settings import CHUNK_OVERLAP, CHUNK_SIZE, GOOGLE_DRIVE_FOLDER_ID
from ingestion.google_drive import download_file, list_files
from ingestion.parsers import load_document
from vectorstore.store import get_vectorstore

console = Console()


def _chunk_documents(docs: list[Document]) -> list[Document]:
    """Split documents into smaller chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True,
    )
    return splitter.split_documents(docs)


def ingest(folder_id: str | None = None) -> int:
    """Run the full ingestion pipeline.

    1. List files from Google Drive.
    2. Download each file locally.
    3. Parse into LangChain Documents.
    4. Chunk and store in ChromaDB.

    Returns the number of chunks stored.
    """
    folder_id = folder_id or GOOGLE_DRIVE_FOLDER_ID
    if not folder_id:
        console.print("[red]Error:[/] GOOGLE_DRIVE_FOLDER_ID is not set.")
        return 0

    console.print(f"[bold]Listing files in folder:[/] {folder_id}")
    files = list_files(folder_id)
    console.print(f"Found [cyan]{len(files)}[/] supported file(s).")

    if not files:
        return 0

    all_docs: list[Document] = []

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for file_meta in track(files, description="Downloading & parsing…"):
            try:
                local_path = download_file(file_meta, dest_dir=tmp_dir)
                docs = load_document(local_path, source_name=file_meta["name"])
                all_docs.extend(docs)
            except Exception as exc:  # noqa: BLE001
                console.print(
                    f"[yellow]Skipping[/] {file_meta['name']}: {exc}"
                )

    console.print(f"Parsed [cyan]{len(all_docs)}[/] page(s) / section(s).")

    chunks = _chunk_documents(all_docs)
    console.print(f"Created [cyan]{len(chunks)}[/] chunk(s).")

    store = get_vectorstore()
    store.add_documents(chunks)
    console.print("[green]✓[/] Chunks stored in ChromaDB.")

    return len(chunks)
