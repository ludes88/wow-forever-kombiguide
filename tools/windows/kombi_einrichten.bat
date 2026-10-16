@echo off
setlocal EnableExtensions EnableDelayedExpansion
rem ----------------------------------------------------------------------------
rem  kombi_einrichten.bat  (einmal ausfuehren, Entscheidung vom 15.10.2026, Punkt 25)
rem  Claude installiert die Addons ab jetzt selbst. Dafuer duerfen die Addon-
rem  Ordner nicht mehr mit dem Repo-Klon verknuepft sein: Sonst landen Claudes
rem  Dateien im Klon, und "git pull" (aktualisieren.bat) bricht danach ab.
rem
rem  Was die Datei tut:
rem   1. entfernt in Interface\AddOns die Verknuepfungen KombiTestlog,
rem      RXPGuides_KombiGuide und RXPGuides_Kombi (nur die Verknuepfung, der
rem      Klon bleibt unveraendert); echte Ordner gleichen Namens kommen nach
rem      AddOns\_alt_kombi
rem   2. holt die neuen Addon-Ordner aus _kombi_neu (dort hat Claude sie
rem      abgelegt) nach Interface\AddOns
rem  Danach: Spiel starten oder im Spiel /reload. Die Testlog-Daten bleiben
rem  (sie liegen in WTF\...\SavedVariables, nicht im Addon-Ordner).
rem
rem  Erwartet: diese Datei liegt im Ordner _classic_beta_ (neben Interface und
rem  WTF). Klappt etwas nicht: Rechtsklick, "Als Administrator ausfuehren".
rem ----------------------------------------------------------------------------

set "BASIS=%~dp0"
set "ADDONS=%BASIS%Interface\AddOns"
set "NEU=%BASIS%_kombi_neu"
set "ALT=%ADDONS%\_alt_kombi"

rem Pfade nie ungeschuetzt in Klammer-Bloecken ausgeben: "Program Files (x86)"
rem enthaelt eine Klammer, die den Block beendet; cmd bricht dann sofort ab
rem (Fenster geht gleich wieder zu, gemeldet am 16.10.2026).
if not exist "%ADDONS%\" goto :keine_addons
if not exist "%NEU%\" goto :kein_neu

echo AddOns: %ADDONS%
echo Neu:    %NEU%
echo.
set "FEHLER=0"
for %%A in (KombiTestlog RXPGuides_KombiGuide RXPGuides_Kombi) do call :ersetzen %%A
echo.
if "%FEHLER%"=="0" (
  rmdir "%NEU%" 2>nul
  echo Fertig. Spiel starten oder im Spiel /reload eingeben.
  echo Ab jetzt schreibt Claude neue Versionen direkt in diese Ordner.
) else (
  echo Es gab Fehler, siehe oben. Nichts wurde in den Repo-Klon geschrieben.
)
pause
exit /b 0

:keine_addons
echo AddOns-Ordner nicht gefunden: "%ADDONS%"
echo Diese Datei muss im Ordner _classic_beta_ liegen.
pause
exit /b 1

:kein_neu
echo Ordner _kombi_neu fehlt: "%NEU%"
echo Claude legt ihn an, ohne ihn gibt es nichts zu installieren.
pause
exit /b 1

:ersetzen
set "NAME=%~1"
if not exist "%NEU%\%NAME%\" (
  echo [uebersprungen] %NAME%: keine neue Version in _kombi_neu
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
if exist "%ADDONS%\%NAME%\" (
  echo [FEHLER] %NAME% liess sich nicht entfernen; nichts geaendert
  set "FEHLER=1"
  exit /b 0
)
move "%NEU%\%NAME%" "%ADDONS%\%NAME%" >nul && (echo [installiert] %NAME%) || (echo [FEHLER] %NAME% liess sich nicht verschieben & set "FEHLER=1")
exit /b 0
