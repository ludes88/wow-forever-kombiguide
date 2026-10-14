# Kombi-Guide bauen: RXP-Gratis-Route 1-22 (Horde, Forever) als eigene Gruppe, Berufsschritte aus der Plan-Tabelle einfügen, prüfen.
#
# Aufruf:  tools/fetch_rxp.sh v4.11.23 && python3 tools/build_kombi.py v4.11.23 [Ausgabeordner]
# Eingaben: data/kombi/plan.csv (eine Zeile pro Berufsschritt), data/karten/forever_karten.csv (Kartenecken), data/kombi/VERSION
# Ausgabe:  <Ausgabeordner, Standard build/>/RXPGuides_KombiGuide/{RXPGuides_KombiGuide.toc, Kombi_Guide.lua}
#
# Koordinaten: Spielkoordinaten (x, y in Prozent, wie im Testlog) werden über die Kartenecken a0/b0 (Karte 0,0) und a1/b1
# (Karte 1,1) in RXP-Weltkoordinaten umgerechnet: a = a0 + (a1 - a0) * x / 100, b = b0 + (b1 - b0) * y / 100.
# NIE RXPs Kommentar-Koordinaten (--c:Zone,x,y) als Grundlage nehmen: Sie passen nicht zur Forever-Karte (Testlauf 2, 13.10.).
import csv, os, re, subprocess, sys
from lupa import lua51

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RXP = os.environ.get("RXP_DIR", os.path.join(ROOT, "vendor", "rxpguides"))
TAG = sys.argv[1] if len(sys.argv) > 1 else "v4.11.23"
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "build")
VERSION = open(os.path.join(ROOT, "data", "kombi", "VERSION"), encoding="utf-8").read().strip()
FILES = ["Guides/forever/Horde-1-12_Mulgore.lua", "Guides/forever/Horde-12-22_Barrens.lua"]
NEW_GROUP = "Kombiguide (H)"
LAST_NEXT = "RestedXP Forever Guide (H)\\22-24 Hillsbrad"
ZONES = {"1412": "Mulgore", "1413": "The Barrens", "1454": "Orgrimmar", "1456": "Thunder Bluff"}


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def show(path):
    return subprocess.run(["git", "-C", RXP, "show", f"{TAG}:{path}"], capture_output=True, text=True, check=True).stdout


def anchor_regex(anker):
    """'accept 1656' -> Zeile '.accept 1656', 'label Name' -> '#label Name'."""
    cmd, _, arg = anker.strip().partition(" ")
    if cmd == "label":
        return rf"^\s*#label\s+{re.escape(arg.strip())}\s*$"
    return rf"^\s*\.{re.escape(cmd)}\s+{re.escape(arg.strip())}\b"


def world(row, maps):
    """Weltkoordinaten (a, b) und Spielkoordinaten (x, y) oder None, wenn die Zeile keinen Ort hat."""
    if row.get("welt_a") and row.get("welt_b"):
        return float(row["welt_a"]), float(row["welt_b"]), None
    if not (row.get("karte") and row.get("x") and row.get("y")):
        return None
    m = maps.get(row["karte"])
    if not m:
        raise SystemExit(f"Plan-Zeile {row['nr']}: Karte {row['karte']} fehlt in data/karten/forever_karten.csv")
    x, y = float(row["x"]), float(row["y"])
    if not (0 <= x <= 100 and 0 <= y <= 100):
        raise SystemExit(f"Plan-Zeile {row['nr']}: Koordinaten {x}/{y} ausserhalb 0-100")
    a0, b0, a1, b1 = (float(m[k]) for k in ("a0", "b0", "a1", "b1"))
    return a0 + (a1 - a0) * x / 100, b0 + (b1 - b0) * y / 100, (x, y)


# Aktionen der Plan-Tabelle und das RXP-Element, das daraus wird (id, menge aus der Zeile):
#   lernen        .train id                      (Zauber-ID)
#   kaufen        .collect id,menge
#   ziel          .collect id,menge,0,1,24       (Fortschritt «x/menge»; Flags 8 = Bank zählt mit, 16 = keine Quest;
#                                                 Quest 0 und Ziel-Maske 1, weil RXP leere Argumente überspringt)
#   fertigkeit    .skill id,menge                (id = Berufsname, z. B. herbalism; erfüllt ab menge)
#   maxfertigkeit .maxskill id,menge             (z. B. Geselle gelernt: Maximum 150)
#   abgeben       .turnin id   ·   annehmen  .accept id
#   hingehen      nur .goto mit radius           (erledigt beim Ankommen)
#   hinweis       Text und +kurz                 (braucht «bis»; bleibt sichtbar, bis der Ziel-Schritt erledigt ist. Ohne das Kästchen
#                                                 wäre der Schritt nur Text, und RXP erledigt ihn sofort: GuideWindow.lua, UpdateStepCompletion)
#   manuell       +kurz                          (Kästchen zum Abhaken. «.itemcount» in extra prüft RXP nur, wenn der Schritt aktiv wird:
#                                                 fehlt das Material da schon, ist der Schritt erledigt; geht es mittendrin aus, Häkchen setzen)
# «bedingung» und «extra» nehmen mehrere rohe RXP-Zeilen, getrennt mit « // ».
AKTIONEN = ("lernen", "kaufen", "ziel", "fertigkeit", "maxfertigkeit", "abgeben", "annehmen", "hingehen", "hinweis", "manuell")


