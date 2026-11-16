# Why are flamingos pink? - real-footage private preview
41.72 seconds, local Kokoro-82M am_onyx. 100% real footage (41.72s live action, no animation scenes).

## Footage rights and provenance
All three used clips are from Pexels under the Pexels license (https://www.pexels.com/license/, full text saved in docs/licenses/evidence/pexels-license-page.txt, read 2026-11-16): free to use, modification allowed, attribution not required; no standalone resale, no endorsement implication, no stock redistribution, no trademark use. Edited educational Short with narration/captions/music is a modified, permitted use. On-screen credit is included anyway (creator | Pexels) on every scene.

1. "Pink Flamingos in a Pond" - Nicky Pe, https://www.pexels.com/video/pink-flamingos-in-a-pond-8368094/ (20.56s, 2560x1440). Used for the food/pigment and feeding scenes. Pink flamingos feeding with heads swept down in a pond.
2. "Flamingo Feeding in Shallow Water at Sunset" - Amit Rai, https://www.pexels.com/video/flamingo-feeding-in-shallow-water-at-sunset-40078384/ (31.63s, 1920x1080). Used for the opening (a grey-brown juvenile-plumage bird feeding beside pale adults, matching the white-gray chick line without claiming the birds are chicks) and the upside-down filter-feeding mechanism scenes.
3. "A Group of Flamingos Standing in the Water" - Magda Ehlers, https://www.pexels.com/video/a-group-of-flamingos-standing-in-the-water-24812188/ (39.32s, 2560x1440). Closing group shot only; top of frame cropped to remove an enclosure fence.

Exact page URLs, official download links and file URLs preserved in docs/licenses/evidence/pexels-flamingo-clips.json. File URLs were taken from links on each video page itself, not guessed. Every used clip was pixel-inspected across its length: no identifiable people, no logos, no leg bands in the used segments. Two other inspected clips (Magda Ehlers park feeding bin, Brixiv standing birds) were rejected for factual mismatch (captive feeding bin vs wild algae/shrimp narration) and visible leg bands; documented in the same JSON.

Edits: excerpted segments, resized to 1080x1920 with blurred/darkened duplicate background, source audio removed, narration/captions/music added, one top crop (clip 3) to remove a fence.

## Facts
- https://nationalzoo.si.edu/animals/news/why-are-flamingos-pink-and-other-flamingo-facts (sections 1-3): chicks hatch with white-gray feathers; pink comes from carotenoid pigments in food; algae and brine shrimp route; bodies process pigments into feathers; upside-down filter feeding with side-to-side bill sweep; tongue pumps water through comb-like plates (lamellae) that trap food. Script does not claim pigment-to-feather timing or that all species eat identical food.

## Music
"Morning" - Kevin MacLeod (incompetech.com), CC BY 4.0 https://creativecommons.org/licenses/by/4.0/ . Trimmed to 41.72s, 1.5s fade-in, 3s fade-out, sidechain-ducked below narration. Track-specific evidence retained under docs/licenses/evidence/morning-track-page.txt and docs/licenses/candidates/Morning.md. The previously claimed Praded track is not used.

## QA
Full narration transcript matches the script (ASR homophone-level noise only: "in their food" heard as "and their food", "its" as "it's"). 124/125 words aligned; mean original-estimate difference +0.151s, p90 abs 0.354s, max abs 0.642s; recognized starts replaced estimates, monotonicity enforced (alignment-qa.json). Actual final video inspected: 7 scene-midpoint frames, 6 scene-boundary frames and 4 full-resolution frames - subjects uncropped, captions readable with no collisions, hook readable, per-scene credits readable, closing shot fence cropped. No upload, no YouTube calls; upload gate unchanged (YOUTUBE_UPLOAD_ENABLED false).
