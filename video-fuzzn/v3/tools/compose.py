#!/usr/bin/env python3
"""fuzzn v3 „Endless Walk“ – setzt die Ebenen-Welt Bild für Bild zusammen.

Aufruf (aus video-fuzzn/v3):  python3 tools/compose.py [start_s end_s]
Ausgabe: work-render/base_v3.mp4 (1920x1080, 30 fps, ohne Ton)

Ebenen (hinten -> vorne): Himmel, SEARCHING, Pop-up-Häuser, Straße,
Bodenschatten + fuzzn (Greenscreen, freigestellt, Nachtlicht), Vordergrund-Laternen.
Zimmer- und Oma-Szenen laufen als Vollbild-Clips. Krankenhaus mit Kamerafahrt.
"""
import subprocess, sys, math
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

W, H, FPS = 1920, 1080, 30
DUR = 90.0
CX = 960                 # fuzzn steht immer hier
GROUND = 925             # Unterkante der Häuser
FEET = 968               # Fußlinie fuzzn
CHAR_H = 430             # Körpergröße fuzzn in px
SPEED = 300.0            # Scroll-Geschwindigkeit der Häuser in px/s

# ---------- Zeitplan ----------
# Gehen (Welt scrollt) in diesen Intervallen
WALK = [(14.0, 28.0), (29.2, 51.0), (67.0, 83.0)]
# Vollbild-Clips: (start, ende, datei, quell-start)
FULL = [
    (0.0, 4.0, "still:img/Z1_zimmer_socken.png", 0.0),
    (4.0, 9.0, "clips/V1_zimmer_start.mp4", 0.0),
    (9.0, 14.0, "clips/V2_schuhe_an.mp4", 0.0),
    (57.0, 63.0, "clips/V3_oma.mp4", 0.0),
    (84.0, 90.0, "clips/V4_schuhe_aus.mp4", 0.0),
]
# fuzzn-Clips draußen: (start, ende, datei, quell-start, ein, aus)  ein/aus = Einblend-/Ausblendzeit
CHAR = [
    (14.0, 19.0, "clips/G1_laufen.mp4", 0.0, 0.5, 0.0),
    (19.0, 25.0, "clips/G4_freunde_v2.mp4", 0.0, 0.0, 0.0),
    (25.0, 28.6, "clips/G1_laufen.mp4", 1.6, 0.0, 0.6),
    (29.2, 35.2, "clips/G2_doener.mp4", 0.0, 0.5, 0.0),
    (35.2, 37.0, "clips/G1_laufen.mp4", 0.5, 0.0, 0.0),
    (37.0, 43.0, "clips/G5_joint.mp4", 0.0, 0.0, 0.0),
    (43.0, 49.0, "clips/G3_rauchen.mp4", 0.0, 0.0, 0.0),
    (49.0, 51.2, "clips/G1_laufen.mp4", 1.0, 0.0, 0.6),
    (67.0, 69.0, "clips/G1_laufen.mp4", 2.0, 0.5, 0.0),
    (69.0, 74.0, "clips/G6_wurf.mp4", 0.0, 0.0, 0.0),
    (74.0, 76.0, "clips/G1_laufen.mp4", 3.0, 0.0, 0.0),
    (76.0, 81.0, "clips/G8_uhr.mp4", 0.0, 0.0, 0.0),
    (81.0, 83.6, "clips/G1_laufen.mp4", 0.0, 0.0, 0.6),
]
# Häuser: (name, datei, höhe_px, zeit wenn Anker bei fuzzn, anker_x_anteil, unten_crop_anteil)
ELEMS = [
    ("H1", "cut/H1_final.png", 720, 14.2, 0.535, 0.95),
    ("T", "cut/H10a_final.png", 560, 17.0, 0.5, 1.0),
    ("H2", "cut/H2_final.png", 470, 19.2, 0.5, 1.0),
    ("L", "cut/H8_final.png", 520, 21.0, 0.5, 1.0),
    ("H3", "cut/H3_final.png", 600, 22.8, 0.5, 1.0),
    ("H4", "cut/H4_final.png", 520, 28.0, 0.24, 0.95),
    ("T", "cut/H10b_final.png", 560, 31.8, 0.5, 1.0),
    ("L", "cut/H8_final.png", 520, 34.2, 0.5, 1.0),
    ("H5", "cut/H5_final.png", 760, 40.0, 0.5, 1.0),
    ("T", "cut/H10a_final.png", 560, 46.2, 0.5, 1.0),
    ("H6", "cut/H6_final.png", 1650, 51.0, 0.5, 0.955),
    ("L", "cut/H8_final.png", 520, 69.5, 0.5, 1.0),
    ("B", "cut/H9_final.png", 190, 72.4, 0.5, 1.0),
    ("T", "cut/H10b_final.png", 560, 75.8, 0.5, 1.0),
    ("H3", "cut/H3_final.png", 600, 78.8, 0.5, 1.0),
    ("H1", "cut/H1_final.png", 720, 83.0, 0.535, 0.95),
]
# Vordergrund-Laternen verdecken die Schnitte zwischen den fuzzn-Clips (Zeitpunkt, an dem sie die Mitte kreuzen)
FG_TIMES = [19.0, 25.0, 35.2, 37.0, 43.0, 49.0, 69.0, 74.0, 76.0, 81.0]
FG_PARALLAX = 1.9
# Krankenhaus-Kamerafahrt
CRANE_UP = (51.6, 56.2)
ZOOM_IN = (56.2, 57.0)
ZOOM_OUT = (63.0, 63.8)
CRANE_DOWN = (63.8, 66.6)
H6_WINDOW = (0.505, 0.435)   # Omas Fenster (Anteil an Breite/Höhe des Krankenhaus-Bilds)


