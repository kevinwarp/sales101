"""End-to-end ingestion pipeline: Drive → parse → chunk → embed → ChromaDB."""

from __future__ import annotations

import logging
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from rich.progress import Progress

import config
from ingest.google_drive import download_file, list_files
from ingest.loader import load_file
from rag.vectorstore import get_vectorstore

logger = logging.getLogger(__name__)


def run(folder_ids: list[str] | None = None) -> int:
    """Run the full ingestion pipeline and return the number of chunks stored.

    Parameters
    ----------
    folder_ids:
        Google Drive folder IDs to ingest. Falls back to ``config.GOOGLE_DRIVE_FOLDER_IDS``.
    """
    folder_ids = folder_ids or config.GOOGLE_DRIVE_FOLDER_IDS
    if not folder_ids:
        raise ValueError(
            "No Google Drive folder IDs configured. "
            "Set GOOGLE_DRIVE_FOLDER_IDS in your .env file."
        )

    download_dir = Path(config.DATA_DIR / "downloads")
    download_dir.mkdir(parents=True, exist_ok=True)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )

    all_chunks = []

    with Progress() as progress:
        for fid in folder_ids:
            files = list(list_files(fid))
            task = progress.add_task(f"Folder {fid[:8]}…", total=len(files))

            for file_meta in files:
                local_path = download_file(file_meta, download_dir)
                docs = load_file(local_path)
                chunks = splitter.split_documents(docs)
                all_chunks.extend(chunks)
                progress.advance(task)

    if not all_chunks:
        logger.warning("No documents found to ingest.")
        return 0

    logger.info("Embedding and storing %d chunks …", len(all_chunks))
    store = get_vectorstore()
    store.add_documents(all_chunks)
    logger.info("Ingestion complete – %d chunks stored.", len(all_chunks))
    return len(all_chunks)
