"""Standard-Verfahren cardmarket.pro: Green-Screen-Handy-Tracking.
Kanten-Fit: Konturpunkte je Bildschirmseite (ohne runde Ecken) -> Geraden -> Schnittpunkte = echte 4 Ecken inkl. Perspektive.
Glaettung nur bei ruhigem Handy (3-Tap), bei schneller Bewegung keine. Misst Fit-Fehler und Rutschen."""
import cv2,numpy as np
from scipy import ndimage
def gmask(img,thr=(150,80,80)):
    B,G,R=[img[...,k].astype(int) for k in range(3)]
    m=(G>thr[0])&(G-R>thr[1])&(G-B>thr[2])
    lab,n=ndimage.label(m);s=ndimage.sum(m,lab,range(1,n+1))
    return ndimage.binary_fill_holes(lab==s.argmax()+1).astype(np.uint8)
def fit_quad(mm):
    cnts,_=cv2.findContours(mm,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    c=max(cnts,key=cv2.contourArea).reshape(-1,2).astype(np.float64)
    (cx,cy),(w,h),a=cv2.minAreaRect(c.astype(np.float32))
    if w>h: w,h=h,w;a+=90
    t=np.deg2rad(a);ux=np.array([np.cos(t),np.sin(t)]);uy=np.array([-np.sin(t),np.cos(t)])
    p=c-[cx,cy];X=p@ux;Y=p@uy
    sides={'top':(Y<-h/2*0.9)&(np.abs(X)<w/2*0.6),'bot':(Y>h/2*0.9)&(np.abs(X)<w/2*0.6),
           'left':(X<-w/2*0.85)&(np.abs(Y)<h/2*0.75),'right':(X>w/2*0.85)&(np.abs(Y)<h/2*0.75)}
    L={};err=0
    for k,sel in sides.items():
        pts=c[sel]
        vx,vy,x0,y0=cv2.fitLine(pts.astype(np.float32),cv2.DIST_HUBER,0,0.01,0.01).ravel()
        L[k]=(np.array([x0,y0]),np.array([vx,vy]))
        n=np.array([-vy,vx]);err=max(err,np.abs((pts-[x0,y0])@n).max())
    def X_(a,b):
        (p1,d1),(p2,d2)=L[a],L[b];A=np.array([d1,-d2]).T;s=np.linalg.solve(A,p2-p1);return p1+s[0]*d1
    q=np.float32([X_('top','left'),X_('top','right'),X_('bot','right'),X_('bot','left')])
    return q,err
def track(frames,thr=(150,80,80)):
    M=[gmask(f,thr) for f in frames];res=[fit_quad(m) for m in M]
    Q=np.array([r[0] for r in res]);E=max(r[1] for r in res)
    fast=np.abs(np.diff(Q.mean(1),axis=0)).max()>6 if len(Q)>1 else True
    S=Q.copy()
    if not fast and len(Q)>2:
        P=np.pad(Q,((1,1),(0,0),(0,0)),mode='edge');S=0.25*P[:-2]+0.5*P[1:-1]+0.25*P[2:]
    slip=np.abs(S-Q).max()
    return S,M,{'fit_err_px':round(float(E),1),'max_offset_px':round(float(slip),1),'fast':bool(fast)}
def composite(frame,quad,mask,ui_bgr):
    H,W=ui_bgr.shape[:2]
    T=cv2.getPerspectiveTransform(np.float32([[0,0],[W,0],[W,H],[0,H]]),quad)
    wp=cv2.warpPerspective(ui_bgr,T,(frame.shape[1],frame.shape[0]),flags=cv2.INTER_AREA)
    m=cv2.GaussianBlur(cv2.dilate(mask,np.ones((5,5),np.uint8)).astype(np.float32),(5,5),0)[...,None]
    return (frame*(1-m)+wp*m).astype(np.uint8)
