# Messplan Beta: Daten mit den Druiden sammeln (14.–22.10.2026)

Stand 15.10.2026. Die Beta läuft bis 22.10. mit Stufengrenze 30 (https://www.warcrafttavern.com/forever/guides/beta/).

Jede Messung beantwortet eine offene Frage im Plan. Bei jeder steht, welche Zahl sie ersetzt. Ob, welche und wann gemessen wird, entscheidest du. Die Reihenfolge unten ist ein Vorschlag.

Grundlagen:
- Goldquellen und Rechnungen: `docs/recherche/2026-10-14_goldquellen.md`
- Pläne: `docs/plan/berufe-plan.md`, `docs/plan/mengen-leder.md`
- Tests T3–T12: Best Practice §10

## Kurzliste bis 22.10. (Vorschlag von Claude, 15.10.)

Du willst in der Beta nur noch wenig spielen, damit die Lust zum Start bleibt (15.10.). Die Liste nimmt nur, was der Plan zum Start braucht und was sich beim Spielen zum Start nicht ohnehin nebenbei misst. Was du davon machst, entscheidest du.

Vorher einmal: `aktualisieren.bat`, dann `/reload`. Die Zeile SITZUNG zeigt «Testlog 3.6».

**Sitzung 1, etwa 2 Stunden (Schätzung aus den Dauern unten): ein Druide auf Stufe 15–16 mit Kürschnerei, Kräuterkunde und Angeln, der Kürschnerei und Kräuterkunde verlernen darf**
1. Orgrimmar: das Auktionshaus öffnen. Der AH-Scan läuft von selbst. Offen lassen, bis «AH-Scan fertig» im Chat steht, und einmal vergleichen: Zeigt das Auktionshaus für Leichtes Leder denselben Tiefstpreis? Steht stattdessen «übersprungen» oder kommt nichts: `/tl ah`. (M11, T15)
2. Orgrimmar, je ein paar Sekunden (neu in Testlog 3.6, M12): den Briefkasten öffnen (T16) und die Bank (T18). Wenn du magst, ein billiges Stück im Auktionshaus einstellen, z. B. 1 Leichtes Leder (T19); kommt es später verkauft oder abgelaufen zurück, misst der Briefkasten das mit.
3. Orgrimmar: Berufswechsel mit dem Kombi-Guide («12-17 The Barrens», Block nach «SpiritsPickup», in der Schrittliste direkt wählbar) oder von Hand nach `docs/plan/berufe-plan.md` §2, Stufe A. So weit Material und Gold reichen, kein Leder extra farmen. Bei Kamari, Karolek, Jhag und Godan im Lehrerfenster den Filter einmal auf alle drei Arten stellen. Danach jedes Berufsfenster einmal öffnen, auch Angeln und Kochen (Rezepte, T17). (M5, M1, T11)
4. Lushwater Oasis im Brachland (etwa 46.8, 39.4; aus RXP umgerechnet, im Spiel ungeprüft): 30 Minuten angeln. (M3)
5. Bist du am Ende wieder an einem Auktionshaus (Orgrimmar und Thunder Bluff teilen eines): nochmals öffnen. Zwei Scans 15 Minuten bis 2 Stunden auseinander ergeben die erste Abnahme (T20).
6. Danach jeden anderen Druiden einmal einloggen und wieder aus. (M2)

**Sitzung 2, wenn du magst (Schritt 7 etwa 10 Minuten, 8 etwa 10 Minuten mit Wegen, 9 30 Minuten; geschätzt)**
7. Ein Druide auf Stufe 21–22: im Kombi-Guide «17-22» die letzten Schritte wählen, in den gekauften Guide wechseln, ein paar Schritte gehen, zurück in den Kombi-Guide und wieder in den gekauften. Steht er noch am selben Schritt? (M9, T5, T14)
8. Der Druide aus Sitzung 1 in Thunder Bluff: Lehrerfenster von Una (Lederverarbeitung, Experte) sowie Mot und Teg Dawnstrider (Verzauberkunst), Filter auf alle drei Arten; dort nochmals das Auktionshaus und den Briefkasten öffnen, als zweiter Scan an einem anderen Tag. (M1, M11, M12)
9. Nur mit einem Druiden mit Kräuterkunde ab 70: 30 Minuten Kräuter im Südbrachland, dazu `/tl M4 Bountiful Harvest Rang <Zahl oder keiner>`. (M4)

Ist der Ordner `KombiDaten` mit Empfehlungen schon da (schreibe ich, sobald ich Zugriff auf deinen WoW-Ordner habe): beim ersten Mal das Spiel neu starten, dann `/tl tipp` (T21).

Weggelassen, weil es beim Spielen zum Start ohnehin mitläuft oder teuer ist: M6 (Farm-Stopp S1), M7 (Armor Kits), M8 (Orte), M10 (Sitzung in Thunder Bluff).

**Nach jeder Sitzung**
- `/reload` oder ausloggen. Erst dann schreibt WoW die Datei.
- Ist dieser Chat mit deinem PC verbunden und der PC an: «fertig» schreiben, ich lese die Datei selbst. Sonst die Datei `World of Warcraft\_classic_beta_\WTF\Account\<KONTO>\SavedVariables\KombiTestlog.lua` im Chat anhängen. Sie enthält alles, auch die AH-Scans.
- Notizen braucht es keine, ausser in Schritt 9. Wenn etwas nicht stimmt: `/tl bug <was>`.
- Seit Testlog 3.6 enthält die Datei auch deinen Bestand, deine Rezepte und die Briefe des Auktionshauses. Daraus rechne ich die Empfehlungen (`tools/markt.py`); ins Repo kommen davon nur die Marktpreise und die Abnahme, ohne Namen.

## So läuft eine Messung

1. `aktualisieren.bat`, dann `/reload`. SITZUNG zeigt «Testlog 3.6». Seit 3.4: die Zeile LEHRER, die beim Öffnen eines Lehrerfensters die ganze Liste schreibt. Seit 3.5: AH-SCAN beim Öffnen des Auktionshauses (M11). Neu in 3.6: REZEPTE (Berufsfenster), INVENTAR (Taschen, Bank), AH-POST (Briefkasten), AH-ANGEBOT (eigenes Angebot) und die Abnahme zwischen zwei AH-Scans (M12).
2. Zu Beginn `/tl M3 Start`, am Ende `/tl M3 Ende` (mit der Nummer der Messung). Die Notiz schreibt Ort, Stufe und Berufe dazu. So finde ich die Abschnitte im Protokoll.
3. Spielen wie unten beschrieben. Das Testlog schreibt das meiste selbst: SAMMELN, ANGELN, HERSTELLEN, ENTZAUBERN, LEHRER, GELD, QUEST AB, BERUF, AH-SCAN.
4. Danach `/reload` und das Protokoll schicken:
   - Am besten die Datei `WTF\Account\<KONTO>\SavedVariables\KombiTestlog.lua`; nur sie enthält die AH-Scans ganz. Ist der Chat mit deinem PC verbunden, lese ich sie selbst.
   - Notfalls `/tl zeigen`: die letzten 1000 Einträge zum Kopieren (vom AH-Scan nur die Plan-Gegenstände, ohne Preisstufen).
   - Die Datei enthält Charakter- und Realmnamen. Sie kommt nicht ins Repo; ich übernehme nur die Zahlen.

Für die Messungen braucht es den Kombi-Guide nicht. Wer ihn auf einem Messcharakter lädt, speichert dort eine eigene Stelle. Welche Stellen bei einem Neubau erhalten bleiben müssen, ist offen (`docs/entscheidungen.md`, Punkte 11 und 14).

## Übersicht

| Nr. | Frage | Druide | Dauer | Kurzliste (15.10.) |
|---|---|---|---|---|
| M1 | Lehrerlisten: Lernstufen, Kosten, was lernbar ist | jeder, der an einem Lehrer vorbeikommt | 1–2 Min pro Lehrer | Sitzung 1 und 2 |
| M2 | Gold pro Stufe | alle Druiden | 1 Min pro Druide | Sitzung 1 |
| M3 | Angeln an der Lushwater Oasis | ab etwa Stufe 14, mit Angeln | 30 Min | Sitzung 1 |
| M4 | Kräuter und Frilled Lichen im Südbrachland | Stufe 16–22, Kräuterkunde ab 70 | 30 Min, dazu Route | Sitzung 2, wenn es den Druiden gibt |
| M5 | Sitzung in Orgrimmar (T11) | ab Stufe 10; darf die Berufe wechseln | 60 Min | Sitzung 1 |
| M6 | Farm-Stopp S1 (T10) | Stufe 13–16, mit Kürschnerei | 20 Min | weggelassen |
| M7 | Medium Armor Kit und Mystic Medium Armor Kit | LW 50–105 | 20 Min | weggelassen |
| M8 | Orte und Widersprüche vor Ort (T8) | jeder | nebenbei | weggelassen |
| M9 | Ende von «17-22» und Sprung in den gekauften Guide (T5), Wechsel hin und zurück (T14), Stellen mit `#completewith` (T3) | Stufe 21–22 | 10 Min | Sitzung 2 |
| M10 | Sitzung in Thunder Bluff (T12) | Stufe 20, LW etwa 80 und VZ etwa 50 | 60 Min | weggelassen |
| M11 | AH-Scan (T15), Abnahme zwischen zwei Scans (T20) | jeder, am Auktionshaus | ungeprüft (Schätzung: 1–2 Min) | Sitzung 1 und 2 |
| M12 | Rezepte, Bestand, Briefe des Auktionshauses, eigenes Angebot (Testlog 3.6, T16–T19) | jeder | je wenige Sekunden | Sitzung 1, Briefkasten auch in 2 |

## M1 Lehrerlisten (Testlog 3.4)

**Frage**
- Ab welcher Fertigkeit lässt sich ein Rezept lernen? Die Quellen widersprechen sich:
  - Widersprüche 17 und 20 (Best Practice §9)
  - AHledgers Farben könnten berechnet sein (`2026-10-14_goldquellen.md` §5)
- Was kosten Geselle, Rezepte und Druidenzauber pro Stufe? Im Guide steht bisher «Kosten ungeprüft».
- Führt ein Lehrer Barbaric Bracers, Mystic Medium Armor Kit oder Heavy Armor Kit?

**Ablauf**
1. Lehrerfenster öffnen.
2. Einmal den Filter (Auswahl oben im Fenster) auf alle drei Arten stellen: verfügbar, nicht verfügbar, bereits bekannt.
3. Fenster schliessen. Mehr braucht es nicht; die Zeile LEHRER nennt den Filter.

Pro Lehrer und Sitzung schreibt das Testlog eine Zeile. Darin steht jeder Eintrag mit Status (lernbar, gesperrt, gelernt), Lernstufe (Stufe, Beruf und Fertigkeit) und Kosten; bei Rezepten auch die Item-ID, sofern der Client sie liefert. Ungeprüft: ob ein Berufslehrer seine Liste auch einem Charakter ohne den Beruf zeigt.

**Lehrer** (Namen und Orte: Best Practice §9 und RXP v4.11.23)
- Druide:
  - Gennia Runetotem (Bloodhoof)
  - Turak Runetotem (Thunder Bluff, Elder Rise)
  - Loganaar (Moonglade)
- Lederverarbeitung:
  - Orgrimmar: Kamari (Lehrling), Karolek (Geselle)
  - Thunder Bluff: Mak, Tarn, Una
  - Chaw Stronghide (Bloodhoof), Krulmoo Fullmoon (Camp Taurajo)
- Verzauberkunst:
  - Orgrimmar: Jhag, Godan
  - Thunder Bluff: Mot und Teg Dawnstrider
- Kürschnerei: Mooranta (Thunder Bluff), Yonn Deepcut (Bloodhoof); in Orgrimmar Thuwd (Widerspruch 15: LW- oder Kürschnerei-Lehrer)
- Kräuterkunde: Komin Winterhoof (Thunder Bluff)
- Angeln: Kah Mistrunner (Thunder Bluff), Uthan Stillwater (Stonebull Lake)
- Kochen: Aska Mistrunner (Thunder Bluff), Pyall Silentstride (Bloodhoof), Duhng (Crossroads)

**Ersetzt**
- Lernstufen in `data/kombi/rezepte.csv`
- «Kosten ungeprüft» in den Guide-Texten (`plan.csv`, z. B. Zeilen 22, 27, 30 und 38)
- Lehrerkosten in der Goldbilanz (`docs/vorgehen.md`, Datenkette 3)
- Widersprüche 3, 4, 5, 6, 15, 16, 17 und 20

## M2 Gold pro Stufe

**Frage:** Wie viel Gold hat ein Druide auf Stufe 16 (Orgrimmar) und 20 (Thunder Bluff)? Reicht es für Stufe B schon in Orgrimmar (etwa 1g 68s, Beta)?

**Ablauf**
- Jeden Druiden einmal einloggen. SITZUNG schreibt Stufe und Geld von selbst.
- Dazu eine Notiz, zum Beispiel: `/tl M2 RXP-Route ja, AH genutzt nein, Berufe seit Stufe 5`.

Quest-Geld kommt nebenbei aus jeder Sitzung (QUEST AB mit Geld). Am 13.10. gaben die Quests in Mulgore nur XP.

**Ersetzt:** Die Goldbilanz gibt es noch nicht. Bisher fehlt jede Zahl zum Gold bei Stufe 16 und 20 (Best Practice §1, offene Punkte).

## M3 Angeln an der Lushwater Oasis

**Frage**
- Wie viele Fänge gibt es pro Stunde?
- Wie oft entkommt ein Fisch oder ein Wurf geht leer?
- Wie hoch ist der Anteil Deviate Fish?
- Ab welcher Angelfertigkeit entkommt im Brachland nichts mehr? Classic-Quellen sagen 75 oder 100; für Forever ist es nicht veröffentlicht.

**Ort**
- Lushwater Oasis, etwa 46.8, 39.4 (Mitte der RXP-Schleife um den See, umgerechnet, im Spiel ungeprüft)
- Ausweichstellen: Forgotten Pools 45.1, 22.5 und Stagnant Oasis 55.6, 42.8
- Herleitung: `2026-10-14_goldquellen.md` §3

**Ablauf**
- 30 Minuten nur angeln, mit gleichbleibendem Köder oder ohne.
- Zu Beginn notieren: `/tl M3 Start Angeln <Fertigkeit>, Köder <welcher>`.
- Die Zeile ANGELN nennt Fang und Würfe seit dem letzten Fang; BERUF nennt jeden Punkt.
- Ideal sind zwei Druiden: einer unter 75 Angeln, einer ab 100.

**Ersetzt**
- Fangrate und Deviate-Anteil in `tools/plan_berufe.py`: `ANGELN_FAENGE_H` (Stonebull Lake, Mulgore) und `DEVIATE_ANTEIL` (AHledger 35 % von 153)
- Damit die Rechnung «Angeln pro Stunde» (berufe-plan §1 und §6) und die offene Entscheidung 9 (Angelzeit)
- Grundlage für Kombi-Guide v0.5 (Angeln als Goldquelle)

## M4 Kräuter und Frilled Lichen im Südbrachland

**Frage**
- Wie viele Kräuterknoten schafft man pro Stunde, und wie viele Kräuter gibt ein Knoten?
- Wie oft fallen Frilled Lichen und Swiftthistle?
- Hängt die Rate an Stufe oder Kräuterkunde? Ein Spielerbericht sagt «mostly for low characters or low skill».

Davon hängt ab, ob sich Kräuterkunde bis Thunder Bluff lohnt. Break-even gegen Angeln: etwa 14–15 Knoten pro Stunde bei NH-Preisen jetzt, 19–22 mit 30-Tage-Preisen (`2026-10-14_goldquellen.md` §2).

**Druide**
- Stufe 16–22, Kräuterkunde ab 70 (Briarthorn ab 70 laut Icy Veins)
- Zwei Druiden mit verschieden hoher Kräuterkunde wären ideal.

**Ort**
- Südbrachland. AHledger: Briarthorn bei «Southern Barrens» und «Lushwater Oasis», Mageroyal bei Agama'gor, Earthroot bei The Dry Hills.
- Koordinaten der Knoten: nicht gefunden.

**Ablauf**
- a) 30 Minuten nur Kräuter sammeln (Kräutersuche an).
- b) Wenn Zeit ist: die Route «17-22» spielen und nur mitnehmen, was am Weg liegt. Das ist die Zahl für die Variante «Kräuterkunde bis Thunder Bluff».
- Zu Beginn notieren, ob der Legacy-Bonus «Bountiful Harvest» aktiv ist und welcher Rang. Laut foreverchanges gibt er +20 % bis +100 % Scarce-Material und verändert damit die Rate.
- SAMMELN schreibt jeden Knoten mit Objekt-ID und Beute (Frilled Lichen hat die ID 249399).

