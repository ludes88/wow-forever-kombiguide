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

---

# Abend 17.10. (15:22–17:08)

Quelle: die Testlog-Datei, Stand 17.10. 17:08 (Testlog 3.7.1, Kombiguide 0.6.1), über die Verbindung zum PC gelesen; dazu `BagBrother.lua` (SavedVariables von Bagnon) und die Schrittliste des Kombi-Guides (`tools/rxp_schritte.py liste … "6-12 Mulgore" --klasse druid`). Ohne Charakter-, Konto- und Realmnamen. Ausgewertet mit den Werkzeugen auf dem Branch `daten/2026-10-17-abend`.

## Sitzungen

| Zeit | Charakter | Guide und Stelle | Was |
|---|---|---|---|
| 15:22–15:37 | Tauren-Druide, Stufe 10 (75 %) → 10 (87 %) | «6-12 Mulgore» #116 → #123 | 1g vom Bankchar, Klassenzauber der Stufe 10, Angel-Quest bei Kaga Wildhoof, Fischgläser und Lagerstühle, Abgabe der Karawane |
| 15:37 | Bankchar, Stufe 1 | «6-12 Mulgore» #2 | 12 Sekunden, nur ein- und ausgeloggt |
| 15:37–17:08 | Tauren-Druide, Stufe 10 (87 %) → 12 (16 %) | «6-12 Mulgore» #123 → #153 | Mine der Venture Co. (3 Tode), Bloodhoof, Thunder Bluff (Waffenmeister, Auktionshaus, Post), Moonglade (Bärengeist), Kochen am eigenen Lagerfeuer |

Alle Sitzungen melden Client 70450, Kombiguide 0.6.1-v4.11.23, Testlog 3.7.1 und KombiDaten «17.10. 13:36, 6 Tipps». Der Stand vom Nachmittag (Kombiguide 0.6.2 und die KombiDaten aus dem Testlog von 15:15) kam erst nach dem Einloggen um 15:37 auf den PC und lädt beim nächsten Einloggen. Keine Zeile FEHLER.

## Stellen

- Druide: #116 → #153 (`.turnin 5930` «Great Bear Spirit», Moonglade), Stufe 12 (16 %). Neue Kombi-Schritte in «6-12 Mulgore» vor #153 nur mit `#maxlevel 11` (seit 0.6.3; geprüft mit `tools/rxp_schritte.py vergleich … --stelle 153 --stufe 12`).
- Stufe 18: weiter #152.

## Notizen im Spiel und was dahinter steht

