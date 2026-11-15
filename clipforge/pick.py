"""Stage 3: pick the best clip moment with a local Ollama model.

Falls back to a speech-density heuristic when no LLM is reachable, so the
pipeline never hard-fails on this stage.
"""
import json
import os

import requests


def _fmt_ts(seconds):
    m = int(seconds // 60)
    s = seconds - m * 60
    return f"{m:02d}:{s:04.1f}"


def _clamp_moment(moment, duration, min_clip, max_clip):
    start = max(0.0, min(float(moment["start"]), duration))
    end = max(0.0, min(float(moment["end"]), duration))
    if end - start > max_clip:
        end = start + max_clip
    if end - start < min_clip:
        end = min(duration, start + min_clip)
        if end - start < min_clip:
            start = max(0.0, end - min_clip)
    moment["start"], moment["end"] = round(start, 2), round(end, 2)
    moment.setdefault("title", "Clip")
    moment.setdefault("hook", "")
    moment.setdefault("reason", "")
    return moment


def _fallback_moment(transcript, min_clip, max_clip):
    """Highest speech-density window of max_clip seconds (earliest on ties)."""
    words = transcript["words"]
    duration = transcript["duration"]
    if not words:
        end = min(duration, max_clip)
        return {"start": 0.0, "end": round(end, 2), "title": "Clip",
                "hook": "", "reason": "no speech found", "source": "fallback"}
    win = min(max_clip, duration)
    starts = [w["start"] for w in words]
    best_start, best_count = 0.0, -1
    j = 0
    for i, w in enumerate(words):
        while starts[i] - starts[j] > win:
            j += 1
        count = i - j + 1
        if count > best_count:
            best_count, best_start = count, starts[j]
    end = min(duration, best_start + win)
    hook = " ".join(w["text"] for w in words
                    if best_start <= w["start"] < best_start + 6)[:60]
    return {"start": round(best_start, 2), "end": round(end, 2),
            "title": "Clip", "hook": hook,
            "reason": "speech-density heuristic", "source": "fallback"}


def _ask_ollama(ollama_url, model, prompt):
    resp = requests.post(
        f"{ollama_url}/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content":
                 "You pick the single most shareable moment from a video "
                 "transcript for a short vertical clip. You answer with JSON "
                 "only."},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.3, "num_ctx": 8192},
        },
        timeout=600,
    )
    resp.raise_for_status()
    return json.loads(resp.json()["message"]["content"])


def pick_moment(transcript, ollama_url, model, min_clip, max_clip,
                workdir, use_llm=True):
    duration = transcript["duration"]
    lines = [f"[{_fmt_ts(s['start'])}] {s['text']}"
             for s in transcript["segments"]]
    joined = "\n".join(lines)
    if len(joined) > 24000:
        joined = joined[:24000] + "\n[...truncated...]"
    prompt = (
        f"Transcript with [mm:ss] timestamps (video is {duration:.0f}s):\n\n"
        f"{joined}\n\n"
        f"Pick the ONE moment that would perform best as a short vertical "
        f"clip: self-contained, surprising or insightful, strong opening "
        f"line. It must be between {min_clip} and {max_clip} seconds long - "
        f"aim for {max_clip} seconds unless the moment is clearly stronger "
        f"when short. Skip intro/outro branding and title cards. Only "
        f"choose a window that actually contains transcript lines.\n"
        f'Respond with JSON only: {{"start": <seconds>, "end": <seconds>, '
        f'"title": "<3-6 word clip title>", "hook": "<punchy on-screen hook, '
        f'max 8 words>", "reason": "<why this moment>"}}'
    )
    moment = None
    if use_llm:
        for attempt in (1, 2):
            try:
                raw = _ask_ollama(ollama_url, model, prompt)
                moment = _clamp_moment(raw, duration, min_clip, max_clip)
                moment["source"] = f"ollama:{model}"
                break
            except Exception as exc:  # noqa: BLE001 - any LLM failure falls back
                print(f"[pick] LLM attempt {attempt} failed: {exc}")
    if moment is not None:
        words_in = sum(1 for w in transcript["words"]
                       if w["end"] > moment["start"]
                       and w["start"] < moment["end"])
        if words_in < 8:
            print(f"[pick] LLM window has only {words_in} words - "
                  "rejecting, using fallback")
            moment = None
    if moment is None:
        moment = _fallback_moment(transcript, min_clip, max_clip)
    with open(os.path.join(workdir, "moment.json"), "w") as f:
        json.dump(moment, f, indent=2)
    print(f"[pick] {moment['start']}-{moment['end']}s "
          f"({moment['end'] - moment['start']:.0f}s) "
          f"via {moment['source']}: {moment.get('title')!r}")
    return moment
