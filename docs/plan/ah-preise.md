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

Insgesamt 7 Scans in `data/preise/ah_eigen.csv`.

## Plan-Gegenstände im letzten Scan (2026-10-17 16:51, ? Horde R2d38 Beta)

Abweichung = 7-Tage-Median gegenüber dem AHledger-Median (Normal Horde US). «nur X Stück»: so viel war im Angebot; «mind.»: mehr Stück als gespeicherte Preisstufen, der Rest ist mit dem höchsten bekannten Preis gerechnet.

| Material | ID | AHledger | Tiefstpreis | Median | 7 Tage (Scans) | Menge | 100 Stück kosten | Abweichung | Plan |
|---|---|---|---|---|---|---|---|---|---|
| Black Pearl (Schwarze Perle) | 7971 | 10g | 5g 55s 55c | 5g 99s 88c | 5g 99s 88c (7) | 17 | nur 17 Stück | -40 % | dünn |
| Crystal Vial (Kristallphiole) | 8925 | 5s | 5s 60c | 5s 60c | 5s 60c (7) | 20 | nur 20 Stück | +12 % | dünn |
| Cured Light Hide (Geschmeidiger leichter Balg) | 4231 | – | 1s 47c | 1s 47c | 1s 47c (7) | 471 | 1g 47s | – | ja |
| Cured Medium Hide (Geschmeidiger mittlerer Balg) | 4233 | – | 7s 10c | 7s 23c | 7s 23c (7) | 494 | 7g 18s 20c | – | ja |
| Dark Leather Belt (Dunkler Ledergürtel) | 4249 | – | 7s | 8s | 8s (7) | 142 | 7g 93s | – | ja |
| Deviate Fish (Deviatfisch) | 6522 | – | 7s 98c | 7s 98c | 7s 98c (7) | 498 | 7g 98s | – | ja |
| Dream Dust (Traumstaub) | 11176 | 58s | 25s 47c | 25s 47c | 25s 47c (7) | 563 | 25g 47s | -56 % | ja |
| Embossed Leather Gloves (Geprägte Lederhandschuhe) | 4239 | – | 1s | 1s | 1s (7) | 300 | 1g | – | ja |
| Fine Leather Belt (Feiner Ledergürtel) | 4246 | – | 3s | 3s | 3s (7) | 85 | nur 85 Stück | – | ja |
| Golden Pearl (Goldene Perle) | 13926 | 5g | 20g | 20g | 1g 99s (7) | 26 | nur 26 Stück | -60 % | dünn |
| Golden Rod (Goldrute) | 11128 | 8s | 1g | 1g 50s | 1g 50s (7) | 156 | 130g 34s | +1775 % | ja |
| Greater Astral Essence (Große Astralessenz) | 11082 | 28s 54c | 40s 47c | 44s 47c | 44s 47c (7) | 451 | 41g 75s | +56 % | ja |
| Greater Eternal Essence (Große ewige Essenz) | 16203 | – | 4g | 4g | 4g (7) | 7 | nur 7 Stück | – | dünn |
| Greater Magic Essence (Große Magieessenz) | 10939 | 1s 96c | 99c | 1s | 1s 20c (7) | 737 | 99s | -39 % | ja |
| Greater Magic Wand (Großer Magiezauberstab) | 11288 | – | 3s | 3s | 3s (5) | 214 | 3g | – | ja |
| Greater Mystic Essence (Große Mystikeressenz) | 11135 | 44s | 1g 59s 82c | 1g 59s 88c | 1g 59s 88c (7) | 700 | 159g 86s 21c | +263 % | ja |
| Greater Nether Essence (Große Netheressenz) | 11175 | 8g | 14g 99s 99c | 14g 99s 99c | 14g 99s 99c (7) | 53 | nur 53 Stück | +87 % | ja |
| Heavy Hide (Schwerer Balg) | 4235 | 35s 40c | 36s 55c | 44s 48c | 31s (7) | 118 | 43g 69s 25c | -12 % | ja |
| Heavy Leather (Schweres Leder) | 4234 | 11s 98c | 10s 28c | 10s 30c | 9s (7) | 644 | 10g 28s | -25 % | ja |
| Hillman's Leather Gloves (Lederhandschuhe des Hügelwächters) | 4247 | – | 14s | 15s | 15s (7) | 71 | nur 71 Stück | – | ja |
| Iridescent Pearl (Schillernde Perle) | 5500 | 3g 4s 50c | 95s 79c | 98s 85c | 99s 86c (7) | 50 | nur 50 Stück | -67 % | ja |
| Large Brilliant Shard (Großer glänzender Splitter) | 14344 | – | 18g 1s | 18g 1s | 18g 1s (7) | 6 | nur 6 Stück | – | dünn |
| Large Glimmering Shard (Großer gleißender Splitter) | 11084 | 78s 99c | 84s 98c | 95s 77c | 95s 77c (7) | 48 | nur 48 Stück | +21 % | ja |
| Large Glowing Shard (Großer leuchtender Splitter) | 11139 | 7g | 3g 30s 89c | 3g 99s 99c | 4g (7) | 78 | nur 78 Stück | -43 % | ja |
| Large Radiant Shard (Großer strahlender Splitter) | 11178 | 11g 49s | 79g 1s | 79g 1s | 25g (7) | 6 | nur 6 Stück | +118 % | ja |
| Lesser Astral Essence (Geringe Astralessenz) | 10998 | 6s 4c | 13s | 13s | 9s 83c (7) | 334 | 13g | +63 % | ja |
| Lesser Eternal Essence (Geringe ewige Essenz) | 16202 | 2g | 1g 0s 99c | 1g 0s 99c | 1g 0s 99c (7) | 24 | nur 24 Stück | -50 % | dünn |
| Lesser Magic Essence (Geringe Magieessenz) | 10938 | 69c | 77c | 77c | 77c (7) | 758 | 77s | +12 % | ja |
| Lesser Magic Wand (Geringer Magiezauberstab) | 11287 | – | 4s | 5s | 5s (5) | 219 | 4g 84s | – | ja |
| Lesser Mystic Essence (Geringe Mystikeressenz) | 11134 | 15s 96c | 30s 95c | 33s 98c | 33s 98c (7) | 770 | 32g 29s | +113 % | ja |
| Lesser Nether Essence (Geringe Netheressenz) | 11174 | 2g 68s 98c | 4g 75s | 4g 98s | 3g 97s 99c (7) | 90 | nur 90 Stück | +48 % | ja |
| Light Armor Kit (Leichtes Rüstungsset) | 2304 | – | 10c | 15c | 17c (7) | 406 | 14s 30c | – | ja |
| Light Hide (Leichter Balg) | 783 | 69c | 67c | 73c | 73c (7) | 646 | 68s 77c | +6 % | ja |
| Light Leather (Leichtes Leder) | 2318 | 50c | 65c | 85c | 85c (7) | 5997 | 65s | +70 % | ja |
| Light Leather Pants (Leichte Lederhose) | 7282 | – | 6s | 6s | 6s (7) | 69 | nur 69 Stück | – | ja |
| Medium Hide (Mittlerer Balg) | 4232 | 8s 88c | 4s | 4s 50c | 4s 73c (7) | 542 | 4g | -47 % | ja |
| Medium Leather (Mittleres Leder) | 2319 | 1s 91c | 1s 85c | 2s 79c | 2s 79c (7) | 6346 | 1g 85s | +46 % | ja |
| Purple Lotus (Lila Lotus) | 8831 | 20g 5s | 30s 98c | 30s 98c | 30s 98c (7) | 60 | nur 60 Stück | -98 % | ja |
| Rugged Leather (Unverwüstliches Leder) | 8170 | 19s 2c | 5s | 5s | 5s 49c (7) | 272 | 5g | -71 % | ja |
| Ruined Leather Scraps (Verdorbene Lederfetzen) | 2934 | 25c | 20c | 25c | 29c (7) | 4485 | 20s | +16 % | ja |
| Shadowgem (Schattenedelstein) | 1210 | 3s 14c | 2s 70c | 2s 89c | 2s 89c (7) | 514 | 2g 70s | -8 % | ja |
| Silver Rod (Silberrute) | 6338 | 19s | 6s | 7s | 7s (7) | 94 | nur 94 Stück | -63 % | ja |
| Small Brilliant Shard (Kleiner glänzender Splitter) | 14343 | 4g 88s | 2g 1s | 2g 1s | 2g 1s (7) | 1 | nur 1 Stück | -59 % | dünn |
| Small Glimmering Shard (Kleiner gleißender Splitter) | 10978 | 3s 66c | 2s | 3s 19c | 2s 14c (7) | 709 | 2g 64s 60c | -42 % | ja |
| Small Glowing Shard (Kleiner leuchtender Splitter) | 11138 | 75s 99c | 14s 99c | 17s 95c | 17s 95c (7) | 477 | 15g 56s 76c | -76 % | ja |
| Small Radiant Shard (Kleiner strahlender Splitter) | 11177 | 7g 99s 98c | 17g 99s 99c | 17g 99s 99c | 17g 99s 98c (7) | 9 | nur 9 Stück | +125 % | dünn |
| Soul Dust (Seelenstaub) | 11083 | 7s 21c | 4s | 4s 98c | 5s (7) | 1602 | 4g 84s 64c | -31 % | ja |
| Strange Dust (Seltsamer Staub) | 10940 | 84c | 33c | 38c | 38c (7) | 4064 | 33s | -55 % | ja |
| Thick Leather (Dickes Leder) | 4304 | 35s 79c | 48s | 52s 99c | 55s 97c (7) | 817 | 48g 50s 81c | +56 % | ja |
| Truesilver Rod (Echtsilberrute) | 11144 | 85s | 1g 17s | 1g 17s | 1g 17s (7) | 31 | nur 31 Stück | +38 % | dünn |
| Vision Dust (Visionenstaub) | 11137 | 19s 71c | 23s 94c | 25s | 11s 99c (7) | 437 | 23g 96s 79c | -39 % | ja |

