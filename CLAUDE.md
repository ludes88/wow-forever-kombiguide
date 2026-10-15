# WoW Forever: Kombi-Guide und Berufe

Ein RestedXP-Guide für Stufe 1–22 (Horde, Tauren-Druide, Start Mulgore): RXPs Gratis-Route mit eigenen Berufsschritten an den passenden Stellen («Weg A»), als Speedrun-Route (Gruppe «Kombiguide (H)») und als Dungeon-Route (Gruppe «Kombiguide Dungeon (H)», seit v0.5). Dazu das Test-Addon KombiTestlog.
Ausführlich, mit Belegen: @docs/Weg-A_Best-Practice.md
Entscheidungen: @docs/entscheidungen.md
Vorgehen und Versionen: @docs/vorgehen.md

## Arbeitsregeln des Nutzers (gelten in jeder Sitzung)

- OBERSTE REGEL: Claude weiss nicht, was gut für den Nutzer ist. Bewertung und Entscheidung liegen immer bei ihm. Keine Absolutismen.
- Quellen zuerst: alle relevanten Quellen mit Link nennen, bevor diskutiert oder gedeutet wird («prüfen statt konsumieren»).
- Prüf-Regel: Jede Ortsangabe, Zahl, Stufe, jeder Preis und Eigenname ist belegt oder ausdrücklich als «ungeprüft» markiert. Gibt es keine Quelle, das sagen statt eine plausible Zahl liefern.
- Blinde Flecken nur als kurzer, markierter «KOMMENTAR:», nie als Blockade.
- Vor Thesen über den Nutzer (Motive, was ihm passt) fragen statt raten.
- Er ist gefühls- und analytisch orientiert zu gleichen Teilen; welche Seite gerade zählt, weiss nur er.
- Schweizer Rechtschreibung: ss statt ß.
- Antworten an den Nutzer enden mit einer Zeile «Tags: {…}» (sein Codewort-System, z. B. `Tags: {Gaming}`).

## Repo-Karte

