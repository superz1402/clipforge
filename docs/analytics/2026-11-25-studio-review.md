# WildWhyz Studio review, 25 November 2026

Source: 23 Studio screenshots sent on WhatsApp at 10:10-10:13 IST today, 28-day window unless noted. Numbers are a dated snapshot, not live counters. Studio warns that views and watch time now include TV co-views (from 16 Nov), so recent numbers may read slightly high.

Tools actually run from Jakeschincariol/youtube-agent-skill (cloned today): retention.py and hookscore.py. Verdicts below come from real runs.

## Channel state

- 4.3K views, 9.1 watch hours, +2 subscribers, 1.7K engaged views in 28 days. Monthly audience 1.7K, of which 99.9% are new viewers. Studio shows no subscriber watch-time report for these dates (not enough data to show one, not a measured zero).
- Stayed to watch 40.2%, swiped away 59.8%. Traffic: 96.2% Shorts feed, 3.2% search. Search terms bringing views: "kya lagao" 4.4%, "cow sounds loud" 1.5%, "crested gecko" 1.5%.
- Audience: India 35.2%, US 21.1%, UK 3.3%. Male 67.2%. Age 25-34 is 37.6%, 35-44 is 29.1%. Mobile 86.8%.
- Last 48 hours: 1,583 views. Crocodile 664, Giraffe 560, Elephant 215, Gecko 143, birds 1. The two newest question-first films carry the channel right now. Different ages, so an early signal, not proof.
- 28-day leaderboard: Elephant 1.3K, Gecko 899, birds 679, Crocodile 560, Flamingos 401. Watch hours: Elephant 2.9, Gecko 2.3, birds 1.3, Crocodile 0.9, Flamingos 0.7, Dolphins 0.4, Sharks 0.2.

## Retention, read with the skill's tool, plus a bug in it

Ran retention.py (yt-retention) on the Elephant curve (33-second film, average view duration 0:16, 47.2%). No timestamped Studio export was available, so the curve was digitized by eye from the retention screenshot; the point values are approximate, and the tool's cliff list on this input is an artifact of that coarse digitizing, so only the overall shape is used below.

Bug confirmed for Shorts: the tool's hook window is a fixed 30 seconds. On a 33-second Short that is 91% of the film, so it printed "HOOK LEAK 100.0% lost in the opening [severe]" and "SLIDE 0.000%". Both are artifacts of the window, not the film. For Shorts the opening window must be proportional (about the first 10%, roughly 3 seconds), and the real hook metric is the swipe decision, which happens before the retention curve starts and never appears in the export.

Corrected reading of the same curve:

- First ~3 seconds: about 7 points lost. Healthy; viewers who stay past the swipe mostly continue.
- No single cliff. A steady bleed of roughly 3 points per second from about 0:05 to the end.
- In yt-retention's own taxonomy this is a slide (pacing), not a hook leak inside the video. The bigger loss sits upstream: 57.2% of Elephant's viewers swiped away instead of staying. Studio's stayed-vs-swiped number covers the opening exposure and does not timestamp the swipe, so it cannot be pinned to a specific second; what is certain is that the swipe decision is not part of the retention export at all.

This matches the standing rule (hook first, plant a question in the first second). The swipe rate is the number to move.

## Titles, scored with hookscore.py

Published and scheduled WildWhyz titles, and the niche's viral winners from the Studio Trends tab, land in the same band:

- WildWhyz: Elephant 34, Crocodile 40, Giraffe 34, Whale 39, Murmuration 37, Hummingbird 45, Zebra 35, Butterfly 40. All read "WEAK".
- Niche winners: "Why The Ocean's Deadliest Predator Never Hunts You" 50, "Why You'd Never Want To Meet A Leopard Seal" 54, "Two Different Things Are Killing Sharks" 32, "Why Freshwater Is Scarier Than the Ocean" 35, "Why Sperm Whales Are The Most Bizarre Deep-Sea Creatures" 38, "Why Jaguars Are So Much More Dangerous Than Leopards" 37. Also "WEAK".

