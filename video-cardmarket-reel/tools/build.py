# Generates index.html: fixed centered cardmarket.pro "card-C" mark over rapid-cut brand identity shots.
import pathlib, math
MINT="#5ee0d4"; TEAL="#00877a"; GR="#0a1118"; W="#ffffff"; LG="#f0f3f4"
CARD="M210,170 L640,70 L690,130 L605,690 Q600,725 560,730 L180,770 Q110,775 110,700 L150,230 Q155,180 210,170 Z"
CC="M435,258 L370,385 L345,410 Q330,440 340,490 Q350,525 380,525 L580,525 L565,640 Q562,648 550,648 L320,648 Q240,640 210,560 Q195,520 205,420 Q220,350 280,320 Z"
ACC="M495,238 L610,238 Q620,240 612,252 L548,375 Q540,385 528,385 L420,385 Q410,383 415,372 Z"
n=[0]
def mark(mode):
    vb='viewBox="100 60 600 720"'
    if mode=="c":
        return f'<svg class="lg" {vb}><path d="{CARD}" fill="{MINT}"/><path d="{CC}" fill="{GR}"/><path d="{ACC}" fill="{TEAL}"/></svg>'
    n[0]+=1; fill={"k":GR,"w":W,"m":MINT}[mode]; mid=f"cut{n[0]}"
    return (f'<svg class="lg" {vb}><defs><mask id="{mid}"><path d="{CARD}" fill="#fff"/><path d="{CC}" fill="#000"/>'
            f'<path d="{ACC}" fill="#000"/></mask></defs><rect x="0" y="0" width="800" height="800" fill="{fill}" mask="url(#{mid})"/></svg>')
def img(i,dx=0,dy=0):
    return f'<div class="fill" style="transform:translate({dx}px,{dy}px) scale({1+2.2*max(abs(dx)/1080,abs(dy)/1920):.3f})"><img class="bg" src="assets/m{i}.png" alt=""></div>'
def mono(t,s): return f'<div class="mono" style="{s}">{t}</div>'
def grid(bg,fg):
    s=f'<div class="fill" style="background:{bg}">'
    s+="".join(f'<div class="gl" style="left:{x}px;top:0;width:2px;height:1920px;background:{fg}"></div>' for x in (400,540,680))
    s+="".join(f'<div class="gl" style="top:{y}px;left:0;height:2px;width:1080px;background:{fg}"></div>' for y in (790,960,1130))
    s+="".join(f'<div class="gc" style="width:{d}px;height:{d}px;margin:-{d//2}px 0 0 -{d//2}px;border-color:{fg}"></div>' for d in (320,640,1000))
    s+=f'<svg style="position:absolute;left:50%;top:50%;width:640px;height:768px;margin:-384px 0 0 -320px;overflow:visible" viewBox="100 60 600 720"><path d="{CARD}" fill="none" stroke="{fg}" stroke-width="3"/><path d="{CC}" fill="none" stroke="{fg}" stroke-width="3"/><path d="{ACC}" fill="none" stroke="{fg}" stroke-width="3"/></svg>'
    return s+mono("Card-C / construction",f"left:70px;top:150px;color:{fg}")+mono("8° skew",f"right:70px;top:1150px;color:{fg}")+mono("Grid 8 pt",f"left:70px;bottom:130px;color:{fg}")+"</div>"
def page(bg,fg,top,l,r,bot):
    return f'<div class="fill" style="background:{bg}">'+mono(top,f"left:0;right:0;top:420px;text-align:center;color:{fg}")+mono(l,f"left:90px;top:560px;color:{fg}")+mono(r,f"right:90px;top:560px;color:{fg};text-align:right")+mono(bot,f"left:0;right:0;bottom:200px;text-align:center;color:{fg}")+f'<div class="pin" style="background:{fg}"></div></div>'
