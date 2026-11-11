import subprocess, wave, numpy as np
SR=48000; DUR=20.8; N=int(SR*DUR); mix=np.zeros((N,2)); voice=np.zeros((N,2))
FS="/home/user/kyomania/video-fastsite"
def load(p,ss=None):
    cmd=["ffmpeg","-v","error"]+(["-ss",str(ss)] if ss is not None else [])+["-i",p,"-f","f32le","-ac","2","-ar",str(SR),"-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True,check=True).stdout,dtype="<f4").reshape(-1,2).astype(np.float64)
def place(b,x,t,g): s=int(t*SR); e=min(N,s+len(x)); b[s:e]+=x[:e-s]*g
for i,t in enumerate([0.35,2.0,5.0,9.7,13.6,17.3],1): place(voice,load(f"dl/vo{i}.mp3"),t,1.15)
env=np.abs(voice).mean(1); k=int(0.25*SR)
act=np.convolve((np.convolve(env,np.ones(1440)/1440,mode="same")>0.01).astype(float),np.ones(k)/k,mode="same").clip(0,1)
m=load(f"{FS}/dl/music.mp3",ss=4.3)[:N]; t=np.arange(len(m))/SR
pre=np.where(t<12.9,0.75,1.0)   # vor dem Drop etwas zurückhaltender
mix[:len(m)]+=m*(0.5*pre*(1-0.45*act[:len(m)])*np.clip((DUR-t)/0.6,0,1))[:,None]
mix+=voice
S={n:load(f"{FS}/sfx/{n}.wav") for n in ["impact","impact_soft","whoosh","whoosh_big","riser","glitch","tick","blip"]}
cues=[(0.25,"impact_soft",0.5),(0.6,"impact_soft",0.5),(1.0,"impact",0.7),(1.88,"glitch",0.5),
      *[(2.05+i*0.5,"tick",0.35) for i in range(6)],(3.0,"whoosh",0.4),(4.93,"impact",0.6),(5.4,"whoosh_big",0.4),
      (6.9,"glitch",0.35),(7.9,"blip",0.4),(8.0,"whoosh",0.35),(8.8,"impact",0.7),(9.68,"glitch",0.5),(9.75,"impact_soft",0.5),
      (11.5,"impact_soft",0.5),(11.75,"impact",0.6),(11.4,"riser",0.55),(12.55,"impact_soft",0.5),(12.95,"impact",1.0),(12.9,"whoosh_big",0.6),
      (15.5,"impact_soft",0.5),(17.3,"impact",0.7),(19.4,"whoosh",0.4)]
for tt,n,g in cues: place(mix,S[n],tt,g)
mix*=min(1,0.98/np.abs(mix).max())
with wave.open("mix.raw.wav","wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg","-y","-v","error","-i","mix.raw.wav","-af","loudnorm=I=-14:TP=-1.0:LRA=9","-ar",str(SR),"buch-spot/assets/audio/mix.wav"],check=True)
print("mixed")
