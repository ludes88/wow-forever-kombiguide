# Prüfbericht 15.10.2026 und was daraus wurde

Auftrag des Nutzers (15.10., spät): «führe auch ein gesamt audit aus und trage alles nach». Geprüft hat ein eigener Prüf-Agent, der die Arbeit nicht selbst gemacht hat, auf dem Stand `main` 2a5b8ed (Merge #22). Er hat nichts geändert; die Umsetzung stammt von Claude (Branch `testlog-3.7`, seit Merge #23 auf `main`; Kombi-Guide 0.5.2). Die zweite Prüfrunde vom 16.10. steht in `pruefbericht-2026-10-16.md`.

## Grundlagen des Prüfers

- Repo `main` 2a5b8ed; RXP-Klon `vendor/rxpguides` mit Tag v4.11.23 und Hauptzweig dec489a2 (15.10.), https://github.com/RestedXP/RXPGuides
- Testlog-Datei vom 15.10. 22:16 (nicht versioniert; Namen nicht übernommen)
- Prüfläufe, alle grün: `validate.py`; `build_kombi.py v4.11.23` bytegleich zu `main`; `plan_mengen.py` und `plan_berufe.py` bytegleich; `ah_aus_testlog.py`, `lehrer_aus_testlog.py`, `karte_aus_testlog.py` ohne Abweichung; `testlog_harness.py`; `rxp_schritte.py vergleich` für #45 und #152; Schrittzahlen in Best Practice §2 und §5 nachgezählt; Dungeon-Gruppe gegen RXP mit RFC, WC, BFD (180 von 180 gleich)

## Befunde und Stand

«umgesetzt» = im Branch `testlog-3.7` erledigt (seit Merge #23 auf `main`); «Entscheid» = liegt beim Nutzer (`docs/entscheidungen.md`).

| Nr. | Befund (kurz) | Stand |
|---|---|---|
| A1 | Die Annahme der Berufs-Quests 97933 und 97936 bei Kaga fehlt; ohne sie erscheinen die Abgaben nie (dem Main fehlen 540 XP und zwei Rezepte) | vorbereitet: Plan-Zeilen 83 und 84 mit Status «aus»; einschalten verschiebt die Stelle #45 (geprüft); Entscheid, offener Punkt 11 |
| A2 | Lernkosten fehlen in allen Goldangaben | umgesetzt: `plan_berufe.py` rechnet `lehrer.csv` ein (A 17s 70c, B 8s 50c, C 30s, D 20s), Texte in `plan.csv` und `messplan-beta.md` |
| A3 | Angeln pro Stunde 7,7 % zu hoch (14 Fänge = 13 Abstände) | umgesetzt: `ANGELN_FAENGE_H = 3600 / (349 / 13)`, Berichte neu (2g 11s statt 2g 27s pro Stunde, NH) |
| A4 | Angeln bis 50 im Teich von Thunder Bluff mit der Rate vom Stonebull Lake | umgesetzt: Text nennt den Stonebull Lake und dass in Hauptstädten bis 75 Fische entkommen |
| A5 | Bedingungen mit alten Lernstufen (Heavy Leather, Hillman's, Runed Silver Rod) | umgesetzt: `<125`, `<120`, `<100` |
| A6 | Enchant Boots - Minor Stamina ohne Lernhinweis, 14s für wenige Punkte | umgesetzt: Zeile entfernt; der Plan nimmt Bracer - Lesser Stamina |
| A7 | Unter VZ 40 kein Rezept für Essenzen | umgesetzt: Text «unter 40 nur Staub»; der Plan prüft jetzt pro Punkt, ob das Rezept schon geht (`learn_at`) |
| A8 | Stufe C: eine Lesser Magic Essence fehlt | umgesetzt: Stufe C kauft jetzt 20 Lesser Magic Essence und 69 Strange Dust (Zähler), weil Hosen und Gürtel an den Händler gehen |
| A9 | Dungeon-Gruppe springt in den Speedrun-Guide statt wie RXP nach «RestedXP Horde 22-30» | umgesetzt: `#next` wie bei RXP; im Spiel ungeprüft (T5) |
| A10 | Kleinfisch-Hinweise, bevor man angelt | umgesetzt: «falls du schon angelst» |
| Kommentar | Grosser Magiezauberstab für VZ 70–100 billiger | ausgebaut: Variante Zauberstäbe (berufe-plan §9, VZ 10–109); Entscheid, offener Punkt 28 |
| B1 | Merge-Commits tragen den Profilnamen des Nutzers (GitHub-Webschnittstelle) | ab jetzt lokale Merges als Claude; alte Commits: Entscheid, offener Punkt 27 |
| B2 | Versionierte Dateien ohne persönliche Daten | in Ordnung (vor jedem Commit erneut geprüft) |
| C1 | Build 70338 statt 70374 | umgesetzt (CLAUDE.md, Best Practice) |
| C2 | Berufe-Plan noch mit Minor Deflect, Status offen | umgesetzt: Minor Deflect gilt ab 40 (AHledger), laut SeeMeta mit dem Rang; im Spiel zu prüfen (Messplan, Stufe-8-Druide) |
| C3 | Falsche Quelle (Rezept 7428 statt 7426) in Plan-Zeile 36 | umgesetzt |
| C4 | Heavy Leather mit altem Preis | offen wie Risiko 22: der Bericht zeigt jetzt den Vergleich mit den eigenen Scan-Preisen; ob sie den Plan ersetzen, ist Entscheid 17 |
| C5 | README-Stand veraltet | umgesetzt |
| C6 | Messplan: Version, Testliste, «Kosten ungeprüft» | umgesetzt |
| C7 | T22 erwartet «0.5» | umgesetzt (Version aus der `.toc`) |
| C8 | Tamar: gemessene Preise (10c, 50c) und Ort | umgesetzt (Best Practice §9) |
| C9 | Kalimdor fehlt in den Kartenlisten | umgesetzt |
| C10 | Risiko 17 mit Zählung auf v4.11.13 | umgesetzt (456 Punkte auf v4.11.23) |
| C11 | `werkzeuge/merge_poc.py`, «ZIP für den Chat» | umgesetzt |
| C12 | `vorgehen.md`: 3 exakte Karten, Stelle #84 | umgesetzt |
| C13 | «im Mittel 50 Stück», der Code nimmt den Median; Quelle «Testlog 3.5» fest im Code | umgesetzt: Text «Median»; die Version kommt ab Testlog 3.7 aus dem Scan |
| C14 | Status-Spalten in `plan.csv` veraltet | umgesetzt |
| C15 | Restwert 3g 85s ist der Wert aller Stufen | erledigt durch die Neuberechnung (Rest jetzt 3g 33s, alle Stufen) |
| C16 | Händlerzeile 20:10 liest sich wie ein Kauf | umgesetzt (`messdaten-2026-10-15.md`) |
| D1 | Unbelegt: «Taste K», «bringt der Lehrling mit», «Build 70245» | umgesetzt (Text belegt oder entfernt) |
| D2 | Geselle Kürschnerei ohne Stufen-Schutz | offen: ob der Geselle Kürschnerei Stufe 10 verlangt, ist ungeprüft (Widersprüche 5, 6); die Plan-Zeilen 8 und 11 liegen nach der Stelle #45 (Zeile 8 ist #88 in «6-12 Mulgore»), eine Bedingung wie in Zeile 15 (`.xp <10,1`) verschöbe #45 also nicht (Begründung korrigiert am 16.10.); seit v0.5.3 nennen beide Texte den Ausweg «Häkchen setzen» |
| D3 | Fine Leather Belt hängt an Cured Medium Hide | offen, bewusst: ohne Medium Hide fehlt auch der Dunkle Ledergürtel (Risiko 20) |
| D4 | Rundung «1g 58s» | umgesetzt (1g 59s) |
| D5 | Kommentar in `rxp_schritte.py` | umgesetzt |
| D6 | Peacebloom als «ungeprüft» im Testlog | umgesetzt |
| D7 | `addons_verknuepfen.bat` sagt `/reload` | umgesetzt (Neustart; dazu der Hinweis auf `kombi_einrichten.bat`) |
| D8 | `ah_abnahme.csv` entsteht erst ab zwei Scans mit 3.6 | umgesetzt (CLAUDE.md) |
| D9 | Weitere Dateien aus RXP-Daten | umgesetzt (`LICENSE-NOTES.md`) |

## Dazu aus der eigenen Prüfung von Claude (15.10., spät)

- Händlerpreise: Classic-Datenbanken taugen nicht für Forever (19 von 91 verglichenen Gegenständen anders, fast nur hergestellte Teile; `docs/recherche/2026-10-15_haendlerpreise.md`). Darum misst Testlog 3.7 den Händlerpreis beim AH-Scan selbst.
- Berufe-Plan: Leichte Lederhosen (Händler 5s 99c) und Dunkle Ledergürtel (7s 3c) bringen beim Händler mehr als ihr Entzauberungs-Ertrag im AH (2s 31c bzw. 5s 11c, Beta). Stufe C netto: 1g 60s statt vorher 2g 73s Einkauf ohne Lehrer.
- Markt (Scan 15.10. 22:15): Für den Händler herstellen lohnt für den Stufe-18-Charakter bei der Leichten Lederhose (Grenzpreis Leichtes Leder 38c); unter dem Händlerpreis lag im Scan nichts (bei den 103 Gegenständen mit bekanntem Forever-Preis).
- Stufen pro Stunde aus dem Protokoll (`docs/plan/spiel.md`): Questen mit Abgaben am 15.10. 1,9 Stufen pro Stunde (Stufe 16,7 → 18,6), Mulgore am 13.10. 2,6 (Stufe 6 → 7,5); Sitzungen mit Berufen und Auktionshaus darunter. Kleine Stichprobe, nur als Grössenordnung.
