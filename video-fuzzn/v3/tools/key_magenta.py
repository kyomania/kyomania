#!/usr/bin/env python3
"""Stellt Welt-Elemente vor pinkem/magenta Papierhintergrund frei.

Aufruf: python3 key_magenta.py <in.png> <out.png> [max_breite]
- Kandidaten: Pixel mit deutlichem Magenta-Stich (R und B klar über G).
- Nur der vom Bildrand aus zusammenhängende Hintergrund wird entfernt
  (Flood-Fill), damit z. B. rote Leuchtschrift im Objekt erhalten bleibt.
- Kanten weich, Magenta-Spill an den Rändern wird neutralisiert.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def main():
    src, dst = sys.argv[1], sys.argv[2]
    maxw = int(sys.argv[3]) if len(sys.argv) > 3 else 2400
    im = Image.open(src).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    a = np.asarray(im).astype(np.int16)
    af = a.astype(np.float32) / 255.0
    mx, mn = af.max(axis=2), af.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    rr, gg, bb = af[..., 0], af[..., 1], af[..., 2]
    dd = np.maximum(mx - mn, 1e-6)
    hue = np.where(mx == rr, ((gg - bb) / dd) % 6, np.where(mx == gg, (bb - rr) / dd + 2, (rr - gg) / dd + 4)) * 60
    # Magenta/Pink-Papier in allen Helligkeiten (Farbton 285-345 Grad)
    cand = (hue > 285) & (hue < 345) & (sat > 0.28) & (mx > 0.12)
    cand |= (mx < 0.11)  # sehr dunkle Ecken / schwarzer Himmel
    m = Image.fromarray(np.where(cand, 255, 0).astype(np.uint8)).copy()  # copy: beschreibbar für floodfill
    h, w = cand.shape
    for x in range(0, w, 4):
        for y in (0, h - 1):
            if m.getpixel((x, y)) == 255:
                ImageDraw.floodfill(m, (x, y), 128)
    for y in range(0, h, 4):
        for x in (0, w - 1):
            if m.getpixel((x, y)) == 255:
                ImageDraw.floodfill(m, (x, y), 128)
    # eingeschlossene, große Pink-Flächen (zwischen Ästen, unter dem Viadukt) ebenfalls entfernen
    thr = int(h * w * 0.002)
    arr = np.asarray(m).copy()
    for y in range(0, h, 24):
        for x in range(0, w, 24):
            if arr[y, x] == 255:
                ImageDraw.floodfill(m, (x, y), 64)
                arr = np.asarray(m).copy()
                region = arr == 64
                val = 128 if region.sum() > thr else 200
                arr[region] = val
                m = Image.fromarray(arr).copy()
    bg = (np.asarray(m) == 128)
    alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8))
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    al = np.asarray(alpha).astype(np.float32) / 255.0
    # Spill: an halbtransparenten Rändern Magenta-Stich herausnehmen
    edge = (al > 0.02) & (al < 0.98)
    out = a.astype(np.float32)
    lim = out[..., 1] + 25
    out[..., 0] = np.where(edge, np.minimum(out[..., 0], lim), out[..., 0])
    out[..., 2] = np.where(edge, np.minimum(out[..., 2], lim), out[..., 2])
    rgba = np.dstack([np.clip(out, 0, 255).astype(np.uint8), (al * 255).astype(np.uint8)])
    res = Image.fromarray(rgba, "RGBA")
    bbox = res.getbbox()
    res.crop(bbox).save(dst, optimize=True)
    print(dst, res.crop(bbox).size)


if __name__ == "__main__":
    main()
