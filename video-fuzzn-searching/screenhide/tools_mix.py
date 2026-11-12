"""Mischt Musik, Atmo und Soundeffekte zu assets/audio/mix.wav (exakt 60 s, loopbar)."""
import subprocess, os

A = "assets/audio"
SR = 48000
DUR = 60.0

# (Datei, Startzeit s, Lautstärke in dB nach Peak-Normalisierung auf -1 dBFS, optional Länge)
EVENTS = [
    ("chain", 1.2, -16), ("brush", 5.75, -8), ("crows", 5.8, -20, 1.6), ("brush", 7.3, -6),
    ("splat", 14.0, -6), ("thunder", 15.3, -16), ("thunder", 21.4, -14),
    ("crows", 23.0, -5), ("crows", 26.55, -3, 1.6),
    ("kunai", 27.85, -4), ("tear", 29.25, -3), ("tear", 30.75, -3), ("tear", 32.25, -3), ("tear", 33.75, -2),
    ("brush", 34.15, -6), ("kunai", 35.0, -10), ("brush", 36.1, -10),
    ("bass", 40.0, -3), ("thunder", 43.2, -18), ("bass", 46.3, -9), ("thunder", 47.0, -12),
    ("chidori", 47.5, -6), ("thunder", 49.35, -4), ("chidori", 50.4, -10), ("chidori", 52.2, -14),
    ("brush", 53.2, -5), ("chain", 55.2, -14),
]
# Atmo-Betten: (Datei, [(von, bis, dB)])
BEDS = [
    ("wind", [(0, 14.6, -20), (36.4, 40.0, -22), (53.2, 60.0, -20)]),
    ("rain", [(14.8, 27.6, -14)]),
]

def run(cmd):
    subprocess.run(cmd, check=True)

os.makedirs(f"{A}/norm", exist_ok=True)
# 1) jede SFX-Datei peak-normalisieren (manche Modelle liefern sehr leise Dateien)
for name in {e[0] for e in EVENTS} | {b[0] for b in BEDS}:
    src = f"{A}/sfx/{name}.mp3"
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    peak = float(out.split("max_volume:")[1].split("dB")[0])
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-af", f"volume={-1 - peak}dB,aresample={SR}", "-ac", "2", f"{A}/norm/{name}.wav"])

# 0) Musik nahtlos machen: Takte 0-16 + Phrase Takt 4-8 = 20 Takte (64 s @ 75 BPM) -> 60 s @ 80 BPM
BAR = 3.2
XF = 0.03
run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{A}/music.mp3", "-ar", str(SR), "-ac", "2", "-t", str(16 * BAR), f"{A}/norm/m_a.wav"])
run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(4 * BAR), "-i", f"{A}/music.mp3", "-ar", str(SR), "-ac", "2", "-t", str(4 * BAR), f"{A}/norm/m_b.wav"])
run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{A}/norm/m_a.wav", "-i", f"{A}/norm/m_b.wav", "-filter_complex",
     f"[0][1]acrossfade=d={XF}:c1=tri:c2=tri,atempo={(20 * BAR - XF) / DUR:.6f},atrim=0:{DUR}[o]", "-map", "[o]", f"{A}/music_loop.wav"])
inputs, filters, labels = ["-i", f"{A}/music_loop.wav"], [], []
# Musik: exakt 60 s, kurze Rampen an der Naht
filters.append(f"[0:a]aresample={SR},atrim=0:{DUR},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={DUR-0.01}:d=0.01,volume=-3dB[mus]")
labels.append("[mus]")
idx = 1
for name, segs in BEDS:
    for (a, b, db) in segs:
        inputs += ["-stream_loop", "-1", "-i", f"{A}/norm/{name}.wav"]
        fi = 0.04 if a == 0 else 0.6
        fo = 0.04 if b >= DUR else 0.6
        filters.append(f"[{idx}:a]atrim=0:{b-a},asetpts=PTS-STARTPTS,afade=t=in:d={fi},afade=t=out:st={b-a-fo}:d={fo},volume={db}dB,adelay={int(a*1000)}|{int(a*1000)}[b{idx}]")
        labels.append(f"[b{idx}]"); idx += 1
for ev in EVENTS:
    name, t, db = ev[:3]
    ln = ev[3] if len(ev) > 3 else None
    inputs += ["-i", f"{A}/norm/{name}.wav"]
    trim = f"atrim=0:{ln},afade=t=out:st={ln-0.4}:d=0.4," if ln else ""
    filters.append(f"[{idx}:a]{trim}volume={db}dB,adelay={int(t*1000)}|{int(t*1000)}[e{idx}]")
    labels.append(f"[e{idx}]"); idx += 1
filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:dropout_transition=0,atrim=0:{DUR},alimiter=limit=0.89[pre]")
filters.append("[pre]loudnorm=I=-16:TP=-1.5:LRA=11[out]")
run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(filters), "-map", "[out]", "-ar", str(SR), "-ac", "2", "-t", str(DUR), f"{A}/mix.wav"])
print("mix ok")
