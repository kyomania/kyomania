#!/usr/bin/env python3
"""v2 motion design for the fast.site diner spot: louder, faster, more 'wow'.

Reuses the brand helpers (fonts, real logo mark, lockup) from build.py.
Run: python3 build2.py  (writes compositions/x-*.html)
"""
import math
import json
from pathlib import Path

_src = (Path(__file__).parent / "build.py").read_text()
exec(_src[: _src.index("# ---------------------------------------------------------------- 1 hero")])

NAVY = "#0B1020"
GREEN_DEEP = "#047844"
STREAK_COLORS = [B_BLUE, B_GREEN, B_YELLOW, B_RED]


def det(i, salt=0):
    """Deterministic pseudo-random 0..1 (no Math.random in compositions)."""
    x = math.sin(i * 12.9898 + salt * 78.233) * 43758.5453
    return x - math.floor(x)


# ====================================================================== 1  SPEED (4.6 s)
streaks = "".join(
    f'<div id="xs-st{k}" class="abs streak" style="top:{int(80 + det(k) * 920)}px;height:{int(4 + det(k, 1) * 14)}px;'
    f'width:{int(500 + det(k, 2) * 900)}px;background:{STREAK_COLORS[k % 4]}"></div>'
    for k in range(26)
)
streak_js = "\n    ".join(
    f'tl.fromTo("#xs-st{k}", {{ x: -1600 }}, {{ x: 2400, duration: {0.35 + det(k, 3) * 0.3:.2f}, ease: "power1.in" }}, {0.45 + det(k, 4) * 0.5:.2f});'
    for k in range(26)
)
skel = "".join(f'<i class="sk" style="width:{w}%"></i>' for w in (70, 92, 85, 60, 88, 40))
speed = scene(
    "xspeed",
    LOCKUP_CSS + f"""
    .streak {{ left: 0; border-radius: 99px; opacity: .9; }}
    #xs-pre {{ left: 0; right: 0; top: 250px; text-align: center; font-size: 74px; color: {MUTED}; }}
    #xs-big {{ left: 0; right: 0; top: 320px; text-align: center; font-size: 300px; line-height: 1; letter-spacing: -0.05em; }}
    #xs-big span {{ background: linear-gradient(90deg,{B_BLUE},{B_GREEN} 40%,{B_YELLOW} 70%,{B_RED}); -webkit-background-clip: text; background-clip: text; color: transparent; }}
    .win {{ top: 560px; width: 760px; height: 400px; border-radius: 26px; background: #fff; border: 2px solid #E2E8F0; box-shadow: 0 40px 90px rgba(16,24,39,.16); overflow: hidden; }}
    .win .bar {{ height: 58px; background: #F7F7F8; border-bottom: 2px solid #E2E8F0; display: flex; align-items: center; gap: 10px; padding: 0 22px; }}
    .win .bar b {{ width: 14px; height: 14px; border-radius: 50%; background: #E2E8F0; }}
    .win .lbl {{ margin-left: 14px; font-size: 28px; font-weight: 700; }}
    .win .prog {{ height: 8px; background: #E2E8F0; }}
    .win .prog i {{ display: block; height: 100%; width: 100%; transform-origin: 0 50%; }}
    .win .page {{ padding: 30px 34px; display: flex; flex-direction: column; gap: 16px; }}
    .sk {{ display: block; height: 26px; border-radius: 8px; background: #EEF2F7; }}
    #xs-wa {{ left: 160px; }}
    #xs-wb {{ left: 1000px; }}
    #xs-wa .prog i {{ background: {MUTED}; }}
    #xs-wb .prog i {{ background: linear-gradient(90deg,{B_BLUE},{B_GREEN},{B_YELLOW},{B_RED}); }}
    #xs-spin {{ left: 500px; top: 820px; width: 70px; height: 70px; border-radius: 50%; border: 8px solid #E2E8F0; border-top-color: {MUTED}; }}
    #xs-done {{ left: 1290px; top: 870px; padding: 14px 28px; border-radius: 999px; background: #ECFDF5; color: {GREEN_DEEP}; font-size: 34px; font-weight: 800; }}
    #xs-host {{ left: 0; right: 0; top: 70px; text-align: center; font-size: 96px; color: {BLUE}; }}
""",
    f"""{streaks}
    <div id="xs-lock" class="lockup">{mark_svg('xa')}<div id="xs-word" class="word">Fast.site</div></div>
    <div id="xs-pre" class="abs h">Mach deine Website</div>
    <div id="xs-big" class="abs h"><span>schneller.</span></div>
    <div id="xs-wa" class="abs win"><div class="bar"><b></b><b></b><b></b><span class="lbl">Ohne</span></div><div class="prog"><i id="xs-pa"></i></div><div class="page" id="xs-ga">{skel}</div></div>
    <div id="xs-wb" class="abs win"><div class="bar"><b></b><b></b><b></b><span class="lbl">Mit fast.site</span></div><div class="prog"><i id="xs-pb"></i></div><div class="page" id="xs-gb">{skel}</div></div>
    <div id="xs-spin" class="abs"></div>
    <div id="xs-done" class="abs">Fertig ⚡</div>
    <div id="xs-host" class="abs h">Behalte dein Hosting.</div>""",
    f"""
    // the logo detonates: four arms rocket out of frame, the word smears away
    tl.fromTo("#xs-word", {{ opacity: 1, filter: "blur(0px)", scaleX: 1 }}, {{ opacity: 0, filter: "blur(16px)", scaleX: 1.6, duration: 0.25, ease: "power3.in" }}, 0.3);
    tl.fromTo("#xa-ul", {{ x: 0, y: 0, scale: 1 }}, {{ x: -1400, y: -900, scale: 5, duration: 0.55, ease: "power3.in" }}, 0.32);
    tl.fromTo("#xa-ur", {{ x: 0, y: 0, scale: 1 }}, {{ x: 1400, y: -900, scale: 5, duration: 0.55, ease: "power3.in" }}, 0.34);
    tl.fromTo("#xa-ll", {{ x: 0, y: 0, scale: 1 }}, {{ x: -1400, y: 900, scale: 5, duration: 0.55, ease: "power3.in" }}, 0.36);
    tl.fromTo("#xa-lr", {{ x: 0, y: 0, scale: 1 }}, {{ x: 1400, y: 900, scale: 5, duration: 0.55, ease: "power3.in" }}, 0.38);
    // warp streaks in brand colours
    {streak_js}
    // kinetic type: the word that matters slams in, stretched by its own speed
    tl.fromTo("#xs-pre", {{ opacity: 0, filter: "blur(10px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.18, ease: "power3.out" }}, 0.95);
    tl.fromTo("#xs-big", {{ opacity: 0, x: 900, scaleX: 2.6, filter: "blur(30px)" }}, {{ opacity: 1, x: 0, scaleX: 1, filter: "blur(0px)", duration: 0.42, ease: "expo.out" }}, 1.25);
    tl.fromTo("#root", {{ y: 0 }}, {{ y: 14, duration: 0.05, ease: "none" }}, 1.42);
    tl.to("#root", {{ y: -9, duration: 0.05, ease: "none" }}, 1.47);
    tl.to("#root", {{ y: 4, duration: 0.05, ease: "none" }}, 1.52);
    tl.to("#root", {{ y: 0, duration: 0.08, ease: "none" }}, 1.57);
    // race: same site, two loads
    tl.to("#xs-pre", {{ y: -200, opacity: 0, duration: 0.3, ease: "power3.in" }}, 1.95);
    tl.to("#xs-big", {{ y: -200, scale: 0.55, duration: 0.45, ease: "expo.inOut" }}, 1.95);
    tl.fromTo("#xs-wa", {{ y: 800 }}, {{ y: 0, duration: 0.45, ease: "expo.out" }}, 2.05);
    tl.fromTo("#xs-wb", {{ y: 800 }}, {{ y: 0, duration: 0.45, ease: "expo.out" }}, 2.12);
    tl.fromTo("#xs-pa", {{ scaleX: 0 }}, {{ scaleX: 0.22, duration: 2.0, ease: "power1.out" }}, 2.4);
    tl.fromTo("#xs-pb", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.28, ease: "expo.out" }}, 2.45);
    tl.fromTo("#xs-ga .sk", {{ opacity: 0 }}, {{ opacity: 0, duration: 0.01 }}, 0);
    tl.fromTo("#xs-gb .sk", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.25, stagger: 0.04, ease: "expo.out" }}, 2.6);
    tl.fromTo("#xs-spin", {{ opacity: 0, rotation: 0 }}, {{ opacity: 1, rotation: 900, duration: 2.0, ease: "none" }}, 2.4);
    tl.fromTo("#xs-done", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)" }}, 2.85);
    // "Behalte dein Hosting." takes the top
    tl.to("#xs-big", {{ opacity: 0, filter: "blur(10px)", duration: 0.2 }}, 2.95);
    tl.fromTo("#xs-host", {{ opacity: 0, y: -60, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }}, 3.05);
    // exit into the globe: a navy flood rises from the bottom
    tl.to("#xs-wa, #xs-wb, #xs-spin, #xs-done, #xs-host", {{ y: -300, opacity: 0, duration: 0.35, ease: "power3.in" }}, 4.2);
""",
)
# a navy panel that floods up at the end of SPEED, so the globe scene starts on navy
speed = speed.replace(
    "</div>\n  <script>",
    f'<div id="xs-flood" class="abs" style="left:0;top:0;width:1920px;height:1080px;background:{NAVY};transform-origin:50% 100%"></div>\n  </div>\n  <script>',
    1,
).replace(
    "    window.__timelines[\"xspeed\"] = tl;",
    '    tl.fromTo("#xs-flood", { scaleY: 0 }, { scaleY: 1, duration: 0.4, ease: "power3.inOut" }, 4.2);\n    window.__timelines["xspeed"] = tl;',
)

