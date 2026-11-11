"""Synthesize the 30 s soundtrack (music + SFX) for the fast.site reel.

128 BPM, 16 bars = exactly 30 s. Deterministic (seeded). No samples, no generation service.
Usage: python3 tools/music.py <out.wav>
"""
import sys, wave
import numpy as np
from scipy import signal

SR = 48000
BPM = 128
BEAT = 60 / BPM          # 0.46875 s
BAR = 4 * BEAT           # 1.875 s
S16 = BEAT / 4
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(128)

L = np.zeros(N); R = np.zeros(N)          # dry bus
VL = np.zeros(N); VR = np.zeros(N)        # reverb send
DUCK = np.ones(N)
KL = np.zeros(N); KR = np.zeros(N)       # kick bus (not ducked)                          # sidechain envelope (kick)


def t_(n):
    return np.arange(n) / SR


def place(x, t, gain=1.0, pan=0.0, send=0.0, kbus=False):
    i = int(round(t * SR))
    if i >= N:
        return
    x = x[: N - i]
    gl = gain * np.cos((pan + 1) * np.pi / 4)
    gr = gain * np.sin((pan + 1) * np.pi / 4)
    (KL if kbus else L)[i:i + len(x)] += x * gl
    (KR if kbus else R)[i:i + len(x)] += x * gr
    if send:
        VL[i:i + len(x)] += x * gl * send
        VR[i:i + len(x)] += x * gr * send


def env(n, a=0.002, d=0.2, curve=4.0):
    tt = t_(n)
    e = np.minimum(tt / max(a, 1e-4), 1.0) * np.exp(-np.maximum(tt - a, 0) * curve / d)
    return e


def lp(x, fc, order=2):
    sos = signal.butter(order, min(fc, SR / 2 - 100) / (SR / 2), "low", output="sos")
    return signal.sosfilt(sos, x)


def hp(x, fc, order=2):
    sos = signal.butter(order, fc / (SR / 2), "high", output="sos")
    return signal.sosfilt(sos, x)


def bp(x, f1, f2, order=2):
    sos = signal.butter(order, [f1 / (SR / 2), f2 / (SR / 2)], "band", output="sos")
    return signal.sosfilt(sos, x)


def sweep_lp(x, f0, f1):
    """Time-varying low-pass via block processing (cheap)."""
    out = np.zeros_like(x)
    blk = 512
    zi = None
    nb = (len(x) + blk - 1) // blk
    for b in range(nb):
        f = f0 * (f1 / f0) ** (b / max(nb - 1, 1))
        sos = signal.butter(2, min(f, SR / 2 - 200) / (SR / 2), "low", output="sos")
        if zi is None:
            zi = np.zeros((sos.shape[0], 2))
        seg = x[b * blk:(b + 1) * blk]
        out[b * blk:b * blk + len(seg)], zi = signal.sosfilt(sos, seg, zi=zi)
    return out


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def saw(f, n, detune=0.0):
    tt = t_(n)
    x = np.zeros(n)
    for d in ([0.0] if not detune else [-detune, 0.0, detune]):
        ph = (f * (1 + d) * tt + rng.random()) % 1.0
        x += 2 * ph - 1
    return x / (1 if not detune else 3)


# ---------------------------------------------------------------- instruments
def kick(strength=1.0):
    n = int(0.45 * SR); tt = t_(n)
    f = 46 + 170 * np.exp(-tt * 38)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-tt * 6.5)
    click = hp(rng.standard_normal(n), 2500) * np.exp(-tt * 300) * 0.35
    return np.tanh((body + click) * 1.6 * strength) * 0.95


def clap():
    n = int(0.35 * SR); tt = t_(n)
    nz = bp(rng.standard_normal(n), 900, 5000)
    e = np.zeros(n)
    for k, off in enumerate([0, 0.011, 0.022, 0.034]):
        i = int(off * SR)
        e[i:] += np.exp(-(tt[: n - i]) * (110 if k < 3 else 22))
    return nz * e * 0.6


def hat(open_=False):
    n = int((0.28 if open_ else 0.06) * SR); tt = t_(n)
    nz = hp(rng.standard_normal(n), 7500)
    return nz * np.exp(-tt * (14 if open_ else 75)) * 0.35


