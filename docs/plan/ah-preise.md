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
| 2026-10-17 16:51 | ? Horde R2d38 Beta | 53001 | 2903 | 0 | 12 s | Testlog-Datei |  |
| 2026-10-17 17:52 | ? Horde R2d38 Beta | 53688 | 2899 | 0 | 14 s | Testlog-Datei |  |

Insgesamt 8 Scans in `data/preise/ah_eigen.csv`.

## Plan-Gegenstände im letzten Scan (2026-10-17 17:52, ? Horde R2d38 Beta)

Abweichung = 7-Tage-Median gegenüber dem AHledger-Median (Normal Horde US). «nur X Stück»: so viel war im Angebot; «mind.»: mehr Stück als gespeicherte Preisstufen, der Rest ist mit dem höchsten bekannten Preis gerechnet.

| Material | ID | AHledger | Tiefstpreis | Median | 7 Tage (Scans) | Menge | 100 Stück kosten | Abweichung | Plan |
|---|---|---|---|---|---|---|---|---|---|
| Black Pearl (Schwarze Perle) | 7971 | 10g | 5g 99s 87c | 5g 99s 87c | 5g 99s 88c (8) | 16 | nur 16 Stück | -40 % | dünn |
| Crystal Vial (Kristallphiole) | 8925 | 5s | 5s 55c | 5s 55c | 5s 57c (8) | 10 | nur 10 Stück | +11 % | dünn |
| Cured Light Hide (Geschmeidiger leichter Balg) | 4231 | – | 1s 47c | 1s 53c | 1s 50c (8) | 353 | 1g 47s | – | ja |
| Cured Medium Hide (Geschmeidiger mittlerer Balg) | 4233 | – | 7s 6c | 7s 20c | 7s 22c (8) | 636 | 7g 6s | – | ja |
| Dark Leather Belt (Dunkler Ledergürtel) | 4249 | – | 8s | 8s | 8s (8) | 122 | 8g | – | ja |
| Deviate Fish (Deviatfisch) | 6522 | – | 7s 98c | 10s 49c | 7s 98c (8) | 294 | 7g 98s 2c | – | ja |
| Dream Dust (Traumstaub) | 11176 | 58s | 25s 47c | 25s 47c | 25s 47c (8) | 663 | 25g 47s | -56 % | ja |
| Embossed Leather Gloves (Geprägte Lederhandschuhe) | 4239 | – | 1s | 1s | 1s (8) | 292 | 1g | – | ja |
| Fine Leather Belt (Feiner Ledergürtel) | 4246 | – | 3s | 3s | 3s (8) | 103 | 3g | – | ja |
| Golden Pearl (Goldene Perle) | 13926 | 5g | 10g | 20g | 1g 99s (8) | 29 | nur 29 Stück | -60 % | dünn |
| Golden Rod (Goldrute) | 11128 | 8s | 50s | 1g 99s | 1g 74s 50c (8) | 148 | 144g 34s | +2081 % | ja |
| Greater Astral Essence (Große Astralessenz) | 11082 | 28s 54c | 40s 47c | 44s 47c | 44s 47c (8) | 437 | 40g 47s | +56 % | ja |
| Greater Eternal Essence (Große ewige Essenz) | 16203 | – | 4g | 4g | 4g (8) | 6 | nur 6 Stück | – | dünn |
| Greater Magic Essence (Große Magieessenz) | 10939 | 1s 96c | 1s | 1s | 1s 20c (8) | 692 | 1g | -39 % | ja |
| Greater Magic Wand (Großer Magiezauberstab) | 11288 | – | 3s | 3s | 3s (6) | 172 | 3g | – | ja |
| Greater Mystic Essence (Große Mystikeressenz) | 11135 | 44s | 1g 59s 79c | 1g 59s 80c | 1g 59s 84c (8) | 713 | 159g 79s 27c | +263 % | ja |
| Greater Nether Essence (Große Netheressenz) | 11175 | 8g | 14g 99s 99c | 14g 99s 99c | 14g 99s 99c (8) | 71 | nur 71 Stück | +87 % | ja |
| Heavy Hide (Schwerer Balg) | 4235 | 35s 40c | 36s 97c | 36s 98c | 33s 99c (8) | 189 | 36g 97s 95c | -4 % | ja |
| Heavy Leather (Schweres Leder) | 4234 | 11s 98c | 10s 28c | 10s 30c | 9s 65c (8) | 781 | 10g 28s | -19 % | ja |
| Hillman's Leather Gloves (Lederhandschuhe des Hügelwächters) | 4247 | – | 15s | 15s | 15s (8) | 56 | nur 56 Stück | – | ja |
| Iridescent Pearl (Schillernde Perle) | 5500 | 3g 4s 50c | 95s 79c | 1g 10s 87c | 1g 5s 36c (8) | 30 | nur 30 Stück | -65 % | ja |
| Large Brilliant Shard (Großer glänzender Splitter) | 14344 | – | 18g 1s | 18g 1s | 18g 1s (8) | 6 | nur 6 Stück | – | dünn |
| Large Glimmering Shard (Großer gleißender Splitter) | 11084 | 78s 99c | 95s 77c | 95s 77c | 95s 77c (8) | 42 | nur 42 Stück | +21 % | ja |
| Large Glowing Shard (Großer leuchtender Splitter) | 11139 | 7g | 3g 70s 88c | 4g | 4g (8) | 69 | nur 69 Stück | -43 % | ja |
| Large Radiant Shard (Großer strahlender Splitter) | 11178 | 11g 49s | 79g | 79g | 26g 50s (8) | 10 | nur 10 Stück | +131 % | dünn |
| Lesser Astral Essence (Geringe Astralessenz) | 10998 | 6s 4c | 10s | 12s | 9s 83c (8) | 156 | 11g 4s | +63 % | ja |
| Lesser Eternal Essence (Geringe ewige Essenz) | 16202 | 2g | 1g 0s 99c | 1g 0s 99c | 1g 0s 99c (8) | 21 | nur 21 Stück | -50 % | dünn |
| Lesser Magic Essence (Geringe Magieessenz) | 10938 | 69c | 75c | 75c | 77c (8) | 1023 | 75s | +12 % | ja |
| Lesser Magic Wand (Geringer Magiezauberstab) | 11287 | – | 4s | 5s | 5s (6) | 225 | 4g 77s | – | ja |
| Lesser Mystic Essence (Geringe Mystikeressenz) | 11134 | 15s 96c | 29s 98c | 29s 98c | 31s 98c (8) | 768 | 29g 98s | +100 % | ja |
| Lesser Nether Essence (Geringe Netheressenz) | 11174 | 2g 68s 98c | 4g 75s | 4g 75s | 4g 36s 50c (8) | 70 | nur 70 Stück | +62 % | ja |
| Light Armor Kit (Leichtes Rüstungsset) | 2304 | – | 15c | 15c | 17c (8) | 482 | 15s | – | ja |
| Light Hide (Leichter Balg) | 783 | 69c | 67c | 73c | 73c (8) | 451 | 67s 94c | +6 % | ja |
| Light Leather (Leichtes Leder) | 2318 | 50c | 50c | 77c | 85c (8) | 5822 | 50s 67c | +70 % | ja |
| Light Leather Pants (Leichte Lederhose) | 7282 | – | 6s | 6s | 6s (8) | 91 | nur 91 Stück | – | ja |
| Medium Hide (Mittlerer Balg) | 4232 | 8s 88c | 4s 9c | 4s 73c | 4s 73c (8) | 460 | 4g 9s 25c | -47 % | ja |
| Medium Leather (Mittleres Leder) | 2319 | 1s 91c | 2s 10c | 2s 79c | 2s 79c (8) | 4127 | 2g 10s | +46 % | ja |
| Purple Lotus (Lila Lotus) | 8831 | 20g 5s | 25s 98c | 33s | 30s 98c (8) | 41 | nur 41 Stück | -98 % | ja |
| Rugged Leather (Unverwüstliches Leder) | 8170 | 19s 2c | 5s | 5s | 5s 49c (8) | 279 | 5g | -71 % | ja |
| Ruined Leather Scraps (Verdorbene Lederfetzen) | 2934 | 25c | 18c | 25c | 29c (8) | 3392 | 18s 38c | +16 % | ja |
| Shadowgem (Schattenedelstein) | 1210 | 3s 14c | 2s 60c | 2s 89c | 2s 89c (8) | 400 | 2g 69s 70c | -8 % | ja |
| Silver Rod (Silberrute) | 6338 | 19s | 4s | 6s | 7s (8) | 59 | nur 59 Stück | -63 % | ja |
| Small Brilliant Shard (Kleiner glänzender Splitter) | 14343 | 4g 88s | 2g 1s | 2g 1s | 2g 1s (8) | 1 | nur 1 Stück | -59 % | dünn |
| Small Glimmering Shard (Kleiner gleißender Splitter) | 10978 | 3s 66c | 2s | 2s | 2s 7c (8) | 317 | 2g | -43 % | ja |
| Small Glowing Shard (Kleiner leuchtender Splitter) | 11138 | 75s 99c | 14s 99c | 17s 95c | 17s 95c (8) | 451 | 15g 41s 61c | -76 % | ja |
| Small Radiant Shard (Kleiner strahlender Splitter) | 11177 | 7g 99s 98c | 19g 99s 99c | 19g 99s 99c | 17g 99s 98c (8) | 11 | nur 11 Stück | +125 % | dünn |
| Soul Dust (Seelenstaub) | 11083 | 7s 21c | 4s 92c | 5s | 5s (8) | 1125 | 4g 92s | -31 % | ja |
| Strange Dust (Seltsamer Staub) | 10940 | 84c | 33c | 38c | 38c (8) | 4049 | 33s | -55 % | ja |
| Thick Leather (Dickes Leder) | 4304 | 35s 79c | 49s | 52s 99c | 55s 48c (8) | 754 | 49g | +55 % | ja |
| Truesilver Rod (Echtsilberrute) | 11144 | 85s | 1g 17s | 1g 17s | 1g 17s (8) | 31 | nur 31 Stück | +38 % | dünn |
| Vision Dust (Visionenstaub) | 11137 | 19s 71c | 23s 86c | 23s 86c | 13s 49c (8) | 798 | 23g 86s | -32 % | ja |

