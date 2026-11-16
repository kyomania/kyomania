# fuzzn Hidescreen v3 – „Endless Walk“

**Idee:** fuzzn läuft die ganze Zeit nach rechts und bleibt dabei in der Bildmitte. Nur die Papierwelt zieht an ihm vorbei, so dass es aussieht, als würde er endlos laufen. Das Video beginnt und endet im Zimmer vor dem PC mit „LOOKING FOR MATCH“, deshalb ist der Loop nahtlos.

**Look:** dieselbe Papier-Figur wie bisher (Referenz `src/f0_base.webp`), handgemachtes Papercut-Diorama, Berlin bei Nacht.

**Einstellungen Bilder:** Seedream 4.5, 2K (Qualität „high“), 16:9, bei Panoramen 21:9, Referenzbild immer `f0_base` hochladen.

---

## 1. Aufbau: eine Welt aus Ebenen (wie ein Pop-up-Buch)

Damit das „endlose Laufen“ wirklich nahtlos aussieht, baue ich die Lauf-Passagen nicht als einzelne KI-Clips, sondern aus Ebenen, die ich selbst bewege:

| Ebene | Inhalt | Bewegung |
|---|---|---|
| 1 Himmel | Nachthimmel, Mond, Sterne aus Papier | steht fast |
| 2 **SEARCHING** | riesige Papierbuchstaben über der ganzen Skyline | zieht sehr langsam mit; bei Zooms und Kamerafahrten (z. B. am Krankenhaus) nur teilweise lesbar |
| 3 Pop-up-Häuser | einzelne Papierhäuser, die von rechts reinkommen, sich wie in einem Pop-up-Buch **aufklappen**, vorbeiziehen und links wieder zuklappen | mittel |
| 4 Straße | Gehweg, Bordstein, Pfützen | so schnell wie seine Schritte |
| 5 **fuzzn** | Lauf-Animation vor Greenscreen, von mir freigestellt und geloopt | bleibt in der Mitte |
| 6 Vordergrund | Laternen, Regen, Mülleimer, Papierschnipsel | am schnellsten; verdeckt nebenbei die Szenenwechsel |

Die Aktionen unterwegs (Freunde, Döner, Joint, rauchen) sind ebenfalls Greenscreen-Clips von fuzzn. Ich setze sie in dieselbe Welt, damit Hintergrund und Laufrichtung durchgehend gleich bleiben.

Nur vier Momente sind Vollbild-Clips: das Zimmer am Anfang, die Schuhe, Oma im Krankenhaus und das Zimmer am Ende.

---

## 2. Ablauf (Vorschlag: 90 Sekunden)

60 Sekunden sind für alle Stationen sehr knapp, jede Aktion wäre nur 2–3 Sekunden lang. 90 Sekunden geben jeder Station Luft. Mit 60 Sekunden geht es auch, dann straffe ich.

| Zeit | Was passiert | Quelle |
|---|---|---|
| 0–4 | Zimmer, von hinten: fuzzn am PC, auf dem Monitor „LOOKING FOR MATCH“. Er steht auf. | Vollbild-Clip V1 (Text setze ich selbst auf den Monitor) |
| 4–7 | Close-up: er zieht seine weißen Air Force 1 an | Vollbild-Clip V2 |
| 7–10 | Er tritt aus der Haustür seines Plattenbaus und läuft los nach rechts | Ebenen + Haus H1 |
| 10–20 | **Lauf 1** durch den Kiez: Späti, Graffiti-Wand. Bei ca. 14 s kommen zwei Freunde entgegen, er dreht sich im Gehen einmal um 360° und gibt ihnen Handschlag | Ebenen + G1, G4 |
| 20–27 | Döner-Laden zieht heran, er biegt in den Eingang ab, kurzer Zeitsprung, kommt mit Döner raus und beißt im Gehen rein | Ebenen + H4, G2 |
| 27–37 | **Kotti:** unter der Hochbahn am Kottbusser Tor steckt ihm ein Typ im Vorbeigehen einen Joint zu. Er zündet ihn an und läuft rauchend weiter | Ebenen + H5, G5, G3 |
| 37–41 | Krankenhaus kommt, er macht den Joint aus und geht rein | Ebenen + H6 |
| 41–47 | Die Kamera fährt außen an der Krankenhaus-Fassade hoch bis zu Omas Fenster. „SEARCHING“ dahinter ist dabei nur noch angeschnitten | Kamerafahrt über H6 |
| 47–53 | Durchs Fenster: er gibt Oma einen Kuss auf die Stirn, sie lächelt, kleines Herz | Vollbild-Clip V3 |
| 53–57 | Kamera fährt wieder runter, er kommt unten raus und läuft weiter | Kamerafahrt + G1 |
| 57–75 | **Lauf 2 mit Aktionen:** wirft das Döner-Papier wie einen Basketball in den Mülleimer (Swish), schaut auf die Uhr („NOCH AM SUCHEN…“) | Ebenen + G6, G8 |
| 75–80 | Zurück am Plattenbau, er geht durch die Haustür rein | Ebenen + H1 |
| 80–85 | Zimmer: er kommt rein, zieht die Schuhe aus und stellt sie an die Tür | Vollbild-Clip V4 |
| 85–90 | Er setzt sich an den PC, auf dem Monitor steht immer noch „LOOKING FOR MATCH“. Das letzte Bild ist identisch mit dem ersten → nahtloser Loop | Vollbild-Clip V5 (Endbild = Startbild) |

