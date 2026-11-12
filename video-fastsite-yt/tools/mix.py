"""Mix music + voiceover + SFX into one 30 s track."""
import subprocess, sys, wave
import numpy as np

SR = 48000
DUR = 30.0
VO_OFFSET = 0.9
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
fade = np.clip((DUR - t) / 1.2, 0, 1)  # fade out last 0.9 s
music_gain = 0.5 * duck[: len(music)] * fade
mix[: len(music)] += music * music_gain[:, None]

place(vo, VO_OFFSET, 1.0)

# --- SFX cue sheet (seconds, video time)
S = {n: load(f"{ROOT}/sfx/{n}.wav") for n in
     ["whoosh", "whoosh_big", "impact", "impact_soft", "riser", "glitch", "blip", "tick"]}
V = VO_OFFSET
cues = [
    (0.10, "whoosh", 0.35), (0.35, "blip", 0.2),
    *[(0.6 + i * 0.5, "tick", 0.12) for i in range(14)],
    (V + 2.04, "impact_soft", 0.35), (V + 3.32, "impact_soft", 0.45),
    (V + 4.70, "whoosh", 0.35),
    (6.60, "riser", 0.55), (7.55, "glitch", 0.45),
    (7.98, "impact", 0.85), (7.95, "whoosh_big", 0.6),
    (10.10, "whoosh", 0.45), (V + 9.75, "glitch", 0.3), (V + 11.0, "blip", 0.35),
    (12.75, "whoosh_big", 0.45), (13.05, "impact_soft", 0.4),
    *[(13.3 + i * 0.12, "blip", 0.12) for i in range(6)],
    (15.85, "whoosh", 0.45), (V + 15.9, "riser", 0.3), (V + 16.6, "impact", 0.55),
    (18.85, "whoosh_big", 0.45),
    *[(19.35 + i * 0.12 + 0.28, "tick", 0.18) for i in range(16)],
    (19.63, "impact_soft", 0.35),
    (V + 20.55, "whoosh", 0.5), (V + 21.65, "whoosh", 0.5), (V + 22.7, "whoosh_big", 0.5), (V + 22.75, "impact_soft", 0.45),
    (V + 23.5, "riser", 0.3), (V + 23.67, "impact", 0.85),
    (V + 25.6, "blip", 0.35), (28.35, "blip", 0.45), (28.37, "impact_soft", 0.3),
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
