#!/bin/bash
# Makro-Frames (540x960, 24fps) -> 1080x1920 MP4, leicht gegradet
set -e; cd "$(dirname "$0")"
for s in "$@"; do
  ffmpeg -y -v error -framerate 24 -i frames_$s/f%04d.png -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,curves=all=${CURVE:-0/0 0.25/0.16 0.6/0.45 1/0.8},eq=contrast=1.08:saturation=1.05,format=yuv420p" \
    -c:v libx264 -crf 15 -preset slow -r 24 ../buch-spot/assets/video/$s.mp4
  echo "comp $s"
done
