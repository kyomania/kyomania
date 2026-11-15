import subprocess, sys, numpy as np, wave
SR=48000; ROOT='/home/user/kyomania/video-fastsite'
def load(f):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype='<f4').reshape(-1,2).astype(np.float64)
DUR=15.0; N=int(DUR*SR); out=np.zeros((N,2))
off=float(sys.argv[2]) if len(sys.argv)>2 else 0.0
m=load(f'{ROOT}/dl/music.mp3')[int(off*SR):int(off*SR)+N]
m=m/np.max(np.abs(m))*0.6
env=np.ones(len(m)); fi=int(.05*SR); env[:fi]=np.linspace(0,1,fi)
fo0=int(13.9*SR); env[fo0:]=np.linspace(1,0,len(m)-fo0)
out[:len(m)]+=m*env[:,None]
S={k:load(f'{ROOT}/sfx/{k}.wav') for k in ['tick','blip','whoosh','whoosh_big','impact','impact_soft','glitch','riser']}
def add(k,t,g):
    x=S[k]*g; i=int(t*SR); j=min(N,i+len(x)); out[i:j]+=x[:j-i]
cues=[('tick',.62,.5),('tick',1.08,.45),('tick',1.38,.4),('whoosh',1.42,.55),
('impact',1.8,.7),('blip',2.0,.45),('whoosh',2.18,.5),('tick',2.66,.4),('tick',2.85,.3),
('impact_soft',3.0,.45)]+[('blip',x,.35) for x in [3.36,3.6,3.84,4.08,4.3]]+[
('impact_soft',4.55,.5),('tick',5.01,.45),('whoosh',5.2,.45),('glitch',5.55,.4),('whoosh_big',5.55,.45),
('impact_soft',6.05,.45)]+[('blip',6.05+x,.25) for x in [.4,.5,.62,.75]]+[('whoosh',7.15,.55),
('whoosh_big',7.55,.45),('whoosh',7.85,.35),('whoosh',8.2,.3),
('tick',9.05,.4),('tick',9.39,.6),('blip',9.45,.45),('impact_soft',9.83,.5)]+[('blip',9.83+i*.05,.25) for i in range(4)]+[
(['tick','blip'][i%2],10.55+i*.25,.55) for i in range(6)]+[('whoosh',11.8,.4),
('whoosh_big',12.05,.5)]+[('tick',12.27+i*.035,.18) for i in range(11)]+[('impact',12.92,.65),('whoosh',12.95,.4),('blip',13.2,.35),('impact_soft',13.3,.35)]
for c in cues: add(*c)
out=out/max(1,np.max(np.abs(out))/0.97)
with wave.open(sys.argv[1],'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype('<i2').tobytes())
print('ok')
