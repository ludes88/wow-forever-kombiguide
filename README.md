# WoW Forever: Kombi-Guide und Berufe

Ein RestedXP-Guide für Stufe 1–22 (Horde, Tauren-Druide), der RXPs Gratis-Route mit Berufsschritten verbindet: Kräuterkunde und Kürschnerei bis etwa Stufe 15, danach Lederverarbeitung und Verzauberkunst bis 150, dazu Fischen und Kochen.

Stand 15.10.2026: Kombi-Guide v0.4 auf Basis RestedXP v4.11.23 (Berufsschritte in Mulgore, Leder bis zum Sweetspot, Berufswechsel in Orgrimmar mit Stückzahlen für Herstellen, Entzaubern, Verzaubern und Einkauf, Rest bis 150 in Thunder Bluff), Testlog 3.5 (mit Lehrerlisten und AH-Scan beim Öffnen des Auktionshauses); im Spiel getestet bis v0.2 (Forever-Beta). Testberichte in `docs/tests/`, Mengenmodell in `docs/plan/mengen-leder.md`, Berufe-Plan in `docs/plan/berufe-plan.md`.

## Inhalt

- `addons/KombiTestlog/`: Notizen und Testprotokoll im Spiel (`/tl hilfe`)
- `addons/RXPGuides_Kombi/`: eigene RXP-Guides, zurzeit der Test «Vorquests Höhlen des Wehklagens»
- `data/kombi/plan.csv`: Plan-Tabelle der Berufsschritte (lässt sich in Excel öffnen); die übrigen Tabellen in `data/kombi/` sind die Eingaben des Mengenmodells
- `data/karten/forever_karten.csv`: Kartenecken für die Koordinaten-Umrechnung
- `docs/Weg-A_Best-Practice.md`: Aufbau, RXP-Syntax, Update-Ablauf, Risiken, Berufsdaten, Testplan
- `docs/vorgehen.md`: Arbeitsweise, Datenkette, Versionen
- `docs/tests/messplan-beta.md`: Messplan für die Beta (welche Messung welche Zahl ersetzt); `docs/recherche/`: Recherchen mit Quellen und Datum, z. B. Goldquellen
- `tools/`: Kombi-Guide bauen (`build_kombi.py`), Mengenmodell (`plan_mengen.py`), Berufe-Plan (`plan_berufe.py`), RXP-Schritte lesen und Stellen prüfen (`rxp_schritte.py`), Kartenecken aus dem Testlog übernehmen (`karte_aus_testlog.py`), Prüfen, Testlauf
- `data/rechnung/`: Rechnung Lederverarbeitung und Verzauberkunst
- `data/preise/`: eigene AH-Preise aus dem Testlog (`tools/ah_aus_testlog.py`), Bericht `docs/plan/ah-preise.md`

## Einbau ins Spiel (Beta)

Einmal: den Ordner `World of Warcraft\_classic_beta_\Interface\AddOns` mit der Maus auf `tools\windows\addons_verknuepfen.bat` ziehen. Das Skript verknüpft `KombiTestlog`, `RXPGuides_KombiGuide` und `RXPGuides_Kombi` aus diesem Repo mit dem AddOns-Ordner (Verzeichnis-Verknüpfung). Vorhandene Ordner gleichen Namens verschiebt es nach `AddOns\_alt_kombi`, es löscht nichts.

Danach bei jeder neuen Version: `tools\windows\aktualisieren.bat` doppelklicken (oder `git pull`) und im Spiel `/reload`.

Ohne Skript: die drei Ordner aus `addons/` nach `World of Warcraft\_classic_beta_\Interface\AddOns\` kopieren, neben `RXPGuides`.

`addons/RXPGuides_KombiGuide/` ist erzeugt: `python3 tools/build_kombi.py <RXP-Version> addons`. Nicht von Hand ändern, sondern `data/kombi/plan.csv`.

## Herkunft

Die Guide-Schritte stammen aus den RestedXP-Gratis-Guides (https://github.com/RestedXP/RXPGuides, CC BY-NC-SA 4.0) und sind bearbeitet. Siehe `LICENSE-NOTES.md`.
