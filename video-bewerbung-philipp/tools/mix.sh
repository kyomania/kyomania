#!/bin/bash
# score ducked under the German VO + clean accents -> film/assets/audio/mix.wav (64 s)
cd "$(dirname "$0")/../film"
D=64
vo=( "p1.mp3 0.8" "p2.mp3 9.8" "p3.mp3 12.3" "p4.mp3 25.3" "p5.mp3 28.0" "p6.mp3 39.8" "p7.mp3 45.8" "p8.mp3 55.0" "p9.mp3 60.4" )
ev=( "pingC5 1.0 0.05" "tick 3.7 0.2" "swell 3.5 0.12" "tick 9.6 0.2" "tick 12.2 0.2" "pingE5 12.6 0.04" "pingG5 15.2 0.04" "pingC6 22.8 0.05" "tick 25.2 0.2"
     "pingC5 28.05 0.06" "pingE5 31.15 0.06" "pingG5 34.45 0.06" "sub 38.3 0.5" "tick 39.6 0.2" "tick 42.4 0.2" "swell 52.2 0.14" "sub 58.85 0.6" "final 59.0 0.2" "pingC5 60.0 0.05" )
in=(-i assets/audio/music.mp3); f=""; vmix=""; smix=""; i=1
for e in "${vo[@]}"; do set -- $e; in+=(-i assets/vo/$1); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=${ms}|${ms}[v$i];"; vmix+="[v$i]"; i=$((i+1)); done
f+="${vmix}amix=inputs=${#vo[@]}:normalize=0,apad=whole_dur=$D,atrim=0:$D,loudnorm=I=-16:TP=-2:LRA=7,asplit=2[vo][sc];"
for e in "${ev[@]}"; do set -- $e; in+=(-i assets/sfx/$1.wav); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$3,adelay=${ms}|${ms}[s$i];"; smix+="[s$i]"; i=$((i+1)); done
f+="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.7,apad=whole_dur=$D,atrim=0:$D,afade=t=out:st=62.4:d=1.6[m0];"
f+="[m0][sc]sidechaincompress=threshold=0.035:ratio=4:attack=40:release=450,apad=whole_dur=$D[m];"
f+="[m][vo]${smix}amix=inputs=$((2+${#ev[@]})):normalize=0:duration=longest,apad=whole_dur=$D,atrim=0:$D,alimiter=limit=0.95[o]"
ffmpeg -v error -y "${in[@]}" -filter_complex "$f" -map "[o]" -ar 48000 -ac 2 assets/audio/mix.wav && echo mixed
