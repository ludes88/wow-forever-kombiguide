# Simuliert die WoW-Umgebung grob und spielt typische Abläufe gegen KombiTestlog.lua durch
# Aufruf: python3 tools/testlog_harness.py addons/KombiTestlog/KombiTestlog.lua
# Streng: Das Addon darf keine neuen globalen Variablen anlegen (ausser den erlaubten unten).
import os, sys
from lupa import lua51

PRELUDE = r'''
messages = {}
DEFAULT_CHAT_FRAME = { AddMessage = function(self, m) table.insert(messages, m) end }
date = os.date
wipe = function(t) for k in pairs(t) do t[k] = nil end return t end
SlashCmdList = {}
UIParent = {}
UISpecialFrames = {}
ChatFontNormal = {}
GameFontHighlightSmall = {}
level = 12
UnitLevel = function(u) if u == "player" then return level end return 9 end
logout = false
UnitXP = function() if logout then return 0 end return 450 end
UnitXPMax = function() return 1000 end
npcName, npcGuid = "Kamari", "Creature-0-3110-0-12345-3365-00004A1B2C"
UnitName = function(u) if u == "player" then return "Testheld" end if u == "npc" then return npcName end return "Prairie Wolf" end
UnitGUID = function(u) if u == "npc" then return npcGuid end return nil end
-- Lehrer-API wie im Forever-UI 1.60.1 (Blizzard_TrainerUI/Mainline): Name, Art, Symbol, Stufe, Untertext, Kategorie
trainer = { trade = true, step = 2, filters = { available = true, unavailable = true, used = true }, services = {} }
GetNumTrainerServices = function() return #trainer.services end
GetTrainerServiceInfo = function(i)
  local s = trainer.services[i]
  if not s then return nil end
  return s.name, s.type, nil, s.level or 0, s.sub or "", ""
end
GetTrainerServiceSkillReq = function(i) local s = trainer.services[i] if s and s.skill then return s.skill, s.rank, true end return nil end
GetTrainerServiceCost = function(i) local s = trainer.services[i] return (s and s.cost) or 0, trainer.trade end
GetTrainerServiceTypeFilter = function(f) if trainer.filters[f] then return 1 end return nil end
GetTrainerServiceStepIndex = function() return trainer.step end
IsTradeskillTrainer = function() return trainer.trade end
GetTrainerServiceItemLink = function(i)
  local s = trainer.services[i]
  if not (s and s.item) then return nil end
  return "|cffffffff|Hitem:" .. s.item .. "::::::::12:::::|h[" .. s.name .. "]|h|r"
end
UnitExists = function(u) return u == "target" end
GetRealmName = function() return "Testrealm" end
GetBuildInfo = function() return "1.60.1", "70338" end
-- nach einem Neustart meldet der Client die Zone erst nach einigen Sekunden (Testlog 13.10. 22:07)
zoneEmpty = 2
GetZoneText = function() if zoneEmpty > 0 then zoneEmpty = zoneEmpty - 1 return "" end return "Mulgore" end
GetSubZoneText = function() return "Bloodhoof Village" end
currentMap = 1412
posX, posY = 0.468, 0.581
-- Kartenecken in Weltkoordinaten (erfundene Testwerte, nur für den Ablauf)
bounds = { [1412] = { 241.3, 2448.2, -3819.8, -3643.3 }, [1456] = { 500.0, 1000.0, -100.0, 400.0 } }
CreateVector2D = function(x, y) return { x = x, y = y, GetXY = function(self) return self.x, self.y end } end
C_Map = {
  GetBestMapForUnit = function() if logout then return nil end return currentMap end,
  GetPlayerMapPosition = function() return { GetXY = function(self) return posX, posY end } end,
  GetWorldPosFromMapPos = function(m, v)
    local b = bounds[m]
    if not b then return nil end
    return 1, CreateVector2D(b[1] + (b[3] - b[1]) * v.x, b[2] + (b[4] - b[2]) * v.y)
  end,
  GetMapWorldSize = function(m) local b = bounds[m] if not b then return 0, 0 end return math.abs(b[4] - b[2]), math.abs(b[3] - b[1]) end,
  GetMapInfo = function(m) if m == 1412 then return { name = "Mulgore" } end if m == 1456 then return { name = "Donnerfels" } end return nil end,
}
RXPCData = { currentGuideGroup = "RestedXP Forever Guide (H)", currentGuideName = "6-12 Mulgore", currentStep = 57 }
counts = { [2318] = 10, [765] = 3, [6291] = 5 }
-- Version 3: Zeit, Geld, Taschen, Zauber, Lootfenster
now_t = 1000
GetTime = function() return now_t end
money = 12345
GetMoney = function() if logout then return 0 end return money end   -- beim Ausloggen meldet der Client 0 (Testlog 13.10.)
NUM_BAG_SLOTS = 4
bags = { [0] = {
  [1] = { id = 6291, n = 5, name = "Roher glänzender Kleinfisch", q = 1 },
  [2] = { id = 6386, n = 1, name = "Gewebte Handschuhe", q = 2 },
} }
C_Container = {
  GetContainerNumSlots = function(bag) if bag == 0 then return 16 end if bags[bag] then return 28 end return 0 end,
  GetContainerItemInfo = function(bag, slot)
    local b = bags[bag]
    local it = b and b[slot]
    if not it then return nil end
    return { itemID = it.id, stackCount = it.n, quality = it.q or 1, itemName = it.name, isBound = it.bound or false,
             hyperlink = "|cff1eff00|Hitem:" .. it.id .. "::::::::12:::::|h[" .. it.name .. "]|h|r" }
  end,
}
spells = { [7751] = "Glänzender Kleinfisch", [13262] = "Entzaubern", [8613] = "Kürschnern", [7620] = "Angeln",
           [5176] = "Zorn", [5177] = "Zorn (Rang 2)", [2152] = "Leichter Rüstungssatz" }
C_Spell = { GetSpellName = function(id) return spells[id] end }
-- Name, Qualität, Gegenstandsstufe, benötigte Stufe, Klasse (4 = Rüstung, 7 = Handwerkswaren), Händlerpreis, Bindung
iteminfo = { [6386] = { "Gewebte Handschuhe", 2, 18, 13, 4 } }
loot = {}
lootsrc = nil
fishing = false
GetNumLootItems = function() return #loot end
GetLootSlotType = function(s) return loot[s] and loot[s].type or 0 end
GetLootSlotInfo = function(s)
  local l = loot[s]
  if not l then return nil end
  return 0, l.name, l.n or 0, nil, 1, false, false, nil, false, l.type == 2
end
GetLootSlotLink = function(s)
  local l = loot[s]
  if not l or l.type ~= 1 then return nil end
  return "|cffffffff|Hitem:" .. l.id .. "::::::::12:::::|h[" .. l.name .. "]|h|r"
end
GetLootSourceInfo = function(s) return lootsrc, 1 end
IsFishingLoot = function() return fishing end
-- Werte wie im Forever-UI-Code 1.60.1 (PlayerInteractionManagerConstantsDocumentation.lua)
Enum = { LootSlotType = { None = 0, Item = 1, Money = 2, Currency = 3 },
         PlayerInteractionType = { QuestGiver = 4, Merchant = 5, TaxiNode = 6, Trainer = 7, Banker = 8, MailInfo = 17,
                                   Auctioneer = 21, Professions = 59, CharacterBanker = 67, AccountBanker = 68 },
         BankType = { Character = 0, Guild = 1, Account = 2 } }
-- Version 3.2: laufende Interaktionen und Blizzard-Fenster (AuctionHouseFrame fehlt absichtlich, wie mit einem Ersatz-Addon)
interacting = {}
C_PlayerInteractionManager = { IsInteractingWithNpcOfType = function(t) return interacting[t] == true end }
local function uiFrame() return { shown = false, IsShown = function(self) return self.shown end } end
MailFrame, MerchantFrame, ClassTrainerFrame, TaxiFrame, ProfessionsFrame = uiFrame(), uiFrame(), uiFrame(), uiFrame(), uiFrame()
C_Item = {
  GetItemCount = function(id) return counts[id] or 0 end,
  GetItemNameByID = function(id) if id == 2318 then return "Leichtes Leder" end if id == 765 then return "Silberblatt" end return nil end,
  GetItemInfo = function(x)
    local id = type(x) == "number" and x or tonumber(tostring(x):match("item:(%d+)"))
    local i = iteminfo[id]
    if not i then return nil end
    return i[1], "link", i[2], i[3], i[4], "Rüstung", "Stoff", 1, "INVTYPE_HAND", 0, i[6] or 4, i[5], 1, i[7] or 0
  end,
  -- Version 3.6: ItemLocation im Test = { id = … }
  GetItemID = function(loc) return loc.id end,
  GetItemLink = function(loc) return "|cffffffff|Hitem:" .. loc.id .. "::::::::12:::::|h[x]|h|r" end,
}
-- Version 3.6: Berufsfenster (C_TradeSkillUI wie im Forever-UI 1.60.1), Werte erfunden
ts = { prof = { professionID = 2810, professionName = "Lederverarbeitung", skillLevel = 55, maxSkillLevel = 150 },
       recipes = {}, changing = false, linked = false, search = "" }
C_TradeSkillUI = {
  GetChildProfessionInfo = function() return ts.prof end,
  GetBaseProfessionInfo = function() return ts.prof end,
  GetFilteredRecipeIDs = function()   -- wie im Spiel: nur, was der Filter (hier die Suche) zeigt
    local ids = {}
    for id, r in pairs(ts.recipes) do
      if ts.search == "" or r.name:find(ts.search, 1, true) then ids[#ids + 1] = id end
    end
    table.sort(ids)
    return ids
  end,
  GetRecipeInfo = function(id)
    local r = ts.recipes[id]
    if not r then return nil end
    return { recipeID = id, name = r.name, learned = r.learned ~= false, relativeDifficulty = r.diff,
             isEnchantingRecipe = r.enchant or false, isDummyRecipe = false, isGatheringRecipe = false }
  end,
  GetRecipeSchematic = function(id, isRecraft)
    local r = ts.recipes[id]
    local slots = {}
    for i, x in ipairs(r.reag) do slots[i] = { reagents = { { itemID = x[1] } }, quantityRequired = x[2], reagentType = 1, required = true } end
    return { recipeID = id, name = r.name, quantityMin = r.qmin or 1, quantityMax = r.qmax or 1, outputItemID = r.out,
             reagentSlotSchematics = slots, isRecraft = false }
  end,
  GetRecipeOutputItemData = function(id) return { itemID = ts.recipes[id].out } end,
  IsDataSourceChanging = function() return ts.changing end,
  IsTradeSkillLinked = function() return ts.linked end,
  IsTradeSkillGuild = function() return false end,
  IsNPCCrafting = function() return false end,
  GetOnlyShowMakeableRecipes = function() return false end,
  GetOnlyShowSkillUpRecipes = function() return false end,
  GetOnlyShowFirstCraftRecipes = function() return false end,
  AreAnyInventorySlotsFiltered = function() return false end,
  AnyRecipeCategoriesFiltered = function() return false end,
  GetShowLearned = function() return true end,
  GetRecipeItemNameFilter = function() return ts.search end,
}
-- Version 3.6: Bank mit Reitern (Enum.BankType laut ItemConstantsDocumentation.lua: Character 0, Account 2)
C_Bank = { FetchPurchasedBankTabData = function(bt)
  if bt == 0 then return { { ID = 6, bankType = 0, name = "Reiter 1" } } end
  if bt == 2 then return { { ID = 15, bankType = 2, name = "Konto 1" } } end
  return {}
end }
-- Version 3.6: Briefkasten (Werte wie GetInboxHeaderInfo und GetInboxInvoiceInfo in MailFrame.lua des Forever-UI 1.60.1);
-- die Betreff-Texte hier sind Testwerte, nicht die echten des deutschen Clients
inbox = {}
GetInboxNumItems = function() return #inbox, #inbox end
GetInboxHeaderInfo = function(i)
  local m = inbox[i]
  if not m then return nil end
  return nil, nil, m.sender or "Auktionshaus", m.subject, m.money or 0, 0, m.days or 29.5, m.items, false, false, false,
         false, false, m.qty, m.link
end
GetInboxInvoiceInfo = function(i)
  local m = inbox[i]
  if not (m and m.inv) then return nil end
  local v = m.inv
  return v.type, v.item, "Kaeufername", v.bid, v.buyout, v.deposit, v.cut, 0, 0, 0, v.count, false
end
AUCTION_SOLD_MAIL_SUBJECT = "Auktion erfolgreich: %s"
AUCTION_EXPIRED_MAIL_SUBJECT = "Auktion abgelaufen: %s"
AUCTION_WON_MAIL_SUBJECT = "Auktion gewonnen: %s"
AUCTION_OUTBID_MAIL_SUBJECT = "Überboten: %s"
AUCTION_REMOVED_MAIL_SUBJECT = "Auktion abgebrochen: %s"
AUCTION_DURATION_ONE, AUCTION_DURATION_TWO, AUCTION_DURATION_THREE = "12 Std.", "24 Std.", "48 Std."
-- Version 3.6: hooksecurefunc wie im Spiel: erst das Original, dann der Haken
hooksecurefunc = function(t, name, hook)
  local orig = t[name]
  t[name] = function(...)
    local r = { orig(...) }
    hook(...)
    return unpack(r)
  end
end
skills = {
  { name = "Berufe", isHeader = true },
  { name = "Kürschnerei", rank = 10, maxRank = 75, isAbandonable = true },
  { name = "Kochen", rank = 5, maxRank = 75, isAbandonable = true },
  { name = "Waffenfertigkeiten", isHeader = true },
  { name = "Stäbe", rank = 50, maxRank = 60, isAbandonable = false },
  { name = "Fischen", rank = 1, maxRank = 75, isAbandonable = false },
  { name = "Sprachen", isHeader = true },
  { name = "Sprache: Orcisch", rank = 300, maxRank = 300, isAbandonable = false },
  { name = "Sprache: Taurisch", rank = 300, maxRank = 300, isAbandonable = false },
}
C_SkillInfo = {
  GetNumSkillLines = function() return #skills end,
  GetSkillLineInfo = function(i) return skills[i] end,
}
C_AddOns = {
  GetAddOnMetadata = function(n, k)
    if n == "RXPGuides" then return "v4.11.13" end
    if n == "RXPGuides_KombiGuide" then return "0.1.1-v4.11.13" end
    return "1"
  end,
  IsAddOnLoaded = function(n) return n == "RXPGuides_KombiGuide" end,
}
C_QuestLog = { GetTitleForQuestID = function(id) if id == 870 then return "Die Vergessenen Teiche (Test)" end return nil end }
-- Version 3.5: AH-Scan. Werte wie GetReplicateItemInfo im Forever-UI 1.60.1 (AuctionHouseDocumentation.lua):
-- Name, Symbol, Anzahl, Qualität, nutzbar, Stufe, Stufenart, Mindestgebot, Erhöhung, Sofortkauf, Gebot, Höchstbieter,
-- Bieter, Verkäufer, Verkäufer voll, Status, Item-ID, alle Infos. Index ab 0 (replicateBase = 0) oder ab 1.
time = os.time
server_t = 1792000000   -- Mitte Oktober 2026 (vor dem Start: Markt «Beta»)
GetServerTime = function() return server_t end
UnitFactionGroup = function() return "Horde", "Horde" end
GetCurrentRegionName = function() return "EU" end
auctions = {}
replicateBase = 0
replicateCalls = 0
needsConfirm = false
posted = {}
C_AuctionHouse = {
  ReplicateItems = function() replicateCalls = replicateCalls + 1 end,
  GetNumReplicateItems = function() return #auctions end,
  GetReplicateItemInfo = function(i)
    local a = auctions[i + 1 - replicateBase]
    if not a then return nil end
    return a.name, 0, a.n, 1, true, 1, "", 1, 1, a.buy, 0, nil, nil, "Verkaeufername", "Verkaeufername-Realm", 0, a.id, true
  end,
  -- Version 3.6: Restlaufzeit-Band (0 kurz … 3 sehr lang) und dessen Grenzen in Sekunden (Testwerte)
  GetReplicateItemTimeLeft = function(i) local a = auctions[i + 1 - replicateBase] return a and (a.band or 3) or 0 end,
  GetTimeLeftBandInfo = function(b)
    local t = { [0] = { 0, 1800 }, [1] = { 1800, 7200 }, [2] = { 7200, 43200 }, [3] = { 43200, 172800 } }
    return t[b][1], t[b][2]
  end,
  -- Version 3.6: Einstellen (PostCommodity meldet, ob eine Bestätigung nötig ist)
  PostCommodity = function(item, duration, quantity, unitPrice) table.insert(posted, "C") return needsConfirm end,
  ConfirmPostCommodity = function(item, duration, quantity, unitPrice) table.insert(posted, "CC") return true end,
  PostItem = function(item, duration, quantity, bid, buyout) table.insert(posted, "I") return needsConfirm end,
  ConfirmPostItem = function(item, duration, quantity, bid, buyout) table.insert(posted, "IC") return true end,
  CalculateCommodityDeposit = function(itemID, duration, quantity) return 3 * quantity * duration end,
  CalculateItemDeposit = function(item, duration, quantity) return 100 * duration end,
}
ticker = nil
C_Timer = { After = function(s, f) f() end, NewTicker = function(s, f) ticker = f return {} end }
frames = {}
unknownEvents = {}   -- Ereignisse, die der «Client» nicht kennt: RegisterEvent wirft wie im echten Spiel
local function newObj()
  local o = {}
  local mt = { __index = function(t, k) return function(...) return nil end end }
  setmetatable(o, mt)
  return o
end
CreateFrame = function(kind, name, parent, template)
  local f = { events = {}, scripts = {}, text = "", unitEvents = {} }
  function f:RegisterEvent(e)
    if unknownEvents[e] then error('Attempt to register unknown event "' .. e .. '"') end
    self.events[e] = true
  end
  function f:RegisterUnitEvent(e, ...)
    if unknownEvents[e] then error('Attempt to register unknown event "' .. e .. '"') end
    self.events[e] = true; self.unitEvents[e] = { ... }
  end
  function f:SetScript(s, fn) self.scripts[s] = fn end
  function f:SetText(t) self.text = t end
  function f:CreateFontString() local fs = newObj() fs.SetText = function(self, t) self.t = t end return fs end
  function f:StartMoving() end
  function f:StopMovingOrSizing() end
  setmetatable(f, { __index = function(t, k) return function(...) return nil end end })
  table.insert(frames, f)
  return f
end
function fire(event, ...)
  for _, f in ipairs(frames) do
    if f.events[event] and f.scripts.OnEvent then f.scripts.OnEvent(f, event, ...) end
  end
end
'''

