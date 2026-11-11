import cv2, numpy as np
def save(name, bgr, m):
    rgba=cv2.cvtColor(bgr,cv2.COLOR_BGR2BGRA); rgba[:,:,3]=m
    ys,xs=np.where(m>10); rgba=rgba[ys.min():ys.max()+1, xs.min():xs.max()+1]; cv2.imwrite(f"cut/{name}.png",rgba); return rgba.shape
# bowl: hand polygon, smoothed
im=cv2.imread('src/1.webp')
pts=np.array([(5,405),(22,368),(60,338),(120,312),(200,293),(300,282),(400,280),(500,288),(590,305),(650,322),(688,336),(688,612),(650,650),(590,690),(510,728),(420,748),(320,748),(220,725),(140,680),(80,622),(40,560),(12,480)],np.int32)
m=np.zeros(im.shape[:2],np.uint8); cv2.fillPoly(m,[pts],255); m=cv2.GaussianBlur(m,(7,7),0)
print('bowl',save('bowl',im,m))
# almonds: saturation threshold inside rects
im=cv2.imread('src/2.jpg'); hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
for i,(x0,y0,x1,y1) in enumerate([(55,560,100,603),(15,618,90,668),(8,673,58,740),(58,673,105,750)]):
    sub=hsv[y0:y1,x0:x1]; mm=((sub[:,:,1]>90)&(sub[:,:,0]<30)).astype(np.uint8)*255
    mm=cv2.morphologyEx(mm,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(mm); k=1+np.argmax(st[1:,4]); mm=np.where(lab==k,255,0).astype(np.uint8)
    cnts,_=cv2.findContours(mm,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); mm[:]=0; cv2.drawContours(mm,cnts,-1,255,-1); mm=cv2.GaussianBlur(mm,(3,3),0)
    print('almond',i,save(f'almond{i}',im[y0:y1,x0:x1],mm))
# cacao nibs: falling nibs on black (img4) -> components
im=cv2.imread('src/4.jpg'); 
sub=im[190:470,20:183]; g=cv2.cvtColor(sub,cv2.COLOR_BGR2GRAY); mm=(g>38).astype(np.uint8)*255
n,lab,st,_=cv2.connectedComponentsWithStats(mm); c=0
order=np.argsort(-st[1:,4])
for k in order[:14]:
    k+=1; x,y,w,h,a=st[k]
    if a<25: continue
    pm=np.where(lab[y:y+h,x:x+w]==k,255,0).astype(np.uint8); pm=np.pad(pm,2); piece=np.pad(sub[y:y+h,x:x+w],((2,2),(2,2),(0,0)))
    save(f'nib{c}',piece,cv2.GaussianBlur(pm,(3,3),0)); c+=1
print('nibs',c)
# nib pile
sub=im[722:775,505:700]; g=cv2.cvtColor(sub,cv2.COLOR_BGR2GRAY); mm=(g>40).astype(np.uint8)*255; mm=cv2.GaussianBlur(mm,(3,3),0)
print('pile',save('nibpile',sub,mm))
# puffies: loose on white (img3)
im=cv2.imread('src/3.jpg'); sub=im[770:822,0:240]; hsv=cv2.cvtColor(sub,cv2.COLOR_BGR2HSV)
mm=((hsv[:,:,1]>55)&(hsv[:,:,0]<35)).astype(np.uint8)*255; mm=cv2.morphologyEx(mm,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
n,lab,st,_=cv2.connectedComponentsWithStats(mm); c=0
for k in np.argsort(-st[1:,4])[:12]:
    k+=1; x,y,w,h,a=st[k]
    if a<30: continue
    pm=np.where(lab[y:y+h,x:x+w]==k,255,0).astype(np.uint8); pm=np.pad(pm,2); piece=np.pad(sub[y:y+h,x:x+w],((2,2),(2,2),(0,0)))
    save(f'puff{c}',piece,cv2.GaussianBlur(pm,(3,3),0)); c+=1
print('puffs',c)
# prozis logo -> white on transparent
lg=cv2.imread('site/logo-blk.png',cv2.IMREAD_UNCHANGED); g=cv2.cvtColor(lg[:,:,:3],cv2.COLOR_BGR2GRAY)
w=np.full(lg.shape[:2]+(3,),255,np.uint8); print('logo',save('prozis_logo',w,g))
