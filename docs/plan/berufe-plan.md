# Berufe-Plan: Wechsel in Orgrimmar, Lederverarbeitung und Verzauberkunst bis 150 (erzeugt von `tools/plan_berufe.py`)

Nicht von Hand ändern: Eingaben anpassen (Preise, Route, Modell) und neu erzeugen. Zum Start mit den Preisen des eigenen Realms neu rechnen.

## Quellen

- Lederverarbeitung 1–155: wow-professions, Leatherworking Leveling Guide (Forever-Beta, «still in progress»), abgerufen 14.10.2026 https://www.wow-professions.com/forever/leatherworking-leveling-guide
- Verzauberkunst 1–150: wow-professions, Enchanting Leveling Guide (Forever-Beta), abgerufen 14.10.2026 https://www.wow-professions.com/forever/enchanting-leveling-guide · Entzaubern ab Fertigkeit 1: https://www.wow-professions.com/forever/disenchanting-guide
- Lernstufen und Farben der Rezepte: AHledger, Rezeptseiten (Forever-Beta) https://ahledger.com/wow-forever/professions/leatherworking · https://ahledger.com/wow-forever/professions/enchanting · SeeMeta https://seemeta.com/en/wow-forever/professions/enchanting
- Lehrer und Händler in Orgrimmar: Icy Veins https://www.icy-veins.com/wow-forever/leatherworking · https://www.icy-veins.com/wow-forever/enchanting · kami-labs https://kami-labs.fr/en/guide-enchantement-wow-forever/ · AHledger NPC-Seiten Kithas https://ahledger.com/wow-forever/npcs/3346-kithas und Tamar https://ahledger.com/wow-forever/npcs/3366-tamar · RXP v4.11.23 (Kamari, Auctioneer Thathung)
- Preise: AHledger, Forever-Beta, Normal Horde US (`data/rechnung/Preise.csv`, Stand der Seiten 27.09.–12.10.; `data/kombi/preise_zusatz.csv`). EU-Preise gibt es erst zum Start.
- Entzaubern (Erwartungswert pro Teil): `data/rechnung/Kreislauf.csv` nach der Tabelle von wow-professions.
- Eigener Bestand beim Wechsel: Mengenmodell `docs/plan/mengen-leder.md` (`tools/plan_mengen.py`).
- Fischen: AHledger, Item 6522 Deviate Fish (Lushwater Oasis 35 % von 153 Fängen; Median Normal Horde US 4s 50c, PvP Horde US 10s 99c) https://ahledger.com/items/6522-deviate-fish · Fangrate: Testlog 13.10. (Stonebull Lake).

## Ergebnis in Kürze

- **Sweetspot** für das eigene Leder (Lesart von Claude, Abschnitt 1): Lederverarbeitung 1–80 (Stufe A). Dafür braucht es 99 Fetzen, 62 Leichtes Leder (dazu 33 aus den Fetzen) und 27 Light Hide.
- Laut Modell bringt die Route bis Orgrimmar 66 Leichtes Leder und 76 Fetzen, mit dem Grinden auf Stufe 16 an Raptoren (Farm-Stopp S1, RXP schlägt das Grinden dort ohnehin vor) 79–86 und 83–87. Laut Modell reicht das Leder; die fehlenden Fetzen und Bälge kosten im AH wenig (Stufe A unten).
- Ab LW 80 bringt jedes Leichte Leder 2- bis 5-mal weniger Punkte als davor (Tabelle in Abschnitt 1). Mehr Leder zu farmen bringt 21–34 Silber pro Stunde Materialwert (Beta); Angeln ergäbe etwa 2g 27s 45c pro Stunde (nur Deviate Fish, Rate ungeprüft, Abschnitt 1).
- Kosten (Beta-Preise «jetzt», ohne Lehrer und Rezepte): Stufe A 40s 86c, B 1g 67s 99c, C 2g 73s 40c, D 7g 37s 76c. Derselbe Einkauf mit den 30-Tage-Medianen: A 44s 90c, B 4g 5s 27c, C 3g 50s 93c, D 9g 56s 16c.
- LW 130–150 rechnet der Plan mit dem Tab «ohne Heavy Hide» von wow-professions (billiger bei diesen Preisen, Vergleich in Abschnitt 4).
- Nach allen Stufen bleibt Entzauberungs-Material übrig, das VZ bis 150 nicht braucht (Wert im AH etwa 3g 85s 36c, Abschnitt 5).

