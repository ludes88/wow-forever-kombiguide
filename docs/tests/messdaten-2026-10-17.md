# Messdaten 16. und 17.10.2026

Quelle: die Testlog-Datei des Nutzers, Stand 17.10. 13:38 (Testlog 3.7.1, Kombiguide 0.6.1), am 17.10. über die Verbindung zum PC gelesen. Ohne Charakter-, Konto- und Realmnamen. Ausgewertet mit `tools/spiel_aus_testlog.py`, `tools/lehrer_aus_testlog.py`, `tools/ah_aus_testlog.py` und `tools/markt.py` (Stand `main` vom 17.10.).

## Sitzungen

| Zeit | Charakter | Guide und Stelle | Was |
|---|---|---|---|
| 16.10. 17:40–17:47 | vier Charaktere | – | nur ein- und ausgeloggt, Notizen (Teststand 16.10. in Best Practice §10) |
| 17.10. 12:54–12:55, 13:30–13:37 | Bankchar, Stufe 1 | «6-12 Mulgore» #2 (Kombiguide (H) geladen) | Briefkasten, Schneiderei gelernt, AH-Scan, zwei Angebote |
| 17.10. 12:56–12:57 | Stufe 18 | «12-17 The Barrens» #152 | Briefkasten |
| 17.10. 12:57–13:30 | Tauren-Druide, Stufe 7 (74 %) → 9 (10 %) | «6-12 Mulgore» #45 → #46 → #50 → #51 → #52 | Messlauf nach der Checkliste (Entscheid 16.10.) |

Alle Sitzungen am 17.10. melden den Client-Build 70450 (am 16.10. noch 70425), dazu Kombiguide 0.6.1-v4.11.23 und Testlog 3.7.1. Fehler-Einträge (FEHLER) gibt es keine.

## Stellen im Kombi-Guide

- Der Druide stand beim Einloggen bei #45 «Accept The Ravaged Caravan» (Zeile 510), wie am 14.10. gespeichert. Kombiguide 0.6.1 hat die Stelle also gehalten (T6).
- Danach #46 um 12:59 (nach der Annahme von 749), #50 um 13:03, #51 um 13:10 (nach der Abgabe von 749), #52 um 13:25. #52 ist `.complete 96130,1` (Zeile 566, Quest «Chakuyak»). Neue Kombi-Schritte in «6-12 Mulgore» gehören ab jetzt hinter #52.
- Um 13:26 ging er wegen voller Taschen und der Zauber der Stufe 8 zurück nach Bloodhoof (Notiz) und gab dort 766, 99081, 756 und 761 ab; RXP blieb bei #52 (die Abgaben stehen später in der Route, erledigte Schritte überspringt RXP).
- Der Stufe-18-Charakter steht weiter bei #152.

## Messwerte des Druiden (12:57–13:30)

- Stufe 7,74 → 9,10 in 33 Minuten (2,48 Stufen pro Stunde, `docs/plan/spiel.md`), 0 Tode. 6 Quests mit zusammen 2685 XP: 99079 (80), 749 (525), 766 (700), 99081 (80), 756 (625), 761 (675 und 2s 50c). Die XP aus QUEST AB und aus den XP-Quellen stimmen überein (T23).
- XP pro Gegner (mit erholter XP, «5 Bubbles» laut Notiz): `data/spiel/xp_quellen.csv`; auf Stufe 8 in Mulgore 15 838 XP pro Stunde über 22 Minuten (Laufweg-Proben).
- Kürschnern, Kürschnerei 25 → 56: 39 Häute in etwa 27 Minuten, 18 Leichtes Leder und 21 Verdorbene Lederfetzen (Taschen: 9 → 27 bzw. 15 → 36). Pro Kreatur:
  - Prairie Stalker (2959): 17 Häute, 9 Leichtes Leder, 8 Fetzen
  - Flatland Cougar (3035): 14 Häute, 6 Leichtes Leder, 8 Fetzen
  - Prairie Wolf (2958): 6 Häute, 3 Leichtes Leder, 3 Fetzen
  - Adult Plainstrider (2956): 2 Häute, 2 Fetzen
  - 31 Punkte aus 39 Häuten: 8 Häute gaben keinen Punkt, bei Kürschnerei 32, 34, 46, 47 (dreimal), 51 und 53.
  - Das sind etwa 40 Leichtes Leder pro Stunde, wie die Schätzung vom 13.10. (Best Practice §9).
