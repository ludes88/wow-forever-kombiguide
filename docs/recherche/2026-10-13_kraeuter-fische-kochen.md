# Recherche: Kräuter, Gewächshaus, Fischen und Kochen entlang der RXP-Route 1–22 (Horde), Stand 13.10.2026

Recherche durch einen Claude-Agenten am 13.10.2026 (42 Web-Abrufe; die AHledger-Seite zum Fischen liess sich nicht abrufen). Lokal gelesen: RXP-Klon Tag v4.11.13, Best Practice §8, §9, §11, `data/rechnung/Preise.csv`, `Quellen.csv`. Stichproben in der Hauptsitzung bestätigt: Deviate Fish (Lushwater 35 % von 153, PvP Horde 10s, 30T 6s 22c), Icy Veins Kräuterkunde (Gewächshaus «Skill to Place» 140, erste Zahlen der Krautzeilen), Frilled Lichen (PvP Horde 2g 72s, 30T 67s 80c, Briarthorn Southern Barrens 16 % von 51).

**Lesehilfe**
- **Märkte:** PH = AHledger PvP Horde US, NH = Normal Horde US. Beides sind Spieler-Scans aus der Forever-Beta. 30T = Median der letzten 30 Tage.
- **Keine EU-Preise:** Die EU-Märkte öffnen laut AHledger erst zum Start ([AHL 268415](https://ahledger.com/items/268415-commonplace-herb-seeds)).
- **«Markt»:** Gemeint ist die Tabelle «Most listed» auf der PH-Marktseite. Sie stammt aus einem einzigen Scan vom **13.10.2026 16:53 UTC**.
- **Item-Seiten:** Sie zeigen teils andere Scans. Den Zeitstempel trage ich in der jeweiligen Zeile mit; zu welchem Markt er gehört, sagt die Seite nicht immer.
- **«Händler zahlt»:** Das ist der Rückkaufpreis laut Fliesstext der AHledger-Item-Seite («buy it back for …»). Die Details-Tabelle derselben Seite vertauscht die Beschriftung (Widerspruch 11).
- **Kräuterkunde:** Die erste Zahl aus der Icy-Veins-Tabelle. Das ist die nötige Fertigkeit; die Seite belegt das am Beispiel Goldthorn 170. Die anderen drei Zahlen beschriftet sie nicht.
- **Bezug zur Route (RXP v4.11.13):** `.goto`-Befehle pro Karte gezählt.
  - «1-6» und «6-12 Mulgore»: Mulgore 126 und 362, Thunder Bluff 36
  - «12-17 The Barrens»: Brachland 469
  - «17-22 Stonetalon/Barrens/Ashenvale»: Brachland 231, Stonetalon 230, Ashenvale 112
  - «RXP ja» heisst: Das Teilgebiet steht im RXP-Text. «Nein» heisst nur, dass es dort nicht genannt wird. Ob die Route trotzdem durchführt, ist damit nicht geprüft.

**Quellen-Schlüssel (Kürzel in den Tabellen)**

| Kürzel | Link | Stand |
|---|---|---|
| AHL-Markt | https://ahledger.com/markets/forever/pvp/horde/us | Scan 13.10.2026 16:53 UTC |
| AHL-Mulgore / AHL-Brachland / AHL-Stonetalon / AHL-Ashenvale | https://ahledger.com/wow-forever/zones/mulgore · …/the-barrens · …/stonetalon-mountains · …/ashenvale | ohne Datum; Basis 6 / 17 / 7 / 8 Spieler; nur Sichtungen («seen N×»); Brachland und Stonetalon abgeschnitten |
| AHL-Kräuterkunde, AHL-Kochen | https://ahledger.com/wow-forever/professions/herbalism · …/cooking | ohne Datum |
| IV-Kräuter | https://www.icy-veins.com/wow-forever/herbalism | 11.10.2026, Abide |
| IV-Fischen | https://www.icy-veins.com/wow-forever/fishing | 11.10.2026, Abide |
| IV-Kochen | https://www.icy-veins.com/wow-forever/cooking | 11.10.2026, Abide |
| IV-Gewächshaus | https://www.icy-veins.com/wow-forever/news/greenhouse-blueprint-found-how-herbalism-seeds-work-in-wow-forever/ | 08.10.2026, Ease |
| IV-Samen | https://www.icy-veins.com/wow-forever/news/players-are-already-looting-seeds-for-a-wow-forever-greenhouse-no-one-can-craft-yet/ | 30.09.2026, Ease |
| IV-Excavation | https://www.icy-veins.com/wow-forever/excavation-site-wetlands-guide | 03.10.2026, Neryssa |
| WT-Kräuter | https://www.warcrafttavern.com/forever/guides/herbalism/ | ohne Datum (Bilder 2026/10) |
| Moba-Kräuter | https://mobalytics.gg/wow-forever/guides/herbalism-profession-guide | ohne Datum, Platzhalter-Guide |
| SM-Kochen | https://seemeta.com/en/wow-forever/professions/cooking | 10.10.2026, 1.60.1 beta; Liste abgeschnitten |
| WP-Fischen | https://www.wow-professions.com/forever/fishing-and-cooking-leveling-guide | ohne Datum, «still in progress» |
| wowtbc | https://wowtbc.gg/warcraftforever/loot-tables/dungeons/excavation-site-wetlands/ | ohne Datum |
| RXP | https://github.com/RestedXP/RXPGuides/tree/v4.11.13 (`Guides/forever/Horde-1-12_Mulgore.lua`, `Horde-12-22_Barrens.lua`) | Tag v4.11.13 |

---

## 1. Kräuter entlang der Route

| Kraut (ID) | Kräuterkunde | Wo (Teilgebiet, Sichtungen) | AH PH (Markt) | Weitere Preise (Item-Seite) | Händler zahlt | Besonderheiten | Quelle | Stand |
|---|---|---|---|---|---|---|---|---|
| Peacebloom (2447) | 1 | **Mulgore:** The Golden Plains 9×; Red Cloud Mesa («Wilted Peacebloom»). **Brachland:** Southern Barrens 26× | 80c (min 75c, 1'802 Stk.) | – | nicht abgerufen | Commonplace Herb Seeds: 1 % von 107 Beutefenstern (Durotar); Zutat der Incense Candle | [IV-Kräuter](https://www.icy-veins.com/wow-forever/herbalism), [AHL-Mulgore](https://ahledger.com/wow-forever/zones/mulgore), [AHL-Brachland](https://ahledger.com/wow-forever/zones/the-barrens), [AHL-Markt](https://ahledger.com/markets/forever/pvp/horde/us), [AHL 268415](https://ahledger.com/items/268415-commonplace-herb-seeds), [Moba](https://mobalytics.gg/wow-forever/guides/herbalism-profession-guide) | Markt 13.10. 16:53 |
| Silverleaf (765) | 1 | **Mulgore:** Galak Camp 21× (RXP «Galak» ja); Red Cloud Mesa («Stunted Silverleaf»). **Brachland:** Grol'dom Farm, gesamt 39× | 1s (min 95c, 1'513; +376,2 % zu 7 Tagen) | – | nicht abgerufen | Commonplace Herb Seeds: Mulgore Stonebull Lake 2×; Durotar 3 % von 67 | [AHL-Mulgore](https://ahledger.com/wow-forever/zones/mulgore), [AHL-Markt](https://ahledger.com/markets/forever/pvp/horde/us), [AHL 268415](https://ahledger.com/items/268415-commonplace-herb-seeds) | Markt 13.10. 16:53 |
| Earthroot (2449) | 15 | IV nennt Mulgore und Brachland als Hauptzonen; AHL-Mulgore führt Earthroot nicht. **Brachland:** The Dry Hills, 38× | 2s 70c (min 2s 30c, 2'157) | – | nicht abgerufen | Frilled Lichen aus Earthroot: Southern Barrens; Durotar 15 % von 39 | [IV-Kräuter](https://www.icy-veins.com/wow-forever/herbalism), [AHL-Brachland](https://ahledger.com/wow-forever/zones/the-barrens), [AHL 249399](https://ahledger.com/items/249399-frilled-lichen) | Markt 13.10. 16:53 |
| Mageroyal (785) | 50 | **Brachland:** Southern Barrens (98 % von 66), Agama'gor, 74×. **Stonetalon:** Blackwolf River 6×. **Ashenvale:** Zoram Strand 2× (RXP ja), Lake Falathim 6× | nicht in «Most listed» | PH 70c (min 56c, 1'978), 30T 1s 8c; NH 74c, 30T 1s 18c | 20c | Händler Jeeda (Sun Rock Retreat) verkauft es für 72c; Swiftthistle 12 % von 66 (Agama'gor); Uncommon Herb Seeds 4 % von 79 (Redridge) | [AHL 785](https://ahledger.com/items/785-mageroyal), [AHL 2452](https://ahledger.com/items/2452-swiftthistle), [AHL 268416](https://ahledger.com/items/268416-uncommon-herb-seeds) | Seite 13.10. 15:49 UTC |
| Briarthorn (2450) | 70 | **Brachland:** Southern Barrens (98 % von 51), Lushwater Oasis (RXP ja), 51×. **Stonetalon:** Webwinder Path 11×. **Ashenvale:** Silverwing Outpost 6× (RXP ja), Ruins of Stardust 9× | 3s 75c (min 1s 79c, 8'920; +106 %) | PH 1s 25c, 30T 1s 98c; NH 1s 34c | 25c | Aus Briarthorn (Southern Barrens): Swiftthistle 33 % von 51, Frilled Lichen 16 % von 51 | [AHL 2450](https://ahledger.com/items/2450-briarthorn), [AHL-Markt](https://ahledger.com/markets/forever/pvp/horde/us), [AHL 2452](https://ahledger.com/items/2452-swiftthistle), [AHL 249399](https://ahledger.com/items/249399-frilled-lichen) | Markt 13.10. 16:53; Seite 12.10. 17:21 UTC |
| Swiftthistle (2452) | kein eigener Knoten; Zusatzbeute aus Mageroyal und Briarthorn | Brachland (siehe oben); **Stonetalon:** Webwinder Path 6×. **Ashenvale:** Ruins of Stardust 4× | 11s 11c (min 7s 99c, 4'165) | 30T 6s 30c; NH 2s 10c, 30T 2s 92c | 15c | Kochrezept Thistle Tea (SM 60/100/120/140) | [AHL 2452](https://ahledger.com/items/2452-swiftthistle), [IV-Kräuter](https://www.icy-veins.com/wow-forever/herbalism), [SM-Kochen](https://seemeta.com/en/wow-forever/professions/cooking) | Markt 13.10. 16:53 (gleich wie Item-Seite) |
| Bruiseweed (2453) | 100 | **Brachland:** Field of Giants 18×. **Stonetalon:** Windshear Crag (RXP ja), The Charred Vale, 15×. **Ashenvale:** Nightsong Woods 4× | 2s 30c (min 1s 91c, 3'353) | – | nicht abgerufen | Frilled Lichen aus Bruiseweed (Ashenvale, Shrine of Aessina) | [IV-Kräuter](https://www.icy-veins.com/wow-forever/herbalism), [AHL-Brachland](https://ahledger.com/wow-forever/zones/the-barrens), [AHL-Stonetalon](https://ahledger.com/wow-forever/zones/stonetalon-mountains), [AHL-Ashenvale](https://ahledger.com/wow-forever/zones/ashenvale) | Markt 13.10. 16:53 |
| Stranglekelp (3820) | 85 (wächst nur unter Wasser, WT) | **Ashenvale:** Zoram Strand 2× (RXP ja). **Stonetalon:** 5× beim Fischen im Blackwolf River | 8s 50c (min 7s 75c, 4'195) | – | nicht abgerufen | – | [AHL-Ashenvale](https://ahledger.com/wow-forever/zones/ashenvale), [AHL-Stonetalon](https://ahledger.com/wow-forever/zones/stonetalon-mountains), [WT](https://www.warcrafttavern.com/forever/guides/herbalism/) | Markt 13.10. 16:53 |
| Wild Steelbloom (3355) | 115 | **Stonetalon:** Webwinder Path 8× | 16s (min 12s 48c, 1'630) | – | nicht abgerufen | – | [AHL-Stonetalon](https://ahledger.com/wow-forever/zones/stonetalon-mountains), [AHL-Markt](https://ahledger.com/markets/forever/pvp/horde/us) | Markt 13.10. 16:53 |
| Kingsblood (3356) | 125 | **Brachland:** Blackthorn Ridge 11×. **Stonetalon:** Windshear Crag 18× (RXP ja) | nicht in «Most listed» | PH 13s 75c (min 5s 55c, 1'271), 30T 6s 6c; NH 8s 86c, 30T 7s 27c | 30c | Ergebnis von Uncommon Herb Seeds; Zutat u. a. der Herbalist's Gloves (Lederverarbeitung) | [AHL 3356](https://ahledger.com/items/3356-kingsblood), [AHL-Stonetalon](https://ahledger.com/wow-forever/zones/stonetalon-mountains), [IV-Gewächshaus](https://www.icy-veins.com/wow-forever/news/greenhouse-blueprint-found-how-herbalism-seeds-work-in-wow-forever/) | PH-Scan 11.10. 13:08 UTC |
| Frilled Lichen (249399) | kein eigener Knoten; seltene Zusatzbeute («scarce»), neu in Forever | **Brachland:** aus Briarthorn, Earthroot und Mageroyal (Southern Barrens) 14×. **Stonetalon:** aus Mageroyal und Kingsblood 5×. **Ashenvale:** aus Bruiseweed 2× | nur unter «Biggest value» | PH 2g 72s (min 2g 45s 65c, 407), 30T 67s 80c; NH 80s 80c, 30T 43s 99c | 30c | Einzige Verwendung: Cerulean Dye (Alchemie); das Talent Bountiful Harvest erhöht die Ausbeute an Scarce-Material | [AHL 249399](https://ahledger.com/items/249399-frilled-lichen), [IV-Kräuter](https://www.icy-veins.com/wow-forever/herbalism), [WT](https://www.warcrafttavern.com/forever/guides/herbalism/) | Seite 13.10. 18:32 UTC |
| Commonplace Herb Seeds (268415) | – | **Mulgore:** aus Silverleaf, Stonebull Lake 2× | – | PH 18c (279 Stk.), 30T 68c; NH 10c | 10c | Ergibt Peacebloom oder Earthroot | [AHL 268415](https://ahledger.com/items/268415-commonplace-herb-seeds), [IV-Gewächshaus](https://www.icy-veins.com/wow-forever/news/greenhouse-blueprint-found-how-herbalism-seeds-work-in-wow-forever/) | Seite 13.10. 16:27 UTC |
| Uncommon Herb Seeds (268416) | – | **Ashenvale:** Zoram Strand 2× (RXP ja) | – | PH 5s 55c (nur 34 Stk.), 30T 6s 60c; NH 1s 26c | 25c | Ergibt Silverleaf oder Kingsblood | [AHL 268416](https://ahledger.com/items/268416-uncommon-herb-seeds), [AHL-Ashenvale](https://ahledger.com/wow-forever/zones/ashenvale), [IV-Gewächshaus](https://www.icy-veins.com/wow-forever/news/greenhouse-blueprint-found-how-herbalism-seeds-work-in-wow-forever/) | Seite 11.10. 13:50 UTC |

**Auf der Route nicht belegt:**
- Liferoot (3357, Kräuterkunde 150, Markt 9s 54c): Die Hauptzonen bei Icy Veins enthalten keines der vier Routengebiete, und die vier AHL-Zonenseiten der Route führen Liferoot nicht.
- Purple Lotus: siehe Widerspruch 4.

---

## 2. Gewächshaus (Greenhouse) und Samen

| Punkt | Befund | Quelle | Stand |
|---|---|---|---|
| Bauplan | «Blueprint: Greenhouse» (Herbalism Recipe) aus der Beute von Shadetooth, dem 2. von 3 Bossen (Saltspine, Shadetooth, Relic Guardian) | [IV-Excavation](https://www.icy-veins.com/wow-forever/excavation-site-wetlands-guide), [IV-Gewächshaus](https://www.icy-veins.com/wow-forever/news/greenhouse-blueprint-found-how-herbalism-seeds-work-in-wow-forever/) | 03.10. / 08.10. |
| Dropchance | **keine Quelle.** wowtbc führt den Bauplan nicht («Loot is still being discovered») | [wowtbc](https://wowtbc.gg/warcraftforever/loot-tables/dungeons/excavation-site-wetlands/) | ohne Datum |
| Dungeon-Stufe und Ort | «tuned for Level 26-33». Wetlands, «just south of the Thelgen Rock cavern», ohne Koordinaten. 8 Quests, davon 3 nur für die Horde. Bei wowtbc haben alle Quests Stufe 24 | [IV-Excavation](https://www.icy-veins.com/wow-forever/excavation-site-wetlands-guide), [wowtbc](https://wowtbc.gg/warcraftforever/loot-tables/dungeons/excavation-site-wetlands/) | 03.10. |
| Kräuterkunde zum Bauen und Platzieren | **140.** IV-Kräuter: «Skill to Place» 140. IV-Samen: «Herbalism skill level 140» als Herstellungsanforderung | [IV-Kräuter](https://www.icy-veins.com/wow-forever/herbalism), [IV-Samen](https://www.icy-veins.com/wow-forever/news/players-are-already-looting-seeds-for-a-wow-forever-greenhouse-no-one-can-craft-yet/) | 11.10. / 30.09. |
| Kräuterkunde zum Pflanzen und Ernten | **keine Quelle** | – | – |
| Material | 2 Simple Wood, 1 Arthas' Tears, 1 Purple Lotus (Item 279964, Rezept-Zauber 1262980) | [Moba](https://mobalytics.gg/wow-forever/guides/herbalism-profession-guide), [AHL-Kräuterkunde](https://ahledger.com/wow-forever/professions/herbalism) | ohne Datum |
| Wo das Material wächst | **Arthas' Tears:** Western Plaguelands, Felwood; Kräuterkunde 220. **Purple Lotus:** Kräuterkunde 210, Fundort umstritten (Widerspruch 4) | [IV-Samen](https://www.icy-veins.com/wow-forever/news/players-are-already-looting-seeds-for-a-wow-forever-greenhouse-no-one-can-craft-yet/), [IV-Kräuter](https://www.icy-veins.com/wow-forever/herbalism) | 30.09. / 11.10. |
| Kosten | **Simple Wood:** NH 70c (09.10.). **Purple Lotus:** PH 50s 79c, NH 20g 5s (Ausreisser; NH 30T 1g 8s 19c), Stand 11.10. **Arthas' Tears:** nicht abgerufen | `data/rechnung/Preise.csv` (AHL-Links dort) | 09.–11.10. |
| Bedingungen | Braucht ein Lagerfeuer in der Nähe. Gibt den Bonus der Incense Candle und kann eine Incense Candle ersetzen | [Moba](https://mobalytics.gg/wow-forever/guides/herbalism-profession-guide), [IV-Samen](https://www.icy-veins.com/wow-forever/news/players-are-already-looting-seeds-for-a-wow-forever-greenhouse-no-one-can-craft-yet/) | – |
| Ablauf und Zeiten | Beim Lager entsteht eine Pflanzkiste. Das Kraut ist nach **8 Minuten** erntbar. Das Gewächshaus hält **15 Minuten**, also geht nur 1 Samen pro Gewächshaus | [IV-Gewächshaus](https://www.icy-veins.com/wow-forever/news/greenhouse-blueprint-found-how-herbalism-seeds-work-in-wow-forever/) | 08.10. |
| Abklingzeit | Alle Lager-Gegenstände teilen sich 3600 s (1 Stunde) | [Moba](https://mobalytics.gg/wow-forever/guides/herbalism-profession-guide), [IV-Kräuter](https://www.icy-veins.com/wow-forever/herbalism) | – |
| Welche Samenstufe welche Kräuter ergibt | **Commonplace:** Peacebloom, Earthroot. **Uncommon:** Silverleaf, Kingsblood. **Scarce:** «Ghost Shroom». Unusual Herb Seeds gibt es auch (WT), ihr Ergebnis ist offen | [IV-Gewächshaus](https://www.icy-veins.com/wow-forever/news/greenhouse-blueprint-found-how-herbalism-seeds-work-in-wow-forever/), [WT](https://www.warcrafttavern.com/forever/guides/herbalism/) | 08.10. |
| Wie man Samen bekommt | Beim Kräutersammeln (IV-Samen). Raten bei AHledger: **Commonplace** aus Silverleaf 3 % von 67 (Durotar), aus Peacebloom 1 % von 107 (Durotar), Mulgore Stonebull Lake 2× ohne Rate. **Uncommon** aus Mageroyal 4 % von 79 (Redridge), Ashenvale Zoram Strand 2× | [IV-Samen](https://www.icy-veins.com/wow-forever/news/players-are-already-looting-seeds-for-a-wow-forever-greenhouse-no-one-can-craft-yet/), [AHL 268415](https://ahledger.com/items/268415-commonplace-herb-seeds), [AHL 268416](https://ahledger.com/items/268416-uncommon-herb-seeds) | 30.09. / 11.–13.10. |
| Ertrag pro Ernte | **keine Quelle** | – | – |
| Seed Hybridizer | Kräuterkunde 300. Material: 4 Mountain Silversage, 1 Crystal Vial, 2 Runecloth. Vermehrt Samen oder kombiniert sie zu selteneren Stufen | [IV-Kräuter](https://www.icy-veins.com/wow-forever/herbalism), [Moba](https://mobalytics.gg/wow-forever/guides/herbalism-profession-guide) | 11.10. |
| Incense Candle | Kräuterkunde 20, vom Lehrer. 1 Peacebloom und 1 Silverleaf. +25 Intelligenz (Moba); stapelt nicht mit Arcane Intellect | [IV-Kräuter](https://www.icy-veins.com/wow-forever/herbalism), [Moba](https://mobalytics.gg/wow-forever/guides/herbalism-profession-guide) | 11.10. |

Folgerung aus den Belegen: Das Gewächshaus braucht einen Bauplan aus einem Dungeon für Stufe 26–33, Kräuterkunde 140 und zwei Zutaten, die man erst ab Kräuterkunde 210 bzw. 220 selbst sammelt. Zwischen Stufe 1 und 22 fallen davon nur die Samen an (Preise in Tabelle 1).

---

## 3. Angelplätze entlang der Route

| Ort | Koordinaten | Fänge (Anteil der Beutefenster) | Ab wann nichts entkommt | Schwärme | Quelle | Stand |
|---|---|---|---|---|---|---|
| **Mulgore, Stonebull Lake** (1–12) | Für die Angelstelle keine. Lehrer Uthan Stillwater: `/mappin 1412 44.6 60.6`, bei IV mit «Bloodhoof Village» | Brilliant Smallfish und Longjaw Mud Snapper. WP für 1–75: «about 45 Brilliant Smallfish and 30 Longjaw Mud Snapper». Keine Raten | 25 laut Best Practice §9 (wow-professions); am 13.10. nicht wiedergefunden | keine Quelle | [WP-Fischen](https://www.wow-professions.com/forever/fishing-and-cooking-leveling-guide), [IV-Fischen](https://www.icy-veins.com/wow-forever/fishing) | ohne Datum / 11.10. |
| **Thunder Bluff, Teich beim Auktionshaus** (WP). Steht in RXP «6-12 Mulgore», Z. 2160–2164: «Fish in the pond» für Quest 76240 | keine | Longjaw 59 %, Catfish 26 %, Smallfish 13 % (je von 137) | **75** («From 75 no fish gets away») | keine Quelle | [AHL 6289](https://ahledger.com/items/6289-raw-longjaw-mud-snapper), [AHL 6308](https://ahledger.com/items/6308-raw-bristle-whisker-catfish), [AHL 6291](https://ahledger.com/items/6291-raw-brilliant-smallfish), [WP-Fischen](https://www.wow-professions.com/forever/fishing-and-cooking-leveling-guide), RXP | 13.10. |
| **Brachland, Lushwater Oasis.** Steht in RXP «12-17»: `.subzone 387`, Z. 2795 | keine | Longjaw 39 %, **Deviate Fish 35 %**, Catfish 12 %, Smallfish 8 % (je von 153) | keine Quelle | keine Quelle | [AHL 6522](https://ahledger.com/items/6522-deviate-fish), [AHL 6289](https://ahledger.com/items/6289-raw-longjaw-mud-snapper), [AHL 6308](https://ahledger.com/items/6308-raw-bristle-whisker-catfish), [AHL 6291](https://ahledger.com/items/6291-raw-brilliant-smallfish), [AHL-Brachland](https://ahledger.com/wow-forever/zones/the-barrens) | 12.–13.10. |
| Brachland, Stagnant Oasis (RXP: Quest 877) und Oasen allgemein | keine | IV: Deviate Fish in «Oasis waters in The Barrens». AHL zeigt an der Stagnant Oasis keine Fänge | keine Quelle | keine Quelle | [IV-Fischen](https://www.icy-veins.com/wow-forever/fishing) | 11.10. |
| Brachland, Küste (Ratchet, RXP `.subzone 392`) | keine | IV: Oily Blackmouth an den Küsten des Brachlands. AHL-Brachland zeigt keine Küstenfänge | keine Quelle | keine Quelle | [IV-Fischen](https://www.icy-veins.com/wow-forever/fishing) | 11.10. |
| **Stonetalon, Blackwolf River** (offenes Wasser; im RXP-Text nicht genannt) | keine | **AHL**, nur Sichtungen: Firefin Snapper 34×, Stranglekelp 5×, Rumsey Rum Dark 2×, Watertight Trunk 2×. **WP** für Fertigkeit 130–205, offenes Wasser in Stonetalon: «about 95 Longjaw Mud Snapper and 145 Bristle Whisker Catfish»; Nightcrawlers bei Kulwia (Sun Rock Retreat) | keine Quelle | keine Quelle | [AHL-Stonetalon](https://ahledger.com/wow-forever/zones/stonetalon-mountains), [WP-Fischen](https://www.wow-professions.com/forever/fishing-and-cooking-leveling-guide) | ohne Datum |
| **Ashenvale** | keine | **AHL:** keine Fänge. Catfish fällt als Beute von Wrathtail-Gegnern am Zoram Strand: Myrmidon 10 % von 20, Razortail 5 % von 44, Wave Rider 4 % von 51. **WP:** Mystral Lake (Shandrina verkauft Expert Cookbook und Nightcrawlers), «targets match Stonetalon». Mystral Lake steht nicht im RXP-Text | keine Quelle | keine Quelle | [AHL-Ashenvale](https://ahledger.com/wow-forever/zones/ashenvale), [AHL 6308](https://ahledger.com/items/6308-raw-bristle-whisker-catfish), [WP-Fischen](https://www.wow-professions.com/forever/fishing-and-cooking-leveling-guide) | – |
| Schwärme allgemein | – | IV beschreibt Schools und Floating Wreckage nur allgemein, ohne Orte auf der Route. Für Raw Sagefish nennt die AHL-Item-Seite keinen Fangort | – | **auf der Route nicht belegt** | [IV-Fischen](https://www.icy-veins.com/wow-forever/fishing), [AHL 21071](https://ahledger.com/items/21071-raw-sagefish) | 11.–13.10. |

**Ränge, Köder und Lager beim Fischen** ([IV-Fischen](https://www.icy-veins.com/wow-forever/fishing), 11.10.)
- **Ränge:** Journeyman ab Fertigkeit 50 und Stufe 10. Expert ab 125 und Stufe 20, über das Buch von Old Man Heming in Booty Bay (`/mappin 1434 27.4 77.0`).
- **Köder:** Shiny Bauble +25; Nightcrawlers +50, ab Fischen 50; Bright Baubles +75, ab Fischen 100; Aquadynamic Fish Attractor +100, ab Fischen 100. Harn Longcast in Bloodhoof verkauft Nightcrawlers und Bright Baubles ([AHL-Mulgore](https://ahledger.com/wow-forever/zones/mulgore)).
- **Lager:** Die Fish Bowl gibt es ab Fischen 20 beim Lehrer: +8 % alle Werte, stapelt nicht mit Blessing of Kings. Das Fishing Rack braucht Fischen 140.

---

## 4. Kochen

**4a. Fische**

| Rohfisch (ID) | Gericht (ID) | Kochen (orange/gelb/grün/grau) | Rezeptquelle | AH roh | AH gekocht | Händler zahlt (roh) | Quelle | Stand |
|---|---|---|---|---|---|---|---|---|
| Raw Brilliant Smallfish (6291) | Brilliant Smallfish (6290) | SM: 1/45/65/85. AHL: Mindestfertigkeit 5 | Harn Longcast, Bloodhoof (AHL-Mulgore, WP); 40c laut Best Practice §9, nicht neu geprüft. AHL-Kochen nennt «trainer» | PH 1s 18c (30T 1s 36c); NH 1s 9c | PH 1s 25c (Markt) | 1c | [AHL 6291](https://ahledger.com/items/6291-raw-brilliant-smallfish), [SM-Kochen](https://seemeta.com/en/wow-forever/professions/cooking), [AHL-Kochen](https://ahledger.com/wow-forever/professions/cooking), [AHL-Mulgore](https://ahledger.com/wow-forever/zones/mulgore), [AHL-Markt](https://ahledger.com/markets/forever/pvp/horde/us) | roh 13.10. 03:52 UTC; gekocht 13.10. 16:53 |
| Raw Longjaw Mud Snapper (6289) | Longjaw Mud Snapper (4592) | SM: 50/90/110/130. AHL: 50 | Harn Longcast (Bloodhoof); Naal Mistrunner (Thunder Bluff) laut WP; 4s laut Best Practice §9 | PH 6c (30T 20c); NH 12c | nicht abgerufen | 1c. Händler verkaufen ihn für 20c, u. a. Kilxx (Ratchet) und Wik'Tar (Zoram'gar) | [AHL 6289](https://ahledger.com/items/6289-raw-longjaw-mud-snapper), [WP-Fischen](https://www.wow-professions.com/forever/fishing-and-cooking-leveling-guide) | 13.10. 01:11 UTC |
| Raw Bristle Whisker Catfish (6308) | Bristle Whisker Catfish (4593) | AHL: 100. Farben: keine Forever-Quelle (SM-Liste abgeschnitten) | Naal Mistrunner (Thunder Bluff) laut WP; 12s laut Best Practice §9 | PH 18c (30T 58c); NH 39c | nicht abgerufen. AHL rechnet für PH −10c pro Herstellung | 2c | [AHL 6308](https://ahledger.com/items/6308-raw-bristle-whisker-catfish) | 13.10. 01:11 UTC |
| Deviate Fish (6522) | Savory Deviate Delight (6657) | AHL und IV: 85. Farben: keine Quelle | «Drops in The Barrens» (IV). Welche Gegner und welche Rate: keine Quelle | PH 10s (30T 6s 22c); NH 5s | **PH 19s 98c** (min 13s 70c, 3'183) | 4c | [AHL 6522](https://ahledger.com/items/6522-deviate-fish), [IV-Kochen](https://www.icy-veins.com/wow-forever/cooking), [AHL-Markt](https://ahledger.com/markets/forever/pvp/horde/us) | roh 12.10. 19:16 UTC; gekocht 13.10. 16:53 |
| Raw Rainbow Fin Albacore (ID 6361 laut AHL-Brachland) | Rainbow Fin Albacore (5095) | SM: 50/90/110/130. AHL: 50 | AHL: «trainer» | nicht abgerufen | nicht abgerufen | nicht abgerufen | [AHL-Brachland](https://ahledger.com/wow-forever/zones/the-barrens), [AHL-Kochen](https://ahledger.com/wow-forever/professions/cooking) | – |
| Firefin Snapper (6359) | kein Kochrezept; Zutat von Fire Oil (Alchemie 110, 2 Stück) | – | – | Markt PH 44c; Item-Seite PH 59c (30T 52c); NH 4s 99c | – | 5c (Details-Tabelle) | [AHL 6359](https://ahledger.com/items/6359-firefin-snapper), [AHL-Markt](https://ahledger.com/markets/forever/pvp/horde/us) | Markt 13.10. 16:53; Seite 29.09. 18:16 UTC |
| Oily Blackmouth (ID nicht abgerufen) | Kochrezept nicht abgerufen. Blackmouth Oil steht im Markt bei 14s 40c, der Beruf ist nicht abgerufen | – | – | PH 5s 87c (Markt) | – | nicht abgerufen | [AHL-Markt](https://ahledger.com/markets/forever/pvp/horde/us), [IV-Fischen](https://www.icy-veins.com/wow-forever/fishing) | 13.10. 16:53 |

Zu Rainbow Fin Albacore: Im Brachland fällt der Rohfisch nur als Beute von Oasis Snapjaw (Lushwater) und Bruuz (Merchant Coast), nicht beim Fischen (AHL-Brachland).

**4b. Fleisch von Gegnern** (AH roh = PH, Markt 13.10.2026 16:53 UTC)

| Fleisch (ID) | Wer es auf der Route fallen lässt | Gericht (ID), Kochen | Rezeptquelle | AH roh | AH gekocht | Quelle |
|---|---|---|---|---|---|---|
| Stringy Wolf Meat (2672) | **Mulgore:** Prairie Stalker, Prairie Wolf, Prairie Wolf Alpha (Golden Plains), 26× | **Charred Wolf Meat (2679):** SM –/45/65/85; AHL 5. **Spiced Wolf Meat (2680):** SM –/50/70/90; AHL 10, dazu Mild Spices. SM zeigt bei Lehrer-Rezepten nur 3 Zahlen | Lehrer (SM); bei Charred Wolf Meat nennt AHL «unknown» | 1s 80c (min 1s 36c, 935) | nicht abgerufen | [AHL-Mulgore](https://ahledger.com/wow-forever/zones/mulgore), [SM-Kochen](https://seemeta.com/en/wow-forever/professions/cooking), [AHL-Kochen](https://ahledger.com/wow-forever/professions/cooking) |
| Kodo Meat (ID nicht abgerufen) | AHL-Mulgore führt keine Drops; auf AHL-Brachland (abgeschnitten) nicht gelistet | **Roasted Kodo Meat (5474):** SM 35/75/95/115; AHL 35, ergibt 2, dazu Mild Spices | Wunna Darkmane, Bloodhoof (AHL-Mulgore); 2s 40c laut Best Practice §9 | nicht abgerufen | nicht abgerufen | [AHL-Mulgore](https://ahledger.com/wow-forever/zones/mulgore), [AHL-Kochen](https://ahledger.com/wow-forever/professions/cooking) |
| Strider Meat (5469) | **Brachland:** Greater Plainstrider (Thorn Hill), Ornery Plainstrider (Honor's Stand), Fleeting Plainstrider (Dreadmist Peak), 111× | **Strider Stew (5477):** SM 50/90/110/130; AHL 50, ergibt 2, dazu Shiny Red Apple | Tari'qa (Crossroads) laut Best Practice §9; AHL-Kochen nennt «trainer» | 38c (min 15c, 1'357) | nicht abgerufen | [AHL-Brachland](https://ahledger.com/wow-forever/zones/the-barrens), [AHL-Markt](https://ahledger.com/markets/forever/pvp/horde/us) |
| Thunder Lizard Tail (5470) | **Brachland:** Stormsnout (Agama'gor), Thunderhead (Southern Barrens), Stormhide (Field of Giants), 19× | **Crispy Lizard Tail (5479):** AHL 100, ergibt 2, dazu Hot Spices (Markt 1s 90c). Farben: keine Quelle | Tari'qa, Crossroads (AHL-Brachland, 12×) | nicht abgerufen | nicht abgerufen | [AHL-Brachland](https://ahledger.com/wow-forever/zones/the-barrens), [AHL-Kochen](https://ahledger.com/wow-forever/professions/cooking) |
| Crawler Meat (ID nicht abgerufen) | auf den AHL-Seiten der Route nicht gelistet | **Crab Cake (2683):** SM –/115/135/155 (Lehrer); AHL 75; dazu Mild Spices | Lehrer (SM) | nicht abgerufen | nicht abgerufen | [SM-Kochen](https://seemeta.com/en/wow-forever/professions/cooking), [AHL-Kochen](https://ahledger.com/wow-forever/professions/cooking) |
| Raptor Flesh (ID nicht abgerufen) | auf den AHL-Seiten der Route nicht gelistet | **Twice-Spiced Raptor Slice (250077, neu):** SM 75/115/133/150; AHL 75; dazu 2 Mild Spices | AHL: «trainer» | nicht abgerufen | nicht abgerufen | dito |
| Raptor Egg | Drops: keine Quelle | **Tasty Raptor Bites (250079, neu):** SM 25/35/55/75; AHL 1; dazu 4 Mild Spices | AHL: «trainer» | 1s 15c | nicht abgerufen | [AHL-Markt](https://ahledger.com/markets/forever/pvp/horde/us), [SM-Kochen](https://seemeta.com/en/wow-forever/professions/cooking) |
| Big Bear Meat (3730) | **Ashenvale:** Ashenvale Bear (Talondeep Path, RXP ja) u. a., 19× | Kochrezept: keine Quelle. AHL nennt «Recipe: Bear Brisket» (250182) als Beute von Ashenvale Bear, ohne Beruf | – | **9s 70c** (min 5s 90c, 3'081; +629,3 %) | – | [AHL-Ashenvale](https://ahledger.com/wow-forever/zones/ashenvale), [AHL-Markt](https://ahledger.com/markets/forever/pvp/horde/us) |
| Stag Meat (5471) | **Stonetalon:** Antlered Courser (Mirkfallon Lake) 13×. **Ashenvale:** Shadowhorn Stag, Wild Buck 19× | Rezept: keine Quelle | – | 99c | – | [AHL-Stonetalon](https://ahledger.com/wow-forever/zones/stonetalon-mountains), [AHL-Ashenvale](https://ahledger.com/wow-forever/zones/ashenvale) |
| Crisp Spider Meat (1081) | **Stonetalon:** Deepmoss 39×. **Ashenvale:** 6×. **Mulgore:** Gloomrise 3× | Rezept: keine Quelle | – | 50c | – | dito, [AHL-Mulgore](https://ahledger.com/wow-forever/zones/mulgore) |
| Clam Meat (5503) / Tangy Clam Meat (5504) | aus Behältern: Brachland 22×, Ashenvale 32× bzw. 2× | **Boiled Clams (5525):** SM –/90/110/130; AHL 50. **Goblin Deviled Clams (5527):** AHL 125, dazu Hot Spices | Lehrer (SM) | Tangy Clam Meat 50c | Goblin Deviled Clams 1s 96c | [AHL-Markt](https://ahledger.com/markets/forever/pvp/horde/us), [AHL-Kochen](https://ahledger.com/wow-forever/professions/cooking) |

**Wirkung** ([IV-Kochen](https://www.icy-veins.com/wow-forever/cooking), 11.10.)
- Wortlaut: «Most foods in WoW Forever also grant Well Fed XP Boost, increasing experience gained from kills by 5% while the food buff is active.»
- Der Bonus gilt nur für XP aus Kills, nicht für Quest-Belohnungen. Die meisten Food-Buffs halten 15 Minuten. Ob ein Gericht den Bonus hat, zeigt der Tooltip.
- Werte für Ausdauer oder Willenskraft je Gericht: keine Quelle abgerufen.
- Savory Deviate Delight: «Transforms you into a human ninja or pirate.»
- Basic Campfire: +4 Willenskraft ([SM-Kochen](https://seemeta.com/en/wow-forever/professions/cooking)).

**Kochlehrer auf der Route** ([IV-Kochen](https://www.icy-veins.com/wow-forever/cooking))
- Pyall Silentstride (Bloodhoof), Aska Mistrunner (Thunder Bluff, Central Rise), Duhng (Aussenposten südöstlich der Crossroads).
- Ränge: Journeyman ab 50. Expert ab 125 über das Expert Cookbook von Wulan (Shadowprey Village, Desolace); laut [WP](https://www.wow-professions.com/forever/fishing-and-cooking-leveling-guide) auch bei Shandrina (Mystral Lake, Ashenvale). Artisan ab 225 und Stufe 35.
- In RXP v4.11.13 lernt man Kochen in «6-12 Mulgore» bei Z. 860 (`.train 2550`) und Fischen bei Z. 2134 (`.train 7734`).

---

## 5. Höchster AH-Wert je Stufenbereich (nur belegte Zahlen, keine Mengen pro Stunde)

Werte: PH, Markt 13.10.2026 16:53 UTC, sonst mit Datum. Die Kräuterkunde-Schwelle steht dabei; ob sie in diesem Stufenbereich erreicht wird, ist nicht geschätzt.

| Stufen | Gebiete (RXP) | Kraut vom Knoten: höchster Wert | Zusatzbeute | Fisch roh: höchster | Fisch gekocht: höchster |
|---|---|---|---|---|---|
| 1–12 | Mulgore, Thunder Bluff | **Earthroot 2s 70c** (ab 15; in Mulgore nur laut IV belegt), danach Silverleaf 1s, Peacebloom 80c | Commonplace Herb Seeds 18c | **Raw Brilliant Smallfish 1s 18c** (13.10. 03:52); Catfish 18c, Longjaw 6c | **Brilliant Smallfish 1s 25c** |
| 12–17 | Brachland | **Kingsblood 13s 75c** (ab 125; Blackthorn Ridge; PH-Scan 11.10.), danach Briarthorn 3s 75c (ab 70), Earthroot 2s 70c, Bruiseweed 2s 30c (ab 100), Mageroyal 70c | **Frilled Lichen 2g 72s** (13.10. 18:32); Swiftthistle 11s 11c | **Deviate Fish 10s** (Lushwater 35 %; 12.10.) | **Savory Deviate Delight 19s 98c** (Kochen 85, Rezept als Drop) |
| 17–22 | Stonetalon, Brachland, Ashenvale | **Wild Steelbloom 16s** (ab 115; Webwinder Path), danach Kingsblood 13s 75c, Stranglekelp 8s 50c (ab 85), Briarthorn 3s 75c, Bruiseweed 2s 30c | Frilled Lichen 2g 72s; Swiftthistle 11s 11c; Uncommon Herb Seeds 5s 55c (34 Stk.; 11.10.) | Brachland: Deviate Fish 10s. Küste: Oily Blackmouth 5s 87c. Stonetalon: Firefin Snapper 44c (der einzige belegte Fang dort) | Savory Deviate Delight 19s 98c |

**Nicht gefragt, aber belegt:** Stringy Wolf Meat roh 1s 80c (Mulgore). Big Bear Meat roh 9s 70c (Ashenvale).

**Mit 30T statt Tageswert** (Item-Seiten) ändert sich die Reihenfolge an der Spitze: Frilled Lichen 67s 80c, Swiftthistle 6s 30c, Deviate Fish 6s 22c, Kingsblood 6s 6c, Briarthorn 1s 98c, Raw Brilliant Smallfish 1s 36c, Mageroyal 1s 8c. Damit liegt Swiftthistle vor Kingsblood. Für Wild Steelbloom, Stranglekelp, Earthroot und Bruiseweed wurde kein 30T abgerufen.

**NH statt PH:** Die Werte weichen stark ab (Swiftthistle 2s 10c, Kingsblood 8s 86c, Frilled Lichen 80s 80c, Deviate Fish 5s). In NH läge für 12–17 Kingsblood vor Deviate Fish und Swiftthistle.

KOMMENTAR: Das sind Beta-Preise mit grossen Sprüngen. Die 7-Tage-Änderung beträgt bei Silverleaf +376 %, bei Brilliant Smallfish +525 % und bei Big Bear Meat +629 %. Frilled Lichen steht heute bei 2g 72s, der 30-Tage-Median bei 67s 80c. Projekt-Risiko 6 gilt (Beta ≠ Live).

**Offene Fragen an den Nutzer** (statt Annahmen)
1. Welcher Markt zählt: Normal oder PvP? Zum Start gibt es EU-Preise, die es heute noch nicht gibt.
2. Zählt bei «das gewinnbringendste Kraut» auch die Zusatzbeute (Swiftthistle, Frilled Lichen, Samen) oder nur das Kraut des Knotens?

---

## Widersprüche

1. **Woher der Bauplan kommt:** Icy Veins (03.10. und 08.10.) sagt Shadetooth. [AHL-Kräuterkunde](https://ahledger.com/wow-forever/professions/herbalism) nennt als Quelle «Trainer». Bei [wowtbc](https://wowtbc.gg/warcraftforever/loot-tables/dungeons/excavation-site-wetlands/) fehlt der Bauplan in der Shadetooth-Beute.
2. **Zauber 1262980:** WT nennt ihn «Fermenter» («lets you grow herbs from seeds»). Bei AHL ist 1262980 das Greenhouse, und «Fermenter» steht auf der Kingsblood-Seite als Alchemie-Rezept ([AHL 3356](https://ahledger.com/items/3356-kingsblood)).
3. **Material des Gewächshauses:** IV-Samen (30.09.) nennt nur Arthas' Tears und Purple Lotus. Moba und AHL nennen dazu 2 Simple Wood.
4. **Fundort Purple Lotus:** IV-Samen (30.09.) sagt Ashenvale und Stranglethorn. IV-Kräuter (11.10.) nennt Azshara, Hinterlands, Feralas, Tanaris und Stranglethorn, aber nicht Ashenvale. AHL-Ashenvale führt Purple Lotus nicht.
5. **Stufe von Excavation Site: Wetlands:** IV sagt 26–33, bei wowtbc haben alle Quests Stufe 24.
6. **Uthan Stillwater:** IV verortet ihn in «Bloodhoof Village» (44.6 60.6), WP «at the lake» (Stonebull Lake), Best Practice §9 «Stonebull Lake 44.6 60.6».
7. **Earthroot in Mulgore:** IV führt Mulgore als Hauptzone, AHL-Mulgore führt Earthroot nicht.
8. **Brilliant Smallfish:** SM nennt als Zutaten Fisch und Mild Spices bei 1/45/65/85. AHL nennt nur den Fisch und Mindestfertigkeit 5.
9. **Kochstufen bei AHL und SM passen nicht zusammen:** Charred Wolf Meat AHL 5, SM gelb 45; Boiled Clams AHL 50, SM gelb 90; Crab Cake AHL 75, SM gelb 115; Royal Tea AHL 65 (Mageroyal-Seite), SM 100/105/115/125. Ob AHL die Lernstufe meint und SM bei 3 Zahlen gelb, grün und grau, ist ungeprüft.
10. **Rezeptquellen:** AHL-Kochen nennt bei Brilliant Smallfish, Longjaw, Roasted Kodo Meat und Strider Stew «trainer». AHL-Mulgore, WP und Best Practice §9 nennen Händler (Harn Longcast, Wunna Darkmane, Naal Mistrunner, Tari'qa).
11. **Händlerpreise:** Auf den AHL-Item-Seiten vertauscht die Details-Tabelle «Vendor sell» und «Vendor buy» gegenüber dem Fliesstext. Das betrifft Mageroyal, Briarthorn, Swiftthistle, Kingsblood, Longjaw, beide Samen und Raw Sagefish. Bei Frilled Lichen stimmen zwei Abschnitte gegen die Tabelle.
12. **Gleicher Markt, verschiedene Scans (PH):** Briarthorn 3s 75c (Markt 13.10. 16:53) gegen 1s 25c (Item 12.10. 17:21); Raw Sagefish 11s 98c gegen 95c (Item 13.10. 04:19); Firefin Snapper 44c gegen 59c (Item 29.09.). Ein Fehler der Seite ist nicht belegt; die Zeitpunkte sind verschieden.
13. **Raw Sagefish:** Der Markt führt ihn mit 11s 98c, die Item-Seite nennt aber keinen Fangort (nur Händler). Auf der Route ist er nicht belegt.
14. **Fischen in Stonetalon:** WP erwartet Longjaw und Catfish. AHL-Stonetalon zeigt nur Firefin Snapper (Blackwolf River).
15. **Best Practice §8 «+5 % XP … schon bei einfachen Rezepten»:** IV-Kochen (11.10.) schreibt «Most foods» und rät, den Tooltip zu prüfen; der Bonus gilt nur für Kill-XP. Das betrifft Projekt-Widerspruch 11.
16. **Best Practice §9 «In Startgebieten entkommen ab Fertigkeit 25 keine Fische»:** Im WP-Abruf vom 13.10. nur «From 75» für Hauptstädte gefunden. IV nennt keine Schwellen.
17. **Best Practice §9, Ränge der Kräuterkunde:** IV-Kräuter (11.10.) bestätigt Journeyman 50 mit Stufe 10, Expert 125 mit Stufe 20 und Artisan 200 mit Stufe 35. Der Widerspruch zu wow-professions («ohne Stufe») bleibt.
18. **Best Practice §9, Bruiseweed:** IV (11.10.) bestätigt 100. warcraft.wiki.gg nennt 85 [Classic].
19. **Ergänzung, kein Widerspruch:** Zur Cultivation (Best Practice §8) sagt WT: «The duplicate does not require Herbalism, but you need Herbalism to pick the original».

## Offen/ungeprüft

- **Gewächshaus:** Dropchance des Bauplans; Kräuterkunde zum Pflanzen und Ernten; Ertrag pro Ernte; ob eine Samenstufe ihr Kraut zufällig oder wählbar ergibt; Unusual und Scarce Herb Seeds (IDs, Quellen, Ergebnis); Preis von Arthas' Tears.
- **Fischen:** Fangraten am Stonebull Lake, an der Stagnant Oasis, an der Küste und in Stonetalon (dort nur Sichtungen); für Ashenvale gibt es keine Daten. Koordinaten der Angelstellen. Schwärme auf der Route. Die AHL-Seite zum Fischen liess sich nicht abrufen.
- **Kochen:** Preise roh (Kodo Meat, Thunder Lizard Tail, Crawler Meat, Raptor Flesh, Rainbow Fin Albacore) und gekocht (Longjaw, Catfish, Roasted Kodo Meat, Strider Stew, Crispy Lizard Tail, Charred und Spiced Wolf Meat, Crab Cake, beide Raptor-Gerichte); Item-IDs von Kodo Meat, Crawler Meat, Raptor Flesh und Oily Blackmouth; Kochfarben für Catfish, Savory Deviate Delight, Crispy Lizard Tail, Smoked Sagefish, Dig Rat Stew, Cooked Crab Claw und Goblin Deviled Clams (die SM-Liste ist abgeschnitten); Werte der Food-Buffs; woher genau das Rezept für Savory Deviate Delight fällt.
- **Kräuter:** Händlerpreise und 30T für Peacebloom, Silverleaf, Earthroot, Bruiseweed, Stranglekelp und Wild Steelbloom; Mirkweed Pods (278201, Stonetalon, Mirkfallon Lake 9×): was das ist und was es wert ist.
- **Route:** Ob die Route die AHL-Teilgebiete berührt (Southern Barrens, Field of Giants, Blackthorn Ridge, Agama'gor, Thorn Hill, Webwinder Path, Blackwolf River, Mirkfallon Lake, Stonebull Lake, Mystral Lake). Der RXP-Text v4.11.13 nennt sie nicht; die Koordinaten der `.goto`-Befehle wurden nicht ausgewertet.
- **Datenbasis:** AHledger-Zonenseiten beruhen auf 6–17 Spielern, Raten gibt es erst ab 20 Beutefenstern. Alle Preise sind US-Beta.

## Benutzte Links

- https://www.icy-veins.com/wow-forever/news/greenhouse-blueprint-found-how-herbalism-seeds-work-in-wow-forever/
- https://www.icy-veins.com/wow-forever/news/players-are-already-looting-seeds-for-a-wow-forever-greenhouse-no-one-can-craft-yet/
- https://www.icy-veins.com/wow-forever/excavation-site-wetlands-guide
- https://www.icy-veins.com/wow-forever/herbalism
- https://www.icy-veins.com/wow-forever/fishing
- https://www.icy-veins.com/wow-forever/cooking
- https://www.warcrafttavern.com/forever/guides/herbalism/
- https://mobalytics.gg/wow-forever/guides/herbalism-profession-guide
- https://seemeta.com/en/wow-forever/professions/herbalism (enthält nur «No recipes»)
- https://seemeta.com/en/wow-forever/professions/cooking
- https://www.wow-professions.com/forever/fishing-and-cooking-leveling-guide
- https://wowtbc.gg/warcraftforever/loot-tables/dungeons/excavation-site-wetlands/
- https://ahledger.com/markets/forever/pvp/horde/us
- https://ahledger.com/wow-forever/zones/mulgore
- https://ahledger.com/wow-forever/zones/the-barrens
- https://ahledger.com/wow-forever/zones/stonetalon-mountains
- https://ahledger.com/wow-forever/zones/ashenvale
- https://ahledger.com/wow-forever/professions/herbalism
- https://ahledger.com/wow-forever/professions/cooking
- https://ahledger.com/wow-forever/professions/fishing (Abruf fehlgeschlagen)
- https://ahledger.com/items/268415-commonplace-herb-seeds
- https://ahledger.com/items/268416-uncommon-herb-seeds
- https://ahledger.com/items/249399-frilled-lichen
- https://ahledger.com/items/785-mageroyal
- https://ahledger.com/items/2450-briarthorn
- https://ahledger.com/items/2452-swiftthistle
- https://ahledger.com/items/3356-kingsblood
- https://ahledger.com/items/6291-raw-brilliant-smallfish
- https://ahledger.com/items/6289-raw-longjaw-mud-snapper
- https://ahledger.com/items/6308-raw-bristle-whisker-catfish
- https://ahledger.com/items/6522-deviate-fish
- https://ahledger.com/items/6359-firefin-snapper
- https://ahledger.com/items/21071-raw-sagefish
- https://github.com/RestedXP/RXPGuides/tree/v4.11.13
