#!/usr/bin/env python3
"""Generates the HyperFrames scene files for the fast.site diner spot.

Shared pieces (fonts, brand mark) live here so every scene stays consistent.
Run: python3 build.py  (rewrites compositions/*.html)
"""
from pathlib import Path
import re

ROOT = Path(__file__).parent
COMP = ROOT / "compositions"
COMP.mkdir(exist_ok=True)

INK = "#101827"
BLUE = "#3158EB"
B_BLUE, B_GREEN, B_RED, B_YELLOW = "#3e71b6", "#0c9958", "#df482b", "#fbb419"
MUTED = "#73737F"

FONTS = """
@font-face { font-family: 'Google Sans Flex'; src: url('assets/fonts/google-sans-flex-latin-v22.woff2') format('woff2'); font-weight: 100 900; }
@font-face { font-family: 'Bricolage Grotesque'; src: url('assets/fonts/bricolage-grotesque-latin-v9.woff2') format('woff2'); font-weight: 200 800; }
"""

# The real fast.site mark (from the site's own SVG), split into its four arms so each can move.
_SRC = (ROOT / "capture/assets/svgs/logo-b6b5fa8e.svg").read_text()
ARM_PATH = re.search(r'fill="#0c9958" d="([^"]+)"', _SRC).group(1)
SHADE_PATH = "M119.15,27.75l-.38,2.19-6.17,35.46c-6.95-6.95-18.25-6.95-25.21,0l-1.31,1.31-5.36-1.31,16.1-15.78,22.34-21.88Z"
R_RIGHT = 'x="67.38" y="38.45" width="129.64" height="38.56" rx="19.28" transform="translate(79.54 -76.57) rotate(45)"'
R_LEFT = 'x="2.98" y="38.45" width="129.64" height="38.56" rx="19.28" transform="translate(-20.97 64.85) rotate(-45)"'


def mark_svg(prefix: str) -> str:
    """Inline mark with four individually addressable arms: {prefix}-ur/-ul/-lr/-ll."""
    def chevron(dy, right, shade, left, ids):
        return f"""<g transform="translate(0 {dy})">
      <g id="{prefix}-{ids[0]}" class="arm"><path fill="{right}" d="{ARM_PATH}"/><rect fill="{right}" {R_RIGHT}/><path fill="{shade}" d="{SHADE_PATH}"/></g>
      <g id="{prefix}-{ids[1]}" class="arm"><rect fill="{left}" {R_LEFT}/></g>
    </g>"""
    return f"""<svg class="mark" viewBox="-40 -40 280 280" xmlns="http://www.w3.org/2000/svg">
    {chevron(0, B_GREEN, '#047844', B_BLUE, ('ur', 'ul'))}
    {chevron(84.53, B_YELLOW, '#d99e28', B_RED, ('lr', 'll'))}
  </svg>"""


