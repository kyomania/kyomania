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
    """Aussenkontur je Seite: pro Abschnitt der aeusserste Punkt (ignoriert Notch und Finger), runde Ecken ausgelassen."""
    cnts,_=cv2.findContours(mm,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    c=max(cnts,key=cv2.contourArea).reshape(-1,2).astype(np.float64)
    (cx,cy),(w,h),a=cv2.minAreaRect(c.astype(np.float32))
    if w>h: w,h=h,w;a+=90
    t=np.deg2rad(a);ux=np.array([np.cos(t),np.sin(t)]);uy=np.array([-np.sin(t),np.cos(t)])
    p=c-[cx,cy];X=p@ux;Y=p@uy
    H_,W_=mm.shape
    onborder=(c[:,0]<=1)|(c[:,1]<=1)|(c[:,0]>=W_-2)|(c[:,1]>=H_-2)
    spec={'top':(X,-Y,w/2),'bot':(X,Y,w/2),'left':(Y,-X,h/2),'right':(Y,X,h/2)}
    L={};err=[]
    for k,(along,out,half) in spec.items():
        lim=0.9 if k=='top' else 0.78
        sel=(out>0)&(np.abs(along)<half*lim)&~onborder
        if sel.sum()<8: sel=(out>0)&(np.abs(along)<half*lim)
        pts=c[sel];al=along[sel];ou=out[sel]
        bins=np.linspace(-half*lim,half*lim,31);keep=[]
        for b0,b1 in zip(bins[:-1],bins[1:]):
            idx=np.where((al>=b0)&(al<b1))[0]
            if len(idx): keep.append(idx[np.argmax(ou[idx])])
        keep=np.array(keep);P0=pts[keep];E0=ou[keep]
        # RANSAC: Gerade mit den meisten Punkten innerhalb 2,5 px; bei Gleichstand die aeussere (Notch/Finger liegen innen)
        best=None
        for u_ in range(len(P0)):
            for v_ in range(u_+1,len(P0)):
                d=P0[v_]-P0[u_];nd=np.linalg.norm(d)
                if nd<10: continue
                n=np.array([-d[1],d[0]])/nd;r=np.abs((P0-P0[u_])@n);inl=r<2.5
                need=4 if k=='top' else max(4,int(0.3*len(P0)))
                sc=(int(inl.sum()>=need),round(float(E0[inl].mean()),0),inl.sum())
                if best is None or sc>best[0]: best=(sc,inl)
        P=P0[best[1]] if best is not None else P0
        vx,vy,x0,y0=cv2.fitLine(P.astype(np.float32),cv2.DIST_HUBER,0,0.01,0.01).ravel()
        L[k]=(np.array([x0,y0]),np.array([vx,vy]))
        n=np.array([-vy,vx]);err.append(np.abs((P-[x0,y0])@n).max())
    def X_(a,b):
        (p1,d1),(p2,d2)=L[a],L[b];A=np.array([d1,-d2]).T;s_=np.linalg.solve(A,p2-p1);return p1+s_[0]*d1
    q=np.float32([X_('top','left'),X_('top','right'),X_('bot','right'),X_('bot','left')])
    return q,max(err)
def track(frames,thr=(150,80,80)):
    """Pro Bild Kanten-Fit; obere Kante (Notch, winzige Ecken) wird aus stabilen Seitenkanten + fester Bildschirmhoehe abgeleitet."""
    M=[gmask(f,thr) for f in frames];res=[fit_quad(m) for m in M]
    Q=np.array([r[0] for r in res],dtype=np.float64);E=max(r[1] for r in res)
    Lh=np.linalg.norm(Q[:,0]-Q[:,3],axis=1);Rh=np.linalg.norm(Q[:,1]-Q[:,2],axis=1)
    lh,rh=np.median(Lh),np.median(Rh)
    for k in range(len(Q)):
        dl=(Q[k,0]-Q[k,3])/Lh[k];dr=(Q[k,1]-Q[k,2])/Rh[k]
        Q[k,0]=Q[k,3]+dl*lh;Q[k,1]=Q[k,2]+dr*rh
    fast=np.abs(np.diff(Q.mean(1),axis=0)).max()>6 if len(Q)>1 else True
    S=Q.copy()
    if not fast and len(Q)>2:
        P=np.pad(Q,((1,1),(0,0),(0,0)),mode='edge');S=0.25*P[:-2]+0.5*P[1:-1]+0.25*P[2:]
    jump=np.abs(np.diff(S,axis=0)).max() if len(S)>1 else 0
    return S.astype(np.float32),M,{'fit_err_px':round(float(E),1),'max_offset_px':round(float(np.abs(S-Q).max()),1),'max_jump_per_frame_px':round(float(jump),1),'fast':bool(fast)}
def composite(frame,quad,mask,ui_bgr):
    H,W=ui_bgr.shape[:2]
    T=cv2.getPerspectiveTransform(np.float32([[0,0],[W,0],[W,H],[0,H]]),quad)
    wp=cv2.warpPerspective(ui_bgr,T,(frame.shape[1],frame.shape[0]),flags=cv2.INTER_AREA)
    m=cv2.GaussianBlur(cv2.dilate(mask,np.ones((5,5),np.uint8)).astype(np.float32),(5,5),0)[...,None]
    out=(frame*(1-m)+wp*m)
    # Handylicht neutralisieren: gruen/tuerkiser Schein um den Bildschirm (Band 60 px) -> neutrales Weiss
    dist=cv2.distanceTransform((mask==0).astype(np.uint8),cv2.DIST_L2,5)
    w=np.clip(1-dist/60,0,1)*(m[...,0]<0.5)
    B,G,R=out[...,0],out[...,1],out[...,2]
    lum=0.3*R+0.4*G+0.3*B
    tint=np.clip(((G+B)/2-R-8)/30,0,1)*w
    for c in range(3): out[...,c]=out[...,c]*(1-tint)+lum*tint
    return out.astype(np.uint8)
