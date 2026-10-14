# Entscheidungen

Nur was der Nutzer entschieden hat, mit Datum. Offenes steht unten.

## Getroffen

- vor 13.10.2026: Main ist ein Tauren-Druide für alle Rollen; Tauren-Bankchar.
- vor 13.10.2026: Fischen ist die Goldquelle.
- vor 13.10.2026: Lederverarbeitung und Verzauberkunst statt Kürschnerei und Lederverarbeitung; vorher bis etwa Stufe 15 Kräuterkunde und Kürschnerei.
- vor 13.10.2026: Leveln mit RestedXP bis Stufe 20, dann so schnell wie möglich Katzengestalt und 30 % Lauftempo.
- 13.10.2026: Hauptteil des Goldes im AH verdienen, immer veredelt (Leder verarbeiten, Verzauberungen, Fischen und Kochen).
- 13.10.2026: Weg A (ein Kombi-Guide aus RXP-Route und Berufsschritten) wird getestet.
- 13.10.2026: Repo `ludes88/wow-forever-kombiguide` angelegt, öffentlich.
- 13.10.2026: Keine persönlichen Daten im Repo, auch kein Vorname. Addons heissen deshalb `KombiTestlog` und `RXPGuides_Kombi`, die Guide-Gruppe `Kombiguide (H)`.
- 13.10.2026: Arbeitsregeln, Überlegungen und die Art der Zusammenarbeit mit KI bleiben bewusst sichtbar. Sie zeigen, wie der Nutzer arbeitet.
- 13.10.2026: Ziel ist möglichst wenig Arbeit für den Nutzer. Claude arbeitet direkt im Repo (Branch, Pull Request) und führt nach den automatischen Prüfungen selbst zusammen.
- 13.10.2026: Die Claude-Sitzung wird mit dem PC des Nutzers verbunden. Claude installiert Addon-Versionen selbst und liest die Testlog-Datei selbst. (Die App bot die Verbindung nicht an; der Nutzer hat stattdessen die AddOns mit dem Repo verknüpft, siehe `vorgehen.md`.)
- 13.10.2026: Die Mengen für Lederverarbeitung und Verzauberkunst werden auf eigene Forever-Messungen gestützt, nicht auf die Classic-Werte («wir machen es richtig und messen»). Dafür Testlog 3.
- 13.10.2026: «Beim Kräuterfarmen zählt immer das gewinnbringendste Kraut.» (Zuerst als «Kräutergarten» notiert; der Nutzer hat korrigiert.)
- 13.10.2026: Beim Fischen zählt der Fisch, der im AH gekocht (oder roh) am meisten bringt.
- 13.10.2026: Ziel: während des Speedruns die Berufe so effizient wie möglich mitskillen und genug Gold dafür haben, «inkl. der Skills usw.».
- 13.10.2026: Update-Rhythmus: «Ich aktualisiere so oft ich kann.» Claude baut neu, sobald es etwas Neues gibt (neue RXP-Version beim Nutzer oder eigene Änderung).
- 13.10.2026: LW-Route 1–150: Claude wählt «nach bestem Wissen und Gewissen».
- 13.10.2026: Der Nutzer hat seine Addons über CurseForge aktualisiert. Laut Testlog (13.10. 22:07) läuft jetzt RestedXP v4.11.23; der Kombi-Guide ist seither darauf gebaut.
- 13.10.2026: Der Nutzer überlässt Claude die Umsetzung. Claude setzt dafür die Datenkette aus Plan-Tabelle und Generator ein (Vorschlag von Claude, siehe `vorgehen.md`). Der Kombi-Guide wird für die RXP-Version gebaut, die beim Nutzer installiert ist (zurzeit v4.11.23).
- 13.10.2026: Mengen, Orte und Farmstellen sollen schon jetzt mit den Quests der Route verbunden sein, auch als Simulation, damit der Nutzer sie im Spiel testen kann («Falls du schon Mengenangaben und Locations und Farmspots mit den Speedrunquests synergieren kannst … dann bau das bitte ein»). Umgesetzt in Kombi-Guide v0.2 mit dem Mengenmodell `docs/plan/mengen-leder.md`.
- 14.10.2026: «Ab etwa Level 12 +/- geht es sowieso nach Crossroads und dort kann ich ja weiter farmen … Hauptsache es reicht auf Leder 150, Verz 150 bei Level 20 oder so.» Dazu der Auftrag, den RXP-Guide genau zu lesen. Claude liest das so: Das Material soll um Stufe 20 für Lederverarbeitung 150 und Verzauberkunst 150 reichen; ob es schon mit Stufe 15 fertig sein muss, ist als Rückfrage offen (der Satz «Es muss auch noch mit Level 15 fertig sein» lässt beides zu). Umgesetzt im Mengenmodell bis Stufe 20 und in Kombi-Guide v0.3 (Leder-Zähler und drei optionale Farm-Stopps).
- 14.10.2026: Der Guide soll genau zeigen, was mit welchem Material hergestellt, entzaubert und verzaubert wird und was ins AH geht: «Einfach ein absoluter no-brain Guide fürs Berufeskillen während dem RXP-Speedrun für maximale Level und profession progress und Gold-Effizienz». Umgesetzt in Kombi-Guide v0.4 (Stufen A bis D mit Stückzahlen) und `docs/plan/berufe-plan.md`.
- 14.10.2026: «Wenn es sich nicht lohnt mit leichtem Leder auf 150 zu kommen, dann tun wir das auch nicht! Dafür ist die Zeit zu schade», Mittleres Leder kauft der Nutzer im AH, finanziert über Fischen und über verkaufte Erzeugnisse. Umgesetzt: eigenes Leder bis LW 80, danach wird gekauft.
- 14.10.2026: Berufswechsel (Kräuterkunde zu Verzauberkunst, Kürschnerei zu Lederverarbeitung) in Orgrimmar: «In OG, aber es soll der Sweetspot an Verrissenem (diese kürschnere ich ja zu leichtem) und leichtem Leder in der Anzahl sein. Dann grinde ich halt ein paar Mobs mehr, aber es muss die errechnete Menge an leichtem Leder sein für einen Break-even an Investment von leichtem Leder.» Umgesetzt: Wechsel in «12-17 The Barrens» nach RXPs Schritt #108 (Stufe 16); Sweetspot nach der Lesart von Claude (offener Punkt 6): LW 1–80 aus eigenem Material, also 99 Fetzen und 62 Leichtes Leder (Zähler beim Farm-Stopp S1). Die Farm-Stopps S2 und S3 entfallen, weil danach nicht mehr gekürschnert wird.

