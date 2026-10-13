# Testlauf 1 – Addons im Spiel (13.10.2026, abgeschlossen)

Ziel: Laufen die eigenen Addons aus dem Repo im Forever-Beta-Client mit RXP? Getestet wurden T0 und ein Teil von T1: KombiTestlog (Version 1) und der WC-Test-Guide (`addons/RXPGuides_Kombi`). Stand Commit 0323e21, RestedXP v4.11.13 beim Nutzer.

## Ergebnis

| Nr. | Handlung | Erwartet | Ergebnis |
|---|---|---|---|
| 1 | Charakterauswahl → AddOns | beide Addons aktiv | **OK** (indirekt: beide geladen) |
| 3 | `/tl zeigen` | `SITZUNG` mit Client, RXP-Version, Versionen | **OK**: Client 1.60.1 (70338), RXP v4.11.13, Kombi-Guide 1, Testlog 1. Charakter Stufe 15 |
| 4 | RXP-Guide-Auswahl | Gruppe «Kombiguide Tests» | **OK.** Im Guide-Fenster: Rechtsklick auf den Guide-Namen oder Zahnrad → «Verfuegbare Guides». Das Fenster «RestedXP Guides v4.11.13» sind die Einstellungen |
| 5 | Guide laden | passender Schritt | **OK**: RXP springt nach Queststand auf #7 und #8 |
| 6 | `/tl …` | NOTIZ | **OK** |
| 7 | `/reload` | Speichern | **OK**: ENDE, danach neue SITZUNG; der Guide bleibt bei #8 |
| 9 | Eindruck des Nutzers | – | «sieht alles perfekt aus und reagiert auch perfekt» |

## Befunde

1. **T0 bestanden.** Testlog und eigener Guide laden im Forever-Client 1.60.1 (70338).
2. **Kernfrage von Weg A beantwortet:** Ein eigener Guide, den ein eigenes Addon über `RXPGuides.RegisterGuide` lädt, erscheint in RestedXP unter einer eigenen Gruppe, lädt und springt nach dem Queststand an die passende Stelle. Der Fortschritt bleibt über `/reload` erhalten.
3. **RXP-Version beim Nutzer: v4.11.13** (Tag vom 03.10.), 110 Commits älter als v4.11.23 (10.10.). Der WC-Guide ist gegen v4.11.13 geprüft. Ob RXP aktualisiert wird, entscheidet der Nutzer.
4. **Testlog-Fehler A:** SITZUNG beim frischen Einloggen ohne Ort und mit Kontinent-Karte (1414). Behoben in Testlog 2: Start erst nach `PLAYER_ENTERING_WORLD`.
5. **Testlog-Fehler B:** Sprachen («Sprache: Orcisch 300/300») in der Berufsliste. Behoben in Testlog 2.
6. **Bedienung:** `/tl bug` für Probleme, `/tl <Text>` für Notizen und Eindrücke, `/tl idee` für Ideen.