# ====================================================================== 2  GLOBE (3.9 s)
N = 520
golden = math.pi * (3 - math.sqrt(5))
pts = []
for i in range(N):
    y = 1 - (i / (N - 1)) * 2
    r = math.sqrt(1 - y * y)
    th = golden * i
    pts.append((round(math.cos(th) * r, 4), round(y, 4), round(math.sin(th) * r, 4)))


def ll(lat, lon):
    la, lo = math.radians(lat), math.radians(lon)
    return (round(math.cos(la) * math.cos(lo), 4), round(math.sin(la), 4), round(math.cos(la) * math.sin(lo), 4))


edges = [("Nordamerika", ll(40, -100), B_BLUE), ("Südamerika", ll(-15, -60), B_GREEN), ("Europa", ll(50, 10), B_YELLOW), ("Asien", ll(30, 100), B_RED)]
users = [ll(det(i, 7) * 120 - 50, det(i, 8) * 360 - 180) for i in range(26)]
# each user is served by the nearest edge
def nearest(u):
    return min(range(4), key=lambda e: sum((u[k] - edges[e][1][k]) ** 2 for k in range(3)))
arcs = [(nearest(u), u) for u in users]
dots = "".join(f'<circle class="gd" r="3.2"/>' for _ in pts)
edge_svg = "".join(f'<g class="ge"><circle r="34" fill="{c}" opacity=".25"/><circle r="14" fill="{c}"/></g>' for _, _, c in edges)
arc_svg = "".join(f'<polyline class="ga" stroke="{edges[e][2]}"/>' for e, _ in arcs)
user_svg = "".join('<circle class="gu" r="7"/>' for _ in arcs)
globe = scene(
    "xglobe",
    f"""
    #root {{ background: {NAVY}; color: #fff; }}
    #xg-svg {{ left: 0; top: 0; width: 1920px; height: 1080px; }}
    .gd {{ fill: #8FA3C7; }}
    .ga {{ fill: none; stroke-width: 4; stroke-linecap: round; }}
    .gu {{ fill: #fff; }}
    #xg-eb {{ left: 140px; top: 300px; color: #7FA6FF; }}
    #xg-h {{ left: 140px; top: 350px; font-size: 104px; width: 760px; }}
    #xg-h em {{ font-style: normal; color: {B_GREEN}; }}
    #xg-pills {{ left: 140px; top: 720px; display: flex; flex-wrap: wrap; gap: 14px; width: 700px; }}
    #xg-pills span {{ padding: 12px 24px; border-radius: 999px; border: 2px solid rgba(255,255,255,.18); font-size: 28px; font-weight: 600; display: inline-flex; gap: 10px; align-items: center; }}
    #xg-pills i {{ width: 14px; height: 14px; border-radius: 50%; }}
""",
    f"""<svg id="xg-svg" class="abs" viewBox="0 0 1920 1080"><g id="xg-g">{dots}{arc_svg}{user_svg}{edge_svg}</g></svg>
    <div id="xg-eb" class="abs eyebrow">Edge-Caching &amp; CDN</div>
    <div id="xg-h" class="abs h">Ausgeliefert von <em>nebenan.</em></div>
    <div id="xg-pills" class="abs">{''.join(f'<span><i style="background:{c}"></i>{n}</span>' for n, _, c in edges)}</div>""",
    f"""
    const P = {json.dumps(pts)};
    const E = {json.dumps([e[1] for e in edges])};
    const A = {json.dumps([[e, list(u)] for e, u in arcs])};
    const CX = 1290, CY = 560, R = 400;
    const dotEls = document.querySelectorAll("#xg-g .gd");
    const edgeEls = document.querySelectorAll("#xg-g .ge");
    const arcEls = document.querySelectorAll("#xg-g .ga");
    const userEls = document.querySelectorAll("#xg-g .gu");
    function proj(p, a, tilt) {{
      const c = Math.cos(a), s = Math.sin(a);
      let x = p[0] * c - p[2] * s, z = p[0] * s + p[2] * c, y = p[1];
      const ct = Math.cos(tilt), st = Math.sin(tilt);
      const y2 = y * ct - z * st, z2 = y * st + z * ct;
      return [CX + x * R, CY - y2 * R, z2];
    }}
    function slerp(a, b, t) {{
      const d = Math.max(-1, Math.min(1, a[0]*b[0] + a[1]*b[1] + a[2]*b[2]));
      const w = Math.acos(d) || 1e-6, sw = Math.sin(w);
      const k1 = Math.sin((1 - t) * w) / sw, k2 = Math.sin(t * w) / sw, lift = 1 + 0.18 * Math.sin(Math.PI * t);
      return [(a[0]*k1 + b[0]*k2) * lift, (a[1]*k1 + b[1]*k2) * lift, (a[2]*k1 + b[2]*k2) * lift];
    }}
    const st = {{ t: 0 }};
    function render() {{
      const t = st.t, ang = 0.9 + t * 0.55, tilt = 0.32;
      for (let i = 0; i < P.length; i++) {{
        const q = proj(P[i], ang, tilt), el = dotEls[i];
        el.setAttribute("cx", q[0].toFixed(1)); el.setAttribute("cy", q[1].toFixed(1));
        el.setAttribute("opacity", q[2] > 0 ? (0.25 + 0.75 * q[2]).toFixed(2) : "0.06");
      }}
      for (let i = 0; i < E.length; i++) {{
        const q = proj(E[i], ang, tilt);
        edgeEls[i].setAttribute("transform", `translate(${{q[0].toFixed(1)}} ${{q[1].toFixed(1)}}) scale(${{Math.min(1, Math.max(0, (t - 0.35) * 4)) * (1 + 0.15 * Math.sin(t * 9 + i))}})`);
        edgeEls[i].setAttribute("opacity", q[2] > -0.1 ? "1" : "0.15");
      }}
      for (let i = 0; i < A.length; i++) {{
        const prog = Math.max(0, Math.min(1, (t - 0.9 - i * 0.045) / 0.45));
        const src = E[A[i][0]], dst = A[i][1];
        let pts = [];
        const n = Math.max(1, Math.round(prog * 18));
        let vis = true;
        for (let k = 0; k <= n; k++) {{
          const q = proj(slerp(src, dst, (k / 18)), ang, tilt);
          if (q[2] < -0.05) vis = false;
          pts.push(q[0].toFixed(1) + "," + q[1].toFixed(1));
        }}
        arcEls[i].setAttribute("points", prog > 0 ? pts.join(" ") : "");
        arcEls[i].setAttribute("opacity", vis ? "0.95" : "0.12");
        const qd = proj(dst, ang, tilt);
        userEls[i].setAttribute("cx", qd[0].toFixed(1)); userEls[i].setAttribute("cy", qd[1].toFixed(1));
        userEls[i].setAttribute("opacity", qd[2] > 0 && prog >= 1 ? "1" : "0");
      }}
    }}
    tl.fromTo(st, {{ t: 0 }}, {{ t: 3.9, duration: 3.9, ease: "none", onUpdate: render }}, 0);
    tl.fromTo("#xg-svg", {{ scale: 0.6, opacity: 0, transformOrigin: "1290px 560px" }}, {{ scale: 1, opacity: 1, duration: 0.7, ease: "expo.out" }}, 0.05);
    tl.fromTo("#xg-eb", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 0.3);
    tl.fromTo("#xg-h", {{ opacity: 0, x: -80, filter: "blur(12px)" }}, {{ opacity: 1, x: 0, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }}, 0.35);
    tl.fromTo("#xg-pills span", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3, stagger: 0.08, ease: "expo.out" }}, 1.0);
    // exit: punch through the globe
    tl.to("#xg-eb, #xg-h, #xg-pills", {{ opacity: 0, x: -120, filter: "blur(10px)", duration: 0.25, ease: "power3.in" }}, 3.5);
    tl.to("#xg-svg", {{ scale: 3.2, opacity: 0, duration: 0.4, ease: "power3.in" }}, 3.5);
""",
)

