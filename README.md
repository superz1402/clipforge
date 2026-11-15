# ClipForge

Hands-free pipeline that turns a long-form video into a vertical (9:16) clip
with karaoke captions, a hook overlay, and optional auto-translated captions.

**Fully open-source, zero cost, no API keys required.** Everything runs on a
free GitHub Actions runner with local models only.

## Pipeline

```
video URL (direct file, non-YouTube)
  -> yt-dlp download
  -> faster-whisper transcription (word-level timestamps, local)
  -> Ollama local LLM moment picking (qwen2.5:3b by default,
     speech-density heuristic fallback)
  -> ffmpeg segment cut
  -> MediaPipe + OpenCV face-tracked 9:16 reframe (center-crop fallback)
  -> karaoke captions + hook overlay burned with ffmpeg/libass
  -> optional Argos Translate caption translation (local, no key)
  -> downloadable Actions artifact
```

## Usage

1. Go to **Actions -> clip -> Run workflow**.
2. Paste a direct video file URL (YouTube is bot-blocked from cloud IPs, so
   use your own uploads or other direct sources).
3. Optionally set a translation target language (`es`, `hi`, `fr`, ...).
4. Download the `clipforge-output` artifact when the run finishes:
   - `clip_final.mp4` - 1080x1920 clip with karaoke captions and hook
   - `clip_final.<lang>.mp4` + `captions.<lang>.srt` - translated variant
   - `metadata.json` - moment choice, reason, and run details
   - `transcript.json` - full word-level transcript

## Run locally

```bash
pip install -r requirements.txt
ollama serve &          # optional: for LLM moment picking
ollama pull qwen2.5:3b  # optional
python -m clipforge.pipeline --input /path/to/video.mp4 --target-lang es
# add --no-llm to use the heuristic picker instead of Ollama
```

## Design notes

- GitHub Actions runners give ~4 vCPU / 7-16 GB RAM, so defaults stay small:
  whisper `base`, a 3B-class Ollama model. Both are inputs - bump them on
  bigger runners (e.g. a free Oracle ARM box) for better quality.
- Moment picking never blocks the pipeline: if the LLM is unreachable or
  returns junk, a speech-density heuristic picks the window instead.
- Reframe detects the main face on sampled frames and EMA-smooths the crop
  track to avoid jump cuts; with no faces it center-crops.
- Translation is a local Argos Translate package download, keyed off the
  detected transcript language.

## Workflows

| Workflow | What it does |
| --- | --- |
| `clip.yml` | The original ClipForge pipeline above: one video URL in, one captioned 9:16 clip out. |
| `supoclip.yml` | Runs [our SupoClip fork](https://github.com/superz1402/supoclip) (AGPL) on the runner via Docker Compose: LLM moment picking, virality scores, styled karaoke captions. Adds `CAPTION_TRANSLATE_TO` (fork feature) for translated captions via the local LLM. Key-free: local whisper + Ollama. |
| `english.yml` | English caption pass for externally picked windows (e.g. SupoClip `clips.json`): cut, reframe, transcribe, LLM-translate, burn. |
| `generate.yml` | MoneyPrinterTurbo (pinned) fully key-free: local LLM script, edge-tts voice, Mixkit-scraped stock footage (no API key), composed short. Runs daily via cron (topic auto-picked from `topics.txt`) or on demand. Optional YouTube auto-upload: set repo variable `YOUTUBE_UPLOAD_ENABLED=true` plus secrets `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` (OAuth consent screen must be published to production, or the refresh token expires weekly). |

## Roadmap

- Multiple ranked clips per run
- Packaging as a hosted service

## Credits

Architecture inspired by [OpenShorts](https://github.com/mutonby/openshorts)
(MIT). No code from SupoClip (AGPL) is used in this repo; the
[SupoClip fork](https://github.com/superz1402/supoclip) lives separately under
its AGPL license. Built with yt-dlp, faster-whisper, Ollama, MediaPipe,
OpenCV, ffmpeg, Argos Translate, and Mixkit footage.

## License

MIT - see [LICENSE](LICENSE).
