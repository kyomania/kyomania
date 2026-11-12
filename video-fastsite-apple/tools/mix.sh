#!/bin/bash
# music (ducked under VO) + VO + SFX -> film/assets/audio/mix.wav   (beat grid: 0.48 + n*0.60373 s)
cd "$(dirname "$0")/../film"
MUSIC=assets/audio/music2.mp3
vo=( "l1.mp3 0.55" "l2.mp3 2.95" "l3.mp3 5.35" "l4.mp3 7.3" "l5.mp3 10.3" "l6c.wav 14.6" "l7.mp3 19.3" "l8.mp3 21.25" "l9.mp3 23.6" "l10c.wav 26.6" )
ev=( "glass 2.5 0.35" "swoosh 5.15 0.4" "click 5.913 0.6" "click 6.42 0.35" "thud 9.536 0.75" "swoosh 10.05 0.35" "ticks 10.743 0.25" "glass 13.8 0.45"
     "swoosh 14.3 0.4" "glass 15.85 0.4" "ticks 17.2 0.25" "click 17.987 0.5" "thud 19.195 0.75" "swoosh 20.33 0.35" "ticks 20.5 0.2" "thud 22.817 0.75"
     "swoosh 23.35 0.35" "click 24.024 0.35" "click 24.628 0.35" "click 25.232 0.35" "glass 26.2 0.5" "hit 27.043 0.8" )
in=(-i $MUSIC); f=""; vmix=""; smix=""; i=1
for e in "${vo[@]}"; do set -- $e; in+=(-i assets/vo/$1); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=${ms}|${ms}[v$i];"; vmix+="[v$i]"; i=$((i+1)); done
f+="${vmix}amix=inputs=${#vo[@]}:normalize=0,apad=whole_dur=30,atrim=0:30,loudnorm=I=-16:TP=-2:LRA=7,asplit=2[vo][sc];"
for e in "${ev[@]}"; do set -- $e; in+=(-i assets/sfx2/$1.wav); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$3,adelay=${ms}|${ms}[s$i];"; smix+="[s$i]"; i=$((i+1)); done
f+="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.6,afade=t=out:st=28.9:d=1.1[m0];"
f+="[m0][sc]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=350,apad=whole_dur=30[m];"
f+="[m][vo]${smix}amix=inputs=$((2+${#ev[@]})):normalize=0:duration=longest,apad=whole_dur=30,atrim=0:30,alimiter=limit=0.95[o]"
ffmpeg -v error -y "${in[@]}" -filter_complex "$f" -map "[o]" -ar 48000 -ac 2 assets/audio/mix.wav && echo mixed
