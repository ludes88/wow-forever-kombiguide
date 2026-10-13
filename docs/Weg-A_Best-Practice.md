# Weg A: Kombi-Guide aus RXP-Route und Berufen – Best Practice

Stand 13.10.2026. Gilt für die Forever-Beta: Client 1.60.1 (Build 70338), RestedXP-Release v4.11.23 (10.10.), RXP-Hauptzweig 9c7aaaf (13.10.).
Zweck: Nachschlagewerk für Claude und den Nutzer. Was steht, ist belegt (Link oder Code-Stelle) oder als **ungeprüft** markiert.

---

## 0. Schnellzugriff

- **Was Weg A ist:** RXPs Gratis-Route für Stufe 1–22 (Mulgore, Brachland) als Kopie, darin unsere Berufsschritte an Ankerstellen. Ein Guide, ein Fenster. Ab 22 wechselt der Nutzer zu seinem gekauften Guide.
- **Wie er geladen wird:** als eigenes kleines Addon (`RXPGuides_KombiGuide`, gebaut von `tools/build_kombi.py`), das `RXPGuides.RegisterGuide([[ … ]])` aufruft. Das Import-Fenster von RXP nimmt nur verschlüsselte, kontogebundene Texte. Im Spiel bestätigt am 13.10. (Testlauf 1 und 2, `docs/tests/`).
- **Pflicht im Kopf jedes Guides:** `#forever`, `#name`, `#group`, `<< Horde`. Ohne `#forever` lädt RXP den Guide in Forever nicht.
- **Eigene Gruppe:** `#group Kombiguide (H)`. Keine Gruppe/Name-Kombination doppelt mit RXP.
- **Update-Ablauf:** RXP-Version aus dem Testlog lesen → genau diesen Tag holen → Skript mischt neu → statische Prüfung → Pull Request und Merge → beim Nutzer `aktualisieren.bat` und `/reload` (AddOns sind mit dem Repo verknüpft, `docs/vorgehen.md`) → der Nutzer testet.
- **Testlog:** `/tl <Text>`, `/tl bug <Text>`, `/tl zeigen`. Datei: `WTF\Account\<KONTO>\SavedVariables\KombiTestlog.lua`. Version 3 schreibt zusätzlich von selbst: HERSTELLEN, ENTZAUBERN, SAMMELN, ANGELN, BEUTE, HÄNDLER, POST, AUKTIONSHAUS, GELD, GELERNT, REZEPT (Liste im Kopf von `KombiTestlog.lua`).
- **Werkzeuge im Repo:** `tools/build_kombi.py` (Kombi-Guide aus `data/kombi/plan.csv` bauen und prüfen), `tools/validate.py` (Guide prüfen), `tools/testlog_harness.py` (Testlog-Probe), `tools/karte_aus_testlog.py` (Kartenecken aus dem Testlog übernehmen und RXP dagegen prüfen), `tools/fetch_rxp.sh` (RXP in einer Version holen).
- **Koordinaten:** eigene Orte in Spielkoordinaten; umgerechnet über `data/karten/forever_karten.csv`. RXPs Kommentar-Koordinaten (`--c:`) passen in Mulgore nicht zur Forever-Karte, in Thunder Bluff und im Brachland genau (Abschnitt 7, Risiko 17). Exakt gemessen: Mulgore, Brachland, Thunder Bluff.

---

## 1. Ziel und Rahmen

- Der Nutzer startet neu als Tauren-Druide in Mulgore und levelt mit RestedXP (RXP).
- Berufsplan (Entscheidung des Nutzers, siehe `docs/entscheidungen.md`): Kräuterkunde und Kürschnerei bis etwa Stufe 15, dann Wechsel auf Lederverarbeitung (LW) und Verzauberkunst (VZ), Ziel je 150. Fischen und Kochen laufen nebenher.
- Mengen aus der Rechnung vom 13.10. (Chat, Teil 2):
  - 416 Leichtes Leder für LW 125 und VZ im Mittel 125
  - 488 für VZ 130 mit 90 % Sicherheit
  - 644 für VZ 150 mit 90 % Sicherheit
  - dazu 100 Ruined Leather Scraps, 27 Light Hide, 10 Medium Hide
