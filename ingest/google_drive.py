"""Google Drive API client – list & download supported documents."""

from __future__ import annotations

import io
import logging
from pathlib import Path
from typing import Iterator

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

import config

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def _get_credentials() -> Credentials:
    """Return valid Google OAuth2 credentials, refreshing or prompting as needed."""
    token_path = Path("token.json")
    creds: Credentials | None = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.GOOGLE_CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json())

    return creds


def _build_service():
    """Build and return a Google Drive API v3 service."""
    return build("drive", "v3", credentials=_get_credentials())


# ── Public API ───────────────────────────────────────────────────────────────


def list_files(folder_id: str) -> Iterator[dict]:
    """Yield file metadata dicts for supported files in *folder_id* (non-recursive)."""
    service = _build_service()
    page_token: str | None = None

    while True:
        resp = (
            service.files()
            .list(
                q=f"'{folder_id}' in parents and trashed = false",
                fields="nextPageToken, files(id, name, mimeType, modifiedTime)",
                pageSize=100,
                pageToken=page_token,
            )
            .execute()
        )

        for f in resp.get("files", []):
            if f["mimeType"] in config.SUPPORTED_MIME_TYPES:
                yield f
            else:
                logger.debug("Skipping unsupported MIME %s: %s", f["mimeType"], f["name"])

        page_token = resp.get("nextPageToken")
        if not page_token:
            break


def download_file(file_meta: dict, dest_dir: Path) -> Path:
    """Download a single Drive file to *dest_dir* and return the local path.

    Google-native formats (Docs, Sheets, Slides) are exported to a compatible
    format; binary uploads (PDF, DOCX, XLSX, PPTX) are downloaded directly.
    """
    service = _build_service()
    file_id = file_meta["id"]
    mime = file_meta["mimeType"]
    export_mime = config.SUPPORTED_MIME_TYPES[mime]

    is_native = mime.startswith("application/vnd.google-apps.")

    ext_map = {
        "application/pdf": ".pdf",
        "text/csv": ".csv",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    }
    ext = ext_map.get(export_mime, ".bin")
    dest = dest_dir / f"{file_meta['name']}{ext}"

    buf = io.BytesIO()
    if is_native:
        request = service.files().export_media(fileId=file_id, mimeType=export_mime)
    else:
        request = service.files().get_media(fileId=file_id)

    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    dest.write_bytes(buf.getvalue())
    logger.info("Downloaded %s → %s", file_meta["name"], dest)
    return dest
