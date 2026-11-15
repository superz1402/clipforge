# WildWhyz ops handoff (Nov 15, 2026)

Everything a fresh agent needs to operate this system cold. Read this file first.

## What this is
Hands-free daily YouTube Shorts pipeline for the user's channel **WildWhyz** (animal-facts
shorts, question-hook style modeled on IG accounts hoodieguyofficial1 / unhingedwildlife -
ideas only, never their footage/audio). Zero cost, no paid API keys: everything runs on
GitHub Actions free runners with local Ollama models. User is Android-only; all state lives
in GitHub + the user's Instinct vault.

## Repos (GitHub account superz1402)
- **clipforge** - the pipeline (MIT). This repo. HEAD of main is current truth.
- **supoclip** - AGPL fork of SupoClip with CAPTION_TRANSLATE_TO + CAPTION_NAMES_PACK
  (Korean fan-channel caption translation; separate project, keep both repos green).
- **perfect-srt** - ASR name-correction packs (living files; fold new mangles in as seen).

## Daily run chain
1. `generate.yml` cron `30 13 * * *` (13:30 UTC = 7:00 PM IST). GitHub cron can lag 90+ min.
2. `watchdog.yml` cron `50 13 * * *` dispatches generate.yml if no run started in 40 min.
   Needs secret `WATCHDOG_PAT` (already set = his GitHub PAT; PAT expiry kills the watchdog -
   re-set from vault item "github-token" if it ever 401s).
3. Topic = `topics.txt` line `(day-of-year % 30) + 1`. Full mapping: `docs/content-calendar.md`.

## Secrets / vault
- GH secrets on clipforge: `YT_REFRESH_TOKEN`, `YT_CLIENT_ID`, `YT_CLIENT_SECRET`,
  `WATCHDOG_PAT`. All set Nov 15.
