import numpy as np
from PIL import Image, ImageFilter
im=np.asarray(Image.open("src.png").convert("RGB")).astype(float)
H,W,_=im.shape
r,g,b=im[...,0],im[...,1],im[...,2]
# background reference: blue sampled from mid-left
ref=im[500:600,5:40].reshape(-1,3).mean(0)
d=np.sqrt(((im-ref)**2).sum(-1))
# also blue-ish dominance
blu=(b-r)
lum=im.mean(-1)
bg=(d<48)&(lum>55)
m=(~bg).astype(np.uint8)*255
m[:400]=0            # text region -> away
m[1068:]=0           # ledge -> away
mi=Image.fromarray(m).filter(ImageFilter.MedianFilter(7))
# keep largest component
import scipy.ndimage as nd
a=np.asarray(mi)>127
lab,n=nd.label(a); sz=nd.sum(a,lab,range(1,n+1)); a=lab==(1+int(np.argmax(sz)))
a=nd.binary_closing(a,structure=np.ones((3,3)),iterations=12,border_value=0)|a
a=nd.binary_fill_holes(a)
a=nd.binary_opening(a,iterations=2)
alpha=Image.fromarray((a*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))
rgba=Image.open("src.png").convert("RGBA"); rgba.putalpha(alpha)
bb=alpha.getbbox(); print("bbox",bb,"ref",ref)
rgba.save("chill-reel/assets/img/dog.png")
# clean plate background + ledge for reference
Image.open("src.png").crop((0,1060,W,H)).save("chill-reel/assets/img/ledge.png")
prev=Image.new("RGBA",(W,H),(255,0,255,255)); prev.alpha_composite(rgba); prev.convert("RGB").resize((384,688)).save("/tmp/claude-0/-home-user-kyomania/3d21545c-dfb0-5e3d-bb64-e2cedfadb77e/scratchpad/cut.png")
