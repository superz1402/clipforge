# birds-short-v2 (PRIVATE PREVIEW, not published)
Replaces birds-short-v1, which is WITHDRAWN: unsupported science claims and six Mixkit clips under the Restricted License (personal use only).
Visuals: 100% original cairo animation (pipeline/birds_anim.py). No stock footage.
Science: Hoekstra et al. 2024, https://esajournals.onlinelibrary.wiley.com/doi/full/10.1002/fee.2694 (~1000x birds in flight on NYE on average; effect decreases with distance, strongest within ~5 km, tenfold up to ~10 km). Mechanism lines are hedged ("can", "may").
Music: "Morning" by Kevin MacLeod (incompetech.com), CC BY 4.0 https://creativecommons.org/licenses/by/4.0/ , trimmed and faded. Put the credit in the description.
Voices: Aria = edge-tts en-US-AriaNeural (original MPT voice). Kokoro variants: Kokoro-82M, Apache-2.0 weights (https://huggingface.co/hexgrad/Kokoro-82M), voices am_michael and am_onyx from kokoro-onnx voices-v1.0.bin.
Kokoro dependency licenses (verify before open-sourcing/bundling): kokoro-onnx MIT; onnxruntime MIT; phonemizer GPL-3.0+ (PyPI classifier); espeakng-loader/espeak-ng GPL-3.0 (not checked at source for loader). Weights/audio not affected, but a repo that redistributes or links these GPL parts needs its own license review. Nothing is bundled here; installed via pip at run time.
Kokoro training data note: HF card lists CC BY audio (SIWIS CC BY 4.0, Koniwa CC BY 3.0) in training; the card does not require output attribution, recorded for completeness.
Caption timings for Kokoro are proportional to characters per sentence (approximation), Aria timings come from WordBoundary.