Überall unten links bleibt das HUD: „LOOKING FOR MATCH · twitch.tv/fuzzn · dfuzzn“.

---

## 3. Bilder (Seedream 4.5, 2K, Referenz `f0_base`)

Jeder Prompt endet mit diesem Stil-Satz:
`Handmade layered papercut diorama photographed, real cut and folded paper with visible texture and fibres, strong depth shadows, Berlin at night, cinematic.`

### 3a. Welt-Elemente (vor Magenta, damit ich sie freistellen kann)

| ID | Format | Prompt-Kern |
|---|---|---|
| W1 SEARCHING | 21:9 | Giant three-dimensional letters spelling exactly "SEARCHING", cut from thick off-white and light grey paper with visible layers and folded edges, standing upright side by side, slightly irregular hand-cut look, soft paper shadows, isolated on a perfectly flat solid magenta (#FF00FF) background, no other text. |
| W2 Himmel | 21:9 | Night sky made of layered dark navy and purple paper, a big round paper moon, small paper stars, soft paper clouds, no buildings, no text. |
| W3 Straße | 21:9 | Side view of a Berlin sidewalk and street strip at night made of paper: grey paving slabs, curb, wet asphalt with small paper puddles and reflections, seen straight from the side, isolated on solid magenta above the curb line, no text. |
| H1 Plattenbau | 16:9 | Front view of a grey East-Berlin Plattenbau apartment block made of paper, many small warm lit windows, a glass entrance door at street level with a small canopy, isolated on solid magenta, no text. |
| H2 Späti | 16:9 | Front view of a small Berlin corner shop (Späti) made of paper, glowing red neon sign that reads exactly "SPÄTI", drinks in the window, isolated on solid magenta. |
| H3 Graffiti-Haus | 16:9 | Front view of an old Berlin Altbau building made of paper with a large graffiti on the ground floor wall that reads exactly "FUZZN", isolated on solid magenta. |
| H4 Döner | 16:9 | Front view of a cosy döner shop made of paper, big glowing sign that reads exactly "HAKIKI DÖNER", open entrance door, warm yellow light inside, rotating döner spit visible, isolated on solid magenta. |
| H5 Kotti | 21:9 | Front view of Kottbusser Tor in Berlin made of paper: the large curved residential complex over the street, the elevated yellow U-Bahn viaduct crossing in front, a blue U-Bahn sign that reads exactly "Kottbusser Tor", isolated on solid magenta. |
| H6 Krankenhaus | 9:16 | Front view of a tall modern hospital building made of paper, seven floors with many windows, red cross and a sign that reads exactly "KRANKENHAUS" above the glass entrance doors, one window on the fifth floor warmly lit, isolated on solid magenta. |
| H7 Straßenmusiker | 16:9 | Side view of a paper street musician playing an acoustic guitar on a small stool, open guitar case with coins, isolated on solid magenta. |
| H8 Laterne | 9:16 | A single tall Berlin street lamp made of paper with a warm glow, isolated on solid magenta. |
| H9 Mülleimer | 1:1 | An orange Berlin street trash can made of paper, isolated on solid magenta. |
| H10 Bäume | 16:9 | Two leafless city trees made of dark paper, isolated on solid magenta. |

### 3b. Startbilder für die Greenscreen-Clips (fuzzn von der Seite)

Alle mit: `full body side view, facing right, plain solid chroma green (#00FF00) background, no floor, no shadow, character fully in frame with space around`.

| ID | Prompt-Kern |
|---|---|
| S1 Laufen | fuzzn mid-stride walking to the right, relaxed confident walk, arms swinging. |
| S2 Döner | fuzzn walking to the right holding a big döner in his right hand, about to bite. |
| S3 Rauchen | fuzzn walking to the right, a lit joint between two fingers, thin smoke curl. |
| S4 Freunde | fuzzn walking to the right, two friends in black streetwear approaching from the right, about to greet him. |
| S5 Joint-Übergabe | fuzzn walking to the right, a guy in a dark hoodie standing at the right edge, hand reaching out for a handshake. |
| S6 Wurf | fuzzn walking to the right, holding a crumpled döner wrapper like a basketball, ready to throw. |
| S7 Tanz | fuzzn walking to the right, starting a small dance move, one foot lifted. |
| S8 Uhr | fuzzn walking to the right, lifting his left wrist to look at his black digital watch. |

### 3c. Vollbilder (Zimmer, Schuhe, Oma)

| ID | Prompt-Kern |
|---|---|
| Z1 Zimmer Start/Ende | Same gaming room as before (Hertha poster, grandma photo, candle ladder, FUZZN LED sign), seen from behind: fuzzn sits at the desk in the gaming chair, the left monitor shows a dark screen (I add "LOOKING FOR MATCH" myself), right monitor dark chat panel. Static camera. |
| Z2 Schuhe | Close-up: fuzzn sitting on the edge of his bed pulling on clean white Nike Air Force 1 low sneakers, hands on the laces. |
| Z3 Oma | View from outside through a hospital window at night: inside, the sweet grandma with grey curls and round glasses lies in a hospital bed, fuzzn leans over and kisses her forehead, warm lamp light inside, rain on the glass. |
| Z4 Schuhe aus | fuzzn in his room by the door, taking off his white Air Force 1 sneakers, placing them neatly next to the door. |

---

## 4. Clips

| ID | Startbild | Bewegung |
|---|---|---|
| G1 Laufen | S1 | locked camera, he walks in place to the right at a steady relaxed pace like on a treadmill, full body always in frame, green background stays plain |
| G2 Döner | S2 | walks in place, takes a big happy bite, chews, keeps walking |
| G3 Rauchen | S3 | walks in place, takes a drag, exhales a curl of paper smoke |
| G4 Freunde | S4 | walks in place, the two friends pass from right to left, he spins once 360° while walking and slaps hands with both, keeps walking |
| G5 Joint | S5 | walks past the guy, quick handshake, a joint is passed into his hand, the guy stays behind, he keeps walking |
| G6 Wurf | S6 | throws the wrapper in a high arc to the right like a basketball shot, celebrates with a small fist pump, keeps walking |
| G7 Tanz | S7 | does a few cool dance steps while moving to the right, then continues walking |
| G8 Uhr | S8 | glances at his watch, rolls his eyes, keeps walking |
| V1 Zimmer Start | Z1 | he takes off his headset, stands up and walks out of frame |
| V2 Schuhe | Z2 | pulls on the sneakers, ties the laces, stands up |
| V3 Oma | Z3 | kisses her forehead, she smiles with closed eyes, he gently strokes her hair |
| V4 Schuhe aus | Z4 | takes off the sneakers and places them next to the door |
| V5 Zimmer Ende | Z1 als Endbild | he walks in, sits down in the gaming chair, puts on the headset, ends exactly on the start frame |

---

## 5. Was ich selbst baue

- Freistellen aller Greenscreen-Clips und Magenta-Elemente, Lauf-Loop sauber geschnitten
- Ebenen-Welt mit Parallax, Pop-up-Aufklappen der Häuser, Kamerafahrt am Krankenhaus
- „LOOKING FOR MATCH“ auf dem Monitor (wie beim Chat, perspektivisch exakt), HUD unten links
- Regen, Papierschnipsel, Licht
- Musik-Loop, Schritte im Takt der Gehbewegung, Pop-up-Papier-Geräusche, Feuerzeug, Kuss
- Schnitt, Render, nahtloser Loop

## 6. Kosten (falls ich hier statt „Unlimited“ mit Credits erzeuge)

| Posten | Menge | Credits |
|---|---|---|
| Bilder Seedream 4.5 (2K, high) | ca. 30 | ca. 30 |
| Clips Kling 3.0 pro, 6 s | 13 | ca. 120 |
| Clips Seedance 2.5, 1080p, 6 s | 13 | ca. 1250 |
| Musik + Geräusche | – | ca. 10 |

„Unlimited“ funktioniert über Claude Code nicht. In der Higgsfield-Oberfläche oder in Claude Desktop geht es.

---

## Stand nach der Logik-Prüfung
- **Kein Tanz:** Straßenmusiker (H7), Startbild S7 und Clip G7 sind gestrichen.
- **Zimmer:** Alle Zimmer-Szenen spielen in exakt derselben Einstellung wie das Start-/Endbild Z1 (das Zimmer aus v2). Er dreht den Gaming-Stuhl zur Kamera und zieht dort die Schuhe an (Z2) bzw. aus (Z4). Es gibt kein Bett und keine Tür, damit die Einrichtung durchgehend gleich bleibt. Z2 und Z4 sind mit Nano Banana Pro als Bearbeitung von Z1 entstanden, weil Seedream den Raum nicht konstant hielt.
- **Monitor:** In allen Zimmerbildern läuft links noch ein KI-Spiel. Das ersetze ich wie in v2 perspektivisch durch „LOOKING FOR MATCH“.
- **Krankenhaus:** Das Kuss-Bild (Z3) zeigt jetzt ein modernes Alu-Fenster in weißer Fassade, passend zum Gebäude H6.
- **Häuser:** Späti und Altbau sind frontaler neu erzeugt. Beim Späti sind die Seitenwände noch leicht zu sehen, die schneide ich weg.
- **Licht:** Die Greenscreen-Bilder bleiben im Studiolicht. Das Nachtlicht (dunkler, warmes Laternenlicht von links, blaues Randlicht) mache ich im Schnitt, weil Seedream beim Umleuchten den grünen Hintergrund zerstört hat.
