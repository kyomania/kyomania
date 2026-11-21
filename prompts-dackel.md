# KI-Prompts: „Der Weg nach Hause“

Die Prompts sind auf Englisch, weil die Videomodelle Englisch am besten verstehen. Gesprochene Sätze und Texte im Bild bleiben **deutsch** und stehen in Anführungszeichen, jeweils mit dem Zusatz „in German“.

## Wie du vorgehst
1. Erzeuge zuerst ein **Startbild (Keyframe)** pro Shot mit einem Bildmodell. Hänge die passenden Referenzbilder an (siehe unten).
2. Animiere dieses Bild dann mit **Image-to-Video** (Kling, Veo oder Seedance) und dem Video-Prompt.
3. Setze den **Style-Block** an das Ende jedes Prompts.

**Style-Block (immer anhängen):**
`cinematic film still, anamorphic 2.39 look in 16:9 frame, 35mm film grain, shallow depth of field, realistic, highly detailed fur, consistent character, no text unless specified`

**Cookie-Block (in jeden Shot mit Cookie):**
`Cookie, a female long-haired dapple merle dachshund, silver-beige and grey-brown marbled coat, tan points on face, chest and legs, long wavy blonde-tipped ears, plumed tail, amber-brown eyes, brown nose, wearing a red bandana`

**Negativ-Prompt:**
`gore, blood splatter, extra legs, deformed paws, short-haired dog, different breed, cartoon, english text, watermark`

---

## Referenzbilder: Was du brauchst

**Minimum: 8 Bilder. Ideal: 10–12.**

| # | Referenz | Anzahl | Hinweis |
|---|----------|--------|---------|
| 1 | **Cookie: Character Sheet** von vorne, seitlich und hinten | 1 | Hast du schon. Füge das **rote Halstuch** hinzu, sonst fehlt es in den Shots. |
| 2 | **Cookie: Gesichts-Close-up** | 1 | Für Shot 2, 6 und 15. Augen und Fellzeichnung müssen gut sichtbar sein. |
| 3 | **Cookie: in Bewegung** (rennend oder schleichend, seitlich) | 1 | Ohne dieses Bild verändern Modelle beim Laufen oft die Körperform. |
| 4 | **Cookie: verdreckt/verwildert** (nasses, zerzaustes Fell) | 1 | Optional. Für Akt 3 und 4, damit der Verfall stimmig bleibt. |
| 5 | **Lena** (8 J.): Gesicht und Ganzkörper, gleiche Kleidung | 1–2 | Zum Beispiel gelbe Regenjacke, damit sie sofort wiedererkannt wird. |
| 6 | **Mutter und Vater**: Ganzkörper | 1 | Ein Bild mit beiden zusammen reicht. |
| 7 | **Zombie-Design**: Gesicht und Ganzkörper | 1 | Damit alle Zombies einheitlich aussehen. |
| 8 | **Die Überlebende** | 1 | Nur für Shot 11. |
| 9 | **Das Haus** (heil und verfallen) | 1–2 | Für Shot 1, 3 und 5. |
| 10 | **Der Leuchtturm / die sichere Zone** | 1 | Für Shot 12 bis 16. |

**Tipps:**
- Erstelle alle Referenzen mit demselben Modell und demselben Seed. Bei Higgsfield geht das gut als **Character/Element**. Cookie als festen Charakter anzulegen bringt am meisten.
- Hänge pro Shot höchstens 2–3 Referenzen an: Cookie und die jeweilige Person oder den Ort.
- Für den Übergang zum nächsten Shot kannst du den letzten Frame eines Clips als Startbild des nächsten verwenden.

---

## Akt 1: Der Ausbruch

**Shot 1 (0:00–0:15) · Refs: Cookie Sheet, Lena, Haus**
> Wide shot, slow dolly-in towards a suburban German row house at golden hour. In the garden, Lena (8, yellow raincoat) throws a red ball, Cookie [Cookie-Block] joyfully chases it across the grass. On the far horizon, thin columns of smoke rise into the warm sky. Warm, nostalgic, peaceful but ominous.

**Shot 2 (0:15–0:30) · Refs: Cookie Close-up**
> Extreme close-up of Cookie's amber eyes reflecting a flickering TV screen, then pan to a living room TV showing a breaking news banner reading "EILMELDUNG: Unbekanntes Virus – Infizierte greifen Menschen an" in German, the image glitches into static. Dim interior light, tense.

**Shot 3 (0:30–0:50) · Refs: Cookie Sheet, Familie, Lena, Zombie**
> Handheld shaky camera, night street lit by flashing blue emergency lights. A family of three rushes to their car carrying bags, panic in the street, silhouetted infected figures staggering in the background with jerky movements. Cookie [Cookie-Block] flinches at a scream and runs into a dark side alley. Chaotic, frightening, no gore.

