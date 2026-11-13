#!/bin/bash
# calm score ducked under the German VO + a few soft tonal accents -> film/assets/audio/mix.wav (31 s)
cd "$(dirname "$0")/../film"
D=31
vo=( "a1.mp3 0.5" "a2.mp3 4.8" "a3.mp3 10.1" "a4.mp3 14.0" "a5.mp3 19.4" "a6.mp3 23.9" )
ev=( "pingC5 0.2 0.06" "pingG5 2.95 0.045" "swell 18.0 0.14" "pingE5 20.75 0.05" "pingC5 23.85 0.06" "pingG5 23.9 0.04" )
in=(-i assets/audio/music.mp3); f=""; vmix=""; smix=""; i=1
for e in "${vo[@]}"; do set -- $e; in+=(-i assets/vo/$1); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=${ms}|${ms}[v$i];"; vmix+="[v$i]"; i=$((i+1)); done
f+="${vmix}amix=inputs=${#vo[@]}:normalize=0,apad=whole_dur=$D,atrim=0:$D,loudnorm=I=-16:TP=-2:LRA=7,asplit=2[vo][sc];"
for e in "${ev[@]}"; do set -- $e; in+=(-i assets/sfx_clean/$1.wav); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$3,adelay=${ms}|${ms}[s$i];"; smix+="[s$i]"; i=$((i+1)); done
f+="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.7,apad=whole_dur=$D,atrim=0:$D,afade=t=out:st=29.4:d=1.6[m0];"
f+="[m0][sc]sidechaincompress=threshold=0.04:ratio=3:attack=40:release=500,apad=whole_dur=$D[m];"
f+="[m][vo]${smix}amix=inputs=$((2+${#ev[@]})):normalize=0:duration=longest,apad=whole_dur=$D,atrim=0:$D,alimiter=limit=0.95[o]"
ffmpeg -v error -y "${in[@]}" -filter_complex "$f" -map "[o]" -ar 48000 -ac 2 assets/audio/mix.wav && echo mixed
