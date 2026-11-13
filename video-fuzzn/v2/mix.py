#!/usr/bin/env python3
"""Mischt Musik-Loop + SFX zu film/assets/audio/mix.wav (60 s). Aufruf aus video-fuzzn/film/."""
import subprocess

ev = []  # (datei, zeit, lautstärke)
for t in [12.0, 23.5, 35.0, 47.0, 59.2]:
    ev.append(("rip", max(0.0, t - 0.03), 1.0))          # Papier reißt
for t, d in [(10.4, 1.6), (16.0, 0.8), (52.0, 1.8)]:      # Uhr: Ping + Ticken
    ev.append(("pingE5", t, 0.5))
    k = 0
    while k * 0.4 < d - 0.1:
        ev.append(("tick", t + 0.2 + k * 0.4, 0.6))
        k += 1
ev.append(("sub", 18.8, 0.9))       # Freeze beim Döner-Biss
ev.append(("pingG5", 40.0, 0.6))    # Herz an Omas Foto
for t in [36.0, 37.0, 38.1, 43.2]:
    ev.append(("tick", t, 0.35))       # Chat-Nachricht

ins = ["-i", "../v2/music_loop.wav"]
f = ["[0:a]volume=0.72[m]"]
lab = ["[m]"]
for i, (n, t, g) in enumerate(ev, 1):
    ins += ["-i", f"assets/sfx/{n}.wav"]
    ms = int(t * 1000)
    f.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g},adelay={ms}|{ms}[s{i}]")
    lab.append(f"[s{i}]")
f.append("".join(lab) + f"amix=inputs={len(lab)}:duration=first:normalize=0,alimiter=limit=0.95,atrim=0:60[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(f),
                "-map", "[o]", "-ar", "48000", "-ac", "2", "assets/audio/mix.wav"], check=True)
print(len(ev), "SFX-Events gemischt")