# ====================================================================== 3  IMAGES (4.3 s)
COLS, ROWS = 12, 7
CW, CH = 1100 / COLS, 600 / ROWS
tiles = "".join(
    f'<div class="tile" style="left:{c*CW:.2f}px;top:{r*CH:.2f}px;width:{CW+0.6:.2f}px;height:{CH+0.6:.2f}px;'
    f'background-position:-{c*CW:.2f}px -{r*CH:.2f}px"></div>'
    for r in range(ROWS) for c in range(COLS)
)
images = scene(
    "ximages",
    f"""
    #root {{ background: {NAVY}; }}
    #xi-white {{ left: 0; top: 0; width: 1920px; height: 1080px; background: #fff; clip-path: circle(0% at 960px 540px); }}
    #xi-h {{ left: 120px; top: 90px; font-size: 92px; }}
    #xi-h em {{ font-style: normal; color: {B_GREEN}; }}
    #xi-card {{ left: 120px; top: 300px; width: 1100px; height: 600px; border-radius: 30px; overflow: hidden; perspective: 1400px; box-shadow: 0 40px 100px rgba(16,24,39,.25); }}
    .tile {{ position: absolute; background-image: url('assets/img/wiese.jpg'); background-size: 1100px 600px; backface-visibility: hidden; }}
    #xi-tag {{ left: 150px; top: 330px; padding: 12px 22px; border-radius: 999px; background: rgba(255,255,255,.94); font-size: 30px; font-weight: 800; }}
    #xi-kb {{ left: 1290px; top: 330px; font-family: 'Bricolage Grotesque'; font-size: 150px; font-weight: 700; letter-spacing: -0.04em; line-height: 1; }}
    #xi-unit {{ left: 1295px; top: 300px; font-size: 30px; color: {MUTED}; font-weight: 600; }}
    #xi-bar {{ left: 1295px; top: 500px; width: 500px; height: 20px; border-radius: 10px; background: #E2E8F0; overflow: hidden; }}
    #xi-fill {{ width: 100%; height: 100%; border-radius: 10px; transform-origin: 0 50%; }}
    #xi-stamp {{ left: 1280px; top: 580px; width: 540px; height: 300px; border-radius: 36px; background: {B_GREEN}; color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 30px 80px rgba(12,153,88,.45); }}
    #xi-stamp b {{ font-family: 'Bricolage Grotesque'; font-size: 190px; line-height: .9; letter-spacing: -0.05em; }}
    #xi-stamp span {{ font-size: 34px; font-weight: 700; }}
    #xi-note {{ left: 120px; top: 935px; font-size: 28px; color: {MUTED}; }}
""",
    f"""<div id="xi-white" class="abs"></div>
    <div id="xi-h" class="abs h">Bilder? <em>Automatisch</em> leichter.</div>
    <div id="xi-card" class="abs">{tiles}</div>
    <div id="xi-tag" class="abs">JPG</div>
    <div id="xi-unit" class="abs">Dateigröße</div>
    <div id="xi-kb" class="abs">303,4 KB</div>
    <div id="xi-bar" class="abs"><div id="xi-fill"></div></div>
    <div id="xi-stamp" class="abs"><b>−35 %</b><span>als WebP · ohne Plugins</span></div>
    <div id="xi-note" class="abs">Beispielbild von fast.site · Ersparnis je nach Bild</div>""",
    f"""
    tl.fromTo("#xi-white", {{ clipPath: "circle(0% at 960px 540px)" }}, {{ clipPath: "circle(120% at 960px 540px)", duration: 0.45, ease: "power3.inOut" }}, 0);
    tl.fromTo("#xi-h", {{ opacity: 0, y: -40, filter: "blur(12px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }}, 0.3);
    // the photo assembles tile by tile out of depth
    tl.fromTo("#xi-card .tile", {{ opacity: 0, z: -600, rotationX: 70 }}, {{ opacity: 1, z: 0, rotationX: 0, duration: 0.5, ease: "expo.out", stagger: {{ each: 0.006, from: "center", grid: [{ROWS}, {COLS}] }} }}, 0.35);
    tl.fromTo("#xi-tag, #xi-unit, #xi-kb, #xi-bar", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.35, stagger: 0.06, ease: "expo.out" }}, 0.7);
    tl.set("#xi-fill", {{ backgroundColor: "#73737F" }}, 0.01);
    // compression sweep: every tile flips once, left to right, and the numbers fall
    tl.to("#xi-card .tile", {{ rotationY: 360, duration: 0.6, ease: "power2.inOut", stagger: {{ each: 0.012, from: "start", grid: [{ROWS}, {COLS}], axis: "x" }} }}, 1.45);
    const kb = {{ v: 303.4 }};
    tl.fromTo(kb, {{ v: 303.4 }}, {{ v: 198.2, duration: 1.0, ease: "power3.inOut", onUpdate: () => {{
      document.querySelector("#xi-kb").textContent = kb.v.toFixed(1).replace(".", ",") + " KB";
    }} }}, 1.45);
    tl.fromTo("#xi-fill", {{ scaleX: 1 }}, {{ scaleX: 0.653, backgroundColor: "{B_GREEN}", duration: 1.0, ease: "power3.inOut" }}, 1.45);
    tl.call(() => {{ document.querySelector("#xi-tag").textContent = "JPG"; }}, null, 2.04);
    tl.call(() => {{ document.querySelector("#xi-tag").textContent = "WebP ⚡"; }}, null, 2.05);
    // the stamp slams in
    tl.fromTo("#xi-stamp", {{ opacity: 0, scale: 2.6, rotation: -14 }}, {{ opacity: 1, scale: 1, rotation: -4, duration: 0.32, ease: "power4.in" }}, 2.45);
    tl.fromTo("#xi-card", {{ x: 0 }}, {{ x: -12, duration: 0.04, ease: "none" }}, 2.77);
    tl.to("#xi-card", {{ x: 9, duration: 0.04, ease: "none" }}, 2.81);
    tl.to("#xi-card", {{ x: 0, duration: 0.06, ease: "none" }}, 2.85);
    tl.fromTo("#xi-note", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 1.0);
    tl.to("#xi-h, #xi-card, #xi-tag, #xi-unit, #xi-kb, #xi-bar, #xi-stamp, #xi-note", {{ opacity: 0, scale: 0.92, filter: "blur(10px)", duration: 0.25, ease: "power3.in" }}, 4.05);
""",
)

