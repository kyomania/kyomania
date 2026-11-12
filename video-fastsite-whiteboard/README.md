# fast.site – Whiteboard-Erklärvideo (38,5 s, 16:9, deutsche Stimme)

Fertig: `fastsite-whiteboard.mp4`. Basis ist das Track-Whiteboard (`video-tracksite-whiteboard/`),
Inhalte von fast.site/de, Logo als Original-SVG (`board/assets/img/fastsite-logo.svg`, `-icon.svg`).

Stimme: Higgsfield, text2speech_v2 / ElevenLabs, Preset „Julian“ (7 Sätze in `dl/vo1–7.mp3`):
1. Mach deine Website schneller. Und behalte dein Hosting.
2. Fast Site legt sich vor deine bestehende Website. Domain verbinden, DNS und SSL einrichten, fertig.
3. Edge-Caching liefert Seiten und Dateien direkt aus, ohne jede Antwort am Server neu zu erzeugen.
4. Deine Bilder werden automatisch zu Web P. Kein Code, keine Plugins.
5. Dazu D-Doss-Schutz. Und dein Hosting bleibt, wie es ist.
6. Für WordPress, WooCommerce, Shopware, Next J S und viele mehr.
7. Teste Fast Site sieben Tage kostenlos. Keine Kreditkarte erforderlich.

Timing: Der Board-Ablauf ist auf 20 s gebaut und wird per Zeit-Warp (`KN` in `board/index.html`
und `tools/sound.py`) auf die Stimme gelegt. Einen Satz neu einsprechen: mp3 ersetzen, Startzeit in
`tools/sound.py` anpassen, `uv run --with numpy --with scipy python tools/sound.py board/assets/audio/mix.wav`.

Rendern: `node tools/capture.cjs board frames 0 1155` (in 4 Teilen parallel), dann
`ffmpeg -framerate 30 -i frames/f%04d.jpg -i board/assets/audio/mix.wav -c:v libx264 -crf 16 -pix_fmt yuv420p -c:a aac -shortest fastsite-whiteboard.mp4`
