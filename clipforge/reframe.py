"""Stage 5: face-tracked 9:16 reframe (MediaPipe + OpenCV -> ffmpeg).

Detects the main face on sampled frames, smooths the horizontal track with an
EMA, crops a 9:16 window and encodes 1080x1920 through an ffmpeg pipe.
Falls back to a center crop when no face is ever found.
"""
import subprocess

import cv2
import numpy as np

OUT_W, OUT_H = 1080, 1920
ASPECT = OUT_W / OUT_H  # 9/16


def _crop_geometry(w, h):
    """Crop box size for a 9:16 window inside a w x h frame."""
    if w / h >= ASPECT:  # landscape-ish: full height, narrower width
        crop_h = h
        crop_w = int(h * ASPECT) & ~1
    else:  # already narrow: full width, shorter height
        crop_w = w & ~1
        crop_h = int(w / ASPECT) & ~1
    return crop_w, crop_h


def _detect_faces(detector, frame_bgr, w, h):
    """Return (cx, cy) of the highest-confidence face in full-frame coords."""
    scale = 320.0 / w
    small = cv2.resize(frame_bgr, (320, max(1, int(h * scale))))
    results = detector.process(cv2.cvtColor(small, cv2.COLOR_BGR2RGB))
    if not results.detections:
        return None
    best = max(results.detections, key=lambda d: d.score[0])
    box = best.location_data.relative_bounding_box
    cx = (box.xmin + box.width / 2) * w
    cy = (box.ymin + box.height / 2) * h
    return cx, cy


def reframe(segment_path, out_path):
    import mediapipe as mp  # heavy import, done lazily

    cap = cv2.VideoCapture(segment_path)
    if not cap.isOpened():
        raise RuntimeError(f"cannot open {segment_path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    crop_w, crop_h = _crop_geometry(w, h)
    detector = mp.solutions.face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.4)

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-pix_fmt", "bgr24",
        "-s", f"{OUT_W}x{OUT_H}", "-r", f"{fps:.6f}", "-i", "-",
        "-i", segment_path,
        "-map", "0:v", "-map", "1:a?",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", out_path,
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    cx_smooth, cy_smooth, faces_seen = None, None, 0
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % 6 == 0:
            found = _detect_faces(detector, frame, w, h)
            if found is not None:
                faces_seen += 1
                if cx_smooth is None:
                    cx_smooth, cy_smooth = found
                else:
                    cx_smooth = 0.75 * cx_smooth + 0.25 * found[0]
                    cy_smooth = 0.75 * cy_smooth + 0.25 * found[1]
        if cx_smooth is None:
            cx, cy = w / 2, h / 2
        else:
            cx, cy = cx_smooth, cy_smooth
        x0 = int(min(max(cx - crop_w / 2, 0), w - crop_w))
        y0 = int(min(max(cy - crop_h / 2, 0), h - crop_h))
        crop = frame[y0:y0 + crop_h, x0:x0 + crop_w]
        resized = cv2.resize(crop, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)
        proc.stdin.write(resized.astype(np.uint8).tobytes())
        idx += 1

    cap.release()
    detector.close()
    proc.stdin.close()
    rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg reframe exited {rc}")
    mode = "face-tracked" if faces_seen else "center-crop fallback"
    print(f"[reframe] {idx} frames -> {OUT_W}x{OUT_H} ({mode})")
