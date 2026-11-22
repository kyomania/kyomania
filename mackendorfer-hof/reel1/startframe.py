"""Startbild fuer die KI-Kartenanimation: Deutschland, schwarz-gold, Niedersachsen rot, leicht geneigt. 1920x1080."""
import json, math, os
from PIL import Image, ImageDraw, ImageFilter
SRC = os.path.join(os.path.dirname(__file__), "src")
W, H, SS = 1920, 1080, 2
CW, CH = W * SS, int(H * SS * 1.25)
feats = json.load(open(os.path.join(SRC, "de.json")))["features"]
cosl = math.cos(math.radians(51.2)); s = CH / 9.6
def P(lon, lat): return (CW / 2 + (lon - 10.45) * s * cosl, CH / 2 - (lat - 51.15) * s)
base = Image.new("RGB", (CW, CH), (8, 7, 7))
glow = Image.new("L", (CW, CH), 0)
d = ImageDraw.Draw(base); g = ImageDraw.Draw(glow)
rings = []
for f in feats:
    gm = f["geometry"]; nm = f["properties"]["name"]
    for poly in ([gm["coordinates"]] if gm["type"] == "Polygon" else gm["coordinates"]):
        pts = [P(*c) for c in poly[0]]; rings.append((nm, pts))
        d.polygon(pts, fill=(22, 18, 16))
        if nm == "Niedersachsen": g.polygon(pts, fill=255)
red = Image.new("RGB", (CW, CH), (95, 22, 30))
base = Image.composite(red, base, glow.filter(ImageFilter.GaussianBlur(30)).point(lambda v: int(v * 0.75)))
# Gold-Linien mit Glow
lines = Image.new("L", (CW, CH), 0); L = ImageDraw.Draw(lines)
for nm, pts in rings: L.line(pts + [pts[0]], fill=255, width=3)
gold = Image.new("RGB", (CW, CH), (190, 150, 92))
base = Image.composite(gold, base, lines.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.5)))
base = Image.composite(gold, base, lines)
# Stadtlichter
d = ImageDraw.Draw(base)
for lon, lat, r in [(9.99,53.55,7),(13.40,52.52,8),(9.73,52.37,6),(11.58,48.14,7),(6.96,50.94,7),(8.68,50.11,6),(9.18,48.78,6),(13.74,51.05,5),(12.37,51.34,5),(10.52,52.27,4),(10.79,52.42,4),(11.63,52.12,4),(8.80,53.08,5),(7.47,51.51,5),(6.78,51.23,5),(11.08,49.45,5),(8.47,49.49,4)]:
    x, y = P(lon, lat)
    d.ellipse([x-r*3, y-r*3, x+r*3, y+r*3], fill=(60, 45, 28)); d.ellipse([x-r, y-r, x+r, y+r], fill=(255, 214, 150))
# Neigung (Perspektive): oben schmaler
def coeffs(src, dst):
    import numpy as np
    A=[];B=[]
    for (x,y),(u,v) in zip(dst,src):
        A+= [[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]; B+=[u,v]
    return list(np.linalg.solve(np.array(A,float),np.array(B,float)))
k = 0.16
src = [(0,0),(CW,0),(CW,CH),(0,CH)]
dst = [(CW*k,0),(CW*(1-k),0),(CW,CH),(0,CH)]
base = base.transform((CW, CH), Image.PERSPECTIVE, coeffs(src, dst), Image.BICUBIC, fillcolor=(8,7,7))
base = base.resize((W, int(CH / SS)), Image.LANCZOS).crop((0, int((CH/SS - H) * 0.45), W, int((CH/SS - H) * 0.45) + H))
vig = Image.new("L", (W, H), 0); ImageDraw.Draw(vig).ellipse([-W*.2,-H*.35,W*1.2,H*1.35], fill=255)
base = Image.composite(base, Image.new("RGB",(W,H),(0,0,0)), vig.filter(ImageFilter.GaussianBlur(180)))
base.save(os.path.join(os.path.dirname(__file__), "frames", "start-frame.png"))
