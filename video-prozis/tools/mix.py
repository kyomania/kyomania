"""Cut VO into phrases, speed 1.15x, place on video timeline, add music + SFX, loudnorm."""
import subprocess, sys, wave, numpy as np
SR=48000; DUR=20.5; SPEED=1.15
ROOT=sys.argv[1]; OUT=sys.argv[2]
def load(path, filt=None):
    cmd=["ffmpeg","-v","error","-i",path]+(["-af",filt] if filt else [])+["-f","f32le","-ac","2","-ar",str(SR),"-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True,check=True).stdout,dtype="<f4").reshape(-1,2).astype(np.float64)
N=int(SR*DUR); mix=np.zeros((N,2)); voice=np.zeros((N,2))
def place(buf,x,t,g=1.0):
    s=int(t*SR); e=min(N,s+len(x))
    if s<N: buf[s:e]+=x[:e-s]*g
# (vo_start, vo_end, video_time)
PH=[(0.00,1.80,0.15),(2.10,4.22,1.80),(4.40,5.20,3.65),(5.52,7.10,4.40),(7.30,10.20,5.75),(10.40,12.54,8.30),
    (12.80,15.19,10.22),(15.55,16.44,12.25),(16.78,17.53,13.50),(17.70,19.55,14.30),(19.74,22.40,16.05),(22.72,24.79,18.42)]
for a,b,t in PH:
    seg=load(f"{ROOT}/dl/vo.mp3",f"atrim={a}:{b},asetpts=PTS-STARTPTS,atempo={SPEED},afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse")
    place(voice,seg,t)
    print(f"phrase {t:.2f}-{t+len(seg)/SR:.2f}")
env=np.abs(voice).mean(1); k=int(0.25*SR)
act=np.convolve((np.convolve(env,np.ones(int(0.03*SR))/int(0.03*SR),mode="same")>0.01).astype(float),np.ones(k)/k,mode="same").clip(0,1)
music=load(f"{ROOT}/dl/music.mp3")[:N]; t=np.arange(len(music))/SR
g=0.5*(1-0.5*act[:len(music)])*np.clip((DUR-0.05-t)/0.4,0,1)
mix[:len(music)]+=music*g[:,None]
mix+=voice*1.0
S={n:load(f"{ROOT}/sfx/{n}.wav") for n in ["whoosh","whoosh_big","impact","impact_soft","pop","pour","sparkle","tick"]}
cues=[(0.1,"sparkle",0.3),(0.55,"pop",0.3),(2.95,"impact",0.6),(3.4,"whoosh_big",0.5),
      (3.65,"whoosh",0.45),(4.05,"pop",0.35),(5.55,"whoosh_big",0.5),(5.85,"whoosh",0.4),
      *[(6.2+i*0.07,"pop",0.18) for i in range(10)],(8.1,"whoosh_big",0.5),(8.3,"whoosh",0.4),
      *[(8.6+i*0.13,"tick",0.12) for i in range(10)],(9.95,"whoosh_big",0.5),(10.2,"whoosh",0.4),(10.5,"pour",0.5),
      (12.05,"whoosh_big",0.5),(12.2,"impact_soft",0.4),(12.45,"pop",0.3),(12.65,"pop",0.3),(12.85,"pop",0.3),(13.05,"pour",0.45),
      (13.4,"whoosh_big",0.5),(13.55,"impact",0.7),(14.0,"sparkle",0.4),(15.85,"whoosh_big",0.45),
      (16.6,"impact_soft",0.4),(18.35,"impact",0.55),(18.6,"sparkle",0.35)]
for tt,n,gg in cues: place(mix,S[n],tt,gg)
pk=np.abs(mix).max()
if pk>0.98: mix*=0.98/pk
with wave.open(OUT+".raw.wav","wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg","-y","-v","error","-i",OUT+".raw.wav","-af","loudnorm=I=-14:TP=-1.0:LRA=9","-ar",str(SR),OUT],check=True)
print("mixed")
