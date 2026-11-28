import json,sys,subprocess
L=sys.argv[1]
d=json.load(open('../../prompts/buy1-app-seller-vo.json'))['SELLER']
S={'title':'Seller Center','sub':'Verkaufen in einer App','items':['0 % Verkaufsprovision*','Keine Einstellgebühr','Einstellen per Scan, CSV oder von Hand','Live-Verkauf & Tables','Jedes Konto persönlich geprüft'],'foot':'* derzeit, zzgl. Zahlungsentgelt'} if L=='DE' else d[L]['screen']
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
if L=='DE': vo=[('SELLER-DE-full.wav',0.0,dur('assets/vo/SELLER-DE-full.wav'))]
else:
  vo=[];e=0
  for i,t in enumerate(d['t']):
    f=f'SELLER-{L}-{i}.mp3';s=max(t,e+0.08);D=dur('assets/vo/'+f);vo.append((f,s,D));e=s+D
end=max(27.0,round(vo[-1][1]+vo[-1][2]+0.5,2))
esc=lambda s:s.replace('&','&amp;')
aud=''.join(f'<audio id="vo{i}" src="assets/vo/{f}" data-start="{s:.2f}" data-duration="{D:.2f}" data-track-index="{10+i}" data-volume="1"></audio>\n' for i,(f,s,D) in enumerate(vo))
items=''.join(f'<li class="pi" id="pi{i}"><svg class="ck" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11"/><path class="ckp" d="M7 12.5l3.2 3.2L17.2 8.6"/></svg><span>{esc(t)}</span></li>' for i,t in enumerate(S['items']))
h=open('tpl/seller.tpl').read().replace('<html lang="%%LANG%%"','<html lang="%s"'%L.lower())
for k,v in dict(AUDIO=aud,ITEMS=items,title=esc(S['title']),sub=esc(S['sub']),foot=esc(S['foot']),DUR=f'{end:.2f}',HOLD=f'{end-26.04:.2f}',WMD=f'{end-25.9:.2f}',FADE=f'{end-0.4:.2f}').items(): h=h.replace('%%'+k+'%%',v)
open('index.html','w').write(h);print(L,end,vo[-1])
