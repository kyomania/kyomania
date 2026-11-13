#!/usr/bin/env python3
"""Mischt Musik-Loop + SFX zu film/assets/audio/mix.wav (60 s). Aufruf aus video-fuzzn/film/."""
import subprocess

ev = []  # (datei, zeit, lautstärke)
for t in [14.5, 23.5, 35.0, 47.0, 59.4]:
    ev.append(("rip", max(0.0, t - 0.03), 1.0))          # Papier reißt
for t, d in [(12.2, 2.3), (52.0, 1.8)]:      # Uhr: Ping + Ticken
    ev.append(("pingE5", t, 0.5))
    k = 0
    while k * 0.4 < d - 0.1:
        ev.append(("tick", t + 0.2 + k * 0.4, 0.6))
        k += 1
ev.append(("sub", 16.5, 0.9))       # Freeze beim Döner-Biss
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
f[0] = "[0:a]volume=0.72,apad=whole_dur=62[m]"
f.append("".join(lab) + f"amix=inputs={len(lab)}:duration=first:normalize=0,alimiter=limit=0.89:level=0,atrim=0:62[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(f),
                "-map", "[o]", "-ar", "48000", "-ac", "2", "../v2/work-mix62.wav"], check=True)
# Alles, was über 60 s hinausklingt (Loop-Riss), an den Anfang falten → nahtloser Ton-Loop
import wave, array
w = wave.open("../v2/work-mix62.wav"); sr, ch = w.getframerate(), w.getnchannels()
x = array.array("h", w.readframes(w.getnframes())); w.close()
N = 60 * sr * ch
out = array.array("h", x[:N])
for i, v in enumerate(x[N:]):
    out[i] = max(-32768, min(32767, out[i] + v))
o = wave.open("assets/audio/mix.wav", "w"); o.setnchannels(ch); o.setsampwidth(2); o.setframerate(sr)
o.writeframes(out.tobytes()); o.close()
