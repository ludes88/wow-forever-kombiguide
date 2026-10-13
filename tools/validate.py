# Prüft einen Guide gegen den RXP-Quellcode in vendor/rxpguides (vorher tools/fetch_rxp.sh <Tag>)
# Aufruf: python3 tools/validate.py <guide.lua> <guide.toc>
import os, re, sys, glob
from lupa import lua51

RXP = os.environ.get("RXP_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vendor", "rxpguides"))
GUIDE = sys.argv[1]
TOC = sys.argv[2]

errors, notes = [], []

# 1) Lua-Syntax (Lua 5.1 wie WoW) und Text abgreifen
lua = lua51.LuaRuntime(unpack_returned_tuples=True)
lua.execute("captured = {}; RXPGuides = {RegisterGuide = function(s) table.insert(captured, s) end}")
src = open(GUIDE, encoding="utf-8").read()
try:
    lua.execute(src)
except Exception as e:
    errors.append(f"Lua-Fehler: {e}")
    print("\n".join(errors)); sys.exit(1)
cap = lua.eval("captured")
texts = [cap[i] for i in range(1, len(cap) + 1)]
if len(texts) != 1:
    errors.append(f"RegisterGuide {len(texts)}x aufgerufen")
text = texts[0]
notes.append(f"Lua 5.1 Syntax ok, Guide-Text {len(text)} Zeichen")

# 2) RXP-Funktionen und Step-Tags aus dem Quellcode
fsrc = open(f"{RXP}/functions.lua", encoding="utf-8").read()
funcs = set(re.findall(r"function addon\.functions\.(\w+)\s*\(", fsrc))
funcs |= set(re.findall(r'addon\.functions\["(\w+)"\]\s*=', fsrc))
funcs |= set(re.findall(r"addon\.functions\.(\w+)\s*=", fsrc))
rxp_guides = "\n".join(open(p, encoding="utf-8").read() for p in glob.glob(f"{RXP}/Guides/forever/*.lua"))
used_steptags = set(re.findall(r"^\s*#(\w+)", rxp_guides, re.M))

# 3) Kopf wie im RXP-Loader (LoadGuide: Kopfzeilen bis zum ersten step)
head, _, body = text.partition("\nstep")
hl = [l.strip() for l in head.strip().splitlines()]
if not any("#FOREVER" in l.upper() for l in hl): errors.append("Kopf ohne #forever: Guide wird in Forever nicht geladen")
for tag in ("#name", "#group"):
    if not any(l.startswith(tag + " ") for l in hl): errors.append(f"Kopf ohne {tag}")
if "<< Horde" not in hl: errors.append("Kopf ohne << Horde")

# 4) Zeilen prüfen
labels, refs = set(), []
step_no = 0
for raw in ("step" + body).splitlines():
    l = raw.strip()
    if not l: continue
    if l.startswith("step"):
        step_no += 1; continue
    if "--" in l: errors.append(f"Schritt {step_no}: '--' im Text schneidet die Zeile ab: {l}")
    if "[[" in l or "]]" in l: errors.append(f"Schritt {step_no}: Klammern beenden den Lua-String: {l}")
    if l.startswith("#"):
        tag, _, val = l[1:].partition(" ")
        if tag not in used_steptags: errors.append(f"Schritt {step_no}: unbekannter Step-Tag #{tag}")
        if tag == "label": labels.add(val.strip())
        if tag == "completewith" and val.strip() != "next": refs.append((step_no, val.strip()))
        continue
    if l.startswith(">>"): continue
    m = re.match(r"^\.(\w+)\s*(.*)$", l)
    if not m:
        errors.append(f"Schritt {step_no}: Zeile nicht erkannt: {l}"); continue
    cmd, args = m.group(1), m.group(2)
    args = re.sub(r"\s*<<.*$", "", args)
    args = args.split(">>")[0].strip()
    if cmd not in funcs: errors.append(f"Schritt {step_no}: Befehl .{cmd} gibt es in RXP nicht")
    # Werte gegen die RXP-Forever-Guides abgleichen
    if cmd == "goto":
        if not re.search(re.escape(f".goto {args}"), rxp_guides):
            # gleiche Koordinate mit anderem Radius zulassen
            core = ",".join(args.split(",")[:3])
            if core not in rxp_guides: errors.append(f"Schritt {step_no}: Koordinate nicht in RXP-Forever-Guides: {args}")
    if cmd in ("target", "mob"):
        name = args.lstrip("+")
        if not re.search(r"\.(target|mob)\s+\+?" + re.escape(name) + r"\s*$", rxp_guides, re.M):
            errors.append(f"Schritt {step_no}: Name nicht in RXP-Forever-Guides: {name}")
    if cmd in ("accept", "turnin"):
        qid = args.split(",")[0]
        if not re.search(rf"\.{cmd}\s+{qid}\b", rxp_guides):
            errors.append(f"Schritt {step_no}: .{cmd} {qid} kommt in RXP-Forever-Guides nicht vor")
    if cmd == "complete":
        qid, obj = args.split(",")[:2]
        if not re.search(rf"\.complete\s+{qid},{obj}\b", rxp_guides):
            errors.append(f"Schritt {step_no}: .complete {qid},{obj} kommt in RXP-Forever-Guides nicht vor")
    if cmd == "fly":
        if not re.search(rf"\.fly\s+{re.escape(args)}\s*>>", rxp_guides):
            errors.append(f"Schritt {step_no}: .fly {args} kommt in RXP-Forever-Guides nicht vor")
for s, ref in refs:
    if ref not in labels: errors.append(f"Schritt {s}: #completewith {ref} hat kein passendes #label")

# 5) .toc
toc = open(TOC, encoding="utf-8").read()
rxptoc = open(f"{RXP}/RXPGuides.toc", encoding="utf-8").read()
iface = re.search(r"## Interface:\s*(.+)", toc).group(1).split(",")
rxp_iface = [x.strip() for x in re.search(r"## Interface:\s*(.+)", rxptoc).group(1).split(",")]
for i in iface:
    if i.strip() not in rxp_iface: errors.append(f".toc Interface {i.strip()} steht nicht in RXPGuides.toc")
if "## Dependencies: RXPGuides" not in toc: errors.append(".toc ohne Abhängigkeit zu RXPGuides")
for fn in re.findall(r"^(\w+\.lua)\s*$", toc, re.M):
    import os
    if not os.path.exists(os.path.join(os.path.dirname(TOC), fn)): errors.append(f".toc nennt fehlende Datei {fn}")

notes.append(f"{step_no} Schritte, Labels: {sorted(labels)}")
print("\n".join(notes))
print("FEHLER:" if errors else "Keine Fehler gefunden.")
print("\n".join(errors))
