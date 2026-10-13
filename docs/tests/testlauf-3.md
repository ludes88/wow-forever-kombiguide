# Testlauf 3 – Mulgore 6 → 10 mit Testlog 3 (ab 13.10.2026, läuft)

Ziel: Messdaten für v0.2 (Mulgore 6–12): Leder pro Tierart, Kräuter pro Knoten, Geld pro Kill und Händlerbesuch, Lehrerkosten auf Stufe 8 und 10. Dazu Test T6 (Fortschritt nach einem Update).

Aufbau: Tauren-Druide, Stufe 6, Kürschnerei 1/75, Kräuterkunde 5/75. Addons nach dem CurseForge-Update und `aktualisieren.bat` (Stand `37141b8`), Spiel neu gestartet.

## Erster Abschnitt (13.10., 22:07–22:11)

| Nr. | Beobachtung | Bedeutung |
|---|---|---|
| 1 | SITZUNG meldet RestedXP **v4.11.23**, «Kombiguide 0.1.2-v4.11.13», «Testlog 3», «Kombi-Test 1», Geld 65c | CurseForge hat RXP von v4.11.13 auf v4.11.23 gebracht. Der Kombi-Guide aus der v4.11.13-Route läuft auch mit RXP v4.11.23 (T0 bestanden) |
| 2 | Fortsetzung bei «06-12 Mulgore #13», dann #14 bis #18 | Das Update v0.1.1 → v0.1.2 (nur Koordinaten) hat die Stelle behalten (T6 für diesen Fall bestanden) |
| 3 | Das WC-Test-Addon (`RXPGuides_Kombi`) ist jetzt geladen; nach dem `/reload` um 19:50 war es das nicht | Neu verknüpfte Addon-Ordner brauchen einen Neustart des Spiels; `/reload` genügt nur für Addons, die schon geladen waren |
| 4 | Erste SITZUNG nach dem Neustart ohne Gebiet, Karte 1414 (Kalimdor), eine Sekunde später GEBIET Mulgore | Fehler A aus Testlauf 1 tritt nach einem Neustart wieder auf. Behoben in Testlog 3.1: Der Start wartet, bis der Client eine Zone meldet (höchstens etwa 12 Sekunden) |
| 5 | KARTE 1414 Kalimdor: (0,0) = 12799.90, 17066.60; (1,1) = −11733.30, −19733.21; 36799.8 × 24533.2 Yards | in `data/karten/forever_karten.csv` übernommen. RXP nutzt Karte 1414 in der Datei der Brachland-Guides (12–22) 43-mal (v4.11.13), aber ohne Kommentar-Koordinaten; Vergleich deshalb nicht möglich |
| 6 | QUEST AB 99108 «Sparringskampf», XP 550, kein Geld | Testlog 3 schreibt Geld in QUEST AB nur, wenn es welches gibt |
| 7 | `/tl list` wurde zur Notiz «list» | `/tl liste` und `/tl list` öffnen ab Testlog 3.1 das Protokoll wie `/tl zeigen` |

## Neubau auf RXP v4.11.23

- `tools/build_kombi.py v4.11.23`: keine Probleme; 4 Guides, 3 Plan-Zeilen. «1-6 Mulgore» ist unverändert (468 Zeilen).
- «6-12 Mulgore» hat vor Schritt #17 einen neuen Schritt: Quest 99411 «Kyle's Gone Missing!» bei Ahab Wheathoof (`#softcore`). Alle späteren Zeilen rücken um 6.
- RXP findet die Stelle über die Zeilennummer (Best Practice, Abschnitt 6). Die gespeicherte Stelle (#18, Zeile 62) zeigt im neuen Bau auf die Annahme von Quest 743. Die ist schon erledigt, RXP springt deshalb selbst einen Schritt weiter.
- Die neue Quest 99411 liegt vor dieser Stelle. RXP führt nicht zurück; wer sie will, holt sie über die Schrittliste.
- Erwartet nach `aktualisieren.bat` und `/reload`: SITZUNG mit «Kombiguide 0.1.2-v4.11.23», die Nummer in der Zeile RXP ist ab hier um 1 höher als im alten Bau.

## Noch offen in diesem Testlauf

- SAMMELN (Kürschnern, Kräuter), BEUTE, HÄNDLER, Lehrer auf Stufe 8 und 10 (GELD und GELERNT)
- T6 nach dem Neubau auf v4.11.23 im Spiel
