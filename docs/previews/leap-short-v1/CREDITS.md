# Why do we have leap years? - private preview
52.79 seconds; local Kokoro 82M am_michael. Original vector animation, no stock assets. Illustrative orbits/clocks, not to scale.

Sources read in full 2026-11-16:
- https://www.jpl.nasa.gov/edu/news/doing-the-math-on-why-we-have-leap-day/ - 365.2422 days (approx), four-year correction overcounts, century/400 exception, 2000 vs 2100.
- https://spaceplace.nasa.gov/leap-year/ - about 365.25 days, about six extra hours, add February 29, keep seasonal/calendar alignment.
All quarter-day/six-hour statements explicitly approximate. No claim that every fourth year always qualifies. Century rule identified visually as Gregorian. Verified 2000/2100 using Python calendar.isleap and 6*4=24, not memory.

Music credit required in any release description:
"Morning" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
https://creativecommons.org/licenses/by/4.0/
Edited: trimmed to 52.79 seconds, 1.5-second fade-in, 3-second fade-out, sidechain-ducked under narration.
Track-specific license evidence: docs/licenses/evidence/morning-track-page.txt and .png.
https://incompetech.com/music/royalty-free/index.html?isrc=USUAN2300003

QA: full narration transcript matches intended script. Base.en Whisper, per-sentence audio slices, number normalization and character-level matching aligned 126/127 words. The remaining unmatched year wording kept its initial estimate. Initial estimate versus recognized timing: mean 0.176s, p90 absolute 0.593s, max absolute 1.441s. These are not measured residual errors: matched estimates were replaced. Final captions monotonic, inspected actual final video sampled frames and all 14 boundary frames, no empty starts/collisions. Removed duplicated opening label after finding hook collision. No claim of auditory emotion review.
No upload; all YouTube activity remains paused.