- Vault (user's Instinct): "github-token" (PAT, approved for sandbox use),
  "WildWhyz YouTube client" (OAuth client id/secret), "WildWhyz YouTube refresh token".
- **PENDING:** current refresh token has scope `youtube.upload` ONLY. A vault request link
  was sent (via main) for a re-mint WITH `youtube.force-ssl` added. When the user submits it:
  1. `tools vault write-file --name "WildWhyz YouTube refresh token" --key password` to the
     sandbox file (`~/.vault/wildwhyz-youtube-refresh-token-*/password`).
  2. Verify scope locally: exchange refresh_token for access_token, check
     `tokeninfo.scope` contains BOTH `youtube.upload` and `youtube.force-ssl`.
  3. Re-seal into GH secret `YT_REFRESH_TOKEN` (sodium sealed-box, same pattern as WATCHDOG_PAT).
  4. Then delete the bad public video `dQiGs9m8HcA` via `videos.delete` and confirm to main.

## Uploads so far
- PUBLIC bad v1 `dQiGs9m8HcA` (cars/B&W park footage - user told to delete manually; delete
  via API once force-ssl lands).
- PUBLIC good `NZZY99Wh8dM` (birds/firecrackers, verified frame-by-frame, ~24s).
- Private samples: octopus v4 `toSDEHipg0Y`, v5 `yLjseqCVB14`, cats `B9QsfBgkF4Y`.

## Known fragility
- **Planner LLM (qwen2.5:3b) is flaky** (~1 in 3 runs produces an unusable script; one-retry
  added Nov 15). Fallback path still ships a decent video but without the hook-title overlay
  and per-beat footage ordering. If a run's log says `PLANNED=no`, that's what happened.
- **Mixkit animal coverage** (clips per query): zero for clownfish, salmon, otter,
  mantis-shrimp, squirrel, raccoon, snail, peacock, swan, duck, firefly; hummingbird only 2.
  Never add topics needing those unless a NOAA archive.org fallback is wired (ident prefix
  `noaa-oe-video-`; same IA collection contains junk B&W NPS items - filter by prefix).
- GH artifacts with the same name across runs merge stale files - artifact names are
  unique per run (`mpt-output-<run_id>`); keep it that way.
- edge-tts: `AndrewMultilingualNeural` is broken server-side; voice is
  `en-US-BrianMultilingualNeural`, edge_tts pinned 7.3.1.
- MPT pinned commit ce289ffb; CLI flags override config.toml for concat mode/duration.

## Gate-check procedure (every daily run, before telling the user it's good)
1. Run is green: `gh api repos/superz1402/clipforge/actions/runs?per_page=3`.
2. Download artifact, extract grid.jpg/hook.jpg, LOOK at the frames (footage matches topic,
   captions low/legible, no off-topic clips). Trust pixels, not logs.
3. Check `PLANNED=yes/no` in the log and say which path ran when reporting.
4. Report to main with run URL + youtu.be URL + verdict + clip attached (compress
   `ffmpeg -crf 26 -preset medium -c:a aac -b:a 96k` to fit 20 MB).

## Open user requests (not pipeline bugs)
- He has 30+ pre-made shorts on his Drive he wants drip-fed. Main asked which channel +
  folder link; unanswered as of Nov 15 8:45 PM. Route via main when he answers.
- K-pop fan channel (supoclip side): SBS-copyrighted clips, not monetizable, side project.

## User's standing rules
- Zero spend, no paid API keys. Public go-live approved Nov 15 ("Yup, approved").
- He judges footage quality harshly - always gate-check frames before celebrating.

## Script quality standard (Nov 15, user's verdict)
His verdict on the first bird short: "scripting was not good, doesn't feel informational,
too short to get clarity." He then confirmed the standard for ALL videos: explain why/how,
clear setup, proper explanation, takeaway - length follows the explanation. plan_video.py
now enforces this (8-beat structure as a guide, ~90-115 words, longer when the explanation needs it). Approved scripts can be rendered
verbatim via the workflow's `script` dispatch input (skips the LLM). The approved bird
remake script is docs/scripts/birds-firecrackers-v3.txt.
**Cron uploads are PAUSED to private** (PRIVACY default flipped in generate.yml, marked
with a PAUSED comment) until he approves script quality - flip the default back to
'public' once he does. Daily runs keep producing drafts privately in the meantime.

## WORKFLOW CHANGE (Nov 15, 11:45 PM, his explicit instruction)
"tell me the questions, I will provide you it's research and on that you write the video
script and generate the video." He rejected our auto-researched script. New contract:
1. The 30-day calendar now supplies QUESTIONS for him, one at a time via main.
2. He replies with his research. We write the script FROM HIS MATERIAL only, cautious
   wording where his text lacks direct evidence; flag gaps to him, don't silently swap
   in a different narrative.
3. Script goes to him for review. On approval, dispatch generate.yml with the `script`
   input (verbatim beats), upload PRIVATE, gate-check frames, report the private preview.
4. Public ONLY on his explicit go. The PRIVACY default stays 'private'.
Both cron schedules (generate 13:30 UTC + watchdog 13:50 UTC) are DISABLED in the
workflow files - nothing runs unattended anymore.
Current state: bird script v4 (docs/scripts/birds-firecrackers-v4.txt) written from his
research, render dispatched private. Next question for him when he's ready:
"How can the jellyfish Turritopsis dohrnii live forever?" (Nov 16 slot, line 21).

## PERMANENT STYLE RULE (Nov 15, his words, applies to EVERY video)
"No need to explain we are not teachers we explain the scientific part and end it with
a question for watcher making them make sure they answer or comment either sarcastic
something or something knowledgeable (make this a permanent rule for everything video)."
Every script: entertaining hook, accessible science (no lecture/teacher tone, no extended
caveat sermons - fold qualifications in naturally), and END WITH A POINTED VIEWER
QUESTION inviting jokes or debate. This supersedes takeaway-style endings, never factual
accuracy. Baked into plan_video.py's SCRIPT_PROMPT.