def make_step(row, maps):
    akt, kurz = row["aktion"], row["kurz"]
    if akt not in AKTIONEN:
        raise SystemExit(f"Plan-Zeile {row['nr']}: Aktion {akt!r} kennt der Generator nicht ({', '.join(AKTIONEN)})")
    text = row["text"].replace("{npc}", f"|cRXP_FRIENDLY_{row['npc']}|r" if row["npc"] else "")
    lines = ["step", f"    #label Kombi{row['nr']}"]
    if row.get("bis"):
        lines.append(f"    #completewith {row['bis']}")
    pos = world(row, maps)
    if pos:
        a, b, xy = pos
        goto = f"    .goto {row['karte']}/1,{a:.2f},{b:.2f}"
        if row.get("radius"):
            goto += f",{row['radius']}"
        if xy:
            goto += f"--c:{ZONES.get(row['karte'], row['karte'])},{xy[0]:.1f},{xy[1]:.1f} (Spielkoordinaten)"
        lines.append(goto)
    elif akt == "hingehen":
        raise SystemExit(f"Plan-Zeile {row['nr']}: «hingehen» braucht einen Ort")
    if akt == "hingehen" and not row.get("radius"):
        raise SystemExit(f"Plan-Zeile {row['nr']}: «hingehen» braucht einen Radius")
    if akt == "hinweis" and not row.get("bis"):
        raise SystemExit(f"Plan-Zeile {row['nr']}: «hinweis» braucht «bis» (Label oder next)")
    lines.append(f"    >>Kombiguide: {text}")
    k = f" >>{kurz}" if kurz else ""
    if akt == "lernen":
        lines.append(f"    .train {row['id']}{k}")
    elif akt == "kaufen":
        lines.append(f"    .collect {row['id']},{row['menge'] or 1}{k}")
    elif akt == "ziel":
        lines.append(f"    .collect {row['id']},{row['menge']},0,1,24{k}")
    elif akt == "fertigkeit":
        lines.append(f"    .skill {row['id']},{row['menge']}{k}")
    elif akt == "maxfertigkeit":
        lines.append(f"    .maxskill {row['id']},{row['menge']}{k}")
    elif akt == "abgeben":
        lines.append(f"    .turnin {row['id']}{k}")
    elif akt == "annehmen":
        lines.append(f"    .accept {row['id']}{k}")
    elif akt == "manuell":
        if not kurz:
            raise SystemExit(f"Plan-Zeile {row['nr']}: «manuell» braucht «kurz» (Text am Kästchen)")
        lines.append(f"    +{kurz}")
    elif akt == "hinweis":
        lines.append(f"    +{kurz or 'Hinweis gelesen'}")
    for cond in (row.get("bedingung") or "").split(" // "):
        if cond.strip():
            lines.append("    " + cond.strip())
    for extra in (row.get("extra") or "").split(" // "):
        if extra.strip():
            lines.append("    " + extra.strip())
    if row["npc"]:
        lines.append(f"    .target {row['npc']}")
    return lines


def split_steps(body):
    head, steps, cur = [], [], None
    for l in body.split("\n"):
        if re.match(r"^\s*step\b", l):
            if cur is not None:
                steps.append(cur)
            cur = [l]
        elif cur is None:
            head.append(l)
        else:
            cur.append(l)
    if cur is not None:
        steps.append(cur)
    return head, steps


plan = read_csv(os.path.join(ROOT, "data", "kombi", "plan.csv"))
maps = {m["karte"]: m for m in read_csv(os.path.join(ROOT, "data", "karten", "forever_karten.csv"))}

# Zeilen mit gleichem Guide, Anker und Position bilden einen Block (Reihenfolge wie in der Tabelle)
blocks = {}
for row in plan:
    blocks.setdefault((row["guide"], row["anker"], row["position"]), []).append(row)

report, problems, out_blocks, used, guide_labels = [], [], [], set(), {}
for path in FILES:
    for body in re.findall(r"RXPGuides\.RegisterGuide\(\[\[(.*?)\]\]\)", show(path), re.S):
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
        for (gname, anker, pos), rows in blocks.items():
            if gname != name:
                continue
            rx = anchor_regex(anker)
            hits = [i for i, st in enumerate(steps) if any(re.search(rx, x) for x in st)]
            if len(hits) != 1:
                problems.append(f"{name}: Anker '{anker}' {len(hits)}x gefunden")
                continue
            i = hits[0]
            if pos == "nach":
                j = i + 1
                while j - 1 < len(steps) and any(re.match(r"^\s*#completewith\s+next\b", x) for x in steps[j - 1]):
                    j += 1
            elif pos == "vor":
                j = i
                while j - 1 >= 0 and any(re.match(r"^\s*#completewith\s+next\b", x) for x in steps[j - 1]):
                    j -= 1
            else:
                problems.append(f"{name}: Position '{pos}' unbekannt (vor/nach)")
                continue
            new = [make_step(r, maps) for r in rows]
            steps[j:j] = new
            used.update(r["nr"] for r in rows)
            report.append(f"{name}: {len(new)} Schritte {pos} '{anker}' (RXP-Schritt {i + 1}) eingefügt, Zeilen {', '.join(r['nr'] for r in rows)}")
        report.append(f"{name}: {len(steps)} Schritte")
        block = "\n".join(newhead) + "\n" + "\n".join("\n".join(s) for s in steps)
        guide_labels[name] = set(re.findall(r"^\s*#label\s+(\S+)\s*$", block, re.M))
        out_blocks.append(block)

