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

Insgesamt 3 Scans in `data/preise/ah_eigen.csv`.

## Plan-Gegenstände im letzten Scan (2026-10-15 22:15, ? Horde R2d38 Beta)

Abweichung = 7-Tage-Median gegenüber dem AHledger-Median (Normal Horde US). «nur X Stück»: so viel war im Angebot; «mind.»: mehr Stück als gespeicherte Preisstufen, der Rest ist mit dem höchsten bekannten Preis gerechnet.

| Material | ID | AHledger | Tiefstpreis | Median | 7 Tage (Scans) | Menge | 100 Stück kosten | Abweichung | Plan |
|---|---|---|---|---|---|---|---|---|---|
| Black Pearl (Schwarze Perle) | 7971 | 10g | 3g 99s 99c | 4g 94s 99c | 4g 95s (3) | 81 | nur 81 Stück | -50 % | ja |
| Crystal Vial | 8925 | 5s | 2s 22c | 5s 55c | 2s 22c (3) | 115 | 3g 84s 85c | -56 % | ja |
| Cured Light Hide (Geschmeidiger leichter Balg) | 4231 | – | 1s 15c | 1s 16c | 1s 16c (3) | 431 | 1g 15s 77c | – | ja |
| Cured Medium Hide (Geschmeidiger mittlerer Balg) | 4233 | – | 9s | 11s 95c | 11s 95c (3) | 953 | 9g | – | ja |
| Dark Leather Belt (Dunkler Ledergürtel) | 4249 | – | 8s | 8s | 8s (3) | 322 | 8g | – | ja |
| Deviate Fish (Deviatfisch) | 6522 | – | 5s 50c | 5s 97c | 5s 97c (3) | 1256 | 5g 50s | – | ja |
| Dream Dust (Traumstaub) | 11176 | 58s | 50s 98c | 50s 98c | 50s 98c (3) | 222 | 50g 98s | -12 % | ja |
| Embossed Leather Gloves (Geprägte Lederhandschuhe) | 4239 | – | 2s | 2s | 2s (3) | 818 | 2g | – | ja |
| Fine Leather Belt (Feiner Ledergürtel) | 4246 | – | 3s | 3s | 3s (3) | 50 | nur 50 Stück | – | ja |
| Golden Pearl (Goldene Perle) | 13926 | 5g | 1g 73s 99c | 1g 99s | 1g 99s (3) | 58 | nur 58 Stück | -60 % | ja |
| Golden Rod (Goldrute) | 11128 | 8s | 10s | 14s | 14s (3) | 159 | 12g 40s | +75 % | ja |
| Greater Astral Essence (Große Astralessenz) | 11082 | 28s 54c | 25s | 31s 99c | 31s 99c (3) | 524 | 25g 43s 12c | +12 % | ja |
| Greater Eternal Essence (Große ewige Essenz) | 16203 | – | 8g | 8g | 4g (3) | 2 | nur 2 Stück | – | dünn |
| Greater Magic Essence (Große Magieessenz) | 10939 | 1s 96c | 1s 45c | 1s 50c | 1s 50c (3) | 1437 | 1g 46s 68c | -23 % | ja |
| Greater Mystic Essence (Große Mystikeressenz) | 11135 | 44s | 15s | 15s | 15s (3) | 401 | 15g | -66 % | ja |
| Greater Nether Essence (Große Netheressenz) | 11175 | 8g | 9g 99s 95c | 9g 99s 95c | 9g 99s 95c (3) | 9 | nur 9 Stück | +25 % | ja |
| Heavy Hide (Schwerer Balg) | 4235 | 35s 40c | 26s | 31s | 37s (3) | 751 | 27g 90s 92c | +5 % | ja |
| Heavy Leather (Schweres Leder) | 4234 | 11s 98c | 6s | 8s 59c | 8s 59c (3) | 1200 | 7g 37s 86c | -28 % | ja |
| Hillman's Leather Gloves (Lederhandschuhe des Hügelwächters) | 4247 | – | 22s | 30s | 30s (3) | 239 | 24g 3s | – | ja |
| Iridescent Pearl (Schillernde Perle) | 5500 | 3g 4s 50c | 1g 15s | 1g 39s | 1g 39s (3) | 72 | nur 72 Stück | -54 % | ja |
| Large Brilliant Shard (Großer glänzender Splitter) | 14344 | – | 19g 99s | 19g 99s | 19g 99s (3) | 5 | nur 5 Stück | – | dünn |
| Large Glimmering Shard (Großer gleißender Splitter) | 11084 | 78s 99c | 98s | 98s 99c | 98s 99c (3) | 184 | 98g 68s 31c | +25 % | ja |
| Large Glowing Shard (Großer leuchtender Splitter) | 11139 | 7g | 6g 99s 98c | 7g 98s | 7g 98s (3) | 62 | nur 62 Stück | +14 % | ja |
| Large Radiant Shard (Großer strahlender Splitter) | 11178 | 11g 49s | 25g | 25g | 25g (3) | 75 | nur 75 Stück | +118 % | ja |
| Lesser Astral Essence (Geringe Astralessenz) | 10998 | 6s 4c | 9s 83c | 9s 83c | 9s 83c (3) | 199 | 9g 83s | +63 % | ja |
| Lesser Eternal Essence (Geringe ewige Essenz) | 16202 | 2g | 1g 18s 99c | 1g 18s 99c | 1g 18s 99c (3) | 25 | nur 25 Stück | -41 % | dünn |
| Lesser Magic Essence (Geringe Magieessenz) | 10938 | 69c | 88c | 91c | 91c (3) | 2484 | 88s | +32 % | ja |
| Lesser Mystic Essence (Geringe Mystikeressenz) | 11134 | 15s 96c | 7s | 7s 47c | 7s 47c (3) | 906 | 7g 46s 53c | -53 % | ja |
| Lesser Nether Essence (Geringe Netheressenz) | 11174 | 2g 68s 98c | 3g 39s 57c | 3g 39s 57c | 3g 39s 57c (3) | 65 | nur 65 Stück | +26 % | ja |
| Light Armor Kit (Leichtes Rüstungsset) | 2304 | – | 28c | 35c | 35c (3) | 720 | 28s 37c | – | ja |
| Light Hide (Leichter Balg) | 783 | 69c | 64c | 68c | 74c (3) | 694 | 64s 54c | +7 % | ja |
| Light Leather (Leichtes Leder) | 2318 | 50c | 35c | 60c | 64c (3) | 8544 | 35s | +28 % | ja |
| Light Leather Pants (Leichte Lederhose) | 7282 | – | 6s | 6s | 6s (3) | 162 | 6g | – | ja |
| Medium Hide (Mittlerer Balg) | 4232 | 8s 88c | 7s | 7s 90c | 7s 90c (3) | 478 | 7g 28s 8c | -11 % | ja |
| Medium Leather (Mittleres Leder) | 2319 | 1s 91c | 1s 72c | 1s 99c | 1s 99c (3) | 7939 | 1g 72s | +4 % | ja |
| Purple Lotus (Lila Lotus) | 8831 | 20g 5s | 25s | 29s | 29s (3) | 102 | 28g 28s 61c | -99 % | ja |
| Rugged Leather (Unverwüstliches Leder) | 8170 | 19s 2c | 5s 22c | 5s 50c | 5s 50c (3) | 470 | 5g 22s 30c | -71 % | ja |
| Ruined Leather Scraps (Verdorbene Lederfetzen) | 2934 | 25c | 15c | 22c | 29c (3) | 3066 | 15s | +16 % | ja |
| Shadowgem (Schattenedelstein) | 1210 | 3s 14c | 2s 55c | 2s 63c | 2s 63c (3) | 214 | 2g 58s 8c | -16 % | ja |
| Silver Rod (Silberrute) | 6338 | 19s | 9s | 15s | 15s (3) | 327 | 9g | -21 % | ja |
| Small Brilliant Shard (Kleiner glänzender Splitter) | 14343 | 4g 88s | 1g 99s | 2g 74s | 2g 74s (3) | 7 | nur 7 Stück | -44 % | dünn |
| Small Glimmering Shard (Kleiner gleißender Splitter) | 10978 | 3s 66c | 1s 49c | 2s | 2s (3) | 859 | 1g 81s 17c | -45 % | ja |
| Small Glowing Shard (Kleiner leuchtender Splitter) | 11138 | 75s 99c | 14s 73c | 14s 75c | 14s 75c (3) | 235 | 14g 73s 13c | -81 % | ja |
| Small Radiant Shard (Kleiner strahlender Splitter) | 11177 | 7g 99s 98c | 10g | 10g | 10g 1s (3) | 51 | nur 51 Stück | +25 % | dünn |
| Soul Dust (Seelenstaub) | 11083 | 7s 21c | 5s 78c | 9s | 5s 84c (3) | 562 | 5g 79s 4c | -19 % | ja |
| Strange Dust (Seltsamer Staub) | 10940 | 84c | 60c | 65c | 65c (3) | 3988 | 60s 82c | -23 % | ja |
| Thick Leather (Dickes Leder) | 4304 | 35s 79c | 50s | 58s 47c | 58s 47c (3) | 478 | 57g 43s 3c | +63 % | ja |
| Truesilver Rod (Echtsilberrute) | 11144 | 85s | 22s | 22s | 22s (3) | 20 | nur 20 Stück | -74 % | dünn |
| Vision Dust (Visionenstaub) | 11137 | 19s 71c | 5s 91c | 6s 91c | 6s 91c (3) | 1306 | 5g 91s | -65 % | ja |

Nicht im Angebot: Arcanite Rod (16206), Illusion Dust (16204).

Spalte «Plan»: «ja» = mit `--eintragen` übernehmbar, «dünn» = bleibt beim AHledger-Preis.

## Im Plan

Noch nicht eingetragen: Der Plan rechnet weiter mit den AHledger-Preisen. Eintragen mit `python3 tools/ah_aus_testlog.py <Testlog> --eintragen`, danach `python3 tools/plan_berufe.py` (offene Entscheidung 17).