# ---------- Zimmer: Monitor „LOOKING FOR MATCH“ + Poster-Reparatur ----------
from PIL import ImageDraw, ImageFont
MON_QUAD = [(1172, 413), (1520, 418), (1516, 622), (1170, 614)]   # TL TR BR BL (gemessen an Z1)
SW, SH = 720, 420
F_BIG = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", 56)
F_SM = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 26)


def homography(src, dst):
    A, bb = [], []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); bb.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); bb.append(v)
    return np.linalg.solve(np.array(A, float), np.array(bb, float))


MON_COEF = tuple(homography(MON_QUAD, [(0, 0), (SW, 0), (SW, SH), (0, SH)]))
_qm = Image.new("L", (W, H), 0)
ImageDraw.Draw(_qm).polygon(MON_QUAD, fill=255)
MON_MASK = np.asarray(_qm.filter(ImageFilter.GaussianBlur(0.8)), np.float32) / 255
MON_IN = np.asarray(_qm.filter(ImageFilter.MinFilter(7)), np.uint8) > 128
_st = np.zeros((630 - 405, 1530 - 1160), bool)
_st[:, :16] = True                                  # linker Rand
_st[-14:, : int(_st.shape[1] * 0.4)] = True         # unterer Rand links
MON_STRIP = _st
REF = np.asarray(Image.open("img/Z1_zimmer_socken.png").convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.float32)
REF_LUM = REF.mean(axis=2)
# Monitor-Bereich als Ausschnitt (schneller)
MX0, MY0, MX1, MY1 = 1160, 405, 1530, 630


def screen_image(t):
    im = Image.new("RGB", (SW, SH), (10, 14, 30))
    d = ImageDraw.Draw(im)
    for y in range(SH):  # Verlauf
        c = int(10 + 22 * y / SH)
        d.line([(0, y), (SW, y)], fill=(c, c + 4, c + 26))
    txt = "LOOKING FOR MATCH"
    tw = d.textlength(txt, font=F_BIG)
    d.text(((SW - tw) / 2, 140), txt, font=F_BIG, fill=(245, 245, 250))
    # Ladebalken (läuft in Schleife)
    bx0, bx1, by = 160, SW - 160, 260
    d.rounded_rectangle([bx0, by, bx1, by + 14], 7, fill=(40, 46, 80))
    u = (t * 0.35) % 1.0
    seg = 0.28
    a0 = bx0 + (bx1 - bx0) * max(0, u - seg)
    a1 = bx0 + (bx1 - bx0) * min(1, u)
    d.rounded_rectangle([a0, by, max(a0 + 14, a1), by + 14], 7, fill=(255, 150, 60))
    st = "WARZONE  ·  SUCHE NACH SPIELERN"
    sw2 = d.textlength(st, font=F_SM)
    d.text(((SW - sw2) / 2, 300), st, font=F_SM, fill=(150, 160, 200))
    return im.filter(ImageFilter.GaussianBlur(0.6))


