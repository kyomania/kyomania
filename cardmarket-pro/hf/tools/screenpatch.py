# Replace fake UI text on a tracked phone screen. Delta-patch: out = frame + warp(patchRef - ref) * mask * (1-occlusion)
import cv2,numpy as np,json,sys,subprocess
from PIL import Image,ImageDraw,ImageFont
FONTS={'b':'/usr/share/fonts/opentype/inter/Inter-Bold.otf','s':'/usr/share/fonts/opentype/inter/Inter-SemiBold.otf','m':'/usr/share/fonts/opentype/inter/Inter-Medium.otf','r':'/usr/share/fonts/opentype/inter/Inter-Regular.otf'}
def ink_bbox(img,bg,thr=45):
    d=np.abs(img.astype(np.float32)-bg).max(2)>thr
    ys,xs=np.nonzero(d)
    if len(xs)<4: return None
    return xs.min(),ys.min(),xs.max()+1,ys.max()+1
def render_patch(ref,boxes,SS=6):
    P=ref.astype(np.float32).copy();M=np.zeros(ref.shape[:2],np.float32)
    for b in boxes:
        x0,y0,x1,y1=b['box'];pad=b.get('pad',2)
        X0,Y0,X1,Y1=x0-pad,y0-pad,x1+pad,y1+pad
        ring=np.concatenate([ref[Y0-2:Y0,X0:X1].reshape(-1,3),ref[Y1:Y1+2,X0:X1].reshape(-1,3),ref[Y0:Y1,X1:X1+2].reshape(-1,3)])
        bg=np.median(ring,0) if 'bg' not in b else np.array(b['bg'][::-1],np.float32)
        old=ink_bbox(ref[Y0:Y1,X0:X1],bg)
        P[Y0:Y1,X0:X1]=bg
        if b.get('text'):
            f=ImageFont.truetype(FONTS[b.get('f','r')],int(b['size']*SS))
            bgc=tuple(int(v) for v in bg[::-1])
            # render on big canvas, then crop by ink
            tmp=Image.new('RGB',(int(f.getlength(b['text']))+8*SS,int(b['size']*SS*2)),bgc);d=ImageDraw.Draw(tmp)
            d.text((4*SS,int(b['size']*SS*0.3)),b['text'],font=f,fill=tuple(b['color']))
            if b.get('rot'): tmp=tmp.rotate(-b['rot'],resample=Image.BICUBIC,expand=True,fillcolor=bgc)
            A=np.asarray(tmp).astype(np.float32)[:,:,::-1]
            ib=ink_bbox(A,np.array(bg,np.float32),30)
            ax0,ay0,ax1,ay1=ib
            # target position from old ink: left/top (or centre-x/top)
            if old is None: ox0,oy0,ox1,oy1=0,0,X1-X0,Y1-Y0
            else: ox0,oy0,ox1,oy1=old
            if b.get('align')=='r': tx=X0+ox1-(ax1-ax0)/SS
            elif b.get('align')=='c': tx=X0+(ox0+ox1)/2-(ax1-ax0)/SS/2
            else: tx=X0+ox0
            ty=Y0+oy0+b.get('dy',0)
            # place: shift so ink top-left -> (tx,ty) at full res via subpixel affine
            Hh,Ww=A.shape[:2]
            Mx=np.float32([[1/SS,0,tx-ax0/SS],[0,1/SS,ty-ay0/SS]])
            big=cv2.resize(A,None,fx=1,fy=1)
            small=cv2.warpAffine(cv2.GaussianBlur(big,(0,0),SS*0.45),Mx,(ref.shape[1],ref.shape[0]),flags=cv2.INTER_AREA if False else cv2.INTER_LINEAR,borderValue=tuple(float(v) for v in bg))
            mk=np.zeros(ref.shape[:2],np.float32)
            ex0,ey0=int(tx)-1,int(ty)-2;ex1,ey1=int(tx+(ax1-ax0)/SS)+2,int(ty+(ay1-ay0)/SS)+3
            mk[ey0:ey1,ex0:ex1]=1
            P[ey0:ey1,ex0:ex1]=small[ey0:ey1,ex0:ex1]
            X0,Y0,X1,Y1=min(X0,ex0),min(Y0,ey0),max(X1,ex1),max(Y1,ey1)
        M[Y0:Y1,X0:X1]=1
    M=cv2.GaussianBlur(cv2.dilate(M,np.ones((3,3))),(5,5),1.2)
    return P,M
