@echo off
rem ----------------------------------------------------------------------------
rem  aktualisieren.bat  (nur beim frueheren Weg mit Verknuepfung)
rem  Holt den neusten Stand von GitHub. Sind die Addons verknuepft
rem  (addons_verknuepfen.bat), hat das Spiel danach sofort die neue Version.
rem  Nach kombi_einrichten.bat (Entscheid vom 15.10.2026, Punkt 25) schreibt
rem  Claude die Addons selbst; dann holt diese Datei nur noch den Klon
rem  zum Nachsehen.
rem ----------------------------------------------------------------------------
set "REPO=%~dp0..\.."
git -C "%REPO%" pull --ff-only
echo.
echo Im Spiel /reload eingeben.
pause
