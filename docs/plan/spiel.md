# Spieldaten: Stufen, Gebiete, XP, Laufweg, Dungeons (erzeugt von `tools/spiel_aus_testlog.py`)

Nicht von Hand ändern: neues Testlog einlesen und neu erzeugen. Ohne Charakternamen und Uhrzeiten.

## Quellen

- Protokoll des Testlogs (alle Versionen): «L16 68%» in jeder Zeile = Stufe und Prozent der Stufe; QUEST AB mit XP; TOD.
- Testlog 3.7: XP pro Quelle (`PLAYER_XP_UPDATE`, Quelle nach Kampf, Ziel und Quest-Abgabe), Laufweg (alle 10 s, bei Stillstand alle 60 s), Dungeon-Läufe (`IsInInstance`, `GetInstanceInfo`); APIs laut Forever-UI 1.60.1 (70374), https://github.com/Gethe/wow-ui-source/tree/forever.
- Grenzen: Zeit pro Gebiet aus dem Abstand zweier Protokollzeilen (Lücken über 10 Minuten zählen als 10); Stufen-Fortschritt aus den ganzen Prozent; Sitzungen unter 3 Minuten fehlen. Sitzungen mit Berufen, Auktionshaus oder Tests bringen wenig Stufen pro Stunde; das ist kein Mass für die Route.

## Sitzungen

| Datum | Dauer | Stufe | Stufen pro Stunde | Quests (XP) | Tode | Gebiete (Minuten) | RXP | Kombiguide |
|---|---|---|---|---|---|---|---|---|
| 2026-10-13 | 17 Min | 5.87 → 6.00 | 0.46 | 0 (0) | 1 | Mulgore 17 | 06-12 Mulgore #13 → 06-12 Mulgore #13 | – |
| 2026-10-13 | 7 Min | 15.70 → 15.70 | 0.00 | 0 (0) | 0 | Thunder Bluff 7 | WC Vorquests #8 → 12-17 The Barrens #52 | – |
| 2026-10-13 | 34 Min | 15.70 → 15.70 | 0.00 | 0 (0) | 0 | Thunder Bluff 32 | 12-17 The Barrens #52 → 12-17 The Barrens #58 | – |
| 2026-10-13 | 8 Min | 15.70 → 15.70 | 0.00 | 0 (0) | 0 | Thunder Bluff 8, ? 0 | 12-17 The Barrens #77 → WC Vorquests #8 | – |
| 2026-10-13 | 21 Min | 15.70 → 15.70 | 0.00 | 0 (0) | 0 | Thunder Bluff 15, Brachland 3, Mulgore 2 | 12-17 The Barrens #58 → 12-17 The Barrens #77 | 0.1.1-v4.11.13 |
| 2026-10-13 | 6 Min | 15.70 → 15.70 | 0.00 | 0 (0) | 0 | Brachland 3, Thunder Bluff 3, Mulgore 1 | 12-17 The Barrens #77 → 12-17 The Barrens #77 | 0.1.1-v4.11.13 |
| 2026-10-13 | 34 Min | 6.00 → 7.46 | 2.57 | 6 (2715) | 1 | Mulgore 34 | 06-12 Mulgore #13 → 06-12 Mulgore #28 | 0.1.2-v4.11.13 |
| 2026-10-14 | 9 Min | 7.46 → 7.74 | 1.92 | 2 (820) | 0 | Mulgore 9 | 06-12 Mulgore #30 → 06-12 Mulgore #45 | 0.3-v4.11.23 |
| 2026-10-15 | 70 Min | 15.97 → 16.67 | 0.60 | 2 (2150) | 2 | Die Ruinen von Lordaeron 29, Brachland 20, Orgrimmar 12 | 12-17 The Barrens #84 → 12-17 The Barrens #103 | 0.4-v4.11.23 |
| 2026-10-15 | 12 Min | 18.56 → 18.56 | 0.00 | 0 (0) | 0 | Orgrimmar 12 | 12-17 The Barrens #152 → 12-17 The Barrens #152 | 0.5-v4.11.23 |
| 2026-10-15 | 60 Min | 16.68 → 18.56 | 1.89 | 17 (31825) | 0 | Orgrimmar 20, Brachland 14, Die Ruinen von Lordaeron 11 | 12-17 The Barrens #103 → 12-17 The Barrens #152 | 0.4-v4.11.23 |
| 2026-10-15 | 15 Min | 15.70 → 15.97 | 1.07 | 1 (750) | 0 | Brachland 15 | 12-17 The Barrens #77 → 12-17 The Barrens #84 | 0.4-v4.11.23 |

## Gebiete und Stufen (aus dem Protokoll, alle Sitzungen)

| Gebiet | Stufe | Minuten | Stufen | pro Stunde | Quests (XP) | Tode | Sitzungen |
|---|---|---|---|---|---|---|---|
| Mulgore | 5 | 11 | 0.13 | 0.73 | 0 (0) | 0 | 1 |
| Mulgore | 6 | 23 | 1.04 | 2.69 | 4 (1640) | 1 | 2 |
| Mulgore | 7 | 26 | 0.70 | 1.63 | 4 (1895) | 1 | 2 |
| Brachland | 15 | 22 | 0.30 | 0.82 | 1 (750) | 0 | 4 |
| Mulgore | 15 | 2 | 0.00 | 0.00 | 0 (0) | 0 | 2 |
| Thunder Bluff | 15 | 64 | 0.00 | 0.00 | 0 (0) | 0 | 5 |
| Brachland | 16 | 19 | 0.33 | 1.04 | 1 (1350) | 0 | 1 |
| Die Ruinen von Lordaeron | 16 | 40 | 0.38 | 0.57 | 0 (0) | 2 | 2 |
| Durotar | 16 | 2 | 0.00 | 0.00 | 0 (0) | 0 | 1 |
| Orgrimmar | 16 | 12 | 0.06 | 0.31 | 1 (800) | 0 | 1 |
| Tirisfal | 16 | 6 | 0.00 | 0.00 | 0 (0) | 0 | 1 |
| Undercity | 16 | 5 | 0.34 | 4.08 | 1 (5450) | 0 | 2 |
| Brachland | 17 | 2 | 0.00 | 0.00 | 0 (0) | 0 | 1 |
| Orgrimmar | 17 | 8 | 0.15 | 1.08 | 3 (2650) | 0 | 1 |
| Silberwald | 17 | 4 | 0.26 | 4.00 | 1 (4600) | 0 | 1 |
| Tirisfal | 17 | 3 | 0.26 | 4.73 | 1 (4600) | 0 | 1 |
| Undercity | 17 | 3 | 0.26 | 6.00 | 1 (4600) | 0 | 1 |
| Brachland | 18 | 12 | 0.51 | 2.45 | 10 (9925) | 0 | 1 |
| Orgrimmar | 18 | 24 | 0.00 | 0.00 | 0 (0) | 0 | 2 |

## XP pro Quelle (Testlog 3.7)

Noch keine Daten (ab Testlog 3.7).

## Laufweg pro Karte und Stufe (Testlog 3.7)

Noch keine Daten (ab Testlog 3.7).

## Dungeon-Läufe (Testlog 3.7)

Noch keine Daten (ab Testlog 3.7).
