# Prüfbericht Kombi-Guide 0.6 (Dungeon-Vorquests), unabhängige Prüfung vom 16.10.2026

Am Repo hat der Prüfer nichts geändert. Seine Hilfsskripte (Stelle beim Laden nachbilden, Neuladen mit Stufe 18 simulieren, RXP-Schritte mit `#completewith next` auf einen V-Schritt suchen, Koordinaten umrechnen) liegen nicht im Repo.

## Quellen

**RXP v4.11.23**, die beim Spieler installierte Version:
- `GuideWindow.lua`:
  - `UpdateStepCompletion`: https://github.com/RestedXP/RXPGuides/blob/v4.11.23/GuideWindow.lua#L670-L746
  - `SetStep` L748–888 (klebende Schritte vor dem aktuellen zuerst: L828–858)
  - `LoadGuide`, Stelle über die Kennung, sonst über die Nummer: L1894–1902
  - «sticky»: L1969; Labels: L1982; Häkchen: L235–247
- `map.lua`: Wegpunkte in Schrittreihenfolge L720, `updateArrowData`/`SetArrowWP` L1023–1146, Pfeil in Instanzen aus L1258–1260.
- `functions.lua`:
  - `goto` (`…,0,0` ergibt lowPrio): L1899–1998
  - `xp`: L3306–3428; `abandon`: L4065–4137
  - `isQuestComplete`: L4320–4358; `isOnQuest`: L4367–4408
  - `zone`: L4642–4671; `zoneskip`: L4714–4750
  - `IsQuestComplete` ruft `C_QuestLog.IsComplete` auf: L405–420
- `RXPGuides.lua`: `LevelCheck` L2658–2664; `PLAYER_LEVEL_UP` lädt den Guide nicht neu, L1885–1901.
- `GuideLoader.lua`: Kommentare L989, Zeilenzählung L1041–1042, `stepId` L1090.
- `SettingsPanel.lua`, Standardwerte: `enableQuestAutomation = true` L132, `enableXpStepSkipping = true` L139, `questLogSize … FOREVER and 40` L158.
- Guides:
  - `Guides/forever/Horde-1-12_Mulgore.lua`: RFCPickups1 L2172, Sprungpfad Hunter Rise L2267–2272, WildManeTurnIn L2313, `.isQuestComplete 99082` L1980.
  - `Guides/forever/Horde-12-22_Barrens.lua`: `.turnin 5722` bei Maur L593, `.isOnQuest 5724` L692/710/741, ZamahTurnin L4538, DeathDUPpickup L4579–4581, Abbruch-Schritte L2770–2782, L5298–5313, L6582.
  - `Guides/Forever/dungeon/Horde-12-22_Barrens.lua`: Sputtervalve/Mebok/Drohn L3902–3913.
- Hauptzweig fe936eea: `Guides/Forever/dungeon/Alliance-11-20.lua`, Wappen 95189 mit `.isOnQuest`, L1744–1748.

**Repo:**
- `data/kombi/vorquests.csv`
- `addons/RXPGuides_KombiGuide/Kombi_Guide.lua`
- `tools/build_kombi.py`, `tools/rxp_schritte.py`
- `docs/recherche/2026-10-16_dungeon-vorquests.md`

**Testlog:** Datei vom 15.10. (22:16), nur lokal, nicht im Repo; ohne Namen ausgewertet.