- Leitsatz des Nutzers: nicht «farme 650 Leder» als Block, sondern pro Gebiet so viel, wie dort effizient geht, dann weiter im Takt der Route.

---

## 2. Was RXP gratis und offen hat

**Quelle:** https://github.com/RestedXP/RXPGuides (Lizenz CC BY-NC-SA 4.0, Datei `LICENSE`).

| Datei | Guides darin | Gruppe |
|---|---|---|
| `Guides/forever/Horde-1-12_Mulgore.lua` | 1-6 Mulgore (62 Schritte), 6-12 Mulgore (275) | RestedXP Forever Guide (H), Untergruppe «Speedrun Guide 1-22», `#defaultfor Tauren` |
| `Guides/forever/Horde-12-22_Barrens.lua` | 12-17 The Barrens (399), 17-22 Stonetalon/Barrens/Ashenvale (460) | dito; `#next 22-24 Hillsbrad` zeigt auf den gekauften Teil |
| `Guides/Forever/dungeon/*.lua` | Dungeon-Varianten | RestedXP Forever Dungeon Guide (H) |
| `Guides/forever/RestedXP-Skyborne.lua` | neues Startgebiet Zephras Isle | – |

- Schrittzahlen gezählt in Release v4.11.23, mit Klassen-Varianten.
- Laut kami-labs (09.10.) sind Stufe 1–20 für alle gratis. Der volle Guide kostet 45 USD für beide Fraktionen oder 30 USD für eine. Die Forever-Routen 1–35 sind fertig, für 35–60 nutzt RXP vorerst die Era-Routen. https://kami-labs.fr/en/wow-forever/mise-a-jour-restedxp-wow-forever/
- Der gekaufte Teil kommt als Import-Text, der verschlüsselt und an das Konto gebunden ist (Code: `GuideLoader.lua`, Funktion `CheckDataIntegrity` ab Zeile 274; Meldung «Account mismatch»). Den können und wollen wir nicht lesen.

**Update-Takt (Git-Historie, gemessen am 13.10.)**
- 276 Commits an den Forever-Guides seit 17.09.
- 31 Commits an den zwei Horde-Dateien, die wir mischen, an 22 von 27 Tagen.
- Releases: v4.11.14 (03.10.) bis v4.11.23 (10.10.), also 10 Releases in 8 Tagen. Der Hauptzweig ist dem letzten Release voraus.
- Umfang in den zwei Horde-Dateien: v4.11.14 → v4.11.23 +424/−181 Zeilen; v4.11.23 → Stand 13.10. +181/−48 Zeilen.
- `#version` bleibt dabei bei 11. Taugt nicht als Änderungsmerkmal; massgebend ist die Addon-Version (Tag).

---

## 3. Wie RXP Guides lädt (Code-Fakten, Stand 9c7aaaf)

- **Registrieren:** `RXPGuides.RegisterGuide(text)` (`GuideLoader.lua` ~L416, global gesetzt ~L1269). Vor dem Laden landen Guides in einer Warteschlange.
- **Kopf-Prüfung beim Laden** (`LoadGuide`, ~L542–640):
  - Der Kopf (alles vor dem ersten `step`) muss `#FOREVER` enthalten (Gross/klein egal), sonst wird der Guide in Forever deaktiviert.
  - `<< Horde` setzt `enabledFor`.
  - `#name` und `#group` sind Pflicht.
  - Gibt es Gruppe und Name schon, meldet RXP «Error trying to load a guide already parsed».
- **Spielversion** (`ParseGuide`, ~L1046): `#classic` gilt auch in Forever. `#forever` zählt nicht als Spieltag, beschränkt also nichts.
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

---

## 5. Aufbau von Weg A

