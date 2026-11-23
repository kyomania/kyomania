# cardmarket.pro – Master-Prompt „Kreativ-Generator“ (Seedance, 10 s + Logo-Abspann)

Freigabe 23.11.2026: volle kreative Freiheit (Ton, Figuren, Handy optional). Kinder im Bild → beim Posten als KI-generiert kennzeichnen.

Zweck: Jeder Durchlauf erzeugt eine NEUE Idee. Fest sind nur Thema (Sammelkarten-Börse), Regeln und Ende. Alles andere entscheidet die KI.

## So benutzen
1. Block A unverändert kopieren.
2. In Block B nichts ausfüllen (volle Freiheit) – oder 1 Würfel-Zeile aus Block C einsetzen, wenn eine Richtung gewünscht ist.
3. Ergebnis an Claude → Screen-Tracking, Arthur-VO (Kosten vorher), Musik A, Schlusssatz.

## Block A – Rahmen (immer gleich)
```
Vertical 9:16 cinematic short film, 10 seconds, 1080p. You are a bold, award-winning commercial director. Invent an ORIGINAL, surprising mini-story — your own concept, genre, setting, characters and twist. Do not make a generic ad.

THEME (must be obvious in every version): trading cards and the world of a card marketplace — collecting, discovering, valuing, trading, selling, sending or finding the right card. Trading cards must be visible and central to the story.

CREATIVE FREEDOM: choose any genre (comedy, thriller, heist, nature documentary, sci-fi, western, horror-parody, sports commentary, slow-motion epic, retro VHS, stop-motion look, etc.), any setting, any era and any characters. Any tone is allowed: family-friendly, absurd, dark humor, parody, epic. Children, adults, animals or no people at all — your choice. Surprise the viewer within the first second. Fast hard cuts roughly every second; the story must be understandable without words.

HARD RULES:
- Trading cards: original, unbranded collectible cards with colorful fantasy artwork and shiny gold or silver frames; no readable text, no logos, not from any existing game or franchise.
- A smartphone is OPTIONAL — use it only if it serves your story. If a smartphone appears: portrait orientation, screen is a flat solid bright green placeholder, fully in frame from its first appearance, no fingers on the screen. When scanning a card: strictly top-down, card and phone both tall vertical rectangles, phone perfectly flat, level and parallel directly above the card, covering the lower half to three quarters of it, phone not moving. The phone casts only soft neutral white light — never green or teal light anywhere.
- No intelligible speech in any language, no voiceover, no singing; nobody forms words on camera. Non-verbal sounds only (laughter, gasps, sighs, murmur).
- No on-screen text, no logos, no brand names, no real people, no celebrities, no existing characters.
- Final second: the story resolves and the camera settles into calm, empty, dark graphite negative space (space for the logo end card).
- Look: cinematic, realistic lighting, dark graphite tones with a thin red rim light as the brand accent; your genre may add its own flavor on top.

Audio: sound design that fits your genre, no words, no copyrighted music.
```

## Block B – optionaler Impuls (leer lassen = volle Freiheit)
```
Creative impulse for this version: [leer lassen ODER eine Zeile aus Block C]
```

## Block C – Würfel-Impulse (zufällig eine wählen, oder kombinieren)
| # | Genre / Stil | Situation |
|---|---|---|
| 1 | Natur-Doku | Ein seltenes Exemplar wird in freier Wildbahn (Wohnzimmer) entdeckt |
| 2 | Heist-Film | Ein Team plant den perfekten Tausch |
| 3 | Western-Duell | Zwei Sammler, eine Karte, Sonnenuntergang über dem Küchentisch |
| 4 | Sci-Fi | Eine Karte wird aus der Zukunft geschickt |
| 5 | Sport-Highlight | Zeitlupen-Replay eines legendären Kartenfunds |
| 6 | Retro-VHS 1998 | Kinderzimmer-Archiv, gefunden 2026 |
| 7 | Horror-Parodie | Etwas lauert unter dem Bett – es ist ein Ordner |
| 8 | Liebesgeschichte | Zwei Hälften eines Sets finden zueinander |
| 9 | Kochshow | Rezept für die perfekte Sammlung |
| 10 | Spionage | Übergabe eines Umschlags im Park |
| 11 | Stummfilm 1920er | Schwarz-weiß, übertriebene Gesten |
| 12 | Museumsführung | Die Sammlung im Kinderzimmer als Ausstellung |

## Feste Nachbearbeitung (Claude)
- Grünen Screen per `tools-screen-tracking.py` ersetzen (Scanner / Portfolio / Angebot)
- Arthur-VO 3–4 kurze Sätze (Kosten vorher, Ja abwarten) + „cardmarket punkt pro.“ vor dem Logo + Schlusssatz „Die Sammelkartenbörse, der du vertrauen kannst.“ auf dem Logo
- Musik A (`audio/musik-lofi-a.mp3`), Logo-Endcard, Ausblende ins Schwarz, H.264 yuv420p