**Web**, Stichprobe zu V10:
- [Icy Veins, News vom 12.09.2026: «Levels 15–20»](https://www.icy-veins.com/wow/news/these-are-warcraft-forevers-new-leveling-dungeons/)
- [Icy Veins, Guide zu den Ruinen von Lordaeron, Stand 23.09.2026: «Level 15-20»](https://www.icy-veins.com/wow-forever/ruins-of-lordaeron-guide)
- [Icy Veins, Quests der Ruinen von Lordaeron, Stand 30.09.2026: nur Mindeststufen, keine Spanne](https://www.icy-veins.com/wow-forever/ruins-of-lordaeron-quests)

## Kurzfassung

- Der Bau ist reproduzierbar und Byte für Byte gleich dem Repo, auch auf `main`.
- «Kombiguide Dungeon (H)» ist in allen vier Blöcken Zeichen für Zeichen gleich wie in a210061, ebenso «1-6 Mulgore» in «Kombiguide (H)».
- Die Stellen #45 und #152 halten für den Druiden. Ich habe das auch gegen die Versionen geprüft, mit denen die Charaktere laut Testlog zuletzt gespeichert haben.
- In Ordnung sind: Koordinaten, Abbruch-Schritte, Voraussetzungen und Syntax-Fallen.
- Zwei schwere Befunde (H1, H2) und eine Pfeil-Übernahme durch Zusatzschritte (M1).

## Befunde nach Schwere

### H1 – V32 (Zamah, Quest 962) erscheint praktisch nie (belegt)

Fundstelle: `Kombi_Guide.lua` L7570, `vorquests.csv` Zeile 24.

**Was passiert:**
- V32 hat `#completewith next`. Der nächste gezeigte Schritt ist bei Druide, Krieger, Jäger, Schurke, Schamane, Hexenmeister und Paladin RXPs «DeathDUPpickup». Das ist nur `#optional` mit einem Label, ohne Elemente.
- Ein Schritt ohne Elemente ist sofort erledigt (`UpdateStepCompletion` L679–688, L731–740). Danach ist der aktuelle Schritt grösser als das Ziel, und V32 gilt als erledigt (L707–710, L727–730).
- Damit ist V32 nur für einen Aktualisierungstakt sichtbar. Auch RXPs Auto-Annahme greift nicht mehr.
- Nur Priester und Magier haben vorher noch einen Klassen-Schritt (Druide: V32 #94, dann gleich DeathDUPpickup #95).
- T36 («Zamah nach der Abgabe von 853») schlägt deshalb fehl. `ziele` meldet es nicht.

**Vorschlag:**
- `bis` auf ein späteres Label setzen, z. B. `KombiV34` (Thunder Bluff, vor der Elder Rise). Das Label zählt auch dann, wenn V34 übersprungen wird.
- Dazu `radius` `0,0`, sonst zieht V32 den Pfeil durch die ganze Berufssitzung in Thunder Bluff.

### H2 – `#maxlevel 17`: Neuladen nach Stufe 18 im Abstecher lässt RXP zu weit springen (Code belegt, simuliert; ob es eintritt, ist ungeprüft)

**Was passiert:**
- RXP blendet `#maxlevel`-Schritte nur beim Laden aus; beim Stufenaufstieg lädt es nicht neu.
- Fall: Der Charakter war beim Laden höchstens 17. Er steht auf V17 oder einer der Abgaben V18–V23 und lädt nach dem Aufstieg auf 18 neu (`/reload` oder neu einloggen).
- Dann ist seine gespeicherte Zeile nicht mehr unter den gezeigten Schritten, und RXP nimmt die Nummer.

**Beispiel Druide:**
- V17 ist #150. Nach dem Laden steht er auf #150 «Accept Chol'aruk» statt auf #143 «FoodandWater2».
- Bei V17 fallen 7 Route-Schritte weg: Wirt in den Crossroads, Abgaben 869, 848, 867, 870, 903, Annahmen 899/4921.
- Bei V18–V23 sind es 8 bis 12 Schritte. Krieger, Jäger und Schamane verhalten sich gleich (`stufe18.py`).
- Entscheid 37 beschreibt nur, dass die Abstecher-Schritte verschwinden, nicht diesen Sprung.

**Wie plausibel:**
- Am 15.10. ging der Abstecher von Stufe 16 (39 %) bis 17 (64 %), mit einem `/reload` mitten im Dungeon (Testlog 20:58).
- `/reload` am Rundenende gehört laut `docs/vorgehen.md` zum Ablauf.

**Vorschlag (Entscheid beim Nutzer, Punkt 37):**
- (a) Hinweis in V17 und in T35 aufnehmen.
- (b) Sobald der Stufe-18-Charakter 0.6 einmal geladen hat, `#maxlevel 17` durch eine wirkungslose Zeile ersetzen, z. B. `#maxlevel 60`. Die Zeilenzahl bleibt gleich, und RXP findet die Stelle über die Kennung. Im Spiel ungeprüft.
- (c) Die Grenze ganz streichen, wenn der Charakter keine Rolle mehr spielt.

### M1 – Zusatzschritte ohne `0,0` übernehmen den Pfeil (belegt)

RXP zeigt den Pfeil auf das erste Ziel in den aktiven Schritten, und klebende Schritte stehen vor dem aktuellen (SetStep L828–858, `SetArrowWP`). Bis man die Quest annimmt oder abhakt, zeigt der Pfeil also auf den Zusatzschritt:
- **V1** (6-12 #177): von Cairne bis WildManeTurnIn. Er zeigt auf die Elder Rise statt auf RXPs Sprungpfad von der Hunter Rise. RXP schreibt dort «Follow the arrow precisely to avoid dying» (Mulgore L2267–2272).
- **V2/V3** (12-17 #109/#110): während der ganzen Berufssitzung in Orgrimmar (nur mit Kürschnerei) und beim Zeppelin-Schritt V10. Der Pfeil zeigt auf Thrall statt auf den Zeppelin-Turm.
- **V41** (#182): beim Sammeln südlich von Ratchet bis LeaveRatchet.
- **V42** (#214): auf dem Weg zur Oase und in der Hezrul-Schleife.

Nicht betroffen: V30, V31, V33, V36 (der Spieler steht beim NPC), V11–V17 (gewollt), V15 und V24 (schon `0,0`).

**Vorschlag:** `radius` `0,0` für V1, V2, V3, V41 und V42. Die Stecknadel auf der Karte bleibt.

### M2 – V24 erscheint nur im Sonderfall (belegt)

- `.xp <18,1` überspringt V24 unter Stufe 18, `#maxlevel 17` blendet ihn ab Stufe 18 beim Laden aus.
- Sichtbar ist V24 nur, wenn der Charakter beim Laden höchstens 17 war und bei V24 ohne Neuladen schon 18 ist.
- Best Practice §5 und T35 versprechen «ab Stufe 18 die SFK-Quests im Grabmal».
- **Vorschlag:** Text und Test anpassen oder V24 mit Entscheid 37 neu fassen.

### N1 – `.isQuestComplete` bei reinen Liefer-Quests (ungeprüft, API)

- Betroffen: V18 (95204), V20 (97288), V34 (5724). RXP fragt dafür `C_QuestLog.IsComplete`.
- Ob das bei Quests ohne Ziel wahr ist, ist im Spiel ungeprüft. Wenn nicht, verschwindet die Abgabe-Erinnerung.
- RXP selbst ist uneinheitlich: `.isOnQuest 5724` und beim Allianz-Wappen 95189 `.isOnQuest`, aber bei 99082, 950 und 6922 `.isQuestComplete`.
- **Vorschlag:** `.isOnQuest`. Bei Liefer-Quests ist das gleichwertig und sicher.

### N2 – Werkzeug `rxp_schritte.py`

- **`vergleich`:** RXP vergleicht mit der Kennung der zuletzt geladenen Version, nicht mit `git:HEAD`.
  - Laut Testlog speicherte der Druide in 6-12 zuletzt mit 0.3 (14.10.), der Stufe-18-Charakter mit 0.5 (15.10. 22:16).
  - Gegen diese Stände geprüft: 6-12 #45 findet RXP über die Kennung (Zeile 510). 12-17 #152 (alte Zeile 2591) findet es über die Nummer, gleicher Schritt `.complete 881,1`.
  - Bei Krieger und Schamane meldet das Werkzeug PROBLEM. Es ist aber derselbe Kombi-Schritt mit neuerem Text, also harmlos.
- **Nachbildung:** sonst treu (Kommentare, Zeilenzählung, stepId, Filter, `#maxlevel`, `.dungeon`). Andere Tags kommen in den vier Speedrun-Guides nicht vor.
- **Lücken:**
  - `ziele` erkennt kein sofort erledigtes Ziel (H1) und keinen RXP-Schritt, dessen `next` jetzt einen V-Schritt trifft (N3).
  - In `ziele` fehlt die Rasse Skyborne; mit ihr nachgeprüft, keine weiteren Fehler.
  - `vergleich` kennt keinen Stufenwechsel zwischen Speichern und Laden (H2).
  - Der Bau prüft `#completewith next` nur am rohen Vorgänger, nicht am gezeigten.

### N3 – V43 ist jetzt «next» von RXPs Druiden-Flug in Moonglade (belegt, harmlos)

Der Flugschritt (`Kombi_Guide.lua` ~L8050, `#completewith next`) verschwindet jetzt nach V43 statt nach dem ersten Abbruch-Schritt.

### N4 – Texte

- **V1:** Quest 5722 gibt man im Dungeon bei Maur Grimtotem ab, nicht bei Rahauro. Bei Rahauro gibt man 5724 und 5723 ab (RXP Barrens L593).
- **V17:** «Gegenstände, die dort fallen» stimmt für das Wappen nicht. Man lootet es aus einem Objekt (Testlog 20:50, «Öffnen | Objekt 614679»).

### N5 – Quellen und Doku

- **V10** nennt als Quelle «Icy Veins 15.09.2026». Die steht nicht in der Recherche. Der Inhalt stimmt (Icy Veins, 12.09. und 23.09.); Link und Datum nachtragen.
- **Best Practice §4:** «Mebok 63.0, 37.2» ist die Stelle von Sputtervalve. Mebok steht bei 62.4, 37.6, so wie in V30.
- **Best Practice §5:** «an derselben Stelle wie RXP» gilt nicht für V1, V36, V41 und V42.

### N6 bis N8 – kleinere Punkte

- **N6 (Vermutung):** In Unterstadt kommt das Königsviertel (V12, V14) vor dem Apothecarium (V13, V16). Das kann einen Rückweg bedeuten.
- **N7 (Vermutung):** Morbin, Griffs und Oran haben in `.target` keine NPC-ID. Im deutschen Client findet das Ziel-Makro sie vielleicht nicht.
- **N8:** Mit «Skip overleveled steps» aus wirkt `#maxlevel` nicht, und #152 verschiebt sich. Standard ist an.

## Die sieben Punkte einzeln

### 1. Hält ein Schritt die Route auf? (belegt)

| Schritt | Hält auf? | Verschwindet bei |
|---|---|---|
| V1, V2, V3 | nein (Erinnerung) | Annahme, Häkchen oder Ziel (WildManeTurnIn bzw. V10) |
| V10 | ja, gewollt | Ankunft in Tirisfal (Karte 1420) oder Häkchen; unter 15 übersprungen |
| V11–V16 | nein | Annahme, Häkchen, V17 erledigt oder ausserhalb von 1420/1458/1421 |
| V17 | ja, gewollt | Häkchen oder Verlassen der drei Karten |
| V18–V23 | nur wenn die Quest erledigt ist | Abgabe, Häkchen, Verlassen der Karten |
| V24 | nein | siehe M2 |
| V41, V42, V30, V31, V33, V36 | nein | Annahme, Häkchen oder Ziel |
| V32 | nein | sofort (H1) |
| V34, V35 | nur wenn die Quest erledigt ist | Abgabe oder Häkchen |
| V43, V44 | nur mit der Quest im Log | Häkchen |

- **Instanz:** Der Testlog zeigt im Kartenfeld «-», die Karte ist dort also nicht lesbar. `zoneskip` tut dann nichts, die Schritte bleiben stehen. Der Pfeil ist in Instanzen aus.
- **Abbruch oder vorzeitiger Ruhestein:** Bei der Ankunft im Brachland (1413) erledigen sich V11–V24 über `zoneskip`. RXPs Ruhestein-Schritt erledigt sich über `.subzoneskip 380`; weiter geht es bei FoodandWater2.
- **Häkchen bei V10 in Orgrimmar:** Alle Abstecher-Schritte fallen sofort weg. Schon angenommene Quests bleiben ohne Erinnerung im Log.

### 2. Pfeil (belegt)

- Die Mechanik ist wie in Best Practice §4 beschrieben. Probleme siehe M1.
- Der Abstecher führt sinnvoll von Tirisfal über Unterstadt zum Eingang. Tabitha bekommt praktisch nie den Pfeil, wie der Text sagt.

### 3. Voraussetzungen und Reihenfolge: in Ordnung

- 1491 kommt nach 865, 962 nach 853, 914 nach 1490, 6563 nach 6562.
- Mindeststufen stehen in `.xp` oder im Text.
- An den Ankern steht der Spieler beim Geber oder kommt direkt vorbei.

### 4. Abbruch-Schritte: vollständig

- In 6-12 gibt es keine.
- In 12-17 nur für RFC, mit `.dungeon RFC` und deshalb in Forever unsichtbar.
- In 17-22 für die sechs WC-Quests und 6563.
- V43 und V44 funktionieren. Ein Abbruch-Schritt lässt sich per Häkchen überspringen, die Quest bleibt im Log.

### 5. Koordinaten: in Ordnung

- Alle Weltkoordinaten sind gleich wie in RXP; die Spielkoordinaten sind richtig umgerechnet.
- Die Abgaben im Testlog liegen 0 bis 5 Yards daneben.
- Kontinent 0 für 1420/1421/1458, 1 für die übrigen Karten.

### 6. Stellen der Testcharaktere: halten

Siehe N2.

### 7. Texte

- Bis auf N4 und N5 belegt.
- Kein `--`, kein `[[`/`]]` und kein `,,` in Feldern.

## Blinde Flecken

KOMMENTAR: RXPs Quest-Automatik ist standardmässig an. Wer einen Geber anspricht, solange der Zusatzschritt aktiv ist, nimmt die freiwilligen Quests also automatisch an.

KOMMENTAR: RXP nimmt für Forever ein Questlog von 40 Plätzen an; im Spiel ist das ungeprüft. Viele freiwillige Quests bleiben ohne Abgabe- oder Abbruch-Erinnerung im Log, z. B. 5725, 5726 und 5761 sowie die Quests für die Ruinen von Lordaeron, Burg Schattenfang, den Kral der Klingenhauer und 6921.

---

## Umsetzung (16.10., Kombi-Guide 0.6.1)

| Befund | Umgesetzt |
|---|---|
| H1 Zamah | V32 bleibt bis «KombiV34» (Elder Rise) stehen, Pfeil nachrangig. `tools/rxp_schritte.py ziele` meldet jetzt leere Ziel-Schritte ohne wartenden Schritt davor (auf dem alten Bau: 30 von 45 Klasse/Rasse). |
| H2 Neuladen ab Stufe 18 | Warnung im Text des Laufs (V17); offene Entscheidung 37 mit den drei Wegen ergänzt. `#maxlevel 17` bleibt, bis der Nutzer entscheidet. |
| M1 Pfeil | `.goto …,0,0` für V1, V2, V3, V32, V41, V42 (dazu schon V15, V24). |
| M2 V24 | bleibt; Best Practice §5 und T35 sagen, wann er erscheint. |
| N1 Liefer-Quests | V18, V20, V34 mit `.isOnQuest`, wie RXP. |
| N2 Werkzeug | `ziele` mit Volk Skyborne und leeren Zielen; `vergleich` gegen den Stand der letzten Speicherung bleibt Handarbeit (hier vom Prüfer gemacht). |
| N3 | harmlos, keine Änderung. |
| N4 Texte | V1 (Abgaben im Dungeon und bei Rahauro), V17 (Wappen aus einem Objekt). |
| N5 Quellen | V10 mit Icy Veins 12.09. und 23.09.; Mebok in Best Practice §4 (62.4, 37.6); §5 «meist an derselben Stelle» mit den Ausnahmen. |
| N6, N7 | Vermutungen, keine Änderung (Reihenfolge in Unterstadt; NPC-IDs von Morbin, Griffs und Oran unbekannt, ungeprüft). |
| N8 | in Best Practice §4 schon beschrieben («Skip overleveled steps», Standard an). |
| Quest-Automatik, Questlog | Best Practice §4; im Ergebnis an den Nutzer als KOMMENTAR. |

Nach der Umsetzung: Bau ohne Probleme; `ziele` für alle vier Guides ohne Befund (9 Klassen, 5 Rassen); Stellen «6-12 Mulgore» #45 (Tauren-Druide, -Jäger, -Schamane, -Krieger) und «12-17» #152 mit Stufe 18 (alle 9 Klassen) halten gegenüber `main`; «Kombiguide Dungeon (H)» gleich wie a210061.