Nicht im Angebot: Arcanite Rod (16206), Illusion Dust (16204).

## Abnahme (Testlog 3.6)

Schätzung der Käufe zwischen zwei Scans: Von den billigsten Angeboten des Scans davor fehlt, was bis dahin nicht ablaufen konnte (Restlaufzeit-Band länger als der Abstand), von unten bis zur ersten Preisstufe, auf der noch etwas liegt, abzüglich neuer Angebote bis zu diesem Preis. «weg» enthält auch zurückgezogene Angebote. Annahme: Käufer nehmen die billigsten zuerst (so verkauft der Server Waren). Zu hoch, wenn jemand zurückzieht und teurer neu einstellt; zu tief, wenn neue Angebote dazukommen. Ganz verschwundene Gegenstände zählen nicht. 7 Tage bis zum letzten Vergleich, gleicher Markt; Werte in `data/preise/ah_abnahme.csv`.

| Gegenstand | ID | geschätzt gekauft | weg | beobachtet | Vergleiche | pro Stunde |
|---|---|---|---|---|---|---|
| Light Leather | 2318 | 1029 | 1387 | 3.2 h | 3 | 316.6 |
| Vision Dust | 11137 | 820 | 1037 | 3.2 h | 3 | 252.3 |
| Friedensblume | 2447 | 661 | 661 | 3.2 h | 3 | 203.4 |
| Strange Dust | 10940 | 612 | 612 | 3.2 h | 3 | 188.3 |
| Heavy Leather | 4234 | 535 | 757 | 3.2 h | 3 | 164.6 |
| Roher Langzahniger Matschschnapper | 6289 | 512 | 512 | 3.2 h | 3 | 157.5 |
| Erdwurzel | 2449 | 462 | 674 | 3.2 h | 3 | 142.2 |
| Königsblut | 3356 | 377 | 417 | 3.2 h | 3 | 116.0 |
| Deviate Fish | 6522 | 283 | 303 | 3.2 h | 3 | 87.1 |
| Large Glimmering Shard | 11084 | 223 | 223 | 3.2 h | 3 | 68.6 |
| Sehniges Wolfsfleisch | 2672 | 206 | 206 | 3.2 h | 3 | 63.4 |
| Wilddornrose | 2450 | 203 | 1027 | 3.2 h | 3 | 62.5 |
| Milde Gewürze | 2678 | 193 | 193 | 3.2 h | 3 | 59.4 |
| Leinenstoffballen | 2996 | 182 | 371 | 3.2 h | 3 | 56.0 |
| Simple Wood | 4470 | 177 | 227 | 3.2 h | 3 | 54.5 |
| Roher glänzender Kleinfisch | 6291 | 173 | 173 | 3.2 h | 3 | 53.2 |
| Silberblatt | 765 | 154 | 169 | 3.2 h | 3 | 47.4 |
| Roher Weisenfisch | 21071 | 141 | 141 | 2.8 h | 2 | 49.8 |
| Small Glimmering Shard | 10978 | 136 | 520 | 2.8 h | 2 | 48.1 |
| Flitzdistel | 2452 | 107 | 226 | 3.2 h | 3 | 32.9 |
| Heavy Hide | 4235 | 87 | 128 | 3.2 h | 3 | 26.8 |
| Brocken Eberfleisch | 769 | 67 | 319 | 3.2 h | 3 | 20.6 |
| Lesser Nether Essence | 11174 | 64 | 93 | 3.2 h | 3 | 19.7 |
| Ruined Leather Scraps | 2934 | 60 | 518 | 3.2 h | 3 | 18.5 |
| Maguskönigskraut | 785 | 56 | 366 | 3.2 h | 3 | 17.2 |
| Large Radiant Shard | 11178 | 48 | 62 | 3.2 h | 3 | 14.8 |
| Lesser Astral Essence | 10998 | 46 | 46 | 1.4 h | 2 | 31.9 |
| Fine Thread | 2321 | 45 | 148 | 3.2 h | 3 | 13.8 |
| Arkaner Wiederverwerter | 279985 | 40 | 40 | 3.2 h | 3 | 12.3 |
| Rolle der Stärke | 954 | 39 | 52 | 1.8 h | 1 | 21.5 |
| Hillman's Leather Gloves | 4247 | 38 | 38 | 3.2 h | 3 | 11.7 |
| Lagerstuhl | 279979 | 36 | 36 | 3.2 h | 3 | 11.1 |
| Mystisches mittleres Rüstungsset | 252436 | 34 | 36 | 3.2 h | 3 | 10.5 |
| Kleines Ei | 6889 | 33 | 33 | 3.2 h | 3 | 10.2 |
| Rolle der Beweglichkeit | 3012 | 30 | 30 | 1.8 h | 1 | 16.6 |
| Cured Medium Hide | 4233 | 27 | 81 | 3.2 h | 3 | 8.3 |
| Rugged Leather | 8170 | 18 | 18 | 3.2 h | 3 | 5.5 |
| Large Glowing Shard | 11139 | 18 | 20 | 3.2 h | 3 | 5.5 |
| Fine Leather Belt | 4246 | 16 | 21 | 3.2 h | 3 | 4.9 |
| Small Radiant Shard | 11177 | 15 | 15 | 3.2 h | 3 | 4.6 |
| Wächterhandschuhe | 5966 | 13 | 13 | 3.2 h | 3 | 4.0 |
| Schwacher Manatrank | 2455 | 11 | 39 | 3.2 h | 3 | 3.4 |
| Kleiner Ledermunitionsbeutel | 7279 | 11 | 11 | 3.2 h | 3 | 3.4 |
| Golden Pearl | 13926 | 11 | 11 | 3.2 h | 3 | 3.4 |
| Gekräuselte Flechte | 249399 | 11 | 20 | 3.2 h | 3 | 3.4 |
| Silver Rod | 6338 | 10 | 10 | 3.2 h | 3 | 3.1 |
| Leichte Lederarmschienen | 7281 | 10 | 10 | 3.2 h | 3 | 3.1 |
| Lesser Magic Wand | 11287 | 10 | 29 | 3.2 h | 3 | 3.1 |
| Geringer Manatrank | 3385 | 9 | 9 | 1.8 h | 1 | 5.0 |
| Kraftvolles mittleres Rüstungsset | 252437 | 9 | 84 | 3.2 h | 3 | 2.8 |
| Geprägte Lederhose | 4242 | 7 | 7 | 1.0 h | 1 | 6.9 |
| Übungszauberstab des Novizen | 247789 | 7 | 7 | 3.2 h | 3 | 2.2 |
| Verbleite Phiole | 3372 | 6 | 6 | 3.2 h | 3 | 1.8 |
| Einfaches Lagerfeuerset | 279981 | 6 | 6 | 3.2 h | 3 | 1.8 |
| Feine Ledertunika | 4243 | 5 | 5 | 3.2 h | 3 | 1.5 |
| Leichter Lederköcher | 7278 | 5 | 5 | 3.2 h | 3 | 1.5 |
| Handgenähter Ledergürtel | 4237 | 4 | 5 | 3.2 h | 3 | 1.2 |
| Dunkle Lederhose | 5961 | 4 | 4 | 3.2 h | 3 | 1.2 |
| Schwarzwelpenschuppe | 7286 | 4 | 4 | 1.0 h | 1 | 3.9 |
| Greater Magic Wand | 11288 | 4 | 4 | 3.2 h | 3 | 1.2 |
| Geprägte Lederweste | 2300 | 3 | 3 | 1.4 h | 2 | 2.1 |
| Schleimige Murlocschuppe | 5784 | 3 | 11 | 3.2 h | 3 | 0.9 |
| Purple Lotus | 8831 | 3 | 3 | 3.2 h | 3 | 0.9 |
| Feiner Lederumhang | 2308 | 2 | 2 | 1.4 h | 2 | 1.4 |
| 3396 | 3396 | 2 | 2 | 1.8 h | 1 | 1.1 |
| Mote of Magic | 247786 | 2 | 2 | 3.2 h | 3 | 0.6 |
| Handgenähte Lederhose | 2303 | 1 | 1 | 3.2 h | 3 | 0.3 |
| Coarse Thread | 2320 | 1 | 1 | 3.2 h | 3 | 0.3 |
| 2987 | 2987 | 1 | 1 | 1.8 h | 1 | 0.6 |
| Gray Dye | 4340 | 1 | 3 | 3.2 h | 3 | 0.3 |
| Black Pearl | 7971 | 1 | 1 | 2.8 h | 2 | 0.4 |
| Lesser Eternal Essence | 16202 | 1 | 1 | 3.2 h | 3 | 0.3 |
| Gewöhnliche Kräutersamen | 268415 | 1 | 1 | 3.2 h | 3 | 0.3 |
| Gebördelter Streitkolben | 766 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Malachit | 774 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Light Hide | 783 | 0 | 7 | 3.2 h | 3 | 0.0 |
| Tigerauge | 818 | 0 | 51 | 1.8 h | 1 | 0.0 |
| Eiskalte Milch | 1179 | 0 | 0 | 1.8 h | 1 | 0.0 |
| 1206 | 1206 | 0 | 2 | 1.8 h | 1 | 0.0 |
| Shadowgem | 1210 | 0 | 17 | 3.2 h | 3 | 0.0 |
| Geringer Mondstein | 1705 | 0 | 2 | 1.8 h | 1 | 0.0 |
| 1733 | 1733 | 0 | 0 | 1.8 h | 1 | 0.0 |
| 1744 | 1744 | 0 | 1 | 1.8 h | 1 | 0.0 |
| 1817 | 1817 | 0 | 0 | 1.8 h | 1 | 0.0 |
| 2287 | 2287 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Handgenähte Lederstiefel | 2302 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Light Armor Kit | 2304 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Geprägte Lederstiefel | 2309 | 0 | 5 | 3.2 h | 3 | 0.0 |
| Geprägter Lederumhang | 2310 | 0 | 0 | 2.2 h | 2 | 0.0 |
| Mittleres Rüstungsset | 2313 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Gekräftigte Lederrüstung | 2314 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Graue Lederstiefel | 2315 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Dunkler Lederumhang | 2316 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Medium Leather | 2319 | 0 | 437 | 3.2 h | 3 | 0.0 |
| Black Dye | 2325 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Beulengras | 2453 | 0 | 215 | 3.2 h | 3 | 0.0 |
| Elixier der schwachen Stärke | 2454 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Elixier der schwachen Beweglichkeit | 2457 | 0 | 24 | 3.2 h | 3 | 0.0 |
| Leinenumhang | 2570 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Leinenstoff | 2589 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Wollstoff | 2592 | 0 | 1053 | 1.8 h | 1 | 0.0 |
| Verkohltes Wolfsfleisch | 2679 | 0 | 10 | 3.2 h | 3 | 0.0 |
| Geröstetes Eberfleisch | 2681 | 0 | 0 | 3.2 h | 3 | 0.0 |
| 3167 | 3167 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Gerissener Eckzahn | 3299 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Hasenpfote | 3300 | 0 | 0 | 1.8 h | 1 | 0.0 |
| 3301 | 3301 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Leere Phiole | 3371 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Cured Light Hide | 4231 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Medium Hide | 4232 | 0 | 6 | 3.2 h | 3 | 0.0 |
| Leinentasche | 4238 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Embossed Leather Gloves | 4239 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Dark Leather Belt | 4249 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Schultern des Hügelwächters | 4251 | 0 | 0 | 2.2 h | 2 | 0.0 |
| Salt | 4289 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Silken Thread | 4291 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Thick Leather | 4304 | 0 | 8 | 3.2 h | 3 | 0.0 |
| Braunes Leinenhemd | 4344 | 0 | 0 | 3.2 h | 3 | 0.0 |
| 4701 | 4701 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Gesprungener Schnabel | 4775 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Gesträubte Feder | 4776 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Lange Schwanzfeder | 5116 | 0 | 26 | 3.2 h | 3 | 0.0 |
| Bluthornfeder | 5165 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Kodofleisch | 5467 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Kleine irisierende Perle | 5498 | 0 | 8 | 3.2 h | 3 | 0.0 |
| Iridescent Pearl | 5500 | 0 | 7 | 3.2 h | 3 | 0.0 |
| Handgenähte Lederweste | 5957 | 0 | 0 | 2.2 h | 2 | 0.0 |
| Barbarische Schultern | 5964 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Copper Rod | 6217 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Roher Stoppelfühlerwels | 6308 | 0 | 56 | 3.2 h | 3 | 0.0 |
| Formula: Enchant 2H Weapon - Lesser Intellect | 6349 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Feuerflossenschnapper | 6359 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Glänzendes Schmuckstück | 6529 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Nachtkriecher | 6530 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Rezept: Pikantes Deviat-Supreme | 6661 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Kräutergebackenes Ei | 6888 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Beinfleisch | 7097 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Handgenähter Lederumhang | 7276 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Handgenähte Armschienen | 7277 | 0 | 0 | 2.2 h | 2 | 0.0 |
| Light Leather Pants | 7282 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Behände Lederhandschuhe | 7285 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Pfeilmacher-Handschuhe | 7348 | 0 | 0 | 3.2 h | 3 | 0.0 |
| 7428 | 7428 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Crystal Vial | 8925 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Lesser Magic Essence | 10938 | 0 | 99 | 3.2 h | 3 | 0.0 |
| Greater Magic Essence | 10939 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Greater Astral Essence | 11082 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Soul Dust | 11083 | 0 | 13 | 3.2 h | 3 | 0.0 |
| Golden Rod | 11128 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Lesser Mystic Essence | 11134 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Greater Mystic Essence | 11135 | 0 | 1 | 3.2 h | 3 | 0.0 |
| Small Glowing Shard | 11138 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Truesilver Rod | 11144 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Greater Nether Essence | 11175 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Dream Dust | 11176 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Eingeborenenhose | 14097 | 0 | 0 | 1.8 h | 1 | 0.0 |
| 14161 | 14161 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Small Brilliant Shard | 14343 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Large Brilliant Shard | 14344 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Greater Eternal Essence | 16203 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Schredderanleitung - Seite 12 | 16656 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Ahornsamenkorn | 17034 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Schwaches Zauberöl | 20744 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Formel: Schwaches Zauberöl | 20758 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Windstein | 255663 | 0 | 0 | 1.8 h | 1 | 0.0 |
| Ungewöhnliche Kräutersamen | 268416 | 0 | 0 | 3.2 h | 3 | 0.0 |
| Verzauberte Laute | 279976 | 0 | 2 | 2.8 h | 2 | 0.0 |
| Lagerzelt | 279978 | 0 | 0 | 3.2 h | 3 | 0.0 |

