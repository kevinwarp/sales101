"""Google Drive API client for listing and downloading files."""

from __future__ import annotations

import io
import tempfile
from pathlib import Path
from typing import BinaryIO

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from config.settings import (
    GOOGLE_CREDENTIALS_PATH,
    GOOGLE_DRIVE_FOLDER_ID,
    GOOGLE_SCOPES,
    GOOGLE_TOKEN_PATH,
)

# Google Workspace MIME types and their export formats.
EXPORT_MIME_MAP: dict[str, tuple[str, str]] = {
    "application/vnd.google-apps.document": (
        "application/pdf",
        ".pdf",
    ),
    "application/vnd.google-apps.spreadsheet": (
        "text/csv",
        ".csv",
    ),
    "application/vnd.google-apps.presentation": (
        "application/pdf",
        ".pdf",
    ),
}

# Binary MIME types we can download directly.
SUPPORTED_BINARY_MIMES: set[str] = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # .xlsx
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # .pptx
}


def _authenticate() -> Credentials:
    """Return valid Google OAuth2 credentials, refreshing or initiating
    the OAuth flow as needed."""
    creds: Credentials | None = None

    if GOOGLE_TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(GOOGLE_TOKEN_PATH), GOOGLE_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(GOOGLE_CREDENTIALS_PATH), GOOGLE_SCOPES
            )
            creds = flow.run_local_server(port=0)

        GOOGLE_TOKEN_PATH.write_text(creds.to_json())

    return creds


def get_drive_service():
    """Build and return an authenticated Google Drive API service."""
    creds = _authenticate()
    return build("drive", "v3", credentials=creds)


def list_files(folder_id: str | None = None) -> list[dict]:
    """List all supported files in the given Drive folder (non-recursive).

    Returns a list of dicts with keys: id, name, mimeType.
    """
    folder_id = folder_id or GOOGLE_DRIVE_FOLDER_ID
    service = get_drive_service()

    all_mimes = set(EXPORT_MIME_MAP.keys()) | SUPPORTED_BINARY_MIMES
    mime_filter = " or ".join(f"mimeType='{m}'" for m in all_mimes)
    query = f"'{folder_id}' in parents and trashed=false and ({mime_filter})"

    results: list[dict] = []
    page_token: str | None = None

    while True:
        resp = (
            service.files()
            .list(
                q=query,
                fields="nextPageToken, files(id, name, mimeType)",
                pageSize=100,
                pageToken=page_token,
            )
            .execute()
        )
        results.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return results


def download_file(file_meta: dict, dest_dir: Path | None = None) -> Path:
    """Download a single Drive file to *dest_dir* and return its local path.

    Google Workspace files are exported via the export API; binary files
    are downloaded directly.
    """
    service = get_drive_service()
    file_id: str = file_meta["id"]
    mime: str = file_meta["mimeType"]
    name: str = file_meta["name"]

    dest_dir = dest_dir or Path(tempfile.mkdtemp())

    if mime in EXPORT_MIME_MAP:
        export_mime, ext = EXPORT_MIME_MAP[mime]
        request = service.files().export_media(fileId=file_id, mimeType=export_mime)
        local_path = dest_dir / f"{Path(name).stem}{ext}"
    else:
        request = service.files().get_media(fileId=file_id)
        local_path = dest_dir / name

    buffer: BinaryIO = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    local_path.write_bytes(buffer.getvalue())
    return local_path
