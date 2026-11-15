# Jellyfish preview - vetted footage sources and build recipe

Audio/subtitles: GitHub Actions artifact of run 43752363557 (audio.mp3, subtitle.srt,
script.json). Narration = user's own script docs/scripts/jellyfish-immortal-v1.txt verbatim.

Footage: archive.org NOAA Ocean Exploration, public domain. Download URLs and the
vetted trim ranges used in the corrected preview (all times in source seconds):

| file | URL | usable range | flaws outside range |
|---|---|---|---|
| redjelly | https://archive.org/download/noaa-oe-video-video-playlist-ex2104-redjelly/ex2104-dive20-redjelly-1280x720-2.ia.mp4 | 7.5-20.7 center-crop; 20.8-23.5 crop x=1700 | end slate from ~28s |
| ex1502 | https://archive.org/download/noaa-oe-video-video-shorts-ex1502-jelly1/ex1502-jelly1.mp4 | 13.5-21.5 center-crop | NOAA logo slate 0-~8s, "MONA CANYON" text ~8-13s, end slate from ~28.5s |
| bigjelly | https://archive.org/download/noaa-oe-video-okeanos-explorations-express-ex2301-gallery-media-ex2301-dive07-bigjelly/ex2301-dive07-bigjelly-1280x720-1.mp4 | 9-53.4 center-crop (whole mid) | lower-third title 0-~7s, end-slate fade from ~54s |
| blooming | https://archive.org/download/noaa-oe-video-okeanos-explorations-ex1907-logs-nov3-media-blooming-jelly/jelly-1280x720-1.mp4 | 21-28 crop x=1700 | near-black 0-8s and 29s+, small/dark jelly 8-21 center-crop |
| stella-medusa | https://archive.org/download/noaa-oe-video-jellyfish-tracking/stella-medusa.mp4 | REJECTED | MBARI dark footage, green timecode burned in whole clip |

Segment table (order, source, start, len, crop) - total 88.73s:
1 redjelly 7.5 13.2 center | 2 ex1502 13.5 8.0 center | 3 bigjelly 9.0 13.2 center |
4 blooming 21.0 7.0 x1700 | 5 bigjelly 25.0 12.7 center | 6 redjelly 7.6 12.9 center (reuse) |
7 bigjelly 40.0 13.4 center | 8 blooming 21.05 6.95 x1700 (reuse) | 9 redjelly 20.8 1.38 x1700

Pipeline fix needed upstream: archive_best_file must skip slates/timecodes; ranges above are the manual map.
