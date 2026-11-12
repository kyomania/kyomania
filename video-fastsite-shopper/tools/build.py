import os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parts=os.path.join(root,'..','video-fastsite')
s=open(f"{root}/tools/index.src.html").read()
for k,f in [("TOP","parts_top.svg"),("BOT","parts_bot.svg")]:
    s=s.replace("{{"+k+"}}",open(f"{parts}/{f}").read())
open(f"{root}/film/index.html","w").write(s); print("built")