**Dateien beim Spieler**
- `Interface\AddOns\RXPGuides_KombiGuide\` mit `.toc` (`## Interface: 16001`, `## Dependencies: RXPGuides`) und `Kombi_Guide.lua`, gebaut von `tools/build_kombi.py`.
- `Interface\AddOns\RXPGuides_Kombi\` nur für den WC-Test (Testlauf 1).
- `Interface\AddOns\KombiTestlog\` für Notizen und Protokoll.
- Ordner der Beta: `World of Warcraft\_classic_beta_\` (kami-labs, 10.10.; beim Start am 04.11. **ungeprüft**).

**Mischen (Skript)**
1. RXP-Release holen, das der Nutzer installiert hat (Tag aus dem Testlog).
2. `RegisterGuide`-Blöcke trennen: Kopf und Schritte.
3. Kopf anpassen:
   - `#group Kombiguide (H)`
   - `#defaultfor` entfernen (sonst konkurrieren zwei Standard-Guides)
   - letztes `#next` → `RestedXP Forever Guide (H)\22-24 Hillsbrad`
4. Berufsschritte an Ankern einfügen. Ein Anker ist eine eindeutige Zeile, z. B. `.turnin 768`, ein `#label` oder eine Quest-ID.
   - Ein Anker muss genau einmal vorkommen, sonst bricht das Skript ab und meldet es.
   - Nie zwischen einen Schritt mit `#completewith next` und seinen Nachfolger einfügen. Das Skript schiebt die Einfügestelle weiter.
   - Berufsschritte bekommen Bedingungen, damit sie ohne den Beruf verschwinden (`.skill leatherworking,<1,1`).
   - Käufe im AH bekommen `#ah`.
5. Herkunft und Lizenz in den Dateikopf schreiben.
6. Prüfen:
   - Lua-5.1-Syntax
   - jeder Befehl existiert in `functions.lua`
   - Kopf-Pflichtfelder vorhanden
   - Anker gefunden
   - Schrittzahl = RXP plus eingefügte Schritte
7. ZIP für den Chat, Textdateien in den Projektordner.

**Machbarkeitsprobe vom 13.10.** (`werkzeuge/merge_poc.py`, Basis v4.11.23)
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
  4. Der Nutzer ersetzt die Datei (bei verknüpften AddOns: `aktualisieren.bat`). Der Fortschritt bleibt, solange Gruppe und Name gleich sind; die Stelle kann sich aber verschieben (nächster Punkt).
