# Testlauf 2 – Kombi-Guide v0.1 (13.10.2026, abgeschlossen)

Ziel: Funktioniert das gekoppelte Konzept (RXP-Route und Berufsschritte in EINEM Guide)? Getestet mit einem Tauren-Druiden auf Stufe 5 (statt neu ab Stufe 1, Entscheidung des Nutzers), RestedXP v4.11.13, Kombi-Guide v0.1 (Basis v4.11.13) und KombiTestlog 1.

## Was in v0.1 steckte

- RXP-Gratis-Route 1–22 als eigene Gruppe «Kombiguide (H)», ohne `#defaultfor`. Das letzte `#next` zeigt auf `RestedXP Forever Guide (H)\22-24 Hillsbrad`.
- 3 Berufsschritte vor «A Task Unfinished» (1656) in «1-6 Mulgore». Für einen Tauren-Druiden sind das die Schritte #36–#38 von 39:
  - #36 Kürschnermesser (Item 7005) bei Kawnie Softbreeze
  - #37 Kürschnerei bei Nawka Wildsong (Zauber 8613)
  - #38 Kräuterkunde bei Garan Sunstrider (Zauber 2366)

## Ergebnis

| Nr. | Handlung | Erwartet | Ergebnis |
|---|---|---|---|
| 1 | Einloggen, Charakter Stufe 5 in Bloodhoof | SITZUNG | **OK**, mit Ort (Fehler A trat nicht auf) |
| 2 | «Kombiguide (H)» → «1-6 Mulgore» | `RXP … \| Kombiguide (H)` | **OK**, Start bei #8 (Händlerschritt Kawnie; er erledigt sich erst vor Ort) |
| 3 | Zurück nach Camp Narache | RXP überspringt Erledigtes | **OK**: #8 → #14 → #15 → #16 → #31 → #34 |
| 3a | #34/#35 Druidenlehrer (RXP) | – | RXPs Route erwartet Stufe 6. Wegen des Sprungs fehlten 353 XP, der Nutzer hat sie nachgeholt. Kein Fehler des Kombi-Guides |
| 4a | #36 Messer | schliesst sich mit Messer in der Tasche | **OK** (8 s) |
| 4b | #37 Kürschnerei | Pfeil auf Nawka, schliesst sich nach dem Lernen | **TEILWEISE**: gelernt (BERUF «Kürschnerei 1/75»), aber der Pfeil zeigte rund 28 Yards nach Südwesten, obwohl der Nutzer bei Nawka stand |
| 4c | #38 Kräuterkunde | überspringen, wenn schon gelernt | **OK**: Der Charakter hatte Kräuterkunde 5/75, RXP sprang auf #39 |
| 5 | Ende von «1-6 Mulgore» | Wechsel in derselben Gruppe | **OK**: «06-12 Mulgore #4 \| Kombiguide (H)» |
| 6 | Testlog | BERUF, RXP, QUEST, TOD | **OK** |

## Befunde

1. **Weg A mit Berufen funktioniert:** Einfügen an Ankern, Bedingungen (`.train`, `.collect`) und `#next` innerhalb der eigenen Gruppe laufen in RXP v4.11.13.
2. **Koordinaten-Fehler, Ursache gefunden:**
   - Die Forever-Koordinaten von Icy Veins waren mit einer Formel umgerechnet, die aus RXPs Kommentar-Koordinaten (`--c:Mulgore,x,y`) stammte. Diese Kommentare passen nicht zur Forever-Karte. RXPs eigentliche Weltkoordinaten stimmen.
   - Messung aus dem Testlog:

     | NPC | Spiel (Testlog) | RXP-Kommentar |
     |---|---|---|
     | Gart Mistrunner | 44.6 / 76.7 | 45.09 / 75.93 |
     | Baine Bloodhoof (Quest 746) | 46.6 / 63.4 | 47.51 / 60.16 |

   - Daraus folgt: Die Forever-Karte von Mulgore ist rund 1,19-mal grösser (etwa 6091 × 4061 Yards statt 5137 × 3425). Das ist eine Schätzung aus zwei Punkten.
   - Das alte Ziel für Nawka lag dadurch etwa 35 Yards südwestlich. Das passt zur Beobachtung «28 Yards Südwest».
   - **Behoben in v0.1.1:**
     - `tools/build_kombi.py` rechnet über `data/karten/forever_karten.csv` um.
     - Testlog 2 schreibt die exakten Kartengrenzen pro Karte mit (Eintrag `KARTE`, über `C_Map.GetWorldPosFromMapPos` und `C_Map.GetMapWorldSize` aus der Forever-API 1.60.1).
     - Sobald diese Werte da sind, ersetzen sie die Schätzung.
3. **Testlog:**
   - Fehler A (SITZUNG ohne Ort) trat nicht jedes Mal auf.
   - B (Sprachen) blieb.
   - Neu: C, die Zeile ENDE beim Ausloggen zeigte 0 % und keine Karte.
   - Alle drei sind in Testlog 2 behoben; das ist mit `tools/testlog_harness.py` geprüft, im Spiel noch nicht.
4. **Offen:** Wie der deutsche Client die Namen von Nawka und Garan im Guide-Fenster anzeigt.
