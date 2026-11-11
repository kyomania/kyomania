import subprocess, wave, numpy as np, re
SR=48000; DUR=25.0; N=int(SR*DUR); mix=np.zeros((N,2))
def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",p,"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True).stdout,dtype="<f4").reshape(-1,2).astype(np.float64)
def place(buf,x,t,g):
    s=int(t*SR); e=min(N,s+len(x)); buf[s:e]+=x[:e-s]*g
voice=np.zeros((N,2))
for i,t in enumerate([0.35,3.15,5.65,10.05,14.85,20.05],1): place(voice,load(f"dl/vo{i}.mp3"),t,1.0)
env=np.abs(voice).mean(1); k=int(0.25*SR)
act=np.convolve((np.convolve(env,np.ones(1440)/1440,mode="same")>0.01).astype(float),np.ones(k)/k,mode="same").clip(0,1)
m=load("dl/music.mp3")[:N]; t=np.arange(len(m))/SR
mix[:len(m)]+=m*(0.55*(1-0.5*act[:len(m)])*np.clip((DUR-t)/0.8,0,1))[:,None]
mix+=voice
S={n:load(f"sfx/{n}.wav") for n in ["rip","tape","swish","click","thump"]}
html=open("scrapbook-reel/index.html").read()
cues=[]
for t,fx in re.findall(r'data-t="([\d.]+)" data-fx="(\w+)"',html):
    t=float(t)
    if fx=="tape": cues.append((t,"tape",0.5))
    elif fx in("slam","stamp"): cues.append((t,"thump",0.55))
    elif fx in("drop","left","right","up"): cues.append((t,"swish",0.35))
    elif fx in("stick","pop"): cues.append((t,"tape",0.35))
    elif fx=="type": cues+= [(t+i*0.125,"click",0.25) for i in range(5)]
for t in [3.05,5.5,9.85,14.6,19.8]: cues.append((t-0.02,"rip",0.6))
for tt,n,g in cues: place(mix,S[n],tt,g)
mix*=min(1,0.98/np.abs(mix).max())
with wave.open("mix.raw.wav","wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg","-y","-v","error","-i","mix.raw.wav","-af","loudnorm=I=-14:TP=-1.0:LRA=9","-ar",str(SR),"scrapbook-reel/assets/audio/mix.wav"],check=True)
print("mixed", len(cues), "cues")