- **Wie RXP die Stelle wiederfindet** (Code v4.11.23): Pro Guide speichert RXP die Schrittnummer und eine Schritt-Kennung aus der Zeilennummer im Guide-Text (`stepId = linenumber + guide.guideId`, `GuideLoader.lua` L1090). Beim Laden sucht es zuerst diese Kennung, sonst nimmt es die Nummer (`GuideWindow.lua` L1894–1901).
  - Ändert ein Neubau nur Koordinaten (gleiche Zeilen, z. B. v0.1.1 → v0.1.2), bleibt die Stelle genau.
  - Ändert sich die Route (andere Zeilen, z. B. Neubau auf einer neueren RXP-Version), kann RXP an einer anderen Stelle stehen. Erledigte Schritte überspringt RXP selbst (Testlauf 2); liegt die Stelle zu weit vorne, hilft die Schrittliste. Im Spiel **ungeprüft** (Test T6).
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
| 7 | Quellen widersprechen sich (14 Punkte, Abschnitt 9) | Falsche Koordinate oder Stufe | Im Spiel prüfen, Befund ins Testlog |
| 8 | Einschub zerreisst `#completewith next` | Schritt hängt | Skript-Regel; Test T3 |
| 9 | Zwei ähnliche Guides in der Liste, RXP wählt beim neuen Charakter seinen eigenen | Falscher Guide aktiv | Einmal von Hand wählen; `#defaultfor` bei uns entfernt |
| 10 | `#next` in den gekauften Guide greift nicht | Bei 22 kein automatischer Wechsel | Von Hand wählen; Test T5 |
| 11 | Deutscher Client | Eigene Texte gemischt mit englischen Ortsnamen | Eigene Texte ohne ungeprüfte Eigennamen; Quest- und NPC-Namen kommen von RXP/Client |
| 12 | Lizenz CC BY-NC-SA 4.0 | Nur nicht-kommerziell, mit Herkunft, gleiche Lizenz | Hinweis in jeder Datei; nie verkaufen oder kommerziell verteilen |
| 13 | «Secret values» im modernen Client (Forever nutzt die Mainline-Vorlagen) | Chat-Text kann für Addons gesperrt sein (`CHAT_MSG_LOOT` ist nicht «NeverSecret») | Testlog zählt über Taschenbestand statt Chat; Abfrage `issecretvalue`. Zauber-Ereignisse wie `UNIT_SPELLCAST_SUCCEEDED` sind laut Forever-API nur für fremde Einheiten «secret», nicht für den Spieler und seinen Begleiter; einzelne Zauber können abweichen (`SecretPredicatesDocumentation.lua`, `SecretWhenUnitSpellCastRestricted`) |
| 14 | Leder pro Stunde unbekannt | Farmmengen pro Gebiet nur geschätzt | Testlog 3: `SAMMELN` (Quelle mit Kreatur- oder Objekt-ID und Beute), `BEUTE`, `ANGELN` mit Ort und Zeit auswerten |
| 18 | Gewächshaus («Kräutergarten») ist ein Lager-Gegenstand der Kräuterkunde (Warcraft Tavern); der Plan sieht vor, Kräuterkunde um Stufe 15 abzulegen | Gewächshaus womöglich nicht nutzbar. **Ungeprüft:** ob Pflanzen und Ernten Kräuterkunde brauchen | Vor dem Verlernen klären; Bauplan kommt erst aus einem Wetlands-Dungeon (Abschnitt 8) |
| 15 | Platz für 400–650 Leder | Taschen voll | Leinentaschen, Bankchar, Apprentice's Skinning Satchel (Abschnitt 8) |
| 16 | Kiste «40 Linen Cloth» lässt sich nicht füllen (Stapel 20) | Merchant's Favor fehlt | Variante 20 Leichtes Leder nutzen (allthings.how, Mobalytics) |
| 17 | RXPs Kommentar-Koordinaten (`--c:Zone,x,y`) passen nicht überall zur Forever-Karte. Mulgore ist in Forever 6154 × 4102 Yards gross; 442 RXP-Punkte weichen im Median 3,5 % ab, höchstens 11,3 %. Thunder Bluff (26 Punkte) und Brachland (18 Punkte) passen genau (Messung 13.10., `docs/tests/messdaten-2026-10-13.md`) | Eigene Pfeile lagen bis 35 Yards daneben (v0.1) | Spielkoordinaten plus Kartenecken (`forever_karten.csv`); exakte Ecken aus Testlog-Eintrag `KARTE` (`C_Map.GetWorldPosFromMapPos`, `C_Map.GetMapWorldSize`, beide in der Forever-API 1.60.1), übernommen mit `tools/karte_aus_testlog.py`. Exakt: 1412 Mulgore, 1413 Brachland, 1456 Thunder Bluff |

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
- **Gewächshaus (Greenhouse), vermutlich der «Kräutergarten» des Nutzers:**
  - Kräuterkunde stellt im Lager-System Incense Candles, Greenhouses und Seed Hybridizers her (Warcraft Tavern, Herbalism Overview).
  - Bauplan: Boss Shadetooth im Dungeon «Excavation Site: Wetlands» (Icy Veins, 08.10.). Stufe des Dungeons: **ungeprüft**.
  - Wird beim Lagerplatz aufgestellt und erzeugt einen Pflanzkasten. Ein Samen pro Gewächshaus: Das Kraut ist nach 8 Minuten erntbar, das Gewächshaus hält 15 Minuten (Icy Veins).
  - Samen: Commonplace (Peacebloom, Earthroot), Uncommon (Silverleaf, Kingsblood), Scarce (Ghost Shroom); Kräuterkundige finden Samen beim Sammeln. Seed Hybridizer ab Kräuterkunde 300 (Icy Veins).
  - **Ungeprüft:** ob Pflanzen und Ernten Kräuterkunde brauchen, wie viele Kräuter eine Ernte gibt.
  - Quellen: https://www.icy-veins.com/wow-forever/news/greenhouse-blueprint-found-how-herbalism-seeds-work-in-wow-forever/ · https://www.warcrafttavern.com/forever/guides/herbalism/
