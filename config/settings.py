"""Centralized configuration loaded from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ── API keys ─────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")
VOYAGE_API_KEY: str = os.environ.get("VOYAGE_API_KEY", "")

# ── Google Drive ─────────────────────────────────────────────────────────────
GOOGLE_DRIVE_FOLDER_ID: str = os.environ.get("GOOGLE_DRIVE_FOLDER_ID", "")
GOOGLE_CREDENTIALS_PATH: Path = PROJECT_ROOT / "credentials.json"
GOOGLE_TOKEN_PATH: Path = PROJECT_ROOT / "token.json"
GOOGLE_SCOPES: list[str] = [
    "https://www.googleapis.com/auth/drive.readonly",
]

# ── ChromaDB ─────────────────────────────────────────────────────────────────
CHROMA_PERSIST_DIR: str = os.environ.get(
    "CHROMA_PERSIST_DIR", str(PROJECT_ROOT / "chroma_db")
)
CHROMA_COLLECTION_NAME: str = os.environ.get("CHROMA_COLLECTION_NAME", "sales101")

# ── Models ───────────────────────────────────────────────────────────────────
ANTHROPIC_MODEL: str = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
VOYAGE_MODEL: str = os.environ.get("VOYAGE_MODEL", "voyage-3")

# ── Chunking ─────────────────────────────────────────────────────────────────
CHUNK_SIZE: int = int(os.environ.get("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP: int = int(os.environ.get("CHUNK_OVERLAP", "200"))
