import sys,os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src=os.path.join(root,'..','video-fastsite')
s=open(f"{root}/tools/index.src.html").read()
for k,f in [("TOP","parts_top.svg"),("BOT","parts_bot.svg")]:
    s=s.replace("{{"+k+"}}",open(f"{src}/{f}").read())
w=open(f"{root}/film/assets/wordmark.svg").read()
w=w[w.index("<svg"):].replace("<svg ",'<svg id="lg-word" ',1)
s=s.replace("{{WORD}}",w)
open(f"{root}/film/index.html","w").write(s)
print("built")
