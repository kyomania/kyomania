import subprocess, wave, numpy as np
SR=48000; DUR=20.8; N=int(SR*DUR); mix=np.zeros((N,2))
FS="/home/user/kyomania/video-fastsite"
def load(p,ss=None):
    cmd=["ffmpeg","-v","error"]+(["-ss",str(ss)] if ss is not None else [])+["-i",p,"-f","f32le","-ac","2","-ar",str(SR),"-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True,check=True).stdout,dtype="<f4").reshape(-1,2).astype(np.float64)
def place(b,x,t,g): s=int(t*SR); e=min(N,s+len(x)); b[s:e]+=x[:e-s]*g
# v2: keine Stimme – nur Musik + Sounddesign
m=load(f"{FS}/dl/music.mp3",ss=4.3)[:N]; t=np.arange(len(m))/SR
fade=np.clip(t/0.9,0,1)*np.clip((DUR-t)/0.8,0,1)
pre=np.where(t<12.9,0.8,1.0)
mix[:len(m)]+=m*(0.62*pre*fade)[:,None]
S={n:load(f"{FS}/sfx/{n}.wav") for n in ["impact","impact_soft","whoosh","whoosh_big","riser","glitch","tick","blip"]}
cuts=[9.52,9.92,10.32,10.72,11.12,11.52,11.92,12.12,12.32,12.52,12.72]
cues=[(0.1,"impact_soft",0.45),(3.25,"whoosh",0.45),(3.32,"impact",0.75),(6.45,"whoosh",0.45),(6.52,"impact",0.75),
      *[(c,"impact_soft" if c<11.9 else "tick",0.45) for c in cuts],(11.0,"riser",0.6),(9.52,"impact",0.6),
      (12.85,"whoosh_big",0.65),(12.95,"impact",1.0),(17.3,"impact_soft",0.55),(19.6,"blip",0.4)]
for tt,n,g in cues: place(mix,S[n],tt,g)
mix*=min(1,0.98/np.abs(mix).max())
with wave.open("mix.raw.wav","wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg","-y","-v","error","-i","mix.raw.wav","-af","loudnorm=I=-14:TP=-1.0:LRA=9","-ar",str(SR),"buch-spot/assets/audio/mix.wav"],check=True)
print("mixed")
