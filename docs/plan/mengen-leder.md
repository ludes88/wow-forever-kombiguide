# Mengenmodell Leder bis Stufe 20 (erzeugt von `tools/plan_mengen.py`)

Seit 14.10. gilt: Berufswechsel in Orgrimmar (Abschnitt E1, Stufe 16, Entscheidung des Nutzers). Danach gibt es kein eigenes Leder mehr; die Zeilen nach E1 zeigen nur, was die Route brächte, wenn Kürschnerei bliebe. Was mit dem Leder geschieht, steht in `docs/plan/berufe-plan.md` (`tools/plan_berufe.py`).

Eingaben: `data/kombi/abschnitte.csv`, `modell_leder.csv`, `kuerschnern_anteile.csv`, `farmstellen.csv`, `farmstopps.csv`, `bedarf_lw_vz.csv`, dazu `data/rechnung/Kreislauf.csv` und `Preise.csv`. Nicht von Hand ändern, sondern die Eingaben anpassen und neu erzeugen.

## Quellen

- Route: RestedXP v4.11.23, `Guides/forever/Horde-1-12_Mulgore.lua` und `Horde-12-22_Barrens.lua` (https://github.com/RestedXP/RXPGuides), gelesen für Tauren-Druide mit RXPs Standard-Einstellungen in Forever (kein Hardcore, kein SSF, keine Dungeons, XP-Rate 1). Schrittnummern so, wie RXP sie diesem Charakter zeigt.
- Anzahlen: RXPs Kommentare an den `.complete`-Zeilen. Stufe am Ende jedes Abschnitts: RXPs `.xp`-Schritte (Spalte «Beleg Stufe»).
- Gegnerstufen: Warcraft Tavern, Hunter-Pets-Seiten (Classic) · MetaForge, Seite «Medium Hide» (VMaNGOS-Daten) · Best Practice §9.
- Anteile beim Kürschnern: Testlog 13.10. (Mulgore) · MetaForge Zhevra Runner und Zhevra Charger (Best Practice §9).
- Wowhead, «Classic Leather Farming: Early Leather» (RenataKane, Stand 09.06.2021): Leichtes Leder am besten von Gegnern der Stufe 11–20, Mittleres Leder ab 16 (am besten 21–30), Bälge 3–5 %, ab Stufe 11 bis zu 2 Leichtes Leder pro Haut (Classic). https://cn.classic.wowhead.com/guides/classic-leather-farming-early-leather
- Lederverarbeitung 1–150: wow-professions, Leatherworking Leveling Guide (Forever-Beta) https://www.wow-professions.com/forever/leatherworking-leveling-guide · kami-labs, Leatherworking Guide (Stand 08.10.) https://kami-labs.fr/en/guide-travail-du-cuir-wow-forever/
- Verzauberkunst 1–150: wow-professions, Enchanting Leveling Guide (Forever-Beta) https://www.wow-professions.com/forever/enchanting-leveling-guide
- Entzaubern und Preise: `data/rechnung/Kreislauf.csv` (wow-professions-Tabelle), `Preise.csv` (AHledger, Beta, Horde US).

## Annahmen

- Bestand am Start: 8 Leichtes Leder, 13 Verdorbene Lederfetzen (Testlog 13.10. 22:42).
- Kills je Quest-Gegenstand: 2 (Annahme), je Kill-Ziel oder benanntem Gegner: 1. Gemessen: Quest 748 am 13.10.: 14 Wölfe für 6 Pfoten (2,3), 6 Ebenenschreiter für 4 Krallen (1,5).
- Jede Haut gibt 1 Gegenstand (Testlog 13.10., 21 von 21 Häuten, Gegner Stufe 5–8). Dass ab Gegnerstufe 11 bis zu 2 Leder kommen (Wowhead, Classic), ist nicht eingerechnet.
- Quest 768 «Gathering Leather» nimmt 12 Leichtes Leder (Abschnitt B2). Wer sie überspringt, hat 12 mehr.
- «Basis» = Quest-Tiere, die die Route sicher tötet. «Option» = Kürschnerbarkeit ungeprüft oder optionale Grind-Schritte. Tiere, die nebenbei sterben, zählt das Modell nicht; das Testlog misst sie (SAMMELN mit Kreatur-ID).
- Farm-Stopps: Minuten aus `farmstopps.csv` (Vorschlag zum Testen), 50–80 Häute pro Stunde (Annahme, keine Quelle für Stufe 12–20). Zum Vergleich gemessen: rund 97 Häute pro Stunde in Mulgore, Charakter Stufe 6–7 gegen Gegner der Stufe 5–8, neben Quest 748 (Testlog 13.10., 21 Häute in rund 13 Minuten). «Plan» = Basis plus Farm-Stopps mit der unteren Rate. Kills an Tieren, die eine Quest der Route ohnehin braucht, zählen beim Farm-Stopp nicht doppelt (Spalte «ueberschneidet» in `farmstopps.csv`).
- Kürschnerei endet mit dem Wechsel in Orgrimmar (Ende E1). Die früheren Farm-Stopps S2 (Südbrachland) und S3 (Camp Taurajo) lagen danach und entfallen.
- Kein Farm-Stopp gleich bei der Ankunft in den Crossroads: Die Route tötet dort sofort dieselben Tiere für «Plainstrider Menace» (844, 7 Schnäbel), «Raptor Thieves» (869, 12 Köpfe) und «The Zhevra» (845, 4 Hufe), zusammen rund 46 Kills. Ein Stopp davor würde diese Kills nur vorziehen und kein zusätzliches Leder bringen.

## Anteile beim Kürschnern nach Gegnerstufe

| Band | Gegnerstufe | Leichtes Leder | Fetzen | Light Hide | Mittleres Leder | Medium Hide | Quelle |
|---|---|---|---|---|---|---|---|
| 1 | 1–10 | 38% | 62% | 0% | 0% | 0% | Testlog 13.10. (Mulgore, Gegner Stufe 5–8: 8 Leichtes Leder und 13 Fetzen aus 21 Häuten) · passt zu MetaForge Kodo Calf (Stufe 7–8: 40 % Leder, 60 % Fetzen) |
| 2 | 11–15 | 60% | 35% | 5% | 0% | 0% | MetaForge Zhevra Runner (Stufe 13–14: 60 % Leder, 35 % Fetzen, 5 % Light Hide · enthält VMaNGOS-Daten, also vermutlich Vanilla · Best Practice §9) |
| 3 | 16–20 | 74% | 0% | 0% | 20% | 2% | MetaForge Zhevra Charger (Stufe 17–18: 74 % Leder, 20 % Mittleres Leder, 2 % Medium Hide · Rest 4 % unbekannt · Best Practice §9) |
| 4 | 21–30 | 74% | 0% | 0% | 20% | 2% | keine Daten: wie Stufe 16–20 angenommen · Wowhead (Classic) nennt Stufe 21–30 als besten Bereich für Mittleres Leder, der wahre Anteil ist dort vermutlich höher |

## Route: Abschnitte und Bestand

Leichtes Leder kumuliert: Basis · Plan mit Farm-Stopps (untere bis obere Rate) · mit Optionen statt Farm-Stopps.

| Abschnitt | RXP-Schritte | bis | Stufe am Ende | Kills Basis (Option) | Farm-Stopp | Leichtes Leder Basis | Plan | mit Optionen | Mittleres Leder Basis / Plan | Fetzen (Plan) | Light Hide (Plan) | Beleg Stufe |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 6-12 Mulgore #31–#83 | Thunder Bluff, Ruhestein (Label TBHome) | 9 | 30 (19) | – | 19 | 19–19 | 27 | 0 / 0 | 32 | 0.0 | RXP #96–#99: optionale Schritte «Grind to 9+3020/6500 xp» kommen kurz danach |
| B1 | 6-12 Mulgore #84–#151 | vor «Gathering Leather» (zweiter Besuch in Thunder Bluff) | 11 | 16 (15) | – | 25 | 25–25 | 38 | 0 / 0 | 42 | 0.0 | ungefähr: zwischen RXP #96–#99 (Stufe 9) und #176 (Stufe 12) |
| B2 | 6-12 Mulgore #152–#194 | Ankunft Crossroads (Ende «6-12 Mulgore») | 12 | 9 (0) | – | 17 | 17–17 | 30 | 0 / 0 | 47 | 0.0 | RXP #176: Druiden-Lehrer «.xp <12,1» vor dem Aufbruch ins Brachland |
| C | 12-17 The Barrens #1–#42 | Abgaben in den Crossroads nach Ratchet | 14 | 34 (0) | – | 37 | 37–37 | 50 | 0 / 0 | 59 | 1.7 | RXP #34/#35: Druiden-Lehrer in Moonglade bei Stufe 14–15 bzw. ab 16 |
| D | 12-17 The Barrens #43–#82 | Nordbrachland (Samophlange, Savannenkatzen) | 15 | 48 (0) | S1 25 min, 21–33 Häute | 66 | 79–86 | 79 | 0 / 0 | 83 | 5.1 | RXP #83: «Grinding to level 16 here is important» · Testcharakter Stufe 15 stand bei #77 (Testlog 13.10.) |
| E1 | 12-17 The Barrens #83–#108 | Orgrimmar, Berufswechsel (Entscheidung 14.10.) | 16 | 0 (0) | – | 66 | 79–86 | 79 | 0 / 0 | 83 | 5.1 | RXP #83: «Grinding to level 16 here is important» («.xp 16») · Orgrimmar #92–#108 (v4.11.23, Tauren-Druide) |
| E2 | 12-17 The Barrens #109–#184 | Ende «12-17 The Barrens» (Aufbruch Steinkrallengebirge) | 17 | 7 (0) | – | 71 | 84–91 | 84 | 1 / 1 | 83 | 5.1 | Guide-Name «12-17» · RXP #152: Lakota'mani erst ab Stufe 18 («.xp <18,1») |
| F | 17-22 Stonetalon/Barrens/Ashenvale #1–#29 | Steinkrallengebirge, Druiden-Lehrer | 18 | 0 (17) | – | 71 | 84–91 | 97 | 1 / 1 | 83 | 5.1 | RXP #28/#29: Druiden-Lehrer bei Stufe 18–19 bzw. ab 20 |
| G | 17-22 Stonetalon/Barrens/Ashenvale #30–#84 | Südbrachland bis Abgabe «Cry of the Thunderhawk» | 20 | 23 (16) | – | 88 | 101–108 | 123 | 6 / 6 | 83 | 5.1 | RXP #58: «Wolf Bracers» anlegen ab Stufe 20 («.xp <20,1», Ratchet) |
| H | 17-22 Stonetalon/Barrens/Ashenvale #85–#175 | Thunder Bluff, Steinkrallen 2, Eschental bis Zoram'gar | 21 | 12 (0) | – | 97 | 110–117 | 132 | 8 / 8 | 83 | 5.1 | RXP #166 «Grind to level 21», #173 «21450/25200 xp» |

**Stand beim Wechsel in Orgrimmar** (Ende Abschnitt E1, Stufe 16): Basis 66 Leichtes Leder, Plan 79–86, dazu 83–87 Fetzen, 5.1–5.8 Light Hide. Daraus rechnet `tools/plan_berufe.py` den Sweetspot.
**Stand bei Stufe 15** (Ende Abschnitt D): Basis 66 Leichtes Leder, Plan 79–86, dazu 83 Fetzen, 5.1 Light Hide.
**Stand bei Stufe 20, nur falls Kürschnerei bliebe** (Ende Abschnitt G): Basis 88 Leichtes Leder, Plan 101–108, dazu 6 Mittleres Leder (Basis 6), 83 Fetzen, 5.1 Light Hide, 0.6 Medium Hide.

## Ziele im Kombi-Guide

Zähler (Bank zählt mit) = Plan vor dem Farm-Stopp des Abschnitts; Farm-Stopp = Plan danach. Abgerundet. Nur bis zum Wechsel (E1).

| Abschnitt | Zähler bis Abschnittsende | Mittleres Leder bis dahin | Farm-Stopp | Ziel Farm-Stopp | Mittleres Leder nach dem Farm-Stopp |
|---|---|---|---|---|---|
| A | 19 | 0 | – | – | – |
| B1 | 25 | 0 | – | – | – |
| B2 | 16 | 0 | – | – | – |
| C | 37 | 0 | – | – | – |
| D | 66 | 0 | S1 Raptoren im Nordbrachland (25 min) | 78 | 0 |
| E1 | 78 | 0 | – | – | – |

Seit v0.4 zeigt der Zähler beim Farm-Stopp S1 nicht den Modellwert, sondern den Sweetspot für Lederverarbeitung 1–80 (62 Leichtes Leder, `docs/plan/berufe-plan.md`).

## Bedarf für Lederverarbeitung 150 und Verzauberkunst 150

Die zwei Forever-Routen für Lederverarbeitung widersprechen sich stark. Die letzte Stufe einer Route wird bis 150 anteilig gezählt. Netto heisst: was die Route selbst herstellt (z. B. Leichtes Leder aus Fetzen, Mittleres Leder aus Leichtem Leder), ist abgezogen.

| Material | LW wow-professions (Cured Heavy Hide) | LW wow-professions (ohne Heavy Hide) | LW kami-labs | AH-Rechenpreis |
|---|---|---|---|---|
| Leichtes Leder | 416 | 416 | 240 | 50c |
| Verdorbene Lederfetzen | 99 | 99 | 0 | 25c |
| Mittleres Leder | 223 | 363 | 72 | 1s 91c |
| Light Hide | 27 | 27 | 32 | 69c |
| Medium Hide | 10 | 10 | 42 | 8s 88c |
| Heavy Hide | 20 | 0 | 0 | 35s 40c |
| Salt | 97 | 37 | 74 | 50c |
| Coarse Thread | 80 | 80 | 96 | 10c |
| Fine Thread | 100 | 140 | 22 | 1s |
| Gray Dye | 10 | 10 | 2 | 3s 50c |
| Heavy Armor Kit | 0 | 0 | 7 | kein Preis |
| Soul Dust | 0 | 0 | 14 | 7s 21c |
| Elixir of Giant Growth | 0 | 0 | 14 | kein Preis |

Was die Herstellung für Verzauberkunst liefert (Erwartungswert, Entzaubern der übrigen grünen Teile nach `Kreislauf.csv`):

- LW wow-professions (Cured Heavy Hide): übrig 3 Cured Light Hide, 21 Embossed Leather Gloves, 9 Fine Leather Belt, 24 Light Leather Pants, 10 Dark Leather Belt, 7 Heavy Leather, 20 Cured Heavy Hide, 14 Hillman's Leather Gloves. Entzaubern ergibt etwa 123.0 Strange Dust, 6.3 Lesser Magic Essence, 9.9 Greater Magic Essence, 3.0 Lesser Astral Essence, 15.8 Soul Dust, 4.2 Greater Astral Essence.
- LW wow-professions (ohne Heavy Hide): übrig 3 Cured Light Hide, 21 Embossed Leather Gloves, 9 Fine Leather Belt, 24 Light Leather Pants, 10 Dark Leather Belt, 7 Heavy Leather, 24 Hillman's Leather Gloves. Entzaubern ergibt etwa 123.0 Strange Dust, 6.3 Lesser Magic Essence, 9.9 Greater Magic Essence, 3.0 Lesser Astral Essence, 27.0 Soul Dust, 7.2 Greater Astral Essence.
- LW kami-labs: übrig 36 Light Armor Kit, 32 Cured Light Hide, 28 Embossed Leather Gloves, 18 Fine Leather Belt, 22 Cured Medium Hide, 2 Dark Leather Belt, 18 Hillman's Shoulders, 7 Forceful Heavy Armor Kit. Entzaubern ergibt etwa 72.8 Strange Dust, 8.4 Lesser Magic Essence, 5.4 Greater Magic Essence, 0.6 Lesser Astral Essence. Ohne Entzauberungswert in `Kreislauf.csv`: Hillman's Shoulders.

Verzauberkunst 1–150 (wow-professions): Staub-Weg 275 Strange Dust und 4 Lesser Magic Essence, Essenz-Weg 313 Lesser Magic Essence und 3 Strange Dust, dazu Copper Rod, 19 Mote of Magic, Silver Rod, Shadowgem. Das Modell nimmt den Staub-Weg und setzt eigene Essenzen dort ein, wo eine Essenz am meisten Staub spart (1 Greater = 3 Lesser).

| | mit LW wow-professions (Cured Heavy Hide) | mit LW wow-professions (ohne Heavy Hide) | mit LW kami-labs |
|---|---|---|---|
| Strange Dust, der nach dem eigenen Entzaubern fehlt | 94 | 94 | 165 |
| dafür zusätzliche Embossed Leather Gloves (je 3 Leichtes Leder) | 66 | 66 | 109 |
| = zusätzliches Leichtes Leder für Verzauberkunst | 198 | 198 | 327 |
| oder Strange Dust im AH kaufen (Beta) | 78s 81c | 78s 81c | 1g 38s 43c |

## Lücke: Leichtes Leder

Bedarf = Lederverarbeitung netto, ohne oder mit dem Leder für Verzauberkunst. Angebot = Plan (Basis plus Farm-Stopps, untere Rate). Farmzeit für den Rest bei 50–80 Häuten pro Stunde und dem Leder-Anteil der Stufe 11–15 bzw. 16–20.

| Sammeln bis | LW-Route | Bedarf | Angebot (Plan) | Lücke | weitere Farmzeit | oder AH (Beta) |
|---|---|---|---|---|---|---|
| Wechsel (E1, Stufe 16) | wow-professions (Cured Heavy Hide) | 416 | 79 | 337 | 7.0–11.2 h | 1g 68s 70c |
| Wechsel (E1, Stufe 16) | wow-professions (Cured Heavy Hide) + VZ aus eigenem Entzaubern | 614 | 79 | 535 | 11.2–17.8 h | 2g 67s 70c |
| Wechsel (E1, Stufe 16) | wow-professions (ohne Heavy Hide) | 416 | 79 | 337 | 7.0–11.2 h | 1g 68s 70c |
| Wechsel (E1, Stufe 16) | wow-professions (ohne Heavy Hide) + VZ aus eigenem Entzaubern | 614 | 79 | 535 | 11.2–17.8 h | 2g 67s 70c |
| Wechsel (E1, Stufe 16) | kami-labs | 240 | 79 | 161 | 3.4–5.4 h | 80s 70c |
| Wechsel (E1, Stufe 16) | kami-labs + VZ aus eigenem Entzaubern | 567 | 79 | 488 | 10.2–16.3 h | 2g 44s 20c |
| Stufe 20, falls Kürschnerei bliebe | wow-professions (Cured Heavy Hide) | 416 | 101 | 315 | 5.3–8.5 h | 1g 57s 60c |
| Stufe 20, falls Kürschnerei bliebe | wow-professions (Cured Heavy Hide) + VZ aus eigenem Entzaubern | 614 | 101 | 513 | 8.7–13.9 h | 2g 56s 60c |
| Stufe 20, falls Kürschnerei bliebe | wow-professions (ohne Heavy Hide) | 416 | 101 | 315 | 5.3–8.5 h | 1g 57s 60c |
| Stufe 20, falls Kürschnerei bliebe | wow-professions (ohne Heavy Hide) + VZ aus eigenem Entzaubern | 614 | 101 | 513 | 8.7–13.9 h | 2g 56s 60c |
| Stufe 20, falls Kürschnerei bliebe | kami-labs | 240 | 101 | 139 | 2.4–3.8 h | 69s 60c |
| Stufe 20, falls Kürschnerei bliebe | kami-labs + VZ aus eigenem Entzaubern | 567 | 101 | 466 | 7.9–12.6 h | 2g 33s 10c |

Mittleres Leder, Bälge und Fetzen (Plan bis zum Wechsel gegen Bedarf):

| Material | Plan bis zum Wechsel | Bedarf LW wow-professions (Cured Heavy Hide) | Bedarf LW wow-professions (ohne Heavy Hide) | Bedarf LW kami-labs |
|---|---|---|---|---|
| Mittleres Leder | 0 | 223 (Lücke 223, AH 4g 25s 93c) | 363 (Lücke 363, AH 6g 93s 33c) | 72 (Lücke 72, AH 1g 37s 52c) |
| Verdorbene Lederfetzen | 83 | 99 (Lücke 16, AH 3s 98c) | 99 (Lücke 16, AH 3s 98c) | 0 (Lücke 0, AH 0c) |
| Light Hide | 5 | 27 (Lücke 22, AH 15s 8c) | 27 (Lücke 22, AH 15s 8c) | 32 (Lücke 27, AH 18s 53c) |
| Medium Hide | 0 | 10 (Lücke 10, AH 88s 80c) | 10 (Lücke 10, AH 88s 80c) | 42 (Lücke 42, AH 3g 72s 96c) |

## Farmstellen entlang der Route (Mitte der RXP-Schleifen, Brachland-Karte 1413 mit exakten Ecken)

| Id | Ort | x, y | Tiere | Stufe | RXP-Bezug | Hinweis |
|---|---|---|---|---|---|---|
| FS1 | Rund um die Crossroads | 51.9, 29.6 | Greater und Fleeting Plainstrider, Sunscale Lashtail und Screecher | 11–15 | 12-17 #5 und #6 (Raptoren «Kill every Raptor you see», Ebenenschreiter-Schleife) | kein eigener Farm-Stopp: die Route tötet hier gleich nach der Ankunft dieselben Tiere für 844 und 869 |
| FS2 | Zhevra-Weg Crossroads–Ratchet | 51.8, 37.6 | Zhevra Runner, Raptoren | 13–15 | 12-17 #32 (Zhevra-Schleife) | auf dem Weg nach Ratchet |
| FS3 | Savannenkatzen bei den Forgotten Pools | 41.0, 22.5 | Savannah Prowler | 14–15 | 12-17 #55 | neben Barak Kodobane und den Kolkar |
| FS4 | Patriarchen bei Vrang | 44.3, 15.5 | Savannah Patriarch | 15–16 | 12-17 #62 (neue Forever-Quest 95494) | RXP: bei viel Andrang später machen |
| FS5 | Raptoren im Nordbrachland | 53.7, 12.8 | Sunscale Lashtail, Screecher und Scytheclaw | 11–18 | 12-17 #81 | nahe Samophlange und Sludge Fen |
| FS6 | Savannenkatzen im Nordbrachland | 54.6, 15.2 | Savannah Prowler | 14–15 | 12-17 #82 | gleich neben FS5 |
| FS7 | Südbrachland Ost (Scytheclaws) | 54.7, 50.1 | Sunscale Scytheclaw (dazu Greater Plainstrider für die Nieren von 821, ohne Mittleres Leder) | 16–18 | 17-22 #42 und #43 | erste Stelle mit Mittlerem Leder |
| FS8 | Stormsnouts östlich von Camp Taurajo | 50.0, 54.5 | Stormsnout | 18–19 | 17-22 #40 | Mittleres Leder |
| FS9 | Donnerechsen bei Camp Taurajo | 47.0, 61.1 | Thunderhead, Stormsnout | 18–21 | 17-22 #78 | Wowhead (Classic): südlich von Camp Taurajo mehr Mittleres Leder |
| FS10 | Löwen östlich der Crossroads | 60.7, 32.0 | Savannah Matriarch und Patriarch | 15–18 | 17-22 #49 | Rest der Quest 95494 |
| FS11 | Schildkröten an der Oase | 55.6, 42.5 | Oasis Snapjaw | 15–16 | 17-22 #45 (Quest 880) | Kürschnerbarkeit in Forever ungeprüft |

Farm-Stopps im Kombi-Guide (`farmstopps.csv`):

| Id | Abschnitt | Farmstelle | Minuten | überschneidet Quest | Wo im Guide | Quelle |
|---|---|---|---|---|---|---|
| S1 | D | FS5 Raptoren im Nordbrachland | 25 | – | «12-17 The Barrens» vor RXPs Schritt «Grind to level 16» (#83): das Grinden an Tieren statt an Venture Co. | Minuten: Vorschlag zum Testen (Annahme) · RXP #83 schlägt hier ohnehin Grinden auf Stufe 16 vor · Raptorenköpfe (869) und Krallen (903) sind dort schon fertig, die Kills sind also zusätzlich |

## Zeilen

| Abschnitt | RXP-Schritte | Quest | Ziel | Kreatur | Stufe | Band | Kills | Art | Quelle |
|---|---|---|---|---|---|---|---|---|---|
| A | #46, #49 | 756 | Stalker Claws (6) | Prairie Stalker | 7 | 1 | 12 | Quest | Anzahl: RXP v4.11.23 (Kommentar) · Stufe 7–8: Best Practice §9 · kürschnerbar: Testlog 13.10. |
| A | #46, #49 | 756 | Cougar Claws (6) | Flatland Cougar | 8 | 1 | 12 | Quest | Anzahl: RXP · Stufe: Mulgore, höchstens 10 (ungeprüft) · kürschnerbar: Testlog 13.10. |
| A | #45, #95 | 766 | Prairie Wolf Heart, Flatland Cougar Femur, Plainstrider Scale (je 1) | Prairie Wolf, Flatland Cougar, Adult Plainstrider | 7 | 1 | 6 | Quest | Anzahl: RXP · kürschnerbar: Testlog 13.10. |
| A | #47, #74, #87, #94, #95 | 761, 766 | Trophy Swoop Quill (8) aus 761 und Swoop Gizzard (1) aus 766 | Wiry Swoop, Swoop, Taloned Swoop | 8 | 1 | 18 | Option: kürschnerbar ungeprüft | Anzahl: RXP · im Testlog 13.10. nie gekürschnert · Stufe 7–9: Best Practice §9 |
| A | #50 | 96130 | Chakuyak's Pelt (1) | Chakuyak | 8 | 1 | 1 | Option: kürschnerbar ungeprüft | Anzahl: RXP · Kreatur-ID: AHledger |
| B1 | #115, #119 | 759 | Prairie Alpha Tooth (8) | Prairie Wolf Alpha | 10 | 1 | 16 | Quest | Anzahl: RXP · Stufe 9–10: Best Practice §9 |
| B1 | #96–#99 | Grind | optionale RXP-Schritte «Grind to 9+3020/6500 xp» in Nord-Mulgore (Annahme 15 Kills) | Prairie Wolf Alpha, Prairie Stalker, Flatland Cougar, Plainstrider | 9 | 1 | 15 | Option: Grind | Kills: Annahme, keine Quelle |
| B2 | #152–#154 | 768 | Gathering Leather: 12 Leichtes Leder abgeben |  |  | – | 0 | Verbrauch | Anzahl: RXP v4.11.23 · Menge: AHledger Quest 768 · nur mit Kürschnerei sichtbar (RXP «.skill skinning,<1,1»), überspringbar |
| B2 | #114, #157, #163 | 861 | Flatland Prowler Claw (4) | Flatland Prowler | 10 | 1 | 8 | Quest | Anzahl: RXP · Stufe: Mulgore, höchstens 10 (ungeprüft) |
| B2 | #162 | 776 | Horn of Arra'chea (1) | Arra'chea | 10 | 1 | 1 | Quest | Anzahl: RXP · Stufe und Kürschnerbarkeit ungeprüft |
| C | #1, #6 | 844 | Plainstrider Beak (7) | Greater Plainstrider, Fleeting Plainstrider | 12 | 2 | 14 | Quest | Anzahl: RXP · Stufe Greater Plainstrider 11–12: Warcraft Tavern (Classic), Fleeting Plainstrider ungeprüft · IDs: AHledger (3246 nur erschlossen) |
| C | #5, #31 | 869 | Raptor Head (12), erste Hälfte (Annahme) | Sunscale Lashtail, Sunscale Screecher | 13 | 2 | 12 | Quest | Anzahl: RXP · Aufteilung auf C und D: Annahme · Stufe Lashtail 11–13, Screecher 13–15: Warcraft Tavern (Classic) · ID Screecher: AHledger |
| D | #44, #54, #81 | 869 | Raptor Head (12), zweite Hälfte (Annahme) | Sunscale Lashtail, Sunscale Screecher, Sunscale Scytheclaw | 14 | 2 | 12 | Quest | wie oben · RXP #81 nennt zusätzlich Sunscale Scytheclaw (Stufe 16–18) |
| C | #17, #32 | 845 | Zhevra Hooves (4) | Zhevra Runner | 13 | 2 | 8 | Quest | Anzahl: RXP · Stufe 13–14: Best Practice §9 · ID: AHledger |
| D | #55, #80, #82 | 903, 821 | Prowler Claws (7) und Savannah Lion Tusk (5), gleiche Kreatur | Savannah Prowler | 14 | 2 | 14 | Quest | Anzahl: RXP · Stufe 14–15: Warcraft Tavern (Classic) · ID: AHledger |
| D | #62 | 95494 | Savannah Lion Hide (6), neue Forever-Quest | Savannah Patriarch | 15 | 2 | 12 | Quest | Anzahl: RXP · Stufe 15–16: Warcraft Tavern (Classic) · ID: AHledger |
| D | #43, #58, #79, #90, #137, #145, #180 (17-22: #42) | 821 | Plainstrider Kidney (5), im Modell ganz in Abschnitt D (Annahme: RXP lässt die Nieren ab #43 nebenbei sammeln, vor Orgrimmar) | Greater, Fleeting und Ornery Plainstrider | 13 | 2 | 10 | Quest | Anzahl: RXP · Stufe 11–17 gemischt (Ornery 17: MetaForge), angenommen 13 |
| E2 | #138, #146–#148 | 905 | Sunscale Feather (3) | Sunscale Scytheclaw | 17 | 3 | 6 | Quest | Anzahl: RXP · Stufe 16–18: Warcraft Tavern (Classic) · ID: AHledger |
| E2 | #120, #123 | 881 | Echeyakee's Hide (1) | Echeyakee | 16 | 3 | 1 | Quest | Anzahl: RXP · Stufe 16: MetaForge |
| F | #9, #18, #26 | 6461 | Deepmoss Creeper (10), Deepmoss Venomspitter (7) | Deepmoss Creeper, Deepmoss Venomspitter | 18 | 3 | 17 | Option: kürschnerbar ungeprüft | Anzahl: RXP · Spinnen · Stufe und Kürschnerbarkeit ungeprüft |
| G | 12-17 #151, #153 · 17-22 #33, #38, #40 | 821 | Thunder Lizard Horn (1) | Stormsnout | 19 | 3 | 2 | Quest | Anzahl: RXP · Stufe 18–19: Best Practice §9 · ID: AHledger |
| G | 12-17 #138, #149 · 17-22 #41, #43 | 865 | Intact Raptor Horn (5), im Modell in G | Sunscale Scytheclaw | 17 | 3 | 10 | Quest | Anzahl: RXP · Stufe 16–18: Warcraft Tavern (Classic) |
| G | #44, #47 | 882 | Fresh Zhevra Carcass (1) | Zhevra Charger | 18 | 3 | 2 | Quest | Anzahl: RXP · Stufe 18: MetaForge |
| G | #48 | 882 | Ishamuhale's Fang (1) | Ishamuhale | 19 | 3 | 1 | Quest | Anzahl: RXP · Stufe 19: Warcraft Tavern (Classic) |
| G | #75, #78 | 907 | Thunder Lizard Blood (3) | Thunderhead, Stormsnout | 20 | 3 | 6 | Quest | Anzahl: RXP · Stufe Thunderhead 20–21, Stormsnout 18–19: Best Practice §9 |
| G | #82 | 913 | Thunderhawk Wings (1) | Thunderhawk Hatchling, Thunderhawk Cloudscraper | 20 | 3 | 2 | Quest | Anzahl: RXP · Stufe 20 bzw. 22: MetaForge |
| G | #45 (12-17: #165) | 880 | Altered Snapjaw Shell (8) | Oasis Snapjaw | 15 | 2 | 16 | Option: kürschnerbar ungeprüft | Anzahl: RXP · Stufe 15–16: Warcraft Tavern (Classic) · Wowhead (Classic) nennt Schildkröten als Lederquelle im Brachland |
| H | #160–#162 | 98251 | Ashenvale Bear (6), Shadowhorn Stag (6) | Ashenvale Bear, Shadowhorn Stag | 22 | 4 | 12 | Quest | Anzahl: RXP · Stufe 22 bzw. 23: MetaForge |
