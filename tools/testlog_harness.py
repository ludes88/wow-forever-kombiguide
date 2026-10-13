# Simuliert die WoW-Umgebung grob und spielt typische Abläufe gegen KombiTestlog.lua durch
# Aufruf: python3 tools/testlog_harness.py addons/KombiTestlog/KombiTestlog.lua
import sys
from lupa import lua51

L = lua51.LuaRuntime(unpack_returned_tuples=True)
L.execute(r'''
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
UnitXP = function() return 450 end
UnitXPMax = function() return 1000 end
UnitName = function(u) if u == "player" then return "Testheld" end return "Prairie Wolf" end
UnitExists = function(u) return u == "target" end
GetRealmName = function() return "Beta" end
GetBuildInfo = function() return "1.60.1", "70338" end
GetZoneText = function() return "Mulgore" end
GetSubZoneText = function() return "Bloodhoof Village" end
C_Map = {
  GetBestMapForUnit = function() return 1412 end,
  GetPlayerMapPosition = function() return { GetXY = function(self) return 0.468, 0.581 end } end,
}
RXPCData = { currentGuideGroup = "RestedXP Forever Guide (H)", currentGuideName = "6-12 Mulgore", currentStep = 57 }
counts = { [2318] = 10, [765] = 3 }
C_Item = {
  GetItemCount = function(id) return counts[id] or 0 end,
  GetItemNameByID = function(id) if id == 2318 then return "Leichtes Leder" end if id == 765 then return "Silberblatt" end return nil end,
}
skills = {
  { name = "Berufe", isHeader = true },
  { name = "Kürschnerei", rank = 10, maxRank = 75, isAbandonable = true },
  { name = "Kochen", rank = 5, maxRank = 75, isAbandonable = true },
  { name = "Waffenfertigkeiten", isHeader = true },
  { name = "Stäbe", rank = 50, maxRank = 60, isAbandonable = false },
  { name = "Fischen", rank = 1, maxRank = 75, isAbandonable = false },
}
C_SkillInfo = {
  GetNumSkillLines = function() return #skills end,
  GetSkillLineInfo = function(i) return skills[i] end,
}
C_AddOns = {
  GetAddOnMetadata = function(n, k) if n == "RXPGuides" then return "v4.11.23" end return "1" end,
  IsAddOnLoaded = function(n) return n == "RXPGuides_Kombi" end,
}
C_QuestLog = { GetTitleForQuestID = function(id) if id == 870 then return "Die Vergessenen Teiche (Test)" end return nil end }
ticker = nil
C_Timer = { After = function(s, f) f() end, NewTicker = function(s, f) ticker = f return {} end }
frames = {}
local function newObj()
  local o = {}
  local mt = { __index = function(t, k) return function(...) return nil end end }
  setmetatable(o, mt)
  return o
end
CreateFrame = function(kind, name, parent, template)
  local f = { events = {}, scripts = {}, text = "" }
  function f:RegisterEvent(e) self.events[e] = true end
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
''')

src = open(sys.argv[1], encoding="utf-8").read()
chunk = L.globals().loadstring(src)
if chunk is None:
    print("loadstring failed"); sys.exit(1)
chunk("KombiTestlog")
g = L.globals()
slash = lambda m: g.SlashCmdList["KOMBITESTLOG"](m)

g.fire("ADDON_LOADED", "KombiTestlog")
g.fire("PLAYER_LOGIN")
L.execute("counts[2318] = 12")
g.fire("BAG_UPDATE_DELAYED")
L.execute("skills[2].rank = 11; skills[5].rank = 51")
g.fire("SKILL_LINES_CHANGED")
L.execute("RXPCData.currentStep = 58")
g.ticker()
g.ticker()  # unverändert: kein zweiter Eintrag
g.fire("QUEST_ACCEPTED", 870)
g.fire("QUEST_TURNED_IN", 870, 450, 0)
L.execute("level = 13")
g.fire("PLAYER_LEVEL_UP", 13)
g.fire("PLAYER_DEAD")
g.fire("ZONE_CHANGED_NEW_AREA")
slash("Pfeil zeigt in den Berg")
slash("bug Schritt 12 bleibt hängen")
slash("idee Hier lohnt eine Farmrunde")
slash("item |cffffffff|Hitem:765::::::::12:::::|h[Silberblatt]|h|r")
L.execute("counts[765] = 5")
g.fire("BAG_UPDATE_DELAYED")
slash("status")
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
before = len(db.log)
slash("leeren ja")
print("nach 'leeren ja':", len(db.log), "vorher", before)
errs = [log for log in []]