def scene(cid: str, css: str, body: str, js: str) -> str:
    return f"""<template>
  <style>
    {FONTS}
    #root {{ position: absolute; inset: 0; background: #ffffff; overflow: hidden; font-family: 'Google Sans Flex', sans-serif; color: {INK}; }}
    .abs {{ position: absolute; }}
    .eyebrow {{ font-family: 'Google Sans Flex'; font-weight: 600; font-size: 30px; letter-spacing: 0.14em; color: {BLUE}; text-transform: uppercase; }}
    .h {{ font-family: 'Bricolage Grotesque'; font-weight: 600; letter-spacing: -0.03em; line-height: 1.02; }}
    {css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080">
    {body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


# Exactly the layout of frames/brand_end.png (the phone screen, full frame):
# a flex column centred in 1920x1080, mark 300px, gap 10px, "Fast.site" 150px/600.
LOCKUP_CSS = """
    .lockup { position: absolute; inset: 0; transform: scale(0.93); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; }
    .lockup .mark { width: 300px; height: 300px; overflow: visible; }
    .lockup .word { font-family: 'Google Sans Flex'; font-weight: 600; font-size: 150px; color: #101827; letter-spacing: -0.02em; line-height: 1; }
"""

# ---------------------------------------------------------------- 1 hero (4.0 s)
hero = scene(
    "hero",
    LOCKUP_CSS + f"""
    #hero-head {{ left: 0; right: 0; top: 380px; text-align: center; font-size: 128px; }}
    #hero-head .w {{ display: inline-block; }}
    #hero-sub {{ left: 0; right: 0; top: 520px; text-align: center; font-size: 128px; color: {BLUE}; }}
    #hero-bar {{ left: 560px; top: 760px; width: 800px; height: 14px; border-radius: 7px; background: #E2E8F0; overflow: hidden; }}
    #hero-fill {{ width: 100%; height: 100%; border-radius: 7px; background: linear-gradient(90deg,{B_BLUE},{B_GREEN},{B_YELLOW},{B_RED}); transform-origin: 0 50%; }}
    #hero-ms {{ left: 560px; top: 795px; width: 800px; display: flex; justify-content: space-between; font-size: 28px; color: {MUTED}; font-weight: 500; }}
    #hero-ms b {{ color: {INK}; }}
""",
    f"""<div id="hero-lock" class="lockup">{mark_svg('hm')}<div id="hero-word" class="word">Fast.site</div></div>
    <div id="hero-head" class="abs h"><span class="w">Mach</span> <span class="w">deine</span> <span class="w">Website</span> <span class="w">schneller.</span></div>
    <div id="hero-sub" class="abs h">Behalte dein Hosting.</div>
    <div id="hero-bar" class="abs"><div id="hero-fill"></div></div>
    <div id="hero-ms" class="abs"><span>Seite lädt …</span><b id="hero-done">Fertig.</b></div>""",
    """
    // lockup lifts away as a unit: mark flies up, word blurs out
    tl.fromTo("#hero-word", { opacity: 1, filter: "blur(0px)" }, { opacity: 0, filter: "blur(10px)", duration: 0.25, ease: "power2.in" }, 0.35);
    tl.fromTo("#hero-lock .mark", { y: 0, scale: 1 }, { y: -330, scale: 0.42, duration: 0.6, ease: "expo.inOut" }, 0.35);
    tl.fromTo("#hero-head .w", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.16, stagger: 0.09, ease: "power3.out" }, 0.75);
    tl.fromTo("#hero-sub", { opacity: 0, y: 30, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }, 1.75);
    tl.fromTo("#hero-bar, #hero-ms", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 2.3);
    tl.fromTo("#hero-fill", { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "expo.out" }, 2.5);
    tl.fromTo("#hero-done", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, 2.85);
    // exit: everything whips left
    tl.to("#hero-head, #hero-sub, #hero-bar, #hero-ms, #hero-lock", { x: -260, opacity: 0, filter: "blur(10px)", duration: 0.3, ease: "power3.in" }, 4.38);
