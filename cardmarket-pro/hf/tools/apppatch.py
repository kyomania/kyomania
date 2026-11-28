import cv2,numpy as np,sys,json,subprocess
sys.path.insert(0,'.');import screenpatch;screenpatch.TRANSLUCENT=0.0;from screenpatch import *
WH=(236,240,240);LT=(200,215,215)
def bx(T):
  b=[dict(box=(272,62,564,100),text='cardmarket.pro',f='b',size=26,color=WH,align='c'),
     dict(box=(116,133,474,180),text='Shared Trading Table',f='s',size=34,color=WH,w=420),
     dict(box=(530,535,614,556),text=T['live'],f='b',size=15,color=WH,align='c'),
     dict(box=(172,597,238,621),text='Tables',f='b',size=15,color=(84,214,190),w=80),
     dict(box=(118,660,420,696),text=T['hist'],f='s',size=26,color=WH,w=330)]
  for v,y in zip(['300','250','200','150','100','50','0'],[250,286,322,358,395,431,466]):
     b.append(dict(box=(128,y-8,146,y+8),text=v,f='m',size=9,color=LT,align='r'))
  for v,x in zip(['2023','2024','2025','2026'],[197,247,297,348]):
     b.append(dict(box=(x-15,473,x+15,488),text=v,f='m',size=9,color=LT,align='c'))
  return b
if __name__=='__main__':
  raw,T,out,Wf=sys.argv[1],json.loads(sys.argv[2]),sys.argv[3],sys.argv[4]
  cap=cv2.VideoCapture(raw);F=[]
  while True:
    ok,f=cap.read()
    if not ok:break
    F.append(f)
  a,b,ri=296,351,324
  W=list(np.load(Wf));ref=F[ri];P,M=render_patch(ref,bx(T))
  F[a:b]=apply(F[a:b],W,ref,P,M)
  F[301]=(F[300].astype(np.float32)*0.5+F[301].astype(np.float32)*0+F[304].astype(np.float32)*0.5).astype(np.uint8)
  A_,B_=F[301].astype(np.float32),F[304].astype(np.float32)
  F[302]=(A_*0.6+B_*0.4).astype(np.uint8);F[303]=(A_*0.25+B_*0.75).astype(np.uint8)
  h,w=F[0].shape[:2]
  p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}','-r','24','-i','-','-i',raw,'-map','0:v','-map','1:a','-c:v','libx264','-crf','12','-preset','medium','-pix_fmt','yuv420p','-c:a','copy',out],stdin=subprocess.PIPE)
  for f in F: p.stdin.write(f.tobytes())
  p.stdin.close();p.wait()
