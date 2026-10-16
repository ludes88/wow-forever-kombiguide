# Goldquellen entlang der Route (Recherche 14.10.2026)

Frage des Nutzers: «Gibt es einen noch besseren Plan, an genügend Gold zu kommen?» Hier stehen die Kandidaten mit Zahlen und Quellen. Die Entscheidung liegt beim Nutzer.

**Korrektur vom 15.10. (Prüfbericht A3) und 16.10.:** Die Fangrate vom Stonebull Lake ist 134 Fänge pro Stunde, nicht 144 (14 Fänge sind 13 Abstände in 349 s). Alle Angelwerte hier (Gold pro Stunde, Spalte «Angeln netto pro Stunde») sind darum rund 7 % zu hoch, die Break-even-Werte für Kräuter ebenso: etwa 13–14 statt 14–15 Knoten pro Stunde (NH jetzt) und 18–20 statt 19–22 (NH 30 Tage). Neu gerechnet: Angeln NH 2g 11s 20c vor und 2g 0s 64c nach 5 % Gebühr, PH 5g 15s 81c bzw. 4g 90s 2c (`docs/plan/berufe-plan.md` §1). Der Text unten bleibt, wie er am 14.10. war.

**Was die Zahlen bedeuten**
- Preise: AHledger, Forever-Beta, US-Märkte. NH = Normal Horde US, PH = PvP Horde US. 30T = Median über 30 Tage.
- «netto» heisst: nach 5 % AH-Gebühr (AHledger, Seite «Auction House»).
- AHledger-Rezeptseiten tragen kein Datum. Sie zeigen die «latest medians» zum Abruf am 14.10.
- Zum Start zählen die Preise des eigenen Realms (offene Entscheidung 4). Beta-Preise taugen nur als Grössenordnung (Risiko 20 und 22).

## Quellen

**Kräuter und Frilled Lichen**
- AHledger, Item Frilled Lichen (249399), Scan 2026-10-14 18:55 UTC: https://ahledger.com/items/249399-frilled-lichen
- AHledger, Zone The Barrens (Kräuter, Angelstelle, Händler): https://ahledger.com/wow-forever/zones/the-barrens
- AHledger, Gold-Meta (Ausgabe 13.10.2026): https://ahledger.com/guides/gold/meta
- AHledger, Rezeptseiten mit Kräuterpreisen (ohne Datum):
  - Lesser Troll's Blood Elixir: https://ahledger.com/wow-forever/recipes/3176-lesser-trolls-blood-elixir
  - Greater Discolored Healing Potion: https://ahledger.com/wow-forever/recipes/1244647-greater-discolored-healing-potion
  - Lesser Mageblood Elixir: https://ahledger.com/wow-forever/recipes/1250789-lesser-mageblood-elixir
  - Cerulean Dye: https://ahledger.com/wow-forever/recipes/1249630-cerulean-dye
- AHledger, Item Bruiseweed (2453), Scan 2026-10-12 17:55 UTC: https://ahledger.com/items/2453-bruiseweed
- Icy Veins:
  - Herbalism (11.10.2026): https://www.icy-veins.com/wow-forever/herbalism
  - Scarce-Material (29.09.2026): https://www.icy-veins.com/wow-forever/news/every-gathering-node-in-wow-forever-can-drop-a-scarce-material-youll-want/
- foreverchanges, Herbalism («Updated on October 8»), mit dem Legacy-Bonus «Bountiful Harvest»: https://foreverchanges.pro/professions/herbalism
- Spielerberichte auf kommerziellen Seiten:
  - mmonster (13.10.2026): https://mmonster.co/wow-forever/guides/gold
  - KingBoost (24.09.2026): https://kingboost.net/blogs/wow-forever/wow-forever-herbalism-guide-and-recipes/
- Vorbefund vom 13.10. mit AHledger-Links: `docs/recherche/2026-10-13_kraeuter-fische-kochen.md`

