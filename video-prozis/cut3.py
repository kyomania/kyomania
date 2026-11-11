import cv2, numpy as np
def save(name,bgr,m):
    rgba=cv2.cvtColor(bgr,cv2.COLOR_BGR2BGRA); rgba[:,:,3]=m
    ys,xs=np.where(m>10); rgba=rgba[ys.min():ys.max()+1, xs.min():xs.max()+1]; cv2.imwrite(f"cut/{name}.png",rgba); print(name,rgba.shape)
def rrect(shape,x0,y0,x1,y1,rt,rb):
    m=np.zeros(shape,np.uint8); cv2.rectangle(m,(x0+rt,y0),(x1-rt,y1-rb),255,-1); cv2.rectangle(m,(x0,y0+rt),(x1,y1-rb),255,-1)
    cv2.rectangle(m,(x0+rb,y0+rt),(x1-rb,y1),255,-1)
    for cx,cy,r in [(x0+rt,y0+rt,rt),(x1-rt,y0+rt,rt),(x0+rb,y1-rb,rb),(x1-rb,y1-rb,rb)]: cv2.circle(m,(cx,cy),r,255,-1)
    return m
def grab(im,rect,it=8):
    m=np.zeros(im.shape[:2],np.uint8); b=np.zeros((1,65)); f=np.zeros((1,65))
    cv2.grabCut(im,m,rect,b,f,it,cv2.GC_INIT_WITH_RECT); return np.where((m==1)|(m==3),255,0).astype(np.uint8)
def fill_keep(m,minarea):
    n,lab,st,_=cv2.connectedComponentsWithStats(m); out=np.zeros_like(m)
    for k in range(1,n):
        if st[k,4]>=minarea: out[lab==k]=255
    cnts,_=cv2.findContours(out,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); out[:]=0; cv2.drawContours(out,cnts,-1,255,-1); return out
# agave: symmetric profile
im=cv2.imread('src/5.jpg'); cx=398.5
prof=[(166,66),(172,74),(232,76),(250,84),(268,94),(288,103),(310,106),(718,106),(728,102),(734,94)]
pts=[(cx-w,y) for y,w in prof]+[(cx+w,y) for y,w in reversed(prof)]
m=np.zeros(im.shape[:2],np.uint8); cv2.fillPoly(m,[np.array(pts,np.int32)],255); m=cv2.GaussianBlur(m,(5,5),0)
save('pack_agave',im,m)
# peanut butter jar
im=cv2.imread('src/6.jpg'); m=rrect(im.shape[:2],174,172,567,764,22,26); m=cv2.GaussianBlur(m,(5,5),0); save('pack_pb',im,m)
# oats bag
im=cv2.imread('src/8.jpg'); m=np.zeros(im.shape[:2],np.uint8); cv2.rectangle(m,(189,189),(547,761),255,-1); m=cv2.GaussianBlur(m,(5,5),0); save('pack_oats',im,m)
# oat clumps from label window
for i,(x,y) in enumerate([(305,545),(345,535),(385,550),(320,590),(360,600),(400,590),(330,630),(380,635)]):
    p=im[y:y+34,x:x+42].copy(); mm=np.zeros(p.shape[:2],np.uint8); cv2.ellipse(mm,(21,17),(19,14),(i*23)%180,0,360,255,-1); mm=cv2.GaussianBlur(mm,(7,7),0); save(f'oat{i}',p,mm)
# protein pouch with chocolate
im=cv2.imread('src/7.jpg'); m=np.zeros(im.shape[:2],np.uint8); cv2.fillPoly(m,[np.array([(155,316),(587,316),(587,860),(580,876),(562,885),(180,885),(162,876),(155,860)],np.int32)],255); m=cv2.GaussianBlur(m,(5,5),0); save('pack_protein',im,m)
for i,(x0,y0,x1,y1) in enumerate([(425,262,532,325),(528,358,638,466),(50,370,158,484),(30,635,252,800),(552,635,722,780)]):
    sub=im[y0:y1,x0:x1].copy(); mm=grab(sub,(3,3,x1-x0-6,y1-y0-6)); mm=fill_keep(mm,200); mm=cv2.GaussianBlur(mm,(3,3),0); save(f'choc{i}',sub,mm)
# peanuts
im=cv2.imread('src/6.jpg')
for i,(x0,y0,x1,y1) in enumerate([(65,685,166,758),(88,568,165,655),(0,700,75,770)]):
    sub=im[y0:y1,x0:x1].copy(); mm=grab(sub,(3,3,x1-x0-6,y1-y0-6)); mm=fill_keep(mm,200); mm=cv2.GaussianBlur(mm,(3,3),0)
    try: save(f'peanut{i}',sub,mm)
    except ValueError: print('skip peanut',i)
# hero bowl on white
im=cv2.imread('src/9.webp'); mn=im.min(2); m=(mn<226).astype(np.uint8)*255
m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8)); m=fill_keep(m,20000); poly=np.zeros_like(m); cv2.fillPoly(poly,[np.array([(0,0),(688,0),(688,470),(664,550),(642,600),(600,650),(530,692),(470,712),(420,722),(300,724),(240,718),(160,690),(90,650),(48,600),(26,550),(0,470)],np.int32)],255); m=cv2.bitwise_and(m,poly); m=cv2.GaussianBlur(m,(5,5),0); save('hero_bowl',im,m)
