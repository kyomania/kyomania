# FUZZN – „SEARCHING FOR A GAME“ Screenhide

Ein Anime-Screenhide als nahtloser 60-Sekunden-Loop für OBS. Version 2: auf deine Bilder abgestimmt.

## Die Leitidee: Die Suche, die nie endet

Die Figur auf deinen Bildern trägt den Akatsuki-Mantel, das ist Itachis Look. Das passt gut zu Sasuke:
**Sasukes ganze Geschichte ist die Suche nach Itachi.** Der Screenhide erzählt diese Suche aus Sasukes
Blick. Itachi taucht auf (auf der Schaukel, auf dem Dach), und jedes Mal, wenn man ihn fast hat,
zerfällt er in Krähen und ist wieder weg. Genau wie das Match, das nicht gefunden wird.
Rotes Pinsel-Banner, Sharingan-Rot und Chidori-Blau sind Sasukes Farben.

**Look:** deine Anime-Film-Hintergründe, darüber Manga-Elemente (Tusche, Speedlines, Papier).
**Farben:** Dämmerung Orange/Violett · Mondnacht Blau · Sharingan-Rot · Chidori-Blau · Tusche-Schwarz.
**Schrift:** kantige Brush-Schrift für „SEARCHING FOR A GAME“, klein darunter 探索中 (*„wird gesucht“*).

---

## Deine Bilder und wofür ich sie nutze

| # | Datei (`assets/bilder/`) | Rolle im Video |
|---|---|---|
| 01 | `01-schaukel-mit-figur` | Itachi wartet auf der Schaukel |
| 02 | `02-schaukel-leer` | **Loop-Anfang und -Ende.** Gleiche Kamera wie 01, perfekt zum Ein- und Ausblenden |
| 03 | `03-dach-mit-figur` | Mondnacht, Regen, Krähen |
| 04 | `04-dach-leer` | Gleiche Kamera wie 03: Er zerfällt in Krähen, das Dach bleibt leer |
| 05 | `05-portrait-blitz` | Höhepunkt: Sharingan-Blick, Blitze |
| 06 | `06-blitz-himmel` | Hintergrund für den Chidori-Text |
| 07 | `07-baum-augen-zu` | ruhiger Moment: Er schläft, Augen zu, Blätter fallen. Später Sharingan-Aufblitzen per Code |
| 08 | `08-papier-riss` | Papierstreifen, wird zum Banner „SEARCHING FOR A GAME“ |
| 09 | `09-tusche-pinsel` | Tusche-Elemente: Splatter, Enso-Kreis, Pinselstriche für Übergänge und Text-Reveals |
| 10 | `10-speedlines` | Manga-Impact bei Schnitten |
| 11 | roter Pinselstrich | dauerhaftes Text-Banner unten. *Liegt noch nicht im Projekt, bitte als Datei ablegen (oder ich baue ihn nach).* |

Die Paare **01/02** und **03/04** sind ideal. Die Figur kann erscheinen und verschwinden, ohne
dass der Hintergrund springt.

---

## Skript: 60-Sekunden-Loop, 16:9, 1920×1080, 30 fps