hookscore's own README says it separates deliberately bad hooks from real ones but cannot separate a creator's hits from misses. The runs agree: titles that pulled 2.6 to 24 lakh views score no better than ours. So the scheduled queue keeps its titles; retitling on this evidence would be churn, not improvement.

What the scores still say: our weakest property on every title is stakes and direct address. The winners talk to the viewer ("you") or set a comparison ("scarier than", "more dangerous than"). That goes into the next batch.

## What is winning in the niche (yt-viral reading of the Trends tab)

- Deep-sea and predator "why" films dominate: sperm whale (24 lakh), leopard seal (12.1 lakh), polar bear (7.6 lakh), freshwater vs ocean (4.6 lakh), false killer whale (4.3 lakh), orca (2.6 lakh). Depth Theory and OctoLab repeat.
- Frames that repeat: direct-address threat ("Never Hunts You", "You'd Never Want to Meet") and comparison ("Scarier Than", "More Dangerous Than", "Worse than Orca?").
- WildWhyz's own board agrees in miniature: a body-part misconception (Elephant) and a how-it-works-without-X (Gecko) lead.

## Decision: next batch, Nov 30 to Dec 6 (nothing is scheduled after Nov 29)

Topics pulled from the winning frames. Each goes through the research-first step before scripting; the claims inside these titles are candidates to verify, not facts to publish yet. Footage availability on Mixkit or NOAA also still needs the same check the original calendar had.

1. Nov 30, orca: "An Orca Can Kill a Great White. So Why Doesn't It Eat It?" (hookscore 39). Pulled forward from the old calendar's Dec 9 slot.
2. Dec 1, leopard seal: "Why You'd Survive a Shark Before a Leopard Seal" (59, the only WORKABLE score in the set).
3. Dec 2, sperm whale: "A Sperm Whale's Head Is One Third of Its Body. Why?" (40).
4. Dec 3, octopus: "This Octopus Has Three Hearts, and Two of Them Quit" (40). Old calendar's Dec 1 topic kept, reworded.
5. Dec 4, polar bear: "Why Polar Bears Are Nearly Invisible to Infrared" (36). Claim needs checking in research; drop if it does not hold.
6. Dec 5, mantis shrimp: "Why a Mantis Shrimp Punches Like a Bullet" (38 with harder wording; the honest claim is bullet-like acceleration, settle in research).
7. Dec 6, crows: "Why a Crow Will Remember Your Face for Years" (old calendar's Nov 17 topic, never filmed in this run).

Rhythm stays at one film a day, 7 PM IST. The audience is 99.9% new viewers with zero subscriber watch time, so the feed tests each film on its own; cadence is not the bottleneck, the swipe rate is. Two uploads a day stays parked.

## Working rules taken from the skill

These are decided rules for the next productions. Today they live only in this review; the durable home for them is the repo (docs/), which is blocked until the token below is refreshed.

- Retention: for Shorts, read the swipe rate and the first-3-seconds hold as the hook metric; run retention.py only with a proportional opening window. Its fixed 30-second window is wrong for this format.
- Hooks: keep writing five options per film and scoring them (yt-script), but treat hookscore as a floor check, not a ranking.
- Packaging: title and first frame are one unit (yt-package). The first frame shows the thing the title asks about; the title does not repeat the on-screen words.
- Audits: one fix at a time (yt-audit). The single biggest lever right now is the swipe rate, and its lever is the first frame plus first line. That is where production effort goes.

## What actually changed today, and what is only proposed

Implemented:

- This review was written to Drive (the folder that holds the 22 Nov audit).
- The next-batch decision (Nov 30 to Dec 6 above) and the working rules above are decided, under the creative-release authority delegated on 22 Nov.

Not changed, deliberately:

- No scheduled film was retitled or re-edited; the Nov 25-29 queue ships as scheduled.
- No repo code, workflow or calendar file was touched; the Actions schedule stays disabled.
- Upload rhythm stays one film a day at 7 PM IST.

## Landing

Committed to this repo on 25 Nov 2026 after the superz1402 token was refreshed. The same review lives in his Drive folder next to the 22 Nov audit (WildWhyz-studio-review-25-Nov-2026.md).
