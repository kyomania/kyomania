---
name: html5-boilerplate
description: Start a new website/web page from HTML5 Boilerplate 9.0.1 (index.html, 404, css, js, favicon, manifest, robots.txt). Use when the user wants a new site, landing page, "boilerplate", "h5bp", or a clean HTML starter.
---
# HTML5 Boilerplate 9.0.1

Template: `~/.claude/skills/html5-boilerplate/template/`

New project: `cp -r ~/.claude/skills/html5-boilerplate/template/. <target-dir>/`
Then edit `index.html` (title, description, lang), `site.webmanifest` (name), and replace icons.
Plain static use needs no build: drop the `webpack.*.js` files and `package.json` unless the user wants webpack.
Pairs with the animate-css skill for animations.