| Ordner | Inhalt |
|---|---|
| `addons/RXPGuides_Kombi/` | eigene RXP-Guides (Test: Vorquests Höhlen des Wehklagens) |
| `addons/KombiTestlog/` | Notizen- und Protokoll-Addon, `/tl hilfe` (Version 3.6: Kartengrenzen `KARTE`, dazu Herstellen, Entzaubern, Sammeln, Beute, Händler, Geld, Lehrerlisten `LEHRER`, AH-Scan `AH-SCAN` mit Abnahme, Daten in `KombiTestlogDB.ahScans`; Rezepte `REZEPTE`, Bestand `INVENTAR`, `AH-POST`, `AH-ANGEBOT`, Daten in `chars`, `kontobank`, `ahPost`, `info`; `/tl tipp` zeigt das Addon `KombiDaten`; Liste im Dateikopf) |
| `addons/RXPGuides_KombiGuide/` | der Kombi-Guide, ERZEUGT von `build_kombi.py` (nie von Hand ändern); eine Datei mit zwei Gruppen: «Kombiguide (H)» (RXP-Speedrun-Route) und «Kombiguide Dungeon (H)» (RXP-Dungeon-Route, WIP, Dungeons aus `data/kombi/dungeons.csv` fest eingebaut) |
| `tools/windows/` | `addons_verknuepfen.bat` (einmal: AddOns ↔ Repo verknüpfen), `aktualisieren.bat` (`git pull`) für den Nutzer |
| `data/kombi/plan.csv` | Plan-Tabelle: eine Zeile pro Berufsschritt (Anker, Aktion, ID, Menge, Ort, bis, extra, Quelle, Status), gilt für beide Gruppen; `VERSION`; `dungeons.csv` (welche Dungeons die Dungeon-Route enthält, `an` = ja/nein) |
| `data/kombi/*.csv` (ausser plan.csv) | Mengenmodell Leder bis zum Wechsel in Orgrimmar: `abschnitte`, `modell_leder` (Quests mit Tieren), `kuerschnern_anteile`, `farmstellen`, `farmstopps`, `bedarf_lw_vz` (LW/VZ 1–150, Spalte `variante`), alle mit Quelle; `tools/plan_mengen.py` macht daraus `docs/plan/mengen-leder.md`. Berufe-Plan: `rezepte` (Lernstufen laut AHledger), `items` (Item-IDs), `preise_zusatz` (Händlerpreise, Fisch); `tools/plan_berufe.py` macht daraus `docs/plan/berufe-plan.md` |
| `data/karten/forever_karten.csv` | RXP-Weltkoordinaten der Kartenecken (0,0) und (1,1) pro Karte |
| `tools/` | `fetch_rxp.sh`, `build_kombi.py` (Kombi-Guide bauen), `plan_mengen.py` (Mengenmodell), `plan_berufe.py` (Berufe-Plan: Sweetspot, Stufen A–D), `rxp_schritte.py` (Schritte wie RXP sie zeigt, `--gruppe`, `--dungeons`; Stellen-Vergleich vor dem Merge), `karte_aus_testlog.py` (Kartenecken aus dem Testlog übernehmen), `ah_aus_testlog.py` (AH-Scans und Abnahme übernehmen, Bericht `docs/plan/ah-preise.md`, mit `--eintragen` in den Plan), `markt.py` (Empfehlungen: herstellen, kaufen und wieder verkaufen, Bestand verkaufen, farmen; Ausgabe nur `build/markt/` und Addon `KombiDaten`), `validate.py`, `testlog_harness.py` (streng: keine neuen globalen Variablen), `merge_poc.py` (alte Probe) |
| `docs/` | Best Practice, Entscheidungen, Vorgehen, `tests/` (Testläufe, Messplan Beta `messplan-beta.md`), `recherche/` (Quellen mit Datum), `plan/` (erzeugte Berichte) |
| `data/rechnung/` | Rechnung LW/VZ 1–300 (CSV-Werte, xlsx mit Formeln) |
| `data/preise/` | eigene AH-Scans, erzeugt von `tools/ah_aus_testlog.py`: `ah_eigen.csv` (beobachtete Gegenstände, alle Scans), `ah_alle.csv` (letzter Scan, alle Gegenstände), `ah_abnahme.csv` (Abnahme zwischen zwei Scans, Schätzung); ohne Realm- und Charakternamen |
| `testlogs/` | Testlog-Dateien aus dem Spiel (`KombiTestlog.lua`), nicht versioniert |
| `vendor/`, `build/` | RXP-Klon und erzeugte Dateien, nicht versioniert |

## Befehle

```bash
pip install -r tools/requirements.txt                     # lupa (Lua 5.1 für Python)
tools/fetch_rxp.sh v4.11.23                               # RXP in der Version des Nutzers nach vendor/ (steht im Testlog: SITZUNG … RXP v…)
python3 tools/plan_mengen.py                              # Mengenmodell -> docs/plan/mengen-leder.md (Ziele für plan.csv)
python3 tools/plan_berufe.py                              # Berufe-Plan -> docs/plan/berufe-plan.md (Sweetspot, Stufen A-D, Einkauf; Zahlen für plan.csv)
python3 tools/build_kombi.py v4.11.23 addons              # Kombi-Guide -> addons/RXPGuides_KombiGuide/ (prüft selbst, Exit 1 bei Problemen); danach committen
python3 tools/rxp_schritte.py vergleich git:HEAD:addons/RXPGuides_KombiGuide/Kombi_Guide.lua addons/RXPGuides_KombiGuide/Kombi_Guide.lua "6-12 Mulgore" --stelle 45 --gruppe "Kombiguide (H)"   # Stelle eines Testcharakters bleibt? (Exit 1 sonst)
python3 tools/rxp_schritte.py liste rxp:v4.11.23:Guides/forever/Horde-12-22_Barrens.lua "12-17 The Barrens" --klasse druid   # Route lesen wie RXP sie zeigt
python3 tools/rxp_schritte.py liste rxp:v4.11.23:Guides/Forever/dungeon/Horde-12-22_Barrens.lua "12-17 The Barrens" --dungeons RFC,WC,BFD   # RXPs Dungeon-Route mit diesen Dungeons
python3 tools/rxp_schritte.py liste addons/RXPGuides_KombiGuide/Kombi_Guide.lua "12-17 The Barrens" --gruppe "Kombiguide Dungeon (H)"   # Dungeon-Gruppe des Kombi-Guides
python3 tools/validate.py addons/RXPGuides_Kombi/WC_Vorquests.lua addons/RXPGuides_Kombi/RXPGuides_Kombi.toc
python3 tools/testlog_harness.py addons/KombiTestlog/KombiTestlog.lua
python3 tools/karte_aus_testlog.py <Testlog> v4.11.23      # KARTE-Zeilen -> data/karten/forever_karten.csv, prüft RXPs Kommentare dagegen
python3 tools/ah_aus_testlog.py <Testlog> [--eintragen]     # AH-Scans -> data/preise/, docs/plan/ah-preise.md; --eintragen: 7-Tage-Median in Preise.csv (dann plan_berufe.py)
python3 tools/markt.py <Testlog> [--marge 0.3]               # Empfehlungen -> build/markt/markt.md und build/markt/KombiDaten/ (nach Interface\AddOns\KombiDaten, nie ins Repo)
```

