import subprocess, wave, numpy as np
SR=48000; DUR=28.0; N=int(SR*DUR); mix=np.zeros((N,2)); voice=np.zeros((N,2))
def load(p): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",p,"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True).stdout,dtype="<f4").reshape(-1,2).astype(np.float64)
def place(b,x,t,g): s=int(t*SR); e=min(N,s+len(x)); b[s:e]+=x[:e-s]*g
for i,t in enumerate([0.6,7.4,14.4,22.6],1): place(voice,load(f"dl/vo{i}.mp3"),t,1.0)
env=np.abs(voice).mean(1); k=int(0.3*SR)
act=np.convolve((np.convolve(env,np.ones(1440)/1440,mode="same")>0.01).astype(float),np.ones(k)/k,mode="same").clip(0,1)
m=load("dl/music.mp3")[:N]; t=np.arange(len(m))/SR
mix[:len(m)]+=m*(0.6*(1-0.4*act[:len(m)])*np.clip((DUR-t)/0.5,0,1))[:,None]
mix+=voice
S={n:load(f"sfx/{n}.wav") for n in ["swell","chime","pop"]}
for tt,n,g in [(6.6,"swell",0.35),(13.6,"swell",0.35),(20.6,"swell",0.35),(0.2,"chime",0.25),(25.8,"chime",0.35),(12.0,"pop",0.2),(17.7,"pop",0.2)]: place(mix,S[n],tt,g)
mix*=min(1,0.98/np.abs(mix).max())
with wave.open("mix.raw.wav","wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg","-y","-v","error","-i","mix.raw.wav","-af","loudnorm=I=-14:TP=-1.0:LRA=9","-ar",str(SR),"brand-reel/assets/audio/mix.wav"],check=True)
print("mixed")
