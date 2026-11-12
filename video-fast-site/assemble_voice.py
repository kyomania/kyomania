#!/usr/bin/env python3
"""Cut fresh voice takes into phrases and drop each phrase, unstretched, onto the lip timing.

For every phrase: trim the take to its speech, try every take and a small offset window,
and keep the take/offset whose loudness envelope best matches the mouth movement
(the clip's original audio). No time-stretching anywhere, so no phasey echo.
"""
import glob
import subprocess
import tempfile
import numpy as np
import librosa
import soundfile as sf

SR = 44100
H = 512
TAKES = "voice_takes"
OUT = "motion/assets/audio"

# clip, window start/end in the clip (s), phrases with target speech span relative to window start
SHOTS = {
    "mann": ("clips/v2_mann.mp4", 0.25, 5.08, [("m1a", 1.10, 1.73), ("m1b", 2.05, 4.69)]),
    "oma": ("clips/v2_oma.mp4", 0.25, 3.25, [("o1", 0.26, 1.42), ("o2", 1.63, 2.25)]),
    "vortex": ("clips/v2_vortex.mp4", 0.25, 2.35, [("v1", 0.08, 0.95), ("v2", 1.13, 1.87)]),
    "ende": ("clips/v2_ende.mp4", 1.85, 4.09, [("e1", 0.59, 0.98), ("e2", 1.32, 2.12)]),
}


def load(p, s=None, e=None):
    with tempfile.NamedTemporaryFile(suffix=".wav") as t:
        c = ["ffmpeg", "-loglevel", "error", "-y"] + (["-ss", str(s), "-to", str(e)] if s is not None else []) + ["-i", p, "-vn", "-ac", "1", "-ar", str(SR), t.name]
        subprocess.run(c, check=True)
        y, _ = sf.read(t.name)
    return y.astype(np.float32)


def env(y):
    e = librosa.feature.rms(y=y, frame_length=2048, hop_length=H)[0]
    return (e - e.mean()) / (e.std() + 1e-9)


def corr(a, b):
    n = min(len(a), len(b))
    return float(np.corrcoef(a[:n], b[:n])[0, 1])


def trim(y):
    iv = librosa.effects.split(y, top_db=35, hop_length=256)
    a, b = iv[0][0], iv[-1][1]
    a = max(0, a - int(0.03 * SR))
    b = min(len(y), b + int(0.06 * SR))
    seg = y[a:b].copy()
    f = int(0.008 * SR)
    seg[:f] *= np.linspace(0, 1, f)
    seg[-f:] *= np.linspace(1, 0, f)
    return seg


for shot, (clip, ws, we, phrases) in SHOTS.items():
    ref = load(clip, ws, we)
    R = env(ref)
    buf = np.zeros(len(ref) + SR, dtype=np.float32)
    report = []
    for name, t0, t1 in phrases:
        best = None
        for path in sorted(glob.glob(f"{TAKES}/{name}_*.mp3")):
            seg = trim(load(path))
            for off in np.arange(-0.10, 0.101, 0.01):
                start = int((t0 + off - 0.03) * SR)
                if start < 0:
                    continue
                trial = np.zeros_like(buf)
                trial[start : start + len(seg)] = seg[: len(trial) - start]
                # score only around this phrase
                a, b = int(max(0, t0 - 0.2) * SR / H), int((t1 + 0.3) * SR / H)
                c = corr(R[a:b], env(trial[: len(ref)])[a:b])
                over = max(0.0, (start + len(seg)) / SR - (t1 + 0.12))
                score = c - 0.6 * over  # penalise voice running past the mouth
                if best is None or score > best[0]:
                    best = (score, c, path, start, seg, len(seg) / SR, off)
        score, c, path, start, seg, dur, off = best
        buf[start : start + len(seg)] += seg[: len(buf) - start]
        report.append(f"{name}: take {path.split('_')[-1][0]} len {dur:.2f}s vs mouth {t1 - t0:.2f}s, offset {off:+.2f}s, r={c:.2f}")
    buf = buf[: len(ref) + int(0.6 * SR)]
    buf = buf / (np.abs(buf).max() or 1) * 0.89
    sf.write(f"{OUT}/cut_{shot}.wav", buf, SR)
    print(shot, "| total r =", round(corr(R, env(buf[: len(ref)])), 2))
    for r in report:
        print("   ", r)
