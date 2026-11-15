#!/usr/bin/env python3
"""Upload a video to YouTube via Data API v3 using an OAuth refresh token.

Free quota: 100 uploads/day (Video Uploads bucket, 1 unit per upload).
Required env: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN.

Note: the OAuth consent screen must be published to "In production".
In "Testing" status the refresh token expires every 7 days, which would
break a hands-free pipeline weekly. An unverified production app works
for the owner's own account after one warning click-through.
"""

import argparse
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--tags", default="", help="comma-separated")
    p.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])
    p.add_argument("--category", default="24", help="YouTube category id (24 = Entertainment)")
    a = p.parse_args()

    missing = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(k)]
    if missing:
        sys.exit(f"missing env vars: {', '.join(missing)}")

    creds = Credentials(
        token=None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        scopes=SCOPES,
    )
    creds.refresh(Request())

    youtube = build("youtube", "v3", credentials=creds, cache_discovery=False)
    body = {
        "snippet": {
            "title": a.title[:100],
            "description": a.description,
            "tags": [t.strip() for t in a.tags.split(",") if t.strip()],
            "categoryId": a.category,
        },
        "status": {"privacyStatus": a.privacy, "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(a.file, chunksize=8 * 1024 * 1024, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media, notifySubscribers=False)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"upload {int(status.progress() * 100)}%")
    print(f"uploaded: https://youtu.be/{response['id']}")


if __name__ == "__main__":
    main()
