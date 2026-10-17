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
| 2026-10-17 14:37 | ? Horde R2d38 Beta | 51632 | 2940 | 0 | 12 s | Testlog-Datei |  |
| 2026-10-17 15:02 | ? Horde R2d38 Beta | 52363 | 2959 | 0 | 12 s | Testlog-Datei |  |

Insgesamt 6 Scans in `data/preise/ah_eigen.csv`.

## Plan-Gegenstände im letzten Scan (2026-10-17 15:02, ? Horde R2d38 Beta)

Abweichung = 7-Tage-Median gegenüber dem AHledger-Median (Normal Horde US). «nur X Stück»: so viel war im Angebot; «mind.»: mehr Stück als gespeicherte Preisstufen, der Rest ist mit dem höchsten bekannten Preis gerechnet.

| Material | ID | AHledger | Tiefstpreis | Median | 7 Tage (Scans) | Menge | 100 Stück kosten | Abweichung | Plan |
|---|---|---|---|---|---|---|---|---|---|
| Black Pearl (Schwarze Perle) | 7971 | 10g | 5g 99s 89c | 5g 99s 89c | 5g 49s 41c (6) | 14 | nur 14 Stück | -45 % | dünn |
| Crystal Vial (Kristallphiole) | 8925 | 5s | 5s 60c | 5s 60c | 5s 57c (6) | 25 | nur 25 Stück | +11 % | ja |
| Cured Light Hide (Geschmeidiger leichter Balg) | 4231 | – | 1s 47c | 1s 60c | 1s 34c (6) | 373 | 1g 47s 20c | – | ja |
| Cured Medium Hide (Geschmeidiger mittlerer Balg) | 4233 | – | 5s 47c | 5s 49c | 8s 72c (6) | 527 | 5g 47s 88c | – | ja |
| Dark Leather Belt (Dunkler Ledergürtel) | 4249 | – | 8s | 8s | 8s (6) | 136 | 8g | – | ja |
| Deviate Fish (Deviatfisch) | 6522 | – | 7s 97c | 7s 98c | 7s 98c (6) | 598 | 7g 97s 80c | – | ja |
| Dream Dust (Traumstaub) | 11176 | 58s | 25s 47c | 25s 47c | 38s 22c (6) | 514 | 25g 47s | -34 % | ja |
| Embossed Leather Gloves (Geprägte Lederhandschuhe) | 4239 | – | 1s | 1s | 1s 50c (6) | 278 | 1g | – | ja |
| Fine Leather Belt (Feiner Ledergürtel) | 4246 | – | 3s | 3s | 3s (6) | 88 | nur 88 Stück | – | ja |
| Golden Pearl (Goldene Perle) | 13926 | 5g | 1g 44s | 1g 44s | 1g 74s 50c (6) | 14 | nur 14 Stück | -65 % | dünn |
| Golden Rod (Goldrute) | 11128 | 8s | 1g | 1g 99s | 1g 7s (6) | 150 | 153g 79s | +1238 % | ja |
| Greater Astral Essence (Große Astralessenz) | 11082 | 28s 54c | 44s 47c | 46s 50c | 39s 25c (6) | 435 | 44g 47s | +38 % | ja |
| Greater Eternal Essence (Große ewige Essenz) | 16203 | – | 4g | 4g | 4g (6) | 7 | nur 7 Stück | – | dünn |
| Greater Magic Essence (Große Magieessenz) | 10939 | 1s 96c | 99c | 1s 15c | 1s 35c (6) | 1067 | 99s 56c | -31 % | ja |
| Greater Magic Wand (Großer Magiezauberstab) | 11288 | – | 3s | 3s | 3s (4) | 167 | 3g | – | ja |
| Greater Mystic Essence (Große Mystikeressenz) | 11135 | 44s | 1g 59s 88c | 1g 59s 88c | 88s 44c (6) | 610 | 159g 88s | +101 % | ja |
| Greater Nether Essence (Große Netheressenz) | 11175 | 8g | 14g 99s 99c | 14g 99s 99c | 12g 49s 97c (6) | 66 | nur 66 Stück | +56 % | ja |
| Heavy Hide (Schwerer Balg) | 4235 | 35s 40c | 23s 45c | 26s 50c | 28s 75c (6) | 153 | 24g 97s 27c | -19 % | ja |
| Heavy Leather (Schweres Leder) | 4234 | 11s 98c | 11s | 11s | 8s 80c (6) | 262 | 11g | -27 % | ja |
| Hillman's Leather Gloves (Lederhandschuhe des Hügelwächters) | 4247 | – | 14s | 15s | 22s 50c (6) | 101 | 15g 15s | – | ja |
| Iridescent Pearl (Schillernde Perle) | 5500 | 3g 4s 50c | 93s 79c | 98s 85c | 1g 19s 43c (6) | 53 | nur 53 Stück | -61 % | ja |
| Large Brilliant Shard (Großer glänzender Splitter) | 14344 | – | 18g 1s | 18g 1s | 18g 67s 49c (6) | 6 | nur 6 Stück | – | dünn |
| Large Glimmering Shard (Großer gleißender Splitter) | 11084 | 78s 99c | 84s 98c | 84s 98c | 91s 98c (6) | 267 | 84g 98s | +16 % | ja |
| Large Glowing Shard (Großer leuchtender Splitter) | 11139 | 7g | 3g 20s 90c | 4g | 5g 99s (6) | 59 | nur 59 Stück | -14 % | ja |
| Large Radiant Shard (Großer strahlender Splitter) | 11178 | 11g 49s | 28g | 28g | 25g (6) | 13 | nur 13 Stück | +118 % | ja |
| Lesser Astral Essence (Geringe Astralessenz) | 10998 | 6s 4c | 8s 90c | 8s 90c | 9s 36c (6) | 17 | nur 17 Stück | +55 % | ja |
| Lesser Eternal Essence (Geringe ewige Essenz) | 16202 | 2g | 1g 0s 99c | 1g 0s 99c | 1g 9s 99c (6) | 21 | nur 21 Stück | -45 % | dünn |
| Lesser Magic Essence (Geringe Magieessenz) | 10938 | 69c | 75c | 77c | 84c (6) | 1020 | 75s 32c | +22 % | ja |
| Lesser Magic Wand (Geringer Magiezauberstab) | 11287 | – | 3s | 5s | 5s (4) | 211 | 4g 88s | – | ja |
| Lesser Mystic Essence (Geringe Mystikeressenz) | 11134 | 15s 96c | 33s 98c | 34s 98c | 21s 98c (6) | 733 | 34g 94s | +38 % | ja |
| Lesser Nether Essence (Geringe Netheressenz) | 11174 | 2g 68s 98c | 3g 80s 99c | 6g 39s | 3g 68s 78c (6) | 101 | 565g 13s 71c | +37 % | ja |
| Light Armor Kit (Leichtes Rüstungsset) | 2304 | – | 15c | 16c | 26c (6) | 465 | 15s | – | ja |
| Light Hide (Leichter Balg) | 783 | 69c | 70c | 73c | 73c (6) | 448 | 72s 22c | +6 % | ja |
| Light Leather (Leichtes Leder) | 2318 | 50c | 78c | 89c | 85c (6) | 4443 | 78s 28c | +70 % | ja |
| Light Leather Pants (Leichte Lederhose) | 7282 | – | 6s | 6s | 6s (6) | 60 | nur 60 Stück | – | ja |
| Medium Hide (Mittlerer Balg) | 4232 | 8s 88c | 4s 10c | 4s 73c | 6s 32c (6) | 516 | 4g 11s 60c | -29 % | ja |
| Medium Leather (Mittleres Leder) | 2319 | 1s 91c | 1s 90c | 2s 79c | 2s 54c (6) | 5220 | 1g 90s | +33 % | ja |
| Purple Lotus (Lila Lotus) | 8831 | 20g 5s | 30s 97c | 30s 98c | 29s 99c (6) | 63 | nur 63 Stück | -99 % | ja |
| Rugged Leather (Unverwüstliches Leder) | 8170 | 19s 2c | 5s | 5s | 5s 50c (6) | 161 | 5g 7s 84c | -71 % | ja |
| Ruined Leather Scraps (Verdorbene Lederfetzen) | 2934 | 25c | 14c | 29c | 29c (6) | 3622 | 14s | +16 % | ja |
| Shadowgem (Schattenedelstein) | 1210 | 3s 14c | 2s 70c | 3s | 2s 82c (6) | 365 | 2g 83s 97c | -10 % | ja |
| Silver Rod (Silberrute) | 6338 | 19s | 6s | 7s | 11s (6) | 104 | 9g 17s | -42 % | ja |
| Small Brilliant Shard (Kleiner glänzender Splitter) | 14343 | 4g 88s | 2g 1s | 2g 1s | 2g 37s 50c (6) | 1 | nur 1 Stück | -51 % | dünn |
| Small Glimmering Shard (Kleiner gleißender Splitter) | 10978 | 3s 66c | 3s | 3s 19c | 2s 7c (6) | 866 | 3g 18s 24c | -43 % | ja |
| Small Glowing Shard (Kleiner leuchtender Splitter) | 11138 | 75s 99c | 17s 93c | 18s 99c | 16s 87c (6) | 312 | 18g 6s 19c | -78 % | ja |
| Small Radiant Shard (Kleiner strahlender Splitter) | 11177 | 7g 99s 98c | 16g 90s 99c | 17g 99s 99c | 14g 0s 49c (6) | 30 | nur 30 Stück | +75 % | dünn |
| Soul Dust (Seelenstaub) | 11083 | 7s 21c | 4s 92c | 5s | 5s 42c (6) | 1777 | 4g 92s | -25 % | ja |
| Strange Dust (Seltsamer Staub) | 10940 | 84c | 33c | 38c | 52c (6) | 3887 | 33s | -39 % | ja |
| Thick Leather (Dickes Leder) | 4304 | 35s 79c | 52s 99c | 54s | 57s 22c (6) | 635 | 52g 99s | +60 % | ja |
| Truesilver Rod (Echtsilberrute) | 11144 | 85s | 1g 17s | 1g 18s | 70s (6) | 56 | nur 56 Stück | -18 % | dünn |
| Vision Dust (Visionenstaub) | 11137 | 19s 71c | 9s | 14s 99c | 9s 47c (6) | 981 | 9g 72s 27c | -52 % | ja |