def tick():
    n = int(0.03 * SR); tt = t_(n)
    return np.sin(2 * np.pi * 3200 * tt) * np.exp(-tt * 260) * 0.5 + hp(rng.standard_normal(n), 6000) * np.exp(-tt * 400) * 0.2


def blip(f, d=0.09):
    n = int(d * SR); tt = t_(n)
    return np.sin(2 * np.pi * f * tt) * env(n, 0.001, d * 0.6, 3) * 0.5


def bass(note, d):
    n = int(d * SR); tt = t_(n)
    f = midi(note)
    x = 0.65 * np.sin(2 * np.pi * f * tt) + 0.35 * lp(saw(f, n), 900)
    e = np.minimum(tt / 0.004, 1) * np.exp(-tt * 3.0)
    e[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
    return np.tanh(x * e * 1.4) * 0.8


def stab(notes, d=0.22, bright=3200):
    n = int(d * SR); tt = t_(n)
    x = sum(saw(midi(m), n, 0.006) for m in notes) / len(notes)
    fc = 300 + bright * np.exp(-tt * 18)
    x = sweep_lp(x, bright + 300, 350) if False else x
    # filter envelope approximation: two bands blended by decay
    x = lp(x, bright) * np.exp(-tt * 12) + lp(x, 600) * np.exp(-tt * 6) * 0.4
    return x * np.minimum(tt / 0.002, 1) * 0.9


def pad(notes, d):
    n = int(d * SR); tt = t_(n)
    x = sum(saw(midi(m), n, 0.009) for m in notes) / len(notes)
    x = lp(x, 1400, 2)
    e = np.minimum(tt / 0.35, 1) * np.minimum((d - tt) / 0.4, 1)
    return x * np.clip(e, 0, 1) * 0.5


def pluck(note, d=0.18):
    n = int(d * SR); tt = t_(n)
    f = midi(note)
    x = np.sign(np.sin(2 * np.pi * f * tt)) * 0.5 + np.sin(2 * np.pi * 2 * f * tt) * 0.3
    x = lp(x, 2600) * np.exp(-tt * 16)
    return x * 0.5


def whoosh(d=0.5, up=True, big=False):
    n = int(d * SR); tt = t_(n)
    nz = rng.standard_normal(n)
    f0, f1 = (400, 9000) if up else (9000, 300)
    x = sweep_lp(nz, f0, f1)
    x = hp(x, 180)
    sh = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** (1.4 if up else 0.8)
    if up:
        sh = (tt / d) ** 2.2 * np.exp(-np.maximum(tt - d * 0.92, 0) * 80)
    return x * sh * (0.7 if big else 0.45)


def riser(d):
    n = int(d * SR); tt = t_(n)
    x = sweep_lp(rng.standard_normal(n), 300, 12000) * (tt / d) ** 2
    f = 200 * 2 ** (3 * tt / d)
    x += np.sin(2 * np.pi * np.cumsum(f) / SR) * (tt / d) ** 3 * 0.25
    return x * 0.5


def impact():
    n = int(1.6 * SR); tt = t_(n)
    f = 36 + 90 * np.exp(-tt * 10)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.6)
    nz = lp(rng.standard_normal(n), 3000) * np.exp(-tt * 7) * 0.5
    return np.tanh((sub + nz) * 1.5) * 0.9


def reverse_cymbal(d=0.9):
    n = int(d * SR); tt = t_(n)
    x = hp(rng.standard_normal(n), 5000) * np.exp(-(d - tt) * 5)
    return x * 0.35


def snare():
    n = int(0.2 * SR); tt = t_(n)
    body = np.sin(2 * np.pi * 190 * tt) * np.exp(-tt * 30) * 0.5
    nz = bp(rng.standard_normal(n), 1500, 8000) * np.exp(-tt * 22) * 0.6
    return body + nz


def duck_at(t, depth=0.55, rel=0.16):
    i = int(t * SR)
    n = int(rel * 2.4 * SR)
    tt = t_(n)
    e = 1 - depth * np.exp(-tt / rel * 2.2)
    seg = DUCK[i:i + n]
    DUCK[i:i + n] = np.minimum(seg, e[: len(seg)])


