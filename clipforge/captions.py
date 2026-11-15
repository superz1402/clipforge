"""Stage 6: karaoke captions + hook overlay as an ASS subtitle, burned in."""
import subprocess

MAX_WORDS_PER_LINE = 4
MAX_LINE_SECONDS = 2.2
HOOK_SECONDS = 2.8

HEADER = """[Script Info]
PlayResX: 1080
PlayResY: 1920
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Caption,DejaVu Sans,78,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,5,0,2,60,60,220,1
Style: Hook,DejaVu Sans,104,&H0000D7FF,&H0000D7FF,&H00000000,&H80000000,1,0,0,0,100,100,1,0,1,6,0,8,60,60,330,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def _ass_time(t):
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def _esc(text):
    return text.replace("{", "(").replace("}", ")").replace("\n", " ")


def group_lines(words):
    """Split word stream into short caption lines."""
    lines, cur = [], []
    for w in words:
        if cur and (len(cur) >= MAX_WORDS_PER_LINE
                    or w["start"] - cur[0]["start"] > MAX_LINE_SECONDS):
            lines.append(cur)
            cur = []
        cur.append(w)
    if cur:
        lines.append(cur)
    return lines


def karaoke_text(line_words):
    parts = []
    for w in line_words:
        cs = max(1, int(round((w["end"] - w["start"]) * 100)))
        parts.append(f"{{\\kf{cs}}}{_esc(w['text'])}")
    return " ".join(parts)


def build_ass(words, hook, clip_duration, path):
    """words: list with clip-local timestamps. Returns the grouped lines."""
    events = []
    lines = group_lines(words)
    for line in lines:
        start, end = line[0]["start"], line[-1]["end"]
        events.append(
            f"Dialogue: 0,{_ass_time(start)},{_ass_time(end)},"
            f"Caption,,0,0,0,,{karaoke_text(line)}")
    hook = (hook or "").strip()
    if hook:
        hook_end = min(HOOK_SECONDS, clip_duration)
        events.append(
            f"Dialogue: 1,{_ass_time(0)},{_ass_time(hook_end)},"
            f"Hook,,0,0,0,,{_esc(hook)}")
    with open(path, "w") as f:
        f.write(HEADER + "\n".join(events) + "\n")
    return lines


def burn(video_path, ass_path, out_path, cwd):
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"ass={ass_path}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
        out_path,
    ]
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg caption burn failed:\n{proc.stderr[-2000:]}")
    print(f"[captions] burned {ass_path} -> {out_path}")
