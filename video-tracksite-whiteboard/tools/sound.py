"""Musik + SFX für das Track-Whiteboard (20 s), im Code erzeugt, deterministisch.
uv run --with numpy --with scipy python tools/sound.py board/assets/audio/mix.wav
Zeitpunkte = GSAP-Timeline in board/index.html.
"""
import sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000; DUR = 20.0; N = int(SR * DUR)
rng = np.random.default_rng(5)
L = np.zeros(N); R = np.zeros(N)

def put(x, t, g=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or i < 0: return
    n = min(len(x), N - i)
    L[i:i+n] += x[:n] * g * np.sqrt((1 - pan) / 2) * 1.414
    R[i:i+n] += x[:n] * g * np.sqrt((1 + pan) / 2) * 1.414

def filt(x, kind, f):
    return sosfilt(butter(2, f, kind, fs=SR, output="sos"), x)

def hz(n):  # MIDI -> Hz
    return 440 * 2 ** ((n - 69) / 12)

IR = None
def verb(x, mix=0.25):
    global IR
    if IR is None:
        n = int(SR * 1.6); t = np.arange(n) / SR
        IR = filt(rng.standard_normal(n), "low", 5000) * np.exp(-t * 4.5); IR /= np.sqrt(np.sum(IR ** 2))
    w = fftconvolve(x, IR)[:len(x) + int(SR * 1.6)]
    d = np.pad(x, (0, len(w) - len(x)))
    return d * (1 - mix) + w * mix

def marimba(f, d=0.6, g=1.0):
    n = int(SR * d); t = np.arange(n) / SR
    y = np.sin(2*np.pi*f*t) * np.exp(-t*7) + 0.35*np.sin(2*np.pi*f*4*t) * np.exp(-t*22) + 0.12*np.sin(2*np.pi*f*10*t)*np.exp(-t*60)
    return y * (1 - np.exp(-t / 0.002)) * g

def pluck_bass(f, d=0.45):
    n = int(SR * d); t = np.arange(n) / SR
    return (np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*2*f*t)) * np.exp(-t*6) * (1 - np.exp(-t / 0.004))

def pop(f=900, g=1.0):
    n = int(SR * 0.12); t = np.arange(n) / SR
    fr = f * (1 + 1.2 * np.exp(-t * 60))
    return np.sin(2*np.pi*np.cumsum(fr)/SR) * np.exp(-t * 38) * g

def click(g=1.0):
    n = int(SR * 0.03); t = np.arange(n) / SR
    return filt(rng.standard_normal(n), "high", 2500) * np.exp(-t * 300) * g

def thud(g=1.0):
    n = int(SR * 0.3); t = np.arange(n) / SR
    return (np.sin(2*np.pi*(90 + 60*np.exp(-t*30))*t) * np.exp(-t*18) + filt(rng.standard_normal(n), "low", 900)*np.exp(-t*40)*0.4) * g

def whoosh(d=0.6, g=1.0):
    n = int(SR * d); t = np.arange(n) / SR; u = t / d
    y = filt(rng.standard_normal(n), "band", [400, 3000]) * np.sin(np.pi * u) ** 2
    return y * g

def marker(d, g=1.0):
    n = int(SR * d); t = np.arange(n) / SR
    strokes = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * (5.5 + 1.5 * np.sin(t * 3)) * t))
    y = filt(rng.standard_normal(n), "band", [1800, 7000]) * strokes
    env = np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.05)
    return y * env * g

# ---- Musik: 112 BPM, C – G – Am – F, freundliche Marimba ----
bpm = 112; beat = 60 / bpm; bar = 4 * beat
chords = [(60, 64, 67), (55, 59, 62), (57, 60, 64), (53, 57, 60)]
mus = np.zeros(N)
t = 0.15; i = 0
while t < 18.1:
    c = chords[(i // 8) % 4]
    k = i % 8
    note = [c[0]+12, c[2]+12, c[1]+12, c[2]+12, c[0]+24, c[2]+12, c[1]+12, c[2]+12][k]
    seg = marimba(hz(note), 0.5, 0.20 if k % 2 else 0.26)
    j = int(t * SR); mus[j:j+len(seg)] += seg[:max(0, N-j)]
    if k % 4 == 0:
        b = pluck_bass(hz(c[0] - 24), 0.5) * 0.5; mus[j:j+len(b)] += b[:max(0, N-j)]
    if k % 2 == 1:  # Shaker
        sh = filt(rng.standard_normal(int(SR*0.06)), "high", 6000) * np.exp(-np.arange(int(SR*0.06))/SR*60) * 0.05
        mus[j:j+len(sh)] += sh[:max(0, N-j)]
    t += beat / 2; i += 1
# Schlussakkord zum Sticker
for n_, g_ in [(48, .3), (60, .25), (64, .22), (67, .22), (72, .18)]:
    put(verb(marimba(hz(n_), 1.8, g_), 0.35), 18.15, 1.0)
musv = verb(mus, 0.2)[:N]
put(musv, 0, 0.8)

# ---- SFX ----
for tt in [2.75, 5.4, 9.0, 11.6, 14.4]: put(whoosh(0.8, 0.10), tt, 1.0, 0.0)
put(whoosh(1.3, 0.12), 16.65)
for tt, d in [(1.25, .7), (1.95, .95), (3.95, .7), (4.25, .75), (4.85, .4), (5.6, .7), (10.85, .8), (11.5, .4), (12.35, .5), (13.05, .4), (13.6, .5), (15.0, .75)]:
    put(marker(d, 0.10), tt, 1.0, rng.uniform(-.4, .4))
pops = [(3.35, 820), (3.8, 1200), (9.3, 760), (9.65, 980), (10.4, 700), (12.05, 860), (12.75, 940), (13.3, 1020), (13.95, 1100), (14.7, 800), (15.45, 1250), (15.85, 900), (8.6, 1400)]
pops += [(5.95 + 0.1 * k, 600 + 80 * k) for k in range(3)] + [(6.2 + 0.07 * k, 900 + 60 * k) for k in range(6)]
for tt, f in pops: put(pop(f, 0.35), tt, 1.0, rng.uniform(-.3, .3))
for tt in [1.22, 7.45, 8.5, 18.12]: put(click(0.5), tt)
for tt in [2.95, 9.85, 15.6]: put(whoosh(0.45, 0.12), tt - 0.1); put(thud(0.35), tt + 0.35)
put(thud(0.5), 18.3); put(pop(1500, 0.3), 18.2)

mix = np.stack([L, R], 1)
t = np.arange(N) / SR
mix *= np.clip((DUR - t) / 1.2, 0, 1)[:, None] * np.clip(t / 0.15, 0, 1)[:, None]
mix = np.tanh(mix / (np.max(np.abs(mix)) + 1e-9) * 1.3) / np.tanh(1.3) * 0.85
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype("<i2").tobytes())
print("ok")