- Leder-Ziel im Guide: Kombi-Schritt «Leder-Ziel bis Thunder Bluff (Modell A)» verlangt 19 Leichtes Leder; vor Thunder Bluff waren es 27 (laut Notiz vom 16.10. zeigte der Zähler bei #45 9/19). Das Modell liegt hier zu tief (T9).
- Kräuter, Kräuterkunde 11 → 20 (Ziel von 97933 erreicht, Abgabe bei Komin Winterhoof in Thunder Bluff steht noch aus): 9 Knoten, 11 Friedensblume, 10 Silberblatt, 3 Erdwurzel und 1 Gekräuselte Flechte (249399) aus Erdwurzel (Objekt 1619, Mulgore 55.1, 49.3, 13:14).
- «Grüner Daumen»: zweimal geerntet, 13:02:30 (1 Friedensblume, Objekt 657382) und 13:17:29 (3 Silberblatt, Objekt 657380). Vermutlich die Tauren-Fähigkeit Cultivation (eigene Objekt-IDs, wie es die Quellen für das Duplikat beschreiben; ungeprüft). Die zwei Ernten liegen 15 Minuten auseinander; das passt zur Abklingzeit von 15 Minuten bei Warcraft Tavern (https://www.warcrafttavern.com/forever/guides/tauren-racials/, abgerufen 17.10.), nicht zu der Stunde, die bis 17.10. in Best Practice §8 stand. SeeMeta (https://seemeta.com/en/wow-forever/races/tauren, «Last Updated October 17, 2026») nennt keine Abklingzeit.
- Kochkunst 1 → 16 mit 15 Verkohltem Wolfsfleisch (2538), jedes gab einen Punkt. Farbwechsel des Rezepts «Einfaches Lagerfeuer»: gelb → grün bei Kochkunst 3, grün → grau bei 5 (REZEPTE, T17).
- Lehrer:
  - Gennia Runetotem (Kreatur 3064, Druidenlehrerin, Bloodhoof): 182 Einträge mit allen drei Filtern. Gelernt: Heilende Berührung (5186) und Wucherwurzeln (339), je 2s.
  - Yonn Deepcut (Kreatur 6290, Kürschnerei, Bloodhoof 45.0, 61.5): Kürschnergeselle «lernbar, ab Kürschnerei 50, 5s», ohne Stufen-Voraussetzung in der Liste (bei Karolek steht für den Gesellen «ab Stufe 10 und Lederverarbeitung 50»). Das klärt Widerspruch 6: Geselle ab Fertigkeit 50, wie wow-professions. Nicht gelernt: Der Druide hatte 2s 78c.
- Geld: 90c → 2s 78c (Beute 7c, Händler +3s 56c für graue Beute, Quest 2s 50c, Lehrer −4s, Händler −25c ohne Gegenstand in der Zeile, vermutlich eine Reparatur, ungeprüft).
- Beim Händler um 13:26 verkaufte er nur graue Beute (Eckzähne, Hasenpfoten, Eierschalen, Schnäbel, Lederkragen, Fangzähne, Feder). Die Warnung «Nicht beim Händler verkaufen» konnte nicht kommen: KombiDaten war veraltet (unten).

## Bankchar und Stufe-18-Charakter

- Bankchar, Briefkasten: Um 12:55 notiert «kann noch immer nicht auf den Briefkasten zugreifen» (am 16.10. ebenso); um 13:30 öffnete er sich am selben Ort (Orgrimmar 50.9, 70.4) und das Testlog schrieb POST mit sieben erhaltenen Gegenständen. Was um 12:55 anders war, zeigt das Testlog nicht.
- Porto: ein Brief mit einem Gegenstand kostete 30c (POST 13:31).
- Schneiderei bei Snang (Kreatur 2855, Orgrimmar, Die Gasse 62.8, 49.4): 25 Einträge mit allen drei Filtern; Lehrling 10c. Gelernt wurden zwei Zauber-IDs, 3908 und 1240953 (wie bei Angeln und Kochen am 13.10.: Lehrling plus eine zweite neue ID).
- Schneiderei 1 → 20: 15 Leinenstoffballen und 4 Leinentaschen. Bei den Leinentaschen schreibt HERSTELLEN «erhalten: -»: Das Testlog hat die fertigen Taschen nicht gesehen. Vermutung (ungeprüft): Sie kamen direkt in freie Taschenplätze und zählen dann nicht zum Inhalt der Taschen.
- Händler in der Gasse (63.1, 51.3): 20 Grober Faden für 2s, also 10c je Stück.
- Auktionshaus Orgrimmar, 13:36:
  - Scan: 50 662 Angebote, 2925 Gegenstände, 11 s (15.10. 22:15: 68 980 und 3058). Unter dem Händlerpreis: 5 Gegenstände, zusammen 2s 4c Gewinn.
  - Angebot 1 Schattenedelstein zu 2s 90c, 24 Stunden: Pfand laut Geldabzug 1s 50c, das Spiel meldete 1s 44c (T25). Angebot 5 Seltsamer Staub zu 33c je Stück: Pfand 1s. Zusammen −2s 50c, wie der Geldabzug.
- Stufe 18, Briefkasten 12:56: AH-POST «abgelaufen: 1x Grober Faden, 1x Geringer Mondstein» (T16); abgeholt wurde nur der Grobe Faden.

## Preise im Scan vom 17.10. 13:36 gegen 15.10. 22:15

Tiefstpreis / Median / Stück im Angebot (`data/preise/ah_eigen.csv`):

| Gegenstand | 15.10. 22:15 | 17.10. 13:36 |
|---|---|---|
| Leichtes Leder (2318) | 35c / 60c / 8544 | 68c / 85c / 5411 |
| Verdorbene Lederfetzen (2934) | 15c / 22c / 3066 | 29c / 50c / 1666 |
| Leichter Balg (783) | 64c / 68c / 694 | 72c / 73c / 355 |
| Seltsamer Staub (10940) | 60c / 65c / 3988 | 33c / 38c / 4729 |
| Geringe Magieessenz (10938) | 88c / 91c / 2484 | 76c / 77c / 1116 |
| Gekräuselte Flechte (249399) | 2g 35s 90c / 2g 59s 94c / 221 | 2g 75s / 3g 24s / 185 |

Der Händler zahlt für die Gekräuselte Flechte 30c (`data/preise/haendler_ankauf.csv`).

## Befunde zum Ablauf

1. KombiDaten im Spiel war veraltet: Am 16.10. um 17:49 sollte die neu gerechnete `Daten.lua` (10 994 Bytes) ins Spiel. Auf dem PC lag danach eine alte Fassung vom 15.10. (763 Bytes, ohne Tipps, ohne nächste Schritte, ohne die Listen für das Testlog 3.7.1); SITZUNG meldete am 17.10. «0 Tipps». Ursache: Die Auslieferung lief über denselben Ordner unter `/mnt/user-data/outputs/` wie am 15.10., und auf den PC kam der alte Stand. Behoben am 17.10.: neue Datei über einen neuen Ordner, danach zurückgelesen und mit SHA-256 verglichen (gleich). Die übrigen Addons im Spiel sind gleich wie auf `main` (SHA-256 geprüft). Regel seit 17.10.: `docs/vorgehen.md`.
2. Folge von 1: `/tl tipp` (T27) und die Warnung beim Händler (T31) konnten am 17.10. nicht wirken; nach `/reload` sind sie da.
3. SAMMELN mit falscher Beute: Um 13:22:24 steht eine Zeile «Kürschnerei | Kreatur 3035 | Pumaklauen, Verfärbter Fangzahn», das ist die Beute eines zweiten Pumas, die direkt nach dem Kürschnern geplündert wurde (1 von 40 Zeilen).
4. Volle Taschen auf Stufe 8 (Notiz 13:26): In den Taschen waren unter anderem 27 Leichtes Leder, 36 Fetzen, 22 Friedensblume, 18 Silberblatt, 15 Verkohltes Wolfsfleisch (INVENTAR 13:30). Risiko 15 in Best Practice §7.

---

# Nachmittag 17.10. (13:38–15:15)

Quelle: die Testlog-Datei, Stand 17.10. 15:15 (Testlog 3.7.1, Kombiguide 0.6.1), am 17.10. über die Verbindung zum PC gelesen; dazu die Schrittliste des Kombi-Guides (`tools/rxp_schritte.py liste … "6-12 Mulgore" --klasse druid --rasse tauren`) und der Bagnon-Ordner im AddOns-Ordner. Ohne Charakter-, Konto- und Realmnamen. Ausgewertet mit denselben Werkzeugen wie oben (Stand des Branches `daten/2026-10-17-nachmittag`).

## Sitzungen

| Zeit | Charakter | Guide und Stelle | Was |
|---|---|---|---|
| 13:38–14:38 | Tauren-Druide, Stufe 9 (10 %) → 9 (94 %) | «6-12 Mulgore» #52 → #94 | Post an den Bankchar, Angeln, Questen, Thunder Bluff (Abgabe 97933, Geselle Kürschnerei, Auktionshaus) |
| 14:39–14:42 | Bankchar, Stufe 1 | «6-12 Mulgore» #2 | Post vom Druiden und vom Stufe-18-Charakter abgeholt, Kräuter und Edelsteine an den Druiden zurück |
| 14:39–14:41 | Stufe 18 | «12-17 The Barrens» #152 | Post an den Bankchar |
| 14:42–15:14 | Tauren-Druide, Stufe 9 (94 %) → 10 (75 %) | «6-12 Mulgore» #94 → #116 | Lehrerlisten in Thunder Bluff, Stufe 10, zwei Tode, Auktionshaus, Bloodhoof |
| 15:15 | Bankchar | «6-12 Mulgore» #2 | Brief des Auktionshauses, 1g verschickt |

Alle Sitzungen melden Client 70450, Kombiguide 0.6.1-v4.11.23, Testlog 3.7.1. KombiDaten: Die Sitzung um 13:38 zeigt noch den alten Stand («15.10. 22:15, 0 Tipps»), ab 14:38 den neuen («17.10. 13:36, 6 Tipps»). Keine Zeile FEHLER.

## Stellen

- Druide: #52 → #116 (`.train 8924`, «Train your class spells» bei Gennia Runetotem in Bloodhoof), Stufe 10 (75 %). Neue Kombi-Schritte in «6-12 Mulgore» gehören ab jetzt hinter #116.
- Stufe 18: weiter #152. Bankchar: «6-12 Mulgore» #2 der Gruppe «Kombiguide (H)».

## Notizen im Spiel und was dahinter steht

1. 14:08 «ich habe das fleisch für kyle nie erhalten» und «die quest habe ich erst jetzt angenommen»: Die Annahme von 99411 «Kyle wird vermisst!» ist Schritt #3 von «6-12 Mulgore». Sie kam mit dem Neubau auf RXP v4.11.23 am 13.10. dazu, als der Druide schon weiter war (Best Practice §10, T6); er sah den Schritt nie, und ohne Quest fällt das Fleisch nicht. Angenommen 14:08:20 bei Ahab Wheathoof (Mulgore 47.3, 57.7), Zartes Schreiterfleisch (287505) 14:09:33 von einem Adult Plainstrider (2956), abgegeben 15:13:17 (625 XP, 1s 75c).
2. 15:04 «ich bin in tb und hohle keine klassen quests für level 10 keine spells und auch nicht die vorqquests für RFC?? ist das richtig?»: so in der Route. Die Klassenquest 5928 «Dem Ruf folgen» gibt Gennia Runetotem in Bloodhoof (#115, angenommen 15:12:11). Die Zauber lernt die Route dort (#116); laut Lehrerliste 15:12 sind 4 Zauber lernbar, je 3s (Griff der Natur, Mal der Wildnis Rang 2, Mondfeuer Rang 2, Verjüngung Rang 2), der Schritt hakt sich mit Mondfeuer Rang 2 ab. Der Druide hatte dort 2s 88c. Die RFC-Vorquests bei Rahauro kommen beim dritten Besuch in Thunder Bluff (#177, nach der Abgabe von 776 bei Cairne), wo RXP selbst sie führt; davor «Gathering Leather» (#160–#162, 12 Leichtes Leder in den Taschen).

## Messwerte des Druiden

- Stufe 9,10 → 10,75 (Sitzungen 61, 5 und 26 Minuten, `docs/plan/spiel.md`), 13 Quests abgegeben, 2 Tode: 14:51:45 in Thunder Bluff (66.8, 51.7), 29 s nach der Abgabe von 98430 bei Cairne, und 15:00:32 am Teufelsfelsen (Mulgore 57.1, 35.7). Die Ursache steht nicht im Testlog.
- Angeln am Stonebull Lake (43.9, 63.4), 13:40:37–13:43:04: 10 Fänge mit 11 Würfen, 6 Roher Langzahniger Matschschnapper, 3 Roher glänzender Kleinfisch, 1 10-pfündiger Matschschnapper; jeder Fang +1 Punkt (Angeln 15 → 25).
- Kürschnerei 56 → 61. Geselle bei Mooranta (Thunder Bluff) um 14:37:15 für 5s: Lehrerliste «Kürschnergeselle (Rang) lernbar, ab Kürschnerei 50, 5s», danach Maximum 150. Der Kombi-Schritt #88 (`.istrained 8617`) war 2 s später erledigt: T29 für Kürschnerei bestanden. Eine Zeile GELERNT gab es dabei nicht.
- Kräuterkunde 20 → 24. Abgabe von 97933 bei Komin Winterhoof um 14:36:52 (270 XP), Rezept Räucherkerze (1229705).
- Gekräuselte Flechte: zwei weitere aus Erdwurzel (14:25:31 bei 34.3, 47.0 und 14:34:12 bei 35.4, 42.5). Am 17.10. damit 3 Flechten aus 3 Erdwurzel-Knoten in Mulgore (kleine Stichprobe; AHledger nennt für Erdwurzel in Durotar 15 % von 39). «Grüner Daumen» um 14:25:37 (3 Erdwurzel, Objekt 657383), 68 Minuten nach der Ernte von 13:17.
- Lehrerlisten neu: Mooranta (Kürschnerei, 5 Einträge), Kray (Alchemie, 9), Thrag Stonehoof (Schmiedekunst, 23), Brek Stonehoof (Bergbau, 16), Gennia Runetotem noch einmal (182); `data/kombi/lehrer.csv` hat jetzt 11 Lehrer mit 369 Einträgen.

## Post zwischen den Charakteren

- 13:39 Druide an den Bankchar: 18 Silberblatt, 2 Malachit, 2 Tigerauge, 27 Leichtes Leder, 19 Friedensblume, 11 Leinenstoff, 36 Verdorbene Lederfetzen; Porto 2s 70c.
- 14:39 Bankchar holt ab. Die Zeile POST nennt nur 20 Leichtes Leder und 20 Fetzen; INVENTAR beim Ausloggen 20 s später zählt 27 und 36 (Befund 1).
- 14:40 Stufe 18 an den Bankchar: Geringer Mondstein, Rolle der Beweglichkeit, 2 Geringer Manatrank, 3 Glänzendes Schmuckstück und 8g; abgezogen 8g 1s 50c in zwei Buchungen.
- 14:42 Bankchar an den Druiden: 18 Silberblatt, 2 Malachit, 2 Tigerauge, 19 Friedensblume (Porto 1s 20c); der Druide holt sie um 14:42:47 in Thunder Bluff ab.
- 15:15 Bankchar: 1g verschickt (abgezogen 1g 30c); der Empfänger steht nicht im Testlog.
- Porto: Alle vier Abzüge passen zu 30c je angehängtem Stapel und 30c für einen Brief nur mit Gold (mit Stapeln zu 20: 9 Stapel = 2s 70c, 4 Stapel = 1s 20c, dazu 30c für das Gold). Wie viele Briefe es waren, zeigt das Testlog nicht (ungeprüft).
- Beim Bankchar liegen nach dem Ausloggen um 15:15 vom Druiden 27 Leichtes Leder, 36 Fetzen und 11 Leinenstoff. Der Druide trägt 6 Leichtes Leder und 5 Fetzen.

## Auktionshaus

Angebote des Druiden in Thunder Bluff, alle 24 Stunden (AH-ANGEBOT):

| Zeit | Gegenstand | Stück | Preis je Stück | Pfand | Händler je Stück |
|---|---|---|---|---|---|
| 14:37 | Gekräuselte Flechte | 3 | 2g 75s | 1s | 30c |
| 14:38 | Erdwurzel | 10 | 99c | 1s 20c | 20c |
| 14:38 | Friedensblume | 3 | 23c | 1s | 10c |
| 14:38 | Silberblatt | 7 | 10c | 1s | 10c |
| 14:38 | Malachit | 1 | 25c | 1s | 15c |
| 14:38 | Schriftrolle: CHAP BALK WELLES | 1 | 1s (je Angebot) | 1s | 15c |
| 15:02 | Tigerauge | 2 | 1s 8c | 1s 20c | 1s |
| 15:03 | Friedensblume | 19 | 23c | 1s 14c (Spiel: 1s 8c) | 10c |
| 15:03 | Silberblatt | 18 | 10c | 1s 8c | 10c |
| 15:03 | Rauer Stein | 2 | 5c | 1s | 2c |
| 15:03 | Kleines Ei | 4 | 1s 99c | 1s | 4c |
| 15:03 | Sehniges Wolfsfleisch | 7 | 1s 9c | 1s | 4c |

- Zusammen 12s 62c Pfand. Verkauft sich alles, bringt es 8g 61s 56c vor und 8g 18s 48c nach Gebühr, davon die Flechten 8g 25s vor Gebühr; ohne die Flechten 36s 56c vor und 34s 73c nach Gebühr, gegen 9s 48c beim Händler.
- Pfand: Alle 14 Angebote mit Pfand aus dem Geldabzug (Testlog 3.7) passen zu «60 % des Händlerpreises mal Menge, mindestens 1s» bei 24 Stunden, ebenso die Pfand-Rückgaben vom 16.10. (Moosachat 2s 40c bei 4s Händlerpreis, Schattenedelstein 1s 50c bei 2s 50c, Tigerauge 1s bei 1s) und der Grobe Faden vom 15.10. (1s). Andere Dauern sind ungeprüft. Das Spiel meldete zweimal weniger, als abgezogen wurde (1s 44c statt 1s 50c, 1s 8c statt 1s 14c).
- Verkauft: der Schattenedelstein des Bankchars (2s 90c, Gebühr 14c, mit Pfand 4s 26c; AH-POST 15:15:04). Beim Druiden kam um 15:02:27 ein Brief mit 1s 95c ohne Zeile AH-POST (Befund 2); der Betrag passt zur Schriftrolle (1s, minus 5c Gebühr, plus 1s Pfand), vermutlich.
- Scans in Thunder Bluff: 14:37 (51 632 Angebote, 2940 Gegenstände, 12 s) und 15:02 (52 363, 2959, 12 s). Unter dem Händlerpreis um 15:02: 6 Gegenstände, zusammen 7s 11c Gewinn.
- Erste Abnahme aus Scan-Paaren (13:36 → 14:37, 61 Minuten, Orgrimmar und Thunder Bluff teilen ein Haus; 14:37 → 15:02, 25 Minuten), geschätzt gekauft (`data/preise/ah_abnahme.csv`):

| Gegenstand | 61 Min | 25 Min |
|---|---|---|
| Leichtes Leder | 430 | 599 |
| Verdorbene Lederfetzen | 0 | 60 |
| Seltsamer Staub | 0 | 612 |
| Friedensblume | 85 | 0 |
| Erdwurzel | 23 | 0 |
| Roher glänzender Kleinfisch | 0 | 41 |
| Gekräuselte Flechte, Kleines Ei, Sehniges Wolfsfleisch, Silberblatt | 0 | 0 |

- Die Abnahme ist eine Schätzung (Risiko 24): Der verkaufte Schattenedelstein des Bankchars steht in keiner der beiden.
- Gekräuselte Flechte: Tiefstpreis 2g 75s (14:37) → 2g 50s (15:02), Angebot 193 → 236 Stück.

## Bagnon

- Bagnon 12.1.7 mit BagBrother liegt seit 17.10. 15:16:44 im AddOns-Ordner (`## Interface: … 16001` in beiden `.toc`), also nach dem letzten Ausloggen um 15:15:20. Geladen war es noch nicht: Die Datei `BagBrother.lua` (SavedVariables `BrotherBags`) fehlt; einen neuen Addon-Ordner lädt der Client erst nach einem Neustart des Spiels (Best Practice §5).
- Was BagBrother speichert (Code der installierten Version, `core/features/caching.lua`, gelesen 17.10.): pro Charakter Taschen, Ausrüstung, Geld, den Briefkasten beim Öffnen, die Bank beim Schliessen (Charakter- und Kontobank über `C_Bank.FetchPurchasedBankTabData`) und Briefe an eigene Charaktere gleich beim Senden (Haken an `SendMail`, eingetragen bei `MAIL_SEND_SUCCESS`), wenn Bagnon den Empfänger schon kennt. Den Tooltip mit der Anzahl pro Charakter (Taschen, Bank, Post) zeigt `core/features/itemTooltips.lua`, Einstellung `countItems`. Jeder Charakter muss sich dafür einmal mit Bagnon einloggen, die Bank einmal öffnen.
- RXP zählt bei `.collect` weiter nur den eingeloggten Charakter (Taschen, mit Flag 8 seine Bank; `functions.lua` Z. 88 und 3089, v4.11.23). Syndicator nutzt RXP nur im Quest-Planer (`DB/questDB.lua` Z. 25–39), Bagnon gar nicht für die Zähler.

## Befunde zum Testlog

1. POST «erhalten» zu kurz, wenn Gegenstände erst nach dem Ende der Sitzung in den Taschen ankommen: 14:39:22 nennt 20 statt 27 Leichtes Leder und 20 statt 36 Fetzen; die Sitzung endete nach 5 s mit «Interaktion zu». Eine Zeile TASCHE für den Rest fehlt ebenfalls (Ruhezeit 1,5 s nach dem Ende). INVENTAR beim Ausloggen stimmt, `tools/markt.py` rechnet mit INVENTAR.
2. AH-POST fehlt, wenn ein Brief schneller abgeholt wird, als das Testlog liest: Es liest 1 s nach `MAIL_SHOW` bzw. `MAIL_INBOX_UPDATE`, der Briefkasten war um 15:02:27 nur 2 s offen.
3. Hinweise im Chat (Warnung beim Händler, T31; «Abnahme messen», T32) schreibt das Testlog nicht in die Datei; ob sie kamen, zeigt es nicht.

## Was daraus geändert wurde (17.10.)

- `tools/markt.py`: Für Stufe A zählt Material bei Lager-Charakteren des Kontos mit (ohne Kürschnerei, Kräuterkunde, Lederverarbeitung und Verzauberkunst, also der Bankchar), mit dem Stand ihres letzten Ausloggens; Post im Briefkasten nicht. «AH statt Händler» nennt die gemessene Abnahme und den Pfand nach der Regel oben. `tools/testlog_harness.py` prüft beides.
- Kombiguide 0.6.2: nur Texte (gleiche Zeilenzahl): Pfand-Regel und Abnahme beim Auktionshaus in Thunder Bluff, Geselle Kürschnerei mit den gemessenen Werten. Stellen #116 (Druide) und #152 (Stufe 18) geprüft.
