#!/usr/bin/env python3
"""Sales101 RAG application – CLI entry point."""

from __future__ import annotations

import argparse
import sys


def _cmd_ingest(args: argparse.Namespace) -> None:
    from ingestion.pipeline import ingest

    folder = getattr(args, "folder_id", None)
    count = ingest(folder_id=folder)
    print(f"Ingestion complete – {count} chunk(s) stored.")


def _cmd_chat(_args: argparse.Namespace) -> None:
    from chat.interface import run_chat

    run_chat()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sales101",
        description="RAG application for querying sales documents.",
    )
    sub = parser.add_subparsers(dest="command")

    # -- ingest ----------------------------------------------------------------
    ingest_parser = sub.add_parser(
        "ingest", help="Download documents from Google Drive and store in ChromaDB."
    )
    ingest_parser.add_argument(
        "--folder-id",
        dest="folder_id",
        default=None,
        help="Override the Google Drive folder ID from .env.",
    )
    ingest_parser.set_defaults(func=_cmd_ingest)

    # -- chat ------------------------------------------------------------------
    chat_parser = sub.add_parser(
        "chat", help="Start an interactive Q&A session over ingested documents."
    )
    chat_parser.set_defaults(func=_cmd_chat)

    # -- dispatch --------------------------------------------------------------
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
