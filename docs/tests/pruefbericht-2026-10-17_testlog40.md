# Prüfbericht Testlog 4.0 (Kampfdaten), unabhängige Prüfung vom 17.10.2026

Geprüft war der Stand des Branches `testlog/4.0-kampf` bei Commit e679068 (vor der ersten Auslieferung ins Spiel). Am Repo hat der Prüfer nichts geändert; die Zeilennummern unten beziehen sich auf diesen Stand. Seine Hilfsskripte (lokale Variablen auf der Datei-Ebene zählen, globale Zuweisungen im Lua-5.1-Bytecode suchen) liegen nicht im Repo. Die Probe `tools/testlog_harness.py` lief vor und nach e679068 grün.

Die Befunde sind danach eingearbeitet (Abschnitt «Umsetzung» bei jedem Punkt); die Version bleibt 4.0, weil 4.0 noch nie im Spiel lief.

## Quellen

- Forever-UI 1.60.1 (Build 70450), https://github.com/Gethe/wow-ui-source/tree/forever, Commit 172a387. «UI/» steht für `Interface/AddOns/`, «Doku/» für `Interface/AddOns/Blizzard_APIDocumentationGenerated/`.
- Secret values: https://warcraft.wiki.gg/wiki/Secret_values (Retail 12.x). Verboten für Addon-Code: Vergleiche, boolesche Tests auf geheimen Booleans, Rechnen, `#`, geheime Tabellenschlüssel; jede verbotene Operation gibt «an immediate Lua error». Erlaubt: `..`, `string.format`, `type()`, geheime Werte als Tabellenwerte. `AllowedWhenUntainted`: Die Funktion nimmt geheime Werte nur ohne Taint an. Für Tabellenschlüssel im UI-Code bestätigt: UI/Blizzard_ScriptErrorsFrame/Blizzard_ScriptErrorsFrame.lua Z. 100–104.
- Retail-Addons, die die Kampflog-Datei selbst einschalten: AutoInstanceLog (12.0.1–12.1.5), https://www.curseforge.com/wow/addons/autoinstancelog/files/7540894 («Automatically enables combat logging when entering dungeons or raids»); Combat Log Reminder (12.0.7–12.1.5), https://www.curseforge.com/wow/addons/combat-log-reminder.

## Kurzfassung

- Klasse A (bricht etwas, Fehler im Spiel): kein belegter Befund. Das Testlog ruft keine geschützte Funktion auf; einzig `LoggingCombat` ist offen (C1).
- Klasse B (falsche oder fehlende Daten): sechs Befunde, alle eingearbeitet.
- Klasse C (Kleinigkeiten): zwölf Punkte, zehn eingearbeitet; C3 lässt sich nicht beheben, C11 ist nur eine Schätzung.

## B – falsche oder fehlende Daten

### B1 Talente fehlen in Forever vermutlich ganz
- Ort: `K.talente` Z. 2956–2960. Liefert `C_ClassTalents.GetActiveConfigID()` nil, bricht die Funktion still ab (keine Zeile TALENTE, kein FEHLER).
- Beleg: Blizzard rechnet in Forever mit diesem nil: UI/Blizzard_PlayerSpells/ClassTalents/Blizzard_ClassTalentsFrame.lua Z. 893–899 fängt es ab, Z. 904 «Overridden in flavors that have a config to fall back on when there is no active config»; der Camelot-Ersatz (UI/Blizzard_PlayerSpells/Camelot/ClassTalents/Blizzard_ClassTalentsFrame.lua Z. 131–133) nimmt `C_SpecializationInfo.GetCombatConfigIDForSpecGroup(…)` (Doku/SpecializationInfoDocumentation.lua Z. 41–55 und 90–103).
- Wahrscheinlichkeit: mittel bis hoch, ungeprüft (die Probe lieferte immer 77).
- Umsetzung: `K.talentConfig()`: zuerst `GetActiveConfigID`, sonst `GetCombatConfigIDForSpecGroup(GetActiveSpecGroup())`; gibt es keine Konfiguration, einmal pro Sitzung die Zeile «TALENTE | nicht lesbar: keine Talent-Konfiguration». Probe: Ersatzweg (Laufzeit L14) und «nicht lesbar» mit geheimer Konfiguration (L13).

