# fuzzn Hidescreen v2 – Produktionsplan

**Status:** v1 (`fuzzn-hidescreen-60s.mp4`) ist abgelehnt. Gründe: zu wenig Motion, und die Bilder passen nicht zusammen (Figuren hell im Studiolicht in dunkle Szenen geklebt, falsche Größe und Perspektive, keine Schatten, doppeltes Geländer).
**Neue Regel des Kunden:** Alles wird selbst in Higgsfield erzeugt, und **fuzzn wird direkt IN jeder Szene generiert**. Kein Einkleben von Cutouts mehr.

## Eckdaten
- 16:9, 1920×1080, 60 s, nahtloser Loop, Twitch-Hidescreen (Weed ist erlaubt)
- **Kein „SEARCHING FOR A GAME“-Titel mehr im Bild.** Die Botschaft „sucht noch ein Spiel“ erzählt jetzt die Uhr: fuzzn schaut auf seine Uhr, Close-up zeigt „NOCH AM SUCHEN…“. Das kehrt als Running Gag wieder. Nur das kleine HUD „SCREEN HIDDEN · twitch.tv/fuzzn“ bleibt als Overlay.
- **Texte im Bild:** ausschließlich Deutsch und exakt vorgegeben (SPÄTI, FUZZN, HAKIKI DÖNER, HERTHA BSC, NOCH AM SUCHEN…). Sonst keine Wörter im Bild.
- **Charakter-Referenz:** `src/f0_base.webp` (Papier-Anime-fuzzn: schwarze Stachelhaare, silberne Visor-Brille auf der Stirn, schwarze Monogramm-Windjacke mit Kapuze, goldene Cuban-Kette mit FUZZN-Anhänger, schwarze Monogramm-Jogger, weiße Low-Top-Sneaker). Bei JEDEM Bild als Referenz hochladen.
- **Szenen-Referenzen** (Stil und Ort): `src/b1_kiez.webp`, `src/b2_hakiki.webp`, `src/b3_balkon.webp`, `src/b4_zimmer.webp`, `src/b5_dach.webp`
- **Bilder:** Nano Banana Pro (statt GPT Image 2.6 Sunburst, dessen Schrift teils unlesbar und nicht deutsch war), 16:9, 1K. fuzzn trägt in allen Shots eine schwarze Digitaluhr am linken Handgelenk.
- **Videos:** kling3_0, Modus pro, sound off, 5 s, 16:9, Startbild = Keyframe. Je Clip etwa 7,5 Credits.
- **Musik:** elevenlabs_music, etwa 62 s, Lo-Fi-Trap mit 85–90 BPM, ohne Gesang und loop-fähig (Anfang = Ende), dazu Papier-SFX.

## Stil-Suffix (an jeden Bild-Prompt anhängen)
`Handmade layered papercut diorama photographed, real cut and folded paper with visible texture and fibres, strong depth shadows, the character is part of the paper scene and lit by the scene's own light, cinematic, 16:9.`

## Keyframes (fuzzn IN der Szene)
| ID | Szene | Prompt-Kern |
|---|---|---|
| K1 | Kiez weit | Wide shot of the rainy Berlin street from b1 (Späti neon, elevated U-Bahn track, FUZZN graffiti). fuzzn walks along the wet sidewalk toward camera-right, small in frame, lit by street lamp and red Späti neon, reflection on wet street, paper rain. |
| K2 | Kiez nah | Medium tracking shot: fuzzn walking past the FUZZN graffiti wall, low camera angle, chain catching the street-lamp light, rain streaks, puddle splashes. |
| K3 | Kette Detail | Extreme close-up of the gold Cuban chain and FUZZN pendant on his black monogram jacket, wet with raindrops, neon reflections. |
| K4 | Hakiki weit | The Hakiki Döner shop from b2 at night; fuzzn stands at the counter in warm orange light, the doner man slices meat from the rotating spit and hands him a döner. |
| K5 | Döner-Biss | Close-up of fuzzn taking a huge happy bite of the döner in front of the glowing shop window, sauce dripping, steam, warm orange key light, blue night rim light. |
| K6 | Balkon | The Plattenbau balcony from b3 at night; fuzzn leans on THE SAME balcony railing seen from the side, lighting a joint, glowing ember, smoke curling over the Berlin night, purple sky. |
| K7 | Joint-Glut Detail | Extreme close-up of the glowing joint tip between his fingers, paper smoke curls, bokeh city lights. |
| K8 | Zimmer | The gaming room from b4 (Hertha poster, Oma photo, aluminium ladder with candles, neon cyan/magenta). fuzzn sits AT this desk in a black gaming chair, headset on, lit by monitor glow and neon rim light, seen from behind-side. |
| K9 | Oma-Foto Detail | Close-up of the framed photo of the sweet smiling grandma on the wall, candle light flickering on it, neon glow edge. |
| K10 | Dach | The rooftop from b5 with Fernsehturm and paper moon; fuzzn stands on the roof edge seen from behind, moonlight rim on his hair and jacket, wind. |
| K11 | Blick auf die Uhr | Under a street lamp in the rain, fuzzn raises his left arm and looks at his chunky black digital watch, impatient, eyebrow raised, cyan screen glow. |
| K12 | Uhr Close-up | Extreme close-up of the watch: cyan screen with exactly „NOCH AM / SUCHEN…“ plus loading spinner, raindrops, neon bokeh. |

