import cv2,numpy as np,sys
sys.path.insert(0,'.');from screenpatch import *
cap=cv2.VideoCapture(sys.argv[6] if len(sys.argv)>6 else '../seller/raw.mp4');F=[]
while True:
    ok,f=cap.read()
    if not ok:break
    F.append(f)
print(len(F))
a,b=int(sys.argv[1]),int(sys.argv[2]);ri=int(sys.argv[3]);rect=tuple(map(int,sys.argv[4].split(',')))
seg=F[a:b];Ws=track(seg,ri-a,rect);Wsm,C=smooth(Ws,rect)
ctr=C.reshape(len(C),4,2).mean(1);acc=np.abs(np.diff(ctr,2,axis=0)).max(1)
print('motion range',ctr.min(0),ctr.max(0),'max 2nd deriv',acc.max().round(2))
np.save(sys.argv[5],np.stack(Wsm))
