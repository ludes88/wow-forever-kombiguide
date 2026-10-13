-- KombiTestlog: Notizen und Testprotokoll für WoW Forever
-- Stand 13.10.2026, Version 3.1
--
--   /tl <Text>        Notiz mit Ort, Stufe, RXP-Schritt, Ziel und Berufen
--   /tl bug <Text>    Fehler festhalten
--   /tl idee <Text>   Idee festhalten
--   /tl zeigen        letzte 1000 Einträge zum Kopieren (Strg+A, Strg+C); auch /tl liste
--   /tl zeigen alle   alle Einträge
--   /tl auto          automatische Einträge an/aus
--   /tl item <Link>   Gegenstand zusätzlich mitzählen (Shift-Klick auf den Gegenstand)
--   /tl karte         Kartengrenzen der aktuellen Karte nochmals festhalten
--   /tl status        Überblick
--   /tl leeren ja     Protokoll löschen
--   /tl hilfe         diese Hilfe
--
-- Automatische Einträge (Version 3 neu: HERSTELLEN bis REZEPT):
--   SITZUNG, ENDE, GEBIET, KARTE, RXP, STUFE, TOD, QUEST AN, QUEST AB (mit Geld), BERUF, TASCHE
--   HERSTELLEN  Rezept, was verbraucht und was erhalten wurde, Berufspunkt ja/nein
--   ENTZAUBERN  welches Teil (Waffe/Rüstung, Qualität, Gegenstandsstufe) und was herauskam
--   SAMMELN     Kürschnern, Kräuter, Bergbau, Öffnen: Quelle (Kreatur- oder Objekt-ID) und Beute
--   ANGELN      Fang
--   BEUTE       Beute von Gegnern mit Geld
--   HÄNDLER     pro Händlerbesuch: verkauft, gekauft, Einnahmen, Ausgaben, Bestand
--   POST, AUKTIONSHAUS  ebenso für Briefkasten und Auktionshaus
--   GELD        übrige Geldänderungen: Lehrer, Flugmeister, sonst (Betrag und Bestand)
--   GELERNT     neuer Zauber (z. B. beim Lehrer)
--   REZEPT      neues Rezept
--
-- Gespeichert wird beim Ausloggen oder /reload in
-- WTF\Account\<KONTO>\SavedVariables\KombiTestlog.lua

local ADDON_NAME = ...
local VERSION = "3.1"
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
local windows = {}         -- offene Fenster: profession, trainer, taxi, quest

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

-- Taschen ganz lesen (Version 3): Grundlage, um Änderungen einer Handlung zuzuordnen
local function scanBags()
    if not (C_Container and C_Container.GetContainerNumSlots and C_Container.GetContainerItemInfo) then return nil end
    local counts = {}
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
                if info.hyperlink and not isSecret(info.hyperlink) then bagLinks[id] = info.hyperlink end
                if info.quality and not isSecret(info.quality) then bagQuality[id] = info.quality end
            end
        end
    end
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