# ---------------------------------------------------------------- arrangement
# Harmony: A minor. Chords per bar (root notes + voicing)
CH = {
    "Am": [57, 60, 64, 67],   # Am7
    "F": [53, 57, 60, 64],    # Fmaj7
    "C": [55, 60, 64, 67],    # C/G
    "G": [55, 59, 62, 67],    # G
}
PROG = ["Am", "Am", "F", "G"]
BASSN = {"Am": 33, "F": 29, "C": 36, "G": 31}

def bar_t(b):
    return b * BAR

K = kick(); KS = kick(1.25); C = clap(); H = hat(); HO = hat(True)

# --- bar 0: loading. clock ticks + drone + "loading" bleeps, riser into bar 1
for i in range(16):
    t = i * S16
    place(tick(), t, 0.35 if i % 4 else 0.6, pan=(-0.3 if i % 2 else 0.3))
place(pad([45, 52, 57], BAR + 0.3), 0.0, 0.5, send=0.6)
for i, t in enumerate([0.25, 0.72, 1.19]):
    place(blip(1320, 0.12), t, 0.35, send=0.5)
place(reverse_cymbal(1.1), bar_t(1) - 1.1, 0.9)
place(riser(1.4), bar_t(1) - 1.4, 0.6)

def groove(b, kick_on=True, clap_on=True, hats=True, bass_on=True, stabs=True, open_hats=True, prog=None):
    t0 = bar_t(b)
    ch = (prog or PROG)[b % 4]
    for beat in range(4):
        tb = t0 + beat * BEAT
        if kick_on:
            place(K, tb, 1.0, kbus=True); duck_at(tb)
        if clap_on and beat in (1, 3):
            place(C, tb, 0.7, send=0.25)
        if hats:
            for s in range(4):
                if s == 2 and open_hats:
                    place(HO, tb + s * S16, 0.5, pan=0.15)
                else:
                    place(H, tb + s * S16, (0.55 if s % 2 else 0.3), pan=(-0.25 if s % 2 else 0.2))
        if bass_on:
            bn = BASSN[ch]
            for s, oct_ in [(2, 0), (3, 12)] if beat % 2 == 0 else [(2, 0), (3, 0)]:
                place(bass(bn + oct_, S16 * 0.95), tb + s * S16, 0.75)
    if stabs:
        for s in [3, 6, 10, 14]:  # syncopated 16ths
            place(stab(CH[ch], 0.2), t0 + s * S16, 0.32, pan=(0.35 if s % 4 == 2 else -0.35), send=0.35)


# Big hit at bar 1 (burst)
place(impact(), bar_t(1), 0.9, send=0.3)
place(whoosh(0.4, up=False, big=True), bar_t(1), 0.6)
for b in range(1, 9):
    groove(b, clap_on=(b >= 2), stabs=(b >= 3), open_hats=(b >= 2))

# --- bars 9-10: breakdown (sphere). pad chords + arpeggio, no kick
for i, ch in enumerate(["F", "G"]):
    place(pad(CH[ch] + [CH[ch][0] + 12], BAR), bar_t(9 + i), 1.4, send=0.7)
    place(bass(BASSN[ch], BAR * 0.98), bar_t(9 + i), 0.8)
arp = [69, 72, 76, 79, 81, 79, 76, 72]
for i in range(32):
    t = bar_t(9) + i * S16
    n_ = arp[i % 8] + (2 if i >= 16 else 0) - (4 if i < 16 else 0)
    place(pluck(n_), t, 0.85, pan=np.sin(i * 0.7) * 0.6, send=0.55)
    if i % 2 == 0:
        place(H, t, 0.18)
# snare roll + riser into drop
for i in range(16):
    t = bar_t(10) + BAR / 2 + i * (BAR / 2) / 16
    place(snare(), t, 0.15 + 0.5 * i / 16, send=0.2)
place(riser(BAR), bar_t(10), 0.7)
place(reverse_cymbal(0.8), bar_t(11) - 0.8, 1.0)

# --- bars 11-12: drop. groove + a stab on every beat (word staccato)
place(impact(), bar_t(11), 1.0, send=0.25)
for b in (11, 12):
    groove(b, prog=["Am", "Am", "F", "G"] if b == 11 else ["G", "G", "G", "G"])
for i in range(8):
    tb = bar_t(11) + i * BEAT
    ch = ["Am", "Am", "F", "F", "G", "G", "G", "G"][i]
    place(stab([n + 12 for n in CH[ch][:3]], 0.16, 4500), tb, 0.38, send=0.3)
