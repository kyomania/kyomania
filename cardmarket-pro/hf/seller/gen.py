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
import sys as _s;_s.path.insert(0,'../tools');from pills import inject
I=lambda p:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'+p+'</svg>'
ISC=I('<path d="M3.5 12.5V4.5a1 1 0 011-1h8l8 8-9 9z"/><circle cx="8" cy="8" r="1.6"/>');ICAM=I('<rect x="3" y="6.5" width="18" height="13" rx="3"/><circle cx="12" cy="13" r="3.6"/><path d="M8.5 6.5l1.5-2.5h4l1.5 2.5"/>');IVER=I('<path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.3-7.5 9.5-4.3-1.2-7.5-4.9-7.5-9.5V6z"/><path d="M8.6 12.2l2.4 2.4 4.4-4.6"/>')
pl=[('p0',7.6,10.35,80,ISC,esc(S['title']),esc(S['sub'])),('p1',10.75,13.05,80,ICAM,esc(S['items'][2]),''),('p2',13.4,15.55,80,IVER,esc(S['items'][4]),'')]
h=inject(h,pl,(16,12,30,58,30,21))
h=h.replace('src="raw.mp4" muted playsinline data-start="5.46"','src="raw_en.mp4" muted playsinline data-start="5.46"').replace('src="raw.mp4" muted playsinline data-start="22.5"','src="raw_en.mp4" muted playsinline data-start="22.5"')
# panel reveal times per VO
if L=='DE': t0,t1,t2=15.9,18.6,20.0
else: t0=vo[5][1];t1=vo[6][1];t2=vo[6][1]+0.45*vo[6][2]
t0=min(max(t0,16.6),20.0);t1=min(max(t1,t0+0.5),20.6);t2=min(max(t2,t1+0.5),21.2)
PT=[t0,t1,16.6,t2,16.85]
h=h.replace('for(let i=0;i<5;i++){const t=16.6+i*.42;','const PT=['+','.join(f'{x:.2f}' for x in PT)+'];for(let i=0;i<5;i++){const t=PT[i];')
open('index.html','w').write(h);print(L,end,vo[-1])
