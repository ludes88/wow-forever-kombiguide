# Vorgehen: vom Plan zum Kombi-Guide

Stand 13.10.2026. Entscheidungen liegen beim Nutzer (siehe `entscheidungen.md`); hier steht, wie gearbeitet wird.

## Arbeitsweise (Entscheidung des Nutzers vom 13.10.2026)

- Claude arbeitet direkt in diesem Repo: Branch, Commit, Pull Request. Nach den automatischen Prüfungen führt Claude selbst zusammen (Merge).
- Für Recherche, Mengen-Rechnung und Bauen kann Claude parallele Agenten einsetzen.
- Sobald die Sitzung mit dem PC des Nutzers verbunden ist, legt Claude neue Addon-Versionen selbst in den AddOns-Ordner und liest die Testlog-Datei selbst. Die Testlog-Datei enthält Charakternamen und kommt NIE ins Repo.
- Die Arbeit des Nutzers pro Runde: spielen, `/reload`, Bescheid geben.

## Datenkette statt Handarbeit

1. **Plan-Tabelle** `data/kombi/plan.csv`
   - Semikolon, UTF-8, lässt sich in Excel öffnen.
   - Eine Zeile pro Berufsschritt. Hier stehen die Entscheidungen: wo im Guide (Anker), was (Aktion), welche Item- oder Zauber-ID, wie viel, Bedingung, Ort, Quelle, Status.
   - Spalten:
     - `nr`, `guide` (Name des RXP-Guides), `anker` (z. B. `accept 1656`, `turnin 768`, `label Name`), `position` (`vor`/`nach`)
     - `aktion` (zurzeit `lernen`, `kaufen`), `id`, `menge`
     - `karte`, `x`, `y` (Spielkoordinaten in Prozent, wie im Testlog), alternativ `welt_a`/`welt_b` (RXP-Weltkoordinaten, wenn RXP den NPC schon kennt)
     - `npc` (englischer Name, RXP übersetzt), `text` (deutscher Text, `{npc}` wird eingesetzt), `kurz` (Text am Element), `bedingung` (eine rohe RXP-Zeile, z. B. `.skill skinning,<1,1`)
     - `quelle`, `status`
2. **Kartentabelle** `data/karten/forever_karten.csv`
   - Pro Karte die RXP-Weltkoordinaten der Kartenecken (0,0) und (1,1).
   - Werte aus dem Testlog-Eintrag `KARTE` sind exakt; Schätzungen sind als solche markiert.
3. **Mengen-Rechnung** (geplant, `tools/plan_mengen.py`): verteilt den Gesamtbedarf auf die Gebiete der Route.
   - Gesamtbedarf aus `data/rechnung/`, z. B. 416 Leichtes Leder für LW 125.
   - Kürschnerbare Gegner pro Gebiet aus den RXP-Schritten.
   - Ausbeute nach Gegnerstufe aus MetaForge und AHledger, später aus dem Testlog (TASCHE pro Gebiet und Zeit).
   - Wo die Route nicht reicht: Farm-Stopp vorschlagen oder Lücke offen zeigen.
4. **Generator** `tools/build_kombi.py`: liest Plan- und Kartentabelle, baut die RXP-Gratis-Route in genau der RXP-Version des Nutzers neu und fügt die Schritte ein.
5. **Prüfung** (automatisch im Generator):
   - Lua-Syntax, Kopf, bekannte Befehle
   - jeder Anker genau einmal, jede Plan-Zeile eingefügt
   - kein `--` und kein `[[`/`]]` in eigenen Texten, Koordinaten 0–100
6. **Spieltest** mit KombiTestlog, dann Auswertung durch Claude, dann Plan anpassen, neue Version bauen und austauschen. Der Fortschritt bleibt, solange Gruppe und Guide-Namen gleich bleiben (T6).

## Versionen

| Version | Inhalt | Stand |
|---|---|---|
| 0.1 | Kürschnermesser, Kürschnerei und Kräuterkunde in Camp Narache | im Spiel getestet (Testlauf 2) |
| 0.1.1 | Koordinaten über Kartentabelle; Testlog 2 (Fehler A–C behoben, Kartengrenzen, Sitzung meldet Kombiguide) | gebaut und geprüft, im Spiel offen |
| 0.2 | Mulgore 6–12 und Thunder Bluff: Kürschnern und Kräuter mit Zielen aus der Rechnung, Kochen und Fischen, soweit nicht in der RXP-Route | geplant |
| 0.3 | Brachland bis zum Wechsel auf Lederverarbeitung und Verzauberkunst um Stufe 15 | geplant |
| 0.4 | 17–22, Lager-Gegenstände, Merchant's Favor, Schlafsack-Strang (79007 ist in RXP) | geplant |

Die Beta läuft bis 22.10.2026 (Stufen-Grenze 30). Bis dahin lassen sich Messdaten sammeln.
