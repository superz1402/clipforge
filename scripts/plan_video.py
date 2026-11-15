#!/usr/bin/env python3
"""Plan a short with the local Ollama LLM: narration script + per-beat
footage search phrases.

Writes into --outdir:
  script.txt   - full narration (sentences joined)
  beats.txt    - one sentence per line (beat 1 = the hook)
  phrases.txt  - one footage search phrase per beat, same order

Every phrase is constrained to literally show the video's main subject, so
the footage matches the topic instead of drifting to generic nature clips.

Exits non-zero when the LLM is unreachable or returns unusable text, so the
workflow can fall back to the simpler subject-based path.
"""

import argparse
import json
import re
import sys
import urllib.request

SCRIPT_PROMPT = """Write a YouTube Shorts voiceover script about: {subject}.
Rules:
- 60 to 80 words total
- exactly 6 short sentences
- the first sentence is a hook under 12 words that creates curiosity
- conversational, surprising facts, no intro or outro filler
- output ONLY the 6 sentences, one per line, no numbering, no quotes"""

PHRASES_PROMPT = """Topic: {subject}
Narration sentences:
{numbered}

For each sentence, write ONE stock-footage search phrase (2-4 words) that literally shows what that sentence describes.
Rules:
- every phrase MUST name the video's main subject (for an animal video, the animal's name appears in every phrase)
- visually concrete (what a camera would see), no abstract words
- output ONLY the numbered phrases, one per line"""


def ollama(prompt, model, base_url):
    url = base_url.rstrip("/") + "/api/generate"
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.load(resp).get("response", "")


def clean_lines(text):
    lines = []
    for raw in text.strip().splitlines():
        line = re.sub(r"^\s*\d+[\.\)]\s*", "", raw).strip().strip('"').strip()
        if line and not line.lower().startswith(("here", "sure", "output")):
            lines.append(line)
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--model", default="qwen2.5:3b")
    ap.add_argument("--base-url", default="http://localhost:11434")
    ap.add_argument("--outdir", default="plan")
    args = ap.parse_args()

    script_raw = ollama(SCRIPT_PROMPT.format(subject=args.subject), args.model, args.base_url)
    beats = clean_lines(script_raw)[:6]
    if len(beats) < 4:
        print(f"script unusable ({len(beats)} beats)", file=sys.stderr)
        return 1

    numbered = "\n".join(f"{i + 1}. {b}" for i, b in enumerate(beats))
    phrases_raw = ollama(
        PHRASES_PROMPT.format(subject=args.subject, numbered=numbered), args.model, args.base_url
    )
    phrases = clean_lines(phrases_raw)
    phrases = [re.sub(r"[^a-zA-Z0-9 ]", "", p).strip() for p in phrases if p.strip()]
    phrases = [p for p in phrases if len(p.split()) >= 2][: len(beats)]
    if len(phrases) < 3:
        print(f"phrases unusable ({len(phrases)})", file=sys.stderr)
        return 1

    # pad missing beats with the subject itself
    while len(phrases) < len(beats):
        phrases.append(args.subject)

    import os
    os.makedirs(args.outdir, exist_ok=True)
    with open(f"{args.outdir}/script.txt", "w") as f:
        f.write(" ".join(beats))
    with open(f"{args.outdir}/beats.txt", "w") as f:
        f.write("\n".join(beats) + "\n")
    with open(f"{args.outdir}/phrases.txt", "w") as f:
        f.write("\n".join(phrases) + "\n")
    print(f"beats: {len(beats)}, phrases: {len(phrases)}")
    for i, (b, p) in enumerate(zip(beats, phrases)):
        print(f"  {i + 1}. [{p}] {b[:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
