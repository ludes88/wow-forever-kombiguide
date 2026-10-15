# Messdaten 14. und 15.10.2026

Quelle: die Testlog-Datei des Nutzers, Stand 15.10. 19:38 (Testlog 3.3 und 3.5), am 15.10. über die Verbindung zum PC gelesen. Ohne Charakter-, Konto- und Realmnamen.

## Sitzungen

| Zeit | Charakter | Guide und Stelle | Versionen |
|---|---|---|---|
| 14.10. 19:52–19:54 | Stufe 15 | «12-17 The Barrens» #77 | Kombiguide 0.3, Testlog 3.3 |
| 14.10. 20:00–20:09 | Tauren-Druide, Stufe 7 (46 % → 74 %) | «6-12 Mulgore» #30 → #45 | Kombiguide 0.3, Testlog 3.3 |
| 15.10. 19:21–19:38 | Stufe 15 (70 % → 97 %) | «12-17 The Barrens» #77 → #84 | Kombiguide 0.4, Testlog 3.5 |

## Stellen im Kombi-Guide (Best Practice §6)

- «6-12 Mulgore» #45: `.accept 749` (Zeile 510). Von v0.3 zu v0.4 unverändert: `tools/rxp_schritte.py vergleich git:2620af4:addons/RXPGuides_KombiGuide/Kombi_Guide.lua addons/RXPGuides_KombiGuide/Kombi_Guide.lua "6-12 Mulgore" --stelle 45 --klasse druid` meldet «Stelle #45 bleibt».
- «12-17 The Barrens» #84: `.xp 16` (Zeile 1799, Druiden-Zählung im Bau v0.4).
- Schrittwechsel des Stufe-15-Charakters am 15.10.:
  - #77 → #78 um 19:28 nach der Beute «Konsolenschlüssel» (Quest 901)
  - an #78 Abgabe 901 und Annahme 902
  - #81 bei den Raptorenköpfen (Quest 869)
  - #84 ab 19:35, an #84 Annahme 858
- Das passt nur zur Druiden-Zählung (`tools/rxp_schritte.py liste … "12-17 The Barrens" --klasse …`). Bei Jäger, Schamane und Krieger stehen an #77 bis #84 andere Schritte. Der Charakter ist also sehr wahrscheinlich ein Druide (die Klasse steht nicht im Testlog).
- RXP sprang um 19:35 von #81 auf #84. #83 ist der Kombi-Schritt «Sweetspot Leichtes Leder». Er erscheint nur mit Kürschnerei, und der Charakter hat keine mehr; der Sprung passt dazu (T4, indirekt).

## Messwerte

- Kürschnern, Druide Stufe 7, Kürschnerei 22 → 25 (je Haut +1):
  - Prairie Wolf (2958): 2 Häute, je 1 Verdorbene Lederfetzen
  - Adult Plainstrider (2956): 1 Haut, 1 Leichtes Leder
- Kräuterkunde 10 → 11: 2 Friedensblume (2447) aus Objekt 1618.
- Quest 97936 «Grundlagen des Zeltens: Kürschnerei», abgegeben am 14.10. um 20:07:
  - Standort des Spielers 45.0, 61.5 (Bloodhoof)
  - Belohnung 270 XP und das Rezept «Lagerstuhl» (1229517)
  - Laut warcraft.wiki.gg ist die Abgabe bei Yonn Deepcut (45.0, 61.4) und die Belohnung das Rezept Camp Chair. Das passt zur Messung; der Name des NPC steht nicht im Testlog. Widerspruch 1: spricht für 45.0, 61.4.
- Händler, 14.10. um 19:53: 11 Greater Magic Wand (11288) für zusammen 22s, also 2s je Stück (Widerspruch 21; die Datenbanken nennen 2s, die Patch-Notiz 1c).
- Quest-XP: 754 «Säuberung von Winterhoof» 550, 901 «Samophlang» 750.
- Beute am 15.10. (Stufe 15, Nordbrachland, 12 Minuten, 13 Beutefenster):
  - Geld zusammen 1s 31c
  - Die Gegenstände haben in Testlog 3.5 noch keinen Preis; erst 3.6 schreibt die Händlerpreise mit.

## Berufe des Stufe-15-Charakters

- Laut Testlog vom 13.10.: Lederverarbeitung 109/150, Verzauberkunst 100/150 (letzte BERUF-Zeilen um 19:24 und 19:46). Seither keine neuen BERUF-Zeilen.
- Laut Nutzer (15.10.): Er hat Kürschnerei und Kräuterkunde schon vor dem geplanten Wechsel in Orgrimmar gegen Lederverarbeitung und Verzauberkunst getauscht.
- Den Berufswechsel (M5, T11) kann er deshalb nicht mehr messen. Wer das misst, ist offener Punkt 22 in `docs/entscheidungen.md`.
- Ob er Angeln hat, zeigt das Testlog nicht (keine BERUF-Zeile dazu).

## Datei und Verknüpfung

- Die Testlog-Datei war am 15.10. um 19:38 60 KB gross, dazu eine `.bak` mit 57 KB. Sie enthält keine AH-Scans: Testlog 3.5 war geladen, aber das Auktionshaus wurde nicht geöffnet.
- Geprüft am 15.10.: Im AddOns-Ordner der Beta sind `KombiTestlog`, `RXPGuides_Kombi` und `RXPGuides_KombiGuide` Verknüpfungen (Junction) auf den Repo-Klon, keine Kopien. `KombiTestlog.lua` hat dort dieselbe Grösse und denselben Zeitstempel (auf die Millisekunde) wie im Klon. Im Ordner `_alt_kombi` liegen die alten Kopien, die `addons_verknuepfen.bat` beiseitegelegt hat.
- Der Klon stand am 15.10. um 19:20 auf `ed47fcf` (Merge #15, Testlog 3.5). Testlog 3.6 (Merge #16) kommt erst mit dem nächsten `aktualisieren.bat`.
- `Interface\AddOns\KombiDaten` hat Claude am 15.10. erstmals geschrieben (`tools/markt.py`). Darin sind noch keine Tipps, weil Preise fehlen.
