import cv2,numpy as np,sys,subprocess
sys.path.insert(0,'.');from screenpatch import *
raw,out,Wf=sys.argv[1:4]
cap=cv2.VideoCapture(raw);F=[]
while True:
    ok,f=cap.read()
    if not ok:break
    F.append(f)
a,b,ri=248,309,264
bx=[dict(box=(180,365,242,384),pad=1,text='Collector',f='m',size=11.3,color=(245,250,250),w=90,rot=-6)]
W=list(np.load(Wf));ref=F[ri];P,M=render_patch(ref,bx)
F[a:b]=apply(F[a:b],W,ref,P,M)
h,w=F[0].shape[:2]
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}','-r','24','-i','-','-i',raw,'-map','0:v','-map','1:a','-c:v','libx264','-crf','12','-preset','medium','-pix_fmt','yuv420p','-c:a','copy',out],stdin=subprocess.PIPE)
for f in F: p.stdin.write(f.tobytes())
p.stdin.close();p.wait()
