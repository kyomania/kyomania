<!doctype html>
<html lang="%%LANG%%" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{font-family:"InterL";src:url(assets/fonts/Inter-Regular.otf);font-weight:400}
@font-face{font-family:"InterL";src:url(assets/fonts/Inter-Medium.otf);font-weight:500}
@font-face{font-family:"InterL";src:url(assets/fonts/Inter-SemiBold.otf);font-weight:600}
@font-face{font-family:"InterL";src:url(assets/fonts/Inter-Bold.otf);font-weight:700}
@font-face{font-family:"InterD";src:url(assets/fonts/InterDisplay-Bold.otf);font-weight:700}
@font-face{font-family:"InterD";src:url(assets/fonts/InterDisplay-SemiBold.otf);font-weight:600}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#000}
body{font-family:"InterL",sans-serif;color:#fff;-webkit-font-smoothing:antialiased}
.full{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.glass{position:absolute;border-radius:30px;background:linear-gradient(140deg,rgba(18,44,44,.78),rgba(8,20,22,.72));
 backdrop-filter:blur(18px) saturate(140%);-webkit-backdrop-filter:blur(18px) saturate(140%);
 box-shadow:0 24px 60px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.10);overflow:hidden}
.glass::before{content:"";position:absolute;inset:0;border-radius:inherit;padding:2px;
 background:linear-gradient(135deg,rgba(94,234,212,.85),rgba(45,212,191,.15) 45%,rgba(94,234,212,.55));
 -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude}
.sheen{position:absolute;top:0;bottom:0;width:40%;left:0;transform:translateX(-150%);background:linear-gradient(100deg,transparent,rgba(255,255,255,.13),transparent)}
.ib{position:absolute;width:92px;height:92px;border-radius:24px;background:linear-gradient(145deg,#2dd4bf,#0f766e);
 color:#04201d;display:flex;align-items:center;justify-content:center;box-shadow:0 0 30px rgba(45,212,191,.45)}
.ib svg{width:50px;height:50px;stroke-width:2.2}
#count{left:150px;top:1010px;width:780px;height:216px}
#count .ib{left:32px;top:62px}
#num{position:absolute;left:150px;top:26px;font-family:"InterD";font-weight:700;font-size:82px;letter-spacing:-1.5px;font-variant-numeric:tabular-nums}
#csub{position:absolute;left:152px;top:122px;font-size:34px;font-weight:600}
#cmeta{position:absolute;left:152px;top:164px;font-size:28px;color:rgba(204,251,241,.7)}
.chip{position:absolute;right:66px;height:92px;border-radius:46px;padding:0 38px 0 96px;display:flex;align-items:center;font-size:36px;font-weight:600;white-space:nowrap}
.chip .ib{left:12px;top:12px;width:68px;height:68px;border-radius:34px}
.chip .ib svg{width:38px;height:38px}
#chip1{top:300px}#chip2{top:420px}#chip3{top:540px}
.card2{left:110px;width:860px;height:220px}
.card2 .ib{left:34px;top:64px}
.card2 .t{position:absolute;left:152px;top:36px;font-family:"InterD";font-weight:700;font-size:44px}
.card2 .b{position:absolute;left:152px;top:98px;font-size:29px;line-height:1.38;color:rgba(224,255,250,.82)}
#prot{top:1010px}#coll{top:290px}
#spark{position:absolute;left:152px;top:150px;width:300px;height:50px}
#freeze{filter:blur(22px) brightness(.55);transform:scale(1.08)}
#panel{left:60px;top:560px;width:960px;height:700px}
#ptitle{position:absolute;left:60px;top:52px;font-family:"InterD";font-weight:700;font-size:56px;color:#5eead4;letter-spacing:-.5px}
#pline{position:absolute;left:60px;top:134px;height:3px;width:840px;background:linear-gradient(90deg,#2dd4bf,rgba(45,212,191,0));transform-origin:left}
#plist{position:absolute;left:60px;top:176px;list-style:none}
.pi{display:flex;align-items:center;height:96px;font-size:37px;font-weight:600;white-space:nowrap}
.ck{width:50px;height:50px;margin-right:26px;flex:none}
.ck circle{fill:rgba(45,212,191,.16);stroke:#2dd4bf;stroke-width:1.4}
.ckp{fill:none;stroke:#5eead4;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:20;stroke-dashoffset:20}
#wm{position:absolute;left:190px;top:1300px;width:700px}
#ctag{position:absolute;left:0;width:1080px;top:1424px;text-align:center;font-family:"InterD";font-weight:600;font-size:54px;color:#5eead4;letter-spacing:.5px}
#fade{position:absolute;inset:0;background:#000;opacity:0}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="27" data-width="1080" data-height="1920">
 <video id="segA" class="clip full" src="raw.mp4" muted playsinline data-start="0" data-duration="17.9" data-media-start="0" data-track-index="0"></video>
 <audio id="musA" src="raw.mp4" data-start="0" data-duration="17.9" data-media-start="0" data-track-index="5" data-volume="1"></audio>
 <img id="freeze" class="clip full" src="assets/freeze.png" data-start="17.9" data-duration="4.85" data-track-index="0">
 <audio id="musB" src="raw.mp4" data-start="17.9" data-duration="4.85" data-media-start="8.0" data-track-index="6" data-volume="0.8"></audio>
 <video id="segD" class="clip full" src="raw.mp4" muted playsinline data-start="22.75" data-duration="2.69" data-media-start="17.33" data-track-index="0"></video>
 <audio id="musD" src="raw.mp4" data-start="22.75" data-duration="2.69" data-media-start="17.33" data-track-index="7" data-volume="1"></audio>
 <img id="hold" class="clip full" src="assets/rawend.png" data-start="25.44" data-duration="1.56" data-track-index="0">
%%AUDIO%%
 <div id="count" class="glass clip" data-start="3.0" data-duration="3.9" data-track-index="1"><div class="sheen"></div>
  <div class="ib">%%ICS%%</div><div id="num">0</div><div id="csub">%%count_sub%%</div><div id="cmeta">%%count_meta%%</div></div>
 <div id="chip1" class="glass chip clip" data-start="10.6" data-duration="2.45" data-track-index="2"><div class="ib">%%ICC%%</div>%%chip1%%</div>
 <div id="chip2" class="glass chip clip" data-start="10.6" data-duration="2.45" data-track-index="3"><div class="ib">%%ICP%%</div>%%chip2%%</div>
 <div id="chip3" class="glass chip clip" data-start="10.6" data-duration="2.45" data-track-index="4"><div class="ib">%%ICB%%</div>%%chip3%%</div>
 <div id="prot" class="glass card2 clip" data-start="13.4" data-duration="2.5" data-track-index="1"><div class="sheen"></div>
  <div class="ib">%%ICSH%%</div><div class="t">%%prot_t%%</div><div class="b">%%prot_b1%%<br>%%prot_b2%%</div></div>
 <div id="coll" class="glass card2 clip" data-start="16.1" data-duration="1.8" data-track-index="1"><div class="sheen"></div>
  <div class="ib">%%ICCO%%</div><div class="t">%%coll_t%%</div><div class="b">%%coll_b%%</div>
  <svg id="spark" viewBox="0 0 300 50"><path id="sp" d="M2 40 C40 38 60 30 90 32 S140 18 170 22 S230 6 296 6" fill="none" stroke="#2dd4bf" stroke-width="4" stroke-linecap="round" stroke-dasharray="330" stroke-dashoffset="330"/></svg></div>
 <div id="panel" class="glass clip" data-start="18.05" data-duration="4.6" data-track-index="1"><div class="sheen"></div>
  <div id="ptitle">%%panel_t%%</div><div id="pline"></div><ul id="plist">%%ITEMS%%</ul></div>
 <img id="wm" class="clip" src="assets/wordmark.png" data-start="24.7" data-duration="2.3" data-track-index="2" style="mix-blend-mode:screen">
 <div id="ctag" class="clip" data-start="25.0" data-duration="2.0" data-track-index="3">Collector</div>
 <div id="fade" class="clip" data-start="26.6" data-duration="0.4" data-track-index="9"></div>
</div>
<script>
const SEP="%%SEP%%";
const fmt=n=>Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g,SEP);
const tl=gsap.timeline({paused:true});
const inn=(sel,t,extra={})=>tl.fromTo(sel,{opacity:0,y:40,scale:.94,filter:"blur(10px)"},{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:.55,ease:"back.out(1.6)",...extra},t);
const out=(sel,t)=>tl.to(sel,{opacity:0,y:-24,scale:.97,filter:"blur(8px)",duration:.35,ease:"power2.in"},t);
const sheen=(sel,t)=>tl.fromTo(sel+" .sheen",{xPercent:-150},{xPercent:330,duration:1.0,ease:"power2.inOut"},t);
// counter
inn("#count",3.0); sheen("#count",3.5);
const c={v:0}; tl.to(c,{v:3605904,duration:1.6,ease:"power3.out",onUpdate:()=>{document.getElementById("num").textContent=fmt(c.v)}},3.1);
tl.set("#num",{textContent:fmt(3605904)},4.75);
out("#count",6.5);
// chips
["#chip1","#chip2","#chip3"].forEach((s,i)=>{tl.fromTo(s,{opacity:0,x:120,filter:"blur(10px)"},{opacity:1,x:0,filter:"blur(0px)",duration:.5,ease:"back.out(1.5)"},10.6+i*.3);});
tl.to(["#chip1","#chip2","#chip3"],{opacity:0,x:60,duration:.3,stagger:.05,ease:"power2.in"},12.7);
// protection
inn("#prot",13.4); sheen("#prot",13.9); out("#prot",15.5);
// collector
inn("#coll",16.1); tl.to("#sp",{strokeDashoffset:0,duration:.9,ease:"power2.out"},16.4); out("#coll",17.55);
// freeze + panel
tl.fromTo("#freeze",{opacity:0},{opacity:1,duration:.25},17.9);
tl.fromTo("#panel",{opacity:0,y:60,scale:.92},{opacity:1,y:0,scale:1,duration:.6,ease:"back.out(1.4)"},18.05);
tl.fromTo("#pline",{scaleX:0},{scaleX:1,duration:.6,ease:"power3.out"},18.3);
sheen("#panel",18.5);
for(let i=0;i<5;i++){const t=18.55+i*.32;
 tl.fromTo("#pi"+i,{opacity:0,x:-40},{opacity:1,x:0,duration:.4,ease:"power3.out"},t);
 tl.to("#pi"+i+" .ckp",{strokeDashoffset:0,duration:.35,ease:"power2.out"},t+.12);}
tl.to("#panel",{opacity:0,scale:1.04,filter:"blur(10px)",duration:.35,ease:"power2.in"},22.3);
tl.to("#freeze",{opacity:0,duration:.2},22.55);
// end
tl.fromTo("#wm",{opacity:0,y:30,filter:"blur(12px)"},{opacity:1,y:0,filter:"blur(0px)",duration:.6,ease:"power3.out"},24.7);
tl.fromTo("#ctag",{opacity:0,y:20,scale:1.15},{opacity:1,y:0,scale:1,duration:.7,ease:"power3.out"},25.0);
tl.fromTo("#fade",{opacity:0},{opacity:1,duration:.4},26.6);
window.__timelines=window.__timelines||{}; window.__timelines["main"]=tl;
</script>
</body>
</html>
