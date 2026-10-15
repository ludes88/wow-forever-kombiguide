# Händlerpreise: Forever-Client gegen Classic (Recherche 15.10.2026)

Frage: Kann man Händlerpreise aus Classic-Datenbanken nehmen, um Gewinne zu finden (AH unter Händlerpreis, für den Händler herstellen)? Antwort aus den Daten: nein, nicht für hergestellte Teile.

## Quellen

- Forever: `data/preise/haendler_ankauf.csv`, aus den Gegenstands-Infos des Testlogs 3.6 (`C_Item.GetItemInfo`, 11. Wert «sellPrice», Forever-Client 1.60.1, Testlog 15.10.2026, 103 Gegenstände).
- Classic: wow-classic-items (MIT, letzter Stand 25.11.2022, Daten von Wowhead und der Blizzard-API), Feld «sellPrice»: https://github.com/nexus-devs/wow-classic-items
- AH: letzter eigener Scan (`data/preise/ah_alle.csv`, 15.10.2026 22:15, Beta, PvP-Realm der Horde).

## Ergebnis

- Verglichen: 91 Gegenstände (ohne Classic-Eintrag: 12, meist neu in Forever). Gleich: 72, anders: 19.
- Anders sind fast nur hergestellte Teile, und zwar fast immer niedriger als in Classic. Gleich geblieben sind z. B. Leichte Lederhose (5s 99c), Dunkler Ledergürtel (7s 3c), Geprägte Lederhose (3s 47c), Feine Ledertunika (4s 61c), Dunkle Lederhose (10s 89c).
- Folge: Ein Vergleich «AH unter Händlerpreis» mit Classic-Preisen meldet am 15.10. Gewinne, die es nicht gibt (Tabelle unten: fast alles hergestellte Teile, deren Forever-Preis tiefer ist). Darum misst das Testlog ab Version 3.7 den Händlerpreis beim AH-Scan selbst.

## Unterschiede (Forever gegen Classic, Kupfer)

| ID | Gegenstand (deutsch, Testlog) | Forever | Classic | hergestellt |
|---|---|---|---|---|
| 2308 | Feiner Lederumhang | 267 | 214 | ja |
| 2310 | Geprägter Lederumhang | 112 | 149 | ja |
| 2314 | Gekräftigte Lederrüstung | 743 | 1487 | ja |
| 2315 | Dunkle Lederstiefel | 307 | 513 | ja |
| 2316 | Dunkler Lederumhang | 408 | 544 | ja |
| 4237 | Handgenähter Ledergürtel | 34 | 35 | ja |
| 4239 | Geprägte Lederhandschuhe | 71 | 119 | ja |
| 4246 | Feiner Ledergürtel | 125 | 208 | ja |
| 4251 | Schultern des Hügelwächters | 1199 | 1200 | ja |
| 7005 | Kürschnermesser | 2 | 16 | nein |
| 7281 | Leichte Lederarmschienen | 84 | 142 | ja |
| 7285 | Behände Lederhandschuhe | 588 | 589 | ja |
| 7348 | Pfeilmacher-Handschuhe | 690 | 829 | ja |
| 10938 | Geringe Magieessenz | 1 | 0 | nein |
| 10940 | Seltsamer Staub | 1 | 0 | nein |
| 10978 | Kleiner gleißender Splitter | 1 | 0 | nein |
| 11287 | Geringer Magiezauberstab | 110 | 508 | ja |
| 11288 | Großer Magiezauberstab | 200 | 1535 | ja |
| 20744 | Schwaches Zauberöl | 100 | 500 | ja |

## AH unter dem Classic-Händlerpreis (Scan 15.10. 22:15)

Mit Classic-Preisen sähe es so aus. «Forever» = gemessener Händlerpreis, wo bekannt; nur Shadowcat Hide ist kein hergestelltes Teil, sein Forever-Preis ist unbekannt (im Spiel prüfen: Tooltip im AH, ab Testlog 3.7 automatisch).

| ID | Gegenstand | Tiefstpreis AH | Classic-Händler | Forever-Händler | Stück im Angebot | hergestellt |
|---|---|---|---|---|---|---|
| 7428 | Shadowcat Hide | 4s | 25s | unbekannt | 43 | nein |
| 11288 | Greater Magic Wand | 3s | 15s 35c | 2s | 156 | ja |
| 2314 | Toughened Leather Armor | 8s | 14s 87c | 7s 43c | 13 | ja |
| 7958 | Bronze Battle Axe | 36s | 40s 59c | unbekannt | 5 | ja |
| 2866 | Rough Bronze Cuirass | 8s | 12s 55c | unbekannt | 112 | ja |
| 11287 | Lesser Magic Wand | 2s | 5s 8c | 1s 10c | 126 | ja |
| 6350 | Rough Bronze Boots | 3s | 4s 93c | unbekannt | 62 | ja |
| 4314 | Double-stitched Woolen Shoulders | 4s | 5s 53c | unbekannt | 119 | ja |
| 3835 | Green Iron Bracers | 17s | 18s 44c | unbekannt | 101 | ja |
| 2857 | Runed Copper Belt | 2s | 3s 30c | unbekannt | 43 | ja |
| 7348 | Fletcher's Gloves | 7s | 8s 29c | 6s 90c | 18 | ja |
| 2315 | Dark Leather Boots | 4s | 5s 13c | 3s 7c | 274 | ja |
| 20744 | Minor Wizard Oil | 4s | 5s | 1s | 153 | ja |
| 2854 | Runed Copper Bracers | 3s | 3s 76c | unbekannt | 94 | ja |
| 2316 | Dark Leather Cloak | 5s | 5s 44c | 4s 8c | 253 | ja |

## Für den Plan

- `tools/plan_berufe.py` und `tools/markt.py` nehmen nur Händlerpreise aus dem Forever-Client (`haendler_ankauf.csv`; für Teile ohne Messung im Plan die Spalte «Händlerpreis (s)» aus `data/rechnung/Kreislauf.csv`, AHledger, als ungeprüft markiert).
- Zum Start (04.11.2026) neu messen: Händlerpreise können sich mit dem Release-Build ändern (Risiko 26 im Best-Practice-Dokument).
