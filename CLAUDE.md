# Regeln für Claude in diesem Projekt

## Kostenregel (IMMER, ohne Ausnahme)

Gib niemals ungefragt Credits, Tokens oder Geld bei kostenpflichtigen Diensten aus.
Das gilt für Higgsfield, ManyMotions, Creative Claw, HeyGen und jeden anderen Dienst,
der pro Generierung, Upload-Verarbeitung oder GPU-Zeit abrechnet.

Vor JEDER kostenpflichtigen Aktion (Bild, Video, Audio, 3D, Upscale, Preset, GPU usw.):
1. Sag genau, was du starten willst (Modell, Anzahl, Länge, Auflösung).
2. Nenne die Kosten in Credits (vorher mit dem Schätz-Tool abfragen; Schätzen ist kostenlos).
3. Warte auf ein ausdrückliches „Ja“ des Nutzers für genau diese Aktion.

Eine frühere Zustimmung gilt nicht für weitere Generierungen.
Formulierungen wie „mach das“, „erstell vergleichbare Videos“ oder „nutze alle Skills“
sind KEINE Freigabe für Kosten. Im Zweifel: Prompt schreiben und fragen.

Ohne Rückfrage erlaubt: Prompts und Pläne schreiben, vom Nutzer gelieferte Dateien
lokal schneiden und bearbeiten, Dateien im Repo ändern, Kosten schätzen.

## Handy-Screens in Videos (IMMER dieses Verfahren)

Grüne Handy-Bildschirme werden IMMER mit `cardmarket-pro/tools-screen-tracking.py` ersetzt:
- Kanten-Fit: Konturpunkte je Bildschirmseite (ohne runde Ecken) → Geraden → Schnittpunkte = echte 4 Ecken inkl. Perspektive. Nie einzelne Eckpunkte suchen, nie ein gerades Rechteck auflegen.
- Glättung pro Bild adaptiv: liegt das Handy ruhig (Mitte < 6 px/Bild) 7-Tap-Glättung, bei Bewegung keine – auch innerhalb derselben Szene.
- Obere Kante (Notch/kleine Ecken) aus stabilen Seitenkanten + fester Bildschirmhöhe ableiten; Kanten per RANSAC auf der Außenkontur (Finger/Notch ignorieren).
- Oberfläche mit Kamera-Aussparung (Dynamic Island) zeichnen, Logo mit Abstand zur Aussparung.
- Grünen/türkisen Lichtschein um das Handy (60 px) und farbiges Bildschirmlicht auf Gesichtern zu neutralem Weiß umfärben.
- Vor dem Senden messen und nennen: Fit-Fehler und Versatz Oberfläche↔Bildschirm (Ziel ≤ 1,5 px), plus Standbilder in voller Größe prüfen.
- Bilder, in denen das Handy noch grün am Bildrand hereinschwenkt, herausschneiden; danach auf 0 grüne Pixel prüfen.
- Export immer H.264 yuv420p, AAC Stereo 48 kHz.

## Stimmen / Voiceover (IMMER)

Sprachaufnahmen IMMER mit ElevenLabs v4 erzeugen (Higgsfield-Modell `elevenlabs_v4`),
nie mit Seed Audio oder anderen Engines. Texte sind deutsch und müssen akzentfrei
deutsch klingen. Die Kostenregel oben gilt trotzdem: vorher Kosten nennen und Ja abwarten.
