"""Baut aus den Seedream-Rohbildern (src/) die fertigen Ebenen für die Komposition (assets/img/).

python3 tools_assets.py
"""
import os, cv2, numpy as np
from scipy import ndimage as ndi
from tools_cut import key, despill, HALF

OUT = "assets/img"
os.makedirs(OUT, exist_ok=True)


def load(i):
    return cv2.resize(cv2.imread(f"src/g{i:02d}.png"), HALF, interpolation=cv2.INTER_AREA)


def keyed(i, **kw):
    img = load(i)
    a, _ = key(img, **kw)
    return despill(img, a), a


def clean(a, keep_largest=True, close=0):
    m = a > 0.5
    m = ndi.binary_opening(m, iterations=2)
    if close: m = ndi.binary_closing(m, iterations=close)
    m = ndi.binary_fill_holes(m)
    if keep_largest:
        lab, n = ndi.label(m)
        if n > 1:
            sizes = ndi.sum(m, lab, range(1, n + 1))
            m = lab == (np.argmax(sizes) + 1)
    m = ndi.binary_dilation(m, iterations=2)
    return a * m


def save(name, img, a, box=None, maxh=None, maxw=None):
    if box:
        x0, y0, x1, y1 = box
        img, a = img[y0:y1, x0:x1], a[y0:y1, x0:x1]
    ys, xs = np.where(a > 0.02)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([img[y0:y1, x0:x1], (a[y0:y1, x0:x1] * 255).astype(np.uint8)])
    h, w = rgba.shape[:2]
    s = 1.0
    if maxh: s = min(s, maxh / h)
    if maxw: s = min(s, maxw / w)
    if s < 1: rgba = cv2.resize(rgba, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f"{OUT}/{name}.png", rgba, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    print(f"{name:14s} {rgba.shape[1]}x{rgba.shape[0]}")


def part(img, a, box, **kw):
    x0, y0, x1, y1 = box
    sub = np.zeros_like(a); sub[y0:y1, x0:x1] = a[y0:y1, x0:x1]
    return clean(sub, **kw)


def yellow(img, a):
    """Graues Papier -> Signalgelb, Struktur und Druck bleiben (Luminanz-Mapping)."""
    lum = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    lum = np.clip((lum - 0.08) / 0.82, 0, 1) ** 0.85
    dark = np.array([20, 40, 70], np.float32)      # BGR: dunkles Ocker
    mid = np.array([54, 201, 243], np.float32)     # #F3C936
    lite = np.array([190, 240, 255], np.float32)
    t = lum[..., None]
    out = np.where(t < 0.6, dark + (mid - dark) * (t / 0.6), mid + (lite - mid) * ((t - 0.6) / 0.4))
    # Messing-Gelenke und Haare (schon farbig / sehr dunkel) behalten mehr Original
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    keep = ((hsv[..., 1] > 90) & (hsv[..., 0] > 12) & (hsv[..., 0] < 35)).astype(np.float32)
    keep = cv2.GaussianBlur(keep, (0, 0), 1.5)[..., None]
    out = out * (1 - keep) + img.astype(np.float32) * keep
    return out.clip(0, 255).astype(np.uint8)


# ---------- Figur: 4 Posen (g04) ----------
img, a = keyed(4, smin=30)
poses = {"pose_kauern": (15, 1830, 510, 2510), "pose_laptop": (30, 700, 700, 1600),
         "pose_jubel": (420, 200, 1270, 1530), "pose_sitzen": (640, 1110, 1440, 2490)}
for n, box in poses.items():
    pa = part(img, a, box)
    if n == "pose_sitzen":  # Klotz unter der Figur entfernen
        ys, xs = np.where(pa > 0.5); x0, y0, x1, y1 = xs.min(), ys.min(), xs.max(), ys.max(); H, W = y1 - y0, x1 - x0
        yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
        blk = ((xx > x0 + 0.68 * W) & (yy > y0 + 0.615 * H)) | ((xx > x0 + 0.6 * W) & (yy > y0 + 0.64 * H))
        pa = pa * ~blk
        pa = clean(pa)
    save(n, img, pa, maxh=1100)
    if n in ("pose_jubel", "pose_sitzen"):
        save(n + "_gelb", yellow(img, pa), pa, maxh=1100)

# ---------- Kiosk (g06) mit Retusche des Farbcodes ----------
img, a = keyed(6, smin=30)
a = clean(a)
ys, xs = np.where(a > 0.5); oy, ox = ys.min(), xs.min()     # Offset der Freistellung (cut/g06_k0 war ab hier)
def patch(dst, src):  # (x0,y0,x1,y1) relativ zum Kiosk-Ausschnitt
    x0, y0, x1, y1 = dst; sx, sy = src
    img[oy + y0:oy + y1, ox + x0:ox + x1] = img[oy + sy:oy + sy + (y1 - y0), ox + sx:ox + sx + (x1 - x0)]
patch((930, 438, 1300, 522), (930, 338))
patch((120, 440, 500, 503), (120, 345))
save("kiosk", img, a, maxh=1100)

# ---------- Türme (g07): einzeln, unterschiedlich hoch abgeschnitten ----------
img, a = keyed(7, smin=30)
towers = [("turm_zeitung", 0, 300, 700, 2270), ("turm_kraft", 325, 575, 420, 2190),
          ("turm_weiss", 610, 860, 900, 2190), ("turm_dunkel", 890, 1155, 560, 2190),
          ("turm_grau", 1185, 1440, 1000, 2335)]
for n, x0, x1, top, bot in towers:
    pa = part(img, a, (x0, top, x1, bot), keep_largest=True)
    save(n, img, pa, maxh=1300)

# ---------- Hauptturm (g08) ----------
img, a = keyed(8, smin=30)
save("turm_haupt", img, clean(a), maxh=1700)

# ---------- Ferne Skyline (g09) ----------
img, a = keyed(9, smin=30)
save("skyline", img, part(img, a, (0, 560, 1440, 1520)), maxw=1440)

# ---------- Himmel (g10) ----------
img, a = keyed(10, smin=30)
sky = {"sonne": (570, 370, 1250, 1010), "mond": (100, 420, 570, 1045), "wolke1": (70, 1150, 720, 1495),
       "wolke2": (780, 1060, 1365, 1390), "wolke3": (365, 1445, 1275, 1915), "stern": (85, 1590, 262, 1765)}
for n, box in sky.items():
    save(n, img, part(img, a, box), maxh=700)

# ---------- Material (g11): Klebeband und Streifen ----------
img, a = keyed(11, smin=30)
mat = {"band_creme": (90, 700, 980, 950), "band_creme2": (455, 1315, 1390, 1590),
       "band_beige": (60, 1645, 1010, 1910), "band_gelb": (670, 1945, 980, 2560),
"fetzen": (1045, 0, 1440, 405)}
for n, box in mat.items():
    save(n, img, part(img, a, box))

# ---------- Gelbe Zettel mit Sicherheitsnadel (g03, Hintergrund grün) ----------
img = load(3)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
d = np.abs(hsv[..., 0] - 48); a = np.maximum(np.clip((d - 5) / 4, 0, 1), np.clip((55 - hsv[..., 1]) / 25, 0, 1))
img = despill(img, a)
for n, box in {"zettel1": (45, 75, 625, 810), "zettel2": (415, 1000, 1025, 1730)}.items():
    save(n, img, part(img, a, box))

# ---------- Zeitungsseite (g05) für den Wisch-Übergang ----------
img, a = keyed(5, smin=30)
a = clean(a)
ys, xs = np.where(a > 0.5); bx0, by0, bw, bh = xs.min(), ys.min(), xs.max() - xs.min(), 2300 - ys.min()
px0, px1, py0, py1 = bx0 + int(.85 * bw), bx0 + int(.95 * bw), by0 + int(.76 * bh), 2300
img[py0:py1, px0:px1] = img[py0:py1, px0 - int(.13 * bw):px1 - int(.13 * bw)]
save("zeitung", img, a, box=(0, 0, 1440, 2300), maxh=1900)

# ---------- Hintergrund-Karton (g01) ----------
img = cv2.imread("src/g01.png")
bg = img[900:4300, 300:2213]
bg = cv2.resize(bg, (1080, 1920), interpolation=cv2.INTER_AREA)
cv2.imwrite(f"{OUT}/karton.jpg", bg, [cv2.IMWRITE_JPEG_QUALITY, 90])
print("karton.jpg     1080x1920")
