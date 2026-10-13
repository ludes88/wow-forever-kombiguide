-- RXPGuides_Kombi: Test-Guide für RestedXP (WoW Forever, Horde)
-- Höhlen des Wehklagens: alle Vorquests. Stand 13.10.2026
--
-- Schritte, Quest-IDs, NPCs und Koordinaten stammen aus den RestedXP-Gratis-Guides
-- für Forever (github.com/RestedXP/RXPGuides, Stand 13.10.2026):
--   Guides/forever/Horde-1-12_Mulgore.lua    (Quest 886, nur Tauren-Druiden)
--   Guides/forever/Horde-12-22_Barrens.lua   (alle anderen Quests)
-- Das Original steht unter der Lizenz CC BY-NC-SA 4.0, diese Bearbeitung ebenso.

if not (RXPGuides and RXPGuides.RegisterGuide) then return end

RXPGuides.RegisterGuide([[
#forever
<< Horde
#version 1
#group Kombiguide Tests
#name WC Vorquests
#displayname Höhlen des Wehklagens: Vorquests (Test)

step << Tauren Druid
    .goto 1456/1,-298.50,-1049.01
    >>Sprich mit |cRXP_FRIENDLY_Hamuul|r. Nur Tauren-Druiden: Anfang der Kette zu Nara
    .accept 886
    .target Arch Druid Hamuul Runetotem
step
    #completewith TongaStart
    .goto 1456/1,26.1,-1196.66
    .fly Crossroads >>Flieg zu den Crossroads im Brachland. Ohne Flugpunkt folgst du dem Pfeil zu Fuss
    .target Tal
    .zoneskip The Barrens
step << Tauren Druid
    .goto 1413/1,-2672.76,-544.77
    >>Sprich mit |cRXP_FRIENDLY_Tonga|r
    .turnin 886
    .target Tonga Runetotem
    .isOnQuest 886
step
    #label TongaStart
    .goto 1413/1,-2672.76,-544.77
    >>Sprich mit |cRXP_FRIENDLY_Tonga|r
    .accept 870
    .target Tonga Runetotem
step
    .goto 1413/1,-2589.67,-424.51
    >>Sprich mit |cRXP_FRIENDLY_Helbrim|r
    .accept 848
    .target Apothecary Helbrim
step
    #completewith Teiche
    >>Sammle unterwegs die |cRXP_LOOT_Pilze|r rund um die Teiche im Norden
    .complete 848,1
step
    #label Teiche
    .goto 1413/1,-1943.16,89.64
    >>Tauch zur blubbernden Spalte am Grund des Teichs
    .complete 870,1
step
    .goto 1413/1,-2672.76,-544.77
    >>Zurück zu |cRXP_FRIENDLY_Tonga|r
    .turnin 870
    .accept 877
    .target Tonga Runetotem
step
    .goto 1413/1,-2589.67,-424.51
    >>Sprich mit |cRXP_FRIENDLY_Helbrim|r
    .turnin 848
    .target Apothecary Helbrim
    .isQuestComplete 848
step
    #completewith Mebok1
    .goto 1413/1,-2595.75,-437.35
    .fly Ratchet >>Flieg nach Ratchet. Ohne Flugpunkt folgst du dem Pfeil nach Osten
    .target Devrak
step
    #label Mebok1
    .goto 1413/1,-3697.24,-929.20
    >>Sprich mit |cRXP_FRIENDLY_Mebok|r
    .accept 865
    .target Mebok Mizzyrix
step
    .goto 1413/1,-3770.20,-928.53
    >>Sprich mit dem Kranführer |cRXP_FRIENDLY_Moppelfuzz|r
    .accept 959
    .target Crane Operator Bigglefuzz
step
    #completewith Oase1
    >>Töte unterwegs |cRXP_ENEMY_Raptoren|r und sammle ihre Hörner
    .complete 865,1
    .mob Sunscale Scytheclaw
step
    #label Oase1
    .goto 1413/1,-3012.23,-1275.80
    >>Tauch zur blubbernden Spalte am Grund der Oase
    .complete 877,1
step
    #loop
    .goto 1413/1,-3023.38,-1234.58,0
    .goto 1413/1,-3023.38,-1234.58,30,0
    .goto 1413/1,-3000.07,-1208.23,30,0
    .goto 1413/1,-2959.54,-1196.75,30,0
    .goto 1413/1,-2953.46,-1241.34,30,0
    .goto 1413/1,-2977.78,-1304.17,30,0
    .goto 1413/1,-3029.46,-1324.44,30,0
    .goto 1413/1,-3066.95,-1311.61,30,0
    .goto 1413/1,-3059.86,-1264.31,30,0
    >>Falls dir noch Pilze fehlen: Sammle sie rund um die Oase
    .complete 848,1
    .isOnQuest 848
step
    .goto 1413/1,-2672.76,-544.77
    >>Zurück zu |cRXP_FRIENDLY_Tonga|r
    .turnin 877
    .accept 880
    .target Tonga Runetotem
step
    .goto 1413/1,-2589.67,-424.51
    >>Sprich mit |cRXP_FRIENDLY_Helbrim|r
    .turnin 848
    .target Apothecary Helbrim
    .isQuestComplete 848
step
    #loop
    .goto 1413/1,-3010.20,-1319.04,0
    .goto 1413/1,-3010.20,-1319.04,40,0
    .goto 1413/1,-2959.54,-1292.69,40,0
    .goto 1413/1,-2953.46,-1239.31,40,0
    .goto 1413/1,-2998.04,-1192.02,40,0
    .goto 1413/1,-3050.74,-1225.13,40,0
    .goto 1413/1,-3066.95,-1260.93,40,0
    .goto 1413/1,-3052.76,-1319.710,40,0
    >>Töte |cRXP_ENEMY_Schnappkiefer|r in und um die Oase und sammle ihre Panzer
    .complete 880,1
    .mob Oasis Snapjaw
step
    #loop
    .goto 1413/1,-3183.48,-2015.61,0
    .goto 1413/1,-2646.42,-1529.16,0
    .goto 1413/1,-3183.48,-2015.61,90,0
    .goto 1413/1,-2646.42,-1529.16,90,0
    >>Falls dir noch Hörner fehlen: Töte weitere |cRXP_ENEMY_Raptoren|r
    .complete 865,1
    .mob Sunscale Scytheclaw
step
    .goto 1413/1,-3697.24,-929.20
    >>Zurück zu |cRXP_FRIENDLY_Mebok|r in Ratchet
    .turnin 865
    .accept 1491
    .target Mebok Mizzyrix
step
    #completewith Tonga3
    .goto 1413/1,-3770.20,-898.12
    .fly Crossroads >>Flieg zu den Crossroads
    .target Bragok
step
    #label Tonga3
    .goto 1413/1,-2672.76,-544.77
    >>Sprich mit |cRXP_FRIENDLY_Tonga|r
    .turnin 880
    .accept 1489
    .target Tonga Runetotem
step
    .goto 1413/1,-2589.67,-424.51
    >>Sprich mit |cRXP_FRIENDLY_Helbrim|r
    >>|cRXP_WARN_Zeitquest: 45 Minuten, um Zamah in Thunder Bluff zu erreichen|r
    .accept 853
    .target Apothecary Helbrim
    .isQuestTurnedIn 848
    .isQuestAvailable 853
step
    #completewith ZamahWeg
    .goto 1413/1,-2595.75,-437.35
    .fly Thunder Bluff >>Flieg sofort nach Thunder Bluff
    .target Devrak
step
    #label ZamahWeg
    #completewith next
    .goto 1456/1,222.96,-1079.42,40,0
    .goto 1456/1,219.09,-1051.44,10 >>Geh auf die Anhöhe und in die Höhle darunter
step
    .goto 1456/1,278.48,-995.29
    >>Sprich mit |cRXP_FRIENDLY_Zamah|r
    .turnin 853
    .accept 962
    .target Apothecary Zamah
    .isOnQuest 853
step
    #optional
    .goto 1456/1,278.48,-995.29
    >>Sprich mit |cRXP_FRIENDLY_Zamah|r. Die Quest gibt es auch ohne die Vorquest
    .accept 962
    .target Apothecary Zamah
step
    #completewith next
    .goto 1456/1,-212.71,-1065.010,80 >>Geh zur Anhöhe der Druiden im Osten
step
    .goto 1456/1,-303.83,-1048.66
    >>Sprich mit |cRXP_FRIENDLY_Hamuul|r
    .turnin 1489
    .accept 1490
    .target Arch Druid Hamuul Runetotem
step
    .goto 1456/1,-272.93,-1069.67
    >>Sprich mit |cRXP_FRIENDLY_Nara|r
    .turnin 1490
    .accept 914
    .target Nara Wildmane
step
    #completewith WCWeg
    .goto 1456/1,26.1,-1196.66
    .fly Crossroads >>Flieg zu den Crossroads
    .target Tal
    .zoneskip The Barrens
step
    #label WCWeg
    .goto 1413/1,-2053.62,-882.58,100 >>Reise zu den Höhlen des Wehklagens
step
    #completewith next
    .goto 1413/1,-2134.68,-764.35,0
    .goto 1413/1,-2134.68,-764.35,30,0
    .goto 1413/1,-2122.52,-734.62,20,0
    .goto 1414/1,-2061.94,-781.68,20,0
    .goto 1414/1,-2028.82,-828.29,10,0
    .goto 1414/1,-2021.46,-816.030,10 >>Lauf den Berg hoch zur versteckten Höhle über dem Eingang
    >>|cRXP_WARN_Folge dem Pfeil genau|r
step
    >>Sprich mit |cRXP_FRIENDLY_Nalpak|r und |cRXP_FRIENDLY_Ebru|r in der Höhle über dem Eingang
    .accept 1486
    .target +Nalpak
    .goto 1414/1,-2036.18,-796.40
    .accept 1487
    .target +Ebru
    .goto 1414/1,-2039.86,-801.31
step
    #completewith Portal
    >>Pflück die |cRXP_PICK_Pflanzen|r für Zamah, schon in der Höhle vor dem Dungeon
    .complete 962,1
    .isOnQuest 962
step
    #completewith Portal
    >>Töte die verwandelten Tiere und sammle ihre Häute
    .complete 1486,1
    .isOnQuest 1486
step
    #completewith Portal
    >>Töte |cRXP_ENEMY_Ektoplasmen|r und sammle ihre Essenz
    .complete 1491,1
    .isOnQuest 1491
step
    #loop
    .goto 1414/1,-2058.26,-749.79,0
    .goto 1414/1,-2003.06,-659.01,0
    .goto 1414/1,-2072.98,-698.27,0
    .goto 1414/1,-2124.50,-730.16,0
    .goto 1414/1,-2058.26,-749.79,30,0
    .goto 1414/1,-2003.06,-659.01,30,0
    .goto 1414/1,-2072.98,-698.27,30,0
    .goto 1414/1,-2124.50,-730.16,30,0
    >>Töte |cRXP_ENEMY_Zausel der Verrückte|r und nimm ihm die Flasche ab
    >>|cRXP_WARN_Er erscheint nur selten. Findest du ihn nicht, überspring den Schritt|r
    .complete 959,1
    .mob Mad Magglish
    .isOnQuest 959
step
    #label Portal
    .goto 1414/1,-2028.82,-636.93,20,0
    .goto 1414/1,-2050.90,-585.41,20,0
    .goto 1414/1,-2168.66,-607.49,30,0
    .goto 1414/1,-2216.5,-742.43,30 >>Zum Portal der Höhlen des Wehklagens. Alle Vorquests sind erledigt
]])