local function sessionStart()
    local build = "-"
    if GetBuildInfo then
        local v, b = GetBuildInfo()
        build = tostring(v) .. " (" .. tostring(b) .. ")"
    end
    local who = (UnitName("player") or "?") .. "-" .. (GetRealmName() or "?")
    local m = getMoney()
    add("SITZUNG", string.format("%s | Client %s | RXP %s | Kombi-Test %s | Kombiguide %s | Testlog %s | Geld %s",
        who, build, addonVersion("RXPGuides"),
        guideAddon("RXPGuides_Kombi"), guideAddon("RXPGuides_KombiGuide"), VERSION, m and money(m) or "?"))
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
    local parts = {}
    if r.how then table.insert(parts, r.how) end
    table.insert(parts, r.src or "Quelle ?")
    table.insert(parts, (#r.items > 0) and table.concat(r.items, ", ") or "keine Gegenstände")
    if r.money ~= 0 then table.insert(parts, "Geld " .. money(r.money, true)) end
    add(r.kind, table.concat(parts, " | "), true, r.ctx)
end

-- Geld (Version 3): Kontext aus offenen Fenstern
local function moneyContext()
    local t = now()
    if windows.trainer then return "Lehrer" end
    if windows.taxi or (windows.taxiClosed and t - windows.taxiClosed < 2) then return "Flugmeister" end
    if windows.quest or (windows.questDone and t - windows.questDone < 2) then return "Quest" end
    return "sonst"
end

-- Händler, Post, Auktionshaus (Version 3): alles, was sich bei offenem Fenster in Taschen und Geld ändert, als eine Zeile
local SESSION_WORDS = {
    ["HÄNDLER"] = { "gekauft", "verkauft" },
    ["POST"] = { "erhalten", "verschickt" },
    ["AUKTIONSHAUS"] = { "erhalten", "abgegeben" },
}

local function finishSession()
    if not session then return end
    local s = session
    session = nil
    quietUntil = now() + 1.5
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
    local w = SESSION_WORDS[s.kind]
    local parts = {}
    if #gave > 0 then table.insert(parts, w[2] .. ": " .. table.concat(gave, ", ")) end
    if #got > 0 then table.insert(parts, w[1] .. ": " .. table.concat(got, ", ")) end
    if s.nPlus > 0 then table.insert(parts, string.format("Einnahmen %s (%d)", money(s.plus, true), s.nPlus)) end
    if s.nMinus > 0 then table.insert(parts, string.format("Ausgaben %s (%d)", money(s.minus, true), s.nMinus)) end
    local m = getMoney()
    table.insert(parts, "Bestand " .. (m and money(m) or "?"))
    add(s.kind, table.concat(parts, " | "))
end

local function startSession(kind)
    if session and session.kind == kind then return end   -- manche Fenster melden sich doppelt
    finishSession()
    session = { kind = kind, diff = {}, plus = 0, minus = 0, nPlus = 0, nMinus = 0 }
end

local function tick()
    checkRXP()
    lastContext = context()
    local m = bestMap()
    if m and not (db.maps and db.maps[m]) then logMap(m) end
    local t = now()
    if pending and ((not pending.lootOpen and t - pending.tLast > 3) or t - pending.t0 > 60) then finishPending() end
    if lootRecord and t - lootRecord.t > 60 then finishLoot() end
end

-- Fenster zum Kopieren
local frame
local function showExport(count)
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
        title:SetText("Testlog: Strg+A, dann Strg+C zum Kopieren")
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
    local lines = db.log
    local first = 1
    if count and count > 0 and #lines > count then
        first = #lines - count + 1
    end
    local buf = {}
    for i = first, #lines do buf[#buf + 1] = lines[i] end
    frame.edit:SetText(table.concat(buf, "\n"))
    frame:Show()
    frame.edit:SetFocus()
    frame.edit:HighlightText()
end

local function help()
    say("Befehle:")
    say("/tl <Text>  Notiz  ·  /tl bug <Text>  ·  /tl idee <Text>")
    say("/tl zeigen [alle]  Protokoll kopieren  ·  /tl status")
    say("/tl auto  automatische Einträge an/aus  ·  /tl item <Shift-Klick>  mitzählen")
    say("/tl karte  Kartengrenzen der aktuellen Karte festhalten")
    say("/tl leeren ja  alles löschen")
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
    elseif lower == "status" then
        local n = 0
        for _ in pairs(db.items) do n = n + 1 end
        say(string.format("%d Einträge, automatisch %s, %d Gegenstände gezählt", #db.log, db.auto and "an" or "aus", n))
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
    db.version = VERSION
end

-- Start erst, wenn der Charakter in der Welt steht (nach dem Ladebildschirm).
-- PLAYER_LOGIN kam beim frischen Einloggen zu früh: Zone leer, Karte = Kontinent (Testlauf 1).
-- Auch 2 Sekunden nach PLAYER_ENTERING_WORLD war die Zone nach einem Neustart des Spiels noch leer
-- (Testlog 13.10. 22:07): darum warten, bis der Client eine Zone meldet, höchstens etwa 12 Sekunden.
local function beginLogging()
    snapshot()
    sessionStart()
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
    if started then return end
    started = true
    C_Timer.After(2, function() waitForZone(10) end)
end

-- Beim Ausloggen liefert der Client Stufe-XP und Karte nicht mehr zuverlässig (Testlauf 2):
-- deshalb den zuletzt bekannten Kontext verwenden.
function handlers.PLAYER_LOGOUT()
    finishPending()
    finishLoot()
    finishSession()
    add("ENDE", nil, true, lastContext)
end

function handlers.PLAYER_LEVEL_UP(level)
    if db.auto then add("STUFE", "Stufe " .. tostring(level)) end
end

function handlers.ZONE_CHANGED_NEW_AREA()
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
    local target = (pending and pending.diff) or (session and session.diff)
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
function handlers.UNIT_SPELLCAST_SUCCEEDED(unit, _, spellID)
    if isSecret(unit) or unit ~= "player" or isSecret(spellID) or not ready then return end
    local name = spellName(spellID)
    lastCast = { id = spellID, name = name, t = now() }
    if not db.auto then return end
    if isDisenchant(spellID, name) then
        startPending("ENTZAUBERN", spellID, name)
    elseif windows.profession then
        startPending("HERSTELLEN", spellID, name)
    end
end

function handlers.TRADE_SKILL_SHOW() windows.profession = true end
function handlers.TRADE_SKILL_CLOSE() windows.profession = false end

-- Version 3: Lootfenster
function handlers.LOOT_OPENED(_, isFromItem)
    if not ready then return end
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
    if session then
        if d > 0 then
            session.plus, session.nPlus = session.plus + d, session.nPlus + 1
        else
            session.minus, session.nMinus = session.minus + d, session.nMinus + 1
        end
        return
    end
    if not db.auto then return end
    local ctx = moneyContext()
    if ctx == "Quest" then return end   -- steht in QUEST AB
    add("GELD", string.format("%s %s | Bestand %s", ctx, money(d, true), money(m)))
end

function handlers.MERCHANT_SHOW() startSession("HÄNDLER") end
function handlers.MERCHANT_CLOSED() finishSession() end
function handlers.MAIL_SHOW() startSession("POST") end
function handlers.MAIL_CLOSED() finishSession() end
function handlers.AUCTION_HOUSE_SHOW() startSession("AUKTIONSHAUS") end
function handlers.AUCTION_HOUSE_CLOSED() finishSession() end
function handlers.TRAINER_SHOW() windows.trainer = true end
function handlers.TRAINER_CLOSED() windows.trainer = false end
function handlers.TAXIMAP_OPENED() windows.taxi = true end
function handlers.TAXIMAP_CLOSED() windows.taxi = false; windows.taxiClosed = now() end
function handlers.QUEST_COMPLETE() windows.quest = true end
function handlers.QUEST_FINISHED() windows.quest = false end

-- Version 3: Gelerntes (Zauber beim Lehrer, Rezepte)
function handlers.LEARNED_SPELL_IN_SKILL_LINE(spellID)
    if not db.auto or not ready or isSecret(spellID) then return end
    add("GELERNT", string.format("%s (%s)", spellName(spellID) or "?", tostring(spellID)))
end

function handlers.NEW_RECIPE_LEARNED(recipeID)
    if not db.auto or not ready or isSecret(recipeID) then return end
    add("REZEPT", string.format("%s (%s)", spellName(recipeID) or "?", tostring(recipeID)))
end

local events = CreateFrame("Frame")
for event in pairs(handlers) do
    -- Zauber nur vom eigenen Charakter: Werte anderer Einheiten können «secret» sein (Forever-API)
    if event == "UNIT_SPELLCAST_SUCCEEDED" and events.RegisterUnitEvent then
        events:RegisterUnitEvent(event, "player")
    else
        events:RegisterEvent(event)
    end
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