# Ab hier dürfen nur noch diese globalen Variablen neu entstehen (Addon: SavedVariables und Slash-Befehl)
STRICT = r'''
local allowed = { SLASH_KOMBITESTLOG1 = true, SLASH_KOMBITESTLOG2 = true, KombiTestlogDB = true, ticker = true, lootsrc = true }
setmetatable(_G, { __newindex = function(t, k, v)
  if allowed[k] then rawset(t, k, v) else error("neue globale Variable: " .. tostring(k), 2) end
end })
'''

src = open(sys.argv[1], encoding="utf-8").read()

def runtime(unknown=(), pre=""):
    L = lua51.LuaRuntime(unpack_returned_tuples=True)
    L.execute(PRELUDE)
    for e in unknown:
        L.execute('unknownEvents["%s"] = true' % e)
    if pre:
        L.execute(pre)   # z. B. ein geladenes Addon KombiDaten (Version 3.6)
    L.execute(STRICT)
    chunk = L.globals().loadstring(src)
    if chunk is None:
        print("loadstring failed"); sys.exit(1)
    chunk("KombiTestlog")
    return L

L = runtime()
g = L.globals()
slash = lambda m: g.SlashCmdList["KOMBITESTLOG"](m)

g.fire("ADDON_LOADED", "KombiTestlog")
g.fire("PLAYER_ENTERING_WORLD", True, False)
g.fire("PLAYER_ENTERING_WORLD", False, False)  # zweiter Ladebildschirm: kein zweiter Start
L.execute("counts[2318] = 12")
g.fire("BAG_UPDATE_DELAYED")
L.execute("skills[2].rank = 11; skills[5].rank = 51")
g.fire("SKILL_LINES_CHANGED")
L.execute("RXPCData.currentStep = 58")
g.ticker()
g.ticker()  # unverändert: kein zweiter Eintrag
g.fire("QUEST_ACCEPTED", 870)
g.fire("QUEST_COMPLETE")
L.execute("money = money + 150")
g.fire("PLAYER_MONEY")              # Quest-Geld: steht in QUEST AB, keine GELD-Zeile
g.fire("QUEST_TURNED_IN", 870, 450, 150)
g.fire("QUEST_FINISHED")
L.execute("level = 13")
g.fire("PLAYER_LEVEL_UP", 13)
g.fire("PLAYER_DEAD")
L.execute("currentMap = 1456")
g.fire("ZONE_CHANGED_NEW_AREA")
g.ticker()  # Karte 1456 schon festgehalten: kein zweiter KARTE-Eintrag
slash("karte")  # von Hand nochmals
slash("Pfeil zeigt in den Berg")
slash("bug Schritt 12 bleibt hängen")
slash("idee Hier lohnt eine Farmrunde")
slash("item |cffffffff|Hitem:765::::::::12:::::|h[Silberblatt]|h|r")
L.execute("counts[765] = 5")
g.fire("BAG_UPDATE_DELAYED")
slash("status")
g.ticker()  # merkt sich den letzten Kontext

# --- Version 3 ---
def later(s):
    L.execute("now_t = now_t + %d" % s)
# Herstellen (Kochen): verbraucht 1 Rohfisch, ergibt 1 Kleinfisch, Kochen 5 -> 6
L.execute("ProfessionsFrame.shown = true")
g.fire("TRADE_SKILL_SHOW")
later(1)
g.fire("UNIT_SPELLCAST_SUCCEEDED", "player", "Cast-1", 7751)
L.execute("bags[0][1].n = 4; counts[6291] = 4; bags[0][3] = { id = 6290, n = 1, name = 'Glänzender Kleinfisch' }")
g.fire("BAG_UPDATE_DELAYED")
L.execute("skills[3].rank = 6")
g.fire("SKILL_LINES_CHANGED")
later(4); g.ticker()
# Zauber bei offenem Berufsfenster ohne Wirkung: keine HERSTELLEN-Zeile
g.fire("UNIT_SPELLCAST_SUCCEEDED", "player", "Cast-1b", 5176)
later(4); g.ticker()
L.execute("ProfessionsFrame.shown = false")
g.fire("TRADE_SKILL_CLOSE")
# Entzaubern mit Lootfenster: Handschuhe weg, 2 Seltsamer Staub dazu
later(10)
g.fire("UNIT_SPELLCAST_SUCCEEDED", "player", "Cast-2", 13262)
L.execute("bags[0][2] = nil")
g.fire("BAG_UPDATE_DELAYED")
L.execute("loot = { { type = 1, name = 'Seltsamer Staub', id = 10940, n = 2 } }; lootsrc = 'Item-0-0-0-0-0-000000000'")
g.fire("LOOT_OPENED", False, False)
L.execute("bags[0][4] = { id = 10940, n = 2, name = 'Seltsamer Staub' }; counts[10940] = 2")
g.fire("BAG_UPDATE_DELAYED")
g.fire("LOOT_CLOSED")
later(4); g.ticker()
# Kürschnern: Zauber, dann Lootfenster einer Kreatur
later(10)
g.fire("UNIT_SPELLCAST_SUCCEEDED", "player", "Cast-3", 8613)
later(1)
L.execute("loot = { { type = 1, name = 'Leichtes Leder', id = 2318, n = 1 }, { type = 1, name = 'Fetzen', id = 2934, n = 1 } }; lootsrc = 'Creature-0-3299-1-12345-2958-0000ABCDEF'")
g.fire("LOOT_OPENED", True, False)
L.execute("counts[2318] = counts[2318] + 1; bags[0][5] = { id = 2318, n = 1, name = 'Leichtes Leder' }")
g.fire("BAG_UPDATE_DELAYED")
g.fire("LOOT_CLOSED")
# Beute mit Geld; kurz davor ein Kampfzauber (darf nicht als Sammeln zählen); Taschen erst nach dem Schliessen
later(10)
g.fire("UNIT_SPELLCAST_SUCCEEDED", "player", "Cast-4", 5176)
later(1)
L.execute("loot = { { type = 2, name = '23 Kupfer' }, { type = 1, name = 'Sehniges Wolfsfleisch', id = 2672, n = 1 } }")
g.fire("LOOT_OPENED", True, False)
L.execute("money = money + 23")
g.fire("PLAYER_MONEY")
g.fire("LOOT_CLOSED")
L.execute("bags[0][6] = { id = 2672, n = 1, name = 'Sehniges Wolfsfleisch' }; counts[2318] = counts[2318] + 1")
g.fire("BAG_UPDATE_DELAYED")      # innerhalb 1,5 s nach dem Schliessen: keine TASCHE-Zeile
# Angeln
later(10)
g.fire("UNIT_SPELLCAST_SUCCEEDED", "player", "Cast-5", 7620)
later(12)
L.execute("fishing = true; loot = { { type = 1, name = 'Roher glänzender Kleinfisch', id = 6291, n = 1 } }; lootsrc = 'GameObject-0-3299-1-12345-35591-0000ABCDEF'")
g.fire("LOOT_OPENED", True, False)
g.fire("LOOT_CLOSED")
L.execute("fishing = false")
# Version 3.2: ein Fisch entkommt, der zweite Wurf fängt: «Würfe 2»
later(10)
g.fire("UNIT_SPELLCAST_SUCCEEDED", "player", "Cast-6", 7620)
later(20)
g.fire("UNIT_SPELLCAST_SUCCEEDED", "player", "Cast-7", 7620)
later(12)
L.execute("fishing = true; loot = { { type = 1, name = 'Roher Langzahniger Matschschnapper', id = 6289, n = 1 } }")
g.fire("LOOT_OPENED", True, False)
g.fire("LOOT_CLOSED")
L.execute("fishing = false")
# Händler: drei Verkäufe und ein Kauf werden eine Zeile (verkauft, gekauft, Einnahmen, Ausgaben)
later(10)
L.execute("MerchantFrame.shown = true")
g.fire("MERCHANT_SHOW")
g.fire("MERCHANT_SHOW")           # doppelt gemeldet: keine zweite Sitzung
L.execute("money = money + 15; bags[0][6] = nil")
g.fire("PLAYER_MONEY"); g.fire("BAG_UPDATE_DELAYED")
for d in (30, 7):
    L.execute("money = money + %d" % d)
    g.fire("PLAYER_MONEY")
