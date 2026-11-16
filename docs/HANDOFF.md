# WildWhyz handoff (written 2026-11-16 ~08:31 IST, pre-expiry)

Everything needed to resume without redoing work. Repo: github.com/superz1402/clipforge
(main @ this commit). GitHub auth: vault login "GitHub token" (sandbox_access=true);
re-materialize with `tools vault write-file --name "GitHub token" --key password
--return-channel whatsapp`, then git -c credential.helper pattern (username superz1402,
password=$(cat ~/.vault/github-token-2ddc96/password)).

## Current phase: awaiting user's verdict on short scripts + music picks

Parent delivered (08:29 IST state): private review File with both short scripts,
then both audio auditions (bird, then jellyfish). No answer yet. NOTHING is rendered,
uploaded, or published since the music incident. Public hold remains.

## Durable artifacts

1. Short scripts (awaiting approval):
   - docs/scripts/birds-firecrackers-v5-short.txt (104 words, TTS-measured 44.064s)
   - docs/scripts/jellyfish-immortal-v2-short.txt (123 words, TTS-measured 53.304s)
   - Also published as a PRIVATE review File (both in one place):
     https://files.instinct.com/nlwzjdfrntcb-short-scripts-bird-44s-jelly-53s
     (fileId file-01M7GTYPTXGYZ5FAC328SVRKZV, generation 2)
2. Narration (regenerable + committed): assets/audio/short-scripts/bird-v5-narration.mp3,
   jelly-v2-narration.mp3. Recipe: edge-tts 7.3.1, voice en-US-BrianMultilingualNeural,
   plain read of the script file. Durations are the timing proofs.
3. Music auditions (committed): assets/audio/short-scripts/bird-v5-audition.mp3,
   jelly-v2-audition.mp3. Recipe: music atrim to narration length, 1.5s fade-in,
   3s fade-out, volume 0.5, sidechaincompress threshold=0.03 ratio=10 attack=15
   release=500 keyed by narration, amix normalize=0, 192k.
4. Music picks + license chain (docs/MUSIC-SOURCING.md, docs/licenses/):
   - bird: "Morning" Kevin MacLeod, CC BY 4.0, per-track evidence
     https://incompetech.com/music/royalty-free/index.html?isrc=USUAN2300003
   - jellyfish: "Dream Culture" Kevin MacLeod, CC BY 4.0,
     https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1300046
   - 6 alternates with full records in docs/licenses/candidates/.
   - Final credits MUST include the change note (see each candidate .md).
5. Fail-closed music state (commit 13d6664): generate.yml passes --bgm-type none AND
   deletes MPT resource/songs/*.mp3 at configure. Policy: docs/MUSIC.md.
6. Clean long masters (narration-only, release assets):
   https://github.com/superz1402/clipforge/releases/tag/preview-jellyfish-v3
   - bird-final-clean.mp4 (129MB; video stream MD5-identical to private preview QlXKY0SRXv8)
   - jellyfish-final-v3.mp4 (music-free by construction)
   These are the LONG versions (1:57 / 1:29); superseded by short scripts if he approves.
7. Jellyfish footage vetting: docs/previews/jellyfish-immortal/SOURCES.md (NOAA
   archive.org trim map), build.sh reproduces the local jellyfish build.
8. Crons/watchdog in generate.yml: DISABLED in YAML. Do not re-enable without user go.

## Open items needing HIS decision (not agent-decidable)

- Verdict on short scripts (File) and music picks/auditions.
- The blocked public bird Short (HAAWK claim on the old music version): replace or
  delete - his call. Claim details: audio "Relaxing Peaceful Piano And Guitar - Praded",
  owner "HAAWK for a 3rd Party", blocked globally, notice dated Nov 15 2026.
- Junk preview cleanup (wwfYnlxKZaI, qNJUkmW09ok, dQiGs9m8HcA) - deletion authority
  still pending.
- YouTube daily upload cap state: UNVERIFIED. No upload retries were scheduled;
  verify live before any upload resume.

## If he approves (continuation recipe)

1. Render each short: narration mp3 + approved music mix (recipe in section 3),
   NOAA/archive.org footage per SOURCES.md pattern, hook overlay + captions
   (scripts/hook_overlay.py, clipforge/captions.py), --bgm-type none stays.
2. Verify actual frames visually before delivery (he catches substitution; check the
   EXACT delivered file, not a lookalike - see galah/cockatoo lesson).
3. Private YouTube preview only. Public only on his explicit go.
4. Video description must carry the change-indicated music credit (candidate .md files).
5. "Illustrative footage" label on generic species footage (standing preference).

## Science sources for the short scripts

- Bird: https://esajournals.onlinelibrary.wiley.com/doi/10.1002/fee.2694 (Hoekstra 2024:
  mass takeoff, anti-predator response to sudden noise, distance-dependent disturbance)
- Jellyfish: https://www.nhm.ac.uk/discover/immortal-jellyfish-secret-to-cheating-death.html
  + https://en.wikipedia.org/wiki/Turritopsis_dohrnii (transdifferentiation, predation/
  disease mortality, no proven individual immortality)
