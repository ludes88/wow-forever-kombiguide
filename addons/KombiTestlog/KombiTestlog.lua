-- KombiTestlog: Notizen und Testprotokoll für WoW Forever
-- Stand 15.10.2026, Version 3.6
--
--   /tl <Text>        Notiz mit Ort, Stufe, RXP-Schritt, Ziel und Berufen
--   /tl bug <Text>    Fehler festhalten
--   /tl idee <Text>   Idee festhalten
--   /tl zeigen        letzte 1000 Einträge zum Kopieren (Strg+A, Strg+C); auch /tl liste
--   /tl zeigen alle   alle Einträge
--   /tl auto          automatische Einträge an/aus
--   /tl item <Link>   Gegenstand zusätzlich mitzählen (Shift-Klick auf den Gegenstand)
--   /tl karte         Kartengrenzen der aktuellen Karte nochmals festhalten
--   /tl ah            AH-Preise jetzt lesen (läuft beim Öffnen des Auktionshauses von selbst, höchstens alle 15 Minuten)
--   /tl ah aus | an   AH-Scan beim Öffnen des Auktionshauses aus- oder einschalten
--   /tl tipp [alle]   Empfehlungen von Claude (Addon KombiDaten, erzeugt von tools/markt.py)
--   /tl status        Überblick
--   /tl leeren ja     Protokoll löschen (die AH-Scans bleiben)
--   /tl hilfe         diese Hilfe
--
-- Automatische Einträge (Version 3 neu: HERSTELLEN bis REZEPT):
--   SITZUNG, ENDE, GEBIET, KARTE, RXP, STUFE, TOD, QUEST AN, QUEST AB (mit Geld), BERUF, TASCHE
--   HERSTELLEN  Rezept, was verbraucht und was erhalten wurde, Berufspunkt ja/nein
--   ENTZAUBERN  welches Teil (Waffe/Rüstung, Qualität, Gegenstandsstufe) und was herauskam
--   SAMMELN     Kürschnern, Kräuter, Bergbau, Öffnen: Quelle (Kreatur- oder Objekt-ID) und Beute
--               («Opening - No Text» sind Quest-Gegenstände, die man aufhebt)
--   ANGELN      Fang, dazu die Würfe seit dem letzten Fang (Version 3.2)
--   BEUTE       Beute von Gegnern mit Geld (leere Lootfenster ohne Quelle: keine Zeile, Version 3.2)
--   HÄNDLER     pro Händlerbesuch: verkauft, gekauft, Einnahmen, Ausgaben, Bestand, Dauer und wodurch beendet
--   POST, AUKTIONSHAUS  ebenso für Briefkasten und Auktionshaus
--   GELD        übrige Geldänderungen: Lehrer, Flugmeister, sonst (Betrag und Bestand)
--   GELERNT     neuer Zauber (z. B. beim Lehrer)
--   REZEPT      neues Rezept
--   LEHRER      Liste des Lehrers beim Öffnen: jeder Eintrag mit Status (lernbar, gesperrt, gelernt), Lernstufe
--               (Stufe, Beruf und Fertigkeit) und Kosten; einmal pro Lehrer und Sitzung (Version 3.4)
--   AH-SCAN     alle Angebote des Auktionshauses (Version 3.5): Kopfzeile mit den Gegenständen des Plans
--               (Tiefstpreis / Median / Stück); alles Weitere in KombiTestlogDB.ahScans: alle (jeder Gegenstand
--               «ID:Tiefstpreis:Median:Menge:Angebote» in Kupfer), plan (dasselbe für die Gegenstände des Plans),
--               stufen (Preisstufen «Kupfer*Stück» der Plan-Gegenstände). Die 10 neuesten Scans behalten alle und
--               stufen, ältere nur plan; höchstens 60 Scans. Ohne Verkäufernamen.
--               Version 3.6: Preisstufen «Kupfer*Stück*davon lang*davon sehr lang» (Restlaufzeit-Band), dazu abnahme:
--               was seit dem letzten Scan von den billigsten Angeboten fehlt («ID:weg:geschätzt gekauft»)
--   REZEPTE     beim Öffnen des Berufsfensters: gelernte Rezepte mit Reagenzien, Ergebnis und Farbe; danach nur
--               Farbwechsel (Version 3.6). Daten in KombiTestlogDB.chars[Charakter].rezepte
--   INVENTAR    Taschen beim Ein- und Ausloggen, Bank beim Öffnen und Schliessen (Version 3.6); Daten in chars, kontobank
--   AH-POST     Briefe des Auktionshauses beim Öffnen des Briefkastens: verkauft, abgelaufen, gekauft (Version 3.6)
--   AH-ANGEBOT  eigenes Angebot im Auktionshaus: Menge, Preis, Dauer, Pfand (Version 3.6). Daten in KombiTestlogDB.ahPost
--
-- Version 3.6: Rezepte, Bestand (Taschen, Bank), AH-Post, eigene Angebote, Abnahme zwischen zwei AH-Scans, /tl tipp.
-- Version 3.5: AH-Preisscan beim Öffnen des Auktionshauses (höchstens alle 15 Minuten) oder mit /tl ah.
-- Version 3.4: Lehrerliste. Damit alle Einträge erscheinen, im Lehrerfenster den Filter auf alle drei Arten stellen
-- (verfügbar, nicht verfügbar, bereits bekannt); die Zeile nennt den Filter.
-- Version 3.3: Bestand in Fenster-Zeilen beim Ausloggen aus dem letzten bekannten Wert (GetMoney meldet dann 0).
-- Version 3.2: Ein Fenster (Händler, Post, Auktionshaus, Lehrer, Flugmeister, Beruf) gilt auch ohne
-- CLOSED-Ereignis als zu, wenn das Blizzard-Fenster nicht mehr sichtbar ist und keine Interaktion läuft,
-- wenn der Charakter weggeht oder das Gebiet wechselt (Testlog 13.10.: POST blieb 16 Minuten offen).
--
-- Gespeichert wird beim Ausloggen oder /reload in
-- WTF\Account\<KONTO>\SavedVariables\KombiTestlog.lua

local ADDON_NAME = ...
local VERSION = "3.6"
local MAX_ENTRIES = 20000
local PREFIX = "|cff33ff99Testlog|r "

-- Gegenstände, die von Anfang an gezählt werden (IDs belegt über AHledger und RestedXP)
local DEFAULT_ITEMS = {
    2318,  -- Light Leather
    2934,  -- Ruined Leather Scraps
    783,   -- Light Hide
    2319,  -- Medium Leather
    4232,  -- Medium Hide
    2449,  -- Earthroot
    2589,  -- Linen Cloth
    6291,  -- Raw Brilliant Smallfish
    2447,  -- Peacebloom (Classic-ID, in Forever ungeprüft)
    765,   -- Silverleaf (Classic-ID; im Spiel am 13.10. als «Silberblatt» bestätigt)
    785,   -- Mageroyal (Classic-ID, in Forever ungeprüft)
    2450,  -- Briarthorn (Classic-ID, in Forever ungeprüft)
    2453,  -- Bruiseweed (Classic-ID, in Forever ungeprüft)
    10940, -- Strange Dust
    10938, -- Lesser Magic Essence
    10939, -- Greater Magic Essence
    10978, -- Small Glimmering Shard
    11083, -- Soul Dust
}

-- Version 3.5: Gegenstände des Plans für den AH-Scan (Preisstufen statt nur Tiefstpreis und Median).
-- IDs aus den AHledger- und Wowhead-Links in data/ und docs/ (Stand 15.10.2026); dazu alles aus DEFAULT_ITEMS und /tl item.
local AH_WATCH = {
    -- Leder, Bälge und LW-Material
    2934, 2318, 783, 2319, 4232, 4234, 4235, 4304, 8170, 4231, 4233,
    4289, 2320, 2321, 4291, 14341, 4340, 2325,
    -- LW-Erzeugnisse (Light Armor Kit, Embossed Leather Gloves, Fine Leather Belt, Light Leather Pants, Dark Leather Belt,
    -- Hillman's Leather Gloves, Dark Leather Boots, Barbaric Shoulders, Guardian Gloves, Nightscape Headband und Pants,
    -- Wicked Leather Gauntlets und Headband)
    2304, 4239, 4246, 7282, 4249, 4247, 2315, 5964, 5966, 8176, 8193, 15083, 15086,
    -- VZ: Staub, Essenzen, Splitter
    10940, 11083, 11137, 11176, 16204, 10938, 10939, 10998, 11082, 11134, 11135, 11174, 11175, 16202, 16203,
    10978, 11084, 11138, 11139, 11177, 11178, 14343, 14344,
    -- VZ: Ruten, Perlen, Shadowgem, Simple Wood, Purple Lotus, Crystal Vial, Mote of Magic, Formeln, Erzeugnisse
    -- (Runed Copper Rod, Brilliant Wand, Glimmering Staff, Arcane Salvager)
    6217, 6338, 11128, 11144, 16206, 5500, 7971, 13926, 1210, 4470, 8831, 8925, 247786, 6349, 20758,
    6218, 249385, 249392, 279985,
    -- Kräuter, Samen, Phiolen (Peacebloom, Silverleaf, Earthroot, Mageroyal, Briarthorn, Swiftthistle, Bruiseweed,
    -- Kingsblood, Frilled Lichen, Commonplace und Uncommon Herb Seeds, Empty und Leaded Vial)
    2447, 765, 2449, 785, 2450, 2452, 2453, 3356, 249399, 268415, 268416, 3371, 3372,
    -- Fisch, Köder, Kochrezept (Raw Brilliant Smallfish, Raw Longjaw Mud Snapper, Raw Bristle Whisker Catfish,
    -- Deviate Fish, Firefin Snapper, Raw Sagefish, Shiny Bauble, Nightcrawlers, Recipe: Savory Deviate Delight), Linen Cloth
    6291, 6289, 6308, 6522, 6359, 21071, 6529, 6530, 6661, 2589,
}
local AH_WATCH_SET = {}
for _, id in ipairs(AH_WATCH) do AH_WATCH_SET[id] = true end

-- Zauber, an denen das Testlog Handlungen erkennt (Classic-IDs, in Forever ungeprüft; Namen als Rückfall)
local DISENCHANT_IDS = { [13262] = true }
local GATHER_IDS = {
    [8613] = true, [8617] = true, [8618] = true, [10768] = true,   -- Kürschnern
    [2366] = true, [2368] = true, [3570] = true, [11993] = true,   -- Kräutersammeln
    [2575] = true, [2576] = true, [3564] = true, [10248] = true,   -- Bergbau
}
-- string.lower ändert nur ASCII-Buchstaben: «Öffnen» bleibt gross, darum beide Schreibweisen
local GATHER_WORDS = { "kürschn", "skinn", "kräuter", "herb", "bergbau", "mining", "öffnen", "Öffnen", "opening" }
local CLASS_NAMES = { [2] = "Waffe", [4] = "Rüstung" }
local QUALITY_NAMES = { [0] = "grau", [1] = "weiss", [2] = "grün", [3] = "blau", [4] = "lila" }
-- Angeln: 7620 und 1240948 hat der Lehrer am 13.10. beigebracht (Testlog); welcher davon der Wurf ist,
-- ist ungeprüft, darum auch über den Namen
local FISHING_IDS = { [7620] = true, [1240948] = true }
local FISHING_NAMES = { ["angeln"] = true, ["fishing"] = true }
local FISHING_PAUSE = 120   -- Sekunden ohne Wurf: Zählung beginnt neu

-- Fenster (Version 3.2). Interaktionstypen und Fensternamen aus dem Forever-UI-Code 1.60.1
-- (PlayerInteractionManagerConstantsDocumentation.lua, MailFrame.xml, MerchantFrame.xml usw.)
local IT = (Enum and Enum.PlayerInteractionType) or {}
local SESSION_INFO = {
    ["HÄNDLER"] = { itype = IT.Merchant or 5, frames = { "MerchantFrame" }, words = { "gekauft", "verkauft" } },
    ["POST"] = { itype = IT.MailInfo or 17, frames = { "MailFrame" }, words = { "erhalten", "verschickt" } },
    ["AUKTIONSHAUS"] = { itype = IT.Auctioneer or 21, frames = { "AuctionHouseFrame" }, words = { "erhalten", "abgegeben" } },
}
local WINDOW_INFO = {
    trainer = { itype = IT.Trainer or 7, frames = { "ClassTrainerFrame" } },
    taxi = { itype = IT.TaxiNode or 6, frames = { "TaxiFrame", "FlightMapFrame" } },
    -- das eigene Berufsfenster bleibt beim Gehen offen: kein Abstand prüfen
    profession = { itype = IT.Professions or 59, frames = { "ProfessionsFrame" }, free = true },
}
local KIND_BY_ITYPE = {}
for kind, info in pairs(SESSION_INFO) do KIND_BY_ITYPE[info.itype] = kind end
local WINDOW_YARDS = 25      -- weiter weg ist kein Händler- oder Briefkastenfenster mehr offen (grosszügig, Reichweite ungeprüft)
local SESSION_MAX = 1800     -- Sekunden; Notbremse, falls nichts anderes greift

local db
local ready = false
local itemLast = {}
local skillLast = {}
local questTitles = {}
local rxpLast
local lastContext   -- letzter bekannter Kontext, für ENDE beim Ausloggen
local started = false

-- Version 3: Handlungen, Lootfenster, Geld
local bagLast              -- Taschenbestand: Item-ID -> Anzahl
local bagLinks = {}        -- Item-ID -> Link (zuletzt gesehen)
local bagQuality = {}      -- Item-ID -> Qualität
local pending              -- laufende Handlung (HERSTELLEN oder ENTZAUBERN)
local lastCast             -- letzter eigener Zauber { id, name, t }
local lootRecord           -- offenes Lootfenster
local quietUntil = 0       -- bis dahin keine TASCHE-Zeilen (Änderung steht schon in einer Handlung)
local moneyLast
local session              -- offenes Händler-, Post- oder Auktionshausfenster
local windows = {}         -- offene Fenster: profession, trainer, taxi (mit Zeit und Ort), quest
local fishCasts, fishLast = 0, 0   -- Würfe seit dem letzten Fang (Version 3.2)
local missingEvents = {}   -- Ereignisse, die der Client nicht kennt (Version 3.2)
local ahScan               -- laufender AH-Scan (Version 3.5)
local ahWanted             -- Auktionshaus geöffnet: Scan beim nächsten Takt prüfen (Version 3.5)
-- Version 3.6
local recipeToken = 0      -- Rezepte: nur der zuletzt geplante Lauf zählt
local recipeSeen = {}      -- Beruf -> { sig = gelernte Rezepte und Filter, farben = Rezept-ID -> Farbe } (diese Sitzung)
local bankToken = 0
local bankLast = {}        -- «Bank»/«Kontobank» -> zuletzt geschriebene Liste (keine doppelten Zeilen)
local mailToken = 0
local postQueue = {}       -- eigene Angebote, die noch auf die Bestätigung warten
local postWarnings = false -- AUCTION_HOUSE_POST_WARNING liess sich registrieren (Bestätigungsfenster erkennbar)

local function say(msg)
    DEFAULT_CHAT_FRAME:AddMessage(PREFIX .. msg)
end

local function isSecret(v)
    return issecretvalue and issecretvalue(v)
end

local function now()
    return GetTime and GetTime() or 0
end

local function coords()
    if not (C_Map and C_Map.GetBestMapForUnit) then return "-" end
    local mapID = C_Map.GetBestMapForUnit("player")
    if not mapID then return "-" end
    local pos = C_Map.GetPlayerMapPosition(mapID, "player")
    if not pos then return tostring(mapID) end
    local x, y = pos:GetXY()
    if not x or not y then return tostring(mapID) end
    return string.format("%d %.1f,%.1f", mapID, x * 100, y * 100)
end