L.execute("money = money - 50; bags[0][7] = { id = 2320, n = 5, name = 'Grobes Garn' }")
g.fire("PLAYER_MONEY"); g.fire("BAG_UPDATE_DELAYED")
L.execute("MerchantFrame.shown = false")
g.fire("MERCHANT_CLOSED")
g.fire("MERCHANT_CLOSED")         # doppelt gemeldet: keine zweite Zeile
# Post: Geld aus einem Verkauf und Leder aus einem Brief
later(10)
L.execute("MailFrame.shown = true")
g.fire("MAIL_SHOW")
L.execute("money = money + 10000")
g.fire("PLAYER_MONEY")
L.execute("bags[0][8] = { id = 2319, n = 20, name = 'Mittleres Leder' }")
g.fire("BAG_UPDATE_DELAYED")
L.execute("MailFrame.shown = false")
g.fire("MAIL_CLOSED")
# Lehrer: Kosten und gelernter Zauber; Version 3.4: Lehrerliste (Berufslehrer, Rang an Stelle 2, Überschrift fällt weg)
L.execute("""trainer.services = {
  { name = "Lederverarbeitung", type = "header" },
  { name = "Lederverarbeitung", sub = "Geselle", type = "available", level = 10, skill = "Lederverarbeitung", rank = 50, cost = 500 },
  { name = "Leichtes Leder", type = "used", cost = 0 },
  { name = "Geprägte Lederhandschuhe", type = "unavailable", skill = "Lederverarbeitung", rank = 30, cost = 150, item = 4239 },
}""")
L.execute("ClassTrainerFrame.shown = true")
g.fire("TRAINER_SHOW")
L.execute("money = money - 100")
g.fire("PLAYER_MONEY")
g.fire("LEARNED_SPELL_IN_SKILL_LINE", 5177, 1, False)
g.fire("TRAINER_UPDATE")            # gleiche Liste: keine zweite LEHRER-Zeile
L.execute("ClassTrainerFrame.shown = false")
g.fire("TRAINER_CLOSED")
g.fire("NEW_RECIPE_LEARNED", 2152)
L.execute("ClassTrainerFrame.shown = true")
g.fire("TRAINER_SHOW")              # derselbe Lehrer nochmals: keine neue Zeile
L.execute("ClassTrainerFrame.shown = false")
g.fire("TRAINER_CLOSED")
g.fire("TRAINER_UPDATE")            # Fenster zu: nichts

# --- Version 3.2: Fenster enden auch ohne CLOSED-Ereignis ---
# A: Briefkasten zu, aber MAIL_CLOSED kommt nicht (Testlog 13.10. 22:26); danach Beute: gehört nicht zur Post
later(10)
L.execute("MailFrame.shown = true")
g.fire("MAIL_SHOW")
L.execute("bags[0][9] = { id = 4306, n = 2, name = 'Seidenstoff' }")
g.fire("BAG_UPDATE_DELAYED")
later(1)
L.execute("MailFrame.shown = false")
later(3)
L.execute("loot = { { type = 1, name = 'Ebenenschreiterkralle', id = 4759, n = 1 } }; lootsrc = 'Creature-0-3299-1-12345-2956-0000ABCDEF'")
g.fire("LOOT_OPENED", True, False)
L.execute("bags[0][10] = { id = 4759, n = 1, name = 'Ebenenschreiterkralle' }")
g.fire("BAG_UPDATE_DELAYED")
g.fire("LOOT_CLOSED")
# B: Händler nur über den Interaktions-Manager (kein MERCHANT_SHOW/CLOSED), Tick bei offenem Fenster
later(10)
L.execute("MerchantFrame.shown = true; interacting[5] = true")
g.fire("PLAYER_INTERACTION_MANAGER_FRAME_SHOW", 5)
L.execute("money = money + 40; bags[0][10] = nil")
g.fire("PLAYER_MONEY"); g.fire("BAG_UPDATE_DELAYED")
later(3); g.ticker()
L.execute("MerchantFrame.shown = false; interacting[5] = false")
g.fire("PLAYER_INTERACTION_MANAGER_FRAME_HIDE", 5)
# C: Auktionshaus ohne Blizzard-Fenster (Ersatz-Addon), Interaktion läuft; Ende, weil der Charakter weggeht
later(10)
L.execute("interacting[21] = true")
g.fire("AUCTION_HOUSE_SHOW")
L.execute("money = money - 2500; bags[0][11] = { id = 2321, n = 1, name = 'Feines Garn' }")
g.fire("PLAYER_MONEY"); g.fire("BAG_UPDATE_DELAYED")
later(3); g.ticker()
L.execute("posX = posX + 0.1")    # Karte 1456 im Test: 600 Yards breit, also 60 Yards weiter
later(2); g.ticker()
L.execute("interacting[21] = false; posX = 0.468")
# D: Gebietswechsel beendet eine Händlersitzung
later(10)
L.execute("MerchantFrame.shown = true")
g.fire("MERCHANT_SHOW")
L.execute("money = money - 7")
g.fire("PLAYER_MONEY")
g.fire("ZONE_CHANGED_NEW_AREA")
L.execute("MerchantFrame.shown = false")
# E: Briefkasten, dann ein Questgeber: andere Interaktion beendet die Post
later(10)
L.execute("MailFrame.shown = true; interacting[17] = true")
g.fire("MAIL_SHOW")
L.execute("bags[0][12] = { id = 2592, n = 5, name = 'Wollstoff' }")
g.fire("BAG_UPDATE_DELAYED")
g.fire("PLAYER_INTERACTION_MANAGER_FRAME_SHOW", 4)
L.execute("MailFrame.shown = false; interacting[17] = false")
# F: leeres Lootfenster ohne Quelle (vor dem Kürschnern): keine Zeile; mit Quelle: Zeile
later(10)
L.execute("loot = {}; lootsrc = nil")
g.fire("LOOT_OPENED", True, False); g.fire("LOOT_CLOSED")
L.execute("lootsrc = 'Creature-0-3299-1-12345-2958-0000ABCDEF'")
g.fire("LOOT_OPENED", True, False); g.fire("LOOT_CLOSED")
# G: Lehrerfenster zu, aber TRAINER_CLOSED fehlt: danach ist Geld wieder «sonst»
# (Version 3.4: dabei ein Klassenlehrer mit Filter ohne «nicht verfügbar»)
later(10)
L.execute("""npcName, npcGuid = "Gennia Runetotem", "Creature-0-3110-0-12345-3060-00004A1B2D"
trainer.trade, trainer.step = false, nil
trainer.filters.unavailable = false
trainer.services = { { name = "Zorn", sub = "Rang 3", type = "available", level = 14, cost = 900 } }""")
L.execute("ClassTrainerFrame.shown = true")
g.fire("TRAINER_SHOW")
L.execute("money = money - 300")
g.fire("PLAYER_MONEY")
L.execute("ClassTrainerFrame.shown = false")
later(3); g.ticker()
L.execute("money = money + 5")
g.fire("PLAYER_MONEY")
# H: Flug: die Kosten kommen kurz nach dem Schliessen der Flugkarte
later(10)
L.execute("TaxiFrame.shown = true")
g.fire("TAXIMAP_OPENED")
L.execute("TaxiFrame.shown = false")
g.fire("TAXIMAP_CLOSED")
later(1)
L.execute("money = money - 95")
g.fire("PLAYER_MONEY")
later(10); g.ticker()
# J: AH-Scan (Version 3.5). Der Versuch aus C bekam keine Daten: Abbruch nach 120 s
later(121); g.ticker()
calls_c = g.replicateCalls
L.execute("server_t = server_t + 1000")      # über 15 Minuten nach dem Versuch aus C
L.execute("""auctions = {
  { id = 2318, n = 20, buy = 960, name = 'Leichtes Leder' },
  { id = 2318, n = 5, buy = 260, name = 'Leichtes Leder' },
  { id = 2318, n = 20, buy = 1100, name = 'Leichtes Leder' },
  { id = 2319, n = 10, buy = 0, name = 'Mittleres Leder' },
  { id = 2319, n = 4, buy = 800, name = 'Mittleres Leder' },
  { id = 4306, n = 10, buy = 5000, name = 'Seidenstoff' },
}""")
L.execute("interacting[21] = true")
g.fire("AUCTION_HOUSE_SHOW")
later(2); g.ticker()                         # startet von selbst
calls_auto = g.replicateCalls
g.fire("REPLICATE_ITEM_LIST_UPDATE")
later(1); g.ticker()                         # noch keine 2 s Ruhe: wartet
g.fire("REPLICATE_ITEM_LIST_UPDATE")         # kommt nochmals
later(1); g.ticker()
later(2); g.ticker()                         # jetzt lesen
L.execute("interacting[21] = false")
g.fire("AUCTION_HOUSE_CLOSED")
later(5)
L.execute("interacting[21] = true; server_t = server_t + 300")   # 5 Minuten später nochmals: kein neuer Scan
g.fire("AUCTION_HOUSE_SHOW")
later(2); g.ticker()
calls_again = g.replicateCalls
slash("ah")                                  # von Hand: versucht es trotzdem, der Server antwortet nicht
later(121); g.ticker()
calls_manual = g.replicateCalls
L.execute("interacting[21] = false")
g.fire("AUCTION_HOUSE_CLOSED")
slash("ah aus")
L.execute("interacting[21] = true; server_t = server_t + 2000")
g.fire("AUCTION_HOUSE_SHOW")
later(2); g.ticker()
calls_off = g.replicateCalls
L.execute("interacting[21] = false")
g.fire("AUCTION_HOUSE_CLOSED")
slash("ah an")
later(3); g.ticker()
slash("ah")                                  # Auktionshaus zu: nur Hinweis
slash("status")
# I: Briefkasten offen beim Ausloggen: Bestand aus dem letzten bekannten Wert, nicht 0
L.execute("MailFrame.shown = true")
g.fire("MAIL_SHOW")
L.execute("money = money + 405")
g.fire("PLAYER_MONEY")
L.execute("logout = true")
g.fire("PLAYER_LOGOUT")
L.execute("logout = false")
slash("liste")                  # Kurzform für zeigen, keine Notiz
slash("zeigen")
slash("leeren")
db = g.KombiTestlogDB
log = db.log
print("=== Protokoll (%d Einträge) ===" % len(log))
for i in range(1, len(log) + 1):
    print(log[i])