Nicht im Angebot: Arcanite Rod (16206), Illusion Dust (16204).

## Abnahme (Testlog 3.6)

Schätzung der Käufe zwischen zwei Scans: Von den billigsten Angeboten des Scans davor fehlt, was bis dahin nicht ablaufen konnte (Restlaufzeit-Band länger als der Abstand), von unten bis zur ersten Preisstufe, auf der noch etwas liegt, abzüglich neuer Angebote bis zu diesem Preis. «weg» enthält auch zurückgezogene Angebote. Annahme: Käufer nehmen die billigsten zuerst (so verkauft der Server Waren). Zu hoch, wenn jemand zurückzieht und teurer neu einstellt; zu tief, wenn neue Angebote dazukommen. Ganz verschwundene Gegenstände zählen nicht. 7 Tage bis zum letzten Vergleich, gleicher Markt; Werte in `data/preise/ah_abnahme.csv`.

| Gegenstand | ID | geschätzt gekauft | weg | beobachtet | Vergleiche | pro Stunde |
|---|---|---|---|---|---|---|
| Light Leather | 2318 | 1029 | 1180 | 1.4 h | 2 | 714.6 |
| Strange Dust | 10940 | 612 | 612 | 1.4 h | 2 | 425.0 |
| Heavy Leather | 4234 | 535 | 609 | 1.4 h | 2 | 371.5 |
| Vision Dust | 11137 | 306 | 333 | 1.4 h | 2 | 212.5 |
| Wilddornrose | 2450 | 203 | 479 | 1.4 h | 2 | 141.0 |
| Deviate Fish | 6522 | 183 | 203 | 1.4 h | 2 | 127.1 |
| Leinenstoffballen | 2996 | 182 | 335 | 1.4 h | 2 | 126.4 |
| Small Glimmering Shard | 10978 | 136 | 520 | 1.0 h | 1 | 133.3 |
| Roher Langzahniger Matschschnapper | 6289 | 133 | 133 | 1.4 h | 2 | 92.4 |
| Flitzdistel | 2452 | 107 | 223 | 1.4 h | 2 | 74.3 |
| Roher Weisenfisch | 21071 | 104 | 104 | 1.0 h | 1 | 102.0 |
| Friedensblume | 2447 | 85 | 85 | 1.4 h | 2 | 59.0 |
| Brocken Eberfleisch | 769 | 67 | 93 | 1.4 h | 2 | 46.5 |
| Lesser Nether Essence | 11174 | 64 | 64 | 1.4 h | 2 | 44.4 |
| Ruined Leather Scraps | 2934 | 60 | 60 | 1.4 h | 2 | 41.7 |
| Heavy Hide | 4235 | 55 | 69 | 1.4 h | 2 | 38.2 |
| Lesser Astral Essence | 10998 | 46 | 46 | 1.4 h | 2 | 31.9 |
| Roher glänzender Kleinfisch | 6291 | 41 | 41 | 1.4 h | 2 | 28.5 |
| Large Radiant Shard | 11178 | 35 | 49 | 1.4 h | 2 | 24.3 |
| Hillman's Leather Gloves | 4247 | 29 | 29 | 1.4 h | 2 | 20.1 |
| Cured Medium Hide | 4233 | 27 | 30 | 1.4 h | 2 | 18.8 |
| Erdwurzel | 2449 | 23 | 76 | 1.4 h | 2 | 16.0 |
| Rugged Leather | 8170 | 18 | 18 | 1.4 h | 2 | 12.5 |
| Large Glowing Shard | 11139 | 18 | 18 | 1.4 h | 2 | 12.5 |
| Fine Leather Belt | 4246 | 16 | 21 | 1.4 h | 2 | 11.1 |
| Königsblut | 3356 | 15 | 15 | 1.4 h | 2 | 10.4 |
| Large Glimmering Shard | 11084 | 13 | 13 | 1.4 h | 2 | 9.0 |
| Mystisches mittleres Rüstungsset | 252436 | 13 | 13 | 1.4 h | 2 | 9.0 |
| Lagerstuhl | 279979 | 12 | 12 | 1.4 h | 2 | 8.3 |
| Schwacher Manatrank | 2455 | 11 | 39 | 1.4 h | 2 | 7.6 |
| Silver Rod | 6338 | 10 | 10 | 1.4 h | 2 | 6.9 |
| Leichte Lederarmschienen | 7281 | 10 | 10 | 1.4 h | 2 | 6.9 |
| Lesser Magic Wand | 11287 | 10 | 28 | 1.4 h | 2 | 6.9 |
| Geprägte Lederhose | 4242 | 7 | 7 | 1.0 h | 1 | 6.9 |
| Einfaches Lagerfeuerset | 279981 | 6 | 6 | 1.4 h | 2 | 4.2 |
| Milde Gewürze | 2678 | 5 | 5 | 1.4 h | 2 | 3.5 |
| Feine Ledertunika | 4243 | 5 | 5 | 1.4 h | 2 | 3.5 |
| Leichter Lederköcher | 7278 | 5 | 5 | 1.4 h | 2 | 3.5 |
| Handgenähter Ledergürtel | 4237 | 4 | 5 | 1.4 h | 2 | 2.8 |
| Schwarzwelpenschuppe | 7286 | 4 | 4 | 1.0 h | 1 | 3.9 |
| Greater Magic Wand | 11288 | 4 | 4 | 1.4 h | 2 | 2.8 |
| Geprägte Lederweste | 2300 | 3 | 3 | 1.4 h | 2 | 2.1 |
| Schleimige Murlocschuppe | 5784 | 3 | 11 | 1.4 h | 2 | 2.1 |
| Small Radiant Shard | 11177 | 3 | 3 | 1.4 h | 2 | 2.1 |
| Feiner Lederumhang | 2308 | 2 | 2 | 1.4 h | 2 | 1.4 |
| Mote of Magic | 247786 | 2 | 2 | 1.4 h | 2 | 1.4 |
| Handgenähte Lederhose | 2303 | 1 | 1 | 1.4 h | 2 | 0.7 |
| Gray Dye | 4340 | 1 | 1 | 1.4 h | 2 | 0.7 |
| Black Pearl | 7971 | 1 | 1 | 1.0 h | 1 | 1.0 |
| Lesser Eternal Essence | 16202 | 1 | 1 | 1.4 h | 2 | 0.7 |
| Gewöhnliche Kräutersamen | 268415 | 1 | 1 | 1.4 h | 2 | 0.7 |
| Silberblatt | 765 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Light Hide | 783 | 0 | 7 | 1.4 h | 2 | 0.0 |
| Maguskönigskraut | 785 | 0 | 126 | 1.4 h | 2 | 0.0 |
| Shadowgem | 1210 | 0 | 17 | 1.4 h | 2 | 0.0 |
| Handgenähte Lederstiefel | 2302 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Light Armor Kit | 2304 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Geprägte Lederstiefel | 2309 | 0 | 3 | 1.4 h | 2 | 0.0 |
| Geprägter Lederumhang | 2310 | 0 | 0 | 0.4 h | 1 | 0.0 |
| Mittleres Rüstungsset | 2313 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Gekräftigte Lederrüstung | 2314 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Graue Lederstiefel | 2315 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Dunkler Lederumhang | 2316 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Medium Leather | 2319 | 0 | 367 | 1.4 h | 2 | 0.0 |
| Coarse Thread | 2320 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Fine Thread | 2321 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Black Dye | 2325 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Beulengras | 2453 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Elixier der schwachen Stärke | 2454 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Elixier der schwachen Beweglichkeit | 2457 | 0 | 24 | 1.4 h | 2 | 0.0 |
| Leinenumhang | 2570 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Leinenstoff | 2589 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Sehniges Wolfsfleisch | 2672 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Verkohltes Wolfsfleisch | 2679 | 0 | 10 | 1.4 h | 2 | 0.0 |
| Geröstetes Eberfleisch | 2681 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Leere Phiole | 3371 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Verbleite Phiole | 3372 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Cured Light Hide | 4231 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Medium Hide | 4232 | 0 | 6 | 1.4 h | 2 | 0.0 |
| Leinentasche | 4238 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Embossed Leather Gloves | 4239 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Dark Leather Belt | 4249 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Schultern des Hügelwächters | 4251 | 0 | 0 | 0.4 h | 1 | 0.0 |
| Salt | 4289 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Silken Thread | 4291 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Thick Leather | 4304 | 0 | 8 | 1.4 h | 2 | 0.0 |
| Braunes Leinenhemd | 4344 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Simple Wood | 4470 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Lange Schwanzfeder | 5116 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Kleine irisierende Perle | 5498 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Iridescent Pearl | 5500 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Handgenähte Lederweste | 5957 | 0 | 0 | 0.4 h | 1 | 0.0 |
| Dunkle Lederhose | 5961 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Barbarische Schultern | 5964 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Wächterhandschuhe | 5966 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Copper Rod | 6217 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Roher Stoppelfühlerwels | 6308 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Formula: Enchant 2H Weapon - Lesser Intellect | 6349 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Feuerflossenschnapper | 6359 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Glänzendes Schmuckstück | 6529 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Nachtkriecher | 6530 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Rezept: Pikantes Deviat-Supreme | 6661 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Kräutergebackenes Ei | 6888 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Kleines Ei | 6889 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Handgenähter Lederumhang | 7276 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Handgenähte Armschienen | 7277 | 0 | 0 | 0.4 h | 1 | 0.0 |
| Kleiner Ledermunitionsbeutel | 7279 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Light Leather Pants | 7282 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Behände Lederhandschuhe | 7285 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Pfeilmacher-Handschuhe | 7348 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Purple Lotus | 8831 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Crystal Vial | 8925 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Lesser Magic Essence | 10938 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Greater Magic Essence | 10939 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Greater Astral Essence | 11082 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Soul Dust | 11083 | 0 | 13 | 1.4 h | 2 | 0.0 |
| Golden Rod | 11128 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Lesser Mystic Essence | 11134 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Greater Mystic Essence | 11135 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Small Glowing Shard | 11138 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Truesilver Rod | 11144 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Greater Nether Essence | 11175 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Dream Dust | 11176 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Golden Pearl | 13926 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Small Brilliant Shard | 14343 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Large Brilliant Shard | 14344 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Greater Eternal Essence | 16203 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Ahornsamenkorn | 17034 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Schwaches Zauberöl | 20744 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Formel: Schwaches Zauberöl | 20758 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Übungszauberstab des Novizen | 247789 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Gekräuselte Flechte | 249399 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Kraftvolles mittleres Rüstungsset | 252437 | 0 | 75 | 1.4 h | 2 | 0.0 |
| Ungewöhnliche Kräutersamen | 268416 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Verzauberte Laute | 279976 | 0 | 2 | 1.0 h | 1 | 0.0 |
| Lagerzelt | 279978 | 0 | 0 | 1.4 h | 2 | 0.0 |
| Arkaner Wiederverwerter | 279985 | 0 | 0 | 1.4 h | 2 | 0.0 |

