# Eigene AH-Preise (erzeugt von `tools/ah_aus_testlog.py`)

Nicht von Hand ändern: neues Testlog einlesen und neu erzeugen.

## Quellen

- Eigene Scans mit Testlog 3.5 oder neuer: `C_AuctionHouse.ReplicateItems` laut Forever-UI 1.60.1 (70374), `Blizzard_APIDocumentationGenerated/AuctionHouseDocumentation.lua` (https://github.com/Gethe/wow-ui-source/tree/forever). Werte: `data/preise/ah_eigen.csv` (Plan-Gegenstände, alle Scans), `data/preise/ah_alle.csv` (letzter Scan, alle Gegenstände).
- Vergleich: AHledger, Forever-Beta, Median Normal Horde US (`data/rechnung/Preise.csv`, Spalte «NH Median (s)»).
- Grenze Beta/Live: Start am 04.11.2026 (https://www.warcrafttavern.com/forever/guides/beta/, geprüft am 13.10.2026).
- Median = Preis pro Stück, bei dem die Hälfte der angebotenen Stückzahl erreicht ist (nach Stückzahl gewichtet). 7 Tage = Median der Scan-Mediane der letzten 7 Tage bis zum letzten Scan, gleicher Markt, nur vollständige Scans. «dünn» = im Median der Scans weniger als 50 Stück im Angebot (Schwelle aus `data/rechnung/Uebersicht.csv`).
- Markt = Region, Fraktion, Kurzzeichen des Realms (statt des Namens), Beta oder Live.

## Scans

| Datum | Markt | Angebote | Gegenstände | nur mit Gebot | Dauer | gelesen aus | Hinweis |
|---|---|---|---|---|---|---|---|
| 2026-10-15 20:12 | ? Horde R2d38 Beta | 65411 | 3079 | 1 | 18 s | Testlog-Datei |  |
| 2026-10-15 21:54 | ? Horde R2d38 Beta | 67980 | 3064 | 1 | 17 s | Testlog-Datei |  |
| 2026-10-15 22:15 | ? Horde R2d38 Beta | 68980 | 3058 | 1 | 17 s | Testlog-Datei |  |
| 2026-10-17 13:36 | ? Horde R2d38 Beta | 50662 | 2925 | 0 | 11 s | Testlog-Datei |  |

Insgesamt 4 Scans in `data/preise/ah_eigen.csv`.

## Plan-Gegenstände im letzten Scan (2026-10-17 13:36, ? Horde R2d38 Beta)

Abweichung = 7-Tage-Median gegenüber dem AHledger-Median (Normal Horde US). «nur X Stück»: so viel war im Angebot; «mind.»: mehr Stück als gespeicherte Preisstufen, der Rest ist mit dem höchsten bekannten Preis gerechnet.

| Material | ID | AHledger | Tiefstpreis | Median | 7 Tage (Scans) | Menge | 100 Stück kosten | Abweichung | Plan |
|---|---|---|---|---|---|---|---|---|---|
| Black Pearl (Schwarze Perle) | 7971 | 10g | 5g 99s 89c | 5g 99s 89c | 4g 96s 96c (4) | 15 | nur 15 Stück | -50 % | ja |
| Crystal Vial | 8925 | 5s | 5s 60c | 5s 60c | 3s 88c (4) | 41 | nur 41 Stück | -22 % | ja |
| Cured Light Hide (Geschmeidiger leichter Balg) | 4231 | – | 1s 47c | 1s 53c | 1s 16c (4) | 574 | 1g 47s | – | ja |
| Cured Medium Hide (Geschmeidiger mittlerer Balg) | 4233 | – | 5s 43c | 5s 49c | 11s 95c (4) | 895 | 5g 47s 40c | – | ja |
| Dark Leather Belt (Dunkler Ledergürtel) | 4249 | – | 8s | 8s | 8s (4) | 147 | 8g | – | ja |
| Deviate Fish (Deviatfisch) | 6522 | – | 7s 98c | 7s 98c | 6s 98c (4) | 767 | 7g 98s | – | ja |
| Dream Dust (Traumstaub) | 11176 | 58s | 25s 47c | 25s 47c | 50s 98c (4) | 556 | 25g 47s | -12 % | ja |
| Embossed Leather Gloves (Geprägte Lederhandschuhe) | 4239 | – | 1s | 1s | 2s (4) | 288 | 1g | – | ja |
| Fine Leather Belt (Feiner Ledergürtel) | 4246 | – | 2s | 3s | 3s (4) | 164 | 2g 79s | – | ja |
| Golden Pearl (Goldene Perle) | 13926 | 5g | 1g 44s | 1g 50s | 1g 99s (4) | 9 | nur 9 Stück | -60 % | ja |
| Golden Rod (Goldrute) | 11128 | 8s | 1g | 3g | 14s 50c (4) | 107 | 251g 76s | +81 % | ja |
| Greater Astral Essence (Große Astralessenz) | 11082 | 28s 54c | 44s 48c | 49s 99c | 31s 99c (4) | 422 | 45g 51s 32c | +12 % | ja |
| Greater Eternal Essence (Große ewige Essenz) | 16203 | – | 4g | 4g | 4g (4) | 2 | nur 2 Stück | – | dünn |
| Greater Magic Essence (Große Magieessenz) | 10939 | 1s 96c | 1s | 1s 20c | 1s 50c (4) | 694 | 1g | -23 % | ja |
| Greater Magic Wand (Großer Magiezauberstab) | 11288 | – | 3s | 3s | 3s (2) | 211 | 3g | – | ja |
| Greater Mystic Essence (Große Mystikeressenz) | 11135 | 44s | 1g 68s | 3g 12s 14c | 16s (4) | 561 | 183g 53s | -64 % | ja |
| Greater Nether Essence (Große Netheressenz) | 11175 | 8g | 14g 99s 99c | 15g | 9g 99s 95c (4) | 100 | 1744g 99s 50c | +25 % | ja |
| Heavy Hide (Schwerer Balg) | 4235 | 35s 40c | 23s 22c | 26s 50c | 34s (4) | 367 | 23g 32s 81c | -4 % | ja |
| Heavy Leather (Schweres Leder) | 4234 | 11s 98c | 9s | 9s | 8s 59c (4) | 785 | 9g | -28 % | ja |
| Hillman's Leather Gloves (Lederhandschuhe des Hügelwächters) | 4247 | – | 14s | 15s | 30s (4) | 118 | 14g 77s | – | ja |
| Iridescent Pearl (Schillernde Perle) | 5500 | 3g 4s 50c | 95s 79c | 99s 86c | 1g 39s (4) | 38 | nur 38 Stück | -54 % | ja |
| Large Brilliant Shard (Großer glänzender Splitter) | 14344 | – | 18g 1s | 18g 1s | 19g 66s 49c (4) | 6 | nur 6 Stück | – | dünn |
| Large Glimmering Shard (Großer gleißender Splitter) | 11084 | 78s 99c | 84s 98c | 84s 98c | 98s 99c (4) | 281 | 84g 98s | +25 % | ja |
| Large Glowing Shard (Großer leuchtender Splitter) | 11139 | 7g | 3g 20s 89c | 3g 80s 90c | 7g 98s (4) | 107 | 377g 53s 97c | +14 % | ja |
| Large Radiant Shard (Großer strahlender Splitter) | 11178 | 11g 49s | 25g | 25g | 25g (4) | 60 | nur 60 Stück | +118 % | ja |
| Lesser Astral Essence (Geringe Astralessenz) | 10998 | 6s 4c | 8s 89c | 8s 90c | 9s 83c (4) | 44 | nur 44 Stück | +63 % | ja |
| Lesser Eternal Essence (Geringe ewige Essenz) | 16202 | 2g | 1g 0s 99c | 1g 0s 99c | 1g 18s 99c (4) | 29 | nur 29 Stück | -41 % | dünn |
| Lesser Magic Essence (Geringe Magieessenz) | 10938 | 69c | 76c | 77c | 91c (4) | 1116 | 76s | +32 % | ja |
| Lesser Magic Wand (Geringer Magiezauberstab) | 11287 | – | 2s | 5s | 3s 50c (2) | 195 | 4g 46s | – | ja |
| Lesser Mystic Essence (Geringe Mystikeressenz) | 11134 | 15s 96c | 38s | 1g 20s | 8s 22c (4) | 674 | 41g 53s 78c | -48 % | ja |
| Lesser Nether Essence (Geringe Netheressenz) | 11174 | 2g 68s 98c | 3g 80s 99c | 3g 97s 99c | 3g 39s 57c (4) | 181 | 385g 75s 1c | +26 % | ja |
| Light Armor Kit (Leichtes Rüstungsset) | 2304 | – | 15c | 17c | 35c (4) | 476 | 15s | – | ja |
| Light Hide (Leichter Balg) | 783 | 69c | 72c | 73c | 74c (4) | 355 | 72s 89c | +7 % | ja |
| Light Leather (Leichtes Leder) | 2318 | 50c | 68c | 85c | 74c (4) | 5411 | 68s | +49 % | ja |
| Light Leather Pants (Leichte Lederhose) | 7282 | – | 6s | 6s | 6s (4) | 30 | nur 30 Stück | – | ja |
| Medium Hide (Mittlerer Balg) | 4232 | 8s 88c | 4s 70c | 4s 73c | 7s 90c (4) | 376 | 4g 72s 49c | -11 % | ja |
| Medium Leather (Mittleres Leder) | 2319 | 1s 91c | 2s 30c | 2s 86c | 2s 14c (4) | 5175 | 2g 30s | +12 % | ja |
| Purple Lotus (Lila Lotus) | 8831 | 20g 5s | 30s 98c | 30s 99c | 29s (4) | 44 | nur 44 Stück | -99 % | ja |
| Rugged Leather (Unverwüstliches Leder) | 8170 | 19s 2c | 5s | 5s 49c | 5s 50c (4) | 155 | 5g 20s 58c | -71 % | ja |
| Ruined Leather Scraps (Verdorbene Lederfetzen) | 2934 | 25c | 29c | 50c | 32c (4) | 1666 | 29s 22c | +26 % | ja |
| Shadowgem (Schattenedelstein) | 1210 | 3s 14c | 2s 90c | 3s | 2s 63c (4) | 354 | 2g 95s 69c | -16 % | ja |
| Silver Rod (Silberrute) | 6338 | 19s | 6s | 7s | 15s (4) | 115 | 7g 50s | -21 % | ja |
| Small Brilliant Shard (Kleiner glänzender Splitter) | 14343 | 4g 88s | 2g 1s | 2g 1s | 2g 74s (4) | 1 | nur 1 Stück | -44 % | dünn |
| Small Glimmering Shard (Kleiner gleißender Splitter) | 10978 | 3s 66c | 50c | 80c | 2s (4) | 1050 | 50s 80c | -45 % | ja |
| Small Glowing Shard (Kleiner leuchtender Splitter) | 11138 | 75s 99c | 18s 95c | 24s 99c | 14s 75c (4) | 239 | 20g 30s 48c | -81 % | ja |
| Small Radiant Shard (Kleiner strahlender Splitter) | 11177 | 7g 99s 98c | 16g 90s 99c | 17g 99s 98c | 10g 1s (4) | 55 | nur 55 Stück | +25 % | dünn |
| Soul Dust (Seelenstaub) | 11083 | 7s 21c | 4s 94c | 5s | 5s 84c (4) | 2169 | 4g 94s | -19 % | ja |
| Strange Dust (Seltsamer Staub) | 10940 | 84c | 33c | 38c | 65c (4) | 4729 | 33s | -23 % | ja |
| Thick Leather (Dickes Leder) | 4304 | 35s 79c | 45s | 55s 97c | 58s 47c (4) | 309 | 54g 20s | +63 % | ja |
| Truesilver Rod (Echtsilberrute) | 11144 | 85s | 1g 18s | 1g 20s | 22s (4) | 46 | nur 46 Stück | -74 % | dünn |
| Vision Dust (Visionenstaub) | 11137 | 19s 71c | 9s 99c | 11s 99c | 6s 93c (4) | 1397 | 9g 99s | -65 % | ja |

Nicht im Angebot: Arcanite Rod (16206), Illusion Dust (16204).

## Unter dem Händlerpreis (Testlog 3.7, Scan 2026-10-17 13:36)

Angebote, deren Preis pro Stück unter dem liegt, was der Händler zahlt (`C_Item.GetItemInfo`, «sellPrice», nur Gegenstände, deren Daten der Client schon hatte). Kaufen und beim Händler verkaufen; keine AH-Gebühr. Gewinn = Händlerpreis × Stück − Kaufpreis.

| Gegenstand | ID | Händler zahlt | Stück darunter | kosten | Gewinn |
|---|---|---|---|---|---|
| 3192 | 3192 | 4s 95c | 1 | 4s | 95c |
| Spinnensekret | 3174 | 16c | 48 | 7s 20c | 48c |
| 4461 | 4461 | 2s 8c | 8 | 16s 40c | 24c |
| Geringer Mondstein | 1705 | 6s | 16 | 95s 79c | 21c |
| 3530 | 3530 | 28c | 16 | 4s 32c | 16c |

Spalte «Plan»: «ja» = mit `--eintragen` übernehmbar, «dünn» = bleibt beim AHledger-Preis.

## Im Plan

Noch nicht eingetragen: Der Plan rechnet weiter mit den AHledger-Preisen. Eintragen mit `python3 tools/ah_aus_testlog.py <Testlog> --eintragen`, danach `python3 tools/plan_berufe.py` (offene Entscheidung 17).