print("=== Chat ===")
msgs = g.messages
for i in range(1, len(msgs) + 1):
    print(msgs[i])
exp = [f for f in g.frames.values() if f.text]
print("=== Exportfenster: %d Zeichen, %d Zeilen ===" % (len(exp[0].text), exp[0].text.count("\n") + 1) if exp else "kein Export")
lines = [log[i] for i in range(1, len(log) + 1)]
# Version 3.5: SavedVariables-Datei nachbauen, so wie der Client sie schreibt (für tools/ah_aus_testlog.py)
SERIALIZE = r'''
return function(name, v)
  local out = {}
  local function key(k)
    if type(k) == "number" then return "[" .. k .. "]" end
    return "[" .. string.format("%q", k) .. "]"
  end
  local function ser(x, ind)
    if type(x) == "table" then
      local ks = {}
      for k in pairs(x) do ks[#ks + 1] = k end
      table.sort(ks, function(a, b) return tostring(a) < tostring(b) end)
      local s = "{\n"
      for _, k in ipairs(ks) do s = s .. ind .. "\t" .. key(k) .. " = " .. ser(x[k], ind .. "\t") .. ",\n" end
      return s .. ind .. "}"
    elseif type(x) == "string" then return string.format("%q", x)
    else return tostring(x) end
  end
  return name .. " = " .. ser(v, "") .. "\n"
end
'''
sv_text = L.execute(SERIALIZE)("KombiTestlogDB", db)
before = len(db.log)
slash("leeren ja")
print("nach 'leeren ja':", len(db.log), "vorher", before)

# Prüfungen
fails = []
def check(cond, text):
    if not cond: fails.append(text)
# Gleichnamige lokale Funktionen überdecken sich in Lua still (13.10.: startSession zweimal)
import re as _re
_names = _re.findall(r"^local function (\w+)", src, _re.M)
_dups = sorted({n for n in _names if _names.count(n) > 1})
check(not _dups, "keine doppelten lokalen Funktionsnamen (%s)" % ", ".join(_dups))
kinds = [l.split(" | ")[1] for l in lines]
check(kinds.count("SITZUNG") == 1, "genau eine SITZUNG")
check(g.zoneEmpty == 0, "Start wartet, bis der Client eine Zone meldet")
check(not any(" | NOTIZ | " in l and "liste" in l for l in lines), "/tl liste öffnet das Protokoll statt einer Notiz")
sitz = next(l for l in lines if " | SITZUNG | " in l)
check("Mulgore" in sitz and "1412 46.8,58.1" in sitz, "SITZUNG mit Ort und Karte")
check("Kombiguide 0.1.1-v4.11.13" in sitz and "Kombi-Test nicht geladen" in sitz, "SITZUNG meldet beide Guide-Addons")
karten = [l for l in lines if " | KARTE | " in l]
check(len(karten) == 3, "KARTE: 1412 beim Start, 1456 beim Gebietswechsel, 1456 von Hand (%d)" % len(karten))
check(all("keine Weltkoordinaten" not in l for l in karten), "KARTE mit Weltkoordinaten")
check("0,0 = 241.30, 2448.20" in karten[0] and "Grösse" in karten[0], "KARTE-Werte 1412")
check(all("Sprache" not in l for l in lines), "keine Sprachen in Berufslisten")
check(any(" | BERUF | " in l and "Kürschnerei 11/75" in l for l in lines), "BERUF Kürschnerei 11/75")
ende = next(l for l in lines if " | ENDE | " in l)
check(" L13 45% " in ende and "1456 46.8,58.1" in ende, "ENDE mit letztem bekanntem Kontext")
check(not any(" | FEHLER | " in l for l in lines), "keine FEHLER")
check(isinstance(db.maps[1412].x0, float) or db.maps[1412].x0 is not None, "db.maps gespeichert")
check(L.eval("(function() for _, f in ipairs(frames) do if f.unitEvents.UNIT_SPELLCAST_SUCCEEDED then return f.unitEvents.UNIT_SPELLCAST_SUCCEEDED[1] end end end)()") == "player",
      "UNIT_SPELLCAST_SUCCEEDED nur für den eigenen Charakter registriert")
# Version 3
def one(kind, *parts):
    hits = [l for l in lines if (" | %s | " % kind) in l and all(p in l for p in parts)]
    check(len(hits) == 1, "%s mit %s (%d Treffer)" % (kind, ", ".join(parts), len(hits)))
check("| Geld 1g 23s 45c" in sitz, "SITZUNG mit Geldbestand")
one("QUEST AB", "870", "XP 450", "Geld 1s 50c")
check(not any(" | GELD | " in l and "Quest" in l for l in lines), "Quest-Geld nicht doppelt als GELD")
one("HERSTELLEN", "Glänzender Kleinfisch (7751)", "verbraucht: 1x Roher glänzender Kleinfisch",
    "erhalten: 1x Glänzender Kleinfisch (6290)", "Punkt: Kochen 5 -> 6")
check(not any(" | HERSTELLEN | " in l and "Zorn" in l for l in lines), "kein HERSTELLEN für einen Zauber ohne Wirkung")
check(not any(" | TASCHE | " in l and ("Item 6291" in l or "Item 10940" in l) for l in lines),
      "keine TASCHE-Zeile für Änderungen, die schon in einer Handlung stehen")
one("ENTZAUBERN", "Gewebte Handschuhe (6386) [Rüstung, grün, Gegenstandsstufe 18, ab Stufe 13]",
    "Ergebnis: 2x Seltsamer Staub (10940)", "kein Punkt")
one("SAMMELN", "Kürschnern", "Kreatur 2958", "1x Leichtes Leder (2318), 1x Fetzen (2934)")
one("BEUTE", "Kreatur 2958", "1x Sehniges Wolfsfleisch (2672)", "Geld +23c")
check(sum(1 for l in lines if " | TASCHE | " in l and "Leichtes Leder" in l) == 1,
      "TASCHE für Leichtes Leder nur vor Version-3-Abläufen (Loot steht in SAMMELN/BEUTE)")
one("ANGELN", "Objekt 35591", "1x Roher glänzender Kleinfisch (6291)")
one("HÄNDLER", "verkauft: 1x Sehniges Wolfsfleisch (2672)", "gekauft: 5x Grobes Garn (2320)",
    "Einnahmen +52c (3)", "Ausgaben -50c (1)")
one("POST", "erhalten: 20x Mittleres Leder (2319)", "Einnahmen +1g (1)")
check(not any(" | GELD | " in l and ("Händler" in l or "Post" in l) for l in lines), "Händler und Post nicht doppelt als GELD")
one("GELD", "Lehrer -1s")
one("GELERNT", "Zorn (Rang 2) (5177)")
one("REZEPT", "Leichter Rüstungssatz (2152)")
# Version 3.2
one("ANGELN", "Würfe 1", "1x Roher glänzender Kleinfisch (6291)")
one("ANGELN", "Würfe 2", "1x Roher Langzahniger Matschschnapper (6289)")
one("HÄNDLER", "verkauft: 1x Sehniges Wolfsfleisch (2672)", "Dauer 0 s, Ende MERCHANT_CLOSED")
one("POST", "erhalten: 20x Mittleres Leder (2319)", "Ende MAIL_CLOSED")
one("POST", "erhalten: 2x Seidenstoff (4306)", "Dauer 4 s, Ende Fenster zu")
check(not any(" | POST | " in l and "Ebenenschreiterkralle" in l for l in lines), "Beute nach dem Briefkasten gehört nicht zur Post")
one("BEUTE", "Kreatur 2956", "1x Ebenenschreiterkralle (4759)")
one("HÄNDLER", "verkauft: 1x Ebenenschreiterkralle (4759)", "Einnahmen +40c (1)", "Dauer 3 s, Ende Interaktion zu")
one("AUKTIONSHAUS", "erhalten: 1x Feines Garn (2321)", "Ausgaben -25s (1)", "Ende entfernt")
one("HÄNDLER", "Ausgaben -7c (1)", "Ende Gebietswechsel")
one("POST", "erhalten: 5x Wollstoff (2592)", "Ende andere Interaktion")
check(not any("Quelle ? | keine Gegenstände" in l for l in lines), "leeres Lootfenster ohne Quelle: keine Zeile")
one("BEUTE", "Kreatur 2958 | keine Gegenstände")
one("GELD", "Lehrer -3s")
one("GELD", "sonst +5c")
one("GELD", "Flugmeister -95c")
one("POST", "Einnahmen +4s 5c (1)", "Bestand 1g 99s 68c", "Ende Ausloggen")
# Version 3.4: Lehrerliste
check(sum(1 for l in lines if " | LEHRER | " in l) == 2, "zwei LEHRER-Zeilen (Berufslehrer einmal, Klassenlehrer einmal)")
one("LEHRER", "Kamari (Kreatur 3365) | Beruf | Filter lernbar+gesperrt+gelernt | 3 Einträge",
    "Lederverarbeitung [Geselle] (Rang) lernbar, ab Stufe 10 und Lederverarbeitung 50, 5s",
    "Leichtes Leder gelernt, kostenlos", "Geprägte Lederhandschuhe (Item 4239) gesperrt, ab Lederverarbeitung 30, 1s 50c")
one("LEHRER", "Gennia Runetotem (Kreatur 3060) | Klasse | Filter lernbar+gelernt | 1 Eintrag", "Zorn [Rang 3] lernbar, ab Stufe 14, 9s")
# Version 3.5: AH-Scan
ah = [l for l in lines if " | AH-SCAN | " in l]
check(len(ah) == 3, "drei AH-SCAN-Zeilen: Abbruch aus C, Scan, Abbruch von Hand (%d)" % len(ah))
check(sum(1 for l in ah if "abgebrochen: kein Ergebnis nach 120 s" in l) == 2, "zwei Abbrüche ohne Ergebnis nach 120 s")
check(calls_auto == calls_c + 1, "AH-Scan startet beim Öffnen des Auktionshauses von selbst")
check(calls_again == calls_auto, "kein zweiter automatischer Scan innerhalb von 15 Minuten")
check(calls_manual == calls_again + 1, "/tl ah versucht es auch innerhalb von 15 Minuten")
check(calls_off == calls_manual, "/tl ah aus: kein automatischer Scan")
one("AH-SCAN", "| EU Horde | Realm Testrealm | 6 Angebote, 3 Gegenstände, 1 nur mit Gebot, 4 s |",
    "Tiefstpreis / Median / Stück: Leichtes Leder (2318) 48c / 52c / 45; 2319 2s / 2s / 4")
check(not any(" | AH-SCAN | " in l and "4306" in l for l in lines), "AH-SCAN-Zeile nur mit Plan-Gegenständen")
scans = db.ahScans
check(scans is not None and len(scans) == 1, "ein Scan gespeichert")
s1 = scans[1] if scans is not None and len(scans) >= 1 else None
if s1 is not None:
    # alle Rohwerte 3: ob 0–3 oder 1–4 gezählt wird, ist nicht zu erkennen -> lang und sehr lang bleiben 0
    check(s1.stufen[2318] == "48*20*0*0,52*5*0*0,55*20*0*0", "Preisstufen Leichtes Leder, Restlaufzeit unklar (%s)" % s1.stufen[2318])
    check(s1.stufen[2319] == "200*4*0*0", "Preisstufen Mittleres Leder ohne Angebot nur mit Gebot (%s)" % s1.stufen[2319])
    check(s1.bandRoh == "3-3" and s1.bandVersatz is None, "Rohwerte der Restlaufzeit gespeichert, Versatz unklar (%s, %s)" % (s1.bandRoh, s1.bandVersatz))
    check(s1.baender == "0:0-1800;1:1800-7200;2:7200-43200;3:43200-172800", "Grenzen der Restlaufzeit-Bänder (%s)" % s1.baender)
    check(s1.abnahme is None, "erster Scan: keine Abnahme")
    check(s1.stufen[4306] is None, "keine Preisstufen für Gegenstände ausserhalb des Plans")
    check(s1.alle == "2318:48:52:45:3;2319:200:200:4:1;4306:500:500:10:1", "alle Gegenstände kompakt (%s)" % s1.alle)
    check(s1.plan == "2318:48:52:45:3;2319:200:200:4:1", "Plan-Gegenstände kompakt (%s)" % s1.plan)
    check((s1.realm, s1.fraktion, s1.region, s1.angebote, s1.nurGebot) == ("Testrealm", "Horde", "EU", 6, 1), "Kopf des Scans")
