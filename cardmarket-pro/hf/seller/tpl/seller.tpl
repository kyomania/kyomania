<!doctype html>
<html lang="%%LANG%%" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=834, height=1112" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{font-family:"InterL";src:url(assets/fonts/Inter-Regular.otf);font-weight:400}
@font-face{font-family:"InterL";src:url(assets/fonts/Inter-Medium.otf);font-weight:500}
@font-face{font-family:"InterL";src:url(assets/fonts/Inter-SemiBold.otf);font-weight:600}
@font-face{font-family:"InterL";src:url(assets/fonts/Inter-Bold.otf);font-weight:700}
@font-face{font-family:"InterD";src:url(assets/fonts/InterDisplay-Bold.otf);font-weight:700}
@font-face{font-family:"InterD";src:url(assets/fonts/InterDisplay-SemiBold.otf);font-weight:600}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:834px;height:1112px;overflow:hidden;background:#000}
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
#panel{left:44px;top:205px;width:746px;height:650px}
#ptitle{position:absolute;left:0;width:100%;top:40px;text-align:center;font-family:"InterD";font-weight:700;font-size:54px;color:#5eead4;letter-spacing:-.5px}
#psub{position:absolute;left:0;width:100%;top:108px;text-align:center;font-size:25px;color:rgba(224,255,250,.75)}
#pline{position:absolute;left:46px;top:156px;height:3px;width:654px;background:linear-gradient(90deg,rgba(45,212,191,0),#2dd4bf,rgba(45,212,191,0))}
#plist{position:absolute;left:46px;top:178px;list-style:none}
.pi{display:flex;align-items:center;height:72px;font-size:29px;font-weight:600;white-space:nowrap}
.ck{width:40px;height:40px;margin-right:20px;flex:none}
.ck circle{fill:rgba(45,212,191,.16);stroke:#2dd4bf;stroke-width:1.4}
.ckp{fill:none;stroke:#5eead4;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:20;stroke-dashoffset:20}
#pfoot{position:absolute;left:0;width:100%;top:570px;text-align:center;font-size:22px;color:rgba(224,255,250,.6)}
#freeze{filter:blur(18px) brightness(.55);transform:scale(1.08)}
#wm{position:absolute;left:192px;top:745px;width:450px}
#fade{position:absolute;inset:0;background:#000;opacity:0}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%DUR%%" data-width="834" data-height="1112">
 <video id="segA" class="clip full" src="raw.mp4" muted playsinline data-start="0" data-duration="5.46" data-media-start="0" data-track-index="0"></video>
 <video id="segB" class="clip full" src="raw.mp4" muted playsinline data-start="5.46" data-duration="10.25" data-media-start="6.21" data-track-index="1"></video>
 <audio id="musA" src="raw.mp4" data-start="0" data-duration="5.46" data-media-start="0" data-track-index="5" data-volume="1"></audio>
 <audio id="musA2" src="raw.mp4" data-start="5.46" data-duration="10.25" data-media-start="6.21" data-track-index="6" data-volume="1"></audio>
 <img id="freeze" class="clip full" src="assets/freeze.png" data-start="15.71" data-duration="6.79" data-track-index="0">
 <audio id="musB" src="raw.mp4" data-start="15.71" data-duration="6.79" data-media-start="2.0" data-track-index="7" data-volume="0.8"></audio>
 <video id="segD" class="clip full" src="raw.mp4" muted playsinline data-start="22.5" data-duration="3.54" data-media-start="16.46" data-track-index="1"></video>
 <audio id="musD" src="raw.mp4" data-start="22.5" data-duration="3.54" data-media-start="16.46" data-track-index="8" data-volume="1"></audio>
 <img id="hold" class="clip full" src="assets/rawend.png" data-start="26.04" data-duration="%%HOLD%%" data-track-index="0">
%%AUDIO%%
 <div id="panel" class="glass clip" data-start="15.9" data-duration="6.4" data-track-index="2"><div class="sheen"></div>
  <div id="ptitle">%%title%%</div><div id="psub">%%sub%%</div><div id="pline"></div><ul id="plist">%%ITEMS%%</ul><div id="pfoot">%%foot%%</div></div>
 <img id="wm" class="clip" src="assets/wordmark.png" data-start="25.9" data-duration="%%WMD%%" data-track-index="3" style="mix-blend-mode:screen">
 <div id="fade" class="clip" data-start="%%FADE%%" data-duration="0.4" data-track-index="9"></div>
</div>
<script>
const tl=gsap.timeline({paused:true});
tl.fromTo("#freeze",{opacity:0},{opacity:1,duration:.35},15.71);
tl.fromTo("#panel",{opacity:0,y:50,scale:.92},{opacity:1,y:0,scale:1,duration:.6,ease:"back.out(1.4)"},15.9);
tl.fromTo("#pline",{scaleX:0},{scaleX:1,duration:.6,ease:"power3.out"},16.2);
tl.fromTo("#panel .sheen",{xPercent:-150},{xPercent:330,duration:1.0,ease:"power2.inOut"},16.4);
for(let i=0;i<5;i++){const t=16.6+i*.42;
 tl.fromTo("#pi"+i,{opacity:0,x:-36},{opacity:1,x:0,duration:.4,ease:"power3.out"},t);
 tl.to("#pi"+i+" .ckp",{strokeDashoffset:0,duration:.35,ease:"power2.out"},t+.12);}
tl.fromTo("#pfoot",{opacity:0},{opacity:1,duration:.5},18.9);
tl.to("#panel",{opacity:0,scale:1.04,filter:"blur(10px)",duration:.35,ease:"power2.in"},21.95);
tl.to("#freeze",{opacity:0,duration:.2},22.3);
tl.fromTo("#wm",{opacity:0,y:24,filter:"blur(12px)"},{opacity:1,y:0,filter:"blur(0px)",duration:.6,ease:"power3.out"},25.9);
tl.fromTo("#fade",{opacity:0},{opacity:1,duration:.4},%%FADE%%);
window.__timelines=window.__timelines||{}; window.__timelines["main"]=tl;
</script>
</body>
</html>
