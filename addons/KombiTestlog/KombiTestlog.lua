-- KombiTestlog: Notizen und Testprotokoll für WoW Forever
-- Stand 13.10.2026, Version 2
--
--   /tl <Text>        Notiz mit Ort, Stufe, RXP-Schritt, Ziel und Berufen
--   /tl bug <Text>    Fehler festhalten
--   /tl idee <Text>   Idee festhalten
--   /tl zeigen        letzte 1000 Einträge zum Kopieren (Strg+A, Strg+C)
--   /tl zeigen alle   alle Einträge
--   /tl auto          automatische Einträge an/aus
--   /tl item <Link>   Gegenstand zusätzlich mitzählen (Shift-Klick auf den Gegenstand)
--   /tl karte         Kartengrenzen der aktuellen Karte nochmals festhalten
--   /tl status        Überblick
--   /tl leeren ja     Protokoll löschen
--   /tl hilfe         diese Hilfe
--
-- Gespeichert wird beim Ausloggen oder /reload in
-- WTF\Account\<KONTO>\SavedVariables\KombiTestlog.lua

local ADDON_NAME = ...
local VERSION = "2"
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

local db
local ready = false
local itemLast = {}
local skillLast = {}
local questTitles = {}
local rxpLast
local lastContext   -- letzter bekannter Kontext, für ENDE beim Ausloggen
local started = false

local function say(msg)
    DEFAULT_CHAT_FRAME:AddMessage(PREFIX .. msg)
end

local function isSecret(v)
    return issecretvalue and issecretvalue(v)
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

local rxpKey

local function snapshot()
    for id in pairs(db.items) do
        itemLast[id] = itemCount(id)
    end
    skillLast = readSkills()
    rxpLast = rxpKey()
    ready = true
end

local function checkItems()
    if not ready then return end
    local changes = {}
    local ids = {}
    for id in pairs(db.items) do table.insert(ids, id) end
    table.sort(ids)
    for _, id in ipairs(ids) do
        local now = itemCount(id)
        local before = itemLast[id] or now
        if now ~= before then
            table.insert(changes, string.format("%s %+d (%d)", itemName(id), now - before, now))
        end
        itemLast[id] = now
    end
    if #changes > 0 and db.auto then
        add("TASCHE", table.concat(changes, "; "))
    end
end

local function checkSkills()
    if not ready then return end
    local now = readSkills()
    for name, v in pairs(now) do
        local before = skillLast[name]
        if not before or before[1] ~= v[1] or before[2] ~= v[2] then
            if db.auto then
                add("BERUF", string.format("%s %d/%d", name, v[1], v[2]))
            end
        end
    end
    skillLast = now
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
    add("SITZUNG", string.format("%s | Client %s | RXP %s | Kombi-Test %s | Kombiguide %s | Testlog %s",
        who, build, addonVersion("RXPGuides"),
        guideAddon("RXPGuides_Kombi"), guideAddon("RXPGuides_KombiGuide"), VERSION))
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

local function tick()
    checkRXP()
    lastContext = context()
    local m = bestMap()
    if m and not (db.maps and db.maps[m]) then logMap(m) end
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
    elseif lower == "zeigen" then
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
function handlers.PLAYER_ENTERING_WORLD()
    if started then return end
    started = true
    C_Timer.After(2, function()
        snapshot()
        sessionStart()
        lastContext = context()
        logMap(bestMap())
        C_Timer.NewTicker(2, function()
            local ok, err = pcall(tick)
            if not ok then add("FEHLER", "tick: " .. tostring(err), false) end
        end)
    end)
end

-- Beim Ausloggen liefert der Client Stufe-XP und Karte nicht mehr zuverlässig (Testlauf 2):
-- deshalb den zuletzt bekannten Kontext verwenden.
function handlers.PLAYER_LOGOUT()
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

function handlers.QUEST_TURNED_IN(questID, xpReward)
    if not db.auto then return end
    local title = questTitles[questID]
        or (C_QuestLog and C_QuestLog.GetTitleForQuestID and C_QuestLog.GetTitleForQuestID(questID))
    if title and isSecret(title) then title = nil end
    add("QUEST AB", tostring(questID) .. " " .. tostring(title or "") .. " | XP " .. tostring(xpReward or 0))
end

function handlers.PLAYER_DEAD()
    if db.auto then add("TOD", nil) end
end

function handlers.BAG_UPDATE_DELAYED()
    checkItems()
end

function handlers.SKILL_LINES_CHANGED()
    checkSkills()
end

local events = CreateFrame("Frame")
for event in pairs(handlers) do
    events:RegisterEvent(event)
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
