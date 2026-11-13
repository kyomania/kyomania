#!/bin/bash
# music2 (action score, delayed 2 s so its drop lands on the T-rex burst) ducked under VO + VO + clean SFX -> film/assets/audio/mix.wav (28.2 s)
cd "$(dirname "$0")/../film"
D=28.2
vo=( "m1.mp3 0.4" "m2.mp3 4.5" "m3.mp3 10.6" "m4.mp3 13.4" "m5.mp3 18.9" "v6.mp3 24.6" "v7.mp3 25.7" )
ev=( "pingC5 0.3 0.12" "pingE5 0.7 0.1" "pingG5 1.1 0.1" "sub 4.25 0.55" "tick 4.75 0.3" "swell 7.9 0.25" "sub 10.45 0.8"
     "pingC5 13.4 0.13" "pingE5 14.8 0.13" "pingG5 16.38 0.13" "pingC6 17.6 0.12" "tick 19.4 0.3" "final 19.45 0.3"
     "swell 23.15 0.3" "sub 23.6 0.5" "swell 23.9 0.5" "sub 24.3 0.7" "tick 24.95 0.28" "final 25.1 0.45" )
in=(-i assets/audio/music2.mp3); f=""; vmix=""; smix=""; i=1
for e in "${vo[@]}"; do set -- $e; in+=(-i assets/vo/$1); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=${ms}|${ms}[v$i];"; vmix+="[v$i]"; i=$((i+1)); done
f+="${vmix}amix=inputs=${#vo[@]}:normalize=0,apad=whole_dur=$D,atrim=0:$D,treble=g=-2:f=7500,loudnorm=I=-16:TP=-2:LRA=7,asplit=2[vo][sc];"
for e in "${ev[@]}"; do set -- $e; in+=(-i assets/sfx_clean/$1.wav); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$3,adelay=${ms}|${ms}[s$i];"; smix+="[s$i]"; i=$((i+1)); done
f+="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.55,adelay=2000|2000,afade=t=in:st=2.0:d=0.6,apad=whole_dur=$D,atrim=0:$D,afade=t=out:st=26.8:d=1.4[m0];"
f+="[m0][sc]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=350,apad=whole_dur=$D[m];"
f+="[m][vo]${smix}amix=inputs=$((2+${#ev[@]})):normalize=0:duration=longest,apad=whole_dur=$D,atrim=0:$D,alimiter=limit=0.95[o]"
ffmpeg -v error -y "${in[@]}" -filter_complex "$f" -map "[o]" -ar 48000 -ac 2 assets/audio/mix.wav && echo mixed