local function zoneText()
    local zone = GetZoneText() or "?"
    local sub = GetSubZoneText() or ""
    if sub ~= "" and sub ~= zone then
        return zone .. " > " .. sub
    end
    return zone
end

local function rxpText()
    local d = rawget(_G, "RXPCData")
    if type(d) ~= "table" then return "RXP -" end
    return string.format("RXP %s #%s", tostring(d.currentGuideName or "?"), tostring(d.currentStep or "?"))
end

local function context()
    local level = UnitLevel("player") or 0
    local xp, xpMax = UnitXP("player") or 0, UnitXPMax("player") or 0
    local pct = 0
    if xpMax > 0 then pct = math.floor(xp * 100 / xpMax) end
    return string.format("L%d %d%% | %s | %s | %s", level, pct, zoneText(), coords(), rxpText())
end

local function add(kind, text, withContext, ctx)
    if not db then return end
    local line = date("%d.%m. %H:%M:%S") .. " | " .. kind
    if withContext ~= false then
        line = line .. " | " .. (ctx or context())
    end
    if text and text ~= "" then
        line = line .. " | " .. text
    end
    table.insert(db.log, line)
    if #db.log > MAX_ENTRIES then
        table.remove(db.log, 1)
    end
end

-- Geld in Gold, Silber, Kupfer
local function money(c, signed)
    if type(c) ~= "number" then return "?" end
    local sign = ""
    if signed then sign = (c < 0) and "-" or "+" end
    c = math.abs(c)
    local g, s, k = math.floor(c / 10000), math.floor(c / 100) % 100, c % 100
    local parts = {}
    if g > 0 then table.insert(parts, g .. "g") end
    if s > 0 then table.insert(parts, s .. "s") end
    if k > 0 or #parts == 0 then table.insert(parts, k .. "c") end
    return sign .. table.concat(parts, " ")
end

local function getMoney()
    if not GetMoney then return nil end
    local m = GetMoney()
    if isSecret(m) then return nil end
    return m
end

-- Berufe: alle Fertigkeiten, die man verlernen kann, dazu Linien mit Berufs-Maximum.
-- Sprachen zählen nicht (Überschrift «Sprachen»/«Languages» oder Name mit Doppelpunkt, nicht verlernbar).
local LANGUAGE_HEADERS = { ["Languages"] = true, ["Sprachen"] = true }

local function isLanguage(header, name, abandon)
    if type(header) == "string" then
        if LANGUAGE_HEADERS[header] or header == rawget(_G, "LANGUAGES_LABEL") then return true end
    end
    return (not abandon) and type(name) == "string" and name:find(":", 1, true) ~= nil
end

local function readSkills()
    local out = {}
    local level = UnitLevel("player") or 0
    local header
    local num = 0
    if C_SkillInfo and C_SkillInfo.GetNumSkillLines then
        num = C_SkillInfo.GetNumSkillLines() or 0
    elseif GetNumSkillLines then
        num = GetNumSkillLines() or 0
    end
    for i = 1, num do
        local name, isHeader, rank, maxRank, abandon
        if C_SkillInfo and C_SkillInfo.GetSkillLineInfo then
            local t, h, _, r, _, _, m, a = C_SkillInfo.GetSkillLineInfo(i)
            if type(t) == "table" then
                name, isHeader, rank, maxRank, abandon = t.name, t.isHeader, t.rank, t.maxRank, t.isAbandonable
            else
                name, isHeader, rank, maxRank, abandon = t, h, r, m, a
            end
        elseif GetSkillLineInfo then
            local n, h, _, r, _, _, m, a = GetSkillLineInfo(i)
            name, isHeader, rank, maxRank, abandon = n, h, r, m, a
        end
        if name and isHeader and not isSecret(name) then header = name end
        if name and not isHeader and not isSecret(name) and not isLanguage(header, name, abandon) then
            local profMax = (maxRank == 75 or maxRank == 150 or maxRank == 225 or maxRank == 300)
                and maxRank ~= level * 5
            if abandon or profMax then
                out[name] = { rank or 0, maxRank or 0 }
            end
        end
    end
    return out
end

local function skillSummary()
    local parts = {}
    for name, v in pairs(readSkills()) do
        table.insert(parts, string.format("%s %d/%d", name, v[1], v[2]))
    end
    table.sort(parts)
    return table.concat(parts, ", ")
end

local function itemCount(id)
    if C_Item and C_Item.GetItemCount then return C_Item.GetItemCount(id) or 0 end
    if GetItemCount then return GetItemCount(id) or 0 end
    return 0
end

local function itemName(id)
    local n = C_Item and C_Item.GetItemNameByID and C_Item.GetItemNameByID(id)
    if n and not isSecret(n) then return n end
    return "Item " .. id
end

local function linkName(link)
    if type(link) ~= "string" or isSecret(link) then return nil end
    return link:match("%[(.-)%]")
end

local function spellName(id)
    if isSecret(id) then return nil end
    local n
    if C_Spell and C_Spell.GetSpellName then
        local ok, v = pcall(C_Spell.GetSpellName, id)
        if ok then n = v end
    elseif GetSpellInfo then
        local ok, v = pcall(GetSpellInfo, id)
        if ok then n = v end
    end
    if n and not isSecret(n) then return n end
    return nil
end

local function num(v)
    if type(v) == "number" and not isSecret(v) then return v end
    return nil
end

-- Version 3.6: Charakter als «Name-Realm» (nur in der SavedVariables-Datei, nie im Repo)
local function charKey()
    local okN, n = pcall(UnitName, "player")
    if not okN or type(n) ~= "string" or isSecret(n) then n = "?" end
    local r = GetRealmName and GetRealmName()
    if type(r) ~= "string" or isSecret(r) then r = "?" end
    return n .. "-" .. r
end

local function charDB()
    db.chars = db.chars or {}
    local k = charKey()
    if not db.chars[k] then db.chars[k] = {} end
    return db.chars[k]
end

-- Version 3.6: Gegenstands-Infos für tools/markt.py: Name (deutsch), Qualität, Händlerpreis, Klasse, Unterklasse,
-- Gegenstandsstufe, Bindung (C_Item.GetItemInfo, 1., 3., 11.–13., 4. und 14. Wert laut ItemDocumentation.lua,
-- Forever-UI 1.60.1). Gebundene Teile (Bindung 1) gehen nicht ins Auktionshaus. Abgefragt über die Item-ID, nicht
-- über den Link: sonst stünde ein Name mit Zufallsendung («… des Bären») unter der ID des Grundgegenstands.
local function remember(id)
    if not db or type(id) ~= "number" or isSecret(id) then return end
    db.info = db.info or {}
    local e = db.info[id]
    if e and e.n then return end
    if not (C_Item and C_Item.GetItemInfo) then return end
    local ok, name, _, q, ilvl, _, _, _, _, _, _, sell, class, sub, bind = pcall(C_Item.GetItemInfo, id)
    if not ok or type(name) ~= "string" or isSecret(name) then return end
    db.info[id] = { n = name, q = num(q), s = num(sell), k = num(class), u = num(sub), l = num(ilvl), b = num(bind) }
end

local function idLabel(id)
    remember(id)
    local e = db and db.info and db.info[id]
    local n = (e and e.n) or (C_Item and C_Item.GetItemNameByID and C_Item.GetItemNameByID(id))
    if type(n) == "string" and not isSecret(n) then return n .. " (" .. id .. ")" end
    return "Item " .. id
end

-- Version 3.6: Gegenstände mit Preisstufen und Abnahme im AH-Scan: Plan (AH_WATCH), /tl item und alles, was in den
-- gelernten Rezepten vorkommt (Reagenzien und Ergebnis, KombiTestlogDB.beobachten)
local function watched(id)
    if AH_WATCH_SET[id] then return true end
    if not db then return false end
    if db.items[id] then return true end
    return db.beobachten ~= nil and db.beobachten[id] == true
end

-- Taschen ganz lesen (Version 3): Grundlage, um Änderungen einer Handlung zuzuordnen
local bagBound = {}        -- Version 3.6: gebundene Stücke in den Taschen (Item-ID -> Anzahl), beim Bestand ausgenommen

local function scanBags()
    if not (C_Container and C_Container.GetContainerNumSlots and C_Container.GetContainerItemInfo) then return nil end
    local counts, bound = {}, {}
    local last = (NUM_BAG_SLOTS or 4) + (NUM_REAGENTBAG_SLOTS or 0)
    for bag = 0, last do
        local n = C_Container.GetContainerNumSlots(bag) or 0
        if isSecret(n) then n = 0 end
        for slot = 1, n do
            local info = C_Container.GetContainerItemInfo(bag, slot)
            if type(info) == "table" and info.itemID and not isSecret(info.itemID) then
                local id = info.itemID
                local c = info.stackCount
                if not c or isSecret(c) then c = 1 end
                counts[id] = (counts[id] or 0) + c
                if not isSecret(info.isBound) and info.isBound == true then bound[id] = (bound[id] or 0) + c end   -- isBound: ContainerItemInfo
                if info.hyperlink and not isSecret(info.hyperlink) then bagLinks[id] = info.hyperlink end
                if info.quality and not isSecret(info.quality) then bagQuality[id] = info.quality end
                remember(id)
            end
        end
    end
    bagBound = bound
    return counts
end

local function bagDiff()
    local cur = scanBags()
    if not cur then return nil end
    local diff = {}
    if bagLast then
        for id, c in pairs(cur) do
            local d = c - (bagLast[id] or 0)
            if d ~= 0 then diff[id] = d end
        end
        for id, c in pairs(bagLast) do
            if not cur[id] then diff[id] = -c end
        end
    end
    bagLast = cur
    return diff
end

local function itemLabel(id)
    return linkName(bagLinks[id]) or itemName(id)
end

-- Teil beim Entzaubern: Name, Art, Qualität, Gegenstandsstufe, benötigte Stufe
local function itemDetail(id, count)
    local link = bagLinks[id]
    local info = {}
    if C_Item and C_Item.GetItemInfo then
        local ok, _, _, quality, ilvl, minLevel, _, _, _, _, _, _, classID = pcall(C_Item.GetItemInfo, link or id)
        if ok then
            if classID and not isSecret(classID) and CLASS_NAMES[classID] then table.insert(info, CLASS_NAMES[classID]) end
            if (not quality or isSecret(quality)) then quality = bagQuality[id] end
            if quality and QUALITY_NAMES[quality] then table.insert(info, QUALITY_NAMES[quality]) end
            if ilvl and not isSecret(ilvl) then table.insert(info, "Gegenstandsstufe " .. ilvl) end
            if minLevel and not isSecret(minLevel) and minLevel > 0 then table.insert(info, "ab Stufe " .. minLevel) end
        end
    end
    local s = ((count and count > 1) and (count .. "x ") or "") .. itemLabel(id) .. " (" .. id .. ")"
    if #info > 0 then s = s .. " [" .. table.concat(info, ", ") .. "]" end
    return s
end

local rxpKey

local function snapshot()
    for id in pairs(db.items) do
        itemLast[id] = itemCount(id)
    end
    skillLast = readSkills()
    rxpLast = rxpKey()
    bagLast = scanBags()
    moneyLast = getMoney()
    ready = true
end

local function checkItems()
    if not ready then return end
    local changes = {}
    local ids = {}
    for id in pairs(db.items) do table.insert(ids, id) end
    table.sort(ids)
    for _, id in ipairs(ids) do
        local cur = itemCount(id)
        local before = itemLast[id] or cur
        if cur ~= before then
            table.insert(changes, string.format("%s %+d (%d)", itemName(id), cur - before, cur))
        end
        itemLast[id] = cur
    end
    -- Steht die Änderung schon in einer Handlung oder Beute-Zeile, keine zweite Zeile
    local covered = pending or lootRecord or session or now() < quietUntil
    if #changes > 0 and db.auto and not covered then
        add("TASCHE", table.concat(changes, "; "))
    end
end

local function checkSkills()
    if not ready then return end
    local cur = readSkills()
    for name, v in pairs(cur) do
        local before = skillLast[name]
        if not before or before[1] ~= v[1] or before[2] ~= v[2] then
            if db.auto then
                add("BERUF", string.format("%s %d/%d", name, v[1], v[2]))
            end
            if pending and before and before[1] ~= v[1] then
                local p = pending.skills[name]
                pending.skills[name] = { p and p[1] or before[1], v[1] }
            end
        end
    end
    skillLast = cur
end

function rxpKey() -- weist der oben deklarierten lokalen Variable zu
    local d = rawget(_G, "RXPCData")
    if type(d) ~= "table" then return nil end
    return tostring(d.currentGuideGroup) .. "|" .. tostring(d.currentGuideName) .. "|" .. tostring(d.currentStep)
end

local function checkRXP()
    if not db or not db.auto then return end
    local key = rxpKey()
    if key and key ~= rxpLast then
        if rxpLast ~= nil then
            add("RXP", tostring(rawget(_G, "RXPCData").currentGuideGroup or "?"))
        end
        rxpLast = key
    end
end

local function addonVersion(name)
    if C_AddOns and C_AddOns.GetAddOnMetadata then
        local ok, v = pcall(C_AddOns.GetAddOnMetadata, name, "Version")
        if ok and v then return v end
    end
    return "-"
end

local function addonLoaded(name)
    if C_AddOns and C_AddOns.IsAddOnLoaded then
        local ok, v = pcall(C_AddOns.IsAddOnLoaded, name)
        return ok and v
    end
    return false
end

local function guideAddon(name)
    if addonLoaded(name) then return addonVersion(name) end
    return "nicht geladen"
end

-- Version 3.6: Empfehlungen aus dem Addon KombiDaten (schreibt Claude mit tools/markt.py, nie aus dem Repo)
local function tipsData()
    local d = rawget(_G, "KombiDaten")
    if type(d) ~= "table" or type(d.tipps) ~= "table" then return nil end
    return d
end

