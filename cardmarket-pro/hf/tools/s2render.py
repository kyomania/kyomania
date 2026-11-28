import cv2,numpy as np,sys,json
sys.path.insert(0,'.');from screenpatch import *
cap=cv2.VideoCapture('../seller/raw.mp4');F=[]
while True:
    ok,f=cap.read()
    if not ok:break
    F.append(f)
T=json.loads(sys.argv[1])
def boxes_s2(T):
    D=(38,38,40);G=(130,130,135)
    return [dict(box=(318,772,366,783),text=T['h'],f='b',size=8.6,color=D,w=110),
            dict(box=(318,792,392,804),text=T['sub'],f='r',size=7.4,color=G,w=110),
            dict(box=(318,818,350,828),text=T['pl'],f='m',size=7.4,color=(90,90,95)),
            dict(box=(318,833,364,844),text=T['pv'],f='s',size=8,color=D),
            dict(box=(318,870,396,882),text=T['ship'],f='r',size=7.6,color=G,w=110),
            dict(box=(327,924,355,934),text=T['i1'],f='r',size=6,color=G,align='c'),
            dict(box=(387,924,407,933),text=T['i2'],f='r',size=6.4,color=G,w=40),
            dict(box=(382,1010,437,1026),text=T['btn'],f='s',size=8,color=(255,255,255),align='c')]
a,b,ri=332,407,348
W=list(np.load(sys.argv[2]));ref=F[ri]
P,M=render_patch(ref,boxes_s2(T))
out=apply(F[a:b],W,ref,P,M)
np.save(sys.argv[3],np.stack(out))
cv2.imwrite(sys.argv[3]+'.png',cv2.resize(np.hstack([ref[560:1070,280:540],out[ri-a][560:1070,280:540]]),None,fx=3,fy=3,interpolation=cv2.INTER_CUBIC))