- **Tauren-Rasse «Cultivation»:** dupliziert ein Kraut, das man ohne Kräuterkunde ernten kann. Abklingzeit 1 Stunde; nötige Stufe = Kraut-Stufe / 5 (Warcraft Tavern, SeeMeta 10.10.). Damit gibt es Kräuter auch nach dem Verlernen.
- **Merchant's Favor:**
  - Die erste Shipping-Label-Quest gibt 50.
  - Kisten droppen ab Stufe 10. «Apprentice Textiles» fällt zum Beispiel bei Stormsnout in 9 % von 23 Beute-Fenstern (AHledger).
  - Bündel: 20 Leichtes Leder ergeben 5 Favor. 2 Cured Light Hide ergeben 10 (Apprentice Fabrics). Cured Light Hide stellt LW auf Stufe 30–55 ohnehin her.
- **Apprentice's Skinning Satchel:** 4 Plätze, Taschentyp Leatherworking Bag, 25c. Gibt es bei Kuruk und Shadi Mistrunner in Thunder Bluff und bei Kawnie Softbreeze in Camp Narache (AHledger, 13.10.).
- **Testlog-Daten** ergeben Leder und XP pro Stunde je Gebiet. Daraus werden die Farmmengen pro Gebiet.

---

## 9. Berufsdaten für Mulgore und Brachland

Tags: [Forever] = Quelle zu Forever, [Classic] = Classic-Daten. **Ungeprüft** heisst: keine Quelle gefunden.

**Lehrer (Horde)**

| Beruf | Wer, wo | Koordinaten | Quelle |
|---|---|---|---|
| Kürschnerei | Nawka Wildsong, Camp Narache (bis 75) | 44.6 76.8 (Icy Veins) / 44.4, 76.8 (kami-labs) | [Forever] |
| Kürschnerei | Yonn Deepcut, Bloodhoof, Great Tent | **Widerspruch:** 45.6 57.8 / 45.0, 61.4 | [Forever] |
| Kürschnerei | Mooranta, Thunder Bluff | 44.43, 43.19 (RXP) | [Forever] |
| Kräuterkunde | Garan Sunstrider, Camp Narache (bis 75) | 44.2 77.8 | [Forever] |
| Kräuterkunde | Komin Winterhoof, Thunder Bluff | 49.8 39.8 | [Forever] |
| LW | Chaw Stronghide, Bloodhoof (Apprentice) | 45.0 61.4 | [Forever] |
| LW | Mak / Tarn / Una, Thunder Bluff (Apprentice/Journeyman/Expert) | 42.2 43.2 / 42.4 43.0 / 41.4 42.6 | [Forever] |
| LW | Krulmoo Fullmoon, Camp Taurajo (Journeyman) | 44.8 59.4 | [Forever] |
| VZ | Mot / Teg Dawnstrider, Thunder Bluff (Apprentice/Journeyman) | 45.0 38.4 / 45.0 38.0 | [Forever] |
| VZ | Hgarth, Sun Rock Retreat (Expert) | 49.2 57.2 | [Forever] |
| Fischen | Uthan Stillwater, Stonebull Lake | 44.6 60.6 | [Forever] |
| Fischen | Kah Mistrunner, Thunder Bluff | 56.0 46.8 / 56.13, 46.39 (RXP) | [Forever] |
| Kochen | Pyall Silentstride, Bloodhoof, Great Tent | 45.0 61.6 | [Forever] |
| Kochen | Aska Mistrunner, Thunder Bluff | 51.0 52.8 | [Forever] |
| Kochen | Duhng, bei den Crossroads | 55.2 31.8 | [Forever] |

Quellen: wow-professions (Trainer-Seiten Skinning, Herbalism, LW, VZ, Fishing, Cooking), Icy Veins (Seiten zu den Berufen, 29.09.–11.10.), kami-labs (08.10.), RXP-Mulgore-Guide.

