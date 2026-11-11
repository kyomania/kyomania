"""Mix music + SFX into the 32 s track for the Track TikTok spot (no voiceover)."""
import subprocess, sys, wave
import numpy as np

SR = 48000
DUR = 32.0
ROOT = sys.argv[1]
OUT = sys.argv[2]


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype="<f4").reshape(-1, 2).astype(np.float64)


N = int(SR * DUR)
mix = np.zeros((N, 2))


def place(x, t, gain=1.0):
    s = int(t * SR)
    e = min(N, s + len(x))
    if s < N:
        mix[s:e] += x[: e - s] * gain


music = load(f"{ROOT}/dl/music.mp3")[:N]
t = np.arange(len(music)) / SR
fade = np.clip((DUR - t) / 1.0, 0, 1)
mix[: len(music)] += music * (0.62 * fade)[:, None]

S = {n: load(f"{ROOT}/sfx/{n}.wav") for n in
     ["whoosh", "whoosh_big", "impact", "impact_soft", "riser", "glitch", "blip", "tick"]}
cues = [
    # S1 Hook
    (0.05, "impact_soft", 0.35), (0.3, "whoosh", 0.3), (0.8, "whoosh", 0.25),
    (1.2, "whoosh", 0.4), (1.4, "whoosh", 0.4), (1.95, "glitch", 0.5), (2.15, "impact", 0.6),
    (2.5, "whoosh_big", 0.5),
    # S2 Probleme
    (2.93, "blip", 0.25), (3.68, "whoosh", 0.3), (4.13, "blip", 0.25), (4.88, "whoosh", 0.3),
    (5.33, "blip", 0.25), (6.08, "whoosh", 0.3),
    (6.0, "blip", 0.25), (6.05, "blip", 0.25), (6.1, "blip", 0.25), (6.18, "whoosh_big", 0.55),
    # S3 Snippet
    (6.5, "impact_soft", 0.45),
    *[(6.9 + i * 0.065, "tick", 0.13) for i in range(18)],
    (8.05, "blip", 0.3), (8.3, "blip", 0.35), (8.55, "whoosh", 0.45),
    # S4 Plattformen
    (8.85, "impact_soft", 0.5), *[(9.05 + i * 0.045, "blip", 0.12) for i in range(12)],
    (10.95, "whoosh", 0.45),
    # S5 Break
    (11.35, "riser", 0.5),
    # S6 Drop
    (12.8, "impact", 0.85), (12.92, "impact_soft", 0.5), (13.15, "whoosh", 0.45), (13.3, "whoosh", 0.45),
    (13.97, "impact", 0.75), (13.97, "glitch", 0.3), (14.2, "blip", 0.3), (15.0, "whoosh_big", 0.55),
    # S7 Consent
    (15.45, "blip", 0.2), (15.55, "blip", 0.2), (15.65, "blip", 0.2), (15.75, "blip", 0.2),
    (16.42, "blip", 0.3), (16.82, "glitch", 0.55), (17.22, "blip", 0.3), (17.4, "whoosh_big", 0.5),
    # S8 Track AI
    (17.75, "blip", 0.3), (18.75, "blip", 0.3), (19.0, "whoosh", 0.35), (19.2, "impact_soft", 0.35),
    (19.62, "blip", 0.4), (19.68, "whoosh_big", 0.5),
    # S9 Score
    (20.3, "whoosh", 0.3), *[(21.05 + i * 0.1, "tick", 0.2) for i in range(9)], (21.95, "impact", 0.6),
    (22.2, "whoosh", 0.4),
    # S10 Recap
    (22.45, "impact_soft", 0.5), (23.2, "impact_soft", 0.5), (24.0, "impact", 0.6), (24.55, "whoosh_big", 0.55),
    # S12 Logo + CTA
    (25.0, "blip", 0.3), (25.6, "impact", 0.9), (25.85, "blip", 0.25), (25.92, "blip", 0.25), (25.99, "blip", 0.25),
    (27.2, "whoosh", 0.35), (28.0, "impact_soft", 0.45), (28.6, "whoosh", 0.3), (29.35, "blip", 0.45),
    (29.42, "impact_soft", 0.45),
]
for tt, n, g in cues:
    place(S[n], tt, g)

peak = np.abs(mix).max()
if peak > 0.98:
    mix *= 0.98 / peak
with wave.open(OUT + ".raw.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", OUT + ".raw.wav",
                "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-ar", str(SR), OUT], check=True)
subprocess.run(["rm", "-f", OUT + ".raw.wav"])
print("mixed", OUT)