# ====================================================================== 4  DDOS (2.7 s)
swarm, swarm_js = "", []
for k in range(42):
    ang = det(k, 11) * math.tau
    d0 = 1250 + det(k, 12) * 300
    sx, sy = 960 + math.cos(ang) * d0, 600 + math.sin(ang) * d0 * 0.75
    hx, hy = 960 + math.cos(ang) * 235, 600 + math.sin(ang) * 235
    bx, by = 960 + math.cos(ang + 0.6) * 520, 600 + math.sin(ang + 0.6) * 520
    t0 = 0.25 + det(k, 13) * 1.15
    swarm += f'<circle id="xd-{k}" r="{9 + det(k, 14) * 8:.1f}"/>'
    swarm_js.append(
        f'tl.fromTo("#xd-{k}", {{ attr: {{ cx: {sx:.0f}, cy: {sy:.0f} }}, opacity: 1 }}, {{ attr: {{ cx: {hx:.0f}, cy: {hy:.0f} }}, duration: 0.32, ease: "power2.in", immediateRender: false }}, {t0:.2f});'
        f'tl.to("#xd-{k}", {{ attr: {{ cx: {bx:.0f}, cy: {by:.0f} }}, opacity: 0, duration: 0.3, ease: "power2.out" }}, {t0 + 0.32:.2f});'
    )
