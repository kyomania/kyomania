#!/usr/bin/env python3
"""Warp a clean TTS line onto the lip timing of a generated video clip.

The video model animated the lips to its own (discarded) audio track. That track is the
timing reference: DTW on MFCCs maps each moment of our line to the moment the lips say it,
then each short chunk of our line is time-stretched to its target length.

usage: lipalign.py <clip.mp4> <ref_start> <ref_end> <tts.mp3> <out.wav>
  ref_start/ref_end: the window of the clip (seconds) that contains the spoken line.
  Output is a wav that starts at ref_start of the clip (place it at that clip time).
"""
import sys
import subprocess
import tempfile
import numpy as np
import librosa
import soundfile as sf

SR = 22050
HOP = 256


def load(path, start=None, end=None):
    with tempfile.NamedTemporaryFile(suffix=".wav") as t:
        cmd = ["ffmpeg", "-loglevel", "error", "-y"]
        if start is not None:
            cmd += ["-ss", str(start), "-to", str(end)]
        cmd += ["-i", path, "-vn", "-ac", "1", "-ar", str(SR), t.name]
        subprocess.run(cmd, check=True)
        y, _ = sf.read(t.name)
    return y.astype(np.float32)


def speech_bounds(y, top_db=32):
    iv = librosa.effects.split(y, top_db=top_db, hop_length=HOP)
    return iv[0][0], iv[-1][1]


def main():
    clip, rs, re_, tts, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
    ref = load(clip, rs, re_)
    src = load(tts)
    r0, r1 = speech_bounds(ref)
    s0, s1 = speech_bounds(src)
    ref_s, src_s = ref[r0:r1], src[s0:s1]

    def feat(y):
        m = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=20, hop_length=HOP)[1:]
        m = (m - m.mean(axis=1, keepdims=True)) / (m.std(axis=1, keepdims=True) + 1e-6)
        return m

    _, wp = librosa.sequence.dtw(X=feat(src_s), Y=feat(ref_s), metric="cosine", global_constraints=True, band_rad=0.25)
    wp = wp[::-1]  # (src_frame, ref_frame), increasing
    # monotone map src frame -> ref frame
    n_src = feat(src_s).shape[1]
    m = np.zeros(n_src)
    for s, r in wp:
        m[s] = max(m[s], r)
    m = np.maximum.accumulate(m)

    # anchors every ~0.12 s of source audio
    step = max(1, int(0.12 * SR / HOP))
    anchors = list(range(0, n_src, step)) + [n_src]
    pieces = []
    for a, b in zip(anchors[:-1], anchors[1:]):
        seg = src_s[a * HOP : min(len(src_s), b * HOP)]
        if len(seg) < 64:
            continue
        ra = m[min(a, n_src - 1)]
        rb = m[min(b, n_src - 1)] if b < n_src else len(ref_s) / HOP
        target = max(1, (rb - ra)) * HOP
        rate = len(seg) / target
        rate = float(np.clip(rate, 0.55, 1.8))
        pieces.append(librosa.effects.time_stretch(seg, rate=rate, n_fft=1024, hop_length=HOP))
    warped = np.concatenate(pieces)
    # final exact fit to the reference speech span
    fit = len(warped) / max(1, len(ref_s))
    if abs(fit - 1) > 0.01:
        warped = librosa.effects.time_stretch(warped, rate=fit, n_fft=1024, hop_length=HOP)
    outbuf = np.zeros(int((re_ - rs) * SR) + SR, dtype=np.float32)
    outbuf[r0 : r0 + len(warped)] = warped[: len(outbuf) - r0]
    peak = np.abs(outbuf).max() or 1
    outbuf = outbuf / peak * 0.89
    sf.write(out, outbuf, SR)
    print(f"{out}: ref speech {r0/SR:.2f}-{r1/SR:.2f}s, tts {len(src_s)/SR:.2f}s -> {len(warped)/SR:.2f}s")


if __name__ == "__main__":
    main()
