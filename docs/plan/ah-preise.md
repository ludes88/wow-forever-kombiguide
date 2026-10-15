# Eigene AH-Preise (erzeugt von `tools/ah_aus_testlog.py`)

Nicht von Hand ändern: neues Testlog einlesen und neu erzeugen.

## Quellen

- Eigene Scans mit Testlog 3.5: `C_AuctionHouse.ReplicateItems` laut Forever-UI 1.60.1 (70374), `Blizzard_APIDocumentationGenerated/AuctionHouseDocumentation.lua` (https://github.com/Gethe/wow-ui-source/tree/forever). Werte: `data/preise/ah_eigen.csv` (Plan-Gegenstände, alle Scans), `data/preise/ah_alle.csv` (letzter Scan, alle Gegenstände).
- Vergleich: AHledger, Forever-Beta, Median Normal Horde US (`data/rechnung/Preise.csv`, Spalte «NH Median (s)»).
- Grenze Beta/Live: Start am 04.11.2026 (https://www.warcrafttavern.com/forever/guides/beta/, geprüft am 13.10.2026).
- Median = Preis pro Stück, bei dem die Hälfte der angebotenen Stückzahl erreicht ist (nach Stückzahl gewichtet). 7 Tage = Median der Scan-Mediane der letzten 7 Tage bis zum letzten Scan, gleicher Markt, nur vollständige Scans. «dünn» = im Mittel weniger als 50 Stück im Angebot (Schwelle aus `data/rechnung/Uebersicht.csv`).
- Markt = Region, Fraktion, Kurzzeichen des Realms (statt des Namens), Beta oder Live.

## Scans

| Datum | Markt | Angebote | Gegenstände | nur mit Gebot | Dauer | gelesen aus | Hinweis |
|---|---|---|---|---|---|---|---|
| 2026-10-15 20:12 | ? Horde R2d38 Beta | 65411 | 3079 | 1 | 18 s | Testlog-Datei |  |
| 2026-10-15 21:54 | ? Horde R2d38 Beta | 67980 | 3064 | 1 | 17 s | Testlog-Datei |  |

Insgesamt 2 Scans in `data/preise/ah_eigen.csv`.

## Plan-Gegenstände im letzten Scan (2026-10-15 21:54, ? Horde R2d38 Beta)

Abweichung = 7-Tage-Median gegenüber dem AHledger-Median (Normal Horde US). «nur X Stück»: so viel war im Angebot; «mind.»: mehr Stück als gespeicherte Preisstufen, der Rest ist mit dem höchsten bekannten Preis gerechnet.

| Material | ID | AHledger | Tiefstpreis | Median | 7 Tage (Scans) | Menge | 100 Stück kosten | Abweichung | Plan |
|---|---|---|---|---|---|---|---|---|---|
| Black Pearl (Schwarze Perle) | 7971 | 10g | 4g 94s 99c | 4g 95s | 4g 96s 96c (2) | 59 | nur 59 Stück | -50 % | ja |
| Crystal Vial | 8925 | 5s | 2s 22c | 2s 22c | 2s 22c (2) | 123 | 3g 54s 5c | -56 % | ja |
| Cured Light Hide (Geschmeidiger leichter Balg) | 4231 | – | 1s 15c | 1s 16c | 1s 16c (2) | 430 | 1g 15s 78c | – | ja |
| Cured Medium Hide (Geschmeidiger mittlerer Balg) | 4233 | – | 11s 93c | 11s 95c | 11s 98c (2) | 837 | 11g 94s 69c | – | ja |
| Dark Leather Belt (Dunkler Ledergürtel) | 4249 | – | 8s | 8s | 8s (2) | 301 | 8g | – | ja |
| Deviate Fish (Deviatfisch) | 6522 | – | 5s 50c | 5s 97c | 8s 30c (2) | 1219 | 5g 59s 90c | – | ja |
| Dream Dust (Traumstaub) | 11176 | 58s | 50s 98c | 50s 98c | 50s 98c (2) | 235 | 50g 98s | -12 % | ja |
| Embossed Leather Gloves (Geprägte Lederhandschuhe) | 4239 | – | 2s | 2s | 2s (2) | 829 | 2g | – | ja |
| Fine Leather Belt (Feiner Ledergürtel) | 4246 | – | 3s | 3s | 3s (2) | 50 | nur 50 Stück | – | ja |
| Golden Pearl (Goldene Perle) | 13926 | 5g | 1g 74s | 1g 99s | 2g 44s 95c (2) | 57 | nur 57 Stück | -51 % | ja |
| Golden Rod (Goldrute) | 11128 | 8s | 10s | 14s | 14s 50c (2) | 163 | 12g 24s | +81 % | ja |
| Greater Astral Essence (Große Astralessenz) | 11082 | 28s 54c | 25s | 31s 99c | 31s 99c (2) | 556 | 25g 24s 50c | +12 % | ja |
| Greater Eternal Essence | 16203 | – | 4g | 4g | 4g (2) | 2 | nur 2 Stück | – | dünn |
| Greater Magic Essence (Große Magieessenz) | 10939 | 1s 96c | 1s 49c | 1s 50c | 1s 50c (2) | 1377 | 1g 49s | -23 % | ja |
| Greater Mystic Essence (Große Mystikeressenz) | 11135 | 44s | 15s | 15s | 16s (2) | 404 | 15g | -64 % | ja |
| Greater Nether Essence (Große Netheressenz) | 11175 | 8g | 9g 99s 95c | 9g 99s 95c | 9g 99s 95c (2) | 54 | nur 54 Stück | +25 % | ja |
| Heavy Hide (Schwerer Balg) | 4235 | 35s 40c | 30s | 37s | 39s (2) | 695 | 30g | +10 % | ja |
| Heavy Leather (Schweres Leder) | 4234 | 11s 98c | 8s 14c | 8s 59c | 8s 40c (2) | 1229 | 8g 14s 99c | -30 % | ja |
| Hillman's Leather Gloves (Lederhandschuhe des Hügelwächters) | 4247 | – | 23s | 30s | 30s (2) | 213 | 26g 28s | – | ja |
| Iridescent Pearl (Schillernde Perle) | 5500 | 3g 4s 50c | 1g 32s 99c | 1g 39s | 1g 56s (2) | 69 | nur 69 Stück | -49 % | ja |
| Large Brilliant Shard (Großer glänzender Splitter) | 14344 | – | 19g 99s | 19g 99s | 19g 66s 49c (2) | 4 | nur 4 Stück | – | dünn |
| Large Glimmering Shard (Großer gleißender Splitter) | 11084 | 78s 99c | 95s 98c | 98s 99c | 99s 50c (2) | 242 | 98g 42s 27c | +26 % | ja |
| Large Glowing Shard (Großer leuchtender Splitter) | 11139 | 7g | 6g 99s 99c | 7g 99s | 7g 98s 50c (2) | 49 | nur 49 Stück | +14 % | ja |
| Large Radiant Shard (Großer strahlender Splitter) | 11178 | 11g 49s | 25g | 25g | 25g (2) | 75 | nur 75 Stück | +118 % | ja |
| Lesser Astral Essence (Geringe Astralessenz) | 10998 | 6s 4c | 9s 83c | 9s 83c | 9s 84c (2) | 241 | 9g 83s | +63 % | ja |
| Lesser Eternal Essence (Geringe ewige Essenz) | 16202 | 2g | 1g 18s 99c | 1g 18s 99c | 1g 18s 99c (2) | 25 | nur 25 Stück | -41 % | dünn |
| Lesser Magic Essence (Geringe Magieessenz) | 10938 | 69c | 88c | 91c | 92c (2) | 2650 | 88s | +33 % | ja |
| Lesser Mystic Essence (Geringe Mystikeressenz) | 11134 | 15s 96c | 7s 47c | 7s 47c | 8s 22c (2) | 917 | 7g 47s | -48 % | ja |
| Lesser Nether Essence (Geringe Netheressenz) | 11174 | 2g 68s 98c | 3g 39s 57c | 3g 39s 57c | 3g 39s 57c (2) | 58 | nur 58 Stück | +26 % | dünn |
| Light Armor Kit (Leichtes Rüstungsset) | 2304 | – | 29c | 35c | 35c (2) | 691 | 29s | – | ja |
| Light Hide (Leichter Balg) | 783 | 69c | 65c | 97c | 86c (2) | 633 | 65s | +24 % | ja |
| Light Leather (Leichtes Leder) | 2318 | 50c | 52c | 64c | 81c (2) | 7094 | 52s | +62 % | ja |
| Light Leather Pants (Leichte Lederhose) | 7282 | – | 6s | 6s | 6s (2) | 141 | 6g | – | ja |
| Medium Hide (Mittlerer Balg) | 4232 | 8s 88c | 6s 66c | 7s 90c | 7s 90c (2) | 488 | 7g 3s 8c | -11 % | ja |
| Medium Leather (Mittleres Leder) | 2319 | 1s 91c | 95c | 1s 99c | 2s 14c (2) | 7934 | 1g 74s 20c | +12 % | ja |
| Purple Lotus (Lila Lotus) | 8831 | 20g 5s | 25s | 29s | 29s (2) | 96 | nur 96 Stück | -99 % | ja |
| Rugged Leather (Unverwüstliches Leder) | 8170 | 19s 2c | 5s 22c | 5s 50c | 8s 2c (2) | 473 | 5g 22s 44c | -58 % | ja |
| Ruined Leather Scraps (Verdorbene Lederfetzen) | 2934 | 25c | 15c | 29c | 32c (2) | 2530 | 15s 87c | +26 % | ja |
| Shadowgem (Schattenedelstein) | 1210 | 3s 14c | 2s 50c | 2s 61c | 2s 62c (2) | 263 | 2g 54s 9c | -17 % | ja |
| Silver Rod (Silberrute) | 6338 | 19s | 9s | 15s | 16s 50c (2) | 318 | 9g | -13 % | ja |
| Small Brilliant Shard (Kleiner glänzender Splitter) | 14343 | 4g 88s | 1g 99s | 2g 74s | 2g 74s (2) | 7 | nur 7 Stück | -44 % | dünn |
| Small Glimmering Shard (Kleiner gleißender Splitter) | 10978 | 3s 66c | 1s 91c | 2s | 2s 7c (2) | 869 | 1g 93s 39c | -43 % | ja |
| Small Glowing Shard (Kleiner leuchtender Splitter) | 11138 | 75s 99c | 14s 73c | 14s 75c | 14s 75c (2) | 226 | 14g 73s 28c | -81 % | ja |
| Small Radiant Shard (Kleiner strahlender Splitter) | 11177 | 7g 99s 98c | 10g | 10g 1s | 10g 1s (2) | 23 | nur 23 Stück | +25 % | dünn |
| Soul Dust (Seelenstaub) | 11083 | 7s 21c | 5s 60c | 5s 84c | 5s 84c (2) | 878 | 5g 60s | -19 % | ja |
| Strange Dust (Seltsamer Staub) | 10940 | 84c | 63c | 65c | 65c (2) | 3807 | 63s | -23 % | ja |
| Thick Leather (Dickes Leder) | 4304 | 35s 79c | 50s | 58s 47c | 59s 24c (2) | 486 | 56g 32s 73c | +66 % | ja |
| Truesilver Rod (Echtsilberrute) | 11144 | 85s | 22s | 22s | 22s (2) | 26 | nur 26 Stück | -74 % | dünn |
| Vision Dust (Visionenstaub) | 11137 | 19s 71c | 5s 91c | 6s 91c | 6s 93c (2) | 1368 | 5g 91s | -65 % | ja |

Nicht im Angebot: Arcanite Rod (16206), Illusion Dust (16204).

Spalte «Plan»: «ja» = mit `--eintragen` übernehmbar, «dünn» = bleibt beim AHledger-Preis.

## Im Plan

Noch nicht eingetragen: Der Plan rechnet weiter mit den AHledger-Preisen. Eintragen mit `python3 tools/ah_aus_testlog.py <Testlog> --eintragen`, danach `python3 tools/plan_berufe.py` (offene Entscheidung 17).