1. 15:23:57 «ich musste mir 1 fg vom bankchar schicken da ich ansonsten zuwenig gold für die klassenspells habe. dies muss in der scharfen verison einbezogen werden»: Vor dem Lehrer hatte der Druide 4s 63c. Die vier Zauber der Stufe 10 kosteten 12s (Lehrer −9s und −3s, 15:24:11 und 15:24:15); der Bankchar hatte um 15:15 1g geschickt (POST 15:23:03, +1g). Kosten aller Klassenzauber: Tabelle unten.
2. 15:26:28 bei Kaga Wildhoof «die angelquest ist ein muss sie gibt sdk beim lagerffeueur»: 97932 «Grundlagen des Zeltens: Angeln», angenommen 15:25:47 bei Kaga Wildhoof (Mulgore 46.2, 67.2), abgegeben 15:26:41 bei 44.2, 63.8 (dort lernte der Druide am 13.10. Angeln; die Abgabe ist laut warcraft.wiki.gg bei Uthan Stillwater): 270 XP und das Rezept Fischglas (1229745: 1 Roher glänzender Kleinfisch und 1 Leere Phiole). Ziel der Quest ist Angeln 20 (warcraft.wiki.gg, Stand 11.10.2026); der Druide hatte 25. RXP führt die Quest für die Horde nicht (v4.11.23; Hauptzweig 17.10. nur «Camping 101: Fishing» 97967 im Skyborne-Guide). «sdk»: Lesart von Claude «Segen der Könige» (das Fischglas gibt am Lagerfeuer +8 % auf alle Werte und stapelt nicht mit Segen der Könige, wow-professions Camping Guide); Rückfrage offen.
3. 16:12:50 «in TB zwingend auch zweihandwaffe für 2 hand streitkolben lehren bei genügend Gold», zurückgenommen um 16:50:44 («ignoriere den letzten post wegen dem 2 hand ich war zu vorschnell»). Dazu steht im Testlog nur: Der Druide lernte Zweihandstreitkolben um 16:50:29 bei Ansekhwa (Thunder Bluff 40.8, 62.3) für 10s; RXP führt den Schritt selbst («6-12 Mulgore» #141 «Train Two-Handed Maces», `<< Shaman/Druid`). Eine Zeile GELERNT gab es dabei nicht.

## Klassenzauber des Druiden

Lehrerliste von Gennia Runetotem (Bloodhoof 47.4, 62.9), 17.10. 15:24, mit allen drei Filtern (182 Einträge bis Stufe 60; `data/kombi/lehrer.csv`):

| Stufe | Zauber | Kosten |
|---|---|---|
| vor 10 | Dornen 1, Heilende Berührung 2, Mal der Wildnis 1, Mondfeuer 1, Verjüngung 1, Wucherwurzeln 1, Zorn 2 (alle gelernt; die Lernstufe nennt die Liste bei gelernten nicht) | 8s 10c |
| 10 | Griff der Natur 1, Mal der Wildnis 2, Mondfeuer 2, Verjüngung 2 (um 15:24 gelernt); Demoralisierendes Gebrüll 1 (gesperrt, kommt mit der Bärengestalt) | 15s (je 3s) |
| 12 | Nachwachsen 1, Wiederbelebung 1, Wutanfall | 24s (je 8s) |
| 14 | Dornen 2, Heilende Berührung 3, Hieb 1, Zorn 3 | 36s (je 9s) |
| 16 | Mondfeuer 3, Prankenhieb 1, Verjüngung 3 | 42s (je 14s) |
| 18 | Feenfeuer 1, Griff der Natur 2, Nachwachsen 2, Winterschlaf 1, Wucherwurzeln 2, Zermalmen 2 | 90s (je 15s) |
| 20 | Demoralisierendes Gebrüll 2, Heilende Berührung 4, Mal der Wildnis 3, Omen der Klarsicht, Schreddern 1, Sternenfeuer 1, Wiedergeburt 1 | 1g 68s (je 24s) |
| 22 | Mondfeuer 4, Tier besänftigen 1, Verjüngung 4, Zorn 4 | 1g 32s (je 33s) |

- Zahlen nach dem Zauber = Rang. Von Stufe 10 bis 22 zusammen 5g 7s, bis zum Wechsel in Orgrimmar (Stufe 16) 1g 17s. Nach dem Lernen um 15:24 noch offen bis Stufe 16: 1g 5s (11 Zauber). Die Katzengestalt (RXP v4.11.23: bei Loganaar in Moonglade ab Stufe 20, `.train 768`) steht nicht auf der Liste; ihr Preis ist ungeprüft.
- Waffenmeister Ansekhwa (Kreatur 11869): Zweihandstreitkolben 10s (Liste mit Filter lernbar und gesperrt, 1 Eintrag).

## Gold des Druiden

- 15:22 4s 63c; nach dem Gold vom Bankchar und den Zaubern 92s 63c; 17:08 1g 19s 59c.
- 15:22–17:08 (die Summe geht auf den Kupfer genau auf): Einnahmen Briefe 1g 34s 63c (1g vom Bankchar, 34s 63c aus sechs AH-Verkäufen mit dem Pfand zurück), Händler 14s 73c, Quests 4s 50c, Geld aus Beute 5s 22c. Ausgaben Lehrer 22s (Klassenzauber 12s, Zweihandstreitkolben 10s), Händler 14s 17c (20 Eiskalte Milch 5s, 5 Leere Phiolen 20c, 10 Einfaches Holz 3s 80c, Feuerstein und Zunder 1s 35c und 3s 82c um 16:47 in Bloodhoof ohne gekauften Gegenstand, vermutlich Reparatur nach den Toden, ungeprüft), Pfand 7s 5c, Porto 90c. Ohne das Gold vom Bankchar: +14s 96c.
- Ganzer Tag (12:57–17:08, Stufe 7,74 → 12,16): ohne das Gold vom Bankchar etwa +18s (Quests 15s 75c, Geld aus Beute 9s 94c, Händler 27s 11c, AH-Briefe 36s 58c; Lehrer 31s, Pfand 19s 67c, Händler 17s 1c, Porto 3s 60c).

## Messwerte des Druiden

- Stufe 10,75 → 12,16 (Sitzungen 14 und 90 Minuten, `docs/plan/spiel.md`), 11 Quests abgegeben, darunter 98424 «Fizsprockets Notizen» (850 XP, in RXPs Route). 3 Tode in der Mine der Venture Co. (16:23:40 bei 58.7, 48.4; 16:30:40 bei 59.1, 48.2; 16:45:48 bei 62.7, 45.9); die Ursache steht nicht im Testlog. Stufe 11 in Mulgore: 64 Minuten, 0,97 Stufen pro Stunde.
- Kürschnerei 61 → 72: 29 Häute in 28 Minuten (15:35–16:04): Prairie Wolf Alpha (2960) 23 (8 Leichtes Leder, 15 Fetzen), Prairie Stalker (2959) 2 (1 und 1), Flatland Cougar (3035) 2 (0 und 2), Prairie Wolf (2958) 1 (1 und 0), Flatland Prowler (3566) 1 (1 und 0); zusammen 11 Leichtes Leder und 18 Fetzen, etwa 24 Leichtes Leder pro Stunde. Namen: AHledger, Seite Mulgore (abgerufen 17.10.). Zweimal stand Beute nach dem Kürschnern in SAMMELN (Sehniges Wolfsfleisch, Hasenpfote), wie am Mittag.
- Kräuterkunde 24 → 31: 7 Knoten (12 Friedensblume, 5 Erdwurzel), keine Flechte. «Grüner Daumen» dreimal (15:36:14 Friedensblume, 15:51:20 und 16:09:26 Erdwurzel), Abstände 15 und 18 Minuten.
- Kochkunst 16 → 32: 16 Verkohltes Wolfsfleisch am eigenen Einfachen Lagerfeuer (Moonglade, 16:57–16:59), jedes +1 (orange). Das Lagerfeuer: 1 Einfaches Holz ergibt ein «Einfaches Lagerfeuerset» (279981).
- Lager: 5 Fischgläser (15:28) und 2 Lagerstühle (15:31, je 3 Leichtes Leder und 2 Einfaches Holz), alle grau, kein Punkt. Beim Ausloggen 11 Leichtes Leder und 23 Fetzen in den Taschen, beim Bankchar 27 und 36.
- Händler im Dorf der Bluthufe (Ort beim Kauf): 20 Eiskalte Milch für 5s (46.7, 64.5), 5 Leere Phiolen für 20c (45.5, 61.8), 10 Einfaches Holz für 3s 80c (45.3, 61.4). Am 13.10. kaufte der Druide dort die Angel (45.5, 61.7, 23c); laut AHledger (Seite Mulgore) verkauft Harn Longcast im Dorf die Angel. In Thunder Bluff: Feuerstein und Zunder 1s 35c (51.3, 52.4).
- Karte Moonglade (1450) exakt aus KARTE (16:57): RXPs Kommentare passen genau (9 Punkte, `tools/karte_aus_testlog.py`).

## Post und Auktionshaus

- 16:53 an den Bankchar: 51 Leinenstoff (20, 20 und 11), Porto 90c in einer Buchung, also 30c je angehängtem Stapel.
- Verkauft (AH-POST 16:47:17 am Briefkasten in Bloodhoof, das Geld um 16:51 in Thunder Bluff abgeholt, +34s 63c mit Pfand): 2 Tigerauge zu 1s 8c, 7 Sehniges Wolfsfleisch zu 1s 9c, 10 Erdwurzel zu 99c, 25 Silberblatt zu 10c, 22 Friedensblume zu 23c, 2 Rauer Stein zu 5c; Gebühr zusammen 1s 34c (5 %). Beim Abholen in Thunder Bluff keine zweite Zeile für dieselben Briefe (T16). Der Händler zahlt dafür 1s, 4c, 20c, 10c, 10c und 2c je Stück.
- Neue Angebote 16:52 (24 Stunden): 10 Erdwurzel zu 1s 34c (Pfand 1s 20c), 13 Friedensblume zu 25c (1s), Pläne: Runenverzierte Kupferbrustplatte 3s (1s), 2 Kupfererz zu 2s 34c (1s), Schriftrolle: CHAP BALK WELLES 3s (1s), Skalpiertomahawk der Intelligenz 5s (1s 85c, das Spiel meldete 1s 80c). Alle sechs passen zur Pfand-Regel (Händlerpreise 20c, 10c, 1s 50c, 5c, 15c, 3s 9c); damit 24 Angebote.
- Scan 16:51 in Thunder Bluff: 53 001 Angebote, 2903 Gegenstände, 12 s, 109 Minuten nach dem Scan von 15:02. Geschätzt gekauft: Friedensblume 576, Visionenstaub 514, Erdwurzel 439, Roher Langzahniger Matschschnapper 379, Königsblut 362, Sehniges Wolfsfleisch 206, Silberblatt 154, Roher glänzender Kleinfisch 132, Gekräuselte Flechte 11; Leichtes Leder 0 (207 weniger im Angebot, aber neue billigere dazu; 61 und 25 Minuten vorher 430 und 599, die Schätzung schwankt stark).
- Tiefstpreise 15:02 → 16:51: Friedensblume 23c → 25c (Angebot 1378 → 411), Erdwurzel 99c → 1s 34c (1532 → 653), Sehniges Wolfsfleisch 1s 9c → 1s 20c (406 → 113), Gekräuselte Flechte 2g 50s → 2g 74s 99c (236 → 200; die drei Flechten des Druiden stehen seit 14:37 zu 2g 75s). Seltsamer Staub 33c, Geringe Magieessenz 77c, Große Magieessenz 99c.
- Unter dem Händlerpreis um 16:51: 9 Gegenstände, zusammen 4s 46c.

## Bagnon

- `BagBrother.lua` gibt es seit dem Neustart (17:08 gelesen): Taschen, Bank, Briefkasten, Ausrüstung und Geld für den Druiden und den Bankchar. Die 51 Leinenstoff stehen schon im Briefkasten des Bankchars. Der Druide trägt 4 Leinentaschen (je 6 Plätze), seine Bank (48 Plätze) ist leer.
- Beim Druiden steht dort Stufe 17 statt 12. BagBrother setzt die Stufe beim Einloggen (`UnitLevel`) und bei `PLAYER_LEVEL_UP` (`core/features/caching.lua`); woher die 17 kommt, ist ungeprüft. Für das Zählen der Gegenstände spielt es keine Rolle.

## Was daraus geändert wurde (17.10. abends)

- Kombiguide 0.6.3: «Grundlagen des Zeltens: Angeln» in «6-12 Mulgore» (Wunsch des Nutzers, Notiz 15:26): vor Kaga Wildhoof bei Harn Longcast eine Angel kaufen und bei Uthan Stillwater Angeln lernen, nach «Camping 101: Cooking» die Quest bei Kaga annehmen, am Stonebull Lake bis Angeln 20 angeln (etwa 9 Minuten nach der Rate vom 13.10.), bei Uthan abgeben (Plan-Zeilen 92–96). Alle fünf Schritte mit `#maxlevel 11`: Der Druide (Stufe 12) sieht sie nicht und behält #153; neue Charaktere sehen sie. Zeile 4 sagt jetzt, woher der Kleinfisch für Thunder Bluff kommt. Die Annahmen für Kräuterkunde und Kürschnerei bei Kaga (Zeilen 83 und 84) bleiben aus (offene Entscheidung 11).
- `tools/markt.py`: Beim Gold für den Wechsel in Orgrimmar zählen die noch offenen Klassenzauber bis Stufe 16 mit, aus der letzten Lehrerliste des Charakters (beim Druiden 1g 5s, zusammen mit Stufe A etwa 1g 65s gegen 1g 19s 59c); für andere Charaktere mit Lehrerliste eine Zeile bis zur nächsten Zielstufe (16, 20, 22). Waffenmeister zählen nicht. `tools/testlog_harness.py` prüft es.
- Wie der Guide selbst an das Gold für die Klassenzauber erinnern soll, ist offen (offene Entscheidung 41).

---

# Spätabend 17.10. (17:20–18:24)

Quelle: die Testlog-Datei, Stand 17.10. 18:24 (Testlog 3.7.1; Kombiguide 0.6.2 bis 17:56, danach 0.6.3), über die Verbindung zum PC gelesen; dazu RXP v4.11.23 (Code und Guide-Dateien im RXP-Klon) und der Forever-UI-Code 1.60.1 (70450, https://github.com/Gethe/wow-ui-source/tree/forever, Commit 172a387). Ohne Charakter-, Konto- und Realmnamen. Ausgewertet mit den Werkzeugen auf dem Branch `daten/2026-10-17-spaet`.

## Sitzungen

| Zeit | Charakter | Guide und Stelle | Was |
|---|---|---|---|
| 17:20–17:34 | Tauren-Druide, Stufe 12 (16 %) → 12 (21 %) | «6-12 Mulgore» #153 → #161 | Abgabe «Grosser Bärengeist» (5930) in Moonglade, Flug nach Thunder Bluff, «Leder sammeln» angenommen, AH-Briefe |
| 17:34 | Bankchar, Stufe 1 | «6-12 Mulgore» #2 | 1 Leichtes Leder an den Druiden (Porto 30c) |
| 17:34–17:51 | Tauren-Druide, Stufe 12 (21 %) → 12 (42 %) | «6-12 Mulgore» #161 → #170 | «Leder sammeln» abgegeben, Mulgore |
| 17:51–17:56 | Bankchar | – | Ausrüstung für den Druiden im AH gekauft (3g 8s und 2g 15s), 7 Teile an ihn geschickt |
| 17:56 | Tauren-Druide | #170 | `/reload` mit Kombiguide 0.6.3 und KombiDaten «17.10. 16:51, 12 Tipps» |
| 17:56–18:24 | Tauren-Druide, Stufe 12 (42 %) → 12 (63 %) | «6-12 Mulgore» #170 → #172 | Ausrüstung aus der Post, Händler, 2 AH-Angebote, Harpyien für Quest 744 im Westen von Mulgore |

Alle Sitzungen: Client 70450, Testlog 3.7.1, keine Zeile FEHLER.

## Stellen

- Druide: #153 → #172 (`.complete 760,1`, Stufe 12, 63 %). Nach der Abgabe von 768 (17:35:28) sprang RXP selbst von #164 auf #170. Kombiguide 0.6.3 hielt die Stelle #170 beim `/reload` um 17:56 (T6).
- Stufe 18: weiter #152.

## Notizen im Spiel und was dahinter steht

1. 17:22:53 «ich hätte den ruhestein ausparren sollen.. bitte erwähne das im guide. Wichtig! nach TB laufen DANN moonglade DANN RS»: Der Druide war um 16:49 mit dem Ruhestein von Bloodhoof nach Thunder Bluff gekommen (34 s) und musste aus Moonglade fliegen. RXP v4.11.23 sagt Druiden an dieser Stelle schon «Travel to Thunder Bluff» (statt «Hearth to Thunder Bluff» für alle anderen; `Horde-1-12_Mulgore.lua`, Schritte nach «Thunderhorn2») und in Moonglade «Hearth to Thunder Bluff» nur ohne Abklingzeit (`.cooldown item,6948,>0`), sonst «Fly to Thunder Bluff». Flug: RXP rechnet 543 Sekunden von Nighthaven nach Thunder Bluff (`DB/forever/flightData.lua`, Knoten 69 nach 22); im Testlog von der Annahme von 5932 (17:20:53) bis zur Ankunft in Thunder Bluff (17:30:42) knapp 10 Minuten, bis zur Abgabe (17:31:59) 11 Minuten.
2. 17:26:38 «mir fällt auf dass beim fliegen die flugzeit von moonglade nach tb nicht angezeigt wird»: RXP hat die Flugzeit (Punkt 1) und einen Flug-Timer (`Timers.lua`: beim Öffnen der Flugkarte `C_TaxiMap.GetAllTaxiNodes`, Start bei `PLAYER_CONTROL_LOST`). Warum er nicht erschien, ist ungeprüft; das Testlog schreibt die Flugkarte und den Flug nicht mit.
3. 17:34:00 «natürlich mache ich die leder quest. plane diese +12 ein bitte»: Das Mengenmodell zieht die 12 schon ab (`data/kombi/modell_leder.csv`, Art «Verbrauch»); `/tl tipp` zählte sie bisher nicht. Seit 17.10. (spät) zählt `tools/markt.py` für Sammler 12 Leichtes Leder mehr, solange keine Zeile QUEST AB 768 im Testlog steht. Der Druide gab 768 um 17:35:28 ab (875 XP, Leichtes Leder −12, danach 0 in den Taschen).
4. 17:37:59 «normalerweise werden mobs im rxp automatisch markiert der haken ist in den rxp optionen drinn aber es passiet nie»: RXP setzt in Forever keine Zielmarkierungen von selbst: `Targeting.lua` Z. 56 «Retail/Forever cannot SetRaidTarget automatically, leverage button» (der Ziel-Knopf von RXP setzt sie mit `/tm` im Makro) und Z. 979 (`UpdateMarker` endet für `FOREVER` sofort; RXP v4.11.23).
5. 17:51:28 «um schneller voran zu kommen kaufe ich mir gear. dies wird im release nicht gehen daher bite ignorieren»: Der Bankchar kaufte um 17:54 und 17:55 im AH für 3g 8s (6 Käufe) und 2g 15s (1 Kauf) und schickte 7 Teile an den Druiden (17:56). Diese Käufe zählen in keiner Rechnung.

## Messwerte

- Stufe 12 (16 % → 63 %): 47 % einer Stufe in 57 Minuten (Sitzungen 13, 17 und 27 Minuten); Quests: «Leder sammeln» 875 XP, «Grosser Bärengeist» 420, «Zurück nach Thunder Bluff» 85.
- Kürschnerei 72 → 74, Kräuterkunde 31 → 34; «Grüner Daumen» um 18:15:05 (2 Erdwurzel, eigene Objekt-ID), wie am Nachmittag.
- Beute: «Muster: Unverwüstliche Lederhose» (7288) von Kreatur 2964 (18:05, Westen von Mulgore); der Händler zahlt 1s 25c (`data/preise/haendler_ankauf.csv`).
- Karten Dunkelküste (1439), Ashenvale (1440) und Steinkrallengebirge (1442) exakt aus KARTE (Flug 17:22–17:30), übernommen mit `tools/karte_aus_testlog.py`.
- Lehrerliste Mooranta (Kürschnerei, Thunder Bluff, 17.10.): Experte gesperrt, ab Kürschnerei 125, 50s; Fachmann ab 200, 5g (`data/kombi/lehrer.csv`).

## Post und Auktionshaus

- AH-POST 17:33:40 (Thunder Bluff): 4 Kleines Ei zu 1s 99c (Gebühr 39c), Pläne: Runenverzierte Kupferbrustplatte 3s (15c), Skalpiertomahawk der Intelligenz 5s (25c); mit dem Pfand +19s 2c.
- Neue Angebote 17:58 (24 Stunden): Geprägte Lederhose 7s (Pfand laut Geldabzug 2s 8c, das Spiel meldete 2s 4c; Händler 3s 47c), Schnitzmesser der Magie 21s (Geldabzug 1s 93c, das Spiel meldete 1s 92c; Händler 3s 23c). Beide passen zur Regel 60 % des Händlerpreises; beim Schnitzmesser (193,8c) nur abgerundet. Damit 26 Angebote; von den 5, die mit Geldabzug noch im Testlog stehen, ist das Schnitzmesser das einzige, bei dem Runden und Abrunden verschieden ausgehen.
- Scan 17:52 in Orgrimmar (Bankchar): 53 688 Angebote, 2899 Gegenstände, 61 Minuten nach dem Scan von 16:51; `tools/ah_aus_testlog.py`: 186 neue Preiszeilen, 164 neue Abnahme-Zeilen, 95 Händlerpreise neu oder geändert.

## Was daraus geändert wurde (17.10. spät)

- Kombiguide 0.6.4:
  - Ruhestein-Hinweis für Druiden vor Moonglade (Plan-Zeile 97, Notiz 1).
  - Gold-Hinweise vor den Druiden-Lehrern der Stufen 10, 12, 14 und 18 mit den gemessenen Kosten (Zeilen 98–101, offene Entscheidung 41). Jeder verschwindet, sobald genug Gold da ist (`.money >X`).
  - Die Annahme von «Grundlagen des Zeltens: Kürschnerei» und «…: Kräuterkunde» bei Kaga Wildhoof ist eingeschaltet (Zeilen 83 und 84, offene Entscheidung 11; das Log zeigt Annahme und Abgabe beider Quests, je 270 XP und ein Rezept).
  - Zeile 10 sagt, dass die 12 Leder für «Leder sammeln» eingeplant sind.
  - Schritte in «6-12 Mulgore» vor der Stelle des Druiden tragen `#maxlevel 11`, der in «12-17» `#maxlevel 17`. Geprüft mit `tools/rxp_schritte.py vergleich` für alle 9 Klassen: Stellen #172 (Stufe 12) und #152 (Stufe 18) bleiben. `tools/rxp_schritte.py ziele` findet alle Ziele (beide Gruppen).
- `tools/build_kombi.py`: In `extra` wird ein Eintrag mit `<<` zum Filter des ganzen Schritts (`step << Tauren Druid`), und `@nur <Gruppe>` baut eine Zeile nur in diese Gruppe ein (RXPs Dungeon-Route «12-17» hat keinen Lehrer in Moonglade).
- `tools/markt.py`: +12 Leichtes Leder für Sammler, solange 768 nicht abgegeben ist (Notiz 3). Den Pfand rundet es jetzt ab (Schnitzmesser). `tools/testlog_harness.py` prüft beides.
