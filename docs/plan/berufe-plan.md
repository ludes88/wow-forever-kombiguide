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
- Ab LW 80 bringt jedes Leichte Leder 2- bis 5-mal weniger Punkte als davor (Tabelle in Abschnitt 1). Mehr Leder zu farmen bringt 21–34 Silber pro Stunde Materialwert (Beta); Angeln ergäbe etwa 2g 64c pro Stunde nach 5 % Gebühr (nur Deviate Fish, Rate ungeprüft, Abschnitt 1).
- Lesser Magic Essence rechnet der Plan zum kleineren Preis: direkt oder ein Drittel einer Greater Magic Essence (1 → 3, gemessen 13.10.). «Jetzt»: direkt 69c, über Greater 65c; eigener Scan (2026-10-15 22:15, ? Horde R2d38 Beta): über Greater 50c, direkt 91c (Regel in Abschnitt 6).
- Einkauf (Beta-Preise «jetzt»): Stufe A 42s 63c, B 1g 76s, C 3g 29s 92c, D 7g 37s 76c. Derselbe Einkauf mit den 30-Tage-Medianen: A 71s 25c, B 5g 1s 12c, C 5g 29s 65c, D 9g 56s 16c.
- **Netto** heisst in diesem Bericht: Einkauf + Lehrer − was der Händler für verkaufte Teile zahlt (Lernkosten gemessen in Orgrimmar, `data/kombi/lehrer.csv`). Den Rest, der am Ende übrig bleibt, rechnet erst die nächste Zeile ab. Stufe A 42s 63c + Lehrer 17s 70c − Händler 0c = netto 60s 33c, Stufe B 1g 76s + Lehrer 6s − Händler 0c = netto 1g 82s, Stufe C 3g 29s 92c + Lehrer 30s − Händler 2g 14s 6c = netto 1g 45s 86c, Stufe D 7g 37s 76c + Lehrer 20s − Händler 0c = netto 7g 57s 76c. Zusammen netto 11g 45s 96c.
- Nach dem Verkauf des Rests im AH (Abschnitt 5, nach 5 % Gebühr 3g 16s 45c) kostet der ganze Plan etwa 8g 29s 51c (ohne Pfand; ob der Rest so abgeht, ist ungeprüft).
- Derselbe Plan mit den Medianen des letzten eigenen AH-Scans (2026-10-15 22:15, ? Horde R2d38 Beta; nur Vergleich, offene Entscheidung 17): A netto 59s 2c, B netto 1g 75s 10c, C netto 1g 54s 55c, D netto 7g 84s 64c, zusammen 11g 73s 31c.
- Verkaufen statt entzaubern (Preisregel, Abschnitt 6): Dark Leather Belt, Light Leather Pants gehen an den Händler, weil er mehr zahlt, als ihr Entzauberungs-Ertrag im AH kostet (Händlerpreise aus dem Forever-Client, Testlog 15.10.).
- Vorschlag (nicht im Guide, Abschnitt 9): VZ 10–109 mit Zauberstäben, die der Händler zurückkauft. Netto A–D zusammen 10g 56s 66c statt 11g 45s 96c.
- LW 130–150 rechnet der Plan mit dem Tab «ohne Heavy Hide» von wow-professions (billiger bei diesen Preisen, Vergleich in Abschnitt 4).
- Nach allen Stufen bleibt Entzauberungs-Material übrig, das VZ bis 150 nicht braucht (Wert im AH etwa 3g 33s 11c vor und 3g 16s 45c nach 5 % Gebühr, Abschnitt 5).

## 1. Sweetspot: wie viel eigenes Leder nach Orgrimmar

Lesart von Claude (Rückfrage an den Nutzer offen): «Break-even an Investment von leichtem Leder» heisst hier: eigenes Leder dort einsetzen, wo es viele Punkte bringt, und nur so viel sammeln, wie die Route ohnehin hergibt (plus das Grinden, das RXP selbst vorschlägt). Bei Beta-Preisen ist Kaufen billiger als zusätzliches Farmen (Rechnung unten); bei anderen Preisen kann das kippen.

