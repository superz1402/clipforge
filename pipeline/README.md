Reusable short pipeline. build.sh SCRIPT.json VOICE OUTDIR MUSIC.mp3 HOOK OUT.mp4
Measured (2 vCPU, 1 GB): Kokoro TTS 20-23 s, animation 12-14 s, caption+mix+encode 12-14 s => ~45-51 s per 37-44 s video once script and scenes exist.
Not automated: writing the script, fact check, and scene code for a NEW topic (birds_anim.py is topic-specific). Rights gate: only original animation or per-asset verified license; no scraped stock.
Setup: pip install kokoro-onnx soundfile; models from https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0 into /downloads/kokoro/.
