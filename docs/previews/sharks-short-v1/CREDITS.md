# Why sharks are older than trees - real-footage private preview
54.61 seconds, local Kokoro-82M am_michael. 100% real footage (no animation scenes).

## Footage rights and provenance
All five used clips are from Pexels under the Pexels license (https://www.pexels.com/license/, full text saved in docs/licenses/evidence/pexels-license-page.txt, read 2026-11-16): free to use, modification allowed, attribution not required. Edited educational Short with narration/captions/music is a permitted modified use. On-screen "creator | Pexels" credit is burned into every scene anyway.

1. "A Shark Swimming in the Ocean with Grass and Seaweed" - Florian Delée - hook and "already swimming" scenes (slowed to 80%).
2. "Graceful Movement of a Shark Underwater" - Yusuf Mahammed - fossil-scales scene, shark against the sun (slowed to 60%).
3. "Aerial View of Dense Pine Forest" - Julien Goettelmann - first-trees scene.
4. "A Whale Shark Swimming Under Water" - Lachlan Ross - mass-extinction survivor scene (95%).
5. "Close-Up View of Shark Swimming Underwater" - Magda Ehlers - cartilage/teeth-fossils scene and closing scene (95%/88%).

Exact page URLs, official download links and file URLs in docs/licenses/evidence/pexels-shark-clips.json. File URLs taken from links on each video page itself. Every used clip pixel-inspected: no identifiable people in used segments, no logos. Two clips were downloaded, inspected and REJECTED (jellyfish-dominant clip = subject mismatch; extra 2.8s clip unneeded); documented in the same JSON.

Edits: excerpted segments, some slowed (60-95%), resized to 1080x1920 with blurred/darkened duplicate background, source audio removed, narration/captions/music added.

## Facts
- https://www.nhm.ac.uk/discover/shark-evolution-a-450-million-year-timeline.html - earliest shark-like scales ~450 mya (Late Ordovician), cartilage skeleton (only teeth not cartilage), survived five mass extinctions including End-Cretaceous.
- https://www.livescience.com/animals/sharks/are-sharks-really-older-than-trees - first true trees (Archaeopteris) ~385 mya; modern shark groups ~195 mya; the lineage-vs-definition nuance, which the script states explicitly in the closing sentence.
- https://www.nhm.ac.uk/discover/when-did-dinosaurs-live.html - dinosaurs first appeared ~245 mya.
Script claims: shark-like scales ~450M, first true trees ~385M, dinosaurs ~245M, 60M+ years of shark-ancestor swimming before first forests (450-385), five mass extinctions survived, cartilage skeleton -> mostly teeth fossils, modern shark species younger than trees. No stronger claim made.

## Music
"Morning" - Kevin MacLeod (incompetech.com), CC BY 4.0 https://creativecommons.org/licenses/by/4.0/ . Trimmed to 54.61s, 1.5s fade-in, 3s fade-out, sidechain-ducked below narration. Evidence: docs/licenses/evidence/morning-track-page.txt. Praded track not used.

## QA
Full narration transcript matches script (ASR noise only on one fast clause). 124/124 words aligned; mean estimate error +0.153s, p90 abs 0.676s, max abs 1.319s; monotonicity enforced (alignment-qa.json). Actual final video inspected: 7 scene-midpoint frames, 6 boundary frames, 1 hook frame, 1 full-res frame - footage matches each sentence (teeth close-up on the fossils line), captions/hook/credits readable, no collisions, no empty frames. No upload, no YouTube calls; upload gate unchanged false.
