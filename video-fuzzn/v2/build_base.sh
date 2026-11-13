#!/usr/bin/env bash
# Baut den 60-s-Grundschnitt (hart geschnitten, ohne Ton) aus den 12 Kling-Clips.
# Aufruf: bash v2/build_base.sh   (aus video-fuzzn/)
set -euo pipefail
cd "$(dirname "$0")"
C=clips; S=work-seg; OUT=../film/assets/video
mkdir -p "$S" "$OUT"
rm -f "$S"/*.mp4 "$S"/list.txt
NORM="scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,format=yuv420p"
n=0
seg() { # clip src_start dur [speed] [rev]
  local clip=$1 ss=$2 dur=$3 speed=${4:-1} rev=${5:-}
  local srcdur; srcdur=$(python3 -c "print($dur*$speed)")
  local f="setpts=(PTS-STARTPTS)/$speed"
  [ -n "$rev" ] && f="reverse,$f"
  n=$((n+1)); local o; o=$(printf "%s/%02d.mp4" "$S" $n)
  ffmpeg -v error -y -ss "$ss" -t "$srcdur" -i "$C/$clip.mp4" -vf "$f,$NORM" -t "$dur" -an -c:v libx264 -crf 16 -preset fast "$o"
  echo "file '$(basename "$o")'" >> "$S/list.txt"
}
still() { # clip time dur
  local clip=$1 t=$2 dur=$3
  n=$((n+1)); local o; o=$(printf "%s/%02d.mp4" "$S" $n)
  ffmpeg -v error -y -ss "$t" -i "$C/$clip.mp4" -frames:v 1 "$S/still.png"
  ffmpeg -v error -y -loop 1 -i "$S/still.png" -vf "$NORM" -t "$dur" -an -c:v libx264 -crf 16 -preset fast "$o"
  echo "file '$(basename "$o")'" >> "$S/list.txt"
}
# --- Kiez 0.0-12.0
seg C01 0.0 3.2
seg C03 0.6 1.8
seg C02 0.8 2.6
seg C11 0.4 2.8
seg C12 0.5 1.6
# --- Hakiki 12.0-23.5
seg C04 0.3 4.0
seg C12 2.0 0.8
seg C05 0.0 2.0
still C05 2.0 0.8
seg C05 2.0 3.9 0.77
# --- Balkon 23.5-35.0
seg C06 0.0 3.5
seg C07 0.5 3.5
seg C06 0.8 4.5 0.6
# --- Zimmer 35.0-47.0
seg C08 0.0 4.0
seg C09 0.3 3.5
seg C08 2.5 4.5 0.55
# --- Dach 47.0-60.0
seg C10 0.0 5.0
seg C12 2.8 1.8
seg C10 1.0 5.4 0.74 rev
still C01 0.0 0.8
ffmpeg -v error -y -f concat -safe 0 -i "$S/list.txt" -c:v libx264 -crf 16 -preset fast -r 30 -an "$OUT/base.mp4"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/base.mp4"
# Standbilder der ausgehenden Frames für die Papier-Übergänge
mkdir -p ../film/assets/img/v2
for t in 12.0 23.5 35.0 47.0 59.2; do
  ffmpeg -v error -y -ss "$(python3 -c "print($t-0.04)")" -i "$OUT/base.mp4" -frames:v 1 -q:v 2 "../film/assets/img/v2/out_${t}.jpg"
done
# Papier-Risse aus den ausgehenden Frames (Richtung/Seed/Schräge je Übergang)
for spec in "12.0 v 3 120" "23.5 h 5 -90" "35.0 v 9 -150" "47.0 h 13 110" "59.2 v 21 60"; do
  set -- $spec
  python3 tear.py "../film/assets/img/v2/out_$1.jpg" "../film/assets/img/v2/tear_$1" "$2" "$3" "$4"
done
echo done
