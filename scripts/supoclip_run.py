#!/usr/bin/env python3
"""Drive a self-hosted SupoClip backend headlessly.

Uploads a local video file, creates a clipping task, polls until the
worker finishes, then downloads every rendered clip.

Auth: SupoClip's backend accepts HMAC-signed headers (the same scheme the
frontend uses). We control BACKEND_AUTH_SECRET via .env, so we sign with a
fixed CI user id that the workflow seeds into postgres.
"""
import hashlib
import hmac
import json
import os
import sys
import time

import requests

BACKEND = os.environ.get("SUPOCLIP_BACKEND", "http://localhost:8000")
SECRET = os.environ["SUPOCLIP_AUTH_SECRET"]
USER_ID = os.environ.get("SUPOCLIP_USER_ID", "ci-user-0001")
VIDEO = os.environ.get("VIDEO_FILE", "video.mp4")
OUT_DIR = os.environ.get("OUT_DIR", "clips")
CLIP_LENGTH = os.environ.get("CLIP_LENGTH", "auto")
POLL_TIMEOUT = int(os.environ.get("POLL_TIMEOUT_SECONDS", str(4 * 3600)))


def auth_headers() -> dict:
    ts = str(int(time.time()))
    sig = hmac.new(
        SECRET.encode(), f"{USER_ID}:{ts}".encode(), hashlib.sha256
    ).hexdigest()
    return {
        "x-supoclip-user-id": USER_ID,
        "x-supoclip-ts": ts,
        "x-supoclip-signature": sig,
    }


def main() -> int:
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"[1/4] Uploading {VIDEO} ...", flush=True)
    with open(VIDEO, "rb") as fh:
        r = requests.post(
            f"{BACKEND}/upload",
            headers=auth_headers(),
            files={"video": (os.path.basename(VIDEO), fh, "video/mp4")},
            timeout=1800,
        )
    r.raise_for_status()
    video_path = r.json()["video_path"]
    print(f"      uploaded as {video_path}", flush=True)

    print("[2/4] Creating task ...", flush=True)
    payload = {
        "source": {"url": video_path},
        "caption_template": "default",
        "output_format": "vertical",
        "add_subtitles": True,
        "clip_length": CLIP_LENGTH,
        "processing_mode": "fast",
        "include_broll": False,
        "font_options": {},
    }
    r = requests.post(
        f"{BACKEND}/tasks/", headers=auth_headers(), json=payload, timeout=120
    )
    if r.status_code >= 400:
        print(f"      task create failed: {r.status_code} {r.text[:800]}", flush=True)
        return 1
    body = r.json()
    task_id = body.get("task_id") or body.get("id")
    print(f"      task_id={task_id}", flush=True)

    print("[3/4] Waiting for processing ...", flush=True)
    deadline = time.time() + POLL_TIMEOUT
    last_line = ""
    while time.time() < deadline:
        r = requests.get(
            f"{BACKEND}/tasks/{task_id}", headers=auth_headers(), timeout=60
        )
        r.raise_for_status()
        task = r.json()
        status = task.get("status")
        progress = task.get("progress", 0)
        message = task.get("progress_message", "")
        line = f"      {status} {progress}% {message}"
        if line != last_line:
            print(line, flush=True)
            last_line = line
        if status == "completed":
            break
        if status in ("error", "cancelled"):
            print(f"      TASK FAILED: {json.dumps(task)[:1500]}", flush=True)
            return 1
        time.sleep(30)
    else:
        print("      TIMED OUT waiting for task", flush=True)
        return 1

    print("[4/4] Downloading clips ...", flush=True)
    clips = task.get("clips", [])
    with open(os.path.join(OUT_DIR, "clips.json"), "w") as fh:
        json.dump(clips, fh, indent=2)
    for i, clip in enumerate(clips):
        clip_id = clip.get("id") or clip.get("clip_id")
        title = (clip.get("title") or clip.get("hook") or f"clip{i+1}")[:60]
        score = clip.get("virality_score") or clip.get("score")
        print(f"      clip {clip_id}: {title!r} score={score}", flush=True)
        r = requests.get(
            f"{BACKEND}/tasks/{task_id}/clips/{clip_id}/file",
            headers=auth_headers(),
            timeout=600,
        )
        if r.status_code >= 400:
            print(f"      download failed for {clip_id}: {r.status_code}", flush=True)
            continue
        out = os.path.join(OUT_DIR, f"clip_{i+1:02d}_{clip_id}.mp4")
        with open(out, "wb") as fh:
            fh.write(r.content)
        print(f"      saved {out} ({len(r.content)//1024//1024} MB)", flush=True)

    print("DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
