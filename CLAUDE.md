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
| `addons/KombiTestlog/` | Notizen- und Protokoll-Addon, `/tl hilfe` (Version 3.7.1; seit 3.6: Kartengrenzen `KARTE`, dazu Herstellen, Entzaubern, Sammeln, Beute, Händler, Geld, Lehrerlisten `LEHRER`, AH-Scan `AH-SCAN` mit Abnahme, Daten in `KombiTestlogDB.ahScans`; Rezepte `REZEPTE`, Bestand `INVENTAR`, `AH-POST`, `AH-ANGEBOT`, Daten in `chars`, `kontobank`, `ahPost`, `info`; `/tl tipp` zeigt das Addon `KombiDaten` mit dem nächsten Schritt pro Charakter; Version 3.7: Laufweg und XP pro Quelle in `chars`, Dungeon-Läufe `DUNGEON` in `dungeons`, Händlerpreis im AH-Scan, Pfand aus dem Geldabzug; Version 3.7.1: Warnung beim Händler (`KombiDaten.nichtVerkaufen`), Hinweis für Scan-Paare, zusätzlich beobachtete Gegenstände (`KombiDaten.beobachten`), Datenanfrage für fehlende Händlerpreise, Berufe und Geld in `chars`; Liste im Dateikopf) |
| `addons/RXPGuides_KombiGuide/` | der Kombi-Guide, ERZEUGT von `build_kombi.py` (nie von Hand ändern); eine Datei mit zwei Gruppen: «Kombiguide (H)» (RXP-Speedrun-Route) und «Kombiguide Dungeon (H)» (RXP-Dungeon-Route, WIP, Dungeons aus `data/kombi/dungeons.csv` fest eingebaut) |
| `tools/windows/` | `kombi_einrichten.bat` (einmal, seit 15.10.: Verknüpfungen weg, Claude installiert die Addons selbst; beim Nutzer liegt die Kopie als `_classic_beta_\KombiEinrichten.bat`, nur die läuft, weil sie `Interface\AddOns` neben sich sucht), `aktualisieren.bat` (`git pull`, nur noch zum Nachsehen), `addons_verknuepfen.bat` (alter Weg: AddOns ↔ Repo verknüpfen) |
| `data/kombi/plan.csv` | Plan-Tabelle: eine Zeile pro Berufsschritt (Anker, Aktion, ID, Menge, Ort, bis, extra, Quelle, Status), gilt für beide Gruppen; `vorquests.csv` (seit 0.6: Dungeon-Vorquests als Zusatzschritte, gleiche Spalten plus `dungeon`, Nummern V…, nur Gruppe «Kombiguide (H)»; kein Semikolon in Feldern, `build_kombi.py` bricht sonst ab); `VERSION`; `dungeons.csv` (welche Dungeons die Dungeon-Route enthält, `an` = ja/nein); `lehrer.csv` (Lehrerlisten aus dem Testlog: Lernstufe, Kosten, Ort) |
| `data/kombi/*.csv` (ausser plan.csv) | Mengenmodell Leder bis zum Wechsel in Orgrimmar: `abschnitte`, `modell_leder` (Quests mit Tieren), `kuerschnern_anteile`, `farmstellen`, `farmstopps`, `bedarf_lw_vz` (LW/VZ 1–150, Spalte `variante`), alle mit Quelle; `tools/plan_mengen.py` macht daraus `docs/plan/mengen-leder.md`. Berufe-Plan: `rezepte` (Lernstufen laut AHledger), `items` (Item-IDs), `preise_zusatz` (Händlerpreise, Fisch), `rezepte_de` (englischer und deutscher Rezeptname, Zauber-ID); `tools/plan_berufe.py` macht daraus `docs/plan/berufe-plan.md` |
| `data/karten/forever_karten.csv` | RXP-Weltkoordinaten der Kartenecken (0,0) und (1,1) pro Karte |
| `tools/` | `fetch_rxp.sh`, `build_kombi.py` (Kombi-Guide bauen), `plan_mengen.py` (Mengenmodell), `plan_berufe.py` (Berufe-Plan: Sweetspot, Stufen A–D), `rxp_schritte.py` (Schritte wie RXP sie zeigt, `--gruppe`, `--dungeons`; Stellen-Vergleich vor dem Merge; `ziele`: Ziele der Zusatzschritte mit `#completewith`), `karte_aus_testlog.py` (Kartenecken aus dem Testlog übernehmen), `lehrer_aus_testlog.py` (Lehrerlisten nach `data/kombi/lehrer.csv`), `ah_aus_testlog.py` (AH-Scans und Abnahme übernehmen, Bericht `docs/plan/ah-preise.md`, mit `--eintragen` in den Plan), `markt.py` (Empfehlungen: herstellen, für den Händler herstellen, unter Händlerpreis kaufen, kaufen und wieder verkaufen, Bestand verkaufen, farmen, nächster Schritt pro Charakter, auch für Sammler, Stufe A mit dem Material der Lager-Charaktere wie dem Bankchar; Gold für die offenen Klassenzauber aus der Lehrerliste des Charakters; Pfand 60 % des Händlerpreises mal Menge, mindestens 1s; Essenzen teilen 1 : 3; ein Angebotsbuch für alle Tipps; Listen `nichtVerkaufen` und `beobachten` für das Testlog; Ausgabe nur `build/markt/` und Addon `KombiDaten`), `spiel_aus_testlog.py` (Sitzungen, Stufen pro Stunde, Gebiete, XP pro Gegner, Laufweg, Dungeon-Läufe -> `data/spiel/`, Bericht `docs/plan/spiel.md`), `validate.py`, `testlog_harness.py` (streng: keine neuen globalen Variablen), `merge_poc.py` (alte Probe) |
| `docs/` | Best Practice, Entscheidungen, Vorgehen, `tests/` (Testläufe, Messplan Beta `messplan-beta.md`), `recherche/` (Quellen mit Datum), `plan/` (erzeugte Berichte) |
| `data/rechnung/` | Rechnung LW/VZ 1–300 (CSV-Werte, xlsx mit Formeln) |
| `data/preise/` | eigene AH-Scans, erzeugt von `tools/ah_aus_testlog.py`: `ah_eigen.csv` (beobachtete Gegenstände, alle Scans), `ah_alle.csv` (letzter Scan, alle Gegenstände, ab Testlog 3.7 mit Händlerpreis), `ah_abnahme.csv` (Abnahme zwischen zwei Scans, Schätzung; entsteht ab zwei Scans mit Testlog 3.6), `haendler_ankauf.csv` (was der Forever-Händler zahlt); ohne Realm- und Charakternamen |
| `data/spiel/` | Spieldaten aus dem Testlog, erzeugt von `tools/spiel_aus_testlog.py`: `sitzungen`, `gebiete`, ab Testlog 3.7 `xp_quellen`, `laufweg`, `dungeons`; ohne Namen und Uhrzeiten |
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
python3 tools/rxp_schritte.py ziele addons/RXPGuides_KombiGuide/Kombi_Guide.lua "12-17 The Barrens" --gruppe "Kombiguide (H)"   # Zusatzschritte: Ziel von #completewith gefunden, keine Kette (9 Klassen, 5 Rassen; Exit 1 sonst)
python3 tools/validate.py addons/RXPGuides_Kombi/WC_Vorquests.lua addons/RXPGuides_Kombi/RXPGuides_Kombi.toc
python3 tools/testlog_harness.py addons/KombiTestlog/KombiTestlog.lua
python3 tools/karte_aus_testlog.py <Testlog> v4.11.23      # KARTE-Zeilen -> data/karten/forever_karten.csv, prüft RXPs Kommentare dagegen
python3 tools/lehrer_aus_testlog.py <Testlog>              # LEHRER-Zeilen -> data/kombi/lehrer.csv (Lernstufe, Kosten, Ort; ersetzt nur die Lehrer im Testlog)
python3 tools/ah_aus_testlog.py <Testlog> [--eintragen]     # AH-Scans -> data/preise/, docs/plan/ah-preise.md; --eintragen: 7-Tage-Median in data/rechnung/Preise.csv und in die AH-Zeilen von data/kombi/preise_zusatz.csv (dann plan_berufe.py)
python3 tools/markt.py <Testlog> [--marge 0.3]               # Empfehlungen -> build/markt/markt.md und build/markt/KombiDaten/ (nach Interface\AddOns\KombiDaten, nie ins Repo)
python3 tools/spiel_aus_testlog.py <Testlog> [weitere]        # Sitzungen, Stufen pro Stunde, Laufweg, XP, Dungeons -> data/spiel/, docs/plan/spiel.md
```

Vor jedem Commit an Guides oder Addons: `validate.py` (handgeschriebene Guides mit einem `RegisterGuide`), `build_kombi.py` (prüft den erzeugten Kombi-Guide selbst; `validate.py` passt dafür nicht; bei Zusatzschritten dazu `rxp_schritte.py ziele` für jeden Guide der Gruppe «Kombiguide (H)») bzw. `testlog_harness.py` laufen lassen.

## Technische Eckpunkte (Belege im Best-Practice-Dokument)

- Forever-Client 1.60.1 (Build 70374 laut Testlog seit 14.10.; davor 70338; Build 70425 im UI-Code und im Testlog seit 16.10.; Build 70450 im UI-Code seit 16.10. 22:31 UTC, Commit 172a387, im Testlog seit 17.10.), `## Interface: 16001`, Spieltyp `camelot`, UI-Familie Mainline. Addon-Ordner der Beta: `_classic_beta_\Interface\AddOns`.
- RXP lädt eigene Guides nur als Addon über `RXPGuides.RegisterGuide([[…]])`. Das Import-Fenster nimmt nur verschlüsselte, kontogebundene Texte.
- Guide-Kopf: `#forever`, `#name`, `#group`, `<< Horde` sind Pflicht. Eigene Gruppen `Kombiguide (H)` und `Kombiguide Dungeon (H)`, kein `#defaultfor`, kein `#beta` (`#beta` im Kopf versteckt einen Guide, solange die Beta-Features von RXP aus sind). `#next` am Ende: Speedrun «RestedXP Forever Guide (H)\22-24 Hillsbrad», Dungeon-Route wie bei RXP «RestedXP Horde 22-30\22-24 Hillsbrad» (seit v0.5.2; im Spiel ungeprüft, T5).
- Dungeons: In Forever blendet RXP die Dungeon-Auswahl aus, der Konfigurator fehlt, und beim Laden des gespeicherten Guides setzt RXP sie auf «keine» («TODO: Fix the dungeon selection for Camelot», v4.11.23 und Hauptzweig 15.10.). Schritte mit `.dungeon X` erscheinen dort also nie. `build_kombi.py` baut die Auswahl aus `data/kombi/dungeons.csv` deshalb fest in die Dungeon-Gruppe ein (Schritte weg oder `.dungeon`-Zeilen weg, wie RXPs DungeonCheck).
- In Guide-Text: `--` schneidet die Zeile ab, `[[`/`]]` beendet den Lua-String, `.subzone` braucht Text.
- Nie zwischen einen Schritt mit `#completewith next` und seinen Nachfolger einfügen.
- Während ein Testcharakter in einem Guide steht: neue Schritte nur nach seiner Stelle einfügen, sonst verschiebt sich die gespeicherte Stelle (RXP merkt sich Zeilennummer und Schrittnummer; Best Practice §6). Stand 17.10. 17:08 (Testlog, Kombiguide 0.6.1): Tauren-Druide (Stufe 12, 16 %) in «6-12 Mulgore» #153 (Moonglade; davor #116, #52, #45; Schritte davor seit 0.6.3 nur mit `#maxlevel 11`, geprüft mit `--stufe 12`), zweiter Testcharakter (laut Schrittfolge Druide) in «12-17 The Barrens» #152 (Stufe 18, 15.10. 22:01; davor #103), beide in «Kombiguide (H)»; in «Kombiguide Dungeon (H)» steht noch niemand. Vor dem Merge mit `tools/rxp_schritte.py vergleich … --gruppe …` prüfen (für den Stufe-18-Charakter mit `--stufe 18`: die Zusatzschritte in «12-17» tragen `#maxlevel 17`, er sieht sie nicht; RXP findet seine Stelle dann über die Nummer, das Werkzeug prüft das seit 16.10.). Plan-Zeilen mit Status «aus …» baut `build_kombi.py` nicht ein (vorbereitet, z. B. die Annahme der Berufs-Quests für Kräuterkunde und Kürschnerei bei Kaga, offene Entscheidung 11).
- `.collect` und `.itemcount` zählen nur den eingeloggten Charakter (Taschen, mit Flag 8 bzw. drittem Wert seine Bank; `functions.lua` Z. 88/3089), nie Post, andere Charaktere oder eine Kontobank (gibt es in Forever nicht). Beim Nutzer liegen seit 17.10. auch Bagnon, BagBrother und Bagnon_* im AddOns-Ordner (CurseForge, Taschen aller Charaktere im Tooltip); Claude schreibt dort nie hinein.
- RXP überspringt leere Argumente (`,,`): `.collect 2318,19,0,1,24` statt `.collect 2318,19,,0,8`.
- `.maxskill` prüft RXP nur beim Aktivieren des Schritts (kein Ereignis); darum hängt `build_kombi.py` an jeden Gesellen-Schritt `.istrained <Zauber>` (hört auf Lehrer- und Fertigkeits-Ereignisse, ohne Lehrer-Automatik). `.train` dagegen kauft bei offenem Lehrerfenster selbst (RXP-Einstellung «Trainer automation», Standard an; Best Practice §4).
- Quest- und NPC-Namen nicht übersetzen: RXP holt Quest-Namen vom Client und übersetzt `.target`/`.mob` selbst.
- Testlog liest Chat-Text nicht aus (kann im modernen Client «secret» sein), sondern zählt den Taschenbestand. Beim Ausloggen meldet `GetMoney` 0, XP und Karte sind dann ebenfalls unzuverlässig.
- Fenster (Händler, Post, Auktionshaus, Lehrer, Flugkarte) öffnet und schliesst das Forever-UI über `PLAYER_INTERACTION_MANAGER_FRAME_SHOW`/`_HIDE`. CLOSED-Ereignisse wie `MAIL_CLOSED` können fehlen (13.10.); das Testlog prüft darum zusätzlich Fenster, Interaktion und Abstand (Risiko 19).
- Koordinaten: Eigene Orte als Spielkoordinaten (Prozent, wie im Testlog) in `plan.csv`; `build_kombi.py` rechnet über `forever_karten.csv` in RXP-Weltkoordinaten um. NIE RXPs Kommentar-Koordinaten (`--c:Zone,x,y`) als Grundlage nehmen: In Mulgore passen sie nicht zur Forever-Karte (Testlauf 2), in Thunder Bluff, Orgrimmar, Durotar und im Brachland genau (Messungen 13.–15.10.). Exakte Kartenecken liefert das Testlog (`KARTE`), `karte_aus_testlog.py` übernimmt sie (exakt: 1411 Durotar, 1412 Mulgore, 1413 Brachland, 1414 Kalimdor, 1415 Östliche Königreiche, 1420 Tirisfal, 1421 Silberwald, 1454 Orgrimmar, 1450 Moonglade, 1456 Thunder Bluff, 1458 Undercity; weitere Karten kommen beim Spielen dazu).
- Achsen: `C_Map.GetWorldPosFromMapPos` liefert (Welt-X, Welt-Y). RXPs `.goto Karte/1,A,B` hat A = Welt-Y (zu Karten-x) und B = Welt-X (zu Karten-y). In `forever_karten.csv`: a0 = Y(0,0), b0 = X(0,0), a1 = Y(1,1), b1 = X(1,1). Die Zahl nach dem Schrägstrich ist der Kontinent (0 Östliche Königreiche, 1 Kalimdor; RXP vergleicht ihn für den Pfeil); `build_kombi.py` setzt 0 für Tirisfal, Unterstadt, Silberwald und die Östlichen Königreiche (`OSTEN`).
- RXP-Schrittnummern zählen nur angezeigte Schritte: für Klasse und Rasse und nach den Einstellungen (ohne `#hardcore` usw.; Tauren-Druide: Kombi-Schritte #36–#38 in «1-6 Mulgore»).

## Lizenz

RXP-Inhalte stehen unter CC BY-NC-SA 4.0: nur nicht-kommerziell, Herkunft nennen, Abgeleitetes unter derselben Lizenz. Details: `LICENSE-NOTES.md`.

## Arbeitsweise

- Änderungen über Branch und Pull Request, nicht direkt auf `main`. Claude führt nach grünen Prüfungen selbst zusammen (Entscheidung des Nutzers, 13.10.).
- Ziel: möglichst wenig Arbeit für den Nutzer. Seit 15.10. (Entscheid, Punkt 25) installiert Claude die Addons selbst: Nach einem Merge schreibt Claude genau den Stand von `main` in `_classic_beta_\Interface\AddOns\…` (KombiTestlog, RXPGuides_KombiGuide, RXPGuides_Kombi, KombiDaten); beim Nutzer genügt `/reload`. Voraussetzung: einmal `kombi_einrichten.bat` (die alten Verknüpfungen auf den Klon müssen weg, sonst landen Claudes Dateien im Klon und `git pull` bricht ab). Solange die Verknüpfungen bestehen, nie in diese drei Ordner schreiben; bis dahin legt Claude den Stand von `main` in `_classic_beta_\_kombi_neu` ab (holt `KombiEinrichten.bat`). «git muss immer aktualisiert sein» (Nutzer, 15.10.): Was im Spiel liegt, ist vorher auf `main` zusammengeführt. Ausnahme: `KombiDaten` liegt nie auf `main` (Bestand und eigene Verkäufe), es kommt aus `build/markt/`, gerechnet mit dem Werkzeug-Stand von `main`.
- Auslieferung auf den PC (seit 17.10.): jede Datei über einen neuen Ordner unter `/mnt/user-data/outputs/` (z. B. mit Datum) an `device_commit_files` geben und danach mit `device_stage_files` zurücklesen und per SHA-256 mit der Quelle vergleichen. Am 16.10. kam über einen schon benutzten Ordner ein alter Stand von `KombiDaten` auf den PC (`docs/tests/messdaten-2026-10-17.md`).
- Das Testlog liest Claude bei verbundenem PC selbst (`WTF\Account\<KONTO>\SavedVariables\KombiTestlog.lua`), sonst schickt der Nutzer es im Chat (`/tl zeigen` oder die Datei).
- Zusammenführen: lokal mit `git merge --no-ff` als Claude und `git push`, nicht über die GitHub-API (die setzt den Profilnamen des Nutzers als Autor; Entscheid 13.10.: keine persönlichen Daten im Repo; Prüfbericht 15.10., B1).
- Commit-Nachrichten auf Deutsch, kurz, Präsens, mit Bereich vorne: `testlog: zählt Kräuter mit`.
- Keine Geheimnisse (API-Keys, Tokens) und keine Testlog-Dateien committen. Ausgaben von `tools/markt.py` (Bestand, eigene Verkäufe) bleiben in `build/` und im Addon `KombiDaten` beim Nutzer.
- Neue Fakten mit Quelle ins Best-Practice-Dokument, neue Entscheidungen des Nutzers nach `docs/entscheidungen.md`.