check(len(g.KombiTestlogDB.ahScans) == 1, "/tl leeren ja lässt die AH-Scans stehen")
check("Verkaeufername" not in sv_text, "keine Verkäufernamen gespeichert")
check(any("Leichtes Leder: Tiefstpreis 48c, Median 52c, 45 Stück" in m for m in [msgs[i] for i in range(1, len(msgs) + 1)]),
      "Chatmeldung nach dem Scan")
check(any("Bitte zuerst das Auktionshaus öffnen" in m for m in [msgs[i] for i in range(1, len(msgs) + 1)]),
      "/tl ah bei geschlossenem Auktionshaus: Hinweis")
check(any("AH-Scan übersprungen: letzter Versuch vor 5 Min" in m for m in [msgs[i] for i in range(1, len(msgs) + 1)]),
      "übersprungener automatischer Scan wird gemeldet")
# Index ab 1 statt ab 0: wird erkannt
L3 = runtime()
g3 = L3.globals()
g3.fire("ADDON_LOADED", "KombiTestlog")
g3.fire("PLAYER_ENTERING_WORLD", True, False)
L3.execute("replicateBase = 1; interacting[21] = true; auctions = { { id = 2318, n = 2, buy = 100, name = 'x' }, { id = 2318, n = 1, buy = 70, name = 'x' } }")
g3.fire("AUCTION_HOUSE_SHOW")
L3.execute("now_t = now_t + 2"); g3.ticker()
g3.fire("REPLICATE_ITEM_LIST_UPDATE")
L3.execute("now_t = now_t + 3"); g3.ticker()
sc3 = g3.KombiTestlogDB.ahScans
check(sc3 is not None and sc3[1].alle == "2318:50:50:3:2", "Index ab 1 erkannt (%s)" % (sc3 and sc3[1].alle))
# Viele Scans: höchstens 60, nur die 10 neuesten mit allen Gegenständen und Preisstufen
for _ in range(64):
    L3.execute("server_t = server_t + 1000; interacting[21] = false")
    g3.fire("AUCTION_HOUSE_CLOSED")
    L3.execute("interacting[21] = true")
    g3.fire("AUCTION_HOUSE_SHOW")
    L3.execute("now_t = now_t + 2"); g3.ticker()
    g3.fire("REPLICATE_ITEM_LIST_UPDATE")
    L3.execute("now_t = now_t + 3"); g3.ticker()
sc3 = g3.KombiTestlogDB.ahScans
voll = [i for i in range(1, len(sc3) + 1) if sc3[i].alle is not None]
check(len(sc3) == 60 and voll == list(range(51, 61)) and sc3[1].plan == "2318:50:50:3:2" and sc3[1].stufen is None,
      "höchstens 60 Scans, die 10 neuesten vollständig (%d Scans, vollständig %s)" % (len(sc3), voll[:3]))
# Das Ereignis wird nie ruhig: nach 120 s wird trotzdem gelesen
L3.execute("server_t = server_t + 1000; interacting[21] = false")
g3.fire("AUCTION_HOUSE_CLOSED")
L3.execute("interacting[21] = true; auctions = { { id = 2318, n = 1, buy = 77, name = 'x' } }")
g3.fire("AUCTION_HOUSE_SHOW")
L3.execute("now_t = now_t + 2"); g3.ticker()
for _ in range(90):
    g3.fire("REPLICATE_ITEM_LIST_UPDATE")
    L3.execute("now_t = now_t + 1.5"); g3.ticker()
sc3 = g3.KombiTestlogDB.ahScans
check(sc3[len(sc3)].alle == "2318:77:77:1:1", "liest nach 120 s auch ohne ruhiges Ereignis (%s)" % sc3[len(sc3)].alle)
# --- Version 3.6: Rezepte, Bestand, AH-Post, eigene Angebote, Abnahme, Empfehlungen ---
L4 = runtime()
g4 = L4.globals()
slash4 = lambda m: g4.SlashCmdList["KOMBITESTLOG"](m)
def later4(s):
    L4.execute("now_t = now_t + %d" % s)
L4.execute("""
iteminfo[2318] = { "Leichtes Leder", 1, 10, 0, 7, 15 }
iteminfo[2934] = { "Fetzen", 0, 5, 0, 7, 1 }
iteminfo[2304] = { "Leichter Rüstungssatz", 1, 5, 1, 0, 6 }
iteminfo[783] = { "Leichter Balg", 1, 10, 0, 7, 10 }
iteminfo[4289] = { "Salz", 1, 5, 0, 7, 12 }
iteminfo[4231] = { "Geschmeidiger leichter Balg", 1, 10, 0, 7, 50 }
iteminfo[10940] = { "Seltsamer Staub", 1, 10, 0, 7, 25 }
iteminfo[2319] = { "Mittleres Leder", 1, 15, 0, 7, 25 }
iteminfo[6291] = { "Roher glänzender Kleinfisch", 1, 5, 0, 0, 2 }
iteminfo[6522] = { "Deviatfisch", 1, 18, 0, 0, 10 }
-- Zeit der Protokollzeilen folgt der Testuhr (für den Wert pro Stunde in tools/markt.py)
date = function(f, t) return os.date(f, t or (server_t + now_t - 1000)) end
ts.recipes = {
  [2881] = { name = "Leichtes Leder", reag = { { 2934, 3 } }, out = 2318, diff = 3 },
  [2152] = { name = "Leichter Rüstungssatz", reag = { { 2318, 1 } }, out = 2304, diff = 1 },
  [3816] = { name = "Geschmeidiger leichter Balg", reag = { { 783, 1 }, { 4289, 1 } }, out = 4231, diff = 0 },
  [2153] = { name = "Handgenähte Lederstiefel", reag = { { 2318, 2 } }, out = 2302, diff = 0, learned = false },
}
""")
g4.fire("ADDON_LOADED", "KombiTestlog")
g4.fire("PLAYER_ENTERING_WORLD", True, False)
# Berufsfenster: alle gelernten Rezepte; danach nur Farbwechsel; fremde Liste (verlinkt): nichts
L4.execute("ProfessionsFrame.shown = true")
g4.fire("TRADE_SKILL_SHOW")
L4.execute("ts.recipes[2152].diff = 2; ts.prof.skillLevel = 61")
g4.fire("TRADE_SKILL_LIST_UPDATE")
g4.fire("TRADE_SKILL_LIST_UPDATE")                 # unverändert: keine Zeile
L4.execute("ts.linked = true; ts.recipes[2152].diff = 3")
g4.fire("TRADE_SKILL_LIST_UPDATE")                 # Liste eines anderen Spielers: keine Zeile
L4.execute("ts.linked = false; ts.changing = true")
g4.fire("TRADE_SKILL_LIST_UPDATE")                 # Liste wird gerade neu aufgebaut: warten
L4.execute("ts.changing = false; ProfessionsFrame.shown = false")
g4.fire("TRADE_SKILL_CLOSE")
# Gefiltert (Suche): der gespeicherte Stand bleibt vollständig, nur das sichtbare Rezept ändert sich; Farbwechsel trotzdem
L4.execute("ProfessionsFrame.shown = true; ts.recipes[2152].diff = 2; ts.recipes[3816].diff = 1; ts.search = 'Balg'")
g4.fire("TRADE_SKILL_SHOW")
L4.execute("ts.search = ''; ProfessionsFrame.shown = false")
g4.fire("TRADE_SKILL_CLOSE")
# Ein zweiter Beruf, zuerst gefiltert gesehen: kurze Zeile, dann ohne Filter die ganze Liste
L4.execute("""ProfessionsFrame.shown = true
ts.prof = { professionID = 2811, professionName = "Verzauberkunst", skillLevel = 12, maxSkillLevel = 75 }
ts.recipes = {
  [7418] = { name = "Armschiene - Schwache Gesundheit", reag = { { 10940, 1 } }, enchant = true, diff = 0 },
  [14293] = { name = "Kleiner Zauberstab", reag = { { 4470, 1 }, { 10938, 1 } }, out = 11287, diff = 1 },
}
ts.search = "Zauberstab" """)
g4.fire("TRADE_SKILL_SHOW")
L4.execute("ts.search = ''")
g4.fire("TRADE_SKILL_LIST_UPDATE")
L4.execute("ProfessionsFrame.shown = false")
g4.fire("TRADE_SKILL_CLOSE")
g4.fire("TRADE_SKILL_LIST_UPDATE")                 # Fenster zu: nichts
# Bank: Reiter des Charakters und Kontobank; dasselbe nochmals über den Interaktions-Manager: keine zweite Zeile
L4.execute("""bags[6] = { [1] = { id = 2318, n = 40, name = 'Leichtes Leder' }, [2] = { id = 4234, n = 7, name = 'Schweres Leder' },
  [3] = { id = 2934, n = 6, name = 'Fetzen', bound = true } }
bags[15] = { [1] = { id = 10940, n = 12, name = 'Seltsamer Staub' } }""")
g4.fire("BANKFRAME_OPENED")
g4.fire("PLAYER_INTERACTION_MANAGER_FRAME_SHOW", 8)
L4.execute("bags[6][1].n = 30")
g4.fire("BANKFRAME_CLOSED")
g4.fire("PLAYER_INTERACTION_MANAGER_FRAME_HIDE", 8)   # gleich wie eben: keine Zeile
# Briefkasten mit Briefen des Auktionshauses (und einem privaten Brief, der nicht zählt)
L4.execute("""inbox = {
  { subject = "Auktion erfolgreich: Leichtes Leder", money = 1140,
    inv = { type = "seller", item = "Leichtes Leder", bid = 1200, buyout = 1200, deposit = 0, cut = 60, count = 20 } },
  { subject = "Auktion erfolgreich: Silberblatt (12)", money = 300 },
  { subject = "Auktion abgelaufen: Seltsamer Staub (5)", items = 1, qty = 5,
    link = "|cffffffff|Hitem:10940::::::::12:::::|h[Seltsamer Staub]|h|r" },
  { subject = "Auktion gewonnen: Mittleres Leder", items = 1, qty = 10,
    link = "|cffffffff|Hitem:2319::::::::12:::::|h[Mittleres Leder]|h|r",
    inv = { type = "buyer", item = "Mittleres Leder", bid = 2500, count = 10 } },
  { sender = "Freund", subject = "Hallo", money = 100 },
}""")
L4.execute("MailFrame.shown = true; interacting[17] = true")
g4.fire("MAIL_SHOW")
g4.fire("MAIL_INBOX_UPDATE")                        # dieselben Briefe: keine zweite Zeile
L4.execute("table.remove(inbox, 1)")                # Geld genommen: Brief weg
g4.fire("MAIL_INBOX_UPDATE")
# Die Rechnung wird erst lesbar, nachdem der Brief einmal geöffnet war: ergänzen statt neu
L4.execute("inbox[1].inv = { type = 'seller', item = 'Silberblatt', bid = 300, buyout = 300, deposit = 0, cut = 15, count = 12 }; "
           "inbox[1].days = 29.49")
g4.fire("MAIL_INBOX_UPDATE")
L4.execute("for _, m in ipairs(inbox) do m.days = (m.days or 29.5) - 0.02 end")   # Ablauf rückt nach: kein neuer Eintrag
g4.fire("MAIL_INBOX_UPDATE")
# Abgeholt, danach kommt ein gleicher Brief (Ablauf 2 Stunden später): ein neuer Eintrag, nicht der alte
L4.execute("for i, m in ipairs(inbox) do if m.subject:find('abgelaufen', 1, true) then table.remove(inbox, i) break end end")
g4.fire("MAIL_INBOX_UPDATE")
L4.execute("table.insert(inbox, { subject = 'Auktion abgelaufen: Seltsamer Staub (5)', items = 1, qty = 5, days = 29.5625, "
           "link = '|cffffffff|Hitem:10940::::::::12:::::|h[Seltsamer Staub]|h|r' })")
