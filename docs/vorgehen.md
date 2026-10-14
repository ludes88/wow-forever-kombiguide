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
     - `aktion` (`lernen`, `kaufen`, `ziel`, `fertigkeit`, `maxfertigkeit`, `abgeben`, `annehmen`, `hingehen`, `hinweis`; Bedeutung im Kopf von `tools/build_kombi.py`), `id`, `menge`
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
   - Wert (Entscheide vom 13.10.): beim Kräuterfarmen das gewinnbringendste Kraut, gerechnet pro Knoten mit Zusatzbeute; beim Fischen der Fisch mit dem höchsten AH-Wert, roh oder gekocht. Preise in der Beta von AHledger, zum Start aus dem Startdokument des Nutzers (EU). Grundlagen: `docs/recherche/2026-10-13_kraeuter-fische-kochen.md`.
   - Goldbilanz entlang der Route: Kosten (Lehrer für Zauber und Berufe, Rezepte, Händlermaterial, Flüge) gegen Einnahmen; Kostenquellen in `docs/recherche/2026-10-13_kosten.md`, gemessene Werte aus Testlog 3.
4. **Generator** `tools/build_kombi.py`: liest Plan- und Kartentabelle, baut die RXP-Gratis-Route in genau der RXP-Version des Nutzers neu und fügt die Schritte ein.
5. **Prüfung** (automatisch im Generator):
   - Lua-Syntax, Kopf, bekannte Befehle
   - jeder Anker genau einmal, jede Plan-Zeile eingefügt
   - kein `--` und kein `[[`/`]]` in eigenen Texten, Koordinaten 0–100
   - dazu von Hand vor dem Merge: `tools/rxp_schritte.py vergleich` für jede gespeicherte Stelle eines Testcharakters (Best Practice §6)
6. **Spieltest** mit KombiTestlog, dann Auswertung durch Claude, dann Plan anpassen, neue Version bauen und austauschen. Der Fortschritt bleibt, solange Gruppe und Guide-Namen gleich bleiben (T6).

## Versionen

| Version | Inhalt | Stand |
|---|---|---|
| 0.1 | Kürschnermesser, Kürschnerei und Kräuterkunde in Camp Narache | im Spiel getestet (Testlauf 2) |
| 0.1.1 | Koordinaten über Kartentabelle; Testlog 2 (Fehler A–C behoben, Kartengrenzen, Sitzung meldet Kombiguide) | im Spiel geladen (13.10., aus dem Repo); Pfeil zu Nawka im Spiel offen |
| 0.1.2 | exakte Kartenecken für Mulgore aus dem Testlog | gebaut und geprüft (13.10.); Pfeil zu Nawka rechnerisch auf der gemessenen Stelle; im Spiel geladen (13.10. 22:08). Seit 13.10. abends auf Basis RXP v4.11.23 (gleiche Berufsschritte) |
| 0.2 | Mulgore 6–12 und Thunder Bluff: Leder- und Kräuterziele aus dem Mengenmodell, Abgabe der Berufs-Quests 97936 und 97933, Geselle in Kürschnerei, Kräuterkunde und Angeln, Auktionshaus, Hinweis zu «Gathering Leather», Angeln im Teich (optional) | gebaut und geprüft (13.10. abends); alle Schritte nach «Well» (#30), damit die Stelle des Testcharakters bleibt; im Spiel offen |
| 0.2.x | Annehmen der Berufs-Quests bei Kaga, Kochen mit Lagerfeuer, Beginn von 6-12 Mulgore | geplant; liegt vor der Stelle des Testcharakters und braucht eine Lösung, die seine gespeicherte Stelle nicht verschiebt (Best Practice §6) |
| 0.3 | Brachland und Südbrachland bis Stufe 20: Leder-Zähler pro Abschnitt (ab Stufe 16 auch Mittleres Leder), drei optionale Farm-Stopps S1–S3 (Nordbrachland beim RXP-Grinden auf 16, Südbrachland bei den Scytheclaws, Camp Taurajo; bei der Ankunft in den Crossroads keiner, weil die Route dort dieselben Tiere für Quests tötet), Ziele aus dem Mengenmodell bis Stufe 20; Leder-Ziel in Mulgore vor und nach «Gathering Leather» getrennt | gebaut und geprüft (14.10.); Stellen geprüft: «6-12 Mulgore» #30 und «12-17 The Barrens» #77 bleiben; im Spiel offen |
| 0.3.x | Zähler in «12-17» vor #77 (Crossroads bis Nordbrachland), Wechsel-Schritte zu Lederverarbeitung und Verzauberkunst | wartet auf Entscheide 7 und 10 in `entscheidungen.md` |
| 0.4 | 17–22, Lager-Gegenstände, Merchant's Favor, Schlafsack-Strang (79007 ist in RXP) | geplant |

Die Beta läuft bis 22.10.2026 (Stufen-Grenze 30), der Start ist am 04.11.2026 (https://www.warcrafttavern.com/forever/guides/beta/, geprüft am 13.10.). Bis 22.10. lassen sich Messdaten sammeln.
