#!/usr/bin/env python3
"""English-caption pass for externally picked windows (e.g. SupoClip picks).

For each window: cut from the source video, face-tracked 9:16 reframe,
faster-whisper word transcript, LLM translation to English (local Ollama),
burn English karaoke captions.

Usage: english_pass.py --video video.mp4 --windows '[[52,77],[100,130]]' \
         --outdir out --llm-model qwen2.5:7b
"""
import argparse
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from clipforge import captions, reframe, transcribe, translate  # noqa: E402
from clipforge.pipeline import cut_segment  # noqa: E402


def llm_translate(lines, source_lang, model, ollama_url):
    numbered = "\n".join(f"{i+1}. {l}" for i, l in enumerate(lines))
    prompt = (
        "Translate these TV/radio show captions to natural, casual English "
        "subtitles. The show is a Korean K-pop idol radio interview. Keep each "
        "line short and punchy; keep numbers and names accurate. Reply with "
        "ONLY the numbered English lines, same numbering.\n\n" + numbered)
    req = urllib.request.Request(
        f"{ollama_url}/api/generate",
        data=json.dumps({"model": model, "prompt": prompt, "stream": False,
                         "options": {"temperature": 0.2}}).encode(),
        headers={"Content-Type": "application/json"})
    resp = json.load(urllib.request.urlopen(req, timeout=600))["response"]
    out = {}
    for m in re.finditer(r"^\s*(\d+)[\.\)]\s*(.+)$", resp, re.M):
        out[int(m.group(1))] = m.group(2).strip()
    return [out.get(i, lines[i - 1]) for i in range(1, len(lines) + 1)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--windows", required=True,
                    help="JSON list of [start_seconds, end_seconds]")
    ap.add_argument("--outdir", default="out_en")
    ap.add_argument("--llm-model", default="qwen2.5:7b")
    ap.add_argument("--ollama-url", default="http://localhost:11434")
    ap.add_argument("--whisper-model", default="small")
    args = ap.parse_args()

    windows = json.loads(args.windows)
    work = os.path.join(args.outdir, "work")
    os.makedirs(work, exist_ok=True)
    results = []

    for i, (start, end) in enumerate(windows, 1):
        start = max(0.0, float(start) - 1.0)
        end = float(end) + 1.0
        print(f"[clip {i}] window {start}-{end}", flush=True)
        seg = cut_segment(args.video, start, end, work)
        reframed = os.path.join(work, f"reframed_{i}.mp4")
        reframe.reframe(seg, reframed)
        transcript = transcribe.transcribe(seg, args.whisper_model, work)
        lang = transcript["language"]
        lines = captions.group_lines(transcript["words"])
        ko_lines = [" ".join(w["text"] for w in g) for g in lines]
        print(f"[clip {i}] lang={lang} lines={len(lines)}", flush=True)
        if lang == "en":
            en_lines = ko_lines
        else:
            en_lines = llm_translate(ko_lines, lang, args.llm_model,
                                     args.ollama_url)
        translated = [(g[0]["start"], g[-1]["end"], t)
                      for g, t in zip(lines, en_lines)]
        for s, e, t in translated:
            print(f"  {s:6.1f}-{e:6.1f} {t[:80]}", flush=True)
        out = os.path.join(args.outdir, f"clip_{i:02d}_english.mp4")
        translate.burn_translated(os.path.abspath(reframed), translated,
                                  "en", out, work)
        results.append({"window": [start, end], "source_lang": lang,
                        "output": out,
                        "lines": [{"start": s, "end": e, "src": k, "en": t}
                                  for (s, e, t), k in zip(translated, ko_lines)]})

    with open(os.path.join(args.outdir, "english_pass.json"), "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