missing = [r["nr"] for r in plan if r["nr"] not in used]
if missing:
    problems.append("nicht eingefügt: Plan-Zeilen " + ", ".join(missing))

header = ("-- Kombi-Guide " + VERSION + " (WoW Forever, Horde): RXP-Gratis-Route 1-22 mit Berufsschritten aus data/kombi/plan.csv\n"
          "-- Basis RestedXP " + TAG + ", Quelle github.com/RestedXP/RXPGuides (CC BY-NC-SA 4.0), bearbeitet, gleiche Lizenz\n"
          "if not (RXPGuides and RXPGuides.RegisterGuide) then return end\n"
          "if UnitFactionGroup(\"player\") == \"Alliance\" then return end\n")
lua_src = header + "\n".join(f"RXPGuides.RegisterGuide([[\n{b}\n]])\n" for b in out_blocks)

# Prüfen: Lua-Syntax, Kopf, Befehle, eigene Texte
L = lua51.LuaRuntime(unpack_returned_tuples=True)
L.execute('captured = {}; RXPGuides = {RegisterGuide = function(s) table.insert(captured, s) end}; UnitFactionGroup = function() return "Horde" end')
fn = L.globals().loadstring(lua_src)
if fn is None:
    raise SystemExit("Lua-Syntaxfehler")
fn()
cap = L.globals().captured
fsrc = show("functions.lua")
funcs = set(re.findall(r"function addon\.functions\.(\w+)\s*\(", fsrc)) | set(re.findall(r'addon\.functions\["(\w+)"\]\s*=', fsrc)) | set(re.findall(r"addon\.functions\.(\w+)\s*=", fsrc))
unknown = set()
for i in range(1, len(cap) + 1):
    t = cap[i]
    h = t.split("\nstep")[0]
    for need in ("#forever", "#name", "#group " + NEW_GROUP, "<< Horde"):
        if need not in h:
            problems.append(f"Guide {i}: {need} fehlt im Kopf")
    if "#defaultfor" in h:
        problems.append(f"Guide {i}: #defaultfor noch da")
    for m in re.finditer(r"^\s*\.(\w+)", t, re.M):
        if m.group(1) not in funcs:
            unknown.add(m.group(1))
for row in plan:
    for field in ("text", "kurz", "bedingung", "npc", "bis", "extra"):
        value = row.get(field) or ""
        if "--" in value:
            problems.append(f"Plan-Zeile {row['nr']}: '--' in {field}")
        if "[[" in value or "]]" in value:
            problems.append(f"Plan-Zeile {row['nr']}: '[[' oder ']]' in {field}")
    for value in (row.get("bedingung") or "").split(" // ") + (row.get("extra") or "").split(" // "):
        if re.search(r"^\s*\.\w+\s+[^>]*,,", value):
            problems.append(f"Plan-Zeile {row['nr']}: leeres Argument (',,') in '{value.strip()}': RXP überspringt es")
    bis = row.get("bis") or ""
    if bis and bis != "next" and bis not in guide_labels.get(row["guide"], set()):
        problems.append(f"Plan-Zeile {row['nr']}: Label '{bis}' (bis) gibt es in '{row['guide']}' nicht")
if unknown:
    problems.append("unbekannte Befehle: " + ", ".join(sorted(unknown)))
report.append(f"Lua 5.1 ok, {len(cap)} Guides registriert, {len(used)} Plan-Zeilen eingefügt, Datei {len(lua_src) // 1024} KB")

d = os.path.join(OUT, "RXPGuides_KombiGuide")
os.makedirs(d, exist_ok=True)
open(os.path.join(d, "Kombi_Guide.lua"), "w", encoding="utf-8").write(lua_src)
open(os.path.join(d, "RXPGuides_KombiGuide.toc"), "w", encoding="utf-8").write(
    "## Interface: 16001\n## Title: RXP Guides Kombiguide\n"
    "## Notes: Kombi-Guide " + VERSION + ": RXP-Gratis-Route 1-22 (Basis " + TAG + ") mit Berufsschritten. CC BY-NC-SA 4.0\n"
    "## Author: ludes88\n## Version: " + VERSION + "-" + TAG + "\n## Dependencies: RXPGuides\n\nKombi_Guide.lua\n")
print("\n".join(report))
print("Probleme: " + ("; ".join(problems) if problems else "keine"))
sys.exit(1 if problems else 0)
