# Kampfdaten: Schaden, Zauber, Werte, Ausrüstung (erzeugt von `tools/kampf_aus_testlog.py`)

Nicht von Hand ändern: neues Testlog einlesen und neu erzeugen. Ohne Charakternamen und Uhrzeiten.

## Quellen

- Testlog 4.0 (Forever-UI 1.60.1, Build 70450, https://github.com/Gethe/wow-ui-source/tree/forever): Schaden, Heilung und erlittener Schaden pro Zauber aus Blizzards Schadensmesser `C_DamageMeter` (nach dem Kampf gelesen, im Kampf «secret»); Treffer, Krits und Ausweichen am Spieler aus `UNIT_COMBAT`; Zauber mit Zeit aus `UNIT_SPELLCAST_SUCCEEDED`; Nahkampfschläge aus `PLAYER_SWING`; Werte aus `UnitStat` und Co. mit der Umrechnung des Charakterfensters (`GetCritChanceFromStat`, `GetAttackPowerForStat`, `Camelot/PaperDollFrameStats.lua`); Ausrüstung aus `GetInventoryItemLink` und `C_Item.GetItemStats`; Talente aus `C_Traits`.
- Gewichte für Gegenstände und Lagerbuffs: RestedXP v4.11.23 DB/forever/StatWeights.lua (CC BY-NC-SA 4.0, https://github.com/RestedXP/RXPGuides); RXPs Zahlen fürs Leveln (Speedrun), kein Messwert.
- Fischglas «8% increased stats», Lagerstuhl «2% increased critical strike chance with all spells and attacks» (Tooltips, https://metaforge.app/wow-forever/database/consumables/fish-bowl und …/camp-chair, abgerufen 17.10.2026). Gerechnet wird mit den fünf Grundwerten (Lesart; der Tooltip nennt sie nicht einzeln).
- Mana aus Intellekt: 15 je Punkt laut Warcraft Tavern (Forever, https://www.warcrafttavern.com/forever/guides/stats/).
- Grenzen: Ohne Schadensmesser (Funktion fehlt, keine neue Sitzung, Werte geheim) steht der eigene Schaden nur als Schätzung aus den Treffern am Ziel (allein, ohne Gruppe). Prozent-Effekte von Gegenständen (Krit, Treffer) liefert `GetItemStats` vielleicht nicht; das Testlog hält dafür die Tooltip-Zeilen fest, die Muster für den deutschen Text sind eine Annahme.

## Überblick pro Stufe und Gestalt

| Klasse | Stufe | Gestalt | Kämpfe | Ø Dauer | Schaden pro s (Messer) | Heilung | erlitten pro s | Krit am Spieler | vermieden | Krit am Ziel (allein) | Tode |
|---|---|---|---|---|---|---|---|---|---|---|---|
| – | | | 0 | | | | | | | | |

## Zauber pro Gestalt (Anzahl, pro Minute, Anteil am Schaden laut Schadensmesser)

Noch keine Kämpfe mit Zaubern.

## Eröffnung und Abstände zwischen Zaubern

Die ersten drei Zauber jedes Kampfes (negative Zeit: vor dem Kampfbeginn) und der mittlere Abstand zwischen zwei Zaubern.

| Klasse | Gestalt | häufigste Eröffnungen | Kämpfe | mittlerer Abstand |
|---|---|---|---|---|
| – | | | 0 | |

## Erlittene Treffer pro Gegner (Kämpfe gegen genau einen Gegner)

| Kreatur | Gestalt | Kämpfe | Treffer | Ø Schaden pro Treffer | Krit |
|---|---|---|---|---|---|
| – | | 0 | | | |

## Werte (neuester Stand pro Stufe und Gestalt)

| Klasse | Stufe | Gestalt | Stä | Bew | Aus | Int | Wil | AP | Krit | Zauberkrit | Ausweichen | Rüstung | Leben | Mana | Umrechnung |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| – | | | | | | | | | | | | | | | |

## Fischglas (+8 % Grundwerte) gegen Lagerstuhl (+2 % Krit)

Mit dem neuesten Stand der Werte. «Spielwerte»: was die 8 % laut Umrechnung des Clients bringen. «RXP»: beide Buffs mit RXPs Gewichten in Punkten (Lagerstuhl = 2 × Gewicht für 1 % Krit, Nahkampf und Zauber zusammen, weil Forever beide Krit-Werte zusammenlegt; Fischglas = 8 % der gewichteten Grundwerte). Pro Spieler gibt es nur einen Lager-Gegenstand pro Stunde (gemeinsame Abklingzeit, wow-professions Camping Guide).

Noch keine Werte im Testlog (ab Testlog 4.0, ausserhalb des Kampfes).

## Ausrüstung (neuester Stand pro Charakter)

## Quest-Belohnungen zur Wahl

Punkte mit RXPs Gewichten für die Stufe beim Abgeben; «gewählt» laut Testlog.

Noch keine Quest mit Belohnungen zur Wahl im Testlog (ab Testlog 4.0).

## Talente (neuester Stand pro Charakter)

Noch keine Talente im Testlog (ab Testlog 4.0).
