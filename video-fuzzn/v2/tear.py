#!/usr/bin/env python3
"""Zerreißt ein Standbild in zwei Papierhälften mit realistischer Risskante.

Aufruf: python3 tear.py <in.jpg> <out_prefix> <v|h> <seed> [slant_px]
Erzeugt <out_prefix>_a.png und <out_prefix>_b.png (RGBA, 1920x1080).
a = links (v) bzw. oben (h), b = rechts bzw. unten.
Hälfte a zeigt das weiße, faserige Papierinnere (breites Band),
Hälfte b nur eine schmale Kante – so sieht echt gerissenes Papier aus.
"""
import random, sys, math
from PIL import Image, ImageDraw, ImageFilter, ImageChops

W, H, SS = 1920, 1080, 2  # Supersampling für weiche Kanten


def noise_path(n_pts, length, amp, rnd):
    """1D-Midpoint-Displacement: grobe Wellen + feine Zacken."""
    pts = [0.0] * (n_pts + 1)
    pts[0] = rnd.uniform(-amp, amp) * 0.4
    pts[-1] = rnd.uniform(-amp, amp) * 0.4
    step, a = n_pts, amp
    while step > 1:
        half = step // 2
        for i in range(half, n_pts, step):
            pts[i] = (pts[i - half] + pts[min(i + half, n_pts)]) / 2 + rnd.uniform(-a, a)
        step = half
        a *= 0.55
    return [(length * i / n_pts, d) for i, d in enumerate(pts)]


def main():
    src, prefix, mode, seed = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    slant = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
    rnd = random.Random(seed)
    img = Image.open(src).convert("RGB").resize((W, H))
    big = img.resize((W * SS, H * SS), Image.LANCZOS)
    Wb, Hb = W * SS, H * SS

    vertical = mode == "v"
    length = Hb if vertical else Wb
    center = (Wb if vertical else Hb) / 2
    raw = noise_path(512, length, 70 * SS, rnd)
    # Hauptlinie (Rand der Druckschicht) und zweite Linie (Rand des Papierkerns)
    band = noise_path(512, length, 5 * SS, random.Random(seed + 7))

    def to_xy(t, d):
        off = center + d + slant * SS * (t / length - 0.5)
        return (off, t) if vertical else (t, off)

    edge = [to_xy(t, d) for t, d in raw]
    # Breite des weißen Bandes schwankt 4..16 px
    core = []
    for (t, d), (_, b) in zip(raw, band):
        w = (10 + b / SS * 1.2 + 6 * math.sin(t / (90 * SS) + seed)) * SS
        w = max(3 * SS, min(18 * SS, w))
        core.append(to_xy(t, d + w))  # Papierkern reicht etwas in Richtung b

    def region(line, side_a):
        if vertical:
            return ([(0, 0)] + line + [(0, Hb)]) if side_a else ([(Wb, 0)] + line + [(Wb, Hb)])
        return ([(0, 0)] + line + [(Wb, 0)]) if side_a else ([(0, Hb)] + line + [(Wb, Hb)])

    def mask(poly):
        m = Image.new("L", (Wb, Hb), 0)
        ImageDraw.Draw(m).polygon(poly, fill=255)
        return m

    m_print_a = mask(region(edge, True))
    m_core_a = mask(region(core, True))
    m_b = ImageChops.invert(m_core_a)

    # Papierkern-Textur: warmes Off-White mit Faserrauschen
    paper = Image.effect_noise((Wb // 4, Hb // 4), 22).resize((Wb, Hb), Image.BILINEAR)
    paper = Image.merge("RGB", [paper.point(lambda v: int(214 + v * 0.14)),
                                paper.point(lambda v: int(208 + v * 0.14)),
                                paper.point(lambda v: int(194 + v * 0.14))])

    # Hälfte a: Druckbild + weißes Band bis zur Kernlinie
    a = Image.new("RGBA", (Wb, Hb), (0, 0, 0, 0))
    a.paste(paper, (0, 0), m_core_a)
    a.paste(big, (0, 0), m_print_a)
    # dunkle Haarlinie am Übergang Druck/Kern (Stufe im Papier)
    d = ImageDraw.Draw(a)
    d.line(edge, fill=(40, 34, 30, 110), width=SS)

    # Hälfte b: Druckbild, an der Kante schmaler heller Saum
    b_img = Image.new("RGBA", (Wb, Hb), (0, 0, 0, 0))
    b_img.paste(big, (0, 0), m_b)
    shifted = [(x + (3 * SS if vertical else 0), y + (0 if vertical else 3 * SS)) for x, y in core]
    m_rim = ImageChops.subtract(m_b, ImageChops.invert(mask(region(shifted, True))))
    b_img.paste(paper, (0, 0), m_rim)

    # Fasern: feine Härchen, die über die Risskante hinausstehen
    fa, fb = ImageDraw.Draw(a), ImageDraw.Draw(b_img)
    for i in range(0, len(core) - 1):
        for _ in range(3):
            (x0, y0), (x1, y1) = core[i], core[i + 1]
            f = rnd.random()
            x, y = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
            L = rnd.uniform(3, 11) * SS
            ang = rnd.uniform(-0.9, 0.9)
            # nach außen: bei v Richtung +x (für a), -x (für b)
            dx, dy = (math.cos(ang), math.sin(ang)) if vertical else (math.sin(ang), math.cos(ang))
            col = (236, 231, 219, rnd.randint(120, 230))
            fa.line([(x, y), (x + dx * L, y + dy * L)], fill=col, width=max(1, SS // 2))
            if rnd.random() < 0.5:
                bx, by = shifted[i]
                fb.line([(bx, by), (bx - dx * L * 0.7, by - dy * L * 0.7)], fill=col, width=max(1, SS // 2))

    for im, suffix in ((a, "a"), (b_img, "b")):
        im.resize((W, H), Image.LANCZOS).save(f"{prefix}_{suffix}.png", optimize=True)
    print("ok", prefix)


if __name__ == "__main__":
    main()
