# Completed real-footage-led preview
Final assets/final/camouflage-short-v1-real-am_michael.mp4. See CREDITS.md for full clip provenance,commercial-use licences,release credits,QA.

Runtime setup recovery:
- git clone currentmain; pip install --user -r pipeline/requirements.txt
- Download Kokoro model/voices to /downloads/kokoro as tts_kokoro.py requires.
- ANIM=camouflage_anim.py bash pipeline/build.sh pipeline/camouflage.script.json am_michael /downloads/camouflage assets/music/candidates/Morning.mp3 'HOW DO OCTOPUSES\NCHANGE COLOR?' /downloads/camouflage-prep.mp4
- Download exact two .ogv sources from media URLs preserved under docs/licenses/footage/ into /downloads/footage/octopus0.ogv and octopus1.ogv. Their API metadata includes source URLs.
- python pipeline/mix_camouflage_real.py writes /downloads/camouflage-real-am_michael.mp4.
- Inspect actual final pixels and narration,not just generation success.

Next preparation candidate: flamingo color from carotenoids, needs authoritative fact sources and independently verified real flamingo footage BEFORE production. No source or script has yet been verified for that next candidate. Real footage is the user's explicit preference; do not revert to all-animation output. No birds rebuild. Do not upload,retry,or re-enable gate without fresh usergo.