g4.fire("MAIL_INBOX_UPDATE")
L4.execute("MailFrame.shown = false; interacting[17] = false")
g4.fire("MAIL_CLOSED")
L4.execute("inbox = {}")                            # Client leert die Liste nach dem Weggehen: kein Brief gilt als abgeholt
g4.fire("MAIL_INBOX_UPDATE")
# Eigene Angebote: Ware ohne Bestätigung, Ware mit Bestätigung (nur eine Zeile), Gegenstand; dann ohne Ereignis:
# einmal mit weniger in den Taschen (Zeile), einmal nie zustande gekommen (keine Zeile). AH-Scan dabei aus.
slash4("ah aus")
L4.execute("interacting[21] = true; counts[2318] = 50")
g4.fire("AUCTION_HOUSE_SHOW")
L4.execute("C_AuctionHouse.PostCommodity({ id = 2318 }, 2, 20, 600)")
g4.fire("AUCTION_HOUSE_AUCTION_CREATED", 101)
L4.execute("needsConfirm = true; C_AuctionHouse.PostCommodity({ id = 2318 }, 1, 5, 700)")
g4.fire("AUCTION_HOUSE_POST_WARNING")              # der Server will eine Bestätigung (Fenster im UI)
L4.execute("C_AuctionHouse.ConfirmPostCommodity({ id = 2318 }, 1, 5, 700)")
g4.fire("AUCTION_HOUSE_AUCTION_CREATED", 102)
L4.execute("needsConfirm = false; C_AuctionHouse.PostItem({ id = 6386 }, 3, 1, nil, 5000)")
g4.fire("AUCTION_HOUSE_AUCTION_CREATED", 103)
L4.execute("counts[2318] = 50; C_AuctionHouse.PostCommodity({ id = 2318 }, 3, 10, 650); counts[2318] = 40")
L4.execute("C_AuctionHouse.PostCommodity({ id = 10940 }, 2, 3, 900)")
later4(31); g4.ticker()
# Bestätigung abgebrochen, gleich danach ein anderes Angebot: das Ereignis gehört zum neuen; abgelehntes Angebot: nichts
L4.execute("needsConfirm = true; C_AuctionHouse.PostCommodity({ id = 10940 }, 2, 5, 800)")
g4.fire("AUCTION_HOUSE_POST_WARNING")
later4(1)
L4.execute("needsConfirm = false; C_AuctionHouse.PostCommodity({ id = 2318 }, 2, 3, 610)")
g4.fire("AUCTION_HOUSE_AUCTION_CREATED", 104)
L4.execute("C_AuctionHouse.PostCommodity({ id = 2934 }, 1, 1, 100)")
g4.fire("AUCTION_HOUSE_POST_ERROR")
# Langsamer Server: das zweite Angebot kommt, bevor das erste bestätigt ist; die Ereignisse kommen der Reihe nach
L4.execute("C_AuctionHouse.PostCommodity({ id = 2318 }, 2, 2, 620)")
later4(5)
L4.execute("C_AuctionHouse.PostCommodity({ id = 2318 }, 2, 4, 630)")
g4.fire("AUCTION_HOUSE_AUCTION_CREATED", 105)
g4.fire("AUCTION_HOUSE_AUCTION_CREATED", 106)
later4(31); g4.ticker()
L4.execute("interacting[21] = false")
g4.fire("AUCTION_HOUSE_CLOSED")
slash4("ah an")
# Zwei AH-Scans 30 Minuten auseinander: Abnahme der billigsten Angebote
L4.execute("""auctions = {
  { id = 2318, n = 20, buy = 960, band = 3, name = 'Leichtes Leder' },
  { id = 2318, n = 5, buy = 260, band = 2, name = 'Leichtes Leder' },
  { id = 2318, n = 20, buy = 1100, band = 1, name = 'Leichtes Leder' },
  { id = 2319, n = 4, buy = 800, band = 3, name = 'Mittleres Leder' },
  { id = 4231, n = 2, buy = 300, band = 0, name = 'Geschmeidiger leichter Balg' },
}""")
def scan4():
    L4.execute("interacting[21] = true")
    g4.fire("AUCTION_HOUSE_SHOW")
    later4(2); g4.ticker()
    g4.fire("REPLICATE_ITEM_LIST_UPDATE")
    later4(3); g4.ticker()
    L4.execute("interacting[21] = false")
    g4.fire("AUCTION_HOUSE_CLOSED")
scan4()
L4.execute("""server_t = server_t + 1800
auctions = {
  { id = 2318, n = 10, buy = 470, band = 3, name = 'Leichtes Leder' },
  { id = 2318, n = 3, buy = 156, band = 2, name = 'Leichtes Leder' },
  { id = 2318, n = 20, buy = 1100, band = 1, name = 'Leichtes Leder' },
}""")
scan4()
# Angeln: 6 Fänge im Abstand von 60 s (Wert pro Stunde in tools/markt.py)
for k in range(6):
    later4(50)
    g4.fire("UNIT_SPELLCAST_SUCCEEDED", "player", "Cast-F%d" % k, 7620)
    later4(10)
    L4.execute("fishing = true; loot = { { type = 1, name = 'Deviatfisch', id = 6522, n = 1 } }; "
               "lootsrc = 'GameObject-0-3299-1-12345-35591-0000ABCDEF'")
    g4.fire("LOOT_OPENED", True, False)
    g4.fire("LOOT_CLOSED")
    L4.execute("fishing = false")
slash4("tipp")                                      # ohne KombiDaten: Hinweis
slash4("status")
L4.execute("logout = true")
g4.fire("PLAYER_LOGOUT")
L4.execute("logout = false")
db4 = g4.KombiTestlogDB
lines4 = [db4.log[i] for i in range(1, len(db4.log) + 1)]
msgs4 = [g4.messages[i] for i in range(1, len(g4.messages) + 1)]
print("=== Protokoll 3.6 (%d Einträge) ===" % len(lines4))
for l in lines4:
    print(l)
def one4(kind, *parts):
    hits = [l for l in lines4 if (" | %s | " % kind) in l and all(p in l for p in parts)]
    check(len(hits) == 1, "3.6: %s mit %s (%d Treffer)" % (kind, ", ".join(parts), len(hits)))
check(not any(" | FEHLER | " in l for l in lines4), "3.6: keine FEHLER (%s)" % [l for l in lines4 if " | FEHLER | " in l])
rez = [l for l in lines4 if " | REZEPTE | " in l]
check(len(rez) == 5, "3.6: fünf REZEPTE-Zeilen: Liste, zwei Farbwechsel, gefiltert, Liste des zweiten Berufs (%d)" % len(rez))
one4("REZEPTE", "Lederverarbeitung 55/150 | 3 Rezepte (Liste des Fensters)",
     "Leichter Rüstungssatz (2152): 1x Leichtes Leder (2318) -> 1x Leichter Rüstungssatz (2304), gelb",
     "Geschmeidiger leichter Balg (3816): 1x Leichter Balg (783) + 1x Salz (4289) -> 1x Geschmeidiger leichter Balg (4231), orange",
     "Leichtes Leder (2881): 3x Fetzen (2934) -> 1x Leichtes Leder (2318), grau")
check(not any("Handgenähte" in l for l in rez), "3.6: nicht gelernte Rezepte fehlen")
one4("REZEPTE", "Lederverarbeitung 61/150 | Farbe: Leichter Rüstungssatz gelb -> grün")
one4("REZEPTE", "Lederverarbeitung 61/150 | Farbe: Geschmeidiger leichter Balg orange -> gelb")
one4("REZEPTE", "Verzauberkunst 12/75 | Liste gefiltert (Suche «Zauberstab»): 1 Rezept sichtbar, gespeicherter Stand ergänzt")
one4("REZEPTE", "Verzauberkunst 12/75 | 2 Rezepte (Liste des Fensters) | Armschiene - Schwache Gesundheit (7418): "
     "1x Seltsamer Staub (10940) -> Verzauberung, orange; Kleiner Zauberstab (14293)")
char4 = db4.chars["Testheld-Testrealm"]
r4 = char4.rezepte["Lederverarbeitung"] if char4 is not None and char4.rezepte is not None else None
check(r4 is not None and r4.liste == "2152:2304:1:1:2:2318*1;2881:2318:1:1:3:2934*3;3816:4231:1:1:1:783*1,4289*1"
      and r4.stufe == 61 and r4.max == 150 and r4.filter is None,
      "3.6: Rezepte in der Datei, gefilterte Ansicht ergänzt nur (%s)" % (r4.liste if r4 is not None else None))
v4 = char4.rezepte["Verzauberkunst"]
check(v4.liste == "7418:0:1:1:0:10940*1;14293:11287:1:1:1:4470*1,10938*1" and v4.filter is None,
      "3.6: zweiter Beruf vollständig, Verzauberung ohne Ergebnis (%s, %s)" % (v4.liste, v4.filter))
check(all(db4.beobachten[i] for i in (2318, 2934, 2304, 783, 4289, 4231)), "3.6: Reagenzien und Ergebnisse werden beobachtet")
check(db4.rezeptNamen[3816] == "Geschmeidiger leichter Balg", "3.6: Rezeptnamen gespeichert")
one4("INVENTAR", "Taschen beim Einloggen: 2 Gegenstände, 6 Stück", "Plan: Roher glänzender Kleinfisch 5")
one4("INVENTAR", "Bank geöffnet | Bank: 2 Gegenstände, Plan: Leichtes Leder 40, Schweres Leder 7 | Kontobank: 1 Gegenstände, Plan: Seltsamer Staub 12")
one4("INVENTAR", "Bank geschlossen | Bank: 2 Gegenstände, Plan: Leichtes Leder 30, Schweres Leder 7")
check(sum(1 for l in lines4 if " | INVENTAR | " in l and "Bank" in l) == 2, "3.6: Bank nur bei Änderung neu")
one4("INVENTAR", "Taschen beim Ausloggen")
check(char4.bank.liste == "2318:30;4234:7" and db4.kontobank.liste == "10940:12" and char4.taschen.liste == "6291:5;6386:1",
      "3.6: Bestand in der Datei (%s / %s / %s)" % (char4.bank.liste, db4.kontobank.liste, char4.taschen.liste))
check(char4.bank.gebunden == "2934:6" and char4.taschen.gebunden is None, "3.6: gebundene Stücke getrennt (%s)" % char4.bank.gebunden)
check(db4.info[2318].n == "Leichtes Leder" and db4.info[2318].s == 15 and db4.info[6386].q == 2, "3.6: Gegenstands-Infos gespeichert")
post = [l for l in lines4 if " | AH-POST | " in l]
check(len(post) == 3, "3.6: drei AH-POST-Zeilen: die Briefe, die ergänzte Rechnung, der neue gleiche Brief (%d)" % len(post))
one4("AH-POST", "verkauft: 20x Leichtes Leder für 12s (Stück 60c), Gebühr 60c, 12x Silberblatt",
     "abgelaufen: 5x Seltsamer Staub (10940)", "gekauft: 10x Mittleres Leder (2319) für 25s")
one4("AH-POST", "Rechnung ergänzt: 12x Silberblatt für 3s (Stück 25c), Gebühr 15c")
check(sum(1 for l in post if l.endswith("| abgelaufen: 5x Seltsamer Staub (10940)")) == 1,
      "3.6: gleicher Brief nach dem Abholen ist ein neuer Eintrag")
check(not any("Hallo" in l or "Freund" in l for l in lines4), "3.6: private Briefe zählen nicht")
ap = db4.ahPost
arten = [ap[i].art for i in range(1, len(ap) + 1)]
check(arten.count("verkauft") == 2 and arten.count("abgelaufen") == 2 and arten.count("gekauft") == 1,
      "3.6: AH-Post in der Datei, kein Brief doppelt, keiner verschluckt (%s)" % arten)
weg4 = [ap[i].art for i in range(1, len(ap) + 1) if ap[i].weg]
check(sorted(weg4) == ["abgelaufen", "verkauft"], "3.6: abgeholte Briefe als weg markiert (%s)" % weg4)
sold = {ap[i].name: ap[i] for i in range(1, len(ap) + 1) if ap[i].art == "verkauft"}
check(sold["Leichtes Leder"].preis == 1200 and sold["Leichtes Leder"].gebuehr == 60 and sold["Leichtes Leder"].menge == 20
      and sold["Silberblatt"].preis == 300 and sold["Silberblatt"].menge == 12 and sold["Silberblatt"].ablauf is not None,
      "3.6: Verkauf mit Preis und Gebühr, Rechnung nachträglich ergänzt")