**Rang-Grenzen**
- LW und VZ: Journeyman ab Fertigkeit 50 und Stufe 10; Expert ab 125 und Stufe 20, kostet 50s; Artisan ab 200 und Stufe 35 [Forever, wow-professions].
- Kürschnerei: laut wow-professions ohne Stufen-Voraussetzung (50/125/200). **Widerspruch:** RankedBoost nennt 75/150/225.
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
- Tiere auf der RXP-Route:
  - Mulgore: Plainstrider, Battleboar, Prairie Wolf, Swoop, Flatland Cougar, Prairie Stalker, Elder Plainstrider, Prairie Wolf Alpha, Taloned Swoop, Flatland Prowler
  - Brachland: Plainstrider-Arten, Zhevra, Sunscale-Raptoren, Savannah-Katzen, Stormsnout, Thunderhead, Oasis Snapjaw
- Stufen [Classic, Wowhead]:
  - Mulgore: Plainstrider 1–2, Prairie Wolf 5–6, Prairie Stalker 7–8, Swoop 7–9, Prairie Wolf Alpha 9–10
  - Brachland: Greater Plainstrider 11–12, Zhevra Runner 13–14, Savannah Prowler 14–15, Sunscale Scytheclaw 16–18, Stormsnout 18–19, Thunderhead 20–21
- Ob Oasis Snapjaw kürschnerbar ist, ist offen. Die Beute bei AHledger enthält Leichtes Leder, sie ist aber nicht als Kürschnerei markiert.

**Kräuter** [Forever, Icy Veins 11.10.]
- Peacebloom 1, Silverleaf 1, Earthroot 15, Mageroyal 50, Briarthorn 70, Stranglekelp 85, Bruiseweed 100, Wild Steelbloom 115.
- **Widerspruch** bei Bruiseweed: warcraft.wiki.gg nennt 85.
- Neu in Forever: Frilled Lichen als seltener Zusatz, unter anderem aus Briarthorn im südlichen Brachland (16 % von 51 Beute-Fenstern, AHledger).

**Entzaubern** [Forever, wow-professions Disenchanting Guide]
- Grüne Rüstung: 75 % Staub, 20 % Essenz. Grüne Waffen: 20 % Staub, 75 % Essenz. Splitter 3–5 %.
- Zeile «11–15»: 2–3 Strange Dust, 1–2 Greater Magic Essence, Small Glimmering Shard.
- Messung 13.10. (15 Zugänge, Art der Teile unbekannt): 8× Staub, 6× Essenz, 1× Splitter; Mengen wie in der Zeile «11–15». 9 Greater Magic Essence ergaben 27 Lesser Magic Essence (1 : 3). Details: `docs/tests/messdaten-2026-10-13.md`.

**Fischen und Kochen** [Forever]
- In Startgebieten entkommen ab Fertigkeit 25 keine Fische mehr, in Hauptstädten ab 75 (wow-professions).
- Stellen: Stonebull Lake für 1–75, Teich in Thunder Bluff für 75–130. An der Lushwater Oasis gibt es auch Deviate Fish (AHledger).
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

**Händler für Berufsmaterial** [Forever, AHledger]
- Nata Dawnstrider (Thunder Bluff): Copper Rod 1s 24c, Mote of Magic 10c, Simple Wood 38c. **Widerspruch:** MetaForge führt dort keine Motes.
- LW-Bedarf:
  - Yonada (Camp Taurajo): Coarse Thread 10c, Fine Thread 1s, Gray Dye 3s 50c, Salt 50c
  - Mahu (Thunder Bluff), Tari'qa (Crossroads), Wunna Darkmane (Bloodhoof)
- Koordinaten dieser Händler: **ungeprüft**.

**Merchant's Favor (Horde)** [Forever]
- Fraktion: Durotar Supply and Logistics. Lager vor dem Westtor der Crossroads, Abgabe bei Dokimi.
- **Widerspruch** bei den Koordinaten: 50.1, 29.3 (Mobalytics) / 42, 34 (Overgear).

**LW-Route 1–150:** wow-professions und kami-labs unterscheiden sich, siehe Projekt-Rechnung und die Links in Abschnitt 11. Die Wahl ist offen.

