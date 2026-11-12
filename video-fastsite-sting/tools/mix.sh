#!/bin/bash
# clean synthesized sting sound -> film/assets/audio/mix.wav (6.5 s)
cd "$(dirname "$0")/../film"
ev=( "swell 0.55 0.3" "sub 1.45 0.55" "pingG5 1.5 0.12" "swell 1.78 0.6" "sub 2.2 0.8" "tick 2.9 0.3" "final 3.05 0.55" "pingC6 3.55 0.12" )
in=(); f=""; smix=""; i=0
for e in "${ev[@]}"; do set -- $e; in+=(-i assets/sfx_clean/$1.wav); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$3,adelay=${ms}|${ms}[s$i];"; smix+="[s$i]"; i=$((i+1)); done
f+="${smix}amix=inputs=$i:normalize=0:duration=longest,apad=whole_dur=6.5,atrim=0:6.5,afade=t=out:st=5.6:d=0.9,loudnorm=I=-16:TP=-1.5,alimiter=limit=0.95[o]"
ffmpeg -v error -y "${in[@]}" -filter_complex "$f" -map "[o]" -ar 48000 -ac 2 assets/audio/mix.wav && echo mixed