one4("AH-ANGEBOT", "20x Leichtes Leder (2318) zu 6s je Stück | Dauer 24 Std. | Pfand 1s 20c | erstellt")
one4("AH-ANGEBOT", "5x Leichtes Leder (2318) zu 7s je Stück | Dauer 12 Std. | Pfand 15c | erstellt")
one4("AH-ANGEBOT", "1x Gewebte Handschuhe (6386) zu 50s je Angebot | Dauer 48 Std. | Pfand 3s | erstellt")
one4("AH-ANGEBOT", "10x Leichtes Leder (2318) zu 6s 50c je Stück | Dauer 48 Std. | Pfand 90c | Taschen weniger, ohne Bestätigung")
one4("AH-ANGEBOT", "3x Leichtes Leder (2318) zu 6s 10c je Stück | Dauer 24 Std. | Pfand 18c | erstellt")
one4("AH-ANGEBOT", "2x Leichtes Leder (2318) zu 6s 20c je Stück | Dauer 24 Std. | Pfand 12c | erstellt")
one4("AH-ANGEBOT", "4x Leichtes Leder (2318) zu 6s 30c je Stück | Dauer 24 Std. | Pfand 24c | erstellt")
check(sum(1 for l in lines4 if " | AH-ANGEBOT | " in l) == 7,
      "3.6: sieben AH-ANGEBOT-Zeilen (bestätigtes nicht doppelt, abgebrochenes und abgelehntes nicht)")
check(not any(" | AH-ANGEBOT | " in l and ("10940" in l or "2934" in l) for l in lines4),
      "3.6: nie erstellte, abgebrochene und abgelehnte Angebote: keine Zeile")
posted4 = [g4.posted[i] for i in range(1, len(g4.posted) + 1)]
check(posted4 == ["C", "C", "CC", "I", "C", "C", "C", "C", "C", "C", "C"],
      "3.6: die Haken lassen die Blizzard-Aufrufe durch (%s)" % posted4)
sc4 = db4.ahScans
check(sc4 is not None and len(sc4) == 2, "3.6: zwei Scans")
if sc4 is not None and len(sc4) == 2:
    check(sc4[1].stufen[2318] == "48*20*20*20,52*5*5*0,55*20*0*0" and sc4[1].bandVersatz == 0 and sc4[1].bandRoh == "0-3",
          "3.6: Preisstufen mit Restlaufzeit, Bänder 0–3 erkannt (%s, %s)" % (sc4[1].stufen[2318], sc4[1].bandVersatz))
    check(sc4[1].stufen[4231] == "150*2*0*0", "3.6: Ergebnis eines Rezepts wird beobachtet (%s)" % sc4[1].stufen[4231])
    # 2319 und 4231 sind ganz verschwunden: gekauft oder zurückgezogen, unbekannt
    check(sc4[2].abnahme == "2318:22:12" and sc4[2].abstand == 1800,
          "3.6: Abnahme seit dem letzten Scan (%s, %s)" % (sc4[2].abnahme, sc4[2].abstand))
one4("AH-SCAN", "Abnahme seit dem letzten Scan (30 Min): 1 Gegenstand verglichen, geschätzt gekauft: Leichtes Leder (2318) 12")
check(any("Keine Empfehlungen geladen" in m for m in msgs4), "3.6: /tl tipp ohne KombiDaten: Hinweis")
check(any("Rezepte: Lederverarbeitung, Verzauberkunst" in m and "AH-Post: 12 Einträge" in m for m in msgs4),
      "3.6: Status mit Rezepten und AH-Post (%s)" % [m for m in msgs4 if "Rezepte:" in m])
sv4 = L4.execute(SERIALIZE)("KombiTestlogDB", db4)
if os.environ.get("TESTLOG_DATEI"):   # zum Ausprobieren der Werkzeuge: Testdatei schreiben
    open(os.environ["TESTLOG_DATEI"], "w", encoding="utf-8").write(sv4)
check("Kaeufername" not in sv4 and "Freund" not in sv4 and "Verkaeufername" not in sv4, "3.6: keine Namen anderer Spieler gespeichert")
# Empfehlungen geladen (Addon KombiDaten)
L5 = runtime(pre="""KombiDaten = { stand = "15.10. 20:15", zeit = server_t - 7200, markt = "EU Horde R1a2b Beta",
  tipps = { "Tipp 1", "Tipp 2", "Tipp 3", "Tipp 4", "Tipp 5", "Tipp 6", "Tipp 7" }, hinweise = { "Preise der Beta" } }""")
g5 = L5.globals()
g5.fire("ADDON_LOADED", "KombiTestlog")
g5.fire("PLAYER_ENTERING_WORLD", True, False)
g5.SlashCmdList["KOMBITESTLOG"]("tipp")
g5.SlashCmdList["KOMBITESTLOG"]("tipp alle")
msgs5 = [g5.messages[i] for i in range(1, len(g5.messages) + 1)]
log5 = [g5.KombiTestlogDB.log[i] for i in range(1, len(g5.KombiTestlogDB.log) + 1)]
check(any("Empfehlungen geladen: 7 Tipps vom 15.10. 20:15" in m for m in msgs5), "3.6: Hinweis beim Einloggen auf die Empfehlungen")
check(any(" | SITZUNG | " in l and "KombiDaten 15.10. 20:15, 7 Tipps" in l for l in log5), "3.6: SITZUNG nennt den Stand der Empfehlungen")
check(any("Empfehlungen vom 15.10. 20:15, vor 2 Std (EU Horde R1a2b Beta):" in m for m in msgs5), "3.6: /tl tipp Kopf mit Alter")
check(sum(1 for m in msgs5 if m.endswith("5. Tipp 5")) == 1 and not any(m.endswith("6. Tipp 6") for m in msgs5)
      and any("2 weitere: /tl tipp alle" in m for m in msgs5), "3.6: /tl tipp zeigt 5 Tipps und den Rest als Hinweis")
exp5 = [f.text for f in g5.frames.values() if f.text]
check(exp5 and "7. Tipp 7" in exp5[0] and "Hinweis: Preise der Beta" in exp5[0], "3.6: /tl tipp alle im Fenster zum Kopieren")
# Restlaufzeit gezählt wie die alte API (1–4): ein Wert 4 zeigt es, der Versatz gilt danach auch für unklare Scans
L7 = runtime()
g7 = L7.globals()
g7.fire("ADDON_LOADED", "KombiTestlog")
g7.fire("PLAYER_ENTERING_WORLD", True, False)
def scan7(auktionen):
    L7.execute("server_t = server_t + 1800; interacting[21] = true; auctions = " + auktionen)
    g7.fire("AUCTION_HOUSE_SHOW")
    L7.execute("now_t = now_t + 2"); g7.ticker()
    g7.fire("REPLICATE_ITEM_LIST_UPDATE")
    L7.execute("now_t = now_t + 3"); g7.ticker()
    L7.execute("interacting[21] = false")
    g7.fire("AUCTION_HOUSE_CLOSED")
scan7("{ { id = 2318, n = 5, buy = 300, band = 4, name = 'x' }, { id = 2318, n = 5, buy = 350, band = 2, name = 'x' } }")
scan7("{ { id = 2318, n = 5, buy = 350, band = 3, name = 'x' } }")
sc7 = g7.KombiTestlogDB.ahScans
check(sc7[1].stufen[2318] == "60*5*5*5,70*5*0*0" and sc7[1].bandVersatz == -1 and sc7[1].bandRoh == "2-4",
      "Restlaufzeit 1–4 erkannt: 4 = sehr lang, 2 = mittel (%s, %s)" % (sc7[1].stufen[2318], sc7[1].bandVersatz))
check(sc7[2].stufen[2318] == "70*5*5*0" and sc7[2].bandVersatz == -1 and sc7[2].abnahme == "2318:5:5",
      "Versatz bleibt für einen unklaren Scan; Abnahme bis zur Stufe, auf der noch etwas liegt (%s, %s)" %
      (sc7[2].stufen[2318], sc7[2].abnahme))
# Werte, die zu keiner Zählung passen (z. B. Sekunden): kein Versatz mehr, auch nicht der gespeicherte; keine Abnahme danach
scan7("{ { id = 2318, n = 5, buy = 350, band = 600, name = 'x' }, { id = 2318, n = 5, buy = 400, band = 170000, name = 'x' } }")
scan7("{ { id = 2318, n = 5, buy = 350, band = 2, name = 'x' } }")
sc7 = g7.KombiTestlogDB.ahScans
check(sc7[3].bandVersatz is None and sc7[3].bandRoh == "600-170000" and sc7[3].stufen[2318] == "70*5*0*0,80*5*0*0"
      and sc7[4].bandVersatz is None and sc7[4].abnahme is None and g7.KombiTestlogDB.ahBandVersatz is None,
      "unpassende Restlaufzeit-Werte: kein Versatz, keine Abnahme (%s, %s, %s)" % (sc7[3].bandVersatz, sc7[3].stufen[2318], sc7[4].abnahme))

# Format-Kopplung: tools/ah_aus_testlog.py liest die SavedVariables-Datei und den Text von /tl zeigen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ah_aus_testlog as at
aus_sv = at.lese(sv_text)
check(len(aus_sv) == 1 and s1 is not None and aus_sv[0]["datum"] == s1.datum and aus_sv[0]["markt"] == "EU Horde " + at.kennung("Testrealm"),
      "ah_aus_testlog liest den Scan aus der Lua-Datei (%s)" % [(x["datum"], x["markt"]) for x in aus_sv])
if aus_sv:
    p = aus_sv[0]["preise"]
    check(p.get(2318, {}).get("stufen") == [(48, 20), (52, 5), (55, 20)] and p[2318]["median"] == 52 and p[4306]["menge"] == 10,
          "ah_aus_testlog: Preise und Stufen aus der Lua-Datei (%s)" % p.get(2318))
    check("realm" not in aus_sv[0] and "Testrealm" not in str(aus_sv[0]) and "Testheld" not in str(aus_sv[0]),
          "ah_aus_testlog gibt keinen Realm- und keinen Charakternamen weiter")
    check(aus_sv[0]["phase"] == "Beta", "Scan vor dem 04.11.2026 zählt als Beta")
aus_txt = at.lese("\n".join(lines))
check(len(aus_txt) == 1 and aus_txt[0]["preise"].get(2318, {}).get("tiefst") == 48 and aus_txt[0]["preise"].get(2319, {}).get("median") == 200,
      "ah_aus_testlog liest die AH-SCAN-Zeile aus dem Text (%s)" % [x["preise"] for x in aus_txt])
check(at.kosten([(48, 20), (52, 5), (55, 20)], 30) == (20 * 48 + 5 * 52 + 5 * 55, 30), "Kosten der billigsten 30 Stück")
check(at.kosten([(48, 20)], 30) == (960, 20), "Kosten, wenn das Angebot nicht reicht")
check(len(aus_txt) == 1 and aus_txt[0]["markt"] == aus_sv[0]["markt"], "Text und Datei ergeben denselben Markt")
check(at.kosten_text({"stufen": [(48, 20)], "menge": 200}, 100) == "mind. 48.00", "Untergrenze, wenn die Preisstufen nicht reichen")
check(at.kosten_text({"stufen": [(48, 20)], "menge": 20}, 100) == "nur 20 Stück", "nur so viel im Angebot")
try:
    at._lua_tabelle("\x1bLuaQ")
    check(False, "Bytecode wird abgewiesen")
except SystemExit as e:
    check("Bytecode" in str(e), "Bytecode wird abgewiesen (%s)" % e)
# Zusammenführen: der Text von /tl zeigen löscht die Kosten aus der Datei nicht; unvollständige Scans zählen nicht
import tempfile
with tempfile.TemporaryDirectory() as tmp:
    at.EIGEN = os.path.join(tmp, "ah_eigen.csv")
    at._write(at.EIGEN, at.F_EIGEN, at.zusammenfuehren(at.zeilen_eigen(aus_sv, {}))[0])
    rows2, neu2 = at.zusammenfuehren(at.zeilen_eigen(aus_txt, {}))
    r2318 = [r for r in rows2 if str(r["item_id"]) == "2318"]
    check(neu2 == 0 and len(r2318) == 1 and r2318[0]["kosten_20_s"] == "9.60" and r2318[0]["angebote"] == "3" and "Testlog-Datei" in r2318[0]["quelle"],
          "Zusammenführen behält Kosten und Angebote (%s)" % r2318)
m = aus_sv[0]["markt"] + " Beta"
w, _ = at.wochen_median([{"datum": "2026-10-14 10:00", "markt": m, "item_id": "2318", "median_s": "0.50", "menge": "60", "hinweis": ""},
                         {"datum": "2026-10-15 10:00", "markt": m, "item_id": "2318", "median_s": "9.00", "menge": "60", "hinweis": "unvollständig"},
                         {"datum": "2026-10-16 10:00", "markt": m, "item_id": "2318", "median_s": "0.60", "menge": "40", "hinweis": ""}], m)
