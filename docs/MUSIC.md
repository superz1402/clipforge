# Music policy (WildWhyz videos)

Incident, Nov 16 2026: YouTube blocked the bird short globally. The claimed audio was
"Relaxing Peaceful Piano And Guitar - Praded" (content owner: HAAWK for a 3rd Party).
Root cause: MoneyPrinterTurbo's default `bgm_type = "random"` mixes a random track from
its bundled `resource/songs/` library (30 untagged `output0XX.mp3` files, no metadata,
no license info, provenance unverifiable) into the final video at 0.2 volume. Our
workflow never set a bgm option, so every render carried one of these tracks.

## Rules

1. Narration-only by default. generate.yml passes `--bgm-type none` AND deletes
   `resource/songs/*.mp3` at configure time, so even a lost flag cannot add music.
2. No MPT bundled songs, ever. No "random" BGM. No track found online under a
   "copyright free" label without a license record.
3. A track may only be used when we hold a saved license record in
   `docs/licenses/` covering our actual use (YouTube, monetization if applicable),
   with the required attribution text recorded alongside it.
4. A Content ID claim is handled by removing the audio, never by disputing without
   verified rights.
5. The claim does not by itself prove infringement, and a license does not by itself
   prevent claims - but absent a verified license record we do not use the track.

## License records

`docs/licenses/` - one file per track: source URL, license text/version, date saved,
attribution string, and where the track was used. Empty as of Nov 16 2026 = no music
in any video.
