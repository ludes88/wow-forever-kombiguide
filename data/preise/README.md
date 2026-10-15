# Eigene AH-Preise

Erzeugt von `tools/ah_aus_testlog.py` aus dem Testlog (Version 3.5, AH-Scan beim Öffnen des Auktionshauses). Nicht von Hand ändern.

- `ah_eigen.csv`: pro Scan und Gegenstand des Plans Tiefstpreis, Median, Menge, Angebote und was die billigsten 20 und 100 Stück kosten (Silber). Neue Scans kommen dazu, alte bleiben; daraus die Wochenpreise.
- `ah_alle.csv`: der letzte Scan mit allen Gegenständen.
- Markt = Region, Fraktion, Kurzzeichen des Realms (statt des Namens), Beta oder Live. Keine Realm- und Charakternamen.
- Bericht: `docs/plan/ah-preise.md`. Mit `--eintragen` kommt der 7-Tage-Median als Preis «jetzt» in `data/rechnung/Preise.csv` (offene Entscheidung 17).
