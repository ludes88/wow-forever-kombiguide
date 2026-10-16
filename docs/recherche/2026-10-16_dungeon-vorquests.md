# Dungeon-Vorquests der Horde bis Stufe 22 (Recherche 16.10.2026)

Frage: Welche Dungeon-Quests kann die Horde bis Stufe 22 dort annehmen, wo die Route vorbeikommt (Entscheid vom 16.10.: «ALLE Pre quests für ALLE dungeons also auch die neue lordaron in uc sowie burg shadowfang»)? Mit Mindeststufe, Geber, Ort und Quelle. Umsetzung: Kombi-Guide 0.6, `data/kombi/vorquests.csv` (unten).

**Kürzel, die in allen Abschnitten gelten**
- **AHL-n** = https://ahledger.com/wow-forever/quests/n (die Seite leitet auf die kanonische Adresse mit Namen weiter, z. B. `…/92421-lights-justice`; abgerufen am 16.10.). AHL nennt Questlevel, XP und Geld aus Addon-Daten, aber **nie eine Mindeststufe**.
- **MF-x** = https://metaforge.app/wow-forever/database/quests/x. Die Seiten sagen selbst «Includes data from VMaNGOS», deshalb gilt **[Classic]**.
- **RXP** = RestedXP-Code, Hauptzweig fe936eea vom 16.10.2026: https://github.com/RestedXP/RXPGuides/tree/fe936eeac7493c5a09da4546b3034756908ece39
- **«Rechnung»** = eine RXP-Weltkoordinate, die ich mit `data/karten/forever_karten.csv` umgerechnet habe (exakte Kartenecken aus dem Testlog). Das ist eine eigene Rechnung, keine Aussage einer Quelle.

---

## 1. Ruinen von Lordaeron (RoL)

**Quellen**
- WT-Q: https://www.warcrafttavern.com/forever/guides/the-ruins-of-lordaeron-quests/
- WT-D: https://www.warcrafttavern.com/forever/guides/the-ruins-of-lordaeron/
- IV: https://www.icy-veins.com/wow-forever/ruins-of-lordaeron-quests (Stand 30.09.)
- ATH: https://allthings.how/ruins-of-lordaeron-walkthrough-wow-forever-location-bosses-and-tips/ (21.09.)
- KL: https://kami-labs.fr/en/ruines-de-lordaeron-wow-forever/ (Build 1.60.1.70205, 10.10.)
- MOB: https://mobalytics.gg/wow-forever/dungeons/ruins-of-lordaeron-dungeon-guide (13.10.)
- MG: https://www.method.gg/wow-forever/dungeons/ruins-of-lordaeron (15.10.)
- Wiki: https://warcraft.wiki.gg/wiki/A_Frightened_Request · https://warcraft.wiki.gg/wiki/Morbin_Lightbane · https://warcraft.wiki.gg/wiki/Deathguard_Kristof · https://warcraft.wiki.gg/wiki/Faranell
- GW: https://gamewave.fr/world-of-warcraft-forever/wow-forever-entree-et-quetes-du-donjon-des-ruines-de-lordaeron/