check(w.get(2318) == (0.55, 2, 50.0), "7-Tage-Median ohne unvollständige Scans, mit Menge (%s)" % (w.get(2318),))
# Ein Ereignis, das der Client nicht kennt: Das Addon lädt trotzdem und meldet es beim Start
try:
    L2 = runtime(unknown=("AUCTION_HOUSE_CLOSED",))
    g2 = L2.globals()
    g2.fire("ADDON_LOADED", "KombiTestlog")
    g2.fire("PLAYER_ENTERING_WORLD", True, False)
    log2 = [g2.KombiTestlogDB.log[i] for i in range(1, len(g2.KombiTestlogDB.log) + 1)]
except Exception as e:
    log2 = []
    check(False, "Addon lädt trotz unbekanntem Ereignis (%s)" % str(e).splitlines()[0])
check(any(" | FEHLER | " in l and "AUCTION_HOUSE_CLOSED" in l for l in log2), "unbekanntes Ereignis als FEHLER gemeldet")
check(any(" | SITZUNG | " in l for l in log2), "Addon läuft trotz unbekanntem Ereignis")
# Format-Kopplung: tools/karte_aus_testlog.py muss die KARTE-Zeilen lesen, als Text und in der SavedVariables-Form
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import karte_aus_testlog as kt
als_text = kt.parse("\n".join(karten))
als_lua = kt.parse("KombiTestlogDB = {\n\t[\"log\"] = {\n" + "".join('\t\t"%s", -- [%d]\n' % (l, i) for i, l in enumerate(karten, 1)) + "\t},\n}\n")
check(sorted(als_text) == ["1412", "1456"], "karte_aus_testlog liest KARTE-Text (%s)" % sorted(als_text))
check(als_lua == als_text, "karte_aus_testlog liest KARTE aus der Lua-Datei gleich wie aus dem Text")
r = als_text.get("1412", {})
check((r.get("a0"), r.get("b0"), r.get("a1"), r.get("b1")) == ("2448.20", "241.30", "-3643.30", "-3819.80"),
      "Achsen: a0 = Welt-Y(0,0), b0 = Welt-X(0,0), a1 = Welt-Y(1,1), b1 = Welt-X(1,1) (%s)" % r)

# --- Version 3.6: tools/ah_aus_testlog.py liest die Abnahme, tools/markt.py rechnet Empfehlungen ---
aus4 = at.lese(sv4)
check(len(aus4) == 2 and aus4[1]["abnahme"] == {2318: (22, 12)} and aus4[1]["abstand"] == 1800,
      "ah_aus_testlog liest die Abnahme (%s)" % [(s["abnahme"], s["abstand"]) for s in aus4])
check(aus4[0]["namen"].get(4231) == "Geschmeidiger leichter Balg", "ah_aus_testlog: Namen aus den Gegenstands-Infos")
check(at._stufen("48*20*20*20,52*5*5*0") == [(48, 20), (52, 5)] and at._stufen("48*20") == [(48, 20)],
      "Preisstufen mit und ohne Restlaufzeit")
import markt as mk
m4 = "EU Horde %s Beta" % at.kennung("Testrealm")
with tempfile.TemporaryDirectory() as tmp:
    at.EIGEN = os.path.join(tmp, "ah_eigen.csv")
    at.ABNAHME = os.path.join(tmp, "ah_abnahme.csv")
    # Verlauf der Woche davor (erfundene Testwerte): ein Scan pro Tag
    verlauf = {2318: (0.80, 300), 4231: (3.00, 40), 783: (0.40, 120), 10940: (1.20, 500), 6522: (5.00, 90), 6291: (1.10, 60)}
    hist = [{"datum": "2026-10-%02d 12:00" % d, "markt": m4, "item_id": i, "tiefstpreis_s": "%.2f" % p,
             "median_s": "%.2f" % (p * 1.2), "menge": n, "angebote": 5, "hinweis": "", "quelle": "Test"}
            for d in range(8, 14) for i, (p, n) in verlauf.items()]
    at._write(at.EIGEN, at.F_EIGEN, hist)
    abn_test = [{"datum": "2026-10-13 %02d:00" % h, "markt": m4, "item_id": i, "stunden": "%.2f" % st, "weg": w, "gekauft": g,
                 "quelle": "Test"} for h in (10, 12) for i, st, w, g in ((2318, 1.0, 35, 30), (4231, 2.0, 6, 5), (6291, 2.0, 9, 8))]
    at._write(at.ABNAHME, at.F_ABNAHME, abn_test)
    erg = mk.rechne(sv4, aus=os.path.join(tmp, "markt"))
    mm = erg["markt"]
    check(mm.markt == m4 and mm.letzter["datum"] == "2026-10-14 18:16", "markt: Markt und letzter Scan (%s, %s)" % (mm.markt, mm.letzter["datum"]))
    h = {e["id"]: e for e in erg["handel"]}
    h2318 = {k: h[2318][k] for k in ("menge", "kosten", "gewinn")} if 2318 in h else str(erg["ohne"])
    check(2318 in h and h[2318]["menge"] == 33 and round(h[2318]["kosten"]) == 1726 and round(h[2318]["gewinn"]) == 782,
          "markt: Leichtes Leder unter dem 7-Tage-Tiefstpreis kaufen (%s)" % (h2318,))
    her = {e["id"]: e for e in erg["herstellen"]}
    check(round(her[3816]["wert"]) == 285 and her[3816]["kosten"] == 90 and round(her[3816]["gewinn"]) == 195 and her[3816]["absatz"],
          "markt: Geschmeidiger leichter Balg (Wert 285, Kosten 90 aus Balg 7 Tage und Salz beim Händler) (%s)" %
          {k: her[3816].get(k) for k in ("wert", "kosten", "gewinn", "herkunft")})
    check(her[2152]["herkunft"] == "Händler-Ankauf" and round(her[2152]["gewinn"]) == -41, "markt: Rezept ohne AH-Preis mit Händler-Ankauf")
    check(her[2881]["fehlt"] == ["Fetzen"], "markt: fehlender Reagenzpreis wird genannt (%s)" % her[2881]["fehlt"])
    vk = {e["id"]: e for e in erg["verkaufen"]}
    check(vk.get(6291, {}).get("absatz") and not vk[6291]["plan"] and vk[10940]["plan"] and vk[2318]["plan"],
          "markt: Bestand verkaufen, Plan-Material markiert (%s)" % sorted(vk))
    check(mm.gebuehr_eigen == (0.05, 1500), "markt: Gebühr aus den eigenen Verkäufen (%s)" % (mm.gebuehr_eigen,))
    check(mm.eigen[2318]["verkauft"] == 20 and mm.eigen[2318]["verkauft_72h"] == 20 and mm.eigen[2318]["angeboten"] == 44,
          "markt: eigene Verkäufe und Angebote (%s)" % mm.eigen.get(2318))
    check(her[2881]["aus_bestand"] == 2, "markt: gebundene Stücke zählen zum Herstellen (%s)" % her[2881]["aus_bestand"])
    # Vorläufige Rechnung (mit Preis) und endgültiger Brief ohne lesbare Rechnung, 10 Stunden später: ein Verkauf
    mt = mk.Markt({"ahPost": [
        {"art": "verkauft", "name": "X", "menge": 20, "preis": 1000, "vorlaeufig": True, "ablauf": 100000, "zeit": 1},
        {"art": "verkauft", "name": "X", "menge": 20, "ablauf": 136000, "zeit": 2},
        {"art": "verkauft", "name": "X", "preis": 50, "vorlaeufig": True, "ablauf": 200000, "zeit": 3}]}, [], {77: "X"})
    check(mt.eigen[77]["verkauft"] == 21 and mt.eigen[77]["n"] == 2,
          "markt: vorläufige Rechnung nicht doppelt, ohne endgültige gezählt (%s)" % mt.eigen.get(77))
    check(mm.absatz(2318) == 72 and mm.absatz(4231) == 10 and mm.absatz(2319) == 0,
          "markt: Absatz mit Beleg nie hochgerechnet (%s, %s, %s)" % (mm.absatz(2318), mm.absatz(4231), mm.absatz(2319)))
    fa = erg["farmen"]
    check(fa and fa[0]["art"] == "Angeln" and fa[0]["gebiet"] == "Mulgore" and round(fa[0]["pro_stunde"]) == 28500,
          "markt: Angeln pro Stunde (%s)" % fa)
    tp = erg["tipps"]
    check(len(tp) == 4 and tp[0].startswith("Kaufen: 33x Leichtes Leder bis 58c (zusammen 17s 26c), wieder einstellen um 80c")
          and tp[1].startswith("Herstellen (Testheld, Lederverarbeitung): Geschmeidiger leichter Balg bringt je 1s 95c (217 %)")
          and tp[2].startswith("Verkaufen: 5x Roher glänzender Kleinfisch (Testheld 5) im AH um 1s 10c")
          and tp[3].startswith("Farmen: Angeln (Mulgore) brachte 2g 85s pro Stunde"), "markt: Tipps (%s)" % tp)
    daten = open(os.path.join(tmp, "markt", "KombiDaten", "Daten.lua"), encoding="utf-8").read()
    toc = open(os.path.join(tmp, "markt", "KombiDaten", "KombiDaten.toc"), encoding="utf-8").read()
    bericht_md = open(os.path.join(tmp, "markt", "markt.md"), encoding="utf-8").read()
    print("=== markt.py: Daten.lua ===")
    print(daten)
    if os.environ.get("MARKT_BERICHT"):
        open(os.environ["MARKT_BERICHT"], "w", encoding="utf-8").write(bericht_md)
    check("## Interface: 16001" in toc and "Daten.lua" in toc, "markt: KombiDaten.toc")
    check("## Quellen" in bericht_md.split("## Kurz")[0] and "https://ahledger.com/wow-forever/auction-house" in bericht_md,
          "markt: Bericht beginnt mit den Quellen")
    # Die erzeugte Datei lädt im Spiel und /tl tipp zeigt die Tipps
    L6 = runtime(pre=daten)
    g6 = L6.globals()
    g6.fire("ADDON_LOADED", "KombiTestlog")
    g6.fire("PLAYER_ENTERING_WORLD", True, False)
    g6.SlashCmdList["KOMBITESTLOG"]("tipp")
    msgs6 = [g6.messages[i] for i in range(1, len(g6.messages) + 1)]
    check(any("Empfehlungen vom 14.10. 18:16" in m for m in msgs6) and any("1. Kaufen: 33x Leichtes Leder" in m for m in msgs6),
          "markt: Daten.lua lädt und /tl tipp zeigt sie (%s)" % msgs6[-6:])
    check(mk.naechstes([(47, 10), (52, 3), (55, 20)], 12) == 52 and mk.naechstes([(47, 10), (52, 3)], 13) is None
          and mk.naechstes([(47, 10), (52, 3)], 10) == 52, "markt: nächstes Angebot nach dem Kauf")
    # Nur eigene Verkäufe als Beleg (20 Stück): Nach dem Kauf der billigsten 20 liegen noch 13 zu 55c im Angebot,
    # wieder einstellen ginge nur um 54c -> keine Empfehlung
    at._write(at.ABNAHME, at.F_ABNAHME, [r for r in abn_test if r["item_id"] != 2318])
    erg2 = mk.rechne(sv4, aus=os.path.join(tmp, "markt2"))
    o2 = {e["id"]: e for e in erg2["ohne"]}
    check(not erg2["handel"] and 2318 in o2 and o2[2318]["menge"] == 20 and o2[2318]["um"] == 54
          and o2[2318]["grund"] == "nächstes Angebot 55c liegt zu tief",
          "markt: billigeres Angebot nach dem Kauf verhindert die Empfehlung (%s)" %
          ({k: o2[2318][k] for k in ("menge", "um", "grund")} if 2318 in o2 else erg2["handel"]))
    check("Achtung: Tiefstpreis fällt (-20 % in den letzten 3 Tagen)." in tp[0], "markt: Warnung bei fallendem Preis")
    # Sonderzeichen in Texten bleiben gültiges Lua
    check(mk.lua_str('a "b" \\ c\nd') == '"a \\"b\\" \\\\ c\\nd"', "markt: Lua-Text mit Anführungszeichen und Zeilenumbruch")
print("=== Prüfungen: %s ===" % ("alle bestanden" if not fails else "FEHLGESCHLAGEN: " + "; ".join(fails)))
sys.exit(1 if fails else 0)
