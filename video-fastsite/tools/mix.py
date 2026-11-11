"""Mix music + voiceover + SFX into one 25 s track."""
import subprocess, sys, wave
import numpy as np

SR = 48000
DUR = 25.0
VO_OFFSET = 0.5
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


# --- music with ducking under the voice
music = load(f"{ROOT}/dl/music.mp3")[:N]
vo = load(f"{ROOT}/dl/vo.mp3")
vo_env = np.zeros(N)
vs = int(VO_OFFSET * SR)
a = np.abs(vo).mean(1)
vo_env[vs:vs + len(a)] = a[: N - vs]
# smooth envelope (attack ~30 ms, release ~250 ms)
k = int(0.03 * SR)
sm = np.convolve(vo_env, np.ones(k) / k, mode="same")
active = (sm > 0.01).astype(float)
rel = int(0.25 * SR)
active = np.convolve(active, np.ones(rel) / rel, mode="same").clip(0, 1)
duck = 1.0 - 0.45 * active
t = np.arange(len(music)) / SR
fade = np.clip((DUR - t) / 0.9, 0, 1)  # fade out last 0.9 s
music_gain = 0.42 * duck[: len(music)] * fade
mix[: len(music)] += music * music_gain[:, None]

place(vo, VO_OFFSET, 1.0)

# --- SFX cue sheet (seconds)
S = {n: load(f"{ROOT}/sfx/{n}.wav") for n in
     ["whoosh", "whoosh_big", "impact", "impact_soft", "riser", "glitch", "blip", "tick"]}
cues = [
    (0.05, "glitch", 0.35),
    (0.55, "blip", 0.25), (0.85, "blip", 0.2),
    (1.30, "impact_soft", 0.35),
    (1.15, "riser", 0.45),
    (2.38, "whoosh_big", 0.6),
    (2.58, "impact", 0.7),
    (3.12, "impact", 0.55),
    (3.95, "whoosh", 0.55),
    (5.10, "whoosh", 0.55),
    (6.38, "whoosh", 0.55),
    (6.70, "impact_soft", 0.45),
    (7.40, "whoosh_big", 0.55),
    (7.70, "blip", 0.3),
    (8.55, "blip", 0.3),
    *[(9.0 + i * 0.1, "tick", 0.22) for i in range(8)],
    (9.78, "impact", 0.75),
    (11.55, "glitch", 0.45),
    (12.55, "glitch", 0.45),
    (13.72, "whoosh", 0.5),
    (13.82, "impact", 0.6),
    (15.10, "whoosh_big", 0.5),
    (15.28, "blip", 0.25), (15.95, "blip", 0.25), (16.62, "blip", 0.25),
    (16.60, "riser", 0.5),
    (17.98, "impact", 0.75),
    (19.55, "whoosh_big", 0.55),
    (19.82, "impact", 0.8),
    (21.15, "whoosh", 0.5),
    (21.30, "impact_soft", 0.5),
    (23.20, "impact_soft", 0.45),
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
print("mixed", OUT)
