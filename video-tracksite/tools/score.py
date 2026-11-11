"""Trailer-Score + SFX für den Track-Kinofilm (30 s), komplett im Code, deterministisch.

Aufruf:  uv run --with numpy --with scipy python tools/score.py film/assets/audio/mix.wav
Die Zeitpunkte unten entsprechen den Schnitten in film/index.html (CUT, MERGE, GATE_T).
"""
import sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(11)

CUT = dict(s2=5.2, s3=10.2, s4=15.4, s5=21.0, s6=24.6, logo=25.0)
MERGE, GATE_T, CLICK = 8.6, 14.45, 2.72

L = np.zeros(N); R = np.zeros(N)


def note(name):
    names = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}
    n, o = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((names[n] + 12 * (o - 4)) / 12)


def put(x, t, gain=1.0, pan=0.0):
    """x mono oder (n,2); pan -1..1"""
    i = int(t * SR)
    if i >= N: return
    if x.ndim == 1:
        l, r = x * np.sqrt((1 - pan) / 2) * 1.414, x * np.sqrt((1 + pan) / 2) * 1.414
    else:
        l, r = x[:, 0], x[:, 1]
    n = min(len(l), N - i)
    if i < 0: return
    L[i:i + n] += l[:n] * gain; R[i:i + n] += r[:n] * gain


def lp(x, fc, order=2):
    return sosfilt(butter(order, min(fc, SR * 0.45), "low", fs=SR, output="sos"), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)


def bp(x, f1, f2, order=2):
    return sosfilt(butter(order, [f1, min(f2, SR * 0.45)], "band", fs=SR, output="sos"), x)


def sweep_lp(x, f0, f1, blocks=200):
    """zeitvariabler Tiefpass (blockweise, exponentielle Kurve)"""
    out = np.zeros_like(x); n = len(x); bs = max(1, n // blocks); zi = None
    for b in range(0, n, bs):
        u = b / max(1, n - 1); fc = f0 * (f1 / f0) ** u
        sos = butter(2, min(fc, SR * 0.45), "low", fs=SR, output="sos")
        if zi is None: zi = np.zeros((sos.shape[0], 2))
        out[b:b + bs], zi = sosfilt(sos, x[b:b + bs], zi=zi)
    return out


def saw(f, n, detune=0.0, phase=0.0):
    t = np.arange(n) / SR
    ph = (f * (1 + detune)) * t + phase
    return 2 * (ph % 1) - 1


def env_adsr(n, a, d, s, r):
    t = np.arange(n) / SR; T = n / SR
    e = np.where(t < a, t / max(a, 1e-4), np.where(t < a + d, 1 - (1 - s) * (t - a) / max(d, 1e-4), s))
    rel = np.clip((T - t) / max(r, 1e-4), 0, 1)
    return e * rel


IR_CACHE = {}
def reverb(x, dur=2.8, mix=0.35, damp=4000, seed=3):
    key = (dur, damp, seed)
    if key not in IR_CACHE:
        g = np.random.default_rng(seed); n = int(SR * dur); t = np.arange(n) / SR
        irl = lp(g.standard_normal(n), damp) * np.exp(-t * 6.9 / dur)
        irr = lp(g.standard_normal(n), damp) * np.exp(-t * 6.9 / dur)
        irl /= np.sqrt(np.sum(irl ** 2)); irr /= np.sqrt(np.sum(irr ** 2))
        IR_CACHE[key] = (irl, irr)
    irl, irr = IR_CACHE[key]
    wl = fftconvolve(x, irl); wr = fftconvolve(x, irr)
    dry = np.pad(x, (0, len(wl) - len(x)))
    return np.stack([dry * (1 - mix) + wl * mix, dry * (1 - mix) + wr * mix], 1)


def soft(x, drive=1.5):
    return np.tanh(x * drive) / np.tanh(drive)


# ---------------- Bausteine ----------------
def braam(notes, dur, open_t=0.35, bright=1800, gain=1.0):
    n = int(SR * dur); x = np.zeros(n)
    for f in notes:
        for d in (-0.006, 0.0, 0.007):
            x += saw(f, n, d, rng.random())
    x /= len(notes) * 3
    t = np.arange(n) / SR
    # Filter öffnet schnell, schließt langsam
    fc_env = 120 + bright * np.minimum(1, t / open_t) * np.exp(-np.maximum(0, t - open_t) * 1.3)
    out = np.zeros(n); bs = 480; zi = None
    for b in range(0, n, bs):
        sos = butter(2, fc_env[b], "low", fs=SR, output="sos")
        if zi is None: zi = np.zeros((sos.shape[0], 2))
        out[b:b + bs], zi = sosfilt(sos, x[b:b + bs], zi=zi)
    out = soft(out * 2.2, 1.8) * env_adsr(n, 0.04, 0.6, 0.55, dur * 0.7)
    sub = np.sin(2 * np.pi * notes[0] / 2 * t) * env_adsr(n, 0.02, 0.4, 0.5, dur * 0.7) * 0.6
    return reverb((out + sub) * gain, 3.2, 0.3)


def boom(dur=3.5, f0=70, f1=32, gain=1.0, crack=0.35):
    n = int(SR * dur); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 7)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.3) * (1 - np.exp(-t / 0.004))
    c = lp(rng.standard_normal(n), 2500) * np.exp(-t * 18) * crack
    return reverb(soft((s + c) * gain, 1.3), 3.5, 0.35, 2500)