""",
)

# ---------------------------------------------------------------- 2 cache (4.5 s)
regions = [("Nordamerika", 900, 470), ("Europa", 1120, 400), ("Asien", 1330, 500), ("Südamerika", 1010, 680)]
nodes = "".join(
    f'<div id="cn-{i}" class="abs node" style="left:{x-26}px;top:{y-26}px"><i></i><span>{n}</span></div>' for i, (n, x, y) in enumerate(regions)
)
links = "".join(
    f'<line id="cl-{i}" x1="560" y1="600" x2="{x}" y2="{y}" pathLength="1"/>' for i, (_, x, y) in enumerate(regions)
)
visitors = [(1640, 400), (1720, 560), (1660, 720), (1740, 880)]
vis = "".join(f'<div id="cv-{i}" class="abs vis" style="left:{x-36}px;top:{y-36}px">👤</div>' for i, (x, y) in enumerate(visitors))
# each visitor served by nearest edge
pairs = [(0, 0), (2, 1), (1, 2), (3, 3)]
vlinks = "".join(
    f'<line id="cvl-{k}" x1="{regions[r][1]}" y1="{regions[r][2]}" x2="{visitors[v][0]}" y2="{visitors[v][1]}" pathLength="1"/>' for k, (r, v) in enumerate(pairs)
)
packets = "".join(f'<circle id="cp-{k}" r="9" cx="0" cy="0"/>' for k in range(len(pairs) * 3))
pk_js = []
for k, (r, v) in enumerate(pairs):
    x1, y1 = regions[r][1], regions[r][2]
    x2, y2 = visitors[v]
    for j in range(3):
        t0 = 2.0 + k * 0.1 + j * 0.38
        pk_js.append(
            f'tl.fromTo("#cp-{k*3+j}", {{ attr: {{ cx: {x1}, cy: {y1} }}, opacity: 1 }}, {{ attr: {{ cx: {x2}, cy: {y2} }}, duration: 0.32, ease: "power2.in" }}, {t0:.2f});'
            f'tl.to("#cp-{k*3+j}", {{ opacity: 0, duration: 0.05 }}, {t0+0.32:.2f});'
        )
cache = scene(
    "cache",
    f"""
    #c-eb {{ left: 140px; top: 120px; }}
    #c-h {{ left: 140px; top: 170px; font-size: 76px; }}
    #c-h em {{ font-style: normal; color: {BLUE}; }}
    #c-srv {{ left: 280px; top: 510px; width: 280px; height: 180px; border-radius: 22px; background: #F7F7F8; border: 2px solid #E2E8F0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; font-size: 26px; font-weight: 600; }}
    #c-srv small {{ font-size: 28px; color: {MUTED}; font-weight: 500; }}
    .node {{ width: 52px; height: 52px; }}
    .node i {{ position: absolute; inset: 0; border-radius: 50%; background: {B_GREEN}; box-shadow: 0 0 0 10px rgba(12,153,88,.15); }}
    .node span {{ position: absolute; top: 60px; left: 50%; transform: translateX(-50%); white-space: nowrap; font-size: 28px; font-weight: 600; color: {INK}; }}
    .vis {{ width: 72px; height: 72px; border-radius: 50%; background: #EEF2FF; border: 3px solid {BLUE}; }}
    .vis::after {{ content: ""; position: absolute; left: 22px; top: 14px; width: 22px; height: 22px; border-radius: 50%; background: {BLUE}; box-shadow: 0 26px 0 6px {BLUE}; clip-path: inset(0 -20px -12px -20px); }}
    #c-svg {{ left: 0; top: 0; width: 1920px; height: 1080px; }}
    #c-svg line {{ stroke-width: 3; fill: none; }}
    #c-svg .up line {{ stroke: #CBD5E1; stroke-dasharray: 1; }}
    #c-svg .down line {{ stroke: {B_GREEN}; stroke-dasharray: 1; opacity: .55; }}
    #c-svg circle {{ fill: {B_GREEN}; opacity: 0; }}
    #c-tag {{ left: 280px; top: 860px; padding: 16px 28px; border-radius: 999px; background: #ECFDF5; color: #047844; font-size: 30px; font-weight: 600; }}
""",
    f"""<div id="c-eb" class="abs eyebrow">Edge-Caching &amp; CDN</div>
    <div id="c-h" class="abs h">Deine Seiten kommen <em>von nebenan.</em></div>
    <svg id="c-svg" class="abs" viewBox="0 0 1920 1080"><g class="up">{links}</g><g class="down">{vlinks}</g>{packets}</svg>
    <div id="c-srv" class="abs"><span>Dein Hosting</span><small>bleibt, wie es ist</small></div>
    {nodes}{vis}
    <div id="c-tag" class="abs">Gecacht am Edge – nah am Besucher</div>""",
    """
    tl.fromTo("#c-eb", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2 }, 0.0);
    tl.fromTo("#c-h", { opacity: 0, x: 120, filter: "blur(10px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }, 0.05);
    tl.fromTo("#c-srv", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }, 0.35);
    tl.fromTo("#c-svg .up line", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.5, stagger: 0.08, ease: "power2.out" }, 0.7);
    tl.fromTo(".node", { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, duration: 0.35, stagger: 0.08, ease: "back.out(2)" }, 1.0);
    tl.fromTo(".vis", { opacity: 0, x: 40 }, { opacity: 1, x: 0, duration: 0.35, stagger: 0.07, ease: "expo.out" }, 1.4);
    tl.fromTo("#c-svg .down line", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.35, stagger: 0.07, ease: "power2.out" }, 1.75);
    
    """ + "\n    ".join(pk_js) + """
    tl.fromTo("#c-tag", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, 1.9);
    tl.to("#root > *", { y: -220, opacity: 0, filter: "blur(10px)", duration: 0.3, ease: "power3.in" }, 3.58);