local function sessionStart()
    local build = "-"
    if GetBuildInfo then
        local v, b = GetBuildInfo()
        build = tostring(v) .. " (" .. tostring(b) .. ")"
    end
    local who = (UnitName("player") or "?") .. "-" .. (GetRealmName() or "?")
    local m = getMoney()
    local tips = tipsData()
    add("SITZUNG", string.format("%s | Client %s | RXP %s | Kombi-Test %s | Kombiguide %s | Testlog %s | Geld %s | KombiDaten %s",
        who, build, addonVersion("RXPGuides"),
        guideAddon("RXPGuides_Kombi"), guideAddon("RXPGuides_KombiGuide"), VERSION, m and money(m) or "?",
        tips and (tostring(tips.stand or "?") .. ", " .. #tips.tipps .. " Tipps") or "-"))
end

-- Kartengrenzen: Weltkoordinaten der Kartenecken (0,0) und (1,1) und Grösse in Yards.
-- Damit rechnet Claude Spielkoordinaten exakt in RXP-Weltkoordinaten um.
local function bestMap()
    if not (C_Map and C_Map.GetBestMapForUnit) then return nil end
    return C_Map.GetBestMapForUnit("player")
end

local function mapBounds(mapID)
    if not (C_Map and C_Map.GetWorldPosFromMapPos and CreateVector2D) then return nil end
    local ok0, c0, p0 = pcall(C_Map.GetWorldPosFromMapPos, mapID, CreateVector2D(0, 0))
    local ok1, _, p1 = pcall(C_Map.GetWorldPosFromMapPos, mapID, CreateVector2D(1, 1))
    if not (ok0 and ok1 and p0 and p1) then return nil end
    local x0, y0 = p0:GetXY()
    local x1, y1 = p1:GetXY()
    if not (x0 and y0 and x1 and y1) or isSecret(x0) then return nil end
    local w, h
    if C_Map.GetMapWorldSize then
        local ok, a, b = pcall(C_Map.GetMapWorldSize, mapID)
        if ok then w, h = a, b end
    end
    return { c = c0, x0 = x0, y0 = y0, x1 = x1, y1 = y1, w = w, h = h }
end

local function logMap(mapID, force)
    if not mapID or not db then return end
    db.maps = db.maps or {}
    if db.maps[mapID] and not force then return end
    local name = "?"
    if C_Map and C_Map.GetMapInfo then
        local ok, info = pcall(C_Map.GetMapInfo, mapID)
        if ok and type(info) == "table" and info.name and not isSecret(info.name) then name = info.name end
    end
    local b = mapBounds(mapID)
    if b then
        db.maps[mapID] = { name = name, c = b.c, x0 = b.x0, y0 = b.y0, x1 = b.x1, y1 = b.y1, w = b.w, h = b.h }
        add("KARTE", string.format("%d %s | Kontinent %s | 0,0 = %.2f, %.2f | 1,1 = %.2f, %.2f | Grösse %s x %s",
            mapID, name, tostring(b.c), b.x0, b.y0, b.x1, b.y1,
            b.w and string.format("%.1f", b.w) or "-", b.h and string.format("%.1f", b.h) or "-"))
    else
        db.maps[mapID] = { name = name, fehlt = true }
        add("KARTE", string.format("%d %s | keine Weltkoordinaten verfügbar", mapID, name))
    end
end

-- Handlungen (Version 3): Herstellen und Entzaubern über eigene Zauber und die Taschen
local function finishPending()
    if not pending then return end
    local p = pending
    pending = nil
    quietUntil = now() + 1.5
    local ids = {}
    for id in pairs(p.diff) do table.insert(ids, id) end
    table.sort(ids)
    local minus, plus, source = {}, {}, {}
    for _, id in ipairs(ids) do
        local d = p.diff[id]
        if d < 0 then
            table.insert(minus, string.format("%dx %s", -d, itemLabel(id)))
            table.insert(source, itemDetail(id, -d))
        else
            table.insert(plus, string.format("%dx %s (%d)", d, itemLabel(id), id))
        end
    end
    local skills = {}
    for name, v in pairs(p.skills) do
        table.insert(skills, string.format("%s %d -> %d", name, v[1], v[2]))
    end
    table.sort(skills)
    local point = (#skills > 0) and ("Punkt: " .. table.concat(skills, ", ")) or "kein Punkt"
    -- Zauber bei offenem Berufsfenster ohne jede Wirkung (z. B. ein Buff): keine Zeile
    if p.kind == "HERSTELLEN" and #ids == 0 and #skills == 0 then return end
    if p.kind == "ENTZAUBERN" then
        add("ENTZAUBERN", string.format("%s | Ergebnis: %s | %s",
            (#source > 0) and table.concat(source, ", ") or "Teil ?",
            (#plus > 0) and table.concat(plus, ", ") or "nichts", point))
    else
        add("HERSTELLEN", string.format("%s (%s) | verbraucht: %s | erhalten: %s | %s",
            p.name or "?", tostring(p.id),
            (#minus > 0) and table.concat(minus, ", ") or "-",
            (#plus > 0) and table.concat(plus, ", ") or "-", point))
    end
end

local function startPending(kind, id, name)
    finishPending()
    pending = { kind = kind, id = id, name = name, t0 = now(), tLast = now(), diff = {}, skills = {} }
end

local function isDisenchant(id, name)
    if DISENCHANT_IDS[id] then return true end
    local n = type(name) == "string" and string.lower(name) or ""
    return n == "entzaubern" or n == "disenchant"
end

local function isGather(cast)
    if not cast then return false end
    if GATHER_IDS[cast.id] then return true end
    local n = type(cast.name) == "string" and string.lower(cast.name) or ""
    for _, w in ipairs(GATHER_WORDS) do
        if n:find(w, 1, true) then return true end
    end
    return false
end

-- Lootfenster (Version 3): Quelle aus der GUID, Beute aus den Lootplätzen, Geld über PLAYER_MONEY
local function lootSource()
    local f = rawget(_G, "GetLootSourceInfo")
    if not f then return nil end
    local ok, guid = pcall(f, 1)
    if not ok or type(guid) ~= "string" or isSecret(guid) then return nil end
    local kind, id = guid:match("^(%a+)%-%d+%-%d+%-%d+%-%d+%-(%d+)%-")
    if kind == "Creature" or kind == "Vehicle" then return "Kreatur " .. id, "Creature" end
    if kind == "GameObject" then return "Objekt " .. id, "GameObject" end
    kind = guid:match("^(%a+)")
    if kind == "Item" then return "Gegenstand", "Item" end
    return kind, kind
end

local function readLoot()
    local parts = {}
    local n = (GetNumLootItems and GetNumLootItems()) or 0
    if isSecret(n) then return parts end
    local moneyType = (Enum and Enum.LootSlotType and Enum.LootSlotType.Money) or 2
    for slot = 1, n do
        local okT, slotType = pcall(GetLootSlotType, slot)
        local ok, _, item, quantity, _, _, _, _, _, _, isCoin = pcall(GetLootSlotInfo, slot)
        local coin = (okT and slotType == moneyType) or (ok and isCoin == true)
        if not coin then
            local link = GetLootSlotLink and GetLootSlotLink(slot)
            local name = linkName(link) or ((ok and type(item) == "string" and not isSecret(item)) and item) or "?"
            local id = (type(link) == "string" and not isSecret(link)) and link:match("item:(%d+)") or nil
            if id then remember(tonumber(id)) end   -- Version 3.6: Händlerpreis für den Wert pro Stunde
            local q = (ok and type(quantity) == "number" and not isSecret(quantity)) and quantity or 1
            table.insert(parts, string.format("%dx %s%s", q, name, id and (" (" .. id .. ")") or ""))
        end
    end
    return parts
end

local function finishLoot()
    if not lootRecord then return end
    local r = lootRecord
    lootRecord = nil
    if #r.items > 0 then quietUntil = now() + 1.5 end
    if not db.auto then return end
    -- leeres Lootfenster ohne Quelle (kam am 13.10. oft vor dem Kürschnern): sagt nichts aus
    if not r.src and #r.items == 0 and r.money == 0 then return end
    local parts = {}
    if r.how then table.insert(parts, r.how) end
    table.insert(parts, r.src or "Quelle ?")
    table.insert(parts, (#r.items > 0) and table.concat(r.items, ", ") or "keine Gegenstände")
    if r.money ~= 0 then table.insert(parts, "Geld " .. money(r.money, true)) end
    add(r.kind, table.concat(parts, " | "), true, r.ctx)
end

-- Fenster (Version 3.2): Ort beim Öffnen, Abstand, Sichtbarkeit, laufende Interaktion
local function playerPos()
    local mapID = bestMap()
    if not mapID or isSecret(mapID) or not C_Map.GetPlayerMapPosition then return nil end
    local pos = C_Map.GetPlayerMapPosition(mapID, "player")
    if not pos then return nil end
    local x, y = pos:GetXY()
    if not x or not y or isSecret(x) or isSecret(y) then return nil end
    return mapID, x, y
end

local function placeHere()
    local rec = { t0 = now() }
    local m, x, y = playerPos()
    if m then
        rec.map, rec.x, rec.y = m, x, y
        if C_Map.GetMapWorldSize then
            local ok, w, h = pcall(C_Map.GetMapWorldSize, m)
            if ok and type(w) == "number" and type(h) == "number" and not isSecret(w) and w > 0 and h > 0 then
                rec.w, rec.h = w, h
            end
        end
    end
    return rec
end

-- weiter als WINDOW_YARDS weg oder auf einer anderen Karte; ohne Ortsangabe: nein
local function movedAway(rec)
    if not rec.map then return false end
    local m, x, y = playerPos()
    if not m then return false end
    if m ~= rec.map then return true end
    if not (rec.w and rec.h) then return false end
    local dx, dy = (x - rec.x) * rec.w, (y - rec.y) * rec.h
    return dx * dx + dy * dy > WINDOW_YARDS * WINDOW_YARDS
end

local function interacting(itype)
    local pim = C_PlayerInteractionManager
    if not (pim and pim.IsInteractingWithNpcOfType) then return nil end
    local ok, v = pcall(pim.IsInteractingWithNpcOfType, itype)
    if not ok or isSecret(v) then return nil end
    return v and true or false
end

-- true: offen, false: zu, nil: keine Auskunft (weder Fenster noch Interaktion abfragbar)
local function stillOpen(info)
    local busy = interacting(info.itype)
    if busy then return true end
    local known = (busy ~= nil)
    for _, name in ipairs(info.frames) do
        local f = rawget(_G, name)
        if type(f) == "table" and type(f.IsShown) == "function" then
            local ok, v = pcall(f.IsShown, f)
            if ok and not isSecret(v) then
                if v then return true end
                known = true
            end
        end
    end
    if known then return false end
    return nil
end

local function windowGone(rec, info)
    if not info.free and movedAway(rec) then return "entfernt" end
    if now() - rec.t0 > 2 and stillOpen(info) == false then return "Fenster zu" end
    return nil
end

local function openWindow(name)
    if not windows[name] then windows[name] = placeHere() end
end

local function closeWindow(name)
    windows[name] = nil
    -- Flugkosten werden erst kurz nach dem Schliessen abgebucht (darum 2 s Nachlauf in moneyContext)
    if name == "taxi" then windows.taxiClosed = now() end
end

-- Version 3.4: Lehrerliste. Pro Lehrer und Sitzung eine Zeile mit jedem Eintrag: Name, Status, Lernstufe, Kosten.
-- Neu geschrieben nur, wenn sich Anzahl oder Filter ändern (Gelerntes steht in GELERNT).
-- API wie im Forever-UI 1.60.1 (Blizzard_TrainerUI/Mainline/Blizzard_TrainerUI.lua): GetNumTrainerServices,
-- GetTrainerServiceInfo, GetTrainerServiceSkillReq, GetTrainerServiceCost, GetTrainerServiceTypeFilter,
-- GetTrainerServiceStepIndex (Rang des Berufs, z. B. Geselle), IsTradeskillTrainer; dazu, falls vorhanden,
-- GetTrainerServiceItemLink (im Forever-UI nicht benutzt, darum ohne Gewähr).
local trainerSeen = {}     -- Lehrer -> Kennung der zuletzt geschriebenen Liste
local trainerToken = 0
local TRAINER_STATUS = { available = "lernbar", unavailable = "gesperrt", used = "gelernt" }

local function callApi(name, ...)
    local f = rawget(_G, name)
    if type(f) ~= "function" then return false end
    return pcall(f, ...)
end

local function plain(v)
    return (v ~= nil) and not isSecret(v)
end

-- Serverzeit in Sekunden (Version 3.5; seit 3.6 auch für Rezepte, Bestand und AH-Post)
local function epoch()
    local ok, t = callApi("GetServerTime")
    if ok and type(t) == "number" and plain(t) then return t end
    return (time and time()) or 0
end

local function npcInfo()
    local okN, name = pcall(UnitName, "npc")
    if not okN or type(name) ~= "string" or isSecret(name) then name = "?" end
    local okG, guid = callApi("UnitGUID", "npc")
    local id = (okG and type(guid) == "string" and not isSecret(guid)) and guid:match("^%a+%-%d+%-%d+%-%d+%-%d+%-(%d+)%-") or nil
    return name, id
end

local function trainerEntry(i, stepIndex)
    local ok, sName, sType, _, reqLevel, subText = callApi("GetTrainerServiceInfo", i)
    if not ok or type(sName) ~= "string" or isSecret(sName) or sType == "header" then return nil end
    local e = sName
    if type(subText) == "string" and subText ~= "" and not isSecret(subText) then e = e .. " [" .. subText .. "]" end
    if i == stepIndex then e = e .. " (Rang)" end
    local okL, link = callApi("GetTrainerServiceItemLink", i)   -- Rezepte: hergestellter Gegenstand (Name ist deutsch)
    local itemID = (okL and type(link) == "string" and not isSecret(link)) and link:match("item:(%d+)") or nil
    if itemID then e = e .. " (Item " .. itemID .. ")" end
    e = e .. " " .. (TRAINER_STATUS[sType] or tostring(sType))
    local req = {}
    if type(reqLevel) == "number" and plain(reqLevel) and reqLevel > 1 then table.insert(req, "Stufe " .. reqLevel) end
    local okS, skill, rank = callApi("GetTrainerServiceSkillReq", i)
    if okS and type(skill) == "string" and skill ~= "" and plain(skill) and type(rank) == "number" and plain(rank) then
        table.insert(req, skill .. " " .. rank)
    end
    if #req > 0 then e = e .. ", ab " .. table.concat(req, " und ") end
    local okC, cost = callApi("GetTrainerServiceCost", i)
    if okC and type(cost) == "number" and plain(cost) then
        e = e .. ", " .. ((cost > 0) and money(cost) or "kostenlos")
    end
    return e
end

local function trainerDump()
    if not db or not db.auto or not ready or not windows.trainer then return end
    local ok, n = callApi("GetNumTrainerServices")
    if not ok or type(n) ~= "number" or isSecret(n) or n <= 0 then return end
    local filters = {}
    for _, f in ipairs({ "available", "unavailable", "used" }) do
        local okF, on = callApi("GetTrainerServiceTypeFilter", f)
        if okF and on and plain(on) then table.insert(filters, TRAINER_STATUS[f]) end
    end
    local name, id = npcInfo()
    local sig = n .. "|" .. table.concat(filters, "+")
    if trainerSeen[id or name] == sig then return end
    local okI, stepIndex = callApi("GetTrainerServiceStepIndex")
    if not okI or not plain(stepIndex) then stepIndex = nil end
    local parts = {}
    for i = 1, n do
        local e = trainerEntry(i, stepIndex)
        if e then table.insert(parts, e) end
    end
    if #parts == 0 then return end
    trainerSeen[id or name] = sig
    local okT, isTrade = callApi("IsTradeskillTrainer")
    local kind = (okT and plain(isTrade)) and (isTrade and "Beruf" or "Klasse") or "?"
    add("LEHRER", string.format("%s%s | %s | Filter %s | %s | %s", name, id and (" (Kreatur " .. id .. ")") or "",
        kind, (#filters > 0) and table.concat(filters, "+") or "?",
        (#parts == 1) and "1 Eintrag" or (#parts .. " Einträge"), table.concat(parts, "; ")))
end

local function scheduleTrainerDump()
    trainerToken = trainerToken + 1
    local token = trainerToken
    if C_Timer and C_Timer.After then
        C_Timer.After(0.3, function() if token == trainerToken then trainerDump() end end)
    else
        trainerDump()
    end
end

-- Version 3.6: Rezepte beim Öffnen des Berufsfensters. API wie im Forever-UI 1.60.1 (70374), C_TradeSkillUI:
-- GetChildProfessionInfo, sonst GetBaseProfessionInfo (Professions.GetProfessionInfo); GetFilteredRecipeIDs (das
-- Forever-UI zeigt nur gelernte Rezepte: Camelot/Blizzard_Professions.lua, GetDefaultShowUnlearned = false);
-- GetRecipeInfo (learned, relativeDifficulty 0 orange, 1 gelb, 2 grün, 3 grau); GetRecipeSchematic (Reagenzien,
-- Menge, Ergebnis); GetRecipeOutputItemData; IsDataSourceChanging, IsTradeSkillLinked, IsTradeSkillGuild, IsNPCCrafting.
-- GetAllRecipeIDs benutzt das Forever-UI nicht: nur, wenn vorhanden (ungeprüft). Ein Rezept in der Datei:
-- «Rezept-ID:Ergebnis-ID:Menge min:Menge max:Farbe:Reagenzien», Ergebnis 0 = Verzauberung ohne Gegenstand,
-- Reagenzien «ID*Anzahl,…». Danach nur Farbwechsel (mit der Fertigkeit: zeigt, ab wann ein Rezept die Farbe wechselt).
local DIFF_NAMES = { [0] = "orange", [1] = "gelb", [2] = "grün", [3] = "grau" }

local function tsCall(name, ...)
    local api = C_TradeSkillUI
    local f = api and api[name]
    if type(f) ~= "function" then return false end
    return pcall(f, ...)
end

local function profInfo()
    local ok, p = tsCall("GetChildProfessionInfo")
    if not ok or type(p) ~= "table" or not p.professionID or p.professionID == 0 then
        ok, p = tsCall("GetBaseProfessionInfo")
    end
    if not ok or type(p) ~= "table" then return nil end
    local name = p.parentProfessionName
    if type(name) ~= "string" or name == "" or isSecret(name) then name = p.professionName end
    if type(name) ~= "string" or name == "" or isSecret(name) then return nil end
    return name, num(p.skillLevel), num(p.maxSkillLevel)
end

-- Filter des Berufsfensters wie Professions.IsUsingDefaultFilters (Blizzard_ProfessionsTemplates/Blizzard_Professions.lua),
-- aber ohne «nicht gelernte zeigen»: Das Forever-UI blendet nicht gelernte Rezepte von sich aus aus
-- (Camelot/Blizzard_Professions.lua). Ist einer an, fehlen Rezepte in der Liste.
local function recipeFilters()
    local filt = {}
    local function on(fn, label)
        local ok, v = tsCall(fn)
        if ok and plain(v) and v == true then filt[#filt + 1] = label end
    end
    on("GetOnlyShowMakeableRecipes", "nur herstellbar")
    on("GetOnlyShowSkillUpRecipes", "nur mit Punkten")
    on("GetOnlyShowFirstCraftRecipes", "nur erstes Herstellen")
    on("AreAnyInventorySlotsFiltered", "Platz")
    on("AnyRecipeCategoriesFiltered", "Kategorie")
    local okL, learned = tsCall("GetShowLearned")
    if okL and plain(learned) and learned == false then filt[#filt + 1] = "gelernte ausgeblendet" end
    local P = rawget(_G, "Professions")
    if type(P) == "table" and type(P.AreAllSourcesUnfiltered) == "function" then
        local ok, v = pcall(P.AreAllSourcesUnfiltered)
        if ok and v == false then filt[#filt + 1] = "Quelle" end
    end
    local okT, txt = tsCall("GetRecipeItemNameFilter")
    if okT and type(txt) == "string" and not isSecret(txt) and txt ~= "" then filt[#filt + 1] = "Suche «" .. txt .. "»" end
    return filt
end

local function recipeEntry(r)
    local rg = {}
    for j, x in ipairs(r.reag) do rg[j] = x[1] .. "*" .. x[2] end
    return string.format("%d:%d:%d:%d:%s:%s", r.id, r.out or 0, r.qmin, r.qmax, r.diff and tostring(r.diff) or "-",
        table.concat(rg, ","))
end

local function recipeRecord(id)
    local okR, info = tsCall("GetRecipeInfo", id)
    if not okR or type(info) ~= "table" or info.learned ~= true or info.isDummyRecipe or info.isGatheringRecipe
        or info.isSalvageRecipe or info.isRecraft then
        return nil
    end
    local okS, sch = tsCall("GetRecipeSchematic", id, false)
    if not okS or type(sch) ~= "table" then sch = {} end
    local reag = {}
    for _, slot in ipairs(type(sch.reagentSlotSchematics) == "table" and sch.reagentSlotSchematics or {}) do
        local first = type(slot.reagents) == "table" and slot.reagents[1] or nil
        local basic = slot.reagentType == nil or slot.reagentType == 1 or slot.required == true
        local q = num(slot.quantityRequired) or 1
        if first and num(first.itemID) and basic and q > 0 then
            reag[#reag + 1] = { first.itemID, q }
        end
    end
    local out = num(sch.outputItemID)
    if not out and not info.isEnchantingRecipe then
        local okO, o = tsCall("GetRecipeOutputItemData", id)
        if okO and type(o) == "table" then out = num(o.itemID) end
    end
    local name = (type(info.name) == "string" and not isSecret(info.name)) and info.name or "?"
    return { id = id, name = name, out = out, qmin = num(sch.quantityMin) or 1, qmax = num(sch.quantityMax) or 1,
             diff = num(info.relativeDifficulty), reag = reag }
end

local function recipeDump()
    if not db or not db.auto or not ready then return end
    local okD, changing = tsCall("IsDataSourceChanging")
    if okD and plain(changing) and changing then return end   -- das nächste TRADE_SKILL_LIST_UPDATE abwarten
    for _, fn in ipairs({ "IsTradeSkillLinked", "IsTradeSkillGuild", "IsNPCCrafting" }) do
        local ok, v = tsCall(fn)
        if ok and plain(v) and v then return end   -- fremde Liste oder Herstellen beim NPC: nicht die eigenen Rezepte
    end
    local pname, skill, maxSkill = profInfo()
    if not pname then return end
    local source = "alle"
    local okI, ids = tsCall("GetAllRecipeIDs")
    if not okI or type(ids) ~= "table" then
        source = "Liste des Fensters"
        okI, ids = tsCall("GetFilteredRecipeIDs")
    end
    if not okI or type(ids) ~= "table" then return end
    local recs = {}
    for _, id in ipairs(ids) do
        if num(id) then
            local r = recipeRecord(id)
            if r then recs[#recs + 1] = r end
        end
    end
    if #recs == 0 then return end
    table.sort(recs, function(a, b) return a.id < b.id end)
    local filt = (source == "alle") and {} or recipeFilters()
    db.beobachten = db.beobachten or {}
    db.rezeptNamen = db.rezeptNamen or {}
    local sigParts = {}
    for i, r in ipairs(recs) do
        sigParts[i] = r.id
        for _, x in ipairs(r.reag) do db.beobachten[x[1]] = true end
        if r.out then db.beobachten[r.out] = true end
        db.rezeptNamen[r.id] = r.name
    end
    local skillText = (skill and maxSkill) and string.format("%s %d/%d", pname, skill, maxSkill) or pname
    local c = charDB()
    c.rezepte = c.rezepte or {}
    local old = c.rezepte[pname]
    local map = {}
    if #filt > 0 and old and old.liste then
        -- gefiltert: nur die sichtbaren Rezepte im gespeicherten Stand ersetzen, die übrigen bleiben
        for e in string.gmatch(old.liste, "[^;]+") do
            local id = tonumber(e:match("^(%d+):"))
            if id then map[id] = e end
        end
    end
    for _, r in ipairs(recs) do map[r.id] = recipeEntry(r) end
    local ids, entries = {}, {}
    for id in pairs(map) do ids[#ids + 1] = id end
    table.sort(ids)
    for i, id in ipairs(ids) do entries[i] = map[id] end
    -- filter: die gespeicherte Liste kann unvollständig sein (bisher nur gefiltert gesehen)
    local incomplete
    if #filt > 0 then
        if old and old.liste then incomplete = old.filter else incomplete = table.concat(filt, ", ") end
    end
    c.rezepte[pname] = { zeit = epoch(), stufe = skill, max = maxSkill, quelle = source, filter = incomplete,
                         liste = table.concat(entries, ";") }
    -- Farbwechsel der sichtbaren Rezepte
    local seen = recipeSeen[pname]
    local sig = table.concat(sigParts, ",")
    if seen and (seen.sig == sig or #filt > 0) then
        local changes = {}
        for _, r in ipairs(recs) do
            local before = seen.farben[r.id]
            if before ~= nil and before ~= (r.diff or -1) then
                changes[#changes + 1] = string.format("%s %s -> %s", r.name, DIFF_NAMES[before] or "?", DIFF_NAMES[r.diff] or "?")
            end
            seen.farben[r.id] = r.diff or -1
        end
        if #changes > 0 then add("REZEPTE", skillText .. " | Farbe: " .. table.concat(changes, ", ")) end
        return
    end
    if #filt > 0 then
        -- gefiltert und in dieser Sitzung noch keine ganze Liste: kurz melden, die ganze Liste kommt ohne Filter
        local farben = {}
        for _, r in ipairs(recs) do farben[r.id] = r.diff or -1 end
        recipeSeen[pname] = { sig = nil, farben = farben }
        add("REZEPTE", string.format("%s | Liste gefiltert (%s): %d %s sichtbar, gespeicherter Stand ergänzt", skillText,
            table.concat(filt, ", "), #recs, (#recs == 1) and "Rezept" or "Rezepte"))
        return
    end
    local colors = {}
    for _, r in ipairs(recs) do colors[r.id] = r.diff or -1 end
    recipeSeen[pname] = { sig = sig, farben = colors }
    local parts = {}
    for _, r in ipairs(recs) do
        local rg = {}
        for j, x in ipairs(r.reag) do rg[j] = string.format("%dx %s", x[2], idLabel(x[1])) end
        local res = "Verzauberung"
        if r.out then
            res = ((r.qmin == r.qmax) and tostring(r.qmin) or (r.qmin .. "-" .. r.qmax)) .. "x " .. idLabel(r.out)
        end
        parts[#parts + 1] = string.format("%s (%d): %s -> %s, %s", r.name, r.id, (#rg > 0) and table.concat(rg, " + ") or "-",
            res, DIFF_NAMES[r.diff] or "?")
    end
    add("REZEPTE", string.format("%s | %d Rezepte (%s) | %s", skillText, #recs, source, table.concat(parts, "; ")))
end

local function scheduleRecipeDump()
    recipeToken = recipeToken + 1
    local token = recipeToken
    local function run()
        if token ~= recipeToken or not windows.profession then return end   -- Fenster inzwischen zu: nichts lesen
        local ok, err = pcall(recipeDump)
        if not ok then add("FEHLER", "Rezepte: " .. tostring(err), false) end
    end
    if C_Timer and C_Timer.After then C_Timer.After(1, run) else run() end
end

-- Geld (Version 3): Kontext aus offenen Fenstern
local function moneyContext()
    local t = now()
    if windows.trainer then return "Lehrer" end
    if windows.taxi or (windows.taxiClosed and t - windows.taxiClosed < 2) then return "Flugmeister" end
    if windows.quest or (windows.questDone and t - windows.questDone < 2) then return "Quest" end
    return "sonst"
end

-- Händler, Post, Auktionshaus (Version 3): alles, was sich bei offenem Fenster in Taschen und Geld ändert, als eine Zeile.
-- Version 3.2: mit Dauer und dem Grund, warum die Sitzung endete. «stale» = Fenster war schon vorher zu,
-- die gerade laufende Änderung gehört nicht mehr dazu (darum keine Ruhezeit für TASCHE).
local function finishSession(reason, stale)
    if not session then return end
    local s = session
    session = nil
    if not stale then quietUntil = now() + 1.5 end
    if not db.auto then return end
    local ids = {}
    for id in pairs(s.diff) do table.insert(ids, id) end
    table.sort(ids)
    local got, gave = {}, {}
    for _, id in ipairs(ids) do
        local d = s.diff[id]
        local txt = string.format("%dx %s (%d)", math.abs(d), itemLabel(id), id)
        if d > 0 then table.insert(got, txt) else table.insert(gave, txt) end
    end
    if #got == 0 and #gave == 0 and s.nPlus == 0 and s.nMinus == 0 then return end
    local w = SESSION_INFO[s.kind].words
    local parts = {}
    if #gave > 0 then table.insert(parts, w[2] .. ": " .. table.concat(gave, ", ")) end
    if #got > 0 then table.insert(parts, w[1] .. ": " .. table.concat(got, ", ")) end
    if s.nPlus > 0 then table.insert(parts, string.format("Einnahmen %s (%d)", money(s.plus, true), s.nPlus)) end
    if s.nMinus > 0 then table.insert(parts, string.format("Ausgaben %s (%d)", money(s.minus, true), s.nMinus)) end
    -- Beim Ausloggen meldet GetMoney 0 (Testlog 13.10. 22:47, 22:48, 22:51): dann den letzten bekannten Stand nehmen
    local m = getMoney()
    if reason == "Ausloggen" then m = moneyLast or m end
    table.insert(parts, "Bestand " .. (m and money(m) or "?"))
    table.insert(parts, string.format("Dauer %d s, Ende %s", math.floor(now() - s.t0 + 0.5), reason or "?"))
    -- Ort und Schritt vom Öffnen: Wird das Ende erst später bemerkt, steht der Charakter schon woanders
    add(s.kind, table.concat(parts, " | "), true, s.ctx)
end

local function startSession(kind)
    if session and session.kind == kind then return end   -- manche Fenster melden sich doppelt
    finishSession("neues Fenster")
    session = placeHere()
    session.kind, session.diff, session.ctx = kind, {}, context()
    session.plus, session.minus, session.nPlus, session.nMinus = 0, 0, 0, 0
    if kind == "AUKTIONSHAUS" then ahWanted = now() end   -- Version 3.5: AH-Scan beim nächsten Takt
end

-- Version 3.2: die offene Sitzung, wenn ihr Fenster noch offen ist; sonst beenden
local function liveSession()
    local s = session
    if not s then return nil end
    local why = windowGone(s, SESSION_INFO[s.kind])
    if not why and now() - s.t0 > SESSION_MAX then why = "Zeitlimit" end
    if why then
        finishSession(why, true)
        return nil
    end
    return s
end

-- Version 3.5: AH-Preisscan.
-- Liest alle Angebote des Auktionshauses und speichert pro Gegenstand Tiefstpreis, Median (nach Stückzahl gewichtet),
-- Menge und Anzahl Angebote; für die Gegenstände des Plans (AH_WATCH, DEFAULT_ITEMS, /tl item) dazu die Preisstufen.
-- Läuft beim Öffnen des Auktionshauses von selbst (höchstens alle 15 Minuten) oder mit /tl ah.
-- API laut Forever-UI 1.60.1 (70374), Blizzard_APIDocumentationGenerated/AuctionHouseDocumentation.lua:
--   C_AuctionHouse.ReplicateItems («should be used in place of an 'allItem' QueryAuctionItems call to query the entire
--   auction house»; ohne HasRestrictions), GetNumReplicateItems, GetReplicateItemInfo (3. Wert Anzahl, 10. Sofortkauf,
--   17. Item-ID), Ereignis REPLICATE_ITEM_LIST_UPDATE.
-- Ungeprüft im Spiel (Test T15): ob der Index bei 0 oder 1 beginnt (wird am ersten Eintrag erkannt) und ob der
-- Sofortkaufpreis für das ganze Angebot gilt (so gerechnet: Preis pro Stück = Sofortkauf / Anzahl).
-- Wartezeit: Der Auto-Scan von AHledger läuft höchstens alle 15 Minuten, sein Knopf zählt herunter, bis der Server
-- wieder einen Scan erlaubt (https://www.curseforge.com/wow/addons/ahledger, Stand 12.10.2026). Wie lange der Server
-- sperrt, steht dort nicht (ungeprüft); das Testlog wartet wie AHledger 15 Minuten. Verkäufernamen speichert es nicht.
local AH_PAUSE = 900      -- Sekunden zwischen zwei automatischen Scans (wie AHledgers Auto-Scan)
local AH_TIMEOUT = 120    -- Sekunden ohne Ergebnis: abbrechen
local AH_QUIET = 2        -- Sekunden ohne neues Ereignis, dann lesen
local AH_BATCH = 1000     -- Angebote pro Bildaufbau
local AH_STEPS = 100      -- Preisstufen pro Gegenstand des Plans (reicht für den Einkauf von einigen hundert Stück)
local AH_KEEP = 60        -- gespeicherte Scans (der älteste fällt weg)
local AH_KEEP_FULL = 10   -- so viele neueste Scans behalten alle Gegenstände und die Preisstufen; ältere nur die
                          -- Plan-Gegenstände (hält die Datei klein; Claude übernimmt jeden Scan ins Repo)

local function ahIsOpen()
    local s = liveSession()
    if s and s.kind == "AUKTIONSHAUS" then return true end
    return interacting(SESSION_INFO["AUKTIONSHAUS"].itype) == true
end

local function ahLabel(id)
    local n = C_Item and C_Item.GetItemNameByID and C_Item.GetItemNameByID(id)
    if type(n) == "string" and not isSecret(n) then return n .. " (" .. id .. ")" end
    return tostring(id)
end

-- Anzahl, Sofortkaufpreis und Item-ID eines Angebots (3., 10. und 17. Wert von GetReplicateItemInfo)
local function ahEntry(i)
    local ok, _, _, count, _, _, _, _, _, _, buyout, _, _, _, _, _, _, itemID = pcall(C_AuctionHouse.GetReplicateItemInfo, i)
    if not ok then return nil end
    return count, buyout, itemID
end

local function ahFail(why)
    ahScan = nil
    add("AH-SCAN", "abgebrochen: " .. why)
    say("AH-Scan abgebrochen: " .. why)
end

-- Tiefstpreis, Median nach Stückzahl und Menge; sortiert die Liste nach Preis pro Stück
local function ahStats(list)
    table.sort(list, function(a, b) return a[1] < b[1] end)
    local total = 0
    for _, e in ipairs(list) do total = total + e[2] end
    local acc, med = 0, list[#list][1]
    for _, e in ipairs(list) do
        acc = acc + e[2]
        if acc * 2 >= total then
            med = e[1]
            break
        end
    end
    return list[1][1], med, total
end

-- Preisstufen der billigsten Angebote (Kupfer pro Stück), gleiche Preise zusammengefasst. Version 3.6:
-- «Preis*Stück*davon lang*davon sehr lang» (Restlaufzeit-Band 2 bzw. 3 von Enum.AuctionHouseTimeLeftBand 0–3).
-- GetReplicateItemTimeLeft liefert laut Doku nur «number»; die alte API (GetAuctionItemTimeLeft) zählte 1–4. Darum:
-- Rohwert + Versatz (0 oder -1, erkannt in ahFinish); unbekannter Versatz: lang und sehr lang = 0.
local function ahSteps(list, offset)
    local steps = {}
    for _, e in ipairs(list) do
        local u = math.floor(e[1] + 0.5)
        local band = (offset and e[3] and e[3] >= 0) and (e[3] + offset) or -1
        local l = (band >= 2) and e[2] or 0
        local v = (band == 3) and e[2] or 0
        local last = steps[#steps]
        if last and last[1] == u then
            last[2], last[3], last[4] = last[2] + e[2], last[3] + l, last[4] + v
        elseif #steps < AH_STEPS then
            steps[#steps + 1] = { u, e[2], l, v }
        else
            break
        end
    end
    local parts = {}
    for i, st in ipairs(steps) do parts[i] = st[1] .. "*" .. st[2] .. "*" .. st[3] .. "*" .. st[4] end
    return table.concat(parts, ",")
end

-- Version 3.6: Grenzen der Restlaufzeit-Bänder in Sekunden laut Client (C_AuctionHouse.GetTimeLeftBandInfo:
-- timeLeftMinSeconds, timeLeftMaxSeconds), «Band:min-max;…»
local function ahBands()
    local api = C_AuctionHouse
    if not (api and api.GetTimeLeftBandInfo) then return nil end
    local parts = {}
    for b = 0, 3 do
        local ok, lo, hi = pcall(api.GetTimeLeftBandInfo, b)
        if ok and num(lo) and num(hi) then parts[#parts + 1] = string.format("%d:%d-%d", b, lo, hi) end
    end
    return (#parts > 0) and table.concat(parts, ";") or nil
end

local function parseBands(text)
    local out = {}
    for b, lo, hi in string.gmatch(text or "", "(%d+):(%d+)%-(%d+)") do out[tonumber(b)] = { tonumber(lo), tonumber(hi) } end
    return out
end

local function parseSteps(text)
    local out = {}
    for u, n, l, v in string.gmatch(text or "", "(%d+)%*(%d+)%*(%d+)%*(%d+)") do
        out[#out + 1] = { tonumber(u), tonumber(n), tonumber(l), tonumber(v) }
    end
    return out
end

-- Version 3.6: Abnahme seit dem letzten Scan, eine Schätzung. Von den billigsten Angeboten des letzten Scans zählen nur
-- die, die bis jetzt nicht ablaufen konnten (Band «lang», wenn der Abstand kürzer ist als dessen Untergrenze, sonst
-- «sehr lang»). Annahme: Käufer nehmen die billigsten zuerst (so verkauft der Server Waren; bei Ausrüstung ungenau).
-- Von unten nach oben: was davon jetzt fehlt, ist weg (gekauft oder zurückgezogen); die erste Stufe, auf der jetzt noch
-- etwas liegt, beendet die Zählung (weiter oben ist kein Käufer gegangen). «gekauft» = weg minus neue Angebote bis zu
-- dieser Stufe (sonst sähe Umstellen auf einen tieferen Preis aus wie ein Kauf). Nicht erkennbar bleibt, wer zurückzieht
-- und höher neu einstellt: dann ist die Schätzung zu hoch. Gibt weg, gekauft zurück oder nil (unbekannt): Abstand zu
-- gross, Gegenstand ganz verschwunden (gekauft oder zurückgezogen?) oder keine Angebote, die nicht ablaufen konnten.
local function ahDemand(prevSteps, cur, dt, bands)
    local long, vlong = bands[2] and bands[2][1], bands[3] and bands[3][1]
    local mode
    if long and dt < long then mode = 3 elseif vlong and dt < vlong then mode = 4 else return nil end
    if #cur == 0 then return nil end
    local curN = {}
    for _, e in ipairs(cur) do
        local u = math.floor(e[1] + 0.5)
        curN[u] = (curN[u] or 0) + e[2]
    end
    local prevN = {}
    for _, st in ipairs(prevSteps) do prevN[st[1]] = st[2] end
    local gone, stopU, anySafe = 0, nil, false
    for _, st in ipairs(prevSteps) do
        local safe = st[mode]
        local still = curN[st[1]] or 0
        if safe > 0 then anySafe = true end
        gone = gone + math.max(0, safe - still)
        stopU = st[1]
        if still > 0 then break end
    end
    if not anySafe then return nil end
    local new = 0
    for u, n in pairs(curN) do
        if u <= stopU then new = new + math.max(0, n - (prevN[u] or 0)) end
    end
    return gone, math.max(0, gone - new)
end

-- Version 3.6: Rohwerte von GetReplicateItemTimeLeft -> Versatz zu Enum.AuctionHouseTimeLeftBand (0–3).
-- Werte 1 bis 4 mit einer 4: Versatz -1 (wie die alte API); Werte 0 bis 3 mit einer 0: Versatz 0. Nur 1 bis 3: der
-- zuletzt erkannte Versatz. Alles andere (z. B. Sekunden, oder 0 und 4 zusammen) passt zu keiner Zählung: kein Versatz,
-- auch der gespeicherte gilt nicht mehr. Ohne Versatz zählen lang und sehr lang nicht (keine Abnahme).
local function ahBandOffset(s)
    local lo, hi = s.bandMin, s.bandMax
    if lo == nil then return db.ahBandVersatz end
    if lo >= 1 and hi == 4 then
        db.ahBandVersatz = -1
    elseif lo == 0 and hi <= 3 then
        db.ahBandVersatz = 0
    elseif lo < 0 or hi > 4 or (lo == 0 and hi == 4) then
        db.ahBandVersatz = nil
    end
    return db.ahBandVersatz
end

local function ahMarket()
    local realm = GetRealmName and GetRealmName()
    if type(realm) ~= "string" or isSecret(realm) then realm = "?" end
    local okF, faction = pcall(UnitFactionGroup, "player")
    if not okF or type(faction) ~= "string" or isSecret(faction) then faction = "?" end
    local okR, region = callApi("GetCurrentRegionName")
    -- in der Beta liefert der Client einen leeren Text (Testlog 15.10.)
    if not okR or type(region) ~= "string" or isSecret(region) or region == "" then region = "?" end
    return realm, faction, region
end

local function ahFinish()
    local s = ahScan
    ahScan = nil
    local ids = {}
    for id in pairs(s.items) do ids[#ids + 1] = id end
    table.sort(ids)
    local offset = ahBandOffset(s)
    local all, plan, steps, stat = {}, {}, {}, {}
    for _, id in ipairs(ids) do
        local list = s.items[id]
        local lo, med, total = ahStats(list)
        lo, med = math.floor(lo + 0.5), math.floor(med + 0.5)
        stat[id] = { lo, med, total }
        local entry = string.format("%d:%.0f:%.0f:%d:%d", id, lo, med, total, #list)   -- %.0f: Kupfer über 2^31
        all[#all + 1] = entry
        if watched(id) then
            plan[#plan + 1] = entry
            steps[id] = ahSteps(list, offset)
        end
    end
    local realm, faction, region = ahMarket()
    local build = "-"
    if GetBuildInfo then
        local v, b = GetBuildInfo()
        build = tostring(v) .. " (" .. tostring(b) .. ")"
    end
    local bandsText = ahBands()
    local rec = {
        zeit = s.epoch, datum = date("%Y-%m-%d %H:%M", s.epoch), realm = realm, fraktion = faction, region = region,
        client = build, angebote = s.n, gegenstaende = #ids, nurGebot = s.bidOnly, fehlend = s.missing, geheim = s.secret,
        dauer = math.floor(now() - s.t0 + 0.5), alle = table.concat(all, ";"), plan = table.concat(plan, ";"), stufen = steps,
        baender = bandsText, bandVersatz = offset,
        bandRoh = s.bandMin and string.format("%d-%d", s.bandMin, s.bandMax) or nil,
    }
    -- Version 3.6: Abnahme seit dem letzten Scan desselben Markts. Beide Scans fast vollständig (fehlende Angebote sähen
    -- aus wie Käufe), der Scan davor mit bekanntem Restlaufzeit-Band.
    db.ahScans = db.ahScans or {}
    local prev = db.ahScans[#db.ahScans]
    local demandText = ""
    local complete = function(r) return (r.fehlend or 0) <= (r.angebote or 0) * 0.005 and (r.geheim or 0) == 0 end
    if prev and prev.stufen and prev.baender and prev.bandVersatz and prev.zeit and prev.realm == realm
        and prev.fraktion == faction and prev.region == region and complete(prev) and complete(rec) then
        local dt = s.epoch - prev.zeit
        local bands = parseBands(prev.baender)
        local pids = {}
        for id in pairs(prev.stufen) do pids[#pids + 1] = id end
        table.sort(pids)
        local out, sold = {}, {}
        for _, id in ipairs(pids) do
            if dt > 0 and watched(id) then
                local g, m = ahDemand(parseSteps(prev.stufen[id]), s.items[id] or {}, dt, bands)
                if g then
                    out[#out + 1] = string.format("%d:%d:%d", id, g, m)
                    if m > 0 then sold[#sold + 1] = { id, m } end
                end
            end
        end
        if #out > 0 then
            rec.abnahme, rec.abstand = table.concat(out, ";"), dt
            table.sort(sold, function(a, b) return a[2] > b[2] end)
            local top = {}
            for i = 1, math.min(5, #sold) do top[i] = string.format("%s %d", ahLabel(sold[i][1]), sold[i][2]) end
            demandText = string.format(" | Abnahme seit dem letzten Scan (%d Min): %d %s verglichen, geschätzt gekauft: %s",
                math.floor(dt / 60 + 0.5), #out, (#out == 1) and "Gegenstand" or "Gegenstände",
                (#top > 0) and table.concat(top, ", ") or "nichts")
        end
    end
    table.insert(db.ahScans, rec)
    while #db.ahScans > AH_KEEP do table.remove(db.ahScans, 1) end
    for i = 1, #db.ahScans - AH_KEEP_FULL do
        db.ahScans[i].alle, db.ahScans[i].stufen = nil, nil
    end
    local parts = {}
    for _, id in ipairs(AH_WATCH) do
        local st = stat[id]
        if st then parts[#parts + 1] = string.format("%s %s / %s / %d", ahLabel(id), money(st[1]), money(st[2]), st[3]) end
    end
    local warn = ""
    if s.missing > s.n * 0.1 then
        warn = string.format(" | unvollständig: %d Angebote ohne Daten (Auktionshaus zu früh geschlossen?)", s.missing)
    end
    if s.secret > 0 then warn = warn .. string.format(" | %d Angebote mit geheimen Werten", s.secret) end
    -- die Abnahme steht vor der Preisliste (tools/ah_aus_testlog.py liest die Liste bis zum Zeilenende)
    add("AH-SCAN", string.format("Scan %s | %s %s | Realm %s | %d Angebote, %d Gegenstände, %d nur mit Gebot, %d s%s%s | Tiefstpreis / Median / Stück: %s",
        rec.datum, region, faction, realm, s.n, #ids, s.bidOnly, rec.dauer, warn, demandText,
        (#parts > 0) and table.concat(parts, "; ") or "keine Plan-Gegenstände im Angebot"))
    local ex = stat[2318]
    say(string.format("AH-Scan fertig: %d Angebote, %d Gegenstände.%s", s.n, #ids,
        ex and string.format(" Leichtes Leder: Tiefstpreis %s, Median %s, %d Stück.", money(ex[1]), money(ex[2]), ex[3]) or ""))
    if not db.ahHinted then
        db.ahHinted = true
        say("Einmal prüfen: Zeigt das Auktionshaus für Leichtes Leder denselben Tiefstpreis pro Stück? Wenn nicht: /tl bug AH-Preis")
    end
end

local function ahBatch()
    local s = ahScan
    if not s or s.phase ~= "lesen" then return end
    local last = math.min(s.i + AH_BATCH, s.n)
    for k = s.i, last - 1 do
        local count, buyout, id = ahEntry(k + s.base)
        if id == nil or count == nil or buyout == nil then
            s.missing = s.missing + 1
        elseif isSecret(id) or isSecret(count) or isSecret(buyout) then
            s.secret = s.secret + 1
        elseif buyout <= 0 or count <= 0 then
            s.bidOnly = s.bidOnly + 1
        else
            local list = s.items[id]
            if not list then
                list = {}
                s.items[id] = list
            end
            if watched(id) then
                -- Version 3.6: Restlaufzeit als Rohwert (Versatz zum Band erst in ahFinish) für die Abnahme
                local okT, band = pcall(C_AuctionHouse.GetReplicateItemTimeLeft, k + s.base)
                band = (okT and num(band)) or -1
                if band >= 0 then
                    s.bandMin = math.min(s.bandMin or band, band)
                    s.bandMax = math.max(s.bandMax or band, band)
                end
                list[#list + 1] = { buyout / count, count, band }
            else
                list[#list + 1] = { buyout / count, count }
            end
        end
    end
    s.i = last
    if s.i >= s.n then
        ahFinish()
    elseif C_Timer and C_Timer.After then
        C_Timer.After(0, function()
            local ok, err = pcall(ahBatch)
            if not ok then ahFail("Fehler beim Lesen: " .. tostring(err)) end
        end)
    else
        ahBatch()
    end
end

local function ahRead()
    local s = ahScan
    local ok, n = pcall(C_AuctionHouse.GetNumReplicateItems)
    if not ok or type(n) ~= "number" or isSecret(n) or n <= 0 then
        ahFail("keine Angebote erhalten")
        return
    end
    local _, _, id0 = ahEntry(0)
    s.phase, s.n, s.i, s.base = "lesen", n, 0, (id0 ~= nil) and 0 or 1
    s.items, s.bidOnly, s.missing, s.secret = {}, 0, 0, 0
    ahBatch()
end

local function ahStart(manual)
    ahWanted = nil
    if ahScan then
        if manual then say("AH-Scan läuft schon.") end
        return
    end
    local api = C_AuctionHouse
    if not (api and api.ReplicateItems and api.GetNumReplicateItems and api.GetReplicateItemInfo) then
        add("AH-SCAN", "nicht möglich: C_AuctionHouse.ReplicateItems fehlt in diesem Client")
        if manual then say("AH-Scan nicht möglich: Der Client hat C_AuctionHouse.ReplicateItems nicht.") end
        return
    end
    if not ahIsOpen() then
        if manual then say("Bitte zuerst das Auktionshaus öffnen, dann /tl ah.") end
        return
    end
    local t = epoch()
    local since = t - (db.ahTry or 0)
    if since < AH_PAUSE then
        if not manual then
            -- die Wartezeit gilt fürs ganze Konto (auch ein Scan des Bankcharakters zählt): darum melden
            say(string.format("AH-Scan übersprungen: letzter Versuch vor %d Min, von selbst erst nach 15 Min. Sofort: /tl ah",
                math.floor(since / 60)))
            return
        end
        say(string.format("Letzter Versuch vor %d Min. Der Server lässt einen neuen Scan erst nach einer Wartezeit zu "
            .. "(Dauer ungeprüft); ich versuche es trotzdem.", math.floor(since / 60)))
    end
    local ok, err = pcall(api.ReplicateItems)
    if not ok then
        add("AH-SCAN", "Start fehlgeschlagen: " .. tostring(err))
        say("AH-Scan konnte nicht starten: " .. tostring(err))
        return
    end
    db.ahTry = t
    ahScan = { t0 = now(), epoch = t, phase = "warten", manual = manual }
    say("AH-Scan läuft: Auktionshaus offen lassen, bis «AH-Scan fertig» kommt.")
end

local function ahTick()
    local t = now()
    if ahWanted and t - ahWanted >= 1 then
        ahWanted = nil
        if db.ahAuto ~= false and ready then ahStart(false) end
    end
    local s = ahScan
    if not s then return end
    if s.phase == "warten" and t - s.t0 > AH_TIMEOUT then
        ahFail(string.format("kein Ergebnis nach %d s. Später nochmals das Auktionshaus öffnen oder /tl ah "
            .. "(der Server lässt einen neuen Scan erst nach einer Wartezeit zu; das Testlog wartet 15 Minuten).", AH_TIMEOUT))
    elseif s.phase == "daten" and (t - s.tEvent >= AH_QUIET or t - s.t0 > AH_TIMEOUT) then
        -- AH_TIMEOUT: auch wenn das Ereignis nie ruhig wird, irgendwann lesen
        ahRead()
    elseif s.phase == "lesen" and t - s.t0 > 600 then
        ahFail("Lesen dauerte zu lange")
    end
end

-- Version 3.6: Bestand. Taschen beim Ein- und Ausloggen, Bank beim Öffnen und Schliessen. Die Forever-Bank hat Reiter
-- (C_Bank.FetchPurchasedBankTabData mit Enum.BankType Character und Account, Behälter-ID im Feld ID; Forever-UI 1.60.1,
-- Blizzard_UIPanels_Game/Camelot/BankFrame.lua und BankDocumentation.lua). Gespeichert als «ID:Anzahl;…» pro Charakter,
-- die Kontobank für alle; für tools/markt.py, nie im Repo. Gebundene Stücke (isBound) stehen getrennt in «gebunden»:
-- Sie gehen nicht ins Auktionshaus, aber in ein Rezept.
local function countsText(counts)
    local ids = {}
    for id in pairs(counts) do ids[#ids + 1] = id end
    table.sort(ids)
    local parts = {}
    for i, id in ipairs(ids) do parts[i] = id .. ":" .. counts[id] end
    return table.concat(parts, ";"), #ids
end

local function planText(counts)
    local ids = {}
    for id in pairs(counts) do
        if watched(id) then ids[#ids + 1] = id end
    end
    table.sort(ids)
    local parts = {}
    for i, id in ipairs(ids) do
        local e = db.info and db.info[id]
        parts[i] = string.format("%s %d", (e and e.n) or itemLabel(id), counts[id])
    end
    return table.concat(parts, ", ")
end

local function readContainer(bag, out, outBound)
    local okN, n = pcall(C_Container.GetContainerNumSlots, bag)
    if not okN or not num(n) then return 0 end
    for slot = 1, n do
        local ok, info = pcall(C_Container.GetContainerItemInfo, bag, slot)
        if ok and type(info) == "table" and num(info.itemID) then
            local c = num(info.stackCount) or 1
            local into = (not isSecret(info.isBound) and info.isBound == true) and outBound or out
            into[info.itemID] = (into[info.itemID] or 0) + c
            local link = (type(info.hyperlink) == "string" and not isSecret(info.hyperlink)) and info.hyperlink or nil
            if link then bagLinks[info.itemID] = link end
            remember(info.itemID)
        end
    end
    return n
end

local function inventoryBags(why, ctx)
    if not bagLast or not db then return end
    local counts = {}
    for id, c in pairs(bagLast) do
        local free = c - (bagBound[id] or 0)
        if free > 0 then counts[id] = free end
    end
    local list, n = countsText(counts)
    local bound = countsText(bagBound)
    charDB().taschen = { zeit = epoch(), liste = list, gebunden = (bound ~= "") and bound or nil, geld = moneyLast }
    if not db.auto then return end
    local total = 0
    for _, v in pairs(counts) do total = total + v end
    local plan = planText(counts)
    add("INVENTAR", string.format("Taschen %s: %d Gegenstände, %d Stück%s | Geld %s", why, n, total,
        (plan ~= "") and (" | Plan: " .. plan) or "", moneyLast and money(moneyLast) or "?"), true, ctx)
end

local function readBank(why)
    if not (db and ready and C_Container and C_Container.GetContainerNumSlots) then return end
    local found = { Bank = {}, Kontobank = {} }
    local bound = { Bank = {}, Kontobank = {} }
    local slots = { Bank = 0, Kontobank = 0 }
    local BT = Enum and Enum.BankType
    if C_Bank and C_Bank.FetchPurchasedBankTabData and BT then
        for name, bankType in pairs({ Bank = BT.Character, Kontobank = BT.Account }) do
            local ok, tabs = pcall(C_Bank.FetchPurchasedBankTabData, bankType)
            if ok and type(tabs) == "table" then
                for _, tab in ipairs(tabs) do
                    if type(tab) == "table" and num(tab.ID) then
                        slots[name] = slots[name] + readContainer(tab.ID, found[name], bound[name])
                    end
                end
            end
        end
    else
        -- Rückfall: Behälter-IDs laut BagIndexConstantsDocumentation.lua (CharacterBankTab_1 bis _9)
        local BI = Enum and Enum.BagIndex
        for i = 1, 9 do
            local b = BI and BI["CharacterBankTab_" .. i]
            if b then slots.Bank = slots.Bank + readContainer(b, found.Bank, bound.Bank) end
        end
    end
    local parts = {}
    for _, name in ipairs({ "Bank", "Kontobank" }) do
        if slots[name] > 0 then
            local list, n = countsText(found[name])
            local boundList = countsText(bound[name])
            local rec = { zeit = epoch(), liste = list, gebunden = (boundList ~= "") and boundList or nil }
            if name == "Bank" then charDB().bank = rec else db.kontobank = rec end
            if bankLast[name] ~= list .. "|" .. boundList then
                bankLast[name] = list .. "|" .. boundList
                local plan = planText(found[name])
                parts[#parts + 1] = string.format("%s: %d Gegenstände%s", name, n, (plan ~= "") and (", Plan: " .. plan) or "")
            end
        end
    end
    if #parts > 0 and db.auto then add("INVENTAR", why .. " | " .. table.concat(parts, " | ")) end
end

local function scheduleBank(why)
    bankToken = bankToken + 1
    local token = bankToken
    local function run()
        if token ~= bankToken then return end
        local ok, err = pcall(readBank, why)
        if not ok then add("FEHLER", "Bank: " .. tostring(err), false) end
    end
    if C_Timer and C_Timer.After then C_Timer.After(1, run) else run() end
end

-- Version 3.6: AH-Post. Beim Öffnen des Briefkastens jeder Brief des Auktionshauses: verkauft, abgelaufen, gekauft,
-- überboten, zurückgezogen. API wie im Forever-UI 1.60.1 (Blizzard_MailFrame/MailFrame.lua): GetInboxNumItems,
-- GetInboxHeaderInfo (… Betreff, Geld, Nachnahme, Tage übrig, … , Menge und Link des ersten Anhangs), GetInboxInvoiceInfo
-- (Art «buyer», «seller» oder «seller_temp_invoice», Gegenstand, Name, Gebot, Sofortkauf, Pfand, Gebühr, …, Anzahl).
-- Das Blizzard-UI ruft vorher GetInboxText auf (markiert den Brief als gelesen), das Testlog nicht: ob die Rechnung auch
-- ohne geöffneten Brief kommt, ist ungeprüft (Test T16); sonst bleibt die Betreffzeile (Texte des Clients
-- AUCTION_SOLD_MAIL_SUBJECT usw., in Forever ungeprüft). Namen von Käufern und Verkäufern speichert das Testlog nicht.
local MAIL_KINDS = {
    { "AUCTION_SOLD_MAIL_SUBJECT", "verkauft" },
    { "AUCTION_EXPIRED_MAIL_SUBJECT", "abgelaufen" },
    { "AUCTION_WON_MAIL_SUBJECT", "gekauft" },
    { "AUCTION_OUTBID_MAIL_SUBJECT", "überboten" },
    { "AUCTION_REMOVED_MAIL_SUBJECT", "zurückgezogen" },
}
local AH_POST_KEEP = 1500     -- Einträge in KombiTestlogDB.ahPost (der älteste fällt weg)
local MAIL_MATCH = 7200       -- Sekunden: derselbe Brief, wenn sein Ablauf (aus «Tage übrig») so nah beim gespeicherten liegt

local function fmtPattern(fmt)
    if type(fmt) ~= "string" or isSecret(fmt) or not fmt:find("%s", 1, true) then return nil end
    local p = fmt:gsub("([%(%)%.%+%-%*%?%[%]%^%$%%])", "%%%1")
    p = p:gsub("%%%%s", "(.+)", 1)
    return "^" .. p .. "$"
end

local function mailKind(subject)
    if type(subject) ~= "string" or isSecret(subject) then return nil end
    for _, mk in ipairs(MAIL_KINDS) do
        local pat = fmtPattern(rawget(_G, mk[1]))
        local name = pat and subject:match(pat)
        if name then return mk[2], name end
    end
    return nil
end

local function postText(r)
    local s = (r.menge and (r.menge .. "x ") or "") .. (r.id and idLabel(r.id) or tostring(r.name or "?"))
    if r.art == "verkauft" and r.preis then
        s = s .. " für " .. money(r.preis)
        if r.menge and r.menge > 1 then s = s .. string.format(" (Stück %s)", money(math.floor(r.preis / r.menge + 0.5))) end
        if r.gebuehr then s = s .. ", Gebühr " .. money(r.gebuehr) end
        if r.vorlaeufig then s = s .. ", Geld folgt" end
    elseif r.art == "gekauft" and r.preis then
        s = s .. " für " .. money(r.preis)
    end
    return s
end

-- Denselben Brief wiederfinden: gleicher Charakter, gleiche Art, gleicher Gegenstand, gleiches Geld, Ablauf höchstens
-- MAIL_MATCH daneben (der nächste gewinnt), in diesem Durchgang noch nicht vergeben, nicht schon abgeholt. Preis und
-- Menge zählen nicht: Die Rechnung kann erst später lesbar werden (sobald der Brief einmal geöffnet war).
local function findMail(k, ablauf, used)
    local best, bestD
    for j = #db.ahPost, 1, -1 do
        local r = db.ahPost[j]
        if r.k == k and not r.weg and not used[r] then
            local d
            if r.ablauf and ablauf then
                d = math.abs(r.ablauf - ablauf)
                if d > MAIL_MATCH then d = nil end
            elseif not r.ablauf and not ablauf then
                d = 0
            end
            if d and (not bestD or d < bestD) then best, bestD = r, d end
        end
    end
    return best
end

local inboxFresh = false   -- seit dem Öffnen des Briefkastens kam MAIL_INBOX_UPDATE: Die Liste ist die des Servers

local function readInbox()
    if not db or not ready then return end
    -- nur am offenen Briefkasten: Danach kann der Client die Liste leeren, das sähe aus wie lauter abgeholte Briefe
    local open = (session and session.kind == "POST") or interacting(SESSION_INFO["POST"].itype) == true
    if not open then return end
    local okN, n, total = callApi("GetInboxNumItems")
    if not okN or not num(n) then return end
    db.ahPost = db.ahPost or {}
    local t = epoch()
    local who = charKey()
    -- vollständig: Liste vom Server, alle Briefe angezeigt (mehr als 50 zeigt der Client erst nach und nach) und lesbar
    local complete = inboxFresh and (not num(total) or total <= n)
    local used, new, filled = {}, {}, {}
    for i = 1, n do
        local okH, _, _, _, subject, mny, _, daysLeft, _, _, _, _, _, _, firstQty, firstLink = callApi("GetInboxHeaderInfo", i)
        if not okH or type(subject) ~= "string" or isSecret(subject) then complete = false end
        local kind, name
        if okH then kind, name = mailKind(subject) end
        local okI, invType, invItem, _, bid, buyout, deposit, cut, _, _, _, count = callApi("GetInboxInvoiceInfo", i)
        if not (okI and type(invType) == "string" and not isSecret(invType)) then invType = nil end
        if invType == "buyer" then
            kind = "gekauft"
        elseif invType and invType:find("seller", 1, true) then
            kind = "verkauft"
        end
        if invType and type(invItem) == "string" and not isSecret(invItem) then name = invItem end
        if okH and kind then
            local link = (type(firstLink) == "string" and not isSecret(firstLink)) and firstLink or nil
            local id = link and tonumber(link:match("item:(%d+)")) or nil
            local qty = (invType and num(count) and count > 0) and count or num(firstQty)
            if type(name) == "string" then
                local base, c = name:match("^(.-) %((%d+)%)$")   -- «Name (20)»
                if base then
                    name = base
                    qty = qty or tonumber(c)
                end
            end
            local dl = num(daysLeft)
            local ablauf = dl and math.floor(t + dl * 86400) or nil
            local k = table.concat({ who, kind, tostring(name), tostring(num(mny) or 0) }, "|")
            local rec = findMail(k, ablauf, used)
            if rec then
                used[rec] = true
                -- die Rechnung ist jetzt lesbar (Brief inzwischen geöffnet): ergänzen statt neu
                if invType and rec.preis == nil and num(bid) then
                    rec.preis, rec.sofort, rec.pfand, rec.gebuehr = num(bid), num(buyout), num(deposit), num(cut)
                    rec.menge = rec.menge or qty
                    rec.vorlaeufig = (invType == "seller_temp_invoice") or nil
                    filled[#filled + 1] = rec
                end
            else
                rec = { k = k, art = kind, name = name, id = id, menge = qty, preis = invType and num(bid) or nil,
                        sofort = invType and num(buyout) or nil, pfand = invType and num(deposit) or nil,
                        gebuehr = invType and num(cut) or nil, geld = num(mny), ablauf = ablauf, zeit = t,
                        vorlaeufig = (invType == "seller_temp_invoice") or nil }
                used[rec] = true
                if id then remember(id) end
                table.insert(db.ahPost, rec)
                new[#new + 1] = rec
            end
        end
    end
    -- Briefe dieses Charakters, die in der vollständigen Liste fehlen, sind abgeholt oder gelöscht: Ein gleicher Brief
    -- danach ist ein neuer Verkauf
    if complete then
        local prefix = who .. "|"
        for _, r in ipairs(db.ahPost) do
            if r.k and not r.weg and not used[r] and r.k:sub(1, #prefix) == prefix then r.weg = true end
        end
    end
    while #db.ahPost > AH_POST_KEEP do table.remove(db.ahPost, 1) end
    if (#new == 0 and #filled == 0) or not db.auto then return end
    local groups, order = {}, {}
    local function put(art, r)
        if not groups[art] then
            groups[art] = {}
            order[#order + 1] = art
        end
        table.insert(groups[art], postText(r))
    end
    for _, r in ipairs(new) do put(r.art, r) end
    for _, r in ipairs(filled) do put("Rechnung ergänzt", r) end
    local parts = {}
    for _, art in ipairs(order) do parts[#parts + 1] = art .. ": " .. table.concat(groups[art], ", ") end
    add("AH-POST", table.concat(parts, " | "))
end

local function scheduleInbox()
    mailToken = mailToken + 1
    local token = mailToken
    local function run()
        if token ~= mailToken then return end
        local ok, err = pcall(readInbox)
        if not ok then add("FEHLER", "AH-Post: " .. tostring(err), false) end
    end
    if C_Timer and C_Timer.After then C_Timer.After(1, run) else run() end
end

-- Version 3.6: eigene Angebote (AH-ANGEBOT). Haken an C_AuctionHouse.PostCommodity, PostItem, ConfirmPostCommodity und
-- ConfirmPostItem (so stellt das Forever-UI ein: Blizzard_AuctionHouseCommoditiesSellFrame.lua und
-- Blizzard_AuctionHouseItemSellFrame.lua; PostCommodity meldet, ob eine Bestätigung nötig ist, und das Fenster hält
-- nur ein Angebot zur Bestätigung). Bestätigt durch AUCTION_HOUSE_AUCTION_CREATED (das Forever-UI meldet damit
-- ERR_AUCTION_STARTED, Blizzard_AuctionHouseFrame.lua) oder nach 30 s, wenn weniger in den Taschen ist; verworfen bei
-- AUCTION_HOUSE_POST_ERROR und wenn ein neues Angebot kommt, während eines auf die Bestätigung wartet
-- (AUCTION_HOUSE_POST_WARNING öffnet im Forever-UI das Bestätigungsfenster). Pfand über
-- CalculateCommodityDeposit bzw. CalculateItemDeposit. Dauer 1 bis 3 wie im Verkaufsfenster (AUCTION_DURATION_ONE bis
-- _THREE). Ob ein Gegenstand mit Menge 3 drei Angebote ergibt, ist ungeprüft.
local DURATION_NAMES = { "AUCTION_DURATION_ONE", "AUCTION_DURATION_TWO", "AUCTION_DURATION_THREE" }

local function postRecord(p, how)
    db.ahPost = db.ahPost or {}
    table.insert(db.ahPost, { art = "angeboten", id = p.id, menge = p.qty, preis = p.price, je = p.per, dauer = p.duration,
                              pfand = p.deposit, zeit = epoch(), bestaetigt = how })
    while #db.ahPost > AH_POST_KEEP do table.remove(db.ahPost, 1) end
    if not db.auto then return end
    local dname = p.duration and rawget(_G, DURATION_NAMES[p.duration] or "")
    add("AH-ANGEBOT", string.format("%sx %s zu %s je %s | Dauer %s | Pfand %s | %s", tostring(p.qty or "?"),
        p.id and idLabel(p.id) or "?", p.price and money(p.price) or "?", p.per,
        (type(dname) == "string" and not isSecret(dname)) and dname or tostring(p.duration or "?"),
        p.deposit and money(p.deposit) or "?", how))
end

local function onPost(fn, item, duration, quantity, a, b)
    if not db or not ready then return end
    local commodity = (fn == "PostCommodity" or fn == "ConfirmPostCommodity")
    local okI, id = pcall(C_Item.GetItemID, item)
    id = okI and num(id) or nil
    if id then remember(id) end
    local price
    if commodity then price = num(a) else price = num(b) or num(a) end   -- Ware: Stückpreis; Gegenstand: Sofortkauf, sonst Gebot
    local okD, dep
    if commodity then
        if id then okD, dep = pcall(C_AuctionHouse.CalculateCommodityDeposit, id, duration, quantity) end
    else
        okD, dep = pcall(C_AuctionHouse.CalculateItemDeposit, item, duration, quantity)
    end
    local p = { id = id, qty = num(quantity), price = price, per = commodity and "Stück" or "Angebot", duration = num(duration),
                deposit = okD and num(dep) or nil, t = now(), before = id and itemCount(id) or nil,
                events = commodity and 1 or (num(quantity) or 1) }
    if fn == "ConfirmPostCommodity" or fn == "ConfirmPostItem" then
        for i = #postQueue, 1, -1 do
            local q = postQueue[i]
            if q.id == p.id and q.qty == p.qty and q.price == p.price and not q.confirmed then
                q.t, q.confirmed, q.awaiting = now(), true, nil   -- dasselbe Angebot, jetzt bestätigt
                return
            end
        end
        p.confirmed = true
    else
        -- Ein neues Angebot: Wartete ein älteres auf die Bestätigung, hat das Fenster es verworfen (abgebrochen).
        -- Ohne AUCTION_HOUSE_POST_WARNING im Client: unbestätigte nach 3 s ebenso. Sind dafür weniger in den Taschen,
        -- wurde es doch erstellt (Ereignis fehlte).
        for i = #postQueue, 1, -1 do
            local q = postQueue[i]
            if q.awaiting or (not postWarnings and not q.confirmed and now() - q.t > 3) then
                table.remove(postQueue, i)
                if q.id and q.before and itemCount(q.id) < q.before then postRecord(q, "Taschen weniger, ohne Bestätigung") end
            end
        end
    end
    postQueue[#postQueue + 1] = p
end

-- Antworten des Servers kommen der Reihe nach: das älteste Angebot, das nicht auf eine Bestätigung wartet
local function postOldest()
    for i, q in ipairs(postQueue) do
        if not q.awaiting then return i end
    end
    return nil
end

local function postFailed()
    local i = postOldest()
    if i then table.remove(postQueue, i) end
end

local function postTick()
    local t = now()
    while postQueue[1] and t - postQueue[1].t > 30 do
        local p = table.remove(postQueue, 1)
        if p.id and p.before and itemCount(p.id) < p.before then postRecord(p, "Taschen weniger, ohne Bestätigung") end
    end
end

-- Version 3.6: Empfehlungen anzeigen (KombiDaten: stand, zeit, markt, tipps, hinweise)
local function ageText(sec)
    if type(sec) ~= "number" or sec < 0 then return nil end
    if sec < 3600 then return math.floor(sec / 60) .. " Min" end
    if sec < 172800 then return math.floor(sec / 3600) .. " Std" end
    return math.floor(sec / 86400) .. " Tagen"
end

local function tick()
    local okA, errA = pcall(ahTick)
    if not okA then
        ahScan = nil   -- ein Fehler im AH-Scan soll nicht alle 2 Sekunden wiederkommen
        add("FEHLER", "AH-Scan: " .. tostring(errA), false)
    end
    local okP, errP = pcall(postTick)
    if not okP then
        postQueue = {}
        add("FEHLER", "AH-Angebot: " .. tostring(errP), false)
    end
    checkRXP()
    lastContext = context()
    local m = bestMap()
    if m and not (db.maps and db.maps[m]) then logMap(m) end
    local t = now()
    if pending and ((not pending.lootOpen and t - pending.tLast > 3) or t - pending.t0 > 60) then finishPending() end
    if lootRecord and t - lootRecord.t > 60 then finishLoot() end
    liveSession()
    for name, info in pairs(WINDOW_INFO) do
        local rec = windows[name]
        if rec and windowGone(rec, info) then closeWindow(name) end
    end
end

-- Fenster zum Kopieren
local frame
local function showText(text, titleText)
    if not frame then
        frame = CreateFrame("Frame", "KombiTestlogFrame", UIParent, "BasicFrameTemplateWithInset")
        frame:SetSize(780, 480)
        frame:SetPoint("CENTER")
        frame:SetMovable(true)
        frame:EnableMouse(true)
        frame:RegisterForDrag("LeftButton")
        frame:SetScript("OnDragStart", frame.StartMoving)
        frame:SetScript("OnDragStop", frame.StopMovingOrSizing)
        frame:SetFrameStrata("DIALOG")
        local title = frame.TitleText
        if type(title) ~= "table" then
            title = frame:CreateFontString(nil, "OVERLAY", "GameFontHighlight")
            title:SetPoint("TOP", 0, -5)
        end
        frame.title = title
        local scroll = CreateFrame("ScrollFrame", "KombiTestlogScroll", frame, "UIPanelScrollFrameTemplate")
        scroll:SetPoint("TOPLEFT", 12, -30)
        scroll:SetPoint("BOTTOMRIGHT", -32, 10)
        local edit = CreateFrame("EditBox", nil, scroll)
        edit:SetMultiLine(true)
        edit:SetFontObject(ChatFontNormal or GameFontHighlightSmall)
        edit:SetWidth(720)
        edit:SetAutoFocus(false)
        edit:SetScript("OnEscapePressed", function() frame:Hide() end)
        scroll:SetScrollChild(edit)
        frame.edit = edit
        if UISpecialFrames then table.insert(UISpecialFrames, "KombiTestlogFrame") end
    end
    frame.title:SetText(titleText)
    frame.edit:SetText(text)
    frame:Show()
    frame.edit:SetFocus()
    frame.edit:HighlightText()
end

local function showExport(count)
    local lines = db.log
    local first = 1
    if count and count > 0 and #lines > count then
        first = #lines - count + 1
    end
    local buf = {}
    for i = first, #lines do buf[#buf + 1] = lines[i] end
    showText(table.concat(buf, "\n"), "Testlog: Strg+A, dann Strg+C zum Kopieren")
end

-- Version 3.6: /tl tipp [Anzahl|alle]
local function showTips(arg)
    local d = tipsData()
    if not d then
        say("Keine Empfehlungen geladen. Claude schreibt sie nach der Auswertung ins Addon KombiDaten (tools/markt.py). "
            .. "Einen neuen Addon-Ordner lädt das Spiel erst nach einem Neustart, spätere Änderungen mit /reload.")
        return
    end
    local age = ageText(num(d.zeit) and (epoch() - d.zeit) or nil)
    local head = string.format("Empfehlungen vom %s%s%s", tostring(d.stand or "?"), age and (", vor " .. age) or "",
        d.markt and (" (" .. tostring(d.markt) .. ")") or "")
    if #d.tipps == 0 then
        say(head .. ": noch keine Empfehlung mit Beleg.")
        if type(d.hinweise) == "table" and d.hinweise[1] then say("Hinweis: " .. tostring(d.hinweise[1])) end
        return
    end
    if arg == "alle" then
        local buf = { head }
        for i, t in ipairs(d.tipps) do buf[#buf + 1] = i .. ". " .. tostring(t) end
        if type(d.hinweise) == "table" then
            for _, h in ipairs(d.hinweise) do buf[#buf + 1] = "Hinweis: " .. tostring(h) end
        end
        showText(table.concat(buf, "\n"), "Empfehlungen von Claude (Strg+A, Strg+C zum Kopieren)")
        return
    end
    say(head .. ":")
    local n = tonumber(arg) or 5
    for i, t in ipairs(d.tipps) do
        if i > n then
            say(string.format("… %d weitere: /tl tipp alle", #d.tipps - n))
            break
        end
        say(i .. ". " .. tostring(t))
    end
end

local function help()
    say("Befehle:")
    say("/tl <Text>  Notiz  ·  /tl bug <Text>  ·  /tl idee <Text>")
    say("/tl zeigen [alle]  Protokoll kopieren  ·  /tl status")
    say("/tl auto  automatische Einträge an/aus  ·  /tl item <Shift-Klick>  mitzählen")
    say("/tl karte  Kartengrenzen der aktuellen Karte festhalten")
    say("/tl ah  AH-Preise lesen (läuft beim Öffnen des Auktionshauses von selbst, höchstens alle 15 Min)  ·  /tl ah aus|an")
    say("/tl tipp [alle]  Empfehlungen von Claude (Addon KombiDaten)")
    say("/tl leeren ja  Protokoll löschen (AH-Scans bleiben)")
end

local function note(kind, text)
    if not text or text == "" then
        say("Bitte Text angeben, z. B. /tl bug Pfeil zeigt falsch")
        return
    end
    local extra = {}
    if UnitExists("target") then
        local n = UnitName("target")
        if n and not isSecret(n) then
            table.insert(extra, "Ziel: " .. n .. " (L" .. tostring(UnitLevel("target") or "?") .. ")")
        end
    end
    local skills = skillSummary()
    if skills ~= "" then table.insert(extra, "Berufe: " .. skills) end
    local full = text
    if #extra > 0 then full = text .. " | " .. table.concat(extra, " | ") end
    add(kind, full)
    say(kind .. " gespeichert (" .. #db.log .. " Einträge)")
end

SLASH_KOMBITESTLOG1 = "/tl"
SLASH_KOMBITESTLOG2 = "/testlog"
SlashCmdList["KOMBITESTLOG"] = function(msg)
    if not db then return end
    msg = msg or ""
    local cmd, rest = msg:match("^(%S*)%s*(.-)%s*$")
    local lower = string.lower(cmd or "")
    if lower == "" or lower == "hilfe" then
        help()
    elseif lower == "bug" then
        note("BUG", rest)
    elseif lower == "idee" then
        note("IDEE", rest)
    elseif lower == "zeigen" or lower == "liste" or lower == "list" then
        if string.lower(rest) == "alle" then showExport(0) else showExport(tonumber(rest) or 1000) end
    elseif lower == "auto" then
        db.auto = not db.auto
        say("Automatische Einträge " .. (db.auto and "an" or "aus"))
        add("EINSTELLUNG", "auto " .. (db.auto and "an" or "aus"))
    elseif lower == "item" then
        local id = tonumber(rest:match("item:(%d+)") or rest:match("^(%d+)$"))
        if id then
            db.items[id] = true
            itemLast[id] = itemCount(id)
            say("Zähle jetzt mit: " .. itemName(id) .. " (" .. id .. ")")
            add("EINSTELLUNG", "zähle " .. itemName(id) .. " (" .. id .. ")", false)
        else
            say("Gegenstand per Shift-Klick einfügen: /tl item [Gegenstand]")
        end
    elseif lower == "karte" then
        local m = bestMap()
        if m then
            logMap(m, true)
            say("Kartengrenzen für Karte " .. m .. " festgehalten")
        else
            say("Keine Karte gefunden")
        end
    elseif lower == "ah" then
        local r = string.lower(rest)
        if r == "aus" or r == "an" then
            db.ahAuto = (r == "an")
            say("AH-Scan beim Öffnen des Auktionshauses: " .. r .. (db.ahAuto and "" or " (von Hand: /tl ah)"))
            add("EINSTELLUNG", "AH-Scan automatisch " .. r, false)
        else
            ahStart(true)
        end
    elseif lower == "tipp" or lower == "tipps" then
        showTips(string.lower(rest))
    elseif lower == "status" then
        local n = 0
        for _ in pairs(db.items) do n = n + 1 end
        say(string.format("%d Einträge, automatisch %s, %d Gegenstände gezählt", #db.log, db.auto and "an" or "aus", n))
        local scans = db.ahScans or {}
        local lastScan = scans[#scans]
        say(string.format("AH-Scans: %d gespeichert%s, beim Öffnen des Auktionshauses %s", #scans,
            lastScan and (", letzter " .. tostring(lastScan.datum)) or "", (db.ahAuto == false) and "aus" or "an"))
        local c = charDB()
        local profs = {}
        for name in pairs(c.rezepte or {}) do profs[#profs + 1] = name end
        table.sort(profs)
        say(string.format("Rezepte: %s · Bank gelesen: %s · AH-Post: %d Einträge · Empfehlungen: %s",
            (#profs > 0) and table.concat(profs, ", ") or "noch keine (Berufsfenster öffnen)",
            c.bank and date("%d.%m. %H:%M", c.bank.zeit) or "noch nie (Bank öffnen)", #(db.ahPost or {}),
            tipsData() and tostring(tipsData().stand) or "keine"))
    elseif lower == "leeren" then
        if string.lower(rest) == "ja" then
            wipe(db.log)
            say("Protokoll gelöscht")
        else
            say("Zum Löschen: /tl leeren ja")
        end
    else
        note("NOTIZ", msg)
    end
end

local handlers = {}

function handlers.ADDON_LOADED(name)
    if name ~= ADDON_NAME then return end
    if type(KombiTestlogDB) ~= "table" then KombiTestlogDB = {} end
    db = KombiTestlogDB
    db.log = db.log or {}
    db.items = db.items or {}
    for _, id in ipairs(DEFAULT_ITEMS) do
        if db.items[id] == nil then db.items[id] = true end
    end
    if db.auto == nil then db.auto = true end
    if db.ahAuto == nil then db.ahAuto = true end
    db.version = VERSION
end

-- Start erst, wenn der Charakter in der Welt steht (nach dem Ladebildschirm).
-- PLAYER_LOGIN kam beim frischen Einloggen zu früh: Zone leer, Karte = Kontinent (Testlauf 1).
-- Auch 2 Sekunden nach PLAYER_ENTERING_WORLD war die Zone nach einem Neustart des Spiels noch leer
-- (Testlog 13.10. 22:07): darum warten, bis der Client eine Zone meldet, höchstens etwa 12 Sekunden.
local function beginLogging()
    snapshot()
    sessionStart()
    inventoryBags("beim Einloggen")
    local tips = tipsData()
    if tips and #tips.tipps > 0 then
        say(string.format("Empfehlungen geladen: %d Tipps vom %s. Anzeigen: /tl tipp", #tips.tipps, tostring(tips.stand or "?")))
    end
    if #missingEvents > 0 then
        table.sort(missingEvents)
        add("FEHLER", "Ereignisse unbekannt, nicht registriert: " .. table.concat(missingEvents, ", "), false)
    end
    lastContext = context()
    logMap(bestMap())
    C_Timer.NewTicker(2, function()
        local ok, err = pcall(tick)
        if not ok then add("FEHLER", "tick: " .. tostring(err), false) end
    end)
end

local function waitForZone(tries)
    local zone = GetZoneText and GetZoneText() or ""
    if (zone == nil or zone == "" or isSecret(zone)) and tries > 0 then
        C_Timer.After(1, function() waitForZone(tries - 1) end)
        return
    end
    beginLogging()
end

function handlers.PLAYER_ENTERING_WORLD()
    if started then
        -- Ladebildschirm (Ruhestein, Instanz): kein Fenster bleibt offen
        finishSession("Ladebildschirm", true)
        return
    end
    started = true
    C_Timer.After(2, function() waitForZone(10) end)
end

-- Beim Ausloggen liefert der Client Stufe-XP und Karte nicht mehr zuverlässig (Testlauf 2):
-- deshalb den zuletzt bekannten Kontext verwenden.
function handlers.PLAYER_LOGOUT()
    finishPending()
    finishLoot()
    finishSession("Ausloggen")
    if ready then inventoryBags("beim Ausloggen", lastContext) end   -- Version 3.6: letzter bekannter Taschenbestand
    add("ENDE", nil, true, lastContext)
end

function handlers.PLAYER_LEVEL_UP(level)
    if db.auto then add("STUFE", "Stufe " .. tostring(level)) end
end

function handlers.ZONE_CHANGED_NEW_AREA()
    finishSession("Gebietswechsel", true)
    if db.auto and ready then
        add("GEBIET", nil)
        logMap(bestMap())
    end
end

function handlers.QUEST_ACCEPTED(questID)
    if not db.auto then return end
    local title = C_QuestLog and C_QuestLog.GetTitleForQuestID and C_QuestLog.GetTitleForQuestID(questID)
    if title and not isSecret(title) then questTitles[questID] = title end
    add("QUEST AN", tostring(questID) .. " " .. tostring(title or ""))
end

function handlers.QUEST_TURNED_IN(questID, xpReward, moneyReward)
    windows.questDone = now()
    if not db.auto then return end
    local title = questTitles[questID]
        or (C_QuestLog and C_QuestLog.GetTitleForQuestID and C_QuestLog.GetTitleForQuestID(questID))
    if title and isSecret(title) then title = nil end
    local line = tostring(questID) .. " " .. tostring(title or "") .. " | XP " .. tostring(xpReward or 0)
    if type(moneyReward) == "number" and not isSecret(moneyReward) and moneyReward > 0 then
        line = line .. " | Geld " .. money(moneyReward)
    end
    add("QUEST AB", line)
end

function handlers.PLAYER_DEAD()
    if db.auto then add("TOD", nil) end
end

function handlers.BAG_UPDATE_DELAYED()
    local diff = bagDiff()
    local s = (not pending) and liveSession()   -- Version 3.2: nur, solange das Fenster offen ist
    local target = (pending and pending.diff) or (s and s.diff)
    if target and diff and next(diff) then
        for id, d in pairs(diff) do
            local v = (target[id] or 0) + d
            target[id] = (v ~= 0) and v or nil
        end
        if pending then pending.tLast = now() end
    end
    checkItems()
end

function handlers.SKILL_LINES_CHANGED()
    checkSkills()
end

-- Version 3: eigene Zauber
local function isFishing(id, name)
    if FISHING_IDS[id] then return true end
    return type(name) == "string" and FISHING_NAMES[string.lower(name)] == true
end

function handlers.UNIT_SPELLCAST_SUCCEEDED(unit, _, spellID)
    if isSecret(unit) or unit ~= "player" or isSecret(spellID) or not ready then return end
    local name = spellName(spellID)
    local t = now()
    lastCast = { id = spellID, name = name, t = t }
    if isFishing(spellID, name) then
        if t - fishLast > FISHING_PAUSE then fishCasts = 0 end
        fishCasts, fishLast = fishCasts + 1, t
    end
    if not db.auto then return end
    if isDisenchant(spellID, name) then
        startPending("ENTZAUBERN", spellID, name)
    elseif windows.profession then
        startPending("HERSTELLEN", spellID, name)
    end
end

function handlers.TRADE_SKILL_SHOW()
    openWindow("profession")
    scheduleRecipeDump()   -- Version 3.6
end
function handlers.TRADE_SKILL_CLOSE() closeWindow("profession") end
-- Version 3.6: Liste neu (nach dem Herstellen, Filter, anderer Beruf): Rezepte bzw. Farbwechsel
function handlers.TRADE_SKILL_LIST_UPDATE() if windows.profession then scheduleRecipeDump() end end
function handlers.TRADE_SKILL_DATA_SOURCE_CHANGED() if windows.profession then scheduleRecipeDump() end end

-- Version 3: Lootfenster
function handlers.LOOT_OPENED(_, isFromItem)
    if not ready then return end
    liveSession()   -- Version 3.2: ein schon geschlossenes Fenster beenden, bevor Beute in die Taschen kommt
    if pending and pending.kind == "ENTZAUBERN" then
        pending.lootOpen = true
        pending.tLast = now()
        return
    end
    finishLoot()
    local kind, how = "BEUTE", nil
    local src, srcType = lootSource()
    if IsFishingLoot and IsFishingLoot() then
        kind = "ANGELN"
        if fishCasts > 0 then how = "Würfe " .. fishCasts end
        fishCasts = 0
    elseif lastCast and now() - lastCast.t < 3 and (isGather(lastCast) or srcType == "GameObject") then
        kind, how = "SAMMELN", lastCast.name
    elseif srcType == "GameObject" then
        kind = "SAMMELN"
    elseif isFromItem then
        src = src or "Gegenstand"
    end
    lootRecord = { kind = kind, how = how, src = src, items = readLoot(), money = 0, t = now(), ctx = context() }
end

function handlers.LOOT_CLOSED()
    if pending and pending.lootOpen then
        pending.lootOpen = false
        pending.tLast = now()
    end
    finishLoot()
end

-- Version 3: Geld
function handlers.PLAYER_MONEY()
    local m = getMoney()
    if not m then return end
    local d = m - (moneyLast or m)
    moneyLast = m
    if d == 0 then return end
    if lootRecord then
        lootRecord.money = lootRecord.money + d
        return
    end
    local s = liveSession()   -- Version 3.2: nur, solange das Fenster offen ist
    if s then
        if d > 0 then
            s.plus, s.nPlus = s.plus + d, s.nPlus + 1
        else
            s.minus, s.nMinus = s.minus + d, s.nMinus + 1
        end
        return
    end
    if not db.auto then return end
    local ctx = moneyContext()
    if ctx == "Quest" then return end   -- steht in QUEST AB
    add("GELD", string.format("%s %s | Bestand %s", ctx, money(d, true), money(m)))
end

function handlers.MERCHANT_SHOW() startSession("HÄNDLER") end
function handlers.MERCHANT_CLOSED() finishSession("MERCHANT_CLOSED") end
function handlers.MAIL_SHOW()
    startSession("POST")
    inboxFresh = false   -- Version 3.6: bis MAIL_INBOX_UPDATE kann die Liste veraltet sein
    scheduleInbox()
end
function handlers.MAIL_CLOSED()
    finishSession("MAIL_CLOSED")
    inboxFresh = false
end
function handlers.MAIL_INBOX_UPDATE()   -- Version 3.6: AH-Post
    inboxFresh = true
    scheduleInbox()
end
-- Version 3.6: Bank (BANKFRAME_OPENED/_CLOSED laut BankDocumentation.lua, Forever-UI 1.60.1)
function handlers.BANKFRAME_OPENED() scheduleBank("Bank geöffnet") end
function handlers.BANKFRAME_CLOSED() readBank("Bank geschlossen") end
-- Version 3.6: Angebot abgelehnt bzw. Bestätigung nötig (AuctionHouseDocumentation.lua; das Forever-UI zeigt dann
-- ein Fenster, bei der Warnung mit «Annehmen» = ConfirmPost…, Blizzard_AuctionHouseFrame.lua)
function handlers.AUCTION_HOUSE_POST_ERROR() postFailed() end
function handlers.AUCTION_HOUSE_POST_WARNING()
    local q = postQueue[#postQueue]
    if q and not q.confirmed then q.awaiting = true end
end
-- Version 3.6: eigenes Angebot erstellt
function handlers.AUCTION_HOUSE_AUCTION_CREATED()
    local i = postOldest()
    if not i then return end
    local p = postQueue[i]
    p.events = p.events - 1
    if p.events <= 0 then
        table.remove(postQueue, i)
        postRecord(p, "erstellt")
    end
end
function handlers.AUCTION_HOUSE_SHOW() startSession("AUKTIONSHAUS") end
function handlers.AUCTION_HOUSE_CLOSED() finishSession("AUCTION_HOUSE_CLOSED") end

-- Version 3.5: Daten des AH-Scans sind da (kann mehrmals kommen; gelesen wird nach AH_QUIET Sekunden Ruhe)
function handlers.REPLICATE_ITEM_LIST_UPDATE()
    local s = ahScan
    if s and (s.phase == "warten" or s.phase == "daten") then
        s.phase, s.tEvent = "daten", now()
    end
end
function handlers.TRAINER_SHOW() openWindow("trainer"); scheduleTrainerDump() end
function handlers.TRAINER_UPDATE() if windows.trainer then scheduleTrainerDump() end end
function handlers.TRAINER_CLOSED() closeWindow("trainer") end
function handlers.TAXIMAP_OPENED() openWindow("taxi") end
function handlers.TAXIMAP_CLOSED() closeWindow("taxi") end
function handlers.QUEST_COMPLETE() windows.quest = true end
function handlers.QUEST_FINISHED() windows.quest = false end

-- Version 3.2: Das Forever-UI öffnet und schliesst diese Fenster über den Interaktions-Manager
-- (PlayerInteractionFrameManager.lua). Das ist ein zweiter Weg neben MAIL_CLOSED und Co.
local WINDOW_BY_ITYPE = {}
for name, info in pairs(WINDOW_INFO) do
    if not info.free then WINDOW_BY_ITYPE[info.itype] = name end
end
-- Version 3.6: Bank auch über den Interaktions-Manager (Banker 8, CharacterBanker 67, AccountBanker 68 laut
-- PlayerInteractionManagerConstantsDocumentation.lua, Forever-UI 1.60.1)
local BANK_ITYPES = { [IT.Banker or 8] = true, [IT.CharacterBanker or 67] = true, [IT.AccountBanker or 68] = true }

function handlers.PLAYER_INTERACTION_MANAGER_FRAME_SHOW(itype)
    if isSecret(itype) then return end
    local kind = KIND_BY_ITYPE[itype]
    if kind then
        startSession(kind)
    elseif session then
        -- eine andere Interaktion beendet die bisherige (z. B. Questgeber nach dem Briefkasten)
        finishSession("andere Interaktion")
    end
    if WINDOW_BY_ITYPE[itype] then openWindow(WINDOW_BY_ITYPE[itype]) end
    if WINDOW_BY_ITYPE[itype] == "trainer" then scheduleTrainerDump() end
    if BANK_ITYPES[itype] then scheduleBank("Bank geöffnet") end
end

function handlers.PLAYER_INTERACTION_MANAGER_FRAME_HIDE(itype)
    if isSecret(itype) then return end
    if session and SESSION_INFO[session.kind].itype == itype then finishSession("Interaktion zu") end
    if WINDOW_BY_ITYPE[itype] then closeWindow(WINDOW_BY_ITYPE[itype]) end
    if BANK_ITYPES[itype] then readBank("Bank geschlossen") end
end

-- Version 3: Gelerntes (Zauber beim Lehrer, Rezepte)
function handlers.LEARNED_SPELL_IN_SKILL_LINE(spellID)
    if not db.auto or not ready or isSecret(spellID) then return end
    add("GELERNT", string.format("%s (%s)", spellName(spellID) or "?", tostring(spellID)))
end

function handlers.NEW_RECIPE_LEARNED(recipeID)
    if not db.auto or not ready or isSecret(recipeID) then return end
    add("REZEPT", string.format("%s (%s)", spellName(recipeID) or "?", tostring(recipeID)))
end

-- Version 3.6: Haken für eigene Angebote (nach dem Blizzard-Aufruf, ändern nichts daran)
if type(hooksecurefunc) == "function" and type(C_AuctionHouse) == "table" then
    for _, fn in ipairs({ "PostCommodity", "ConfirmPostCommodity", "PostItem", "ConfirmPostItem" }) do
        if type(C_AuctionHouse[fn]) == "function" then
            hooksecurefunc(C_AuctionHouse, fn, function(...)
                local ok, err = pcall(onPost, fn, ...)
                if not ok and db then add("FEHLER", "AH-Angebot: " .. tostring(err), false) end
            end)
        end
    end
end

local events = CreateFrame("Frame")
for event in pairs(handlers) do
    -- Zauber nur vom eigenen Charakter: Werte anderer Einheiten können «secret» sein (Forever-API).
    -- Version 3.2: Kennt der Client ein Ereignis nicht, bricht das Laden nicht ab (Meldung als FEHLER beim Start).
    local ok
    if event == "UNIT_SPELLCAST_SUCCEEDED" and events.RegisterUnitEvent then
        ok = pcall(events.RegisterUnitEvent, events, event, "player")
    else
        ok = pcall(events.RegisterEvent, events, event)
    end
    if not ok then table.insert(missingEvents, event) end
    if ok and event == "AUCTION_HOUSE_POST_WARNING" then postWarnings = true end
end
events:SetScript("OnEvent", function(_, event, ...)
    local h = handlers[event]
    if not h then return end
    if event ~= "ADDON_LOADED" and not db then return end
    local ok, err = pcall(h, ...)
    if not ok and db then
        add("FEHLER", event .. ": " .. tostring(err), false)
    end
end)
