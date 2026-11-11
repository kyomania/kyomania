"""Builds porridge-reel/index.html (v2: 7 products, no voice, 24 s)."""
import json, sys
OUT = sys.argv[1]

# id, pack img, pack width(px), bg css, text color, tag bg, tag fg, kicker, name, tag, fx, particles
P = [
    ("oats", "pack_oats.png", 520, "radial-gradient(90% 70% at 50% 55%, #ff7a6b 0%, #e8483f 50%, #9c1f1a 100%)", "#fff4e3", "#fff4e3", "#c8302a",
     "01 · Die Basis", "Hafer-<br>flocken", "100 % natürlich", "burst", ["oat0.png","oat1.png","oat2.png","oat3.png","oat4.png","oat5.png","oat6.png","oat7.png"]),
    ("protein", "pack_protein.png", 600, "radial-gradient(90% 70% at 50% 55%, #1f9a7c 0%, #0f6b57 55%, #06352b 100%)", "#ecd28a", "#ecd28a", "#0f4f40",
     "02 · Der Protein-Boost", "Supreme<br>Vegan Protein", "Schoko-Haselnuss · 100 % vegan", "powder", ["choc0.png","choc1.png","choc3.png"]),
    ("agave", "pack_agave.png", 330, "radial-gradient(90% 70% at 50% 50%, #6fb3ad 0%, #2f6f6c 55%, #163c3b 100%)", "#fff4e3", "#fff4e3", "#2f6f6c",
     "03 · Die Süße", "Bio-<br>Agavensirup", "Bio · fettfrei", "honey", []),
    ("almond", "pack_almonds.png", 540, "radial-gradient(90% 70% at 50% 55%, #e6c49b 0%, #c49a6c 55%, #8f6339 100%)", "#170b06", "#170b06", "#f6ecdf",
     "04 · Der Crunch", "Kalifornische<br>Mandeln", "Protein &amp; Ballaststoffe", "burst", ["almond0.png","almond1.png","almond3.png"]),
    ("puffies", "pack_puffies.png", 540, "radial-gradient(90% 70% at 50% 55%, #ff6b9a 0%, #e33a6e 50%, #9e1748 100%)", "#fff4e3", "#fff4e3", "#e33a6e",
     "05 · Extra Crunch", "Mini Protein<br>Puffies", "Vegan · ohne Zuckerzusatz", "pop", ["puff1.png","puff2.png","puff3.png","puff4.png","puff5.png"]),
    ("nibs", "pack_nibs.png", 530, "radial-gradient(70% 45% at 50% 58%, #5a4413 0%, #1a1206 55%, #0a0703 100%)", "#e6c35c", "#e6c35c", "#170b06",
     "06 · Das Finish", "Bio-<br>Kakaonibs", "100 % natürlich · vegan", "rain", [f"nib{i}.png" for i in range(14)]),
    ("pb", "pack_pb.png", 560, "radial-gradient(90% 70% at 50% 55%, #7cc0ec 0%, #3f8fc9 55%, #1d4f7a 100%)", "#fff4e3", "#fff4e3", "#2a6aa0",
     "07 · Das Topping", "Erdnussbutter<br>mit Zimt", "Crunchy · Zimtschnecke", "swirl", ["peanut1.png","choc0.png"]),
]
T0, STEP = 3.02, 1.5
ING_END = T0 + STEP * len(P)          # 13.52
MIX = ING_END                         # 13.52 .. 16.02
HERO = 16.02                          # .. 20.52
END = 20.52                           # .. 24
DUR = 24.0

scenes = []
for i, (pid, img, w, bg, fg, tbg, tfg, kick, name, tag, fx, parts) in enumerate(P):
    st = T0 + i * STEP
    extra = ""
    if fx == "honey":
        extra = '''<svg class="abs" id="honey" viewBox="0 0 1080 1000" style="left:0;top:0;width:1080px;height:1000px">
          <defs><linearGradient id="hg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8c64e"/><stop offset="1" stop-color="#d98a12"/></linearGradient>
          <linearGradient id="hl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="rgba(255,255,255,0)"/><stop offset="0.5" stop-color="rgba(255,248,220,0.7)"/><stop offset="1" stop-color="rgba(255,255,255,0)"/></linearGradient></defs>
          <g id="hdrips"></g>
          <rect id="hbar" x="0" y="-40" width="1080" height="120" fill="url(#hg)"/>
          <rect x="0" y="40" width="1080" height="14" fill="url(#hl)" opacity="0.6"/>
        </svg>'''
    if fx == "powder":
        extra = '<div class="layer" id="powder"></div>'
    if fx == "swirl":
        extra = '''<svg class="abs" id="swirl" viewBox="0 0 1080 1920" style="left:0;top:0;width:1080px;height:1920px">
          <path id="sw1" d="M 120 1500 C 60 1100, 300 820, 540 860 S 1040 1150, 960 1420 S 520 1700, 300 1500 S 330 1000, 760 760" fill="none" stroke="#b56a2c" stroke-width="64" stroke-linecap="round"/>
          <path id="sw2" d="M 120 1500 C 60 1100, 300 820, 540 860 S 1040 1150, 960 1420 S 520 1700, 300 1500 S 330 1000, 760 760" fill="none" stroke="#e7a86a" stroke-width="18" stroke-linecap="round" transform="translate(-10 -12)"/>
        </svg>'''
    scenes.append(f'''
      <div id="s_{pid}" class="clip ing" data-start="{st:.2f}" data-duration="{STEP + 0.35:.2f}" style="z-index:{20 + i};background:{bg};color:{fg}">
        <div class="abs num">{i + 1:02d}</div>
        {extra}
        <div class="layer pt"></div>
        <div class="abs shadow" style="left:{540 - w * 0.45:.0f}px;top:1470px;width:{w * 0.9:.0f}px"></div>
        <img class="pack pk" src="assets/img/{img}" style="left:{540 - w / 2:.0f}px;top:1460px;width:{w}px" alt="" />
        <div class="abs ttl"><div class="kicker">{kick}</div><div class="serif name">{name}</div></div>
        <div class="abs full tg" style="top:1545px"><span class="tag" style="background:{tbg};color:{tfg}">{tag}</span></div>
      </div>''')

strobe = "".join(
    f'<div class="sb" style="background:{p[3]}"><img src="assets/img/{p[1]}" style="height:{1000 if p[0]!="agave" else 1050}px" alt=""/></div>' for p in P)
orbit = "".join(f'<img class="ob" src="assets/img/{p[1]}" alt="" />' for p in P)
mini = "".join(f'<img class="mn" id="mn{i}" src="assets/img/{p[1]}" alt="" />' for i, p in enumerate(P))
fan = "".join(f'<img class="pack fn" src="assets/img/{p[1]}" alt="" />' for p in P)

cfg = json.dumps([{"id": p[0], "fx": p[10], "parts": p[11]} for p in P])
html = open(OUT + ".tpl").read()
html = (html.replace("{{SCENES}}", "".join(scenes)).replace("{{STROBE}}", strobe).replace("{{ORBIT}}", orbit)
        .replace("{{MINI}}", mini).replace("{{FAN}}", fan).replace("{{CFG}}", cfg)
        .replace("{{T0}}", str(T0)).replace("{{STEP}}", str(STEP)).replace("{{MIX}}", str(MIX)).replace("{{HERO}}", str(HERO))
        .replace("{{END}}", str(END)).replace("{{DUR}}", str(DUR)))
open(OUT, "w").write(html)
print("built", OUT)