""",
)

# ---------------------------------------------------------------- 3 images (4.0 s)
images = scene(
    "images",
    f"""
    #i-eb {{ left: 140px; top: 120px; }}
    #i-h {{ left: 140px; top: 170px; font-size: 76px; }}
    #i-card {{ left: 140px; top: 360px; width: 1020px; height: 560px; border-radius: 28px; overflow: hidden; box-shadow: 0 30px 80px rgba(16,24,39,.18); }}
    #i-card img {{ width: 100%; height: 100%; object-fit: cover; }}
    #i-fmt {{ left: 170px; top: 390px; padding: 10px 20px; border-radius: 999px; background: rgba(255,255,255,.92); font-size: 30px; font-weight: 700; }}
    #i-panel {{ left: 1240px; top: 380px; width: 540px; }}
    #i-panel .lbl {{ font-size: 28px; color: {MUTED}; font-weight: 500; }}
    #i-kb {{ font-family: 'Bricolage Grotesque'; font-size: 132px; font-weight: 600; letter-spacing: -0.03em; margin-top: 6px; }}
    #i-track {{ margin-top: 20px; height: 18px; border-radius: 9px; background: #E2E8F0; overflow: hidden; }}
    #i-size {{ height: 100%; width: 100%; background: {MUTED}; border-radius: 9px; transform-origin: 0 50%; }}
    #i-badge {{ margin-top: 40px; display: inline-block; padding: 16px 30px; border-radius: 999px; background: #ECFDF5; color: #047844; font-size: 44px; font-weight: 700; }}
    #i-note {{ left: 140px; top: 950px; font-size: 28px; color: {MUTED}; }}
""",
    f"""<div id="i-eb" class="abs eyebrow">Bildoptimierung</div>
    <div id="i-h" class="abs h">Schnellere Bilder. Ganz automatisch.</div>
    <div id="i-card" class="abs"><img id="i-img" src="assets/img/wiese.jpg" alt=""></div>
    <div id="i-fmt" class="abs">Original JPG</div>
    <div id="i-panel" class="abs"><div class="lbl">Dateigröße</div><div id="i-kb">303,4 KB</div><div id="i-track"><div id="i-size"></div></div><div id="i-badge">−35 % · WebP</div></div>
    <div id="i-note" class="abs">Beispielbild von fast.site · Ersparnis je nach Bild</div>""",
    """
    tl.fromTo("#i-eb", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 0.0);
    tl.fromTo("#i-h", { opacity: 0, y: 140, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }, 0.05);
    tl.fromTo("#i-card", { opacity: 0, scale: 1.08, clipPath: "inset(0 100% 0 0 round 28px)" }, { opacity: 1, scale: 1, clipPath: "inset(0 0% 0 0 round 28px)", duration: 0.6, ease: "expo.out" }, 0.3);
    tl.fromTo("#i-fmt, #i-panel", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, ease: "expo.out", stagger: 0.08 }, 0.7);
    // the conversion: count 303,4 -> 198,2 while the bar shrinks and the label flips
    const kb = { v: 303.4 };
    tl.fromTo(kb, { v: 303.4 }, { v: 198.2, duration: 0.9, ease: "power3.inOut", onUpdate: () => {
      document.querySelector("#i-kb").textContent = kb.v.toFixed(1).replace(".", ",") + " KB";
    } }, 1.3);
    tl.fromTo("#i-size", { scaleX: 1, backgroundColor: "#73737F" }, { scaleX: 0.653, backgroundColor: "#0c9958", duration: 0.9, ease: "power3.inOut" }, 1.3);
    tl.call(() => { document.querySelector("#i-fmt").textContent = "Schnelles WebP"; }, null, 1.95);
    tl.call(() => { document.querySelector("#i-fmt").textContent = "Original JPG"; }, null, 1.94);
    tl.fromTo("#i-badge", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.2)" }, 2.15);
    tl.fromTo("#i-note", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 1.0);
    tl.to("#root > *", { x: 260, opacity: 0, filter: "blur(10px)", duration: 0.3, ease: "power3.in" }, 3.98);
