# Testlogs

Hier landen Dateien aus dem Spiel, damit Claude sie auswerten kann:

`World of Warcraft\_classic_beta_\WTF\Account\<KONTO>\SavedVariables\KombiTestlog.lua`

Die Datei wird beim Ausloggen oder mit `/reload` geschrieben. Sie enthält Charakternamen und seit Testlog 3.6 auch Bestand, Rezepte und die Briefe des Auktionshauses; sie wird deshalb nicht versioniert (siehe `.gitignore`).

Auswerten:
- Kartenecken: `python3 tools/karte_aus_testlog.py testlogs/KombiTestlog.lua v4.11.23` übernimmt alle Zeilen `KARTE` nach `data/karten/forever_karten.csv`. Text aus `/tl zeigen` geht genauso.
- AH-Preise (Testlog 3.5): `python3 tools/ah_aus_testlog.py testlogs/KombiTestlog.lua` übernimmt die Scans nach `data/preise/` (ohne Realm- und Charakternamen) und schreibt `docs/plan/ah-preise.md`. Text aus `/tl zeigen` geht auch, dann nur die Plan-Gegenstände ohne Preisstufen.
- Abnahme (Testlog 3.6): derselbe Aufruf schreibt `data/preise/ah_abnahme.csv`.
- Empfehlungen (Testlog 3.6): `python3 tools/markt.py testlogs/KombiTestlog.lua` schreibt `build/markt/markt.md` und das Addon `build/markt/KombiDaten/` (gehört nach `Interface\AddOns\KombiDaten`). Beides bleibt ausserhalb des Repos.
- Messwerte, die bleiben sollen, kommen ohne Charakternamen nach `docs/tests/`.
