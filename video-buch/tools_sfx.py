"""Sanfte, filmische SFX für den Buch-Spot (deterministisch)."""
import sys, wave, numpy as np
sys.argv = [sys.argv[0], "sfx"]
sys.path.insert(0, "/home/user/kyomania/video-fastsite/tools")
from sfx import save, svf, SR  # nutzt dieselben Helfer
rng = np.random.default_rng(21)

def reverb(x, dur=1.8, mix=0.35):  # einfacher Hall per Rausch-Impulsantwort
    n = int(SR * dur); t = np.arange(n) / SR
    ir = rng.standard_normal(n) * np.exp(-t * 3.0); ir = svf(ir, 3000.0, q=0.5, mode="lp"); ir /= np.abs(ir).sum() ** 0.5 * 8
    L = len(x) + n - 1; N = 1 << (L - 1).bit_length()
    wet = np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(ir, N), N)[:L]
    out = np.zeros(L); out[:len(x)] += x * (1 - mix); return out + wet * mix

def air_hit(name, dur=1.8, f=62, body=1.0):
    n = int(SR * dur); t = np.arange(n) / SR
    att = 1 - np.exp(-t / 0.018)                       # weicher Anschlag, kein Knacken
    sub = np.sin(2 * np.pi * np.cumsum(f + 14 * np.exp(-t * 6)) / SR) * att * np.exp(-t * 2.4)
    air = svf(rng.standard_normal(n), 520.0, q=0.5, mode="lp") * att * np.exp(-t * 4.0) * 0.35
    shim = sum(np.sin(2 * np.pi * h * t + p) for h, p in [(1320, 0), (1985, 1), (2640, 2)]) * np.exp(-t * 3.5) * att * 0.025
    save(name, reverb((sub * body + air + shim), 2.2, 0.4))

def swell(name, dur=0.9):
    n = int(SR * dur); t = np.linspace(0, 1, n)
    y = svf(rng.standard_normal(n), 300 + 2600 * t ** 2, q=0.9) * t ** 3
    y = reverb(y[::-1], 1.2, 0.5)[::-1][-n:]           # Rückwärts-Hall-Gefühl
    save(name, y * np.minimum(1, (1 - t) / 0.03 + 0.0).clip(0, 1) ** 0.5)

def tap(name):
    n = int(SR * 0.35); t = np.arange(n) / SR
    y = svf(rng.standard_normal(n), 1400.0, q=0.6, mode="lp") * (1 - np.exp(-t / 0.002)) * np.exp(-t * 30)
    y += np.sin(2 * np.pi * 90 * t) * np.exp(-t * 18) * 0.6 * (1 - np.exp(-t / 0.004))
    save(name, reverb(y, 0.9, 0.3))

air_hit("air_hit"); air_hit("air_hit_big", 2.6, 48, 1.3); swell("swell"); tap("tap")
print("ok")
