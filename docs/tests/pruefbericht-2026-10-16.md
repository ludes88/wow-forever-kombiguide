# Prüfbericht 16.10.2026: zweite Prüfrunde

Auftrag des Nutzers (15.10., spät): «alles nochmals genauestens durchzugehen, durchzurechnen, feinjustierungen zu tätigen, ggf anpassungen zu machen und die wichtigsten test z erörtern … führe auch ein gesamt audit aus und trage alles nach».

Geprüft haben vier eigene Prüf-Agenten, die die Arbeit nicht selbst gemacht haben, auf dem Stand `main` 0389f10 (Merge #23). Sie haben nichts geändert:
- **Zahlen** (Z): Berufe-Plan, Kombi-Guide 0.5.2 und Markt-Empfehlungen, mit eigenem Rechen-Code nachgerechnet.
- **Doku** (D): alle versionierten Dateien, Neubauten bytegleich zum Repo.
- **Markt** (M): die drei AH-Scans vom 15.10. (20:12, 21:54, 22:15) mit Angebotstiefe, Händlerpreisen und Beute.
- **Testlog**: Testlog 3.7 gegen die Forever-API 1.60.1 (70374). Dieser Prüfer brach vor seinem Bericht ab (Sitzungsgrenze). Sein Protokoll nennt keinen Fehler; offen blieb eine Frage zur Reihenfolge der Laufweg-Proben, die Claude geprüft und behoben hat (unten).

Die Umsetzung stammt von Claude (Branch `pruefung-2`, Kombi-Guide 0.5.3, Testlog 3.7.1). Ein fünfter Prüfer hat die Umsetzung gegengeprüft (Abschnitt «Gegenprüfung»).

«umgesetzt» = im Branch `pruefung-2` erledigt; «teilweise»; «offen» = noch nicht gemacht; «Entscheid» = liegt beim Nutzer (`docs/entscheidungen.md`).

## Die wichtigsten Befunde

| Nr. | Befund | Stand |
|---|---|---|
| Z-A1 | Stufe C in Thunder Bluff für Quereinsteiger (LW über 100, ohne Zwischenprodukte, wie der Stufe-18-Charakter): Die Zähler verlangen die volle Menge (240 Leichtes und 35 Mittleres Leder, im Scan vom 15.10. etwa 1g 44s), danach erscheint kein LW-Schritt, weil Cured Light Hide, Fine Leather Belt und Cured Medium Hide fehlen | umgesetzt (v0.5.3): Plan-Zeilen 85–89 (Hinweise, Bälge und Gürtel selbst herstellen), Texte in 52 und 54 («bis LW 115 pro fehlendem Punkt etwa 16 Leichtes Leder», die genaue Menge zeigt `/tl tipp`). Die Zähler selbst bleiben bei der Plan-Menge. |
| Z-A2 | VZ 130–150 ohne eigenen Soul Dust: gekaufter Soul Dust etwa 78s teurer als Stiefel - Schwache Ausdauer (AHledger; mit dem eigenen Scan etwa 68s) | umgesetzt: Zeile 90 (Stiefel, nur mit weniger als 20 Soul Dust), Text in 81, Berufe-Plan Stufe D |
| Z-A3 | Markt-Tipps 1 und 2 brauchen dasselbe billige Leder; beide zusammen hätten etwa 28s Verlust gebracht | umgesetzt: ein Angebotsbuch für alle Tipps, Mindestgewinn 5c je Herstellung |
| D-A1 | Die Einrichtung (Punkt 25) zeigt auf die Datei im Repo-Klon; die bricht ab, weil sie `Interface\AddOns` neben sich sucht | umgesetzt: überall `KombiEinrichten.bat` im Ordner `_classic_beta_` |
| Z-B6, M-1 | Lesser Magic Essence wird nie über Greater Magic Essence gerechnet, obwohl Teilen 1 → 3 gemessen ist (13.10.: aus 9 wurden 27) | umgesetzt: Berufe-Plan (kleinerer Preis), Markt-Werkzeug (Teilen mit Rest), Zählertexte. Damit wird der Grosse Magiezauberstab für den Händler zum Tipp (Scan 15.10.: etwa 63c je Stab, Grenze 81c je Lesser) |
| Z-C1 | `.maxskill` hat in RXP v4.11.23 kein Ereignis (`functions.lua`): Gesellen-Schritte haken nach dem Lernen nicht von selbst ab | umgesetzt: zusätzlich `.istrained` mit der Zauber-ID des Gesellen (IDs aus RXP, in Forever ungeprüft; T29) |
| M-a | Warnung beim Händler: Am 15.10. um 20:10 gingen 5 Graue Farbstoffe und 7 Einfaches Holz für 4s 98c an den Händler; im AH lagen sie bei 4s bzw. 53c pro Stück, und der Plan braucht 10 Graue Farbstoffe | umgesetzt: Testlog 3.7.1 mit `KombiDaten.nichtVerkaufen` (T31) |

## Zahlen

| Nr. | Befund | Stand |
|---|---|---|
| Z-B1 | Zwei Netto-Begriffe; Rest vor Gebühr | umgesetzt: «netto» erklärt; Rest nach Gebühr 3g 16s 45c; der ganze Plan nach Verkauf des Rests etwa 8g 29s 51c |
| Z-B2 | §1: Hosen und Gürtel mit dem Entzauberungswert, Bälge mit 0 | umgesetzt: Spalte «wie» (Händler, entzaubert, AH nach Gebühr, Material) |
| Z-B3 | Heavy Leather als Gewinn | umgesetzt: nach Gebühr, der eigene Scan daneben (dort Kosten statt Gewinn) |
| Z-B4 | §3 meldet Widersprüche, die die Lehrerlisten aufgelöst haben | umgesetzt: Lernstufen zuerst aus `data/kombi/lehrer.csv` |
| Z-B5 | VZ 110–130: «2 pro Punkt» | umgesetzt (Zeile 78: etwa 3 pro Punkt) |
| Z-B7 | Angeln vor Gebühr | umgesetzt: 2g 0s 64c (NH) bzw. 4g 90s 2c (PH) pro Stunde nach Gebühr |
| Z-B8 | Zauberstab-Regeln vergleichen mit dem teureren Weg | umgesetzt |
| Z-C2, Z-C3 | Gesellen-Schritt fällt unter Fertigkeit 50 weg; Zeile 81 ohne «Häkchen» | umgesetzt (Texte 29, 46, 81) |
| Z-C4 | Händlerverkauf (etwa 2g 14s) erst nach dem Kauf für Stufe D | umgesetzt: Verkauf vorher |
| Z-C5 | Lehrer B mit Minor Stamina | umgesetzt (Lehrer B 6s) |
| Z-C6 | Tamar mit alter Quelle und altem Ort | umgesetzt (Ort gemessen 63.2, 45.3; Preise «nicht eindeutig») |
| Z-C7 | Zahlen und Namen ohne Beleg in Guide-Texten | umgesetzt (Zeilen 6, 22, 30, 31, 78; der Tipp-Text nennt AH und Händler getrennt) |
| Z-C8 | `fuer_haendler` kauft Zwischenprodukte im AH, «geschätzt» wird nie angezeigt | umgesetzt |
| Z-C9 | «Unter dem Händlerpreis» nennt die falsche Testlog-Version | umgesetzt |
| Z-C10 | Pfand fehlt in allen Margen | offen: Pfand-Formel ungeprüft (gemessen 1s für 1 Groben Faden, 8s 50c für 4 Edelsteine); Messung T25 |
| Z-C11 | Rückfall auf nicht lernbare Rezepte | umgesetzt |
| Z-C12 | Festwerte in §9 | umgesetzt (aus dem eigenen Scan) |
| Z-C13 | Strange Dust fehlt im ersten AH-Zähler in Orgrimmar (zweiter Gang ins AH) | offen: Zeile 19 liegt vor der Stelle #152; eine zusätzliche Zeile geht nur, wenn `tools/rxp_schritte.py vergleich` die Stelle hält |
| Z-C14 | «gleißender» neben «Grosse» | Entscheid: Schreibweise der Client-Namen |
| Z-C15 | Zu viel kaufen bei Zwischenständen (Zeile 23: 27 Salt bei LW 55–79; Zeile 31: Rute und 19 Motes bei VZ 2–49) | offen, gleicher Grund wie Z-C13 |
| Z-C16 | Händlerware ausserhalb der Plan-Tabellen zum AH-Preis | offen: Forever-Händlerpreise dafür ungeprüft |
| Z-K1 | Hillman's Shoulders (4251) als billigerer Weg für LW 125–150 | offen: Messung bei LW 125–130 |
| Z-K2 | Mittleres Leder selbst herstellen, solange Leichtes Leder höchstens 43c kostet | teilweise: das Markt-Werkzeug stellt Zwischenprodukte selbst her, der Berufe-Plan nicht |

## Doku

| Nr. | Befund | Stand |
|---|---|---|
| D-B1 | Fangrate 134 statt 144 nur im Berufe-Plan | umgesetzt: Best Practice §9, Messplan (Break-even etwa 13–14 bzw. 18–20 Knoten pro Stunde), Korrekturvermerk in `docs/recherche/2026-10-14_goldquellen.md` |
| D-B2 | Entscheidungsgrundlagen mit alten Zahlen (Punkte 6 und 8, Best Practice §1) | umgesetzt |
| D-B3 | Einfüge-Regel nennt #84 statt #152 | umgesetzt |
| D-B4, D-B5, D-B9 | vorgehen.md, Messplan, README und `aktualisieren.bat` beschreiben den alten Ablauf | umgesetzt |
| D-B6, D-B7 | Messplan: Stände widersprechen sich; «der Plan» meint einen Markt-Tipp | umgesetzt (ein Stand 15.10. 22:16; Abschnitt für den Stufe-8-Druiden neu) |
| D-B8 | Prüfbericht 15.10., D2: Begründung falsch | umgesetzt (Zeilen 8 und 11 liegen nach #45; beide Texte nennen jetzt den Ausweg «Häkchen setzen», falls der Lehrer eine höhere Stufe verlangt) |
| D-B10 | `#next` der Dungeon-Gruppe falsch beschrieben | umgesetzt |
| D-B11 | Messdaten 15.10.: ein Tod statt zwei, im falschen Abschnitt | umgesetzt (20:48 und 20:52, Abschnitt 19:48–20:58) |
| D-C1–D-C32 | Kleinigkeiten (Karten, Zahlen, Pfade, Versionen, «ungeprüft», fehlende Einträge) | umgesetzt; die offenen Rückfragen stehen als Punkte 30–35 in `docs/entscheidungen.md` |

## Markt

| Nr. | Vorschlag | Stand |
|---|---|---|
| M-1 | Umwandlungen: Grosse Essenz in 3 Geringe und zurück | teilweise: Teilen ja (Magie, Astral, Mystik, Nether, Ewig), Zusammenfügen nicht |
| M-2 | Für den Händler herstellen mit Umwandlungen, Zwischenprodukten und Grenzpreis | umgesetzt |
| M-3 | Billigster Weg pro Punkt über alle gelernten Rezepte | teilweise: der Berufe-Plan nimmt für VZ pro Abschnitt das günstigste lernbare Rezept samt Lernkosten; im Markt-Werkzeug offen |
| M-4 | Pfand-Modell | offen (wie Z-C10) |
| M-5 | Einzelstücke ohne Abnahme-Beleg empfehlen | teilweise: Zeile «AH statt Händler» für Sammler (nach Gebühr mindestens 3-mal der Händlerpreis, mindestens 20 Stück im Angebot); ohne Pfand-Schwelle |
| M-6 | Farmwert mit AH-Preisen | offen |
| M-7 | Knappheit melden | offen |
| M-8 | Nächster Schritt für Sammler | umgesetzt (Leder für Stufe A, Gold für Orgrimmar, AH statt Händler) |
| M-9 | Listen in KombiDaten | teilweise: «nicht beim Händler verkaufen» und «beobachten» umgesetzt, «beim Händler kaufen, nicht im AH» offen |
| M-a | Warnung beim Händler | umgesetzt (oben) |
| M-b | Grenzpreise live im Testlog | offen |
| M-c | Erinnerung für Scan-Paare | umgesetzt: 20 Minuten nach einem Scan, wenn der Charakter noch ausruht (Stadt oder Gasthaus) |
| M-d | Mehr Beute beobachten | umgesetzt: eigene Beute, Plan-Leder, Essenzen, Shadowcat Hide, zwei Rüstungssets, Wollstoff; Fleisch und Rollen, sobald sie einmal gefallen sind |
| M-e | Umwandeln im Testlog erkennen | offen (sichtbar ist es schon in TASCHE: −1 Grosse, +3 Geringe) |
| M-f | Pfand pro Angebot | weitgehend seit Testlog 3.7 (AH-ANGEBOT mit Menge, Dauer und Pfand aus dem Geldabzug) |

## Testlog

- Reihenfolge der Laufweg-Proben (Frage des Testlog-Prüfers): `tools/spiel_aus_testlog.py` sammelt die Proben aus mehreren Dateien in einer Menge. Bei gleicher Sekunde hing die Reihenfolge von Sitzungsmarke «S» und erster Probe vom Hash-Zufall ab; die Auswertung konnte von Lauf zu Lauf um eine Probe abweichen. Behoben: `weg_ordnung` sortiert die Marke vor die Probe derselben Sekunde (Probe in `tools/testlog_harness.py`, gegengeprüft mit verschiedenen `PYTHONHASHSEED`).
- Testlog 3.7.1 dazu: fehlende Händlerpreise fragt das Testlog beim AH-Scan an (`C_Item.RequestLoadItemDataByID`, höchstens 200 pro Scan), Berufe und Geld pro Charakter merkt es für `/tl tipp`.

## Gegenprüfung der Umsetzung

Wird nach dem Bericht des fünften Prüfers ergänzt.

## Datenschutz

- Vor jedem Commit: Suche nach Namen, Konto, Wohnort und E-Mail im Diff (leer).
- Kontoname in den Zeilen `## Author:` der drei `.toc`: Entscheid (Punkt 27).
- Uhrzeiten in `data/preise/ah_eigen.csv` und `docs/tests/`: Entscheid (Punkt 33).
