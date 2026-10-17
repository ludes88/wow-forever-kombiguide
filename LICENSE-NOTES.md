# Lizenzhinweise

## Inhalte aus RestedXP

Alle Guide-Dateien, die Schritte, Quest-IDs, NPC-Namen oder Koordinaten aus RestedXP enthalten, sind Bearbeitungen von:

- RestedXP Guides, https://github.com/RestedXP/RXPGuides
- Lizenz: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0), https://creativecommons.org/licenses/by-nc-sa/4.0/

Das heisst für dieses Repo:

- Nur nicht-kommerziell nutzen und weitergeben.
- Herkunft nennen (steht im Kopf jeder Guide-Datei).
- Bearbeitete RXP-Inhalte stehen unter derselben Lizenz.
- Kenntlich machen, dass etwas geändert wurde.

Betroffen: `addons/RXPGuides_Kombi/*.lua`, `addons/RXPGuides_KombiGuide/*` (erzeugt von `tools/build_kombi.py`) und alles, was die Werkzeuge nach `build/` schreiben. In `data/kombi/plan.csv` stammen Weltkoordinaten in den Spalten `welt_a`/`welt_b` aus RestedXP, wo die Spalte `quelle` das sagt. In `data/kombi/dungeons.csv` stammen Kürzel, Gebiets-IDs und Werte aus RestedXP (`DB/forever/db.lua`). `data/kampf/gewichte_rxp.csv` ist eine Abschrift der Gewichte aus `DB/forever/StatWeights.lua` (RXP v4.11.23); `tools/kampf_aus_testlog.py` nutzt sie für den Bericht `docs/plan/kampf.md`. Aus RXP-Daten abgeleitet sind auch `data/kombi/farmstellen.csv` (Mitte der RXP-Schleifen), `data/kombi/modell_leder.csv` (Anzahlen aus RXP-Kommentaren) und die Angelstellen in `docs/recherche/2026-10-14_goldquellen.md` §3 (aus RXP-Koordinaten umgerechnet).

## Daten Dritter zum Vergleich

`docs/recherche/2026-10-15_haendlerpreise.md` vergleicht Händlerpreise mit wow-classic-items (MIT-Lizenz, https://github.com/nexus-devs/wow-classic-items); übernommen sind nur einzelne Zahlen mit Quelle, keine Dateien.

## Eigene Teile

`addons/KombiTestlog/`, `tools/`, `docs/` und `data/` sind eigene Arbeit. Eine Lizenz dafür ist noch nicht gewählt; ohne Lizenz gilt das Urheberrecht des Autors.
