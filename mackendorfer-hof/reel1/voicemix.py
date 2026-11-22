"""Schneidet die Sprachdatei an Pausen in 8 Phrasen und legt sie an feste Bildzeitpunkte; Musik wird unter der Stimme abgesenkt."""
import re, subprocess, sys
voice, video, out = sys.argv[1:4]
TARGETS = [0.3, 2.5, 5.2, 6.7, 8.8, 13.0, 14.3, 18.0]
dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",voice]))
log = subprocess.run(["ffmpeg","-i",voice,"-af","silencedetect=n=-40dB:d=0.25","-f","null","-"],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",log)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",log)]
sil=list(zip(st,en))
speech=[]; cur=0.0
for s,e in sil:
    if s-cur>0.05: speech.append([cur,s])
    cur=e
if dur-cur>0.05: speech.append([cur,dur])
while len(speech)>8:  # kleinste Luecke zusammenfassen
    gaps=[speech[i+1][0]-speech[i][1] for i in range(len(speech)-1)]
    i=gaps.index(min(gaps)); speech[i][1]=speech[i+1][1]; del speech[i+1]
assert len(speech)==8, speech
parts=[]; labels=[]
for k,((a,b),t) in enumerate(zip(speech,TARGETS)):
    a=max(0,a-0.05); b=b+0.15
    parts.append(f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b-a-0.08}:d=0.08,adelay={int(t*1000)}|{int(t*1000)}[v{k}]")
    labels.append(f"[v{k}]")
fc=";".join(parts)+f";{''.join(labels)}amix=inputs=8:normalize=0,volume=1.6,highpass=f=80,acompressor=threshold=-18dB:ratio=3,apad=whole_dur=20.06[vo];[vo]asplit[vo1][vo2];[0:a]volume=0.85[mu];[mu][vo1]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[duck];[duck][vo2]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]"
subprocess.check_call(["ffmpeg","-y","-v","error","-i",video,"-i",voice,"-filter_complex",fc,"-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-shortest",out])
print(out, [(round(a,2),round(b,2)) for a,b in speech])