## 1. Sweetspot: wie viel eigenes Leder nach Orgrimmar

Lesart von Claude (Rückfrage an den Nutzer offen): «Break-even an Investment von leichtem Leder» heisst hier: eigenes Leder dort einsetzen, wo es viele Punkte bringt, und nur so viel sammeln, wie die Route ohnehin hergibt (plus das Grinden, das RXP selbst vorschlägt). Bei Beta-Preisen ist Kaufen billiger als zusätzliches Farmen (Rechnung unten); bei anderen Preisen kann das kippen.

| Material | LW 1–80 braucht | Route bis Orgrimmar (ohne S1) | mit S1 (untere–obere Rate) | im AH kaufen (mit S1, untere Rate) | Beta-Preis |
|---|---|---|---|---|---|
| Ruined Leather Scraps (Verdorbene Lederfetzen) | 99 | 76 | 83–87 | 16 | 25c |
| Light Leather (Leichtes Leder) | 62 (netto; 33 mehr entstehen aus den Fetzen) | 66 | 79–86 | 0 | 50c |
| Light Hide | 27 | 4 | 5–6 | 22 | 69c |

Die 66 Leder ohne S1 setzen voraus, dass die 5 Plainstrider Kidneys (Quest 821) vor Orgrimmar fallen (Annahme in `modell_leder.csv`; RXP erinnert bis 12-17 #180 daran); ohne sie wären es etwa 60. Ist der Zähler beim Farm-Stopp S1 schon voll, ist S1 nur Zugabe.

Punkte pro Leichtem Leder und Kosten pro Punkt (Plan-Route, Beta-Preise «jetzt»; «zurück» = Wert, der als Material oder beim Entzaubern zurückkommt; netto negativ = Gewinn):

| Stufe | LW | Rezept | Herstellungen | Leichtes Leder | Punkte je Leder | Material (AH/Händler) | zurück | netto je Punkt |
|---|---|---|---|---|---|---|---|---|
| A | 1–30 | Light Leather | 33 | 0 | – | 24s 75c | 16s 50c | 28c |
| A | 30–55 | Cured Light Hide | 27 | 0 | – | 32s 13c | 0c | 1s 29c |
| A | 55–75 | Embossed Leather Gloves | 21 | 63 | 0.32 | 35s 70c | 24s 19c | 58c |
| A | 75–80 | Medium Leather | 8 | 32 | 0.16 | 16s | 15s 28c | 14c |
| B | 80–90 | Cured Medium Hide | 10 | 0 | – | 93s 80c | 0c | 9s 38c |
| B | 90–100 | Fine Leather Belt | 19 | 114 | 0.09 | 60s 80c | 20s 78c | 4s |
| C | 100–115 | Light Leather Pants | 24 | 240 | 0.06 | 1g 44s | 55s 43c | 5s 90c |
| C | 115–125 | Dark Leather Belt | 10 | 0 | – | 55s | 51s 8c | 39c |
| C | 125–130 | Heavy Leather | 7 | 0 | – | 66s 85c | 83s 86c | −3s 40c |
| D | 130–150 | Hillman's Leather Gloves | 24 | 0 | – | 7g 37s 76c | 4g 75s 99c | 13s 9c |

Zeit gegen Gold (Beta-Preise; Raten sind Annahmen, siehe Abschnitt 8):

- Grinden für Leder, Gegner Stufe 11–15: 21–34 Silber pro Stunde Materialwert bei 50–80 Häuten (30-Tage-Preise: 31–49). Dazu gibt es XP; RXP schlägt das Grinden auf Stufe 16 an der Sludge Fen ohnehin vor.
- Angeln an der Lushwater Oasis, nur Deviate Fish gerechnet: rund 51 pro Stunde bei der Fangrate vom Stonebull Lake ergibt 2g 27s 45c pro Stunde (Normal Horde US) bzw. 5g 55s 48c (PvP Horde US). Ungeprüft: Fangrate und nötige Angelfertigkeit im Brachland (keine Forever-Quelle).
- Folgerung (bei diesen Preisen): Grinden nur für Leder lohnt sich erst, wenn Leichtes Leder etwa 4s 74c–7s 58c kostet (heute 50c).

## 2. Ablauf: Stufen A bis D

Stufe A ist die Sitzung in Orgrimmar (LW 1–80, VZ 1–50, beide Gesellen). Stufe B geht dort auch, wenn das Gold reicht; C und D (und B, falls noch offen) kommen in Thunder Bluff (Route «17-22», Stufe 20). Herstellungen laut wow-professions; der Guide-Schritt endet bei der Zielfertigkeit, Rest bleibt für die nächste Stufe.

### Stufe A: LW bis 80, VZ bis 50 (Kern in Orgrimmar: eigenes Leder verarbeiten)

Herstellen (Lederverarbeitung):

- LW 1→30: 33× Light Leather — 99 Ruined Leather Scraps (davon 83 aus dem Vorrat)
- LW 30→55: 27× Cured Light Hide — 27 Light Hide (davon 5 aus dem Vorrat), 27 Salt
- LW 55→75: 21× Embossed Leather Gloves — 63 Light Leather (davon 63 aus dem Vorrat), 42 Coarse Thread
- LW 75→80: 8× Medium Leather — 32 Light Leather (davon 32 aus dem Vorrat)

Entzaubern: 21× Embossed Leather Gloves → erwartet 23.6 Strange Dust, 6.3 Lesser Magic Essence

Verzaubern:

- VZ 1–2: 1× Runed Copper Rod
- VZ 2–20: 18× Enchant Bracer - Inferior Stamina
- VZ 20–50: 6× Enchant Bracer - Minor Deflect
- VZ 20–50: 24× Enchant Chest - Inferior Stamina

Einkauf im AH: 22 Light Hide, 16 Ruined Leather Scraps, 1 Strange Dust = 20s 2c (derselbe Einkauf mit den 30-Tage-Medianen: 24s 6c)
Einkauf beim Händler: 27 Salt, 42 Coarse Thread, 19 Mote of Magic, 1 Copper Rod = 20s 84c

### Stufe B: LW bis 100, VZ bis 100 (in Orgrimmar, wenn das Gold reicht, sonst in Thunder Bluff)

Herstellen (Lederverarbeitung):

- LW 80→90: 10× Cured Medium Hide — 10 Medium Hide, 10 Salt
- LW 90→100: 19× Fine Leather Belt — 114 Light Leather (davon 17 aus dem Vorrat), 38 Coarse Thread

Entzaubern: 9× Fine Leather Belt → erwartet 16.9 Strange Dust, 2.7 Greater Magic Essence, 0.4 Small Glimmering Shard. 10 Fine Leather Belt behalten (für Dark Leather Belt in Stufe C).

Verzaubern:

- VZ 50–70: 8× Enchant Bracer - Minor Deflect
- VZ 50–70: 12× Enchant Chest - Inferior Stamina
- VZ 70–100: 2× Enchant Bracer - Minor Stamina
- VZ 70–100: 30.8× Enchant Chest - Minor Absorption

Einkauf im AH: 10 Medium Hide, 98 Light Leather, 31 Lesser Magic Essence = 1g 59s 19c (derselbe Einkauf mit den 30-Tage-Medianen: 3g 96s 47c)
Einkauf beim Händler: 10 Salt, 38 Coarse Thread = 8s 80c

### Stufe C: LW bis 130, VZ bis 130 (in Thunder Bluff, Stufe 20)

Herstellen (Lederverarbeitung):

- LW 100→115: 24× Light Leather Pants — 240 Light Leather, 24 Cured Light Hide (davon 24 aus dem Vorrat), 24 Fine Thread
- LW 115→125: 10× Dark Leather Belt — 10 Fine Leather Belt (davon 10 aus dem Vorrat), 10 Cured Medium Hide (davon 10 aus dem Vorrat), 20 Fine Thread, 10 Gray Dye
- LW 125→130: 7× Heavy Leather — 35 Medium Leather (davon 8 aus dem Vorrat)

Entzaubern: 24× Light Leather Pants, 10× Dark Leather Belt → erwartet 82.5 Strange Dust, 3.0 Lesser Astral Essence, 7.2 Greater Magic Essence, 1.4 Small Glimmering Shard

Verzaubern:

- VZ 100–109: 18× Enchant Chest - Minor Absorption
- VZ 109–110: 1× Runed Silver Rod
- VZ 110–130: 32× Enchant Cloak - Minor Protection

Einkauf im AH: 240 Light Leather, 27 Medium Leather, 1 Silver Rod, 1 Shadowgem, 1 Lesser Magic Essence = 1g 94s 40c (derselbe Einkauf mit den 30-Tage-Medianen: 2g 71s 93c)
Einkauf beim Händler: 44 Fine Thread, 10 Gray Dye = 79s

### Stufe D: LW bis 150, VZ bis 150 (in Thunder Bluff, der teure Rest bis 150)

Herstellen (Lederverarbeitung):

- LW 130→150: 24× Hillman's Leather Gloves — 336 Medium Leather, 96 Fine Thread

Entzaubern: 24× Hillman's Leather Gloves → erwartet 7.2 Greater Astral Essence, 27.0 Soul Dust, 1.0 Large Glimmering Shard

Verzaubern:

- VZ 130–150: 4× Enchant Boots - Minor Stamina
- VZ 130–150: 16× Enchant Bracer - Lesser Stamina

Einkauf im AH: 336 Medium Leather = 6g 41s 76c (derselbe Einkauf mit den 30-Tage-Medianen: 8g 60s 16c)
Einkauf beim Händler: 96 Fine Thread = 96s

## 3. Lernstufen: wo die Quellen sich widersprechen

wow-professions nutzt diese Rezepte früher, als AHledger sie lernen lässt («orange» = lernbar ab). Im Spiel prüfen; der Guide nennt einen Ausweg.

| Beruf | Rezept | wow-professions ab | AHledger lernbar ab | Quelle |
|---|---|---|---|---|
| VZ | Enchant Bracer - Minor Deflect | 20 | 40 | AHledger Rezeptseite 7428 (ahledger.com/wow-forever/recipes, Recherche 14.10.) · SeeMeta 80/100/120 · Widerspruch: wow-professions nutzt es ab 20 |
| VZ | Enchant Chest - Inferior Stamina | 20 | 30 | AHledger Rezeptseite 7420 (ahledger.com/wow-forever/recipes, Recherche 14.10.) · SeeMeta 70/90/110 · Widerspruch: wow-professions nutzt es ab 20 · kami-labs nennt 15 |

## 4. LW 130–150: Tab «Cured Heavy Hide» oder «ohne Heavy Hide»

wow-professions: «If 20x Heavy Hide cost less than around 120x Heavy Leather, 140x Medium Leather and 17x Moss Agate» → Tab «Cured Heavy Hide», sonst «Leveling without Heavy Hide». Die Regel denkt bis 175; hier zählt nur bis 150.

| Tab | Einkauf A–D (jetzt) | Rückverkauf übriges Material | netto |
|---|---|---|---|
| Cured Heavy Hide | 16g 57s 82c | 1g 88s 83c | 14g 68s 99c |
| ohne Heavy Hide | 12g 20s 1c | 3g 85s 36c | 8g 34s 65c |

Der Plan nimmt «ohne Heavy Hide». Bei anderen Preisen zum Start kann es kippen: neu rechnen.

## 5. Verkaufen im AH

Was nach Stufe D übrig bleibt (Erwartungswert) und nicht für VZ bis 150 gebraucht wird. Ob man es für LW oder VZ über 150 behält, entscheidest du.

| Material | Menge | Wert (jetzt) | Wert (30 Tage) |
|---|---|---|---|
| Greater Astral Essence | 7.2 | 2g 5s 49c | 2g 64s 24c |
| Soul Dust | 11.0 | 79s 31c | 93s 83c |
| Large Glimmering Shard | 1.0 | 75s 83c | 1g 7s 17c |
| Lesser Astral Essence | 3.0 | 18s 12c | 28s 26c |
| Small Glimmering Shard | 1.7 | 6s 30c | 6s 4c |
| Strange Dust (Seltsamer Staub) | 0.4 | 31c | 91c |

Dazu aus der Lederverarbeitung: 3 Cured Light Hide, 7 Heavy Leather. Heavy Leather braucht wow-professions erst ab LW 155.

Produkte der Verzauberkunst (Zauberstäbe, Öle): Die Beta-Zahlen widersprechen sich (Händlerpreis Lesser Magic Wand seit Build 70245 1c, AHledger-Rezeptseiten und Itemseiten mit verschiedenen Ständen; `data/rechnung/Produkte.csv`). Der Plan rechnet deshalb nicht damit; zum Start neu prüfen.

## 6. Preisregeln (Break-even)

Wann sich eine Wahl umdreht. Spalten: Wert mit den Beta-Preisen «jetzt» und mit den 30-Tage-Medianen (AHledger, Normal Horde US); der Plan oben rechnet mit «jetzt». Zum Start mit den eigenen Preisen prüfen.

| Wahl | Regel | jetzt | 30 Tage |
|---|---|---|---|
| Fehlende Fetzen | kaufen, wenn 3 Fetzen weniger kosten als 2 Leichtes Leder; sonst Light Armor Kit (1 Leder) | 75c gegen 1s: Fetzen kaufen | 84c gegen 1s 58c: Fetzen kaufen |
| Extra Embossed Leather Gloves nur zum Entzaubern | lohnt, wenn 1,125 Strange Dust und 0,3 Lesser Magic Essence (Ertrag) mehr wert sind als 3 Leichtes Leder und 2 Coarse Thread | 1s 70c gegen 1s 15c: lohnt nicht, Staub kaufen | 2s 57c gegen 4s 93c: lohnt |
| VZ 20–70 und 100–109 | 1 Strange Dust oder 1 Lesser Magic Essence pro Punkt: das billigere | 69c gegen 84c: Essenz | 7s 35c gegen 2s 42c: Staub |
| VZ 70–100 | Essenz (33 für 30 Punkte) lohnt, solange sie weniger als 1,82 Strange Dust kostet | 69c gegen 1s 53c: Essenz (Chest - Minor Absorption) | 7s 35c gegen 4s 40c: Staub (Bracer - Minor Stamina) |
| VZ 110–130 | Essenz (80, dazu Formel 5s) statt 64 Strange Dust lohnt unter etwa 0,8 Strange Dust pro Essenz | 60s 20c gegen 53s 76c: Staub (Cloak - Minor Protection) | 5g 93s gegen 1g 54s 88c: Staub (Cloak - Minor Protection) |
| VZ 130–150 | Soul Dust (20) statt 80 Strange Dust lohnt unter 4 Strange Dust pro Soul Dust; eigener Soul Dust aus Hillman's zählt 0 | 1g 44s 20c gegen 67s 20c: Staub kaufen | 1g 70s 60c gegen 1g 93s 60c: Soul Dust kaufen |
| LW 130–150 | Tab «Cured Heavy Hide» (20 Heavy Hide, 60 Salt, 14 Hillman's) statt «ohne Heavy Hide» (24 Hillman's), ohne Entzaubern gerechnet | 11g 68s 36c gegen 7g 37s 76c: ohne Heavy Hide | 25g 22s 76c gegen 9g 56s 16c: ohne Heavy Hide |
| Leder grinden statt angeln | Grinden (50–80 Häute pro Stunde, Gegner 11–15) bringt mehr als Angeln (nur Deviate Fish, Rate ungeprüft) | 21s 10c–33s 76c gegen 2g 27s 45c pro Stunde: Angeln | 30s 55c–48s 88c gegen 2g 11s 78c pro Stunde: Angeln |

## 7. Gegenstände im Guide (Item-IDs)

| Gegenstand | deutsch (Testlog) | ID | Quelle |
|---|---|---|---|
| Light Leather | Leichtes Leder | 2318 | AHledger https://ahledger.com/items/2318-light-leather |
| Ruined Leather Scraps | Verdorbene Lederfetzen | 2934 | AHledger https://ahledger.com/items/2934-ruined-leather-scraps |
| Medium Leather | Mittleres Leder | 2319 | AHledger https://ahledger.com/items/2319-medium-leather |
| Light Hide | – | 783 | AHledger https://ahledger.com/items/783-light-hide |
| Medium Hide | – | 4232 | AHledger https://ahledger.com/items/4232-medium-hide |
| Heavy Hide | – | 4235 | AHledger https://ahledger.com/items/4235-heavy-hide |
| Salt | – | 4289 | AHledger https://ahledger.com/items/4289-salt |
| Coarse Thread | – | 2320 | AHledger https://ahledger.com/items/2320-coarse-thread |
| Fine Thread | – | 2321 | AHledger https://ahledger.com/items/2321-fine-thread |
| Gray Dye | – | 4340 | AHledger https://ahledger.com/items/4340-gray-dye |
| Cured Light Hide | – | 4231 | AHledger https://ahledger.com/items/4231-cured-light-hide |
| Cured Medium Hide | – | 4233 | AHledger, Ergebnis-Link der Rezeptseite 3817 (Recherche 14.10.) |
| Embossed Leather Gloves | – | 4239 | Wowhead-Link in data/rechnung/Kreislauf.csv · AHledger, Ergebnis-Link der Rezeptseite 3756 |
| Fine Leather Belt | – | 4246 | Wowhead-Link in Kreislauf.csv · AHledger Rezeptseite 3763 |
| Light Leather Pants | – | 7282 | Wowhead-Link in Kreislauf.csv · AHledger Rezeptseite 9068 |
| Dark Leather Belt | – | 4249 | Wowhead-Link in Kreislauf.csv · AHledger Rezeptseite 3766 |
| Heavy Leather | – | 4234 | AHledger https://ahledger.com/items/4234-heavy-leather |
| Hillman's Leather Gloves | – | 4247 | Wowhead-Link in Kreislauf.csv (https://www.wowhead.com/forever/item=4247/hillmans-leather-gloves) |
| Light Armor Kit | – | 2304 | AHledger https://ahledger.com/items/2304-light-armor-kit |
| Strange Dust | Seltsamer Staub | 10940 | AHledger https://ahledger.com/items/10940-strange-dust |
| Lesser Magic Essence | Geringe Magieessenz | 10938 | AHledger https://ahledger.com/items/10938-lesser-magic-essence |
| Greater Magic Essence | Grosse Magieessenz | 10939 | AHledger https://ahledger.com/items/10939-greater-magic-essence |
| Lesser Astral Essence | – | 10998 | AHledger https://ahledger.com/items/10998-lesser-astral-essence |
| Greater Astral Essence | – | 11082 | AHledger https://ahledger.com/items/11082-greater-astral-essence |
| Soul Dust | – | 11083 | AHledger https://ahledger.com/items/11083-soul-dust |
| Small Glimmering Shard | – | 10978 | AHledger https://ahledger.com/items/10978-small-glimmering-shard |
| Large Glimmering Shard | – | 11084 | AHledger https://ahledger.com/items/11084-large-glimmering-shard |
| Copper Rod | – | 6217 | AHledger https://ahledger.com/items/6217-copper-rod |
| Silver Rod | – | 6338 | AHledger https://ahledger.com/items/6338-silver-rod |
| Shadowgem | – | 1210 | AHledger https://ahledger.com/items/1210-shadowgem |
| Mote of Magic | – | 247786 | AHledger https://ahledger.com/items/247786-mote-of-magic |
| Simple Wood | – | 4470 | AHledger https://ahledger.com/items/4470-simple-wood |
| Deviate Fish | – | 6522 | AHledger https://ahledger.com/items/6522-deviate-fish |

## 8. Annahmen und offene Punkte

- Eigener Bestand: untere Rate des Mengenmodells beim Wechsel (Abschnitt E1). Was der Zähler im Spiel zeigt, gilt.
- Herstellungen pro Abschnitt: wow-professions («These numbers are estimates»). Der letzte Abschnitt bis 155 ist bis 150 anteilig gezählt.
- Fehlende Fetzen: kaufen ist billiger als Light Armor Kits aus Leder, solange 3 × Fetzenpreis < 2 × Lederpreis (heute 75c gegen 1s).
- Entzaubern: Erwartungswert aus `Kreislauf.csv`; Greater Magic Essence zählt als 3 Lesser (wow-professions: Rechtsklick teilt sie).
- Verzaubern: pro Punkt das Rezept mit den geringsten Kaufkosten; eigenes Material kostet nichts. Ob man ein Zielteil (Armschiene, Brust, Umhang, Stiefel, Zweihänder) braucht, sagt keine Forever-Quelle ausdrücklich (wow-professions erwähnt im Makro einen «optional target slot»).
- Lehrer: LW-Geselle Karolek, VZ-Geselle Godan (Orgrimmar; wow-professions, Icy Veins). Kosten der Ränge laut wow-professions ohne Einheit («Journeyman 5», bei Karolek «450»); Kosten der Rezepte nicht gefunden. Das Testlog misst beides (GELERNT, GELD).
- Fangrate beim Angeln: 144 Fänge pro Stunde (Testlog 13.10., Stonebull Lake, Angeln 1–15). Im Brachland ungeprüft.
- Preise: Beta, Normal Horde US. Zum Start zählen die Preise des eigenen Realms (offene Entscheidung 4).

