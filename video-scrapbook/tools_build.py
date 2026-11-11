import re
css=open('styleframes.html').read().split('<style>')[1].split('</style>')[0]
css=css.replace("body { background: #000; }","html, body { width:1080px; height:1920px; overflow:hidden; background:#141414; }\n  #root { position:relative; width:1080px; height:1920px; overflow:hidden; background:var(--ink); font-family:'Archivo',sans-serif; color:var(--cream); }")
css=re.sub(r"\.frame \{[^}]*\}\n","",css); css=re.sub(r"\.frame\.on \{[^}]*\}\n","",css)
css=css.replace(".noise {","#noise {")
css+="""
  .clip { position:absolute; inset:0; width:1080px; height:1920px; overflow:hidden; }
  .scene { background: var(--ink); }
  .boil { translate: var(--bx, 0px) var(--by, 0px); rotate: var(--br, 0deg); }
"""
body=open('scrapbook-reel/body.tpl').read(); js=open('scrapbook-reel/anim.js.tpl').read()
html=f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <style>{css}</style>
  </head>
  <body>
{body}
    <script>
{js}
    </script>
  </body>
</html>
"""
open('scrapbook-reel/index.html','w').write(html); print('built')