hits = sorted(0.25 + det(k, 13) * 1.15 + 0.32 for k in range(0, 42, 4))
rings = "".join(f'<div id="xd-r{i}" class="abs xring"></div>' for i in range(len(hits)))
ring_js = "\n    ".join(
    f'tl.fromTo("#xd-r{i}", {{ scale: 1, opacity: 0.9 }}, {{ scale: 1.5, opacity: 0, duration: 0.45, ease: "power2.out", immediateRender: false }}, {h:.2f});'
    for i, h in enumerate(hits)
)
ddos = scene(
    "xddos",
    f"""
    #root {{ background: {NAVY}; color: #fff; }}
    #xd-red {{ left: 0; top: 0; width: 1920px; height: 1080px; background: radial-gradient(circle at 50% 55%, rgba(223,72,43,.0) 20%, rgba(223,72,43,.35) 100%); }}
    #xd-svg {{ left: 0; top: 0; width: 1920px; height: 1080px; }}
    #xd-svg circle {{ fill: {B_RED}; opacity: 0; }}
    .xring {{ left: 735px; top: 375px; width: 450px; height: 450px; border-radius: 50%; border: 6px solid #7FA6FF; opacity: 0; }}
    #xd-shield {{ left: 810px; top: 450px; width: 300px; height: 300px; }}
    #xd-h {{ left: 0; right: 0; top: 90px; text-align: center; font-size: 110px; }}
    #xd-h em {{ font-style: normal; color: {B_RED}; }}
    #xd-ok {{ left: 0; right: 0; top: 880px; text-align: center; }}
    #xd-ok span {{ display: inline-flex; align-items: center; gap: 16px; padding: 18px 36px; border-radius: 999px; background: {B_GREEN}; color: #fff; font-size: 38px; font-weight: 800; }}
""",
    f"""<div id="xd-red" class="abs"></div>
    <svg id="xd-svg" class="abs" viewBox="0 0 1920 1080">{swarm}</svg>
    {rings}
    <svg id="xd-shield" class="abs" viewBox="0 0 100 100"><defs><linearGradient id="xdg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5B8CFF"/><stop offset="1" stop-color="{B_BLUE}"/></linearGradient></defs><path d="M50 6 L88 20 V48 C88 72 70 88 50 95 C30 88 12 72 12 48 V20 Z" fill="url(#xdg)"/><path d="M33 50 L45 62 L68 38" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <div id="xd-h" class="abs h"><em>Angriffe?</em> Prallen ab.</div>
    <div id="xd-ok" class="abs"><span>● Website bleibt online</span></div>""",
    f"""
    tl.fromTo("#xd-red", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 0.1);
    tl.fromTo("#xd-shield", {{ scale: 0, rotation: -30 }}, {{ scale: 1, rotation: 0, duration: 0.45, ease: "back.out(1.8)" }}, 0.0);
    tl.fromTo("#xd-h", {{ opacity: 0, scale: 1.3, filter: "blur(14px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out" }}, 0.1);
    {chr(10).join('    ' + s for s in swarm_js)}
    {ring_js}
    tl.to("#xd-red", {{ opacity: 0, duration: 0.4 }}, 1.3);
    tl.fromTo("#xd-ok", {{ opacity: 0, y: 40, scale: 0.8 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(2)" }}, 1.35);
    tl.to("#xd-h, #xd-ok, #xd-shield, .xring", {{ opacity: 0, filter: "blur(10px)", duration: 0.2, ease: "power3.in" }}, 2.45);
""",
)

