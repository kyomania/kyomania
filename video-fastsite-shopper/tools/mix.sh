#!/bin/bash
# music3 (launch score, entering at 4 s) ducked under VO + VO + clean SFX -> film/assets/audio/mix.wav  (25 s)
cd "$(dirname "$0")/../film"
vo=( "v1.mp3 0.35" "v2.mp3 2.55" "v3b.mp3 4.75" "v4c.wav 6.3" "v5.mp3 15.35" "v6.mp3 20.7" "v7.mp3 22.45" )
ev=( "pingC5 0.45 0.12" "pingE5 0.85 0.10" "swell 4.2 0.2" "sub 5.8 0.45"
     "pingC5 7.55 0.16" "pingE5 8.95 0.16" "pingG5 10.95 0.16" "pingC6 13.1 0.14" "pingG5 14.3 0.16"
     "tick 15.62 0.3" "tick 17.0 0.3" "sub 20.6 0.5" "final 22.2 0.35" )
in=(-ss 4 -i assets/audio/music3.mp3); f=""; vmix=""; smix=""; i=1
for e in "${vo[@]}"; do set -- $e; in+=(-i assets/vo/$1); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=${ms}|${ms}[v$i];"; vmix+="[v$i]"; i=$((i+1)); done
f+="${vmix}amix=inputs=${#vo[@]}:normalize=0,apad=whole_dur=25,atrim=0:25,treble=g=-2:f=7500,loudnorm=I=-16:TP=-2:LRA=7,asplit=2[vo][sc];"
for e in "${ev[@]}"; do set -- $e; in+=(-i assets/sfx_clean/$1.wav); ms=$(python3 -c "print(int($2*1000))")
  f+="[$i:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$3,adelay=${ms}|${ms}[s$i];"; smix+="[s$i]"; i=$((i+1)); done
f+="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:25,asetpts=PTS-STARTPTS,volume=0.6,afade=t=in:d=0.3,afade=t=out:st=24.0:d=1.0[m0];"
f+="[m0][sc]sidechaincompress=threshold=0.03:ratio=5:attack=30:release=350,apad=whole_dur=25[m];"
f+="[m][vo]${smix}amix=inputs=$((2+${#ev[@]})):normalize=0:duration=longest,apad=whole_dur=25,atrim=0:25,alimiter=limit=0.95[o]"
ffmpeg -v error -y "${in[@]}" -filter_complex "$f" -map "[o]" -ar 48000 -ac 2 assets/audio/mix.wav && echo mixed
