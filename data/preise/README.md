# Eigene AH-Preise

Erzeugt von `tools/ah_aus_testlog.py` aus dem Testlog (seit Version 3.5 AH-Scan beim Öffnen des Auktionshauses). Nicht von Hand ändern.

- `ah_eigen.csv`: pro Scan und beobachtetem Gegenstand Tiefstpreis, Median, Menge, Angebote und was die billigsten 20 und 100 Stück kosten (Silber). Beobachtet sind der Plan, `/tl item` und seit Testlog 3.6 alle Reagenzien und Ergebnisse der gelernten Rezepte. Neue Scans kommen dazu, alte bleiben; daraus die Wochenpreise.
- `ah_alle.csv`: der letzte Scan mit allen Gegenständen.
- `ah_abnahme.csv` (seit Testlog 3.6): pro Scan und beobachtetem Gegenstand, was seit dem Scan davor von den billigsten Angeboten fehlt. Gezählt werden nur Angebote, die bis dahin nicht ablaufen konnten, von unten bis zur ersten Preisstufe, auf der noch etwas liegt. `weg` = verschwunden (gekauft oder zurückgezogen), `gekauft` = weg minus neue Angebote bis zu diesem Preis, eine Schätzung: zu hoch, wenn jemand zurückzieht und teurer neu einstellt; zu tief, wenn neue Angebote dazukommen. Ganz verschwundene Gegenstände fehlen (gekauft oder zurückgezogen, unbekannt). Annahme: Käufer nehmen die billigsten zuerst (Waren). `stunden` = Abstand der beiden Scans.
- `haendler_ankauf.csv`: was der Händler im Forever-Client für einen Gegenstand zahlt (`C_Item.GetItemInfo`, «sellPrice»), aus den Gegenstands-Infos (Testlog 3.6) und den AH-Scans (Testlog 3.7). Ein geänderter Wert ersetzt den alten mit neuem Datum. Classic-Datenbanken nennen für viele hergestellte Teile höhere Werte (`docs/recherche/2026-10-15_haendlerpreise.md`).
- Markt = Region, Fraktion, Kurzzeichen des Realms (statt des Namens), Beta oder Live. Keine Realm- und Charakternamen.
- Bericht: `docs/plan/ah-preise.md`. Mit `--eintragen` kommt der 7-Tage-Median als Preis «jetzt» in `data/rechnung/Preise.csv` und in die AH-Zeilen von `data/kombi/preise_zusatz.csv` (nur aus vollständigen Scans und bei mindestens 50 Stück im Angebot; danach `tools/plan_berufe.py`; offene Entscheidung 17).
- Empfehlungen daraus rechnet `tools/markt.py`; dessen Ausgabe enthält den eigenen Bestand und bleibt in `build/` (nicht im Repo).
