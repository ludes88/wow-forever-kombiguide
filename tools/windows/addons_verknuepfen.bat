@echo off
setlocal EnableExtensions EnableDelayedExpansion
rem ----------------------------------------------------------------------------
rem  addons_verknuepfen.bat  (einmal ausfuehren)
rem  Verknuepft die Addons aus diesem Repo mit dem AddOns-Ordner von WoW
rem  (Verzeichnis-Verknuepfung, "Junction"). Danach genuegt "git pull" bzw.
rem  aktualisieren.bat, und das Spiel hat die neue Version (im Spiel /reload;
rem  einen neu verknuepften Ordner laedt das Spiel erst nach einem Neustart).
rem  Seit 15.10.2026 (Entscheid Punkt 25) installiert Claude die Addons selbst:
rem  dafuer stattdessen einmal kombi_einrichten.bat ausfuehren.
rem
rem  Aufruf: den Ordner  ...\_classic_beta_\Interface\AddOns  mit der Maus auf
rem  diese Datei ziehen. Ohne Ordner wird der uebliche Pfad versucht oder
rem  nachgefragt. Vorhandene Ordner gleichen Namens werden NICHT geloescht,
rem  sondern nach AddOns\_alt_kombi verschoben.
rem ----------------------------------------------------------------------------

set "REPO=%~dp0..\.."
for %%I in ("%REPO%") do set "REPO=%%~fI"

set "ADDONS=%~1"
if "%ADDONS%"=="" set "ADDONS=C:\Program Files (x86)\World of Warcraft\_classic_beta_\Interface\AddOns"
if not exist "%ADDONS%\" (
  echo AddOns-Ordner nicht gefunden: !ADDONS!
  set /p "ADDONS=Pfad zum Ordner _classic_beta_\Interface\AddOns eingeben: "
)
if not exist "%ADDONS%\" (
  echo Ordner gibt es nicht: !ADDONS!
  pause
  exit /b 1
)

echo Repo:   %REPO%
echo AddOns: %ADDONS%
echo.
set "ALT=%ADDONS%\_alt_kombi"
for %%A in (KombiTestlog RXPGuides_KombiGuide RXPGuides_Kombi) do call :link %%A
echo.
echo Fertig. Das Spiel neu starten (neu verknuepfte Ordner laedt es erst dann).
echo Klappt etwas nicht: Rechtsklick auf diese Datei, "Als Administrator ausfuehren".
pause
exit /b 0

:link
set "NAME=%~1"
if not exist "%REPO%\addons\%NAME%\" (
  echo [uebersprungen] %NAME% gibt es im Repo nicht
  exit /b 0
)
if exist "%ADDONS%\%NAME%\" (
  set "ATTR="
  for %%F in ("%ADDONS%\%NAME%") do set "ATTR=%%~aF"
  if /i "!ATTR:~-1!"=="l" (
    rmdir "%ADDONS%\%NAME%"
  ) else (
    if not exist "%ALT%\" mkdir "%ALT%"
    move "%ADDONS%\%NAME%" "%ALT%\%NAME%_!RANDOM!" >nul && echo [beiseite gelegt] alter Ordner %NAME% nach _alt_kombi
  )
)
mklink /J "%ADDONS%\%NAME%" "%REPO%\addons\%NAME%" >nul && (echo [verknuepft] %NAME%) || (echo [FEHLER] %NAME% konnte nicht verknuepft werden)
exit /b 0
