#!/bin/bash
# Anfangsanimation: Karte -> KI-Satellitenflug -> Dorf mit Schriftzug. Aufruf: ./opener.sh <map-frames> <ki-clip> <out>
set -e
M=$1; K=$2; OUT=$3
SER=/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf
SERI=/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf
ffmpeg -y -v error -framerate 30 -i $M/%04d.png -i $K \
 -f lavfi -i "aevalsrc='0.22*sin(2*PI*55*t)*(0.6+0.4*sin(2*PI*0.25*t))+0.12*sin(2*PI*82.4*t)+0.08*sin(2*PI*110*t+sin(2*PI*0.5*t))':s=48000:d=13" \
 -filter_complex "
[0:v]trim=0:4.6,setpts=PTS-STARTPTS,fps=30,format=yuv420p,settb=1/30[m];
[1:v]scale=1920:1080,fps=30,eq=contrast=1.06:saturation=0.9,colorbalance=rh=0.04:bh=-0.03,vignette=PI/5,format=yuv420p,settb=1/30[k];
[m][k]xfade=transition=zoomin:duration=0.8:offset=3.8,
drawtext=fontfile=$SER:text='MACKENDORF':fontsize=110:fontcolor=0xB08D57:x=(w-tw)/2:y=h*0.70:alpha='min(max((t-8.6)/0.7,0),1)':shadowcolor=black@0.6:shadowx=0:shadowy=3,
drawtext=fontfile=$SERI:text='bei Wolfsburg':fontsize=56:fontcolor=0xE8DFD0:x=(w-tw)/2:y=h*0.70+130:alpha='min(max((t-9.0)/0.7,0),1)':shadowcolor=black@0.6:shadowx=0:shadowy=3,
fade=t=out:st=11.3:d=0.5[v];
[2:a]lowpass=f=600,afade=t=in:d=1.5,afade=t=out:st=10.8:d=1,volume=0.9[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -shortest $OUT
