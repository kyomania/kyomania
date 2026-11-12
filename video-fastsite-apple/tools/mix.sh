#!/bin/bash
# music + subtle SFX -> assets/audio/mix.wav
cd "$(dirname "$0")/../film"
ev=( "whoosh 3.95 0.16" "whoosh 9.9 0.14" "whoosh 15.35 0.16" "whoosh 20.7 0.13" "whoosh 23.85 0.13" "tick 6.85 0.35" "blip 7.25 0.18" "blip 17.45 0.2" "impact_soft 26.6 0.32" )
in=(-i assets/audio/music.mp3); f="[0:a]afade=t=out:st=28.6:d=1.4,volume=0.9[m];"; mixin="[m]"; i=1
for e in "${ev[@]}"; do set -- $e; in+=(-i assets/sfx/$1.wav); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$3,adelay=${ms}|${ms}[s$i];"; mixin+="[s$i]"; i=$((i+1)); done
f+="${mixin}amix=inputs=$i:normalize=0:duration=first,atrim=0:30,alimiter=limit=0.95[o]"
ffmpeg -v error -y "${in[@]}" -filter_complex "$f" -map "[o]" -ar 48000 -ac 2 assets/audio/mix.wav && echo mixed
