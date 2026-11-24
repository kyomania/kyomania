#!/usr/bin/env bash
# Mixes the English ElevenLabs v4 voiceover + score onto the (upscaled, end-frozen) reel. No text overlays.
set -e
cd "$(dirname "$0")"
ffmpeg -y -i assets/reel.mp4 -i assets/score-fit.wav -i assets/vo1.mp3 -i assets/vo2.mp3 -filter_complex "\
[2]adelay=600|600,apad[v1];[3]adelay=8900|8900,apad[v2];\
[v1][v2]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5,asplit=2[vo][sc];\
[1]volume=0.55[mu];[mu][sc]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=400[duck];\
[duck][vo]amix=inputs=2:normalize=0,atrim=0:14.53,afade=t=out:st=14.1:d=0.43[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest cm-reel1.mp4