## Offen

1. Welche Quellen-Widersprüche zuerst im Spiel geprüft werden.
2. Lizenz für die eigenen Teile.
3. Format der Plan-Tabelle: CSV mit Semikolon ist gesetzt (Vorgabe von Claude, für Excel), änderbar.
4. Welcher AH-Markt für die Preise zählt: zum Start ein EU-Realm, Normal oder PvP. Bis dahin rechnet Claude mit den US-Beta-Preisen von AHledger (Normal Horde).
5. Zählt beim «gewinnbringendsten Kraut» die Zusatzbeute mit (Swiftthistle, Frilled Lichen, Samen)? Claude rechnet vorerst mit Zusatzbeute, also mit dem Wert pro Kräuterknoten.
6. Lesart von «Break-even an Investment von leichtem Leder» (Rückfrage an den Nutzer). Claude liest: eigenes Leder dort einsetzen, wo es viele Punkte bringt (bis LW 80), und nur so viel sammeln, wie die Route samt RXPs Grinden auf Stufe 16 hergibt. Mehr Leder zu farmen lohnt sich bei Beta-Preisen erst, wenn Leichtes Leder etwa 4s 70c bis 7s 60c kostet (Vergleich mit Angeln, `docs/plan/berufe-plan.md` §1). Der Farm-Stopp S1 steht im Modell weiter mit 25 Minuten (Vorschlag); im Guide zeigt sein Zähler den Sweetspot (62 Leichtes Leder).
7. Woher das Material für Verzauberkunst kommt. Der Plan nimmt zuerst das eigene Entzauberungs-Material und kauft den Rest, pro Punkt die billigste Art. Zusätzliche Embossed Leather Gloves nur für Staub lohnen sich bei den Beta-Preisen «jetzt» nicht, mit den 30-Tage-Medianen schon (Preisregeln in `docs/plan/berufe-plan.md` §6); Bestätigung durch den Nutzer offen.
8. Stufe D (LW 130–150) ist der teuerste Teil: Beta-Einkauf etwa 7g 38s, davon kommen etwa 3g 85s über verkauftes Entzauberungs-Material zurück. Ob und wann, entscheidet der Nutzer.
9. Wie viel Zeit fürs Angeln als Goldquelle eingeplant wird. Der Plan nennt nur die Grössenordnung (Deviate Fish an der Lushwater Oasis, Rate und nötige Angelfertigkeit im Brachland ungeprüft).
10. Übriges Material nach VZ 150: verkaufen oder für LW und VZ über 150 behalten (Heavy Leather, Soul Dust, Greater Astral Essence).
11. Ob Kombi-Schritte in «12-17 The Barrens» vor Schritt #77 dazukommen dürfen. Dort steht der zweite Testcharakter; v0.3 und v0.4 fügen deshalb erst danach ein (Best Practice §6).
