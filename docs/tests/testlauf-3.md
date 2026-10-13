# Testlauf 3 – Mulgore 6 → 10 mit Testlog 3 (ab 13.10.2026, läuft)

Ziel: Messdaten für v0.2 (Mulgore 6–12): Leder pro Tierart, Kräuter pro Knoten, Geld pro Kill und Händlerbesuch, Lehrerkosten auf Stufe 8 und 10. Dazu Test T6 (Fortschritt nach einem Update).

Aufbau: Tauren-Druide, Stufe 6, Kürschnerei 1/75, Kräuterkunde 5/75. Addons nach dem CurseForge-Update und `aktualisieren.bat` (Stand `37141b8`), Spiel neu gestartet.

## Erster Abschnitt (13.10., 22:07–22:11)

| Nr. | Beobachtung | Bedeutung |
|---|---|---|
| 1 | SITZUNG meldet RestedXP **v4.11.23**, «Kombiguide 0.1.2-v4.11.13», «Testlog 3», «Kombi-Test 1», Geld 65c | CurseForge hat RXP von v4.11.13 auf v4.11.23 gebracht. Der Kombi-Guide aus der v4.11.13-Route läuft auch mit RXP v4.11.23 (T0 bestanden) |
| 2 | Fortsetzung bei «06-12 Mulgore #13», dann #14 bis #18 | Das Update v0.1.1 → v0.1.2 (nur Koordinaten) hat die Stelle behalten (T6 für diesen Fall bestanden) |
| 3 | Das WC-Test-Addon (`RXPGuides_Kombi`) ist jetzt geladen; nach dem `/reload` um 19:50 war es das nicht | Neu verknüpfte Addon-Ordner brauchen einen Neustart des Spiels; `/reload` genügt nur für Addons, die schon geladen waren |
| 4 | Erste SITZUNG nach dem Neustart ohne Gebiet, Karte 1414 (Kalimdor), eine Sekunde später GEBIET Mulgore | Fehler A aus Testlauf 1 tritt nach einem Neustart wieder auf. Behoben in Testlog 3.1: Der Start wartet, bis der Client eine Zone meldet (höchstens etwa 12 Sekunden) |
| 5 | KARTE 1414 Kalimdor: (0,0) = 12799.90, 17066.60; (1,1) = −11733.30, −19733.21; 36799.8 × 24533.2 Yards | in `data/karten/forever_karten.csv` übernommen. RXP nutzt Karte 1414 in der Datei der Brachland-Guides (12–22) 43-mal (v4.11.13), aber ohne Kommentar-Koordinaten; Vergleich deshalb nicht möglich |
| 6 | QUEST AB 99108 «Sparringskampf», XP 550, kein Geld | Testlog 3 schreibt Geld in QUEST AB nur, wenn es welches gibt |
| 7 | `/tl list` wurde zur Notiz «list» | `/tl liste` und `/tl list` öffnen ab Testlog 3.1 das Protokoll wie `/tl zeigen` |

## Neubau auf RXP v4.11.23 und Test T6

- `tools/build_kombi.py v4.11.23`: keine Probleme; 4 Guides, 3 Plan-Zeilen. «1-6 Mulgore» ist unverändert (468 Zeilen).
- «6-12 Mulgore» hat neu die Quest 99411 «Kyle's Gone Missing!» bei Ahab Wheathoof (`#softcore`): Annahme vor dem alten Schritt #17, dazu Sammeln von «Tender Strider Meat» und vor der Abgabe von 748 ein Schritt «Kyle füttern».
- So findet RXP die Stelle wieder (Code v4.11.23):
  - Die Schritt-Kennung ist die Zeilennummer im Guide-Text. RXP zählt nur nicht-leere Zeilen, Kommentare entfernt es vorher (`GuideLoader.lua`, Schleife `string.gmatch(text, "[^\n\r]+")`, `step.stepId = linenumber + guide.guideId`).
  - Die Nummer in der Zeile RXP zählt nur Schritte, die angezeigt werden (`addon.ProcessGuideTable` mit `addon.IsStepShown`). Für den Tauren-Druiden fehlen zum Beispiel alle `#hardcore`-Schritte.
  - Findet RXP die Kennung nicht, nimmt es die gespeicherte Nummer (`GuideWindow.lua`, `LoadGuide`).
