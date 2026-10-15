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

Insgesamt 1 Scans in `data/preise/ah_eigen.csv`.

## Plan-Gegenstände im letzten Scan (2026-10-15 20:12, ? Horde R2d38 Beta)

Abweichung = 7-Tage-Median gegenüber dem AHledger-Median (Normal Horde US). «nur X Stück»: so viel war im Angebot; «mind.»: mehr Stück als gespeicherte Preisstufen, der Rest ist mit dem höchsten bekannten Preis gerechnet.

| Material | ID | AHledger | Tiefstpreis | Median | 7 Tage (Scans) | Menge | 100 Stück kosten | Abweichung | Plan |
|---|---|---|---|---|---|---|---|---|---|
| Black Pearl (Schwarze Perle) | 7971 | 10g | 4g 93s | 4g 98s 93c | 4g 98s 93c (1) | 45 | nur 45 Stück | -50 % | dünn |
| Crystal Vial | 8925 | 5s | 2s 22c | 2s 22c | 2s 22c (1) | 128 | 3g 34s 80c | -56 % | ja |
| Cured Light Hide (Geschmeidiger leichter Balg) | 4231 | – | 1s 15c | 1s 16c | 1s 16c (1) | 818 | 1g 15s 46c | – | ja |
| Cured Medium Hide (Geschmeidiger mittlerer Balg) | 4233 | – | 11s 99c | 12s | 12s (1) | 407 | 11g 99s 46c | – | ja |
| Dark Leather Belt (Dunkler Ledergürtel) | 4249 | – | 8s | 8s | 8s (1) | 267 | 8g | – | ja |
| Deviate Fish | 6522 | – | 5s 96c | 10s 64c | 10s 64c (1) | 1096 | 5g 96s | – | ja |
| Dream Dust (Traumstaub) | 11176 | 58s | 50s 98c | 50s 98c | 50s 98c (1) | 192 | 50g 98s | -12 % | ja |
| Embossed Leather Gloves (Geprägte Lederhandschuhe) | 4239 | – | 2s | 2s | 2s (1) | 631 | 2g | – | ja |
| Fine Leather Belt (Feiner Ledergürtel) | 4246 | – | 3s | 3s | 3s (1) | 80 | nur 80 Stück | – | ja |
| Golden Pearl (Goldene Perle) | 13926 | 5g | 1g 99s | 2g 90s 90c | 2g 90s 90c (1) | 61 | nur 61 Stück | -42 % | ja |
| Golden Rod (Goldrute) | 11128 | 8s | 12s | 15s | 15s (1) | 162 | 13g 55s | +88 % | ja |
| Greater Astral Essence (Große Astralessenz) | 11082 | 28s 54c | 28s 98c | 32s | 32s (1) | 401 | 30g 90s 68c | +12 % | ja |
| Greater Eternal Essence | 16203 | – | 4g | 4g | 4g (1) | 4 | nur 4 Stück | – | dünn |
| Greater Magic Essence (Große Magieessenz) | 10939 | 1s 96c | 1s 49c | 1s 50c | 1s 50c (1) | 1278 | 1g 49s | -23 % | ja |
| Greater Mystic Essence (Große Mystikeressenz) | 11135 | 44s | 15s | 17s | 17s (1) | 228 | 15g 70s | -61 % | ja |
| Greater Nether Essence (Große Netheressenz) | 11175 | 8g | 9g 99s 95c | 9g 99s 95c | 9g 99s 95c (1) | 64 | nur 64 Stück | +25 % | ja |
| Heavy Hide (Schwerer Balg) | 4235 | 35s 40c | 41s | 41s | 41s (1) | 392 | 41g | +16 % | ja |
| Heavy Leather (Schweres Leder) | 4234 | 11s 98c | 8s 15c | 8s 20c | 8s 20c (1) | 2347 | 8g 15s | -32 % | ja |
| Hillman's Leather Gloves (Lederhandschuhe des Hügelwächters) | 4247 | – | 30s | 30s | 30s (1) | 145 | 30g | – | ja |
| Iridescent Pearl (Schillernde Perle) | 5500 | 3g 4s 50c | 1g 39s | 1g 73s | 1g 73s (1) | 47 | nur 47 Stück | -43 % | dünn |
| Large Brilliant Shard | 14344 | – | 19g 33s 98c | 19g 33s 98c | 19g 33s 98c (1) | 2 | nur 2 Stück | – | dünn |
| Large Glimmering Shard (Großer gleißender Splitter) | 11084 | 78s 99c | 99s | 1g | 1g (1) | 122 | 102g 97s 94c | +27 % | ja |
| Large Glowing Shard (Großer leuchtender Splitter) | 11139 | 7g | 6g 99s 99c | 7g 98s | 7g 98s (1) | 66 | nur 66 Stück | +14 % | ja |
| Large Radiant Shard (Großer strahlender Splitter) | 11178 | 11g 49s | 25g | 25g | 25g (1) | 73 | nur 73 Stück | +118 % | ja |
| Lesser Astral Essence (Geringe Astralessenz) | 10998 | 6s 4c | 9s 83c | 9s 86c | 9s 86c (1) | 229 | 9g 84s 30c | +63 % | ja |
| Lesser Eternal Essence (Geringe ewige Essenz) | 16202 | 2g | 1g 18s 99c | 1g 18s 99c | 1g 18s 99c (1) | 33 | nur 33 Stück | -41 % | dünn |
| Lesser Magic Essence (Geringe Magieessenz) | 10938 | 69c | 89c | 93c | 93c (1) | 2638 | 89s 89c | +35 % | ja |
| Lesser Mystic Essence (Geringe Mystikeressenz) | 11134 | 15s 96c | 8s | 8s 98c | 8s 98c (1) | 397 | 8g 55s 86c | -44 % | ja |
| Lesser Nether Essence | 11174 | 2g 68s 98c | 2g 45s | 3g 39s 57c | 3g 39s 57c (1) | 16 | nur 16 Stück | +26 % | dünn |
| Light Armor Kit (Leichtes Rüstungsset) | 2304 | – | 30c | 35c | 35c (1) | 786 | 30s | – | ja |
| Light Hide (Leichter Balg) | 783 | 69c | 58c | 74c | 74c (1) | 685 | 58s 26c | +7 % | ja |
| Light Leather (Leichtes Leder) | 2318 | 50c | 73c | 98c | 98c (1) | 4310 | 73s | +96 % | ja |
| Light Leather Pants (Leichte Lederhose) | 7282 | – | 6s | 6s | 6s (1) | 145 | 6g | – | ja |
| Medium Hide | 4232 | 8s 88c | 7s | 7s 90c | 7s 90c (1) | 519 | 7g 5s 58c | -11 % | ja |
| Medium Leather (Mittleres Leder) | 2319 | 1s 91c | 1s 99c | 2s 29c | 2s 29c (1) | 5984 | 1g 99s | +20 % | ja |
| Purple Lotus (Lila Lotus) | 8831 | 20g 5s | 29s | 29s | 29s (1) | 87 | nur 87 Stück | -99 % | ja |
| Rugged Leather (Unverwüstliches Leder) | 8170 | 19s 2c | 5s 22c | 10s 55c | 10s 55c (1) | 545 | 5g 23s 34c | -45 % | ja |
| Ruined Leather Scraps (Verdorbene Lederfetzen) | 2934 | 25c | 24c | 34c | 34c (1) | 1674 | 24s | +36 % | ja |
| Shadowgem (Schattenedelstein) | 1210 | 3s 14c | 2s 55c | 2s 63c | 2s 63c (1) | 226 | 2g 60s 12c | -16 % | ja |
| Silver Rod (Silberrute) | 6338 | 19s | 9s | 18s | 18s (1) | 244 | 12g 99s | -5 % | ja |
| Small Brilliant Shard (Kleiner glänzender Splitter) | 14343 | 4g 88s | 2g 74s | 2g 74s | 2g 74s (1) | 8 | nur 8 Stück | -44 % | dünn |
| Small Glimmering Shard (Kleiner gleißender Splitter) | 10978 | 3s 66c | 1s 96c | 2s 14c | 2s 14c (1) | 932 | 1g 96s 94c | -42 % | ja |
| Small Glowing Shard (Kleiner leuchtender Splitter) | 11138 | 75s 99c | 14s 73c | 14s 75c | 14s 75c (1) | 369 | 14g 73s | -81 % | ja |
| Small Radiant Shard (Kleiner strahlender Splitter) | 11177 | 7g 99s 98c | 10g 1s | 10g 1s | 10g 1s (1) | 37 | nur 37 Stück | +25 % | dünn |
| Soul Dust (Seelenstaub) | 11083 | 7s 21c | 5s 59c | 5s 83c | 5s 83c (1) | 1037 | 5g 59s 87c | -19 % | ja |
| Strange Dust (Seltsamer Staub) | 10940 | 84c | 63c | 65c | 65c (1) | 4716 | 63s 82c | -23 % | ja |
| Thick Leather (Dickes Leder) | 4304 | 35s 79c | 58s 49c | 60s | 60s (1) | 301 | 58g 51s | +68 % | ja |
| Truesilver Rod (Echtsilberrute) | 11144 | 85s | 22s | 22s | 22s (1) | 52 | nur 52 Stück | -74 % | ja |
| Vision Dust (Visionenstaub) | 11137 | 19s 71c | 6s 91c | 6s 95c | 6s 95c (1) | 1850 | 6g 91s | -65 % | ja |

Nicht im Angebot: Arcanite Rod (16206), Illusion Dust (16204).

Spalte «Plan»: «ja» = mit `--eintragen` übernehmbar, «dünn» = bleibt beim AHledger-Preis.

## Im Plan

Noch nicht eingetragen: Der Plan rechnet weiter mit den AHledger-Preisen. Eintragen mit `python3 tools/ah_aus_testlog.py <Testlog> --eintragen`, danach `python3 tools/plan_berufe.py` (offene Entscheidung 17).
