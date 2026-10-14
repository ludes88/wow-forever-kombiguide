# Vorgehen: vom Plan zum Kombi-Guide

Stand 14.10.2026. Entscheidungen liegen beim Nutzer (siehe `entscheidungen.md`); hier steht, wie gearbeitet wird.

## Arbeitsweise (Entscheidung des Nutzers vom 13.10.2026)

- Claude arbeitet direkt in diesem Repo: Branch, Commit, Pull Request. Nach den automatischen Prüfungen führt Claude selbst zusammen (Merge).
- Für Recherche, Mengen-Rechnung und Bauen kann Claude parallele Agenten einsetzen.
- Die Verbindung «Link to this computer» bot die Desktop-App für die erste Sitzung nicht an (13.10.). Ersatz: Die AddOns des Nutzers sind mit dem Repo verknüpft (`tools/windows/addons_verknuepfen.bat`, einmal). Der Kombi-Guide liegt deshalb erzeugt im Repo unter `addons/RXPGuides_KombiGuide/`.
- Ist eine Sitzung mit dem PC verbunden, liest Claude die Testlog-Datei selbst; sonst schickt der Nutzer sie im Chat. Die Testlog-Datei enthält Charakternamen und kommt NIE ins Repo.
- Die Arbeit des Nutzers pro Runde: `aktualisieren.bat` doppelklicken, `/reload`, spielen, Testlog schicken.

## Datenkette statt Handarbeit

1. **Plan-Tabelle** `data/kombi/plan.csv`
   - Semikolon, UTF-8, lässt sich in Excel öffnen.
   - Eine Zeile pro Berufsschritt. Hier stehen die Entscheidungen: wo im Guide (Anker), was (Aktion), welche Item- oder Zauber-ID, wie viel, Bedingung, Ort, Quelle, Status.
   - Spalten:
     - `nr`, `guide` (Name des RXP-Guides), `anker` (z. B. `accept 1656`, `turnin 768`, `label Name`), `position` (`vor`/`nach`)
     - `aktion` (`lernen`, `kaufen`, `ziel`, `fertigkeit`, `maxfertigkeit`, `abgeben`, `annehmen`, `hingehen`, `hinweis`, `manuell`; Bedeutung im Kopf von `tools/build_kombi.py`), `id`, `menge`
     - `karte`, `x`, `y` (Spielkoordinaten in Prozent, wie im Testlog), `radius` (optional), alternativ `welt_a`/`welt_b` (RXP-Weltkoordinaten, wenn RXP den NPC schon kennt); ohne Ort kein Pfeil
     - `npc` (englischer Name, RXP übersetzt), `text` (deutscher Text, `{npc}` wird eingesetzt), `kurz` (Text am Element), `bedingung` (eine rohe RXP-Zeile, z. B. `.skill skinning,<1,1`)
     - `bis` (Label für `#completewith`, z. B. `TBHome` oder `next`: so lange bleibt der Schritt als Erinnerung sichtbar), `extra` (weitere rohe RXP-Zeilen, getrennt mit ` // `)
     - `quelle`, `status`
2. **Kartentabelle** `data/karten/forever_karten.csv`
   - Pro Karte die RXP-Weltkoordinaten der Kartenecken (0,0) und (1,1).
   - Werte aus dem Testlog-Eintrag `KARTE` sind exakt; Schätzungen sind als solche markiert.
   - `tools/karte_aus_testlog.py <Testlog> <RXP-Tag>` übernimmt die KARTE-Zeilen und prüft RXPs Kommentar-Koordinaten dagegen. Stand 13.10.: 1412 Mulgore, 1413 Brachland und 1456 Thunder Bluff exakt.
