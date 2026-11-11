# Stil „Hyperpop Warp“

Gespeicherter Video-Stil aus dem fast.site-TikTok-Video (`video-fastsite/`).
Für schnelle, laute Produkt- und Werbevideos im Hochformat (TikTok, Reels, Shorts).

## So nutzt du den Stil für ein neues Video

Schreib in einem neuen Chat (Ordner `styles/hyperpop-warp/` muss im Projekt liegen):

> Starte Motion Fabrik. Mach ein [Länge]-Sekunden-Video im Format 9:16 über [Link/Thema].
> Nutze exakt den Stil aus `styles/hyperpop-warp/STYLE.md` und starte von
> `styles/hyperpop-warp/template/`. Logo und Inhalte von der Webseite. Deutsche Stimme,
> Musik und Soundeffekte wie dort beschrieben. Ziel erreicht, wenn es genauso spektakulär
> wirkt wie das fast.site-Video.

Die Farbpalette darf pro Marke getauscht werden (nur die Tokens in `template/index.html` → `:root`),
alles andere (Typo, Bewegung, Übergänge, Sound) bleibt gleich.

## Farben

| Token | Wert | Rolle |
|---|---|---|
| `--uv` | `#0b0220` | Grund, Ultraviolett-Schwarz; dunkle Schrift auf hellen Flächen |
| `--uv2` / `--violet` | `#1a0846` / `#6a2cff` | Glows, Verläufe, Tunnel-Ringe |
| `--acid` | `#c8ff1a` | Hauptakzent: Kern-Botschaft, CTA-Button, Zahlen |
| `--hot` | `#ff2d8a` | Problem/Spannung, Durchstreichen, Stempel |
| `--ice` | `#7cf6ff` | Kühler Kontrast, Nodes, Warp-Farbe |
| `--paper` | `#f6f2ff` | Helle Schrift |

Regeln: Jede Szene hat **eine** vollflächige Grundfarbe (abwechselnd dunkel UV → Acid → Hot → Ice →
dunkel). Auf hellen Flächen ist Schrift immer `--uv`. Logos behalten ihre Originalfarben.
Die Palette ist bewusst *nicht* an die Marke angelehnt.

## Typografie

- **Unbounded 900**, Versalien, Laufweite −0,04 em, Zeilenhöhe 0,92: Headlines, Slams, Zahlen (100–330 px)
- **Inter Tight 800/900**: Einleitungs-Zeilen („Deine Website ist“, „alles auf der“), 70–90 px
- **JetBrains Mono 800**, Versalien, Laufweite +0,12–0,22 em: Nummern („01 ——“), Labels, Taglines, HUD
- Pro Bild höchstens 2–3 Textebenen. Wichtigstes Wort riesig, Rest klein.

## Bewegung

- Tempo am Beat: Musik 150 bpm → Schnitte auf dem 0,4-s-Raster, Animationen auf dem gesprochenen Wort.
- Rein: `expo.out` / `back.out(2–3)` / `power4.out`, 0,25–0,5 s. Raus: `power4.in`, 0,3–0,4 s.
- Buchstaben einzeln (`split()` + Stagger 0,02–0,07 s).
- Impact-Momente = **Slam + Weißblitz + Shake** gleichzeitig (`rgbSlam`, `flash`, `shake`).
- Auf jeder Ebene bewegt sich etwas: driftende Farb-Blobs, flackerndes Grain, Speed-Lines, Partikel.
- Zahlen zählen hoch und schlagen dann ein (−35 %-Moment), mit Partikel-Explosion.
- „Langsam“ darf träge wirken (bounce, absackende Buchstaben), „schnell“ immer explosiv.

## Übergänge (Bausteine in `template/index.html`)

| Baustein | Wirkung | Wann |
|---|---|---|
| `implode(sel, t)` + `warp(t)` | Szene wird in die Mitte gesaugt, Lichtgeschwindigkeits-Streifen | Problem → Lösung |
| `chevWipe(t, c1, c2)` | Riesiger Doppel-Chevron fegt von unten nach oben | Großer Szenenwechsel |
| `whipIn` / `whipOut` | Seitlicher Wisch mit Skew und Blur | Feature-Reihen (01/02/03) |
| Zoom-through (`scale 2.6 + blur`) + `warp` | Durch die Szene hindurchfliegen | Kapitelwechsel |
| `clipPath` inset/circle | Harte Farbflächen-Reveals | Schnelle Text-Takes |
| 3D-Tunnel + Wörter, die auf die Kamera zufliegen | Aufzählungen (Plattformen, Features) | Listen |
| Marquee-Reihen schräg (−9°) + Beat-Flackern | Musik-Drop | Höhepunkt |

## Aufbau (Dramaturgie, ~25 s)

1. **Hook / Problem** (0–2,5 s), dunkel, träge, Zähler läuft hoch
2. **Lösung-Slam** (2,5–4 s), Acid-Fläche, riesiges Wort mit RGB-Split
3. **3 Features** (4–7,5 s), je ~1,2 s, Whip-Wechsel, nummeriert 01/02/03
4. **Beweis-Zahl** (7,5–11,5 s), echte Werte von der Webseite, Zahl zählt hoch + Explosion
5. **Einwände weg** (11,5–15 s), kurze Takes: „Kein X. Keine Y. Z bleibt.“
6. **Stack / Drop** (15–19,5 s), Tunnel, dann Drop mit Marquee
7. **Logo + CTA** (19,5–25 s), Logo fliegt ein, Blitz, Angebot, pulsierender Button

## Ton

- Stimme: ElevenLabs v4 über Higgsfield (`elevenlabs_v4`, Stimme „Callum“, stability 0.4), deutsch, ~22 s Text,
  kurze Sätze mit Pause. Startet bei 0,5 s.
- Musik: ElevenLabs Music v2.5, Prompt:
  „Instrumental high-energy hyperpop phonk for a TikTok tech ad, 150 bpm, punchy 808 kick and glitchy
  synth stabs, short riser intro, massive drop at 2 seconds, stutter break at 12 seconds, second drop,
  clean hard stop ending at 25 seconds“
- SFX: `tools/sfx.py` (Whoosh, großer Whoosh, Impact, weicher Impact, Riser, Glitch, Blip, Tick).
- Mix: `tools/mix.py`; Musik wird unter der Stimme abgesenkt, Cue-Liste mit den Szenenzeiten
  abgleichen, Ziel −14 LUFS.
  Aufruf: `python3 tools/mix.py <ordner-mit-dl-und-sfx> <ausgabe.wav>` (erwartet `dl/music.mp3`, `dl/vo.mp3`, `sfx/*.wav`).

## Technik

- HyperFrames 0.9.33, 1080×1920, 30 fps. GSAP und Schriften liegen lokal in `template/assets/`.
- Nur deterministischer Zufall (`rnd()`), kein `Math.random()`.
- Kein `shake()` auf Elemente, die gleichzeitig eigene x/y-Tweens haben (dann `yPercent` verwenden).
- Keine Animation von `letterSpacing` (ruckelt); stattdessen `scaleX`.
- Lange Wörter: `white-space: nowrap` und Größe prüfen, Inhalt zwischen x 70–1010 und y 180–1560 halten
  (TikTok-Bedienelemente).
- Vor dem Rendern: `npx hyperframes lint` und `npx hyperframes snapshot --at …` anschauen.
- Rendern: `npx hyperframes render -o video.mp4 -q delivery` (~5–6 min für 25 s).

Referenz-Umsetzung mit allen Szenen: `reference-fastsite.src.html` (Original in `video-fastsite/tools/`).
