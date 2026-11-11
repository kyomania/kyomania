import sys
root=sys.argv[1]
s=open(f"{root}/tools/index.src.html").read()
for k,f in [("TOP","parts_top.svg"),("BOT","parts_bot.svg"),("WORD","parts_word.svg")]:
    s=s.replace("{{"+k+"}}",open(f"{root}/{f}").read())
open(f"{root}/fastsite-tiktok/index.html","w").write(s)
print("built")
