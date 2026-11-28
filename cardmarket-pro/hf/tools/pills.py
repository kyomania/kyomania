CSS='''.pillrow{position:absolute;left:0;width:100%;display:flex;justify-content:center}
.pill{position:relative;display:flex;align-items:center;border-radius:999px}
.pill .ib{position:relative;left:auto;top:auto;flex:none}
.pn{font-family:"InterD";font-weight:700;white-space:nowrap}
.ps{color:rgba(224,255,250,.8);white-space:nowrap}
'''
def inject(h,pills,sz,extra_css=''):
    # pills: list of (id,start,end,top,icon_svg,name,sub)
    css=CSS+f'''.pill{{gap:{sz[0]}px;padding:{sz[1]}px {sz[2]}px {sz[1]}px {sz[1]}px}}
.pill .ib{{width:{sz[3]}px;height:{sz[3]}px;border-radius:999px}}.pill .ib svg{{width:{int(sz[3]*.55)}px;height:{int(sz[3]*.55)}px}}
.pn{{font-size:{sz[4]}px}}.ps{{font-size:{sz[5]}px;margin-top:2px}}
'''+extra_css
    h=h.replace('</style>',css+'</style>',1)
    html='';js=''
    for (i,s,e,top,ic,n,sub) in pills:
        html+=f'<div id="{i}" class="pillrow clip" data-start="{s:.2f}" data-duration="{e-s:.2f}" data-track-index="4" style="top:{top}px"><div class="glass pill"><div class="sheen"></div><div class="ib">{ic}</div><div><div class="pn">{n}</div><div class="ps">{sub}</div></div></div></div>\n'
        js+=f'tl.fromTo("#{i} .pill",{{opacity:0,y:36,scale:.9,filter:"blur(10px)"}},{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:.55,ease:"back.out(1.6)"}},{s:.2f});\n'
        js+=f'tl.fromTo("#{i} .ib",{{scale:.4,rotation:-20}},{{scale:1,rotation:0,duration:.5,ease:"back.out(2.4)"}},{s+0.1:.2f});\n'
        js+=f'tl.fromTo("#{i} .sheen",{{xPercent:-150}},{{xPercent:330,duration:.9,ease:"power2.inOut"}},{s+0.35:.2f});\n'
        js+=f'tl.to("#{i} .pill",{{opacity:0,y:-20,scale:.96,filter:"blur(8px)",duration:.3,ease:"power2.in"}},{e-0.32:.2f});\n'
    h=h.replace(' <div id="fade"',html+' <div id="fade"',1)
    h=h.replace('window.__timelines=window.__timelines||{};',js+'window.__timelines=window.__timelines||{};',1)
    return h
