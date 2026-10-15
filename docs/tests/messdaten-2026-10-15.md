# Messdaten 14. und 15.10.2026

Quelle: die Testlog-Datei des Nutzers, Stand 15.10. 19:38 (Testlog 3.3 und 3.5), am 15.10. über die Verbindung zum PC gelesen. Ohne Charakter-, Konto- und Realmnamen.

## Sitzungen

| Zeit | Charakter | Guide und Stelle | Versionen |
|---|---|---|---|
| 14.10. 19:52–19:54 | Stufe 15 | «12-17 The Barrens» #77 | Kombiguide 0.3, Testlog 3.3 |
| 14.10. 20:00–20:09 | Tauren-Druide, Stufe 7 (46 % → 74 %) | «6-12 Mulgore» #30 → #45 | Kombiguide 0.3, Testlog 3.3 |
| 15.10. 19:21–19:38 | Stufe 15 (70 % → 97 %) | «12-17 The Barrens» #77 → #84 | Kombiguide 0.4, Testlog 3.5 |

Nachtrag: Datei vom 15.10. 20:58 (nach `/reload`), siehe Abschnitt «15.10. 19:48–20:58» unten; Datei vom 15.10. 22:01, Abschnitt «15.10. 20:58–22:01».

## Stellen im Kombi-Guide (Best Practice §6)

- «6-12 Mulgore» #45: `.accept 749` (Zeile 510). Von v0.3 zu v0.4 unverändert: `tools/rxp_schritte.py vergleich git:2620af4:addons/RXPGuides_KombiGuide/Kombi_Guide.lua addons/RXPGuides_KombiGuide/Kombi_Guide.lua "6-12 Mulgore" --stelle 45 --klasse druid` meldet «Stelle #45 bleibt».
- «12-17 The Barrens» #84: `.xp 16` (Zeile 1799, Druiden-Zählung im Bau v0.4).
- Schrittwechsel des Stufe-15-Charakters am 15.10.:
  - #77 → #78 um 19:28 nach der Beute «Konsolenschlüssel» (Quest 901)
  - an #78 Abgabe 901 und Annahme 902
  - #81 bei den Raptorenköpfen (Quest 869)
  - #84 ab 19:35, an #84 Annahme 858
- Das passt nur zur Druiden-Zählung (`tools/rxp_schritte.py liste … "12-17 The Barrens" --klasse …`). Bei Jäger, Schamane und Krieger stehen an #77 bis #84 andere Schritte. Der Charakter ist also sehr wahrscheinlich ein Druide (die Klasse steht nicht im Testlog).
- RXP sprang um 19:35 von #81 auf #84. #83 ist der Kombi-Schritt «Sweetspot Leichtes Leder». Er erscheint nur mit Kürschnerei, und der Charakter hat keine mehr; der Sprung passt dazu (T4, indirekt).

## Messwerte

- Kürschnern, Druide Stufe 7, Kürschnerei 22 → 25 (je Haut +1):
  - Prairie Wolf (2958): 2 Häute, je 1 Verdorbene Lederfetzen
  - Adult Plainstrider (2956): 1 Haut, 1 Leichtes Leder
- Kräuterkunde 10 → 11: 2 Friedensblume (2447) aus Objekt 1618.
- Quest 97936 «Grundlagen des Zeltens: Kürschnerei», abgegeben am 14.10. um 20:07:
  - Standort des Spielers 45.0, 61.5 (Bloodhoof)
  - Belohnung 270 XP und das Rezept «Lagerstuhl» (1229517)
  - Laut warcraft.wiki.gg ist die Abgabe bei Yonn Deepcut (45.0, 61.4) und die Belohnung das Rezept Camp Chair. Das passt zur Messung; der Name des NPC steht nicht im Testlog. Widerspruch 1: spricht für 45.0, 61.4.
- Händler, 14.10. um 19:53: 11 Greater Magic Wand (11288) für zusammen 22s, also 2s je Stück (Widerspruch 21; die Datenbanken nennen 2s, die Patch-Notiz 1c).
- Quest-XP: 754 «Säuberung von Winterhoof» 550, 901 «Samophlang» 750.
- Beute am 15.10. (Stufe 15, Nordbrachland, 12 Minuten, 13 Beutefenster):
  - Geld zusammen 1s 31c
  - Die Gegenstände haben in Testlog 3.5 noch keinen Preis; erst 3.6 schreibt die Händlerpreise mit.

