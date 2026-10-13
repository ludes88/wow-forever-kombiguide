# Messdaten 13.10.2026 (Testlog, Thunder Bluff)

Herkunft: Testlog vom 13.10., 19:17–19:51 Uhr, ein Charakter auf Stufe 15 in Thunder Bluff, RestedXP v4.11.13. Bis 19:50 lief Testlog 1, danach Testlog 2 (nach dem Verknüpfen der AddOns mit dem Repo und `/reload`). Die Datei selbst enthält Charakternamen und liegt nicht im Repo.

Quellen für die Vergleiche:
- Entzaubern in Forever: https://www.wow-professions.com/forever/disenchanting-guide (Tabelle «What You Get» und Zeile «11–15»)
- Entzaubern in Classic, zum Gegencheck: https://warcraft.wiki.gg/wiki/Disenchanting_tables (dort als veraltet markiert)
- RXP-Koordinaten: https://github.com/RestedXP/RXPGuides, Tag v4.11.13, `Guides/forever/*.lua`
- Forever-API: https://github.com/Gethe/wow-ui-source/tree/forever (`Blizzard_APIDocumentationGenerated`)
- Rechnung des Projekts: `data/rechnung/Kreislauf.csv`

## 1. Kartenecken Thunder Bluff (exakt)

Testlog 2 schrieb gleich nach dem Einloggen:

| Karte | Ecke (0,0): Welt-X, Welt-Y | Ecke (1,1): Welt-X, Welt-Y | Grösse |
|---|---|---|---|
| 1456 Thunder Bluff | −850.00, 516.67 | −1545.83, −527.08 | 1043.8 × 695.8 Yards |

- `tools/karte_aus_testlog.py` hat die Zeile in `data/karten/forever_karten.csv` übernommen: a0 = 516.67, b0 = −850.00, a1 = −527.08, b1 = −1545.83 (Status «exakt»).
- **Achsen:** `C_Map.GetWorldPosFromMapPos` liefert (Welt-X, Welt-Y). RXP schreibt `.goto Karte/1,A,B` mit A = Welt-Y (gehört zu Karten-x) und B = Welt-X (gehört zu Karten-y). Beleg: RXPs Schritt für Mooranta, `.goto 1456/1,52.93,-1150.53--c:Thunder Bluff,44.43,43.19`, ergibt mit den gemessenen Ecken genau 44.43 / 43.19.
- **Vergleich mit RXPs Kommentar-Koordinaten (`--c:`), RXP v4.11.13:**

  | Karte | Ecken | RXP-Punkte mit Kommentar | Abweichung Median | Abweichung max |
  |---|---|---|---|---|
  | 1456 Thunder Bluff | exakt (Testlog) | 26 | 0.00 % | 0.00 % |
  | 1412 Mulgore | geschätzt (Testlauf 2) | 442 | 3.47 % | 10.95 % |

  In Thunder Bluff passen RXPs Kommentare also genau zur Forever-Karte, in Mulgore nicht. Für Mulgore ist das nur gegen die Schätzung aus zwei Punkten gemessen. Die exakten Ecken für Mulgore (1412) und das Brachland (1413) fehlen noch.

## 2. Lederverarbeitung 98 → 109

- 19:19 kamen 60 Medium Leather (Mittleres Leder) in die Taschen. Woher, steht nicht im Testlog.
- 19:20–19:25: 15 Herstellungen zu je 4 Medium Leather, zusammen 60.
- 11 Punkte (98 → 109). Ohne Punkt blieben 4 Herstellungen: 1× bei 105, 3× bei 107.
- Rund 8 Sekunden pro Herstellung.
- Welches Rezept, steht nicht im Testlog. Es zählt nur ausgewählte Gegenstände; Garn, Farbe und das Ergebnis gehören nicht dazu.

## 3. Entzaubern (19:25–19:38)

Das Testlog sah 15 Zugänge an Entzauberungsmaterial, je etwa 5 Sekunden auseinander. Dass jeder Zugang eine Entzauberung war, ist **ungeprüft**: Die entzauberten Gegenstände zählt das Testlog nicht.

| Ergebnis | Anzahl | Menge pro Mal | Summe | Anteil |
|---|---|---|---|---|
| Strange Dust (Seltsamer Staub) | 8 | 2–3 | 19 | 53 % |
| Greater Magic Essence (Grosse Magieessenz) | 6 | 1–2 | 9 | 40 % |
| Small Glimmering Shard (Kleiner gleissender Splitter) | 1 | 1 | 1 | 7 % |

- Die Mengen pro Mal passen zur Zeile «11–15» der Forever-Tabelle von wow-professions: 2–3 Strange Dust, 1–2 Greater Magic Essence, Small Glimmering Shard.
- Die Anteile weichen von «Rüstung» ab. wow-professions nennt für grüne Rüstung 75 % Staub und 20 % Essenz, für grüne Waffen 20 % Staub und 75 % Essenz, Splitter 3–5 %.
- Rechnung: Wären alle 15 Teile Rüstung gewesen, kämen höchstens 8 Staub in rund 6 % der Fälle vor (Binomialverteilung, n = 15, p = 0,75). Eine Mischung aus Rüstung und Waffen würde die Anteile erklären. Was entzaubert wurde, steht nicht im Testlog.
- Die Rechnung (`Kreislauf.csv`) rechnet für LW-Teile mit 75 / 20 / 4 %, also mit Rüstung. Die Messung widerlegt das nicht, weil die Art der Teile unbekannt ist.

## 4. Grosse in Geringe Magieessenz (19:39)

- 9 Greater Magic Essence wurden zu 27 Lesser Magic Essence, also 1 : 3.

## 5. Verzauberkunst 80 → 100 (19:40–19:46)

- 20 Herstellungen, 20 Punkte (jede gab einen Punkt).
  - 13× je 2 Lesser Magic Essence (80 → 93)
  - 7× je 2 Strange Dust (93 → 100)
- Rund 8–10 Sekunden pro Herstellung.
- Welche Rezepte, steht nicht im Testlog. Weitere Zutaten zählt es nicht.
- Rest danach: 1 Lesser Magic Essence, 5 Strange Dust, 3 Small Glimmering Shard.

## 6. Testlog 2 und Guide-Addons

- Nach `/reload` meldete die SITZUNG «Kombiguide 0.1.1-v4.11.13» und «Testlog 2». Die verknüpften Addons laufen also aus dem Repo.
- «Kombi-Test nicht geladen»: Das WC-Test-Addon `RXPGuides_Kombi` lag vor dem Verknüpfen nicht im AddOns-Ordner und lief nach `/reload` nicht. Die Ursache ist **ungeprüft**; denkbar sind ein Haken in der AddOns-Liste oder dass ein neues Addon erst nach einem Neustart erkannt wird. Für den Kombi-Guide ist es nicht nötig.
- KARTE kam sofort nach dem Einloggen, für die aktuelle Karte.

## 7. Grenzen des Testlogs (Stand Testlog 2)

- Es zählt nur ausgewählte Gegenstände. Rezept, Ergebnis und die entzauberten Gegenstände fehlen deshalb.
- **Vorschlag, offen:** Herstellen und Entzaubern über das Ereignis `UNIT_SPELLCAST_SUCCEEDED` mit Zauber-ID festhalten. In der Forever-API ist es als `SecretWhenUnitSpellCastRestricted` markiert (`UnitDocumentation.lua`). Ob es beim Herstellen lesbar ist, ist **ungeprüft**.