Nicht im Angebot: Arcanite Rod (16206), Illusion Dust (16204).

## Abnahme (Testlog 3.6)

Schätzung der Käufe zwischen zwei Scans: Von den billigsten Angeboten des Scans davor fehlt, was bis dahin nicht ablaufen konnte (Restlaufzeit-Band länger als der Abstand), von unten bis zur ersten Preisstufe, auf der noch etwas liegt, abzüglich neuer Angebote bis zu diesem Preis. «weg» enthält auch zurückgezogene Angebote. Annahme: Käufer nehmen die billigsten zuerst (so verkauft der Server Waren). Zu hoch, wenn jemand zurückzieht und teurer neu einstellt; zu tief, wenn neue Angebote dazukommen. Ganz verschwundene Gegenstände zählen nicht. 7 Tage bis zum letzten Vergleich, gleicher Markt; Werte in `data/preise/ah_abnahme.csv`.

| Gegenstand | ID | geschätzt gekauft | weg | beobachtet | Vergleiche | pro Stunde |
|---|---|---|---|---|---|---|
| Light Leather | 2318 | 1029 | 1446 | 4.3 h | 4 | 241.5 |
| Vision Dust | 11137 | 820 | 1049 | 4.3 h | 4 | 192.5 |
| Friedensblume | 2447 | 692 | 692 | 4.3 h | 4 | 162.4 |
| Strange Dust | 10940 | 612 | 612 | 4.3 h | 4 | 143.7 |
| Erdwurzel | 2449 | 559 | 771 | 4.3 h | 4 | 131.2 |
| Heavy Leather | 4234 | 535 | 757 | 4.3 h | 4 | 125.6 |
| Roher Langzahniger Matschschnapper | 6289 | 512 | 512 | 4.3 h | 4 | 120.2 |
| Medium Leather | 2319 | 487 | 924 | 4.3 h | 4 | 114.3 |
| Deviate Fish | 6522 | 426 | 446 | 4.3 h | 4 | 100.0 |
| Königsblut | 3356 | 377 | 482 | 4.3 h | 4 | 88.5 |
| Soul Dust | 11083 | 353 | 366 | 4.3 h | 4 | 82.9 |
| Large Glimmering Shard | 11084 | 229 | 229 | 4.3 h | 4 | 53.8 |
| Sehniges Wolfsfleisch | 2672 | 206 | 241 | 4.3 h | 4 | 48.4 |
| Wilddornrose | 2450 | 203 | 1027 | 4.3 h | 4 | 47.7 |
| Lesser Astral Essence | 10998 | 197 | 301 | 2.5 h | 3 | 80.4 |
| Milde Gewürze | 2678 | 193 | 193 | 4.3 h | 4 | 45.3 |
| Leinenstoffballen | 2996 | 182 | 371 | 4.3 h | 4 | 42.7 |
| Simple Wood | 4470 | 177 | 238 | 4.3 h | 4 | 41.5 |
| Roher glänzender Kleinfisch | 6291 | 173 | 173 | 4.3 h | 4 | 40.6 |
| Silberblatt | 765 | 169 | 184 | 4.3 h | 4 | 39.7 |
| Ruined Leather Scraps | 2934 | 165 | 1239 | 4.3 h | 4 | 38.7 |
| Roher Weisenfisch | 21071 | 141 | 151 | 3.8 h | 3 | 36.7 |
| Small Glimmering Shard | 10978 | 136 | 520 | 3.8 h | 3 | 35.4 |
| Salt | 4289 | 133 | 133 | 4.3 h | 4 | 31.2 |
| Flitzdistel | 2452 | 107 | 226 | 4.3 h | 4 | 25.1 |
| Heavy Hide | 4235 | 87 | 147 | 4.3 h | 4 | 20.4 |
| Cured Light Hide | 4231 | 74 | 74 | 4.3 h | 4 | 17.4 |
| Medium Hide | 4232 | 68 | 131 | 4.3 h | 4 | 16.0 |
| Brocken Eberfleisch | 769 | 67 | 319 | 3.2 h | 3 | 20.6 |
| Lesser Nether Essence | 11174 | 64 | 93 | 4.3 h | 4 | 15.0 |
| Maguskönigskraut | 785 | 56 | 408 | 4.3 h | 4 | 13.1 |
| Tigerauge | 818 | 49 | 140 | 2.8 h | 2 | 17.4 |
| Kleines Ei | 6889 | 49 | 49 | 4.3 h | 4 | 11.5 |
| Large Radiant Shard | 11178 | 48 | 67 | 4.3 h | 4 | 11.3 |
| Fine Thread | 2321 | 45 | 148 | 4.3 h | 4 | 10.6 |
| Arkaner Wiederverwerter | 279985 | 42 | 42 | 4.3 h | 4 | 9.9 |
| Rolle der Stärke | 954 | 39 | 52 | 2.8 h | 2 | 13.8 |
| Kleine irisierende Perle | 5498 | 39 | 71 | 4.3 h | 4 | 9.2 |
| Hillman's Leather Gloves | 4247 | 38 | 43 | 4.3 h | 4 | 8.9 |
| Lagerstuhl | 279979 | 36 | 36 | 4.3 h | 4 | 8.5 |
| Mystisches mittleres Rüstungsset | 252436 | 34 | 38 | 4.3 h | 4 | 8.0 |
| Rolle der Beweglichkeit | 3012 | 30 | 30 | 2.8 h | 2 | 10.6 |
| Shadowgem | 1210 | 29 | 49 | 4.3 h | 4 | 6.8 |
| Greater Magic Essence | 10939 | 28 | 171 | 4.3 h | 4 | 6.6 |
| Cured Medium Hide | 4233 | 27 | 81 | 3.2 h | 3 | 8.3 |
| Leichte Lederarmschienen | 7281 | 20 | 20 | 4.3 h | 4 | 4.7 |
| Rugged Leather | 8170 | 18 | 18 | 4.3 h | 4 | 4.2 |
| Large Glowing Shard | 11139 | 18 | 30 | 4.3 h | 4 | 4.2 |
| Iridescent Pearl | 5500 | 17 | 24 | 4.3 h | 4 | 4.0 |
| Lagerzelt | 279978 | 17 | 17 | 4.3 h | 4 | 4.0 |
| Fine Leather Belt | 4246 | 16 | 21 | 4.3 h | 4 | 3.8 |
| Small Radiant Shard | 11177 | 15 | 17 | 4.3 h | 4 | 3.5 |
| Übungszauberstab des Novizen | 247789 | 15 | 15 | 4.3 h | 4 | 3.5 |
| Wächterhandschuhe | 5966 | 13 | 13 | 4.3 h | 4 | 3.1 |
| Schwacher Manatrank | 2455 | 11 | 39 | 4.3 h | 4 | 2.6 |
| Kleiner Ledermunitionsbeutel | 7279 | 11 | 11 | 3.2 h | 3 | 3.4 |
| Golden Pearl | 13926 | 11 | 11 | 4.3 h | 4 | 2.6 |
| Gekräuselte Flechte | 249399 | 11 | 20 | 4.3 h | 4 | 2.6 |
| Silver Rod | 6338 | 10 | 10 | 4.3 h | 4 | 2.3 |
| Lesser Magic Wand | 11287 | 10 | 29 | 4.3 h | 4 | 2.3 |
| Geringer Manatrank | 3385 | 9 | 9 | 2.8 h | 2 | 3.2 |
| Kraftvolles mittleres Rüstungsset | 252437 | 9 | 84 | 4.3 h | 4 | 2.1 |
| Geprägte Lederhose | 4242 | 7 | 7 | 2.0 h | 2 | 3.4 |
| Dark Leather Belt | 4249 | 7 | 7 | 4.3 h | 4 | 1.6 |
| Verbleite Phiole | 3372 | 6 | 6 | 4.3 h | 4 | 1.4 |
| Handgenähter Ledergürtel | 4237 | 6 | 7 | 4.3 h | 4 | 1.4 |
| Einfaches Lagerfeuerset | 279981 | 6 | 6 | 4.3 h | 4 | 1.4 |
| 3396 | 3396 | 5 | 5 | 2.8 h | 2 | 1.8 |
| Feine Ledertunika | 4243 | 5 | 9 | 4.3 h | 4 | 1.2 |
| Leichter Lederköcher | 7278 | 5 | 5 | 4.3 h | 4 | 1.2 |
| Crystal Vial | 8925 | 5 | 15 | 4.3 h | 4 | 1.2 |
| Dunkle Lederhose | 5961 | 4 | 4 | 4.3 h | 4 | 0.9 |
| Schwarzwelpenschuppe | 7286 | 4 | 4 | 1.0 h | 1 | 3.9 |
| Greater Magic Wand | 11288 | 4 | 4 | 4.3 h | 4 | 0.9 |
| Geprägte Lederweste | 2300 | 3 | 3 | 1.4 h | 2 | 2.1 |
| Schleimige Murlocschuppe | 5784 | 3 | 11 | 4.3 h | 4 | 0.7 |
| Purple Lotus | 8831 | 3 | 3 | 4.3 h | 4 | 0.7 |
| 1744 | 1744 | 2 | 3 | 2.8 h | 2 | 0.7 |
| Feiner Lederumhang | 2308 | 2 | 2 | 1.4 h | 2 | 1.4 |
| Lange Schwanzfeder | 5116 | 2 | 28 | 4.3 h | 4 | 0.5 |
| Mote of Magic | 247786 | 2 | 2 | 4.3 h | 4 | 0.5 |
| Gebördelter Streitkolben | 766 | 1 | 1 | 2.8 h | 2 | 0.4 |
| Handgenähte Lederhose | 2303 | 1 | 1 | 4.3 h | 4 | 0.2 |
| Coarse Thread | 2320 | 1 | 1 | 4.3 h | 4 | 0.2 |
| 2987 | 2987 | 1 | 1 | 2.8 h | 2 | 0.4 |
| Hasenpfote | 3300 | 1 | 1 | 2.8 h | 2 | 0.4 |
| Gray Dye | 4340 | 1 | 3 | 4.3 h | 4 | 0.2 |
| Braunes Leinenhemd | 4344 | 1 | 1 | 4.3 h | 4 | 0.2 |
| 4701 | 4701 | 1 | 1 | 2.8 h | 2 | 0.4 |
| Nachtkriecher | 6530 | 1 | 1 | 4.3 h | 4 | 0.2 |
| Black Pearl | 7971 | 1 | 3 | 3.8 h | 3 | 0.3 |
| 14161 | 14161 | 1 | 1 | 2.8 h | 2 | 0.4 |
| Lesser Eternal Essence | 16202 | 1 | 1 | 4.3 h | 4 | 0.2 |
| Greater Eternal Essence | 16203 | 1 | 1 | 4.3 h | 4 | 0.2 |
| Gewöhnliche Kräutersamen | 268415 | 1 | 1 | 4.3 h | 4 | 0.2 |
| Malachit | 774 | 0 | 0 | 2.8 h | 2 | 0.0 |
| Light Hide | 783 | 0 | 7 | 4.3 h | 4 | 0.0 |
| Eiskalte Milch | 1179 | 0 | 0 | 2.8 h | 2 | 0.0 |
| 1206 | 1206 | 0 | 3 | 2.8 h | 2 | 0.0 |
| Geringer Mondstein | 1705 | 0 | 2 | 2.8 h | 2 | 0.0 |
| 1733 | 1733 | 0 | 0 | 2.8 h | 2 | 0.0 |
| 1817 | 1817 | 0 | 0 | 2.8 h | 2 | 0.0 |
| 2287 | 2287 | 0 | 0 | 2.8 h | 2 | 0.0 |
| Handgenähte Lederstiefel | 2302 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Light Armor Kit | 2304 | 0 | 14 | 4.3 h | 4 | 0.0 |
| Geprägte Lederstiefel | 2309 | 0 | 5 | 4.3 h | 4 | 0.0 |
| Geprägter Lederumhang | 2310 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Mittleres Rüstungsset | 2313 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Gekräftigte Lederrüstung | 2314 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Graue Lederstiefel | 2315 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Dunkler Lederumhang | 2316 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Black Dye | 2325 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Beulengras | 2453 | 0 | 322 | 4.3 h | 4 | 0.0 |
| Elixier der schwachen Stärke | 2454 | 0 | 57 | 4.3 h | 4 | 0.0 |
| Elixier der schwachen Beweglichkeit | 2457 | 0 | 24 | 4.3 h | 4 | 0.0 |
| Leinenumhang | 2570 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Leinenstoff | 2589 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Wollstoff | 2592 | 0 | 1142 | 2.8 h | 2 | 0.0 |
| Verkohltes Wolfsfleisch | 2679 | 0 | 10 | 4.3 h | 4 | 0.0 |
| Geröstetes Eberfleisch | 2681 | 0 | 0 | 4.3 h | 4 | 0.0 |
| 3167 | 3167 | 0 | 0 | 2.8 h | 2 | 0.0 |
| Gerissener Eckzahn | 3299 | 0 | 0 | 1.8 h | 1 | 0.0 |
| 3301 | 3301 | 0 | 0 | 2.8 h | 2 | 0.0 |
| Leere Phiole | 3371 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Leinentasche | 4238 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Embossed Leather Gloves | 4239 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Schultern des Hügelwächters | 4251 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Silken Thread | 4291 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Thick Leather | 4304 | 0 | 45 | 4.3 h | 4 | 0.0 |
| Gesprungener Schnabel | 4775 | 0 | 0 | 2.8 h | 2 | 0.0 |
| Gesträubte Feder | 4776 | 0 | 0 | 2.8 h | 2 | 0.0 |
| Bluthornfeder | 5165 | 0 | 0 | 2.8 h | 2 | 0.0 |
| Kodofleisch | 5467 | 0 | 0 | 2.8 h | 2 | 0.0 |
| Handgenähte Lederweste | 5957 | 0 | 3 | 3.2 h | 3 | 0.0 |
| Barbarische Schultern | 5964 | 0 | 2 | 4.3 h | 4 | 0.0 |
| Copper Rod | 6217 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Roher Stoppelfühlerwels | 6308 | 0 | 56 | 4.3 h | 4 | 0.0 |
| Formula: Enchant 2H Weapon - Lesser Intellect | 6349 | 0 | 1 | 4.3 h | 4 | 0.0 |
| Feuerflossenschnapper | 6359 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Glänzendes Schmuckstück | 6529 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Rezept: Pikantes Deviat-Supreme | 6661 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Kräutergebackenes Ei | 6888 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Ausgezupfte Feder | 7096 | 0 | 0 | 1.0 h | 1 | 0.0 |
| Beinfleisch | 7097 | 0 | 0 | 2.8 h | 2 | 0.0 |
| Handgenähter Lederumhang | 7276 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Handgenähte Armschienen | 7277 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Light Leather Pants | 7282 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Behände Lederhandschuhe | 7285 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Pfeilmacher-Handschuhe | 7348 | 0 | 0 | 4.3 h | 4 | 0.0 |
| 7428 | 7428 | 0 | 0 | 2.8 h | 2 | 0.0 |
| Einfache Leinenhose | 10045 | 0 | 0 | 1.0 h | 1 | 0.0 |
| Lesser Magic Essence | 10938 | 0 | 594 | 4.3 h | 4 | 0.0 |
| Greater Astral Essence | 11082 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Golden Rod | 11128 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Lesser Mystic Essence | 11134 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Greater Mystic Essence | 11135 | 0 | 1 | 4.3 h | 4 | 0.0 |
| Small Glowing Shard | 11138 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Truesilver Rod | 11144 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Greater Nether Essence | 11175 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Dream Dust | 11176 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Eingeborenenhose | 14097 | 0 | 0 | 2.8 h | 2 | 0.0 |
| Small Brilliant Shard | 14343 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Large Brilliant Shard | 14344 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Schredderanleitung - Seite 12 | 16656 | 0 | 2 | 2.8 h | 2 | 0.0 |
| Ahornsamenkorn | 17034 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Schwaches Zauberöl | 20744 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Formel: Schwaches Zauberöl | 20758 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Windstein | 255663 | 0 | 0 | 2.8 h | 2 | 0.0 |
| Ungewöhnliche Kräutersamen | 268416 | 0 | 0 | 4.3 h | 4 | 0.0 |
| Fischglas | 279967 | 0 | 0 | 1.0 h | 1 | 0.0 |
| Verzauberte Laute | 279976 | 0 | 2 | 3.8 h | 3 | 0.0 |

Spalte «Plan»: «ja» = mit `--eintragen` übernehmbar, «dünn» = bleibt beim AHledger-Preis.

## Im Plan

Noch nicht eingetragen: Der Plan rechnet weiter mit den AHledger-Preisen. Eintragen mit `python3 tools/ah_aus_testlog.py <Testlog> --eintragen`, danach `python3 tools/plan_berufe.py` (offene Entscheidung 17).