## Berufe des Stufe-15-Charakters

- Laut Testlog vom 13.10.: Lederverarbeitung 109/150, Verzauberkunst 100/150 (letzte BERUF-Zeilen um 19:24 und 19:46). Seither keine neuen BERUF-Zeilen.
- Laut Nutzer (15.10.): Er hat Kürschnerei und Kräuterkunde schon vor dem geplanten Wechsel in Orgrimmar gegen Lederverarbeitung und Verzauberkunst getauscht.
- Den Berufswechsel (M5, T11) kann er deshalb nicht mehr messen. Wer das misst, ist offener Punkt 22 in `docs/entscheidungen.md`.
- Ob er Angeln hat, zeigt das Testlog nicht (keine BERUF-Zeile dazu).

## Datei und Verknüpfung

- Die Testlog-Datei war am 15.10. um 19:38 60 KB gross, dazu eine `.bak` mit 57 KB. Sie enthält keine AH-Scans: Testlog 3.5 war geladen, aber das Auktionshaus wurde nicht geöffnet.
- Geprüft am 15.10.: Im AddOns-Ordner der Beta sind `KombiTestlog`, `RXPGuides_Kombi` und `RXPGuides_KombiGuide` Verknüpfungen (Junction) auf den Repo-Klon, keine Kopien. `KombiTestlog.lua` hat dort dieselbe Grösse und denselben Zeitstempel (auf die Millisekunde) wie im Klon. Im Ordner `_alt_kombi` liegen die alten Kopien, die `addons_verknuepfen.bat` beiseitegelegt hat.
- Der Klon stand am 15.10. um 19:20 auf `ed47fcf` (Merge #15, Testlog 3.5). Testlog 3.6 (Merge #16) kommt erst mit dem nächsten `aktualisieren.bat`.
- `Interface\AddOns\KombiDaten` hat Claude am 15.10. erstmals geschrieben (`tools/markt.py`). Darin sind noch keine Tipps, weil Preise fehlen.

## 15.10. 19:48–20:58 (Datei nach `/reload` um 20:58)

Gleicher Charakter (Stufe 15 → 16), Kombiguide 0.4, Testlog 3.5. Der Repo-Klon war weiter auf `ed47fcf` (`.git/FETCH_HEAD` und `.git/logs/HEAD` unverändert seit 19:20); Testlog 3.6 lief also noch nicht.

**Verlauf**
- 19:49 Stufe 16 an der Sludge Fen (Schlickermoor). Die BERUF-Zeilen beim Stufenaufstieg zeigen Kochkunst 1/75 und Angeln 5/75: Er hat Angeln und Kochen.
- Quests: 858 «Zündung» abgegeben (1350 XP), 863 angenommen; in Orgrimmar 97246 «Mahlzeit oder Spielzeit» (800 XP) und 97249, 97242.
- Danach Durotar, Zeppelin nach Tirisfal, Undercity und «Die Ruinen von Lordaeron» (Quests 92421, 92422, 92401, 95204).
- Stelle im Kombi-Guide um 20:58: «12-17 The Barrens» #103.

**Messwerte**
- Händler in Orgrimmar (20:10): 9 Posten für zusammen 24s 77c, darunter 5 Grauer Farbstoff (4340) und 7 Einfaches Holz (4470).
- Post (20:19): ein Brief mit 7 Posten, 30 Leinenstoff sind darin 2 Stapel (Stapelgrösse 20, Risiko 16), also 8 Stapel. Porto 2s 40c; das passt zu 30c je Stapel (gerechnet, nicht gemessen).
- Erster AH-Scan (20:12, Orgrimmar, Testlog 3.5, T15):
  - 65 411 Angebote, 3079 Gegenstände, 1 nur mit Gebot, 18 s
  - kein Angebot ohne Daten, keine geheimen Werte
  - Übernommen mit `tools/ah_aus_testlog.py`: `data/preise/ah_eigen.csv` (87 beobachtete Gegenstände), `data/preise/ah_alle.csv` (alle 3079), Bericht `docs/plan/ah-preise.md`
  - Ob der Tiefstpreis im Auktionshaus gleich aussah, ist nicht gemeldet (T15 offen).
- Die Region liefert der Beta-Client leer (`GetCurrentRegionName` gibt einen leeren Text). Der Scan steht deshalb unter dem Markt «? Horde R2d38 Beta»; Testlog und Werkzeug machen seit 15.10. aus dem leeren Text «?».
- Der Realm heisst «… PvP …». Der Bericht vergleicht vorerst mit dem AHledger-Median Normal Horde US (offene Entscheidung 4).
- Plan-Gegenstände im Scan (Tiefstpreis / Median nach Stückzahl / Stück im Angebot; dahinter AHledger NH):

  | Gegenstand | Scan 15.10. | AHledger NH |
  |---|---|---|
  | Leichtes Leder (2318) | 73c / 98c / 4310 | 50c |
  | Verdorbene Lederfetzen (2934) | 24c / 34c / 1674 | 25c |
  | Mittleres Leder (2319) | 1s 99c / 2s 29c / 5984 | 1s 91c |
  | Schweres Leder (4234) | 8s 15c / 8s 20c / 2347 | 11s 98c |
  | Seltsamer Staub (10940) | 63c / 65c / 4716 | 84c |
  | Geringe Magieessenz (10938) | 89c / 93c / 2638 | 69c |
  | Grauer Farbstoff (4340) | 4s / 4s 30c / 123 | – |
  | Deviate Fish (6522) | 5s 96c / 10s 64c / 1096 | – |

  Ein Scan ist ein Zeitpunkt; die 7-Tage-Werte brauchen weitere Scans (`docs/plan/ah-preise.md`).
- Neue Kartenecken (KARTE, übernommen mit `tools/karte_aus_testlog.py`):
  - 1411 Durotar: RXPs Kommentare passen genau, 32 Punkte
  - 1415 Östliche Königreiche, 1420 Tirisfal, 1458 Undercity: ohne RXP-Punkte zum Vergleich
- Münzbeute: In den Ruinen von Lordaeron und im Brachland schrieb das Testlog Geld aus Beute oft als eigene Zeile GELD «sonst», nicht in der Zeile BEUTE. Seit 15.10. rechnet `tools/markt.py` dieses Geld zur Beute, wenn es während eines Durchgangs im selben Gebiet kam. Ruinen von Lordaeron: 5s 55c in 25 Minuten.

## 15.10. 20:58–22:01 (Datei nach `/reload` um 22:01)

Gleicher Charakter, Stufe 16 (65 %) → 18 (56 %). Bis 21:58 Kombiguide 0.4 und Testlog 3.5; um 21:58 hat der Nutzer `aktualisieren.bat` ausgeführt (`.git/FETCH_HEAD` im Klon 21:58:10) und `/reload` gemacht: SITZUNG 21:58:27 meldet «Kombiguide 0.5-v4.11.23 | Testlog 3.6 | KombiDaten 15.10. 20:12, 0 Tipps».

**Verlauf**
- 20:50–21:09 Ruinen von Lordaeron, ein Tod um 20:52 (Warte Lordamere). Beute u. a. «Rezept: Elixier der geringen Beweglichkeit» (3396), «Gravierter Umhang» (4701).
- Quests mit XP (Testlog QUEST AB):
  - Undercity und Umgebung: 95204 «Wappen von Lordaeron» 5450 XP (danach Stufe 17); 92421 «Die Gerechtigkeit des Lichts» 4600 XP und 45s; 92422 «Der Zorn von Rath'mael» 4600; 92401 «Eine verängstigte Bitte» 4600 (Silberwald)
  - Orgrimmar: 97242 «Yelmaks Mischmasch» 800, 97275 «Whuut Ding will Weile haben» 800, 97249 «Lieblingsessen» 1050 (danach Stufe 18)
  - Crossroads: 848 1050 (7s), 869 900 (6s), 867 1050 (7s), 870 675, 903 1050 (7s), 98248 «Versandetikett» 650, 91904 «Eine ganz große Kiste» 0 XP und 5s
  - Ratchet: 902 1150, 863 1700 (20s), 896 1700
- Der Nutzer hat dabei alle Quests abgegeben, auch gegen RXPs Reihenfolge (Nachricht 15.10.).
- Neu angenommen: 5725 (Undercity), 1061 «Die Geister des Steinkrallengebirges» (Label «SpiritsPickup»), 97003 «Chol'aruk der Verschlinger».

**Kombi-Guide**
- Orgrimmar-Block (v0.4): #108 um 21:34 («SpiritsPickup»), #114 bis #143 in rund 5 Minuten. Laut Nutzer hat alles mit Lederverarbeitung und Verzauberkunst funktioniert (T11 teilweise: Charakter mit LW 109 und VZ 100).
- Bei #115 (Plan-Zeile 23, Einkauf Stufe A, in v0.4 ohne die Bedingung «ab LW 80») kaufte er bei Tamar 44 Grober Faden und 27 Salz für zusammen 17s 90c (HÄNDLER 21:38, 33 Käufe; passt zu 10c und 50c je Stück, AHledger nennt 9c und 45c; die Aufteilung ist aus der Summe nicht eindeutig). Mit LW 109 braucht der Plan beides nicht mehr; v0.4.1 blendet den Schritt dann aus.
- Stelle «12-17» #152 vor und nach dem Update auf 0.5 (Kombiguide (H)); #152 gehört nicht zu den Stellen, an denen eine alte Kennung im Neubau einen anderen Schritt trifft.
- Die Versionsangabe aus der `.toc` liest WoW schon beim `/reload` neu: ENDE 21:58:18, SITZUNG 21:58:27 mit «Kombiguide 0.5» (9 Sekunden, also kein Neustart). T22 teilweise.

**Geld** (Bestand 70s 99c → 1g 78s 15c)
- Ein: Quests 97s, Händler 38s 41c (6 Teile verkauft), Beute 1s 90c
- Aus: Tamar 17s 90c, Flüge 2s 75c (3 × 55c, 1 × 1s 10c), Pfand im AH 9s 50c
- Die Summe geht auf (+1g 7s 16c).

**Auktionshaus**
- Zweiter Scan 21:54 (noch Testlog 3.5): 67 980 Angebote, 3064 Gegenstände, 1 nur mit Gebot, 17 s, keine Angebote ohne Daten. Übernommen mit `tools/ah_aus_testlog.py` (jetzt 2 Scans in `data/preise/ah_eigen.csv`).
- Gegenüber 20:12 (Tiefstpreis / Median / Stück): Leichtes Leder 73c / 98c / 4310 → 52c / 64c / 7094; Mittleres Leder 1s 99c / 2s 29c / 5984 → 95c / 1s 99c / 7934; Seltsamer Staub 63c / 65c gleich; Verdorbene Lederfetzen 24c → 15c.
- 21:55 stellte er 4 Edelsteine ein (Tigerauge, Moosachat, Schattenedelstein, Geringer Mondstein; aus einem Beutel in Undercity). Testlog 3.5 kennt nur die Abbuchung: 8s 50c Pfand zusammen.
- 22:00 mit Testlog 3.6 (T19): AH-ANGEBOT «1x Grober Faden zu 24c je Stück | Dauer 24 Stunden | Pfand 0c | erstellt». Die Zeile AUKTIONSHAUS daneben zeigt «Ausgaben -1s». Der Pfand aus `CalculateCommodityDeposit` stimmt also nicht (der Haken läuft nach dem Einstellen; ob die Funktion dann 0 liefert oder ob es eine Mindestgebühr gibt, ist ungeprüft). Abhilfe geplant: Pfand aus der Abbuchung.
- Abnahme: noch keine. Der Scan um 21:54 lief mit Testlog 3.5 (ohne Restlaufzeit-Bänder, Region leer statt «?»); 3.6 vergleicht nur mit einem Scan, der Bänder hat und denselben Markt zeigt.

**Testlog 3.6 im Spiel**
- INVENTAR beim Einloggen: 19 Gegenstände, 131 Stück; Bank beim Schliessen: 0 Gegenstände. Kontobank: keine Daten (ungeprüft, ob es keine gibt oder ob die Abfrage nichts liefert). T18 teilweise.
- REZEPTE (T17): Lederverarbeitung 109/150 mit 39 Rezepten (7 orange, 2 gelb, 6 grün, 24 grau), Verzauberkunst 100/150 mit 19 (7 orange, 3 gelb, 3 grün, 6 grau), Kochkunst 1/75 mit 4. Für alle 12 Rezepte in `data/kombi/rezepte.csv` mit Zauber-ID (9 LW, 3 VZ) passt die Farbe im Spiel zu den Lernstufen von AHledger, z. B. Leichte Lederhose gelb (100/115), Feiner Ledergürtel grün (100/115), Dunkler Ledergürtel orange (bis 125), Runenverzierte Silberrute orange (bis 130).
- Verzauberkunst 100, orange: Umhang - Schwacher Schutz (7771), Brust - Geringe Ausdauer (7748), Zweihandwaffe - Schwacher Einschlag (7745), Armschiene - Schwache Beweglichkeit (7779), Waffe - Schwaches Schlagen (7788), Runenverzierte Silberrute (7795), Großer Magiezauberstab (14807); gelb: Brust - Schwache Absorption (7426), Umhang - Schwacher Widerstand (7454), Armschiene - Schwache Ausdauer (7457).
- Nicht im Protokoll: LEHRER (kein Lehrerfenster geöffnet), AH-POST (Briefkasten nicht geöffnet).

**Karten**
- 1421 Silberwald exakt (KARTE 21:19; `tools/karte_aus_testlog.py`). Keine RXP-Punkte mit Kommentar zum Vergleich.

## 15.10. 22:01–22:16 (Datei beim Beenden des Spiels um 22:16)

Gleicher Charakter, Stufe 18, Orgrimmar, Testlog 3.6. Danach hat der Nutzer das Spiel geschlossen (Server-Abschaltung angekündigt).

**Lehrerlisten (M1, T13)**
- Vier Lehrer in Orgrimmar, je zuerst mit dem Filter «lernbar+gesperrt», dann mit allen drei Arten: Kamari (Kreatur 5811, 17 Einträge), Karolek (3365, 48), Jhag (11066, 10), Godan (3345, 29). Ändert sich der Filter, schreibt das Testlog eine neue Zeile; das ist so gebaut (gleiche Liste: keine zweite Zeile).
- Übernommen mit `tools/lehrer_aus_testlog.py` nach `data/kombi/lehrer.csv` (104 Einträge mit Lernstufe, Kosten, Ort; ohne Charakter und ohne Status).
- Geselle: Lederverarbeitung und Verzauberkunst je ab Stufe 10 und Fertigkeit 50, 5s (Karolek, Godan). Lehrling 10c. Einen Experten führen Karolek und Godan nicht.
- Lernstufen der Rezepte unseres Plans (Lehrerliste gegen `data/kombi/rezepte.csv`, Spalte orange = AHledger):

  | Rezept | Lehrerliste | AHledger (orange) |
  |---|---|---|
  | Cured Light Hide (Geschmeidiger leichter Balg) | 30, 50c | 10 |
  | Embossed Leather Gloves (Geprägte Lederhandschuhe) | 40, 1s 50c | 30 |
  | Fine Leather Belt (Feiner Ledergürtel) | 55, 3s | 45 |
  | Light Leather Pants (Leichte Lederhose) | 70, 4s | 60 |
  | Medium Leather (Mittleres Leder) | 75, 5s | 35 |
  | Cured Medium Hide (Geschmeidiger mittlerer Balg) | 75, 2s | 50 |
  | Dark Leather Belt (Dunkler Ledergürtel) | 100, 4s | 85 |
  | Hillman's Leather Gloves (Lederhandschuhe des Hügelwächters) | 120, 5s | 105 |
  | Heavy Leather (Schweres Leder) | 125, 10s | 85 |
  | Cured Heavy Hide (Geschmeidiger schwerer Balg) | 125, 5s | – |
  | Enchant Chest - Inferior Stamina (Brust - Minderwertige Ausdauer) | 15, 50c | 30 |
  | Enchant Chest - Minor Absorption (Brust - Schwache Absorption) | 40, 1s | 50 |
  | Enchant Bracer - Minor Stamina (Armschiene - Schwache Ausdauer) | 50, 2s 50c | 60 |
  | Enchant Cloak - Minor Protection (Umhang - Schwacher Schutz) | 70, 2s | 70 |
  | Runed Silver Rod (Runenverzierte Silberrute) | 100, 10s | 90 |
  | Enchant Boots - Minor Stamina (Stiefel - Schwache Ausdauer) | 125, 14s | 110 |
  | Enchant Bracer - Lesser Stamina (Armschiene - Geringe Ausdauer) | 130, 15s | – |

  Englisch–deutsch über die Item-ID oder, bei Verzauberungen, über die Zauber-ID der gelernten Rezepte (REZEPTE); «Stiefel - Schwache Ausdauer» und «Armschiene - Geringe Ausdauer» nur über den Namen zugeordnet (nicht gelernt, keine Zauber-ID).
- Jedes Rezept der Routen ist lernbar, wenn die Route es braucht (wow-professions: Medium Leather ab 75, Heavy Leather ab 125, Hillman's Leather Gloves ab 130; kami-labs: Hillman's Shoulders ab 130, Lehrerliste 105).
- Nicht auf den Listen, obwohl der Charakter sie kennt: Light Leather, Light Armor Kit, Handgenähte Lederstiefel (Lederverarbeitung), Runed Copper Rod, Enchant Bracer - Inferior Stamina, Übungszauberstab des Novizen, Staub zu Partikel (Verzauberkunst); sehr wahrscheinlich bringt sie der Lehrling mit. Ebenso nicht dabei: **Enchant Bracer - Minor Deflect (Armschiene - Schwache Abwehr)**, Minor Wizard Oil (Formel beim Händler), Enchant 2H Weapon - Lesser Intellect (Formel beim Händler) und das Mystische mittlere Rüstungsset (Muster bei Tamar).
- Lernkosten bis 150, gerechnet aus der Liste: Lederverarbeitung (Route wow-professions) 40s 10c, mit dem Tab «Cured Heavy Hide» 45s 10c; Verzauberkunst Staub-Weg 34s 10c, Essenz-Weg 21s 10c mit der Formel 2H Weapon - Lesser Intellect (5s), ohne Minor Deflect.
- Neue Forever-Rezepte: Dunkle Lederstiefel (252425), Mondscheinstiefel, Murlocschuppenschuhe, Schwarzwelpenpantoffeln (ab 35, je 5s), sieben «Ledergürtel des …» (ab 150, je 20s).
- Orte (Standort beim Öffnen, Karte 1454): Kamari 63.2, 44.9; Karolek 62.8, 44.2; Jhag 53.5, 38.1; Godan 53.8, 38.6. Passt zu RXP (Kamari 63.3, 44.8) und Icy Veins (Karolek 62.8, 44.4; Jhag 53.6, 38.2; Godan 53.8, 38.4).

**Dritter AH-Scan 22:15 (erster mit Testlog 3.6)**
- 68 980 Angebote, 3058 Gegenstände, 1 nur mit Gebot, 17 s, vollständig. Region «?».
- Restlaufzeit (Risiko 24): `GetReplicateItemTimeLeft` liefert Rohwerte 1 bis 4 (`bandRoh` 1-4, `bandVersatz` -1, also wie die alte API). Bänder laut `GetTimeLeftBandInfo`: 0 bis 30 Minuten, 30 Minuten bis 2 Stunden, 2 bis 12 Stunden, 12 bis 24 Stunden.
- Keine Abnahme: Der Scan davor (21:54) lief mit Testlog 3.5.
- Gegenüber 21:54 (Tiefstpreis / Median / Stück): Leichtes Leder 52c / 64c / 7094 → 35c / 60c / 8544; Mittleres Leder 95c / 1s 99c / 7934 → 1s 72c / 1s 99c / 7939; Schweres Leder 8s 14c / 8s 59c → 6s / 8s 59c; Schwerer Balg 30s → 26s; Salz 95c und Grober Faden 24c gleich.

**Nicht gemessen**
- Briefkasten: keine Zeile POST, also nicht geöffnet. Ob die 4 Edelsteine verkauft wurden, ist offen (T16).