Vor jedem Commit an Guides oder Addons: `validate.py` (handgeschriebene Guides mit einem `RegisterGuide`), `build_kombi.py` (prüft den erzeugten Kombi-Guide selbst; `validate.py` passt dafür nicht) bzw. `testlog_harness.py` laufen lassen.

## Technische Eckpunkte (Belege im Best-Practice-Dokument)

- Forever-Client 1.60.1 (Build 70338), `## Interface: 16001`, Spieltyp `camelot`, UI-Familie Mainline. Addon-Ordner der Beta: `_classic_beta_\Interface\AddOns`.
- RXP lädt eigene Guides nur als Addon über `RXPGuides.RegisterGuide([[…]])`. Das Import-Fenster nimmt nur verschlüsselte, kontogebundene Texte.
- Guide-Kopf: `#forever`, `#name`, `#group`, `<< Horde` sind Pflicht. Eigene Gruppen `Kombiguide (H)` und `Kombiguide Dungeon (H)`, kein `#defaultfor`, kein `#beta` (`#beta` im Kopf versteckt einen Guide, solange die Beta-Features von RXP aus sind).
- Dungeons: In Forever blendet RXP die Dungeon-Auswahl aus, der Konfigurator fehlt, und beim Laden des gespeicherten Guides setzt RXP sie auf «keine» («TODO: Fix the dungeon selection for Camelot», v4.11.23 und Hauptzweig 15.10.). Schritte mit `.dungeon X` erscheinen dort also nie. `build_kombi.py` baut die Auswahl aus `data/kombi/dungeons.csv` deshalb fest in die Dungeon-Gruppe ein (Schritte weg oder `.dungeon`-Zeilen weg, wie RXPs DungeonCheck).
- In Guide-Text: `--` schneidet die Zeile ab, `[[`/`]]` beendet den Lua-String, `.subzone` braucht Text.
- Nie zwischen einen Schritt mit `#completewith next` und seinen Nachfolger einfügen.
- Während ein Testcharakter in einem Guide steht: neue Schritte nur nach seiner Stelle einfügen, sonst verschiebt sich die gespeicherte Stelle (RXP merkt sich Zeilennummer und Schrittnummer; Best Practice §6). Stand 15.10.: Tauren-Druide (Stufe 7) in «6-12 Mulgore» #45, zweiter Testcharakter (laut Schrittfolge Druide) in «12-17 The Barrens» #152 (Stufe 18, 15.10. 22:01; davor #103), beide in «Kombiguide (H)»; in «Kombiguide Dungeon (H)» steht noch niemand. Vor dem Merge mit `tools/rxp_schritte.py vergleich … --gruppe …` prüfen.
- RXP überspringt leere Argumente (`,,`): `.collect 2318,19,0,1,24` statt `.collect 2318,19,,0,8`.
- Quest- und NPC-Namen nicht übersetzen: RXP holt Quest-Namen vom Client und übersetzt `.target`/`.mob` selbst.
- Testlog liest Chat-Text nicht aus (kann im modernen Client «secret» sein), sondern zählt den Taschenbestand. Beim Ausloggen meldet `GetMoney` 0, XP und Karte sind dann ebenfalls unzuverlässig.
- Fenster (Händler, Post, Auktionshaus, Lehrer, Flugkarte) öffnet und schliesst das Forever-UI über `PLAYER_INTERACTION_MANAGER_FRAME_SHOW`/`_HIDE`. CLOSED-Ereignisse wie `MAIL_CLOSED` können fehlen (13.10.); das Testlog prüft darum zusätzlich Fenster, Interaktion und Abstand (Risiko 19).
- Koordinaten: Eigene Orte als Spielkoordinaten (Prozent, wie im Testlog) in `plan.csv`; `build_kombi.py` rechnet über `forever_karten.csv` in RXP-Weltkoordinaten um. NIE RXPs Kommentar-Koordinaten (`--c:Zone,x,y`) als Grundlage nehmen: In Mulgore passen sie nicht zur Forever-Karte (Testlauf 2), in Thunder Bluff und im Brachland genau (Messung 13.10.). Exakte Kartenecken liefert das Testlog (`KARTE`), `karte_aus_testlog.py` übernimmt sie (exakt: 1411 Durotar, 1412 Mulgore, 1413 Brachland, 1415 Östliche Königreiche, 1420 Tirisfal, 1421 Silberwald, 1454 Orgrimmar, 1456 Thunder Bluff, 1458 Undercity; weitere Karten kommen beim Spielen dazu).
- Achsen: `C_Map.GetWorldPosFromMapPos` liefert (Welt-X, Welt-Y). RXPs `.goto Karte/1,A,B` hat A = Welt-Y (zu Karten-x) und B = Welt-X (zu Karten-y). In `forever_karten.csv`: a0 = Y(0,0), b0 = X(0,0), a1 = Y(1,1), b1 = X(1,1).
- RXP-Schrittnummern zählen nur angezeigte Schritte: für Klasse und Rasse und nach den Einstellungen (ohne `#hardcore` usw.; Tauren-Druide: Kombi-Schritte #36–#38 in «1-6 Mulgore»).

## Lizenz

RXP-Inhalte stehen unter CC BY-NC-SA 4.0: nur nicht-kommerziell, Herkunft nennen, Abgeleitetes unter derselben Lizenz. Details: `LICENSE-NOTES.md`.

## Arbeitsweise

- Änderungen über Branch und Pull Request, nicht direkt auf `main`. Claude führt nach grünen Prüfungen selbst zusammen (Entscheidung des Nutzers, 13.10.).
- Ziel: möglichst wenig Arbeit für den Nutzer. Seine AddOns sind mit dem Repo verknüpft (`tools/windows/addons_verknuepfen.bat`): Nach einem Merge genügt bei ihm `aktualisieren.bat` und `/reload`. Das Testlog schickt er im Chat (`/tl zeigen` oder die Datei `WTF\Account\<KONTO>\SavedVariables\KombiTestlog.lua`); ist eine Sitzung mit seinem PC verbunden, liest Claude es selbst.
- Commit-Nachrichten auf Deutsch, kurz, Präsens, mit Bereich vorne: `testlog: zählt Kräuter mit`.
- Keine Geheimnisse (API-Keys, Tokens) und keine Testlog-Dateien committen. Ausgaben von `tools/markt.py` (Bestand, eigene Verkäufe) bleiben in `build/` und im Addon `KombiDaten` beim Nutzer.
- Neue Fakten mit Quelle ins Best-Practice-Dokument, neue Entscheidungen des Nutzers nach `docs/entscheidungen.md`.
