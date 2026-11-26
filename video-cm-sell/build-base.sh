#!/usr/bin/env bash
# 4:5 base cut: source segments + freeze frames (data stops). Original audio lowered, silent during freezes.
set -e
cd "$(dirname "$0")"
S=assets/source.mp4
# segment table: src_start src_end freeze_after
SEG=("0 7.6 8.8" "7.6 10.2 10.1" "10.2 14.0 5.5" "14.0 17.5 7.0" "17.5 20.04 0.6")
F=""; A=""; n=0
for s in "${SEG[@]}"; do set -- $s
  F+="[0:v]trim=$1:$2,setpts=PTS-STARTPTS,scale=1080:1440,crop=1080:1350:0:45,fps=30,tpad=stop_mode=clone:stop_duration=$3[v$n];"
  A+="[0:a]atrim=$1:$2,asetpts=PTS-STARTPTS,volume=0.45,apad=pad_dur=$3[a$n];"
  n=$((n+1)); done
C=""; for i in $(seq 0 $((n-1))); do C+="[v$i][a$i]"; done
ffmpeg -y -i "$S" -filter_complex "$F$A${C}concat=n=$n:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 15 -pix_fmt yuv420p -c:a aac -b:a 192k assets/base.mp4
