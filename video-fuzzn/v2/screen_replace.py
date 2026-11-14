#!/usr/bin/env python3
"""Ersetzt das KI-Spiel auf dem linken Monitor durch echtes Gameplay.

Aufruf: python3 screen_replace.py <base_in.mp4> <base_out.mp4> <gameplay.mp4>
- Projiziert das Gameplay per Homographie auf die vier gemessenen Monitorecken.
- Maske: Hand, Controller und Jacke, die unten links in den Bildschirm ragen,
  werden pro Frame erkannt und bleiben vor dem Gameplay.
- Nur in den Zimmer-Szenen (RANGES); alle anderen Frames laufen unverändert durch.
"""
import subprocess, sys
import numpy as np
from PIL import Image, ImageFilter

W, H, FPS = 1920, 1080, 30
# Bildschirmfläche im Video (gemessen an C08, Kamera fest)
QUAD = [(1162, 413), (1501, 419), (1494, 620), (1157, 614)]  # TL, TR, BR, BL
# (Startzeit im Grundschnitt, Ende, Startzeit im Gameplay)
RANGES = [(35.0, 39.0, 0.0), (42.5, 47.0, 0.15)]
# Zone, in der Hand/Controller/Jacke den Bildschirm überdecken können
OCC_ZONE = (1140, 596, 1310, 630)


def homography(src, dst):
    A, b = [], []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    return np.linalg.solve(np.array(A, float), np.array(b, float))


def read_frames(path, w, h, vf=None):
    cmd = ["ffmpeg", "-v", "error", "-i", path]
    if vf:
        cmd += ["-vf", vf]
    cmd += ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)


def main():
    base_in, base_out, game = sys.argv[1:4]
    # Gameplay: auf Bildschirm-Seitenverhältnis zuschneiden, 30 fps, 680x400
    GW, GH = 680, 400
    gvf = f"fps={FPS},crop=ih*{GW/GH}:ih,scale={GW}:{GH}"
    gframes = list(read_frames(game, GW, GH, gvf))
    print("gameplay frames", len(gframes))

    # Inverse Abbildung Video → Gameplay für PIL.transform(PERSPECTIVE)
    coeffs = homography(QUAD, [(0, 0), (GW, 0), (GW, GH), (0, GH)])
    quad_mask = Image.new("L", (W, H), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(quad_mask).polygon(QUAD, fill=255)
    quad_mask = quad_mask.filter(ImageFilter.GaussianBlur(0.7))
    qm = np.asarray(quad_mask, np.float32) / 255.0

    # Bildschirm-Look: leicht entsättigt, etwas dunkler, weiche Kante, dezentes Glühen
    def screen_look(img):
        a = img.astype(np.float32)
        lum = a.mean(axis=2, keepdims=True)
        a = lum + (a - lum) * 0.9
        a = a * 0.9 + 6
        return np.clip(a, 0, 255)

    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16",
                            "-preset", "fast", "-pix_fmt", "yuv420p", base_out], stdin=subprocess.PIPE)
    x0, y0, x1, y1 = OCC_ZONE
    done = 0
    for i, fr in enumerate(read_frames(base_in, W, H)):
        t = i / FPS
        rng = next((r for r in RANGES if r[0] <= t < r[1]), None)
        if rng is None:
            enc.stdin.write(fr.tobytes()); continue
        gi = min(len(gframes) - 1, int(round((t - rng[0] + rng[2]) * FPS)))
        g = Image.fromarray(gframes[gi]).filter(ImageFilter.GaussianBlur(0.5))
        warped = g.transform((W, H), Image.PERSPECTIVE, tuple(coeffs), Image.BICUBIC)
        wa = screen_look(np.asarray(warped))
        m = qm.copy()
        # Verdeckung: Haut (Hand) oder sehr dunkel (Controller/Jacke) in der Zone bleibt vorne
        z = fr[y0:y1, x0:x1].astype(np.int16)
        r, gch, b = z[..., 0], z[..., 1], z[..., 2]
        lum = (r + gch + b) / 3
        # Haut: hell, warm, aber nicht gesättigt wie Explosions-Orange
        skin = (r > 150) & (gch > 120) & (b > 95) & (r - b > 20) & (r - b < 85) & (gch - b > 5)
        dark = lum < 38
        occ = (skin | dark).astype(np.uint8) * 255
        occ_img = Image.fromarray(occ).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
        m[y0:y1, x0:x1] *= 1.0 - np.asarray(occ_img, np.float32) / 255.0
        out = fr.astype(np.float32) * (1 - m[..., None]) + wa * m[..., None]
        enc.stdin.write(np.clip(out, 0, 255).astype(np.uint8).tobytes())
        done += 1
    enc.stdin.close(); enc.wait()
    print("frames ersetzt:", done)


if __name__ == "__main__":
    main()