def room_fix(frame, t):
    fr = frame.astype(np.float32).copy()
    # 1) Monitor ersetzen, Verdeckung (fuzzn davor) behalten
    scr = screen_image(t).transform((W, H), Image.PERSPECTIVE, MON_COEF, Image.BICUBIC)
    sa = np.asarray(scr, np.float32)[MY0:MY1, MX0:MX1]
    sa = sa * 0.92 + 4
    reg = fr[MY0:MY1, MX0:MX1]
    lum = reg.mean(axis=2)
    ref = REF_LUM[MY0:MY1, MX0:MX1]
    r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
    skin = (r > 150) & (r - b > 25) & (g > 110)
    inside = MON_IN[MY0:MY1, MX0:MX1]
    cand = (((lum < 60) | skin) & (inside | MON_STRIP)).astype(np.uint8) * 255
    cm = Image.fromarray(cand).copy()
    hh, ww = cand.shape
    for y in range(0, hh, 3):                     # Saat: linker Rand
        if cm.getpixel((2, y)) == 255:
            ImageDraw.floodfill(cm, (2, y), 128)
    for x in range(0, int(ww * 0.4), 3):          # Saat: unterer Rand, linkes Drittel
        if cm.getpixel((x, hh - 3)) == 255:
            ImageDraw.floodfill(cm, (x, hh - 3), 128)
    occ = np.asarray(cm) == 128
    occ_img = Image.fromarray((occ * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    m = MON_MASK[MY0:MY1, MX0:MX1] * (1 - np.asarray(occ_img, np.float32) / 255)
    fr[MY0:MY1, MX0:MX1] = reg * (1 - m[..., None]) + sa * m[..., None]
    return np.clip(fr, 0, 255).astype(np.uint8)


def walk_x(t):
    """Welt-Position (px) zum Zeitpunkt t."""
    x = 0.0
    for a, b in WALK:
        if t <= a:
            break
        x += (min(t, b) - a) * SPEED
    return x


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def demagenta(img):
    """Rosa Stich vom Magenta-Hintergrund aus den Elementen nehmen."""
    a = np.asarray(img).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    pink = np.clip(((r - g) + (b - g)) / 2 - 12, 0, None)
    pink = np.where((r > g) & (b > g * 0.95), pink, 0)
    a[..., 0] = r - pink * 0.55
    a[..., 2] = b - pink * 0.55
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


def night(img, k=0.8):
    """Elemente an die Nacht anpassen: dunkler, leicht blau."""
    a = np.asarray(img).astype(np.float32)
    a[..., :3] *= k
    a[..., 2] = a[..., 2] * 1.06 + 4
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")


def load_elem(path, h, crop_bottom):
    im = Image.open(path).convert("RGBA")
    if crop_bottom < 1.0:
        im = im.crop((0, 0, im.width, int(im.height * crop_bottom)))
        im = im.crop(im.getbbox())
    im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    return night(demagenta(im), 0.82)


# ---------- Assets ----------
print("lade Assets …")
SKY = Image.open("img/W2_himmel.png").convert("RGB")
SKY = SKY.resize((round(SKY.width * 1150 / SKY.height), 1150), Image.LANCZOS)
SKY = ImageEnhance.Brightness(SKY).enhance(0.5)
SKY_TOP = (14, 16, 38)
LETTERS = night(demagenta(Image.open("cut/W1_final.png").convert("RGBA")), 0.78)
LETTERS = LETTERS.resize((round(LETTERS.width * 330 / LETTERS.height), 330), Image.LANCZOS)
STREET = night(demagenta(Image.open("cut/W3_final.png").convert("RGBA")), 0.85)
STREET = STREET.resize((round(STREET.width * 175 / STREET.height), 175), Image.LANCZOS)
EL = []
cache = {}
for name, path, h, tc, ax, cb in ELEMS:
    key = (path, h, cb)
    if key not in cache:
        cache[key] = load_elem(path, h, cb)
    im = cache[key]
    wx = walk_x(tc) + CX - ax * im.width          # linke Kante in Welt-Koordinaten
    EL.append((name, im, wx))
FG = cache.get(("cut/H8_final.png", 520, 1.0)) or load_elem("cut/H8_final.png", 520, 1.0)
FG = FG.resize((round(FG.width * 980 / FG.height), 980), Image.LANCZOS)
FG = ImageEnhance.Brightness(FG).enhance(0.35).filter(ImageFilter.GaussianBlur(6))
SHADOW = Image.new("L", (300, 60), 0)
from PIL import ImageDraw
ImageDraw.Draw(SHADOW).ellipse((10, 10, 290, 50), fill=150)
SHADOW = SHADOW.filter(ImageFilter.GaussianBlur(10))
H6 = [e for e in EL if e[0] == "H6"][0]


def cam_y(t):
    """Kamera-Höhe (px nach oben) bei der Krankenhaus-Fahrt."""
    im = H6[1]
    target = (1 - H6_WINDOW[1]) * im.height - (GROUND - 540)   # Fenster in Bildmitte
    if CRANE_UP[0] <= t < CRANE_UP[1]:
        return target * ease((t - CRANE_UP[0]) / (CRANE_UP[1] - CRANE_UP[0]))
    if CRANE_UP[1] <= t < CRANE_DOWN[0]:
        return target
    if CRANE_DOWN[0] <= t < CRANE_DOWN[1]:
        return target * (1 - ease((t - CRANE_DOWN[0]) / (CRANE_DOWN[1] - CRANE_DOWN[0])))
    return 0.0


def zoom(t):
    if ZOOM_IN[0] <= t < ZOOM_IN[1]:
        u = ease((t - ZOOM_IN[0]) / (ZOOM_IN[1] - ZOOM_IN[0]))
        return 1 + 2.2 * u
    if ZOOM_OUT[0] <= t < ZOOM_OUT[1]:
        u = ease((t - ZOOM_OUT[0]) / (ZOOM_OUT[1] - ZOOM_OUT[0]))
        return 3.2 - 2.2 * u
    return 1.0


# ---------- Clip-Leser ----------
class Clip:
    def __init__(self, path, src_start, size=None):
        self.path, self.size = path, size
        vf = f"fps={FPS}" + (f",scale={size[0]}:{size[1]}" if size else "")
        w, h = size if size else (W, H)
        self.w, self.h = w, h
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(src_start), "-i", path, "-vf", vf,
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.last = None

    def next(self):
        buf = self.p.stdout.read(self.w * self.h * 3)
        if len(buf) == self.w * self.h * 3:
            self.last = np.frombuffer(buf, np.uint8).reshape(self.h, self.w, 3)
        return self.last


def key_green(fr):
    """Grün freistellen, Spill entfernen, Nachtlicht."""
    a = fr.astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    gd = g - np.maximum(r, b)
    alpha = np.clip(1 - (gd - 6) / 22, 0, 1)
    a[..., 1] = np.minimum(g, np.maximum(r, b) + 4)
    # Nachtlicht: dunkler, warmes Licht von links oben, kühler Rand rechts
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]].astype(np.float32)
    xn = xx / a.shape[1]
    warm = 1 - xn
    a *= 0.74
    a[..., 0] *= 1 + 0.12 * warm
    a[..., 1] *= 1 + 0.03 * warm
    a[..., 2] *= 1 + 0.10 * xn
    return np.dstack([np.clip(a, 0, 255), alpha * 255]).astype(np.uint8)


