# Track (track.site) – Kinofilm, 30 s, 16:9

Fertiges Video: `track-kinofilm-30s.mp4` (1920×1080, 30 fps, Cinemascope-Balken 2.39:1, Stereo-Score).

## Aufbau

| Zeit | Szene | Text |
|---|---|---|
| 0 – 5,2 s | Website zeichnet sich, Klick auf „Jetzt kaufen“, ein Event wird geboren | Ein Snippet. |
| 5,2 – 10,2 s | Browser- und Server-Event kreisen umeinander und verschmelzen | Jede Conversion genau einmal gezählt. |
| 10,2 – 15,4 s | Flug durch den Tunnel, Consent-Tor, rote Events prallen ab | Nur, was Consent erlaubt, verlässt deine Seite. |
| 15,4 – 21 s | Auffächern zu Meta, Google, TikTok … Kamera zieht weit auf | Jede Plattform. |
| 21 – 24,6 s | Tracking Health Score 70 → 100 | Du weißt immer, was als Nächstes zu tun ist. |
| 24,6 – 30 s | Stille, Schlag, drei Lichtpunkte formen das Logo | Track · Ein Snippet. Jede Plattform. Jede Conversion genau einmal gezählt. · track.site |

Alle Aussagen stammen von track.site/de. Das Logo ist am Ende das Original-SVG (#1f4fe0), nicht nachgebaut.

## Bearbeiten

- **Texte, Ebenen, Keyframes:** `film/index.html`. Texte stehen im HTML, das Timing im GSAP-Block unten
  (`up(...)`, `flash(...)`). Die 3D-Welt (three.js) hängt an derselben Timeline. Schnittzeiten stehen in `CUT`.
- **Ton:** `tools/score.py` erzeugt Score und SFX im Code (gleiche Schnittzeiten).
  `uv run --with numpy --with scipy python tools/score.py film/assets/audio/mix.wav`
- **Vorschau:** `cd film && npx hyperframes@0.9.33 preview`

## Rendern

`npx hyperframes render` funktioniert, ist hier ohne GPU aber langsam (WebGL in Software, ca. 90 min).
Schneller ist die Bildaufnahme mit Playwright (ca. 10 min), danach Zusammenfügen mit ffmpeg:

```bash
for r in "0 300" "300 600" "600 900"; do set -- $r; node tools/capture.cjs film frames $1 $2 & done; wait
ffmpeg -framerate 30 -i frames/f%04d.jpg -i film/assets/audio/mix.wav -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -c:a aac -b:a 256k -shortest track-kinofilm-30s.mp4
```