| Quest (ID) | Mindeststufe | Questlevel | Geber und Ort | Abgabe | Ziel | Belohnung |
|---|---|---|---|---|---|---|
| Light's Justice (92421, AHL) | 15 (IV, ATH) | 22 (AHL, KL) | Morbin Lightbane, Unterstadt, Königsviertel «near Sylvanas»: 57.8, 89.7 (WT-Q) / 57.8, 89.8 (IV) / 57.9, 89.5 (MOB) / 57.8, 88.2 (Wiki); GW: «dans l'Apothicarium» | Morbin (WT-Q) | 25 Intact Limbs von Untoten im Dungeon (AHL, WT-Q) | 4600 XP, 45s (AHL); Wahl The Stitcher oder Spare Part Bindings (IV) |
| The New Plague (95216, AHL, WT-Q) | 16 (IV, ATH) | 22 (AHL, KL) | Theodore Griffs, Apothecarium, untere Ebene bei den Alchemie-Lehrern: 46.7, 71.9 (WT-Q) / 46.6, 72.0 (IV) / 46.6, 71.4 (KL) | Theodore Griffs (WT-Q) | 1 Highly Toxic Strain von Witherfang, dem 1. Boss (AHL, WT-Q) | 5450 XP (AHL); Plaguefang oder Blight Gloves (IV) |
| The Wrath of Rath'mael (92422, AHL) | 15 (IV, ATH) | 22 (AHL, KL) | Deathguard Kristof, Tirisfal, Zelte zwischen Unterstadt und Brill: 65.2, 60.1 (WT-Q) / 65.2, 60.2 (IV, Wiki) / 65.3, 60.1 (MOB); RXP steuert ihn für die andere Quest 99141 an: 65.2, 60.2 (Rechnung) | Kristof (WT-Q) | Rath'mael töten, den Endboss (AHL «0/1 slain») | 4600 XP (AHL); Forsaken Greataxe oder Gnarled Necromancer's Staff (IV) |
| A Frightened Request (92401, AHL) | 15 (IV, ATH); «Requires 15» (Wiki); RXP `.xp <15,1` | 22 (AHL, Wiki) | Tabitha Heartweaver (NPC 250686 laut RXP), Grabstätte im Silberwald: 44.6, 42.9 (WT-Q) / 44.5, 43.0 (IV, KL, MOB); RXP 44.5, 43.0 (Rechnung) | Tabitha (Wiki) | «Investigate the disappearance of Edward Heartweaver» (AHL); die Leiche liegt im westlichen Teil des Friedhofs von Rath'mael, hingehen genügt (WT-Q) | 4600 XP (AHL) **oder** 7050 XP und Unterstadt +150 (Wiki); Edward's Knife oder Tabitha's Cuffs |
| Unending Torment (97288, AHL, WT-Q) | 16 (IV, ATH) / 17 (MOB) | 21 (AHL, KL) | Startet mit dem Gegenstand Abominable Head (Item 280438), der von Kreatur 250660 in King's Alley fällt (https://ahledger.com/items/280438-abominable-head); laut WT-Q, IV und ATH von The Baron | Master Apothecary Faranell, Apothecarium: 49.2, 69.9 (WT-Q) / 48.4, 69.6 (KL) / 48.6, 69.6 (Wiki); RXP 48.8, 69.3 (Rechnung) | «Deliver the Abominable Head to Master Apothecary Faranell» (AHL) | 3450 XP (AHL) |
| Crest of Lordaeron, Horde (95204, AHL und WT-D) | 16 (IV, ATH) | 22 (AHL) | Startet mit dem Gegenstand Crest of Lordaeron (Item 275521, King's Alley, https://ahledger.com/items/275521-crest-of-lordaeron); laut WT-Q 5 mögliche Fundorte | Oran Snakewrithe, Magieviertel: 73.3, 32.6 (WT-Q) / 73.4, 32.4 (KL) | Wappen zu Oran bringen (AHL) | 5450 XP, Small Sack of Gems (AHL) |

- **Kette von Unending Torment:** 5 Schritte, alle Questlevel 21, ab Schritt 2 je 1650 XP und 13s (AHL-97289 bis AHL-97292; KL: «step 1 of 5»).
  - 97289: von Faranell; «Bring the Head of the Baron to Othmar's body», Abgabe Unfinished Abomination.
  - 97290: von der Unfinished Abomination zurück zu Faranell.
  - 97291: Toxic Skullcap, Blisterweed und Essence of Agony bringen.
  - 97292: «Administer Hissing Serum».
  - Orte laut WT-Q: Abomination 46.0, 62.1; Topf mit Blisterweed 54.1, 49.4; Toxic Skullcap bei Tawny Grisette (wandert im oberen Handelsviertel); Essence of Agony bei Ezekiel Graves, 75.7, 51.5; Serum vom Geländer aus, 45.0, 62.9.
- **Allianz-Gegenstück zum Wappen:** 95189, Abgabe Lady Dena Kennedy, 6200 XP (AHL-95189). Diese ID nutzt auch RXPs Allianz-Guide, mit Item 268579.
- **Voraussetzungen:** Für die Quests ausser Unending Torment nennt keine Quelle eine.
- **Eingang:**
  - WT-D: «Undercity, Tirisfal Glades … Its coordinates are 72.4, 11.6»; welche Karte, sagt die Seite nicht.
  - ATH: «Enter the ruins in Tirisfal (roughly 71.6, 11.4)».
  - MOB: 71.6, 11.4, ohne Zone.
  - KL: «Entrance: Tirisfal Glades, coordinates 64.3, 67.2».
  - RXPs Allianz-Guide steuert den Eingang mit `.goto 1458/0,170.700,1804.700` an («Travel to the Ruins of Lordaeron in Undercity»), siehe https://github.com/RestedXP/RXPGuides/blob/fe936eeac7493c5a09da4546b3034756908ece39/Guides/Forever/dungeon/Alliance-11-20.lua.
  - **Rechnung:** RXPs Punkt liegt auf der Unterstadt-Karte bei 73.2, 11.4, auf der Tirisfal-Karte bei 63.4, 67.5. Liest man 72.4, 11.6 und 71.6, 11.4 als Unterstadt-Karte, liegen sie bei Tirisfal 63.2, 67.5 und 63.0, 67.5: knapp 8 Yards auseinander und je etwa 8 Yards von RXPs Punkt. KLs 64.3, 67.2 liegt etwa 44 Yards daneben. Als Tirisfal-Karte gelesen läge 72.4, 11.6 am Nordrand von Tirisfal. Beide Werte passen also zur Unterstadt-Karte (1458), nicht zu Tirisfal.
- **Stufenbereich:**
  - 15–20 (WT-D, KL, ATH; ATH empfiehlt 17–20)
  - 15–22 (MG)
  - MOB: «advertised as being levels 11-24 … at least level 15»
  - KL: «The Group Finder offers it from level 15»
- **RXP Horde, Stand 16.10.:**
  - Nur 92401 ist eingebaut, und zwar abgeschaltet: `step << skip` mit `.dungeon ROL` und dem Kommentar «TODO: Activate step once .dungeon ROL command works» (`Guides/forever/Horde-01-14_Undead.lua`).
  - `dungeonList` in `DB/forever/db.lua` kennt kein ROL.
  - Nicht verwechseln: RXPs Untoten-Route führt «A New Plague» (367, 368, 369, 492). Das ist die Classic-Kette in Tirisfal, nicht 95216.

## 2. Burg Shadowfang (SFK)

**Quellen**
- WT-SQ: https://www.warcrafttavern.com/forever/guides/shadowfang-keep-quests/
- WT-SD: https://www.warcrafttavern.com/forever/guides/shadowfang-keep/
- IV-S: https://www.icy-veins.com/wow-forever/shadowfang-keep-quests (02.10.)
- KL-S: https://kami-labs.fr/en/donjon-d-ombrecroc-wow-forever/
- MOB-S: https://mobalytics.gg/wow-forever/dungeons/shadowfang-keep-guide (15.10.)
- MF: `the-book-of-ur`, `deathstalkers-in-shadowfang`, `arugal-must-die`

| Quest (ID) | Mindeststufe | Questlevel | Geber | Ziel und Abgabe | AHL |
|---|---|---|---|---|---|
| Deathstalkers in Shadowfang (1098) | «Level Required: 18» (WT-SQ); 18 (IV-S, MOB-S); [Classic] 18 (MF) | 25 (AHL, KL-S, MF) | High Executor Hadrec (NPC 1952), Grabstätte im Silberwald: 43.4, 40.8 (IV-S) / 43.4, 40.9 (MOB-S); RXP 43.4, 40.9 (Rechnung) | Deathstalker Adamant und Vincent finden; Abgabe bei Vincent im Dungeon (WT-SQ) | 5350 XP, 18s |
| The Book of Ur (1013) | 16 (WT-SQ, IV-S, MOB-S, MF) | 26 | Keeper Bel'dugur (NPC 2934), Apothecarium: 53.6, 54.0 (IV-S, KL-S) / 59.2, 76.6 (MOB-S) | Buch im Raum von Fenrus; Abgabe Bel'dugur | 5600 XP |
| Arugal Must Die (1014) | 18 (WT-SQ, IV-S, MOB-S, MF) | 27 | Dalar Dawnweaver (NPC 1938), Grabstätte: 44.2, 39.8 (IV-S, KL-S, MOB-S); RXP 44.2, 39.7 (Rechnung) | Head of Arugal; Abgabe Dalar | 8850 XP, Seal of Sylvanas |

- **Klassenquests:** The Orb of Soran'ruk (1740, Hexenmeister), Mindeststufe 20, Doan Karhan, Brachland 49.2, 57.2 (IV-S). The Horn of Xelthos (78261, Schurke, solo), Mindeststufe 1 (IV-S).
- **Was Forever geändert hat:** «The quests are currently the same as their WoW Classic versions except for some updated rewards, with the exception of one quest for Rogues that has carried over from Season of Discovery.» (WT-SQ). Mindeststufen und Questlevel stimmen mit den VMaNGOS-Werten überein (MF). KL-S markiert einzelne Belohnungen als «New».
- **Ketten:** keine, «one of the few early dungeons with no quest chains» (WT-SQ).
- **Stufenbereich:** 20–26 (WT-SD); 18–25 (MOB-S); «open from level 11. The Group Finder offers it from level 18» (KL-S).
- **Eingang:** Silberwald 44.5, 68.0 (WT-SD) / 44.6, 67.7 (KL-S).

## 3. Hall of Thanes

**Quellen**
- WT-HD: https://www.warcrafttavern.com/forever/guides/hall-of-thanes/
- WT-HQ: https://www.warcrafttavern.com/forever/guides/hall-of-thanes-quests/
- WT-HN: https://www.warcrafttavern.com/forever/news/how-to-find-the-hall-of-thanes-dungeon-quests/ (19.09.)
- Wiki-H: https://warcraft.wiki.gg/wiki/Hall_of_Thanes_(instance)
- IV-H: https://www.icy-veins.com/wow-forever/hall-of-thanes-quests (30.09.)
- KL-H: https://kami-labs.fr/en/la-salle-des-thanes-wow-forever/
- AHL-96395

**Fakten**
- **Ort:** unter Eisenschmiede. Der Eingang liegt im Thronsaal beim High Seat (König Magni), durch einen Gang mit Spinnweben, bei Eisenschmiede 43.5, 52.0 (WT-HD, WT-HN, KL-H).
- **Stufe:** 13–18 (WT-HD, WT-HN, Wiki-H, KL-H).
- **Fraktion:**
  - WT-HN: «a new level 13-18 Alliance-exclusive dungeon», das Gegenstück zu RFC.
  - WT-HD: «Horde can complete this dungeon if desired»; der Zugang sei schwierig, Horde-Quests gebe es keine.
  - WT-HQ: Horde «won't be getting any quests».
  - Wiki-H: «Almost all quests for the dungeon are Alliance-based»; Zugang «ill-advised for Horde players»; An Ancient Grudge ist «Neutral» und wird im Dungeon von einem neutralen Geist vergeben.
  - IV-H: 3 von 5 Quests nur Allianz. Ohne Fraktionszeichen sind An Ancient Grudge (Ghostly Attendant, im Dungeon, Mindeststufe 10) und Important Heirlooms (Thom Filch, Eisenschmiede 32.6, 44.6, Mindeststufe 10).
  - AHL-96395 (An Ancient Grudge): Questlevel 15, 2300 XP, keine Fraktionsangabe.
- **Gruppensuche:** Die LFG-Oberfläche «does not form them automatically or teleport everyone to the dungeon»; Versammlungssteine funktionieren nicht (https://www.warcrafttavern.com/forever/news/no-group-finder-or-summoning-stones-in-wow-forever/).
- **Horde-Quests ausserhalb des Dungeons:** keine gefunden.

## 4. Tiefschwarze Grotte (BFD)

**Quellen**
- WT-BQ: https://www.warcrafttavern.com/forever/guides/blackfathom-deeps-quests/
- WT-BD: https://www.warcrafttavern.com/forever/guides/blackfathom-deeps/
- IV-B: https://www.icy-veins.com/wow-forever/blackfathom-deeps-quests
- MOB-B: https://mobalytics.gg/wow-forever/dungeons/blackfathom-deeps-guide (15.10.)
- KL-B: https://kami-labs.fr/en/profondeurs-de-brassenoire-wow-forever/
- RXP: `Guides/Forever/dungeon/Horde-12-22_Barrens.lua` und `Guides/forever/Horde-12-22_Barrens.lua`

| Quest (ID) | Mindeststufe | Questlevel (AHL) | Geber und Ort | Abgabe, Ziel | AHL |
|---|---|---|---|---|---|
| Trouble in the Deeps (6562) | [Classic] 17 (MF `trouble-in-the-deeps`); Forever: keine Quelle | 22 | Tsunaman, Sun Rock Retreat, Steinkrallengebirge (AHL). Schon in RXPs Speedrun-Route «17-22» (Label «Tsunaman1»), Abgabe bei Je'neu | Je'neu Sancrea | 440 XP |
| The Essence of Aku'Mai (6563) | 17 (IV-B, MOB-B) / 18 (WT-BQ) | 22 | Je'neu Sancrea, Zoram'gar, Eschental 11.6, 34.2 (IV-B, MOB-B); setzt 6562 voraus (WT-BQ, RXP) | 20 Sapphire of Aku'Mai, in und vor dem Dungeon | 1750 XP, 14s |
| Allegiance to the Old Gods (6564) | 17 (WT-BQ, IV-B, MOB-B; sie trennen 6564 und 6565 nicht) | 22 | Damp Note (Item 16790, RXP) von Blackfathom Tide Priestess vor dem Dungeon | Note zu Je'neu bringen | 1300 XP, 11s |
| Allegiance to the Old Gods (6565) | wie oben | 26 | Je'neu | Lorgus Jett töten | 6300 XP, 40s |
| Amongst the Ruins (6921 laut AHL und RXP; WT nennt 908) | 21 (WT-BQ, IV-B, MOB-B) | 27 | Je'neu | Fathom Core unter Wasser | 6550 XP, 45s |
| Baron Aquanis (6922 laut AHL und RXP; WT nennt 78920) | 21 (alle drei) | 30 | Strange Water Globe (Item 16782) von Baron Aquanis | Abgabe Je'neu | 7250 XP |
| Blackfathom Villainy, Horde (6561 laut AHL und RXP; WT nennt 78922) | 18 (alle drei) | 27 | **Geber ist Argent Guard Thaelrid im Dungeon** (WT-BQ, IV-B, MOB-B, RXP). Bashana ist nur die Abgabe | Bashana Runetotem, Thunder Bluff: 70.8, 33.7 (WT, Excavation-Seite) / RXP 71.0, 34.2 (Rechnung); Ziel Head of Kelris | 7850 XP, 65s |

- **Stufenbereich:** 22–28 (WT-BD); 24–32 (MOB-B); «open from level 15», Gruppensuche ab 22 (KL-B).
- **Eingang:** Eschental 14.5, 14.6 (WT-BD); Instanzportal 16.4, 10.9 (KL-B); RXPs Portal liegt auf der Kalimdor-Karte bei 44.4, 34.9 (Rechnung).
- **Was Forever geändert hat:** «haven't changed from their WoW Classic versions other than some updated rewards» (WT-BQ).

## 5. Kral und Hügel der Klingenhauer (RFK, RFD)

**Quellen**
- WT-KQ: https://www.warcrafttavern.com/forever/guides/razorfen-kraul-quests/
- WT-DQ: https://www.warcrafttavern.com/forever/guides/razorfen-downs-quests/
- WT-L (Dungeonliste): https://www.warcrafttavern.com/forever/guides/dungeons/
- KL-L: https://kami-labs.fr/en/donjons-raids-wow-forever/

**Stufenbereiche:** RFK 29–38 (WT-L), «Level 24» (KL-L); RFD 37–46 (WT-L), «Level 34» (KL-L).

**Annahme in Thunder Bluff, im Brachland und in Orgrimmar**
- **A Vengeful Fate (1102):** Mindeststufe 29 (WT-KQ; [Classic] MF `a-vengeful-fate` 29). Questlevel 34, 8500 XP (AHL). Auld Stonespire, Lower Rise, Thunder Bluff (Koordinaten: keine Quelle). Ziel: Razorflank's Heart.
- **Blueleaf Tubers (1221), neutral:** Mindeststufe 20 (WT-KQ; [Classic] MF 20). Questlevel 26, 5000 XP und Small Container of Gems (AHL). Mebok Mizzyrix in Ratchet; Crate with Holes, Command Stick und Owner's Manual liegen neben ihm (WT-KQ).
- **Brutal Armor (1838), nur Krieger:** Mindeststufe 20, Thun'grim Firegaze östlich der Crossroads (WT-KQ).
- **A Host of Evil (6626), neutral:** Mindeststufe 28 (WT-DQ, MF). Myriam Moonsinger, auf dem Hügel vor RFD; WT verlinkt dazu das Brachland, MF nennt Tausend Nadeln. Ziel: 8 Battleguard, 8 Thornweaver und 8 Death's Head Cultist vor dem Dungeon töten.

**Annahme in Unterstadt**
- Going, Going, Guano! (1109): Faranell, Mindeststufe 30 (WT-KQ), Questlevel 33 (AHL).
- Bring the End (3341): Andrew Brownell, Magieviertel, Mindeststufe 37 (WT-DQ).

**Start mit Beute bzw. im Dungeon:** An Unholy Alliance 6522 (RFK) und 6521 (RFD), Mindeststufe 28; Willix the Importer (1144), Mindeststufe 22; Belnistrasz (3523 und 3525), Mindeststufe 32 (WT-KQ, WT-DQ).

**Was Forever geändert hat (RFD):** «haven't changed from their WoW Classic versions other than receiving updated rewards» (WT-DQ).

## 6. Mindeststufen RFC und WC

**Quellen**
- IV-R: https://www.icy-veins.com/wow-forever/ragefire-chasm-quests (29.09.)
- WT-R: https://www.warcrafttavern.com/forever/guides/ragefire-chasm-quests/
- IV-W: https://www.icy-veins.com/wow-forever/wailing-caverns-quests
- WT-W: https://www.warcrafttavern.com/forever/guides/wailing-caverns-quests/
- Wiki-AZ: https://warcraft.wiki.gg/wiki/Apothecary_Zamah_(quest)
- MF `apothecary-zamah`, `nara-wildmane`, `serpentbloom`

**Ragefire Chasm** (Mindeststufe 9 bei allen, WT-R und IV-R)

| ID | Quest | Questlevel (AHL) | XP (AHL) | Geber und Ort |
|---|---|---|---|---|
| 5722 | Searching for the Lost Satchel | 16 | 1800 | Rahauro, Elder Rise: 70.6, 31.6 (IV-R) / RXP 70.4, 29.6 (Rechnung) |
| 5723 | Testing an Enemy's Strength | 15 | 2150, 7s | Rahauro |
| 5724 | Returning the Lost Satchel | 16 | 2950 | an der Leiche von Maur Grimtotem, Abgabe Rahauro |
| 5725 | The Power to Destroy… | 16 | 2950 | Varimathras, Unterstadt: 56.2, 92.6 (IV-R) / RXP 56.3, 92.2 (Rechnung) |
| 5726 | Hidden Enemies, Teil 1 (Insignia in Skull Rock) | 12 | 900, 2s50c | Thrall, Orgrimmar: 32.0, 37.8 (IV-R) / RXP 31.7, 37.8 |
| 5727 | Hidden Enemies, Teil 2 (Neeru befragen) | 12 | 460 | Thrall |
| 5728 | Hidden Enemies, Teil 3 (Jergosh und Bazzalan töten) | 16 | 2350, 8s | Thrall |
| 5761 | Slaying the Beast | 16 | 2350, 8s | Neeru Fireblade: 49.6, 50.4 (IV-R) / RXP 49.5–49.6, 50.4–50.6 |

Für die Teile 5726–5728 nennt WT-R die Stufe 9 für die ganze Kette, nicht pro Teil. WT-R: «There are no significant changes to these quests from their original versions in Classic.»

**Höhlen des Wehklagens**

| ID | Quest | Mindeststufe | Questlevel (AHL) | XP (AHL) | Geber |
|---|---|---|---|---|---|
| 959 | Trouble at the Docks | 14 (WT-W, IV-W) | 18 | 2650, 10s | Bigglefuzz: 63.0, 37.6 (IV-W) / RXP 63.1, 37.6 |
| 962 | Serpentbloom | 14 (WT-W, IV-W, MF) | 18 | 3300, 20s | Zamah, TB: 23.0, 21.0 (IV-W) / RXP 22.8, 20.9 |
| 914 | Leaders of the Fang | 10 (WT-W, IV-W) | 22 | 4300 | Nara Wildmane: 75.6, 31.2 (IV-W) / RXP 75.7, 31.6. Kette laut WT-W: 886 → 870 → 877 → 880 → 1489 → 1490 → 914 |
| 1486 | Deviate Hides | 13 | 17 | 3100, 18s | Nalpak: 46.4, 33.7 (IV-W) / RXP 46.0, 35.7 (Rechnung) |
| 1487 | Deviate Eradication | 15 | 21 | 4000, 25s | Ebru, am selben Ort |
| 1491 | Smart Drinks | 13 | 18 | 2650, 10s | Mebok: 62.4, 37.6 (IV-W, RXP); setzt Raptor Horns (865) voraus |
| 853 | Apothecary Zamah | «Level: 15 (Requires 10)» (Wiki-AZ); 10 (MF) | 15 | 800, Cauldron Stirrer | Apothecary Helbrim, RXP 51.4, 30.2; setzt Fungal Spores (848) voraus (RXP `.isQuestTurnedIn 848`, MF) |
| 1490 | Nara Wildmane | [Classic] 10 (MF) | 16 | 120 | Hamuul, RXP 78.6, 28.6 |
| 6981 | The Glowing Shard | 15 (WT-W, IV-W: «at least level 15 to use the Glowing Shard») | 26 | 5150 | Glowing Shard (Item 10441) von Mutanus; Abgabe Falla Sagewind (AHL) |

**Zeitlimit von 853**
- Wiki-AZ: «Time limit: 45 min»; der Artikel sagt dazu «remains in Classic and Forever».
- RXP (Speedrun- und Dungeon-Route, Stand 16.10.): «Starts a 45-minute timed quest», dazu «You are on a timed quest, don't go afk. It will get turned 20-30 minutes after pick-up».
- AHL-853: Das Ziel endet abgeschnitten mit «before the time», ohne Dauer.
- MF: «before the time limit is up», ohne Dauer.
- Ein Forever-Datenbankeintrag mit der Dauer: nicht gefunden.

WT-W: «carried over from Classic WoW with no changes other than their rewards».

## 7. Weitere Dungeons mit Horde-Quests in den genannten Gebieten

- **Unter Stufe 22 annehmbar:** nur Blueleaf Tubers (RFK, Ratchet, Mindeststufe 20; siehe Abschnitt 5). Dazu kommen RFC, WC, RoL, SFK und BFD aus den Abschnitten oben.
- **Excavation Site: Wetlands:** 24–29 (WT-L) bzw. 26–33 (https://www.warcrafttavern.com/forever/guides/excavation-site-wetlands-quests/); alle Quests ab 24 (https://www.icy-veins.com/wow-forever/excavation-site-wetlands-quests).
  - Changing Tastes (95697): Borstan, Orgrimmar, The Drag, 57.3, 53.3 (WT) / 57.4, 53.4 (IV).
  - Elder Knowledge (95664): Titan Relic → Bashana, Thunder Bluff → Earthen Echo (98823) → Muln Earthfury, Mulgore 33.4, 22.5 (WT).
  - Dragonmaw Rumors: Zaruk, Arathi.
- **City of Dalaran:** 28–33 (WT-L; https://mobalytics.gg/wow-forever/profile/phaseshifter/dungeons/the-city-of-dalaran-bosses-loot-and-quests; https://gamewave.fr/world-of-warcraft-forever/wow-forever-entree-et-quetes-du-donjon-de-la-cite-de-dalaran/). Alle Quests ab 24 (MOB, GW).
  - Source of Power: Doctor Martin Felben, Apothecarium 45.8, 73.2 (MOB).
  - Weitere Horde-Quests in Tarrens Mühle und am Eingang.
- **Gnomeregan:** Rig Wars (80132) und Chief Engineer Scooty (80133) in Orgrimmar, «Level» 25 (https://www.warcrafttavern.com/forever/guides/gnomeregan-quests/).
- **Scharlachrotes Kloster:** keine Horde-Quest unter 22, die niedrigste hat Stufe 25 (https://www.warcrafttavern.com/forever/guides/scarlet-monastery-quests/).
  - In Unterstadt: 1048 (33), 1113 (30), 1160 (25).
  - In Thunder Bluff: 1049 (28).
- **Todesminen:** «exclusive to the Alliance» (https://www.warcrafttavern.com/forever/guides/the-deadmines-quests/).

---

## Widersprüche
1. **Eingang RoL:** 72.4, 11.6 (WT-D, ohne Karte) gegen 71.6, 11.4 (ATH «in Tirisfal», MOB) gegen Tirisfal 64.3, 67.2 (KL). Laut meiner Rechnung passen die ersten beiden zur Unterstadt-Karte.
2. **IDs des Wappens:** Die WT-Questseite nennt Horde 95189 und Allianz 95204. WT-D, AHL und RXP nennen Horde 95204 und Allianz 95189.
3. Mindeststufe Unending Torment: 16 (IV, ATH) gegen 17 (MOB). MG nennt bei allen RoL-Quests «16», ohne zu sagen, was die Zahl bedeutet.
4. XP für A Frightened Request: 4600 (AHL) gegen 7050 (Wiki).
5. Koordinaten in Unterstadt:
   - Morbin: 89.5–89.8 gegen 88.2 (Wiki); GW nennt das Apothecarium statt des Königsviertels.
   - Faranell: 49.2, 69.9 / 48.4, 69.6 / 48.6, 69.6 / RXP 48.8, 69.3.
   - Griffs: 71.9 / 72.0 / 71.4.
6. Stufenbereich RoL: 15–20 / 15–22 / «11-24».
7. Bel'dugur: 53.6, 54.0 (IV-S, KL-S) gegen 59.2, 76.6 (MOB-S).
8. Stufenbereich SFK: 20–26 / 18–25 / ab 11, Gruppensuche ab 18.
9. **BFD-IDs bei WT:** 908, 78920 und 78922. AHL und RXP nennen 6921, 6922 und 6561.
10. Mindeststufe Essence of Aku'Mai: 17 (IV-B, MOB-B) gegen 18 (WT-BQ).
11. BFD-Bereich: 22–28 / 24–32 / ab 15, Gruppensuche ab 22. Eingang: 14.5, 14.6 gegen 16.4, 10.9.
12. **Blackfathom Villainy:** Im Rechercheauftrag stand Bashana als Geber. Alle Quellen nennen Thaelrid im Dungeon als Geber und Bashana als Abgabe. AHL-6561 schreibt dazu «Picked up in Thunder Bluff», ohne den Geber zu nennen.
13. **Hall of Thanes:** WT sagt «Alliance-exclusive» und «no quests» für die Horde. Laut Wiki ist An Ancient Grudge «Neutral», IV zeigt zwei Quests ohne Fraktion.
14. Myriam Moonsinger: Brachland (WT-DQ) gegen Tausend Nadeln (MF).
15. Rahauro: 70.6, 31.6 (IV-R) gegen RXP 70.4, 29.6. Nalpak und Ebru: 46.4, 33.7 (IV-W) gegen RXP 46.0, 35.7.
16. Stufenbereiche: Excavation Site 24–29 gegen 26–33 (beides WT). City of Dalaran 28–35 und 26–33, beides auf derselben MG-Seite (https://www.method.gg/wow-forever/dungeons/city-of-dalaran).
17. WT-R selbst: Für Hidden Enemies verlinkt der Kopf 5728, der Text 5726.

## Nicht gefunden
- Mindeststufen aus einer Forever-Quelle für 6562, 1490 und 853 (nur MF [Classic] bzw. Wiki); Mindeststufen der Schritte 2–5 von Unending Torment.
- Die Dauer des Zeitlimits von 853 in einer Forever-Datenbank (nur RXP-Text und Wiki).
- Koordinaten von Auld Stonespire, Andrew Brownell, Myriam Moonsinger und Tsunaman.
- Je'neu und Tsunaman aus RXP umgerechnet: In `forever_karten.csv` fehlen die Kartenecken für 1440 (Eschental) und 1442 (Steinkrallengebirge).
- Abgabe-NPCs für 92421, 92422 und 95216 bei AHL (nur bei WT-Q).
- Icy-Veins-Seiten für RFK und RFD in Forever.
- Ob die Horde in der Hall of Thanes eine Quest bekommt: Die Quellen widersprechen sich, offen.
- Abrufe, die fehlschlugen:
  - foreverchanges.pro/quest/92421: Freigabe nicht beantwortet.
  - AHL 78922, 908, 6626 und 97293: Fehler beim Abruf.
  - AHL-NPC-Seiten: Fehler beim Abruf.
  - MF `the-essence-of-aku-mai`, `amongst-the-ruins`, `blackfathom-villainy`, `hidden-enemies`: Fehler beim Abruf.
  - Die Mobalytics-Kopie der RoL-Seite (facefoot): Fehler beim Abruf.
  - Wowhead Classic 853: Seite leer.

---

## Umsetzung im Kombi-Guide 0.6 (16.10.)

Zeilen in `data/kombi/vorquests.csv`, nur in der Gruppe «Kombiguide (H)». Orte aus RXP (Weltkoordinaten) oder, wo RXP den NPC nicht führt, aus den Quellen oben (Spielkoordinaten, umgerechnet mit `data/karten/forever_karten.csv`).

| Dungeon | Wo im Guide | Zeilen | Ort aus |
|---|---|---|---|
| RFC | Thunder Bluff nach Cairne (Rahauro 5722, 5723); Orgrimmar vor «SpiritsPickup» (Thrall 5726, Neeru 5761); Unterstadt im Abstecher (Varimathras 5725); Abgaben 5724 und 5723 bei Rahauro in «17-22» | V1–V3, V14, V34, V35 | RXP v4.11.23 (Mulgore, Barrens, Horde-01-14_Undead.lua) |
| RoL | Abstecher nach der Berufssitzung in Orgrimmar: Zeppelin, Annahmen 92422, 92421, 95216 (ab 16), 92401, Lauf, Abgaben 95204, 95216, 97288, 92421, 92422, 92401 | V10–V13, V15, V17–V23 | RXP v4.11.23 (Zeppelin «ZeptoUC1», Kristof, Faranell), RXP-Hauptzweig (Tabitha, Eingang aus der Allianz-Route), Warcraft Tavern (Morbin, Griffs, Oran) |
| SFK | im Abstecher: 1013 bei Bel'dugur (ab 16); 1014 und 1098 im Grabmal (ab 18) | V16, V24 | Icy Veins und kami-labs (Bel'dugur, Widerspruch 7 offen), RXP v4.11.23 (Dalar, Hadrec) |
| WC | «12-17»: Bigglefuzz beim ersten Halt in Ratchet, Nalpak und Ebru an der Lushwater Oasis; «17-22»: Mebok nach der Abgabe von Raptor Horns, Bigglefuzz, Zamah, Nara | V41, V42, V30–V33 | RXP v4.11.23 (Speedrun- und Dungeon-Route) |
| RFK | «17-22»: Blueleaf Tubers bei Mebok (ab 20), im selben Schritt wie die WC-Quest | V30 | RXP (Mebok) |
| BFD | «17-22»: Je'neu Sancrea in Zoram'gar (6563, 6921 ab 21) | V36 | RXP v4.11.23 |

Nicht im Guide: Hall of Thanes (Allianz, keine Horde-Quests ausserhalb), Todesminen (nur Allianz), Quests ab Stufe 24 (Excavation Site, City of Dalaran, Gnomeregan, Scharlachrotes Kloster, RFK ausser Blueleaf Tubers, RFD) und Klassenquests anderer Klassen (Abschnitte 2, 5 und 7).

**RXPs Abbruch-Schritte.** RXPs Speedrun-Route (v4.11.23, `Guides/forever/Horde-12-22_Barrens.lua`) hat Schritte `.abandon` ohne `.dungeon`: in «17-22» nach dem Label «WCEnd» für 1486, 1487, 1491, 959, 914 und 962, am Ende von «17-22» unter anderem für 6563. Sie halten die Route auf, solange die Quest im Log steht (`functions.lua` `abandon`). Davor steht im Kombi-Guide je ein Kästchen «Gelesen» (V43, V44, nur mit einer dieser Quests im Log, `.isOnQuest`); wer den Dungeon noch machen will, setzt beim Abbruch-Schritt das Häkchen (offene Entscheidung 39). Die RFC-Abbrüche in «12-17» (5723, 5725, 5728, 5761) haben `.dungeon RFC` und erscheinen in Forever nicht.

**Stufen.** Die Zusatzschritte in «12-17» vor der Stelle #152 tragen `#maxlevel 17` (offene Entscheidung 37); wo eine Quest eine höhere Mindeststufe hat, blendet `.xp <N,1` den Schritt darunter aus (95216 und 1013 ab 16, 1014 und 1098 ab 18, 1221 nur im Text: ab 20).