### B2 Charakterstufe im Gegenstands-Schlüssel
- Ort: `K.stats` Z. 2873, `K.ausruestung` Z. 2932 und 2935. Der Schlüssel war der ganze `item:…`-Teil des Links; Feld 9 ist `linkLevel` (Format: UI/Blizzard_PTRFeedback/Blizzard_Reports.lua Z. 391). Steht dort die aktuelle Stufe, meldet AUSRÜSTUNG nach jedem Stufenaufstieg alle Plätze als «X statt X», und `itemWerte`/`itemTexte` bekommen je Teil und Stufe einen neuen Eintrag.
- Wahrscheinlichkeit: hoch, falls `GetInventoryItemLink` die Stufe einträgt (in Forever ungeprüft).
- Umsetzung: `K.itemKey()` leert Feld 9 und 10 (`linkLevel`, `specializationID`) und lässt leere Felder am Ende weg («item:6070», mit Verzauberung «item:6070:15»). Probe: Links mit Stufe 13 statt 12 geben keine neue Zeile und keinen neuen Eintrag; eine Verzauberung ist ein Wechsel.

### B3 Belohnungen mit noch nicht geladenen Gegenständen
- Ort: `K.belohnung` Z. 3005–3023, `K.stats` Z. 2876. Gelesen wurde sofort bei QUEST_COMPLETE; fehlt der Gegenstand im Cache, kamen «?» oder leere Werte, und `K.stats` speicherte den leeren Stand dauerhaft.
- Beleg: Das Forever-UI baut die Belohnungen bei QUEST_ITEM_UPDATE neu auf (UI/Blizzard_UIPanels_Game/Mainline/QuestFrame.lua Z. 15 und 75–84; Ereignis in Doku/QuestOfferDocumentation.lua Z. 91).
- Wahrscheinlichkeit: gering bis mittel.
- Umsetzung: QUEST_ITEM_UPDATE liest neu, solange das Belohnungsfenster offen ist; `K.stats` speichert nur, wenn `C_Item.IsItemDataCachedByID` die Daten kennt, und ersetzt einen leeren Stand später. Probe: ein Teil ohne Daten, eines ohne Link, beide nach QUEST_ITEM_UPDATE vollständig.

### B4 Zuordnung der Sitzung des Schadensmessers
- Ort: `K.dm` Z. 2624–2669. Drei Fälle: (a) `K.dmSeen` galt nur bis `/reload`; ein «Kampf» ohne eigene Sitzung danach (z. B. Fallschaden) bekäme die Werte des letzten Kampfes vor dem Neuladen nochmals. (b) Nach «Zurücksetzen» (DAMAGE_METER_RESET, Doku/DamageMeterDocumentation.lua Z. 152) beginnen die Nummern vielleicht neu (ungeprüft); neue Sitzungen gälten dann als gelesen. (c) Fasst Blizzard Kämpfe zusammen oder läuft die Sitzung in der Gruppe weiter (ungeprüft), liest das Testlog einen Teilstand, und der nächste Kampf bekommt «keine neue Sitzung».
- Umsetzung: DAMAGE_METER_COMBAT_SESSION_UPDATED (Art, Sitzung; ohne Secret-Kennzeichen, Doku Z. 132–142; laut UI/Blizzard_DamageMeter/DamageMeterSessionWindow.lua Z. 197–199 je eine Meldung für die Gesamtsitzung mit 0 und eine für die laufende) registriert: Das Testlog liest die im Kampf gemeldete Sitzung, sonst die neueste. Der gelesene Stand der 10 neuesten Sitzungen bleibt in `KombiTestlogDB.dmStand`; eine schon gelesene Sitzung gibt nur den Zuwachs (`dm.teil`, in der Zeile «Zuwachs einer schon gelesenen Sitzung»). Neu angefangen wird bei DAMAGE_METER_RESET, beim ersten Einloggen (`PLAYER_ENTERING_WORLD` mit `isInitialLogin`, Doku/SystemDocumentation.lua Z. 134–142) und bei einer kürzeren oder kleineren Sitzung unter derselben Nummer. Dauer der Sitzung (`durationSeconds`, Doku Z. 10–19 und 167) und Herkunft (`quelle`: «gemeldet» oder «neueste») stehen im Kampf; `tools/kampf_aus_testlog.py` schreibt sie in `messer_sitzung`, `messer_dauer_s`, `messer_zuwachs`. Probe: gemeldete statt neuester Sitzung, Zuwachs, Zurücksetzen, kürzere Sitzung.

### B5 XP des Kampfes zu spät festgehalten
- Ort: `K.finish` Z. 2672. `f.xp` wurde erst beim Schreiben berechnet, bei der Wiederholung 6,5 s nach dem Kampf; XP eines Folgekampfs (doppelt gezählt) oder einer Abgabe in diesen Sekunden kam dazu.
- Umsetzung: XP zählt bis zum Beginn des nächsten Kampfes oder bis zum ersten Lesen des Schadensmessers (1,5 s), was früher kommt; so zählt die XP des letzten Gegners noch mit, wenn sie kurz nach dem Kampfende kommt (Reihenfolge ungeprüft). Probe mit wartenden Timern: zwei Kämpfe mit 50 und 70 XP.