| Material | LW 1–80 braucht | Route bis Orgrimmar (ohne S1) | mit S1 (untere–obere Rate) | im AH kaufen (mit S1, untere Rate) | Beta-Preis |
|---|---|---|---|---|---|
| Ruined Leather Scraps (Verdorbene Lederfetzen) | 99 | 76 | 83–87 | 16 | 25c |
| Light Leather (Leichtes Leder) | 62 (netto; 33 mehr entstehen aus den Fetzen) | 66 | 79–86 | 0 | 50c |
| Light Hide (Leichter Balg) | 27 | 4 | 5–6 | 22 | 69c |

Die 66 Leder ohne S1 setzen voraus, dass die 5 Plainstrider Kidneys (Quest 821) vor Orgrimmar fallen (Annahme in `modell_leder.csv`; RXP erinnert bis 12-17 #180 daran); ohne sie wären es etwa 60. Ist der Zähler beim Farm-Stopp S1 schon voll, ist S1 nur Zugabe.

Punkte pro Leichtem Leder und Kosten pro Punkt (Plan-Route). «zurück» = was aus den Herstellungen zurückkommt: beim Händler (Forever-Client), beim Entzaubern (Ertrag zum Kaufpreis, weil die Verzauberkunst ihn sonst kauft), als Material für später (Preis, ohne Preis zu den eigenen Kosten) oder im AH nach 5 % Gebühr. Netto negativ = Gewinn. Zwei Preisbasen: AHledger «jetzt» und der letzte eigene Scan (2026-10-15 22:15, ? Horde R2d38 Beta):

| Stufe | LW | Rezept | Herstellungen | Leichtes Leder | Punkte je Leder | Material (AH/Händler) | zurück | wie | netto je Punkt | netto je Punkt (eigener Scan) |
|---|---|---|---|---|---|---|---|---|---|---|
| A | 1–30 | Light Leather | 33 | 0 | – | 24s 75c | 16s 50c | Material für später | 28c | 7c |
| A | 30–55 | Cured Light Hide | 27 | 0 | – | 32s 13c | 32s 13c | Material für später (ohne Preis: zu Kosten) | 0c | 2c |
| A | 55–75 | Embossed Leather Gloves | 21 | 63 | 0.32 | 35s 70c | 23s 96c | entzaubert | 59c | 1s 17c |
| A | 75–80 | Medium Leather | 8 | 32 | 0.16 | 16s | 15s 28c | Material für später | 14c | 66c |
| B | 80–90 | Cured Medium Hide | 10 | 0 | – | 93s 80c | 93s 80c | Material für später (ohne Preis: zu Kosten) | 0c | −3s 55c |
| B | 90–100 | Fine Leather Belt | 19 | 114 | 0.09 | 60s 80c | 52s 78c | entzaubert, 10 behalten | 80c | 1s 85c |
| C | 100–115 | Light Leather Pants | 24 | 240 | 0.06 | 1g 44s | 1g 43s 76c | Händler | 2c | 3s 47c |
| C | 115–125 | Dark Leather Belt | 10 | 0 | – | 55s | 70s 30c | Händler | −1s 53c | 13s 42c |
| C | 125–130 | Heavy Leather | 7 | 0 | – | 66s 85c | 79s 67c | AH nach Gebühr | −2s 56c | 2s 51c |
| D | 130–150 | Hillman's Leather Gloves | 24 | 0 | – | 7g 37s 76c | 4g 75s 99c | entzaubert | 13s 9c | 9s 81c |

Zeit gegen Gold (Beta-Preise; Raten sind Annahmen, siehe Abschnitt 8):

- Grinden für Leder, Gegner Stufe 11–15: 21–34 Silber pro Stunde Materialwert bei 50–80 Häuten (30-Tage-Preise: 31–49). Dazu gibt es XP; RXP schlägt das Grinden auf Stufe 16 an der Sludge Fen ohnehin vor.
- Angeln an der Lushwater Oasis, nur Deviate Fish gerechnet: rund 47 pro Stunde bei der Fangrate vom Stonebull Lake ergibt 2g 11s 20c pro Stunde vor und 2g 64c nach 5 % Gebühr (Normal Horde US), bzw. 5g 15s 81c und 4g 90s 2c (PvP Horde US). Ungeprüft: Fangrate und nötige Angelfertigkeit im Brachland (keine Forever-Quelle).
- Folgerung (bei diesen Preisen, Fisch nach Gebühr): Grinden nur für Leder lohnt sich erst, wenn Leichtes Leder etwa 4s 18c–6s 69c kostet (heute 50c).

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
- VZ 20–50: 10× Enchant Bracer - Minor Deflect
- VZ 20–50: 20× Enchant Chest - Inferior Stamina

Einkauf im AH: 22 Light Hide, 16 Ruined Leather Scraps, 4 Lesser Magic Essence = 21s 79c (derselbe Einkauf mit den 30-Tage-Medianen: 50s 41c)
Einkauf beim Händler: 27 Salt, 42 Coarse Thread, 19 Mote of Magic, 1 Copper Rod = 20s 84c
Beim Lehrer: LW Lehrling 10c (Kamari), VZ Lehrling 10c (Godan), LW Geselle 5s (Karolek, ab 50), VZ Geselle 5s (Godan, ab 50), Cured Light Hide 50c (Kamari, ab 30), Embossed Leather Gloves 1s 50c (Kamari, ab 40), Medium Leather 5s (Karolek, ab 75), Enchant Chest - Inferior Stamina 50c (Godan, ab 15) = 17s 70c

### Stufe B: LW bis 100, VZ bis 100 (in Orgrimmar, wenn das Gold reicht, sonst in Thunder Bluff)

Herstellen (Lederverarbeitung):

- LW 80→90: 10× Cured Medium Hide — 10 Medium Hide, 10 Salt
- LW 90→100: 19× Fine Leather Belt — 114 Light Leather (davon 17 aus dem Vorrat), 38 Coarse Thread

Entzaubern: 9× Fine Leather Belt → erwartet 16.9 Strange Dust, 2.7 Greater Magic Essence, 0.4 Small Glimmering Shard. 10 Fine Leather Belt behalten (für Dark Leather Belt in Stufe C).

Verzaubern:

- VZ 50–70: 20× Enchant Bracer - Minor Deflect
- VZ 70–100: 33× Enchant Chest - Minor Absorption

Einkauf im AH: 10 Medium Hide, 98 Light Leather, 45 Lesser Magic Essence = 1g 67s 20c (derselbe Einkauf mit den 30-Tage-Medianen: 4g 92s 32c)
Einkauf beim Händler: 10 Salt, 38 Coarse Thread = 8s 80c
Beim Lehrer: Cured Medium Hide 2s (Karolek, ab 75), Fine Leather Belt 3s (Karolek, ab 55), Enchant Chest - Minor Absorption 1s (Godan, ab 40) = 6s

### Stufe C: LW bis 130, VZ bis 130 (in Thunder Bluff, Stufe 20)

Herstellen (Lederverarbeitung):

- LW 100→115: 24× Light Leather Pants — 240 Light Leather, 24 Cured Light Hide (davon 24 aus dem Vorrat), 24 Fine Thread
- LW 115→125: 10× Dark Leather Belt — 10 Fine Leather Belt (davon 10 aus dem Vorrat), 10 Cured Medium Hide (davon 10 aus dem Vorrat), 20 Fine Thread, 10 Gray Dye
- LW 125→130: 7× Heavy Leather — 35 Medium Leather (davon 8 aus dem Vorrat)

Beim Händler verkaufen (statt entzaubern): 24× Light Leather Pants zu je 5s 99c = 1g 43s 76c, 10× Dark Leather Belt zu je 7s 3c = 70s 30c

Verzaubern:

- VZ 100–109: 9× Enchant Cloak - Minor Protection
- VZ 109–110: 1× Runed Silver Rod
- VZ 110–130: 32× Enchant Cloak - Minor Protection

Einkauf im AH: 240 Light Leather, 65 Strange Dust, 27 Medium Leather, 1 Silver Rod, 1 Shadowgem, 4 Lesser Magic Essence = 2g 50s 92c (derselbe Einkauf mit den 30-Tage-Medianen: 4g 50s 65c)
Einkauf beim Händler: 44 Fine Thread, 10 Gray Dye = 79s
Beim Lehrer: Light Leather Pants 4s (Karolek, ab 70), Dark Leather Belt 4s (Karolek, ab 100), Heavy Leather 10s (Karolek, ab 125), Enchant Cloak - Minor Protection 2s (Godan, ab 70), Runed Silver Rod 10s (Godan, ab 100) = 30s

### Stufe D: LW bis 150, VZ bis 150 (in Thunder Bluff, der teure Rest bis 150)

Herstellen (Lederverarbeitung):

- LW 130→150: 24× Hillman's Leather Gloves — 336 Medium Leather, 96 Fine Thread

Entzaubern: 24× Hillman's Leather Gloves → erwartet 7.2 Greater Astral Essence, 27.0 Soul Dust, 1.0 Large Glimmering Shard

Verzaubern:

- VZ 130–150: 20× Enchant Bracer - Lesser Stamina

Ohne eigenen Soul Dust (Stufe D nicht gemacht oder zu wenige Hillman's Leather Gloves entzaubert): VZ 130–150 mit 20× Enchant Boots - Minor Stamina (80 Strange Dust, Lehrer 14s) kostet «jetzt» 81s 20c, mit gekauftem Soul Dust (20× Enchant Bracer - Lesser Stamina, Lehrer 15s) 1g 59s 20c; mit dem eigenen Scan 66s gegen 1g 95s. Stiefel: 4 Strange Dust je Verzauberung laut wow-professions (Tab Strange Dust, im Spiel ungeprüft), lernbar ab VZ 125 (Lehrerliste Godan, Orgrimmar); ob Teg Dawnstrider in Thunder Bluff sie führt, ist ungeprüft.

Einkauf im AH: 336 Medium Leather = 6g 41s 76c (derselbe Einkauf mit den 30-Tage-Medianen: 8g 60s 16c)
Einkauf beim Händler: 96 Fine Thread = 96s
Beim Lehrer: Hillman's Leather Gloves 5s (Karolek, ab 120), Enchant Bracer - Lesser Stamina 15s (Godan, ab 130) = 20s

## 3. Lernstufen: wo die Route früher ist als die Lehrer

wow-professions nutzt diese Rezepte früher, als sie lernbar sind: zuerst die Lehrerlisten aus Orgrimmar (gemessen 15.10., `data/kombi/lehrer.csv`), sonst AHledger («orange» = lernbar ab). Der Plan rechnet pro Punkt nur mit Rezepten, die schon gehen (Abschnitt 2); der Guide nennt einen Ausweg.

| Beruf | Rezept | wow-professions ab | lernbar ab | Quelle |
|---|---|---|---|---|
| VZ | Enchant Bracer - Minor Deflect | 20 | 40 | AHledger Rezeptseite 7428 (ahledger.com/wow-forever/recipes, Recherche 14.10.) · SeeMeta 80/100/120 · Widerspruch: wow-professions nutzt es ab 20 (AHledger, nicht in den Lehrerlisten) |

Gemessen in Orgrimmar (15.10.): Enchant Chest - Inferior Stamina ab VZ 15 (wow-professions: 20, AHledger: 30); Enchant Bracer - Minor Deflect steht bei Jhag und Godan nicht in der Liste, laut SeeMeta kommt es mit dem Rang (https://seemeta.com/en/wow-forever/professions/enchanting, Stand 14.10.2026; im Spiel ungeprüft). Der Guide nimmt dafür Enchant Chest - Minor Absorption (ab VZ 40, gleiches Material).

## 4. LW 130–150: Tab «Cured Heavy Hide» oder «ohne Heavy Hide»

wow-professions: «If 20x Heavy Hide cost less than around 120x Heavy Leather, 140x Medium Leather and 17x Moss Agate» → Tab «Cured Heavy Hide», sonst «Leveling without Heavy Hide». Die Regel denkt bis 175; hier zählt nur bis 150.

| Tab | Einkauf A–D (jetzt) | Händler zahlt für Teile | Rückverkauf Rest (nach Gebühr) | Saldo (ohne Lehrer) |
|---|---|---|---|---|
| Cured Heavy Hide | 17g 34s 21c | 2g 14s 6c | 1g 57s 15c | 13g 63s |
| ohne Heavy Hide | 12g 86s 32c | 2g 14s 6c | 3g 16s 45c | 7g 55s 81c |

Der Plan nimmt «ohne Heavy Hide». Bei anderen Preisen zum Start kann es kippen: neu rechnen.

## 5. Verkaufen im AH

Was nach Stufe D übrig bleibt (Erwartungswert) und nicht für VZ bis 150 gebraucht wird. Ob man es für LW oder VZ über 150 behält, entscheidest du.

| Material | Menge | Wert (jetzt) | nach 5 % Gebühr | Wert (30 Tage) |
|---|---|---|---|---|
| Greater Astral Essence | 7.2 | 2g 5s 49c | 1g 95s 21c | 2g 64s 24c |
| Large Glimmering Shard | 1.0 | 75s 83c | 72s 4c | 1g 7s 17c |
| Soul Dust | 7.0 | 50s 47c | 47s 95c | 59s 71c |
| Small Glimmering Shard (Kleiner gleißender Splitter) | 0.4 | 1s 32c | 1s 25c | 1s 26c |

Zusammen 3g 33s 11c vor und 3g 16s 45c nach Gebühr (ohne Pfand). Dazu kommt, was die Lederverarbeitung übrig lässt (nächste Zeile).

Dazu aus der Lederverarbeitung: 3 Cured Light Hide, 7 Heavy Leather. Heavy Leather braucht wow-professions erst ab LW 155.

Produkte der Verzauberkunst (Zauberstäbe): Der Forever-Client zahlt beim Händler 1s 10c für den Geringen und 2s für den Grossen Magiezauberstab (Gegenstands-Infos, Testlog 15.10.; der Verkauf von 11 grossen für 22s am 14.10. passt dazu). Eine Patch-Notiz vom 01.10. nannte 1c (Widerspruch 21). Der Plan rechnet nur in der Variante von Abschnitt 9 damit; zum Start neu prüfen.

## 6. Preisregeln (Break-even)

Wann sich eine Wahl umdreht. Spalten: Wert mit den Beta-Preisen «jetzt» und mit den 30-Tage-Medianen (AHledger, Normal Horde US); der Plan oben rechnet mit «jetzt». Zum Start mit den eigenen Preisen prüfen.

| Wahl | Regel | jetzt | 30 Tage |
|---|---|---|---|
| Fehlende Fetzen | kaufen, wenn 3 Fetzen weniger kosten als 2 Leichtes Leder; sonst Light Armor Kit (1 Leder) | 75c gegen 1s: Fetzen kaufen | 84c gegen 1s 58c: Fetzen kaufen |
| Extra Embossed Leather Gloves nur zum Entzaubern | lohnt, wenn 1,125 Strange Dust und 0,3 Lesser Magic Essence (Ertrag) mehr wert sind als 3 Leichtes Leder und 2 Coarse Thread | 1s 70c gegen 1s 14c: lohnt nicht, Staub kaufen | 2s 57c gegen 4s 88c: lohnt |
| VZ 20–70 und 100–109 | 1 Strange Dust oder 1 Lesser Magic Essence pro Punkt: das billigere | 65c gegen 84c: Essenz | 7s 19c gegen 2s 42c: Staub |
| VZ 70–100 | Essenz (33 für 30 Punkte) lohnt, solange sie weniger als 1,82 Strange Dust kostet | 65c gegen 1s 53c: Essenz (Chest - Minor Absorption) | 7s 19c gegen 4s 40c: Staub (Bracer - Minor Stamina) |
| VZ 110–130 | Essenz (80, dazu Formel 5s) statt 64 Strange Dust lohnt unter etwa 0,8 Strange Dust pro Essenz | 57s 27c gegen 53s 76c: Staub (Cloak - Minor Protection) | 5g 80s 47c gegen 1g 54s 88c: Staub (Cloak - Minor Protection) |
| VZ 130–150 | Soul Dust (20) statt 80 Strange Dust lohnt unter 4 Strange Dust pro Soul Dust; eigener Soul Dust aus Hillman's zählt 0 | 1g 44s 20c gegen 67s 20c: Staub kaufen | 1g 70s 60c gegen 1g 93s 60c: Soul Dust kaufen |
| LW 130–150 | Tab «Cured Heavy Hide» (20 Heavy Hide, 60 Salt, 14 Hillman's) statt «ohne Heavy Hide» (24 Hillman's), ohne Entzaubern gerechnet | 11g 68s 36c gegen 7g 37s 76c: ohne Heavy Hide | 25g 22s 76c gegen 9g 56s 16c: ohne Heavy Hide |
| Light Leather Pants: Händler statt Entzaubern | Händler zahlt 5s 99c (Forever-Client); lohnt, solange der Ertrag (1,875 Strange Dust, 0,3 Greater Magic Essence, 0,04 Splitter) weniger wert ist | 2s 31c gegen 5s 99c: Händler | 11s 15c gegen 5s 99c: entzaubern |
| Dark Leather Belt: Händler statt Entzaubern | Händler zahlt 7s 3c (Forever-Client); lohnt, solange 3,75 Strange Dust, 0,3 Lesser Astral Essence und 0,04 Splitter weniger wert sind | 5s 11c gegen 7s 3c: Händler | 12s 4c gegen 7s 3c: entzaubern |
| VZ 10–75: Geringer Magiezauberstab | statt des Plan-Wegs (1 Strange Dust pro Punkt, ab VZ 40 auch 1 Lesser Magic Essence: das billigere): 1 Simple Wood und 1 Lesser Magic Essence, der Händler zahlt den Stab zurück | −7c gegen 65c: Zauberstab | 6s 47c gegen 2s 42c: Plan-Weg |
| VZ 70–110: Grosser Magiezauberstab | statt des Plan-Wegs (pro Punkt 1,1 Lesser Magic Essence mit Chest - Minor Absorption oder 2 Strange Dust mit Bracer - Minor Stamina: das billigere): 1 Simple Wood und 2 Lesser Magic Essence, der Händler zahlt den Stab zurück | −31c gegen 72c: Zauberstab | 12s 77c gegen 4s 84c: Plan-Weg |
| Lesser Magic Essence: direkt oder über Greater | Greater Magic Essence kaufen und teilen (1 → 3), wenn sie weniger als 3 Lesser kostet (gemessen 13.10.: aus 9 wurden 27) | 65c gegen 69c: Greater kaufen und teilen | 7s 19c gegen 7s 35c: Greater kaufen und teilen |
| Leder grinden statt angeln | Grinden (50–80 Häute pro Stunde, Gegner 11–15) bringt mehr als Angeln (nur Deviate Fish nach 5 % Gebühr, Rate ungeprüft) | 21s 10c–33s 76c gegen 2g 64c pro Stunde: Angeln | 30s 55c–48s 88c gegen 1g 86s 82c pro Stunde: Angeln |

## 7. Gegenstände im Guide (Item-IDs)

| Gegenstand | deutsch (Testlog) | ID | Quelle |
|---|---|---|---|
| Light Leather | Leichtes Leder | 2318 | AHledger https://ahledger.com/items/2318-light-leather |
| Ruined Leather Scraps | Verdorbene Lederfetzen | 2934 | AHledger https://ahledger.com/items/2934-ruined-leather-scraps |
| Medium Leather | Mittleres Leder | 2319 | AHledger https://ahledger.com/items/2319-medium-leather |
| Light Hide | Leichter Balg | 783 | AHledger https://ahledger.com/items/783-light-hide |
| Medium Hide | Mittlerer Balg | 4232 | AHledger https://ahledger.com/items/4232-medium-hide |
| Heavy Hide | – | 4235 | AHledger https://ahledger.com/items/4235-heavy-hide |
| Salt | Salz | 4289 | AHledger https://ahledger.com/items/4289-salt |
| Coarse Thread | Grober Faden | 2320 | AHledger https://ahledger.com/items/2320-coarse-thread |
| Fine Thread | Feiner Faden | 2321 | AHledger https://ahledger.com/items/2321-fine-thread |
| Gray Dye | Grauer Farbstoff | 4340 | AHledger https://ahledger.com/items/4340-gray-dye |
| Cured Light Hide | Geschmeidiger leichter Balg | 4231 | AHledger https://ahledger.com/items/4231-cured-light-hide |
| Cured Medium Hide | Geschmeidiger mittlerer Balg | 4233 | AHledger, Ergebnis-Link der Rezeptseite 3817 (Recherche 14.10.) |
| Embossed Leather Gloves | Geprägte Lederhandschuhe | 4239 | Wowhead-Link in data/rechnung/Kreislauf.csv · AHledger, Ergebnis-Link der Rezeptseite 3756 |
| Fine Leather Belt | Feiner Ledergürtel | 4246 | Wowhead-Link in Kreislauf.csv · AHledger Rezeptseite 3763 |
| Light Leather Pants | Leichte Lederhose | 7282 | Wowhead-Link in Kreislauf.csv · AHledger Rezeptseite 9068 |
| Dark Leather Belt | Dunkler Ledergürtel | 4249 | Wowhead-Link in Kreislauf.csv · AHledger Rezeptseite 3766 |
| Heavy Leather | Schweres Leder | 4234 | AHledger https://ahledger.com/items/4234-heavy-leather |
| Hillman's Leather Gloves | Lederhandschuhe des Hügelwächters | 4247 | Wowhead-Link in Kreislauf.csv (https://www.wowhead.com/forever/item=4247/hillmans-leather-gloves) |
| Light Armor Kit | Leichtes Rüstungsset | 2304 | AHledger https://ahledger.com/items/2304-light-armor-kit |
| Strange Dust | Seltsamer Staub | 10940 | AHledger https://ahledger.com/items/10940-strange-dust |
| Lesser Magic Essence | Geringe Magieessenz | 10938 | AHledger https://ahledger.com/items/10938-lesser-magic-essence |
| Greater Magic Essence | Grosse Magieessenz | 10939 | AHledger https://ahledger.com/items/10939-greater-magic-essence |
| Lesser Astral Essence | – | 10998 | AHledger https://ahledger.com/items/10998-lesser-astral-essence |
| Greater Astral Essence | – | 11082 | AHledger https://ahledger.com/items/11082-greater-astral-essence |
| Soul Dust | – | 11083 | AHledger https://ahledger.com/items/11083-soul-dust |
| Small Glimmering Shard | Kleiner gleißender Splitter | 10978 | AHledger https://ahledger.com/items/10978-small-glimmering-shard |
| Large Glimmering Shard | – | 11084 | AHledger https://ahledger.com/items/11084-large-glimmering-shard |
| Copper Rod | Kupferrute | 6217 | AHledger https://ahledger.com/items/6217-copper-rod |
| Silver Rod | Silberrute | 6338 | AHledger https://ahledger.com/items/6338-silver-rod |
| Shadowgem | Schattenedelstein | 1210 | AHledger https://ahledger.com/items/1210-shadowgem |
| Mote of Magic | Magiepartikel | 247786 | AHledger https://ahledger.com/items/247786-mote-of-magic |
| Simple Wood | Einfaches Holz | 4470 | AHledger https://ahledger.com/items/4470-simple-wood |
| Deviate Fish | – | 6522 | AHledger https://ahledger.com/items/6522-deviate-fish |
| Lesser Magic Wand | Geringer Magiezauberstab | 11287 | AHledger https://ahledger.com/items/11287-lesser-magic-wand · Testlog 15.10. (REZEPTE 14293, Gegenstands-Infos) |
| Greater Magic Wand | Grosser Magiezauberstab | 11288 | AHledger https://ahledger.com/items/11288-greater-magic-wand · Testlog 15.10. (REZEPTE 14807, Gegenstands-Infos) |

## 8. Annahmen und offene Punkte

- Eigener Bestand: untere Rate des Mengenmodells beim Wechsel (Abschnitt E1 des Mengenmodells, `docs/plan/mengen-leder.md`). Was der Zähler im Spiel zeigt, gilt.
- Häute pro Stunde beim Grinden: 50–80 (Annahme aus `tools/plan_mengen.py`, keine Quelle für Stufe 12–20; gemessen in Mulgore rund 97 pro Stunde, Charakter Stufe 6–7, Testlog 13.10.).
- Herstellungen pro Abschnitt: wow-professions («These numbers are estimates»). Der letzte Abschnitt bis 155 ist bis 150 anteilig gezählt.
- Fehlende Fetzen: kaufen ist billiger als Light Armor Kits aus Leder, solange 3 × Fetzenpreis < 2 × Lederpreis (heute 75c gegen 1s).
- Entzaubern: Erwartungswert aus `Kreislauf.csv`; Greater Magic Essence zählt als 3 Lesser (wow-professions: Rechtsklick teilt sie). Gekauft wird die Lesser zum kleineren Preis: direkt oder ein Drittel der Greater (gemessen 13.10.: aus 9 wurden 27).
- Verzaubern: pro Punkt das Rezept mit den geringsten Kaufkosten; eigenes Material kostet nichts. Ob man ein Zielteil (Armschiene, Brust, Umhang, Stiefel, Zweihänder) braucht, sagt keine Forever-Quelle ausdrücklich (wow-professions erwähnt im Makro einen «optional target slot»).
- Lehrer: Lernstufen und Kosten gemessen bei Kamari, Karolek, Jhag und Godan (Orgrimmar, Testlog 15.10., `data/kombi/lehrer.csv`): Lehrling 10c, Geselle 5s (ab Stufe 10 und Fertigkeit 50), Rezepte 50c bis 25s. Lehrer in Thunder Bluff nicht gemessen. Rezepte ohne Eintrag in der Liste (Light Leather, Light Armor Kit, Runed Copper Rod, Bracer - Inferior Stamina, Bracer - Minor Deflect) zählen mit 0; laut SeeMeta kommt Minor Deflect mit dem Rang (https://seemeta.com/en/wow-forever/professions/enchanting, Stand 14.10.2026), im Spiel ungeprüft.
- Händler zahlt (Verkauf der Teile): Forever-Client (`data/preise/haendler_ankauf.csv`, Testlog 15.10.); für Teile ohne Messung AHledger (Spalte «Händlerpreis (s)» in `Kreislauf.csv`), im Spiel ungeprüft. Viele hergestellte Teile zahlt der Forever-Händler niedriger als Classic (z. B. Grosser Magiezauberstab 2s statt 15s 35c, Geprägte Lederhandschuhe 71c statt 1s 19c; Vergleich in `docs/recherche/2026-10-15_haendlerpreise.md`).
- Fangrate beim Angeln: 134 Fänge pro Stunde (Testlog 13.10., Stonebull Lake, Angeln 1–15: 14 Fänge, 13 Abstände in 349 s). Im Brachland ungeprüft.
- Preise: Beta, Normal Horde US. Zum Start zählen die Preise des eigenen Realms (offene Entscheidung 4).

## 9. Variante: Verzauberkunst mit Zauberstäben (Vorschlag von Claude, nicht im Guide)

Idee: Der Geringe Magiezauberstab (ab VZ 10, 50c beim Lehrer) ist laut SeeMeta bis VZ 75 orange, der Grosse (ab VZ 70, 2s) bis 110 (https://seemeta.com/en/wow-forever/professions/enchanting, Stand 14.10.2026; bei VZ 100 im Testlog 15.10. bestätigt: Geringer grün, Grosser orange). Orange heisst: jede Herstellung gibt einen Punkt. Der Händler kauft die Stäbe zurück (Forever-Client: 1s 10c bzw. 2s). Gleiche Lederverarbeitung wie oben; die Verzauberkunst nimmt pro Punkt das Billigste, Zauberstäbe eingeschlossen.

| Stufe | Einkauf | Lehrer | Händler zurück | netto | ohne Zauberstäbe netto |
|---|---|---|---|---|---|
| A | 76s 43c | 17s 70c | 44s | 50s 13c | 60s 33c |
| B | 2g 12s 64c | 7s | 82s | 1g 37s 64c | 1g 82s |
| C | 3g 13s 18c | 30s | 2g 32s 6c | 1g 11s 12c | 1g 45s 86c |
| D | 7g 37s 76c | 20s | 0c | 7g 57s 76c | 7g 57s 76c |

Verzaubern in der Variante:

- Stufe A: VZ 1–2 1× Runed Copper Rod, VZ 2–20 8× Enchant Bracer - Inferior Stamina, VZ 2–20 10× Lesser Magic Wand, VZ 20–50 30× Lesser Magic Wand
- Stufe B: VZ 50–70 20× Lesser Magic Wand, VZ 70–100 30× Greater Magic Wand
- Stufe C: VZ 100–109 9× Greater Magic Wand, VZ 109–110 1× Runed Silver Rod, VZ 110–130 32× Enchant Cloak - Minor Protection
- Stufe D: VZ 130–150 20× Enchant Bracer - Lesser Stamina

Was dafür spricht und was offen ist:

- Mit den Medianen des eigenen Scans (2026-10-15 22:15, ? Horde R2d38 Beta; Lesser Magic Essence 50c über die Greater, direkt 91c; Strange Dust 65c; Simple Wood 38c beim Händler) kostet ein Punkt mit dem Geringen Stab netto −22c statt 50c auf dem Plan-Weg, mit dem Grossen −62c statt 55c (negativ = Gewinn; Regeln in Abschnitt 6).
- Offen: ob die Farben in Forever so laufen (SeeMeta, nur bei VZ 100 geprüft; das Testlog schreibt jeden Farbwechsel), ob der Händlerpreis zum Start bleibt (Widerspruch 21) und ob der Markt die nötigen Essenzen hat (im letzten Scan etwa 6795 Lesser Magic Essence, jede Greater als 3 gezählt).
- Entscheid beim Nutzer (offener Punkt 28; dazu Punkt 7: woher das Material für Verzauberkunst kommt).