Dauerhaft im Bild: Unten liegt der **rote Pinselstrich (11)** als Banner mit
`SEARCHING FOR A GAME` und einem kleinen Sharingan als Lade-Spinner. Die drei Punkte sind drei Tomoe.
Groß inszeniert erscheint der Text zusätzlich **4×** (#1–#4).

| Zeit | Szene | Bild & Bewegung | Text | Ton |
|---|---|---|---|---|
| **0–6 s** | **1. Leere Schaukel** (02) | Parallax-Ebenen (Himmel, Stadt, Baum, Gras vorn), langsamer Push-in, Blätter treiben, die Schaukel pendelt leicht. | Banner wischt mit Pinsel-Swoosh ein. | Wind, Grillen, Kettenquietschen, Musik startet |
| **6–14 s** | **2. Er wartet** (01) | Ein paar Krähenfedern wirbeln vorbei, dann ist er da (weiche Überblendung 02→01 hinter einer Federwolke). Leichtes Atmen, Mantel und Haare im Wind. | **#1:** „SEARCHING FOR A GAME“ malt sich als Tusche-Strich (09) über den Himmel. | Federrascheln, Pinsel-Swoosh |
| **14–17 s** | **Übergang** | Tusche-Splatter (09) spritzt ins Bild und füllt es schwarz. | – | Tusche-„Splat“ |
| **17–27 s** | **3. Mondnacht** (03→04) | Regen-Partikel, Mond glimmt, Krähen kreisen (Bild + zusätzliche Code-Krähen). Push-in auf seinen Rücken. Bei ~23 s **zerfällt er in Krähen**, die auf die Kamera zufliegen, und das Dach (04) ist leer. | **#2:** Hinter den Krähen stehen in Rot „STILL SEARCHING…“ | Regen, Donner, Krähenschrei, Flügelschwarm |
| **27–36 s** | **4. Zerrissene Bilder** | Die Bilder 01, 03, 05 und 07 hängen als Papierabzüge an einer dunklen Wand, je mit einem Kunai. Im Takt **reißt eins nach dem anderen mittig durch**, Fetzen fallen, Kamera-Shake, kurz Speedlines (10). Hinter dem letzten Riss liegt der Papierstreifen (08). | **#3:** Auf dem Streifen (08) steht in schwarzer Tusche **SEARCHING FOR A GAME**. | 4× Papierreißen auf den Beat, Kunai-„Thunk“ |
| **36–40 s** | **5. Ruhe** (07) | Er schläft am Baum, Sonnenstrahlen flackern, Blätter fallen. Langsamer Zoom auf das Gesicht … | – | Musik nimmt sich zurück, Vogel, Blätter |
| **40–44 s** | **Augen auf** | … Harter Schnitt + Speedlines (10): Die Augen öffnen sich, **rotes Sharingan-Aufblitzen** (Code-Overlay auf 07 bzw. Schnitt auf 05). | – | Bass-Hit, „Shing“ |
| **44–53 s** | **6. Chidori** (05→06) | Das Portrait (05) mit flackernden Blitzen, die Kamera zittert. Dann bleibt nur der Blitzhimmel (06): Ein **Chidori-Blitz schreibt die Buchstaben** ein, Weißblitz, blaues Nachglühen. | **#4:** Großer blauer Blitz-Text **SEARCHING FOR A GAME**. | Chidori-Zirpen, Donner, Impact |
| **53–60 s** | **7. Zurück zur Schaukel** (02) | Enso-Kreis (09) als Blende zurück in die Dämmerung. Die Schaukel ist **leer und schwingt noch nach**. Ein Blatt landet auf dem Brett. Kamera fährt exakt auf Frame 0 zurück. | klein: „he's still out there…“ | Kettenquietschen, Musik schließt die Schleife |

**Loop-Naht:** Der letzte Frame ist identisch mit dem ersten (02, gleicher Ausschnitt). Das Pendeln klingt bis
dahin aus, Partikel und Musik laufen in Schleifenlänge. Das Video läuft stundenlang ohne sichtbaren Sprung.

**Gag-Zeilen** (wechseln klein über dem Banner):
„Noch nicht mal Kakashi kommt so spät.“ · „Queue-Jutsu wird gewirkt …“ ·
„Sasuke hat Itachi schneller gefunden.“ · „Matchmaking im Tsukuyomi: gefühlt 72 Stunden.“

---

## Was noch fehlt (optional, macht es besser)

| Was | Warum | Weg |
|---|---|---|
| **Höhere Auflösung** | Deine Bilder haben 1344×752 Pixel, das Video 1920×1080. Ohne Upscale wirken sie leicht weich. | Upscale über Higgsfield (kostet Credits) oder die Originale in voller Größe aus Higgsfield ablegen |
| **Kurze Clips aus 01 und 03** (je 5 s) | Echte Bewegung in Mantel und Haaren statt nur Parallax | Image-to-Video über Higgsfield (Kling / Seedance) |
| **Roter Pinselstrich** als Datei | Banner unten | Datei in `assets/bilder/` legen, oder ich baue ihn im Code nach |
| **FUZZN-Logo** (PNG/SVG, transparent) | Logo-Slot im Banner | von dir |
| **Musik** (60 s, loopbar) | Lofi + Shakuhachi, melancholisch. **Kein Naruto-Soundtrack** (Twitch-Mute / DMCA) | über Higgsfield generieren |
| **Soundeffekte** | Papier, Kunai, Krähen, Regen, Chidori, Kette, Tusche | über Higgsfield generieren |

Code-Effekte, die ich selbst baue: Parallax, Regen, Blätter, Federn, Krähenschwarm, Papierrisse, Kamera-Shake,
Blitz-Schrift, Sharingan-Spinner und Augen-Aufblitzen, Pinsel-Reveals.

---

## Bonus: als „lebendige“ OBS-Browserquelle

Weil das Video aus HTML entsteht, kann es auch **live in OBS als Browserquelle** laufen:
mit **echtem Queue-Timer** („Searching… 04:12“), Gag-Zeilen in zufälliger Reihenfolge und ohne Loop-Sprung.
Das MP4 bleibt als Backup.

## Rahmen

- 16:9, 1920×1080, 30 fps, nahtloser 60-s-Loop
- MP4 (H.264) für die OBS-Medienquelle mit „Wiederholen“, optional die HTML-Browserquelle
- Fan-Art auf dem eigenen Stream ist üblich. Keine Original-Musik, keine 1:1-Szenen aus dem Anime.