# ====================================================================== 5  CTA (4.8 s)
rise, rise_js = "", []
for k in range(36):
    x = 60 + det(k, 21) * 1800
    s = 0.35 + det(k, 22) * 0.9
    t0 = 2.0 + det(k, 23) * 2.2
    arm = ["ul", "ur", "ll", "lr"][k % 4]
    rise += f'<div id="xc-r{k}" class="abs rise" style="left:{x:.0f}px">{mark_svg(f"xc{k}")}</div>'
    rise_js.append(
        f'tl.fromTo("#xc-r{k}", {{ y: 1200, scale: {s:.2f}, opacity: 1 }}, {{ y: -300, duration: {0.9 + det(k, 24) * 0.8:.2f}, ease: "power2.in", immediateRender: false }}, {t0:.2f});'
    )
cta = scene(
    "xcta",
    f"""
    #root {{ background: {NAVY}; }}
    #xc-white {{ left: 0; top: 0; width: 1920px; height: 1080px; background: #fff; clip-path: inset(100% 0 0 0); }}
    #xc-h {{ left: 0; right: 0; top: 230px; text-align: center; font-size: 110px; }}
    #xc-form {{ left: 410px; top: 470px; width: 1100px; height: 140px; border-radius: 32px; border: 3px solid #E2E8F0; background: #fff; display: flex; align-items: center; padding: 0 16px 0 46px; box-shadow: 0 30px 80px rgba(16,24,39,.14); }}
    #xc-in {{ flex: 1; font-size: 54px; font-weight: 600; color: {INK}; white-space: nowrap; overflow: hidden; }}
    #xc-btn {{ height: 104px; padding: 0 46px; border-radius: 22px; background: {BLUE}; color: #fff; font-size: 40px; font-weight: 800; display: flex; align-items: center; }}
    #xc-ok {{ left: 0; right: 0; top: 660px; text-align: center; font-size: 44px; font-weight: 800; color: {GREEN_DEEP}; }}
    #xc-flood {{ left: 0; top: 0; width: 1920px; height: 1080px; background: {BLUE}; clip-path: circle(0px at 1380px 540px); }}
    .rise {{ top: 0; width: 140px; height: 140px; opacity: 0; }}
    .rise .mark {{ width: 140px; height: 140px; }}
    #xc-big {{ left: 0; right: 0; top: 250px; text-align: center; color: #fff; font-size: 330px; line-height: .9; letter-spacing: -0.05em; }}
    #xc-big2 {{ left: 0; right: 0; top: 560px; text-align: center; color: #fff; font-size: 120px; }}
    #xc-sub {{ left: 0; right: 0; top: 760px; text-align: center; }}
    #xc-sub span {{ display: inline-block; padding: 20px 44px; border-radius: 999px; background: #fff; color: {BLUE}; font-size: 44px; font-weight: 800; }}
    #xc-end {{ left: 0; top: 0; width: 1920px; height: 1080px; background: #fff; clip-path: circle(0% at 960px 540px); }}
""",
    f"""<div id="xc-white" class="abs"></div>
    <div id="xc-h" class="abs h">Domain verbinden.</div>
    <div id="xc-form" class="abs"><div id="xc-in"></div><div id="xc-btn">Verbinden ↗</div></div>
    <div id="xc-ok" class="abs">✓ Fertig. Beschleunigung aktiv.</div>
    <div id="xc-flood" class="abs"></div>
    {rise}
    <div id="xc-big" class="abs h">7 Tage</div>
    <div id="xc-big2" class="abs h">kostenlos testen.</div>
    <div id="xc-sub" class="abs"><span>Keine Kreditkarte nötig</span></div>
    <div id="xc-end" class="abs"></div>""",
    f"""
    const domain = "deinedomain.de";
    tl.fromTo("#xc-white", {{ clipPath: "inset(100% 0 0 0)" }}, {{ clipPath: "inset(0% 0 0 0)", duration: 0.35, ease: "power3.inOut" }}, 0);
    tl.fromTo("#xc-h", {{ opacity: 0, y: 40, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }}, 0.2);
    tl.fromTo("#xc-form", {{ opacity: 0, scaleX: 0.2 }}, {{ opacity: 1, scaleX: 1, duration: 0.45, ease: "expo.out" }}, 0.3);
    const typed = {{ n: 0 }};
    tl.fromTo(typed, {{ n: 0 }}, {{ n: domain.length, duration: 0.55, ease: "none", onUpdate: () => {{
      document.querySelector("#xc-in").textContent = domain.slice(0, Math.round(typed.n));
    }} }}, 0.6);
    tl.fromTo("#xc-btn", {{ scale: 1 }}, {{ scale: 0.9, duration: 0.08, ease: "power2.in" }}, 1.3);
    tl.to("#xc-btn", {{ scale: 1, backgroundColor: "{B_GREEN}", duration: 0.25, ease: "back.out(3)" }}, 1.38);
    tl.fromTo("#xc-ok", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.2)" }}, 1.45);
    // the click floods the world blue
    tl.fromTo("#xc-flood", {{ clipPath: "circle(0px at 1380px 540px)" }}, {{ clipPath: "circle(2300px at 1380px 540px)", duration: 0.55, ease: "power3.in" }}, 1.85);
    tl.to("#xc-h, #xc-form, #xc-ok", {{ opacity: 0, duration: 0.01 }}, 2.42);
    tl.fromTo("#xc-big", {{ opacity: 0, scale: 0.4, filter: "blur(20px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }}, 2.35);
    tl.fromTo("#xc-big2", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }}, 2.6);
    tl.fromTo("#xc-sub", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, 3.0);
    // brand arrows rise like speed itself
    {chr(10).join('    ' + s for s in rise_js)}
    // iris to white: the endcard starts on white
    tl.fromTo("#xc-end", {{ clipPath: "circle(0% at 960px 540px)" }}, {{ clipPath: "circle(75% at 960px 540px)", duration: 0.4, ease: "power3.in" }}, 4.4);
""",
)

for name, html in [("x-speed", speed), ("x-globe", globe), ("x-images", images), ("x-ddos", ddos), ("x-cta", cta)]:
    (COMP / f"{name}.html").write_text(html)
print("ok")
