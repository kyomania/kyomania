#!/bin/bash
# warm acoustic score ducked under German VO + soft paper/pop accents -> film/assets/audio/mix.wav (30 s)
cd "$(dirname "$0")/../film"
D=30
vo=( "h1.mp3 4.4" "h2.mp3 7.8" "h3.mp3 11.3" "h4.mp3 14.5" "h5.mp3 18.0" "h6.mp3 22.0" "h7.mp3 25.6" )
ev=( "pingC5 0.45 0.05" "pingE5 0.63 0.05" "pingG5 0.81 0.05" "tick 4.0 0.18" "pingE5 4.6 0.06" "tick 7.2 0.18" "pingC5 8.75 0.05" "tick 10.8 0.18" "tick 14.1 0.18" "pingG5 14.7 0.04" "tick 17.5 0.18" "tick 21.6 0.18" "pingC6 23.4 0.04" "tick 25.1 0.18" "swell 25.3 0.12" "final 25.6 0.18" )
in=(-i assets/audio/music.mp3); f=""; vmix=""; smix=""; i=1
for e in "${vo[@]}"; do set -- $e; in+=(-i assets/vo/$1); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=${ms}|${ms}[v$i];"; vmix+="[v$i]"; i=$((i+1)); done
f+="${vmix}amix=inputs=${#vo[@]}:normalize=0,apad=whole_dur=$D,atrim=0:$D,loudnorm=I=-15:TP=-2:LRA=7,asplit=2[vo][sc];"
for e in "${ev[@]}"; do set -- $e; in+=(-i assets/sfx/$1.wav); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$3,adelay=${ms}|${ms}[s$i];"; smix+="[s$i]"; i=$((i+1)); done
f+="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.75,apad=whole_dur=$D,atrim=0:$D,afade=t=out:st=28.4:d=1.6[m0];"
f+="[m0][sc]sidechaincompress=threshold=0.035:ratio=4:attack=40:release=450,apad=whole_dur=$D[m];"
f+="[m][vo]${smix}amix=inputs=$((2+${#ev[@]})):normalize=0:duration=longest,apad=whole_dur=$D,atrim=0:$D,alimiter=limit=0.95[o]"
ffmpeg -v error -y "${in[@]}" -filter_complex "$f" -map "[o]" -ar 48000 -ac 2 assets/audio/mix.wav && echo mixed
