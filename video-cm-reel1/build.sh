#!/usr/bin/env bash
# Original video + original audio (lowered, ducked) + English ElevenLabs v4 VO. Video stream copied untouched, length unchanged.
set -e
cd "$(dirname "$0")"
SRC="${1:-assets/original.mp4}"
ffmpeg -y -i "$SRC" -i assets/vo1.mp3 -i assets/vo2.mp3 -filter_complex "\
[1]adelay=600|600,apad[v1];[2]atempo=1.08,adelay=7000|7000,apad[v2];\
[v1][v2]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5,asplit=2[vo][sc];\
[0:a]volume=0.5[mu];[mu][sc]sidechaincompress=threshold=0.04:ratio=5:attack=20:release=400[duck];\
[duck][vo]amix=inputs=2:normalize=0,atrim=0:12.05[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t 12.05 cm-reel1.mp4