def riser(dur, f0=200, f1=3500, gain=0.5, tone=True):
    n = int(SR * dur); t = np.arange(n) / SR; u = t / dur
    noise = rng.standard_normal(n)
    y = np.zeros(n); bs = 480; zi = None
    for b in range(0, n, bs):
        fc = f0 * (f1 / f0) ** (u[b] ** 1.5)
        sos = butter(2, [fc * 0.7, min(fc * 1.4, 20000)], "band", fs=SR, output="sos")
        if zi is None: zi = np.zeros((sos.shape[0], 2))
        y[b:b + bs], zi = sosfilt(sos, noise[b:b + bs], zi=zi)
    y = y / (np.max(np.abs(y)) + 1e-9)
    if tone:
        ft = 110 * (8) ** (u ** 2)
        y += 0.35 * np.sin(2 * np.pi * np.cumsum(ft) / SR) + 0.2 * np.sin(2 * np.pi * np.cumsum(ft * 1.5) / SR)
    return reverb(y * u ** 2.2 * gain, 1.5, 0.25)


def whoosh(dur=0.9, f0=300, f1=2400, gain=0.5, pan_from=-0.8, pan_to=0.8):
    n = int(SR * dur); t = np.arange(n) / SR; u = t / dur
    noise = rng.standard_normal(n); y = np.zeros(n); bs = 480; zi = None
    for b in range(0, n, bs):
        fc = f0 * (f1 / f0) ** np.sin(u[b] * np.pi / 2)
        sos = butter(2, [fc * 0.6, min(fc * 1.6, 20000)], "band", fs=SR, output="sos")
        if zi is None: zi = np.zeros((sos.shape[0], 2))
        y[b:b + bs], zi = sosfilt(sos, noise[b:b + bs], zi=zi)
    y = y / (np.max(np.abs(y)) + 1e-9) * np.sin(np.pi * u) ** 1.8 * gain
    p = pan_from + (pan_to - pan_from) * u
    return np.stack([y * np.sqrt((1 - p) / 2) * 1.4, y * np.sqrt((1 + p) / 2) * 1.4], 1)


def ping(f, dur=2.5, gain=0.3, bright=1.0):
    n = int(SR * dur); t = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t * (2.2 + h * 0.9)) for h, a in [(1, 1), (2.01, 0.35 * bright), (3.0, 0.15 * bright), (4.2, 0.08 * bright)])
    y *= (1 - np.exp(-t / 0.002))
    return reverb(y * gain, 2.6, 0.45, 6000)


