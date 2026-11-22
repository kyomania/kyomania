"""Hochwertiges Startbild: Ausschnitt Norddeutschland, geneigte Karte, Gold auf Schwarz, Pin auf Mackendorf. 1920x1080."""
import json, math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

D = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080
SS = 2
CW, CH = W * SS, int(H * SS * 1.3)
TARGET = (10.955, 52.392)
COSL = math.cos(math.radians(52.4))
SCALE = CW / 6.5  # Pixel pro Laengengrad*cos -> Ausschnitt ca. 5 Grad breit

def P(lon, lat):
    return (CW * 0.5 + (lon - TARGET[0]) * SCALE * COSL / COSL * COSL,
            CH * 0.56 - (lat - TARGET[1]) * SCALE)

def load(name):
    out = []
    for f in json.load(open(os.path.join(D, "src", name)))["features"]:
        g = f["geometry"]; nm = f["properties"].get("name", "")
        for poly in ([g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]):
            out.append((nm, [P(*c) for c in poly[0]]))
    return out

LAND = load("de.json"); KREIS = load("kreise.json")
rng = np.random.default_rng(7)

def col(c): return Image.new("RGB", (CW, CH), c)
def mask(): return Image.new("L", (CW, CH), 0)

# Hintergrund: fast schwarz mit feiner Struktur (Meer / Ausland)
noise = (rng.normal(0, 1, (CH // 4, CW // 4)) * 255).clip(0, 255).astype(np.uint8)
tex = Image.fromarray(noise).resize((CW, CH), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
base = Image.composite(col((14, 12, 12)), col((5, 5, 6)), tex.point(lambda v: v // 3))

# Land mit Relief-Textur
lm = mask(); L = ImageDraw.Draw(lm)
for _, pts in LAND: L.polygon(pts, fill=255)
relief = (rng.normal(0, 1, (CH // 16, CW // 16)) * 60 + 128).clip(0, 255).astype(np.uint8)
relief = Image.fromarray(relief).resize((CW, CH), Image.BICUBIC).filter(ImageFilter.GaussianBlur(20))
fine = (rng.normal(0, 1, (CH // 2, CW // 2)) * 40 + 128).clip(0, 255).astype(np.uint8)
fine = Image.fromarray(fine).resize((CW, CH), Image.BICUBIC)
landtex = ImageChops.multiply(relief.convert("RGB"), fine.convert("RGB"))
landcol = Image.blend(col((24, 20, 18)), ImageChops.multiply(col((70, 58, 50)), landtex), 0.55)
base = Image.composite(landcol, base, lm)

# Niedersachsen: tiefrotes Leuchten von innen
nm_ = mask(); N = ImageDraw.Draw(nm_)
for n, pts in LAND:
    if n == "Niedersachsen": N.polygon(pts, fill=255)
inner = nm_.filter(ImageFilter.GaussianBlur(60))
base = Image.composite(ImageChops.multiply(col((150, 30, 40)), landtex.point(lambda v: min(255, v + 90))), base,
                       ImageChops.multiply(nm_, inner).point(lambda v: int(v * 0.85)))

# Kreisgrenzen fein, Landesgrenzen hell mit Glow
GOLD = (205, 165, 100)
km = mask(); K = ImageDraw.Draw(km)
for _, pts in KREIS: K.line(pts + [pts[0]], fill=255, width=2)
base = Image.composite(col(GOLD), base, km.point(lambda v: int(v * 0.22)))
bm = mask(); B = ImageDraw.Draw(bm)
for _, pts in LAND: B.line(pts + [pts[0]], fill=255, width=4)
base = Image.composite(col(GOLD), base, bm.filter(ImageFilter.GaussianBlur(14)).point(lambda v: min(255, int(v * 0.9))))
base = Image.composite(col((240, 205, 140)), base, bm)

# Staedte als Lichter
d = ImageDraw.Draw(base)
glow = mask(); Gd = ImageDraw.Draw(glow)
for lon, lat, r in [(9.99, 53.55, 16), (9.73, 52.37, 13), (10.52, 52.27, 10), (10.787, 52.423, 10), (8.80, 53.08, 12),
                    (11.63, 52.12, 11), (13.40, 52.52, 16), (8.05, 52.27, 9), (9.94, 51.54, 8), (8.21, 53.14, 8),
                    (10.55, 52.48, 6), (11.01, 52.23, 6), (10.41, 53.25, 7), (8.53, 52.02, 9), (11.15, 52.60, 5),
                    (9.36, 52.73, 5), (10.08, 52.62, 6), (11.86, 51.48, 9)]:
    x, y = P(lon, lat)
    Gd.ellipse([x - r * 6, y - r * 6, x + r * 6, y + r * 6], fill=255)
    d.ellipse([x - r * 0.6, y - r * 0.6, x + r * 0.6, y + r * 0.6], fill=(255, 225, 170))
base = Image.composite(col((255, 190, 110)), base, glow.filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.45)))

# Pin auf Mackendorf
px, py = P(*TARGET)
rings = mask(); R = ImageDraw.Draw(rings)
for r, w in [(160, 8), (280, 5), (420, 3)]:
    R.ellipse([px - r, py - r, px + r, py + r], outline=255, width=w)
base = Image.composite(col(GOLD), base, rings.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.6)))
lp = mask(); ImageDraw.Draw(lp).ellipse([px - 260, py - 260, px + 260, py + 260], fill=255)
base = Image.composite(col((255, 200, 120)), base, lp.filter(ImageFilter.GaussianBlur(120)).point(lambda v: int(v * 0.35)))
sh = mask(); ImageDraw.Draw(sh).ellipse([px - 70, py - 22, px + 70, py + 22], fill=255)
base = Image.composite(col((0, 0, 0)), base, sh.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.8)))
hh, rr = 270, 100
pin = Image.new("RGB", (CW, CH)); pm = mask()
pd = ImageDraw.Draw(pm)
pd.polygon([(px - rr * 0.86, py - hh + rr * 0.5), (px + rr * 0.86, py - hh + rr * 0.5), (px, py)], fill=255)
pd.ellipse([px - rr, py - hh - rr, px + rr, py - hh + rr], fill=255)
yy, xx = np.mgrid[0:CH, 0:CW]
grad = np.clip(((xx - (px - rr)) / (2 * rr)) * 0.6 + ((yy - (py - hh - rr)) / (hh + rr)) * 0.4, 0, 1)
metal = np.stack([230 - 110 * grad, 190 - 100 * grad, 120 - 70 * grad], -1)
metal += 40 * np.exp(-(((xx - (px - rr * 0.35)) / 30) ** 2 + ((yy - (py - hh - rr * 0.4)) / 45) ** 2))[..., None]
pin = Image.fromarray(metal.clip(0, 255).astype(np.uint8))
base = Image.composite(pin, base, pm)
ImageDraw.Draw(base).ellipse([px - rr * 0.38, py - hh - rr * 0.38, px + rr * 0.38, py - hh + rr * 0.38], fill=(12, 9, 9))

# Perspektive: Karte nach hinten geneigt
def coeffs(src, dst):
    A, Bv = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; Bv += [u, v]
    return list(np.linalg.solve(np.array(A, float), np.array(Bv, float)))
k = 0.17
img = base.transform((CW, CH), Image.PERSPECTIVE,
                     coeffs([(0, 0), (CW, 0), (CW, CH), (0, CH)], [(CW * k, 0), (CW * (1 - k), 0), (CW * 1.08, CH), (-CW * 0.08, CH)]),
                     Image.BICUBIC, fillcolor=(5, 5, 6))
img = img.resize((W, int(CH / SS)), Image.LANCZOS)
top = int(img.height * 0.5 - H * 0.47)
img = img.crop((0, top, W, top + H))

# Tiefenunschaerfe oben und unten
blur = img.filter(ImageFilter.GaussianBlur(9))
dm = Image.fromarray((np.clip(np.abs(np.linspace(-1, 1, H) - 0.0) * 1.3 - 0.55, 0, 1)[:, None] * 255 * np.ones((1, W))).astype(np.uint8))
img = Image.composite(blur, img, dm)

# Goldstaub / Bokeh
dust = Image.new("RGB", (W, H)); dd = ImageDraw.Draw(dust)
random.seed(3)
for _ in range(60):
    x, y, r = random.uniform(0, W), random.uniform(0, H), random.choice([1, 1, 1, 2, 2, 3, 5])
    a = random.uniform(0.2, 0.9)
    dd.ellipse([x - r, y - r, x + r, y + r], fill=(int(230 * a), int(180 * a), int(110 * a)))
img = ImageChops.add(img, dust.filter(ImageFilter.GaussianBlur(1.5)))

# Vignette + leichte Koernung
vig = Image.new("L", (W, H), 0); ImageDraw.Draw(vig).ellipse([-W * .15, -H * .25, W * 1.15, H * 1.3], fill=255)
img = Image.composite(img, Image.new("RGB", (W, H)), vig.filter(ImageFilter.GaussianBlur(220)))
grain = Image.fromarray((rng.normal(128, 10, (H, W))).clip(0, 255).astype(np.uint8)).convert("RGB")
img = ImageChops.overlay(img, grain)
img.save(os.path.join(D, "frames", "start-frame-hq.png"))
print("ok")
