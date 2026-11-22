"""Rendert die Karten-Zoomfahrt (Deutschland -> Mackendorf) als PNG-Frames, 1920x1080, 30 fps."""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
DUR = 5.0
OUT = sys.argv[1] if len(sys.argv) > 1 else "frames_map"
os.makedirs(OUT, exist_ok=True)
SRC = os.path.join(os.path.dirname(__file__), "src")

BG = (14, 12, 11); LAND = (26, 21, 19); NDS = (40, 22, 24)
LINE = (70, 58, 48); KREIS = (52, 42, 36); GOLD = (176, 141, 87); IVORY = (232, 223, 208); WINE = (138, 45, 52)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

# Mackendorf (Gemeinde Velpke, Landkreis Helmstedt) – ungefähre Ortsmitte
TARGET = (10.955, 52.392)
CITIES = [("Hamburg", 9.99, 53.55, 0), ("Berlin", 13.40, 52.52, 0), ("Hannover", 9.73, 52.37, 0),
          ("Magdeburg", 11.63, 52.12, 1), ("Braunschweig", 10.52, 52.27, 1), ("Wolfsburg", 10.787, 52.423, 1),
          ("Helmstedt", 11.01, 52.23, 2), ("Gifhorn", 10.55, 52.48, 2)]

def load(path):
    polys = []
    for f in json.load(open(path))["features"]:
        g = f["geometry"]; name = f["properties"].get("name", "")
        rings = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for poly in rings:
            polys.append((name, poly[0]))
    return polys

LAENDER = load(os.path.join(SRC, "de.json"))
KREISE = load(os.path.join(SRC, "kreise.json"))
COSL = math.cos(math.radians(TARGET[1]))

def ease(t):
    return t * t * (3 - 2 * t)

def cam(t):
    # Zoom: Breite in Längengrad von 11.0 (Deutschland) auf 0.12 (Ort), exponentiell
    z = ease(min(max(t / 4.3, 0), 1))
    span = 17.0 * (0.6 / 17.0) ** z
    # Mittelpunkt wandert von Deutschland-Mitte zum Ziel
    c0 = (10.4, 51.2)
    k = ease(min(max(t / 3.2, 0), 1))
    cx = c0[0] + (TARGET[0] - c0[0]) * k
    cy = c0[1] + (TARGET[1] - c0[1]) * k
    return cx, cy, span

def proj(lon, lat, cx, cy, span):
    s = W / span
    return W / 2 + (lon - cx) * s * COSL, H * 0.47 - (lat - cy) * s

def font(p, size):
    return ImageFont.truetype(p, int(size))

VIG = Image.new("L", (W, H), 0)
ImageDraw.Draw(VIG).ellipse([-W * 0.15, -H * 0.3, W * 1.15, H * 1.3], fill=255)
VIG = VIG.filter(ImageFilter.GaussianBlur(200))
BAND = Image.linear_gradient('L').resize((W, H)).point(lambda v: max(0, (v - 150) * 2))
BLACK = Image.new("RGB", (W, H), (0, 0, 0))
n = int(DUR * FPS)
for i in range(n):
    t = i / FPS
    cx, cy, span = cam(t)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for name, ring in LAENDER:
        pts = [proj(x, y, cx, cy, span) for x, y in ring[:: max(1, int(len(ring) / 600) if span > 3 else 1)]]
        if len(pts) > 2:
            d.polygon(pts, fill=NDS if name == "Niedersachsen" else LAND)
    kalpha = min(max((7.0 - span) / 4.0, 0), 1)
    if kalpha > 0:
        kc = tuple(int(BG[j] + (KREIS[j] - BG[j]) * kalpha) for j in range(3))
        for name, ring in KREISE:
            pts = [proj(x, y, cx, cy, span) for x, y in ring]
            d.line(pts + [pts[0]], fill=kc, width=2)
    for name, ring in LAENDER:
        pts = [proj(x, y, cx, cy, span) for x, y in ring]
        d.line(pts + [pts[0]], fill=LINE, width=3)
    # Straßen-Andeutung: feine goldene Linie Wolfsburg -> Mackendorf, erscheint im Nahbereich
    if span < 2.5:
        a = min((2.5 - span) / 1.5, 1)
        col = tuple(int(BG[j] + (GOLD[j] - BG[j]) * a * 0.7) for j in range(3))
        p1 = proj(10.787, 52.423, cx, cy, span); p2 = proj(*TARGET, cx, cy, span)
        mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 - 40 * (W / span) / 900)
        curve = [((1-u)**2*p1[0]+2*(1-u)*u*mid[0]+u*u*p2[0], (1-u)**2*p1[1]+2*(1-u)*u*mid[1]+u*u*p2[1]) for u in [k/30 for k in range(31)]]
        d.line(curve, fill=col, width=5)
    # Städte
    for name, lon, lat, lvl in CITIES:
        show = {0: span > 1.2, 1: 0.35 < span < 6, 2: 0.25 < span < 2.2, 3: span < 0.9}[lvl]
        if not show:
            continue
        x, y = proj(lon, lat, cx, cy, span)
        if not (-100 < x < W + 100 and -100 < y < H + 100):
            continue
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=IVORY)
        d.text((x + 18, y - 20), name, font=font(SANS, 38), fill=(169, 156, 138))
    # Pin
    px, py = proj(*TARGET, cx, cy, span)
    pin_in = min(max((t - 0.4) / 0.5, 0), 1)
    if pin_in > 0:
        ph = (t * 1.6) % 1
        r = 26 + ph * 110
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        g = ImageDraw.Draw(glow)
        g.ellipse([px - r, py - r, px + r, py + r], outline=GOLD + (int(200 * (1 - ph) * pin_in),), width=5)
        img.paste(glow, (0, 0), glow)
        s = 1.0 + 0.25 * (1 - pin_in)
        hh = 70 * s; rr = 30 * s
        d.ellipse([px - rr, py - hh - rr, px + rr, py - hh + rr], fill=GOLD)
        d.polygon([(px - rr * 0.82, py - hh + rr * 0.5), (px + rr * 0.82, py - hh + rr * 0.5), (px, py)], fill=GOLD)
        d.ellipse([px - rr * 0.38, py - hh - rr * 0.38, px + rr * 0.38, py - hh + rr * 0.38], fill=BG)
    # Vignette
    img = Image.composite(img, BLACK, VIG)
    if t > 2.6:
        img = Image.composite(BLACK, img, BAND.point(lambda v: int(v * min((t - 2.6) / 0.5, 1))))
    d = ImageDraw.Draw(img)
    # Texte
    def center(txt, f, y, col, alpha):
        if alpha <= 0:
            return
        c = tuple(int(col[j] * alpha) for j in range(3))
        w = d.textlength(txt, font=f)
        d.text(((W - w) / 2, y), txt, font=f, fill=c)
    a1 = min(max((t - 0.3) / 0.6, 0), 1) * min(max((2.6 - t) / 0.4, 0), 1)
    center("Ein neuer Ort im Norden.", font(SERIF_I, 60), 90, IVORY, a1)
    a2 = 0 if os.environ.get("NOTEXT") else min(max((t - 2.9) / 0.5, 0), 1)
    center("MACKENDORF", font(SERIF, 96), 790, GOLD, a2)
    center("bei Wolfsburg", font(SERIF_I, 52), 905, IVORY, a2)
    img.save(os.path.join(OUT, f"{i:04d}.png"))
print("frames", n)