### B6 Kämpfe rund um `/reload` und Ausloggen
- Ort: `K.stop` Z. 2589; nach `/reload` `K.tick` Z. 3122 und die Handler Z. 3579 und 3583. (a) Endete ein Kampf weniger als 1,5 s (mit Wiederholung 6,5 s) vor `/reload` oder Ausloggen, lief der Timer nicht mehr, und der Kampf fehlte. (b) `/reload` im Kampf: PLAYER_LOGOUT kommt auch bei `/reload` (ENDE und SITZUNG vom 15.10.); danach blieb `W.inCombat` false, und der weitere Kampf zerfiel in Stücke von je 6 s.
- Umsetzung: Beendete Kämpfe warten in einer Liste (`K.wartend`); PLAYER_LOGOUT schreibt sie ohne Schadensmesser («vor dem Ausloggen/Neuladen nicht gelesen»), danach den offenen Kampf («Ende Ausloggen/Neuladen»); ein später doch laufender Timer schreibt nichts doppelt. Beim Einloggen setzt das Testlog im Kampf (`InCombatLockdown`) `W.inCombat` und beginnt einen Kampf mit «Beginn nach dem Laden (im Kampf)». Endet ein Kampf ohne Kampfende des Clients (Fallschaden), zählt die Dauer bis zum letzten Ereignis, nicht bis zum Ende der Pause von 6 s. Probe: Ausloggen mit wartendem und offenem Kampf; `/reload` im Kampf (L14).

## C – Kleinigkeiten

| Nr. | Befund | Umsetzung |
|---|---|---|
| C1 | `LoggingCombat` ist für Addons nicht als gesperrt belegt (fehlt in der Doku, Blizzard ruft es im Slash-Befehl, UI/Blizzard_ChatFrameBase/Shared/SlashCommands.lua Z. 856–865; Retail-Addons schalten selbst ein). Für die Abfrage gibt es `C_ChatInfo.IsLoggingCombat()` (Doku/ChatInfoDocumentation.lua Z. 372–380, mit «advanced»). Seit e679068 entstand nach jedem `/tl geheim` beim nächsten Einloggen eine überflüssige Zeile GEHEIM (Vergleichstext mit «true/false» gegen «vorhanden»). | Zustand aus `IsLoggingCombat` («an», «aus», «(erweitert)»), ohne die Funktion nur von Hand über `LoggingCombat`; verglichen wird der Text ohne die Kampflog-Datei. |
| C2 | `W.yes("IsInGroup")` in `K.start` ohne `isSecret`. | `K.ja("IsInGroup")`. |
| C3 | `UnitHealth` trägt `SecretReturns = true` ohne Bedingung (Doku/UnitDocumentation.lua Z. 1526–1528); greifen die Secret-Regeln, steht in `lp0`/`lp1` «?». | Nicht behebbar; in Best Practice §4 vermerkt. |
| C4 | `K.rund(mr[2], 2)` ungeprüft in `string.format("%s:%s")`. | `tostring`. |
| C5 | Baum-Name nur aus `groupIDs[1]`; Blizzard sucht über alle Gruppen (Camelot-Datei Z. 164–175). | Erste Gruppe mit Namen, wie `GetTraitTreeName`. |
| C6 | `swingType` (0 Waffenhand, 1 Schildhand, 2 Distanz; Doku/SwingTimerDocumentation.lua) wurde nicht ausgewertet. | Nur die Waffenhand zählt als «Schläge»; die anderen getrennt (`swingAndere`). |
| C7 | KAMPF beim Ausloggen nahm `context()`, ENDE bewusst `lastContext`. | `lastContext` auch für KAMPF beim Ausloggen. |
| C8 | `K.dm` lief ohne eigenes `pcall`; ein Fehler kostete den ganzen Kampf. | Eigenes `pcall`; der Kampf wird mit dem Grund geschrieben. |
| C9 | `K.dirty` behielt nur den frühesten Anlass («Stufe N» ging neben «Werte geändert» verloren). | Frühester Termin, die Anlässe zusammen. |
| C10 | PLAYER_LEVEL_UP liefert Zuwachs an Leben, Kraft, Talentpunkten und Grundwerten (Doku/UnitDocumentation.lua ab Z. 3832). | Zeile STUFE mit «Zuwachs …», `chars[…].stufen` (höchstens 60), `data/spiel/stufen.csv`. |
| C11 | Speicher (geschätzt): KAMPF etwa 1–2 KB je Eintrag, bis 400 je Charakter; `werteLog` mit der Kennung `sig` doppelt so gross; `zauberNamen` ohne Obergrenze; KAMPF teilt sich die 20 000 Zeilen von `db.log`. | Kennung getrennt (`werteSig`), nicht mehr in `werteLog`; `zauberNamen` bleibt ohne Grenze (wenige Zauber pro Klasse). |
| C12 | `/tl kampf` zeigte «noch nicht gelesen», wenn Talente gelesen, aber keine Punkte verteilt waren. | «keine Punkte verteilt». |