""",
)

# ---------------------------------------------------------------- 4 ddos (3.5 s)
import math
shots = []
dots = ""
rings = ""
for k in range(14):
    ang = (k * 137.5) % 360
    rad = math.radians(ang)
    sx, sy = 960 + math.cos(rad) * 1150, 560 + math.sin(rad) * 700
    ex, ey = 960 + math.cos(rad) * 250, 560 + math.sin(rad) * 250
    bx, by = 960 + math.cos(rad) * 330, 560 + math.sin(rad) * 330
    t0 = 0.45 + k * 0.095
    dots += f'<circle id="dd-{k}" r="13" cx="{sx:.0f}" cy="{sy:.0f}"/>'
    rings += f'<div id="d-ring-{k}" class="abs dring"></div>'
    shots.append(
        f'tl.fromTo("#dd-{k}", {{ attr: {{ cx: {sx:.0f}, cy: {sy:.0f} }}, opacity: 1, scale: 1 }}, {{ attr: {{ cx: {ex:.0f}, cy: {ey:.0f} }}, duration: 0.3, ease: "power2.in" }}, {t0:.2f});'
        f'tl.to("#dd-{k}", {{ attr: {{ cx: {bx:.0f}, cy: {by:.0f} }}, opacity: 0, duration: 0.25, ease: "power2.out" }}, {t0+0.3:.2f});'
        f'tl.fromTo("#d-ring-{k}", {{ scale: 1, opacity: .9 }}, {{ scale: 1.12, opacity: 0, duration: 0.3, ease: "power2.out" }}, {t0+0.3:.2f});'
    )
ddos = scene(
    "ddos",
    f"""
    #d-eb {{ left: 0; right: 0; top: 110px; text-align: center; }}
    #d-h {{ left: 0; right: 0; top: 160px; text-align: center; font-size: 76px; }}
    #d-svg {{ left: 0; top: 0; width: 1920px; height: 1080px; }}
    #d-svg circle {{ fill: {B_RED}; opacity: 0; }}
    #d-shield {{ left: 810px; top: 410px; width: 300px; height: 300px; }}
    #d-root-unused {{ left: 0; }}
    .dring {{ left: 700px; opacity: 0; top: 300px; width: 520px; height: 520px; border-radius: 50%; border: 6px solid {B_BLUE}; }}
    #d-ok {{ left: 0; right: 0; top: 860px; text-align: center; }}
    #d-ok span {{ display: inline-flex; align-items: center; gap: 14px; padding: 16px 30px; border-radius: 999px; background: #ECFDF5; color: #047844; font-size: 32px; font-weight: 700; }}
    #d-ok i {{ width: 16px; height: 16px; border-radius: 50%; background: {B_GREEN}; }}
""",
    f"""<div id="d-eb" class="abs eyebrow">DDoS-Schutz</div>
    <div id="d-h" class="abs h">Angriffe prallen ab.</div>
    <svg id="d-svg" class="abs" viewBox="0 0 1920 1080">{dots}</svg>
    {rings}
    <svg id="d-shield" class="abs" viewBox="0 0 100 100"><path d="M50 6 L88 20 V48 C88 72 70 88 50 95 C30 88 12 72 12 48 V20 Z" fill="{B_BLUE}"/><path d="M33 50 L45 62 L68 38" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <div id="d-ok" class="abs"><span><i></i>Website online</span></div>""",
    """
        tl.fromTo("#d-eb", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 0.0);
    tl.fromTo("#d-h", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2 }, 0.05);
    tl.fromTo("#d-shield", { scale: 0, rotation: -20 }, { scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }, 0.15);
    """ + "\n    ".join(shots) + """
    tl.fromTo("#d-ok", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, 1.3);
    tl.to("#root > *", { scale: 0.9, opacity: 0, filter: "blur(10px)", duration: 0.3, ease: "power3.in" }, 2.38);
