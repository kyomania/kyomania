---
name: animate-css
description: Add ready-made CSS animations (fadeIn, bounce, slideInUp, zoomIn, ...) with animate.css 4.1.1 to HTML pages. Use when the user wants animations in a page, "animate.css", entrance/exit effects.
---
# animate.css 4.1.1

Local copy: `~/.claude/skills/animate-css/animate.min.css` (copy it next to the page, or use CDN
`https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css`).
All animation names: `names.txt`.

Usage:
```html
<h1 class="animate__animated animate__fadeInUp animate__delay-1s">Hi</h1>
```
- Modifiers: `animate__delay-1s..5s`, `animate__slow|slower|fast|faster`, `animate__repeat-1..3`, `animate__infinite`.
- Tune per element: `style="--animate-duration:.6s; --animate-delay:.2s"`.
- Trigger via JS: add classes, remove them on `animationend`.
- Respects `prefers-reduced-motion` automatically.