**Ersetzt**
- Wert pro Kräuterknoten (offene Entscheidung 5) und Break-even gegen Angeln
- Grundlage für die Entscheidung, ob Kräuterkunde bis Thunder Bluff bleibt (offene Entscheidung 12)

## M5 Sitzung in Orgrimmar (T11)

**Frage**
- Wie geht das Verlernen? (Widerspruch 18)
- Lassen sich die VZ-Rezepte 20–40 wie geplant lernen? (Widerspruch 17)
- Wie viele Herstellungen pro Punkt braucht es?
- Was gibt das Entzaubern der Embossed Leather Gloves?
- Wie lange dauert die Sitzung, und was kostet sie?

**Druide**
- Ab Stufe 10, wegen des Gesellen.
- Er muss Kürschnerei und Kräuterkunde hergeben dürfen: Verlernen löscht die Fertigkeit.
- Material für Stufe A: 99 Fetzen, 62 Leichtes Leder, 27 Light Hide (Rest im AH, etwa 20s), dazu Händlerware für etwa 21s (berufe-plan §2).

**Ablauf**
- Mit dem Kombi-Guide (Block nach «SpiritsPickup» in «12-17») oder von Hand nach berufe-plan §2, Stufe A.
- Bei Abweichungen `/tl bug <was>`.
- HERSTELLEN schreibt jeden Versuch mit «Punkt» ja oder nein. ENTZAUBERN schreibt, was aus welchem Teil kam. LEHRER, GELERNT und GELD schreiben Kosten und Rezepte.

