# Track phone screen by optical flow on screen-edge points + RANSAC homography; measure jitter
import sys,cv2,numpy as np
from scipy import ndimage
sys.path.insert(0,'/tmp/claude-0/-home-user-kyomania/5ad058ef-4988-5e8f-8beb-41f6d96aa4d1/scratchpad')
from ui2 import stock,portfolio
src,dst=sys.argv[1],sys.argv[2]
segs=[(23,37,stock),(38,62,stock),(72,89,portfolio),(90,131,stock)]
def gmask(img):
    B,G,R=[img[...,k].astype(int) for k in range(3)]
    m=(G>150)&(G-R>80)&(G-B>80)
    lab,n=ndimage.label(m);s=ndimage.sum(m,lab,range(1,n+1))
    return ndimage.binary_fill_holes(lab==s.argmax()+1).astype(np.uint8)
def rect(mm):
    cnts,_=cv2.findContours(mm,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    c=max(cnts,key=cv2.contourArea)
    (cx,cy),(w,h),a=cv2.minAreaRect(c)
    if w>h: w,h=h,w;a+=90
    if a>45:a-=90
    if a<-45:a+=90
    return np.array([cx,cy,w,h,a])
def quad(r):
    cx,cy,w,h,a=r;t=np.deg2rad(a);R=np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])
    p=np.array([[-w/2,-h/2],[w/2,-h/2],[w/2,h/2],[-w/2,h/2]])
    return (p@R.T+[cx,cy]).astype(np.float32)
report=[]
for a,b,fn in segs:
    ks=list(range(a,b+1));imgs={i:cv2.imread(f'{src}/{i:04d}.png') for i in ks};M={i:gmask(imgs[i]) for i in ks}
    raw=np.array([rect(M[i]) for i in ks])
    # light smoothing: 3-tap on centre/angle only, size = segment median (size barely changes)
    sm=raw.copy()
    fast=np.abs(np.diff(raw[:,:2],axis=0)).max()>6
    for d in ((0,1,4) if not fast else ()):
        sm[:,d]=np.convolve(np.pad(raw[:,d],1,mode='edge'),[0.25,0.5,0.25],'valid')
    for d in (2,3): sm[:,d]=np.median(raw[:,d])  # if size varies strongly keep raw
    if np.ptp(raw[:,3])>25 or fast: sm[:,2:4]=raw[:,2:4]
    w,h=np.median(raw[:,2]),np.median(raw[:,3]);W=520;H=int(W*h/w)
    u=cv2.cvtColor(np.asarray(fn(W,H)),cv2.COLOR_RGB2BGR)
    jit=[]
    for k,i in enumerate(ks):
        q=quad(sm[k]);T=cv2.getPerspectiveTransform(np.float32([[0,0],[W,0],[W,H],[0,H]]),q)
        img=imgs[i];wp=cv2.warpPerspective(u,T,(img.shape[1],img.shape[0]),flags=cv2.INTER_LINEAR)
        m=cv2.GaussianBlur(cv2.dilate(M[i],np.ones((5,5),np.uint8)).astype(np.float32),(5,5),0)[...,None]
        cv2.imwrite(f'{dst}/{i:04d}.png',(img*(1-m)+wp*m).astype(np.uint8))
        jit.append(np.abs(quad(raw[k])-q).max())
    # frame-to-frame motion of UI vs of real screen (wobble = difference)
    dUI=np.diff(sm[:,:2],axis=0);dReal=np.diff(raw[:,:2],axis=0)
    report.append((a,b,round(float(np.max(jit)),1),round(float(np.abs(dUI-dReal).max()),1),round(float(np.ptp(raw[:,4])),1)))
for r in report: print('seg %d-%d  max offset UI vs screen %.1f px | max relative slip/frame %.1f px | angle range %.1f deg'%r)