**Alle 14 Widersprüche zwischen den Quellen** (Recherche 13.10., im Spiel zu prüfen)
1. Koordinaten Yonn Deepcut (Kürschnerei, Bloodhoof)
2. Koordinaten Mooranta (Kürschnerei, Thunder Bluff), drei Quellen
3. LW-Ränge: kami-labs gegen wow-professions und Icy Veins
4. VZ-Ränge und Koordinaten von Mot, Teg und Hgarth
5. Stufen-Voraussetzung Kräuterkunde: wow-professions gegen Icy Veins
6. Ab wann Kürschnerei-Journeyman: RankedBoost gegen die anderen
7. Bruiseweed: Fertigkeit 85 oder 100
8. Flint and Tinder für Lagerfeuer nötig oder nicht
9. Geben versiegelte Kisten Ruf oder nicht
10. Lager von Durotar Supply bzw. Koordinaten Dokimi
11. XP-Bonus bei allem gekochten Essen oder nur bei den meisten
12. Dedicated Study bei voller Fertigkeit: 3 oder 2–4 Essenzen
13. LW- und VZ-Route 1–150: wow-professions gegen kami-labs
14. Untergrenze Leichtes Leder: Gegnerstufe 1 oder 5

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

Stand 13.10.2026 (Testlauf 1 und 2, Messdaten, `docs/tests/`):
- **T0** bestanden, auch mit Testlog 2 und den verknüpften AddOns (SITZUNG meldet «Kombiguide 0.1.1-v4.11.13»).
- **T1** bestanden: Gruppe sichtbar, Wechsel 1-6 → 6-12 innerhalb «Kombiguide (H)».
- **T2** teilweise: Schritte am richtigen Ort, Pfeil zu Nawka rund 28 Yards daneben (v0.1). v0.1.2 zielt mit den exakten Kartenecken auf die gemessene Stelle. Im Spiel nur mit einem Charakter ohne Kürschnerei prüfbar, sonst überspringt RXP den Schritt.
- **T4** indirekt: Ein schon gelernter Beruf wird übersprungen.
- **T7** teilweise: BERUF, RXP, QUEST und TOD laufen; TASCHE zählt Herstellen und Entzaubern, noch ohne Kürschner-Daten; KARTE läuft (Thunder Bluff).
- **T3, T5, T6, T8** offen.

---

## 11. Quellen

- RXP: https://github.com/RestedXP/RXPGuides · https://community.restedxp.com/?p=586526 · https://kami-labs.fr/en/wow-forever/mise-a-jour-restedxp-wow-forever/ · https://kami-labs.fr/wow-forever/installer-restedxp-wow-forever/
- Blizzard-UI-Code Forever 1.60.1 (70338): https://github.com/Gethe/wow-ui-source/tree/forever
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
- Daten-Seiten ohne JavaScript: AHledger, MetaForge (teilweise), SeeMeta, wow-professions, Icy Veins. Wowhead-Forever-Seiten bleiben oft leer.

---

## 12. Offene Entscheidungen (beim Nutzer)

1. Update-Rhythmus: (a) bei Bedarf, (b) wöchentlich, (c) einfrieren und zum Start neu mischen.
2. LW-Route: wow-professions oder kami-labs.
3. Welche Widersprüche zuerst im Spiel geprüft werden.

## 13. Änderungen an diesem Dokument

- 13.10.2026: erstellt (Recherche RXP-Code, Forever-UI-Code, Berufsdaten, Machbarkeitsprobe, Testlog v1).
- 13.10.2026: Testläufe 1 und 2 eingetragen, Koordinaten-Befund (Risiko 17), Generator mit Plan-Tabelle, Testlog 2.
- 13.10.2026: Messdaten (Kartenecken Thunder Bluff, Herstellen, Entzaubern), `karte_aus_testlog.py`, Risiko 17 genauer, Ankerstellen nach RXP-Version, Update-Ablauf mit verknüpften AddOns.
- 13.10.2026: Kartenecken Mulgore und Brachland exakt, Risiko 17 mit exakten Werten, Kombi-Guide v0.1.2.
- 13.10.2026: Wie RXP die Stelle nach einem Update wiederfindet (Abschnitt 6); Zauber-Ereignisse des Spielers sind laut Forever-API nicht «secret» (Risiko 13).
- 13.10.2026: Testlog 3 (Herstellen, Entzaubern, Sammeln, Angeln, Beute, Händler, Post, Auktionshaus, Geld, Gelerntes); Gewächshaus (Abschnitt 8, Risiko 18).
