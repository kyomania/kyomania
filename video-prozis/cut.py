import cv2, numpy as np, sys, json
jobs = {
 "pack_almonds": ("src/2.jpg", (228,170,378,600)),
 "pack_puffies": ("src/3.jpg", (188,168,382,600)),
 "pack_nibs":    ("src/4.jpg", (182,170,378,580)),
 "pack_agave":   ("src/5.jpg", (286,160,232,620)),
 "bowl":         ("src/1.webp", (0,285,688,470)),
}
for name,(f,(x,y,w,h)) in jobs.items():
    im = cv2.imread(f)
    mask = np.zeros(im.shape[:2], np.uint8)
    bg = np.zeros((1,65),np.float64); fg = np.zeros((1,65),np.float64)
    cv2.grabCut(im, mask, (x,y,w,h), bg, fg, 8, cv2.GC_INIT_WITH_RECT)
    m = np.where((mask==1)|(mask==3),255,0).astype(np.uint8)
    # keep largest component, fill holes
    n,lab,st,_ = cv2.connectedComponentsWithStats(m)
    if n>1:
        k = 1+np.argmax(st[1:,cv2.CC_STAT_AREA]); m = np.where(lab==k,255,0).astype(np.uint8)
    cnts,_ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    m = np.zeros_like(m); cv2.drawContours(m, cnts, -1, 255, -1)
    m = cv2.GaussianBlur(m,(5,5),0)
    rgba = cv2.cvtColor(im, cv2.COLOR_BGR2BGRA); rgba[:,:,3]=m
    ys,xs = np.where(m>10); rgba = rgba[ys.min():ys.max()+1, xs.min():xs.max()+1]
    cv2.imwrite(f"cut/{name}.png", rgba); print(name, rgba.shape)
