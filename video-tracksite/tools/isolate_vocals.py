"""Isolate vocals with UVR MDX-NET Voc_FT (onnx). Usage: isolate_vocals.py model.onnx in.(mp4|wav) out.wav"""
import subprocess, sys, wave
import numpy as np
import onnxruntime as ort

MODEL, INP, OUT = sys.argv[1:4]
SR = 44100
N_FFT, HOP, DIM_F, DIM_T = 7680, 1024, 3072, 256
CHUNK = HOP * (DIM_T - 1)
TRIM = N_FFT // 2
GEN = CHUNK - 2 * TRIM
NB = N_FFT // 2 + 1
WIN = (0.5 - 0.5 * np.cos(2 * np.pi * np.arange(N_FFT) / N_FFT)).astype(np.float32)  # periodic hann

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", INP, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
mix = np.frombuffer(raw, "<f4").reshape(-1, 2).T.copy()  # [2, n]
n = mix.shape[1]
pad = GEN - n % GEN
mixp = np.concatenate([np.zeros((2, TRIM)), mix, np.zeros((2, pad + TRIM))], 1).astype(np.float32)


def stft(x):  # x [chunk] -> [NB, T] complex, torch.stft(center=True, reflect)
    xp = np.pad(x, (N_FFT // 2, N_FFT // 2), mode="reflect")
    T = 1 + (len(xp) - N_FFT) // HOP
    fr = np.lib.stride_tricks.as_strided(xp, (T, N_FFT), (xp.strides[0] * HOP, xp.strides[0]))
    return np.fft.rfft(fr * WIN, axis=1).T


def istft(X, length):
    fr = np.fft.irfft(X.T, n=N_FFT, axis=1) * WIN
    T = fr.shape[0]
    L = N_FFT + HOP * (T - 1)
    y = np.zeros(L); ws = np.zeros(L)
    for t in range(T):
        y[t * HOP:t * HOP + N_FFT] += fr[t]; ws[t * HOP:t * HOP + N_FFT] += WIN ** 2
    y /= np.maximum(ws, 1e-8)
    return y[N_FFT // 2:N_FFT // 2 + length]


sess = ort.InferenceSession(MODEL)
out = []
for i in range(0, mixp.shape[1] - CHUNK + 1, GEN):
    seg = mixp[:, i:i + CHUNK]
    specs = [stft(seg[c]) for c in range(2)]
    inp = np.stack([specs[0].real, specs[0].imag, specs[1].real, specs[1].imag])[:, :DIM_F][None].astype(np.float32)
    o = sess.run(None, {"input": inp})[0][0]
    full = np.zeros((4, NB, o.shape[2]), np.float32); full[:, :DIM_F] = o
    y = np.stack([istft(full[0] + 1j * full[1], CHUNK), istft(full[2] + 1j * full[3], CHUNK)])
    out.append(y[:, TRIM:-TRIM])
voc = np.concatenate(out, 1)[:, :n] * 1.021
peak = np.abs(voc).max() or 1
voc = voc / max(peak, 1.0)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((voc.T * 32767).astype("<i2").tobytes())
print("vocals", OUT, n / SR, "s")
