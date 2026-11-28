import json,sys,subprocess
L=sys.argv[1];F=sys.argv[2] if len(sys.argv)>2 else '9x16'
d=json.load(open('../../prompts/buy1-app-seller-vo.json'))['APP']
S={"title":"Eine App. Alles drin.","tiles":[["Kaufen","3,6 Mio. Karten"],["Sammeln","Täglicher Sammlungswert"],["Tables","Live handeln & tauschen"],["Verkaufen","0 % Provision*"]],"foot":"* derzeit, zzgl. Zahlungsentgelt"} if L=='DE' else d[L]['screen']
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
if L=='DE': vo=[('APP-DE-full.wav',0.0,dur('assets/vo/APP-DE-full.wav'))]
else:
  vo=[];e=0
  for i,t in enumerate([0,8.88,17.0,24.7]):
    f=f'APP-{L}-{i}.mp3';s=max(t,e+0.12);D=dur('assets/vo/'+f);vo.append((f,s,D));e=s+D
assert vo[-1][1]+vo[-1][2]<=28.45,vo
aud=''.join(f'<audio id="vo{i}" src="assets/vo/{f}" data-start="{s:.2f}" data-duration="{D:.2f}" data-track-index="{10+i}" data-volume="1"></audio>\n' for i,(f,s,D) in enumerate(vo))
IC=['<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2.5 3.5h3l2.4 11.5h11l2-8H7"/>','<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M6.5 16l3.5-4 3 2.5 4.5-5.5"/>','<circle cx="8.5" cy="8" r="3.2"/><circle cx="16.5" cy="9.5" r="2.6"/><path d="M2.5 20c.6-3.6 3-5.6 6-5.6s5.4 2 6 5.6"/><path d="M15 14.6c2.8-.3 5 1.4 5.8 4.6"/>','<path d="M3.5 12.5V4.5a1 1 0 011-1h8l8 8-9 9z"/><circle cx="8" cy="8" r="1.6"/>']
esc=lambda s:s.replace('&','&amp;')
tiles=''.join(f'<div id="t{i}" class="glass tile"><div class="sheen"></div><div class="ib"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{IC[i]}</svg></div><div class="n">{esc(n)}</div><div class="s">{esc(s)}</div></div>' for i,(n,s) in enumerate(S['tiles']))
h=open('tpl/app.tpl').read()
for k,v in dict(AUDIO=aud,TILES=tiles,title=esc(S['title']),foot=esc(S['foot'])).items(): h=h.replace('%%'+k+'%%',v)
h=h.replace('lang="de"' if False else '<html lang="%%LANG%%"','<html lang="%s"'%L.lower())
if F=='4x5':
  for a,b in [('height=1920','height=1350'),('data-height="1920"','data-height="1350"'),('height:1920px','height:1350px'),('assets/freeze.png','assets/freeze45.png'),('assets/rawend.png','assets/rawend45.png')]: h=h.replace(a,b)
  h=h.replace('</style>','#title{top:200px}#grid{top:310px}#foot{top:918px}#wm{left:260px;top:1000px;width:560px}\n</style>')
open('index.html','w').write(h);print(vo)
