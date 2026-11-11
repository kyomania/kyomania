"""Synthesize SFX for the fast.site TikTok video (deterministic, seeded)."""
import sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)
out = sys.argv[1]


def save(name, x):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    peak = np.max(np.abs(x)) or 1
    x = x / peak * 0.95
    with wave.open(f"{out}/{name}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def svf(x, fc, q=0.7, mode="bp"):
    """State-variable filter with per-sample cutoff array."""
    fc = np.broadcast_to(fc, x.shape)
    low = band = 0.0
    y = np.zeros_like(x)
    damp = 1.0 / q
    for i in range(len(x)):
        f = 2 * np.sin(np.pi * min(fc[i], SR / 6) / SR)
        high = x[i] - low - damp * band
        band += f * high
        low += f * band
        y[i] = band if mode == "bp" else (low if mode == "lp" else high)
    return y


def env(n, a, r, curve=2.0):
    t = np.linspace(0, 1, n)
    e = np.minimum(t / max(a, 1e-4), 1.0) * (1 - np.clip((t - (1 - r)) / r, 0, 1)) ** curve
    return e


def whoosh(dur, f0, f1, name, pan=True):
    n = int(SR * dur)
    noise = rng.standard_normal(n)
    t = np.linspace(0, 1, n)
    fc = f0 * (f1 / f0) ** (np.sin(t * np.pi / 2))
    y = svf(noise, fc, q=1.4)
    e = np.sin(np.pi * t) ** 1.6
    y *= e
    if pan:
        l = y * (1 - 0.6 * t); r = y * (0.4 + 0.6 * t)
        save(name, np.stack([l, r], 1))
    else:
        save(name, y)


def impact(name, dur=1.6, f0=95, f1=38, crack=0.5):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 9)
    ph = 2 * np.pi * np.cumsum(f) / SR
    sub = np.sin(ph) * np.exp(-t * 3.2)
    sub = np.tanh(sub * 2.2)
    nz = rng.standard_normal(n) * np.exp(-t * 28) * crack
    nz = svf(nz, 2400.0, q=0.6, mode="lp")
    tail = svf(rng.standard_normal(n), 900.0, q=0.5, mode="lp") * np.exp(-t * 5) * 0.25
    save(name, sub + nz + tail)


def riser(name, dur=1.4):
    n = int(SR * dur)
    t = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    y = svf(noise, 300 * (9000 / 300) ** t, q=3.0) * t ** 2.2
    ph = 2 * np.pi * np.cumsum(180 * 2 ** (3 * t ** 1.5)) / SR
    tone = np.sin(ph) * 0.25 * t ** 2
    save(name, y + tone)


def glitch(name, dur=0.32):
    n = int(SR * dur)
    y = np.zeros(n)
    seg = int(SR * 0.02)
    for k in range(0, n, seg):
        f = rng.choice([220, 440, 880, 1760, 3520, 120])
        tt = np.arange(min(seg, n - k)) / SR
        sq = np.sign(np.sin(2 * np.pi * f * tt)) * (0.5 if rng.random() > 0.3 else 0)
        y[k:k + len(tt)] = sq + rng.standard_normal(len(tt)) * 0.3 * (rng.random() > 0.5)
    y = np.round(y * 4) / 4  # bitcrush
    y *= env(n, 0.01, 0.3)
    save(name, y)


def blip(name, f=1800, dur=0.09):
    n = int(SR * dur)
    t = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * t) * np.exp(-t * 55)
    save(name, y)


def tick(name):
    blip(name, 3200, 0.04)


whoosh(0.55, 400, 6000, "whoosh")
whoosh(0.9, 200, 4500, "whoosh_big")
impact("impact")
impact("impact_soft", dur=1.0, f0=120, f1=55, crack=0.25)
riser("riser")
glitch("glitch")
blip("blip")
tick("tick")
print("ok")