## Geprüft, ohne Befund

- Geheime Werte: Alle Rückgaben in K laufen über `K.multi`, `W.val`/`num`, `K.ja`, `K.rund` oder `isSecret`, bevor verglichen, gerechnet oder als Schlüssel benutzt wird (einzige Ausnahme war C2). UNIT_SPELLCAST_SUCCEEDED prüft die Zauber-ID, UNIT_COMBAT alle fünf Werte. Der Schadensmesser wird nur ausserhalb des Kampfes gelesen; `isLocalPlayer` ist NeverSecret, `sourceGUID` (ConditionalSecret) wird geprüft (Doku Z. 199, 206).
- Taint: `hooksecurefunc` auf `GetQuestReward` ist ein sicherer Nach-Haken; Blizzard ruft die globale Funktion (QuestFrame.lua Z. 168, GameDialogDefs.lua Z. 524). C_TooltipInfo, C_DamageMeter, UnitIsUnit und UnitCanAttack sind Abfragen ohne `HasRestrictions`; «target» mit «player» ist als Paar erlaubt (SecretPredicatesDocumentation.lua Z. 10–14). K schreibt in keine Blizzard-Tabelle.
- Signaturen gegen Doku und UI-Code: UnitStat, UnitAttackPower, UnitDamage, UnitAttackSpeed, UnitArmor (zweiter Wert = wirksame Rüstung), UnitDefenseSkill, GetCritChance() und GetSpellCritChance() ohne Argument, GetSpellBonusDamage (Schule 4 Natur, 7 Arkan; Camelot/PaperDollFrameStats.lua Z. 396–401), GetCritChanceFromStat, GetSpellCritChanceFromStat und GetDodgeChanceFromAttribute als Anteil (×100 richtig, Z. 277, 316–320), GetAttackPowerForStat, UnitHPPerStamina, GetManaRegenFromSpirit/GetHealthRegenFromSpirit, GetShapeshiftFormInfo (4. Wert = Zauber-ID, StanceBar.lua Z. 70), C_DamageMeter (`sourceCreatureID` darf nil sein, Doku Z. 67–68), C_Traits, GetNumQuestChoices, GetQuestItemLink("choice", i), GetQuestID (Mainline/QuestInfo.lua Z. 525–526, 647), Tooltip-Zeilen `lines[i].leftText` (TooltipUtil.lua Z. 55), UNIT_COMBAT ohne Secret-Kennzeichen (UnitDocumentation.lua Z. 4169–4180), ADDON_RESTRICTION_STATE_CHANGED mit Arten 0–5, Ausrüstungsplätze 1–19 wie `INVSLOT_*`. Alle neu registrierten Ereignisse gibt es in Forever.
- Logik: K.tick wiederholt keinen Fehler alle 2 s; die Wiederholung nach 5 s kommt nur einmal; die Obergrenzen sind umgesetzt.
- Lua 5.1: 193 von 200 lokalen Variablen auf der Datei-Ebene (7 frei); keine Funktion über 60 Upvalues (die Datei kompiliert); globale Zuweisungen im Bytecode nur an `KombiTestlogDB`, `SLASH_KOMBITESTLOG1`, `SLASH_KOMBITESTLOG2`. Nach der Umsetzung nachgeprüft: unverändert.

## Hinweis (ungeprüft)

Laut Doku ist `UnitGUID` für Einheiten, die kein Spieler steuert, geheim (`SecretWhenUnitIdentityRestricted`, SecretPredicatesDocumentation.lua Z. 125–128). Trotzdem lieferte das Testlog am 17.10. Kreatur-IDs über `UnitGUID("target")` (T23). Das spricht dafür, dass die Secret-Regeln in der Beta derzeit nicht greifen, also `C_Secrets.HasSecretRestrictions()` false meldet («If false, all APIs … will never do so», SecretPredicateAPIDocumentation.lua Z. 93–100). Die Zeile GEHEIM (T38) zeigt, ob das stimmt.

## Was die Probe nicht sehen kann

Fehler beim Vergleichen geheimer Werte (ihr `issecretvalue` löst keine aus), echte Links mit wechselnder Stufe, ein nil aus `GetActiveConfigID` im echten Client, noch nicht geladene Gegenstände im echten Client und ob Blizzards Schadensmesser Kämpfe zusammenfasst. Die Probe bildet diese Fälle nach (Laufzeiten L12–L14 in `tools/testlog_harness.py`); ob der Client sich so verhält, zeigen T38–T46.
