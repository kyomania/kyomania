import subprocess, sys, numpy as np, wave
SR=48000; OLD='/home/user/kyomania/video-fastsite'; A='/home/user/kyomania/video-fastsite-reel/audio'
def load(f):
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','2','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype='<f4').reshape(-1,2).astype(np.float64)
DUR=33.4; N=int(DUR*SR)
music=np.zeros((N,2)); vo=np.zeros((N,2)); fx=np.zeros((N,2))
def put(buf,x,t,g=1.0):
    i=int(t*SR); j=min(N,i+len(x)); buf[i:j]+=x[:j-i]*g
M=load(f'{OLD}/dl/music.mp3'); M=M/np.max(np.abs(M))
def ramp(n0,n1,a,b,arr):
    arr[n0:n1]*=np.linspace(a,b,n1-n0)[:,None]
segA=M[int(10.6*SR):int(10.6*SR)+int(15.8*SR)].copy(); ramp(int(15.0*SR),len(segA),1,0,segA); ramp(0,int(.05*SR),0,1,segA); put(music,segA,0)
segB=M[int(12.4*SR):int(12.4*SR)+int(15.4*SR)].copy(); ramp(len(segB)-int(1.2*SR),len(segB),1,0,segB); put(music,segB,18.0)
VOT=[.15,1.85,21.1,5.5,8.7,12.1,15.05,18.1,26.7,29.85]
for i,t in enumerate(VOT):
    x=load(f'{A}/vo/t{i}.wav'); x=x/np.max(np.abs(x)); put(vo,x,t)
# ducking envelope from VO
env=np.abs(vo).max(1); k=int(.12*SR); env=np.convolve(env,np.ones(k)/k,'same'); duck=1-.6*np.clip(env/.04,0,1)
S={k:load(f'{OLD}/sfx/{k}.wav') for k in ['tick','blip','whoosh','whoosh_big','impact','impact_soft','glitch']}
S['charge']=load(f'{A}/charge.mp3'); S['poweron']=load(f'{A}/poweron.mp3')
for k in S: S[k]=S[k]/np.max(np.abs(S[k]))
MK=[]; t=.28
while t<2.0-.2: MK.append(t); t+=.2
roll=[21.85+3.0*(1-(1-k/14)**2) for k in range(14)]
cues=[('tick',.62,.4),('tick',1.08,.35),('tick',1.38,.3),('whoosh',1.42,.45),
('impact',1.8,.6),('blip',2.0,.35),('whoosh',2.18,.4),('tick',2.66,.3),
('impact_soft',3.4,.4)]+[('blip',3.4+m,.22) for m in MK]+[
('impact_soft',5.4,.45)]+[('tick',5.45+i*.07,.3) for i in range(8)]+[('whoosh',6.3,.35),('whoosh',7.0,.4),('whoosh',7.12,.35),('glitch',7.85,.3),('whoosh_big',7.85,.45),
('impact_soft',8.6,.4)]+[('blip',9.0+i*.11,.2) for i in range(5)]+[('whoosh',11.66,.45),
('whoosh_big',12.0,.4),('whoosh',12.4,.3),('whoosh',12.8,.3),('whoosh',13.2,.25),
('charge',15.0,.85),('poweron',18.0,.9),('impact',18.0,.55),
('tick',18.33,.5),('blip',18.4,.4),('impact_soft',18.78,.45)]+[('blip',18.78+i*.05,.22) for i in range(4)]+[
('whoosh',21.0,.4)]+[('tick',x,.3) for x in roll]+[('impact_soft',24.75,.5),
]+[(['tick','blip'][i%2],26.6+i*2.6/6,.5) for i in range(6)]+[('whoosh',29.0,.35),
('whoosh_big',29.2,.45)]+[('tick',29.42+i*.035,.15) for i in range(11)]+[('impact',30.06,.55),('whoosh',30.1,.35),('impact_soft',30.4,.3)]
for k,t,g in cues: put(fx,S[k],t,g)
out=music*.5*duck[:,None]+vo*1.0+fx*.8
out=out/max(1,np.max(np.abs(out))/0.97)
with wave.open(sys.argv[1],'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype('<i2').tobytes())
print('ok')