def tick(gain=0.3, f=2400):
    n = int(SR * 0.05); t = np.arange(n) / SR
    return bp(rng.standard_normal(n), f * 0.7, f * 1.5) * np.exp(-t * 160) * gain


def zap(gain=0.4):
    n = int(SR * 0.35); t = np.arange(n) / SR
    f = 900 * np.exp(-t * 9) + 120
    y = soft(np.sin(2 * np.pi * np.cumsum(f) / SR) * 2, 2) * np.exp(-t * 11)
    y += bp(rng.standard_normal(n), 2000, 6000) * np.exp(-t * 40) * 0.5
    return reverb(y * gain, 1.0, 0.3)


def pad(notes, dur, gain=0.2, cutoff=1400, a=1.5, r=2.0):
    n = int(SR * dur); t = np.arange(n) / SR; x = np.zeros(n)
    for f in notes:
        for d in (-0.004, 0.0, 0.005):
            x += saw(f, n, d, rng.random())
    x = lp(x / (len(notes) * 3), cutoff, 2) * env_adsr(n, a, 0.5, 0.9, r)
    x *= 1 + 0.08 * np.sin(2 * np.pi * 0.25 * t)
    return reverb(x * gain, 3.5, 0.5, 3500)


def drone(f, dur, gain=0.25, cutoff=300):
    n = int(SR * dur); t = np.arange(n) / SR
    x = saw(f, n, -0.003) + saw(f, n, 0.004, 0.3) + 0.5 * saw(f * 2, n, 0.002, 0.7)
    x = lp(x, cutoff, 2) + 0.6 * np.sin(2 * np.pi * f / 2 * t)
    return x * gain


# ---------------- Partitur ----------------
A1, E2, A2, C3, E3, F2, G2, D2 = (note(x) for x in ("A1", "E2", "A2", "C3", "E3", "F2", "G2", "D2"))

# 0 – 5.2  Ignition
n0 = int(SR * 5.6); t0 = np.arange(n0) / SR
dr = drone(A1, 5.6, 0.32, 260) * np.minimum(1, t0 / 2.2) * np.clip((5.6 - t0) / 0.5, 0, 1)
put(dr, 0.0, 1.0)
put(pad([note("A4"), note("E5"), note("B5")], 5.0, 0.06, 5000, a=2.0, r=1.5), 0.2, 1.0)    # Luft / Glas
put(riser(2.6, 300, 4500, 0.35, tone=False), CLICK - 2.6, 1.0)                                  # Ansaugen zum Klick
put(tick(0.9, 3000), CLICK); put(boom(1.6, 110, 45, 0.6, 0.15), CLICK, 0.7)
put(ping(note("E6"), 3.0, 0.45), CLICK, 1.0, 0.2)
put(whoosh(1.4, 250, 3000, 0.55, 0.6, -0.7), CLICK + 0.15)
for k in range(8):                                                                               # Puls setzt ein
    put(boom(0.5, 75, 45, 0.35, 0.0), 3.3 + k * 0.5, 0.45)

# 5.2  Braam 1 (a-Moll)
put(braam([A1, E2, A2, C3], 3.2, 0.25, 1900, 0.9), CUT["s2"])
put(boom(3.0, 70, 30, 0.9, 0.3), CUT["s2"], 0.9)
# 5.2 – 8.6  Orbit: beschleunigende Ticks + zwei umeinander kreisende Töne
tt = CUT["s2"] + 0.4
while tt < MERGE - 0.05:
    u = (tt - CUT["s2"]) / (MERGE - CUT["s2"])
    put(tick(0.25 + 0.3 * u, 2200 + 1800 * u), tt, 1.0, np.sin(tt * 7) * 0.6)
    tt += 0.36 * (1 - u) ** 1.4 + 0.045
