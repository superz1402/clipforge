"""Stage 2: local transcription with faster-whisper (word timestamps)."""
import json
import os

from faster_whisper import WhisperModel


def _merge_continuation_words(words):
    """Glue faster-whisper fragments that carry no leading space onto the
    previous word (they are sub-word pieces, not real word boundaries)."""
    merged = []
    for w in words:
        text = w["text"]
        if merged and text and not text.startswith(" "):
            merged[-1]["text"] += text
            if w["end"] is not None:
                merged[-1]["end"] = w["end"]
        else:
            merged.append(dict(w))
    for w in merged:
        w["text"] = w["text"].strip()
    return [w for w in merged if w["text"]]


def transcribe(video_path, model_size, workdir):
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments_iter, info = model.transcribe(
        video_path,
        word_timestamps=True,
        vad_filter=True,
        condition_on_previous_text=False,
        beam_size=5,
    )
    words, segments = [], []
    for seg in segments_iter:
        text = seg.text.strip()
        if text:
            segments.append({"start": round(seg.start, 3),
                             "end": round(seg.end, 3), "text": text})
        for w in (seg.words or []):
            if w.start is None or w.end is None:
                continue
            words.append({"start": round(w.start, 3),
                          "end": round(w.end, 3), "text": w.word})
    words = _merge_continuation_words(words)
    data = {
        "language": info.language,
        "language_probability": round(info.language_probability, 3),
        "duration": round(info.duration, 3),
        "words": words,
        "segments": segments,
    }
    out = os.path.join(workdir, "transcript.json")
    with open(out, "w") as f:
        json.dump(data, f)
    print(f"[transcribe] lang={info.language} words={len(words)} "
          f"segments={len(segments)} duration={info.duration:.1f}s")
    return data
