# Grafiken für das Whiteboard-Video „Die Lizenz zum Erfolg“

**Regeln für alle Grafiken**
- **Kein Text in den Bildern.** Alle Wörter und Zitate kommen als echte AE-Textebenen dazu, damit sie editierbar bleiben und korrekt geschrieben sind.
- **Transparenter Hintergrund (PNG)**, außer bei G01. Klappt das nicht, auf Weiß generieren und danach mit Higgsfield `remove_background` freistellen.
- **Keine Logos echter Firmen** (z. B. kein Microsoft-Logo bei „Goliath“) und **kein Porträt von Soheil** generieren. Für ihn nehmen wir echte Fotos (siehe „Von dir“).
- Modell: GPT Image 2 (Higgsfield-Standard), 1:1 für Objekte, 16:9 für Plates. Die Figur zuerst als Referenz erstellen (G10) und bei G11–G14 als Referenzbild mitgeben, damit sie gleich aussieht.

**Stil-Baustein** (an jeden Prompt anhängen):

```
STYLE: hand-drawn whiteboard marker illustration, confident black dry-erase marker lines with slight wobble, minimal flat fill, single accent color warm yellow #F5C400 used sparingly, no other colors, no shading gradients, clean isolated object, transparent background, no text, no letters, no logos
```

---

## Von dir (nicht generieren)

| # | Was | Warum |
|---|---|---|
| V1 | **Buchcover** als hochauflösende Datei (PNG/JPG, ideal ≥ 2000 px hoch, oder PDF vom Verlag) | Hauptbild am Ende, muss exakt stimmen |
| V2 | **1–2 Pressefotos von Soheil** (am liebsten freigestellt) | Kurz als Foto-Sticky-Note auf dem Board, statt eines generierten Gesichts |
| V3 | Optional: **Schriftart des Covers** (oder OK für eine Ersatzschrift wie „Bebas Neue“ / „Oswald“) | Titel im gleichen Look |
| V4 | Optional: **Namen für die 3 Cursor** (z. B. „Soheil“, „Lehrerin“, „Kunde“ oder „Du“) | Die Cursor sind Teil der Story |

---

## Board und Grundbausteine

**G01 – Whiteboard-Plate** (16:9, 3840×2160, KEIN Transparenz)
```
A large clean white whiteboard surface seen straight on, filling the entire frame, subtle realistic texture: faint ghost marks of erased marker, very light grey smudges, soft even studio light, no frame visible, no objects, no text, photographic, high resolution, 16:9
```

**G02 – Sticky Notes, 4 Varianten** (je 1:1, einzeln generieren)
```
A single square sticky note, [VARIANT], seen from the front, slight paper texture, soft drop shadow, isolated on transparent background, no text, no writing, photographic but clean
```
Varianten: `bright yellow #F5C400, flat` · `bright yellow #F5C400, bottom right corner slightly curled up` · `plain white, flat` · `plain white, slightly rotated with a small piece of clear tape on top`

**G03 – Marker-Hand** (1:1)
```
A realistic right hand holding a black whiteboard marker, pen tip pointing down-left as if drawing, cut off at the wrist, neutral skin, isolated on transparent background, soft studio light, photographic, no text
```

**G04 – Annotations-Pack** (16:9, ein Sheet, danach in AE ausschneiden – oder in AE selbst als Shapes zeichnen)
```
A sheet of separate hand-drawn whiteboard annotation marks spread out with space between them: 3 loose circles, 2 wavy underlines, 1 double underline, 4 curved arrows of different lengths, 1 zigzag arrow, 1 star burst, 2 exclamation marks, 1 question mark, 1 checkmark, 1 cross, 1 bracket. Black marker, a few marks in yellow #F5C400. STYLE: ...
```
> Tipp: Die Pfeile und Kreise, die sich „einschreiben“ sollen, baue ich in AE als Shape-Layer mit Trim Paths. G04 ist nur Vorlage/Textur.

**Cursor:** nicht generieren. Ich baue sie als AE-Shapes (Pfeil + Namens-Pille in Gelb, Schwarz, Weiß), damit Bewegung und Namen editierbar bleiben.

---

## Die Figur (ein Charakter, mehrere Lebensphasen)

**G10 – Figuren-Referenz** (16:9, zuerst erstellen)
```
Character reference sheet of ONE simple whiteboard doodle character: a young man with short dark hair and a short full beard, drawn with minimal lines, dot eyes, expressive eyebrows, wearing a plain t-shirt. Show the same character three times side by side: front view neutral, side view walking, front view with arms crossed and confident. Black marker only, yellow #F5C400 only on the t-shirt. STYLE: ...
```

**G11 – Als Kind im Auto, Blick zum Flugzeug** (1:1, Referenz G10)
```
The same doodle character as a small boy (about 8 years old, no beard) sitting in the back seat of a simple doodle car, looking out of the window with big curious eyes at an airplane taking off, swimming goggles around his neck. STYLE: ...
```

**G12 – Als Schüler, klein und zusammengesunken** (1:1, Referenz G10)
```
The same doodle character as a teenage schoolboy (no beard) sitting slumped at a small school desk, head low, a large shadow of an adult teacher figure pointing a finger at him from the side, an empty speech bubble above the teacher. STYLE: ...
```

