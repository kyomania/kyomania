# FUZZN – „SEARCHING FOR A GAME“ Screenhide

Ein Anime-Screenhide mit Sasuke, als nahtloser Loop für OBS.

## Die Leitidee: Sasuke sucht. Immer.

Sasukes ganze Geschichte dreht sich ums Suchen: nach Itachi, nach Stärke und am Ende
nach dem Weg nach Hause. Genau das passiert auch in der Queue. Daraus ergibt sich der rote Faden:
**Warten, Suchen, Loslassen (zerreißen) und wieder von vorn.** Deshalb funktioniert das Video als Loop:
Es beginnt und endet bei der leeren Schaukel.

**Look:** handgemalte Anime-Film-Hintergründe (wie dein Schaukelbild), darüber
Manga-Elemente: Tusche-Pinselstriche, Speedlines, Papiertextur, Screentone-Raster.
**Farben:** Dämmerungs-Orange/Violett als Basis, dazu Sharingan-Rot (#C8102E), Chidori-Blau (#5AC8FF)
und Tusche-Schwarz. **Schrift:** „SEARCHING FOR A GAME“ in einer kantigen Brush-Schrift
(z. B. „Gang of Three“ oder eine freie Font wie „Rock Salt“ bzw. „Permanent Marker“), dazu klein
探索中 (*tansaku-chū* = „wird gesucht“) als japanischer Untertitel.

---

## Motion-Ideen (der Werkzeugkasten)

| Idee | Was passiert | Wofür |
|---|---|---|
| **Sharingan als Ladekreis** | Die drei Tomoe drehen sich wie ein Lade-Spinner, mal schneller, mal langsamer. | dauerhaftes „Suchen“-Symbol, Loop-Anker |
| **Zerrissene Bilder** | Momente auf Papier, mit Kunai an eine Holzwand gepinnt. Im Takt reißt jedes Bild mittig durch (gezackte Kante, Fasern, Schatten). Hinter dem Riss kommt das nächste Bild zum Vorschein. | Sasuke lässt seine Vergangenheit hinter sich, und es sorgt für Tempo |
| **Schaukel-Pendel** | Sasuke wartet auf der Schaukel, die ganz leicht pendelt. Am Ende ist sie leer und schwingt noch nach. | emotionaler Kern und Loop-Punkt |
| **Rauchwolken-Teleport** | Sasuke erscheint bzw. verschwindet in einer Ninja-Rauchwolke („poof“). | Auf- und Abtritte ohne harte Schnitte |
| **Krähen-Wipe** | Ein Krähenschwarm fliegt durchs Bild und wischt die Szene weg (Itachi-Hommage). | Übergang |
| **Chidori schreibt den Text** | Ein blauer Blitz kriecht über den Bildschirm und „brennt“ SEARCHING FOR A GAME ein. Kurzes Weißblitzen, dann Nachglühen. | Hauptmoment für den Text |
| **Manga-Panel-Split** | Das Bild zerfällt in 3 schräge Panels mit Speedlines (Auge, Hand am Schwert, Schaukel). | Rhythmus, Comic-Feeling |
| **Mangekyō-Zoom** | Kamerafahrt ins Auge, das Muster dreht sich und wird zum Tunnel in die nächste Szene. | Übergang |
| **Konoha-Blätter & Glut** | Blätter und Funken treiben in Parallax-Ebenen durchs ganze Video. | sorgt dafür, dass sich immer etwas bewegt |
| **Animierte Punkte** | Hinter „SEARCHING FOR A GAME“ laufen Punkte als kleine Tomoe statt als normale Punkte. | Detail, das man zweimal ansieht |
| **Gag-Zeilen** | Kleine Untertitel wechseln sich ab: „Sasuke wartet länger als auf Itachis Erklärung.“ · „Noch nicht mal Kakashi kommt so spät.“ · „Queue-Jutsu läuft …“ | Humor, Chat schreibt drüber |

**Dauerhafte Ebene über dem ganzen Loop:** Unten liegt ein schmaler Balken mit Tusche-Kante:
`SEARCHING FOR A GAME ⟳` (Sharingan-Spinner), daneben ein FUZZN-Logo-Slot.
So steht der Text in **jeder Sekunde** im Bild. Groß inszeniert taucht er zusätzlich
**4× pro Loop** auf (siehe Skript).

---

## Skript: 60-Sekunden-Loop, 16:9, 1920×1080, 30 fps

| Zeit | Szene | Bild & Bewegung | Text-Moment | Ton |
|---|---|---|---|---|
| **0–7 s** | **1. Die leere Schaukel** | Dein Schaukelbild in Parallax-Ebenen (Himmel, Stadt, Baum, Gerüst). Langsamer Push-in, Blätter treiben, die Schaukel pendelt minimal. | Der dauerhafte Balken fährt mit Pinselstrich ein. | Wind, Grillen, leises Quietschen der Schaukelkette, Musik setzt ein (Lofi + Shakuhachi) |
| **7–15 s** | **2. Sasuke erscheint** | Rauchwolke, darin sitzt Sasuke auf der Schaukel und blickt nach unten. Image-to-Video-Clip: Haare und Umhang bewegen sich leicht im Wind, er schaukelt kaum. | **#1:** „SEARCHING FOR A GAME“ schreibt sich groß als Tusche-Pinselstrich über den Himmel, darunter 探索中. | „Poof“-Rauch, Tusche-Pinsel-Swoosh |
| **15–21 s** | **3. Das Auge** | Harter Schnitt auf ein Augen-Close-up. Das Auge öffnet sich, das Sharingan aktiviert sich, die Tomoe drehen sich als Spinner. Langsamer Zoom hinein. | **#2:** In der Iris spiegelt sich in Rot „SEARCHING…“. | tiefer Bass-Hit, Sharingan-„Shing“ |
| **21–33 s** | **4. Zerrissene Bilder** | Der Mangekyō-Tunnel führt an eine Holzwand. 4 Papierbilder hängen dort mit Kunai: Team-7-Foto · Kind-Sasuke mit Bruder (Rückenansicht) · Sasuke im Regen · Schwert-Silhouette. Im Beat reißt eins nach dem anderen durch, Fetzen fallen, Kamera-Shake. | **#3:** Hinter dem letzten Riss steht schwarz auf rot, wie auf zerrissenem Papier: **SEARCHING FOR A GAME** | 4× Papierreißen auf den Beat, Kunai-„Thunk“ |
| **33–42 s** | **5. Regen-Dach** | Sasuke steht nachts im Regen auf einem Dach, Rückenansicht, und blickt über die Stadt. Regen-Partikel, Blitz in der Ferne. Krähenschwarm kommt von rechts und wischt das Bild weg. | Gag-Zeile wechselt. | Regen, Donner, Krähenrufe, Flügelschlag |
| **42–52 s** | **6. Chidori** | Manga-Panel-Split in 3 Panels (Hand mit Chidori · Auge · Schaukel), Speedlines. Blauer Blitz läuft über alle Panels. | **#4:** Chidori brennt **SEARCHING FOR A GAME** ein, Weißblitz, blaues Nachglühen. | Chidori-Zirpen (Vogelgezwitscher + Elektro), Impact |
| **52–60 s** | **7. Zurück an der Schaukel** | Zurück in der Dämmerung. Die Schaukel ist **leer, schwingt aber noch nach** (er ist gerade weg). Ein Blatt fällt auf das Sitzbrett. Ruhiger Pull-out bis exakt zum ersten Frame. | Klein: „still searching…“ | Musik läuft zur Schleife, Kettenquietschen |

**Loop-Naht:** Frame 1800 ist identisch mit Frame 0 (leere Schaukel, gleicher Bildausschnitt). Das Nachschwingen
klingt bis dahin aus, Partikel und Musik laufen in Schleifenlänge. Den Loop kann man stundenlang laufen lassen,
ohne dass ein Sprung auffällt.

---

## Welche Grafiken ich brauche

Status: ✅ vorhanden · 🆕 neu generieren (Higgsfield) · 💻 baue ich im Code

Damit alles wie aus einem Film aussieht, sollte **jedes neue Bild das Schaukelbild bzw. den Itachi-Look
als Stil-Referenz** bekommen. Sasuke-Bilder am besten **mit derselben Charakter-Referenz**, sonst sieht er
in jeder Szene anders aus.

| # | Grafik | Status | Notiz / Prompt-Kern |
|---|---|---|---|
| 1 | Leere Schaukel bei Dämmerung (16:9) | ✅ | `assets/higgsfield/schaukel-leer.png` |
| 2 | **Gleiche Schaukel, Sasuke sitzt drauf** | 🆕 | Als *Bild-Edit* von #1 (Nano Banana 2), damit Kamera und Licht exakt gleich bleiben: „same image, a lonely teen ninja with spiky black hair, dark blue high-collar shirt, sits on the swing, head down, hands on chains“ |
| 3 | Video-Clip aus #2: Sasuke wartet (5 s, loopbar) | 🆕 | Image-to-Video (Kling / Seedance): „hair and clothes move gently in the evening wind, swing sways slightly, he barely moves, static camera“ |
| 4 | Video-Clip aus #1: leere Schaukel schwingt aus | 🆕 | „empty swing swaying and slowly coming to rest, leaves drifting, static camera“ |
| 5 | Augen-Close-up, normal (dunkles Auge) | 🆕 | extreme close-up, 16:9, Anime-Film-Stil wie Referenz |
| 6 | Augen-Close-up, Sharingan aktiv | 🆕 | gleiches Bild als Edit von #5, Iris rot mit 3 Tomoe. Die Tomoe animiere ich zusätzlich als Vektor 💻 |
| 7 | Holzwand / Ninja-Trainingsraum | 🆕 | Hintergrund für die Papierbilder, warmes Seitenlicht, viel freie Fläche |
| 8–11 | **4 Bilder zum Zerreißen** | 🆕 | jedes als eigenes Bild, Stil „old printed photo / sketch on paper“: Team-Foto (3 Kinder + Lehrer, Sasuke schaut weg) · zwei Brüder von hinten im Sonnenuntergang · Sasuke im Regen · Schwert-Silhouette vor Mond |
| 12 | Regen-Dach-Szene, Rückenansicht | 🆕 | Nacht, Regen, Stadt mit Lichtern, Umhang. Optional als Video-Clip (Umhang weht) |
| 13 | Hand mit Chidori | 🆕 | Close-up, blau leuchtende Blitze, dunkler Hintergrund (für Panel 1) |
| 14 | Krähe(n) freigestellt | 🆕 | 2–3 Krähen-Posen, danach `remove_background`. Der Schwarm entsteht im Code aus den Einzelkrähen 💻 |
| 15 | Kunai freigestellt | 🆕 | ein Kunai, schräg, auf weißem Grund → freistellen |
| 16 | Papier-Riss-Kanten, Fasern, Tusche-Texturen | 💻 | baue ich prozedural (gezackte Masken, Faser-Rauschen) |
| 17 | Rauchwolke, Blätter, Funken, Regen, Speedlines, Chidori-Blitz, Mangekyō-Tunnel | 💻 | alles im Code animiert |
| 18 | **FUZZN-Logo** | ❓ von dir | als PNG/SVG mit transparentem Hintergrund |
| 19 | Musik (60 s, loopbar) | 🆕 | Lofi-Hip-Hop mit Shakuhachi/Koto, melancholisch. **Kein Naruto-Original-Soundtrack!** Der wird auf Twitch gemutet oder kann einen DMCA-Strike auslösen. |
| 20 | Soundeffekte | 🆕 | Papierreißen, Kunai-Thunk, Poof-Rauch, Kettenquietschen, Krähen, Regen/Donner, Chidori-Zirpen, Sharingan-„Shing“ |

> **Wenn du die Bilder schon hast:** Leg sie einfach in `video-fuzzn-searching/assets/` oder sag mir,
> welche in Higgsfield liegen. In deinem Verlauf habe ich bisher nur die leere Schaukel gefunden.

---

## Bonus-Idee: als „lebendige“ OBS-Browserquelle

Das Video wird aus HTML gebaut. Ich kann deshalb zusätzlich eine Version liefern, die **live in OBS als
Browserquelle** läuft statt als MP4:

- **echter Queue-Timer**, der hochzählt („Searching… 04:12“)
- Gag-Zeilen in zufälliger Reihenfolge, also nie zweimal gleich
- kein Loop-Sprung, keine Datei-Größe, schärfer als ein komprimiertes Video

Das MP4 bleibt als Backup.

---

## Rahmen

- **Format:** 16:9, 1920×1080, 30 fps (auf Wunsch 60 fps), nahtloser Loop, 60 s
- **Ausgabe:** MP4 (H.264) für die OBS-Medienquelle mit „Wiederholen“, optional die HTML-Browserquelle
- **Rechtliches in einem Satz:** Fan-Art von Naruto-Figuren auf dem eigenen Stream ist üblich. Original-Logos,
  Original-Musik und Szenen 1:1 aus dem Anime würde ich weglassen, darum ist hier alles neu gezeichnet
  und neu vertont.
