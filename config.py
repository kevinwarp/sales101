"""Centralized configuration loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"

# ── Anthropic / Claude ───────────────────────────────────────────────────────
ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL: str = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

# ── Voyage AI ────────────────────────────────────────────────────────────────
VOYAGE_API_KEY: str = os.environ.get("VOYAGE_API_KEY", "")
VOYAGE_EMBED_MODEL: str = os.environ.get("VOYAGE_EMBED_MODEL", "voyage-3")

# ── Google Drive ─────────────────────────────────────────────────────────────
GOOGLE_CREDENTIALS_PATH: str = os.environ.get("GOOGLE_CREDENTIALS_PATH", "credentials.json")
GOOGLE_DRIVE_FOLDER_IDS: list[str] = [
    fid.strip()
    for fid in os.environ.get("GOOGLE_DRIVE_FOLDER_IDS", "").split(",")
    if fid.strip()
]

# ── ChromaDB ─────────────────────────────────────────────────────────────────
CHROMA_PERSIST_DIR: str = os.environ.get("CHROMA_PERSIST_DIR", str(DATA_DIR / "chroma"))
CHROMA_COLLECTION_NAME: str = os.environ.get("CHROMA_COLLECTION_NAME", "sales101")

# ── Chunking ─────────────────────────────────────────────────────────────────
CHUNK_SIZE: int = int(os.environ.get("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP: int = int(os.environ.get("CHUNK_OVERLAP", "200"))

# ── Google Drive MIME helpers ────────────────────────────────────────────────
SUPPORTED_MIME_TYPES: dict[str, str] = {
    # Native Google formats → export MIME type
    "application/vnd.google-apps.document": "application/pdf",
    "application/vnd.google-apps.spreadsheet": "text/csv",
    "application/vnd.google-apps.presentation": "application/pdf",
    # Binary uploads kept as-is
    "application/pdf": "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}
