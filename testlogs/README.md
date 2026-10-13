# Testlogs

Hier landen Dateien aus dem Spiel, damit Claude sie auswerten kann:

`World of Warcraft\_classic_beta_\WTF\Account\<KONTO>\SavedVariables\KombiTestlog.lua`

Die Datei wird beim Ausloggen oder mit `/reload` geschrieben. Sie enthält Charakternamen und wird deshalb nicht versioniert (siehe `.gitignore`).

Auswerten:
- Kartenecken: `python3 tools/karte_aus_testlog.py testlogs/KombiTestlog.lua v4.11.13` übernimmt alle Zeilen `KARTE` nach `data/karten/forever_karten.csv`. Text aus `/tl zeigen` geht genauso.
- Messwerte, die bleiben sollen, kommen ohne Charakternamen nach `docs/tests/`.
