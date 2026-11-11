import subprocess, sys, wave, numpy as np
SR=48000; DUR=24.0; ROOT=sys.argv[1]; OUT=sys.argv[2]
def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",p,"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True).stdout,dtype="<f4").reshape(-1,2).astype(np.float64)
N=int(SR*DUR); mix=np.zeros((N,2))
def place(x,t,g):
    s=int(t*SR); e=min(N,s+len(x)); mix[s:e]+=x[:e-s]*g
m=load(f"{ROOT}/dl/music25.mp3")[:N]; t=np.arange(len(m))/SR
mix[:len(m)]+=m*0.75*np.clip((DUR-t)/0.3,0,1)[:,None]
S={n:load(f"{ROOT}/sfx/{n}.wav") for n in ["whoosh","whoosh_big","impact","impact_soft","pop","pour","sparkle","tick","riser"]}
T0,STEP,MIX,HERO,END=3.02,1.5,13.52,16.02,20.52
c=[(0.02,"riser",0.5),*[(0.02+k*0.125,"pop",0.35) for k in range(8)],(1.02,"impact",0.9),(1.02,"whoosh_big",0.5),(1.4,"sparkle",0.3),
   (2.7,"whoosh_big",0.6),(3.02,"impact_soft",0.5)]
fx=["pop","impact_soft","pour","pop","pop","tick","pour"]
for i in range(7):
    st=T0+i*STEP
    c+= [(st-0.08,"whoosh",0.5),(st+0.1,"impact_soft",0.3)]
    if fx[i]=="pop": c+=[(st+0.4+k*0.05,"pop",0.18) for k in range(6)]
    elif fx[i]=="tick": c+=[(st+0.15+k*0.1,"tick",0.15) for k in range(10)]
    elif fx[i]=="pour": c+=[(st+0.3,"pour",0.5)]
    else: c+=[(st+0.4,"whoosh_big",0.4)]
    c+=[(st+STEP-0.3,"whoosh",0.3)]
c+=[(MIX-0.05,"whoosh_big",0.5)]+[(MIX+0.45+i*0.22+0.05,"pop",0.3) for i in range(7)]+[(MIX+0.95,"pour",0.4),(MIX+1.85,"pour",0.4)]
c+=[(HERO-0.33,"whoosh_big",0.6),(HERO,"impact",0.85),(HERO+0.5,"sparkle",0.4),(HERO+2.02,"sparkle",0.3),
    (END-0.05,"whoosh_big",0.5),(END+0.35,"impact_soft",0.5),(END+1.0,"impact",0.6),(END+1.2,"sparkle",0.35)]
for tt,n,g in c: place(S[n],tt,g)
pk=np.abs(mix).max(); mix*=min(1,0.98/pk)
with wave.open(OUT+".raw.wav","wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg","-y","-v","error","-i",OUT+".raw.wav","-af","loudnorm=I=-14:TP=-1.0:LRA=9","-ar",str(SR),OUT],check=True)
print("mixed")
