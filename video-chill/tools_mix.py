"""Ton für den Chill-Reel: Chaos-Bus mit Tape-Stop, Lo-Fi-Beat (80 BPM, synthetisch), SFX-Cues."""
import subprocess, wave, numpy as np
from scipy.signal import lfilter, butter
SR = 48000; DUR = 12.5; N = int(SR * DUR); FREEZE = 2.4; BEAT = 0.75
rng = np.random.default_rng(11)
def load(p): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",p,"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True).stdout,dtype="<f4").reshape(-1,2).astype(np.float64)
def place(b, x, t, g):
    s = int(t * SR); e = min(len(b), s + len(x))
    if s < len(b): b[s:e] += x[:e - s] * g
def st(x): return np.stack([x, x], 1)
def lp(x, fc, o=2): b, a = butter(o, fc / (SR / 2)); return lfilter(b, a, x, axis=0)
def hp(x, fc, o=2): b, a = butter(o, fc / (SR / 2), "high"); return lfilter(b, a, x, axis=0)
def repitch(x, r): idx = np.arange(0, len(x) - 1, r); return np.stack([np.interp(idx, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1)
S = {n: load(f"sfx/{n}.wav") for n in ["blip","riser","whoosh","whoosh_big","impact_soft","glitch","chime","pop","tap","air_hit","swell"]}

# ---------- Chaos-Bus ----------
chaos = np.zeros((int(SR * (FREEZE + 0.2)), 2))
cardT = [0.08 + 2.15 * np.sqrt(i / 18) for i in range(18)]
for i, t in enumerate(cardT): place(chaos, repitch(S["blip"], 0.8 + 0.06 * i), t, 0.55)
for i, t in enumerate(cardT): place(chaos, S["pop"], t + 0.01, 0.25)
place(chaos, S["riser"], FREEZE - 1.4, 0.55)
tt = np.arange(len(chaos)) / SR
buzz = np.sign(np.sin(2 * np.pi * 150 * tt)) * (np.sin(2 * np.pi * 7 * tt) > 0) * np.clip((tt - 0.6) / 1.5, 0, 1)
chaos += st(lp(buzz, 900) * 0.10)
alarm = np.sin(2 * np.pi * np.where((tt * 4).astype(int) % 2, 880, 660) * tt) * np.clip((tt - 1.0) / 1.2, 0, 1) * 0.16
chaos += st(alarm)
# Tape-Stop: Abspielrate 1 -> 0 in den letzten 0.45 s
ts = FREEZE - 0.45; n0 = int(ts * SR); nT = int(FREEZE * SR)
rate = np.ones(nT); rate[n0:] = np.linspace(1, 0, nT - n0) ** 1.6
pos = np.cumsum(rate); chaosOut = np.stack([np.interp(pos, np.arange(len(chaos)), chaos[:, c]) for c in (0, 1)], 1)
chaosOut[n0:] = lp(chaosOut[n0:], 2500)

# ---------- Lo-Fi-Beat ----------
mus = np.zeros((N, 2)); T0 = FREEZE
def note(f, dur, g, t):
    n = int(dur * SR); t_ = np.arange(n) / SR
    idx = 1.6 * np.exp(-t_ * 6) + 0.25
    x = np.sin(2 * np.pi * f * t_ + idx * np.sin(2 * np.pi * f * t_)) * np.exp(-t_ * 1.4) * (1 + 0.12 * np.sin(2 * np.pi * 4.5 * t_))
    x *= np.clip(t_ / 0.006, 0, 1) * np.clip((dur - t_) / 0.08, 0, 1)
    pan = rng.uniform(-0.3, 0.3)
    place(mus, np.stack([x * (1 - pan), x * (1 + pan)], 1), t, g)
mid = lambda m: 440 * 2 ** ((m - 69) / 12)
chords = [[53, 57, 60, 64, 67], [52, 55, 59, 62, 66], [50, 53, 57, 60, 64], [48, 52, 55, 59, 62]]  # Fmaj9 Em7(9) Dm9 Cmaj7(9)
roots = [41, 40, 38, 36]
bar = 4 * BEAT; sw = 0.58
for b in range(5):
    tb = T0 + b * bar
    if tb > DUR: break
    ch = chords[b % 4]
    for k, m in enumerate(ch): note(mid(m), bar, 0.10, tb + k * 0.018)
    for k, m in enumerate(ch[1:]): note(mid(m), BEAT * 1.4, 0.05, tb + BEAT * (1 + 2 * sw) + k * 0.012)
    # Bass
    for off, d in [(0, BEAT * 1.6), (BEAT * 2.5 * 1.0, BEAT)]:
        n = int(d * SR); t_ = np.arange(n) / SR
        place(mus, st(np.sin(2 * np.pi * mid(roots[b % 4]) * t_) * np.exp(-t_ * 1.2) * np.clip((d - t_) / 0.05, 0, 1)), tb + off, 0.32)
def kick():
    t_ = np.arange(int(0.45 * SR)) / SR; f = 45 + 80 * np.exp(-t_ * 28)
    return st(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t_ * 7))
def snare():
    t_ = np.arange(int(0.3 * SR)) / SR; nz = hp(lp(rng.standard_normal(len(t_)), 5000), 900)
    return st(nz * np.exp(-t_ * 16) * 0.6 + np.sin(2 * np.pi * 190 * t_) * np.exp(-t_ * 30) * 0.5)
def hat():
    t_ = np.arange(int(0.06 * SR)) / SR; return st(hp(rng.standard_normal(len(t_)), 7000) * np.exp(-t_ * 70))
K, Sn = kick(), snare()
nb = int((DUR - T0) / BEAT) + 1
for i in range(nb):
    t = T0 + i * BEAT; ib = i % 4
    if ib in (0,): place(mus, K, t, 0.9)
    if ib == 1: place(mus, K, t + BEAT * sw, 0.6)
    if ib == 2: place(mus, K, t + BEAT * 0.5, 0.0)
    if ib in (1, 3): place(mus, Sn, t + 0.012, 0.55)
    place(mus, hat(), t, 0.10); place(mus, hat(), t + BEAT * sw, 0.06)
mus = lp(mus, 3800)
# Vinyl-Knistern + Rauschen
crk = np.zeros(N); pts = rng.integers(0, N, 900); crk[pts] = rng.uniform(-1, 1, 900) ** 3
crk = hp(crk, 1500) * 0.5 + lp(rng.standard_normal(N), 1200) * 0.012
mus += st(crk) * 0.35
tN = np.arange(N) / SR
env = np.clip((tN - T0) / 0.15, 0, 1) * np.clip((DUR - tN) / 0.9, 0, 1)
mus *= env[:, None]

# ---------- SFX ----------
fx = np.zeros((N, 2))
cues = [(FREEZE - 0.02, "glitch", 0.45), (FREEZE, "air_hit", 0.55), (FREEZE + BEAT + 0.05, "whoosh_big", 0.5),
        (FREEZE + 2 * BEAT - 0.3, "swell", 0.35), (FREEZE + 2 * BEAT + 0.25, "chime", 0.45),
        (4.65, "tap", 0.45), (5.4, "whoosh", 0.25), (6.15, "glitch", 0.4), (6.9, "whoosh_big", 0.35),
        (7.0, "swell", 0.3), (7.65, "whoosh", 0.2), (8.39, "impact_soft", 0.5), (8.55, "whoosh", 0.22),
        (9.9, "pop", 0.4), (DUR - 1.1 + 0.25, "chime", 0.4)]
for i in range(6): place(fx, repitch(S["pop"], 0.9 + 0.08 * i), 6.15 + 0.03 * i, 0.25)
for i in range(14): place(fx, repitch(S["blip"], 1.6), 4.65 + 0.25 + i * 0.035, 0.12)
for t, n, g in cues: place(fx, S[n], t, g)

mix = mus * 0.8 + fx
place(mix, chaosOut, 0, 0.9)
mix *= min(1, 0.98 / np.abs(mix).max())
with wave.open("mix.raw.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg","-y","-v","error","-i","mix.raw.wav","-af","loudnorm=I=-14:TP=-1.0:LRA=9","-ar",str(SR),"chill-reel/assets/audio/mix.wav"], check=True)
print("mixed")
