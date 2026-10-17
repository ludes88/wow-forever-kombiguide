# Weg A: Kombi-Guide aus RXP-Route und Berufen – Best Practice

Stand 17.10.2026. Gilt für die Forever-Beta: Client 1.60.1 (Build 70374 laut Testlog seit 14.10., davor 70338; Build 70425 im Blizzard-UI-Code seit 16.10. 00:52 UTC (Commit b401e03), im Testlog seit 16.10. 17:40; Build 70450 im UI-Code seit 16.10. 22:31 UTC (Commit 172a387 in https://github.com/Gethe/wow-ui-source/tree/forever), im Testlog seit 17.10. 12:54; bis 17.10. stand hier für 70450 der Commit b401e03; die Spieldateien im Beta-Ordner tragen das Datum 16.10. 02:55; in der API-Doku nur Ergänzungen, nichts, was die Addons nutzen, fiel weg), RestedXP-Release v4.11.23 (10.10.), RXP-Hauptzweig 998caf30 (14.10.; die Dungeon-Teile geprüft auf dec489a2, 15.10.).
Zweck: Nachschlagewerk für Claude und den Nutzer. Was steht, ist belegt (Link oder Code-Stelle) oder als **ungeprüft** markiert.

---

## 0. Schnellzugriff

- **Was Weg A ist:** RXPs Gratis-Route für Stufe 1–22 (Mulgore, Brachland) als Kopie, darin unsere Berufsschritte an Ankerstellen. Ein Guide, ein Fenster. Ab 22 wechselt der Nutzer zu seinem gekauften Guide. Seit v0.5 zwei Gruppen in derselben Datei: «Kombiguide (H)» (RXPs Speedrun-Route) und «Kombiguide Dungeon (H)» (RXPs Dungeon-Route mit fest eingebauten Dungeons, §5). Seit v0.6 hat «Kombiguide (H)» die Dungeon-Vorquests als Zusatzschritte dort, wo die Route an den Quest-Gebern vorbeikommt, dazu den Abstecher zu den Ruinen von Lordaeron nach Orgrimmar (`data/kombi/vorquests.csv`, §5). Seit v0.6.3 dazu «Grundlagen des Zeltens: Angeln» bei Kaga Wildhoof (Wunsch des Nutzers, §5).
- **Wie er geladen wird:** als eigenes kleines Addon (`RXPGuides_KombiGuide`, gebaut von `tools/build_kombi.py`), das `RXPGuides.RegisterGuide([[ … ]])` aufruft. Das Import-Fenster von RXP nimmt nur verschlüsselte, kontogebundene Texte. Im Spiel bestätigt am 13.10. (Testlauf 1 und 2, `docs/tests/`).
- **Pflicht im Kopf jedes Guides:** `#forever`, `#name`, `#group`, `<< Horde`. Ohne `#forever` lädt RXP den Guide in Forever nicht.
- **Eigene Gruppen:** `#group Kombiguide (H)` und `#group Kombiguide Dungeon (H)`. Keine Gruppe/Name-Kombination doppelt mit RXP.
- **Dungeons:** In Forever lässt RXP keine Dungeons zu (Auswahl ausgeblendet, beim Laden auf «keine» gesetzt; §4). Die Dungeon-Gruppe enthält die Dungeons aus `data/kombi/dungeons.csv` deshalb fest (§5).
- **Update-Ablauf:** RXP-Version aus dem Testlog lesen → genau diesen Tag holen → Skript mischt neu → statische Prüfung → Pull Request und Merge → Claude schreibt den Stand von `main` in den AddOns-Ordner (Entscheid vom 15.10., Punkt 25; einmal vorher beim Nutzer `_classic_beta_\KombiEinrichten.bat`, die Kopie von `tools/windows/kombi_einrichten.bat`, die die Ordner aus `_classic_beta_\_kombi_neu` holt; bis dahin legt Claude den Stand dort ab, `docs/vorgehen.md`) → beim Nutzer `/reload` → der Nutzer testet.
- **Testlog:** `/tl <Text>`, `/tl bug <Text>`, `/tl zeigen`. Datei: `WTF\Account\<KONTO>\SavedVariables\KombiTestlog.lua`. Version 3 schreibt zusätzlich von selbst: HERSTELLEN, ENTZAUBERN, SAMMELN, ANGELN, BEUTE, HÄNDLER, POST, AUKTIONSHAUS, GELD, GELERNT, REZEPT (Liste im Kopf von `KombiTestlog.lua`). Version 3.2 beendet Fenster-Sitzungen auch ohne CLOSED-Ereignis (Risiko 19) und zählt beim Angeln die Würfe pro Fang; 3.3 nimmt beim Ausloggen den letzten bekannten Geldstand; 3.4 schreibt beim Öffnen eines Lehrerfensters die ganze Liste (LEHRER: Status, Lernstufe, Kosten; T13); 3.5 liest beim Öffnen des Auktionshauses alle Angebote (AH-SCAN, höchstens alle 15 Minuten, von Hand `/tl ah`; T15); 3.6 schreibt die gelernten Rezepte mit Reagenzien und Farbe (REZEPTE), den Bestand in Taschen, Bank und Kontobank (INVENTAR), die Briefe des Auktionshauses (AH-POST), eigene Angebote (AH-ANGEBOT) und die Abnahme zwischen zwei AH-Scans; `/tl tipp` zeigt die Empfehlungen aus dem Addon `KombiDaten` (T16–T21); 3.7 schreibt den Laufweg (alle 10 s, bei Stillstand alle 60 s), XP pro Quelle (Gegner mit Kreatur-ID und Stufe, Quest, sonst; erholt getrennt), Dungeon-Läufe (DUNGEON), beim AH-Scan den Händlerpreis und was darunter angeboten wird, und den Pfand aus dem Geldabzug; `/tl tipp` zeigt dazu den nächsten Schritt für den Charakter (T23–T28); 3.7.1 warnt beim Händler vor dem Verkauf von Plan-Leder und Beute mit hohem AH-Wert (Liste `KombiDaten.nichtVerkaufen`, verkauft wird nichts automatisch), erinnert 20 Minuten nach einem Scan an das Scan-Paar für die Abnahme (nur in Orgrimmar, Thunder Bluff und Undercity), beobachtet zusätzlich die Gegenstände aus `KombiDaten.beobachten`, fragt beim Scan die Daten von bis zu 200 Gegenständen ohne Händlerpreis an (jeden höchstens einmal pro Sitzung; der nächste Scan kennt ihren Preis) und merkt sich Berufe und Geld pro Charakter, auch beim Einloggen (T29–T33).
- **Messplan Beta:** `docs/tests/messplan-beta.md` (M1–M12, was jede Messung im Plan ersetzt; Kurzliste bis 22.10. vom 15.10.; Checkliste für den Stufe-8-Druiden vom 16.10.). Goldquellen mit Zahlen: `docs/recherche/2026-10-14_goldquellen.md`.
- **Eigene AH-Preise:** `tools/ah_aus_testlog.py <Testlog> [--eintragen]` übernimmt die AH-Scans ohne Realm- und Charakternamen: `data/preise/ah_eigen.csv` (alle Scans, Plan-Gegenstände, daraus die Wochenpreise), `data/preise/ah_alle.csv` (letzter Scan, alle Gegenstände), Bericht `docs/plan/ah-preise.md`. Mit `--eintragen` wird der 7-Tage-Median zum Preis «jetzt» in `data/rechnung/Preise.csv` und in den AH-Zeilen von `data/kombi/preise_zusatz.csv` (danach `tools/plan_berufe.py`), nur aus vollständigen Scans und nur bei mindestens 50 Stück im Angebot; die 30-Tage-Werte und die xlsx bleiben AHledger (offene Entscheidung 17). Markt = Region, Fraktion, Kurzzeichen des Realms, Beta oder Live. Seit Testlog 3.6 dazu `data/preise/ah_abnahme.csv`: pro Scan und beobachtetem Gegenstand, was seit dem Scan davor von den billigsten Angeboten fehlt (eine Schätzung der Käufe, Risiko 24). Beobachtet sind der Plan, `/tl item` und alle Reagenzien und Ergebnisse der gelernten Rezepte.
- **Markt-Empfehlungen:** `tools/markt.py <Testlog>` rechnet aus Rezepten, Bestand, AH-Post, Scans und dem Verlauf in `data/preise/`: herstellen (Marge nach 5 % Gebühr), kaufen und wieder verkaufen (Angebote unter dem 7-Tage-Tiefstpreis mit Mindestmarge, nur mit Abnahme-Beleg und höchstens so viel, wie geschätzt abging; nie hochgerechnet), aus dem Bestand verkaufen, farmen pro Stunde (Tipp erst ab 15 Minuten und mit einem Preis für jede Beute); seit 15.10. auch für den Händler herstellen (Rezepte, deren Ergebnis der Forever-Händler höher bezahlt, als das Material im letzten Scan kostet, mit Grenzpreis), Angebote unter dem Händlerpreis und den nächsten Schritt pro Charakter (Abschnitt des Berufe-Plans, Material, Lehrer, Zwischenprodukte selbst herstellen, Überschuss). Seit 16.10.: Geringe Essenzen zum kleineren Preis aus direkt gekauften oder geteilten Grossen (1 → 3, für die Magieessenz gemessen); alle Händler-Tipps teilen ein Angebotsbuch (was ein Tipp kauft, fehlt dem nächsten; eine Herstellung zählt ab 5c Gewinn); ein nächster Schritt auch für Sammler (Leder für Stufe A behalten, Gold für Orgrimmar, Beute mit hohem AH-Wert); dazu die Listen für das Testlog 3.7.1. Seit 17.10.: Für Stufe A zählt Material bei Lager-Charakteren des Kontos mit (ohne Kürschnerei, Kräuterkunde, Lederverarbeitung und Verzauberkunst, z. B. der Bankchar; Stand ihres letzten Ausloggens, Post im Briefkasten nicht); «AH statt Händler» nennt die gemessene Abnahme und den Pfand (§9). Seit 17.10. abends zählen beim Gold für Orgrimmar die noch offenen Klassenzauber bis Stufe 16 mit (aus der letzten Lehrerliste vom Typ «Klasse», die der Charakter geöffnet hat; Waffenmeister nicht), für andere Charaktere bis zur nächsten Zielstufe 20 bzw. 22 (Notiz des Nutzers 17.10., §9 Klassenzauber). Daneben die 30 Tage als Langzeit-Vergleich: Tiefstpreis und Abnahme im Beleg, Warnung, wenn der 7-Tage-Wert 20 % oder mehr darüber liegt; Preis, Beleg und Menge bleiben bei 7 Tagen (Schwellen: Wahl von Claude, offener Punkt 20). Ausgabe nur nach `build/markt/` (Bericht `markt.md`, Addon `KombiDaten` für `/tl tipp`); Bestand und eigene Verkäufe kommen nie ins Repo. Das Addon `KombiDaten` gehört nach `Interface\AddOns\KombiDaten`, nie in einen mit dem Repo verknüpften Ordner; ein neuer Addon-Ordner lädt erst nach einem Neustart des Spiels.
- **Werkzeuge im Repo:** `tools/build_kombi.py` (Kombi-Guide aus `data/kombi/plan.csv` bauen und prüfen), `tools/validate.py` (Guide prüfen), `tools/testlog_harness.py` (Testlog-Probe, dazu die Kopplung mit `ah_aus_testlog.py` und `markt.py`), `tools/karte_aus_testlog.py` (Kartenecken aus dem Testlog übernehmen und RXP dagegen prüfen), `tools/ah_aus_testlog.py` (AH-Scans und Händlerpreise übernehmen), `tools/lehrer_aus_testlog.py` (Lehrerlisten), `tools/markt.py` (Empfehlungen), `tools/spiel_aus_testlog.py` (Sitzungen, Stufen pro Stunde, Gebiete, ab Testlog 3.7 XP pro Gegner, Laufweg und Dungeon-Läufe; `data/spiel/`, Bericht `docs/plan/spiel.md`), `tools/fetch_rxp.sh` (RXP in einer Version holen).
- **Koordinaten:** eigene Orte in Spielkoordinaten; umgerechnet über `data/karten/forever_karten.csv`. RXPs Kommentar-Koordinaten (`--c:`) passen in Mulgore nicht zur Forever-Karte, in Thunder Bluff, Orgrimmar, Durotar und im Brachland genau (Abschnitt 7, Risiko 17). Exakt gemessen: Mulgore, Brachland, Thunder Bluff, Orgrimmar, seit 15.10. auch Durotar, Tirisfal, Undercity, Silberwald und die Kontinente Kalimdor und Östliche Königreiche, seit 17.10. Moonglade.
- **Mengen:** `tools/plan_mengen.py` rechnet aus `data/kombi/*.csv`, wie viel Leder die RXP-Route bis Stufe 20 bringt (mit und ohne Farm-Stopps), was Lederverarbeitung 150 und Verzauberkunst 150 brauchen und wie gross die Lücke ist (Bericht `docs/plan/mengen-leder.md`). Die Ziele im Kombi-Guide kommen daher.
- **Berufe-Plan:** `tools/plan_berufe.py` rechnet aus dem Mengenmodell, der LW- und VZ-Route von wow-professions und den Preisen den Sweetspot für eigenes Leder und die Stufen A–D mit Stückzahlen, Einkauf, Entzaubern und Verkauf (Bericht `docs/plan/berufe-plan.md`). Kombi-Guide v0.4 setzt das um: Wechsel in Orgrimmar (Stufe A, dazu B, wenn das Gold reicht), Rest in Thunder Bluff (Stufe 20). Seit 15.10. rechnet der Plan die gemessenen Lernkosten (`data/kombi/lehrer.csv`) und die Händlerpreise aus dem Forever-Client (`data/preise/haendler_ankauf.csv`) ein: Leichte Lederhosen und Dunkle Ledergürtel gehen an den Händler statt ins Entzaubern (Preisregel, berufe-plan §6; Kombi-Guide v0.5.2); als Vorschlag daneben die Variante Zauberstäbe (berufe-plan §9).
- **Schritte lesen und Stellen prüfen:** `tools/rxp_schritte.py liste …` zeigt die Schritte so, wie RXP sie einem Charakter zeigt (`--gruppe` wählt die Gruppe, `--dungeons RFC,WC` schaltet Dungeons ein); `… vergleich …` prüft vor dem Merge, dass ein Neubau die gespeicherte Stelle eines Testcharakters nicht verschiebt (§6); `… ziele …` prüft, dass jeder Zusatzschritt mit `#completewith` sein Ziel findet und keine Kette bildet (9 Klassen, 5 Rassen; §4).

---

## 1. Ziel und Rahmen

- Der Nutzer startet neu als Tauren-Druide in Mulgore und levelt mit RestedXP (RXP).
- Berufsplan (Entscheidung des Nutzers, siehe `docs/entscheidungen.md`): Kräuterkunde und Kürschnerei bis etwa Stufe 15, dann Wechsel auf Lederverarbeitung (LW) und Verzauberkunst (VZ), Ziel je 150. Fischen und Kochen laufen nebenher.
- Mengen aus der Rechnung vom 13.10. (Chat, Teil 2):
  - 416 Leichtes Leder für LW 125 und VZ im Mittel 125
  - 488 für VZ 130 mit 90 % Sicherheit
  - 644 für VZ 150 mit 90 % Sicherheit
  - dazu 100 Ruined Leather Scraps, 27 Light Hide, 10 Medium Hide
  - Die Herleitung dieser Zahlen ist im Repo nicht mehr auffindbar. Neu gerechnet am 14.10. mit den Forever-Routen (`docs/plan/mengen-leder.md`): Lederverarbeitung 150 braucht netto 240 (kami-labs) bis 416 (wow-professions) Leichtes Leder; mit Verzauberkunst 150 aus eigenem Entzaubern 567 bis 614. Die 416 stimmen zahlenmässig mit dem Netto-Bedarf der wow-professions-Route überein; ob die alte Zahl so entstand, ist offen.
- Vorgabe des Nutzers vom 14.10.: Das Material muss nicht mit Stufe 15 fertig sein; es soll um Stufe 20 für Lederverarbeitung 150 und Verzauberkunst 150 reichen (Lesart von Claude, Rückfrage offen, `docs/entscheidungen.md`).
- Leitsatz des Nutzers: nicht «farme 650 Leder» als Block, sondern pro Gebiet so viel, wie dort effizient geht, dann weiter im Takt der Route.
- Entscheide vom 14.10. (`docs/entscheidungen.md`): Berufswechsel in Orgrimmar (Stufe 16); eigenes Leder nur bis zum «Sweetspot», danach kaufen («Wenn es sich nicht lohnt mit leichtem Leder auf 150 zu kommen, dann tun wir das auch nicht»); Fischen und verkaufte Erzeugnisse finanzieren den Einkauf; der Guide zeigt Stückzahlen für Herstellen, Entzaubern, Verzaubern und Verkauf.
- Rechnung dazu (`docs/plan/berufe-plan.md`, Beta-Preise): Lederverarbeitung 1–80 braucht 99 Fetzen, 62 Leichtes Leder netto und 27 Light Hide; die Route bringt bis Orgrimmar laut Modell etwa 66 Leder (mit der Annahme, dass die Nieren für Quest 821 vorher fallen) und 76 Fetzen, mit dem Grinden auf Stufe 16 (S1) 79–86 und 83–87. Ab LW 80 bringt ein Leichtes Leder 2- bis 5-mal weniger Punkte. Einkauf Stufe A etwa 40s, B 1g 67s, C 2g 73s, D 7g 38s (ohne Lehrer und Rezepte). Preisregeln, wann eine Wahl kippt: berufe-plan.md §6 (mit den 30-Tage-Medianen lohnen sich z. B. zusätzliche Embossed Leather Gloves zum Entzaubern).

---

## 2. Was RXP gratis und offen hat

**Quelle:** https://github.com/RestedXP/RXPGuides (Lizenz CC BY-NC-SA 4.0, Datei `LICENSE`).

| Datei | Guides darin | Gruppe |
|---|---|---|
| `Guides/forever/Horde-1-12_Mulgore.lua` | 1-6 Mulgore (62 Schritte), 6-12 Mulgore (275) | RestedXP Forever Guide (H), Untergruppe «Speedrun Guide 1-22», `#defaultfor Tauren` |
| `Guides/forever/Horde-12-22_Barrens.lua` | 12-17 The Barrens (399), 17-22 Stonetalon/Barrens/Ashenvale (460) | dito; `#next 22-24 Hillsbrad` zeigt auf den gekauften Teil |
| `Guides/Forever/dungeon/Horde-1-12_Mulgore.lua` | 1-6 Mulgore, 6-12 Mulgore, je nur ein `#include RestedXP Forever Guide (A)\…` | RestedXP Forever Dungeon Guide (H), Untergruppe «(WIP) Dungeon Guide 1-22», `#beta`, `#defaultfor Tauren` |
| `Guides/Forever/dungeon/Horde-12-22_Barrens.lua` | 12-17 The Barrens (403), 17-22 Stonetalon/Barrens/Ashenvale (436), beide `#xprate <1.99`; dazu 13-20 The Barrens und 20-24 Stonetalon/Barrens mit `#xprate >1.99` | dito; `#next RestedXP Horde 22-30\22-24 Hillsbrad` |
| `Guides/Forever/RestedXP-Skyborne.lua` | neues Startgebiet Zephras Isle | – |

- Schrittzahlen gezählt in Release v4.11.23, mit Klassen-Varianten.
- Dungeon-Route (v4.11.23, gelesen am 15.10.):
  - Die Dungeon-Mulgore-Guides binden «RestedXP Forever Guide (A)\1-6 Mulgore» bzw. «…\6-12 Mulgore» ein. Einen Guide mit Gruppe «(A)» und diesem Namen gibt es in v4.11.23 nicht (`git grep "#name 1-6 Mulgore"`); findet RXP ihn nicht, meldet es «Error trying to include guide» (`GuideWindow.lua` `IncludeGuide`). Lesart von Claude: Gemeint ist die Speedrun-Route. Im Spiel ungeprüft.
  - Schon die Speedrun-Route enthält Dungeon-Schritte: «12-17» 71 Schritte mit `.dungeon` (RFC 68, DM 3), «17-22» 125 (WC, DM, BFD). In Forever erscheinen sie nie (§4, Dungeons).
  - Die Dungeon-Route ist eine eigene Route, nicht die Speedrun-Route mit Dungeons: «12-17» +683/−577 Zeilen gegenüber der Speedrun-Route, «17-22» +427/−374. Ein Tauren-Druide sieht ohne Dungeons 150 bzw. 171 Schritte (Speedrun-Route 184 bzw. 198), mit RFC, WC und BFD 202 bzw. 222 (`tools/rxp_schritte.py … --dungeons RFC,WC,BFD`). Ohne Dungeons fehlen in der Dungeon-Route also Quests, die die Dungeons ersetzen.
  - Welcher Brachland-Teil gilt, entscheidet `#xprate` im Kopf (§3); in Forever ist das «12-17» und «17-22».
  - Hauptzweig (dec489a2, 15.10.): Die Dungeon-Route im Brachland heisst dort «12-17 The Barrens» und «17-22 The Barrens», die Teile 13-20 und 20-24 fehlen. Ein Neubau auf dem nächsten Release braucht deshalb eine neue Anker- und Namensprüfung.
- Laut kami-labs (09.10.) sind Stufe 1–20 für alle gratis (**Widerspruch**: Die Gratis-Dateien im RXP-Repo reichen bis Stufe 22, Tabelle oben). Der volle Guide kostet 45 USD für beide Fraktionen oder 30 USD für eine. Die Forever-Routen 1–35 sind fertig, für 35–60 nutzt RXP vorerst die Era-Routen. https://kami-labs.fr/en/wow-forever/mise-a-jour-restedxp-wow-forever/
- Der gekaufte Teil kommt als Import-Text, der verschlüsselt und an das Konto gebunden ist (Code: `GuideLoader.lua`, Funktion `CheckDataIntegrity` ab Zeile 274; Meldung «Account mismatch»). Den können und wollen wir nicht lesen.

**Update-Takt (Git-Historie, gemessen am 13.10.)**
- 276 Commits an den Forever-Guides seit 17.09.
- 31 Commits an den zwei Horde-Dateien, die wir mischen, an 22 von 27 Tagen.
- Releases: v4.11.14 (03.10.) bis v4.11.23 (10.10.), also 10 Releases in 8 Tagen. Der Hauptzweig ist dem letzten Release voraus.
- Umfang in den zwei Horde-Dateien: v4.11.14 → v4.11.23 +424/−181 Zeilen; v4.11.23 → Stand 13.10. +181/−48 Zeilen.
- `#version` bleibt dabei bei 11. Taugt nicht als Änderungsmerkmal; massgebend ist die Addon-Version (Tag).

**Stand 14.10. abends** (`git fetch` im RXP-Klon)
- Neuester Release ist weiter v4.11.23. Der Hauptzweig steht bei 998caf30 (14.10. 20:15), 46 Commits weiter.
- 4 dieser Commits ändern die zwei Horde-Dateien, zusammen +216/−69 Zeilen:
  - 060d66a0 (11.10.) «Added Cat form chain / fixes + updates forever»
  - 7b37767e (11.10.) «Typo / Parsing error fixes»
  - aa016195 (12.10.) «1-22 minor improvements/fixes Forever»
  - df745bd3 (13.10.) «Barrens minor fixes/improvements Forever»
- Inhalt:
  - In «1-6» und «6-12» fällt `#era/som--h` aus dem Kopf. In «6-12» kommen Hardcore- und Softcore-Varianten (Sparring Match, `.deathskip`), `.money <0.01` beim Kochlehrer und ein zweites Abgeben von «Camping 101: Cooking» bei Pyall dazu.
  - Im Brachland: kleine Korrekturen, ein Schritt `.xp 20` vor Thunder Bluff und die Druiden-Questreihe «The Great Cat Spirit» (§5).
- RXP baut seine Pakete weiter über `.github/workflows/package.yml` (BigWigs packager, bei jedem Push auf `main` und bei Tags). Am 12.10. entfernt: nur der FTP-Upload (Commits 598cf6d6, 96422b90).
- Eine Alpha-Version, wie sie das Testlog als «v4.11.23-46-g998caf30» melden würde, löst git auf (`git rev-parse` ergibt 998caf30). `fetch_rxp.sh` und `build_kombi.py` nehmen sie also auch.
- Probebau auf dem Hauptzweig: siehe §5 (Anker) und §6 (Stellen).

---

## 3. Wie RXP Guides lädt (Code-Fakten, Stand 9c7aaaf)

- **Registrieren:** `RXPGuides.RegisterGuide(text)` (`GuideLoader.lua` ~L416, global gesetzt ~L1269). Vor dem Laden landen Guides in einer Warteschlange.
- **Kopf-Prüfung beim Laden** (`LoadGuide`, ~L542–640):
  - Der Kopf (alles vor dem ersten `step`) muss `#FOREVER` enthalten (Gross/klein egal), sonst wird der Guide in Forever deaktiviert.
  - `<< Horde` setzt `enabledFor`.
  - `#name` und `#group` sind Pflicht.
  - Gibt es Gruppe und Name schon, meldet RXP «Error trying to load a guide already parsed».
- **Spielversion** (`ParseGuide`, ~L1046): `#classic` gilt auch in Forever. `#forever` zählt nicht als Spieltag, beschränkt also nichts.
- **`#beta` im Kopf:** Der Kopf setzt `guide.beta` (`GuideLoader.lua` ~L1113–1123), und `IsGuideActive` prüft `BetaVersionCheck(guide)` (`GuideWindow.lua` ~L2398–2402, `RXPGuides.lua` ~L2695). Ein solcher Guide erscheint nur mit «Beta-Features aktivieren» (Einstellungen, «Erweiterte Einstellungen»; deutsche Texte aus `locale/deDE.lua` L333–334). RXPs Forever-Dungeon-Guides haben `#beta`, unsere Gruppen nicht.
- **`#xprate` im Kopf:** gilt für den ganzen Guide (`XpRateCheck(guide)`, gleiche Stelle). In Forever bleibt die XP-Rate beim Standard 1 (`xprate = 1` in den Standardwerten von `SettingsPanel.lua`): `DetectXPRate` setzt bei Spielversionen unter 20000 nur die Saison.
- **Ein aktiver Guide:** `addon:LoadGuide` ersetzt den aktuellen (`GuideWindow.lua` ~L1812). Zwei Guides gleichzeitig gehen nicht.
- **Farm-Guides:** Gruppen mit `+` am Anfang erscheinen nur im «Gold Assistant Modus» (umschaltbar im Menü).
- **Fortschritt pro Guide:** `RXPCData.guideProgress[guide.key]` mit Schritt und Schritt-ID (`RXPGuides.lua` L1399–1447). Wechseln und zurück behält die Stelle.
- **Globale Werte, die das Testlog liest:** `RXPCData.currentGuideGroup`, `currentGuideName`, `currentStep`; gespeichert bei jedem Schrittwechsel (`GuideWindow.lua` ~L785). `RXP = addon` ist global, laut Kommentar «debug purposes».
- **Lokalisierung:**
  - Quest-Namen holt RXP vom Client, wenn das Element keinen eigenen Text hat (`.accept 870` ohne `>>`).
  - NPC-Namen in `.target`/`.mob` übersetzt RXP über `locale/NPCnames.lua`, Deutsch im Abschnitt `deDE`.
  - Deutsche Menütexte stehen in `locale/deDE.lua`, z. B. «Verfuegbare Guides», «Gold Assistant Modus aktivieren».
  - Eigene Texte nach `>>` zeigt RXP so, wie sie dastehen.

---

## 4. Syntax-Referenz (aus dem Code gezogen)

**Kopf-Tags** (Forever-Guides): `#forever`, `<< Horde`, `#name`, `#displayname`, `#version`, `#group`, `#subgroup`, `#next A;B`, `#defaultfor Tauren`, `#era/som`. `#next Gruppe\Name` springt in eine andere Gruppe.

**Schritt-Tags** (Häufigkeit in den Forever-Guides und Bedeutung):

| Tag | Anzahl | Wirkung |
|---|---|---|
| `#completewith X` | 2649 | Schritt bleibt sichtbar, bis Schritt mit Label X (oder `next`) fertig ist |
| `#optional` | 1441 | nicht zwingend |
| `#label X` | 1294 | Ankername |
| `#loop` | 449 | Koordinaten der Schritte im Kreis |
| `#requires X` | 376 | nur aktiv, wenn Label X erfüllt |
| `#xprate <1.59` | 342 | je nach eingestellter XP-Rate |
| `#season 0` | 249 | je nach Saison-Einstellung |
| `#sticky` | 226 | bleibt bis erledigt |
| `#softcore` / `#hardcore` | 190 / 133 | je nach Modus |
| `#ah` / `#ssf` | 76 / 35 | Auktionshaus- bzw. Selbstversorger-Schritte |
| `#include Gruppe\Name` | 25 | Abschnitt eines anderen Guides einbinden |
| `#hidewindow` | 24 | Schritt ohne Anzeige |

**Klassen-/Rassen-Filter** (`<< …`, `GuideLoader.lua` L36–104): `/` heisst ODER, Leerzeichen heisst UND, `!` verneint, Klammern gruppieren. Eine Zahl prüft die Stufe (Stufe ≥ Zahl). Beispiele: `<< Tauren Druid`, `<< !Tauren`, `<< Rogue/Warrior`.

**Befehle** (165 definiert, 59 in Forever-Guides genutzt). Die wichtigsten:

| Befehl | Argumente | Hinweis |
|---|---|---|
| `.goto` | `mapID/1,welt-x,welt-y[,radius[,0]]` oder `Zone,x,y` | 15'044× genutzt; `--c:Zone,x,y` dahinter ist Kommentar |
| `.accept` / `.turnin` | `questID[,flags]` | ohne Text nimmt RXP den Quest-Namen vom Client |
| `.complete` | `questID,objective` | |
| `.collect` | `itemID,anzahl[,questID,…]` | zeigt Fortschritt, z. B. `.collect 2318,416` |
| `.skill` | `beruf,[<]stufe[,1]` | ohne 3. Wert: erfüllt ab Stufe; mit `,1`: Schritt wird übersprungen, wenn die Bedingung stimmt (`.skill skinning,<1,1` = nur mit Kürschnerei) |
| `.maxskill` | wie `.skill`, prüft das Maximum | zeigt, ob der nächste Rang gelernt ist |
| `.train` | `spellID` | Fertigkeit lernen |
| `.trainer`, `.vendor` | `npcID` | |
| `.target`, `.mob` | Namen (Englisch), `+` für Untereintrag | RXP übersetzt |
| `.fly`, `.fp`, `.hs`, `.home`, `.bindlocation` | Ort | |
| `.xp` | `<20,1` usw. | Stufenbedingung |
| `.isOnQuest`, `.isQuestComplete`, `.isQuestTurnedIn`, `.isQuestAvailable` | `questID` | Bedingungen |
| `.zone`, `.subzone`, `.zoneskip`, `.subzoneskip` | Zone bzw. Gebiets-ID | `.subzone` braucht zwingend Text |
| `.dungeon` | `WC` usw. | nur bei eingeschaltetem Dungeon |
| `.itemcount`, `.use`, `.cast`, `.timer`, `.link`, `.money` | | |

- Berufsnamen für `.skill`: `alchemy blacksmithing enchanting engineering herbalism leatherworking mining skinning tailoring cooking firstaid fishing` (`DB/forever/db.lua` L235). RXP löst sie über Zauber-IDs auf, das geht auch im deutschen Client.
- `.tradeskill npcID,index` lernt beim Lehrer über die Listenposition. Das ist anfällig, wir nutzen es nicht.

**Fallen:**
- `--` in einer Textzeile schneidet den Rest ab (Kommentar).
- `[[` oder `]]` im Text beendet den Lua-String.
- `.subzone` ohne Text führt zu einem Ladefehler.
- Leere Argumente gibt es nicht: RXP teilt die Argumente mit `string.gmatch(args, "[^,]+")` (`GuideLoader.lua`, `parseLine`). `.collect 2318,19,,0,8` wird deshalb zu Quest 0 und Ziel-Maske 8. Richtig: `.collect 2318,19,0,1,24` (Flags 8 = Bank zählt mit, 16 = nicht an eine Quest gebunden). Der Generator meldet `,,` als Fehler.
- `.collect` zeigt bei Forever (Spielversion unter 90000) «Text» und darunter «Gegenstand: x/y»; erfüllt ab y, wieder offen, wenn der Bestand sinkt (`functions.lua`).
- `.skill beruf,n` ohne dritten Wert zeigt keinen Zähler, nur den Text und ein Häkchen ab Fertigkeit n. `.maxskill beruf,150` ist erfüllt, sobald der Geselle gelernt ist (ohne Zauber-ID).
- `.goto` ohne Radius zeigt den Pfeil und hält den Schritt nicht auf (Element «textOnly»). Ein Radius über 0 macht das Hingehen zur Bedingung, ausser mit einem fünften Argument (wie in RXPs Schleifen `…,60,0`); Radius 0 ohne fünftes Argument nimmt den Pfeil weg (`functions.lua`, `addon.functions["goto"]`). Farm-Stopps nutzen deshalb `.goto` ohne Radius.
- `.xp N,1` überspringt einen Schritt ab Stufe N, `.xp <N,1` unter Stufe N; `.xp N` allein heisst «Grind to level N» (`functions.lua`, `addon.functions.xp`). Daraus stammen die Stufen-Stände der Route im Mengenmodell.
- RXP merkt sich Berufsstufen bis zum nächsten `/reload`: `currrentSkillLevel` (`RXPGuides.lua`) wird nur für Berufe gesetzt, die in der Fertigkeitsliste stehen, und nie geleert. Ein verlernter Beruf behält also bis zum Neuladen seine alte Stufe; erst danach liest `GetSkillLevel` ihn als −1. `.skill beruf,<1` würde das Verlernen deshalb erst nach `/reload` bemerken. Der Kombi-Guide nimmt fürs Verlernen ein Kästchen (Aktion `manuell`) und blendet den Schritt mit `.skill beruf,<1,1` nur für Charaktere mit dem Beruf ein.
- `.collect` und `.itemcount` zählen nur den eingeloggten Charakter: `C_Item.GetItemCount(id, includeBank)` mit zwei Werten (`functions.lua` Z. 88, 3089, 6198; v4.11.23), also Taschen und mit Flag 8 bzw. drittem Wert die eigene Bank. Post, andere Charaktere und die Kontobank zählen nicht (den fünften Wert `includeAccountBank` hat die Forever-API, `ItemDocumentation.lua`, Build 70450; RXP übergibt ihn nicht). RXP fragt Syndicator nur im Quest-Planer (`DB/questDB.lua` Z. 25–39), nicht in den Guide-Schritten. Schickt der Druide Leder zum Bankchar, zeigen die Leder-Zähler im Kombi-Guide also weniger (Testlog 17.10.). Eine Kontobank gibt es in Forever nicht: Blizzard erwägt eine «in the not-too-distant future» (https://massivelyop.com/2026/10/13/world-of-warcraft-forever-devs-discuss-account-wide-banks-new-races-and-tanking-shamans/), das Testlog fand am 15.10. keine Reiter (T18).
- `.itemcount id,n[,1]` erledigt einen Schritt, wenn beim Aktivieren weniger als n Stück da sind (mit 1 als drittem Wert zählt die Bank mit). RXP prüft das nur beim Aktivieren: `itemcount` hat kein Ereignis (`functions.lua`), `BindActiveStepElement` (`GuideWindow.lua`) ruft es einmal auf. Geht das Material mitten im Schritt aus, bleibt der Schritt stehen; die Texte im Kombi-Guide sagen dann «Häkchen setzen».
- Ein Schritt nur aus `>>Text` gilt sofort als erledigt: Eine `>>`-Zeile ohne Befehl wird ein reines Textelement (`textOnly`, `GuideLoader.lua` `parseLine`), und `UpdateStepCompletion` (`GuideWindow.lua`) prüft nur die anderen Elemente. Das gilt auch mit `#completewith`: Solche Schritte werden «sticky» und verschwinden sofort. `+Text` ergibt ein Kästchen zum Abhaken (Aktionen `manuell` und `hinweis` im Generator).
- `.money <X` erledigt einen Schritt, solange weniger als X Gold da sind, und prüft das laufend (`functions.lua` `money`). Für Einkaufsschritte taugt das nicht: Der Schritt verschwindet mitten im Einkauf.
- `.maxskill` hat kein Ereignis (`functions.lua`: es gibt `events.skill`, aber kein `events.maxskill`; `GuideLoader.lua` setzt das Tag `maxskill`). RXP prüft es nur, wenn der Schritt aktiv wird (`BindActiveStepElement` ruft das Element einmal auf). Ein Gesellen-Schritt hakt sich nach dem Lernen also nicht von selbst ab, erst nach dem nächsten Laden (`/reload`). Seit v0.5.3 hängt `build_kombi.py` darum `.istrained <Zauber>` an: Es hört auf `TRAINER_SHOW`, `CHAT_MSG_SYSTEM`, `SKILL_LINES_CHANGED` und `TRAINER_UPDATE` (`events.istrained = events.train`) und erledigt den Schritt, sobald `IsPlayerSpell` den Zauber kennt. IDs des Gesellen aus RXPs `DB/forever/db.lua` (`addon.professionID`, meist in der Reihenfolge Lehrling, Geselle …; bei Verzauberkunst steht 13920 vorne): Lederverarbeitung 3104, Verzauberkunst 7412, Kürschnerei 8617, Angeln 7731; Kräuterkunde 2368 aus RXPs `Guides/Herbalism.lua`. Ob der Forever-Client den Gesellen unter diesen IDs führt, ist ungeprüft; Lehrling Angeln 7620 und Kochen 2550 hat das Testlog beim Lernen gesehen, jeweils mit einer zweiten neuen ID (1240948 bzw. 1240945; GELERNT 13.10.). Kein RXP-Forever-Guide nutzt `.istrained`. RXP prüft mit `addon.IsPlayerSpell` (`RXPGuides.lua`: `IsPlayerSpell`, `IsSpellKnown`), wie bei `.train`; `IsPlayerSpell` steht in der Forever-UI nur im Rückfall-Ordner `Blizzard_DeprecatedSpellBook` (CVar `loadDeprecationFallbacks`), ob es im Spiel greift, ist ungeprüft. Kennt der Client die ID nicht, bleibt alles wie vorher (Häkchen setzen); kennt der Charakter sie schon vor dem Lernen, verschwände der Schritt zu früh (T29 prüft beides; Gegenprüfung 16.10.).
- `.train` kauft bei offenem Lehrerfenster selbst, wenn «Trainer automation» an ist (`SettingsPanel.lua`, Standard: an, ausser `RXPData.disableTrainerAutomation`): `OnTrainer` (`RXPGuides.lua`) kauft 15 Sekunden lang alle 0,2 s den ersten verfügbaren Eintrag, dessen Name dem Zauber gleicht oder dessen Fertigkeitslinie (`GetTrainerServiceSkillLine`) dem Zaubernamen gleicht. Bei Berufslehrern mit Rezepten könnte das ein Rezept derselben Linie treffen (ungeprüft, Risiko 28). Die Gesellen-Schritte nutzen darum `.istrained` (ohne Kauf), nicht `.train`.
- `#maxlevel N` blendet einen Schritt beim Laden aus, wenn der Charakter über Stufe N ist und «Skip overleveled steps» an ist (Standard; `RXPGuides.lua` `LevelCheck`).
- Zusatzschritte, die die Route nicht aufhalten (geprüft 16.10. für die Dungeon-Vorquests, v4.11.23):
  - `#completewith <Label>` macht einen Schritt «sticky» (`GuideWindow.lua`: `if step.completewith and not step.tip then step.sticky = true`): Er steht neben dem aktuellen Schritt im Fenster und hält die Route nicht auf. Er verschwindet, wenn seine Elemente erledigt sind oder wenn der Schritt mit dem Label erledigt ist (`UpdateStepCompletion`).
  - `#optional` dagegen blendet einen Schritt nur in der Schrittliste aus (`IsFrameShown`, `UI/V2/Core.lua`); im Fenster hält er die Route auf, bis er erledigt ist.
  - `.accept` gilt als erledigt, wenn die Quest im Log steht oder schon abgegeben ist (`functions.lua` `accept`: `IsQuestTurnedIn(id) or IsOnQuest(id)`).
  - `.isQuestComplete X` überspringt einen Schritt, solange X nicht erledigt im Log steht (Tooltip «Missing pre-requisites»); RXP prüft das bei Quest-Ereignissen neu (`events.isQuestComplete = events.complete`).
  - `.zone <Karte> >>Text` erledigt den Schritt beim Betreten der Karte (`addon.functions.zone`), wie RXPs Zeppelin-Schritt «ZeptoUC1» (`Guides/forever/Horde-01-12_Durotar.lua`).
  - `.zoneskip A/B/C[,1]`: ohne `,1` erledigt, wenn man auf einer der Karten ist; mit `,1`, wenn man auf keiner ist. RXP prüft bei jedem Gebietswechsel (`events.zoneskip = zoneEvents`); ist die Karte nicht lesbar (in Instanzen meldet das Testlog keine Karte), passiert nichts (`type(currentMap) ~= "number"`).
  - `.goto Karte/Kontinent,…`: Kontinent 0 = Östliche Königreiche, 1 = Kalimdor (`element.instance`); RXP vergleicht ihn mit dem Kontinent des Spielers (`map.lua`, `wrongContinent`). RXPs eigene Schritte schreiben `1420/0`, `1458/0`, `1421/0` (Tirisfal, Unterstadt, Silberwald); `build_kombi.py` setzt den Kontinent seit 16.10. selbst (vorher stand immer 1).
  - `Name::NPC-ID` in Text und `.target` (z. B. `Tabitha Heartweaver::250686` im RXP-Hauptzweig): RXP setzt über die NPC-ID den Namen aus dem Client ein (`functions.lua` `ReplaceNpcIds`, `CheckNpcIds`, schon in v4.11.23). Für neue Forever-NPCs ohne Eintrag in `locale/NPCnames.lua` ist das der Weg zum deutschen Namen.
  - Ketten: Zeigt `#completewith` auf einen Schritt, der selbst `#completewith` hat, ist der erste erledigt, sobald der zweite erledigt oder übersprungen ist (`UpdateStepCompletion`: `if guide.steps[completewith].sticky then if RXPCData.stepSkip[completewith]`). Blendet `.xp …,1` einen solchen Schritt aus, setzt RXP ihn sofort auf erledigt (`functions.lua` `xp`: `step.completed = true`), und der erste verschwindet mit. Zwei Annahmen mit `#completewith next` hintereinander gehen deshalb nicht: Nimmt man die zweite an, verschwindet die erste. Mehrere Annahmen am selben Ort zeigen auf ein Label danach (Abstecher: «KombiV17») oder stehen in einem Schritt. `build_kombi.py` meldet die Kette `bis next` → Zusatzschritt mit `bis` seit 16.10. als Fehler; `tools/rxp_schritte.py ziele` sucht das Ziel jedes Zusatzschritts für 9 Klassen und 5 Rassen.
  - Häkchen: Das Kästchen vor jedem Element (Tooltip «Skip step») setzt `element.skip` (`GuideWindow.lua` `ActiveStepElementPostClick`); damit lässt sich jeder Schritt abhaken, auch `.zone` und `.abandon`.
  - Pfeil: RXP nimmt die Schritte mit `#completewith` vor dem aktuellen Schritt in die aktiven Schritte auf (`GuideWindow.lua` `SetStep`: zuerst `for i = 1, n - 1` die offenen «sticky», dann der aktuelle) und zeigt den Pfeil auf das erste Ziel in dieser Reihenfolge (`map.lua` `updateArrowData`, `SetArrowWP`). Ein Zusatzschritt mit `.goto` zieht den Pfeil also zu sich, bis er erledigt oder abgehakt ist. `.goto …,0,0` (Radius 0 mit fünftem Argument) macht das Ziel nachrangig (`lowPrio`): Der Pfeil zeigt erst dorthin, wenn kein anderes Ziel ansteht; die Stecknadel auf der Karte bleibt. So machen es RXPs Forever-Guides bei Schritten mit `#completewith` (z. B. `Guides/forever/Alliance-1-10_NightElf.lua`, Label «balance1»). Ohne fünftes Argument nimmt Radius 0 den Pfeil weg (`addon.functions["goto"]`).
  - `.abandon X` ist erledigt, wenn X nicht im Log ist, sonst hält der Schritt die Route auf (`functions.lua` `abandon`). RXPs Speedrun-Route hat solche Schritte ohne `.dungeon`, sie erscheinen also auch ohne Dungeons: in «17-22» nach «WCEnd» für die WC-Quests 1486, 1487, 1491, 959, 914 und 962 (Thunder Bluff, nach den Druiden-Schritten in Moonglade) und am Ende von «17-22» unter anderem für 6563 (BFD). Die RFC-Abbrüche in «12-17» (5723, 5725, 5728, 5761) stehen nur mit `.dungeon RFC` und erscheinen in Forever nicht (v4.11.23).
  - `.isOnQuest a,b,…` zeigt einen Schritt nur, wenn mindestens eine der Quests im Log steht (`functions.lua` `isOnQuest`). Für Abgaben von Liefer-Quests (ein Gegenstand bringen, ohne Ziel im Log) nimmt RXP `.isOnQuest` (z. B. 5724 «Returning the Lost Satchel», Allianz-Wappen 95189); `.isQuestComplete` fragt `C_QuestLog.IsComplete`, ob das bei Quests ohne Ziel wahr ist, ist ungeprüft. Der Kombi-Guide macht es seit 16.10. wie RXP.
  - Ein Schritt nur aus Tags (z. B. RXPs `#optional` mit `#label DeathDUPpickup`) hat kein Element, auf das RXP wartet, und ist sofort erledigt. Als Ziel von `#completewith` markiert er nur eine Stelle: Ein Zusatzschritt bleibt bis dorthin stehen, wenn davor ein Schritt liegt, auf den RXP wartet; folgt das leere Ziel gleich nach dem Zusatzschritt, verschwindet dieser sofort (Prüfung 16.10.; `tools/rxp_schritte.py ziele` meldet das).
  - Quest-Automatik: RXP nimmt eine Quest beim Geber selbst an, wenn ihr `.accept` in einem aktiven Schritt steht oder im Schritt gleich nach einem aktiven (`RXPGuides.lua` `QuestAutoAccept`, Einstellung «Quest automation», Standard an: `enableQuestAutomation = true`, `SettingsPanel.lua`). Freiwillige Annahmen in Zusatzschritten nimmt man also beim Ansprechen des Gebers mit; wer eine nicht will, setzt vorher das Häkchen. Für Forever rechnet RXP mit 40 Plätzen im Questlog (`questLogSize`, `SettingsPanel.lua`), im Spiel ungeprüft.

**Dungeons** (Code v4.11.23, dazu Hauptzweig dec489a2 vom 15.10.)
- `.dungeon X` merkt sich X, `.dungeon !Y` merkt sich Y, je die letzte Zeile im Schritt (`functions.lua` `addon.functions.dungeon`). `DungeonCheck` (`RXPGuides.lua`) blendet den Schritt aus, wenn Y an ist; sonst zeigt es ihn, wenn X an ist oder der Schritt kein X hat. Eine `.dungeon`-Zeile mit `<< Klasse` gilt nur für diese Klasse (wie jede Zeile, `parseLine`).
- Labels zählt RXP nur unter den gezeigten Schritten, ebenso `#completewith next` (`GuideWindow.lua`: `guide.labels` und `step.index` werden über die gezeigten Schritte vergeben). Ein ausgeblendeter Schritt wirkt also wie ein gelöschter.
- In Forever lässt RXP keine Auswahl zu:
  - Die Dungeon-Einstellungen sind für `FOREVER` ausgeblendet (`SettingsPanel.lua` ~L1374–1435, `hidden = addon.game == "FOREVER" or …`).
  - Der «Guide Configurator» mit «Enable Dungeons» bricht für Forever gleich am Anfang ab (`UI/V2/GuideConfigurator.lua` L2–5: `if WOW_PROJECT_ID == WOW_PROJECT_CAMELOT then --TODO: Fix the dungeon selection for Camelot return end`). Den Knopf «Run Guide Configurator» blendet RXP dann aus (`SettingsPanel.lua` `splashUI`, `hidden = not (… LaunchConfigurator)`); im Spiel ungeprüft.
  - Beim Laden des gespeicherten Guides setzt RXP alle Dungeons auf «aus» (`RXPGuides.lua` ~L1365–1368, `addon.settings.dungeons:SetNone()`, gleicher TODO-Kommentar). Standard ist ohnehin «keine» (`dungeons = {}`).
  - Hauptzweig (dec489a2): Die Einstellungen erscheinen mit `/rxp debug`; Konfigurator und Zurücksetzen beim Laden sind unverändert.
- RXPs Empfehlung (`SetRecommended`, `SettingsPanel.lua`): Wert = Reise × 0,7 + Quests × 1,2 + Klasse × 1,4 aus `dungeonStats` (`DB/forever/db.lua`), an ab einem Wert über 7. Horde-Druide (v4.11.23): an WC 9,9, BFD 8,5, GNOMER 8,0, ZF und MARA 7,8, SFK 7,3, RFK und RFC 7,1; aus RFD 5,9, ULDA und ST 5,7, SM 4,5, DM 4,2. Kürzel wie in RXP; Gebiets-IDs in `dungeonList` derselben Datei (RFC 2437, WC 718, BFD 719, DM 1581).
- Guide-Wechsel statt Schalter (für den Switch Solo/Gruppe, offene Entscheidung 36): `#next A;B` lädt den ersten aktiven Guide der Liste (`functions.lua` L3882–3911, «Iterates through every guide until it finds a valid one»), nicht den zuletzt benutzten; einen Rücksprung «dorthin, wo ich herkam» gibt es damit nicht. Ein Schritt kann mit `.next Gruppe\Name` mitten im Guide einen anderen laden (`addon.functions.next`, gleiche Datei); kein RXP-Guide nutzt das (v4.11.23, 0 Stellen), im Spiel ungeprüft. Ein eigener Vorquest-Guide sprang im Spiel nach dem Queststand an die richtige Stelle (Testlauf 1, 13.10.).
- Dungeon-Quests in RXPs Dungeon-Route (v4.11.23, `Guides/Forever/dungeon/Horde-12-22_Barrens.lua`, für RFC dazu `Guides/forever/Horde-1-12_Mulgore.lua`; Namen und NPCs aus RXPs Texten, Orte aus RXPs Koordinaten mit `forever_karten.csv`):
  - RFC: Rahauro in Thunder Bluff (70.4, 29.6): 5722 «Searching for the Lost Satchel», 5723 «Testing an Enemy's Strength» (Schritt «RFCPickups1» in «6-12 Mulgore»; im Dungeon rät RXP, sie sich von der Gruppe teilen zu lassen). Thrall in Orgrimmar: Kette «Hidden Enemies» 5726 → 5727 → 5728 (für 5726 Kills in Skull Rock, bis «Lieutenant's Insignia» fällt), nach dem Lauf weiter mit 5729 und 5730 zwischen Thrall und Neeru Fireblade. Neeru Fireblade: 5761 «Slaying the Beast». Im Dungeon Maur Grimtotem: 5722 ab, 5724 «Returning the Lost Satchel» an (Abgabe bei Rahauro).
  - WC: Mebok Mizzyrix und Crane Operator Bigglefuzz in Ratchet (Brachland 62.4, 37.6 bzw. 63.1, 37.6; bis 16.10. stand hier 63.0, 37.2, die Stelle von Sputtervalve): 1491 «Smart Drinks», 959 «Trouble at the Docks». Apothecary Helbrim (Brachland 51.4, 30.2): 853 «Apothecary Zamah», laut RXP «a 45-minute timed quest», abzugeben bei Apothecary Zamah in Thunder Bluff (22.8, 20.9), dort 962 «Serpentbloom». Hamuul (Thunder Bluff 78.6, 28.6): 1490 «Nara Wildmane», dann Nara Wildmane (75.7, 31.6): 914 «Leaders of the Fang». Nalpak und Ebru über dem Höhleneingang (Kalimdor 51.9, 55.4): 1486 «Deviate Hides», 1487 «Deviate Eradication». Im Dungeon 6981 «The Glowing Shard», Abgabe bei Falla Sagewind (Brachland 48.2, 32.8).
- Weitere Dungeon-Vorquests der Horde bis Stufe 22 (Recherche 16.10., Belege und Widersprüche: `docs/recherche/2026-10-16_dungeon-vorquests.md`):
  - Ruinen von Lordaeron (RoL, neu in Forever, 15–20 laut Warcraft Tavern, kami-labs, allthings.how): in Unterstadt Morbin Lightbane 92421 (Königsviertel), Theodore Griffs 95216 (Apothecarium, ab 16), Varimathras 5725 (RFC); Deathguard Kristof 92422 (Tirisfal), Tabitha Heartweaver 92401 (Grabmal, Silberwald). Im Dungeon starten 95204 (Wappen, Abgabe Oran Snakewrithe, Magieviertel) und 97288 (Kopf, Abgabe Master Apothecary Faranell, Apothecarium; danach vier weitere Quests 97289–97292). Eingang: RXPs Allianz-Route `.goto 1458/0,170.700,1804.700` (Unterstadt 73.2, 11.4). RXP führt RoL für die Horde nicht (v4.11.23; Hauptzweig 16.10. nur ein ausgeschalteter Schritt).
  - Burg Schattenfang (SFK): 1013 bei Keeper Bel'dugur (Apothecarium, ab 16, Ort widersprüchlich); 1098 (High Executor Hadrec, Gruft im Grabmal) und 1014 (Dalar Dawnweaver, Grabmal) erst ab 18. Orte aus RXP v4.11.23 `Guides/forever/Horde-01-14_Undead.lua`.
  - Tiefschwarze Grotte (BFD): 6563 bei Je'neu Sancrea (ab 17 bzw. 18, nach 6562), 6921 ab 21; 6564 startet mit einem Gegenstand vor dem Dungeon, 6561 gibt Argent Guard Thaelrid im Dungeon (Bashana ist nur die Abgabe).
  - Kral der Klingenhauer (RFK, 29–38 laut Warcraft Tavern): Blueleaf Tubers 1221 bei Mebok in Ratchet ab 20, die Gegenstände liegen neben ihm.
  - WC: 1491 gibt es erst nach Raptor Horns 865 (RXPs Dungeon-Route nimmt sie im selben Schritt nach der Abgabe an; Recherche), 959 und 962 ab 14, 914 ab 10, 1486 ab 13, 1487 ab 15 (Icy Veins, Warcraft Tavern).
  - Nicht bis 22: Hall of Thanes (Allianz, keine Horde-Quests ausserhalb), Todesminen (nur Allianz), Excavation Site: Wetlands, City of Dalaran, Gnomeregan, Scharlachrotes Kloster (Quests ab 24 bzw. 25).
- Questlog: Wie viele Quests es in Forever fasst, ist ungeprüft. Die API-Doku nennt `MAXIMUM_NUM_QUESTS_LOG_CAN_ACCEPT` = 40 (`QuestConstantsDocumentation.lua` L160, Build 70425); `MAX_QUESTLOG_QUESTS` setzt nur der Mainline-Teil (`Blizzard_FrameXMLBase.toc`: `Constants.lua [AllowLoadGameType mainline]`).

---

## 5. Aufbau von Weg A

**Dateien beim Spieler**
- `Interface\AddOns\RXPGuides_KombiGuide\` mit `.toc` (`## Interface: 16001`, `## Dependencies: RXPGuides`) und `Kombi_Guide.lua`, gebaut von `tools/build_kombi.py`.
- `Interface\AddOns\RXPGuides_Kombi\` nur für den WC-Test (Testlauf 1).
- `Interface\AddOns\KombiTestlog\` für Notizen und Protokoll.
- Ordner der Beta: `World of Warcraft\_classic_beta_\` (kami-labs, 10.10.; beim Start am 04.11. **ungeprüft**).
- Die Versionsangabe aus der `.toc` eines schon geladenen Addons liest der Client beim `/reload` neu: Testlog 15.10., ENDE 21:58:18 und SITZUNG 21:58:27 mit «Kombiguide 0.5» statt 0.4 (`docs/tests/messdaten-2026-10-15.md`).
- Neu verknüpfte Addon-Ordner lädt der Client erst nach einem Neustart des Spiels; Änderungen an Addons, die schon geladen waren, übernimmt `/reload` (Testlog 13.10.: um 19:50 nach `/reload` «Kombi-Test nicht geladen», um 22:07 nach dem Neustart geladen; Testlog 2 kam um 19:50 per `/reload`).

**Mischen (Skript)**
1. RXP-Release holen, das der Nutzer installiert hat (Tag aus dem Testlog).
2. `RegisterGuide`-Blöcke trennen: Kopf und Schritte.
3. Kopf anpassen:
   - `#group Kombiguide (H)` bzw. `#group Kombiguide Dungeon (H)` (dort auch `#subgroup (WIP) Dungeon Guide 1-22` für alle vier Guides)
   - `#defaultfor` entfernen (sonst konkurrieren zwei Standard-Guides), ebenso `#beta` (§3)
   - letztes `#next` → `RestedXP Forever Guide (H)\22-24 Hillsbrad` (Gruppe «Kombiguide (H)»); die Dungeon-Gruppe behält RXPs Ziel «RestedXP Horde 22-30\22-24 Hillsbrad» (seit v0.5.2, `LAST_NEXT` in `build_kombi.py`)
   - Nur Dungeon-Gruppe: Dungeons aus `data/kombi/dungeons.csv` fest einbauen, bevor die Berufsschritte dazukommen (§4 Dungeons): Ein Schritt, den RXPs `DungeonCheck` mit dieser Auswahl ausblenden würde, fällt weg; bei den übrigen fallen die `.dungeon`-Zeilen weg. Gilt eine `.dungeon`-Zeile nur für eine Klasse und ändert sie für diese das Ergebnis, kommt die Bedingung in die Kopfzeile (`step << !Priest`). Fehlt ein Dungeon in `dungeons.csv`, bricht das Skript ab.
4. Berufsschritte an Ankern einfügen. Ein Anker ist eine eindeutige Zeile, z. B. `.turnin 768`, ein `#label` oder eine Quest-ID; der Zusatz ` @softcore` oder ` @hardcore` wählt unter doppelten Ankern den mit diesem Tag (seit v0.5.2, Kaga-Schritt).
   - Ein Anker muss genau einmal vorkommen, sonst bricht das Skript ab und meldet es.
   - Nie zwischen einen Schritt mit `#completewith next` und seinen Nachfolger einfügen. Das Skript schiebt die Einfügestelle weiter.
   - Berufsschritte bekommen Bedingungen, damit sie ohne den Beruf verschwinden (`.skill leatherworking,<1,1`).
   - Aktionen der Plan-Tabelle: `lernen`, `kaufen`, `ziel` (Menge mit Fortschritt), `fertigkeit`, `maxfertigkeit`, `abgeben`, `annehmen`, `hingehen` (Ort mit Radius), `hinweis` (nur Text, braucht `bis`), `manuell` (Kästchen zum Abhaken). Zeilen mit Status «aus …» baut der Generator nicht ein. Spalte `bis` setzt `#completewith`, `extra` nimmt weitere RXP-Zeilen (getrennt mit ` // `), `radius` gilt für den Ort. Liste im Kopf von `tools/build_kombi.py`.
   - Käufe im AH bekommen `#ah`.
5. Herkunft und Lizenz in den Dateikopf schreiben.
6. Prüfen:
   - Lua-5.1-Syntax
   - jeder Befehl existiert in `functions.lua`
   - Kopf-Pflichtfelder vorhanden
   - Anker gefunden
   - Schrittzahl = RXP plus eingefügte Schritte
7. Ins Repo (Pull Request), Textdateien in den Projektordner; ins Spiel kommt der Stand von `main` (seit 15.10. schreibt Claude ihn selbst in den AddOns-Ordner).

**Machbarkeitsprobe vom 13.10.** (`tools/merge_poc.py`, Basis v4.11.23)
- 4 Guides gemischt, 1 Probeschritt nach `.turnin 768` (Gathering Leather) eingefügt; der Anker war eindeutig.
- Lua 5.1 ok, 4 Guides registriert, Datei 356 KB, keine unbekannten Befehle.
- Kopf richtig umgeschrieben: Gruppe ersetzt, `#defaultfor` entfernt, letztes `#next` mit Gruppe.
- Im Spiel nicht getestet.

**Ankerstellen in der RXP-Route, die zu den Berufen passen** (v4.11.23; ausser dem Schlafsack auch schon in v4.11.13)
- Mulgore 6-12, Thunder Bluff:
  - Kürschnerei bei Mooranta lernen, mit Hinweis «This will unlock an easy quest»
  - Quest «Gathering Leather» (768): 12 Leichtes Leder, sonst im AH gekauft (`#ah`, nur mit Kürschnerei)
- Kochen: «The Great Outdoors» (96605) und «Camping 101: Cooking» (96661) in Mulgore.
- Fischen: ein Raw Brilliant Smallfish im Teich von Thunder Bluff für «Stalk With The Earthmother» (76240).
- Schlafsack: «...and that note you found» (79007) im Guide 17-22. Erst ab v4.11.23 (RXP-Commit «Added Engraved Ring / Sleeping bag part 1», 10.10.), nicht in v4.11.13.
- Berufs-Quests bei Kaga Wildhoof (Stonebull Lake, gleicher Ort wie «Camping 101: Cooking» in RXP): 97933 «Grundlagen des Zeltens: Kräuterkunde» und 97936 «Grundlagen des Zeltens: Kürschnerei» (im Spiel angenommen, Testlog 13.10. 22:13). RXPs Horde-Route führt beide nicht (v4.11.13, v4.11.23, Hauptzweig df745bd vom 13.10. abends). Für die Allianz führt RXP die Gegenstücke 97921 «Camping 101: Herbalism» und 97924 «Camping 101: Skinning» mit `.skill herbalism,<1,1` bzw. `.skill skinning,<1,1` (`Guides/forever/Alliance-1-13_Human.lua`).
  - Ziel jeweils Fertigkeit 20, ab Stufe 6 (benötigt 4), Belohnung 270 XP und das Rezept des Lager-Gegenstands (Camp Chair bzw. Incense Candle). Abgabe Horde in Mulgore: Kürschnerei bei Yonn Deepcut (Bloodhoof, 45.0, 61.4), Kräuterkunde bei Komin Winterhoof (Thunder Bluff, 49.8, 39.8). Quelle: warcraft.wiki.gg, Seiten «Camping 101: Skinning» und «Camping 101: Herbalism» (abgerufen 13.10.).
  - Im Kombi-Guide v0.2: Abgabe beider Quests (mit `.isQuestComplete`). Das Annehmen bei Kaga liegt vor der Stelle des Testcharakters (Abschnitt 6); seit v0.5.2 vorbereitet (Plan-Zeilen 83 und 84, Status «aus», offene Entscheidung 11).
  - Dazu 97932 «Grundlagen des Zeltens: Angeln» (im Spiel angenommen 17.10. 15:25:47 bei Kaga Wildhoof, Mulgore 46.2, 67.2; abgegeben 15:26:41 bei 44.2, 63.8: 270 XP und das Rezept Fischglas 1229745). Laut warcraft.wiki.gg (Seite «Camping 101: Fishing», Stand 11.10.2026): Stufe 6, ab 4, vorher «The Great Outdoors», Ziel «Raise your fishing skill to 20», Abgabe Horde in Mulgore bei Uthan Stillwater. RXPs Horde-Route führt sie nicht (v4.11.23, Hauptzweig 17.10.); im Skyborne-Guide des Hauptzweigs heisst sie 97967 und steht unter `.train 7620,3` (nur, wer Angeln hat; Flags 3 = Textelement und umgekehrt, `functions.lua` `train`). Ob die Annahme ohne Angeln geht, ist ungeprüft. Seit v0.6.3 im Kombi-Guide (unten).
- Brachland und Südbrachland bis Stufe 20 (gelesen am 14.10., v4.11.23, Tauren-Druide; Liste mit Schrittnummern in `docs/plan/mengen-leder.md`):
  - «6-12 Mulgore» endet in den Crossroads (#186–#194, Druiden-Lehrer davor mit `.xp <12,1`): Ankunft um Stufe 12.
  - Tier-Quests im Brachland: 844 (7 Schnäbel), 869 (12 Raptorenköpfe), 845 (4 Hufe), 903 und 821 (Savannah Prowler, Ebenenschreiter-Nieren, Thunder Lizard Horn), 95494 (6 Savannah Lion Hide, neu in Forever, bei Vrang), 905 und 865 (Sunscale Scytheclaw), 881 (Echeyakee), 880 (Oasis Snapjaw), 882 und 10338 (Ishamuhale, Zhevra Charger), 907 und 913 (Donnerechsen, Donnerfalke), im Eschental 98251 (je 6 Bären und Hirsche).
  - Stufen laut RXP: Druiden-Lehrer bei 14–15 (12-17 #34), «Grinding to level 16 here is important» an der Sludge Fen (#83), Lakota'mani erst ab 18 (#152), Lehrer 18–19 bzw. ab 20 nach dem ersten Steinkrallen-Besuch (17-22 #28/#29), Wolf Bracers ab 20 in Ratchet (17-22 #58), «Grind to level 21» im Eschental (#166).
  - Rund um die Crossroads tötet die Route gleich nach der Ankunft dieselben Tiere für 844, 869 und 845 (rund 46 Kills). Ein Farm-Stopp dort würde diese Kills nur vorziehen; zusätzliches Leder bringt Farmen erst an Tieren, deren Quests schon fertig sind.
  - Synergie: RXP schlägt an der Sludge Fen ohnehin Grinden auf Stufe 16 vor; der Kombi-Guide schlägt dafür Raptoren und Savannenkatzen gleich daneben vor (RXP-Schleifen #81/#82), damit das Grinden Leder bringt.
- Kombi-Guide v0.3 (14.10.): Leder-Zähler pro Abschnitt und drei optionale Farm-Stopps S1–S3 (Nordbrachland beim RXP-Grinden auf 16, Südbrachland bei den Scytheclaws, Camp Taurajo) mit Ziel aus dem Mengenmodell, ab Stufe 16 auch Mittleres Leder. Alle mit `.skill skinning,<1,1`, verschwinden also ohne Kürschnerei. In «12-17» erst nach Schritt #77 eingefügt (zweiter Testcharakter, §6).
- Orgrimmar in «12-17» (v4.11.23, Tauren-Druide #92–#108): Eingang West, Erste Hilfe (nur mit dem Beruf), Kette «Meal Appeal» (Valley of Strength, The Drag, Valley of Honor), Flugpunkt, «The Spirits of Stonetalon» bei Zor Lonetree (#107), Label «SpiritsPickup» (#108), danach Ruhestein zu den Crossroads (#109). Thunder Bluff in «17-22» (#85–#97, um Stufe 20): Flug, Bank, Ruhestein, Spirit Rise, Label «DeathDUPpickup» (#92), Erste Hilfe, Elder Rise.
- Kombi-Guide v0.4 (14.10.): Sweetspot-Zähler beim Farm-Stopp S1 (62 Leichtes Leder); Sitzung in Orgrimmar nach «SpiritsPickup» (AH, Kräuterkunde und Kürschnerei verlernen, LW 1–80, VZ 1–50, beide Gesellen, Stufe B optional); Sitzung in Thunder Bluff nach «DeathDUPpickup» (Stufen B–D, Verkauf). Einkauf mit Zählern (eigene Bestände zählen mit); Herstell-, Entzauberungs- und Verzauberungsschritte hängen an `.itemcount` und `.skill`: Sie entfallen, wenn das Material beim Erreichen des Schritts fehlt oder die Stufe schon erreicht ist; geht das Material mittendrin aus, setzt man das Häkchen. In Thunder Bluff zuerst der ganze Einkauf (Varianten «B und C», «C allein», «C und D»), «D allein» erst nach Stufe C. Alle Schritte nur mit dem jeweiligen Beruf (`.skill …,<1,1`). Die Leder-Zähler und Farm-Stopps nach Orgrimmar (S2, S3) sind entfallen.
- Kombi-Guide v0.4.1 (15.10.): für Charaktere, die die Berufe schon früher gewechselt haben (der Stufe-15-Charakter hat Lederverarbeitung 109 und Verzauberkunst 100). In Orgrimmar entfallen dann:
  - «Lerne Lederverarbeitung» und «Lerne Verzauberkunst», wenn der Beruf schon da ist (`.skill leatherworking,1,1`, `.skill enchanting,1,1`)
  - die Käufe der Stufe A ab LW 80 bzw. VZ 50 (`.skill leatherworking,80,1`, `.skill enchanting,50,1`)
  - der Kauf von Salt und Coarse Thread für Stufe B ab LW 100 (`.skill leatherworking,100,1`, auch in Thunder Bluff)
  
  Die Herstell- und Verzauberungsschritte entfielen schon vorher über `.skill` und `.itemcount`. Übrig bleiben das Kästchen «Weiter mit der Route» und die Kästchen fürs Entzaubern, falls Embossed Leather Gloves oder mehr als 10 Fine Leather Belts in den Taschen sind. Im Spiel ungeprüft.
- Kombi-Guide v0.5 (15.10.), Wunsch des Nutzers «ich brauche den MIT dungeons» (`docs/entscheidungen.md`): zweite Gruppe «Kombiguide Dungeon (H)» in derselben Datei `Kombi_Guide.lua` (so reicht beim Nutzer `/reload`; die Gruppe «Kombiguide (H)» bleibt Zeichen für Zeichen gleich, Stellen #45 und #103 geprüft).
  - Quellen: «1-6» und «6-12 Mulgore» aus der Speedrun-Datei (RXPs Dungeon-Mulgore bindet sie ein, §2), «12-17 The Barrens» und «17-22 Stonetalon/Barrens/Ashenvale» aus `Guides/Forever/dungeon/Horde-12-22_Barrens.lua`. Die Teile 13-20 und 20-24 (`#xprate >1.99`) nicht.
  - Dungeons: Vorschlag von Claude ist RXPs eigene Empfehlung für Horde-Druiden (§4): RFC, WC und BFD an, DM aus (`data/kombi/dungeons.csv`, offene Entscheidung 23). BFD betrifft in 12-22 nur Priester.
  - Mit dieser Auswahl fallen 3 RXP-Schritte in «12-17» und 34 in «17-22» weg (vor allem der Weg ohne WC: Ruhestein nach Thunder Bluff mit `.dungeon !WC`); ein Schritt bekommt `step << !Priest` (`.dungeon !BFD << Priest`). In «6-12 Mulgore» erscheint RXPs Schritt «RFCPickups1» (Quests 5722 und 5723 bei Rahauro, Thunder Bluff).
  - Geprüft mit `tools/rxp_schritte.py`: Für 9 Klassen und 5 Rassen zeigt die gebaute Gruppe (ohne Dungeons, wie in Forever) dieselben RXP-Schritte wie RXPs Quelle mit RFC, WC und BFD (180 Vergleiche, keine Abweichung).
  - Tauren-Druide in der Dungeon-Gruppe: «6-12 Mulgore» 208 Schritte, «12-17» 234 (davon 32 Kombi-Schritte), «17-22» 256 (34; seit v0.5.3 261 mit 39 Kombi-Schritten). RFC kommt gleich zu Beginn von «12-17» (Reise nach Orgrimmar, RXP-Text «Now you should be looking for a group to Ragefire Chasm»), WC in «17-22». Berufsschritte an denselben Ankern: Sweetspot-Zähler #106 vor `.xp 16` (Sludge Fen, gleicher RXP-Text wie in der Speedrun-Route), Orgrimmar nach «SpiritsPickup» (#123), Thunder Bluff nach «DeathDUPpickup» (#87).
  - Nicht neu gerechnet: Das Mengenmodell (`docs/plan/mengen-leder.md`) und die Leder-Ziele gelten für die Speedrun-Route. Wie viel Leder die Dungeon-Route bis Orgrimmar bringt, ist ungeprüft (offene Entscheidung 24).
  - Im Spiel ungeprüft (T22).
- Kombi-Guide v0.5.1 (15.10. Nacht): Texte der Berufsschritte mit den gemessenen Lernstufen und Kosten (Lehrerlisten Orgrimmar; in Thunder Bluff mit dem Zusatz «in Orgrimmar», weil dort noch nicht gemessen) und den deutschen Rezeptnamen in Klammern. Statt Enchant Bracer - Minor Deflect, das die Lehrer in Orgrimmar nicht führen, nimmt der Guide Enchant Chest - Minor Absorption (ab VZ 40, gleiches Material). Nur Text geändert, gleiche Zeilenzahl: Stellen #45 und #152 bleiben. Der Berufe-Plan (`docs/plan/berufe-plan.md`) rechnet die Punkte weiter mit Minor Deflect; beide sind dort orange, Material und Stückzahl gleich (ungeprüft im Spiel).
- Kombi-Guide v0.5.2 (15.10. spät, nach dem Prüfbericht von Claude): Thunder Bluff (Stufe C): Leichte Lederhosen und Dunkle Ledergürtel beim Händler verkaufen statt entzaubern (Forever-Händler 5s 99c bzw. 7s 3c, der Entzauberungs-Ertrag ist im AH weniger wert); dafür kauft Stufe C 69 Strange Dust und 20 Lesser Magic Essence dazu (Zähler). Enchant Boots - Minor Stamina fällt weg (14s für wenige Punkte; der Plan nimmt Bracer - Lesser Stamina). Bedingungen mit den gemessenen Lernstufen (Heavy Leather ab 125, Hillman's ab 120, Runed Silver Rod ab 100). Texte: Lernkosten in den Goldangaben, Minor Deflect laut SeeMeta mit dem Rang, Angeln im Teich (Hauptstädte bis 75), Kleinfisch nur, wenn man schon angelt. Vorbereitet, aber aus (Status «aus», offene Entscheidung 11): Annahme der Berufs-Quests 97933 und 97936 bei Kaga Wildhoof (Anker `accept 96661 @softcore`: RXP führt den Kaga-Schritt für Softcore und Hardcore doppelt); eingeschaltet würde sie die Stelle #45 verschieben (geprüft). Dungeon-Gruppe: `#next` wie bei RXP («RestedXP Horde 22-30\22-24 Hillsbrad»). Stellen #45 und #152 bleiben (geprüft für den Tauren-Druiden).
- Kombi-Guide v0.5.3 (16.10. früh, nach der zweiten Prüfrunde, `docs/tests/pruefbericht-2026-10-16.md`):
  - Gesellen-Schritte mit `.istrained` (oben, §4): Sie haken sich nach dem Lernen von selbst ab, wenn die Zauber-ID stimmt; sonst wie bisher Häkchen setzen. In «12-17» ersetzt die Zeile das überflüssige `.skill …,<1,1` (`<50,1` schliesst es ein), die Zeilenzahl bleibt.
  - Thunder Bluff für Quereinsteiger (LW schon über 100, wie der Stufe-18-Charakter): Hinweise für Geschmeidige leichte Bälge, Feine Ledergürtel und Geschmeidige mittlere Bälge (kaufen oder herstellen), damit Leichte Lederhose und Dunkler Ledergürtel nicht mangels Zwischenprodukt entfallen; der Zähler der Stufe C sagt, dass Quereinsteiger weniger brauchen (genaue Menge: `/tl tipp`).
  - Verzauberkunst 100–130 neu geordnet: zuerst die Runenverzierte Silberrute (ab VZ 100), dann Umhang - Schwacher Schutz bis 130; Brust - Schwache Absorption und Staub kaufen nur als Ausweg. Vorher hätten die 4 gekauften Lesser Magic Essence für die Rute in der Brust-Verzauberung landen können.
  - VZ 130–150 ohne eigenen Soul Dust: Stiefel - Schwache Ausdauer (80 Strange Dust, Lehrer 14s) statt gekauftem Soul Dust (Beta: etwa 81s gegen 1g 59s).
  - Leichte Lederhosen und Dunkle Ledergürtel verkauft man vor dem Einkauf der Stufe D (der Erlös von etwa 2g 14s hilft dabei).
  - Nach der Gegenprüfung (16.10.): VZ 50–70 zuerst mit Essenzen (Brust - Schwache Absorption), Brust - Minderwertige Ausdauer mit Staub nur, wenn Essenzen fehlen, in Orgrimmar und Thunder Bluff, wie im Berufe-Plan; so bleibt der Staub für den Umhang der Stufe C. Die Staub-Zähler der Stufe C zeigen den ganzen Bedarf: 85 (eigener Staub aus dem Entzaubern zählt mit, gekauft werden etwa 65) bzw. 68, wenn Stufe B erst in Thunder Bluff kommt (der Staub aus ihren Feinen Ledergürteln kommt nach dem Einkauf dazu). Vorher hätte der Zähler bei 65 etwa 20 Staub zu wenig gekauft. Für Quereinsteiger getrennte Hinweise zu Feinen Ledergürteln und Geschmeidigen mittleren Bälgen (neue Plan-Zeile 91). In «12-17» sind dabei nur zwei Schritte gleicher Länge vertauscht (#136 und #137 für den Druiden), die Stelle #152 bleibt.
  - Zähler mit dem neu gerechneten Plan: Stufe B 45 Lesser Magic Essence (oder Greater kaufen und teilen), Stufe C 65 Strange Dust und 4 Lesser Magic Essence; Texte nach Prüf-Regel (Quellen, «vermutlich» statt «sehr wahrscheinlich», Tamar gemessen).
  - Stellen «6-12 Mulgore» #45 und «12-17 The Barrens» #152 bleiben (geprüft für den Tauren-Druiden). Im Spiel ungeprüft.
- Kombi-Guide v0.6 (16.10., Entscheid des Nutzers «Wir bauen nur EINEN guide und setzten ALLE Pre quests für ALLE dungeons … hinein», `docs/entscheidungen.md`): Dungeon-Vorquests als Zusatzschritte in «Kombiguide (H)», Tabelle `data/kombi/vorquests.csv` (Nummern V…). Die Gruppe «Kombiguide Dungeon (H)» bekommt sie nicht (RXPs Dungeon-Route führt RFC und WC selbst) und bleibt Zeichen für Zeichen gleich.
  - Annahmen sind Erinnerungen (`#completewith`, §4): Sie stehen neben der Route, halten sie nicht auf und verschwinden mit dem Ziel-Schritt. Abgaben erscheinen nur, wenn die Quest erledigt ist (`.isQuestComplete`; bei Liefer-Quests `.isOnQuest`, wie RXP). Wo RXP die Vorquests in seiner Datei schon hat (versteckt mit `.dungeon`), stehen unsere Schritte meist an derselben Stelle; anders: Rahauro nach Cairne (bei RXPs «RFCPickups1» liegt `#completewith next`), Je'neu nach der Abgabe von 6562, Bigglefuzz und Nalpak/Ebru schon in «12-17».
  - Pfeil (§4): Bei Annahmen, an denen die Route nur vorbeiführt, ist das Ziel nachrangig (`.goto …,0,0`: Rahauro, Thrall, Neeru, Zamah, Bigglefuzz in «12-17», Nalpak, Tabitha, die SFK-Quests im Grabmal); der Pfeil bleibt bei der Route, die Stecknadel zeigt den Geber. So behält z. B. RXPs Sprungpfad von der Hunter Rise in Thunder Bluff seinen Pfeil («Follow the arrow precisely to avoid dying»). Wo man ohnehin beim Geber steht (Mebok, Bigglefuzz in «17-22», Nara, Je'neu) und im Abstecher zeigt der Pfeil auf die Annahme.
  - Thunder Bluff («6-12», nach Cairne): Rahauro, zwei RFC-Quests (RXPs Schritt «RFCPickups1»), sichtbar bis «WildManeTurnIn» (Ende von Mulgore).
  - Namen der Dungeons in den Texten deutsch (Flammenschlund, Höhlen des Wehklagens, Burg Schattenfang, Tiefschwarze Grotte, Kral der Klingenhauer, Ruinen von Lordaeron), Quest-Namen nicht: RXP zeigt sie aus dem Client.
  - Orgrimmar («12-17», vor «SpiritsPickup»): Thrall (5726, Anfang der Kette «Hidden Enemies») und Neeru Fireblade (5761), sichtbar bis zum Zeppelin-Schritt des Abstechers (so zeigt der Abstecher keine Erinnerung an Orgrimmar; unter Stufe 15 fällt der Zeppelin-Schritt weg, dann verschwinden sie nach der Berufssitzung).
  - Abstecher zu den Ruinen von Lordaeron («12-17», nach der Berufssitzung, vor RXPs Ruhestein zu den Crossroads; der Pfeil führt durch die Annahmen in Tirisfal und Unterstadt zum Eingang, Tabitha im Silberwald und die SFK-Quests im Grabmal sind nachrangig, `.goto …,0,0`): zuerst der Zeppelin (hält die Route auf; Häkchen = kein Abstecher), in Tirisfal, Unterstadt und Silberwald die Annahmen als Liste (Deathguard Kristof 92422, Morbin Lightbane 92421, Varimathras 5725 für RFC, Tabitha Heartweaver 92401), dazu ab Stufe 16 Theodore Griffs 95216 und Keeper Bel'dugur 1013 (SFK), der Lauf als Kästchen, danach nur die erledigten Abgaben (Wappen von Lordaeron 95204, Griffs, Faranell 97288, Morbin, Kristof, Tabitha) und ab Stufe 18 die zwei SFK-Quests im Grabmal (solange `#maxlevel 17` gilt, nur wenn Stufe 18 erst im Abstecher kommt und ohne Neuladen dazwischen). Alle Schritte nach dem Zeppelin tragen `.zoneskip 1420/1458/1421,1`: ohne Abstecher fallen sie in Orgrimmar weg, und wer vorzeitig mit dem Ruhestein geht, verliert sie ebenfalls. Der Rückweg ist RXPs Ruhestein-Schritt. RXP selbst führt die Ruinen für die Horde noch nicht (v4.11.23 nichts; Hauptzweig 16.10.: ein ausgeschalteter Schritt für Tabitha mit `.dungeon ROL` und dem Vermerk «TODO: Activate step once .dungeon ROL command works», `Horde-01-14_Undead.lua`).
  - «12-17» nach der Stelle #152 (ohne `#maxlevel`): WC bei Crane Operator Bigglefuzz beim ersten Halt in Ratchet («RapHornsPickup», sichtbar bis «LeaveRatchet»), Nalpak und Ebru über dem Höhleneingang bei der Lushwater Oasis (sichtbar bis «Hezrul»).
  - «17-22»: bei Mebok nach der Abgabe von Raptor Horns (vorher gibt es 1491 nicht) WC 1491 und ab Stufe 20 RFK 1221 in einem Schritt; Bigglefuzz, falls noch nicht angenommen; bei Zamah nach der Abgabe von 853 (sichtbar bis zur Elder Rise; mit `#completewith next` wäre sie sofort verschwunden, weil gleich danach RXPs leerer Schritt «DeathDUPpickup» kommt) und bei Nara nach der Abgabe von 1490 (Thunder Bluff); dort vor Hamuul die RFC-Abgaben bei Rahauro (nur wenn erledigt); BFD bei Je'neu Sancrea (Zoram'gar). Vor RXPs Abbruch-Schritten für WC und BFD (§4) je ein Kästchen «Gelesen», nur mit einer dieser Quests im Log: Wer den Dungeon noch machen will, setzt dort das Häkchen statt abzubrechen.
  - Alle Zusatzschritte in «12-17» vor der Stelle #152 tragen `#maxlevel 17`, damit der Stufe-18-Charakter seine Stelle behält (offene Entscheidung 37). Nebenwirkung (Prüfung 16.10.): Erreicht ein Charakter im Abstecher Stufe 18 und lädt dann neu (`/reload`, neu einloggen), während einer der Abstecher-Schritte aktuell ist (Lauf oder Abgaben), fehlen nach dem Laden die ausgeblendeten Schritte, die gespeicherte Zeile ist nicht mehr da, und RXP nimmt die Nummer: Es steht 7 bis 12 Schritte zu weit, z. B. hinter dem Wirt und den Abgaben in den Crossroads (Druide, Krieger, Jäger, Schamane; simuliert). Der Text beim Lauf warnt davor. Geprüft für alle 9 Klassen (Tauren, Stufe 18): RXP findet #152 über die Nummer; beim Schamanen traf die alte Zeile zuerst einen anderen Schritt, eine zusätzliche Textzeile im Neeru-Schritt behebt das. Ziele der Zusatzschritte geprüft mit `tools/rxp_schritte.py ziele` (9 Klassen, 5 Rassen, keine Kette).
  - Ablauf des Abstechers wie am 15.10. gespielt (Testlog, `docs/plan/spiel.md`): von 20:21 (Zeppelinturm, Durotar) bis 21:23 (Abgabe im Grabmal), Stufe 16 (39 %) bis 17 (64 %); im Dungeon 40 Minuten für 0,38 Stufen mit 2 Toden, die vier Abgaben brachten zusammen 19 250 XP.
  - 0.6.1 (16.10.): die Befunde der unabhängigen Prüfung (`docs/tests/pruefbericht-2026-10-16_vorquests.md`) sind oben eingearbeitet (Pfeil, Zamah bis zur Elder Rise, `.isOnQuest` bei Liefer-Quests, Warnung zum Neuladen ab Stufe 18, Texte).
  - Im Spiel ungeprüft (T34–T37).
- Kombi-Guide v0.6.2 (17.10.): nur Texte, gleiche Zeilenzahl: Pfand-Regel und gemessene Abnahme beim Auktionshaus in Thunder Bluff (Plan-Zeile 6), Geselle Kürschnerei mit den gemessenen Werten (Zeilen 8 und 11). Stellen «6-12 Mulgore» #116 (Druide) und «12-17 The Barrens» #152 (Stufe 18) geprüft.
- Kombi-Guide v0.6.3 (17.10. abends), Notiz des Nutzers bei Kaga Wildhoof «die angelquest ist ein muss» (`docs/entscheidungen.md`): «Grundlagen des Zeltens: Angeln» in «6-12 Mulgore» (Plan-Zeilen 92–96). Vor RXPs Kaga-Schritt (Druide #19, `turnin 96659 @softcore`) bei Harn Longcast eine Angel kaufen (23c, gemessen 13.10. bei 45.5, 61.7) und bei Uthan Stillwater Angeln lernen (1s, gemessen 13.10. bei 44.2, 63.8; `.train 7620`); nach «Camping 101: Cooking» (`accept 96661 @softcore`) die Quest bei Kaga annehmen (`.skill fishing,<1,1`), am Stonebull Lake bis Angeln 20 angeln (gemessen 13.10.: etwa 27 Sekunden und 1 Punkt pro Fang, also etwa 9 Minuten) und bei Uthan abgeben (`.isQuestComplete 97932`). Alle fünf Schritte tragen `#maxlevel 11`: Der Druide (Stufe 12, #153) sieht sie nicht, RXP findet seine Stelle über die Nummer (geprüft mit `tools/rxp_schritte.py vergleich … --stelle 153 --stufe 12`). Ohne Fisch kauft RXP den Kleinfisch für «Stalk With The Earthmother» im AH (`#ah`), Angeln lehrt RXP in Thunder Bluff nur im Modus `#ssf`; Zeile 4 sagt das jetzt. «12-17» unverändert (#152 geprüft für Druide, Jäger, Schamane, Krieger). Im Spiel ungeprüft (neuer Charakter).
- Probebau auf dem RXP-Hauptzweig (14.10., 998caf30):
  - Alle Anker passen ausser einem: «Camping 101: Cooking» (`turnin 96661`) kommt dort zweimal vor.
  - Plan-Zeile 5 hängt deshalb seit 14.10. an `label Vision` (davor). Auf v4.11.23 ist der Bau damit bytegleich.
  - Auf dem Hauptzweig fügt der Probebau alle 82 Zeilen ein, ohne Probleme.
- Katzengestalt:
  - RXP v4.11.23 lässt Druiden sie ab Stufe 20 bei Loganaar in Moonglade lernen («17-22» #29, `.train 768`, `.xp <20,1`).
  - Der Hauptzweig hat dazu die Questreihe «The Great Cat Spirit»: 98340 bei Turak in Thunder Bluff, Moonglade, Stormrage Barrow Dens, zurück nach Thunder Bluff (98362).
  - Sie beginnt gleich nach «DeathDUPpickup», also nach unserem Thunder-Bluff-Block. Was die Questreihe bringt, steht nicht im Guide-Text (ungeprüft).
  - Ob die Berufssitzung davor oder danach kommt, ist offene Entscheidung 13.
- Wo RXP selbst Berufe oder das AH berührt (v4.11.23, Brachland):
  - Erste Hilfe nur mit dem Beruf (`.skill firstaid,<1,1`).
  - `#ah` nur in Dungeon-Varianten (Flask of Oil für Deadmines) und bei Waffen für Krieger und Schamanen.
  - Serpentbloom nur mit Wailing Caverns (`.dungeon WC`).
  - Keine Überschneidung mit unseren Schritten.
- Unterschied v4.11.13 → v4.11.23 in den zwei Horde-Dateien: +463/−181 Zeilen aus 8 Commits (03.–10.10.), gemessen am 13.10. mit `git diff` im RXP-Klon.

---

## 6. Updates: was sie bedeuten und wie wir sie machen

- **Ein RXP-Update macht unseren Guide nicht kaputt.** Er ist eine eigene Datei und läuft weiter. Ihm fehlen nur die neuen Routen-Korrekturen, bis wir neu mischen.
- **Kaputt gehen kann er nur, wenn RXP die Syntax ändert.** Das zeigt die Prüfung gegen den neuen Code, und im Spiel das Testlog (Einträge `FEHLER`).
- **Ablauf:**
  1. Im Testlog steht bei jeder Sitzung die RXP-Version (`SITZUNG … RXP v4.11.xx`).
  2. Claude holt genau diesen Tag und mischt neu.
  3. Bericht an den Nutzer:
     - was sich in den gemischten Abschnitten geändert hat
     - welche Anker noch passen
     - was von Hand nachgebessert wurde
  4. Claude schreibt die Datei in den AddOns-Ordner (seit 15.10.; vorher bei verknüpften AddOns `aktualisieren.bat`), der Nutzer gibt `/reload` ein. Der Fortschritt bleibt, solange Gruppe und Name gleich sind; die Stelle kann sich aber verschieben (nächster Punkt).
- **Wie RXP die Stelle wiederfindet** (Code v4.11.23): Pro Guide speichert RXP die Schrittnummer und eine Schritt-Kennung aus der Zeilennummer im Guide-Text (`stepId = linenumber + guide.guideId`, `GuideLoader.lua` L1090). Beim Laden sucht es zuerst diese Kennung, sonst nimmt es die Nummer (`GuideWindow.lua` L1894–1901).
  - Gezählt werden nur nicht-leere Zeilen; Kommentarzeilen entfernt RXP vorher (`string.gmatch(text, "[^\n\r]+")`). Die Nummer zählt nur angezeigte Schritte (`ProcessGuideTable`, `IsStepShown`; z. B. fehlen `#hardcore`-Schritte).
  - Regel für Neubauten während eines Tests: neue Schritte nur **nach** der Stelle des Testcharakters einfügen. Dann bleiben Kennung und Nummer gleich (v0.2: Stelle «Well» #30, Zeile 339, unverändert).
  - Prüfen vor dem Merge: `python3 tools/rxp_schritte.py vergleich git:HEAD:addons/RXPGuides_KombiGuide/Kombi_Guide.lua addons/RXPGuides_KombiGuide/Kombi_Guide.lua "<Guide>" --stelle N --gruppe "<Gruppe>" --klasse <klasse>` (Exit 1, wenn sich ein Schritt bis N verschiebt). Text ändern bei gleicher Zeilenzahl ist erlaubt: RXP findet die Stelle über die Zeilennummer.
  - Seit 16.10. prüft das Werkzeug genau so, wie RXP lädt: Verschieben sich Zeilen vor N, ist es trotzdem in Ordnung, wenn die alte Zeile keinen gezeigten Schritt trifft und unter der Nummer N derselbe Schritt steht (RXP nimmt dann die Nummer, `GuideWindow.lua` `LoadGuide`). Damit gehen neue Schritte vor der Stelle eines Testcharakters, wenn er sie nicht sieht, z. B. mit `#maxlevel` unter seiner Stufe (`--stufe` angeben). Kombi-Guide 0.6 nutzt das in «12-17» (`#maxlevel 17` für den Stufe-18-Charakter, offene Entscheidung 37). Trifft die alte Zeile zufällig den Anfang eines anderen gezeigten Schritts, meldet das Werkzeug PROBLEM (16.10. beim Schamanen; eine zusätzliche Zeile im eingefügten Block verschob die Zeilen so, dass die alte Zeile keinen Schritt mehr trifft).
  - Stellen am 14.10.: Testcharakter Tauren-Druide in «6-12 Mulgore» #30 (Testlog 13.10. 22:50), zweiter Testcharakter (Stufe 15, Tauren, Klasse nicht im Testlog) in «12-17 The Barrens» #77 der Gruppe «Kombiguide (H)» (Testlog 13.10. 22:48). Für alle Tauren-Klassen liegt #77 spätestens bei Zeile 1742 (RXP-Zählung, `tools/rxp_schritte.py`); v0.3 fügt in «12-17» erst danach ein (geprüft für Druide, Jäger, Schamane, Krieger).
  - Stellen am 15.10. (`docs/tests/messdaten-2026-10-15.md`): Tauren-Druide in «6-12 Mulgore» #45 (Stufe 7, Testlog 14.10. 20:09; Zeile 510, `.accept 749`, in v0.3 und v0.4 gleich), zweiter Testcharakter in «12-17 The Barrens» #84 (Stufe 15, Testlog 15.10. 19:38, Kombiguide 0.4; Zeile 1799, `.xp 16`). Seine Schrittfolge #77 → #78 → #81 → #84 mit den Quests 901, 902 und 869 passt nur zur Druiden-Zählung (Jäger, Schamane und Krieger zählen dort anders); er ist also sehr wahrscheinlich ein Druide. Neue Schritte deshalb nur nach #45 bzw. #84, seit 15.10. 22:01 nach #152 (im Testlog bis 22:16 unverändert). Um 20:58 stand er bei #103 (Stufe 16, Orgrimmar-Teil vor «SpiritsPickup»), um 22:01 bei #152 (Stufe 18, nach dem Orgrimmar-Block, Crossroads und Ratchet).
  - Stellen am 17.10. (Abend, `docs/tests/messdaten-2026-10-17.md`): Tauren-Druide in «6-12 Mulgore» #153 (Stufe 12, Moonglade, Testlog 17:08; davor #116, #52, #45), Stufe-18-Charakter in «12-17 The Barrens» #152. Kombi-Guide 0.6.3 fügt in «6-12» vor #153 nur Schritte mit `#maxlevel 11` ein: Zeilen verschieben sich ab #19, RXP findet #153 über die Nummer (`tools/rxp_schritte.py vergleich … --stelle 153 --stufe 12`).
  - Neubau v0.4 → v0.4.1 (gleiche Schrittzahl, im Orgrimmar-Block mehr Zeilen): Ab dem Block verschieben sich die Zeilen um 1–5. RXP findet die alte Kennung dann meist nicht und nimmt die Nummer (gleicher Schritt). An 11 Stellen des Druiden in «12-17» (#141, #151, #154, #168, #172–#174, #187, #202, #206, #215) trifft die alte Kennung aber einen anderen Schritt, eine Nummer davor; RXP stünde dort einen Schritt zu früh (erledigte Schritte überspringt es selbst). Gezählt am 15.10. mit `tools/rxp_schritte.py`; im Spiel ungeprüft. Der Charakter stand bei #152, also nicht betroffen.
  - Ausweg für Schritte davor, ungeprüft im Spiel: `#maxlevel 14` blendet einen Schritt für Charaktere ab Stufe 15 aus, dann zählt er für deren Nummer nicht mit (`LevelCheck`, wird beim Laden des Guides geprüft).
  - Ändert ein Neubau nur Koordinaten (gleiche Zeilen, z. B. v0.1.1 → v0.1.2), bleibt die Stelle genau.
  - Ändert sich die Route (andere Zeilen, z. B. Neubau auf einer neueren RXP-Version), kann RXP an einer anderen Stelle stehen. Erledigte Schritte überspringt RXP selbst (Testlauf 2); liegt die Stelle zu weit vorne, hilft die Schrittliste. Im Spiel **ungeprüft** (Test T6).
  - Probebau auf dem RXP-Hauptzweig (14.10., 998caf30), verglichen mit dem Bau v0.4:
    - Die Zeilen verschieben sich vor beiden Stellen: «6-12» #30 von Zeile 339 nach 347, «12-17» #77 um 2–3 Zeilen, je nach Klasse.
    - Die alten Kennungen treffen im Neubau keinen anderen Schritt. RXP nimmt deshalb die Nummer.
    - Unter dieser Nummer steht derselbe Schritt: «Well» bzw. derselbe Inhalt bei #77, geprüft für alle 9 Klassen.
    - Ein Neubau auf dem nächsten Release dürfte die Stellen also halten, sofern RXP bis dahin vor den Stellen nichts mehr ändert. Im Spiel ungeprüft (T6).
  - Seit v0.5 (15.10.) steht jeder Guide-Name zweimal in `Kombi_Guide.lua` (zuerst «Kombiguide (H)», dann «Kombiguide Dungeon (H)»). `tools/rxp_schritte.py … --gruppe "<Gruppe>"` wählt die Gruppe; ohne `--gruppe` gilt die erste. Die Kennung hängt an Gruppe und Name (`guideId`) und an der Zeile im eigenen Guide-Text, die Gruppen stören sich also nicht. In «Kombiguide Dungeon (H)» steht noch kein Testcharakter (15.10.); sobald einer dort steht, gilt dieselbe Regel.
- **Wann aktualisieren?** Das entscheidet der Nutzer. Möglich sind:
  - (a) nur bei Bedarf, also wenn ein Routenfehler stört
  - (b) wöchentlich in der Beta
  - (c) vor dem Start einfrieren und zum Start einmal mit dem Start-Release neu mischen
- **Aufwand:** Mit Skript sind es Minuten. Von Hand wird es nur, wenn ein Anker wegfällt.

---

## 7. Hürden und Risiken

| # | Risiko | Folge | Gegenmittel |
|---|---|---|---|
| 1 | RXP ändert die Route fast täglich (31 Commits in 27 Tagen) | Unsere Kopie veraltet, Anker fallen weg | Mischen per Skript, Anker-Prüfung, Änderungsbericht |
| 2 | RXP ändert Befehle oder den Lader | Ladefehler | Prüfung gegen aktuellen RXP-Code; Testlog `FEHLER` |
| 3 | Gekaufter Guide weicht in 1–22 von der Gratis-Route ab | Kleine Unterschiede zur gewohnten Route | Im Test vergleichen |
| 4 | Interface-Nummer ändert sich (heute 16001) | Addon «veraltet» | `.toc` anpassen; «Veraltete AddOns laden» |
| 5 | Ordner zum Start anders als `_classic_beta_` | Addons am falschen Ort | Zum Start prüfen (offen seit 07.10.) |
| 6 | Beta ≠ Live (Drops, Rezepte, Lehrer) | Mengen und Orte stimmen nicht | Testlog misst; zum Start nachprüfen |
| 7 | Quellen widersprechen sich (21 Punkte, Abschnitt 9) | Falsche Koordinate oder Stufe | Im Spiel prüfen, Befund ins Testlog |
| 8 | Einschub zerreisst `#completewith next` | Schritt hängt | Skript-Regel; Test T3 |
| 9 | Zwei ähnliche Guides in der Liste, RXP wählt beim neuen Charakter seinen eigenen | Falscher Guide aktiv | Einmal von Hand wählen; `#defaultfor` bei uns entfernt |
| 10 | `#next` in den gekauften Guide greift nicht | Bei 22 kein automatischer Wechsel | Von Hand wählen; Test T5 |
| 11 | Deutscher Client | Eigene Texte gemischt mit englischen Ortsnamen | Eigene Texte ohne ungeprüfte Eigennamen; Quest- und NPC-Namen kommen von RXP/Client |
| 12 | Lizenz CC BY-NC-SA 4.0 | Nur nicht-kommerziell, mit Herkunft, gleiche Lizenz | Hinweis in jeder Datei; nie verkaufen oder kommerziell verteilen |
| 13 | «Secret values» im modernen Client (Forever nutzt die Mainline-Vorlagen) | Chat-Text kann für Addons gesperrt sein (`CHAT_MSG_LOOT` ist nicht «NeverSecret») | Testlog zählt über Taschenbestand statt Chat; Abfrage `issecretvalue`. Zauber-Ereignisse wie `UNIT_SPELLCAST_SUCCEEDED` sind laut Forever-API nur für fremde Einheiten «secret», nicht für den Spieler und seinen Begleiter; einzelne Zauber können abweichen (`SecretPredicatesDocumentation.lua`, `SecretWhenUnitSpellCastRestricted`) |
| 14 | Leder pro Stunde unbekannt | Farmmengen pro Gebiet nur geschätzt | Testlog 3: `SAMMELN` (Quelle mit Kreatur- oder Objekt-ID und Beute), `BEUTE`, `ANGELN` mit Ort und Zeit auswerten |
| 15 | Platz für 400–650 Leder | Taschen voll (17.10.: auf Stufe 8 voll, Notiz im Testlog; darin 27 Leichtes Leder, 36 Fetzen, Kräuter, Fleisch); Leder beim Bankchar zählen die RXP-Zähler nicht (§4) | Leinentaschen (der Bankchar lernt dafür Schneiderei, Entscheid 17.10.), Bankchar (am 17.10. 27 Leichtes Leder und 36 Fetzen per Post, Porto 2s 70c), Apprentice's Skinning Satchel (Abschnitt 8); Überblick über alle Charaktere: Bagnon (§8) und `/tl tipp` (Stufe A mit dem Bankchar, seit 17.10.); zum Herstellen in Orgrimmar muss das Material wieder in den Taschen sein (`.itemcount`) |
| 16 | Kiste «40 Linen Cloth» lässt sich nicht füllen (Stapel 20) | Merchant's Favor fehlt | Variante 20 Leichtes Leder nutzen (allthings.how, Mobalytics) |
| 17 | RXPs Kommentar-Koordinaten (`--c:Zone,x,y`) passen nicht überall zur Forever-Karte. Mulgore ist in Forever 6154 × 4102 Yards gross; 442 RXP-Punkte (gezählt auf v4.11.13) weichen im Median 3,5 % ab, höchstens 11,3 %; auf v4.11.23 sind es 456 Punkte, Median 3,48 %, höchstens 11,34 % (Prüfbericht 15.10.). Thunder Bluff (26 Punkte) und Brachland (18 Punkte) passen genau (Messung 13.10., `docs/tests/messdaten-2026-10-13.md`) | Eigene Pfeile lagen bis 35 Yards daneben (v0.1) | Spielkoordinaten plus Kartenecken (`forever_karten.csv`); exakte Ecken aus Testlog-Eintrag `KARTE` (`C_Map.GetWorldPosFromMapPos`, `C_Map.GetMapWorldSize`, beide in der Forever-API 1.60.1), übernommen mit `tools/karte_aus_testlog.py`. Exakt: 1412 Mulgore, 1413 Brachland, 1454 Orgrimmar, 1456 Thunder Bluff; in Orgrimmar passen RXPs Kommentare genau (14 Punkte). Seit 15.10. auch 1411 Durotar (RXPs Kommentare genau, 32 Punkte), 1414 Kalimdor, 1415 Östliche Königreiche, 1420 Tirisfal, 1421 Silberwald, 1458 Undercity, seit 17.10. 1450 Moonglade (RXPs Kommentare genau, 9 Punkte) |
| 19 | CLOSED-Ereignisse kommen nicht immer: Am 13.10. blieb eine Post-Sitzung von etwa 22:26 bis zum Ausloggen offen (MAIL_SHOW ja, MAIL_CLOSED nein). Von fünf Post-Sitzungen an diesem Abend endeten vier erst beim Ausloggen (Testlauf 3, Nr. 15). Das Forever-UI öffnet und schliesst diese Fenster über den Interaktions-Manager (`PLAYER_INTERACTION_MANAGER_FRAME_SHOW`/`_HIDE`, `PlayerInteractionFrameManager.lua`, UI 1.60.1) | Beute, Quest-Abgaben und Geld landen in der falschen Zeile (POST statt BEUTE, TASCHE, GELD); Lehrer- und Flugkosten könnten falsch zugeordnet werden | Testlog 3.2: Ende auch über die Interaktions-Ereignisse, über die Prüfung «Blizzard-Fenster sichtbar oder Interaktion läuft» (`C_PlayerInteractionManager.IsInteractingWithNpcOfType`), bei mehr als 25 Yards Abstand, Gebietswechsel und Ladebildschirm; jede Zeile nennt Dauer und Grund |
| 20 | AH-Angebot zum Start dünn oder teuer (Medium Hide, Mittleres Leder in Hunderten, Leichtes Leder) | Stufen B–D teurer oder nicht machbar; Beta-Preise taugen nur als Grössenordnung | Stufen nach Gold staffeln (Guide v0.4); `tools/plan_berufe.py` zum Start mit EU-Preisen neu rechnen (offene Entscheidung 4) |
| 21 | Lernstufen der VZ-Rezepte widersprechen sich (AHledger gegen wow-professions, Widerspruch 17) | Schritt VZ 20–50 lässt sich vielleicht nicht wie geplant machen | Guide nennt den Ausweg (Bracer bis 25, Minor Wizard Oil bis 30); Befund mit `/tl` notieren, dann neu bauen. Seit Testlog 3.4: Lehrerliste (LEHRER) zeigt die Lernstufen direkt (Messplan M1). Gemessen 15.10. (Lehrerlisten Orgrimmar): Chest - Inferior Stamina ab 15, Chest - Minor Absorption ab 40, Minor Deflect nicht im Angebot; Kombi-Guide v0.5.1 nimmt Minor Absorption |
| 22 | AHledger-Preise widersprechen sich innerhalb weniger Tage, je nach Seite: Light Hide 69c (Item-Seite 09.10.) gegen etwa 3s (aus den Reagenzienkosten der Rezeptseite Cured Light Hide, 14.10.); Heavy Leather 11s 98c (08.10.), 9s 40c (12.10.), etwa 7s 20c (Rezeptseite 14.10.) | Die Rangfolge der Optionen im Berufe-Plan kann kippen (Heavy Leather in Stufe C zeigt Gewinn, die Rezeptseite Verlust, `docs/recherche/2026-10-14_goldquellen.md` §1) | Beta-Preise nur als Grössenordnung; Preisregeln (berufe-plan §6) statt fester Wahl; zum Start mit den Preisen des eigenen Realms neu rechnen (offene Entscheidung 4) |
| 23 | AH-Scan (Testlog 3.5) im Spiel ungeprüft: Index ab 0 oder 1, Sofortkaufpreis für das ganze Angebot, wie lange der Server zwischen zwei Scans sperrt (die Dauer ist gemessen: 17–18 s, Scans vom 15.10.). AHledger nennt nur seinen eigenen Abstand («never runs more than once per 15 minutes»; der Knopf zählt herunter, bis der Server wieder einen Scan erlaubt; https://www.curseforge.com/wow/addons/ahledger, Stand 12.10.). Dieselbe Seite sagt, der Beta-Client schreibe SavedVariables, lese sie aber nicht zurück; ebenso das Addon ForeverSVBridge («the client writes addon saved variables at logout but does not read them back at login», https://www.curseforge.com/wow/addons/foreversvbridge, Stand 24.09.). Am 13.10. sprach alles dagegen: Einträge vor und nach `/reload` und über drei Charaktere in einer Datei (`docs/tests/messdaten-2026-10-13.md`, `testlauf-3.md` Nr. 15), und nach dem Neustart des Spiels um 22:07 fand RXP seine gespeicherte Stelle wieder (`testlauf-3.md` Nr. 2). Geschrieben wird beim Ausloggen und bei `/reload` (https://warcraft.wiki.gg/wiki/Saving_variables_between_game_sessions) | Falsche Preise pro Stück; zu wenige Scans für Wochenpreise; Datei wird gross; Scan wird übersprungen, weil der letzte (auch eines anderen Charakters) weniger als 15 Minuten her ist | Index erkennt das Testlog selbst, Preis pro Stück im Spiel einmal vergleichen (T15); `tools/ah_aus_testlog.py` übernimmt jeden Scan ins Repo, die Wochenpreise hängen also nicht an der Datei; die Datei behält höchstens 60 Scans, nur die 10 neuesten mit allen Gegenständen; ein übersprungener Scan meldet sich im Chat (sofort: `/tl ah`); unvollständige Scans (über 10 % ohne Daten) und dünne Angebote (unter 50 Stück) kommen nicht in den Plan. Erster Scan im Spiel am 15.10. um 20:12 (Testlog 3.5, Orgrimmar): 65 411 Angebote, 3079 Gegenstände, 18 s, kein Angebot ohne Daten, keine geheimen Werte; die Region gibt der Beta-Client als leeren Text zurück (`GetCurrentRegionName`), seither als «?» gespeichert (`docs/tests/messdaten-2026-10-15.md`) |
| 24 | Testlog 3.6 im Spiel ungeprüft: ob `GetInboxInvoiceInfo` Preis und Gebühr auch für ungeöffnete Briefe liefert (das Forever-UI ruft vorher `GetInboxText` auf, `MailFrame.lua`; das Testlog nicht, weil das den Brief als gelesen markiert); ob die Betreff-Texte des Clients (`AUCTION_SOLD_MAIL_SUBJECT` usw.) in Forever bestehen; ob `GetReplicateItemTimeLeft` die Restlaufzeit als 0–3 (wie `Enum.AuctionHouseTimeLeftBand`) oder als 1–4 (wie die alte `GetAuctionItemTimeLeft`) liefert, die Doku sagt nur «number» (gemessen 15.10.: 1–4, siehe Ende der Zeile). `AUCTION_HOUSE_AUCTION_CREATED` nutzt das Forever-UI selbst (Meldung `ERR_AUCTION_STARTED`, `Blizzard_AuctionHouseFrame.lua`), ebenso `AUCTION_HOUSE_POST_WARNING` für das Bestätigungsfenster. `GetAllRecipeIDs` steht weder in der Doku noch im Forever-UI (`GetFilteredRecipeIDs` fehlt in der Doku auch, das UI nutzt es); das Testlog versucht `GetAllRecipeIDs` zuerst und nimmt sonst `GetFilteredRecipeIDs`. Die Abnahme ist eine Schätzung: Ein Scan zeigt Angebote, keine Käufe; wer zurückzieht und teurer neu einstellt, sieht aus wie ein Kauf | AH-POST nur mit Art und Menge aus dem Betreff; Abnahme zu hoch oder zu tief; Empfehlungen zu optimistisch | Rückfall auf die Betreffzeile, die Rechnung wird nachgetragen, sobald sie lesbar ist; ein abgeholter Brief zählt nicht mehr beim Wiederfinden (gleicher Brief danach = neuer Verkauf); die Restlaufzeit-Zählung erkennt das Testlog am Wert 0 oder 4 (sonst keine Abnahme); die Abnahme zählt nur Angebote, die bis zum nächsten Scan nicht ablaufen konnten (Bänder laut `GetTimeLeftBandInfo`), von unten bis zur ersten Preisstufe, auf der noch etwas liegt, abzüglich neuer Angebote bis zu diesem Preis; ganz verschwundene Gegenstände zählen nicht; Beleg erst ab 2 Vergleichen über 1 Stunde, Mengen nie hochgerechnet; Tests T16–T20. Gemessen 15.10. 22:15: `GetReplicateItemTimeLeft` liefert 1 bis 4 (`bandRoh` 1-4, Versatz -1); Bänder 30 Minuten, 2, 12 und 24 Stunden. Erste Abnahme aus Scan-Paaren am 17.10. (61 und 25 Minuten, `data/preise/ah_abnahme.csv`); ein echter Verkauf (Schattenedelstein des Bankchars, AH-POST 15:15) steht in keiner der beiden Schätzungen, die Abnahme kann also auch zu tief liegen. Am 17.10. fehlte AH-POST für einen Brief, der nach 2 s abgeholt war (das Testlog liest 1 s nach `MAIL_INBOX_UPDATE`) |
| 25 | RXPs Dungeon-Route für Forever ist «WIP» (Untergruppe «(WIP) Dungeon Guide 1-22», `#beta`), und RXP lässt in Forever keine Dungeons zu (§4). Der Hauptzweig baut die Route um (andere Namen, 13-20 und 20-24 fallen weg; §2) | RXP selbst hat die Route in Forever kaum mit Dungeons laufen lassen können; Fehler in Dungeon-Schritten; die fest eingebauten Dungeons lassen sich im Spiel nicht abschalten; Leder-Ziele passen vielleicht nicht zur Route | Auswahl in `data/kombi/dungeons.csv` ändern und neu bauen; Befunde mit `/tl bug`; die Speedrun-Gruppe bleibt als Ausweg; beim nächsten Release Anker und Namen neu prüfen; Mengenmodell für die Dungeon-Route erst nach Entscheid (offene Entscheidung 24); T22 |
| 26 | Händlerpreise hergestellter Teile: Der Forever-Händler zahlt für viele hergestellte Teile weniger als in Classic (19 von 91 verglichenen Gegenständen anders, z. B. Grosser Magiezauberstab 2s statt 15s 35c, Geprägte Lederhandschuhe 71c statt 1s 19c; Leichte Lederhose 5s 99c und Dunkler Ledergürtel 7s 3c wie in Classic; `docs/recherche/2026-10-15_haendlerpreise.md`). Eine Patch-Notiz vom 01.10. nannte für Zauberstäbe 1c (Widerspruch 21) | Zum Start können Verkäufe an den Händler (Stufe C) und die Variante Zauberstäbe weniger bringen; Classic-Datenbanken nennen zu hohe Händlerpreise | Nur Händlerpreise aus dem Forever-Client verwenden (Gegenstands-Infos ab Testlog 3.6, AH-Scan ab 3.7, `data/preise/haendler_ankauf.csv`); Preisregeln (berufe-plan §6); zum Start neu messen |
| 27 | Testlog 3.7 im Spiel ungeprüft: Reihenfolge von `PLAYER_XP_UPDATE` und `QUEST_TURNED_IN` (die Quelle wird deshalb 1 s später bestimmt); Kreatur beim Kill aus dem toten Ziel oder dem letzten Ziel der letzten 10 s (Kills ohne Ziel, z. B. durch Schaden über Zeit nach einem Zielwechsel, kommen auf eine falsche oder «?»-Kreatur); Instanz über `IsInInstance` («party», «raid», «scenario»); `UnitGUID("target")` kann laut Doku «secret» sein (SecretWhenUnitIdentityRestricted); Dateigrösse durch den Laufweg | XP falsch zugeordnet; Laufweg-Lücken; grössere SavedVariables (höchstens 30 000 Proben pro Charakter, etwa 1 MB) | «Gegner» nur im Kampf oder bis 5 s danach, sonst «sonst»; geheime Werte werden übersprungen; Obergrenze der Proben; Tests T23–T26. Dazu 3.7.1 (16.10.): Warnung beim Händler, Hinweis für das Scan-Paar (`IsResting`), Datenanfrage (`C_Item.RequestLoadItemDataByID`, laut Doku «SecretArguments = AllowedWhenUntainted»), Berufe und Geld pro Charakter; im Spiel ungeprüft (T29–T33) |
| 28 | RXPs Lehrer-Automatik bei `.train`-Schritten (§4): kauft bei offenem Lehrerfenster den ersten verfügbaren Eintrag mit passendem Namen oder passender Fertigkeitslinie. Betrifft die Lern-Schritte (Aktion `lernen`: Kürschnerei, Kräuterkunde, Lederverarbeitung, Verzauberkunst als Lehrling); RXPs eigene Forever-Guides nutzen dasselbe (`.train 7411 >> Train Enchanting`) | Vielleicht ein Rezept mitgekauft (50c bis 1s 50c bei den Lehrlings-Rezepten in Orgrimmar, `lehrer.csv`), ungeprüft | Gesellen-Schritte ohne `.train` (seit v0.5.3); beim Druiden in Orgrimmar die Zeilen GELERNT und GELD beim Lehrer prüfen (Messplan); notfalls in RXP «Trainer automation» ausschalten |
| 29 | Gold reicht nicht für die Klassenzauber: Der Druide hatte am 17.10. vor dem Lehrer der Stufe 10 4s 63c, die vier Zauber kosteten 12s; der Bankchar schickte 1g (Notiz des Nutzers: «muss in der scharfen Version einbezogen werden»). Am ganzen Tag (Stufe 7,74 → 12,16) gewann der Druide ohne dieses Gold etwa 18s; die Klassenzauber kosten von Stufe 10 bis 16 zusammen 1g 17s, bis 22 5g 7s (Lehrerliste, §9) | Zum Start hat der Main keinen Bankchar mit Gold; Zauber oder Berufsschritte fallen aus, oder der Einkauf in Orgrimmar reicht nicht | `tools/markt.py` zählt die offenen Klassenzauber beim Gold für Orgrimmar mit (seit 17.10.); Erinnerung im Guide vor dem Lehrer offen (offene Entscheidung 41); Beute mit hohem AH-Wert verkaufen statt beim Händler (Abnahme gemessen, §9) |

---

## 8. Möglichkeiten

- **Essen gibt +5 % XP aus Kills für 15 Minuten**, schon bei einfachen Rezepten (Icy Veins 15.09., Mobalytics 09.10.). Fleisch fällt auf der Route ohnehin: Kodo Meat, Stringy Wolf Meat, Strider Meat, Thunder Lizard Tail.
- **Lager-Gegenstände ab Stufe 20 des jeweiligen Berufs** (wow-professions, Camping Guide):

| Gegenstand | Beruf | Material | Wirkung |
|---|---|---|---|
| Camp Chair | Kürschnerei 20 | 3 Leichtes Leder, 2 Simple Wood | +2 % Krit, stapelt nicht mit Moonkin Aura |
| Camp Tent | LW 20 | 5 Leichtes Leder | erholte XP im Wert von 5 % einer Stufe, nur wenn keine gespeichert sind |
| Enchanted Lute | VZ 20 | 1 Simple Wood, 1 Strange Dust | stapelt nicht mit Mal der Wildnis |
| Incense Candle | Kräuterkunde 20 | 1 Peacebloom, 1 Silverleaf | Intelligenz, nicht mit Arcane Intellect |
| Fish Bowl | Fischen 20 | 1 Raw Brilliant Smallfish, 1 Empty Vial | +8 % alle Werte, nicht mit Blessing of Kings |

  Regeln: 1 Minute am Feuer sitzen gibt 1 Stunde Camp Benefits. Pro Spieler ein Gegenstand. Alle teilen sich 1 Stunde Abklingzeit.

  Gemessen 17.10. (Testlog): Fischglas (Rezept 1229745 aus «Grundlagen des Zeltens: Angeln») ist bei Angeln 25 grau, der Lagerstuhl (1229517) schon bei Kürschnerei 36; beide geben keinen Punkt; Leere Phiolen gab es in Bloodhoof für 4c (45.5, 61.8). Das Einfache Lagerfeuer (Kochkunst, 1229737) macht aus 1 Einfaches Holz ein «Einfaches Lagerfeuerset» (279981); daran kochte der Druide in Moonglade 16 Verkohltes Wolfsfleisch, jedes +1 (Kochkunst 16 → 32).
- **Gewächshaus (Greenhouse), Lager-Gegenstand der Kräuterkunde** (Details und Quellen: `docs/recherche/2026-10-13_kraeuter-fische-kochen.md`, Abschnitt 2):
  - Bauplan: Boss Shadetooth im Dungeon «Excavation Site: Wetlands», laut Icy Veins für Stufe 26–33 (03.10.); bei wowtbc haben die Quests Stufe 24.
  - Platzieren braucht Kräuterkunde 140 (Icy Veins, 11.10.). Material: 2 Simple Wood, 1 Arthas' Tears, 1 Purple Lotus (Mobalytics, AHledger); beide Kräuter sammelt man erst ab Kräuterkunde 210 bzw. 220.
  - Ein Samen pro Gewächshaus: Das Kraut ist nach 8 Minuten erntbar, das Gewächshaus hält 15 Minuten (Icy Veins, 08.10.).
  - Samen: Commonplace (Peacebloom, Earthroot), Uncommon (Silverleaf, Kingsblood), Scarce (Ghost Shroom); Kräuterkundige finden Samen beim Sammeln.
  - Für den Plan (Kräuterkunde bis etwa Stufe 15) fallen nur die Samen an; ihr AH-Wert steht in der Recherche.
  - **Ungeprüft:** ob Pflanzen und Ernten Kräuterkunde brauchen, wie viele Kräuter eine Ernte gibt.
- **Tauren-Rasse «Cultivation»:** dupliziert ein Kraut, das man ohne Kräuterkunde ernten kann. Abklingzeit 15 Minuten laut Warcraft Tavern (https://www.warcrafttavern.com/forever/guides/tauren-racials/, abgerufen 17.10.; bis 17.10. stand hier 1 Stunde, aus Warcraft Tavern und SeeMeta vom 10.10.; SeeMeta nennt am 17.10. keine Abklingzeit); gemessen 17.10.: zwei Ernten «Grüner Daumen» mit eigenen Objekt-IDs 15 Minuten auseinander, vermutlich das Duplikat dieser Fähigkeit (`docs/tests/messdaten-2026-10-17.md`). Nötige Stufe = Kraut-Stufe / 5 (Warcraft Tavern). Damit gibt es Kräuter auch nach dem Verlernen.
- **Merchant's Favor:**
  - Die erste Shipping-Label-Quest gibt 50.
  - Kisten droppen ab Stufe 10. «Apprentice Textiles» fällt zum Beispiel bei Stormsnout in 9 % von 23 Beute-Fenstern (AHledger).
  - Bündel: 20 Leichtes Leder ergeben 5 Favor. 2 Cured Light Hide ergeben 10 (Apprentice Fabrics). Cured Light Hide stellt LW auf Stufe 30–55 ohnehin her.
- **Taschen über alle Charaktere:** Bagnon (Forever-Datei 12.1.7 vom 15.10., «Updated for WoW Forever!» seit 12.1.2, https://www.curseforge.com/wow/addons/bagnon) speichert über BagBrother (`BrotherBags`) pro Charakter Taschen, Ausrüstung, Geld, Briefkasten, Bank beim Schliessen und Briefe an eigene Charaktere gleich beim Senden, wenn es den Empfänger schon kennt; der Tooltip zeigt die Anzahl pro Charakter (Code der installierten Version, `core/features/caching.lua` und `itemTooltips.lua`, gelesen 17.10.). Ebenfalls mit Forever-Datei: Baganator mit Syndicator (13.10., https://www.curseforge.com/wow/addons/baganator, https://www.curseforge.com/wow/addons/syndicator), BagSync (29.09., https://www.curseforge.com/wow/addons/bagsync). Beim Nutzer seit 17.10. 15:16 installiert, im Spiel noch nicht geladen (Messdaten 17.10.). Die RXP-Zähler bleiben beim eingeloggten Charakter (§4).
- **Apprentice's Skinning Satchel:** 4 Plätze, Taschentyp Leatherworking Bag, 25c. Gibt es bei Kuruk und Shadi Mistrunner in Thunder Bluff und bei Kawnie Softbreeze in Camp Narache (AHledger, 13.10.).
- **Testlog-Daten** ergeben Leder und XP pro Stunde je Gebiet. Daraus werden die Farmmengen pro Gebiet.

---

## 9. Berufsdaten für Mulgore und Brachland

Tags: [Forever] = Quelle zu Forever, [Classic] = Classic-Daten. **Ungeprüft** heisst: keine Quelle gefunden.

**Lehrer (Horde)**

| Beruf | Wer, wo | Koordinaten | Quelle |
|---|---|---|---|
| Kürschnerei | Nawka Wildsong, Camp Narache (bis 75) | 44.6 76.8 (Icy Veins) / 44.4, 76.8 (kami-labs) | [Forever] |
| Kürschnerei | Yonn Deepcut, Bloodhoof, Great Tent | **Widerspruch:** 45.6 57.8 / 45.0, 61.4; gemessen 45.0, 61.5 (Standort bei der Abgabe von 97936, Testlog 14.10.; Abgabe laut warcraft.wiki.gg bei Yonn Deepcut, der Name steht nicht im Testlog) | [Forever] |
| Kürschnerei | Mooranta, Thunder Bluff | 44.43, 43.19 (RXP) | [Forever] |
| Kräuterkunde | Garan Sunstrider, Camp Narache (bis 75) | 44.2 77.8 | [Forever] |
| Kräuterkunde | Komin Winterhoof, Thunder Bluff | 49.8 39.8 | [Forever] |
| LW | Chaw Stronghide, Bloodhoof (Apprentice) | 45.0 61.4 | [Forever] |
| LW | Mak / Tarn / Una, Thunder Bluff (Apprentice/Journeyman/Expert) | 42.2 43.2 / 42.4 43.0 / 41.4 42.6 | [Forever] |
| LW | Krulmoo Fullmoon, Camp Taurajo (Journeyman) | 44.8 59.4 | [Forever] |
| VZ | Mot / Teg Dawnstrider, Thunder Bluff (Apprentice/Journeyman) | 45.0 38.4 / 45.0 38.0 | [Forever] |
| VZ | Hgarth, Sun Rock Retreat (Expert) | 49.2 57.2 | [Forever] |
| Fischen | Uthan Stillwater, Stonebull Lake | 44.6 60.6; **gemessen 44.2, 63.8** (Testlog 13.10., Standort beim Lernen; rund 130 Yards südlicher; dieselbe Stelle bei der Abgabe von 97932 am 17.10.) | [Forever] |
| Fischen | Kah Mistrunner, Thunder Bluff | 56.0 46.8 / 56.13, 46.39 (RXP) | [Forever] |
| Kochen | Pyall Silentstride, Bloodhoof, Great Tent | 45.0 61.6; gemessen 44.9, 61.7 (Testlog 13.10.; gleich wie RXPs Weltkoordinaten) | [Forever] |
| Kochen | Aska Mistrunner, Thunder Bluff | 51.0 52.8 | [Forever] |
| Kochen | Duhng, bei den Crossroads | 55.2 31.8 | [Forever] |

Quellen: wow-professions (Trainer-Seiten Skinning, Herbalism, LW, VZ, Fishing, Cooking), Icy Veins (Seiten zu den Berufen, 29.09.–11.10.), kami-labs (08.10.), RXP-Mulgore-Guide.

**Rang-Grenzen**
- LW und VZ: Journeyman ab Fertigkeit 50 und Stufe 10; Expert ab 125 und Stufe 20, kostet 50s; Artisan ab 200 und Stufe 35 [Forever, wow-professions].
- Gemessen 15.10. (Lehrerlisten in Orgrimmar, `data/kombi/lehrer.csv`): Geselle Lederverarbeitung (Karolek) und Verzauberkunst (Godan) je ab Stufe 10 und Fertigkeit 50, 5s; Lehrling 10c. Einen Experten führen beide nicht.
- Der Geselle (Journeyman) hebt das Maximum auf 150; den Experten braucht man erst für mehr als 150 [Forever: wow-professions Enchanting Leveling Guide «Journeyman (70-150)», «Expert (150-225)»; kami-labs Leatherworking: «Your limit then rises to 150», Expert «learn it before continuing past 150»; abgerufen 14.10.]. Lederverarbeitung 150 und Verzauberkunst 150 gehen also ab Stufe 10, ohne Stufe 20.
- Kürschnerei: laut wow-professions ohne Stufen-Voraussetzung (50/125/200). **Widerspruch:** RankedBoost nennt 75/150/225. Gemessen 17.10. (Lehrerlisten Yonn Deepcut, Bloodhoof, und Mooranta, Thunder Bluff): Geselle ab Kürschnerei 50, ohne Stufe, 5s; passt zu wow-professions. Gelernt bei Mooranta am 17.10. um 14:37 (5s, danach Maximum 150).
- Kräuterkunde: laut wow-professions ohne Stufen-Voraussetzung. **Widerspruch:** Icy Veins nennt Stufe 10/20/35.
- Fischen: Journeyman ab 50 und Stufe 10. Expert ab 125 und Stufe 20, über ein Buch von Old Man Heming in Booty Bay [Forever, Icy Veins].
- Kochen: Journeyman ab 50. Expert ab 125, über das Expert Cookbook von Wulan (Desolace) [Forever].

**Kürschnern** [Classic, wowpedia / warcraft.wiki.gg]
- Nötige Fertigkeit: für Gegner der Stufe 1–10 genügt 1; Stufe 11–20: 10 × Stufe − 100; ab Stufe 21: 5 × Stufe. Icy Veins bestätigt «5 × Stufe ab 20» [Forever].
- Material nach Gegnerstufe: Ruined Leather Scraps 5–17, Light Leather 5–27, Light Hide 9–25, Medium Leather 15–38, Medium Hide 20–35. **Widerspruch** zur Untergrenze von Light Leather: GoldGoblin nennt 1.
- Anteile beim Kürschnern laut MetaForge (enthält VMaNGOS-Daten, also vermutlich Vanilla):
  - Kodo Calf (7–8): 60 % Schrott, 40 % Leichtes Leder
  - Zhevra Runner (13–14): 35 % Schrott, 60 % Leichtes Leder, 5 % Light Hide
  - Zhevra Charger (17–18): 74 % Leichtes Leder, 20 % Medium Leather, 2 % Medium Hide
- **Messung Forever** (Testlog 13.10., Mulgore, Charakter Stufe 6–7, 21 Häute, jede Haut 1 Gegenstand und +1 Punkt): Prairie Wolf (2958) 4 Leichtes Leder und 10 Fetzen von 14; Adult Plainstrider (2956) 3 und 1 von 4; Flatland Cougar (3035) 1 und 1; Prairie Stalker (2959) 0 und 1. Zusammen 8 Leder, 13 Fetzen; hochgerechnet etwa 40 Leder pro Stunde neben Quest 748 (kleine Stichprobe). Namen zu den IDs: AHledger, Seite Mulgore. Details: `docs/tests/testlauf-3.md`. Dazu 14.10. (Stufe 7, Kürschnerei 22 → 25, je Haut +1): Prairie Wolf 2× je 1 Fetzen, Adult Plainstrider 1 Leichtes Leder (`docs/tests/messdaten-2026-10-15.md`). Dazu 17.10. (Stufe 7–9, Kürschnerei 25 → 56, 39 Häute in etwa 27 Minuten, 31 Punkte): Prairie Stalker (2959) 9 Leichtes Leder und 8 Fetzen von 17, Flatland Cougar (3035) 6 und 8 von 14, Prairie Wolf (2958) 3 und 3 von 6, Adult Plainstrider (2956) 0 und 2 von 2; zusammen 18 Leichtes Leder und 21 Fetzen, etwa 40 Leichtes Leder pro Stunde (`docs/tests/messdaten-2026-10-17.md`).
- Tiere auf der RXP-Route:
  - Mulgore: Plainstrider, Battleboar, Prairie Wolf, Swoop, Flatland Cougar, Prairie Stalker, Elder Plainstrider, Prairie Wolf Alpha, Taloned Swoop, Flatland Prowler
  - Brachland: Plainstrider-Arten, Zhevra, Sunscale-Raptoren, Savannah-Katzen, Stormsnout, Thunderhead, Oasis Snapjaw
- Stufen [Classic, Wowhead]:
  - Mulgore: Plainstrider 1–2, Prairie Wolf 5–6, Prairie Stalker 7–8, Swoop 7–9, Prairie Wolf Alpha 9–10
  - Brachland: Greater Plainstrider 11–12, Zhevra Runner 13–14, Savannah Prowler 14–15, Sunscale Scytheclaw 16–18, Stormsnout 18–19, Thunderhead 20–21
- Ob Oasis Snapjaw kürschnerbar ist, ist offen. Die Beute bei AHledger enthält Leichtes Leder, sie ist aber nicht als Kürschnerei markiert. Wowhead (Classic) nennt Schildkröten unter den Lederquellen im Brachland.
- Weitere Stufen [Classic]: Sunscale Lashtail 11–13, Sunscale Screecher 13–15, Sunscale Scytheclaw 16–18, Savannah Highmane 12–13, Savannah Prowler 14–15, Savannah Patriarch 15–16, Oasis Snapjaw 15–16, Ishamuhale 19 (Warcraft Tavern, Hunter-Pets-Seiten); Ornery Plainstrider 17, Savannah Matriarch 18, Zhevra Charger 18, Echeyakee 16, Thunderhawk Hatchling 20, Thunderhawk Cloudscraper 22, Ashenvale Bear 22, Shadowhorn Stag 23 (MetaForge, Seite «Medium Hide», VMaNGOS-Daten). Kreatur-IDs aus den Links der AHledger-Seite «The Barrens»: Greater Plainstrider 3244, Ornery Plainstrider 3245, Zhevra Runner 3242, Sunscale Screecher 3255, Sunscale Scytheclaw 3256, Savannah Prowler 3425, Savannah Patriarch 3241, Savannah Matriarch 3416, Stormsnout 3240, Thunderhead 3239 (Fleeting Plainstrider 3246 nur erschlossen).
- Wowhead, «Classic Leather Farming: Early Leather» (RenataKane, Stand 09.06.2021, Patch 1.15.2) [Classic]: Leichtes Leder ab Gegnerstufe 6, am besten 11–20; Mittleres Leder ab 16, am besten 21–30; Bälge meist mit dem passenden Leder, etwa 3–5 %; ab Stufe 11 bis zu 2 Leichtes Leder pro Haut; im Brachland nördlich von Camp Taurajo eher Leichtes, südlich eher Mittleres Leder. https://cn.classic.wowhead.com/guides/classic-leather-farming-early-leather
- Medium Hide kürschnert man laut MetaForge ab Gegnerstufe 16 (z. B. Echeyakee, Zhevra Charger, Sunscale Scytheclaw, Savannah Matriarch, Stormsnout).

**Kräuter** [Forever, Icy Veins 11.10.]
- Peacebloom 1, Silverleaf 1, Earthroot 15, Mageroyal 50, Briarthorn 70, Stranglekelp 85, Bruiseweed 100, Wild Steelbloom 115.
- **Widerspruch** bei Bruiseweed: warcraft.wiki.gg nennt 85.
- Neu in Forever: Frilled Lichen als seltener Zusatz, unter anderem aus Briarthorn im südlichen Brachland (16 % von 51 Beute-Fenstern, AHledger).
- Frilled Lichen, Stand 14.10. (Details und Quellen: `docs/recherche/2026-10-14_goldquellen.md` §2):
  - Median NH 82s 80c (30 Tage 49s 34c), PH 2g 15s (79s 29c); Scan 14.10.
  - Weitere Quellen laut AHledger: Earthroot in Durotar 15 % von 39, Kingsblood in Duskwood 15 % von 20; im Brachland auch aus Earthroot und Mageroyal.
  - 16 % von 51 sind etwa 8 Funde, das 95-%-Intervall reicht von 8 % bis 28 %.
  - Gefunden am 17.10. in Mulgore: 3 Gekräuselte Flechten (249399) aus 3 Erdwurzel-Knoten (13:14 bei Kräuterkunde 16, 14:25 und 14:34 bei 21 bis 24; kleine Stichprobe). Am Nachmittag in Thunder Bluff zu 2g 75s angeboten; der Tiefstpreis fiel bis 15:02 auf 2g 50s, das Angebot stieg von 193 auf 236 Stück, in 1,4 Stunden kein Kauf geschätzt. Eigener AH-Scan 17.10. 13:36: Tiefstpreis 2g 75s, Median 3g 24s, 185 Stück im Angebot; der Händler zahlt 30c (`docs/tests/messdaten-2026-10-17.md`).
  - Der Legacy-Bonus «Bountiful Harvest» gibt +20 % bis +100 % Scarce-Material (foreverchanges, 08.10.).
  - Spielerbericht (mmonster, 13.10.): «mostly for low characters or low skill».
  - Mit 16 % ist ein Briarthorn-Knoten netto etwa 14–15s wert (NH), rund 80–85 % davon aus Frilled Lichen. Kräuter sammeln schlägt Angeln ab etwa 13–14 Knoten pro Stunde (NH jetzt) bzw. 18–20 (30 Tage); umgerechnet aus den Werten vom 14.10. (14–15 bzw. 19–22, dort schon nach 5 % Gebühr) mit der korrigierten Fangrate (134 statt 144 pro Stunde), also grob. Knoten pro Stunde: keine Quelle (Messplan M4).

**Entzaubern** [Forever, wow-professions Disenchanting Guide]
- Grüne Rüstung: 75 % Staub, 20 % Essenz. Grüne Waffen: 20 % Staub, 75 % Essenz. Splitter 3–5 %.
- Zeile «11–15»: 2–3 Strange Dust, 1–2 Greater Magic Essence, Small Glimmering Shard.
- Messung 13.10. (15 Zugänge, Art der Teile unbekannt): 8× Staub, 6× Essenz, 1× Splitter; Mengen wie in der Zeile «11–15». 9 Greater Magic Essence ergaben 27 Lesser Magic Essence (1 : 3). Details: `docs/tests/messdaten-2026-10-13.md`.

**Fischen und Kochen** [Forever]
- In Startgebieten entkommen ab Fertigkeit 25 keine Fische mehr (wow-professions; am 13.10. dort nicht wiedergefunden), in Hauptstädten ab 75 (wow-professions, bestätigt 13.10.).
- Stellen: Stonebull Lake für 1–75, Teich in Thunder Bluff für 75–130. Lushwater Oasis (Brachland, in der RXP-Route): Longjaw 39 %, **Deviate Fish 35 %**, Catfish 12 %, Smallfish 8 % von 153 Beutefenstern (AHledger, 12.–13.10.).
- Messung Stonebull Lake (Testlog 13.10., 45.4, 65.2): 14 Fänge in rund 6 Minuten, 11 Roher Langzahniger Matschschnapper und 3 Roher glänzender Kleinfisch; jeder Fang +1 Punkt (Angeln 1 → 15). Entkommene Fische zählt erst Testlog 3.2 (Würfe pro Fang).
- Köder: Shiny Bauble +25, Nightcrawlers +50 (ab 50), Bright Baubles +75 (ab 100).
- Rezepte (SeeMeta, Stufen orange/gelb/grün/grau):
  - Brilliant Smallfish 1/45/65/85
  - Roasted Kodo Meat 35/75/95/115
  - Strider Stew 50/90/110/130
  - Longjaw Mud Snapper 50/90/110/130
  - Tasty Raptor Bites 25/35/55/75 (neu)
- Rezept-Händler (AHledger):
  - Wunna Darkmane (Bloodhoof): Roasted Kodo Meat 2s 40c
  - Harn Longcast (Bloodhoof): Brilliant Smallfish 40c, Longjaw Mud Snapper 4s
  - Naal Mistrunner (Thunder Bluff): Catfish 12s
  - Tari'qa (Crossroads): Strider Stew, Crispy Lizard Tail, Preise nicht sauber lesbar

**Wertvergleich Kräuter und Fische** [Forever-Beta, AHledger PvP Horde US, 13.10.; Details, 30-Tage-Werte und Quellen: `docs/recherche/2026-10-13_kraeuter-fische-kochen.md`]

| Stufen | Kraut vom Knoten, höchster Wert | Zusatzbeute | Fisch roh, höchster | Fisch gekocht, höchster |
|---|---|---|---|---|
| 1–12 | Earthroot 2s 70c (Kräuterkunde 15), Silverleaf 1s, Peacebloom 80c | Commonplace Herb Seeds 18c | Raw Brilliant Smallfish 1s 18c | Brilliant Smallfish 1s 25c |
| 12–17 | Kingsblood 13s 75c (125), Briarthorn 3s 75c (70), Earthroot 2s 70c, Bruiseweed 2s 30c (100) | Frilled Lichen 2g 72s (aus Briarthorn im südlichen Brachland 16 % von 51), Swiftthistle 11s 11c (aus Briarthorn 33 % von 51) | Deviate Fish 10s (Lushwater 35 %) | Savory Deviate Delight 19s 98c (Kochen 85, Rezept fällt im Brachland; Quelle offen) |
| 17–22 | Wild Steelbloom 16s (115), Kingsblood 13s 75c, Stranglekelp 8s 50c (85, unter Wasser) | wie oben; Uncommon Herb Seeds 5s 55c | Deviate Fish 10s; Küste: Oily Blackmouth 5s 87c | Savory Deviate Delight 19s 98c |

- Beta-Preise schwanken stark: Frilled Lichen 2g 72s heute, 67s 80c im 30-Tage-Median; Normal Horde US weicht ab (z. B. Kingsblood 8s 86c, Frilled Lichen 80s 80c). Zum Start zählen EU-Preise (offene Entscheidung 4 in `entscheidungen.md`).
- Kosten (Lehrer, Flüge) sind öffentlich kaum beziffert; Händlerpreise und Lücken: `docs/recherche/2026-10-13_kosten.md`. Testlog 3 misst Lehrer- und Flugkosten.
- Gemessen 13.10. (Testlog, Stufe 6): Angeln lernen 1s, Kochen lernen 1s, Angel 23c. Die Quests 99108, 96659, 96605, 96661, 771 und 748 gaben nur XP, kein Geld; die Tiere in dieser Stichprobe gaben kein Geld, ein Venture Co. Hireling 1c.

**Händler für Berufsmaterial** [Forever, AHledger]
- Nata Dawnstrider (Thunder Bluff): Copper Rod 1s 24c, Mote of Magic 10c, Simple Wood 38c. **Widerspruch:** MetaForge führt dort keine Motes.
- Simple Wood (1 pro Lagerfeuer, 2 für den Camp Chair): Kuruk (Thunder Bluff) 35c, Nata Dawnstrider (Thunder Bluff) 38c, Barg (Crossroads) 35c; in Bloodhoof kein Händler gelistet, die Liste ist unvollständig («and 34 more»). Quelle: AHledger Item 4470, Stand 13.10. Gemessen 17.10.: in Bloodhoof 10 Stück für 3s 80c (38c, Händler bei 45.3, 61.4; Name nicht im Testlog).
- Angel und Phiolen in Bloodhoof: Angel 23c (Testlog 13.10., Händler bei 45.5, 61.7; laut AHledger, Seite Mulgore, verkauft Harn Longcast im Dorf die Angel, abgerufen 17.10.), Leere Phiole 4c (Testlog 17.10., 45.5, 61.8). Eiskalte Milch 25c (17.10., 46.7, 64.5).
- Quest «Gathering Leather» (768, Veren Tallstrider, Thunder Bluff): 12 Leichtes Leder; Belohnung 875 XP und Animal Skin Belt oder Double-layered Gloves, kein Geld (AHledger, 13.10.). Im Kombi-Guide ein Hinweis davor: Die Quest kostet Leder aus dem Vorrat.
- LW-Bedarf:
  - Yonada (Camp Taurajo): Coarse Thread 10c, Fine Thread 1s, Gray Dye 3s 50c, Salt 50c
  - Mahu (Thunder Bluff), Tari'qa (Crossroads), Wunna Darkmane (Bloodhoof)
- Koordinaten dieser Händler: **ungeprüft**.

**Merchant's Favor (Horde)** [Forever]
- Fraktion: Durotar Supply and Logistics. Lager vor dem Westtor der Crossroads, Abgabe bei Dokimi.
- **Widerspruch** bei den Koordinaten: 50.1, 29.3 (Mobalytics) / 42, 34 (Overgear).

**LW-Route 1–150** (Wahl bei Claude, Entscheidung des Nutzers vom 13.10.; Zahlen in `data/kombi/bedarf_lw_vz.csv` und `docs/plan/mengen-leder.md`):
- wow-professions (Forever-Beta, abgerufen 14.10.): 1–30 Light Leather aus Fetzen, 30–55 Cured Light Hide, 55–75 Embossed Leather Gloves, 75–80 Medium Leather (aus 4 Leichtem Leder), 80–90 Cured Medium Hide, 90–100 Fine Leather Belt, 100–115 Light Leather Pants, 115–125 Dark Leather Belt, 125–130 Heavy Leather, 130–140 Cured Heavy Hide, 140–155 Hillman's Leather Gloves. Netto bis 150: 416 Leichtes Leder, 223 Mittleres Leder, 99 Fetzen, 27 Light Hide, 10 Medium Hide, 20 Heavy Hide. Laut Seite werden die meisten Rezepte in Forever 25 Punkte früher grau als in Classic.
- kami-labs (Stand 08.10.): 1–36 Light Armor Kit, 36–62 Cured Light Hide, 62–85 Embossed Leather Gloves, 85–100 Fine Leather Belt, 100–128 Cured Medium Hide, 128–130 Dark Leather Belt, 130–143 Hillman's Shoulders, 143–150 Forceful Heavy Armor Kit (neu, Muster bei Saenorion in Darnassus oder Nioma im Hinterland, für Horde **ungeprüft**). Netto: 240 Leichtes Leder, 72 Mittleres Leder, 32 Light Hide, 42 Medium Hide.
- Messung 13.10. (`docs/tests/messdaten-2026-10-13.md`): ein Rezept mit 4 Mittlerem Leder gab ab LW 98 Punkte, ab 105 kamen Fehlschläge. Das passt zur Aussage von wow-professions (Rezepte früher grau). Welches Rezept es war, steht nicht im Testlog.
- Ab LW 130 zwei Tabs bei wow-professions (abgerufen 14.10.): «Cured Heavy Hide» (130–140 20× Cured Heavy Hide, 140–155 20× Hillman's Leather Gloves) oder «Leveling without Heavy Hide» (130–155 30× Hillman's Leather Gloves, je 14 Mittleres Leder und 4 Fine Thread). Wahlregel der Seite: «If 20x Heavy Hide cost less than around 120x Heavy Leather, 140x Medium Leather and 17x Moss Agate» → Tab «Cured Heavy Hide». Welche Zeile zu welchem Tab gehört, ist aus der Reihenfolge erschlossen; die Einkaufsliste der Seite passt dazu. Bis 150 ist «ohne Heavy Hide» bei Beta-Preisen billiger (berufe-plan.md §4).
- Planungsgrundlage deshalb vorerst wow-professions (die vorsichtigere Rechnung), kami-labs als günstigere Variante daneben. Testlog 3 zeichnet beim Herstellen Rezept und Punkte auf (HERSTELLEN); damit lassen sich die Farbbereiche prüfen.

**VZ-Route 1–150** (wow-professions, Forever-Beta, abgerufen 14.10.): Staub-Weg 275 Strange Dust und 4 Lesser Magic Essence oder Essenz-Weg 313 Lesser Magic Essence und 3 Strange Dust, dazu Copper Rod, 19 Mote of Magic, Silver Rod, Shadowgem; Greater Magic Essence lässt sich 1 : 3 in Lesser umwandeln. Lehrer Horde: Mot und Teg Dawnstrider (Thunder Bluff), Experte Hgarth (Sun Rock Retreat).
- Die Seite hat zwei Tabs: Lesser Magic Essence (70–100 33× Chest - Minor Absorption, 100–109 18× dasselbe, 110–130 20× 2H Weapon - Lesser Intellect, 130–150 32× dasselbe) und Strange Dust (70–100 30× Bracer - Minor Stamina, 100–109 9× Cloak - Minor Protection, 110–130 32× dasselbe, 130–150 20× Boots - Minor Stamina oder 20× Bracer - Lesser Stamina mit 20 Soul Dust). Formel 2H Weapon - Lesser Intellect bei Kithas (Orgrimmar) und Nata Dawnstrider (Thunder Bluff) für 5s, verlangt VZ 100 (AHledger Item 6349).
- Entzaubern: «You get Disenchant together with Apprentice Enchanting», es steht im Berufsfenster, nicht im Zauberbuch, und geht ab Fertigkeit 1 (wow-professions, Enchanting- und Disenchanting-Guide). Ob Entzaubern Punkte gibt, sagt keine Forever-Quelle.
- Ob man für eine Verzauberung ein Zielteil braucht, sagt keine Forever-Quelle ausdrücklich; wow-professions erwähnt im Makro einen «optional target slot».
- Entzaubern der grünen Teile aus der LW-Route liefert laut Modell rund 73 (kami-labs) bis 123 (wow-professions) Strange Dust. Für den Rest braucht es rund 200 bis 330 Leichtes Leder mehr (zusätzliche Embossed Leather Gloves) oder Strange Dust aus dem AH (Beta: unter 1g 40s). Das Modell entzaubert alle grünen Teile; der Plan verkauft seit v0.5.2 Leichte Lederhosen und Dunkle Ledergürtel an den Händler (berufe-plan.md).

**Klassenzauber (Druide, Horde)** [Forever, gemessen 17.10.]
- Lehrerliste von Gennia Runetotem (Bloodhoof, Testlog 3.4, alle drei Filter, 182 Einträge bis Stufe 60; `data/kombi/lehrer.csv`): Stufe 10 15s (5 Zauber je 3s), 12 24s (3 je 8s), 14 36s (4 je 9s), 16 42s (3 je 14s), 18 90s (6 je 15s), 20 1g 68s (7 je 24s), 22 1g 32s (4 je 33s); von 10 bis 22 zusammen 5g 7s. Die Ränge vor Stufe 10 kosteten zusammen 8s 10c. Einzelne Zauber: `docs/tests/messdaten-2026-10-17.md` (Abschnitt Abend).
- «gesperrt» heisst dort: Stufe noch nicht erreicht oder Voraussetzung fehlt (Demoralisierendes Gebrüll auf Stufe 10 erst mit der Bärengestalt). Die Katzengestalt (RXP v4.11.23: Loganaar in Moonglade ab 20, `.train 768`) steht nicht auf der Liste; ihr Preis ist ungeprüft.
- RXPs Route (v4.11.23, Tauren-Druide, «Kombiguide (H)»): Lehrer auf Stufe 8 und 10 in Bloodhoof (#43, #116), 12 am Ende von «6-12 Mulgore» (Gennia, `.xp <12,1`), 14 oder 16 in Moonglade («12-17» #34/#35, Label «DruidTraining1»), 18 und 20 in Moonglade («17-22», Label «DruidTraining2» mit der Katzengestalt). Dazu Zweihandstreitkolben bei Ansekhwa in Thunder Bluff (#141 «Train Two-Handed Maces», `<< Shaman/Druid`, gemessen 10s).
- RXP selbst nutzt `.money >X` für «sammle so viel Gold» (Schritt verschwindet ab X Gold, `functions.lua` `money`; z. B. «Loot them until you have 2 silver worth of vendor items», `Horde-1-12_Mulgore.lua`) und `.money <X` in Lehrer-Schritten (Schritt fällt weg, solange weniger als X da ist).

**Orgrimmar: Lehrer, Händler, Auktionshaus** [Forever, Recherche 14.10.]
- Lederverarbeitung: Kamari (Lehrling, The Drag; RXP v4.11.23 `.goto 1454/1,-4568.1,1855.2`, Spielkoordinaten 63.3, 44.8; Icy Veins 63.0, 45.0), Karolek (Geselle 50–150, Icy Veins `/mappin 1454 62.8 44.4`, wow-professions «Orgrimmar: Karolek»). Experte für die Horde: Una in Thunder Bluff.
- Verzauberkunst: Jhag (Lehrling, Godan's Runeworks; Icy Veins 53.6, 38.2; https://www.wow-professions.com/forever/npc/jhag), Godan (Geselle 50–150; Icy Veins 53.8, 38.4; wow-professions «Orgrimmar: Godan»). Experte: Hgarth, Sun Rock Retreat.
- Händler: Tamar (NPC 3366, Leatherworking Supplies: Coarse Thread 9c, Fine Thread 90c, Gray Dye 3s 15c, Salt 45c; https://ahledger.com/wow-forever/npcs/3366-tamar; gemessen 15.10. 21:38: 44 Coarse Thread und 27 Salt für 17s 90c, passt zu 10c und 50c, ist aber nicht eindeutig (auch 37c und 6c ergäben 17s 90c), Standort beim Kauf 1454 63.2, 45.3; Prüfbericht 15.10.; am 17.10. kostete Grober Faden bei einem Händler in der Gasse 10c, 20 Stück für 2s), Felika (NPC 3367, dazu Copper Rod 1s 7c; https://ahledger.com/wow-forever/npcs/3367-felika), Borya (NPC 3364, ohne Salt; https://ahledger.com/wow-forever/npcs/3364-borya), Kithas (NPC 3346, Enchanting Supplies: Copper Rod 1s 24c, Mote of Magic 10c, Simple Wood 38c, Strange Dust 8s, Lesser Magic Essence 8s, Formel 2H Weapon - Lesser Intellect 5s). Quelle: AHledger-NPC-Seiten (von Spielern gemeldet, teils unter dem Grundpreis). Ort von Tamar gemessen (oben), Kithas in Forever **ungeprüft** (Wiki: 53, 38; wow-professions: der Händler steht neben dem Lehrer).
- Auktionshaus im Valley of Strength; Orgrimmar, Thunder Bluff und Undercity teilen ein Haus, Gebühr 5 % (AHledger, Seite «Auction House»). Pfand je Angebot (gemessen, 24 Angebote 15.–17.10., 24 Stunden): 60 % des Händlerpreises mal Menge, mindestens 1s; zurück beim Verkauf, sonst weg; andere Dauern ungeprüft (`docs/tests/messdaten-2026-10-17.md`). Porto (17.10.): passt zu 30c je angehängtem Stapel und 30c für einen Brief nur mit Gold; am Abend kostete ein Brief mit 3 Stapeln 90c in einer Buchung, also 30c je Stapel, nicht je Brief. Auctioneer Thathung: RXP v4.11.23 `.goto 1454/1,-4460.31,1685.31` (55.6, 62.9).
- Rang-Kosten: wow-professions nennt «Apprentice 10, Journeyman 5, Expert 50, Artisan 5» ohne Einheit, auf der NPC-Seite von Karolek Journeyman «450»; ausdrücklich nur «Expert … costs 50 silver». Kosten einzelner Rezepte nicht gefunden. Das Testlog misst beides.
- Gemessen 15.10.: Lernstufe und Kosten aller Rezepte bei Kamari, Karolek, Jhag und Godan in `data/kombi/lehrer.csv` (übernommen mit `tools/lehrer_aus_testlog.py`, Tabelle mit AHledger-Vergleich in `docs/tests/messdaten-2026-10-15.md`). Die Lernstufen liegen bei den LW-Rezepten 10 bis 40 Punkte über AHledgers «orange», bei den VZ-Rezepten teils darunter; die Farben bei der aktuellen Fertigkeit passen zu AHledger (12 Rezepte geprüft). Lernkosten bis 150, gerechnet: Lederverarbeitung 40s 10c (mit «Cured Heavy Hide» 45s 10c), Verzauberkunst 34s 10c (Staub-Weg, mit Stiefel - Schwache Ausdauer) bzw. 21s 10c (Essenz-Weg mit Formel, ohne Minor Deflect). Der Plan seit 16.10. lernt für Lederverarbeitung 40s 10c und für Verzauberkunst 33s 60c (Stufen A–D zusammen 73s 70c, berufe-plan.md).
- Enchant Bracer - Minor Deflect (Armschiene - Schwache Abwehr) steht auf keiner der beiden Verzauberkunst-Listen in Orgrimmar, auch nicht als gelernt; der gemessene Charakter kennt es trotzdem. Woher es kommt (mit dem Lehrling, anderer Lehrer, Formel), ist offen. SeeMeta (Enchanting, Stand 14.10.2026, https://seemeta.com/en/wow-forever/professions/enchanting) sagt «Learned automatically with the profession rank»; das passt dazu, im Spiel ungeprüft (Test mit dem Stufe-8-Druiden: Lehrling lernen, Berufsfenster öffnen; REZEPTE zeigt es). Der Kombi-Guide nimmt seit v0.5.1 stattdessen Enchant Chest - Minor Absorption (ab 40, 1s, gleiches Material: 1 Lesser Magic Essence). Bei VZ 100 zeigte REZEPTE (15.10.): Minor Deflect grün, Minor Absorption gelb, Chest - Inferior Stamina grün, Bracer - Minor Stamina gelb, passend zu AHledger (`data/kombi/rezepte.csv`).
- Zauberstäbe (Recherche 15.10.): Geringer Magiezauberstab laut SeeMeta gelb ab 75, grün ab 95, grau ab 115; Grosser Magiezauberstab gelb ab 110, grün ab 130, grau ab 150 (https://seemeta.com/en/wow-forever/professions/enchanting, Stand 14.10.2026). Bei VZ 100 im Testlog: Geringer grün, Grosser orange (passt). Reagenzien laut Testlog: 1 Simple Wood und 1 bzw. 2 Lesser Magic Essence. Lernbar ab 10 (50c) bzw. 70 (2s) (`lehrer.csv`). Der Händler zahlt 1s 10c bzw. 2s (Gegenstands-Infos 15.10.). Daraus die Variante in berufe-plan §9 (Vorschlag, nicht im Guide).
- Händlerpreise im Forever-Client (`data/preise/haendler_ankauf.csv`, ab Testlog 3.6): Vergleich mit den Classic-Daten in `docs/recherche/2026-10-15_haendlerpreise.md`. Viele hergestellte Teile zahlt der Händler niedriger als in Classic (Risiko 26).
- Verlernen: Warcraft Tavern (Forever) «click on the red X next to the profession's skill bar in the Professions window», Bestätigung eintippen; Zockify: Reiter «Skills» im Charakterfenster (**Widerspruch**). Forever-API 1.60.1: `C_SkillInfo.AbandonSkill(skillLineID)`. Kosten nicht gefunden.
- Mote of Magic: Item 247786, neu in Forever, 10c bei den Enchanting-Händlern der Hauptstädte (Kithas, Nata Dawnstrider u. a.); Rezept «Dust to Motes» macht aus 1 Strange Dust 3 Motes (AHledger). Laut wow-professions nicht im AH kaufen; AHledger zeigt trotzdem Angebote.
- Lernstufen der Rezepte (Farben orange/gelb/grün/grau) laut AHledger: `data/kombi/rezepte.csv`. Sie passen zu den Herstellungszahlen von wow-professions für LW; für VZ 20–40 nicht (Widerspruch 17).

**Fischen im Brachland** [Forever, AHledger, Recherche 14.10.]
- Lushwater Oasis: Longjaw 39 %, Deviate Fish 35 %, Catfish 12 %, Smallfish 8 % von 153 Fängen (Itemseiten). Deviate Fish (Item 6522): Median Normal Horde US 4s 50c, PvP Horde US 10s 99c; 30 Tage 4s 19c bzw. 7s 26c; «about 1,900 sold a day» (PvP Horde US).
- Savory Deviate Delight: Kochen 85 (85/125/145/165), 1 Deviate Fish und 1 Mild Spices; Median Normal Horde US 4s 45c, PvP Horde US 7s 94c. Rezept 6661 fällt im Brachland, z. B. bei Witchwing Roguefeather und Zhevra Runner je 2 % (AHledger); method.gg: «drops from any mob in The Barrens».
- Nötige Angelfertigkeit im Brachland: keine Forever-Quelle. [Classic] Wowhead: Deviate Fish ab 1, ohne Entkommen ab 75 (https://www.wowhead.com/classic/cn/guide/best-fishing-pools-farming-locations-classic-wow); Warcraft Tavern: 100 (https://warcrafttavern.com/wow-classic/guides/deviate-fish).
  - realmfirst (24.09.): «The Forever client does not publish a fishing level per zone».
  - classicwowforever (03.10.): «Zone skill levels live on the server, so they aren't confirmed for Forever yet».
- Angelstellen auf der Forever-Karte, aus RXP v4.11.23 umgerechnet (Karte 1413, exakt), im Spiel ungeprüft:
  - Lushwater Oasis etwa 46.8, 39.4: Mittelwert der Schleife um den See bei Hezrul, Zeilen 2855–2889
  - Forgotten Pools 45.1, 22.5: Bubbling Fissure, Quest 870, Zeile 1550
  - Stagnant Oasis 55.6, 42.8: Bubbling Fissure, Quest 877, Zeile 2540
  - Die Classic-Werte von Warcraft Tavern (46, 40 / 45, 23 / 55, 43) liegen bis 1,6 Punkte daneben.
  - warcraft.wiki.gg und wowpedia nennen Koordinaten der Karte nach Cataclysm; die passen nicht.
- Roh verkaufen bringt mehr als kochen: Deviate Fish 4s 50c gegen Savory Deviate Delight 4s 45c (NH); PH 10s 99c gegen 7s 94c.
- Angeln pro Stunde, gerechnet mit der Fangrate vom Stonebull Lake (14 Fänge mit 13 Abständen in 349 s, also 134 pro Stunde; davon 35 % Deviate Fish): 2g 11s (NH) bzw. 5g 16s (PH) vor und 2g 1s bzw. 4g 90s nach 5 % Gebühr (berufe-plan.md §1; bis 15.10. mit 144 Fängen gerechnet, Prüfbericht 15.10., A3). Die Rate im Brachland ist ungeprüft (Messplan M3).
- Lederverarbeitung mit Gewinn laut AHledger (Liste mit Absatz und Musterquellen: `docs/recherche/2026-10-14_goldquellen.md` §4):
  - Cured Light Hide NH +4s 53c
  - Medium Armor Kit NH +1s 70c
  - Mystic Medium Armor Kit NH +3s 24c, PH +13s 22c; Muster bei Tamar 4s 50c
  - Light Leather Reagent Bag NH +9s 6c (Muster-Quelle unbekannt)
  - Barbaric Bracers NH +15g 24s (Muster-Quelle in Forever unbekannt)
- Heavy Leather auf der Rezeptseite ohne Gewinn: NH −2s 51c, PH −96c. Der Berufe-Plan rechnet mit dem älteren Preis (Risiko 22).

**Widersprüche zwischen den Quellen** (Recherche 13.10. und 14.10., im Spiel zu prüfen)
1. Koordinaten Yonn Deepcut (Kürschnerei, Bloodhoof); gemessen 14.10.: 45.0, 61.5 bei der Abgabe von 97936, passt zu 45.0, 61.4
2. Koordinaten Mooranta (Kürschnerei, Thunder Bluff), drei Quellen
3. LW-Ränge: kami-labs gegen wow-professions und Icy Veins; gemessen 15.10.: Geselle ab Stufe 10 und LW 50, 5s (Karolek)
4. VZ-Ränge und Koordinaten von Mot, Teg und Hgarth; gemessen 15.10. in Orgrimmar: Geselle ab Stufe 10 und VZ 50, 5s (Godan); Thunder Bluff offen
5. Stufen-Voraussetzung Kräuterkunde: wow-professions gegen Icy Veins
6. Ab wann Kürschnerei-Journeyman: RankedBoost gegen die anderen; gemessen 17.10.: ab Kürschnerei 50, ohne Stufe, 5s (Yonn Deepcut), wie wow-professions
7. Bruiseweed: Fertigkeit 85 oder 100
8. Flint and Tinder für Lagerfeuer nötig oder nicht
9. Geben versiegelte Kisten Ruf oder nicht
10. Lager von Durotar Supply bzw. Koordinaten Dokimi
11. XP-Bonus bei allem gekochten Essen oder nur bei den meisten
12. Dedicated Study bei voller Fertigkeit: 3 oder 2–4 Essenzen
13. LW- und VZ-Route 1–150: wow-professions gegen kami-labs
14. Untergrenze Leichtes Leder: Gegnerstufe 1 oder 5
15. Thuwd in Orgrimmar: LW-Lehrer (Icy Veins) oder Kürschnerei-Lehrer (wow-professions)
16. Ränge der VZ-Lehrer: Godan und Teg Dawnstrider Geselle (wow-professions, Icy Veins) oder Experte (kami-labs); gemessen 15.10.: Godan führt den Gesellen, keinen Experten (wow-professions und Icy Veins stimmen)
17. Lernstufen VZ 20–40: Enchant Chest - Inferior Stamina ab 30 und Bracer - Minor Deflect ab 40 (AHledger) gegen ab 20 (wow-professions); gemessen 15.10.: Chest - Inferior Stamina ab 15 (wie kami-labs), Minor Deflect bei Jhag und Godan nicht im Angebot; laut SeeMeta kommt Minor Deflect mit dem Rang (Stand 14.10.)
18. Verlernen: Berufsfenster (Warcraft Tavern) oder Reiter Fertigkeiten (Zockify)
19. Mote of Magic nur beim Händler (wow-professions) gegen Angebote im AH (AHledger)
20. Lesser Magic Wand ab 35 (AHledger) oder ab 10 (kami-labs); Minor Mana Oil ab 120 oder 150; Minor Wizard Oil ab 1 oder 5 (AHledger Rezept- gegen Formelseite); gemessen 15.10.: Lesser Magic Wand ab 10 (wie kami-labs); Minor Wizard Oil und Minor Mana Oil führen die Lehrer in Orgrimmar nicht
21. Händlerpreis hergestellter Zauberstäbe: 1c laut Patch-Notiz zum Level-30-Update (Warcraft Tavern, 01.10.: https://www.warcrafttavern.com/forever/news/level-30-content-is-now-available-in-the-wow-forever-beta/) gegen 1s 10c (Lesser Magic Wand) und 2s (Greater Magic Wand) in Datenbanken auf Build 70374 (https://foreverchanges.pro/item/11287, https://foreverchanges.pro/item/11288, https://wowforever.wclbox.com/en/wupin/11287). Gemessen 14.10. (Testlog 19:53): Ein Händler zahlte 22s für 11 Greater Magic Wand, also 2s je Stück wie in den Datenbanken; der Forever-Client meldet in den Gegenstands-Infos (Testlog 15.10.) 1s 10c für den Geringen und 2s für den Grossen Magiezauberstab

---

## 10. Testplan (gemeinsam)

Jeder Befund kommt mit `/tl bug <Text>` oder `/tl <Text>` ins Testlog. Zurück an Claude geht er über `/tl zeigen` (kopieren und einfügen) oder als Datei `KombiTestlog.lua`.

| ID | Test | Erwartet |
|---|---|---|
| T0 | Beide Addons installiert, einloggen | Testlog schreibt `SITZUNG` mit Client, RXP-Version und Kombi-Guide-Version |
| T1 | RXP-Menü → «Verfuegbare Guides» → «Kombiguide (H)» | Gruppe und 4 Guides sichtbar, Start mit «1-6 Mulgore» |
| T2 | Mulgore 1–6 spielen | Schritte laufen wie bei RXP; Berufsschritte erscheinen an der richtigen Stelle; Pfeil stimmt |
| T3 | Stellen mit `#completewith next` neben unseren Schritten | Nichts hängt |
| T4 | Ohne Kürschnerei weiterspielen (Probe) | Berufsschritte mit `.skill …,<1,1` verschwinden |
| T5 | Ende 17-22 | Sprung in den gekauften Guide «22-24 Hillsbrad» oder klare Meldung |
| T6 | Update-Übung: neue Kombi-Datei einspielen | Fortschritt bleibt erhalten |
| T7 | Testlog prüfen | `SAMMELN` beim Kürschnern und Kräutersammeln, `HERSTELLEN`/`ENTZAUBERN` beim Beruf, `HÄNDLER`/`GELD` beim Einkaufen und beim Lehrer; `BERUF` bei jedem Punkt; `RXP` bei jedem Schritt |
| T8 | Quellen-Widersprüche vor Ort prüfen | Koordinaten Yonn Deepcut, Rang-Grenzen Kürschnerei/Kräuterkunde, Bruiseweed, Dokimi |
| T9 | Leder-Zähler im Kombi-Guide (v0.2/v0.3) gegen den echten Bestand | Zähler zeigt «x/Ziel»; das Testlog (SAMMELN, TASCHE) zeigt, ob das Modell zu hoch oder zu tief liegt |
| T10 | Farm-Stopp S1 (optional, seit v0.4 mit Sweetspot-Zähler) | Pfeil zur Farmstelle; Häute pro Stunde, Anteil Leichtes/Mittleres Leder und Stücke pro Haut ab Gegnerstufe 11 im Testlog (SAMMELN mit Kreatur-ID und Zeit) |
| T11 | Sitzung in Orgrimmar (v0.4, Stufe A, optional B) | Verlernen per Kästchen; Rezepte lassen sich wie geplant lernen (VZ 20–40 prüfen, Widerspruch 17); Zähler und Material-Bedingungen schalten richtig; Testlog zeigt Dauer und Kosten (HERSTELLEN, ENTZAUBERN, GELERNT, GELD) |
| T12 | Sitzung in Thunder Bluff (v0.4, Stufen B–D) | Schon erledigte Stufen verschwinden; Einkaufszähler stimmen für «B und C zusammen», «C allein» und «D» |
| T13 | Lehrerfenster öffnen, Filter auf alle drei Arten (Testlog 3.4) | Eine Zeile LEHRER pro Lehrer mit Status, Lernstufe und Kosten jedes Eintrags; beim zweiten Öffnen keine neue Zeile; bei Berufslehrern der Rang (Geselle) mit «(Rang)» |
| T14 | Nach dem Sprung in den gekauften Guide zurück in den Kombi-Guide und wieder in den gekauften | Der gekaufte Guide steht am selben Schritt (Fortschritt pro Guide, §3); Grundlage für Berufs-Halte nach Stufe 22 |
| T15 | Auktionshaus öffnen (Testlog 3.5) | Chat «AH-Scan läuft», dann «AH-Scan fertig» mit Angeboten und Leichtem Leder; Tiefstpreis gleich wie im Auktionshaus; Zeile AH-SCAN; beim nächsten Öffnen innerhalb von 15 Minuten kein neuer Scan; nach `/reload` zählt `/tl status` die Scans weiter |
| T16 | Briefkasten mit Briefen des Auktionshauses öffnen (Testlog 3.6) | Eine Zeile AH-POST mit verkauft, abgelaufen, gekauft (Menge, Preis, Gebühr); beim nächsten Öffnen keine Zeile für dieselben Briefe; Preis gleich wie im geöffneten Brief |
| T17 | Jedes Berufsfenster öffnen, danach herstellen (Testlog 3.6) | REZEPTE mit allen gelernten Rezepten (Reagenzien, Ergebnis, Farbe) wie im Fenster; nach einem Farbwechsel eine kurze Zeile «Farbe: …» mit der Fertigkeit |
| T18 | Bank öffnen und wieder schliessen (Testlog 3.6) | INVENTAR mit Bank und Kontobank; ohne Änderung keine zweite Zeile; nach Ein- oder Auslagern beim Schliessen eine neue |
| T19 | Etwas im Auktionshaus einstellen (Testlog 3.6) | AH-ANGEBOT mit Menge, Preis je Stück oder je Angebot, Dauer und Pfand wie im Verkaufsfenster, Ende «erstellt» |
| T20 | Zwei AH-Scans 15 Minuten bis 2 Stunden auseinander (Testlog 3.6) | In der Datei bei jedem Scan `bandRoh` (kleinster und grösster Rohwert der Restlaufzeit) und `bandVersatz` (0 bei 0–3, -1 bei 1–4); zweite Zeile AH-SCAN mit «Abnahme seit dem letzten Scan»; `tools/ah_aus_testlog.py` schreibt `data/preise/ah_abnahme.csv` |
| T21 | Ordner `KombiDaten` neu, Spiel neu starten, dann `/tl tipp` und `/tl tipp alle` | Beim Einloggen «Empfehlungen geladen»; SITZUNG nennt den Stand; Tipps im Chat und im Fenster zum Kopieren; nach einer neuen `Daten.lua` reicht `/reload` |
| T22 | Kombi-Guide v0.5 oder neuer: neue Version im AddOns-Ordner, `/reload`, im RXP-Menü die Gruppe «Kombiguide Dungeon (H)» wählen (ohne Beta-Features) | Gruppe mit 4 Guides sichtbar, keine Fehlermeldung beim Laden; SITZUNG meldet die Version aus der `.toc` (z. B. «Kombiguide 0.5.2-v4.11.23») (die Version steht in der `.toc`; `/reload` liest sie neu, Testlog 15.10.); ein Charakter in «6-12 Mulgore» sieht in Thunder Bluff «RFCPickups1», einer in «12-17» zu Beginn die RFC-Schritte; «Kombiguide (H)» steht weiter an der alten Stelle |
| T23 | Testlog 3.7: 20 Minuten questen und kämpfen, dann `/reload` | `/tl status` zeigt Laufweg-Proben und XP-Quellen; `tools/spiel_aus_testlog.py` schreibt `laufweg.csv` und `xp_quellen.csv`; «Gegner» mit Kreatur-ID und Gegnerstufe; Quest-XP gleich wie in QUEST AB |
| T24 | Dungeon-Lauf (RFC oder WC), mit Tod und Rückweg, wenn er passiert | DUNGEON beim Betreten und am Ende (Dauer, Zeit draussen, XP, Kills, Geld, Beute, Tode, Stufe, Gruppe); Tod und Wiederbetreten bleiben ein Lauf |
| T25 | Eigenes Angebot im AH (Testlog 3.7) | AH-ANGEBOT mit dem Pfand aus dem Geldabzug; weicht der Wert des Spiels ab, steht er dahinter («Spiel meldete …») |
| T26 | AH-Scan mit Testlog 3.7 | Händlerpreise in `data/preise/ah_alle.csv` und `haendler_ankauf.csv`; liegen Angebote unter dem Händlerpreis, meldet der Chat sie; einen gemeldeten Gegenstand im Tooltip prüfen (Verkaufspreis) |
| T27 | `/tl tipp` mit neuen KombiDaten | Zuerst «Nächster Schritt für dich» (Beruf, Fertigkeit, Rezept, Material, Kosten); stimmt mit dem Berufsfenster überein |
| T28 | Im Ordner `_classic_beta_` die Datei `KombiEinrichten.bat` (Kopie von `tools/windows/kombi_einrichten.bat`) einmal ausführen, dann das Spiel starten (ob `/reload` statt Neustart reicht, ist ungeprüft) | Die drei Addon-Ordner sind echte Ordner (keine Verknüpfung); SITZUNG zeigt die Versionen aus `_kombi_neu` (seit 16.10.: Testlog 3.7.1, Kombiguide 0.6.1); Claude schreibt danach neue Versionen direkt. Die Datei im Repo-Klon bricht ab (sie sucht `Interface\AddOns` neben sich) |
| T29 | Gesellen-Schritt (Kürschnerei in Thunder Bluff, ab Fertigkeit 50; Lederverarbeitung und Verzauberkunst in Orgrimmar) | Vor dem Lernen ist der Schritt da (sonst kennt der Charakter die ID schon); nach dem Lernen hakt er sich selbst ab (`.istrained`); GELERNT zeigt die Zauber-ID des Gesellen. Hakt er nicht ab: Häkchen setzen und die ID aus GELERNT melden |
| T30 | Lern-Schritte mit `.train` bei Kamari und Jhag (Lederverarbeitung und Verzauberkunst lernen, Risiko 28) | Nur der Lehrling wird gekauft: GELERNT nur Lederverarbeitung bzw. Verzauberkunst, GELD beim Lehrer 10c |
| T31 | Händler öffnen mit Leder oder Beute aus `KombiDaten.nichtVerkaufen` in den Taschen (Testlog 3.7.1) | Eine Chat-Zeile «Nicht beim Händler verkaufen …» mit höchstens 6 Einträgen; beim zweiten Öffnen im selben Besuch keine zweite |
| T32 | Zwei AH-Scans 20 bis 110 Minuten auseinander (Testlog 3.7.1) | 20 Minuten nach dem ersten der Hinweis «Abnahme messen», nur in Orgrimmar, Thunder Bluff oder Undercity; zweite Zeile AH-SCAN mit «Abnahme seit dem letzten Scan»; im zweiten Scan mehr Gegenstände mit Händlerpreis als im ersten |
| T33 | Ein- und Ausloggen, Beruf steigt, Geld ändert sich (Testlog 3.7.1) | In der Datei bei `chars[Charakter]` die Felder `berufe` und `geld`; `/tl tipp` zeigt beim Sammler (Druide) den nächsten Schritt mit Gold für Orgrimmar |
| T34 | Kombi-Guide 0.6, «6-12 Mulgore» in Thunder Bluff nach Cairne | Zusatzschritt «Rahauro» mit zwei RFC-Quests steht neben der Route und hält sie nicht auf; nach der Annahme hakt er sich ab; ohne Annahme verschwindet er am Ende von Mulgore («WildManeTurnIn»); der Pfeil bleibt bei der Route (auch auf dem Sprungpfad von der Hunter Rise), Rahauro hat eine Stecknadel; spricht man ihn an, nimmt RXP die Quests selbst an (Quest-Automatik) |
| T35 | Kombi-Guide 0.6, «12-17» in Orgrimmar (Stufe 15–17) | Vor der Berufssitzung Thrall und Neeru als Zusatzschritte bis zum Zeppelin-Schritt; danach der Abstecher: Häkchen beim Zeppelin-Schritt lässt alle Abstecher-Schritte wegfallen (weiter mit dem Ruhestein); mit dem Zeppelin erscheinen in Tirisfal die Annahmen als Liste (ab Stufe 16 auch Griffs und Bel'dugur), der Lauf als Kästchen, danach nur die erledigten Abgaben (auch Faranell; Wappen und Kopf mit `.isOnQuest`), die SFK-Quests im Grabmal nur, wenn Stufe 18 erst im Abstecher kam; Pfeile in Tirisfal, Unterstadt und Silberwald zeigen richtig (Kontinent 0); im Dungeon bleiben die Schritte stehen (`.zoneskip` ohne Karte) |
| T36 | Kombi-Guide 0.6, «12-17» nach Orgrimmar und «17-22» | Ratchet beim ersten Halt: Bigglefuzz bis «LeaveRatchet»; Lushwater Oasis: Nalpak und Ebru bis «Hezrul» (beide mit Stecknadel, der Pfeil bleibt bei der Route); in «17-22» bei Mebok nach der Abgabe von Raptor Horns die WC-Quest (und ab Stufe 20 die RFK-Quest), Zamah nach der Abgabe von 853 (bleibt bis zur Elder Rise stehen), Nara nach der Abgabe von 1490; RFC-Abgaben bei Rahauro nur, wenn erledigt; BFD bei Je'neu Sancrea (Zoram'gar) |
| T37 | Kombi-Guide 0.6, «17-22» mit einer WC-Quest im Log (Thunder Bluff nach Moonglade) bzw. mit 6563 am Ende | Zuerst das Kästchen «Gelesen» (Kombiguide), dann RXPs Schritte «Abandon …»; Häkchen dort lässt die Quest im Log und die Route geht weiter; ohne solche Quests erscheint weder das Kästchen noch ein Abbruch-Schritt |

Messungen mit mehreren Druiden (M1–M12, Stand 15.10., mit Kurzliste bis 22.10.) und die Checkliste für den Stufe-8-Druiden (16.10.: was er beim normalen Leveln selbst prüft): `docs/tests/messplan-beta.md`.

Teststand bis 15.10. 22:16 (Testläufe, Messdaten, `docs/tests/`):
- **T0** bestanden, auch mit Testlog 2 und den verknüpften AddOns (SITZUNG meldet «Kombiguide 0.1.1-v4.11.13»), und am 13.10. 22:08 mit RestedXP v4.11.23, Testlog 3 und «Kombiguide 0.1.2-v4.11.13» (der ältere Bau läuft mit dem neueren RXP).
- **T1** bestanden: Gruppe sichtbar, Wechsel 1-6 → 6-12 innerhalb «Kombiguide (H)».
- **T2** teilweise: Schritte am richtigen Ort, Pfeil zu Nawka rund 28 Yards daneben (v0.1). v0.1.2 zielt mit den exakten Kartenecken auf die gemessene Stelle. Im Spiel nur mit einem Charakter ohne Kürschnerei prüfbar, sonst überspringt RXP den Schritt.
- **T4** indirekt: Ein schon gelernter Beruf wird übersprungen.
- **T7** teilweise: BERUF, RXP, QUEST, TOD und KARTE laufen; mit Testlog 3 (13.10. 22:12–22:42) auch SAMMELN (Kürschnern, Kräuter), ANGELN, BEUTE, HÄNDLER, GELD (Lehrer), GELERNT, REZEPT und AUKTIONSHAUS. Eine Post-Sitzung blieb offen (Risiko 19), behoben in Testlog 3.2; «Bestand 0c» beim Ausloggen behoben in 3.3. Im Spiel noch offen: HERSTELLEN, ENTZAUBERN, Flugkosten.
- **T6** teilweise: Update v0.1.1 → v0.1.2 (nur Koordinaten) behielt die Stelle («06-12 Mulgore #13», 13.10. 22:08). Neubau auf RXP v4.11.23: neue Quest 99411 «Kyle's Gone Missing!» (`#softcore`); für den Tauren-Druiden kommen davor zwei Schritte dazu. Erwartet für den Stand vom 13.10. 22:42 («06-12 Mulgore #28», Quest 754): RXP findet die Kennung nicht, nimmt #28 (Abgabe 748, erledigt), springt selbst auf #30, dieselbe Stelle. **Bestanden** (13.10. 22:50: SITZUNG zeigt #30; `docs/tests/testlauf-3.md`, Nr. 13).
- **T3, T5** offen; **T8** teilweise: Yonn Deepcut (Abgabe von 97936 bei 45.0, 61.5, Testlog 14.10.).
- **T15** teilweise (15.10. 20:12): Der Scan lief beim Öffnen des Auktionshauses von selbst und vollständig. Der Vergleich mit dem Tiefstpreis im Auktionshaus und das zweite Öffnen innerhalb von 15 Minuten sind nicht gemeldet. Zweiter Scan 21:54, ebenso vollständig.
- Stand 15.10. 22:01 (`docs/tests/messdaten-2026-10-15.md`):
  - **T11** teilweise: Der Orgrimmar-Block lief für einen Charakter mit LW 109 und VZ 100 durch (laut Nutzer «alles hat funktioniert»); mit v0.4 erschien noch der Einkauf der Stufe A (behoben in v0.4.1).
  - **T17** teilweise: REZEPTE für Lederverarbeitung, Verzauberkunst und Kochkunst mit Farben; Farbwechsel noch nicht beobachtet.
  - **T18** teilweise: Taschen und Bank (leer) erfasst, Kontobank ohne Daten.
  - **T19** teilweise: Angebot erfasst; der Pfand aus `CalculateCommodityDeposit` zeigt 0c, abgebucht wurden 1s.
  - **T22** teilweise: Nach `aktualisieren.bat` und `/reload` meldet SITZUNG Kombiguide 0.5; ob die Dungeon-Gruppe im Menü erscheint, ist nicht gemeldet.
  - **T13** bestanden (22:08–22:13): eine Zeile pro Lehrer und Filter, Status, Lernstufe und Kosten, der Geselle mit «(Rang)».
  - **T20** teilweise (22:15): `bandRoh` und `bandVersatz` stehen in der Datei; die Abnahme braucht einen zweiten Scan mit Testlog 3.6.
- Stand 16.10. 17:47 (vier Charaktere ein- und ausgeloggt, Client 70425):
  - **T28** bestanden: `KombiEinrichten.bat` (nach der Korrektur für «Program Files (x86)», PR #29) hat die drei Verknüpfungen nach `_alt_kombi` gelegt und die Ordner aus `_kombi_neu` installiert; alle vier SITZUNG-Zeilen zeigen «Kombiguide 0.6.1-v4.11.23», «Testlog 3.7.1» und KombiDaten.
  - **T6** bestanden für 0.6.1: Der Tauren-Druide steht weiter in «6-12 Mulgore» #45, der Stufe-18-Charakter in «12-17 The Barrens» #152 (über `#maxlevel 17`, §6).
  - **T16** teilweise: AH-POST mit drei Verkäufen (Preis, Gebühr 5 %, Pfand zurück); die Pfand-Werte je Edelstein stehen in den Briefen. Zwei weitere Briefe brachten zusammen 7g 0s 1c, ohne Rechnung des Auktionshauses (Herkunft nicht im Testlog).
  - **T33** teilweise: Berufe und Geld pro Charakter beim Einloggen in `chars`.
- Stand 17.10. 13:38 (Messlauf des Druiden nach der Checkliste, Stufe 7,74 → 9,10; Client 70450; `docs/tests/messdaten-2026-10-17.md`):
  - **T6** bestanden für 0.6.1 beim Druiden: Er stand beim Einloggen bei #45 und kam bis #52.
  - **T13** bestanden auch für einen Klassenlehrer (182 Einträge) und für Kürschnerei und Schneiderei, jeweils mit allen drei Filtern.
  - **T15** teilweise: Scan am 17.10. 13:36 vollständig (Bankchar, Orgrimmar); das zweite Öffnen fehlt noch.
  - **T16** teilweise: AH-POST erkennt auch «abgelaufen».
  - **T17** teilweise: Farbwechsel beobachtet (Einfaches Lagerfeuer gelb → grün → grau, Kochkunst 3 und 5).
  - **T23** bestanden: XP pro Gegner mit Kreatur-ID und Gegnerstufe; Quest-XP gleich wie in QUEST AB.
  - **T25** bestanden: AH-ANGEBOT mit Pfand aus dem Geldabzug (1s 50c) und dem Wert des Spiels daneben (1s 44c).
  - **T27, T31** nicht prüfbar: KombiDaten im Spiel war ein alter Stand (Ablauf-Befund 1 in den Messdaten), seit 17.10. 11:43 UTC neu und geprüft.
  - **T29** offen: Geselle Kürschnerei lernbar ab 50 für 5s, der Druide hatte 2s 78c.
  - Neu im Testlog: Die fertigen Leinentaschen (HERSTELLEN) erscheinen nicht als Ergebnis; eine Beute direkt nach dem Kürschnern landete einmal in SAMMELN.
- Stand 17.10. 15:15 (Nachmittag, Druide Stufe 9,10 → 10,75; `docs/tests/messdaten-2026-10-17.md`):
  - **T6** bestanden: Der Druide kam von #52 bis #116; der Stufe-18-Charakter steht weiter bei #152.
  - **T16** teilweise: AH-POST «verkauft» beim Bankchar (Preis, Gebühr, Pfand zurück); ein Brief, der nach 2 s abgeholt war, fehlt.
  - **T20, T32** teilweise: Zwei Scan-Paare (61 und 25 Minuten) ergeben die erste Abnahme; ob der Hinweis «Abnahme messen» kam, steht nicht in der Datei (nur Chat).
  - **T25, T26** bestanden: 14 Angebote mit Pfand aus dem Geldabzug; Scans mit Händlerpreis und Angeboten darunter.
  - **T27** teilweise: KombiDaten mit dem Stand 17.10. 13:36 geladen (SITZUNG ab 14:38).
  - **T29** bestanden für Kürschnerei: Der Gesellen-Schritt bei Mooranta (`.istrained 8617`) war 2 s nach dem Lernen erledigt.
  - **T31** offen: Die Warnung beim Händler schreibt das Testlog nicht in die Datei.
  - Testlog: POST «erhalten» nannte beim Bankchar 20 statt 27 Leichtes Leder und 20 statt 36 Fetzen (Rest kam nach dem Ende der Sitzung; INVENTAR stimmt).
- Stand 17.10. 17:08 (Abend, Druide Stufe 10,75 → 12,16; `docs/tests/messdaten-2026-10-17.md`):
  - **T6** bestanden: Der Druide kam mit 0.6.1 von #116 bis #153 (Moonglade); der Stufe-18-Charakter steht weiter bei #152.
  - **T13** bestanden auch für einen Waffenmeister (Ansekhwa, 1 Eintrag, Typ «Klasse»); das Lernen dort schreibt keine Zeile GELERNT, nur GELD beim Lehrer.
  - **T16** bestanden für sechs Briefe: AH-POST beim Öffnen des Briefkastens in Bloodhoof, beim Abholen in Thunder Bluff keine zweite Zeile.
  - **T19, T25** bestanden: sechs weitere Angebote, alle mit der Pfand-Regel; beim Skalpiertomahawk meldete das Spiel 5c weniger als den Geldabzug.
  - **T20, T32** teilweise: drittes Scan-Paar (109 Minuten) mit Abnahme; der Hinweis «Abnahme messen» steht weiter nur im Chat.
  - **T26** bestanden: 241 Händlerpreise neu oder ergänzt.
  - **T27** teilweise: Die KombiDaten vom Nachmittag lagen erst nach dem Einloggen um 15:37 auf dem PC.

---

## 11. Quellen

- RXP: https://github.com/RestedXP/RXPGuides · https://community.restedxp.com/?p=586526 · https://kami-labs.fr/en/wow-forever/mise-a-jour-restedxp-wow-forever/ · https://kami-labs.fr/wow-forever/installer-restedxp-wow-forever/
- Blizzard-UI-Code Forever 1.60.1 (70338; seit 14.10. 70374): https://github.com/Gethe/wow-ui-source/tree/forever
- Testlog 3.7, Forever-UI 1.60.1 (70374): `InstanceDocumentation.lua` (`IsInInstance`, `GetInstanceInfo` mit `instanceID` an 8. Stelle), `PlayerScriptDocumentation.lua` (`GetXPExhaustion`, `IsResting`), `UnitDocumentation.lua` (`UnitGUID` mit SecretWhenUnitIdentityRestricted, `UnitOnTaxi`, `UnitIsDeadOrGhost`, Ereignis `PLAYER_XP_UPDATE`), `ItemDocumentation.lua` (`IsItemDataCachedByID`, `GetItemInfo` mit «sellPrice» an 11. Stelle)
- Rezepte und Zauberstäbe: SeeMeta, Enchanting (Stand 14.10.2026) https://seemeta.com/en/wow-forever/professions/enchanting
- Händlerpreise in Classic zum Vergleich (nur Vergleich, nicht für den Plan): wow-classic-items (MIT, Stand 25.11.2022, Daten von Wowhead) https://github.com/nexus-devs/wow-classic-items
- Berufe Forever:
  - https://www.wow-professions.com/forever/leatherworking-leveling-guide · https://www.wow-professions.com/forever/enchanting-leveling-guide · https://www.wow-professions.com/forever/disenchanting-guide
  - https://www.wow-professions.com/forever/camping-guide · https://www.wow-professions.com/forever/merchants-favor-durotar-supply-azeroth-commerce · https://www.wow-professions.com/forever/fishing-and-cooking-leveling-guide
  - https://www.icy-veins.com/wow-forever/skinning · https://www.icy-veins.com/wow-forever/herbalism · https://www.icy-veins.com/wow-forever/fishing · https://www.icy-veins.com/wow-forever/cooking
  - https://kami-labs.fr/en/guide-travail-du-cuir-wow-forever/ · https://kami-labs.fr/en/guide-enchantement-wow-forever/
- Essen und XP: https://www.icy-veins.com/wow/news/crafted-food-in-wow-forever-gives-you-5-more-xp-from-kills/ · https://mobalytics.gg/wow-forever/profile/fierce-sun-30v6cf/guides/wow-forever-professions-overview-everything-you-need-to-know
- Daten:
  - https://ahledger.com/wow-forever/zones/mulgore · https://ahledger.com/wow-forever/zones/the-barrens
  - https://metaforge.app/wow-forever/database/creatures · https://seemeta.com/en/wow-forever/professions/cooking
  - https://warcraft.wiki.gg/wiki/Skinning · https://wowpedia.fandom.com/wiki/Skinning
- Beta: https://www.warcrafttavern.com/forever/guides/beta/
- Orgrimmar und Berufswechsel: https://www.icy-veins.com/wow-forever/leatherworking · https://www.icy-veins.com/wow-forever/enchanting · https://www.wow-professions.com/forever/leatherworking-trainers · https://www.wow-professions.com/forever/npc/karolek · https://www.wow-professions.com/forever/npc/godan · https://ahledger.com/wow-forever/npcs/3346-kithas · https://ahledger.com/wow-forever/npcs/3366-tamar · https://ahledger.com/wow-forever/auction-house · https://www.warcrafttavern.com/forever/guides/professions/ · https://www.zockify.com/forever/professions/ · https://ahledger.com/items/247786-mote-of-magic
- Fischen: https://ahledger.com/items/6522-deviate-fish · https://ahledger.com/items/6661-recipe-savory-deviate-delight · https://www.method.gg/wow-forever/savory-whimsyfin-delight-and-savory-deviate-delight-how-to-turn-into-a-pirate-or-ninja-in-wow-forever
- Leder und Gegnerstufen: https://cn.classic.wowhead.com/guides/classic-leather-farming-early-leather · https://metaforge.app/wow-forever/database/trade-goods/medium-hide · https://www.warcrafttavern.com/wow-classic/hunter-pets/violet-raptors/ · https://www.warcrafttavern.com/wow-classic/hunter-pets/golden-lions/ · https://www.warcrafttavern.com/wow-classic/hunter-pets/brown-tallstriders/ · https://www.warcrafttavern.com/wow-classic/hunter-pets/blue-turtles/ · https://www.warcrafttavern.com/wow-classic/hunter-pets/pets/savannah-patriarch/
- Daten-Seiten ohne JavaScript: AHledger, MetaForge (teilweise), SeeMeta, wow-professions, Icy Veins. Wowhead-Forever-Seiten bleiben oft leer.
- AH-Scan: Forever-UI 1.60.1 (70374), `Blizzard_APIDocumentationGenerated/AuctionHouseDocumentation.lua` (`C_AuctionHouse.ReplicateItems`, `GetNumReplicateItems`, `GetReplicateItemInfo`, `REPLICATE_ITEM_LIST_UPDATE`; ReplicateItems ohne `HasRestrictions`) https://github.com/Gethe/wow-ui-source/tree/forever · fertige Scan-Addons für Forever: AHledger https://www.curseforge.com/wow/addons/ahledger (Scan-Knopf, `/ahl scan`, Auto-Scan höchstens alle 15 Minuten, der Knopf zählt bis zur Freigabe durch den Server herunter; Upload an ahledger.com nur mit der Sync-App und «Contribute scans», Stand 12.10.) · auxForever https://www.curseforge.com/wow/addons/auxforever (Full scan, Preisverlauf, Stand 14.10.)
- Testlog 3.6, alles Forever-UI 1.60.1 (70374), https://github.com/Gethe/wow-ui-source/tree/forever: Rezepte `Blizzard_APIDocumentationGenerated/TradeSkillUIDocumentation.lua` und `TradeSkillUITypesDocumentation.lua` (`GetChildProfessionInfo`, `GetBaseProfessionInfo`, `GetRecipeInfo` mit `learned` und `relativeDifficulty` 0–3, `GetRecipeSchematic`, `GetRecipeOutputItemData`), `Blizzard_ProfessionsTemplates/Blizzard_Professions.lua` (`GetFilteredRecipeIDs`) und `Camelot/Blizzard_Professions.lua` (`GetDefaultShowUnlearned` = false); Bank `BankDocumentation.lua` (`FetchPurchasedBankTabData`, `BANKFRAME_OPENED`), `ItemConstantsDocumentation.lua` (`Enum.BankType` Character 0, Account 2), `Blizzard_UIPanels_Game/Camelot/BankFrame.lua`; Post `Blizzard_MailFrame/MailFrame.lua` (`GetInboxHeaderInfo`, `GetInboxInvoiceInfo`, `GetInboxText`), `MailInfoDocumentation.lua` (`MAIL_INBOX_UPDATE`); Auktionshaus `AuctionHouseDocumentation.lua` (`GetReplicateItemTimeLeft`, `GetTimeLeftBandInfo`, `PostCommodity`, `PostItem`, `ConfirmPostCommodity`, `CalculateCommodityDeposit`, `AUCTION_HOUSE_AUCTION_CREATED`), `AuctionHouseEnumsDocumentation.lua` (`Enum.AuctionHouseTimeLeftBand` 0–3; was `GetReplicateItemTimeLeft` liefert, ist ungeprüft, Risiko 24), `Blizzard_AuctionHouseUI/Shared/Blizzard_AuctionHouseCommoditiesSellFrame.lua` und `…ItemSellFrame.lua` (so stellt das UI ein), `…/Blizzard_AuctionHouseFrame.lua` (`AUCTION_HOUSE_AUCTION_CREATED` mit `ERR_AUCTION_STARTED`, `AUCTION_HOUSE_POST_ERROR`); Gegenstände `ItemDocumentation.lua` (`GetItemInfo` mit Händlerpreis und Bindung); Interaktion `PlayerInteractionManagerConstantsDocumentation.lua` (Banker 8, CharacterBanker 67, AccountBanker 68).
- Gebühr 5 % im Auktionshaus: AHledger, Seite «Auction House» https://ahledger.com/wow-forever/auction-house; `tools/markt.py` prüft sie an den eigenen Rechnungen (AH-POST).

---

## 12. Offene Entscheidungen (beim Nutzer)

Stand und Liste: `docs/entscheidungen.md`. Am 13.10. entschieden: Update-Rhythmus «so oft ich kann», LW-Route wählt Claude «nach bestem Wissen und Gewissen». Offen u. a.: welche Widersprüche zuerst im Spiel geprüft werden, welcher AH-Markt zählt, ob beim Kraut die Zusatzbeute mitzählt.

## 13. Änderungen an diesem Dokument

- 13.10.2026: erstellt (Recherche RXP-Code, Forever-UI-Code, Berufsdaten, Machbarkeitsprobe, Testlog v1).
- 13.10.2026: Testläufe 1 und 2 eingetragen, Koordinaten-Befund (Risiko 17), Generator mit Plan-Tabelle, Testlog 2.
- 13.10.2026: Messdaten (Kartenecken Thunder Bluff, Herstellen, Entzaubern), `karte_aus_testlog.py`, Risiko 17 genauer, Ankerstellen nach RXP-Version, Update-Ablauf mit verknüpften AddOns.
- 13.10.2026: Kartenecken Mulgore und Brachland exakt, Risiko 17 mit exakten Werten, Kombi-Guide v0.1.2.
- 13.10.2026: Wie RXP die Stelle nach einem Update wiederfindet (Abschnitt 6); Zauber-Ereignisse des Spielers sind laut Forever-API nicht «secret» (Risiko 13).
- 13.10.2026: Testlog 3 (Herstellen, Entzaubern, Sammeln, Angeln, Beute, Händler, Post, Auktionshaus, Geld, Gelerntes); Gewächshaus (Abschnitt 8).
- 13.10.2026: Recherche Kräuter, Fische, Kochen und Kosten (`docs/recherche/`), Wertvergleich in Abschnitt 9; Risiko 18 entfernt (beruhte auf einem Missverständnis: «Kräuterfarmen», nicht «Kräutergarten»); offene Entscheidungen nach `entscheidungen.md` verwiesen.
- 13.10.2026: Kombi-Guide auf RXP v4.11.23 gebaut (Testlog zeigt v4.11.23 nach dem CurseForge-Update); neue Addon-Ordner brauchen einen Neustart; Teststand T0 und T6.
- 13.10.2026: Testlauf 3, zweiter Abschnitt: Messwerte Kürschnern, Kräuter, Angeln, Lehrer und Geld (§9); Lehrer-Koordinaten gemessen; Berufs-Quests 97933 und 97936 (§5); Risiko 19 und Testlog 3.2; T6-Erwartung neu gerechnet, T7.
- 13.10.2026: Kombi-Guide v0.2 (6-12 Mulgore, Thunder Bluff) mit Mengenmodell; T6 bestanden; Regel «neue Schritte nach der Teststelle» (§6); Berufs-Quests mit Ziel, Abgabe und Belohnung (§5); Karte Orgrimmar exakt; Testlog 3.3; «Gathering Leather» und Simple Wood (§9).
- 14.10.2026: Berufswechsel in Orgrimmar und Sweetspot (§1), Berufe-Plan mit Stufen A–D (§0, §5), Orgrimmar-Lehrer und -Händler, Verlernen, Lernstufen, VZ-Tabs, LW ab 130, Mote of Magic, Fischen im Brachland (§9), Widersprüche 15–20, RXP-Verhalten von `.skill …,<1`, `.itemcount`, Text-Schritten und `.money` (§4), Tests T11 und T12 (§10), Kombi-Guide v0.4 (§5).
- 14.10.2026 (abends): RXP-Stand und Probebau auf dem Hauptzweig (§2, §5, §6), Anker der Plan-Zeile 5, Katzengestalt und neue Druiden-Questreihe (§5), Frilled Lichen, Angelstellen, Erzeugnisse mit Gewinn, Heavy Leather (§9), Risiko 22, Testlog 3.4 mit Lehrerliste und Test T13, Messplan Beta (§0, §10).
- 14.10.2026: RXP-Route bis Stufe 20 gelesen (§5); Mengenmodell bis Stufe 20 mit Bedarf für LW 150 und VZ 150 (§1, §9); Geselle reicht bis 150 (§9); LW-Routen von wow-professions und kami-labs verglichen, Planungsgrundlage gewählt (§9); Gegnerstufen und Leder-Anteile im Brachland (§9); `.goto` ohne Radius, `.xp`, `#maxlevel` (§4); Kombi-Guide v0.3 mit Leder-Zählern und Farm-Stopps (§5); Stellen-Prüfung mit `tools/rxp_schritte.py` (§6); Tests T9 und T10 (§10).
- 15.10.2026: Testlog 3.5 mit AH-Scan (§0, Risiko 23, T15), `tools/ah_aus_testlog.py` und `data/preise/` (§0), T14 (Wechsel zwischen gekauftem Guide und Kombi-Guide), Kurzliste Beta im Messplan, Quellen zum AH-Scan (§11).
- 15.10.2026 (abends): Risiko 23 mit ForeverSVBridge und dem Gegenbeleg vom 13.10. (RXP-Stelle nach dem Neustart), Quelle zum Schreiben der SavedVariables.
- 15.10.2026 (spät): Testlog 3.6 (Rezepte, Bestand, AH-Post, eigene Angebote, Abnahme zwischen zwei Scans, `/tl tipp`), `tools/markt.py` und Addon `KombiDaten` (§0), `data/preise/ah_abnahme.csv`, Risiko 24, Tests T16–T21, Quellen zu Testlog 3.6 und zur Gebühr (§11).
- 15.10.2026 (Nachtrag): `tools/markt.py` mit 30-Tage-Vergleich und strengerem Farm-Tipp (§0); Stellen der Testcharaktere am 15.10. (§6); Messwerte vom 14. und 15.10.: Yonn Deepcut, Kürschnern, Händlerpreis Greater Magic Wand (§9, Widersprüche 1 und 21, T8).
- 15.10.2026 (Nachtrag 2): erster eigener AH-Scan (Risiko 23, T15) in `data/preise/`; Region im Beta-Client leer; Kartenecken Durotar, Tirisfal, Undercity, Östliche Königreiche (§0, Risiko 17); Stelle #103 (§6).
- 15.10.2026 (Nacht): Dungeon-Route: RXPs Forever-Dungeon-Guides (§2), `#beta` und `#xprate` im Guide-Kopf (§3), Dungeons in Forever und RXPs Empfehlung (§4), Kombi-Guide v0.5 mit der Gruppe «Kombiguide Dungeon (H)» und `data/kombi/dungeons.csv` (§0, §5, §6), Risiko 25, T22.
- 15.10.2026 (Nacht, Nachtrag): Messdaten bis 22:01: `/reload` liest die Version aus der `.toc` neu (§5, T22), Stelle #152 und Kennungen nach dem Neubau v0.4.1 (§6), Kartenecken Silberwald (§0, Risiko 17), Teststand T11, T15, T17–T19, T22 (§10).
- 15.10.2026 (Nacht, Nachtrag 2): Lehrerlisten Orgrimmar (§9: Ränge, Kosten, Lernstufen; Widersprüche 3, 4, 16, 17, 20; Risiko 21), Restlaufzeit im AH-Scan (Risiko 24), Kombi-Guide v0.5.1 mit gemessenen Lernstufen und Kosten in den Texten, T13, T20.
- 16.10.2026 (früh, zweite Prüfrunde): Testlog 3.7.1 (§0, Risiko 27, T29–T33), `.maxskill` ohne Ereignis, `.istrained`, Lehrer-Automatik von `.train` (§4, Risiko 28), Kombi-Guide v0.5.3 (§5), Markt mit Essenzen, Angebotsbuch, Sammler-Schritt und Listen (§0), Doku-Befunde der Prüfung eingearbeitet (Angel-Rate 134, `#next` der Dungeon-Gruppe, Kalimdor, 21 Widersprüche, Pfade, `--gruppe`, Tamar, Lernkosten, Teststand); Break-even der Kräuter neu umgerechnet (13–14 bzw. 18–20 Knoten pro Stunde, §9), Build 70425 im UI-Code (Kopf). Prüfbericht: `docs/tests/pruefbericht-2026-10-16.md`.
- 15.10.2026 (spät, Gesamt-Prüfung): Testlog 3.7 (§0, Risiko 27, T23–T27), Addons installiert Claude selbst (§0, §6, T28), Händlerpreise aus dem Forever-Client (§9, Risiko 26), Zauberstäbe und Minor Deflect laut SeeMeta (§9, Widersprüche 17 und 21), Tamar gemessen (§9), Kombi-Guide v0.5.2 (§5), Berufe-Plan mit Lernkosten, Händler statt Entzaubern und Variante Zauberstäbe (§0), Risiko 17 auf v4.11.23 nachgezählt, Kalimdor exakt, Build 70374, `tools/merge_poc.py`, Quellen (§11).
- 16.10.2026: Guide-Wechsel statt Schalter (`#next`, Schritt-`.next`), Dungeon-Quests in RXPs Dungeon-Route mit NPCs und Orten, Questlog-Grösse ungeprüft (§4, Dungeons; für den Switch Solo/Gruppe, offene Entscheidung 36).
- 16.10.2026 (später): Kombi-Guide v0.6 mit Dungeon-Vorquests als Zusatzschritten und dem Abstecher zu den Ruinen von Lordaeron (§0, §5), RXP-Verhalten von `#completewith` (auch Ketten), `#optional`, `.accept`, `.isQuestComplete`, `.zone`, `.zoneskip`, `.abandon`, `.isOnQuest`, Häkchen, Kontinent im `.goto` und `Name::NPC-ID` (§4), RXPs Abbruch-Schritte für Dungeon-Quests in der Speedrun-Route (§4), Dungeon-Vorquests der Horde bis 22 mit Recherche `docs/recherche/2026-10-16_dungeon-vorquests.md` (§4), Stellen-Prüfung wie RXP lädt und `rxp_schritte.py ziele` (§4, §6), Tests T34–T37 (§10). Danach unabhängige Prüfung (`docs/tests/pruefbericht-2026-10-16_vorquests.md`): Pfeil der Zusatzschritte, leere Ziel-Schritte, Quest-Automatik, `.isOnQuest` bei Liefer-Quests, Sprung beim Neuladen mit `#maxlevel` (§4, §5), Mebok-Koordinaten (§4).
- 16.10.2026 (Nachtrag): T28 mit Kombiguide 0.6.1; Checkliste für den Stufe-8-Druiden im Messplan (§0, §10).
- 17.10.2026: Messlauf des Druiden: Build 70450 (Kopf), Cultivation mit 15 Minuten Abklingzeit (§8), Geselle Kürschnerei ab 50 für 5s (§9, Widerspruch 6), Kürschnern und Gekräuselte Flechte in Mulgore, Grober Faden 10c (§9), Risiko 15, Teststand (§10).
- 17.10.2026 (Nachmittag): Commit zu Build 70450 berichtigt (Kopf); RXP zählt nur den eingeloggten Charakter, keine Kontobank in Forever (§4); Pfand und Porto gemessen (§9); Bagnon und andere Taschen-Addons für alle Charaktere (§8); Flechten aus Erdwurzel, Geselle bei Mooranta (§9); Risiken 15 und 24; Teststand (§10); `tools/markt.py` zählt den Bankchar für Stufe A mit (§0).
- 17.10.2026 (Abend): Kombi-Guide v0.6.3 mit «Grundlagen des Zeltens: Angeln» (§0, §5), Klassenzauber des Druiden mit Kosten und RXPs Lehrer-Stellen (§9), Risiko 29 (Gold für die Klassenzauber), `tools/markt.py` mit dem Gold für die Klassenzauber (§0), Händler in Bloodhoof (Angel, Phiolen, Einfaches Holz, Milch), Uthan Stillwater bei der Abgabe, Pfand an 24 Angeboten, Porto je Stapel (§9), Lager-Gegenstände gemessen (§8), Karte Moonglade exakt (§0, Risiko 17), Teststand (§10).
