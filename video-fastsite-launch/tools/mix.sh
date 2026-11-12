#!/bin/bash
# music (ducked under VO) + VO + clean synthesized SFX (sfx_clean, tuned to C major) -> film/assets/audio/mix.wav
cd "$(dirname "$0")/../film"
vo=( "intro.mp3 0.5" "eng.mp3 3.5" "l1.mp3 6.5" "l2.mp3 8.2" "l5.mp3 10.1" "l6c.wav 14.55" "l7.mp3 19.15" "l8.mp3 21.15" "l10c.wav 26.4" )
ev=( "pingC5 1.35 0.16" "swell 2.98 0.22" "pingG5 5.25 0.14" "swell 5.98 0.22" "sub 9.8 0.55" "swell 13.95 0.2"
     "tick 16.6 0.22" "sub 19.06 0.6" "swell 19.85 0.18"
     "pingC5 23.4 0.24" "pingE5 24.0 0.24" "pingG5 24.6 0.24" "pingC6 25.2 0.22" "sub 23.4 0.3" "final 25.8 0.42" )
in=(-i assets/audio/music3.mp3); f=""; vmix=""; smix=""; i=1
for e in "${vo[@]}"; do set -- $e; in+=(-i assets/vo/$1); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=${ms}|${ms}[v$i];"; vmix+="[v$i]"; i=$((i+1)); done
f+="${vmix}amix=inputs=${#vo[@]}:normalize=0,apad=whole_dur=30,atrim=0:30,treble=g=-2:f=7500,loudnorm=I=-16:TP=-2:LRA=7,asplit=2[vo][sc];"
for e in "${ev[@]}"; do set -- $e; in+=(-i assets/sfx_clean/$1.wav); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$3,adelay=${ms}|${ms}[s$i];"; smix+="[s$i]"; i=$((i+1)); done
f+="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.6,afade=t=out:st=29.0:d=1.0[m0];"
f+="[m0][sc]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=350,apad=whole_dur=30[m];"
f+="[m][vo]${smix}amix=inputs=$((2+${#ev[@]})):normalize=0:duration=longest,apad=whole_dur=30,atrim=0:30,alimiter=limit=0.95[o]"
ffmpeg -v error -y "${in[@]}" -filter_complex "$f" -map "[o]" -ar 48000 -ac 2 assets/audio/mix.wav && echo mixed