- Stand beim Ausloggen (22:42): «06-12 Mulgore #28». Das ist der Schritt «Well» für Quest 754 «Säuberung von Winterhoof» (Zeile 293 im alten Bau).
- Im Neubau beginnt bei Zeile 293 kein Schritt. RXP nimmt deshalb die Nummer 28; das ist im Neubau die Abgabe von 748 (Zeile 328). Die ist erledigt, ebenso #29 (Quest 771 ist abgegeben). RXP hakt beide ab und steht dann auf #30 «Well», also an derselben Stelle wie vorher.
- Erwartet nach `aktualisieren.bat` und `/reload`: SITZUNG mit «Kombiguide 0.1.2-v4.11.23», in der Zeile RXP kurz #28, dann #30. Ab hier sind die Nummern um 2 höher als im alten Bau.
- Quest 99411 hat der Charakter nicht. Spätere Schritte dazu zeigt RXP trotzdem (Kyle füttern; eine Abgabe ohne Bedingung) mit dem Hinweis «Missing pre-requisites». Überspringen oder die Quest nachholen.
- Korrektur: Die Erwartung, die hier vorher stand (#18, «Zeile 62», Annahme von Quest 743), beruhte auf einer falschen Zeilenzählung und gilt nicht mehr.

## Zweiter Abschnitt (13.10., 22:12–22:42): Messwerte

Charakter Stufe 6 → 7, Mulgore zwischen Bloodhoof und Stonebull Lake, RXP «06-12 Mulgore» #18 bis #28. Namen der Kreaturen zu den IDs: AHledger, Seite Mulgore (https://ahledger.com/wow-forever/zones/mulgore, Links der Kreaturen, 13.10.).

**Kürschnern** (21 Häute, Kürschnerei 1 → 22, jede Haut +1 Punkt, jede Haut genau 1 Gegenstand)

| Kreatur | Häute | Leichtes Leder | Verdorbene Lederfetzen |
|---|---|---|---|
| 2958 Prairie Wolf | 14 | 4 | 10 |
| 2956 Adult Plainstrider | 4 | 3 | 1 |
| 3035 Flatland Cougar | 2 | 1 | 1 |
| 2959 Prairie Stalker | 1 | 0 | 1 |
| zusammen | 21 | 8 | 13 |

- Zeit: 12 Häute 22:15–22:22 und 9 Häute 22:34–22:40, nebenbei Quest 748. Hochgerechnet aus diesen rund 12 Minuten: etwa 40 Leichtes Leder pro Stunde. Die Stichprobe ist klein.
- Zum Vergleich MetaForge (Vanilla-Daten, Best Practice §9): Kodo Calf (7–8) 40 % Leder, Zhevra Runner (13–14) 60 %.

**Kräuter** (5 Knoten, Kräuterkunde 5 → 10, jeder Knoten +1 Punkt)

| Knoten (Objekt-ID) | Knoten | Kräuter |
|---|---|---|
| 1618 Friedensblume (Peacebloom) | 2 | 3 + 2 |
| 1617 Silberblatt (Silverleaf) | 3 | 1 + 2 + 2 |

Keine Zusatzbeute (Samen) in diesen 5 Knoten.

**Angeln** am Stonebull Lake (Karte 1412, 45.4, 65.2), 22:27:57–22:33:46

- 14 Fänge: 11 Roher Langzahniger Matschschnapper (6289), 3 Roher glänzender Kleinfisch (6291).
- Angeln 1 → 15, jeder Fang +1 Punkt.
- Wie oft ein Fisch entkam, zeigt Testlog 3.1 nicht (es zählt keine Würfe). Testlog 3.2 schreibt die Würfe pro Fang mit.
- Wert laut AHledger (US-Beta, PvP Horde, 13.10.; `docs/recherche/2026-10-13_kraeuter-fische-kochen.md`): Kleinfisch roh 1s 18c, Matschschnapper roh 6c.

**Lehrer und Händler**

| Zeit | Was | Kosten oder Ertrag | Ort (Spielkoordinaten) |
|---|---|---|---|
| 22:23 | verkauft: Gerissener Eckzahn, 2× Gesträubte Feder | +1s 30c | 1412 46.0, 64.0 (Bloodhoof) |
| 22:24 | Angeln gelernt bei Uthan Stillwater: Angeln (7620 und 1240948), «Köder und Angelzubehör» (1278067) | −1s | 1412 44.2, 63.8 (Stonebull Lake) |
| 22:25 | verkauft: 3× Leinenverband, Kleines Ei | +34c | 1412 45.0, 61.8 (Bloodhoof) |
| 22:25 | Kochkunst gelernt bei Pyall Silentstride (2550 und 1240945); Rezepte Verkohltes Wolfsfleisch (2538), Geröstetes Eberfleisch (2540), Kräutergebackenes Ei (8604), Einfaches Lagerfeuer (1229737) | −1s | 1412 44.9, 61.7 (Bloodhoof) |
| 22:26 | Angel (6256) beim Händler gekauft | −23c | 1412 45.5, 61.7 (Bloodhoof) |

- Uthan Stillwater steht laut wow-professions bei 44.6, 60.6 (Best Practice §9). Gemessen: 44.2, 63.8, also rund 130 Yards weiter südlich. Vermutlich eine Classic-Koordinate, die nicht zur Forever-Karte passt (wie RXPs Kommentar-Koordinaten in Mulgore, Risiko 17).
- Pyall Silentstride: gemessen 44.9, 61.7; das passt zu RXPs Weltkoordinaten (`.goto 1412/1,-285.000,-2263.400`, umgerechnet 44.9, 61.7) und zu wow-professions (45.0, 61.6).

**Geld**

- Quests ohne Geld: 99108, 96659, 96605, 96661, 771 und 748 gaben nur XP (550, 410, 410, 270, 625, 450).
- Beute: Tiere ohne Geld; ein Venture Co. Hireling (2975) gab 1c.
- Verlauf: 65c beim Einloggen, höchstens 1s 96c, 7c beim Ausloggen.

**Quests der Berufe (Forever, neu)**

- Bei Kaga Wildhoof (1412 46.2, 67.2) angenommen: 97933 «Grundlagen des Zeltens: Kräuterkunde» und 97936 «Grundlagen des Zeltens: Kürschnerei». Abgabe: **ungeprüft**.
- RXPs Horde-Route führt beide nicht (v4.11.13, v4.11.23 und Hauptzweig vom 13.10. abends). Für die Allianz hat RXP die Gegenstücke (97924 Skinning, 97921 Herbalism) mit `.skill skinning,<1,1` usw. (`Guides/forever/Alliance-1-13_Human.lua`). Kandidat für Kombi-Guide v0.2.

## Zweiter Abschnitt: Befunde zum Testlog

| Nr. | Beobachtung | Folge |
|---|---|---|
| 8 | Die Zeile POST um 22:42:30 kam mit ENDE beim Ausloggen. Darin stehen als «verschickt» die Quest-Gegenstände, die bei den Abgaben verbraucht wurden, und als «erhalten» alles, was ab etwa 22:26 dazukam (Fische, Leder, Kräuter) | Eine Post-Sitzung blieb von etwa 22:26 bis zum Ausloggen offen: MAIL_SHOW kam, danach kein MAIL_CLOSED. Solange war auch TASCHE still. Die Zeilen SAMMELN, ANGELN und BEUTE stimmen trotzdem. Ob um 22:26 ein Briefkasten offen war, ist **ungeprüft** (Frage an den Spieler) |
| 9 | Das Forever-UI öffnet und schliesst Briefkasten, Händler, Auktionshaus, Lehrer und Flugkarte über den Interaktions-Manager (`PLAYER_INTERACTION_MANAGER_FRAME_SHOW`/`_HIDE`; `PlayerInteractionFrameManager.lua`, `MailFrame.lua`, Forever-UI 1.60.1) | Testlog 3.2 nutzt diese Ereignisse zusätzlich. Ausserdem endet ein Fenster, wenn das Blizzard-Fenster nicht mehr sichtbar ist und keine Interaktion läuft (`C_PlayerInteractionManager.IsInteractingWithNpcOfType`), wenn der Charakter mehr als 25 Yards weggeht oder bei Gebietswechsel und Ladebildschirm. Die Zeile nennt Dauer und Grund («Ende MAIL_CLOSED», «Ende Fenster zu» usw.) |
| 10 | 6 Zeilen «BEUTE \| Quelle ? \| keine Gegenstände»: 4 davon 3–4 Sekunden vor einem Kürschnern, eine direkt vor der richtigen Beute-Zeile derselben Sekunde, eine allein | Lootfenster ohne Inhalt und ohne Quelle. Testlog 3.2 schreibt dafür keine Zeile mehr |
| 11 | SAMMELN «Opening - No Text» an Objekt 2912 (Bernsteinkorn) und 2910 (Quellstein) | Quest-Gegenstände, die man aufhebt. Für die Berufe zählen nur SAMMELN mit Kürschnerei, Kräuterkunde oder Bergbau |
| 12 | Um 22:42 noch «Kombiguide 0.1.2-v4.11.13», «Testlog 3» | Der Stand von PR #8 war noch nicht geholt; T6 für den Neubau steht noch aus |

## Noch offen in diesem Testlauf

- Stufe 8 und 10: Lehrer (GELD, GELERNT) bei Gennia Runetotem (Bloodhoof, laut RXP-Route)
- T6 nach dem Neubau auf v4.11.23 im Spiel (Erwartung oben)
- Testlog 3.2 im Spiel: Endet jede Fenster-Sitzung mit einem Grund? Kommt MAIL_CLOSED, wenn der Briefkasten normal geschlossen wird?
