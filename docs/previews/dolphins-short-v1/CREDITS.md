# Dolphins sleep with one eye open — preview v1 (real footage)

- Voice: Kokoro-82M am_onyx. Length: 37.21s. Words: 128. Hook caption: "HALF ASLEEP, HALF AWAKE".
- Script: pipeline/dolphins.script.json (7 sentences, ends with comment-bait question).
- Compositor: pipeline/mix_dolphins_real.py (1080x1920, blurred bg, center-cropped fg band, per-clip credit line).
- Music: assets/music/candidates/Morning.mp3 (Kevin MacLeod, CC BY 4.0 — see existing music evidence).
- TTS/align QA: 131/132 words matched on stability re-check, mean drift -0.002s, p90 0.02s, max 0.34s.
- Visual QA: 28 dense temporal samples (every ~1.4s across the whole video) + 7 midpoints + 6 boundary frames + hook inspected. v2 note: midpoint/boundary-only sampling missed a boat hull inside scene 4 in v1; dense sampling is now standard (dolphins-QA-mids.png, dolphins-QA-bounds.png). No people, boats, watermarks, or UI artifacts in any shipped frame.

## Facts (verified)
- Unihemispheric slow-wave sleep: one brain hemisphere rests while the other stays alert; they alternate.
- Breathing is voluntary: cetaceans must consciously take every breath and cannot breathe when unconscious (source cites anaesthetized captive dolphins that stopped breathing). Video ties breath-stopping to unconsciousness, not to sleep per se.
- One eye remains active while the eye associated with the sleeping brain hemisphere is shut (wording mirrors the source; no body-side/laterality claim is made in the video).
- They rest motionless at/near the surface or in the water column, or swim slowly; the alert half watches for predators and controls surfacing to breathe.
Source: ORCA Foundation, "Cetacean Sleep" — https://orcafoundation.com/2017/08/cetacean-sleep/

## Footage (all real, Pexels License — https://www.pexels.com/license/, full text in docs/licenses/evidence/pexels-license-page.txt)
- USED: claudio baroni, "Captivating Underwater Dolphin Group Swim" — https://www.pexels.com/video/captivating-underwater-dolphin-group-swim-35610558/ (all 7 scenes; verified-safe source ranges t=4-18.5 and t=19-30.1; a boat hull enters at ~t=31 and a snorkeler selfie at ~t=37 — both excluded).
- REJECTED: Kemal Can https://www.pexels.com/video/dolphins-swimming-in-open-ocean-waters-33768424/ (dolphins not visible).
- DOWNLOADED, UNUSED: Adrien JACTA https://www.pexels.com/video/a-pod-of-dolphins-swimming-in-the-blue-sea-15546561/ (dolphins too distant); "Diana" https://www.pexels.com/video/dolphins-swimming-underwater-11042822/ and https://www.pexels.com/video/dolphin-group-swimming-in-blue-water-11042832/ (captive pool: visible walls, floor drain).
