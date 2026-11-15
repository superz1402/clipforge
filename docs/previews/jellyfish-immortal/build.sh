#!/bin/bash
# Rebuild corrected jellyfish preview. Needs: the 5 source mp4s (see SOURCES.md),
# audio.mp3 + subtitle.srt from run 43752363557 artifact, overlay.ass (this dir,
# already generated from subtitle.srt with hook + illustrative-footage label).
set -e
cut_c() { ffmpeg -loglevel error -ss $2 -t $3 -i $1.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -an -r 30 -c:v libx264 -preset ultrafast -crf 18 seg_$4.mp4 -y; }
cut_r() { ffmpeg -loglevel error -ss $2 -t $3 -i $1.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920:1700:0" -an -r 30 -c:v libx264 -preset ultrafast -crf 18 seg_$4.mp4 -y; }
cut_c redjelly 7.5 13.2 1
cut_c ex1502-jelly1 13.5 8.0 2
cut_c bigjelly 9.0 13.2 3
cut_r blooming-jelly 21.0 7.0 4
cut_c bigjelly 25.0 12.7 5
cut_c redjelly 7.6 12.9 6
cut_c bigjelly 40.0 13.4 7
cut_r blooming-jelly 21.05 6.95 8
cut_r redjelly 20.8 1.38 9
printf "file 'seg_%s.mp4'\n" 1 2 3 4 5 6 7 8 9 > list.txt
ffmpeg -loglevel error -f concat -safe 0 -i list.txt -i audio.mp3 -vf "ass=overlay.ass" -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -b:a 128k -shortest jellyfish-final.mp4 -y
ffprobe -v error -show_entries format=duration -of default=nw=1 jellyfish-final.mp4
