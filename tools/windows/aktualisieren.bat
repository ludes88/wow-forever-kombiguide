@echo off
rem ----------------------------------------------------------------------------
rem  aktualisieren.bat  (nach jeder neuen Version doppelklicken)
rem  Holt den neusten Stand von GitHub. Sind die Addons verknuepft
rem  (addons_verknuepfen.bat), hat das Spiel danach sofort die neue Version.
rem ----------------------------------------------------------------------------
set "REPO=%~dp0..\.."
git -C "%REPO%" pull --ff-only
echo.
echo Im Spiel /reload eingeben.
pause