def palette():
    rows=[(GR,"Graphite","#0A1118",W),(MINT,"Mint","#5EE0D4",GR),(TEAL,"Deep Teal","#00877A",W),(LG,"Paper","#F0F3F4",GR)]
    h=480; o='<div class="fill">'
    for i,(bg,nm,hx,fg) in enumerate(rows):
        o+=f'<div style="position:absolute;left:0;right:0;top:{i*h}px;height:{h}px;background:{bg}">'+mono(nm,f"left:70px;top:40px;color:{fg}")+mono(f"HEX {hx}<br>RGB · CMYK",f"right:70px;top:40px;text-align:right;color:{fg}")+"</div>"
    return o+"</div>"
def cards(bg,fg):
    s=f'<div class="fill" style="background:{bg}">'
    for ring,(rad,cnt) in enumerate([(340,12),(470,17),(610,22),(760,28),(920,34)]):
        for j in range(cnt):
            if (j*5+ring*3)%6==0: continue
            a=2*math.pi*j/cnt+ring*0.25; x=540+rad*math.cos(a); y=960+rad*math.sin(a)
            s+=f'<div class="mini" style="left:{x-26:.0f}px;top:{y-36:.0f}px;background:{fg};transform:rotate({math.degrees(a)+90:.0f}deg) skewX(-8deg)"></div>'
    return s+"</div>"
def poster(bg,fg):
    return f'<div class="fill" style="background:{bg}">'+mono("Buy. Sell. Trade.<br>Every card, one market.",f"left:90px;top:620px;color:{fg};font-size:34px")+mono("cardmarket.pro",f"left:90px;bottom:420px;color:{fg}")+f'<div style="position:absolute;left:0;right:0;top:80px;height:110px;background:{fg};opacity:.12"></div></div>'

S={"m1":(img(1),"k"),"m2":(img(2,-26),"c"),"m3":(img(3,0,-120),"m"),"m4":(img(4,40,-200),"k"),
   "m5":(img(5,185),"m"),"m6":(img(6),"m"),"m7":(img(7),"c"),"m8":(img(8,0,120),"c"),
   "gl":(grid(LG,"#9aa3a8"),"k"),"gd":(grid(GR,"#3a4752"),"m"),
   "tl":(page(LG,GR,"cardmarket.pro","Unit of","Trade","cardmarket.pro 2026©"),"k"),
   "td":(page(GR,W,"cardmarket.pro","Unit of","Trade","cardmarket.pro 2026©"),"m"),
   "pa":(palette(),"c"),"cm":(cards(TEAL,MINT),"w"),"cg":(cards(GR,MINT),"c"),
   "pm":(poster(MINT,GR),"k"),"pg":(poster(GR,MINT),"m")}
seq="m1 m2 gl m4 tl m6 pa gd pm m8 m1 m7 m3 cm m2 m5 m4 td pa m6 gl pg m8 m1 m2 cg m4 m7 m3".split()
d=0.3; t=0.0; out=[]
for i,k in enumerate(seq):
    body,lm=S[k]
    out.append(f'<div id="s{i}" class="clip shot" data-start="{round(t,2)}" data-duration="{d}" data-track-index="0">{body}<div class="logo">{mark(lm)}</div></div>'); t+=d
fin=(f'<div class="fill" style="background:#080f14"><img src="assets/wordmark-dark.png" alt="cardmarket.pro" style="position:absolute;left:90px;width:900px;top:890px">'
     +mono("Buy · Sell · Trade",f"left:0;right:0;top:600px;text-align:center;color:{W}")
     +mono("Trading card marketplace",f"left:0;right:0;bottom:200px;text-align:center;color:{MINT}")+'</div>')
out.append(f'<div id="sfin" class="clip shot" data-start="{round(t,2)}" data-duration="{round(10-t,2)}" data-track-index="0">{fin}</div>')
p=pathlib.Path(__file__).parent
(p.parent/"index.html").write_text((p/"template.html").read_text().replace("{{SHOTS}}","\n".join(out)))
print(len(seq),"shots, final at",round(t,2))