""",
)

# ---------------------------------------------------------------- 5 setup + return to lockup (4.0 s)
platforms = ["WordPress", "WooCommerce", "Shopware", "Shopify", "Magento", "TYPO3"]
plat = "".join(f'<span class="pl">{p}</span>' for p in platforms)
setup = scene(
    "setup",
    LOCKUP_CSS + f"""
    #s-eb {{ left: 0; right: 0; top: 260px; text-align: center; }}
    #s-h {{ left: 0; right: 0; top: 310px; text-align: center; font-size: 84px; }}
    #s-form {{ left: 460px; top: 500px; width: 1000px; height: 120px; border-radius: 26px; border: 3px solid #E2E8F0; background: #fff; display: flex; align-items: center; padding: 0 14px 0 40px; box-shadow: 0 20px 60px rgba(16,24,39,.10); }}
    #s-in {{ flex: 1; font-size: 44px; font-weight: 500; color: {INK}; white-space: nowrap; overflow: hidden; }}
    #s-btn {{ height: 90px; padding: 0 40px; border-radius: 18px; background: {BLUE}; color: #fff; font-size: 34px; font-weight: 700; display: flex; align-items: center; gap: 12px; }}
    #s-lock {{ opacity: 0; }}
    #s-ok {{ left: 0; right: 0; top: 660px; text-align: center; font-size: 34px; font-weight: 700; color: #047844; }}
    #s-pl {{ left: 0; right: 0; top: 770px; display: flex; justify-content: center; gap: 18px; }}
    .pl {{ padding: 14px 26px; border-radius: 999px; background: #F7F7F8; border: 2px solid #E2E8F0; font-size: 28px; font-weight: 600; }}
    #s-cta {{ left: 0; right: 0; top: 900px; text-align: center; font-size: 40px; font-weight: 700; color: {BLUE}; }}
""",
    f"""<div id="s-eb" class="abs eyebrow">Einrichtung</div>
    <div id="s-h" class="abs h">Domain verbinden. Fertig.</div>
    <div id="s-form" class="abs"><div id="s-in"></div><div id="s-btn">Verbinden ↗</div></div>
    <div id="s-ok" class="abs">✓ Beschleunigung aktiv</div>
    <div id="s-pl" class="abs">{plat}</div>
    <div id="s-cta" class="abs">7 Tage kostenlos testen · keine Kreditkarte</div>
    <div id="s-lock" class="lockup">{mark_svg('sm')}<div id="s-word" class="word">Fast.site</div></div>""",
    """
    const domain = "deinedomain.de";
        tl.fromTo("#s-eb", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 0.0);
    tl.fromTo("#s-h", { opacity: 0, y: -40, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }, 0.05);
    tl.fromTo("#s-form", { opacity: 0, scaleX: 0.3 }, { opacity: 1, scaleX: 1, duration: 0.45, ease: "expo.out" }, 0.2);
    const typed = { n: 0 };
    tl.fromTo(typed, { n: 0 }, { n: domain.length, duration: 0.6, ease: "none", onUpdate: () => {
      document.querySelector("#s-in").textContent = domain.slice(0, Math.round(typed.n));
    } }, 0.55);
    tl.fromTo("#s-btn", { scale: 1 }, { scale: 0.92, duration: 0.08, ease: "power2.in" }, 1.25);
    tl.to("#s-btn", { scale: 1, backgroundColor: "#0c9958", duration: 0.25, ease: "back.out(3)" }, 1.33);
    tl.fromTo("#s-ok", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, 1.4);
    tl.fromTo(".pl", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, stagger: 0.06, ease: "expo.out" }, 1.55);
    tl.fromTo("#s-cta", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 1.8);
    // everything collapses into the centre and the lockup lands on exactly the phone-screen frame
    tl.to("#s-eb, #s-h, #s-form, #s-ok, #s-pl, #s-cta", { scale: 0.2, opacity: 0, filter: "blur(12px)", duration: 0.35, ease: "power3.in", transformOrigin: "50% 50%" }, 3.7);
    tl.fromTo("#s-lock", { opacity: 0 }, { opacity: 1, duration: 0.01 }, 4.0);
    tl.fromTo("#sm-ur, #sm-ul, #sm-lr, #sm-ll", { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.35, ease: "back.out(1.6)", stagger: 0.04 }, 4.0);
    tl.fromTo("#s-word", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2 }, 4.15);