def char_geometry(path):
    """Skalierung und Fußpunkt aus dem ersten Bild (Personen-Box)."""
    fr = Clip(path, 0.0).next()
    al = key_green(fr)[..., 3] > 128
    ys, xs = np.where(al)
    h = ys.max() - ys.min()
    s = CHAR_H / h
    # fuzzn ist bei Freunde/Joint die linke Person: Mittelpunkt der linken Hälfte der Box
    x0, x1 = xs.min(), xs.max()
    if "freunde" in path or "joint" in path:
        left = xs[xs < x0 + (x1 - x0) * 0.3]
        cx = (left.min() + left.max()) / 2
    else:
        cx = (x0 + x1) / 2
    return s, cx, ys.max()


GEO = {}


def render(t0, t1, out):
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "fast",
                            "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    open_full, open_char = {}, {}
    n0, n1 = round(t0 * FPS), round(t1 * FPS)
    for n in range(n0, n1):
        t = n / FPS
        full = next((f for f in FULL if f[0] <= t < f[1]), None)
        if full:
            s, e, path, ss = full
            if path.startswith("still:"):
                frame = np.asarray(Image.open(path[6:]).convert("RGB").resize((W, H), Image.LANCZOS))
            else:
                if full not in open_full:
                    open_full.clear()
                    open_full[full] = Clip(path, ss + (t - s), (W, H))
                frame = open_full[full].next()
            if "zimmer" in path or "schuhe" in path:
                frame = room_fix(frame, t)
            enc.stdin.write(np.ascontiguousarray(frame).tobytes())
            continue
        wx = walk_x(t)
        cy = cam_y(t)
        canvas = Image.new("RGBA", (W, H), SKY_TOP + (255,))
        # Himmel (sehr langsam)
        sx = -((wx * 0.04) % (SKY.width - W))
        canvas.paste(SKY, (int(sx), int(H - SKY.height - 40 + cy * 0.25)))
        # SEARCHING – wiederholt, langsame Parallaxe
        lx = -(wx * 0.12) % (LETTERS.width + 700)
        for k in range(-1, 3):
            x = int(lx + k * (LETTERS.width + 700) - (LETTERS.width + 700))
            canvas.alpha_composite(LETTERS, (x, int(90 + cy * 0.45)))
        # Häuser mit Pop-up
        for name, im, ex in EL:
            x = ex - wx
            if x > W + 50 or x + im.width < -50:
                continue
            # Aufklappen beim Reinkommen rechts, Zuklappen links
            cxe = x + im.width / 2
            u_in = ease((W + im.width * 0.15 - (x)) / (im.width * 0.5 + 300)) if name != "H6" else 1.0
            u_out = ease((x + im.width - (-im.width * 0.05)) / (im.width * 0.5 + 300)) if name != "H6" else 1.0
            u = min(u_in, u_out)
            if u <= 0.02:
                continue
            hh = max(2, int(im.height * u))
            el = im if hh == im.height else im.resize((im.width, hh), Image.BILINEAR)
            if u < 1:
                el = ImageEnhance.Brightness(el).enhance(0.55 + 0.45 * u)
            canvas.alpha_composite(el, (int(x), int(GROUND - hh + cy)))
        # Straße (gekachelt)
        stx = -(wx % STREET.width)
        for k in range(0, W // STREET.width + 3):
            canvas.alpha_composite(STREET, (int(stx + k * STREET.width), int(GROUND - 12 + cy)))
        # fuzzn
        ch = next((c for c in CHAR if c[0] <= t < c[1]), None)
        if ch and cy < 1:
            s, e, path, ss, fin, fout = ch
            if path not in GEO:
                GEO[path] = char_geometry(path)
            sc, ccx, cfeet = GEO[path]
            if ch not in open_char:
                open_char.clear()
                open_char[ch] = Clip(path, ss + (t - s))
            fr = open_char[ch].next()
            rgba = Image.fromarray(key_green(fr), "RGBA")
            rw, rh = round(rgba.width * sc), round(rgba.height * sc)
            rgba = rgba.resize((rw, rh), Image.BILINEAR)
            px = int(CX - ccx * sc)
            py = int(FEET - cfeet * sc)
            op = 1.0
            if fin and t < s + fin:
                op = (t - s) / fin
            if fout and t > e - fout:
                op = min(op, (e - t) / fout)
            if op < 1:
                al = rgba.getchannel("A").point(lambda v: int(v * op))
                rgba.putalpha(al)
            sh = SHADOW.point(lambda v: int(v * op))
            canvas.paste((0, 0, 0, 255), (CX - 150, FEET - 32), sh)
            canvas.alpha_composite(rgba, (px, py))
        # Vordergrund-Laternen (schnell, dunkel, unscharf)
        for ft in FG_TIMES:
            fx = CX - FG.width / 2 - (wx - walk_x(ft)) * FG_PARALLAX
            if -FG.width < fx < W:
                canvas.alpha_composite(FG, (int(fx), int(H - FG.height + 140 + cy)))
        # Zoom ins Fenster
        z = zoom(t)
        if z > 1.001:
            im6, ex6 = H6[1], H6[2]
            wxp = ex6 - wx + H6_WINDOW[0] * im6.width
            wyp = GROUND - im6.height + cy + H6_WINDOW[1] * im6.height
            cw, chh = W / z, H / z
            box = (wxp - cw / 2, wyp - chh / 2, wxp + cw / 2, wyp + chh / 2)
            canvas = canvas.crop(tuple(int(v) for v in box)).resize((W, H), Image.BICUBIC)
        # leichte Vignette
        frame = np.asarray(canvas.convert("RGB")).astype(np.float32)
        enc.stdin.write(np.clip(frame * VIG, 0, 255).astype(np.uint8).tobytes())
        if n % 150 == 0:
            print(f"  {t:5.1f} s")
    enc.stdin.close()
    enc.wait()


yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.35 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) ** 1.4)[..., None]
VIG = np.clip(VIG, 0.55, 1)

if __name__ == "__main__":
    t0 = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
    t1 = float(sys.argv[2]) if len(sys.argv) > 2 else DUR
    out = sys.argv[3] if len(sys.argv) > 3 else "work-render/base_v3.mp4"
    import os
    os.makedirs("work-render", exist_ok=True)
    render(t0, t1, out)
    print("fertig", out)
