#!/bin/bash
# music2 (action score, entering at 4 s so its drop lands on the tablet section) ducked under VO + VO + clean SFX -> film/assets/audio/mix.wav (25.8 s)
cd "$(dirname "$0")/../film"
vo=( "b1.mp3 0.35" "b2.mp3 2.95" "b3.mp3 5.5" "b4.mp3 15.85" "v6.mp3 21.95" "v7.mp3 23.3" )
ev=( "sub 2.74 0.45" "pingC6 2.95 0.18" "pingC5 8.2 0.14" "pingE5 10.45 0.14" "pingG5 12.3 0.14" "pingC6 13.95 0.13"
     "sub 15.72 0.3" "tick 18.45 0.32" "swell 19.85 0.3" "sub 20.75 0.5" "pingG5 20.8 0.12" "swell 21.08 0.55" "sub 21.5 0.75" "tick 22.2 0.28" "final 22.35 0.5" )
in=(-ss 4 -i assets/audio/music2.mp3); f=""; vmix=""; smix=""; i=1
for e in "${vo[@]}"; do set -- $e; in+=(-i assets/vo/$1); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=${ms}|${ms}[v$i];"; vmix+="[v$i]"; i=$((i+1)); done
f+="${vmix}amix=inputs=${#vo[@]}:normalize=0,apad=whole_dur=25.8,atrim=0:25.8,treble=g=-2:f=7500,loudnorm=I=-16:TP=-2:LRA=7,asplit=2[vo][sc];"
for e in "${ev[@]}"; do set -- $e; in+=(-i assets/sfx_clean/$1.wav); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$3,adelay=${ms}|${ms}[s$i];"; smix+="[s$i]"; i=$((i+1)); done
f+="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:25.8,asetpts=PTS-STARTPTS,volume=0.55,afade=t=in:d=0.4,afade=t=out:st=24.6:d=1.2[m0];"
f+="[m0][sc]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=350,apad=whole_dur=25.8[m];"
f+="[m][vo]${smix}amix=inputs=$((2+${#ev[@]})):normalize=0:duration=longest,apad=whole_dur=25.8,atrim=0:25.8,alimiter=limit=0.95[o]"
ffmpeg -v error -y "${in[@]}" -filter_complex "$f" -map "[o]" -ar 48000 -ac 2 assets/audio/mix.wav && echo mixed
