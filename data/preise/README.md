# Eigene AH-Preise

Erzeugt von `tools/ah_aus_testlog.py` aus dem Testlog (seit Version 3.5 AH-Scan beim Öffnen des Auktionshauses). Nicht von Hand ändern.

- `ah_eigen.csv`: pro Scan und beobachtetem Gegenstand Tiefstpreis, Median, Menge, Angebote und was die billigsten 20 und 100 Stück kosten (Silber). Beobachtet sind der Plan, `/tl item` und seit Testlog 3.6 alle Reagenzien und Ergebnisse der gelernten Rezepte. Neue Scans kommen dazu, alte bleiben; daraus die Wochenpreise.
- `ah_alle.csv`: der letzte Scan mit allen Gegenständen.
- `ah_abnahme.csv` (seit Testlog 3.6): pro Scan und beobachtetem Gegenstand, was seit dem Scan davor von den billigsten Angeboten fehlt. Gezählt werden nur Angebote, die bis dahin nicht ablaufen konnten, von unten bis zur ersten Preisstufe, auf der noch etwas liegt. `weg` = verschwunden (gekauft oder zurückgezogen), `gekauft` = weg minus neue Angebote bis zu diesem Preis, eine Schätzung: zu hoch, wenn jemand zurückzieht und teurer neu einstellt; zu tief, wenn neue Angebote dazukommen. Ganz verschwundene Gegenstände fehlen (gekauft oder zurückgezogen, unbekannt). Annahme: Käufer nehmen die billigsten zuerst (Waren). `stunden` = Abstand der beiden Scans.
- Markt = Region, Fraktion, Kurzzeichen des Realms (statt des Namens), Beta oder Live. Keine Realm- und Charakternamen.
- Bericht: `docs/plan/ah-preise.md`. Mit `--eintragen` kommt der 7-Tage-Median als Preis «jetzt» in `data/rechnung/Preise.csv` (offene Entscheidung 17).
- Empfehlungen daraus rechnet `tools/markt.py`; dessen Ausgabe enthält den eigenen Bestand und bleibt in `build/` (nicht im Repo).
