#!/usr/bin/env python3
"""Ton für v3: Musik-Loop (90 s, nahtlos) + Schritte + Effekte. Ausgabe: film/assets/audio/mix.wav
Aufruf aus video-fuzzn/v3."""
import subprocess, wave, array, sys, os
sys.argv = ["x"]
import importlib.util
spec = importlib.util.spec_from_file_location("c", "tools/compose.py")
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

SR, DUR = 48000, 90.0
os.makedirs("work-audio", exist_ok=True)


def load(path):
    out = f"work-audio/{os.path.basename(path)}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ar", str(SR), "-ac", "2", out], check=True)
    w = wave.open(out)
    a = array.array("h", w.readframes(w.getnframes()))
    w.close()
    return a


N = int(DUR * SR) * 2
mix = [0.0] * 0
import numpy as np
buf = np.zeros(int((DUR + 4) * SR) * 2, np.float32)


def place(a, t, gain):
    x = np.frombuffer(a, np.int16).astype(np.float32) * gain
    i = int(t * SR) * 2
    j = min(len(buf), i + len(x))
    buf[i:j] += x[: j - i]


# Musik
place(load("audio/music_raw.mp3"), 0.0, 0.7)
# Schritte (4-s-Schnipsel) während der Laufphasen
steps = load("audio/steps.mp3")
for a, b in C.WALK:
    t = a
    while t < b - 0.2:
        seg = steps[: int(min(4.0, b - t) * SR) * 2]
        place(seg, t, 0.32)
        t += 4.0
# Papier-Pop, wenn ein Haus rechts ins Bild klappt
pop = load("audio/pop.mp3")
for name, im, ex in C.EL:
    if name == "H6":
        continue
    target = ex - C.W + im.width * 0.1        # linke Kante kurz nach Eintritt
    for k in range(0, int(DUR * C.FPS)):
        t = k / C.FPS
        if C.walk_x(t) >= target:
            if any(a <= t <= b for a, b in C.WALK):
                place(pop, t, 0.45)
            break
place(load("audio/clap.mp3"), 22.8, 0.8)          # Abklatschen mit den Freunden
place(load("audio/lighter.mp3"), 43.2, 0.7)       # Feuerzeug
place(load("audio/swish.mp3"), 71.9, 0.8)         # Korbwurf
tick = load("../film/assets/sfx/tick.wav")
for k in range(5):
    place(tick, 76.6 + k * 0.45, 0.5)             # Blick auf die Uhr

# alles über 90 s an den Anfang falten -> nahtloser Loop
n90 = int(DUR * SR) * 2
out = buf[:n90].copy()
tail = buf[n90:]
out[: len(tail)] += tail
peak = np.abs(out).max()
if peak > 30000:
    out *= 30000 / peak
os.makedirs("film/assets/audio", exist_ok=True)
w = wave.open("film/assets/audio/mix.wav", "w")
w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(out.astype(np.int16).tobytes())
w.close()
print("mix fertig, peak", peak)