place(whoosh(0.45, up=True), bar_t(12) + BEAT - 0.45, 0.6)  # into marquee

# --- bar 13: stack flicker — 16th blips rising
place(KS, bar_t(13), 1.0, kbus=True); duck_at(bar_t(13))
for i in range(16):
    t = bar_t(13) + i * S16
    place(blip(660 * 2 ** (i / 16 * 1.5), 0.07), t, 0.4, pan=(-0.4 if i % 2 else 0.4))
    if i % 4 == 0 and i:
        place(K, t, 0.9, kbus=True); duck_at(t)
    place(H, t, 0.35)
place(bass(33, BAR * 0.9), bar_t(13), 0.6)
place(riser(BAR * 0.6), bar_t(14) - BAR * 0.6, 0.7)

# --- bars 14-15: end card. hit, half-time groove, final stab, tail
place(impact(), bar_t(14), 1.0, send=0.3)
place(pad(CH["Am"] + [69], BAR * 2), bar_t(14), 0.55, send=0.7)
groove(14, clap_on=True, stabs=True, prog=["Am"] * 4)
for beat in range(3):
    tb = bar_t(15) + beat * BEAT
    place(K, tb, 0.9, kbus=True); duck_at(tb)
    for s in range(4):
        place(H, tb + s * S16, 0.3)
place(bass(33, BEAT * 3), bar_t(15), 0.7)
final_t = bar_t(15) + 3 * BEAT        # 29.53
place(stab([57, 60, 64, 69, 72], 0.6, 5000), final_t, 0.6, send=0.9)
place(KS, final_t, 1.0, kbus=True)
place(impact() * 0.7, final_t, 0.8, send=0.4)

# --- SFX at transitions (visual cue list)
CUES_WHOOSH = [(3.75, True), (5.625, False), (9.375, True), (13.125, False), (16.875, True), (24.375, False), (26.25, True)]
for t, up in CUES_WHOOSH:
    if up:
        place(whoosh(0.42, up=True), t - 0.42, 0.55, pan=0.2)
    else:
        place(whoosh(0.4, up=False), t, 0.5, pan=-0.2)
# letter slams FAST.SITE (scene 2)
for i in range(9):
    place(tick() * 1.5, 3.80 + i * 0.045, 0.35, pan=-0.6 + i * 0.15)
# race dots arrive (scene 3)
for t in [6.80, 6.92, 7.03]:
    place(blip(1760, 0.08), t, 0.35, send=0.3)
# shape morphs (scene 4)
for i in range(4):
    place(blip(880 * (1.25 ** i), 0.1), 9.375 + i * 2 * BEAT, 0.3, send=0.4)
# truchet ripple + -35 % slam
place(whoosh(0.9, up=False), 13.2, 0.4)
place(impact() * 0.6, 14.53, 0.7)
# end card: logo pop + CTA ticks
place(blip(2093, 0.12), 27.0, 0.35, send=0.5)
place(blip(1568, 0.12), 27.95, 0.3, send=0.5)

# ---------------------------------------------------------------- mix
# reverb: convolve with decaying stereo noise
ir_n = int(1.8 * SR)
tt = t_(ir_n)
irL = rng.standard_normal(ir_n) * np.exp(-tt * 3.2); irR = rng.standard_normal(ir_n) * np.exp(-tt * 3.2)
irL = lp(irL, 6000); irR = lp(irR, 6000)
irL /= np.sqrt(np.sum(irL ** 2)); irR /= np.sqrt(np.sum(irR ** 2))
revL = signal.fftconvolve(hp(VL, 200), irL)[:N] * 0.6
revR = signal.fftconvolve(hp(VR, 200), irR)[:N] * 0.6

# sidechain: duck everything except kick; approximate by ducking reverb + whole bus lightly
mixL = L * (0.4 + 0.6 * DUCK) + revL * DUCK + KL * 0.8
mixR = R * (0.4 + 0.6 * DUCK) + revR * DUCK + KR * 0.8
# master: gentle glue + soft clip
mix = np.stack([mixL, mixR], 1)
mix /= np.max(np.abs(mix)) + 1e-9
mix = np.tanh(mix * 1.6) / np.tanh(1.6)
# fade the very end
fo = int(0.25 * SR)
mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix *= 0.92

with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype("<i2").tobytes())
print("wrote", sys.argv[1])
