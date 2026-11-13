#!/bin/bash
# calm score ducked under the German VO + a few soft tonal accents -> film/assets/audio/mix.wav (31 s)
cd "$(dirname "$0")/../film"
D=34.1
vo=( "a1.mp3 0.35" "a7.mp3 5.25" "a2.mp3 10.4" "a3.mp3 15.3" "a4.mp3 17.45" "a5.mp3 21.95" "a6f.mp3 27.7" )
ev=( "sub 3.8 0.35" "swell 8.4 0.18" "sub 8.75 0.45" "tick 10.35 0.12" "sub 21.7 0.5" "pingC5 24.4 0.07" "pingG5 24.45 0.05" "swell 27.1 0.12" )
in=(-ss 0.3 -i assets/audio/music3.mp3); f=""; vmix=""; smix=""; i=1
for e in "${vo[@]}"; do set -- $e; in+=(-i assets/vo/$1); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=${ms}|${ms}[v$i];"; vmix+="[v$i]"; i=$((i+1)); done
f+="${vmix}amix=inputs=${#vo[@]}:normalize=0,apad=whole_dur=$D,atrim=0:$D,loudnorm=I=-16:TP=-2:LRA=7,asplit=2[vo][sc];"
for e in "${ev[@]}"; do set -- $e; in+=(-i assets/sfx_clean/$1.wav); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$3,adelay=${ms}|${ms}[s$i];"; smix+="[s$i]"; i=$((i+1)); done
f+="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.85,apad=whole_dur=$D,atrim=0:$D,afade=t=out:st=32.5:d=1.6[m0];"
f+="[m0][sc]sidechaincompress=threshold=0.035:ratio=4:attack=40:release=500,apad=whole_dur=$D[m];"
f+="[m][vo]${smix}amix=inputs=$((2+${#ev[@]})):normalize=0:duration=longest,apad=whole_dur=$D,atrim=0:$D,alimiter=limit=0.95[o]"
ffmpeg -v error -y "${in[@]}" -filter_complex "$f" -map "[o]" -ar 48000 -ac 2 assets/audio/mix.wav && echo mixed
