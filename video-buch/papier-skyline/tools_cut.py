"""Stellt die Seedream-Bilder frei (Hintergrund-Key) und zerlegt sie in Einzelteile.

python3 tools_cut.py           -> cut/gNN_kK.png (+ cut/sheet_gNN.jpg zum Auswählen)
"""
import sys, os, cv2, numpy as np
from scipy import ndimage as ndi

SRC, OUT = "src", "cut"
os.makedirs(OUT, exist_ok=True)
HALF = (1440, 2560)


def key(img, tol_in=5.0, tol_out=9.0, smin=45):
    """Alpha = 0 wo Farbton nahe am Hintergrund und gesättigt. Weiche Kante dazwischen."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    H, S = hsv[..., 0], hsv[..., 1]
    b = np.concatenate([hsv[:12].reshape(-1, 3), hsv[-12:].reshape(-1, 3), hsv[:, :12].reshape(-1, 3), hsv[:, -12:].reshape(-1, 3)])
    b = b[b[:, 1] > smin]
    hb = np.median(b[:, 0])
    d = np.abs(H - hb); d = np.minimum(d, 180 - d)
    a_h = np.clip((d - tol_in) / (tol_out - tol_in), 0, 1)
    a_s = np.clip((smin + 25 - S) / 25, 0, 1)          # ungesättigt (weiß/grau/schwarz) = Papier
    a = np.maximum(a_h, a_s)
    return a, hb


def despill(img, a):
    out = img.astype(np.float32)
    B, G, R = out[..., 0], out[..., 1], out[..., 2]
    edge = (a < 0.98)
    lim = np.maximum(R, B)
    G[edge] = np.minimum(G[edge], lim[edge])
    return out.clip(0, 255).astype(np.uint8)


def components(a, min_area):
    m = a > 0.5
    m = ndi.binary_opening(m, iterations=2)
    m = ndi.binary_fill_holes(m)
    lab, n = ndi.label(m)
    objs = ndi.find_objects(lab)
    res = []
    for i, sl in enumerate(objs, 1):
        area = (lab[sl] == i).sum()
        if area >= min_area:
            res.append((i, sl, area))
    return lab, res


def run(idx, min_area=4000, **kw):
    img = cv2.imread(f"{SRC}/g{idx:02d}.png")
    img = cv2.resize(img, HALF, interpolation=cv2.INTER_AREA)
    a, hb = key(img, **kw)
    img = despill(img, a)
    lab, comps = components(a, min_area)
    sheet = img.copy()
    for k, (i, sl, area) in enumerate(comps):
        ys, xs = sl
        pad = 6
        y0, y1 = max(0, ys.start - pad), min(img.shape[0], ys.stop + pad)
        x0, x1 = max(0, xs.start - pad), min(img.shape[1], xs.stop + pad)
        mask = ndi.binary_dilation(lab[y0:y1, x0:x1] == i, iterations=3)
        alpha = (a[y0:y1, x0:x1] * mask * 255).astype(np.uint8)
        rgba = np.dstack([img[y0:y1, x0:x1], alpha])
        cv2.imwrite(f"{OUT}/g{idx:02d}_k{k}.png", rgba)
        cv2.rectangle(sheet, (x0, y0), (x1, y1), (0, 0, 255), 6)
        cv2.putText(sheet, f"k{k}", (x0 + 10, y0 + 70), cv2.FONT_HERSHEY_SIMPLEX, 2.6, (0, 0, 255), 7)
    cv2.imwrite(f"{OUT}/sheet_g{idx:02d}.jpg", cv2.resize(sheet, (540, 960)), [cv2.IMWRITE_JPEG_QUALITY, 80])
    print(f"g{idx:02d}: Hintergrund-H={hb:.0f}, {len(comps)} Teile")


if __name__ == "__main__":
    ids = [int(x) for x in sys.argv[1:]] or [2, 4, 6, 7, 8, 9, 10, 11, 3]
    for i in ids:
        run(i)
