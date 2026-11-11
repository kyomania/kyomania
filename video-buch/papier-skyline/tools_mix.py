"""Ton: Musik + Papier-Sounddesign, auf die Schritte der Komposition gelegt."""
import subprocess, wave, numpy as np

SR = 48000; DUR = 30.0; N = int(SR * DUR); mix = np.zeros((N, 2))
SB = "/home/user/kyomania/video-scrapbook"


def load(p, ss=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + ["-i", p, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype="<f4").reshape(-1, 2).astype(np.float64)


def place(x, t, g):
    s = int(t * SR); e = min(N, s + len(x)); mix[s:e] += x[:e - s] * g


m = load(f"{SB}/dl/music.mp3")[:N]; t = np.arange(len(m)) / SR
mix[:len(m)] += m * (0.5 * np.clip(t / 0.5, 0, 1) * np.clip((DUR - t) / 1.4, 0, 1))[:, None]

S = {n: load(f"{SB}/sfx/{n}.wav") for n in ["rip", "tape", "swish", "click", "thump"]}
cues = [
    # A
    (0.1, "swish", .35), (0.5, "thump", .35), (1.0, "swish", .45), (1.45, "tape", .4),
    (1.75, "thump", .5), (2.25, "thump", .5), (2.75, "thump", .6), (5.25, "rip", .7),
    # B
    (6.15, "swish", .4), (6.6, "thump", .45), (6.9, "thump", .4), (7.6, "click", .5), (8.6, "click", .5), (8.62, "tape", .35),
    (9.2, "tape", .5),
    # C
    (12.6, "swish", .35), (12.9, "swish", .3),
    (13.55, "thump", .5), (14.0, "thump", .5), (14.4, "thump", .5), (14.75, "thump", .45), (15.05, "thump", .45),
    (15.6, "swish", .5), (16.15, "thump", .75),
    (16.7, "tape", .55), (17.4, "tape", .55), (18.1, "tape", .55),
    (19.0, "swish", .5), (19.2, "thump", .85),
    # D
    (22.0, "swish", .5), (22.2, "rip", .6), (22.45, "swish", .35),
    (22.75, "swish", .4), (23.2, "thump", .7), (23.45, "tape", .5), (23.65, "tape", .5),
    (24.05, "swish", .35), (24.35, "thump", .4), (24.75, "thump", .65), (25.4, "tape", .5),
]
cues += [(6.4 + i * 0.17, "click", .18) for i in range(6)]                 # Sterne
cues += [(7.5 + i * 0.25, "click", .12 + .05 * (i % 2)) for i in range(20)]  # Tippen
for tt, n, g in cues: place(S[n], tt, g)

mix *= min(1, 0.98 / np.abs(mix).max())
with wave.open("mix.raw.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "mix.raw.wav", "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-ar", str(SR), "assets/audio/mix.wav"], check=True)
print("gemischt:", len(cues), "Cues")
