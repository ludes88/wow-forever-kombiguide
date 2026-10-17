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
