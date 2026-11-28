import cv2,numpy as np,sys,json
sys.path.insert(0,'.');from screenpatch import *
D=(38,38,40);G=(130,130,135);WH=(255,255,255)
def bx(k,T):
  if k=='s1': return [dict(box=(314,433,372,449),text=T['h'],f='b',size=10,color=D,w=130,rot=2.5),
            dict(box=(311,460,400,477),text=T['sub'],f='r',size=8.6,color=G,w=130,rot=2.5),
            dict(box=(308,489,346,503),text=T['pl'],f='m',size=8.6,color=(90,90,95),w=60,rot=2.5),
            dict(box=(305,506,361,523),text=T['pv'],f='s',size=9.2,color=D,rot=2.5),
            dict(box=(301,554,392,572),text=T['ship'],f='r',size=9,color=G,w=130,rot=3),
            dict(box=(303,621,339,634),text=T['i1'],f='r',size=7,color=G,align='c',rot=3),
            dict(box=(377,625,401,639),text=T['i2'],f='r',size=7.5,color=G,w=50,rot=3),
            dict(box=(352,727,438,751),text=T['btn'],f='s',size=9.5,color=WH,align='c',rot=3)]
  if k=='s2': return [dict(box=(318,772,366,783),text=T['h'],f='b',size=8.6,color=D,w=110),
            dict(box=(318,792,392,804),text=T['sub'],f='r',size=7.4,color=G,w=110),
            dict(box=(318,818,350,828),text=T['pl'],f='m',size=7.4,color=(90,90,95),w=60),
            dict(box=(318,833,364,844),text=T['pv'],f='s',size=8,color=D),
            dict(box=(318,870,396,882),text=T['ship'],f='r',size=7.6,color=G,w=110),
            dict(box=(327,924,355,934),text=T['i1'],f='r',size=6,color=G,align='c'),
            dict(box=(387,924,407,933),text=T['i2'],f='r',size=6.4,color=G,w=40),
            dict(box=(382,1010,437,1026),text=T['btn'],f='s',size=8,color=WH,align='c')]
  if k=='s3': return [dict(box=(128,557,180,569),text=T['h'],f='b',size=9.3,color=D,w=120),
            dict(box=(128,581,208,593),text=T['sub'],f='r',size=8,color=G,w=120),
            dict(box=(128,608,162,618),text=T['pl'],f='m',size=8,color=(90,90,95),w=60),
            dict(box=(128,624,177,635),text=T['pv'],f='s',size=8.6,color=D),
            dict(box=(129,665,211,676),text=T['ship'],f='r',size=8.2,color=G,w=120),
            dict(box=(141,723,175,732),text=T['i1'],f='r',size=6.5,color=G,align='c'),
            dict(box=(204,723,224,732),text=T['i2'],f='r',size=6.9,color=G,w=40),
            dict(box=(188,813,268,829),text=T['btn'],f='s',size=8.6,color=WH,align='c')]
SEG={'s1':(291,332,300),'s2':(332,407,348),'s3':(407,448,412)}
if __name__=='__main__':
  raw,T,out=sys.argv[1],json.loads(sys.argv[2]),sys.argv[3]
  cap=cv2.VideoCapture(raw);F=[]
  while True:
    ok,f=cap.read()
    if not ok:break
    F.append(f)
  Wd=sys.argv[4]
  for k,(a,b,ri) in SEG.items():
    W=list(np.load(f'{Wd}/W_{k}.npy'));ref=F[ri];P,M=render_patch(ref,bx(k,T))
    F[a:b]=apply(F[a:b],W,ref,P,M)
  h,w=F[0].shape[:2]
  p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}','-r','24','-i','-','-i',raw,'-map','0:v','-map','1:a','-c:v','libx264','-crf','12','-preset','medium','-pix_fmt','yuv420p','-c:a','copy',out],stdin=subprocess.PIPE)
  for f in F: p.stdin.write(f.tobytes())
  p.stdin.close();p.wait()