""",
)

# ---------------------------------------------------------------- endcard (4.0 s)
endcard = scene(
    "endcard",
    f"""
    #e-wrap {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; gap: 36px; }}
    #e-wrap .mark {{ width: 260px; height: 260px; overflow: visible; }}
    #e-word {{ font-family: 'Google Sans Flex'; font-weight: 600; font-size: 170px; letter-spacing: -0.02em; line-height: 1; clip-path: inset(0 100% 0 0); }}
    #e-cta {{ left: 0; right: 0; top: 760px; display: flex; justify-content: center; align-items: center; gap: 28px; }}
    #e-btn {{ padding: 22px 44px; border-radius: 18px; background: {BLUE}; color: #fff; font-size: 38px; font-weight: 700; }}
    #e-sub {{ font-size: 30px; color: {MUTED}; font-weight: 500; }}
    #e-line {{ left: 0; right: 0; bottom: 0; height: 10px; background: linear-gradient(90deg,{B_BLUE},{B_GREEN},{B_YELLOW},{B_RED}); transform-origin: 0 50%; }}
""",
    f"""<div id="e-wrap">{mark_svg('em')}<div id="e-word">Fast.site</div></div>
    <div id="e-cta" class="abs"><div id="e-btn">Kostenlos testen ↗</div><div id="e-sub">7 Tage · keine Kreditkarte</div></div>
    <div id="e-line" class="abs"></div>""",
    """
    // four arms fly in from four corners and snap together
    tl.fromTo("#em-ul", { x: -900, y: -500, rotation: -90, opacity: 0 }, { x: 0, y: 0, rotation: 0, opacity: 1, duration: 0.55, ease: "expo.out" }, 0.10);
    tl.fromTo("#em-ur", { x: 900, y: -500, rotation: 90, opacity: 0 }, { x: 0, y: 0, rotation: 0, opacity: 1, duration: 0.55, ease: "expo.out" }, 0.18);
    tl.fromTo("#em-ll", { x: -900, y: 600, rotation: 90, opacity: 0 }, { x: 0, y: 0, rotation: 0, opacity: 1, duration: 0.55, ease: "expo.out" }, 0.26);
    tl.fromTo("#em-lr", { x: 900, y: 600, rotation: -90, opacity: 0 }, { x: 0, y: 0, rotation: 0, opacity: 1, duration: 0.55, ease: "expo.out" }, 0.34);
    // the snap: a quick upward kick, like the arrow it is
    tl.fromTo("#e-wrap .mark", { y: 0 }, { y: -26, duration: 0.12, ease: "power2.out" }, 0.86);
    tl.to("#e-wrap .mark", { y: 0, duration: 0.4, ease: "back.out(3)" }, 0.98);
    tl.fromTo("#e-word", { clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)", duration: 0.5, ease: "expo.out" }, 1.0);
    tl.fromTo("#e-cta", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: "expo.out" }, 1.45);
    tl.fromTo("#e-line", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "expo.out" }, 1.45);
""",
)

for name, html in [("hero", hero), ("cache", cache), ("images", images), ("ddos", ddos), ("setup", setup), ("endcard", endcard)]:
    (COMP / f"{name}.html").write_text(html)
print("ok")
