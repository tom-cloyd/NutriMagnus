#!/usr/bin/env python3
"""
upload_ai_manual.py — Build the AI edition of the manual and put it in
Google Drive as a Google Doc, for the AI help notebook to sync from.

    python scripts/upload_ai_manual.py          # build, then upload
    python scripts/upload_ai_manual.py --new    # create a fresh Doc instead

The first run creates the Doc and records its file ID; every later run
replaces that same Doc's content in place (Drive API files.update), so the
Doc keeps its ID and link, and the notebook source that points at it stays
valid. The notebook still needs its "sync" clicked to pick up the change.

Owner-only tool. Needs, once:
  pip install google-api-python-client google-auth-oauthlib
  an OAuth "Desktop app" client from Google Cloud Console, saved as
  <config dir>/google-drive/client_secret.json (see README section below)
The first run opens a browser for Google sign-in and stores the resulting
token next to it. Scope is drive.file: the script can see only files it
created itself, nothing else in the Drive.

Docs: README-numa-documentation.md, "AI help edition of the manual".
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build_ai_manual  # noqa: E402
from platform_utils import get_config_dir  # noqa: E402

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
except ImportError:
    sys.exit("Error: Google API packages missing.  Run:\n"
             "  pip install google-api-python-client google-auth-oauthlib")

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
DOC_NAME = "NutriMagnus User Manual — AI edition"
GOOGLE_DOC = "application/vnd.google-apps.document"

STATE_DIR = get_config_dir() / "google-drive"
CLIENT_SECRET = STATE_DIR / "client_secret.json"
TOKEN = STATE_DIR / "token.json"
DOC_RECORD = STATE_DIR / "ai_manual_doc.json"


def _credentials() -> Credentials:
    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception as exc:      # revoked, or expired (see README)
            print(f"Stored sign-in no longer works ({exc}); signing in again.")
            creds = None
    if not creds or not creds.valid:
        if not CLIENT_SECRET.exists():
            sys.exit(f"Error: {CLIENT_SECRET} not found — see the README section "
                     "\"AI help edition of the manual\" for the one-time setup.")
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
        creds = flow.run_local_server(port=0)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN.write_text(creds.to_json(), encoding="utf-8")
    TOKEN.chmod(0o600)
    return creds


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--new", action="store_true",
                    help="create a new Doc even if one is already recorded")
    args = ap.parse_args()

    html_path = build_ai_manual.main()
    service = build("drive", "v3", credentials=_credentials())
    media = MediaFileUpload(str(html_path), mimetype="text/html", resumable=True)
    doc_id = None
    if DOC_RECORD.exists() and not args.new:
        doc_id = json.loads(DOC_RECORD.read_text(encoding="utf-8"))["file_id"]

    if doc_id:
        try:
            f = service.files().update(
                fileId=doc_id, media_body=media, fields="id,webViewLink,modifiedTime",
            ).execute()
        except HttpError as exc:
            if exc.resp.status == 404:
                sys.exit(f"Error: the recorded Doc ({doc_id}) is gone (deleted or "
                         "trashed?). Restore it from Drive's trash, or run with --new "
                         "and re-add the new Doc to the notebook.")
            raise
        print(f"Updated in place: {f['webViewLink']}  ({f['modifiedTime']})")
        print("Now click the source in the notebook and sync it with Google Drive.")
    else:
        f = service.files().create(
            body={"name": DOC_NAME, "mimeType": GOOGLE_DOC},
            media_body=media, fields="id,webViewLink",
        ).execute()
        DOC_RECORD.write_text(json.dumps({"file_id": f["id"]}), encoding="utf-8")
        print(f"Created: {f['webViewLink']}")
        print("Add this Doc to the notebook as a Google Drive source.")


if __name__ == "__main__":
    main()