## Kling-Clips (Startbild = Keyframe)
| Clip | Start | Bewegung |
|---|---|---|
| V1 | K1 | camera slowly tracks right with fuzzn walking, U-Bahn train rattles across the bridge, paper rain falls, puddle ripples |
| V2 | K2 | low tracking shot, fuzzn walks past camera, rain, neon flicker |
| V3 | K4 | doner man slices the spit and hands over the döner, spit rotates, steam rises, fuzzn grins |
| V4 | K5 | fuzzn bites, chews happily, sauce drips, camera pushes in |
| V5 | K6 | he takes a drag and exhales, smoke billows and drifts across the night city, camera slowly arcs |
| V6 | K8 | he plays intensely, hands fast on keyboard/mouse, monitor light flickers, candles flicker, camera slowly pushes in |
| V7 | K10 | camera cranes up and around him revealing the skyline and Fernsehturm, wind in his hair |
| V8 | K11 | he lifts his wrist, glances at the watch, sighs and rolls his eyes, rain keeps falling, slow push-in toward the watch |

## Schnitt (60 s, etwa 24 Shots, Cut alle 2–3 s)
- 0–10: V1 → K3 (Punch-in auf die Kette, Handkamera) → V8 (Blick auf die Uhr) → **K12 Uhr-Close-up „NOCH AM SUCHEN…“** (Spinner dreht als Overlay) → V2.
- 10–11: Übergang Papier zerreißt
- 11–23: V3 → V4 → K5-Freeze mit Zoom-Punch → V4-Rest. Kurzer Insert K12 (0,6 s), Spinner dreht weiter.
- 23–24: Übergang Zerknüllen
- 24–36: V5 → K7 (Glut-Detail mit Rauch-Overlay) → V5-Ende. Rauch formt Chat-Blasen („W“, „GG“, „Oma > alle“).
- 36–37: Übergang Umblättern
- 37–51: V6 → K9 (Oma-Zoom mit Herz) → V6. Kerzen-Flicker-Overlay.
- 51–52: Übergang Schere
- 52–60: V7, ab 57 s ein letzter K12-Insert mit „NOCH AM SUCHEN…“. Bei 59,2 s Riss zurück zu V1, Frame 0.
- Durchgehend: Handkamera-Micro-Shake, Whip-Pans zwischen Shots, Papierschnipsel-Partikel, Neon-Flicker. Kein Titel-Overlay, nur HUD unten links.

## Kosten
- 10 Keyframes: etwa 2,5 Credits
- 7 Clips: etwa 52 Credits
- Musik: etwa 5 Credits
- **Gesamt: etwa 60 Credits.** Plan wird am 17.11. erneuert, vorher ggf. Kontostand prüfen.

## Stand 13.11. – Keyframes erzeugt (Runde 2)
Alle 12 Keyframes liegen in `v2/keyframes/` (Übersicht: `v2/keyframes_kontaktbogen.jpg`). Erzeugt mit Nano Banana Pro, 1K (1376×768). Alle Schriften im Bild sind deutsch und lesbar: SPÄTI, FUZZN, HAKIKI DÖNER, NOCH AM SUCHEN…
Kleinigkeiten: Das Hertha-Poster in K08 schreibt „HERTHABSC“ ohne Leerzeichen. K04 hat zusätzlich „BESTER DÖNER IN KREUZBERG“ und „Kotbusser Str.“ (statt korrekt „Kottbusser“).

## Stand 13.11. – Maximal-Version (12 KI-Videos)
Auf Kundenwunsch wurde jeder Keyframe zu einem Kling-Clip (kling3_0 pro, 5 s, ohne Ton). C01–C12 liegen in `v2/clips/` (Job-IDs in `v2/jobs.md`). Damit gibt es keine reinen Standbild-Motion-Szenen mehr, nur der Döner-Freeze ist ein Standbild.
Musik: ElevenLabs Music v2.5, Lo-Fi-Trap 88 BPM, instrumental, per Crossfade auf exakt 60 s geloopt (`v2/music_loop.wav`). Dazu SFX: Swell auf den 5 Papier-Übergängen, Ticken und Ping bei der Uhr, Sub beim Freeze, Pings bei Chat-Blasen und Herz (`film/assets/audio/mix.wav`).

**Workflow**
1. `bash v2/build_base.sh` baut aus den Clips den 60-s-Grundschnitt `film/assets/video/base.mp4` (21 Segmente, Slow-Mo/Reverse wo nötig) und die Standbilder für die Übergänge.
2. `film/index.html` legt darüber Handkamera-Shake, Punch-Zooms an den Schnitten, Freeze-Flash, deutsche Chat-Blasen (W, GG, Ehrenmann, lass gehen, Oma > alle), Herz, Papierschnipsel, 5 Papier-Übergänge und das HUD. Kein Titel.
3. `npm run render` im Ordner `film/`.

