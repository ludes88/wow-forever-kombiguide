# Testlogs

Hier landen Dateien aus dem Spiel, damit Claude sie auswerten kann:

`World of Warcraft\_classic_beta_\WTF\Account\<KONTO>\SavedVariables\KombiTestlog.lua`

Die Datei wird beim Ausloggen oder mit `/reload` geschrieben. Sie enthält Charakternamen und wird deshalb nicht versioniert (siehe `.gitignore`).

Auswerten:
- Kartenecken: `python3 tools/karte_aus_testlog.py testlogs/KombiTestlog.lua v4.11.23` übernimmt alle Zeilen `KARTE` nach `data/karten/forever_karten.csv`. Text aus `/tl zeigen` geht genauso.
- AH-Preise (Testlog 3.5): `python3 tools/ah_aus_testlog.py testlogs/KombiTestlog.lua` übernimmt die Scans nach `data/preise/` (ohne Realm- und Charakternamen) und schreibt `docs/plan/ah-preise.md`. Text aus `/tl zeigen` geht auch, dann nur die Plan-Gegenstände ohne Preisstufen.
- Messwerte, die bleiben sollen, kommen ohne Charakternamen nach `docs/tests/`.
