import json,sys,subprocess
L=sys.argv[1]
d=json.load(open('../../prompts/buy1-app-seller-vo.json'))['BUY1']
DE={"count_sub":"Karten im Katalog","count_meta":"22 Spiele · 5 Sportarten","chip1":"Mit Foto finden","chip2":"Preise vergleichen","chip3":"Graded & versiegelt","prot_t":"Käuferschutz","prot_b1":"Der Verkäufer wird erst bezahlt,","prot_b2":"wenn deine Karte angekommen ist.","coll_t":"Direkt im Collector","coll_b":"mit Kaufpreis & täglichem Wert","panel_t":"Kaufen auf cardmarket.pro","panel":["3,6 Mio. Karten im Katalog","Mit Foto finden & Preise vergleichen","Graded-Karten & versiegelte Produkte","Käuferschutz bis zur Empfangsbestätigung","Käufe landen automatisch im Collector"]}
S=DE if L=='DE' else d[L]['screen']
sep={'EN':',','FR':' '}.get(L,'.')
A='../../audio/vo-3videos/'
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
vo=[]
if L=='DE': vo=[('BUY1-DE-full.mp3',0.0,dur(A+'BUY1-DE-full.mp3'))]
else:
  e=0
  for i,t in enumerate(d['t']):
    f=f'BUY1-{L}-{i}.mp3'; s=max(t,e+0.12); D=dur(A+f); vo.append((f,s,D)); e=s+D
assert vo[-1][1]+vo[-1][2]<=27.0, vo[-1]
aud=''.join(f'<audio id="vo{i}" src="assets/vo/{f}" data-start="{s:.2f}" data-duration="{D:.2f}" data-track-index="{10+i}" data-volume="1"></audio>\n' for i,(f,s,D) in enumerate(vo))
ICON={'search':'<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>','cam':'<rect x="3" y="6.5" width="18" height="13" rx="3"/><circle cx="12" cy="13" r="3.6"/><path d="M8.5 6.5l1.5-2.5h4l1.5 2.5"/>','chart':'<path d="M3 20h18"/><path d="M4 16l5-5 4 3 7-7"/><path d="M15 7h5v5"/>','box':'<rect x="4" y="3" width="16" height="18" rx="2.5"/><path d="M8 7h8"/><path d="M8 17l3-4 2 2 3-4"/>','shield':'<path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.3-7.5 9.5-4.3-1.2-7.5-4.9-7.5-9.5V6z"/><path d="M8.6 12.2l2.4 2.4 4.4-4.6"/>','coll':'<rect x="3" y="4" width="18" height="16" rx="3"/><path d="M6.5 16l3.5-4 3 2.5 4.5-5.5"/>'}
def ic(n): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICON[n]}</svg>'
items=''.join(f'<li class="pi" id="pi{i}"><svg class="ck" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11"/><path class="ckp" d="M7 12.5l3.2 3.2L17.2 8.6"/></svg><span>{t.replace('&','&amp;')}</span></li>' for i,t in enumerate(S['panel']))
h=open('tpl/buy1.tpl').read()
for k,v in dict(ICS=ic('search'),ICC=ic('cam'),ICP=ic('chart'),ICB=ic('box'),ICSH=ic('shield'),ICCO=ic('coll'),ITEMS=items,AUDIO=aud,SEP=sep,LANG=L.lower()).items(): h=h.replace('%%'+k+'%%',v)
for k,v in S.items():
  if isinstance(v,str): h=h.replace('%%'+k+'%%',v.replace('&','&amp;'))
open('index.html','w').write(h)
print(vo)
F=sys.argv[2] if len(sys.argv)>2 else '9x16'
if F=='4x5':
  h=open('index.html').read()
  for a,b in [('height=1920','height=1350'),('data-height="1920"','data-height="1350"'),('height:1920px','height:1350px'),('assets/freeze.png','assets/freeze45.png'),('assets/rawend.png','assets/rawend45.png')]: h=h.replace(a,b)
  h=h.replace('</style>','''#count{top:690px}#chip1{top:190px}#chip2{top:305px}#chip3{top:420px}#prot{top:700px}#coll{top:150px}
#panel{top:325px}#wm{left:240px;top:910px;width:600px}#ctag{top:1010px;font-size:46px}
</style>''')
  open('index.html','w').write(h)
