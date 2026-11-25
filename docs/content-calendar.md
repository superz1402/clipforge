# WildWhyz 30-day content calendar (Nov 16 - Dec 15, 2026)

Genre modeled on @hoodieguyofficial1 ("I make boring stories more fun") and
@unhingedwildlife ("the craziest stories of the animal kingdom"): weird-but-true
animal behavior, curiosity-question hook on screen, scientific payoff in ~6 beats.
We take IDEA INSPIRATION ONLY from those accounts - every short is scripted by our
local LLM, voiced by edge-TTS Brian, with Mixkit / NOAA public-domain footage.

Every topic below is footage-verified: the subject animal exists on Mixkit
(checked 2026-11-15) or in the NOAA Ocean Exploration archive fallback.

Daily upload 7:00 PM IST (13:30 UTC cron). The pipeline picks by
day-of-year rotation over topics.txt; the mapping below is exact.

| Day | Date | Topic (drives script + title) | On-screen hook angle |
| --- | --- | --- | --- |
| 1 | Nov 16 | The jellyfish that never dies | "This animal is immortal?" |
| 2 | Nov 17 | Why crows hold grudges for years | "Wrong a crow once?" |
| 3 | Nov 18 | Why sharks are older than trees | "Sharks predate TREES?" |
| 4 | Nov 19 | Why dolphins sleep with one eye open | "Half a brain stays awake?" |
| 5 | Nov 20 | How some turtles breathe through their butts | "Breathing... backwards?" |
| 6 | Nov 21 | Why bees dance to give directions | "A dance with an address?" |
| 7 | Nov 22 | Why flamingos are pink | "Born grey - so why pink?" |
| 8 | Nov 23 | Why owls can rotate their heads | "270 degrees. How?" |
| 9 | Nov 24 | Why cats bring you dead gifts | "Your cat's creepy present?" |
| 10 | Nov 25 | Why dogs tilt their heads | "That head tilt means what?" |
| 11 | Nov 26 | Why male seahorses get pregnant | "The dad gives birth?" |
| 12 | Nov 27 | Why zebras have stripes | "Stripes confuse WHAT?" |
| 13 | Nov 28 | How elephants hear through their feet | "Ears in their FEET?" |
| 14 | Nov 29 | Why penguins propose with pebbles | "A pebble engagement ring?" |
| 15 | Nov 30 | Why octopuses have three hearts | "Three hearts, blue blood?" |
| 16 | Dec 1 | How frogs freeze solid and survive winter | "Frozen solid. Still alive?" |
| 17 | Dec 2 | Why bats sleep upside down | "Why don't they fall?" |
| 18 | Dec 3 | Why parrots copy human speech | "Mocking you - or learning?" |
| 19 | Dec 4 | Why crabs walk sideways | "Evolution's odd choice?" |
| 20 | Dec 5 | Why snakes smell with their tongues | "Tongue = nose?" |
| 21 | Dec 6 | Why spiders don't stick to their own webs | "Their web, their rules?" |
| 22 | Dec 7 | How butterflies taste with their feet | "Tasting with feet?" |
| 23 | Dec 8 | Why horses sleep standing up | "Never lying down?" |
| 24 | Dec 9 | How orcas hunt great white sharks | "What eats a great white?" |
| 25 | Dec 10 | Why cats knead with their paws | "Making biscuits - why?" |
| 26 | Dec 11 | How bees make honey | "Honey is bee WHAT?" |
| 27 | Dec 12 | Why penguins fly underwater instead of the sky | "Birds that fly underwater?" |
| 28 | Dec 13 | How jellyfish can sink fishing boats | "Jellyfish sank a BOAT?" |
| 29 | Dec 14 | Why some sharks never stop swimming | "Sleep-swimming sharks?" |
| 30 | Dec 15 | Why elephants never forget | "Memory that lasts decades?" |

Day 0 (Nov 15) was his own pitch, uploaded manually: "Why birds fly away when
firecrackers burst".

After Dec 15 the rotation repeats; refresh this file with the next 30 ideas
before then (seasonal hooks: winter/Christmas animals mid-December).

## Actual releases and next batch (updated 25 Nov 2026)

The rotation table above is the original plan. Actual releases diverged from
22 Nov: custom question-first films shipped instead (Elephant 22 Nov,
Crocodile 23, Giraffe 24, Whale 25, Murmuration 26, Hummingbird 27, Zebra 28,
Butterfly 29, all 7 PM IST). Nothing is scheduled after 29 Nov.

Next batch, decided 25 Nov from the Studio review
(docs/analytics/2026-11-25-studio-review.md). Each claim still goes through
the research-first step, and footage through the Mixkit/NOAA availability
check, before scripting.

| Date | Topic | Working title |
| --- | --- | --- |
| Nov 30 | Orca vs great white | "An Orca Can Kill a Great White. So Why Doesn't It Eat It?" |
| Dec 1 | Leopard seal | "Why You'd Survive a Shark Before a Leopard Seal" |
| Dec 2 | Sperm whale | "A Sperm Whale's Head Is One Third of Its Body. Why?" |
| Dec 3 | Octopus | "This Octopus Has Three Hearts, and Two of Them Quit" |
| Dec 4 | Polar bear | "Why Polar Bears Are Nearly Invisible to Infrared" (verify claim first) |
| Dec 5 | Mantis shrimp | "Why a Mantis Shrimp Punches Like a Bullet" (verify wording in research) |
| Dec 6 | Crows | "Why a Crow Will Remember Your Face for Years" |

Rhythm stays one film a day at 7 PM IST.

## Working rules (from the 25 Nov review, via Jakeschincariol/youtube-agent-skill)

- Shorts hook metric: the stayed-vs-swiped rate and the first-3-seconds hold.
  Run retention.py only with a proportional opening window (~10% of the film);
  its fixed 30-second window is wrong for Shorts.
- hookscore.py is a floor check, not a ranking; it cannot tell a hit from a
  miss, and the niche's viral titles score in the same band as ours.
- Title and first frame are one unit: the first frame shows the thing the
  title asks about, and the title does not repeat the on-screen words.
- One fix per audit. The current lever is the swipe rate, worked through the
  first frame plus the first line.
