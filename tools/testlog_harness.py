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
-- nach einem Neustart meldet der Client die Zone erst nach einigen Sekunden (Testlog 13.10. 22:07)
zoneEmpty = 2
GetZoneText = function() if zoneEmpty > 0 then zoneEmpty = zoneEmpty - 1 return "" end return "Mulgore" end
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
counts = { [2318] = 10, [765] = 3, [6291] = 5 }
-- Version 3: Zeit, Geld, Taschen, Zauber, Lootfenster
now_t = 1000
GetTime = function() return now_t end
money = 12345
GetMoney = function() return money end
NUM_BAG_SLOTS = 4
bags = { [0] = {
  [1] = { id = 6291, n = 5, name = "Roher glänzender Kleinfisch", q = 1 },
  [2] = { id = 6386, n = 1, name = "Gewebte Handschuhe", q = 2 },
} }
C_Container = {
  GetContainerNumSlots = function(bag) if bag == 0 then return 16 end return 0 end,
  GetContainerItemInfo = function(bag, slot)
    local b = bags[bag]
    local it = b and b[slot]
    if not it then return nil end
    return { itemID = it.id, stackCount = it.n, quality = it.q or 1, itemName = it.name,
             hyperlink = "|cff1eff00|Hitem:" .. it.id .. "::::::::12:::::|h[" .. it.name .. "]|h|r" }
  end,
}
spells = { [7751] = "Glänzender Kleinfisch", [13262] = "Entzaubern", [8613] = "Kürschnern", [7620] = "Angeln",
           [5176] = "Zorn", [5177] = "Zorn (Rang 2)", [2152] = "Leichter Rüstungssatz" }
C_Spell = { GetSpellName = function(id) return spells[id] end }
-- Name, Qualität, Gegenstandsstufe, benötigte Stufe, Klasse (4 = Rüstung)
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
Enum = { LootSlotType = { None = 0, Item = 1, Money = 2, Currency = 3 } }
C_Item = {
  GetItemCount = function(id) return counts[id] or 0 end,
  GetItemNameByID = function(id) if id == 2318 then return "Leichtes Leder" end if id == 765 then return "Silberblatt" end return nil end,
  GetItemInfo = function(x)
    local id = type(x) == "number" and x or tonumber(tostring(x):match("item:(%d+)"))
    local i = iteminfo[id]
    if not i then return nil end
    return i[1], "link", i[2], i[3], i[4], "Rüstung", "Stoff", 1, "INVTYPE_HAND", 0, 4, i[5], 1
  end,
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
  local f = { events = {}, scripts = {}, text = "", unitEvents = {} }
  function f:RegisterEvent(e) self.events[e] = true end
  function f:RegisterUnitEvent(e, ...) self.events[e] = true; self.unitEvents[e] = { ... } end
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
# Händler: drei Verkäufe und ein Kauf werden eine Zeile (verkauft, gekauft, Einnahmen, Ausgaben)
later(10)
g.fire("MERCHANT_SHOW")
g.fire("MERCHANT_SHOW")           # doppelt gemeldet: keine zweite Sitzung
L.execute("money = money + 15; bags[0][6] = nil")
g.fire("PLAYER_MONEY"); g.fire("BAG_UPDATE_DELAYED")
for d in (30, 7):
    L.execute("money = money + %d" % d)
    g.fire("PLAYER_MONEY")
L.execute("money = money - 50; bags[0][7] = { id = 2320, n = 5, name = 'Grobes Garn' }")
g.fire("PLAYER_MONEY"); g.fire("BAG_UPDATE_DELAYED")
g.fire("MERCHANT_CLOSED")
g.fire("MERCHANT_CLOSED")         # doppelt gemeldet: keine zweite Zeile
# Post: Geld aus einem Verkauf und Leder aus einem Brief
later(10)
g.fire("MAIL_SHOW")
L.execute("money = money + 10000")
g.fire("PLAYER_MONEY")
L.execute("bags[0][8] = { id = 2319, n = 20, name = 'Mittleres Leder' }")
g.fire("BAG_UPDATE_DELAYED")
g.fire("MAIL_CLOSED")
# Lehrer: Kosten und gelernter Zauber
g.fire("TRAINER_SHOW")
L.execute("money = money - 100")
g.fire("PLAYER_MONEY")
g.fire("LEARNED_SPELL_IN_SKILL_LINE", 5177, 1, False)
g.fire("TRAINER_CLOSED")
g.fire("NEW_RECIPE_LEARNED", 2152)
later(10); g.ticker()
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
