#!/bin/bash
# music (ducked under VO) + VO + subtle SFX -> film/assets/audio/mix.wav
cd "$(dirname "$0")/../film"
vo=( "l1.mp3 0.55" "l2.mp3 2.25" "l3.mp3 5.3" "l4.mp3 7.75" "l5.mp3 10.7" "l6c.wav 15.6" "l7.mp3 19.33" "l8.mp3 21.35" "l9.mp3 24.0" "l10c.wav 26.6" )
ev=( "whoosh 3.95 0.12" "whoosh 9.9 0.1" "whoosh 15.35 0.12" "whoosh 20.7 0.1" "whoosh 23.85 0.1" "tick 6.85 0.3" "blip 7.25 0.15" "blip 17.45 0.16" "impact_soft 26.6 0.28" )
in=(-i assets/audio/music.mp3); f=""; vmix=""; smix=""; i=1
for e in "${vo[@]}"; do set -- $e; in+=(-i assets/vo/$1); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=${ms}|${ms}[v$i];"; vmix+="[v$i]"; i=$((i+1)); done
nv=${#vo[@]}
f+="${vmix}amix=inputs=$nv:normalize=0,apad=whole_dur=30,atrim=0:30,loudnorm=I=-16:TP=-2:LRA=7,asplit=2[vo][sc];"
for e in "${ev[@]}"; do set -- $e; in+=(-i assets/sfx/$1.wav); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$3,adelay=${ms}|${ms}[s$i];"; smix+="[s$i]"; i=$((i+1)); done
f+="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.55,afade=t=out:st=28.8:d=1.2[m0];"
f+="[m0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=450[m];"
f+="[m][vo]${smix}amix=inputs=$((2+${#ev[@]})):normalize=0:duration=first,atrim=0:30,alimiter=limit=0.95[o]"
ffmpeg -v error -y "${in[@]}" -filter_complex "$f" -map "[o]" -ar 48000 -ac 2 assets/audio/mix.wav && echo mixed