## Unter dem Händlerpreis (Testlog 3.7, Scan 2026-10-17 15:02)

Angebote, deren Preis pro Stück unter dem liegt, was der Händler zahlt (`C_Item.GetItemInfo`, «sellPrice», nur Gegenstände, deren Daten der Client schon hatte). Kaufen und beim Händler verkaufen; keine AH-Gebühr. Gewinn = Händlerpreis × Stück − Kaufpreis.

| Gegenstand | ID | Händler zahlt | Stück darunter | kosten | Gewinn |
|---|---|---|---|---|---|
| 14048 | 14048 | 20s | 1 | 17s | 3s |
| 1529 | 1529 | 7s | 2 | 12s | 2s |
| 1251 | 1251 | 10c | 46 | 3s 68c | 92c |
| Lange Schwanzfeder | 5116 | 3s 3c | 30 | 90s | 90c |
| 5635 | 5635 | 45c | 19 | 8s 36c | 19c |
| Geringer Mondstein | 1705 | 6s | 2 | 11s 90c | 10c |

Spalte «Plan»: «ja» = mit `--eintragen` übernehmbar, «dünn» = bleibt beim AHledger-Preis.

## Im Plan

Noch nicht eingetragen: Der Plan rechnet weiter mit den AHledger-Preisen. Eintragen mit `python3 tools/ah_aus_testlog.py <Testlog> --eintragen`, danach `python3 tools/plan_berufe.py` (offene Entscheidung 17).