3. **Mengen-Rechnung** (`tools/plan_mengen.py`, Leder bis Stufe 20 seit 14.10.): was die Route bringt, was Lederverarbeitung 150 und Verzauberkunst 150 brauchen, und die Lücke dazwischen. Ausgabe `docs/plan/mengen-leder.md`.
   - `data/kombi/abschnitte.csv`: Abschnitte der Route mit der Stufe am Ende (aus RXPs `.xp`-Schritten).
   - `data/kombi/modell_leder.csv`: pro Quest mit Tieren die Anzahl aus den RXP-Kommentaren, Kills je Stück, Gegnerstufe, Quelle; Art «Quest», «Option: …» oder «Verbrauch» (z. B. 12 Leder für Quest 768).
   - `data/kombi/kuerschnern_anteile.csv`: Anteile Leichtes Leder, Fetzen, Light Hide, Mittleres Leder, Medium Hide nach Gegnerstufe, mit Quelle.
   - `data/kombi/farmstellen.csv` (Orte, Mitte der RXP-Schleifen) und `farmstopps.csv` (welcher Stopp in welchem Abschnitt, wie viele Minuten).
   - `data/kombi/bedarf_lw_vz.csv`: Lederverarbeitung und Verzauberkunst 1–150 nach den Forever-Routen von wow-professions und kami-labs; Entzaubern und Preise aus `data/rechnung/`.
   - Die Ziele trägt Claude in `plan.csv` ein (Aktion `ziel`, Tabelle «Ziele im Kombi-Guide» im Bericht); das Testlog misst, wie weit sie stimmen.
   - `tools/rxp_schritte.py liste` zeigt die Route so, wie RXP sie einem Charakter zeigt (Klasse, Rasse, Forever-Standard-Einstellungen); daraus stammen die Schrittnummern.
   - Kürschnerbare Gegner pro Gebiet aus den RXP-Schritten.
   - Ausbeute nach Gegnerstufe aus MetaForge und AHledger, dann aus dem Testlog 3 (SAMMELN und BEUTE mit Kreatur-ID, Ort und Zeit).
   - Kosten und Einnahmen aus dem Testlog 3 (HÄNDLER, POST, AUKTIONSHAUS, GELD, GELERNT), Punkte pro Rezept aus HERSTELLEN, Ausbeute pro Teil aus ENTZAUBERN.
   - Wo die Route nicht reicht: Farm-Stopp vorschlagen oder Lücke offen zeigen.
   - Berufe-Plan (`tools/plan_berufe.py`, seit 14.10.): nimmt den Bestand beim Wechsel in Orgrimmar aus dem Mengenmodell und rechnet den Sweetspot für eigenes Leder sowie die Stufen A–D (Herstellen, Entzaubern, Verzaubern, Einkauf im AH und beim Händler, Verkauf) mit Stückzahlen und Kosten. Eingaben: `bedarf_lw_vz.csv` (Spalte `variante` für die zwei Tabs ab LW 130, Route «wow-professions Alternative» für Soul Dust), `rezepte.csv` (Lernstufen laut AHledger, für die Widerspruchsprüfung), `items.csv` (Item-IDs, deutsche Namen nur aus dem Testlog), `preise_zusatz.csv` (Händlerpreise und Fisch), dazu `data/rechnung/Preise.csv` und `Kreislauf.csv`. Bericht `docs/plan/berufe-plan.md`; die Zahlen trägt Claude in `plan.csv` ein.
   - Wert (Entscheide vom 13.10.): beim Kräuterfarmen das gewinnbringendste Kraut, gerechnet pro Knoten mit Zusatzbeute; beim Fischen der Fisch mit dem höchsten AH-Wert, roh oder gekocht. Preise in der Beta von AHledger, zum Start aus dem Startdokument des Nutzers (EU). Grundlagen: `docs/recherche/2026-10-13_kraeuter-fische-kochen.md`.
   - Goldbilanz entlang der Route: Kosten (Lehrer für Zauber und Berufe, Rezepte, Händlermaterial, Flüge) gegen Einnahmen; Kostenquellen in `docs/recherche/2026-10-13_kosten.md`, gemessene Werte aus Testlog 3.
4. **Generator** `tools/build_kombi.py`: liest Plan- und Kartentabelle, baut die RXP-Gratis-Route in genau der RXP-Version des Nutzers neu und fügt die Schritte ein.
5. **Prüfung** (automatisch im Generator):
   - Lua-Syntax, Kopf, bekannte Befehle
   - jeder Anker genau einmal, jede Plan-Zeile eingefügt
   - kein `--` und kein `[[`/`]]` in eigenen Texten, Koordinaten 0–100
   - dazu von Hand vor dem Merge: `tools/rxp_schritte.py vergleich` für jede gespeicherte Stelle eines Testcharakters (Best Practice §6)
6. **Spieltest** mit KombiTestlog, dann Auswertung durch Claude, dann Plan anpassen, neue Version bauen und austauschen. Der Fortschritt bleibt, solange Gruppe und Guide-Namen gleich bleiben (T6).
   - Messplan für die Beta (14.–22.10.): `docs/tests/messplan-beta.md`. Jede Messung (M1–M10) nennt, welche Zahl in welcher Tabelle sie ersetzt. Testlog 3.4 schreibt dafür auch die Lehrerlisten (LEHRER).

