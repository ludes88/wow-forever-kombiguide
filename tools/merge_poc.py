# Machbarkeitsprobe Weg A: RXP-Gratis-Guide holen, Gruppe umbenennen, Berufsschritt an Anker einfügen, prüfen
# Aufruf: tools/fetch_rxp.sh v4.11.23 && python3 tools/merge_poc.py v4.11.23  -> build/Kombi_Probe.lua
import os, re, subprocess, sys
from lupa import lua51

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RXP = os.environ.get("RXP_DIR", os.path.join(ROOT, "vendor", "rxpguides"))
TAG = sys.argv[1] if len(sys.argv) > 1 else "v4.11.23"
FILES = ["Guides/forever/Horde-1-12_Mulgore.lua", "Guides/forever/Horde-12-22_Barrens.lua"]
NEW_GROUP = "Kombiguide (H)"
LAST_NEXT = "RestedXP Forever Guide (H)\\22-24 Hillsbrad"

# Einfügungen: (Guide-Name, Anker-Regex, Position, Schritttext)
INSERTS = [
    ("6-12 Mulgore", r"^\s*\.turnin 768\b", "after",
     "step\n    #label KombiProbe1\n    >>|cRXP_WARN_Kombi-Probe: hier käme ein Berufsschritt|r\n    .skill skinning,<1,1\n"),
]

def show(path):
    return subprocess.run(["git", "-C", RXP, "show", f"{TAG}:{path}"], capture_output=True, text=True, check=True).stdout

def split_steps(body):
    lines = body.split("\n")
    head, steps, cur = [], [], None
    for l in lines:
        if re.match(r"^\s*step\b", l):
            if cur is not None: steps.append(cur)
            cur = [l]
        elif cur is None:
            head.append(l)
        else:
            cur.append(l)
    if cur is not None: steps.append(cur)
    return head, steps

report = []
out_blocks = []
for path in FILES:
    src = show(path)
    blocks = re.findall(r"RXPGuides\.RegisterGuide\(\[\[(.*?)\]\]\)", src, re.S)
    for body in blocks:
        head, steps = split_steps(body)
        name = next((re.sub(r"^\s*#name\s+", "", l).strip() for l in head if re.match(r"^\s*#name\s", l)), "?")
        newhead = []
        for l in head:
            if re.match(r"^\s*#group\s", l):
                l = f"#group {NEW_GROUP}"
            elif re.match(r"^\s*#defaultfor\s", l):
                continue
            elif re.match(r"^\s*#next\s+22-24 Hillsbrad\s*$", l):
                l = f"#next {LAST_NEXT}"
            newhead.append(l)
        for gname, anchor, pos, text in INSERTS:
            if gname != name: continue
            hits = [i for i, st in enumerate(steps) if any(re.search(anchor, x) for x in st)]
            if len(hits) != 1:
                report.append(f"{name}: Anker {anchor!r} {len(hits)}x gefunden, nicht eingefügt"); continue
            i = hits[0]
            if pos == "after":
                j = i + 1
                # nie zwischen einen '#completewith next'-Schritt und seinen Nachfolger
                while j - 1 < len(steps) and any(re.match(r"^\s*#completewith\s+next\b", x) for x in steps[j - 1]):
                    j += 1
            else:
                j = i
                while j - 1 >= 0 and any(re.match(r"^\s*#completewith\s+next\b", x) for x in steps[j - 1]):
                    j -= 1
            steps.insert(j, text.rstrip("\n").split("\n"))
            report.append(f"{name}: eingefügt nach Schritt {i + 1} (Anker eindeutig), neue Position {j + 1}")
        report.append(f"{name}: {len(steps)} Schritte")
        out_blocks.append("\n".join(newhead) + "\n" + "\n".join("\n".join(s) for s in steps))

header = ("-- Kombi-Guide (Machbarkeitsprobe), Basis RestedXP " + TAG + "\n"
          "-- Quelle: github.com/RestedXP/RXPGuides (CC BY-NC-SA 4.0), bearbeitet\n"
          "if not (RXPGuides and RXPGuides.RegisterGuide) then return end\n"
          "if UnitFactionGroup(\"player\") == \"Alliance\" then return end\n")
lua_src = header + "\n".join(f"RXPGuides.RegisterGuide([[\n{b}\n]])\n" for b in out_blocks)
os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
open(os.path.join(ROOT, "build", "Kombi_Probe.lua"), "w", encoding="utf-8").write(lua_src)

# Prüfen: Lua-Syntax, RegisterGuide-Aufrufe, Kopf, Befehle
L = lua51.LuaRuntime(unpack_returned_tuples=True)
L.execute('captured = {}; RXPGuides = {RegisterGuide = function(s) table.insert(captured, s) end}; UnitFactionGroup = function() return "Horde" end')
fn = L.globals().loadstring(lua_src)
assert fn is not None, "Lua-Syntaxfehler"
fn()
cap = L.globals().captured
report.append(f"Lua 5.1 ok, {len(cap)} Guides registriert, Datei {len(lua_src)//1024} KB")
fsrc = open(f"{RXP}/functions.lua", encoding="utf-8").read()
funcs = set(re.findall(r"function addon\.functions\.(\w+)\s*\(", fsrc)) | set(re.findall(r'addon\.functions\["(\w+)"\]\s*=', fsrc)) | set(re.findall(r"addon\.functions\.(\w+)\s*=", fsrc))
unknown = set()
for i in range(1, len(cap) + 1):
    t = cap[i]
    if "#forever" not in t.split("\nstep")[0]: report.append(f"Guide {i}: #forever fehlt")
    for m in re.finditer(r"^\s*\.(\w+)", t, re.M):
        if m.group(1) not in funcs: unknown.add(m.group(1))
    if "Kombiguide (H)" not in t.split("\nstep")[0]: report.append(f"Guide {i}: Gruppe nicht ersetzt")
report.append("unbekannte Befehle: " + (", ".join(sorted(unknown)) if unknown else "keine"))
print("\n".join(report))