n = int(SR * (MERGE - CUT["s2"])); t = np.arange(n) / SR; u = t / t[-1]
fA = 330 * 2 ** (u ** 2 * 1.0); fB = 330 * 2 ** (u ** 2 * 1.0) * 1.0 + 6 * (1 - u)
orbA = np.sin(2 * np.pi * np.cumsum(fA) / SR); orbB = np.sin(2 * np.pi * np.cumsum(fB) / SR)
pan = np.sin(2 * np.pi * np.cumsum(0.5 + 6 * u ** 2) / SR)
env = u ** 1.5 * 0.12
put(np.stack([(orbA * (1 + pan) / 2 + orbB * (1 - pan) / 2) * env, (orbA * (1 - pan) / 2 + orbB * (1 + pan) / 2) * env], 1), CUT["s2"])
put(riser(2.4, 200, 6000, 0.55), MERGE - 2.4)
# 8.6  Verschmelzen
put(boom(4.0, 90, 28, 1.2, 0.5), MERGE, 1.0)
put(braam([A1, E2, A2, E3], 2.5, 0.08, 2600, 0.7), MERGE, 0.8)
put(ping(note("A5"), 3.5, 0.35, 1.2), MERGE + 0.02, 1.0, -0.3); put(ping(note("E6"), 3.5, 0.25, 1.2), MERGE + 0.05, 1.0, 0.3)
put(drone(A1, 1.6, 0.18, 400) * np.linspace(0, 1, int(SR * 1.6)), MERGE)

# 10.2 – 15.4  Tunnel: Ostinato, Consent-Treffer, Tor
put(braam([F2, A2, C3, note("F3")], 2.6, 0.2, 1700, 0.75), CUT["s3"])
put(boom(2.5, 70, 32, 0.8, 0.25), CUT["s3"], 0.8)
step = 0.125; tt = CUT["s3"]; i = 0
while tt < GATE_T - 0.02:
    u = (tt - CUT["s3"]) / (GATE_T - CUT["s3"])
    f = [A1, A1, A2, A1][i % 4] if tt < 12.3 else [F2 / 2 * 2, F2, F2 * 2, F2][i % 4] if tt < 13.3 else [G2, G2, G2 * 2, G2][i % 4]
    nn = int(SR * 0.12); tn = np.arange(nn) / SR
    b = lp(saw(f, nn, 0, 0) + saw(f, nn, 0.006, 0.4), 300 + 2400 * u ** 1.6) * np.exp(-tn * 22)
    put(soft(b * 1.6, 1.4) * (0.22 + 0.18 * u), tt, 1.0, 0.25 if i % 2 else -0.25)
    if i % 4 == 0: put(boom(0.4, 80, 45, 0.5, 0.05), tt, 0.35)
    tt += step; i += 1
for k in range(6):
    put(zap(0.5), 11.0 + k * 0.42, 1.0, [-0.6, 0.5, -0.3, 0.7, -0.7, 0.3][k])
put(riser(1.6, 400, 7000, 0.6), GATE_T - 1.6)
put(whoosh(0.8, 500, 5000, 0.9, -0.2, 0.2), GATE_T - 0.35)
put(ping(note("A5"), 3, 0.3), GATE_T, 1.0, -0.4); put(ping(note("C#6"), 3, 0.25), GATE_T + 0.02, 1.0, 0.0); put(ping(note("E6"), 3, 0.25), GATE_T + 0.04, 1.0, 0.4)
put(boom(1.5, 100, 50, 0.6, 0.4), GATE_T, 0.6)

# 15.4  Auffächern – Höhepunkt
put(boom(4.5, 85, 26, 1.3, 0.55), CUT["s4"], 1.0)
put(braam([A1, E2, A2, note("C#3"), E3], 4.0, 0.12, 2400, 1.0), CUT["s4"])
put(whoosh(1.6, 200, 4000, 0.7, 0.0, 0.0), CUT["s4"] + 0.4)
penta = ["A5", "B5", "C#6", "E6", "F#6", "A6", "B6", "C#7"]
for k in range(8):
    tarr = CUT["s4"] + 0.55 + k * 0.15 + 1.5
    put(ping(note(penta[k]), 2.2, 0.16, 0.8), tarr, 1.0, -0.8 + k * 0.23)