## Versionen

| Version | Inhalt | Stand |
|---|---|---|
| 0.1 | Kürschnermesser, Kürschnerei und Kräuterkunde in Camp Narache | im Spiel getestet (Testlauf 2) |
| 0.1.1 | Koordinaten über Kartentabelle; Testlog 2 (Fehler A–C behoben, Kartengrenzen, Sitzung meldet Kombiguide) | im Spiel geladen (13.10., aus dem Repo); Pfeil zu Nawka im Spiel offen |
| 0.1.2 | exakte Kartenecken für Mulgore aus dem Testlog | gebaut und geprüft (13.10.); Pfeil zu Nawka rechnerisch auf der gemessenen Stelle; im Spiel geladen (13.10. 22:08). Seit 13.10. abends auf Basis RXP v4.11.23 (gleiche Berufsschritte) |
| 0.2 | Mulgore 6–12 und Thunder Bluff: Leder- und Kräuterziele aus dem Mengenmodell, Abgabe der Berufs-Quests 97936 und 97933, Geselle in Kürschnerei, Kräuterkunde und Angeln, Auktionshaus, Hinweis zu «Gathering Leather», Angeln im Teich (optional) | gebaut und geprüft (13.10. abends); alle Schritte nach «Well» (#30), damit die Stelle des Testcharakters bleibt; im Spiel offen |
| 0.2.x | Annehmen der Berufs-Quests bei Kaga, Kochen mit Lagerfeuer, Beginn von 6-12 Mulgore | geplant; liegt vor der Stelle des Testcharakters und braucht eine Lösung, die seine gespeicherte Stelle nicht verschiebt (Best Practice §6) |
| 0.3 | Brachland und Südbrachland bis Stufe 20: Leder-Zähler pro Abschnitt (ab Stufe 16 auch Mittleres Leder), drei optionale Farm-Stopps S1–S3 (Nordbrachland beim RXP-Grinden auf 16, Südbrachland bei den Scytheclaws, Camp Taurajo; bei der Ankunft in den Crossroads keiner, weil die Route dort dieselben Tiere für Quests tötet), Ziele aus dem Mengenmodell bis Stufe 20; Leder-Ziel in Mulgore vor und nach «Gathering Leather» getrennt | gebaut und geprüft (14.10.); Stellen geprüft: «6-12 Mulgore» #30 und «12-17 The Barrens» #77 bleiben; im Spiel offen |
| 0.3.x | Zähler in «12-17» vor #77 (Crossroads bis Nordbrachland) | wartet auf offenen Punkt 11 in `entscheidungen.md` |
| 0.4 | Berufswechsel in Orgrimmar (Entscheid 14.10.): Sweetspot-Zähler bei S1 (62 Leichtes Leder), in Orgrimmar nach RXP #108 Verlernen, LW 1–80, VZ 1–50, beide Gesellen, Stufe B optional; in Thunder Bluff (Stufe 20, «17-22» nach #92) Stufen B–D und Verkauf; Leder-Zähler und Farm-Stopps nach Orgrimmar entfallen; neue Aktion `manuell` | gebaut und geprüft (14.10.); Stellen «6-12 Mulgore» #30 und «12-17 The Barrens» #77 bleiben; im Spiel offen (T11, T12). 14.10. abends: Plan-Zeile 5 hängt an `label Vision` statt an `turnin 96661` (RXP-Hauptzweig gibt die Kochquest zweimal ab); Bau auf v4.11.23 bytegleich, darum keine neue Versionsnummer |
| 0.5 | Angeln als Goldquelle (Stellen und Zeit nach Entscheid des Nutzers, Zahlen aus Messung M3), Lager-Gegenstände, Merchant's Favor, Schlafsack-Strang (79007 ist in RXP); je nach Entscheid: Variante «Kräuterkunde bis Thunder Bluff» (offener Punkt 12, Messung M4), «verkaufen statt entzaubern» (Punkt 15), Lage der Berufssitzung zur neuen Katzen-Questreihe (Punkt 13) | geplant |

Die Beta läuft bis 22.10.2026 (Stufen-Grenze 30), der Start ist am 04.11.2026 (https://www.warcrafttavern.com/forever/guides/beta/, geprüft am 13.10.). Bis 22.10. lassen sich Messdaten sammeln.
