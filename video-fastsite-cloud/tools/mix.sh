#!/bin/bash
# music3 (launch score, delayed 1.2 s: near-silence on the fall, drop on the rocket) ducked under VO + VO + clean SFX -> film/assets/audio/mix.wav (31.1 s)
cd "$(dirname "$0")/../film"
D=31.1
vo=( "c1.mp3 0.5" "c2.mp3 4.5" "c3.mp3 8.6" "c4.mp3 11.6" "c5.mp3 21.2" "v6.mp3 27.55" "v7.mp3 28.6" )
ev=( "pingC5 0.6 0.12" "swell 7.8 0.3" "sub 11.0 0.6" "pingC5 13.95 0.14" "pingE5 16.1 0.14" "pingG5 17.95 0.14" "pingC6 19.35 0.13"
     "tick 22.0 0.25" "tick 22.55 0.25" "tick 23.1 0.25" "swell 25.75 0.3" "sub 26.2 0.5" "swell 26.5 0.5" "sub 26.9 0.7" "tick 27.6 0.28" "final 27.75 0.45" )
in=(-i assets/audio/music3.mp3); f=""; vmix=""; smix=""; i=1
for e in "${vo[@]}"; do set -- $e; in+=(-i assets/vo/$1); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=${ms}|${ms}[v$i];"; vmix+="[v$i]"; i=$((i+1)); done
f+="${vmix}amix=inputs=${#vo[@]}:normalize=0,apad=whole_dur=$D,atrim=0:$D,treble=g=-2:f=7500,loudnorm=I=-16:TP=-2:LRA=7,asplit=2[vo][sc];"
for e in "${ev[@]}"; do set -- $e; in+=(-i assets/sfx_clean/$1.wav); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$3,adelay=${ms}|${ms}[s$i];"; smix+="[s$i]"; i=$((i+1)); done
f+="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.55,adelay=1200|1200,afade=t=in:st=1.2:d=0.3,apad=whole_dur=$D,atrim=0:$D,afade=t=out:st=29.8:d=1.3[m0];"
f+="[m0][sc]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=350,apad=whole_dur=$D[m];"
f+="[m][vo]${smix}amix=inputs=$((2+${#ev[@]})):normalize=0:duration=longest,apad=whole_dur=$D,atrim=0:$D,alimiter=limit=0.95[o]"
ffmpeg -v error -y "${in[@]}" -filter_complex "$f" -map "[o]" -ar 48000 -ac 2 assets/audio/mix.wav && echo mixed