put(pad([A2, E3, note("A3"), note("C#4"), note("E4"), note("B4")], 6.2, 0.13, 2200, a=1.8, r=1.2), 16.6)
put(drone(A1, 6.0, 0.2, 260) * np.minimum(1, np.arange(int(SR * 6)) / SR / 1.5), 15.6)

# 17.4 – 24.5  Momentum: Arpeggio + Puls bis zum Riser
arp = ["A4", "E5", "A5", "C#6", "B5", "E5", "A5", "E6"]
tt = 17.4; k = 0
while tt < 24.45:
    g = 0.07 + 0.06 * min(1, (tt - 17.4) / 6)
    put(ping(note(arp[k % 8]), 1.0, g, 0.6), tt, 1.0, np.sin(k * 0.9) * 0.6)
    if k % 2 == 0: put(boom(0.45, 80, 45, 0.45, 0.0), tt, 0.4 + 0.25 * min(1, (tt - 17.4) / 6))
    tt += 0.25; k += 1
# 21.0 – 24.6  Score
put(whoosh(1.1, 300, 2200, 0.4, 0.5, -0.5), CUT["s5"] - 0.3)
tt = 21.6; k = 0
while tt < 23.5:
    put(tick(0.2, 1800 + k * 60), tt, 1.0, 0.0); tt += 0.09 if tt > 22.6 else 0.14; k += 1
put(ping(note("A5"), 3.0, 0.3), 23.5, 1.0, -0.3); put(ping(note("E6"), 3.0, 0.28), 23.52, 1.0, 0.0); put(ping(note("A6"), 3.0, 0.22), 23.54, 1.0, 0.3)
put(riser(1.05, 300, 9000, 0.75), CUT["s6"] - 1.05)
put(pad([note("F2"), note("C3"), note("A3"), note("E4")], 3.6, 0.16, 2400, a=0.6, r=0.3), 21.0)

# 24.6 – 25.0  Stille.   25.0  der Schlag, das Logo
put(boom(5.0, 75, 24, 1.5, 0.6), CUT["logo"], 1.0)
put(braam([A1, E2, A2, note("C#3"), E3], 4.8, 0.3, 1500, 0.85), CUT["logo"])
for k, (tt, p) in enumerate([(CUT["logo"], -0.8), (CUT["logo"] + 0.12, 0.8), (CUT["logo"] + 0.24, 0.1)]):
    put(whoosh(1.15, 250, 3500, 0.45, p, 0.0), tt)
    put(tick(0.7, 3500), tt + 1.15); put(ping(note(["E6", "A6", "C#7"][k]), 2.2, 0.2), tt + 1.15, 1.0, p * 0.5)
put(whoosh(0.5, 2000, 8000, 0.35, -0.5, 0.5), CUT["logo"] + 1.35)
put(ping(note("A4"), 4.0, 0.25, 1.4), CUT["logo"] + 1.9)
put(pad([A2, E3, note("A3"), note("C#4"), note("E4"), note("G#4"), note("B4")], 4.8, 0.17, 2600, a=0.8, r=1.6), CUT["logo"] + 1.9)
put(boom(2.0, 60, 35, 0.5, 0.0), 28.25, 0.6)

# ---------------- Master ----------------
mix = np.stack([L, R], 1)
mix[:, 0] = hp(mix[:, 0], 28); mix[:, 1] = hp(mix[:, 1], 28)
t = np.arange(N) / SR
gate = np.ones(N)
gate[(t > CUT["s6"] - 0.02) & (t < CUT["logo"])] = 0.0                                      # absolute Stille vor dem Logo
ramp = (t >= CUT["s6"] - 0.06) & (t < CUT["s6"] - 0.02); gate[ramp] = np.linspace(1, 0, ramp.sum())
mix *= gate[:, None]
mix *= np.clip((DUR - t) / 0.6, 0, 1)[:, None]
mix = np.tanh(mix / (np.max(np.abs(mix)) + 1e-9) * 1.6) / np.tanh(1.6) * 0.89
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
print("ok", sys.argv[1])