**Ersetzt**
- Farben und Lernstufen in `rezepte.csv`
- Herstellungen pro Abschnitt in `bedarf_lw_vz.csv`
- Entzauberungswerte in `data/rechnung/Kreislauf.csv`
- Dauer und Kosten von Stufe A
- Texte der Plan-Zeilen 20, 21, 27, 35, 36 und 38

## M6 Farm-Stopp S1 (T10)

**Frage**
- Wie viele Häute gibt es pro Stunde?
- Welcher Anteil ist Leichtes Leder, Fetzen und Light Hide, und wie viele Stück gibt eine Haut ab Gegnerstufe 11?

**Ort**
- S1 bei 53.7, 12.8 (Plan-Zeile 17; Mitte der RXP-Schleifen #81/#82 in «12-17»)
- Gegner: Raptoren und Savannenkatzen

**Ablauf**
- 20 Minuten nur töten und kürschnern.
- SAMMELN schreibt jede Haut mit Kreatur-ID und Beute.

**Ersetzt**
- Anteile in `data/kombi/kuerschnern_anteile.csv` (bisher MetaForge/VMaNGOS, also Classic)
- Annahme «50–80 Häute pro Stunde» (berufe-plan §1 und §8)
- Minuten in `farmstopps.csv`
- Den Sweetspot-Zähler (62 Leichtes Leder) prüft T9 nebenbei.

## M7 Medium Armor Kit und Mystic Medium Armor Kit

**Frage:** Ab wann geben die beiden Rezepte Punkte, und ab wann keine mehr? AHledger nennt 50/90/97/105 und 55/95/102/110. Lohnt die Variante B' (`2026-10-14_goldquellen.md` §4)?

**Druide**
- Lederverarbeitung 50–105, zum Beispiel der Druide aus M5 nach Stufe A
- Material: Mittleres Leder (4 pro Kit), Coarse Thread; für Mystic dazu 2 Strange Dust und 2 Minor Mana Potion pro Stück
- Muster laut AHledger bei Tamar in Orgrimmar für 4s 50c, im Spiel ungeprüft

**Ablauf**
- Beide Rezepte lernen; die Lehrerliste (M1) zeigt die Lernstufe.
- Von 80 bis zum ersten Fehlschlag herstellen; HERSTELLEN zeigt «Punkt» ja oder nein.

**Ersetzt:** Farben in `rezepte.csv`. Danach kann ich die Variante B' für dich durchrechnen; ob sie in den Plan kommt, ist offene Entscheidung 15.

## M8 Orte und Widersprüche vor Ort (T8)

Nebenbei, wenn ein Druide vorbeikommt: neben die Person stellen und `/tl M8 <Name>` tippen. Die Notiz schreibt die Koordinaten dazu.

| Widerspruch (Best Practice §9) | Was tun |
|---|---|
| 1 Yonn Deepcut, Bloodhoof: 45.6, 57.8 oder 45.0, 61.4 | Notiz neben ihm |
| 2 Mooranta, Thunder Bluff: drei Quellen | Notiz neben ihr |
| 7 Bruiseweed ab Kräuterkunde 85 oder 100 | mit Kräuterkunde 85–99 einen Knoten versuchen, Meldung als `/tl` |
| 10 Lager von Durotar Supply bei den Crossroads, Dokimi: 50.1, 29.3 oder 42, 34 | Notiz neben Dokimi |
| 15 Thuwd in Orgrimmar: LW- oder Kürschnerei-Lehrer | Lehrerfenster öffnen (M1) |
| 19 Mote of Magic im AH | im AH suchen, `/tl` mit Preis |
| Orte von Tamar und Kithas in Orgrimmar (ungeprüft) | Notiz neben ihnen; ein Kauf schreibt HÄNDLER mit Ort |

## M9 Ende von «17-22» (T5) und `#completewith` (T3)

- Ein Druide auf Stufe 21–22 lädt in RXP «Kombiguide (H)» → «17-22» und wählt in der Schrittliste die letzten Schritte.
- Erwartet: Nach dem letzten Schritt springt RXP in den gekauften Guide «22-24 Hillsbrad», oder es kommt eine klare Meldung.
- Bei Problemen `/tl bug <was>`.
- T14: Nach ein paar Schritten im gekauften Guide zurück in den Kombi-Guide und wieder in den gekauften wechseln. Erwartet: RXP steht im gekauften Guide am selben Schritt (RXP speichert die Stelle pro Guide, `RXPCData.guideProgress`, Best Practice §3). Das braucht es für Berufs-Halte nach Stufe 22 (Weg B, offene Entscheidung 18).
- T3 nebenbei: Bleibt irgendwo ein Schritt hängen, an dem ein Kombi-Schritt neben einem RXP-Schritt mit `#completewith` steht, `/tl bug` mit der Schrittnummer.

## M10 Sitzung in Thunder Bluff (T12)

- Druide auf Stufe 20 mit LW etwa 80 und VZ etwa 50; Kombi-Guide «17-22», Block nach «DeathDUPpickup».
- Geprüft wird:
  - Schon erledigte Stufen verschwinden.
  - Die Einkaufszähler stimmen für «B und C», «C allein» und «D».
- Dazu Dauer und Kosten der Stufen B–D.
- Teuer: Stufe D allein kostet in der Beta etwa 7g 38s.

## M11 AH-Scan (Testlog 3.5, T15)

**Frage**
- Läuft der Scan im Spiel? Ungeprüft sind: ob der Index bei 0 oder 1 beginnt (das Testlog erkennt es selbst), ob der Sofortkaufpreis für das ganze Angebot gilt (Preis pro Stück = Sofortkauf durch Anzahl), wie lange der Scan dauert und wie lange der Server danach sperrt.
- Bleiben die Scans über Ausloggen und Tage erhalten? Daraus kommen die Wochenpreise.

**Ablauf**
- Das Auktionshaus öffnen. Der Scan läuft von selbst, höchstens alle 15 Minuten (so oft wie der Auto-Scan von AHledger, https://www.curseforge.com/wow/addons/ahledger; wie lange der Server sperrt, steht dort nicht). Die 15 Minuten gelten fürs ganze Konto: Hat ein anderer Charakter gerade gescannt, meldet der Chat «übersprungen». Das Auktionshaus offen lassen, bis «AH-Scan fertig» kommt.
- Einmal vergleichen: den Tiefstpreis von Leichtem Leder in der Chatmeldung mit dem Preis im Auktionshaus. Weicht er ab: `/tl bug AH-Preis <was du siehst>`.
- Von Hand: `/tl ah`. Ausschalten: `/tl ah aus`, einschalten: `/tl ah an`.
- Läuft daneben ein anderes Scan-Addon mit Auto-Scan (z. B. AHledger), eines davon ausschalten: `/tl ah aus` oder dort `/ahl auto off` (Befehl laut https://www.curseforge.com/wow/addons/ahledger).

**Ersetzt**
- Den Preis «jetzt» in `data/rechnung/Preise.csv` und `data/kombi/preise_zusatz.csv`, sobald du es willst (`tools/ah_aus_testlog.py --eintragen`, offene Entscheidung 17): 7-Tage-Median aus vollständigen Scans, nur bei mindestens 50 Stück im Angebot. Bis dahin vergleicht der Bericht `docs/plan/ah-preise.md` nur.
- Grundlage für die Wochenpreise zum Start.
- Seit Testlog 3.6 (T20): Zwei vollständige Scans 15 Minuten bis 2 Stunden auseinander ergeben die Abnahme («geschätzt gekauft», eine Schätzung) in `data/preise/ah_abnahme.csv`. Ungeprüft, ob der Client die Restlaufzeit als 0–3 oder 1–4 zählt; das Testlog erkennt es am Wert 0 oder 4 und schreibt die Grenzen der Bänder (`GetTimeLeftBandInfo`) in jeden Scan.

## M12 Rezepte, Bestand, AH-Post, eigenes Angebot (Testlog 3.6, T16–T19)

**Frage**
- Was kann jeder Charakter herstellen, mit welchen Reagenzien, und welche Farbe hat ein Rezept bei welcher Fertigkeit?
- Was liegt in Taschen, Bank und Kontobank?
- Was hast du im Auktionshaus angeboten, verkauft, gekauft, und was lief ab? Das sind die einzigen echten Verkaufsbelege; ein Scan zeigt nur Angebote.

**Ablauf**
- Jedes Berufsfenster einmal öffnen (auch nach dem Lernen neuer Rezepte). Die Zeile REZEPTE schreibt alle gelernten Rezepte; danach nur Farbwechsel. Ist im Fenster ein Filter an («nur herstellbar», Suche), sagt die Zeile «Liste unvollständig».
- Bank öffnen: INVENTAR mit Bank und Kontobank. Taschen schreibt das Testlog beim Ein- und Ausloggen selbst.
- Briefkasten öffnen: AH-POST mit den Briefen des Auktionshauses (verkauft, abgelaufen, gekauft). Die Briefe musst du dafür nicht öffnen. Ungeprüft: ob der Client Preis und Gebühr auch für ungeöffnete Briefe liefert; sonst steht zuerst nur die Betreffzeile (Art, Gegenstand, Menge), und sobald ein Brief einmal offen war, trägt das Testlog die Rechnung nach («Rechnung ergänzt»).
- Etwas einstellen: AH-ANGEBOT mit Menge, Preis, Dauer und Pfand.

**Ersetzt**
- Die Rezepte, Reagenzien und Farben aus AHledger und wow-professions durch die des Spiels (Widersprüche 17 und 20).
- Grundlage für `tools/markt.py`: Was du herstellen kannst und was es bringt, was du im Bestand hast, was sich bei dir verkauft.

## Was danach passiert

- Ich werte jede Lieferung aus und trage die Messwerte mit Datum in die Tabellen ein: `rezepte.csv`, `kuerschnern_anteile.csv`, `bedarf_lw_vz.csv`, `Kreislauf.csv`, Konstanten in `plan_berufe.py`. AH-Scans übernimmt `tools/ah_aus_testlog.py` nach `data/preise/` (ohne Realm- und Charakternamen).
- Dazu rechnet `tools/markt.py` die Empfehlungen (herstellen, kaufen und wieder verkaufen, aus dem Bestand verkaufen, farmen) und schreibt sie nach `build/markt/` und als Addon `KombiDaten` (im Spiel `/tl tipp`). Das bleibt bei dir, nicht im Repo.
- Danach rechne ich die Pläne neu und baue den Guide neu. Der Bericht sagt, welche Zahl sich wie geändert hat.
- Entscheidungen bleiben bei dir. Mit M3 und M4 lassen sich die offenen Punkte 9 (Angelzeit) und 12 (Kräuterkunde bis Thunder Bluff) entscheiden; mit M1 und M7 der Punkt 15 (verkaufen statt entzaubern).
- Beta-Daten gelten für die Beta. Zum Start am 04.11. prüfe ich Preise und Orte nach (Risiko 6).
