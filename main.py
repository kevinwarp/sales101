#!/usr/bin/env python3
"""Sales101 RAG CLI – ingest documents and chat with them."""

from __future__ import annotations

import argparse
import logging
import sys


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%H:%M:%S",
    )


def cmd_ingest(args: argparse.Namespace) -> None:
    """Run the document ingestion pipeline."""
    from ingest.pipeline import run

    folder_ids = args.folder_ids or None
    count = run(folder_ids=folder_ids)
    print(f"\n✓ Ingested {count} chunks into the vector store.")


def cmd_chat(_args: argparse.Namespace) -> None:
    """Start the interactive chat session."""
    from chat.cli import start

    start()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sales101",
        description="RAG-powered sales knowledge base",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    sub = parser.add_subparsers(dest="command")

    # ── ingest ───────────────────────────────────────────────────────────
    ingest_parser = sub.add_parser("ingest", help="Ingest documents from Google Drive")
    ingest_parser.add_argument(
        "folder_ids",
        nargs="*",
        help="Google Drive folder IDs (overrides .env)",
    )

    # ── chat ─────────────────────────────────────────────────────────────
    sub.add_parser("chat", help="Start an interactive chat session")

    args = parser.parse_args()
    _setup_logging(args.verbose)

    if args.command == "ingest":
        cmd_ingest(args)
    elif args.command == "chat":
        cmd_chat(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
