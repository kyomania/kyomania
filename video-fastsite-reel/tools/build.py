# Generates index.html: fixed centered fast.site logo over rapid-cut brand identity shots.
import pathlib
B="#3f71b5";G="#0f9956";R="#df4a2a";Y="#f9b41b";INK="#0d0f14";PAPER="#ece8e0";W="#ffffff"
def logo(mode):
    if mode=="c": cols=[G,B,Y,R]
    else:
        c={"w":W,"k":INK}.get(mode,mode); cols=[c]*4
    return f'''<svg class="lg" viewBox="0 0 1024 1024"><line x1="512" y1="135" x2="840" y2="462" stroke="{cols[0]}"/><line x1="182" y1="462" x2="512" y2="135" stroke="{cols[1]}"/><line x1="512" y1="566" x2="840" y2="893" stroke="{cols[2]}"/><line x1="182" y1="893" x2="512" y2="566" stroke="{cols[3]}"/></svg>'''
def img(n,pos="50% 50%",tf=""):
    return f'<img class="bg" src="assets/m{n}.png" style="object-position:{pos};{tf}" alt="">'
def mono(t,style):return f'<div class="mono" style="{style}">{t}</div>'
def grid(bg,fg):
    lines="".join(f'<div class="gl" style="left:{x}px;top:0;width:2px;height:1920px;background:{fg}"></div>' for x in (390,540,690))
    lines+="".join(f'<div class="gl" style="top:{y}px;left:0;height:2px;width:1080px;background:{fg}"></div>' for y in (810,960,1110))
    circ="".join(f'<div class="gc" style="width:{d}px;height:{d}px;margin:-{d//2}px 0 0 -{d//2}px;border-color:{fg}"></div>' for d in (300,620,980))
    return f'<div class="fill" style="background:{bg}">{lines}{circ}'+mono("Construction",f"left:70px;top:820px;color:{fg}")+mono("3×",f"right:70px;top:1120px;color:{fg}")+mono("Grid 8 pt",f"left:70px;bottom:120px;color:{fg}")+"</div>"
def page(bg,fg,top,l,r,bot):
    return f'<div class="fill" style="background:{bg}">'+mono(top,f"left:0;right:0;top:420px;text-align:center;color:{fg}")+mono(l,f"left:90px;top:560px;color:{fg}")+mono(r,f"right:90px;top:560px;color:{fg}")+mono(bot,f"left:0;right:0;bottom:200px;text-align:center;color:{fg}")+f'<div class="pin" style="background:{fg}"></div></div>'
def palette():
    rows=[(INK,"Midnight Ink","#0D0F14",W),(PAPER,"Paper","#ECE8E0",INK),(W,"Speed Blue","#3F71B5",INK),("#fde9b8","Signal Yellow","#F9B41B",INK)]
    h=1920//4;out='<div class="fill">'
    for i,(bg,n,hx,fg) in enumerate(rows):
        out+=f'<div style="position:absolute;left:0;right:0;top:{i*h}px;height:{h}px;background:{bg}">'+mono(n,f"left:70px;top:40px;color:{fg}")+mono(f"HEX {hx}<br>RGB · CMYK",f"right:70px;top:40px;text-align:right;color:{fg}")+"</div>"
    return out+"</div>"
def dots(bg,fg):
    import math
    s=f'<div class="fill" style="background:{bg}">'
    k=0
    for ring,(rad,n) in enumerate([(330,18),(430,24),(530,30),(640,36),(760,44),(900,52)]):
        for j in range(n):
            a=2*math.pi*j/n+ring*0.2; x=540+rad*math.cos(a); y=960+rad*math.sin(a)
            if (j*7+ring*3)%5==0: continue
            w=90 if (j+ring)%4==0 else 46
            s+=f'<div class="pill" style="left:{x-w/2:.0f}px;top:{y-23:.0f}px;width:{w}px;background:{fg};transform:rotate({math.degrees(a)+90:.0f}deg)"></div>'
            k+=1
    return s+"</div>"
def poster(bg,fg):
    return f'<div class="fill" style="background:{bg}">'+mono("A faster website.<br>Higher on Google.",f"left:90px;top:640px;color:{fg};font-size:34px")+mono("fast.site",f"left:90px;bottom:420px;color:{fg}")+f'<div style="position:absolute;left:0;right:0;top:80px;height:110px;background:{fg};opacity:.12"></div></div>'

S={
 "m1":(img(1),"c"), "m2":(img(2,"50% 50%"),"k"), "m3":(img(3,"50% 50%","transform:translateY(-40px)"),"w"),
 "m4":(img(4),"w"), "m5":(img(5,"50% 50%","transform:translate(12px,-120px) scale(1.1)"),"c"), "m6":(img(6),"w"),
 "m7":(img(7,"50% 50%","transform:translateY(180px)"),"k"), "m8":(img(8,"50% 50%","transform:translate(90px,-100px) scale(1.08)"),"c"),
 "gl":(grid(PAPER,"#9a958c"),"k"), "gd":(grid("#1a1d24","#5a5f6a"),"w"),
 "tl":(page(PAPER,INK,"fast.site","Unit of digital","Speed","fast.site 2026©"),"k"),
 "td":(page("#1a1d24",W,"fast.site","Unit of digital","Speed","fast.site 2026©"),"w"),
 "pa":(palette(),B), "db":(dots(B,W),"w"), "dy":(dots(Y,INK),"k"),
 "pb":(poster(B,W),"w"), "pr":(poster(R,W),"w"),
}
seq="m1 m2 gl m3 tl m4 pa gd pb m7 m1 m5 m6 db m2 m8 m3 td pa m4 gl pr m7 m1 m2 dy m3 m5 m6".split()
d=0.3; shots=[]; t=0.0
for k in seq: shots.append((k,round(t,2),d)); t+=d
FIN=10-t
html=[]
for i,(k,st,du) in enumerate(shots):
    body,lm=S[k]
    html.append(f'<div id="s{i}" class="clip shot" data-start="{st}" data-duration="{du}" data-track-index="0">{body}<div class="logo">{logo(lm)}</div></div>')
final=page(PAPER,INK,"fast.site","A faster website.","Higher on Google.","Start free trial · fast.site")
html.append(f'<div id="sfin" class="clip shot" data-start="{round(t,2)}" data-duration="{round(FIN,2)}" data-track-index="0">{final}<div class="logo">{logo("c")}</div></div>')
doc=pathlib.Path(__file__).with_name("template.html").read_text().replace("{{SHOTS}}","\n".join(html))
pathlib.Path(__file__).parent.parent.joinpath("index.html").write_text(doc)
print(len(shots),"shots, final at",round(t,2))