**Shot 4 (0:50–1:05) · Refs: Lena, Zombie**
> Low ground-level wide angle from a dog's perspective. A car speeds away down a night street, pale zombies reaching after it. In the rear window, Lena presses her hands against the glass, shouting "COOKIE!" in German, tears on her face. The car disappears, the street falls silent.

## Akt 2: Die tote Stadt

**Shot 5 (1:05–1:20) · Refs: Cookie verdreckt, Haus verfallen**
> Static wide shot, timelapse in front of the same row house slowly decaying over weeks: windows break, graffiti appears, leaves pile up, zombies shuffle past. Under the porch, Cookie [Cookie-Block] hides and waits, getting thinner and scruffier. Desaturated grey-green tones.

**Shot 6 (1:20–1:40) · Refs: Cookie Close-up**
> Close-up of Cookie's nose sniffing a child's yellow scarf lying in an abandoned military checkpoint, next to a crumpled flyer reading "Sichere Zone: Leuchtturm – Küste" in German. Rack focus from the flyer to Cookie lifting her head with determination. Dusty light beams.

**Shot 7 (1:40–2:00) · Refs: Cookie in Bewegung**
> Drone shot rising up from a tiny dachshund [Cookie-Block] walking alone down the center of a destroyed city boulevard, burnt-out cars, smoke, zombie hordes far in the distance. Epic scale, lonely, overcast sky. Leave the upper third empty for the title "Der Weg nach Hause" (title added in post).

## Akt 3: Durch die Apokalypse

**Shot 8 (2:00–2:20) · Refs: Cookie in Bewegung, Zombie**
> Ground-level tracking shot alongside Cookie [Cookie-Block] sneaking underneath rows of abandoned cars on a jammed highway. Above her, the dragging feet of zombies shuffle past. She freezes and holds still. Tense, quiet, grey daylight.

**Shot 9 (2:20–2:40) · Refs: Cookie verdreckt, Zombie**
> Medium shot inside an overturned bus at night, thunderstorm, cold blue light. Cookie [Cookie-Block] curls up asleep on a torn seat. A lightning flash reveals a zombie face pressed against the window right above her. She opens her eyes and stays perfectly still. Suspense.

**Shot 10 (2:40–3:00) · Refs: Cookie in Bewegung, Zombie**
> Fast-paced handheld action. In a looted supermarket, Cookie [Cookie-Block] knocks over a tin can, it clatters loudly, a horde of zombies turns. She sprints through the aisles between empty shelves and escapes through a small ventilation shaft at the last second. Dynamic, no gore.

**Shot 11 (3:00–3:15) · Refs: Cookie verdreckt, Überlebende**
> Soft wide shot inside a barricaded barn lit by warm firelight. A weathered woman survivor kneels and gives Cookie [Cookie-Block] water and food, then points at a hand-drawn map and says in German: "Der Leuchtturm … da musst du hin." Warm, hopeful.

**Shot 12 (3:15–3:30) · Refs: Cookie in Bewegung, Leuchtturm**
> Crane shot over a misty field at dawn, Cookie [Cookie-Block] small in the frame running towards the coast. On the horizon: a lighthouse, fences, floodlights and a protective wall by the sea. Seagulls, first rays of sunlight, rising hope.

## Akt 4: Die sichere Zone

**Shot 13 (3:30–3:45) · Refs: Cookie verdreckt, Zombie, Leuchtturm**
> Low point-of-view at a tall chain-link fence, guards with flashlights behind it, a gate closing. Zombies shuffle closer from behind. Cookie [Cookie-Block] squeezes under the fence at the last second. Alarm lights, tension.

**Shot 14 (3:45–4:00) · Refs: keine (Cookie nur als Zeichnung)**
> Close-up of a wall covered in missing-person notes. Among them, a child's crayon drawing of a long-haired dachshund with a red bandana, handwritten in German: "Wer hat Cookie gesehen? – Lena". Soft morning light, emotional.

**Shot 15 (4:00–4:15) · Refs: Lena, Cookie Close-up**
> Wide shot of Lena (8, yellow raincoat) from behind in the safe zone camp, she slowly turns around, dolly zoom onto her face as she recognizes her dog. Reverse shot: Cookie [Cookie-Block] frozen, ears up. Complete silence, time stands still.

**Shot 16 (4:15–4:30) · Refs: Cookie Sheet, Lena, Familie**
> Slow motion, backlit by the sunrise over the sea. Cookie [Cookie-Block] runs towards Lena, Lena falls to her knees and hugs her, the parents rush in and embrace them both. Tears and laughter, golden light, close-up on the red bandana. Fade to black.