**Schnitt (final, Stand Runde 5)**
| Zeit | Shot |
|---|---|
| 0,0–3,2 | C01 Kiez weit (ab 0,6 s im Clip, 0,0–0,6 laufen schon unter dem Loop-Riss) |
| 3,2–5,0 | C03 Kette |
| 5,0–8,6 | C02 Kiez nah |
| 8,6–12,2 | C11 Blick auf die Uhr |
| 12,2–14,5 | C12 Uhr „NOCH AM SUCHEN…“ → Riss |
| 14,5–16,5 | C05 er isst |
| 16,5–17,3 | Freeze-Punch beim Biss |
| 17,3–22,3 | C05 weiter, Slow-Mo |
| 22,3–23,5 | C03 Kette → Riss |
| 23,5–27,0 | C06 Balkon |
| 27,0–30,5 | C07 Glut (drinnen, kein Regen) |
| 30,5–35,0 | C06 Slow-Mo → Riss |
| 35,0–39,0 | C08 Zimmer mit Chat |
| 39,0–42,5 | C09 Oma + Herz |
| 42,5–47,0 | C08 Slow-Mo mit Chat → Riss |
| 47,0–52,0 | C10 Dach |
| 52,0–53,8 | C12 Uhr-Insert |
| 53,8–59,4 | C10 rückwärts, Slow-Mo |
| 59,4–60,0 | Loop-Riss, darunter C01 0,0–0,6 in Bewegung; Hälften sind genau bei 60,0 aus dem Bild |

## Stand 13.11. – Runde 3 (Kundenfeedback)
- **Gaming-Zimmer neu (K08c / C08):** Links Warzone-artiges Gameplay, fuzzn hält einen Controller, rechts ein leeres Twitch-Chat-Panel. Darüber hängt die LED-Schrift „FUZZN“ in warmem Orange-Weiß, das alte F-Logo ist entfernt. Der Kling-Clip hat eine feste Kamera, damit später echte Chat-Nachrichten auf den rechten Monitor gelegt werden können (Platzhalter im `#cam`-Container von `film/index.html`). Das Poster zeigt „HERTHA BSC“, das Leerzeichen ist aber eng.
- **Regen:** Die bunten Papierschnipsel sind raus. Stattdessen fallen in den Außenszenen (0–35 s) dezent ein Papier-Regenstreifen und ein Papier-Tropfen aus Higgsfield (`v2/sprites/`, freigestellt nach `film/assets/img/v2/streak.png` und `drop.png`).
- **Übergänge:** Alle 5 sind jetzt realistische Papier-Risse (`v2/tear.py`). Die Risskante ist zackig auf mehreren Ebenen, eine Hälfte zeigt das weiße, faserige Papierinnere, dazu feine Fasern und ein Schlagschatten. Erst reißt das Papier von einer Seite her auf, dann werden die Hälften mit leichter 3D-Wölbung weggezogen. Ton: echtes Reiß-Geräusch (Mirelo SFX, `film/assets/sfx/rip.wav`).
- **Chat:** Die erfundenen Chat-Blasen sind entfernt. Echte Nachrichten samt Benutzernamen liefert der Kunde.
- Mix: `cd film && python3 ../v2/mix.py`

## Stand 13.11. – Runde 4
- Döner-Reihenfolge korrigiert: erst bekommt er den Döner, dann Blick auf die Uhr, dann isst er.
- Kein Regen in der Glut-Szene (27,0–30,5 s), da er drinnen am Fenster steht.
- Chat auf dem rechten Monitor im Zimmer, Twitch-Stil, nacheinander eingeblendet: VanooO_ (36,0 s), AbuKaetzchen (37,0 s), satyrbe (38,1 s), dilard47 (43,2 s). Das Video und der Chat liegen im gemeinsamen Container `#plate`, damit sie sich bei Zooms zusammen bewegen.

## Stand 13.11. – Runde 5
- **Döner:** C04 (Überreichen) ist raus, weil er dort schon einen Döner in der Hand hält. Die Döner-Szene zeigt nur noch das Essen, der Kiez-Teil ist dafür bis 14,5 s verlängert.
- **Nahtloser Loop:** Der letzte Riss endet genau bei 60,0 s. Darunter läuft C01 schon in Bewegung an, und der Anfang setzt bei C01 0,6 s fort. Das Kamera-Wackeln kehrt am Ende auf null zurück, das Reiß-Geräusch wird über die Loop-Grenze an den Anfang gefaltet (`v2/mix.py`).
- **Chat schräg:** Die Chat-Ebene liegt per `matrix3d` (Homographie aus den vier gemessenen Ecken der Monitorfläche) exakt auf dem geneigten Bildschirm.

## Runde 6
- Chat stärker geneigt (Homographie mit tieferer rechter Seite).
- HUD unten links: „LOOKING FOR MATCH · twitch.tv/fuzzn“ statt „SCREEN HIDDEN“.
- HUD ergänzt: Instagram-Logo + @dfuzzn neben twitch.tv/fuzzn.
