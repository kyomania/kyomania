# fast.site Markenfilm – Briefing (Stand: in Arbeit, pausiert)

## Kernauftrag
**Firmenvorstellung: wer fast.site ist und wofür sie stehen – Philosophie, Leitgedanke, Haltung.**
**Nicht:** Funktionen, Features, Produkt-Demo, was das Programm macht.

## Leitgedanke & Philosophie (aus fast.site/de und fast.site/de/about, nichts erfunden)
- Leitgedanke: „Mach deine Website schneller. Behalte dein Hosting.“
- Behalte, was funktioniert – Anwendung, Inhalte und Hosting bleiben unter deiner Kontrolle.
- Weniger Aufwand. Mehr für deine Website.
- Performance statt Versprechen – miss den Unterschied auf deinen eigenen Seiten; „Ein CDN garantiert kein Google-Ranking.“
- Lass die Ergebnisse entscheiden – 7 Tage, mit Klarheit darüber, was danach passiert.
- Roter Faden: Ehrlichkeit statt Hype, Respekt vor dem, was der Kunde aufgebaut hat.

## Stil (vom Nutzer gewählt)
- Referenz: „Microsoft Loop“ von NotReal (motiondesignawards.com/project/882) – weiches Pastell-3D,
  schillernde/gläserne Formen, fließende Bänder, weiße Doodle-Linien, Bubbles, Studio-Licht.
- Umsetzung in **Blender (Cycles)** via `bpy` – Szene: `blender/scene_leitgedanke.py`.
- Verworfen: gemalter Cel-Look, „Messlabor“ (zu langweilig), flache „Chevrons“-Plakate.

## Für die Weiterarbeit beachten
- Der aktuelle Styleframe (`3d/loop_blender.png`) zeigt noch die fast.site-Oberfläche und
  Bubbles wie „Nur schneller“ – das ist zu produktlastig. Bildsprache stattdessen über
  **Symbole für Haltung**: z. B. ein Zuhause/Ort, schützende Hände/Hülle, Wurzeln/Fundament,
  eine Waage oder Messinstrument für Ehrlichkeit, Offenheit/Transparenz (Glas!), Ruhe statt Hektik.
- Logo als glänzendes 3D-Objekt bleibt (exakte Farben).
- Skript-Entwurf „Behalte, was funktioniert“ (ca. 30 s): siehe Chatverlauf; Sprechertext
  philosophisch, keine Feature-Aufzählung.

## Render-Planung
- 4 CPU-Kerne, keine GPU: ~90 s/Frame in voller Qualität, ~10 s/Frame bei halber Auflösung.
- Empfohlen: Option A – 3D in halber Auflösung (540×960), hochskaliert; Typo/Overlays scharf
  in HyperFrames. Geschätzt 1,5–2 Std. Renderzeit für ~25 s.
- `bpy` liegt nur im Scratchpad-venv dieser Sitzung; in neuer Sitzung neu installieren:
  `python3 -m venv venv && venv/bin/pip install bpy`