def track(frames,ref_i,rect):
    x,y,w,h=rect;g=lambda f:cv2.GaussianBlur(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),(3,3),0).astype(np.float32)
    R=g(frames[ref_i]);tmpl=R[y:y+h,x:x+w];mask=np.zeros(R.shape,np.uint8);mask[y:y+h,x:x+w]=255
    Ws=[None]*len(frames);Ws[ref_i]=np.eye(3,dtype=np.float32)
    crit=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,200,1e-5)
    for order in (range(ref_i+1,len(frames)),range(ref_i-1,-1,-1)):
        prev=np.eye(3,dtype=np.float32);sc=[]
        for i in order:
            Wm=prev.copy()
            try: _,Wm=cv2.findTransformECC(R,g(frames[i]),Wm,cv2.MOTION_HOMOGRAPHY,crit,mask,5)
            except cv2.error: pass
            Ws[i]=Wm;prev=Wm
    return Ws
def smooth(Ws,rect):
    x,y,w,h=rect;pts=np.float32([[x,y],[x+w,y],[x+w,y+h],[x,y+h]]).reshape(-1,1,2)
    C=np.stack([cv2.perspectiveTransform(pts,W).reshape(-1) for W in Ws])
    ctr=C.reshape(len(C),4,2).mean(1);v=np.r_[0,np.linalg.norm(np.diff(ctr,axis=0),axis=1)]
    S=C.copy()
    for i in range(len(C)):
        if v[max(0,i-1):i+2].max()<1.5:
            a,b=max(0,i-3),min(len(C),i+4);S[i]=C[a:b].mean(0)
    return [cv2.getPerspectiveTransform(pts.reshape(4,2),s.reshape(4,2).astype(np.float32)) for s in S],S
def apply(frames,Ws,ref,P,M,occ=35):
    D=P-ref.astype(np.float32);out=[];h,w=ref.shape[:2]
    for f,W in zip(frames,Ws):
        Dw=cv2.warpPerspective(D,W,(w,h),flags=cv2.INTER_LINEAR);Mw=cv2.warpPerspective(M,W,(w,h))
        Rw=cv2.warpPerspective(ref.astype(np.float32),W,(w,h))
        fl=cv2.cvtColor(f,cv2.COLOR_BGR2LAB).astype(np.float32);rl=cv2.cvtColor(np.clip(Rw,0,255).astype(np.uint8),cv2.COLOR_BGR2LAB).astype(np.float32)
        ch=np.abs(fl[:,:,1:]-rl[:,:,1:]).max(2);lu=cv2.blur(np.abs(fl[:,:,0]-rl[:,:,0]),(21,21))
        o=np.clip((cv2.blur(ch,(15,15))-8)/6,0,1);o=np.maximum(o,np.clip((lu-40)/15,0,1))
        o=cv2.dilate(o,np.ones((5,5)));o=cv2.GaussianBlur(o,(7,7),2)
        a=(Mw*(1-o))[:,:,None]
        Pw=cv2.warpPerspective(P,W,(w,h),flags=cv2.INTER_LINEAR)
        L=cv2.GaussianBlur(f.astype(np.float32)-Rw,(0,0),8)
        new=Pw+L
        TD=globals().get('TRANSLUCENT',0.0)
        base=f*(1-a)+new*a
        if TD: base=base+(Pw-Rw)*(Mw*o*TD)[:,:,None]
        out.append(np.clip(base,0,255).astype(np.uint8))
    return out