## Unter dem Händlerpreis (Testlog 3.7, Scan 2026-10-17 16:51)

Angebote, deren Preis pro Stück unter dem liegt, was der Händler zahlt (`C_Item.GetItemInfo`, «sellPrice», nur Gegenstände, deren Daten der Client schon hatte). Kaufen und beim Händler verkaufen; keine AH-Gebühr. Gewinn = Händlerpreis × Stück − Kaufpreis.

| Gegenstand | ID | Händler zahlt | Stück darunter | kosten | Gewinn |
|---|---|---|---|---|---|
| 4360 | 4360 | 60c | 24 | 13s 20c | 1s 20c |
| Spinnensekret | 3174 | 16c | 82 | 12s 30c | 82c |
| Leichtes Rüstungsset | 2304 | 15c | 14 | 1s 40c | 70c |
| Tigerauge | 818 | 1s | 66 | 65s 34c | 66c |
| 4384 | 4384 | 10s | 38 | 3g 79s 62c | 38c |
| 5075 | 5075 | 25c | 25 | 6s | 25c |
| Dunkler Ledergürtel | 4249 | 7s 3c | 7 | 49s | 21c |
| Silberblatt | 765 | 10c | 15 | 1s 35c | 15c |
| 14369 | 14369 | 8s 9c | 1 | 8s | 9c |

Spalte «Plan»: «ja» = mit `--eintragen` übernehmbar, «dünn» = bleibt beim AHledger-Preis.

## Im Plan

Noch nicht eingetragen: Der Plan rechnet weiter mit den AHledger-Preisen. Eintragen mit `python3 tools/ah_aus_testlog.py <Testlog> --eintragen`, danach `python3 tools/plan_berufe.py` (offene Entscheidung 17).
