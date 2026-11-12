# track.site – Whiteboard-Motion-Design (20 s, 16:9)

## Auftrag (für die lokale Sitzung)

Du bist Motion Designer. Mach mit HyperFrames ein 20 Sekunden langes Whiteboard-Video
im Format 16:9 für Track – https://www.track.site/de – den KI-first Tag-Manager mit
serverseitigem Event-Router.

Ziel: Erklär-/Markenclip für Social Media und Website. Zielgruppe: Shop-Betreiber,
Marketer und Agenturen.

Look: wie die Referenz `assets/referenz-whiteboard.png` (FigJam-artiges Board): helles
Punktraster, Polaroid-Fotos mit Klebestreifen, farbige Sticky Notes, ein Kanban-Board,
Live-Cursor mit Namens-Pillen, handschriftliche Notizen in Rot/Lila, gezeichnete Pfeile
und Kringel, oben Board-Titelleiste mit Avataren und „Share board“-Button. Das Layout
der Referenz bleibt erhalten, nur die Inhalte sind Track. Logo exakt (`assets/track-logo.svg`,
#1f4fe0), Schrift Bricolage Grotesque / Inter wie auf track.site, Handschrift z. B. Caveat.

Bewegung: Die Kamera führt den Blick übers Board. Cursor bewegen sich wie echte
Kolleg:innen, Sticky Notes ploppen auf, Annotationen zeichnen sich von Hand, Pfeile
verbinden die Karten. Alle Texte, Formen und Keyframes bleiben editierbar.

Inhalt (nur Aussagen von track.site/de):
- Titel: „Ein Snippet. Jede Plattform.“ – Handschrift darunter: „jede Conversion genau einmal gezählt“
- Kanban „Setup-Sprint“: Zu tun / In Arbeit / Erledigt – z. B. Snippet einbauen,
  Consent verbinden, Meta & Google anbinden, Purchase-Währung ergänzen, Config v15 veröffentlichen
- Stickies: „Nur, was Consent erlaubt, verlässt deine Seite.“ · „Browser + Server, eine Event-ID“ ·
  „Tracking Health Score 100/100“ · „EU-Datenregion“
- Pfeil-Flow: Website → Track → Consent-Check → Meta · Google · TikTok · LinkedIn
- Endkarte: Track-Logo + track.site

Ton: keine Stimme · leichte, freundliche Musik · Klick-, Pop- und Marker-Sounds.

Ziel erreicht, wenn es wie ein echtes, lebendiges Team-Board wirkt, man in 20 Sekunden
versteht, was Track macht, und ein Designer „wow“ sagt.

Sei kreativ. Prüf deine Zwischenstände selbst, bevor du fertig meldest.

## Bilder: Seedream 4.5 über Higgsfield, Unlimited

In Chrome auf higgsfield.ai erzeugen (Unlimited an, Seedream 4.5, Format 3:4, Qualität basic),
danach in `assets/img/` ablegen (polaroid-1.png, polaroid-2.png, flatlay.png).

1. polaroid-1 (Shop-Betreiberin):
   Candid editorial portrait photo of a young female e-commerce shop owner in her small bright online-shop studio, smiling warmly, holding a kraft-paper parcel box with a blank white label, shelves with neatly packed products softly blurred behind her, soft natural window daylight, light beige and white tones, shot on 50mm, shallow depth of field, clean modern, realistic skin, no text

2. polaroid-2 (Performance-Marketer):
   Candid editorial portrait photo of a friendly male performance marketer in his early thirties sitting at a light wooden desk, holding a coffee mug, a laptop open in front of him showing abstract colorful charts, relaxed confident smile looking at camera, soft natural daylight, white and light grey office, plants in the background softly blurred, shot on 50mm, shallow depth of field, realistic, no readable text

3. flatlay (Bestellung):
   Top-down flat lay photo on a warm light-grey desk: hands packing an online order into a kraft-paper box, tissue paper, a small thank-you card without text, a smartphone showing a simple green checkmark confirmation screen, soft natural daylight, clean minimal styling, realistic, no readable text

## Technik-Hinweise aus dem ersten Track-Film (`video-tracksite/`)

- Fonts liegen schon in `video-tracksite/film/assets/fonts/`, GSAP in `.../vendor/gsap.min.js`.
- Schnell rendern: `video-tracksite/tools/capture.cjs` (Playwright, Bild für Bild), dann ffmpeg.
- Beim Seeken per Playwright nie das Timeline-Objekt zurückgeben (`seek(t); return 1;`).
