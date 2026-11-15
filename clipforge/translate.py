"""Optional stage: local caption translation with Argos Translate (no key).

Produces a translated SRT sidecar and a second burned video with the
translated lines on the original timings.
"""
import os
import subprocess


def _install_package(from_code, to_code):
    from argostranslate import package
    package.update_package_index()
    available = package.get_available_packages()
    pkg = next((p for p in available
                if p.from_code == from_code and p.to_code == to_code), None)
    if pkg is None:
        raise RuntimeError(f"no Argos package {from_code}->{to_code}")
    package.install_from_path(pkg.download())


def _srt_time(t):
    t = max(0.0, t)
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int((s % 1) * 1000):03d}"


def translate_lines(lines, target_lang, source_lang, workdir):
    """Translate grouped caption lines. Returns list of (start, end, text)."""
    _install_package(source_lang, target_lang)
    from argostranslate import translate as argos_translate
    out = []
    for line in lines:
        text = " ".join(w["text"] for w in line)
        translated = argos_translate.translate(text, source_lang, target_lang)
        out.append((line[0]["start"], line[-1]["end"], translated.strip()))
    srt_path = os.path.join(workdir, f"captions.{target_lang}.srt")
    with open(srt_path, "w") as f:
        for i, (start, end, text) in enumerate(out, 1):
            f.write(f"{i}\n{_srt_time(start)} --> {_srt_time(end)}\n"
                    f"{text}\n\n")
    print(f"[translate] {len(out)} lines {source_lang}->{target_lang}")
    return out


def burn_translated(video_path, translated, target_lang, out_path, workdir):
    from .captions import HEADER, _ass_time, _esc
    events = []
    for start, end, text in translated:
        events.append(f"Dialogue: 0,{_ass_time(start)},{_ass_time(end)},"
                      f"Caption,,0,0,0,,{_esc(text)}")
    ass_name = f"captions.{target_lang}.ass"
    with open(os.path.join(workdir, ass_name), "w") as f:
        f.write(HEADER + "\n".join(events) + "\n")
    cmd = [
        "ffmpeg", "-y", "-i", video_path, "-vf", f"ass={ass_name}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
        out_path,
    ]
    proc = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"ffmpeg translated burn failed:\n{proc.stderr[-2000:]}")
    print(f"[translate] burned -> {out_path}")
