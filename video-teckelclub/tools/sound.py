"""Weihnachtsmusik + Papier-SFX für die Teckelclub-Einladung (15 s), im Code erzeugt.
uv run --with numpy --with scipy python tools/sound.py film/assets/audio/mix.wav
"""
import sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
SR = 48000; DUR = 15.0; N = int(SR * DUR); rng = np.random.default_rng(12)
L = np.zeros(N); Rr = np.zeros(N)
def put(x, t, g=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or i < 0: return
    n = min(len(x), N - i); L[i:i+n] += x[:n]*g*np.sqrt((1-pan)/2)*1.414; Rr[i:i+n] += x[:n]*g*np.sqrt((1+pan)/2)*1.414
def flt(x, k, f): return sosfilt(butter(2, f, k, fs=SR, output="sos"), x)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
IR = None
def verb(x, mix=.3):
    global IR
    if IR is None:
        n = int(SR*2.2); t = np.arange(n)/SR; IR = flt(rng.standard_normal(n), "low", 6000)*np.exp(-t*3.2); IR /= np.sqrt(np.sum(IR**2))
    w = fftconvolve(x, IR)[:len(x)+int(SR*2.2)]; return np.pad(x,(0,len(w)-len(x)))*(1-mix)+w*mix
def celesta(f, d=1.2, g=1.):
    n=int(SR*d); t=np.arange(n)/SR
    return (np.sin(2*np.pi*f*t)*np.exp(-t*3.5)+.4*np.sin(2*np.pi*f*2*t)*np.exp(-t*6)+.15*np.sin(2*np.pi*f*5.4*t)*np.exp(-t*14))*(1-np.exp(-t/.002))*g
def pizz(f, d=.4):
    n=int(SR*d); t=np.arange(n)/SR; return (np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*2*f*t))*np.exp(-t*9)*(1-np.exp(-t/.003))
def bells(d=.12, g=1.):
    n=int(SR*d); t=np.arange(n)/SR
    y=sum(np.sin(2*np.pi*f*t+rng.uniform(0,6)) for f in (5200,6800,8100,9600))*np.exp(-t*35)
    return (y+flt(rng.standard_normal(n),"high",7000)*np.exp(-t*50)*.6)*g*.25
def rip(d=.75, g=1.):
    n=int(SR*d); t=np.arange(n)/SR; u=t/d
    crack=(rng.random(n)<(0.02+0.05*np.sin(np.pi*u)))*rng.standard_normal(n)
    y=flt(rng.standard_normal(n)*(0.4+0.6*np.abs(np.sin(t*90))), "band", [700,6000])*np.sin(np.pi*u)**.7 + flt(crack,"band",[1500,8000])*1.5
    return y*g
def slap(g=1.):
    n=int(SR*.18); t=np.arange(n)/SR
    return (flt(rng.standard_normal(n),"band",[300,3500])*np.exp(-t*45)+np.sin(2*np.pi*140*t)*np.exp(-t*30)*.5)*g
def squeak(g=1.):
    n=int(SR*.32); t=np.arange(n)/SR; f=900+700*np.sin(np.pi*t/.32)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*t/.32)**.6*g
def tap(g=1.):
    n=int(SR*.05); t=np.arange(n)/SR; return flt(rng.standard_normal(n),"band",[800,3000])*np.exp(-t*120)*g

# Musik: 120 BPM, C – Am – F – G, eigene Melodie
beat=.5; prog=[(48,(60,64,67)),(45,(57,60,64)),(41,(53,57,60)),(43,(55,59,62))]
mel=[76,79,81,79, 76,72,74,76, 77,76,74,72, 74,76,79,0, 76,79,81,84, 83,81,79,76, 77,81,79,77, 76,74,72,0]
mus=np.zeros(N)
for b in range(int(14.2/beat)):
    t=b*beat; bass,ch=prog[(b//4)%4]
    j=int(t*SR)
    def add(x):
        n=min(len(x),N-j)
        if n>0: mus[j:j+n]+=x[:n]
    add(pizz(hz(bass), .45)*.5 if b%2==0 else pizz(hz(ch[0]-12), .4)*.3)
    m=mel[b%len(mel)]
    if m and t>0.2: add(celesta(hz(m),1.0,.32))
    if b%2==1: add(sum(celesta(hz(c),.6,.07) for c in ch))
for k in range(int(14.2/(beat/2))):
    put(bells(.12, .55 if k%2 else .35), k*beat/2+.02, 1., .3)
put(verb(mus,.28), 0, .85)
for m,g in [(48,.4),(60,.3),(64,.28),(67,.28),(72,.25),(76,.2)]: put(verb(celesta(hz(m),3.,g),.4), 14.0)

# SFX
for c in (3.6,6.2,8.4,10.4,11.9): put(rip(.62,.24), c-.33, 1., rng.uniform(-.3,.3))
for t in [0.2,1.22,2.15,4.0,6.6,8.7,10.65]: put(slap(.24), t+.05, 1., rng.uniform(-.25,.25))
for i in range(6): put(tap(.22), .15+i*.17+.08, 1., .3)          # Dackel-Hüpfer
put(squeak(.14), 1.22); put(tap(.3), 1.62)
for i,t in enumerate([2.5,2.67,2.84,3.0]): put(tap(.15), t, 1., (-1)**i*.3)
put(verb(celesta(hz(88),1.6,.32),.5), 2.85, 1., .2); put(verb(celesta(hz(91),1.6,.24),.5), 2.92, 1., .2)
for i in range(7): put(verb(celesta(hz([72,74,76,79,81,84,86][i]),.8,.16),.4), 6.75+i*.13, 1., -.6+.2*i)   # Fenster gehen an
for i in range(6): put(tap(.25), 9.0+i*.25, 1., (-1)**i*.25); put(pop_ := tap(.12), 9.125+i*.25)    # Parade-Hüpfer
for t0,n,g in [(0.3,20,.05),(2.25,14,.05),(4.1,28,.04),(6.7,12,.05),(8.8,19,.04),(9.2,20,.04),(10.75,40,.03),(12.25,20,.04),(12.6,15,.05),(14.05,34,.03)]:
    for i in range(n): put(tap(g), t0+i*(0.03 if n<25 else 0.022)+.1, 1., rng.uniform(-.4,.4))   # Buchstaben
put(slap(.6), 13.35); put(verb(np.sin(2*np.pi*70*np.arange(int(SR*.4))/SR)*np.exp(-np.arange(int(SR*.4))/SR*12)*.6,.3), 13.35)  # Datums-Stempel
put(slap(.35), 13.77)
put(verb(bells(.3,1.5),.5), 12.2, 1.)

mix=np.stack([L,Rr],1); t=np.arange(N)/SR
mix*=np.clip((DUR-t)/.8,0,1)[:,None]*np.clip(t/.1,0,1)[:,None]
mix=np.tanh(mix/(np.max(np.abs(mix))+1e-9)*1.3)/np.tanh(1.3)*.85
with wave.open(sys.argv[1],"wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype("<i2").tobytes())
print("ok")
