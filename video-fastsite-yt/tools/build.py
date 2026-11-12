"""Inline fast.site logo parts into the composition: tools/index.src.html -> spot/index.html"""
import re, sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logo = open(os.path.join(root, "..", "video-fastsite", "site", "logo.svg")).read()
fills = dict(re.findall(r"\.(cls-\d)\s*\{\s*fill:\s*([^;]+);", logo))
paths = re.findall(r"<path class=\"(cls-\d)\" d=\"([^\"]+)\"\s*/>", logo)
icon = "".join(f'<path fill="{fills[c]}" d="{d}"/>' for c, d in paths if c != "cls-3")
word = "".join(f'<path d="{d}"/>' for c, d in paths if c == "cls-3")
s = open(os.path.join(root, "tools", "index.src.html")).read()
s = (s.replace("{{ICONSPLIT}}", icon).replace("{{ICON}}", icon).replace("{{WORD}}", word)
     .replace("{{JPGKB}}", "303,4").replace("{{WEBPKB}}", "198,2").replace("{{PCT}}", "35").replace("{{RATIO}}", "0.653"))
open(os.path.join(root, "spot", "index.html"), "w").write(s)
print("built", len(s))