**Angeln**
- AHledger, Item Deviate Fish (6522), Scan 2026-10-13 23:15 UTC: https://ahledger.com/items/6522-deviate-fish
- Koordinaten: RestedXP v4.11.23, `Guides/forever/Horde-12-22_Barrens.lua`, Zeilen 1550, 2540, 2835 und 2855–2889 (https://github.com/RestedXP/RXPGuides). Umgerechnet mit `data/karten/forever_karten.csv` (Karte 1413, exakt).
- Nötige Angelfertigkeit, Forever:
  - Icy Veins Fishing (11.10.): https://www.icy-veins.com/wow-forever/fishing
  - realmfirst (24.09.): https://realmfirst.net/world-of-warcraft-forever/professions/fishing/
  - classicwowforever (03.10.): https://classicwowforever.com/professions/fishing/
- Nötige Angelfertigkeit, Classic-Daten:
  - wowforever.be (11.10.): https://wowforever.be/tradeskills/forever/fishing/
  - foreverchanges: https://foreverchanges.pro/professions/fishing
  - Wowhead Classic (05.01.2025): https://www.wowhead.com/classic/cn/guide/best-fishing-pools-farming-locations-classic-wow
  - Warcraft Tavern: https://warcrafttavern.com/wow-classic/guides/deviate-fish
  - wowseer: https://wowseer.gg/items/Deviate_Fish_6522
- Fangrate: Testlog 13.10. (Stonebull Lake, `docs/tests/testlauf-3.md`)

**Lederverarbeitung und Verzauberkunst**
- AHledger:
  - Übersicht LW: https://ahledger.com/wow-forever/professions/leatherworking
  - Übersicht VZ: https://ahledger.com/wow-forever/professions/enchanting
  - Crafting PvP Horde US: https://ahledger.com/crafting?market=forever/pvp/horde/us
- AHledger, Rezeptseiten (Abruf 14.10., «Value» = Median × Ausbeute − 5 %):
  - mit bekannter Adresse:
    - https://ahledger.com/wow-forever/recipes/23399-barbaric-bracers
    - https://ahledger.com/wow-forever/recipes/1301537-azure-gustwoven-spaulders
    - https://ahledger.com/wow-forever/recipes/1263056-arcane-salvager
  - Adresse ohne Namensteil, als Nummer unter ahledger.com/wow-forever/recipes: 2165, 1255124, 1255123, 3780, 1255095, 3816, 3817, 20648, 20649, 1302604, 5244, 2163, 14293, 14807, 25124
- AHledger, NPC Tamar: https://ahledger.com/wow-forever/npcs/3366-tamar
- AHledger, «Professions in Forever» (01.10.2026): https://ahledger.com/guides/professions-in-forever
- Warcraft Tavern, Level-30-Update (Zauberstäbe für 1c beim Händler, 01.10.2026): https://www.warcrafttavern.com/forever/news/level-30-content-is-now-available-in-the-wow-forever-beta/
- Wahrscheinlichkeit für einen Punkt beim Herstellen:
  - Wowpedia «Profession»: https://wowpedia.fandom.com/wiki/Profession
  - warcraft.wiki.gg «Skill up»: https://warcraft.wiki.gg/wiki/Skill_up
  - RankedBoost: https://rankedboost.com/world-of-warcraft/forever/professions/

**Gold pro Stunde**
- Ohne Methode; die Seiten werben für einen Goldverkäufer:
  - https://www.wowforever.games/365.html
  - https://www.wowforever.games/721.html
  - https://www.wowforever.games/392.html
- Ausdrücklich ohne Zahlen:
  - LepreStore: https://leprestore.com/guides/world-of-warcraft-forever/wow-forever-gold-farming-guide/
  - Overgear: https://overgear.com/guides/wow-forever/earning-gold/

## 1. Ergebnis in Kürze

- **Kräuterkunde mit Frilled Lichen** ist der Kandidat mit dem grössten Hebel, aber auch der unsicherste. AHledger misst Frilled Lichen aus Briarthorn im Südbrachland in 16 % von 51 Beutefenstern, also etwa 8 Funde. Damit ist ein Briarthorn-Knoten netto etwa 14–15s wert (NH, jetzt); ein Deviate Fish bringt 4s 27c. Kräutersammeln schlägt das Angeln, sobald man mehr als etwa 14–15 Knoten pro Stunde schafft. Mit den 30-Tage-Preisen braucht es 19–22 Knoten pro Stunde. Wie viele Knoten pro Stunde gehen, sagt keine Quelle (Abschnitt 2, Messung M4).
- **Angeln** (Deviate Fish an der Lushwater Oasis) bringt bei der Fangrate vom Stonebull Lake netto etwa 2g 16s pro Stunde (NH) bzw. 5g 28s (PH). Ob die Rate im Brachland gilt und welche Fertigkeit es dort braucht, sagt keine Forever-Quelle (Abschnitt 3, Messung M3).
- **LW-Erzeugnisse mit Gewinn** gibt es (Abschnitt 4). Die meisten haben aber kleinen Absatz, oder ihre Musterquelle ist ungeklärt. Zwei Kandidaten für den Plan:
  - Stufe B mit Medium Armor Kit und Mystic Medium Armor Kit statt Cured Medium Hide und Fine Leather Belt. Das ist grob 58s günstiger (NH, jetzt).
  - Ab LW 130 Erzeugnisse verkaufen statt Hillman's Leather Gloves entzaubern. Für diese Rezepte fehlen Farbstufen und NH-Preise.
- **Korrektur:** Heavy Leather bringt auf der AHledger-Rezeptseite keinen Gewinn: NH −2s 51c, PH −96c. Der Plan rechnet mit dem älteren Preis 11s 98c (Item-Seite 08.10.) und zeigt deshalb Gewinn (`berufe-plan.md` §1, Stufe C). Bei 7 Stück geht es um rund 36s.
- **Gold pro Stunde im Netz:** Es gibt nur unbelegte Zahlen von Werbeseiten. Seriöse Seiten nennen ausdrücklich keine.

## 2. Kräuter und Frilled Lichen

**Fakten**
- Frilled Lichen (249399), «New in WoW Forever», Trade Goods/Herb. Einziges Rezept bei AHledger: Cerulean Dye (Alchemie 10), dafür braucht es 2 Frilled Lichen (Item- und Rezeptseite). Icy Veins (29.09.) nennt zusätzlich Enchant Weapon - Insight und Schneiderei ab 260; das ist ein Widerspruch.
- Wo AHledger Frilled Lichen gesehen hat, als Anteil der Beutefenster:
  - Briarthorn, Südbrachland: 16 % von 51
  - Earthroot, Durotar (Thunder Ridge): 15 % von 39
  - Kingsblood, Duskwood: 15 % von 20
  - Earthroot, Redridge: 4 % von 193 und 10 % von 79
  - Brachland laut Zonenseite: aus Briarthorn, Earthroot und Mageroyal (alle Südbrachland), zusammen 14× gesehen
- Spielerbericht: Frilled Lichen falle «mostly for low characters or low skill». mmonster schreibt selbst dazu, das sei «a player report, not a Blizzard statement».
- Legacy-Bonus «Bountiful Harvest»: «20 / 40 / 60 / 80 / 100%» mehr Scarce-Material (foreverchanges). Er verändert die Rate; bei Messungen deshalb notieren, ob und welcher Rang aktiv ist.
- Fertigkeit: Briarthorn ab 70, Mageroyal ab 50, Earthroot ab 15 (Icy Veins).
- Briarthorn im Brachland laut AHledger: «Southern Barrens» und «Lushwater Oasis». Koordinaten oder Knotenzahlen: nicht gefunden.
- Zusatzbeute aus Briarthorn: Swiftthistle in 33 % von 51 Beutefenstern (Vorbefund 13.10.).

**Preise** (Frilled Lichen: Item-Seite, Scan 14.10. 18:55 UTC)

| Markt | Median | 30 Tage | Angebote | Verkauf pro Tag |
|---|---|---|---|---|
| NH | 82s 80c | 49s 34c | 220 | nicht angegeben |
| PH | 2g 15s | 79s 29c | 192 | nicht angegeben |
| NA | 74s 49c | 51s 11c | 254 | etwa 550 |

- Briarthorn:
  - NH: 1s 34c (Item-Seite 12.10.) oder 2s 59c (Rezeptseite 3176, ohne Datum)
  - PH: 5s mit etwa 3'700 Verkäufen pro Tag (Gold-Meta 13.10.) oder 1s 25c (Item-Seite 12.10.)
- Swiftthistle: NH 2s 10c (Vorbefund 13.10.), PH 12s (Gold-Meta 13.10.)

**Wert eines Briarthorn-Knotens und Vergleich mit Angeln**

Die Rechnung nimmt pro Knoten 1 Briarthorn an. Wie viele Kräuter ein Knoten in Forever gibt, ist ungeprüft; mehr Kräuter pro Knoten erhöhen den Wert. Dazu kommt Frilled Lichen mit seiner Rate und Swiftthistle in 33 %. Alles netto.

Die Rate 16 % beruht auf etwa 8 Funden. Das 95-%-Intervall nach Wilson reicht von 8 % bis 28 %. Die Tabelle zeigt deshalb drei Raten.

| Preise | Frilled-Lichen-Rate | Knoten netto | Angeln netto pro Stunde | Break-even (Knoten pro Stunde) |
|---|---|---|---|---|
| NH jetzt | 8 % / 16 % / 28 % | 8–10s / 14–15s / 24–25s | 2g 16s | 23–26 / 14–15 / 9 |
| NH 30 Tage | 8 % / 16 % / 28 % | 6–7s / 9–10s / 15–16s | 2g 1s | 29–35 / 19–22 / 12–13 |
| PH jetzt | 8 % / 16 % / 28 % | 22–25s / 37–41s / 62–66s | 5g 28s | 21–24 / 13–14 / 8–9 |

- Die Spannen in «Knoten netto» kommen vom Briarthorn-Preis (Item- gegen Rezeptseite).
- Angeln ist so gerechnet: 144 Fänge pro Stunde (Stonebull Lake), davon 35 % Deviate Fish; Rechnung in Abschnitt 3.

**Was das heisst**
- Der Wert eines Knotens kommt zu rund 80–85 % aus Frilled Lichen (NH jetzt, Rate 16 %).
- Die Rechnung gilt für Kräutersammeln anstelle von Angeln. Kräuter am Weg der Route kosten kaum Zeit, dafür ist ihre Zahl offen.
- Für den Plan heisst das eine Variante: Kräuterkunde erst in Thunder Bluff (Stufe 20) verlernen und Verzauberkunst erst dort lernen.
  - Im Guide müsste Verzauberkunst 1–50 nach Thunder Bluff wandern.
  - Die Embossed Leather Gloves würden dort entzaubert.
  - Dafür bringt die Route von Stufe 16 bis 20 die Kräuter am Weg.
- Ob sich das lohnt, hängt an zwei Zahlen: Knoten pro Stunde und Frilled-Lichen-Rate. Beides misst M4.

## 3. Angeln im Brachland

**Stellen** (Forever-Karte 1413, aus RXP-Weltkoordinaten umgerechnet, im Spiel ungeprüft)

| Stelle | Spielkoordinaten | Grundlage |
|---|---|---|
| Lushwater Oasis | 46.8, 39.4 (Mittelwert der 35 Punkte; Bereich x 45.6–48.6, y 36.9–42.1) | RXP-Schleife um den See bei Hezrul (Zeilen 2855–2889) |
| Forgotten Pools | 45.1, 22.5 | Bubbling Fissure, Quest 870 (Zeile 1550) |
| Stagnant Oasis | 55.6, 42.8 | Bubbling Fissure, Quest 877 (Zeile 2540) |

- Warcraft Tavern [Classic] nennt Lushwater 46, 40; Stagnant Oasis 55, 43; Forgotten Pools 45, 23. Das liegt bis etwa 1,6 Punkte daneben.
- warcraft.wiki.gg und wowpedia nennen andere Werte. Die gelten für die Karte nach Cataclysm und passen nicht zu Forever.

**Fänge** (AHledger, Lushwater Oasis, offenes Wasser)
- Gesehen: Longjaw 69×, Deviate Fish 53×, Catfish 25×, Smallfish 13× (Zonenseite).
- Die Item-Seite von Deviate Fish nennt 35 % von 153 Beutefenstern.
- Classic-Raten für Deviate Fish (wowseer): Lushwater 29 %, Stagnant Oasis 29 %, Forgotten Pools 26 %; in den Schwärmen 85 %.

**Nötige Angelfertigkeit**
- Forever: nicht veröffentlicht.
  - realmfirst: «The Forever client does not publish a fishing level per zone»
  - classicwowforever: «Zone skill levels live on the server, so they aren't confirmed for Forever yet»
- Classic-Daten, ab wann kein Fisch mehr entkommt:
  - 75: wowforever.be, foreverchanges, Wowhead
  - 100: Warcraft Tavern
  - Das ist ein Widerspruch.

**Preise** (Deviate Fish, Scan 13.10. 23:15 UTC)

| Markt | Median | 30 Tage | Verkauf pro Tag |
|---|---|---|---|
| NH | 4s 50c | 4s 19c | nicht angegeben |
| PH | 10s 99c | 7s 26c | etwa 1'900 |

- Savory Deviate Delight (Kochen 85) bringt weniger als der rohe Fisch: NH 4s 45c, PH 7s 94c (Best Practice §9). Roh verkaufen bringt also mehr. So lautet auch der Entscheid vom 13.10.: Es zählt der höhere Wert, roh oder gekocht.
- Übrige Fische (Vorbefund 13.10.): Longjaw NH 12c, Catfish NH 39c. Sie ändern am Ergebnis wenig.

**Gold pro Stunde, gerechnet**
- Fangrate vom Stonebull Lake: 14 Fänge in 349 s (Testlog 13.10., Angeln 1–15, Mulgore). Das sind 144 Fänge pro Stunde.
- Davon 35 % Deviate Fish: 50,5 pro Stunde.
- Ergebnis pro Stunde, netto:
  - NH: 2g 16s (30 Tage: 2g 1s)
  - PH: 5g 28s (30 Tage: 3g 49s)
- Ungeprüft:
  - die Fangrate im Brachland
  - wie viele Fische dort bei welcher Fertigkeit entkommen
- Messung M3 klärt beides.

## 4. LW- und VZ-Erzeugnisse mit Gewinn (AHledger)

Marge = «Value» minus Reagenzien, beides zum Median. Wer eigenes Material nimmt, rechnet mit dessen Verkaufswert. «Absatz» = verkauft pro Tag laut Fliesstext der Seite.

| Erzeugnis | LW | Farben (AHledger) | Marge NH / PH | Absatz | Muster, Quelle |
|---|---|---|---|---|---|
| Cured Light Hide | 10 | 10/50/60/70 | +4s 53c / −29c | ~280 NH, ~700 PH | Lehrer; NH-Median 8s 73c, im 30-Tage-Chart +490 % |
| Medium Armor Kit | 50 | 50/90/97/105 | +1s 70c / +1s 46c | ~180 NH | Lehrer |
| Mystic Medium Armor Kit | 55 (kami-labs 80) | 55/95/102/110 | +3s 24c / +13s 22c | ~170 PH | Muster 252783 bei Tamar (Orgrimmar) 4s 50c, «a profession trainer teaches it as well» |
| Light Leather Reagent Bag | 1 (SeeMeta, kami-labs 30) | 1/40/45/50 | +9s 6c / +2s 44c | ~47 NH, ~150 PH | Muster 277716 (BoP), Quelle nicht gefunden |
| White Leather Jerkin | 30 | 30/70/85/100 | +8s 36c / +89s 3c | ~21 PH | Muster 2407, Drop (höchstens 0,39 %, MetaForge) |
| Heavy Armor Kit | 105 | 105/145/155/165 | −9s 16c / +26s 75c | ~370 PH | Lehrer |
| Forceful Heavy Armor Kit | 115 | 115/155/165/175 | +11s 43c / +3s 23c | ~55 PH | Muster 252812, Horde-Quelle nicht gefunden |
| Barbaric Bracers | 115 | 115/155/165/175 | +15g 24s / +9g 70s | ~12 NH, ~72 PH | Muster 18949 und «Lehrer» (widersprüchlich), Quelle in Forever nicht gefunden |
| Herbalist's Gloves | 95 | nicht abgerufen | nur PH: +3g 8s | ~16 PH | 4 Kingsblood je Stück |
| Barbaric Shoulders | 130 | nicht abgerufen | nur PH: +91s 53c | ~89 PH | |
| Dusky Leather Armor | 130 | nicht abgerufen | nur PH: +73s 18c | ~43 PH | |
| Guardian Leather Bracers | 150 | nicht abgerufen | nur PH: +85s 15c | ~16 PH | |
| Dusky Belt | 150 | nicht abgerufen | nur PH: +3g 35s | ~19 PH | |

- Ohne Gewinn, NH / PH:
  - Heavy Leather −2s 51c / −96c
  - Medium Leather −29c / −90c
  - Cured Medium Hide −56c / +48c
  - Forceful Medium Armor Kit −6s 50c / −12s 67c
  - Mystic Heavy Armor Kit −26s 38c / −12s 51c
  - Dark Leather Belt −14s 18c / −12s 60c
- Verzauberkunst bringt wenig:
  - Lesser Magic Wand +41c / +42c, etwa 400 pro Tag (PH)
  - Minor Wizard Oil −2s 26c / +2s 20c
  - Arcane Salvager (VZ 100) PH +1g 95s
  - Händlerpreis hergestellter Zauberstäbe: laut Patch-Notiz zum Level-30-Update 1c (Warcraft Tavern, 01.10.). Datenbanken auf Build 70374 nennen 1s 10c (Lesser Magic Wand) und 2s (Greater Magic Wand): https://foreverchanges.pro/item/11287, https://foreverchanges.pro/item/11288. Das ist ein Widerspruch (Best Practice §9, Nr. 21).
- Der Absatz begrenzt den Gewinn: Ein Markt mit 15 Verkäufen pro Tag nimmt keine 20 Stück zum Median.

**Kandidat B': Stufe B (LW 80–100) mit Armor Kits** (NH, jetzt; grob gerechnet)
- Plan heute:
  - LW 80–90: 10× Cured Medium Hide
  - LW 90–100: 19× Fine Leather Belt, davon 9 entzaubert und 10 für Stufe C behalten
  - Kosten netto rund 1g 34s (Material 1g 55s abzüglich 21s Entzauberungswert; `berufe-plan.md` §1)
- Variante:
  - LW 80–90: 10× Medium Armor Kit (orange bis 90)
  - LW 90–100: 10–11× Mystic Medium Armor Kit (orange bis 95, danach gelb), die Kits verkaufen
  - Die 10 Cured Medium Hide und 10 Fine Leather Belt für Stufe C trotzdem herstellen; sie geben dann keinen Punkt mehr.
- Rechnung:
  - Ein Mystic Kit mit selbst hergestelltem Medium Armor Kit kostet 7s 30c + 3s 44c (2 Minor Mana Potion, 2 Strange Dust). Es bringt 16s 15c netto, also etwa +5s 41c.
  - Die 3s 44c sind erschlossen: Reagenzien des Mystic Kit 12s 91c minus Medium Armor Kit zum Median (9s / 0,95 = 9s 47c).
  - 10 Stück bringen etwa +54s.
  - Dazu kommen 10 Cured Medium Hide (94s) und 10 Fine Leather Belt (32s) sowie das Muster (4s 50c).
  - Ergebnis: Variante rund 76s, Plan rund 1g 34s, also rund 58s günstiger.
- Ungeprüft:
  - Farbstufen: AHledgers orange = gelb − 40 könnte berechnet sein (Abschnitt 5).
  - Lernstufe des Mystic Kit: 55 laut AHledger, 80 laut kami-labs.
  - Preis und Angebot von Minor Mana Potion.
  - Absatz in NH.
- Messungen: M1 (Lehrerliste) und M7.
- Passt dazu: Am 13.10. gab «ein Rezept mit 4 Mittlerem Leder» ab LW 98 Punkte, ab 105 kamen Fehlschläge (`docs/tests/messdaten-2026-10-13.md`). Medium Armor Kit braucht 4 Mittleres Leder, Grau ab 105. Welches Rezept es war, steht nicht im Testlog.

**Kandidat ab LW 130: verkaufen statt entzaubern**
- Stufe D entzaubert 24 Hillman's Leather Gloves. Das kostet netto etwa 11s pro Stück: 30s 74c Material, 19s 83c Entzauberungswert.
- Barbaric Shoulders (+91s 53c, ~89 pro Tag PH) oder Dusky Leather Armor (+73s 18c, ~43 pro Tag) würden aus Kosten Gewinn machen. Voraussetzung: Sie geben in 130–150 noch Punkte.
- Es fehlen:
  - Farbstufen dieser Rezepte
  - NH-Preise
  - der Absatz bei mehreren Stück
- Das klärt M1 (Lehrerliste) teilweise; Preise zum Start.

**Barbaric Bracers** (LW 115)
- Marge pro Stück NH +15g 24s. Ein paar verkaufte Stück würden Stufe D bezahlen.
- Ob man das Muster in Forever bekommt: AHledger nennt Muster 18949 und zugleich «a profession trainer teaches it as well». Das steht auf vielen AHledger-Rezeptseiten, auch bei Rezepten, deren Muster wow-professions beim Händler Pawani für Merchant's Favor führt (https://www.wow-professions.com/forever/npc/pawani). Die Angabe ist also unsicher.
- Die Lehrerliste (M1) zeigt, ob ein Lehrer es führt.

## 5. Punkte beim Herstellen

- Wowpedia: «chance = (greySkill - yourSkill) / (greySkill - yellowSkill)», eingeleitet mit «appears to be»; gleiche Seite: gelb «roughly 60%».
- warcraft.wiki.gg: «Exact chances for a skillup are not known.»
- RankedBoost (Forever): «The game files do not store green or the chance itself».
- In allen 27 am 14.10. abgerufenen AHledger-Rezeptseiten gilt grün = (gelb + grau) / 2, abgerundet, und orange = gelb − 40 (Untergrenze 1). Das ist eine eigene Auswertung; die Farben könnten also berechnet statt aus dem Spiel gelesen sein.
- Ob Forever die Formel ändert: nicht gefunden. Ein Legacy-Bonus erhöht die Chance um «4% (5 Ranks)»; ob pro Rang oder insgesamt, steht dort nicht (Mobalytics, 13.10.: https://mobalytics.gg/wow-forever/guides/wow-forever-all-new-profession-changes).
- Die Testlog-Zeilen HERSTELLEN («Punkt» ja/nein) messen das im Spiel.

## 6. Gold pro Stunde: was im Netz steht

- wowforever.games, ohne Methode, mit Werbung für einen Goldverkäufer:
  - Kräuterkunde 30–60g pro Stunde mit Händler, 50–100g mit AH, Stufe 1–20 (Seite 365, 22.09.)
  - 40–70g pro Stunde auf Stufe 20 (Seite 721, 24.09.)
  - Die Seiten widersprechen sich auch untereinander.
- Ausdrücklich keine Zahlen:
  - LepreStore: «no reliable launch-economy gold-per-hour rankings yet»
  - Overgear: «We avoid exact gold-per-hour claims»
- Ebenfalls ohne Zahlen: ExpCarry, AccountShark, timesaver.gg, mmonster, AHledger.
- Für Angeln nennt keine Forever-Quelle eine Zahl pro Stunde.
- Die einzigen Zahlen pro Stunde in diesem Repo stammen aus eigenen Messungen (Testlog) und den Rechnungen oben.

## 7. Offen (Messplan `docs/tests/messplan-beta.md`)

- Knoten pro Stunde, Kräuter pro Knoten und Frilled-Lichen-Rate im Südbrachland (M4)
- Fangrate, Würfe pro Fang und nötige Fertigkeit an der Lushwater Oasis (M3)
- Lernstufen und Kosten beim Lehrer, ob Barbaric Bracers und Mystic Medium Armor Kit lernbar sind (M1)
- Farbstufen von Medium Armor Kit und Mystic Medium Armor Kit (M7)
- Gold bei Stufe 16 und 20 (M2)
- NH-Preise und Farbstufen der Erzeugnisse ab LW 130 (Recherche, zum Start Preise des eigenen Realms)
