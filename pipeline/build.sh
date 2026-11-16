#!/bin/bash
# build.sh SCRIPT.json VOICE OUTDIR MUSIC.mp3 HOOK OUT.mp4   (animation module chosen by ANIM env, default birds_anim.py)
set -e; P=$(cd "$(dirname "$0")"; pwd); S=$(realpath $1); V=$2; O=$3; M=$(realpath $4); H=$5; OUT=$(realpath -m $6); mkdir -p $O; cd $O
t0=$(date +%s)
python3 $P/tts_kokoro.py $S $V . ; t1=$(date +%s)
D=$(cat end.txt)
python3 $P/align_words.py narr.wav words.json
python3 $P/caps.py words.json $D "$H" cap.ass
python3 $P/${ANIM:-birds_anim.py} anim.mp4 ; t2=$(date +%s)
FO=$(python3 -c "print(max($D-3,0))")
ffmpeg -loglevel error -y -i narr.wav -i $M -filter_complex "[1:a]atrim=0:$D,asetpts=PTS-STARTPTS,afade=t=in:d=1.5,afade=t=out:st=$FO:d=3,volume=0.5[m];[0:a]asplit=2[n][k];[m][k]sidechaincompress=threshold=0.03:ratio=10:attack=15:release=500[d];[n][d]amix=inputs=2:normalize=0[a]" -map "[a]" -ar 44100 -b:a 192k mix.mp3
ffmpeg -loglevel error -y -i anim.mp4 -i mix.mp3 -vf "ass=cap.ass" -map 0:v -map 1:a -c:v libx264 -crf 26 -maxrate 2.5M -bufsize 5M -preset medium -pix_fmt yuv420p -c:a aac -b:a 160k -t $D -movflags +faststart $OUT
t3=$(date +%s); echo "TIMING tts=$((t1-t0))s anim=$((t2-t1))s encode=$((t3-t2))s total=$((t3-t0))s"
