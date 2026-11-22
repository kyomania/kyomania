#!/bin/bash
# Baut Reel 1 "So findest du uns" (16:9). Aufruf: ./build.sh <map-frames-dir> <endcard.png> <out.mp4>
set -e
M=$1; E=$2; OUT=$3; V=src/rundgang.mp4
G="eq=brightness=-0.05:contrast=1.12:saturation=0.8,colorbalance=rs=0.06:bs=-0.05:rm=0.04:bm=-0.03,vignette=PI/4.5"
clip(){ # start dur zoomfrom zoomto
  echo "[0:v]trim=start=$1:duration=$2,setpts=PTS-STARTPTS,scale=3840:-1,zoompan=z='$3+($4-$3)*on/($2*30)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=30,$G,format=yuv420p"
}
ffmpeg -y -v error -i $V -framerate 30 -i $M/%04d.png -loop 1 -t 3.6 -framerate 30 -i $E \
 -f lavfi -i "aevalsrc='0.22*sin(2*PI*55*t)*(0.6+0.4*sin(2*PI*0.25*t))+0.12*sin(2*PI*82.4*t)+0.08*sin(2*PI*110*t+sin(2*PI*0.5*t))':s=48000:d=17" \
 -filter_complex "
[1:v]format=yuv420p,fps=30,settb=1/30[m];
$(clip 7.9 2.4 1.0 1.18)[a];
$(clip 34.3 1.8 1.05 1.15)[b];
$(clip 37.2 1.7 1.12 1.02)[c];
$(clip 40.2 1.8 1.0 1.1)[d];
$(clip 47.0 1.8 1.1 1.2)[e];
[2:v]fps=30,format=yuv420p,fade=in:st=0:d=0.8[z];
[m]settb=1/30[m1];[a]settb=1/30[a1];[b]settb=1/30[b1];[c]settb=1/30[c1];[d]settb=1/30[d1];[e]settb=1/30[e1];[z]settb=1/30[z1];
[m1][a1]xfade=transition=zoomin:duration=0.7:offset=4.3[x1];
[x1][b1]xfade=transition=fadewhite:duration=0.6:offset=6.0[x2];
[x2][c1]xfade=transition=fade:duration=0.4:offset=7.4[x3];
[x3][d1]xfade=transition=slideleft:duration=0.4:offset=8.7[x4];
[x4][e1]xfade=transition=fade:duration=0.4:offset=10.1[x5];
[x5][z1]xfade=transition=fadeblack:duration=0.6:offset=11.3[vout];
[3:a]lowpass=f=600,afade=t=in:d=1.5,afade=t=out:st=13.4:d=1.5,volume=0.9[aout]" \
 -map "[vout]" -map "[aout]" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -shortest $OUT
