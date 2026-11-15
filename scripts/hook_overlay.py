#!/usr/bin/env python3
"""Burn a hook-title overlay onto a short: the first subtitle cue's text,
large and top-center, shown while the first sentence plays (max 5s).

Usage: hook_overlay.py --video in.mp4 --srt subtitle.srt --out out.mp4
Exits 0 without writing output when no usable first cue exists.
"""

import argparse
import re
import subprocess
import sys
import tempfile
import os

MAX_HOOK_SECONDS = 5.0

ASS_TEMPLATE = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,DejaVu Sans,78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,5,0,8,50,50,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,{start},{end},Hook,,0,0,0,,{text}
"""


def first_cue(srt_path):
    blocks = re.split(r"\n\s*\n", open(srt_path, encoding="utf-8").read().strip())
    for b in blocks:
        lines = b.strip().splitlines()
        if len(lines) < 2:
            continue
        time_line = lines[1] if "-->" not in lines[0] else lines[0]
        text_lines = lines[2:] if "-->" not in lines[0] else lines[1:]
        m = re.match(
            r"(\d+):(\d\d):(\d\d)[,.](\d\d\d)\s*-->\s*(\d+):(\d\d):(\d\d)[,.](\d\d\d)",
            time_line,
        )
        if m and text_lines:
            h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, m.groups())
            start = h1 * 3600 + m1 * 60 + s1 + ms1 / 1000
            end = h2 * 3600 + m2 * 60 + s2 + ms2 / 1000
            return start, end, " ".join(text_lines).strip()
    return None


def ass_time(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{(cs // 6000) % 60:02d}:{(cs // 100) % 60:02d}.{cs % 100:02d}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--video", required=True)
    p.add_argument("--srt", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--text", default="", help="hook text override (default: first srt cue)")
    a = p.parse_args()

    if a.text.strip():
        start, end, text = 0.1, MAX_HOOK_SECONDS, a.text.strip()
    else:
        cue = first_cue(a.srt)
        if not cue:
            print("no usable first cue; hook overlay skipped")
            return 0
        start, end, text = cue
        end = min(end, start + MAX_HOOK_SECONDS)
    text = re.sub(r"\{[^}]*\}", "", text).upper().replace("\n", " ").strip()
    words = text.split()
    if len(words) > 10:
        text = " ".join(words[:10])
    if not text:
        print("empty hook text; skipped")
        return 0

    ass = ASS_TEMPLATE.format(start=ass_time(start), end=ass_time(end), text=text)
    with tempfile.NamedTemporaryFile("w", suffix=".ass", delete=False, encoding="utf-8") as f:
        f.write(ass)
        ass_path = f.name
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", a.video, "-vf", f"ass={ass_path}",
             "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-c:a", "copy", a.out],
            check=True,
        )
    finally:
        os.unlink(ass_path)
    print(f"hook overlay: \"{text}\" {start:.1f}-{end:.1f}s -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
