# Simuliert die WoW-Umgebung grob und spielt typische Abläufe gegen KombiTestlog.lua durch
# Aufruf: python3 tools/testlog_harness.py addons/KombiTestlog/KombiTestlog.lua
import os, sys
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
logout = false
UnitXP = function() if logout then return 0 end return 450 end
UnitXPMax = function() return 1000 end
UnitName = function(u) if u == "player" then return "Testheld" end return "Prairie Wolf" end
UnitExists = function(u) return u == "target" end
GetRealmName = function() return "Beta" end
GetBuildInfo = function() return "1.60.1", "70338" end
GetZoneText = function() return "Mulgore" end
GetSubZoneText = function() return "Bloodhoof Village" end
currentMap = 1412
-- Kartenecken in Weltkoordinaten (erfundene Testwerte, nur für den Ablauf)
bounds = { [1412] = { 241.3, 2448.2, -3819.8, -3643.3 }, [1456] = { 500.0, 1000.0, -100.0, 400.0 } }
CreateVector2D = function(x, y) return { x = x, y = y, GetXY = function(self) return self.x, self.y end } end
C_Map = {
  GetBestMapForUnit = function() if logout then return nil end return currentMap end,
  GetPlayerMapPosition = function() return { GetXY = function(self) return 0.468, 0.581 end } end,
  GetWorldPosFromMapPos = function(m, v)
    local b = bounds[m]
    if not b then return nil end
    return 1, CreateVector2D(b[1] + (b[3] - b[1]) * v.x, b[2] + (b[4] - b[2]) * v.y)
  end,
  GetMapWorldSize = function(m) local b = bounds[m] if not b then return 0, 0 end return math.abs(b[4] - b[2]), math.abs(b[3] - b[1]) end,
  GetMapInfo = function(m) if m == 1412 then return { name = "Mulgore" } end if m == 1456 then return { name = "Donnerfels" } end return nil end,
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
g.fire("QUEST_TURNED_IN", 870, 450, 0)
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
L.execute("logout = true")
g.fire("PLAYER_LOGOUT")
L.execute("logout = false")
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
before = len(db.log)
slash("leeren ja")
print("nach 'leeren ja':", len(db.log), "vorher", before)

# Prüfungen
fails = []
def check(cond, text):
    if not cond: fails.append(text)
kinds = [l.split(" | ")[1] for l in lines]
check(kinds.count("SITZUNG") == 1, "genau eine SITZUNG")
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
print("=== Prüfungen: %s ===" % ("alle bestanden" if not fails else "FEHLGESCHLAGEN: " + "; ".join(fails)))
sys.exit(1 if fails else 0)
