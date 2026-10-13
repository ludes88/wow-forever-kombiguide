# WoW Forever: Kombi-Guide und Berufe

Ein RestedXP-Guide für Stufe 1–22 (Horde, Tauren-Druide, Start Mulgore): RXPs Gratis-Route mit eigenen Berufsschritten an den passenden Stellen («Weg A»). Dazu das Test-Addon KombiTestlog.
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
| `addons/KombiTestlog/` | Notizen- und Protokoll-Addon, `/tl hilfe` (Version 2: schreibt auch Kartengrenzen `KARTE`) |
| `addons/RXPGuides_KombiGuide/` | der Kombi-Guide, ERZEUGT von `build_kombi.py` (nie von Hand ändern) |
| `tools/windows/` | `addons_verknuepfen.bat` (einmal: AddOns ↔ Repo verknüpfen), `aktualisieren.bat` (`git pull`) für den Nutzer |
| `data/kombi/plan.csv` | Plan-Tabelle: eine Zeile pro Berufsschritt (Anker, Aktion, ID, Menge, Ort, Quelle, Status); `VERSION` |
| `data/karten/forever_karten.csv` | RXP-Weltkoordinaten der Kartenecken (0,0) und (1,1) pro Karte |
| `tools/` | `fetch_rxp.sh`, `build_kombi.py` (Kombi-Guide bauen), `validate.py`, `testlog_harness.py`, `merge_poc.py` (alte Probe) |
| `docs/` | Best Practice, Entscheidungen, Vorgehen, `tests/` (Testläufe) |
| `data/rechnung/` | Rechnung LW/VZ 1–300 (CSV-Werte, xlsx mit Formeln) |
| `testlogs/` | Testlog-Dateien aus dem Spiel (`KombiTestlog.lua`), nicht versioniert |
| `vendor/`, `build/` | RXP-Klon und erzeugte Dateien, nicht versioniert |

## Befehle

```bash
pip install -r tools/requirements.txt                     # lupa (Lua 5.1 für Python)
tools/fetch_rxp.sh v4.11.13                               # RXP in der Version des Nutzers nach vendor/ (steht im Testlog: SITZUNG … RXP v…)
python3 tools/build_kombi.py v4.11.13 addons              # Kombi-Guide -> addons/RXPGuides_KombiGuide/ (prüft selbst, Exit 1 bei Problemen); danach committen
python3 tools/validate.py addons/RXPGuides_Kombi/WC_Vorquests.lua addons/RXPGuides_Kombi/RXPGuides_Kombi.toc
python3 tools/testlog_harness.py addons/KombiTestlog/KombiTestlog.lua
```

Vor jedem Commit an Guides oder Addons: `validate.py` bzw. `testlog_harness.py` laufen lassen.

## Technische Eckpunkte (Belege im Best-Practice-Dokument)

- Forever-Client 1.60.1 (Build 70338), `## Interface: 16001`, Spieltyp `camelot`, UI-Familie Mainline. Addon-Ordner der Beta: `_classic_beta_\Interface\AddOns`.
- RXP lädt eigene Guides nur als Addon über `RXPGuides.RegisterGuide([[…]])`. Das Import-Fenster nimmt nur verschlüsselte, kontogebundene Texte.
- Guide-Kopf: `#forever`, `#name`, `#group`, `<< Horde` sind Pflicht. Eigene Gruppe `Kombiguide (H)`, kein `#defaultfor`.
- In Guide-Text: `--` schneidet die Zeile ab, `[[`/`]]` beendet den Lua-String, `.subzone` braucht Text.
- Nie zwischen einen Schritt mit `#completewith next` und seinen Nachfolger einfügen.
- Quest- und NPC-Namen nicht übersetzen: RXP holt Quest-Namen vom Client und übersetzt `.target`/`.mob` selbst.
- Testlog liest Chat-Text nicht aus (kann im modernen Client «secret» sein), sondern zählt den Taschenbestand.
- Koordinaten: Eigene Orte als Spielkoordinaten (Prozent, wie im Testlog) in `plan.csv`; `build_kombi.py` rechnet über `forever_karten.csv` in RXP-Weltkoordinaten um. NIE RXPs Kommentar-Koordinaten (`--c:Zone,x,y`) als Grundlage nehmen, sie passen nicht zur Forever-Karte (Testlauf 2). Exakte Kartenecken liefert das Testlog (`KARTE`).
- RXP-Schrittnummern zählen nur Schritte, die für Klasse und Rasse gelten (Tauren-Druide: Kombi-Schritte #36–#38 in «1-6 Mulgore», v0.1/v0.1.1).

## Lizenz

RXP-Inhalte stehen unter CC BY-NC-SA 4.0: nur nicht-kommerziell, Herkunft nennen, Abgeleitetes unter derselben Lizenz. Details: `LICENSE-NOTES.md`.

## Arbeitsweise

- Änderungen über Branch und Pull Request, nicht direkt auf `main`. Claude führt nach grünen Prüfungen selbst zusammen (Entscheidung des Nutzers, 13.10.).
- Ziel: möglichst wenig Arbeit für den Nutzer. Seine AddOns sind mit dem Repo verknüpft (`tools/windows/addons_verknuepfen.bat`): Nach einem Merge genügt bei ihm `aktualisieren.bat` und `/reload`. Das Testlog schickt er im Chat (`/tl zeigen` oder die Datei `WTF\Account\<KONTO>\SavedVariables\KombiTestlog.lua`); ist eine Sitzung mit seinem PC verbunden, liest Claude es selbst.
- Commit-Nachrichten auf Deutsch, kurz, Präsens, mit Bereich vorne: `testlog: zählt Kräuter mit`.
- Keine Geheimnisse (API-Keys, Tokens) und keine Testlog-Dateien committen.
- Neue Fakten mit Quelle ins Best-Practice-Dokument, neue Entscheidungen des Nutzers nach `docs/entscheidungen.md`.