**G13 – Nachts am alten Laptop** (1:1, Referenz G10)
```
The same doodle character as a young man (light stubble) hunched over an old bulky laptop at a kitchen table at night, laptop screen glowing yellow #F5C400 on his face, a coffee mug, a small moon in a window behind him, tired but focused. STYLE: ...
```

**G14 – Als Unternehmer, aufrecht** (1:1, Referenz G10)
```
The same doodle character as an adult with full beard standing upright and calm, hands in pockets, looking forward with determination, a long winding path behind him leading up from the bottom of the frame. STYLE: ...
```

---

## Story-Objekte (je 1:1, transparent)

**G20 – Flughafen statt Schwimmbad**
```
An airplane taking off at a steep angle with a dotted flight path line behind it, a small swimming pool sign crossed out next to it. STYLE: ...
```

**G21 – Zeugnis / zurückgestuft**
```
A school report card sheet with scribbled lines instead of text, a big downward arrow next to it, and a small stair step going down. STYLE: ...
```

**G22 – Wecker 03:00**
```
A classic twin-bell alarm clock, hands pointing to three o'clock, small motion lines around the bells. Clock face filled yellow #F5C400. STYLE: ...
```

**G23 – Zehn USB-Sticks + Geldbündel**
```
Ten small USB sticks fanned out in a row, next to a thin stack of banknotes held by a paper band, a balance scale tipping between them. STYLE: ...
```

**G24 – Geschlossenes Paket**
```
A closed cardboard shipping box with tape across the top, a shipping label with scribbled lines, a small question mark floating above. STYLE: ...
```

**G25 – Offenes Paket, nur eine Münze**
```
The same cardboard shipping box now open and empty inside, flaps open, with one single coin lying at the bottom glowing yellow #F5C400, a small dust cloud. STYLE: ...
```

**G26 – Tresen vs. Online-Shop**
```
Split composition: left side a simple bar counter with a beer tap and a tired small figure behind it, right side a laptop with a shopping cart icon on screen and coins flying out toward the viewer, a yellow arrow pointing from left to right. STYLE: ...
```

**G27 – David gegen Goliath**
```
A tiny doodle figure with a slingshot standing at the bottom left, facing a gigantic generic glass corporate skyscraper that towers over him and casts a long shadow, the skyscraper has no logo and no text. The small figure is outlined in yellow #F5C400. STYLE: ...
```

**G28 – 7:00 Uhr, Polizei an der Tür**
```
A front door of an apartment seen from the hallway, a police cap and the silhouette of an officer's shoulder visible through the frosted door glass, a small wall clock showing seven o'clock. STYLE: ...
```

**G29 – Der Kunde**
```
A doodle customer figure holding a phone with a frustrated expression and a jagged speech bubble with a lightning symbol, next to a headset and a simple support ticket card. STYLE: ...
```

**G30 – Außen vs. Innen (der Weg)**
```
Two paths side by side from bottom to top ending at the same flag on a hilltop: the left path is one perfectly straight clean line, the right path is a chaotic tangled scribble full of loops, dead ends and small crosses. The flag is yellow #F5C400. STYLE: ...
```

**G31 – Eisberg „Ergebnis vs. Kosten“** (für den Kernsatz)
```
An iceberg in water: the small tip above the waterline is clean and shiny with a tiny trophy on it, the huge part below the waterline is filled with doodle icons: an alarm clock, an empty box, a coin, a police cap, a crossed-out report card, a laptop. Waterline drawn in yellow #F5C400. STYLE: ...
```

---

## Ablauf: wo welche Grafik vorkommt (60 s, 16:9)

| Zeit | Szene | Grafiken | Bewegung |
|---|---|---|---|
| 0–5 s | Hook: „Erfolg sieht von außen einfach aus.“ | G01, G30 (nur linker Pfad), G14 | Cursor „Du“ fährt rein, Sticky Note poppt |
| 5–12 s | Flughafen, Schule | G11, G20, G12, G21 | Zitat „Aus dem wird nichts.“ auf gelber Sticky Note, roter Kreis → dann „Den kriegen wir hin.“ |
| 12–22 s | 03:00, USB-Sticks, Münze | G13, G22, G23, G24 → G25 | Pfeile verbinden die Notes, Paket „öffnet“ sich (Wechsel G24→G25) |
| 22–32 s | Tresen vs. online, David gegen Goliath, 7:00 Uhr | G26, G27, G28 | zwei Cursor „ziehen“ Notes gegeneinander, Hochhaus wächst |
| 32–42 s | „Am Anfang stand jedes Mal ein Kunde.“ | G29, G14 | Sticky Notes reihen sich zu einer Linie |
| 42–52 s | „Du siehst das Ergebnis. Nicht, was es gekostet hat.“ | G31, G30 ganz | Zoom raus: alle Notes ergeben den chaotischen Pfad |
| 52–60 s | Buch + CTA | V1, V2, G02 | Cover als große Sticky Note, „Jetzt bei Amazon, Thalia, Hugendubel, bücher.de“ |

**Summe:** 24 generierte Bilder (G01, G02 ×4, G03, G04, G10–G14, G20–G31) + 2–4 Dateien von dir.
